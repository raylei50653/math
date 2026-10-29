#!/usr/bin/env python3
"""A complete same-graph Kempe countermodel for a proposed B5 strengthening.

The marked pentagram 5-pole is NOT a plane disk. Its complete Tait-coloring
space realizes the 932 B5 certificate, has noncrossing boundary pairings in
every state, and is closed under all actual component switches. The capped
graph has no genus-zero rotation system. Standard library only.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_dual_path_surgery as surgery
import four_color_counts_cone_verification as cone


ROOT = Path(__file__).resolve().parents[1]
PAIRS = tuple(combinations((1, 2, 3), 2))
# Edge i is the marked terminal edge at port i. Edge 5+i is internal.
EDGES = tuple((i, 5 + i) for i in range(5)) + tuple((i, (i + 2) % 5) for i in range(5))


def colorings():
    result = []
    for internal in product((1, 2, 3), repeat=5):
        labels = [None] * 5 + list(internal)
        for v in range(5):
            colors = [labels[e] for e, vs in enumerate(EDGES) if v in vs and e >= 5]
            if len(set(colors)) != 2:
                break
            labels[v] = 6 - sum(colors)
        else:
            assert all({labels[e] for e, vs in enumerate(EDGES) if v in vs} == {1, 2, 3}
                       for v in range(5))
            result.append(tuple(labels))
    return tuple(sorted(result))


def signed_pairing(labels, pair):
    matching, cycles = surgery.matching(EDGES, labels, pair, 5)
    assert cycles == 0
    return tuple((a, b, -1 if labels[a] == labels[b] else 1) for a, b in matching)


def signature_face(states):
    words = tuple(w for w in product((1, 2, 3), repeat=5)
                  if all(w.count(c) % 2 == 1 for c in (1, 2, 3)))
    rows = tuple((w, p) for w in words for p in PAIRS)
    sigs = tuple(cone.signatures(5))
    by_word = {w: [s for s in states if s[:5] == w] for w in words}
    counts = {w: len(ss) for w, ss in by_word.items()}
    assert Counter(counts.values()) == {0: 30, 1: 30}
    # Extract actual signed path data on this ONE graph; no independent
    # choices of compatible matchings or abstract weights are made.
    actual = {(w, p): Counter(signed_pairing(s, p) for s in by_word[w]) for w, p in rows}
    weights, incidence, inactive, forbidden = {}, {}, [], []
    for sig in sigs:
        ids = [i for i, (w, p) in enumerate(rows) if cone.compatible(w, p, sig)]
        incidence[sig] = ids
        if not ids:
            inactive.append(sig)
            weights[sig] = 0  # unobservable coordinates, not claimed unique
            continue
        values = {actual[rows[i]][sig] for i in ids}
        assert len(values) == 1
        weights[sig] = values.pop()
        if any(counts[rows[i][0]] == 0 for i in ids):
            assert weights[sig] == 0
            forbidden.append(sig)
    positive = [sig for sig in sigs if weights[sig]]
    assert len(inactive) == 31 and len(forbidden) == 20 and len(positive) == 10
    old = cone.standard_b5_certificate()
    assert sorted(positive) == sorted(tuple(tuple(p) for p in item['signature'])
                                      for item in old['weights'])
    for w, p in rows:
        assert sum(weights[sig] for sig in sigs if cone.compatible(w, p, sig)) == counts[w]
    # Independent effective-face proof: zero rows kill 20 active signatures;
    # each positive row then contains exactly ONE surviving signature.
    # Equality propagation in the incidence graph forces all positive x's and
    # all ten effective y's to share one scalar. The 31 inactive y's are ignored.
    adjacency = {('x', w): set() for w in words if counts[w]}
    for sig in positive:
        adjacency['y', sig] = set()
        for i in incidence[sig]:
            w = rows[i][0]
            adjacency['x', w].add(('y', sig))
            adjacency['y', sig].add(('x', w))
    assert all(sum(cone.compatible(w, p, sig) for sig in positive) == counts[w]
               for w, p in rows)
    root = min(adjacency)
    seen, queue, tree = {root}, deque([root]), []
    while queue:
        u = queue.popleft()
        for v in sorted(adjacency[u]):
            if v not in seen:
                seen.add(v)
                queue.append(v)
                tree.append([u, v])
    assert len(seen) == len(adjacency) == 40 and len(tree) == 39
    # Controls: actually alter one coordinate, replay all 180 equations, and
    # retain a concrete failed equality rather than only an incidence test.
    negative_controls = []
    for kind, coordinate in sorted(adjacency):
        changed_counts, changed_weights = dict(counts), dict(weights)
        if kind == 'x':
            changed_counts[coordinate] += 1
        else:
            changed_weights[coordinate] += 1
        failures = []
        for i, (word, pair) in enumerate(rows):
            lhs = changed_counts[word]
            rhs = sum(changed_weights[sig] for sig in sigs if cone.compatible(word, pair, sig))
            if lhs != rhs:
                failures.append(dict(equation=i, word=word, pair=pair, lhs=lhs, rhs=rhs))
        assert failures
        negative_controls.append(dict(coordinate=(kind, coordinate), increment=1,
                                      failed_equations=len(failures), first_failure=failures[0]))
    return dict(parity_words=len(words), rows=len(rows),
                positive_words=sum(counts.values()), effective_signatures=30,
                zero_forced_effective_signatures=len(forbidden),
                positive_effective_signatures=len(positive),
                unobservable_signatures=len(inactive),
                actual_common_weights=[dict(signature=sig, weight=weights[sig]) for sig in positive],
                equal_value_component_nodes=len(adjacency), equality_spanning_tree=tree,
                coordinate_perturbation_negative_controls=negative_controls,
                conclusion='The projected 932 face is the known t-ray; only effective y coordinates are unique.')


def automaton(states):
    index = {s: i for i, s in enumerate(states)}
    transitions = []
    neighbors = {i: set() for i in range(len(states))}
    for i, labels in enumerate(states):
        for pair in PAIRS:
            matching, cycles = surgery.matching(EDGES, labels, pair, 5)
            assert cycles == 0
            for strand in surgery.pair_strands(EDGES, labels, pair):
                assert strand['ends']
                target = tuple(sum(pair) - c if e in strand['edges'] else c
                               for e, c in enumerate(labels))
                assert target in index
                assert tuple(sum(pair) - c if e in strand['edges'] else c
                             for e, c in enumerate(target)) == labels
                prediction, cut = surgery.ordered_surgery(EDGES, labels, 5, pair, strand)
                assert surgery.matching(EDGES, target, pair, 5) == (matching, cycles)
                for system, answer in prediction.items():
                    assert surgery.matching(EDGES, target, system, 5) == answer
                for system in PAIRS:
                    # This assertion checks noncrossing boundary pairings and
                    # zero cycle counts, including both changed systems.
                    assert surgery.matching(EDGES, target, system, 5)[1] == 0
                j = index[target]
                neighbors[i].add(j)
                transitions.append(dict(source=i, target=j, pair=pair,
                                        path_edge_ids=strand['edges'],
                                        boundary_ends=[v - 5 for v in strand['ends']], cut=cut))
    assert len(transitions) == 150
    for row in transitions:
        reverse = [r for r in transitions if r['source'] == row['target']
                   and r['target'] == row['source'] and r['pair'] == row['pair']
                   and set(r['path_edge_ids']) == set(row['path_edge_ids'])]
        assert len(reverse) == 1
    reached, queue = {0}, deque([0])
    while queue:
        for j in sorted(neighbors[queue.popleft()]):
            if j not in reached:
                reached.add(j)
                queue.append(j)
    assert len(reached) == 30 and all(len(ns) == 5 for ns in neighbors.values())
    return dict(states=[dict(id=i, edge_colors=s, boundary_word=s[:5],
                             integrated_boundary=cone.integrate(s[:5]),
                             systems=[dict(pair=p, signature=signed_pairing(s, p), cycles=0)
                                      for p in PAIRS]) for i, s in enumerate(states)],
                directed_transitions=len(transitions), undirected_transitions=len(transitions) // 2,
                noncrossing_system_checks=3 * len(states),
                surgery_system_checks=3 * len(transitions), mixed_system_predictions=2 * len(transitions),
                involution_checks=len(transitions), connected_states=len(reached),
                transitions=transitions,
                closure='All components of all three systems are enumerated. Closure for arbitrary finite histories follows by induction.')


def capped_rotations():
    # A disk embedding with the literal port order 0,1,2,3,4 would remain
    # planar after adding these five edges just outside the disk boundary.
    edges = EDGES + tuple((5 + i, 5 + (i + 1) % 5) for i in range(5))
    adjacency = {v: sorted(w if u == v else u for u, w in edges if v in (u, w))
                 for v in range(10)}
    assert all(len(ns) == 3 for ns in adjacency.values())
    # Independent short Euler obstruction. For every edge, find a shortest
    # alternate endpoint path after deleting that edge. Their minimum lengths
    # prove girth five; their existence also proves that there are no bridges.
    shortest_cycles = []
    for e, (a, b) in enumerate(edges):
        removed = frozenset((a, b))
        previous, queue = {a: None}, deque([a])
        while queue and b not in previous:
            u = queue.popleft()
            for v in adjacency[u]:
                if frozenset((u, v)) != removed and v not in previous:
                    previous[v] = u
                    queue.append(v)
        assert b in previous
        path, current = [], b
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        shortest_cycles.append(dict(edge=e, shortest_alternate_path=path,
                                    cycle_length=len(path)))
    assert {item['cycle_length'] for item in shortest_cycles} == {5}
    # A hypothetical plane embedding has F=E-V+2=7. Each face walk has
    # length >=5, while their total length is 2E=30: 35 <= 30 is impossible.
    euler_obstruction = dict(vertices=10, edges=15, connected=True, bridgeless=True,
                             girth=5, shortest_cycles=shortest_cycles,
                             hypothetical_planar_faces=7, minimum_total_face_length=35,
                             actual_total_face_length=30)
    darts = tuple(d for e in edges for d in (e, e[::-1]))
    histogram = Counter()
    minimum = None
    records = []
    for bits in product((0, 1), repeat=10):
        rotations = {v: (ns if bits[v] == 0 else ns[::-1]) for v, ns in adjacency.items()}
        successor = {(u, v): (v, rotations[v][(rotations[v].index(u) + 1) % 3])
                     for u, v in darts}
        seen, faces = set(), []
        for dart in darts:
            if dart in seen:
                continue
            face, current = [], dart
            while current not in seen:
                seen.add(current)
                face.append(current)
                current = successor[current]
            assert current == dart
            faces.append(face)
        chi = 10 - 15 + len(faces)
        assert (2 - chi) % 2 == 0
        genus = (2 - chi) // 2
        histogram[genus] += 1
        records.append(dict(rotation_bits=bits, face_count=len(faces), genus=genus))
        if minimum is None or genus < minimum['genus']:
            minimum = dict(rotation_bits=bits, genus=genus, face_darts=faces)
    assert dict(histogram) == {1: 40, 2: 664, 3: 320}
    # Positive topological control: put the internal cycle in the same port
    # order instead. Its identity terminal order admits a plane rotation.
    polygon_edges = tuple((i, 5 + i) for i in range(5)) + tuple((i, (i + 1) % 5) for i in range(5))
    # Explicit oriented pentagonal-prism faces certify a sphere embedding.
    prism_faces = [tuple(range(5)), tuple(reversed(range(5, 10)))]
    prism_faces += [(i, 5 + i, 5 + ((i + 1) % 5), (i + 1) % 5) for i in range(5)]
    expected_darts = Counter(d for e in polygon_edges + edges[-5:] for d in (e, e[::-1]))
    observed_darts = Counter((f[i], f[(i + 1) % len(f)]) for f in prism_faces for i in range(len(f)))
    assert observed_darts == expected_darts and 10 - 15 + len(prism_faces) == 2
    return dict(capped_edges=edges, graph='Petersen graph with the literal terminal order',
                independent_euler_obstruction=euler_obstruction,
                rotations=len(records), genus_histogram=dict(sorted(histogram.items())),
                minimum_genus=minimum, rotation_certificates=records,
                planar_order_positive_control_faces=prism_faces,
                conclusion='No common disk embedding with terminal order 0,1,2,3,4 exists.')


def report():
    states = colorings()
    assert len(states) == 30 and len({s[:5] for s in states}) == 30
    support = {cone.ck.normalize(cone.integrate(s[:5])) for s in states}
    mask = sum(1 << cone.ck.patterns(5).index(b) for b in support)
    assert mask == 932
    dependencies = (Path(__file__), ROOT / 'scripts/four_color_counts_cone_verification.py',
                    ROOT / 'scripts/ck_kempe_obstruction.py', ROOT / 'scripts/c5_dual_path_surgery.py',
                    ROOT / 'scripts/c5_kempe_connectivity.py', ROOT / 'scripts/c5_adjacent_singleton_counts.py',
                    ROOT / 'scripts/c5_kempe_screen.py')
    return dict(scope='Non-disk same-graph countermodel; not a planar realization or 932 exclusion.',
                vertices=dict(internal=list(range(5)), terminals=list(range(5, 10))),
                edges=EDGES, support_mask=mask, support_patterns=sorted(support),
                standard_b5=signature_face(states), complete_kempe_automaton=automaton(states),
                common_embedding_obstruction=capped_rotations(),
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--check', type=Path, help='Compare replay with an existing exact certificate.')
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert args.check.read_text() == payload, 'Certificate differs from exact replay'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(dict(support_mask=result['support_mask'], colorings=30,
                          directed_transitions=150, genus_histogram=result['common_embedding_obstruction']['genus_histogram']),
                     sort_keys=True))


if __name__ == '__main__':
    main()
