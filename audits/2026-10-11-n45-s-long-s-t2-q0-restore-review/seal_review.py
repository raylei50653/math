#!/usr/bin/env python3
"""Seal/check an exclusive review tree. Existing delivery files never overwrite."""
import argparse
import hashlib
import json
from pathlib import Path
import stat


def inventory(root):
    files, dirs = {}, []
    assert stat.S_ISDIR(root.lstat().st_mode)
    todo = [root]
    while todo:
        directory = todo.pop()
        for path in sorted(directory.iterdir()):
            name = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                dirs.append(name)
                todo.append(path)
            elif stat.S_ISREG(mode):
                raw = path.read_bytes()
                files[name] = {'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
            else:
                raise AssertionError('symlink or special entry: ' + name)
    return files, sorted(dirs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--seal', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = args.directory.resolve()
    files, dirs = inventory(root)
    acceptance = json.loads((root / 'acceptance.json').read_bytes())
    delivery_path = root / 'delivery.json'
    if args.seal:
        assert 'delivery.json' not in files
        delivery = {'task_id': acceptance['task_id'], 'base': acceptance['base'],
                    'status': acceptance['status'], 'adoption_layer': 'exclusive audit review',
                    'metadata_exclusions': ['delivery.json'],
                    'metadata_exclusion_reason': 'self digest cannot be contained in its own payload manifest',
                    'directories': dirs, 'payload_files': len(files),
                    'payload_bytes': sum(item['bytes'] for item in files.values()),
                    'payload': [files[name] for name in sorted(files)]}
        with delivery_path.open('x') as stream:
            stream.write(json.dumps(delivery, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
        print(json.dumps({'sealed_payload_files': len(files), 'payload_bytes': delivery['payload_bytes'],
                          'delivery_sha256': hashlib.sha256(delivery_path.read_bytes()).hexdigest()}))
        return
    delivery = json.loads(delivery_path.read_bytes())
    assert delivery['metadata_exclusions'] == ['delivery.json']
    payload = delivery['payload']
    names = [item['path'] for item in payload]
    assert len(names) == len(set(names)) == delivery['payload_files']
    assert set(files) == set(names) | {'delivery.json'}
    assert delivery['directories'] == dirs
    assert delivery['payload_bytes'] == sum(item['bytes'] for item in payload)
    for item in payload:
        assert files[item['path']] == item, 'digest mismatch: ' + item['path']
    assert all(delivery[key] == acceptance[key] for key in ('task_id', 'base', 'status'))
    print(json.dumps({'status': 'exact review payload passes', 'payload_files': len(payload),
                      'delivery_sha256': files['delivery.json']['sha256']}))


if __name__ == '__main__':
    main()
