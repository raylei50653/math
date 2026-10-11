#!/usr/bin/env python3
"""Exclusive-create or read-only check of either new independent review tree."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIRECTORIES = {'batch': HERE, 'joint': HERE.parent / '2026-10-11-n45-s-long-s-joint-review'}
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'


def inventory(root):
    files, directories = [], []
    for path in sorted(root.rglob('*')):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError('unexpected symlink: ' + name)
        if path.is_dir():
            directories.append(name)
        elif path.is_file():
            if name == 'delivery.json':
                continue
            raw = path.read_bytes()
            files.append({'path': name, 'bytes': len(raw), 'sha256': sha256(raw).hexdigest()})
        else:
            raise ValueError('unexpected special file: ' + name)
    return files, directories


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', choices=sorted(DIRECTORIES), required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--create', action='store_true')
    group.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = DIRECTORIES[args.directory]
    files, directories = inventory(root)
    expected = {'base': BASE, 'review_directory': root.name,
                'files': files, 'directories': directories, 'payload_files': len(files),
                'payload_bytes': sum(item['bytes'] for item in files),
                'metadata_exclusions': [{'path': 'delivery.json', 'reason': 'manifest self-hash recursion'}],
                'authority': 'independent review record; original worker deliveries remain immutable',
                'source_realization_or_Lean_established': False}
    path = root / 'delivery.json'
    if args.create:
        with path.open('xb') as stream:
            stream.write((json.dumps(expected, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode())
    if json.loads(path.read_bytes()) != expected:
        raise ValueError('review manifest or exact inventory mismatch')
    print(json.dumps({'directory': root.name, 'status': 'passes', 'payload_files': len(files),
                      'payload_bytes': expected['payload_bytes'],
                      'delivery_sha256': sha256(path.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
