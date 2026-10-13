#!/usr/bin/env python3
"""Finite literal-frame arithmetic used by TOPOLOGY.md, not source enumeration."""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROWS = {0: (0, 1, 2, 1, 2), 1: (0, 1, 2, 0, 2), 3: (0, 1, 0, 2, 1)}
EDGES = {frozenset((v, (v + 1) % 5)) for v in range(5)}


def closure(t):
    return tuple(h for h in range(5)
                 if all(q[h] in {q[v] for v in t} for q in ROWS.values()))


def direct_matrices(m, n, kr, ks):
    result = []
    for bits in itertools.product((0, 1), repeat=m * n):
        if not all(ks - 1 <= sum(bits[x*n:(x+1)*n]) <= ks for x in range(m)):
            continue
        if not all(kr - 1 <= sum(bits[x*n+y] for x in range(m)) <= kr for y in range(n)):
            continue
        result.append(bits)
    return result


def generate():
    signatures = [tuple(q[h] for q in ROWS.values()) for h in range(5)]
    assert len(set(signatures)) == 5
    arcs = [tuple((v + j) % 5 for j in range(3)) for v in range(5)]
    geometry = []
    for p, q in itertools.product(arcs, repeat=2):
        pe = {frozenset(p[j:j+2]) for j in range(2)}
        qe = {frozenset(q[j:j+2]) for j in range(2)}
        if pe & qe:
            continue
        unused, = EDGES - pe - qe
        z = closure(unused)
        pz, qz = tuple(sorted(set(p) & set(z))), tuple(sorted(set(q) & set(z)))
        assert not any(edge <= set(pz) for edge in EDGES)
        assert not any(edge <= set(qz) for edge in EDGES)
        geometry.append(dict(P=list(p), Q=list(q), unused_spoke_edge=sorted(unused),
                             Z=list(z), P_contact_sites=list(pz), Q_contact_sites=list(qz)))
    assert len(geometry) == 10

    three_color = []
    for arc in arcs:
        witness = [i for i, q in ROWS.items() if len({q[v] for v in arc}) == 3]
        assert witness
        three_color.append(dict(support=list(arc), rows=witness,
                                colors={str(i): [ROWS[i][v] for v in arc] for i in witness}))

    cuts = []
    for tr, ts, ps in [(1, 1, 3), (2, 1, 3), (2, 0, 4)]:
        m, n, pr = 4-tr, 4-ts, 1
        lower, upper = m*(ps-1), n*pr
        assert lower > upper
        feasible = direct_matrices(m, n, pr, ps)
        assert feasible == []
        cuts.append(dict(spokes=[tr, ts], P_incidences=[pr, ps],
                         grid=[m, n], row_total_lower=lower, column_total_upper=upper,
                         independently_enumerated_feasible_matrices=0))

    incidence_cases = []
    for pr, ps in itertools.product(range(1, 4), repeat=2):
        qr, qs = 4-pr, 4-ps
        high_p, high_q = min(pr, ps) >= 2, min(qr, qs) >= 2
        if not (high_p or high_q):
            assert { (pr, ps), (qr, qs) } == { (1, 3), (3, 1) }
            status = 'basic-total-capacity-cut'
        elif high_p and high_q:
            status = 'both-HH11'
        else:
            low = (qr+qs) if high_p else (pr+ps)
            assert low <= 3
            status = 'HH11-plus-low-incidence-escape'
        incidence_cases.append(dict(P=[pr, ps], Q=[qr, qs], status=status))

    forced_rows = []
    for row in itertools.product((0, 1), repeat=4):
        if all(row[y] == 0 for y in (0, 1, 2)) and 2 <= sum(row) <= 3:
            forced_rows.append(row)
    assert forced_rows == []
    return dict(scope='literal-frame and capacity arithmetic only',
                complete_source_status='not triggered',
                rows={str(i): list(q) for i, q in ROWS.items()},
                signatures=[list(s) for s in signatures],
                two_long_geometries=geometry, three_color_support_witnesses=three_color,
                capacity_cuts=cuts, t11_incidence_cases=incidence_cases,
                final_leaf_bridge_row_cut=dict(forced_zeros=3, columns=4,
                    required_row_lower=2, remaining_upper=1, independent_feasible_rows=0))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--artifact', type=Path, default=HERE/'topology_arithmetic.json')
    args = parser.parse_args()
    data = generate()
    encoded = json.dumps(data, indent=2, sort_keys=True)+'\n'
    if args.check:
        assert args.artifact.read_text() == encoded, 'topology arithmetic artifact mismatch'
    else:
        with args.artifact.open('x') as output:
            output.write(encoded)
    print(json.dumps(dict(status='PASS', source_status='not triggered',
                         geometries=len(data['two_long_geometries']),
                         literal_arcs=len(data['three_color_support_witnesses']),
                         total_capacity_cuts=len(data['capacity_cuts']),
                         t11_incidence_cases=len(data['t11_incidence_cases'])), sort_keys=True))


if __name__ == '__main__':
    main()
