#!/usr/bin/env python3
"""Independent named fibres for the representative and strength controls.

Imports only the independent fixed-order DFS, never controls/check.py or
controls/strength.py. Explicit edges are rebuilt here. Face orbits are checked
separately, allowing the repeated vertices on a legitimate bridge facial walk.
"""
from collections import Counter
import gzip
import json
from pathlib import Path

from check import BETAS, TAUS, all_lifts, cyclic, edges_from_intervals

ROOT = Path(__file__).resolve().parent.parent


def norm(edges):
    return sorted({tuple(sorted(edge)) for edge in edges})


def sphere(n, edges, faces, rotation):
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        assert a != b and 0 <= a < n and 0 <= b < n
        adjacency[a].add(b)
        adjacency[b].add(a)
    assert len(rotation) == n
    for v, neighbours in enumerate(rotation):
        assert len(neighbours) == len(set(neighbours))
        assert set(neighbours) == adjacency[v]
    unseen = {(a, b) for a in range(n) for b in adjacency[a]}
    derived = []
    while unseen:
        first = min(unseen)
        dart = first
        face = []
        while True:
            assert dart in unseen
            unseen.remove(dart)
            a, b = dart
            face.append(a)
            ns = rotation[b]
            dart = (b, ns[(ns.index(a) + 1) % len(ns)])
            if dart == first:
                break
        derived.append(cyclic(face))
    assert Counter(derived) == Counter(map(cyclic, faces))
    assert n - len(edges) + len(faces) == 2
    assert cyclic([0, 4, 3, 2, 1]) in derived


def support(rows):
    return {(i, j) for i, row in enumerate(rows) for j, cell in enumerate(row['cells'])
            if cell and len(set(TAUS[j])) == 3}


def recompute(g, n, edges):
    assert g['vertices'] == list(range(n))
    assert g['B'] == list(range(5)) and g['U'] == list(range(5, 10))
    assert g['private'] == list(range(10, n))
    assert g['edges'] == list(map(list, edges))
    sphere(n, edges, g['faces'], g['rotation'])
    assert cyclic(list(range(5, 10))) in set(map(cyclic, g['faces']))
    we = norm(edges + [(u, n) for u in range(5, 10)])
    assert g['wheel_edges'] == list(map(list, we))
    sphere(n + 1, we, g['wheel_faces'], g['wheel_rotation'])
    expected_wf = Counter(map(cyclic, g['faces']))
    del expected_wf[cyclic(list(range(5, 10)))]
    expected_wf.update(cyclic([5 + i, 5 + (i + 1) % 5, n]) for i in range(5))
    assert expected_wf == Counter(map(cyclic, g['wheel_faces']))
    assert g['degree_G'] == [sum(v in e for e in we) for v in range(n + 1)]
    pe = [e for e in edges if e[0] >= 10]
    assert g['degree_private'] == [sum(v in e for e in pe) for v in range(10, n)]
    unvisited = set(range(10, n))
    components = 0
    while unvisited:
        components += 1
        stack = [min(unvisited)]
        while stack:
            v = stack.pop()
            if v not in unvisited:
                continue
            unvisited.remove(v)
            stack.extend(w for e in pe if v in e for w in e if w != v)
    assert g['rho_private'] == len(pe) - (n - 10) + components
    actual = []
    mask = 0
    for i, beta in enumerate(BETAS):
        cells = [[] for _ in TAUS]
        for lift in all_lifts(n, edges, beta, False):
            cells[int(lift[5:10], 4)].append(lift)
        wheel = all_lifts(n, edges, beta, True)
        actual.append({'beta': list(beta), 'cells': cells, 'wheel_full_lifts': wheel})
        if wheel:
            mask |= 1 << i
    assert g['rows'] == actual
    assert mask == g['Sigma'] == 1023
    return actual


def main():
    certificate = json.loads(gzip.decompress((ROOT / 'controls/strength.json.gz').read_bytes()))
    assert certificate['beta_order'] == list(map(list, BETAS))
    assert certificate['tau_order'] == list(map(list, TAUS))
    ring_edges = [(off + i, off + (i + 1) % 5) for off in (0, 5) for i in range(5)]
    prism_edges = norm(ring_edges + [(i, 5 + i) for i in range(5)])
    specifications = {
        'prism_representative_r0': (10, prism_edges),
        'triangulated_prism_r0': (10, norm(prism_edges + [((i + 1) % 5, 5 + i) for i in range(5)])),
        'prism_private_degree2': (11, norm(prism_edges + [(0, 10), (5, 10)])),
        'contractible_private_triangle_weaker_premises':
            (13, norm(prism_edges + [(0, 10), (10, 11), (11, 12), (10, 12)])),
        'essential_r5_weaker_premises': edges_from_intervals(((1, 1),) * 5),
    }
    graphs = {g['key']: g for g in certificate['graphs']}
    assert len(graphs) == len(certificate['graphs']) == 5
    assert set(graphs) == set(specifications)
    totals = Counter()
    rows = {}
    for key, (n, edges) in specifications.items():
        rows[key] = recompute(graphs[key], n, edges)
        for row in rows[key]:
            totals['A_lifts'] += sum(map(len, row['cells']))
            totals['G_lifts'] += len(row['wheel_full_lifts'])
            totals['empty_cells'] += sum(not c for c in row['cells'])

    prism = rows['prism_representative_r0']
    diagonal = rows['triangulated_prism_r0']
    plus = rows['prism_private_degree2']
    contractible = rows['contractible_private_triangle_weaker_premises']
    assert support(prism) != support(diagonal)
    assert support(prism) == support(plus) == support(contractible)
    for i in range(10):
        for j in range(1024):
            assert len(plus[i]['cells'][j]) == 2 * len(prism[i]['cells'][j])
            assert len(contractible[i]['cells'][j]) == 18 * len(prism[i]['cells'][j])

    witness = certificate['template_to_representative_R3_difference']
    letters = {'B': (1, 0), 'D': (1, 1), 'U': (0, 1)}
    n, edges = edges_from_intervals(tuple(letters[s] for s in witness['template']))
    beta, tau = tuple(witness['beta']), tuple(witness['tau'])
    source_cell = [lift for lift in all_lifts(n, edges, beta, False)
                   if tuple(map(int, lift[5:10])) == tau]
    rep_cell = prism[BETAS.index(beta)]['cells'][TAUS.index(tau)]
    assert source_cell == witness['template_full_lifts']
    assert rep_cell == witness['representative_full_lifts']
    assert bool(source_cell) != bool(rep_cell)
    assert len(set(tau)) == 3

    assert totals == {'A_lifts': 14380, 'G_lifts': 7260, 'empty_cells': 48965}
    print(json.dumps({
        'status': 'PASS independent all five graphs and full witness cell',
        'graphs': 5, 'cells': 51200, **dict(totals),
        'Sigma': {key: graphs[key]['Sigma'] for key in sorted(graphs)},
        'R3_support_sizes': {key: len(support(rows[key])) for key in sorted(rows)},
        'template_representative_R3_difference': witness,
        'same_R3_fibre_factors': {'degree2_decoration': 2, 'private_triangle': 18},
        'source_minimality': 'not triggered',
        'representative_strength': 'capped Sigma only',
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
