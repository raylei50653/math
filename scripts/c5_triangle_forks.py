#!/usr/bin/env python3
"""Exhaustive contracted first-fork minors; paper coverage is in the report.

--check verifies saved subdivisions on every lift without planarity search.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx
from c5_tree_cores import Q, options, lifted_edges
from c5_odd_join_cores import kuratowski_certificate
from c5_disk_deletions import sha

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_triangle_forks/observations.json'


def templates():
    for a in range(3):
        for c in range(3):
            if a == c:
                continue
            for incoming in range(4):
                for outgoing in combinations([x for x in range(4) if x != incoming], 2):
                    if 3 not in (incoming, *outgoing):
                        continue
                    lists = [{3, a, c}, {3, a}, {3, a}, {incoming, *outgoing}]
                    inner = [(0, 1), (0, 2), (1, 2), (0, 3)]
                    for color in outgoing:
                        j = len(lists)
                        inner.append((3, j))
                        if color == 3:
                            lists.append({3})
                        else:
                            lists.extend([{3, color}, {3}])
                            inner.append((j, j+1))
                    yield (a, c, incoming, outgoing), lists, inner


def witness_edges(witness):
    """Validate the topological model independently of its search procedure."""
    branch = set(witness['branch_vertices'])
    paths = witness['paths']
    links, interiors, edges = set(), [], set()
    for path in paths:
        assert len(path) >= 2 and len(set(path)) == len(path)
        assert path[0] in branch and path[-1] in branch
        assert not branch.intersection(path[1:-1])
        interiors.extend(path[1:-1])
        links.add(tuple(sorted((path[0], path[-1]))))
        edges.update(tuple(sorted(e)) for e in zip(path, path[1:]))
    assert len(interiors) == len(set(interiors))
    assert len(links) == len(paths)
    if witness['model'] == 'K5':
        assert len(branch) == 5
        assert links == set(combinations(sorted(branch), 2))
    else:
        assert witness['model'] == 'K3,3' and len(branch) == 6
        assert any(links == {tuple(sorted((u, v))) for u in side for v in branch-set(side)}
                   for side in combinations(sorted(branch), 3))
    return edges


def edge_mask(edges):
    assert all(0 <= u < v < 32 for u, v in edges)
    return sum(1 << (32*u+v) for u, v in set(edges))


def build(saved=None):
    pool = [] if saved is None else saved['subdivisions']
    masks = [edge_mask(witness_edges(w)) for w in pool]
    assignments, counts = [], Counter()
    digest = hashlib.sha256()
    for metadata, lists, inner in templates():
        for ns in product(*(options(c for c in range(3) if c not in ls) for ls in lists)):
            edges = lifted_edges(inner, ns)
            n = 5 + len(ns)
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
            counts['lifts'] += 1
            counts['incoming_' + str(metadata[2])] += 1
            digest.update((json.dumps([metadata, ns, edges], separators=(',', ':'))+'\n').encode())
    assert counts['lifts'] == 90112
    assert len(assignments) == (len(saved['witness_by_lift']) if saved else 90112)
    counts['subdivisions'] = len(pool)
    sources = ['c5_triangle_forks', 'c5_tree_cores', 'c5_odd_join_cores',
               'c5_disk_deletions', 'c5_cell_enumerator', 'local_closure', 'boundary_relations']
    return dict(schema=1, fixed_pattern=Q,
                scope='Contracted triangle-to-first-fork minors; no coloring equivalence asserted.',
                source_sha256={f'scripts/{s}.py': sha(ROOT / 'scripts' / f'{s}.py') for s in sources},
                counts=dict(sorted(counts.items())), enumeration_sha256=digest.hexdigest(),
                subdivisions=pool, witness_by_lift=assignments)


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
    print(json.dumps(result['counts'], indent=2))


if __name__ == '__main__':
    main()
