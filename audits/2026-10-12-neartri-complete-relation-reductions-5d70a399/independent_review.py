#!/usr/bin/env python3
"""Independent, read-only verification of the neartri relation certificates.

No production checker is imported. Only an explicit --report is written,
using exclusive creation. Certificate hashes identify the compared evidence.
"""
import argparse
import hashlib
import itertools as it
import json
from functools import lru_cache
from pathlib import Path


DEFAULT_AUDIT = Path(__file__).resolve().parent
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
PERMS = tuple(it.permutations(range(4)))


def normalize(word):
    palette = tuple(dict.fromkeys(word))
    return tuple(palette.index(c) for c in word)


def rgs(n, limit=None):
    """All set partitions encoded by restricted-growth strings."""
    def extend(prefix):
        if len(prefix) == n:
            yield tuple(prefix)
            return
        choices = max(prefix, default=-1) + 2
        if limit is not None:
            choices = min(choices, limit)
        for color in range(choices):
            yield from extend(prefix + [color])
    yield from extend([])


def proper(word):
    return all(a != b for a, b in zip(word, word[1:] + word[:1]))


@lru_cache(None)
def patterns(n):
    return tuple(p for p in rgs(n, 4) if proper(p))


def full_orbit(word):
    return {tuple(perm[c] for c in word) for perm in PERMS}


@lru_cache(None)
def noncrossing_partitions(n):
    return tuple(part for part in rgs(n)
                 if not any(part[a] == part[c] and part[b] == part[d]
                            and part[a] != part[b]
                            for a, b, c, d in it.combinations(range(n), 4)))


def kempe_table(n):
    """Generate all NC partitions first, then filter by actual colour sides."""
    pats = patterns(n)
    index = {p: i for i, p in enumerate(pats)}
    table = []
    for word in pats:
        row = []
        for split in SPLITS:
            sides = tuple(int(c in split[1]) for c in word)
            swap = dict(x for pair in split for x in (pair, pair[::-1]))
            options = set()
            for part in noncrossing_partitions(n):
                if any(part[i] == part[j] and sides[i] != sides[j]
                       for i in range(n) for j in range(i)):
                    continue
                if any(sides[i] == sides[(i + 1) % n]
                       and part[i] != part[(i + 1) % n] for i in range(n)):
                    continue
                orbit = 0
                for flips in it.product((False, True), repeat=1 + max(part)):
                    q = tuple(swap[c] if flips[part[i]] else c
                              for i, c in enumerate(word))
                    assert proper(q)
                    orbit |= 1 << index[normalize(q)]
                options.add(orbit)
            assert options
            row.append(sorted(options))
        table.append(row)
    return table


def mask_words(mask, n):
    return set().union(*(full_orbit(p) for i, p in enumerate(patterns(n))
                         if mask >> i & 1))


def check_crosscuts(cert, known):
    p5 = patterns(5)
    index = {p: i for i, p in enumerate(p5)}
    short_words = {m: mask_words(m, 4) for m in cert['c4_screen']['necessary']}
    long_words = {m: mask_words(m, 5) for m in known}
    for record in cert['crosscut_joins']:
        a, b = record['short_mask'], record['long_mask']
        actual = 0
        for short in short_words[a]:
            for long in long_words[b]:
                if (short[2], short[0], short[3]) != (long[0], long[3], long[4]):
                    continue
                outer = (long[1], long[2], short[0], short[1], short[2])
                actual |= 1 << index[normalize(outer)]
        assert actual == record['result'] and actual in known, (a, b)
        # Also compare each named shared-vertex fibre, including all empties.
        for p, recorded in zip(p5, record['fibres']):
            short = {c for c in range(4) if (p[2], p[3], p[4], c) in short_words[a]}
            long = {c for c in range(4) if (p[4], p[0], p[1], p[2], c) in long_words[b]}
            assert recorded == dict(short=sorted(short), long=sorted(long), joint=sorted(short & long))
    assert len(cert['crosscut_joins']) == 924
    return len(cert['crosscut_joins'])


def check_ring(cert):
    allowed = [0] * 10
    for j, inner in enumerate(patterns(5)):
        for word in full_orbit(inner):
            for i, outer in enumerate(patterns(5)):
                if all(outer[t] not in (word[t], word[(t - 1) % 5]) for t in range(5)):
                    allowed[i] |= 1 << j
    assert allowed == cert['ring_allowed_masks']
    return allowed


def reverse_columns(supports):
    """Fix canonical outer rows; enumerate literal inner words and transport
    both together to a canonical inner row.  This recovers full outer lifts,
    including unused-colour permutations, as well as their column masks.
    """
    n = len(supports)
    inner_index = {p: i for i, p in enumerate(patterns(n))}
    columns = [0] * len(inner_index)
    lifts = [set() for _ in inner_index]
    for word in it.product(range(4), repeat=n):
        if not proper(word):
            continue
        q = normalize(word)
        k = inner_index[q]
        used = tuple(dict.fromkeys(word))
        rename = dict(zip(used, range(len(used))))
        unused = tuple(c for c in range(4) if c not in rename)
        maps = [rename | dict(zip(unused, rest))
                for rest in it.permutations(range(len(used), 4))]
        for j, outer in enumerate(patterns(5)):
            if all(word[i] not in {outer[b] for b in adj} for i, adj in enumerate(supports)):
                columns[k] |= 1 << j
                for mapping in maps:
                    lifts[k].add(tuple(mapping[c] for c in outer))
    return columns, [sorted(words) for words in lifts]


def unpack(mask, size):
    return frozenset(i for i in range(size) if mask >> i & 1)


def asynchronous_prune(columns, table, target):
    size = len(columns)
    keep = {i for i, c in enumerate(columns) if c | target == target}
    options = [[list(map(lambda o: unpack(o, size), opts)) for opts in row]
               for row in table]
    changed = True
    while changed:
        changed = False
        for i in sorted(keep):
            if any(not any(orbit <= keep for orbit in opts) for opts in options[i]):
                keep.remove(i)
                changed = True
    return keep


def review(audit):
    source_paths = [audit / 'certificate.json', audit / 'collar_certificate.json']
    frozen_path = audit / 'frozen/artifacts/c5_cells/cells.json'
    hashes_before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in source_paths + [frozen_path]}
    cert, collar = [json.loads(p.read_text()) for p in source_paths]
    known = set(map(int, json.loads(frozen_path.read_text())['cells']))
    assert len(known) == 132
    assert cert['pattern_order'] == [list(p) for p in patterns(5)]
    assert collar['outer_pattern_order'] == cert['pattern_order']
    c4table = kempe_table(4)
    assert c4table == cert['c4_screen']['obligations']
    count = check_crosscuts(cert, known)
    print(f'PASS: {count} full-S4 crosscut joins and 9240 named fibres')
    ring = check_ring(cert)
    print(f'PASS: independently reconstructed S4 annular row masks {ring}')
    tables = {}
    for n in (5, 6, 7):
        assert collar['inner_pattern_orders'][str(n)] == [list(p) for p in patterns(n)]
        tables[n] = kempe_table(n)
        assert tables[n] == collar['kempe_obligations'][str(n)]
        print(f'PASS: independent RGS noncrossing Kempe table C{n}, {len(patterns(n))} rows')
    summaries = []
    cases = collar['cases']
    assert len(cases) == 21
    for case in cases:
        t = case['boundary_extras']
        expected_supports = []
        for i in range(5):
            expected_supports.append([i, (i + 1) % 5])
            expected_supports.extend([[(i + 1) % 5]] * t[(i + 1) % 5])
        assert expected_supports == case['inner_supports']
        columns, lifts = reverse_columns(expected_supports)
        assert columns == case['column_masks'], t
        assert [[list(word) for word in words] for words in lifts] == case['outer_lifts_for_each_named_inner_row'], t
        table = tables[5 + sum(t)]
        for result in case['targets']:
            target = result['target']
            initial = sum(1 << i for i, c in enumerate(columns) if c | target == target)
            assert initial == result['initial']
            current = initial
            for recorded_round in result['rounds']:
                assert current == recorded_round['before']
                removals = []
                for i in unpack(current, len(columns)):
                    bad = [j for j, opts in enumerate(table[i])
                           if not any(unpack(orbit, len(columns)) <= unpack(current, len(columns)) for orbit in opts)]
                    if bad:
                        removals.append(dict(pattern_index=i, split_indices=bad))
                assert sorted(removals, key=lambda r: r['pattern_index']) == recorded_round['removals']
                current &= ~sum(1 << r['pattern_index'] for r in removals)
            keep = asynchronous_prune(columns, table, target)
            fixed = sum(1 << i for i in keep)
            assert fixed == current == result['fixed_point']
            outer_union = 0
            for i in keep:
                outer_union |= columns[i]
            assert outer_union == result['possible_outer_union']
            assert result['excluded'] == (outer_union != target)
            summaries.append(dict(boundary_extras=t, target=target,
                                  fixed_point_size=len(keep), outer_union=outer_union,
                                  excluded=result['excluded']))
    print('PASS: all 21 reverse-direction literal-colour column tables and full outer lifts')
    print('PASS: all 42 asynchronous set-based fixed points and synchronous removal certificates')
    survivors = [r for r in summaries if not r['excluded']]
    assert survivors == [dict(boundary_extras=[0, 0, 1, 0, 1], target=941,
                             fixed_point_size=55, outer_union=941, excluded=False)]
    print('PASS: sole necessary-condition survivor ' + json.dumps(survivors[0], sort_keys=True))
    hashes_after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in source_paths + [frozen_path]}
    assert hashes_before == hashes_after, 'Inputs changed during the read-only review'
    return dict(status='PASS', input_sha256=hashes_before, production_code_imported=False,
                input_mutations=False, independent_crosscut_joins=count,
                independent_named_crosscut_fibres=count * 10,
                independent_ring_masks=ring, independently_generated_kempe_tables=[4, 5, 6, 7],
                reverse_column_cases=len(cases), asynchronous_fixed_points=len(summaries),
                cases=summaries, survivors=survivors,
                trust='Finite evidence review only. Universal disk topology and necessary-screen soundness are paper arguments; survivors are not source realizations.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit', type=Path, default=DEFAULT_AUDIT)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = review(args.audit)
    if args.report:
        with args.report.open('x') as f:
            json.dump(result, f, indent=2, sort_keys=True)
            f.write('\n')
        print('Report: ' + str(args.report))


if __name__ == '__main__':
    main()
