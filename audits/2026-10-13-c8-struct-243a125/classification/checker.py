#!/usr/bin/env python3
"""Independent classification checker: no import of producer or solver."""
import argparse
from fractions import Fraction
import hashlib
from itertools import permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'frozen/audits/2026-10-13-c8-joint-count-3097ef5'


def canonical(word):
    names = list(dict.fromkeys(word))
    return tuple(names.index(c) for c in word)


def image_word(word, positions):
    inverse = [positions.index(i) for i in range(len(positions))]
    return canonical([word[i] for i in inverse])


def edgeset(edges):
    return {frozenset(edge) for edge in edges}


def verify(data):
    assert data['schema'] == 'c8-struct-classification-v1'
    for path, digest in data['source_sha256'].items():
        assert hashlib.sha256((SOURCE / path).read_bytes()).hexdigest() == digest
    I = json.loads((SOURCE / 'interface.json').read_text())
    C = json.loads((SOURCE / 'counts/certificate.v2.json').read_text())
    P = list(map(tuple, I['pattern_order']))
    B = list(map(tuple, I['outer_pattern_order']))
    cases = {c['id']: c for c in I['cases']}
    residuals = {f"{q['case_id']}-{q['target']}": q for q in C['queries']
                 if q['status'] == 'necessary_condition_residual'}
    assert len(data['queries']) == len(residuals) == 10
    records = {q['query_id']: q for q in data['queries']}
    assert set(records) == set(residuals)
    # Independently enumerate all S5 bijections and select cycle automorphisms.
    automorphisms = [m for m in permutations(range(5)) if all(
        (m[(i + 1) % 5] - m[i]) % 5 in (1, 4) for i in range(5))]
    assert len(automorphisms) == 10
    stabs = {}
    for target in (933, 941):
        wanted = set()
        for m in automorphisms:
            rows = tuple(B.index(image_word(b, m)) for b in B)
            if sum(1 << rows[r] for r in range(10) if target >> r & 1) == target:
                wanted.add((tuple(m), rows))
        actual = data['stabilizers'][str(target)]
        assert len(actual) == len(wanted) == 2
        assert {(tuple(a['outer_positions']), tuple(a['outer_rows'])) for a in actual} == wanted
        for a in actual:
            assert a['outer_positions'] == [(a['offset'] + a['sign'] * i) % 5 for i in range(5)]
        stabs[target] = wanted
    chord_tests = 0
    for name, q in residuals.items():
        record = records[name]
        c = cases[q['case_id']]
        for field in ('extras', 'boundary_order', 'supports', 'collar_edges'):
            assert record[field] == c[field], (name, field)
        for field in ('counts', 'outer_counts', 'target'):
            assert record[field] == q[field], (name, field)
        positive = [r for r, value in enumerate(q['counts']) if Fraction(value) > 0]
        assert record['positive_rows'] == positive
        assert sum(1 << r for r in positive) == q['final_upper_mask']
        pairs = {(i, j) for i in range(8) for j in range(i + 1, 8) if j - i not in (1, 7)}
        assert len(record['nonadjacent_pairs']) == 20
        assert {tuple(p['positions']) for p in record['nonadjacent_pairs']} == pairs
        for pair in record['nonadjacent_pairs']:
            i, j = pair['positions']
            assert pair['names'] == [c['boundary_order'][i], c['boundary_order'][j]]
            assert pair['positive_equal_rows'] == [r for r in positive if P[r][i] == P[r][j]]
            chord_tests += 1
    covered = []
    for t in data['transports']:
        name, other = t['source'], t['destination']
        covered += [name, other]
        q, r = residuals[name], residuals[other]
        c, d = cases[q['case_id']], cases[r['case_id']]
        assert q['target'] == r['target']
        bm, br = t['outer_positions'], t['outer_rows']
        im, ir = t['inner_positions'], t['inner_rows']
        assert (tuple(bm), tuple(br)) in stabs[q['target']]
        assert bm != list(range(5))
        assert bm == [(t['offset'] + t['sign'] * i) % 5 for i in range(5)]
        assert sorted(im) == list(range(8))
        assert sorted(ir) == list(range(274))
        assert all((im[(i + 1) % 8] - im[i]) % 8 == t['sign'] % 8 for i in range(8))
        labels = t['label_map']
        assert set(labels) == {f'b{i}' for i in range(5)} | set(c['boundary_order'])
        assert set(labels.values()) == {f'b{i}' for i in range(5)} | set(d['boundary_order'])
        assert all(labels[f'b{i}'] == f'b{bm[i]}' for i in range(5))
        assert [labels[v] for v in c['boundary_order']] == [d['boundary_order'][i] for i in im]
        assert edgeset([[labels[u], labels[v]] for u, v in c['collar_edges']]) == edgeset(d['collar_edges'])
        for i in range(8):
            assert {bm[j] for j in c['supports'][i]} == set(d['supports'][im[i]])
        # Every whole-word permutation is followed by one common color normalization.
        assert ir == [P.index(image_word(p, im)) for p in P]
        assert br == [B.index(image_word(b, bm)) for b in B]
        # Literal collar counts: all ten rows, all 274 inner coordinates.
        assert all(c['transfer'][b][p] == d['transfer'][br[b]][ir[p]]
                   for b in range(10) for p in range(274))
        assert all(c['column_masks'][p] == sum(1 << b for b in range(10)
                   if d['column_masks'][ir[p]] >> br[b] & 1) for p in range(274))
        x = [Fraction(s) for s in q['counts']]
        y = [Fraction(s) for s in r['counts']]
        moved = [x[ir.index(i)] for i in range(274)]
        assert list(map(Fraction, t['transported_counts'])) == moved
        moved_outer = [Fraction(q['outer_counts'][br.index(i)]) for i in range(10)]
        assert list(map(Fraction, t['transported_outer_counts'])) == moved_outer
        assert all(sum(Fraction(d['transfer'][b][p]) * moved[p] for p in range(274)) == moved_outer[b]
                   for b in range(10))
        supports_match = all(bool(a) == bool(b) for a, b in zip(moved, y))
        assert t['support_matches'] == supports_match == True
        assert t['stored_vectors_equal'] == (moved == y)
        ratios = {a / b for a, b in zip(moved, y) if b}
        assert t['stored_vectors_proportional'] == (supports_match and len(ratios) == 1)
    assert sorted(covered) == sorted(residuals) and len(data['transports']) == 5
    assert data['classes'] == [[t['source'], t['destination']] for t in data['transports']]
    assert data['edge_observation_status'].startswith('conditional:')
    return dict(status='PASS', queries=10, classes=5, pair_equality_checks=chord_tests,
                full_transfer_entries_checked=5 * 10 * 274,
                proof_scope='named whole-collar equivalence; conditional edge obstructions; no source exclusion')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE / 'classification.json')
    args = parser.parse_args()
    print(json.dumps(verify(json.loads(args.certificate.read_text())), sort_keys=True))
