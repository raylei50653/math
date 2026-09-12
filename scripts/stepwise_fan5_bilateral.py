#!/usr/bin/env python3
"""Exact two-sided fan-5 languages K(L,R) = {X : L X R is colourable}.

Fixed labels throughout, gap length unrestricted. No fan-6 work or disk claim.
Minimality certificates use all words of length <=4 and independent graph replay.
"""
from collections import Counter, deque
from itertools import product
import json
from pathlib import Path
import sys

from stepwise_fan5_signatures import build_model, direct_colouring, run, signature

OUT = Path(__file__).resolve().parents[1] / 'artifacts/stepwise/fan5_bilateral.json'


def analyse():
    model = build_model(5)
    delta, live, left_reps = (model[k] for k in ('rows', 'live', 'reps'))
    qs = list(delta)
    assert qs == list(range(97))
    # B_R = {q : delta*(q,R) accepts}; prefixing i uses inverse image.
    subsets = [frozenset(q for q in qs if live[q])]
    subset_ids = {subsets[0]: 0}
    right_delta, right_reps = [], {0: ()}
    for subset in subsets:
        j = subset_ids[subset]
        row = []
        for i in range(4):
            target = frozenset(q for q in qs if delta[q][i] in subset)
            if target not in subset_ids:
                subset_ids[target] = len(subsets)
                right_reps[len(subsets)] = (i,) + right_reps[j]
                subsets.append(target)
            row.append(subset_ids[target])
        right_delta.append(tuple(row))
    n = len(subsets)
    assert n == 97
    # Reversal of this strip language is exact at the DFA level: the right
    # subsets are in bijection with classes of reversed right histories.
    reverse_class = {j: run(delta, model['start'], tuple(reversed(w)))
                     for j, w in right_reps.items()}
    assert len(set(reverse_class.values())) == 97
    for j in range(n):
        assert (model['start'] in subsets[j]) == live[reverse_class[j]]
        for i in range(4):
            assert reverse_class[right_delta[j][i]] == delta[reverse_class[j]][i]
    left_steps = [tuple(delta[q][i]*n+j for i in range(4)) for q in qs for j in range(n)]
    right_steps = [tuple(q*n+right_delta[j][i] for i in range(4)) for q in qs for j in range(n)]
    accepts = [q in subset for q in qs for subset in subsets]
    partition = list(map(int, accepts))
    refinement_counts = [len(set(partition))]
    while True:
        ids, new = {}, []
        for state, row in enumerate(left_steps):
            key = (partition[state],) + tuple(partition[t] for t in row)
            new.append(ids.setdefault(key, len(ids)))
        refinement_counts.append(len(ids))
        if len(ids) == len(set(partition)):
            partition = new
            break
        partition = new
    assert refinement_counts == [2,31,267,425,437,437]
    rows, right_rows, accepting, representatives, pair_counts = {}, {}, {}, {}, Counter()
    for state, row in enumerate(left_steps):
        k = partition[state]
        assert rows.setdefault(k, tuple(partition[t] for t in row)) == tuple(partition[t] for t in row)
        rr = tuple(partition[t] for t in right_steps[state])
        assert right_rows.setdefault(k, rr) == rr
        assert accepting.setdefault(k, accepts[state]) == accepts[state]
        q, j = divmod(state, n)
        pair = left_reps[q], right_reps[j]
        key = len(pair[0])+len(pair[1]), len(pair[0]), pair
        if k not in representatives or key < representatives[k][0]:
            representatives[k] = key, pair
        pair_counts[k] += 1
    # The two updates commute: inserting c at the left of the gap and d at
    # its right has the same result in either order.
    for k in rows:
        for c in range(4):
            for d in range(4):
                assert right_rows[rows[k][c]][d] == rows[right_rows[k][d]][c]
    coaccessible = {k for k in rows if accepting[k]}
    while True:
        new = coaccessible | {k for k, row in rows.items() if any(t in coaccessible for t in row)}
        if new == coaccessible:
            break
        coaccessible = new
    dead, = set(rows) - coaccessible
    # Sink removal on the coaccessible graph distinguishes finite languages
    # from states which can reach a live cycle.
    finite = set()
    while True:
        new = finite | {k for k in coaccessible if all(t not in coaccessible or t in finite for t in rows[k])}
        if new == finite:
            break
        finite = new
    finite_signatures = {}
    for k in finite:
        allowed = tuple(i for i, t in enumerate(rows[k]) if accepting[t])
        assert accepting[k]
        assert len(allowed) <= 2
        for i, t in enumerate(rows[k]):
            if i in allowed:
                assert accepting[t] and all(x == dead for x in rows[t])
            else:
                assert t == dead
        finite_signatures[k] = allowed
    assert len(finite_signatures) == len(set(finite_signatures.values())) == 11
    # All mature A/A pairs collapse to exactly 24 alternating-parity languages
    # and the empty language. Structural signatures use actual fixed colours.
    side_sig = {q: signature(model['order'][run(model['delta'],0,w)]) for q,w in left_reps.items()}
    mature, mature_counts, alternating = set(), Counter(), {}
    for q in qs:
        for j in range(n):
            if side_sig[q][0] != 'A' or side_sig[reverse_class[j]][0] != 'A':
                continue
            k = partition[q*n+j]
            mature.add(k)
            mature_counts[k] += 1
            if k == dead:
                continue
            _, b, a, _ = side_sig[q]
            sig = (b, a, 0 if accepting[k] else 1)
            assert alternating.setdefault(k, sig) == sig
    assert len(mature) == 25 and len(alternating) == len(set(alternating.values())) == 24
    for k, (b,a,parity) in alternating.items():
        t = rows[k][b]
        assert all(rows[k][i] == dead for i in range(4) if i != b)
        assert rows[t][a] == k
        assert all(rows[t][i] == dead for i in range(4) if i != a)
        assert accepting[t] != accepting[k]
        assert t in alternating
    # Independent minimality certificate: finite-depth truth vectors are all
    # different, and each of their bits is independently checked on the graph.
    tests = [w for length in range(5) for w in product(range(4), repeat=length)]
    fingerprints = {}
    for k in sorted(rows):
        left, right = representatives[k][1]
        bits = 0
        for bit, word in enumerate(tests):
            expected = accepting[run(rows,k,word)]
            actual = direct_colouring((5,), left+word+right) is not None
            assert expected == actual
            if actual:
                bits |= 1 << bit
        fingerprints[k] = hex(bits)
    assert len(set(fingerprints.values())) == len(rows) == 437
    single_hole_masks = {(int(bits,16) >> 1) & 15 for bits in fingerprints.values()}
    assert len(single_hole_masks) == 16
    # Also validate every one of the original 97*97 contexts at an empty gap.
    for q in qs:
        for j in range(n):
            assert (direct_colouring((5,), left_reps[q]+right_reps[j]) is not None) == (q in subsets[j])
    # Readable full-colouring examples, including why independent frames fail.
    examples = []
    for kind, contexts, word in [
        ('same independent S/S signatures, different relative colour alignment',
         [((0,),(0,)), ((0,),(1,))], (1,)),
        ('mature A_d/A_d in independent frames; one join possible, the other impossible at every gap length',
         [((2,1,0,1,0),(0,1,0,1,2)), ((2,1,0,1,0),(0,1,0,1,3))], (1,))]:
        witnesses = []
        for left,right in contexts:
            colouring = direct_colouring((5,),left+word+right)
            j = 0
            for c in reversed(right):
                j = right_delta[j][c]
            k = partition[run(delta,model['start'],left)*n+j]
            assert (colouring is not None) == accepting[run(rows,k,word)]
            witnesses.append(dict(left=left,right=right,central=word,class_id=k,colouring=colouring))
        if kind.startswith('mature'):
            assert witnesses[0]['class_id'] in alternating
            assert witnesses[1]['class_id'] == dead
        examples.append(dict(kind=kind,witnesses=witnesses))
    classes = []
    for k in sorted(rows):
        left,right = representatives[k][1]
        entry = dict(id=k,left=left,right=right,empty_gap_accepts=accepting[k],
                     left_delta=rows[k],right_delta=right_rows[k],raw_pair_count=pair_counts[k],
                     truth_vector_through_length_4=fingerprints[k],
                     language_kind='empty' if k==dead else 'finite' if k in finite else 'infinite')
        if k in finite_signatures:
            entry['finite_language'] = [()] + [(c,) for c in finite_signatures[k]]
        if k in alternating:
            entry['alternating_signature'] = dict(first=alternating[k][0],second=alternating[k][1],length_parity=alternating[k][2])
            entry['mature_pair_count'] = mature_counts[k]
        classes.append(entry)
    return dict(status='computationally observed; not a Lean proof of strip graph semantics',
        definition='K(L,R) = {X : the finite fan-5 strip with boundary L+X+R is colourable}; all finite gap lengths including zero',
        labels='fixed shared colours 0..3; no independent left/right quotient',
        left_classes=97,right_subsets=97,raw_pairs=n*len(qs),classes_count=len(rows),
        refinement_counts=refinement_counts,dead_class=dead,
        single_hole_allowed_colour_sets=len(single_hole_masks),
        language_counts=dict(empty=1,finite_nonempty=len(finite),infinite=len(coaccessible-finite)),
        mature_A_pairs=dict(raw_pairs=sum(mature_counts.values()),classes=len(mature),
            impossible_pairs=mature_counts[dead],nonempty_classes=len(alternating)),
        classes=classes,pair_to_class=[partition[q*n:(q+1)*n] for q in qs],
        right_states=[dict(id=j,representative=right_reps[j],accepted_left_classes=sorted(subsets[j]),
                          prepend_delta=right_delta[j],reversed_word_class=reverse_class[j]) for j in range(n)],
        test_word_order='length 0..4 then lexicographic over 0..3; bit 0 is empty word',
        examples=examples,
        verification=dict(right_reversal_isomorphism=True,both_updates_well_defined=True,
            commuting_update_checks=16*len(rows),raw_empty_gap_graph_replays=n*len(qs),
            independent_minimality_bits=len(tests)*len(rows),truth_vectors_pairwise_distinct=True,
            exact_mature_alternating_closure=True))


if __name__ == '__main__':
    content = json.dumps(analyse(),indent=2)+'\n'
    if '--check' in sys.argv:
        assert OUT.read_text() == content
        print('fan5 bilateral: full closure, both-end updates, 437 distinct graph-replayed residuals, mature signatures and artifact match passed')
    else:
        OUT.write_text(content)
        result=json.loads(content)
        print(json.dumps({k:result[k] for k in ('classes_count','refinement_counts','language_counts','mature_A_pairs','verification')},indent=2))
