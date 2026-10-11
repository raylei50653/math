#!/usr/bin/env python3
"""Read-only metadata/custody validation. Does not certify the paper proof."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', action='store_true')
    args = parser.parse_args()
    claims = json.loads((ROOT / 'claims.json').read_text())
    cov = json.loads((ROOT / 'coverage.json').read_text())
    checks = json.loads((ROOT / 'checks.json').read_text())
    assert claims['adoption_status'] == cov['adoption_status'] == '待獨立驗收'
    assert len(cov['schedules']) == cov['assigned_schedule_count'] == cov['paper_exclusion_count'] == 7
    assert cov['schedule_residual_count'] == 0
    all_ids = {c['id'] for c in claims['claims']}
    for claim in claims['claims']:
        for required in ['quantifier', 'premises', 'conclusion', 'conclusion_type',
                         'dependencies', 'original_coordinates']:
            assert claim[required], (claim['id'], required)
        assert claim['original_coordinates']['original_e'] == ['r', 'b4']
    expected_pairs = {('933', tuple(map(int, s))) for s in ['0123', '0124', '0234', '1234']}
    expected_pairs |= {('941', tuple(map(int, s))) for s in ['023', '024', '124']}
    assert {(s['Sigma_orbit'], tuple(s['QG'])) for s in cov['schedules']} == expected_pairs
    total = 0
    for schedule in cov['schedules']:
        assert schedule['Delta'] == [q for q in schedule['QG'] if q != 2]
        assert schedule['original_s_spoke_variants'] == [[0, 2]]
        assert not schedule['remaining_schedule_obligations']
        assert schedule['restored_rows']
        for proof in schedule['restored_rows']:
            assert proof['q'] in schedule['Delta'] and proof['claim'] in all_ids
            assert proof['pins'] == [0, 3] and proof['gamma_b4'] != 0
        assert len(schedule['all_ten_literal_obligations']) == 10
        for row in schedule['all_ten_literal_obligations']:
            assert row['gamma_b4'] == int(row['literal'][4])
            assert {(p['r'], p['s']) for p in row['pins']} == {(a, b) for a in range(4) for b in range(4)}
            assert len(row['pins']) == 16
            for p in row['pins']:
                assert p['diagonal'] == (p['r'] == p['s'])
                assert p['counts'] is None and p['all_preimages'] is None
            if row['q'] in schedule['Delta'] and row['q'] in [3, 4]:
                p = next(p for p in row['pins'] if [p['r'], p['s']] == [0, 3])
                assert p['contradiction']
            total += len(row['pins'])
    assert total == cov['ambient_symbolic_cells'] == 1120
    assert checks['calibration']['stdout_byte_equal']
    assert checks['target_source'] == {'executed': False, 'trigger_count': None, 'status': 'not triggered'}
    assert len(checks['negative_controls']) == 2
    assert all(n['native_exit'] != 0 for n in checks['negative_controls'])
    if args.manifest:
        delivery = json.loads((ROOT / 'delivery.json').read_text())
        assert delivery['adoption_status'] == '待獨立驗收'
        assert delivery['metadata_exclusions'] == ['delivery.json', 'seal-receipt.json']
        paths = {p['path'] for p in delivery['payload']}
        actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
                  if p.is_file() and p not in {ROOT / 'delivery.json', ROOT / 'seal-receipt.json'}}
        assert paths == actual, ('manifest set mismatch', sorted(paths ^ actual))
        for record in delivery['payload']:
            data = (ROOT / record['path']).read_bytes()
            assert len(data) == record['bytes']
            assert hashlib.sha256(data).hexdigest() == record['sha256']
        before = json.loads((ROOT / 'custody-before.json').read_text())
        after = json.loads((ROOT / 'custody-after.json').read_text())
        assert before['files'] == after['files']
        assert before['head'] == after['head']
        assert before['tracked_diff_sha256'] == after['tracked_diff_sha256']
    print(json.dumps({'status': 'passes', 'scope': 'metadata and byte custody only',
                      'schedules': 7, 'symbolic_pin_cells': total,
                      'manifest_checked': args.manifest, 'independent_acceptance': False}, sort_keys=True))


if __name__ == '__main__':
    main()
