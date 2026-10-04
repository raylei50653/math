#!/usr/bin/env python3
"""Necessary singleton-unary schedules in one literal C5 color frame.

Assuming deletion of the original unary U accepts every boundary row and the
complete source rejects the listed rows, its complete one-contact relation must
be the singleton recorded here.  The controls enforce support-local S4
equivariance and the paper single-contact unused-color conservation theorem.
They do not classify mixed components, project their ternary relation, or test
graph realizability. The connected main checker owns the fresh named face domain.
"""
import argparse
from itertools import permutations, product
import json

from c5_independent_support_capacity import B, ROWS, U

PERMUTATIONS = tuple(permutations(range(4)))


def rejected_rows(sigma):
    # D5 moves transport the complete mask as well as the literal rows, so the
    # main checker's covariance audit also supplies noncanonical mask images.
    assert 0 <= sigma <= 1023
    result = [(i, q) for i, q in enumerate(ROWS) if not sigma >> i & 1]
    assert all(set(q) == {0, 1, 2} for _, q in result)
    return result


def singleton_schedules(sigma, a_spokes, support):
    """Return every literal candidate schedule, with explicit rejection evidence.

    `support` is the exact boundary support of the same original U.  A support
    envelope must be expanded into all its subsets by the caller.  Candidate
    domains exclude the original a-spoke colors; no mixed-coordinate marginal
    or independently normalized component is used.  Degenerate same-color
    spokes may leave three candidates, which this conservative API retains.
    """
    a_spokes, support = tuple(sorted(a_spokes)), tuple(sorted(support))
    assert len(a_spokes) == 2 and len(set(a_spokes)) == 2
    assert set(a_spokes) <= B and set(support) <= B
    rs = rejected_rows(sigma)
    domains = [sorted(U - {q[h] for h in a_spokes}) for _, q in rs]
    # Keep every matching permutation, including same-row stabilizers.
    constraints = [(qi, pi, perm) for qi, (_, q) in enumerate(rs)
                   for pi, (_, p) in enumerate(rs) for perm in PERMUTATIONS
                   if all(perm[q[h]] == p[h] for h in support)]
    records = []
    for schedule in product(*domains):
        equivariance = None
        for qi, pi, perm in constraints:
            if perm[schedule[qi]] != schedule[pi]:
                qidx, q = rs[qi]
                pidx, p = rs[pi]
                equivariance = dict(source_row_index=qidx, source_literal_boundary=q,
                    target_row_index=pidx, target_literal_boundary=p,
                    actual_support=support,
                    source_support_colors=[q[h] for h in support],
                    target_support_colors=[p[h] for h in support],
                    literal_color_permutation=perm,
                    source_singleton_color=schedule[qi],
                    permuted_source_singleton_color=perm[schedule[qi]],
                    target_singleton_color=schedule[pi],
                    same_row_stabilizer=qi == pi)
                break
        conservation = None
        if 3 in schedule and any(d != 3 for d in schedule):
            qi = next(j for j, d in enumerate(schedule) if d == 3)
            pi = next(j for j, d in enumerate(schedule) if d != 3)
            qidx, q = rs[qi]
            pidx, p = rs[pi]
            conservation = dict(fixed_unused_color=3,
                row_forbidding_fixed_color=dict(row_index=qidx, literal_boundary=q,
                    complete_R_U=[(schedule[qi],)]),
                row_forbidding_other_color=dict(row_index=pidx, literal_boundary=p,
                    complete_R_U=[(schedule[pi],)]),
                actual_support=support,
                fixed_color_absent_on_both_entire_boundaries=True,
                singleton_contact_block_palette_conservation_required=True)
        records.append(dict(singleton_colors=schedule,
            complete_singleton_unary_relations=[dict(row_index=ri, literal_boundary=q,
                contact_order=['u'], complete_R_U=[(d,)])
                for (ri, q), d in zip(rs, schedule, strict=True)],
            support_S4_equivariant=equivariance is None,
            first_S4_conflict=equivariance,
            fixed_unused_3_conserved=conservation is None,
            fixed_unused_3_conflict=conservation,
            survives_both_necessary_controls=equivariance is None and conservation is None))
    survivors = [r for r in records if r['survives_both_necessary_controls']]
    return dict(source_sigma=sigma, original_a_spokes=a_spokes,
        actual_original_U_support=support,
        literal_rejected_rows=[dict(row_index=ri, literal_boundary=q)
            for ri, q in rs],
        candidate_singleton_domains=domains,
        support_matching_S4_constraints=len(constraints),
        same_row_stabilizer_constraints=sum(qi == pi for qi, pi, _ in constraints),
        all_candidate_schedules=records, surviving_schedules=survivors,
        counts=dict(candidates=len(records),
            S4_equivariant=sum(r['support_S4_equivariant'] for r in records),
            fixed_unused_3_conserved=sum(r['fixed_unused_3_conserved'] for r in records),
            surviving=len(survivors)),
        scope='Necessary complete-singleton unary schedules, conditional on the '
              'original U-deleted graph accepting all rows; no mixed classification '
              'or graph realizability claim')


def canonical_conflicts():
    # The common three-row subsystem makes the 941 conservation contradiction
    # explicit and also supplies a necessary contradiction for Sigma 933.
    common = [(ROWS.index(q), q) for q in
              ((0, 1, 0, 2, 1), (0, 1, 2, 0, 2), (0, 1, 2, 1, 2))]
    support, spokes = (0, 3, 4), (0, 1)
    domains = [sorted(U - {q[h] for h in spokes}) for _, q in common]
    constraints = [(qi, pi, perm) for qi, (_, q) in enumerate(common)
                   for pi, (_, p) in enumerate(common) for perm in PERMUTATIONS
                   if all(perm[q[h]] == p[h] for h in support)]
    equivariant = [f for f in product(*domains)
        if all(perm[f[qi]] == f[pi] for qi, pi, perm in constraints)]
    assert equivariant == [(3, 2, 3)]
    stabilizer = (0, 3, 2, 1)  # Fix 0,2, exchange 1,3 at row 01202.
    exchange = (0, 2, 1, 3)    # 01212 support 0,1,2 -> 01021 support 0,2,1.
    assert all(stabilizer[common[1][1][h]] == common[1][1][h] for h in support)
    assert stabilizer[3] != 3 and stabilizer[2] == 2
    assert all(exchange[common[2][1][h]] == common[0][1][h] for h in support)
    return dict(original_a=5, original_b=6, original_a_spokes=spokes,
        original_b_spokes=(2, 3), actual_original_U_support=support,
        common_literal_rejected_rows=[dict(row_index=i, literal_boundary=q)
            for i, q in common],
        row_01202_forced_singleton_2=dict(row_index=common[1][0],
            literal_boundary=common[1][1], candidates=[2, 3],
            literal_stabilizer=stabilizer, excluded_candidate=3),
        rows_01212_01021_forced_singleton_3=dict(
            source_row_index=common[2][0], source_literal_boundary=common[2][1],
            target_row_index=common[0][0], target_literal_boundary=common[0][1],
            literal_color_permutation=exchange,
            candidate_2_maps_to_color_1_forbidden_by_original_a_spoke=True,
            only_equivariant_pair_of_singletons=[3, 3]),
        only_common_three_row_equivariant_schedule=equivariant[0],
        fixed_unused_3_conservation_conflict=True,
        controls=[singleton_schedules(sigma, spokes, actual)
            for sigma, actual in product((933, 941), ((0, 3), (0, 3, 4)))],
        scope='Same original U, exact support, and literal color permutations; '
              'the singleton premise is a separate paper/source reduction')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
        help='Recompute the canonical algebra controls without a stored artifact')
    parser.parse_args()
    canonical = canonical_conflicts()
    assert all(c['counts']['surviving'] == 0 for c in canonical['controls'])
    print(json.dumps(dict(canonical_original_a_spokes=[0, 1],
        canonical_original_b_spokes=[2, 3],
        common_three_row_equivariant_schedule=
            canonical['only_common_three_row_equivariant_schedule'],
        fixed_unused_3_conservation_conflict=True,
        controls=[dict(source_sigma=c['source_sigma'],
            actual_original_U_support=c['actual_original_U_support'], counts=c['counts'])
            for c in canonical['controls']]), ensure_ascii=False))


if __name__ == '__main__':
    main()
