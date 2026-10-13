#!/usr/bin/env python3
"""Independent C9 literal-interface verification; no producer imports.

Noncrossing partitions are built recursively from the block containing the
first point and its disjoint interval gaps, rather than Bell partitions and
crossing rejection. Annulus lifts come from a boundary-vertex DFS.
"""
import argparse
from collections import Counter, defaultdict
import copy
from functools import lru_cache
import gzip
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
TARGETS = (932, 933, 941)


def relabel(word):
    seen = []
    answer = []
    for value in word:
        if value not in seen:
            seen.append(value)
        answer.append(seen.index(value))
    return tuple(answer)


def words(n):
    result = []
    def visit(prefix):
        if len(prefix) == n:
            if prefix[-1] != prefix[0]:
                result.append(tuple(prefix))
            return
        for color in range(min(3, max(prefix) + 1) + 1):
            if color != prefix[-1]:
                visit(prefix + [color])
    visit([0])
    return tuple(result)


@lru_cache(None)
def interval_partitions(lo, hi):
    if lo == hi:
        return ((),)
    result = []
    for count in range(hi - lo):
        for tail in combinations(range(lo + 1, hi), count):
            first = (lo,) + tail
            gaps = [interval_partitions(a + 1, b)
                    for a, b in zip(first, first[1:] + (hi,))]
            for fillings in product(*gaps):
                blocks = [first]
                for fill in fillings:
                    blocks.extend(fill)
                result.append(tuple(sorted(blocks)))
    return tuple(result)


def partition_word(blocks, n=9):
    owner = [None] * n
    for index, block in enumerate(blocks):
        for value in block:
            owner[value] = index
    assert all(value is not None for value in owner)
    return relabel(owner)


def mask(indices):
    value = 0
    for index in indices:
        value |= 1 << index
    return value


def obligations(patterns, nc):
    index = {word: i for i, word in enumerate(patterns)}
    splits = (({0, 1}, {2, 3}), ({0, 2}, {1, 3}), ({0, 3}, {1, 2}))
    table = []
    owners = [(blocks, partition_word(blocks)) for blocks in nc]
    for p in patterns:
        row = []
        for left, right in splits:
            side = [int(color in right) for color in p]
            mates = {}
            for pair in (left, right):
                a, b = sorted(pair)
                mates[a], mates[b] = b, a
            candidates = set()
            for blocks, owner in owners:
                if any(any(side[v] != side[block[0]] for v in block[1:])
                       for block in blocks):
                    continue
                if any(side[i] == side[(i + 1) % 9]
                       and owner[i] != owner[(i + 1) % 9] for i in range(9)):
                    continue
                orbit_words = {p}
                for block in blocks:
                    swapped = set()
                    for q in orbit_words:
                        changed = list(q)
                        for v in block:
                            changed[v] = mates[changed[v]]
                        swapped.add(tuple(changed))
                    orbit_words |= swapped
                candidates.add(mask(index[relabel(q)] for q in orbit_words))
            assert candidates
            row.append(sorted(candidates))
        table.append(row)
    return table


def collar_extras():
    # Stars-and-bars via four bars among eight positions, independent of the
    # producer's recursive composition generator; lexical source order.
    result = []
    for bars in combinations(range(8), 4):
        limits = (-1,) + bars + (8,)
        result.append(tuple(b - a - 1 for a, b in zip(limits, limits[1:])))
    return sorted(result)


def build_collar(extras):
    boundary = ['a0']
    for b in range(1, 5):
        boundary.extend(f'y{b}_{j}' for j in range(1, extras[b] + 1))
        boundary.append(f'a{b}')
    boundary.extend(f'y0_{j}' for j in range(1, extras[0] + 1))
    faces = [[f'b{i}', f'b{(i + 1) % 5}', f'a{i}'] for i in range(5)]
    for b in range(5):
        neighbors = [f'a{(b - 1) % 5}']
        neighbors.extend(f'y{b}_{j}' for j in range(1, extras[b] + 1))
        neighbors.append(f'a{b}')
        faces.extend([f'b{b}', neighbors[j + 1], neighbors[j]]
                     for j in range(len(neighbors) - 1))
    incidences = defaultdict(int)
    for face in faces:
        for a, b in zip(face, face[1:] + face[:1]):
            incidences[tuple(sorted((a, b)))] += 1
    cycle_edges = {tuple(sorted((f'b{i}', f'b{(i + 1) % 5}'))) for i in range(5)}
    cycle_edges |= {tuple(sorted((boundary[i], boundary[(i + 1) % 9]))) for i in range(9)}
    assert all(count == (1 if edge in cycle_edges else 2)
               for edge, count in incidences.items())
    assert len(incidences) == 28 and len(faces) == 14
    assert 14 - len(incidences) + len(faces) == 0
    outer = [f'b{i}' for i in range(5)]
    directed_boundary = {(outer[i], outer[(i + 1) % 5]) for i in range(5)}
    directed_boundary |= {(boundary[(i + 1) % 9], boundary[i]) for i in range(9)}
    darts = []
    next_neighbor = {v: {} for v in outer + boundary}
    adjacent = {v: set() for v in outer + boundary}
    for face in faces:
        for i, v in enumerate(face):
            a, b = face[i - 1], face[(i + 1) % 3]
            # Clockwise neighbor order: for oriented (v,b,a), move b -> a.
            assert b not in next_neighbor[v]
            next_neighbor[v][b] = a
            adjacent[v].update((a, b))
            darts.append((v, b))
    assert len(set(darts)) == len(darts)
    darts = set(darts)
    for a, b in incidences:
        if (a, b) in directed_boundary or (b, a) in directed_boundary:
            assert ((a, b) in darts) == ((a, b) in directed_boundary)
            assert ((b, a) in darts) == ((b, a) in directed_boundary)
        else:
            assert (a, b) in darts and (b, a) in darts
    rotation_paths = {}
    for v in outer + boundary:
        starts = adjacent[v] - set(next_neighbor[v].values())
        ends = adjacent[v] - set(next_neighbor[v])
        assert len(starts) == len(ends) == 1
        path = [next(iter(starts))]
        while path[-1] in next_neighbor[v]:
            path.append(next_neighbor[v][path[-1]])
            assert len(path) <= len(adjacent[v])
        assert set(path) == adjacent[v] and len(path) == len(adjacent[v])
        assert path[-1] in ends
        cycle, direction = (outer, 1) if v in outer else (boundary, -1)
        position = cycle.index(v)
        assert path[0] == cycle[(position + direction) % len(cycle)]
        assert path[-1] == cycle[(position - direction) % len(cycle)]
        rotation_paths[v] = path
    support = []
    for inner in boundary:
        support.append(sorted(int(v[1:]) for edge in incidences if inner in edge
                              for v in edge if v.startswith('b')))
    return boundary, support, set(incidences), faces, rotation_paths


def full_fibres(patterns, outer_patterns, boundary, support):
    outer_index = {word: i for i, word in enumerate(outer_patterns)}
    result = []
    columns = []
    for inner in patterns:
        forbidden = [set() for _ in range(5)]
        for position, adjacent in enumerate(support):
            for b in adjacent:
                forbidden[b].add(inner[position])
        rows = [[] for _ in range(10)]
        def fill(prefix):
            if len(prefix) == 5:
                if prefix[4] != prefix[0]:
                    rows[outer_index[relabel(prefix)]].append(prefix + list(inner))
                return
            b = len(prefix)
            for color in range(4):
                if color not in forbidden[b] and (not prefix or color != prefix[-1]):
                    fill(prefix + [color])
        fill([])
        columns.append(mask(j for j, lifts in enumerate(rows) if lifts))
        result.append(rows)
    return columns, result


def iterate(columns, table, target, geometry_mask):
    live = {i for i, value in enumerate(columns)
            if value | target == target and geometry_mask >> i & 1}
    initial = mask(live)
    rounds = []
    while True:
        encoded = mask(live)
        removed = []
        for i in sorted(live):
            failed = []
            for split, options in enumerate(table[i]):
                if not any(orbit | encoded == encoded for orbit in options):
                    failed.append(split)
            if failed:
                removed.append({'pattern_index': i, 'split_indices': failed})
        if not removed:
            break
        rounds.append({'before': encoded, 'removals': removed})
        live.difference_update(entry['pattern_index'] for entry in removed)
    output = 0
    for i in live:
        output |= columns[i]
    return {'target': target, 'initial': initial, 'rounds': rounds,
            'fixed_point': mask(live), 'possible_outer_union': output,
            'excluded_transfer': output != target}


def build_expected(payload):
    inputs = json.loads((AUDIT / 'INPUTS.json').read_text())
    for entry in inputs['inputs']:
        data = (AUDIT / 'frozen' / entry['path']).read_bytes()
        assert len(data) == entry['bytes']
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
    assert payload['base'] == inputs['base']
    assert payload['schema'] == 'c9-no4ct-frontier-v2'
    inner, outer = words(9), words(5)
    assert len(inner) == 820 and len(outer) == 10
    assert Counter(len(set(p)) for p in inner) == {3: 85, 4: 735}
    assert payload['inner_pattern_order'] == [list(p) for p in inner]
    assert payload['outer_pattern_order'] == [list(p) for p in outer]
    nc = interval_partitions(0, 9)
    assert len(nc) == 4862 and len(set(nc)) == 4862
    quotients = sorted(partition_word(blocks) for blocks in nc
                       if all(not ({i, (i + 1) % 9} <= set(block))
                              for block in blocks for i in range(9)))
    assert len(quotients) == 232
    q_masks = [mask(i for i, row in enumerate(inner)
                    if all(row[a] == row[b] for a in range(9) for b in range(a)
                           if partition[a] == partition[b])) for partition in quotients]
    assert payload['quotient_partitions'] == [list(p) for p in quotients]
    assert payload['quotient_masks'] == q_masks
    table = obligations(inner, nc)
    assert payload['kempe_obligations'] == table, 'independent component-orbit mismatch'
    expected_cases, expected_queries = [], []
    ear_sizes = Counter()
    for case_id, extras in enumerate(collar_extras()):
        boundary, support, edges, faces, rotation_paths = build_collar(extras)
        old_case = payload['cases'][case_id]
        assert old_case['id'] == f'c{case_id:02d}'
        assert old_case['extras'] == list(extras)
        assert old_case['boundary_order'] == boundary
        assert [set(s) for s in old_case['supports']] == [set(s) for s in support]
        assert [len(s) for s in old_case['supports']] == [len(s) for s in support]
        assert {tuple(sorted(edge)) for edge in old_case['annulus_edges']} == edges
        assert len(old_case['annulus_edges']) == len(edges)
        def oriented(face):
            face = tuple(face)
            return min(face[i:] + face[:i] for i in range(3))
        assert {oriented(face) for face in old_case['annulus_faces']} == {oriented(face) for face in faces}
        assert len(old_case['annulus_faces']) == len(faces)
        assert old_case['annulus_rotation_paths'] == rotation_paths
        assert old_case['joint_vertex_order'] == [f'b{i}' for i in range(5)] + boundary
        columns, fibres = full_fibres(inner, outer, boundary, support)
        assert old_case['column_masks'] == columns
        assert old_case['full_lifts_by_inner_then_outer_row'] == fibres, 'literal annulus-fibre mismatch'
        geometries = [{'id': 'induced', 'short_arc': None, 'chord': None,
                       'boundary_mask': (1 << 820) - 1,
                       'quotient_indices': list(range(232))}]
        for start in range(9):
            arc = [(start + j) % 9 for j in range(5)]
            if any(boundary[j][0] != 'a' for j in arc[1:4]):
                continue
            u, v = arc[0], arc[4]
            geometries.append({'id': f'ear{start}', 'short_arc': arc, 'chord': [u, v],
                               'boundary_mask': mask(i for i, p in enumerate(inner)
                                                     if p[u] != p[v] and len(set(p[j] for j in arc)) == 3),
                               'quotient_indices': [i for i, p in enumerate(quotients) if p[u] != p[v]]})
        ear_sizes[len(geometries) - 1] += 1
        assert old_case['geometries'] == geometries
        for geometry in geometries:
            for target in TARGETS:
                check = iterate(columns, table, target, geometry['boundary_mask'])
                missing = [q for q in geometry['quotient_indices']
                           if not check['fixed_point'] & q_masks[q]]
                status = ('excluded_transfer_kempe' if check['excluded_transfer'] else
                          'excluded_relative_quotient' if missing else
                          'necessary_condition_residual')
                expected_queries.append({'query_id': f'c{case_id:02d}-{geometry["id"]}-{target}',
                                         'case_id': f'c{case_id:02d}', 'geometry_id': geometry['id'],
                                         'extras': list(extras), **check, 'status': status,
                                         'missing_quotient_indices': missing,
                                         'necessary_support_size': check['fixed_point'].bit_count()})
        expected_cases.append({'boundary_order': boundary, 'columns': columns, 'fibres': fibres,
                               'geometries': geometries, 'rotation_paths': rotation_paths,
                               'faces': faces})
    assert len(payload['cases']) == 70 and ear_sizes == {0: 20, 1: 30, 2: 15, 3: 5}
    assert payload['queries'] == expected_queries, 'complete independent query-ledger mismatch'
    summary = {'named_collars': 70, 'named_geometries': 145, 'target_queries': 435,
               'inner_orbits': 820, 'literal_inner_assignments': 19680,
               'independent_noncrossing_partitions': 232, 'annulus_fibres': 574000,
               'annulus_empty_fibres': sum(not f for c in expected_cases for row in c['fibres'] for f in row),
               'annulus_full_lifts': sum(len(f) for c in expected_cases for row in c['fibres'] for f in row),
               'by_target': {str(t): dict(Counter(q['status'] for q in expected_queries if q['target'] == t)) for t in TARGETS},
               'by_geometry_type': {typ: dict(Counter(q['status'] for q in expected_queries
                                                      if (q['geometry_id'] == 'induced') == (typ == 'induced')))
                                    for typ in ('induced', 'one_w5_ear')}}
    assert payload['summary'] == summary
    assert payload['scope']['four_colour_theorem_used'] is False
    assert payload['scope']['main_proposition'] == 'OPEN'
    assert payload['scope']['actual_target_source'] == 'not triggered'
    assert payload['color_frame'] == [0, 1, 2, 3]
    residuals = [q for q in expected_queries if q['status'] == 'necessary_condition_residual']
    assert all(q['geometry_id'] == 'induced' for q in residuals)
    assert len(residuals) == 84 and max(max(q['extras']) for q in residuals) == 3
    family_22, family_211 = set(), set()
    for extras in collar_extras():
        positive = [i for i, value in enumerate(extras) if value]
        zero = [i for i, value in enumerate(extras) if not value]
        if len(positive) == 2 and sorted(extras[i] for i in positive) == [2, 2]:
            if (positive[0] - positive[1]) % 5 not in (1, 4):
                family_22.add(extras)
        if len(positive) == 3 and sorted(extras[i] for i in positive) == [1, 1, 2]:
            if (zero[0] - zero[1]) % 5 in (1, 4):
                family_211.add(extras)
    actual_932 = {tuple(q['extras']) for q in residuals if q['target'] == 932}
    assert len(family_22) == 5 and len(family_211) == 15
    assert actual_932 == family_22 | family_211
    restrictions = {'all_three_targets_maximum_gap': 3, '932_maximum_gap': 2,
                    '932_two_nonadjacent_twos': 5, '932_three_consecutive_211': 15}
    return summary, {'cases': expected_cases, 'kempe_obligations': table,
                     'queries': expected_queries, 'residual_degree_restrictions': restrictions}


def negative_controls(payload, reference):
    # Reuse the independently reconstructed accepted records. Every mutation
    # alters a literal or semantic field whose equality was separately proved.
    variants = []
    changed = copy.deepcopy(payload['cases'][0])
    changed['boundary_order'].reverse()
    variants.append(('wrong_original_boundary_order', changed['boundary_order'], reference['cases'][0]['boundary_order']))
    source_index = next(i for i, c in enumerate(payload['cases'])
                        if any(f for row in c['full_lifts_by_inner_then_outer_row'] for f in row))
    source = payload['cases'][source_index]
    changed = copy.deepcopy(source)
    next(f for row in changed['full_lifts_by_inner_then_outer_row'] for f in row if f).pop()
    variants.append(('missing_literal_full_lift', changed['full_lifts_by_inner_then_outer_row'],
                     reference['cases'][source_index]['fibres']))
    ci, gi = next((ci, gi) for ci, c in enumerate(payload['cases'])
                  for gi, g in enumerate(c['geometries']) if g['chord'])
    source = payload['cases'][ci]['geometries'][gi]
    changed = copy.deepcopy(source)
    changed['boundary_mask'] = (1 << 820) - 1
    variants.append(('forgotten_original_ear_chord_and_center', changed, reference['cases'][ci]['geometries'][gi]))
    changed = copy.deepcopy(source)
    changed['quotient_indices'] = list(range(232))
    variants.append(('loop_creating_ear_endpoint_identification', changed, reference['cases'][ci]['geometries'][gi]))
    changed = copy.deepcopy(payload['kempe_obligations'][0])
    changed[1].pop()
    variants.append(('missing_joint_kempe_component_orbit', changed, reference['kempe_obligations'][0]))
    qi = next(i for i, q in enumerate(payload['queries']) if q['status'] == 'necessary_condition_residual')
    source = payload['queries'][qi]
    changed = copy.deepcopy(source)
    changed['status'] = 'excluded_transfer_kempe'
    variants.append(('false_unbounded_source_exclusion', changed, reference['queries'][qi]))
    changed = copy.deepcopy(payload['cases'][0]['annulus_faces'])
    changed[0] = changed[0][::-1]
    def directed_darts(faces):
        return sorted((a, b) for face in faces for a, b in zip(face, face[1:] + face[:1]))
    variants.append(('reversed_actual_triangle_orientation', directed_darts(changed),
                     directed_darts(reference['cases'][0]['faces'])))
    changed = copy.deepcopy(payload['cases'][0]['annulus_rotation_paths'])
    changed['b0'].reverse()
    variants.append(('reversed_original_rotation_path', changed, reference['cases'][0]['rotation_paths']))
    rejected = []
    for label, altered, accepted in variants:
        try:
            assert altered == accepted, label
        except AssertionError:
            rejected.append(label)
        else:
            raise AssertionError('accepted corrupt certificate: ' + label)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE.parent / 'finite/certificate.v2.json.gz')
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    with gzip.open(args.certificate, 'rt') as stream:
        payload = json.load(stream)
    summary, reference = build_expected(payload)
    result = {'status': 'PASS', 'algorithm': 'first-block-interval-noncrossing; literal-boundary-DFS', **summary}
    result['residual_degree_restrictions'] = reference['residual_degree_restrictions']
    if args.negative:
        result['negative_controls_rejected'] = negative_controls(payload, reference)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
