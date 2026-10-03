#!/usr/bin/env python3
"""Three spokes, original (2,1): fixed same-source profile exclusion.

Arbitrary original component sizes are covered by the companion paper
lemmas. This script does not enumerate source graphs or assert realizability.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U, T4, normalize
from c5_excess_two_three_unary import orbit
from c5_excess_two_binary_three_unary import invariant_sets, transport

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_three_spoke_binary/observations.json'
PERMS = tuple(permutations(range(4)))


def geometry(spokes):
    sectors = [tuple((s + k) % 5 for k in
                     range((spokes[(j + 1) % 3] - s) % 5 + 1))
               for j, s in enumerate(spokes)]
    choices = [(sid, a, b, sector[a:b + 1])
               for sid, sector in enumerate(sectors)
               for a in range(len(sector)) for b in range(a + 2, len(sector))]
    for placement in product(choices, repeat=2):
        p, q = placement
        if p[0] == q[0] and not (p[2] <= q[1] or q[2] <= p[1]):
            continue
        yield dict(spokes=spokes, sectors=sectors,
                   component_order=['original_binary_C', 'original_unary_V'],
                   sector_ids=[p[0] for p in placement],
                   offsets=[[p[1], p[2]] for p in placement],
                   envelopes=[p[3] for p in placement])


@lru_cache(None)
def profile_domain(support, capacity):
    """All local S4-equivariant envelope profiles, including all-empty."""
    representatives, row_maps = {}, []
    for ri, row in enumerate(ROWS):
        values = tuple(row[j] for j in support)
        key = normalize(values)
        representatives.setdefault(key, (ri, values))
        row_maps.append((key, values))
    keys = sorted(representatives)
    options = [invariant_sets(set(representatives[key][1]), capacity) for key in keys]
    assert keys == [(0, 1, 0), (0, 1, 2)]
    assert list(map(len, options)) == ([5, 11] if capacity == 2 else [3, 5])
    transports, checks = [], 0
    for key, values in row_maps:
        base = representatives[key][1]
        maps = [p for p in PERMS if tuple(p[c] for c in base) == values]
        assert maps
        for forbidden in options[keys.index(key)]:
            expected = transport(base, values, forbidden)
            assert {tuple(sorted(p[c] for c in forbidden)) for p in maps} == {expected}
            checks += len(maps)
        transports.append(dict(equality_pattern=key, aligned_color_permutations=maps))
    profiles, choices = [], []
    for selected in product(*options):
        literal = tuple(transport(representatives[key][1], values,
                                  selected[keys.index(key)])
                        for key, values in row_maps)
        profiles.append(literal)
        choices.append(selected)
    assert len(set(profiles)) == len(profiles)
    assert len(profiles) == (55 if capacity == 2 else 15)
    record = dict(envelope_boundary_indices=support, forbidden_capacity=capacity,
        local_classes=[dict(equality_pattern=key, representative_row=representatives[key][0],
                            representative_literal_colors=representatives[key][1],
                            stabilizer_invariant_forbidden_options=opts)
                       for key, opts in zip(keys, options, strict=True)],
        row_transports=transports, aligned_permutation_controls=checks,
        all_empty_profile_allowed=True,
        profiles=[dict(profile_index=i, forbidden_by_local_class=choice,
                       complete_ten_row_forbidden_profile=profile)
                  for i, (choice, profile) in enumerate(zip(choices, profiles, strict=True))])
    return tuple(profiles), record


def source_controls():
    target_masks = sorted(set(orbit(933) + orbit(941)))
    placements, sector_catalog, used = [], [], set()
    comparisons, digest, totals = 0, sha256(), Counter()
    row_independent_controls = []
    for spokes in combinations(range(5), 3):
        shapes = list(geometry(spokes))
        sectors = [tuple((s + k) % 5 for k in
                         range((spokes[(j + 1) % 3] - s) % 5 + 1))
                   for j, s in enumerate(spokes)]
        lengths = sorted(len(sector) - 1 for sector in sectors)
        assert len(shapes) == (2 if lengths == [1, 2, 2] else 0)
        sector_catalog.append(dict(spokes=spokes, sectors=sectors,
                                   sector_edge_lengths=lengths, named_placements=len(shapes)))
        for shape in shapes:
            gid = len(placements)
            supports = tuple(map(tuple, shape['envelopes']))
            used.update(zip(supports, (2, 1)))
            pools = [profile_domain(support, capacity)[0]
                     for support, capacity in zip(supports, (2, 1), strict=True)]
            histogram, witnesses, rejected_histogram = Counter(), {}, Counter()
            t4_histogram = Counter()
            for indices in product(*(range(len(pool)) for pool in pools)):
                fc, fv = [pool[i] for pool, i in zip(pools, indices, strict=True)]
                mask = sum(1 << ri for ri, row in enumerate(ROWS)
                           if U - {row[s] for s in spokes} - set(fc[ri]) - set(fv[ri]))
                assert mask not in target_masks, (shape, indices, mask)
                histogram[mask] += 1
                witnesses.setdefault(mask, indices)
                rejected_histogram[10 - mask.bit_count()] += 1
                if mask & T4 == T4:
                    assert 10 - mask.bit_count() <= 1
                    t4_histogram[10 - mask.bit_count()] += 1
                digest.update(json.dumps([gid, indices, mask], separators=(',', ':')).encode())
                comparisons += 1
            placements.append(dict(shape, geometry_id=gid,
                profile_domain_sizes=list(map(len, pools)),
                sigma_histogram=[dict(sigma=m, count=n, first_profile_indices=witnesses[m])
                                 for m, n in sorted(histogram.items())],
                rejected_row_count_histogram=sorted(rejected_histogram.items()),
                T4_accepting_rejected_row_count_histogram=sorted(t4_histogram.items())))
            totals.update(histogram)
            # Independent-row choices deliberately omit the common local
            # profile requirement. All 100 target queries then remain possible.
            for target in target_masks:
                selected, row_counts = [], []
                for ri, row in enumerate(ROWS):
                    opts = [invariant_sets({row[j] for j in support}, capacity)
                            for support, capacity in zip(supports, (2, 1), strict=True)]
                    rows = [(fc, fv) for fc, fv in product(*opts)
                            if bool(U - {row[s] for s in spokes} - set(fc) - set(fv))
                            == bool(target >> ri & 1)]
                    assert rows
                    row_counts.append(len(rows))
                    selected.append(rows[0])
                row_independent_controls.append(dict(geometry_id=gid, target=target,
                    row_candidate_counts=row_counts, complete_ten_row_forbidden_profile=selected,
                    scope='Each row is selected independently. This deliberately drops '
                          'same-component S4 profile consistency; no source realization.'))
    assert len(placements) == 10 and comparisons == 8250
    assert len(row_independent_controls) == 100
    return dict(original_contact_order=['C_x', 'C_y', 'V_v'],
        original_component_order=['original_binary_C', 'original_unary_V'],
        target_orbits={str(m): orbit(m) for m in (933, 941)},
        envelope_endpoint_rule='Both endpoints are actual attachments in the same '
            'source embedding; interiors are permissible positions only.',
        spoke_sector_catalog=sector_catalog,
        profile_domains=[profile_domain(support, capacity)[1]
                         for support, capacity in sorted(used)],
        geometry=placements, all_profile_comparisons=comparisons,
        comparisons_sha256=digest.hexdigest(), global_sigma_histogram=sorted(totals.items()),
        row_independent_negative_controls=row_independent_controls,
        surviving_target_profiles=0, binary_path_screen=False,
        first_bridge_screen=False, original_omission_screen=False, unary_D_identity_screen=False)


def gluing_controls():
    binary = tuple(product(range(4), repeat=2))
    unary_domains = [tuple(c for c in range(4) if bits >> c & 1) for bits in range(1, 16)]
    spoke_triples = tuple(product(range(4), repeat=3))
    operator = tuple(t for t in product(range(4), repeat=7) if t[0] not in t[1:])
    assert len(operator) == 2916
    fibers = {(sp, p, u): tuple((a,) + sp + p + (u,) for a in range(4)
                              if a not in sp + p + (u,))
              for sp, p, u in product(spoke_triples, binary, range(4))}
    assert sorted(t for value in fibers.values() for t in value) == list(operator)
    single_checks, pair_checks, digest = 0, 0, sha256()
    for domain in unary_domains:
        fv = set(domain) if len(domain) == 1 else set()
        for sp in spoke_triples:
            single_joins = []
            for p in binary:
                joined = tuple(sorted(t for u in domain for t in fibers[sp, p, u]))
                direct = tuple(sorted((a,) + sp + p + (u,)
                    for a, u in product(range(4), domain) if a not in sp + p + (u,)))
                assert joined == direct
                assert {t[0] for t in joined} == U - set(sp) - set(p) - fv
                single_joins.append(joined)
                digest.update(json.dumps([p, domain, sp, joined], separators=(',', ':')).encode())
                single_checks += 1
            for i, j in combinations(range(16), 2):
                relation = (binary[i], binary[j])
                joined = tuple(sorted(single_joins[i] + single_joins[j]))
                direct = tuple(sorted((a,) + sp + p + (u,)
                    for p, a, u in product(relation, range(4), domain)
                    if a not in sp + p + (u,)))
                assert joined == direct
                fc = set(binary[i]) & set(binary[j])
                assert {t[0] for t in joined} == U - set(sp) - fc - fv
                digest.update(json.dumps([relation, domain, sp, joined], separators=(',', ':')).encode())
                pair_checks += 1
    assert single_checks == 15360 and pair_checks == 115200
    collision = []
    for relation in (((0, 1), (1, 0)), ((0, 0), (1, 1))):
        sp, domain = (2, 2, 2), (2, 3)
        joined = tuple(sorted((a,) + sp + p + (u,)
            for p, a, u in product(relation, range(4), domain)
            if a not in sp + p + (u,)))
        collision.append(dict(original_ordered_binary_relation=relation,
            endpoint_marginals=[sorted({p[j] for p in relation}) for j in range(2)],
            binary_forbidden=sorted(set.intersection(*(set(p) for p in relation))),
            literal_spoke_colors=sp, original_unary_domain=domain,
            complete_seven_port_join=joined, exact_root_projection=sorted({t[0] for t in joined})))
    assert collision[0]['endpoint_marginals'] == collision[1]['endpoint_marginals']
    assert collision[0]['exact_root_projection'] == [3]
    assert collision[1]['exact_root_projection'] == [0, 1, 3]
    return dict(port_order=['r', 'b_first_spoke', 'b_second_spoke', 'b_third_spoke',
                           'C_x', 'C_y', 'V_v'],
        complete_seven_port_operator=operator, ordered_binary_tuples=binary,
        nonempty_unary_domains=unary_domains, literal_spoke_color_triples=spoke_triples,
        singleton_fiber_count=len(fibers), singleton_relation_spoke_triple_checks=single_checks,
        two_tuple_relation_spoke_triple_checks=pair_checks,
        complete_joins_sha256=digest.hexdigest(), marginal_collision=collision,
        arbitrary_relation_coverage='In one literal frame, J(R,S) is the union of '
            'the singleton ordered-tuple joins over all p in the original R and '
            'all u in the original S. Empty fibers stay empty. F is only the '
            'exact root-query projection and never replaces the ordered R.',
        scope='Full ordered relation algebra; abstract controls assert no source realization.')


def build():
    source, joins = source_controls(), gluing_controls()
    t4_counts = Counter()
    for placement in source['geometry']:
        t4_counts.update(dict(placement['T4_accepting_rejected_row_count_histogram']))
    assert sorted(t4_counts.items()) == [(0, 1440), (1, 360)]
    names = ('c5_independent_support_capacity', 'c5_excess_two_three_unary',
             'c5_excess_two_binary_three_unary', 'c5_short_support_singleton')
    paths = [Path(__file__).resolve()] + [ROOT / 'scripts' / (name + '.py') for name in names]
    return dict(schema=1, scope='epsilon=2, unique degree-6 root, t=3 original (2,1) whole-source exclusion',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        pattern_order=ROWS, source_controls=source, complete_relation_gluing=joins,
        paper_dependencies=['original component slack and complete ordered seven-port gluing',
            'edge-minimal private witnesses and short-support exclusion give both spans at least two',
            'three original spokes confine each whole component to one original sector',
            'same embedding compatible envelopes have actual first and last attachment endpoints',
            'common-frame S4 equivariance of full original relations implies common envelope profiles'],
        summary=dict(named_spoke_triples=10, named_sector_envelopes=10,
            binary_profile_domain_size=55, unary_profile_domain_size=15,
            all_profile_comparisons=8250, target_orbits=10, surviving_target_profiles=0,
            T4_accepting_profile_pairs=1800, T4_accepting_maximum_rejected_rows=1,
            T4_accepting_rejected_row_count_histogram=sorted(t4_counts.items()),
            row_independent_negative_controls=100,
            complete_seven_port_operator_tuples=len(joins['complete_seven_port_operator']),
            singleton_relation_spoke_triple_checks=joins['singleton_relation_spoke_triple_checks'],
            two_tuple_relation_spoke_triple_checks=joins['two_tuple_relation_spoke_triple_checks'],
            binary_path_screen=False, first_bridge_screen=False,
            original_omission_screen=False, unary_D_identity_screen=False,
            graph_enumeration=False, disk_realizability_claim=False, new_Lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
