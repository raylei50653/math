#!/usr/bin/env python3
"""Finite facts behind the D16 strength calibration and sparse-source reduction.

Standard library only for every check except the planarity test of small
candidates with H colourable and G not colourable (networkx is imported lazily,
only for such candidates, and is never used to colour). Does not import any repository solver or earlier producer.

Checks
  1. Ring-6 adjacent 5-5 pair: 31 proper patterns, interior acceptance A,
     synchronous D closure of Pat \\ A, residual S (16 types), and that S is the
     unique non-empty D-fixed subset of S (all 2^16 - 1 subsets).
  2. R(H) = S forces C0 chordless (every non-adjacent ring pair is equal in S).
  3. Ring lower bound: for each ring vertex u, the number of distinct non-ring
     neighbours forced by the only S-closed partitions; sum gives m >= 10.
  4. Ring-7 adjacent 5-6 pair: interior acceptance and D residual (the second
     Wernicke half), reported as a finite fact.
  5. Independent small check (no D machinery): every graph H on the 6-ring plus
     k <= 2 interior vertices (all chord / cross / interior edge subsets), and k = 3
     with chordless ring and interior H-degree >= 5, and the k = 4 equality case of the
     counting lemma, has H colourable => G colourable, or G non-planar.
  6. Sharpness control: icosahedron minus a 5-5 edge meets every counting bound
     with equality (|F| = 4, e(F) = 5 = 2|F| - 3, m = 10, all degrees 5) and its
     relation meets A.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys

COLORS = (0, 1, 2, 3)
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
RING6_NAMES = ('z', 'a', 'b', 'w', 'c', 'd')


# ---------------------------------------------------------------- patterns / D

def normalize(word):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in word)


def proper_ring(word):
    n = len(word)
    return all(word[i] != word[(i + 1) % n] for i in range(n))


def set_partitions(points):
    if not points:
        yield ()
        return
    first, *rest = points
    for partial in set_partitions(rest):
        yield ((first,),) + partial
        for idx, block in enumerate(partial):
            yield partial[:idx] + ((first,) + block,) + partial[idx + 1:]


def swapped(word, split, blocks, selected):
    mate = {}
    for x, y in SPLITS[split]:
        mate[x], mate[y] = y, x
    out = list(word)
    for idx, blk in enumerate(blocks):
        if (selected >> idx) & 1:
            for pos in blk:
                out[pos] = mate[word[pos]]
    return tuple(out)


@lru_cache(maxsize=None)
def options(word, split):
    """All joint non-crossing partitions of one split, with full block-subset orbit."""
    n = len(word)
    left, _ = SPLITS[split]
    lp = [i for i, c in enumerate(word) if c in left]
    rp = [i for i, c in enumerate(word) if c not in left]
    out = []
    for lpart in set_partitions(lp):
        for rpart in set_partitions(rp):
            blocks = tuple(sorted(lpart + rpart))
            owner = {p: i for i, b in enumerate(blocks) for p in b}
            if any((word[i] in left) == (word[(i + 1) % n] in left)
                   and owner[i] != owner[(i + 1) % n] for i in range(n)):
                continue
            if any(owner[a] == owner[c] and owner[b] == owner[d] and owner[a] != owner[b]
                   for a, b, c, d in combinations(range(n), 4)):
                continue
            orbit = frozenset(swapped(word, split, blocks, s) for s in range(1 << len(blocks)))
            assert all(proper_ring(t) for t in orbit)
            out.append((blocks, orbit))
    return tuple(out)


def colourable(n, adj, fixed=None):
    """Backtracking 4-colouring test on bitmask adjacency; fixed = partial colouring.

    Colour classes are kept as vertex bitmasks, so a vertex may take colour c iff
    its neighbourhood misses class c.
    """
    cls = [0, 0, 0, 0]
    done = 0
    if fixed:
        for v, c in fixed.items():
            if adj[v] & cls[c]:
                return False
            cls[c] |= 1 << v
            done |= 1 << v
    order = sorted((v for v in range(n) if not (done >> v) & 1),
                   key=lambda v: -adj[v].bit_count())
    nbr = [adj[v] for v in order]
    bits = [1 << v for v in order]
    last = len(order)

    def rec(i):
        if i == last:
            return True
        a, b = nbr[i], bits[i]
        for c in COLORS:
            if not a & cls[c]:
                cls[c] |= b
                if rec(i + 1):
                    return True
                cls[c] ^= b
        return False

    return rec(0)


def pair_acceptance(ring_len, inner_edges):
    """Patterns of a ring_len ring (vertices 2..) and those extending to centres 0,1."""
    ring = tuple(range(2, 2 + ring_len))
    pats = sorted({normalize(w) for w in product(COLORS, repeat=ring_len) if proper_ring(w)})
    acc = set()
    for w in pats:
        col = dict(zip(ring, w))
        for x, y in product(COLORS, repeat=2):
            c = col | {0: x, 1: y}
            if all(c[u] != c[v] for u, v in inner_edges):
                acc.add(w)
                break
    return pats, acc


def d_closure(pats, start):
    """Synchronous D fixed point on S4 pattern sets; returns (rounds removed, fixed)."""
    cur = set(start)
    removed = []
    while True:
        rem = set()
        for w in cur:
            for sp in range(3):
                if not any({normalize(t) for t in orb} <= cur for _, orb in options(w, sp)):
                    rem.add(w)
                    break
        if not rem:
            return removed, cur
        removed.append(sorted(rem))
        cur -= rem


def is_d_fixed(subset):
    return all(any({normalize(t) for t in orb} <= subset for _, orb in options(w, sp))
               for w in subset for sp in range(3))


# ---------------------------------------------------------------- ring-6 pair

RING6 = (2, 3, 4, 5, 6, 7)          # (z, a, b, w, c, d) as vertex ids 2..7
# x1 = 0 : x2, z, a, b, w ; x2 = 1 : x1, w, c, d, z
EDGES6_CENTRES = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (1, 6), (1, 7), (1, 2))
RING6_EDGES = tuple((RING6[i], RING6[(i + 1) % 6]) for i in range(6))


def ring6_facts():
    pats, acc = pair_acceptance(6, EDGES6_CENTRES + RING6_EDGES)
    rest = [w for w in pats if w not in acc]
    removed, S = d_closure(pats, rest)
    S = sorted(S)
    assert len(pats) == 31 and len(acc) == 13 and len(rest) == 18
    assert [len(r) for r in removed] == [2] and len(S) == 16
    expected = ['010201', '010212', '010213', '010231', '012012', '012021', '012102', '012121',
                '012123', '012132', '012301', '012302', '012312', '012313', '012321', '012323']
    assert [''.join(map(str, w)) for w in S] == expected

    fixed_subsets = [mask for mask in range(1, 1 << 16)
                     if is_d_fixed({S[i] for i in range(16) if (mask >> i) & 1})]
    assert fixed_subsets == [(1 << 16) - 1]

    literal = sorted({tuple(p[c] for c in w) for w in S
                      for p in permutations(COLORS)})
    assert len(literal) == 384

    # chords: each non-adjacent ring pair is equal-coloured in some row of S
    chord_witness = {}
    for i, j in combinations(range(6), 2):
        if (j - i) % 6 in (1, 5):
            continue
        wit = next(w for w in S if w[i] == w[j])
        chord_witness[f'{RING6_NAMES[i]}{RING6_NAMES[j]}'] = ''.join(map(str, wit))
    assert len(chord_witness) == 9

    # forced distinct non-ring neighbours per ring vertex
    Sset = set(S)
    need = [0] * 6
    need_witness = [None] * 6
    for r in literal:
        for u in range(6):
            forced_colours = []
            for c in COLORS:
                if c == r[u]:
                    continue
                sp = next(i for i, (p, q) in enumerate(SPLITS) if {r[u], c} in ({*p}, {*q}))
                opts = [blk for blk, orb in options(r, sp) if {normalize(t) for t in orb} <= Sset]
                assert opts, (r, sp)
                reaches = all(len(next(b for b in blk if u in b)) > 1 for blk in opts)
                ring_nbr_has_c = r[(u - 1) % 6] == c or r[(u + 1) % 6] == c
                if reaches and not ring_nbr_has_c:
                    forced_colours.append(c)
            if len(forced_colours) > need[u]:
                need[u] = len(forced_colours)
                need_witness[u] = {'row': ''.join(map(str, r)), 'colours': forced_colours}
    centre_nbrs = [2, 1, 1, 2, 1, 1]
    g_degree_lower = [2 + centre_nbrs[u] + need[u] for u in range(6)]
    return {
        'patterns': len(pats),
        'accepted_types': sorted(''.join(map(str, w)) for w in acc),
        'removed_first_round': [''.join(map(str, w)) for w in removed[0]],
        'S_types': expected,
        'S_literal_rows': len(literal),
        'nonempty_D_fixed_subsets_of_S': len(fixed_subsets),
        'chord_equal_witness': chord_witness,
        'forced_nonring_neighbours': dict(zip(RING6_NAMES, need)),
        'forced_witness': dict(zip(RING6_NAMES, need_witness)),
        'cross_edge_lower_bound_m': sum(need),
        'ring_G_degree_lower_bound': dict(zip(RING6_NAMES, g_degree_lower)),
    }, set(acc), Sset


# ---------------------------------------------------------------- ring-7 pair

def ring7_facts():
    ring = (2, 3, 4, 5, 6, 7, 8)     # (z, a, b, w, c, d, e)
    centres = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5),            # x1: x2 z a b w
               (1, 5), (1, 6), (1, 7), (1, 8), (1, 2))            # x2: x1 w c d e z
    redges = tuple((ring[i], ring[(i + 1) % 7]) for i in range(7))
    pats, acc = pair_acceptance(7, centres + redges)
    rest = [w for w in pats if w not in acc]
    removed, fixed = d_closure(pats, rest)
    return {
        'ring': 'z a b w c d e',
        'patterns': len(pats),
        'accepted_types': len(acc),
        'rejected_types': len(rest),
        'removed_per_round': [len(r) for r in removed],
        'D_residual_types': len(fixed),
        'D_residual': sorted(''.join(map(str, w)) for w in fixed),
    }


# ---------------------------------------------------------------- small blocking check

def small_blocking_check():
    """H on ring 2..7 (+centres 0,1 for G) and interior vertices 8.. ; see module doc."""
    ring_cycle = RING6_EDGES
    chords = [(RING6[i], RING6[j]) for i, j in combinations(range(6), 2) if (j - i) % 6 not in (1, 5)]
    found = {}
    counts = {}
    stage = ['']

    def test(edges_h, n):
        adj_h = [0] * n
        for u, v in edges_h:
            adj_h[u] |= 1 << v
            adj_h[v] |= 1 << u
        adj_g = adj_h[:]
        for u, v in EDGES6_CENTRES:
            adj_g[u] |= 1 << v
            adj_g[v] |= 1 << u
        # H uses vertices 2..n-1 only; centres isolated in adj_h are harmless.
        if colourable(n, adj_g):
            return
        if colourable(n, adj_h):
            found.setdefault(stage[0], []).append(sorted(edges_h))

    for k in (0, 1, 2):
        stage[0] = f'k={k}_all_edge_subsets'
        n = 8 + k
        interior = list(range(8, n))
        optional = chords + [(r, v) for v in interior for r in RING6] + list(combinations(interior, 2))
        cnt = 0
        for mask in range(1 << len(optional)):
            edges = list(ring_cycle) + [optional[i] for i in range(len(optional)) if (mask >> i) & 1]
            test(edges, n)
            cnt += 1
        counts[f'k={k}_all_edge_subsets'] = cnt

    # k = 3: chordless ring (forced by S), every interior vertex H-degree >= 5
    stage[0] = 'k=3_chordless_deg5'
    n = 11
    interior = [8, 9, 10]
    ipairs = list(combinations(interior, 2))
    ring_subsets = {s: [c for c in range(1 << 6) if bin(c).count('1') >= s] for s in range(7)}
    cnt = 0
    for imask in range(8):
        iedges = [ipairs[i] for i in range(3) if (imask >> i) & 1]
        deg = {v: sum(v in e for e in iedges) for v in interior}
        lists = [ring_subsets[max(0, 5 - deg[v])] for v in interior]
        for r0 in lists[0]:
            for r1 in lists[1]:
                for r2 in lists[2]:
                    edges = list(ring_cycle) + iedges
                    for v, rm in zip(interior, (r0, r1, r2)):
                        edges += [(RING6[i], v) for i in range(6) if (rm >> i) & 1]
                    test(edges, n)
                    cnt += 1
    counts['k=3_chordless_deg5'] = cnt

    # k = 4 tight case forced by the counting lemma: chordless, e(F) = 5, every
    # interior H-degree exactly 5, ring cross-degrees exactly (1,2,2,1,2,2).
    stage[0] = 'k=4_tight_case'
    n = 12
    interior = [8, 9, 10, 11]
    ipairs = list(combinations(interior, 2))
    target = (1, 2, 2, 1, 2, 2)
    cnt = 0
    for missing in ipairs:
        iedges = [e for e in ipairs if e != missing]
        deg = {v: sum(v in e for e in iedges) for v in interior}
        lists = [[c for c in range(1 << 6) if c.bit_count() == 5 - deg[v]] for v in interior]
        for rms in product(*lists):
            if tuple(sum((rm >> i) & 1 for rm in rms) for i in range(6)) != target:
                continue
            edges = list(ring_cycle) + iedges
            for v, rm in zip(interior, rms):
                edges += [(RING6[i], v) for i in range(6) if (rm >> i) & 1]
            test(edges, n)
            cnt += 1
    counts['k=4_tight_case'] = cnt

    per_stage = {}
    planar_examples = []
    if found:
        import networkx as nx  # only used for candidates; never as a colouring oracle
    for name in counts:
        cands = found.get(name, [])
        planar = [e for e in cands if nx.check_planarity(nx.Graph(e + list(EDGES6_CENTRES)))[0]]
        per_stage[name] = {'H_colourable_G_not': len(cands), 'of_which_G_planar': len(planar)}
        planar_examples += planar[:5]
    return {
        'graphs_tested': counts,
        'per_stage': per_stage,
        'planar_examples': planar_examples,
    }


# ---------------------------------------------------------------- icosahedron control

def icosahedron_control(acc6):
    # vertices: 0 top, 1..5 upper ring, 6..10 lower ring, 11 bottom
    E = set()
    for i in range(5):
        u, un = 1 + i, 1 + (i + 1) % 5
        l, ln = 6 + i, 6 + (i + 1) % 5
        E |= {(0, u), (u, un), (l, ln), (11, l), (u, l), (un, l)}
    E = {tuple(sorted(e)) for e in E}
    assert len(E) == 30
    adj = {v: set() for v in range(12)}
    for u, v in E:
        adj[u].add(v)
        adj[v].add(u)
    assert all(len(adj[v]) == 5 for v in adj)
    x1, x2 = 0, 1
    z, w = sorted(adj[x1] & adj[x2])
    # ring order around x1 then x2: z, a, b, w, c, d
    def link_path(x, start, end, avoid):
        path, prev, cur = [start], None, start
        while cur != end:
            nxt = next(y for y in adj[cur] & adj[x] if y != prev and y != avoid and y not in path)
            path.append(nxt)
            prev, cur = cur, nxt
        return path
    p1 = link_path(x1, z, w, x2)
    p2 = link_path(x2, w, z, x1)
    ring = p1 + p2[1:-1]
    assert len(ring) == 6 and len(set(ring)) == 6
    F = [v for v in range(12) if v not in ring and v not in (x1, x2)]
    eF = sum(1 for u, v in E if u in F and v in F)
    m = sum(1 for u, v in E if (u in F) != (v in F) and (u in ring or v in ring))
    chords = sum(1 for u, v in E if u in ring and v in ring) - 6
    H_vertices = ring + F
    idx = {v: i for i, v in enumerate(H_vertices)}
    hadj = [0] * len(H_vertices)
    for u, v in E:
        if u in idx and v in idx:
            hadj[idx[u]] |= 1 << idx[v]
            hadj[idx[v]] |= 1 << idx[u]
    rows = set()
    for word in product(COLORS, repeat=6):
        if proper_ring(word) and colourable(len(H_vertices), hadj, dict(enumerate(word))):
            rows.add(normalize(word))
    gadj = [0] * 12
    for u, v in E:
        gadj[u] |= 1 << v
        gadj[v] |= 1 << u
    return {
        'ring': ring, 'F': F, 'k': len(F), 'e_F': eF, 'two_k_minus_3': 2 * len(F) - 3,
        'cross_edges_m': m, 'k_plus_6': len(F) + 6, 'chords': chords,
        'all_degrees_5': True, 'G_colourable': colourable(12, gadj),
        'R_types': len(rows), 'R_meets_A': bool(rows & acc6),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', required=True, type=Path)
    args = ap.parse_args()
    if args.out_dir.exists():
        sys.exit(f'{args.out_dir} exists; choose a new directory')
    r6, acc6, _ = ring6_facts()
    print('ring6 done', r6['forced_nonring_neighbours'], r6['cross_edge_lower_bound_m'], flush=True)
    r7 = ring7_facts()
    print('ring7 done', r7['D_residual_types'], flush=True)
    ico = icosahedron_control(acc6)
    print('icosahedron done', ico, flush=True)
    small = small_blocking_check()
    print('small done', small, flush=True)
    results = {'ring6_pair': r6, 'ring7_pair': r7, 'icosahedron_minus_pair': ico,
               'small_blocking_check': small}
    args.out_dir.mkdir(parents=True)
    blob = json.dumps(results, indent=1, sort_keys=True).encode()
    (args.out_dir / 'results.json').write_bytes(blob)
    src = Path(__file__).read_bytes()
    (args.out_dir / 'verification.json').write_text(json.dumps({
        'script_sha256': sha256(src).hexdigest(),
        'results_sha256': sha256(blob).hexdigest(),
    }, indent=1) + '\n')


if __name__ == '__main__':
    main()
