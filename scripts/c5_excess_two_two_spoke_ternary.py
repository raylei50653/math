#!/usr/bin/env python3
"""Two spokes, original (3,1): reuse single-spoke singleton profiles.

The finite domain contains necessary same-source S4 profiles, never source
graphs. Complete ordered seven-port joins are checked independently.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS
from c5_excess_two_three_unary import orbit
from c5_excess_two_ternary_two_unary import profile_domain

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_two_spoke_ternary/observations.json'
U = set(range(4))


def source_controls():
    arcs = [(a, b) for a in range(6) for b in range(a + 2, 6)]
    target_masks = sorted(set(orbit(933) + orbit(941)))
    sectors, placements, used, totals = [], [], set(), Counter()
    digest, comparisons = sha256(), 0
    for second_spoke in range(1, 5):
        ordered = [(a, b) for a, b in product(arcs, repeat=2)
                   if a[1] <= b[0]
                   and not any(x < second_spoke < y for x, y in (a, b))]
        assert len(ordered) == (1, 3, 3, 1)[second_spoke - 1]
        sectors.append(dict(second_spoke_boundary_index=second_spoke,
            original_sector_intervals=[(0, second_spoke), (second_spoke, 5)],
            ordered_interval_pairs=ordered))
        for position, intervals in enumerate(ordered):
            for slots in permutations(range(2)):
                placed = tuple(intervals[k] for k in slots)
                used.update(placed)
                pools = [profile_domain(a)[0] for a in placed]
                histogram, witnesses, rejected_count_histogram = Counter(), {}, Counter()
                for indices in product(*(range(len(p)) for p in pools)):
                    profiles = [pool[i] for pool, i in zip(pools, indices)]
                    mask = sum(1 << ri for ri, row in enumerate(ROWS)
                        if len({row[0], row[second_spoke]}
                               | {f[ri] for f in profiles if f[ri] >= 0}) < 4)
                    assert mask not in target_masks, (second_spoke, placed, indices, mask)
                    histogram[mask] += 1
                    rejected_count_histogram[10 - mask.bit_count()] += 1
                    witnesses.setdefault(mask, indices)
                    digest.update(json.dumps([second_spoke, position, slots, indices, mask]).encode())
                    comparisons += 1
                placements.append(dict(second_spoke_boundary_index=second_spoke,
                    sector_catalog_pair=position, factor_slot_indices=slots,
                    factor_intervals=placed, profile_domain_sizes=list(map(len, pools)),
                    sigma_histogram=[dict(sigma=m, count=n, first_profile_indices=witnesses[m])
                                     for m, n in sorted(histogram.items())],
                    rejected_row_count_histogram=sorted(rejected_count_histogram.items())))
                totals.update(histogram)
    assert len(placements) == 16 and comparisons == 107296
    return dict(factor_order=['original_ternary_C', 'original_unary_U'],
        original_ordered_contact_names=['C_x', 'C_y', 'C_z', 'U_u'],
        first_spoke_boundary_index=0, slit_boundary_indices=[0, 1, 2, 3, 4, 0],
        interval_endpoints='First and last actual attachments in the same compatible lift; '
                           'interval interior points are an allowed envelope, never new attachments.',
        geometric_sector_catalog=sectors,
        profile_domains=[profile_domain(a)[1] for a in sorted(used)],
        placements=placements, target_orbits={str(m): orbit(m) for m in (933, 941)},
        all_profile_comparisons=comparisons, comparisons_sha256=digest.hexdigest(),
        global_sigma_histogram=sorted(totals.items()), surviving_target_profiles=0,
        ternary_D_identity_screen=False,
        scope='Necessary common-frame singleton profiles; no fabricated original relation or disk graph.')


def gluing_controls():
    ternary = list(product(range(4), repeat=3))
    domains = [tuple(c for c in range(4) if bits >> c & 1) for bits in range(1, 16)]
    # Literal coordinates are r, the two original frame neighbours, then all
    # four original internal contacts. Coordinate ordering is kept throughout.
    operator = [t for t in product(range(4), repeat=7) if t[0] not in t[1:]]
    assert len(operator) == 2916
    fibers = {(e, f, p, u): tuple((a, e, f) + p + (u,) for a in range(4)
                                 if a not in {e, f, u} | set(p))
              for e, f, p, u in product(range(4), range(4), ternary, range(4))}
    assert sorted(t for value in fibers.values() for t in value) == operator
    checks, double_checks, digest = 0, 0, sha256()
    non_cartesian_witness = None
    for domain in domains:
        unary_forbidden = set(domain) if len(domain) == 1 else set()
        for e, f in product(range(4), repeat=2):
            singleton_fibers = []
            for p in ternary:
                joined = tuple(sorted(t for u in domain for t in fibers[e, f, p, u]))
                direct = tuple(sorted((a, e, f) + p + (u,)
                    for a, u in product(range(4), domain) if a not in {e, f, u} | set(p)))
                assert joined == direct
                assert {t[0] for t in joined} == U - {e, f} - set(p) - unary_forbidden
                singleton_fibers.append(joined)
                digest.update(json.dumps([p, domain, e, f, joined]).encode())
                checks += 1
            for i, j in combinations(range(64), 2):
                relation = (ternary[i], ternary[j])
                joined = tuple(sorted(singleton_fibers[i] + singleton_fibers[j]))
                direct = tuple(sorted((a, e, f) + p + (u,)
                    for p, a, u in product(relation, range(4), domain)
                    if a not in {e, f, u} | set(p)))
                assert joined == direct
                forbidden = set(ternary[i]) & set(ternary[j])
                assert {t[0] for t in joined} == U - {e, f} - forbidden - unary_forbidden
                marginals = [set(p[k] for p in relation) for k in range(3)]
                if (non_cartesian_witness is None and len(forbidden) <= 1
                        and len(set(product(*marginals))) > len(relation) and joined):
                    non_cartesian_witness = dict(original_ordered_relation=relation,
                        unary_domain=domain, literal_spoke_colors=[e, f],
                        full_join=joined, forbidden_colors=sorted(forbidden),
                        excluded_marginal_product_tuples=sorted(set(product(*marginals)) - set(relation)))
                digest.update(json.dumps([relation, domain, e, f, joined]).encode())
                double_checks += 1
    assert checks == 15360 and double_checks == 483840
    assert non_cartesian_witness is not None
    return dict(port_order=['r', 'b_first_spoke', 'b_second_spoke', 'C_x', 'C_y', 'C_z', 'U_u'],
        complete_seven_port_operator=operator, ordered_ternary_tuples=ternary,
        nonempty_unary_domains=domains, singleton_relation_spoke_pair_checks=checks,
        two_tuple_relation_spoke_pair_checks=double_checks,
        complete_joins_sha256=digest.hexdigest(), non_cartesian_control=non_cartesian_witness,
        arbitrary_relation_coverage='In one literal frame, J(R,S) is the union of singleton '
            'ordered-tuple joins over every p in original R and every u in original S. '
            'The root projection is U minus both literal spoke colors, intersection(set(p)), '
            'and the unary singleton forbidden set.',
        scope='Full ordered relation algebra; these abstract controls assert no source realization.')


def build():
    source, joins = source_controls(), gluing_controls()
    paths = [Path(__file__).resolve()] + [ROOT / 'scripts' / (name + '.py') for name in (
        'c5_excess_two_ternary_two_unary', 'c5_excess_two_three_unary',
        'c5_independent_support_capacity', 'c5_single_spoke_three_one',
        'c5_short_support_singleton')]
    return dict(schema=1, scope='epsilon=2, unique degree-6 root, t=2 original (3,1) whole-source exclusion',
        pattern_order=ROWS,
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        source_controls=source, complete_relation_gluing=joins,
        paper_dependencies=['ternary capacity at most one uses at least one original spoke',
            'short-support lemma and edge-minimality give both actual support spans at least two',
            'two original spokes confine each connected original component to one sector',
            'same original graph support envelopes and common-frame S4 profile equivariance'],
        summary=dict(spoke_pairs_in_one_literal_frame=4, ordered_sector_interval_pairs=8,
            named_placements=16, all_profile_comparisons=107296, target_orbits=10,
            surviving_target_profiles=0, ternary_D_identity_needed=False,
            complete_seven_port_operator_tuples=2916,
            singleton_relation_spoke_pair_checks=joins['singleton_relation_spoke_pair_checks'],
            two_tuple_relation_spoke_pair_checks=joins['two_tuple_relation_spoke_pair_checks'],
            graph_enumeration=False, disk_realizability_claim=False, new_Lean_theorem=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
