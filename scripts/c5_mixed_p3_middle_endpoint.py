#!/usr/bin/env python3
"""Mixed P3 with a middle contact and an end contact: C5 source exclusion.

Keep the unrooted leaf and all three of its actual frame attachments. The
four-block annulus is a necessary geometric relaxation, not a replacement
coloring interface or a disk realization. No target queries or Lean claims.
"""

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import c5_mixed_capacity_contacts as capacity

base = capacity.base
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_mixed_p3_middle_endpoint/observations.json"
U, Q = capacity.U, base.Q
MASKS = (0, 1, 2)
NAMES = ("z_side", "x1_with_original_x0", "x2", "w_side")
RHO, PI = (3, 2, 1, 0, 4), (1, 0, 2, 3)
PERMS = tuple(permutations(range(4)))


def seen(support):
    return frozenset(Q[i] for i in support)


def key(value):
    return json.dumps(value, sort_keys=True)


def triple_mask(triples):
    return sum(1 << (16*a + 4*b + c) for a, b, c in triples)


def witness(support, residual):
    return next((p for p in PERMS if all(p[c] == c for c in seen(support))
                 and {p[c] for c in residual} != set(residual)), None)


def interface(supports, masks=MASKS):
    lists = [U - seen(s) for s in supports]
    triples = tuple(t for t in product(*map(sorted, lists))
                    if t[0] != t[1] and t[1] != t[2])
    pz = tuple(i for i, m in enumerate(masks) if m & 1)
    pw = tuple(i for i, m in enumerate(masks) if m & 2)
    F = capacity.forbidden(triples, pz, pw)
    attachments = {7+i: supports[i] + ((base.Z,) if masks[i] & 1 else ())
                   + ((base.W,) if masks[i] & 2 else ()) for i in range(3)}
    region = base.make_region("P3_middle_endpoint", [(7, 8), (8, 9)], attachments)
    R, ports, full = base.joint_interface(region, Q)
    contacts = frozenset(tuple(t[v-7] for v in ports) for t in triples)
    assert set(full) == contacts and base.PAIRS - R == F
    for a, b in sorted(base.PAIRS):
        coloring = base.first_coloring(tuple(range(10)), region["edges"],
            dict(enumerate(Q)) | {base.Z: a, base.W: b})
        assert (coloring is None) == ((a, b) in F)
    return lists, triples, F


def local_audit():
    sides = [capacity.encode_side(s) for s in capacity.necessary_sides(1)]
    side_ids = {key(s): i for i, s in enumerate(sides)}
    records, cases, roles, color_roles = [], [], {}, set()
    for supports in product(combinations(range(5), 3),
                            combinations(range(5), 1), combinations(range(5), 2)):
        lists, triples, F = interface(supports)
        joins = capacity.minimal_side_joins(F, 1, 1)
        record = dict(id=len(records), actual_supports=supports,
            vertex_tuple_mask=triple_mask(triples),
            contact_tuple_mask=base.mask({(t[1], t[2]) for t in triples}),
            forbidden_pair_mask=base.mask(F))
        records.append(record)
        if not F:
            assert not joins
            continue
        assert joins and len(F) == 1
        a, b = next(iter(F))
        assert b == 3 and a != 3
        c = Q[supports[1][0]]
        d, = U - {a, c, 3}
        assert {a, c, d} == {0, 1, 2}
        assert lists == [frozenset({3}), U - {c}, frozenset({d, 3})]
        assert triples == tuple(sorted(((3, a, d), (3, a, 3), (3, d, 3))))
        color_roles.add((a, c, d))
        record.update(a=a, c=c, d=d)
        for branch, Ez, Ew, expected in (
                ("used_z_singleton", {a}, {a, 3}, 85),
                ("unused_w_singleton", {a, 3}, {3}, 115)):
            selected = [j for j in joins if set(j["z"]["residual"]) == Ez
                        and set(j["w"]["residual"]) == Ew]
            assert len(selected) == expected
            role_key = f"{a}:{branch}"
            encoded = [(side_ids[key(j["z"])], side_ids[key(j["w"])]) for j in selected]
            if role_key in roles:
                assert roles[role_key] == encoded
            roles[role_key] = encoded
            cases.append(dict(id=len(cases), local_id=record["id"], branch=branch,
                role_key=role_key, z_residual=sorted(Ez), w_residual=sorted(Ew)))
        assert len(joins) == 200

    by_support = {r["actual_supports"]: r for r in records}
    symmetry = []
    for record in records:
        if not record["forbidden_pair_mask"]:
            continue
        supports = record["actual_supports"]
        triples = tuple(t for t in product(range(4), repeat=3)
                        if record["vertex_tuple_mask"] & (1 << (16*t[0]+4*t[1]+t[2])))
        reflected = by_support[tuple(tuple(sorted(RHO[i] for i in s)) for s in supports)]
        assert reflected["vertex_tuple_mask"] == triple_mask(
            tuple(PI[c] for c in t) for t in triples)
        assert reflected["forbidden_pair_mask"] == base.mask({(PI[record["a"]], 3)})
        record["reflected_local_id"] = reflected["id"]
        for swap, reverse in ((True, False), (False, True), (True, True)):
            masks = tuple(((m & 1) << 1) | ((m & 2) >> 1) for m in MASKS) if swap else MASKS
            other_supports = tuple(reversed(supports)) if reverse else supports
            if reverse:
                masks = tuple(reversed(masks))
            _, transformed, F = interface(other_supports, masks)
            assert set(transformed) == {tuple(reversed(t)) if reverse else t for t in triples}
            assert F == ({(3, record["a"])} if swap else {(record["a"], 3)})
            transformed_joins = {key(j) for j in capacity.minimal_side_joins(F, 1, 1)}
            for j in capacity.minimal_side_joins(frozenset({(record["a"], 3)}), 1, 1):
                expected = dict(z=j["w"], w=j["z"]) if swap else j
                assert key(expected) in transformed_joins
            symmetry.append(dict(local_id=record["id"], root_swap=swap, path_reverse=reverse,
                root_masks=masks, vertex_tuple_mask=triple_mask(transformed),
                forbidden_pair_mask=base.mask(F)))
    assert len(records) == 500 and len(cases) == 224 and len(color_roles) == 6
    assert len(symmetry) == 336
    assert sum(len(roles[c["role_key"]]) for c in cases) == 22400
    return dict(root_masks=MASKS, configurations=records, cases=cases, side_roles=sides,
        joins_by_role_key=roles, color_roles=sorted(color_roles), symmetries=symmetry,
        independent_pin_queries=16*(len(records)+len(symmetry)))


def compositions(total, n):
    if n == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first, n-1):
                yield (first,) + rest


def support_offsets(length, position):
    choices = ((0,),) if length == 0 else tuple(
        (0,) + tuple(sorted(s)) + (length,) for s in capacity.subsets(range(1, length)))
    return tuple(s for s in choices if (position != 1 or len(s) in (3, 4))
                 and (position != 2 or len(s) == 2))


def lift_geometries():
    """Four connected original blocks, allowing zero spans at either root."""
    found = {}
    for extra in range(3):
        for excess in compositions(extra, 4):
            lengths = tuple(x+y for x, y in zip((0, 2, 1, 0), excess))
            for gaps in compositions(5-sum(lengths), 4):
                options = [support_offsets(n, i) for i, n in enumerate(lengths)]
                for offsets in product(*options):
                    for anchor, direction in product(range(5), (1, -1)):
                        cursor, lifts = anchor, []
                        for i, support in enumerate(offsets):
                            lifts.append(tuple(cursor + direction*j for j in support))
                            cursor += direction*(lengths[i]+gaps[i])
                        supports = tuple(tuple(sorted(v % 5 for v in s)) for s in lifts)
                        found.setdefault(supports, dict(anchor=anchor, direction=direction,
                            lengths=lengths, gaps=gaps, lifts=lifts, supports=supports))
    return [dict(id=i, **g) for i, (_, g) in enumerate(sorted(found.items()))]


def independent_hulls():
    """Choose actual subsets first, then test their lifted cyclic hulls."""
    choices = []
    for support in capacity.subsets(range(5)):
        if not support:
            continue
        for start in sorted(support):
            length = max((v-start) % 5 for v in support)
            choices.append((tuple(sorted(support)), start, length))
    found = set()

    def visit(items):
        if len(items) == 4:
            supports = tuple(s for s, _, _ in items)
            found.add(supports)
            found.add(tuple(tuple(sorted((-v) % 5 for v in s)) for s in supports))
            return
        position = len(items)
        for support, start, length in choices:
            if position == 1 and len(support) not in (3, 4):
                continue
            if position == 2 and len(support) != 2:
                continue
            if items:
                anchor = items[0][1]
                start = anchor + (start-anchor) % 5
                # A point at the final end can coincide with the first point.
                if start < items[-1][1] + items[-1][2]:
                    start += 5
                if start + length > anchor + 5:
                    continue
            visit(items + ((support, start, length),))

    visit(())
    return found


def geometry_audit(local):
    geometries = lift_geometries()
    assert len(geometries) == 570
    assert {g["supports"] for g in geometries} == independent_hulls()
    lookup = defaultdict(list)
    for g in geometries:
        lookup[g["supports"][1:3]].append(g)
    records, counts, role_counts = [], Counter(), Counter()
    for case in local["cases"]:
        r = local["configurations"][case["local_id"]]
        S0, S1, S2 = r["actual_supports"]
        matches = []
        for g in lookup[(tuple(sorted(set(S0) | set(S1))), S2)]:
            bad = {name: p for name, p in (
                ("z", witness(g["supports"][0], case["z_residual"])),
                ("w", witness(g["supports"][3], case["w_residual"]))) if p is not None}
            assert bad, (case, g)
            matches.append(dict(geometry_id=g["id"], side_stabilizer_witnesses=bad))
        reason = "side_residual_stabilizer" if matches else "original_square_order"
        records.append(dict(case_id=case["id"], reason=reason, matches=matches))
        counts[reason] += 1
        role_counts[reason] += len(local["joins_by_role_key"][case["role_key"]])
    assert counts == {"original_square_order": 44, "side_residual_stabilizer": 180}
    assert role_counts == {"original_square_order": 4400, "side_residual_stabilizer": 18000}
    assert sum(len(r["matches"]) for r in records) == 1032
    case_ids = {(c["local_id"], c["branch"]): c["id"] for c in local["cases"]}
    for case, record in zip(local["cases"], records):
        reflected_id = local["configurations"][case["local_id"]]["reflected_local_id"]
        other = records[case_ids[reflected_id, case["branch"]]]
        assert record["reason"] == other["reason"]
        assert len(record["matches"]) == len(other["matches"])
    return dict(named_blocks=NAMES,
        scope="necessary relaxation; retains S0 and S1 separately in local data; "
              "does not impose the internal order of the original x0 star and x1 spoke",
        ordered_geometries=geometries, exclusions=records,
        case_counts=dict(counts), role_counts=dict(role_counts),
        compatible_geometries=sum(len(r["matches"]) for r in records),
        retained=0, target_queries=0)


def paper_controls():
    stabilizers = []
    for support in capacity.subsets(range(5)):
        colors = seen(support)
        for a in range(3):
            for residual in ({a}, {a, 3}, {3}):
                bad = witness(support, residual)
                required = ({a} if residual == {a} else
                            U - {a, 3} if residual == {a, 3} else {0, 1, 2})
                assert (bad is None) == (required <= colors)
                stabilizers.append(dict(support=sorted(support), residual=sorted(residual),
                    required_seen=sorted(required), witness=bad))
    # Direct word controls for the two paths in the used-singleton proof.
    # a,c,d are 0,1,2 here. The start of S2 is either a or c.
    shortest = {}
    for start in (0, 1):
        prefix, suffix = [], []
        for n in range(1, 6):
            for word in product(range(3), repeat=n):
                if word[0] == 0 and word[-1] == start and set(word) == {0, 1, 2}:
                    prefix.append(word)
                if word[0] != start or word[-1] != 0:
                    continue
                # End of S2 is the other of a,c; the subsequent w support sees c,d.
                if any(word[j] == 1-start and {1, 2} <= set(word[j:])
                       for j in range(1, len(word))):
                    suffix.append(word)
        p = min(prefix, key=lambda w: (len(w), w))
        s = min(suffix, key=lambda w: (len(w), w))
        assert (len(p)-1, len(s)-1) == ((3, 3) if start == 0 else (2, 4))
        shortest[str(start)] = dict(prefix=p, suffix=s, total_edges=len(p)+len(s)-2)
    colors = (0, 1, 2, 0, 1, 2)
    supports = ((1, 2, 3), (1,), (3, 4))
    lists = [U - {colors[v] for v in s} for s in supports]
    triples = tuple(t for t in product(*map(sorted, lists)) if t[0] != t[1] != t[2])
    assert capacity.forbidden(triples, (1,), (2,)) == {(0, 3)}
    blocks = ((0,), (1, 2, 3), (3, 4), (4, 5))
    assert all(colors[i] != colors[(i+1) % 6] for i in range(6))
    assert set(blocks[1]) == set(supports[0]) | set(supports[1])
    assert colors[blocks[0][0]] == 0 and {colors[i] for i in blocks[3]} == {1, 2}
    assert all(max(blocks[i]) <= min(blocks[i+1]) for i in range(3))
    return dict(stabilizers=stabilizers, shortest_words=shortest, six_edge_control=dict(
        scope="necessary support/color control only; not a degree/minimality source graph",
        boundary_colors=colors, actual_mixed_supports=supports, ordered_blocks=blocks,
        complete_triples=triples, forbidden_pair_mask=base.mask({(0, 3)}),
        z_residual=[0], w_residual=[0, 3], z_side_span=0, perimeter=6))


def build():
    local = local_audit()
    return dict(schema=1,
        scope="C5 disk-source exclusion: sole mixed P3 with middle/end contacts, "
              "all source residuals and whole root/path symmetries; arbitrary unary size; "
              "no T4, external degree-list theorem, target, full Sigma, or Lean claim",
        local=local, geometry=geometry_audit(local), paper_controls=paper_controls(),
        scripts_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
            for p in (Path(__file__).resolve(), Path(capacity.__file__).resolve(),
                      Path(base.__file__).resolve())})


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
    print(json.dumps(dict(actual_support_triples=len(data["local"]["configurations"]),
        residual_cases=len(data["local"]["cases"]), support_role_joins=22400,
        independent_pin_queries=data["local"]["independent_pin_queries"],
        ordered_geometries=len(data["geometry"]["ordered_geometries"]),
        case_exclusions=data["geometry"]["case_counts"],
        role_exclusions=data["geometry"]["role_counts"],
        compatible_geometries=data["geometry"]["compatible_geometries"],
        retained=0, target_queries=0, artifact_bytes=len(raw)), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
