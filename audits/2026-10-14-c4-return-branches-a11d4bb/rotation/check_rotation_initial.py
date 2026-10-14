#!/usr/bin/env python3
"""Check the full colour hypothesis before reusing a rotated return proof."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CELLS = ROOT / 'artifacts/c5_cells/cells.json'
COLOURS = tuple(range(4))


def canonical(word):
    names = {}
    return tuple(names.setdefault(v, len(names)) for v in word)


def calculate():
    cells = json.loads(CELLS.read_text())
    patterns = tuple(map(tuple, cells['pattern_order']))
    index = {p: i for i, p in enumerate(patterns)}
    singleton = {int(i): v for i, v in cells['singleton_of_three_colour'].items()}
    proper = [word for word in itertools.product(COLOURS, repeat=5)
              if all(word[i] != word[(i + 1) % 5] for i in range(5))]
    assert len(proper) == 240
    assert set(map(canonical, proper)) == set(patterns)
    records = []
    for mask in (932, 933, 941):
        support = [word for word in proper if mask >> index[canonical(word)] & 1]
        singletons = sorted(singleton[j] for j in singleton if mask >> j & 1)
        cuts = []
        for shift in range(5):
            order = tuple((shift + j) % 5 for j in range(5))
            moved = [tuple(word[j] for j in order) for word in support]
            # Direct target: a'=c', fixed proper outer triangle (z,x',y')=(0,1,2),
            # and b' is one of the two non-z triangle colours.
            target = sorted(word for word in moved
                            if word[2] == word[4] == 0 and word[:2] == (1, 2)
                            and word[3] in (1, 2))
            expected = sorted(j for j in (shift, (shift + 1) % 5) if j in singletons)
            assert len(target) == len(expected)
            transported = sum(1 << index[canonical(word)] for word in set(map(canonical, moved)))
            cuts.append({'edge_indices': [shift, (shift + 1) % 5],
                         'new_to_original': order, 'transported_mask': transported,
                         'positive_target_singletons': expected,
                         'fixed_triangle_target': target,
                         'return_failure_colour_premise': not target})
            for permutation in itertools.permutations(COLOURS):
                for word in moved:
                    assert canonical(tuple(permutation[c] for c in word)) == canonical(word)
        records.append({'original_mask': mask, 'positive_singletons': singletons, 'cuts': cuts})
    by_mask = {r['original_mask']: r for r in records}
    assert [r['edge_indices'][0] for r in by_mask[932]['cuts']
            if r['return_failure_colour_premise']] == [0, 1, 2, 3, 4]
    assert [r['edge_indices'][0] for r in by_mask[933]['cuts']
            if r['return_failure_colour_premise']] == [0, 1, 2]
    assert [r['edge_indices'][0] for r in by_mask[941]['cuts']
            if r['return_failure_colour_premise']] == [0]
    assert by_mask[941]['cuts'][2]['fixed_triangle_target']
    assert by_mask[933]['cuts'][3]['fixed_triangle_target']
    return {'scope': 'literal boundary colour transport; not source realization',
            'catalogue_sha256': hashlib.sha256(CELLS.read_bytes()).hexdigest(),
            'proper_labelled_boundary_words': len(proper), 'records': records,
            'negative_controls': ['941/ab has a positive target', '933/bc has a positive target'],
            'actual_target_sources': 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--create', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE / 'rotation.json')
    args = parser.parse_args()
    assert args.create != args.check, 'choose exactly one mode'
    value = calculate()
    if args.create:
        with args.certificate.open('x') as stream:
            json.dump(value, stream, indent=2)
            stream.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == value, 'certificate mismatch'
    print(json.dumps({'status': 'PASS', 'cuts': 15, 'actual_target_sources': 0}))


if __name__ == '__main__':
    main()
