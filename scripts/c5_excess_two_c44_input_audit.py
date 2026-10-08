#!/usr/bin/env python3
"""Read-only semantic and hash audit of the ES/ER inputs used by Task C44.

This does not rerun plantri or claim an independent completeness proof.  It
checks every saved ER source graph, its combinatorial embedding, and every
positive coloring witness.  Rejection/absence and generator completeness
remain dependencies of the separately compared ES/ER computations.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from c5_kempe_screen import REPS

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'artifacts/c5_excess_two_independent_search'
OUTPUT = ROOT / 'artifacts/c5_excess_two_c44/input_audit.json'
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
SINGLETON_INDICES = (6, 4, 3, 1, 0)


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def normalized(values):
    seen = {}
    return tuple(seen.setdefault(value, len(seen)) for value in values)


def d5_actions():
    index = {row: i for i, row in enumerate(REPS)}
    return tuple(tuple(index[normalized(tuple(row[(rotation + sign * i) % 5]
                                                for i in range(5)))]
                       for row in REPS)
                 for sign in (1, -1) for rotation in range(5))


def mask_images(mask):
    return sorted({sum(1 << image[i] for i in range(10) if mask >> i & 1)
                   for image in d5_actions()})


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        if u in vertices and v in vertices:
            adjacency[u].add(v)
            adjacency[v].add(u)
    reached = set()
    pending = [min(vertices)]
    while pending:
        vertex = pending.pop()
        if vertex not in reached:
            reached.add(vertex)
            pending.extend(adjacency[vertex] - reached)
    return reached == vertices


def faces(rotation):
    darts = {(u, v) for u, neighbors in rotation.items() for v in neighbors}
    result = []
    while darts:
        first = min(darts)
        current = first
        face = []
        while True:
            assert current in darts, ('repeated dart before face closes', current)
            darts.remove(current)
            u, v = current
            face.append(u)
            around = rotation[v]
            current = (v, around[(around.index(u) + 1) % len(around)])
            if current == first:
                break
        result.append(face)
    return result


def valid_coloring(colors, edges, row, n):
    assert len(colors) == n
    assert tuple(colors[:5]) == REPS[row]
    assert all(type(c) is int and 0 <= c < 4 for c in colors)
    assert all(colors[u] != colors[v] for u, v in edges)


def validate_source(record, kind, k):
    n = k + 5
    source_edges = tuple(tuple(edge) for edge in record['canonical_edges'])
    assert source_edges == tuple(sorted(set(source_edges)))
    assert all(0 <= u < v < n for u, v in source_edges)
    edges = frozenset(source_edges)
    assert frozenset(edge for edge in edges if edge[1] < 5) == FRAME
    degrees = Counter(v for edge in edges for v in edge)
    expected = [6 if kind == 'D6' and v == 5 else
                5 if kind != 'D6' and v in (5, 6) else 4
                for v in range(5, n)]
    assert [degrees[v] for v in range(5, n)] == expected
    assert sum(degrees[v] - 4 for v in range(5, n)) == 2
    assert all(sum(u < 5 for u, w in edges if w == v) <= 3
               for v in range(5, n))
    assert kind == 'D6' or ((5, 6) in edges) == (kind == 'AD')
    assert connected(range(5, n), edges)
    mask = record['sigma_mask']
    assert mask & 932 == 932
    q = [i for i, index in enumerate(SINGLETON_INDICES) if not mask >> index & 1]
    assert q and q == record['Q']
    assert all(record['domain'].values())
    accepted = record['accepted_colourings']
    assert {int(i) for i in accepted} == {i for i in range(10) if mask >> i & 1}
    for row, colors in accepted.items():
        valid_coloring(colors, edges, int(row), n)
    deletions = record['deletion_sigmas']
    assert {tuple(item['edge']) for item in deletions} == edges - FRAME
    assert len(deletions) == len(edges - FRAME)
    new_witnesses = 0
    for deletion in deletions:
        edge = tuple(deletion['edge'])
        dm = deletion['sigma_mask']
        assert dm & mask == mask
        added = {i for i in range(10) if (dm & ~mask) >> i & 1}
        assert set(deletion['new_indices']) == added
        assert {int(i) for i in deletion['witnesses']} == added
        for row, colors in deletion['witnesses'].items():
            valid_coloring(colors, edges - {edge}, int(row), n)
            assert colors[edge[0]] == colors[edge[1]], 'new witness must violate removed edge'
            new_witnesses += 1
    assert record['critical'] == all(d['sigma_mask'] != mask for d in deletions)
    apex = n
    augmented_edges = edges | {(v, apex) for v in range(5)}
    rotation = {int(v): tuple(neighbors)
                for v, neighbors in record['augmented_rotation'].items()}
    assert set(rotation) == set(range(n + 1))
    for vertex, neighbors in rotation.items():
        assert len(neighbors) == len(set(neighbors))
        expected_neighbors = {v if u == vertex else u
                              for u, v in augmented_edges if vertex in (u, v)}
        assert set(neighbors) == expected_neighbors
    augmented_faces = faces(rotation)
    assert n + 1 - len(augmented_edges) + len(augmented_faces) == 2
    disk_rotation = {v: tuple(u for u in neighbors if u != apex)
                     for v, neighbors in rotation.items() if v != apex}
    disk_faces = faces(disk_rotation)
    assert n - len(edges) + len(disk_faces) == 2
    assert sum(len(face) == 5 and set(face) == set(range(5))
               for face in disk_faces) == 1
    return Counter(source_graphs=1, accepted_witnesses=len(accepted),
                   edge_deletion_profiles=len(deletions),
                   new_row_witnesses=new_witnesses, augmented_rotations=1,
                   disk_boundary_faces=1)


def audit():
    targets = {str(mask): mask_images(mask) for mask in (933, 941)}
    totals = Counter()
    layers = []
    for kind in ('NA', 'AD', 'D6'):
        for k in range(3, 10):
            layer_path = INPUT / f'{kind}_k{k}.json'
            raw = layer_path.read_bytes()
            layer = json.loads(raw)
            assert layer['type'] == kind and layer['k'] == k
            comparison = layer['comparison']
            assert comparison['consistent']
            assert all(not values for values in comparison['differences'].values())
            source_path = ROOT / comparison['es_source']
            source_hash_matches = None
            if source_path.is_file():
                source_hash_matches = sha256(source_path.read_bytes()).hexdigest() == comparison['es_sha256']
                assert source_hash_matches, ('ES input hash drift', str(source_path))
            chunk_manifest = []
            records = []
            semantic_checks = Counter()
            for chunk in layer['q_orbit_chunks']:
                path = ROOT / chunk['path']
                chunk_raw = path.read_bytes()
                assert sha256(chunk_raw).hexdigest() == chunk['sha256']
                value = json.loads(chunk_raw)
                assert value['type'] == kind and value['k'] == k
                assert len(value['q_orbits']) == chunk['orbits']
                chunk_manifest.append(dict(chunk, bytes=len(chunk_raw)))
                for record in value['q_orbits']:
                    semantic_checks.update(validate_source(record, kind, k))
                    records.append(record)
            by_code = {record['code']: record for record in records}
            assert len(by_code) == len(records) == len(layer['q_orbits'])
            for summary in layer['q_orbits']:
                record = by_code[summary['code']]
                assert all(summary[key] == record[key] for key in
                           ('code', 'Q', 'critical', 'orbit_size', 'sigma_mask', 'stabilizer_size'))
            critical = [record for record in records if record['critical']]
            critical_manifest = []
            for path in sorted((INPUT / f'{kind}_k{k}/crit_orbits').glob('orbit_*.json')):
                critical_raw = path.read_bytes()
                record = json.loads(critical_raw)
                assert record['critical'] and record == by_code[record['code']]
                critical_manifest.append({'path': str(path.relative_to(ROOT)),
                                          'sha256': sha256(critical_raw).hexdigest(),
                                          'bytes': len(critical_raw), 'code': record['code']})
            assert len(critical_manifest) == len(critical)
            assert {entry['code'] for entry in critical_manifest} == {r['code'] for r in critical}
            rejection_rows = sum(len(record['Q']) for record in records)
            critical_rows = sum(len(record['Q']) for record in critical)
            labelled_q = sum(record['orbit_size'] for record in records)
            labelled_critical = sum(record['orbit_size'] for record in critical)
            assert labelled_q == comparison['er_counts']['q'] == comparison['es_counts']['q']
            assert labelled_critical == comparison['er_counts']['crit'] == comparison['es_counts']['crit']
            assert len(records) == comparison['er_q_orbits'] == comparison['es_q_orbits']
            assert len(critical) == comparison['er_crit_orbits'] == comparison['es_crit_orbits']
            target_counts = {target: {'q_orbits': sum(r['sigma_mask'] in images for r in records),
                                      'critical_orbits': sum(r['sigma_mask'] in images for r in critical)}
                             for target, images in targets.items()}
            counts = dict(q_orbits=len(records), critical_orbits=len(critical),
                          rejection_rows=rejection_rows, critical_rejection_rows=critical_rows,
                          labelled_q=labelled_q, labelled_critical=labelled_critical)
            totals.update({f'{kind}_{key}': value for key, value in counts.items()})
            totals.update(semantic_checks)
            layers.append({'type': kind, 'k': k, 'counts': counts,
                           'layer_path': str(layer_path.relative_to(ROOT)),
                           'layer_sha256': sha256(raw).hexdigest(),
                           'q_chunk_manifest': chunk_manifest,
                           'critical_manifest': critical_manifest,
                           'source_checks': dict(semantic_checks),
                           'sigma_histogram': dict(sorted(Counter(str(r['sigma_mask']) for r in records).items())),
                           'target_sigma_d5_orbit_intersections': target_counts,
                           'existing_es_er_comparison_consistent': True,
                           'es_source': comparison['es_source'],
                           'es_source_expected_sha256': comparison['es_sha256'],
                           'es_source_present': source_path.is_file(),
                           'es_source_hash_matches': source_hash_matches})
    assert sum(layer['counts']['q_orbits'] for layer in layers) == 9644
    assert sum(layer['counts']['critical_orbits'] for layer in layers) == 179
    assert [totals[f'{kind}_critical_orbits'] for kind in ('NA', 'AD', 'D6')] == [54, 9, 116]
    return {'schema': 'c5-excess-two-c44-input-audit-v1',
            'source_base_commit': 'b2ca452',
            'source_scripts': {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
                               for path in (Path(__file__), ROOT / 'scripts/c5_kempe_screen.py')},
            'definition_sources': ['docs/c5_excess_two_finite_search.md section 1',
                                   'docs/c5_excess_two_independent_search.md sections 1-4'],
            'domain': {'boundary': [0, 1, 2, 3, 4], 'induced_C5': True,
                       'disk': 'apex adjacent to all five boundary vertices has sphere rotation',
                       'interior_minimum_full_degree': 4, 'epsilon': 2,
                       'interior_connected': True, 'spokes_per_vertex_max': 3,
                       'T4_mask': 932, 'Q_nonempty': True,
                       'NA': 'roots 5,6 degree5, nonadjacent; other interior vertices degree4',
                       'AD': 'roots 5,6 degree5, adjacent; other interior vertices degree4',
                       'D6': 'single root5 degree6; other interior vertices degree4',
                       'q_vs_critical': 'all q graphs counted; critical subset separately marked',
                       'small_empty_layers': 'k1,2 have impossible prescribed degree/spoke cap; k3 NA,D6 empty'},
            'D5_row_actions': d5_actions(), 'target_sigma_D5_orbits': targets,
            'totals': dict(totals), 'layers': layers,
            'trust_boundaries': {
                'source_hashes': 'all ER chunks checked against saved manifests; available ES layer hash checked',
                'source_semantics': 'all graph degrees, frame, connectedness, mask payloads, positive coloring witnesses and sphere/disk rotations checked',
                'rejection_absence': 'source rejection masks not recomputed here; C44 core computation and brute comparisons check its row-specific decisions',
                'completeness': 'inherits ES/ER compared enumerations and external plantri completeness; no plantri replay in this audit',
                'range': 'k<=9 only; no four-color-theorem or boundary-state oracle'}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = audit()
    data = encoded(result)
    if args.check:
        assert OUTPUT.read_bytes() == data, 'input audit byte mismatch'
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        with OUTPUT.open('xb') as output:
            output.write(data)
    print(json.dumps({'output': str(OUTPUT.relative_to(ROOT)),
                      'check': args.check, 'totals': result['totals'],
                      'target_sigma_D5_orbits': result['target_sigma_D5_orbits']}, sort_keys=True))


if __name__ == '__main__':
    main()
