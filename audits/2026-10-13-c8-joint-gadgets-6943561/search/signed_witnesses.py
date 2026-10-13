#!/usr/bin/env python3
"""Explicit same-frame full fibres for the eight forced-row signed caps."""
import argparse
import copy
import gzip
import json
from pathlib import Path
import witnesses

HERE = Path(__file__).resolve().parent


def build():
    frozen = HERE.parent / 'frozen/audits'
    rows = json.loads((frozen / '2026-10-13-c8-joint-count-3097ef5/interface.json').read_text())['pattern_order']
    queries = [q for q in json.loads((frozen / '2026-10-13-c5-no4ct-c8-6cafdfb/RESULTS.json').read_text())['queries']
               if q['status'] == 'necessary_condition_residual']
    records = [json.loads(line) for line in (HERE / 'signed_h0.jsonl').read_text().splitlines()]
    certificates = []
    for item in records:
        if item['kind'] != 'forced_row':
            continue
        query = queries[item['query_index']]
        n_text, code = item['ascii'].split()
        assert int(n_text) == 8
        rotation = [[ord(c)-97 for c in part] for part in code.split(',')]
        boundary = next(face for face in witnesses.faces(rotation) if len(face) == 8)
        canonical = {v: i for i, v in enumerate(boundary)}
        edges = sorted({tuple(sorted((canonical[a], canonical[b]))) for a, ns in enumerate(rotation) for b in ns})
        cycle = {tuple(sorted((i, (i+1) % 8))) for i in range(8)}
        chords = sorted(set(edges) - cycle)
        assert list(map(list, chords)) == item['chords']
        mask = item['equality_mask']
        t = item['transform']
        direction, shift = (1, t) if t < 8 else (-1, t-8)
        named = [(shift+direction*j) % 8 for j in range(8)]
        eq = [tuple(sorted((named[a], named[b]))) for i, (a, b) in enumerate(chords) if mask >> i & 1]
        diff = [tuple(sorted((named[a], named[b]))) for a, b in edges if (a, b) not in [c for i, c in enumerate(chords) if mask >> i & 1]]
        classes = [{i} for i in range(8)]
        for a, b in eq:
            first = next(c for c in classes if a in c)
            second = next(c for c in classes if b in c)
            if first is not second:
                first.update(second)
                classes.remove(second)
        assert all(not any(a in c and b in c for c in classes) for a, b in diff)
        saved = 8-len(classes)
        assert saved == item['saved_boundary_vertices']
        full = [[[]] if all(row[a] == row[b] for a, b in eq) and all(row[a] != row[b] for a, b in diff) else [] for row in rows]
        support = sum(1 << i for i, fibre in enumerate(full) if fibre)
        assert support & query['support'] == 1 << item['forced_row']
        names = query['boundary_order']
        certificates.append({'query_id': query['query_id'], 'boundary_order': names,
                             'source': item, 'private_vertices': 0,
                             'equality_edges': [[names[a], names[b]] for a, b in sorted(eq)],
                             'different_edges': [[names[a], names[b]] for a, b in sorted(diff)],
                             'contraction_classes': [[names[i] for i in sorted(c)] for c in sorted(classes, key=min)],
                             'net_added_vertices': -saved,
                             'full_private_lifts_by_literal_row': full,
                             'support': support, 'upper_support_intersection': 1 << item['forced_row'],
                             'forced_row': item['forced_row'], 'forced_literal': rows[item['forced_row']]})
    assert len(certificates) == 8
    return {'schema': 'c8-signed-forced-row-witnesses-v1', 'color_frame': [0, 1, 2, 3],
            'literal_rows': rows, 'witnesses': certificates,
            'scope': 'Explicit full-fibre witnesses for eight forced-row incidences. Equality operations require the frozen induced-C8 source contract; the graph signed edges are all on the cap side.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = build()
    target = HERE / 'signed_witnesses.json.gz'
    if args.check:
        got = json.loads(gzip.decompress(target.read_bytes()))
        assert got == expected
        bad = copy.deepcopy(got)
        w = bad['witnesses'][0]
        w['full_private_lifts_by_literal_row'][w['forced_row']] = []
        assert bad != expected
        bad = copy.deepcopy(got)
        bad['witnesses'][0]['boundary_order'].reverse()
        assert bad != expected
    else:
        with target.open('xb') as output:
            output.write(gzip.compress((json.dumps(expected, sort_keys=True, separators=(',', ':'))+'\n').encode(), mtime=0))
    print(json.dumps({'status': 'PASS', 'witnesses': len(expected['witnesses']),
                      'full_fibres': 8*274,
                      'negative_controls_rejected': ['deleted_forced_lift', 'reversed_names'] if args.check else []}))


if __name__ == '__main__':
    main()
