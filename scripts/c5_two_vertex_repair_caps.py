#!/usr/bin/env python3
"""A fixed asymmetric four-port disk beyond ring and even-fan reductions.

The local table and rejection argument are paper proofs. This certificate
checks complete attachments, source disks, relations, repairs, and sufficient
degree obstructions independently of the construction's claimed equivalence.
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
from c5_two_vertex_join_topology import trace_faces
from c5_two_vertex_repair_fans import fan_edges
from c5_two_vertex_repair_patches import rotation_from_faces, same_orientation
from c5_two_vertex_repair_rings import no_clique_patch, ring_edges
from c5_two_vertex_repair_sources import CORE_NAMES, TABLE, core_edges, core_lift, endpoints
from c5_two_vertex_repair_strips import old_core_embedding, source_relations
from c5_two_vertex_repair_transport import (
    DOMAIN, check_hashes, cycle_edges, project, relation, verify_frame_proofs, word,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/repair_sources.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/repair_caps.json"
# Ports are 0,1,2,3 in that order. Every triangle is an oriented inner face.
FACES = ((0, 9, 3), (2, 12, 11), (0, 4, 9), (11, 1, 2),
         (6, 11, 12), (7, 5, 8), (5, 6, 12), (7, 10, 6),
         (7, 6, 5), (9, 4, 6), (9, 6, 10), (11, 6, 4),
         (0, 1, 11), (0, 11, 4), (8, 10, 7), (9, 10, 8),
         (9, 8, 3), (5, 12, 2), (3, 8, 5), (3, 5, 2))
EDGES = set().union(*(cycle_edges(f) for f in FACES))
LIFTS = {"0101": "120102321", "0102": "310201323", "0121": "102123031"}
# A subdivision of the four old spokes, with centre 4; interiors are disjoint.
SPOKES = ((4, 0), (4, 11, 1), (4, 6, 12, 2), (4, 9, 3))


def edge(u, v):
    return tuple(sorted((u, v)))


def neighbours(n, es):
    ns = [set() for _ in range(n)]
    for u, v in es:
        ns[u].add(v)
        ns[v].add(u)
    return ns


def obstruction_data(graph, owners):
    """Necessary patterns for EVERY sealed inverse, irrespective of naming."""
    ns = neighbours(len(graph["vertices"]), graph["edges"])
    d4 = {v for v in owners if len(ns[v]) == 4}
    d5 = {v for v in owners if len(ns[v]) == 5}
    matching = all(len(ns[v] & d4) <= 1 for v in d4)
    d5_counts = {str(v): len(ns[v] & d5) for v in sorted(d4)}
    ring_candidates = [v for v in sorted(d4) if len(ns[v] & d5) == 4]
    return {"private_degrees": {str(v): len(ns[v]) for v in sorted(owners)},
            "degree_four_vertices": sorted(d4), "degree_five_vertices": sorted(d5),
            "degree_four_induced_edges": sorted(e for e in map(tuple, graph["edges"]) if set(e) <= d4),
            "degree_four_induced_maximum_degree_at_most_one": matching,
            "private_degree_five_neighbours_of_degree_four": d5_counts,
            "possible_ring_centres_by_degree": ring_candidates}


def verify_obstructions(graph, owners):
    data = obstruction_data(graph, owners)
    assert min(data["private_degrees"].values()) >= 4, "private low degree"
    assert data["degree_four_induced_maximum_degree_at_most_one"], "possible even-fan path"
    assert not data["possible_ring_centres_by_degree"], "possible ring centre"
    assert all(k <= 1 for k in data["private_degree_five_neighbours_of_degree_four"].values())
    return data


def local_audit():
    ns = neighbours(13, EDGES)
    rot = rotation_from_faces(13, [*FACES, (3, 2, 1, 0)])
    faces, _ = trace_faces(dict(enumerate(rot)), EDGES)
    assert len(EDGES) == 32 and 13 - len(EDGES) + len(faces) == 2
    assert {frozenset(f) for f in FACES} == {
        frozenset(t) for t in combinations(range(13), 3) if cycle_edges(t) <= EDGES}
    for i, path in enumerate(SPOKES):
        assert path[0] == 4 and path[-1] == i
        assert all(edge(u, v) in EDGES for u, v in zip(path, path[1:]))
        assert not set(path[1:-1]) & set(range(4))
    assert sum(len(p[1:-1]) for p in SPOKES) == len(set().union(*(set(p[1:-1]) for p in SPOKES)))
    rows, ws = graph_extensions(13, sorted(EDGES), 4)
    wheel = sorted(cycle_edges((0, 1, 2, 3)) | {edge(v, 4) for v in range(4)})
    old, _ = graph_extensions(5, wheel, 4)
    assert old == rows == expand(tuple(map(int, w)) for w in LIFTS)
    for w, tail in LIFTS.items():
        full = tuple(map(int, w + tail))
        assert len(full) == 13 and all(full[u] != full[v] for u, v in EDGES)
    old5, _ = graph_extensions(5, wheel, 5)
    new5, _ = graph_extensions(13, sorted(EDGES), 5)
    assert (0, 1, 2, 1, 3) in old5 - new5 and (0, 1, 0, 1, 1) in new5 - old5
    broken = sorted(EDGES - {(4, 6)})
    bad, bw = graph_extensions(13, broken, 4)
    assert (0, 1, 2, 3) in bad
    obstructions = verify_obstructions({"vertices": list(range(13)), "edges": sorted(EDGES)}, range(4, 13))
    # Positive controls: the degree screen must not certify known reductions.
    ring = sorted(cycle_edges((0, 1, 2, 3)) | ring_edges(range(4), range(4, 8), 8))
    fan = sorted(fan_edges((0, 1, 2, 3), (1, 4, 5, 6, 3)))
    controls = []
    for name, n, es in (("actual_ring", 9, ring), ("actual_even_fan", 7, fan)):
        data = obstruction_data({"vertices": list(range(n)), "edges": es}, range(4, n))
        if name == "actual_ring":
            assert data["possible_ring_centres_by_degree"] == [8]
        else:
            assert not data["degree_four_induced_maximum_degree_at_most_one"]
        controls.append({"name": name, "edges": es, "degree_screen": data})
    # Fixed rejected candidate: two pentagonal rings with caps, one edge removed.
    u = lambda i: 2 + i % 5
    v = lambda i: 7 + i % 5
    sphere = [f for i in range(5) for f in ((0, u(i), u(i + 1)), (1, v(i + 1), v(i)),
              (u(i), v(i), u(i + 1)), (u(i + 1), v(i), v(i + 1)))]
    ie = set().union(*(cycle_edges(f) for f in sphere)) - {(0, 2)}
    order = [0, 3, 2, 6, 1, 4, 5, 7, 8, 9, 10, 11]
    ie = sorted(edge(order.index(a), order.index(b)) for a, b in ie)
    ir, iw = graph_extensions(12, ie, 4)
    assert rows < ir and ir - rows == expand([(0, 1, 2, 3)])
    return {"edges": sorted(EDGES), "inner_faces": FACES, "rotation": rot,
            "four_port_relation": relation(rows), "paper_lift_templates": LIFTS,
            "edge_only_orbit_lifts": {word(r): word(w) for r, w in sorted(ws.items())},
            "degrees": [len(s) for s in ns], "spoke_subdivision": SPOKES,
            "inverse_obstructions": obstructions, "degree_screen_positive_controls": controls,
            "five_port_control": {"old_relation": relation(old5), "new_relation": relation(new5),
                "old_only": "01213", "new_only": "01011"},
            "missing_edge_control": {"deleted_edge": [4, 6], "edges": broken,
                "relation": relation(bad), "rainbow_lift": word(bw[(0, 1, 2, 3)])},
            "rejected_candidate": {"name": "pentagonal_belt_caps_minus_one_edge", "edges": ie,
                "relation": relation(ir), "excess": relation(ir - rows), "rainbow_lift": word(iw[(0, 1, 2, 3)])}}


def replace_star(graph, frames, owners, centre, rim, side):
    n = len(graph["vertices"])
    mapping = list(rim) + [centre, *range(n, n + 8)]
    es = set(map(tuple, graph["edges"]))
    assert neighbours(n, es)[centre] == set(rim) and cycle_edges(rim) <= es
    for rec in frames:
        if rec["available"]:
            faces, _ = trace_faces(dict(enumerate(rec["rotation"])), es)
            star = [f for f in faces if centre in f]
            assert len(star) == 4 and {frozenset(f) for f in star} == {
                frozenset((centre, rim[i], rim[(i + 1) % 4])) for i in range(4)}
            forward = any(same_orientation((centre, rim[0], rim[1]), f) for f in star)
            added = [tuple(mapping[v] for v in f) for f in FACES]
            if not forward:
                added = [f[::-1] for f in added]
            rec["rotation"] = rotation_from_faces(n + 8, [f for f in faces if centre not in f] + added)
        else:
            spokes = {rim[i]: [mapping[v] for v in p] for i, p in enumerate(SPOKES)}
            for j, old in enumerate(rec["alternating_paths"]):
                new = [old[0]]
                for a, b in zip(old, old[1:]):
                    segment = (spokes[b] if a == centre else spokes[a][::-1] if b == centre else [a, b])
                    new.extend(segment[1:])
                rec["alternating_paths"][j] = new
    graph["vertices"].extend(f"{side}_cap{v}" for v in range(n, n + 8))
    graph["edges"] = [list(e) for e in sorted(
        (es - {edge(centre, v) for v in rim}) | {edge(mapping[a], mapping[b]) for a, b in EDGES})]
    owners.update({v: side for v in range(n, n + 8)})
    return {"centre": centre, "rim": list(rim), "vertex_map": mapping, "owner": side}


def construct(baseline, depths):
    graph, frames = deepcopy(baseline["graph"]), deepcopy(baseline["frame_certificates"])
    owners = {v: "A" if v < 13 else "B" for v in range(8, 15)}
    steps = []
    for side, centre, rim, depth in (("A", 8, (10, 2, 12, 0), depths[0]),
                                     ("B", 13, (7, 6, 14, 5), depths[1])):
        for _ in range(depth):
            step = replace_star(graph, frames, owners, centre, rim, side)
            steps.append(step)
            rim = tuple(step["vertex_map"][i] for i in (0, 11, 6, 9))
    return graph, frames, owners, steps


def verify_structure(graph, frames, owners, steps, orientation):
    n = len(graph["vertices"])
    assert graph["vertices"][:15] == CORE_NAMES and len(set(graph["vertices"])) == n
    es = set(map(tuple, graph["edges"]))
    assert len(es) == len(graph["edges"]) and all(0 <= a < b < n for a, b in es)
    assert set(owners) == set(range(8, n)), "complete ownership"
    assert set(owners.values()) == {"A", "B"}
    assert all(owners[v] == ("A" if v < 13 else "B") for v in range(8, 15))
    s, t = endpoints(orientation)
    boundaries = {"A": (0, 1, 2, 3, 4), "B": (5, s, 6, t, 7)}
    private = {side: sorted(v for v in owners if owners[v] == side) for side in boundaries}
    vs = {side: set(boundaries[side]) | set(private[side]) for side in boundaries}
    assert all(any({a, b} <= vertices for vertices in vs.values()) for a, b in es), "source ownership"
    remaining, compressed = set(range(n)), set(es)
    template_ns = neighbours(13, EDGES)
    for step in reversed(steps):
        centre, rim, mapping, side = (step[k] for k in ("centre", "rim", "vertex_map", "owner"))
        assert len(mapping) == len(set(mapping)) == 13 and set(mapping) <= remaining, "cap vertex map"
        assert mapping[:4] == rim and mapping[4] == centre, "ordered cap ports"
        assert all(owners.get(v) == side for v in mapping[4:]), "cap ownership"
        assert cycle_edges(rim) <= compressed, "complete rim"
        ns = neighbours(n, compressed)
        for i, v in enumerate(mapping[4:], 4):
            assert ns[v] == {mapping[w] for w in template_ns[i]}, "complete cap attachments"
        internal = set(mapping[4:])
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


def lift(row, orientation, graph, steps):
    full = list(core_lift(row, orientation))
    for step in steps:
        colours = tuple(full[v] for v in step["rim"])
        canonical = word(normalize(colours))
        seen = list(dict.fromkeys(colours))
        perm = seen + sorted(set(range(4)) - set(seen))
        tail = [perm[int(c)] for c in LIFTS[canonical]]
        assert step["vertex_map"][5:] == list(range(len(full), len(full) + 8))
        full[step["centre"]] = tail[0]
        full.extend(tail[1:])
    assert tuple(full[:8]) == row and len(full) == len(graph["vertices"])
    assert all(full[a] != full[b] for a, b in graph["edges"])
    return tuple(full)


def audit(baseline, depths, order):
    orientation = baseline["orientation"]
    graph, frames, owners, steps = construct(baseline, depths)
    private, boundaries = verify_structure(graph, frames, owners, steps, orientation)
    reduction = no_clique_patch(graph, private, boundaries)
    obstructions = verify_obstructions(graph, owners)
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
            "owners": {str(v): s for v, s in sorted(owners.items())}, "cap_replacements": steps,
            "source_relations": {s: data[1] for s, data in sources.items()},
            "previous_reductions": reduction, "local_inverse_obstructions": obstructions,
            "boundary_fixed_old_core_embeddings": embeddings, "frame_certificates": frames,
            "J": relation(joint), "P": relation(pullback), "difference": relation(delta),
            "roles": baseline["roles"], "all_inclusion_minimal_repairs": repairs,
            "arity_residual_orbits": residual, "r_star": 4, "sparse_witness_lifts": sparse,
            "constructive_full_lifts_checked": len(full_lifts),
            "constructive_full_lifts_sha256": sha256(json.dumps(full_lifts).encode()).hexdigest()}


def guards(baseline):
    graph, frames, owners, steps = construct(baseline, (1, 1))
    mapping = steps[0]["vertex_map"]
    cases = []
    bad = deepcopy(graph)
    bad["edges"].remove(list(edge(mapping[4], mapping[6])))
    cases.append(("missing_cap_edge", bad, frames, owners, steps))
    bad = deepcopy(graph)
    bad["edges"].append(list(edge(4, mapping[5])))
    cases.append(("extra_private_attachment", bad, frames, owners, steps))
    bad = deepcopy(graph)
    bad["edges"].append(list(edge(mapping[5], steps[1]["vertex_map"][5])))
    cases.append(("cross_source_edge", bad, frames, owners, steps))
    cases.append(("missing_owner", graph, frames, {v: s for v, s in owners.items() if v != mapping[5]}, steps))
    bad = deepcopy(frames)
    next(r for r in bad if r["available"])["rotation"][0].pop()
    cases.append(("invalid_rotation", graph, bad, owners, steps))
    cases.append(("missing_candidate_frame", graph, frames[1:], owners, steps))
    bad = deepcopy(steps)
    bad[0]["vertex_map"][0], bad[0]["vertex_map"][1] = bad[0]["vertex_map"][1], bad[0]["vertex_map"][0]
    cases.append(("wrong_ordered_ports", graph, frames, owners, bad))
    bad = deepcopy(steps)
    bad[0]["vertex_map"][5] = bad[0]["vertex_map"][6]
    cases.append(("identified_private_vertices", graph, frames, owners, bad))
    result = []
    for name, g, fs, own, recipe in cases:
        try:
            verify_structure(g, fs, own, recipe, baseline["orientation"])
        except AssertionError as error:
            result.append({"name": name, "rejected": True, "guard": str(error)})
        else:
            raise AssertionError(f"accepted bad cap: {name}")
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
    records = [audit(b, ds, order) for b in baselines for ds in ((1, 0), (0, 1), (1, 1), (2, 2))]
    controls = [dict(c, orientation=b["orientation"]) for b in baselines for c in guards(b)]
    paths = [SOURCE, join_path, "scripts/c5_two_vertex_repair_caps.py",
             "scripts/c5_two_vertex_repair_fans.py", "scripts/c5_two_vertex_repair_rings.py",
             "scripts/c5_two_vertex_repair_strips.py", "scripts/c5_two_vertex_repair_patches.py",
             "scripts/c5_two_vertex_repair_sources.py", "scripts/c5_two_vertex_common_repair.py",
             "scripts/c5_two_vertex_repair_transport.py", "scripts/c5_two_vertex_join.py",
             "scripts/c5_two_vertex_join_topology.py", "scripts/boundary_relations.py"]
    return {"schema": "c5-common-repair-asymmetric-four-port-cap-v1",
            "scope": "Exact D13 four-port disk and arbitrary-depth paper family with no clique, whole-source path, ring, or even-fan inverse start; not rewrite completeness or Lean.",
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
