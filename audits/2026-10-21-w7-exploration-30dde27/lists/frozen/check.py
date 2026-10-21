#!/usr/bin/env python3
"""Exact contact-case coverage and local collar topology calibration.

No graph-source realization, LP, or bounded replacement search is performed.
The arbitrary-size original-source Jordan proof is in PROOF.md.
"""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
BASE = '13e51db3ec3d8d7ec7eeef60167afdc19ad956c4'
C = ['n', 'h', 'L', 'u1', 'u2', 'u3', 'u4']
P = ['n', 'u4', 'u3', 'u2', 'u1', 'L']


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edges(cycle):
    return {tuple(sorted((cycle[i], cycle[(i + 1) % len(cycle)])))
            for i in range(len(cycle))}


def check_inputs():
    manifest = json.loads((HERE / 'BASE.json').read_text())
    require(manifest['base'] == BASE, 'exclusive BASE changed')
    for row in manifest['inputs']:
        raw = (HERE / 'frozen' / row['path']).read_bytes()
        require(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                'frozen input drift: ' + row['path'])
    certificate = json.loads((HERE / 'frozen/audits/2026-10-21-w7-private-face-points-d23f94f/certificate.json').read_text())
    require(certificate['all_zi_color_domain_in_both_targets'] == [0, 3], 'target domain changed')
    for target, z0 in zip(certificate['whole_original_target_03_forcing'], ['v', 'w']):
        require(target['all_03_boundary_component_contacts'] == [['a'], ['q', z0]],
                'original full a/q separation changed')
    return len(manifest['inputs'])


def contact_cases():
    types = [frozenset([i]) for i in range(7)]
    types += [frozenset([i, (i + 1) % 7]) for i in range(7)]
    records = []
    for a, b in combinations(types, 2):
        if a & b:
            continue
        choices = [(i, j) for i in sorted(a) for j in sorted(b)
                   if (i - j) % 7 not in (0, 1, 6)]
        if choices:
            i, j = choices[0]
            arc1 = [(i + k) % 7 for k in range(1, (j - i) % 7)]
            arc2 = [(j + k) % 7 for k in range(1, (i - j) % 7)]
            require(arc1 and arc2, 'C5 arc omitted')
            require(set(arc1) | set(arc2) == set(range(7)) - {i, j}, 'C5 arc coverage')
            require(not (a & b), 'a forced common C5 center is permitted')
            records.append({'A_x': sorted(a), 'A_y': sorted(b), 'rule': 'C5',
                            'contacts_i_j': [i, j], 'opposite_open_C_arcs': [arc1, arc2]})
        else:
            require(len(a) == len(b) == 1, 'the C4 residual is not adjacent singleton')
            i, j = next(iter(a)), next(iter(b))
            require((i - j) % 7 in (1, 6), 'C4 contacts are not adjacent')
            records.append({'A_x': sorted(a), 'A_y': sorted(b), 'rule': 'C4',
                            'opposite_original_points': ['R', 'outside_third_point_of_ij']})
    return {'all_contact_types': [sorted(a) for a in types], 'disjoint_pair_cases': records,
            'C4_cases': sum(x['rule'] == 'C4' for x in records),
            'C5_cases': sum(x['rule'] == 'C5' for x in records)}


def connected(graph):
    seen, todo = set(), [next(iter(graph))]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(graph[v] - seen)
    return seen == set(graph)


def collar(profile, counts, with_graph=False):
    names = (['n'] if profile == 0 else []) + ['1', '2', '3', '4', 'L']
    H = {name: [f'H{name}_{j}' for j in range(size)] for name, size in zip(names, counts)}
    z = ['a' if profile == 1 else 'z1', 'z2', 'z3', 'z4', 'z5']
    arc = {'h': ['p', 'q'], 'L': [z[4], *H['L'], 'q']}
    arc['n'] = ['p', 'a', *reversed(H['n']), z[0]] if profile == 0 else ['p', 'a']
    for i in range(1, 5):
        arc[P[i]] = [z[i - 1], *H[str(i)], z[i]]
    boundary = ['p', 'a']
    if profile == 0:
        boundary += [*reversed(H['n']), z[0]]
    for i in range(1, 5):
        boundary += [*H[str(i)], z[i]]
    boundary += [*H['L'], 'q']
    faces = [('R', C[i], C[(i + 1) % 7]) for i in range(7)]
    thirds = ['p', 'q', z[4], z[3], z[2], z[1], z[0]]
    faces += [(C[i], C[(i + 1) % 7], thirds[i]) for i in range(7)]
    faces += [(center, a, b) for center, row in arc.items() for a, b in zip(row, row[1:])]
    incidence = Counter(e for f in faces for e in edges(f))
    require(all(k in (1, 2) for k in incidence.values()), 'a patch edge has invalid incidence')
    require({e for e, k in incidence.items() if k == 1} == edges(boundary), 'wrong unique boundary')
    graph = defaultdict(set)
    for a, b in incidence:
        graph[a].add(b)
        graph[b].add(a)
    require(connected(graph), 'patch is disconnected')
    require(len(graph) - len(incidence) + len(faces) == 1, 'disk Euler identity failed')
    require(set(graph) - set(boundary) == set(C) | {'R'}, 'eight original interior points changed')
    require(len(boundary) == len(set(boundary)), 'boundary repeats a point')
    require(len(boundary) == (8 if profile == 0 else 7) + sum(counts), 'collar length changed')
    require(len(faces) == 16 + len(boundary) - 2, 'exact triangular face count changed')
    for v in graph:
        link = defaultdict(set)
        for face in faces:
            if v in face:
                a, b = [x for x in face if x != v]
                link[a].add(b)
                link[b].add(a)
        require(connected(link), 'a full patch link is disconnected')
        degs = sorted(map(len, link.values()))
        expected = [1, 1] + [2] * (len(link) - 2) if v in boundary else [2] * len(link)
        require(degs == sorted(expected), 'a vertex link is not the required path/cycle')
    require(len(graph['R']) == 7 and len(graph['h']) == 5, 'original complete R/h stars changed')
    for v in C:
        require(len(graph[v]) == 3 + len(arc[v]), 'original complete C link size changed')
    require({e for e in incidence if set(e) <= set(boundary)} == edges(boundary),
            'a symbolic collar has a chord')
    row = {'profile': profile, 'H_lengths': dict(zip(names, counts)),
           'boundary': boundary, 'interior': C + ['R'], 'faces': len(faces)}
    return (row, graph) if with_graph else row


def canonical_cycle_colors(length):
    rows = []
    def visit(row):
        if len(row) == length:
            if row[-1] != row[0]:
                rows.append(row)
            return
        for color in range(min(3, max(row) + 1) + 1):
            if color != row[-1]:
                visit(row + [color])
    visit([0])
    return rows


def full_interface_controls():
    kernel = [(r, colors) for r in range(4)
              for colors in product([c for c in range(4) if c != r], repeat=7)
              if all(colors[i] != colors[(i + 1) % 7] for i in range(7))]
    require(len(kernel) == 504, 'full wheel lift candidate count changed')
    rows, marginal_failures = [], []
    for profile, width in [(0, 6), (1, 5)]:
        data, graph = collar(profile, [0] * width, with_graph=True)
        boundary = data['boundary']
        for colors in canonical_cycle_colors(len(boundary)):
            sigma = dict(zip(boundary, colors))
            allowed = [set(range(4)) - {sigma[s] for s in graph[t] if s in sigma} for t in C]
            formula = sum(all(c in domain for c, domain in zip(inner, allowed))
                          for r, inner in kernel)
            # Independent generic graph backtracking: no wheel decomposition.
            def count(assigned):
                remaining = set(graph) - assigned.keys()
                if not remaining:
                    return 1
                domains = {v: set(range(4)) - {assigned[w] for w in graph[v] if w in assigned}
                           for v in remaining}
                v = min(remaining, key=lambda x: (len(domains[x]), x))
                return sum(count(assigned | {v: color}) for color in domains[v])
            direct = count(sigma)
            require(direct == formula, 'seven-list formula lost a full lift or an empty fibre')
            rows.append({'profile': profile, 'ordered_S_colors': colors, 'full_lifts': direct})
            if direct == 0 and not any(row['profile'] == profile for row in marginal_failures):
                marginal_r = next((r for r in range(4) if all(domain - {r} for domain in allowed)), None)
                if marginal_r is not None:
                    marginal_failures.append({'profile': profile, 'ordered_S_colors': colors,
                                              'lists': [sorted(domain) for domain in allowed],
                                              'common_r_with_each_list_nonempty': marginal_r,
                                              'joint_full_lifts': 0})
    require(len(rows) == 365, 'whole local interface coloring coverage changed')
    require(len(marginal_failures) == 2, 'joint-versus-marginal negative controls are missing')
    return {'unrestricted_wheel_candidates': len(kernel), 'all_local_interface_counts': rows,
            'zero_fibres': sum(row['full_lifts'] == 0 for row in rows),
            'marginal_join_negative_controls': marginal_failures,
            'full_941_source_triggered': False}


def compute():
    inputs = check_inputs()
    cases = []
    for profile, width in [(0, 6), (1, 5)]:
        cases += [collar(profile, counts) for counts in product(range(3), repeat=width)
                  if sum(counts) <= 2]
    require(len(cases) == 49, 'local topology coverage changed')
    return {'base': BASE, 'frozen_inputs': inputs, 'contacts': contact_cases(),
            'local_topology_cases': cases, 'full_941_source_triggered_by_controls': False,
            'full_interface_controls': full_interface_controls(),
            'profile0_source_excluded': False, 'profile1_source_excluded': False,
            'smaller_source_constructed': False, 'new_Lean': False, 'LP_run': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    result = compute()
    path = HERE / 'certificate.json'
    if args.build:
        with path.open('x') as stream:
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write('\n')
    require(json.loads(path.read_text()) == result, 'certificate changed')
    print(json.dumps({'result': 'PASS', 'frozen_inputs': result['frozen_inputs'],
                      'contact_C4_cases': result['contacts']['C4_cases'],
                      'contact_C5_cases': result['contacts']['C5_cases'],
                      'local_topology_cases': len(result['local_topology_cases']),
                      'full_interface_count_cases': len(result['full_interface_controls']['all_local_interface_counts']),
                      'source_exclusions': []}, sort_keys=True))


if __name__ == '__main__':
    main()
