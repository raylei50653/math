#!/usr/bin/env python3
"""Common-endpoint original P3: double-fan source restrictions and residuals.

The coloring interface keeps all three original vertices. Whole root-side
support is used only for necessary geometry. Arbitrary unary size belongs to
the paper argument; rotation controls realize geometry, not minimal sources.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import c5_mixed_capacity_contacts as capacity

base = capacity.base
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_mixed_p3_common_endpoint/observations.json"
ROTATIONS = ROOT / "artifacts/c5_mixed_p3_common_endpoint/rotation_controls.json"
U, Q = capacity.U, base.Q
MASKS = (0, 0, 3)
ORDERS = ((2, 0, 1), (2, 1, 0), (0, 1, 2), (1, 0, 2))
NAMES = ("A_z", "A_w", "S2")
PERMS = tuple(permutations(range(4)))
SUPPORTS = tuple(tuple(sorted(s)) for s in capacity.subsets(range(5)) if s)
RHO, PI = (3, 2, 1, 0, 4), (1, 0, 2, 3)


def seen(support):
    return frozenset(Q[i] for i in support)


def tuple_mask(triples):
    return sum(1 << (16*a + 4*b + c) for a, b, c in triples)


def key(value):
    return json.dumps(value, sort_keys=True)


def interface(supports, masks=MASKS):
    lists = [U - seen(s) for s in supports]
    triples = tuple(t for t in product(*map(sorted, lists))
                    if t[0] != t[1] and t[1] != t[2])
    pz = tuple(i for i, m in enumerate(masks) if m & 1)
    pw = tuple(i for i, m in enumerate(masks) if m & 2)
    F = capacity.forbidden(triples, pz, pw)
    attachments = {7+i: supports[i] + ((base.Z,) if masks[i] & 1 else ())
                   + ((base.W,) if masks[i] & 2 else ()) for i in range(3)}
    region = base.make_region("original_common_endpoint_P3", [(7, 8), (8, 9)], attachments)
    R, ports, full = base.joint_interface(region, Q)
    assert set(full) == {tuple(t[v-7] for v in ports) for t in triples}
    assert base.PAIRS - R == F
    for a, b in sorted(base.PAIRS):
        coloring = base.first_coloring(tuple(range(10)), region["edges"],
            dict(enumerate(Q)) | {base.Z: a, base.W: b})
        assert (coloring is None) == ((a, b) in F)
    return lists, triples, F


def local_audit():
    sides = [capacity.encode_side(s) for s in capacity.necessary_sides(1)]
    side_ids = {key(s): i for i, s in enumerate(sides)}
    records, cases, joins_by_a, roles = [], [], {}, set()
    for supports in product(combinations(range(5), 3),
                            combinations(range(5), 2), combinations(range(5), 1)):
        lists, triples, F = interface(supports)
        record = dict(id=len(records), actual_supports=supports,
            lists=[sorted(L) for L in lists], complete_triples=triples,
            vertex_tuple_mask=tuple_mask(triples), forbidden_pair_mask=base.mask(F))
        records.append(record)
        if not F:
            assert not capacity.minimal_side_joins(F, 1, 1)
            continue
        d = triples[0][1]
        c, = seen(supports[2])
        a, = U - {c, d, 3}
        assert {a, c, d} == {0, 1, 2}
        assert lists == [{3}, {d, 3}, U - {c}]
        assert triples == ((3, d, a), (3, d, 3))
        assert F == {(a, 3), (3, a)}
        record.update(a=a, c=c, d=d)
        roles.add((a, c, d))
        joins = capacity.minimal_side_joins(F, 1, 1)
        encoded = [(side_ids[key(j["z"])], side_ids[key(j["w"])]) for j in joins]
        assert len(encoded) == 125
        if str(a) in joins_by_a:
            assert joins_by_a[str(a)] == encoded
        joins_by_a[str(a)] = encoded
        expected = (((a, 3), (a, 3)), ((a,), (a, 3)), ((3,), (a, 3)),
                    ((a, 3), (a,)), ((a, 3), (3,)))
        for branch, (Ez, Ew) in enumerate(expected):
            ids = [i for i, j in enumerate(joins)
                   if tuple(j["z"]["residual"]) == Ez and tuple(j["w"]["residual"]) == Ew]
            assert len(ids) == 25
            cases.append(dict(id=len(cases), name=f"CPP-{record['id']:03d}-{branch}",
                local_id=record["id"], branch=branch, z_residual=Ez, w_residual=Ew,
                side_join_ids=ids))
    assert len(records) == 500 and len(cases) == 560 and len(roles) == 6

    # Reuse the six saved color configurations, without importing exclusion flags.
    prior = json.loads(capacity.OUT.read_bytes())["three_vertices"]["color_cases"]
    six = [r for r in prior if r["shape"] == "P3" and tuple(r["root_masks"]) == MASKS
           and r["forbidden_pair_mask"]]
    assert len(six) == 6
    reused_roles = set()
    for r in six:
        colors = tuple(map(frozenset, r["boundary_colors"]))
        d, = U - colors[1] - {3}
        c, = colors[2]
        a, = U - {c, d, 3}
        assert (a, c, d) in roles
        reused_roles.add((a, c, d))
        assert r["complete_vertex_tuple_mask"] == tuple_mask(((3, d, a), (3, d, 3)))
        assert r["forbidden_pair_mask"] == base.mask({(a, 3), (3, a)})
        assert r["minimal_role_joins"] == 125
    assert reused_roles == roles

    lookup = {r["actual_supports"]: r for r in records}
    symmetries = []
    for r in records:
        if not r["forbidden_pair_mask"]:
            continue
        reflected = lookup[tuple(tuple(sorted(RHO[v] for v in s)) for s in r["actual_supports"])]
        assert reflected["vertex_tuple_mask"] == tuple_mask(
            tuple(PI[x] for x in t) for t in r["complete_triples"])
        r["reflected_local_id"] = reflected["id"]
        for swap, reverse in ((True, False), (False, True), (True, True)):
            supports = tuple(reversed(r["actual_supports"])) if reverse else r["actual_supports"]
            masks = tuple(reversed(MASKS)) if reverse else MASKS
            _, ts, F = interface(supports, masks)
            assert set(ts) == {tuple(reversed(t)) if reverse else t for t in r["complete_triples"]}
            assert F == {(r["a"], 3), (3, r["a"])}
            join_set = {key(j) for j in capacity.minimal_side_joins(F, 1, 1)}
            for j in capacity.minimal_side_joins(F, 1, 1):
                assert key(dict(z=j["w"], w=j["z"]) if swap else j) in join_set
            symmetries.append(dict(local_id=r["id"], root_swap=swap, path_reverse=reverse,
                root_masks=masks, vertex_tuple_mask=tuple_mask(ts), forbidden_pair_mask=base.mask(F)))
    return dict(root_masks=MASKS, configurations=records, cases=cases, side_roles=sides,
        joins_by_a=joins_by_a, reused_color_configurations=six, color_roles=sorted(roles),
        symmetries=symmetries, independent_pin_queries=16*(len(records)+len(symmetries)))


def stabilizer_witness(support, residual):
    return next((p for p in PERMS if all(p[c] == c for c in seen(support))
                 and {p[c] for c in residual} != set(residual)), None)


def fan_sectors(supports):
    S0, S1, S2 = supports
    out = []
    for h in S0:
        end = h + min((v-h) % 5 for v in S0 if v != h)
        T1 = tuple(sorted(h + (v-h) % 5 for v in S1))
        s = h + (S2[0]-h) % 5
        if max(T1) > end or s > end:
            continue
        for child, (left, right) in enumerate(zip((h,) + T1, T1 + (end,))):
            if left <= s <= right:
                out.append(dict(anchor=h, I=(h, end), S1_lifts=T1,
                    child=child, J=(left, right), S2_lift=s))
    return out


def order_witness(sector, Az, Aw):
    h = sector["anchor"]
    blocks = tuple(tuple(sorted(h + (v-h) % 5 for v in s))
                   for s in (Az, Aw, (sector["S2_lift"] % 5,)))
    left, right = sector["J"]
    if any(min(t) < left or max(t) > right for t in blocks):
        return None
    for order in ORDERS:
        if all(max(blocks[i]) <= min(blocks[j]) for i, j in zip(order, order[1:])):
            return dict(block_lifts=blocks, named_order=[NAMES[i] for i in order])
    return None


def geometry_audit(local):
    exclusions, retained, counts = [], [], Counter()
    for case in local["cases"]:
        r = local["configurations"][case["local_id"]]
        sectors = fan_sectors(r["actual_supports"])
        choices = [[s for s in SUPPORTS if stabilizer_witness(s, E) is None]
                   for E in (case["z_residual"], case["w_residual"])]
        counts["side_support_candidates"] += len(choices[0])*len(choices[1])
        matches = []
        for Az, Aw in product(*choices):
            for sector in sectors:
                order = order_witness(sector, Az, Aw)
                if order is None:
                    continue
                geometry = dict(id=len(retained), case_id=case["id"],
                    case_name=case["name"], local_id=r["id"], actual_side_supports=(Az, Aw),
                    **sector, **order)
                retained.append(geometry)
                matches.append(geometry["id"])
                break
        reason = "retained_necessary_geometry" if matches else "double_fan_tether_stabilizer"
        exclusions.append(dict(case_id=case["id"], reason=reason, geometry_ids=matches))
        counts[reason] += 1
        if r["d"] == 2:
            assert not matches
        if r["c"] == 2 and matches:
            assert case["branch"] in (1, 3)
            for gid in matches:
                g = retained[gid]
                word = tuple(Q[v % 5] for v in range(g["J"][0], g["J"][1]+1))
                positions = tuple(range(g["J"][0], g["J"][1]+1))
                if word[0] == 2:
                    word = tuple(reversed(word))
                    positions = tuple(reversed(positions))
                assert word in ((r["a"], r["d"], 2), (r["a"], r["d"], r["a"], 2))
                singleton = g["actual_side_supports"][0 if case["branch"] == 1 else 1]
                assert seen(singleton) <= {r["a"], r["d"]} and r["a"] in seen(singleton)
                assert positions[0] % 5 in singleton
                assert set(singleton) <= {v % 5 for v in positions[:2]}
    assert len(retained) == 140
    assert counts == {"side_support_candidates": 114048,
        "retained_necessary_geometry": 36, "double_fan_tether_stabilizer": 524}
    cases = {c["id"]: c for c in local["cases"]}
    def signature(g):
        c = cases[g["case_id"]]
        return (g["local_id"], tuple(c["z_residual"]), tuple(c["w_residual"]),
                *g["actual_side_supports"])
    signatures = {signature(g) for g in retained}
    for g in retained:
        c = cases[g["case_id"]]
        assert (g["local_id"], tuple(c["w_residual"]), tuple(c["z_residual"]),
                *reversed(g["actual_side_supports"])) in signatures
        reflected_id = local["configurations"][g["local_id"]]["reflected_local_id"]
        assert (reflected_id, tuple(sorted(PI[x] for x in c["z_residual"])),
                tuple(sorted(PI[x] for x in c["w_residual"])),
                *(tuple(sorted(RHO[v] for v in s)) for s in g["actual_side_supports"])) in signatures
    by_branch = Counter(cases[g["case_id"]]["branch"] for g in retained)
    assert by_branch == {0: 20, 1: 58, 2: 2, 3: 58, 4: 2}
    return dict(scope="necessary geometry only; whole-side supports do not replace unary relations",
        allowed_linear_orders=[[NAMES[i] for i in order] for order in ORDERS],
        case_counts=dict(counts), retained_geometries=retained, case_results=exclusions,
        retained_by_branch=dict(by_branch), retained_cases=36, retained_local_configurations=18,
        retained_side_role_joins=36*25, target_queries=0)


def skeleton_edges(supports, side_supports):
    edges = set(base.CYCLE) | {(5, 6), (5, 9), (6, 9), (7, 8), (8, 9)}
    for v, support in zip((7, 8, 9, 5, 6), (*supports, *side_supports)):
        edges.update(tuple(sorted((v, b))) for b in support)
    return edges


def rotation_faces(rotation, edges):
    rotation = {int(v): tuple(ns) for v, ns in rotation.items()}
    for v in range(10):
        neighbors = {b if a == v else a for a, b in edges if v in (a, b)}
        assert len(rotation[v]) == len(set(rotation[v])) and set(rotation[v]) == neighbors
    assert base.is_connected(tuple(range(10)), edges)
    darts = {(a, b) for e in edges for a, b in (e, tuple(reversed(e)))}
    used, faces = set(), []
    for start in sorted(darts):
        if start in used:
            continue
        dart, face = start, []
        while dart not in used:
            used.add(dart)
            a, b = dart
            face.append(a)
            ns = rotation[b]
            dart = (b, ns[(ns.index(a)-1) % len(ns)])
        assert dart == start
        faces.append(tuple(face))
    assert used == darts and 10 - len(edges) + len(faces) == 2
    assert any(len(f) == 5 and set(f) == set(range(5)) for f in faces)
    assert any(len(f) == 3 and set(f) == {5, 6, 9} for f in faces)
    return faces


def rotation_audit(local, geometry):
    data = json.loads(ROTATIONS.read_bytes())
    cases = {c["id"]: c for c in local["cases"]}
    expected = set()
    for g in geometry["retained_geometries"]:
        c = cases[g["case_id"]]
        expected.add((g["local_id"], tuple(c["z_residual"]), tuple(c["w_residual"]),
                      *g["actual_side_supports"]))
    actual, controls = set(), []
    for r in data["records"]:
        supports, sides = tuple(map(tuple, r["supports"])), tuple(map(tuple, r["side_supports"]))
        local_record = local["configurations"][r["local_id"]]
        assert supports == local_record["actual_supports"]
        sig = (r["local_id"], tuple(r["Ez"]), tuple(r["Ew"]), *sides)
        assert sig in expected and sig not in actual
        actual.add(sig)
        edges = skeleton_edges(supports, sides)
        faces = rotation_faces(r["rotation"], edges)
        controls.append(dict(local_id=r["local_id"], z_residual=r["Ez"], w_residual=r["Ew"],
            side_supports=sides, vertices=10, edges=len(edges), faces=faces,
            root_degrees=[sum(v in e for e in edges) for v in (5, 6)]))
    assert actual == expected
    return dict(scope="140 positive disk geometry controls; unary contracted only for geometry; "
        "not source degree/minimality realizations or coloring replacements",
        controls=controls, rotation_input_sha256=sha256(ROTATIONS.read_bytes()).hexdigest())


def build():
    local = local_audit()
    geometry = geometry_audit(local)
    g = geometry["retained_geometries"][30]
    c = local["cases"][g["case_id"]]
    r = local["configurations"][g["local_id"]]
    z_id, w_id = local["joins_by_a"]["1"][20]
    assert c["name"] == "CPP-134-1" and 20 in c["side_join_ids"]
    assert g["actual_side_supports"] == ((1,), (2, 4)) and g["J"] == (1, 4)
    assert (z_id, w_id) == (8, 1)
    assert local["side_roles"][z_id]["unary_forbidden"] == [[0, 2, 3]]
    assert local["side_roles"][w_id]["unary_forbidden"] == [[0, 2]]
    next_entry = dict(case_name=c["name"], geometry_id=30, side_join_id=20,
        actual_supports=r["actual_supports"], complete_triples=r["complete_triples"],
        actual_side_supports=g["actual_side_supports"], J=g["J"], side_ids=(z_id, w_id),
        z_role=local["side_roles"][z_id], w_role=local["side_roles"][w_id],
        preserved_original_external_path=(5, 9, 4),
        scope="named necessary candidate; own unary supports and source realization unresolved")
    return dict(schema=1,
        scope="original common-endpoint P3; arbitrary-unary double-fan paper lemma, "
              "d=2 source exclusion and c=2 source restriction; 36 necessary residual cases; "
              "no target, T4, full Sigma, general exit or Lean claim",
        local=local, geometry=geometry, topology_controls=rotation_audit(local, geometry),
        next_entry=next_entry,
        scripts_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
            for p in (Path(__file__).resolve(), Path(capacity.__file__).resolve(), Path(base.__file__).resolve())})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode()
    if args.check:
        assert OUT.read_bytes() == raw, f"stale artifact: {OUT}"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(raw)
    print(json.dumps(dict(actual_support_triples=500, nonempty_forbidden=112,
        reused_color_roles=6, residual_cases=560, necessary_side_role_joins=14000,
        independent_pin_queries=data["local"]["independent_pin_queries"],
        **data["geometry"]["case_counts"], retained_geometries=140,
        retained_local_configurations=18, retained_side_role_joins=900,
        target_queries=0, rotation_controls=len(data["topology_controls"]["controls"]),
        artifact_bytes=len(raw)), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
