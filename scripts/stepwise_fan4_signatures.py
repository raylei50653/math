#!/usr/bin/env python3
"""Complete fan-4 residual signatures and their first collisions on fan 5.

Pure finite computation, not a Lean proof of strip/DFA soundness. The transferable
recipe below reads the actual fan's cut; it does not simulate fan 4 on fan-5 words.
"""
from collections import Counter, deque
from itertools import product
import json
from pathlib import Path
import sys

from stepwise_aligned_reference import (
    PERMS, automaton, direct_colouring, frame, quotient, run, separator,
)

OUT = Path(__file__).resolve().parents[1] / 'artifacts/stepwise/fan4_signatures.json'
MOVES = [tuple(0 if j == i else j + 1 if j < i else j for j in range(4))
         for i in range(4)]


def signature(cut, fan):
    """Fan-4 minimal structural recipe, explicitly extended to other fan sizes.

    No internal vertex: retain <=2 boundary colours; otherwise use the last
    three to create a virtual palette. Internal vertex present: keep the last
    three boundary colours and its feasible palette, collapsing three distinct
    boundary colours to T. Dropping earlier pending boundary colours and the
    T collapse are hypotheses when fan != 4, not established equivalences.
    """
    if not cut:
        return ('dead',)
    row = next(iter(cut))
    if len(row) < fan:  # no internal vertex has been introduced
        assert len(cut) == 1
        if len(row) < 3:
            return ('prefix', row)
        h, b, a = row[-3:]
        palette = tuple(c for c in range(4) if c not in (a, b)) if h == a else (h,)
        return ('A', b, a, palette)
    assert len(row) == fan
    boundaries = {r[:-1] for r in cut}
    assert len(boundaries) == 1
    h, b, a = row[-4:-1]
    if h != a:
        return ('T',)
    return ('A', b, a, tuple(sorted({r[-1] for r in cut})))


def short_name(sig):
    if sig[0] == 'prefix':
        return ('E', 'S', 'P')[len(sig[1])]
    if sig[0] == 'A':
        assert sig[1:3] == (1, 0)
        return {(2, 3): 'A_cd', (2,): 'A_c', (3,): 'A_d'}[sig[3]]
    return sig[0]


def build_model(fan):
    order, delta, _ = automaton((fan,))
    cls, rows, live, reps = quotient(order, delta)
    return dict(fan=fan, order=order, delta=delta, cls=cls, rows=rows,
                live=live, reps=reps, start=cls[0])


def first_collision(model, minimum_length):
    # Exhaustive equal-length search; no fixed maximum or sampled histories.
    counts = {}
    n = minimum_length
    while True:
        candidates = []
        for word in product(range(4), repeat=n):
            if tuple(frame(word)[c] for c in word) != word:
                continue
            state = run(model['delta'], 0, word)
            cut = model['order'][state]
            if cut:
                candidates.append((word, model['cls'][state], signature(cut, 5)))
        counts[n] = len(candidates)
        for j, (u, q, sig) in enumerate(candidates):
            for v, r, other in candidates[j+1:]:
                if sig == other and q != r:
                    suffix = separator(model['rows'], model['live'], q, r)
                    witnesses = []
                    for w in (u, v):
                        prefix = direct_colouring((5,), w)
                        continued = direct_colouring((5,), w + suffix)
                        assert prefix is not None
                        assert (continued is not None) == model['live'][run(model['rows'], model['start'], w + suffix)]
                        witnesses.append(dict(history=w,
                            cut=sorted(model['order'][run(model['delta'], 0, w)]),
                            prefix_colouring=prefix, continued_colouring=continued))
                    return dict(length=n, signature=sig, histories=[u, v],
                                suffix=suffix, outcomes=[x['continued_colouring'] is not None for x in witnesses],
                                candidate_counts=counts, witnesses=witnesses)
        n += 1


def analyse():
    f4, f5 = build_model(4), build_model(5)
    cls, rows, live, reps = (f4[k] for k in ('cls', 'rows', 'live', 'reps'))
    by_sig, by_class, cuts = {}, {}, {}
    for s, cut in enumerate(f4['order']):
        sig, q = signature(cut, 4), cls[s]
        assert by_sig.setdefault(sig, q) == q
        assert by_class.setdefault(q, sig) == sig
        cuts.setdefault(q, set()).add(tuple(sorted(cut)))
    assert len(by_sig) == len(rows) == 55
    # All fixed-label classes, with shortest reachable representatives.
    raw_classes = [dict(id=q, signature=by_class[q], representative=reps[q],
                        live=live[q], delta=rows[q], cut_variants=sorted(cuts[q]))
                   for q in sorted(rows)]
    # Verify the group action before constructing the aligned register machine.
    action = {(q, p): run(rows, f4['start'], tuple(p[c] for c in w))
              for q, w in reps.items() for p in PERMS}
    for (q, p), t in action.items():
        assert live[q] == live[t]
        for i in range(4):
            assert action[rows[q][i], p] == rows[t][p[i]]
    paths = {f4['start']: ()}
    todo = deque(paths)
    aligned = {}
    while todo:
        q = todo.popleft()
        w = paths[q]
        sig = by_class[q]
        name = short_name(sig)
        targets = [action[rows[q][i], MOVES[i]] for i in range(4)]
        aligned[name] = dict(raw_class=q, signature=sig, representative=w,
                             live=live[q], delta=[short_name(by_class[t]) for t in targets])
        for i, t in enumerate(targets):
            if t not in paths:
                paths[t] = tuple(MOVES[i][c] for c in w + (i,))
                assert run(rows, f4['start'], paths[t]) == t
                todo.append(t)
    assert len(aligned) == 8
    # Minimality certificates: every pair of raw residual classes is separated.
    # Recheck ALL certificates through an independent full-graph solver.
    separators = []
    for q in sorted(rows):
        for r in sorted(rows):
            if q >= r:
                continue
            suffix = separator(rows, live, q, r)
            outcomes = []
            for state in (q, r):
                accepted = direct_colouring((4,), reps[state] + suffix) is not None
                assert accepted == live[run(rows, state, suffix)]
                outcomes.append(accepted)
            assert outcomes[0] != outcomes[1]
            separators.append([q, r, suffix])
    aligned_separators = []
    for j, (name, entry) in enumerate(aligned.items()):
        for other, target in list(aligned.items())[j+1:]:
            suffix = separator(rows, live, entry['raw_class'], target['raw_class'])
            aligned_separators.append([name, other, suffix])
    general = first_collision(f5, 0)
    mature = first_collision(f5, 5)
    assert general['histories'] == [(0,2,1,0), (3,2,1,0)] and general['suffix'] == (1,)
    assert mature['histories'] == [(0,2,0,1,0), (2,1,0,1,0)] and mature['suffix'] == (1,)
    replays = 0
    for n in range(8):
        for word in product(range(4), repeat=n):
            if tuple(frame(word)[c] for c in word) != word:
                continue
            for model in (f4, f5):
                actual = direct_colouring((model['fan'],), word) is not None
                expected = model['live'][run(model['rows'], model['start'], word)]
                assert actual == expected
                replays += 1
    return dict(status='computationally observed; not a Lean proof of graph semantics',
                minimality='55 fixed-label classes; 8 aligned register signatures with an external colour frame; pairwise residual separators',
                signature_transfer=signature.__doc__,
                collision_order='equal length, then lexicographic canonical histories; shortest lexicographic fixed-frame suffix',
                fan4=dict(raw_reachable_states=len(f4['order']), residual_classes=len(rows),
                    live_residual_classes=sum(live.values()), aligned=aligned, classes=raw_classes,
                    separators=separators, aligned_separators=aligned_separators,
                    separator_lengths=dict(sorted(Counter(len(s) for _, _, s in separators).items()))),
                fan5=dict(raw_reachable_states=len(f5['order']), residual_classes=len(f5['rows']),
                          first_collision=general, first_mature_collision=mature),
                verification=dict(all_raw_states_classified=True, action_equivariance=True,
                    independently_replayed_separator_endpoints=2*len(separators),
                    canonical_graph_replays_through_length_7=replays))


if __name__ == '__main__':
    content = json.dumps(analyse(), indent=2) + '\n'
    if '--check' in sys.argv:
        assert OUT.read_text() == content
        print('fan4 signatures: full classification, all minimality separators, fan5 first collisions, independent replay and artifact match passed')
    else:
        OUT.write_text(content)
        result = json.loads(content)
        print(json.dumps({k: result[k] for k in ('minimality', 'verification')}, indent=2))
        for key in ('first_collision', 'first_mature_collision'):
            c = result['fan5'][key]
            print(key, c['histories'], c['suffix'], c['outcomes'])
