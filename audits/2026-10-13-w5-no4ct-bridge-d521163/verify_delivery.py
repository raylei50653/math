#!/usr/bin/env python3
"""Read-only verification of this bridge package's own delivery seal."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    seal = json.loads((ROOT / 'DELIVERY.json').read_text())
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts
              and p.name != 'DELIVERY.json'}
    assert actual == {row['path'] for row in seal['files']}, 'delivery path drift'
    for row in seal['files']:
        data = (ROOT / row['path']).read_bytes()
        assert len(data) == row['bytes'], row['path']
        assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
    print(json.dumps({'status': 'PASS', 'base': seal['base'],
                      'files': len(actual), 'delivery_drift': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
