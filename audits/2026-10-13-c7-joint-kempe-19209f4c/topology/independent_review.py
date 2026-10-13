#!/usr/bin/env python3
"""Independent RGS/noncrossing-partition and literal graph verification."""
import argparse
import copy
import hashlib
import itertools as it
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent


def canonical(word):
    order = list(dict.fromkeys(word))
    return tuple(order.index(x) for x in word)


def proper(word):
    return all(a != b for a, b in zip(word, word[1:] + word[:1]))


@lru_cache(None)
def patterns(n):
    def grow(w):
        if len(w) == n:
            if proper(w):
                yield w
        else:
            for c in range(min(3, max(w, default=-1) + 1) + 1):
                yield from grow(w + (c,))
    return tuple(grow(()))


@lru_cache(None)
def partitions(n):
    if n == 0:
        return ((),)
    out = []
    for blocks in partitions(n - 1):
        out.append(blocks + ((n - 1,),))
        for j in range(len(blocks)):
            out.append(blocks[:j] + (blocks[j] + (n - 1,),) + blocks[j + 1:])
    return tuple(out)


def kempe(n):
    ps = patterns(n)
    index = {p: j for j, p in enumerate(ps)}
    nc = []
    for blocks in partitions(n):
        owner = [next(j for j, b in enumerate(blocks) if v in b) for v in range(n)]
        if any(owner[a] == owner[c] and owner[b] == owner[d] and owner[a] != owner[b]
               for a, b, c, d in it.combinations(range(n), 4)):
            continue
        nc.append((blocks, owner))
    table = []
    for p in ps:
        row = []
        for pair in ((0, 1), (0, 2), (0, 3)):
            other = tuple(c for c in range(4) if c not in pair)
            side = [c in pair for c in p]
            swap = {pair[0]: pair[1], pair[1]: pair[0], other[0]: other[1], other[1]: other[0]}
            options = set()
            for blocks, owner in nc:
                if any(len({side[v] for v in b}) != 1 for b in blocks):
                    continue
                if any(side[v] == side[(v + 1) % n] and owner[v] != owner[(v + 1) % n]
                       for v in range(n)):
                    continue
                mask = 0
                for switches in it.product((False, True), repeat=len(blocks)):
                    word = tuple(swap[c] if switches[owner[v]] else c for v, c in enumerate(p))
                    mask |= 1 << index[canonical(word)]
                options.add(mask)
            row.append(options)
        table.append(row)
    return table


def screen(columns, obligations, target):
    allowed = sum(1 << i for i, col in enumerate(columns) if col | target == target)
    while True:
        before = allowed
        for i, row in enumerate(obligations):
            if allowed >> i & 1 and any(not any(o | allowed == allowed for o in options) for options in row):
                allowed ^= 1 << i
        if allowed == before:
            break
    union = 0
    for i, col in enumerate(columns):
        if allowed >> i & 1:
            union |= col
    return allowed, union


def verify(cert):
    for r in cert['inputs']:
        assert hashlib.sha256((HERE / r['frozen']).read_bytes()).hexdigest() == r['sha256']
    assert cert['named_ring'] == ['a0', 'a1', 'y2', 'a2', 'a3', 'y4', 'a4']
    for n in (4, 5, 6, 7):
        assert cert['pattern_orders'][str(n)] == [list(p) for p in patterns(n)]
    k = sorted(map(int, json.loads((HERE / 'frozen/cells.json').read_text())['cells']))
    assert cert['short_C5_K132'] == k and len(k) == 132
    l4 = [7, 10, 11, 12, 13, 14, 15]
    assert cert['short_C4_necessary_masks'] == l4
    p7 = patterns(7)
    indexes = {n: {p: i for i, p in enumerate(patterns(n))} for n in (4, 5, 6, 7)}
    supports = [(0, 1), (1, 2), (2,), (2, 3), (3, 4), (4,), (4, 0)]
    collar = cert['original_collar']
    assert collar['inner_supports'] == [list(s) for s in supports]
    columns = []
    for i, p in enumerate(p7):
        assignments = [list(b) for b in it.product(range(4), repeat=5)
                       if proper(b) and all(p[v] not in [b[u] for u in sup]
                                            for v, sup in enumerate(supports))]
        assert collar['outer_lifts_for_each_named_inner_row'][i] == assignments
        col = sum({1 << indexes[5][canonical(b)] for b in assignments})
        columns.append(col)
    assert columns == collar['column_masks']
    assert len(cert['chords']) == 6468
    seen = set()
    for r in cert['chords']:
        s, a, b = r['start'], r['short_mask'], r['long_mask']
        assert (s, a, b) not in seen
        seen.add((s, a, b))
        assert s in range(7) and a in l4 and b in k
        left = [(s + j) % 7 for j in range(4)]
        right = [(s + j) % 7 for j in range(3, 8)]
        assert r['short_cycle'] == left and r['long_cycle'] == right
        accepted = []
        for i, p in enumerate(p7):
            q, t = tuple(p[v] for v in left), tuple(p[v] for v in right)
            if proper(q) and proper(t) and a >> indexes[4][canonical(q)] & 1 and b >> indexes[5][canonical(t)] & 1:
                accepted.append(i)
        mask = sum(1 << i for i in accepted)
        outer = 0
        for i in accepted:
            outer |= columns[i]
        assert r['inner_accepted_mask'] == mask and r['inner_rejected_mask'] == ((1 << 91) - 1) ^ mask
        assert r['outer_accepted_mask'] == outer and r['outer_rejected_mask'] == 1023 ^ outer
        assert outer in k
    tables = {n: kempe(n) for n in (6, 7)}
    assert len(cert['two_edge_crosscuts']) == 973
    seen = set()
    full_words = {n: [w for w in it.product(range(4), repeat=n) if proper(w)] for n in (4, 5)}
    for r in cert['two_edge_crosscuts']:
        d, s, a = r['distance'], r['start'], r['short_mask']
        assert (d, s, a) not in seen
        seen.add((d, s, a))
        assert d in (2, 3) and s in range(7) and a in (l4 if d == 2 else k)
        short = [(s + j) % 7 for j in range(d + 1)] + [7]
        long = [(s + j) % 7 for j in range(d, 8)] + [7]
        assert r['short_cycle'] == short and r['long_cycle'] == long
        short_words = [w for w in full_words[d + 2] if a >> indexes[d + 2][canonical(w)] & 1]
        result = []
        for j, p in enumerate(patterns(9 - d)):
            pins = dict(zip(long, p))
            completions = set()
            for w in short_words:
                mapping = dict(zip(short, w))
                if any(mapping[v] != pins[v] for v in (s, (s + d) % 7, 7)):
                    continue
                joined = pins | mapping
                ring = tuple(joined[v] for v in range(7))
                assert proper(ring)
                completions.add(ring)
            assert sorted(completions) == sorted(map(tuple, r['completion_words_by_long_row'][j]))
            assert len(completions) == len(r['completion_words_by_long_row'][j])
            col = 0
            for ring in completions:
                col |= columns[indexes[7][canonical(ring)]]
            result.append(col)
        assert r['column_masks'] == result
        fixed, outer = screen(result, tables[9 - d], 941)
        assert r['screen']['fixed_point'] == fixed and r['screen']['possible_outer_union'] == outer
        assert outer != 941 and outer & ~429 == 0
        before = sum(1 << i for i, c in enumerate(result) if c & ~941 == 0)
        assert r['screen']['initial'] == before
        for round_ in r['screen']['rounds']:
            assert round_['before'] == before
            deleted = 0
            for drop in round_['removals']:
                i = drop['pattern_index']
                assert before >> i & 1
                bad = [j for j, options in enumerate(tables[9 - d][i])
                       if not any(o & ~before == 0 for o in options)]
                assert bad == drop['split_indices'] and bad
                deleted |= 1 << i
            before &= ~deleted
        assert before == fixed
    return dict(status='PASS', chord_joins=6468, excluded_crosscuts=973,
                every_crosscut_possible_outer_union_subset_of=429)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    p.add_argument('--negative-controls', action='store_true')
    a = p.parse_args()
    cert = json.loads(a.certificate.read_text())
    result = verify(cert)
    if a.negative_controls:
        mutations = [
            ('alter_accepted_inner_row', lambda c: c['chords'][0].__setitem__('inner_accepted_mask', c['chords'][0]['inner_accepted_mask'] ^ 1)),
            ('alter_rejected_inner_row', lambda c: c['chords'][0].__setitem__('inner_rejected_mask', c['chords'][0]['inner_rejected_mask'] ^ 1)),
            ('delete_literal_outer_lift', lambda c: next(row for row in c['original_collar']['outer_lifts_for_each_named_inner_row'] if row).pop()),
            ('alter_crosscut_fixed_point', lambda c: c['two_edge_crosscuts'][0]['screen'].__setitem__('fixed_point', c['two_edge_crosscuts'][0]['screen']['fixed_point'] ^ 1)),
            ('delete_short_completion', lambda c: next(row for row in c['two_edge_crosscuts'][0]['completion_words_by_long_row'] if row).pop()),
        ]
        results = []
        for name, mutate in mutations:
            bad = copy.deepcopy(cert)
            mutate(bad)
            try:
                verify(bad)
            except AssertionError:
                results.append(dict(name=name, status='counterexample', corrupted_certificate_rejected=True))
            else:
                raise AssertionError(name + ' was not rejected')
        result['negative_controls'] = results
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
