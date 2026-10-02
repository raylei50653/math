#!/usr/bin/env python3
"""Exact even double-fan replacement beyond the wheel-ring inverse rule.

Arbitrary length and context are paper statements. This finite certificate
checks full four-port relations, actual sealed attachments, source disks,
all available frames, reduction obstructions and complete repair relations.
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
from c5_two_vertex_repair_patches import rotation_from_faces, same_orientation
from c5_two_vertex_repair_rings import no_clique_patch
from c5_two_vertex_repair_sources import CORE_NAMES, TABLE, core_edges, core_lift, endpoints
from c5_two_vertex_repair_strips import colour_walk, old_core_embedding, source_relations
from c5_two_vertex_repair_transport import (
    DOMAIN, check_hashes, cycle_edges, project, relation, verify_frame_proofs, word,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/repair_sources.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/repair_fans.json"


def edge(u, v):
    return tuple(sorted((u, v)))


def fan_edges(rim, path):
    return (cycle_edges(tuple(rim)) | {edge(u, v) for u, v in zip(path, path[1:])}
            | {edge(h, v) for h in (rim[0], rim[2]) for v in path[1:-1]})


def local_audit():
    records = []
    for length in (2, 3, 4, 5, 6, 8):
        path = [1, *range(4, length + 3), 3]
        es = sorted(fan_edges((0, 1, 2, 3), path))
        rows, witnesses = graph_extensions(length + 3, es, 4)
        expected = {r for r in product(range(4), repeat=4)
                    if all(r[u] != r[v] for u, v in cycle_edges((0, 1, 2, 3)))
                    and (r[0] == r[2] or ((r[1] == r[3]) == (length % 2 == 0)))}
        assert rows == expected
        lifts = []
        for row in sorted(rows):
            walk = colour_walk(set(range(4)) - {row[0], row[2]}, length, {row[1]}, {row[3]})
            assert walk is not None
            full = row + walk[1:-1]
            assert all(full[u] != full[v] for u, v in es)
            lifts.append(word(full))
        records.append({"length": length, "path": path, "edges": es,
                        "relation": relation(rows), "all_constructive_lifts": lifts,
                        "edge_only_orbit_lifts": {word(r): word(w) for r, w in sorted(witnesses.items())}})
    # Retaining the midpoint colour changes the five-port relation at length 4.
    old5, _ = graph_extensions(5, sorted(fan_edges((0, 1, 2, 3), [1, 4, 3])), 5)
    new_edges = sorted(fan_edges((0, 1, 2, 3), [1, 5, 4, 6, 3]))
    new5, _ = graph_extensions(7, new_edges, 5)
    assert (0, 1, 2, 1, 3) in old5 - new5
    assert (0, 1, 2, 1, 1) in new5 - old5
    broken = [e for e in new_edges if e != (4, 5)]
    bad, lifts = graph_extensions(7, broken, 4)
    assert (0, 1, 2, 3) in bad
    return {"four_port_controls": records,
            "five_port_control": {"port_order": ["a0", "a1", "a2", "a3", "midpoint"],
                "old_relation": relation(old5), "new_relation": relation(new5),
                "old_only": "01213", "new_only": "01211"},
            "missing_path_edge_control": {"edges": broken, "deleted_edge": [4, 5],
                "relation": relation(bad), "rainbow_full_lift": word(lifts[(0, 1, 2, 3)])}}


def replace_star(graph, frames, owners, centre, rim, length, side):
    """Use the two chosen opposite hubs, preserving the whole exterior."""
    assert length >= 2 and length % 2 == 0
    n = len(graph["vertices"])
    inserted = list(range(n, n + length - 2))
    half = length // 2 - 1
    path = [rim[1], *inserted[:half], centre, *inserted[half:], rim[3]]
    es = set(map(tuple, graph["edges"]))
    assert {v if u == centre else u for u, v in es if centre in (u, v)} == set(rim)
    assert cycle_edges(tuple(rim)) <= es
    for rec in frames:
        if rec["available"]:
            faces, _ = trace_faces(dict(enumerate(rec["rotation"])), es)
            star = [f for f in faces if centre in f]
            assert len(star) == 4 and all(len(f) == 3 for f in star)
            assert {frozenset(f) for f in star} == {
                frozenset((centre, rim[i], rim[(i + 1) % 4])) for i in range(4)}
            forward = any(same_orientation((centre, rim[0], rim[1]), f) for f in star)
            new_faces = [f for u, v in zip(path, path[1:])
                         for f in ((rim[0], u, v), (rim[2], v, u))]
            if not forward:
                new_faces = [f[::-1] for f in new_faces]
            rec["rotation"] = rotation_from_faces(n + length - 2,
                [f for f in faces if centre not in f] + new_faces)
        else:
            k = path.index(centre)
            spoke_paths = {rim[0]: [centre, rim[0]], rim[2]: [centre, rim[2]],
                           rim[1]: path[:k + 1][::-1], rim[3]: path[k:]}
            for j, old in enumerate(rec["alternating_paths"]):
                new = [old[0]]
                for u, v in zip(old, old[1:]):
                    segment = (spoke_paths[v] if u == centre else spoke_paths[u][::-1]
                               if v == centre else [u, v])
                    new.extend(segment[1:])
                rec["alternating_paths"][j] = new
    graph["vertices"].extend(f"{side}_fan{v}" for v in inserted)
    graph["edges"] = [list(e) for e in sorted(
        (es - {edge(centre, v) for v in rim}) | fan_edges(rim, path))]
    owners.update({v: side for v in inserted})
    return {"centre": centre, "rim": list(rim), "path": path, "length": length, "owner": side}


def construct(baseline, lengths):
    graph, frames = deepcopy(baseline["graph"]), deepcopy(baseline["frame_certificates"])
    owners = {v: "A" if v < 13 else "B" for v in range(8, 15)}
    steps = [replace_star(graph, frames, owners, centre, rim, length, side)
             for side, centre, rim, length in (
                 ("A", 8, (10, 2, 12, 0), lengths[0]),
                 ("B", 13, (7, 6, 14, 5), lengths[1]))]
    return graph, frames, owners, steps


def verify_structure(graph, frames, owners, steps, orientation):
    """Reverse from full neighbourhoods, before consulting any colour relation."""
    n = len(graph["vertices"])
    assert graph["vertices"][:15] == CORE_NAMES and len(set(graph["vertices"])) == n
    es = set(map(tuple, graph["edges"]))
    assert len(es) == len(graph["edges"]) and all(0 <= u < v < n for u, v in es)
    assert set(owners) == set(range(8, n)), "complete ownership"
    assert set(owners.values()) == {"A", "B"}
    assert all(owners[v] == ("A" if v < 13 else "B") for v in range(8, 15))
    s, t = endpoints(orientation)
    boundaries = {"A": (0, 1, 2, 3, 4), "B": (5, s, 6, t, 7)}
    private = {side: sorted(v for v in owners if owners[v] == side) for side in boundaries}
    vs = {side: set(boundaries[side]) | set(private[side]) for side in boundaries}
    assert all(any({u, v} <= vertices for vertices in vs.values()) for u, v in es), "source ownership"
    remaining, compressed = set(range(n)), set(es)
    for step in reversed(steps):
        centre, rim, path, length, side = (step[k] for k in ("centre", "rim", "path", "length", "owner"))
        assert len(rim) == len(set(rim)) == 4
        assert length >= 2 and length % 2 == 0, "even path length"
        assert len(path) == len(set(path)) == length + 1
        assert path[0] == rim[1] and path[-1] == rim[3]
        assert centre == path[length // 2] and set(path[1:-1]).isdisjoint(rim)
        assert set(rim) | set(path) <= remaining
        assert all(owners.get(v) == side for v in path[1:-1]), "fan ownership"
        assert cycle_edges(tuple(rim)) <= compressed, "complete rim"
        for i, v in enumerate(path[1:-1], 1):
            adjacent = {b if a == v else a for a, b in compressed if v in (a, b)}
            assert adjacent == {rim[0], rim[2], path[i - 1], path[i + 1]}, "complete fan attachments"
        internal = set(path[1:-1])
        compressed = {e for e in compressed if set(e).isdisjoint(internal)} | {edge(centre, v) for v in rim}
        remaining -= internal - {centre}
    assert remaining == set(range(15)) and compressed == core_edges(orientation), "reduced core"
    verify_frame_proofs(frames, graph)
    assert {frozenset(cycle_edges(r["cycle"])) for r in frames if r["available"]} == {
        frozenset(cycle_edges(c)) for c in ((0, 4, 3, 2, 6), (s, 1, t, 7, 5))}
    for side, boundary in boundaries.items():
        se = {e for e in es if set(e) <= vs[side]}
        for rec in frames:
            if not rec["available"]:
                continue
            rot = {v: [w for w in rec["rotation"][v] if w in vs[side]] for v in vs[side]}
            faces, _ = trace_faces(rot, se)
            assert len(vs[side]) - len(se) + len(faces) == 2
            outer, = [f for f in faces if len(f) == 5 and cycle_edges(f) == cycle_edges(boundary)]
            assert all(len(f) == 3 for f in faces if f != outer)
            triangles = {frozenset(c) for c in combinations(sorted(vs[side]), 3) if cycle_edges(c) <= se}
            assert triangles == {frozenset(f) for f in faces if len(f) == 3}
    return private, boundaries


def ring_obstruction(graph, owners):
    """Every sealed ring inverse needs four private degree-five ring vertices."""
    es = set(map(tuple, graph["edges"]))
    degrees = {v: sum(v in e for e in es) for v in owners}
    by_side = {s: [v for v in sorted(owners) if owners[v] == s and degrees[v] == 5] for s in ("A", "B")}
    # Even allowing a cross-source private cap, there are fewer than four.
    assert sum(map(len, by_side.values())) < 4
    return {"private_degrees": {str(v): d for v, d in sorted(degrees.items())},
            "degree_five_vertices_by_source": by_side, "sealed_ring_inverse_possible": False}


def lift(row, orientation, graph, steps):
    full = list(core_lift(row, orientation)) + [-1] * (len(graph["vertices"]) - 15)
    for step in steps:
        rim, path = step["rim"], step["path"]
        walk = colour_walk(set(range(4)) - {full[rim[0]], full[rim[2]]},
                          step["length"], {full[path[0]]}, {full[path[-1]]})
        assert walk is not None
        for v, c in zip(path[1:-1], walk[1:-1]):
            full[v] = c
    assert tuple(full[:8]) == row and all(c in range(4) for c in full)
    assert all(full[u] != full[v] for u, v in graph["edges"])
    return tuple(full)


def audit(baseline, lengths, order):
    orientation = baseline["orientation"]
    graph, frames, owners, steps = construct(baseline, lengths)
    private, boundaries = verify_structure(graph, frames, owners, steps, orientation)
    reduction = no_clique_patch(graph, private, boundaries)
    rings = ring_obstruction(graph, owners)
    sources = source_relations(graph, private, boundaries, order)
    assert [sources[s][1]["class_id"] for s in ("A", "B")] == [127, 167]
    joint, _ = graph_extensions(len(graph["vertices"]), graph["edges"], 8)
    assert joint == {row for row in DOMAIN if all(project(row, boundaries[s]) in sources[s][0] for s in sources)}
    assert relation(joint) == baseline["J"]
    full_lifts = [word(lift(row, orientation, graph, steps)) for row in sorted(joint)]
    fs = [tuple(r["cycle"]) for r in frames if r["available"]]
    flocal = [{project(row, f) for row in joint} for f in fs]
    pullback = {row for row in DOMAIN if all(project(row, f) in rel for f, rel in zip(fs, flocal))}
    assert relation(pullback) == baseline["P"]
    delta = pullback - joint
    scopes = list(combinations(range(8), 4))
    local = [{project(row, s) for row in joint} for s in scopes]
    cuts = [{row for row in delta if project(row, s) not in rel} for s, rel in zip(scopes, local)]
    a, b, t = (baseline["roles"][k] for k in ("A", "B", "T"))
    es = baseline["roles"]["E"]
    repairs = verify_hypotheses(delta, cuts, a, b, t, es, [tuple(map(int, w)) for w, _ in TABLE[orientation]])
    assert [list(ids) for ids in repairs] == baseline["all_inclusion_minimal_repairs"]
    for ids in repairs:
        assert {row for row in pullback if all(project(row, scopes[i]) in local[i] for i in ids)} == joint
    sparse = []
    for (w, completions), rejected in zip(TABLE[orientation], ({a}, {b, t}, {b, *es})):
        witness = tuple(map(int, w))
        rows = [tuple(map(int, q)) for q in completions]
        differences = [{i for i in range(8) if row[i] != witness[i]} for row in rows]
        assert {i for i, s in enumerate(scopes) if not any(set(s).isdisjoint(d) for d in differences)} == rejected
        assert all(any(set(f).isdisjoint(d) for d in differences) for f in fs)
        sparse.append({"witness": w, "exact_rejected_scope_ids": sorted(rejected),
                       "completions": [{"U": word(row), "changed_ports": sorted(d),
                            "full_colouring": word(lift(row, orientation, graph, steps))} for row, d in zip(rows, differences)]})
    residual = []
    for arity in range(5):
        left = set(delta)
        for scope in combinations(range(8), arity):
            projected = {project(row, scope) for row in joint}
            left = {row for row in left if project(row, scope) in projected}
        residual.append(relation(left)["global_s4_orbits"])
    assert residual == [54, 54, 16, 16, 0]
    embeddings = {s: old_core_embedding(graph, orientation, s, private, boundaries) for s in sources}
    for side, length in zip(("A", "B"), lengths):
        assert (embeddings[side] is None) == (length > 2)
        assert reduction[side]["private_graph_is_path"] == (length == 2)
        assert len(reduction[side]["common_private_neighbours"]) == (3 if side == "A" else 2) - (length > 2)
    return {"orientation": orientation, "lengths": lengths, "graph": graph,
            "owners": {str(v): s for v, s in sorted(owners.items())}, "fan_replacements": steps,
            "source_relations": {s: data[1] for s, data in sources.items()},
            "previous_reductions": reduction, "ring_inverse_obstruction": rings,
            "boundary_fixed_old_core_embeddings": embeddings, "frame_certificates": frames,
            "J": relation(joint), "P": relation(pullback), "difference": relation(delta),
            "roles": baseline["roles"], "all_inclusion_minimal_repairs": repairs,
            "arity_residual_orbits": residual, "r_star": 4, "sparse_witness_lifts": sparse,
            "constructive_full_lifts_checked": len(full_lifts),
            "constructive_full_lifts_sha256": sha256(json.dumps(full_lifts).encode()).hexdigest()}


def guards(baseline):
    graph, frames, owners, steps = construct(baseline, (4, 4))
    cases = []
    bad = deepcopy(graph)
    bad["edges"].remove(list(edge(steps[0]["path"][1], steps[0]["path"][2])))
    cases.append(("missing_path_edge", bad, frames, owners, steps))
    bad = deepcopy(graph)
    bad["edges"].append([4, 15])
    cases.append(("extra_private_attachment", bad, frames, owners, steps))
    bad = deepcopy(graph)
    bad["edges"].append([15, 17])
    cases.append(("cross_source_edge", bad, frames, owners, steps))
    cases.append(("missing_owner", graph, frames, {v: s for v, s in owners.items() if v != 15}, steps))
    bad = deepcopy(frames)
    next(r for r in bad if r["available"])["rotation"][0].pop()
    cases.append(("invalid_rotation", graph, bad, owners, steps))
    cases.append(("missing_candidate_frame", graph, frames[1:], owners, steps))
    bad = deepcopy(steps)
    bad[0]["length"] = 3
    cases.append(("odd_length_certificate", graph, frames, owners, bad))
    result = []
    for name, g, fs, own, recipe in cases:
        try:
            verify_structure(g, fs, own, recipe, baseline["orientation"])
        except AssertionError as error:
            result.append({"name": name, "rejected": True, "guard": str(error)})
        else:
            raise AssertionError(f"accepted bad fan: {name}")
    return result


def build():
    saved = json.loads((ROOT / SOURCE).read_text())
    check_hashes(saved)
    join_path = "artifacts/c5_two_vertex_overlap/eight_point_joins.json"
    joins = json.loads((ROOT / join_path).read_text())
    check_hashes(joins)
    order = tuple(map(tuple, joins["pattern_order"]))
    baselines = [r for r in saved["cases"] if not r["elimination"]]
    local = local_audit()
    records = [audit(b, ls, order) for b in baselines for ls in ((4, 2), (2, 4), (4, 4), (6, 8))]
    controls = [dict(c, orientation=b["orientation"]) for b in baselines for c in guards(b)]
    paths = [SOURCE, join_path, "scripts/c5_two_vertex_repair_fans.py",
             "scripts/c5_two_vertex_repair_rings.py", "scripts/c5_two_vertex_repair_strips.py",
             "scripts/c5_two_vertex_repair_patches.py", "scripts/c5_two_vertex_repair_sources.py",
             "scripts/c5_two_vertex_common_repair.py", "scripts/c5_two_vertex_repair_transport.py",
             "scripts/c5_two_vertex_join.py", "scripts/c5_two_vertex_join_topology.py", "scripts/boundary_relations.py"]
    return {"schema": "c5-common-repair-four-port-even-fans-v1",
            "scope": "Exact four-port even double fans and arbitrary-length paper family with no clique, whole-source path, or ring inverse start; not completeness or Lean.",
            "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "local_certificate": local, "cases": records, "negative_controls": controls,
            "summary": {"graph_controls": len(records), "vertex_counts": [len(r["graph"]["vertices"]) for r in records],
                        "full_lifts_checked": sum(r["constructive_full_lifts_checked"] for r in records),
                        "sparse_full_lifts": 11 * len(records), "negative_controls": len(controls),
                        "local_port_assignment_domain": 4**4, "local_length_controls": 6,
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
