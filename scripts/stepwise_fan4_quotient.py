#!/usr/bin/env python3
"""Fan 4 versus the aligned fan 3 quotient; exact finite checks, not a Lean proof."""
from collections import deque
from itertools import product
import json
from pathlib import Path
import sys
from stepwise_aligned_reference import automaton, minimise, run, frame, quotient, separator, direct_colouring

OUT = Path(__file__).resolve().parents[1] / 'artifacts/stepwise/fan4_quotient.json'


def analyse():
    models = {f: automaton((f,)) for f in (3, 4)}
    classes = {f: minimise(o, d) for f, (o, d, _) in models.items()}
    o, d, _ = models[4]
    # Exhaustive reachable raw states, with actual representative histories.
    paths = {0: ()}
    todo = deque([0])
    while todo:
        s = todo.popleft()
        for i, t in enumerate(d[s]):
            if t not in paths:
                paths[t] = paths[s] + (i,)
                todo.append(t)
    relations, class_map = {}, {}
    transitions = {}
    for s, w in paths.items():
        if len(w) < 4 or not o[s]:
            continue
        p = frame(w)
        rel = tuple(sorted(tuple(p[c] for c in row) for row in o[s]))
        normalized = tuple(p[c] for c in w)
        q = classes[4][run(d, 0, normalized)]
        assert class_map.setdefault(rel, q) == q
        relations.setdefault(rel, normalized)
        for i in range(4):
            move = tuple(0 if j == i else j + 1 if j < i else j for j in range(4))
            # Each tuple is (third-last boundary, b, a, last internal).
            predicted = tuple(sorted({tuple(move[z] for z in (b, a, i, y))
                for h, b, a, x in rel for y in range(4)
                if i != a and y not in (h, b, a, i) and y != x}))
            t = d[s][p.index(i)]
            actual = tuple(sorted(tuple(move[p[c]] for c in row) for row in o[t]))
            assert predicted == actual
            assert transitions.setdefault((rel, i), predicted) == predicted
    assert len(relations) == len(set(class_map.values())) == 4
    names = {((0, 1, 0, 2), (0, 1, 0, 3)): 'A_cd',
             ((0, 1, 0, 2),): 'A_c', ((0, 1, 0, 3),): 'A_d',
             ((2, 1, 0, 3),): 'T'}
    assert set(names) == set(relations)
    # Define "first": equal length >=4, each already in its recency frame,
    # live in both models; length then lexicographic pair, then shortest suffix.
    first = None
    counts = {}
    for n in range(4, 6):
        candidates = []
        for w in product(range(4), repeat=n):
            if tuple(frame(w)[c] for c in w) != w:
                continue
            states = {f: run(models[f][1], 0, w) for f in models}
            if all(models[f][0][states[f]] for f in models):
                candidates.append((w, classes[3][states[3]], classes[4][states[4]]))
        counts[n] = len(candidates)
        for j, (u, q3, q4) in enumerate(candidates):
            for v, r3, r4 in candidates[j+1:]:
                if q3 == r3 and q4 != r4:
                    _, rows, live, _ = quotient(o, d)
                    suffix = separator(rows, live, q4, r4)
                    first = dict(histories=[u, v], suffix=suffix)
                    break
            if first:
                break
        if first:
            break
    assert first == dict(histories=[(2,1,0,1,0),(2,1,2,1,0)], suffix=(1,))
    replay = []
    for w in first['histories']:
        entry = dict(history=w, models={})
        for f in models:
            fo, fd, _ = models[f]
            entry['models'][f] = dict(frontier=sorted(fo[run(fd,0,w)]),
                prefix_colouring=direct_colouring((f,),w),
                continued_colouring=direct_colouring((f,),w+first['suffix']))
            assert entry['models'][f]['prefix_colouring'] is not None
            assert (entry['models'][f]['continued_colouring'] is not None) == bool(fo[run(fd,0,w+first['suffix'])])
        replay.append(entry)
    checked = 0
    for n in range(7):
        for w in product(range(4), repeat=n):
            if tuple(frame(w)[c] for c in w) != w:
                continue
            for f, (fo, fd, _) in models.items():
                assert (direct_colouring((f,),w) is not None) == bool(fo[run(fd,0,w)])
                checked += 1
    return dict(status='computationally observed; graph semantics not proved in Lean',
        ordering='equal length >=4; canonical a=0,b=1,c=2,d=3; lexicographic histories; shortest lexicographic suffix',
        candidates_by_length=counts, first=first, witnesses=replay,
        states={names[r]: dict(frontier=r, representative=relations[r],
            transitions=[names[transitions[r,i]] if transitions[r,i] else 'dead' for i in range(4)]) for r in sorted(relations)},
        exhaustive_raw_states_checked=len(paths), independent_graph_replays=checked)


if __name__ == '__main__':
    result = json.dumps(analyse(), indent=2) + '\n'
    if '--check' in sys.argv:
        assert OUT.read_text() == result
        print('fan4 quotient: exact closure, first pair, independent graph replay, artifact match passed')
    else:
        OUT.write_text(result)
        print(result)
