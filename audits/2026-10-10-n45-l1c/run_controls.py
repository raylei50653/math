#!/usr/bin/env python3
"""Write only this audit's logs and synthetic negative controls; never worker files."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORKER = ROOT / 'audits/2026-10-10-n45-s-low1'


def record(label, argv, expected_exit, expected_error='', env_overrides=None):
    env_overrides = env_overrides or {}
    process = subprocess.run(argv, cwd=ROOT, env=os.environ | env_overrides, capture_output=True)
    (HERE / 'logs' / f'{label}.stdout.log').write_bytes(process.stdout)
    (HERE / 'logs' / f'{label}.stderr.log').write_bytes(process.stderr)
    reason = expected_error in process.stderr.decode() if expected_error else not process.stderr
    row = dict(id=label, argv=argv, cwd=str(ROOT), env_overrides=env_overrides,
               exit_code=process.returncode, expected_exit=expected_exit,
               expected_rejection=expected_error, rejection_reason_matches=reason,
               stdout=f'logs/{label}.stdout.log', stderr=f'logs/{label}.stderr.log',
               stdout_sha256=hashlib.sha256(process.stdout).hexdigest(),
               stderr_sha256=hashlib.sha256(process.stderr).hexdigest())
    records.append(row)
    return process


def save(relative, text):
    path = HERE / 'controls' / relative
    path.write_text(text)
    return str(path)


def json_control(relative, obj):
    return save(relative, json.dumps(obj, sort_keys=True, indent=2) + '\n')


records = []
checker = ['python3', '-B', str(HERE / 'checker.py')]
normal = record('normal', checker, 0)
seeded = record('seed17', checker, 0, env_overrides={'PYTHONHASHSEED': '17'})
lines = (WORKER / 'MANIFEST.final-v4.sha256').read_text().splitlines()
corrupted = lines.copy()
corrupted[0] = ('0' if corrupted[0][0] != '0' else '1') + corrupted[0][1:]
tests = [
    ('corrupt-digest', '--manifest', save('corrupt-digest.sha256', '\n'.join(corrupted) + '\n'),
     '[payload-digests]: manifest digest differs:'),
    ('omit-payload-path', '--manifest', save('omit-payload-path.sha256', '\n'.join(lines[1:]) + '\n'),
     '[payload-inventory]: manifest payload inventory differs'),
    ('duplicate-payload-path', '--manifest', save('duplicate-payload-path.sha256', '\n'.join(lines + [lines[0]]) + '\n'),
     '[payload-inventory]: duplicate manifest path:'),
    ('unsafe-payload-path', '--manifest', save('unsafe-payload-path.sha256', '\n'.join([('0' * 64) + '  ../outside'] + lines[1:]) + '\n'),
     '[payload-inventory]: unsafe path:'),
]
links = json.loads((WORKER / 'symlinks.json').read_text())
first = sorted(links)[0]
links[first] += '-wrong-target'
tests.append(('wrong-symlink-target', '--symlinks', json_control('wrong-symlink-target.json', links),
              '[symlink-identities]: payload symlink identities differ'))
receipt = json.loads((WORKER / 'delivery.json').read_text())
first = sorted(receipt['seal_files'])[0]
omitted = json.loads(json.dumps(receipt))
del omitted['seal_files'][first]
tests.append(('unbound-receipt-file', '--receipt', json_control('unbound-receipt-file.json', omitted),
              '[receipt-inventory]: receipt exact metadata inventory differs'))
corrupt_receipt = json.loads(json.dumps(receipt))
corrupt_receipt['seal_files'][first] = '0' * 64
tests.append(('wrong-receipt-digest', '--receipt', json_control('wrong-receipt-digest.json', corrupt_receipt),
              '[receipt-digests]: receipt digest differs:'))
for label, flag, path, reason in tests:
    record(label, checker + [flag, path], 2, reason)
record('worker-live-after-new-directories', ['python3', '-B', str(WORKER / 'verify.py')], 2,
       'pre-existing workspace inventory differs')
checks = dict(task='N45-L1C', commands=records, normal_seed17_stdout_byte_equal=normal.stdout == seeded.stdout,
              own_negative_controls=len(tests), own_negative_scope='artifact integrity only; no finite source control',
              all_exits_and_rejection_stages_match=all(x['exit_code'] == x['expected_exit'] and x['rejection_reason_matches'] for x in records),
              worker_strict_live_failure_expected_because='fresh supervisory and reviewer directories change the exact Git inventory',
              checked_worker_scope='frozen artifact, BASE blobs, frozen current pins, sealed receipts and historical logs; current whole-worktree recursive hash not asserted')
(HERE / 'checks.json').write_text(json.dumps(checks, sort_keys=True, indent=2) + '\n')
if not checks['all_exits_and_rejection_stages_match'] or not checks['normal_seed17_stdout_byte_equal']:
    print(json.dumps(checks, sort_keys=True))
    raise SystemExit(1)
print(json.dumps({'task':'N45-L1C','commands':len(records),'own_negative_controls':len(tests),
                  'actual_exits_and_rejection_stages_match':True,'normal_seed17_byte_equal':True},sort_keys=True))
