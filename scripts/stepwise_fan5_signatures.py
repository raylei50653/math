#!/usr/bin/env python3
"""Dissect all 97 fan-5 residuals; no fan-6 exploration.

Structural classification and transition rules are independent of Moore class
IDs. Exhaustive finite checks and full-graph separator replay, not a Lean proof.
"""
from collections import Counter, deque
from itertools import product
import json
from pathlib import Path
import sys

from stepwise_fan4_signatures import (
    MOVES, PERMS, build_model, direct_colouring, frame, run, separator,
)

OUT = Path(__file__).resolve().parents[1] / 'artifacts/stepwise/fan5_signatures.json'
COLORS = frozenset(range(4))
DEAD = ('dead',)
STOP = ('T',)


def signature(cut):
    if not cut:
        return DEAD
    row = next(iter(cut))
    if len(row) <= 3:
        assert len(cut) == 1
        return ('prefix', row)
    if len(row) == 4:  # Four committed boundary colours, no interior yet.
        assert len(cut) == 1
        h, j, b, a = row
        if len(set(row)) == 4:
            return STOP
        if j == a:
            palette = tuple(sorted(COLORS - {a, b})) if h == b else (h,)
            return ('A', b, a, palette)
        return ('F', tuple(sorted(set(row) - {a})))
    assert len(row) == 5
    assert len({r[:-1] for r in cut}) == 1
    boundary = row[:-1]
    if len(set(boundary)) == 3:
        return STOP
    assert len(set(boundary)) == 2
    return ('A', boundary[-2], boundary[-1], tuple(sorted({r[-1] for r in cut})))


def step(sig, i):
    """Fixed-label structural update, without the DFA or its class IDs."""
    tag = sig[0]
    if tag in ('dead', 'T'):
        return DEAD
    if tag == 'F':
        return STOP if i in sig[1] else DEAD
    if tag == 'prefix':
        w = sig[1]
        if w and w[-1] == i:
            return DEAD
        return signature(frozenset({w + (i,)}))
    assert tag == 'A'
    _, b, a, palette = sig
    if i == a:
        return DEAD
    new_palette = tuple(y for y in range(4) if y not in (a, b, i)
                        and any(x != y for x in palette))
    if not new_palette:
        return DEAD
    if i != b:
        return STOP
    return ('A', a, b, new_palette)


def name(sig):
    tag = sig[0]
    if tag == 'prefix':
        w = sig[1]
        if len(w) < 3:
            return ('E', 'S', 'P')[len(w)]
        return 'U_aba' if w[0] == w[2] else 'U_cba'
    if tag == 'A':
        assert sig[1:3] == (1, 0)
        return {(2,3): 'A_cd', (2,): 'A_c', (3,): 'A_d'}[sig[3]]
    if tag == 'F':
        assert sig[1] == (1, 2)
        return 'F_bc'
    return tag


def analyse():
    model = build_model(5)
    order, delta, cls, rows, live, reps = (model[k] for k in
        ('order', 'delta', 'cls', 'rows', 'live', 'reps'))
    by_sig, by_class, variants = {}, {}, {}
    for state, cut in enumerate(order):
        sig, q = signature(cut), cls[state]
        assert by_sig.setdefault(sig, q) == q
        assert by_class.setdefault(q, sig) == sig
        variants.setdefault(q, set()).add(tuple(sorted(cut)))
        for i in range(4):
            assert step(sig, i) == signature(order[delta[state][i]])
    assert len(by_sig) == len(rows) == 97
    raw_classes = [dict(id=q, signature=by_class[q], representative=reps[q],
                        live=live[q], delta=rows[q], cut_variants=sorted(variants[q]))
                   for q in sorted(rows)]
    # Explicit aligned action, not an independent symmetry quotient.
    action = {(q, p): run(rows, model['start'], tuple(p[c] for c in w))
              for q, w in reps.items() for p in PERMS}
    for (q, p), t in action.items():
        assert live[q] == live[t]
        for i in range(4):
            assert action[rows[q][i], p] == rows[t][p[i]]
    paths = {model['start']: ()}
    todo = deque(paths)
    aligned = {}
    while todo:
        q = todo.popleft()
        targets = [action[rows[q][i], MOVES[i]] for i in range(4)]
        aligned[name(by_class[q])] = dict(raw_class=q, representative=paths[q],
            signature=by_class[q], live=live[q], delta=[name(by_class[t]) for t in targets])
        for i, t in enumerate(targets):
            if t not in paths:
                paths[t] = tuple(MOVES[i][c] for c in paths[q] + (i,))
                assert run(rows, model['start'], paths[t]) == t
                todo.append(t)
    assert len(aligned) == 11
    # Reachability at arbitrarily large lengths, via exact set iteration.
    reached, seen, sequence = frozenset({model['start']}), {}, []
    while reached not in seen:
        seen[reached] = len(sequence)
        sequence.append(reached)
        reached = frozenset(action[rows[q][i], MOVES[i]] for q in reached for i in range(4))
    recurrent = frozenset().union(*sequence[seen[reached]:])
    recurrent_names = sorted(name(by_class[q]) for q in recurrent if live[q])
    assert recurrent_names == ['A_c', 'A_cd', 'A_d', 'T']
    separators = []
    for q in sorted(rows):
        for r in sorted(rows):
            if q >= r:
                continue
            suffix = separator(rows, live, q, r)
            outcomes = []
            for state in (q, r):
                actual = direct_colouring((5,), reps[state] + suffix) is not None
                assert actual == live[run(rows, state, suffix)]
                outcomes.append(actual)
            assert outcomes[0] != outcomes[1]
            separators.append([q, r, suffix])
    aligned_separators = []
    for j, (label, item) in enumerate(aligned.items()):
        for other, target in list(aligned.items())[j+1:]:
            suffix = separator(rows, live, item['raw_class'], target['raw_class'])
            aligned_separators.append([label, other, suffix])
    # Independent graph replay of every raw-state representative (including
    # the actual left-end phases, not just representatives after minimisation).
    raw_paths = {0: ()}
    todo = deque([0])
    while todo:
        q = todo.popleft()
        for i, t in enumerate(delta[q]):
            if t not in raw_paths:
                raw_paths[t] = raw_paths[q] + (i,)
                todo.append(t)
    assert len(raw_paths) == len(order)
    for state, word in raw_paths.items():
        assert (direct_colouring((5,), word) is not None) == bool(order[state])
    replay_count = 0
    for n in range(9):
        for w in product(range(4), repeat=n):
            if tuple(frame(w)[c] for c in w) != w:
                continue
            actual = direct_colouring((5,), w) is not None
            assert actual == live[run(rows, model['start'], w)]
            replay_count += 1
    # Full-colouring witnesses for semantic merges: unlike histories, same
    # residual. Include both a permitted and a forbidden continuation.
    merges = []
    for u, v, suffixes in [
        ((1,0,1,0), (0,1,0,1,0), [(1,), (2,), (2,1)]),
        ((2,0,1,0), (2,0,1,0,1,0), [(1,), (2,), (3,)]),
        ((0,2,1,0), (1,2,1,0), [(1,), (2,), (3,), (1,2)]),
        ((3,2,1,0), (0,2,0,1,0), [(), (1,)])]:
        q = run(rows, model['start'], u)
        assert q == run(rows, model['start'], v)
        checks = []
        for suffix in suffixes:
            witnesses = [direct_colouring((5,), w + suffix) for w in (u, v)]
            assert all((x is not None) == live[run(rows, q, suffix)] for x in witnesses)
            checks.append(dict(suffix=suffix, colourings=witnesses))
        merges.append(dict(histories=[u,v], raw_class=q, signature=by_class[q], checks=checks))
    counts = Counter()
    for sig in by_sig:
        tag = sig[0]
        if tag == 'prefix':
            w = sig[1]
            tag = ('E', 'S', 'P')[len(w)] if len(w) < 3 else ('U_aba' if w[0] == w[2] else 'U_cba')
        counts[tag] += 1
    assert dict(counts) == dict(E=1, S=4, dead=1, P=12, U_aba=12, U_cba=24, A=36, F=6, T=1)
    return dict(status='computationally observed; strip graph semantics not proved in Lean',
        scope='fan 5 only; minimal signature means exact residual partition, not minimum description length',
        raw_reachable_states=len(order), residual_classes=len(rows), live_classes=sum(live.values()),
        family_counts=dict(sorted(counts.items())), aligned=aligned,
        recurrent_live_signatures=recurrent_names, classes=raw_classes,
        separators=separators, aligned_separators=aligned_separators,
        separator_lengths=dict(sorted(Counter(len(s) for _,_,s in separators).items())),
        semantic_merges=merges,
        verification=dict(structural_transition_cases=4*len(order),
            signature_bijection=True, action_equivariance=True,
            independent_separator_endpoints=2*len(separators),
            independent_raw_representatives=len(raw_paths), canonical_replays_through_length_8=replay_count))


if __name__ == '__main__':
    content = json.dumps(analyse(), indent=2) + '\n'
    if '--check' in sys.argv:
        assert OUT.read_text() == content
        print('fan5: full signatures and transitions, all pair separators, independent graph replays, artifact match passed')
    else:
        OUT.write_text(content)
        result = json.loads(content)
        print(json.dumps({k: result[k] for k in ('family_counts', 'recurrent_live_signatures', 'separator_lengths', 'verification')}, indent=2))
