#!/usr/bin/env python3
"""Exhaustive bounded target collar colors; no exterior/source realization.

The ordered original collar is imported from frozen BASE bytes.  Every target
proper coloring is stored, and every unrestricted local H lift above its full
S color word is stored by index in the complete 504-entry wheel kernel.
"""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
from math import comb
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
SOURCE = 'audits/2026-10-21-w7-profile0-13e51db'
PRIVATE = 'audits/2026-10-21-w7-private-face-points-d23f94f'
C = ['n', 'h', 'L', 'u1', 'u2', 'u3', 'u4']
P = ['n', 'u4', 'u3', 'u2', 'u1', 'L']
TARGET = dict(zip(P, [1, 2, 1, 2, 1, 2]))
MAX_K = 5


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def inputs():
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base'] == BASE, 'exclusive BASE changed')
    for row in manifest['inputs']:
        raw = (HERE / 'frozen' / row['path']).read_bytes()
        require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                'frozen input drift: ' + row['path'])
    private = json.loads((HERE / 'frozen' / PRIVATE / 'certificate.json').read_text())
    require(private['all_zi_color_domain_in_both_targets'] == [0, 3], 'z domain changed')
    for row, sid, tip in zip(private['whole_original_target_03_forcing'],
                            [44459, 44466], ['v', 'w']):
        require(row['state'] == sid and row['all_03_boundary_component_contacts']
                == [['a'], ['q', tip]], 'full original target contacts changed')
        require(row['literal_tuple'][:8] == [0, 1, 2, 1, 2, 1, 2, 3],
                'fixed target color frame changed')
    spec = importlib.util.spec_from_file_location('frozen_collar', HERE / 'frozen' / SOURCE / 'check.py')
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    require(source.C == C and source.P == P, 'ordered collar source changed')
    return source


def compositions(total, width):
    if width == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, width - 1):
                yield (first,) + tail


def multiply(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def predicted(counts):
    poly = [1]
    for k in counts:
        local = [comb(k + 1 - j, j) for j in range((k + 1) // 2 + 1)]
        poly = multiply(poly, local)
        require(sum(x * 2 ** j for j, x in enumerate(local))
                == (2 ** (k + 2) + (-1) ** (k + 1)) // 3,
                'closed independent-set formula changed')
    return {str(b): coefficient * 2 ** (b - 1)
            for b, coefficient in enumerate(poly) if b and coefficient}


def is_proper(graph, colors):
    return all(colors[a] != colors[b] for a in graph for b in graph[a])


def components03(graph, colors):
    unseen = {v for v in graph if colors[v] in (0, 3)}
    out = []
    while unseen:
        todo, seen = [min(unseen)], set()
        while todo:
            v = todo.pop()
            if v in seen:
                continue
            seen.add(v)
            todo.extend(w for w in graph[v] if w in unseen and w not in seen)
        unseen -= seen
        out.append(sorted(seen))
    return sorted(out)


def separated(comps):
    return not any('a' in row and 'q' in row for row in comps)


def kernel_data():
    kernel = [[r, list(colors)] for r in range(4)
              for colors in product([c for c in range(4) if c != r], repeat=7)
              if all(colors[i] != colors[(i + 1) % 7] for i in range(7))]
    require(len(kernel) == 504, 'wheel kernel is not complete')
    bits = [[sum(1 << j for j, (_, colors) in enumerate(kernel) if colors[i] == c)
             for c in range(4)] for i in range(7)]
    target_ids = {i for i, (r, colors) in enumerate(kernel)
                  if all(colors[C.index(v)] == col for v, col in TARGET.items())}
    require(len(target_ids) == 2, 'P-restricted wheel candidates changed')
    return kernel, bits, target_ids


def full_lifts(graph, sigma, bits):
    mask = (1 << 504) - 1
    for i, t in enumerate(C):
        blocked = {sigma[v] for v in graph[t] if v in sigma}
        allowed = sum(bits[i][c] for c in range(4) if c not in blocked)
        mask &= allowed
    out = []
    while mask:
        bit = mask & -mask
        out.append(bit.bit_length() - 1)
        mask -= bit
    return out


def shape_case(source, profile, counts, bits, target_ids, rng):
    data, graph = source.collar(profile, counts, with_graph=True)
    boundary = data['boundary']
    path = boundary[1:]
    z = ['a' if profile else 'z1', 'z2', 'z3', 'z4', 'z5']
    h_nodes = [v for v in boundary if v.startswith('H')]
    centers = {v: next(t for t in P if t in graph[v]) for v in h_nodes}
    dgraph = {v: graph[v] - {'p', 'h', 'R'} for v in graph if v not in {'p', 'h', 'R'}}
    fixed = {'p': 2, 'a': 0, 'q': 3, **TARGET}
    hist, variants, center_hist = Counter(), Counter(), Counter()
    all_lifts_hist = Counter()
    records = []
    domains = {}
    for v in path:
        domain = [fixed[v]] if v in fixed else ([0, 3] if v in z else [c for c in range(4) if c != TARGET[centers[v]]])
        if rng:
            rng.shuffle(domain)
        domains[v] = domain

    def visit(i, assigned):
        if i != len(path):
            v = path[i]
            for col in domains[v]:
                if i == 0 or col != assigned[path[i - 1]]:
                    visit(i + 1, assigned | {v: col})
            return
        sigma = {'p': 2, **assigned}
        colors = {**sigma, **TARGET}
        require(is_proper(dgraph, colors), 'enumeration produced improper D-intersection coloring')
        barriers = [v for v in h_nodes if sigma[v] in (1, 2)]
        b = len(barriers)
        comps = components03(dgraph, colors)
        sep = separated(comps)
        require(sep == bool(b), 'barrier/separation equivalence failed')
        require(len(comps) == b + 1, '03 components are not the consecutive runs')
        require(all(sigma[v] == 3 - TARGET[centers[v]] for v in barriers), 'barrier is not opposite color')
        lift_ids = full_lifts(graph, sigma, bits)
        matched = sorted(set(lift_ids) & target_ids)
        require(len(matched) == 1, 'a literal target color word lost its unique target lift')
        full_colors = {**colors, 'h': 0, 'R': 3}
        require(is_proper(graph, full_colors), 'forced target lift is not a full proper H coloring')
        require(all(not(v in barriers and w in barriers) for v in h_nodes for w in graph[v]),
                'neighboring same-center barriers accepted')
        all_lifts_hist[str(len(lift_ids))] += 1
        if sep:
            hist[str(b)] += 1
            center_set = tuple(t for t in P if t in {centers[v] for v in barriers})
            center_hist[','.join(center_set)] += 1
            variants['all_separated'] += 1
            if b == 1:
                variants['exactly_one_barrier'] += 1
            if len(center_set) == 1:
                variants['one_barrier_center'] += 1
            if len(center_set) > 1:
                variants['at_least_two_barrier_centers'] += 1
            if len({sigma[v] for v in z}) == 1:
                variants['all_z_same_color'] += 1
            if all(sigma[a] != sigma[b] for a, b in zip(z, z[1:])):
                variants['z_colors_alternate'] += 1
            if len(center_set) == len([k for k in counts if k]):
                variants['every_nonempty_H_has_a_barrier'] += 1
        else:
            variants['all_H_03_relaxed_separation'] += 1
        # Complete literal S words and complete unrestricted local H fibres.
        # Everything else can be recomputed from the original ordered graph.
        records.append([[sigma[v] for v in boundary], lift_ids])

    visit(0, {})
    records.sort(key=lambda x: x[0])
    expected = predicted(counts)
    require(dict(hist) == expected, 'literal enumeration disagrees with arbitrary-K formula')
    require(hist.get('1', 0) == sum(counts), 'each single barrier position is not exactly once')
    expected_zero = int(((6 if profile == 0 else 5) + sum(counts)) % 2 == 1)
    require(variants['all_H_03_relaxed_separation'] == expected_zero, 'zero-barrier path parity changed')
    require(len(records) == sum(hist.values()) + expected_zero, 'a local proper coloring was omitted')
    return {'profile': profile, 'K': sum(counts), 'H_lengths': list(counts),
            'H_order': (['n'] if profile == 0 else []) + ['u4', 'u3', 'u2', 'u1', 'L'],
            'S': boundary, 'target_proper_colorings': len(records),
            'barrier_count_histogram': dict(sorted(hist.items())),
            'barrier_center_set_histogram': dict(sorted(center_hist.items())),
            'variants': dict(sorted(variants.items())),
            'full_H_lift_count_histogram': dict(sorted(all_lifts_hist.items())),
            'record_columns': ['ordered_S_colors', 'all_unrestricted_H_lift_kernel_indices'],
            'records': records}


def negative_controls(source):
    # Profile 1, K=0 is properly colored, but has the forbidden a-q 03 path.
    data, graph = source.collar(1, [0] * 5, with_graph=True)
    colors = {'p': 2, 'a': 0, 'z2': 3, 'z3': 0, 'z4': 3, 'z5': 0, 'q': 3, **TARGET}
    dgraph = {v: graph[v] - {'p', 'h', 'R'} for v in graph if v not in {'p', 'h', 'R'}}
    require(is_proper(dgraph, colors), 'zero-barrier negative control not proper')
    require(not separated(components03(dgraph, colors)), 'zero-barrier negative control falsely separated')
    # A true barrier cannot be flipped without its actual whole 12 component.
    data2, graph2 = source.collar(1, [1, 0, 0, 0, 0], with_graph=True)
    colors2 = {'p': 2, 'a': 0, 'H1_0': 1, 'z2': 3, 'z3': 0, 'z4': 3,
               'z5': 0, 'q': 3, **TARGET}
    dgraph2 = {v: graph2[v] - {'p', 'h', 'R'} for v in graph2 if v not in {'p', 'h', 'R'}}
    require(is_proper(dgraph2, colors2), 'single-barrier control not proper')
    require(separated(components03(dgraph2, colors2)), 'single barrier fails to separate')
    bad = colors2 | {'H1_0': 2}
    require(not is_proper(dgraph2, bad), 'single private-point 12 flip wrongly accepted')
    whole = {v for v in dgraph2 if colors2[v] in (1, 2)}
    flipped = {v: (3 - col if v in whole else col) for v, col in colors2.items()}
    require(is_proper(dgraph2, flipped), 'whole local 12 component flip failed')
    # Two barriers in one H would be adjacent and equal, hence cannot be proper.
    data3, graph3 = source.collar(1, [2, 0, 0, 0, 0], with_graph=True)
    wrong = {**colors2, 'H1_1': 1}
    dgraph3 = {v: graph3[v] - {'p', 'h', 'R'} for v in graph3 if v not in {'p', 'h', 'R'}}
    require(not is_proper(dgraph3, wrong), 'adjacent barriers wrongly accepted')
    return {'zero_barrier_proper_but_not_separated': True,
            'single_barrier_flip_rejected': True, 'whole_12_component_flip_proper': True,
            'adjacent_same_center_barriers_rejected': True,
            'all_passed': True}


def compute(seed):
    source = inputs()
    kernel, bits, target_ids = kernel_data()
    shapes = [(profile, counts) for profile, width in [(0, 6), (1, 5)]
              for k in range(MAX_K + 1) for counts in compositions(k, width)]
    rng = random.Random(seed) if seed is not None else None
    if rng:
        rng.shuffle(shapes)
    cases = [shape_case(source, profile, counts, bits, target_ids, rng) for profile, counts in shapes]
    cases.sort(key=lambda row: (row['profile'], row['K'], row['H_lengths']))
    require(len(cases) == 714, 'length-distribution coverage changed')
    totals = []
    for profile in (0, 1):
        for k in range(MAX_K + 1):
            rows = [row for row in cases if row['profile'] == profile and row['K'] == k]
            hist, variants, lifts = Counter(), Counter(), Counter()
            possible_centers = set()
            for row in rows:
                hist.update(row['barrier_count_histogram'])
                variants.update(row['variants'])
                lifts.update(row['full_H_lift_count_histogram'])
                for names in row['barrier_center_set_histogram']:
                    possible_centers.update(names.split(','))
            totals.append({'profile': profile, 'K': k, 'shapes': len(rows),
                           'target_proper_colorings': sum(row['target_proper_colorings'] for row in rows),
                           'barrier_count_histogram': dict(sorted(hist.items())),
                           'variants': dict(sorted(variants.items())),
                           'full_H_lift_count_histogram': dict(sorted(lifts.items())),
                           'possible_barrier_centers': [t for t in P if t in possible_centers]})
    return {'base': BASE, 'max_K': MAX_K, 'target_states': [44459, 44466],
            'same_local_data_only': True, 'wheel_kernel_columns': ['R_color', 'C_colors'],
            'ordered_C': C, 'wheel_kernel': kernel,
            'target_restricted_full_H_lifts_per_record': 1,
            'target_forced_completion': {'p': 2, 'h': 0, 'R': 3},
            'summary': totals, 'cases': cases,
            'negative_controls': negative_controls(source),
            'local_a_q_03_separation_is_necessary_only': True,
            'outside_E_constructed': False, 'source_realizability': False,
            'source_exclusions': [], 'full_arbitrary_S_relation_computed': False,
            'strict_smaller_bad': False, 'LP_run': False, 'new_Lean': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--seed', type=int)
    args = parser.parse_args()
    result = compute(args.seed)
    raw = encode(result)
    certificate = HERE / 'colorings.json.gz'
    summary = {key: value for key, value in result.items() if key not in {'cases', 'wheel_kernel'}}
    summary['shapes'] = len(result['cases'])
    summary['literal_S_words'] = sum(row['target_proper_colorings'] for row in result['cases'])
    summary['payload_sha256'] = sha256(raw).hexdigest()
    summary['payload_uncompressed_bytes'] = len(raw)
    if args.build:
        with certificate.open('xb') as stream:
            stream.write(gzip.compress(raw, compresslevel=9, mtime=0))
        with (HERE / 'certificate.json').open('x') as stream:
            json.dump(summary, stream, indent=2, sort_keys=True)
            stream.write('\n')
    require(gzip.decompress(certificate.read_bytes()) == raw, 'literal color/fibre certificate changed')
    require(json.loads((HERE / 'certificate.json').read_text()) == summary, 'summary certificate changed')
    print(json.dumps({'result': 'PASS', 'seed': args.seed, 'shapes': summary['shapes'],
                      'literal_S_words': summary['literal_S_words'],
                      'payload_sha256': summary['payload_sha256'],
                      'negative_controls': result['negative_controls'],
                      'source_exclusions': []}, sort_keys=True))


if __name__ == '__main__':
    main()
