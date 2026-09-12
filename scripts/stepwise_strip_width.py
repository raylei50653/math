#!/usr/bin/env python3
"""Exact boundary automaton of an infinite strip, and how its state count grows with width.

python scripts/stepwise_strip_width.py            # ~8 min, writes artifacts/stepwise/strip_width.json
python scripts/stepwise_strip_width.py --fast     # ~1 min, skips the three slowest shapes

Strips are described by a tuple of fans, one per interior row: vertex (r,i) of row r is
adjacent to (r-1,i..i+fans[r-1]-1) in the row below (row 0 = boundary b_0 b_1 ...) and to
(r,i-1),(r,i+1).  Fan 2 is a plain triangulated row (stepwise_strip.py's extra rows); fan
>= 3 makes the row see several lower vertices at once.  The infinite boundary is handled
exactly instead of being cut at length 8: the boundary is read left to right as a word over
{0,1,2,3}, interior vertices are introduced (existentially) as soon as their last lower
neighbour is known, and the automaton state after reading b_0..b_n is the set of feasible
colourings of the *active* vertices (those with a neighbour not yet introduced).  The active
set is the window b_{n-fans[0]+2..n}, the last fans[r]-1 vertices of each row r below the
top and one vertex of the top row: a cut of size 1 + sum(f-1 for f in fans).

The set-of-colourings automaton is then minimised (Moore partition refinement), so its live
states are precisely the Nerode classes of the language of extendable boundary words.
|Q(width)| is the number of live classes up to a global colour permutation; `raw` counts
them without quotienting.  This is the quantity the (window, q_n) formulation of
docs/stepwise_state_sufficiency.md section 3 asks about: constant in the depth, or growing.
Three families: (f,2,2,...) adds plain rows under a fan-f row (they can never die, so they
should add nothing); (3,3,...), (3,4), ... stack constraining rows; (2,...,2,f) buries a
constraining row under d free rows, so the boundary only feels it through d layers.

Also reported: for every proper block u of length <= PUMP_LEN, the transient and period of
q, q.u, q.u^2, ... from the initial state (finite Q forces eventual periodicity; the numbers
say how fast).
"""
from collections import defaultdict
from itertools import permutations, product
import json
import sys
import time

from stepwise_sufficiency import OUT

PERMS = list(permutations(range(4)))
# plain rows under a fan row: the rows can never die, |Q| should stay put
PLAIN = [(2,) * w for w in range(1, 5)] + [(3,) + (2,) * w for w in range(0, 5)] + [(4,) + (2,) * w for w in range(0, 4)]
# constraining rows stacked on constraining rows
NESTED = [(3,) * d for d in range(1, 5)] + [(4, 4), (3, 4), (4, 3), (3, 3, 4), (4, 3, 3), (3, 4, 3), (3, 4, 4), (3, 3, 3, 4)]
# free rows *between* the boundary and a constraining row: the depth experiment proper
BURIED = [(2,) * d + (3,) for d in range(1, 4)] + [(2,) * d + (4,) for d in range(1, 4)] + [(2, 3, 3), (2, 2, 3, 3), (2, 3, 4), (3, 2, 4)]
SLOW = {(2, 2, 2, 3), (2, 2, 2, 4), (2, 2, 3, 3)}    # 1-3 min each; skipped with --fast
QUICK = [(3,), (3, 2), (3, 3), (4,), (4, 3), (2, 3)]
PUMP_LEN = 3


def build(fans):
    """Adjacency, introduction step and existence for the strip with the given row fans.

    (0,i) is boundary position i, read as input at step i.  (r,i), r >= 1, sees
    (r-1, i..i+fans[r-1]-1) and (r, i-1), (r, i+1).  Interior vertex step = step of its
    latest lower neighbour, so every edge is checked when its later endpoint is introduced.
    """
    depth = len(fans)

    def fan(r):
        return fans[r - 1]

    def col(r, n):
        """Column of the row-r vertex introduced at step n."""
        c = n
        for q in range(1, r + 1):
            c -= fan(q) - 1
        return c

    def neighbours(v):
        r, i = v
        out = [(r, i - 1), (r, i + 1)]
        if r >= 1:
            out += [(r - 1, i + j) for j in range(fan(r))]
        if r < depth:
            out += [(r + 1, i - j) for j in range(fan(r + 1))]
        return out

    def step(v):
        r, i = v
        return i if r == 0 else step((r - 1, i + fan(r) - 1))

    def exists(v):
        return 0 <= v[0] <= depth

    return col, neighbours, step, exists, depth


def automaton(fans):
    """Reachable DFA of the strip from the genuine left end b_0.

    A state is (k, S): k = min(letters read, n0) and S the set of feasible colourings of the
    active vertices in absolute coordinates.  Beyond n0 = 2*(sum(fans)+2) letters the active
    set is a translate of the one at n0, so the tuple frame is reused and k is clamped;
    this is exactly translation invariance of the strip.
    """
    col, neighbours, step, exists, depth = build(fans)
    span = sum(fans) + 2
    n0 = 2 * span

    def valid(v):
        return exists(v) and v[1] >= 0

    def introduced_at(n):
        vs = [(0, n)] + [(r, col(r, n)) for r in range(1, depth + 1)]
        return [v for v in vs if valid(v)]

    def active_after(n):
        """Vertices introduced by step n with a neighbour introduced later."""
        act = []
        for m in range(max(0, n - span), n + 1):
            for v in introduced_at(m):
                if any(valid(u) and step(u) > n for u in neighbours(v)):
                    act.append(v)
        return sorted(act)

    active = {n: active_after(n) for n in range(-1, n0 + 1)}
    intro = {n: introduced_at(n) for n in range(n0 + 1)}
    shifted = [(v[0], v[1] - 1) for v in active[n0]]
    if shifted != active[n0 - 1]:
        raise RuntimeError(f'not translation invariant at n0: {active[n0 - 1]} vs {active[n0]}')

    def transition(k, state, c):
        prev, nxt, new_vs = active[k - 1], active[k], intro[k]
        new = set()
        for colouring in state:
            assign = dict(zip(prev, colouring))
            if any(assign.get(u) == c for u in neighbours((0, k))):
                continue
            assign[(0, k)] = c

            def go(j):
                if j == len(new_vs):
                    new.add(tuple(assign[v] for v in nxt))
                    return
                v = new_vs[j]
                for d in range(4):
                    if all(assign.get(u) != d for u in neighbours(v)):
                        assign[v] = d
                        go(j + 1)
                        del assign[v]
            go(1)
        return frozenset(new)

    start = (0, frozenset([()]))
    states = {start: 0}
    order = [start]
    delta = []
    for k, s in order:
        row = []
        for c in range(4):
            t = (min(k + 1, n0), transition(k, s, c))
            if t not in states:
                states[t] = len(order)
                order.append(t)
            row.append(states[t])
        delta.append(row)
    return [s for _, s in order], delta, active[n0 - 1]


def minimise(order, delta):
    """Moore refinement; returns class index per state.  Dead = empty set (residual empty)."""
    cls = [0 if s else 1 for s in order]   # live vs dead split first
    while True:
        sig = {}
        new = []
        for i, row in enumerate(delta):
            key = (cls[i],) + tuple(cls[j] for j in row)
            new.append(sig.setdefault(key, len(sig)))
        if len(set(new)) == len(set(cls)):
            return new
        cls = new


def orbits(order, delta, cls, states_index):
    """Union live classes related by a global colour permutation."""
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent.setdefault(parent[x], parent[x])
            x = parent[x]
        return x

    for i, s in enumerate(order):
        if not s:
            continue
        for p in PERMS:
            t = frozenset(tuple(p[c] for c in colouring) for colouring in s)
            j = states_index[t]
            parent[find(cls[i])] = find(cls[j])
    return len({find(cls[i]) for i, s in enumerate(order) if s})


def recurrent(order, delta, cls, index):
    """Live classes (mod perm) reachable by words of length >= 2 and by arbitrarily long words.

    R_k = states reachable by words of length exactly k; the sequence of sets is eventually
    periodic and the union over one period is the recurrent part (the stationary regime of an
    infinitely long boundary, which is what stepwise_strip.py section 9 sampled).
    """
    R, seen, seq = frozenset([0]), {}, []
    while R not in seen:
        seen[R] = len(seq)
        seq.append(R)
        R = frozenset(delta[s][c] for s in R for c in range(4))
    start = seen[R]
    rec = frozenset().union(*seq[start:])

    def count(states):
        parent = {}

        def find(x):
            while parent.setdefault(x, x) != x:
                parent[x] = parent.setdefault(parent[x], parent[x])
                x = parent[x]
            return x

        for i in states:
            if not order[i]:
                continue
            for p in PERMS:
                j = index[frozenset(tuple(p[c] for c in col) for col in order[i])]
                parent[find(cls[i])] = find(cls[j])
        return len({find(cls[i]) for i in states if order[i]})

    from_len2 = frozenset().union(*seq[2:]) | rec
    return count(from_len2), count(rec), start


def pumping(order, delta, cls):
    """Transient and period of the class sequence q_0, q_0.u, q_0.u^2, ... for short blocks u."""
    out = {}
    worst = (0, 0)
    for length in range(1, PUMP_LEN + 1):
        for u in product(range(4), repeat=length):
            if any(u[i] == u[i + 1] for i in range(length - 1)):
                continue
            seen, seq, s = {}, [], 0
            while cls[s] not in seen:
                seen[cls[s]] = len(seq)
                seq.append(cls[s])
                for c in u:
                    s = delta[s][c]
            transient = seen[cls[s]]
            period = len(seq) - transient
            out[''.join(map(str, u))] = dict(transient=transient, period=period, dead=not order[s])
            worst = max(worst, (transient + period, transient))
    return out, worst


def main():
    report = {}
    shapes = QUICK if '--quick' in sys.argv else PLAIN + NESTED + BURIED
    if '--fast' in sys.argv:
        shapes = [f for f in shapes if f not in SLOW]
    for fans in shapes:
        t0 = time.time()
        order, delta, cut = automaton(fans)
        cls = minimise(order, delta)
        index = {s: i for i, s in enumerate(order)}
        live_raw = len({cls[i] for i, s in enumerate(order) if s})
        live_orbits = orbits(order, delta, cls, index)
        has_dead = any(not s for s in order)
        pump, worst = pumping(order, delta, cls)
        live_len2, live_rec, transient = recurrent(order, delta, cls, index)
        name = 'fans' + ''.join(map(str, fans))
        report[name] = dict(fans=list(fans), depth=len(fans), cut=[list(v) for v in cut], cut_size=len(cut),
                            reachable_states=len(order), live_classes_raw=live_raw,
                            live_classes_mod_perm=live_orbits, live_classes_len_ge2=live_len2,
                            live_classes_recurrent=live_rec, left_end_transient=transient, dead_state=has_dead,
                            max_transient_plus_period=worst[0], pumping=pump,
                            seconds=round(time.time() - t0, 2))
        print(f"{name}: cut {len(cut)} reachable {len(order)} live Nerode raw {live_raw} "
              f"mod perm {live_orbits} (len>=2: {live_len2}, recurrent: {live_rec}) dead {has_dead} "
              f"pump(t+p) max {worst[0]} [{report[name]['seconds']}s]")
    summary = {name: (r['cut_size'], r['reachable_states'], r['live_classes_raw'], r['live_classes_recurrent'])
               for name, r in report.items()}
    report['summary_cut_reachable_rawlive_recurrent'] = summary
    for name, row in summary.items():
        print(f"  {name:14s} cut {row[0]:2d}  reachable {row[1]:6d}  raw live classes {row[2]:4d}  recurrent mod perm {row[3]}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'strip_width.json').write_text(json.dumps(report, indent=1) + '\n')


if __name__ == '__main__':
    main()
