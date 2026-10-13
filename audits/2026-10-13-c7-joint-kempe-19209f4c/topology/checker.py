#!/usr/bin/env python3
"""Exact named C7 chord and two-edge crosscut exclusions.

The universal disk-separation and minimality arguments are in REPORT.md.
This program certifies all finite relation operations; no source enumeration.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'frozen/audits/2026-10-12-neartri-complete-relation-reductions-5d70a399'
spec = importlib.util.spec_from_file_location('frozen_collar', OLD / 'collar_checker.py')
collar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collar)
NAMES = ['a0', 'a1', 'y2', 'a2', 'a3', 'y4', 'a4']
L4 = [7, 10, 11, 12, 13, 14, 15]
TARGET = 941


def inputs():
    records = json.loads((HERE / 'INPUTS.json').read_text())['inputs']
    for r in records:
        assert hashlib.sha256((HERE / r['frozen']).read_bytes()).hexdigest() == r['sha256']
    base = json.loads((HERE.parent / 'BASE.json').read_text())
    for name in ('collar_checker.py', 'collar_certificate.json'):
        rel = 'audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/' + name
        assert hashlib.sha256((OLD / name).read_bytes()).hexdigest() == base['inputs_sha256'][rel]
    return records


def case():
    cert = json.loads((OLD / 'collar_certificate.json').read_text())
    return next(c for c in cert['cases'] if c['boundary_extras'] == [0, 0, 1, 0, 1])


def build():
    frozen = inputs()
    k = sorted(map(int, json.loads((HERE / 'frozen/cells.json').read_text())['cells']))
    pats = {n: collar.patterns(n) for n in (4, 5, 6, 7)}
    indexes = {n: {p: i for i, p in enumerate(ps)} for n, ps in pats.items()}
    source = case()
    columns = source['column_masks']
    tables = {n: collar.kempe_table(n) for n in (6, 7)}
    chords = []
    for s in range(7):
        c4 = [(s + j) % 7 for j in range(4)]
        c5 = [(s + j) % 7 for j in range(3, 8)]
        restrictions = []
        for p in pats[7]:
            q4 = collar.norm(tuple(p[v] for v in c4))
            q5 = collar.norm(tuple(p[v] for v in c5))
            restrictions.append((indexes[4].get(q4), indexes[5].get(q5)))
        for a in L4:
            for b in k:
                inner = outer = 0
                for i, (i4, i5) in enumerate(restrictions):
                    if i4 is not None and i5 is not None and a >> i4 & 1 and b >> i5 & 1:
                        inner |= 1 << i
                        outer |= columns[i]
                assert outer in k and outer != TARGET
                chords.append(dict(start=s, short_cycle=c4, long_cycle=c5,
                                   short_mask=a, long_mask=b,
                                   inner_accepted_mask=inner,
                                   inner_rejected_mask=((1 << 91) - 1) ^ inner,
                                   outer_accepted_mask=outer, outer_rejected_mask=1023 ^ outer))
    crosscuts = []
    for d, known in ((2, L4), (3, k)):
        n = 9 - d
        for s in range(7):
            short = [(s + j) % 7 for j in range(d + 1)] + [7]
            long = [(s + j) % 7 for j in range(d, 8)] + [7]
            raw = []
            for p in pats[n]:
                pins = dict(zip(long, p))
                row = []
                for cs in itertools.product(range(4), repeat=d - 1):
                    colors = pins | dict(zip([(s + j) % 7 for j in range(1, d)], cs))
                    q = collar.norm(tuple(colors[v] for v in short))
                    ring = tuple(colors[v] for v in range(7))
                    r = collar.norm(ring)
                    if q in indexes[d + 2] and r in indexes[7]:
                        row.append((indexes[d + 2][q], ring, columns[indexes[7][r]]))
                raw.append(row)
            for a in known:
                transfer = []
                completions = []
                for row in raw:
                    col = 0
                    words = []
                    for idx, ring, out in row:
                        if a >> idx & 1:
                            col |= out
                            words.append(ring)
                    transfer.append(col)
                    completions.append(words)
                result = collar.prune(transfer, tables[n], TARGET)
                assert result['excluded']
                crosscuts.append(dict(distance=d, start=s, new_vertex='z=7',
                                      short_cycle=short, long_cycle=long, short_mask=a,
                                      completion_words_by_long_row=completions,
                                      column_masks=transfer, screen=result))
    assert len(chords) == 6468 and len(crosscuts) == 973
    return dict(named_ring=NAMES, outer_names=['b' + str(i) for i in range(5)],
                color_frame=list(range(4)), pattern_orders=pats, inputs=frozen,
                short_C4_necessary_masks=L4, short_C5_K132=k,
                original_collar=source, chords=chords, two_edge_crosscuts=crosscuts,
                claims={'induced_C7': True, 'no_nonadjacent_two_edge_crosscut': True,
                        'all_apex_original_degrees_at_least_6': True,
                        'original_internal_vertices_at_least_14': True},
                source_status='not triggered', h2_source_excluded=False)


def main():
    p = argparse.ArgumentParser()
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    a = p.parse_args()
    cert = build()
    dest = HERE / 'certificate.json'
    if a.write:
        with dest.open('x') as f:
            json.dump(cert, f, separators=(',', ':'), sort_keys=True)
            f.write('\n')
    else:
        assert json.loads(dest.read_text()) == json.loads(json.dumps(cert)), 'certificate mismatch'
    print(json.dumps(dict(status='PASS', chord_joins=len(cert['chords']),
                          excluded_crosscuts=len(cert['two_edge_crosscuts']),
                          source_status=cert['source_status'], h2_source_excluded=False)))


if __name__ == '__main__':
    main()
