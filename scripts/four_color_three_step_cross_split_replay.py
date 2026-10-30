#!/usr/bin/env python3
"""Independent stdlib-only replay of cross-split trapped-swap exclusion of PAIR-C0-D16.

Uses ONLY the Python standard library. Does NOT import the producer script,
ck_kempe_obstruction, four_color_counts_cone_verification, or any repository solver.
Independently recomputes set partitions, Boolean D fixed point, D-minimality over all
65,535 non-empty subsets, standard B6 signed-matching equations, universal P-exclusion
across all 24 literal frames, combinatorial sphere/disk embeddings, three-step
(x1, x2, z) buckets retaining all empty fibres, delayed writeback bijections,
union-find bicolored components, and retained KERNEL-936/732 + ZV-17 controls.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLORS = (0, 1, 2, 3)
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
CYCLE = (2, 3, 4, 7, 5, 6)
CENTER_ONLY_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 7),
    (1, 2), (1, 5), (1, 6), (1, 7),
)
INNER_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 7),
    (1, 2), (1, 5), (1, 6), (1, 7),
    (2, 3), (2, 6), (3, 4), (4, 7), (5, 6), (5, 7),
)
PRIOR = 'audits/2026-10-29-three-step-relation-control-e1a90fe/results.json'
ZV = 'audits/2026-10-30-three-step-shared-exterior-e1a90fe/results.json'


def normalize(word: tuple[int, ...]) -> tuple[int, ...]:
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in word)


def proper_ring(word: tuple[int, ...]) -> bool:
    n = len(word)
    return all(word[i] != word[(i + 1) % n] for i in range(n))


def set_partitions(points: list[int]):
    if not points:
        yield ()
        return
    first, *rest = points
    for partial in set_partitions(rest):
        yield ((first,),) + partial
        for idx, block in enumerate(partial):
            yield partial[:idx] + ((first,) + block,) + partial[idx + 1:]


def changed_row(word: tuple[int, ...], split: int,
                blocks: tuple[tuple[int, ...], ...], selected: int) -> tuple[int, ...]:
    mate = {a: b for pair in SPLITS[split] for a, b in (pair, pair[::-1])}
    out = list(word)
    for idx, blk in enumerate(blocks):
        if (selected >> idx) & 1:
            for pos in blk:
                out[pos] = mate[word[pos]]
    return tuple(out)


@lru_cache(maxsize=None)
def noncrossing_options(word: tuple[int, ...], split: int):
    left, right = SPLITS[split]
    lp = [i for i, c in enumerate(word) if c in left]
    rp = [i for i, c in enumerate(word) if c in right]
    res = []
    for l_part in set_partitions(lp):
        for r_part in set_partitions(rp):
            blocks = tuple(sorted(l_part + r_part))
            owner = {p: i for i, b in enumerate(blocks) for p in b}
            if any((word[i] in left) == (word[(i + 1) % 6] in left)
                   and owner[i] != owner[(i + 1) % 6]
                   for i in range(6)):
                continue
            if any(owner[a] == owner[c] and owner[b] == owner[d] and owner[a] != owner[b]
                   for a, b, c, d in combinations(range(6), 4)):
                continue
            orbit = frozenset(changed_row(word, split, blocks, sel)
                              for sel in range(1 << len(blocks)))
            assert all(proper_ring(t) for t in orbit)
            res.append((blocks, orbit))
    return tuple(sorted(res))


def reconstruct_d_and_minimality(baseline_rec: dict) -> tuple[list[tuple[int, ...]], int, int]:
    patterns = sorted({normalize(w) for w in product(COLORS, repeat=6) if proper_ring(w)})
    lookup = {w: i for i, w in enumerate(patterns)}
    accepted = 0
    for idx, word in enumerate(patterns):
        bdry = dict(zip(CYCLE, word))
        if any(all((bdry | {0: x, 1: y})[u] != (bdry | {0: x, 1: y})[v] for u, v in INNER_EDGES)
               for x, y in product(COLORS, repeat=2)):
            accepted |= 1 << idx

    orbit_masks = [
        [
            tuple(sorted({
                # Global color permutations can normalize distinct literal rows
                # to the same pattern. Count each bit once to avoid carries.
                sum(1 << idx for idx in {lookup[normalize(t)] for t in orbit})
                for _, orbit in noncrossing_options(word, split)
            }))
            for split in range(3)
        ]
        for word in patterns
    ]

    cur = ((1 << len(patterns)) - 1) ^ accepted
    removed = []
    while True:
        rem = sum(
            1 << idx for idx, splits in enumerate(orbit_masks)
            if ((cur >> idx) & 1)
            and any(not any((m & cur) == m for m in masks) for masks in splits)
        )
        if not rem:
            break
        removed.append(rem)
        cur &= ~rem

    assert len(patterns) == 31 and accepted == 4969575
    assert removed == [67108872] and cur == 2075405200
    assert baseline_rec['patterns'] == [list(p) for p in patterns]
    assert baseline_rec['accepted_mask'] == accepted
    assert baseline_rec['removed_masks'] == removed
    assert baseline_rec['residual_mask'] == cur

    # Exhaustively verify D-minimality over all 2^16 - 1 = 65,535 non-empty subsets:
    active = [i for i in range(len(patterns)) if (cur >> i) & 1]
    assert len(active) == 16
    consistent = []
    for sub in range(1, 1 << 16):
        mask = 0
        for bit, p_idx in enumerate(active):
            if (sub >> bit) & 1:
                mask |= 1 << p_idx
        ok = True
        for bit, p_idx in enumerate(active):
            if (sub >> bit) & 1:
                for masks in orbit_masks[p_idx]:
                    if not any((m & mask) == m for m in masks):
                        ok = False
                        break
                if not ok:
                    break
        if ok:
            consistent.append(mask)

    assert consistent == [cur]
    assert baseline_rec['d_minimality'] == dict(
        nonempty_subsets_tested=65535,
        d_consistent_nonempty_subsets=[cur],
        is_minimal_nonempty_d_fixed=True,
    )
    return patterns, accepted, cur


def perfect_noncrossing_matchings(verts: tuple[int, ...]):
    if not verts:
        yield ()
        return
    a = verts[0]
    for i in range(1, len(verts)):
        b = verts[i]
        for rest in perfect_noncrossing_matchings(verts[1:i] + verts[i + 1:]):
            cand = ((a, b),) + rest
            if not any(u < x < v < y or x < u < y < v for (u, v), (x, y) in combinations(cand, 2)):
                yield cand


def all_b6_signatures():
    for sz in (0, 2, 4, 6):
        for verts in combinations(range(6), sz):
            for m in perfect_noncrossing_matchings(verts):
                for signs in product((-1, 1), repeat=len(m)):
                    yield tuple((a, b, s) for (a, b), s in zip(m, signs))


def integrate_parity_word(word: tuple[int, ...]) -> tuple[int, ...]:
    cur = 0
    out = []
    for step in word:
        out.append(cur)
        cur ^= step
    assert cur == 0
    return tuple(out)


def verify_b6_cone(patterns: list[tuple[int, ...]], residual: int, b6_rec: dict) -> dict:
    lookup = {p: i for i, p in enumerate(patterns)}
    words = [w for w in product((1, 2, 3), repeat=6) if all(w.count(c) % 2 == 0 for c in (1, 2, 3))]
    sigs = list(all_b6_signatures())
    states = [lookup[normalize(integrate_parity_word(w))] for w in words]
    rows = [(i, pair) for i in range(len(words)) for pair in combinations((1, 2, 3), 2)]

    def is_compat(w, pair, sig):
        ports = {j for j, c in enumerate(w) if c in pair}
        cov = {j for a, b, _ in sig for j in (a, b)}
        return ports == cov and all((w[a] == w[b]) == (sgn == -1) for a, b, sgn in sig)

    cols = [[r for r, (i, pair) in enumerate(rows) if is_compat(words[i], pair, s)] for s in sigs]
    eligible = [s for s, col in enumerate(cols) if col and all((residual >> states[rows[r][0]]) & 1 for r in col)]
    assert len(words) == 183 and len(sigs) == 191 and len(rows) == 549 and len(eligible) == 29

    stored_weights = b6_rec['primal_signature_weights']
    assert len(stored_weights) == 27
    row_sums = [0] * len(rows)
    for item in stored_weights:
        s_idx = item['signature_index']
        w = item['weight']
        assert isinstance(w, int) and w > 0 and s_idx in eligible
        assert [list(t) for t in sigs[s_idx]] == item['matching']
        for r in cols[s_idx]:
            row_sums[r] += w

    pat_mult = {}
    for r, (i, _) in enumerate(rows):
        st = states[i]
        if (residual >> st) & 1:
            if st in pat_mult:
                assert pat_mult[st] == row_sums[r]
            else:
                pat_mult[st] = row_sums[r]
                assert pat_mult[st] > 0
        else:
            assert row_sums[r] == 0

    assert {str(k): v for k, v in sorted(pat_mult.items())} == b6_rec['induced_pattern_multiplicities']
    assert sum(pat_mult.values()) == 18 == b6_rec['canonical_total_weight']
    assert 24 * sum(pat_mult.values()) == 432 == b6_rec['literal_total_weight']
    return dict(
        equations_checked=len(rows),
        active_signatures=len(stored_weights),
        canonical_total_weight=18,
    )


def verify_exit_bounds_and_universal_exclusion(patterns: list[tuple[int, ...]],
                                               residual: int,
                                               aux_rec: dict,
                                               excl_rec: dict) -> dict:
    d16_indices = [i for i in range(len(patterns)) if (residual >> i) & 1]
    d16_pats = {patterns[i] for i in d16_indices}
    lit_support = {tuple(perm[c] for c in p) for p in d16_pats for perm in permutations(COLORS)}
    assert len(lit_support) == 384

    # 1. Verify all 9 non-adjacent pairs of C0 are monochromatic in >= 2 D16 patterns:
    nonadj = []
    for i in range(6):
        for j in range(i + 1, 6):
            if (j - i) % 6 not in (1, 5):
                mono = [idx for idx in d16_indices if patterns[idx][i] == patterns[idx][j]]
                assert len(mono) >= 2
                nonadj.append((i, j, mono))
    assert len(nonadj) == 9 == aux_rec['c0_nonadjacent_pairs']

    # 2. Verify forced 1-step exterior exit lower bounds (1, 2, 2, 1, 2, 2):
    stored_lbs = [item['min_exterior_neighbors_outside_c0'] for item in aux_rec['vertex_exit_lower_bounds']]
    assert tuple(stored_lbs) == (1, 2, 2, 1, 2, 2)
    for item in aux_rec['vertex_exit_lower_bounds']:
        v = item['position']
        prev_v, next_v = (v - 1) % 6, (v + 1) % 6
        r = tuple(item['witness']['pattern'])
        assert r in d16_pats
        colors_forced = set()
        for fe in item['witness']['forced_exits']:
            s_idx = fe['split']
            pair = tuple(fe['pair'])
            assert pair in SPLITS[s_idx] and r[v] in pair
            assert r[prev_v] not in pair and r[next_v] not in pair
            valid_p = [b for b, orb in noncrossing_options(r, s_idx) if orb <= lit_support]
            assert valid_p and all(any(v in blk and len(blk) >= 2 for blk in b) for b in valid_p)
            other = pair[0] if pair[1] == r[v] else pair[1]
            assert other == fe['forced_exterior_color']
            colors_forced.add(other)
        assert len(colors_forced) == item['min_exterior_neighbors_outside_c0']

    # 3. Verify universal P-exclusion over all 24 literal color frames of #20 -> #13:
    records = excl_rec['literal_records']
    assert len(records) == 24
    seen_frames = set()
    for rec in records:
        c0, c1, c2, c3 = rec['color_frame']
        assert sorted((c0, c1, c2, c3)) == [0, 1, 2, 3]
        seen_frames.add((c0, c1, c2, c3))
        r0 = (c0, c1, c2, c1, c2, c1)
        r0_prime = (c0, c1, c2, c0, c2, c1)
        assert list(r0) == rec['source_row'] and list(r0_prime) == rec['trapped_swap_target_row']
        assert r0 in lit_support and r0_prime in lit_support

        sp = rec['premise_split']
        ss = rec['second_split']
        assert {frozenset(p) for p in SPLITS[sp]} == {frozenset((c0, c1)), frozenset((c2, c3))}
        assert {frozenset(p) for p in SPLITS[ss]} == {frozenset((c0, c2)), frozenset((c1, c3))}

        vp_r0 = [b for b, orb in noncrossing_options(r0, sp) if orb <= lit_support]
        vs_r0 = [b for b, orb in noncrossing_options(r0, ss) if orb <= lit_support]
        vs_r0p = [b for b, orb in noncrossing_options(r0_prime, ss) if orb <= lit_support]

        # Every one of the three partition sets MUST be a singleton (zero representative choice!):
        assert vp_r0 == [((0, 1, 5), (2, 4), (3,))]
        assert vs_r0 == [((0, 2, 4), (1,), (3,), (5,))]
        assert vs_r0p == [((0,), (1, 5), (2, 3, 4))]

    assert len(seen_frames) == 24
    assert excl_rec['admissible_common_source_annotations_for_d16'] == 0
    assert excl_rec['admissible_nonempty_complement_subsets_under_P'] == 0
    return dict(
        chordless_pairs=9,
        exit_degree_bounds=[1, 2, 2, 1, 2, 2],
        universal_literal_frames_verified=24,
        admissible_d16_annotations=0,
    )


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def verify_embedding_record(emb: dict) -> None:
    n_g = emb['n_vertices_g']
    h_edges = [tuple(e) for e in emb['h_edges']]
    g_edges = sorted(set(CENTER_ONLY_EDGES) | {tuple(sorted(e)) for e in h_edges})
    g_faces = [tuple(f) for f in emb['g_oriented_faces']]
    assert len(g_edges) == emb['n_edges_g'] and len(g_faces) == emb['n_faces_g']

    darts = Counter((f[i], f[(i + 1) % len(f)]) for f in g_faces for i in range(len(f)))
    assert darts == Counter({(u, v): 1 for u, v in g_edges} | {(v, u): 1 for u, v in g_edges})
    assert n_g - len(g_edges) + len(g_faces) == 2

    # Check single-cycle rotation at every vertex and connectedness of G:
    uf_g = UnionFind(n_g)
    for u, v in g_edges:
        uf_g.union(u, v)
    assert len({uf_g.find(u) for u in range(n_g)}) == 1

    rot_g = {}
    for u in range(n_g):
        nxt = {}
        for f in g_faces:
            L = len(f)
            for i, x in enumerate(f):
                if x == u:
                    prv = f[(i - 1) % L]
                    assert prv not in nxt
                    nxt[prv] = f[(i + 1) % L]
        start = min(nxt)
        cur = nxt[start]
        order = [start]
        while cur != start:
            order.append(cur)
            cur = nxt[cur]
        assert len(order) == len(nxt)
        rot_g[u] = order
        if u < 8:
            assert emb['core_degrees_in_g'][str(u)] == len(order)

    # Induced H = G - {0, 1} faces and facial C0 check:
    rot_h = {u: [v for v in rot_g[u] if v >= 2] for u in range(2, n_g)}
    seen = set()
    h_faces = []
    for u in range(2, n_g):
        for v in rot_h[u]:
            if (u, v) not in seen:
                walk = []
                cu, cv = u, v
                while (cu, cv) not in seen:
                    seen.add((cu, cv))
                    walk.append(cu)
                    r = rot_h[cv]
                    cu, cv = cv, r[(r.index(cu) + 1) % len(r)]
                m = min(walk)
                k = walk.index(m)
                h_faces.append(tuple(walk[k:] + walk[:k]))
    h_faces.sort()
    assert [list(f) for f in h_faces] == emb['h_oriented_faces']
    assert (n_g - 2) - len(h_edges) + len(h_faces) == 2
    c0_faces = [f for f in h_faces if len(f) == 6 and set(f) == set(CYCLE)]
    assert len(c0_faces) == 1 and list(c0_faces[0]) == emb['c0_facial_walk']

    # Cycle rank beta_1(H - V(C0)) via UnionFind:
    ext_v = sorted(set(range(2, n_g)) - set(CYCLE))
    v_idx = {u: i for i, u in enumerate(ext_v)}
    ext_e = [(u, v) for u, v in h_edges if u in v_idx and v in v_idx]
    uf_ext = UnionFind(len(ext_v))
    for u, v in ext_e:
        uf_ext.union(v_idx[u], v_idx[v])
    cc = len({uf_ext.find(i) for i in range(len(ext_v))}) if ext_v else 0
    beta1 = len(ext_e) - len(ext_v) + cc
    assert beta1 == emb['beta1_h_minus_c0']


def all_proper_colorings(verts: tuple[int, ...], edges: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    pos = {u: i for i, u in enumerate(verts)}
    active_edges = [(pos[u], pos[v]) for u, v in edges if u in pos and v in pos]
    preds = [
        tuple(sorted({u if v == i else v for u, v in active_edges if (u == i and v < i) or (v == i and u < i)}))
        for i in range(len(verts))
    ]
    out = []
    cur = [0] * len(verts)

    def dfs(i: int) -> None:
        if i == len(verts):
            out.append(tuple(cur))
            return
        forbidden = {cur[j] for j in preds[i]}
        for c in COLORS:
            if c not in forbidden:
                cur[i] = c
                dfs(i + 1)

    dfs(0)
    return out


def uf_property_p_check(n_g: int, h_edges: list[tuple[int, int]], cols_h: list[tuple[int, ...]]) -> tuple[int, int]:
    """Independent Union-Find evaluation of Property P across all colorings in Col_4(H)."""
    n_h = n_g - 2
    shifted_edges = [(u - 2, v - 2) for u, v in h_edges]
    c_pos = tuple(u - 2 for u in CYCLE)
    col_set = set(cols_h)

    def pair_uf(col, pair_set):
        uf = UnionFind(n_h)
        for u, v in shifted_edges:
            if col[u] in pair_set and col[v] in pair_set:
                uf.union(u, v)
        return uf

    hits = violations = 0
    for col in cols_h:
        r = tuple(col[p] for p in c_pos)
        c0, c1, c2, wc, cc_col, dc = r
        if not (wc == c1 and cc_col == c2 and dc == c1 and len({c0, c1, c2}) == 3):
            continue
        c3 = next(c for c in COLORS if c not in {c0, c1, c2})
        uf_23 = pair_uf(col, {c2, c3})
        if uf_23.find(c_pos[2]) != uf_23.find(c_pos[4]):
            continue
        uf_01 = pair_uf(col, {c0, c1})
        rw = uf_01.find(c_pos[3])
        if any(uf_01.find(c_pos[k]) == rw for k in (0, 1, 2, 4, 5)):
            continue
        hits += 1
        col2 = tuple(
            (c0 if col[u] == c1 else c1) if (col[u] in {c0, c1} and uf_01.find(u) == rw) else col[u]
            for u in range(n_h)
        )
        assert col2 in col_set

        uf_02_f = pair_uf(col, {c0, c2})
        uf_02_f2 = pair_uf(col2, {c0, c2})
        uf_13_f = pair_uf(col, {c1, c3})
        uf_13_f2 = pair_uf(col2, {c1, c3})

        cond1 = uf_02_f.find(c_pos[0]) in {uf_02_f.find(c_pos[2]), uf_02_f.find(c_pos[4])}
        cond2 = uf_02_f2.find(c_pos[0]) not in {uf_02_f2.find(c_pos[2]), uf_02_f2.find(c_pos[4])}
        cond3 = uf_13_f.find(c_pos[1]) != uf_13_f.find(c_pos[5])
        cond4 = uf_13_f2.find(c_pos[1]) == uf_13_f2.find(c_pos[5])
        if cond1 and cond2 and cond3 and cond4:
            violations += 1
    return hits, violations


def verify_controls_and_pipeline(ctrl_rec: dict, patterns: list[tuple[int, ...]], residual: int) -> dict:
    d16_pats = {patterns[i] for i in range(len(patterns)) if (residual >> i) & 1}

    # 1. RADIAL-MINDEG5-14
    r14 = ctrl_rec['radial_mindeg5_14']
    verify_embedding_record(r14['embedding'])
    assert r14['embedding']['beta1_h_minus_c0'] == 1
    assert all(v >= 5 for v in r14['embedding']['core_degrees_in_g'].values())
    h14_edges = [tuple(e) for e in r14['embedding']['h_edges']]
    cols_h14 = all_proper_colorings(tuple(range(2, 14)), h14_edges)
    cols_g14 = all_proper_colorings(tuple(range(0, 14)), list(CENTER_ONLY_EDGES) + h14_edges)
    assert len(cols_h14) == 4560 and len(cols_g14) == 1824 == r14['full_g_colorings']
    hits14, viol14 = uf_property_p_check(14, h14_edges, cols_h14)
    assert (hits14, viol14) == (96, 0)
    assert r14['property_P']['trapped_antecedent_hits'] == 96 and r14['property_P']['p_violations'] == 0

    # Independently replay three-step (x1, x2, z) buckets with empty fibres and delayed writeback on RADIAL-MINDEG5-14:
    pipe = r14['three_step_pipeline']
    s1_scope = (1, 2, 3, 4, 7)
    b1_e = [e for e in CENTER_ONLY_EDGES if 0 in e]
    w1 = {
        row: [c0 for c0 in COLORS if all((dict(zip(s1_scope, row)) | {0: c0})[u] != (dict(zip(s1_scope, row)) | {0: c0})[v] for u, v in b1_e)]
        for row in product(COLORS, repeat=5)
    }
    assert sum(map(bool, w1.values())) == 784 == pipe['step1_elim_x1']['nonempty']
    assert sum(not v for v in w1.values()) == 240 == pipe['step1_elim_x1']['empty']

    s2_scope = (2, 3, 4, 5, 6, 7)
    b2_e = [e for e in CENTER_ONLY_EDGES if 1 in e and 0 not in e]
    w2 = {}
    for row in product(COLORS, repeat=6):
        asg = dict(zip(s2_scope, row))
        w2[row] = [
            (c0, c1) for c1 in COLORS
            if all((asg | {1: c1})[u] != (asg | {1: c1})[v] for u, v in b2_e)
            for c0 in w1[tuple((asg | {1: c1})[u] for u in s1_scope)]
        ]
    assert sum(map(bool, w2.values())) == 2728 == pipe['step2_elim_x2']['nonempty']
    assert sum(not v for v in w2.values()) == 1368 == pipe['step2_elim_x2']['empty']

    y_scope = tuple(pipe['step3_elim_z']['scope'])
    assert y_scope == (3, 4, 5, 6, 7, 12)
    z_e = [e for e in h14_edges if 2 in e]
    w3_g, w3_h = {}, {}
    for row in product(COLORS, repeat=len(y_scope)):
        asg = dict(zip(y_scope, row))
        gl, hl = [], []
        for cz in COLORS:
            fz = asg | {2: cz}
            if all(fz[u] != fz[v] for u, v in z_e):
                hl.append(cz)
                for c0, c1 in w2[tuple(fz[u] for u in s2_scope)]:
                    gl.append((c0, c1, cz))
        w3_g[row] = gl
        w3_h[row] = hl
    assert sum(map(bool, w3_g.values())) == pipe['step3_elim_z']['g_bucket_nonempty']
    assert sum(not v for v in w3_g.values()) == pipe['step3_elim_z']['g_bucket_empty']
    assert sum(map(bool, w3_h.values())) == pipe['step3_elim_z']['h_bucket_nonempty']
    assert sum(not v for v in w3_h.values()) == pipe['step3_elim_z']['h_bucket_empty']

    rem_v = tuple(range(3, 14))
    rem_pos = {u: i for i, u in enumerate(rem_v)}
    cols_rem = all_proper_colorings(rem_v, [e for e in h14_edges if 2 not in e])
    wb_h = sorted((cz,) + rc for rc in cols_rem for cz in w3_h[tuple(rc[rem_pos[u]] for u in y_scope)])
    wb_g = sorted((c0, c1, cz) + rc for rc in cols_rem for c0, c1, cz in w3_g[tuple(rc[rem_pos[u]] for u in y_scope)])
    assert wb_h == sorted(cols_h14) and wb_g == sorted(cols_g14)

    # 2. THETA-VIOLATOR-12 (beta_1 = 2 sharp boundary witness)
    t12 = ctrl_rec['theta_violator_12']
    verify_embedding_record(t12['embedding'])
    assert t12['embedding']['beta1_h_minus_c0'] == 2
    h12_edges = [tuple(e) for e in t12['embedding']['h_edges']]
    cols_h12 = all_proper_colorings(tuple(range(2, 12)), h12_edges)
    cols_g12 = all_proper_colorings(tuple(range(0, 12)), list(CENTER_ONLY_EDGES) + h12_edges)
    assert len(cols_h12) == 3240 and len(cols_g12) == 1200 == t12['full_g_colorings']
    hits12, viol12 = uf_property_p_check(12, h12_edges, cols_h12)
    assert (hits12, viol12) == (24, 24)

    # 3. BUFFER-2STEP-19 (beta_1 = 3 full 2-step local survivor)
    b19 = ctrl_rec['buffer_2step_19']
    verify_embedding_record(b19['embedding'])
    assert b19['embedding']['beta1_h_minus_c0'] == 3
    h19_edges = [tuple(e) for e in b19['embedding']['h_edges']]
    f19 = tuple(b19['level2_buffer_certificate']['witness_h_coloring'])
    assert len(f19) == 17 and all(f19[u - 2] != f19[v - 2] for u, v in h19_edges)
    c_pos = tuple(u - 2 for u in CYCLE)
    c_map = {p: i for i, p in enumerate(c_pos)}
    assert tuple(f19[p] for p in c_pos) == (0, 1, 2, 1, 2, 1)

    def uf_bdry_blocks(col):
        res = []
        for s in range(3):
            part = []
            for pair in SPLITS[s]:
                uf = UnionFind(17)
                for u, v in h19_edges:
                    if col[u - 2] in pair and col[v - 2] in pair:
                        uf.union(u - 2, v - 2)
                groups = {}
                for u in range(17):
                    if col[u] in pair:
                        groups.setdefault(uf.find(u), []).append(u)
                for members in groups.values():
                    b = tuple(sorted(c_map[u] for u in members if u in c_map))
                    if b:
                        part.append((pair, b, tuple(members)))
            part.sort(key=lambda x: x[1])
            res.append(part)
        return res

    cs_19 = uf_bdry_blocks(f19)
    swaps_19 = 0
    for s in range(3):
        cs = cs_19[s]
        for m in range(1, 1 << len(cs)):
            swaps_19 += 1
            f2 = list(f19)
            for bit, (pair, _, members) in enumerate(cs):
                if (m >> bit) & 1:
                    ac, bc = pair
                    for u in members:
                        f2[u] = bc if f2[u] == ac else ac
            r2 = tuple(f2[p] for p in c_pos)
            assert normalize(r2) in d16_pats
            cs2 = uf_bdry_blocks(f2)
            for s2 in range(3):
                for m2 in range(1, 1 << len(cs2[s2])):
                    r3 = list(r2)
                    for b2, (p2, b_sub, _) in enumerate(cs2[s2]):
                        if (m2 >> b2) & 1:
                            a2, b2c = p2
                            for pos_i in b_sub:
                                r3[pos_i] = b2c if r3[pos_i] == a2 else a2
                    assert normalize(tuple(r3)) in d16_pats
    assert swaps_19 == 25
    g19_sample = tuple(b19['sample_full_g_coloring'])
    assert len(g19_sample) == 19
    assert all(g19_sample[u] != g19_sample[v] for u, v in list(CENTER_ONLY_EDGES) + h19_edges)

    # 4. Retained KERNEL-936/732 and ZV-17 controls:
    ret = ctrl_rec['retained']
    prior = json.loads((ROOT / PRIOR).read_text())
    zv = json.loads((ROOT / ZV).read_text())
    core = {tuple(e) for e in prior['core_edges']}
    assert core == set(INNER_EDGES) | {(2, 8)}
    complete = {}
    lifts_9 = 0
    for word in product(COLORS, repeat=9):
        if all(word[u] != word[v] for u, v in core):
            lifts_9 += 1
            complete.setdefault(word[3:], []).append(word[:3])
    assert (len(complete), 4 ** 6 - len(complete), lifts_9) == (732, 3364, 936)
    empty_word = (0, 1, 1, 0, 0, 1)
    assert empty_word not in complete
    fixed_ew = dict(zip(range(3, 9), empty_word))
    assert all(fixed_ew[u] != fixed_ew[v] for u, v in core if u >= 3)
    q_h_edges = sorted(tuple(sorted(e)) for e in core if e[0] >= 2 and e[1] >= 2)
    cols_qh = all_proper_colorings(tuple(range(2, 9)), q_h_edges)
    _, qh_viol = uf_property_p_check(9, q_h_edges, cols_qh)
    assert len(cols_qh) == (3 ** 6 + 3) * 3 == 2196 and qh_viol == 0

    zv_contract = zv['contract']
    zv_edges = {tuple(e) for e in zv_contract['original_edges']}
    outer_cycle = zv_contract['C_order']
    attachments = {(3, 9), (4, 13), (5, 11), (6, 15), (2, 16)}
    ring_edges = {tuple(sorted(e)) for e in zip(outer_cycle, outer_cycle[1:] + outer_cycle[:1])}
    assert zv_edges == core | ring_edges | attachments and len(zv_edges) == 29
    zv_counts = zv['outer']['full_counts']
    assert len(zv_counts) == 4 ** 8
    core_colorings = [w for w in product(COLORS, repeat=9) if all(w[u] != w[v] for u, v in core)]
    cache_sig = {}
    proper_zv = 0
    for word, cnt in zip(product(COLORS, repeat=8), zv_counts):
        if not proper_ring(word):
            assert cnt == 0
            continue
        proper_zv += 1
        eta = dict(zip(outer_cycle, word))
        sig = tuple(eta[v] for v in (9, 13, 11, 15, 16))
        if sig not in cache_sig:
            cache_sig[sig] = sum(all(c[u] != eta[v] for u, v in attachments) for c in core_colorings)
        assert cache_sig[sig] == cnt > 0
        h = eta[15]
        p = min(set(COLORS) - {h, eta[9], eta[11]})
        q = min(set(COLORS) - {h, p, eta[13]})
        r = (set(COLORS) - {h, p, q}).pop()
        full_c = dict(enumerate((r, q, h, p, q, p, r, h, p))) | eta
        assert all(full_c[u] != full_c[v] for u, v in zv_edges)
    assert proper_zv == 6564 and sum(zv_counts) == 1529784
    assert ret['zv']['proper_outer_words'] == 6564 and ret['zv']['literal_lifts'] == 1529784

    return dict(
        radial_mindeg5_14=dict(h_colorings=4560, g_colorings=1824, trapped_hits=96, p_violations=0, writeback_bijection=True),
        theta_violator_12=dict(beta1=2, h_colorings=3240, p_violations=24),
        buffer_2step_19=dict(beta1=3, level1_swaps=25, level2_failures=0, g_4colorable_witness=True),
        retained_kernel=dict(nonempty=732, empty=3364, lifts=936, q_h_p_violations=0),
        retained_zv=dict(beta1=1, proper_outer_words=6564, literal_lifts=1529784),
    )


def verify_manifest(results_path: Path) -> dict:
    manifest = json.loads((results_path.parent / 'verification.json').read_text())
    required = {
        PRIOR,
        ZV,
        'scripts/ck_kempe_obstruction.py',
        'scripts/four_color_counts_cone_verification.py',
        'scripts/four_color_three_step_cross_split_exclusion.py',
        'scripts/four_color_three_step_cross_split_replay.py',
    }
    assert set(manifest['sources']) == required
    for rel, expected in manifest['sources'].items():
        actual = sha256((ROOT / rel).read_bytes()).hexdigest()
        assert actual == expected, f'SHA mismatch on {rel}'
    assert manifest['outputs'] == {'results.json': sha256(results_path.read_bytes()).hexdigest()}
    return dict(source_hashes=len(required), result_hash=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, required=True)
    args = parser.parse_args()

    data = json.loads(args.results.read_text())
    assert data['contract']['original_cycle'] == list(CYCLE)
    assert data['contract']['inner_edges'] == [list(e) for e in INNER_EDGES]

    patterns, accepted, residual = reconstruct_d_and_minimality(data['old_and_b6_baseline'])
    b6_summary = verify_b6_cone(patterns, residual, data['old_and_b6_baseline']['b6_signed_matching_cone'])
    excl_summary = verify_exit_bounds_and_universal_exclusion(
        patterns, residual, data['auxiliary_1step_exit_bounds'], data['universal_exclusion_of_d16']
    )
    ctrl_summary = verify_controls_and_pipeline(
        data['three_step_preservation_and_controls'], patterns, residual
    )
    manifest_summary = verify_manifest(args.results)

    print(json.dumps(dict(
        status='PASS',
        proper_c0_patterns=len(patterns),
        inside_accepted_patterns=accepted.bit_count(),
        d_residual_patterns=residual.bit_count(),
        d_minimal_nonempty_subsets=1,
        b6_cone_comparison=b6_summary,
        universal_p_exclusion=excl_summary,
        controls_and_three_step_writeback=ctrl_summary,
        manifest=manifest_summary,
        open_boundaries=[
            'general planar exteriors with beta_1(H - V(C0)) >= 2',
            '4CT-free existence of Col_4(H) != empty',
            'general 4CT',
        ],
    ), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
