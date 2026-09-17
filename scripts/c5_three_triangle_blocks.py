#!/usr/bin/env python3
"""Three vertex-disjoint triangle blocks: direct-bridge minor certificates."""
import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path

import networkx as nx
from c5_tree_cores import Q, options, lifted_edges
from c5_two_triangle_blocks import criticality
from c5_triangle_forks import witness_edges, edge_mask
from c5_odd_join_cores import kuratowski_certificate
from c5_disk_deletions import sha

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_three_triangle_blocks/observations.json'


def templates():
    triangles = [(3*t+i, 3*t+j) for t in range(3)
                 for i, j in [(0, 1), (0, 2), (1, 2)]]
    for same in (True, False):
        for a, b, c, x, y in product(range(3), repeat=5):
            if x in (a, b) or y in (b, c) or (same and x == y):
                continue
            lists = [{3, f} for f in (a, b, c) for _ in range(3)]
            middle = 3 if same else 4
            for v, f in [(0, x), (3, x), (middle, y), (6, y)]:
                lists[v].add(f)
            yield ('same_port' if same else 'distinct_ports', [a, b, c, x, y],
                   lists, triangles + [(0, 3), (middle, 6)])


def build(saved=None):
    pool = [] if saved is None else saved['subdivisions']
    masks = [edge_mask(witness_edges(w)) for w in pool]
    assignments, controls = [], []
    counts, digests = Counter(), {}
    for kind, metadata, lists, inner in templates():
        choices = [options(c for c in range(3) if c not in ls) for ls in lists]
        representative = lifted_edges(inner, tuple(row[0] for row in choices))
        controls.append(dict(kind=kind, metadata=metadata,
                             edges=representative, critical_edges=criticality(14, representative)))
        for ns in product(*choices):
            edges = lifted_edges(inner, ns)
            apex_edges = set(edges) | {(b, 14) for b in range(5)}
            mask = edge_mask(apex_edges)
            if saved is None:
                wi = next((i for i, wm in enumerate(masks) if wm & mask == wm), None)
                if wi is None:
                    graph = nx.Graph(sorted(apex_edges))
                    planar, _ = nx.check_planarity(graph)
                    assert not planar, (kind, metadata, ns)
                    witness = kuratowski_certificate(graph)
                    wi = len(pool)
                    pool.append(witness)
                    masks.append(edge_mask(witness_edges(witness)))
            else:
                wi = saved['witness_by_lift'][len(assignments)]
            assert type(wi) is int and 0 <= wi < len(pool)
            assert masks[wi] & mask == masks[wi]
            assignments.append(wi)
            counts[kind] += 1
            digests.setdefault(kind, hashlib.sha256()).update(
                (json.dumps([metadata, ns, edges], separators=(',', ':'))+'\n').encode())
    assert counts == dict(same_port=50688, distinct_ports=101440), counts
    if saved is not None:
        assert len(assignments) == len(saved['witness_by_lift'])
    sources = ['c5_three_triangle_blocks', 'c5_two_triangle_blocks', 'c5_triangle_forks',
               'c5_tree_cores', 'c5_odd_join_cores', 'c5_disk_deletions',
               'c5_cell_enumerator', 'local_closure', 'boundary_relations']
    prior = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'
    return dict(schema=1, fixed_pattern=Q,
                scope='Three vertex-disjoint triangle blocks, other blocks bridges, degree four; paper reduction.',
                source_sha256={f'scripts/{s}.py': sha(ROOT/'scripts'/f'{s}.py') for s in sources},
                dependency_sha256={str(prior.relative_to(ROOT)): sha(prior)},
                counts=dict(sorted(counts.items())), representative_criticality=controls,
                subdivisions=pool, witness_by_lift=assignments,
                enumeration_sha256={k:v.hexdigest() for k,v in sorted(digests.items())})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    saved = json.loads(OUT.read_text()) if args.check else None
    result = build(saved)
    data = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.check:
        assert OUT.read_text() == data, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(dict(**result['counts'], subdivisions=len(result['subdivisions']),
                          palette_controls=len(result['representative_criticality'])), indent=2))


if __name__ == '__main__':
    main()
