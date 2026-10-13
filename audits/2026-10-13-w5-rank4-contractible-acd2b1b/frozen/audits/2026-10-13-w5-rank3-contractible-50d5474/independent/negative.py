#!/usr/bin/env python3
"""Original-edge, geometry, rank, full-lift and preservation negative controls.

Two actual records (c=1 and c=2) are positive controls. Every corruption is
rejected by both primary recomputation and independent edges/rotation/DFS.
A separate complete prism control demonstrates equal Sigma with unequal R3.
"""
import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, separators=(',', ':'))+'\n').encode()


def digest(obj):
    return hashlib.sha256(encoded(obj)).hexdigest()


def prism(independent):
    faces = [[0, 4, 3, 2, 1]]
    faces += [[i, (i+1) % 5, 5+(i+1) % 5, 5+i] for i in range(5)]
    faces += [list(range(5, 10))]
    edges = sorted({tuple(sorted((f[i], f[(i+1) % len(f)])))
                    for f in faces for i in range(len(f))})
    wheel_edges = sorted(edges+[(u, 10) for u in range(5, 10)])
    wheel_faces = faces[:-1]+[[5+i, 5+(i+1) % 5, 10] for i in range(5)]

    def rotations(n, fs):
        result = []
        for x in range(n):
            steps = {f[(i-1) % len(f)]: f[(i+1) % len(f)]
                     for f in fs for i in range(len(f)) if f[i] == x}
            start = min(steps)
            cycle = [start]
            while steps[cycle[-1]] != start:
                cycle.append(steps[cycle[-1]])
            assert len(cycle) == len(steps)
            result.append(cycle)
        return result

    rotation = rotations(10, faces)
    wheel_rotation = rotations(11, wheel_faces)
    independent.rotation_faces(10, edges, faces, rotation)
    independent.rotation_faces(11, wheel_edges, wheel_faces, wheel_rotation)
    rows, sigma = [], 0
    for i, beta in enumerate(independent.BETAS):
        cells = [[] for _ in range(1024)]
        for lift in independent.colour(10, edges, beta, False):
            cells[int(lift[5:10], 4)].append(lift)
        full_g = independent.colour(10, edges, beta, True)
        if full_g:
            sigma |= 1 << i
        rows.append({'beta': list(beta), 'cells': cells, 'wheel_full_lifts': full_g})
    assert sigma == 1023
    return {'key': 'prism-strength-control', 'vertices': list(range(10)),
            'B': list(range(5)), 'U': list(range(5, 10)), 'private': [],
            'edges': list(map(list, edges)), 'faces': faces, 'rotation': rotation,
            'wheel_edges': list(map(list, wheel_edges)), 'wheel_faces': wheel_faces,
            'wheel_rotation': wheel_rotation,
            'ownership': {'outer_face': 0, 'empty_U_face': 6,
                          'centre_after_restoration': 10, 'pin_map': list(range(10))},
            'rows': rows, 'Sigma': sigma}


def compute():
    primary = module('rank3c_primary_negative', ROOT/'controls/check.py')
    independent = module('rank3c_independent_negative', ROOT/'independent/check.py')
    sources = {}
    with gzip.open(ROOT/'controls/certificate.jsonl.gz', 'rt') as stream:
        next(stream)
        for line in stream:
            record = json.loads(line)
            c = record['parameters']['c']
            if c not in sources and record['Sigma'] == 1023:
                sources[c] = record
            if len(sources) == 2:
                break
    assert set(sources) == {1, 2}

    def independent_validate(record):
        param = record['parameters']
        n, edges = independent.graph_from_neighbours(param)
        independent.geometry(record, param, n, edges)
        independent.verify_rows(record, n, edges)

    expected = {}
    positives = []
    for c, record in sources.items():
        expected[c] = primary.fill(primary.make(record['parameters']))
        assert expected[c] == record
        independent_validate(record)
        positives.append({'c': c, 'source_key': record['key'],
                          'record_sha256': digest(record),
                          'status': 'triggered and holds: both validators'})

    corruptions = []

    def corrupt(name, c, mutate, patch):
        record = copy.deepcopy(sources[c])
        mutate(record)
        corruptions.append((name, c, record, patch))

    omitted_edge = next(e for e in sources[1]['edges'] if min(e) >= 10)
    corrupt('omitted_original_private_edge', 1,
            lambda r: r['edges'].remove(omitted_edge), {'remove_edge': omitted_edge})
    corrupt('wrong_private_rank', 1,
            lambda r: r['counts'].__setitem__('rho', 2), {'counts.rho': 2})
    corrupt('omitted_tree_component', 2,
            lambda r: r['components'].pop(), {'remove_component': sources[2]['components'][-1]})
    corrupt('wrong_U_pin_map', 1,
            lambda r: r['ownership']['pin_map'].__setitem__(slice(5, 7), [6, 5]),
            {'ownership.pin_map[5:7]': [6, 5]})
    corrupt('reversed_designated_U_face', 1,
            lambda r: r['faces'][-1].reverse(), {'reverse_face_index': -1})

    def confuse_degree(r):
        for x, d in zip(r['private'], r['degree_F']):
            r['degree_G'][x] = d

    corrupt('G_degree_replaced_by_F_degree', 1, confuse_degree,
            {'degree_G_on_private': sources[1]['degree_F']})
    row, cell = next((i, j) for i, r in enumerate(sources[1]['rows'])
                     for j, lifts in enumerate(r['cells']) if lifts)
    omitted_lift = sources[1]['rows'][row]['cells'][cell][-1]
    corrupt('omitted_necessary_full_A_lift', 1,
            lambda r: r['rows'][row]['cells'][cell].pop(),
            {'row': row, 'cell': cell, 'remove_lift': omitted_lift})
    corrupt('essential_only_M_zero_applied', 1,
            lambda r: r['counts'].__setitem__('M', 0), {'counts.M': 0})

    failures = []
    for name, c, record, patch in corruptions:
        for validator in ('primary', 'independent'):
            try:
                if validator == 'primary':
                    assert record == expected[c], 'recomputed complete record mismatch'
                else:
                    independent_validate(record)
            except AssertionError:
                failures.append({'case': name, 'validator': validator,
                                 'source_key': sources[c]['key'],
                                 'source_sha256': digest(sources[c]),
                                 'patch': patch, 'corrupt_record_sha256': digest(record),
                                 'status': 'rejected'})
            else:
                raise AssertionError(f'corruption accepted: {name} {validator}')
    assert len(failures) == 16

    control = prism(independent)
    assert primary.fill(copy.deepcopy(control)) == control
    source = sources[1]
    assert source['Sigma'] == control['Sigma'] == 1023
    mismatch = None
    for i, (left, right) in enumerate(zip(source['rows'], control['rows'])):
        for j, (sl, tl) in enumerate(zip(left['cells'], right['cells'])):
            tau = independent.TAUS[j]
            if len(set(tau)) == 3 and bool(sl) != bool(tl):
                mismatch = {'beta': list(independent.BETAS[i]), 'tau': list(tau),
                            'source_nonempty': bool(sl), 'prism_nonempty': bool(tl),
                            'source_A_lift': sl[0] if sl else None,
                            'prism_A_lift': tl[0] if tl else None}
                break
        if mismatch is not None:
            break
    assert mismatch is not None
    strength = {'status': 'counterexample', 'claim': 'equal Sigma implies equal R3',
                'Sigma': 1023, 'source_key': source['key'],
                'source_record_sha256': digest(source), 'prism': control, **mismatch,
                'checks': 'independent direct A/G DFS; primary complete fibre recomputation'}
    return {'base': independent.BASE, 'positive_controls': positives,
            'corruption_rejections': failures, 'strength_counterexample': strength,
            'actual_minimum_source': 'not triggered'}


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = compute()
    path = ROOT/'independent/negative-controls.json.gz'
    data = encoded(result)
    if args.write:
        with path.open('xb') as raw:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as stream:
                stream.write(data)
    else:
        with gzip.open(path, 'rb') as stream:
            assert stream.read() == data, 'negative evidence changed'
    witness = result['strength_counterexample']
    print(json.dumps({'status': 'PASS', 'positive_records': 2,
                      'corrupted_records': 8, 'validator_rejections': 16,
                      'same_Sigma_different_R3': {k: witness[k] for k in
                          ('status', 'beta', 'tau', 'source_nonempty', 'prism_nonempty')},
                      'prism_cells': 10240, 'uncompressed_sha256': hashlib.sha256(data).hexdigest(),
                      'actual_minimum_source': 'not triggered'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
