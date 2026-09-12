#!/usr/bin/env python3
"""Independent full-assignment replay, plus explicit primitive port topology checks."""
import hashlib
import itertools as it
import json
from pathlib import Path

import networkx as nx
from search_boundary import REPS, CYCLE, normalize, raw_mask


def full_sigma(n, edges):
    return {c[:5] for c in it.product(range(4), repeat=n)
            if all(c[u] != c[v] for u, v in edges)}


def check_certificate(c):
    clean = {k: v for k, v in c.items() if k != 'sha256'}
    assert c['sha256'] == hashlib.sha256(json.dumps(clean, sort_keys=True,
                                                  separators=(',', ':')).encode()).hexdigest()
    edges = list(map(tuple, c['edges']))
    assert c['boundary'] == list(range(5))
    assert set(e for e in edges if e[1] < 5) == set(CYCLE)
    actual = full_sigma(c['n'], edges)
    assert actual == set(map(tuple, c['sigma']))
    assert {normalize(b) for b in actual} == set(map(tuple, c['color_orbits']))
    assert raw_mask(actual) == int(c['sigma_bits_hex'], 16)
    assert c['state_bits'] == sum(1 << i for i, b in enumerate(REPS) if b in actual)
    emb = nx.PlanarEmbedding()
    emb.set_data(dict(enumerate(c['rotation'])))
    emb.check_structure()
    assert {tuple(sorted(e)) for e in emb.edges()} == set(edges)
    apex = nx.Graph(edges)
    apex.add_nodes_from(range(c['n']+1))
    apex.add_edges_from((i, c['n']) for i in range(5))
    assert nx.check_planarity(apex)[0] == c['cofacial_test']
    return actual


def primitives():
    eq = [(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]
    frame = list(it.combinations(range(4), 2))
    cases = [('NEQ', 2, [(0,1)], [0,1]), ('EQ', 5, eq, [0,1]),
             ('frame_exclude_A_C', 5, frame+[(0,4),(2,4)], [0,1,2,3,4]),
             ('frame_force_D', 5, frame+[(0,4),(1,4),(2,4)], [0,1,2,3,4])]
    result = []
    for name, n, edges, ports in cases:
        colors = [c for c in it.product(range(4), repeat=n)
                  if all(c[u] != c[v] for u,v in edges)]
        relation = sorted({tuple(c[i] for i in ports) for c in colors})
        if name == 'NEQ':
            assert relation == [(x,y) for x,y in it.product(range(4),repeat=2) if x != y]
        elif name == 'EQ':
            assert relation == [(x,x) for x in range(4)]
        else:
            expected = [c for c in it.product(range(4), repeat=5)
                        if len(set(c[:4])) == 4 and
                        (c[4] in (c[1],c[3]) if name == 'frame_exclude_A_C' else c[4] == c[3])]
            assert relation == expected
        graph = nx.Graph(edges)
        planar, emb = nx.check_planarity(graph)
        assert planar
        augmented = graph.copy()
        augmented.add_edges_from((n, v) for v in ports)
        cofacial = nx.check_planarity(augmented)[0]
        result.append(dict(name=name, n=n, edges=edges, ports=ports, relation=relation,
                           planar=planar, cofacial_ports_test=cofacial,
                           rotation=[list(emb.neighbors_cw_order(v)) for v in range(n)]))
    assert [c['cofacial_ports_test'] for c in result] == [True,False,False,False]
    return result


def main():
    root = Path('artifacts/gadgets')
    for name in ['library.jsonl', 'bad_certificates.jsonl']:
        certificates = [json.loads(line) for line in (root/name).read_text().splitlines()]
        for c in certificates:
            actual = check_certificate(c)
            if name == 'bad_certificates.jsonl':
                assert actual and all(len(set(b)) == 4 for b in actual)
        print(name, len(certificates), 'independent full-coloring replays passed', flush=True)
    (root/'primitives.json').write_text(json.dumps(primitives(), sort_keys=True, indent=2)+'\n')
    explanation = json.loads((root/'explanation.json').read_text())
    for side in explanation.values():
        for row in side['rejections']:
            b = row['boundary']
            allowed = {v: set(range(4)) - {b[j] for j in ns}
                       for v, ns in side['neighbors'].items()}
            assert allowed == {v: set(cs) for v, cs in row['allowed'].items()}
            union = set().union(*(allowed[str(v)] for v in row['vertices']))
            assert union == set(row['available_union'])
            assert len(union) < len(row['vertices'])
    print('Primitive relations and port topology checked', flush=True)


if __name__ == '__main__':
    main()
