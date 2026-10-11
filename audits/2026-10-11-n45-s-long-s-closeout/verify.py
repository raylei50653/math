#!/usr/bin/env python3
"""Read-only closeout guard; validates sealed evidence, not paper soundness."""
import argparse
import hashlib
import json
from pathlib import Path
import stat

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def key(item):
    return item['t_s'], item['SigmaG_orbit'], tuple(item['QG']), item['beta_q']


def check():
    before = json.loads((HERE / 'custody-before.json').read_bytes())
    observed_files, observed_dirs = set(), set()
    for name in before['protected_roots']:
        directory = ROOT / name
        for path in [directory, *directory.rglob('*')]:
            relative = path.relative_to(ROOT).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                observed_dirs.add(relative)
            elif stat.S_ISREG(mode):
                observed_files.add(relative)
            else:
                raise AssertionError('special entry: ' + relative)
    assert observed_dirs == set(before['protected_directories'])
    assert observed_files == {p['path'] for p in before['protected_files']}
    for pin in before['protected_files']:
        path = ROOT / pin['path']
        raw = path.read_bytes()
        assert len(raw) == pin['bytes'], pin['path']
        assert hashlib.sha256(raw).hexdigest() == pin['sha256'], pin['path']
        assert stat.S_IMODE(path.lstat().st_mode) == pin['mode'], pin['path']

    prefix = ROOT / 'audits'
    first = json.loads((prefix / '2026-10-11-n45-s-long-s-review/remaining-schedules.json').read_bytes())
    final = json.loads((prefix / '2026-10-11-n45-s-long-s-t1-rfibre-review/remaining-schedules.json').read_bytes())
    raw_keys = [key(s) for s in first['raw_schedules']]
    excluded_keys = [key(s) for s in final['excluded_schedules']]
    assert len(raw_keys) == len(set(raw_keys)) == 28
    assert len(excluded_keys) == len(set(excluded_keys)) == 28
    assert set(raw_keys) == set(excluded_keys)
    assert final['remaining_schedules'] == []
    assert final['counts']['remaining'] == 0
    assert final['counts']['this_dispatch_wave_schedules'] == 24
    assert final['counts']['this_dispatch_wave_spoke_combinations'] == 38
    assert sum(len(s['s_spoke_domain']) for s in first['remaining_schedules']) == 38
    groups = [first['excluded_schedules']]
    for suffix, count in [('t2-q0-restore-review', 3), ('t2-q2-restore-review', 7), ('t1-rfibre-review', 14)]:
        ledger = json.loads((prefix / ('2026-10-11-n45-s-long-s-' + suffix) / 'remaining-schedules.json').read_bytes())
        assert len(ledger['newly_excluded_schedules']) == count
        groups.append(ledger['newly_excluded_schedules'])
    assert [len(g) for g in groups] == [4, 3, 7, 14]
    partition = [key(s) for group in groups for s in group]
    assert len(set(partition)) == len(partition) == 28
    assert set(partition) == set(raw_keys)
    assert final['D_new_source_exclusions'] == 0
    d = json.loads((prefix / '2026-10-11-n45-s-long-s-block-transfer-review/acceptance.json').read_bytes())
    assert d['new_source_exclusions'] == 0
    t1 = json.loads((prefix / '2026-10-11-n45-s-long-s-t1-rfibre-review/T1-coverage-corrections.json').read_bytes())
    assert t1['counts']['new_X_empty'] == 352
    assert t1['counts']['new_G_empty_total'] == 780
    assert t1['counts']['changed_fields_total'] == 1132
    q2 = json.loads((prefix / '2026-10-11-n45-s-long-s-t2-q2-restore-review/q2-coverage-corrections.json').read_bytes())
    assert q2['scope']['genuine_unknown_to_empty_cells'] == 112
    print(json.dumps({'status': 'pass', 'protected_roots': len(before['protected_roots']),
                      'protected_files': len(observed_files), 'protected_bytes': sum(p['bytes'] for p in before['protected_files']),
                      'partition': [4, 3, 7, 14], 'raw_schedules': 28, 'remaining': 0,
                      'wave_schedules': 24, 'wave_spoke_queries': 38, 'D_new_source_exclusions': 0,
                      'paper_soundness_or_general_closure_checked': False}, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.parse_args()
    check()
