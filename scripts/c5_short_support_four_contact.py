#!/usr/bin/env python3
"""Four original contacts cannot forbid the unseen pair on one boundary edge.

Finite palette and actual-edge minor controls for the companion paper proof.
The skeletons do not assert complete source degree/list or disk realizability.
"""
import argparse
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import colorings
from c5_single_spoke_two_two_minor import verify_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_short_support_four_contact/observations.json'


def skeleton(kind, start, landing, length, subdivide):
    a, b = start, (start + 1) % 5
    assert landing not in (a, b)
    edges = {tuple(sorted((f'b{i}', f'b{(i+1)%5}'))) for i in range(5)}

    def edge(x, y):
        edges.add(tuple(sorted((x, y))))

    route = ['r', 'external0', 'external1', f'b{landing}'] if subdivide else ['r', f'b{landing}']
    for x, y in zip(route, route[1:]):
        edge(x, y)
    complement = {f'b{i}' for i in range(5) if i not in (a, b)}
    external = set(route[:-1]) | complement
    if kind == 'leaf_bridge':
        contacts = ['v', 'w', 'p', 'q']
        internal = set(contacts)
        for x, y in zip(contacts, contacts[1:]):
            edge(x, y)
        for x in contacts:
            edge('r', x)
        for x in ('v', 'w'):
            edge(x, f'b{a}')
            edge(x, f'b{b}')
        bags = [{'v'}, internal - {'v'}, {f'b{a}'}, {f'b{b}'}, external]
    elif kind == 'inactive_leaf_cycle':
        cycle = [f'x{i}' for i in range(length)]
        for x, y in zip(cycle, cycle[1:] + cycle[:1]):
            edge(x, y)
        contacts = ['p0', 'p1', 'p2', 'p3']
        for x, y in zip([cycle[-1]] + contacts, contacts):
            edge(x, y)
        for x in contacts:
            edge('r', x)
        for x in cycle[:-1]:
            edge(x, f'b{a}')
            edge(x, f'b{b}')
        internal = set(cycle + contacts)
        bags = [{cycle[0]}, {cycle[1]}, {f'b{a}'}, {f'b{b}'},
                (internal - {cycle[0], cycle[1]}) | external]
    else:
        assert kind == 'two_active_leaf_triangles' and length % 2 == 1
        contacts = ['u', 'v', 'w', 'z']
        path = ['x'] + [f'p{i}' for i in range(length - 1)] + ['y']
        for triangle, frame in ((['u', 'v', 'x'], a), (['w', 'z', 'y'], b)):
            for x, y in zip(triangle, triangle[1:] + triangle[:1]):
                edge(x, y)
            for x in triangle:
                edge(x, f'b{frame}')
        for x, y in zip(path, path[1:]):
            edge(x, y)
        for x in path[1:-1]:
            edge(x, f'b{a}')
            edge(x, f'b{b}')
        for x in contacts:
            edge('r', x)
        internal = set(contacts + path)
        # The selected positive leaf triangle has three actual a attachments.
        outside = (internal - {'u', 'v', 'x'}) | set(route[:-1]) | {
            f'b{i}' for i in range(5) if i != a}
        bags = [{'u'}, {'v'}, {'x'}, {f'b{a}'}, outside]
        # These internal points really retain degree four in this control.
        assert all(sum(v in e for e in edges) == 4 for v in internal)
    assert len(contacts) == len(set(contacts)) == 4
    assert {v if u == 'r' else u for u, v in edges
            if 'r' in (u, v) and (v if u == 'r' else u) in internal} == set(contacts)
    return dict(kind=kind, original_contacts=contacts, boundary_edge=[a, b],
                original_external_route=route, length=length, edges=sorted(edges),
                branch_sets=[sorted(s) for s in bags], adjacencies=verify_minor(edges, bags))


def build():
    palette_controls = []
    for a, b, c, d in permutations(range(4)):
        # In the leaf-bridge case the remaining component must force d, with
        # root c fixed.  Every seen boundary colour is necessary for that.
        for mask in range(4):
            seen = {color for bit, color in enumerate((a, b)) if mask >> bit & 1}
            stable = all(p[d] == d for p in permutations(range(4))
                         if p[c] == c and all(p[s] == s for s in seen))
            assert stable == (seen == {a, b})
            palette_controls.append(dict(seen=sorted(seen), fixed_root=c,
                                         forced_leaf_neighbor=d, invariant=stable))
        # A positive leaf triangle, whose outgoing active bridge is negative,
        # has one common actual boundary neighbour at all three vertices.
        for forbidden_boundary in (a, b):
            other = ({a, b} - {forbidden_boundary}).pop()
            for root, opposite in ((c, d), (d, c)):
                private = set(range(4)) - {root, forbidden_boundary}
                cut = set(range(4)) - {forbidden_boundary}
                assert private == {opposite, other}
                assert cut == private | {root} and not private & {root}
    leaf_counts = []
    for sizes in product((3, 5, 7), repeat=2):
        contacts = sum(n - 1 for n in sizes)
        admissible = contacts <= 4
        assert admissible == (sizes == (3, 3))
        leaf_counts.append(dict(two_original_leaf_cycle_lengths=sizes,
                                necessary_private_contacts=contacts, admissible=admissible))
    records = []
    for start in range(5):
        for landing in range(5):
            if landing in (start, (start + 1) % 5):
                continue
            for subdivide in (False, True):
                records.append(skeleton('leaf_bridge', start, landing, 1, subdivide))
                for length in (3, 5, 7):
                    records.append(skeleton('inactive_leaf_cycle', start, landing, length, subdivide))
                for length in (1, 3, 5, 7):
                    records.append(skeleton('two_active_leaf_triangles', start, landing, length, subdivide))
    # A genuine full ordered four-contact relation on the degree-four
    # two-triangle control, before fixing its common root colour.
    vertices = tuple(range(5, 11))
    extra = [(5, 6), (6, 7), (5, 7), (8, 9), (9, 10), (8, 10), (7, 8),
             (0, 5), (0, 6), (0, 7), (1, 8), (1, 9), (1, 10)]
    relation_controls = []
    for a, b in permutations(range(4), 2):
        fs = colorings(vertices, extra, {0: a, 1: b})
        relation = sorted({tuple(f[v] for v in (5, 6, 9, 10)) for f in fs})
        forbidden = set.intersection(*(set(t) for t in relation))
        assert forbidden == set(range(4)) - {a, b}
        witnesses = [next([f[v] for v in vertices] for f in fs
                          if tuple(f[v] for v in (5, 6, 9, 10)) == t) for t in relation]
        relation_controls.append(dict(boundary_edge_colors=[a, b], port_order=[5, 6, 9, 10],
                                      relation=relation, full_internal_witnesses=witnesses,
                                      forbidden=sorted(forbidden)))
    negative = []
    base = records[0]
    edges, bags = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    for name, bad_edges, bad_bags in (
            ('missing_leaf_bridge', edges - {('v', 'w')}, bags),
            ('missing_leaf_boundary_attachment', edges - {('b0', 'v')}, bags),
            ('overlapping_branch_sets', edges, [bags[0] | bags[1]] + bags[1:])):
        try:
            verify_minor(bad_edges, bad_bags)
        except AssertionError:
            negative.append(name)
        else:
            raise AssertionError(name)
    paths = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
             ROOT / 'scripts/c5_single_spoke_two_two_minor.py']
    return dict(schema=1, scope='four contacts, adjacent actual support, unseen pair exclusion',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in paths}, leaf_bridge_palette_controls=palette_controls,
                active_leaf_count_controls=leaf_counts, minor_controls=records,
                full_ordered_relation_controls=relation_controls, negative_controls=negative,
                summary=dict(leaf_bridge_palette_controls=len(palette_controls),
                    active_leaf_count_controls=len(leaf_counts), original_minor_controls=len(records),
                    four_contact_relations=len(relation_controls),
                    relation_tuples=sum(len(r['relation']) for r in relation_controls),
                    remaining=0, graph_enumeration=False, disk_realizability_claimed=False,
                    new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
