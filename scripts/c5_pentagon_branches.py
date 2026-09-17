#!/usr/bin/env python3
"""Absorbed-branch cycle-5 minors; --check uses saved subdivisions only.

Coverage for arbitrary attached trees is the paper reduction in the report.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx
from c5_tree_cores import Q, options, lifted_edges
from c5_triangle_forks import witness_edges, edge_mask
from c5_odd_join_cores import kuratowski_certificate
from c5_disk_deletions import CYCLE, sha
from local_closure import direct_graph_extend

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_pentagon_branches/observations.json'
RING = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]


def templates():
    for a in range(3):
        yield 'contains_D', [3, a], [{3, a} for _ in range(5)], RING
    for a, b in combinations(range(3), 2):
        yield ('no_D', [a, b],
               [{a, b, 3} for _ in range(5)] + [{3} for _ in range(5)],
               RING + [(v, v+5) for v in range(5)])


def palette_control():
    """Independent brute-force control of the length-five list lemma."""
    count = 0
    for lists in product(list(combinations(range(4), 2)), repeat=5):
        colorable = any(all(colors[u] != colors[v] for u, v in RING)
                        for colors in product(*lists))
        assert colorable == (len(set(lists)) != 1)
        count += 1
    assert count == 7776
    return dict(assignments=count, uncolorable=6)


def build(saved=None):
    pool = [] if saved is None else saved['subdivisions']
    masks = [edge_mask(witness_edges(w)) for w in pool]
    assignments, counts, criticality = [], Counter(), []
    digests = {}
    for kind, palette, lists, inner in templates():
        first = True
        for ns in product(*(options(c for c in range(3) if c not in ls) for ls in lists)):
            edges = lifted_edges(inner, ns)
            n = 5 + len(ns)
            if first:
                # Q lists depend on colors, not the chosen same-color boundary vertex.
                assert all(sum(v in e for e in edges) == 4 for v in range(5, n))
                assert not direct_graph_extend(n, edges, Q)
                deletions = sorted(set(edges)-CYCLE)
                for edge in deletions:
                    assert direct_graph_extend(n, tuple(e for e in edges if e != edge), Q)
                criticality.append(dict(kind=kind, palette=palette, edges=edges,
                                        critical_edges=deletions))
                first = False
            apex_edges = set(edges) | {(b, n) for b in range(5)}
            mask = edge_mask(apex_edges)
            if saved is None:
                wi = next((i for i, wm in enumerate(masks) if wm & mask == wm), None)
                if wi is None:
                    witness = kuratowski_certificate(nx.Graph(sorted(apex_edges)))
                    wi = len(pool)
                    pool.append(witness)
                    masks.append(edge_mask(witness_edges(witness)))
            else:
                wi = saved['witness_by_lift'][len(assignments)]
                assert type(wi) is int and 0 <= wi < len(pool)
            assert masks[wi] & mask == masks[wi]
            assignments.append(wi)
            counts[kind+'_lifts'] += 1
            digests.setdefault(kind, hashlib.sha256()).update(
                (json.dumps([palette, ns, edges], separators=(',', ':'))+'\n').encode())
    assert counts == dict(contains_D_lifts=1088, no_D_lifts=66560)
    if saved is not None:
        assert len(assignments) == len(saved['witness_by_lift'])
    sources = ['c5_pentagon_branches', 'c5_triangle_forks', 'c5_tree_cores',
               'c5_odd_join_cores', 'c5_disk_deletions', 'c5_cell_enumerator',
               'local_closure', 'boundary_relations']
    return dict(schema=1, fixed_pattern=Q,
                scope='Cycle-5 absorbed-branch minors; paper coverage, no Lean theorem.',
                source_sha256={f'scripts/{s}.py': sha(ROOT/'scripts'/f'{s}.py') for s in sources},
                counts=dict(sorted(counts.items())), palette_control=palette_control(),
                list_assignment_criticality=criticality,
                subdivisions=pool, witness_by_lift=assignments,
                enumeration_sha256={k: v.hexdigest() for k,v in sorted(digests.items())})


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
    print(json.dumps(dict(**result['counts'], subdivisions=len(result['subdivisions'])), indent=2))


if __name__ == '__main__':
    main()
