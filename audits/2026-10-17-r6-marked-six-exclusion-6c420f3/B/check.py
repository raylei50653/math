#!/usr/bin/env python3
"""Finite local calibration; no source-realizability or Jordan certificate."""
import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

P = Path(__file__).resolve().parent
R = P.parent


def edge(a, b):
    return tuple(sorted((a, b)))


def cap_record(boundary, banned, outside, distinguished, expected):
    rim = {edge(boundary[i], boundary[(i + 1) % 5]) for i in range(5)}
    diagonals = {edge(*e) for e in combinations(boundary, 2)} - rim

    def crosses(e, f):
        if set(e) & set(f):
            return False
        a, b = sorted(boundary.index(x) for x in e)
        c, d = sorted(boundary.index(x) for x in f)
        return a < c < b < d or c < a < d < b

    triangulations = [set(ds) for ds in combinations(sorted(diagonals), 2)
                      if not crosses(*ds)]
    assert len(triangulations) == 5
    retained = [ds for ds in triangulations if not ds & banned]
    assert len(retained) == 1 and retained[0] == expected
    all_edges = rim | retained[0]
    triangles = [tri for tri in combinations(boundary, 3)
                 if all(edge(*e) in all_edges for e in combinations(tri, 2))]
    assert len(triangles) == 3
    w5 = [(boundary[i], boundary[(i + 1) % 5], 'u') for i in range(5)]
    links = []
    for kind, faces in [('empty', triangles), ('W5', w5)]:
        adj = {}
        for tri in outside + faces:
            if distinguished not in tri:
                continue
            a, b = [x for x in tri if x != distinguished]
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)
        assert len(adj) == 5 and all(len(nbrs) == 2 for nbrs in adj.values())
        seen = set()
        stack = [next(iter(adj))]
        while stack:
            x = stack.pop()
            if x not in seen:
                seen.add(x)
                stack.extend(adj[x] - seen)
        assert seen == set(adj)
        links.append({'cap': kind, 'complete_neighbours': sorted(adj),
                      'complete_original_degree': len(adj),
                      'link_edges': sorted({edge(a, b) for a, ns in adj.items()
                                            for b in ns})})
    return {'boundary': boundary, 'all_empty_triangulations': 5,
            'forbidden_diagonals': sorted(banned),
            'retained_empty_diagonals': sorted(retained[0]),
            'fixed_exterior_faces': outside, 'complete_links': links}


def recompute():
    manifest = json.loads((R / 'INPUTS.json').read_text())
    checked = []
    for entry in manifest['entries']:
        path = R / entry['frozen_path']
        digest = sha256(path.read_bytes()).hexdigest()
        assert digest == entry['sha256'], 'frozen hash mismatch: ' + entry['path']
        checked.append({'path': entry['path'], 'sha256': digest})

    # Midpoints are labelled h1,h2; no v5 link restriction is imposed.
    names = ('v', 'w', 'p', 'q', 'h1', 'h2')
    marked = {edge('v', 'w'), edge('p', 'q')}
    banned = {edge(a, b) for a in ('v', 'w') for b in ('p', 'q')}
    cycles = set()
    for rest in permutations(names[1:]):
        cycle = ('v',) + rest
        es = {edge(cycle[i], cycle[(i + 1) % 6]) for i in range(6)}
        if marked <= es and not es & banned:
            cycles.add(min(cycle, ('v',) + tuple(reversed(rest))))
    assert len(cycles) == 4
    canonical = set()
    for cycle in cycles:
        rename = {}
        def normalized(x):
            if x in ('h1', 'h2'):
                return rename.setdefault(x, 'h' + str(len(rename) + 1))
            return x
        canonical.add(tuple(normalized(x) for x in cycle))
    assert canonical == {('v', 'h1', 'p', 'q', 'h2', 'w'),
                         ('v', 'h1', 'q', 'p', 'h2', 'w')}

    # Endpoint identities change the shared star-path names, not terminals.
    endpoint_orders = []
    for alpha_p, beta_q in product((False, True), repeat=2):
        alpha = 'p' if alpha_p else 'alpha'
        beta = 'q' if beta_q else 'beta'
        pm = [alpha, 'w', 'v', beta]
        pz = [alpha] + ([] if alpha_p else ['p'])
        pz += ['q'] + ([] if beta_q else [beta])
        boundary = pm + list(reversed(pz))[1:-1]
        assert len(boundary) == len(set(boundary))
        terminal_order = [x for x in boundary if x in {'w', 'v', 'q', 'p'}]
        k = terminal_order.index('w')
        terminal_order = terminal_order[k:] + terminal_order[:k]
        assert terminal_order == ['w', 'v', 'q', 'p']
        endpoint_orders.append({'alpha_is_p': alpha_p, 'beta_is_q': beta_q,
                                'terminal_order': terminal_order})

    caps = [
        cap_record(('t', 'p', 'q', 'h', 'w'),
                   {edge('t', 'q'), edge('p', 'w'), edge('q', 'w')},
                   [('t', 'p', 'a'), ('a', 'p', 'b'), ('b', 'p', 'q')],
                   'p', {edge('t', 'h'), edge('p', 'h')}),
        cap_record(('s', 'q', 'p', 'h', 'v'),
                   {edge('s', 'p'), edge('q', 'v'), edge('p', 'v')},
                   [('s', 'q', 'c'), ('c', 'q', 'b'), ('b', 'q', 'p')],
                   'q', {edge('s', 'h'), edge('q', 'h')}),
    ]
    components = [{'components': n, 'minimum_cut_size': 4 + 3 * (n - 1)}
                  for n in range(1, 5)]
    assert all(x['minimum_cut_size'] >= 7 for x in components[1:])
    return {'base': manifest['base'], 'authority': 'finite local calibration only',
            'frozen_inputs': checked, 'labelled_cycles': sorted(cycles),
            'pairings_mod_midpoint_renaming': sorted(canonical),
            'endpoint_order_cases': endpoint_orders, 'caps': caps,
            'cyclic_component_lower_bounds': components,
            'original_v5_assumption': False, 'support_reflection_used': False,
            'source_instances': 0, 'source_coverage': 'not triggered',
            'arbitrary_size_topology_authority': 'PROOF.md; not finite enumeration',
            'W110_plus_W101_positive': 'OPEN'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.loads(json.dumps(recompute()))
    if args.check:
        assert result == json.loads(args.check.read_text()), 'certificate differs'
        print(json.dumps({'status': 'PASS', 'pairings': 2, 'cap_links': 4,
                          'literal_endpoint_cases': 4, 'source_instances': 0,
                          'joint_positive': 'OPEN'}, sort_keys=True))
    elif args.output:
        with args.output.open('x') as stream:
            stream.write(json.dumps(result, indent=2, sort_keys=True) + '\n')
        print('created ' + str(args.output))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
