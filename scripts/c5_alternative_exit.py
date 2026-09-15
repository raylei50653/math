#!/usr/bin/env python3
"""Source-side alternative-exit schema on the existing 48-state region only."""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path

import networkx as nx

from c5_edge_choices import EdgeModel, Move, ROOT
from c5_edge_states import TYPE_PAIRS
from c5_strategy_barriers import cut_audit, quotient, path_events
from c5_complementary_cube import singleton_of

SOURCE = ROOT / 'artifacts/c5_cells/strategy_safe.json'
REGION = ROOT / 'artifacts/c5_cells/strategy_no_comp.json'
OUT = ROOT / 'artifacts/c5_cells/alternative_exit.json'


def pieces(q):
    """Shapes with original edge IDs; isolates remain in q, not in this display."""
    g = nx.MultiGraph()
    g.add_nodes_from(range(len(q['blocks'])))
    g.add_edges_from((u, v, {'edge': e}) for u, v, e in q['edges'])
    answer = []
    for b in nx.connected_components(g):
        h = g.subgraph(b)
        if not h.number_of_edges():
            continue
        degrees = sorted(d for _, d in h.degree())
        if all(d == 2 for d in degrees):
            kind = 'cycle'
        elif degrees == [1, 1] + [2] * (len(b) - 2):
            kind = 'path'
        else:
            kind = 'other'
        answer.append(dict(kind=kind, length=h.number_of_edges(),
                           edges=sorted(e for _, _, e in h.edges(data='edge'))))
    return sorted(answer, key=lambda x: (x['kind'], x['length'], x['edges']))


def shape(q):
    return sorted((p['kind'], p['length']) for p in pieces(q))


def source_schema(model, c):
    """No target coloring, goal table, state ID, or target cycle vector is read.

    One COMMON color-role map for the complete source and all systems. Physical
    vertices, primal edge IDs and dual vertices are never relabeled.
    """
    model.validate(c)
    C, D, C2, A, B = c[:5]
    assert C == C2 and len({A, B, C, D}) == 4
    roles = {A: 0, B: 1, C: 2, D: 3}
    r = tuple(roles[x] for x in c)
    # This local guard proves Comp_AD(1) cannot contain boundary vertex 3.
    assert all(r[v] in (1, 2) for v in model.adj[3])
    action = next(a for a in model.actions(c)
                  if set(a.pair) == {A, D} and 1 in a.component)
    S = set(action.component)
    assert S & set(range(5)) == {1}
    cut = [e for e, (u, v) in enumerate(model.edges) if (u in S) != (v in S)]
    old = [r[u] ^ r[v] for u, v in model.edges]
    systems = model.dual.systems(r)
    assert cut == list(next(es for terminals, es in systems[0] if terminals == (0, 1)))
    assert sum(not terminals for terminals, _ in systems[0]) == 1
    assert sorted(t for t, _ in systems[0] if t) == [(0, 1), (2, 3)]
    # Build both wirings from the SOURCE cut. No target system is an input.
    charts = []
    for types in TYPE_PAIRS[1:]:
        retained = [e for e, t in enumerate(old) if t in types and e not in cut]
        before = quotient(model, retained, [e for e in cut if old[e] in types])
        after = quotient(model, retained, [e for e in cut if old[e] ^ 3 in types])
        assert before['retained_nullity'] == after['retained_nullity'] == 0
        charts.append(dict(types=types, retained_edges=retained, before=before, after=after,
                           before_pieces=pieces(before), after_pieces=pieces(after)))
    x, y = charts
    assert shape(x['before']) == [('path', 5), ('path', 6)]
    assert shape(x['after']) == [('cycle', 3), ('cycle', 6), ('path', 1)]
    assert shape(y['before']) == [('cycle', 3), ('path', 7)]
    assert shape(y['after']) == [('cycle', 1), ('path', 4), ('path', 6)]
    # The triangle moves systems with the SAME physical edges and retained
    # blocks. This is a coupled relation, not two independently matched shapes.
    triangle = next(p['edges'] for p in pieces(y['before']) if p['kind'] == 'cycle')
    assert triangle == next(p['edges'] for p in pieces(x['after'])
                            if p['kind'] == 'cycle' and p['length'] == 3)
    def expanded(q, edges):
        nodes = {v for u, v, e in q['edges'] if e in edges} | {
            u for u, v, e in q['edges'] if e in edges}
        return sorted(q['blocks'][i] for i in nodes)
    assert expanded(y['before'], triangle) == expanded(x['after'], triangle)
    vertices = {v for block in expanded(y['before'], triangle) for v in block}
    def lifted(chart):
        return sorted(triangle + [e for e in chart['retained_edges']
                                  if set(model.dual.ends[e]) <= vertices])
    assert lifted(x) == lifted(y)
    loop = next(p['edges'][0] for p in pieces(y['after']) if p['kind'] == 'cycle')
    assert any(e == loop for _, _, e in x['before']['edges'])
    hexagon = next(p['edges'] for p in pieces(x['after'])
                   if p['kind'] == 'cycle' and p['length'] == 6)
    junction = [(e, sorted(set(model.dual.ends[e]) & set(model.dual.ends[loop])))
                for e in hexagon if set(model.dual.ends[e]) & set(model.dual.ends[loop])]
    assert len(junction) == 1 and len(junction[0][1]) == 1
    # The loop-closing edge and hexagon-closing edge meet the same physical
    # dual port. Its retained owner changes when the retained system changes.
    port = junction[0][1][0]
    other = next(v for v in model.dual.ends[loop] if v != port)
    def owner(chart, v):
        return next(j for j, b in enumerate(chart['before']['blocks']) if v in b)
    assert owner(x, port) != owner(x, other)
    assert owner(y, port) == owner(y, other)
    boundary_after = list(c[:5])
    boundary_after[1] = A
    assert singleton_of(boundary_after) == 4
    return dict(role_colors=[A, B, C, D], component=list(action.component), pair=action.pair,
                cut_edges=cut, boundary_before=c[:5], boundary_after=boundary_after,
                neighbor_guard=sorted(model.adj[3]), charts=charts,
                transferred_triangle_edges=triangle, transferred_full_cycle=lifted(x),
                new_loop_edge=loop, junction=dict(dual_vertex=port,
                    face=model.faces[port], loop_edge=loop, hexagon_edge=junction[0][0]))


def report():
    source, region = [json.loads(p.read_text()) for p in (SOURCE, REGION)]
    for artifact in (source, region):
        for path, digest in artifact['hashes'].items():
            assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    model = EdgeModel(source['graph'])
    rows, states, chi = source['transitions'], source['states'], source['chi']
    R = set(region['thresholds']['3']['witness']['reachable'])
    assert len(R) == 48 and {chi[s] for s in R} == {2}
    assert not R & set(source['goals'])
    keys = {(s, e['target'], tuple(e['pair']), tuple(e['component']))
            for s in R for e in rows[s] if e['boundary_roots'] and e['target'] in R}
    assert all((t, s, p, b) in keys for s, t, p, b in keys)
    cross_level = []
    for s in sorted(R):
        for e in rows[s]:
            if not e['boundary_roots'] or e['target'] in R:
                continue
            delta = [b - a for a, b in zip(source['cycle_vectors'][s],
                                         source['cycle_vectors'][e['target']])]
            if sorted(delta) != [-1, 0, 2] and chi[e['target']] <= 4:
                assert chi[e['target']] == 4
                cross_level.append(dict(source=s, **e))
            if chi[e['target']] <= 3:
                assert sorted(delta) == [-1, 0, 2]
    # Source schema is evaluated before any successor-table lookup.
    checks = []
    for s in sorted(R):
        c = tuple(states[s])
        schema = source_schema(model, c)
        action = Move(tuple(schema['pair']), tuple(schema['component']))
        d = model.apply(c, action)
        event = next(e for e in rows[s] if e['pair'] == list(action.pair)
                     and e['component'] == list(action.component))
        assert tuple(states[event['target']]) == d
        assert list(d[:5]) == schema['boundary_after']
        assert singleton_of(d) == 4 and event['target'] in source['goals']
        roles = {color: j for j, color in enumerate(schema['role_colors'])}
        mapped = tuple(roles[color] for color in d)
        assert model.dual.systems(mapped)[0] == model.dual.systems(tuple(roles[color] for color in c))[0]
        assert [sum(not t for t, _ in sy) for sy in model.dual.systems(mapped)] == [1, 2, 1]
        assert chi[event['target']] == 4
        checks.append(dict(source=s, target=event['target'], schema=schema))
    # Explicit neutral paths to the original anchor, without assuming symmetry
    # of the globally edge-deleted graph.
    parent = {3022: None}
    queue = deque([3022])
    while queue:
        s = queue.popleft()
        for e in rows[s]:
            t = e['target']
            if e['boundary_roots'] and t in R and t not in parent:
                parent[t] = s
                queue.append(t)
    assert set(parent) == R
    routes = []
    for s in sorted(R):
        path = [s]
        while path[-1] != 3022:
            path.append(parent[path[-1]])
        events = path_events(source, path)
        for e in events:
            assert chi[e['source']] == chi[e['target']] == 2
            assert model.apply(tuple(states[e['source']]),
                               Move(tuple(e['pair']), tuple(e['component']))) == tuple(states[e['target']])
        routes.append(dict(start=s, path=path, events=events))
    comparison = [cut_audit(source, model, dict(source=3022, **next(
        e for e in rows[3022] if e['target'] == t)), True) for t in (3489, 1027)]
    files = {SOURCE, REGION, Path(__file__).resolve(), ROOT / 'scripts/c5_strategy_barriers.py',
             *(ROOT / p for a in (source, region) for p in a['hashes'])}
    return dict(trust='Source-interface lemma on paper; fixed-region Python replay; not Lean.',
        source_coloring=states[3022], comparison=comparison, region_checks=checks,
        neutral_routes_to_anchor=routes, allowed_exits_peak4=cross_level,
        summary=dict(region_size=len(R), source_schema_matches=len(checks),
                     allowed_exits_peak4=len(cross_level), neutral_routes=len(routes)),
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
