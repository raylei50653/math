#!/usr/bin/env python3
"""Final read-only drift/seal/ledger verification across this acceptance wave."""
import hashlib
import json
from pathlib import Path
import stat
import subprocess

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TASKS = ['2026-10-11-n45-s-long-s-t2-q0-restore', '2026-10-11-n45-s-long-s-t2-q2-restore',
         '2026-10-11-n45-s-long-s-block-transfer', '2026-10-11-n45-s-long-s-t1-rfibre']
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'


def read(path):
    return json.loads(path.read_bytes())


def pin(path):
    assert stat.S_ISREG(path.lstat().st_mode)
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def tree(root):
    records = {}
    todo = [root]
    while todo:
        d = todo.pop()
        for p in sorted(d.iterdir()):
            name = p.relative_to(root).as_posix()
            mode = p.lstat().st_mode
            if stat.S_ISDIR(mode):
                records[name + '/'] = {'type': 'directory'}; todo.append(p)
            elif stat.S_ISREG(mode):
                records[name] = {'type': 'regular', **pin(p)}
            else:
                raise AssertionError('special or symlink: ' + str(p))
    return records


def main():
    guards, originals, seals = {}, [], []
    for task in TASKS:
        target = REPO / 'audits' / task
        review = REPO / 'audits' / (task + '-review')
        baseline = read(review / 'custody-before.json')
        assert tree(target) == baseline['target_tree'], 'original target drift: ' + task
        key = 'authority_and_old_certificate_files' if task.endswith('q0-restore') else 'guarded_original_files'
        for name, record in baseline[key].items():
            assert name not in guards or guards[name] == record
            guards[name] = record
        assert read(review / 'checks.json')['checks_pass']
        acceptance = read(review / 'acceptance.json')
        assert acceptance['base'] == BASE and not acceptance['shared_documents_updated']
        bound = next(p for p in acceptance['reviewed_worker_files'] if p['path'] == str((target / 'delivery.json').relative_to(REPO)))
        assert all(pin(target / 'delivery.json')[k] == bound[k] for k in ('bytes', 'sha256'))
        originals.append({'task': task, 'delivery': pin(target / 'delivery.json'), 'entire_tree_zero_drift': True})
        if review != HERE:
            delivery = read(review / 'delivery.json')
            payload = delivery['payload']
            current = tree(review)
            regular = {name: rec for name, rec in current.items() if rec['type'] == 'regular'}
            names = [p['path'] for p in payload]
            assert len(names) == len(set(names)) == delivery['payload_files']
            assert set(regular) == set(names) | {'delivery.json'}
            assert sorted(n[:-1] for n in current if n.endswith('/')) == delivery['directories']
            for p in payload:
                assert all(regular[p['path']][k] == p[k] for k in ('bytes', 'sha256'))
            seals.append({'review': str(review.relative_to(REPO)), 'delivery': pin(review / 'delivery.json'), 'exact_payload_still_passes': True})
    for name, record in guards.items():
        assert pin(REPO / name) == record, 'authority/old certificate drift: ' + name
    for item in read(HERE / 'extra-authority-inputs.json')['inputs']:
        assert pin(REPO / item['path']) == pin(HERE / item['frozen_path']) == {k: item[k] for k in ('bytes', 'sha256')}
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    diff = subprocess.check_output(['git', 'diff', '--binary', 'HEAD'], cwd=REPO)
    assert head == BASE and not diff
    ledger = read(HERE / 'remaining-schedules.json')
    prior = read(REPO / 'audits/2026-10-11-n45-s-long-s-review/remaining-schedules.json')
    key = lambda r: (r['t_s'], r['beta_q'], r['SigmaG_orbit'], tuple(r['QG']))
    assert len(ledger['excluded_schedules']) == len({key(r) for r in ledger['excluded_schedules']}) == 28
    assert {key(r) for r in ledger['excluded_schedules']} == {key(r) for r in prior['raw_schedules']}
    assert ledger['remaining_schedules'] == [] and ledger['counts']['remaining'] == 0
    for row in ledger['excluded_schedules']:
        original = next(r for r in prior['raw_schedules'] if key(r) == key(row))
        for field in ('Delta', 'QX', 'F_C_beta', 'F_U_beta', 'beta_literal', 'original_e', 'original_r_split', 's_spoke_domain', 'all_Delta_X_lifts_required_r'):
            assert row[field] == original[field], 'original schedule coordinate changed: ' + field
    assert read(REPO / 'audits/2026-10-11-n45-s-long-s-block-transfer-review/acceptance.json')['new_source_exclusions'] == 0
    print(json.dumps({'status': 'final wave drift, prior seals and exact raw-domain closure pass',
                      'base': BASE, 'tracked_diff_bytes': 0, 'original_deliveries': originals,
                      'guarded_distinct_original_files_union': len(guards), 'guarded_files_drift': [],
                      'prior_review_seals': seals, 'raw_schedules': 28, 'excluded_schedules': 28,
                      'this_wave_assigned_schedules': 24, 'this_wave_spoke_combinations': 38,
                      'remaining_schedules': 0, 'general_closure_or_source_execution_claimed': False}, sort_keys=True))


if __name__ == '__main__':
    main()
