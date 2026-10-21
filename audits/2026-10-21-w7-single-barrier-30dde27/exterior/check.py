#!/usr/bin/env python3
"""Same-exterior strip recoloring and exact original-cap acceptance kernel.

This is not a new source-graph or noncrossing-partition enumeration.
Every cap fibre, including empty rows, is retained for each strip extension.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import gzip
import importlib.util
import json
import random
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = '30dde27293b5d3ad63c75fae73cda5be96db705b'
CAP = 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/caps.json.gz'
COLLAR = 'audits/2026-10-21-w7-profile0-13e51db/check.py'
P = ('n', 'u4', 'u3', 'u2', 'u1', 'L')
RIM = ('a', *P, 'q', 'c', 's', 'v', 'w', 't')
TAIL = ('c', 's', 'v', 'w', 't')
ORIGINAL = (1, 2, 1, 2, 1, 2)
ROWS = ('01012', '01021', '01023', '01201', '01202', '01203',
        '01212', '01213', '01231', '01232')
FORBIDDEN = {'G': {'01021', '01202', '01212'},
             'Q1': {'01232'}, 'J1': {'01202', '01212'}}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def packed(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def canonical(colors):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in colors)


def inputs():
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base'] == BASE, 'exclusive BASE changed')
    for row in manifest['inputs']:
        raw = (HERE / 'frozen' / row['path']).read_bytes()
        require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                'frozen input changed: ' + row['path'])
    spec = importlib.util.spec_from_file_location('frozen_original_collar', HERE / 'frozen' / COLLAR)
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    require(source.P == list(P), 'ordered original P changed')
    cap = json.load(gzip.open(HERE / 'frozen' / CAP, 'rt'))
    require(tuple(cap['ordered_rim']) == RIM, 'ordered original cap rim changed')
    require(len(cap['states']) == 66430, 'old cap state coverage changed')
    return source, cap


@lru_cache(None)
def full_caps(rim):
    """Direct full cap edge constraints, independently of old count matrices."""
    colors = dict(zip(RIM, rim))
    a, n, L, q, c, s, v, w, t = (colors[x] for x in
                                   ('a', 'n', 'L', 'q', 'c', 's', 'v', 'w', 't'))
    allowed_R = set(range(4)) - {colors[x] for x in P}
    right = [(x, y, r) for x, y, r in product(range(4), repeat=3)
             if r not in (s, v, w, t, x, y) and x not in (c, s, y)
             and y not in (a, t)]
    left = {'G': [(b, p, h, R) for b, p, h, R in product(range(4), repeat=4)
                  if R in allowed_R and b not in (a, c, q, p)
                  and p not in (a, q, n, h) and h not in (q, L, R, n)],
            'Q1': [(b, R) for b, R in product(range(4), repeat=2)
                   if R in allowed_R and b == n and R == q
                   and b not in (a, c, q)],
            'J1': [(b, R) for b, R in product(range(4), repeat=2)
                   if R in allowed_R and b == L and a != R
                   and b not in (a, c, q)]}
    out = {g: {row: [] for row in ROWS} for g in FORBIDDEN}
    for g, lifts in left.items():
        for lift in lifts:
            b = lift[0]
            for x, y, r in right:
                row = ''.join(map(str, canonical((x, y, a, b, c))))
                require(row in ROWS, 'full lift has a nonproper C5 frame')
                out[g][row].append([*lift, x, y, r])
    for g in out:
        for row in ROWS:
            out[g][row].sort()
    return out


def strip_extensions(domains, rng=None, a=0, q=3):
    lists = [sorted(row) for row in domains]
    if rng:
        for row in lists:
            rng.shuffle(row)
    return sorted(tuple(row) for row in product(*lists)
                  if row[0] != a and row[-1] != q
                  and all(a != b for a, b in zip(row, row[1:])))


def signature_domains(profile, center, beta, a=0):
    """Arbitrary-K complete six-list relation for exactly one barrier.

    beta=None: its sector contains both 03 colors, so the center is pinned.
    beta=0/3: its whole sector is (beta, barrier, beta), so it has two colors.
    """
    domains = [{1, 2} for _ in P]
    if profile == 1:
        domains[0] = set(range(4)) - {a}  # Complete n-star includes a-u4 ear.
    j = P.index(center)
    domains[j] = {ORIGINAL[j]} if beta is None else {ORIGINAL[j], 3 - beta}
    return domains


def kernel_case(profile, center, beta, tip, cap, state_index, rng, a=0, q=3):
    domains = signature_domains(profile, center, beta, a)
    extensions = strip_extensions(domains, rng, a, q)
    require(tuple(ORIGINAL) in extensions, 'original target lift was lost')
    records = []
    for extension in extensions:
        e0, e1 = (3-q, 1) if tip == 'v' else (1, 3-q)
        rim = (a, *extension, q, 1, 2, e0, e1, 2)
        state = state_index[canonical(rim)]
        fibres = full_caps(rim)
        for g in FORBIDDEN:
            require([len(fibres[g][row]) for row in ROWS]
                    == [matrix[state] for matrix in cap['matrices'][g]],
                    'direct full cap lifts differ from frozen original matrices')
        bad = [{'graph': g, 'row': row, 'lift': fibres[g][row][0]}
               for g in FORBIDDEN for row in sorted(FORBIDDEN[g]) if fibres[g][row]]
        records.append({'P_colors': list(extension), 'old_C13_state': state,
                        'complete_cap_fibres': fibres, 'forbidden_witnesses': bad})
    return {'profile': profile, 'center': center, 'same_neighbor_03': beta,
            'a_color': a, 'q_color': q,
            'target_q_tip': tip, 'complete_P_lists': [sorted(x) for x in domains],
            'complete_strip_extensions': records,
            'same_exterior_source_branch_excluded': any(r['forbidden_witnesses'] for r in records)}


def compositions(total, width):
    if width == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, width - 1):
                yield (first, *tail)


def topology(source, profile, counts):
    data, whole = source.collar(profile, counts, with_graph=True)
    A = data['boundary'][1:]
    vertices = set(A) | set(P)
    graph = {v: whole[v] & vertices for v in vertices}
    triangles = [tuple(t) for t in combinations(sorted(graph), 3)
                 if all(b in graph[a] for a, b in combinations(t, 2))]
    edges = Counter(tuple(sorted(e)) for face in triangles for e in combinations(face, 2))
    boundary = ['a', *P, 'q', *reversed(A[1:-1])]
    expected_edges = {tuple(sorted((boundary[i], boundary[(i + 1) % len(boundary)])))
                      for i in range(len(boundary))}
    require(len(boundary) == len(set(boundary)) == len(graph), 'strip is not an all-boundary polygon')
    require({edge for edge, n in edges.items() if n == 1} == expected_edges,
            'strip triangle gluing has the wrong boundary')
    require(all(n in (1, 2) for n in edges.values()), 'invalid strip face incidence')
    require(len(graph) - len(edges) + len(triangles) == 1, 'strip disk Euler identity')
    K = sum(counts)
    require(len(triangles) == (11 if profile == 0 else 10) + K, 'strip triangle count')
    require(len(A) - 1 == (6 if profile == 0 else 5) + K, 'A length')
    e_boundary = [*A, *TAIL]
    require(len(e_boundary) == (12 if profile == 0 else 11) + K, 'complete exterior boundary')
    require(('a' in graph['u4']) == (profile == 1), 'profile1 a-u4 ear lost')
    return {'profile': profile, 'H_lengths': list(counts), 'A': A,
            'strip_vertices': len(graph), 'strip_triangles': len(triangles),
            'ordered_exterior_boundary': e_boundary}


def actual_single_barrier(source, profile, counts, y):
    data, graph = source.collar(profile, counts, with_graph=True)
    A = data['boundary'][1:]
    center = next(t for t in P if t in graph[y])
    colors = {'a': 0, 'q': 3, y: 3 - ORIGINAL[P.index(center)]}
    iy = A.index(y)
    for i in range(1, iy):
        colors[A[i]] = 3 - colors[A[i - 1]]
    for i in range(len(A) - 2, iy, -1):
        colors[A[i]] = 3 - colors[A[i + 1]]
    domains = [set(range(4)) - {colors[v] for v in graph[t] if v in colors} for t in P]
    barrier_sector_length = sum(v.startswith('H') and center in graph[v] for v in A)
    beta = colors[A[iy - 1]] if barrier_sector_length == 1 and colors[A[iy - 1]] == colors[A[iy + 1]] else None
    require(domains == signature_domains(profile, center, beta), 'arbitrary-K signature missed a full list')
    require(all(colors[a] != colors[b] for a, b in zip(A, A[1:])), 'improper one-barrier A')
    return center, beta, colors


def compute(seed):
    source, cap = inputs()
    rng = random.Random(seed) if seed is not None else None
    index = {tuple(t): i for i, t in enumerate(cap['states'])}
    kernel = []
    for profile in (0, 1):
        for center in (P if profile == 0 else P[1:]):
            # Endpoint beta is fixed by a=0, q=3; the first profile1 sector begins at a.
            betas = [None, 0] if center == 'n' or (profile == 1 and center == 'u4') else [None, 3] if center == 'L' else [None, 0, 3]
            for beta in betas:
                for tip in ('v', 'w'):
                    kernel.append(kernel_case(profile, center, beta, tip, cap, index, rng))
    require(len(kernel) == 58, 'complete signature kernel coverage changed')
    lookup = {(r['profile'], r['center'], r['same_neighbor_03'], r['target_q_tip']): i
              for i, r in enumerate(kernel)}
    phase_kernel = []
    for a, q in product((0, 3), repeat=2):
        for profile in (0, 1):
            for center in (P if profile == 0 else P[1:]):
                betas = [None, a] if center == 'n' or (profile == 1 and center == 'u4') else [None, q] if center == 'L' else [None, 0, 3]
                for beta in betas:
                    for tip in ('v', 'w'):
                        phase_kernel.append(kernel_case(profile, center, beta, tip, cap, index, rng, a, q))
    require(len(phase_kernel) == 232, 'four-phase signature coverage changed')
    phase_lookup = {(r['profile'], r['center'], r['same_neighbor_03'],
                     r['target_q_tip'], r['a_color'], r['q_color']): i
                    for i, r in enumerate(phase_kernel)}
    topology_cases, signature_calibration, phase_calibration, k1 = [], [], [], []
    for profile, width in ((0, 6), (1, 5)):
        for K in range(4):
            for counts in compositions(K, width):
                topo = topology(source, profile, counts)
                topology_cases.append(topo)
                for y in [v for v in topo['A'] if v.startswith('H')]:
                    center, beta, colors = actual_single_barrier(source, profile, counts, y)
                    signature_calibration.append([profile, list(counts), y, center, beta])
                    iy = topo['A'].index(y)
                    phase_ids = []
                    for flip_a, flip_q in product((0, 1), repeat=2):
                        current = {v: (3-c if (topo['A'].index(v) < iy and flip_a) or
                                              (topo['A'].index(v) > iy and flip_q) else c)
                                   for v, c in colors.items()}
                        # A length >=2 always retains a 03-03 edge within this sector.
                        _, source_graph = source.collar(profile, counts, with_graph=True)
                        sector_size = sum(v.startswith('H') and center in source_graph[v] for v in topo['A'])
                        phase_beta = current[topo['A'][iy - 1]] if sector_size == 1 and current[topo['A'][iy - 1]] == current[topo['A'][iy + 1]] else None
                        actual_domains = [set(range(4)) - {current[v] for v in source_graph[t] if v in current} for t in P]
                        require(actual_domains == signature_domains(profile, center, phase_beta, current['a']),
                                'complete-component phase changed a list outside short signature')
                        ids = [phase_lookup[profile, center, phase_beta, tip, current['a'], current['q']]
                               for tip in ('v', 'w')]
                        phase_ids.append({'flip_a': flip_a, 'flip_q': flip_q, 'kernel_indices': ids})
                        phase_calibration.append([profile, list(counts), y, flip_a, flip_q, phase_beta, ids])
                    if K == 1:
                        k1.append({'profile': profile, 'center': center, 'barrier': y,
                                   'A_colors': [colors[v] for v in topo['A']],
                                   'kernel_indices': [lookup[profile, center, beta, tip] for tip in ('v', 'w')],
                                   'four_complete_03_phase_kernel_indices': phase_ids,
                                   'excluded_after_some_complete_03_phase': any(phase_kernel[i]['same_exterior_source_branch_excluded'] for row in phase_ids for i in row['kernel_indices']),
                                   'excluded_for_both_targets': all(kernel[lookup[profile, center, beta, tip]]['same_exterior_source_branch_excluded'] for tip in ('v', 'w'))})
    require(len(topology_cases) == 140 and len(k1) == 11, 'bounded structural coverage')
    require([(r['profile'], r['center']) for r in k1 if r['excluded_for_both_targets']]
            == [(0, 'u2'), (0, 'u4'), (0, 'n')],
            'K1 exclusion set changed')
    expected = lambda r: (r['same_neighbor_03'] is not None and
                         ((r['profile'] == 0 and (r['center'] == 'n' or
                           (r['center'] in P[1:5] and r['same_neighbor_03'] == 3))) or
                          (r['profile'] == 1 and r['center'] in P[2:5])))
    require(all(r['same_exterior_source_branch_excluded'] == expected(r) for r in kernel),
            'arbitrary-K finite-signature classification changed')
    require(all(r['same_exterior_source_branch_excluded'] ==
                (r['a_color'] != r['q_color'] and r['same_neighbor_03'] is not None and
                 ((r['profile'] == 0 and (r['center'] == 'n' or
                   (r['center'] in P[1:5] and r['same_neighbor_03'] == r['q_color']))) or
                  (r['profile'] == 1 and r['center'] in P[2:5])))
                for r in phase_kernel), 'four-phase cap classification changed')
    require(all(r['excluded_after_some_complete_03_phase'] == r['excluded_for_both_targets'] for r in k1),
            'four-phase K1 exclusion scope changed')
    # A selected original target D-coloring itself does not need to extend to G.
    require(all(not next(x for x in r['complete_strip_extensions']
                         if x['P_colors'] == list(ORIGINAL))['forbidden_witnesses']
                for r in kernel), 'target itself was confused with a forbidden G extension')
    return {'base': BASE, 'scope': 'same actual E retained; complete strip recoloring followed by original full caps',
            'finite_signature_kernel': kernel, 'four_phase_signature_kernel': phase_kernel,
            'topology_calibration': topology_cases,
            'arbitrary_K_list_signature_calibration': signature_calibration,
            'four_phase_signature_calibration': phase_calibration,
            'K1_eleven_positions': k1,
            'K1_excluded_positions': [[r['profile'], r['center']] for r in k1 if r['excluded_for_both_targets']],
            'negative_controls': {'wrong_K1_neighbor_phase_rejected': True,
                                  'profile1_n_singleton_domain_rejected': True,
                                  'omit_complete_strip_lift_rejected': True},
            'source_profile0_excluded': False, 'source_profile1_excluded': False,
            'new_source_realization': False, 'general_W7_excluded': False,
            'new_Lean': False, 'new_NC_enumeration': False}


def controls(result):
    # Explicitly recompute each polluted claim and require a mismatch.
    k1 = result['K1_eleven_positions']
    phases = []
    for row in k1:
        colors = row['A_colors']
        iy = next(i for i, c in enumerate(colors) if c in (1, 2))
        phases.append(colors[iy - 1] == colors[iy + 1])
    require(phases == [row['profile'] == 0 for row in k1], 'true K1 phase failed')
    require(phases != [row['profile'] == 1 for row in k1], 'wrong phase control not rejected')
    row = next(r for r in result['finite_signature_kernel'] if r['profile'] == 1 and r['same_neighbor_03'] is None)
    true = [r['P_colors'] for r in row['complete_strip_extensions']]
    polluted_domains = [set(x) for x in row['complete_P_lists']]
    polluted_domains[0] = {1}
    require(strip_extensions(polluted_domains) != [tuple(x) for x in true],
            'profile1 complete n-star negative control failed')
    row = next(r for r in result['finite_signature_kernel'] if r['same_exterior_source_branch_excluded'])
    actual = row['complete_strip_extensions']
    require([r for r in actual if not r['forbidden_witnesses']] != actual,
            'deleted full-lift negative control failed')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--build', action='store_true')
    ap.add_argument('--seed', type=int)
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate-v2.json')
    args = ap.parse_args()
    result = compute(args.seed)
    controls(result)
    if args.build:
        with args.certificate.open('xb') as f:
            f.write(packed(result))
    require(json.loads(args.certificate.read_text()) == result, 'certificate missing, corrupted, or incomplete')
    print(json.dumps({'result': 'PASS', 'signature_cases': len(result['finite_signature_kernel']),
                      'four_phase_signature_cases': len(result['four_phase_signature_kernel']),
                      'topology_cases': len(result['topology_calibration']),
                      'single_barrier_signature_calibration': len(result['arbitrary_K_list_signature_calibration']),
                      'K1_positions': 11, 'K1_excluded': result['K1_excluded_positions'],
                      'whole_profiles_still_OPEN': [0, 1], 'negative_controls': result['negative_controls']}, sort_keys=True))


if __name__ == '__main__':
    main()
