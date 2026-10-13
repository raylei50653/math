#!/usr/bin/env python3
"""Exact C9-only D3 / generic Kempe support certificates, stdlib replay.

No C8 module, equality matrix, triangulated orbit cone, or numerical optimizer
is imported.  The generic C9 Kempe table is an explicitly frozen prerequisite;
the independent reviewer reconstructs that table separately.
"""
import argparse
from collections import Counter
import copy
import gzip
import hashlib
from itertools import permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SOURCE_REL = 'audits/2026-10-13-c5-no4ct-frontier-6943561/c9/finite/certificate.v2.json.gz'
SOURCE = AUDIT / 'frozen' / SOURCE_REL


def norm(word):
    mapping = {}
    return tuple(mapping.setdefault(c, len(mapping)) for c in word)


def mask(indices):
    value = 0
    for i in indices:
        value |= 1 << i
    return value


def entries(bits):
    return [i for i in range(820) if bits >> i & 1]


def load_source():
    manifest = json.loads((AUDIT / 'INPUTS.json').read_text())
    item, = [x for x in manifest['inputs'] if x['path'] == SOURCE_REL]
    raw = SOURCE.read_bytes()
    assert len(raw) == item['bytes']
    assert hashlib.sha256(raw).hexdigest() == item['sha256']
    with gzip.open(SOURCE, 'rt') as stream:
        source = json.load(stream)
    return manifest['base'], item['sha256'], source


def rebuild_patterns():
    answer = sorted({norm(p) for p in product(range(4), repeat=9)
                     if all(p[i] != p[(i + 1) % 9] for i in range(9))})
    assert len(answer) == 820
    assert Counter(len(set(p)) for p in answer) == {3: 85, 4: 735}
    return answer


def degree3_triples(patterns):
    """All literal eight-site assignments, modulo common S4 only.

    Each stored triple contains three occurrences, including repetitions.
    The witness fixes every position other than a throughout all three terms.
    """
    index = {p: i for i, p in enumerate(patterns)}
    tables = []
    for a in range(9):
        witnesses = {}
        for p in patterns:
            c = p[(a - 1) % 9]
            if c != p[(a + 1) % 9]:
                continue
            allowed_colors = [d for d in range(4) if d != c]
            terms = []
            for d in allowed_colors:
                changed = list(p)
                changed[a] = d
                terms.append(index[norm(changed)])
            triple = tuple(sorted(terms))
            fixed = list(p)
            fixed[a] = None
            witness = {'fixed_other_eight_colors': fixed,
                       'common_neighbor_color': c,
                       'apex_color_options': allowed_colors,
                       'row_indices_by_apex_color': terms}
            if triple not in witnesses:
                witnesses[triple] = witness
        tables.append([{'row_indices': list(t), **witnesses[t]}
                       for t in sorted(witnesses)])
    return tables


def full_transfer(case, patterns, outer_patterns):
    """Count complete literal inner lifts at each fixed original B word.

    Reconstruct from the named original annulus edges, and compare every
    coefficient with the frozen complete inner-then-outer fibre cardinality.
    Both C5 and odd C9 proper words have free S4 action (orbit size 24).
    """
    labels = case['boundary_order']
    outer_index = {f'b{i}': i for i in range(5)}
    inner_index = {label: i for i, label in enumerate(labels)}
    spokes = []
    expected_edges = {frozenset((f'b{i}', f'b{(i + 1) % 5}')) for i in range(5)}
    expected_edges |= {frozenset((labels[i], labels[(i + 1) % 9])) for i in range(9)}
    for u, v in case['annulus_edges']:
        if u in outer_index and v in inner_index:
            spokes.append((outer_index[u], inner_index[v]))
        elif v in outer_index and u in inner_index:
            spokes.append((outer_index[v], inner_index[u]))
        else:
            assert frozenset((u, v)) in expected_edges
    assert len(spokes) == 14
    perm = list(permutations(range(4)))
    result = [[0] * 820 for _ in range(10)]
    for p_index, p in enumerate(patterns):
        literal = {tuple(g[c] for c in p) for g in perm}
        assert len(literal) == 24
        for r, outer in enumerate(outer_patterns):
            result[r][p_index] = sum(all(outer[b] != word[v] for b, v in spokes)
                                     for word in literal)
            fibre = case['full_lifts_by_inner_then_outer_row'][p_index][r]
            assert result[r][p_index] == len(fibre)
            assert len({tuple(lift) for lift in fibre}) == len(fibre)
            for lift in fibre:
                assert len(lift) == 14 and tuple(lift[5:]) == p
                assert norm(lift[:5]) == tuple(outer)
                colors = dict(zip(case['joint_vertex_order'], lift))
                assert all(colors[u] != colors[v] for u, v in case['annulus_edges'])
    return result


def close_hypothesis(initial, triples, obligations):
    support = initial
    steps = []
    rounds = 0
    while True:
        before_round = support
        # All D3 removals in this stage use the same support, before mutation.
        removed = {}
        for t, triple in enumerate(triples):
            live_occurrences = [p for p in triple['row_indices'] if support >> p & 1]
            if len(live_occurrences) == 1:
                removed.setdefault(live_occurrences[0], t)
        if removed:
            after = support & ~mask(removed)
            steps.append({'rule': 'degree3_triangle', 'before': support,
                          'after': after, 'removals': [
                              {'row_index': p, 'triple_index': t}
                              for p, t in sorted(removed.items())]})
            support = after
        # Actual H components give at least one complete orbit for every split.
        removals = []
        for p in entries(support):
            for split, options in enumerate(obligations[p]):
                if all(orbit & ~support for orbit in options):
                    blockers = []
                    for orbit in options:
                        missing = orbit & ~support
                        first = (missing & -missing).bit_length() - 1
                        blockers.append(first)
                    removals.append({'row_index': p, 'split_index': split,
                                     'first_missing_row_per_orbit': blockers})
                    break
        if removals:
            after = support & ~mask(r['row_index'] for r in removals)
            steps.append({'rule': 'generic_c9_kempe', 'before': support,
                          'after': after, 'removals': removals})
            support = after
        rounds += 1
        if before_round == support:
            break
    return support, steps, rounds


def build():
    base, source_sha, source = load_source()
    patterns = rebuild_patterns()
    assert patterns == list(map(tuple, source['inner_pattern_order']))
    assert len(source['quotient_partitions']) == len(source['quotient_masks']) == 232
    quotient_masks = []
    for part in source['quotient_partitions']:
        assert all(part[i] != part[(i + 1) % 9] for i in range(9))
        qmask = mask(i for i, p in enumerate(patterns)
                     if all(p[a] == p[b] for a in range(9) for b in range(a)
                            if part[a] == part[b]))
        assert qmask
        quotient_masks.append(qmask)
    assert quotient_masks == source['quotient_masks']
    assert source['quotient_partitions'][231] == list(range(9))
    triples = degree3_triples(patterns)
    cases = {c['id']: c for c in source['cases']}
    queries = [q for q in source['queries'] if q['target'] == 932
               and q['status'] == 'necessary_condition_residual']
    assert len(queries) == 20 and all(q['geometry_id'] == 'induced' for q in queries)
    systems, results = [], []
    for q in queries:
        case = cases[q['case_id']]
        transfer = full_transfer(case, patterns, source['outer_pattern_order'])
        columns = [mask(r for r in range(10) if transfer[r][p]) for p in range(820)]
        assert columns == case['column_masks']
        for p in entries(q['fixed_point']):
            assert columns[p] & ~932 == 0
        assert all(q['fixed_point'] & qm for qm in quotient_masks)
        systems.append({'query_id': q['query_id'], 'case_id': q['case_id'],
                        'extras': case['extras'],
                        'boundary_order': case['boundary_order'],
                        'initial_support': q['fixed_point'],
                        'outer_transfer': transfer,
                        'accepted_outer_rows': [2, 5, 7, 8, 9],
                        'rejected_outer_rows': [0, 1, 3, 4, 6]})
        for a, name in enumerate(case['boundary_order']):
            if not name.startswith('a'):
                continue
            final, steps, rounds = close_hypothesis(q['fixed_point'], triples[a],
                                                    source['kempe_obligations'])
            outer_union = 0
            for p in entries(final):
                outer_union |= columns[p]
            missing_quotients = [i for i, qm in enumerate(quotient_masks) if not final & qm]
            assert final == outer_union == 0 and missing_quotients == list(range(232))
            results.append({'query_id': q['query_id'], 'apex': name,
                            'apex_position': a, 'initial_support': q['fixed_point'],
                            'steps': steps, 'rounds_including_final_stationary': rounds,
                            'final_support': final,
                            'missing_accepted_outer_rows': [2, 5, 7, 8, 9],
                            'missing_quotient_indices': missing_quotients,
                            'result': 'degree3_hypothesis_excluded'})
    assert len(results) == 100
    return {'schema': 'c9-932-h4-apex-d3-support-v1', 'base': base,
            'source_certificate_sha256': source_sha,
            'inner_pattern_order': patterns,
            'outer_pattern_order': source['outer_pattern_order'],
            'degree3_triples_by_boundary_position': triples,
            'quotient_partitions': source['quotient_partitions'],
            'quotient_masks': quotient_masks,
            'same_H_count_systems': systems,
            'hypotheses': results,
            'summary': {'original_C9_queries': 20, 'apex_hypotheses': 100,
                        'excluded_hypotheses': 100, 'empty_final_supports': 100,
                        'C9_count_coordinates': 820,
                        'source_relative_quotient_constraints': 232,
                        'degree3_triples_per_position': [len(t) for t in triples],
                        'repeated_index_triples_per_position': [sum(len(set(t['row_indices'])) < 3 for t in ts) for ts in triples],
                        'initial_support_sizes': dict(sorted(Counter(q['fixed_point'].bit_count() for q in queries).items())),
                        'round_histogram_including_stationary': dict(sorted(Counter(q['rounds_including_final_stationary'] for q in results).items())),
                        'whole_source_queries_excluded': 0,
                        'C8_equalities_or_conclusion_used': False,
                        'four_colour_theorem_used': False,
                        'h_ge_5_status': 'OPEN', 'general_932_status': 'OPEN'}}


def canonical(value):
    return json.loads(json.dumps(value))


def verify(actual, expected):
    assert actual == expected, 'complete C9 D3-support certificate mismatch'


def negative_controls(payload):
    mutations = []
    bad = copy.deepcopy(payload)
    bad['hypotheses'][0]['apex_position'] = (bad['hypotheses'][0]['apex_position'] + 1) % 9
    mutations.append(('wrong_named_apex_position', bad))
    bad = copy.deepcopy(payload)
    first = bad['hypotheses'][0]['steps'][0]['removals'][0]
    first['triple_index'] = (first['triple_index'] + 1) % len(bad['degree3_triples_by_boundary_position'][0])
    mutations.append(('wrong_D3_witness', bad))
    bad = copy.deepcopy(payload)
    bad['degree3_triples_by_boundary_position'][0][0]['row_indices'].pop()
    mutations.append(('truncated_D3_three_term_identity', bad))
    bad = copy.deepcopy(payload)
    step = next(s for h in bad['hypotheses'] for s in h['steps'] if s['rule'] == 'generic_c9_kempe')
    step['removals'][0]['first_missing_row_per_orbit'].pop()
    mutations.append(('incomplete_Kempe_orbit_obligation', bad))
    bad = copy.deepcopy(payload)
    bad['same_H_count_systems'][0]['outer_transfer'][2][0] += 1
    mutations.append(('changed_complete_annulus_count', bad))
    bad = copy.deepcopy(payload)
    bad['hypotheses'][0]['final_support'] = 1
    mutations.append(('false_nonempty_terminal_support', bad))
    bad = copy.deepcopy(payload)
    bad['hypotheses'].pop()
    mutations.append(('missing_named_apex_hypothesis', bad))
    rejected = []
    for name, bad in mutations:
        try:
            verify(bad, payload)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('accepted mutation ' + name)
    return rejected


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    ap.add_argument('--negative', action='store_true')
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json.gz')
    args = ap.parse_args()
    payload = canonical(build())
    if args.write:
        with args.certificate.open('xb') as raw:
            with gzip.GzipFile(fileobj=raw, mode='wb', mtime=0) as stream:
                stream.write((json.dumps(payload, sort_keys=True, separators=(',', ':')) + '\n').encode())
    else:
        with gzip.open(args.certificate, 'rt') as stream:
            verify(json.load(stream), payload)
    result = {'status': 'PASS', **payload['summary']}
    if args.negative:
        result['negative_controls_rejected'] = negative_controls(payload)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
