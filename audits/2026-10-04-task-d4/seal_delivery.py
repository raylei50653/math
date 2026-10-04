#!/usr/bin/env python3
"""Seal every D4 file, including frozen bytes and failed historical attempts."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=('seal', 'verify'))
    p.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    a = p.parse_args()
    root = a.directory.resolve()
    table = root / 'DELIVERY_SHA256.json'
    paths = {str(f.relative_to(root)): f for f in root.rglob('*') if f.is_file()
             and '__pycache__' not in f.parts and f.suffix != '.pyc' and f != table}
    if a.action == 'seal':
        assert not table.exists(), 'Do not replace a delivery seal'
        data = {rel: dict(sha256=digest(f), size=f.stat().st_size) for rel, f in sorted(paths.items())}
        table.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(dict(sealed_files=len(data), includes_snapshot_and_all_attempts=True)))
    else:
        data = json.loads(table.read_text())
        missing = sorted(set(data) - set(paths))
        added = sorted(set(paths) - set(data))
        changed = [rel for rel in data if rel in paths and
                   (digest(paths[rel]) != data[rel]['sha256'] or paths[rel].stat().st_size != data[rel]['size'])]
        result = dict(all_checks_passed=not missing and not added and not changed,
                      files_checked=len(data), missing=missing, added=added, changed=changed)
        print(json.dumps(result))
        assert result['all_checks_passed']


if __name__ == '__main__':
    main()
