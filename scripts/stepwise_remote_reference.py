#!/usr/bin/env python3
"""Is a colour-referenced remote state sufficient?  (section 3, second reading of b/c/d)

python scripts/stepwise_remote_reference.py       # ~3 min, writes artifacts/stepwise/remote_reference.json

Reading of S_n = (a(n-1), a(n), a(n+1), b^+-, c^+-, d^+-) tested here: a is the colour just
committed, the a(.) part is a local window, and b, c, d are the OTHER THREE COLOURS, each
carrying a fixed kind of information about its nearest occurrence in the history -- which
may be arbitrarily far back.  Fixed kinds of reference, unbounded reference distance.

Test bed: the exact strip automata of stepwise_strip_width.py.  For each shape the Nerode
class of a live boundary word is the ground truth for "what the future can still see".

Part A (exact, on the DFA): finite range.  Is the class a function of the last k letters?
  Pairs of live states in different classes are pushed forward letter by letter until
  empty or a nonempty fixed point. 'none' means no bounded window works.

Part B (live words of length T..T+5, T = left-end transient; exhaustive or a CAP random
        sample): colour-referenced features.
  For the current colour a and each other colour x (named by recency: the most recently
  seen other colour, the second, the third, so the state is colour-symmetric):
    present     x occurs in the history at all
    parity      distance back to the nearest x, mod 2
    after       the colour written right after that nearest x
    before      the colour written right before it
    two_col     the segment strictly between the nearest x and now uses <= 2 colours
    a_parity    number of a's strictly between the nearest x and now, mod 2
    order       the recency order of the three other colours itself (which is nearest)
  and two families about a itself / the run structure:
    self        the previous occurrence of a: present, distance parity, colour after, before
    alt         the maximal 2-coloured suffix: its length parity and the colour just before it
    first       distance parity back to the FIRST occurrence of a and of each other colour
                (a parity channel that reaches all the way to the left end)
    origin      parity of the distance to the left end b_0 itself

Part C: run channels.  The history is cut greedily from the right into maximal 2-coloured
  runs; each run is summarised by its (relative) colour pair and its length, kept exactly
  below `cap` and only mod 2 beyond it.  Candidate = window 3 + self + the last R runs.
  Reports the minimal (cap, R) that is sufficient, if any with cap <= 8, R <= 5.
  Candidate state = (last k letters normalised, chosen features).  Sufficient iff equal
  candidate states never have different Nerode classes up to a global colour permutation.
  WARNING: Parts B/C use independent colour orbits and are historical diagnostics,
  not aligned sufficiency tests. Use stepwise_aligned_reference.py for the corrected
  test under directional first-encounter naming (dist(a,b)<dist(a,c)<dist(a,d)).
  Reports minimal sufficient subsets and, for
  the full feature set with window 3, a counterexample pair if it still fails.
"""
from collections import defaultdict
from itertools import combinations
import json
import random
import sys
import time

from stepwise_strip_width import PERMS, automaton, minimise
from stepwise_sufficiency import OUT

SHAPES = [(3,), (4,), (3, 4), (3, 3, 4), (2, 3), (2, 2, 3), (2, 4), (2, 2, 4), (2, 3, 4), (3, 2, 4)]
SPAN = 5
CAP = 60_000
MAX_RUNS, MAX_CAP = 5, 8
FEATURES = ['present', 'parity', 'after', 'before', 'two_col', 'a_parity', 'order', 'self', 'alt', 'first', 'origin']


def finite_range(order, delta, cls):
    """Minimal k with class determined by the last k letters, on the quotient (minimal) DFA."""
    q_delta, q_live = {}, {}
    for i, row in enumerate(delta):
        q_delta[cls[i]] = [cls[j] for j in row]
        q_live[cls[i]] = bool(order[i])
    live = sorted(q for q in q_delta if q_live[q])
    pairs = {(p, q) for p in live for q in live if p < q}
    k = 0
    while True:
        if not pairs:
            return k
        nxt = set()
        for p, q in pairs:
            for c in range(4):
                a, b = q_delta[p][c], q_delta[q][c]
                if a != b and q_live[a] and q_live[b]:
                    nxt.add((a, b) if a < b else (b, a))
        if nxt == pairs:
            return None
        assert nxt < pairs
        pairs = nxt
        k += 1


def class_orbits(order, cls):
    """Nerode class up to a global colour permutation, per state (the colour-symmetric truth)."""
    index = {st: i for i, st in enumerate(order)}
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent.setdefault(parent[x], parent[x])
            x = parent[x]
        return x

    for i, st in enumerate(order):
        if not st:
            continue
        for p in PERMS:
            j = index[frozenset(tuple(p[c] for c in col) for col in st)]
            parent[find(cls[i])] = find(cls[j])
    return [find(c) for c in cls]


def transient(order, delta):
    """Prefix length after which the set of reachable states stops changing (left-end transient)."""
    R, seen = frozenset([0]), {}
    while R not in seen:
        seen[R] = len(seen)
        R = frozenset(delta[s][c] for s in R for c in range(4))
    return seen[R]


def live_words(order, delta, seed=0):
    """Live words of length T..T+SPAN, T = left-end transient: exhaustive when few, else a random
    walk sample (uniform among live letters) of CAP words.  Short words are excluded on purpose:
    near b_0 the deeper rows do not exist yet, and that transient is about depth, not colour."""
    T = transient(order, delta)
    lo, hi = T, T + SPAN
    counts, cnt = [], {0: 1}
    for L in range(1, hi + 1):
        nxt = {}
        for st, c in cnt.items():
            for a in range(4):
                t = delta[st][a]
                if order[t]:
                    nxt[t] = nxt.get(t, 0) + c
        cnt = nxt
        counts.append(sum(cnt.values()))
    total = sum(counts[lo - 1:hi])
    if total <= CAP:
        out, stack = [], [((), 0)]
        while stack:
            w, st = stack.pop()
            if len(w) >= lo:
                out.append((w, st))
            if len(w) == hi:
                continue
            for c in range(4):
                t = delta[st][c]
                if order[t]:
                    stack.append((w + (c,), t))
        return out, T, total, 'exhaustive'
    rng = random.Random(seed)
    out = set()
    while len(out) < CAP:
        L = rng.randint(lo, hi)
        w, st = (), 0
        for _ in range(L):
            live = [c for c in range(4) if order[delta[st][c]]]
            c = rng.choice(live)
            w, st = w + (c,), delta[st][c]
        out.add((w, st))
    return sorted(out), T, total, 'sampled'


def features(w):
    n = len(w) - 1
    a = w[n]
    last = {}
    for i, c in enumerate(w):
        last[c] = i
    others = sorted((x for x in range(4) if x != a), key=lambda x: -last.get(x, -1))
    f = {}
    f['order'] = tuple(last.get(x, -1) >= 0 for x in others)   # presence pattern in recency order
    for j, x in enumerate(others):
        if x not in last:
            f[f'present{j}'] = False
            for name in ('parity', 'after', 'before', 'two_col', 'a_parity'):
                f[f'{name}{j}'] = None
            continue
        p = last[x]
        f[f'present{j}'] = True
        f[f'parity{j}'] = (n - p) % 2
        f[f'after{j}'] = w[p + 1]
        f[f'before{j}'] = w[p - 1] if p > 0 else None
        seg = w[p + 1:n]
        f[f'two_col{j}'] = len(set(seg)) <= 2
        f[f'a_parity{j}'] = seg.count(a) % 2
    # colours are named relative to a and recency, so express 'after'/'before' relatively too
    rel = {a: 'a'}
    for j, x in enumerate(others):
        rel[x] = 'bcd'[j]
    for key in list(f):
        if key.startswith(('after', 'before')) and f[key] is not None:
            f[key] = rel[f[key]]
    packed = {'order': (f['order'],), 'window': tuple(rel[c] for c in w)}
    for nm in FEATURES:
        if nm not in ('order', 'self', 'alt', 'first', 'origin'):
            packed[nm] = tuple(f[nm + str(j)] for j in range(3))
    prev_a = [i for i in range(n) if w[i] == a]
    if prev_a:
        p = prev_a[-1]
        packed['self'] = (True, (n - p) % 2, rel[w[p + 1]], rel[w[p - 1]] if p > 0 else None)
    else:
        packed['self'] = (False, None, None, None)
    i = n
    while i > 0 and len(set(w[i - 1:n + 1])) <= 2:
        i -= 1
    packed['alt'] = ((n + 1 - i) % 2, rel[w[i - 1]] if i > 0 else None)
    first = {}
    for i, c in enumerate(w):
        first.setdefault(c, i)
    packed['first'] = tuple((n - first[x]) % 2 if x in first else None for x in [a] + others)
    packed['origin'] = (n % 2,)
    runs, end = [], n + 1
    while end > 0 and len(runs) < MAX_RUNS:
        i = end
        while i > 0 and len(set(w[i - 1:end])) <= 2:
            i -= 1
        runs.append((end - i, tuple(sorted(rel[c] for c in set(w[i:end])))))
        end = i
    packed['runs'] = tuple(runs)
    return packed


def run_channels(f, cap, R):
    return tuple((L if L < cap else cap + L % 2, pair) for L, pair in f['runs'][:R])


def sufficient(words, cls, k, names):
    table = {}
    for w, s, f in words:
        key = f['window'][len(w) - k:] if k else ()
        for nm in names:
            key += f[nm]
        if table.setdefault(key, (cls[s], w))[0] != cls[s]:
            return False, (table[key][1], w)
    return True, None


def analyse(fans):
    order, delta, cut = automaton(fans)
    raw_cls = minimise(order, delta)
    k_range = finite_range(order, delta, raw_cls)
    cls = class_orbits(order, raw_cls)      # candidate states are colour-symmetric, so compare orbits
    sample, T, total, how = live_words(order, delta)
    words = [(w, s, features(w)) for w, s in sample]
    live_classes = len({cls[s] for _, s, _ in words})
    result = dict(fans=list(fans), finite_range_k=k_range, transient=T, lengths=[T, T + SPAN],
                  live_words_in_range=total, words=len(words), sampling=how, classes_seen=live_classes)
    # window alone
    win = {}
    for k in range(0, 5):
        ok, ce = sufficient(words, cls, k, [])
        win[f'window{k}'] = ok
    result['window_alone'] = win
    # minimal sufficient feature subsets per window size
    minimal = {}
    for k in range(0, 4):
        found = []
        for size in range(0, len(FEATURES) + 1):
            for subset in combinations(FEATURES, size):
                if any(set(m) <= set(subset) for m in found):
                    continue
                ok, _ = sufficient(words, cls, k, list(subset))
                if ok:
                    found.append(subset)
            if found:
                break
        minimal[f'window{k}'] = [list(m) for m in found]
    result['minimal_sufficient'] = minimal
    ok, ce = sufficient(words, cls, 3, FEATURES)
    result['window3_all_features'] = dict(sufficient=ok,
                                          counterexample=None if ok else [''.join(map(str, ce[0])), ''.join(map(str, ce[1]))])
    # Part C: run channels
    best, last_ce = None, None
    for cap in (2, 4, 8):
        for R in range(1, MAX_RUNS + 1):
            table, ok = {}, True
            for w, s_, f in words:
                key = (f['window'][-3:], f['self'], run_channels(f, cap, R))
                if table.setdefault(key, (cls[s_], w))[0] != cls[s_]:
                    ok, last_ce = False, (table[key][1], w)
                    break
            if ok:
                best = (cap, R)
                break
        if best:
            break
    result['run_channels'] = dict(minimal_cap_runs=best,
                                  counterexample=None if best else [''.join(map(str, last_ce[0])), ''.join(map(str, last_ce[1]))])
    return result


def main():
    report = {}
    for fans in SHAPES:
        t0 = time.time()
        r = analyse(fans)
        seconds = round(time.time() - t0, 1)
        name = 'fans' + ''.join(map(str, fans))
        report[name] = r
        sys.stdout.flush()
        print(f"{name}: range k={r['finite_range_k']}  len {r['lengths']} words {r['words']}/{r['live_words_in_range']} "
              f"({r['sampling']}) classes {r['classes_seen']}  "
              f"window alone {[k for k, v in r['window_alone'].items() if v][:1] or 'never'}  "
              f"minimal w/ window3 {r['minimal_sufficient']['window3']}  "
              f"w/ window0 {r['minimal_sufficient']['window0']}  [{seconds}s]", flush=True)
        if not r['window3_all_features']['sufficient']:
            print(f"   all features + window 3 insufficient, e.g. {r['window3_all_features']['counterexample']}")
        rc = r['run_channels']
        print(f"   run channels (window3 + self + last R runs, length exact below cap): "
              f"{'cap %d, R = %d' % rc['minimal_cap_runs'] if rc['minimal_cap_runs'] else 'none up to cap 8 / 5 runs, e.g. ' + str(rc['counterexample'])}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'remote_reference.json').write_text(json.dumps(report, indent=1) + '\n')


if __name__ == '__main__':
    main()
