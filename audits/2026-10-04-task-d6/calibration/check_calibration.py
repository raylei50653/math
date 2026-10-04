#!/usr/bin/env python3
"""Small independent audit of saved graph witnesses, not their producers.

Only standard-library graph/color/rotation routines are used.  No existing
checker is imported, and no unsaved graph search is performed.
"""

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
FRAME = set(range(5))
FRAME_EDGES = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}


def components(vertices, adjacency):
    unseen = set(vertices)
    result = []
    while unseen:
        todo = [min(unseen)]
        component = set()
        while todo:
            vertex = todo.pop()
            if vertex in component:
                continue
            component.add(vertex)
            todo.extend((adjacency[vertex] & unseen) - component)
        unseen -= component
        result.append(component)
    return result


def extension(vertices, edges, pattern):
    """Find a literal 4-color extension using independent small DFS."""
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colors = dict(enumerate(pattern))
    if any(colors[a] == colors[b] for a, b in FRAME_EDGES):
        return None

    def search():
        if len(colors) == len(vertices):
            return dict(colors)
        choices = []
        for v in set(vertices) - colors.keys():
            available = set(range(4)) - {colors[u] for u in adjacency[v] if u in colors}
            choices.append((len(available), -len(adjacency[v]), v, available))
        _, _, v, available = min(choices, key=lambda x: x[:3])
        for color in sorted(available):
            colors[v] = color
            answer = search()
            if answer is not None:
                return answer
        colors.pop(v, None)
        return None

    return search()


def same_cycle(a, b):
    if len(a) != len(b):
        return False
    for candidate in (b, list(reversed(b))):
        if any(a == candidate[i:] + candidate[:i] for i in range(len(b))):
            return True
    return False


def check_disk_rotation(vertices, edges, rotation):
    """Check a sphere rotation with C5 as a face from the actual darts."""
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    assert set(rotation) == set(vertices)
    assert all(len(rotation[v]) == len(set(rotation[v])) and set(rotation[v]) == adjacency[v]
               for v in vertices)
    darts = {(a, b) for a, b in edges} | {(b, a) for a, b in edges}
    unseen = set(darts)
    faces = []
    while unseen:
        dart = min(unseen)
        start = dart
        walk = []
        while True:
            assert dart in unseen
            unseen.remove(dart)
            a, b = dart
            walk.append(a)
            around_b = rotation[b]
            dart = (b, around_b[(around_b.index(a) - 1) % len(around_b)])
            if dart == start:
                break
        faces.append(walk)
    assert len(components(vertices, adjacency)) == 1
    assert len(vertices) - len(edges) + len(faces) == 2
    frame_faces = sum(same_cycle(f, list(range(5))) for f in faces)
    # With no private vertex, both sphere faces have the same cycle boundary.
    assert frame_faces == (2 if set(vertices) == FRAME else 1)
    return {'vertices': len(vertices), 'edges': len(edges), 'faces': len(faces),
            'euler_characteristic': 2, 'frame_is_face': True}


def normalize_rotation(embedding):
    if 'rotation' in embedding:
        return {row['vertex']: row['clockwise'] for row in embedding['rotation']}
    return {int(v): around for v, around in embedding['disk_rotation'].items()}


def reconstruct(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        assert a != b
        adjacency[a].add(b)
        adjacency[b].add(a)
    assert {e for e in edges if set(e) <= FRAME} == FRAME_EDGES
    private = set(vertices) - FRAME
    roots = {v for v in private if len(adjacency[v]) >= 5}
    pieces = []
    for number, p in enumerate(components(private - roots, adjacency)):
        support = set().union(*(adjacency[v] & FRAME for v in p))
        neighbors = set().union(*(adjacency[v] & roots for v in p))
        rest = private - p
        one_sided = bool(rest) and len(components(rest, adjacency)) == 1
        contained_in_frame_edge = any(support <= set(e) for e in FRAME_EDGES)
        pieces.append({'id': f'P{number}', 'vertices': sorted(p),
                       'degree_by_vertex': [[v, len(adjacency[v])] for v in sorted(p)],
                       'adjacent_roots': sorted(neighbors), 'actual_support': sorted(support),
                       'unary': len(neighbors) == 1, 'one_sided': one_sided,
                       'long_support': not contained_in_frame_edge})
    unary = [p for p in pieces if p['unary']]
    # The long piece must be distinct from both counted unary pieces.
    candidate_triples = []
    for p in pieces:
        if not p['one_sided'] or not p['long_support']:
            continue
        other_unary = [u for u in unary if u['id'] != p['id']]
        for i, u in enumerate(other_unary):
            for v in other_unary[i + 1:]:
                candidate_triples.append([p['id'], u['id'], v['id']])
    return {'private_vertices': sorted(private), 'roots': sorted(roots),
            'degree_by_vertex': [[v, len(adjacency[v])] for v in sorted(private)],
            'interior_connected': bool(private) and len(components(private, adjacency)) == 1,
            'all_private_degree_at_least_four': all(len(adjacency[v]) >= 4 for v in private),
            'pieces': pieces, 'unary_count': len(unary),
            'candidate_distinct_triples': candidate_triples}


def main():
    s_path = HERE / 'snapshot/c5_shield_calibration/observations.json'
    e_path = HERE / 'snapshot/c5_excess_rejection_law/observations.json'
    s = json.loads(s_path.read_text())
    e = json.loads(e_path.read_text())
    assert s['pattern_order'] == e['pattern_order']
    patterns = s['pattern_order']
    canonical_patterns = set()
    for row in itertools.product(range(4), repeat=5):
        if any(row[a] == row[b] for a, b in FRAME_EDGES):
            continue
        color_names = {}
        canonical_patterns.add(tuple(color_names.setdefault(c, len(color_names)) for c in row))
    assert [tuple(q) for q in patterns] == sorted(canonical_patterns)
    saved = {}
    occurrences = Counter()

    def record(label, group, vertices, raw_edges, embedding=None, expected_sigma=None):
        edges = frozenset(tuple(sorted(x)) for x in raw_edges)
        key = (tuple(sorted(vertices)), tuple(sorted(edges)))
        occurrences[group] += 1
        entry = saved.setdefault(key, {'vertices': sorted(vertices), 'edges': sorted(edges),
                                       'sources': [], 'embeddings': [], 'expected_sigmas': []})
        entry['sources'].append(label)
        if embedding is not None:
            entry['embeddings'].append((label, embedding))
        if expected_sigma is not None:
            entry['expected_sigmas'].append((label, expected_sigma))

    for i, g in enumerate(s['graphs']):
        record(f'S#/graphs/{i} ({g["id"]})', 'S graphs', g['vertices'], g['edges'],
               g['embedding'], g['sigma']['mask'])
    for i, row in enumerate(e['exhaustive']):
        for mask, g in row['minima_by_sigma'].items():
            record(f'E#/exhaustive/{i}/minima_by_sigma/{mask}', 'E saved minima',
                   g['vertices'], g['all_edges'], g['embedding'], g['sigma_mask'])
    for i, row in enumerate(e['scratch']):
        vertices = sorted(FRAME | {v for edge in row['original_edges'] for v in edge})
        record(f'E#/scratch/{i}/original_edges', 'E scratch originals', vertices,
               list(FRAME_EDGES) + row['original_edges'])
        for j, outcome in enumerate(row['outcomes']):
            outcome_vertices = sorted(FRAME | {v for edge in outcome['edges'] for v in edge})
            record(f'E#/scratch/{i}/outcomes/{j}/edges', 'E saved outcomes', outcome_vertices,
                   list(FRAME_EDGES) + outcome['edges'])
        g = row['witness']
        record(f'E#/scratch/{i}/witness', 'E scratch witnesses', g['vertices'], g['all_edges'],
               g['embedding'], g['sigma_mask'])

    results = []
    for i, (_, g) in enumerate(sorted(saved.items())):
        vertices = g['vertices']
        edges = set(g['edges'])
        structural = reconstruct(vertices, edges)
        accepted = [index for index, q in enumerate(patterns)
                    if extension(vertices, edges, q) is not None]
        sigma = sum(1 << index for index in accepted)
        assert all(mask == sigma for _, mask in g['expected_sigmas'])
        deleted_extensions = {}
        for edge in sorted(edges - FRAME_EDGES):
            deleted_extensions[edge] = [index for index, q in enumerate(patterns)
                                       if extension(vertices, edges - {edge}, q) is not None]
        critical_q = [index for index in range(10) if index not in accepted
                      and all(index in rows for rows in deleted_extensions.values())]
        sigma_minimal = all(set(rows) != set(accepted) for rows in deleted_extensions.values())
        disk_proofs = [dict(source=label, **check_disk_rotation(vertices, edges,
                                                               normalize_rotation(embedding)))
                       for label, embedding in g['embeddings']]
        assert disk_proofs, f'No saved disk rotation for {g["sources"]}'
        results.append({'id': f'G{i:02d}', 'sources': g['sources'], 'vertices': vertices,
                        'edges': [list(x) for x in sorted(edges)], **structural,
                        'sigma': sigma, 'accepted_pattern_indices': accepted,
                        'single_q_minimal_pattern_indices': critical_q,
                        'edge_minimal_for_entire_sigma': sigma_minimal,
                        'disk_rotation_checks': disk_proofs})

    # Two explicitly constructed controls; they are not saved input graphs.
    q = [0, 1, 0, 1, 2]
    negative_vertices = list(range(13))
    accepting_edges = FRAME_EDGES | {(0, 6), (3, 6), (4, 6), (5, 6)}
    for a, b, d, ee, f in [(0, 1, 7, 8, 9), (2, 3, 10, 11, 12)]:
        accepting_edges |= {tuple(sorted(pair)) for pair in
                            [(d, ee), (ee, f), (d, f), (d, a), (d, b),
                             (ee, b), (ee, 5), (f, a), (f, 5)]}
    accepting_rotation = {
        0: [1, 4, 6, 9, 7], 1: [0, 7, 8, 2], 2: [1, 12, 10, 3],
        3: [2, 10, 11, 6, 4], 4: [3, 6, 0], 5: [6, 11, 12, 8, 9],
        6: [0, 4, 3, 5], 7: [1, 0, 9, 8], 8: [5, 1, 7, 9], 9: [0, 5, 8, 7],
        10: [3, 2, 12, 11], 11: [5, 3, 10, 12], 12: [2, 5, 11, 10]}
    accepting_control = {
        'purpose': 'Unconditional paraphrase counterexample; degree-5 root, but q accepts.',
        'vertices': negative_vertices, 'edges': [list(x) for x in sorted(accepting_edges)],
        'rotation': accepting_rotation, **reconstruct(negative_vertices, accepting_edges),
        'disk_rotation_check': check_disk_rotation(negative_vertices, accepting_edges,
                                                   accepting_rotation),
        'q': q, 'q_extension': extension(negative_vertices, accepting_edges, q)}
    assert accepting_control['candidate_distinct_triples']
    assert accepting_control['q_extension'] is not None
    assert accepting_control['all_private_degree_at_least_four']

    rejecting_edges = FRAME_EDGES | {(0, 5), (1, 5), (2, 5), (4, 5),
                                     (2, 12), (3, 12), (4, 12), (5, 12)}
    triangle_edges = []
    for a, b, d, ee, f in [(0, 1, 8, 7, 6), (1, 2, 11, 10, 9)]:
        added = {tuple(sorted(pair)) for pair in
                 [(d, ee), (ee, f), (d, f), (d, a), (d, b),
                  (ee, b), (ee, 5), (f, a), (f, 5)]}
        triangle_edges.extend(added)
        rejecting_edges |= added
    rejecting_rotation = {
        0: [1, 4, 5, 6, 8], 1: [0, 8, 7, 5, 9, 11, 2], 2: [1, 11, 10, 5, 12, 3],
        3: [2, 12, 4], 4: [3, 12, 5, 0], 5: [0, 4, 12, 2, 10, 9, 1, 7, 6],
        6: [0, 5, 7, 8], 7: [5, 1, 8, 6], 8: [1, 0, 6, 7],
        9: [1, 5, 10, 11], 10: [5, 2, 11, 9], 11: [2, 1, 9, 10], 12: [2, 5, 4, 3]}
    rejecting_control = {
        'purpose': 'Unconditional paraphrase counterexample; q rejects but unary edges noncritical.',
        'vertices': negative_vertices, 'edges': [list(x) for x in sorted(rejecting_edges)],
        'rotation': rejecting_rotation, **reconstruct(negative_vertices, rejecting_edges),
        'disk_rotation_check': check_disk_rotation(negative_vertices, rejecting_edges,
                                                   rejecting_rotation),
        'q': q, 'q_extension': extension(negative_vertices, rejecting_edges, q),
        'q_rejects_after_each_unary_edge_deletion': [
            {'edge': list(edge), 'q_extension': extension(negative_vertices,
                                                        rejecting_edges - {edge}, q)}
            for edge in sorted(triangle_edges)],
        'q_extension_after_root_long_edge_deletion': extension(
            negative_vertices, rejecting_edges - {(5, 12)}, q)}
    assert rejecting_control['candidate_distinct_triples']
    assert rejecting_control['q_extension'] is None
    assert rejecting_control['all_private_degree_at_least_four']
    assert all(x['q_extension'] is None
               for x in rejecting_control['q_rejects_after_each_unary_edge_deletion'])
    assert rejecting_control['q_extension_after_root_long_edge_deletion'] is not None

    hashes_before = json.loads((HERE / 'hash_before.json').read_text())
    drift = []
    hashes_after = []
    repo = next(p for p in HERE.parents if (p / '.git').exists())
    for row in hashes_before:
        # The path entries are relative to repo root.
        raw = (repo / row['path']).read_bytes()
        current = hashlib.sha256(raw).hexdigest()
        hashes_after.append({'path': row['path'], 'sha256': current, 'size': len(raw)})
        if current != row['sha256']:
            drift.append({'path': row['path'], 'before': row['sha256'], 'after': current})
    summary = {
        'saved_graph_occurrences': dict(occurrences),
        'distinct_saved_labelled_graphs': len(results),
        'graphs_by_unary_count': dict(sorted(Counter(x['unary_count'] for x in results).items())),
        'graphs_with_two_or_more_unary': [x['id'] for x in results if x['unary_count'] >= 2],
        'all_two_unary_graphs_have_exactly_two_pieces_and_one_root': all(
            len(x['pieces']) == 2 and len(x['roots']) == 1
            for x in results if x['unary_count'] == 2),
        'candidate_long_piece_plus_two_distinct_unary': [x['id'] for x in results
                                                        if x['candidate_distinct_triples']],
        'all_saved_rotations_verified': True,
        'degree_minimum_failures': [x['id'] for x in results
                                   if not x['all_private_degree_at_least_four']],
        'whole_sigma_minimality_failures': [x['id'] for x in results
                                           if not x['edge_minimal_for_entire_sigma']],
        'single_q_minimal_histogram': dict(sorted(Counter(len(x['single_q_minimal_pattern_indices'])
                                                         for x in results).items())),
        'source_hash_drift': drift,
        'scope': 'Only explicit saved labelled witnesses; no exhaustive producer re-run.',
        'imports': 'Python standard library only; no audited checker or graph library.'}
    output = {'summary': summary, 'saved_graphs': results,
              'unconditional_paraphrase_negative_controls': [accepting_control, rejecting_control]}
    (HERE / 'results.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'hash_after.json').write_text(json.dumps(hashes_after, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    assert not drift


if __name__ == '__main__':
    main()
