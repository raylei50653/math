#!/usr/bin/env python3
"""Literal full-r-lift J predicate and its simultaneous marked-cycle screen."""
import argparse
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def partitions(items):
    if not items:
        yield ()
        return
    first, rest = items[0], items[1:]
    for tail in partitions(rest):
        yield ((first,),) + tail
        for i, block in enumerate(tail):
            yield tail[:i] + ((first,) + block,) + tail[i+1:]


def good(values):
    e, f, g = values
    return (e == f) == (e == g)


def all_r(row):
    m, v, w, z, p, q = row
    lifts = sorted(set(range(4)) - {m, v, w})
    assert len(lifts) == 1
    for r in lifts:
        if z == r:
            if {p, q} != set(range(4)) - {z, m}:
                return False, lifts
        elif not {p, q} & (set(range(4)) - {z, m, r}):
            return False, lifts
    return True, lifts


def build():
    for record in json.loads((HERE / 'INPUTS.json').read_text())['inputs']:
        for path in (ROOT / record['path'], HERE / 'frozen' / record['path']):
            assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'], str(path)
    edges = ((0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3))
    rows = []
    for row in product(range(4), repeat=6):
        if any(row[a] == row[b] for a, b in edges):
            continue
        m, v, w, z, p, q = row
        values = (v ^ w, p ^ q, m ^ z)
        accepted, lifts = all_r(row)
        bad1 = values[0] == values[1] != values[2]
        bad2 = values[0] == values[2] != values[1]
        assert accepted == good(values)
        assert bad1 == {p, q}.isdisjoint({v, w})
        assert bad2 == (z not in {v, w} and {p, q} != {v, w})
        assert not (bad1 and bad2)
        rows.append({'literal_row': row, 'edge_differences': values,
                     'all_r_lifts': lifts, 'source_allowed': accepted,
                     'E': bad1, 'additional_bad_event': bad2})
    assert len(rows) == 432
    assert sum(row['source_allowed'] for row in rows) == 240
    assert sum(row['E'] for row in rows) == sum(row['additional_bad_event'] for row in rows) == 96
    cubes = []
    for values in product((1, 2, 3), repeat=3):
        if not good(values):
            continue
        e, f, g = values
        for pair in combinations((1, 2, 3), 2):
            active = tuple(i for i, c in enumerate(values) if c in pair)
            for blocks in partitions(active):
                def same(a, b):
                    return any(a in block and b in block for block in blocks)
                safe = True
                if e == f == g and e in pair:
                    safe = same(1, 2)
                elif f == g and e != f and set(pair) == {e, f}:
                    safe = same(1, 2)
                elif len(set(values)) == 3:
                    if set(pair) == {e, f}:
                        safe = same(0, 1)
                    elif set(pair) == {e, g}:
                        safe = same(0, 2)
                targets = []
                for mask in range(1 << len(blocks)):
                    target = list(values)
                    for bit, block in enumerate(blocks):
                        if mask & (1 << bit):
                            for i in block:
                                target[i] ^= pair[0] ^ pair[1]
                    targets.append(target)
                bad_masks = [i for i, target in enumerate(targets) if not good(target)]
                assert safe == (not bad_masks)
                if bad_masks:
                    assert any(not good(targets[1 << i]) for i in range(len(blocks)))
                cubes.append({'marked_colours': values, 'pair': pair, 'blocks': blocks,
                              'all_targets': targets, 'source_safe': safe,
                              'forbidden_masks': bad_masks})
    assert len(cubes) == 117
    controls = []
    previous = json.loads((ROOT / 'audits/2026-10-15-six-pin-lifts-6ddea32/certificate.json').read_text())
    for control in previous['controls']:
        pins, vertices = control['pins'], control['vertices']
        classified = []
        for row in control['all_full_J_colourings']:
            colour = dict(zip(vertices, row))
            literal = tuple(colour[pins[c]] for c in 'mvwzpq')
            values = (literal[1] ^ literal[2], literal[4] ^ literal[5], literal[0] ^ literal[3])
            allowed, _ = all_r(literal)
            assert allowed == good(values)
            classified.append({'full_J_colouring': row, 'source_allowed': allowed,
                               'E': values[0] == values[1] != values[2],
                               'additional_bad_event': values[0] == values[2] != values[1]})
        controls.append({'name': control['name'], 'full_classification': classified,
                         'counts': {key: sum(row[key] for row in classified)
                                    for key in ('source_allowed', 'E', 'additional_bad_event')}})
    return {'schema': 'full-j-source-predicate-v1', 'status': 'PASS',
            'proper_rows': rows, 'combined_cycle_cubes': cubes, 'controls': controls,
            'scope': 'Exact J all-r necessary predicate, not a sufficient condition for the complete U source.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = json.loads(json.dumps(build()))
    if args.write:
        with args.write.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    else:
        assert json.loads(args.check.read_text()) == result, 'certificate mismatch'
    print(json.dumps({'status': result['status'], 'proper_rows': 432, 'allowed_rows': 240,
                      'E_rows': 96, 'additional_bad_rows': 96, 'combined_cubes': 117,
                      'controls': {c['name']: c['counts'] for c in result['controls']}}))


if __name__ == '__main__':
    main()
