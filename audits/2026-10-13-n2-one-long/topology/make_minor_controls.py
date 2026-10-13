#!/usr/bin/env python3
"""Named original-edge K5 controls; not complete N2 target sources."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def edge(a, b):
    return tuple(sorted((a, b)))


def build(name, original_edges, bags, premise):
    edges = sorted({edge(a, b) for a, b in original_edges})
    adjacency = {}
    for a, b in edges:
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)
    named = [(label, sorted(vertices)) for label, vertices in bags]
    used = set()
    trees = {}
    for label, vertices in named:
        assert vertices and not (used & set(vertices))
        used.update(vertices)
        reached = {vertices[0]}
        todo = [vertices[0]]
        tree = []
        while todo:
            a = todo.pop(0)
            for b in sorted(adjacency.get(a, set()) & set(vertices)):
                if b not in reached:
                    reached.add(b)
                    todo.append(b)
                    tree.append(list(edge(a, b)))
        assert reached == set(vertices), (name, label)
        trees[label] = tree
    witnesses = []
    for i, (a, av) in enumerate(named):
        for b, bv in named[i + 1:]:
            crossing = [e for e in edges if
                        (e[0] in av and e[1] in bv) or
                        (e[1] in av and e[0] in bv)]
            assert crossing, (name, a, b)
            witnesses.append({'bags': [a, b], 'original_edge': crossing[0]})
    return {
        'name': name,
        'status': 'triggered and holds',
        'claim': 'K5 minor in the explicitly named original-edge control',
        'complete_N2_target': 'not triggered',
        'premise_calibrated': premise,
        'vertices': sorted(adjacency),
        'original_edges': edges,
        'ordered_bags': [{'name': name, 'vertices': vs} for name, vs in named],
        'bag_spanning_trees': trees,
        'all_ten_original_cross_edges': witnesses,
    }


def observations():
    boundary = [('b0', 'b1'), ('b1', 'b2'), ('b2', 'b3'),
                ('b3', 'b4'), ('b4', 'b0')]
    root_short = [('r', 's0'), ('s0', 's')]
    cycle = [('p', 'q'), ('p', 'x'), ('q', 'x'),
             ('p', 'r'), ('q', 's'), ('p', 'b2'), ('q', 'b2')]
    direct = build(
        'leaf_cycle_direct_R_to_h',
        boundary + root_short + cycle + [('s0', 'b2'), ('x', 'b4'),
                                         ('x', 'r'), ('x', 'b3')],
        [('P', ['p']), ('Q', ['q']), ('H', ['b2']),
         ('R', ['r', 's', 's0']), ('F', ['x', 'b0', 'b1', 'b3', 'b4'])],
        'Leaf-cycle direct-attachment branch-set construction; degree and source conditions not asserted.',
    )
    arc = build(
        'leaf_cycle_boundary_arc_R_to_h',
        boundary + root_short + cycle + [('s0', 'b0'), ('x', 'b4'), ('x', 'b3')],
        [('P', ['p']), ('Q', ['q']), ('H', ['b2']),
         ('R', ['r', 's', 's0', 'b0', 'b1']), ('F', ['x', 'b3', 'b4'])],
        'Leaf-cycle boundary arcs h=b2, a=b0, b=b4; degree and source conditions not asserted.',
    )
    bridge = build(
        'leaf_bridge_both_endpoints_spokes',
        boundary + root_short + [('p', 'x'), ('p', 'r'), ('p', 'b1'),
                                ('p', 'b2'), ('r', 'b1'), ('s', 'b2'),
                                ('x', 'b4'), ('x', 's'), ('s0', 'b0')],
        [('P', ['p']), ('A', ['b1']), ('B', ['b2']),
         ('R', ['r', 's', 's0']), ('F', ['x', 'b0', 'b3', 'b4'])],
        'Leaf bridge ab=12 whose endpoints are actual root spokes; degree and source conditions not asserted.',
    )
    return {'schema': 1, 'evidence_layer': 'finite named minor controls only',
            'controls': [direct, arc, bridge]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = (json.dumps(observations(), sort_keys=True, indent=2) + '\n').encode()
    path = HERE / 'minor_controls.json'
    if args.check:
        assert path.read_bytes() == data, 'artifact mismatch'
    else:
        with path.open('xb') as stream:
            stream.write(data)
    print(json.dumps({'ok': True, 'controls': 3,
                      'original_cross_edges': 30,
                      'sha256': hashlib.sha256(data).hexdigest()}))


if __name__ == '__main__':
    main()
