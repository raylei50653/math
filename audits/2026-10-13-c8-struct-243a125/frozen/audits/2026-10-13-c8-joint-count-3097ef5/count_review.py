#!/usr/bin/env python3
"""Independent exact review: no imports from count/transfer producers or checkers."""
import argparse
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def canonical(word):
    keys = []
    for color in word:
        if color not in keys:
            keys.append(color)
    return tuple(keys.index(color) for color in word)


def block_partitions(n):
    if n == 0:
        yield ()
        return
    for blocks in block_partitions(n-1):
        yield blocks+((n-1,),)
        for j in range(len(blocks)):
            yield blocks[:j]+(blocks[j]+(n-1,),)+blocks[j+1:]


def build():
    interface = json.loads((HERE/'interface.json').read_text())
    certificate = json.loads((HERE/'counts/certificate.v2.json').read_text())
    words = sorted({canonical(w) for w in product(range(4), repeat=8)
                    if all(w[i] != w[(i+1) % 8] for i in range(8))})
    parts = []
    for blocks in block_partitions(8):
        owner = {v: j for j, block in enumerate(blocks) for v in block}
        if any(owner[a] == owner[c] and owner[b] == owner[d] and owner[a] != owner[b]
               for a, b, c, d in combinations(range(8), 4)):
            continue
        parts.append(tuple(owner[i] for i in range(8)))
    parts.sort()
    assert len(parts) == 1430 and len(words) == 274
    assert certificate['pattern_order'] == list(map(list, words))
    assert certificate['noncrossing_partitions'] == list(map(list, parts))
    pairs = list(combinations(range(8), 2))
    equality_masks = [sum(1 << j for j, (a, b) in enumerate(pairs) if w[a] == w[b])
                      for w in words]
    part_masks = [sum(1 << j for j, (a, b) in enumerate(pairs) if p[a] == p[b])
                  for p in parts]
    equalities = [[j for j, p in enumerate(part_masks) if p & ~e == 0]
                  for e in equality_masks]
    active = [j for j in range(1430) if any(j in row for row in equalities)]
    assert active == certificate['active_partition_indices'] and len(active) == 91
    assert certificate['equality_rows'] == [[int(j in row) for j in active]
                                           for row in equalities]
    identity_count = 0

    def identity(ident, upper):
        nonlocal identity_count
        residual = [Q(0)]*1430
        forced = set()
        for side, sign in [('lhs', 1), ('rhs', -1)]:
            seen = set()
            for term in ident[side]:
                i, coefficient = term['index'], Q(term['coefficient'])
                assert 0 <= i < 274 and coefficient and i not in seen
                assert term['word'] == list(words[i])
                seen.add(i)
                if side == 'lhs':
                    assert upper >> i & 1 and coefficient > 0
                    forced.add(i)
                else:
                    assert not (upper >> i & 1)
                for j in equalities[i]:
                    residual[j] += sign*coefficient
        assert all(value == 0 for value in residual)
        identity_count += 1
        return forced

    expected_keys = {(case['id'], target['target']) for case in interface['cases']
                     for target in case['targets']}
    assert len(expected_keys) == len(certificate['queries']) == 70
    assert {(q['case_id'], q['target']) for q in certificate['queries']} == expected_keys
    reports = []
    for query in certificate['queries']:
        case = next(c for c in interface['cases'] if c['id'] == query['case_id'])
        target = next(t for t in case['targets'] if t['target'] == query['target'])
        upper = target['fixed_point']
        assert upper == query['upper_mask']
        accepted = [j for j in range(10) if query['target'] >> j & 1]

        def preimages(mask):
            return {str(j): [i for i in range(274) if mask >> i & 1
                             and case['transfer'][j][i]] for j in accepted}

        assert query['accepted_preimages'] == preimages(upper)
        for stage in query.get('refinement_stages', []):
            assert stage['upper_before'] == upper
            forced = set()
            for ident in stage['forced_zero_identities']:
                forced |= identity(ident, upper)
            upper &= ~sum(1 << i for i in forced)
            assert stage['count_support'] == upper
            for round_ in stage['kempe_rounds']:
                assert round_['before'] == upper
                expected = []
                for i in range(274):
                    if upper >> i & 1:
                        bad = [j for j, options in enumerate(interface['kempe_obligations'][i])
                               if all(orbit & ~upper for orbit in options)]
                        if bad:
                            expected.append({'pattern_index': i, 'split_indices': bad})
                assert round_['removals'] == expected and expected
                upper &= ~sum(1 << item['pattern_index'] for item in expected)
            assert stage['upper_after'] == upper
        if 'refinement_stages' in query:
            assert query['final_upper_mask'] == upper
            assert query['final_accepted_preimages'] == preimages(upper)
        info = {'case_id': query['case_id'], 'extras': case['extras'],
                'target': query['target'], 'status': query['status'],
                'initial_upper_size': target['fixed_point'].bit_count(),
                'final_upper_size': upper.bit_count()}
        if query['status'] == 'excluded_transfer':
            assert not preimages(upper)[str(query['missing_outer_index'])]
        elif query['status'] == 'excluded_count':
            forced = identity(query['identity'], upper)
            needed = preimages(upper)[str(query['forced_outer_index'])]
            assert needed and set(needed) <= forced and query['forced_preimages'] == needed
            info.update(positive_lhs_terms=len(query['identity']['lhs']),
                        zero_rhs_terms=len(query['identity']['rhs']),
                        all_forced_preimages=needed)
        else:
            assert query['status'] == 'necessary_condition_residual'
            assert all(key in query for key in ('refinement_stages', 'final_upper_mask',
                       'final_accepted_preimages', 'residual_support_mask'))
            counts = list(map(Q, query['counts']))
            coefficients = list(map(Q, query['partition_coefficients']))
            assert len(counts) == 274 and len(coefficients) == 91
            assert all(x >= 0 for x in counts)
            assert sum(1 << i for i, x in enumerate(counts) if x) == upper
            assert upper == query['residual_support_mask']
            for i, x in enumerate(counts):
                assert x == sum(c for j, c in zip(active, coefficients) if j in equalities[i])
            outer = [sum(Q(t)*x for t, x in zip(row, counts)) for row in case['transfer']]
            assert list(map(str, outer)) == query['outer_counts']
            assert all((y > 0 if j in accepted else y == 0) for j, y in enumerate(outer))
            assert all(any(orbit & ~upper == 0 for orbit in options)
                       for i in range(274) if upper >> i & 1
                       for options in interface['kempe_obligations'][i])
            info.update(common_count_span='verified exactly',
                        full_support_Kempe='triggered and holds', actual_source='not triggered',
                        outer_counts=list(map(str, outer)),
                        fractional_nonzero_coordinates=sum(x.denominator > 1 for x in counts))
        reports.append(info)
    summary = dict(Counter(r['status'] for r in reports))
    assert summary == certificate['summary']
    consumed_files = ['interface.json', 'counts/certificate.v2.json']
    return {
        'status': 'PASS',
        'method': 'Independent literal word enumeration, block insertion partition enumeration, '
                  'pair-equality bitmask evaluation, exact Fraction count-vector reconstruction. '
                  'No imports from producer or primary checker. Interface combinatorial '
                  'correctness remains separately audited.',
        'frozen_base': '3097ef5be241b7777451a5ef8a663f3987d6b866',
        'file_sha256': {p: hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in consumed_files},
        'proper_orbits': 274, 'NC_partitions': 1430, 'active_equality_columns': 91,
        'identities_checked_on_all_NC_vectors': identity_count,
        'query_count': len(reports), 'summary': summary, 'queries': reports,
        'review_findings': [
            {'severity': 'resolved', 'finding': 'v2 residual closure was initially an optional '
             'field; strengthened schema now requires support and refinement data for each final residual.'},
            {'severity': 'boundary', 'finding': 'Certificate checker relies on separately '
             'verified interface data for full literal transfer and complete Kempe orbit enumeration.'},
            {'severity': 'boundary', 'finding': 'Final nonnegative rational vectors satisfy the '
             'common count span, actual support Kempe obligations and complete transfer, '
             'but are not graph realizations.'}]}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    parser.add_argument('--output', type=Path, default=HERE/'count_review.json')
    args = parser.parse_args()
    result = build()
    if args.write:
        with args.output.open('x') as stream:
            stream.write(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    else:
        assert json.loads(args.output.read_text()) == result, 'independent review mismatch'
    print(json.dumps({'status': 'PASS', 'queries': result['query_count'],
                      'summary': result['summary'],
                      'all_partition_identities': result['identities_checked_on_all_NC_vectors']},
                     sort_keys=True))


if __name__ == '__main__':
    main()
