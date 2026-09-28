#!/usr/bin/env python3
"""No-spoke path-bag K5 exclusions and same-component target refinements.

The arbitrary-size extraction is a paper proof.  Controls are topology
skeletons, not degree-list sources or disk-realizability certificates.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_single_spoke_cores import Q, TARGETS, U, PI, RHO
from c5_single_spoke_two_two_minor import connected, residual_audit, verify_minor
from c5_single_spoke_two_two_external import STYLES
from c5_single_spoke_frame_arc import (
    admissible_supports, control, frame_arcs, support_audit, verify_arcs,
)
from c5_single_spoke_cross_row import (
    algebra_audit, closes_target, component_evidence, joint_supports,
    support_audit as cross_support_audit,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_no_spoke_supports/observations.json'
OUT = ROOT / 'artifacts/c5_no_spoke_path_minor/observations.json'
TABLE = OUT.with_name('support_table.md')


def canonical(value):
    return json.loads(json.dumps(value))


def digest(value):
    return sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def evidence(record, row, bans, cross=True):
    """All constraints on entire path bags; all external routes are original."""
    constraints, witnesses = [], []
    for k, f in enumerate(bans):
        if len(f) != 2:
            continue
        assert record['parts'][k] == 2
        support, f = tuple(record['supports'][k]), tuple(f)
        source_f = tuple(record['bans'][k])
        local = admissible_supports(tuple(row), support, f)
        ev = None
        if tuple(row) != Q and len(source_f) == 2:
            ev = component_evidence(Q, row, support, source_f, f)
            local = ev['joint_supports' if cross else 'separate_row_supports']
        local = [sorted(t) for t in local]
        forced = sorted(set.intersection(*map(set, local))) if local else []
        constraints.append(dict(component=k, ordered_contacts=[f'c{k}p0', f'c{k}p1'],
                                forbidden=f, allowed_bag_supports=local,
                                forced_vertices=forced, cross_row=ev))
        if not local:
            witnesses.append(dict(kind='no_possible_path_bag', component=k))
            continue
        for pair in combinations(forced, 2):
            for j, other in enumerate(record['supports']):
                if j == k:
                    continue
                for h in sorted(set(other) - set(pair)):
                    arcs = frame_arcs(*pair, h)
                    witnesses.append(dict(kind='original_external_path_K5', component=k,
                        ordered_contacts=[f'c{k}p0', f'c{k}p1'], forced_pair=pair,
                        external_component=j, external_contact=f'c{j}p0', landing=h,
                        frame_arcs=arcs,
                        branch_set_recipe=[f'W_i in C{k}', f'W_(i+1) in C{k}',
                            f'(J_C{k} minus x_i,x_(i+1)) union original C{j} route union Z_frame',
                            'X_frame', 'Y_frame']))
    return dict(forbidden_options=bans, constraints=constraints, witnesses=witnesses,
                eliminated=bool(witnesses))


def reflection_audit(record, row, bans, result):
    rr = dict(record, supports=record['reflection']['supports'],
              bans=record['reflection']['bans'])
    raw = tuple(PI[row[RHO[i]]] for i in range(5))
    moved = [sorted(PI[c] for c in f) for f in bans]
    reflected = evidence(rr, raw, moved)
    assert reflected['eliminated'] == result['eliminated']
    for a, b in zip(result['constraints'], reflected['constraints']):
        assert a['component'] == b['component']
        assert {tuple(sorted(RHO[i] for i in t)) for t in a['allowed_bag_supports']} == {
            tuple(t) for t in b['allowed_bag_supports']}
        assert sorted(RHO[i] for i in a['forced_vertices']) == b['forced_vertices']
    for w in result['witnesses']:
        if w['kind'] != 'original_external_path_K5':
            continue
        marks = [RHO[i] for i in (*w['forced_pair'], w['landing'])]
        verify_arcs(marks, [[RHO[i] for i in arc] for arc in w['frame_arcs']])
        assert marks[2] in rr['supports'][w['external_component']]
        assert w['external_component'] != w['component']
    return dict(raw_row=raw, forbidden_options=moved,
                eliminated=reflected['eliminated'])


def no_spoke_control(length, index, pair, landing, styles, external_arity=2, size=2):
    assert length % 2 == 1 and size >= 1 and external_arity in (1, 2)
    r = control(length, index, index + 1, pair, landing, styles, size)
    edges = set(map(tuple, r['edges']))

    def edge(a, b):
        edges.add(tuple(sorted((a, b))))

    # Retain all five contacts and the third original component. Extra
    # contacts are not needed by this particular minor witness.
    ports = [[f'x0', f'x{length}'], ['e0'], ['f0']]
    if external_arity == 2:
        edge('d1', 'z')
        edge('d1', 'e0')
        ports[1].append('d1')
    else:
        edge('f0', 'f1')
        edge('f1', 'z')
        ports[2].append('f1')
    edge('f0', 'z')
    edge('f0', f'b{landing}')
    external = {f'e{i}' for i in range(size)} | ({'d1'} if external_arity == 2 else set())
    third = {'f0'} | ({'f1'} if external_arity == 1 else set())
    vertices = set().union(*map(set, edges))
    interior = vertices - {'z'} - {f'b{i}' for i in range(5)}
    components = [interior - external - third, external, third]
    assert sorted(map(len, ports)) == [1, 2, 2]
    assert {v if u == 'z' else u for u, v in edges if 'z' in (u, v)} == set(sum(ports, []))
    assert all(connected(c, edges) for c in components)
    assert all(not any((u in a and v in b) or (v in a and u in b) for u, v in edges)
               for a, b in combinations(components, 2))
    bags = list(map(set, r['branch_sets']))
    r.update(edges=sorted(edges), adjacencies=verify_minor(edges, bags),
             component_vertices=[sorted(c) for c in components], ordered_contacts=ports,
             external_arity=external_arity, scope='topology skeleton only')
    rename = lambda v: f'b{RHO[int(v[1:])]}' if v.startswith('b') else v
    reflected_edges = {tuple(sorted((rename(u), rename(v)))) for u, v in edges}
    reflected_bags = [{rename(v) for v in b} for b in bags]
    r['reflected_adjacencies'] = verify_minor(reflected_edges, reflected_bags)
    return r


def minor_controls():
    result = [no_spoke_control(length, i, (a, b), h, ('direct', 'direct'), arity)
              for a, b, h in permutations(range(5), 3)
              for length in (1, 3, 5) for i in range(length) for arity in (1, 2)]
    result += [no_spoke_control(length, i, (0, 4), 1, styles, 2, size)
               for length in (1, 3, 5) for i in range(length)
               for styles in product(STYLES, repeat=2) for size in (1, 3)]
    assert len(result) == 1368
    return result


def negative_controls():
    r = no_spoke_control(1, 0, (0, 4), 1, ('direct', 'direct'))
    edges, bags = set(map(tuple, r['edges'])), list(map(set, r['branch_sets']))
    broken = [
        ('missing_original_external_contact', edges - {('e0', 'z')}, bags),
        ('missing_external_boundary_edge', edges - {('b1', 'e1')}, bags),
        ('missing_tether', edges - {('b0', 'x0')}, bags),
        ('missing_bridge', edges - {('x0', 'x1')}, bags),
        ('missing_cycle_contact', edges - {('x0', 'z')}, bags),
        ('disconnected_frame_arc', edges - {('b1', 'b2')}, bags),
        ('missing_frame_adjacency', edges - {('b0', 'b4')}, bags),
        ('overlapping_bags', edges, [bags[0] | {'z'}] + bags[1:]),
    ]
    result = []
    for name, es, bs in broken:
        try:
            verify_minor(es, bs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    dummy = dict(parts=[2, 2, 1], supports=[[0, 4]] * 3, bans=[[0, 2], [1], [3]])
    assert not evidence(dummy, Q, dummy['bans'])['eliminated']
    result.append('no_distinct_external_landing_is_not_a_witness')
    assert component_evidence(Q, TARGETS[0], (0, 1, 4), (0,), (0, 1)) is None
    result.append('singleton_source_has_no_pair_cross_row_identity')
    assert frozenset((1, 2, 3)) in joint_supports(Q, TARGETS[0], (1, 2, 3, 4), (2, 3), (2, 3))
    result.append('non_alignment_is_vacuous')
    assert not closes_target([dict(eliminated=True), dict(eliminated=False)])
    assert not closes_target([])
    result.append('one_remaining_cover_prevents_acceptance')
    return result


def refine_table(source):
    records = [r for r in source['records'] if r['parts'] == [2, 2, 1] and r['status'] == 'retained']
    assert len(records) == 616
    excluded, retained, new = [], [], []
    stats = Counter()
    for r in records:
        base = evidence(r, Q, r['bans'])
        base['reflection'] = reflection_audit(r, Q, r['bans'], base)
        if base['eliminated']:
            excluded.append(dict(source_id=r['index'], original_record=r, source_evidence=base))
            stats['excluded_old_' + '/'.join(t['status'] for t in r['targets'])] += 1
            continue
        targets = []
        for n, t in enumerate(r['targets']):
            choices = product(*(c['options'] for c in t['components']))
            covers = [fs for fs in choices if set().union(*map(set, fs)) == U]
            assert bool(covers) == (t['status'] != 'accept')
            assert t['necessary_cover_if_rejected'] == (canonical(covers[0]) if covers else None)
            cases = []
            for fs in covers:
                ev = evidence(r, t['row'], fs)
                ev['reflection'] = reflection_audit(r, t['row'], fs, ev)
                ev['eliminated_without_cross_permutation'] = evidence(r, t['row'], fs, cross=False)['eliminated']
                cases.append(ev)
            closed = closes_target(cases)
            # A previous exact rejection plus a minor would exclude the source,
            # not prove a target extension. No such record survives q here.
            assert t['status'] != 'reject'
            status = 'accept' if closed else t['status']
            if closed:
                without_cross = all(c['eliminated_without_cross_permutation'] for c in cases)
                new.append(dict(source_id=r['index'], target=n, needs_cross_permutation=not without_cross))
            targets.append(dict(row=t['row'], previous=t, status=status, cases=cases,
                                remaining_covers=[c['forbidden_options'] for c in cases if not c['eliminated']]))
        retained.append(dict(source_id=r['index'], original_record=r,
                             source_evidence=base, targets=targets))
    counts = Counter('/'.join(t['status'] for t in r['targets']) for r in retained)
    assert len(excluded) == 500 and len(retained) == 116 and len(new) == 104
    assert counts == {'accept/accept': 108, 'accept/unresolved': 2,
                      'unresolved/accept': 2, 'unresolved/unresolved': 4}
    assert sum(n['needs_cross_permutation'] for n in new) == 16
    # Swapping the two original binary components never swaps their coordinates.
    key = lambda r: (tuple(map(tuple, r['bans'])), tuple(map(tuple, r['supports'])))
    lookup = {key(r): r['index'] for r in records}
    states = {r['source_id']: ('excluded',) for r in excluded}
    states.update({r['source_id']: tuple(t['status'] for t in r['targets']) for r in retained})
    for r in records:
        swapped = dict(r, bans=[r['bans'][1], r['bans'][0], r['bans'][2]],
                       supports=[r['supports'][1], r['supports'][0], r['supports'][2]])
        assert states[r['index']] == states[lookup[key(swapped)]]
    pending = [dict(source_id=r['source_id'], target=n, remaining_covers=t['remaining_covers'])
               for r in retained for n, t in enumerate(r['targets']) if t['status'] != 'accept']
    assert len(pending) == 12
    return dict(input_records=616, source_excluded=500, source_retained=116,
                counts=dict(sorted(counts.items())), excluded_previous_status_counts=dict(sorted(stats.items())),
                new_accepts=new, new_accept_count=len(new), unresolved_queries=pending,
                excluded=excluded, retained=retained)


def build():
    source = json.loads(SOURCE.read_text())
    for path, expected in source['inputs_sha256'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    table = refine_table(source)
    record599 = next(r for r in table['excluded'] if r['source_id'] == 599)
    assert record599['source_evidence']['constraints'][1]['allowed_bag_supports'] == [[0, 4]]
    assert any(w['component'] == 1 and w['external_component'] == 0 and w['landing'] == 1
               for w in record599['source_evidence']['witnesses'])
    audits = {}
    for name, fn in [('residual', residual_audit), ('single_row_support', support_audit),
                     ('cross_row_support', cross_support_audit), ('residual_algebra', algebra_audit)]:
        data = fn()
        audits[name] = dict(count=len(data), sha256=digest(data))
    paths = [Path(__file__), SOURCE] + [ROOT / 'scripts' / f'{name}.py' for name in (
        'c5_single_spoke_cores', 'c5_single_spoke_two_two_minor',
        'c5_single_spoke_two_two_external', 'c5_single_spoke_frame_arc',
        'c5_single_spoke_cross_row')]
    return dict(schema=1, scope='arbitrary-size paper K5 extraction, finite controls; no disk realizability or new Lean theorem',
                inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
                inherited_inputs_sha256=source['inputs_sha256'], table=table,
                algebra_controls=audits, minor_controls=minor_controls(), negative_controls=negative_controls())


def render(result):
    table = result['table']
    lines = ['# No-spoke (2,2,1): path-bag refinement', '',
             'Generated by [checker](../../scripts/c5_no_spoke_path_minor.py).',
             'Proof and scope: [report](../../docs/c5_no_spoke_path_minor.md).', '',
             '500 source exclusions; 116 retained; 108 accept both targets; 12 unresolved queries.',
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
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payloads = [(OUT, json.dumps(result, sort_keys=True, indent=2) + '\n'), (TABLE, render(result))]
    for path, payload in payloads:
        if args.check:
            assert path.read_text() == payload, f'certificate differs: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps({k: result['table'][k] for k in (
        'source_excluded', 'source_retained', 'counts', 'new_accept_count')}, sort_keys=True))


if __name__ == '__main__':
    main()
