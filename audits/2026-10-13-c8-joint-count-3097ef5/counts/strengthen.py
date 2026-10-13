#!/usr/bin/env python3
"""Alternate exact nonnegative count-cone support with sound Kempe pruning."""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from checker import algebra, verify
from generate import nullspace, reconstruct, tracked_basis, express, integral_identity

HERE = Path(__file__).resolve().parent


def context(case, target, upper, rows):
    allowed = [i for i in range(274) if upper >> i & 1]
    rejected = [i for i in range(274) if not (upper >> i & 1)]
    accepted = [j for j in range(10) if target >> j & 1]
    width = len(rows[0])
    kernel = nullspace([rows[i] for i in rejected], width)
    V = [[sum(Q(a)*b for a, b in zip(row, v)) for v in kernel] for row in rows]
    C = [V[i] for i in allowed]
    outer = [[sum(Q(case['transfer'][j][i])*V[i][k] for i in allowed)
              for k in range(len(kernel))] for j in accepted]
    C += outer
    b = [Q(0)]*len(allowed) + [Q(1)]*len(accepted)
    return allowed, rejected, accepted, kernel, V, C, b, outer


def feasible(C, b, dimension):
    if not dimension:
        return [] if not any(c > 0 for c in b) else None
    lp = linprog(np.zeros(dimension), A_ub=-np.array(C, float), b_ub=-np.array(b, float),
                 bounds=(None, None), method='highs')
    if lp.success:
        return reconstruct(lp.x, C, b)
    assert lp.status == 2, lp.message
    return None


def count_vector(kernel, rows, y):
    cs = [sum(v[j]*c for v, c in zip(kernel, y)) for j in range(len(rows[0]))]
    x = [sum(c*a for c, a in zip(row, cs)) for row in rows]
    return cs, x


def dual_identity(o, literal_lhs, V, allowed, rejected, rows, words):
    dim = len(o)
    if dim:
        dual = linprog(np.ones(len(allowed)), A_eq=np.array([V[i] for i in allowed], float).T,
                       b_eq=-np.array(o, float), bounds=(0, None), method='highs')
        if not dual.success:
            return None
        A = [[Q(int(i == j)) for j in range(len(allowed))] for i in range(len(allowed))]
        A += [[V[i][k] for i in allowed] for k in range(dim)]
        A += [[-V[i][k] for i in allowed] for k in range(dim)]
        lambdas = reconstruct(dual.x, A, [Q(0)]*len(allowed)+[-c for c in o]+list(o))
    else:
        lambdas = [Q(0)]*len(allowed)
    lhs = {i: Q(literal_lhs.get(i, 0))+c for i, c in zip(allowed, lambdas)
           if literal_lhs.get(i, 0) or c}
    target_row = [sum(c*rows[i][j] for i, c in lhs.items()) for j in range(len(rows[0]))]
    rhs = express(target_row, tracked_basis(rows, rejected))
    return integral_identity(lhs, rhs, words)


def prune(upper, table):
    rounds = []
    while True:
        removals = []
        for i in range(274):
            if upper >> i & 1:
                bad = [j for j, opts in enumerate(table[i]) if not any(o & ~upper == 0 for o in opts)]
                if bad:
                    removals.append({'pattern_index': i, 'split_indices': bad})
        if not removals:
            return upper, rounds
        rounds.append({'before': upper, 'removals': removals})
        upper &= ~sum(1 << r['pattern_index'] for r in removals)


def build(initial, interface):
    words, nc, active_indices, rows = algebra()
    result = json.loads(json.dumps(initial))
    result['joint_refinement'] = 'Maximal feasible count support alternated with complete Kempe pruning.'
    cases = {c['id']: c for c in interface['cases']}
    for query in result['queries']:
        if query['status'] != 'necessary_condition_residual':
            continue
        case, target = cases[query['case_id']], query['target']
        upper = query['upper_mask']
        stages = []
        for step in range(275):
            allowed, rejected, accepted, kernel, V, C, b, outer = context(case, target, upper, rows)
            preimages = {str(j): [i for i in allowed if case['transfer'][j][i]] for j in accepted}
            missing = [j for j in accepted if not preimages[str(j)]]
            if missing:
                query.update(status='excluded_transfer', missing_outer_index=missing[0])
                break
            y = feasible(C, b, len(kernel))
            if y is None:
                for j, o in zip(accepted, outer):
                    identity = dual_identity(o, {i: case['transfer'][j][i] for i in allowed},
                                             V, allowed, rejected, rows, words)
                    if identity is not None:
                        query.update(status='excluded_count', forced_outer_index=j,
                                     forced_preimages=preimages[str(j)], identity=identity)
                        break
                else:
                    raise AssertionError('No exact outer dual')
                break
            forced = set()
            identities = []
            while True:
                cs, x = count_vector(kernel, rows, y)
                missing_coordinates = [i for i in allowed if not x[i] and i not in forced]
                if not missing_coordinates:
                    break
                i = missing_coordinates[0]
                yi = feasible(C+[V[i]], b+[Q(1)], len(kernel))
                if yi is not None:
                    y = [a+c for a, c in zip(y, yi)]
                else:
                    identity = dual_identity(V[i], {i: 1}, V, allowed, rejected, rows, words)
                    assert identity is not None
                    identities.append(identity)
                    forced.update(t['index'] for t in identity['lhs'])
            count_support = sum(1 << i for i, value in enumerate(x) if value)
            assert count_support == upper & ~sum(1 << i for i in forced)
            after, rounds = prune(count_support, interface['kempe_obligations'])
            stages.append({'upper_before': upper, 'forced_zero_identities': identities,
                           'count_support': count_support, 'kempe_rounds': rounds, 'upper_after': after})
            print(query['case_id'], target, 'stage', step, 'upper', upper.bit_count(),
                  'count_support', count_support.bit_count(), 'Kempe_after', after.bit_count(), flush=True)
            if after == count_support:
                upper = after
                final_preimages = {str(j): [i for i in range(274) if upper >> i & 1
                                           and case['transfer'][j][i]] for j in accepted}
                outer_counts = [sum(Q(c)*a for c, a in zip(row, x)) for row in case['transfer']]
                query.update(status='necessary_condition_residual', counts=list(map(str, x)),
                             partition_coefficients=list(map(str, cs)), outer_counts=list(map(str, outer_counts)),
                             residual_support_mask=count_support)
                preimages = final_preimages
                break
            upper = after
        else:
            raise AssertionError('Nonterminating refinement')
        query.update(refinement_stages=stages, final_upper_mask=upper,
                     final_accepted_preimages=preimages)
        if query['status'] != 'necessary_condition_residual':
            for key in ('counts', 'partition_coefficients', 'outer_counts'):
                query.pop(key, None)
        print(query['case_id'], target, 'FINAL', query['status'], flush=True)
    totals = {}
    for q in result['queries']:
        totals[q['status']] = totals.get(q['status'], 0)+1
    result['summary'] = totals
    result = json.loads(json.dumps(result))
    verify(result, interface)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', type=Path, default=HERE.parent/'interface.json')
    parser.add_argument('--initial', type=Path, default=HERE/'certificate.json')
    parser.add_argument('--output', type=Path, default=HERE/'certificate.v2.json')
    args = parser.parse_args()
    result = build(json.loads(args.initial.read_text()), json.loads(args.interface.read_text()))
    with args.output.open('x') as stream:
        stream.write(json.dumps(result, sort_keys=True, separators=(',', ':'))+'\n')
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
