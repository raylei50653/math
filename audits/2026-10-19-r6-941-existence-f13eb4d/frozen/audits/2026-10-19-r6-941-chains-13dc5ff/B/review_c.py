#!/usr/bin/env python3
"""Independent edge-based C review; does not import C/check.py."""
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path

D = Path(__file__).resolve().parent
C = D.parent / 'C'
ROWS = ('01012', '01021', '01023', '01201', '01202', '01203', '01212', '01213', '01231', '01232')
PINS = ('a', 'n', 'R', 'L', 'q', 'u', 's', 'v', 'w', 't')
STARS = {'b': ('a', 'c', 'p', 'q'), 'p': ('a', 'b', 'q', 'h', 'n'),
         'h': ('p', 'q', 'L', 'R', 'n'), 'x': ('y', 'c', 'r', 's'),
         'y': ('x', 'a', 'r', 't'), 'r': ('x', 'y', 't', 'w', 'v', 's'),
         'c': ('b', 'q', 'u', 's', 'x')}


def canonical(values):
    seen = {}
    return ''.join(str(seen.setdefault(v, len(seen))) for v in values)


def main():
    cert = json.loads(gzip.decompress((C / 'certificate.json.gz').read_bytes()))
    caps = json.loads(gzip.decompress((C / 'cap-lifts.json.gz').read_bytes()))
    full_edges = {tuple(sorted((u, v))) for u, nbrs in STARS.items() for v in nbrs}
    base_edges = {e for e in full_edges if 'c' not in e}
    assignments = tuple(itertools.product(range(4), repeat=3))
    result = [[[0] * len(caps) for _ in ROWS] for _ in range(6)]
    full_products = 0
    for i, entry in enumerate(caps):
        f = dict(zip(PINS, entry['core']))
        assert tuple(entry['core']) == tuple(cert['core_states'][i])
        for side, names in (('left', ('b', 'p', 'h')), ('right', ('x', 'y', 'r'))):
            side_edges = {e for e in base_edges if set(e) & set(names)}
            possible = [t for t in assignments if all(
                dict(f, **dict(zip(names, t)))[u] != dict(f, **dict(zip(names, t)))[v]
                for u, v in side_edges)]
            for old in entry['original_by_c']:
                c = old['c']
                relevant = {e for e in full_edges if set(e) <= set(f) | set(names) | {'c'}}
                expected = [t for t in possible if all(
                    dict(f, c=c, **dict(zip(names, t)))[u] != dict(f, c=c, **dict(zip(names, t)))[v]
                    for u, v in relevant)]
                assert expected == [tuple(t) for t in old[side]]
            for j, candidate in enumerate(entry['candidates']):
                additions = cert['operations'][j]['added_edges']
                # A core-only failing edge may zero either factor; the stored
                # convention assigns it to left. Full products are checked below.
                relevant = [e for e in additions if set(e) <= set(f) | set(names)
                            and (side == 'left' or set(e) & set(names))]
                expected = [t for t in possible if all(
                    dict(f, **dict(zip(names, t)))[u] != dict(f, **dict(zip(names, t)))[v]
                    for u, v in relevant)]
                assert expected == [tuple(t) for t in candidate[side]]
        groups = [(0, old['c'], old['left'], old['right']) for old in entry['original_by_c']]
        groups += [(j + 1, f[cert['operations'][j]['boundary'][-1]], v['left'], v['right'])
                   for j, v in enumerate(entry['candidates'])]
        for index, fifth, left, right in groups:
            for l, r in itertools.product(left, right):
                b, p, h = l
                x, y, rv = r
                ff = dict(f, b=b, p=p, h=h, x=x, y=y, r=rv)
                if index == 0:
                    ff['c'] = fifth
                    es = full_edges
                else:
                    es = base_edges | {tuple(e) for e in cert['operations'][index - 1]['added_edges']}
                assert all(ff[u] != ff[v] for u, v in es)
                row = ROWS.index(canonical((x, y, f['a'], b, fifth)))
                result[index][row][i] += 1
                full_products += 1
        factor = math.factorial(4 - len(set(entry['core'])))
        for matrix in result:
            for row in matrix:
                assert row[i] % factor == 0
                row[i] //= factor
    matrices = [cert['original_matrix']] + cert['candidate_matrices']
    assert result == matrices, 'all six independently reconstructed literal matrices'

    def upper(matrix, live):
        return sum(1 << r for r in range(10) if any(matrix[r][i] for i in live))

    surviving = []
    for entry in cert['joint_comparisons']:
        actual = [upper(matrix, entry['live']) for matrix in result]
        assert actual[0] == entry['original_support_upper']
        assert actual[1:] == entry['candidate_support_uppers']
        supports = entry['exact_supports_hypothesis']
        valid = actual[0] == 941 and all(s & u == s for s, u in zip(supports, actual[1:]))
        assert valid == entry['not_excluded_by_zero_closure']
        if valid:
            surviving.append(entry['zero_bits'])
    individual_comparisons = 0
    for j, summary in enumerate(cert['individual_comparisons']):
        possible = []
        for entry in summary['comparisons']:
            original = upper(result[0], entry['live'])
            candidate = upper(result[j + 1], entry['live'])
            assert original == entry['original_support_upper']
            assert [candidate] == entry['candidate_support_uppers']
            support = entry['allowed_catalogue_support']
            valid = original == 941 and support & candidate == support
            assert valid == entry['not_excluded_by_zero_closure']
            if valid:
                possible.append(support)
            individual_comparisons += 1
        assert possible == summary['compatible_catalogue_supports']
    assert surviving == [2, 6, 10, 11, 14, 26, 27, 30]
    output = {'pass': True, 'reviewed_core_states': len(caps),
              'independently_checked_full_cap_products': full_products,
              'independently_rebuilt_literal_matrices': 6,
              'individual_support_comparisons': individual_comparisons,
              'joint_support_comparisons': 32, 'surviving_zero_bits': surviving,
              'C_reviewed_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in (C / 'check.py', C / 'PROOF.md',
                                             C / 'certificate.json.gz', C / 'cap-lifts.json.gz')}}
    print(json.dumps(output, sort_keys=True))


if __name__ == '__main__':
    main()
