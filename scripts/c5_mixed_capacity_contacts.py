#!/usr/bin/env python3
"""Finite controls for mixed capacity and the first three-vertex interfaces.

No disk/support catalogue, target separation, or graph realization theorem.
Complete tuples and original vertex identities are retained throughout.
"""

import argparse
from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_adjacent_degree5_interfaces as base

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_mixed_capacity_contacts/observations.json"
U = frozenset(range(4))
PAIRS = tuple(product(range(4), repeat=2))
PARTITIONS = {0: ((),), 1: ((1,),), 2: ((2,), (1, 1)),
              3: ((3,), (2, 1), (1, 1, 1))}


def subsets(xs):
    return tuple(frozenset(c) for n in range(len(xs) + 1)
                 for c in combinations(sorted(xs), n))


SETS = subsets(U)


def union(sets):
    return frozenset().union(*sets)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def forbidden(tuples, pz, pw):
    return frozenset((a, b) for a, b in PAIRS if not any(
        all(t[i] != a for i in pz) and all(t[i] != b for i in pw) for t in tuples))


def fiber_bounds(F, k, ell):
    return (all(sum((a, b) in F for a in U) <= k for b in U)
            and all(sum((a, b) in F for b in U) <= ell for a in U))


def join_ok(F, left, right):
    square = frozenset(product(left, right))
    return not (square - base.DELTA - F) and bool((square & base.DELTA) - F) \
        and bool(square - base.DELTA)


def side_audit():
    """All color-role candidates; no boundary placements or mixed realizations."""
    counts, forms = Counter(), Counter()
    for m in range(1, 5):
        for spokes in subsets({0, 1, 2}):
            t = len(spokes)
            if m + t > 4:
                continue
            for ports in PARTITIONS[4 - m - t]:
                choices = [[f for f in SETS if 0 < len(f) <= k] for k in ports]
                for fs in product(*choices):
                    counts["candidates"] += 1
                    if union(fs) & spokes:
                        continue
                    if any(not (f - union(fs[:i] + fs[i + 1:])) for i, f in enumerate(fs)):
                        continue
                    counts["spoke_and_private_pass"] += 1
                    overlap = sum(map(len, fs)) - len(union(fs))
                    assert overlap == 0  # at most three unary incidences
                    D = sum(k - len(f) for k, f in zip(ports, fs))
                    E = U - spokes - union(fs)
                    assert len(E) == m + D
                    if len(E) > m + 1:
                        continue
                    forms[m, t, ports, tuple(map(len, fs)), D] += 1
                    counts["capacity_pass"] += 1
    records = [dict(mixed_incidences=m, spokes=t, unary_contacts=ks,
                    forbidden_sizes=ss, deficit=d, residual_size=m+d, color_roles=n)
               for (m, t, ks, ss, d), n in sorted(forms.items())]
    assert len(records) == 18
    assert sum(r["deficit"] == 1 for r in records) == 4
    return dict(summary=dict(counts), forms=records)


@cache
def necessary_sides(m):
    result = []
    for spokes in subsets({0, 1, 2}):
        if m + len(spokes) > 4:
            continue
        for ports in PARTITIONS[4 - m - len(spokes)]:
            for fs in product(*[[f for f in SETS if 0 < len(f) <= k] for k in ports]):
                if union(fs) & spokes or sum(map(len, fs)) != len(union(fs)):
                    continue
                E = U - spokes - union(fs)
                if m <= len(E) <= m + 1:
                    result.append((spokes, ports, fs, E))
    return tuple(result)


def encode_side(side):
    spokes, ports, fs, E = side
    return dict(spoke_colors=sorted(spokes), unary_contacts=ports,
                unary_forbidden=[sorted(f) for f in fs], residual=sorted(E))


@cache
def minimal_side_joins(F, k, ell):
    """Full single-edge criteria on color-role data, not their realizability."""
    records = []
    for left, right in product(necessary_sides(k), necessary_sides(ell)):
        Ez, Ew = left[3], right[3]
        if not join_ok(F, Ez, Ew):
            continue
        if any(not (frozenset(product(released, Ew)) - base.DELTA - F)
               for released in left[2] + tuple(frozenset({c}) for c in sorted(left[0]))):
            continue
        if any(not (frozenset(product(Ez, released)) - base.DELTA - F)
               for released in right[2] + tuple(frozenset({c}) for c in sorted(right[0]))):
            continue
        records.append(dict(z=encode_side(left), w=encode_side(right)))
    return records


def fiber_budget_audit():
    """Exhaustive nonempty-component fibers within the root incidence budget."""
    counts = Counter()
    for m in range(1, 5):
        partitions = PARTITIONS.get(m, ((4,), (3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)))
        for ks in partitions:
            for fs in product(*[[f for f in SETS if len(f) <= k] for k in ks]):
                combined = union(fs)
                for E in SETS:
                    if len(E) < m:
                        continue
                    for b in U:
                        required = E - {b}
                        if not required <= combined:
                            continue
                        eps = len(E) - m
                        delta = sum(k - len(f) for k, f in zip(ks, fs))
                        overlap = sum(map(len, fs)) - len(combined)
                        leak = len(combined - required)
                        assert delta + overlap + leak == int(b in E) - eps
                        assert eps <= 1
                        if eps == 1:
                            assert b in E and delta == overlap == leak == 0
                        counts["covered_fibers"] += 1
    return dict(counts)


def two_contact_audit():
    counts, relations = Counter(), {}
    for bits in range(1, 1 << 16):
        ts = tuple(t for i, t in enumerate(PAIRS) if bits & (1 << i))
        F = forbidden(ts, (0,), (1,))
        counts["complete_tuple_sets"] += 1
        if not fiber_bounds(F, 1, 1):
            continue
        counts["fiber_bound_pass"] += 1
        counts[f"forbidden_size_{len(F)}"] += 1
        assert len(F) <= 2
        if len(F) == 2:
            (a, b), (c, d) = sorted(F)
            assert a != c and b != d
            assert set(ts) == {(a, d), (c, b)}
        relations[base.mask(F)] = F
    join_shapes = Counter()
    for F in relations.values():
        for left, right in product(SETS[1:], repeat=2):
            if not join_ok(F, left, right):
                continue
            assert len(left) <= 2 and len(right) <= 2
            assert (len(left), len(right)) in ((1, 2), (2, 1), (2, 2))
            if len(left) == len(right) == 2:
                assert left == right and F == frozenset(product(left, left)) - base.DELTA
            join_shapes[len(left), len(right)] += 1
    for T in SETS:
        if len(T) < 2:
            continue
        F = forbidden(tuple((x,) for x in sorted(T)), (0,), (0,))
        expected = frozenset(product(T, T)) - base.DELTA if len(T) == 2 else frozenset()
        assert F == expected
        counts["shared_contact_sets"] += 1
    # Same endpoint projections, different complete two-contact relation.
    equal = ((0, 0), (3, 3))
    cartesian = tuple(product((0, 3), repeat=2))
    assert forbidden(equal, (0,), (1,)) == {(0, 3), (3, 0)}
    assert not forbidden(cartesian, (0,), (1,))
    return dict(summary=dict(counts), distinct_forbidden_relations=len(relations),
                residual_shapes=[dict(sizes=s, count=n) for s, n in sorted(join_shapes.items())],
                marginal_negative_control=dict(tuples=equal, marginal_product=cartesian,
                                               lost_forbidden_pairs=[[0, 3], [3, 0]]))


def small_shape_formula(shape, lists, root_masks, a, b):
    residual = [L - ({a} if mask & 1 else set()) - ({b} if mask & 2 else set())
                for L, mask in zip(lists, root_masks)]
    if shape == "P3":
        return (len(residual[0]) == len(residual[2]) == 1
                and residual[0] != residual[2]
                and residual[1] == residual[0] | residual[2])
    return len(residual[0]) == 2 and residual[0] == residual[1] == residual[2]


def three_vertex_audit():
    summaries, transcript, color_cases, incidence_forms, witnesses = {}, [], [], [], {}
    for shape, edges, degrees in (("P3", ((0, 1), (1, 2)), (1, 2, 1)),
                                  ("K3", ((0, 1), (1, 2), (0, 2)), (2, 2, 2))):
        counts = Counter()
        for masks in product(range(4), repeat=3):
            pz = tuple(i for i, mask in enumerate(masks) if mask & 1)
            pw = tuple(i for i, mask in enumerate(masks) if mask & 2)
            if not pz or not pw:
                continue
            counts["named_incidence_patterns"] += 1
            bcounts = [4 - deg - mask.bit_count() for deg, mask in zip(degrees, masks)]
            options = [tuple(combinations(range(3), n)) for n in bcounts]
            local_count = joint_count = minimal_count = 0
            for boundary in product(*options):
                lists = [U - set(s) for s in boundary]
                tuples = tuple(t for t in product(*[sorted(L) for L in lists])
                               if all(t[i] != t[j] for i, j in edges))
                F = forbidden(tuples, pz, pw)
                assert fiber_bounds(F, len(pz), len(pw))
                expected = frozenset((a, b) for a, b in PAIRS
                                     if small_shape_formula(shape, lists, masks, a, b))
                assert F == expected
                counts["q_color_list_cases"] += 1
                counts["ordered_pair_checks"] += 16
                if F:
                    counts["nonempty_forbidden_cases"] += 1
                    local_count += 1
                joins = [(left, right) for left, right in product(SETS[1:], repeat=2)
                         if len(left) >= len(pz) and len(right) >= len(pw)
                         and join_ok(F, left, right)]
                # These are only coarse residual candidates, not full minimality.
                if joins:
                    joint_count += 1
                    counts["coarse_join_cases"] += 1
                    counts["coarse_residual_joins"] += len(joins)
                    key = shape + ":" + str((len(pz), len(pw)))
                    witnesses.setdefault(key, dict(shape=shape, root_masks=masks,
                        boundary_colors=boundary, contact_vertices=sorted(set(pz) | set(pw)),
                        complete_vertex_tuples=tuples, forbidden_pairs=sorted(F),
                        residuals=[sorted(s) for s in joins[0]]))
                minimal = minimal_side_joins(F, len(pz), len(pw))
                assert not minimal or joins
                if minimal:
                    minimal_count += 1
                    counts["minimal_role_color_cases"] += 1
                    counts["minimal_role_joins"] += len(minimal)
                    key = "minimal:" + shape + ":" + str((len(pz), len(pw)))
                    witnesses.setdefault(key, dict(shape=shape, root_masks=masks,
                        boundary_colors=boundary, contact_vertices=sorted(set(pz) | set(pw)),
                        complete_vertex_tuples=tuples, forbidden_pairs=sorted(F),
                        sides=minimal[0]))
                transcript.append([shape, masks, boundary, base.mask(F),
                                   [[sorted(a), sorted(b)] for a, b in joins], minimal])
                color_cases.append(dict(shape=shape, root_masks=masks, boundary_colors=boundary,
                    complete_vertex_tuple_mask=sum(1 << (16*x + 4*y + z) for x, y, z in tuples),
                    forbidden_pair_mask=base.mask(F), coarse_residual_joins=len(joins),
                    minimal_role_joins=len(minimal), minimal_role_sha256=digest(minimal)))
            incidence_forms.append(dict(shape=shape, root_masks=masks,
                contacts_z=pz, contacts_w=pw, boundary_counts=bcounts,
                nonempty_forbidden_color_cases=local_count, coarse_join_color_cases=joint_count,
                minimal_role_color_cases=minimal_count))
        assert counts["named_incidence_patterns"] == 49
        summaries[shape] = dict(counts)
    return dict(summary=summaries, incidence_forms=incidence_forms,
                witnesses=witnesses, color_cases=color_cases,
                color_case_transcript_sha256=digest(transcript))


def existing_region_audit():
    counts = Counter()
    for region in base.controls():
        k, ell = len(region["ports_z"]), len(region["ports_w"])
        if not k or not ell:
            continue
        counts["regions"] += 1
        for row in base.ROWS:
            R, _, _ = base.joint_interface(region, row)
            F = base.PAIRS - R
            assert fiber_bounds(F, k, ell)
            counts["row_interfaces"] += 1
            for a, b in PAIRS:
                fixed = dict(enumerate(row)) | {base.Z: a, base.W: b}
                actual = base.first_coloring(tuple(range(7)) + region["vertices"], region["edges"], fixed)
                assert (actual is None) == ((a, b) in F)
                counts["independent_pin_queries"] += 1
    return dict(counts)


def validate_k5(edges, groups):
    assert len(groups) == 5 and sum(map(len, groups)) == len(union(groups))
    assert all(base.is_connected(tuple(sorted(g)), edges) for g in groups)
    assert all(any(base.edge(u, v) in edges for u in A for v in B)
               for A, B in combinations(groups, 2))


def fixed_graph_audit():
    """Replace the old common singleton interface by an actual P3 region."""
    mixed = base.make_region("mixed_P3", [(7, 14), (14, 15)],
                             {7: (base.Z, 0, 1), 14: (0, 1), 15: (base.W, 0, 1)})
    left = base.make_region("z_triangle", [(8, 9), (8, 10), (9, 10)],
                            {8: (0, 1), 9: (base.Z, 0), 10: (base.Z, 0)})
    right = base.make_region("w_triangle", [(11, 12), (11, 13), (12, 13)],
                             {11: (0, 1), 12: (base.W, 1), 13: (base.W, 1)})
    regions = [mixed, left, right]
    edges = base.CYCLE | {base.edge(base.Z, base.W), base.edge(base.Z, 0), base.edge(base.W, 1)}
    edges |= union(r["edges"] for r in regions)
    vertices = tuple(range(16))
    assert [sum(v in e for e in edges) for v in vertices[5:]] == [5, 5] + [4] * 9
    assert not base.whole_pairs(vertices, edges, base.Q)
    deletions = []
    for e in sorted(edges - base.CYCLE):
        coloring = base.first_coloring(vertices, edges - {e}, dict(enumerate(base.Q)))
        assert coloring is not None and coloring[e[0]] == coloring[e[1]]
        deletions.append(dict(edge=e, coloring=[coloring[v] for v in vertices]))
    rows, canonical = [], []
    for row in base.ROWS:
        local = [base.joint_interface(r, row) for r in regions]
        relations = [r[0] for r in local]
        direct = base.whole_pairs(vertices, edges, row)
        assert direct == base.glued_pairs(regions, relations, edges, row, frozenset())
        T = U - {row[0], row[1]}
        assert relations[0] == base.PAIRS - (frozenset(product(T, T)) - base.DELTA)
        rows.append([row, base.mask(direct)])
        if row in base.CANONICAL:
            canonical.append(dict(row=row, root_pairs=sorted(direct), regions=[
                dict(name=r["name"], ports=ports, complete_tuples=sorted(witnesses),
                     forbidden_pairs=sorted(base.PAIRS - R))
                for r, (R, ports, witnesses) in zip(regions, local)]))
    groups = [{base.Z, 7, 1}, {8}, {9}, {10}, {0}]
    validate_k5(edges, groups)
    return dict(scope="actual minimal q-core; explicit K5, not a disk witness",
                vertices=vertices, edges=sorted(edges),
                regions=[dict(name=r["name"], vertices=r["vertices"], edges=sorted(r["edges"]),
                              contacts_z=r["ports_z"], contacts_w=r["ports_w"]) for r in regions],
                q_deletion_witnesses=deletions, canonical_rows=canonical,
                nonplanar_minor=[sorted(g) for g in groups],
                all_row_count=len(rows), all_rows_sha256=digest(rows))


def build():
    result = dict(schema=1,
        scope="paper mixed-capacity reduction with finite controls; no disk realization, "
              "new target separation, full Sigma, general exit, or Lean theorem",
        side_budget=side_audit(), fiber_budget=fiber_budget_audit(),
        two_contacts=two_contact_audit(), three_vertices=three_vertex_audit(),
        existing_regions=existing_region_audit(), fixed_graph=fixed_graph_audit())
    result["scripts_sha256"] = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
        for p in (Path(__file__).resolve(), Path(base.__file__).resolve())}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    raw = (json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        assert OUT.read_bytes() == raw, f"stale artifact: {OUT}"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(raw)
    print(json.dumps(dict(side_budget=data["side_budget"]["summary"],
        side_forms=len(data["side_budget"]["forms"]), fiber_budget=data["fiber_budget"],
        two_contacts=data["two_contacts"]["summary"], three_vertices=data["three_vertices"]["summary"],
        existing_regions=data["existing_regions"], fixed_graph_rows=data["fixed_graph"]["all_row_count"],
        deletion_witnesses=len(data["fixed_graph"]["q_deletion_witnesses"])), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
