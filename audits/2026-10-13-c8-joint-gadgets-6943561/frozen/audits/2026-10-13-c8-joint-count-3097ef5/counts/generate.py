#!/usr/bin/env python3
"""Discover with scipy; reconstruct and check every answer over exact rationals."""
import argparse
from fractions import Fraction as Q
from functools import reduce
from math import gcd, lcm
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from checker import algebra, echelon, verify

HERE = Path(__file__).resolve().parent


def nullspace(rows, width):
    basis = echelon(rows)
    free = [j for j in range(width) if j not in basis]
    result = []
    for j in free:
        v = [Q(0)]*width
        v[j] = Q(1)
        for p, row in sorted(basis.items(), reverse=True):
            v[p] = -sum(row[k]*v[k] for k in range(p+1, width))
        result.append(v)
    return result


def reconstruct(approx, A, b):
    """Exact active face reconstruction, preserving free coordinates rationally."""
    basis = {}
    for row, rhs in zip(A, b):
        residual = sum(float(c)*v for c, v in zip(row, approx)) - float(rhs)
        if abs(residual) > 1e-7:
            continue
        v = list(map(Q, row)) + [Q(rhs)]
        for p, r in sorted(basis.items()):
            z = v[p]
            if z:
                v = [a-z*c for a, c in zip(v, r)]
        if any(v[:-1]):
            p = next(j for j, c in enumerate(v[:-1]) if c)
            z = v[p]
            basis[p] = [c/z for c in v]
        else:
            assert not v[-1]
    result = [Q(float(c)).limit_denominator(10**7) for c in approx]
    for p, row in sorted(basis.items(), reverse=True):
        result[p] = row[-1] - sum(row[k]*result[k] for k in range(p+1, len(result)))
    assert all(sum(c*v for c, v in zip(row, result)) >= rhs for row, rhs in zip(A, b))
    return result


def tracked_basis(rows, indices):
    basis = {}
    for i in indices:
        v, cs = list(map(Q, rows[i])), {i: Q(1)}
        for p, (r, expansion) in sorted(basis.items()):
            z = v[p]
            if z:
                v = [a-z*b for a, b in zip(v, r)]
                for k, c in expansion.items():
                    cs[k] = cs.get(k, Q(0)) - z*c
        if any(v):
            p = next(j for j, c in enumerate(v) if c)
            z = v[p]
            basis[p] = ([c/z for c in v], {k: c/z for k, c in cs.items() if c})
    return basis


def express(vector, basis):
    v, cs = list(map(Q, vector)), {}
    for p, (r, expansion) in sorted(basis.items()):
        z = v[p]
        if z:
            v = [a-z*b for a, b in zip(v, r)]
            for k, c in expansion.items():
                cs[k] = cs.get(k, Q(0)) + z*c
    assert not any(v)
    return {k: c for k, c in cs.items() if c}


def integral_identity(lhs, rhs, words):
    den = lcm(*(c.denominator for c in list(lhs.values())+list(rhs.values())))
    divisor = reduce(gcd, (int(c*den) for c in list(lhs.values())+list(rhs.values())))
    def terms(cs):
        return [{'index': i, 'word': words[i], 'coefficient': int(c*den)//divisor}
                for i, c in sorted(cs.items()) if c]
    return {'lhs': terms(lhs), 'rhs': terms(rhs)}


def build(interface):
    words, nc, active_indices, rows = algebra()
    assert interface['pattern_order'] == list(map(list, words))
    result = {'pattern_order': words, 'noncrossing_partitions': nc,
              'active_partition_indices': active_indices, 'equality_rows': rows,
              'full_rank': len(echelon(rows)), 'queries': [], 'summary': {}}
    width = len(active_indices)
    for case in interface['cases']:
        for target in case['targets']:
            upper = target['fixed_point']
            allowed = [i for i in range(274) if upper >> i & 1]
            rejected = [i for i in range(274) if not (upper >> i & 1)]
            accepted = [j for j in range(10) if target['target'] >> j & 1]
            preimages = {str(j): [i for i in allowed if case['transfer'][j][i]]
                         for j in accepted}
            query = {'case_id': case['id'], 'target': target['target'],
                     'upper_mask': upper, 'accepted_preimages': preimages}
            missing = [j for j in accepted if not preimages[str(j)]]
            if missing:
                query.update(status='excluded_transfer', missing_outer_index=missing[0])
            else:
                kernel = nullspace([rows[i] for i in rejected], width)
                V = [[sum(Q(a)*b for a, b in zip(row, v)) for v in kernel] for row in rows]
                C = [V[i] for i in allowed]
                outer_V = [[sum(Q(case['transfer'][j][i])*V[i][k] for i in allowed)
                            for k in range(len(kernel))] for j in accepted]
                C += outer_V
                b = [Q(0)]*len(allowed) + [Q(1)]*len(accepted)
                if kernel:
                    lp = linprog(np.zeros(len(kernel)), A_ub=-np.array(C, float),
                                 b_ub=-np.array(b, float), bounds=(None, None), method='highs')
                else:
                    lp = None
                if lp is not None and lp.success:
                    y = reconstruct(lp.x, C, b)
                    coefficients = [sum(v[j]*c for v, c in zip(kernel, y)) for j in range(width)]
                    x = [sum(c*a for c, a in zip(row, coefficients)) for row in rows]
                    outer = [sum(Q(c)*a for c, a in zip(row, x)) for row in case['transfer']]
                    query.update(status='necessary_condition_residual', counts=list(map(str, x)),
                                 partition_coefficients=list(map(str, coefficients)),
                                 outer_counts=list(map(str, outer)))
                else:
                    assert lp is None or lp.status == 2, lp.message
                    # Convexity: at least one required outer row is forced to zero.
                    # Normalize that row's coefficient to one in a Farkas witness.
                    found = None
                    for outer_index, o in zip(accepted, outer_V):
                        if not kernel:
                            lambdas = [Q(0)]*len(allowed)
                        else:
                            # Find nonnegative l such that sum l_i V_i = -o.
                            dual = linprog(np.ones(len(allowed)), A_eq=np.array([V[i] for i in allowed], float).T,
                                           b_eq=-np.array(o, float), bounds=(0, None), method='highs')
                            if not dual.success:
                                continue
                            A = [[Q(int(i == j)) for j in range(len(allowed))]
                                 for i in range(len(allowed))]
                            A += [[V[i][k] for i in allowed] for k in range(len(kernel))]
                            A += [[-V[i][k] for i in allowed] for k in range(len(kernel))]
                            bdual = [Q(0)]*len(allowed) + [-c for c in o] + list(o)
                            lambdas = reconstruct(dual.x, A, bdual)
                        lhs = {i: Q(case['transfer'][outer_index][i])+c
                               for i, c in zip(allowed, lambdas)
                               if case['transfer'][outer_index][i] or c}
                        target_row = [sum(c*rows[i][j] for i, c in lhs.items()) for j in range(width)]
                        rhs = express(target_row, tracked_basis(rows, rejected))
                        identity = integral_identity(lhs, rhs, words)
                        found = (outer_index, identity)
                        break
                    assert found is not None, 'No exact dual recovered'
                    query.update(status='excluded_count', forced_outer_index=found[0],
                                 forced_preimages=preimages[str(found[0])], identity=found[1])
            result['queries'].append(query)
            status = query['status']
            result['summary'][status] = result['summary'].get(status, 0)+1
            print(case['id'], target['target'], len(allowed), status, flush=True)
    result = json.loads(json.dumps(result))
    verify(result, interface)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', type=Path, default=HERE.parent/'interface.json')
    parser.add_argument('--output', type=Path, default=HERE/'certificate.json')
    args = parser.parse_args()
    result = build(json.loads(args.interface.read_text()))
    with args.output.open('x') as stream:
        stream.write(json.dumps(result, sort_keys=True, separators=(',', ':'))+'\n')
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
