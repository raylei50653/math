#!/usr/bin/env python3
"""Finite local audit for the paper bridge-path lemma; no graph-size cover."""
import argparse
import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_single_spoke_bridge_path/observations.json'
U = set(range(4))
Q = (0, 1, 0, 1, 2)
P = (0, 1, 0, 2, 1)


def audit():
    rows = []
    for contact in (False, True):
        for size in range(5):
            for support in combinations(range(1, 5), size):
                degree = 4 - size - int(contact)
                if degree < 1:
                    continue
                lists = []
                for row, z in ((Q, 3), (P, 2), (P, 3)):
                    external = [row[i] for i in support] + ([z] if contact else [])
                    if len(set(external)) != len(external):
                        break
                    lists.append(sorted(U - set(external)))
                else:
                    assert all(len(ls) == degree for ls in lists)
                    rows.append(dict(contact=contact, support=list(support),
                                     degree=degree, lists=lists))
    assert len(rows) == 16
    # On-path residual lists must survive removing identical off-path palettes.
    path_rows = []
    for r in rows:
        wanted = ({3}, {2}) if r['contact'] else ({2, 3}, {2, 3})
        m2, m3 = map(set, r['lists'][1:])
        if wanted[0] <= m2 and wanted[1] <= m3 and m2-wanted[0] == m3-wanted[1]:
            assert 3 not in r['support']
            path_rows.append(r)
    # Ordered bridge colors in the two bad assignments.  An internal vertex
    # has the same residual list, so an unequal incoming pair must reverse.
    transitions = []
    for a in U:
        for b in U - {a}:
            for c in U - {a}:
                for d in U - {b}:
                    if {a, c} == {b, d}:
                        assert (c, d) == (b, a)
                        transitions.append([a, b, c, d])
    assert len(transitions) == 12
    pair = (3, 2)
    parity = []
    for length in range(1, 9):
        end = pair if length % 2 else pair[::-1]
        assert (end == pair) == (length % 2 == 1)
        parity.append(dict(length=length, endpoint_pair=list(end),
                           compatible=end == pair))
    return dict(scope='local necessary conditions only; arbitrary-size proof in report',
                assignments=['q,z=3', 'p1,z=2', 'p1,z=3'],
                tight_rows=rows, path_rows=path_rows,
                bridge_transitions=transitions, parity_controls=parity)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = audit()
    if args.check:
        assert json.loads(OUT.read_text()) == result
        print('single-spoke bridge path: 16 tight rows, 12 transitions verified')
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
