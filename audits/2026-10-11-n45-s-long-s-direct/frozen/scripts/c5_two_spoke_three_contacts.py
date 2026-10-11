#!/usr/bin/env python3
"""Local palette differences and K5 branch sets; no graph enumeration.

Arbitrary arm lengths and actual-source extraction are proved in the report.
"""
import argparse
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_two_spoke_three_contacts/observations.json'
U = frozenset(range(4))
Q = (0, 1, 0, 1, 2)


def local_table():
    subsets = [frozenset(s) for n in (1, 2, 3) for s in combinations(U, n)]
    pairs = [(a, b) for a in subsets for b in subsets
             if len(a) == len(b) and a & {0, 1} == b & {0, 1}
             and int(2 in a)-int(2 in b) == -(int(3 in a)-int(3 in b))]
    records = []
    for n in range(1, 5):
        for indices in combinations_with_replacement(range(len(pairs)), n):
            ps = [pairs[i] for i in indices]
            degree = sum(len(a) for a, _ in ps)
            if degree > 4:
                continue
            a = frozenset().union(*(x for x, _ in ps))
            b = frozenset().union(*(y for _, y in ps))
            if len(a) != degree or len(b) != degree:
                continue
            if a == b and 3 in a:
                kind = 'noncontact'
            elif a-b == {3} and b-a == {2} and degree <= 3:
                kind = 'contact'
            else:
                continue
            active = sum(x != y for x, y in ps)
            assert active in ((0, 2) if kind == 'noncontact' else (1,))
            records.append(dict(kind=kind, palettes=[[sorted(x), sorted(y)] for x, y in ps],
                                active_incidence=active))
    return records


def edge(u, v):
    return tuple(sorted((u, v)))


def minor(lengths, subdivide):
    es = {edge(f'b{i}', f'b{(i+1)%5}') for i in range(5)}
    es |= {edge('z', 'b0'), edge('z', 'b1')}
    es |= {edge(f'v{i}', f'v{j}') for i, j in combinations(range(3), 2)}
    groups = [{'z'}] + [{f'v{i}'} for i in range(3)] + [{f'b{i}' for i in range(5)}]
    ports, tethers = [], []
    for i, length in enumerate(lengths):
        arm = [f'v{i}'] + [f'a{i}_{j}' for j in range(1, length+1)]
        es.update(edge(a, b) for a, b in zip(arm, arm[1:]))
        es.add(edge('z', arm[-1]))
        ports.append(arm[-1])
        groups[i+1].update(arm)
        target = (1, 3, 4)[i]
        tether = [f'v{i}'] + ([f'w{i}_0', f'w{i}_1'] if subdivide[i] else []) + [f'b{target}']
        es.update(edge(a, b) for a, b in zip(tether, tether[1:]))
        groups[4].update(tether[1:-1])
        tethers.append(tether)
    assert len(set(ports)) == 3
    assert sum(map(len, groups)) == len(set().union(*groups))
    for group in groups:
        reached = {min(group)}
        while True:
            more = reached | {v for u in reached for v in group if edge(u, v) in es}
            if more == reached:
                break
            reached = more
        assert reached == group
    adjacency = []
    for i, j in combinations(range(5), 2):
        witness = next((edge(u, v) for u in sorted(groups[i]) for v in sorted(groups[j])
                        if edge(u, v) in es), None)
        assert witness is not None
        adjacency.append(dict(pair=[i, j], edge=witness))
    return dict(lengths=lengths, ports=ports, tethers=tethers, edges=sorted(es),
                branch_sets=[sorted(g) for g in groups], adjacency=adjacency)


def run():
    local = local_table()
    # These are subdivisions of the proved minor, not candidate degree-4 graphs.
    lengths = list(product((0, 2), repeat=3)) + [(1, 1, 1), (1, 3, 1)]
    minors = [minor(ls, bits) for ls in lengths for bits in product((False, True), repeat=3)]
    rows = [(0, 1, 0, 2, 1), (0, 1, 2, 0, 1), (0, 1, 2, 0, 2), (0, 1, 2, 1, 2)]
    attachments = []
    for p in rows:
        allowed = [t for n in range(3) for t in combinations(range(5), n)
                   if len({Q[i] for i in t}) == n and len({p[i] for i in t}) == n
                   and {Q[i] for i in t} <= {0, 1} and {p[i] for i in t} <= {0, 1}]
        attachments.append(dict(second_row=p, possible_contact_attachments=allowed))
    # Arm signs alternate; all contacts have the same sign. This is algebraic
    # control only; the induction for unbounded lengths is in the report.
    parity = []
    for ls in product(range(8), repeat=3):
        possible = [c for c in (2, 3)
                    if all((c if length % 2 == 0 else 5-c) == 3 for length in ls)]
        assert bool(possible) == (len({n % 2 for n in ls}) == 1)
        if possible:
            parity.append(dict(lengths=ls, central_color=possible[0]))
    return dict(scope='local algebra and explicit K5 subdivisions; no full graph enumeration',
                local_palettes=local, contact_attachments=attachments, minors=minors,
                parity_controls=parity,
                summary=dict(local_states=len(local), K5_certificates=len(minors),
                             parity_tests=8**3, second_rows=len(rows)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
