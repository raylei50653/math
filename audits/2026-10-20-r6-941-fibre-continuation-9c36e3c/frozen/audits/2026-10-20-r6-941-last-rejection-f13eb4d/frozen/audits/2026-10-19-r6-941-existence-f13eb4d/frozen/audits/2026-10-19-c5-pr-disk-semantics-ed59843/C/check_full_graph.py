#!/usr/bin/env python3
"""Reconstruct disks and enumerate complete literal fibres; stdlib only.

--check is read-only. --write exclusively creates this directory's outputs.
This is an independent reconstruction, not replay of absent historical code.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SOURCE_REL = "docs/sources/2026-10-19-c5-grammar-v02/certificate_v02.json"
SOURCE = AUDIT / "frozen" / SOURCE_REL


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def edge(a, b):
    return tuple(sorted((a, b)))


def make_disk(word):
    """Graph construction does not consult any matrix or support mask."""
    require(word and word[0] in "FC" and set(word[1:]) <= {"P", "R"}, "bad word")
    edges = {edge(i, (i + 1) % 5) for i in range(5)}
    boundary = list(range(5))
    if word[0] == "F":
        edges.update({(0, 2), (0, 3)})
        faces = [[0, 1, 2], [0, 2, 3], [0, 3, 4]]
    else:
        faces = [list(range(5))]
    vertices = 5
    for letter in word[1:]:
        if letter == "R":
            boundary = boundary[-1:] + boundary[:-1]
        else:
            x = vertices
            vertices += 1
            a, b, z = boundary[0], boundary[1], boundary[4]
            edges.update({edge(x, a), edge(x, b), edge(x, z)})
            # New faces oppose the old boundary edges and follow the new ones.
            faces.extend([[b, a, x], [a, z, x]])
            boundary = [x] + boundary[1:]
    return {
        "vertices": vertices,
        "edges": [list(e) for e in sorted(edges)],
        "boundary": boundary,
        "faces": faces,
    }


def validate_disk(graph):
    """Check a connected oriented disk cellulation, including every vertex link."""
    n = graph["vertices"]
    require(type(n) is int and n >= 5, "invalid vertex count")
    vertices = set(range(n))
    raw_edges = graph["edges"]
    require(all(len(e) == 2 and e[0] < e[1] and set(e) <= vertices for e in raw_edges), "invalid edge")
    edges = {tuple(e) for e in raw_edges}
    require(len(edges) == len(raw_edges), "duplicate edge")
    boundary = graph["boundary"]
    require(len(boundary) == 5 and len(set(boundary)) == 5 and set(boundary) <= vertices, "boundary is not a simple ordered C5")
    boundary_darts = {(boundary[i], boundary[(i + 1) % 5]) for i in range(5)}
    require({edge(*d) for d in boundary_darts} <= edges, "missing boundary edge")
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    seen, todo = set(), [0]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(adjacency[v] - seen)
    require(seen == vertices, "disconnected graph")
    incidence = defaultdict(list)
    links = [[] for _ in range(n)]
    for face in graph["faces"]:
        require(len(face) >= 3 and len(face) == len(set(face)) and set(face) <= vertices, "non-simple face")
        for i, a in enumerate(face):
            b = face[(i + 1) % len(face)]
            require(edge(a, b) in edges, "face uses absent edge")
            incidence[edge(a, b)].append((a, b))
            links[a].append(edge(face[i - 1], b))
    require(set(incidence) == edges, "edge outside all cells")
    for e, darts in incidence.items():
        if e in {edge(*d) for d in boundary_darts}:
            require(len(darts) == 1 and darts[0] in boundary_darts, "boundary incidence/orientation mismatch")
        else:
            require(len(darts) == 2 and darts[0] == darts[1][::-1], "interior incidence/orientation mismatch")
    require(n - len(edges) + len(graph["faces"]) == 1, "disk Euler characteristic mismatch")
    for v in range(n):
        link_edges = links[v]
        require(len(link_edges) == len(set(link_edges)), "duplicate corner in vertex link")
        link_adj = {u: set() for u in adjacency[v]}
        for a, b in link_edges:
            link_adj[a].add(b)
            link_adj[b].add(a)
        reached, pending = set(), [next(iter(link_adj))]
        while pending:
            u = pending.pop()
            if u not in reached:
                reached.add(u)
                pending.extend(link_adj[u] - reached)
        require(reached == set(link_adj), "disconnected vertex link")
        degree_multiset = sorted(map(len, link_adj.values()))
        if v in boundary:
            require(degree_multiset == [1, 1] + [2] * (len(link_adj) - 2), "boundary link is not a path")
        else:
            require(degree_multiset == [2] * len(link_adj), "interior link is not a cycle")
    return adjacency


def full_fibre(graph, row, adjacency):
    """Enumerate actual proper graph colourings with this exact boundary tuple.

    Return the colours on increasing interior vertex IDs. Every boundary colour
    is fixed literally in {0,1,2,3}; no quotient is taken during enumeration.
    """
    n = graph["vertices"]
    colours = [-1] * n
    for v, c in zip(graph["boundary"], map(int, row)):
        colours[v] = c
    interior = [v for v in range(n) if colours[v] < 0]
    for a, b in graph["edges"]:
        if colours[a] >= 0 and colours[a] == colours[b]:
            return []
    assignments = []

    def visit(pending):
        if not pending:
            assignments.append("".join(str(colours[v]) for v in interior))
            return
        # A graph-only constraint heuristic; does not use boundary row classes.
        v = max(pending, key=lambda u: (len({colours[w] for w in adjacency[u] if colours[w] >= 0}), len(adjacency[u]), -u))
        forbidden = {colours[w] for w in adjacency[v]}
        rest = pending - {v}
        for c in range(4):
            if c not in forbidden:
                colours[v] = c
                visit(rest)
        colours[v] = -1

    visit(set(interior))
    return sorted(assignments)


def matrix_step(matrix, counts):
    return [sum(a * b for a, b in zip(row, counts)) for row in matrix]


def word_counts(model, word):
    counts = model["seeds"][word[0]]["counts"]
    for letter in word[1:]:
        counts = matrix_step(model["operators"][letter], counts)
    return counts


def support(counts):
    return sum(1 << i for i, count in enumerate(counts) if count)


def get_graph_counts(graph, rows):
    adjacency = validate_disk(graph)
    fibres = [full_fibre(graph, row, adjacency) for row in rows]
    return list(map(len, fibres)), fibres


def negative_controls(model):
    controls = []

    def rejection(name, graph):
        try:
            validate_disk(graph)
        except ValueError as exc:
            controls.append({"name": name, "detected": True, "reason": str(exc)})
        else:
            raise ValueError("negative control accepted: " + name)

    graph = make_disk("FP")
    graph["edges"].remove([0, 5])
    rejection("missing_spoke_but_retained_triangular_faces", graph)
    graph = make_disk("FP")
    graph["boundary"][0] = graph["boundary"][1]
    rejection("repeated_boundary_vertex", graph)
    graph = make_disk("FP")
    graph["faces"][-1].reverse()
    rejection("one_reversed_face", graph)
    graph = make_disk("FP")
    graph["vertices"] += 1
    rejection("isolated_extra_vertex", graph)

    graph = make_disk("FP")
    graph["edges"].remove([0, 5])
    graph["faces"] = graph["faces"][:-2] + [[1, 0, 4, 5]]
    counts, _ = get_graph_counts(graph, model["rows"])
    require(counts != word_counts(model, "FP"), "spokeless legal disk escaped count control")
    controls.append({"name": "legal_spokeless_attachment_changes_counts", "detected": True, "counts": counts, "expected_P_counts": word_counts(model, "FP")})

    graph = make_disk("F")
    graph["boundary"] = graph["boundary"][1:] + graph["boundary"][:1]
    counts, _ = get_graph_counts(graph, model["rows"])
    require(counts != word_counts(model, "FR"), "opposite rotation escaped count control")
    controls.append({"name": "opposite_rotation_changes_counts", "detected": True, "counts": counts, "expected_R_counts": word_counts(model, "FR")})

    counts, _ = get_graph_counts(make_disk("FPP"), model["rows"])
    booleanized = list(map(lambda n: int(n > 0), counts))
    require(counts != booleanized and support(counts) == support(booleanized), "multiplicity control failed")
    controls.append({"name": "booleanized_counts_preserve_support_but_lose_multiplicity", "detected": True, "literal_counts": counts, "booleanized_counts": booleanized})
    return controls


def cross_check_enumerator(rows):
    """An unpruned Cartesian product supplies a second enumeration method."""
    controls = []
    for word in ("F", "C", "FP", "CP", "FPP", "FRRRPPRPRR", "FPPRPPRRRPP", "FPPRPPRRRPPP"):
        graph = make_disk(word)
        adjacency = validate_disk(graph)
        interior = sorted(set(range(graph["vertices"])) - set(graph["boundary"]))
        counts = []
        for row in rows:
            expected = []
            for assignment in product(range(4), repeat=len(interior)):
                colours = dict(zip(graph["boundary"], map(int, row)))
                colours.update(zip(interior, assignment))
                if all(colours[a] != colours[b] for a, b in graph["edges"]):
                    expected.append("".join(map(str, assignment)))
            require(full_fibre(graph, row, adjacency) == expected, "independent Cartesian-product disagreement")
            counts.append(len(expected))
        controls.append({"word": word, "counts": counts, "all_ten_complete_fibres_equal": True})
    return controls


def build():
    base = json.loads((AUDIT / "BASE.json").read_text())
    raw = SOURCE.read_bytes()
    require(sha256(raw).hexdigest() == base["inputs"][SOURCE_REL]["sha256"], "frozen source SHA mismatch")
    source = json.loads(raw)
    model = source["model"]
    rows = model["rows"]
    cases = []
    for grammar in ("F", "FC"):
        reps = source["minimum_representatives"][grammar]
        require(len(reps["states"]) == 132, "unexpected representative domain")
        for state in reps["states"]:
            representative = reps["witness"][str(state)]
            require(representative[0] in reps["allowed_seeds"], "witness seed outside grammar")
            for suffix in ("", "P", "R"):
                word = representative + suffix
                graph = make_disk(word)
                counts, fibres = get_graph_counts(graph, rows)
                predicted = word_counts(model, word)
                require(counts == predicted, f"integer fibre disagreement: {grammar}/{state}/{suffix}")
                target = state if not suffix else model["transitions"][str(state)][suffix]
                require(support(counts) == target, f"support disagreement: {grammar}/{state}/{suffix}")
                require(graph["vertices"] - 5 == reps["distance"][str(state)] + (suffix == "P"), "interior cost disagreement")
                if grammar == "F":
                    require(all(len(face) == 3 for face in graph["faces"]), "F graph has a nontriangular face")
                interior = sorted(set(range(graph["vertices"])) - set(graph["boundary"]))
                cases.append({
                    "grammar": grammar,
                    "representative_state": state,
                    "suffix": suffix,
                    "word": word,
                    "graph": graph,
                    "interior_vertices": interior,
                    "literal_fibres": fibres,
                    "counts": counts,
                    "matrix_counts": predicted,
                    "support": target,
                })
    controls = negative_controls(model)
    enumerator_controls = cross_check_enumerator(rows)
    certificate = {
        "schema": "c5-pr-disk-whole-graph/v1",
        "scope": "independent_reconstruction_not_historical_original_code_replay",
        "source_sha256": sha256(raw).hexdigest(),
        "rows": rows,
        "fibre_encoding": "literal_fibres[i] lists every colouring on increasing interior_vertices for fixed literal boundary rows[i]; empty list is empty fibre, empty string is the unique no-interior assignment",
        "operations": {
            "P": "retain all old vertices and edges; add fresh x adjacent b4,b0,b1; replace boundary by (x,b1,b2,b3,b4); add oriented faces (b1,b0,x),(b0,b4,x)",
            "R": "retain graph and cells; replace boundary by (b4,b0,b1,b2,b3)",
        },
        "cases": cases,
        "negative_controls": controls,
        "enumerator_cross_checks": enumerator_controls,
    }
    summary = {
        "schema": "c5-pr-disk-whole-graph-verification/v1",
        "scope": certificate["scope"],
        "source_sha256": certificate["source_sha256"],
        "certificate_sha256": sha256(canonical_bytes(certificate)).hexdigest(),
        "graph_cases": len(cases),
        "grammars": {grammar: sum(case["grammar"] == grammar for case in cases) for grammar in ("F", "FC")},
        "representatives_per_grammar": 132,
        "successors_per_representative": 2,
        "literal_fibres": sum(len(case["literal_fibres"]) for case in cases),
        "empty_fibres": sum(not fibre for case in cases for fibre in case["literal_fibres"]),
        "literal_full_colourings": sum(sum(case["counts"]) for case in cases),
        "max_vertices": max(case["graph"]["vertices"] for case in cases),
        "max_single_fibre_size": max(max(case["counts"]) for case in cases),
        "integer_matrix_disagreements": 0,
        "support_disagreements": 0,
        "disk_cellulation_failures": 0,
        "negative_controls_detected": len(controls),
        "independent_product_fibres": 10 * len(enumerator_controls),
        "all_pass": True,
    }
    return certificate, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true", help="recompute, compare bytes, never write")
    modes.add_argument("--write", action="store_true", help="exclusively create this C directory's certificate and result")
    args = parser.parse_args()
    certificate, summary = build()
    if args.write:
        require(all(not (HERE / filename).exists() for filename in ("certificate.json", "verification.json")), "--write requires absent C output files")
    for filename, obj in (("certificate.json", certificate), ("verification.json", summary)):
        data = canonical_bytes(obj)
        path = HERE / filename
        if args.write:
            with path.open("xb") as handle:
                handle.write(data)
        else:
            require(path.read_bytes() == data, "generated bytes differ: " + filename)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
