#!/usr/bin/env python3
"""Complete collar transfer and sound necessary Kempe pruning, h <= 2."""
import argparse
from itertools import product, combinations
from functools import lru_cache
import json
from pathlib import Path


def norm(p):
    d = {}
    return tuple(d.setdefault(c, len(d)) for c in p)


@lru_cache(None)
def patterns(n):
    return tuple(sorted({norm(p) for p in product(range(4), repeat=n)
                         if all(p[i] != p[(i+1) % n] for i in range(n))}))


@lru_cache(None)
def partitions(xs):
    if not xs:
        return ((),)
    x, *rest = xs
    result = []
    for ps in partitions(tuple(rest)):
        result.append(((x,),) + ps)
        for j in range(len(ps)):
            result.append(ps[:j] + ((x,) + ps[j],) + ps[j+1:])
    return tuple(result)


def kempe_table(n):
    pats = patterns(n)
    index = {p: i for i, p in enumerate(pats)}
    splits = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
    table = []
    for p in pats:
        row = []
        for split in splits:
            side = {c: j for j, pair in enumerate(split) for c in pair}
            swap = {a: b for pair in split for a, b in (pair, pair[::-1])}
            opts = set()
            left = tuple(i for i in range(n) if side[p[i]] == 0)
            right = tuple(i for i in range(n) if side[p[i]] == 1)
            for lp in partitions(left):
                for rp in partitions(right):
                    blocks = lp + rp
                    owner = {v: i for i, block in enumerate(blocks) for v in block}
                    if any(owner[a] == owner[c] and owner[b] == owner[d]
                           and owner[a] != owner[b]
                           for a, b, c, d in combinations(range(n), 4)):
                        continue
                    if any(side[p[i]] == side[p[(i+1) % n]]
                           and owner[i] != owner[(i+1) % n] for i in range(n)):
                        continue
                    orbit = 0
                    for bits in range(1 << len(blocks)):
                        q = tuple(swap[c] if bits >> owner[i] & 1 else c
                                  for i, c in enumerate(p))
                        orbit |= 1 << index[norm(q)]
                    opts.add(orbit)
            assert opts
            row.append(sorted(opts))
        table.append(row)
    return table


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total+1):
        for rest in compositions(total-first, length-1):
            yield (first,) + rest


P5 = patterns(5)
I5 = {p: i for i, p in enumerate(P5)}
OUTER_ASSIGNMENTS = tuple(b for b in product(range(4), repeat=5)
                          if all(b[i] != b[(i+1) % 5] for i in range(5)))


def collar_supports(t):
    # Ordered ring: apex a0; extras at b1; apex a1; ... apex a4; extras at b0.
    result = []
    for i in range(5):
        result.append((i, (i+1) % 5))
        result.extend([((i+1) % 5,)] * t[(i+1) % 5])
    return result


def columns(t):
    supports = collar_supports(t)
    cols = []
    full_lifts = []
    for inner in patterns(len(supports)):
        mask = 0
        words = []
        for b in OUTER_ASSIGNMENTS:
            if all(all(inner[j] != b[i] for i in support)
                   for j, support in enumerate(supports)):
                mask |= 1 << I5[norm(b)]
                words.append(b)
        cols.append(mask)
        full_lifts.append(words)
    return cols, full_lifts


def prune(cols, table, target):
    allowed = sum(1 << i for i, c in enumerate(cols) if c & ~target == 0)
    initial = allowed
    rounds = []
    while True:
        removals = []
        for i in range(len(cols)):
            if not (allowed >> i & 1):
                continue
            bad_splits = [j for j, opts in enumerate(table[i])
                          if not any(orbit & ~allowed == 0 for orbit in opts)]
            if bad_splits:
                removals.append(dict(pattern_index=i, split_indices=bad_splits))
        if not removals:
            break
        rounds.append(dict(before=allowed, removals=removals))
        allowed &= ~sum(1 << r['pattern_index'] for r in removals)
    union = 0
    for i, c in enumerate(cols):
        if allowed >> i & 1:
            union |= c
    return dict(target=target, initial=initial, rounds=rounds, fixed_point=allowed,
                possible_outer_union=union, excluded=(union != target))


def build():
    tables = {n: kempe_table(n) for n in (5, 6, 7)}
    cases = []
    for h in range(3):
        for t in compositions(h, 5):
            cols, full_lifts = columns(t)
            checks = [prune(cols, tables[5+h], target) for target in (933, 941)]
            cases.append(dict(boundary_extras=t, inner_supports=collar_supports(t),
                              column_masks=cols, outer_lifts_for_each_named_inner_row=full_lifts,
                              targets=checks))
    payload = dict(
        boundary_order=list(range(5)), color_frame=list(range(4)),
        outer_pattern_order=P5,
        inner_pattern_orders={str(n): patterns(n) for n in (5,6,7)},
        complementary_splits=[[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]],
        kempe_obligations={str(n): tables[n] for n in (5,6,7)}, cases=cases,
        trust='Necessary Kempe screen on an arbitrary actual inner disk; abstract surviving masks are not source realizations.')
    survivors = [(c['boundary_extras'], r['target'], r['fixed_point'])
                 for c in cases for r in c['targets'] if not r['excluded']]
    assert survivors == [((0, 0, 1, 0, 1), 941, 755425272170557940120206052)]
    assert survivors[0][2].bit_count() == 55
    payload['target_source_status'] = 'not triggered'
    return payload


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    parser.add_argument('--certificate', type=Path,
                        default=Path(__file__).with_name('collar_certificate.json'))
    args = parser.parse_args()
    payload = build()
    if args.write:
        with args.certificate.open('x') as f:
            json.dump(payload, f, separators=(',', ':'), sort_keys=True)
            f.write('\n')
    else:
        assert json.loads(args.certificate.read_text()) == json.loads(json.dumps(payload)), 'certificate mismatch'
    cases = payload['cases']
    for h in range(3):
        group=[c for c in cases if sum(c['boundary_extras'])==h]
        for target in (933,941):
            sub=[(c['boundary_extras'], next(r for r in c['targets'] if r['target']==target)) for c in group]
            survivors=[dict(extras=t,initial=r['initial'].bit_count(),fixed_point=r['fixed_point'].bit_count(),outer=r['possible_outer_union']) for t,r in sub if not r['excluded']]
            print(json.dumps(dict(h=h,target=target,cases=len(group),excluded=sum(r['excluded'] for t,r in sub),survivors=survivors)))
    print(json.dumps(dict(status='PASS', target_source_status='not triggered')))

if __name__ == '__main__':
    main()
