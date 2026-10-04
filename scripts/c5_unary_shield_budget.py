#!/usr/bin/env python3
"""Finite controls for the epsilon-free shield budget and the hub principle.

Part A replays the purely topological shield claims on random plane disk
graphs with a fixed outer C5. Part B exhausts small hub wirings of the pure
k-hub lemma (k <= 4) with a networkx planarity test. Part C applies Lemma 2
and Lemma 1(c) to the saved A4 residual U-support records. None of the parts
builds a 933/941 source; the unbounded statements are paper proofs in
docs/c5_unary_shield_budget.md.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_unary_shield_budget/observations.json'
A4 = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04/observations.json'
FRAME = tuple(range(5))
FRAME_EDGES = tuple(tuple(sorted((i, (i + 1) % 5))) for i in range(5))


def edge(a, b):
    assert a != b
    return (a, b) if a < b else (b, a)


# ---------------------------------------------------------------- Part A


def random_disk(rng, interior, flips):
    """Random combinatorial triangulation of the pentagon b0..b4."""
    faces = [(i, (i + 1) % 5, 5) for i in range(5)]
    for v in range(6, 5 + interior):
        a, b, c = faces.pop(rng.randrange(len(faces)))
        faces += [(a, b, v), (b, c, v), (c, a, v)]
    edges = {edge(*e) for f in faces for e in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0]))}
    for _ in range(flips):
        u, v = rng.choice(sorted(edges))
        if (u, v) in FRAME_EDGES:
            continue
        pair = [f for f in faces if u in f and v in f]
        assert len(pair) == 2
        f1, f2 = pair
        x = next(w for w in f1 if w not in (u, v))
        y = next(w for w in f2 if w not in (u, v))
        if edge(x, y) in edges or (x < 5 and y < 5):
            continue
        # Orient: f1 contains u->v in ccw order, f2 contains v->u.
        i = f1.index(u)
        if f1[(i + 1) % 3] != v:
            f1, f2, x, y = f2, f1, y, x
        faces.remove(f1)
        faces.remove(f2)
        faces += [(x, u, y), (y, v, x)]
        edges.remove(edge(u, v))
        edges.add(edge(x, y))
    return edges, faces


def face_frame_edges(faces, k_edges, start):
    """Frame edges on the face of K that contains the non-K vertex start."""
    by_edge = {}
    for i, f in enumerate(faces):
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            by_edge.setdefault(edge(a, b), []).append(i)
    seed = next(i for i, f in enumerate(faces) if start in f)
    seen, todo = {seed}, [seed]
    while todo:
        f = faces[todo.pop()]
        for a, b in ((f[0], f[1]), (f[1], f[2]), (f[2], f[0])):
            e = edge(a, b)
            if e in k_edges:
                continue
            for j in by_edge[e]:
                if j not in seen:
                    seen.add(j)
                    todo.append(j)
    return {e for i in seen for a, b in ((faces[i][0], faces[i][1]),
                                         (faces[i][1], faces[i][2]),
                                         (faces[i][2], faces[i][0]))
            for e in [edge(a, b)] if e in FRAME_EDGES}


def components(vertices, adj):
    left, out = set(vertices), []
    while left:
        start = min(left)
        seen, todo = {start}, [start]
        while todo:
            v = todo.pop()
            for w in adj[v]:
                if w in left and w not in seen:
                    seen.add(w)
                    todo.append(w)
        left -= seen
        out.append(frozenset(seen))
    return out


def closed_gaps(support):
    """Closed frame arcs between cyclically consecutive support points."""
    pts = sorted(support)
    gaps = []
    for i, s in enumerate(pts):
        t = pts[(i + 1) % len(pts)]
        arc = [s]
        while arc[-1] != t:
            arc.append((arc[-1] + 1) % 5)
        gaps.append(tuple(arc))
    return gaps


def max_gap_free(support):
    """Length of the shortest closed arc containing support."""
    return 5 - max(len(g) - 1 for g in closed_gaps(support))


def shield_case(rng, interior, flips, delete_p, root_p):
    edges, faces = random_disk(rng, interior, flips)
    edges = {e for e in edges if e in FRAME_EDGES or rng.random() >= delete_p}
    verts = sorted({v for e in edges for v in e})
    adj = {v: set() for v in verts}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    inner = [v for v in verts if v >= 5]
    comps = components(inner, adj)
    if not comps:
        return None
    hv = max(comps, key=lambda c: (len(c), sorted(c)))
    roots = sorted(v for v in hv if rng.random() < root_p)
    if not roots:
        roots = [min(hv)]
    rest = sorted(hv - set(roots))
    pieces = components(rest, adj)
    stats = Counter()
    shields = []
    for comp in pieces:
        root_nbrs = {w for v in comp for w in adj[v] if w in roots}
        others = hv - comp
        one_sided = len(components(others, adj)) == 1
        kind = 'unary' if len(root_nbrs) == 1 else 'mixed'
        if not one_sided:
            assert kind == 'mixed'
            stats['separating_mixed'] += 1
            continue
        stats[f'one_sided_{kind}'] += 1
        support = {w for v in comp for w in adj[v] if w < 5}
        attach = {w for v in others for w in adj[v] if w < 5}
        k_edges = {e for e in edges if e in FRAME_EDGES or
                   (e[0] in comp or e[1] in comp) and set(e) <= comp | set(FRAME)}
        gap = face_frame_edges(faces, k_edges, min(others))
        shield = set(FRAME_EDGES) - gap
        gap_vertices = {v for e in gap for v in e}
        # Claim (a): the rest of H attaches inside the closed gap arc, and the
        # shield is one closed arc containing the whole support.
        if gap:
            assert attach <= gap_vertices, (sorted(comp), sorted(attach), sorted(gap))
        else:
            assert len(attach) <= 1 and attach <= support
        if shield and gap:
            ends = Counter(v for e in shield for v in e)
            assert sum(1 for c in ends.values() if c == 1) == 2
            assert support <= set(ends), (sorted(support), sorted(shield))
        if len(support) >= 2:
            assert len(shield) >= max(1, max_gap_free(support)), (sorted(support), sorted(shield))
        ambiguous = len([g for g in closed_gaps(support) if attach <= set(g)]) > 1 \
            if len(support) >= 2 and attach else False
        stats['ambiguous_gap'] += ambiguous
        stats['nontrivial_shield' if shield and gap else 'trivial_shield'] += 1
        # Lemma 2: when the interior touches all five frame vertices, the
        # support of a one-sided piece is exactly the vertex set of its shield.
        touched = {w for v in hv for w in adj[v] if w < 5}
        if touched == set(FRAME) and len(support) >= 2:
            span = {v for e in shield for v in e} if gap else set(FRAME)
            assert support == span, (sorted(support), sorted(shield))
            stats['full_touch_interval_support'] += 1
        shields.append((comp, support, attach, shield if gap else set()))
    # Claim (b): shields of distinct one-sided pieces are edge-disjoint.
    for (c1, s1, a1, o1), (c2, s2, a2, o2) in combinations(shields, 2):
        assert s2 <= a1 and s1 <= a2
        assert not (o1 & o2), (sorted(c1), sorted(c2), sorted(o1), sorted(o2))
        if o1 and o2:
            stats['nontrivial_pairs'] += 1
    long_ = sum(1 for *_, o in shields if len(o) >= 2)
    assert long_ <= 2
    stats[f'long_shields_{long_}'] += 1
    return stats


def part_a():
    rng = random.Random(20261004)
    total = Counter()
    cases = 0
    for interior in (4, 6, 9, 13, 18):
        for delete_p in (0.15, 0.3, 0.45):
            for root_p in (0.15, 0.3, 0.5):
                for _ in range(60):
                    stats = shield_case(rng, interior, 3 * interior, delete_p, root_p)
                    if stats is not None:
                        cases += 1
                        total.update(stats)
    return dict(seed=20261004, graphs=cases, counts=dict(sorted(total.items())))


# ---------------------------------------------------------------- Part B


def colorable(n, nbrs, lists):
    order = sorted(range(n), key=lambda v: len(lists[v]))
    color = {}

    def go(i):
        if i == n:
            return True
        v = order[i]
        for c in lists[v]:
            if all(color.get(w) != c for w in nbrs[v]):
                color[v] = c
                if go(i + 1):
                    return True
                del color[v]
        return False

    return go(0)


def part_b(max_n):
    counts = Counter()
    examples = {}
    for g in nx.graph_atlas_g()[1:]:
        n = g.number_of_nodes()
        if n > max_n or not nx.is_connected(g) or max(d for _, d in g.degree()) > 4:
            continue
        nbrs = [sorted(g[v]) for v in range(n)]
        need = [4 - len(nbrs[v]) for v in range(n)]
        for k in range(1, 5):
            if max(need) > k:
                continue
            choices = [list(combinations(range(k), m)) for m in need]
            for wiring in product(*choices):
                lists = [tuple(c for c in range(4) if c not in wiring[v]) for v in range(n)]
                counts[f'k{k}_instances'] += 1
                if colorable(n, nbrs, lists):
                    continue
                counts[f'k{k}_uncolorable'] += 1
                j = nx.Graph(g)
                hubs = [('X', i) for i in range(k)]
                j.add_edges_from(combinations(hubs, 2))
                j.add_edges_from((v, hubs[i]) for v in range(n) for i in wiring[v])
                assert all(j.degree(v) == 4 for v in range(n))
                planar, _ = nx.check_planarity(j)
                assert not planar, (sorted(g.edges()), wiring)
                key = f'k{k}'
                if key not in examples or n < len(examples[key]['wiring']):
                    examples[key] = dict(c_edges=sorted(map(list, g.edges())),
                                         wiring=[list(w) for w in wiring])
    return dict(max_c_vertices=max_n, counts=dict(sorted(counts.items())),
                smallest_uncolorable=dict(sorted(examples.items())))


# ---------------------------------------------------------------- Part C


def interval(support):
    s = set(support)
    return len(s) <= 1 or len(s) == 5 or sum((v - 1) % 5 not in s for v in s) == 1


def interior(support):
    """Interior vertices of the shield arc; none claimed when S_U is all of B."""
    s = set(support)
    if len(s) == 5:
        return set()
    return {v for v in s if (v - 1) % 5 in s and (v + 1) % 5 in s}


def part_c():
    raw = A4.read_bytes()
    data = json.loads(raw)
    targets = []
    for t in data['targets']:
        before, after, reasons, frames = Counter(), Counter(), Counter(), []
        for f in t['complete_remaining_named_original_frames']:
            spokes = set(f['original_a_spokes']) | set(f['original_b_spokes'])
            kept = []
            for pl in f['all_original_U_face_support_placements']:
                for rec in pl['all_actual_original_U_support_subsets']:
                    if rec['status'].startswith('excluded'):
                        continue
                    sup = rec['actual_original_U_support']
                    before['U_support_records'] += 1
                    if not interval(sup):
                        reasons['lemma2_noncontiguous_support'] += 1
                    elif spokes & interior(sup):
                        reasons['lemma1c_spoke_in_shield_interior'] += 1
                    else:
                        after['U_support_records'] += 1
                        kept.append(dict(face=pl['original_U_face'], support=sup))
            for p in f['remaining_named_original_U_placements']:
                sup = p['actual_original_U_support']
                n = len(p['complete_singleton_unary_relation_schedules'])
                before['singleton_schedules'] += n
                if interval(sup) and not spokes & interior(sup):
                    after['singleton_schedules'] += n
            assert kept, f['named_frame_id']
            frames.append(dict(named_frame_id=f['named_frame_id'], spokes=sorted(spokes),
                               kept_U_records=kept))
        targets.append(dict(source_sigma=t['source_sigma'], frames=len(frames),
                            before=dict(before), after=dict(after),
                            pruned_by=dict(sorted(reasons.items())),
                            frames_emptied=0, frame_survivors=frames))
    return dict(input=str(A4.relative_to(ROOT)), input_sha256=sha256(raw).hexdigest(),
                scope='Prunes saved necessary U-support records only; no frame, '
                      'C relation or source realization is claimed.',
                targets=targets)


def build():
    a = part_a()
    b = part_b(7)
    c = part_c()
    summary = dict(part_a_graphs=a['graphs'],
                   part_a_nontrivial_pairs=a['counts'].get('nontrivial_pairs', 0),
                   part_b_uncolorable={k: v for k, v in b['counts'].items()
                                       if k.endswith('uncolorable')},
                   part_c_A4_residual={t['source_sigma']: dict(before=t['before'],
                                                               after=t['after'])
                                       for t in c['targets']})
    return dict(part_a_shields=a, part_b_hubs=b, part_c_a4_residual=c, summary=summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
