#!/usr/bin/env python3
"""Refine no-mixed t_z=t_w=2 targets using original bridges and frame arcs.

The source table is immutable. Paper palette induction and branch sets cover
arbitrary sources; these finite controls are neither disk realizations nor Lean.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2 import row_evidence
from c5_no_spoke_first_bridge import FRAME_PARTITIONS
from c5_single_spoke_cores import Q, TARGETS, U, PERMS, PI, RHO
from c5_single_spoke_first_bridge import fixed_colors, algebra_controls
from c5_single_spoke_frame_arc import admissible_supports, FRAME_EDGES, verify_arcs
from c5_single_spoke_two_two_external import STYLES
from c5_single_spoke_two_two_minor import connected, subsets, verify_minor, residual_audit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2/observations.json'
OUT = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_bridge/observations.json'
TABLE = OUT.with_name('support_table.md')
ROOTS = ('z', 'w')


def canonical(value):
    return json.loads(json.dumps(value, sort_keys=True))


def external_routes(supports, k):
    """Actual edges or an actual path inside the OTHER original unary."""
    root, other = ROOTS[k], ROOTS[1-k]
    routes = []
    for j in (1, 2):
        routes.append(dict(mode='own_spoke', landing=supports[3*k+j][0],
                           path=[root, f'b{supports[3*k+j][0]}']))
        h = supports[3*(1-k)+j][0]
        routes.append(dict(mode='other_spoke', landing=h, path=[root, other, f'b{h}']))
    for h in supports[3*(1-k)]:
        routes.append(dict(mode='other_component', landing=h,
                           path=[root, other, 'other0', f'b{h}'],
                           path_scope='other0...b_h is an original C_other path'))
    return routes


def frame_evidence(supports, k, family):
    if not family:
        return dict(supports=[], witnesses=[], eliminated=True, reason='no_possible_bag')
    witnesses = []
    for x, y, outside in FRAME_PARTITIONS:
        if not all(t & set(x) and t & set(y) for t in family):
            continue
        for route in external_routes(supports, k):
            if route['landing'] in outside:
                witnesses.append(dict(frame_arcs=[x, y, outside], route=route))
    return dict(supports=[sorted(t) for t in family], witnesses=witnesses,
                eliminated=bool(witnesses), reason='original_path_K5' if witnesses else 'unresolved')


def component_evidence(record, row, bans, k):
    f = bans[k]
    if len(f) != 2:
        return None  # Never apply a pair residual lemma to a singleton F.
    support = tuple(record['supports'][3*k])
    c = record['q']['joins'][0]['forbidden_sets'][k][0]
    family = admissible_supports(tuple(row), support, tuple(f))
    direct = frame_evidence(record['supports'], k, family)
    fixed = fixed_colors(Q, row, support)
    bridge = dict(applicable=c in fixed, fixed_colors=sorted(fixed), beta_cases=[], eliminated=False)
    if c in fixed:
        if c not in f:
            bridge.update(eliminated=True, reason='conserved_endpoint_color_absent')
        else:
            for beta in sorted(U - {c}):
                residual = tuple(sorted((c, beta)))
                if set(residual) & fixed != set(f) & fixed:
                    continue
                q_family = admissible_supports(Q, support, residual)
                common = tuple(t for t in family if t in q_family)
                bridge['beta_cases'].append(dict(beta=beta, source_residual=residual,
                    target_residual=f, frame=frame_evidence(record['supports'], k, common)))
            bridge.update(eliminated=all(b['frame']['eliminated'] for b in bridge['beta_cases']),
                          reason='all_shared_beta_cases')
    return dict(component=k, root=ROOTS[k], ordered_contacts=[f'C{ROOTS[k]}_0', f'C{ROOTS[k]}_1'],
                source_forbidden=[c], target_forbidden=f, direct_frame=direct, first_bridge=bridge,
                eliminated=direct['eliminated'] or bridge['eliminated'])


def evidence(record, row, bans):
    components = [c for k in range(2) if (c := component_evidence(record, row, bans, k)) is not None]
    return dict(components=components, eliminated=any(c['eliminated'] for c in components))


def reflection_audit(record, row, bans, ev, records):
    reflected = records[record['reflected_id']]
    raw = tuple(PI[row[RHO[i]]] for i in range(5))
    moved = [sorted(PI[c] for c in f) for f in bans]
    rev = evidence(reflected, raw, moved)
    assert ev['eliminated'] == rev['eliminated']

    def compare_frame(a, b):
        assert a['eliminated'] == b['eliminated']
        assert {tuple(sorted(RHO[i] for i in t)) for t in a['supports']} == set(map(tuple, b['supports']))
        keys = {(tuple(map(tuple, w['frame_arcs'])), w['route']['mode'], w['route']['landing'])
                for w in b['witnesses']}
        for w in a['witnesses']:
            arcs = tuple(tuple(sorted(RHO[i] for i in arc)) for arc in w['frame_arcs'])
            verify_arcs([arc[0] for arc in arcs], arcs)
            assert (arcs, w['route']['mode'], RHO[w['route']['landing']]) in keys

    for a, b in zip(ev['components'], rev['components'], strict=True):
        assert a['component'] == b['component'] and a['eliminated'] == b['eliminated']
        compare_frame(a['direct_frame'], b['direct_frame'])
        x, y = a['first_bridge'], b['first_bridge']
        assert x['applicable'] == y['applicable'] and x['eliminated'] == y['eliminated']
        assert {PI[c] for c in x['fixed_colors']} == set(y['fixed_colors'])
        by_beta = {bc['beta']: bc for bc in y['beta_cases']}
        assert {PI[bc['beta']] for bc in x['beta_cases']} == set(by_beta)
        for bc in x['beta_cases']:
            rc = by_beta[PI[bc['beta']]]
            assert {PI[c] for c in bc['source_residual']} == set(rc['source_residual'])
            compare_frame(bc['frame'], rc['frame'])
    return dict(raw_target=raw, transported_forbidden=moved, verified=True)


def minor_control(record, k, witness, length=1, styles=('direct', 'direct'), suppliers=None):
    """Both original roots, four spokes, two unaries; topology skeleton only."""
    assert length >= 1 and length % 2 == 1
    supports = record['supports']
    root, other = ROOTS[k], ROOTS[1-k]
    xarc, yarc, outside = witness['frame_arcs']
    edges = set()

    def edge(a, b):
        assert a != b
        edges.add(tuple(sorted((a, b))))

    for a, b in FRAME_EDGES:
        edge(f'b{a}', f'b{b}')
    edge('z', 'w')
    for j, r in enumerate(ROOTS):
        for s in supports[3*j+1:3*j+3]:
            edge(r, f'b{s[0]}')
    path = [f'x{i}' for i in range(length+1)]
    for a, b in zip([root] + path, path + [root]):
        edge(a, b)
    for a, b in ((other, 'other0'), ('other0', 'other1'), ('other1', other)):
        edge(a, b)
    for h in supports[3*(1-k)]:
        edge('other0', f'b{h}')
    possible = [sorted(set(supports[3*k]) & set(arc)) for arc in (xarc, yarc)]
    assert all(possible)
    suppliers = suppliers or [tuple(a[0] for a in possible)] * 2
    bags, routes = [], []
    for x, style, pair in zip(path[:2], styles, suppliers, strict=True):
        assert pair[0] in possible[0] and pair[1] in possible[1]
        a, b = (f'b{i}' for i in pair)
        if style == 'direct':
            tethers = [[x, a], [x, b]]
        elif style == 'shared_trunk':
            tethers = [[x, x+'_t', a], [x, x+'_t', b]]
        else:
            assert style in ('separate_bridges', 'shared_cycle')
            tethers = [[x, x+'_a', a], [x, x+'_b', b]]
            if style == 'shared_cycle':
                edge(x+'_a', x+'_b')
        bag = {x}
        for route in tethers:
            bag.update(route[:-1])
            for a, b in zip(route, route[1:]):
                edge(a, b)
        bags.append(bag)
        routes.append(tethers)
    # Keep the full actual support. These extra attachments do not enter Z.
    for h in supports[3*k]:
        edge('x0', f'b{h}')
    route = witness['route']['path']
    assert all(tuple(sorted(e)) in edges for e in zip(route, route[1:]))
    bags += [set(path[2:]) | set(route) | {f'b{i}' for i in outside},
             {f'b{i}' for i in xarc}, {f'b{i}' for i in yarc}]
    adjacencies = verify_minor(edges, bags)
    rename = lambda v: f'b{RHO[int(v[1:])]}' if v.startswith('b') else v
    reflected_edges = {tuple(sorted((rename(a), rename(b)))) for a, b in edges}
    reflected_bags = [{rename(v) for v in bag} for bag in bags]
    return dict(record_id=record['id'], component=k, length=length, styles=styles,
                suppliers=suppliers, original_external_route=witness['route'], frame_arcs=witness['frame_arcs'],
                edges=sorted(edges), branch_sets=[sorted(b) for b in bags], actual_tether_routes=routes,
                adjacencies=adjacencies, reflected_adjacencies=verify_minor(reflected_edges, reflected_bags),
                scope='topology skeleton, not a degree-list source')


def support_controls():
    partitions = set()
    for labels in product(range(3), repeat=5):
        arcs = tuple(tuple(i for i in range(5) if labels[i] == j) for j in range(3))
        if all(connected(set(arc), FRAME_EDGES) for arc in arcs):
            verify_arcs([arc[0] for arc in arcs], arcs)
            partitions.add(arcs)
    assert partitions == set(FRAME_PARTITIONS)
    controls = []
    for row, f, t in product((Q, *TARGETS), combinations(range(4), 2), subsets(range(5))):
        allowed = all({p[c] for c in f} == set(f) for p in PERMS
                      if all(p[row[i]] == row[i] for i in t))
        required = U - set(f) if 3 in f else set(f)
        assert allowed == (required <= {row[i] for i in t})
        assert allowed == (t in admissible_supports(row, tuple(sorted(t)), f))
        controls.append([row, f, sorted(t), allowed])
    assert len(controls) == 576
    return dict(frame_partitions=len(partitions), stabilizer_controls=controls,
                pair_residual_controls=residual_audit(), first_bridge_algebra=algebra_controls())


def negative_controls(records):
    result = []
    r = records[4]
    bans = [[1], [0, 3]]
    ev = evidence(r, TARGETS[0], bans)
    assert ev['eliminated'] and len(ev['components']) == 1
    assert component_evidence(r, TARGETS[0], [[1], [0]], 1) is None
    result.append('singleton_forbidden_is_not_a_pair_residual')
    c = component_evidence(records[5], TARGETS[1], bans, 1)
    assert not c['first_bridge']['applicable'] and not c['eliminated']
    result.append('nonconserved_source_color_does_not_force_shared_beta')
    target = records[43]['targets'][1]
    covers = [evidence(records[43], target['row'], j['forbidden_sets'])
              for j in target['joins'] if not j['root_pairs']]
    direct = [any(c['direct_frame']['eliminated'] for c in e['components']) for e in covers]
    assert any(direct) and not all(direct) and all(e['eliminated'] for e in covers)
    result.append('partial_direct_cover_needs_remaining_first_bridge_proof')
    assert frame_evidence(r['supports'], 1, ())['reason'] == 'no_possible_bag'
    assert not frame_evidence(r['supports'], 1, ())['witnesses']
    result.append('empty_family_is_not_a_vacuous_minor')
    family = admissible_supports(TARGETS[1], (1, 2, 3, 4), (0, 3))
    assert {1, 2} in family and {2, 3} in family and {3, 4} in family
    assert not frame_evidence(records[5]['supports'], 1, family)['eliminated']
    result.append('one_fixed_partition_must_work_for_all_supports')
    w = dict(frame_arcs=[(1, 2), (3, 4), (0,)],
             route=dict(mode='other_spoke', landing=0, path=['w', 'z', 'b0']))
    control = minor_control(r, 1, w)
    edges, bags = set(map(tuple, control['edges'])), list(map(set, control['branch_sets']))
    for name, es, bs in (
        ('original_zw_required_by_this_route', edges - {('w', 'z')}, bags),
        ('original_spoke_required_by_this_route', edges - {('b0', 'z')}, bags),
        ('original_bridge_required', edges - {('x0', 'x1')}, bags),
        ('actual_supplier_required', edges - {('b1', 'x1')}, bags),
        ('branch_sets_must_be_disjoint', edges, [bags[0] | {'w'}] + bags[1:]),
    ):
        try:
            verify_minor(es, bs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    w = dict(frame_arcs=[(1,), (2, 3), (0, 4)],
             route=dict(mode='own_spoke', landing=4, path=['w', 'b4']))
    control = minor_control(r, 1, w)
    try:
        verify_minor(set(map(tuple, control['edges'])) - {('b0', 'b4')},
                     list(map(set, control['branch_sets'])))
    except AssertionError:
        result.append('outside_frame_arc_must_be_connected')
    else:
        raise AssertionError('disconnected frame arc accepted')
    # Record 54 supplies two individually possible supports that cannot use
    # the same beta on the first bridge; the local source E is not F(q)={3}.
    bridge = component_evidence(records[54], TARGETS[1], [[0, 3], [0, 3]], 1)['first_bridge']
    families = {b['beta']: set(map(tuple, b['frame']['supports'])) for b in bridge['beta_cases']}
    assert (3, 4) in families[0] and (2, 3) in families[2]
    assert not any({(3, 4), (2, 3)} <= family for family in families.values())
    assert all(len(b['source_residual']) == 2 for b in bridge['beta_cases'])
    result.append('different_endpoint_betas_are_not_one_edge_palette')
    return result


def build():
    data = json.loads(SOURCE.read_text())
    assert data['source_sha256'] == sha256((ROOT/'scripts/c5_adjacent_degree5_no_mixed_t2.py').read_bytes()).hexdigest()
    assert data['original_source_sha256'] == sha256((ROOT/data['original_source_path']).read_bytes()).hexdigest()
    for path, digest in data['inputs_sha256'].items():
        assert digest == sha256((ROOT/path).read_bytes()).hexdigest()
    assert [r['id'] for r in data['records']] == list(range(322))
    inherited_accepts = sum(t['status'] == 'accept' for r in data['records'] for t in r['targets'])
    assert inherited_accepts == 512
    records, controls, used_controls = [], [], set()
    stages = Counter()
    failing_joins = 0
    reflection_count = 0
    for r in data['records']:
        source = data['original_records'][r['source_id']]
        targets = []
        for n, target in enumerate(r['targets']):
            # Recompute every full F-product join, keeping the original root pair.
            fresh = row_evidence(source, tuple(map(tuple, r['supports'])), tuple(target['row']))
            assert canonical(fresh) == target
            cases = []
            for j, join in enumerate(target['joins']):
                if join['root_pairs']:
                    continue
                failing_joins += 1
                ev = evidence(r, target['row'], join['forbidden_sets'])
                reflected = reflection_audit(r, target['row'], join['forbidden_sets'], ev, data['records'])
                reflection_count += 1
                for c in ev['components']:
                    frames = [c['direct_frame']] + [bc['frame'] for bc in c['first_bridge']['beta_cases']]
                    for f in frames:
                        if f['witnesses']:
                            witness = f['witnesses'][0]
                            key = json.dumps([r['id'], c['component'], witness], sort_keys=True)
                            if key not in used_controls:
                                used_controls.add(key)
                                controls.append(minor_control(r, c['component'], witness))
                direct = any(c['direct_frame']['eliminated'] for c in ev['components'])
                cases.append(dict(original_join_index=j, original_join=join, evidence=ev,
                                  direct_eliminated=direct, eliminated=ev['eliminated'], reflection=reflected))
            direct_closed = all(c['direct_eliminated'] for c in cases)
            closed = all(c['eliminated'] for c in cases)
            stages['direct_accepts'] += direct_closed
            stages['final_accepts'] += closed
            targets.append(dict(row=target['row'], inherited_accept=target['status'] == 'accept',
                direct_status='accept' if direct_closed else 'unresolved',
                status='accept' if closed else 'unresolved', cases=cases,
                remaining_candidates=[c['original_join'] for c in cases if not c['eliminated']]))
        records.append(dict(id=r['id'], original_record=r,
                            original_geometry=data['geometries'][r['geometry_id']], targets=targets))
    counts = Counter('/'.join(t['status'] for t in r['targets']) for r in records)
    assert counts == {'accept/accept': 258, 'accept/unresolved': 32, 'unresolved/accept': 32}
    for entry in records:
        r = entry['original_record']
        other = records[r['root_swapped_id']]
        assert [t['status'] for t in entry['targets']] == [t['status'] for t in other['targets']]
        for a, b in zip(entry['targets'], other['targets'], strict=True):
            assert {(tuple(map(tuple, c['original_join']['forbidden_sets'][::-1])), c['eliminated']) for c in a['cases']} == {
                (tuple(map(tuple, c['original_join']['forbidden_sets'])), c['eliminated']) for c in b['cases']}
    pending = [dict(record_id=r['id'], target_index=i, row=t['row'], candidates=t['remaining_candidates'])
               for r in records for i, t in enumerate(r['targets']) if t['status'] == 'unresolved']
    assert len(pending) == 64 and pending[0]['record_id'] == 5 and pending[0]['target_index'] == 1
    # Stress the composed branch sets on record 4: all external route modes,
    # odd path lengths, both tether shapes, and independent boundary suppliers.
    r = data['records'][4]
    direct = evidence(r, TARGETS[0], [[1], [0, 3]])['components'][0]['direct_frame']
    for mode in ('own_spoke', 'other_spoke', 'other_component'):
        w = next(w for w in direct['witnesses'] if w['route']['mode'] == mode)
        pairs = list(product(*(sorted(set(r['supports'][3]) & set(a)) for a in w['frame_arcs'][:2])))
        for length, styles, p0, p1 in product((1, 3, 5), product(STYLES, repeat=2), pairs, pairs):
            controls.append(minor_control(r, 1, w, length, styles, [p0, p1]))
    negatives = negative_controls(data['records'])
    summary = dict(original_records=322, original_source_exclusions=0, new_source_exclusions=0,
        target_queries=644, inherited_accepts=inherited_accepts, original_unresolved=132,
        original_failing_joins=failing_joins, direct_frame_accepts=stages['direct_accepts'],
        new_accepts=stages['final_accepts']-512, final_accepts=stages['final_accepts'],
        unresolved_queries=len(pending), both_targets_proved=258, target_classes=dict(sorted(counts.items())),
        eliminated_failing_joins=sum(c['eliminated'] for r in records for t in r['targets'] for c in t['cases']),
        root_swap_checks=len(records), literal_reflection_checks=reflection_count,
        minor_controls=len(controls), negative_controls=len(negatives))
    assert summary['new_accepts'] == 68 and summary['original_failing_joins'] == 160
    assert summary['direct_frame_accepts'] == 556 and summary['eliminated_failing_joins'] == 96
    inputs = ['scripts/c5_adjacent_degree5_no_mixed_t2.py', 'scripts/c5_no_spoke_first_bridge.py',
              'scripts/c5_single_spoke_first_bridge.py', 'scripts/c5_single_spoke_frame_arc.py',
              'scripts/c5_single_spoke_two_two_minor.py', 'scripts/c5_single_spoke_two_two_external.py',
              'scripts/c5_single_spoke_cores.py']
    return dict(schema=1, scope='necessary support refinement, partial targets; no disk realizations or Lean theorem',
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        original_source_path=str(SOURCE.relative_to(ROOT)), original_source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
        inputs_sha256={p: sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
        original_frontier=data['original_records'], source_fibers=data['source_fibers'],
        q_complete_schemas=data['q_complete_schemas'], rotation_templates=data['rotation_templates'],
        summary=summary, records=records, open_queries=pending,
        algebra_controls=support_controls(), minor_controls=controls, negative_controls=negatives)


def render(data):
    lines = ['# 無 mixed 兩側 t=2：原 bridge 與固定框弧套表', '',
             '原 322 份必要資料皆保留，新增 68 個指定列延拓，剩 64 個查詢未決。',
             'A 為已證接受，? 為上界候選未決；必要資料及 minor skeletons 均非 disk 實現。', '',
             '| 原 ID | 原 sides | actual supports：Cz/z0/z1/Cw/w0/w1 | 原 p₁/p₂ | 本輪 p₁/p₂ |',
             '| ---: | --- | --- | --- | --- |']
    mark = lambda ts: '/'.join('A' if t['status'] == 'accept' else '?' for t in ts)
    for r in data['records']:
        old = r['original_record']
        supports = '/'.join(''.join(map(str, s)) for s in old['supports'])
        lines.append(f"| {r['id']} | {old['source_side_ids']} | {supports} | {mark(old['targets'])} | {mark(r['targets'])} |")
    lines += ['', '完整同源記錄、schemas、placements、rotations、160 份失敗候選、',
              '首橋共用 β 與固定框弧 witnesses 見 [JSON](observations.json)。',
              '紙面論證與精確停止點見 [研究報告](../../docs/c5_adjacent_degree5_no_mixed_t2_bridge.md)。', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    for path, payload in ((OUT, json.dumps(result, sort_keys=True, indent=2)+'\n'), (TABLE, render(result))):
        if args.check:
            assert path.read_bytes() == payload.encode(), f'certificate differs: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
