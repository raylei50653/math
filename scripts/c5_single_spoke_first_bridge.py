#!/usr/bin/env python3
"""Singleton-source certificates on a target-pair original bridge path.

The local source residual is not the source forbidden set.  Both first-bridge
ends use the same beta.  Paper induction supplies arbitrary-size coverage;
these controls and the immutable-table refinement do not prove realizability.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_single_spoke_two_two_minor import Q, U, PERMS, subsets, verify_minor
from c5_single_spoke_two_two_external import RHO, PI, STYLES, routes
from c5_single_spoke_frame_arc import ROWS, admissible_supports, control, frame_arcs, verify_arcs
from c5_single_spoke_cross_row import candidate_evidence, closes_target, joint_supports
from c5_single_spoke_two_arc import evidence as two_arc_evidence, support_family

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_single_spoke_two_two/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_single_spoke_two_arc/observations.json'
OUT = ROOT / 'artifacts/c5_single_spoke_first_bridge/observations.json'
TABLE = OUT.with_name('support_table.md')


def fixed_colors(q, r, support):
    return {c for c in U if all((q[i] == c) == (r[i] == c) for i in support)}


def component_evidence(record, row, bans, k):
    fq, fr = record['bans'][k], bans[k]
    if len(fq) != 1 or len(fr) != 2:
        return None
    support, c = tuple(record['supports'][k]), fq[0]
    fixed = fixed_colors(Q, row, support)
    ev = dict(component=k, ordered_contacts=record['ordered_contacts'][k],
              source_forbidden=fq, target_forbidden=fr, fixed_colors=sorted(fixed),
              applicable=c in fixed, beta_cases=[], eliminated=False)
    if c not in fixed:
        return ev  # No assertion about the next root's membership of c.
    if c not in fr:
        # Endpoint tightness gives c in E0(q), conservation gives c in E0(r).
        return dict(ev, eliminated=True, reason='endpoint_fixed_color_contradiction',
                    conserved_source_color=c)
    betas = [b for b in sorted(U - {c}) if {c, b} & fixed == set(fr) & fixed]
    ev['possible_beta'] = betas
    for beta in betas:
        residual = tuple(sorted((c, beta)))
        target = admissible_supports(tuple(row), support, tuple(fr))
        source = admissible_supports(Q, support, residual)
        family = tuple(t for t in target if t in source)
        forced = sorted(set.intersection(*map(set, family))) if family else []
        witnesses = []
        for pair in combinations(forced, 2):
            for route in routes(record['spoke'], record['supports'][1-k], pair):
                arcs = frame_arcs(*pair, route['landing'])
                witnesses.append(dict(kind='first_bridge_frame_arc_K5', forced_pair=pair,
                    route=route, external_component=1-k if route['mode']=='external_component' else None,
                    frame_arcs=arcs,
                    branch_set_recipe=dict(A=f'W_0 in C{k}', A_prime=f'W_1 in C{k}',
                        Z=f'(V(J_C{k}) minus x_0,x_1) union V(L) union Z_frame',
                        X=[f'b{i}' for i in arcs[0]], Y=[f'b{i}' for i in arcs[1]])))
        ev['beta_cases'].append(dict(beta=beta, common_source_residual=residual,
            target_only_supports=[sorted(t) for t in target],
            first_two_bag_supports=[sorted(t) for t in family],
            forced_vertices=forced, witnesses=witnesses,
            eliminated=not family or bool(witnesses),
            reason='no_possible_first_bag' if not family else 'minor' if witnesses else 'unresolved'))
    # Empty beta domain is a contradiction of the existing first bridge.
    ev['eliminated'] = all(case['eliminated'] for case in ev['beta_cases'])
    ev['reason'] = 'all_shared_beta_cases' if betas else 'no_possible_first_bridge_palette'
    return ev


def evidence(record, row, bans):
    components = [ev for k in range(2)
                  if (ev := component_evidence(record, row, bans, k)) is not None]
    return dict(components=components, eliminated=any(c['eliminated'] for c in components))


def reflection_audit(record, row, bans, ev):
    reflected = dict(record['reflection'], ordered_contacts=record['ordered_contacts'])
    raw = tuple(PI[row[RHO[i]]] for i in range(5))
    moved = [sorted(PI[c] for c in f) for f in bans]
    rev = evidence(reflected, raw, moved)
    assert ev['eliminated'] == rev['eliminated']
    for a, b in zip(ev['components'], rev['components']):
        assert a['component'] == b['component']
        if a['applicable']:
            assert a['reason'] == b['reason']
        assert {PI[c] for c in a['fixed_colors']} == set(b['fixed_colors'])
        assert a['applicable'] == b['applicable'] and a['eliminated'] == b['eliminated']
        rb = {case['beta']: case for case in b['beta_cases']}
        for case in a['beta_cases']:
            rc = rb[PI[case['beta']]]
            assert case['eliminated'] == rc['eliminated']
            assert {PI[c] for c in case['common_source_residual']} == set(rc['common_source_residual'])
            for key in ('target_only_supports', 'first_two_bag_supports'):
                assert {tuple(sorted(RHO[i] for i in t)) for t in case[key]} == set(map(tuple, rc[key]))
            for w in case['witnesses']:
                pair = sorted(RHO[i] for i in w['forced_pair'])
                route = dict(mode=w['route']['mode'], landing=RHO[w['route']['landing']])
                # The clockwise arc convention reverses under reflection; the
                # reflected partition itself remains a valid named minor.
                verify_arcs(tuple(RHO[i] for i in (*w['forced_pair'], w['route']['landing'])),
                            [[RHO[i] for i in arc] for arc in w['frame_arcs']])
                assert any(list(rw['forced_pair']) == pair and rw['route'] == route for rw in rc['witnesses'])


def algebra_controls():
    # All possible (list, descendant-union) memberships in one induction step.
    states = [(ls, children) for ls in subsets(U) for children in subsets(ls)]
    closure, digest = 0, sha256()
    for c, (lq, hq), (lr, hr) in product(sorted(U), states, states):
        if (c in lq) != (c in lr) or (c in hq) != (c in hr):
            continue
        assert (c in lq-hq) == (c in lr-hr)
        digest.update(json.dumps([c, sorted(lq), sorted(hq), sorted(lr), sorted(hr)]).encode())
        closure += 1
    assert closure == 8748
    residual = []
    pairs = [(d, q) for d, q in product(subsets(U), repeat=2) if not d & q]
    for (dq, qq), (dr, qr) in product(pairs, repeat=2):
        if U-dr-qr != {1, 2} or dq & {1, 3} != dr & {1, 3} or qq & {1, 3} != qr & {1, 3}:
            continue
        eq = U-dq-qq
        assert 1 in eq and 3 not in eq
        residual.append([sorted(dq), sorted(qq), sorted(dr), sorted(qr), sorted(eq)])
    assert len(residual) == 36
    # Endpoint tightness is needed in addition to E\{c}={beta}.
    endpoints = []
    for c, (direct, branch), beta in product(sorted(U), pairs, sorted(U)):
        if c in direct or c in branch or U-direct-branch-{c} != {beta}:
            continue
        eq = U-direct-branch
        assert beta != c and eq == {c, beta}
        endpoints.append([c, sorted(direct), sorted(branch), beta])
    assert len(endpoints) == 48
    first_edges = []
    for c, beta, contact, e1 in product(sorted(U), sorted(U), (False, True), subsets(U)):
        if beta == c or c not in e1:
            continue
        if contact:
            valid = e1-{c} == {beta}
        else:
            valid = len(e1) == 2 and beta in e1
        if valid:
            assert e1 == {c, beta}
            first_edges.append([c, beta, contact, sorted(e1)])
    assert len(first_edges) == 24
    return dict(fixed_color_induction_count=closure, induction_sha256=digest.hexdigest(),
                record87_residual=residual, tight_endpoint=endpoints, first_edge=first_edges)


def record87_controls():
    rows, pairs = [], []
    for t in subsets((2, 3, 4)):
        allowed = []
        for beta in (0, 2):
            eq = {1, beta}
            # Direct stabilizers, independent of admissible_supports.
            invariant = all({p[c] for c in f} == f for row, f in ((Q, eq), (ROWS[2], {1, 2}))
                            for p in PERMS if all(p[row[i]] == row[i] for i in t))
            expected = ({2, 3} if beta == 0 else {3, 4}) <= t
            assert invariant == expected
            if invariant:
                allowed.append(beta)
        rows.append(dict(support=sorted(t), allowed_beta=allowed))
    for a, b, beta in product(rows, rows, (0, 2)):
        if beta in a['allowed_beta'] and beta in b['allowed_beta']:
            pairs.append(dict(beta=beta, supports=[a['support'], b['support']]))
    assert len(rows) == len(pairs) == 8
    return dict(supports=rows, shared_beta_support_pairs=pairs)


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
    base = control(1, 0, 1, (2, 3), 0, ('direct', 'direct'), 0,
                   arcs=[[2], [3], [0, 1, 4]])
    edges, bags = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    broken = [('missing_spoke', edges-{('b0', 'z')}, bags),
              ('missing_tether', edges-{('b2', 'x0')}, bags),
              ('missing_bridge', edges-{('x0', 'x1')}, bags),
              ('missing_cycle_edge', edges-{('x0', 'z')}, bags),
              ('broken_complement_arc', edges-{('b0', 'b4')}, bags),
              ('missing_frame_adjacency', edges-{('b2', 'b3')}, bags),
              ('overlap', edges, [bags[0]|{'z'}]+bags[1:])]
    results = []
    for name, es, bs in broken:
        try:
            verify_minor(es, bs)
        except AssertionError:
            results.append(name)
        else:
            raise AssertionError(name)
    support_rows = {tuple(r['support']): set(r['allowed_beta'])
                    for r in record87_controls()['supports']}
    a, b = support_rows[2, 3], support_rows[3, 4]
    assert a and b and not a & b
    results.append('independent_beta_choices_do_not_give_a_shared_palette')
    assert {0}-{1} == {0} and {0} != {0, 1}
    results.append('endpoint_equation_alone_does_not_supply_deleted_color')
    # First-bridge beta can change further along a rejected odd path.
    palette_sequence = [0, 1, 2]
    assert all(x != y and 1 in (x, y) for x, y in zip(palette_sequence, palette_sequence[1:]))
    results.append('different_odd_bridges_need_not_share_beta')
    assert {1} != {1, 0}
    results.append('local_source_residual_is_not_singleton_F')
    assert support_family(ROWS[2], (2, 3, 4), (1,), (1, 2)) == admissible_supports(ROWS[2], (2, 3, 4), (1, 2))
    try:
        joint_supports(Q, ROWS[2], (2, 3, 4), (1,), (1, 2))
    except AssertionError:
        results.append('old_singleton_guard_is_preserved')
    else:
        raise AssertionError('joint_supports singleton guard lost')
    assert not closes_target([dict(eliminated=True), dict(eliminated=False)])
    assert not closes_target([])
    results.append('partial_or_empty_rejection_cases_do_not_accept_target')
    # Synthetic guard controls do not assert a realizable source.
    r = dict(supports=[[2, 3, 4], [0, 1, 2]], bans=[[1], [2, 3]],
             spoke=0, ordered_contacts=[['u0', 'v0'], ['u1', 'v1']])
    assert not component_evidence(r, ROWS[1], [[1, 2], [3]], 0)['applicable']
    results.append('nonconserved_source_color_does_not_enter_lemma')
    r['supports'][0] = [0, 2, 3, 4]
    ev = component_evidence(r, ROWS[2], [[1, 2], [3]], 0)
    assert not ev['eliminated'] and [b['beta'] for b in ev['beta_cases'] if not b['eliminated']] == [0]
    results.append('one_unresolved_beta_keeps_the_complete_candidate')
    assert component_evidence(r, ROWS[2], [[1], [2, 3]], 0) is None
    results.append('singleton_target_has_no_target_pair_path')
    return results


def refine_table():
    source, previous = [json.loads(p.read_text()) for p in (SOURCE, PREVIOUS)]
    for path, digest in previous['source_sha256'].items():
        assert sha256((ROOT/path).read_bytes()).hexdigest() == digest
    originals = {r['id']: r for r in source['records']}
    old = previous['table']
    assert old['remaining_labeled'] == 102 and old['unresolved_queries'] == 18
    retained, new, allcases, used_minors = [], [], [], set()
    for entry in old['retained']:
        rid, r = entry['source_id'], entry['original_record']
        assert r == originals[rid]
        targets = []
        for ti, pt in enumerate(entry['targets']):
            row, cases = pt['row'], []
            if pt['status'] == 'unresolved':
                original = r['targets'][ti]
                assert row == original['row'] == list(ROWS[ti+1])
                assert r['reflection']['targets'][ti]['row'] == [PI[row[RHO[i]]] for i in range(5)]
                rejecting = [[f0, f1] for f0, f1 in product(*(c['forbidden_options'] for c in original['components']))
                             if U-{row[r['spoke']]} <= set(f0)|set(f1)]
                assert rejecting == original['rejection_options'] == [c['forbidden_options'] for c in pt['rejection_cases']]
                assert sum(not c['eliminated'] for c in pt['rejection_cases']) == 1
                for bans, oldcase in zip(rejecting, pt['rejection_cases']):
                    cross = candidate_evidence(r, row, bans)
                    two = two_arc_evidence(r, row, bans)
                    assert json.loads(json.dumps(two)) == oldcase['two_arc_evidence']
                    assert cross['eliminated'] == oldcase['inherited_eliminated']
                    assert oldcase['eliminated'] == bool(cross['eliminated'] or two['witnesses'])
                    ev = evidence(r, row, bans) if not oldcase['eliminated'] else None
                    if ev is not None:
                        reflection_audit(r, row, bans, ev)
                        for c in ev['components']:
                            for b in c['beta_cases']:
                                for w in b['witnesses']:
                                    used_minors.add((tuple(w['forced_pair']), w['route']['landing'], w['route']['mode']))
                    cases.append(dict(forbidden_options=bans, inherited_evidence=oldcase,
                        inherited_eliminated=oldcase['eliminated'], first_bridge_evidence=ev,
                        eliminated=oldcase['eliminated'] or bool(ev and ev['eliminated'])))
                if closes_target(cases):
                    new.append(dict(source_id=rid, target_index=ti, row=row))
            targets.append(dict(row=row, previous_status=pt['status'], previous_target=pt,
                rejection_cases=cases, status='accept' if closes_target(cases) else pt['status']))
            allcases.extend(cases)
        retained.append(dict(source_id=rid, original_record=r, source_evidence=entry['source_evidence'], targets=targets))
    key = lambda e: (e['original_record']['spoke'], tuple(map(tuple, e['original_record']['supports'])),
                     tuple(map(tuple, e['original_record']['bans'])))
    keyed = {key(e): e for e in retained}
    for (s, supports, bans), e in keyed.items():
        other = keyed[s, supports[::-1], bans[::-1]]
        for a, b in zip(e['targets'], other['targets']):
            assert a['status'] == b['status']
            assert {tuple(map(tuple, c['forbidden_options'][::-1])): c['eliminated'] for c in a['rejection_cases']} == {
                tuple(map(tuple, c['forbidden_options'])): c['eliminated'] for c in b['rejection_cases']}
    counts = Counter('/'.join(t['status'] for t in e['targets']) for e in retained)
    assert counts == {'accept/accept': 100, 'accept/unresolved': 2}
    unresolved = [[e['source_id'], i] for e in retained for i, t in enumerate(e['targets']) if t['status']=='unresolved']
    assert unresolved == [[90, 1], [282, 1]] and len(new) == 16
    excluded_ids = sorted(old['previous_excluded_source_ids']+[e['source_id'] for e in old['excluded']])
    assert len(excluded_ids) == len(set(excluded_ids)) == 278
    assert [e['source_id'] for e in retained] == old['remaining_source_ids']
    audit = dict(rejection_cases=len(allcases), inherited_eliminated=sum(c['inherited_eliminated'] for c in allcases),
                 newly_eliminated=sum(c['eliminated'] and not c['inherited_eliminated'] for c in allcases),
                 remaining=sum(not c['eliminated'] for c in allcases))
    modes = Counter(next(ev['reason'] for ev in c['first_bridge_evidence']['components'] if ev['eliminated']) for c in allcases
                    if not c['inherited_eliminated'] and c['eliminated'])
    assert modes == {'all_shared_beta_cases': 10, 'endpoint_fixed_color_contradiction': 6}
    return dict(previous_excluded_source_ids=excluded_ids, newly_excluded_labeled=0,
        cumulative_excluded_labeled=278, remaining_labeled=102, remaining_component_swap_types=51,
        remaining_source_ids=old['remaining_source_ids'], retained=retained, newly_accepted=new,
        queries_removed_by_source_exclusion=[], scanned_unresolved_queries=18, candidate_audit=audit,
        new_extension_reasons=dict(modes), remaining_targets=dict(sorted(counts.items())),
        unresolved_queries=2, unresolved_records=2, unresolved=unresolved), sorted(used_minors)


def build():
    paths = [SOURCE, PREVIOUS, Path(__file__)] + [ROOT/'scripts'/name for name in (
        'c5_single_spoke_two_arc.py', 'c5_single_spoke_cross_row.py', 'c5_single_spoke_frame_arc.py',
        'c5_single_spoke_two_two_external.py', 'c5_single_spoke_two_two_minor.py')]
    table, used = refine_table()
    # Also cover every frame/route mode actually used by the table.
    general = [control(length, 0, 1, pair, landing, styles, size)
               for pair, landing, mode in used for length in (1, 3, 7)
               for styles in product(STYLES, repeat=2)
               for size in ((0,) if mode=='spoke' else (1, 4))]
    return dict(scope='singleton-source first bridge on target-pair path; paper proof and finite controls, not realizations',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        algebra=algebra_controls(), record87=record87_controls(), record87_minor_controls=minor_controls(),
        table_minor_controls=general, negative_controls=negative_controls(), table=table)


def support_table(result):
    table = result['table']
    lines = ['# (2,2) singleton-source first-bridge target extensions', '',
        'Generated by [checker](../../scripts/c5_single_spoke_first_bridge.py);',
        'paper proof and trust boundary: [report](../../docs/c5_single_spoke_first_bridge.md).', '',
        'No new source exclusion. A = proved extension; ? = unresolved, not a realization.',
        'The original records and all previous target evidence remain in JSON.', '',
        '| ID | p1 | p2 | newly proved |', '| ---: | --- | --- | --- |']
    for e in table['retained']:
        labels = [{'accept':'A', 'unresolved':'?'}[t['status']] for t in e['targets']]
        new = ', '.join(f'p{i+1}' for i,t in enumerate(e['targets']) if t['status'] != t['previous_status'])
        lines.append(f"| {e['source_id']} | {labels[0]} | {labels[1]} | {new} |")
    lines += ['', '16 new target extensions; 278 cumulative source exclusions unchanged.',
              '102 retained sources / 51 swap types; 100 A/A, 2 A/?.',
              'Only record 90 and its component swap 282 remain unresolved at p2.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    fields = []
    for key, value in sorted(result.items()):
        encoded = ('[\n'+',\n'.join(json.dumps(v, sort_keys=True) for v in value)+'\n]'
                   if key.endswith('_minor_controls') else json.dumps(value, sort_keys=True, indent=2))
        fields.append(json.dumps(key)+': '+encoded)
    payload, table = '{\n'+',\n'.join(fields)+'\n}\n', support_table(result)
    if args.check:
        assert OUT.read_bytes() == payload.encode(), 'certificate differs'
        assert TABLE.read_bytes() == table.encode(), 'support table differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
        TABLE.write_text(table)
    print(json.dumps(dict(record87_minor_controls=len(result['record87_minor_controls']),
        table_minor_controls=len(result['table_minor_controls']), negative_controls=len(result['negative_controls']),
        candidate_audit=result['table']['candidate_audit'], new_extension_reasons=result['table']['new_extension_reasons'],
        remaining_targets=result['table']['remaining_targets'], unresolved=result['table']['unresolved']), sort_keys=True))


if __name__ == '__main__':
    main()
