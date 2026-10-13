#!/usr/bin/env python3
"""Produce explicit, whole-collar D5 maps; no search for graphs or counts."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'frozen/audits/2026-10-13-c8-joint-count-3097ef5'


def norm(word):
    d = {}
    return tuple(d.setdefault(c, len(d)) for c in word)


def move(word, positions):
    out = [None] * len(word)
    for i, j in enumerate(positions):
        out[j] = word[i]
    return norm(out)


def build():
    interface = json.loads((SOURCE / 'interface.json').read_text())
    counts = json.loads((SOURCE / 'counts/certificate.v2.json').read_text())
    patterns = list(map(tuple, interface['pattern_order']))
    outer = list(map(tuple, interface['outer_pattern_order']))
    cases = {c['id']: c for c in interface['cases']}
    queries = {f"{q['case_id']}-{q['target']}": q for q in counts['queries']
               if q['status'] == 'necessary_condition_residual'}
    index = {p: i for i, p in enumerate(patterns)}
    outer_index = {p: i for i, p in enumerate(outer)}
    stabilizers = {}
    for target in (933, 941):
        stabilizers[str(target)] = []
        for sign in (1, -1):
            for offset in range(5):
                positions = [(offset + sign * i) % 5 for i in range(5)]
                rows = [outer_index[move(p, positions)] for p in outer]
                image = sum(1 << rows[r] for r in range(10) if target >> r & 1)
                if image == target:
                    stabilizers[str(target)].append(dict(
                        sign=sign, offset=offset, outer_positions=positions,
                        outer_rows=rows))
    query_records = []
    transports = []
    for name, q in sorted(queries.items()):
        c = cases[q['case_id']]
        x = list(map(Fraction, q['counts']))
        positive = [i for i, value in enumerate(x) if value > 0]
        pairs = []
        for i in range(8):
            for j in range(i + 1, 8):
                if j - i in (1, 7):
                    continue
                equal_rows = [r for r in positive if patterns[r][i] == patterns[r][j]]
                pairs.append(dict(positions=[i, j], names=[c['boundary_order'][i],
                                                            c['boundary_order'][j]],
                                  positive_equal_rows=equal_rows))
        query_records.append(dict(query_id=name, target=q['target'],
                                  extras=c['extras'], boundary_order=c['boundary_order'],
                                  supports=c['supports'], collar_edges=c['collar_edges'],
                                  counts=q['counts'], outer_counts=q['outer_counts'],
                                  positive_rows=positive, nonadjacent_pairs=pairs,
                                  status='necessary-condition residual'))
        for action in stabilizers[str(q['target'])]:
            sign, offset = action['sign'], action['offset']
            if (sign, offset) == (1, 0):
                continue
            bmap = action['outer_positions']
            extras = [None] * 5
            for i, j in enumerate(bmap):
                extras[j] = c['extras'][i]
            destination = next(d for d in cases.values() if d['extras'] == extras)
            other = f"{destination['id']}-{q['target']}"
            if name > other:
                continue
            labels = {f'b{i}': f'b{bmap[i]}' for i in range(5)}
            labels.update({f'a{i}': f'a{(offset + sign * i - (sign == -1)) % 5}'
                           for i in range(5)})
            for i, t in enumerate(c['extras']):
                for j in range(1, t + 1):
                    labels[f'y{i}_{j}'] = f'y{bmap[i]}_{j if sign == 1 else t + 1 - j}'
            inner_positions = [destination['boundary_order'].index(labels[label])
                               for label in c['boundary_order']]
            inner_rows = [index[move(p, inner_positions)] for p in patterns]
            transformed = ['0'] * 274
            for i, j in enumerate(inner_rows):
                transformed[j] = str(x[i])
            y = list(map(Fraction, queries[other]['counts']))
            ratios = {Fraction(a) / b for a, b in zip(transformed, y) if b}
            transformed_outer = ['0'] * 10
            for i, j in enumerate(action['outer_rows']):
                transformed_outer[j] = q['outer_counts'][i]
            transports.append(dict(
                source=name, destination=other, sign=sign, offset=offset,
                label_map=labels, outer_positions=bmap,
                outer_rows=action['outer_rows'], inner_positions=inner_positions,
                inner_rows=inner_rows, transported_counts=transformed,
                transported_outer_counts=transformed_outer,
                support_matches=all(bool(Fraction(a)) == bool(b)
                                    for a, b in zip(transformed, y)),
                stored_vectors_equal=list(map(Fraction, transformed)) == y,
                stored_vectors_proportional=len(ratios) == 1 and all(
                    bool(Fraction(a)) == bool(b) for a, b in zip(transformed, y))))
    return dict(schema='c8-struct-classification-v1',
                source_sha256={p: hashlib.sha256((SOURCE / p).read_bytes()).hexdigest()
                               for p in ('interface.json', 'counts/certificate.v2.json')},
                scope='Five explicit D5 equivalences of named query contracts; no graph realization claimed.',
                stabilizers=stabilizers, queries=query_records, transports=transports,
                classes=[[t['source'], t['destination']] for t in transports],
                edge_observation_status='conditional: applies to realization of the complete saved positive support, not to every source whose support is contained in the certified upper')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE / 'classification.json')
    args = parser.parse_args()
    result = build()
    with args.output.open('x') as out:
        json.dump(result, out, indent=2, sort_keys=True)
        out.write('\n')
    print('PASS: 10 named residuals, five explicit whole-collar symmetry pairs')
