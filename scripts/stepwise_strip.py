#!/usr/bin/env python3
"""The ring as a segment of an infinitely long boundary: strips with fans.

python scripts/stepwise_strip.py          # writes artifacts/stepwise/strip.json

Boundary = path b_0 .. b_{L-1} (no closing edge).  Inside = strip(width, fan): row 1 has
vertices t_i adjacent to the boundary block b_i .. b_{i+fan-1} and to t_{i-1}, t_{i+1};
each further row r has v_{r,i} adjacent to v_{r-1,i}, v_{r-1,i+1}, v_{r,i-1}, v_{r,i+1}.
fan = 2 is the plain triangulated strip (never dead); fan >= 3 makes interior vertices
see several boundary positions at once, so boundary prefixes can die.

The boundary is coloured left to right, forward only.  A prefix is alive iff some
completion of the boundary word extends to a proper colouring of the strip.  Nerode
classes: two prefixes are equivalent iff their residual sets of raw suffixes agree up to a
global colour permutation.  The 'infinite edge' is approximated by a finite strip of
length L with prefixes kept short (suffixes of length >= L - MAX_PREFIX remain).

Candidate local state = window (last k boundary colours) plus +/- relations about the
frontier interior vertices (those adjacent to the last read boundary position):
  may(v, c)   frontier vertex v can still take the colour of boundary position n-1-c
  fresh(v)    it can still take a colour not among the last three boundary colours
  forced(v)   exactly one live colour remains for it
  nfresh(v)   how many live colours it has outside the last three boundary colours
"""
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
import json

from stepwise_sufficiency import OUT, normalize

L = 8
MAX_PREFIX = 5
SHAPES = [(1, 2), (2, 2), (1, 3), (2, 3), (1, 4)]   # (width, fan)


def strip(width, fan, length=L):
    adj = defaultdict(set)

    def edge(u, v):
        adj[u].add(v)
        adj[v].add(u)

    for i in range(length - 1):
        edge((0, i), (0, i + 1))
    row1 = range(length - fan + 1)
    for i in row1:
        for j in range(fan):
            edge((1, i), (0, i + j))
        if i > 0:
            edge((1, i), (1, i - 1))
    prev = list(row1)
    for r in range(2, width + 1):
        cur = range(len(prev) - 1)
        for i in cur:
            edge((r, i), (r - 1, i))
            edge((r, i), (r - 1, i + 1))
            if i > 0:
                edge((r, i), (r, i - 1))
        prev = list(cur)
    interior = sorted(v for v in adj if v[0] > 0)
    return adj, interior


def colourings(adj, interior, boundary):
    colour = {(0, i): c for i, c in enumerate(boundary)}

    def go(k):
        if k == len(interior):
            yield dict(colour)
            return
        v = interior[k]
        for c in range(4):
            if all(colour.get(u) != c for u in adj[v]):
                colour[v] = c
                yield from go(k + 1)
                del colour[v]

    yield from go(0)


def proper_words(n):
    return sorted({normalize(p) for p in product(range(4), repeat=n)
                   if all(p[i] != p[i + 1] for i in range(n - 1))})


PERMS = list(permutations(range(4)))


def canonical_residual(suffixes):
    return min(tuple(sorted(tuple(s[c] for c in suf) for suf in suffixes)) for s in PERMS)


def analyse(width, fan):
    adj, interior = strip(width, fan)
    words = proper_words(L)
    # per accepted word: for each n, the set of frontier colourings over live interior colourings
    frontier_of = {n: sorted(v for v in interior if (0, n - 1) in adj[v]) for n in range(2, MAX_PREFIX + 1)}
    accepted, frontier_cols = set(), {}
    for w in words:
        cols = list(colourings(adj, interior, w))
        if cols:
            accepted.add(w)
            frontier_cols[w] = {n: {tuple(c[v] for v in frontier_of[n]) for c in cols}
                                for n in frontier_of}
    by_prefix = {}
    for n in range(2, MAX_PREFIX + 1):
        prefixes = proper_words(n)
        residual, live_frontier = {}, {}
        for p in prefixes:
            suffixes, fr = [], set()
            for s in product(range(4), repeat=L - n):
                full = p + s
                if any(full[i] == full[i + 1] for i in range(L - 1)):
                    continue
                w = normalize(full)
                if w in accepted:
                    suffixes.append(s)
                    # frontier colours are stored in the frame of w; map back to p's frame
                    names = {}
                    for c in list(full) + [0, 1, 2, 3]:
                        names.setdefault(c, len(names))
                    inv = {v: k for k, v in names.items()}
                    fr |= {tuple(inv[c] for c in t) for t in frontier_cols[w][n]}
            residual[p] = canonical_residual(suffixes)
            live_frontier[p] = fr
        classes = defaultdict(list)
        for p, r in residual.items():
            classes[r].append(p)
        alive = [p for p in prefixes if live_frontier[p]]
        preds = {}
        for idx, v in enumerate(frontier_of[n]):
            for c in range(min(3, n)):
                preds[f'may({v[0]},{v[1]}; a(n-{c + 1}))'] = (idx, ('pos', n - 1 - c))
            preds[f'fresh({v[0]},{v[1]})'] = (idx, ('fresh', None))
            preds[f'forced({v[0]},{v[1]})'] = (idx, ('forced', None))
            preds[f'nfresh({v[0]},{v[1]})'] = (idx, ('nfresh', None))
        pred_values = {}
        for name, (idx, (kind, pos)) in preds.items():
            pred_values[name] = {}
            for p in prefixes:
                live = {t[idx] for t in live_frontier[p]}
                if kind == 'pos':
                    pred_values[name][p] = p[pos] in live
                elif kind == 'fresh':
                    pred_values[name][p] = bool(live - set(p[-3:]))
                elif kind == 'forced':
                    pred_values[name][p] = len(live) == 1
                else:
                    pred_values[name][p] = len(live - set(p[-3:]))
        rows = {}
        for k in (1, 2, 3):
            win = {p: normalize(p[-k:]) for p in prefixes}
            per_window = Counter()
            for r, ps in classes.items():
                for wv in {win[p] for p in ps}:
                    per_window[wv] += 1
            best = None
            names = list(preds)
            for size in range(len(names) + 1):
                for subset in combinations(names, size):
                    table, ok = {}, True
                    for p in alive:
                        key = (win[p],) + tuple(pred_values[nm][p] for nm in subset)
                        if table.setdefault(key, residual[p]) != residual[p]:
                            ok = False
                            break
                    if ok:
                        best = list(subset)
                        break
                if best is not None:
                    break
            rows[f'window{k}'] = dict(window_values=len(set(win.values())),
                                      max_classes_per_window=max(per_window.values()),
                                      minimal_frontier_relations_alive=best)
        by_prefix[f'n={n}'] = dict(prefixes=len(prefixes), alive=len(alive), nerode_classes=len(classes),
                                   nerode_classes_alive=len({residual[p] for p in alive}),
                                   dead_prefixes=[p for p in prefixes if not live_frontier[p]][:8],
                                   frontier=frontier_of[n], predicates=list(preds), windows=rows)
    return dict(interior_vertices=len(interior), accepted_words=len(accepted), proper_words=len(words),
                by_prefix=by_prefix)


def main():
    report = {}
    for width, fan in SHAPES:
        name = f'width{width}_fan{fan}'
        report[name] = analyse(width, fan)
        r = report[name]
        print(f"{name}: {r['accepted_words']}/{r['proper_words']} boundary words of length {L} extendable")
        for n, row in r['by_prefix'].items():
            print(f"  {n}: prefixes {row['prefixes']} alive {row['alive']} Nerode {row['nerode_classes']}"
                  f" (alive {row['nerode_classes_alive']}) frontier {row['frontier']} dead e.g. {row['dead_prefixes'][:3]}")
            for k, wr in row['windows'].items():
                print(f"     {k}: values {wr['window_values']} max classes/window {wr['max_classes_per_window']}"
                      f" -> relations {wr['minimal_frontier_relations_alive']}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'strip.json').write_text(json.dumps(report, indent=1, default=repr) + '\n')


if __name__ == '__main__':
    main()
