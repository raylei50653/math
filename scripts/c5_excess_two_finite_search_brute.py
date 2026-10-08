#!/usr/bin/env python3
"""Independent labelled reference for the epsilon-two ES search (k <= 6).

No T4-prefix, touching, tree, symmetry or conjectural pruning is used. All
labelled internal edge sets and all degree-determined boundary attachments
are enumerated. Full Sigma and every Sigma(G-e) are computed independently
by ordinary four-colour backtracking. Symmetry is applied only after a graph
has reached q or crit, for comparison with the specialized search.

Creation is exclusive; --check recomputes and compares the entire JSON bytes.
Elapsed time is printed but is deliberately absent from deterministic JSON.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
import json
from multiprocessing import Pool
from pathlib import Path
import sys
from time import perf_counter

import networkx as nx
try:
    import rustworkx as rx
except ImportError:
    rx = None

FRAME = tuple(range(5))
FRAME_EDGES = tuple(sorted(tuple(sorted((i, (i + 1) % 5))) for i in FRAME))
T4 = 932
REJECTION_INDEX = (6, 4, 3, 1, 0)
CLASSES = ('edgesets', 'disk', 't4', 'q', 'crit')
ROOT = Path(__file__).resolve().parents[1]


def _normalize(values):
    seen = {}
    return tuple(seen.setdefault(v, len(seen)) for v in values)


ROWS = tuple(sorted({_normalize(row) for row in product(range(4), repeat=5)
                     if all(row[i] != row[(i + 1) % 5] for i in FRAME)}))
assert len(ROWS) == 10
assert tuple(i for i, row in enumerate(ROWS) if len(set(row)) == 4) == (2, 5, 7, 8, 9)


def prescribed_degrees(kind, k):
    if kind not in ('NA', 'AD', 'D6'):
        raise ValueError(kind)
    if not 1 <= k <= 6:
        raise ValueError('the independent reference is restricted to 1 <= k <= 6')
    if kind != 'D6' and k < 2:
        raise ValueError('two-root types require k >= 2')
    return tuple((6 if i == 0 else 4) if kind == 'D6'
                 else (5 if i < 2 else 4) for i in range(k))


@lru_cache(None)
def _private_permutations(kind, k):
    blocks = ((5,), tuple(range(6, 5 + k))) if kind == 'D6' else ((5, 6), tuple(range(7, 5 + k)))
    maps = []
    for images in product(*(tuple(permutations(block)) for block in blocks)):
        mapping = list(range(5 + k))
        for block, image in zip(blocks, images):
            for old, new in zip(block, image):
                mapping[old] = new
        maps.append(tuple(mapping))
    return tuple(maps)


def group_size(kind, k):
    return 10 * len(_private_permutations(kind, k))


def canonical_form(edges, kind, k):
    """Full literal edge canonical form under D5 x degree-preserving Sym(k)."""
    edges = tuple(tuple(sorted(e)) for e in edges)
    best = None
    for private_map in _private_permutations(kind, k):
        for direction in (-1, 1):
            for shift in range(5):
                mapping = tuple((direction * v + shift) % 5 for v in FRAME) + private_map[5:]
                image = tuple(sorted(tuple(sorted((mapping[a], mapping[b]))) for a, b in edges))
                if best is None or image < best:
                    best = image
    return best


def _adjacency(edges, k):
    neighbours = [[] for _ in range(5 + k)]
    for a, b in edges:
        neighbours[a].append(b)
        neighbours[b].append(a)
    return neighbours


def sigma_mask(edges, k):
    """Ten completely separate ordinary DFS extension decisions."""
    neighbours = _adjacency(edges, k)
    order = sorted(range(5, 5 + k), key=lambda v: (-len(neighbours[v]), v))
    mask = 0
    colours = [-1] * (5 + k)

    def extend(index):
        if index == k:
            return True
        vertex = order[index]
        banned = {colours[u] for u in neighbours[vertex] if colours[u] >= 0}
        for colour in range(4):
            if colour not in banned:
                colours[vertex] = colour
                if extend(index + 1):
                    colours[vertex] = -1
                    return True
                colours[vertex] = -1
        return False

    for index, row in enumerate(ROWS):
        colours[:5] = row
        if extend(0):
            mask |= 1 << index
    return mask


def deletion_sigmas(edges, k):
    edges = tuple(tuple(e) for e in edges)
    return [{'edge': list(edge), 'sigma_mask': sigma_mask(edges[:i] + edges[i + 1:], k)}
            for i, edge in enumerate(edges) if edge[1] >= 5]


def planar_disk(edges, k, *, networkx_only=False):
    apex = 5 + k
    if rx is not None and not networkx_only:
        graph = rx.PyGraph(multigraph=False)
        graph.add_nodes_from(range(apex + 1))
        graph.add_edges_from_no_data(list(edges) + [(apex, b) for b in FRAME])
        return rx.is_planar(graph)
    graph = nx.Graph()
    graph.add_nodes_from(range(apex + 1))
    graph.add_edges_from(edges)
    graph.add_edges_from((apex, b) for b in FRAME)
    return nx.check_planarity(graph)[0]


def internal_edge_sets(kind, k):
    """The Euler bound gives e(H)>=k because epsilon=2 fixes degree sum 4k+2."""
    degrees = prescribed_degrees(kind, k)
    vertices = tuple(range(5, 5 + k))
    optional = tuple(pair for pair in combinations(vertices, 2)
                     if kind == 'D6' or pair != (5, 6))
    forced = ((5, 6),) if kind == 'AD' else ()
    for size in range(max(0, k - len(forced)), len(optional) + 1):
        for selected in combinations(optional, size):
            edges = forced + selected
            internal_degrees = [0] * k
            neighbours = [set() for _ in vertices]
            for a, b in edges:
                internal_degrees[a - 5] += 1
                internal_degrees[b - 5] += 1
                neighbours[a - 5].add(b - 5)
                neighbours[b - 5].add(a - 5)
            needs = tuple(d - internal_degrees[i] for i, d in enumerate(degrees))
            if any(need < 0 or need > 3 for need in needs):
                continue
            reached = {0}
            pending = [0]
            while pending:
                for v in neighbours[pending.pop()] - reached:
                    reached.add(v)
                    pending.append(v)
            if len(reached) != k:
                continue
            yield tuple(sorted(edges)), needs


def _task(args):
    kind, k, internal, needs = args
    edges = list(FRAME_EDGES + internal)
    counts = Counter(dict.fromkeys(CLASSES, 0))
    counts['edgesets'] = 1
    q_counts = Counter()
    crit_counts = Counter()

    def attach(i):
        if i == k:
            complete = tuple(sorted(edges))
            counts['disk'] += 1
            mask = sigma_mask(complete, k)
            if mask & T4 != T4:
                return
            counts['t4'] += 1
            if not any(not (mask >> index & 1) for index in REJECTION_INDEX):
                return
            counts['q'] += 1
            canonical = canonical_form(complete, kind, k)
            q_counts[canonical] += 1
            # Deliberately recompute all edges, including after the first failure.
            deleted = deletion_sigmas(complete, k)
            if all(record['sigma_mask'] != mask for record in deleted):
                counts['crit'] += 1
                crit_counts[canonical] += 1
            return
        vertex = 5 + i
        for support in combinations(FRAME, needs[i]):
            added = [(b, vertex) for b in support]
            edges.extend(added)
            if planar_disk(edges, k):
                attach(i + 1)
            if added:
                del edges[-len(added):]

    # This only eliminates H already incompatible with the specified disk.
    if planar_disk(edges, k):
        attach(0)
    return dict(counts), q_counts, crit_counts


def _orbit_record(edges, labelled_count, kind, k):
    mask = sigma_mask(edges, k)
    deleted = deletion_sigmas(edges, k)
    q = [p for p, index in enumerate(REJECTION_INDEX) if not mask >> index & 1]
    assert planar_disk(edges, k, networkx_only=True)
    assert group_size(kind, k) % labelled_count == 0
    return dict(canonical_edges=[list(e) for e in edges], labelled_count=labelled_count,
                orbit_size=labelled_count,
                sigma_mask=mask, Q=q, deletion_sigmas=deleted)


def run(kind, k, jobs=1):
    prescribed_degrees(kind, k)
    if jobs < 1:
        raise ValueError('--jobs must be positive')
    tasks = ((kind, k, edges, needs) for edges, needs in internal_edge_sets(kind, k))
    counts = Counter(dict.fromkeys(CLASSES, 0))
    q_counts = Counter()
    crit_counts = Counter()
    if jobs == 1:
        results = map(_task, tasks)
        for counted, q, crit in results:
            counts.update(counted)
            q_counts.update(q)
            crit_counts.update(crit)
    else:
        with Pool(jobs) as pool:
            for counted, q, crit in pool.imap_unordered(_task, tasks, chunksize=1):
                counts.update(counted)
                q_counts.update(q)
                crit_counts.update(crit)
    q_orbits = [_orbit_record(edges, q_counts[edges], kind, k) for edges in sorted(q_counts)]
    crit_orbits = [dict(record) for record in q_orbits
                   if tuple(map(tuple, record['canonical_edges'])) in crit_counts]
    assert sum(record['labelled_count'] for record in q_orbits) == counts['q']
    assert sum(record['labelled_count'] for record in crit_orbits) == counts['crit']
    for record in crit_orbits:
        assert all(item['sigma_mask'] != record['sigma_mask'] for item in record['deletion_sigmas'])
    return dict(schema='c5-excess-two-brute-v1', kind=kind, k=k,
                rows=[list(row) for row in ROWS], t4_mask=T4,
                rejection_index=list(REJECTION_INDEX), group_size=group_size(kind, k),
                counts={name: counts[name] for name in CLASSES},
                q_orbits=q_orbits, crit_orbits=crit_orbits)


def encode(result):
    return (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--type', dest='kind', choices=('NA', 'AD', 'D6'), required=True)
    parser.add_argument('--k', type=int, required=True)
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = args.output or ROOT / f'artifacts/c5_excess_two_finite_search/brute_{args.kind}_k{args.k}.json'
    started = perf_counter()
    result = run(args.kind, args.k, args.jobs)
    payload = encode(result)
    if args.check:
        expected = output.read_bytes()
        if expected != payload:
            raise SystemExit(f'CHECK FAILED: {output} differs from exact reference replay')
        status = 'CHECK OK'
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('xb') as handle:
            handle.write(payload)
        status = 'GENERATED'
    print(f'{status}: {args.kind} k={args.k} {result["counts"]}; '
          f'q_orbits={len(result["q_orbits"])} crit_orbits={len(result["crit_orbits"])}; '
          f'{perf_counter() - started:.3f} seconds; {output}', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
