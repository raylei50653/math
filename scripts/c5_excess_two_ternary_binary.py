#!/usr/bin/env python3
"""Original (3,2): same-source D identity and binary path-bag exclusion."""
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
from c5_single_spoke_frame_arc import admissible_supports
from c5_single_spoke_cross_row import joint_supports
from c5_single_spoke_two_arc import fixed_partitions

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_ternary_binary/observations.json'
PERMS = tuple(permutations(range(4)))


@lru_cache(None)
def path_evidence(support, external, queries):
    family = set(frozenset(c) for n in range(len(support) + 1) for c in combinations(support, n))
    for i, forbidden in queries:
        local = set(admissible_supports(ROWS[i], support, forbidden))
        independent = {t for t in family if all({p[c] for c in forbidden} == set(forbidden)
            for p in PERMS if all(p[ROWS[i][v]] == ROWS[i][v] for v in t))}
        assert family & local == independent
        family &= local
    for (i, f), (j, g) in combinations(queries, 2):
        joint = set(joint_supports(ROWS[i], ROWS[j], support, f, g))
        independent = {t for t in family if all({p[c] for c in f} == set(g)
            for p in PERMS if all(p[ROWS[i][v]] == ROWS[j][v] for v in t))}
        assert family & joint == independent
        family &= joint
    family = sorted(tuple(sorted(t)) for t in family)
    record = dict(binary_envelope=support, actual_external_anchors=external,
                  same_binary_pair_rows=queries, admissible_actual_bag_supports=family)
    if not family:
        return dict(record, exclusion='empty_actual_bag_support_family')
    partitions = fixed_partitions(tuple(family), external)
    if partitions:
        return dict(record, exclusion='common_two_frame_arcs_K5',
                    frame_partition=[sorted(a) for a in partitions[0]])
    forced = sorted(set.intersection(*map(set, family)))
    for pair in combinations(forced, 2):
        landing = sorted(set(external) - set(pair))
        if landing:
            return dict(record, exclusion='forced_pair_three_frame_arcs_K5',
                        forced_boundary_pair=pair, actual_external_landing=landing[0])
    return dict(record, exclusion=None)


def solve(supports, target, use_path=True):
    maps, options = {}, {}
    for comp, (support, capacity) in enumerate(zip(supports, (2, 1))):
        representatives = {}
        for i, row in enumerate(ROWS):
            values = tuple(row[j] for j in support)
            key = (comp, normalize(values))
            if key not in representatives:
                representatives[key] = values
                options[key] = invariant_sets(set(values), capacity)
            maps[comp, i] = (key, representatives[key], values)
    variables = sorted(options)
    row_options = []
    for i, row in enumerate(ROWS):
        m = [maps[c, i] for c in range(2)]
        records = []
        for choices in product(*(range(len(options[x[0]])) for x in m)):
            fs = [set(transport(x[1], x[2], options[x[0]][a])) for x, a in zip(m, choices)]
            if bool(U - {row[0]} - set.union(*fs)) != bool(target >> i & 1):
                continue
            records.append((dict((x[0], a) for x, a in zip(m, choices)), fs))
        row_options.append(records)
    order = sorted(range(10), key=lambda i: len(row_options[i]))
    chosen, counts, reasons = {}, Counter(), {}
    digest = sha256()
    external = tuple(sorted({0, supports[1][0], supports[1][-1]}))

    def dfs(pos, assigned, role):
        counts['search_nodes'] += 1
        if pos == 10:
            return [[sorted(f) for f in chosen[i]] for i in range(10)]
        i = order[pos]
        for choice_index, (assignment, fs) in enumerate(row_options[i]):
            if any(k in assigned and assigned[k] != v for k, v in assignment.items()):
                counts['same_local_profile_conflicts'] += 1
                continue
            newrole = role
            if len(set(ROWS[i])) == 3 and fs[1]:
                typ = 3 in fs[1]
                if role is not None and role != typ:
                    counts['same_ternary_D_identity_conflicts'] += 1
                    continue
                newrole = typ
            if use_path and len(fs[0]) == 2:
                queries = tuple(sorted([(j, tuple(sorted(f[0]))) for j, f in chosen.items()
                                        if len(f[0]) == 2] + [(i, tuple(sorted(fs[0])))]))
                evidence = path_evidence(supports[0], external, queries)
                if evidence['exclusion']:
                    counts[evidence['exclusion']] += 1
                    key = json.dumps(evidence, sort_keys=True)
                    reasons[key] = evidence
                    digest.update(json.dumps([pos, i, choice_index, evidence], sort_keys=True).encode())
                    continue
            chosen[i] = fs
            found = dfs(pos + 1, assigned | assignment, newrole)
            if found is not None:
                return found
            del chosen[i]
        return None

    witness = dfs(0, {}, None)
    return dict(target=target, variable_count=len(variables),
        variable_domains=[dict(component=k[0], equality_pattern=k[1],
                               options=[sorted(f) for f in options[k]]) for k in variables],
        row_candidate_counts=list(map(len, row_options)), row_order=order,
        search_counts=dict(sorted(counts.items())), exclusions=list(reasons.values()),
        path_exclusion_trace_sha256=digest.hexdigest(), surviving_profile=witness)


def source_controls():
    arcs = [(a, b) for a in range(6) for b in range(a + 2, 6)]
    ordered = [(a, b) for a, b in product(arcs, repeat=2) if a[1] <= b[0]]
    assert len(ordered) == 5
    records, negative_controls = [], []
    for shape_id, intervals in enumerate(ordered):
        for slots in permutations(range(2)):
            supports = tuple(tuple(i % 5 for i in range(intervals[j][0], intervals[j][1] + 1))
                             for j in slots)
            for target in sorted(set(orbit(933) + orbit(941))):
                result = solve(supports, target)
                assert result['surviving_profile'] is None
                records.append(dict(result, ordered_interval_pair=shape_id,
                                    factor_slots=slots, factor_envelopes=supports))
                weaker = solve(supports, target, use_path=False)
                if weaker['surviving_profile'] is not None:
                    negative_controls.append(dict(ordered_interval_pair=shape_id,
                        factor_slots=slots, factor_envelopes=supports, target=target,
                        profile=weaker['surviving_profile'],
                        scope='Necessary S4 and D-identity profile only; not a disk realization.'))
    assert len(records) == 100 and len(negative_controls) == 8
    return dict(factor_order=['original_binary_B', 'original_ternary_C'],
        original_contact_order=['binary_x', 'binary_y', 'ternary_u', 'ternary_v', 'ternary_w'],
        fixed_spoke_boundary_index=0, slit_boundary_indices=[0, 1, 2, 3, 4, 0],
        interval_endpoints='Actual source attachments; interval interiors are envelope points only.',
        ordered_interval_pairs=ordered, queries=records,
        target_orbits={str(m): orbit(m) for m in (933, 941)},
        no_binary_path_screen_controls=negative_controls)


def gluing_controls():
    binary = list(product(range(4), repeat=2))
    ternary = list(product(range(4), repeat=3))
    operator = [t for t in product(range(4), repeat=6) if t[0] not in t[1:]]
    fibers = {(p, q): tuple(t for t in operator if t[1:3] == p and t[3:] == q)
              for p, q in product(binary, ternary)}
    singleton, double, digest = 0, 0, sha256()
    for p, q in product(binary, ternary):
        direct = tuple((a,) + p + q for a in range(4) if a not in p + q)
        assert direct == fibers[p, q]
        for e in range(4):
            joined = tuple(t for t in direct if t[0] != e)
            assert {t[0] for t in joined} == U - set(p) - set(q) - {e}
            singleton += 1
    for bp, tp in product(combinations(binary, 2), combinations(ternary, 2)):
        joined = tuple(sorted(t for p, q in product(bp, tp) for t in fibers[p, q]))
        direct = tuple(sorted((a,) + p + q for a, p, q in product(range(4), bp, tp)
                              if a not in p + q))
        assert joined == direct
        fb = set(bp[0]) & set(bp[1])
        ft = set(tp[0]) & set(tp[1])
        assert {t[0] for t in joined} == U - fb - ft
        for e in range(4):
            assert {t[0] for t in joined if t[0] != e} == U - fb - ft - {e}
        double += 1
        digest.update(json.dumps([bp, tp, joined]).encode())
    assert singleton == 4096 and double == 241920
    return dict(port_order=['r', 'binary_x', 'binary_y', 'ternary_u', 'ternary_v', 'ternary_w'],
        complete_six_port_star_operator=operator, ordered_binary_tuples=binary,
        ordered_ternary_tuples=ternary, singleton_pair_spoke_checks=singleton,
        two_element_relation_pair_checks=double, two_element_pair_spoke_checks=4 * double,
        full_relations_sha256=digest.hexdigest(),
        arbitrary_relation_coverage='J(RB,RC) is the union of singleton ordered-tuple '
            'joins over RB times RC. Full shared-color tuples are retained.',
        scope='Abstract complete relation controls; no source realizability claim.')


def build():
    source, joins = source_controls(), gluing_controls()
    paths = [Path(__file__).resolve()] + [ROOT / 'scripts' / (name + '.py') for name in (
        'c5_excess_two_binary_three_unary', 'c5_independent_support_capacity',
        'c5_excess_two_three_unary', 'c5_single_spoke_frame_arc',
        'c5_single_spoke_cross_row', 'c5_single_spoke_two_arc')]
    counts = Counter()
    for query in source['queries']:
        counts.update(query['search_counts'])
    return dict(schema=1, scope='t=1 original (3,2) whole-source exclusion', pattern_order=ROWS,
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        source_controls=source, complete_relation_gluing=joins,
        paper_dependencies=['ternary capacity one and cross-row D identity',
            'actual support span at least two for both original components',
            'one actual spoke slit and simultaneous minimal support envelopes',
            'binary same-original-path bag residuals and original-source K5 minors'],
        summary=dict(ordered_interval_pairs=5, named_placements=10, target_queries=100,
            remaining=0, profiles_without_binary_path_screen=8, search_counts=dict(sorted(counts.items())),
            singleton_relation_pair_spoke_checks=4096, two_element_relation_pair_checks=241920,
            two_element_pair_spoke_checks=967680, graph_enumeration=False,
            disk_realizability_claim=False, new_Lean_theorem=False))


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
