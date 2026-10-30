#!/usr/bin/env python3
"""Exact finite Kempe escape controls, retaining remote components and full lifts.

Produces the complete S4 quotient of the actual single-component exchange graph
on two named original exteriors, plus literal shortest escape paths. This is a
finite control audit; it does not establish general D16 exclusion. Replay uses
an independently ordered coloring enumerator and union-find components.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CYCLE = (2, 3, 4, 7, 5, 6)
PAIRS = tuple(combinations(range(4), 2))
D16 = frozenset(tuple(map(int, s)) for s in (
    '010201', '010212', '010213', '010231', '012012', '012021', '012102', '012121',
    '012123', '012132', '012301', '012302', '012312', '012313', '012321', '012323',
))
INNER = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 7),
         (1, 2), (1, 5), (1, 6), (1, 7))


def normalize(word):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in word)


def boundary(col):
    return tuple(col[v - 2] for v in CYCLE)


def accepted(col):
    assign = {v: col[v - 2] for v in CYCLE}
    return [(a, b) for a in range(4) for b in range(4)
            if all((assign | {0: a, 1: b})[u] != (assign | {0: a, 1: b})[v]
                   for u, v in INNER)]


def adjacency(n, edges):
    out = [[] for _ in range(n)]
    for u, v in edges:
        out[u - 2].append(v - 2)
        out[v - 2].append(u - 2)
    return out


def enumerate_normalized(n, edges):
    prev = [[] for _ in range(n)]
    for u, v in edges:
        prev[max(u, v) - 2].append(min(u, v) - 2)
    col = [0] * n
    result = []

    def visit(i, maximum):
        if i == n:
            result.append(tuple(col))
            return
        used = {col[j] for j in prev[i]}
        for c in range(min(3, maximum + 1) + 1):
            if c not in used:
                col[i] = c
                visit(i + 1, max(maximum, c))

    visit(0, -1)
    return result


def components(col, adj):
    out = []
    for a, b in PAIRS:
        unseen = {v for v, c in enumerate(col) if c in (a, b)}
        blocks = []
        while unseen:
            start = min(unseen)
            queue = [start]
            unseen.remove(start)
            for u in queue:
                for v in adj[u]:
                    if v in unseen:
                        unseen.remove(v)
                        queue.append(v)
            blocks.append(tuple(sorted(queue)))
        out.append(tuple(blocks))
    return tuple(out)


def swapped(col, pair, block):
    out = list(col)
    for v in block:
        out[v] = sum(pair) - out[v]
    return tuple(out)


def distances(transitions, states, boundary_only=False):
    graph = [set() for _ in states]
    boundary_mask = sum(1 << (v - 2) for v in CYCLE)
    for i, actions in enumerate(transitions):
        for _, mask, j in actions:
            if not boundary_only or mask & boundary_mask:
                graph[i].add(j)
    dist = {i: 0 for i, c in enumerate(states) if normalize(boundary(c)) not in D16}
    queue = deque(dist)
    while queue:
        i = queue.popleft()
        for j in graph[i]:
            if j not in dist:
                dist[j] = dist[i] + 1
                queue.append(j)
    sizes = []
    unseen = set(range(len(states)))
    while unseen:
        r = min(unseen)
        unseen.remove(r)
        queue = [r]
        for i in queue:
            for j in graph[i]:
                if j in unseen:
                    unseen.remove(j)
                    queue.append(j)
        sizes.append(len(queue))
    bad = [i for i, c in enumerate(states) if normalize(boundary(c)) in D16]
    histogram = Counter(dist.get(i, 'unreachable') for i in bad)
    return dist, dict(
        connected_component_sizes=sorted(sizes),
        d16_state_orbits=len(bad),
        distance_to_escape_histogram={str(k): v for k, v in sorted(histogram.items(), key=lambda x: str(x[0]))},
        d16_closed_state_orbits=sum(i not in dist for i in bad),
    )


def literal_shortest_path(initial, adj, boundary_only=False):
    seen = {initial: None}
    queue = deque([initial])
    boundary_points = {v - 2 for v in CYCLE}
    while queue:
        col = queue.popleft()
        if normalize(boundary(col)) not in D16:
            end = col
            break
        for p, blocks in enumerate(components(col, adj)):
            for block in blocks:
                if boundary_only and not boundary_points.intersection(block):
                    continue
                target = swapped(col, PAIRS[p], block)
                if target not in seen:
                    seen[target] = (col, p, block)
                    queue.append(target)
    else:
        return None
    path = []
    while seen[end] is not None:
        col, p, block = seen[end]
        path.append(dict(
            source=list(col),
            source_boundary=list(boundary(col)),
            pair=list(PAIRS[p]),
            component_vertices=[v + 2 for v in block],
            hits_boundary=bool(boundary_points.intersection(block)),
            target=list(end),
            target_boundary=list(boundary(end)),
            source_all_six_components=[[[v + 2 for v in b] for b in blocks]
                                       for blocks in components(col, adj)],
            target_all_six_components=[[[v + 2 for v in b] for b in blocks]
                                       for blocks in components(end, adj)],
        ))
        end = col
    path.reverse()
    final = tuple(path[-1]['target']) if path else initial
    return dict(steps=len(path), path=path, final_center_fibre=accepted(final),
                literal_states_discovered=len(seen))


def build_control(name, edges, initial):
    n = len(initial)
    states = enumerate_normalized(n, edges)
    lookup = {c: i for i, c in enumerate(states)}
    adj = adjacency(n, edges)
    actions = []
    for col in states:
        row = []
        for p, blocks in enumerate(components(col, adj)):
            for block in blocks:
                target = normalize(swapped(col, PAIRS[p], block))
                row.append([p, sum(1 << v for v in block), lookup[target]])
        actions.append(row)
    d_all, summary = distances(actions, states)
    d_boundary, boundary_summary = distances(actions, states, True)
    full_path = literal_shortest_path(initial, adj)
    boundary_path = literal_shortest_path(initial, adj, True)
    initial_idx = lookup[normalize(initial)]
    assert full_path['steps'] == d_all[initial_idx]
    assert boundary_path['steps'] == d_boundary[initial_idx]
    assert full_path['final_center_fibre'] and boundary_path['final_center_fibre']
    # At least three used colors makes every whole-coloring S4 orbit size 24.
    assert all(len(set(c)) >= 3 for c in states)
    return dict(
        name=name, ordered_vertices=list(range(2, n + 2)), edges=[list(e) for e in edges],
        initial_coloring=list(initial), full_normalized_colorings=[list(c) for c in states],
        # For state i: [pair-index, component vertex bitmask using vertex v -> bit v-2, target-state-index].
        all_single_component_transitions=actions,
        quotient_states=len(states), literal_colorings=24 * len(states),
        all_component_summary=summary, boundary_component_summary=boundary_summary,
        shortest_literal_escape=full_path, shortest_boundary_only_escape=boundary_path,
        retained_original_boundary=list(CYCLE),
        complete_coloring_sha256=sha256(json.dumps(states, separators=(',', ':')).encode()).hexdigest(),
        transition_sha256=sha256(json.dumps(actions, separators=(',', ':')).encode()).hexdigest(),
    )


# Replay deliberately uses a different coloring order and component algorithm.
def replay_enumerate(n, edges):
    adj = adjacency(n, edges)
    assigned = {0: 0, 1: 1}  # Original edge (z,a)=(2,3); full remaining colors kept.
    out = set()
    leaves = 0

    def visit():
        nonlocal leaves
        if len(assigned) == n:
            out.add(normalize(tuple(assigned[i] for i in range(n))))
            leaves += 1
            return
        u = max((i for i in range(n) if i not in assigned),
                key=lambda i: (len({assigned[j] for j in adj[i] if j in assigned}), len(adj[i]), -i))
        used = {assigned[j] for j in adj[u] if j in assigned}
        for c in range(4):
            if c not in used:
                assigned[u] = c
                visit()
                del assigned[u]

    visit()
    # Stabilizer of an ordered distinct-color edge has size two; no coloring
    # uses fewer than three colors here, so each canonical orbit has two leaves.
    assert leaves == 2 * len(out)
    return sorted(out)


def replay_components(col, edges):
    out = []
    for pair in PAIRS:
        parent = {i: i for i, c in enumerate(col) if c in pair}

        def root(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v

        for u, v in edges:
            a, b = u - 2, v - 2
            if a in parent and b in parent:
                parent[root(a)] = root(b)
        groups = {}
        for u in sorted(parent):
            groups.setdefault(root(u), []).append(u)
        out.append(tuple(sorted(tuple(b) for b in groups.values())))
    return tuple(out)


def replay(data):
    checked = []
    for rec in data['controls']:
        states = [tuple(c) for c in rec['full_normalized_colorings']]
        edges = [tuple(e) for e in rec['edges']]
        n = len(rec['ordered_vertices'])
        assert states == replay_enumerate(n, edges)
        lookup = {c: i for i, c in enumerate(states)}
        expected = []
        for col in states:
            row = []
            for p, blocks in enumerate(replay_components(col, edges)):
                for block in blocks:
                    target = list(col)
                    for u in block:
                        target[u] = PAIRS[p][col[u] == PAIRS[p][0]]
                    target = normalize(target)
                    row.append([p, sum(1 << u for u in block), lookup[target]])
            expected.append(row)
        assert expected == rec['all_single_component_transitions']
        dist, summary = distances(expected, states)
        bdist, bsummary = distances(expected, states, True)
        assert summary == rec['all_component_summary']
        assert bsummary == rec['boundary_component_summary']
        for key, distances_by_state in [('shortest_literal_escape', dist), ('shortest_boundary_only_escape', bdist)]:
            cert = rec[key]
            current = tuple(rec['initial_coloring'])
            assert cert['steps'] == distances_by_state[lookup[normalize(current)]]
            for step in cert['path']:
                assert tuple(step['source']) == current
                p = PAIRS.index(tuple(step['pair']))
                block = tuple(v - 2 for v in step['component_vertices'])
                blocks = replay_components(current, edges)
                assert block in blocks[p]
                assert step['source_all_six_components'] == [
                    [[v + 2 for v in b] for b in part] for part in blocks]
                result = tuple(sum(PAIRS[p]) - c if i in block else c for i, c in enumerate(current))
                assert result == tuple(step['target'])
                assert all(result[u - 2] != result[v - 2] for u, v in edges)
                assert step['target_all_six_components'] == [
                    [[v + 2 for v in b] for b in part] for part in replay_components(result, edges)]
                if key == 'shortest_boundary_only_escape':
                    assert set(step['component_vertices']) & set(CYCLE)
                current = result
            assert normalize(boundary(current)) not in D16
            assert [list(x) for x in accepted(current)] == cert['final_center_fibre']
            assert cert['final_center_fibre']
        checked.append(dict(name=rec['name'], quotient_states=len(states),
                            exact_single_component_transitions=sum(map(len, expected)),
                            all_components_recomputed=True, no_d16_closed_class=summary['d16_closed_state_orbits'] == 0,
                            shortest_escape=rec['shortest_literal_escape']['steps'],
                            boundary_only_shortest_escape=rec['shortest_boundary_only_escape']['steps']))
    return dict(passed=True, independent_coloring_order='DSATUR with ordered edge fixed to (0,1)',
                independent_component_algorithm='union-find', controls=checked,
                scope='Finite named original graphs only; general D16 exclusion remains OPEN.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path)
    parser.add_argument('--replay', type=Path)
    args = parser.parse_args()
    if args.replay:
        print(json.dumps(replay(json.loads(args.replay.read_text())), indent=2))
        return
    if args.out_dir is None:
        parser.error('--out-dir or --replay is required')
    # Only the producer imports named constants; replay has no repository imports.
    import four_color_three_step_cross_split_exclusion as prior
    args.out_dir.mkdir(parents=True, exist_ok=False)
    recs = [build_control('THETA-VIOLATOR-12', prior.THETA12_H_EDGES, prior.THETA12_WITNESS_H),
            build_control('BUFFER-2STEP-19', prior.BUFFER19_H_EDGES, prior.BUFFER19_WITNESS_H)]
    data = dict(
        schema='three-step-kempe-escape-v1', color_pair_order=[list(p) for p in PAIRS],
        original_cycle=list(CYCLE), d16_patterns=[list(p) for p in sorted(D16)],
        quotient_contract='One common S4 action on each entire original-vertex coloring; no separate boundary/lift permutation.',
        scope='Finite named original graphs only; general D16 exclusion remains OPEN.', controls=recs,
    )
    (args.out_dir / 'results.json').write_text(json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n')
    manifest = {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in (
        'scripts/four_color_three_step_kempe_escape.py',
        'scripts/four_color_three_step_cross_split_exclusion.py',)}
    manifest['results.json'] = sha256((args.out_dir / 'results.json').read_bytes()).hexdigest()
    (args.out_dir / 'verification.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(controls=[dict(name=r['name'], quotient_states=r['quotient_states'],
                        summary=r['all_component_summary'], shortest_escape=r['shortest_literal_escape']['steps'],
                        boundary_only_escape=r['shortest_boundary_only_escape']['steps']) for r in recs]), indent=2))


if __name__ == '__main__':
    main()
