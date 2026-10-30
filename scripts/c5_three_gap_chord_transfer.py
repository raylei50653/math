#!/usr/bin/env python3
"""Exact ordinary-PM and odd-complement transfer across the literal inner digon.

This module is independent of the source matching/component helpers.  It
enumerates all edge subsets on both sides, including the zero/four-leaf
ordinary families.  The transfer is not merely a Tait n/y signature.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path


def _components(edges, kept, vertices):
    adjacency = {v: [] for v in vertices}
    for edge in kept:
        u, v = edges[edge]
        adjacency[u].append((v, edge))
        adjacency[v].append((u, edge))
    unseen, result = set(vertices), []
    while unseen:
        reached = {min(unseen)}
        queue = list(reached)
        for v in queue:
            for w, _ in adjacency[v]:
                if w not in reached:
                    reached.add(w)
                    queue.append(w)
        unseen -= reached
        es = sorted({e for v in reached for _, e in adjacency[v]})
        cycle = bool(es) and all(len(adjacency[v]) == 2 for v in reached)
        result.append(dict(vertices=sorted(reached), edges=es,
            cycle=cycle, odd_cycle=cycle and len(es) % 2 == 1))
    return result


def _all_pm(edges, n):
    families = {p: [] for size in (0, 2, 4) for p in combinations(range(5), size)}
    for mask in range(1 << len(edges)):
        chosen = frozenset(e for e in range(len(edges)) if mask >> e & 1)
        degree = [0] * (n + 5)
        for e in chosen:
            for v in edges[e]:
                degree[v] += 1
        if degree[:n] != [1] * n or any(d > 1 for d in degree[n:]):
            continue
        exposed = tuple(i for i in range(5) if degree[n + i] == 0)
        assert exposed in families
        complement = _components(edges, set(range(len(edges))) - chosen, range(n + 5))
        families[exposed].append(dict(matching=sorted(chosen),
            odd=sum(p['odd_cycle'] for p in complement), full_complement=complement))
    return families


def _embedding(edges, rotation, n):
    assert set(rotation) == set(range(n + 5))
    for v, order in rotation.items():
        assert sorted(order) == [e for e, ends in enumerate(edges) if v in ends]
        assert len(order) == (3 if v < n else 1)
    unseen = {(v, e) for e, ends in enumerate(edges) for v in ends}
    faces = []
    while unseen:
        start = min(unseen)
        current, darts, vertices, es = start, [], [], []
        while current not in darts:
            v, e = current
            darts.append(current)
            vertices.append(v)
            es.append(e)
            unseen.remove(current)
            w = next(w for w in edges[e] if w != v)
            order = rotation[w]
            current = (w, order[(order.index(e) + 1) % len(order)])
        assert current == start
        faces.append(dict(vertices=vertices + [vertices[0]], edges=es))
    assert n + 5 - len(edges) + len(faces) == 2
    outer = [i for i, f in enumerate(faces) if all(n + j in f['vertices'] for j in range(5))]
    assert len(outer) == 1
    leaf_order = [v - n for v in faces[outer[0]]['vertices'][:-1] if v >= n]
    assert sorted(leaf_order) == list(range(5))
    start = leaf_order.index(0)
    leaf_order = leaf_order[start:] + leaf_order[:start]
    assert leaf_order == list(range(5))
    return dict(rotation={str(v): r for v, r in rotation.items()},
        all_face_walks=faces, outer_face_index=outer[0], terminal_order=leaf_order,
        euler_sphere_passes=True)


def chord_transfer(control):
    """Return every ordinary matching fibre of the retained literal control.

    Original edge IDs 0,5 are the parallel 0--1 edges.  Removing vertices
    0,1 and edges 0,1,4,5 creates the replacement d=2--4.  If d is absent
    from N, each of its two lifts replaces complementary d by a length-three
    path, adding two to one complete complement component.  If d is in N,
    the unique lift selects edges 1,4 and adds the even 0/5 bigon to the
    complement.  Thus ordinary PM and odd(M), not only evenness, transfer.
    """
    graph = control['graph']
    edges = [tuple(e) for e in graph['network_edges']]
    n = graph['network_internal_vertices']
    assert n == 7
    assert edges[:6] == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 1)]
    removed = {0, 1, 4, 5}
    kept = [e for e in range(len(edges)) if e not in removed]
    vertex_map = {v: v - 2 for v in range(2, n + 5)}
    edge_map = {old: new for new, old in enumerate(kept)}
    reduced_edges = [tuple(vertex_map[v] for v in edges[e]) for e in kept]
    d = len(reduced_edges)
    reduced_edges.append((vertex_map[2], vertex_map[4]))
    reduced_n = n - 2
    original_rotation = {int(v): list(r) for v, r in graph['literal_rotation'].items()}
    reduced_rotation = {}
    for v in range(2, n + 5):
        reduced_rotation[vertex_map[v]] = [
            d if e in {1, 4} else edge_map[e] for e in original_rotation[v]]
    embedding = _embedding(reduced_edges, reduced_rotation, reduced_n)
    original = _all_pm(edges, n)
    reduced = _all_pm(reduced_edges, reduced_n)
    assert {''.join(map(str, p)): [r['matching'] for r in rs] for p, rs in original.items()} == control['complete_pm_families']
    fibres, minimum_rows = [], []
    for family in original:
        originals = {tuple(r['matching']): r for r in original[family]}
        used = set()
        for row in reduced[family]:
            matching = set(row['matching'])
            common = {kept[e] for e in matching if e != d}
            lifts = [common | {1, 4}] if d in matching else [common | {0}, common | {5}]
            lifted = []
            for lift in lifts:
                key = tuple(sorted(lift))
                assert key in originals and key not in used
                used.add(key)
                full = originals[key]
                assert full['odd'] == row['odd']
                lifted.append(full)
            fibres.append(dict(exposed=list(family), reduced_matching=row,
                replacement_edge_selected=d in matching, original_lifts=lifted,
                fibre_size=len(lifted), exact_odd_count_preserved=True,
                complement_operation='add even original bigon' if d in matching
                    else 'replace complementary d by length-three original path'))
        assert used == set(originals)
        old_min = min((r['odd'] for r in original[family]), default=None)
        new_min = min((r['odd'] for r in reduced[family]), default=None)
        assert old_min == new_min
        minimum_rows.append(dict(exposed=list(family), original_minimum=old_min,
            reduced_minimum=new_min,
            original_all_minimizers=[r['matching'] for r in original[family] if r['odd'] == old_min],
            reduced_all_minimizers=[r['matching'] for r in reduced[family] if r['odd'] == new_min]))
    old_even = [''.join(map(str, p)) for p, rows in original.items()
                if len(p) == 2 and any(r['odd'] == 0 for r in rows)]
    new_even = [''.join(map(str, p)) for p, rows in reduced.items()
                if len(p) == 2 and any(r['odd'] == 0 for r in rows)]
    assert old_even == new_even == ['02', '03', '24', '34']
    return dict(scope='Exact ordinary-PM and odd-count digon reduction for the literal chord control; no general E932 conclusion.',
        original_graph=graph,
        reduction=dict(removed_original_vertices=[0, 1], removed_original_edges=sorted(removed),
            original_to_reduced_vertices={str(v): w for v, w in vertex_map.items()},
            original_to_reduced_edges={str(e): f for e, f in edge_map.items()},
            replacement_edge=d, replacement_original_endpoints=[2, 4]),
        reduced_graph=dict(network_internal_vertices=reduced_n, network_edges=reduced_edges,
            literal_embedding=embedding),
        complete_original_pm_families={''.join(map(str, p)): rows for p, rows in original.items()},
        complete_reduced_pm_families={''.join(map(str, p)): rows for p, rows in reduced.items()},
        complete_transfer_fibres=fibres, all_family_minimum_transfers=minimum_rows,
        complete_even_support_before=old_even, complete_even_support_after=new_even,
        totals=dict(original_subsets_examined=1 << len(edges), reduced_subsets_examined=1 << len(reduced_edges),
            exposed_families=len(original), original_ordinary_matchings=sum(map(len, original.values())),
            reduced_ordinary_matchings=sum(map(len, reduced.values())),
            transfer_fibres=len(fibres), one_lift_fibres=sum(f['fibre_size'] == 1 for f in fibres),
            two_lift_fibres=sum(f['fibre_size'] == 2 for f in fibres),
            even_supports_equal=True, all_odd_counts_and_family_minima_preserved=True))


def main():
    from c5_nonfacial_two_gap_verification import sharp_three_gap_control
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = chord_transfer(sharp_three_gap_control())
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert args.check.read_text() == payload, 'Chord transfer certificate differs'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(result['totals'], sort_keys=True))


if __name__ == '__main__':
    main()
