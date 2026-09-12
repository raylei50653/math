#!/usr/bin/env python3
"""Independent, labelled 4^n replay of JSON certificates and deterministic search checks."""
import hashlib
import itertools as it
import json
from pathlib import Path
from search_boundary import COLORINGS, REPS, canonical, normalize

root = Path('artifacts/boundary')
summary = json.loads((root/'summary.json').read_text())
assert len(COLORINGS) == 240 and len(REPS) == 10
assert len({canonical(c) for c in COLORINGS}) == 2
lines = (root/'bad_certificates.jsonl').read_text().splitlines()
for line in lines:
    c = json.loads(line)
    digest = c.pop('sha256')
    assert hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest() == digest
    actual = {a[:5] for a in it.product(range(4),repeat=c['n'])
              if all(a[u] != a[v] for u,v in c['edges'])}
    assert actual == set(map(tuple,c['sigma']))
    assert actual and all(len(set(a))==4 for a in actual)
    assert set(map(tuple,c['color_orbits'])) == {normalize(a) for a in actual}
    assert set(map(tuple,c['dihedral_orbits'])) == {canonical(a) for a in actual}
    raw = sum(1 << i for i,b in enumerate(COLORINGS) if b in actual)
    assert format(raw,'060x') == c['sigma_bits_hex']
w = summary['composition_witness']
left = {c for c in COLORINGS if all(c[u]!=c[v] for u,v in w['left'])}
right = {c for c in COLORINGS if all(c[u]!=c[v] for u,v in w['right'])}
assert {canonical(c) for c in left} == {canonical(c) for c in right}
assert any(len(set(c))<=3 for c in left)
assert left & right and all(len(set(c))==4 for c in left & right)
mask = lambda s: sum(1 << i for i,b in enumerate(COLORINGS) if b in s)
assert mask(left & right) == mask(left) & mask(right)
print(f'Independent full-colouring replay: {len(lines)} certificates and composition witness passed')
