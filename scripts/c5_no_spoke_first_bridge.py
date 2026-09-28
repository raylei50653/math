#!/usr/bin/env python3
"""Close no-spoke (2,2,1) with first-bridge palettes and fixed frame arcs.

The source residual E is not the forbidden set F.  One beta binds both
first-bridge ends; an original other component connects z to the frame.
Fixed frame arcs also allow the two bags to use different boundary vertices.
Paper induction supplies arbitrary-size coverage, not these finite controls.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_single_spoke_cores import Q, TARGETS, U, PI, RHO
from c5_single_spoke_two_two_minor import PERMS, subsets, connected, verify_minor
from c5_single_spoke_two_two_external import STYLES
from c5_single_spoke_frame_arc import FRAME_EDGES, admissible_supports, frame_arcs, verify_arcs
from c5_single_spoke_cross_row import closes_target, joint_supports
from c5_single_spoke_first_bridge import fixed_colors, algebra_controls
from c5_no_spoke_path_minor import (
    canonical, digest, no_spoke_control, negative_controls as path_negative_controls,
)

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT / 'artifacts/c5_no_spoke_path_minor/observations.json'
OUT = ROOT / 'artifacts/c5_no_spoke_first_bridge/observations.json'
TABLE = OUT.with_name('support_table.md')
FRAME_PARTITIONS = tuple(tuple(tuple(a) for a in frame_arcs(*anchors))
                         for anchors in permutations(range(5), 3))
assert len(set(FRAME_PARTITIONS)) == 60


def frame_evidence(record, row, bans):
    """One fixed three-arc partition, with possibly different bag landings."""
    constraints, witnesses = [], []
    for k, f in enumerate(bans):
        if len(f) != 2:
            continue
        assert record['parts'][k] == 2
        family = admissible_supports(tuple(row), tuple(record['supports'][k]), tuple(f))
        constraints.append(dict(component=k, ordered_contacts=[f'c{k}p0', f'c{k}p1'],
                                forbidden=f, allowed_bag_supports=[sorted(t) for t in family]))
        if not family:
            witnesses.append(dict(kind='no_possible_path_bag', component=k))
            continue
        for x, y, zframe in FRAME_PARTITIONS:
            if not all(t & set(x) and t & set(y) for t in family):
                continue
            for j, other in enumerate(record['supports']):
                if j == k:
                    continue
                for h in sorted(set(other) & set(zframe)):
                    witnesses.append(dict(kind='fixed_three_frame_arcs_K5', component=k,
                        frame_arcs=[x, y, zframe], external_component=j,
                        external_contact=f'c{j}p0', landing=h,
                        branch_set_recipe=[f'W_0 in C{k}', f'W_1 in C{k}',
                            f'(J_C{k} minus x_0,x_1) union original C{j} route union Z_frame',
                            'X_frame', 'Y_frame']))
    return dict(constraints=constraints, witnesses=witnesses, eliminated=bool(witnesses))


def frame_reflection_audit(record, row, bans, ev):
    rr = dict(record, supports=record['reflection']['supports'], bans=record['reflection']['bans'])
    raw = [PI[row[RHO[i]]] for i in range(5)]
    moved = [sorted(PI[c] for c in f) for f in bans]
    rev = frame_evidence(rr, raw, moved)
    assert ev['eliminated'] == rev['eliminated']
    for a, b in zip(ev['constraints'], rev['constraints'], strict=True):
        assert a['component'] == b['component']
        assert {tuple(sorted(RHO[i] for i in t)) for t in a['allowed_bag_supports']} == {
            tuple(t) for t in b['allowed_bag_supports']}
    for w in ev['witnesses']:
        if w['kind'] == 'no_possible_path_bag':
            assert w in rev['witnesses']
            continue
        arcs = [sorted(RHO[i] for i in a) for a in w['frame_arcs']]
        verify_arcs([a[0] for a in arcs], arcs)
        assert any(rw['kind'] == w['kind'] and rw['component'] == w['component']
                   and list(map(list, rw['frame_arcs'])) == arcs
                   and rw['external_component'] == w['external_component']
                   and rw['landing'] == RHO[w['landing']] for rw in rev['witnesses'])
    return dict(raw_target=raw, transported_forbidden=moved, evidence=rev)


def evidence(record, row, bans):
    assert record['parts'] == [2, 2, 1]
    assert len(bans) == len(record['supports']) == 3
    components = []
    for k, (fq, fr) in enumerate(zip(record['bans'], bans)):
        if len(fq) != 1 or len(fr) != 2:
            continue
        assert record['parts'][k] == 2
        support, c = tuple(record['supports'][k]), fq[0]
        fixed = fixed_colors(Q, row, support)
        ev = dict(component=k, ordered_contacts=[f'c{k}p0', f'c{k}p1'],
                  source_forbidden=fq, target_forbidden=fr,
                  fixed_colors=sorted(fixed), applicable=c in fixed,
                  beta_cases=[], eliminated=False)
        components.append(ev)
        if c not in fixed:
            continue
        if c not in fr:
            ev.update(eliminated=True, reason='endpoint_fixed_color_contradiction')
            continue
        betas = [b for b in sorted(U - {c}) if {c, b} & fixed == set(fr) & fixed]
        for beta in betas:
            residual = tuple(sorted((c, beta)))
            target = admissible_supports(tuple(row), support, tuple(fr))
            source = admissible_supports(Q, support, residual)
            family = [sorted(t) for t in target if t in source]
            forced = sorted(set.intersection(*map(set, family))) if family else []
            witnesses = []
            for pair in combinations(forced, 2):
                for j, other in enumerate(record['supports']):
                    if j == k:
                        continue
                    for h in sorted(set(other) - set(pair)):
                        witnesses.append(dict(kind='first_bridge_original_external_path_K5',
                            forced_pair=pair, external_component=j,
                            external_contact=f'c{j}p0', landing=h,
                            frame_arcs=frame_arcs(*pair, h),
                            branch_set_recipe=[f'W_0 in C{k}', f'W_1 in C{k}',
                                f'(J_C{k} minus x_0,x_1) union original C{j} route union Z_frame',
                                'X_frame', 'Y_frame']))
            ev['beta_cases'].append(dict(beta=beta, common_source_residual=residual,
                target_residual=fr, first_two_bag_supports=family,
                forced_vertices=forced, witnesses=witnesses,
                eliminated=not family or bool(witnesses)))
        ev.update(possible_beta=betas, eliminated=all(b['eliminated'] for b in ev['beta_cases']),
                  reason='all_shared_beta_cases' if betas else 'no_possible_first_bridge_palette')
    return dict(components=components, eliminated=any(c['eliminated'] for c in components))


def reflection_audit(record, row, bans, ev):
    reflected = dict(record, supports=record['reflection']['supports'],
                     bans=record['reflection']['bans'])
    raw = [PI[row[RHO[i]]] for i in range(5)]
    moved = [sorted(PI[c] for c in f) for f in bans]
    rev = evidence(reflected, raw, moved)
    assert ev['eliminated'] == rev['eliminated']
    for a, b in zip(ev['components'], rev['components'], strict=True):
        assert a['component'] == b['component']
        assert a['applicable'] == b['applicable'] and a['eliminated'] == b['eliminated']
        assert {PI[c] for c in a['fixed_colors']} == set(b['fixed_colors'])
        rb = {c['beta']: c for c in b['beta_cases']}
        assert {PI[c['beta']] for c in a['beta_cases']} == set(rb)
        for case in a['beta_cases']:
            rc = rb[PI[case['beta']]]
            assert case['eliminated'] == rc['eliminated']
            for key in ('common_source_residual', 'target_residual'):
                assert {PI[c] for c in case[key]} == set(rc[key])
            assert {tuple(sorted(RHO[i] for i in t)) for t in case['first_two_bag_supports']} == {
                tuple(t) for t in rc['first_two_bag_supports']}
            for w in case['witnesses']:
                pair = sorted(RHO[i] for i in w['forced_pair'])
                h = RHO[w['landing']]
                verify_arcs(tuple(RHO[i] for i in (*w['forced_pair'], w['landing'])),
                            [[RHO[i] for i in arc] for arc in w['frame_arcs']])
                assert any(list(rw['forced_pair']) == pair and rw['landing'] == h
                           and rw['external_component'] == w['external_component']
                           for rw in rc['witnesses'])
    return dict(raw_target=raw, transported_forbidden=moved, evidence=rev)


def support_controls():
    result = []
    # Independently compare all 24 permutations with the explicit forced pair.
    for support, row, c, fr, beta_pair in (
        ((0, 1, 4), TARGETS[0], 0, {0, 1}, ((1, {0, 1}), (2, {0, 4}))),
        ((2, 3, 4), TARGETS[1], 1, {1, 2}, ((0, {2, 3}), (2, {3, 4}))),
    ):
        for beta, forced in beta_pair:
            expected = set(admissible_supports(Q, support, tuple(sorted((c, beta))))) & set(
                admissible_supports(tuple(row), support, tuple(sorted(fr))))
            for t in subsets(support):
                invariant = all({p[h] for h in f} == f
                    for r, f in ((Q, {c, beta}), (row, fr))
                    for p in PERMS if all(p[r[i]] == r[i] for i in t))
                assert invariant == (forced <= t) == (t in expected)
                result.append(dict(support=sorted(t), row=row, beta=beta,
                                   source_residual=sorted((c, beta)), allowed=invariant,
                                   forced_pair=sorted(forced)))
    assert len(result) == 32
    return result


def minor_controls():
    controls = [no_spoke_control(length, 0, pair, h, styles, arity, size)
        for pair, h in (((0, 1), 2), ((0, 4), 2), ((2, 3), 0), ((3, 4), 0))
        for length in (1, 3, 5) for styles in product(STYLES, repeat=2)
        for arity in (1, 2) for size in (1, 3)]
    assert len(controls) == 768
    return controls


def frame_controls():
    # Independent vertex assignments check all labeled connected partitions.
    independent = set()
    for assignment in product(range(3), repeat=5):
        arcs = tuple(tuple(i for i in range(5) if assignment[i] == j) for j in range(3))
        if all(connected(set(a), FRAME_EDGES) for a in arcs):
            verify_arcs([a[0] for a in arcs], arcs)
            independent.add(arcs)
    assert independent == set(FRAME_PARTITIONS)
    supports = []
    for n, row in enumerate(TARGETS):
        f = {1, 3} if n == 0 else {2, 3}
        family = admissible_supports(tuple(row), (0, 1, 2, 3), tuple(sorted(f)))
        for t in subsets((0, 1, 2, 3)):
            invariant = all({p[c] for c in f} == f for p in PERMS
                            if all(p[row[i]] == row[i] for i in t))
            expected = (3 in t and bool(t & {0, 2}) if n == 0
                        else 0 in t and bool(t & {1, 3}))
            assert invariant == expected == (t in family)
            supports.append(dict(target=n, support=sorted(t), allowed=invariant))
        assert len(family) == 6
    controls = []
    for n in (0, 1):
        arcs = [[0, 1, 2], [3], [4]] if n == 0 else [[0], [1, 2, 3], [4]]
        suppliers = [(a, 3) for a in (0, 2)] if n == 0 else [(0, b) for b in (1, 3)]
        for pair0, pair1, length, styles, size in product(
                suppliers, suppliers, (1, 3, 5), product(STYLES, repeat=2), (1, 3)):
            r = no_spoke_control(length, 0, pair0, 4, styles, 2, size)
            edges = set(map(tuple, r['edges']))
            # Reattach the second bag to independently chosen points in X/Y.
            for route, landing in zip(r['actual_tether_routes'][1], pair1, strict=True):
                edges.remove(tuple(sorted(route[-2:])))
                route[-1] = f'b{landing}'
                edges.add(tuple(sorted(route[-2:])))
            bags = list(map(set, r['branch_sets']))
            bags[2] = (bags[2] - {f'b{i}' for i in range(5)}) | {f'b{i}' for i in arcs[2]}
            bags[3:] = [{f'b{i}' for i in a} for a in arcs[:2]]
            rename = lambda v: f'b{RHO[int(v[1:])]}' if v.startswith('b') else v
            reflected_edges = {tuple(sorted((rename(u), rename(v)))) for u, v in edges}
            reflected_bags = [{rename(v) for v in b} for b in bags]
            r.pop('pair')
            r.update(target=n, bag_supplier_pairs=[pair0, pair1], frame_arcs=arcs,
                     edges=sorted(edges), branch_sets=[sorted(b) for b in bags],
                     adjacencies=verify_minor(edges, bags),
                     reflected_adjacencies=verify_minor(reflected_edges, reflected_bags))
            controls.append(r)
    assert len(controls) == 768 and len(supports) == 32
    return dict(partition_count=len(independent), support_controls=supports, minor_controls=controls)


def negative_controls(frame_data):
    result = path_negative_controls()
    r = dict(parts=[2, 2, 1], supports=[[0, 1, 4], [1, 2, 3], [3, 4]],
             bans=[[0], [2, 3], [1]])
    bans = [[0, 1], [3], [2]]
    ev = evidence(r, TARGETS[0], bans)['components'][0]
    families = {b['beta']: set(map(tuple, b['first_two_bag_supports'])) for b in ev['beta_cases']}
    assert (0, 1) in families[1] and (0, 4) in families[2]
    assert not any({(0, 1), (0, 4)} <= f for f in families.values())
    result.append('independent_endpoint_beta_does_not_give_one_bridge_palette')
    assert all(len(b['common_source_residual']) == 2 for b in ev['beta_cases'])
    assert r['bans'][0] == [0]
    result.append('source_forbidden_singleton_is_not_local_residual')
    try:
        joint_supports(Q, TARGETS[0], (0, 1, 4), (0,), (0, 1))
    except AssertionError:
        result.append('old_pair_guard_preserved')
    else:
        raise AssertionError('singleton used as pair residual')
    assert not evidence(r, TARGETS[0], [[0], [1, 3], [2]])['components']
    result.append('no_singleton_to_pair_component_adds_no_evidence')
    changed = dict(r, bans=[[1], [2, 3], [0]])
    assert not evidence(changed, TARGETS[0], bans)['components'][0]['applicable']
    result.append('nonconserved_source_color_skipped')
    # Synthetic support control only; no claim that this is a disk source.
    changed = dict(r, supports=[[0, 1, 4], [0, 1], [0, 1]])
    partial = evidence(changed, TARGETS[0], bans)
    assert not partial['eliminated']
    assert [b['eliminated'] for b in partial['components'][0]['beta_cases']] == [False, True]
    result.append('one_beta_without_external_landing_keeps_candidate')
    assert not closes_target([dict(eliminated=True), dict(eliminated=False)])
    assert not closes_target([])
    result.append('all_complete_candidates_required')
    # The singleton-source quartet cannot be closed by frame partitions alone.
    assert not frame_evidence(r, TARGETS[0], bans)['eliminated']
    result.append('frame_partitions_do_not_replace_shared_beta')
    # Different bag landings invalidate a fixed-point witness, but not the
    # three-arc witness. Requiring a common point would lose this valid case.
    family = admissible_supports(TARGETS[0], (0, 1, 2, 3), (1, 3))
    assert set.intersection(*map(set, family)) == {3}
    assert all(t & {0, 1, 2} and t & {3} for t in family)
    result.append('one_common_frame_vertex_does_not_mean_no_arc_witness')
    assert not all(t & {0} and t & {1, 2, 3} for t in family)
    result.append('one_partition_must_work_for_every_support')
    r = next(r for r in frame_data['minor_controls'] if r['length'] == 1
             and r['styles'] == ('direct', 'direct')
             and r['bag_supplier_pairs'] == [(0, 3), (2, 3)])
    edges, bags = set(map(tuple, r['edges'])), list(map(set, r['branch_sets']))
    for name, es, bs in (
        ('arc_missing_original_route', edges - {('e0', 'z')}, bags),
        ('arc_missing_second_bag_supplier', edges - {('b2', 'x1')}, bags),
        ('arc_missing_bridge', edges - {('x0', 'x1')}, bags),
        ('arc_disconnected_X', edges - {('b1', 'b2')}, bags),
        ('arc_overlapping_bags', edges, [bags[0] | {'z'}] + bags[1:]),
    ):
        try:
            verify_minor(es, bs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    assert len(result) == 27
    return result


def refine_table(previous):
    old = previous['table']
    retained, new = [], []
    for entry in old['retained']:
        record, targets = entry['original_record'], []
        for n, target in enumerate(entry['targets']):
            if target['status'] == 'accept':
                targets.append(dict(row=target['row'], status='accept', inherited_accept=True))
                continue
            assert target['status'] == 'unresolved'
            covers = [fs for fs in product(*(c['options'] for c in record['targets'][n]['components']))
                      if set().union(*map(set, fs)) == U]
            assert canonical(covers) == [c['forbidden_options'] for c in target['cases']]
            cases = []
            for fs, before in zip(covers, target['cases'], strict=True):
                ev = evidence(record, target['row'], fs)
                reflected = reflection_audit(record, target['row'], fs, ev)
                cases.append(dict(forbidden_options=fs, previous_evidence=before,
                    first_bridge_evidence=ev, reflection=reflected,
                    eliminated=before['eliminated'] or ev['eliminated']))
            closed = closes_target(cases)
            status = 'accept' if closed else 'unresolved'
            if closed:
                new.append(dict(source_id=entry['source_id'], target=n))
            targets.append(dict(row=target['row'], status=status, inherited_accept=False,
                cases=cases, remaining_covers=[c['forbidden_options'] for c in cases if not c['eliminated']]))
        retained.append(dict(source_id=entry['source_id'], original_record=record, targets=targets))
    assert new == [dict(source_id=i, target=n) for i, n in ((84, 0), (408, 1), (1472, 0), (1561, 1))]
    assert [r['source_id'] for r in retained] == [r['source_id'] for r in old['retained']]
    counts = Counter('/'.join(t['status'] for t in r['targets']) for r in retained)
    assert counts == {'accept/accept': 112, 'unresolved/unresolved': 4}
    key = lambda r: (tuple(map(tuple, r['supports'])), tuple(map(tuple, r['bans'])))
    lookup = {key(r['original_record']): r for r in retained}
    for r in retained:
        a = r['original_record']
        swapped = dict(a, supports=[a['supports'][1], a['supports'][0], a['supports'][2]],
                       bans=[a['bans'][1], a['bans'][0], a['bans'][2]])
        assert [t['status'] for t in r['targets']] == [t['status'] for t in lookup[key(swapped)]['targets']]
    pending = [dict(source_id=r['source_id'], target=n, remaining_covers=t['remaining_covers'])
               for r in retained for n, t in enumerate(r['targets']) if t['status'] != 'accept']
    assert len(pending) == 8
    first_stage = dict(new_accepts=new[:], counts=dict(sorted(counts.items())), unresolved_queries=pending)
    source_arc_evidence = [frame_evidence(r['original_record'], Q, r['original_record']['bans']) for r in retained]
    assert not any(ev['eliminated'] for ev in source_arc_evidence)
    for r in retained:
        for n, t in enumerate(r['targets']):
            if t['status'] == 'accept':
                continue
            for case in t['cases']:
                ev = frame_evidence(r['original_record'], t['row'], case['forbidden_options'])
                ev['reflection'] = frame_reflection_audit(r['original_record'], t['row'], case['forbidden_options'], ev)
                case['frame_evidence'] = ev
                case['eliminated'] |= ev['eliminated']
            assert closes_target(t['cases'])
            t.update(status='accept', remaining_covers=[])
            new.append(dict(source_id=r['source_id'], target=n))
    assert len(new) == 12
    assert all(t['status'] == 'accept' for r in retained for t in r['targets'])
    cases = [c for r in retained for t in r['targets'] for c in t.get('cases', [])]
    stats = dict(complete_covers=len(cases), inherited_eliminated=sum(c['previous_evidence']['eliminated'] for c in cases),
                 newly_eliminated=sum(c['eliminated'] and not c['previous_evidence']['eliminated'] for c in cases))
    return dict(source_excluded=old['source_excluded'], new_source_excluded=0,
                source_retained=len(retained), counts={'accept/accept': len(retained)},
                new_accept_count=len(new), new_accepts=new, candidate_counts=stats,
                first_bridge_stage=first_stage,
                source_frame_audit=dict(count=len(source_arc_evidence), new_exclusions=0, sha256=digest(source_arc_evidence)),
                unresolved_queries=[], retained=retained)


def build():
    previous = json.loads(PREVIOUS.read_text())
    for path, expected in previous['inputs_sha256'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    algebra = algebra_controls()
    frames = frame_controls()
    names = ('c5_single_spoke_cores', 'c5_single_spoke_two_two_minor',
             'c5_single_spoke_two_two_external', 'c5_single_spoke_frame_arc',
             'c5_single_spoke_cross_row', 'c5_single_spoke_first_bridge',
             'c5_no_spoke_path_minor')
    paths = [Path(__file__), PREVIOUS] + [ROOT / 'scripts' / f'{n}.py' for n in names]
    return dict(schema=1, scope='paper first-bridge induction and original no-spoke K5; finite controls, not realizations or Lean',
        inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        inherited_inputs_sha256=previous['inputs_sha256'], table=refine_table(previous),
        algebra_controls=dict(sha256=digest(algebra), fixed_color_induction_count=algebra['fixed_color_induction_count'],
            endpoint_count=len(algebra['tight_endpoint']), first_edge_count=len(algebra['first_edge'])),
        support_controls=support_controls(), minor_controls=minor_controls(),
        frame_controls=frames, negative_controls=negative_controls(frames))


def render(result):
    table = result['table']
    lines = ['# No-spoke (2,2,1): first-bridge and frame-arc completion', '',
             'Generated by [checker](../../scripts/c5_no_spoke_first_bridge.py).',
             'Proof and scope: [report](../../docs/c5_no_spoke_first_bridge.md).', '',
             '500 inherited source exclusions; no new source exclusions; 116 retained.',
             '12 new target extensions: 4 by shared first-bridge beta, 8 by fixed frame arcs.',
             'All 116 records accept both targets; 0 unresolved queries.',
             'Necessary support records are not realizable source graphs.', '',
             '| Source record | Actual supports | q forbidden sets | p1 | p2 |',
             '| ---: | --- | --- | --- | --- |']
    for entry in table['retained']:
        r = entry['original_record']
        word = lambda xs: '/'.join(''.join(map(str, x)) for x in xs)
        lines.append(f"| {r['index']} | {word(r['supports'])} | {word(r['bans'])} | "
                     + ' | '.join(t['status'] for t in entry['targets']) + ' |')
    lines += ['', '## Remaining complete covers', '']
    lines += [f"- Record {r['source_id']}, p{r['target']+1}: `{r['remaining_covers']}`."
              for r in table['unresolved_queries']]
    if not table['unresolved_queries']:
        lines.append('None: every complete rejection candidate has been eliminated.')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    for path, payload in ((OUT, json.dumps(result, sort_keys=True, indent=2) + '\n'), (TABLE, render(result))):
        if args.check:
            assert path.read_bytes() == payload.encode(), f'certificate differs: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps({k: result['table'][k] for k in (
        'source_excluded', 'new_source_excluded', 'source_retained', 'counts', 'new_accept_count', 'candidate_counts')}, sort_keys=True))


if __name__ == '__main__':
    main()
