#!/usr/bin/env python3
"""Independent brute-force complete named fibres for eight 5-private cap minima.

No producer import. Enumerates all 4^5 private tuples per fixed literal row.
"""
import argparse
import copy
import gzip
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def faces(rotation):
    darts = {(a, b) for a, neighbours in enumerate(rotation) for b in neighbours}
    assert all((b, a) in darts for a, b in darts)
    assert all(len(set(ns)) == len(ns) and a not in ns for a, ns in enumerate(rotation))
    todo = set(darts)
    result = []
    # Match producer's documented first-dart convention without its code.
    for a, ns in enumerate(rotation):
        for b in ns:
            if (a, b) not in todo:
                continue
            walk = []
            first = (a, b)
            while True:
                todo.remove((a, b))
                walk.append(a)
                k = rotation[b].index(a)
                a, b = b, rotation[b][(k + 1) % len(rotation[b])]
                if (a, b) == first:
                    break
            result.append(walk)
    assert len(rotation) - len(darts)//2 + len(result) == 2
    assert sorted(map(len, result)) == [3]*(len(result)-1) + [8]
    return result


def normalize(word):
    colors = {}
    return tuple(colors.setdefault(c, len(colors)) for c in word)


def build():
    summary = json.loads((HERE / 'RESULTS.json').read_text())
    frozen = HERE.parent / 'frozen/audits'
    rows = json.loads((frozen / '2026-10-13-c8-joint-count-3097ef5/interface.json').read_text())['pattern_order']
    queries = [q for q in json.loads((frozen / '2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json').read_text())['queries']
               if q['status'] == 'necessary_condition_residual']
    assert rows == summary['rows'] and queries == summary['queries']
    assert len(rows) == 274 and len(queries) == 8
    row_index = {tuple(row): i for i, row in enumerate(rows)}
    graph_lines = gzip.decompress((HERE / 'data/h5.ascii.gz').read_bytes()).decode().splitlines()
    count_bytes = gzip.decompress((HERE / 'data/h5.counts.u16le.gz').read_bytes())
    result = []
    for q, record in zip(queries, summary['by_private_vertices'][5]['queries']):
        graph_id = record['witness_graph_index']
        n_text, encoded = graph_lines[graph_id].split()
        assert int(n_text) == 13
        rotation = [[ord(c)-97 for c in ns] for ns in encoded.split(',')]
        outer = next(f for f in faces(rotation) if len(f) == 8)
        interior = sorted(set(range(13)) - set(outer))
        t = record['witness_transform']
        direction, shift = (1, t) if t < 8 else (-1, t-8)
        cap_to_named = [(shift+direction*j) % 8 for j in range(8)]
        old_to_named = dict(zip(outer, cap_to_named))
        old_to_named.update({v: 8+i for i, v in enumerate(interior)})
        edges = sorted({tuple(sorted((old_to_named[a], old_to_named[b])))
                        for a, ns in enumerate(rotation) for b in ns})
        names = q['boundary_order'] + [f'z{i}' for i in range(5)]
        full = []
        for row in rows:
            fibre = []
            for private in itertools.product(range(4), repeat=5):
                assignment = list(row) + list(private)
                if all(assignment[a] != assignment[b] for a, b in edges):
                    fibre.append(list(private))
            full.append(fibre)
            cap_row = normalize([row[i] for i in cap_to_named])
            offset = 2*(274*graph_id + row_index[cap_row])
            expected_count = int.from_bytes(count_bytes[offset:offset+2], 'little')
            assert len(fibre) == expected_count
        support = sum(1 << i for i, fibre in enumerate(full) if fibre)
        intersection = support & q['support']
        assert intersection.bit_count() == record['minimum_intersection']
        assert any(a >= 8 and b >= 8 for a, b in edges)
        named_rotation = [[] for _ in range(13)]
        for a, ns in enumerate(rotation):
            named_rotation[old_to_named[a]] = [old_to_named[b] for b in ns]
        result.append({'query_id': q['query_id'], 'private_vertices': 5,
                       'boundary_order': q['boundary_order'], 'private_order': names[8:],
                       'plantri_graph_index': graph_id, 'transform': t,
                       'plantri_ascii': graph_lines[graph_id],
                       'name_order': names, 'rotation': named_rotation,
                       'edges': [[names[a], names[b]] for a, b in edges],
                       'complete_private_lifts_by_literal_row': full,
                       'support': support,
                       'upper_support_intersection': intersection,
                       'intersection_rows': [i for i in range(274) if intersection >> i & 1]})
    return {'schema': 'c8-allcaps-named-full-fibre-witnesses-v1', 'color_frame': [0, 1, 2, 3],
            'literal_rows': rows, 'witnesses': result,
            'encoding': 'Each complete lift is the stored literal boundary row followed by the private tuple in private_order. Empty fibres [] are retained. Named rotations are index lists in name_order.',
            'scope': 'Eight five-private-vertex caps with adjacent private vertices attaining the global minimum U-intersection sizes. No source exclusion.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = build()
    path = HERE / 'witnesses.json.gz'
    if args.check:
        got = json.loads(gzip.decompress(path.read_bytes()))
        assert got == expected
        bad = copy.deepcopy(got)
        witness = bad['witnesses'][0]
        i = next(i for i, f in enumerate(witness['complete_private_lifts_by_literal_row']) if f)
        witness['complete_private_lifts_by_literal_row'][i].pop()
        assert bad != expected
        bad = copy.deepcopy(got)
        bad['witnesses'][0]['boundary_order'].reverse()
        assert bad != expected
        bad = copy.deepcopy(got)
        bad['witnesses'][0]['upper_support_intersection'] = 0
        assert bad != expected
    else:
        with path.open('xb') as output:
            output.write(gzip.compress((json.dumps(expected, sort_keys=True, separators=(',', ':'))+'\n').encode(), mtime=0))
    print(json.dumps({'status': 'PASS', 'witnesses': 8, 'full_fibres': 8*274,
                      'full_lifts': sum(len(f) for w in expected['witnesses'] for f in w['complete_private_lifts_by_literal_row']),
                      'negative_controls_rejected': ['deleted_lift', 'reversed_names', 'false_empty_intersection'] if args.check else []}))


if __name__ == '__main__':
    main()
