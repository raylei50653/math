#!/usr/bin/env python3
"""Solver-free exact verification of the C8 joint-count certificates."""
import argparse
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def partitions(n, word=()):
    if len(word) == n:
        yield word
    else:
        for c in range(max(word, default=-1) + 2):
            yield from partitions(n, word + (c,))


def is_noncrossing(p):
    return not any(p[a] == p[c] and p[b] == p[d] and p[a] != p[b]
                   for a, b, c, d in combinations(range(len(p)), 4))


def equality(p, partition):
    return int(all(partition[i] != partition[j] or p[i] == p[j]
                   for i, j in combinations(range(len(p)), 2)))


def algebra():
    words = tuple(p for p in partitions(8) if max(p) < 4
                  and all(p[i] != p[(i+1) % 8] for i in range(8)))
    nc = tuple(p for p in partitions(8) if is_noncrossing(p))
    active_indices = [j for j, q in enumerate(nc)
                      if any(equality(p, q) for p in words)]
    active = [nc[j] for j in active_indices]
    rows = [[equality(p, q) for q in active] for p in words]
    assert len(words) == 274 and len(nc) == 1430
    return words, nc, active_indices, rows


def echelon(rows):
    basis = {}
    for row in rows:
        v = list(map(Q, row))
        for pivot, r in sorted(basis.items()):
            z = v[pivot]
            if z:
                v = [a-z*b for a, b in zip(v, r)]
        if any(v):
            p = next(j for j, c in enumerate(v) if c)
            z = v[p]
            basis[p] = [c/z for c in v]
    return basis


def term_map(terms, words):
    result = {}
    for t in terms:
        i, c = t['index'], Q(t['coefficient'])
        assert 0 <= i < len(words) and c and i not in result
        assert t['word'] == list(words[i]), 'mixed pattern labels'
        result[i] = c
    return result


def check_identity(identity, words, nc):
    lhs, rhs = term_map(identity['lhs'], words), term_map(identity['rhs'], words)
    for p in nc:
        assert sum(c*equality(words[i], p) for i, c in lhs.items()) == \
            sum(c*equality(words[i], p) for i, c in rhs.items()), \
            'identity fails on a noncrossing equality vector'
    return lhs, rhs


def load_interface(path):
    interface = json.loads(Path(path).read_text())
    return interface


def verify(certificate, interface):
    words, nc, active_indices, rows = algebra()
    assert certificate['pattern_order'] == list(map(list, words))
    assert interface['pattern_order'] == list(map(list, words))
    assert certificate['noncrossing_partitions'] == list(map(list, nc))
    assert certificate['active_partition_indices'] == active_indices
    assert certificate['equality_rows'] == rows
    assert certificate['full_rank'] == len(echelon(rows))
    cases = {(c['id'], t['target']): (c, t) for c in interface['cases']
             for t in c['targets']}
    queries = certificate['queries']
    assert len(cases) == len(queries) == 70
    assert {(q['case_id'], q['target']) for q in queries} == set(cases)
    totals = {}
    for query in queries:
        case, target = cases[query['case_id'], query['target']]
        if certificate.get('joint_refinement') and query['status'] == 'necessary_condition_residual':
            assert all(key in query for key in ('refinement_stages', 'final_upper_mask',
                       'final_accepted_preimages', 'residual_support_mask')), 'incomplete joint residual'
        upper = target['fixed_point']
        allowed = [i for i in range(274) if upper >> i & 1]
        rejected = [i for i in range(274) if not (upper >> i & 1)]
        assert query['upper_mask'] == upper
        accepted = [j for j in range(10) if query['target'] >> j & 1]
        preimages = {str(j): [i for i in allowed if case['transfer'][j][i]]
                     for j in accepted}
        assert query['accepted_preimages'] == preimages, 'incomplete necessary preimages'
        assert target['accepted_preimages'] == preimages
        if 'refinement_stages' in query:
            for stage in query['refinement_stages']:
                assert stage['upper_before'] == upper
                forced = set()
                for identity in stage['forced_zero_identities']:
                    lhs, rhs = check_identity(identity, words, nc)
                    assert lhs and all(upper >> i & 1 and c > 0 for i, c in lhs.items())
                    assert all(not (upper >> i & 1) for i in rhs)
                    forced.update(lhs)
                upper &= ~sum(1 << i for i in forced)
                assert stage['count_support'] == upper
                for round_ in stage['kempe_rounds']:
                    assert round_['before'] == upper
                    removals = []
                    for i in range(274):
                        if upper >> i & 1:
                            bad = [j for j, opts in enumerate(interface['kempe_obligations'][i])
                                   if not any(o & ~upper == 0 for o in opts)]
                            if bad:
                                removals.append({'pattern_index': i, 'split_indices': bad})
                    assert removals and round_['removals'] == removals
                    upper &= ~sum(1 << r['pattern_index'] for r in removals)
                assert stage['upper_after'] == upper
            assert query['final_upper_mask'] == upper
            allowed = [i for i in range(274) if upper >> i & 1]
            rejected = [i for i in range(274) if not (upper >> i & 1)]
            preimages = {str(j): [i for i in allowed if case['transfer'][j][i]] for j in accepted}
            assert query['final_accepted_preimages'] == preimages
        status = query['status']
        totals[status] = totals.get(status, 0) + 1
        if status == 'excluded_transfer':
            assert query['missing_outer_index'] in accepted
            assert not preimages[str(query['missing_outer_index'])]
        elif status == 'excluded_count':
            lhs, rhs = check_identity(query['identity'], words, nc)
            assert all(i in allowed and c > 0 for i, c in lhs.items())
            assert all(i in rejected for i in rhs)
            forced = query['forced_outer_index']
            assert forced in accepted and preimages[str(forced)]
            assert set(preimages[str(forced)]) <= set(lhs), 'missing necessary preimage'
            assert query['forced_preimages'] == preimages[str(forced)]
        elif status == 'necessary_condition_residual':
            x = list(map(Q, query['counts']))
            coefficients = list(map(Q, query['partition_coefficients']))
            assert len(x) == 274 and len(coefficients) == len(active_indices)
            assert all(v >= 0 for v in x)
            assert all(x[i] == 0 for i in rejected)
            assert all(x[i] == sum(Q(c)*a for c, a in zip(rows[i], coefficients))
                       for i in range(274)), 'vector outside common count span'
            y = [sum(Q(c)*a for c, a in zip(row, x)) for row in case['transfer']]
            assert list(map(str, y)) == query['outer_counts']
            assert all(v > 0 if j in accepted else v == 0 for j, v in enumerate(y))
            if 'residual_support_mask' in query:
                support = sum(1 << i for i, value in enumerate(x) if value)
                assert query['residual_support_mask'] == support == upper
                assert all(any(o & ~support == 0 for o in opts)
                           for i in allowed for opts in interface['kempe_obligations'][i]), \
                    'residual support fails Kempe closure'
        else:
            raise AssertionError('unknown status')
    assert certificate['summary'] == totals
    return totals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=HERE/'certificate.v2.json')
    parser.add_argument('--interface', type=Path, default=HERE.parent/'interface.json')
    parser.add_argument('--check', action='store_true', help='accepted explicit verification flag')
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    summary = verify(certificate, load_interface(args.interface))
    print(json.dumps({'status': 'PASS', 'queries': 70, 'summary': summary,
                      'NC_partitions': 1430, 'arithmetic': 'int/Fraction only'}, sort_keys=True))


if __name__ == '__main__':
    main()
