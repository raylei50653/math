#!/usr/bin/env python3
"""Finite checks behind docs/c5_equivalent_formulations.md.

python3 scripts/c5_equivalent_forms_check.py

1. The disk count identity x_uv = m + sum_{i not in uv} y_i, under the
   four-row certificate (accept 01232, reject 01021/01202/01212), leaves
   exactly the fixed masks 932/933/940/941; 940 is a D5 image of 933.
2. None of the 132 catalogue keys violates statement (E) in any D5 position;
   all 64 abstract four-row masks lie outside the catalogue.
3. Catalogue keys rejecting two adjacent singletons: 45 keys, 8 D5 orbits.
4. XOR words of the four certificate rows and their singleton edge positions.
5. On random C5 near-triangulations (explicit face lists, no embedding
   search), every literal boundary row beta satisfies
   N_beta = sum over admissible even-complement matchings M of 2^c(M).

Read-only on the catalogue. Item 5 is a randomized control of a standard
duality, not a proof; items 1-4 are exhaustive over finite objects.
"""
from collections import Counter
from itertools import product
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / 'artifacts/c5_cells/cells.json'

DATA = json.loads(CATALOGUE.read_text())
PO = [tuple(p) for p in DATA['pattern_order']]
KEYS = {int(k) for k in DATA['cells']}
SINGLE = {0: 4, 1: 3, 3: 2, 4: 1, 6: 0}            # bit -> singleton position
PAIR = {2: (0, 2), 5: (0, 3), 7: (1, 3), 8: (1, 4), 9: (2, 4)}  # bit -> repeated pair
ACCEPT, REJECT = 9, (1, 4, 6)                         # 01232; 01021, 01202, 01212


def canon(p):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in p)


INDEX = {p: i for i, p in enumerate(PO)}
D5 = ([[(i + r) % 5 for i in range(5)] for r in range(5)]
      + [[(r - i) % 5 for i in range(5)] for r in range(5)])


def act(mask, perm):
    out = 0
    for i, p in enumerate(PO):
        if mask >> i & 1:
            out |= 1 << INDEX[canon(tuple(p[perm[j]] for j in range(5)))]
    return out


def four_row(mask):
    return bool(mask >> ACCEPT & 1) and not any(mask >> b & 1 for b in REJECT)


def support(mask):
    return {SINGLE[b] for b in SINGLE if mask >> b & 1}


def check_identity_masks():
    masks = set()
    for m, a, b in product((1, 2), (0, 1), (0, 1)):
        y = {0: 0, 1: 0, 2: a, 3: 0, 4: b}
        mask = sum(1 << bit for bit, i in SINGLE.items() if y[i])
        for bit, (u, v) in PAIR.items():
            if m + sum(y[i] for i in range(5) if i not in (u, v)) > 0:
                mask |= 1 << bit
        masks.add(mask)
    assert masks == {932, 933, 940, 941}, masks
    assert any(act(933, p) == 940 for p in D5)
    return sorted(masks)


def check_catalogue():
    abstract = [m for m in range(1024) if four_row(m)]
    assert len(abstract) == 64 and not KEYS.intersection(abstract)
    assert not [k for k in KEYS for p in D5 if four_row(act(k, p))]
    adjacent = [k for k in KEYS
                if any(i not in support(k) and (i + 1) % 5 not in support(k)
                       for i in range(5))]
    orbits = {min(act(k, p) for p in D5) for k in adjacent}
    assert len(adjacent) == 45 and len(orbits) == 8
    return {'abstract_four_row_masks': 64, 'adjacent_rejecting_keys': 45,
            'adjacent_rejecting_orbits': sorted(orbits)}


def xor_word(beta):
    return tuple(beta[i] ^ beta[(i + 1) % 5] for i in range(5))


def check_words():
    rows = {'01232': (0, 1, 2, 3, 2), '01021': (0, 1, 0, 2, 1),
            '01202': (0, 1, 2, 0, 2), '01212': (0, 1, 2, 1, 2)}
    expect = {'01232': ((1, 3, 1, 1, 2), (1, 4)), '01021': ((1, 1, 2, 3, 1), (2, 3)),
              '01202': ((1, 3, 2, 2, 2), (0, 1)), '01212': ((1, 3, 3, 3, 2), (0, 4))}
    out = {}
    for name, beta in rows.items():
        w = xor_word(beta)
        c = Counter(w)
        ends = tuple(i for i in range(5) if c[w[i]] == 1)
        assert (w, ends) == expect[name], (name, w, ends)
        out[name] = {'word': ''.join(map(str, w)), 'singleton_edges': list(ends)}
    return out


# ---- randomized duality control on explicit near-triangulations ----

def wheel():
    return 6, [tuple(sorted((i, (i + 1) % 5, 5))) for i in range(5)]


def edges_of(faces):
    return {tuple(sorted(e)) for f in faces for e in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2]))}


def random_near_triangulation(rng, steps):
    n, faces = wheel()
    boundary = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
    for _ in range(steps):
        if rng.random() < 0.5 or n < 7:
            f = faces.pop(rng.randrange(len(faces)))
            a, b, c = f
            faces += [tuple(sorted(t)) for t in ((a, b, n), (b, c, n), (a, c, n))]
            n += 1
            continue
        es = edges_of(faces)
        inner = [e for e in es if e not in boundary]
        e = rng.choice(inner)
        two = [f for f in faces if e[0] in f and e[1] in f]
        if len(two) != 2:
            continue
        p = [v for v in two[0] if v not in e][0]
        q = [v for v in two[1] if v not in e][0]
        if tuple(sorted((p, q))) in es:
            continue
        faces = [f for f in faces if f not in two]
        faces += [tuple(sorted((p, q, e[0]))), tuple(sorted((p, q, e[1])))]
    return n, faces


def coloring_count(n, edges, beta):
    adj = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    if any(beta[a] == beta[b] for a, b in edges if a < 5 and b < 5):
        return 0
    col = dict(enumerate(beta))
    inner = list(range(5, n))

    def go(t):
        if t == len(inner):
            return 1
        v, total = inner[t], 0
        for c in range(4):
            if all(col.get(u) != c for u in adj[v]):
                col[v] = c
                total += go(t + 1)
                del col[v]
        return total
    return go(0)


def matching_weight(faces, beta):
    w = xor_word(beta)
    c3 = Counter(w).most_common(1)[0][0]
    unmatched = {i for i in range(5) if w[i] != c3}
    fid = {f: j for j, f in enumerate(faces)}
    dual = []                      # (kind, a, b): internal edge between faces, or terminal i at face
    for e in edges_of(faces):
        inc = [fid[f] for f in faces if e[0] in f and e[1] in f]
        if len(inc) == 2:
            dual.append(('in', inc[0], inc[1]))
        else:
            i = e[0] if (e[0] + 1) % 5 == e[1] else e[1]
            dual.append(('term', inc[0], i))
    total = 0

    def finish(chosen):
        comp = [d for k, d in enumerate(dual) if k not in chosen]
        if {d[2] for d in comp if d[0] == 'term'} != unmatched:
            return 0
        adj = {}
        for d in comp:
            if d[0] == 'in':
                adj.setdefault(d[1], []).append(d[2])
                adj.setdefault(d[2], []).append(d[1])
        on_path = {d[1] for d in comp if d[0] == 'term'}
        seen, cycles = set(), 0
        for s in adj:
            if s in seen:
                continue
            stack, size, comp_v = [s], 0, set()
            while stack:
                v = stack.pop()
                if v in comp_v:
                    continue
                comp_v.add(v)
                stack += adj[v]
            seen |= comp_v
            if comp_v & on_path:
                continue
            if len(comp_v) % 2:
                return 0
            cycles += 1
        return 2 ** cycles

    def go(covered, chosen):
        nonlocal total
        free = [j for j in range(len(faces)) if j not in covered]
        if not free:
            total += finish(chosen)
            return
        j = free[0]
        for k, d in enumerate(dual):
            if k in chosen:
                continue
            if d[0] == 'term' and d[1] == j and d[2] not in unmatched:
                go(covered | {j}, chosen | {k})
            elif d[0] == 'in' and j in (d[1], d[2]):
                other = d[2] if d[1] == j else d[1]
                if other not in covered:
                    go(covered | {j, other}, chosen | {k})
    go(frozenset(), frozenset())
    return total


def check_matchings(trials=60, seed=17):
    rng = random.Random(seed)
    rows, positive = 0, 0
    for _ in range(trials):
        n, faces = random_near_triangulation(rng, rng.randrange(0, 9))
        es = edges_of(faces)
        for beta in PO:
            lhs = coloring_count(n, es, beta)
            rhs = matching_weight(faces, beta)
            assert lhs == rhs, (n, faces, beta, lhs, rhs)
            rows += 1
            positive += lhs > 0
    return {'graphs': trials, 'rows': rows, 'positive_rows': positive, 'seed': seed}


def main():
    report = {
        'identity_masks': check_identity_masks(),
        'catalogue': check_catalogue(),
        'xor_words': check_words(),
        'matching_control': check_matchings(),
    }
    json.dump(report, sys.stdout, indent=1)
    print('\nPASS')


if __name__ == '__main__':
    main()
