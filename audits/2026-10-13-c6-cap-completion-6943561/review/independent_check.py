#!/usr/bin/env python3
"""Independent exact cap checker; imports no producer or prior audit code.

All private assignments are enumerated as the full Cartesian product 4^6.
The planar cap domain has an additional independent constructive enumeration.
The paper annulus/core classification is the completeness argument for that
enumeration; this program is its finite, independently checked control.
"""
import argparse
import collections
import copy
import functools
import gzip
import hashlib
import itertools
import json
import pathlib
import random

HERE = pathlib.Path(__file__).resolve().parent
AUDIT = HERE.parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(row):
    colors = list(dict.fromkeys(row))
    return tuple(colors.index(x) for x in row), colors


def cycle_rows(n):
    literal = [t for t in itertools.product(range(4), repeat=n)
               if all(t[j] != t[(j + 1) % n] for j in range(n))]
    return literal, sorted({canonical(t)[0] for t in literal})


def cyclic(word):
    return min(tuple(word[j:] + word[:j]) for j in range(len(word)))


def faces(rotation):
    # Predecessor, rather than producer's successor, walks opposite face sides.
    darts = {(v, w) for v, ns in enumerate(rotation) for w in ns}
    assert all(v != w and (w, v) in darts for v, w in darts)
    assert sum(map(len, rotation)) == len(darts)
    remaining = set(darts)
    result = []
    while remaining:
        first = min(remaining)
        a, b = first
        word = []
        while (a, b) in remaining:
            remaining.remove((a, b))
            word.append(a)
            ns = rotation[b]
            a, b = b, ns[(ns.index(a) - 1) % len(ns)]
        assert (a, b) == first
        result.append(word)
    return result


def edges_of(rotation):
    return sorted({tuple(sorted((v, w))) for v, ns in enumerate(rotation) for w in ns})


def raw_domain(data):
    accepted = {}
    total = 0
    for index, line in enumerate(data.decode().splitlines()):
        size, ascii_rotation = line.split(' ', 1)
        assert int(size) == 12
        rotation = [[ord(c) - ord('a') for c in row] for row in ascii_rotation.split(',')]
        assert len(rotation) == 12 and all(len(r) == len(set(r)) for r in rotation)
        fs = faces(rotation)
        assert len(fs) == 17 and sorted(map(len, fs)) == [3] * 16 + [6]
        assert len(edges_of(rotation)) == 27
        boundary = next(f for f in fs if len(f) == 6)
        assert len(set(boundary)) == 6
        bset = set(boundary)
        private = set(range(12)) - bset
        chordless = sum(w in bset for v in bset for w in rotation[v]) == 12
        if chordless and all(len(rotation[v]) >= 5 for v in private):
            accepted[index] = rotation
        total += 1
    return total, accepted


def independent_caps():
    """Construct every annulus wiring from all 14 hexagon triangulations.

    Rotation of the outer rim and reversal are later included in map classes.
    Core cyclic labels start at 6; the wheel center is 11.
    """
    rim = {(j, j + 1) for j in range(5)} | {(0, 5)}
    diagonals = [p for p in itertools.combinations(range(6), 2) if p not in rim]
    triangulations = []
    for choice in itertools.combinations(diagonals, 3):
        if any(a < c < b < d or c < a < d < b
               for (a, b), (c, d) in itertools.combinations(choice, 2)):
            continue
        triangulations.append(rim | set(choice))
    assert len(triangulations) == 14

    def add_annulus(core, advances, ring_size):
        result = set(rim) | set(core)
        position = 0
        assert sum(advances) == 6
        for i in range(ring_size):
            for step in range(advances[i] + 1):
                result.add(((position + step) % 6, i + 6))
            position += advances[i]
        assert position == 6 and len(result) == 27
        degree = collections.Counter(v for edge in result for v in edge)
        assert all(degree[v] >= 5 for v in range(6, 12))
        return sorted(result)

    outerplane = []
    for core in triangulations:
        degrees = collections.Counter(v for e in core for v in e)
        if max(degrees.values()) <= 4:
            advances = [4 - degrees[j] for j in range(6)]
            outerplane.append(add_annulus({(a + 6, b + 6) for a, b in core}, advances, 6))
    wheel = {(6 + j, 6 + (j + 1) % 5) for j in range(5)}
    wheel = {tuple(sorted(e)) for e in wheel} | {(6 + j, 11) for j in range(5)}
    wheel_cases = [add_annulus(wheel, [2 if j == doubled else 1 for j in range(5)], 5)
                   for doubled in range(5)]
    return outerplane + wheel_cases, len(outerplane), len(wheel_cases)


def graph_code(edges):
    return cached_graph_code(tuple(tuple(e) for e in edges))


@functools.lru_cache(maxsize=None)
def cached_graph_code(edges):
    # Exact finite isomorphism: every private permutation and every C6 dihedral
    # boundary map, with no package/canonical-labeller dependency.
    best = None
    for direction, shift in itertools.product((1, -1), range(6)):
        boundary = [(shift + direction * j) % 6 for j in range(6)]
        for perm in itertools.permutations(range(6, 12)):
            mapping = boundary + list(perm)
            code = tuple(sorted(tuple(sorted((mapping[a], mapping[b]))) for a, b in edges))
            if best is None or code < best:
                best = code
    return best


def tuple_pool(edges):
    internal = [(a - 6, b - 6) for a, b in edges if a >= 6 and b >= 6]
    return [t for t in itertools.product(range(4), repeat=6)
            if all(t[a] != t[b] for a, b in internal)]


def literal_fibre(pool, edges, row):
    boundary_edges = [(a, b) for a, b in edges if b < 6]
    if any(row[a] == row[b] for a, b in boundary_edges):
        return []
    contacts = [(a, b - 6) for a, b in edges if a < 6 <= b]
    return [list(t) for t in pool if all(row[a] != t[b] for a, b in contacts)]


def verify_structure(value, accepted, independent_codes):
    caps = value['caps']
    assert len(caps) == len(accepted) == len(independent_codes) == 3, 'missing or extra cap'
    assert set(c['source_line_index_0based'] for c in caps) == set(accepted), 'raw domain coverage'
    assert len(set(c['cap_id'] for c in caps)) == len(caps)
    codes = []
    for c in caps:
        source = accepted[c['source_line_index_0based']]
        assert c['source_rotation'] == source
        source_face = c['source_outer_face']
        assert any(cyclic(source_face) in (cyclic(f), cyclic(f[::-1]))
                   for f in faces(source) if len(f) == 6)
        mapping = c['old_to_named']
        if isinstance(mapping, dict):
            mapping = [mapping[str(j)] for j in range(12)]
        assert sorted(mapping) == list(range(12))
        assert set(mapping[v] for v in source_face) == set(range(6))
        expected_rotation = [[] for _ in range(12)]
        for v, ns in enumerate(source):
            expected_rotation[mapping[v]] = [mapping[w] for w in ns]
        assert c['rotation'] == expected_rotation, 'rotation custody mismatch'
        rotation = c['rotation']
        edges = edges_of(rotation)
        assert c['edges'] == [list(e) for e in edges]
        assert c['boundary_degrees'] == list(map(len, rotation[:6]))
        assert c['private_degrees'] == list(map(len, rotation[6:]))
        assert c['core_edges'] == [list(e) for e in edges if e[0] >= 6]
        assert c['boundary_private_edges'] == [list(e) for e in edges if e[0] < 6 <= e[1]]
        assert c['named_boundary'] == list(range(6)) and c['private_order'] == list(range(6, 12))
        fs = faces(rotation)
        assert sorted(map(len, fs)) == [3] * 16 + [6]
        outer = next(f for f in fs if len(f) == 6)
        assert cyclic(outer) in (tuple(range(6)), (0, 5, 4, 3, 2, 1))
        assert [(a, b) for a, b in edges if b < 6] == [(0, 1), (0, 5), (1, 2), (2, 3), (3, 4), (4, 5)]
        assert all(len(rotation[v]) >= 5 for v in range(6, 12))
        deep = [v for v in range(6, 12) if all(w >= 6 for w in rotation[v])]
        assert c['deep_centers'] == deep
        assert c['deep_wheel_rings'] == [rotation[v] for v in deep]
        if deep:
            assert len(deep) == 1
            center = deep[0]
            ring = rotation[center]
            assert set(ring) == set(range(6, 12)) - {center}
            assert all(tuple(sorted((ring[j], ring[(j + 1) % 5]))) in edges for j in range(5))
            assert len([e for e in edges if e[0] >= 6]) == 10
            assert 'wheel' in c['core_type'].lower() or 'w5' in c['core_type'].lower()
        else:
            assert all(len(rotation[v]) == 5 for v in range(6, 12))
            core_rotation = [[w - 6 for w in rotation[v] if w >= 6] for v in range(6, 12)]
            assert sorted(map(len, faces(core_rotation))) == [3, 3, 3, 3, 6]
            assert len(edges_of(core_rotation)) == 9
            assert 'outerplane' in c['core_type'].lower()
        codes.append(graph_code(edges))
        attachments = c['attachments']
        assert len(attachments) == 96
        assert {(a['short_eq_index'], a['direction'], a['shift']) for a in attachments} == set(itertools.product(range(8), (1, -1), range(6)))
        for a in attachments:
            i, d, s = a['short_eq_index'], a['direction'], a['shift']
            pair = [i, (i + 2) % 8]
            order = [i] + [(i + step) % 8 for step in range(3, 8)]
            pins = [order[(s + d * j) % 6] for j in range(6)]
            inverse = [-1] * 8
            for j, v in enumerate(pins):
                inverse[v] = j
            inverse[pair[1]] = inverse[pair[0]]
            assert a['identified_original_pair'] == pair
            assert a['long_pocket_original_order'] == order
            assert a['cap_boundary_to_original'] == pins
            assert a['original_C8_to_cap_boundary'] == inverse, 'original pin map mismatch'
            assert a['private_original_order'] == list(range(8, 14))
    assert len(set(codes)) == 3 and set(codes) == independent_codes, 'independent annulus domain mismatch'


def verify(value, accepted, independent_codes, interface, queries, seed=None, all_literals=True):
    verify_structure(value, accepted, independent_codes)
    c8_literals, c8_patterns = cycle_rows(8)
    c6_literals, c6_patterns = cycle_rows(6)
    assert value['original_C8_pattern_order'] == interface['pattern_order'] == list(map(list, c8_patterns))
    assert interface['literal_assignments'] == list(map(list, c8_literals))
    assert interface['literal_to_pattern'] == [c8_patterns.index(canonical(r)[0]) for r in c8_literals]
    assert value['original_U_queries'] == queries
    assert value['C6_pattern_order'] == list(map(list, c6_patterns))
    assert len(c8_patterns) == 274 and len(c8_literals) == 6564 and len(c6_patterns) == 31
    codec = value['C8_literal_expansion']
    literal_frames = []
    for row in c8_literals:
        _, frame = canonical(row)
        literal_frames.append(frame + [x for x in range(4) if x not in frame])
    assert codec['literal_order'] == list(map(list, c8_literals))
    assert codec['canonical_indices'] == interface['literal_to_pattern']
    assert codec['canonical_to_literal_total_permutations'] == literal_frames
    counts = collections.Counter()
    caps = list(value['caps'])
    rng = random.Random(seed)
    if seed is not None:
        rng.shuffle(caps)
    for c in caps:
        edges = [tuple(e) for e in c['edges']]
        pool = tuple_pool(edges)
        direct = {row: literal_fibre(pool, edges, row) for row in c6_literals}
        assert len(c['all_31_C6_fibres']) == 31, 'missing C6 fibre'
        for index, row in enumerate(c6_patterns):
            assert c['all_31_C6_fibres'][index] == direct[row], 'C6 full tuple mismatch'
            counts['C6_complete_canonical_fibres'] += 1
        assert c['C6_support_indices'] == [p for p, row in enumerate(c6_patterns) if direct[row]]
        counts['C6_direct_literal_fibres'] += len(direct)
        attachments = list(c['attachments'])
        if seed is not None:
            rng.shuffle(attachments)
        for a in attachments:
            assert len(a['all_274_C8_fibres']) == 274, 'missing C8 fibre'
            pair, pins = a['identified_original_pair'], a['cap_boundary_to_original']
            indices = list(range(274))
            if seed is not None:
                rng.shuffle(indices)
            for p in indices:
                row = c8_patterns[p]
                expected = [] if row[pair[0]] != row[pair[1]] else direct[tuple(row[v] for v in pins)]
                assert a['all_274_C8_fibres'][p] == expected, 'C8 full tuple mismatch'
                counts['C8_complete_canonical_fibres'] += 1
                if row[pair[0]] != row[pair[1]]:
                    counts['Eq_mismatch_empty_cells'] += 1
            expected_transfers = []
            for p, row in enumerate(c8_patterns):
                if row[pair[0]] != row[pair[1]]:
                    continue
                projected = tuple(row[v] for v in pins)
                normal, frame = canonical(projected)
                frame += [x for x in range(4) if x not in frame]
                expected_transfers.append({
                    'original_C8_index': p, 'literal_cap_C6_row': list(projected),
                    'normalized_C6_index': c6_patterns.index(normal),
                    'normalized_to_original_total_colour_permutation': frame})
            assert len(expected_transfers) == 92
            assert a['all_92_Eq_row_transfers'] == expected_transfers
            counts['Eq_full_colour_frame_transfers'] += 92
            support = [p for p, f in enumerate(a['all_274_C8_fibres']) if f]
            assert a['C8_support_indices'] == support
            assert len(a['query_intersections']) == len(queries) == 8
            for saved, q in zip(a['query_intersections'], queries):
                intersection = [p for p in support if (q['support'] >> p) & 1]
                assert saved['query_id'] == q['query_id']
                assert saved['original_C8_indices'] == intersection and intersection
                assert saved['first_witness'] == {
                    'original_C8_index': intersection[0],
                    'original_C8_row': list(c8_patterns[intersection[0]]),
                    'private_lift': a['all_274_C8_fibres'][intersection[0]][0]}
                counts['nonempty_same_row_U_intersections'] += 1
            if all_literals:
                literal_digest = hashlib.sha256()
                literal_lifts = 0
                for li, (row, p, full_frame) in enumerate(zip(c8_literals, interface['literal_to_pattern'], literal_frames)):
                    assert sorted(full_frame) == list(range(4))
                    pulled = sorted([full_frame[x] for x in lift]
                                    for lift in a['all_274_C8_fibres'][p])
                    expected = [] if row[pair[0]] != row[pair[1]] else direct[tuple(row[v] for v in pins)]
                    assert pulled == expected, 'literal S4 reconstruction mismatch'
                    literal_digest.update(json.dumps([li, expected], sort_keys=True, separators=(',', ':')).encode() + b'\n')
                    literal_lifts += len(expected)
                    counts['C8_complete_literal_fibres_S4_checked'] += 1
                assert a['literal_fibre_count'] == 6564
                assert a['literal_lift_count'] == literal_lifts
                assert a['all_6564_literal_fibres_sha256'] == literal_digest.hexdigest()
                counts['C8_complete_literal_lifts'] += literal_lifts
        counts['caps'] += 1
    return dict(counts)


def negative_tests(value, accepted, independent_codes, interface, queries):
    results = {}
    for name in ('missing_graph', 'missing_fibre', 'missing_tuple', 'damaged_rotation', 'damaged_pin_map'):
        bad = copy.deepcopy(value)
        cap = bad['caps'][0]
        if name == 'missing_graph':
            bad['caps'].pop()
        elif name == 'missing_fibre':
            cap['all_31_C6_fibres'].pop()
        elif name == 'missing_tuple':
            next(f for f in cap['all_31_C6_fibres'] if f).pop()
        elif name == 'damaged_rotation':
            cap['rotation'][0][0], cap['rotation'][0][1] = cap['rotation'][0][1], cap['rotation'][0][0]
        elif name == 'damaged_pin_map':
            a = cap['attachments'][0]
            a['original_C8_to_cap_boundary'][a['identified_original_pair'][0]] = -1
        try:
            verify(bad, accepted, independent_codes, interface, queries, all_literals=False)
        except (AssertionError, ValueError, KeyError, IndexError) as exc:
            results[name] = {'rejected': True, 'reason': str(exc) or type(exc).__name__}
        else:
            raise AssertionError('accepted corrupt certificate: ' + name)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int)
    parser.add_argument('--write', type=pathlib.Path)
    args = parser.parse_args()
    manifest = json.loads((AUDIT / 'INPUTS.json').read_text())
    for record in manifest['inputs']:
        data = (AUDIT / 'frozen' / record['path']).read_bytes()
        assert len(data) == record['bytes'] and digest(data) == record['sha256']
    authority = AUDIT / 'frozen' / 'predecessor-authority'
    interface = json.loads(next(authority.rglob('interface.json')).read_text())
    integrated = json.loads(next(authority.rglob('RESULTS.json')).read_text())
    queries = [q for q in integrated['queries'] if q['status'] == 'necessary_condition_residual']
    cert_path = AUDIT / 'search' / 'CERTIFICATE.json.gz'
    compressed = cert_path.read_bytes()
    value = json.loads(gzip.decompress(compressed))
    raw_path = AUDIT / 'search' / 'all-c6-n12.ascii'
    if raw_path.exists():
        raw = raw_path.read_bytes()
    else:
        raw = gzip.decompress((AUDIT / 'search' / 'all-c6-n12.ascii.gz').read_bytes())
    total, accepted = raw_domain(raw)
    assert value['generator']['raw_count'] == total == 89038
    assert value['generator']['raw_bytes'] == len(raw)
    assert value['generator']['raw_sha256'] == digest(raw)
    constructed, outer_count, wheel_count = independent_caps()
    independent_codes = {graph_code(edges) for edges in constructed}
    counts = verify(value, accepted, independent_codes, interface, queries, args.seed)
    negatives = negative_tests(value, accepted, independent_codes, interface, queries)
    result = {
        'schema': 'c6_cap_independent_check_v1', 'accepted': True,
        'certificate_sha256': digest(compressed),
        'checker_sha256': digest(pathlib.Path(__file__).read_bytes()),
        'inputs_sha256': digest((AUDIT / 'INPUTS.json').read_bytes()),
        'seed': args.seed, 'raw_graphs_all_topology_checked': total,
        'raw_accepted_source_lines_0based': sorted(accepted),
        'independent_construction': {
            'hexagon_triangulations': 14, 'outerplane_annulus_parameter_rows': outer_count,
            'wheel_annulus_parameter_rows': wheel_count,
            'constructed_graph_classes_under_C6_dihedral_and_private_relabeling': len(independent_codes),
            'matches_all_certificate_caps': True,
            'completeness_authority': 'paper core classification and annulus-word lemma; finite control is independent of plantri'},
        'counts': counts, 'corrupt_certificates': negatives,
        'generator_authority': 'raw plantri replay retained; independent annulus enumeration provides a second domain control',
        'preserved_boundaries': ['eight original U queries retained', 'source realizability OPEN',
                                 'main theorem OPEN', 'no Lean theorem', 'prior signed-five-point plantri dependency retained']}
    output = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.write:
        with args.write.open('x') as stream:
            stream.write(output)
    print(output, end='')


if __name__ == '__main__':
    main()
