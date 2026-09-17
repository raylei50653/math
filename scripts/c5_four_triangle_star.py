#!/usr/bin/env python3
"""Four triangle blocks in a shared-cut star: necessary-minor certificates."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx
from c5_tree_cores import Q, options, lifted_edges
from c5_two_triangle_blocks import criticality
from c5_triangle_forks import witness_edges, edge_mask
from c5_odd_join_cores import kuratowski_certificate
from c5_disk_deletions import sha

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_four_triangle_star/observations.json'


COLORS = set(range(4))
PAIRS = list(combinations(range(4), 2))
CORE = sorted({tuple(sorted(e)) for t in [(0, 1, 2), (0, 3, 4),
                                          (1, 5, 6), (2, 7, 8)]
               for e in combinations(t, 2)})


def transfer(allowed, side):
    return {w for w in COLORS if any(v != w and x != w and v != x
                                    for v in allowed for x in side)}


def direct_colorable(lists):
    # Independent graph backtracking, with no interface or palette criterion.
    neighbors = [set() for _ in lists]
    for u, v in CORE:
        neighbors[u].add(v)
        neighbors[v].add(u)
    colors = {}
    def visit():
        if len(colors) == len(lists):
            return True
        choices = {v: set(ls)-{colors[u] for u in neighbors[v] if u in colors}
                   for v, ls in enumerate(lists) if v not in colors}
        v = min(choices, key=lambda u: (len(choices[u]), u))
        for c in sorted(choices[v]):
            colors[v] = c
            if visit():
                return True
            del colors[v]
        return False
    return visit()


def interface_controls():
    rejected = []
    for a, b, c, d, e, f in product(PAIRS, repeat=6):
        available = [transfer(a, b), transfer(c, d), transfer(e, f)]
        via_interface = any(len({x, y, z}) == 3
                            for x, y, z in product(*available))
        criterion = a == b == c == d == e == f
        lists = [COLORS, COLORS, COLORS, a, b, c, d, e, f]
        assert direct_colorable(lists) == via_interface == (not criterion)
        if criterion:
            rejected.append(dict(petal_palette=a, center_palette=sorted(COLORS-set(a))))
    assert len(rejected) == 6
    return dict(assignments=len(PAIRS)**6, rejected=rejected)


def templates():
    for petal in PAIRS:
        p = set(petal)
        residual = [COLORS]*3 + [p]*6
        lists = [ls | {3} for ls in residual]
        inner = list(CORE)
        for v, ls in enumerate(residual):
            if 3 not in ls:
                inner.append((v, len(lists)))
                lists.append({3})
        yield ('petal_has_D' if 3 in p else 'petal_no_D', list(petal), lists, inner)


def build(saved=None):
    pool = [] if saved is None else saved['subdivisions']
    masks = [edge_mask(witness_edges(w)) for w in pool]
    assignments, controls = [], []
    counts, digests = Counter(), {}
    for kind, metadata, lists, inner in templates():
        choices = [options(c for c in range(3) if c not in ls) for ls in lists]
        representative = lifted_edges(inner, tuple(row[0] for row in choices))
        controls.append(dict(kind=kind, metadata=metadata,
                             edges=representative, critical_edges=criticality(5 + len(lists), representative)))
        for ns in product(*choices):
            edges = lifted_edges(inner, ns)
            apex_edges = set(edges) | {(b, 5 + len(lists)) for b in range(5)}
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
    assert counts == dict(petal_has_D=4224, petal_no_D=528384), counts
    if saved is not None:
        assert len(assignments) == len(saved['witness_by_lift'])
    sources = ['c5_four_triangle_star', 'c5_four_triangle_chain', 'c5_shared_triangle_blocks', 'c5_three_triangle_blocks', 'c5_two_triangle_blocks', 'c5_triangle_forks',
               'c5_tree_cores', 'c5_odd_join_cores', 'c5_disk_deletions',
               'c5_cell_enumerator', 'local_closure', 'boundary_relations']
    priors = [ROOT / f'artifacts/{name}/observations.json'
              for name in ['c5_shared_triangle_blocks', 'c5_four_triangle_chain']]
    return dict(schema=1, fixed_pattern=Q,
                scope='Four triangles in a shared-cut star, arbitrary attached trees, degree four; paper reduction.',
                interface_controls=interface_controls(),
                source_sha256={f'scripts/{s}.py': sha(ROOT/'scripts'/f'{s}.py') for s in sources},
                dependency_sha256={str(prior.relative_to(ROOT)): sha(prior) for prior in priors},
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
