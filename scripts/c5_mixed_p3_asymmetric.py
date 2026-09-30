#!/usr/bin/env python3
"""Opposite-end mixed P3: asymmetric root residuals have no C5 disk source.

Paper proof allows arbitrary original unary components and zero singleton-side
span. These finite controls retain actual supports and complete relations;
they are neither source realization nor target acceptance certificates.
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
OUT = ROOT / "artifacts/c5_mixed_p3_asymmetric/observations.json"
U = frozenset(range(4))
Q = base.Q
NAMES = ("z_side", "x0", "x1", "x2", "w_side")
PERMS = tuple(permutations(range(4)))
RHO, PI = (3, 2, 1, 0, 4), (1, 0, 2, 3)


def seen(support):
    return frozenset(Q[i] for i in support)


def witness(support, residual):
    return next((p for p in PERMS if all(p[c] == c for c in seen(support))
                 and {p[c] for c in residual} != set(residual)), None)


def side_key(side):
    return json.dumps(side, sort_keys=True)


def local_audit():
    sides = [capacity.encode_side(s) for s in capacity.necessary_sides(1)]
    side_ids = {side_key(s): i for i, s in enumerate(sides)}
    local, cases, roles = [], [], {}
    for supports in product(combinations(range(5), 2), repeat=3):
        lists = [U - seen(s) for s in supports]
        triples = tuple(t for t in product(*map(sorted, lists))
                        if t[0] != t[1] and t[1] != t[2])
        contacts = frozenset((t[0], t[2]) for t in triples)
        F = capacity.forbidden(triples, (0,), (2,))
        region = base.make_region("P3", [(7, 8), (8, 9)], {
            7: (base.Z,) + supports[0], 8: supports[1],
            9: (base.W,) + supports[2]})
        R, ports, full = base.joint_interface(region, Q)
        assert ports == (7, 9) and set(full) == contacts
        assert base.PAIRS - R == F
        for a, b in sorted(base.PAIRS):
            coloring = base.first_coloring(tuple(range(10)), region["edges"],
                dict(enumerate(Q)) | {base.Z: a, base.W: b})
            assert (coloring is None) == ((a, b) in F)
        local_id = len(local)
        local.append(dict(id=local_id, actual_supports=supports,
            vertex_tuple_mask=sum(1 << (16*a + 4*b + c) for a, b, c in triples),
            contact_tuple_mask=base.mask(contacts), forbidden_pair_mask=base.mask(F)))
        joins = capacity.minimal_side_joins(F, 1, 1)
        for a, b in sorted(base.PAIRS):
            if a == b or (a, b) not in F or (a, a) in F:
                continue
            # Exact P3 rejection; all original lists contain unused color 3.
            residual = (lists[0] - {a}, lists[1], lists[2] - {b})
            assert len(residual[0]) == len(residual[2]) == 1
            assert residual[0] != residual[2]
            assert residual[1] == residual[0] | residual[2]
            assert all(len(L) == 2 for L in lists) and 3 in (a, b)
            if b == 3:
                assert lists[0] == {a, 3} and lists[1] == lists[2]
            key = f"{a},{b}:{base.mask(F)}"
            selected = [j for j in joins if j["z"]["residual"] == [a]
                        and j["w"]["residual"] == sorted((a, b))]
            assert selected
            encoded = [(side_ids[side_key(j["z"])], side_ids[side_key(j["w"])])
                       for j in selected]
            if key in roles:
                assert roles[key] == encoded
            roles[key] = encoded
            cases.append(dict(id=len(cases), local_id=local_id, a=a, b=b,
                role_key=key, paper_branch="unused_singleton" if a == 3 else "used_singleton"))

    by_support = {tuple(r["actual_supports"]): r for r in local}
    case_ids = {(c["local_id"], c["a"], c["b"]): c["id"] for c in cases}
    for case in cases:
        record = local[case["local_id"]]
        supports = record["actual_supports"]
        reflected = tuple(tuple(sorted(RHO[i] for i in s)) for s in supports)
        other = by_support[reflected]
        case["reflected_case_id"] = case_ids[other["id"], PI[case["a"]], PI[case["b"]]]
        old_triples = [t for t in product(range(4), repeat=3)
                       if record["vertex_tuple_mask"] & (1 << (16*t[0] + 4*t[1] + t[2]))]
        assert other["vertex_tuple_mask"] == sum(
            1 << (16*PI[a] + 4*PI[b] + PI[c]) for a, b, c in old_triples)
        swapped = by_support[tuple(reversed(supports))]
        assert swapped["vertex_tuple_mask"] == sum(
            1 << (16*c + 4*b + a) for a, b, c in old_triples)
        transposed_F = frozenset((b, a) for a, b in base.PAIRS
                                if record["forbidden_pair_mask"] & (1 << (4*a+b)))
        assert swapped["forbidden_pair_mask"] == base.mask(transposed_F)
        swapped_joins = {side_key(j) for j in capacity.minimal_side_joins(transposed_F, 1, 1)}
        for left, right in roles[case["role_key"]]:
            assert side_key(dict(z=sides[right], w=sides[left])) in swapped_joins
        case["root_swapped_local_id"] = swapped["id"]

    assert len(local) == 1000 and len(cases) == 384
    counts = Counter(c["paper_branch"] for c in cases)
    assert counts == {"unused_singleton": 192, "used_singleton": 192}
    assert sum(len(roles[c["role_key"]]) for c in cases) == 26400
    return dict(configurations=local, normalized_cases=cases, side_roles=sides,
                joins_by_role_key=roles, normalized_branch_counts=dict(counts),
                independent_pin_queries=16000,
                swapped_case_semantics="reverse x0,x1,x2; transpose complete F; swap entire z/w side roles")


def lift_geometries():
    """All common lifts, allowing a point support at the singleton root."""
    geometries = {}
    for lengths in product(range(3), repeat=5):
        if any(lengths[i] < 1 for i in (1, 2, 3, 4)) or sum(lengths) > 5:
            continue
        for gaps in product(range(2), repeat=5):
            if sum(lengths) + sum(gaps) != 5:
                continue
            for anchor, direction in product(range(5), (1, -1)):
                cursor, options = anchor, []
                for i, length in enumerate(lengths):
                    choices = [(cursor,)] if length == 0 else [(cursor, cursor + direction*length)]
                    if length == 2 and i in (0, 4):
                        choices.append((cursor, cursor + direction, cursor + 2*direction))
                    options.append(choices)
                    cursor += direction * (length + gaps[i])
                for lifts in product(*options):
                    supports = tuple(tuple(sorted(v % 5 for v in s)) for s in lifts)
                    geometries.setdefault(supports, dict(anchor=anchor, direction=direction,
                        lengths=lengths, gaps=gaps, lifts=lifts, supports=supports))
    return [dict(id=i, **g) for i, (_, g) in enumerate(sorted(geometries.items()))]


def independent_hulls():
    """Build cyclic hulls from actual subsets, independently of span/gap tuples."""
    choices = []
    for size in range(1, 6):
        for support in combinations(range(5), size):
            for start in support:
                length = max((v-start) % 5 for v in support)
                mask = sum(1 << ((start+j) % 5) for j in range(length))
                choices.append((support, start, length, mask))
    found = set()

    def visit(items, used):
        if len(items) == 5:
            anchor = items[0][1]
            intervals = [((s-anchor) % 5, (s-anchor) % 5 + n) for _, s, n, _ in items]
            if all(intervals[i][1] <= intervals[i+1][0] for i in range(4)) \
                    and intervals[-1][1] <= 5:
                supports = tuple(item[0] for item in items)
                found.add(supports)
                found.add(tuple(tuple(sorted((-v) % 5 for v in s)) for s in supports))
            return
        for choice in choices:
            if len(items) and choice[2] == 0:
                continue
            if len(items) in (1, 2, 3) and len(choice[0]) != 2:
                continue
            if not used & choice[3]:
                visit(items + (choice,), used | choice[3])

    visit((), 0)
    return found


def geometry_audit(local):
    geometries = lift_geometries()
    assert len(geometries) == 110
    assert {g["supports"] for g in geometries} == independent_hulls()
    records, counts, role_counts = [], Counter(), Counter()
    for case in local["normalized_cases"]:
        supports = local["configurations"][case["local_id"]]["actual_supports"]
        matches = []
        for g in geometries:
            if g["supports"][1:4] != supports:
                continue
            a, b = case["a"], case["b"]
            bad = {name: p for name, p in (
                ("z", witness(g["supports"][0], {a})),
                ("w", witness(g["supports"][4], {a, b}))) if p is not None}
            assert bad
            matches.append(dict(geometry_id=g["id"], side_stabilizer_witnesses=bad))
        reason = "side_residual_stabilizer" if matches else "original_pentagon_order"
        records.append(dict(case_id=case["id"], matches=matches, reason=reason))
        counts[reason] += 1
        role_counts[reason] += len(local["joins_by_role_key"][case["role_key"]])
    assert counts == {"original_pentagon_order": 340, "side_residual_stabilizer": 44}
    assert sum(len(r["matches"]) for r in records) == 84
    for case, record in zip(local["normalized_cases"], records):
        reflected = records[case["reflected_case_id"]]
        assert record["reason"] == reflected["reason"]
        assert len(record["matches"]) == len(reflected["matches"])
    return dict(named_units=NAMES, ordered_geometries=geometries, exclusions=records,
                normalized_case_counts=dict(counts), normalized_role_counts=dict(role_counts),
                retained=0, target_queries=0)


def support_lemma_audit():
    checks = 0
    for support in capacity.subsets(range(5)):
        colors = seen(support)
        for a in range(4):
            if witness(support, {a}) is None:
                assert (colors == {0, 1, 2}) if a == 3 else (a in colors)
            checks += 1
        for a in range(3):
            if witness(support, {a, 3}) is None:
                assert U - {a, 3} <= colors
            checks += 1
    assert checks == 224
    # Nonvacuous sharpness control for the support budget, not a source graph.
    colors = (0, 1, 2, 1, 2, 1)
    supports = ((0,), (1, 2), (2, 3), (3, 4), (4, 5))
    palettes = [U - {colors[v] for v in s} for s in supports[1:4]]
    triples = tuple(t for t in product(*map(sorted, palettes)) if t[0] != t[1] != t[2])
    F = capacity.forbidden(triples, (0,), (2,))
    assert (0, 3) in F and (0, 0) not in F
    assert colors[0] == 0 and {colors[v] for v in supports[4]} == {1, 2}
    assert 1 + sum(max(s)-min(s) for s in supports[1:4]) + 2 == 6
    return dict(stabilizer_checks=checks, six_edge_control=dict(
        scope="necessary support/color control only; no degree/minimality realization",
        boundary_colors=colors, supports=supports, complete_triples=triples,
        forbidden_pair_mask=base.mask(F), singleton_side_span=0,
        point_to_x0_cost=1, three_mixed_spans=3, w_side_to_point_cost=2, perimeter=6))


def build():
    local = local_audit()
    return dict(schema=1,
        scope="C5 disk-source exclusion for sole mixed P3 with opposite-end contacts, "
              "asymmetric residuals (1,2) and full root swap; arbitrary unary size; "
              "no T4, external degree-list theorem, target, full Sigma, or Lean claim",
        local=local, geometry=geometry_audit(local), support_lemmas=support_lemma_audit(),
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
    print(json.dumps(dict(actual_P3_support_triples=1000, independent_pin_queries=16000,
        normalized_asymmetric_cases=384, normalized_support_role_joins=26400,
        ordered_geometries=110, support_role_exclusions=data["geometry"]["normalized_role_counts"],
        root_swap_verified=True, retained=0, target_queries=0, artifact_bytes=len(raw)),
        sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
