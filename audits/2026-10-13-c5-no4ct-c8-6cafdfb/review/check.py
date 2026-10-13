#!/usr/bin/env python3
"""Independent finite C8 review; imports no producer or old checker code."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OLD = ROOT / 'frozen/audits/2026-10-13-c8-struct-243a125'


def norm(word):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in word)


def proper(word):
    return all(word[i] != word[(i+1) % len(word)] for i in range(len(word)))


def partitions(n):
    def extend(word):
        if len(word) == n:
            yield word
        else:
            for x in range(max(word)+2):
                yield from extend(word+(x,))
    return list(extend((0,)))


def noncrossing(part):
    return not any(part[a] == part[c] and part[b] == part[d] and part[a] != part[b]
                   for a, b, c, d in it.combinations(range(len(part)), 4))


def mask(indices):
    return sum(1 << x for x in set(indices))


def orbit_obligations(words, nc):
    index = {w: i for i, w in enumerate(words)}
    output = []
    # Pair 0 with each other color; the complement is the other pair.
    for word in words:
        per_split = []
        for partner in (1, 2, 3):
            first = {0, partner}
            other = sorted(set(range(4))-first)
            swap = {0: partner, partner: 0, other[0]: other[1], other[1]: other[0]}
            group = tuple(int(c in first) for c in word)
            possible = set()
            for part in nc:
                blocks = [tuple(i for i in range(8) if part[i] == b)
                          for b in range(max(part)+1)]
                if any(len({group[i] for i in block}) != 1 for block in blocks):
                    continue
                if any(group[i] == group[(i+1) % 8] and part[i] != part[(i+1) % 8]
                       for i in range(8)):
                    continue
                orbit = set()
                for bits in it.product((0, 1), repeat=len(blocks)):
                    changed = tuple(swap[c] if bits[part[i]] else c for i, c in enumerate(word))
                    assert proper(changed)
                    orbit.add(index[norm(changed)])
                possible.add(mask(orbit))
            assert possible
            per_split.append(sorted(possible))
        output.append(per_split)
    return output


def collar(extras):
    names, supports = [], []
    for i in range(5):
        names.append(f'a{i}')
        supports.append((i, (i+1) % 5))
        for j in range(1, extras[(i+1) % 5]+1):
            names.append(f'y{(i+1) % 5}_{j}')
            supports.append(((i+1) % 5,))
    return names, supports


def prune(columns, obligations, target):
    allowed = mask(i for i, col in enumerate(columns) if col & ~target == 0)
    initial = allowed
    while True:
        keep = mask(i for i in range(len(columns)) if allowed >> i & 1
                    and all(any(o & ~allowed == 0 for o in choices)
                            for choices in obligations[i]))
        if keep == allowed:
            break
        allowed = keep
    union = 0
    for i, col in enumerate(columns):
        if allowed >> i & 1:
            union |= col
    return dict(initial=initial, fixed_point=allowed, possible_outer_union=union,
                excluded=(union != target))


def build():
    literal8 = [w for w in it.product(range(4), repeat=8) if proper(w)]
    words8 = sorted({norm(w) for w in literal8})
    literal5 = [w for w in it.product(range(4), repeat=5) if proper(w)]
    words5 = sorted({norm(w) for w in literal5})
    assert (len(literal8), len(words8), len(literal5), len(words5)) == (6564, 274, 240, 10)
    index5 = {w: i for i, w in enumerate(words5)}
    parts = partitions(8)
    nc = [p for p in parts if noncrossing(p)]
    independent = [p for p in nc if proper(p)]
    assert (len(parts), len(nc), len(independent)) == (4140, 1430, 91)
    equalities = {p: [i for i, w in enumerate(words8)
                      if all(w[a] == w[b] for a in range(8) for b in range(a)
                             if p[a] == p[b])] for p in independent}
    quotient = json.loads((OLD / 'classification/quotient.json').read_text())
    results = json.loads((OLD / 'RESULTS.json').read_text())
    assert quotient['patterns'] == list(map(list, words8))
    assert {tuple(c['partition']): c['equality_rows'] for c in quotient['conditions']} == equalities
    cofacial = []
    for query in quotient['queries']:
        upper = query['final_upper_mask']
        intersections = [[i for i in equalities[tuple(cond['partition'])] if upper >> i & 1]
                         for cond in quotient['conditions']]
        assert intersections == query['intersections']
        final = next(x for x in results['queries'] if x['query_id'] == query['query_id'])
        if query['query_id'] not in ('c16-941', 'c32-941'):
            assert final['support'] & ~upper == 0
            assert all(any(final['support'] >> i & 1 for i in rows)
                       for rows in equalities.values())
        row = dict(query_id=query['query_id'], empty_conditions=sum(not x for x in intersections))
        if query['query_id'] in ('c16-941', 'c32-941'):
            positions = [query['boundary_order'].index(x) for x in ('a1', 'a4')]
            equals = [i for i, w in enumerate(words8) if w[positions[0]] == w[positions[1]]]
            assert len(equals) == 74 and not any(upper >> i & 1 for i in equals)
            assert row['empty_conditions'] == 9
            row.update(pair_positions=positions, all_equal_rows=equals)
        else:
            assert row['empty_conditions'] == 0
        cofacial.append(row)

    obligations = orbit_obligations(words8, nc)
    cases = []
    for extras in it.product(range(4), repeat=5):
        if sum(extras) != 3:
            continue
        names, supports = collar(extras)
        columns, fibres = [], []
        for inner in words8:
            rows = [[] for _ in words5]
            for outer in literal5:
                if all(inner[j] != outer[b] for j, contact in enumerate(supports) for b in contact):
                    rows[index5[norm(outer)]].append(list(outer+inner))
            columns.append(mask(i for i, fibre in enumerate(rows) if fibre))
            fibres.append(rows)
        cases.append(dict(extras=list(extras), names=names, columns=columns, fibres=fibres,
                          targets={str(t): prune(columns, obligations, t) for t in (932, 933, 941)}))
    assert len(cases) == 35
    new = [c['targets']['932'] for c in cases]
    assert all(t['excluded'] for t in new)
    assert sum(t['fixed_point'] == 0 for t in new) == 30
    assert sum(t['fixed_point'] != 0 for t in new) == 5
    return dict(schema='independent-no4ct-c8-review-v1', cases=cases,
                words8=list(map(list, words8)), words5=list(map(list, words5)),
                obligations=obligations, cofacial=cofacial,
                summary=dict(collared_queries=105, new_932_queries=35,
                             new_932_excluded=35, new_932_empty_fixed_points=30,
                             cofacial_conditions=91, cofacial_intersections=910,
                             source_status='not triggered', graph_source_search=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--producer', type=Path)
    args = parser.parse_args()
    result = build()
    out = HERE / 'certificate.json'
    if args.write:
        with out.open('x') as stream:
            json.dump(result, stream, sort_keys=True, separators=(',', ':'))
            stream.write('\n')
    else:
        assert result == json.loads(out.read_text()), 'independent certificate mismatch'
    if args.producer:
        producer = json.loads(args.producer.read_text())
        interface = producer['interface']
        assert interface['pattern_order'] == result['words8']
        assert interface['outer_pattern_order'] == result['words5']
        assert len(interface['cases']) == len(result['cases']) == 35
        for own, theirs in zip(result['obligations'], interface['kempe_obligations']):
            assert [set(x) for x in own] == [set(x) for x in theirs], 'Kempe orbit mismatch'
        for own, theirs in zip(result['cases'], interface['cases']):
            assert own['extras'] == theirs['extras']
            assert own['names'] == theirs['boundary_order']
            assert own['columns'] == theirs['column_masks']
            assert own['fibres'] == theirs['joint_full_lifts_by_inner_index_then_outer_index'], 'full lift mismatch'
            for row in theirs['targets']:
                expected = own['targets'][str(row['target'])]
                assert all(row[key] == value for key, value in expected.items()), 'target fixed point mismatch'
                assert row['accepted_preimages'] == {
                    str(i): [j for j, col in enumerate(own['columns'])
                             if row['fixed_point'] >> j & 1 and col >> i & 1]
                    for i in range(10) if row['target'] >> i & 1}, 'accepted preimages mismatch'
            # Orbit double counting: fix an inner representative and range over
            # the 24 literal B orbit words, then fix B and range over its inner
            # orbit. Inner alternating words have orbit size 12, others 24.
            for r in range(10):
                for p, word in enumerate(result['words8']):
                    size = 12 if len(set(word)) == 2 else 24
                    count = len(own['fibres'][p][r]) * size
                    assert count % 24 == 0
                    assert count // 24 == theirs['transfer'][r][p], 'transfer count mismatch'
        result['summary']['producer_comparison'] = 'PASS: full fibres, columns, orbits, 105 fixed points, transfer, accepted preimages'
    print(json.dumps(dict(status='PASS', **result['summary'],
                          certificate_sha256=hashlib.sha256(out.read_bytes()).hexdigest())))


if __name__ == '__main__':
    main()
