#!/usr/bin/env python3
"""Independently verify the old fan cap and all fixed-boundary full lifts."""
import argparse
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--certificate', type=Path, default=HERE / 'singleton_cap.json')
args = parser.parse_args()
c = json.loads(args.certificate.read_text())

def norm(p):
    encountered = []
    out = []
    for color in p:
        if color not in encountered:
            encountered.append(color)
        out.append(encountered.index(color))
    return tuple(out)

patterns = sorted({norm(p) for p in product(range(4), repeat=7)
                   if all(p[i] != p[(i+1) % 7] for i in range(7))})
cycle = {tuple(sorted((i, (i+1) % 7))) for i in range(7)}
fan = cycle | {(0, i) for i in range(2, 6)}
assert c['vertex_count'] == 7 and c['boundary_order'] == list(range(7))
assert {tuple(sorted(e)) for e in c['edges']} == fan
assert c['bounded_faces'] == [[0, i, i+1] for i in range(1, 6)]
assert c['outer_face'] == [0, 6, 5, 4, 3, 2, 1]
assert len(c['rows']) == 91
mask = 0
for i, (p, record) in enumerate(zip(patterns, c['rows'])):
    accepted = all(p[a] != p[b] for a, b in fan)
    assert record == dict(index=i, boundary_row=list(p), accepted=accepted,
                          full_lifts=[list(p)] if accepted else [])
    if accepted:
        mask |= 1 << i
assert mask == c['full_relation_mask'] and mask.bit_count() == 16
assert c['accepted_indices'] == [i for i in range(91) if mask >> i & 1]
assert c['rejected_indices'] == [i for i in range(91) if not mask >> i & 1]
assert mask & c['upper_bound_mask'] == c['intersection_mask'] == 1 << 89
assert c['intersection_index'] == 89 and patterns[89] == (0, 1, 2, 3, 2, 3, 1)
print(json.dumps(dict(status='PASS', full_boundary_rows=91, accepted=16, rejected=75,
                     complete_fixed_boundary_lifts=16, unique_upper_intersection='0123231',
                     embedding='explicit fan triangulation', control_status='triggered and holds'), sort_keys=True))
