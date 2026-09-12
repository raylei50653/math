#!/usr/bin/env python3
"""Section 3 of docs/stepwise_state_sufficiency.md on the C5 test bed:
how far is the window (a(n-1), a(n), a(n+1)) from a sufficient state, and which
finite extra relations b, c, d close the gap?

python scripts/stepwise_window_state.py      # writes artifacts/stepwise/window_state.json

History H = (inside patch Sigma_in, legal ring prefix a(0..m-1)), forward-only.
Continuation = the remaining ring colours followed by a library outside patch
(87 patches x 10 dihedral alignments).  Two histories are *indistinguishable*
(Myhill-Nerode) iff every continuation gives the same completable/dead verdict.
The window is the last three committed colours (for m = 5 the ring is closed and the
window is taken around position 0: a(4), a(0), a(1)).

Predicate pool for b, c, d:
  eq(i,j)      a(i) = a(j) for committed positions
  ncol>=3, ncol=4   number of colours used so far
  pair(i,j)    conditional forcing status of Sigma_in on ring pair (i,j) given the
               prefix literals (forced_equal / forced_different / free / infeasible),
               for pairs with at least one uncommitted position
  four_ok / three_ok   Sigma_in still admits a completion using 4 / at most 3 colours
               (added after the first counterexample: pair statuses miss the colour count)
The script reports the smallest subsets of the pool that, together with the window,
refine the indistinguishability partition.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
import json
from math import log2, ceil

from stepwise_sufficiency import FAN, OUT, RING, Bits, align, dihedral, normalize, sigma_from_edges


def legal_prefixes(bits, m):
    if m == RING:
        return sorted(p for p in bits.index if p[0] != p[-1])
    return [p for p in bits.prefixes[m] if all(p[j] != p[j + 1] for j in range(m - 1))]


def completions(bits, p):
    m = len(p)
    if m == RING:
        return {(): p}
    out = {}
    for rest in product(range(4), repeat=RING - m):
        full = normalize(p + rest)
        if full in bits.index:
            out[rest] = full
    return out


def window(p):
    if len(p) == RING:
        return normalize((p[-1], p[0], p[1]))
    return normalize(p[-3:])


def pair_status(sigma, p, i, j):
    """Status of ring pair (i, j) under Sigma_in restricted to patterns extending p."""
    live = live_patterns(sigma, p)
    if not live:
        return 'infeasible'
    eq = {q[i] == q[j] for q in live}
    return 'free' if len(eq) == 2 else 'forced_equal' if True in eq else 'forced_different'


def predicate_pool(m):
    pool = {}
    for i, j in combinations(range(m), 2):
        pool[f'eq({i},{j})'] = lambda sigma, p, i=i, j=j: p[i] == p[j]
    pool['ncol>=3'] = lambda sigma, p: len(set(p)) >= 3
    pool['ncol=4'] = lambda sigma, p: len(set(p)) == 4
    for i, j in combinations(range(RING), 2):
        if j >= m:
            pool[f'pair({i},{j})'] = lambda sigma, p, i=i, j=j: pair_status(sigma, p, i, j)
    if m == RING:
        pool['accepted'] = lambda sigma, p: p in sigma
    if m < RING:
        # discovered by the first counterexample: pair statuses cannot see the colour count
        pool['four_ok'] = lambda sigma, p: any(max(q) == 3 for q in live_patterns(sigma, p))
        pool['three_ok'] = lambda sigma, p: any(max(q) <= 2 for q in live_patterns(sigma, p))
    return pool


def live_patterns(sigma, p):
    return [q for q in sigma if normalize(q[:len(p)]) == p]


def refines(keys, classes):
    """Do the key values, per history, separate every pair of distinct classes?"""
    seen = {}
    for h, key in keys.items():
        c = classes[h]
        if seen.setdefault(key, c) != c:
            return False
    return True


def minimal_subsets(pool_values, window_values, classes, max_size=None):
    names = list(pool_values)
    found = []
    for size in range(0, (len(names) if max_size is None else max_size) + 1):
        for subset in combinations(names, size):
            keys = {h: (window_values[h],) + tuple(pool_values[n][h] for n in subset)
                    for h in classes}
            if refines(keys, classes):
                found.append(list(subset))
        if found:
            return size, found
    return None, []


def main():
    data = json.loads((FAN / 'states.json').read_text())
    bits = Bits([tuple(p) for p in data['pattern_order']])
    sigmas = [sigma_from_edges([tuple(e) for e in s['edges']]) for s in data['states']]
    outs = [align(sigmas[x], g) for x in range(len(sigmas)) for g in dihedral()]
    # which full ring patterns can the library outsides tell apart?
    signature = {q: tuple(q in o for o in outs) for q in bits.index}
    pattern_class = {q: min(r for r in bits.index if signature[r] == signature[q]) for q in bits.index}
    report = dict(scope=__doc__.split('\n\n')[2],
                  outside_separates_all_patterns=len(set(signature.values())) == len(bits.index),
                  depths={})
    for m in (3, 4, RING):
        prefixes = legal_prefixes(bits, m)
        comps = {p: completions(bits, p) for p in prefixes}
        histories = [(i, p) for i in range(len(sigmas)) for p in prefixes]
        # Nerode signature: for each remaining-ring continuation, the outside-visible class
        # of the resulting pattern if the inside accepts it, else None.
        sig = {}
        for i, p in histories:
            sig[(i, p)] = tuple((rest, pattern_class[q] if q in sigmas[i] else None)
                                for rest, q in sorted(comps[p].items()))
        classes = {h: sig[h] for h in histories}
        alive = {h for h in histories if any(c is not None for _, c in sig[h])}
        distinct = len(set(classes.values()))
        win = {h: window(h[1]) for h in histories}
        per_window = Counter()
        for h in histories:
            per_window[(win[h], classes[h])] += 1
        classes_per_window = Counter(w for w, _ in per_window)
        pool = predicate_pool(m)
        pool_values = {name: {h: f(sigmas[h[0]], h[1]) for h in histories} for name, f in pool.items()}
        size, subsets = minimal_subsets(pool_values, win, classes)
        # the same search restricted to alive histories (dead ones need no state)
        alive_classes = {h: classes[h] for h in alive}
        size_alive, subsets_alive = minimal_subsets(
            {n: {h: v[h] for h in alive} for n, v in pool_values.items()},
            {h: win[h] for h in alive}, alive_classes)
        # how far does the *whole* pool get, and one concrete counterexample if it fails
        full_key = {h: (win[h],) + tuple(pool_values[n][h] for n in pool) for h in histories}
        merged = defaultdict(set)
        for h in histories:
            merged[full_key[h]].add(classes[h])
        counterexample = None
        for key, cls in merged.items():
            if len(cls) > 1:
                hs = [h for h in histories if full_key[h] == key]
                h1 = hs[0]
                h2 = next(h for h in hs if classes[h] != classes[h1])
                rest, c1, c2 = next((r, c1, c2) for (r, c1), (_, c2) in zip(sig[h1], sig[h2]) if c1 != c2)
                q1, q2 = comps[h1[1]][rest], comps[h2[1]][rest]
                # an outside accepting exactly one of the two resulting patterns
                x = next(k for k, o in enumerate(outs) if (q1 in o and c1 is not None) != (q2 in o and c2 is not None))
                counterexample = dict(history_1=dict(inside=h1[0], prefix=h1[1]),
                                      history_2=dict(inside=h2[0], prefix=h2[1]),
                                      shared_key=dict(zip(['window'] + list(pool), key)),
                                      continuation=dict(rest_of_ring=rest, outside=x // 10, alignment=dihedral()[x % 10]),
                                      pattern_1=q1, accepted_1=c1 is not None and q1 in outs[x],
                                      pattern_2=q2, accepted_2=c2 is not None and q2 in outs[x])
                break
        report['depths'][f'm={m}'] = dict(
            full_pool_keys=len(merged),
            full_pool_merged_classes=sum(len(c) - 1 for c in merged.values()),
            full_pool_counterexample=counterexample,
            histories=len(histories), alive=len(alive), legal_prefixes=len(prefixes),
            nerode_classes=distinct, nerode_classes_alive=len(set(alive_classes.values())),
            window_values=len(classes_per_window),
            nerode_classes_per_window=dict((str(k), v) for k, v in sorted(classes_per_window.items())),
            extra_bits_needed=ceil(log2(max(classes_per_window.values()))),
            pool_size=len(pool),
            minimal_predicate_sets=dict(size=size, sets=subsets[:12], count=len(subsets)),
            minimal_predicate_sets_alive_only=dict(size=size_alive, sets=subsets_alive[:12],
                                                   count=len(subsets_alive)))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'window_state.json').write_text(json.dumps(report, indent=1, default=repr) + '\n')
    print('library outsides separate all 10 ring patterns:', report['outside_separates_all_patterns'])
    for m, r in report['depths'].items():
        print(f"{m}: histories {r['histories']} (alive {r['alive']}), Nerode classes {r['nerode_classes']}"
              f" (alive {r['nerode_classes_alive']}), window values {r['window_values']},"
              f" classes per window {r['nerode_classes_per_window']}, extra bits {r['extra_bits_needed']}")
        print(f"   full pool: {r['full_pool_keys']} keys, {r['full_pool_merged_classes']} classes merged; "
              f"counterexample {r['full_pool_counterexample']}")
        for label in ('minimal_predicate_sets', 'minimal_predicate_sets_alive_only'):
            s = r[label]
            print(f"   {label}: size {s['size']} ({s['count']} sets) e.g. {s['sets'][:4]}")


if __name__ == '__main__':
    main()
