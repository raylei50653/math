#!/usr/bin/env python3
"""Read-only frozen-input/output custody check for this exclusive audit."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

AUDIT = Path(__file__).resolve().parents[1]
ROOT = AUDIT.parents[1]
ROUTING = {'docs/STATUS.md', 'docs/c5_kempe_guide.md', 'docs/c5_c4_triangle_core.md'}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    base = json.loads((AUDIT/'BASE.json').read_text())
    head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    assert head == base['head'], 'HEAD changed after audit freeze'
    frozen = 0
    allowed_drift = []
    for name in ('BASE.json', 'ADDITIONAL_INPUTS.json', 'SOURCE_G_INPUT.json'):
        for entry in json.loads((AUDIT/name).read_text())['inputs']:
            rel, expected = entry['path'], entry['sha256']
            assert digest(AUDIT/'frozen'/rel) == expected, f'frozen drift: {rel}'
            if digest(ROOT/rel) != expected:
                assert rel in ROUTING, f'live mathematical input drift: {rel}'
                allowed_drift.append(rel)
            frozen += 1
    manifest = json.loads((AUDIT/'MANIFEST.json').read_text())
    for entry in manifest['outputs']:
        assert digest(AUDIT/entry['path']) == entry['sha256'], entry['path']
    print(json.dumps({'status':'PASS', 'head':head, 'frozen_inputs':frozen,
                      'sealed_outputs':len(manifest['outputs']),
                      'allowed_routing_drift':sorted(set(allowed_drift)),
                      'mathematical_input_drift':0}, sort_keys=True))


if __name__ == '__main__':
    main()
