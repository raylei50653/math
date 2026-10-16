#!/usr/bin/env python3
"""Direct pin/r-fibre arithmetic, independent of every worker checker.

Jordan separation and existence of full source colourings are paper premises.
The 4^7 local rows below are not counts of actual source colourings.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLOURS = set(range(4))
EDGES = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
         (0, 5), (5, 6), (6, 0))


def canonical(row):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in row)


def local(row):
    z, s, v, w, t, p, q = row
    proper = all(row[u] != row[vv] for u, vv in EDGES)
    lifts = sorted(COLOURS - {s, v, w, t}) if proper else []
    checks = []
    for r in lifts:
        # Direct original four-cycle rule; no use of the worker transfer table.
        if z == r and s == t:
            ok = {p, q} == COLOURS - {z, s}
        elif z == r:
            ok = False
        elif s == t:
            missing = COLOURS - {z, s, r}
            ok = len(missing) == 1 and bool(missing <= {p, q})
        else:
            ok = {p, q} == {s, t}
        checks.append(ok)
    return proper, lifts, checks


def calculate():
    digest = hashlib.sha256()
    proper_count = admissible_count = empty_r_count = 0
    for row in itertools.product(range(4), repeat=7):
        proper, lifts, checks = local(row)
        digest.update(json.dumps([list(row), proper, lifts, checks],
                                 separators=(',', ':')).encode())
        digest.update(b'\n')
        proper_count += proper
        admissible_count += proper and all(checks)
        empty_r_count += proper and not lifts
    cases = []
    for a, b, c in itertools.permutations(range(4), 3):
        d, = COLOURS - {a, b, c}
        for p, q in [(b, c), (c, b)]:
            for reflect in [False, True]:
                x = (a, b, a, b, c, p, q)
                if reflect:
                    x = (a, c, b, a, b, q, p)
                    # One common B/C renaming gives the literal reflected X.
                    x = tuple(c if v == b else b if v == c else v for v in x)
                assert local(x)[0] and all(local(x)[2])
                i = 4 if reflect else 1
                for swap_pq in [False, True]:
                    # Jordan separates the switched endpoint from the other
                    # two BC boundary vertices; edge pq keeps its endpoints together.
                    switched = {i} | ({5, 6} if swap_pq else set())
                    y = tuple((c if v == b else b if v == c else v)
                              if j in switched else v for j, v in enumerate(x))
                    assert local(y)[0] and all(local(y)[2])
                    z, s, v, w, t, pp, qq = y
                    assert s == t and len({v ^ w, pp ^ qq, s ^ z}) == 3
                    assert local(y)[1] == [d]
                    # Reverse-link obstruction keeps pq fixed while moving
                    # only the v (or reflected w) pin from A to D.
                    bad = list(y)
                    bad[3 if reflect else 2] = d
                    assert local(tuple(bad))[0]
                    assert local(tuple(bad))[1] == [a]
                    assert not all(local(tuple(bad))[2])
                    forward_bad = list(x)
                    forward_bad[3 if reflect else 2] = d
                    assert canonical(forward_bad[:5]) not in {
                        (0, 1, 0, 1, 2), (0, 1, 0, 2, 1),
                        (0, 1, 0, 2, 3), (0, 1, 2, 0, 1),
                        (0, 1, 2, 0, 2), (0, 1, 2, 0, 3),
                        (0, 1, 2, 3, 1)}
                    cases.append([list(x), sorted(switched), list(y), bad])
    return {'rows': 4 ** 7, 'proper_rows': proper_count,
            'all_r_admissible_rows': admissible_count,
            'proper_empty_r_fibres': empty_r_count,
            'dense_direct_row_sha256': digest.hexdigest(),
            'bijection_local_cases': len(cases), 'cases': cases,
            'actual_minimum_sources': 0, 'source_coverage': 'not triggered',
            'paper_premises': ['complete support 319',
                               'full original all-r condition',
                               'Jordan separation of alternating outer endpoints',
                               'maximal full Kempe components']}


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = calculate()
    if args.write:
        with args.write.open('x') as out:
            json.dump(result, out, indent=2)
            out.write('\n')
    else:
        assert json.loads(args.check.read_text()) == result, 'certificate mismatch'
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, sort_keys=True))


if __name__ == '__main__':
    main()
