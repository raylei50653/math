#!/usr/bin/env python3
"""Independent final ledger check against all exact subcertificates."""
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def check(result):
    assert result['schema'] == 'c8-struct-final-results-v1'
    assert result['base'] == '243a125a80e4d8de40957f59d8da0bdbc974cf69'
    assert result['color_frame'] == [0, 1, 2, 3]
    assert result['excluded'] == 2 and result['residual'] == 8
    assert result['total_C8_excluded'] == 62 and result['total_C8_queries'] == 70
    assert result['h_lower_bound'] == 3 and result['n5_lower_bound'] == 9
    names = {'geometry/certificate.json', 'classification/classification.json',
             'classification/quotient.json', 'kempe/certificate.json'}
    assert set(result['source_certificates']) == names
    for name, digest in result['source_certificates'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest
    cone = json.loads((HERE / 'kempe/certificate.json').read_text())
    interface = json.loads((HERE / 'frozen/audits/2026-10-13-c8-joint-count-3097ef5/interface.json').read_text())
    cases = {c['id']: c for c in interface['cases']}
    source = {(q['case_id'], q['target']): q for q in cone['queries']}
    assert result['pattern_order'] == cone['pattern_order']
    assert result['outer_pattern_order'] == interface['outer_pattern_order']
    assert len(result['queries']) == 10
    assert {(q['case_id'], q['target']) for q in result['queries']} == set(source)
    excluded = []
    for q in result['queries']:
        key = q['case_id'], q['target']
        original = source[key]
        assert q['query_id'] == f'{key[0]}-{key[1]}'
        for field in ('extras', 'boundary_order', 'supports'):
            assert q[field] == original[field]
        assert q['collar_edges'] == cases[key[0]]['collar_edges']
        if key in {('c16', 941), ('c32', 941)}:
            assert q['status'] == 'proved' and q['result'] == 'source excluded'
            assert q['certificate'] == 'classification/quotient.json'
            assert q['proof'] == 'classification/QUOTIENT_PROOF.md'
            assert 'counts' not in q
            excluded.append(q['query_id'])
        else:
            assert q['status'] == 'necessary-condition residual' and q['result'] == 'source not excluded'
            for field in ('counts', 'partition_coefficients', 'orbit_coefficients', 'outer_counts', 'support'):
                assert q[field] == original[field]
            assert q['forced_zero_fibres'] == original['forced_zeros']
            assert q['support_size'] == original['support'].bit_count()
            assert q['count_denominator'] == math.lcm(*(Fraction(v).denominator for v in q['counts']))
            assert q['remaining_obligation']
    return {'status': 'PASS', 'excluded': excluded, 'complete_residual_vectors': 8}


if __name__ == '__main__':
    import copy
    data = json.loads((HERE / 'RESULTS.json').read_text())
    print(json.dumps(check(data), sort_keys=True))
    bad = copy.deepcopy(data)
    bad['excluded'] = 10
    try:
        check(bad)
    except AssertionError:
        print(json.dumps({'negative_control': 'false full closure', 'status': 'rejected'}, sort_keys=True))
    else:
        raise AssertionError('false full closure accepted')
