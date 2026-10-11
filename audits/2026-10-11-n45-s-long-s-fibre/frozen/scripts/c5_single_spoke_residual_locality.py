#!/usr/bin/env python3
"""Close record 90 by locality of the first two source residuals.

Equality concerns E, not the component forbidden set F.  The first-bridge
certificate supplies E and the paper rooted-block induction supplies locality.
Controls are not source realizations or a Lean proof.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_single_spoke_two_two_minor import Q, U, PERMS, subsets, verify_minor
from c5_single_spoke_two_two_external import RHO, PI, STYLES, routes
from c5_single_spoke_frame_arc import ROWS, control, frame_arcs, verify_arcs
from c5_single_spoke_cross_row import closes_target, joint_supports
from c5_single_spoke_first_bridge import evidence as first_evidence

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_single_spoke_two_two/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_single_spoke_first_bridge/observations.json'
OUT = ROOT / 'artifacts/c5_single_spoke_residual_locality/observations.json'
TABLE = OUT.with_name('support_table.md')


def compatible(q, row, support, source_residual, target_residual):
    # Only a necessary condition. Different local rows add no restriction.
    return (any(q[i] != row[i] for i in support)
            or set(source_residual) == set(target_residual))


def evidence(record, row, bans):
    old = first_evidence(record, row, bans)
    components = []
    for component in old['components']:
        if not component['applicable'] or not component['beta_cases']:
            continue
        k, cases = component['component'], []
        for bc in component['beta_cases']:
            eq, er = bc['common_source_residual'], bans[k]
            original = bc['first_two_bag_supports']
            family = [t for t in original if compatible(Q, row, t, eq, er)]
            removed = [dict(support=t, identical_local_rows=[Q[i] for i in t],
                            source_residual=eq, target_residual=er)
                       for t in original if t not in family]
            forced = sorted(set.intersection(*map(set, family))) if family else []
            witnesses = []
            for pair in combinations(forced, 2):
                for route in routes(record['spoke'], record['supports'][1-k], pair):
                    arcs = frame_arcs(*pair, route['landing'])
                    witnesses.append(dict(forced_pair=pair, route=route, frame_arcs=arcs,
                        external_component=1-k if route['mode']=='external_component' else None,
                        branch_set_recipe=dict(A=f'W_0 in C{k}', A_prime=f'W_1 in C{k}',
                            Z=f'(V(J_C{k}) minus x_0,x_1) union V(L) union Z_frame',
                            X=arcs[0], Y=arcs[1])))
            cases.append(dict(beta=bc['beta'], common_source_residual=eq,
                target_residual=er, previous_supports=original,
                removed_by_locality=removed, refined_supports=family,
                forced_vertices=forced, witnesses=witnesses,
                inherited_eliminated=bc['eliminated'],
                eliminated=bc['eliminated'] or not family or bool(witnesses)))
        components.append(dict(component=k, ordered_contacts=record['ordered_contacts'][k],
            source_forbidden=record['bans'][k], target_forbidden=bans[k],
            beta_cases=cases, eliminated=all(c['eliminated'] for c in cases)))
    return dict(components=components, eliminated=old['eliminated'] or
                any(c['eliminated'] for c in components))


def reflection_audit(record, row, bans, ev):
    reflected = dict(record['reflection'], ordered_contacts=record['ordered_contacts'])
    raw = [PI[row[RHO[i]]] for i in range(5)]
    moved = [sorted(PI[c] for c in f) for f in bans]
    rev = evidence(reflected, raw, moved)
    assert ev['eliminated'] == rev['eliminated']
    for a, b in zip(ev['components'], rev['components']):
        assert a['component'] == b['component'] and a['eliminated'] == b['eliminated']
        rb = {c['beta']: c for c in b['beta_cases']}
        for c in a['beta_cases']:
            rc = rb[PI[c['beta']]]
            assert c['eliminated'] == rc['eliminated']
            for key in ('common_source_residual', 'target_residual'):
                assert {PI[h] for h in c[key]} == set(rc[key])
            for key in ('previous_supports', 'refined_supports'):
                assert {tuple(sorted(RHO[i] for i in t)) for t in c[key]} == set(map(tuple, rc[key]))
            assert {tuple(sorted(RHO[i] for i in t['support'])) for t in c['removed_by_locality']} == {
                tuple(t['support']) for t in rc['removed_by_locality']}
            for w in c['witnesses']:
                pair = sorted(RHO[i] for i in w['forced_pair'])
                landing = RHO[w['route']['landing']]
                verify_arcs(tuple(RHO[i] for i in (*w['forced_pair'], w['route']['landing'])),
                            [[RHO[i] for i in arc] for arc in w['frame_arcs']])
                assert any(list(rw['forced_pair']) == pair and rw['route'] ==
                    dict(mode=w['route']['mode'], landing=landing) for rw in rc['witnesses'])
    return dict(raw_target=raw, transported_forbidden=moved, evidence=rev)


def algebra_controls():
    # The induction subtracts the already determined descendant palettes.
    induction = []
    for ls in subsets(U):
        for children in subsets(ls):
            residual = ls - children
            for perm in PERMS:
                moved = lambda values: {perm[c] for c in values}
                assert moved(residual) == moved(ls) - moved(children)
                induction.append([sorted(ls), sorted(children), perm, sorted(residual)])
    # Direct-root attachments and all off-path palettes must both be retained.
    root = []
    for support in subsets((0, 3, 4)):
        for direct in subsets(support):
            dq, dr = {Q[i] for i in direct}, {ROWS[2][i] for i in direct}
            assert dq == dr
            for branches in subsets(U - dq):
                eq, er = U - dq - branches, U - dr - branches
                assert eq == er
                root.append([sorted(support), sorted(direct), sorted(branches), sorted(eq)])
    # Independently check all source/target stabilizers in the record 90 domain.
    supports = []
    for beta, t in product((0, 2), subsets((0, 2, 3, 4))):
        eq, er = {1, beta}, {1, 2}
        local = all({p[c] for c in f} == f for row, f in ((Q, eq), (ROWS[2], er))
                    for p in PERMS if all(p[row[i]] == row[i] for i in t))
        same = all(Q[i] == ROWS[2][i] for i in t)
        allowed = local and (not same or eq == er)
        expected = {2, 3} <= t if beta == 0 else {3, 4} <= t
        assert allowed == expected
        supports.append(dict(beta=beta, support=sorted(t), separate_stabilizers=local,
                             identical_local_rows=same, allowed=allowed))
    assert len(induction) == 1944 and len(supports) == 32
    return dict(induction_count=len(induction),
        induction_sha256=sha256(json.dumps(induction, sort_keys=True).encode()).hexdigest(),
        root_controls=root, record90_supports=supports)


def minor_controls():
    result = []
    for pair, length, styles, reflected in product(((2, 3), (3, 4)), range(1, 18, 2),
                                                   product(STYLES, repeat=2), (False, True)):
        spoke = 0
        arcs = [[pair[0]], [pair[1]], sorted(set(range(5))-set(pair))]
        if reflected:
            pair, spoke = tuple(RHO[i] for i in pair), RHO[spoke]
            arcs = [[RHO[i] for i in arc] for arc in arcs]
        result.append(control(length, 0, 1, pair, spoke, styles, 0, arcs=arcs))
    assert len(result) == 576
    return result


def negative_controls():
    result = []
    assert compatible(Q, ROWS[2], (2, 3), (0, 1), (1, 2))
    result.append('different_local_rows_do_not_imply_equal_residuals')
    assert compatible(Q, ROWS[2], (0, 3, 4), (1, 2), (1, 2))
    result.append('equal_local_residuals_are_not_excluded')
    assert not compatible(Q, ROWS[2], (0, 3, 4), (0, 1), (1, 2))
    assert compatible(Q, ROWS[2], (0, 2, 3, 4), (0, 1), (1, 2))
    result.append('include_root_direct_attachments_in_support')
    assert {1} != {0, 1}
    result.append('source_F_is_not_local_E')
    try:
        joint_supports(Q, ROWS[2], (0, 2, 3, 4), (1,), (1, 2))
    except AssertionError:
        result.append('old_singleton_guard_preserved')
    else:
        raise AssertionError('lost singleton guard')
    assert not closes_target([dict(eliminated=True), dict(eliminated=False)])
    assert not closes_target([])
    result.append('partial_or_empty_candidates_do_not_close_target')
    base = control(1, 0, 1, (2, 3), 0, ('direct', 'direct'), 0,
                   arcs=[[2], [3], [0, 1, 4]])
    edges, bags = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    broken = [('missing_spoke', edges-{('b0', 'z')}, bags),
              ('missing_tether', edges-{('b2', 'x0')}, bags),
              ('missing_bridge', edges-{('x0', 'x1')}, bags),
              ('missing_cycle_edge', edges-{('x0', 'z')}, bags),
              ('broken_complement_arc', edges-{('b0', 'b4')}, bags),
              ('missing_frame_adjacency', edges-{('b2', 'b3')}, bags),
              ('overlapping_bags', edges, [bags[0]|{'z'}]+bags[1:])]
    for name, es, bs in broken:
        try:
            verify_minor(es, bs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    return result


def refine_table():
    source, previous = [json.loads(p.read_text()) for p in (SOURCE, PREVIOUS)]
    for path, digest in previous['source_sha256'].items():
        assert sha256((ROOT/path).read_bytes()).hexdigest() == digest
    originals = {r['id']: r for r in source['records']}
    old = previous['table']
    assert old['unresolved'] == [[90, 1], [282, 1]]
    retained, new, allcases = [], [], []
    for entry in old['retained']:
        rid, r = entry['source_id'], entry['original_record']
        assert r == originals[rid]
        targets = []
        for ti, pt in enumerate(entry['targets']):
            row, cases = pt['row'], []
            if pt['status'] == 'unresolved':
                original = r['targets'][ti]
                rejecting = [[f0, f1] for f0, f1 in product(*(c['forbidden_options'] for c in original['components']))
                             if U-{row[r['spoke']]} <= set(f0)|set(f1)]
                assert row == original['row'] == list(ROWS[ti+1])
                assert rejecting == original['rejection_options'] == [c['forbidden_options'] for c in pt['rejection_cases']]
                assert sum(not c['eliminated'] for c in pt['rejection_cases']) == 1
                for bans, oldcase in zip(rejecting, pt['rejection_cases']):
                    ev = reflection = None
                    if not oldcase['eliminated']:
                        first = first_evidence(r, row, bans)
                        assert json.loads(json.dumps(first)) == oldcase['first_bridge_evidence']
                        assert not first['eliminated']
                        ev = evidence(r, row, bans)
                        reflection = reflection_audit(r, row, bans, ev)
                    cases.append(dict(forbidden_options=bans, inherited_eliminated=oldcase['eliminated'],
                        locality_evidence=ev, reflection=reflection,
                        eliminated=oldcase['eliminated'] or bool(ev and ev['eliminated'])))
                if closes_target(cases):
                    new.append(dict(source_id=rid, target_index=ti, row=row))
            targets.append(dict(row=row, previous_status=pt['status'], previous_target=pt,
                rejection_cases=cases, status='accept' if closes_target(cases) else pt['status']))
            allcases.extend(cases)
        retained.append(dict(source_id=rid, original_record=r,
                             source_evidence=entry['source_evidence'], targets=targets))
    pair = [e for e in retained if e['source_id'] in (90, 282)]
    assert pair[0]['original_record']['supports'] == pair[1]['original_record']['supports'][::-1]
    assert {tuple(map(tuple, c['forbidden_options'][::-1])): c['eliminated'] for c in pair[0]['targets'][1]['rejection_cases']} == {
        tuple(map(tuple, c['forbidden_options'])): c['eliminated'] for c in pair[1]['targets'][1]['rejection_cases']}
    counts = Counter('/'.join(t['status'] for t in e['targets']) for e in retained)
    assert counts == {'accept/accept': 102}
    assert [(x['source_id'], x['target_index']) for x in new] == [(90, 1), (282, 1)]
    assert [e['source_id'] for e in retained] == old['remaining_source_ids']
    assert len(old['previous_excluded_source_ids']) == old['cumulative_excluded_labeled'] == 278
    return dict(previous_excluded_source_ids=old['previous_excluded_source_ids'],
        newly_excluded_labeled=0, cumulative_excluded_labeled=278,
        remaining_labeled=102, remaining_component_swap_types=51,
        remaining_source_ids=old['remaining_source_ids'], retained=retained,
        newly_accepted=new, queries_removed_by_source_exclusion=[],
        scanned_unresolved_queries=2, candidate_audit=dict(total=len(allcases),
            inherited_eliminated=sum(c['inherited_eliminated'] for c in allcases),
            newly_eliminated=sum(c['eliminated'] and not c['inherited_eliminated'] for c in allcases),
            remaining=sum(not c['eliminated'] for c in allcases)),
        remaining_targets=dict(counts), unresolved_queries=0, unresolved=[])


def build():
    paths = [SOURCE, PREVIOUS, Path(__file__)] + [ROOT/'scripts'/name for name in (
        'c5_single_spoke_first_bridge.py', 'c5_single_spoke_cross_row.py',
        'c5_single_spoke_frame_arc.py', 'c5_single_spoke_two_two_external.py',
        'c5_single_spoke_two_two_minor.py')]
    return dict(scope='record 90 residual locality and target extension; not source realizability',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        algebra=algebra_controls(), minor_controls=minor_controls(),
        negative_controls=negative_controls(), table=refine_table())


def support_table(result):
    lines = ['# (2,2) residual locality: completed target table', '',
        'Generated by [checker](../../scripts/c5_single_spoke_residual_locality.py).',
        'Scope and proof: [report](../../docs/c5_single_spoke_residual_locality.md).', '',
        'A = proved target extension; retained records are not realizations.',
        'Original records and previous evidence remain in JSON.', '',
        '| ID | p1 | p2 | newly proved |', '| ---: | --- | --- | --- |']
    for e in result['table']['retained']:
        new = ', '.join(f'p{i+1}' for i, t in enumerate(e['targets']) if t['status'] != t['previous_status'])
        lines.append(f"| {e['source_id']} | A | A | {new} |")
    return '\n'.join(lines + ['', '2 new target extensions; 278 source exclusions unchanged.',
        '102 retained records / 51 component-swap types; 102 A/A, 0 unresolved queries.', ''])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    fields = []
    for key, value in sorted(result.items()):
        encoded = ('[\n'+',\n'.join(json.dumps(v, sort_keys=True) for v in value)+'\n]'
                   if key == 'minor_controls' else json.dumps(value, sort_keys=True, indent=2))
        fields.append(json.dumps(key)+': '+encoded)
    payload, table = '{\n'+',\n'.join(fields)+'\n}\n', support_table(result)
    if args.check:
        assert OUT.read_bytes() == payload.encode(), 'certificate differs'
        assert TABLE.read_bytes() == table.encode(), 'support table differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
        TABLE.write_text(table)
    print(json.dumps(dict(induction_controls=result['algebra']['induction_count'],
        root_controls=len(result['algebra']['root_controls']),
        support_controls=len(result['algebra']['record90_supports']),
        minor_controls=len(result['minor_controls']), negative_controls=len(result['negative_controls']),
        candidate_audit=result['table']['candidate_audit'],
        remaining_targets=result['table']['remaining_targets'], unresolved=result['table']['unresolved']), sort_keys=True))


if __name__ == '__main__':
    main()
