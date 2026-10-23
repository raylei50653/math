#!/usr/bin/env python3
"""Independent read-only replay of the fixed second-layer geometry certificate.

No source-graph generation, LP, or import of produce.py. The named source
contract is an inherited conditional premise, not checked by finite controls.
"""
import argparse
import copy
import gzip
import hashlib
import itertools
import json
import subprocess
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OLD = 'audits/2026-10-13-c9-932-source-d521163/'
FRONT = OLD + 'frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/'
BASE = 'cb8f8593e273a7426ecadd59797a6e643cc4768e'


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def check_inputs(manifest, strict_entry=False):
    require(manifest['base'] == BASE, 'wrong BASE')
    drift = []
    for record in manifest['inputs']:
        local = (HERE / record['frozen_path']).read_bytes()
        require(len(local) == record['bytes'], 'frozen byte length: ' + record['path'])
        require(hashlib.sha256(local).hexdigest() == record['sha256'], 'frozen SHA: ' + record['path'])
        live = (REPO / record['path']).read_bytes()
        base_bytes = subprocess.check_output(['git', 'show', BASE + ':' + record['path']], cwd=REPO)
        require(local == base_bytes, 'not exact BASE bytes: ' + record['path'])
        if live != local:
            drift.append(record['path'])
    require(not drift, 'source authority drift: ' + repr(drift))
    shared = [p for p, digest in manifest['entry_shared_dirty_sha256'].items()
              if hashlib.sha256((REPO / p).read_bytes()).hexdigest() != digest]
    if strict_entry:
        require(not shared, 'entry dirty shared files changed: ' + repr(shared))
    return {'frozen_files': len(manifest['inputs']), 'authority_drift': drift,
            'entry_shared_dirty_drift': shared,
            'entry_shared_dirty_guard': 'strict' if strict_entry else 'report only; routing drift permitted'}


def chord_crosses(a, b):
    """Independent linear cyclic-order test, valid for any polygon size."""
    if len(set(a + b)) != 4:
        return False
    a0, a1 = sorted(a)
    b0, b1 = sorted(b)
    return (a0 < b0 < a1) != (a0 < b1 < a1)


@lru_cache(None)
def polygon_triangulation_edges(n):
    boundary = {tuple(sorted((v, (v + 1) % n))) for v in range(n)}
    diagonals = [e for e in itertools.combinations(range(n), 2) if e not in boundary]
    crosses = {i: {j for j, other in enumerate(diagonals) if chord_crosses(edge, other)}
               for i, edge in enumerate(diagonals)}
    result = set()
    for chosen in itertools.combinations(range(len(diagonals)), n - 3):
        if all(j not in crosses[i] for i, j in itertools.combinations(chosen, 2)):
            result.add(frozenset(boundary | {diagonals[j] for j in chosen}))
    return result


def check_ears(records, n):
    all_edges = polygon_triangulation_edges(n)
    require(len(records) == len(all_edges) == {5: 5, 9: 429}[n], 'polygon coverage')
    actual = set()
    for record in records:
        faces = record['faces']
        require(len(faces) == n - 2, 'triangulation face count')
        require(all(len(set(f)) == 3 and all(0 <= v < n for v in f) for f in faces), 'triangle labels')
        edges = frozenset(tuple(sorted((a, b))) for f in faces for a, b in itertools.combinations(f, 2))
        require(edges in all_edges and edges not in actual, 'missing/duplicate polygon triangulation')
        actual.add(edges)
        degrees = [sum(v in e for e in edges) for v in range(n)]
        ears = [v for v in range(n) if degrees[v] == 2]
        require(record['degrees'] == degrees and record['ears'] == ears, 'ear witness mismatch')
        require(len(ears) >= 2, 'two-ear condition')
        if n == 5:
            require(any(v != 0 for v in ears), 'pentagon requires an ear other than distinguished t_i')
    require(actual == all_edges, 'incomplete polygon family')


def mesh_properties(mesh):
    boundary = mesh['boundary']
    private = mesh['private_vertices']
    require(boundary == ['c' + str(i) for i in range(9)], 'ordered control C9')
    vertices = boundary + private
    require(len(set(vertices)) == len(vertices), 'aliased mesh vertices')
    faces = mesh['oriented_faces']
    require(len({frozenset(f) for f in faces}) == len(faces), 'duplicate mesh face')
    incidence = defaultdict(list)
    adjacency = {v: set() for v in vertices}
    links = {v: defaultdict(set) for v in vertices}
    for face in faces:
        require(len(face) == len(set(face)) == 3 and set(face) <= set(vertices), 'invalid mesh face')
        for a, b in zip(face, face[1:] + face[:1]):
            incidence[tuple(sorted((a, b)))].append((a, b))
            adjacency[a].add(b)
            adjacency[b].add(a)
        for v in face:
            a, b = [w for w in face if w != v]
            links[v][a].add(b)
            links[v][b].add(a)
    boundary_directed = {(boundary[i], boundary[(i + 1) % 9]) for i in range(9)}
    observed_boundary = set()
    for edge, occurrences in incidence.items():
        require(len(occurrences) in (1, 2), 'nonmanifold mesh edge')
        if len(occurrences) == 1:
            observed_boundary.add(occurrences[0])
        else:
            require(occurrences[0] == occurrences[1][::-1], 'incoherent oriented faces')
    require(observed_boundary == boundary_directed, 'mesh boundary/side changed')
    for v in vertices:
        require(links[v], 'unused mesh vertex')
        seen, todo = set(), [next(iter(links[v]))]
        while todo:
            w = todo.pop()
            if w not in seen:
                seen.add(w)
                todo.extend(links[v][w] - seen)
        require(seen == set(links[v]), 'disconnected vertex link')
        degrees = sorted(map(len, links[v].values()))
        expected = [1, 1] + [2] * (len(degrees) - 2) if v in boundary else [2] * len(degrees)
        require(degrees == expected, 'vertex link is not boundary path/interior cycle')
    require(len(vertices) - len(incidence) + len(faces) == 1, 'mesh not disk Euler characteristic')
    require(all(len(adjacency[v]) >= 4 for v in boundary), 'boundary degree below four')
    require(all(len(adjacency[v]) >= 5 for v in private), 'private degree below five')
    allowed = {tuple(sorted((boundary[i], boundary[(i + 1) % 9]))) for i in range(9)}
    require({edge for edge in incidence if set(edge) <= set(boundary)} == allowed, 'C9 chord')
    third = []
    for i in range(9):
        endpoints = {boundary[i], boundary[(i + 1) % 9]}
        candidates = [set(f) - endpoints for f in faces if endpoints <= set(f)]
        require(len(candidates) == 1, 'boundary edge face not unique')
        third.append(next(iter(candidates[0])))
    require(third == mesh['face_third_vertices'] == ['t' + str(i) for i in range(9)], 'face-third labels')
    triples = []
    for v in private:
        contacts = [i for i, c in enumerate(boundary) if c in adjacency[v]]
        require(all(min(abs(i-j), 9-abs(i-j)) in (1, 4)
                    for i, j in itertools.combinations(contacts, 2)), 'forbidden private contact distance')
        require(len(contacts) <= 3, 'too many C contacts')
        if len(contacts) == 3:
            triples.append(v)
    extra = [i for i, v in enumerate(third) if boundary[(i + 5) % 9] in adjacency[v]]
    require(extra == mesh['optional_opposite_contacts'] and len(extra) <= 1, 'incompatible extra contact')
    require(len(triples) == len(extra), 'triple not an original face point')
    require(mesh['source_claim'] is False and mesh['status']['complete_932_global_minimal_source'] == 'not triggered',
            'control incorrectly asserted source realization')
    return {'m': len(private), 'V': len(vertices), 'E': len(incidence), 'F': len(faces),
            'C_degrees': [len(adjacency[v]) for v in boundary],
            'I_degrees': [len(adjacency[v]) for v in private],
            'optional_contacts': extra, 'triangulated_disk': True}


def verify(data):
    require(data['schema'] == 'C9-second-layer-v1' and data['base'] == BASE, 'certificate identity')
    expected_conclusions = {'maximum_triple_contact_private_vertices': 1,
                            'm_minimum': 10, 'k_minimum': 19,
                            'if_triple_contact_each_C6_strict_private_minimum': 5,
                            'if_triple_contact_m_minimum': 11,
                            'if_triple_contact_k_minimum': 20,
                            'source_exclusion': False, 'new_Lean': False}
    require(data['conclusions'] == expected_conclusions, 'unsupported conclusion')
    triples = data['contact_triples']
    require(triples == [[i, (i+1) % 9, (i+5) % 9] for i in range(9)], 'wrong original contact triples')
    allowed_subsets = []
    for mask in range(512):
        subset = [i for i in range(9) if mask >> i & 1]
        if all(min(abs(i-j), 9-abs(i-j)) in (1, 4) for i, j in itertools.combinations(subset, 2)):
            allowed_subsets.append(subset)
    require(len(allowed_subsets) == 37 and max(map(len, allowed_subsets)) == 3, 'inherited contact subset fact')
    require({tuple(sorted(t)) for t in triples} == {tuple(s) for s in allowed_subsets if len(s) == 3}, 'triple classification')
    witnesses = data['alternating_witnesses']
    expected_pairs = set(itertools.combinations(range(9), 2))
    require(len(witnesses) == 36, 'incomplete crossing witnesses')
    actual_pairs = set()
    for witness in witnesses:
        i, j = witness['star_indices']
        require((i, j) in expected_pairs and (i, j) not in actual_pairs, 'crossing witness indices')
        actual_pairs.add((i, j))
        first, second = witness['first_path_contacts'], witness['second_path_contacts']
        require(len(first) == len(second) == 2 and set(first) <= set(triples[i]) and set(second) <= set(triples[j]),
                'crossing path not in actual star')
        require(chord_crosses(first, second), 'paths do not have four distinct alternating terminals')
        require(witness['cyclic_four_distinct_terminals'] == sorted(first + second), 'four-terminal order')
    require(actual_pairs == expected_pairs, 'missing star pair')
    require(len(data['all_optional_patterns']) == 512, 'incomplete optional pattern family')
    for mask, record in enumerate(data['all_optional_patterns']):
        active = [i for i in range(9) if mask >> i & 1]
        crossing_pairs = [p for p in itertools.combinations(active, 2) if p in actual_pairs]
        require(record['mask'] == mask and record['active'] == active, 'optional mask identity')
        require(record['compatible'] == (not crossing_pairs), 'crossing pattern accepted')
        require(record['crossing_star_pair'] == (list(crossing_pairs[0]) if crossing_pairs else []), 'pattern rejection witness')
    source = json.loads(gzip.decompress((HERE / 'frozen' / FRONT / 'c9/finite/certificate.v2.json.gz').read_bytes()))
    cases = {c['id']: c for c in source['cases']}
    queries = {q['query_id']: q for q in source['queries'] if q['target'] == 932 and q['geometry_id'] == 'induced'
               and q['status'] == 'necessary_condition_residual'}
    require(len(queries) == len(data['case_bindings']) == 20, 'named case coverage')
    seen = set()
    for binding in data['case_bindings']:
        query_id = binding['query_id']
        require(query_id in queries and query_id not in seen, 'unnamed/duplicate source binding')
        seen.add(query_id)
        query, case = queries[query_id], cases[queries[query_id]['case_id']]
        order = case['boundary_order']
        require(binding['extras'] == query['extras'] and binding['C9_original_names'] == order, 'original names/attachments changed')
        require(binding['retained_frozen_case_sha256'] == hashlib.sha256(json.dumps(case, sort_keys=True,
            separators=(',', ':')).encode()).hexdigest(), 'full original case not retained')
        expected_thirds = [{'name': 't'+str(i), 'original_edge': [order[i], order[(i+1) % 9]],
                            'only_possible_extra_contact': order[(i+5) % 9]} for i in range(9)]
        require(binding['face_third_definitions'] == expected_thirds, 'original face point identities')
        require(binding['necessary_templates'] == [[], *[[i] for i in range(9)]], 'ten-template coverage')
        require(binding['full_820_row_order_preserved'] is True and binding['new_row_deletions'] == [], 'unsupported row deletion')
    require(len(source['inner_pattern_order']) == 820 and len(source['outer_pattern_order']) == 10, 'complete frozen row order')
    check_ears(data['ear_certificates']['5'], 5)
    check_ears(data['ear_certificates']['9'], 9)
    require(len(data['geometric_controls']) == 2, 'control coverage')
    controls = {mesh['id']: mesh_properties(mesh) for mesh in data['geometric_controls']}
    require(controls['no_triple_m10']['m'] == 10 and controls['one_triple_m11']['m'] == 11, 'sharpness control counts')
    return {'named_cases': len(queries), 'necessary_templates': 200, 'crossing_pairs': 36,
            'optional_patterns_checked': 512, 'compatible_optional_patterns': 10,
            'polygon_triangulations': {'5': 5, '9': 429}, 'geometric_controls': controls,
            'target_source_control': 'not triggered', 'source_exclusions': 0,
            'new_C9_row_deletions': 0, 'conditional_k_minimum': 19,
            'conditional_triple_k_minimum': 20}


def negative_controls(data):
    mutations = []
    bad = copy.deepcopy(data)
    bad['alternating_witnesses'].pop()
    mutations.append(('missing_original_crossing_pair', bad))
    bad = copy.deepcopy(data)
    bad['all_optional_patterns'][3]['compatible'] = True
    mutations.append(('two_opposite_contacts_accepted', bad))
    bad = copy.deepcopy(data)
    bad['case_bindings'][0]['face_third_definitions'][0]['only_possible_extra_contact'] = 'b0'
    mutations.append(('extra_contact_moved_to_original_B', bad))
    bad = copy.deepcopy(data)
    bad['geometric_controls'][0]['oriented_faces'][0].reverse()
    mutations.append(('original_side_orientation_reversed_locally', bad))
    bad = copy.deepcopy(data)
    bad['conclusions']['k_minimum'] = 20
    mutations.append(('unconditional_bound_overclaimed', bad))
    bad = copy.deepcopy(data)
    bad['ear_certificates']['9'].pop()
    mutations.append(('incomplete_polygon_coverage', bad))
    bad = copy.deepcopy(data)
    mesh = bad['geometric_controls'][0]
    mesh['private_vertices'] = ['t'+str(i) for i in range(9)]
    mesh['oriented_faces'] = [f for f in mesh['oriented_faces'] if 's0' not in f]
    mesh['oriented_faces'] += [['t0', 't'+str(i), 't'+str(i+1)] for i in range(1, 8)]
    mutations.append(('m9_empty_center_ear_has_degree_four', bad))
    rejected = []
    for name, bad in mutations:
        try:
            verify(bad)
        except (AssertionError, KeyError, ValueError):
            rejected.append(name)
        else:
            raise AssertionError('negative accepted: ' + name)
    malformed = subprocess.run([sys.executable, '-B', str(HERE / 'check.py'), '--check', '--source',
                                str(HERE / 'certificate.json')], capture_output=True)
    require(malformed.returncode == 2 and b'unrecognized arguments: --source' in malformed.stderr,
            'unsupported named --source proposal was accepted')
    rejected.append('unsupported_named_source_interface_rejected')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--negative', action='store_true')
    parser.add_argument('--check-entry-shared', action='store_true',
                        help='also require the three entry dirty routing files to remain byte-identical')
    args = parser.parse_args()
    inputs = check_inputs(json.loads((HERE / 'INPUTS.json').read_text()), args.check_entry_shared)
    additional = check_inputs(json.loads((HERE / 'ADDITIONAL_INPUTS.json').read_text()), args.check_entry_shared)
    inputs['frozen_files'] += additional['frozen_files']
    data = json.loads((HERE / 'certificate.json').read_text())
    summary = verify(data)
    if args.negative:
        summary['negative_controls_rejected'] = negative_controls(data)
    print(json.dumps({'status': 'PASS', 'frozen_input_check': inputs, **summary}, sort_keys=True))


if __name__ == '__main__':
    main()
