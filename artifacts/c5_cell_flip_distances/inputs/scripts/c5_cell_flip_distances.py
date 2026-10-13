#!/usr/bin/env python3
"""Bounded facial-flip BFS on actual named graphs in the C5 catalogue.

A target is a boundary relation, not a replacement graph. Each intermediate
state retains all vertices and edges. Distances use the embedding selected by
c5_cell_transform.topology, so they are directed policy distances and witnessed
upper bounds for unrestricted embedding choices. Requires networkx==3.5.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
import csv
import gzip
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

import networkx as nx

import c5_cell_transform as transform

ROOT = Path(__file__).resolve().parents[1]
CYCLE = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}


def universe(k):
    return [e for e in combinations(range(5 + k), 2) if e not in CYCLE]


def graph_key(graph):
    k = len(graph['vertices']) - 5
    if graph['vertices'] != list(range(5 + k)) or graph['boundary'] != list(range(5)):
        raise ValueError('Distance atlas requires the literal catalogue vertex frame')
    edges = {tuple(e) for e in graph['edges']}
    bits = sum(1 << i for i, e in enumerate(universe(k)) if e in edges)
    return f'{k}:{bits}'


def graph_from_key(key):
    k, bits = map(int, key.split(':'))
    if k < 0 or bits < 0 or bits >> len(universe(k)):
        raise ValueError('Invalid graph key')
    return transform.canonical_graph({
        'vertices': list(range(5 + k)), 'boundary': list(range(5)),
        'edges': list(CYCLE) + [e for i, e in enumerate(universe(k)) if bits & (1 << i)]})


class ColourTable:
    """Lossless bitsets of ALL interior assignments for each fixed boundary row."""

    def __init__(self, k):
        self.edges = universe(k)
        assignments = list(product(range(4), repeat=k))
        self.full = (1 << len(assignments)) - 1
        self.compat = []
        for p in transform.PATTERNS:
            row = []
            for u, v in self.edges:
                bits = 0
                for index, assignment in enumerate(assignments):
                    c = p + assignment
                    if c[u] != c[v]:
                        bits |= 1 << index
                row.append(bits)
            self.compat.append(row)

    def counts(self, edge_bits):
        indices = [i for i in range(len(self.edges)) if edge_bits & (1 << i)]
        counts = []
        for row in self.compat:
            live = self.full
            for i in indices:
                live &= row[i]
                if not live:
                    break
            counts.append(live.bit_count())
        return counts


def d5_orbit(mask):
    index = {p: i for i, p in enumerate(transform.PATTERNS)}
    orbit = set()
    for sign in (-1, 1):
        for shift in range(5):
            image = 0
            for i, p in enumerate(transform.PATTERNS):
                if mask & (1 << i):
                    q = transform.normalize(tuple(p[(shift + sign * j) % 5] for j in range(5)))
                    image |= 1 << index[q]
            orbit.add(image)
    return sorted(orbit)


def move_kind(source, target):
    if source == target:
        return 'preserve'
    if source & target == source:
        return 'gain_only'
    if source & target == target:
        return 'lose_only'
    return 'exchange'


def read_atlas(path):
    data = Path(path).read_bytes()
    if Path(path).suffix == '.gz':
        data = gzip.decompress(data)
    return json.loads(data)


def query(atlas, source, target):
    row = atlas['sources'][str(source)]
    distance = row['distance'][str(target)]
    result = {'source_representative': source, 'target_relation': target,
              'distance': distance, 'scope': atlas['scope'],
              'status': ('reached' if distance is not None else
                         'unreachable under this policy' if row['exhausted'] else
                         f"not reached within {atlas['depth']} flips")}
    if distance is not None:
        path = row['paths'][str(target)]
        result['graphs'] = [graph_from_key(key) for key in path]
        result['relations'] = [atlas['nodes'][key]['sigma'] for key in path]
        result['flips'] = [next(move for move in atlas['nodes'][a]['moves'] if move['target'] == b)
                           for a, b in zip(path, path[1:])]
    return result


def build(depth, catalogue_path=transform.CATALOGUE, progress=False):
    if type(depth) is not int or depth < 1:
        raise ValueError('Depth must be a positive integer')
    catalogue = transform.read_catalogue(catalogue_path)
    masks = sorted(map(int, catalogue['cells']))
    if len(masks) != 132:
        raise ValueError('Expected the existing 132-relation catalogue')
    tables = {k: ColourTable(k) for k in sorted({c['k_eff'] for c in catalogue['cells'].values()})}
    nodes = {}

    def intern(graph):
        key = graph_key(graph)
        if key not in nodes:
            k, bits = map(int, key.split(':'))
            counts = tables[k].counts(bits)
            sigma = sum(1 << i for i, n in enumerate(counts) if n)
            if sigma not in masks:
                raise ValueError(f'New relation {sigma} outside the saved catalogue')
            nodes[key] = {'sigma': sigma, 'counts': counts, 'rotation': None, 'moves': None}
        return key

    def expand(key):
        node = nodes[key]
        if node['moves'] is not None:
            return node['moves']
        graph = graph_from_key(key)
        topo = transform.topology(graph)
        if not topo['disk'] or not topo['connected']:
            raise ValueError('A BFS state failed connected disk validation')
        node['rotation'] = topo['rotation']
        node['moves'] = []
        for candidate in transform.flip_candidates(graph, topo):
            old, new = tuple(candidate['remove']), tuple(candidate['add'])
            edges = {tuple(e) for e in graph['edges']} - {old} | {new}
            target = intern(transform.with_edges(graph, edges))
            node['moves'].append({'remove': list(old), 'add': list(new), 'target': target})
        return node['moves']

    sources = {}
    for source_index, mask in enumerate(masks):
        graph = transform.load_cell(mask, catalogue_path)
        start = intern(graph)
        if nodes[start]['sigma'] != mask:
            raise ValueError(f'Source relation mismatch: {mask}')
        queue = deque([start])
        distance, parent = {start: 0}, {start: None}
        first = {mask: start}
        while queue:
            key = queue.popleft()
            if distance[key] == depth:
                continue
            for move in expand(key):
                target = move['target']
                if target not in distance:
                    distance[target] = distance[key] + 1
                    parent[target] = key
                    first.setdefault(nodes[target]['sigma'], target)
                    queue.append(target)
        paths = {}
        for target_mask, end in sorted(first.items()):
            path = []
            while end is not None:
                path.append(end)
                end = parent[end]
            paths[str(target_mask)] = list(reversed(path))
        steps = {str(target): (len(paths[str(target)]) - 1 if str(target) in paths else None)
                 for target in masks}
        one_step = Counter(move_kind(mask, nodes[m['target']]['sigma']) for m in expand(start))
        k = len(graph['vertices']) - 5
        lower = [target for target in masks if catalogue['cells'][str(target)]['k_eff'] < k
                 and steps[str(target)] is not None]
        lower_distance = min((steps[str(t)] for t in lower), default=None)
        sources[str(mask)] = {
            'start': start, 'k': k, 'edges': len(graph['edges']),
            'state_layers': [sum(d == i for d in distance.values()) for i in range(depth + 1)],
            'distance': steps, 'paths': paths,
            'relation_layers': [sum(d == i for d in steps.values()) for i in range(depth + 1)],
            'one_step_moves': dict(sorted(one_step.items())),
            'lower_catalogue_k_distance': lower_distance,
            'nearest_lower_catalogue_masks': [t for t in lower if steps[str(t)] == lower_distance],
            # Exact closure only if every visited state was expanded and no successor escaped.
            'exhausted': all(nodes[key]['moves'] is not None and
                             all(m['target'] in distance for m in nodes[key]['moves'])
                             for key in distance),
        }
        if progress and (source_index + 1) % 12 == 0:
            print(f'{source_index + 1}/{len(masks)} sources; {len(nodes)} distinct graphs', file=sys.stderr, flush=True)

    strata = {}
    classes = {}
    for mask, source in sources.items():
        strata.setdefault(f"{source['k']},{source['edges']}", []).append(int(mask))
        signature = [source['k'], source['edges'], source['relation_layers'],
                     source['one_step_moves'], source['lower_catalogue_k_distance']]
        classes.setdefault(json.dumps(signature, sort_keys=True), []).append(int(mask))
    orbits = {str(min(d5_orbit(mask))): d5_orbit(mask) for mask in masks}
    counts = Counter(d for source in sources.values() for d in source['distance'].values() if d is not None)
    source_files = ['scripts/c5_cell_flip_distances.py', 'scripts/c5_cell_transform.py',
                    'scripts/boundary_relations.py']
    return {
        'schema': 'c5-cell-flip-distances-v1', 'depth': depth,
        'scope': 'directed BFS under the freshly computed NetworkX disk embedding at every actual graph',
        'target': 'fixed-frame boundary relation; no representative substitution on paths',
        'unreached': 'null means not reached within this bound; only exhausted sources certify policy nonreachability',
        'catalogue_sha256': sha256(Path(catalogue_path).read_bytes()).hexdigest(),
        'source_sha256': {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in source_files},
        'networkx_version': nx.__version__,
        'pattern_order': [''.join(map(str, p)) for p in transform.PATTERNS],
        'mask_order': masks, 'nodes': dict(sorted(nodes.items())), 'sources': sources,
        'strata': strata, 'd5_orbits': orbits,
        'signature_classes': [{'signature': json.loads(s), 'members': members}
                              for s, members in sorted(classes.items())],
        'summary': {
            'graph_states': len(nodes), 'expanded_states': sum(n['moves'] is not None for n in nodes.values()),
            'distance_histogram': {str(d): counts[d] for d in sorted(counts)},
            'unreached_pairs': len(masks) ** 2 - sum(counts.values()),
            'frozen_sources': [int(s) for s, r in sources.items() if not r['one_step_moves']],
            'exhausted_sources': [int(s) for s, r in sources.items() if r['exhausted']],
            'signature_class_count': len(classes),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--depth', type=int, default=3)
    parser.add_argument('--catalogue', type=Path, default=transform.CATALOGUE)
    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument('--output', type=Path)
    output.add_argument('--check', type=Path)
    output.add_argument('--query', type=Path, help='inspect a saved shortest witnessed path')
    parser.add_argument('--source', type=int)
    parser.add_argument('--target', type=int)
    parser.add_argument('--csv', type=Path, help='also create the source-by-target distance matrix')
    args = parser.parse_args()
    try:
        if args.query:
            if args.source is None or args.target is None or args.csv:
                raise ValueError('--query needs --source and --target, without --csv')
            print(json.dumps(query(read_atlas(args.query), args.source, args.target), indent=2))
        elif args.check:
            saved = read_atlas(args.check)
            current = build(saved['depth'], args.catalogue, progress=True)
            if saved != current:
                raise ValueError('Saved atlas differs from complete deterministic replay')
            print('PASS: complete atlas replay')
        else:
            if args.output.exists() or (args.csv and args.csv.exists()):
                raise ValueError('Output already exists; refusing to overwrite')
            result = build(args.depth, args.catalogue, progress=True)
            data = (json.dumps(result, separators=(',', ':')) + '\n').encode()
            if args.output.suffix == '.gz':
                data = gzip.compress(data, mtime=0)
            with args.output.open('xb') as stream:
                stream.write(data)
            if args.csv:
                with args.csv.open('x', newline='') as stream:
                    writer = csv.writer(stream)
                    writer.writerow(['source_representative/target_relation', *result['mask_order']])
                    for source in result['mask_order']:
                        row = result['sources'][str(source)]['distance']
                        writer.writerow([source, *(row[str(target)] if row[str(target)] is not None
                                                   else f'>{args.depth}' for target in result['mask_order'])])
            print(json.dumps(result['summary'], indent=2))
    except (ValueError, KeyError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
