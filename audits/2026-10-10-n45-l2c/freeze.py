#!/usr/bin/env python3
"""Exclusive reviewer capture; never import or run worker sealing code."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORKER = ROOT / 'audits/2026-10-10-n45-s-low2'
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as target:
        target.write(data)


def main():
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    assert head == BASE
    inventory = {}
    for path in sorted(WORKER.rglob('*')):
        relative = path.relative_to(WORKER).as_posix()
        assert not path.is_symlink(), relative
        if path.is_file():
            write(HERE / 'frozen/worker' / relative, path.read_bytes())
            inventory[relative] = {'sha256': digest(path), 'mode': stat.S_IMODE(path.stat().st_mode)}
    assert len(inventory) == 85
    initial = json.loads((WORKER / 'inputs-initial.json').read_text())
    pins = []
    for record in initial['pins']:
        actual = digest(ROOT / record['path'])
        assert actual == record['expected'] == record['actual']
        pins.append({'path': record['path'], 'expected': record['expected'], 'actual': actual})
    old = json.loads((WORKER / 'preexisting-files.json').read_text())
    counts = {k: 0 for k in ('file', 'symlink', 'directory', 'missing')}
    for relative, record in sorted(old.items()):
        path = ROOT / relative
        kind = record['kind']
        counts[kind] += 1
        if kind == 'file':
            assert path.is_file() and not path.is_symlink(), relative
            assert digest(path) == record['sha256'], relative
            assert stat.S_IMODE(path.stat().st_mode) == record['mode'], relative
        elif kind == 'symlink':
            assert path.is_symlink() and os.readlink(path) == record['target'], relative
        elif kind == 'directory':
            assert path.is_dir(), relative
        else:
            assert not path.exists() and not path.is_symlink(), relative
    for args, name in [(('diff', '--binary'), 'initial-tracked-diff'),
                       (('diff', '--cached', '--binary'), 'initial-cached-diff')]:
        actual = subprocess.check_output(['git', *args], cwd=ROOT)
        assert actual == (WORKER / f'logs/{name}.stdout.log').read_bytes(), name
    base_records = json.loads((WORKER / 'base-inputs.json').read_text())['inputs']
    for record in base_records:
        blob = subprocess.check_output(['git', 'show', BASE + ':' + record['path']], cwd=ROOT)
        obj = subprocess.check_output(['git', 'rev-parse', BASE + ':' + record['path']], cwd=ROOT).decode().strip()
        assert hashlib.sha256(blob).hexdigest() == record['sha256']
        assert obj == record['git_blob']
        assert blob == (WORKER / 'frozen/BASE' / record['path']).read_bytes()
    root_evidence = ROOT / 'audits/2026-10-10-n45-low2-supervision/initial-strict-replays.json'
    write(HERE / 'frozen/root-initial-strict-replays.json', root_evidence.read_bytes())
    for relative, record in inventory.items():
        assert digest(WORKER / relative) == record['sha256'], relative
    result = {'task': 'N45-L2C', 'BASE': BASE, 'head_at_capture': head,
              'worker_path': WORKER.relative_to(ROOT).as_posix(),
              'worker_full_inventory': inventory, 'worker_regular_files': 85,
              'worker_symlinks': 0, 'pins_independently_rehashed': pins,
              'BASE_objects_independently_verified': base_records,
              'preexisting_records_independently_rehashed': counts,
              'preexisting_tracking_diffs_byte_equal': True,
              'exact_live_git_inventory_repeated': False,
              'exact_live_inventory_reason': 'Parent and reviewers already added isolated audit directories; parent strict replays precede those additions.',
              'nested_repository_recursive_hash': False,
              'root_initial_evidence_sha256': digest(root_evidence),
              'capture_boundary': 'Old named files, modes, symlink identities and directory existence checked at capture; additions by parallel reviewers are permitted. Future replay checks frozen inputs only.'}
    write(HERE / 'inputs.json', (json.dumps(result, indent=2, sort_keys=True) + '\n').encode())
    print(json.dumps({'worker_files': len(inventory), 'pins': len(pins), 'BASE_objects': len(base_records), 'preexisting': counts}, sort_keys=True))


if __name__ == '__main__':
    main()
