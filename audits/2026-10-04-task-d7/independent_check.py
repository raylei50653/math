#!/usr/bin/env python3
"""D7 independent fixed-domain audit; imports only the standard library.

Re-derive the 9+243 actual labelled forms from degrees and support subset
234, then compare complete literal colouring relations to saved DATA.
Also check the two specified E1 graphs, without replaying E1 enumeration.
No audited checker or helper is imported. Outputs stay in this directory.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))


def normalized(edges):
    return frozenset(tuple(sorted(e)) for e in edges)


def rows_from_scratch():
    # Canonical restricted-growth colour names, followed by lexicographic order.
    rows = []
    for row in product(range(4), repeat=5):
        if row[0] != 0 or any(row[i] > 1 + max(row[:i]) for i in range(1, 5)):
            continue
        if all(row[a] != row[b] for a, b in FRAME):
            rows.append(row)
    assert len(rows) == 10
    return rows


def colourings(edges, row, private, root_pin=None):
    """Fixed numerical vertex order DFS, keeping every full literal assignment."""
    private = tuple(sorted(private))
    n = max((4,) + private) + 1
    neighbors = [[] for _ in range(n)]
    included = set(range(5)) | set(private)
    for a, b in edges:
        if a in included and b in included:
            neighbors[a].append(b)
            neighbors[b].append(a)
    colours = [-1] * n
    colours[:5] = row
    if not all(colours[a] != colours[b] for a, b in FRAME):
        return []
    answer = []

    def extend(i):
        if i == len(private):
            answer.append(tuple(colours))
            return
        v = private[i]
        candidates = (root_pin,) if v == 5 and root_pin is not None else range(4)
        for c in candidates:
            if all(colours[w] != c for w in neighbors[v]):
                colours[v] = c
                extend(i + 1)
                colours[v] = -1

    extend(0)
    return answer


def sigma(edges, private, rows):
    return sum(1 << i for i, row in enumerate(rows) if colourings(edges, row, private))


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    todo = [next(iter(vertices))]
    seen = set(todo)
    while todo:
        u = todo.pop()
        for a, b in edges:
            v = b if a == u else a if b == u else None
            if v in vertices and v not in seen:
                seen.add(v)
                todo.append(v)
    return seen == vertices


def verify_witness(witness, edges, row, order=None):
    if isinstance(witness, dict):
        f = {int(v): c for v, c in witness.items()}
    else:
        f = dict(zip(order or range(len(witness)), witness))
    assert all(c in range(4) for c in f.values())
    assert [f[i] for i in range(5)] == list(row)
    assert all(f[a] != f[b] for a, b in edges if a in f and b in f)
    return f


def verify_minor(edges, bags):
    bags = [set(bag) for bag in bags]
    assert len(bags) == 5
    assert all(connected(bag, edges) for bag in bags)
    assert all(not (a & b) for a, b in combinations(bags, 2))
    crosses = []
    for i, j in combinations(range(5), 2):
        witnesses = sorted((a, b) for a, b in edges
                           if (a in bags[i] and b in bags[j]) or
                           (b in bags[i] and a in bags[j]))
        assert witnesses, (i, j, bags)
        crosses.append({'bags': [i, j], 'edge': witnesses[0]})
    return crosses


def independent_forms():
    # These are the two paper forms, BEFORE colour checks or planarity filtering.
    interiors = [((5, 6, 7), ((5, 6), (5, 7), (6, 7))),
                 ((5, 6, 7, 8, 9, 10),
                  ((5, 6), (5, 7), (6, 7), (6, 8), (8, 9), (8, 10), (9, 10)))]
    for vertices, inside in interiors:
        base = FRAME | normalized(inside) | {(0, 5), (4, 5)}
        private = vertices[1:]
        needed = [4 - sum(v in e for e in base) for v in private]
        assert needed == ([2, 2] if len(private) == 2 else [1, 2, 1, 2, 2])
        for attachments in product(*(tuple(combinations((2, 3, 4), k)) for k in needed)):
            edges = base | {(b, v) for v, at in zip(private, attachments) for b in at}
            assert all(sum(v in e for e in edges) == 4 for v in vertices)
            yield vertices, frozenset(edges)


def check_252(rows):
    path = REPO / 'artifacts/c5_excess_one_e2_951_unary_core/observations.json'
    saved = json.loads(path.read_text())
    assert [list(row) for row in rows] == saved['pattern_order']
    lookup = {normalized(m['edges']): m for m in saved['models']}
    assert len(lookup) == len(saved['models']) == 252
    t4 = sum(1 << i for i, row in enumerate(rows) if len(set(row)) == 4)
    q, p = (0, 1, 2, 0, 2), (0, 1, 0, 1, 2)
    counts = Counter()
    family_masks = {3: Counter(), 6: Counter()}
    failures = []
    seen = set()
    for vertices, edges in independent_forms():
        assert edges in lookup and edges not in seen
        seen.add(edges)
        model = lookup[edges]
        family_masks[len(vertices)][sigma(edges, vertices, rows)] += 1
        full = [colourings(edges, row, vertices) for row in rows]
        actual_mask = sum(1 << i for i, assignments in enumerate(full) if assignments)
        assert actual_mask == model['complete_sigma']
        relevant = not full[rows.index(q)] and actual_mask & t4 == t4
        assert relevant == (model['q_rejected'] and model['accepts_T4'])
        counts['forms'] += 1
        counts['full_row_queries'] += len(rows)
        if not relevant:
            continue
        counts['q_rejected_T4'] += 1
        for row, assignments, data in zip(rows, full, model['rows']):
            actual_joint = {tuple(f[v] for v in (5, 6, 7)) for f in assignments}
            assert actual_joint == set(map(tuple, data['complete_ordered_root_relation']))
            assert len(assignments) == data['root_full_extension_count']
            binary = colourings(edges, row, vertices[1:])
            binary_joint = {tuple(f[v] for v in (6, 7)) for f in binary}
            assert binary_joint == set(map(tuple, data['complete_ordered_binary_relation']))
            assert len(binary) == data['binary_full_extension_count']
            forbidden = {c for c in range(4) if all(c in t for t in binary_joint)}
            assert forbidden == set(data['binary_forbidden'])
            for witness in data['root_tuple_witnesses']:
                verify_witness(witness, edges, row)
                counts['saved_full_witnesses'] += 1
            for witness in data['binary_tuple_witnesses']:
                verify_witness(witness, edges, row, list(range(5)) + list(vertices[1:]))
                counts['saved_full_witnesses'] += 1
        assert {tuple(r['edge']) for r in model['q_critical_edge_witnesses']} == edges - FRAME
        for witness in model['q_critical_edge_witnesses']:
            smaller = edges - {tuple(witness['edge'])}
            verify_witness(witness['coloring'], smaller, q)
            assert colourings(smaller, q, vertices)
            counts['q_critical_edges'] += 1
        if colourings(edges, p, vertices, root_pin=3):
            assert 'p_root_D_extension' in model
            f = verify_witness(model['p_root_D_extension']['coloring'], edges, p)
            assert f[5] == 3
            counts['p_root_D'] += 1
        else:
            # Reconstruct bags from actual equal adjacent private attachments.
            u, v = (6, 7) if len(vertices) == 3 else (9, 10)
            su = {a for a in range(5) if tuple(sorted((a, u))) in edges}
            sv = {a for a in range(5) if tuple(sorted((a, v))) in edges}
            assert su == sv and len(su) == 2 and tuple(sorted(su)) in FRAME
            a, b = sorted(su)
            bags = [[u], [v], [a], [b], sorted((set(range(5)) | set(vertices)) - {u, v, a, b})]
            crosses = verify_minor(edges, bags)
            verify_minor(edges, model['original_K5_minor']['branch_sets'])
            failures.append({'model_id': model['model_id'], 'edges': sorted(edges),
                             'bags': bags, 'ten_edges': crosses})
            counts['K5'] += 1
    assert seen == set(lookup)
    assert counts['q_rejected_T4'] == 40 and counts['p_root_D'] == 36 and counts['K5'] == 4
    assert counts['q_critical_edges'] == 656
    return {'counts': dict(counts), 'family_sigma_histograms': family_masks,
            'four_K5': failures, 'source_sha256': sha256(path.read_bytes()).hexdigest()}


def rotation_faces(edges, rotation):
    rotation = {int(v): list(neighbors) for v, neighbors in rotation.items()}
    assert set(rotation) == {v for edge in edges for v in edge}
    for v, neighbors in rotation.items():
        assert len(neighbors) == len(set(neighbors))
        assert set(neighbors) == {a if b == v else b for a, b in edges if v in (a, b)}
    unseen = {(a, b) for a, b in edges} | {(b, a) for a, b in edges}
    faces = []
    while unseen:
        first = min(unseen)
        dart = first
        face = []
        while True:
            assert dart in unseen
            unseen.remove(dart)
            a, b = dart
            face.append(a)
            neighbors = rotation[b]
            dart = (b, neighbors[(neighbors.index(a) - 1) % len(neighbors)])
            if dart == first:
                break
        faces.append(face)
    assert len(rotation) - len(edges) + len(faces) == 2
    assert any(len(face) == 5 and set(face) == set(range(5)) for face in faces)
    return faces


def greedy_q_core(edges, private, row):
    core = edges
    omitted = []
    for edge in sorted(edges - FRAME):
        if not colourings(core - {edge}, row, private):
            core = core - {edge}
            omitted.append(edge)
    active = tuple(v for v in private if any(v in edge for edge in core))
    assert not colourings(core, row, active)
    assert all(colourings(core - {edge}, row, active) for edge in core - FRAME)
    degrees = {v: sum(v in edge for edge in core) for v in active}
    assert min(degrees.values()) >= 4
    return core, active, omitted, degrees


def check_e1(rows):
    path = REPO / 'artifacts/c5_excess_rejection_law/observations.json'
    data = json.loads(path.read_text())
    t4 = sum(1 << i for i, row in enumerate(rows) if len(set(row)) == 4)
    controls = []
    for level, mask in ((4, 951), (2, 935)):
        graph = data['exhaustive'][level]['minima_by_sigma'][str(mask)]
        edges = normalized(graph['all_edges'])
        private = tuple(v for v in graph['vertices'] if v >= 5)
        actual = sigma(edges, private, rows)
        assert actual == mask and actual & t4 == t4
        degrees = {v: sum(v in edge for edge in edges) for v in private}
        assert sum(d - 4 for d in degrees.values()) == 2
        assert connected(private, edges)
        assert {a for a in range(5) if any(a in edge and max(edge) >= 5 for edge in edges)} == set(range(5))
        faces = rotation_faces(edges, graph['embedding']['disk_rotation'])
        for i, witness in graph['accepted_colourings'].items():
            verify_witness(witness, edges, rows[int(i)])
        for certificate in graph['critical_edges']:
            smaller = edges - {tuple(certificate['edge'])}
            deletion_sigma = sigma(smaller, private, rows)
            assert deletion_sigma == certificate['sigma_after_deletion']
            assert deletion_sigma != mask and deletion_sigma | mask == deletion_sigma
            verify_witness(certificate['colouring'], smaller, certificate['pattern'])
        cores = []
        for i, row in enumerate(rows):
            if (mask >> i) & 1:
                continue
            core, active, omitted, core_degrees = greedy_q_core(edges, private, row)
            cores.append({'row_index': i, 'row': row, 'core_edges': sorted(core),
                          'active_private': active, 'omitted_edges': omitted,
                          'private_degrees': core_degrees, 'core_sigma': sigma(core, active, rows)})
        concrete_failures = []
        if mask == 951:
            # The high-degree root has SIX incidences: deleting a capacity-two
            # component can leave degree four. E2's one-incidence lemma fails.
            for component in ((6, 9), (7, 8)):
                contacts = tuple(v for v in component if (5, v) in edges)
                support = sorted({b for b in range(5) for v in component if (b, v) in edges})
                forbidden_by_row = {}
                for i in (3, 6):
                    tuples = {tuple(f[v] for v in contacts)
                              for f in colourings(edges, rows[i], component)}
                    forbidden_by_row[i] = sorted(c for c in range(4) if all(c in t for t in tuples))
                concrete_failures.append({'component': component, 'capacity': len(contacts),
                                          'actual_support': support, 'forbidden': forbidden_by_row})
        else:
            # Under singleton-1, both original roots are forced to D and the
            # root-root edge already rejects. Their common mixed degree-four
            # vertex can be omitted as a whole, leaving two degree-four roots.
            q1 = rows[4]
            without_7 = frozenset(e for e in edges if 7 not in e)
            assert not colourings(without_7, q1, (5, 6))
            assert all(sum(v in e for e in without_7) == 4 for v in (5, 6))
            concrete_failures.append({'q1_core_without_mixed_vertex_7': sorted(without_7),
                                      'sigma': sigma(without_7, (5, 6), rows),
                                      'degree_loss': {'5': 1, '6': 1}})
        controls.append({'pointer': f'/exhaustive/{level}/minima_by_sigma/{mask}',
                         'mask': mask, 'edges': sorted(edges), 'degrees': degrees,
                         'epsilon': 2, 'disk_faces': faces, 'q_cores': cores,
                         'concrete_downstream_failures': concrete_failures,
                         'first_E2_failure': '§3.1: unique degree-5 root, all other effective vertices degree 4'})
    return {'source_sha256': sha256(path.read_bytes()).hexdigest(), 'controls': controls}


def build():
    rows = rows_from_scratch()
    return {'schema': 1, 'scope': '252 fixed forms plus two specified E1 graphs only',
            'imports_audited_checker': False, 'rows_independently_derived': rows,
            'unary_omission': check_252(rows), 'epsilon_two_controls': check_e1(rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    target = HERE / 'independent_results.json'
    if args.check:
        assert target.read_text() == payload
    else:
        target.write_text(payload)
    print(json.dumps(result['unary_omission']['counts'], sort_keys=True))
    for control in result['epsilon_two_controls']['controls']:
        print(control['mask'], 'original degrees', control['degrees'],
              'q-core degrees', [(c['row_index'], c['private_degrees']) for c in control['q_cores']])


if __name__ == '__main__':
    main()
