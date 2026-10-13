#!/usr/bin/env python3
"""Independent maximal complementary-partition check, no source enumeration."""
from itertools import combinations, product
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'frozen/audits/2026-10-12-neartri-complete-relation-reductions-5d70a399'
UPPER = 755425272170557940120206052
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def canonical(word):
    colors = []
    result = []
    for color in word:
        if color not in colors:
            colors.append(color)
        result.append(colors.index(color))
    return tuple(result)


def partitions(items):
    if not items:
        yield ()
        return
    for tail in partitions(items[1:]):
        yield ((items[0],),) + tail
        for j in range(len(tail)):
            yield tail[:j] + ((items[0],) + tail[j],) + tail[j+1:]


def valid(blocks, side):
    owner = {v: j for j, block in enumerate(blocks) for v in block}
    if any(side[i] == side[(i+1) % 7] and owner[i] != owner[(i+1) % 7]
           for i in range(7)):
        return False
    return not any(owner[a] == owner[c] and owner[b] == owner[d]
                   and owner[a] != owner[b]
                   for a, b, c, d in combinations(range(7), 4))


def options(word, split, index):
    side = tuple(int(c in split[1]) for c in word)
    left = tuple(i for i in range(7) if side[i] == 0)
    right = tuple(i for i in range(7) if side[i] == 1)
    transitions = sum(side[i] != side[(i+1) % 7] for i in range(7))
    minimal_blocks = transitions // 2 + 1
    swap = {a: b for pair in split for a, b in (pair, pair[::-1])}
    result = []
    for lp in partitions(left):
        for rp in partitions(right):
            blocks = lp + rp
            if not valid(blocks, side):
                continue
            assert len(blocks) >= minimal_blocks
            owner = {v: j for j, block in enumerate(blocks) for v in block}
            orbit = 0
            for bits in range(1 << len(blocks)):
                image = canonical(tuple(swap[c] if bits & (1 << owner[i]) else c
                                        for i, c in enumerate(word)))
                orbit |= 1 << index[image]
            result.append(dict(blocks=blocks, orbit=orbit,
                               maximal=len(blocks) == minimal_blocks))
    return result


def build():
    frozen = json.loads((BASE / 'collar_certificate.json').read_text())
    words = tuple(sorted({canonical(w) for w in product(range(4), repeat=7)
                          if all(w[i] != w[(i+1) % 7] for i in range(7))}))
    assert list(map(list, words)) == frozen['inner_pattern_orders']['7']
    index = {w: i for i, w in enumerate(words)}
    case, = [x for x in frozen['cases'] if x['boundary_extras'] == [0,0,1,0,1]]
    rows = []
    domination_checks = 0
    triple_count = 0
    for i, word in enumerate(words):
        splits = []
        for j, split in enumerate(SPLITS):
            opts = options(word, split, index)
            all_orbits = sorted({o['orbit'] for o in opts})
            assert all_orbits == frozen['kempe_obligations']['7'][i][j]
            maximal = [o for o in opts if o['maximal']]
            assert maximal
            for opt in opts:
                witnesses = [m for m in maximal if m['orbit'] & ~opt['orbit'] == 0]
                assert witnesses, (word, split, opt)
                domination_checks += 1
            viable = [m for m in maximal if m['orbit'] & ~UPPER == 0]
            splits.append(dict(all_partition_count=len(opts),
                               maximal_partition_count=len(maximal),
                               all_orbits=all_orbits,
                               maximal_orbits=sorted({m['orbit'] for m in maximal}),
                               upper_viable_maximal_partitions=viable))
        supported = bool(UPPER & (1 << i))
        count = 1
        for s in splits:
            count *= len(s['upper_viable_maximal_partitions'])
        if supported:
            assert count
            triple_count += count
        rows.append(dict(index=i, word=word, upper_accepted=supported,
                         maximal_triple_count=count, splits=splits))
    allowed = sum(1 << i for i, c in enumerate(case['column_masks']) if c & ~941 == 0)
    rounds = []
    while True:
        remove = [i for i in range(len(words)) if allowed & (1 << i)
                  and any(not any(o & ~allowed == 0 for o in s['maximal_orbits'])
                          for s in rows[i]['splits'])]
        if not remove:
            break
        rounds.append(dict(before=allowed, removed=remove))
        allowed &= ~sum(1 << i for i in remove)
    assert allowed == UPPER
    return dict(boundary_order=['a0','a1','y2','a2','a3','y4','a4'],
                color_frame=list(range(4)), pattern_order=words, rows=rows,
                maximal_screen_rounds=rounds, final_mask=allowed,
                final_count=allowed.bit_count(),
                partition_orbit_domination_checks=domination_checks,
                viable_triples_summed_over_upper=triple_count,
                conclusion='Maximal complementary partitions do not strengthen this screen; arbitrary one-row triples are simultaneously realizable, not the 55-row relation.',
                target_source_status='not triggered')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    path = HERE / 'maximal_certificate.json'
    if args.write:
        with path.open('x') as f:
            json.dump(result, f, sort_keys=True, separators=(',', ':'))
            f.write('\n')
    if args.check:
        assert json.loads(path.read_text()) == json.loads(json.dumps(result))
    print(json.dumps({k: result[k] for k in ('final_count', 'partition_orbit_domination_checks',
                     'viable_triples_summed_over_upper', 'target_source_status')}))


if __name__ == '__main__':
    main()
