"""Independent literal-graph checks for the fixed degree-5 star audit.

No imports from the producer, catalogue checker, or topology implementation.
Colour vectors are always indexed by the graph's sorted, original integer IDs.
The rotation convention is clockwise neighbours and predecessor face walks.
"""

from collections import Counter


PATTERNS = [
    [0, 1, 0, 1, 2], [0, 1, 0, 2, 1], [0, 1, 0, 2, 3],
    [0, 1, 2, 0, 1], [0, 1, 2, 0, 2], [0, 1, 2, 0, 3],
    [0, 1, 2, 1, 2], [0, 1, 2, 1, 3], [0, 1, 2, 3, 1],
    [0, 1, 2, 3, 2],
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _literal_graph(graph):
    """Parse only literal graph data; never infer or renumber a vertex."""
    require(isinstance(graph, dict), "graph must be a dictionary")
    require({"nodes", "boundary", "edges"} <= set(graph), "missing literal graph field")
    nodes = graph["nodes"]
    require(isinstance(nodes, list), "nodes must be a list")
    require(all(type(v) is int for v in nodes), "noninteger vertex label")
    require(nodes == sorted(set(nodes)), "nodes must be distinct and sorted")
    require(isinstance(graph["boundary"], list) and
            all(type(v) is int for v in graph["boundary"]) and
            graph["boundary"] == [0, 1, 2, 3, 4], "wrong named boundary")
    require(set(range(5)) <= set(nodes), "missing boundary vertex")
    adjacency = {v: set() for v in nodes}
    edges = set()
    require(isinstance(graph["edges"], list), "edges must be a list")
    for edge in graph["edges"]:
        require(isinstance(edge, list) and len(edge) == 2, "invalid edge record")
        u, v = edge
        require(type(u) is int and type(v) is int, "noninteger edge label")
        require(u in adjacency and v in adjacency, "edge uses missing vertex")
        require(u != v, "self-loop")
        key = (min(u, v), max(u, v))
        require(key not in edges, "parallel edge")
        edges.add(key)
        adjacency[u].add(v)
        adjacency[v].add(u)
    for i in range(5):
        require((min(i, (i + 1) % 5), max(i, (i + 1) % 5)) in edges,
                "missing original boundary edge")
    return nodes, edges, adjacency


def enumerate_lifts(graph, beta):
    """Return every proper four-colouring extending the fixed boundary beta.

    This is MRV backtracking with domains recomputed from the current partial
    assignment.  It neither consumes nor filters producer colourings.  Isolated
    vertices and nonconsecutive original labels retain all four choices.
    """
    nodes, edges, adjacency = _literal_graph(graph)
    require(isinstance(beta, (list, tuple)) and len(beta) == 5,
            "boundary colouring must have five entries")
    require(all(type(c) is int and 0 <= c < 4 for c in beta),
            "boundary colour outside 0..3")
    assigned = dict(zip(graph["boundary"], beta))
    if any(u in assigned and v in assigned and assigned[u] == assigned[v]
           for u, v in edges):
        return []
    free = set(nodes) - set(assigned)
    result = []

    def search():
        if not free:
            result.append([assigned[v] for v in nodes])
            return
        chosen = None
        chosen_domain = None
        chosen_key = None
        for v in free:
            forbidden = {assigned[w] for w in adjacency[v] if w in assigned}
            domain = [c for c in range(4) if c not in forbidden]
            if not domain:
                return
            key = (len(domain), -len(adjacency[v] & free), v)
            if chosen_key is None or key < chosen_key:
                chosen, chosen_domain, chosen_key = v, domain, key
        free.remove(chosen)
        for colour in chosen_domain:
            assigned[chosen] = colour
            search()
        del assigned[chosen]
        free.add(chosen)

    search()
    return sorted(result)


def _cycle_key(walk):
    require(bool(walk), "empty face walk")
    return min(tuple(walk[i:] + walk[:i]) for i in range(len(walk)))


def verify_operation(source, mark, operation):
    """Independently check literal source-to-operation maps and admission.

    The main verifier separately checks every supplied rotation and face.  This
    function uses direct edge arithmetic, source face incidence, and quotient
    blocks; it does not invoke the operation producer or its surgery code.
    """
    from itertools import combinations

    nodes, edges, adjacency = _literal_graph(source)
    v, link = mark["v"], mark["L"]
    require(v not in source["boundary"] and v in adjacency, "invalid marked centre")
    require(len(adjacency[v]) == 5, "marked centre does not have degree five")
    require(link == source["rotation"][str(v)], "L is not the original cyclic neighbour list")
    rest = mark["deleted_center_graph"]
    rest_nodes, rest_edges, _ = _literal_graph(rest)
    require(rest_nodes == [u for u in nodes if u != v], "centre deletion changes other labels")
    require(rest_edges == {e for e in edges if v not in e}, "wrong centre-deletion edges")
    for u in rest_nodes:
        require(_cycle_key(rest["rotation"][str(u)]) ==
                _cycle_key([w for w in source["rotation"][str(u)] if w != v]),
                "centre deletion changes inherited rotation")
    target = operation["graph"]
    target_nodes, target_edges, _ = _literal_graph(target)
    kind = operation["kind"]
    if kind in ("delete", "flip"):
        spoke = tuple(sorted(operation["spoke"]))
        require(spoke in edges and v in spoke, "operation spoke is not original")
        require(target_nodes == nodes, "spoke operation changes original vertex labels")
        expected_edges = edges - {spoke}
        if kind == "flip":
            u = next(w for w in spoke if w != v)
            incident = [f for f in source["faces"]
                        for a, b in zip(f, f[1:] + f[:1]) if {a, b} == {u, v}]
            require(len(incident) == 2 and all(len(f) == 3 for f in incident),
                    "flip needs two incident triangular face walks")
            require(all(_cycle_key(f) != tuple(source["boundary"]) for f in incident),
                    "flip uses the outer face")
            quad = set(incident[0]) | set(incident[1])
            require(len(quad) == 4, "flip quadrilateral repeats a vertex")
            opposite = tuple(sorted(quad - {u, v}))
            require(tuple(operation["diagonal"]) == opposite and opposite not in edges,
                    "wrong or already present opposite diagonal")
            expected_edges.add(opposite)
        require(target_edges == expected_edges, "wrong literal spoke-operation edges")
        for u in nodes:
            expected_rotation = [w for w in source["rotation"][str(u)]
                                 if tuple(sorted((u, w))) != spoke]
            inherited_rotation = target["rotation"][str(u)][:]
            if kind == "flip" and u in opposite:
                inherited_rotation.remove(next(w for w in opposite if w != u))
            require(_cycle_key(expected_rotation) == _cycle_key(inherited_rotation),
                    "spoke operation changes original surviving rotation")
    elif kind == "quotient":
        blocks = operation["partition"]
        require(isinstance(blocks, list) and all(isinstance(b, list) and b for b in blocks),
                "invalid partition blocks")
        require(sorted(w for block in blocks for w in block) == sorted(link),
                "quotient partition does not partition the actual neighbours")
        require(any(len(block) > 1 for block in blocks), "identity quotient is not admitted")
        group = {w: i for i, block in enumerate(blocks) for w in block}
        for a, b, c, d in combinations(range(5), 4):
            require(not (group[link[a]] == group[link[c]] and
                         group[link[b]] == group[link[d]] and
                         group[link[a]] != group[link[b]]),
                    "quotient blocks cross in the original cyclic order")
        expected_map = {u: u for u in rest_nodes}
        for block in blocks:
            boundary_members = sorted(set(block) & set(source["boundary"]))
            require(len(boundary_members) <= 1, "quotient identifies original boundary labels")
            require(not any(a in block and b in block for a, b in rest_edges),
                    "quotient identifies adjacent original vertices")
            representative = boundary_members[0] if boundary_members else min(block)
            expected_map.update({u: representative for u in block})
        require(operation["vertex_map"] == {str(u): w for u, w in expected_map.items()},
                "wrong original-to-quotient label map")
        require(target_nodes == sorted(set(expected_map.values())), "wrong quotient nodes")
        require(target_edges == {tuple(sorted((expected_map[a], expected_map[b])))
                                 for a, b in rest_edges}, "wrong quotient edge images")
        actual_preimages = {
            tuple(record["edge"]): {tuple(e) for e in record["source_edges"]}
            for record in operation["edge_preimages"]
        }
        require(len(actual_preimages) == len(operation["edge_preimages"]),
                "duplicate quotient preimage record")
        expected_preimages = {edge: set() for edge in target_edges}
        for a, b in rest_edges:
            expected_preimages[tuple(sorted((expected_map[a], expected_map[b])))].add((a, b))
        require(actual_preimages == expected_preimages, "incomplete quotient edge preimages")
    else:
        raise ValueError("unknown operation kind")
    return {"literal_map_valid": True, "kind": kind}


def verify_domain(domain):
    """Replay completeness and admission without the topology producer.

    Generate set partitions from all 5^5 label strings, quotienting only the
    block names by their first occurrence.  Compare all 52 records per mark,
    all five spoke/flip records, and their exact admitted operation lists.
    Literal operation maps are checked separately by ``verify_operation``.
    """
    from itertools import combinations, product

    require(domain["patterns"] == PATTERNS, "wrong fixed ten-row order")
    sources = {entry["id"]: entry for entry in domain["sources"]}
    require(len(sources) == len(domain["sources"]), "duplicate source ID")
    source_graphs = {sid: entry["graph"] for sid, entry in sources.items()}
    expected_marks = set()
    for sid, entry in sources.items():
        nodes, _, adjacent = _literal_graph(entry["graph"])
        degree_five = [v for v in nodes if v not in range(5) and len(adjacent[v]) == 5]
        require(entry["degree5_vertices"] == degree_five, "incomplete degree-five source marks")
        expected_marks.update((sid, v) for v in degree_five)
    actual_marks = [(mark["source_id"], mark["v"]) for mark in domain["marks"]]
    require(len(set(actual_marks)) == len(actual_marks) and set(actual_marks) == expected_marks,
            "omitted, repeated, or extra marked source")
    require(len({mark["id"] for mark in domain["marks"]}) == len(domain["marks"]),
            "duplicate mark ID")

    partitions = set()
    for labels in product(range(5), repeat=5):
        names, canonical = {}, []
        for label in labels:
            if label not in names:
                names[label] = len(names)
            canonical.append(names[label])
        partitions.add(tuple(canonical))
    require(len(partitions) == 52, "independent partition count is not 52")

    operation_ids = set()
    quotient_records = 0
    flip_records = 0
    operation_count = 0
    for mark in domain["marks"]:
        source = source_graphs[mark["source_id"]]
        nodes, edges, adjacency = _literal_graph(source)
        v, link = mark["v"], mark["L"]
        require(link == source["rotation"][str(v)] and len(link) == 5,
                "mark does not preserve original neighbour rotation")
        consecutive_present = [tuple(sorted((link[i], link[(i + 1) % 5]))) in edges
                               for i in range(5)]
        require(mark["link_edges_present"] == consecutive_present and
                mark["is_C5_link"] == all(consecutive_present), "wrong literal C5-link claim")
        ops = mark["operations"]
        local_ids = [op["id"] for op in ops]
        require(len(set(local_ids)) == len(local_ids) and not (set(local_ids) & operation_ids),
                "duplicate operation ID")
        operation_ids.update(local_ids)
        require(all(op["kind"] in ("delete", "flip", "quotient") for op in ops),
                "extra operation kind")
        operation_count += len(ops)

        # Obtain each face directly from the supplied oriented face walks,
        # starting with the requested dart, rather than producer face traversal.
        face_at_dart = {}
        for face in source["faces"]:
            for i, (a, b) in enumerate(zip(face, face[1:] + face[:1])):
                require((a, b) not in face_at_dart, "source face repeats a directed edge")
                face_at_dart[a, b] = face[i:] + face[:i]
        require(len(mark["flip_candidates"]) == 5, "incomplete flip candidate table")
        deletion_ops = [op for op in ops if op["kind"] == "delete"]
        require(len(deletion_ops) == 5, "incomplete original spoke deletions")
        expected_flips = set()
        for i, u in enumerate(link):
            spoke = list(sorted((v, u)))
            deletion = [op for op in deletion_ops if op["spoke_index"] == i]
            require(len(deletion) == 1 and deletion[0]["spoke"] == spoke,
                    "missing or duplicate named spoke deletion")
            left, right = face_at_dart[v, u], face_at_dart[u, v]
            triangles = len(left) == len(right) == 3 and left != right
            distinct = len(set(left + right)) == 4
            inner = all(_cycle_key(f) != tuple(source["boundary"]) for f in (left, right))
            opposite = sorted(set(left + right) - {v, u})
            absent = len(opposite) == 2 and tuple(opposite) not in edges
            eligible = triangles and distinct and inner and absent
            candidate = mark["flip_candidates"][i]
            expected_values = {
                "spoke": spoke, "spoke_index": i, "incident_faces": [left, right],
                "opposite": opposite, "two_triangles": triangles,
                "distinct_quadrilateral": distinct, "both_inner": inner,
                "opposite_diagonal_absent": absent, "eligible": eligible,
            }
            require(all(candidate.get(k) == value for k, value in expected_values.items()),
                    "flip candidate differs from original face incidence")
            matching = [op for op in ops if op["kind"] == "flip" and op["spoke_index"] == i]
            require(len(matching) == int(eligible), "flip operation admission is incomplete")
            if eligible:
                require(candidate.get("operation_id") == matching[0]["id"] and
                        matching[0]["spoke"] == spoke and matching[0]["diagonal"] == opposite,
                        "flip candidate links the wrong named operation")
                expected_flips.add(matching[0]["id"])
            else:
                require("operation_id" not in candidate, "ineligible flip has an operation ID")
            flip_records += 1
        require(expected_flips == {op["id"] for op in ops if op["kind"] == "flip"},
                "extra flip operation outside the five spoke candidates")

        candidates = mark["quotient_candidates"]
        require(len(candidates) == 52 and
                {tuple(rec["restricted_growth"]) for rec in candidates} == partitions,
                "incomplete 52-partition candidate domain")
        admitted = set()
        for candidate in candidates:
            labels = candidate["restricted_growth"]
            positions = [[i for i, label in enumerate(labels) if label == block]
                         for block in range(max(labels) + 1)]
            blocks = [[link[i] for i in block] for block in positions]
            crossing = [list(indices) for indices in combinations(range(5), 4)
                        for a, b, c, d in [indices]
                        if labels[a] == labels[c] and labels[b] == labels[d] and
                        labels[a] != labels[b]]
            boundary_collisions = [block for block in blocks if len(set(block) & set(range(5))) > 1]
            internal_edges = sorted({tuple(sorted(pair)) for block in blocks
                                     for pair in combinations(block, 2)
                                     if tuple(sorted(pair)) in edges})
            nontrivial = len(blocks) < 5
            eligible = nontrivial and not crossing and not boundary_collisions and not internal_edges
            expected_values = {
                "position_blocks": positions, "blocks": blocks, "nontrivial": nontrivial,
                "crossing_position_quadruples": crossing, "multiple_boundary_blocks": boundary_collisions,
                "adjacent_identified_pairs": [list(edge) for edge in internal_edges], "eligible": eligible,
            }
            require(all(candidate.get(k) == value for k, value in expected_values.items()),
                    "quotient candidate disagrees with independent partition admission")
            matching = [op for op in ops if op["kind"] == "quotient" and
                        tuple(op["restricted_growth"]) == tuple(labels)]
            require(len(matching) == int(eligible), "quotient operation admission is incomplete")
            if eligible:
                require(candidate.get("operation_id") == matching[0]["id"] and
                        matching[0]["partition"] == blocks,
                        "quotient candidate links the wrong actual-label partition")
                admitted.add(matching[0]["id"])
            else:
                require("operation_id" not in candidate, "ineligible quotient has an operation ID")
            quotient_records += 1
        require(admitted == {op["id"] for op in ops if op["kind"] == "quotient"},
                "extra quotient operation outside the 52 candidates")
    return {"sources": len(sources), "marks": len(domain["marks"]),
            "flip_candidates": flip_records, "quotient_candidates": quotient_records,
            "operations": operation_count}


def verify_graph(graph):
    """Validate the supplied named disk embedding and independent planarity.

    Face walks are oriented and canonicalized by cyclic shift, never reversal.
    For disconnected inputs the rotation defines separate sphere components;
    their outside faces can be nested in the interior of B.  Each isolated
    vertex is represented by its singleton face [v].  We check Euler per
    component and also after merging outside faces into one global face.

    Returns small verification metadata; malformed inputs raise ValueError.
    NetworkX is deliberately a required second, independent planarity test.
    """
    import networkx as nx

    nodes, edges, adjacency = _literal_graph(graph)
    require({"rotation", "faces"} <= set(graph), "missing embedding field")
    encoded_rotation = graph["rotation"]
    require(isinstance(encoded_rotation, dict), "rotation must be a dictionary")
    require(set(encoded_rotation) == {str(v) for v in nodes},
            "rotation keys differ from original labels")
    rotation = {}
    for v in nodes:
        neighbours = encoded_rotation[str(v)]
        require(isinstance(neighbours, list), "rotation must contain lists")
        require(all(type(w) is int for w in neighbours), "invalid rotation label")
        require(len(neighbours) == len(set(neighbours)), "duplicate rotation dart")
        require(set(neighbours) == adjacency[v], "rotation differs from edges")
        rotation[v] = neighbours

    components = []
    unseen = set(nodes)
    while unseen:
        start = min(unseen)
        component = {start}
        stack = [start]
        unseen.remove(start)
        while stack:
            for w in adjacency[stack.pop()] & unseen:
                unseen.remove(w)
                component.add(w)
                stack.append(w)
        components.append(component)

    predecessor = {
        (v, w): neighbours[(i - 1) % len(neighbours)]
        for v, neighbours in rotation.items()
        for i, w in enumerate(neighbours)
    }
    unused_darts = {(u, v) for u, v in edges} | {(v, u) for u, v in edges}
    faces = []
    while unused_darts:
        initial = min(unused_darts)
        dart = initial
        walk = []
        while True:
            require(dart in unused_darts, "face dart permutation closes wrongly")
            unused_darts.remove(dart)
            u, v = dart
            walk.append(u)
            dart = (v, predecessor[v, u])
            if dart == initial:
                break
        faces.append(_cycle_key(walk))
    faces.extend((v,) for v in nodes if not adjacency[v])

    supplied_faces = graph["faces"]
    require(isinstance(supplied_faces, list), "faces must be a list")
    require(all(isinstance(f, list) and f and
                all(type(v) is int and v in adjacency for v in f)
                for f in supplied_faces), "invalid face label or walk")
    require(Counter(_cycle_key(f) for f in supplied_faces) == Counter(faces),
            "supplied faces differ from rotation dart walks")
    require(tuple(graph["boundary"]) in faces,
            "named forward B is not a supplied outer face")

    component_metadata = []
    for component in components:
        vertex_count = len(component)
        edge_count = sum(len(adjacency[v]) for v in component) // 2
        face_count = sum(f[0] in component for f in faces)
        require(vertex_count - edge_count + face_count == 2,
                "rotation component has nonzero genus")
        component_metadata.append({
            "nodes": sorted(component), "vertices": vertex_count,
            "edges": edge_count, "faces": face_count,
        })
    global_faces = len(faces) - len(components) + 1
    require(len(nodes) - len(edges) + global_faces == 1 + len(components),
            "disconnected global Euler identity fails")

    literal = nx.Graph()
    literal.add_nodes_from(nodes)
    literal.add_edges_from(edges)
    require(nx.check_planarity(literal)[0], "literal graph is not planar")
    apex = max(nodes) + 1
    augmented = literal.copy()
    augmented.add_edges_from((apex, v) for v in graph["boundary"])
    require(nx.check_planarity(augmented)[0], "boundary is not cofacial by apex test")
    return {
        "vertices": len(nodes), "edges": len(edges),
        "component_face_walks": len(faces), "global_faces": global_faces,
        "components": component_metadata,
        "forward_boundary_face": True, "apex_planar": True,
    }
