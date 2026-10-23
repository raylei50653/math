#!/usr/bin/env python3
"""Independent checks of marked-link shapes and the K0 connectivity gap.

This calibrates finite local statements and a rejected inference. It is not a
full 941 source, or a finite proof of the arbitrary-size two-tree dichotomy.
"""
from itertools import product
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OLD = REPO / 'audits/2026-10-23-three-mask-round2-cb8f859/941/certificate.json'


def component(adj, colours, palette, root):
    reached = {root}
    todo = [root]
    while todo:
        v = todo.pop()
        for w in adj[v]:
            if colours[w] in palette and w not in reached:
                reached.add(w)
                todo.append(w)
    return reached


def link_shapes(center, marked, spare):
    shapes = []
    for word in product((marked, spare, 3), repeat=5):
        if any(word[i] == word[(i + 1) % 5] for i in range(5)):
            continue
        if word.count(marked) < 2 or word.count(3) < 2:
            continue
        if sorted(word) != sorted((marked, marked, spare, 3, 3)):
            raise ValueError('wrong forced degree-five shape')
        shapes.append(word)
    if len(shapes) != 10:
        raise ValueError('missing degree-five orientation')
    high = (marked, 3, marked, 3, marked, 3)
    if any(high[i] == high[(i + 1) % 6] for i in range(6)):
        raise ValueError('missing degree-six calibration')
    return {'center_colour': center, 'degree_five_oriented_words': len(shapes),
            'necessary_multiset': sorted((marked, marked, spare, 3, 3)),
            'degree_six_without_spare_colour': list(high)}


def main():
    old = json.loads(OLD.read_text())
    control = next(r['graph'] for r in old['local_controls']
                   if r['name'] == 'rootless_13_branch_retained')
    phi = control['colors']
    adj = {v: set() for v in phi}
    for face in control['faces']:
        if len({phi[v] for v in face}) != 3:
            raise ValueError('improper sealed control')
        for a, b in zip(face, face[1:] + face[:1]):
            adj[a].add(b)
            adj[b].add(a)
    K = component(adj, phi, {0, 2}, 'U')
    psi = {v: 2 - colour if v in K else colour for v, colour in phi.items()}
    C = component(adj, psi, {1, 2}, 'U')
    K0 = {v for v in K if phi[v] == 0}
    if K0 <= C:
        raise ValueError('control no longer detects invalid cross-palette connectivity')
    result = {'status': 'PASS', 'source_status': 'not triggered',
              'K0_subset_C_is_a_valid_general_inference': False,
              'sealed_control': {'name': control['name'], 'K': sorted(K),
                                  'original_K0': sorted(K0),
                                  'successor_C': sorted(C),
                                  'original_K0_outside_C': sorted(K0 - C)},
              'last_bridge_T_link': link_shapes(0, 1, 2),
              'insertion_Z_link': link_shapes(2, 0, 1),
              'pair_exclusions': 0, 'source_realized': False}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
