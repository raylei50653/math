#!/usr/bin/env python3
"""Replay two-frame-arc K5 minors, source exclusions and target extensions.

The entire other original component belongs to Z.  One fixed partition must
work for every admissible path-bag support.  Controls are not source graphs.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_single_spoke_two_two_minor import Q, U, PERMS, connected, subsets, verify_minor
from c5_single_spoke_two_two_external import RHO, PI, STYLES
from c5_single_spoke_frame_arc import ROWS, FRAME_EDGES, admissible_supports
from c5_single_spoke_cross_row import (
    candidate_evidence, closes_target, joint_supports,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_single_spoke_two_two/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_single_spoke_cross_row/observations.json'
OUT = ROOT / 'artifacts/c5_single_spoke_two_arc/observations.json'
TABLE = OUT.with_name('support_table.md')
FRAME = frozenset(range(5))


def verify_partition(arcs):
    assert len(arcs) == 2
    x, y = map(set, arcs)
    assert not x & y and x | y == FRAME
    assert connected(x, FRAME_EDGES) and connected(y, FRAME_EDGES)
    assert any((a in x) != (b in x) for a, b in FRAME_EDGES)


PARTITIONS = tuple((x, FRAME - x) for x in subsets(FRAME)
                   if 0 in x and connected(x, FRAME_EDGES)
                   and connected(FRAME - x, FRAME_EDGES))
assert len(PARTITIONS) == 10  # Unordered connected bipartitions of C5.


def crossing(support, arcs):
    return all(set(support) & set(arc) for arc in arcs)


def fixed_partitions(family, external_support):
    # An empty family has a separate impossibility proof; no vacuous minor.
    if not family:
        return []
    return [arcs for arcs in PARTITIONS if crossing(external_support, arcs)
            and all(crossing(t, arcs) for t in family)]


@lru_cache(None)
def support_family(row, support, fq, fr):
    if len(fr) != 2:
        return None
    if row == Q:
        assert fq == fr
        return admissible_supports(row, support, fr)
    if len(fq) == 2:
        return joint_supports(Q, row, support, fq, fr)
    return admissible_supports(row, support, fr)


def evidence(record, row, bans):
    row = tuple(row)
    components, witnesses = [], []
    for k, support in enumerate(record['supports']):
        fq, fr = tuple(record['bans'][k]), tuple(bans[k])
        family = support_family(row, tuple(support), fq, fr)
        if family is None:
            continue
        local = admissible_supports(row, tuple(support), fr)
        mode = ('source_row_stabilizer' if row == Q else
                'joint_supports' if len(fq) == 2 else 'target_row_stabilizer')
        external = sorted({record['spoke']} | set(record['supports'][1-k]))
        components.append(dict(component=k, ordered_contacts=record['ordered_contacts'][k],
            source_forbidden=fq, target_forbidden=fr, support_mode=mode,
            target_only_supports=[sorted(t) for t in local],
            admissible_supports=[sorted(t) for t in family], external_support=external))
        if not family:
            witnesses.append(dict(kind='no_possible_path_bag', component=k))
            continue
        for arcs in fixed_partitions(family, external):
            verify_partition(arcs)
            attachments = []
            for arc in arcs:
                landing = min(set(external) & arc)
                attachments.append(dict(landing=landing,
                    mode='original_spoke' if landing == record['spoke'] else 'other_component'))
            witnesses.append(dict(kind='two_frame_arc_K5', component=k,
                ordered_contacts=record['ordered_contacts'][k],
                external_component=1-k, external_contacts=record['ordered_contacts'][1-k],
                support_mode=mode, frame_arcs=[sorted(a) for a in arcs],
                external_attachments=attachments,
                works_with_target_row_alone=all(crossing(t, arcs) for t in local),
                branch_set_recipe=dict(A=f'W_i in C{k}', A_prime=f'W_(i+1) in C{k}',
                    Z=f'(V(J_C{k}) minus x_i,x_(i+1)) union V(C{1-k})',
                    X=[f'b{i}' for i in sorted(arcs[0])],
                    Y=[f'b{i}' for i in sorted(arcs[1])])))
    return dict(component_constraints=components, witnesses=witnesses)


def reflection_audit(record, row, bans, ev):
    # Reflection relabels frame positions/colors, retaining the ordered ports.
    rr = dict(record['reflection'], ordered_contacts=record['ordered_contacts'])
    raw = tuple(PI[row[RHO[i]]] for i in range(5))
    moved = [tuple(sorted(PI[c] for c in f)) for f in bans]
    reflected = evidence(rr, raw, moved)
    by_component = {c['component']: c for c in reflected['component_constraints']}
    for c in ev['component_constraints']:
        rc = by_component[c['component']]
        for key in ('target_only_supports', 'admissible_supports'):
            assert {tuple(sorted(RHO[i] for i in t)) for t in c[key]} == set(map(tuple, rc[key]))
        assert sorted(RHO[i] for i in c['external_support']) == rc['external_support']
    for w in ev['witnesses']:
        if w['kind'] == 'no_possible_path_bag':
            assert w in reflected['witnesses']
            continue
        arcs = [{RHO[i] for i in a} for a in w['frame_arcs']]
        verify_partition(arcs)
        rc = by_component[w['component']]
        assert crossing(rc['external_support'], arcs)
        assert all(crossing(t, arcs) for t in rc['admissible_supports'])
        assert any(rw['kind'] == w['kind'] and rw['component'] == w['component']
                   and {frozenset(a) for a in rw['frame_arcs']} == set(map(frozenset, arcs))
                   for rw in reflected['witnesses'])
        for attachment, arc in zip(w['external_attachments'], arcs):
            landing = RHO[attachment['landing']]
            assert landing in arc
            if attachment['mode'] == 'original_spoke':
                assert landing == rr['spoke']
            else:
                assert landing in rr['supports'][w['external_component']]


def record17_audit():
    result = []
    for ti, row in enumerate(ROWS[1:]):
        rows = []
        for t in subsets(FRAME):
            # Direct 24-permutation check independent of joint_supports.
            local = all({p[c] for c in (2, 3)} == {2, 3}
                        for r in (Q, row) for p in PERMS
                        if all(p[r[i]] == r[i] for i in t))
            cross = all({p[c] for c in (2, 3)} == {2, 3}
                        for p in PERMS if all(row[i] == p[Q[i]] for i in t))
            accepted = local and cross
            expected = (1 in t and bool(t & {0, 2}) if ti == 0 else
                        0 in t and bool(t & {1, 3}))
            assert accepted == expected
            rows.append(dict(support=sorted(t), admissible=accepted))
        family = support_family(row, tuple(range(5)), (2, 3), (2, 3))
        assert {tuple(r['support']) for r in rows if r['admissible']} == {
            tuple(sorted(t)) for t in family}
        assert len(family) == 12
        arcs = [[0, 2, 3, 4], [1]] if ti == 0 else [[0], [1, 2, 3, 4]]
        assert all(crossing(t, arcs) for t in family) and crossing({0, 1}, arcs)
        assert set.intersection(*map(set, family)) == ({1} if ti == 0 else {0})
        if ti == 1:
            assert family == admissible_supports(row, tuple(range(5)), (2, 3))
        result.append(dict(row=row, examined_supports=rows, admissible_count=len(family), frame_arcs=arcs))
    return result


def partition_audit():
    # Independent edge-cut enumeration verifies completeness of PARTITIONS.
    cuts = set()
    for e1, e2 in combinations(FRAME_EDGES, 2):
        es = FRAME_EDGES - {e1, e2}
        side = {0}
        while True:
            more = side | {v for u, v in es if u in side} | {u for u, v in es if v in side}
            if more == side:
                break
            side = more
        cuts.add(frozenset(side))
    assert cuts == {x for x, _ in PARTITIONS}
    for arcs in PARTITIONS:
        verify_partition(arcs)
    nonempty = subsets(FRAME)[1:]
    families = [(t,) for t in nonempty] + list(combinations(nonempty, 2))
    # Direct quantifier evaluation versus intersection of partition masks.
    masks = {t: {i for i, arcs in enumerate(PARTITIONS) if crossing(t, arcs)} for t in nonempty}
    digest, count = sha256(), 0
    for external, family in product(nonempty, families):
        expected = masks[external].intersection(*(masks[t] for t in family))
        found = fixed_partitions(family, external)
        assert found == [a for i, a in enumerate(PARTITIONS) if i in expected]
        digest.update(json.dumps([sorted(external), [sorted(t) for t in family], sorted(expected)]).encode())
        count += 1
    assert count == 15376
    return dict(partitions=[[sorted(a) for a in arcs] for arcs in PARTITIONS],
                family_controls=count, results_sha256=digest.hexdigest())


def control(length, i, j, arcs, suppliers, spoke, other_support,
            styles=('direct', 'direct'), external_style='shared_trunk'):
    assert 0 <= i < j <= length
    verify_partition(arcs)
    assert crossing({spoke} | set(other_support), arcs)
    assert all(a in arcs[0] and b in arcs[1] for a, b in suppliers)
    edges = set()

    def edge(u, v):
        assert u != v
        edges.add(tuple(sorted((u, v))))

    for u, v in FRAME_EDGES:
        edge(f'b{u}', f'b{v}')
    path = [f'x{k}' for k in range(length + 1)]
    for u, v in zip(['z'] + path, path + ['z']):
        edge(u, v)
    edge('z', f'b{spoke}')
    bags, tethers = [], []
    for root, style, pair in zip((path[i], path[j]), styles, suppliers):
        a, b = [f'b{k}' for k in pair]
        if style == 'direct':
            paths = [[root, a], [root, b]]
        elif style == 'shared_trunk':
            paths = [[root, root+'_t', a], [root, root+'_t', b]]
        else:
            assert style in ('separate_bridges', 'shared_cycle')
            paths = [[root, root+'_a', a], [root, root+'_b', b]]
            if style == 'shared_cycle':
                edge(root+'_a', root+'_b')
        bag = {root}
        for route in paths:
            bag.update(route[:-1])
            for u, v in zip(route, route[1:]):
                edge(u, v)
        bags.append(bag)
        tethers.append(paths)
    # For nonadjacent choices absorb the intermediate path into A.
    bags[0].update(path[i:j])
    other = {'c0', 'c1'}
    edge('c0', 'c1')
    edge('z', 'c0')
    edge('z', 'c1')
    assert other_support
    external_paths = []
    for h in other_support:
        if external_style == 'shared_trunk':
            route = ['c0', 'ct0', 'ct1', f'b{h}']
        else:
            assert external_style == 'separate'
            route = ['c0', f'ct{h}', f'b{h}']
        other.update(route[:-1])
        for u, v in zip(route, route[1:]):
            edge(u, v)
        external_paths.append(route)
    bags += [set(['z'] + path[:i] + path[j+1:]) | other,
             {f'b{k}' for k in arcs[0]}, {f'b{k}' for k in arcs[1]}]
    adjacency = verify_minor(edges, bags)
    return dict(length=length, chosen_indices=[i, j], frame_arcs=[sorted(a) for a in arcs],
                suppliers=suppliers, spoke=spoke, other_support=sorted(other_support),
                styles=styles, external_style=external_style, other_component=sorted(other),
                original_contacts=['c0', 'c1'], edges=sorted(edges),
                branch_sets=[sorted(b) for b in bags], actual_tether_routes=tethers,
                external_paths=external_paths, adjacencies=adjacency)


def minor_controls():
    general = []
    for arcs in PARTITIONS:
        pairs = list(product(sorted(arcs[0]), sorted(arcs[1])))
        for a, b in pairs:
            for spoke, other in ((a, b), (b, a)):
                for suppliers in product(pairs, repeat=2):
                    general.append(control(1, 0, 1, arcs, suppliers, spoke, (other,)))
        for length in range(1, 6):
            for i, j in combinations(range(length + 1), 2):
                # Both external attachments can use shared internal vertices.
                general.append(control(length, i, j, arcs, (pairs[0], pairs[-1]),
                    pairs[0][0], pairs[0], ('shared_trunk', 'shared_cycle')))
    assert len(general) == 3150
    record17 = []
    choices = [(length, i, i+1) for length in (1, 3, 5) for i in range(length)] + [(5, 1, 4)]
    for ti, (arcs, pairs) in enumerate((
            ([[0, 2, 3, 4], [1]], [(0, 1), (2, 1)]),
            ([[0], [1, 2, 3, 4]], [(0, 1), (0, 3)]))):
        for (length, i, j), suppliers, styles, external_style in product(
                choices, product(pairs, repeat=2), product(STYLES, repeat=2), ('shared_trunk', 'separate')):
            record17.append(dict(target_index=ti, **control(length, i, j, arcs, suppliers,
                0, (0, 1), styles, external_style)))
    assert len(record17) == 2560
    return general, record17


def negative_controls():
    base = control(1, 0, 1, [[0, 2, 3, 4], [1]], ((0, 1), (2, 1)), 0, (1,))
    es, bs = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    broken = [
        ('missing_spoke', es - {('b0', 'z')}, bs),
        ('other_component_disconnected_from_z', es - {('c0', 'z'), ('c1', 'z')}, bs),
        ('missing_other_attachment', es - {('b1', 'ct1')}, bs),
        ('missing_tether', es - {('b1', 'x0')}, bs),
        ('missing_original_bridge', es - {('x0', 'x1')}, bs),
        ('missing_cycle_edge', es - {('x0', 'z')}, bs),
        ('disconnected_frame_arc', es - {('b3', 'b4')}, bs),
        ('missing_both_frame_cuts', es - {('b0', 'b1'), ('b1', 'b2')}, bs),
        ('overlapping_bags', es, [bs[0] | {'z'}] + bs[1:]),
        ('external_support_only_one_side', (es - {('b1', 'ct1')}) | {('b2', 'ct1')}, bs),
    ]
    long = control(5, 1, 4, [[0, 2, 3, 4], [1]], ((0, 1), (2, 1)), 0, (1,))
    lbs = list(map(set, long['branch_sets']))
    broken.append(('unabsorbed_intermediate_path', set(map(tuple, long['edges'])),
                   [lbs[0] - {'x2', 'x3'}] + lbs[1:]))
    result = []
    for name, edges, bags in broken:
        try:
            verify_minor(edges, bags)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(f'negative control passed: {name}')
    for name, arcs in [('disconnected_partition', [[0, 2], [1, 3, 4]]),
                       ('overlapping_partition', [[0, 1], [1, 2, 3, 4]]),
                       ('empty_partition', [[], list(range(5))])]:
        try:
            verify_partition(arcs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    family, external = [{0, 2}, {1, 2}], {0, 1}
    assert all(fixed_partitions([t], external) for t in family)
    assert not fixed_partitions(family, external)
    result.append('each_support_has_a_split_but_no_common_split')
    assert not fixed_partitions([], external)
    result.append('empty_family_does_not_certify_minor')
    assert support_family(ROWS[1], (0, 1, 2, 3, 4), (2, 3), (2,)) is None
    assert support_family(ROWS[1], (0, 1, 2, 3, 4), (2,), (2, 3)) == admissible_supports(
        ROWS[1], (0, 1, 2, 3, 4), (2, 3))
    result.append('singleton_target_skipped_source_singleton_uses_target_only')
    assert not closes_target([dict(eliminated=True), dict(eliminated=False)])
    assert not closes_target([])
    result.append('partial_or_empty_candidate_list_is_not_extension')
    return result


def refine_table():
    source, previous = [json.loads(p.read_text()) for p in (SOURCE, PREVIOUS)]
    for path, digest in previous['source_sha256'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest
    by_id = {r['id']: r for r in source['records']}
    old = previous['table']
    assert old['remaining_labeled'] == 108 and old['unresolved_queries'] == 50
    excluded, retained, new, removed_queries = [], [], [], []
    scanned, allcases = 0, []
    for entry in old['retained']:
        rid, r = entry['source_id'], entry['original_record']
        assert r == by_id[rid]
        source_ev = evidence(r, Q, r['bans'])
        reflection_audit(r, Q, r['bans'], source_ev)
        if source_ev['witnesses']:
            excluded.append(dict(source_id=rid, original_record=r,
                previous_targets=entry['targets'], source_evidence=source_ev))
            removed_queries += [[rid, i] for i, t in enumerate(entry['targets']) if t['status'] == 'unresolved']
            continue
        targets = []
        for ti, previous_target in enumerate(entry['targets']):
            row, cases = previous_target['row'], []
            assert r['reflection']['targets'][ti]['row'] == [PI[row[RHO[i]]] for i in range(5)]
            if previous_target['status'] == 'unresolved':
                scanned += 1
                original = r['targets'][ti]
                options = [c['forbidden_options'] for c in original['components']]
                rejecting = [[f0, f1] for f0, f1 in product(*options)
                             if U - {row[r['spoke']]} <= set(f0) | set(f1)]
                assert rejecting == original['rejection_options']
                assert rejecting == [c['forbidden_options'] for c in previous_target['rejection_cases']]
                for bans, oldcase in zip(rejecting, previous_target['rejection_cases']):
                    assert json.loads(json.dumps(candidate_evidence(r, row, bans))) == oldcase
                    ev = evidence(r, row, bans)
                    reflection_audit(r, row, bans, ev)
                    cases.append(dict(forbidden_options=bans, inherited_eliminated=oldcase['eliminated'],
                        two_arc_evidence=ev, eliminated=bool(oldcase['eliminated'] or ev['witnesses'])))
                if closes_target(cases):
                    new.append(dict(source_id=rid, target_index=ti, row=row))
            targets.append(dict(row=row, previous_status=previous_target['status'],
                previous_target=previous_target, rejection_cases=cases,
                status='accept' if closes_target(cases) else previous_target['status']))
            allcases.extend(cases)
        retained.append(dict(source_id=rid, original_record=r, source_evidence=source_ev, targets=targets))
    assert [e['source_id'] for e in excluded] == [174, 231, 965, 1233, 1332, 1417]
    assert scanned + len(removed_queries) == 50
    key = lambda r: (r['spoke'], tuple(map(tuple, r['supports'])), tuple(map(tuple, r['bans'])))
    keyed = {key(e['original_record']): e for e in retained + excluded}
    for (s, supports, bans), e in keyed.items():
        other = keyed[s, supports[::-1], bans[::-1]]
        assert ('targets' in e) == ('targets' in other)
        if 'targets' not in e:
            continue
        for a, b in zip(e['targets'], other['targets']):
            assert a['status'] == b['status']
            assert {tuple(map(tuple, c['forbidden_options'][::-1])): c['eliminated'] for c in a['rejection_cases']} == {
                tuple(map(tuple, c['forbidden_options'])): c['eliminated'] for c in b['rejection_cases']}
    assert {e['source_id'] for e in retained + excluded} == set(old['remaining_source_ids'])
    counts = Counter('/'.join(t['status'] for t in e['targets']) for e in retained)
    assert counts == {'accept/accept': 84, 'accept/unresolved': 8, 'unresolved/accept': 10}
    assert [(e['source_id'], e['target_index']) for e in new] == [
        (rid, ti) for rid in (17, 73, 82, 316, 317, 338, 433, 451, 828, 829) for ti in (0, 1)]
    audit = dict(rejection_cases=len(allcases), inherited_eliminated=sum(c['inherited_eliminated'] for c in allcases),
        newly_eliminated=sum(c['eliminated'] and not c['inherited_eliminated'] for c in allcases),
        remaining=sum(not c['eliminated'] for c in allcases))
    assert audit == dict(rejection_cases=166, inherited_eliminated=124, newly_eliminated=24, remaining=18)
    return dict(previous_excluded_source_ids=old['previous_excluded_source_ids'],
        newly_excluded_labeled=len(excluded), cumulative_excluded_labeled=272+len(excluded),
        excluded=excluded, remaining_labeled=len(retained), remaining_component_swap_types=len(retained)//2,
        remaining_source_ids=[e['source_id'] for e in retained], retained=retained,
        queries_removed_by_source_exclusion=removed_queries, scanned_unresolved_queries=scanned,
        newly_accepted=new, candidate_audit=audit, remaining_targets=dict(sorted(counts.items())),
        unresolved_queries=sum(t['status']=='unresolved' for e in retained for t in e['targets']),
        unresolved_records=sum(any(t['status']=='unresolved' for t in e['targets']) for e in retained))


def build():
    paths = [SOURCE, PREVIOUS, Path(__file__)] + [ROOT/'scripts'/name for name in (
        'c5_single_spoke_cross_row.py', 'c5_single_spoke_frame_arc.py',
        'c5_single_spoke_two_two_minor.py', 'c5_single_spoke_two_two_external.py')]
    general, record17 = minor_controls()
    return dict(scope='paper two-frame-arc minor with other original component in Z; finite controls, not realizations',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        record17_support=record17_audit(), partition_audit=partition_audit(),
        general_minor_controls=general, record17_minor_controls=record17,
        negative_controls=negative_controls(), table=refine_table())


def support_table(result):
    table = result['table']
    lines = ['# (2,2) two-frame-arc source exclusions and target extensions', '',
        'Generated by [checker](../../scripts/c5_single_spoke_two_arc.py);',
        'paper proof and trust boundary: [report](../../docs/c5_single_spoke_two_arc.md).', '',
        'A = proved extension; ? = unresolved. Retained sources are not realizations.',
        'Full original ordered relations and all previous target evidence remain in JSON.', '',
        'New source exclusions: ' + ', '.join(str(e['source_id']) for e in table['excluded']) + '.',
        'Their 12 unresolved queries are removed with the sources, not counted as extensions.', '',
        '| ID | p1 | p2 | newly proved | remaining rejection cases p1 / p2 |',
        '| ---: | --- | --- | --- | --- |']
    for e in table['retained']:
        ts = e['targets']
        labels = [{'accept':'A', 'unresolved':'?'}[t['status']] for t in ts]
        new = ', '.join(f'p{i+1}' for i, t in enumerate(ts) if t['status'] != t['previous_status'])
        cases = ' / '.join(str(sum(not c['eliminated'] for c in t['rejection_cases']))
                           if t['previous_status']=='unresolved' else 'inherited' for t in ts)
        lines.append(f"| {e['source_id']} | {labels[0]} | {labels[1]} | {new} | {cases} |")
    lines += ['', f"New extensions: {len(table['newly_accepted'])}; new source exclusions: {table['newly_excluded_labeled']}.",
        f"Remaining: {table['remaining_labeled']} sources / {table['remaining_component_swap_types']} swap types; "
        f"{table['unresolved_records']} unresolved records / {table['unresolved_queries']} queries.",
        f"Target counts: {json.dumps(table['remaining_targets'], sort_keys=True)}.", '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    fields = []
    for key, value in sorted(result.items()):
        if key.endswith('_controls') and key != 'negative_controls':
            encoded = '[\n' + ',\n'.join(json.dumps(v, sort_keys=True) for v in value) + '\n]'
        else:
            encoded = json.dumps(value, sort_keys=True, indent=2)
        fields.append(json.dumps(key) + ': ' + encoded)
    payload, table = '{\n' + ',\n'.join(fields) + '\n}\n', support_table(result)
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
        assert TABLE.read_text() == table, 'support table differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
        TABLE.write_text(table)
    print(json.dumps(dict(general_minor_controls=len(result['general_minor_controls']),
        record17_minor_controls=len(result['record17_minor_controls']),
        negative_controls=len(result['negative_controls']),
        new_source_exclusions=result['table']['newly_excluded_labeled'],
        new_target_extensions=len(result['table']['newly_accepted']),
        remaining_targets=result['table']['remaining_targets'], unresolved_queries=result['table']['unresolved_queries']),
        sort_keys=True))


if __name__ == '__main__':
    main()
