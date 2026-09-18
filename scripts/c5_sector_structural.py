#!/usr/bin/env python3
"""Boundary algebra and fixed-graph checks for the paper sector lemmas.

Does not computationally prove Jordan separation or arbitrary-size exclusion.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx
from boundary_relations import normalize
from c5_sector_targets import FULL, REPS, CYCLE

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'artifacts/c5_degree5_tree_components/observations.json'
OUT = ROOT/'artifacts/c5_sector_structural/observations.json'


def proper(b):
    return all(b[i] != b[(i+1) % 5] for i in range(5))


def component(graph, colors, vertex, pair):
    return nx.node_connected_component(graph.subgraph(v for v in graph if colors[v] in pair), vertex)


def build():
    formula = []
    for b in FULL:
        actual = bool(831 >> REPS.index(normalize(b)) & 1)
        expected = b[1] != b[3] or b[0] == b[2]
        assert actual == expected
        formula.append(dict(row=b, accepts=actual))
    chords = []
    for u, v in combinations(range(5), 2):
        if (u, v) in CYCLE:
            continue
        witnesses = [i for i in (0, 1, 4) if REPS[i][u] == REPS[i][v]]
        assert witnesses and all(831 >> i & 1 for i in witnesses)
        chords.append(dict(chord=[u, v], accepted_equal_rows=witnesses))
    # Each implication is proved by one legal component swap if the required
    # terminal connection is absent. Verify the resulting forbidden row exactly.
    claims = [dict(name='proper_A', row=[0,1,0,1,2], pair=[0,3], start=0, must_hit=[2]),
              dict(name='open_B', row=[1,1,0,1,2], pair=[1,3], start=0, must_hit=[1,3]),
              dict(name='open_C', row=[2,1,0,1,2], pair=[2,3], start=0, must_hit=[4]),
              dict(name='proper_01232', row=[0,1,2,3,2], pair=[1,3], start=1, must_hit=[3])]
    for r in claims:
        row = list(r['row'])
        row[r['start']] = r['pair'][1]
        assert proper(row) and not (831 >> REPS.index(normalize(row)) & 1)
        r['forbidden_single_terminal_swap'] = row
    source = json.loads(SOURCE.read_text())['templates'][41]
    g = nx.Graph(source['edges'])
    assert set(g[0]) == {1,4,5}
    g.remove_node(0)
    g = nx.relabel_nodes(g, {5:0})
    opened = g.copy()
    opened.remove_edges_from([(0,1),(0,4)])
    inner = sorted(set(g)-set(range(5)))
    controls = []
    for claim in claims:
        graph = opened if claim['name'].startswith('open') else g
        witnesses = []
        for cs in product(range(4), repeat=len(inner)):
            colors = dict(enumerate(claim['row'])) | dict(zip(inner,cs))
            if not all(colors[u] != colors[v] for u,v in graph.edges()):
                continue
            comp = component(graph, colors, claim['start'], claim['pair'])
            assert comp & set(claim['must_hit'])
            entry = dict(colors=[[v,colors[v]] for v in sorted(graph)], required_component=sorted(comp))
            if claim['name'] == 'proper_01232':
                # Record whether the complementary component gives a crossing.
                complementary = component(graph,colors,2,[0,2])
                entry['complementary_component_at_b2'] = sorted(complementary)
                entry['alternating_connection'] = sorted(complementary & {0,4})
            witnesses.append(entry)
        assert witnesses
        controls.append(dict(name=claim['name'], extensions=len(witnesses), witnesses=witnesses))
    files = [SOURCE] + [ROOT/'scripts'/f'{n}.py' for n in
                         ('c5_sector_structural','c5_sector_targets','boundary_relations','c5_cell_enumerator')]
    return dict(schema=1, scope='Finite boundary algebra and one saved graph; topology and general Kempe implications are paper arguments.',
                input_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files},
                conditional_equality=formula, chord_exclusions=chords, necessary_connections=claims,
                positive_control=controls,
                summary=dict(proper_rows=len(formula), chords_excluded=len(chords),
                             necessary_connection_claims=len(claims),
                             control_extension_counts={r['name']:r['extensions'] for r in controls}))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    result=build()
    data=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.check:
        assert OUT.read_text()==data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(result['summary'],indent=2))


if __name__=='__main__':
    main()
