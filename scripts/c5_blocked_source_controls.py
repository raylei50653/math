#!/usr/bin/env python3
"""Fixed-source controls for five-step returns; no graph-catalogue expansion.

The Errera source and its five degree-preserving diagonal flips are exact
controls. A complete Kempe space is retained modulo one common S4 action;
all literal lifts and all global permutations are accounted for explicitly.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_ab_swap_cube import ERRERA, NEW_TO_OLD, FACES, orient_and_verify
from c5_adjacent_singleton_counts import REPS
from c5_kempe_connectivity import adjacency, component, pair_components, swap

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'audits/2026-10-29-kempe-realizability/source/controls.json'
STEPS = (((0, 3), 2), ((1, 3), 4), ((1, 2), 1), ((0, 2), 3), ((0, 3), 0))
BOUNDARIES = ((0, 1, 3, 2, 3), (0, 1, 3, 2, 1), (0, 2, 3, 2, 1),
              (0, 2, 3, 0, 1), (3, 2, 3, 0, 1))
ALIGN = (2, 3, 1, 0)


def normalized(c):
    labels = {}
    for x in c:
        if x not in labels:
            labels[x] = len(labels)
    for x in range(4):
        if x not in labels:
            labels[x] = len(labels)
    return tuple(labels[x] for x in c), tuple(labels[x] for x in range(4))


def enumerate_colors(adj):
    n = len(adj)
    order = sorted(range(5, n), key=lambda v: (-len(adj[v]), v))
    answer = []
    for b in REPS:
        c = list(b) + [-1] * (n - 5)
        def visit(depth):
            if depth == len(order):
                answer.append(tuple(c))
                return
            v = order[depth]
            for color in range(4):
                if all(c[w] != color for w in adj[v]):
                    c[v] = color
                    visit(depth + 1)
            c[v] = -1
        visit(0)
    return sorted(answer)


def topology(edges, faces):
    adj = adjacency(17, edges)
    assert min(map(len, adj)) == 5
    ef = defaultdict(list)
    directed = []
    for j, f in enumerate(faces):
        for i in range(3):
            arc = (f[i], f[(i + 1) % 3])
            directed.append(arc)
            ef[tuple(sorted(arc))].append(j)
    assert len(directed) == len(set(directed))
    assert all((v, u) in directed for u, v in directed)
    assert set(ef) == set(edges) and all(len(x) == 2 for x in ef.values())
    assert 17 - len(edges) + len(faces) == 2
    rows = []
    for root in range(17):
        def visit(path):
            u = path[-1]
            if len(path) >= 3 and root in adj[u] and path[1] < path[-1]:
                size = len(path)
                cut = {tuple(sorted((path[i], path[(i + 1) % size]))) for i in range(size)}
                unseen = set(range(len(faces)))
                sides = []
                while unseen:
                    start = min(unseen)
                    unseen.remove(start)
                    queue = [start]
                    for j in queue:
                        f = faces[j]
                        for i in range(3):
                            edge = tuple(sorted((f[i], f[(i + 1) % 3])))
                            if edge not in cut:
                                for k in ef[edge]:
                                    if k in unseen:
                                        unseen.remove(k)
                                        queue.append(k)
                    sides.append(sorted({v for j in queue for v in faces[j]} - set(path)))
                assert len(sides) == 2
                sides.sort(key=lambda x: (len(x), x))
                rows.append(dict(cycle=path, sides=sides))
            if len(path) == 5:
                return
            for v in sorted(adj[u]):
                if v > root and v not in path:
                    visit(path + [v])
        visit([root])
    bad34 = [r for r in rows if len(r['cycle']) <= 4 and r['sides'][0]]
    bad5 = [r for r in rows if len(r['cycle']) == 5 and len(r['sides'][0]) >= 2]
    assert not bad34
    return dict(degrees=list(map(len, adj)), cycles=rows, separating_34=bad34,
                separating_5_two_each_side=bad5,
                satisfies_structural_class=not bool(bad5))


def inspect(name, edges, raw_faces, mutation):
    oe = [e for e in edges if 16 not in e]
    of = [f for f in raw_faces if 16 not in f]
    disk_faces = orient_and_verify(16, oe, of)
    faces = disk_faces + [(i, 16, (i + 1) % 5) for i in range(5)]
    geo = topology(edges, faces)
    adj = adjacency(16, oe)
    colors = enumerate_colors(adj)
    ids = {c: j for j, c in enumerate(colors)}
    transitions = []
    for c in colors:
        actions = []
        for pair in combinations(range(4), 2):
            for s in sorted(pair_components(adj, c, pair), key=lambda s: min(s)):
                raw = swap(c, s, pair)
                assert all(raw[u] != raw[v] for u, v in oe)
                target, align = normalized(raw)
                assert target in ids
                actions.append(dict(pair=pair, component=sorted(s),
                                    target=ids[target], global_alignment=align))
        transitions.append(actions)
    unseen = set(range(len(colors)))
    classes = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue = [start]
        for j in queue:
            for action in transitions[j]:
                k = action['target']
                if k in unseen:
                    unseen.remove(k)
                    queue.append(k)
        extending = [j for j in queue if len(set(colors[j][:5])) == 3]
        classes.append(dict(states=sorted(queue), extending_states=extending,
                            normalized_size=len(queue), literal_size=24 * len(queue),
                            blocked=not bool(extending)))
    h, returns, fails = {}, [], []
    for c in colors:
        if c[:5] != (0, 1, 0, 2, 3):
            continue
        q, moves = c, []
        for j, ((pair, root), expected) in enumerate(zip(STEPS, BOUNDARIES)):
            s = component(adj, q, pair, root)
            q = swap(q, s, pair)
            assert all(q[u] != q[v] for u, v in oe)
            moves.append(dict(pair=pair, root=root, component=sorted(s), coloring=q))
            if q[:5] != expected:
                fails.append(dict(state=ids[c], first_failure=j + 1, moves=moves))
                break
        else:
            q = tuple(ALIGN[x] for x in q)
            assert q in ids and q[:5] == c[:5]
            h[ids[c]] = ids[q]
            returns.append(dict(source=ids[c], target=ids[q], moves=moves,
                                global_alignment=ALIGN))
    cycles, seen = [], set()
    for start in sorted(h):
        path, local, q = [], {}, start
        while q in h and q not in local and q not in seen:
            local[q] = len(path)
            path.append(q)
            q = h[q]
        if q in local:
            cyc = path[local[q]:]
            cycles.append(cyc)
        seen.update(path)
    escapes = []
    for cyc in cycles:
        start = cyc[0]
        previous = {start: None}
        via, queue = {}, deque([start])
        while queue:
            j = queue.popleft()
            if len(set(colors[j][:5])) == 3:
                end, route = j, []
                while previous[j] is not None:
                    route.append(dict(source=previous[j], **via[j]))
                    j = previous[j]
                escapes.append(dict(source=start, target=end,
                                    shortest_quotient_steps=len(route), moves=route[::-1]))
                break
            for action in transitions[j]:
                k = action['target']
                if k not in previous:
                    previous[k] = j
                    via[k] = action
                    queue.append(k)
    assert not any(k['blocked'] for k in classes)
    return dict(name=name, mutation=mutation, original_edges=edges, sphere_faces=faces,
                deleted_vertex=16, boundary=list(range(5)), exterior_edges=oe,
                topology=geo, normalized_colorings=colors, actions=transitions,
                classes=classes, H_returns=returns, H_failures=fails,
                H_cycles=cycles, escapes=escapes)


def report():
    index = {old: new for new, old in enumerate(NEW_TO_OLD)}
    index[0] = 16
    edges = sorted(tuple(sorted((index[u], index[v]))) for u, vs in ERRERA.items() for v in vs)
    disk = [e for e in edges if 16 not in e]
    faces = orient_and_verify(16, disk, FACES) + [(i, 16, (i + 1) % 5) for i in range(5)]
    adj = adjacency(17, edges)
    controls = [inspect('ERRERA-RETURN4-S34', edges, faces, None)]
    for u, v in edges:
        if len(adj[u]) < 6 or len(adj[v]) < 6:
            continue
        selected = [j for j, f in enumerate(faces) if u in f and v in f]
        assert len(selected) == 2
        x, y = [next(w for w in faces[j] if w not in (u, v)) for j in selected]
        assert tuple(sorted((x, y))) not in edges
        changed = sorted((set(edges) - {(u, v)}) | {tuple(sorted((x, y)))})
        changed_faces = [f for j, f in enumerate(faces) if j not in selected] + [(x, y, u), (y, x, v)]
        controls.append(inspect(f'ERRERA-FLIP-{u}-{v}-S5', changed, changed_faces,
                                dict(remove=(u, v), add=(x, y))))
    assert len(controls) == 6
    assert [len(c['normalized_colorings']) for c in controls] == [100, 68, 68, 68, 68, 68]
    assert list(map(len, controls[0]['H_cycles'])) == [4]
    assert len(controls[0]['topology']['separating_5_two_each_side']) == 1
    assert all(c['topology']['satisfies_structural_class'] and not c['H_cycles'] for c in controls[1:])
    files = [Path(__file__), ROOT / 'scripts/c5_ab_swap_cube.py',
             ROOT / 'scripts/c5_kempe_connectivity.py', ROOT / 'scripts/c5_adjacent_singleton_counts.py']
    return dict(schema='c5-fixed-source-return-controls-v1',
                trust='Exact finite controls, paper disk/sphere interpretation. No universal classification, no blocked component counterexample, no Lean theorem.',
                S4_contract='Every proper C5 coloring uses at least three colors, so the S4 action is free. Each stored state has exactly 24 literal lifts. Every global permutation is reachable by swapping every component of each generating color transposition. Thus quotient classes lift to the complete literal Kempe classes.',
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files},
                controls=controls)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', nargs='?', const=str(DEFAULT))
    p.add_argument('--output', default=str(DEFAULT))
    args = p.parse_args()
    result = report()
    encoded = json.dumps(result, indent=2) + '\n'
    if args.check:
        assert Path(args.check).read_text() == encoded, 'Certificate differs'
    else:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('x') as f:
            f.write(encoded)
    print(json.dumps(dict(status='CHECK OK' if args.check else 'CREATED',
                         controls=[dict(name=c['name'], normalized_states=len(c['normalized_colorings']),
                                        literal_states=24 * len(c['normalized_colorings']),
                                        legal=c['topology']['satisfies_structural_class'],
                                        H_cycle_lengths=list(map(len, c['H_cycles'])),
                                        Kempe_classes=len(c['classes'])) for c in result['controls']]), sort_keys=True))


if __name__ == '__main__':
    main()
