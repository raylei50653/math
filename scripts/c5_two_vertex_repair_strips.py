#!/usr/bin/env python3
"""Parity strips with the same C5 classes but no boundary-fixed old core.

Paper arbitrary-length proofs are separate from these finite edge-only,
rotation, full-relation, constructive-lift and repair-certificate checks.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_two_vertex_common_repair import verify_hypotheses
from c5_two_vertex_join import expand, graph_extensions
from c5_two_vertex_join_topology import trace_faces
from c5_two_vertex_repair_patches import rotation_from_faces
from c5_two_vertex_repair_sources import CORE_NAMES, TABLE, core_edges, endpoints
from c5_two_vertex_repair_transport import (
    DOMAIN, check_hashes, cycle_edges, project, relation, verify_frame_proofs, word,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/repair_sources.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/repair_strips.json"


def edge(u, v):
    return tuple(sorted((u, v)))


def path_edges(path):
    return {edge(u, v) for u, v in zip(path, path[1:])}


def stretch(graph, frames, owner, u, v, hubs, length, side):
    """Replace the two incident triangles by a triangulated path strip."""
    assert length >= 1
    if length == 1:
        return
    old_edges = set(map(tuple, graph["edges"]))
    assert edge(u, v) in old_edges
    n = len(graph["vertices"])
    inserted = list(range(n, n + length - 1))
    path = [u, *inserted, v]
    for record in frames:
        if record["available"]:
            faces, _ = trace_faces(dict(enumerate(record["rotation"])), old_edges)
            changed = []
            found_hubs = []
            for face in faces:
                if edge(u, v) not in cycle_edges(face):
                    changed.append(face)
                    continue
                assert len(face) == 3
                hub, = set(face) - {u, v}
                found_hubs.append(hub)
                forward = any(face[i] == u and face[(i + 1) % 3] == v for i in range(3))
                oriented = path if forward else path[::-1]
                changed.extend((a, b, hub) for a, b in zip(oriented, oriented[1:]))
            assert set(found_hubs) == set(hubs) and len(found_hubs) == 2
            record["rotation"] = rotation_from_faces(n + length - 1, changed)
        else:
            for i, old in enumerate(record["alternating_paths"]):
                new = [old[0]]
                for a, b in zip(old, old[1:]):
                    segment = path if (a, b) == (u, v) else path[::-1]
                    new.extend(segment[1:] if edge(a, b) == edge(u, v) else [b])
                record["alternating_paths"][i] = new
    graph["vertices"].extend(f"{side}_strip{i}" for i in inserted)
    graph["edges"] = [list(e) for e in sorted(
        (old_edges - {edge(u, v)}) | path_edges(path)
        | {edge(h, z) for h in hubs for z in inserted})]
    owner.update({z: side for z in inserted})


def construct(baseline, lengths):
    left, right, b_length = lengths
    graph, frames = deepcopy(baseline["graph"]), deepcopy(baseline["frame_certificates"])
    owner = {v: "A" if v < 13 else "B" for v in range(8, 15)}
    stretch(graph, frames, owner, 12, 8, (0, 2), left - 1, "A")
    stretch(graph, frames, owner, 9, 11, (0, 3), right - 1, "A")
    stretch(graph, frames, owner, 13, 14, (5, 6), b_length, "B")
    return graph, frames, owner


def verify_structure(graph, orientation, owner, frames):
    """Extract the two whole private paths from edges, without relation data."""
    n = len(graph["vertices"])
    assert graph["vertices"][:8] == CORE_NAMES[:8]
    assert len(set(graph["vertices"])) == n
    edges = set(map(tuple, graph["edges"]))
    assert len(edges) == len(graph["edges"]) and all(0 <= u < v < n for u, v in edges)
    assert set(owner) == set(range(8, n)), "complete ownership"
    assert set(owner.values()) == {"A", "B"}
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    s, t = endpoints(orientation)
    boundaries = {"A": (0, 1, 2, 3, 4), "B": (5, s, 6, t, 7)}
    paths = {}
    for side, end_port in (("A", 1), ("B", 7)):
        private = {v for v, label in owner.items() if label == side}
        starts = adj[end_port] & private
        assert len(starts) == 1, "unique endpoint attachment"
        start, = starts
        path = [start]
        while True:
            onward = (adj[path[-1]] & private) - set(path[-2:])
            if not onward:
                break
            assert len(onward) == 1, "private path branching"
            nxt, = onward
            assert nxt not in path, "private path cycle"
            path.append(nxt)
        assert set(path) == private, "complete private path"
        paths[side] = path
    a, b = paths["A"], paths["B"]
    centres = [i for i, v in enumerate(a) if {2, 3} <= adj[v]]
    assert len(centres) == 1, "unique A centre"
    centre, = centres
    lengths = (centre, len(a) - 1 - centre, len(b) - 1)
    assert lengths[0] >= 2 and lengths[1] >= 2 and lengths[2] >= 1, "path lengths"
    expected = cycle_edges(boundaries["A"]) | cycle_edges(boundaries["B"]) | {(6, 7)}
    expected |= path_edges(a) | path_edges(b)
    expected |= {edge(0, v) for v in a} | {edge(2, v) for v in a[:centre + 1]}
    expected |= {edge(3, v) for v in a[centre:]} | {edge(1, a[0]), edge(4, a[-1])}
    expected |= {edge(h, v) for h in (5, 6) for v in b} | {edge(7, b[0]), edge(s, b[-1])}
    assert edges == expected, "complete actual attachments"
    assert min(len(adj[v]) for v in owner) >= 4, "private minimum degree"
    verify_frame_proofs(frames, graph)
    available = [r for r in frames if r["available"]]
    assert {frozenset(cycle_edges(r["cycle"])) for r in available} == {
        frozenset(cycle_edges(c)) for c in ((0, 4, 3, 2, 6), (s, 1, t, 7, 5))}
    for side, boundary in boundaries.items():
        vs = set(boundary) | set(paths[side])
        es = {e for e in edges if set(e) <= vs}
        for rec in available:
            rot = {v: [w for w in rec["rotation"][v] if w in vs] for v in vs}
            faces, _ = trace_faces(rot, es)
            assert len(vs) - len(es) + len(faces) == 2
            outer, = [f for f in faces if len(f) == 5 and cycle_edges(f) == cycle_edges(boundary)]
            assert all(len(f) == 3 for f in faces if f != outer)
    return paths, lengths, boundaries


def formulas(row, orientation, lengths):
    x, l, y, m, n, p, q, r = row
    left, right, b_length = lengths
    s, t = endpoints(orientation)
    proper_a = all(row[u] != row[v] for u, v in cycle_edges((0, 1, 2, 3, 4)))
    proper_b = all(row[u] != row[v] for u, v in cycle_edges((5, s, 6, t, 7)) | {(6, 7)})
    a = proper_a and (x in (y, m) or (
        ((l == m) == (left % 2 == 0)) and ((n == y) == (right % 2 == 0))))
    b = proper_b and (p == q or ((r == row[s]) == (b_length % 2 == 0)))
    return a, b


def colour_walk(alphabet, length, starts, ends):
    """Finite path recurrence; never consult the graph relation or class mask."""
    paths = {c: (c,) for c in sorted(set(alphabet) & set(starts))}
    for _ in range(length):
        paths = {c: min(w + (c,) for last, w in paths.items() if last != c)
                 for c in sorted(alphabet) if any(last != c for last in paths)}
    choices = [w for c, w in paths.items() if c in ends]
    return min(choices) if choices else None


def lift(row, graph, paths, lengths, orientation):
    assert all(formulas(row, orientation, lengths))
    colours = set(range(4))
    x, l, y, m, n, p, q, r = row
    left, right, b_length = lengths
    a, b = paths["A"], paths["B"]
    full = list(row) + [-1] * (len(graph["vertices"]) - 8)
    for c in sorted(colours - {x, y, m}):
        wl = colour_walk(colours - {x, y}, left, colours - {x, y, l}, {c})
        wr = colour_walk(colours - {x, m}, right, {c}, colours - {x, m, n})
        if wl is not None and wr is not None:
            for v, colour in zip(a, wl + wr[1:]):
                full[v] = colour
            break
    else:
        raise AssertionError("A constructive path lift")
    s, _ = endpoints(orientation)
    wb = colour_walk(colours - {p, q}, b_length, colours - {p, q, r}, colours - {p, q, row[s]})
    assert wb is not None
    for v, colour in zip(b, wb):
        full[v] = colour
    assert all(c in range(4) for c in full)
    assert all(full[u] != full[v] for u, v in graph["edges"])
    return tuple(full)


def source_relations(graph, paths, boundaries, order):
    result = {}
    for side, boundary in boundaries.items():
        mapping = list(boundary) + paths[side]
        lookup = {v: i for i, v in enumerate(mapping)}
        edges = sorted(edge(lookup[u], lookup[v]) for u, v in graph["edges"] if u in lookup and v in lookup)
        rows, _ = graph_extensions(len(mapping), edges, 5)
        result[side] = (rows, {"vertex_map": mapping, "edges": edges, "relation": relation(rows),
                              "class_id": sum(1 << i for i, row in enumerate(order) if row in rows)})
    return result


def old_core_embedding(graph, orientation, side, paths, boundaries):
    """Independent exhaustive subgraph test; fixes boundary and ownership."""
    old_private = list(range(8, 13)) if side == "A" else [13, 14]
    old_vertices = set(boundaries[side]) | set(old_private)
    old_edges = {e for e in core_edges(orientation) if set(e) <= old_vertices}
    actual = set(map(tuple, graph["edges"]))
    mapping = {v: v for v in boundaries[side]}

    def visit():
        remaining = [v for v in old_private if v not in mapping]
        if not remaining:
            return dict(mapping)
        v = max(remaining, key=lambda z: (sum(edge(z, w) in old_edges for w in mapping), -z))
        for w in paths[side]:
            if w in mapping.values():
                continue
            if all(edge(v, u) not in old_edges or edge(w, z) in actual for u, z in mapping.items()):
                mapping[v] = w
                found = visit()
                if found is not None:
                    return found
                del mapping[v]
        return None

    return visit()


def audit(baseline, lengths, order):
    orientation = baseline["orientation"]
    graph, frames, owner = construct(baseline, lengths)
    paths, actual_lengths, boundaries = verify_structure(graph, orientation, owner, frames)
    assert tuple(lengths) == actual_lengths
    sources = source_relations(graph, paths, boundaries, order)
    assert [sources[s][1]["class_id"] for s in ("A", "B")] == [127, 167]
    joint, _ = graph_extensions(len(graph["vertices"]), graph["edges"], 8)
    joined = {row for row in DOMAIN if all(project(row, boundaries[s]) in sources[s][0] for s in sources)}
    assert joint == joined == {row for row in DOMAIN if all(formulas(row, orientation, lengths))}
    assert joint == expand(tuple(map(int, w)) for w in baseline["J"]["patterns"])
    for row in sorted(joint):
        assert lift(row, graph, paths, lengths, orientation)[:8] == row
    fs = [tuple(r["cycle"]) for r in frames if r["available"]]
    flocal = [{project(row, scope) for row in joint} for scope in fs]
    pullback = {row for row in DOMAIN if all(project(row, s) in rel for s, rel in zip(fs, flocal))}
    assert relation(pullback) == baseline["P"]
    delta = pullback - joint
    scopes = list(combinations(range(8), 4))
    local = [{project(row, scope) for row in joint} for scope in scopes]
    cuts = [{row for row in delta if project(row, s) not in rel} for s, rel in zip(scopes, local)]
    a, b, t = (baseline["roles"][k] for k in ("A", "B", "T"))
    es = baseline["roles"]["E"]
    witnesses = [tuple(map(int, w)) for w, _ in TABLE[orientation]]
    repairs = verify_hypotheses(delta, cuts, a, b, t, es, witnesses)
    assert [list(ids) for ids in repairs] == baseline["all_inclusion_minimal_repairs"]
    for ids in repairs:
        assert {row for row in pullback if all(project(row, scopes[i]) in local[i] for i in ids)} == joint
    sparse = []
    for (w, completions), rejected in zip(TABLE[orientation], ({a}, {b, t}, {b, *es})):
        witness = tuple(map(int, w))
        lifts, differences = [], []
        for q in completions:
            row = tuple(map(int, q))
            full = lift(row, graph, paths, lengths, orientation)
            changed = {i for i in range(8) if row[i] != witness[i]}
            differences.append(changed)
            lifts.append({"U": q, "changed_ports": sorted(changed), "full_colouring": word(full)})
        assert {i for i, scope in enumerate(scopes) if not any(set(scope).isdisjoint(d) for d in differences)} == rejected
        assert all(any(set(scope).isdisjoint(d) for d in differences) for scope in fs)
        sparse.append({"witness": w, "exact_rejected_scope_ids": sorted(rejected), "completions": lifts})
    residual = []
    for arity in range(5):
        left = set(delta)
        for scope in combinations(range(8), arity):
            projected = {project(row, scope) for row in joint}
            left = {row for row in left if project(row, scope) in projected}
        residual.append(relation(left)["global_s4_orbits"])
    assert residual == [54, 54, 16, 16, 0]
    embeddings = {s: old_core_embedding(graph, orientation, s, paths, boundaries) for s in sources}
    assert (embeddings["A"] is not None) == (lengths[:2] == (2, 2))
    assert (embeddings["B"] is not None) == (lengths[2] == 1)
    assert None in embeddings.values()
    return {"orientation": orientation, "lengths": lengths, "graph": graph,
            "owners": {str(v): s for v, s in sorted(owner.items())}, "private_paths": paths,
            "sources": {s: data[1] for s, data in sources.items()}, "frame_certificates": frames,
            "boundary_fixed_old_source_core_embeddings": embeddings,
            "private_minimum_degree": min(sum(v in e for e in graph["edges"]) for v in owner),
            "J": relation(joint), "P": relation(pullback), "difference": relation(delta),
            "roles": baseline["roles"], "all_inclusion_minimal_repairs": repairs,
            "arity_residual_orbits": residual, "r_star": 4, "sparse_witness_lifts": sparse,
            "constructive_full_lifts_checked": len(joint)}


def parity_controls(baseline, order):
    """All eight parity combinations, on actual disk sources, with witnesses."""
    result = []
    original = {}
    for lengths in product((2, 3), (2, 3), (1, 2)):
        graph, frames, owner = construct(baseline, lengths)
        paths, _, boundaries = verify_structure(graph, "forward", owner, frames)
        sources = source_relations(graph, paths, boundaries, order)
        source_records = {}
        for side, (rows, record) in sources.items():
            boundary = boundaries[side]
            # The source formula ignores ports belonging solely to the other side.
            formula_rows = set()
            for row in product(range(4), repeat=5):
                full = [0] * 8
                for v, c in zip(boundary, row):
                    full[v] = c
                if formulas(full, "forward", lengths)[0 if side == "A" else 1]:
                    formula_rows.add(row)
            assert rows == formula_rows
            if lengths == (2, 2, 1):
                original[side] = rows
            difference = rows ^ original[side]
            witness = min(difference) if difference else None
            source_records[side] = {**record, "same_as_old_class": not difference,
                                    "separating_assignment": word(witness) if witness else None,
                                    "new_accepts_witness": witness in rows if witness else None}
        assert source_records["A"]["same_as_old_class"] == (lengths[:2] == (2, 2))
        assert source_records["B"]["same_as_old_class"] == (lengths[2] == 1)
        result.append({"lengths": lengths, "sources": source_records,
                       "graph": graph, "frame_certificates": frames})
    return result


def guard_controls(baseline):
    graph, frames, owner = construct(baseline, (4, 4, 3))
    cases = []
    bad = deepcopy(graph)
    bad["edges"].remove([6, 7])
    cases.append(("missing_boundary_chord", bad, owner, frames))
    bad = deepcopy(graph)
    bad["edges"].append([13, 15])
    cases.append(("cross_source_private_edge", bad, owner, frames))
    bad = deepcopy(graph)
    bad["edges"].append([4, 15])
    cases.append(("extra_boundary_attachment", bad, owner, frames))
    cases.append(("missing_owner", graph, {v: s for v, s in owner.items() if v != 15}, frames))
    bad_frames = deepcopy(frames)
    next(r for r in bad_frames if r["available"])["rotation"][0].pop()
    cases.append(("invalid_rotation", graph, owner, bad_frames))
    bad_frames = deepcopy(frames)
    bad_frames.pop()
    cases.append(("omitted_candidate_frame", graph, owner, bad_frames))
    result = []
    for name, g, own, fs in cases:
        try:
            verify_structure(g, baseline["orientation"], own, fs)
        except AssertionError as error:
            result.append({"name": name, "rejected": True, "guard": str(error)})
        else:
            raise AssertionError(f"accepted bad strip: {name}")
    return result


def fixed_endpoint_control():
    # Local strip replacement preserves the source boundary relation only
    # after existentially recolouring private vertices, not all four contacts.
    spokes = {edge(h, v) for h in (0, 1) for v in (2, 3)}
    old_edges = sorted(spokes | {(2, 3)})
    new_edges = sorted(spokes | {(2, 4), (4, 5), (3, 5)}
                       | {edge(h, v) for h in (0, 1) for v in (4, 5)})
    old, _ = graph_extensions(4, old_edges, 4)
    new, _ = graph_extensions(6, new_edges, 4)
    witness = (0, 0, 1, 1)
    full = witness + (2, 3)
    assert old < new and witness in new - old
    assert all(full[u] != full[v] for u, v in new_edges)
    return {"ports": ["hub0", "hub1", "u", "v"], "old_edges": old_edges,
            "new_edges": new_edges, "old_relation": relation(old), "new_relation": relation(new),
            "new_only_assignment": word(witness), "full_new_colouring": word(full)}


def build():
    saved = json.loads((ROOT / SOURCE).read_text())
    check_hashes(saved)
    join_path = "artifacts/c5_two_vertex_overlap/eight_point_joins.json"
    joins = json.loads((ROOT / join_path).read_text())
    check_hashes(joins)
    order = tuple(map(tuple, joins["pattern_order"]))
    baselines = [r for r in saved["cases"] if not r["elimination"]]
    lengths = ((4, 2, 1), (2, 4, 1), (2, 2, 3), (4, 4, 3), (6, 8, 5))
    records = [audit(b, ls, order) for b in baselines for ls in lengths]
    controls = [dict(c, orientation=b["orientation"]) for b in baselines for c in guard_controls(b)]
    parity = parity_controls(baselines[0], order)
    paths = [SOURCE, join_path, "scripts/c5_two_vertex_repair_strips.py",
             "scripts/c5_two_vertex_repair_patches.py", "scripts/c5_two_vertex_repair_sources.py",
             "scripts/c5_two_vertex_common_repair.py", "scripts/c5_two_vertex_repair_transport.py",
             "scripts/c5_two_vertex_join.py", "scripts/c5_two_vertex_join_topology.py", "scripts/boundary_relations.py"]
    return {"schema": "c5-common-repair-parity-strips-v1",
            "scope": "Paper arbitrary-length parity classification in a specified strip family, not all same-class sources or Lean.",
            "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "cases": records, "parity_controls": parity, "negative_controls": controls,
            "fixed_endpoint_counterexample": fixed_endpoint_control(),
            "summary": {"core_absent_controls": len(records),
                        "vertex_counts": [len(r["graph"]["vertices"]) for r in records],
                        "full_lifts_checked": sum(r["constructive_full_lifts_checked"] for r in records),
                        "sparse_full_lifts": 11 * len(records), "parity_controls": len(parity),
                        "negative_controls": len(controls), "fixed_endpoint_counterexamples": 1,
                        "new_lean_theorem": False}}


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
