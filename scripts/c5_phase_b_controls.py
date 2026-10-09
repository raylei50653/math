#!/usr/bin/env python3
"""Small Phase B controls; no catalogue search or source-realizability claim.

Read two immutable disk graphs and two new nonplanar capacity controls.
Check complete relations, witnesses and embeddings. --check is read-only.
"""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_phase_b/controls.json"
S935 = ROOT / "artifacts/c5_shield_calibration/counterexample_S935.json"
C44 = ROOT / "artifacts/c5_excess_two_c44/counterexample_C44-AD3-row0-44.json"
CAPACITY = ROOT / "artifacts/c5_phase_b/capacity_inputs.json"
PATTERNS = tuple(tuple(map(int, s)) for s in (
    "01012", "01021", "01023", "01201", "01202",
    "01203", "01212", "01213", "01231", "01232"))
FRAME = {(0, 1), (0, 4), (1, 2), (2, 3), (3, 4)}
ROWS = tuple(r for r in product(range(4), repeat=5)
             if all(r[u] != r[v] for u, v in FRAME))


def relation(vertices, edges):
    private = sorted(set(vertices) - set(range(5)))
    result = {}
    for row in ROWS:
        for colors in product(range(4), repeat=len(private)):
            f = dict(zip(range(5), row)) | dict(zip(private, colors))
            if all(f[u] != f[v] for u, v in edges):
                result[row] = [f[v] for v in vertices]
                break
    return result


def disk_rotation(vertices, edges, rotation):
    darts = {(u, v) for a, b in edges for u, v in ((a, b), (b, a))}
    assert set(rotation) == set(vertices)
    for v in vertices:
        assert len(rotation[v]) == len(set(rotation[v]))
        assert set(rotation[v]) == {w for u, w in darts if u == v}
    unseen, faces = set(darts), []
    while unseen:
        start = min(unseen)
        dart, face = start, []
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            face.append(u)
            neighbors = rotation[v]
            dart = (v, neighbors[(neighbors.index(u) + 1) % len(neighbors)])
            if dart == start:
                break
        faces.append(face)
    assert len(vertices) - len(edges) + len(faces) == 2
    outer = [f for f in faces if len(f) == 5 and set(f) == set(range(5))]
    assert len(outer) == 1
    assert {tuple(sorted((outer[0][i], outer[0][(i + 1) % 5])))
            for i in range(5)} == FRAME
    return {"faces": faces, "outer": outer[0], "euler": 2}


def graph_control(name, vertices, edges, rotation, expected):
    vertices = sorted(vertices)
    edges = sorted(tuple(sorted(e)) for e in edges)
    assert {e for e in edges if max(e) < 5} == FRAME
    full = relation(vertices, edges)
    mask = sum(1 << i for i, r in enumerate(PATTERNS) if r in full)
    assert mask == expected
    deletions = []
    common = set(ROWS) - set(full)
    for e in edges:
        if e in FRAME:
            continue
        cut = relation(vertices, [x for x in edges if x != e])
        new = set(cut) - set(full)
        assert new
        common &= new
        deletions.append({"edge": e, "new_rows": sorted(new),
                          "witness_row": min(new), "witness": cut[min(new)]})
    return {"name": name, "vertices": vertices, "edges": edges,
            "degrees": [[v, sum(v in e for e in edges)] for v in vertices],
            "sigma_mask": mask, "accepted_rows": sorted(full),
            "literal_row_count": len(ROWS), "sigma_critical": True,
            "q_minimal_rejected_rows": sorted(common),
            "deletions": deletions,
            "disk_rotation": disk_rotation(vertices, edges, rotation)}


def first_lift(vertices, edges, pins):
    """Exact MRV backtracking, independently implemented for the larger controls."""
    neighbors = {v: {w if v == u else u for u, w in edges if v in (u, w)}
                 for v in vertices}
    f = dict(pins)
    if any(u in f and v in f and f[u] == f[v] for u, v in edges):
        return None

    def search():
        if len(f) == len(vertices):
            return [f[v] for v in vertices]
        choices = []
        for v in vertices:
            if v not in f:
                colors = sorted(set(range(4)) - {f[w] for w in neighbors[v] if w in f})
                choices.append((len(colors), v, colors))
        _, v, colors = min(choices)
        for color in colors:
            f[v] = color
            found = search()
            if found is not None:
                del f[v]
                return found
            del f[v]
        return None

    return search()


def check_kuratowski(edges, witness):
    original = {tuple(sorted(e)) for e in edges}
    branches = set(witness["branch_vertices"])
    internal, reduced, used_edges = set(), set(), set()
    for item in witness["paths"]:
        p = item["path"]
        pair = tuple(sorted(item["edge"]))
        assert (p[0], p[-1]) == tuple(item["edge"])
        assert len(p) == len(set(p)) and set(pair) <= branches
        assert not (set(p[1:-1]) & (internal | branches))
        internal.update(p[1:-1])
        for u, v in zip(p, p[1:]):
            edge = tuple(sorted((u, v)))
            assert edge in original and edge not in used_edges
            used_edges.add(edge)
        assert pair not in reduced
        reduced.add(pair)
    assert reduced == {tuple(e) for e in witness["reduced_edges"]}
    assert used_edges == {tuple(e) for e in witness["original_subdivision_edges"]}
    if witness["type"] == "K5":
        assert len(branches) == 5
        assert reduced == {(u, v) for u in branches for v in branches if u < v}
    else:
        assert witness["type"] == "K3,3" and len(branches) == 6
        start = min(branches)
        right = {v if u == start else u for u, v in reduced if start in (u, v)}
        left = branches - right
        assert len(left) == len(right) == 3
        assert reduced == {tuple(sorted((u, v))) for u in left for v in right}


def capacity_control(g):
    vertices, edges, q = g["vertices"], g["edges"], g["q"]
    assert {tuple(e) for e in edges if max(e) < 5} == FRAME
    assert first_lift(vertices, edges, dict(enumerate(q))) is None
    deletions = []
    for e in edges:
        if tuple(e) in FRAME:
            continue
        cut = [x for x in edges if x != e]
        f = first_lift(vertices, cut, dict(enumerate(q)))
        assert f is not None and f[e[0]] == f[e[1]]
        assert all(f[u] != f[v] for u, v in cut)
        deletions.append({"edge": e, "q_witness": f})
    mask = sum(1 << i for i, row in enumerate(PATTERNS)
               if first_lift(vertices, edges, dict(enumerate(row))) is not None)
    assert mask == g["expected_sigma_mask"] and mask & 932 != 932
    degrees = {v: sum(v in e for e in edges) for v in vertices}
    assert [degrees[5], degrees[6]] == [6, 5]
    assert all(degrees[v] == 4 for v in vertices if v >= 7)
    check_kuratowski(edges, g["kuratowski"])
    remaining, components = set(vertices) - set(range(7)), []
    while remaining:
        component, frontier = set(), [min(remaining)]
        while frontier:
            v = frontier.pop()
            if v in component:
                continue
            component.add(v)
            frontier += [w if u == v else u for u, w in edges
                         if v in (u, w) and (w if u == v else u) in remaining - component]
        remaining -= component
        components.append(sorted(component))
    records, forbidden_pairs, mixed_records = [], [], []
    for c in components:
        ports = {r: [v for v in c if [min(r, v), max(r, v)] in edges] for r in (5, 6)}
        tuples = []
        for colors in product(range(4), repeat=len(c)):
            f = dict(enumerate(q)) | dict(zip(c, colors))
            if all(f[u] != f[v] for u, v in edges if u in f and v in f):
                tuples.append(f)
        assert tuples
        owners = [r for r in ports if ports[r]]
        if len(owners) == 1:
            r = owners[0]
            forbidden = sorted(set.intersection(*[{f[v] for v in ports[r]} for f in tuples]))
            records.append({"vertices": c, "root": r, "ports": ports[r],
                            "complete_tuples": [[f[v] for v in c] for f in tuples],
                            "forbidden": forbidden})
        else:
            assert len(owners) == 2
            pairs = [(a, b) for a, b in product(range(4), repeat=2)
                     if not any(all(f[v] != a for v in ports[5]) and
                                all(f[v] != b for v in ports[6]) for f in tuples)]
            forbidden_pairs += pairs
            mixed_records.append({"vertices": c, "contacts": ports,
                                  "complete_tuples": [[f[v] for v in c] for f in tuples],
                                  "forbidden_pairs": pairs})
    assert len(mixed_records) == 1
    assert mixed_records[0]["vertices"] == [7]
    assert mixed_records[0]["contacts"] == {5: [7], 6: [7]}
    assert [5, 6] in edges
    z_records = [r for r in records if r["root"] == 5]
    assert [r["forbidden"] for r in z_records] == g["expected_z_unary_forbidden"]
    budgets = {}
    for root in (5, 6):
        unary = [r for r in records if r["root"] == root]
        factors = [{q[w if u == root else u]} for u, w in edges
                   if root in (u, w) and (w if u == root else u) < 5]
        factors += [set(r["forbidden"]) for r in unary]
        union = set().union(*factors)
        budgets[root] = {"D": sum(len(r["ports"]) - len(r["forbidden"]) for r in unary),
                         "O": sum(map(len, factors)) - len(union),
                         "E": sorted(set(range(4)) - union)}
    ez, ew = set(budgets[5]["E"]), set(budgets[6]["E"])
    assert all(a == b or (a, b) in forbidden_pairs for a, b in product(ez, ew))
    columns = []
    for b in sorted(ew):
        column = {a for a, t in forbidden_pairs if t == b}
        a_set = ez - {b}
        assert a_set <= column and len(column) <= 1
        delta, overlap, leakage = 1 - len(column), 0, len(column - a_set)
        lhs = budgets[5]["D"] + budgets[5]["O"] + delta + overlap + leakage
        rhs = degrees[5] - 5 + int(b in ez)
        assert lhs == rhs
        columns.append({"b": b, "delta": delta, "o": overlap, "lambda": leakage,
                        "lhs": lhs, "rhs": rhs})
    return {"name": g["name"], "sigma_mask": mask, "q_minimal": True,
            "capacity_control_domain": "adjacent two roots; sole shared incidence11 mixed",
            "epsilon": 3, "disk": False, "nonplanar_certificate": g["kuratowski"],
            "T4_hypothesis": "not_triggered", "q_deletion_witnesses": deletions,
            "unary_relations": records, "mixed_relations": mixed_records,
            "mixed_forbidden_pairs": forbidden_pairs,
            "budgets": budgets, "generalized_column_identity": columns}


def build():
    s = json.loads(S935.read_text())["graph"]
    c = json.loads(C44.read_text())
    s_rotation = {r["vertex"]: r["clockwise"] for r in s["embedding"]["rotation"]}
    c_edges = c["source_graph"]["canonical_edges"]
    c_vertices = sorted({v for e in c_edges for v in e})
    c_rotation = {int(v): [w for w in ws if w in c_vertices]
                  for v, ws in c["source_augmented_rotation"].items()
                  if int(v) in c_vertices}
    graphs = [graph_control("S935", s["vertices"], s["edges"], s_rotation, 935),
              graph_control(c["name"], c_vertices, c_edges, c_rotation, 956)]
    # S935 is Sigma-critical but not q-minimal for any rejected literal row.
    assert graphs[0]["q_minimal_rejected_rows"] == []
    p = s["pieces"][0]
    assert p["vertices"] == [5] and p["adjacent_roots"] == [6, 7]
    assert p["actual_support"] == [3, 4] and p["one_sided"]
    f = {0: 0, 1: 1, 2: 2, 3: 0, 4: 1, 6: 2, 7: 3}
    assert all(f[u] != f[v] for u, v in s["edges"] if 5 not in (u, v))
    assert {f[w] for u, w in ((5, 3), (5, 4), (5, 6), (5, 7))} == set(range(4))
    # The supplied C44 subgraph is q-minimal, even though its source has Sigma 956.
    core = c["core"]
    q = tuple(c["rejection_row"]["literal_row"])
    assert q not in relation(core["vertices"], core["edges"])
    core_cuts = []
    for e in core["edges"]:
        if tuple(e) in FRAME:
            continue
        cut = relation(core["vertices"], [x for x in core["edges"] if x != e])
        assert q in cut
        core_cuts.append({"edge": e, "q_witness": cut[q]})
    # Complete tuples cannot be replaced by coordinate marginals.
    joint = {(0, 1), (1, 0)}
    marginals = [{t[i] for t in joint} for i in range(2)]
    assert (0, 0) in set(product(*marginals)) - joint
    # Even all binary projections can miss a ternary restriction.
    parity = {(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)}
    scopes = ((0, 1), (0, 2), (1, 2))
    assert all((1, 1) in {(t[i], t[j]) for t in parity} for i, j in scopes)
    assert (1, 1, 1) not in parity
    # The same J with different observed frame scopes need not have the same P.
    j = {(0, 0), (1, 1)}
    p_singletons = set(product(*[{t[i] for t in j} for i in range(2)]))
    assert p_singletons - j == {(0, 1), (1, 0)}
    capacity = [capacity_control(g) for g in json.loads(CAPACITY.read_text())["graphs"]]
    assert capacity[0]["budgets"][5]["O"] == 1
    assert capacity[1]["budgets"][5]["D"] == 2
    return {"schema": 1, "scope": "two named disk graphs, two nonplanar capacity graphs and abstract controls",
            "inputs_sha256": {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                              for p in (S935, C44, CAPACITY)},
            "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "graphs": graphs,
            "capacity_controls": capacity,
            "S935_short_mixed": {"piece": [5], "support": [3, 4], "shield_edges": [[3, 4]],
                                  "unextendable_outside_coloring": sorted(f.items()),
                                  "broad_long_mixed_claim": "counterexample",
                                  "fixed_933_941_hypothesis": "not_triggered"},
            "C44_qcore": {"edges": core["edges"], "vertices": core["vertices"],
                           "root_degrees": core["root_degrees"], "q": q,
                           "deletion_witnesses": core_cuts,
                           "broad_no_44_claim": "counterexample",
                           "fixed_933_941_hypothesis": "not_triggered"},
            "abstract_controls": {"marginal_joint": sorted(joint), "false_marginal_tuple": [0, 0],
                                  "ternary_parity": sorted(parity), "false_pair_tuple": [1, 1, 1],
                                  "same_J": sorted(j), "P_singleton_scopes": sorted(p_singletons),
                                  "P_full_scope": sorted(j), "graph_realization": "not_asserted"},
            "summary": {"disk_graphs": 2, "literal_rows_per_disk_graph": len(ROWS),
                        "critical_edge_deletions": sum(len(g["deletions"]) for g in graphs),
                        "qcore_edge_deletions": len(core_cuts), "abstract_controls": 3,
                        "nonplanar_capacity_graphs": len(capacity),
                        "capacity_q_deletions": sum(len(g["q_deletion_witnesses"]) for g in capacity),
                        "new_source_classes": 0, "new_lean_theorems": 0}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
    if args.check:
        assert OUT.read_bytes() == payload, f"certificate differs: {OUT}"
    else:
        assert not OUT.exists(), "refuses to overwrite; use --check"
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
