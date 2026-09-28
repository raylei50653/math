#!/usr/bin/env python3
"""Replay same-component cross-row residual constraints and target extensions.

Only double-forbidden rows share the proved path-bag residual identity.  This
adds a certificate layer to the immutable frame-arc table, not a graph search.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_single_spoke_two_two_minor import Q, U, PERMS, residual_audit, subsets, verify_minor
from c5_single_spoke_two_two_external import RHO, PI, STYLES, routes
from c5_single_spoke_frame_arc import (
    ROWS, admissible_supports, control, frame_arcs, verify_arcs, witnesses,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_single_spoke_two_two/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_single_spoke_frame_arc/observations.json'
OUT = ROOT / 'artifacts/c5_single_spoke_cross_row/observations.json'
TABLE = OUT.with_name('support_table.md')


@lru_cache(None)
def alignments(q, r, support):
    return tuple(p for p in PERMS if all(r[i] == p[q[i]] for i in support))


def cross_compatible(q, r, support, fq, fr):
    # Universal implication: no aligning permutation adds no restriction.
    return all({p[c] for c in fq} == set(fr)
               for p in alignments(tuple(q), tuple(r), tuple(sorted(support))))


def injection_check(q, r, support, fq, fr):
    """Independent check via all possible images of the unobserved colors."""
    partial = {}
    for i in support:
        if q[i] in partial and partial[q[i]] != r[i]:
            return True
        partial[q[i]] = r[i]
    if len(set(partial.values())) != len(partial):
        return True
    fixed = {partial[c] for c in fq if c in partial}
    free_count = len(set(fq) - partial.keys())
    images = [fixed | set(rest) for rest in
              combinations(sorted(U - set(partial.values())), free_count)]
    assert images
    return all(image == set(fr) for image in images)


@lru_cache(None)
def joint_supports(q, r, support, fq, fr):
    assert len(fq) == len(fr) == 2
    local = set(admissible_supports(q, support, fq)) & set(admissible_supports(r, support, fr))
    return tuple(t for t in subsets(support) if t in local and cross_compatible(q, r, t, fq, fr))


def component_evidence(q, r, support, fq, fr):
    if len(fq) != 2 or len(fr) != 2:
        return None  # No assertion of a singleton path-bag residual identity.
    q, r, support, fq, fr = map(tuple, (q, r, support, fq, fr))
    local = set(admissible_supports(q, support, fq)) & set(admissible_supports(r, support, fr))
    joint = joint_supports(q, r, support, fq, fr)
    removed = []
    for t in subsets(support):
        if t in local and t not in joint:
            bad = next(p for p in alignments(q, r, tuple(sorted(t)))
                       if {p[c] for c in fq} != set(fr))
            removed.append(dict(support=sorted(t), violating_permutation=bad,
                                moved_forbidden=sorted(bad[c] for c in fq)))
    forced = sorted(set.intersection(*map(set, joint))) if joint else []
    return dict(source_forbidden=fq, target_forbidden=fr,
                separate_row_supports=[sorted(t) for t in subsets(support) if t in local],
                joint_supports=[sorted(t) for t in joint], removed_supports=removed,
                forced_vertices=forced, no_possible_bag=not joint)


def support_audit():
    result = []
    for r, fq, fr, t in product(ROWS[1:], combinations(range(4), 2),
                                combinations(range(4), 2), subsets(range(5))):
        ps = alignments(Q, r, tuple(sorted(t)))
        ok = cross_compatible(Q, r, t, fq, fr)
        assert ok == injection_check(Q, r, t, fq, fr)
        result.append(dict(target_row=r, source_forbidden=fq, target_forbidden=fr,
                           support=sorted(t), alignment_count=len(ps), compatible=ok))
    assert len(result) == 2304
    return result


def algebra_audit():
    result = []
    # Each color is direct, in the off-path palette union, or residual.
    for direct, branches in product(subsets(U), repeat=2):
        if direct & branches:
            continue
        residual = U - direct - branches
        for p in PERMS:
            dr, qr = {p[c] for c in direct}, {p[c] for c in branches}
            er = U - dr - qr
            assert er == {p[c] for c in residual}
            result.append(dict(direct=sorted(direct), branches=sorted(branches),
                               permutation=p, residual=sorted(residual), moved_residual=sorted(er)))
    assert len(result) == 1944
    return result


def record16_audit():
    result = component_evidence(Q, ROWS[1], (1, 2, 3, 4), (2, 3), (2, 3))
    assert result['separate_row_supports'] == [[1, 2], [1, 2, 3], [1, 2, 4], [2, 3, 4], [1, 2, 3, 4]]
    assert result['joint_supports'] == [[1, 2], [1, 2, 3], [1, 2, 4], [1, 2, 3, 4]]
    assert result['removed_supports'] == [dict(support=[2, 3, 4],
        violating_permutation=(0, 2, 1, 3), moved_forbidden=[1, 3])]
    assert result['forced_vertices'] == [1, 2]
    result['examined_support_subsets'] = 16
    return result


def minor_controls():
    # Record 16's exact named arcs and original spoke, all edge positions.
    result = [control(length, i, i + 1, (1, 2), 0, styles, 0,
                      arcs=[[1], [2], [0, 3, 4]])
              for length in (1, 3, 5, 7, 9) for i in range(length)
              for styles in product(STYLES, repeat=2)]
    assert len(result) == 400
    return result


def closes_target(cases):
    return bool(cases) and all(c['eliminated'] for c in cases)


def negative_controls():
    base = control(1, 0, 1, (1, 2), 0, ('direct', 'direct'), 0,
                   arcs=[[1], [2], [0, 3, 4]])
    edges, bags = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    broken = [
        ('missing_original_spoke', edges - {('b0', 'z')}, bags),
        ('missing_tether', edges - {('b1', 'x0')}, bags),
        ('missing_original_bridge', edges - {('x0', 'x1')}, bags),
        ('missing_cycle_edge', edges - {('x0', 'z')}, bags),
        ('missing_frame_arc_edge', edges - {('b0', 'b4')}, bags),
        ('missing_frame_adjacency', edges - {('b1', 'b2')}, bags),
        ('overlapping_bags', edges, [bags[0] | {'z'}] + bags[1:]),
    ]
    result = []
    for name, es, bs in broken:
        try:
            verify_minor(es, bs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(f'negative control passed: {name}')
    assert alignments(Q, ROWS[1], (1, 2, 3)) == ()
    assert frozenset((1, 2, 3)) in joint_supports(Q, ROWS[1], (1, 2, 3, 4), (2, 3), (2, 3))
    result.append('no_alignment_is_vacuous_not_exclusion')
    ps = alignments(Q, ROWS[1], (2,))
    assert any({p[c] for c in (2, 3)} == {2, 3} for p in ps)
    assert not cross_compatible(Q, ROWS[1], (2,), (2, 3), (2, 3))
    result.append('one_alignment_is_not_enough')
    assert component_evidence(Q, ROWS[1], (1, 2, 3, 4), (2,), (2, 3)) is None
    assert component_evidence(Q, ROWS[1], (1, 2, 3, 4), (2, 3), (2,)) is None
    result.append('singleton_in_either_row_is_skipped')
    assert not closes_target([dict(eliminated=True), dict(eliminated=False)])
    assert not closes_target([])
    result.append('partial_or_empty_case_list_is_not_new_extension')
    # A valid transport can change the deleted z color and the root list.
    p = (0, 2, 1, 3)
    assert {p[c] for c in U - {2}} != U - {2}
    assert cross_compatible(Q, ROWS[1], (2, 3, 4), (2, 3), (1, 3))
    result.append('root_list_and_z_color_need_not_be_fixed')
    return result


def candidate_evidence(record, row, bans):
    components, new_witnesses = [], []
    for k, support in enumerate(record['supports']):
        ev = component_evidence(Q, row, support, record['bans'][k], bans[k])
        if ev is None:
            continue
        ev = dict(component=k, ordered_contacts=record['ordered_contacts'][k], **ev)
        components.append(ev)
        if ev['no_possible_bag']:
            new_witnesses.append(dict(kind='no_compatible_path_bag', component=k))
            continue
        for pair in combinations(ev['forced_vertices'], 2):
            for route in routes(record['spoke'], record['supports'][1-k], pair):
                arcs = frame_arcs(*pair, route['landing'])
                new_witnesses.append(dict(kind='cross_row_frame_arc_K5', component=k,
                    ordered_contacts=record['ordered_contacts'][k], forced_pair=pair,
                    frame_arcs=dict(X=arcs[0], Y=arcs[1], Z_frame=arcs[2]),
                    branch_set_recipe=dict(A=f'W_i in C{k}', A_prime=f'W_(i+1) in C{k}',
                        Z=f'(V(J_C{k}) minus x_i,x_(i+1)) union V(L) union Z_frame',
                        X=[f'b{i}' for i in arcs[0]], Y=[f'b{i}' for i in arcs[1]]),
                    external_component=1-k if route['mode']=='external_component' else None,
                    external_contact=(record['ordered_contacts'][1-k][0]
                                      if route['mode']=='external_component' else None), **route))
    old = witnesses(record, row, bans)
    separate_only = bool(old)
    for ev in components:
        supports = ev['separate_row_supports']
        forced = sorted(set.intersection(*map(set, supports))) if supports else []
        if not supports or any(routes(record['spoke'], record['supports'][1-ev['component']], pair)
                               for pair in combinations(forced, 2)):
            separate_only = True
    return dict(forbidden_options=bans, component_constraints=components,
                inherited_frame_arc_witnesses=old, cross_row_witnesses=new_witnesses,
                eliminated_without_cross_permutation=separate_only,
                eliminated=bool(old or new_witnesses))


def reflection_audit(record, row, bans, case):
    rr = record['reflection']
    raw = tuple(PI[row[RHO[i]]] for i in range(5))
    moved = [tuple(sorted(PI[c] for c in f)) for f in bans]
    assert tuple(PI[Q[RHO[i]]] for i in range(5)) == Q
    for ev in case['component_constraints']:
        k = ev['component']
        reflected = component_evidence(Q, raw, rr['supports'][k], rr['bans'][k], moved[k])
        for key in ('separate_row_supports', 'joint_supports'):
            assert {tuple(sorted(RHO[i] for i in t)) for t in ev[key]} == set(map(tuple, reflected[key]))
        assert sorted(RHO[i] for i in ev['forced_vertices']) == reflected['forced_vertices']
    for w in case['cross_row_witnesses']:
        if w['kind'] != 'cross_row_frame_arc_K5':
            continue
        pair = tuple(RHO[i] for i in w['forced_pair'])
        assert dict(mode=w['mode'], landing=RHO[w['landing']]) in routes(
            rr['spoke'], rr['supports'][1-w['component']], pair)
        arcs = [[RHO[i] for i in w['frame_arcs'][key]] for key in ('X', 'Y', 'Z_frame')]
        verify_arcs((*pair, RHO[w['landing']]), arcs)


def refine_table():
    source, previous = [json.loads(p.read_text()) for p in (SOURCE, PREVIOUS)]
    for path, digest in previous['source_sha256'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest
    by_id = {r['id']: r for r in source['records']}
    oldtable = previous['table']
    earlier = sorted(oldtable['previous_excluded_source_ids'] + [e['source_id'] for e in oldtable['excluded']])
    assert len(set(earlier)) == len(earlier) == 272
    assert len(oldtable['retained']) == 108 and oldtable['unresolved_queries'] == 66
    retained, newly_accepted = [], []
    scanned = 0
    for entry in oldtable['retained']:
        rid, r = entry['source_id'], entry['original_record']
        assert r == by_id[rid]
        targets = []
        for ti, previous_target in enumerate(entry['targets']):
            row = previous_target['row']
            assert r['reflection']['targets'][ti]['row'] == [PI[row[RHO[i]]] for i in range(5)]
            cases = []
            if previous_target['status'] == 'unresolved':
                scanned += 1
                target = r['targets'][ti]
                opts = [c['forbidden_options'] for c in target['components']]
                rejecting = [[f0, f1] for f0, f1 in product(*opts)
                             if U - {row[r['spoke']]} <= set(f0) | set(f1)]
                assert rejecting == target['rejection_options']
                assert rejecting == [c['forbidden_options'] for c in previous_target['rejection_cases']]
                for bans, oldcase in zip(rejecting, previous_target['rejection_cases']):
                    case = candidate_evidence(r, row, bans)
                    assert json.loads(json.dumps(case['inherited_frame_arc_witnesses'])) == oldcase['witnesses']
                    reflection_audit(r, row, bans, case)
                    cases.append(case)
                if closes_target(cases):
                    newly_accepted.append(dict(source_id=rid, target_index=ti, row=row))
            closed = closes_target(cases)
            targets.append(dict(row=row, previous_status=previous_target['status'],
                previous_target=previous_target, status='accept' if closed else previous_target['status'],
                rejection_cases=cases, justification='all_rejection_options_eliminated' if closed else 'inherited'))
        retained.append(dict(source_id=rid, original_record=r, targets=targets))
    assert scanned == 66
    key = lambda r: (r['spoke'], tuple(map(tuple, r['supports'])), tuple(map(tuple, r['bans'])))
    keyed = {key(e['original_record']): e for e in retained}
    for (s, supports, bans), e in keyed.items():
        other = keyed[s, supports[::-1], bans[::-1]]
        for a, b in zip(e['targets'], other['targets']):
            assert a['status'] == b['status']
            swapped = {tuple(map(tuple, c['forbidden_options'][::-1])): c['eliminated'] for c in a['rejection_cases']}
            assert swapped == {tuple(map(tuple, c['forbidden_options'])): c['eliminated'] for c in b['rejection_cases']}
    assert [e['source_id'] for e in retained] == oldtable['remaining_source_ids']
    r16 = next(e for e in retained if e['source_id'] == 16)
    assert [t['status'] for t in r16['targets']] == ['accept', 'accept']
    counts = Counter('/'.join(t['status'] for t in e['targets']) for e in retained)
    assert counts == {'accept/accept':74, 'accept/unresolved':8,
                      'unresolved/accept':10, 'unresolved/unresolved':16}
    assert [(e['source_id'], e['target_index']) for e in newly_accepted] == [
        (16, 0), (31, 1), (336, 1), (337, 0), (432, 0), (447, 0), (449, 1), (468, 0),
        (477, 0), (486, 0), (815, 0), (816, 0), (817, 0), (823, 1), (824, 0), (826, 0)]
    separate_only, partial = [], []
    allcases = []
    for e in retained:
        for ti, target in enumerate(e['targets']):
            cases = target['rejection_cases']
            allcases.extend(cases)
            if cases and all(c['eliminated_without_cross_permutation'] for c in cases):
                separate_only.append([e['source_id'], ti])
            if target['status']=='unresolved' and any(
                    c['eliminated'] and not c['inherited_frame_arc_witnesses'] for c in cases):
                partial.append([e['source_id'], ti])
    assert separate_only == [[31, 1], [336, 1]]
    assert partial == [[493, 0], [827, 0], [1111, 1], [1115, 0], [1515, 0], [1527, 1]]
    audit = dict(rejection_cases=len(allcases),
                 inherited_eliminated_cases=sum(bool(c['inherited_frame_arc_witnesses']) for c in allcases),
                 separate_rows_eliminated_cases=sum(c['eliminated_without_cross_permutation'] for c in allcases),
                 eliminated_cases=sum(c['eliminated'] for c in allcases),
                 separate_rows_new_extensions=separate_only, partially_pruned_unresolved_queries=partial)
    assert (audit['rejection_cases'], audit['inherited_eliminated_cases'],
            audit['separate_rows_eliminated_cases'], audit['eliminated_cases']) == (222, 126, 136, 168)
    return dict(previous_excluded_source_ids=earlier, newly_excluded_labeled=0,
                cumulative_excluded_labeled=272, remaining_labeled=108, remaining_component_swap_types=54,
                remaining_source_ids=oldtable['remaining_source_ids'], retained=retained,
                scanned_unresolved_queries=scanned, newly_accepted=newly_accepted, candidate_audit=audit,
                remaining_targets=dict(sorted(counts.items())),
                unresolved_queries=sum(t['status']=='unresolved' for e in retained for t in e['targets']),
                unresolved_records=sum(any(t['status']=='unresolved' for t in e['targets']) for e in retained))


def build():
    paths = [SOURCE, PREVIOUS, Path(__file__)] + [ROOT / 'scripts' / name for name in (
        'c5_single_spoke_frame_arc.py', 'c5_single_spoke_two_two_minor.py', 'c5_single_spoke_two_two_external.py')]
    return dict(scope='same-component double-forbidden cross-row paper lemma; finite controls; conditional extensions',
                source_sha256={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in paths},
                endpoint_residual_rows=residual_audit(), residual_transport_controls=algebra_audit(),
                support_controls=support_audit(), record16_support=record16_audit(),
                minor_controls=minor_controls(), negative_controls=negative_controls(), table=refine_table())


def support_table(result):
    table = result['table']
    lines = ['# (2,2) cross-row residual target extensions', '',
        'Generated by [checker](../../scripts/c5_single_spoke_cross_row.py);',
        'arbitrary-size proof and trust boundary: [report](../../docs/c5_single_spoke_cross_row.md).', '',
        'A = proved extension; ? = unresolved. Retained sources are not realizations.',
        'Original ordered relations, placements and raw reflected rows remain in JSON.', '',
        '| ID | p1 | p2 | newly proved | remaining rejection cases p1 / p2 |',
        '| ---: | --- | --- | --- | --- |']
    for e in table['retained']:
        ts = e['targets']
        labels = [{'accept':'A', 'unresolved':'?'}[t['status']] for t in ts]
        new = ', '.join(f'p{i+1}' for i, t in enumerate(ts) if t['status'] != t['previous_status'])
        cases = ' / '.join(str(sum(not c['eliminated'] for c in t['rejection_cases']))
                           if t['previous_status']=='unresolved' else 'inherited' for t in ts)
        lines.append(f"| {e['source_id']} | {labels[0]} | {labels[1]} | {new} | {cases} |")
    lines += ['', f"New target extensions: {len(table['newly_accepted'])}; new source exclusions: 0.",
              f"Remaining: 108 labeled sources / 54 swap types; {table['unresolved_records']} unresolved records / {table['unresolved_queries']} queries.",
              f"Target counts: {json.dumps(table['remaining_targets'], sort_keys=True)}.", '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    # One complete control per line; original table records remain readable.
    fields = []
    for key, value in sorted(result.items()):
        if key.endswith('_controls') and key != 'negative_controls':
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
    print(json.dumps(dict(residual_controls=len(result['residual_transport_controls']),
        support_controls=len(result['support_controls']), minor_controls=len(result['minor_controls']),
        negative_controls=len(result['negative_controls']), newly_accepted=len(result['table']['newly_accepted']),
        remaining_targets=result['table']['remaining_targets'], unresolved_queries=result['table']['unresolved_queries']), sort_keys=True))


if __name__ == '__main__':
    main()
