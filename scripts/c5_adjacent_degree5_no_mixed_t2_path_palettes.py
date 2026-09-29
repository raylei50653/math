#!/usr/bin/env python3
"""Close the four no-mixed t=2 queries using the entire original bridge path.

Paper induction covers arbitrary paths. Finite palette and minor controls are
not source realizations, replacement states, or Lean proofs.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2 import row_evidence
from c5_adjacent_degree5_no_mixed_t2_bridge import (
    canonical, evidence as bridge_evidence, ROOTS,
)
from c5_adjacent_degree5_no_mixed_t2_endpoints import evidence as endpoint_evidence
from c5_single_spoke_cores import Q, U, PI, RHO
from c5_single_spoke_two_two_external import STYLES
from c5_single_spoke_two_two_minor import subsets, verify_minor
from c5_single_spoke_frame_arc import FRAME_EDGES, verify_arcs

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_endpoints/observations.json'
OUT = ROOT / 'artifacts/c5_adjacent_degree5_no_mixed_t2_path_palettes/observations.json'
TABLE = OUT.with_name('support_table.md')


def evidence(record, row, bans):
    """The first-edge family applies to EVERY odd edge when d is conserved."""
    prior = bridge_evidence(record, row, bans)
    components = []
    for c in prior['components']:
        first = c['first_bridge']
        d = c['source_forbidden'][0]
        if not first['applicable'] or d not in c['target_forbidden']:
            continue
        cases = first['beta_cases']
        survivors = [b['beta'] for b in cases if not b['frame']['eliminated']]
        components.append(dict(
            component=c['component'], root=c['root'], ordered_contacts=c['ordered_contacts'],
            source_forbidden=[d], target_forbidden=c['target_forbidden'],
            fixed_colors=first['fixed_colors'], odd_edge_cases=cases,
            surviving_betas=survivors,
            forced_source_pair=sorted([d, *survivors]) if len(survivors) == 1 else None,
            eliminated=len(survivors) <= 1,
            reason=('no_possible_odd_edge' if not survivors else
                    'constant_path_forces_second_source_ban' if len(survivors) == 1 else
                    'multiple_odd_palettes_remain'),
            scope='each odd original edge; no assumption of equal odd palettes before exclusion'))
    return dict(components=components, eliminated=any(c['eliminated'] for c in components))


def reflection_audit(record, row, bans, ev, originals):
    raw = tuple(PI[row[RHO[i]]] for i in range(5))
    moved = [sorted(PI[c] for c in f) for f in bans]
    other = evidence(originals[record['reflected_id']], raw, moved)
    assert ev['eliminated'] == other['eliminated']
    for a, b in zip(ev['components'], other['components'], strict=True):
        assert a['component'] == b['component'] and a['reason'] == b['reason']
        for key in ('source_forbidden', 'target_forbidden', 'fixed_colors', 'surviving_betas'):
            assert {PI[c] for c in a[key]} == set(b[key])
        if a['forced_source_pair'] is not None:
            assert {PI[c] for c in a['forced_source_pair']} == set(b['forced_source_pair'])
        by_beta = {c['beta']: c for c in b['odd_edge_cases']}
        assert {PI[c['beta']] for c in a['odd_edge_cases']} == set(by_beta)
        for case in a['odd_edge_cases']:
            twin = by_beta[PI[case['beta']]]
            assert case['frame']['eliminated'] == twin['frame']['eliminated']
            assert {tuple(sorted(RHO[i] for i in t)) for t in case['frame']['supports']} == {
                tuple(t) for t in twin['frame']['supports']}
            keys = {(tuple(map(tuple, w['frame_arcs'])), w['route']['mode'], w['route']['landing'])
                    for w in twin['frame']['witnesses']}
            for w in case['frame']['witnesses']:
                arcs = tuple(tuple(sorted(RHO[i] for i in a)) for a in w['frame_arcs'])
                assert (arcs, w['route']['mode'], RHO[w['route']['landing']]) in keys
    return dict(raw_target=raw, transported_forbidden=moved, verified=True)


def residuals(d, edges):
    return [{d, edges[0]}, *({a, b} for a, b in zip(edges, edges[1:])), {d, edges[-1]}]


def path_controls():
    rows = []
    # Enumerate unrestricted edge words independently of the alternating recipe.
    for d, length in product(sorted(U), (1, 3, 5, 7)):
        valid = []
        for edges in product(sorted(U), repeat=length):
            if all(len(e) == 2 and d in e for e in residuals(d, edges)):
                valid.append(edges)
        expected = {tuple(next(it) if i % 2 == 0 else d for i in range(length))
                    for odd in product(sorted(U-{d}), repeat=(length+1)//2)
                    for it in [iter(odd)]}
        assert set(valid) == expected
        rows.append(dict(source_color=d, length=length, valid_words=len(valid),
                         words_sha256=sha256(json.dumps(valid).encode()).hexdigest()))
    # Independent local list equalities, with every split into direct colors
    # and off-path palettes. The latter remain fixed during the path swap.
    swaps = []
    for d, beta in product(sorted(U), repeat=2):
        if d == beta:
            continue
        for direct in subsets(U-{d, beta}):
            branches = U-{d, beta}-direct
            for endpoint in (False, True):
                old_path = {beta} if endpoint else {d, beta}
                new_path = {d} if endpoint else {d, beta}
                old_list = U-direct-({d} if endpoint else set())
                new_list = U-direct-({beta} if endpoint else set())
                assert not branches & old_path and not branches & new_path
                assert branches | old_path == old_list
                assert branches | new_path == new_list
                swaps.append(dict(source_color=d, new_forbidden=beta, endpoint=endpoint,
                                  direct=sorted(direct), unchanged_branches=sorted(branches),
                                  original_list=sorted(old_list), switched_list=sorted(new_list)))
    assert len(swaps) == 96
    return dict(alternating_words=rows, local_palette_swaps=swaps)


def has_coloring(edges, lists, pins=None):
    """Small independent list solver for abstract Gallai controls only."""
    choices = {v: set(s) for v, s in lists.items()}
    for v, c in (pins or {}).items():
        choices[v] &= {c}
    adjacency = {v: set() for v in lists}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)

    def visit(todo):
        if not todo:
            return True
        v = min(todo, key=lambda x: (len(todo[x]), x))
        for c in sorted(todo[v]):
            nxt = {w: (s-{c} if w in adjacency[v] else s) for w, s in todo.items() if w != v}
            if all(nxt.values()) and visit(nxt):
                return True
        return False

    return visit(choices)


def gallai_control(d, word, style):
    """Full ordered endpoint relation; no boundary/disk realization claim."""
    length = len(word)
    blocks = [([f'x{i}', f'x{i+1}'], {c}) for i, c in enumerate(word)]
    local = residuals(d, word)
    for j, r in enumerate(local):
        colors = sorted(U-r)
        x = f'x{j}'
        if style == 'leaf':
            blocks.append(([x, f'l{j}'], {colors[0]}))
        elif style == 'triangle':
            blocks.append(([x, f'a{j}', f'b{j}'], set(colors)))
        elif style == 'nested':
            blocks.extend([([x, f'a{j}'], {colors[0]}),
                           ([f'a{j}', f'b{j}', f'c{j}'], {d, colors[1]}),
                           ([f'c{j}', f'e{j}'], {colors[0]})])
        else:
            assert style == 'bare'
    edges, lists = set(), {}
    for vertices, palette in blocks:
        for v in vertices:
            assert not lists.setdefault(v, set()) & palette
            lists[v].update(palette)
        for a, b in zip(vertices, vertices[1:]+vertices[:1]):
            edges.add(tuple(sorted((a, b))))
    assert not has_coloring(edges, lists)
    base = {v: s | ({d} if v in ('x0', f'x{length}') else set()) for v, s in lists.items()}
    relation = [(a, b) for a, b in product(sorted(U), repeat=2)
                if has_coloring(edges, base, {'x0': a, f'x{length}': b})]
    assert relation
    bans = set.intersection(*(set(t) for t in relation))
    expected = {d, word[0]} if len(set(word[::2])) == 1 else {d}
    assert bans == expected
    return dict(source_color=d, edge_palettes=word, branch_style=style,
                blocks=[dict(vertices=v, palette=sorted(p)) for v, p in blocks],
                edges=sorted(edges), base_lists={v: sorted(s) for v, s in base.items()},
                ordered_endpoint_relation=relation, forbidden=sorted(bans),
                scope='abstract degree-list control, not an original boundary source')


def minor_control(record, component, witness, length, edge_index, styles, suppliers):
    assert length % 2 == edge_index % 2 == 1 and 1 <= edge_index <= length
    supports = record['supports']
    root, other = ROOTS[component], ROOTS[1-component]
    arcs = witness['frame_arcs']
    verify_arcs([a[0] for a in arcs], arcs)
    edges = set()

    def edge(a, b):
        assert a != b
        edges.add(tuple(sorted((a, b))))

    for a, b in FRAME_EDGES:
        edge(f'b{a}', f'b{b}')
    edge('z', 'w')
    for k, r in enumerate(ROOTS):
        for s in supports[3*k+1:3*k+3]:
            edge(r, f'b{s[0]}')
    path = [f'x{i}' for i in range(length+1)]
    for a, b in zip([root]+path, path+[root]):
        edge(a, b)
    for a, b in ((other, 'other0'), ('other0', 'other1'), ('other1', other)):
        edge(a, b)
    for h in supports[3*(1-component)]:
        edge('other0', f'b{h}')
    bags = [{x} for x in path]
    tethers = []
    indices = (edge_index-1, edge_index)
    for j, style, pair in zip(indices, styles, suppliers, strict=True):
        assert all(h in supports[3*component] and h in arc for h, arc in zip(pair, arcs[:2]))
        x = path[j]
        a, b = (f'b{h}' for h in pair)
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
    for j in set(range(length+1))-set(indices):
        edge(path[j], path[j]+'_tail')
        bags[j].add(path[j]+'_tail')
    for h in supports[3*component]:
        edge('x0', f'b{h}')
    route = witness['route']['path']
    assert all(tuple(sorted(e)) in edges for e in zip(route, route[1:]))
    branch_sets = [bags[j] for j in indices] + [
        set(path)-{path[j] for j in indices} | set(route) | {f'b{h}' for h in arcs[2]},
        {f'b{h}' for h in arcs[0]}, {f'b{h}' for h in arcs[1]}]
    adjacencies = verify_minor(edges, branch_sets)
    for reflect, swap in product((False, True), repeat=2):
        def rename(v):
            if reflect and v.startswith('b') and v[1:].isdigit():
                return f'b{RHO[int(v[1:])]}'
            return {'z': 'w', 'w': 'z'}.get(v, v) if swap else v
        verify_minor({tuple(sorted((rename(a), rename(b)))) for a, b in edges},
                     [{rename(v) for v in bag} for bag in branch_sets])
    return dict(record_id=record['id'], component=component, length=length,
                odd_edge_index=edge_index, styles=styles, suppliers=suppliers,
                frame_arcs=arcs, original_external_route=witness['route'],
                edges=sorted(edges), path_bags=[sorted(b) for b in bags],
                actual_tether_routes=tethers, branch_sets=[sorted(b) for b in branch_sets],
                adjacencies=adjacencies, root_swap_and_reflection_verified=True,
                scope='original-edge topology skeleton, not a degree-list source')


def negative_controls(originals, controls):
    result = []
    r = originals[54]
    row, bans = (0, 1, 0, 2, 1), [[2, 3], [3]]
    c = evidence(r, row, bans)['components'][0]
    assert c['forced_source_pair'] == [2, 3]
    assert not next(b for b in c['odd_edge_cases'] if b['beta'] == 2)['frame']['eliminated']
    result.append('remaining_beta_two_is_not_itself_a_frame_minor')
    assert not evidence(r, Q, [[3], [3]])['components']
    result.append('singleton_target_does_not_supply_a_pair_path')
    r5 = originals[5]
    assert not evidence(r5, (0, 1, 2, 1, 2), [[1], [0, 3]])['components']
    result.append('nonconserved_source_ban_does_not_allow_path_induction')
    variable = gallai_control(3, (2, 3, 1), 'nested')
    assert variable['forbidden'] == [3]
    result.append('first_beta_two_does_not_force_later_odd_beta_two')
    # An even path with a constant two-color residual accepts when both
    # endpoints are forced to the same color: odd length is essential.
    assert has_coloring({('a', 'b'), ('b', 'c')}, {'a': {3}, 'b': {2, 3}, 'c': {3}})
    result.append('even_path_does_not_force_second_ban')
    base = next(c for c in controls if c['length'] == 5 and c['odd_edge_index'] == 3
                and c['styles'] == ('direct', 'direct') and c['suppliers'] == ((0, 4), (2, 4)))
    edges = set(map(tuple, base['edges']))
    bags = list(map(set, base['branch_sets']))
    for name, edge in (
        ('missing_original_zw', ('w', 'z')),
        ('missing_other_component_tether', ('b3', 'other0')),
        ('missing_selected_odd_bridge', ('x2', 'x3')),
        ('missing_left_return_edge', ('x1', 'x2')),
        ('missing_right_return_edge', ('x3', 'x4')),
        ('missing_actual_supplier', ('b4', 'x3')),
        ('broken_fixed_frame_arc', ('b0', 'b1')),
    ):
        try:
            verify_minor(edges-{edge}, bags)
        except AssertionError:
            result.append(name)
        else:
            raise AssertionError(name)
    try:
        verify_minor(edges, [bags[0] | {'z'}, *bags[1:]])
    except AssertionError:
        result.append('overlapping_branch_sets')
    else:
        raise AssertionError('overlapping_branch_sets')
    return dict(names=result, variable_odd_palette_control=variable)


def build():
    data = json.loads(SOURCE.read_text())
    assert data['source_sha256'] == sha256((ROOT/'scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py').read_bytes()).hexdigest()
    assert data['previous_sha256'] == sha256((ROOT/data['previous_path']).read_bytes()).hexdigest()
    assert data['original_source_sha256'] == sha256((ROOT/data['original_source_path']).read_bytes()).hexdigest()
    for path, digest in data['inputs_sha256'].items():
        assert digest == sha256((ROOT/path).read_bytes()).hexdigest()
    assert data['summary']['final_accepts'] == 640
    originals = [e['inherited_record']['original_record'] for e in data['records']]
    assert [r['id'] for r in originals] == list(range(322))
    records, new_cases = [], []
    join_count = failure_count = 0
    for old, r in zip(data['records'], originals, strict=True):
        targets = []
        for n, target in enumerate(r['targets']):
            fresh = row_evidence(data['original_frontier'][r['source_id']],
                                 tuple(map(tuple, r['supports'])), tuple(target['row']))
            assert canonical(fresh) == target
            join_count += len(target['joins'])
            cases = []
            by_index = {c['original_join_index']: c for c in old['targets'][n]['cases']}
            for j, join in enumerate(target['joins']):
                if join['root_pairs']:
                    continue
                failure_count += 1
                previous = by_index[j]
                assert previous['original_join'] == join
                bridge = bridge_evidence(r, target['row'], join['forbidden_sets'])
                endpoint = endpoint_evidence(r, target['row'], join['forbidden_sets'])
                assert canonical(endpoint) == previous['endpoint_evidence']
                assert previous['inherited_eliminated'] == bridge['eliminated']
                assert previous['eliminated'] == (bridge['eliminated'] or endpoint['eliminated'])
                ev = None
                if not previous['eliminated']:
                    ev = evidence(r, target['row'], join['forbidden_sets'])
                    assert ev['eliminated']
                    audit = reflection_audit(r, target['row'], join['forbidden_sets'], ev, originals)
                    new_cases.append(dict(record_id=r['id'], target_index=n, row=target['row'],
                                          original_join_index=j, original_join=join,
                                          path_evidence=ev, reflection=audit))
                cases.append(dict(original_join_index=j, original_join=join,
                                  inherited_eliminated=previous['eliminated'], path_evidence=ev,
                                  eliminated=previous['eliminated'] or ev['eliminated']))
            assert old['targets'][n]['status'] == ('accept' if all(c['inherited_eliminated'] for c in cases) else 'unresolved')
            targets.append(dict(row=target['row'], inherited_status=old['targets'][n]['status'],
                                status='accept' if all(c['eliminated'] for c in cases) else 'unresolved', cases=cases))
        records.append(dict(id=r['id'], original_record=r, targets=targets))
    assert [(c['record_id'], c['target_index']) for c in new_cases] == [(54, 0), (68, 1), (173, 1), (256, 0)]
    for new in new_cases:
        r = originals[new['record_id']]
        twin = originals[r['root_swapped_id']]
        rev = evidence(twin, new['row'], new['original_join']['forbidden_sets'][::-1])
        assert rev['eliminated']
        for a, b in zip(new['path_evidence']['components'], rev['components'], strict=True):
            assert a['component'] == 1-b['component']
            for key in ('source_forbidden', 'target_forbidden', 'surviving_betas', 'forced_source_pair', 'odd_edge_cases'):
                def swap_roots(value):
                    if isinstance(value, str):
                        return {'z': 'w', 'w': 'z'}.get(value, value)
                    if isinstance(value, (list, tuple)):
                        return [swap_roots(v) for v in value]
                    if isinstance(value, dict):
                        return {k: swap_roots(v) for k, v in value.items()}
                    return value
                assert canonical(swap_roots(a[key])) == canonical(b[key])
    classes = Counter('/'.join(t['status'] for t in r['targets']) for r in records)
    assert classes == {'accept/accept': 322}
    for r in records:
        assert [t['status'] for t in r['targets']] == [t['status'] for t in records[r['original_record']['root_swapped_id']]['targets']]
    controls = []
    r = originals[54]
    c = new_cases[0]['path_evidence']['components'][0]
    bc = next(b for b in c['odd_edge_cases'] if b['beta'] == 1)
    witness = bc['frame']['witnesses'][0]
    for length in (1, 3, 5, 9):
        for index, styles, a, b in product(range(1, length+1, 2), product(STYLES, repeat=2), (0, 2), (0, 2)):
            controls.append(minor_control(r, 0, witness, length, index, styles, ((a, 4), (b, 4))))
    gallai = [gallai_control(d, tuple(beta if i % 2 == 0 else d for i in range(length)), style)
              for d, beta in product(sorted(U), repeat=2) if d != beta
              for length, style in product((1, 3, 5, 9), ('bare', 'leaf', 'triangle', 'nested'))]
    negatives = negative_controls(originals, controls)
    summary = dict(original_records=322, target_queries=644, inherited_accepts=640,
                   inherited_unresolved=4, new_accepts=len(new_cases), final_accepts=644,
                   new_source_exclusions=0, both_targets_proved=322, unresolved_queries=0,
                   target_classes=dict(classes), complete_joins_replayed=join_count,
                   original_failing_joins=failure_count, inherited_failing_joins_eliminated=156,
                   new_failing_joins_eliminated=len(new_cases), root_swap_checks=322,
                   new_candidate_root_swap_checks=len(new_cases), literal_reflection_checks=len(new_cases),
                   minor_controls=len(controls), complete_relation_controls=len(gallai),
                   negative_controls=len(negatives['names']))
    assert join_count == 2892 and failure_count == 160 and len(controls) == 704 and len(gallai) == 192
    inputs = sorted(set(data['inputs_sha256']) | {
        'scripts/c5_adjacent_degree5_no_mixed_t2_endpoints.py',
        'scripts/c5_adjacent_degree5_no_mixed_t2_bridge.py'})
    return dict(schema=1, scope='specified two-row separation for no-mixed t=2; no source realizability or Lean theorem',
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                previous_path=str(SOURCE.relative_to(ROOT)), previous_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
                original_source_path=data['original_source_path'], original_source_sha256=data['original_source_sha256'],
                inputs_sha256={p: sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
                original_frontier=data['original_frontier'], source_fibers=data['source_fibers'],
                q_complete_schemas=data['q_complete_schemas'], rotation_templates=data['rotation_templates'],
                summary=summary, records=records, new_cases=new_cases, open_queries=[],
                path_controls=path_controls(), complete_relation_controls=gallai,
                minor_controls=controls, negative_controls=negatives)


def render(data):
    lines = ['# 無 mixed 兩側 t=2：整條原 bridge 路徑與第二禁色', '',
             '原 322 份全保留；新增 4 個延拓，644／644 查詢全證，0 個未決。',
             '來源排除仍為 0；必要資料與有限控制都不是 disk 實現。', '',
             '| 原 ID | 原 sides | 原 actual supports | 前層 p₁/p₂ | 本輪 p₁/p₂ |',
             '| ---: | --- | --- | --- | --- |']
    for r in data['records']:
        o = r['original_record']
        support = '/'.join(''.join(map(str, s)) for s in o['supports'])
        old = '/'.join('A' if t['inherited_status'] == 'accept' else '?' for t in r['targets'])
        lines.append(f"| {r['id']} | {o['source_side_ids']} | {support} | {old} | A/A |")
    lines += ['', '原記錄、完整 schemas／rotations、joins、palettes 與 minor 證書見 [JSON](observations.json)。',
              '任意大小證明、出口接合及信任界線見 [報告](../../docs/c5_adjacent_degree5_no_mixed_t2_path_palettes.md)。', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    for path, payload in ((OUT, json.dumps(data, sort_keys=True, indent=2)+'\n'), (TABLE, render(data))):
        if args.check:
            assert path.read_bytes() == payload.encode(), f'certificate differs: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(data['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
