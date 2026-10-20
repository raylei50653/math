#!/usr/bin/env python3
"""Independent exact checker. No import of experiment code; stdlib only."""
import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
FROZEN = AUDIT / "frozen/artifacts/c5_cells/cells.json"
FROZEN_SHA = "04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8"
PAIRS = list(itertools.combinations(range(4), 2))
BOUNDARY = [0, 1, 2, 3, 4]
SOURCES = [[0, 1, 0, 1, 2, 1, 3, 2], [0, 1, 0, 1, 2, 2, 3, 3]]
FACES = [[0, 1, 7], [1, 2, 7], [2, 3, 6], [3, 4, 6], [4, 0, 6],
         [0, 5, 6], [2, 6, 5], [0, 7, 5], [2, 5, 7]]
CERTIFICATE = HERE / "collision_certificate.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def graph():
    raw = FROZEN.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == FROZEN_SHA, "frozen source hash")
    witness = json.loads(raw)["cells"]["95"]
    require(witness["k_eff"] == 3, "catalogue order")
    edges = {tuple(sorted(e)) for e in witness["edges"]}
    edges.update(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
    require(all(0 <= a < b < 8 for a, b in edges), "simple graph")
    return sorted(edges)


def proper(coloring, edges):
    return (type(coloring) is list and len(coloring) == 8
            and all(type(c) is int and 0 <= c < 4 for c in coloring)
            and all(coloring[u] != coloring[v] for u, v in edges))


def components(coloring, pair, edges):
    """Closure of every vertex in the whole induced two-color graph."""
    unseen = {v for v in range(8) if coloring[v] in pair}
    answer = []
    while unseen:
        reached = {min(unseen)}
        while True:
            grown = reached | {
                v for edge in edges for v in edge
                if coloring[v] in pair and any(u in reached for u in edge)
            }
            if grown == reached:
                break
            reached = grown
        require(reached <= unseen, "components overlap")
        unseen -= reached
        answer.append(sorted(reached))
    return sorted(answer)


def state(coloring, edges):
    full = [components(coloring, pair, edges) for pair in PAIRS]
    restricted = [
        sorted([sorted(set(component) & set(BOUNDARY)) for component in row
                if set(component) & set(BOUNDARY)])
        for row in full
    ]
    return {"coloring": coloring, "full_components": full,
            "signature": [coloring[:5], restricted]}


def swap(coloring, pair, root, edges):
    require(root in BOUNDARY and coloring[root] in pair, "illegal rooted action")
    selected = [c for c in components(coloring, pair, edges) if root in c]
    require(len(selected) == 1, "rooted component uniqueness")
    changed = coloring[:]
    for v in selected[0]:
        changed[v] = pair[0] + pair[1] - changed[v]
    require(proper(changed, edges), "swap is improper")
    return changed, selected[0]


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def segment_contains(a, b, c):
    return (cross(a, b, c) == 0
            and min(a[0], b[0]) <= c[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))


def segments_intersect(a, b, c, d):
    signs = [cross(a, b, c), cross(a, b, d), cross(c, d, a), cross(c, d, b)]
    if signs[0] * signs[1] < 0 and signs[2] * signs[3] < 0:
        return True
    return (segment_contains(a, b, c) or segment_contains(a, b, d)
            or segment_contains(c, d, a) or segment_contains(c, d, b))


def barycentric_points(edges):
    points = [tuple(map(Q, p)) for p in [(0, 0), (4, 0), (6, 3), (3, 6), (0, 4)]]
    neighbors = [{v for e in edges if u in e for v in e if v != u} for u in range(8)]
    matrix = [
        [Q(len(neighbors[u]) if u == v else -int(v in neighbors[u]))
         for v in range(5, 8)]
        + [sum((points[v][j] for v in neighbors[u] if v < 5), Q(0))
           for j in range(2)]
        for u in range(5, 8)
    ]
    for i in range(3):
        require(matrix[i][i] != 0, "barycentric pivot")
        pivot = matrix[i][i]
        matrix[i] = [x / pivot for x in matrix[i]]
        for k in range(3):
            if k != i:
                scale = matrix[k][i]
                matrix[k] = [x - scale * y for x, y in zip(matrix[k], matrix[i])]
    points.extend(tuple(row[3:]) for row in matrix)
    for u in range(5, 8):
        for j in range(2):
            require(len(neighbors[u]) * points[u][j]
                    == sum(points[v][j] for v in neighbors[u]), "barycentric equation")
    return points


def geometry(edges, points, faces):
    require(len(points) == 8 and len(set(points)) == 8, "coincident vertices")
    for i in range(5):
        a, b = points[i], points[(i + 1) % 5]
        require(all(cross(a, b, points[j]) > 0 for j in range(8)
                    if j not in {i, (i + 1) % 5}), "strict convex boundary/interior")
    for u, v in edges:
        require(all(not segment_contains(points[u], points[v], points[w])
                    for w in range(8) if w not in {u, v}), "vertex on nonincident edge")
    for first, second in itertools.combinations(edges, 2):
        if set(first).isdisjoint(second):
            require(not segments_intersect(*(points[v] for v in first + second)),
                    "nonincident edge crossing")
    require(len(faces) == 9 and len({tuple(sorted(f)) for f in faces}) == 9,
            "distinct nine faces")
    directed = Counter()
    face_area = []
    for face in faces:
        require(len(face) == 3 and len(set(face)) == 3, "triangle")
        require(all(type(v) is int and 0 <= v < 8 for v in face), "face vertex")
        area = cross(*(points[v] for v in face))
        require(area > 0, "positive oriented face")
        face_area.append(area)
        directed.update(zip(face, face[1:] + face[:1]))
    boundary_directed = {(i, (i + 1) % 5) for i in range(5)}
    require({tuple(sorted(e)) for e in directed} == set(edges), "face edges")
    for u, v in edges:
        if (u, v) in boundary_directed:
            require((directed[u, v], directed[v, u]) == (1, 0), "boundary incidence")
        elif (v, u) in boundary_directed:
            require((directed[u, v], directed[v, u]) == (0, 1), "boundary incidence")
        else:
            require((directed[u, v], directed[v, u]) == (1, 1), "interior incidence")
    # Each interior link is one cycle; each boundary link is one path.
    links = []
    for v in range(8):
        link_edges = [tuple(w for w in f if w != v) for f in faces if v in f]
        link_vertices = {w for edge in link_edges for w in edge}
        degrees = Counter(w for edge in link_edges for w in edge)
        reached = {min(link_vertices)}
        while True:
            grown = reached | {w for edge in link_edges if reached.intersection(edge)
                               for w in edge}
            if grown == reached:
                break
            reached = grown
        require(reached == link_vertices, "disconnected vertex link")
        if v < 5:
            require(sorted(degrees.values()) == [1, 1] + [2] * (len(degrees) - 2),
                    "boundary link is not path")
            require({u for u, degree in degrees.items() if degree == 1}
                    == {(v - 1) % 5, (v + 1) % 5}, "boundary link endpoints")
        else:
            require(set(degrees.values()) == {2}, "interior link is not cycle")
        links.append(sorted([sorted(e) for e in link_edges]))
    polygon_area = sum(
        points[i][0] * points[(i + 1) % 5][1]
        - points[i][1] * points[(i + 1) % 5][0] for i in range(5)
    )
    require(sum(face_area) == polygon_area, "face area does not cover polygon")
    require(8 - len(edges) + len(faces) == 1, "disk Euler characteristic")
    return {"twice_face_areas": [str(a) for a in face_area],
            "twice_polygon_area": str(polygon_area), "vertex_links": links}


def expected_certificate():
    edges = graph()
    records, changed_components = [], []
    for source in SOURCES:
        require(proper(source, edges), "source improper")
        target, selected = swap(source, (1, 2), 1, edges)
        records.append({"source": state(source, edges), "target": state(target, edges)})
        changed_components.append(selected)
    require(records[0]["source"]["signature"] == records[1]["source"]["signature"],
            "source signature mismatch")
    require(records[0]["target"]["signature"] != records[1]["target"]["signature"],
            "target signature equality")
    points = barycentric_points(edges)
    geometry_result = geometry(edges, points, FACES)
    fibre = [
        SOURCES[0][:5] + list(private)
        for private in itertools.product(range(4), repeat=3)
        if proper(SOURCES[0][:5] + list(private), edges)
    ]
    return {
        "schema": "independent-joint-kempe-literal-collision-v1",
        "catalogue": "95", "frozen_sha256": FROZEN_SHA,
        "n": 8, "ordered_boundary": BOUNDARY, "edges": [list(e) for e in edges],
        "pair_order": [list(p) for p in PAIRS], "action": {"pair": [1, 2], "root": 1},
        "records": records, "swapped_full_components": changed_components,
        "complete_fixed_literal_boundary_fibre": fibre,
        "embedding": {"points": [[str(x) for x in p] for p in points],
                      "oriented_faces": FACES, **geometry_result},
        "conclusion": "same literal source signature; different literal target signature",
        "scope": "one fixed C5 disk; all six partitions; one rooted action; J1/r6 not triggered"
    }


def validate(data):
    require(type(data) is dict, "certificate object")
    expected = expected_certificate()
    require(set(data) == set(expected), "certificate fields")
    require(data["n"] == 8, "vertex count")
    edges = [tuple(edge) for edge in data["edges"]]
    require(edges == graph(), "frozen graph mismatch")
    for record in data["records"]:
        for side in ["source", "target"]:
            require(proper(record[side]["coloring"], edges), "improper supplied coloring")
            require(canonical(record[side]) == canonical(state(record[side]["coloring"], edges)),
                    "supplied maximal components/signature")
        target, _ = swap(record["source"]["coloring"],
                         data["action"]["pair"], data["action"]["root"], edges)
        require(target == record["target"]["coloring"], "wrong supplied target")
    points = [tuple(Q(value) for value in point) for point in data["embedding"]["points"]]
    geometry(edges, points, data["embedding"]["oriented_faces"])
    require(canonical(data) == canonical(expected), "exact certificate mismatch")
    return expected


def negative_controls(good):
    corruptions = {}
    bad = copy.deepcopy(good)
    del bad["action"]
    corruptions["missing_action"] = bad
    bad = copy.deepcopy(good)
    bad["n"] = True
    corruptions["boolean_integer"] = bad
    bad = copy.deepcopy(good)
    bad["records"][0]["source"]["coloring"][1] = 0
    corruptions["improper_source"] = bad
    bad = copy.deepcopy(good)
    bad["records"][0]["source"]["full_components"][0][0].remove(0)
    corruptions["nonmaximal_component"] = bad
    bad = copy.deepcopy(good)
    bad["records"][0]["source"]["signature"][1][0] = [[0, 1], [2, 3]]
    corruptions["wrong_boundary_partition"] = bad
    bad = copy.deepcopy(good)
    bad["action"]["root"] = 3
    corruptions["different_action"] = bad
    bad = copy.deepcopy(good)
    bad["records"][0]["target"]["coloring"][7] = 2
    corruptions["partial_swap"] = bad
    bad = copy.deepcopy(good)
    bad["embedding"]["points"][5] = bad["embedding"]["points"][0][:]
    corruptions["coincident_geometry"] = bad
    bad = copy.deepcopy(good)
    bad["embedding"]["points"][6] = ["20", "20"]
    corruptions["outside_geometry"] = bad
    bad = copy.deepcopy(good)
    bad["embedding"]["oriented_faces"][0] = [0, 7, 1]
    corruptions["reversed_face"] = bad
    rejected = {}
    for name, data in corruptions.items():
        try:
            validate(data)
        except (ValueError, TypeError, KeyError, IndexError) as error:
            rejected[name] = str(error)
        else:
            raise ValueError("accepted corruption: " + name)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["build", "check"])
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    args = parser.parse_args()
    if args.mode == "build":
        data = expected_certificate()
        validate(data)
        with args.certificate.open("x", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
    before = args.certificate.read_bytes()
    data = json.loads(before)
    validate(data)
    rejected = negative_controls(data)
    require(args.certificate.read_bytes() == before, "checker changed certificate")
    print(json.dumps({"status": "PASS", "mode": args.mode,
                      "certificate_sha256": hashlib.sha256(before).hexdigest(),
                      "literal_boundary_fibre_count":
                      len(data["complete_fixed_literal_boundary_fibre"]),
                      "negative_controls": rejected}, indent=2))


if __name__ == "__main__":
    main()
