#!/usr/bin/env python3
"""Read-only identity check after publication; this is not a proof checker."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AUDIT = 'audits/2026-10-17-r6-joint-positive-113e41f'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(value):
    path = PurePosixPath(value)
    require(bool(path.parts) and not path.is_absolute() and '..' not in path.parts
            and path.as_posix() == value, 'invalid relative path: ' + value)
    return path


def local(value):
    path = ROOT
    for part in relative(value).parts:
        path /= part
        require(not path.is_symlink(), 'unexpected symlink: ' + value)
    return path


def read_preserved(value, archive):
    path = local(value)
    if path.exists():
        require(path.is_file(), 'not a regular file: ' + value)
        return path.read_bytes(), path.stat().st_mode & 0o777
    require(value in archive['files'], 'missing unarchived file: ' + value)
    record = archive['files'][value]
    blob = archive['blobs'][record['sha256']]
    packed = local(blob['path']).read_bytes()
    require(len(packed) == blob['bytes'] and digest(packed) == blob['sha256'],
            'compressed blob drift: ' + value)
    data = gzip.decompress(packed)
    require(len(data) == record['bytes'] and digest(data) == record['sha256'],
            'archived bytes drift: ' + value)
    return data, record['mode']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inventory', type=Path, default=HERE / 'initial-state.json')
    args = parser.parse_args()
    initial = json.loads(args.inventory.read_text())
    require(initial['audit_directory'] == AUDIT and initial['source_positivity'] == 'OPEN',
            'unexpected publication scope')
    expected = initial['audit_files']
    require(len(expected) == 359, 'incomplete publication inventory')
    archive = json.loads((ROOT / 'audits/ARCHIVE.json').read_text())
    actual = {p.relative_to(ROOT / AUDIT).as_posix()
              for p in (ROOT / AUDIT).rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    actual |= {p.removeprefix(AUDIT + '/') for p in archive['files']
               if p.startswith(AUDIT + '/')}
    require(actual == set(expected), 'audit membership drift')
    for rel, record in expected.items():
        relative(rel)
        data, mode = read_preserved(AUDIT + '/' + rel, archive)
        require(len(data) == record['bytes'] and digest(data) == record['sha256']
                and mode == record['mode'], 'audit identity drift: ' + rel)

    base = initial['research_base']
    subprocess.run(['git', 'merge-base', '--is-ancestor', base, 'HEAD'], cwd=ROOT, check=True)
    authority_count = 0
    for name in ('BASE.json', 'ADDITIONAL_INPUTS.json', 'ADDITIONAL_GEOMETRY_INPUTS.json'):
        manifest = json.loads((ROOT / AUDIT / name).read_text())
        require(manifest['base'] == base, 'authority BASE mismatch')
        for record in manifest['inputs']:
            rel = record['path']
            data, _ = read_preserved(AUDIT + '/frozen/' + rel, archive)
            historical = subprocess.check_output(['git', 'show', base + ':' + rel], cwd=ROOT)
            require(data == historical and digest(data) == record['sha256'],
                    'frozen or Git authority drift: ' + rel)
            if not record.get('routing', False):
                live, _ = read_preserved(rel, archive)
                require(digest(live) == record['sha256'], 'live mathematical input drift: ' + rel)
            authority_count += 1
    require(authority_count == 206, 'authority membership drift')

    for rel, record in initial['routing_at_research_delivery'].items():
        snapshot = HERE / relative(record['snapshot'])
        require(digest(snapshot.read_bytes()) == record['sha256'],
                'research-delivery routing snapshot drift: ' + rel)

    old_archive = json.loads(subprocess.check_output(
        ['git', 'show', base + ':audits/ARCHIVE.json'], cwd=ROOT))
    require(all(archive['files'][p] == v for p, v in old_archive['files'].items()),
            'old archive path changed')
    require(all(archive['blobs'][p] == v for p, v in old_archive['blobs'].items()),
            'old archive blob changed')
    print(json.dumps({'status': 'PASS', 'research_base': base, 'audit_files': len(expected),
                      'authority_inputs': authority_count, 'original_bytes_unchanged': True,
                      'source_positivity': 'OPEN', 'mathematical_proof_verifier': False},
                     sort_keys=True))


if __name__ == '__main__':
    main()
