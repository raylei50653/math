#!/usr/bin/env python3
"""Independent original-edge, connected-bag checks for fixed named K5 controls."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE / 'frozen/topology/minor_controls.json'


def require(value, message):
    if not value:
        raise ValueError(message)


def connected(vertices, edges):
    reached = {min(vertices)}
    witnesses = []
    while reached != set(vertices):
        candidates = sorted(e for e in edges if len(set(e) & reached) == 1
                            and set(e) <= set(vertices))
        require(candidates, 'bag is not connected by original edges')
        edge = candidates[0]
        witnesses.append(list(edge))
        reached.update(edge)
    return witnesses


def generate(source):
    data = source.read_bytes()
    raw = json.loads(data)
    require(raw['schema'] == 1 and len(raw['controls']) == 3, 'incomplete fixed minor control input')
    results = []
    names = set()
    for control in raw['controls']:
        require(control['name'] not in names, 'duplicate control name')
        names.add(control['name'])
        vertices = control['vertices']
        require(len(set(vertices)) == len(vertices), 'duplicate original vertex')
        edges = {tuple(sorted(e)) for e in control['original_edges']}
        require(len(edges) == len(control['original_edges']), 'duplicate original edge')
        require(all(len(e) == 2 and e[0] != e[1] and set(e) <= set(vertices) for e in edges),
                'malformed original edge')
        bags = control['ordered_bags']
        require(len(bags) == 5, 'K5 requires all five original bags')
        require(len({bag['name'] for bag in bags}) == 5, 'duplicate bag name')
        flattened = [v for bag in bags for v in bag['vertices']]
        require(len(flattened) == len(set(flattened)), 'original bags are not disjoint')
        require(set(flattened) <= set(vertices), 'bag contains non-original vertex')
        independent_trees = {}
        for bag in bags:
            group = bag['vertices']
            require(group, 'empty branch set')
            independent_trees[bag['name']] = connected(group, edges)
            supplied = {tuple(sorted(e)) for e in control['bag_spanning_trees'][bag['name']]}
            require(len(supplied) == len(group) - 1 and supplied <= edges,
                    'supplied spanning tree is not original')
            require(all(set(e) <= set(group) for e in supplied), 'tree leaves its original bag')
            connected(group, supplied)
        declared = control['all_ten_original_cross_edges']
        require(len(declared) == 10, 'incomplete K5 cross-edge witnesses')
        by_pair = {tuple(sorted(w['bags'])): w['original_edge'] for w in declared}
        require(len(by_pair) == 10, 'duplicate supplied bag pair')
        cross = []
        for left, right in itertools.combinations(bags, 2):
            pair = tuple(sorted((left['name'], right['name'])))
            possible = sorted(e for e in edges
                              if ((e[0] in left['vertices'] and e[1] in right['vertices']) or
                                  (e[1] in left['vertices'] and e[0] in right['vertices'])))
            require(possible, 'missing original cross edge for ' + repr(pair))
            require(tuple(sorted(by_pair[pair])) in possible, 'supplied cross witness is not an original edge')
            cross.append({'named_bag_pair': list(pair),
                          'all_original_cross_edges': [list(e) for e in possible],
                          'supplied_original_cross_edge': by_pair[pair]})
        require(control['complete_N2_target'] == 'not triggered', 'source-control qualification drift')
        results.append({'original_control_name': control['name'], 'original_vertices': vertices,
                        'original_edges': [list(e) for e in sorted(edges)], 'ordered_original_bags': bags,
                        'independently_computed_original_bag_spanning_trees': independent_trees,
                        'all_ten_bag_pair_original_cross_edges': cross,
                        'K5_minor_status': 'triggered and holds',
                        'complete_original_N2_target_status': 'not triggered'})
    return {'schema': 'n2-one-long-independent-named-minors-v1',
            'source_sha256': hashlib.sha256(data).hexdigest(),
            'scope': 'fixed original-edge branch-set construction controls; no graph replacement or source enumeration',
            'controls': results,
            'counts': {'fixed_minor_controls': 3, 'original_connected_disjoint_bags': 15,
                       'original_cross_edge_pairs': 30, 'target_sources': 0}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--artifact', type=Path, default=HERE / 'minor_observations.json')
    args = parser.parse_args()
    result = generate(args.source)
    data = (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()
    if args.write:
        with args.artifact.open('xb') as stream:
            stream.write(data)
    else:
        require(args.artifact.read_bytes() == data, 'minor artifact mismatch')
    print(json.dumps({'mode': 'write' if args.write else 'check', 'bytes': len(data),
                      'sha256': hashlib.sha256(data).hexdigest(), 'counts': result['counts']}, sort_keys=True))


if __name__ == '__main__':
    main()
