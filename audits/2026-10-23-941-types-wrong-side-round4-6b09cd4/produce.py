#!/usr/bin/env python3
"""Exclusive-create the finite complete-star set-system certificate."""
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = '6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd'
OPTIONS = [[], ['T'], ['r'], ['s'], ['T', 'r'], ['T', 's']]
rows = []
for a, b in combinations_with_replacement(OPTIONS, 2):
    first = list(range(5-len(a)))
    max_common = 2-len(set(a) & set(b))
    second = list(range(max_common)) + list(range(len(first), len(first)+5-len(b)-max_common))
    rows.append(dict(a=a, b=b, outside_sizes=[5-len(a), 5-len(b)],
                     max_common=max_common, minimum_union=8-len(set(a) | set(b)),
                     witness=[first, second], reservoir_offset=10-len(set(a) | set(b))))
cert = dict(schema='941-two-complete-M2-stars-v1', base=BASE,
            ordered_gamma=['r','T','s','x','h','W','e','d'],
            degree_lower_bound=5, rows=rows, q_minimum=2,
            reservoir_bound='q+7', exterior_bound='q+7+t', spectator_minimum=1,
            source_controls='not triggered', whole_type_exclusions=0,
            global_k_lower_bound=23)
with (HERE/'pair-star-certificate.json').open('x') as f:
    json.dump(cert, f, indent=2, sort_keys=True)
    f.write('\n')
print(json.dumps({'status':'created', 'pair_cases':len(rows)}))
