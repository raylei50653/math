#!/usr/bin/env python3
"""Refine the immutable no-mixed t=2 table using both ORIGINAL endpoints.

Endpoint palettes need not agree with the next path vertex or each other.
The paper argument covers arbitrary paths; skeletons are not source graphs.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2 import row_evidence
from c5_adjacent_degree5_no_mixed_t2_bridge import (
    canonical, evidence as previous_evidence, frame_evidence, ROOTS,
)
from c5_single_spoke_cores import Q, TARGETS, U, PERMS, PI, RHO
from c5_single_spoke_first_bridge import fixed_colors, algebra_controls
from c5_single_spoke_frame_arc import admissible_supports, FRAME_EDGES, verify_arcs
from c5_single_spoke_two_two_external import STYLES
from c5_single_spoke_two_two_minor import subsets, verify_minor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_bridge/observations.json'
OUT = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_endpoints/observations.json'
TABLE = OUT.with_name('support_table.md')


def component_evidence(record, row, bans, k):
    f = bans[k]
    if len(f) != 2:
        return None
    support = tuple(record['supports'][3*k])
    d = record['q']['joins'][0]['forbidden_sets'][k][0]
    fixed = fixed_colors(Q, row, support)
    target = admissible_supports(tuple(row), support, tuple(f))
    cases, union = [], set()
    for beta in sorted(U - {d}):
        residual = tuple(sorted((d, beta)))
        if set(residual) & fixed != set(f) & fixed:
            continue
        source = admissible_supports(Q, support, residual)
        family = [t for t in target if t in source]
        union.update(family)
        cases.append(dict(beta=beta, source_endpoint_residual=residual,
                          supports=[sorted(t) for t in family]))
    family = sorted(union, key=lambda t: (len(t), sorted(t)))
    frame = frame_evidence(record['supports'], k, family)
    return dict(component=k, root=ROOTS[k], source_forbidden=[d], target_forbidden=f,
                ordered_contacts=[f'C{ROOTS[k]}_0', f'C{ROOTS[k]}_1'],
                fixed_colors=sorted(fixed), endpoint_cases=cases,
                endpoint_family=frame,
                endpoint_beta_scope='independent endpoint choices; no next-vertex equality',
                eliminated=frame['eliminated'])


def evidence(record, row, bans):
    components = [c for k in range(2)
                  if (c := component_evidence(record, row, bans, k)) is not None]
    return dict(components=components, eliminated=any(c['eliminated'] for c in components))


def reflection_audit(record, row, bans, ev, originals):
    reflected = originals[record['reflected_id']]
    raw = tuple(PI[row[RHO[i]]] for i in range(5))
    moved = [sorted(PI[c] for c in f) for f in bans]
    rev = evidence(reflected, raw, moved)
    assert ev['eliminated'] == rev['eliminated']
    for a, b in zip(ev['components'], rev['components'], strict=True):
        assert a['component'] == b['component'] and a['eliminated'] == b['eliminated']
        assert {PI[c] for c in a['fixed_colors']} == set(b['fixed_colors'])
        assert {PI[c] for c in a['source_forbidden']} == set(b['source_forbidden'])
        by_beta = {c['beta']: c for c in b['endpoint_cases']}
        assert {PI[c['beta']] for c in a['endpoint_cases']} == set(by_beta)
        for case in a['endpoint_cases']:
            other = by_beta[PI[case['beta']]]
            assert {PI[c] for c in case['source_endpoint_residual']} == set(other['source_endpoint_residual'])
            assert {tuple(sorted(RHO[i] for i in t)) for t in case['supports']} == set(map(tuple, other['supports']))
        x, y = a['endpoint_family'], b['endpoint_family']
        assert {tuple(sorted(RHO[i] for i in t)) for t in x['supports']} == set(map(tuple, y['supports']))
        keys = {(tuple(map(tuple, w['frame_arcs'])), w['route']['mode'], w['route']['landing'])
                for w in y['witnesses']}
        for w in x['witnesses']:
            arcs = tuple(tuple(sorted(RHO[i] for i in arc)) for arc in w['frame_arcs'])
            verify_arcs([arc[0] for arc in arcs], arcs)
            assert (arcs, w['route']['mode'], RHO[w['route']['landing']]) in keys
    return dict(raw_target=raw, transported_forbidden=moved, verified=True)


def minor_control(record, k, witness, length=1, styles=('direct', 'direct'), suppliers=None):
    """A = W_0 union ... union W_(ell-1); A' = W_ell, in the same graph."""
    assert length >= 1 and length % 2 == 1
    supports = record['supports']
    root, other = ROOTS[k], ROOTS[1-k]
    xarc, yarc, outside = witness['frame_arcs']
    verify_arcs([arc[0] for arc in witness['frame_arcs']], witness['frame_arcs'])
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
    bags = [{x} for x in path]
    tethers = []
    for j, style, pair in zip((0, length), styles, suppliers, strict=True):
        assert pair[0] in possible[0] and pair[1] in possible[1]
        x = path[j]
        a, b = (f'b{i}' for i in pair)
        if style == 'direct':
            routes = [[x, a], [x, b]]
        elif style == 'shared_trunk':
            routes = [[x, x+'_t', a], [x, x+'_t', b]]
        else:
            assert style in ('separate_bridges', 'shared_cycle')
            routes = [[x, x+'_a', a], [x, x+'_b', b]]
            if style == 'shared_cycle':
                edge(x+'_a', x+'_b')
        for route in routes:
            bags[j].update(route[:-1])
            for a, b in zip(route, route[1:]):
                edge(a, b)
        tethers.append(routes)
    for j in range(1, length):
        edge(path[j], path[j]+'_tail')
        bags[j].add(path[j]+'_tail')
    for h in supports[3*k]:
        edge('x0', f'b{h}')  # Keep the complete original support in the skeleton.
    route = witness['route']['path']
    assert all(tuple(sorted(e)) in edges for e in zip(route, route[1:]))
    branch_sets = [set().union(*bags[:-1]), bags[-1],
                   set(route) | {f'b{i}' for i in outside},
                   {f'b{i}' for i in xarc}, {f'b{i}' for i in yarc}]
    adjacencies = verify_minor(edges, branch_sets)
    rename = lambda v: f'b{RHO[int(v[1:])]}' if v.startswith('b') else v
    reflected_edges = {tuple(sorted((rename(a), rename(b)))) for a, b in edges}
    reflected_bags = [{rename(v) for v in bag} for bag in branch_sets]
    return dict(record_id=record['id'], component=k, length=length, styles=styles,
                endpoint_indices=[0, length], suppliers=suppliers,
                original_external_route=witness['route'], frame_arcs=witness['frame_arcs'],
                edges=sorted(edges), path_bags=[sorted(b) for b in bags],
                branch_sets=[sorted(b) for b in branch_sets], actual_tether_routes=tethers,
                adjacencies=adjacencies, reflected_adjacencies=verify_minor(reflected_edges, reflected_bags),
                scope='topology skeleton, not a degree-list source')


def endpoint_controls():
    controls = []
    for row, support, d, pair in product(TARGETS, subsets(range(5)), sorted(U), combinations(range(4), 2)):
        fixed = fixed_colors(Q, row, support)
        betas = [b for b in sorted(U-{d}) if {d, b} & fixed == set(pair) & fixed]
        # Independent enumeration of the endpoint residual and its removed color.
        residuals = [e for e in subsets(U) if d in e and len(e-{d}) == 1
                     and e & fixed == set(pair) & fixed]
        assert {tuple(sorted((d, b))) for b in betas} == {tuple(sorted(e)) for e in residuals}
        for beta in betas:
            eq = {d, beta}
            family = set(admissible_supports(Q, tuple(sorted(support)), tuple(sorted(eq)))) & set(
                admissible_supports(tuple(row), tuple(sorted(support)), pair))
            independent = [t for t in subsets(support) if all(
                {p[c] for c in e} == set(e) for colors, e in ((Q, eq), (row, pair))
                for p in PERMS if all(p[colors[i]] == colors[i] for i in t))]
            assert family == set(independent)
        controls.append(dict(row=row, support=sorted(support), source_color=d,
                             target_pair=pair, fixed_colors=sorted(fixed), possible_betas=betas))
    assert len(controls) == 1536
    return dict(endpoint_domains=controls, inherited_palette_algebra=algebra_controls())


def negative_controls(originals):
    r = originals[5]
    bans = [[1], [0, 3]]
    c = component_evidence(r, TARGETS[1], bans, 1)
    assert c['source_forbidden'][0] not in c['fixed_colors'] and c['eliminated']
    assert [e['beta'] for e in c['endpoint_cases']] == [3]
    assert component_evidence(r, TARGETS[1], [[1], [0]], 1) is None
    result = ['nonconserved_source_color_still_has_endpoint_tightness',
              'target_singleton_has_no_pair_path']
    # Allowed local palette equations, NOT realizable graph assertions.
    edges = (3, 2, 3)
    residuals = [{0, edges[0]}, *({a, b} for a, b in zip(edges, edges[1:])), {0, edges[-1]}]
    assert residuals[0] == residuals[-1] == {0, 3} and residuals[1] == {2, 3}
    assert all(e & {1, 3} == {3} for e in residuals)
    result.append('nonconserved_source_color_does_not_fix_next_vertex')
    edges = (1, 3, 2)
    residuals = [{3, edges[0]}, *({a, b} for a, b in zip(edges, edges[1:])), {3, edges[-1]}]
    assert all(e & {0, 3} == {3} for e in residuals) and edges[0] != edges[-1]
    result.append('different_endpoint_edges_need_not_share_beta')
    assert {3}-{0} == {3} and 0 not in {3}
    result.append('removed_color_equation_alone_does_not_supply_tightness')
    unresolved = evidence(originals[54], TARGETS[0], [[2, 3], [3]])
    assert not unresolved['eliminated']
    result.append('endpoint_beta_union_must_not_discard_unresolved_choices')
    w = next(w for w in c['endpoint_family']['witnesses']
             if w['route']['mode'] == 'other_spoke' and w['route']['landing'] == 0)
    base = minor_control(r, 1, w, 3, suppliers=[(1, 4), (3, 4)])
    es, bs = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    broken = [
        ('missing_original_zw', es-{('w', 'z')}, bs),
        ('missing_original_spoke', es-{('b0', 'z')}, bs),
        ('missing_intermediate_bridge', es-{('x0', 'x1')}, bs),
        ('missing_join_bridge', es-{('x2', 'x3')}, bs),
        ('missing_last_contact', es-{('w', 'x3')}, bs),
        ('missing_last_supplier', es-{('b4', 'x3')}, bs),
        ('broken_frame_arc', es-{('b1', 'b2')}, bs),
        ('endpoint_bags_are_not_adjacent_without_path', es, [{ 'x0' }, bs[1], *bs[2:]]),
        ('overlapping_branch_sets', es, [bs[0] | {'w'}, *bs[1:]]),
    ]
    for name, test_edges, test_bags in broken:
        try:
            verify_minor(test_edges, test_bags)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    return result


def build():
    data = json.loads(SOURCE.read_text())
    assert data['source_sha256'] == sha256((ROOT/'scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py').read_bytes()).hexdigest()
    assert data['original_source_sha256'] == sha256((ROOT/data['original_source_path']).read_bytes()).hexdigest()
    for path, digest in data['inputs_sha256'].items():
        assert digest == sha256((ROOT/path).read_bytes()).hexdigest()
    assert data['summary']['final_accepts'] == 580
    originals = [entry['original_record'] for entry in data['records']]
    assert [r['id'] for r in originals] == list(range(322))
    records, controls = [], []
    fresh_count = old_failures = reflection_count = 0
    for entry, r in zip(data['records'], originals, strict=True):
        targets = []
        for n, target in enumerate(r['targets']):
            fresh = row_evidence(data['original_frontier'][r['source_id']],
                                 tuple(map(tuple, r['supports'])), tuple(target['row']))
            assert canonical(fresh) == target
            fresh_count += len(target['joins'])
            old = entry['targets'][n]
            inherited = {c['original_join_index']: c for c in old['cases']}
            cases = []
            for j, join in enumerate(target['joins']):
                if join['root_pairs']:
                    continue
                old_failures += 1
                assert inherited[j]['original_join'] == join
                prior = previous_evidence(r, target['row'], join['forbidden_sets'])
                assert canonical(prior) == inherited[j]['evidence']
                ev = evidence(r, target['row'], join['forbidden_sets'])
                reflection = reflection_audit(r, target['row'], join['forbidden_sets'], ev, originals)
                reflection_count += 1
                is_new = not prior['eliminated'] and ev['eliminated']
                if is_new:
                    c = next(c for c in ev['components'] if c['eliminated'])
                    assert c['endpoint_family']['witnesses']
                    controls.append(minor_control(r, c['component'], c['endpoint_family']['witnesses'][0], 3))
                cases.append(dict(original_join_index=j, original_join=join,
                                  inherited_eliminated=prior['eliminated'], endpoint_evidence=ev,
                                  newly_eliminated=is_new, eliminated=prior['eliminated'] or ev['eliminated'],
                                  reflection=reflection))
            assert old['status'] == ('accept' if all(c['inherited_eliminated'] for c in cases) else 'unresolved')
            closed = all(c['eliminated'] for c in cases)
            targets.append(dict(row=target['row'], inherited_status=old['status'],
                                status='accept' if closed else 'unresolved', cases=cases,
                                remaining_candidates=[c['original_join'] for c in cases if not c['eliminated']]))
        records.append(dict(id=r['id'], inherited_record=entry, targets=targets))
    classes = Counter('/'.join(t['status'] for t in r['targets']) for r in records)
    assert classes == {'accept/accept': 318, 'accept/unresolved': 2, 'unresolved/accept': 2}
    for r, old in zip(records, originals, strict=True):
        other = records[old['root_swapped_id']]
        assert [t['status'] for t in r['targets']] == [t['status'] for t in other['targets']]
        for a, b in zip(r['targets'], other['targets'], strict=True):
            assert {(tuple(map(tuple, c['original_join']['forbidden_sets'][::-1])), c['eliminated']) for c in a['cases']} == {
                (tuple(map(tuple, c['original_join']['forbidden_sets'])), c['eliminated']) for c in b['cases']}
    pending = [dict(record_id=r['id'], target_index=i, row=t['row'], candidates=t['remaining_candidates'])
               for r in records for i, t in enumerate(r['targets']) if t['status'] == 'unresolved']
    assert [(p['record_id'], p['target_index']) for p in pending] == [(54, 0), (68, 1), (173, 1), (256, 0)]
    r = originals[5]
    c = component_evidence(r, TARGETS[1], [[1], [0, 3]], 1)
    for mode in ('other_spoke', 'other_component'):
        w = next(w for w in c['endpoint_family']['witnesses'] if w['route']['mode'] == mode)
        pairs = [p for p in product(*(sorted(set(r['supports'][3]) & set(a)) for a in w['frame_arcs'][:2]))
                 if sorted(p) in c['endpoint_family']['supports']]
        for length, styles, p0, p1 in product((1, 3, 5, 9), product(STYLES, repeat=2), pairs, pairs):
            controls.append(minor_control(r, 1, w, length, styles, [p0, p1]))
    negatives = negative_controls(originals)
    summary = dict(original_records=322, target_queries=644, inherited_accepts=580,
                   inherited_unresolved=64, new_accepts=60, final_accepts=640,
                   new_source_exclusions=0, both_targets_proved=318, unresolved_queries=4,
                   target_classes=dict(sorted(classes.items())), complete_joins_replayed=fresh_count,
                   original_failing_joins=old_failures, new_failing_joins_eliminated=sum(
                       c['newly_eliminated'] for r in records for t in r['targets'] for c in t['cases']),
                   root_swap_checks=322, literal_reflection_checks=reflection_count,
                   minor_controls=len(controls), negative_controls=len(negatives))
    assert fresh_count == 2892 and old_failures == reflection_count == 160
    assert summary['new_failing_joins_eliminated'] == 60
    inputs = sorted(set(data['inputs_sha256']) | {'scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py'})
    return dict(schema=1, scope='necessary endpoint refinement; partial targets; no source realizability or Lean theorem',
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                previous_path=str(SOURCE.relative_to(ROOT)), previous_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
                original_source_path=data['original_source_path'], original_source_sha256=data['original_source_sha256'],
                inputs_sha256={p: sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
                original_frontier=data['original_frontier'], source_fibers=data['source_fibers'],
                q_complete_schemas=data['q_complete_schemas'], rotation_templates=data['rotation_templates'],
                summary=summary, records=records, open_queries=pending,
                algebra_controls=endpoint_controls(), minor_controls=controls, negative_controls=negatives)


def render(data):
    lines = ['# 無 mixed 兩側 t=2：原雙端點與完整 bridge 路徑', '',
             '原 322 份全部保留；新增 60 個延拓，640／644 個 target 已證，4 個未決。',
             '必要資料與 minor skeletons 均非 disk 實現；A 為已證接受，? 為上界未決。', '',
             '| 原 ID | 原 sides | actual supports：Cz/z0/z1/Cw/w0/w1 | 前層 p₁/p₂ | 本輪 p₁/p₂ |',
             '| ---: | --- | --- | --- | --- |']
    mark = lambda ts: '/'.join('A' if t['status'] == 'accept' else '?' for t in ts)
    for r in data['records']:
        old = r['inherited_record']
        original = old['original_record']
        supports = '/'.join(''.join(map(str, s)) for s in original['supports'])
        lines.append(f"| {r['id']} | {original['source_side_ids']} | {supports} | {mark(old['targets'])} | {mark(r['targets'])} |")
    lines += ['', '原資料、完整 schemas／rotations、所有 joins、雙端點族與原圖 minor 見 [JSON](observations.json)。',
              '論證、四個未決項及信任界線見 [研究報告](../../docs/c5_adjacent_degree5_no_mixed_t2_endpoints.md)。', '']
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
