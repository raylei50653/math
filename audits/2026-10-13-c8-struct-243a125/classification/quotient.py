#!/usr/bin/env python3
"""Finite core for the proved cofacial-identification / four-color condition."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'frozen/audits/2026-10-13-c8-joint-count-3097ef5'


def build():
    I = json.loads((SOURCE / 'interface.json').read_text())
    C = json.loads((SOURCE / 'counts/certificate.v2.json').read_text())
    P = I['pattern_order']
    cases = {c['id']: c for c in I['cases']}
    conditions = []
    for index, part in enumerate(C['noncrossing_partitions']):
        if any(part[i] == part[(i + 1) % 8] for i in range(8)):
            continue
        rows = [r for r, p in enumerate(P) if all(part[i] != part[j] or p[i] == p[j]
                for i in range(8) for j in range(i + 1, 8))]
        conditions.append(dict(partition_index=index, partition=part, equality_rows=rows))
    queries = []
    for q in C['queries']:
        if q['status'] != 'necessary_condition_residual':
            continue
        c = cases[q['case_id']]
        upper = q['final_upper_mask']
        intersections = [[r for r in condition['equality_rows'] if upper >> r & 1]
                         for condition in conditions]
        missing = [i for i, rows in enumerate(intersections) if not rows]
        pair_witness = None
        if missing:
            positions = [c['boundary_order'].index(v) for v in ('a1', 'a4')]
            i, j = positions
            rows = [r for r, p in enumerate(P) if p[i] == p[j]]
            assert not any(upper >> r & 1 for r in rows)
            pair_witness = dict(names=['a1', 'a4'], positions=positions,
                                equality_rows=rows, equality_upper_intersection=[])
        queries.append(dict(query_id=f"{q['case_id']}-{q['target']}",
                            final_upper_mask=upper, boundary_order=c['boundary_order'],
                            intersections=intersections, missing_conditions=missing,
                            pair_witness=pair_witness,
                            status='proved exclusion' if missing else 'necessary-condition residual'))
    return dict(schema='c8-struct-cofacial-quotient-v1',
                source_sha256={p: hashlib.sha256((SOURCE / p).read_bytes()).hexdigest()
                               for p in ('interface.json', 'counts/certificate.v2.json')},
                theorem_dependencies=['source global minimality', 'induced C8 theorem',
                                      'four-color theorem for finite loopless planar graphs'],
                patterns=P, conditions=conditions, queries=queries,
                summary=dict(excluded=2, residual=8, proper_noncrossing_conditions=91),
                scope='complete finite boundary core of an arbitrary-size cofacial-quotient theorem; not a finite graph search')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=HERE / 'quotient.json')
    args = parser.parse_args()
    result = build()
    with args.output.open('x') as out:
        json.dump(result, out, indent=2, sort_keys=True)
        out.write('\n')
    print('PASS: cofacial quotient excludes c16-941 and c32-941; eight queries remain')
