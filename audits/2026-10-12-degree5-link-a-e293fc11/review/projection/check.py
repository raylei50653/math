#!/usr/bin/env python3
"""Finite named-pin countercontrol. Read-only --check; exclusive --write."""
import argparse
import itertools
import json
from pathlib import Path

B = ('a', 'b', 'c', 'd', 'e')
VERTICES = B + ('z',)
BOUNDARY = [(B[i], B[(i + 1) % 5]) for i in range(5)]
SPOKES = {'P0': ('a',), 'P1': ('e',), 'Q': ('b', 'c', 'd'),
          'P0_Q': ('a', 'b', 'c', 'd'), 'P1_Q': ('b', 'c', 'd', 'e')}


def canon(values):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in values)


def rows():
    return sorted({canon(p) for p in itertools.product(range(4), repeat=5)
                   if all(p[i] != p[(i + 1) % 5] for i in range(5))})


def build():
    import networkx as nx
    result = {'schema': 'degree5-link-a-pin-projection-v1', 'boundary': list(B),
              'pins': list(VERTICES), 'source_status': 'not triggered',
              'claim_status': 'counterexample', 'graphs': {}}
    for name, spokes in SPOKES.items():
        edges = BOUNDARY + [('z', b) for b in spokes]
        graph = nx.Graph(); graph.add_nodes_from(VERTICES); graph.add_edges_from(edges)
        # An outer apex tests the specified C5 as a facial boundary.
        apex = graph.copy(); apex.add_edges_from(('OUT', b) for b in B)
        assert nx.check_planarity(apex)[0]
        fibres = []
        for beta in rows():
            full = [list(beta + (c,)) for c in range(4)
                    if all(c != beta[B.index(b)] for b in spokes)]
            # Independent direct whole graph enumeration, with every edge checked.
            direct = []
            for colors in itertools.product(range(4), repeat=6):
                if colors[:5] != beta:
                    continue
                assignment = dict(zip(VERTICES, colors))
                if all(assignment[u] != assignment[v] for u, v in edges):
                    direct.append(list(colors))
            assert direct == full
            fibres.append({'beta': list(beta), 'full_lifts': full})
        result['graphs'][name] = {'vertices': list(VERTICES), 'edges': [list(e) for e in edges],
                                 'fibres': fibres,
                                 'mask': sum((1 << i) for i, f in enumerate(fibres) if f['full_lifts'])}
    assert len(rows()) == 10
    assert result['graphs']['P0']['mask'] == result['graphs']['P1']['mask'] == 1023
    for i, beta in enumerate(rows()):
        for name in ('P0', 'P1'):
            old = {tuple(x) for x in result['graphs'][name]['fibres'][i]['full_lifts']}
            ext = {tuple(x) for x in result['graphs']['Q']['fibres'][i]['full_lifts']}
            joint = {tuple(x) for x in result['graphs'][name + '_Q']['fibres'][i]['full_lifts']}
            assert old & ext == joint
    witness = [0, 1, 2, 3, 1]
    index = rows().index(tuple(witness))
    assert not result['graphs']['P0_Q']['fibres'][index]['full_lifts']
    assert result['graphs']['P1_Q']['fibres'][index]['full_lifts'] == [witness + [0]]
    result['difference'] = {'beta': witness, 'P0_Q': [], 'P1_Q': [witness + [0]]}
    result['rotation_contract'] = {
        'wheel_rotation_at_z': list(B),
        'Q_face': ['z', 'd', 'e', 'a', 'b'],
        'P0_edge_in_Q_face': ['z', 'a'], 'P1_edge_in_Q_face': ['z', 'e'],
        'interpretation': 'Delete absent spokes from one fixed embedded wheel; the added edge lies in the same named face.'}
    return result


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path); group.add_argument('--check', type=Path)
    args = parser.parse_args()
    expected = build()
    if args.write:
        with args.write.open('x') as stream:
            json.dump(expected, stream, indent=2); stream.write('\n')
    else:
        actual = json.loads(args.check.read_text())
        if actual != expected:
            raise SystemExit('REJECT: certificate differs from complete literal reconstruction')
    print(json.dumps({'status': 'PASS', 'control': 'counterexample', 'rows': len(rows()),
                      'masks': {key: value['mask'] for key, value in expected['graphs'].items()},
                      'source_status': 'not triggered'}, sort_keys=True))


if __name__ == '__main__':
    main()
