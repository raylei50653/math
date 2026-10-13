#!/usr/bin/env python3
"""Exact stdlib verification of universal disk-C7 extension-count identities.

No imported graph enumerator, SAT solver, CAS, or floating arithmetic.
Boundary assignments retain the frozen named order and literal colors.
"""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'frozen/audits/2026-10-12-neartri-complete-relation-reductions-5d70a399'
UPPER = 755425272170557940120206052


def norm(word):
    distinct = []
    result = []
    for c in word:
        if c not in distinct:
            distinct.append(c)
        result.append(distinct.index(c))
    return tuple(result)


def set_partitions(word=()):
    if len(word) == 7:
        yield word
        return
    for c in range(max(word, default=-1)+2):
        yield from set_partitions(word+(c,))


def noncrossing(partition):
    return not any(partition[a] == partition[c]
                   and partition[b] == partition[d]
                   and partition[a] != partition[b]
                   for a, b, c, d in combinations(range(7), 4))


def equality_entry(word, partition):
    return int(all(partition[i] != partition[j] or word[i] == word[j]
                   for i, j in combinations(range(7), 2)))


def build_basis(rows, sources):
    """Echelon basis tracking literal rational combinations of source rows."""
    basis = {}
    for i in sources:
        v = list(map(Fraction, rows[i]))
        coefficients = {i: Fraction(1)}
        for pivot, (r, expansion) in sorted(basis.items()):
            scale = v[pivot]
            if scale:
                v = [a-scale*b for a,b in zip(v,r)]
                for j, c in expansion.items():
                    coefficients[j] = coefficients.get(j,0)-scale*c
        if any(v):
            pivot = next(j for j,c in enumerate(v) if c)
            scale = v[pivot]
            basis[pivot] = ([c/scale for c in v],
                            {j:c/scale for j,c in coefficients.items() if c})
    return basis


def express(vector, basis):
    v = list(map(Fraction, vector))
    coefficients = {}
    for pivot, (r, expansion) in sorted(basis.items()):
        scale = v[pivot]
        if scale:
            v = [a-scale*b for a,b in zip(v,r)]
            for j,c in expansion.items():
                coefficients[j] = coefficients.get(j,0)+scale*c
    assert not any(v), 'Requested universal identity does not follow'
    return {j:c for j,c in coefficients.items() if c}


def build():
    frozen = json.loads((BASE / 'collar_certificate.json').read_text())
    words = tuple(sorted({norm(word) for word in product(range(4), repeat=7)
                          if all(word[i] != word[(i+1) % 7] for i in range(7))}))
    assert list(map(list, words)) == frozen['inner_pattern_orders']['7']
    partitions = tuple(p for p in set_partitions() if noncrossing(p))
    active = tuple(p for p in partitions if any(equality_entry(w,p) for w in words))
    assert len(partitions) == 429 and len(active) == 36
    rows = tuple(tuple(equality_entry(w,p) for p in active) for w in words)
    rejected = [i for i in range(len(words)) if not (UPPER >> i & 1)]
    all_basis = build_basis(rows, range(91))
    rejected_basis = build_basis(rows, rejected)
    assert len(all_basis) == 36 and len(rejected_basis) == 31
    identities = []
    left_sides = [{42:1}, {49:1}, {73:1}, {75:1}, {6:1,35:1},
                  {58:1,6:-1}, {89:1,6:-1}]
    for lhs in left_sides:
        target = [sum(c*rows[i][j] for i,c in lhs.items()) for j in range(36)]
        rhs = express(target, rejected_basis)
        assert all(c.denominator == 1 for c in rhs.values())
        rhs = {i:int(c) for i,c in rhs.items()}
        # Direct identity check includes every NC partition, even 393 zero columns.
        residuals = [sum(c*equality_entry(words[i],p) for i,c in lhs.items())
                     -sum(c*equality_entry(words[i],p) for i,c in rhs.items())
                     for p in partitions]
        assert not any(residuals)
        identities.append(dict(lhs=[dict(index=i,word=words[i],coefficient=c)
                                    for i,c in sorted(lhs.items())],
                               rhs=[dict(index=i,word=words[i],coefficient=c)
                                    for i,c in sorted(rhs.items())],
                               partition_residuals=residuals))
    case, = [c for c in frozen['cases'] if c['boundary_extras'] == [0,0,1,0,1]]
    outer_words = frozen['outer_pattern_order']
    outer_index = outer_words.index([0,1,2,3,2])
    accepted_preimages = [i for i,c in enumerate(case['column_masks'])
                         if UPPER >> i & 1 and c >> outer_index & 1]
    assert accepted_preimages == [6,58,89]
    assert 941 >> outer_index & 1
    # Intentional false coefficient must be visible in the NC equality vectors.
    bad = dict((x['index'],x['coefficient']) for x in identities[0]['rhs'])
    bad[8] += 1
    corrupted_residual = [equality_entry(words[42],p)
                          -sum(c*equality_entry(words[i],p) for i,c in bad.items())
                          for p in partitions]
    assert any(corrupted_residual)
    # U's Boolean membership vector cannot be an actual extension count vector.
    boolean_residuals = [sum(x['coefficient']*int(UPPER >> x['index'] & 1)
                             for x in identity['lhs'])
                        -sum(x['coefficient']*int(UPPER >> x['index'] & 1)
                             for x in identity['rhs'])
                        for identity in identities]
    assert boolean_residuals == [1,1,1,1,2,0,0]
    return dict(boundary_order=['a0','a1','y2','a2','a3','y4','a4'],
                color_frame=[0,1,2,3], pattern_order=words,
                noncrossing_partitions=partitions, active_partitions=active,
                equality_rows=rows, full_rank=len(all_basis),
                rejected_rank=len(rejected_basis), upper_mask=UPPER,
                rejected_indices=rejected, identities=identities,
                outer_accepted_word=outer_words[outer_index],
                outer_word_index=outer_index,
                upper_preimages_of_outer_word=accepted_preimages,
                proof_consequence='All RHS counts vanish. Nonnegativity and x6+x35=0 force x6=x35=0; x58=x6 and x89=x6 force every 01232 preimage to vanish. Exact outer transfer cannot be 941.',
                controls=dict(corrupt_coefficient_detected=any(corrupted_residual),
                              boolean_upper_identity_residuals=boolean_residuals),
                target_source_status='excluded universally by planar count identities and nonnegativity')


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, default=HERE/'count_identity_certificate.json')
    args = parser.parse_args()
    result = build()
    if args.write:
        with args.certificate.open('x') as f:
            json.dump(result, f, sort_keys=True, separators=(',', ':'))
            f.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == json.loads(json.dumps(result)), 'certificate mismatch'
    print(json.dumps(dict(status='PASS', proper_rows=len(result['pattern_order']),
                          NC_partitions=len(result['noncrossing_partitions']),
                          active_columns=len(result['active_partitions']),
                          identities=len(result['identities']),
                          final_outer_preimages=result['upper_preimages_of_outer_word'],
                          target_source_status=result['target_source_status'])))


if __name__ == '__main__':
    main()
