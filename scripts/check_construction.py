#!/usr/bin/env python3
"""Independent ALL-4^n coloring replay; no DSATUR or canonical pruning."""
import hashlib
import itertools as it
import json
from pathlib import Path

import networkx as nx
from search_boundary import CYCLE, COLORINGS, canonical, normalize, raw_mask


def main():
    root = Path('artifacts/construction')
    for name in ['bad_certificates.jsonl', 'minimized.jsonl']:
        for line in (root / name).read_text().splitlines():
            c = json.loads(line)
            digest = c.pop('sha256')
            assert digest == hashlib.sha256(json.dumps(c, sort_keys=True,
                                                       separators=(',', ':')).encode()).hexdigest()
            edges = list(map(tuple, c['edges']))
            assert c['boundary'] == list(range(5))
            assert set(e for e in edges if e[1] < 5) == set(CYCLE)
            actual = {colors[:5] for colors in it.product(range(4), repeat=c['n'])
                      if all(colors[u] != colors[v] for u, v in edges)}
            assert actual == set(map(tuple, c['sigma']))
            assert actual and all(len(set(b)) == 4 for b in actual)
            assert {normalize(b) for b in actual} == set(map(tuple, c['color_orbits']))
            assert {canonical(b) for b in actual} == set(map(tuple, c['dihedral_orbits']))
            assert c['sigma_bits_hex'] == format(raw_mask(actual), '060x')
            g = nx.Graph()
            g.add_nodes_from(range(c['n']))
            g.add_edges_from(edges)
            emb = nx.PlanarEmbedding()
            emb.set_data(dict(enumerate(c['rotation'])))
            emb.check_structure()
            assert {tuple(sorted(e)) for e in emb.edges()} == set(edges)
            apex = g.copy()
            apex.add_edges_from((c['n'], v) for v in range(5))
            assert nx.check_planarity(apex)[0] == c['cofacial_test']
            if name == 'minimized.jsonl':
                assert actual == {b for b in COLORINGS if len(set(b)) == 4}
            print(name, 'full replay and rotation structure passed;', len(actual), 'colors', flush=True)


if __name__ == '__main__':
    main()
