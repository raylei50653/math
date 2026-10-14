#!/usr/bin/env python3
"""Finite cap control only; no target graph is supplied or fabricated."""
import itertools
import json

COLORS = range(4)
TYPES = ((0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 2, 1), (0, 1, 2, 3))
NAMES = ('ABAB', 'ABAC', 'ABCB', 'ABCD')
# Boundary vertices z,s,r,t = 0,1,2,3; cap vertices x,y = 4,5.
EDGES = ((0,1), (1,2), (2,3), (3,0),
         (0,4), (1,4), (2,4), (4,5), (0,5), (2,5), (3,5))
EXPECTED = (((2,3),(3,2)), ((2,1),(2,3),(3,1)), (), ((3,1),))
rows = []
for boundary, name, expected in zip(TYPES, NAMES, EXPECTED):
    # Direct full graph edge checker, independent of palette formulas.
    extensions = []
    for x,y in itertools.product(COLORS, repeat=2):
        coloring = boundary + (x,y)
        if all(coloring[a] != coloring[b] for a,b in EDGES):
            extensions.append((x,y))
    assert tuple(extensions) == expected
    palettes = sorted({tuple(sorted(xy)) for xy in extensions})
    # p,q are two marked internal pins making a triangle with z.
    # No unprovided edges incident to these pins are assumed.
    pq_rows = []
    for p,q in itertools.product(COLORS, repeat=2):
        if p == q or p == boundary[0] or q == boundary[0]:
            continue
        good = [xy for xy in extensions if set(xy) != {p,q}]
        pq_rows.append({'pq': [p,q], 'good_caps': [list(xy) for xy in good]})
        if name == 'ABAC':
            assert len(good) == 2
    rows.append({'type':name, 'boundary':list(boundary),
                 'extensions':[list(xy) for xy in extensions],
                 'palettes':[list(pair) for pair in palettes], 'pq_checks':pq_rows})

# The order is exactly the source-relative C4 table in
# audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md section 3.
source_masks = (7,10,11,12,13,14,15)
without_abac = [m for m in source_masks if not m & (1 << 1)]
assert without_abac == [12,13]
# Planar z=r quotient is separately certified colourable by source minimality.
# Therefore the C4 relation has ABAB or ABAC, i.e. one of bits zero/one.
after_quotient_nonempty = [m for m in without_abac if m & 0b0011]
assert after_quotient_nonempty == [13]

# Negative information control: an abstract joint relation on the four outer
# pins and p,q can have mask 13 and forbid every cap palette change.
# This is a compatibility relation, not a claimed realizable planar source.
abstract_joint = ((0, (2,3)), (2, (1,2)), (3, (1,3)))
for type_index, pq in abstract_joint:
    boundary = TYPES[type_index]
    assert pq[0] != pq[1] and boundary[0] not in pq
    for xy in EXPECTED[type_index]:
        assert set(xy) == set(pq)
assert sum(1 << i for i,_ in abstract_joint) == 13

from pathlib import Path
from hashlib import sha256
import argparse

result = {'status': 'PASS', 'type_order': NAMES, 'rows': rows,
          'source_masks': source_masks,
          'after_cap_multivalued_palette': without_abac,
          'after_source_relative_quotient': after_quotient_nonempty,
          'abstract_joint_negative_control': 'PASS; not a graph',
          'actual_target_source_controls': 0,
          'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
output = Path(__file__).with_name('cap.json')
payload = json.dumps(result, indent=2) + '\n'
if args.check:
    assert output.read_text() == payload, 'Cap certificate differs'
else:
    with output.open('x') as handle:
        handle.write(payload)
print(json.dumps({'ok': True, 'counts': [len(row['extensions']) for row in rows],
                  'pq_cases': sum(len(row['pq_checks']) for row in rows),
                  'remaining_mask': after_quotient_nonempty,
                  'actual_target_source_controls': 0}))
