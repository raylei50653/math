#!/usr/bin/env python3
"""Read-only independent review: reverse transfer and asynchronous pruning."""
import hashlib
import json
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / 'frozen'
NEAR = FROZEN / 'audits/2026-10-12-neartri-complete-relation-reductions-5d70a399'


def normalize(word):
    names = []
    answer = []
    for color in word:
        if color not in names:
            names.append(color)
        answer.append(names.index(color))
    return tuple(answer)


@lru_cache(None)
def partitions(n):
    words = [(0,)]
    for _ in range(1, n):
        words = [w + (x,) for w in words for x in range(max(w) + 2)]
    return tuple(words)


@lru_cache(None)
def noncrossing(n):
    return tuple(w for w in partitions(n) if not any(
        w[a] == w[c] and w[b] == w[d] and w[a] != w[b]
        for a, b, c, d in combinations(range(n), 4)))


def orbit_table(patterns):
    n = len(patterns[0])
    index = {w: i for i, w in enumerate(patterns)}
    splits = ((0, 1), (0, 2), (0, 3))
    answer = []
    for word in patterns:
        row = []
        for pair in splits:
            opposite = tuple(x for x in range(4) if x not in pair)
            color_side = {x: int(x not in pair) for x in range(4)}
            swap = {pair[0]: pair[1], pair[1]: pair[0],
                    opposite[0]: opposite[1], opposite[1]: opposite[0]}
            options = set()
            for part in noncrossing(n):
                blocks = [tuple(j for j in range(n) if part[j] == b)
                          for b in range(max(part) + 1)]
                if any(len({color_side[word[j]] for j in block}) != 1
                       for block in blocks):
                    continue
                if any(color_side[word[j]] == color_side[word[(j + 1) % n]]
                       and part[j] != part[(j + 1) % n] for j in range(n)):
                    continue
                orbit = 0
                for selected in product((False, True), repeat=len(blocks)):
                    changed = tuple(swap[x] if selected[part[j]] else x
                                    for j, x in enumerate(word))
                    orbit |= 1 << index[normalize(changed)]
                options.add(orbit)
            assert options
            row.append(sorted(options))
        answer.append(row)
    return answer


def reverse_transfer(t, patterns, outer_patterns):
    # Fix the original outer word first, then enumerate literal inner colors.
    supports = []
    for i in range(5):
        supports.append((i, (i + 1) % 5))
        supports.extend([((i + 1) % 5,)] * t[(i + 1) % 5])
    index = {w: j for j, w in enumerate(patterns)}
    columns = [0] * len(patterns)
    for outer_index, outer in enumerate(outer_patterns):
        domains = [tuple(c for c in range(4) if all(c != outer[b] for b in s))
                   for s in supports]

        def visit(word):
            if len(word) == len(domains):
                if word[-1] != word[0]:
                    columns[index[normalize(word)]] |= 1 << outer_index
                return
            for color in domains[len(word)]:
                if not word or word[-1] != color:
                    visit(word + (color,))

        visit(())
    return columns


def asynchronous(columns, table, target):
    allowed = {i for i, column in enumerate(columns) if column & ~target == 0}
    initial = len(allowed)
    while True:
        changed = False
        # Immediate deletions, in reverse order, differ from the source checker.
        for i in sorted(allowed, reverse=True):
            mask = sum(1 << j for j in allowed)
            if any(not any(orbit & ~mask == 0 for orbit in options)
                   for options in table[i]):
                allowed.remove(i)
                changed = True
        if not changed:
            break
    union = 0
    for i in allowed:
        union |= columns[i]
    return dict(target=target, initial_size=initial, fixed_size=len(allowed),
                fixed_mask=sum(1 << i for i in allowed), possible_outer_union=union)


def main():
    inputs = json.loads((ROOT / 'INPUTS.json').read_text())['inputs']
    for entry in inputs:
        data = (FROZEN / entry['path']).read_bytes()
        assert len(data) == entry['bytes']
        assert hashlib.sha256(data).hexdigest() == entry['sha256']

    source = json.loads((NEAR / 'collar_certificate.json').read_text())
    pats = {int(n): tuple(map(tuple, rows)) for n, rows in source['inner_pattern_orders'].items()}
    outer = tuple(map(tuple, source['outer_pattern_order']))
    tables = {n: orbit_table(rows) for n, rows in pats.items()}
    for n, table in tables.items():
        assert table == source['kempe_obligations'][str(n)]

    cases = []
    for case in source['cases']:
        t = case['boundary_extras']
        n = 5 + sum(t)
        columns = reverse_transfer(t, pats[n], outer)
        assert columns == case['column_masks']
        queries = [asynchronous(columns, tables[n], target) for target in (932, 933, 941)]
        for old in case['targets']:
            new = next(q for q in queries if q['target'] == old['target'])
            assert new['fixed_mask'] == old['fixed_point']
            assert new['possible_outer_union'] == old['possible_outer_union']
        cases.append(dict(extras=t, queries=queries))
    survivors = [(c['extras'], q) for c in cases for q in c['queries']
                 if q['possible_outer_union'] == q['target']]
    assert len(cases) == 21 and len(survivors) == 1
    assert survivors[0][0] == [0, 0, 1, 0, 1]
    assert survivors[0][1]['target'] == 941
    assert survivors[0][1]['fixed_mask'] == 755425272170557940120206052
    assert all(q['fixed_mask'] == 0 for c in cases for q in c['queries'] if q['target'] == 932)

    submitted = json.loads((ROOT / 'collar/certificate.json').read_text())
    assert len(submitted['cases']) == len(cases)
    for original, independent, new in zip(source['cases'], cases, submitted['cases']):
        assert new['boundary_extras'] == independent['extras']
        assert new['column_masks'] == original['column_masks']
        for query, result in zip(independent['queries'], new['targets']):
            assert query['target'] == result['target']
            assert query['fixed_mask'] == result['fixed_point']
            assert query['possible_outer_union'] == result['possible_outer_union']

    # Independently verify all 924 common-color crosscuts from literal pin values.
    joins = json.loads((NEAR / 'certificate.json').read_text())['crosscut_joins']
    c4p = tuple(sorted({normalize(w) for w in product(range(4), repeat=4)
                       if all(w[i] != w[(i + 1) % 4] for i in range(4))}))
    c4i = {w: i for i, w in enumerate(c4p)}
    c5i = {w: i for i, w in enumerate(outer)}
    catalog_path = FROZEN / 'audits/2026-10-13-c5-no4ct-degrees-6cafdfb/frozen/audits/2026-10-12-c5-saturation-degree-bound/frozen/cells.json'
    catalog = {int(x) for x in json.loads(catalog_path.read_text())['cells']}
    assert len(catalog) == 132
    results = set()
    for join in joins:
        mask = 0
        for pi, p in enumerate(outer):
            common = []
            for color in range(4):
                sw = (p[2], p[3], p[4], color)
                lw = (p[4], p[0], p[1], p[2], color)
                si, li = c4i.get(normalize(sw)), c5i.get(normalize(lw))
                if si is not None and li is not None and join['short_mask'] >> si & 1 and join['long_mask'] >> li & 1:
                    common.append(color)
            assert common == join['fibres'][pi]['joint']
            if common:
                mask |= 1 << pi
        assert mask == join['result'] and mask in catalog
        results.add(mask)
    assert len(joins) == 924 and len(results) == 90

    # Check the exact signed C7 identities on an independent NC-partition list.
    count = json.loads((FROZEN / 'audits/2026-10-13-c7-joint-kempe-19209f4c/joint/count_identity_certificate.json').read_text())
    assert tuple(map(tuple, count['noncrossing_partitions'])) == noncrossing(7)
    count_patterns = tuple(map(tuple, count['pattern_order']))
    assert count_patterns == pats[7]
    for identity in count['identities']:
        assert all(not (count['upper_mask'] >> term['index'] & 1)
                   for term in identity['rhs'])
        for term in identity['lhs'] + identity['rhs']:
            assert tuple(term['word']) == count_patterns[term['index']]
        for part in noncrossing(7):
            def evaluate(terms):
                return sum(term['coefficient'] * all(
                    part[a] != part[b] or count_patterns[term['index']][a] == count_patterns[term['index']][b]
                    for a in range(7) for b in range(a)) for term in terms)
            assert evaluate(identity['lhs']) == evaluate(identity['rhs'])
    special = next(c for c in source['cases'] if c['boundary_extras'] == [0, 0, 1, 0, 1])
    upper = count['upper_mask']
    assert outer[9] == (0, 1, 2, 3, 2)
    assert [sorted((term['index'], term['coefficient']) for term in item['lhs'])
            for item in count['identities'][4:]] == [
                [(6, 1), (35, 1)], [(6, -1), (58, 1)], [(6, -1), (89, 1)]]
    preimages = [i for i, col in enumerate(special['column_masks']) if upper >> i & 1 and col >> 9 & 1]
    assert preimages == count['upper_preimages_of_outer_word'] == [6, 58, 89]
    print(json.dumps(dict(status='PASS', frozen_inputs=len(inputs), crosscuts=924,
                         crosscut_distinct_outputs=90, reverse_transfers=21,
                         asynchronous_queries=63, direct_exclusions=62,
                         c7_partitions=len(noncrossing(7)), c7_identities=len(count['identities']),
                         c7_preimages=preimages, survivors=survivors, cases=cases), indent=2))


if __name__ == '__main__':
    main()
