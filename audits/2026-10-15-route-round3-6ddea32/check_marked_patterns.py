#!/usr/bin/env python3
"""Independent local verification; imports no worker implementation."""
import argparse
from itertools import combinations, product
import json
from pathlib import Path


def partitions(items):
    if not items:
        yield ()
        return
    first, rest = items[0], items[1:]
    for tail in partitions(rest):
        yield ((first,),) + tail
        for i, block in enumerate(tail):
            yield tail[:i] + ((first,) + block,) + tail[i+1:]


def target(colours):
    e, f, g = colours
    return e == f and e != g


def check():
    # Literal order (m,v,w,z,p,q), retaining both triangles and the mz edge.
    edges = ((0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3))
    rows = []
    for row in product(range(4), repeat=6):
        if any(row[a] == row[b] for a, b in edges):
            continue
        m, v, w, z, p, q = row
        event = {p, q}.isdisjoint({v, w})
        delta = (v ^ w, p ^ q, m ^ z)
        assert event == target(delta)
        rows.append({'literal_colours': row, 'edge_differences': delta, 'event': event})
    assert len(rows) == 432 and sum(r['event'] for r in rows) == 96

    records = []
    for colours in product(range(3), repeat=3):
        if target(colours):
            continue
        e, f, g = colours
        for pair in combinations(range(3), 2):
            eligible = tuple(i for i, c in enumerate(colours) if c in pair)
            for blocks in partitions(eligible):
                def same(a, b):
                    return any(a in block and b in block for block in blocks)
                condition = True
                if e == f == g and e in pair:
                    condition = same(2, 0) or same(2, 1)
                elif e != f and set(pair) == {e, f}:
                    if g == e:
                        condition = same(0, 1) or same(0, 2)
                    elif g == f:
                        condition = same(1, 0) or same(1, 2)
                    else:
                        condition = same(0, 1)
                successors = []
                for mask in range(1 << len(blocks)):
                    result = list(colours)
                    for bit, block in enumerate(blocks):
                        if mask & (1 << bit):
                            for i in block:
                                result[i] = sum(pair) - result[i]
                    successors.append(tuple(result))
                safe = not any(map(target, successors))
                assert condition == safe, (colours, pair, blocks)
                # A single component already suffices whenever the cube can return.
                if not safe:
                    assert any(target(successors[1 << i]) for i in range(len(blocks)))
                records.append({'marked_colours': colours, 'pair': pair,
                                'blocks': blocks, 'all_successors': successors,
                                'target_free_cube': safe})
    return {'status': 'PASS', 'proper_six_vertex_rows': len(rows),
            'event_rows': sum(r['event'] for r in rows),
            'marked_partition_cases': len(records), 'rows': rows,
            'partition_cases': records,
            'scope': 'Exhaustive local algebra and marked-cycle partitions only; no source realization.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = check()
    encoded = json.loads(json.dumps(result))
    if args.write:
        with args.write.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    else:
        assert json.loads(args.check.read_text()) == encoded, 'certificate mismatch'
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('rows', 'partition_cases')}))


if __name__ == '__main__':
    main()
