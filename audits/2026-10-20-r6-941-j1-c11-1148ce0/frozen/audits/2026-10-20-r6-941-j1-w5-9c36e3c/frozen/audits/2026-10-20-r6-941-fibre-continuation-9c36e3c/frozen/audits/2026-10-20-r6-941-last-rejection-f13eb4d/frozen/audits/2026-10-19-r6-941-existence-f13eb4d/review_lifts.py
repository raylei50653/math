"""Independent direct-edge audit of the two c=5 quotient projections."""
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = HERE / 'frozen'
PINS = ('a', 'n', 'R', 'L', 'q', 'u', 's', 'v', 'w', 't')
ROWS = ('01012', '01021', '01023', '01201', '01202',
        '01203', '01212', '01213', '01231', '01232')


def canonical(t):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in t)


def main():
    cert = json.loads(gzip.decompress((HERE / 'B/certificate.json.gz').read_bytes()))
    caps = json.loads(gzip.decompress((HERE / 'B/cap-lifts.json.gz').read_bytes()))
    assert cert['literal_rows'] == list(ROWS)
    assert cert['core_order'] == list(PINS)
    # Reconstruct the original full stars as undirected edge sets. Delete p,h
    # before identifying classes; no independently selected marginal lifts.
    stars = {
        'b': ('a', 'c', 'p', 'q'),
        'p': ('a', 'b', 'q', 'h', 'n'),
        'h': ('p', 'q', 'L', 'R', 'n'),
        'c': ('b', 'q', 'u', 's', 'x'),
        'x': ('y', 'c', 'r', 's'),
        'y': ('x', 'a', 'r', 't'),
        'r': ('x', 'y', 't', 'w', 'v', 's'),
    }
    edges = {tuple(sorted((v, w))) for v, ns in stars.items() for w in ns}
    edges.update(tuple(sorted((PINS[i], PINS[(i + 1) % 10]))) for i in range(10))
    remaining = sorted(e for e in edges if not {'p', 'h'} & set(e))
    matrices = [[[0] * len(cert['core_states']) for _ in ROWS] for _ in range(2)]
    complete = empty = 0
    for i, word in enumerate(cert['core_states']):
        core = dict(zip(PINS, word))
        for j, groups in enumerate(((('n', 'b'), ('R', 'q')), (('n', 'L', 'b'),))):
            actual = []
            for b, c in itertools.product(range(4), repeat=2):
                fixed = dict(core, b=b, c=c)
                if any(len({fixed[v] for v in group}) != 1 for group in groups):
                    continue
                # Test every retained edge with assigned endpoints before the
                # final right cap, solely as a pruning step.
                if any(fixed[v] == fixed[w] for v, w in remaining if v in fixed and w in fixed):
                    continue
                for x, y, r in itertools.product(range(4), repeat=3):
                    f = dict(fixed, x=x, y=y, r=r)
                    if any(f[v] == f[w] for v, w in remaining):
                        continue
                    actual.append((b, c, x, y, r))
                    row = ROWS.index(''.join(map(str, canonical((x, y, f['a'], b, c)))))
                    matrices[j][row][i] += 1
            expected = sorted((b, rec['c'], *right)
                              for rec in caps['Q_and_S_caps'][i]['Q_by_c']
                              for b in rec['Q' + str(j + 1) + '_b']
                              for right in rec['right'])
            assert sorted(actual) == expected, ('all direct quotient lifts', j, i)
            complete += len(actual)
            empty += not actual
            divisor = math.factorial(4 - len(set(word)))
            for row in matrices[j]:
                assert row[i] % divisor == 0
                row[i] //= divisor
    assert matrices == cert['Q_matrices'], 'all fixed-literal quotient coefficients'
    assert cert['H4_zero_implies_Q_supports'] == [1021, 1021]
    for branch in cert['H4_zero_branches']:
        for j in range(2):
            options = [r['hypothesis'] for r in branch['Q_catalogue_comparisons'][j] if r['not_excluded']]
            assert options == [1021]
            assert branch['acceptance_zero'][j]['original_upper'] == 429
    print(json.dumps({'pass': True, 'direct_full_lifts': complete,
                      'empty_quotient_fibres': empty, 'complete_quotient_fibres': 2 * len(cert['core_states']),
                      'literal_matrix_entries': 20 * len(cert['core_states']),
                      'H4_zero_implies_Q_supports': [1021, 1021],
                      'source_realized': False}, sort_keys=True))


if __name__ == '__main__':
    main()
