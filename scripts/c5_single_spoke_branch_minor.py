#!/usr/bin/env python3
"""Replay local tether coverage and extracted K5 controls, not source graphs."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_single_spoke_branch_palettes import audit as palette_audit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_single_spoke_branch_minor/observations.json'
SOURCE = ROOT / 'artifacts/c5_single_spoke_completion/observations.json'


def tether_audit():
    data = palette_audit()
    results = []
    for row in data['path_rows']:
        residual = row['q_residual']
        a, = [c for c in (1, 2) if residual & (1 << c)]
        h = 4 if a == 1 else 1
        required = {2, h}
        supplied = set(row['support'])
        assert 3 not in supplied
        for q, p in row['children']:
            entry, = [r for r in data['root_supports']
                      if (r['q_palette'], r['p_palette']) == (q, p)]
            # Only use support shared by every surviving necessary support.
            supplied |= set.intersection(*(set(s) for s in entry['allowed_supports']))
        assert required <= supplied
        results.append(dict(**row, odd_edge_color=a, required_boundary=sorted(required)))
    assert len(results) == 20
    return results


def connected(vs, edges):
    if not vs:
        return False
    seen = {next(iter(vs))}
    while True:
        more = {y for x, y in edges if x in seen and y in vs}
        more |= {x for x, y in edges if y in seen and x in vs}
        if more <= seen:
            return seen == vs
        seen |= more


def verify_minor(edges, bags):
    used = set()
    for bag in bags:
        assert not used & bag and connected(bag, edges)
        used |= bag
    witnesses = []
    for i, j in combinations(range(5), 2):
        candidates = [(u, v) for u, v in sorted(edges)
                      if (u in bags[i] and v in bags[j]) or
                         (v in bags[i] and u in bags[j])]
        assert candidates, (i, j)
        witnesses.append(dict(bags=[i, j], edge=list(candidates[0])))
    return witnesses


def control(length, edge_index, a, styles, route_length):
    """A schematic extracted subgraph. No degree/list realizability assertion."""
    assert length % 2 == edge_index % 2 == 1
    edges = set()

    def edge(u, v):
        assert u != v
        edges.add(tuple(sorted((u, v))))

    for i in range(5):
        edge(f'b{i}', f'b{(i+1)%5}')
    path = [f'x{i}' for i in range(length + 1)]
    for u, v in zip(path, path[1:]):
        edge(u, v)
    edge('z', path[0])
    edge('z', path[-1])
    edge('z', 'b0')
    exterior = {'z'}
    routes = []
    for b in (1, 4):
        interior = [f'c{b}_{i}' for i in range(route_length)]
        route = ['z'] + interior + [f'b{b}']
        for u, v in zip(route, route[1:]):
            edge(u, v)
        exterior.update(interior)
        routes.append(route)
    h = 4 if a == 1 else 1
    endpoints = path[edge_index-1:edge_index+1]
    endpoint_bags = []
    for root, style in zip(endpoints, styles):
        bag = {root}
        if style == 'direct':
            edge(root, 'b2')
            edge(root, f'b{h}')
        else:
            y, w = root + '_y', root + '_w'
            bag.update((y, w))
            edge(root, y)
            edge(root, w)
            if style == 'shared_cycle':
                edge(y, w)
            edge(y, 'b2')
            edge(w, f'b{h}')
        endpoint_bags.append(bag)
    exterior.update(set(path) - set(endpoints))
    if a == 1:
        exterior.add('b1')
        hubs = [{'b2'}, {'b3', 'b4'}]
    else:
        exterior.update(('b3', 'b4'))
        hubs = [{'b2'}, {'b1'}]
    bags = endpoint_bags + [exterior] + hubs
    witnesses = verify_minor(edges, bags)
    return dict(length=length, odd_edge=edge_index, q_color=a, styles=styles,
                exterior_routes=routes, edges=sorted(edges),
                branch_sets=[sorted(b) for b in bags], adjacencies=witnesses)


def refine_table():
    source = json.loads(SOURCE.read_text())
    results, counts, changed = [], Counter(), []
    for row in source['records']:
        flags = [t['status'] == 'accept' for t in row['targets']]
        roles = {tuple(b): tuple(s) for b, s in zip(row['bans'], row['supports'])}
        applies = (row['spoke'] == 0 and row['bans'][0] == [3] and
                   roles == {(1,): (0, 1), (2,): (0, 4), (3,): (1, 2, 3, 4)})
        if applies:
            assert flags == [False, True]
            changed.append(row['source_index'])
            flags[0] = True
        counts[{(True, True): 'both', (True, False): 'p1_only',
                (False, True): 'p2_only', (False, False): 'neither'}[tuple(flags)]] += 1
        results.append(dict(source_index=row['source_index'], spoke=row['spoke'],
                            bans=row['bans'], supports=row['supports'],
                            placements=row['placements'],
                            accepted_targets=flags, branch_minor_applies=applies))
    assert changed == [24, 29]
    assert counts == {'both': 64, 'p1_only': 20, 'p2_only': 30}
    return dict(counts=dict(counts), newly_accepted_p1=changed, records=results)


def build():
    controls = [control(length, i, a, styles, route_length)
                for length in (1, 3, 5, 7) for i in range(1, length+1, 2)
                for a in (1, 2)
                for styles in product(('direct', 'separate_bridges', 'shared_cycle'), repeat=2)
                for route_length in (1, 3)]
    assert len(controls) == 360
    paths = [SOURCE, Path(__file__), ROOT / 'scripts/c5_single_spoke_branch_palettes.py',
             ROOT / 'scripts/c5_single_spoke_bridge_path.py']
    return dict(scope='local support audit and extracted K5 controls; arbitrary-size proof in report',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in paths},
                tether_rows=tether_audit(), minor_controls=controls, table=refine_table())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(dict(local_cases=len(result['tether_rows']),
                          minors=len(result['minor_controls']),
                          counts=result['table']['counts']), sort_keys=True))


if __name__ == '__main__':
    main()
