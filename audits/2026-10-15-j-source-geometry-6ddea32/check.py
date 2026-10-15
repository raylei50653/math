#!/usr/bin/env python3
"""Two-original-star fibre calibration; controls are not minimum sources."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BASE = '6ddea32a81349821ad3724ae1652bddb9c6a7b04'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def all_colourings(vertices, edges):
    adjacent = {v: set() for v in vertices}
    for a, b in edges:
        adjacent[a].add(b)
        adjacent[b].add(a)
    assigned, out = {}, []
    order = sorted(vertices, key=lambda v: (-len(adjacent[v]), v))

    def visit(i):
        if i == len(order):
            out.append(tuple(assigned[v] for v in vertices))
            return
        v = order[i]
        forbidden = {assigned[w] for w in adjacent[v] if w in assigned}
        for colour in range(4):
            if colour not in forbidden:
                assigned[v] = colour
                visit(i + 1)
                del assigned[v]
    visit(0)
    return sorted(out)


def source_palette(f):
    r = next(iter(set(range(4)) - {f[x] for x in ('m', 'v', 'w')}))
    pq = {f['p'], f['q']}
    if f['z'] == r:
        allowed = pq == set(range(4)) - {f['m'], r}
    else:
        fourth = next(iter(set(range(4)) - {f['z'], f['m'], r}))
        allowed = pq in ({r, fourth}, {f['m'], fourth})
    e = f['v'] ^ f['w']
    ff = f['p'] ^ f['q']
    g = f['m'] ^ f['z']
    assert allowed == ((e == ff) == (e == g))
    return allowed, r, (e, ff, g)


def local_six_rows():
    names = ('m', 'v', 'w', 'z', 'p', 'q')
    edges = [('m', 'v'), ('m', 'w'), ('v', 'w'), ('z', 'p'), ('z', 'q'), ('p', 'q'), ('m', 'z')]
    out = []
    for row in itertools.product(range(4), repeat=6):
        f = dict(zip(names, row))
        if any(f[a] == f[b] for a, b in edges):
            continue
        allowed, r, values = source_palette(f)
        out.append({'row': row, 'r_lifts': [r], 'edge_differences': values,
                    'source_all_r_allowed': allowed})
    assert len(out) == 432 and sum(x['source_all_r_allowed'] for x in out) == 240
    return out


def patch(a0, c0, sg=6, tg=6):
    h = a0 + c0 - 8
    assert a0 >= 4 and c0 >= 4 and h >= 3 and sg >= 6 and tg >= 6
    alpha = 'p' if a0 == 4 else 'alpha'
    beta = 'q' if c0 == 4 else 'beta'
    m_path = [alpha] + ['t' + str(i) for i in range(tg - 5)] + ['w', 'v'] + ['s' + str(i) for i in range(sg - 5)] + [beta]
    a_path = ['p'] if a0 == 4 else ['alpha'] + ['a' + str(i) for i in range(a0 - 5)] + ['p']
    c_path = ['q'] if c0 == 4 else ['q'] + ['c' + str(i) for i in range(c0 - 5)] + ['beta']
    z_path = a_path + c_path
    assert set(m_path) & set(z_path) == {alpha, beta}
    boundary = m_path + list(reversed(z_path[1:-1]))
    assert len(boundary) == len(set(boundary)) == sg + tg + h - 6
    assert len(boundary) >= 9
    faces = [('m', a, b) for a, b in zip(m_path, m_path[1:])]
    faces += [('z', a, b) for a, b in zip(z_path, z_path[1:])]
    faces += [('m', 'z', alpha), ('m', 'z', beta)]
    edges = sorted({edge(a, b) for face in faces for a, b in itertools.combinations(face, 2)})
    vertices = boundary + ['m', 'z']
    boundary_edges = {edge(a, b) for a, b in zip(boundary, boundary[1:] + boundary[:1])}
    assert {e for e in edges if sum(e[0] in f and e[1] in f for f in faces) == 1} == boundary_edges
    assert all(sum(e[0] in f and e[1] in f for f in faces) == (1 if e in boundary_edges else 2) for e in edges)
    assert len(edges) == 3 * len(vertices) - len(boundary) - 3
    degrees = {v: sum(v in e for e in edges) for v in vertices}
    assert degrees['m'] == sg + tg - 5 and degrees['z'] == h + 3
    assert edge(alpha, beta) not in edges
    assert all(edge(p, q) not in edges for p in ('p', 'q') for q in ('v', 'w'))
    full = all_colourings(vertices, edges)
    indexed = {}
    for row in full:
        indexed.setdefault(row[:-2], []).append(row[-2:])
    fibres = []
    distinct_endpoint_nonempty = 0
    for row in itertools.product(range(4), repeat=len(boundary)):
        if any(row[i] == row[(i + 1) % len(row)] for i in range(len(row))):
            continue
        colouring = dict(zip(boundary, row))
        am = sorted(set(range(4)) - {colouring[v] for v in m_path})
        az = sorted(set(range(4)) - {colouring[v] for v in z_path})
        pairs = [(a, b) for a in am for b in az if a != b]
        assert len(am) <= 2 and len(az) <= 2
        assert pairs == indexed.get(row, [])
        details = []
        for m, z in pairs:
            f = colouring | {'m': m, 'z': z}
            allowed, r, values = source_palette(f)
            details.append({'hub_pair': [m, z], 'full_J_patch_colouring': list(row) + [m, z],
                            'all_r_lifts': [r], 'all_r_source_allowed': allowed})
            if colouring[alpha] != colouring[beta]:
                assert values[2] == colouring[alpha] ^ colouring[beta]
        if pairs and colouring[alpha] != colouring[beta]:
            distinct_endpoint_nonempty += 1
        fibres.append({'boundary_row': row, 'A_m': am, 'A_z': az,
                       'all_hub_pairs_including_empty': pairs, 'all_full_lifts': details})
    assert len(fibres) == 3 ** len(boundary) + 3 * (-1) ** len(boundary)
    assert sum(len(f['all_full_lifts']) for f in fibres) == len(full)
    return {'scope': 'two-star-patch calibration, not a sphere or minimum source',
            'parameters': {'a0': a0, 'c0': c0, 'dG_s': sg, 'dG_t': tg, 'h': h},
            'alpha': alpha, 'beta': beta, 'boundary': boundary, 'vertices': vertices,
            'm_link_without_z': m_path, 'z_link_without_m': z_path,
            'faces': faces, 'edges': edges, 'degrees': degrees,
            'all_complete_patch_colourings': full, 'full_count': len(full),
            'all_proper_boundary_fibres_including_empty': fibres,
            'other_4^L_boundary_assignments': 'empty because an original boundary edge is monochromatic',
            'empty_fibre_count': sum(not f['all_full_lifts'] for f in fibres),
            'distinct_alpha_beta_nonempty_fibres': distinct_endpoint_nonempty}


def build():
    inputs = json.loads((HERE / 'INPUTS.json').read_text())
    assert inputs['base'] == BASE
    for item in inputs['entries']:
        assert digest(HERE / item['frozen_path']) == item['sha256']
        assert digest(REPO / item['path']) == item['sha256']
    sectors = [
        {'a_is_v': False, 'b_is_w': False, 'forced_inside': ['v', 'w'], 'outcome': 'contradicts proper C5 at most one interior vertex'},
        {'a_is_v': True, 'b_is_w': False, 'forced_inside': ['w'], 'outcome': 'W5 forces forbidden sw'},
        {'a_is_v': False, 'b_is_w': True, 'forced_inside': ['v'], 'outcome': 'W5 forces forbidden tv'},
        {'a_is_v': True, 'b_is_w': True, 'forced_inside': [], 'outcome': 'the retained facial triangle mvw'}]
    return {'base': BASE, 'inputs_sha256': digest(HERE / 'INPUTS.json'),
            'checker_sha256': digest(Path(__file__)), 'input_drift': 0,
            'cross_edge_cases': sectors, 'all_proper_six_pin_rows': local_six_rows(),
            'patch_controls': [patch(a, c) for a, c in [(5, 6), (4, 7), (7, 4)]],
            'source_count': 0, 'source_status': 'not triggered',
            'paper_scope': 'arbitrary-size source geometry; finite checks validate the interface algebra only',
            'complete_319_exclusion': 'OPEN'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = ap.parse_args()
    result = json.loads(json.dumps(build()))
    if args.write:
        with args.certificate.open('x') as f:
            json.dump(result, f, sort_keys=True, separators=(',', ':'))
            f.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == result, 'certificate mismatch'
    print(json.dumps({'status': 'PASS', 'proper_six_pin_rows': 432, 'all_r_allowed': 240,
                      'patches': [{'parameters': p['parameters'], 'full_count': p['full_count'],
                                   'empty_fibres': p['empty_fibre_count']} for p in result['patch_controls']],
                      'source_status': 'not triggered', 'input_drift': 0}, sort_keys=True))


if __name__ == '__main__':
    main()
