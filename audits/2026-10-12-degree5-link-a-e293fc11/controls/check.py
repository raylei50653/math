#!/usr/bin/env python3
"""Read-only, complete replay of finite degree-5 link topology controls.

Use --write only for exclusive creation. --check never changes a certificate.
The seed changes the independent coloring search order, not its semantics.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

import networkx as nx

B = ('a', 'b', 'c', 'd', 'e')
COLORS = tuple(range(4))
REPS = [
    ('m0-annulus', ('x', 'y', 'z', 'w', 't')),
    ('m1-pin', ('a', 'x', 'y', 'z', 'w')),
    ('m2-shared-edge', ('a', 'b', 'x', 'y', 'z')),
    ('m2-C4-C6', ('a', 'x', 'c', 'y', 'z')),
    ('m2-C5-C5', ('a', 'x', 'y', 'c', 'z')),
    ('m3-consecutive', ('a', 'b', 'c', 'x', 'y')),
    ('m3-edge-isolated', ('a', 'b', 'x', 'd', 'y')),
    ('m4', ('a', 'b', 'c', 'd', 'x')),
    ('m5', B),
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(u, v):
    return tuple(sorted((u, v)))


def cycle_edges(cycle):
    return {edge(u, v) for u, v in zip(cycle, cycle[1:] + cycle[:1])}


def normalize(colors):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in colors)


PATTERNS = sorted({normalize(c) for c in itertools.product(COLORS, repeat=5)
                   if all(c[i] != c[(i + 1) % 5] for i in range(5))})


def gap_signature(pairs):
    if not pairs:
        return ()
    candidates = []
    for sequence in (list(pairs), list(reversed(pairs))):
        candidates.extend(tuple(sequence[i:] + sequence[:i]) for i in range(len(sequence)))
    return min(candidates)


def cyclic_path(cycle, start, end):
    i, j = cycle.index(start), cycle.index(end)
    length = (j - i) % len(cycle)
    return tuple(cycle[(i + k) % len(cycle)] for k in range(length + 1))


def geometry(name, link):
    contacts = tuple(v for v in B if v in link)
    m = len(contacts)
    edges = cycle_edges(B) | cycle_edges(link) | {edge('v', x) for x in link}
    faces = [B] + [('v', link[(i + 1) % 5], link[i]) for i in range(5)]
    regions = []
    if m == 0:
        edges.add(edge('a', 'x'))
        walk = ('a', 'e', 'd', 'c', 'b', 'a') + link + ('x',)
        faces.append(walk)
        regions.append({'name': 'annulus', 'topology': 'annulus before the diagnostic bridge is cut',
                        'boundary_components': [tuple(reversed(B)), link],
                        'cellular_face_walk_after_bridge': walk,
                        'owned_extra_edges': [('a', 'x')], 'shared_pins': []})
    elif m == 1:
        require(link[0] == 'a', 'canonical one-contact origin changed')
        walk = ('a', 'e', 'd', 'c', 'b') + link
        faces.append(walk)
        regions.append({'name': 'pin_region', 'topology': 'non-Jordan closed region with repeated boundary pin',
                        'boundary_walk': walk, 'owned_extra_edges': [], 'shared_pins': ['a']})
    else:
        for i, start in enumerate(contacts):
            end = contacts[(i + 1) % m]
            bp, lp = cyclic_path(B, start, end), cyclic_path(link, start, end)
            require((len(bp) == 2) == (len(lp) == 2), 'unphysical shared edge orientation')
            if len(bp) == 2:
                regions.append({'name': f'shared_edge_{i}', 'topology': 'shared boundary edge; no open region',
                                'edge': [start, end], 'shared_pins': [start, end], 'owned_extra_edges': []})
            else:
                walk = tuple(reversed(bp)) + lp[1:-1]
                require(len(set(walk)) == len(walk), 'cap boundary is not simple')
                faces.append(walk)
                regions.append({'name': f'cap_{i}', 'topology': 'simple disk',
                                'B_arc': bp, 'L_arc': lp, 'boundary_walk': walk,
                                'length': len(walk), 'shared_pins': [start, end], 'owned_extra_edges': []})
    vertices = tuple(B) + tuple(x for x in link if x not in B) + ('v',)
    rotations = validate_embedding(vertices, edges, faces)
    require({w for e in edges if 'v' in e for w in e if w != 'v'} == set(link), 'center degree differs')
    require({e for e in edges if set(e) <= set(link)} == cycle_edges(link), 'link is not induced')
    require({e for e in edges if set(e) <= set(B)} == cycle_edges(B), 'outer boundary is not chordless')
    degrees = {x: sum(x in e for e in edges) for x in B}
    common_edges = cycle_edges(B) & cycle_edges(link)
    forced_degree3 = [x for x in contacts if sum(x in e for e in common_edges) == 2]
    return {'name': name, 'B': B, 'v': 'v', 'L': link, 'm': m, 'vertices': vertices,
            'edges': sorted(edges), 'oriented_faces_outer_first': faces, 'rotations': rotations,
            'regions': regions, 'shared_edges': sorted(common_edges), 'boundary_degrees_in_skeleton': degrees,
            'source_forced_degree3_vertices': forced_degree3,
            'private_patch_components': [], 'center_component_owner': {'vertices': ['v'], 'owner': 'star'},
            'annular_bridge_owner': {'edge': ['a', 'x'], 'owner': 'annulus'} if m == 0 else None,
            'interior_vertex_count': len(vertices) - 5,
            'global_minimal_catalogue_outside_source': 'not triggered',
            'target_933_941_source': 'not triggered',
            'scope': 'Literal topology skeleton only; caps have no private vertices. No global-minimality assertion.'}


def validate_embedding(vertices, edges, faces):
    darts = [(u, v) for f in faces for u, v in zip(f, f[1:] + f[:1])]
    expected = {(u, v) for a, b in edges for u, v in ((a, b), (b, a))}
    require(len(darts) == len(set(darts)) and set(darts) == expected, 'face darts incomplete or repeated')
    require(len(vertices) - len(edges) + len(faces) == 2, 'wrong embedding Euler characteristic')
    rotations = {}
    for vertex in vertices:
        following = {}
        for f in faces:
            for i, x in enumerate(f):
                if x != vertex:
                    continue
                previous, nxt = f[i - 1], f[(i + 1) % len(f)]
                require(previous not in following, 'repeated predecessor in rotation')
                following[previous] = nxt
        neighbors = {w for e in edges if vertex in e for w in e if w != vertex}
        require(set(following) == set(following.values()) == neighbors, 'rotation omits neighbor')
        current = min(neighbors)
        rotation = []
        while current not in rotation:
            rotation.append(current)
            current = following[current]
        require(current == rotation[0] and set(rotation) == neighbors, 'pinched vertex rotation')
        rotations[vertex] = rotation
    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)
    require(nx.is_connected(graph), 'skeleton is disconnected')
    graph.add_edges_from(('outer_apex', x) for x in B)
    require(nx.check_planarity(graph)[0], 'independent outer-apex planarity failed')
    return rotations


def independent_lifts(vertices, edges, outer, seed):
    """Constraint backtracking, independent of product enumeration and star join."""
    rng = random.Random(seed)
    order = list(vertices[5:])
    rng.shuffle(order)
    colors = list(COLORS)
    rng.shuffle(colors)
    neighbors = {x: {w for e in edges if x in e for w in e if w != x} for x in vertices}
    fixed = dict(zip(B, outer))
    found = []

    def visit(index):
        if index == len(order):
            found.append(tuple(fixed[x] for x in vertices[5:]))
            return
        x = order[index]
        for color in colors:
            if any(fixed.get(y) == color for y in neighbors[x]):
                continue
            fixed[x] = color
            visit(index + 1)
            del fixed[x]

    visit(0)
    return sorted(found)


def relations(graph, seed):
    vertices = graph['vertices']
    private = vertices[5:-1]
    edges = graph['edges']
    outside_edges = [e for e in edges if 'v' not in e]
    rows = []
    for outer in PATTERNS:
        interface_ok = []
        center_masks = []
        joined = []
        for assignment in itertools.product(COLORS, repeat=len(private)):
            coloring = dict(zip(B, outer))
            coloring.update(zip(private, assignment))
            proper = all(coloring[u] != coloring[v] for u, v in outside_edges)
            interface_ok.append('1' if proper else '0')
            mask = 0
            if proper:
                for color in COLORS:
                    if all(color != coloring[x] for x in graph['L']):
                        mask |= 1 << color
                        joined.append(assignment + (color,))
            center_masks.append(mask)
        direct = []
        for lift in itertools.product(COLORS, repeat=len(vertices) - 5):
            coloring = dict(zip(vertices, outer + lift))
            if all(coloring[u] != coloring[v] for u, v in edges):
                direct.append(lift)
        require(joined == direct, 'star join differs from direct full-graph enumeration')
        require(direct == independent_lifts(vertices, edges, outer, seed), 'independent complete fibres differ')
        rows.append({'outer': outer, 'interface_edge_ok': ''.join(interface_ok),
                     'center_color_masks': center_masks, 'full_lifts': direct})
    return {'outer_pattern_order': PATTERNS, 'interface_order': tuple(B) + private,
            'private_interface_assignment_order': 'itertools.product((0,1,2,3), repeat=len(private_interface_order)); lexicographic',
            'private_interface_order': private, 'full_lift_order': private + ('v',),
            'color_mask_encoding': 'bit c records center color c; zero records an empty fiber; interface_edge_ok distinguishes improper assignments',
            'all_ten_rows': rows, 'Sigma': sum(1 << i for i, row in enumerate(rows) if row['full_lifts']),
            'full_join_and_independent_search': 'triggered and holds'}


def transport_to_rep(physical_link, reps):
    """One literal global vertex map transports both cycles; never color-normalize a patch."""
    for name, link in reps:
        if len(set(link) & set(B)) != len(set(physical_link) & set(B)):
            continue
        for direction in (1, -1):
            for bshift in range(5):
                mapping = {B[i]: B[(bshift + direction * i) % 5] for i in range(5)}
                for lshift in range(5):
                    trial = dict(mapping)
                    valid = True
                    for i, x in enumerate(link):
                        target = physical_link[(lshift + direction * i) % 5]
                        if x in B and trial[x] != target or x not in B and target in B:
                            valid = False
                            break
                        trial[x] = target
                    if valid and len(set(trial.values())) == len(trial):
                        trial['v'] = 'v'
                        return {'representative': name, 'global_vertex_map': trial,
                                'simultaneous_orientation': direction,
                                'B_start_shift': bshift, 'L_start_shift': lshift}
    raise ValueError('legal contact map has no simultaneous representative transport')


def contact_enumeration():
    candidates = []
    base_records = [(0, (), (), 0)]
    for m in range(1, 6):
        base_records.extend((m, bs, ls, shift)
                            for bs in itertools.combinations(range(5), m)
                            for ls in itertools.combinations(range(5), m)
                            for shift in range(m))
    counts = collections.Counter()
    by_type = collections.Counter()
    for m, bs, ls, shift in base_records:
        ordered = ls[shift:] + ls[:shift]
        physical_link = [f'q{i}' for i in range(5)]
        for bi, li in zip(bs, ordered):
            physical_link[li] = B[bi]
        pairs = [((bs[(i + 1) % m] - bs[i]) % 5, (ordered[(i + 1) % m] - ordered[i]) % 5)
                 for i in range(m)] if m >= 2 else []
        legal = all((p == 1) == (q == 1) for p, q in pairs)
        trans = transport_to_rep(physical_link, REPS) if legal else None
        for sign in (1, -1):
            raw_link = [physical_link[(sign * i) % 5] for i in range(5)]
            record = {'m': m, 'B': B, 'raw_L': raw_link,
                      'raw_L_orientation_relative_to_B': sign, 'physical_L': physical_link,
                      'contact_gap_pairs_in_B_order': pairs,
                      'topologically_legal_induced_chordless_contact': legal,
                      'status': 'triggered and holds' if legal else 'not triggered',
                      'rejection_reason': None if legal else 'a unit arc is paired with a nonunit arc: incompatible shared edge orientation or an induced/chordless violation; this encoding violates the incidence antecedents and is not a mathematical counterexample',
                      'transport': trans}
            candidates.append(record)
            counts[f'm{m}_{"legal" if legal else "rejected"}'] += 1
            if trans:
                by_type[trans['representative']] += 1
    require(len(candidates) == 1262, 'raw oriented candidate count changed')
    require(sum(by_type.values()) == 362 and len(by_type) == 9, 'complete legal contact counts changed')
    return {'enumeration_domain': 'All cyclic-order-preserving contacts between two oriented named 5-cycles, with both raw L orientations retained; m=0 has one incidence type per raw orientation.',
            'base_orientation_candidate_count': len(base_records), 'both_raw_orientation_candidate_count': len(candidates),
            'counts': dict(sorted(counts.items())), 'representative_transport_counts': dict(sorted(by_type.items())),
            'records': candidates,
            'scope': 'Finite classification of cycle incidence encodings. Paper Jordan arguments justify that these encodings cover nested source links.'}


def replay(seed):
    require(len(PATTERNS) == 10, 'outer ten rows changed')
    controls = []
    for name, link in REPS:
        graph = geometry(name, link)
        graph['relations'] = relations(graph, seed)
        controls.append(graph)
    return {'schema': 'degree5-link-taskA-topology-controls-v2',
            'colors': COLORS, 'pattern_order': PATTERNS,
            'contact_enumeration': contact_enumeration(), 'controls': controls,
            'full_source_identity': 'not triggered', 'target_933_941': 'not triggered',
            'universal_topology_proof': 'separate paper obligation', 'Lean': 'not executed',
            'independent_methods': ['literal product full graph enumeration', 'seeded constraint backtracking', 'complete named interface star join', 'oriented face/rotation sphere check', 'NetworkX independent apex planarity']}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(data):
    return json.loads(data, object_pairs_hook=unique_object)


def canonical(data):
    return (json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', type=Path)
    mode.add_argument('--check', type=Path)
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    try:
        expected = canonical(replay(args.seed))
        path = args.write or args.check
        if args.write:
            with path.open('xb') as output:
                output.write(expected)
            action = 'created'
        else:
            actual = path.read_bytes()
            require(read_json(actual) == read_json(expected), 'certificate differs from complete replay')
            require(actual == expected, 'certificate bytes are not canonical')
            action = 'checked'
        print(f'PASS: {action} {path}; SHA256={hashlib.sha256(expected).hexdigest()}; 9 literal skeletons; 362 legal oriented records; full ten-row fibers')
        return 0
    except (ValueError, KeyError, OSError, TypeError, json.JSONDecodeError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
