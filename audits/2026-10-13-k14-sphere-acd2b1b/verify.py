#!/usr/bin/env python3
"""Read-only input/delivery integrity; mathematical replays are separate."""
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
base = json.loads((HERE / 'BASE.json').read_text())
for name, digest in base['sha256'].items():
    assert hashlib.sha256((HERE / 'frozen' / name).read_bytes()).hexdigest() == digest, name
extra = json.loads((HERE / 'C8_INPUTS.json').read_text())
assert extra['base'] == base['base']
for name, entry in extra['inputs'].items():
    assert hashlib.sha256(gzip.decompress((HERE / entry['stored']).read_bytes())).hexdigest() == entry['sha256'], name
delivery = json.loads((HERE / 'DELIVERY.json').read_text())
for name, digest in delivery['sha256'].items():
    assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, name
assert sorted(p.as_posix() for p in (f.relative_to(HERE) for f in HERE.rglob('*') if f.is_file())
              if p.as_posix() != 'DELIVERY.json') == sorted(delivery['sha256']), 'delivery file set drift'
print(json.dumps(dict(status='PASS', frozen_inputs=len(base['sha256']) + len(extra['inputs']),
                      input_drift=0, delivery_files=len(delivery['sha256']),
                      new_Lean_theorem=False), sort_keys=True))
