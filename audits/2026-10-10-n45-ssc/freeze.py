#!/usr/bin/env python3
"""Exclusive byte freeze for the N45-SSC integrity audit; no worker code runs."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
WORKER = ROOT / 'audits/2026-10-10-n45-u-ss'
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def write_new(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != raw:
            raise RuntimeError('partial freeze drift: ' + str(path))
        return
    with path.open('xb') as stream:
        stream.write(raw)

def main():
    inventory = {}
    symlinks = {}
    for path in sorted(WORKER.rglob('*')):
        if path.is_symlink():
            rel = path.relative_to(WORKER).as_posix()
            target = str(path.readlink())
            symlinks[rel] = target
            dest = OUT / 'frozen/worker' / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.is_symlink():
                os.symlink(target, dest)
            elif str(dest.readlink()) != target:
                raise RuntimeError('partial symlink freeze drift: ' + rel)
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(WORKER).as_posix()
        raw = path.read_bytes()
        write_new(OUT / 'frozen/worker' / rel, raw)
        inventory[rel] = {'sha256': digest(raw), 'bytes': len(raw)}
    inputs = json.loads((WORKER / 'inputs.json').read_bytes())['inputs']
    inputs += json.loads((WORKER / 'inputs-additional.json').read_bytes())
    current, base, commands = [], [], []
    for item in inputs:
        if 'frozen' not in item:
            continue
        if item['layer'] == 'BASE-git-blob':
            argv = ['git', 'show', BASE + ':' + item['path']]
            result = subprocess.run(argv, cwd=ROOT, capture_output=True)
            log = 'freeze-logs/base-' + str(len(base)).zfill(2)
            write_new(OUT / (log + '.stdout.log'), result.stdout)
            write_new(OUT / (log + '.stderr.log'), result.stderr)
            commands.append({'argv': argv, 'cwd': str(ROOT), 'exit_code': result.returncode,
                             'stdout': log + '.stdout.log', 'stderr': log + '.stderr.log'})
            if result.returncode:
                raise RuntimeError('git object unavailable: ' + item['path'])
            write_new(OUT / 'frozen/base-object' / item['path'], result.stdout)
            base.append({'path': item['path'], 'sha256': digest(result.stdout), 'bytes': len(result.stdout)})
        else:
            raw = (ROOT / item['path']).read_bytes()
            write_new(OUT / 'frozen/live-current' / item['path'], raw)
            current.append({'path': item['path'], 'sha256': digest(raw), 'bytes': len(raw)})
    for key, argv in [('head', ['git', 'rev-parse', 'HEAD']),
                      ('initial-diff', ['git', 'diff', '--binary']),
                      ('initial-cached-diff', ['git', 'diff', '--cached', '--binary']),
                      ('initial-visible-paths', ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'])]:
        result = subprocess.run(argv, cwd=ROOT, capture_output=True)
        log = 'freeze-logs/' + key
        write_new(OUT / (log + '.stdout.log'), result.stdout)
        write_new(OUT / (log + '.stderr.log'), result.stderr)
        commands.append({'argv': argv, 'cwd': str(ROOT), 'exit_code': result.returncode,
                         'stdout': log + '.stdout.log', 'stderr': log + '.stderr.log'})
    record = {'task': 'N45-SSC', 'base': BASE, 'worker': str(WORKER.relative_to(ROOT)),
              'worker_files': inventory, 'worker_file_count': len(inventory), 'worker_symlinks': symlinks,
              'current': current, 'base_objects': base, 'commands': commands}
    write_new(OUT / 'freeze.json', (json.dumps(record, indent=2, sort_keys=True) + '\n').encode())
    print(json.dumps({'worker_file_count': len(inventory), 'current_count': len(current),
                      'base_object_count': len(base), 'freeze_sha256': digest((OUT / 'freeze.json').read_bytes())}, sort_keys=True))

if __name__ == '__main__':
    main()
