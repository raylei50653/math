#!/usr/bin/env python3
"""Independent literal controls for the local degree-four fibre identity."""
import argparse
import itertools
import json
from pathlib import Path


def compute():
    cycle = ((0, 1), (1, 2), (2, 3), (3, 0))
    cases = []
    # Both diagonals together would make K5 after adding v: retain as an
    # algebraic empty-extension control, never as a planar cap witness.
    for diagonal_mask in range(4):
        diagonals = [edge for i, edge in enumerate(((0, 2), (1, 3)))
                     if diagonal_mask >> i & 1]
        rows = []
        for p in itertools.product(range(4), repeat=4):
            proper = all(p[u] != p[w] for u, w in cycle + tuple(diagonals))
            lifts = [a for a in range(4) if proper and all(a != x for x in p)]
            branches = [int(proper and p[0] == p[2]),
                        int(proper and p[1] == p[3])]
            assert len(lifts) == sum(branches)
            if proper:
                assert 4 - len(set(p)) == sum(branches)
            rows.append({'row': list(p), 'proper': proper,
                         'full_v_lifts': lifts, 'branch_counts': branches})
        cases.append({'diagonal_mask': diagonal_mask,
                      'diagonals': [list(e) for e in diagonals],
                      'planar_wheel_plus_diagonals': diagonal_mask != 3,
                      'proper_neighbor_rows': sum(r['proper'] for r in rows),
                      'empty_fibres': sum(not r['full_v_lifts'] for r in rows),
                      'full_lifts': sum(len(r['full_v_lifts']) for r in rows),
                      'rows': rows})
    return {'schema': 'degree4-local-literal-control-v1',
            'literal_colors': [0, 1, 2, 3],
            'scope': 'local fibre identity only; topology is paper proof',
            'row_cells': sum(len(c['rows']) for c in cases),
            'cases': cases}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = compute()
    target = Path(__file__).with_name('degree4_results.json')
    if args.check:
        assert json.loads(target.read_text()) == result
    else:
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'check': args.check,
                      'row_cells': result['row_cells'],
                      'case_totals': [{k: c[k] for k in
                                      ('diagonal_mask', 'proper_neighbor_rows',
                                       'empty_fibres', 'full_lifts')}
                                     for c in result['cases']]}))


if __name__ == '__main__':
    main()
