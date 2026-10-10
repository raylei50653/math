#!/usr/bin/env python3
"""Exclusive new audit seal; failed attempts must be preserved."""
import json
import os
from pathlib import Path
import subprocess
import sys

import checker
import verify

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as target:
        target.write(data)


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def main():
    for name in ('MANIFEST.sha256', 'delivery.json', 'receipt.json', 'receipt'):
        checker.require(not (HERE / name).exists(), 'seal already exists; preserve failed attempt: ' + name)
    regular, links = checker.inventory(HERE, verify.EXCLUDED)
    checker.require(not links, 'unexpected reviewer symlink')
    hashes = {relative: checker.digest(HERE / relative) for relative in regular}
    manifest = ''.join(f'{hashes[relative]}  {relative}\n' for relative in regular).encode()
    write(HERE / 'MANIFEST.sha256', manifest)
    records = []
    for name in ('normal', 'seed17'):
        command = [sys.executable, '-B', str(HERE / 'verify.py'), '--payload-only']
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        env.pop('PYTHONHASHSEED', None)
        if name == 'seed17':
            env['PYTHONHASHSEED'] = '17'
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
        for stream in ('stdout', 'stderr'):
            write(HERE / f'receipt/{name}.{stream}.log', getattr(result, stream))
        records.append({'name': name, 'command': command, 'cwd': str(ROOT),
                        'PYTHONHASHSEED': env.get('PYTHONHASHSEED'), 'exit_code': result.returncode,
                        'stdout': f'receipt/{name}.stdout.log', 'stderr': f'receipt/{name}.stderr.log'})
    checker.require(all(r['exit_code'] == 0 for r in records), 'seal checker failed; preserve logs and manifest')
    checker.require((HERE / 'receipt/normal.stdout.log').read_bytes() ==
                    (HERE / 'receipt/seed17.stdout.log').read_bytes(), 'seal seed output differs')
    files_after, links_after = checker.inventory(HERE, verify.EXCLUDED)
    checker.require(files_after == regular and not links_after, 'seal payload names changed')
    checker.require(all(checker.digest(HERE / relative) == hashes[relative] for relative in regular),
                    'seal payload bytes changed')
    manifest_sha = checker.digest(HERE / 'MANIFEST.sha256')
    receipt = {'commands': records,
               'metadata': {relative: checker.digest(HERE / relative) for relative in sorted(verify.LOGS)},
               'payload_before': manifest_sha, 'payload_after': manifest_sha,
               'scope': 'frozen artifact evidence; not current workspace inventory or mathematical proof'}
    write(HERE / 'receipt.json', json_bytes(receipt))
    delivery = {'task': 'N45-L2C', 'BASE': checker.BASE, 'manifest_sha256': manifest_sha,
                'receipt_sha256': checker.digest(HERE / 'receipt.json'),
                'payload_regular_files': len(regular), 'payload_symlinks': 0,
                'excluded_exact_paths': sorted(verify.EXCLUDED),
                'tool_verdict': 'ACCEPT_SCOPED_ARTIFACT_INTEGRITY',
                'mathematical_verdict': 'not evaluated by this audit',
                'source_controls': 'not established; not executed; no trigger count'}
    write(HERE / 'delivery.json', json_bytes(delivery))
    print(json.dumps({'sealed': True, 'payload_regular_files': len(regular), 'manifest_sha256': manifest_sha,
                      'receipt_sha256': delivery['receipt_sha256']}, sort_keys=True))


if __name__ == '__main__':
    main()
