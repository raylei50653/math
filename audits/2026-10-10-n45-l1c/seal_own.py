#!/usr/bin/env python3
"""Seal only this new audit directory; never writes a worker or shared path."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(relative, obj):
    (HERE / relative).write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')


def payload():
    records = {}
    for path in HERE.rglob('*'):
        relative = path.relative_to(HERE).as_posix()
        if relative in {'MANIFEST.sha256', 'delivery.json'} or relative.startswith('seal-checks/'):
            continue
        if path.is_symlink():
            raise ValueError(f'own payload unexpectedly has symlink: {relative}')
        if path.is_file():
            records[relative] = sha(path)
    return dict(sorted(records.items()))


if (HERE / 'MANIFEST.sha256').exists() or (HERE / 'delivery.json').exists():
    raise SystemExit('refusing to reseal an existing audit')
seal = HERE / 'seal-checks'
seal.mkdir(exist_ok=False)
before = payload()
(HERE / 'MANIFEST.sha256').write_text(''.join(f'{value}  {relative}\n' for relative, value in before.items()))
write('seal-checks/payload-before.json', before)
commands = []
outputs = []
for label, env_overrides in [('normal', {}), ('seed17', {'PYTHONHASHSEED': '17'})]:
    argv = ['python3', '-B', str(HERE / 'checker.py')]
    process = subprocess.run(argv, cwd=ROOT, env=os.environ | env_overrides, capture_output=True)
    (seal / f'{label}.stdout.log').write_bytes(process.stdout)
    (seal / f'{label}.stderr.log').write_bytes(process.stderr)
    commands.append(dict(id=label, argv=argv, cwd=str(ROOT), env_overrides=env_overrides,
                         exit_code=process.returncode, expected_exit=0,
                         stdout=f'seal-checks/{label}.stdout.log', stderr=f'seal-checks/{label}.stderr.log'))
    outputs.append(process.stdout)
after = payload()
write('seal-checks/payload-after.json', after)
if before != after or any(row['exit_code'] != 0 for row in commands) or outputs[0] != outputs[1]:
    raise SystemExit('independent audit sealing checks failed; preserve all bytes and investigate')
write('seal-checks/commands.json', dict(commands=commands, normal_seed17_stdout_byte_equal=True,
                                      payload_byte_drift=False, mathematical_proof=False))
metadata = {p.relative_to(HERE).as_posix(): sha(p) for p in sorted(seal.rglob('*')) if p.is_file()}
if len(metadata) != 7:
    raise SystemExit('unexpected independent audit seal metadata inventory')
write('delivery.json', dict(task='N45-L1C', base='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744',
                           sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                           manifest_file='MANIFEST.sha256', manifest_sha256=sha(HERE / 'MANIFEST.sha256'),
                           regular_payload_files=len(before), payload_symlinks=0,
                           manifest_scope='Every regular file except top-level MANIFEST.sha256, delivery.json and exact top-level seal-checks/ metadata; frozen nested worker receipts and manifests are included.',
                           seal_files=metadata, receipt_bound_metadata_files=7,
                           decision='ACCEPT_TOOL_ENVELOPE_WITH_NONBLOCKING_INDEX_FINDING',
                           finding_id='L1C-INDEX-01',
                           paper_math_adjudication='outside this audit; no mathematical theorem proved by tool',
                           new_finite_source_controls='not established or executed; no trigger count',
                           commit=False, push=False, PR=False, delegation=False, authored_shared_edits=0,
                           worker_mutators_executed=False,
                           normal_exit=0, seed17_exit=0, normal_seed17_stdout_byte_equal=True,
                           stop='Independent tool/artifact/coverage audit complete; leave mathematical adoption to the parent and paper auditors.'))
print(json.dumps(dict(task='N45-L1C', payload_files=len(before), payload_symlinks=0,
                      receipt_bound_metadata_files=7, manifest_sha256=sha(HERE / 'MANIFEST.sha256')),
                 sort_keys=True))
