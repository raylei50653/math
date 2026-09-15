#!/usr/bin/env python3
"""Degree-four singleton exit: source owner formula and fixed-closure replay."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import networkx as nx

from c5_edge_choices import EdgeModel, Move, ROOT
from c5_edge_states import TYPE_PAIRS
from c5_strategy_barriers import quotient
from c5_complementary_cube import singleton_of

SOURCE = ROOT / 'artifacts/c5_cells/strategy_safe.json'
REGION = ROOT / 'artifacts/c5_cells/strategy_no_comp.json'
OUT = ROOT / 'artifacts/c5_cells/local_exit.json'


def local_source(model, c):
    """Only a complete SOURCE is read; no successor, Goal, or region lookup."""
    model.validate(c)
    C, D, C2, A, B = c[:5]
    assert C == C2 and len({A, B, C, D}) == 4
    assert len(model.adj[3]) == 4
    assert all(c[v] in (B, C) for v in model.adj[3])
    roles = {A: 0, B: 1, C: 2, D: 3}
    r = tuple(roles[x] for x in c)
    cut = [e for e, uv in enumerate(model.edges) if 3 in uv]
    graph = nx.Graph()
    graph.add_edges_from(model.dual.ends[e] for e in cut)
    terminals = [model.dual.f + i for i in (2, 3)]
    path = nx.shortest_path(graph, *terminals)
    assert len(path) == 5 and set(path) == set(graph)
    assert graph.number_of_edges() == 4
    edges = [next(e for e in cut if set(model.dual.ends[e]) == {u, v})
             for u, v in zip(path, path[1:])]
    old = [r[u] ^ r[v] for u, v in model.edges]
    assert [old[e] for e in edges] == [2, 1, 2, 1]
    charts, deltas = [], [0]
    for types in TYPE_PAIRS[1:]:
        retained = [e for e, t in enumerate(old) if t in types and e not in cut]
        assert all(v not in terminals for e in retained for v in model.dual.ends[e])
        before = quotient(model, retained, [e for e in cut if old[e] in types])
        after = quotient(model, retained, [e for e in cut if old[e] ^ 3 in types])
        owner = {v: j for j, block in enumerate(before['blocks']) for v in block}
        owners = [owner[v] for v in path[1:4]]
        left, right = int(owners[0] == owners[1]), int(owners[1] == owners[2])
        predicted = [left, right] if types == (1, 3) else [right, left]
        assert [before['quotient_nullity'], after['quotient_nullity']] == predicted
        delta = predicted[1] - predicted[0]
        assert -1 <= delta <= 1
        deltas.append(delta)
        charts.append(dict(types=types, retained_edges=retained, owners=owners,
                           closure_indicators=predicted, before=before, after=after))
    return dict(role_colors=[A, B, C, D], pair=sorted((A, D)), component=[3],
                dual_path=path, cut_edges_in_path_order=edges,
                charts=charts, predicted_delta=deltas)


def partition_audit():
    """All partitions of the three inner ports, even unrealizable ones.

    Terminal owners are always fresh. Parallel edges and loops are retained.
    This finite sanity check complements the paper proof, not disk soundness.
    """
    partitions = [p for p in product(range(3), repeat=3)
                  if p[0] == 0 and all(p[i] <= max(p[:i]) + 1 for i in (1, 2))]
    assert len(partitions) == 5
    rows = []
    for p in partitions:
        vertices = [3, *p, 4]
        betas = []
        for positions in ((1, 3), (0, 2)):
            g = nx.MultiGraph()
            g.add_nodes_from(set(vertices))
            g.add_edges_from((vertices[i], vertices[i + 1]) for i in positions)
            betas.append(g.number_of_edges() - g.number_of_nodes()
                         + nx.number_connected_components(g))
        assert betas == [int(p[0] == p[1]), int(p[1] == p[2])]
        rows.append(dict(owners=p, quotient_nullities=betas))
    deltas = sorted({(0, x['quotient_nullities'][1] - x['quotient_nullities'][0],
                     y['quotient_nullities'][0] - y['quotient_nullities'][1])
                     for x in rows for y in rows})
    assert len(deltas) == 9
    assert all(sorted(d) != [-1, 0, 2] and sum(d) <= 2 for d in deltas)
    return dict(partitions=rows, coupled_cases=25, possible_deltas=deltas)


def report():
    source, region = [json.loads(p.read_text()) for p in (SOURCE, REGION)]
    for artifact in (source, region):
        for path, digest in artifact['hashes'].items():
            assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    model = EdgeModel(source['graph'])
    R = set(region['thresholds']['3']['witness']['reachable'])
    checks, boundary_count = [], 0
    for s, colors in enumerate(source['states']):
        c = tuple(colors)
        C, D, C2, A, B = c[:5]
        if C != C2 or len({A, B, C, D}) != 4:
            continue
        boundary_count += 1
        if len(model.adj[3]) != 4 or not all(c[v] in (B, C) for v in model.adj[3]):
            continue
        schema = local_source(model, c)
        action = Move(tuple(schema['pair']), (3,))
        # Actual move and independently reconstructed target systems follow the
        # source-only predicate and prediction, never supply its premises.
        d = model.apply(c, action)
        event = next(e for e in source['transitions'][s]
                     if e['pair'] == schema['pair'] and e['component'] == [3])
        t = event['target']
        assert event['boundary_roots'] == [3] and tuple(source['states'][t]) == d
        assert tuple(d[:5]) == (C, D, C, D, B) and singleton_of(d) == 4
        assert t in source['goals']
        roles = {color: i for i, color in enumerate(schema['role_colors'])}
        sy = [model.dual.systems(tuple(roles[x] for x in z)) for z in (c, d)]
        vectors = [[sum(not terminals for terminals, _ in system) for system in systems]
                   for systems in sy]
        assert sy[0][0] == sy[1][0]
        assert [b - a for a, b in zip(*vectors)] == schema['predicted_delta']
        assert vectors == [[1, 0, 1], [1, 1, 2]]
        assert sum(vectors[0]) == source['chi'][s] == 2
        assert sum(vectors[1]) == source['chi'][t] == 4
        for i, chart in enumerate(schema['charts'], 1):
            assert chart['before']['cycles'] == vectors[0][i]
            assert chart['after']['cycles'] == vectors[1][i]
        checks.append(dict(source=s, target=t, in_R=s in R, schema=schema,
                           source_cycles=vectors[0], target_cycles=vectors[1]))
    assert boundary_count == 384 and len(checks) == 96
    assert {r['source'] for r in checks if r['in_R']} == R and len(R) == 48
    anchor = next(r for r in checks if r['source'] == 3022)
    assert anchor['target'] == 1112
    files = {SOURCE, REGION, Path(__file__).resolve(), ROOT / 'scripts/c5_strategy_barriers.py',
             *(ROOT / p for a in (source, region) for p in a['hashes'])}
    return dict(trust='General local lemma on paper, not Lean; fixed-closure Python evidence.',
                abstraction=partition_audit(), checks=checks,
                summary=dict(boundary_sources=boundary_count, local_guard_sources=len(checks),
                             covered_R=len(R), anchor=[3022, 1112],
                             delta_histogram=dict(Counter(','.join(map(str, r['schema']['predicted_delta']))
                                                          for r in checks))),
                hashes={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                        for p in sorted(files)})


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
