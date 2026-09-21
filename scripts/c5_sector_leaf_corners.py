#!/usr/bin/env python3
"""Audit marked corner orders, not candidate graphs or colorings."""
import argparse
from hashlib import sha256
from itertools import permutations, combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / 'artifacts/c5_sector_leaf_reduction/observations.json'
OUT = ROOT / 'artifacts/c5_sector_leaf_corners/observations.json'
LEAVES = {'1', '4', 'b', 'p', 'q', 'r'}


def contour(rot):
    start = ('1', 'zero')
    dart = start
    seen, word = [], []
    while dart not in seen:
        seen.append(dart)
        u, v = dart
        if u in LEAVES:
            word.append(u)
        around = rot[v]
        dart = (v, around[(around.index(u) + 1) % len(around)])
    assert dart == start and len(seen) == 14
    assert set(word) == LEAVES and len(word) == 6
    return tuple(word)


def alternating(word, first, second):
    a, b = sorted(word.index(v) for v in first)
    return sum(a < word.index(v) < b for v in second) == 1


def build():
    upstream = json.loads(UPSTREAM.read_text())
    for name, expected in upstream['input_sha256'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    rotations = {}
    for left in permutations(('4', 'b', 'w')):
        for right in permutations(('p', 'q', 'r')):
            rot = {'zero': ['1', *left], 'w': ['zero', *right]}
            rot.update({v: ['zero' if v in {'1', '4', 'b'} else 'w'] for v in sorted(LEAVES)})
            word = contour(rot)
            assert word not in rotations
            rotations[word] = rot
    assert len(rotations) == 36
    records = []
    for tail in permutations(('b', 'p', 'q', 'r')):
        word = ('1', '4', *tail)
        tree_ok = word in rotations
        assert tree_ok == (tail[0] == 'b' or tail[-1] == 'b')
        # Insert the retained frame path. All other entries are selected corners,
        # not a claim that these are the only occurrences of their vertices.
        expanded = ('1', '2', '3', '4', *tail)
        paths = {'A': ('1', 'q'), 'B': ('4', 'r'), 'P': ('3', 'p')}
        crossings = [list(pair) for pair in combinations(paths, 2)
                     if alternating(expanded, paths[pair[0]], paths[pair[1]])]
        old_ok = ['A', 'B'] not in crossings
        records.append(dict(corners=list(word), tree_insertable=tree_ok,
                            tree_rotation=rotations.get(word),
                            disjoint_path_endpoints=paths, alternating_pairs=crossings,
                            old_sides_compatible=old_ok,
                            retained=tree_ok and not crossings))
    retained = [r['corners'] for r in records if r['retained']]
    assert retained == [['1', '4', 'b', 'r', 'p', 'q'],
                        ['1', '4', 'r', 'p', 'q', 'b']]
    summary = dict(marked_orders=24, tree_rotations=36,
                   tree_insertable=sum(r['tree_insertable'] for r in records),
                   after_old_sides=sum(r['tree_insertable'] and r['old_sides_compatible'] for r in records),
                   after_p_to_3=len(retained))
    assert summary == dict(marked_orders=24, tree_rotations=36, tree_insertable=12,
                           after_old_sides=6, after_p_to_3=2)
    inputs = {UPSTREAM, Path(__file__).resolve()}
    inputs.update(ROOT / name for name in upstream['input_sha256'])
    return dict(schema=1,
                scope='Corner-order and tree-rotation audit only; retained orders are not sector realizations.',
                input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
                summary=summary, cases=records, retained=retained,
                closure_effect=dict(profile_deletions=0, inherited_profiles=603, fixed_point_recomputed=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
