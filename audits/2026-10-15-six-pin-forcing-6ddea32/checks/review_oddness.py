#!/usr/bin/env python3
"""Independent read-only check of oddness controls; imports no sibling checker."""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SIBLING = HERE.parent / "2026-10-15-oddness-descent-6ddea32"
graphs_bytes = (SIBLING / "graphs.json").read_bytes()
certificate_bytes = (SIBLING / "certificate.json").read_bytes()
graphs = json.loads(graphs_bytes)
controls = json.loads(certificate_bytes)["controls"]
results = []

for g, certificate in zip(graphs, controls):
    n, edges = g["n"], g["edges"]
    incidence = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        incidence[u].append((i, v)); incidence[v].append((i, u))

    def enumerate_matchings(available, chosen):
        if not available:
            yield tuple(sorted(chosen)); return
        u = max(available)
        for i, v in incidence[u]:
            if v in available:
                yield from enumerate_matchings(available - {u, v}, chosen + (i,))

    matchings = sorted(enumerate_matchings(set(range(n)), ()))
    assert matchings == [tuple(m["edges"]) for m in certificate["matchings"]]
    sets = list(map(set, matchings))

    def edge_components(selected):
        neighbours = {}
        for i in selected:
            u, v = edges[i]
            neighbours.setdefault(u, set()).add(v)
            neighbours.setdefault(v, set()).add(u)
        unseen = set(neighbours); out = []
        while unseen:
            root = unseen.pop(); todo = [root]; comp = {root}
            while todo:
                u = todo.pop()
                fresh = neighbours[u] & unseen
                unseen -= fresh; comp |= fresh; todo.extend(fresh)
            out.append(comp)
        return out

    cycles = [edge_components(set(range(len(edges))) - M) for M in sets]
    measures = [(sum(len(c) % 2 for c in cs), sum(len(c) for c in cs if len(c) % 2))
                for cs in cycles]
    assert measures == [(m["oddness"], m["odd_vertex_mass"]) for m in certificate["matchings"]]
    e, f, start = g["e"], g["f"], g["matching_index"]
    sign = (e in sets[start], f in sets[start])
    allowed = [i for i, M in enumerate(sets) if
               ((e in M, f in M) == sign if g["mode"] == "fixed_direction"
                else (e in M) != (f in M))]
    assert allowed == certificate["admissible_state_indices"]
    moves = [[i, j] for i, j in itertools.combinations(allowed, 2)
             if len(edge_components(sets[i] ^ sets[j])) == 1]
    assert moves == certificate["complete_admissible_single_cycle_edges"]
    neighbours = sorted(j if i == start else i for i, j in moves if start in (i, j))
    assert neighbours == [row["to"] for row in certificate["complete_start_moves"]]
    opposite = [i for i, M in enumerate(sets) if (e in M) != (f in M)
                and (e in M, f in M) != sign and measures[i][0] < measures[start][0]
                and len(edge_components(M ^ sets[start])) == 1]
    if g["name"] == "dodecahedron_4sum":
        assert len(neighbours) == 12 and all(measures[i] == (2, 36) for i in neighbours)
        assert measures[start] == (2, 10) and len(opposite) == 11
        primal = {tuple(sorted(e)) for e in certificate["embedding"]["primal_edges"]}
        triangles = certificate["embedding"]["primal_triangular_faces"]
        assert (8, 9) in primal and (8, 10) in primal and (3, 8) not in primal
        assert any(set(t) == {9, 3, 10} for t in triangles)
    if g["name"] == "icosahedron_dual_transversal_control":
        assert sum(o > 0 for o, m in measures) == 6
        for i, M in enumerate(sets):
            if not measures[i][0]:
                continue
            for N in sets:
                if len(edge_components(M ^ N)) != 1:
                    continue
                B = N - M
                multiplicities = [sum(edges[j][0] in c for j in B) for c in cycles[i]]
                assert any(m > 1 for m in multiplicities)
    results.append({"name": g["name"], "all_matchings": len(matchings),
                    "allowed_states": len(allowed), "all_allowed_moves": len(moves),
                    "start_neighbours": len(neighbours),
                    "source_status": g["source_status"]})

print(json.dumps({"status": "PASS", "graphs_sha256": hashlib.sha256(graphs_bytes).hexdigest(),
                  "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
                  "controls": results}, indent=2))
