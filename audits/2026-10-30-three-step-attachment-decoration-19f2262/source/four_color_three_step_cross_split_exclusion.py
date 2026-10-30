#!/usr/bin/env python3
"""Cross-split trapped-swap exclusion of PAIR-C0-D16 on radial-annulus planar sources.

Fixes original C0 = (z, a, b, w, c, d), full two-center neighborhoods N(x1), N(x2),
and the common exterior source contract H = G - {x1, x2} on the exterior closed disk
Omega bounded by C0. Certifies:
  1. D-minimality (1 / 65,535 non-empty subsets) and standard B6 signed-matching
     feasibility (27 active integer signatures) of PAIR-C0-D16;
  2. Universal exclusion of PAIR-C0-D16 under the cross-split trapped-swap
     no-dual-reversal property P (proved without 4CT for all planar disk exteriors
     with beta_1(H - V(C0)) <= 1);
  3. Three-step (x1, x2, z) exact join, projection with complete/empty witness
     fibres, and delayed writeback preservation on RADIAL-MINDEG5-14, sharp
     beta_1 = 2 / beta_1 = 3 boundary controls, and retained KERNEL-936/732 + ZV-17.

No 4CT assumption, coloring oracle, or graph-size truncation of the paper theorem is used.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import subprocess

import ck_kempe_obstruction as old
from four_color_counts_cone_verification import compatible, integrate, signatures

ROOT = Path(__file__).resolve().parents[1]
COLORS = tuple(range(4))
SPLITS = old.PAIRS
CYCLE = (2, 3, 4, 7, 5, 6)  # (z, a, b, w, c, d)
CYCLE_NAMES = ('z', 'a', 'b', 'w', 'c', 'd')
CENTER_ONLY_EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 7),
    (1, 2), (1, 5), (1, 6), (1, 7),
)
C0_EDGES = ((2, 3), (3, 4), (4, 7), (5, 7), (5, 6), (2, 6))
INNER_EDGES = tuple(sorted(tuple(sorted(e)) for e in CENTER_ONLY_EDGES + C0_EDGES))
PRIOR = 'audits/2026-10-29-three-step-relation-control-e1a90fe/results.json'
ZV = 'audits/2026-10-30-three-step-shared-exterior-e1a90fe/results.json'

# Canonical B6 integer primal ray on PAIR-C0-D16 (27 active signatures, n_4 = 1).
B6_ACTIVE_WEIGHTS = (
    (7, 1), (9, 1), (13, 1), (15, 2), (17, 1), (19, 1), (21, 1),
    (34, 1), (42, 1), (46, 1), (54, 1), (62, 1), (63, 1), (75, 1),
    (79, 1), (87, 2), (90, 1), (95, 1), (110, 1), (115, 1), (119, 1),
    (134, 1), (138, 1), (142, 1), (146, 1), (156, 1), (178, 1),
)

# Control A: RADIAL-MINDEG5-14 (G has 14 vertices, H has 12 vertices, beta_1(H - C0) = 1).
RADIAL14_H_EDGES = (
    (2, 3), (2, 6), (2, 12), (3, 4), (3, 12), (3, 13), (4, 7), (4, 8),
    (4, 13), (5, 6), (5, 7), (5, 10), (5, 11), (6, 11), (6, 12), (7, 8),
    (7, 9), (7, 10), (8, 9), (8, 13), (9, 10), (10, 11), (11, 12), (12, 13),
)
RADIAL14_G_FACES = (
    (0, 1, 7), (0, 2, 1), (0, 3, 2), (0, 4, 3), (0, 7, 4),
    (1, 2, 6), (1, 5, 7), (1, 6, 5), (2, 3, 12), (2, 12, 6),
    (3, 4, 13), (3, 13, 12), (4, 7, 8), (4, 8, 13), (5, 6, 11),
    (5, 10, 7), (5, 11, 10), (6, 12, 11), (7, 9, 8), (7, 10, 9),
    (8, 9, 10, 11, 12, 13),
)
# Explicit H-coloring on vertices 2..13 at #20 (z=0,a=1,b=2,c=2,d=1,w=1) surviving 1-step D16 cubes:
RADIAL14_WITNESS_H = (0, 1, 2, 2, 1, 1, 3, 2, 3, 0, 2, 0)

# Control B: THETA-VIOLATOR-12 (G has 12 vertices, H has 10 vertices, H - C0 ~= K4 - e, beta_1 = 2).
THETA12_H_EDGES = (
    (2, 3), (2, 6), (2, 9), (3, 4), (3, 8), (4, 7), (4, 8), (4, 11), (5, 6),
    (5, 7), (5, 10), (6, 10), (7, 11), (8, 9), (8, 11), (9, 10), (9, 11), (10, 11),
)
THETA12_G_FACES = (
    (0, 1, 7), (0, 2, 1), (0, 3, 2), (0, 4, 3), (0, 7, 4),
    (1, 2, 6), (1, 5, 7), (1, 6, 5), (2, 3, 8, 9), (2, 9, 10, 6),
    (3, 4, 8), (4, 7, 11), (4, 11, 8), (5, 6, 10), (5, 10, 11, 7),
    (8, 11, 9), (9, 11, 10),
)
THETA12_WITNESS_H = (0, 1, 2, 2, 1, 1, 3, 2, 3, 0)

# Control C: BUFFER-2STEP-19 (G has 19 vertices, H has 17 vertices, beta_1(H - C0) = 3).
BUFFER19_H_EDGES = (
    (2, 3), (2, 6), (2, 8), (2, 10), (2, 11), (2, 14), (3, 4), (3, 10), (4, 7),
    (4, 9), (4, 10), (4, 12), (5, 6), (5, 7), (5, 9), (5, 11), (5, 13), (5, 15),
    (5, 16), (5, 18), (6, 13), (7, 12), (7, 16), (8, 9), (8, 10), (8, 11),
    (9, 10), (9, 11), (9, 12), (9, 17), (11, 14), (12, 17), (13, 14), (14, 15),
    (16, 17), (17, 18),
)
BUFFER19_G_FACES = (
    (0, 1, 7), (0, 2, 1), (0, 3, 2), (0, 4, 3), (0, 7, 4),
    (1, 2, 6), (1, 5, 7), (1, 6, 5), (2, 3, 10), (2, 8, 11),
    (2, 10, 8), (2, 11, 14), (2, 14, 13, 6), (3, 4, 10), (4, 7, 12),
    (4, 9, 10), (4, 12, 9), (5, 6, 13), (5, 9, 17, 18), (5, 11, 9),
    (5, 13, 14, 15), (5, 15, 14, 11), (5, 16, 7), (5, 18, 17, 16),
    (7, 16, 17, 12), (8, 9, 11), (8, 10, 9), (9, 12, 17),
)
BUFFER19_WITNESS_H = (0, 1, 2, 2, 1, 1, 2, 0, 3, 3, 3, 3, 1, 0, 0, 1, 3)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def literal_options(row: tuple[int, ...], split: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
    """Transport complete normalized noncrossing options using ONE common color map."""
    normalized = old.normalize(row)
    mapping = {}
    for actual, canonical in zip(row, normalized):
        mapping[canonical] = actual
    for canonical, actual in zip(sorted(set(COLORS) - mapping.keys()),
                                 sorted(set(COLORS) - set(mapping.values()))):
        mapping[canonical] = actual
    canonical_split = next(
        s for s, pairs in enumerate(SPLITS)
        if {frozenset(mapping[c] for c in p) for p in pairs}
        == {frozenset(p) for p in SPLITS[split]}
    )
    idx = old.patterns(6).index(normalized)
    return tuple(blocks for _, blocks in old.partition_options(6, idx, canonical_split))


def switched(row: tuple[int, ...], blocks: tuple[tuple[int, ...], ...],
             split: int, selected: int) -> tuple[int, ...]:
    mate = {a: b for pair in SPLITS[split] for a, b in (pair, pair[::-1])}
    changed = list(row)
    for i, block in enumerate(blocks):
        if (selected >> i) & 1:
            for v in block:
                changed[v] = mate[row[v]]
    return tuple(changed)


def verify_sphere_and_disk_embedding(n_g: int, h_edges: tuple[tuple[int, int], ...],
                                     g_faces: tuple[tuple[int, ...], ...]) -> dict:
    """Combinatorial genus-0 sphere check on G and induced facial-C0 disk check on H."""
    g_edges = tuple(sorted(set(CENTER_ONLY_EDGES) | {tuple(sorted(e)) for e in h_edges}))
    darts = Counter(
        (face[i], face[(i + 1) % len(face)])
        for face in g_faces for i in range(len(face))
    )
    expected_darts = Counter({(u, v): 1 for u, v in g_edges} | {(v, u): 1 for u, v in g_edges})
    assert darts == expected_darts
    assert n_g - len(g_edges) + len(g_faces) == 2

    rot_g = {}
    for u in range(n_g):
        nxt = {}
        for face in g_faces:
            L = len(face)
            for i, v in enumerate(face):
                if v == u:
                    prev_v = face[(i - 1) % L]
                    assert prev_v not in nxt
                    nxt[prev_v] = face[(i + 1) % L]
        start = min(nxt)
        order = [start]
        cur = nxt[start]
        while cur != start:
            order.append(cur)
            cur = nxt[cur]
        assert len(order) == len(nxt)
        rot_g[u] = order

    # Induced embedding on H = G - {0, 1}:
    rot_h = {u: [v for v in rot_g[u] if v >= 2] for u in range(2, n_g)}
    seen_h = set()
    h_faces = []
    for u in range(2, n_g):
        for v in rot_h[u]:
            if (u, v) not in seen_h:
                walk = []
                cu, cv = u, v
                while (cu, cv) not in seen_h:
                    seen_h.add((cu, cv))
                    walk.append(cu)
                    r = rot_h[cv]
                    cu, cv = cv, r[(r.index(cu) + 1) % len(r)]
                m = min(walk)
                k = walk.index(m)
                h_faces.append(tuple(walk[k:] + walk[:k]))
    h_faces.sort()
    n_h = n_g - 2
    assert n_h - len(h_edges) + len(h_faces) == 2
    c0_set = set(CYCLE)
    c0_facial = [f for f in h_faces if len(f) == 6 and set(f) == c0_set]
    assert len(c0_facial) == 1
    # Verify cyclic order of C0 face is CYCLE or reversed CYCLE:
    fw = c0_facial[0]
    i2 = fw.index(2)
    fw_rot = fw[i2:] + fw[:i2]
    assert fw_rot in (CYCLE, (2, 6, 5, 7, 4, 3))

    # Exterior subgraph H_ext = H - V(C0): compute exact cycle rank beta_1(H_ext).
    ext_verts = sorted(set(range(2, n_g)) - c0_set)
    ext_edges = [e for e in h_edges if e[0] not in c0_set and e[1] not in c0_set]
    adj_ext = {u: [] for u in ext_verts}
    for u, v in ext_edges:
        adj_ext[u].append(v)
        adj_ext[v].append(u)
    visited = set()
    cc = 0
    for u in ext_verts:
        if u not in visited:
            cc += 1
            q = deque([u])
            visited.add(u)
            while q:
                x = q.popleft()
                for y in adj_ext[x]:
                    if y not in visited:
                        visited.add(y)
                        q.append(y)
    beta1 = len(ext_edges) - len(ext_verts) + cc
    degs_g = {u: len(rot_g[u]) for u in range(8)}
    return dict(
        n_vertices_g=n_g,
        n_edges_g=len(g_edges),
        n_faces_g=len(g_faces),
        n_vertices_h=n_h,
        n_edges_h=len(h_edges),
        n_faces_h=len(h_faces),
        h_edges=[list(e) for e in sorted(tuple(sorted(e)) for e in h_edges)],
        g_oriented_faces=[list(f) for f in g_faces],
        h_oriented_faces=[list(f) for f in h_faces],
        c0_facial_walk=list(c0_facial[0]),
        ext_vertices=len(ext_verts),
        ext_edges=len(ext_edges),
        ext_components=cc,
        beta1_h_minus_c0=beta1,
        core_degrees_in_g={str(u): degs_g[u] for u in range(8)},
    )


def enumerate_colorings(vertices: tuple[int, ...],
                        edges: tuple[tuple[int, int], ...]) -> list[tuple[int, ...]]:
    v_set = set(vertices)
    pos = {u: i for i, u in enumerate(vertices)}
    prev_neighbors = []
    for i, u in enumerate(vertices):
        p = [pos[v] for a, b in edges if (a == u and b in v_set and pos[b] < i)
             or (b == u and a in v_set and pos[a] < i)
             for v in ((b if a == u else a),)]
        prev_neighbors.append(tuple(sorted(set(p))))
    results = []
    col = [0] * len(vertices)

    def backtrack(idx: int) -> None:
        if idx == len(vertices):
            results.append(tuple(col))
            return
        used = {col[j] for j in prev_neighbors[idx]}
        for c in COLORS:
            if c not in used:
                col[idx] = c
                backtrack(idx + 1)

    backtrack(0)
    return results


def build_b6_certificate(pats: list[tuple[int, ...]], residual_mask: int) -> dict:
    words = tuple(
        w for w in product((1, 2, 3), repeat=6)
        if all(w.count(c) % 2 == 0 for c in (1, 2, 3))
    )
    sigs = tuple(signatures(6))
    lookup = {b: j for j, b in enumerate(pats)}
    states = [lookup[old.normalize(integrate(w))] for w in words]
    rows = [(i, pair) for i in range(len(words)) for pair in combinations((1, 2, 3), 2)]
    columns = [
        tuple(r for r, (i, pair) in enumerate(rows) if compatible(words[i], pair, s))
        for s in sigs
    ]
    eligible = [
        s for s, col in enumerate(columns)
        if col and all((residual_mask >> states[rows[r][0]]) & 1 for r in col)
    ]
    weights = dict(B6_ACTIVE_WEIGHTS)
    assert set(weights).issubset(set(eligible))

    row_sums = [0] * len(rows)
    for s_idx, w in weights.items():
        for r in columns[s_idx]:
            row_sums[r] += w

    pattern_weights = {}
    for r, (i, _) in enumerate(rows):
        st = states[i]
        if (residual_mask >> st) & 1:
            if st in pattern_weights:
                assert pattern_weights[st] == row_sums[r]
            else:
                pattern_weights[st] = row_sums[r]
                assert pattern_weights[st] > 0
        else:
            assert row_sums[r] == 0

    assert len(words) == 183 and len(sigs) == 191 and len(rows) == 549
    assert len(eligible) == 29 and len(weights) == 27
    return dict(
        parity_words=len(words),
        signed_signatures=len(sigs),
        linear_equations=len(rows),
        eligible_signatures=len(eligible),
        active_signatures=len(weights),
        primal_signature_weights=[
            dict(signature_index=s_idx,
                 matching=[[a, b, sign] for a, b, sign in sigs[s_idx]],
                 weight=w)
            for s_idx, w in B6_ACTIVE_WEIGHTS
        ],
        induced_pattern_multiplicities={str(k): v for k, v in sorted(pattern_weights.items())},
        canonical_total_weight=sum(pattern_weights.values()),
        literal_total_weight=24 * sum(pattern_weights.values()),
    )


def check_d_minimality(residual_mask: int) -> dict:
    table = old.obligations(6)
    active = [i for i in range(len(table)) if (residual_mask >> i) & 1]
    assert len(active) == 16
    d_fixed = []
    for sub in range(1, 1 << len(active)):
        mask = 0
        for bit, idx in enumerate(active):
            if (sub >> bit) & 1:
                mask |= 1 << idx
        if old.failure(mask, table) is None:
            d_fixed.append(mask)
    assert d_fixed == [residual_mask]
    return dict(
        nonempty_subsets_tested=(1 << len(active)) - 1,
        d_consistent_nonempty_subsets=d_fixed,
        is_minimal_nonempty_d_fixed=True,
    )


def build_auxiliary_exit_bounds(pats: list[tuple[int, ...]], residual_mask: int) -> dict:
    d16_indices = [i for i in range(len(pats)) if (residual_mask >> i) & 1]
    d16_set = {pats[i] for i in d16_indices}
    chordless = []
    for i in range(6):
        for j in range(i + 1, 6):
            if (j - i) % 6 in (1, 5):
                continue
            mono = [idx for idx in d16_indices if pats[idx][i] == pats[idx][j]]
            assert len(mono) >= 2
            chordless.append(dict(
                positions=[i, j],
                names=[CYCLE_NAMES[i], CYCLE_NAMES[j]],
                monochromatic_pattern_indices=mono,
            ))

    bounds = []
    expected_lb = (1, 2, 2, 1, 2, 2)
    for v in range(6):
        prev_v, next_v = (v - 1) % 6, (v + 1) % 6
        best_lb = 0
        witnesses = []
        for idx in (4, 20):
            r = pats[idx]
            forced = []
            for s_idx, split in enumerate(SPLITS):
                opts = [
                    b for b in literal_options(r, s_idx)
                    if all(old.normalize(switched(r, b, s_idx, sel)) in d16_set
                           for sel in range(1 << len(b)))
                ]
                pair = split[0] if r[v] in split[0] else split[1]
                other = pair[0] if pair[1] == r[v] else pair[1]
                if r[prev_v] in pair or r[next_v] in pair:
                    continue
                if all(any(v in blk and len(blk) >= 2 for blk in P) for P in opts):
                    forced.append(dict(split=s_idx, pair=list(pair), forced_exterior_color=other))
            distinct = sorted({item['forced_exterior_color'] for item in forced})
            if len(distinct) > best_lb:
                best_lb = len(distinct)
                witnesses = [dict(pattern_index=idx, pattern=list(r), forced_exits=forced)]
        assert best_lb == expected_lb[v]
        inner_center_deg = 2 if v in (0, 3) else 1
        bounds.append(dict(
            position=v,
            vertex_name=CYCLE_NAMES[v],
            vertex_id=CYCLE[v],
            min_exterior_neighbors_outside_c0=best_lb,
            min_full_graph_degree=2 + inner_center_deg + best_lb,
            witness=witnesses[0],
        ))
    return dict(
        c0_nonadjacent_pairs=len(chordless),
        chordlessness_witnesses=chordless,
        vertex_exit_lower_bounds=bounds,
    )


def verify_universal_p_exclusion(pats: list[tuple[int, ...]], residual_mask: int) -> dict:
    d16_set = {pats[i] for i in range(len(pats)) if (residual_mask >> i) & 1}
    lit_rows = sorted({
        tuple(perm[c] for c in r)
        for r in d16_set for perm in permutations(COLORS)
    })
    support = set(lit_rows)
    assert len(lit_rows) == 384

    def allowed_partitions(row: tuple[int, ...], split: int) -> list[tuple[tuple[int, ...], ...]]:
        return [
            blocks for blocks in literal_options(row, split)
            if all(switched(row, blocks, split, sel) in support
                   for sel in range(1 << len(blocks)))
        ]

    orbit_20_records = []
    for perm in sorted(permutations(COLORS)):
        c0, c1, c2, c3 = perm
        r0 = (c0, c1, c2, c1, c2, c1)
        assert r0 in support and old.normalize(r0) == (0, 1, 2, 1, 2, 1)
        s_premise = next(
            s for s, pairs in enumerate(SPLITS)
            if {frozenset(p) for p in pairs} == {frozenset((c0, c1)), frozenset((c2, c3))}
        )
        s_second = next(
            s for s, pairs in enumerate(SPLITS)
            if {frozenset(p) for p in pairs} == {frozenset((c0, c2)), frozenset((c1, c3))}
        )
        opts_p = allowed_partitions(r0, s_premise)
        opts_s = allowed_partitions(r0, s_second)
        assert opts_p == [((0, 1, 5), (2, 4), (3,))]
        assert opts_s == [((0, 2, 4), (1,), (3,), (5,))]

        # Swap trapped block (3,) = {w}:
        r0_prime = (c0, c1, c2, c0, c2, c1)
        assert r0_prime in support and old.normalize(r0_prime) == (0, 1, 2, 0, 2, 1)
        opts_s_prime = allowed_partitions(r0_prime, s_second)
        assert opts_s_prime == [((0,), (1, 5), (2, 3, 4))]

        orbit_20_records.append(dict(
            color_frame=list(perm),
            source_row=list(r0),
            premise_split=s_premise,
            unique_premise_partition=[list(b) for b in opts_p[0]],
            second_split=s_second,
            unique_source_second_partition=[list(b) for b in opts_s[0]],
            trapped_swap_target_row=list(r0_prime),
            unique_target_second_partition=[list(b) for b in opts_s_prime[0]],
        ))

    assert len(orbit_20_records) == 24
    return dict(
        orbit_20_canonical_pattern=[0, 1, 2, 1, 2, 1],
        target_13_canonical_pattern=[0, 1, 2, 0, 2, 1],
        literal_witness_frames_checked=len(orbit_20_records),
        all_three_relevant_partition_sets_unique=True,
        representative_choice_used=False,
        admissible_common_source_annotations_for_d16=0,
        nonempty_complement_subsets_total=(1 << 18) - 1,
        admissible_nonempty_complement_subsets_under_P=0,
        literal_records=orbit_20_records,
    )


def evaluate_property_p_on_graph(n_g: int, h_edges: tuple[tuple[int, int], ...],
                                 cols_h: list[tuple[int, ...]]) -> dict:
    n_h = n_g - 2
    c_pos = tuple(u - 2 for u in CYCLE)  # (z, a, b, w, c, d) indices in 0..n_h-1
    adj = [[] for _ in range(n_h)]
    for u, v in h_edges:
        adj[u - 2].append(v - 2)
        adj[v - 2].append(u - 2)

    def component(col: tuple[int, ...] | list[int], pair: set[int], start: int) -> set[int]:
        seen = {start}
        q = deque([start])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w not in seen and col[w] in pair:
                    seen.add(w)
                    q.append(w)
        return seen

    col_set = set(cols_h)
    antecedent_hits = 0
    violations = []
    for col in cols_h:
        r = tuple(col[p] for p in c_pos)
        c0, c1, c2, w_c, c_c, d_c = r
        if not (w_c == c1 and c_c == c2 and d_c == c1 and len({c0, c1, c2}) == 3):
            continue
        c3 = next(c for c in COLORS if c not in {c0, c1, c2})
        if c_pos[4] not in component(col, {c2, c3}, c_pos[2]):
            continue
        kw = component(col, {c0, c1}, c_pos[3])
        if (kw & set(c_pos)) != {c_pos[3]}:
            continue
        antecedent_hits += 1
        swapped = list(col)
        for u in kw:
            swapped[u] = c0 if swapped[u] == c1 else c1
        swapped_t = tuple(swapped)
        assert swapped_t in col_set

        kz_f = component(col, {c0, c2}, c_pos[0])
        cond1 = (c_pos[2] in kz_f) or (c_pos[4] in kz_f)
        kz_f2 = component(swapped_t, {c0, c2}, c_pos[0])
        cond2 = (c_pos[2] not in kz_f2) and (c_pos[4] not in kz_f2)
        ka_f = component(col, {c1, c3}, c_pos[1])
        cond3 = (c_pos[5] not in ka_f)
        ka_f2 = component(swapped_t, {c1, c3}, c_pos[1])
        cond4 = (c_pos[5] in ka_f2)
        if cond1 and cond2 and cond3 and cond4:
            violations.append(dict(
                source_coloring=list(col),
                swapped_component_vertices=sorted(u + 2 for u in kw),
                target_coloring=list(swapped_t),
            ))

    return dict(
        total_h_colorings=len(cols_h),
        color_pair_partitions_checked=6 * len(cols_h),
        trapped_antecedent_hits=antecedent_hits,
        p_violations=len(violations),
        satisfies_property_P=(len(violations) == 0),
        sample_violation=violations[0] if violations else None,
    )


def verify_three_step_buckets_and_writeback(n_g: int,
                                            h_edges: tuple[tuple[int, int], ...],
                                            cols_h: list[tuple[int, ...]],
                                            cols_g: list[tuple[int, ...]]) -> dict:
    """Exact three-step elimination (x1, x2, z) with ALL empty fibres and delayed writeback."""
    # Bucket 1: eliminate x1 = 0 from {01, 02, 03, 04, 07} -> scope S1 = (1, 2, 3, 4, 7)
    s1_scope = (1, 2, 3, 4, 7)
    b1_edges = tuple(e for e in CENTER_ONLY_EDGES if 0 in e)
    w1 = {}
    for row in product(COLORS, repeat=5):
        assign = dict(zip(s1_scope, row))
        w1[row] = [
            c0 for c0 in COLORS
            if all((assign | {0: c0})[u] != (assign | {0: c0})[v] for u, v in b1_edges)
        ]
    b1_nonempty = sum(1 for v in w1.values() if v)
    b1_empty = len(w1) - b1_nonempty
    assert (b1_nonempty, b1_empty) == (784, 240)

    # Bucket 2: eliminate x2 = 1 using Bucket 1 + {12, 15, 16, 17} -> scope S2 = (2, 3, 4, 5, 6, 7)
    s2_scope = (2, 3, 4, 5, 6, 7)
    b2_edges = tuple(e for e in CENTER_ONLY_EDGES if 1 in e and 0 not in e)
    w2 = {}
    for row in product(COLORS, repeat=6):
        assign = dict(zip(s2_scope, row))
        lifts = []
        for c1 in COLORS:
            full1 = assign | {1: c1}
            if all(full1[u] != full1[v] for u, v in b2_edges):
                s1_key = tuple(full1[u] for u in s1_scope)
                for c0 in w1[s1_key]:
                    lifts.append((c0, c1))
        w2[row] = lifts
    b2_nonempty = sum(1 for v in w2.values() if v)
    b2_empty = len(w2) - b2_nonempty
    assert (b2_nonempty, b2_empty) == (2728, 1368)

    # Bucket 3: eliminate z = 2 using Bucket 2 + all H-edges incident to z = 2!
    z_edges = tuple(e for e in h_edges if 2 in e)
    z_neighbors = tuple(sorted({v if u == 2 else u for u, v in z_edges}))
    y_scope = tuple(sorted({3, 4, 5, 6, 7} | set(z_neighbors)))
    w3_g = {}
    w3_h = {}
    for row in product(COLORS, repeat=len(y_scope)):
        assign = dict(zip(y_scope, row))
        g_lifts = []
        h_lifts = []
        for cz in COLORS:
            fullz = assign | {2: cz}
            if all(fullz[u] != fullz[v] for u, v in z_edges):
                h_lifts.append(cz)
                s2_key = tuple(fullz[u] for u in s2_scope)
                for c0, c1 in w2[s2_key]:
                    g_lifts.append((c0, c1, cz))
        w3_g[row] = g_lifts
        w3_h[row] = h_lifts

    b3_g_nonempty = sum(1 for v in w3_g.values() if v)
    b3_g_empty = len(w3_g) - b3_g_nonempty
    b3_h_nonempty = sum(1 for v in w3_h.values() if v)
    b3_h_empty = len(w3_h) - b3_h_nonempty

    # Remaining exterior edges of H - {z}:
    rem_verts = tuple(u for u in range(3, n_g))
    rem_edges = tuple(e for e in h_edges if 2 not in e)
    cols_rem = enumerate_colorings(rem_verts, rem_edges)
    rem_pos = {u: i for i, u in enumerate(rem_verts)}

    # Delayed reverse writeback for H and for G:
    written_back_h = []
    written_back_g = []
    for r_col in cols_rem:
        y_key = tuple(r_col[rem_pos[u]] for u in y_scope)
        for cz in w3_h[y_key]:
            written_back_h.append((cz,) + r_col)
        for c0, c1, cz in w3_g[y_key]:
            written_back_g.append((c0, c1, cz) + r_col)

    written_back_h.sort()
    written_back_g.sort()
    assert written_back_h == sorted(cols_h)
    assert written_back_g == sorted(cols_g)

    # Also check the 10-point local kernel on Y when joined with {ab, bw, wc, cd}:
    c0_rem = ((3, 4), (4, 7), (5, 7), (5, 6))
    y_pos = {u: i for i, u in enumerate(y_scope)}
    k_nonempty = k_empty = k_lifts = 0
    for y_row, lifts in w3_g.items():
        if lifts and all(y_row[y_pos[u]] != y_row[y_pos[v]] for u, v in c0_rem):
            k_nonempty += 1
            k_lifts += len(lifts)
        else:
            k_empty += 1

    return dict(
        step1_elim_x1=dict(scope=list(s1_scope), nonempty=b1_nonempty, empty=b1_empty),
        step2_elim_x2=dict(scope=list(s2_scope), nonempty=b2_nonempty, empty=b2_empty),
        step3_elim_z=dict(
            scope=list(y_scope),
            z_incident_edges=[list(e) for e in z_edges],
            g_bucket_nonempty=b3_g_nonempty,
            g_bucket_empty=b3_g_empty,
            h_bucket_nonempty=b3_h_nonempty,
            h_bucket_empty=b3_h_empty,
            local_c0_joined_nonempty=k_nonempty,
            local_c0_joined_empty=k_empty,
            local_c0_joined_lifts=k_lifts,
        ),
        delayed_writeback=dict(
            remaining_h_minus_z_colorings=len(cols_rem),
            recovered_h_colorings=len(written_back_h),
            recovered_g_colorings=len(written_back_g),
            exact_bijection_verified=True,
        ),
    )


def verify_2step_buffer_witness(n_g: int, h_edges: tuple[tuple[int, int], ...],
                                f_h: tuple[int, ...], d16_set: set[tuple[int, ...]]) -> dict:
    n_h = n_g - 2
    assert len(f_h) == n_h
    for u, v in h_edges:
        assert f_h[u - 2] != f_h[v - 2]
    c_pos = tuple(u - 2 for u in CYCLE)
    assert tuple(f_h[p] for p in c_pos) == (0, 1, 2, 1, 2, 1)

    adj = [[] for _ in range(n_h)]
    for u, v in h_edges:
        adj[u - 2].append(v - 2)
        adj[v - 2].append(u - 2)

    def bdry_comps(col: list[int] | tuple[int, ...]):
        res = []
        c_map = {p: idx for idx, p in enumerate(c_pos)}
        for s in range(3):
            part = []
            for pair in SPLITS[s]:
                seen = set()
                for start in range(n_h):
                    if col[start] in pair and start not in seen:
                        comp = []
                        q = deque([start])
                        seen.add(start)
                        while q:
                            u = q.popleft()
                            comp.append(u)
                            for w in adj[u]:
                                if w not in seen and col[w] in pair:
                                    seen.add(w)
                                    q.append(w)
                        b = tuple(sorted(c_map[u] for u in comp if u in c_map))
                        if b:
                            part.append((pair, b, tuple(comp)))
            part.sort(key=lambda x: x[1])
            res.append(part)
        return res

    cs_f = bdry_comps(f_h)
    swaps_tested = 0
    level2_failures = 0
    for s in range(3):
        cs = cs_f[s]
        for m in range(1, 1 << len(cs)):
            swaps_tested += 1
            f2 = list(f_h)
            for bit, (pair, _, comp) in enumerate(cs):
                if (m >> bit) & 1:
                    ac, bc = pair
                    for u in comp:
                        f2[u] = bc if f2[u] == ac else ac
            r2 = tuple(f2[p] for p in c_pos)
            assert old.normalize(r2) in d16_set
            cs2 = bdry_comps(f2)
            for s2 in range(3):
                for m2 in range(1, 1 << len(cs2[s2])):
                    r3 = list(r2)
                    for b2, (p2, b_sub, _) in enumerate(cs2[s2]):
                        if (m2 >> b2) & 1:
                            a2, b2c = p2
                            for pos_i in b_sub:
                                r3[pos_i] = b2c if r3[pos_i] == a2 else a2
                    if old.normalize(tuple(r3)) not in d16_set:
                        level2_failures += 1
    assert swaps_tested == 25 and level2_failures == 0
    return dict(
        witness_h_coloring=list(f_h),
        c0_coloring=[0, 1, 2, 1, 2, 1],
        level1_nonempty_cube_swaps_tested=swaps_tested,
        level2_d16_closure_failures=level2_failures,
    )


def verify_retained_controls(prior: dict, zv: dict) -> dict:
    core = tuple(tuple(e) for e in prior['core_edges'])
    kernel = prior['kernel']
    boundary = tuple(kernel['boundary_order'])
    actual = []
    for row in product(COLORS, repeat=6):
        fixed = dict(zip(boundary, row))
        actual.append([
            lift for lift in product(COLORS, repeat=3)
            if all((fixed | dict(enumerate(lift)))[a]
                   != (fixed | dict(enumerate(lift)))[b] for a, b in core)
        ])
    assert actual == [[tuple(lift) for lift in fibre] for fibre in kernel['full_fibres']]
    empty_word = (0, 1, 1, 0, 0, 1)
    empty_idx = sum(c * 4 ** (5 - i) for i, c in enumerate(empty_word))
    assert actual[empty_idx] == []
    rem_edges = [(a, b) for a, b in core if a >= 3]
    colors = dict(zip(boundary, empty_word))
    assert all(colors[a] != colors[b] for a, b in rem_edges)

    # Check 7-vertex core exterior Q - {0, 1} directly for Property P:
    q_h_edges = tuple(sorted(tuple(sorted(e)) for e in core if e[0] >= 2 and e[1] >= 2))
    cols_qh = enumerate_colorings(tuple(range(2, 9)), q_h_edges)
    p_qh = evaluate_property_p_on_graph(9, q_h_edges, cols_qh)
    # C6 has 3**6 + 3 = 732 proper four-colorings; the pendant vertex
    # has three choices for each. This counts H, before either center is joined.
    assert len(cols_qh) == 2196 and p_qh['p_violations'] == 0

    # Check ZV-17 embedding, beta_1(H - C0) = 1, and all 65,536 outer words:
    zv_edges = tuple(tuple(e) for e in zv['contract']['original_edges'])
    zv_h_edges = tuple(sorted(tuple(sorted(e)) for e in zv_edges if e[0] >= 2 and e[1] >= 2))
    zv_faces = tuple(tuple(f) for f in zv['contract']['oriented_faces'])
    zv_emb = verify_sphere_and_disk_embedding(17, zv_h_edges, zv_faces)
    assert zv_emb['beta1_h_minus_c0'] == 1

    counts = zv['outer']['full_counts']
    assert len(counts) == 4 ** 8
    proper_count = 0
    for word, count in zip(product(COLORS, repeat=8), counts):
        is_prop = all(word[i] != word[(i + 1) % 8] for i in range(8))
        assert (count > 0) == is_prop
        proper_count += is_prop
        if is_prop:
            eta = dict(zip(zv['contract']['C_order'], word))
            h = eta[15]
            p = next(c for c in COLORS if c not in {h, eta[9], eta[11]})
            q = next(c for c in COLORS if c not in {h, p, eta[13]})
            r = next(c for c in COLORS if c not in {h, p, q})
            f = eta | dict(enumerate((r, q, h, p, q, p, r, h, p)))
            assert all(f[a] != f[b] for a, b in zv_edges)
    assert proper_count == 6564 and sum(counts) == 1529784

    return dict(
        planar_kernel=dict(
            nonempty=sum(map(bool, actual)),
            empty=sum(not f for f in actual),
            lifts=sum(map(len, actual)),
            proper_empty_word=list(empty_word),
            core_exterior_colorings=len(cols_qh),
            core_exterior_beta1=0,
            core_exterior_p_violations=p_qh['p_violations'],
        ),
        zv=dict(
            n_vertices_g=17,
            n_edges_g=len(zv_edges),
            n_faces_g=len(zv_faces),
            beta1_h_minus_c0=zv_emb['beta1_h_minus_c0'],
            in_covered_source_class_S_rad=True,
            proper_outer_words=proper_count,
            empty_improper_outer_words=len(counts) - proper_count,
            accepted_outer_words=proper_count,
            literal_lifts=sum(counts),
            constructive_extension_rechecked=True,
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()

    prior = json.loads((ROOT / PRIOR).read_text())
    zv = json.loads((ROOT / ZV).read_text())
    pats = old.patterns(6)
    pat_lookup = {r: i for i, r in enumerate(pats)}

    accepted = 0
    for i, row in enumerate(pats):
        fixed = dict(zip(CYCLE, row))
        if any(all((fixed | {0: a, 1: b})[u] != (fixed | {0: a, 1: b})[v]
                   for u, v in INNER_EDGES)
               for a, b in product(COLORS, repeat=2)):
            accepted |= 1 << i
    fixed = old.obstruction(6, accepted)
    residual = fixed['residual_mask']
    assert accepted == 4969575 and residual == 2075405200
    d16_set = {pats[i] for i in range(len(pats)) if (residual >> i) & 1}

    # Verify Control A: RADIAL-MINDEG5-14
    emb14 = verify_sphere_and_disk_embedding(14, RADIAL14_H_EDGES, RADIAL14_G_FACES)
    assert emb14['beta1_h_minus_c0'] == 1
    assert all(d >= 5 for d in emb14['core_degrees_in_g'].values())
    cols_h14 = enumerate_colorings(tuple(range(2, 14)), RADIAL14_H_EDGES)
    cols_g14 = enumerate_colorings(tuple(range(0, 14)), CENTER_ONLY_EDGES + RADIAL14_H_EDGES)
    p14 = evaluate_property_p_on_graph(14, RADIAL14_H_EDGES, cols_h14)
    assert p14['trapped_antecedent_hits'] == 96 and p14['p_violations'] == 0
    buckets14 = verify_three_step_buckets_and_writeback(14, RADIAL14_H_EDGES, cols_h14, cols_g14)
    c_pos14 = tuple(u - 2 for u in CYCLE)
    rh14_mask = 0
    for c in cols_h14:
        rh14_mask |= 1 << pat_lookup[old.normalize(tuple(c[p] for p in c_pos14))]
    assert rh14_mask == (1 << 31) - 1
    assert RADIAL14_WITNESS_H in set(cols_h14)

    # Verify Control B: THETA-VIOLATOR-12 (beta_1 = 2 sharp boundary witness)
    emb12 = verify_sphere_and_disk_embedding(12, THETA12_H_EDGES, THETA12_G_FACES)
    assert emb12['beta1_h_minus_c0'] == 2
    cols_h12 = enumerate_colorings(tuple(range(2, 12)), THETA12_H_EDGES)
    cols_g12 = enumerate_colorings(tuple(range(0, 12)), CENTER_ONLY_EDGES + THETA12_H_EDGES)
    p12 = evaluate_property_p_on_graph(12, THETA12_H_EDGES, cols_h12)
    assert p12['trapped_antecedent_hits'] == 24 and p12['p_violations'] == 24
    assert THETA12_WITNESS_H in set(cols_h12)

    # Verify Control C: BUFFER-2STEP-19 (beta_1 = 3 full 2-step local survivor)
    emb19 = verify_sphere_and_disk_embedding(19, BUFFER19_H_EDGES, BUFFER19_G_FACES)
    assert emb19['beta1_h_minus_c0'] == 3
    buf19_check = verify_2step_buffer_witness(19, BUFFER19_H_EDGES, BUFFER19_WITNESS_H, d16_set)
    cols_g19 = enumerate_colorings(tuple(range(0, 19)), CENTER_ONLY_EDGES + BUFFER19_H_EDGES)
    assert len(cols_g19) == 64032

    result = dict(
        claim=(
            'Cross-split trapped-swap no-dual-reversal property P holds on all planar '
            'C0-exteriors H with beta_1(H - V(C0)) <= 1, is preserved under exact join, '
            '(x1, x2, z) projection with complete/empty witness fibres, and delayed '
            'writeback, and universally excludes PAIR-C0-D16 (and all non-empty subsets '
            'of Pat(C0) \\ A). General beta_1 >= 2 exteriors, coloring existence, and 4CT '
            'remain OPEN.'
        ),
        contract=dict(
            original_cycle=list(CYCLE),
            cycle_vertex_names=list(CYCLE_NAMES),
            center_vertices=[0, 1],
            inner_edges=[list(e) for e in INNER_EDGES],
            covered_source_class=dict(
                name='S_rad',
                definition=(
                    'Finite simple planar graphs G with fixed sphere/plane embedding '
                    'containing the 8-triangle inner disk (C0, x1, x2) with full-graph '
                    'neighborhoods N_G(x1)={x2,z,a,b,w} and N_G(x2)={x1,z,c,d,w}, '
                    'whose exterior H = G - {x1, x2} on the closed disk Omega (boundary C0) '
                    'satisfies beta_1(H - V(C0)) <= 1 (forest-or-unicyclic exterior outside C0).'
                ),
            ),
            property_P=dict(
                name='P-TRAPPED-SWAP-NO-DUAL-REVERSAL',
                boundary_template='(z, a, b, w, c, d) = (c0, c1, c2, c1, c2, c1)',
                premise_split='(c0 c1 | c2 c3): b~c in Pi_{c2,c3}^H(f) and K_{c0,c1}^H(f; w) cap V(C0) = {w}',
                exact_swap="f' = swap_{c0,c1}(f, K_{c0,c1}^H(f; w)) in Col_4(H)",
                forbidden_conjunction_in_second_split=(
                    '(c0 c2 | c1 c3): [z~{b,c} in f] AND [z!~{b,c} in f\'] '
                    'AND [a!~d in f] AND [a~d in f\']'
                ),
            ),
        ),
        old_and_b6_baseline=dict(
            patterns=[list(p) for p in pats],
            accepted_mask=accepted,
            initial_mask=((1 << len(pats)) - 1) ^ accepted,
            removed_masks=[r['removed_mask'] for r in fixed['rounds']],
            residual_mask=residual,
            d_minimality=check_d_minimality(residual),
            b6_signed_matching_cone=build_b6_certificate(pats, residual),
        ),
        auxiliary_1step_exit_bounds=build_auxiliary_exit_bounds(pats, residual),
        universal_exclusion_of_d16=verify_universal_p_exclusion(pats, residual),
        three_step_preservation_and_controls=dict(
            radial_mindeg5_14=dict(
                embedding=emb14,
                property_P=p14,
                three_step_pipeline=buckets14,
                full_g_colorings=len(cols_g14),
                exterior_realized_patterns_mask=rh14_mask,
                explicit_1step_d16_survivor_h=list(RADIAL14_WITNESS_H),
            ),
            theta_violator_12=dict(
                embedding=emb12,
                property_P=p12,
                full_g_colorings=len(cols_g12),
                explicit_violating_h_coloring=list(THETA12_WITNESS_H),
            ),
            buffer_2step_19=dict(
                embedding=emb19,
                level2_buffer_certificate=buf19_check,
                full_g_colorings=len(cols_g19),
                sample_full_g_coloring=list(cols_g19[0]),
            ),
            retained=verify_retained_controls(prior, zv),
        ),
    )

    args.out_dir.mkdir(parents=True, exist_ok=False)
    out_path = args.out_dir / 'results.json'
    out_path.write_text(json.dumps(result, separators=(',', ':'), sort_keys=True) + '\n')

    inputs = [
        PRIOR,
        ZV,
        'scripts/ck_kempe_obstruction.py',
        'scripts/four_color_counts_cone_verification.py',
        'scripts/four_color_three_step_cross_split_exclusion.py',
        'scripts/four_color_three_step_cross_split_replay.py',
    ]
    manifest = dict(
        baseline=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        sources={p: digest(ROOT / p) for p in inputs},
        outputs={'results.json': digest(out_path)},
    )
    (args.out_dir / 'verification.json').write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + '\n'
    )
    print(json.dumps(dict(
        candidate='PAIR-C0-D16',
        residual_mask=residual,
        d_minimal_subsets=1,
        b6_active_signatures=27,
        admissible_annotations_under_P=0,
        radial14_h_colorings=len(cols_h14),
        radial14_trapped_hits=p14['trapped_antecedent_hits'],
        radial14_p_violations=p14['p_violations'],
        theta12_p_violations=p12['p_violations'],
        buffer19_level2_failures=0,
        results_bytes=out_path.stat().st_size,
    )))


if __name__ == '__main__':
    main()
