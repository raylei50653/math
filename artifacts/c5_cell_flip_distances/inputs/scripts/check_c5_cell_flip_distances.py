#!/usr/bin/env python3
"""Independently audit a bounded C5 flip atlas; no production BFS is imported.

Colour counts enumerate every interior assignment through forbidden-assignment
unions. Facial moves are reconstructed from directed darts in saved rotations.
This checks the rotations as planar witnesses; deterministic policy identity is
separately checked by c5_cell_flip_distances.py --check.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, product
import gzip
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / 'artifacts/c5_cells/cells.json'
PATTERNS = ('01012', '01021', '01023', '01201', '01202',
            '01203', '01212', '01213', '01231', '01232')
FRAME = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode(key):
    k, bits = map(int, key.split(':'))
    require(0 <= k <= 5 and bits >= 0, 'Invalid graph key range')
    require(key == f'{k}:{bits}', 'Graph key is not canonical')
    available = [e for e in combinations(range(k + 5), 2) if e not in FRAME]
    require(bits < 1 << len(available), 'Graph key has excess edge bits')
    edges = FRAME | {e for i, e in enumerate(available) if (bits >> i) & 1}
    return k, edges


def encode(k, edges):
    available = [e for e in combinations(range(k + 5), 2) if e not in FRAME]
    return f'{k}:{sum(1 << i for i, e in enumerate(available) if e in edges)}'


class AssignmentAudit:
    """Every bit denotes a literal full assignment, without colour quotienting."""

    def __init__(self, k):
        self.total = 4 ** k
        self.forbidden = {}
        edges = list(combinations(range(5 + k), 2))
        for pattern in PATTERNS:
            bad = {e: 0 for e in edges}
            for index, assignment in enumerate(product(range(4), repeat=k)):
                colors = tuple(map(int, pattern)) + assignment
                for e in edges:
                    if colors[e[0]] == colors[e[1]]:
                        bad[e] |= 1 << index
            self.forbidden[pattern] = bad

    def counts(self, edges):
        result = []
        for pattern in PATTERNS:
            bad = 0
            for e in edges:
                bad |= self.forbidden[pattern][e]
            result.append(self.total - bad.bit_count())
        return result


def facial_moves(k, edges, saved_rotation):
    """Check a spherical rotation with C5 face, then derive all facial flips."""
    require(isinstance(saved_rotation, list), 'Missing rotation')
    require([r['vertex'] for r in saved_rotation] == list(range(5 + k)),
            'Rotation vertex frame differs')
    rotation = {r['vertex']: r['clockwise'] for r in saved_rotation}
    for v, neighbors in rotation.items():
        expected = {w if u == v else u for u, w in edges if v in (u, w)}
        require(len(neighbors) == len(set(neighbors)) and set(neighbors) == expected,
                'Rotation does not contain exactly the incident edges')
    reached = {0}
    todo = [0]
    while todo:
        for v in rotation[todo.pop()]:
            if v not in reached:
                reached.add(v)
                todo.append(v)
    require(len(reached) == 5 + k, 'Rotation graph is disconnected')
    seen, faces = set(), []
    for u in range(5 + k):
        for v in rotation[u]:
            if (u, v) in seen:
                continue
            first = dart = (u, v)
            face = []
            while dart not in seen:
                seen.add(dart)
                a, b = dart
                face.append(a)
                neighbors = rotation[b]
                dart = (b, neighbors[(neighbors.index(a) + 1) % len(neighbors)])
            require(dart == first, 'Face traversal merged into an earlier face')
            faces.append(face)
    require(5 + k - len(edges) + len(faces) == 2, 'Rotation is not planar')
    require(any(len(f) == 5 and set(f) == set(range(5)) and
                {tuple(sorted((f[i], f[(i + 1) % 5]))) for i in range(5)} == FRAME
                for f in faces), 'Rotation does not exhibit the ordered C5 face')
    moves = []
    for f, g in combinations(faces, 2):
        if len(f) != 3 or len(g) != 3:
            continue
        common = set(f) & set(g)
        if len(common) != 2:
            continue
        old = tuple(sorted(common))
        opposite = (set(f) | set(g)) - common
        if old in FRAME or len(opposite) != 2:
            continue
        new = tuple(sorted(opposite))
        if new in edges:
            continue
        moves.append({'remove': list(old), 'add': list(new),
                      'target': encode(k, (edges - {old}) | {new})})
    return sorted(moves, key=lambda m: (m['remove'], m['add']))


def validate_node(key, node, tables):
    k, edges = decode(key)
    expected = tables[k].counts(edges)
    require(node['counts'] == expected, f'Full assignment counts differ: {key}')
    sigma = sum(1 << i for i, count in enumerate(expected) if count)
    require(node['sigma'] == sigma, f'Relation differs: {key}')
    if node['moves'] is None:
        require(node['rotation'] is None, 'Unexpanded node unexpectedly has a rotation')
    else:
        require(node['moves'] == facial_moves(k, edges, node['rotation']),
                f'Facial move set differs: {key}')


def orbit(mask):
    images = set()
    for shift in range(5):
        for direction in (1, -1):
            transformed = 0
            for index, pattern in enumerate(PATTERNS):
                if not mask & (1 << index):
                    continue
                names = {}
                word = ''
                for j in range(5):
                    color = pattern[(shift + direction * j) % 5]
                    if color not in names:
                        names[color] = str(len(names))
                    word += names[color]
                transformed |= 1 << PATTERNS.index(word)
            images.add(transformed)
    return sorted(images)


def relation_change(source, target):
    removed, added = source & ~target, target & ~source
    return ('exchange' if removed and added else 'lose_only' if removed else
            'gain_only' if added else 'preserve')


def validate_sources(data, catalogue):
    nodes, depth = data['nodes'], data['depth']
    masks = sorted(map(int, catalogue['cells']))
    require(type(depth) is int and depth >= 1, 'Invalid depth')
    require(data['mask_order'] == masks and len(masks) == 132, 'Catalogue mask frame differs')
    require(set(data['sources']) == set(map(str, masks)), 'Source set differs')
    all_seen = set()
    for mask in masks:
        source = data['sources'][str(mask)]
        saved = catalogue['cells'][str(mask)]
        edges = FRAME | {tuple(sorted(e)) for e in saved['edges']}
        start = encode(saved['k_eff'], edges)
        require(source['start'] == start, f'Source graph was replaced: {mask}')
        require(source['k'] == saved['k_eff'] and source['edges'] == len(edges),
                f'Source size differs: {mask}')
        require(nodes[start]['sigma'] == mask, f'Source relation differs: {mask}')
        queue = deque([start])
        distance, parent, first = {start: 0}, {start: None}, {mask: start}
        while queue:
            key = queue.popleft()
            if distance[key] == depth:
                continue
            require(nodes[key]['moves'] is not None, 'A state below the depth bound is unexpanded')
            for move in nodes[key]['moves']:
                target = move['target']
                require(target in nodes, 'A move names an absent graph state')
                if target in distance:
                    continue
                distance[target] = distance[key] + 1
                parent[target] = key
                first.setdefault(nodes[target]['sigma'], target)
                queue.append(target)
        all_seen.update(distance)
        expected_distance = {str(m): distance[first[m]] if m in first else None for m in masks}
        require(source['distance'] == expected_distance, f'Distance table differs: {mask}')
        paths = {}
        for target_mask, endpoint in first.items():
            path = []
            while endpoint is not None:
                path.append(endpoint)
                endpoint = parent[endpoint]
            paths[str(target_mask)] = path[::-1]
        require(source['paths'] == paths, f'Graph witness paths differ: {mask}')
        require(source['state_layers'] == [sum(d == i for d in distance.values())
                                           for i in range(depth + 1)], f'Graph layers differ: {mask}')
        require(source['relation_layers'] == [sum(d == i for d in expected_distance.values())
                                              for i in range(depth + 1)],
                f'Relation layers differ: {mask}')
        changes = Counter(relation_change(mask, nodes[m['target']]['sigma']) for m in nodes[start]['moves'])
        require(source['one_step_moves'] == dict(changes), f'One-step classification differs: {mask}')
        lower = [m for m in masks if catalogue['cells'][str(m)]['k_eff'] < saved['k_eff']
                 and expected_distance[str(m)] is not None]
        nearest = min((expected_distance[str(m)] for m in lower), default=None)
        require(source['lower_catalogue_k_distance'] == nearest, f'Lower-k distance differs: {mask}')
        require(source['nearest_lower_catalogue_masks'] ==
                [m for m in lower if expected_distance[str(m)] == nearest],
                f'Lower-k targets differ: {mask}')
        require(type(source['exhausted']) is bool, 'Invalid exhaustion flag')
        if source['exhausted']:
            require(all(nodes[key]['moves'] is not None and
                        all(m['target'] in distance for m in nodes[key]['moves']) for key in distance),
                    f'False exhaustion claim: {mask}')
    require(all_seen == set(nodes), 'Atlas has graph states outside all source searches')


def validate_aggregate(data):
    sources = {m: data['sources'][m] for m in sorted(data['sources'], key=int)}
    strata, classes = {}, {}
    for mask, source in sources.items():
        strata.setdefault(f"{source['k']},{source['edges']}", []).append(int(mask))
        signature = [source['k'], source['edges'], source['relation_layers'],
                     source['one_step_moves'], source['lower_catalogue_k_distance']]
        classes.setdefault(json.dumps(signature, sort_keys=True), []).append(int(mask))
    require(data['strata'] == strata, 'Invariant strata differ')
    require(data['signature_classes'] == [
        {'signature': json.loads(s), 'members': members} for s, members in sorted(classes.items())],
        'Finite signature classes differ')
    expected_orbits = {str(min(orbit(m))): orbit(m) for m in data['mask_order']}
    require(data['d5_orbits'] == expected_orbits, 'D5 relation partition differs')
    histogram = Counter(d for source in sources.values() for d in source['distance'].values() if d is not None)
    expected = {
        'graph_states': len(data['nodes']),
        'expanded_states': sum(n['moves'] is not None for n in data['nodes'].values()),
        'distance_histogram': {str(d): histogram[d] for d in sorted(histogram)},
        'unreached_pairs': len(sources) ** 2 - sum(histogram.values()),
        'frozen_sources': [int(m) for m, r in sources.items() if not r['one_step_moves']],
        'exhausted_sources': [int(m) for m, r in sources.items() if r['exhausted']],
        'signature_class_count': len(classes),
    }
    require(data['summary'] == expected, 'Summary differs')


def validate_atlas(data, catalogue_path=CATALOGUE, provenance=True):
    require(data['schema'] == 'c5-cell-flip-distances-v1', 'Unsupported schema')
    require(data['pattern_order'] == list(PATTERNS), 'Boundary color frame differs')
    catalogue_path = Path(catalogue_path)
    catalogue = json.loads(catalogue_path.read_text())
    require(catalogue['pattern_order'] == [list(map(int, p)) for p in PATTERNS],
            'Catalogue color frame differs')
    if provenance:
        require(data['catalogue_sha256'] == sha256(catalogue_path.read_bytes()).hexdigest(),
                'Catalogue hash differs')
        expected_files = {'scripts/c5_cell_flip_distances.py', 'scripts/c5_cell_transform.py',
                          'scripts/boundary_relations.py'}
        require(set(data['source_sha256']) == expected_files, 'Producer source hash set differs')
        for filename, digest in data['source_sha256'].items():
            require(sha256((ROOT / filename).read_bytes()).hexdigest() == digest,
                    f'Producer source hash differs: {filename}')
    tables = {k: AssignmentAudit(k) for k in range(6)}
    for key, node in data['nodes'].items():
        validate_node(key, node, tables)
        require(node['sigma'] in data['mask_order'], 'Node relation absent from catalogue')
        if node['moves'] is not None:
            require(all(m['target'] in data['nodes'] for m in node['moves']), 'Missing move target')
    validate_sources(data, catalogue)
    validate_aggregate(data)
    return {'checked_graphs': len(data['nodes']), 'checked_sources': len(data['sources']),
            'checked_expanded_rotations': sum(n['moves'] is not None for n in data['nodes'].values()),
            'color_check': 'all literal assignments in all ten boundary rows',
            'exhaustion_check': 'true flags verified; conservative false flags permitted'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('atlas', type=Path)
    parser.add_argument('--catalogue', type=Path, default=CATALOGUE)
    args = parser.parse_args()
    try:
        opener = gzip.open if args.atlas.suffix == '.gz' else open
        with opener(args.atlas, 'rt') as stream:
            result = validate_atlas(json.load(stream), args.catalogue)
        print(json.dumps({'status': 'PASS', **result}, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
