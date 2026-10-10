#!/usr/bin/env python3
"""Exclusive-create this audit's exact payload and actual read-only replay receipt."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SEAL_FILES = ('seal-checks/before.json', 'seal-checks/after.json',
              'seal-checks/normal.stdout.log', 'seal-checks/normal.stderr.log',
              'seal-checks/seed17.stdout.log', 'seal-checks/seed17.stderr.log',
              'seal-checks/corrupt.stdout.log', 'seal-checks/corrupt.stderr.log',
              'seal-checks/corrupt.sha256', 'seal-checks/commands.json', 'seal-checks/receipt.json')
EXCLUDED = {'MANIFEST.sha256', 'delivery.json', *SEAL_FILES}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def data(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def put(name, raw):
    path = HERE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as file:
        file.write(raw)


def state():
    assert not any(p.is_symlink() for p in HERE.rglob('*'))
    return {p.relative_to(HERE).as_posix(): sha(p.read_bytes())
            for p in sorted(HERE.rglob('*')) if p.is_file() and p.relative_to(HERE).as_posix() not in EXCLUDED}


def main():
    before = state()
    raw = ''.join(digest + '  ' + name + '\n' for name, digest in before.items()).encode()
    put('MANIFEST.sha256', raw)
    put('seal-checks/before.json', data(before))
    commands = []
    for label, seed in [('normal', None), ('seed17', '17'), ('corrupt', None)]:
        command = [sys.executable, '-B', str(HERE / 'verify.py'), '--payload-only']
        if label == 'corrupt':
            changed = ('0' if raw[:1] != b'0' else '1').encode() + raw[1:]
            put('seal-checks/corrupt.sha256', changed)
            command += ['--manifest', str(HERE / 'seal-checks/corrupt.sha256')]
        env = os.environ.copy()
        if seed is not None:
            env['PYTHONHASHSEED'] = seed
        run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
        put('seal-checks/' + label + '.stdout.log', run.stdout)
        put('seal-checks/' + label + '.stderr.log', run.stderr)
        expected = 2 if label == 'corrupt' else 0
        commands.append({'label': label, 'command': command, 'cwd': str(ROOT),
                         'environment': {'PYTHONHASHSEED': seed}, 'expected_exit': expected,
                         'actual_exit': run.returncode, 'stdout_sha256': sha(run.stdout),
                         'stderr_sha256': sha(run.stderr)})
        assert run.returncode == expected, label + ': ' + run.stderr.decode()
    after = state()
    assert before == after, 'payload mutated'
    assert (HERE / 'seal-checks/normal.stdout.log').read_bytes() == (HERE / 'seal-checks/seed17.stdout.log').read_bytes()
    assert 'payload digest differs' in (HERE / 'seal-checks/corrupt.stderr.log').read_text()
    put('seal-checks/after.json', data(after))
    put('seal-checks/commands.json', data({'commands': commands, 'normal_seed17_bytes_equal': True}))
    bound = {name: sha((HERE / name).read_bytes()) for name in SEAL_FILES if name != 'seal-checks/receipt.json'}
    receipt = {'task': 'N45-H1R', 'manifest_sha256': sha(raw), 'files': bound,
               'exact_relative_paths': True, 'nested_same_name_metadata_in_payload': True}
    put('seal-checks/receipt.json', data(receipt))
    bound['seal-checks/receipt.json'] = sha((HERE / 'seal-checks/receipt.json').read_bytes())
    delivery = {'task': 'N45-H1R', 'BASE': 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744',
                'manifest_file': 'MANIFEST.sha256', 'manifest_sha256': sha(raw),
                'payload_files': len(before), 'seal_files': bound,
                'receipt_file': 'seal-checks/receipt.json',
                'judgment_sha256': sha((HERE / 'independent-judgment.json').read_bytes()),
                'decision': 'accept_HIGH1_full_contract_paper_with_BASE_and_external_trust',
                'finite_source': 'not established; not executed; no trigger count', 'new_Lean': False,
                'general_N2_E': 'OPEN'}
    put('delivery.json', data(delivery))
    run = subprocess.run([sys.executable, '-B', str(HERE / 'verify.py')], cwd=ROOT, capture_output=True)
    assert run.returncode == 0, run.stderr.decode()
    print(run.stdout.decode().strip())
    print(json.dumps({'manifest_sha256': sha(raw), 'payload_files': len(before),
                      'receipt_bound_metadata': len(bound), 'full_final_exit': run.returncode}, sort_keys=True))


if __name__ == '__main__':
    main()
