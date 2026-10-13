#!/usr/bin/env python3
"""Independent finite-core checker; does not import producer or use a solver."""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'frozen/audits/2026-10-13-c8-joint-count-3097ef5'


def norm(word):
    names = list(dict.fromkeys(word))
    return tuple(names.index(c) for c in word)


def all_partitions():
    # Grow set blocks, independently of the frozen restricted-growth producer.
    states = [((0,),)]
    for vertex in range(1, 8):
        following = []
        for blocks in states:
            following.append(blocks + ((vertex,),))
            for i in range(len(blocks)):
                following.append(blocks[:i] + (blocks[i] + (vertex,),) + blocks[i + 1:])
        states = following
    words = []
    for blocks in states:
        word = [None] * 8
        for i, block in enumerate(blocks):
            for vertex in block:
                word[vertex] = i
        words.append(tuple(word))
    assert len(words) == len(set(words)) == 4140
    return sorted(words)


def verify(data):
    assert data['schema'] == 'c8-struct-cofacial-quotient-v1'
    assert data['theorem_dependencies'] == ['source global minimality', 'induced C8 theorem',
                                           'four-color theorem for finite loopless planar graphs']
    for path, digest in data['source_sha256'].items():
        assert hashlib.sha256((SOURCE / path).read_bytes()).hexdigest() == digest
    I = json.loads((SOURCE / 'interface.json').read_text())
    C = json.loads((SOURCE / 'counts/certificate.v2.json').read_text())
    literal = [p for p in product(range(4), repeat=8)
               if all(p[i] != p[(i + 1) % 8] for i in range(8))]
    P = sorted(set(norm(p) for p in literal))
    assert len(literal) == 6564 and len(P) == 274
    assert data['patterns'] == I['pattern_order'] == C['pattern_order'] == list(map(list, P))
    nc = [p for p in all_partitions() if not any(
        p[a] == p[c] and p[b] == p[d] and p[a] != p[b]
        for a, b, c, d in combinations(range(8), 4))]
    assert len(nc) == 1430 and nc == list(map(tuple, C['noncrossing_partitions']))
    proper = [(index, part) for index, part in enumerate(nc)
              if all(part[i] != part[(i + 1) % 8] for i in range(8))]
    assert len(proper) == len(data['conditions']) == 91
    equality_rows = []
    for condition, (index, part) in zip(data['conditions'], proper):
        assert condition['partition_index'] == index and tuple(condition['partition']) == part
        blocks = [{i for i in range(8) if part[i] == b} for b in set(part)]
        rows = [r for r, p in enumerate(P) if all(len({p[i] for i in block}) == 1 for block in blocks)]
        assert rows and condition['equality_rows'] == rows
        equality_rows.append(rows)
    residuals = {f"{q['case_id']}-{q['target']}": q for q in C['queries']
                 if q['status'] == 'necessary_condition_residual'}
    cases = {c['id']: c for c in I['cases']}
    assert len(data['queries']) == len(residuals) == 10
    assert {q['query_id'] for q in data['queries']} == set(residuals)
    excluded = []
    for record in data['queries']:
        q = residuals[record['query_id']]
        c = cases[q['case_id']]
        upper = q['final_upper_mask']
        assert record['final_upper_mask'] == upper
        assert record['boundary_order'] == c['boundary_order']
        intersections = [[r for r in rows if upper >> r & 1] for rows in equality_rows]
        assert record['intersections'] == intersections
        missing = [i for i, rows in enumerate(intersections) if not rows]
        assert record['missing_conditions'] == missing
        if missing:
            excluded.append(record['query_id'])
            assert record['status'] == 'proved exclusion'
            pair = record['pair_witness']
            assert pair['names'] == ['a1', 'a4']
            i, j = [c['boundary_order'].index(v) for v in pair['names']]
            assert pair['positions'] == [i, j]
            assert (j - i) % 8 not in (0, 1, 7)
            rows = [r for r, p in enumerate(P) if p[i] == p[j]]
            assert len(rows) == 74 and pair['equality_rows'] == rows
            assert pair['equality_upper_intersection'] == [r for r in rows if upper >> r & 1] == []
            assert all(Fraction(q['counts'][r]) == 0 for r in rows)
            # The old geometric relaxation included the same obstruction even before count refinement.
            assert not any(q['upper_mask'] >> r & 1 for r in rows)
        else:
            assert record['status'] == 'necessary-condition residual' and record['pair_witness'] is None
    assert excluded == ['c16-941', 'c32-941']
    assert data['summary'] == dict(excluded=2, residual=8, proper_noncrossing_conditions=91)
    return dict(status='PASS', excluded=excluded, residual=8,
                set_partitions_independently_enumerated=4140,
                complete_equality_conditions_checked=10 * 91,
                pair_equality_rows_checked=2 * 74,
                scope='complete boundary core under proved induced-C8 and four-color theorem')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'quotient.json')
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.certificate.read_text())), sort_keys=True))
