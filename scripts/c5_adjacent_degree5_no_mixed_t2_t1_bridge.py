#!/usr/bin/env python3
"""Refine the immutable t_z=2, t_w=1 table with original-path K5 witnesses.

Three original components, five contacts, three spokes and zw are retained.
The report proves arbitrary-size coverage; finite controls are not sources.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2_t1 import COMPONENTS, row_evidence
from c5_adjacent_degree5_no_mixed_t2_bridge import canonical, support_controls
from c5_no_spoke_first_bridge import FRAME_PARTITIONS
from c5_single_spoke_cores import Q, TARGETS, U, PI, RHO
from c5_single_spoke_first_bridge import fixed_colors
from c5_single_spoke_frame_arc import admissible_supports, FRAME_EDGES, verify_arcs
from c5_single_spoke_two_two_external import STYLES
from c5_single_spoke_two_two_minor import verify_minor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_t1/observations.json'
OUT = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_t1_bridge/observations.json'
TABLE = OUT.with_name('support_table.md')


def context(record, source):
    return dict(record_id=record['id'],
        root_boundary={r: source[r]['root_boundary'] for r in ('z', 'w')},
        components=[dict(name=name, root=root, support=record['supports'][pos],
                         contacts=[f'{name}_{i}' for i in range(k)],
                         source_forbidden=source[root]['forbidden'][col])
                    for name, root, col, pos, k in COMPONENTS])


def external_routes(ctx, k):
    """Every route uses original edges, with a named component if needed."""
    root = ctx['components'][k]['root']
    routes = []
    for owner, support in ctx['root_boundary'].items():
        prefix = [root] if owner == root else [root, owner]
        for h in support:
            routes.append(dict(mode='own_spoke' if owner == root else 'other_spoke',
                component=None, landing=h, path=prefix + [f'b{h}']))
    for j, comp in enumerate(ctx['components']):
        if j == k:
            continue
        prefix = [root] if comp['root'] == root else [root, comp['root']]
        for h in comp['support']:
            routes.append(dict(mode='same_root_component' if comp['root'] == root else 'other_root_component',
                component=comp['name'], landing=h,
                path=prefix + [comp['contacts'][0], f'b{h}'],
                path_scope='last segment abbreviates an original component path, ending at its first boundary vertex'))
    return routes


def frame_evidence(ctx, k, family):
    if not family:
        return dict(supports=[], witnesses=[], eliminated=True, reason='no_possible_bag')
    witnesses = [dict(frame_arcs=[x, y, outside], route=route)
        for x, y, outside in FRAME_PARTITIONS
        if all(t & set(x) and t & set(y) for t in family)
        for route in external_routes(ctx, k) if route['landing'] in outside]
    return dict(supports=[sorted(t) for t in family], witnesses=witnesses,
                eliminated=bool(witnesses), reason='original_path_K5' if witnesses else 'unresolved')


def component_evidence(ctx, row, bans, k):
    comp, f = ctx['components'][k], bans[k]
    if len(comp['contacts']) != 2 or len(f) != 2:
        return None
    support = tuple(comp['support'])
    assert len(comp['source_forbidden']) == 1
    d = comp['source_forbidden'][0]
    family = admissible_supports(tuple(row), support, tuple(f))
    direct = frame_evidence(ctx, k, family)
    fixed = fixed_colors(Q, row, support)
    bridge = dict(applicable=d in fixed, fixed_colors=sorted(fixed), beta_cases=[], eliminated=False)
    if d in fixed:
        if d not in f:
            bridge.update(eliminated=True, reason='conserved_endpoint_color_absent')
        else:
            for beta in sorted(U - {d}):
                residual = tuple(sorted((d, beta)))
                if set(residual) & fixed != set(f) & fixed:
                    continue
                q_family = admissible_supports(Q, support, residual)
                common = tuple(t for t in family if t in q_family)
                bridge['beta_cases'].append(dict(beta=beta, source_residual=residual,
                    target_residual=f, frame=frame_evidence(ctx, k, common)))
            bridge.update(eliminated=all(b['frame']['eliminated'] for b in bridge['beta_cases']),
                          reason='all_shared_beta_cases')
    return dict(component=k, name=comp['name'], root=comp['root'], ordered_contacts=comp['contacts'],
        source_forbidden=[d], target_forbidden=f, direct_frame=direct, first_bridge=bridge,
        eliminated=direct['eliminated'] or bridge['eliminated'])


def evidence(ctx, row, bans):
    components = [ev for k in range(3) if (ev := component_evidence(ctx, row, bans, k)) is not None]
    direct = any(c['direct_frame']['eliminated'] for c in components)
    eliminated = any(c['eliminated'] for c in components)
    return dict(components=components, eliminated=eliminated,
                closure_reason='fixed_frame_original_path' if direct else
                'shared_first_bridge' if eliminated else None)


def root_pairs(ctx, row, bans):
    return [(a, b) for a, b in product(range(4), repeat=2) if a != b
            and all(color != row[h] for root, color in (('z', a), ('w', b))
                    for h in ctx['root_boundary'][root])
            and all((a if c['root'] == 'z' else b) not in f
                    for c, f in zip(ctx['components'], bans, strict=True))]


def swapped(ctx):
    swap = {'z': 'w', 'w': 'z'}
    return dict(ctx, root_boundary={swap[r]: s for r, s in ctx['root_boundary'].items()},
                components=[dict(c, root=swap[c['root']]) for c in ctx['components']])


def symmetry_audit(ctx, row, bans, ev, reflected):
    raw = tuple(PI[row[RHO[i]]] for i in range(5))
    moved = [sorted(PI[c] for c in f) for f in bans]
    rev = evidence(reflected, raw, moved)
    assert (ev['eliminated'], ev['closure_reason']) == (rev['eliminated'], rev['closure_reason'])

    def compare_frame(a, b):
        assert a['eliminated'] == b['eliminated']
        assert {tuple(sorted(RHO[i] for i in t)) for t in a['supports']} == set(map(tuple, b['supports']))
        keys = {(tuple(map(tuple, w['frame_arcs'])), w['route']['mode'],
                 w['route']['component'], w['route']['landing']) for w in b['witnesses']}
        for w in a['witnesses']:
            arcs = tuple(tuple(sorted(RHO[i] for i in arc)) for arc in w['frame_arcs'])
            verify_arcs([arc[0] for arc in arcs], arcs)
            assert (arcs, w['route']['mode'], w['route']['component'], RHO[w['route']['landing']]) in keys

    for a, b in zip(ev['components'], rev['components'], strict=True):
        assert a['component'] == b['component'] and a['eliminated'] == b['eliminated']
        compare_frame(a['direct_frame'], b['direct_frame'])
        x, y = a['first_bridge'], b['first_bridge']
        assert (x['applicable'], x['eliminated']) == (y['applicable'], y['eliminated'])
        assert {PI[c] for c in x['fixed_colors']} == set(y['fixed_colors'])
        betas = {c['beta']: c for c in y['beta_cases']}
        assert {PI[c['beta']] for c in x['beta_cases']} == set(betas)
        for bc in x['beta_cases']:
            rc = betas[PI[bc['beta']]]
            assert {PI[c] for c in bc['source_residual']} == set(rc['source_residual'])
            compare_frame(bc['frame'], rc['frame'])
    sw = evidence(swapped(ctx), row, bans)
    assert (ev['eliminated'], ev['closure_reason']) == (sw['eliminated'], sw['closure_reason'])
    for a, b in zip(ev['components'], sw['components'], strict=True):
        assert a['name'] == b['name'] and a['root'] != b['root']
        for fa, fb in [(a['direct_frame'], b['direct_frame'])] + [
                (x['frame'], y['frame']) for x, y in zip(
                    a['first_bridge']['beta_cases'], b['first_bridge']['beta_cases'], strict=True)]:
            renamed = canonical(fa)
            for witness in renamed['witnesses']:
                witness['route']['path'] = [dict(z='w', w='z').get(v, v) for v in witness['route']['path']]
            assert renamed == canonical(fb)
    return dict(raw_target=raw, transported_forbidden=moved, reflection_verified=True, root_swap_verified=True)


def minor_control(ctx, k, witness, length=1, styles=('direct', 'direct'), suppliers=None, external_length=1):
    """Three original components and exact root incidences; topology only."""
    assert length >= 1 and length % 2 == 1 and external_length >= 1
    comp = ctx['components'][k]
    root = comp['root']
    xarc, yarc, outside = witness['frame_arcs']
    edges = set()

    def edge(a, b):
        assert a != b
        edges.add(tuple(sorted((a, b))))

    for a, b in FRAME_EDGES:
        edge(f'b{a}', f'b{b}')
    edge('z', 'w')
    for owner, support in ctx['root_boundary'].items():
        for h in support:
            edge(owner, f'b{h}')
    path = [comp['contacts'][0]] + [f'x{i}' for i in range(1, length)] + [comp['contacts'][1]]
    for a, b in zip([root] + path, path + [root]):
        edge(a, b)
    full_component_vertices = {comp['name']: set(path)}
    component_routes = {}
    for j, other in enumerate(ctx['components']):
        if j == k:
            continue
        trunk = [other['contacts'][0]] + [f"{other['name']}_body{i}" for i in range(external_length)]
        for a, b in zip([other['root']] + trunk, trunk):
            edge(a, b)
        vertices = set(trunk)
        for contact in other['contacts'][1:]:
            edge(other['root'], contact)
            edge(contact, trunk[-1])
            vertices.add(contact)
        for h in other['support']:
            edge(trunk[-1], f'b{h}')
            component_routes[other['name'], h] = trunk + [f'b{h}']
        full_component_vertices[other['name']] = vertices
    possible = [sorted(set(comp['support']) & set(arc)) for arc in (xarc, yarc)]
    assert all(possible)
    suppliers = suppliers or [tuple(a[0] for a in possible)] * 2
    bags, tethers = [], []
    for x, style, pair in zip(path[:2], styles, suppliers, strict=True):
        assert all(h in allowed for h, allowed in zip(pair, possible, strict=True))
        a, b = (f'b{h}' for h in pair)
        if style == 'direct':
            routes = [[x, a], [x, b]]
        elif style == 'shared_trunk':
            routes = [[x, x + '_t', a], [x, x + '_t', b]]
        else:
            assert style in ('separate_bridges', 'shared_cycle')
            routes = [[x, x + '_a', a], [x, x + '_b', b]]
            if style == 'shared_cycle':
                edge(x + '_a', x + '_b')
        bag = {x}
        for route in routes:
            bag.update(route[:-1])
            for a, b in zip(route, route[1:]):
                edge(a, b)
        bags.append(bag)
        tethers.append(routes)
        full_component_vertices[comp['name']].update(bag)
    for h in set(comp['support']) - set(suppliers[0]):
        edge(path[0], f'b{h}')
    abstract = witness['route']
    route = abstract['path']
    if abstract['component'] is not None:
        route = route[:-2] + component_routes[abstract['component'], abstract['landing']]
    assert all(tuple(sorted(e)) in edges for e in zip(route, route[1:]))
    bags += [set(path[2:]) | set(route) | {f'b{i}' for i in outside},
             {f'b{i}' for i in xarc}, {f'b{i}' for i in yarc}]
    adjacency = verify_minor(edges, bags)
    # Check the retained graph identities independently of the minor witness.
    for owner in ('z', 'w'):
        neighbors = {b if a == owner else a for a, b in edges if owner in (a, b)}
        expected = {dict(z='w', w='z')[owner]} | {f'b{h}' for h in ctx['root_boundary'][owner]}
        expected |= {p for c in ctx['components'] if c['root'] == owner for p in c['contacts']}
        assert neighbors == expected and len(neighbors) == 5
    for other in ctx['components']:
        vertices = full_component_vertices[other['name']]
        boundary = {int(v[1:]) for a, b in edges for u, v in ((a, b), (b, a))
                    if u in vertices and v.startswith('b')}
        assert boundary == set(other['support'])
        assert not any(a in vertices and b in elsewhere for name, elsewhere in full_component_vertices.items()
                       if name != other['name'] for u, v in edges for a, b in ((u, v), (v, u)))
    rename = lambda v: f'b{RHO[int(v[1:])]}' if v.startswith('b') else v
    swap = lambda v: dict(z='w', w='z').get(v, v)
    for transform in (rename, swap):
        verify_minor({tuple(sorted((transform(a), transform(b)))) for a, b in edges},
                     [{transform(v) for v in bag} for bag in bags])
    return dict(record_id=ctx['record_id'], component=k, length=length, styles=styles,
                suppliers=suppliers, external_length=external_length,
                original_external_route=abstract, expanded_external_route=route,
                frame_arcs=witness['frame_arcs'], path=path, edges=sorted(edges),
                component_vertices={name: sorted(vs) for name, vs in full_component_vertices.items()},
                branch_sets=[sorted(b) for b in bags], actual_tether_routes=tethers,
                adjacencies=adjacency, reflection_and_root_swap_verified=True,
                scope='topology skeleton with original incidences, not a degree-list source')


def negative_controls(contexts, originals):
    result = []
    ctx, bans = contexts[14], [[1], [0, 3], [1]]
    assert evidence(ctx, TARGETS[0], bans)['eliminated']
    assert component_evidence(ctx, TARGETS[0], [[1], [0], [1]], 1) is None
    assert component_evidence(ctx, TARGETS[0], [[1], [0], [0, 3]], 2) is None
    result += ['singleton_F_has_no_pair_residual', 'single_contact_Dw_has_no_pair_path']
    c = component_evidence(contexts[22], TARGETS[1], [[1], [0, 3], [2]], 1)
    assert not c['first_bridge']['applicable'] and not c['eliminated']
    result.append('nonconserved_source_color_does_not_force_shared_beta')
    assert frame_evidence(ctx, 1, ()) == dict(supports=[], witnesses=[], eliminated=True, reason='no_possible_bag')
    result.append('empty_family_is_not_a_vacuous_minor')
    family = admissible_supports(TARGETS[1], (2, 3, 4), (0, 3))
    assert {2, 3} in family and {3, 4} in family
    assert not frame_evidence(contexts[22], 1, family)['eliminated']
    result.append('one_partition_must_cover_the_whole_family')
    partial = []
    for r, ctx0 in zip(originals, contexts, strict=True):
        for t in r['targets']:
            evs = [evidence(ctx0, t['row'], j['forbidden_sets']) for j in t['joins'] if not j['root_pairs']]
            direct = [e['closure_reason'] == 'fixed_frame_original_path' for e in evs]
            if any(direct) and not all(direct):
                partial.append((r['id'], t['row']))
    assert partial
    result.append('partial_direct_cover_needs_remaining_candidate_proofs')
    w = dict(frame_arcs=[(1, 2), (3, 4), (0,)],
             route=dict(mode='other_spoke', component=None, landing=0, path=['w', 'z', 'b0']))
    control = minor_control(ctx, 1, w)
    edges, bags = set(map(tuple, control['edges'])), list(map(set, control['branch_sets']))
    broken = [
        ('original_zw_required_by_this_witness', edges - {('w', 'z')}, bags),
        ('original_zb0_required_by_this_witness', edges - {('b0', 'z')}, bags),
        ('original_bridge_required', edges - {('Cw_0', 'Cw_1')}, bags),
        ('actual_tether_required', edges - {('Cw_1', 'b1')}, bags),
        ('frame_arc_must_be_connected', edges - {('b1', 'b2')}, bags),
        ('branch_sets_must_be_disjoint', edges, [bags[0] | {'w'}] + bags[1:]),
    ]
    dw = dict(frame_arcs=[(1, 2), (3,), (0, 4)],
              route=dict(mode='same_root_component', component='Dw', landing=4, path=['w', 'Dw_0', 'b4']))
    control = minor_control(ctx, 1, dw, external_length=3)
    de, db = set(map(tuple, control['edges'])), list(map(set, control['branch_sets']))
    broken += [('Dw_original_contact_required', de - {('Dw_0', 'w')}, db),
               ('Dw_internal_path_required', de - {('Dw_body0', 'Dw_body1')}, db),
               ('Dw_actual_attachment_required', de - {('Dw_body2', 'b4')}, db)]
    for name, es, bs in broken:
        try:
            verify_minor(es, bs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(f'negative control passed: {name}')
    return result


def build():
    data = json.loads(SOURCE.read_text())
    assert data['source_sha256'] == sha256((ROOT / 'scripts/c5_adjacent_degree5_no_mixed_t2_t1.py').read_bytes()).hexdigest()
    for path, expected in data['inputs_sha256'].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected
    contexts = [context(r, data['original_records'][r['source_id']]) for r in data['records']]
    records, controls, pending = [], [], []
    stages, joins, causes, outcomes = Counter(), Counter(), Counter(), Counter()
    reflection_count, root_pair_swaps = 0, 0
    control_keys = set()
    for r, ctx in zip(data['records'], contexts, strict=True):
        source = data['original_records'][r['source_id']]
        targets = []
        for ti, t in enumerate(r['targets']):
            assert canonical(row_evidence(source, tuple(map(tuple, r['supports'])), tuple(t['row']))) == t
            cases = []
            for j in t['joins']:
                assert canonical(root_pairs(ctx, t['row'], j['forbidden_sets'])) == j['root_pairs']
                assert {(b, a) for a, b in root_pairs(ctx, t['row'], j['forbidden_sets'])} == set(
                    root_pairs(swapped(ctx), t['row'], j['forbidden_sets']))
                root_pair_swaps += 1
                if j['root_pairs']:
                    cases.append(dict(original_join=j, eliminated=False, evidence=None, closure_reason='root_pair'))
                    continue
                ev = evidence(ctx, t['row'], j['forbidden_sets'])
                audit = symmetry_audit(ctx, t['row'], j['forbidden_sets'], ev, contexts[r['reflected_id']])
                reflection_count += 1
                joins[ev['closure_reason'] or 'unresolved'] += 1
                cases.append(dict(original_join=j, eliminated=ev['eliminated'], evidence=ev,
                                  closure_reason=ev['closure_reason'], symmetry=audit))
                for c in ev['components']:
                    frames = [c['direct_frame']] + [b['frame'] for b in c['first_bridge']['beta_cases']]
                    for frame in frames:
                        modes = set()
                        for w in frame['witnesses']:
                            route_key = w['route']['mode'], w['route']['component']
                            if route_key in modes:
                                continue
                            modes.add(route_key)
                            key = json.dumps([r['id'], c['component'], w], sort_keys=True)
                            if key not in control_keys:
                                control_keys.add(key)
                                controls.append(minor_control(ctx, c['component'], w))
            remaining = [c['original_join'] for c in cases if not c['original_join']['root_pairs'] and not c['eliminated']]
            if remaining:
                closure = None
                causes.update(reason for j in remaining for reason in j['obstruction_reasons'])
                pending.append(dict(record_id=r['id'], source_id=r['source_id'], target_index=ti,
                                    row=t['row'], candidates=remaining))
            elif t['status'] == 'accept':
                closure = t['closure_reason']
                stages['inherited'] += 1
            elif all(c['closure_reason'] in ('root_pair', 'fixed_frame_original_path') for c in cases):
                closure = 'fixed_frame_original_path'
                stages['direct'] += 1
            else:
                closure = 'shared_first_bridge'
                stages['first_bridge'] += 1
            targets.append(dict(row=t['row'], status='unresolved' if remaining else 'accept',
                                closure_reason=closure, cases=cases, remaining_candidates=remaining))
        outcomes['/'.join('A' if t['status'] == 'accept' else '?' for t in targets)] += 1
        records.append(dict(id=r['id'], original_record=r, context=ctx, targets=targets))
    # Record 14 keeps the actual w-z-b0 route and, separately, the full Dw route.
    ev = evidence(contexts[14], TARGETS[0], [[1], [0, 3], [1]])
    frame = ev['components'][0]['direct_frame']
    assert frame['supports'] == [[1, 3], [1, 2, 3]]
    assert all(t['status'] == 'accept' for t in records[14]['targets'])
    for mode in ('other_spoke', 'same_root_component', 'other_root_component'):
        witness = next(w for w in frame['witnesses'] if w['route']['mode'] == mode)
        suppliers = list(product(*(sorted(set(contexts[14]['components'][1]['support']) & set(a))
                                   for a in witness['frame_arcs'][:2])))
        for length, styles, p0, p1, ext in product((1, 3, 5), product(STYLES, repeat=2), suppliers, suppliers, (1, 3)):
            controls.append(minor_control(contexts[14], 1, witness, length, styles, [p0, p1], ext))
    negatives = negative_controls(contexts, data['records'])
    assert stages == {'inherited': 1002, 'direct': 42, 'first_bridge': 10}
    assert joins == {'fixed_frame_original_path': 70, 'shared_first_bridge': 10, 'unresolved': 66}
    assert outcomes == {'A/A': 494, 'A/?': 33, '?/A': 33}
    assert len(pending) == 66 and (pending[0]['record_id'], pending[0]['target_index']) == (22, 1)
    summary = dict(original_records=560, target_queries=1120, inherited_accepts=stages['inherited'],
        direct_frame_new_accepts=stages['direct'], first_bridge_new_accepts=stages['first_bridge'],
        new_accepts=52, final_accepts=1054, unresolved_queries=len(pending), both_targets_proved=494,
        original_failing_joins=sum(joins.values()), eliminated_failing_joins=80,
        candidate_closures=dict(sorted(joins.items())), remaining_candidate_causes=dict(sorted(causes.items())),
        target_classes=dict(sorted(outcomes.items())), new_source_exclusions=0,
        literal_reflection_checks=reflection_count, candidate_root_swap_checks=reflection_count,
        complete_join_root_swap_checks=root_pair_swaps, minor_controls=len(controls), negative_controls=len(negatives))
    inputs = ['scripts/' + name + '.py' for name in (
        'c5_adjacent_degree5_no_mixed_t2_t1', 'c5_adjacent_degree5_no_mixed_t2_bridge',
        'c5_no_spoke_first_bridge', 'c5_single_spoke_first_bridge', 'c5_single_spoke_frame_arc',
        'c5_single_spoke_two_two_minor', 'c5_single_spoke_two_two_external', 'c5_single_spoke_cores')]
    return dict(schema=1, scope='necessary support refinement; partial target separation, no source realization or Lean theorem',
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        original_source_path=str(SOURCE.relative_to(ROOT)), original_source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
        inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
        original_frontier=data['original_records'], source_fibers=data['source_fibers'],
        geometries=data['geometries'], rotation_templates=data['rotation_templates'],
        q_complete_binary_schemas=data['q_complete_binary_schemas'],
        summary=summary, records=records, open_queries=pending,
        algebra_controls=support_controls(), minor_controls=controls, negative_controls=negatives)


def render(data):
    lines = ['# 無 mixed t_z=2、t_w=1：原外部路徑與首橋', '',
        '原 560 份全保留；新增 52 個指定列延拓，1,054／1,120 已證、66 查詢未決。',
        'A 表示已證延拓，? 表示候選未決；沒有新增來源排除或 disk 實現。',
        '支援順序 Cz / z0 / z1 / Cw / Dw / w0；Dw 始終是原單接點分量。', '',
        '| 原 ID | 原側 IDs | 實際支援 | 原 p₁/p₂ | 本輪 p₁ | 本輪 p₂ |',
        '| ---: | --- | --- | --- | --- | --- |']
    for r in data['records']:
        old = r['original_record']
        support = ' / '.join(''.join(map(str, s)) for s in old['supports'])
        before = '/'.join('A' if t['status'] == 'accept' else '?' for t in old['targets'])
        closures = [t['closure_reason'] or '?' for t in r['targets']]
        lines.append(f"| {r['id']} | {old['source_side_ids']} | {support} | {before} | {closures[0]} | {closures[1]} |")
    lines += ['', '完整原記錄、schemas、rotations、146 組失敗候選及每筆反證見 [JSON](observations.json)。',
        '紙面證明、record 14 及 record 22 停止點見 [研究報告](../../docs/c5_adjacent_degree5_no_mixed_t2_t1_bridge.md)。', '']
    return '\n'.join(lines)


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
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
