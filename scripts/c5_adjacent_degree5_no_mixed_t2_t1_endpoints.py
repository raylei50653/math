#!/usr/bin/env python3
"""Close the t_z=2, t_w=1 queries with both original contact endpoints.

All three components, five contacts, three spokes and zw are retained.
Paper arguments cover arbitrary sources; finite skeletons are not sources.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2_t1 import row_evidence
from c5_adjacent_degree5_no_mixed_t2_t1_bridge import (
    canonical, context, evidence as previous_evidence, frame_evidence,
    minor_control as first_edge_control, root_pairs, swapped,
)
from c5_adjacent_degree5_no_mixed_t2_endpoints import endpoint_controls
from c5_single_spoke_cores import Q, TARGETS, U, PI, RHO
from c5_single_spoke_first_bridge import fixed_colors
from c5_single_spoke_frame_arc import admissible_supports, verify_arcs
from c5_single_spoke_two_two_external import STYLES
from c5_single_spoke_two_two_minor import verify_minor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_t1_bridge/observations.json'
OUT = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints/observations.json'
TABLE = OUT.with_name('support_table.md')


def component_evidence(ctx, row, bans, k):
    comp, pair = ctx['components'][k], bans[k]
    if len(comp['contacts']) != 2 or len(pair) != 2:
        return None
    assert len(comp['source_forbidden']) == 1
    d = comp['source_forbidden'][0]
    support = tuple(comp['support'])
    fixed = fixed_colors(Q, row, support)
    target = admissible_supports(tuple(row), support, tuple(pair))
    cases, union = [], set()
    for beta in sorted(U - {d}):
        residual = tuple(sorted((d, beta)))
        if set(residual) & fixed != set(pair) & fixed:
            continue
        source = admissible_supports(Q, support, residual)
        common = [t for t in target if t in source]
        union.update(common)
        cases.append(dict(beta=beta, source_endpoint_residual=residual,
                          supports=[sorted(t) for t in common]))
    family = sorted(union, key=lambda t: (len(t), sorted(t)))
    frame = frame_evidence(ctx, k, family)
    return dict(component=k, name=comp['name'], root=comp['root'],
        ordered_contacts=comp['contacts'], source_forbidden=[d], target_forbidden=pair,
        fixed_colors=sorted(fixed), endpoint_cases=cases, endpoint_family=frame,
        endpoint_beta_scope='all choices at both original endpoints; no next-vertex equality',
        eliminated=frame['eliminated'])


def evidence(ctx, row, bans):
    components = [c for k in range(3)
                  if (c := component_evidence(ctx, row, bans, k)) is not None]
    return dict(components=components, eliminated=any(c['eliminated'] for c in components))


def symmetry_audit(ctx, row, bans, ev, reflected):
    raw = tuple(PI[row[RHO[i]]] for i in range(5))
    moved = [sorted(PI[c] for c in f) for f in bans]
    rev = evidence(reflected, raw, moved)
    assert ev['eliminated'] == rev['eliminated']
    for a, b in zip(ev['components'], rev['components'], strict=True):
        assert (a['component'], a['eliminated']) == (b['component'], b['eliminated'])
        for key in ('source_forbidden', 'target_forbidden', 'fixed_colors'):
            assert {PI[c] for c in a[key]} == set(b[key])
        cases = {c['beta']: c for c in b['endpoint_cases']}
        assert {PI[c['beta']] for c in a['endpoint_cases']} == set(cases)
        for case in a['endpoint_cases']:
            twin = cases[PI[case['beta']]]
            assert {PI[c] for c in case['source_endpoint_residual']} == set(twin['source_endpoint_residual'])
            assert {tuple(sorted(RHO[i] for i in t)) for t in case['supports']} == set(map(tuple, twin['supports']))
        x, y = a['endpoint_family'], b['endpoint_family']
        assert x['eliminated'] == y['eliminated']
        assert {tuple(sorted(RHO[i] for i in t)) for t in x['supports']} == set(map(tuple, y['supports']))
        keys = {(tuple(map(tuple, w['frame_arcs'])), w['route']['mode'],
                 w['route']['component'], w['route']['landing']) for w in y['witnesses']}
        for witness in x['witnesses']:
            arcs = tuple(tuple(sorted(RHO[i] for i in arc)) for arc in witness['frame_arcs'])
            verify_arcs([arc[0] for arc in arcs], arcs)
            route = witness['route']
            assert (arcs, route['mode'], route['component'], RHO[route['landing']]) in keys
    other = evidence(swapped(ctx), row, bans)
    renamed = canonical(ev)
    for c in renamed['components']:
        c['root'] = dict(z='w', w='z')[c['root']]
        for witness in c['endpoint_family']['witnesses']:
            witness['route']['path'] = [dict(z='w', w='z').get(v, v) for v in witness['route']['path']]
    assert renamed == canonical(other)
    return dict(raw_target=raw, transported_forbidden=moved,
                reflection_verified=True, complete_root_swap_verified=True)


def minor_control(ctx, k, witness, length=1, styles=('direct', 'direct'), suppliers=None, external_length=1):
    """Keep both ORIGINAL contacts; put the entire intervening path in A."""
    assert length >= 1 and length % 2 == 1
    control = first_edge_control(ctx, k, witness, 1, styles, suppliers, external_length)
    a, b = ctx['components'][k]['contacts']
    edges = set(map(tuple, control['edges']))
    bags = list(map(set, control['branch_sets']))
    path = [a] + [f'endpoint_middle_{j}' for j in range(1, length)] + [b]
    edges.remove(tuple(sorted((a, b))))
    edges.update(tuple(sorted(e)) for e in zip(path, path[1:]))
    middle = set(path[1:-1])
    for v in path[1:-1]:
        edges.add(tuple(sorted((v, v + '_tail'))))
        middle.add(v + '_tail')
    bags[0].update(middle)
    vertices = control['component_vertices']
    vertices[ctx['components'][k]['name']] = sorted(set(vertices[ctx['components'][k]['name']]) | middle)
    adjacency = verify_minor(edges, bags)
    reflect = lambda v: f'b{RHO[int(v[1:])]}' if v.startswith('b') else v
    swap = lambda v: dict(z='w', w='z').get(v, v)
    for transform in (reflect, swap):
        verify_minor({tuple(sorted((transform(a), transform(b)))) for a, b in edges},
                     [{transform(v) for v in bag} for bag in bags])
    control.update(length=length, path=path, endpoint_indices=[0, length],
        edges=sorted(edges), branch_sets=[sorted(bag) for bag in bags], adjacencies=adjacency,
        scope='original endpoint topology skeleton; middle path retained; not a degree-list source')
    return control


def negative_controls(contexts):
    ctx, bans = contexts[22], [[1], [0, 3], [2]]
    c = component_evidence(ctx, TARGETS[1], bans, 1)
    assert c['source_forbidden'][0] not in c['fixed_colors'] and c['eliminated']
    assert [b['beta'] for b in c['endpoint_cases']] == [3]
    assert c['endpoint_family']['supports'] == [[2, 3], [2, 3, 4]]
    assert component_evidence(ctx, TARGETS[1], [[1], [0], [2]], 1) is None
    assert component_evidence(ctx, TARGETS[1], [[1], [0], [0, 3]], 2) is None
    result = ['nonconserved_d_still_constrains_both_original_endpoints',
              'singleton_F_has_no_pair_path', 'single_contact_Dw_has_no_pair_path']
    word = (3, 0, 3)
    residuals = [{2, word[0]}, *({a, b} for a, b in zip(word, word[1:])), {2, word[-1]}]
    assert residuals[0] == residuals[-1] == {2, 3} and residuals[1] == {0, 3}
    assert all(r & {1, 3} == {3} for r in residuals)
    result.append('endpoint_tightness_does_not_fix_the_next_vertex')
    assert not frame_evidence(ctx, 1, admissible_supports(TARGETS[1], (2, 3, 4), (0, 3)))['eliminated']
    result.append('target_only_support_family_has_no_uniform_frame')
    assert frame_evidence(ctx, 1, ())['reason'] == 'no_possible_bag'
    result.append('empty_family_is_not_a_vacuous_minor')
    witness = next(w for w in c['endpoint_family']['witnesses']
                   if canonical(w['frame_arcs']) == [[1, 2], [3, 4], [0]]
                   and w['route']['mode'] == 'other_spoke' and w['route']['landing'] == 0)
    base = minor_control(ctx, 1, witness, 3)
    es, bs = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    broken = [
        ('missing_original_zw', es - {('w', 'z')}, bs),
        ('missing_original_spoke', es - {('b0', 'z')}, bs),
        ('missing_intermediate_bridge', es - {('Cw_0', 'endpoint_middle_1')}, bs),
        ('missing_join_bridge', es - {('Cw_1', 'endpoint_middle_2')}, bs),
        ('missing_last_contact', es - {('Cw_1', 'w')}, bs),
        ('missing_last_attachment', es - {('Cw_1', 'b3')}, bs),
        ('broken_fixed_frame_arc', es - {('b1', 'b2')}, bs),
        ('dropping_the_middle_path', es, [{'Cw_0'}, *bs[1:]]),
        ('overlapping_branch_sets', es, [bs[0] | {'w'}, *bs[1:]]),
    ]
    # Use record 14's Dw route: record 22 also has an original spoke to b1,
    # which would keep Z connected after these Dw edge deletions.
    frame = previous_evidence(contexts[14], TARGETS[0], [[1], [0, 3], [1]])['components'][0]['direct_frame']
    dw = next(w for w in frame['witnesses']
              if canonical(w['frame_arcs']) == [[1, 2], [3], [0, 4]]
              and w['route']['mode'] == 'same_root_component')
    base = minor_control(contexts[14], 1, dw, 3, external_length=3)
    route = base['expanded_external_route']
    for name, edge in [('missing_Dw_contact', route[:2]),
                       ('missing_Dw_internal_edge', route[1:3]),
                       ('missing_Dw_actual_attachment', route[-2:])]:
        broken.append((name, set(map(tuple, base['edges'])) - {tuple(sorted(edge))},
                       list(map(set, base['branch_sets']))))
    for name, es, bs in broken:
        try:
            verify_minor(es, bs)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    return result


def next_frontier():
    """Read the next ordered subtable only; do not enumerate new supports."""
    path = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed/observations.json'
    data = json.loads(path.read_text())
    sides = data['side_normal_forms']
    rows = [dict(retained_join_id=i, side_ids=pair)
            for i, pair in enumerate(data['abstract_conditions']['retained'])
            if sides[pair[0]]['ports'] == [2] and len(sides[pair[0]]['root_boundary']) == 2
            and sides[pair[1]]['ports'] == [2, 1, 1] and not sides[pair[1]]['root_boundary']]
    assert len(rows) == 96 and rows[0] == dict(retained_join_id=3048, side_ids=[133, 64])
    return dict(source_path=str(path.relative_to(ROOT)), source_sha256=sha256(path.read_bytes()).hexdigest(),
                scope='next t_z=2,(2), t_w=0,(2,1,1) ordered frontier; no support coverage yet',
                records=rows, first_sides=[sides[i] for i in rows[0]['side_ids']])


def build():
    data = json.loads(SOURCE.read_text())
    prior_script = 'scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py'
    assert data['source_sha256'] == sha256((ROOT / prior_script).read_bytes()).hexdigest()
    assert data['original_source_sha256'] == sha256((ROOT / data['original_source_path']).read_bytes()).hexdigest()
    for path, digest in data['inputs_sha256'].items():
        assert digest == sha256((ROOT / path).read_bytes()).hexdigest()
    assert data['summary']['final_accepts'] == 1054
    assert [r['id'] for r in data['records']] == list(range(560))
    # Rebuild the producer's z,w insertion order; sorted JSON stores w,z.
    contexts = [context(e['original_record'], data['original_frontier'][e['original_record']['source_id']])
                for e in data['records']]
    records, controls, fresh = [], [], []
    joins_replayed = failures = reflections = inherited_failures = 0
    route_modes = set()
    for entry, ctx in zip(data['records'], contexts, strict=True):
        r = entry['original_record']
        source = data['original_frontier'][r['source_id']]
        assert canonical(ctx) == entry['context']
        targets = []
        for ti, t in enumerate(r['targets']):
            assert canonical(row_evidence(source, tuple(map(tuple, r['supports'])), tuple(t['row']))) == t
            previous = entry['targets'][ti]
            cases = []
            for ji, (join, old) in enumerate(zip(t['joins'], previous['cases'], strict=True)):
                assert join == old['original_join']
                pairs = root_pairs(ctx, t['row'], join['forbidden_sets'])
                assert canonical(pairs) == join['root_pairs']
                assert {(b, a) for a, b in pairs} == set(root_pairs(swapped(ctx), t['row'], join['forbidden_sets']))
                joins_replayed += 1
                if pairs:
                    continue
                failures += 1
                prior = previous_evidence(ctx, t['row'], join['forbidden_sets'])
                assert canonical(prior) == old['evidence'] and prior['eliminated'] == old['eliminated']
                inherited_failures += prior['eliminated']
                ev = evidence(ctx, t['row'], join['forbidden_sets'])
                symmetry = symmetry_audit(ctx, t['row'], join['forbidden_sets'], ev, contexts[r['reflected_id']])
                reflections += 1
                new = not prior['eliminated'] and ev['eliminated']
                if new:
                    fresh.append(dict(record_id=r['id'], target_index=ti, original_join_index=ji))
                    c = next(c for c in ev['components'] if c['eliminated'])
                    modes = set()
                    for witness in c['endpoint_family']['witnesses']:
                        key = witness['route']['mode'], witness['route']['component']
                        if key in modes:
                            continue
                        modes.add(key)
                        route_modes.add(witness['route']['mode'])
                        controls.append(minor_control(ctx, c['component'], witness, 3))
                cases.append(dict(original_join_index=ji, original_join=join,
                    inherited_eliminated=prior['eliminated'], endpoint_evidence=ev,
                    newly_eliminated=new, eliminated=prior['eliminated'] or ev['eliminated'], symmetry=symmetry))
            assert previous['status'] == ('accept' if all(c['inherited_eliminated'] for c in cases) else 'unresolved')
            remaining = [c['original_join'] for c in cases if not c['eliminated']]
            targets.append(dict(row=t['row'], inherited_status=previous['status'],
                status='unresolved' if remaining else 'accept', cases=cases, remaining_candidates=remaining))
        records.append(dict(id=r['id'], inherited_record=entry, targets=targets))
    c = component_evidence(contexts[22], TARGETS[1], [[1], [0, 3], [2]], 1)
    for mode in ('own_spoke', 'other_spoke', 'same_root_component', 'other_root_component'):
        witness = next(w for w in c['endpoint_family']['witnesses']
                       if canonical(w['frame_arcs']) == [[2], [3], [0, 1, 4]] and w['route']['mode'] == mode)
        for length, styles, ext in product((1, 3, 5, 9), product(STYLES, repeat=2), (1, 3)):
            controls.append(minor_control(contexts[22], 1, witness, length, styles, [(2, 3), (2, 3)], ext))
    negatives = negative_controls(contexts)
    classes = Counter('/'.join('A' if t['status'] == 'accept' else '?' for t in r['targets']) for r in records)
    pending = [dict(record_id=r['id'], target_index=i, candidates=t['remaining_candidates'])
               for r in records for i, t in enumerate(r['targets']) if t['status'] == 'unresolved']
    assert classes == {'A/A': 560} and not pending
    assert len(fresh) == 66 and joins_replayed == 3148 and failures == reflections == 146
    assert inherited_failures == 80
    assert {(p['record_id'], p['target_index']) for p in fresh} == {
        (p['record_id'], p['target_index']) for p in data['open_queries']}
    summary = dict(original_records=560, target_queries=1120, inherited_accepts=1054,
        inherited_unresolved=66, new_accepts=66, final_accepts=1120, both_targets_proved=560,
        unresolved_queries=0, new_source_exclusions=0, target_classes=dict(classes),
        complete_joins_replayed=joins_replayed, complete_join_root_swap_checks=joins_replayed,
        original_failing_joins=failures, inherited_failing_joins_eliminated=inherited_failures,
        new_failing_joins_eliminated=len(fresh), literal_reflection_checks=reflections,
        candidate_root_swap_checks=reflections, minor_controls=len(controls),
        negative_controls=len(negatives), external_route_modes=sorted(route_modes))
    inputs = sorted(set(data['inputs_sha256']) | {prior_script,
        'scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py',
        'scripts/c5_single_spoke_branch_palettes.py'})
    return dict(schema=1, scope='all targets proved for this source class; no source realization or Lean theorem',
        source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        previous_path=str(SOURCE.relative_to(ROOT)), previous_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
        original_source_path=data['original_source_path'], original_source_sha256=data['original_source_sha256'],
        inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
        original_frontier=data['original_frontier'], source_fibers=data['source_fibers'],
        geometries=data['geometries'], rotation_templates=data['rotation_templates'],
        q_complete_binary_schemas=data['q_complete_binary_schemas'], summary=summary, records=records,
        new_closures=fresh, open_queries=pending, next_frontier=next_frontier(), algebra_controls=endpoint_controls(),
        minor_controls=controls, negative_controls=negatives)


def render(data):
    lines = ['# 無 mixed t_z=2、t_w=1：原雙端點與完整 bridge 路徑', '',
        '原 560 份全部保留；新增 66 個延拓，1,120／1,120 查詢全證、0 未決。',
        '必要資料與 minor skeletons 均非 disk 實現；A 表示已證接受。', '',
        '| 原 ID | 原 sides | 支援 Cz/z0/z1/Cw/Dw/w0 | 前層 p₁/p₂ | 本輪 p₁/p₂ |',
        '| ---: | --- | --- | --- | --- |']
    mark = lambda ts: '/'.join('A' if t['status'] == 'accept' else '?' for t in ts)
    for r in data['records']:
        old = r['inherited_record']
        original = old['original_record']
        supports = '/'.join(''.join(map(str, s)) for s in original['supports'])
        lines.append(f"| {r['id']} | {original['source_side_ids']} | {supports} | {mark(old['targets'])} | {mark(r['targets'])} |")
    lines += ['', '完整原資料、schemas、rotations、joins 及證書見 [JSON](observations.json)。',
        '任意大小論證、record 22 與信任界線見 [研究報告](../../docs/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md)。', '']
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
