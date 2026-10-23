#!/usr/bin/env python3
"""Read-only custody check for the exact connected publication source domain."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(path, record):
    data = path.read_bytes()
    require((len(data), hashlib.sha256(data).hexdigest()) ==
            (record['bytes'], record['sha256']), 'custody drift: ' + str(path))


def main():
    base = json.loads((HERE / 'BASE.json').read_text())
    require(base['base'] == '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd', 'BASE')
    require(len(base['directories']) == 32, 'source directories')
    expected = {r['path'] for r in base['entries']}
    require(len(expected) == len(base['entries']) == base['files'] == 1790,
            'complete source inventory')
    actual = {p.relative_to(ROOT).as_posix()
              for directory in base['directories']
              for p in (ROOT / directory).rglob('*')
              if p.is_file() and '__pycache__' not in p.parts}
    require(actual == expected, 'source file domain changed')
    for record in base['entries']:
        check(ROOT / record['path'], record)
    for record in base['routing']:
        check(HERE / 'entry' / record['path'], record)
    total = sum(r['bytes'] for r in base['entries'])
    require(total == base['bytes'] == 206002019, 'source byte total')
    # Publication may legitimately update live routing. Frozen source may not drift.
    routing_changed = []
    for record in base['routing']:
        if (ROOT / record['path']).read_bytes() != (HERE / 'entry' / record['path']).read_bytes():
            routing_changed.append(record['path'])
    indexed = set(subprocess.check_output(
        ['git', '-C', str(ROOT), 'ls-files', '-z']).decode().split('\0'))
    print(json.dumps(dict(status='PASS', source_directories=32, source_files=1790,
                          source_bytes=total, immutable_drift=0,
                          source_files_in_index=len(expected & indexed),
                          live_routing_changed=routing_changed), sort_keys=True))


if __name__ == '__main__':
    main()
