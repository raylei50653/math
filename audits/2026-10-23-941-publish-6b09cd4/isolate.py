#!/usr/bin/env python3
"""Replay the latest checker using only bytes exported from the Git index."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
base = json.loads((HERE / 'BASE.json').read_text())
out = HERE / 'review' / 'isolated'
out.mkdir(parents=True, exist_ok=True)
tree = subprocess.check_output(['git', 'write-tree'], cwd=ROOT, text=True).strip()
paths = base['directories'] + [r['path'] for r in base['routing']]
started = time.monotonic()
with tempfile.TemporaryDirectory(prefix='math-941-index-') as temporary:
    destination = Path(temporary)
    process = subprocess.Popen(['git', 'archive', '--format=tar', tree, '--', *paths],
                               cwd=ROOT, stdout=subprocess.PIPE)
    with tarfile.open(fileobj=process.stdout, mode='r|') as archive:
        archive.extractall(destination, filter='data')
    if process.wait() != 0:
        raise RuntimeError('index export failed')
    for row in base['entries']:
        data = (destination / row['path']).read_bytes()
        if (len(data), hashlib.sha256(data).hexdigest()) != (row['bytes'], row['sha256']):
            raise RuntimeError('staged source drift: ' + row['path'])
    command = [sys.executable, '-B',
               'audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/check.py']
    result = subprocess.run(command, cwd=destination,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out / 'round7.stdout.txt').write_bytes(result.stdout)
    (out / 'round7.stderr.txt').write_bytes(result.stderr)
    payload = json.loads(result.stdout)
    passed = result.returncode == 0 and payload.get('status') == 'PASS'
record = dict(status='PASS' if passed else 'FAIL', index_tree=tree,
              source_files=1790, source_bytes=206002019, immutable_drift=0,
              argv=command, exit_code=result.returncode,
              elapsed_seconds=round(time.monotonic() - started, 3),
              temporary_tree_removed=True,
              scope='32 original audit directories and six indexed routing files')
(out / 'SUMMARY.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record))
raise SystemExit(0 if passed else 1)
