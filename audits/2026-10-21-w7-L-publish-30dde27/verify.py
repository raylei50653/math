#!/usr/bin/env python3
"""Preserve original W7 evidence and replay with its exact historical routing.

Current documentation is checked separately.  This overlay changes no original
checker, certificate or live file.  Restore the audit archive before replay.
"""
import argparse
import gzip
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROUTING = {'docs/HANDOFF.md', 'docs/STATUS.md', 'docs/c5_kempe_guide.md'}
PREFIX = 'audits/2026-10-21-w7-'
COMMANDS = {
    'root': [PREFIX + 'L-path-30dde27/check.py'],
    'integrated': [PREFIX + 'L-path-30dde27/integrate.py'],
    'single': [PREFIX + 'single-barrier-30dde27/independent_caps.py'],
    'mixed': [PREFIX + 'k1-mixed-30dde27/integrate.py'],
    'full-E': [PREFIX + 'k1-mixed-30dde27/full_exterior.py'],
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_bytes())


def original_bytes(path, archive):
    live = ROOT / path
    if live.is_file():
        return live.read_bytes()
    require(path in archive['files'], 'missing source; restore audit archive: ' + path)
    entry = archive['files'][path]
    return gzip.decompress((ROOT / archive['blobs'][entry['sha256']]['path']).read_bytes())


def custody():
    base = load(HERE / 'BASE.json')
    evidence = load(HERE / 'evidence-before.json')
    archive = load(ROOT / 'audits/ARCHIVE.json')
    before = json.loads(gzip.decompress((HERE / 'ARCHIVE-before.json.gz').read_bytes()))
    for key in ('files', 'blobs'):
        require(all(archive[key].get(path) == value for path, value in before[key].items()),
                'an older archive record changed: ' + key)
    for row in evidence['files']:
        raw = original_bytes(row['path'], archive)
        require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                'original audit bytes changed: ' + row['path'])
    selection = load(HERE / 'archive-selection.json')['paths']
    for path in selection:
        record = archive['files'][path]
        blob = archive['blobs'][record['sha256']]
        compressed = (ROOT / blob['path']).read_bytes()
        require(sha256(compressed).hexdigest() == blob['sha256'] and len(compressed) == blob['bytes'],
                'new archive gzip changed')
        raw = gzip.decompress(compressed)
        require(sha256(raw).hexdigest() == record['sha256'] and len(raw) == record['bytes'],
                'new archive original bytes changed')
    mathematical = set()
    routing = {}
    for audit in base['connected_audit_roots']:
        manifest = load(ROOT / audit / 'BASE.json')
        for row in manifest['inputs']:
            path = row['path']
            if path in ROUTING:
                raw = (HERE / 'routing-before' / path).read_bytes()
                require(sha256(raw).hexdigest() == row['sha256'], 'historical routing pin changed')
                routing[path] = {'before_sha256': row['sha256'],
                                 'current_sha256': sha256((ROOT / path).read_bytes()).hexdigest(),
                                 'current_equals_before': (ROOT / path).read_bytes() == raw}
            else:
                raw = original_bytes(path, archive)
                require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                        'non-routing authority changed: ' + path)
                mathematical.add(path)
    return {'result': 'PASS', 'original_audit_files': len(evidence['files']),
            'original_audit_bytes': evidence['total_bytes'],
            'nonrouting_authorities_unchanged': len(mathematical),
            'historical_routing_pins': routing,
            'old_archive_records_unchanged': True, 'new_archive_paths': selection,
            'new_archive_original_bytes': sum(archive['files'][p]['bytes'] for p in selection)}


def overlay(destination):
    roots = set(load(HERE / 'BASE.json')['connected_audit_roots'])
    for source in ROOT.iterdir():
        if source.name not in ('audits', 'docs', 'README.md'):
            (destination / source.name).symlink_to(source, target_is_directory=source.is_dir())
    for dirname in ('audits', 'docs'):
        target = destination / dirname
        target.mkdir()
        for source in (ROOT / dirname).iterdir():
            relative = str(source.relative_to(ROOT))
            if relative in roots:
                shutil.copytree(source, target / source.name,
                                ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            elif relative in ROUTING:
                shutil.copyfile(HERE / 'routing-before' / relative, target / source.name)
            else:
                (target / source.name).symlink_to(source, target_is_directory=source.is_dir())
    shutil.copyfile(HERE / 'routing-before/README.md', destination / 'README.md')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', choices=COMMANDS, action='append', default=[])
    parser.add_argument('--seed17', action='store_true')
    parser.add_argument('--log-dir', type=Path)
    args = parser.parse_args()
    result = custody()
    if args.replay:
        require(args.log_dir is not None, '--log-dir is required for replay')
        args.log_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='w7-publication-replay-') as directory:
            mirror = Path(directory)
            overlay(mirror)
            outcomes = []
            for name in args.replay:
                command = ['python3', '-B'] + (['-O'] if args.seed17 else []) + COMMANDS[name]
                env = os.environ | {'PYTHONDONTWRITEBYTECODE': '1'}
                if args.seed17:
                    env['PYTHONHASHSEED'] = '17'
                with (args.log_dir / (name + '.stdout')).open('x') as out, \
                     (args.log_dir / (name + '.stderr')).open('x') as err:
                    run = subprocess.run(command, cwd=mirror, env=env, stdout=out, stderr=err)
                outcomes.append({'name': name, 'command': command, 'exit_code': run.returncode})
                require(run.returncode == 0, 'historical-routing replay failed: ' + name)
            result['temporary_historical_routing_replays'] = outcomes
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
