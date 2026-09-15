#!/usr/bin/env python3
"""Exact strategy comparison on the fixed survivor-811; no summary quotient."""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

from c5_behavior_refinement import ROOT, SOURCE
from c5_edge_choices import EdgeModel
from c5_kempe_connectivity import PAIRS, pair_components, swap
from c5_complementary_cube import singleton_of

OUT = ROOT / 'artifacts/c5_cells/strategy_safe.json'
RADIUS = ROOT / 'artifacts/c5_cells/behavior_radius2.json'


def solve(rows, goals, allowed, safe):
    """Reverse BFS, with a rank and selected edge for every winning state."""
    reverse = [[] for _ in rows]
    for s, edges in enumerate(rows):
        if safe(s):
            for a, edge in enumerate(edges):
                t = edge['target']
                if safe(t) and allowed(s, edge):
                    reverse[t].append((s, a))
    rank, policy = [None] * len(rows), [None] * len(rows)
    queue = deque()
    for s in sorted(goals):
        if safe(s):
            rank[s] = 0
            queue.append(s)
    while queue:
        t = queue.popleft()
        for s, a in reverse[t]:
            if rank[s] is None:
                rank[s], policy[s] = rank[t] + 1, a
                queue.append(s)
    # Certificate obligations: winning ranks descend; losing safe states are
    # goal-free and closed under every permitted safe transition.
    for s, edges in enumerate(rows):
        if rank[s] is not None:
            if rank[s] == 0:
                assert s in goals and safe(s)
            else:
                edge = edges[policy[s]]
                assert safe(s) and safe(edge['target']) and allowed(s, edge)
                assert rank[edge['target']] == rank[s] - 1
        elif safe(s):
            assert s not in goals
            assert all(rank[e['target']] is None for e in edges
                       if safe(e['target']) and allowed(s, e))
    return dict(rank=rank, policy=policy)


def route(rows, solution, start):
    if solution['rank'][start] is None:
        return None
    events, s = [], start
    while solution['rank'][s]:
        edge = rows[s][solution['policy'][s]]
        events.append(dict(source=s, **edge))
        s = edge['target']
    return dict(start=start, events=events, goal=s)


def report():
    source = json.loads(SOURCE.read_text())
    radius = json.loads(RADIUS.read_text())
    assert radius['graph'] == source['graph']
    for artifact in (source, radius):
        for path, digest in artifact['hashes'].items():
            assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    model = EdgeModel(source['graph'])
    seeds = [tuple(w['source']) for w in source['witnesses']]
    # Enumerate the FULL component-swap closure, including interior components.
    states = list(dict.fromkeys(seeds))
    index = {c: i for i, c in enumerate(states)}
    rows = []
    graph = nx.Graph()
    graph.add_nodes_from(range(model.n))
    graph.add_edges_from(model.edges)
    for c in states:
        model.validate(c)
        edges = []
        for pair in PAIRS:
            blocks = sorted(map(sorted, pair_components(model.adj, c, pair)))
            independent = sorted(map(sorted, nx.connected_components(
                graph.subgraph(v for v in graph if c[v] in pair))))
            assert blocks == independent
            for block in blocks:
                d = swap(c, block, pair)
                independent_d = tuple(pair[1] if v in block and color == pair[0]
                    else pair[0] if v in block else color for v, color in enumerate(c))
                assert d == independent_d
                if d not in index:
                    index[d] = len(states)
                    states.append(d)
                    if len(states) > 100000:
                        raise RuntimeError('Incomplete closure: cap exceeded; no certificate written.')
                edges.append(dict(pair=pair, component=block, target=index[d],
                                  boundary_roots=[v for v in block if v < 5]))
        rows.append(edges)
    assert len(rows) == len(states)
    # Independent dual graph component count; no call to Dual.systems here.
    chi, cycle_vectors = [], []
    for c in states:
        vector = []
        types = [c[u] ^ c[v] for u, v in model.edges]
        for pair in ((1, 2), (1, 3), (2, 3)):
            dual = nx.Graph()
            dual.add_edges_from(ends for ends, typ in zip(model.dual.ends, types) if typ in pair)
            vector.append(sum(all(v < model.dual.f for v in block)
                              for block in nx.connected_components(dual)))
        expected = [sum(not terminals for terminals, _ in system)
                    for system in model.dual.systems(c)]
        assert vector == expected
        cycle_vectors.append(vector)
        chi.append(sum(vector))
    goals = {i for i, c in enumerate(states) if singleton_of(c) in (1, 3, 4)}
    full = solve(rows, goals, lambda s, e: True, lambda s: True)
    rooted = lambda s, e: bool(e['boundary_roots'])
    boundary = solve(rows, goals, rooted, lambda s: True)
    reachable = {index[c] for c in seeds}
    queue = deque(sorted(reachable))
    while queue:
        for edge in rows[queue.popleft()]:
            t = edge['target']
            if edge['boundary_roots'] and t not in reachable:
                reachable.add(t)
                queue.append(t)
    assert len(reachable) == len(states), 'Boundary-root closure differs from full closure.'
    monotone = solve(rows, goals,
                     lambda s, e: rooted(s, e) and chi[e['target']] <= chi[s],
                     lambda s: True)
    # Cross-check all three unbounded-vertex strategy reachability calculations.
    for solution, allowed in ((full, lambda s, e: True), (boundary, rooted),
            (monotone, lambda s, e: rooted(s, e) and chi[e['target']] <= chi[s])):
        digraph = nx.DiGraph()
        digraph.add_nodes_from(range(len(states) + 1))
        digraph.add_edges_from((s, e['target']) for s, es in enumerate(rows) for e in es
                              if allowed(s, e))
        digraph.add_edges_from((g, len(states)) for g in goals)
        distances = nx.single_source_shortest_path_length(digraph.reverse(), len(states))
        assert solution['rank'] == [distances[i] - 1 if i in distances else None
                                   for i in range(len(states))]
    thresholds, kappa = {}, [None] * len(states)
    for k in range(max(chi) + 1):
        sol = solve(rows, goals, rooted, lambda s: chi[s] <= k)
        # Independent graph-library shortest distances for each threshold.
        digraph = nx.DiGraph()
        digraph.add_nodes_from(i for i in range(len(states)) if chi[i] <= k)
        digraph.add_edges_from((s, e['target']) for s, es in enumerate(rows) for e in es
            if chi[s] <= k and chi[e['target']] <= k and rooted(s, e))
        sentinel = len(states)
        digraph.add_node(sentinel)
        digraph.add_edges_from((g, sentinel) for g in goals if chi[g] <= k)
        distances = nx.single_source_shortest_path_length(digraph.reverse(), sentinel)
        assert sol['rank'] == [distances[i] - 1 if i in distances else None
                               for i in range(len(states))]
        for i, rank in enumerate(sol['rank']):
            if rank is not None and kappa[i] is None:
                kappa[i] = k
        thresholds[str(k)] = sol
    initial = [index[tuple(r['coloring'])] for r in radius['corpus']]
    seed_ids = [index[c] for c in seeds]
    lost = [i for i in range(len(states))
            if boundary['rank'][i] is not None and monotone['rank'][i] is None]
    def counts(ids):
        return dict(states=len(ids), full_win=sum(full['rank'][i] is not None for i in ids),
            boundary_win=sum(boundary['rank'][i] is not None for i in ids),
            monotone_win=sum(monotone['rank'][i] is not None for i in ids),
            needs_above_initial=sum(kappa[i] is not None and kappa[i] > chi[i] for i in ids),
            thresholds={k: dict(initially_safe=sum(chi[i] <= int(k) for i in ids),
                winning=sum(sol['rank'][i] is not None for i in ids),
                safe_but_lost=sum(chi[i] <= int(k) and boundary['rank'][i] is not None
                                 and sol['rank'][i] is None for i in ids))
                for k, sol in thresholds.items()})
    radius_lost = [i for i in initial if monotone['rank'][i] is None
                   and boundary['rank'][i] is not None]
    rebound = [i for i in lost if kappa[i] == chi[i]]
    witness_ids = list(dict.fromkeys(seed_ids + lost[:1] +
        radius_lost[:1] + rebound[:1] +
        [i for i in range(len(states)) if kappa[i] is not None and kappa[i] > chi[i]][:1]))
    witnesses = [dict(state=i, chi=chi[i], kappa=kappa[i],
        unrestricted=route(rows, boundary, i),
        optimal_peak=route(rows, thresholds[str(kappa[i])], i) if kappa[i] is not None else None,
        monotone=route(rows, monotone, i)) for i in witness_ids]
    files = {SOURCE, RADIUS, Path(__file__).resolve(),
             *(ROOT / p for a in (source, radius) for p in a['hashes'])}
    return dict(scope='Fixed survivor-811 full Kempe closure of two seeds; exact raw colors. Python evidence, no Lean or cross-graph theorem.',
        graph=source['graph'], goal='Boundary singleton at position 1, 3, or 4',
        complexity='Sum of cycle counts in the three complementary dual systems',
        states=states, transitions=rows, cycle_vectors=cycle_vectors, chi=chi,
        goals=sorted(goals), seed_ids=seed_ids, initial_radius2=initial,
        full=full, boundary=boundary, monotone=monotone, thresholds=thresholds,
        kappa=kappa, witnesses=witnesses,
        summary=dict(closure=counts(range(len(states))), radius2=counts(initial), seeds=counts(seed_ids),
            transitions=sum(map(len, rows)), cycle_histogram=dict(sorted(Counter(chi).items())),
            boundary_transitions=sum(bool(e['boundary_roots']) for es in rows for e in es),
            monotone_lost=len(lost), rebound_without_higher_peak=len(rebound)),
        hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in sorted(files)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    content = json.dumps(result, sort_keys=True, separators=(',', ':')) + '\n'
    if args.check:
        assert OUT.read_text() == content, 'Certificate differs; inspect before regenerating.'
    else:
        OUT.write_text(content)
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
