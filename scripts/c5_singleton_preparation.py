#!/usr/bin/env python3
"""Neutral reachability limits and singleton preparation on the existing B2."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import networkx as nx

from c5_edge_choices import EdgeModel, Move, ROOT
from c5_edge_states import TYPE_PAIRS
from c5_complementary_cube import singleton_of
from c5_kempe_screen import normalize
from c5_strategy_barriers import quotient
from c5_strategy_safe import solve, route

SOURCE = ROOT / 'artifacts/c5_cells/strategy_safe.json'
BARRIERS = ROOT / 'artifacts/c5_cells/strategy_barriers.json'
LOCAL = ROOT / 'artifacts/c5_cells/local_exit.json'
OUT = ROOT / 'artifacts/c5_cells/singleton_preparation.json'


def success_boundary(c):
    return singleton_of(c) in (1, 3, 4)


def tail_guard(model, c):
    """Predict the finishing component using SOURCE vertex colors only.

    Boundary (A,D,C,A,B). After AB@0, the A/C vertices are exactly W.
    The final AC@4 escapes iff 2 and 4 lie in different components of G[W].
    No target coloring, Goal table, state ID, or cycle vector is consulted.
    """
    A, D, C, A2, B = c[:5]
    assert A == A2 and len({A, B, C, D}) == 4
    first = next(a for a in model.actions(c) if set(a.pair) == {A, B} and 0 in a.component)
    S = set(first.component)
    assert S & set(range(5)) == {0, 3, 4}
    W = {v for v, color in enumerate(c)
         if color == C or (color == A and v not in S) or (color == B and v in S)}
    graph = nx.Graph()
    graph.add_nodes_from(W)
    graph.add_edges_from((u, v) for u, v in model.edges if u in W and v in W)
    blocks = sorted(map(sorted, nx.connected_components(graph)))
    assert 2 in W and 4 in W
    separated = not nx.has_path(graph, 2, 4)
    return dict(role_colors=[A, B, C, D], first_pair=sorted((A, B)),
                first_component=list(first.component), predicted_AC_vertices=sorted(W),
                predicted_AC_components=blocks, separated=separated)


def structural_tail(model, initial):
    """Two-branch recipe; guards use connectivity, not certificate IDs."""
    c, moves, guards = initial, [], []
    def step(pair, root):
        nonlocal c
        a = next(a for a in model.actions(c) if set(a.pair) == set(pair) and root in a.component)
        moves.append(a)
        c = model.apply(c, a)
    guard = tail_guard(model, c)
    guards.append(guard)
    prelude = not guard['separated']
    if prelude:
        # Interchange B/C at boundary 2, then recompute the common roles.
        pair = (c[2], c[4])
        step(pair, 2)
        assert set(moves[-1].component) & set(range(5)) == {2, 4}
        guard = tail_guard(model, c)
        guards.append(guard)
        assert guard['separated']
    A, B, C, _ = guard['role_colors']
    step((A, B), 0)
    step((A, C), 4)
    assert set(moves[-1].component) & set(range(5)) == {4}
    return dict(prelude=prelude, guards=guards), moves


def singleton_source(model, c, v, new_color):
    """General degree-four fan formula; no target or success premise.

    One common role map: root=0, new=3, left neighbor=2, right neighbor=1.
    This extends the former vertex-3 formula without altering its certificate.
    """
    model.validate(c)
    assert v in range(5) and len(model.adj[v]) == 4
    left, right = c[(v - 1) % 5], c[(v + 1) % 5]
    colors = [c[v], right, left, new_color]
    assert len(set(colors)) == 4
    assert all(c[u] in (left, right) for u in model.adj[v])
    roles = {color: i for i, color in enumerate(colors)}
    r = tuple(roles[color] for color in c)
    cut = [e for e, uv in enumerate(model.edges) if v in uv]
    g = nx.Graph()
    g.add_edges_from(model.dual.ends[e] for e in cut)
    terminals = [model.dual.f + (v - 1) % 5, model.dual.f + v]
    path = nx.shortest_path(g, *terminals)
    assert len(path) == 5 and set(path) == set(g) and g.number_of_edges() == 4
    edges = [next(e for e in cut if set(model.dual.ends[e]) == {a, b})
             for a, b in zip(path, path[1:])]
    types = [r[a] ^ r[b] for a, b in model.edges]
    assert [types[e] for e in edges] == [2, 1, 2, 1]
    charts, delta = [], [0]
    for pair in TYPE_PAIRS[1:]:
        retained = [e for e, t in enumerate(types) if t in pair and e not in cut]
        assert not any(u in terminals for e in retained for u in model.dual.ends[e])
        before = quotient(model, retained, [e for e in cut if types[e] in pair])
        after = quotient(model, retained, [e for e in cut if types[e] ^ 3 in pair])
        owner = {u: i for i, block in enumerate(before['blocks']) for u in block}
        a, b, d = [owner[u] for u in path[1:4]]
        indicators = [int(a == b), int(b == d)]
        if pair == (2, 3):
            indicators.reverse()
        assert [before['quotient_nullity'], after['quotient_nullity']] == indicators
        delta.append(indicators[1] - indicators[0])
        charts.append(dict(types=pair, retained_edges=retained, before=before, after=after,
                           inner_owners=[a, b, d], indicators=indicators))
    assert all(-1 <= d <= 1 for d in delta)
    return dict(vertex=v, new_color=new_color, role_colors=colors,
                pair=sorted((c[v], new_color)), component=[v],
                cut_path=path, cut_edges=edges, charts=charts, predicted_delta=delta)


def boundary_audit():
    table = {}
    checked = 0
    for c in product(range(4), repeat=5):
        if any(c[i] == c[(i + 1) % 5] for i in range(5)):
            continue
        checked += 1
        moves = []
        for v in range(5):
            for color in range(4):
                if color in (c[v], c[(v - 1) % 5], c[(v + 1) % 5]):
                    continue
                d = list(c)
                d[v] = color
                if success_boundary(d):
                    moves.append((v, singleton_of(d)))
        p = tuple(normalize(c))
        value = sorted(moves)
        if p in table:
            assert table[p] == value
        table[p] = value
        if p == (0, 1, 2, 0, 1):
            assert sorted(v for v, _ in moves) == [0, 4]
    assert checked == 240 and len(table) == 10
    return dict(proper_assignments=checked, table=[dict(pattern=p, successful_recolors=moves)
                for p, moves in sorted(table.items())])


def report():
    source, barriers, local = [json.loads(p.read_text()) for p in (SOURCE, BARRIERS, LOCAL)]
    for artifact in (source, barriers, local):
        for path, digest in artifact['hashes'].items():
            assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    rows, states, chi = source['transitions'], source['states'], source['chi']
    goals = set(source['goals'])
    assert goals == {i for i, c in enumerate(states) if success_boundary(c)}
    model = EdgeModel(source['graph'])
    assert [len(model.adj[v]) for v in range(5)] == [10, 4, 6, 4, 7]
    # Exhaust every maximal-component action on every non-Goal chi=2 source.
    # Predicate reads the boundary result, never the target or Goal table.
    direct = {}
    for s, c0 in enumerate(states):
        if chi[s] != 2 or s in goals:
            continue
        c = tuple(c0)
        for action in model.actions(c):
            if len(action.component) != 1:
                continue
            v = action.component[0]
            if v >= 5 or len(model.adj[v]) != 4:
                continue
            color = next(x for x in action.pair if x != c[v])
            boundary = list(c[:5])
            boundary[v] = color
            if success_boundary(boundary):
                schema = singleton_source(model, c, v, color)
                assert sum(schema['predicted_delta']) <= 2
                direct.setdefault(s, []).append(schema)
    assert set(direct) == {r['source'] for r in local['checks']}
    # Equal-height edges are reversible; the forbidden delta has sum +1 and
    # therefore deletes none of them. Do NOT undirect the general banned graph.
    neutral = nx.Graph()
    neutral.add_nodes_from(i for i, h in enumerate(chi) if h == 2 and i not in goals)
    keys = {(s, e['target'], tuple(e['pair']), tuple(e['component']))
            for s in neutral for e in rows[s] if e['boundary_roots'] and e['target'] in neutral}
    assert all((t, s, p, c) in keys for s, t, p, c in keys)
    neutral.add_edges_from((s, t) for s, t, _, _ in keys)
    components = sorted((sorted(b) for b in nx.connected_components(neutral)), key=lambda b: b[0])
    coverage = [dict(states=b, direct_sources=sorted(set(b) & set(direct))) for b in components]
    covered = {s for row in coverage if row['direct_sources'] for s in row['states']}
    assert len(components) == 20 and len(neutral) == 936 and covered == set(direct)
    assert len(covered) == 96
    basin = next(b for b in barriers['plateaus'] if b['start'] == 84)
    B = set(basin['states'])
    assert B == set(nx.node_connected_component(neutral, 84)) and len(B) == 72
    assert not B & covered
    assert {tuple(normalize(states[s][:5])) for s in B} == {(0, 1, 2, 0, 1)}
    # Suffixes stay outside B, never rise, and stay at or below 4.
    safe = lambda s: chi[s] <= 4 and s not in B
    allowed = lambda s, e: bool(e['boundary_roots']) and chi[e['target']] <= chi[s]
    solution = solve(rows, goals, allowed, safe)
    graph = nx.DiGraph()
    graph.add_nodes_from(s for s in range(len(states)) if safe(s))
    graph.add_edges_from((s, e['target']) for s in list(graph) for e in rows[s]
                        if e['target'] in graph and allowed(s, e))
    graph.add_node(-1)
    graph.add_edges_from((g, -1) for g in goals if safe(g))
    distances = nx.single_source_shortest_path_length(graph.reverse(), -1)
    assert solution['rank'] == [distances[s] - 1 if s in distances else None for s in range(len(states))]
    preparation = []
    for s in sorted(B):
        c = tuple(states[s])
        actions = [a for a in model.actions(c) if len(a.component) == 1
                   and a.component[0] < 5 and len(model.adj[a.component[0]]) == 4]
        assert len(actions) == 1 and actions[0].component == (1,)
        a = actions[0]
        color = next(x for x in a.pair if x != c[1])
        schema = singleton_source(model, c, 1, color)
        d = model.apply(c, a)
        e = next(e for e in rows[s] if e['pair'] == list(a.pair) and e['component'] == [1])
        t = e['target']
        assert tuple(states[t]) == d and t not in goals and chi[t] == 4
        assert schema['predicted_delta'] == [0, 1, 1]
        roles = {color: i for i, color in enumerate(schema['role_colors'])}
        systems = [model.dual.systems(tuple(roles[x] for x in z)) for z in (c, d)]
        assert systems[0][0] == systems[1][0]
        vectors = [[sum(not terminals for terminals, _ in system) for system in triple]
                   for triple in systems]
        assert [b - a for a, b in zip(*vectors)] == schema['predicted_delta']
        for i, chart in enumerate(schema['charts'], 1):
            assert [chart['before']['cycles'], chart['after']['cycles']] == [vectors[0][i], vectors[1][i]]
        suffix = route(rows, solution, t)
        assert suffix is not None and len(suffix['events']) in (2, 3)
        strategy, moves = structural_tail(model, d)
        guard_sources = [d]
        if strategy['prelude']:
            guard_sources.append(model.apply(d, moves[0]))
        for guard_c, guard in zip(guard_sources, strategy['guards']):
            A, _, C, _ = guard['role_colors']
            after_first = model.apply(guard_c, Move(tuple(guard['first_pair']),
                                                   tuple(guard['first_component'])))
            actual_blocks = sorted(list(a.component) for a in model.actions(after_first)
                                   if set(a.pair) == {A, C})
            assert actual_blocks == guard['predicted_AC_components']
            assert sorted(v for block in actual_blocks for v in block) == guard['predicted_AC_vertices']
            assert guard['separated'] == all(not {2, 4} <= set(block) for block in actual_blocks)
        # Independently found shortest nonincreasing suffixes certify that the
        # source-guard recipe has the same length on this corpus.
        assert len(moves) == len(suffix['events'])
        events, current_id = [dict(source=s, **e)], t
        for move in moves:
            event = next(e for e in rows[current_id] if e['pair'] == list(move.pair)
                         and e['component'] == list(move.component))
            assert chi[event['target']] <= chi[current_id]
            events.append(dict(source=current_id, **event))
            current_id = event['target']
        current, ids = c, [s]
        for event in events:
            assert event['source'] == ids[-1] and event['boundary_roots']
            current = model.apply(current, Move(tuple(event['pair']), tuple(event['component'])))
            target = event['target']
            assert current == tuple(states[target])
            delta = [b - a for a, b in zip(source['cycle_vectors'][ids[-1]], source['cycle_vectors'][target])]
            assert sorted(delta) != [-1, 0, 2]
            assert target not in B
            ids.append(target)
        assert ids[-1] in goals and max(chi[i] for i in ids) == 4
        expected_heights = [2, 4, 3, 3, 2] if strategy['prelude'] else [2, 4, 3, 2]
        assert [chi[i] for i in ids] == expected_heights
        preparation.append(dict(source=s, schema=schema, path=ids,
                                heights=[chi[i] for i in ids], events=events,
                                structural_tail=strategy, independent_shortest_suffix=suffix))
    files = {SOURCE, BARRIERS, LOCAL, Path(__file__).resolve(), ROOT / 'scripts/c5_strategy_safe.py',
             ROOT / 'scripts/c5_strategy_barriers.py',
             *(ROOT / p for a in (source, barriers, local) for p in a['hashes'])}
    summary = dict(chi2_non_goals=len(neutral), neutral_components=len(components),
                   covered_components=sum(bool(r['direct_sources']) for r in coverage),
                   covered_states=len(covered), uncovered_states=len(neutral) - len(covered),
                   B2_states=len(B), singleton_preparations=len(preparation),
                   tail_guard_direct=sum(not r['structural_tail']['prelude'] for r in preparation),
                   tail_guard_needs_prelude=sum(r['structural_tail']['prelude'] for r in preparation),
                   suffix_length_histogram=dict(sorted(Counter(len(r['events']) - 1 for r in preparation).items())),
                   total_replayed_steps=sum(len(r['events']) for r in preparation))
    return dict(trust='Boundary obstruction and local fan bound on paper; fixed-closure strategy replay; not Lean.',
                boundary_audit=boundary_audit(), neutral_components=coverage,
                direct_source_ids=sorted(direct), B2=sorted(B), preparations=preparation,
                suffix_solution=solution, summary=summary,
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
