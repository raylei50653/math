#!/usr/bin/env python3
"""Sealed clique patches beyond private degree-three elimination.

The arbitrary-size and embedded-core statements are paper proofs. This replay
checks exact graph attachments, one colouring certificate, full rotations,
independent edge-only relations, and the existing common repair hypotheses.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_two_vertex_common_repair import verify_hypotheses
from c5_two_vertex_join import expand, graph_extensions
from c5_two_vertex_join_topology import components, trace_faces
from c5_two_vertex_repair_sources import (
    CORE_NAMES, TABLE, core_edges, core_lift, edge, endpoints,
)
from c5_two_vertex_repair_transport import (
    DOMAIN, check_hashes, cycle_edges, project, relation, verify_frame_proofs, word,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "artifacts/c5_two_vertex_overlap/repair_sources.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/repair_patches.json"


def rotation_from_faces(n, faces):
    predecessors = [{} for _ in range(n)]
    for face in faces:
        for i, v in enumerate(face):
            before, after = face[i - 1], face[(i + 1) % len(face)]
            assert before not in predecessors[v]
            predecessors[v][before] = after
    rotation = []
    for pred in predecessors:
        start = min(pred)
        ns, nxt = [start], pred[start]
        while nxt != start:
            assert nxt not in ns
            ns.append(nxt)
            nxt = pred[nxt]
        assert len(ns) == len(pred)
        rotation.append(list(reversed(ns)))
    return rotation


def patch_templates():
    faces_o = []
    for bits in product(range(2), repeat=3):
        a, b, c = [i + 3 * bits[i] for i in range(3)]
        faces_o.append((a, c, b) if sum(bits) % 2 else (a, b, c))
    faces_i = []
    for i in range(5):
        u, un = 1 + i, 1 + (i + 1) % 5
        v, vn, vp = 6 + i, 6 + (i + 1) % 5, 6 + (i - 1) % 5
        faces_i += [(0, u, un), (u, v, un), (u, vp, v), (11, vn, v)]
    result = {}
    for name, n, faces, colouring in (
        ("octahedron", 6, faces_o, "012012"),
        ("icosahedron", 12, faces_i, "012123303021"),
    ):
        edges = sorted(set().union(*(cycle_edges(f) for f in faces)))
        rotation = rotation_from_faces(n, faces)
        actual_faces, _ = trace_faces(dict(enumerate(rotation)), set(edges))
        assert n - len(edges) + len(actual_faces) == 2
        assert any(f == (0, 1, 2) for f in actual_faces)
        colours = tuple(map(int, colouring))
        assert all(colours[u] != colours[v] for u, v in edges)
        # Independent full attachment relation, not a sampled boundary row.
        local, _ = graph_extensions(n, edges, 3)
        assert local == set(permutations(range(4), 3))
        result[name] = {"vertices": list(range(n)), "edges": edges,
                        "rotation": rotation, "one_colouring": colouring,
                        "boundary": [0, 1, 2], "boundary_relation": relation(local),
                        "private_minimum_degree": min(sum(v in e for e in edges) for v in range(3, n))}
    return result


def same_orientation(a, b):
    return any(tuple(a) == tuple(b[i:] + b[:i]) for i in range(len(b)))


def insert_patch(graph, frames, owner, colouring, triangle, side, patch):
    """Replace a face by a certified triangular disk in every saved rotation."""
    old_n = len(graph["vertices"])
    mapping = list(triangle) + list(range(old_n, old_n + len(patch["vertices"]) - 3))
    old_edges = set(map(tuple, graph["edges"]))
    for record in frames:
        if not record["available"]:
            continue
        host = record["rotation"]
        faces, _ = trace_faces(dict(enumerate(host)), old_edges)
        target, = (f for f in faces if len(f) == 3 and set(f) == set(triangle))
        patch_rot = [[mapping[u] for u in ns] for ns in patch["rotation"]]
        # The patch exterior and the removed host face have opposite orientation.
        if same_orientation(target, list(triangle)):
            patch_rot = [list(reversed(ns)) for ns in patch_rot]
        for i, u in enumerate(target):
            before, after = target[i - 1], target[(i + 1) % 3]
            ns = patch_rot[mapping.index(u)]
            k = ns.index(after)
            ns = ns[k:] + ns[:k]
            assert ns[-1] == before
            assert host[u][(host[u].index(before) - 1) % len(host[u])] == after
            host[u][host[u].index(before):host[u].index(before)] = ns[1:-1]
        host.extend(patch_rot[3:])
    graph["vertices"].extend(f"{side}_patch{v}" for v in mapping[3:])
    graph["edges"] = [list(e) for e in sorted(old_edges | {
        edge(mapping[u], mapping[v]) for u, v in patch["edges"]})]
    owner.update({v: side for v in mapping[3:]})
    old = tuple(map(int, patch["one_colouring"]))
    perm = next(p for p in permutations(range(4))
                if all(p[old[i]] == colouring[mapping[i]] for i in range(3)))
    colouring.extend(perm[c] for c in old[3:])
    return {"side": side, "triangle": list(triangle), "local_to_global": mapping}


def verify_source(graph, orientation, owner, colouring, frames):
    """Structural certificate checker; reads no J, P, patch recipe or repairs."""
    n = len(graph["vertices"])
    assert graph["vertices"][:15] == CORE_NAMES
    assert len(set(graph["vertices"])) == n
    edges = set(map(tuple, graph["edges"]))
    assert len(edges) == len(graph["edges"]) and all(0 <= u < v < n for u, v in edges)
    assert {e for e in edges if e[1] < 15} == core_edges(orientation), "induced core"
    assert set(owner) == set(range(15, n)) and set(owner.values()) <= {"A", "B"}, "ownership domain"
    sides = {"A": set(range(5)) | set(range(8, 13)), "B": {0, 2, 5, 6, 7, 13, 14}}
    for v, side in owner.items():
        sides[side].add(v)
    assert all(any({u, v} <= vs for vs in sides.values()) for u, v in edges), "source ownership"
    adj = {v: set() for v in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    extra = set(range(15, n))
    blocks = []
    for comp in components({v: adj[v] & extra for v in extra}):
        attachment = set().union(*(adj[v] for v in comp)) - comp
        assert attachment <= set(range(15))
        assert 1 <= len(attachment) <= 3, "clique attachment size"
        assert all(edge(u, v) in edges for u, v in combinations(sorted(attachment), 2)), "attachment clique"
        blocks.append({"private_vertices": sorted(comp), "attachment": sorted(attachment),
                       "side": owner[min(comp)]})
    assert len(colouring) == n and all(c in range(4) for c in colouring), "one colouring domain"
    assert all(colouring[u] != colouring[v] for u, v in edges), "one proper colouring"
    verify_frame_proofs(frames, graph)
    s, t = endpoints(orientation)
    expected = {frozenset(cycle_edges(c)) for c in ((0, 4, 3, 2, 6), (s, 1, t, 7, 5))}
    assert {frozenset(cycle_edges(r["cycle"])) for r in frames if r["available"]} == expected
    for label, cycle in (("A", (0, 1, 2, 3, 4)), ("B", (5, s, 6, t, 7))):
        for record in frames:
            if not record["available"]:
                continue
            for vs in (sides[label], sides[label] & set(range(15))):
                es = {e for e in edges if set(e) <= vs}
                rot = {v: [u for u in record["rotation"][v] if u in vs] for v in vs}
                fs, _ = trace_faces(rot, es)
                assert len(vs) - len(es) + len(fs) == 2
                outer, = (f for f in fs if len(f) == 5 and cycle_edges(f) == cycle_edges(cycle))
                if vs <= set(range(15)):
                    assert all(len(f) == 3 for f in fs if f != outer), "triangulated source core"
                    assert len(fs) - 1 == (13 if label == "A" else 7)
    return blocks


def lift_by_blocks(core_colouring, colouring, graph, blocks):
    result = list(core_colouring) + [-1] * (len(graph["vertices"]) - 15)
    for block in blocks:
        attachment = block["attachment"]
        perm = next(p for p in permutations(range(4))
                    if all(p[colouring[v]] == result[v] for v in attachment))
        for v in block["private_vertices"]:
            result[v] = perm[colouring[v]]
    assert all(c in range(4) for c in result)
    assert all(result[u] != result[v] for u, v in graph["edges"])
    return tuple(result)


def edge_only_relation(graph):
    """Exhaust 4^8 rows using actual edges; core-first is only a search order."""
    n, edges = len(graph["vertices"]), graph["edges"]
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    port_edges = [(u, v) for u, v in edges if v < 8]
    colours = [-1] * n

    def solve():
        uncoloured = [v for v in range(8, n) if colours[v] < 0]
        if not uncoloured:
            return True
        candidates = [v for v in uncoloured if v < 15] or uncoloured
        domains = {v: sorted(set(range(4)) - {colours[u] for u in adj[v]}) for v in candidates}
        v = min(candidates, key=lambda u: (len(domains[u]), -len(adj[u]), u))
        for c in domains[v]:
            colours[v] = c
            ok = solve()
            colours[v] = -1
            if ok:
                return True
        return False

    result = set()
    for row in DOMAIN:
        if any(row[u] == row[v] for u, v in port_edges):
            continue
        colours[:8] = row
        if solve():
            result.add(row)
    return result


def audit(graph, orientation, owner, colouring, frames, baseline):
    blocks = verify_source(graph, orientation, owner, colouring, frames)
    joint = edge_only_relation(graph)
    assert joint == expand(tuple(map(int, w)) for w in baseline["J"]["patterns"])
    for row in joint:
        full = lift_by_blocks(core_lift(row, orientation), colouring, graph, blocks)
        assert full[:8] == row
    fs = [tuple(r["cycle"]) for r in frames if r["available"]]
    flocals = [{project(row, s) for row in joint} for s in fs]
    pullback = {row for row in DOMAIN if all(project(row, s) in r for s, r in zip(fs, flocals))}
    assert relation(pullback) == baseline["P"]
    delta = pullback - joint
    scopes = list(combinations(range(8), 4))
    local = [{project(row, s) for row in joint} for s in scopes]
    cuts = [{row for row in delta if project(row, s) not in r} for s, r in zip(scopes, local)]
    a, b, t = (baseline["roles"][k] for k in ("A", "B", "T"))
    es = baseline["roles"]["E"]
    witnesses = [tuple(map(int, w)) for w, _ in TABLE[orientation]]
    repairs = verify_hypotheses(delta, cuts, a, b, t, es, witnesses)
    assert [list(ids) for ids in repairs] == baseline["all_inclusion_minimal_repairs"]
    for ids in repairs:
        assert {q for q in pullback if all(project(q, scopes[i]) in local[i] for i in ids)} == joint
    sparse = []
    for (w, completions), rejected in zip(TABLE[orientation], ({a}, {b, t}, {b, *es})):
        witness = tuple(map(int, w))
        lifts = []
        differences = []
        for q in completions:
            row = tuple(map(int, q))
            full = lift_by_blocks(core_lift(row, orientation), colouring, graph, blocks)
            changed = {i for i in range(8) if row[i] != witness[i]}
            assert full[:8] == row and row in joint
            differences.append(changed)
            lifts.append({"U": q, "changed_ports": sorted(changed), "full_colouring": word(full)})
        assert {i for i, scope in enumerate(scopes)
                if not any(set(scope).isdisjoint(d) for d in differences)} == rejected
        assert all(any(set(scope).isdisjoint(d) for d in differences) for scope in fs)
        sparse.append({"witness": w, "exact_rejected_scope_ids": sorted(rejected), "completions": lifts})
    residual = []
    for arity in range(5):
        remaining = set(delta)
        for scope in combinations(range(8), arity):
            projected = {project(q, scope) for q in joint}
            remaining = {q for q in remaining if project(q, scope) in projected}
        residual.append(relation(remaining)["global_s4_orbits"])
    assert residual == [54, 54, 16, 16, 0]
    degrees = {v: sum(v in e for e in graph["edges"]) for v in range(15, len(graph["vertices"]))}
    assert min(degrees.values()) >= 4  # No first step in ANY core-preserving degree-three peel.
    return {"orientation": orientation, "graph": graph, "owners": {str(k): v for k, v in sorted(owner.items())},
            "one_full_colouring": word(colouring), "sealed_components": blocks,
            "frame_certificates": frames, "extra_vertex_degrees": {str(k): v for k, v in degrees.items()},
            "degree_three_peel_has_no_first_step": True, "J": relation(joint), "P": relation(pullback),
            "difference": relation(delta), "all_inclusion_minimal_repairs": repairs,
            "arity_residual_orbits": residual, "r_star": 4, "sparse_witness_lifts": sparse,
            "constructive_full_lifts_checked": len(joint)}


def guard_control(name, graph, orientation, owner, colouring, frames):
    try:
        verify_source(graph, orientation, owner, colouring, frames)
    except AssertionError as error:
        return {"name": name, "rejected": True, "guard": str(error)}
    raise AssertionError(f"accepted bad certificate: {name}")


def boundary_controls():
    # A planar graph with a nonclique two-point attachment and one colouring
    # forces the two contacts equal. A single arbitrary witness is insufficient.
    edges = sorted({edge(u, v) for u in (0, 1) for v in (2, 3, 4)} |
                   {edge(u, v) for u, v in combinations((2, 3, 4), 2)})
    rows, _ = graph_extensions(5, edges, 2)
    assert rows == {(c, c) for c in range(4)}
    # A proper C4 can use four colours; its central degree-four star then fails.
    wheel = sorted(cycle_edges((0, 1, 2, 3)) | {(i, 4) for i in range(4)})
    wheel_rows, _ = graph_extensions(5, wheel, 4)
    assert (0, 1, 0, 1) in wheel_rows and (0, 1, 2, 3) not in wheel_rows
    controls = [{"name": "nonclique_two_contact_patch", "edges": edges, "one_colouring": "00123",
             "attachment": [0, 1], "complete_relation": relation(rows), "rejected_attachment": "01"},
            {"name": "four_contact_disk_star", "edges": wheel, "one_colouring": "01012",
             "attachment": [0, 1, 2, 3], "complete_relation": relation(wheel_rows), "rejected_attachment": "0123"}]
    for control in controls:
        colouring = tuple(map(int, control["one_colouring"]))
        assert all(colouring[u] != colouring[v] for u, v in control["edges"])
    return controls


def build():
    saved = json.loads((ROOT / SOURCE).read_text())
    check_hashes(saved)
    templates = patch_templates()
    records, controls = [], []
    for baseline in saved["cases"]:
        if baseline["elimination"]:
            continue
        orientation = baseline["orientation"]
        for name, sequence in (("octahedral", ["octahedron"]),
                               ("icosahedral", ["icosahedron"]),
                               ("nested_icosahedral", ["icosahedron", "icosahedron"])):
            graph, frames = deepcopy(baseline["graph"]), deepcopy(baseline["frame_certificates"])
            owner, recipe = {}, []
            colouring = list(core_lift(tuple(map(int, baseline["J"]["patterns"][0])), orientation))
            for side, triangle in (("A", (0, 8, 10)), ("B", (6, 13, 14))):
                for kind in sequence:
                    step = insert_patch(graph, frames, owner, colouring, triangle, side, templates[kind])
                    step["template"] = kind
                    recipe.append(step)
                    mapping = step["local_to_global"]
                    # A genuine interior triangle of the icosahedral disk.
                    if kind == "icosahedron":
                        triangle = tuple(mapping[v] for v in (3, 7, 8))
            record = audit(graph, orientation, owner, colouring, frames, baseline)
            record.update(name=orientation + "_" + name, construction=recipe)
            records.append(record)
            if name != "octahedral":
                continue
            bad = deepcopy(graph)
            bad["edges"].remove([6, 7])
            controls.append(guard_control(orientation + "_missing_core_edge", bad, orientation, owner, colouring, frames))
            bad = deepcopy(graph)
            bad["edges"].append([15, 18])
            controls.append(guard_control(orientation + "_cross_source_edge", bad, orientation, owner, colouring, frames))
            bad = deepcopy(graph)
            bad["edges"].append([1, 15])
            controls.append(guard_control(orientation + "_unsealed_fourth_contact", bad, orientation, owner, colouring, frames))
            bad_colours = list(colouring)
            bad_colours[15] = bad_colours[16]
            controls.append(guard_control(orientation + "_bad_one_colouring", graph, orientation, owner, bad_colours, frames))
            bad_frames = deepcopy(frames)
            next(r for r in bad_frames if r["available"])["rotation"][0].pop()
            controls.append(guard_control(orientation + "_bad_frame_rotation", graph, orientation, owner, colouring, bad_frames))
            controls.append(guard_control(orientation + "_missing_owner", graph, orientation,
                                          {v: s for v, s in owner.items() if v != 15}, colouring, frames))
    paths = [SOURCE, "scripts/c5_two_vertex_repair_patches.py", "scripts/c5_two_vertex_repair_sources.py",
             "scripts/c5_two_vertex_common_repair.py", "scripts/c5_two_vertex_repair_transport.py",
             "scripts/c5_two_vertex_join.py", "scripts/c5_two_vertex_join_topology.py", "scripts/boundary_relations.py"]
    return {"schema": "c5-common-repair-sealed-patches-v1",
            "scope": "Paper arbitrary-size clique-patch theorem; six explicit nonpeelable planar controls. Not all source representatives or Lean.",
            "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "patch_templates": templates, "cases": records, "negative_controls": controls,
            "interface_counterexamples": boundary_controls(),
            "summary": {"nonpeelable_source_controls": len(records), "vertex_counts": [len(r["graph"]["vertices"]) for r in records],
                        "patch_boundary_assignments_checked": 48,
                        "full_lifts_checked": sum(r["constructive_full_lifts_checked"] for r in records),
                        "sparse_full_lifts": 11 * len(records), "negative_controls": len(controls),
                        "interface_counterexamples": 2, "new_lean_theorem": False}}


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
