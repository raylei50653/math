#!/usr/bin/env python3
"""Read-only catalogue membership and original-B D5 pullback audit.

This supplements, and does not replace, the two complete colouring checkers.
Only the frozen BASE catalogue is used. --write creates evidence exclusively.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def canonical(row):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in row)


def calculate():
    metadata = json.loads((ROOT/'CATALOGUE_INPUT.json').read_text())
    raw = (ROOT/'frozen'/metadata['path']).read_bytes()
    assert len(raw) == metadata['bytes']
    assert hashlib.sha256(raw).hexdigest() == metadata['sha256']
    catalogue = json.loads(raw)
    rows = sorted({canonical(t) for t in itertools.product(range(4), repeat=5)
                   if all(t[i] != t[(i+1) % 5] for i in range(5))})
    assert len(rows) == 10 and list(map(list, rows)) == catalogue['pattern_order']
    masks = set(map(int, catalogue['cells']))
    assert len(masks) == 132
    actions = [[rows.index(canonical([beta[(offset+sign*i) % 5] for i in range(5)]))
                for beta in rows] for sign in (1, -1) for offset in range(5)]

    def transform(mask, action):
        return sum(1 << action[i] for i in range(10) if mask & (1 << i))

    assert all(transform(m, action) in masks for m in masks for action in actions)
    counts, by_component, by_radius = Counter(), Counter(), Counter()
    with gzip.open(ROOT/'controls/certificate.jsonl.gz', 'rt') as stream:
        header = json.loads(next(stream))
        assert header['base'] == metadata['base']
        assert header['beta_order'] == list(map(list, rows))
        for line in stream:
            graph = json.loads(line)
            assert [row['beta'] for row in graph['rows']] == list(map(list, rows))
            sigma = sum(1 << i for i, row in enumerate(graph['rows']) if row['wheel_full_lifts'])
            assert sigma == graph['Sigma'] and sigma in masks, graph['key']
            counts[sigma] += 1
            by_component[graph['counts']['c']] += 1
            by_radius[graph['counts']['r']] += 1
    return {'base': metadata['base'], 'status': 'triggered and holds',
            'completion': 'all necessary templates have complete Sigma in frozen K132',
            'templates': sum(counts.values()), 'masks': dict(sorted(counts.items())),
            'by_c': dict(sorted(by_component.items())), 'by_r': dict(sorted(by_radius.items())),
            'catalogue_sha256': metadata['sha256'], 'catalogue_size': len(masks),
            'D5_closed_all_132': True,
            'accepted_rows': {str(m): [''.join(map(str, rows[i])) for i in range(10) if m & (1 << i)]
                              for m in sorted(counts)},
            'pullback_masks': {str(m): sorted({transform(m, action) for action in actions})
                               for m in sorted(counts)},
            'representative_claim': 'none; direct membership completion',
            'R3_preservation_claim': False,
            'minimum_outside_catalogue_source': 'not triggered'}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = calculate()
    data = json.dumps(result, sort_keys=True, indent=2)+'\n'
    path = ROOT/'controls/catalogue.json'
    if args.write:
        with path.open('x') as out:
            out.write(data)
    else:
        assert path.read_text() == data
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
