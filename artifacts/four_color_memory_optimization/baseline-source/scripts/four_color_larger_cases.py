"""Deterministic larger original graphs with independent exact colour oracles.

These are structured finite controls, not coverage of arbitrary planar graphs.
Every generated constraint is an original edge or a literal fixed colour.  The
oracles use the stated graph decompositions, never solver factors or records.

``project(scope)`` returns the complete global solution projection in exactly
the supplied original-vertex order, with literal colours 0..3.  An explicit
``ProjectionLimit`` means that the requested complete projection is too large;
it never substitutes an empty relation for an incomplete calculation.
"""

from __future__ import annotations

from itertools import combinations, permutations, product
from math import prod

from four_color_lab import normalize_graph


PROJECTION_ROW_CEILING = 100000
ENDPOINT_DOMAINS = {
    "compatible": (0, 1),
    "overlap": (1, 2),
    "incompatible": (2, 3),
}


class ProjectionLimit(ValueError):
    """The exact requested projection exceeds the permitted row count."""

    def __init__(self, row_count, max_rows):
        self.row_count = row_count
        self.max_rows = max_rows
        super().__init__(f"exact projection needs {row_count} rows; limit is {max_rows}")


def equality_tree_case(shape, edge_count, endpoint):
    """Build a tree of K5-e equality gadgets and four fixed pendant vertices.

    The two nonadjacent hubs of each K5-e share a private triangle.  Its three
    distinct colours force both hubs to the fourth colour.  The hub incidence
    graph is a tree: blocks only meet at articulation vertices, so their planar
    embeddings can be glued.  Closing the hub tree into a cycle is not used.

    Arbitrary positive sizes are accepted for small independent tests; the
    experiment suite uses chain sizes 4/12/24 and binary sizes 6/14/30.
    """
    if shape not in ("chain", "binary"):
        raise ValueError("shape must be chain or binary")
    if type(edge_count) is not int or edge_count < 1:
        raise ValueError("edge_count must be a positive integer")
    if endpoint not in ENDPOINT_DOMAINS:
        raise ValueError("unknown endpoint condition")

    hubs = list(range(edge_count + 1))
    hub_edges = [[i - 1 if shape == "chain" else (i - 1) // 2, i]
                 for i in range(1, edge_count + 1)]
    edges, triangles = [], []
    next_vertex = len(hubs)
    for left, right in hub_edges:
        triangle = list(range(next_vertex, next_vertex + 3))
        next_vertex += 3
        edges.extend([list(pair) for pair in combinations(triangle, 2)])
        edges.extend([[hub, vertex] for hub in (left, right) for vertex in triangle])
        triangles.append({"hubs": [left, right], "vertices": triangle})

    root, far = hubs[0], hubs[-1]
    far_domain = ENDPOINT_DOMAINS[endpoint]
    fixed_leaves, fixed = [], []
    for role, hub, domain in (("root", root, (0, 1)), ("far", far, far_domain)):
        excluded = [color for color in range(4) if color not in domain]
        leaves = list(range(next_vertex, next_vertex + 2))
        next_vertex += 2
        for leaf, color in zip(leaves, excluded):
            edges.append([hub, leaf])
            fixed.append([leaf, color])
        fixed_leaves.append({"role": role, "hub": hub, "vertices": leaves,
                             "fixed_colors": excluded, "hub_domain": list(domain)})

    name = f"equality-{shape}-m{edge_count}-{endpoint}"
    metadata = {
        "family": "private-triangle-equality-tree",
        "shape": shape,
        "edge_count": edge_count,
        "endpoint": endpoint,
        "hubs": hubs,
        "hub_tree_edges": hub_edges,
        "private_triangles": triangles,
        "fixed_leaves": fixed_leaves,
        "planarity": "Planar K5-e blocks glued only at hub-tree articulation vertices, plus pendant leaves.",
        "solution_description": "All hubs share one colour in the intersection of the endpoint domains; each private triangle independently permutes the other three literal colours.",
        "expected_vertex_count": 4 * edge_count + 5,
    }
    graph = normalize_graph({"name": name, "vertices": list(range(next_vertex)),
                             "edges": edges, "fixed": fixed,
                             "source_metadata": metadata})
    descriptor = {
        "kind": "private-triangle-equality-tree-v1",
        "shape": shape,
        "edge_count": edge_count,
        "endpoint": endpoint,
        "common_hub_colours": sorted(set((0, 1)) & set(far_domain)),
        "solution_count_formula": "len(common_hub_colours) * 6 ** edge_count",
    }
    return {"name": name, "graph": graph, "oracle": descriptor}


def double_wheel_case(rim_size):
    """Build a rim cycle with two distinct fixed-colour universal rim hubs."""
    if type(rim_size) is not int or rim_size < 3:
        raise ValueError("rim_size must be an integer at least three")
    rim = list(range(rim_size))
    hubs = [rim_size, rim_size + 1]
    edges = [[i, (i + 1) % rim_size] for i in rim]
    edges.extend([[hub, vertex] for hub in hubs for vertex in rim])
    name = f"double-wheel-rim{rim_size}-fixed23"
    graph = normalize_graph({
        "name": name, "vertices": rim + hubs, "edges": edges,
        "fixed": [[hubs[0], 2], [hubs[1], 3]],
        "source_metadata": {
            "family": "fixed-distinct-hub-double-wheel",
            "rim": rim, "hubs": hubs, "fixed_hub_colours": [2, 3],
            "planarity": "Embed the rim as a polygon with one universal hub on each side.",
            "solution_description": "The fixed hubs leave literal colours 0 and 1 on the rim; an even rim has its two alternating solutions and an odd rim has none.",
        },
    })
    descriptor = {"kind": "fixed-distinct-hub-double-wheel-v1",
                  "rim_size": rim_size, "solution_count": 2 if rim_size % 2 == 0 else 0}
    return {"name": name, "graph": graph, "oracle": descriptor}


def generate_cases():
    """Return the 24 deterministic cases as JSON-serializable dictionaries."""
    cases = [equality_tree_case(shape, size, endpoint)
             for shape, sizes in (("chain", (4, 12, 24)), ("binary", (6, 14, 30)))
             for size in sizes for endpoint in ENDPOINT_DOMAINS]
    cases.extend(double_wheel_case(size) for size in (9, 10, 25, 26, 97, 98))
    return cases


class StructuredOracle:
    """A graph-bound exact oracle for one of the two finite control families."""

    def __init__(self, case):
        if not isinstance(case, dict) or not isinstance(case.get("oracle"), dict):
            raise ValueError("case must have graph and oracle objects")
        descriptor = case["oracle"]
        kind = descriptor.get("kind")
        if kind == "private-triangle-equality-tree-v1":
            expected = equality_tree_case(descriptor.get("shape"), descriptor.get("edge_count"),
                                          descriptor.get("endpoint"))
        elif kind == "fixed-distinct-hub-double-wheel-v1":
            expected = double_wheel_case(descriptor.get("rim_size"))
        else:
            raise ValueError("unsupported oracle descriptor")

        # Bind the decomposition to the complete original graph.  Vertex order
        # can change; identities, every edge, every fixed value and source
        # metadata must still agree.  Extra/missing edges invalidate this oracle.
        graph = normalize_graph(case.get("graph"))
        original = expected["graph"]
        if (descriptor != expected["oracle"]
                or set(graph["vertices"]) != set(original["vertices"])
                or graph["edges"] != original["edges"]
                or sorted(graph["fixed"]) != sorted(original["fixed"])
                or graph.get("source_metadata") != original["source_metadata"]):
            raise ValueError("oracle descriptor does not match the complete original graph")

        self.graph = graph
        self.kind = kind
        self.vertices = tuple(graph["vertices"])
        self._vertex_set = frozenset(self.vertices)
        self._fixed = dict(graph["fixed"])
        self._edges = tuple(map(tuple, graph["edges"]))
        source = graph["source_metadata"]
        if kind == "private-triangle-equality-tree-v1":
            self.hubs = tuple(source["hubs"])
            self.triangles = tuple(tuple(record["vertices"])
                                   for record in source["private_triangles"])
            self.common_hub_colours = tuple(descriptor["common_hub_colours"])
            self.solution_count = len(self.common_hub_colours) * 6 ** len(self.triangles)
            self._triangle_index = {vertex: i for i, triangle in enumerate(self.triangles)
                                    for vertex in triangle}
            self._hub_set = frozenset(self.hubs)
        else:
            self.rim = tuple(source["rim"])
            self.hubs = tuple(source["hubs"])
            self.solution_count = descriptor["solution_count"]

    def _scope(self, scope):
        scope = tuple(scope)
        if any(type(vertex) is not int or vertex not in self._vertex_set for vertex in scope):
            raise ValueError("projection scope must contain original integer vertex identities")
        return scope

    def _triangle_scope(self, scope):
        selected = set(scope)
        return [(triangle, tuple(v for v in triangle if v in selected))
                for triangle in self.triangles if any(v in selected for v in triangle)]

    def projection_count(self, scope):
        """Compute the exact projection row count without enumerating rows."""
        scope = self._scope(scope)
        if not self.solution_count:
            return 0
        if self.kind == "fixed-distinct-hub-double-wheel-v1":
            return 2 if any(v in self.rim for v in scope) else 1
        selected = self._triangle_scope(scope)
        # A selected k-coordinate triangle has P(3,k) rows for each common
        # hub colour.  There are at most two possible hub colours.  If no hub
        # is selected, their projections intersect in P(2,k) per triangle.
        per_colour = prod((1, 3, 6, 6)[len(vertices)] for _, vertices in selected)
        count = len(self.common_hub_colours) * per_colour
        if len(self.common_hub_colours) == 2 and not any(v in self._hub_set for v in scope):
            count -= prod((1, 2, 2, 0)[len(vertices)] for _, vertices in selected)
        return count

    def project(self, scope, max_rows=PROJECTION_ROW_CEILING):
        """Return all globally extendable tuples in the supplied literal frame.

        Repeated vertices, when supplied, retain their repeated coordinates.
        Rows alone are deduplicated as required for a mathematical relation.
        The independent exact count is checked before rows are materialized.
        """
        scope = self._scope(scope)
        if type(max_rows) is not int or max_rows < 0:
            raise ValueError("max_rows must be a nonnegative integer")
        effective_limit = min(max_rows, PROJECTION_ROW_CEILING)
        count = self.projection_count(scope)
        if count > effective_limit:
            raise ProjectionLimit(count, effective_limit)
        if not count:
            return frozenset()
        if self.kind == "fixed-distinct-hub-double-wheel-v1":
            rows = frozenset(tuple(assignment[v] for v in scope)
                             for assignment in self._double_wheel_assignments())
        else:
            selected = self._triangle_scope(scope)
            rows = set()
            for colour in self.common_hub_colours:
                base = dict(self._fixed)
                base.update((hub, colour) for hub in self.hubs)
                other = tuple(c for c in range(4) if c != colour)
                choices = [tuple(permutations(other, len(vertices)))
                           for _, vertices in selected]
                for selected_rows in product(*choices):
                    assignment = dict(base)
                    for (_, vertices), values in zip(selected, selected_rows):
                        assignment.update(zip(vertices, values))
                    rows.add(tuple(assignment[v] for v in scope))
            rows = frozenset(rows)
        if len(rows) != count:
            raise AssertionError("independent projection count and literal rows disagree")
        return rows

    def _double_wheel_assignments(self):
        if not self.solution_count:
            return
        for first in (0, 1):
            assignment = dict(self._fixed)
            assignment.update((vertex, (first + i) % 2) for i, vertex in enumerate(self.rim))
            yield assignment

    def witnesses(self, limit=4):
        """Return deterministic full colourings checked on original constraints."""
        if type(limit) is not int or limit < 0:
            raise ValueError("limit must be a nonnegative integer")
        if not limit or not self.solution_count:
            return []
        result = []
        if self.kind == "fixed-distinct-hub-double-wheel-v1":
            assignments = self._double_wheel_assignments()
        else:
            def equality_assignments():
                for colour in self.common_hub_colours:
                    choices = tuple(permutations(c for c in range(4) if c != colour))
                    for triangle_rows in product(choices, repeat=len(self.triangles)):
                        assignment = dict(self._fixed)
                        assignment.update((hub, colour) for hub in self.hubs)
                        for triangle, values in zip(self.triangles, triangle_rows):
                            assignment.update(zip(triangle, values))
                        yield assignment
            assignments = equality_assignments()
        for assignment in assignments:
            colors = [assignment[v] for v in self.vertices]
            if not self.validate_witness(colors):
                raise AssertionError("structural witness fails an original edge or fixed colour")
            result.append(colors)
            if len(result) >= limit:
                break
        return result

    def validate_witness(self, colors):
        """Check only original vertex identities, original edges and fixed values."""
        if (not isinstance(colors, (list, tuple)) or len(colors) != len(self.vertices)
                or any(type(c) is not int or c not in range(4) for c in colors)):
            return False
        assignment = dict(zip(self.vertices, colors))
        return (all(assignment[u] != assignment[v] for u, v in self._edges)
                and all(assignment[v] == color for v, color in self._fixed.items()))


def create_oracle(case):
    """Validate and construct the independent exact oracle for one case."""
    return StructuredOracle(case)
