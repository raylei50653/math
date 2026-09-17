#!/usr/bin/env python3
"""Three triangle blocks sharing cut vertices: necessary-minor certificates."""
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
OUT = ROOT / 'artifacts/c5_shared_triangle_blocks/observations.json'


def interface_controls():
    """Enumerate all five residual two-lists; color the actual seven-point core."""
    pairs = list(combinations(range(4), 2))
    records = []
    for left1, left2, right1, right2, middle in product(pairs, repeat=5):
        forbidden_left = [c for c in range(4) if not any(
            x != y and c not in (x, y) for x in left1 for y in left2)]
        forbidden_right = [c for c in range(4) if not any(
            x != y and c not in (x, y) for x in right1 for y in right2)]
        available_left = set(range(4))-set(forbidden_left)
        available_right = set(range(4))-set(forbidden_right)
        via_interface = any(v != w and v != x and w != x
                            for v in available_left for w in available_right for x in middle)
        # Independent enumeration of all four petal colors and middle color.
        direct = any(a != b and c != d and v != w and v != x and w != x
                     and v not in (a, b) and w not in (c, d)
                     for a, b, c, d, x in product(left1, left2, right1, right2, middle)
                     for v, w in product(range(4), repeat=2))
        criterion = (left1 == left2 == right1 == right2
                     and set(left1).isdisjoint(middle))
        assert direct == via_interface == (not criterion)
        if criterion:
            records.append(dict(petal_palette=left1, middle_palette=middle))
    assert len(records) == 6
    return dict(assignments=len(pairs)**5, rejected=records)


def templates():
    # Shared vertices 0,3; middle triangle 0,3,6; outer triangles 0,1,2 and 3,4,5.
    triangles = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5),
                 (0, 3), (0, 6), (3, 6)]
    for middle in combinations(range(4), 2):
        petal = set(range(4))-set(middle)
        residual = [set(range(4)), petal, petal, set(range(4)), petal, petal, set(middle)]
        lists = [ls | {3} for ls in residual]
        inner = list(triangles)
        for v, ls in enumerate(residual):
            if 3 not in ls:
                inner.append((v, len(lists)))
                lists.append({3})
        yield ('middle_has_D' if 3 in middle else 'petals_have_D', list(middle), lists, inner)


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
    assert counts == dict(middle_has_D=17408, petals_have_D=1280), counts
    if saved is not None:
        assert len(assignments) == len(saved['witness_by_lift'])
    sources = ['c5_shared_triangle_blocks', 'c5_three_triangle_blocks', 'c5_two_triangle_blocks', 'c5_triangle_forks',
               'c5_tree_cores', 'c5_odd_join_cores', 'c5_disk_deletions',
               'c5_cell_enumerator', 'local_closure', 'boundary_relations']
    priors = [ROOT / f'artifacts/{name}/observations.json'
              for name in ['c5_two_triangle_blocks', 'c5_three_triangle_blocks']]
    return dict(schema=1, fixed_pattern=Q,
                scope='Three triangle blocks with shared cut vertices, other blocks bridges, degree four; paper reduction.',
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
