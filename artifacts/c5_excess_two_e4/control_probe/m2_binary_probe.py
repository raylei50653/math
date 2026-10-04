#!/usr/bin/env python3
"""Fixed m=2 binary+singleton control probe (25000 named spoke choices).

Uses finite exact colouring and NetworkX disk checks from the adjacent probe
module, never a Four Colour Theorem oracle. Exclusive-create output; --check
replays the fixed finite experiment. Failure is not a general exclusion.
"""
import argparse
import json
from pathlib import Path

import networkx as nx
from m2_probe import B, REPS, T4, template

OUT = Path(__file__).resolve().with_suffix('.json')


def build():
    t = template('C_binary22_plus_singleton11', tuple(range(10)),
                 ((5, 7), (5, 8), (6, 7), (6, 8), (7, 8), (5, 9), (6, 9)),
                 ((5, 2), (6, 2), (7, 1), (8, 1), (9, 2)))
    return dict(schema='e4-nonadjacent-m2-binary-control-probe-v1', base_commit='2ac279b',
                scope='Only one fixed five-private m2 binary22/singleton11 interior; 25000 named spoke assignments.',
                no_four_color_theorem_oracle=True, networkx_version=nx.__version__,
                B=B, pattern_order=REPS, T4_indices=sorted(T4), template=t,
                positive_control_count=len(t['positive_controls']))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    result = build()
    data = (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()
    if args.check:
        assert OUT.read_bytes() == data
    else:
        with OUT.open('xb') as f:
            f.write(data)
    print(json.dumps(dict(counts=result['template']['counts'], controls=result['positive_control_count']), sort_keys=True))
    print('CHECK OK' if args.check else 'CREATED m2_binary_probe.json')


if __name__ == '__main__':
    main()
