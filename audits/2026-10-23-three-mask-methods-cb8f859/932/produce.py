#!/usr/bin/env python3
"""Produce fixed C9 contact witnesses and two explicit geometric controls.

This enumerates subsets and polygon triangulations, never source graphs.
Generation is exclusive-create. check.py does not import this producer.
"""
import gzip
import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = 'audits/2026-10-13-c9-932-source-d521163/'
FRONT = OLD + 'frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/'


def alternating(a, b):
    if len(set(a + b)) != 4:
        return False
    u, v = a
    return ((b[0] - u) % 9 < (v - u) % 9) != ((b[1] - u) % 9 < (v - u) % 9)


@lru_cache(None)
def triangulations(polygon):
    if len(polygon) < 3:
        return ((),)
    if len(polygon) == 3:
        return ((tuple(polygon),),)
    result = []
    for k in range(1, len(polygon) - 1):
        triangle = (polygon[0], polygon[k], polygon[-1])
        for left in triangulations(polygon[:k + 1]):
            for right in triangulations(polygon[k:]):
                result.append(tuple(sorted(left + right + (triangle,))))
    assert len(result) == len(set(result))
    return tuple(result)


def polygon_record(n):
    records = []
    for faces in triangulations(tuple(range(n))):
        edges = {tuple(sorted((a, b))) for face in faces for a, b in zip(face, face[1:] + face[:1])}
        degrees = [sum(v in edge for edge in edges) for v in range(n)]
        ears = [v for v, degree in enumerate(degrees) if degree == 2]
        assert len(ears) >= 2
        records.append({'faces': [list(f) for f in faces], 'degrees': degrees, 'ears': ears})
    return records


def mesh(extra):
    c = ['c' + str(i) for i in range(9)]
    t = ['t' + str(i) for i in range(9)]
    faces = [[c[i], c[(i + 1) % 9], t[i]] for i in range(9)]
    for i in range(9):
        if extra and i == 5:
            faces += [[c[i], t[i], t[0]], [c[i], t[0], t[4]]]
        else:
            faces.append([c[i], t[i], t[(i - 1) % 9]])
    cycles = [[0, 1, 2, 3, 4], [0, 5, 6, 7, 8]] if extra else [list(range(9))]
    centers = ['s' + str(j) for j in range(len(cycles))]
    for center, cycle in zip(centers, cycles):
        for a, b in zip(cycle, cycle[1:] + cycle[:1]):
            faces.append([t[a], t[b], center])
    return {'id': 'one_triple_m11' if extra else 'no_triple_m10',
            'boundary': c, 'private_vertices': t + centers,
            'face_third_vertices': t, 'oriented_faces': faces,
            'optional_opposite_contacts': [0] if extra else [],
            'status': {'geometric_premises': 'triggered and holds',
                       'complete_932_global_minimal_source': 'not triggered'},
            'source_claim': False}


def main():
    authority = json.loads((HERE / 'INPUTS.json').read_text())
    data = json.loads(gzip.decompress((HERE / 'frozen' / FRONT / 'c9/finite/certificate.v2.json.gz').read_bytes()))
    triples = [[i, (i + 1) % 9, (i + 5) % 9] for i in range(9)]
    witnesses = []
    for i, j in itertools.combinations(range(9), 2):
        choices = [(list(a), list(b)) for a in itertools.combinations(triples[i], 2)
                   for b in itertools.combinations(triples[j], 2) if alternating(a, b)]
        assert choices
        a, b = choices[0]
        witnesses.append({'star_indices': [i, j], 'first_path_contacts': a,
                          'second_path_contacts': b,
                          'cyclic_four_distinct_terminals': sorted(a + b)})
    optional_patterns = []
    for mask in range(512):
        active = [i for i in range(9) if mask >> i & 1]
        optional_patterns.append({'mask': mask, 'active': active,
                                 'compatible': len(active) <= 1,
                                 'crossing_star_pair': active[:2] if len(active) > 1 else []})
    cases = {c['id']: c for c in data['cases']}
    bindings = []
    queries = [q for q in data['queries'] if q['target'] == 932 and q['geometry_id'] == 'induced'
               and q['status'] == 'necessary_condition_residual']
    assert len(queries) == 20
    for query in queries:
        case = cases[query['case_id']]
        order = case['boundary_order']
        bindings.append({'query_id': query['query_id'], 'extras': query['extras'],
                         'C9_original_names': order,
                         'face_third_definitions': [{'name': 't' + str(i),
                             'original_edge': [order[i], order[(i + 1) % 9]],
                             'only_possible_extra_contact': order[(i + 5) % 9]}
                             for i in range(9)],
                         'retained_frozen_case_sha256': hashlib.sha256(json.dumps(case, sort_keys=True,
                              separators=(',', ':')).encode()).hexdigest(),
                         'necessary_templates': [[], *[[i] for i in range(9)]],
                         'full_820_row_order_preserved': True,
                         'new_row_deletions': []})
    payload = {'schema': 'C9-second-layer-v1', 'base': authority['base'],
               'scope': 'conditional same-source C9 h=4,932 geometry, arbitrary finite private size',
               'contact_triples': triples, 'alternating_witnesses': witnesses,
               'all_optional_patterns': optional_patterns, 'case_bindings': bindings,
               'ear_certificates': {'5': polygon_record(5), '9': polygon_record(9)},
               'geometric_controls': [mesh(False), mesh(True)],
               'conclusions': {'maximum_triple_contact_private_vertices': 1,
                               'm_minimum': 10, 'k_minimum': 19,
                               'if_triple_contact_each_C6_strict_private_minimum': 5,
                               'if_triple_contact_m_minimum': 11,
                               'if_triple_contact_k_minimum': 20,
                               'source_exclusion': False, 'new_Lean': False}}
    with (HERE / 'certificate.json').open('x') as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'certificate': 'certificate.json', 'crossing_pairs': len(witnesses),
                      'named_cases': len(bindings), 'compatible_optional_patterns': 10,
                      'polygon_triangulations': {n: len(v) for n, v in payload['ear_certificates'].items()}},
                     sort_keys=True))


if __name__ == '__main__':
    main()
