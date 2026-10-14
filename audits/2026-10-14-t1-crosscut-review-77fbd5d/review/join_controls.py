#!/usr/bin/env python3
"""Compare literal full-lift products with direct colouring of actual toy disks.

These planar graphs are positive controls, not minimum no4ct sources.
All shell faces are read from the adopted BASE authority, never a new producer.
"""
import copy
from functools import lru_cache
import importlib.util
from itertools import product
import json
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[1]
REPO = AUDIT.parents[1]
BASE_AUTHORITY = REPO / 'audits/2026-10-13-c8-terminal-s1-d521163/AUTHORITY.json'
BROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
EXAMPLES = (
    ('cycle', 0, ()),
    ('wheel', 1, tuple((6, i) for i in range(6))),
    ('fan', 0, ((0,2),(0,3),(0,4))),
    ('triangle', 0, ((0,2),(2,4),(4,0))),
    ('opposite_chord', 0, ((0,3),)),
    ('short_chord', 0, ((0,2),)),
    ('stacked_fan', 1, ((0,2),(0,3),(0,4),(6,0),(6,1),(6,2))),
)


def edge(a, b):
    return tuple(sorted((a, b)))


def all_lifts(vertices, edges, fixed=None):
    """Enumerate literal complete colourings with dynamic degree order."""
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    colors = dict(fixed or {})
    assert all(colors[a] != colors[b] for a, b in edges if a in colors and b in colors)
    out = []
    def visit():
        if len(colors) == len(vertices):
            out.append(tuple(colors[v] for v in vertices))
            return
        free = [v for v in vertices if v not in colors]
        domains = {v: set(range(4)) - {colors[w] for w in adj[v] if w in colors} for v in free}
        v = min(free, key=lambda v: (len(domains[v]), -len(adj[v]), vertices.index(v)))
        for c in sorted(domains[v]):
            colors[v] = c
            visit()
        colors.pop(v, None)
    visit()
    return sorted(out)


@lru_cache(None)
def side_lifts(example_index):
    name, n, added = EXAMPLES[example_index]
    vertices = list(range(6+n))
    edges = {edge(i, (i+1)%6) for i in range(6)} | {edge(a,b) for a,b in added}
    fibres = {gamma: [] for gamma in product(range(4), repeat=6)}
    for word in all_lifts(vertices, edges):
        fibres[word[:6]].append(word[6:])
    return fibres, edges


def main():
    authority = json.loads(BASE_AUTHORITY.read_text())
    assert authority['B_rows'] == list(BROWS)
    results = []
    for case_index, q in enumerate(authority['queries']):
        pair = case_index % 4
        rename = dict(zip(q['original_C_names'], q['named_C']))
        faces = [[rename.get(v,v) for v in f] for f in q['annulus_faces']]
        edges = {edge(a,b) for f in faces for a,b in zip(f,f[1:]+f[:1])}
        edges |= {edge('x', f'c{pair}'), edge('x', f'c{pair+4}')}
        vertices = [f'b{i}' for i in range(5)] + [f'c{i}' for i in range(8)] + ['x']
        interfaces = [['x'] + [f'c{(pair+4*s+j)%8}' for j in range(5)] for s in range(2)]
        chosen = (case_index % len(EXAMPLES), (case_index+1) % len(EXAMPLES))
        fibres, graph_edges, all_vertices = [], set(edges), list(vertices)
        for side, ex in enumerate(chosen):
            f, es = side_lifts(ex)
            fibres.append(f)
            names = interfaces[side] + [f'z{side}_{j}' for j in range(EXAMPLES[ex][1])]
            all_vertices += names[6:]
            graph_edges |= {edge(names[a],names[b]) for a,b in es}
        totals, empty_cells = [], 0
        for beta in BROWS:
            fixed = dict(zip(vertices[:5], map(int,beta)))
            joined = []
            for shell in all_lifts(vertices, edges, fixed):
                color = dict(zip(vertices,shell))
                gamma = [tuple(color[v] for v in d) for d in interfaces]
                left, right = fibres[0][gamma[0]], fibres[1][gamma[1]]
                if not left or not right:
                    empty_cells += 1
                for a,b in product(left,right):
                    joined.append(shell+a+b)
            direct = all_lifts(all_vertices, graph_edges, fixed)
            assert sorted(joined) == direct
            assert len(joined) == len(set(joined))
            totals.append(len(direct))
        results.append({'query':q['query'], 'pair':pair, 'side_controls':[EXAMPLES[i][0] for i in chosen],
                        'full_lifts_by_B':totals, 'empty_shell_product_cells':empty_cells})
    # The supplied verifier did not bind per-record kind/pair to file slot.
    spec = importlib.util.spec_from_file_location('custody', AUDIT / 'replay_candidate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = json.loads((AUDIT/'candidate-original/t1_broad_probe/twohole_PINCH_0.json').read_text())['records']
    rejected = []
    for label in ('wrong_kind','wrong_pair','duplicate_query','missing_query'):
        damaged = copy.deepcopy(data)
        if label == 'wrong_kind': damaged[0]['kind'] = 'BRIDGE'
        elif label == 'wrong_pair': damaged[0]['pair'] = 1
        elif label == 'duplicate_query': damaged[1] = copy.deepcopy(damaged[0])
        else: damaged.pop()
        try:
            module.validate_slot(damaged, 'PINCH', 0)
        except AssertionError:
            rejected.append(label)
        else:
            raise AssertionError(('accepted malformed coverage',label))
    assert len(rejected) == 4
    print(json.dumps({'status':'PASS','scope':'actual planar controls, not minimum-source realizations',
                      'joined_graphs':len(results),'fixed_B_fibres_compared':len(results)*len(BROWS),
                      'full_lifts_compared':sum(sum(r['full_lifts_by_B']) for r in results),
                      'empty_product_cells':sum(r['empty_shell_product_cells'] for r in results),
                      'records':results,'additional_index_negative_controls_rejected':rejected}, indent=2))


if __name__ == '__main__':
    main()
