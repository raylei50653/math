#!/usr/bin/env python3
"""Read-only authority drift verification; --write uses exclusive creation."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def calculate():
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    records = []
    for item in manifest['inputs']:
        frozen = HERE / 'frozen' / item['path']
        assert frozen.stat().st_size == item['bytes'], item['path']
        assert sha(frozen) == item['sha256'], 'frozen input drift: ' + item['path']
        live = ROOT / item.get('source_path', item['path'])
        live_sha = sha(live)
        if not item['routing']:
            assert live_sha == item['sha256'], 'mathematical input drift: ' + item['path']
        records.append({'path': item['path'], 'origin': item['origin'],
                        'routing': item['routing'], 'frozen_sha256': item['sha256'],
                        'live_sha256': live_sha, 'live_drift': live_sha != item['sha256']})
    return {'base': manifest['base'], 'frozen_inputs': len(records),
            'frozen_drift': 0, 'mathematical_drift': 0,
            'routing_drift': sum(v['live_drift'] for v in records if v['routing']),
            'files': records}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = calculate()
    if args.write:
        with (HERE / 'INPUT_DRIFT.json').open('x') as out:
            json.dump(result, out, indent=2)
            out.write('\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
