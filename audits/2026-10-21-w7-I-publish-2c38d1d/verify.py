#!/usr/bin/env python3
"""Verify the unchanged Type-I research snapshot and its direct replay inputs."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, why):
    if not ok:
        raise ValueError(why)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=HERE.parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    inventory = json.loads((HERE / 'evidence-before.json').read_text())
    require(inventory['base'] == '2c38d1dcb4490017312467deb19d9da02b7bb2a6',
            'publication BASE changed')
    expected_source = set()
    source_root = inventory['source_root']
    for row in inventory['source_dependency_records']:
        path = Path(row['path'])
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe source path')
        target = repo / path
        require(target.is_file() and not target.is_symlink(), 'missing regular source: ' + str(path))
        data = target.read_bytes()
        require(len(data) == row['bytes'] and sha256(data).hexdigest() == row['sha256'],
                'source bytes changed: ' + str(path))
        if row['path'].startswith(source_root + '/'):
            expected_source.add(row['path'])
    actual_source = {str(p.relative_to(repo)) for p in (repo / source_root).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    require(actual_source == expected_source, 'research snapshot census changed')
    require(len(expected_source) == inventory['research_snapshot_files'] == 51,
            'research snapshot coverage changed')
    require(not inventory['new_source_pair_exclusions'] and not inventory['new_source_realizations'],
            'publication promoted source status')
    print(json.dumps({'result': 'PASS', 'research_snapshot_files': len(expected_source),
                      'source_dependency_records': len(inventory['source_dependency_records']),
                      'source_dependency_bytes': inventory['source_dependency_bytes'],
                      'original_bytes_changed': 0, 'new_source_pair_exclusions': 0,
                      'new_source_realizations': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
