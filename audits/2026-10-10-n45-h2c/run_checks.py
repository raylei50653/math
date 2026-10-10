#!/usr/bin/env python3
"""Exclusive audit streams/receipts; only explicit read-only worker commands."""
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
WORKER = ROOT / 'audits/2026-10-10-n45-s-high2'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def encoded(x):
    return (json.dumps(x, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def snapshot():
    return {p.relative_to(WORKER).as_posix(): {'kind': 'regular' if stat.S_ISREG(p.lstat().st_mode) else 'other',
            'bytes': p.lstat().st_size, 'mode': stat.S_IMODE(p.lstat().st_mode), 'sha256': sha(p.read_bytes())}
            for p in sorted(WORKER.rglob('*')) if p.is_file() or p.is_symlink()}


def run(item):
    name, command, seed, stdin_path = item
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    env.pop('PYTHONHASHSEED', None)
    if seed:
        env['PYTHONHASHSEED'] = seed
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    before = time.monotonic()
    inp = stdin_path.read_bytes() if stdin_path else None
    r = subprocess.run(command, cwd=ROOT, env=env, input=inp, capture_output=True)
    rec = {'name': name, 'command': command, 'cwd': str(ROOT), 'exit': r.returncode,
           'started_UTC': started, 'elapsed_seconds': round(time.monotonic() - before, 3),
           'environment': {k: env[k] for k in ['PYTHONDONTWRITEBYTECODE', 'GIT_OPTIONAL_LOCKS']},
           'stdout_path': name + '.stdout.txt', 'stderr_path': name + '.stderr.txt',
           'stdout_sha256': sha(r.stdout), 'stderr_sha256': sha(r.stderr)}
    if seed:
        rec['environment']['PYTHONHASHSEED'] = seed
    if stdin_path:
        rec.update({'stdin_path': str(stdin_path.relative_to(OUT)), 'stdin_sha256': sha(inp)})
    for suffix, b in [('.stdout.txt', r.stdout), ('.stderr.txt', r.stderr), ('.receipt.json', encoded(rec))]:
        with (OUT / 'runs' / (name + suffix)).open('xb') as f:
            f.write(b)
    return {'name': name, 'exit': r.returncode, 'stdout_sha256': sha(r.stdout),
            'stderr_sha256': sha(r.stderr), 'elapsed_seconds': rec['elapsed_seconds']}


def main():
    (OUT / 'runs').mkdir()
    (OUT / 'negative').mkdir()
    before = snapshot()
    with (OUT / 'worker-tree-before.json').open('xb') as f:
        f.write(encoded(before))
    bad_cert = OUT / 'negative/bad-certificate.json'
    with bad_cert.open('xb') as f:
        f.write((WORKER / 'certificate.json').read_bytes() + b'\n')
    bad_inputs = OUT / 'negative/bad-inputs.json'
    wrong = json.loads((WORKER / 'inputs-final.json').read_text())
    wrong['inputs'][0]['sha256'] = '0' * 64
    with bad_inputs.open('xb') as f:
        f.write(encoded(wrong))
    bad_manifest = OUT / 'negative/formal-manifest-with-nested-omission.json'
    manifest = json.loads((WORKER / 'manifest.json').read_text())
    del manifest['payload']['negative/nested/receipt.json']
    with bad_manifest.open('xb') as f:
        f.write(encoded(manifest))
    checker = ['python3', '-B', str(WORKER / 'checker.py')]
    seal = ['python3', '-B', str(WORKER / 'seal.py')]
    items = [
        ('checker-normal', checker + ['--check'], None, None),
        ('checker-seed17', checker + ['--check'], '17', None),
        ('seal-normal', seal + ['--check-delivery'], None, None),
        ('seal-seed17', seal + ['--check-delivery'], '17', None),
        ('wrong-certificate', checker + ['--check', '--certificate', str(bad_cert)], None, None),
        ('wrong-input-index', checker + ['--check', '--inputs', str(bad_inputs)], None, None),
        ('nested-receipt-omission', seal + ['--check-inventory-stdin'], None, bad_manifest),
        ('wrong-receipt-binding', ['python3', '-B', str(OUT / 'negative_receipt_probe.py')], None, None),
        ('outside-custody', ['python3', '-B', str(WORKER / 'verify_local.py')], None, None),
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, items))
    after = snapshot()
    with (OUT / 'worker-tree-after.json').open('xb') as f:
        f.write(encoded(after))
    result = {'executions': results, 'worker_tree_byte_mode_identity': before == after,
              'worker_regular_files': len(before), 'worker_tree_before_sha256': sha(encoded(before)),
              'worker_tree_after_sha256': sha(encoded(after)),
              'expected_exits': [0, 0, 0, 0, 2, 2, 2, 2, 1]}
    for first, second in [('checker-normal', 'checker-seed17'), ('seal-normal', 'seal-seed17')]:
        assert (OUT / 'runs' / (first + '.stdout.txt')).read_bytes() == (OUT / 'runs' / (second + '.stdout.txt')).read_bytes()
        assert (OUT / 'runs' / (first + '.stderr.txt')).read_bytes() == (OUT / 'runs' / (second + '.stderr.txt')).read_bytes()
    with (OUT / 'actual-checks.json').open('xb') as f:
        f.write(encoded(result))
    print(json.dumps(result, sort_keys=True))
    assert before == after
    assert [r['exit'] for r in results] == result['expected_exits']


if __name__ == '__main__':
    main()
