#!/usr/bin/env python3
"""Two-triangle block minors with certificate-only topology replay.

Paper coverage includes arbitrary outer trees and arbitrary bridge-path length.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx
from c5_tree_cores import Q, QI, options, lifted_edges
from c5_triangle_forks import witness_edges, edge_mask
from c5_odd_join_cores import kuratowski_certificate
from c5_disk_deletions import CYCLE, faces_of, relation, sha
from local_closure import direct_graph_extend

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'
TRIANGLES = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5)]


def templates():
    for a, b in combinations(range(3), 2):
        yield ('no_D', [a, b], [{a, b, 3} for _ in range(3)] + [{3} for _ in range(3)],
               [(0, 1), (0, 2), (1, 2), (0, 3), (1, 4), (2, 5)])
    for a in range(3):
        p = {3, a}
        other = set(range(4))-p
        yield ('shared', [a], [set(range(4)), p, p, other | {3}, other | {3}, {3}, {3}],
               [(0, 1), (0, 2), (1, 2), (0, 3), (0, 4), (3, 4), (3, 5), (4, 6)])
    for a, c, b, d in product(range(3), repeat=4):
        if a == c or b == d:
            continue
        yield ('contracted_bridge', [a, c, b, d],
               [{3, a, c}, {3, a}, {3, a}, {3, b, d}, {3, b}, {3, b}],
               TRIANGLES + [(0, 3)])


def lifts():
    for kind, metadata, lists, inner in templates():
        for ns in product(*(options(c for c in range(3) if c not in ls) for ls in lists)):
            yield kind, metadata, ns, lifted_edges(inner, ns)


def stem_lifts(bases):
    for base_index, base in enumerate(bases):
        a, c, b, d = base['metadata']
        for kind, lists, inner in [
                ('one_stem', [{3, c, d}, {3}], TRIANGLES + [(0, 6), (3, 6), (6, 7)]),
                ('two_stem', [{3, c}, {3, d}], TRIANGLES + [(0, 6), (6, 7), (3, 7)])]:
            if kind == 'one_stem' and c == d:
                continue
            for extra in product(*(options(x for x in range(3) if x not in ls) for ls in lists)):
                ns = tuple(tuple(row) for row in base['neighborhoods']) + extra
                yield kind, [base_index, a, c, b, d], ns, lifted_edges(inner, ns)


def branch_lifts(bases):
    for base_index, base in enumerate(bases):
        a, c, b, d = base['metadata']
        if c != d:
            continue
        for v, neighbors in enumerate(base['neighborhoods']):
            for dropped in neighbors:
                color = Q[dropped]
                prefix = [tuple(ns) for ns in base['neighborhoods']]
                prefix[v] = tuple(x for x in prefix[v] if x != dropped)
                for root, leaf in product(options(x for x in range(3) if x != color), options(range(3))):
                    ns = tuple(prefix) + (root, leaf)
                    yield ('outer_branch', [base_index, a, c, b, d, v, color], ns,
                           lifted_edges(TRIANGLES + [(0, 3), (v, 6), (6, 7)], ns))


def criticality(n, edges):
    assert all(sum(v in e for e in edges) == 4 for v in range(5, n))
    assert not direct_graph_extend(n, edges, Q)
    deleted = sorted(set(edges)-CYCLE)
    for edge in deleted:
        assert direct_graph_extend(n, tuple(e for e in edges if e != edge), Q)
    return deleted


def shared_palette_control():
    """A triangle with two 2-lists forbids two root colors iff lists coincide."""
    records = []
    for p, r in product(list(combinations(range(4), 2)), repeat=2):
        forbidden = [c for c in range(4)
                     if not any(x != y and x != c and y != c for x in p for y in r)]
        assert forbidden == (list(p) if p == r else [])
        records.append(dict(lists=[p, r], forbidden=forbidden))
    return records


def build(saved=None):
    pool = [] if saved is None else saved['subdivisions']
    masks = [edge_mask(witness_edges(w)) for w in pool]
    assignments, disks, checks = [], [], []
    counts, digests, seen = Counter(), {}, set()

    def consume(rows):
        for kind, metadata, ns, edges in rows:
            n = 5 + len(ns)
            apex_edges = set(edges) | {(b, n) for b in range(5)}
            mask = edge_mask(apex_edges)
            rotation = None
            if saved is None:
                wi = next((i for i, wm in enumerate(masks) if wm & mask == wm), None)
                if wi is None:
                    graph = nx.Graph(sorted(apex_edges))
                    planar, embedding = nx.check_planarity(graph)
                    if planar:
                        wi = -1
                        rotation = [list(embedding.neighbors_cw_order(v)) for v in range(n+1)]
                    else:
                        witness = kuratowski_certificate(graph)
                        wi = len(pool)
                        pool.append(witness)
                        masks.append(edge_mask(witness_edges(witness)))
            else:
                wi = saved['witness_by_lift'][len(assignments)]
                assert type(wi) is int and -1 <= wi < len(pool)
                if wi == -1:
                    rotation = saved['disk_templates'][len(disks)]['apex_rotation']
            assignments.append(wi)
            counts[kind+'_lifts'] += 1
            if wi >= 0:
                assert masks[wi] & mask == masks[wi]
            else:
                assert kind == 'contracted_bridge'
                assert len(rotation) == n+1
                assert all(0 <= w <= n for ring in rotation for w in ring)
                assert {(min(v,w), max(v,w)) for v, ring in enumerate(rotation) for w in ring} == apex_edges
                assert n+1-len(apex_edges)+len(faces_of(rotation)) == 2
                sigma, full = relation(n, edges)
                assert bool(sigma >> QI & 1) == (metadata[1] != metadata[3])
                disks.append(dict(kind=kind, metadata=metadata, neighborhoods=ns, edges=edges,
                                  apex_rotation=rotation, sigma=sigma, full_relation=full,
                                  critical_edges=criticality(n, edges) if metadata[1] == metadata[3] else None))
                counts[kind+'_disk'] += 1
                counts['disk_sigma_'+str(sigma)] += 1
            # Q-criticality depends on palettes, not choices inside a boundary color class.
            check_key = (kind, tuple(metadata[1:] if kind.endswith('_stem') or kind == 'outer_branch' else metadata))
            if check_key not in seen:
                seen.add(check_key)
                is_obstruction = kind != 'contracted_bridge' or metadata[1] == metadata[3]
                if is_obstruction:
                    checks.append(dict(kind=kind, metadata=metadata, edges=edges,
                                       critical_edges=criticality(n, edges)))
                else:
                    assert direct_graph_extend(n, edges, Q)
            digests.setdefault(kind, hashlib.sha256()).update(
                (json.dumps([metadata, ns, edges, wi == -1], separators=(',', ':'))+'\n').encode())

    consume(lifts())
    bases = list(disks)
    consume(stem_lifts(bases))
    consume(branch_lifts(bases))
    assert {k:v for k,v in counts.items() if k.endswith('_lifts')} == dict(
        no_D_lifts=1088, shared_lifts=768, contracted_bridge_lifts=7744,
        one_stem_lifts=512, two_stem_lifts=768, outer_branch_lifts=5120), counts
    assert len(disks) == 128
    assert counts['disk_sigma_1022'] == 64
    for base in disks:
        if base['metadata'][1] == base['metadata'][3]:
            assert base['sigma'] == 1023 ^ (1 << QI)
    if saved is not None:
        assert len(assignments) == len(saved['witness_by_lift'])
        assert len(disks) == len(saved['disk_templates'])
    sources = ['c5_two_triangle_blocks', 'c5_triangle_forks', 'c5_tree_cores',
               'c5_odd_join_cores', 'c5_disk_deletions', 'c5_cell_enumerator',
               'local_closure', 'boundary_relations']
    return dict(schema=1, fixed_pattern=Q,
                scope='Exactly two triangle cycle blocks with arbitrary connecting path and outer trees; paper coverage.',
                source_sha256={f'scripts/{s}.py': sha(ROOT/'scripts'/f'{s}.py') for s in sources},
                counts=dict(sorted(counts.items())), shared_palette_control=shared_palette_control(),
                representative_criticality=checks, subdivisions=pool, witness_by_lift=assignments,
                disk_templates=disks, enumeration_sha256={k:v.hexdigest() for k,v in sorted(digests.items())})


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
