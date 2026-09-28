#!/usr/bin/env python3
"""Replay adjacent tether pairs and external-path K5 exclusions.

The source table and the earlier 26 exclusions are immutable inputs. Controls
are extracted topology skeletons, not realizable degree/list source graphs.
Arbitrary path lengths and branch sizes are covered by the paper proof.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_single_spoke_two_two_minor import Q, U, connected, subsets, verify_minor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_single_spoke_two_two/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_single_spoke_two_two_minor/observations.json'
OUT = ROOT / 'artifacts/c5_single_spoke_two_two_external/observations.json'
TABLE = OUT.with_name('support_table.md')
STYLES = ('direct', 'separate_bridges', 'shared_cycle', 'shared_trunk')
RHO = (3, 2, 1, 0, 4)
PI = (1, 0, 2, 3)


def forced_pair(support, forbidden):
    if len(forbidden) != 2:
        return None
    needed = U - set(forbidden) if 3 in forbidden else set(forbidden)
    fibers = [[i for i in support if Q[i] == c] for c in sorted(needed)]
    if not all(len(fiber) == 1 for fiber in fibers):
        return None
    pair = sorted(fiber[0] for fiber in fibers)
    if (pair[1] - pair[0]) % 5 not in (1, 4):
        return None
    return pair


def support_audit():
    rows = []
    for forbidden in combinations(range(4), 2):
        needed = U - set(forbidden) if 3 in forbidden else set(forbidden)
        for support in subsets(range(5))[1:]:
            admissible = [t for t in subsets(support) if needed <= {Q[i] for i in t}]
            forced = set.intersection(*(set(t) for t in admissible)) if admissible else set()
            fibers = [[i for i in support if Q[i] == c] for c in sorted(needed)]
            expected = {a[0] for a in fibers if len(a) == 1} if admissible else set()
            assert forced == expected
            pair = forced_pair(support, forbidden)
            if pair is not None:
                assert admissible and all(set(pair) <= t for t in admissible)
            rows.append(dict(forbidden=forbidden, actual_support=sorted(support),
                             required_colors=sorted(needed), color_fibers=fibers,
                             admissible_local_supports=[sorted(t) for t in admissible],
                             forced_vertices=sorted(forced), adjacent_pair=pair))
    assert len(rows) == 186
    # Same color at b0 or b2 does not force either named attachment.
    assert forced_pair([0, 2, 3, 4], [2, 3]) is None
    return rows


def routes(spoke, other_support, pair):
    result = []
    if spoke not in pair:
        result.append(dict(mode='spoke', landing=spoke))
    result += [dict(mode='external_component', landing=h)
               for h in other_support if h not in pair]
    return result


def control(length, edge_index, styles, pair=(0, 4), spoke=0,
            landing=1, external_vertices=2):
    """One original cycle, two disjoint tether bags, and a named outside route."""
    assert length % 2 == 1 and 1 <= edge_index <= length
    assert len(pair) == 2 and (pair[1] - pair[0]) % 5 in (1, 4)
    assert landing not in pair
    assert external_vertices > 0 or landing == spoke
    edges = set()

    def edge(u, v):
        assert u != v
        edges.add(tuple(sorted((u, v))))

    for i in range(5):
        edge(f'b{i}', f'b{(i + 1) % 5}')
    edge('z', f'b{spoke}')
    path = [f'x{i}' for i in range(length + 1)]
    for u, v in zip(path, path[1:]):
        edge(u, v)
    edge('z', path[0])
    edge('z', path[-1])
    endpoints = path[edge_index - 1:edge_index + 1]
    bags, tethers = [], []
    for root, style in zip(endpoints, styles):
        a, b = [f'b{i}' for i in pair]
        if style == 'direct':
            tether_routes = [[root, a], [root, b]]
        elif style == 'shared_trunk':
            tether_routes = [[root, root + '_w', a], [root, root + '_w', b]]
        else:
            tether_routes = [[root, root + '_y', a], [root, root + '_w', b]]
            if style == 'shared_cycle':
                edge(root + '_y', root + '_w')
        bag = {root}
        for route in tether_routes:
            bag.update(route[:-1])
            for u, v in zip(route, route[1:]):
                edge(u, v)
        bags.append(bag)
        tethers.append(tether_routes)
    route = ['z'] + [f'e{i}' for i in range(external_vertices)] + [f'b{landing}']
    for u, v in zip(route, route[1:]):
        edge(u, v)
    complement = {f'b{i}' for i in range(5) if i not in pair}
    z_bag = (set(path) - set(endpoints)) | set(route) | complement
    bags += [z_bag, {f'b{pair[0]}'}, {f'b{pair[1]}'}]
    assert not (set(route[1:-1]) & (set(path) | bags[0] | bags[1]))
    assert connected(complement, edges)
    witnesses = verify_minor(edges, bags)
    return dict(length=length, edge_index=edge_index, styles=styles,
                pair=pair, spoke=spoke, landing=landing,
                external_vertices=external_vertices, external_route=route,
                edges=sorted(edges), branch_sets=[sorted(b) for b in bags],
                actual_tether_routes=tethers, adjacencies=witnesses)


def minor_controls():
    result = [control(length, i, styles) for length in (1, 3, 5, 7)
              for i in range(1, length + 1) for styles in product(STYLES, repeat=2)]
    for a in range(5):
        pair = tuple(sorted((a, (a + 1) % 5)))
        for spoke, landing, size in product(range(5), range(5), (1, 2, 5)):
            if landing not in pair:
                result.append(control(1, 1, ('shared_trunk', 'shared_cycle'),
                                      pair, spoke, landing, size))
        for spoke in range(5):
            if spoke not in pair:
                result.append(control(3, 2, ('separate_bridges', 'direct'),
                                      pair, spoke, spoke, 0))
    assert len(result) == 496
    return result


def negative_controls():
    base = control(1, 1, ('direct', 'direct'))
    edges = set(map(tuple, base['edges']))
    bags = list(map(set, base['branch_sets']))
    broken = [
        ('missing_external_first_edge', edges - {('e0', 'z')}, bags),
        ('missing_external_last_edge', edges - {('b1', 'e1')}, bags),
        ('missing_tether', edges - {('b0', 'x0')}, bags),
        ('missing_original_bridge', edges - {('x0', 'x1')}, bags),
        ('overlapping_branch_sets', edges, [bags[0] | {'e0'}] + bags[1:]),
    ]
    rejected = []
    for name, es, bs in broken:
        try:
            verify_minor(es, bs)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(f'negative control passed: {name}')
    # An external route landing on X or Y does not connect the complement arc.
    assert routes(0, [0, 4], [0, 4]) == []
    rejected.append('no_route_to_complement')
    return rejected


def witnesses(row):
    result = []
    for k, (support, forbidden) in enumerate(zip(row['supports'], row['bans'])):
        pair = forced_pair(support, forbidden)
        if pair is None:
            continue
        for route in routes(row['spoke'], row['supports'][1-k], pair):
            result.append(dict(component=k, ordered_contacts=row['ordered_contacts'][k],
                               forced_pair=pair, complement=sorted(set(range(5))-set(pair)),
                               external_component=1-k if route['mode']=='external_component' else None,
                               external_contact=(row['ordered_contacts'][1-k][0]
                                                 if route['mode']=='external_component' else None),
                               **route))
    return result


def refine_table():
    source = json.loads(SOURCE.read_text())
    previous = json.loads(PREVIOUS.read_text())
    assert previous['source_sha256'][str(SOURCE.relative_to(ROOT))] == sha256(SOURCE.read_bytes()).hexdigest()
    by_id = {r['id']: r for r in source['records']}
    earlier = {r['source_id'] for r in previous['table']['excluded']}
    incoming = set(previous['table']['remaining_source_ids'])
    assert len(earlier) == 26 and len(incoming) == 354 and not earlier & incoming
    assert earlier | incoming == {r['id'] for r in source['records'] if r['T4_status']=='retained'}
    assert all(e['original_record'] == by_id[e['source_id']] for e in previous['table']['excluded'])
    excluded, remaining, modes = [], [], Counter()
    for rid in sorted(incoming):
        row = by_id[rid]
        ws = witnesses(row)
        if not ws:
            remaining.append(row)
            continue
        # Check the inherited full-relation reflection at the exact named frame.
        reflected = row['reflection']
        for w in ws:
            k = w['component']
            assert sorted(RHO[i] for i in row['supports'][k]) == reflected['supports'][k]
            assert sorted(PI[c] for c in row['bans'][k]) == reflected['bans'][k]
            pair = forced_pair(reflected['supports'][k], reflected['bans'][k])
            assert pair == sorted(RHO[i] for i in w['forced_pair'])
            assert dict(mode=w['mode'], landing=RHO[w['landing']]) in routes(
                reflected['spoke'], reflected['supports'][1-k], pair)
        modes['+'.join(sorted({w['mode'] for w in ws}))] += 1
        excluded.append(dict(source_id=rid, original_record=row, witnesses=ws,
                             source_status='excluded_by_adjacent_pair_external_K5'))
    assert len(excluded) == 210 and len(remaining) == 144
    assert {104, 148} <= {r['source_id'] for r in excluded}
    for records, expected_types in ((remaining, 72),
                                   ([e['original_record'] for e in excluded], 105)):
        keys = {(r['spoke'], tuple(map(tuple, r['supports'])), tuple(map(tuple, r['bans'])))
                for r in records}
        assert len(keys) == len(records)
        for s, supports, bans in keys:
            assert (s, supports[::-1], bans[::-1]) in keys
            assert (supports, bans) != (supports[::-1], bans[::-1])
        assert len({min(key, (key[0], key[1][::-1], key[2][::-1]))
                    for key in keys}) == expected_types
    counts = Counter('/'.join(t['status'] for t in r['targets']) for r in remaining)
    removed_counts = Counter('/'.join(t['status'] for t in r['original_record']['targets']) for r in excluded)
    assert counts == {'accept/accept':54, 'accept/unresolved':30,
                      'unresolved/accept':42, 'unresolved/unresolved':18}
    assert removed_counts['accept/accept'] == 50
    assert modes == {'external_component':106, 'external_component+spoke':104}
    return dict(excluded=excluded, remaining_source_ids=[r['id'] for r in remaining],
                previous_excluded_source_ids=sorted(earlier), previous_remaining=354,
                newly_excluded_labeled=210, cumulative_excluded_labeled=236,
                remaining_labeled=144, remaining_component_swap_types=72,
                route_modes=dict(sorted(modes.items())),
                excluded_targets=dict(sorted(removed_counts.items())),
                remaining_targets=dict(sorted(counts.items())),
                excluded_by_spoke=dict(sorted(Counter(r['original_record']['spoke'] for r in excluded).items())),
                remaining_by_spoke=dict(sorted(Counter(r['spoke'] for r in remaining).items())))


def support_table(result):
    lines = ['# (2,2) 相鄰支援對與外部路徑排除表', '',
             '由 [checker](../../scripts/c5_single_spoke_two_two_external.py) 產生；',
             '任意大小證明與界線見 [報告](../../docs/c5_single_spoke_two_two_external.md)。', '',
             '210 筆新排除含交換分量名字；每筆僅顯示第一份充分 witness。',
             '完整來源 relation schemas、placements、反射及全部 witness 在 observations.json。', '',
             '| ID | s | S0 / S1 | F0 / F1 | 路徑分量 | 強迫框點 | 外部接合 |',
             '| ---: | ---: | --- | --- | ---: | --- | --- |']
    for entry in result['table']['excluded']:
        r, w = entry['original_record'], entry['witnesses'][0]
        fmt = lambda groups: ' / '.join(''.join(map(str, x)) for x in groups)
        route = 'spoke' if w['mode']=='spoke' else f"C{w['external_component']}"
        lines.append(f"| {r['id']} | {r['spoke']} | {fmt(r['supports'])} | {fmt(r['bans'])} | {w['component']} | {fmt([w['forced_pair']])} | {route} → b{w['landing']} |")
    lines += ['', '剩餘 144 筆／72 型；A/A 54、A/? 30、?/A 42、?/? 18。',
              '來源排除不新增延拓；原 104 筆 A/A 中 50 筆已排除、54 筆仍保留。', '']
    return '\n'.join(lines)


def build():
    paths = [SOURCE, PREVIOUS, Path(__file__),
             ROOT / 'scripts/c5_single_spoke_two_two_minor.py',
             ROOT / 'scripts/c5_single_spoke_two_two.py']
    return dict(scope='arbitrary-size paper exclusion; finite local and topology controls only',
                source_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in paths},
                support_rows=support_audit(), minor_controls=minor_controls(),
                negative_controls=negative_controls(), table=refine_table())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    table = support_table(result)
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
        assert TABLE.read_text() == table, 'support table differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
        TABLE.write_text(table)
    print(json.dumps(dict(support_rows=len(result['support_rows']),
                          minor_controls=len(result['minor_controls']),
                          negative_controls=len(result['negative_controls']),
                          newly_excluded=result['table']['newly_excluded_labeled'],
                          remaining=result['table']['remaining_labeled'],
                          remaining_targets=result['table']['remaining_targets']), sort_keys=True))


if __name__ == '__main__':
    main()
