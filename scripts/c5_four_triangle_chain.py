#!/usr/bin/env python3
"""Four triangle blocks in a shared-cut chain: necessary-minor certificates."""
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
OUT = ROOT / 'artifacts/c5_four_triangle_chain/observations.json'


COLORS = set(range(4))
PAIRS = list(combinations(range(4), 2))
CORE = sorted({tuple(sorted(e)) for t in [(0, 1, 2), (0, 3, 4),
                                          (3, 5, 6), (5, 7, 8)]
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
    transfers = []
    for forbidden in [()] + PAIRS:
        for side in PAIRS:
            actual = COLORS-transfer(COLORS-set(forbidden), side)
            expected = set(side) if set(side) == COLORS-set(forbidden) else set()
            assert actual == expected
            transfers.append(dict(incoming=forbidden, side=side, outgoing=sorted(actual)))
    rejected = []
    for a, b, r, s, c, d in product(PAIRS, repeat=6):
        allowed = transfer(a, b)
        allowed = transfer(allowed, r)
        allowed = transfer(allowed, s)
        via_interface = bool(allowed & transfer(c, d))
        criterion = a == b == s and c == d == r and set(a).isdisjoint(r)
        lists = [COLORS, a, b, COLORS, r, COLORS, s, c, d]
        assert direct_colorable(lists) == via_interface == (not criterion)
        if criterion:
            rejected.append(dict(left_palette=a, right_palette=r))
    assert len(rejected) == 6
    return dict(assignments=len(PAIRS)**6, rejected=rejected, transfers=transfers)


def templates():
    for left in PAIRS:
        p = set(left)
        q = COLORS-p
        residual = [COLORS, p, p, COLORS, q, COLORS, p, q, q]
        lists = [ls | {3} for ls in residual]
        inner = list(CORE)
        for v, ls in enumerate(residual):
            if 3 not in ls:
                inner.append((v, len(lists)))
                lists.append({3})
        yield ('left_has_D' if 3 in p else 'right_has_D', list(left), lists, inner)


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
    assert counts == dict(left_has_D=12288, right_has_D=12288), counts
    if saved is not None:
        assert len(assignments) == len(saved['witness_by_lift'])
    sources = ['c5_four_triangle_chain', 'c5_shared_triangle_blocks', 'c5_three_triangle_blocks', 'c5_two_triangle_blocks', 'c5_triangle_forks',
               'c5_tree_cores', 'c5_odd_join_cores', 'c5_disk_deletions',
               'c5_cell_enumerator', 'local_closure', 'boundary_relations']
    priors = [ROOT / f'artifacts/{name}/observations.json'
              for name in ['c5_shared_triangle_blocks']]
    return dict(schema=1, fixed_pattern=Q,
                scope='Four triangles in a shared-cut chain, arbitrary attached trees, degree four; paper reduction.',
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
