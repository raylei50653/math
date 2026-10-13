#!/usr/bin/env python3
"""Bind the three-target C8 interface to the exact downstream named contracts.

The graph implications are in geometry/PROOF.md. This checker verifies their
complete finite interfaces and prevents silently changing a boundary or target.
"""
import argparse
from collections import Counter
import copy
import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDITS = HERE / 'frozen/audits'
STRUCT = AUDITS / '2026-10-13-c8-struct-243a125'
EXPECTED = {'c15-933', 'c18-933', 'c04-941', 'c07-941',
            'c15-941', 'c18-941', 'c20-941', 'c30-941'}
QUOTIENT = {'c16-941', 'c32-941'}


def read(path):
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == '.gz' else data)


def edges(es):
    return {tuple(sorted(e)) for e in es}


def build():
    finite = read(HERE / 'finite/certificate.json')
    old = read(STRUCT / 'RESULTS.json')
    old_queries = {q['query_id']: q for q in old['queries']}
    cases = {c['id']: c for c in finite['interface']['cases']}
    assert len(cases) == 35
    assert len(finite['query_ledger']) == 105
    assert {q['target'] for q in finite['query_ledger']} == {932, 933, 941}
    rows = []
    for q in finite['query_ledger']:
        name = q['query_id']
        row = {k: q[k] for k in ('query_id', 'case_id', 'target', 'extras', 'boundary_order')}
        if q['status'] != 'necessary_condition_residual':
            assert q['status'] in {'excluded_transfer', 'excluded_count'}
            row['status'] = q['status']
        else:
            original = old_queries[name]
            case = cases[q['case_id']]
            for key in ('extras', 'boundary_order'):
                assert q[key] == original[key] == case[key]
            assert edges(case['collar_edges']) == edges(original['collar_edges'])
            if name in QUOTIENT:
                a, b = (q['boundary_order'].index(v) for v in ('a1', 'a4'))
                equal = [i for i, w in enumerate(finite['interface']['pattern_order'])
                         if w[a] == w[b]]
                upper = q['common_count_query']['final_upper_mask']
                assert len(equal) == 74 and upper.bit_count() == 102
                assert not any(upper >> i & 1 for i in equal)
                row.update(status='excluded_relative_cofacial_quotient',
                           same_original_pair=['a1', 'a4'], positions=[a, b],
                           complete_equal_preimages=equal,
                           quotient_order='k-1', available_colourability_order='k+5')
            else:
                assert name in EXPECTED
                fixed = q['fixed_split_query']
                for key in ('counts', 'partition_coefficients', 'orbit_coefficients',
                            'outer_counts', 'support'):
                    assert fixed[key] == original[key], (name, key)
                row.update(status='necessary_condition_residual',
                           support=fixed['support'], support_size=fixed['support'].bit_count(),
                           source_realizability='OPEN')
        rows.append(row)
    assert {r['query_id'] for r in rows if r['status'] == 'necessary_condition_residual'} == EXPECTED
    tally = Counter(r['status'] for r in rows)
    assert dict(tally) == {'excluded_transfer': 92, 'excluded_count': 3,
                          'excluded_relative_cofacial_quotient': 2,
                          'necessary_condition_residual': 8}

    # The apex proof consumes the literal same frozen vectors, not just eight IDs.
    apex = AUDITS / '2026-10-13-c8-apex-degree-45bc1c3'
    apex_base = read(apex / 'BASE.json')
    assert read(apex / apex_base['inputs']['results']['frozen']) == old

    # Reconnect each m=9 and m=10 graph to its entire original collar and row order.
    followup = read(AUDITS / '2026-10-13-c8-followup-6cafdfb/certificate.json.gz')
    peeling = read(AUDITS / '2026-10-13-c8-peeling-6cafdfb/calibration/certificate.json.gz')
    assert {q['id'] for q in followup['cases']} == EXPECTED
    assert Counter(q['contract'] for q in peeling['B_source_controls']) == Counter({q: 16 for q in EXPECTED})
    for group, order_key, edge_key, name_key, rows_key in (
            (followup['cases'], 'collar_C', 'edges', 'id', 'row_order'),
            (peeling['B_source_controls'], 'original_C_names', None, 'contract', 'B_row_order')):
        for q in group:
            source = old_queries[q[name_key]]
            assert q[order_key] == source['boundary_order']
            assert q['e'] == source['extras'] and q['target'] == source['target']
            assert [list(map(int, w)) for w in q[rows_key]] == old['outer_pattern_order']
            graph_edges = q[edge_key] if edge_key else q['graph']['edges']
            collar_vertices = set(source['boundary_order']) | {f'b{i}' for i in range(5)}
            induced = [e for e in graph_edges if set(e) <= collar_vertices]
            assert edges(induced) == edges(source['collar_edges'])
            assert q['sigma'] == 1023
    return dict(schema='c8-no4ct-integrated-v1',
                contract='global minimum k outside K, then maximum edges; same original B and full relation',
                targets=[932, 933, 941], queries=rows, query_count=105,
                exclusions=97, residuals=8, status_counts=dict(sorted(tally.items())),
                source_932={'h_min': 4, 'n5_min': 10, 'unbounded_exclusion': 'OPEN'},
                common_bounds={'k_min': 16, 'h_min': 3, 'n5_min': 9},
                h3_bound={'k_min': 19, 'strict_C8_interior_min': 11,
                          'apex_H_degree_min': 4},
                downstream_binding={'apex_full_results_identical': True,
                                    'm9_original_collars': 8, 'm10_original_collars': 128},
                actual_source_status='not triggered', general_theorem='OPEN',
                four_colour_theorem_assumed=False, new_Lean_theorem=False)


def verify(data, expected):
    assert data == expected, 'complete integration ledger mismatch'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    expected = build()
    path = HERE / 'RESULTS.json'
    if args.write:
        with path.open('x') as stream:
            json.dump(expected, stream, indent=2)
            stream.write('\n')
    else:
        verify(read(path), expected)
    rejected = []
    if args.negative:
        for label, modify in (
                ('false complete closure', lambda d: d.update(residuals=0)),
                ('raise common h', lambda d: d['common_bounds'].update(h_min=4)),
                ('missing named query', lambda d: d['queries'].pop()),
                ('silently assume 4CT', lambda d: d.update(four_colour_theorem_assumed=True))):
            bad = copy.deepcopy(expected)
            modify(bad)
            try:
                verify(bad, expected)
            except AssertionError:
                rejected.append(label)
            else:
                raise AssertionError('accepted corrupted ledger: ' + label)
    print(json.dumps(dict(status='PASS', exclusions=97, residuals=8,
                          downstream_binding=expected['downstream_binding'],
                          negative_rejected=rejected), sort_keys=True))


if __name__ == '__main__':
    main()
