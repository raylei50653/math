#!/usr/bin/env python3
"""Replay a sufficient source certificate for the common repair lemma.

The arbitrary-size statement is proved by private degree-three elimination.
This program verifies two original cores and two larger source controls, exact
named colour relations, constructive lifts and all graph-certificate guards.
No new class-pair search, colouring oracle or Lean claim.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_two_vertex_common_repair import verify_hypotheses
from c5_two_vertex_join import graph_extensions
from c5_two_vertex_join_topology import trace_faces
from c5_two_vertex_repair_transport import (
    DOMAIN, FRAMES, SOURCE, check_hashes, cycle_edges, project, reconstruct,
    relation, verify_frame_proofs, word,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_two_vertex_overlap/repair_sources.json"
PORTS = ["a0", "a1", "a2", "a3", "a4", "b0", "b2", "b4"]
CORE_NAMES = PORTS + [f"A_inner{i}" for i in range(5, 10)] + ["B_inner5", "B_inner6"]
A_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4),
           (0, 8), (0, 9), (0, 10), (0, 11), (0, 12),
           (2, 8), (2, 10), (2, 12), (3, 9), (3, 10), (3, 11),
           (1, 12), (4, 11), (8, 12), (8, 10), (9, 10), (9, 11)]
TABLE = {
    "forward": [
        ("01232113", ["31232113", "03232113", "01032113", "01202113"]),
        ("01201130", ["21201130", "01201330", "01201110", "02101132", "01021132"]),
        ("01012122", ["01012112", "01012123"]),
    ],
    "reverse": [
        ("01232112", ["31232112", "03232112", "01032112", "01202112"]),
        ("01212132", ["01012132", "01212332", "01212112", "10212130", "21210130"]),
        ("01012122", ["01012112", "01012123"]),
    ],
}


def edge(u, v):
    return tuple(sorted((u, v)))


def endpoints(orientation):
    assert orientation in TABLE
    return (0, 2) if orientation == "forward" else (2, 0)


def core_edges(orientation):
    s, t = endpoints(orientation)
    b = [(5, s), (s, 6), (6, t), (t, 7), (7, 5), (6, 7),
         (13, 5), (13, 6), (13, 7), (14, 5), (14, 6), (14, s), (13, 14)]
    return {edge(u, v) for u, v in A_EDGES + b}


def source_formula(row, orientation):
    s, _ = endpoints(orientation)
    return (all(row[u] != row[v] for u, v in core_edges(orientation) if v < 8)
            and len({row[i] for i in (0, 1, 2, 3)}) <= 3
            and len({row[i] for i in (0, 4, 3, 2)}) <= 3
            and (row[s] != row[7] or row[5] == row[6]))


def core_lift(row, orientation):
    """The three A cases and two-list B proof, not graph backtracking."""
    assert source_formula(row, orientation)
    x, l, y, m, n, p, q, r = row
    colours = set(range(4))
    full = list(row) + [-1] * 7
    if len({x, y, m}) == 3:
        k = min(colours - {x, y, m})
        assert l == m and n == y
        full[8:13] = [m, y, k, k, k]
    elif x == y:
        k = min(colours - {x, m, n})
        d = min(colours - {x, m, k})
        full[8:13] = [m, d, k, k, min(colours - {x, m, l})]
    else:
        assert x == m
        k = min(colours - {x, y, l})
        d = min(colours - {x, y, k})
        full[8:13] = [d, y, k, min(colours - {x, y, n}), k]
    s, _ = endpoints(orientation)
    pairs = [(v, w) for v in sorted(colours - {p, q, r})
             for w in sorted(colours - {p, q, row[s]}) if v != w]
    assert pairs
    full[13:15] = pairs[0]
    assert all(full[u] != full[v] for u, v in core_edges(orientation))
    return tuple(full)


def verify_source(graph, orientation, peel, owner, frames):
    """Check structure without reading J, P, repairs or witness signatures."""
    names = graph["vertices"]
    n = len(names)
    assert names[:15] == CORE_NAMES and len(names) == len(set(names))
    edges = set(map(tuple, graph["edges"]))
    assert len(edges) == len(graph["edges"])
    assert all(0 <= u < v < n for u, v in edges)
    assert {e for e in edges if e[1] < 15} == core_edges(orientation), "induced core"
    assert set(owner) == set(range(15, n)) and set(owner.values()) <= {"A", "B"}
    side = {"A": set(range(5)) | set(range(8, 13)),
            "B": {0, 2, 5, 6, 7, 13, 14}}
    for v, label in owner.items():
        side[label].add(v)
    assert all(any(u in vs and v in vs for vs in side.values()) for u, v in edges), "source ownership"
    assert len(peel) == len(set(peel)) and set(peel) == set(range(15, n))
    remaining = set(range(n))
    steps = []
    for v in peel:
        ns = sorted(u if w == v else w for u, w in edges
                    if v in (u, w) and u in remaining and w in remaining)
        assert len(ns) <= 3, "private elimination degree"
        steps.append({"vertex": v, "remaining_neighbours": ns})
        remaining.remove(v)
    # Every U cycle gets an actual rotation or inherited original crosscuts.
    verify_frame_proofs(frames, graph)
    s, t = endpoints(orientation)
    expected = {frozenset(cycle_edges(c)) for c in ((0, 4, 3, 2, 6), (s, 1, t, 7, 5))}
    assert {frozenset(cycle_edges(r["cycle"])) for r in frames if r["available"]} == expected
    # Certify each original source disk as well; no simultaneous-region policy.
    for label, cycle in (("A", (0, 1, 2, 3, 4)), ("B", (5, s, 6, t, 7))):
        vs = side[label]
        es = {e for e in edges if set(e) <= vs}
        for record in frames:
            if record["available"]:
                rot = {v: [u for u in record["rotation"][v] if u in vs] for v in vs}
                faces, _ = trace_faces(rot, es)
                assert len(vs) - len(es) + len(faces) == 2
                assert any(len(f) == 5 and cycle_edges(f) == cycle_edges(cycle) for f in faces), "source disk"
    return steps


def extend_peel(full, graph, steps):
    result = list(full) + [-1] * (len(graph["vertices"]) - 15)
    for step in reversed(steps):
        ns = step["remaining_neighbours"]
        assert all(result[u] >= 0 for u in ns)
        result[step["vertex"]] = min(set(range(4)) - {result[u] for u in ns})
    assert all(c in range(4) for c in result)
    assert all(result[u] != result[v] for u, v in graph["edges"])
    return tuple(result)


def stack(graph, frames, triangle, side, owner):
    """Insert one private vertex into a named face in BOTH frame rotations."""
    edges = set(map(tuple, graph["edges"]))
    v = len(graph["vertices"])
    for record in frames:
        if not record["available"]:
            continue
        rot = record["rotation"]
        faces, _ = trace_faces(dict(enumerate(rot)), edges)
        face = next(f for f in faces if len(f) == 3 and set(f) == set(triangle))
        for i, u in enumerate(face):
            before = face[i - 1]
            after = face[(i + 1) % 3]
            assert rot[u][(rot[u].index(before) - 1) % len(rot[u])] == after
            rot[u].insert(rot[u].index(before), v)
        rot.append(list(face))
    graph["vertices"].append(f"{side}_extra{v}")
    graph["edges"] = [list(e) for e in sorted(edges | {edge(u, v) for u in triangle})]
    owner[v] = side
    return v


def rejection(row, role, orientation):
    s, t = endpoints(orientation)
    if role == "A":
        return len({row[i] for i in (0, 1, 2, 3)}) == 4
    if role == "BT":
        return len({row[i] for i in (s, t, 5, 6)}) == 4 and row[s] == row[7] and row[5] != row[6]
    return row[6] == row[7]


def audit(graph, orientation, peel, owner, frames, joint):
    steps = verify_source(graph, orientation, peel, owner, frames)
    formula_joint = {row for row in DOMAIN if source_formula(row, orientation)}
    assert formula_joint == joint
    for row in joint:
        full = extend_peel(core_lift(row, orientation), graph, steps)
        assert full[:8] == row
    fs = [tuple(r["cycle"]) for r in frames if r["available"]]
    locals_ = [{project(row, scope) for row in joint} for scope in fs]
    pullback = {row for row in DOMAIN if all(project(row, scope) in loc for scope, loc in zip(fs, locals_))}
    delta = pullback - joint
    scopes = list(combinations(range(8), 4))
    local = [{project(row, scope) for row in joint} for scope in scopes]
    cuts = [{row for row in delta if project(row, scope) not in loc} for scope, loc in zip(scopes, local)]
    s, t = endpoints(orientation)
    a, b, tt = [scopes.index(tuple(sorted(vs))) for vs in ((0, 1, 2, 3), (s, 5, 6, 7), (s, t, 5, 6))]
    es = [i for i, scope in enumerate(scopes) if {6, 7} <= set(scope) and i != b]
    signatures = [{a}, {b, tt}, {b, *es}]
    records, witnesses = [], []
    for (w, completion_words), role, rejectors in zip(TABLE[orientation], ("A", "BT", "BE"), signatures):
        row = tuple(map(int, w))
        witnesses.append(row)
        assert rejection(row, role, orientation) and row in delta
        completions = [tuple(map(int, q)) for q in completion_words]
        differences = [{i for i in range(8) if row[i] != q[i]} for q in completions]
        assert all(q in joint for q in completions)
        # Sparse completions alone cover EVERY other scope and both frames.
        uncovered = {i for i, scope in enumerate(scopes) if not any(set(scope).isdisjoint(d) for d in differences)}
        assert uncovered == rejectors
        assert all(any(set(scope).isdisjoint(d) for d in differences) for scope in fs)
        records.append({"role": role, "pattern": w, "rejected_scope_ids": sorted(rejectors),
                        "completions": [{"U": word(q), "changed_ports": sorted(d),
                            "full_colouring": word(extend_peel(core_lift(q, orientation), graph, steps))}
                            for q, d in zip(completions, differences)]})
    templates = verify_hypotheses(delta, cuts, a, b, tt, es, witnesses)
    # The paper cover proof only needs these implications, not a projected table.
    assert all(len({q[i] for i in (0, 4, 3, 2)}) <= 3
               and (q[t] != q[5] or q[7] != q[s]) for q in pullback)
    assert all(len({q[i] for i in (s, t, 5, 6)}) <= 3 for q in joint)
    for q in pullback:
        ga = len({q[i] for i in (0, 1, 2, 3)}) <= 3
        gb = q[s] != q[7] or q[5] == q[6]
        ge = q[6] != q[7]
        gt = len({q[i] for i in (s, t, 5, 6)}) <= 3
        assert (q in joint) == (ga and gb and ge)
        assert not (ga and gt and ge) or gb
    return {"orientation": orientation, "graph": graph, "extra_vertex_owners": {str(k): v for k, v in sorted(owner.items())},
            "elimination": steps, "frame_certificates": frames,
            "J": relation(joint), "P": relation(pullback), "difference": relation(delta),
            "witness_completion_table": records, "roles": {"A": a, "B": b, "T": tt, "E": es},
            "all_inclusion_minimal_repairs": templates, "constructive_full_lifts_checked": len(joint)}


def must_reject(name, graph, orientation, peel, owner, frames):
    try:
        verify_source(graph, orientation, peel, owner, frames)
    except AssertionError as error:
        return {"name": name, "rejected": True, "guard": str(error)}
    raise AssertionError(f"accepted bad source certificate: {name}")


def build():
    source = json.loads((ROOT / SOURCE).read_text())
    frame_data = json.loads((ROOT / FRAMES).read_text())
    common_path = "artifacts/c5_two_vertex_overlap/common_repair.json"
    common = json.loads((ROOT / common_path).read_text())
    for data in (source, frame_data, common):
        check_hashes(data)
    catalogue = json.loads((ROOT / "artifacts/c5_cells/cells.json").read_text())
    records, controls, degenerate = [], [], []
    for case in source["cases"][:-2]:
        joint, _, _ = reconstruct(case, catalogue, tuple(map(tuple, source["pattern_order"])))
        frames = frame_data["cases"][case["name"]]
        verify_frame_proofs(frames, case["graph"])
        ports = case["joint"]["ports"]
        available = [tuple(r["cycle"]) for r in frames if r["available"]]
        original = [tuple(ports.index(v) for v in case["boundary_maps"][side]) for side in ("A", "B")]
        assert all(any(cycle_edges(c) == cycle_edges(f) for f in available) for c in original)
        projected = [{project(q, scope) for q in joint} for scope in original]
        source_pullback = {q for q in DOMAIN if all(project(q, s) in r for s, r in zip(original, projected))}
        assert source_pullback == joint
        frame_relations = [{project(q, scope) for q in joint} for scope in available]
        pullback = {q for q in DOMAIN if all(project(q, s) in r for s, r in zip(available, frame_relations))}
        assert pullback == joint
        degenerate.append({"name": case["name"], "original_frame_scopes": original,
                           "J": relation(joint), "P_equals_J": True, "unique_minimal_repair": []})
    for case, orientation in zip(source["cases"][-2:], TABLE):
        graph = {key: deepcopy(case["graph"][key]) for key in ("vertices", "edges")}
        frames = deepcopy(frame_data["cases"][case["name"]])
        joint, _, _ = reconstruct(case, catalogue, tuple(map(tuple, source["pattern_order"])))
        rec = audit(graph, orientation, [], {}, frames, joint)
        rec["name"] = case["name"]
        old = next(c for c in common["cases"] if c["name"] == case["name"])
        assert rec["J"] == old["J"] and rec["P"] == old["P"]
        assert [list(ids) for ids in rec["all_inclusion_minimal_repairs"]] == old["all_inclusion_minimal_repairs"]
        records.append(rec)
        enlarged, larger_frames, owner = deepcopy(graph), deepcopy(frames), {}
        for side, triangle in (("A", (0, 8, 10)), ("B", (6, 13, 14))):
            for _ in range(3):
                v = stack(enlarged, larger_frames, triangle, side, owner)
                triangle = (triangle[0], triangle[1], v)
        peel = list(reversed(range(15, len(enlarged["vertices"]))))
        actual, _ = graph_extensions(len(enlarged["vertices"]), list(map(tuple, enlarged["edges"])), 8)
        assert actual == joint
        rec = audit(enlarged, orientation, peel, owner, larger_frames, actual)
        rec["name"] = case["name"] + "_six_private_insertions"
        records.append(rec)
        bad = deepcopy(graph)
        bad["edges"].remove([6, 7])
        controls.append(must_reject(orientation + "_missing_core_edge", bad, orientation, [], {}, frames))
        bad = deepcopy(enlarged)
        bad["edges"].append([13, 15])
        controls.append(must_reject(orientation + "_cross_source_attachment", bad, orientation, peel, owner, larger_frames))
        bad = deepcopy(enlarged)
        bad["edges"].append([1, 17])
        controls.append(must_reject(orientation + "_degree_four_elimination", bad, orientation, peel, owner, larger_frames))
        bad_frames = deepcopy(larger_frames)
        available = next(r for r in bad_frames if r["available"])
        available["rotation"][0].pop()
        controls.append(must_reject(orientation + "_invalid_frame_rotation", enlarged, orientation, peel, owner, bad_frames))
        controls.append(must_reject(orientation + "_unsealed_extra_vertex", enlarged, orientation, peel[1:], owner, larger_frames))
        # Containing the core alone is insufficient: a degree-four private star
        # can reject a previously valid row, even within just the A source.
        bad = deepcopy(graph)
        bad["vertices"].append("A_extra15")
        bad["edges"] = [list(e) for e in sorted(set(map(tuple, bad["edges"])) | {(u, 15) for u in (0, 1, 2, 4)})]
        row = min(q for q in joint if len({q[i] for i in (0, 1, 2, 4)}) == 4)
        control = must_reject(orientation + "_degree_four_star_changes_J", bad, orientation, [15], {15: "A"}, frames)
        control.update(original_J_witness=word(row), new_vertex=15, four_colour_neighbours=[0, 1, 2, 4])
        controls.append(control)
    paths = [SOURCE, FRAMES, common_path, "artifacts/c5_cells/cells.json",
             "scripts/c5_two_vertex_repair_sources.py", "scripts/c5_two_vertex_common_repair.py",
             "scripts/c5_two_vertex_repair_transport.py", "scripts/c5_two_vertex_join.py",
             "scripts/c5_two_vertex_join_topology.py", "scripts/boundary_relations.py"]
    return {"schema": "c5-common-repair-source-certificate-v1",
            "scope": "Paper sufficient source theorem: named induced core, sealed private degree <=3 elimination, source ownership, both mixed-frame rotations. Two cores and two larger controls; not all source graphs or Lean.",
            "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "cases": records, "degenerate_source_cases": degenerate, "negative_controls": controls,
            "summary": {"original_cores": 2, "larger_graph_controls": 2, "degenerate_source_cases": len(degenerate), "sparse_completion_rows_per_core": 11,
                        "full_lifts_checked": sum(r["constructive_full_lifts_checked"] for r in records),
                        "negative_controls": len(controls), "new_lean_theorem": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        assert OUT.read_bytes() == payload, "artifact differs"
        print("checked", OUT.relative_to(ROOT))
    else:
        OUT.write_bytes(payload)
        print("wrote", OUT.relative_to(ROOT))
    print(json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
