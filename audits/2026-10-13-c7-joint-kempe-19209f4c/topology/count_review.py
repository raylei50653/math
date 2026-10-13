#!/usr/bin/env python3
"""Separate block-partition check of the seven universal count identities."""
import itertools as it
import json
from pathlib import Path
from independent_review import canonical, partitions, patterns, proper

HERE = Path(__file__).resolve().parent


def main():
    cert = json.loads((HERE.parent / 'joint/count_identity_certificate.json').read_text())
    words = patterns(7)
    assert cert['pattern_order'] == [list(w) for w in words]
    assert cert['boundary_order'] == ['a0', 'a1', 'y2', 'a2', 'a3', 'y4', 'a4']
    blocks_nc = []
    for blocks in partitions(7):
        owner = {v: j for j, b in enumerate(blocks) for v in b}
        if any(owner[a] == owner[c] and owner[b] == owner[d] and owner[a] != owner[b]
               for a, b, c, d in it.combinations(range(7), 4)):
            continue
        blocks_nc.append(blocks)
    assert len(blocks_nc) == 429
    upper = cert['upper_mask']
    expected_lhs = [{42: 1}, {49: 1}, {73: 1}, {75: 1}, {6: 1, 35: 1},
                    {6: -1, 58: 1}, {6: -1, 89: 1}]
    assert len(cert['identities']) == len(expected_lhs)
    for identity, expected in zip(cert['identities'], expected_lhs):
        assert {t['index']: t['coefficient'] for t in identity['lhs']} == expected
        for side in ('lhs', 'rhs'):
            assert all(t['word'] == list(words[t['index']]) for t in identity[side])
        assert all(not upper >> t['index'] & 1 for t in identity['rhs'])
        for blocks in blocks_nc:
            def value(side):
                return sum(t['coefficient'] for t in identity[side]
                           if all(len({words[t['index']][v] for v in b}) == 1 for b in blocks))
            assert value('lhs') == value('rhs')
    supports = [(0, 1), (1, 2), (2,), (2, 3), (3, 4), (4,), (4, 0)]
    needed_outer = (0, 1, 2, 3, 2)
    preimages = []
    for i, p in enumerate(words):
        if not upper >> i & 1:
            continue
        for b in it.product(range(4), repeat=5):
            if canonical(b) == needed_outer and all(p[v] != b[u] for v, sup in enumerate(supports) for u in sup):
                assert proper(b)
                preimages.append(i)
                break
    assert preimages == [6, 58, 89] == cert['upper_preimages_of_outer_word']
    # The last three verified identities and all-zero rejected counts give:
    # x6+x35=0; x58=x6; x89=x6. Counts are nonnegative, so all preimages vanish.
    print(json.dumps(dict(status='PASS', independently_generated_NC_partitions=429,
                          identities_checked=7, forced_zero_outer_preimages=preimages,
                          universal_scope='Every finite graph embedded in the named C7 disk',
                          verdict='No S subset U55 can transfer to 941')))


if __name__ == '__main__':
    main()
