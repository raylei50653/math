#!/usr/bin/env python3
"""Project one common necessary C8 support onto six fixed actual operations."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT/'kempe-consistency.json'
CATALOGUE = ROOT/'frozen/artifacts/c5_cells/cells.json'
data = json.loads(SOURCE.read_text())
catalogue = json.loads(CATALOGUE.read_text())
K = {int(mask) for mask in catalogue['cells']}
assert len(K) == 132
ROWS = ('01012', '01021', '01023', '01201', '01202', '01203', '01212', '01213', '01231', '01232')
NAMES = ('GA', 'GB', 'H', 'S', 'Q1', 'Q2')


def canonical(t):
    d = {}
    return ''.join(str(d.setdefault(x, len(d))) for x in t)


def bit(t):
    return 1 << ROWS.index(canonical(t))


records = []
for i, values in enumerate(data['tuples']):
    c = dict(zip(data['pin_order'], values))
    a, n, right, left, q, outer_c, x, y = [c[v] for v in data['pin_order']]
    contribution = dict.fromkeys(NAMES, 0)
    fan_a_proper = a not in {q, left, right}
    if fan_a_proper:
        contribution['H'] = bit((x, y, a, q, outer_c))
    lifts = []
    for b in range(4):
        if b in {a, outer_c, q}:
            continue
        row_bit = bit((x, y, a, b, outer_c))
        premises = {'GA': fan_a_proper, 'GB': b not in {n, left, right},
                    'S': q == n, 'Q1': n == b and q == right,
                    'Q2': n == b and b == left}
        for name, holds in premises.items():
            if holds:
                contribution[name] |= row_bit
        lifts.append({'b': b, 'row': canonical((x, y, a, b, outer_c)),
                      'candidate_membership': premises})
    records.append({'tuple_id': i, 'local_candidate_masks': contribution,
                    'all_b_assignments': lifts})

results = []
for result in data['results']:
    masks = dict.fromkeys(NAMES, 0)
    for i in result['surviving_ids']:
        for name in NAMES:
            masks[name] |= records[i]['local_candidate_masks'][name]
    assert all(mask in K for mask in masks.values())
    results.append({'original_mask': result['source_mask'],
                    'same_exterior_tuple_ids': result['surviving_ids'],
                    'candidate_masks': masks,
                    'all_candidate_masks_in_K132': True})

RESULT = {'scope': 'common Kempe-consistent boundary relation, not a realized plane exterior',
          'inputs': {'kempe_certificate_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                     'catalogue_sha256': hashlib.sha256(CATALOGUE.read_bytes()).hexdigest()},
          'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'rows': ROWS, 'complete_local_records': records, 'results': results,
          'smaller_bad_source_constructed': False}
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
parser.add_argument('--certificate', type=Path, default=ROOT/'candidate-projections.json')
args = parser.parse_args()
if args.check:
    assert json.loads(args.certificate.read_text()) == json.loads(json.dumps(RESULT))
else:
    with args.certificate.open('x') as f:
        f.write(json.dumps(RESULT, indent=2)+'\n')
print(json.dumps([{'original_mask': r['original_mask'], 'candidate_masks': r['candidate_masks']}
                  for r in results]))
