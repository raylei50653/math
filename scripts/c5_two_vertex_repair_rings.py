#!/usr/bin/env python3
"""Exact four-port wheel inflation beyond clique patches and private paths.

The arbitrary-depth and arbitrary-context statements are paper proofs. This
finite replay checks local relations, complete attachments, rotations, clique
separators, original-edge colourings, and all common-repair hypotheses.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from boundary_relations import normalize
from c5_two_vertex_common_repair import verify_hypotheses
from c5_two_vertex_join import expand, graph_extensions
from c5_two_vertex_join_topology import components, trace_faces
from c5_two_vertex_repair_patches import rotation_from_faces, same_orientation
from c5_two_vertex_repair_sources import CORE_NAMES, TABLE, core_edges, core_lift, endpoints
from c5_two_vertex_repair_strips import old_core_embedding, source_relations
from c5_two_vertex_repair_transport import (
    DOMAIN, check_hashes, cycle_edges, project, relation, verify_frame_proofs, word,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/repair_sources.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/repair_rings.json"
# For canonical proper non-rainbow rim: four inner-ring colours, then centre.
LIFTS = {"0101": "23230", "0102": "23130", "0121": "23031"}


def edge(u, v):
    return tuple(sorted((u, v)))


def ring_edges(rim, ring, centre):
    return (cycle_edges(tuple(ring)) | {edge(centre, v) for v in ring}
            | {edge(ring[i], rim[j]) for i in range(4) for j in (i, (i + 1) % 4)})


def local_audit():
    rim, ring = tuple(range(4)), tuple(range(4, 8))
    wheel = sorted(cycle_edges(rim) | {edge(v, 4) for v in rim})
    inflated = sorted(cycle_edges(rim) | ring_edges(rim, ring, 8))
    old, _ = graph_extensions(5, wheel, 4)
    new, _ = graph_extensions(9, inflated, 4)
    assert old == new == expand(tuple(map(int, w)) for w in LIFTS)
    for w, tail in LIFTS.items():
        full = tuple(map(int, w + tail))
        assert all(full[u] != full[v] for u, v in inflated)
    annulus = [e for e in inflated if 8 not in e]
    ann, _ = graph_extensions(8, annulus, 8)
    rainbow = sorted(row[4:] for row in ann if row[:4] == (0, 1, 2, 3))
    assert rainbow == [(2, 3, 0, 1), (3, 0, 1, 2)]
    assert all(len(set(row[:4])) < 4 or len(set(row[4:])) == 4 for row in ann)
    # Observing the old centre is forbidden: the full five-port relations differ.
    mapping = {**{i: i for i in range(4)}, 8: 4, **{i: i + 1 for i in range(4, 8)}}
    with_centre = sorted(edge(mapping[u], mapping[v]) for u, v in inflated)
    old5, _ = graph_extensions(5, wheel, 5)
    new5, _ = graph_extensions(9, with_centre, 5)
    assert (0, 1, 0, 1, 2) in old5 - new5
    assert (0, 1, 0, 1, 0) in new5 - old5
    # A missing central spoke admits a rainbow rim, so the cap is substantive.
    broken = [e for e in inflated if e != (4, 8)]
    bad, bad_witnesses = graph_extensions(9, broken, 4)
    assert new < bad and (0, 1, 2, 3) in bad
    return {"wheel_edges": wheel, "inflated_edges": inflated,
            "four_port_relation": relation(new), "annulus_relation": relation(ann),
            "rainbow_inner_words": list(map(word, rainbow)), "lift_templates": LIFTS,
            "five_port_control": {"port_order": ["a0", "a1", "a2", "a3", "centre"],
                "old_relation": relation(old5), "new_relation": relation(new5),
                "old_only": "01012", "new_only": "01010"},
            "missing_spoke_control": {"deleted_edge": [4, 8], "relation": relation(bad),
                "rainbow_full_lift": word(bad_witnesses[(0, 1, 2, 3)])}}


def inflate(graph, frames, owners, centre, side):
    """Replace the whole four-triangle star; retain every other face and edge."""
    n = len(graph["vertices"])
    es = set(map(tuple, graph["edges"]))
    rotation = next(r for r in frames if r["available"])["rotation"]
    neighbours = tuple(rotation[centre])
    assert len(neighbours) == 4
    rim = min(p[i:] + p[:i] for p in (neighbours, neighbours[::-1]) for i in range(4))
    ring = tuple(range(n, n + 4))
    assert cycle_edges(rim) <= es
    for rec in frames:
        if rec["available"]:
            faces, _ = trace_faces(dict(enumerate(rec["rotation"])), es)
            star = [f for f in faces if centre in f]
            assert len(star) == 4 and all(len(f) == 3 for f in star)
            forward = any(same_orientation((centre, rim[0], rim[1]), f) for f in star)
            new_faces = []
            for i, a in enumerate(rim):
                b, z, prev = rim[(i + 1) % 4], ring[i], ring[i - 1]
                new_faces.extend(((a, b, z), (a, z, prev), (centre, prev, z)))
            if not forward:
                new_faces = [f[::-1] for f in new_faces]
            rec["rotation"] = rotation_from_faces(n + 4, [f for f in faces if centre not in f] + new_faces)
        else:
            # Four internally disjoint spoke subdivisions preserve both crosscuts.
            for j, path in enumerate(rec["alternating_paths"]):
                new_path = [path[0]]
                for u, v in zip(path, path[1:]):
                    if centre in (u, v):
                        other = v if u == centre else u
                        new_path.append(ring[rim.index(other)])
                    new_path.append(v)
                rec["alternating_paths"][j] = new_path
    graph["vertices"].extend(f"{side}_ring{v}" for v in ring)
    graph["edges"] = [list(e) for e in sorted(
        (es - {edge(centre, v) for v in rim}) | ring_edges(rim, ring, centre))]
    owners.update({v: side for v in ring})
    return {"centre": centre, "rim": rim, "ring": ring, "owner": side}


def construct(baseline, depths):
    graph, frames = deepcopy(baseline["graph"]), deepcopy(baseline["frame_certificates"])
    owners = {v: "A" if v < 13 else "B" for v in range(8, 15)}
    steps = [inflate(graph, frames, owners, centre, side)
             for side, centre, depth in zip(("A", "B"), (8, 13), depths) for _ in range(depth)]
    return graph, frames, owners, steps


def verify_structure(graph, frames, owners, steps, orientation):
    """Reverse the new local rule using full actual neighbour sets, then check disks."""
    n = len(graph["vertices"])
    assert graph["vertices"][:15] == CORE_NAMES
    assert len(set(graph["vertices"])) == n
    es = set(map(tuple, graph["edges"]))
    assert len(es) == len(graph["edges"]) and all(0 <= u < v < n for u, v in es)
    assert set(owners) == set(range(8, n)), "complete ownership"
    assert all(owners[v] == ("A" if v < 13 else "B") for v in range(8, 15))
    s, t = endpoints(orientation)
    boundaries = {"A": (0, 1, 2, 3, 4), "B": (5, s, 6, t, 7)}
    private = {side: sorted(v for v in owners if owners[v] == side) for side in boundaries}
    vs = {side: set(boundaries[side]) | set(private[side]) for side in boundaries}
    assert set(owners.values()) == {"A", "B"}
    assert all(any({u, v} <= vertices for vertices in vs.values()) for u, v in es), "source ownership"
    remaining = set(range(n))
    compressed = set(es)
    for step in reversed(steps):
        centre, rim, ring, side = (step[k] for k in ("centre", "rim", "ring", "owner"))
        assert len(rim) == len(set(rim)) == len(ring) == len(set(ring)) == 4
        assert len({centre, *rim, *ring}) == 9 and {centre, *rim, *ring} <= remaining
        assert all(owners.get(v) == side for v in (centre, *ring)), "ring ownership"
        assert cycle_edges(tuple(rim)) <= compressed, "complete rim"
        adjacent = lambda v: {b if a == v else a for a, b in compressed if v in (a, b)}
        assert adjacent(centre) == set(ring), "complete centre neighbourhood"
        for i, v in enumerate(ring):
            assert adjacent(v) == {centre, ring[i - 1], ring[(i + 1) % 4], rim[i], rim[(i + 1) % 4]}, "complete ring attachments"
        compressed = {e for e in compressed if set(e).isdisjoint(ring)} | {edge(centre, v) for v in rim}
        remaining -= set(ring)
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
            # Every triangle is facial; there are no separating triangles.
            triangles = {frozenset(c) for c in combinations(sorted(vs[side]), 3) if cycle_edges(c) <= se}
            assert triangles == {frozenset(f) for f in faces if len(f) == 3}
    return private, boundaries


def no_clique_patch(graph, private, boundaries):
    """Exhaust every clique of size <=3 and every complete remaining component."""
    es = set(map(tuple, graph["edges"]))
    result = {}
    for side, boundary in boundaries.items():
        vs = set(boundary) | set(private[side])
        se = {e for e in es if set(e) <= vs}
        counts = [0, 0, 0]
        for size in range(1, 4):
            for cut in combinations(sorted(vs), size):
                if not all(edge(u, v) in se for u, v in combinations(cut, 2)):
                    continue
                counts[size - 1] += 1
                adj = {v: set() for v in vs - set(cut)}
                for u, v in se:
                    if u in adj and v in adj:
                        adj[u].add(v)
                        adj[v].add(u)
                assert all(set(c) & set(boundary) for c in components(adj)), "sealed clique patch exists"
        degrees = [sum(v in e for e in se) for v in private[side]]
        induced = [sum(v in e and set(e) <= set(private[side]) for e in se) for v in private[side]]
        result[side] = {"clique_cuts_checked_by_size": counts, "private_minimum_degree": min(degrees),
                        "private_degree_sequence": sorted(induced),
                        "boundary_pair": [boundary[0], boundary[2]],
                        "common_private_neighbours": [v for v in private[side]
                            if all(edge(v, u) in se for u in (boundary[0], boundary[2]))],
                        "private_graph_is_path": sorted(induced) == [1, 1] + [2] * (len(induced) - 2)}
        assert min(degrees) >= 4
    return result


def lift(row, orientation, graph, steps):
    full = list(core_lift(row, orientation))
    for step in steps:
        colours = tuple(full[v] for v in step["rim"])
        canonical = word(normalize(colours))
        assert canonical in LIFTS
        seen = list(dict.fromkeys(colours))
        permutation = seen + sorted(set(range(4)) - set(seen))
        tail = [permutation[int(c)] for c in LIFTS[canonical]]
        assert list(step["ring"]) == list(range(len(full), len(full) + 4))
        full.extend(tail[:4])
        full[step["centre"]] = tail[4]
    assert tuple(full[:8]) == row
    assert len(full) == len(graph["vertices"])
    assert all(full[u] != full[v] for u, v in graph["edges"])
    return tuple(full)


def audit(baseline, depths, order):
    orientation = baseline["orientation"]
    graph, frames, owners, steps = construct(baseline, depths)
    private, boundaries = verify_structure(graph, frames, owners, steps, orientation)
    reduction = no_clique_patch(graph, private, boundaries)
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
    for side, depth in zip(("A", "B"), depths):
        assert (embeddings[side] is None) == (depth > 0)
        assert reduction[side]["private_graph_is_path"] == (depth == 0)
        assert len(reduction[side]["common_private_neighbours"]) == (3 if side == "A" else 2) - (depth > 0)
    return {"orientation": orientation, "depths": depths, "graph": graph,
            "owners": {str(v): s for v, s in sorted(owners.items())}, "inflations": steps,
            "source_relations": {s: data[1] for s, data in sources.items()},
            "previous_reductions": reduction, "boundary_fixed_old_core_embeddings": embeddings,
            "frame_certificates": frames, "J": relation(joint), "P": relation(pullback),
            "difference": relation(delta), "roles": baseline["roles"],
            "all_inclusion_minimal_repairs": repairs, "arity_residual_orbits": residual,
            "r_star": 4, "sparse_witness_lifts": sparse, "constructive_full_lifts_checked": len(full_lifts),
            "constructive_full_lifts_sha256": sha256(json.dumps(full_lifts).encode()).hexdigest()}


def guards(baseline):
    graph, frames, owners, steps = construct(baseline, (1, 1))
    cases = []
    bad = deepcopy(graph)
    bad["edges"].remove(list(edge(*steps[0]["ring"][:2])))
    cases.append(("missing_ring_edge", bad, frames, owners))
    bad = deepcopy(graph)
    bad["edges"].append([4, 15])
    cases.append(("extra_ring_attachment", bad, frames, owners))
    bad = deepcopy(graph)
    bad["edges"].append([15, 19])
    cases.append(("cross_source_edge", bad, frames, owners))
    cases.append(("missing_owner", graph, frames, {v: s for v, s in owners.items() if v != 15}))
    bad = deepcopy(frames)
    next(r for r in bad if r["available"])["rotation"][0].pop()
    cases.append(("invalid_rotation", graph, bad, owners))
    cases.append(("missing_candidate_frame", graph, frames[1:], owners))
    result = []
    for name, g, fs, own in cases:
        try:
            verify_structure(g, fs, own, steps, baseline["orientation"])
        except AssertionError as error:
            result.append({"name": name, "rejected": True, "guard": str(error)})
        else:
            raise AssertionError(f"accepted bad ring: {name}")
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
    records = [audit(b, ds, order) for b in baselines for ds in ((1, 0), (0, 1), (1, 1), (2, 3))]
    controls = [dict(c, orientation=b["orientation"]) for b in baselines for c in guards(b)]
    paths = [SOURCE, join_path, "scripts/c5_two_vertex_repair_rings.py",
             "scripts/c5_two_vertex_repair_strips.py", "scripts/c5_two_vertex_repair_patches.py",
             "scripts/c5_two_vertex_repair_sources.py", "scripts/c5_two_vertex_common_repair.py",
             "scripts/c5_two_vertex_repair_transport.py", "scripts/c5_two_vertex_join.py",
             "scripts/c5_two_vertex_join_topology.py", "scripts/boundary_relations.py"]
    return {"schema": "c5-common-repair-four-port-rings-v1",
            "scope": "Exact four-port inflation and arbitrary-depth paper family beyond prior clique/path reductions; not a necessary classification or Lean proof.",
            "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "local_certificate": local, "cases": records, "negative_controls": controls,
            "summary": {"graph_controls": len(records), "vertex_counts": [len(r["graph"]["vertices"]) for r in records],
                        "full_lifts_checked": sum(r["constructive_full_lifts_checked"] for r in records),
                        "sparse_full_lifts": 11 * len(records), "negative_controls": len(controls),
                        "local_port_assignment_domain": 4**4, "new_lean_theorem": False}}


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
