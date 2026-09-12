#!/usr/bin/env python3
"""Trial seven: aligned residuals, exact register updates, replayable separators.

Pure stdlib. No claim of planarity, general depth growth, or Lean graph soundness.
The finite DFA is exact for the finite-prefix strip colouring language defined by
stepwise_strip_width. An accepting prefix need not accept every future suffix.
Run directly to write aligned_reference.json; --check compares the whole artifact.
"""
from collections import deque
from itertools import product
import json
from pathlib import Path
import sys

from stepwise_strip_width import automaton, minimise, PERMS
from stepwise_remote_reference import features, live_words, FEATURES, run_channels

OUT = Path(__file__).resolve().parents[1] / 'artifacts/stepwise'
SHAPES = [(3,), (4,), (2, 3), (2, 4), (2, 2, 3), (2, 2, 4)]


def run(delta, state, word):
    for c in word:
        state = delta[state][c]
    return state


def quotient(order, delta):
    cls = minimise(order, delta)
    rows, live = {}, {}
    for i, row in enumerate(delta):
        q = cls[i]
        target = tuple(cls[j] for j in row)
        assert rows.setdefault(q, target) == target
        assert live.setdefault(q, bool(order[i])) == bool(order[i])
    words = {cls[0]: ()}
    todo = deque(words)
    while todo:
        q = todo.popleft()
        for c, t in enumerate(rows[q]):
            if t not in words:
                words[t] = words[q] + (c,)
                todo.append(t)
    return cls, rows, live, words


def separator(delta, live, p, q):
    todo = deque([(p, q, ())])
    seen = {(p, q)}
    while todo:
        a, b, word = todo.popleft()
        if live[a] != live[b]:
            return word
        for c in range(4):
            pair = delta[a][c], delta[b][c]
            if pair not in seen:
                seen.add(pair)
                todo.append((*pair, word + (c,)))
    raise AssertionError('distinct minimal classes have no separator')


def finite_window_certificate(delta, live, words):
    """All live distinct pairs; iterated image reaches empty or a fixed point.

    If nonempty, exhibit a cycle: two live prefixes followed by arbitrarily
    many copies of one common nonempty word still have different residuals.
    """
    qs = sorted(q for q in delta if live[q])
    pairs = {(a, b) for a in qs for b in qs if a < b}

    def edges(pair):
        for c in range(4):
            a, b = (delta[q][c] for q in pair)
            if a != b and live[a] and live[b]:
                yield c, tuple(sorted((a, b)))

    depth = 0
    while pairs:
        nxt = {t for pair in pairs for _, t in edges(pair)}
        if nxt == pairs:
            break
        assert nxt < pairs
        pairs = nxt
        depth += 1
    if not pairs:
        return dict(minimum_k=depth, cycle=None)
    # A finite nonempty image-fixed set has a cycle. Walk predecessors.
    pred = {}
    for pair in sorted(pairs):
        for c, t in edges(pair):
            if t in pairs:
                pred.setdefault(t, (pair, c))
    seen, trail = {}, []
    pair = min(pairs)
    while pair not in seen:
        seen[pair] = len(trail)
        trail.append(pair)
        pair = pred[pair][0]
    cycle_nodes = trail[seen[pair]:]
    word = tuple(pred[t][1] for t in reversed(cycle_nodes))
    a, b = pair
    assert tuple(sorted((run(delta, a, word), run(delta, b, word)))) == pair
    # Double the word if it swaps the ordered pair.
    if run(delta, a, word) != a:
        word *= 2
    assert run(delta, a, word) == a and run(delta, b, word) == b
    suffix = separator(delta, live, a, b)
    return dict(minimum_k=None, fixed_point_pairs=len(pairs), cycle=dict(
        prefixes=[list(words[a]), list(words[b])], loop=list(word),
        separator=list(suffix), outcomes=[live[run(delta, q, suffix)] for q in pair]))


def frame(word):
    """Absolute colours to directional first-encounter a,b,c,d ranks.

    Direction is backwards into committed history: dist(a,b)<dist(a,c)<dist(a,d).
    This is a naming convention, not a claim that nearest-occurrence features
    summarize all constraints. The opposite direction is not tested here.

    Unseen colours are interchangeable; the numeric tie-break has no semantic
    effect since the residual is invariant under permutations of unseen colours.
    """
    last = {c: i for i, c in enumerate(word)}
    names = sorted(range(4), key=lambda c: (-last.get(c, -1), c))
    return tuple(names.index(c) for c in range(4))


def direct_colouring(fans, boundary):
    """Independent full-graph backtracking, no frontier/DFA/build helpers.

    Include exactly the vertices whose entire lower fan has been introduced.
    Return an actual full colouring, or None after exhaustive search.
    """
    lengths = [len(boundary)]
    for f in fans:
        lengths.append(max(0, lengths[-1] - f + 1))
    vertices = [(r, i) for r, n in enumerate(lengths) for i in range(n)]
    adj = {v: set() for v in vertices}

    def edge(a, b):
        adj[a].add(b)
        adj[b].add(a)

    for r, n in enumerate(lengths):
        for i in range(n):
            if i:
                edge((r, i - 1), (r, i))
            if r:
                for j in range(fans[r - 1]):
                    edge((r, i), (r - 1, i + j))
    assigned = {(0, i): c for i, c in enumerate(boundary)}
    if any(assigned[u] == assigned[v] for u in assigned for v in adj[u] if v in assigned):
        return None

    def solve():
        if len(assigned) == len(vertices):
            return dict(assigned)
        choices = []
        for v in vertices:
            if v not in assigned:
                allowed = tuple(c for c in range(4) if all(assigned.get(u) != c for u in adj[v]))
                if not allowed:
                    return None
                choices.append((len(allowed), -len(adj[v]), v, allowed))
        _, _, v, allowed = min(choices)
        for c in allowed:
            assigned[v] = c
            result = solve()
            if result is not None:
                return result
        del assigned[v]
        return None

    result = solve()
    if result is not None:
        assert all(result[u] != result[v] for u in vertices for v in adj[u])
        return [[r, i, result[r, i]] for r, i in vertices]
    return None


def analyse(fans):
    order, delta, _ = automaton(fans)
    cls, rows, live, reps = quotient(order, delta)
    start = cls[0]
    # Permute the representative WORD, not an independently quotient-ed relation.
    action = {(q, p): run(rows, start, tuple(p[c] for c in w))
              for q, w in reps.items() for p in PERMS}
    for (q, p), t in action.items():
        assert live[q] == live[t]
        for c in range(4):
            assert action[rows[q][c], p] == rows[t][p[c]]

    # Reading rank i moves that colour to the front; reframe the residual with
    # the SAME permutation. Closure is exhaustive, including the left end.
    moves = [tuple(0 if j == i else j + 1 if j < i else j for j in range(4)) for i in range(4)]
    ids, states, trans = {start: 0}, [start], []
    for q in states:
        row = []
        for i in range(4):
            t = action[rows[q][i], moves[i]]
            if t not in ids:
                ids[t] = len(states)
                states.append(t)
            row.append(ids[t])
        trans.append(row)
    register = dict(start=0, live=[live[q] for q in states], delta=trans,
                    live_states=sum(live[q] for q in states), total_states=len(states))
    reached, seen, sequence = frozenset([0]), {}, []
    while reached not in seen:
        seen[reached] = len(sequence)
        sequence.append(reached)
        reached = frozenset(trans[q][c] for q in reached for c in range(4))
    recurrent = frozenset().union(*sequence[seen[reached]:])
    register['recurrent_live_states'] = sum(live[states[q]] for q in recurrent)
    if fans == (3,):
        # Obtain a mature history for every recurrent register state, and expose
        # the three values as actual frontier palettes in the current frame.
        paths = {(0, 0): ()}
        todo = deque(paths)
        while todo:
            q, length = todo.popleft()
            for rank, t in enumerate(trans[q]):
                key = t, min(10, length + 1)
                if key not in paths:
                    paths[key] = paths[q, length] + (rank,)
                    todo.append(key)
        palettes = {}
        for q in sorted(recurrent):
            if not live[states[q]]:
                continue
            names, word = list(range(4)), []
            for rank in paths[q, 10]:
                word.append(names[rank])
                names.insert(0, names.pop(rank))
            p = frame(word)
            relation = {tuple(p[c] for c in col) for col in order[run(delta, 0, word)]}
            palette = sorted({col[-1] for col in relation})
            assert relation == {(1, 0, c) for c in palette}
            palettes[q] = palette
        assert sorted(palettes.values()) == [[2], [2, 3], [3]]
        # Independent local rule: the new fan sees old b, old a, input i;
        # its internal colour must differ from some feasible old internal colour.
        for q, palette in palettes.items():
            for i, t in enumerate(trans[q]):
                allowed = [] if i == 0 else sorted({moves[i][y] for y in range(4)
                    if y not in (0, 1, i) and any(x != y for x in palette)})
                assert allowed == (palettes[t] if live[states[t]] else [])
        register['fan3_frontier_palettes'] = {str(q): cs for q, cs in palettes.items()}
        register['fan3_palette_rule_verified'] = True

    def aligned(word):
        p = frame(word)
        return tuple(p[c] for c in word)

    def witness(w, v):
        u, z = aligned(w), aligned(v)
        a, b = run(rows, start, u), run(rows, start, z)
        suffix = separator(rows, live, a, b)
        outcomes, colourings = [], []
        for prefix in (u, z):
            result = direct_colouring(fans, prefix + suffix)
            outcome = live[run(rows, start, prefix + suffix)]
            assert (result is not None) == outcome
            assert direct_colouring(fans, prefix) is not None
            outcomes.append(outcome)
            colourings.append(result)
        assert outcomes[0] != outcomes[1]
        return dict(histories=[list(u), list(z)], suffix=list(suffix),
                    outcomes=outcomes, full_colourings=colourings)

    sample, T, total, how = live_words(order, delta)
    records = [(w, action[cls[s], frame(w)], features(w)) for w, s in sample]
    old = json.loads((OUT / 'remote_reference.json').read_text())['fans' + ''.join(map(str, fans))]
    candidates = {'all_features_window3': lambda f: (f['window'][-3:], *(f[n] for n in FEATURES))}
    for names in old['minimal_sufficient']['window0']:
        candidates['old_window0:' + ','.join(names)] = lambda f, names=names: tuple(f[n] for n in names)
    best = old['run_channels']['minimal_cap_runs']
    if best:
        candidates['old_best_runs'] = lambda f: (f['window'][-3:], f['self'], run_channels(f, *best))
    results = {}
    for name, key in candidates.items():
        table, collision = {}, None
        for w, q, f in records:
            old_q, old_w = table.setdefault(key(f), (q, w))
            if old_q != q:
                collision = witness(old_w, w)
                left, right = (tuple(h) for h in collision['histories'])
                assert key(features(left)) == key(features(right))
                break
        results[name] = dict(sample_sufficient=collision is None, counterexample=collision)

    cycle = finite_window_certificate(rows, live, reps)
    if cycle['cycle']:
        cert = cycle['cycle']
        for k in (0, 1, 2, 5):
            for prefix, expected in zip(cert['prefixes'], cert['outcomes']):
                word = tuple(prefix + cert['loop'] * k + cert['separator'])
                assert (direct_colouring(fans, word) is not None) == expected

    # Independent complete short-prefix check, canonical words cover every S4 orbit.
    checked = 0
    for n in range(7):
        for w in product(range(4), repeat=n):
            names = {}
            canonical = tuple(names.setdefault(c, len(names)) for c in w)
            if w != canonical:
                continue
            assert (direct_colouring(fans, w) is not None) == live[run(rows, start, w)]
            names, state = list(range(4)), 0
            for c in w:
                rank = names.index(c)
                state = trans[state][rank]
                names.insert(0, names.pop(rank))
            assert states[state] == action[run(rows, start, w), frame(w)]
            checked += 1
    small = None
    if fans == (3,):
        w, v = (1, 2, 1, 0), (2, 0, 1, 0)
        assert frame(w) == frame(v) == tuple(range(4))
        assert features(w)['present'] == features(v)['present']
        small = witness(w, v)
    return dict(fans=list(fans), status='computationally observed',
                finite_window=cycle, register_automaton=register,
                small_presence_counterexample=small,
                independent_short_words=checked, sampling=how, sample_size=len(sample),
                sample_lengths=[T, T + 5], words_in_range=total,
                aligned_classes_seen=len({q for _, q, _ in records}), candidates=results)


def main():
    result = dict(scope='Fixed strip grammars; forward-only finite-prefix colouring. '
                  'Exact finite automaton computations, independent full-graph witness replay; '
                  'feature sufficiency is sampled only. No disk or arbitrary-depth theorem.', shapes={})
    for fans in SHAPES:
        name = 'fans' + ''.join(map(str, fans))
        r = analyse(fans)
        result['shapes'][name] = r
        print(name, 'register live', r['register_automaton']['live_states'],
              'recurrent', r['register_automaton']['recurrent_live_states'],
              'aligned sample classes', r['aligned_classes_seen'],
              {k: v['sample_sufficient'] for k, v in r['candidates'].items()}, flush=True)
    encoded = json.dumps(result, indent=1) + '\n'
    path = OUT / 'aligned_reference.json'
    if '--check' in sys.argv:
        assert path.read_text() == encoded, 'artifact differs'
        print('whole artifact reproduced; independent replay passed')
    else:
        path.write_text(encoded)


if __name__ == '__main__':
    main()
