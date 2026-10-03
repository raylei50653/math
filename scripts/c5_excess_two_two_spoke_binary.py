#!/usr/bin/env python3
"""Exclude t=2 original (2,2) with the same original first bridge.

Finite necessary profiles and literal ordered relation controls.  Arbitrary
source sizes are covered by the paper lemmas, not by graph enumeration.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U, normalize
from c5_excess_two_three_unary import orbit
from c5_excess_two_binary_three_unary import invariant_sets, transport
from c5_excess_two_ternary_binary import path_evidence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_two_spoke_binary/observations.json'
PERMS = tuple(permutations(range(4)))


def geometry(spokes):
    sectors = [tuple((s + k) % 5 for k in
                     range((spokes[(j + 1) % 2] - s) % 5 + 1))
               for j, s in enumerate(spokes)]
    choices = [(sid, a, b, sector[a:b + 1])
               for sid, sector in enumerate(sectors)
               for a in range(len(sector)) for b in range(a + 2, len(sector))]
    for placement in product(choices, repeat=2):
        p, q = placement
        if p[0] == q[0] and not (p[2] <= q[1] or q[2] <= p[1]):
            continue
        yield dict(spokes=spokes, sectors=sectors,
                   component_order=['original_binary_A', 'original_binary_C'],
                   sector_ids=[p[0] for p in placement],
                   offsets=[[p[1], p[2]] for p in placement],
                   envelopes=[p[3] for p in placement])


@lru_cache(None)
def bag_evidence(support, external, residual_rows):
    """Reuse the t=1 support algebra with local E, which need not equal F.

For pure pair rows it covers all original path bags.  With a singleton-row
local residual it covers precisely the two bags at the same first bridge.
"""
    result = dict(path_evidence(support, external, residual_rows))
    result['local_residual_rows'] = result.pop('same_binary_pair_rows')
    return result


@lru_cache(None)
def first_bridge_evidence(support, external, queries):
    pair_rows = tuple((i, f) for i, f in queries if len(f) == 2)
    if not pair_rows:
        return None
    singleton_rows = []
    for qi, fq in queries:
        if len(fq) != 1:
            continue
        c = fq[0]
        for ri, fr in pair_rows:
            kept = tuple(h for h in range(4) if all(
                (ROWS[qi][v] == h) == (ROWS[ri][v] == h) for v in support))
            if c not in kept:
                continue
            base = dict(singleton_row=qi, singleton_forbidden=c,
                        reference_pair_row=ri, pair_forbidden=fr,
                        envelope_membership_conserved_colors=kept)
            if c not in fr:
                return dict(exclusion='first_endpoint_conserved_color_contradiction',
                            binary_envelope=support, **base)
            betas = tuple(b for b in range(4) if b != c and
                          {c, b} & set(kept) == set(fr) & set(kept))
            singleton_rows.append(dict(base, possible_same_first_bridge_beta=betas))
            # One applicable reference pair is enough.  Other reference-pair
            # membership tests are safely omitted; all residual transports
            # are still checked after the local E is selected.
            break
    if not singleton_rows:
        return None
    branches = []
    for betas in product(*(r['possible_same_first_bridge_beta'] for r in singleton_rows)):
        residual_rows = tuple(sorted(pair_rows + tuple(
            (r['singleton_row'], tuple(sorted((r['singleton_forbidden'], beta))))
            for r, beta in zip(singleton_rows, betas, strict=True))))
        evidence = bag_evidence(support, external, residual_rows)
        if evidence['exclusion'] is None:
            return None
        branches.append(dict(beta_by_singleton_row=betas,
                             common_first_bridge_bag_evidence=evidence))
    return dict(exclusion='all_common_first_bridge_residuals_excluded',
                binary_envelope=support, actual_external_anchors=external,
                same_original_pair_rows=pair_rows,
                singleton_local_residual_controls=singleton_rows,
                all_independent_row_beta_branches=branches,
                scope='Each row shares beta only between the two ends of the same '
                      'original first bridge; different rows choose beta independently.')


def solve(spokes, supports, target, use_path=True, use_first_bridge=True):
    maps, options = {}, {}
    for comp, support in enumerate(supports):
        representatives = {}
        for i, row in enumerate(ROWS):
            values = tuple(row[j] for j in support)
            key = (comp, normalize(values))
            if key not in representatives:
                representatives[key] = values
                options[key] = invariant_sets(set(values), 2)
            maps[comp, i] = (key, representatives[key], values)
    row_options = []
    for i, row in enumerate(ROWS):
        mapped = [maps[c, i] for c in range(2)]
        spoke_colors = {row[s] for s in spokes}
        records = []
        for choices in product(*(range(len(options[x[0]])) for x in mapped)):
            fs = [set(transport(x[1], x[2], options[x[0]][a]))
                  for x, a in zip(mapped, choices, strict=True)]
            if bool(U - spoke_colors - set.union(*fs)) != bool(target >> i & 1):
                continue
            # Both named original binary omissions and the two-spoke omission
            # accept every row under the fixed-source hypotheses.
            if any(spoke_colors | f == U for f in fs) or set.union(*fs) == U:
                continue
            records.append((dict((x[0], a) for x, a in
                                 zip(mapped, choices, strict=True)), fs))
        row_options.append(records)
    order = sorted(range(10), key=lambda i: len(row_options[i]))
    chosen, counts, reasons = {}, Counter(), {}
    digest = sha256()
    external = [tuple(sorted(set(spokes) |
                {supports[1 - c][0], supports[1 - c][-1]})) for c in range(2)]

    def dfs(pos, assigned):
        counts['search_nodes'] += 1
        if pos == 10:
            return [[sorted(f) for f in chosen[i]] for i in range(10)]
        i = order[pos]
        for choice_index, (assignment, fs) in enumerate(row_options[i]):
            if any(k in assigned and assigned[k] != v for k, v in assignment.items()):
                counts['same_local_profile_conflicts'] += 1
                continue
            evidence = None
            if use_path:
                for comp in range(2):
                    if not fs[comp]:
                        continue
                    queries = tuple(sorted(
                        [(j, tuple(sorted(f[comp]))) for j, f in chosen.items() if f[comp]] +
                        [(i, tuple(sorted(fs[comp])))]))
                    pairs = tuple((j, f) for j, f in queries if len(f) == 2)
                    if not pairs:
                        continue
                    pure = bag_evidence(supports[comp], external[comp], pairs)
                    if pure['exclusion'] is not None:
                        evidence = dict(pure, original_component=comp,
                                        bag_scope='all original binary path bags')
                        break
                    if use_first_bridge:
                        first = first_bridge_evidence(supports[comp], external[comp], queries)
                        if first is not None:
                            evidence = dict(first, original_component=comp,
                                            bag_scope='two bags at the same original first bridge')
                            break
            if evidence is not None:
                counts[evidence['exclusion']] += 1
                reasons[json.dumps(evidence, sort_keys=True)] = evidence
                digest.update(json.dumps([pos, i, choice_index, evidence], sort_keys=True).encode())
                continue
            chosen[i] = fs
            found = dfs(pos + 1, assigned | assignment)
            if found is not None:
                return found
            del chosen[i]
        return None

    witness = dfs(0, {})
    return dict(target=target,
        variable_domains=[dict(component=k[0], equality_pattern=k[1],
                               options=[list(f) for f in options[k]]) for k in sorted(options)],
        row_candidate_counts=list(map(len, row_options)), row_order=order,
        search_counts=dict(sorted(counts.items())), exclusions=list(reasons.values()),
        exclusion_trace_sha256=digest.hexdigest(), surviving_profile=witness)


def source_controls():
    placements, records, negative_controls = [], [], []
    for spokes in combinations(range(5), 2):
        shapes = list(geometry(spokes))
        assert len(shapes) == (2 if (spokes[1] - spokes[0]) in (1, 4) else 6)
        for shape in shapes:
            gid = len(placements)
            placements.append(shape)
            supports = tuple(map(tuple, shape['envelopes']))
            for target in sorted(set(orbit(933) + orbit(941))):
                result = solve(spokes, supports, target)
                assert result['surviving_profile'] is None
                records.append(dict(result, geometry_id=gid))
                weaker = solve(spokes, supports, target, use_first_bridge=False)
                if weaker['surviving_profile'] is not None:
                    negative_controls.append(dict(geometry_id=gid, target=target,
                        complete_ten_row_forbidden_profile=weaker['surviving_profile'],
                        row_candidate_counts=weaker['row_candidate_counts'],
                        scope='Same-source necessary profiles with pure pair-path constraints; '
                              'not a source graph or disk realization.'))
    assert len(placements) == 40 and len(records) == 400
    assert len(negative_controls) == 20
    assert all(r['target'] in orbit(941) for r in negative_controls)
    return dict(original_contact_order=['A_x', 'A_y', 'C_u', 'C_v'],
                original_component_order=['original_binary_A', 'original_binary_C'],
                target_orbits={str(m): orbit(m) for m in (933, 941)},
                envelope_endpoint_rule='Both endpoints are actual attachments in the '
                    'same source embedding; interiors are permissible positions only.',
                geometry=placements, queries=records,
                no_first_bridge_controls=negative_controls)


def relation_controls():
    tuples = tuple(product(range(4), repeat=2))
    operator = tuple(t for t in product(range(4), repeat=5) if t[0] not in t[1:])
    fibers = {(p, q): tuple(t for t in operator if t[1:3] == p and t[3:] == q)
              for p, q in product(tuples, repeat=2)}
    fiber_records = []
    for p, q in product(tuples, repeat=2):
        independent = tuple((r,) + p + q for r in range(4)
                            if r not in p and r not in q)
        assert fibers[p, q] == independent
        fiber_records.append(dict(A_ordered_tuple=p, C_ordered_tuple=q,
                                  full_five_port_fiber=independent))
    representatives, unary_digest = {}, sha256()
    for bits in range(1, 1 << 16):
        relation = tuple(t for j, t in enumerate(tuples) if bits >> j & 1)
        forbidden = tuple(sorted(set.intersection(*(set(t) for t in relation))))
        lifted = tuple((a,) + p for a, p in product(range(4), relation) if a not in p)
        assert {t[0] for t in lifted} == U - set(forbidden)
        representatives.setdefault(forbidden, relation)
        unary_digest.update(bytes(c for t in lifted for c in t) + b'\xff')
    relations = sorted(set(representatives.values()) |
                       {((0, 1), (1, 0)), ((0, 0), (1, 1)), tuples})
    digest, checked = sha256(), 0
    witnesses = []
    for ra, rc in product(relations, repeat=2):
        fa, fc = (set.intersection(*(set(t) for t in r)) for r in (ra, rc))
        joined = tuple(sorted(t for p, q in product(ra, rc) for t in fibers[p, q]))
        direct = tuple(sorted((a,) + p + q for a, p, q in product(range(4), ra, rc)
                              if a not in p + q))
        assert joined == direct
        for mask in range(16):
            colors = {c for c in range(4) if mask >> c & 1}
            restricted = tuple(t for t in joined if t[0] not in colors)
            independent = tuple((a,) + p + q for a, p, q in product(range(4), ra, rc)
                                if a not in p + q and a not in colors)
            assert restricted == independent
            assert {t[0] for t in restricted} == U - fa - fc - colors
            digest.update(bytes(c for t in restricted for c in t) + b'\xff')
            checked += 1
        witnesses.append(dict(A_relation=ra, C_relation=rc,
                              A_forbidden=sorted(fa), C_forbidden=sorted(fc),
                              full_five_port_relation=joined))
    assert len(relations) == 13 and checked == 2704
    return dict(port_order=['r', 'A_x', 'A_y', 'C_u', 'C_v'],
        complete_five_port_star_operator=operator, ordered_binary_tuples=tuples,
        all_singleton_ordered_tuple_pair_fibers=fiber_records,
        singleton_ordered_tuple_pair_fiber_checks=256,
        all_nonempty_binary_relations_checked=65535,
        exhaustive_binary_projection_sha256=unary_digest.hexdigest(),
        representative_full_relations=relations, representative_pair_controls=witnesses,
        full_relation_pair_spoke_color_set_checks=checked,
        full_join_sha256=digest.hexdigest(),
        marginal_collision=dict(R1=[[0, 1], [1, 0]], R2=[[0, 0], [1, 1]], F1=[0, 1], F2=[]),
        arbitrary_relation_coverage='Each arbitrary complete join is the union of its '
            'singleton ordered-tuple fibers; both original relations stay in one color frame.',
        scope='Abstract relation controls, not source graph realizations.')


def build():
    source, relations = source_controls(), relation_controls()
    counts = Counter()
    for query in source['queries']:
        counts.update(query['search_counts'])
    names = ('c5_independent_support_capacity', 'c5_excess_two_three_unary',
             'c5_excess_two_binary_three_unary', 'c5_excess_two_ternary_binary',
             'c5_single_spoke_frame_arc', 'c5_single_spoke_cross_row',
             'c5_single_spoke_two_arc')
    paths = [Path(__file__).resolve()] + [ROOT / 'scripts' / (name + '.py') for name in names]
    return dict(schema=1, scope='t=2 original (2,2) whole-source exclusion',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        pattern_order=ROWS, source_controls=source, complete_relation_controls=relations,
        paper_dependencies=['original component slack and complete ordered five-port gluing',
            'fixed-Sigma edge-minimal private witnesses and short-support exclusion',
            'same embedding two-spoke sectors and compatible actual support envelopes',
            'both original binary omissions and the two-spoke omission accept all rows',
            'same original binary odd bridge path and rooted block palette uniqueness',
            'singleton fixed-color endpoint and common first-bridge residual',
            'all aligned color permutations transport local rooted residuals',
            'original-source two-frame-arc and three-frame-arc K5 constructions'],
        summary=dict(named_sector_envelopes=40, target_queries=400, remaining=0,
            queries_remaining_without_first_bridge=20,
            search_counts=dict(sorted(counts.items())),
            exhaustive_binary_relation_controls=65535,
            full_relation_pair_spoke_color_set_checks=2704,
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
