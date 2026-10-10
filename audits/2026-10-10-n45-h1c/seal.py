#!/usr/bin/env python3
"""Exclusive H1C seal; precise receipt metadata exclusions, no basename filter."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import verify

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def data_json(x):
    return (json.dumps(x, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def put(path, data):
    with path.open('xb') as f:
        f.write(data)


def payload_inventory():
    files = {}
    for p in sorted(HERE.rglob('*')):
        assert not p.is_symlink(), p
        if p.is_file():
            name = p.relative_to(HERE).as_posix()
            if name not in verify.EXCLUDED:
                files[name] = sha(p)
    return files


def main():
    before = payload_inventory()
    manifest = ''.join(h + '  ' + name + '\n' for name,h in before.items()).encode()
    put(HERE / 'MANIFEST.sha256', manifest)
    folder = HERE / 'seal-checks'
    folder.mkdir(exist_ok=False)
    runs = []
    base_command = ['python3','-B','audits/2026-10-10-n45-h1c/verify.py','--payload-only']
    for label, expected, env in [('normal',0,{}), ('seed17',0,{'PYTHONHASHSEED':'17'}), ('bad-digest',2,{})]:
        command = list(base_command)
        stdin = None
        if label == 'bad-digest':
            command += ['--manifest-stdin']
            stdin = b'0' * 64 + manifest[64:]
        environment = os.environ.copy()
        environment.update(env)
        r = subprocess.run(command, cwd=ROOT, env=environment, input=stdin, capture_output=True)
        record = dict(id=label, command=command, cwd=str(ROOT), environment=env,
                      actual_exit=r.returncode, expected_exit=expected)
        for stream in ('stdout','stderr'):
            data = getattr(r,stream)
            name = 'seal-checks/' + label + '.' + stream + '.txt'
            put(HERE / name,data)
            record[stream + '_file'] = name
            record[stream + '_sha256'] = hashlib.sha256(data).hexdigest()
        if stdin is not None:
            record['stdin_text'] = stdin.decode()
            record['stdin_sha256'] = hashlib.sha256(stdin).hexdigest()
        put(folder / (label + '.json'), data_json(record))
        runs.append(record)
        assert r.returncode == expected, record
        if label == 'bad-digest':
            reject = json.loads(r.stderr)
            assert reject['stage'] == 'audit payload inventory' and 'digest differs' in reject['reason']
    assert (folder / 'normal.stdout.txt').read_bytes() == (folder / 'seed17.stdout.txt').read_bytes()
    assert (folder / 'normal.stderr.txt').read_bytes() == (folder / 'seed17.stderr.txt').read_bytes()
    assert payload_inventory() == before, 'payload changed during seal'
    receipt = dict(task='N45-H1C', manifest_sha256=sha(HERE / 'MANIFEST.sha256'),
                   payload_files=len(before), payload_before_after_identical=True, runs=runs,
                   scope='artifact integrity and fixed-domain calibration only; paper not adjudicated')
    put(folder / 'receipt.json', data_json(receipt))
    seal_files = {name:sha(HERE / name) for name in verify.SEAL_FILES}
    delivery = dict(task='N45-H1C', BASE='dc8e9aa7d6fccb51f63d30aa3f9c132296d44744',
                    decision='accepted_artifact_integrity_only', manifest_file='MANIFEST.sha256',
                    manifest_sha256=sha(HERE / 'MANIFEST.sha256'), payload_files=len(before),
                    seal_files=seal_files, independent_judgment_sha256=sha(HERE / 'independent-judgment.json'),
                    paper_mathematics='not adjudicated', finite_HIGH1_source='not established / not executed / no trigger count',
                    new_Lean=False, general_N2_E='OPEN')
    put(HERE / 'delivery.json', data_json(delivery))
    result = subprocess.run(['python3','-B','audits/2026-10-10-n45-h1c/verify.py'], cwd=ROOT, capture_output=True)
    assert result.returncode == 0, result.stderr.decode()
    assert payload_inventory() == before
    print(json.dumps(dict(status='sealed', payload_files=len(before), receipt_metadata_files=len(seal_files),
                          manifest_sha256=delivery['manifest_sha256'], full_receipt_check_exit=result.returncode), sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
