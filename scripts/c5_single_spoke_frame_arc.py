#!/usr/bin/env python3
"""Replay frame-arc K5 controls and separate source/target table refinements.

No graph enumeration or claim of palette-certificate existence from controls.
The arbitrary-size argument and its external theorem boundary are in the report.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_single_spoke_two_two_minor import (
    Q, U, PERMS, connected, residual_audit, subsets, verify_minor,
)
from c5_single_spoke_two_two_external import RHO, PI, STYLES, routes

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_single_spoke_two_two/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_single_spoke_two_two_external/observations.json'
OUT = ROOT / 'artifacts/c5_single_spoke_frame_arc/observations.json'
TABLE = OUT.with_name('support_table.md')
ROWS = (Q, (0, 1, 0, 2, 1), (0, 1, 2, 1, 2))
FRAME_EDGES = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}


def verify_arcs(anchors, arcs):
    assert len(set(anchors)) == 3 and set(anchors) <= set(range(5))
    assert len(arcs) == 3
    used = set()
    for anchor, arc in zip(anchors, arcs):
        assert anchor in arc and not used & set(arc)
        assert connected(set(arc), FRAME_EDGES)
        used.update(arc)
    assert used == set(range(5))
    for i, j in combinations(range(3), 2):
        assert any((u in arcs[i] and v in arcs[j]) or
                   (v in arcs[i] and u in arcs[j]) for u, v in FRAME_EDGES)


def frame_arcs(a, b, h):
    """Partition the oriented frame at its three marked vertices."""
    anchors = (a, b, h)
    assert len(set(anchors)) == 3 and set(anchors) <= set(range(5))
    arcs = []
    for start in anchors:
        arc = [start]
        nxt = (start + 1) % 5
        while nxt not in anchors:
            arc.append(nxt)
            nxt = (nxt + 1) % 5
        arcs.append(sorted(arc))
    verify_arcs(anchors, arcs)
    return arcs


@lru_cache(None)
def admissible_supports(row, support, forbidden):
    f = set(forbidden)
    return tuple(t for t in subsets(support) if all(
        {p[c] for c in f} == f for p in PERMS
        if all(p[row[i]] == row[i] for i in t)))


def forced_pairs(row, support, forbidden):
    if len(forbidden) != 2:
        return []
    allowed = admissible_supports(tuple(row), tuple(support), tuple(forbidden))
    assert allowed, 'whole-support stabilizer already contradicts this pair'
    forced = set.intersection(*(set(t) for t in allowed))
    return list(combinations(sorted(forced), 2))


def support_audit():
    result = []
    for row, f, support in product(ROWS, combinations(range(4), 2), subsets(range(5))):
        seen = {row[i] for i in support}
        violating = [p for p in PERMS if all(p[c] == c for c in seen)
                     and {p[c] for c in f} != set(f)]
        needed = U - set(f) if 3 in f else set(f)
        assert (not violating) == (needed <= seen)
        result.append(dict(row=row, forbidden=f, local_support=sorted(support),
                           required_colors=sorted(needed), invariant=not violating,
                           violating_permutation=violating[0] if violating else None))
    assert len(result) == 576
    # Target-row specialization is recomputed, never a renamed q row.
    qsets = admissible_supports(ROWS[0], (0, 2, 3, 4), (2, 3))
    psets = admissible_supports(ROWS[2], (0, 2, 3, 4), (2, 3))
    assert set.intersection(*map(set, qsets)) == {3}
    assert set.intersection(*map(set, psets)) == {0, 3}
    return result


def control(length, i, j, pair, landing, styles, external_vertices=2, arcs=None):
    """Two possibly nonconsecutive bags on an original bridge path."""
    assert 0 <= i < j <= length and external_vertices >= 0
    arcs = frame_arcs(*pair, landing) if arcs is None else arcs
    verify_arcs((*pair, landing), arcs)
    edges = set()

    def edge(u, v):
        assert u != v
        edges.add(tuple(sorted((u, v))))

    for u, v in FRAME_EDGES:
        edge(f'b{u}', f'b{v}')
    path = [f'x{k}' for k in range(length + 1)]
    for u, v in zip(['z'] + path, path + ['z']):
        edge(u, v)
    bags, tethers = [], []
    for root, style in zip((path[i], path[j]), styles):
        a, b = [f'b{k}' for k in pair]
        if style == 'direct':
            tether_routes = [[root, a], [root, b]]
        elif style == 'shared_trunk':
            tether_routes = [[root, root + '_w', a], [root, root + '_w', b]]
        else:
            assert style in ('separate_bridges', 'shared_cycle')
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
    # Absorb the intermediate path into A; Z uses the other arc through z.
    bags[0].update(path[i:j])
    route = ['z'] + [f'e{k}' for k in range(external_vertices)] + [f'b{landing}']
    for u, v in zip(route, route[1:]):
        edge(u, v)
    xarc, yarc, harc = [{f'b{k}' for k in arc} for arc in arcs]
    bags += [set(path[:i] + path[j + 1:] + route) | harc, xarc, yarc]
    adjacency = verify_minor(edges, bags)
    return dict(length=length, chosen_indices=[i, j], pair=pair, landing=landing,
                styles=styles, frame_arcs=arcs, external_route=route,
                edges=sorted(edges), branch_sets=[sorted(b) for b in bags],
                actual_tether_routes=tethers, adjacencies=adjacency)


def minor_controls():
    # All ordered frame marks, all bag positions, both even and odd lengths.
    result = [control(length, i, j, (a, b), h, ('direct', 'direct'))
              for a, b, h in permutations(range(5), 3)
              for length in range(1, 6)
              for i, j in combinations(range(length + 1), 2)]
    # Branches may share their own internal vertices; the two bags are disjoint.
    result += [control(5, 1, 4, (a, b), h, styles, size)
               for a, b, h in permutations(range(5), 3)
               for styles in product(STYLES, repeat=2) for size in (0, 1, 4)]
    assert len(result) == 4980
    return result


def negative_controls():
    base = control(1, 0, 1, (0, 3), 1, ('direct', 'direct'),
                   arcs=[[0, 4], [3], [1, 2]])
    edges = set(map(tuple, base['edges']))
    bags = list(map(set, base['branch_sets']))
    broken = [
        ('missing_external_first_edge', edges - {('e0', 'z')}, bags),
        ('missing_external_last_edge', edges - {('b1', 'e1')}, bags),
        ('missing_tether', edges - {('b0', 'x0')}, bags),
        ('missing_original_bridge', edges - {('x0', 'x1')}, bags),
        ('missing_frame_arc_connection', edges - {('b0', 'b4')}, bags),
        ('missing_frame_adjacency', edges - {('b3', 'b4')}, bags),
        ('overlapping_bags', edges, [bags[0] | {'e0'}] + bags[1:]),
        ('disconnected_old_complement', edges,
         [bags[0], bags[1], {'z', 'e0', 'e1', 'b1', 'b2', 'b4'}, {'b0'}, {'b3'}]),
    ]
    result = []
    for name, es, bs in broken:
        try:
            verify_minor(es, bs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(f'negative control passed: {name}')
    for name, action in [
        ('landing_on_tether', lambda: frame_arcs(0, 3, 0)),
        ('unabsorbed_intermediate_path', lambda: verify_minor(
            set(map(tuple, gap['edges'])),
            [set(gap['branch_sets'][0]) - {'x1'}] + list(map(set, gap['branch_sets'][1:])))),
    ]:
        gap = control(3, 0, 2, (0, 3), 1, ('direct', 'direct'))
        try:
            action()
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(f'negative control passed: {name}')
    assert routes(0, [0, 3], [0, 3]) == []
    result.append('no_external_landing')
    return result


def witnesses(record, row, bans):
    result = []
    for k, (support, forbidden) in enumerate(zip(record['supports'], bans)):
        for pair in forced_pairs(row, support, forbidden):
            for route in routes(record['spoke'], record['supports'][1-k], pair):
                arcs = frame_arcs(*pair, route['landing'])
                result.append(dict(component=k, ordered_contacts=record['ordered_contacts'][k],
                    forbidden=forbidden, forced_pair=pair,
                    frame_arcs=dict(X=arcs[0], Y=arcs[1], Z_frame=arcs[2]),
                    branch_set_recipe=dict(
                        A=f'W_i in C{k}', A_prime=f'W_(i+1) in C{k}',
                        Z=f'(V(J_C{k}) minus x_i,x_(i+1)) union V(L) union Z_frame',
                        X=[f'b{i}' for i in arcs[0]], Y=[f'b{i}' for i in arcs[1]]),
                    external_component=1-k if route['mode']=='external_component' else None,
                    external_contact=(record['ordered_contacts'][1-k][0]
                                      if route['mode']=='external_component' else None), **route))
    return result


def check_reflection(record, row, bans, ws):
    rr = record['reflection']
    raw = tuple(PI[row[RHO[i]]] for i in range(5))
    moved = [sorted(PI[c] for c in f) for f in bans]
    for w in ws:
        k = w['component']
        pair = tuple(RHO[i] for i in w['forced_pair'])
        assert tuple(sorted(pair)) in forced_pairs(raw, rr['supports'][k], moved[k])
        assert dict(mode=w['mode'], landing=RHO[w['landing']]) in routes(
            rr['spoke'], rr['supports'][1-k], pair)
        arcs = [[RHO[i] for i in w['frame_arcs'][key]] for key in ('X', 'Y', 'Z_frame')]
        verify_arcs((*pair, RHO[w['landing']]), arcs)


def refine_table():
    source, previous = [json.loads(p.read_text()) for p in (SOURCE, PREVIOUS)]
    assert previous['source_sha256'][str(SOURCE.relative_to(ROOT))] == sha256(SOURCE.read_bytes()).hexdigest()
    by_id = {r['id']: r for r in source['records']}
    incoming = set(previous['table']['remaining_source_ids'])
    earlier = set(previous['table']['previous_excluded_source_ids'])
    earlier.update(e['source_id'] for e in previous['table']['excluded'])
    assert len(incoming) == 144 and len(earlier) == 236 and not incoming & earlier
    assert incoming | earlier == {r['id'] for r in source['records'] if r['T4_status']=='retained'}
    assert all(e['original_record'] == by_id[e['source_id']] for e in previous['table']['excluded'])
    excluded, retained, newly_accepted = [], [], []
    for rid in sorted(incoming):
        r = by_id[rid]
        ws = witnesses(r, Q, r['bans'])
        check_reflection(r, Q, r['bans'], ws)
        if ws:
            excluded.append(dict(source_id=rid, original_record=r, witnesses=ws,
                                 source_status='excluded_by_q_frame_arc_K5'))
            continue
        targets = []
        for ti, target in enumerate(r['targets']):
            row = target['row']
            available = U - {row[r['spoke']]}
            opts = [c['forbidden_options'] for c in target['components']]
            rejecting = [[f0, f1] for f0, f1 in product(*opts)
                         if available <= set(f0) | set(f1)]
            assert rejecting == target['rejection_options']
            assert r['reflection']['targets'][ti]['row'] == [PI[row[RHO[i]]] for i in range(5)]
            cases = []
            for bans in rejecting:
                cws = witnesses(r, row, bans)
                check_reflection(r, row, bans, cws)
                cases.append(dict(forbidden_options=bans, witnesses=cws))
            closed = target['status']=='unresolved' and bool(cases) and all(c['witnesses'] for c in cases)
            if closed:
                newly_accepted.append(dict(source_id=rid, target_index=ti, row=row))
            targets.append(dict(row=row, previous_status=target['status'],
                                status='accept' if closed else target['status'],
                                rejection_cases=cases,
                                justification='all_rejection_options_have_frame_arc_K5' if closed else 'inherited'))
        retained.append(dict(source_id=rid, original_record=r, targets=targets))
    # Keep complete records intact, and audit the component-name involution.
    key = lambda r: (r['spoke'], tuple(map(tuple, r['supports'])), tuple(map(tuple, r['bans'])))
    statuses = {key(e['original_record']): [t['status'] for t in e['targets']] for e in retained}
    for (s, supports, bans), value in statuses.items():
        assert statuses[s, supports[::-1], bans[::-1]] == value
    excluded_keys = {key(e['original_record']) for e in excluded}
    assert all((s, supports[::-1], bans[::-1]) in excluded_keys for s, supports, bans in excluded_keys)
    counts = Counter('/'.join(t['status'] for t in e['targets']) for e in retained)
    assert len(excluded)==36 and len(retained)==108 and len(newly_accepted)==18
    assert counts == {'accept/accept':58, 'accept/unresolved':12,
                      'unresolved/accept':22, 'unresolved/unresolved':16}
    r15 = next(e for e in retained if e['source_id']==15)
    assert [t['status'] for t in r15['targets']] == ['accept', 'accept']
    assert r15['targets'][1]['rejection_cases'][0]['forbidden_options'] == [[1], [2, 3]]
    return dict(previous_excluded_source_ids=sorted(earlier), previous_remaining=144,
                excluded=excluded, retained=retained,
                newly_excluded_labeled=len(excluded), cumulative_excluded_labeled=len(earlier)+len(excluded),
                remaining_source_ids=[e['source_id'] for e in retained], remaining_labeled=len(retained),
                remaining_component_swap_types=len(statuses)//2, newly_accepted=newly_accepted,
                remaining_targets=dict(sorted(counts.items())),
                excluded_targets=dict(sorted(Counter('/'.join(t['status'] for t in e['original_record']['targets'])
                                                       for e in excluded).items())),
                unresolved_queries=sum(t['status']=='unresolved' for e in retained for t in e['targets']),
                unresolved_records=sum(any(t['status']=='unresolved' for t in e['targets']) for e in retained))


def build():
    paths = [SOURCE, PREVIOUS, Path(__file__),
             ROOT / 'scripts/c5_single_spoke_two_two_minor.py',
             ROOT / 'scripts/c5_single_spoke_two_two_external.py']
    return dict(scope='paper frame-arc minor; finite controls; separate source exclusion and target acceptance',
                source_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in paths},
                residual_rows=residual_audit(), support_rows=support_audit(),
                minor_controls=minor_controls(), negative_controls=negative_controls(),
                record15_named_control=control(1, 0, 1, (0, 3), 1, ('direct', 'direct'),
                                               arcs=[[0, 4], [3], [1, 2]]),
                table=refine_table())


def support_table(result):
    table = result['table']
    lines = ['# (2,2) frame-arc source exclusions and target extensions', '',
             'Generated by [checker](../../scripts/c5_single_spoke_frame_arc.py);',
             'arbitrary-size proof and trust boundary: [report](../../docs/c5_single_spoke_frame_arc.md).', '',
             '## New source exclusions (36 labeled records)', '',
             '| ID | component | forced frame pair | landing | X / Y / Z frame arcs |',
             '| ---: | ---: | --- | ---: | --- |']
    for e in table['excluded']:
        w = e['witnesses'][0]
        arcs = ' / '.join(''.join(map(str, w['frame_arcs'][k])) for k in ('X', 'Y', 'Z_frame'))
        lines.append(f"| {e['source_id']} | {w['component']} | {w['forced_pair']} | {w['landing']} | {arcs} |")
    lines += ['', '## Retained sources (108 labeled records, 54 swap types)', '',
              'A = proved extension, ? = unresolved; a retained source is not a realization.',
              'Full original relations, contacts, placements, reflection and target cases remain in JSON.', '',
              '| ID | p1 | p2 | newly proved |', '| ---: | --- | --- | --- |']
    for e in table['retained']:
        ts = e['targets']
        labels = [{'accept':'A', 'unresolved':'?'}[t['status']] for t in ts]
        new = ', '.join(f'p{i+1}' for i,t in enumerate(ts) if t['status'] != t['previous_status'])
        lines.append(f"| {e['source_id']} | {labels[0]} | {labels[1]} | {new} |")
    lines += ['', 'A/A 58; A/? 12; ?/A 22; ?/? 16. There are 50 unresolved records and 66 queries.',
              '36 source exclusions and 18 new target extensions are counted separately.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    # One complete skeleton per line keeps thousands of explicit witnesses
    # reviewable without a million-line artifact; the file is ordinary JSON.
    fields = []
    for key, value in sorted(result.items()):
        if key == 'minor_controls':
            encoded = '[\n' + ',\n'.join(json.dumps(v, sort_keys=True) for v in value) + '\n]'
        else:
            encoded = json.dumps(value, sort_keys=True, indent=2)
        fields.append(json.dumps(key) + ': ' + encoded)
    payload = '{\n' + ',\n'.join(fields) + '\n}\n'
    table = support_table(result)
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
        assert TABLE.read_text() == table, 'support table differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
        TABLE.write_text(table)
    print(json.dumps(dict(minor_controls=len(result['minor_controls']),
                         support_rows=len(result['support_rows']), negative_controls=result['negative_controls'],
                         newly_excluded=result['table']['newly_excluded_labeled'],
                         newly_accepted=len(result['table']['newly_accepted']),
                         remaining=result['table']['remaining_labeled'],
                         remaining_targets=result['table']['remaining_targets']), sort_keys=True))


if __name__ == '__main__':
    main()
