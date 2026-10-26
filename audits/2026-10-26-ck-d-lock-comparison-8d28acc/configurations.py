"""Five explicit ordered disk patches for the C6--C8 D/locking comparison.

The Birkhoff free completion is transcribed from Steinberger, Fig. 1, with
integer coordinates reflected vertically so that every listed bounded face and
the ordered ring are counterclockwise. The remaining patches are explicit
constructions: the free completion of an adjacent degree-five pair and wheels.
No Four Color Theorem, planar catalogue, or drawing library is used to validate
the embeddings. A named patch is not itself an assertion of D-reducibility.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
import json


STEINBERGER = "https://arxiv.org/pdf/0905.0043"


def _edge(a, b):
    return tuple(sorted((a, b)))


def _area2(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _on_segment(a, b, c):
    return (_area2(a, b, c) == 0
            and min(a[0], b[0]) <= c[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))


def _intersect(a, b, c, d):
    signs = (_area2(a, b, c), _area2(a, b, d),
             _area2(c, d, a), _area2(c, d, b))
    if signs[0] * signs[1] < 0 and signs[2] * signs[3] < 0:
        return True
    return ((signs[0] == 0 and _on_segment(a, b, c))
            or (signs[1] == 0 and _on_segment(a, b, d))
            or (signs[2] == 0 and _on_segment(c, d, a))
            or (signs[3] == 0 and _on_segment(c, d, b)))


def _inside(point, polygon):
    """Exact winding-number test; boundary points are not interior points."""
    winding = 0
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        if _on_segment(a, b, point):
            return False
        if a[1] <= point[1] < b[1] and _area2(a, b, point) > 0:
            winding += 1
        elif b[1] <= point[1] < a[1] and _area2(a, b, point) < 0:
            winding -= 1
    return winding == 1


def validate_disk(configuration):
    """Validate the literal graph, ordered ring, CCW faces and integer drawing.

    Raises ValueError on any failed obligation. The result is a compact evidence
    summary; all geometric predicates use exact integer arithmetic. Integer or
    JSON-string vertex keys are accepted for the positions dictionary.
    """
    name = configuration.get("name", "unnamed")

    def require(condition, obligation):
        if not condition:
            raise ValueError(f"{name}: {obligation}")

    vertices = configuration["vertices"]
    ring = configuration["ring"]
    internal = configuration["internal"]
    edges = configuration["edges"]
    faces = configuration["faces"]
    positions = configuration["positions"]
    require(all(type(v) is int for v in vertices), "vertex IDs must be integers")
    require(len(vertices) == len(set(vertices)), "vertex IDs must be distinct")
    vertex_set = set(vertices)
    require(len(ring) >= 3 and len(ring) == len(set(ring)), "ring must be a simple cycle")
    require(len(internal) == len(set(internal)), "internal IDs must be distinct")
    require(set(ring).isdisjoint(internal), "ring and internal vertices overlap")
    require(set(ring) | set(internal) == vertex_set, "ring/internal partition is incomplete")
    try:
        points = {v: positions[v] if v in positions else positions[str(v)] for v in vertices}
    except KeyError as exc:
        raise ValueError(f"{name}: every vertex needs a position") from exc
    require(len(positions) == len(vertices), "positions must contain exactly the graph vertices")
    require(all(len(p) == 2 and all(type(c) is int for c in p) for p in points.values()),
            "positions must be integer pairs")
    require(len({tuple(p) for p in points.values()}) == len(vertices),
            "vertex positions must be distinct")
    require(all(len(e) == 2 and e[0] != e[1] and set(e) <= vertex_set for e in edges),
            "edges must have two distinct original endpoints")
    edge_set = {_edge(*edge) for edge in edges}
    require(len(edge_set) == len(edges), "original edges must not be duplicated")
    ring_edges = {_edge(a, b) for a, b in zip(ring, ring[1:] + ring[:1])}
    require(ring_edges <= edge_set, "all original ring edges must be present")
    require(all(len(f) == 3 and len(set(f)) == 3 and set(f) <= vertex_set for f in faces),
            "faces must be triples of distinct original vertices")
    require(len({tuple(sorted(f)) for f in faces}) == len(faces), "faces must be distinct")
    incidence = Counter(_edge(f[i], f[(i + 1) % 3]) for f in faces for i in range(3))
    directed = Counter((f[i], f[(i + 1) % 3]) for f in faces for i in range(3))
    require(set(incidence) == edge_set, "faces must cover exactly all original edges")
    require(all(incidence[e] == (1 if e in ring_edges else 2) for e in edge_set),
            "ring edges need one bounded face and all other edges need two")
    require(all(directed[(a, b)] == directed[(b, a)] == 1
                for a, b in edge_set - ring_edges),
            "the two incidences of every interior edge must have opposite orientation")
    require(all(directed[(a, b)] == 1 and directed[(b, a)] == 0
                for a, b in zip(ring, ring[1:] + ring[:1])),
            "face orientation must agree with the CCW ring")
    require(all(_area2(*(points[v] for v in f)) > 0 for f in faces),
            "every bounded triangle must have strictly positive CCW area")
    boundary_area = sum(points[a][0] * points[b][1] - points[a][1] * points[b][0]
                        for a, b in zip(ring, ring[1:] + ring[:1]))
    require(boundary_area > 0, "the boundary polygon must be counterclockwise")
    require(sum(_area2(*(points[v] for v in f)) for f in faces) == boundary_area,
            "bounded triangle areas must exactly fill the boundary area")
    for a, b in edges:
        for v in vertices:
            if v not in (a, b):
                require(not _on_segment(points[a], points[b], points[v]),
                        f"original vertex {v} lies on edge {(a, b)}")
    for first, second in combinations(edges, 2):
        if set(first).isdisjoint(second):
            require(not _intersect(*(points[v] for v in (*first, *second))),
                    f"disjoint original edges {first} and {second} intersect")
    polygon = [points[v] for v in ring]
    require(all(_inside(points[v], polygon) for v in internal),
            "every internal vertex must lie strictly inside the ordered ring")
    neighbours = {v: set() for v in vertices}
    for a, b in edges:
        neighbours[a].add(b)
        neighbours[b].add(a)
    seen = {vertices[0]}
    pending = [vertices[0]]
    for v in pending:
        for w in neighbours[v] - seen:
            seen.add(w)
            pending.append(w)
    require(seen == vertex_set, "the original graph must be connected")
    require(len(vertices) - len(edges) + len(faces) == 1, "Euler disk equation failed")
    require(len(edges) == 3 * len(vertices) - len(ring) - 3,
            "triangulated-disk edge count failed")
    return dict(
        name=name, vertices=len(vertices), edges=len(edges), ring_size=len(ring),
        bounded_triangular_faces=len(faces),
        internal_degrees={v: len(neighbours[v]) for v in internal},
        minimum_internal_degree=min((len(neighbours[v]) for v in internal), default=None),
        twice_boundary_area=boundary_area,
        all_embedding_obligations_passed=True,
        checks=["distinct IDs and positions", "exact vertex partition", "original edge coverage",
                "face incidence and orientation", "positive triangle areas", "exact filled area",
                "no vertex on a nonincident edge", "no crossings or disjoint-edge contacts",
                "internal points strictly inside ring", "connected original graph", "Euler disk"])


def _make(name, ring_size, internal_count, extra_edges, faces, positions, primary_source):
    return dict(
        name=name, vertices=list(range(ring_size + internal_count)),
        ring=list(range(ring_size)), internal=list(range(ring_size, ring_size + internal_count)),
        edges=[list(e) for e in sorted({_edge(i, (i + 1) % ring_size)
                                      for i in range(ring_size)}
                                     | {_edge(*e) for e in extra_edges})],
        faces=[list(f) for f in faces],
        positions={v: list(point) for v, point in enumerate(positions)},
        primary_source=primary_source)


def configurations():
    """Return fresh dictionaries for BD, adjacent 5--5, W6, W7 and W8."""
    diamond = _make(
        "birkhoff_diamond", 6, 4,
        [(6, 7), (7, 8), (8, 9), (9, 6), (7, 9),
         (0, 6), (1, 6), (1, 7), (2, 7), (2, 8),
         (3, 8), (4, 8), (4, 9), (5, 9), (5, 6)],
        [(0, 1, 6), (1, 7, 6), (1, 2, 7), (2, 8, 7),
         (2, 3, 8), (3, 4, 8), (4, 9, 8), (4, 5, 9),
         (5, 6, 9), (5, 0, 6), (6, 7, 9), (7, 8, 9)],
        [(-3, 0), (-2, -2), (2, -2), (3, 0), (2, 2), (-2, 2),
         (-1, 0), (0, -1), (1, 0), (0, 1)],
        dict(kind="primary-paper figure transcription", url=STEINBERGER,
             title="An Unavoidable Set of D-Reducible Configurations",
             location="Figure 1 (PDF page 10); kernel and free-completion distinction on PDF pages 13--14",
             construction="Explicit labeling and vertical reflection of Figure 1, left; four internal degree-five vertices."))
    pair = _make(
        "adjacent_5_5", 6, 2,
        [(6, 7)] + [(6, i) for i in (0, 1, 2, 3)] + [(7, i) for i in (0, 3, 4, 5)],
        [(0, 1, 6), (1, 2, 6), (2, 3, 6), (3, 7, 6),
         (3, 4, 7), (4, 5, 7), (5, 0, 7), (0, 6, 7)],
        [(0, 3), (-2, 2), (-2, -2), (0, -3), (2, -2), (2, 2), (-1, 0), (1, 0)],
        dict(kind="explicit free-completion construction", url=STEINBERGER,
             title="An Unavoidable Set of D-Reducible Configurations",
             location="Section 3 free-completion definition (PDF page 14)",
             construction="Core K2 with both prescribed degrees five; the explicit edges and embedding are independently validated here, not copied from a named source figure."))
    wheel_polygons = {
        6: [(-3, 0), (-2, -2), (2, -2), (3, 0), (2, 2), (-2, 2)],
        7: [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2)],
        8: [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)],
    }
    wheels = [_make(
        f"wheel_{k}", k, 1,
        [(i, k) for i in range(k)], [(i, (i + 1) % k, k) for i in range(k)],
        wheel_polygons[k] + [(0, 0)],
        dict(kind="explicit construction", url=None,
             title=f"Ordered {k}-cycle with one internal vertex adjacent to its complete ring",
             location="This audit's literal edge and face definition",
             construction="No external theorem or catalogue is needed to define or validate this wheel."))
        for k in (6, 7, 8)]
    return [diamond, pair, *wheels]


if __name__ == "__main__":
    print(json.dumps([validate_disk(c) for c in configurations()], indent=2, sort_keys=True))
