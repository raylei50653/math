#!/usr/bin/env python3
"""Concrete-source cross-round audit, retaining full same-state interfaces.

The two saved sources are calibration controls. Neither is a legal fully
blocked period-four source. All whole-source fibres/actions remain available
by immutable SHA-256 plus JSON pointers into the upstream certificate.
"""
from __future__ import annotations

import argparse
from collections import deque
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

from c5_d2_separation import parts, edge, sides

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'audits/2026-10-30-c5-six-cross-round'
SOURCE = ROOT / 'audits/2026-10-30-c5-d2-separation/controls.json'
SEPARATION = ROOT / 'audits/2026-10-30-c5-d2-separation/separation-certificate.json'
PAIRS = ((0, 3), (1, 3), (1, 2), (0, 2), (0, 3))
ROOT_POSITIONS = (2, 4, 1, 3, 0)
ALIGN = (2, 3, 1, 0)


def power(perm, exponent):
    result = list(range(4))
    for _ in range(exponent % 4):
        result = [perm[x] for x in result]
    return result


def swap(colors, order, component, pair):
    component = set(component)
    return [sum(pair) - value if x in component else value
            for x, value in zip(order, colors)]


def proper(colors, order, graph):
    ix = dict(zip(order, colors))
    return all(ix[x] != ix[y] for x in order for y in graph[x])


def path_between(graph, allowed, a, b):
    previous, todo = {a: None}, deque([a])
    while todo:
        x = todo.popleft()
        if x == b:
            route = []
            while x is not None:
                route.append(x)
                x = previous[x]
            return list(reversed(route))
        for y in sorted(graph[x] & set(allowed)):
            if y not in previous:
                previous[y] = x
                todo.append(y)
    raise AssertionError('requested path does not exist in this full colouring')


def build_timeline(control, graph):
    """Retain normalized-round records and a continuous literal swap history."""
    order, boundary = control['exterior_vertices'], control['boundary']
    snapshots, moves, normalization_events = [], [], []
    continuous = [control['normalized_iterates'][0]]
    round_rows = list(control['rounds'])
    if 'failed_next_round' in control:
        round_rows.append(control['failed_next_round'])
    for r, round_row in enumerate(round_rows):
        c = list(round_row['source_colors'])
        back = power(ALIGN, -r)
        assert [back[value] for value in c] == continuous[-1]
        def snapshot(t, colors):
            sid = len(snapshots)
            snapshots.append(dict(snapshot_id=sid, round=r, time=t,
                round_defined=round_row['defined'], colors=list(colors),
                continuous_time=len(continuous) - 1,
                continuous_colors=[back[value] for value in colors]))
            return sid
        before_id = snapshot(0, c)
        for t, move in enumerate(round_row['moves']):
            pair = list(PAIRS[t])
            root = boundary[ROOT_POSITIONS[t]]
            ix = dict(zip(order, c))
            active = {x for x in order if ix[x] in pair}
            comp = next(p for p in parts(graph, active) if root in p)
            assert comp == move['component']
            assert move['pair'] == pair and move['root'] == root
            hit = sorted(set(comp) & set(boundary))
            expected = swap(c, order, comp, pair)
            assert proper(expected, order, graph) and expected == move['colors']
            lifted_pair = sorted(back[value] for value in pair)
            lifted = swap(continuous[-1], order, comp, lifted_pair)
            assert lifted == [back[value] for value in expected]
            assert proper(lifted, order, graph)
            continuous.append(lifted)
            after_id = snapshot(t + 1, expected)
            moves.append(dict(move_id=len(moves), round=r, step=t + 1,
                pair=pair, root=root, component=comp, boundary_intersection=hit,
                prescribed_singleton=hit == [root],
                source_snapshot_id=before_id, target_snapshot_id=after_id,
                continuous_pair=lifted_pair, continuous_time=len(continuous) - 2,
                same_state_paths_to_boundary=[dict(target=x, path=path_between(graph, active, root, x)) for x in hit]))
            before_id, c = after_id, expected
        if round_row['defined']:
            normalized = [ALIGN[value] for value in c]
            assert normalized == round_row['normalized_colors']
            normalization_events.append(dict(round=r, permutation=list(ALIGN),
                raw_colors=c, normalized_colors=normalized,
                continuous_time=len(continuous) - 1))
        else:
            assert moves[-1]['prescribed_singleton'] is False
            assert all(row['prescribed_singleton'] for row in moves[:-1])
    assert all(row['prescribed_singleton'] for row in moves if control['premise_flags']['least_h_period4'])
    return snapshots, moves, normalization_events, continuous


def side_component_rows(graph, vertices, interface, active):
    answer = []
    for component in parts(graph, set(vertices) & active):
        original_attachments = sorted(set().union(*(graph[x] for x in component)) - set(component))
        all_cross = sorted([x, y] for x in component for y in graph[x] & set(interface))
        active_cross = [xy for xy in all_cross if xy[1] in active]
        answer.append(dict(component=component, all_original_attachments=original_attachments,
            all_interface_cross_edges=all_cross,
            active_interface_cross_edges=active_cross,
            active_interface_attachments=sorted({y for _, y in active_cross})))
    return answer


def glue_snapshot(region, graph, order, snapshot):
    ix = dict(zip(order, snapshot['colors']))
    C, inner, outer = set(region['cycle']), set(region['inner']), set(region['outer'])
    assert C | inner | outer == set(order)
    assert not (C & inner or C & outer or inner & outer)
    assert all(not graph[x] & outer for x in inner)
    pair_rows = []
    for pair in combinations(range(4), 2):
        active = {x for x in order if ix[x] in pair}
        left = side_component_rows(graph, inner, C, active)
        right = side_component_rows(graph, outer, C, active)
        interface_components = parts(graph, C & active)
        full = parts(graph, active)
        # Contract both open sides. Empty-contact side components are retained.
        aux, expand = {}, {}
        for x in C & active:
            aux[x] = graph[x] & C & active
            expand[x] = {x}
        next_id = max(order) + 1
        for row in left + right:
            aux[next_id] = set(row['active_interface_attachments'])
            expand[next_id] = set(row['component'])
            for x in aux[next_id]:
                aux[x].add(next_id)
            next_id += 1
        recomposed = sorted(sorted(set().union(*(expand[x] for x in component)))
                            for component in parts(aux, aux))
        assert recomposed == full
        pair_rows.append(dict(pair=list(pair), inner_components=left,
            interface_components=interface_components, outer_components=right,
            full_components=full, recomposed_components=recomposed,
            full_three_way_intersections=[dict(component=component,
                inner=sorted(set(component) & inner), interface=sorted(set(component) & C),
                outer=sorted(set(component) & outer)) for component in full]))
    return dict(snapshot_id=snapshot['snapshot_id'], pairs=pair_rows)


def vertex_words(control, moves, continuous):
    order = control['exterior_vertices']
    answer = []
    for j, vertex in enumerate(order):
        membership = [int(vertex in move['component']) for move in moves]
        permutation = list(range(4))
        trajectory = [continuous[0][j]]
        round_permutations = []
        for k, (bit, move) in enumerate(zip(membership, moves)):
            if bit:
                a, b = move['continuous_pair']
                permutation = [a + b - value if value in (a, b) else value for value in permutation]
            assert permutation[continuous[0][j]] == continuous[k + 1][j]
            trajectory.append(continuous[k + 1][j])
            if (k + 1) % 5 == 0:
                round_permutations.append(list(permutation))
        answer.append(dict(vertex=vertex, membership_word=''.join(map(str, membership)),
            continuous_colors=trajectory, induced_permutation=permutation,
            fixes_initial_color=permutation[continuous[0][j]] == continuous[0][j],
            permutation_is_identity=permutation == list(range(4)),
            prefix_permutations_after_each_complete_round=round_permutations))
    return answer


def shortest_escape(control, graph, start):
    """Literal BFS; every edge swaps exactly one current complete component."""
    order, boundary = control['exterior_vertices'], control['boundary']
    ix = {x: j for j, x in enumerate(order)}
    start = tuple(start)
    queue, previous = deque([start]), {start: None}
    via = {}
    target = None
    while queue:
        c = queue.popleft()
        if len({c[ix[x]] for x in boundary}) == 3:
            target = c
            break
        for pair in combinations(range(4), 2):
            active = {x for x in order if c[ix[x]] in pair}
            for component in parts(graph, active):
                nxt = tuple(swap(c, order, component, pair))
                if nxt not in previous:
                    previous[nxt] = c
                    via[nxt] = dict(pair=list(pair), component=component,
                        source_colors=list(c), target_colors=list(nxt),
                        boundary_intersection=sorted(set(component) & set(boundary)))
                    queue.append(nxt)
    assert target is not None
    route, current = [], target
    while previous[current] is not None:
        route.append(via[current])
        current = previous[current]
    route.reverse()
    return dict(source_colors=list(start), target_colors=list(target),
        length=len(route), literal_moves=route, explored_literal_states=len(previous),
        target_boundary_word=[target[ix[x]] for x in boundary],
        search_complete_through_shorter_distances=True)


def differences_and_regions(control, separation, graph):
    order, center = control['exterior_vertices'], control['center']
    fullgraph = {x: set(row) for x, row in enumerate(control['rotation'])}
    regions, region_ids, differences = [], {}, []
    for ci, comparison in enumerate(separation['comparisons']):
        source = control['comparisons'][ci]
        difference = sorted(x for x, a, b in zip(order, source['c'], source['d']) if a != b)
        assert difference == comparison['difference_vertices']
        component_rows = []
        for qi, old in enumerate(comparison['components']):
            q, a = old['vertices'], old['attachments']
            assert a == sorted(set().union(*(fullgraph[x] for x in q)) - set(q))
            sep = old['v_facing_boundary']['selected_original_separator']
            C = sep['cycle']
            key = (tuple(q), tuple(C))
            if key not in region_ids:
                region_ids[key] = len(regions)
                inner = sep['opposite_side']
                outer = sorted(set(sep['center_side']) - {center})
                assert set(q) <= set(inner)
                assert not set(a) - set(C) if len(a) == 6 else True
                all_components = parts(fullgraph, set(fullgraph) - set(C))
                region = dict(region_id=len(regions), Q=q, attachments=a, cycle=C,
                    inner=inner, outer=outer, center_side=sep['center_side'],
                    full_open_side_components=[dict(vertices=p,
                        side='center' if set(p) <= set(sep['center_side']) else 'opposite')
                        for p in all_components],
                    cycle_induced_edges=sorted([x, y] for x in C for y in fullgraph[x] & set(C) if x < y),
                    cycle_is_chordless=len([1 for x in C for y in fullgraph[x] & set(C) if x < y]) == len(C),
                    original_face_ids_meeting_Q=old['incident_original_face_ids'],
                    original_face_ids_on_inner_side=[j for j, face in enumerate(control['sphere_faces'])
                        if set(face) <= set(C) | set(inner)],
                    source_comparison_refs=[])
                region['Q_equals_entire_inner_open_side'] = set(q) == set(inner)
                region['inner_open_side_connected'] = len(parts(fullgraph, inner)) == 1
                if region['cycle_is_chordless'] and set(a) == set(C):
                    assert region['inner_open_side_connected']
                    assert region['Q_equals_entire_inner_open_side']
                region['geometry_scope'] = ('For this concrete source, Q is the complete connected inner open side. '
                    'The paper implication uses an induced original separator and all original Q attachments.')
                assert all(set(item['vertices']) <= (set(sep['center_side']) if item['side'] == 'center' else set(inner))
                           for item in region['full_open_side_components'])
                regions.append(region)
            rid = region_ids[key]
            regions[rid]['source_comparison_refs'].append(dict(comparison_index=ci, component_index=qi))
            row = deepcopy(old)
            row['region_id'] = rid
            row['inner_vertices_not_in_Q'] = sorted(set(regions[rid]['inner']) - set(q))
            row['side_components_at_this_comparison'] = [dict(**item,
                changed_vertices=sorted(set(item['vertices']) & set(difference)),
                fixed_vertices=sorted(set(item['vertices']) - set(difference)),
                other_difference_components=[other['vertices'] for other in comparison['components']
                    if other['vertices'] != q and set(other['vertices']) & set(item['vertices'])])
                for item in regions[rid]['full_open_side_components']]
            component_rows.append(row)
        differences.append(dict(comparison_index=ci, source_iterate=comparison['source_iterate'],
            target_iterate=comparison['target_iterate'], D=difference,
            components=component_rows, fixed_five_cycles=comparison['fixed_five_cycles'],
            rigidity_violations=comparison['rigidity_violations']))
    return differences, regions


def synchronous_difference_traces(control, graph, snapshots, moves):
    """Exact same-step update between two current complete colourings.

    For a common pair P and actual rooted components K,L, a membership
    difference toggles equality only when both current colours lie in P.
    No component is transported through H by this identity.
    """
    order = control['exterior_vertices']
    lookup = {(state['round'], state['time']): state for state in snapshots}
    move_lookup = {(move['round'], move['step']): move for move in moves}
    period4 = control['premise_flags']['least_h_period4']
    starts = list(range(4)) if period4 else [0]
    result = []
    for r in starts:
        s = (r + 2) % 4 if period4 else r + 2
        steps = []
        for t in range(1, 6):
            if (r, t) not in move_lookup or (s, t) not in move_lookup:
                break
            first, second = move_lookup[r, t], move_lookup[s, t]
            assert first['pair'] == second['pair']
            pair = first['pair']
            a, b = lookup[r, t - 1], lookup[s, t - 1]
            aa, bb = lookup[r, t], lookup[s, t]
            av, bv = dict(zip(order, a['colors'])), dict(zip(order, b['colors']))
            before = {x for x in order if av[x] != bv[x]}
            after = {x for x, c, d in zip(order, aa['colors'], bb['colors']) if c != d}
            K, L = set(first['component']), set(second['component'])
            J = {x for x in order if av[x] in pair and bv[x] in pair}
            toggle = (K ^ L) & J
            assert after == before ^ toggle
            steps.append(dict(step=t, pair=pair,
                first_source_snapshot_id=a['snapshot_id'], second_source_snapshot_id=b['snapshot_id'],
                first_target_snapshot_id=aa['snapshot_id'], second_target_snapshot_id=bb['snapshot_id'],
                first_move_id=first['move_id'], second_move_id=second['move_id'],
                K=sorted(K), L=sorted(L), both_colors_in_pair_J=sorted(J),
                K_symmetric_difference_L=sorted(K ^ L),
                equality_toggle_vertices=sorted(toggle), D_before=sorted(before), D_after=sorted(after),
                born=sorted(after - before), died=sorted(before - after),
                difference_components_before=parts(graph, before),
                difference_components_after=parts(graph, after),
                both_exchanges_prescribed_singleton=first['prescribed_singleton'] and second['prescribed_singleton']))
        assert steps
        initial = steps[0]['D_before']
        terminal = steps[-1]['D_after']
        complete = len(steps) == 5
        if complete:
            first_normalized = [ALIGN[value] for value in lookup[r, 5]['colors']]
            second_normalized = [ALIGN[value] for value in lookup[s, 5]['colors']]
            normalized_difference = sorted(x for x, c, d in zip(order, first_normalized, second_normalized) if c != d)
            assert terminal == normalized_difference
            target_pair = [(r + 1) % 4, (s + 1) % 4]
            target_initial = control['normalized_iterates'][target_pair[0]]
            target_second = control['normalized_iterates'][target_pair[1]]
            assert first_normalized == target_initial and second_normalized == target_second
        else:
            normalized_difference, target_pair = None, None
        result.append(dict(first_round=r, second_round=s, steps=steps,
            initial_difference=initial, terminal_difference=terminal,
            compared_steps=len(steps), complete_five_step_pair=complete,
            prescribed_continuation_legal=all(step['both_exchanges_prescribed_singleton'] for step in steps),
            common_alignment_applied=complete,
            normalized_terminal_difference=normalized_difference,
            target_normalized_iterate_pair=target_pair,
            produces_next_parity_difference=complete,
            formula='D_after = D_before symmetric_difference ((K symmetric_difference L) intersection J)',
            scope=('Actual period-four pair: common normalization leaves the difference set unchanged.' if complete else
                'Only the saved two-return/failed-third-return prefix is compared. The third compared swap is legal as a Kempe swap but fails the prescribed singleton condition. No next normalized parity difference or D1 is asserted.')))
    return result


def failure_escape(control, graph, snapshots, moves):
    """Alternate exchange before a first non-singleton prescribed component."""
    bad = [move for move in moves if not move['prescribed_singleton']]
    if not bad:
        return None
    assert len(bad) == 1
    failed = bad[0]
    order, boundary = control['exterior_vertices'], control['boundary']
    current = snapshots[failed['source_snapshot_id']]['colors']
    color = dict(zip(order, current))
    pair = sorted(set(range(4)) - set(failed['pair']))
    roots = [x for x in boundary if color[x] in pair]
    assert len(roots) == 2
    active = {x for x in order if color[x] in pair}
    complete = parts(graph, active)
    first = next(component for component in complete if roots[0] in component)
    second = next(component for component in complete if roots[1] in component)
    assert first != second
    assert set(first) & set(boundary) == {roots[0]}
    target = swap(current, order, first, pair)
    assert proper(target, order, graph)
    assert len({target[order.index(x)] for x in boundary}) == 3
    prefix = [move for move in moves if move['round'] == failed['round'] and move['step'] < failed['step']]
    route = [dict(pair=move['pair'], component=move['component'],
        source_colors=snapshots[move['source_snapshot_id']]['colors'],
        target_colors=snapshots[move['target_snapshot_id']]['colors']) for move in prefix]
    route.append(dict(pair=pair, component=first, source_colors=current, target_colors=target))
    return dict(failed_move_id=failed['move_id'], source_snapshot_id=failed['source_snapshot_id'],
        alternate_pair=pair, alternate_root=roots[0], other_complementary_boundary_root=roots[1],
        all_actual_complementary_components=complete,
        alternate_component=first, other_complementary_component=second,
        two_complementary_roots_disconnected_in_this_full_coloring=True,
        source_normalized_iterate=failed['round'],
        source_colors=control['normalized_iterates'][failed['round']],
        literal_moves=route, target_colors=target,
        target_boundary_word=[target[order.index(x)] for x in boundary],
        contract='The prescribed failing exchange is not executed in this route. Every listed exchange is one actual component of the immediately preceding complete coloring.')


def disk_fibres(control, regions, graph):
    """All proper inner-disk colourings, including globally unextendible rows.

    The direct original-edge enumeration is independent of full-O extendibility.
    Full source lifts are attached afterwards; they never filter a disk row.
    """
    exterior = control['exterior_vertices']
    ext_ix = {x: j for j, x in enumerate(exterior)}
    full_lifts = []
    for sid, state in enumerate(control['full_kempe_component']['normalized_states']):
        for perm in permutations(range(4)):
            full_lifts.append((dict(normalized_state=sid, global_permutation=list(perm)),
                               [perm[value] for value in state]))
    output = []
    for region in regions:
        C, inner = region['cycle'], region['inner']
        disk_order = C + sorted(inner)
        words = {}
        for i, c in enumerate(control['normalized_iterates']):
            word = tuple(c[ext_ix[x]] for x in C)
            words.setdefault(word, []).append(i)
        fibres = []
        for word, endpoints in sorted(words.items()):
            current = dict(zip(C, word))
            rows = []
            def enumerate_disk(j):
                if j == len(inner):
                    rows.append([current[x] for x in disk_order])
                    return
                x = inner[j]
                forbidden = {current[y] for y in graph[x] if y in current}
                for color in range(4):
                    if color not in forbidden:
                        current[x] = color
                        enumerate_disk(j + 1)
                current.pop(x, None)
            enumerate_disk(0)
            rows.sort()
            assert len(rows) == len({tuple(row) for row in rows})
            lifts_by_disk = {tuple(row): [] for row in rows}
            for ref, c in full_lifts:
                projected = tuple(c[ext_ix[x]] for x in disk_order)
                if tuple(projected[:len(C)]) == word:
                    assert projected in lifts_by_disk
                    lifts_by_disk[projected].append(ref)
            row_ids = {tuple(row): i for i, row in enumerate(rows)}
            disk_graph = {x: graph[x] & set(disk_order) for x in disk_order}
            fixed_actions, disk_components = [], []
            action_graph = {i: set() for i in range(len(rows))}
            for i, row in enumerate(rows):
                color = dict(zip(disk_order, row))
                pair_components, actions = [], []
                for pair in combinations(range(4), 2):
                    components = parts(disk_graph, {x for x in disk_order if color[x] in pair})
                    pair_components.append(dict(pair=list(pair), components=components))
                    for component in components:
                        if not set(component) & set(C):
                            target = swap(row, disk_order, component, pair)
                            tid = row_ids[tuple(target)]
                            actions.append(dict(pair=list(pair), component=component, target_disk_row=tid,
                                is_actual_full_O_component_by_interface_separation=True))
                            action_graph[i].add(tid)
                fixed_actions.append(actions)
                disk_components.append(pair_components)
            local_classes = parts(action_graph, action_graph)
            endpoint_rows = []
            for endpoint in endpoints:
                full = control['normalized_iterates'][endpoint]
                projected = tuple(full[ext_ix[x]] for x in disk_order)
                row_id = row_ids[projected]
                endpoint_rows.append(dict(normalized_iterate=endpoint, disk_row_id=row_id,
                    interior_Kempe_class_id=next(j for j, cc in enumerate(local_classes) if row_id in cc)))
            fibres.append(dict(cycle_word=list(word), normalized_iterate_refs=endpoints,
                complete_disk_rows=[dict(disk_row_id=i, disk_colors=row,
                    full_source_lifts_refs=lifts_by_disk[tuple(row)],
                    all_six_pairs_disk_components=disk_components[i],
                    boundary_fixed_interior_Kempe_actions=fixed_actions[i]) for i, row in enumerate(rows)],
                boundary_fixed_interior_Kempe_classes=local_classes,
                normalized_endpoint_disk_rows=endpoint_rows,
                complete_disk_fibre_size=len(rows),
                globally_extendible_disk_row_count=sum(bool(lifts_by_disk[tuple(row)]) for row in rows),
                contract='Direct complete disk enumeration with fixed literal cycle word. Empty full-source lift lists are retained; whole-O extendibility is attached only afterwards.'))
        output.append(dict(region_id=region['region_id'], disk_vertex_order=disk_order,
            disk_original_edges=sorted([x, y] for x in disk_order for y in graph[x] & set(disk_order) if x < y),
            fibres=fibres))
    return output


def inspect(control, separation, index):
    order = control['exterior_vertices']
    graph = {x: set(control['rotation'][x]) - {control['center']} for x in order}
    differences, regions = differences_and_regions(control, separation, graph)
    snapshots, moves, events, continuous = build_timeline(control, graph)
    gluing = [dict(region_id=region['region_id'], snapshots=[glue_snapshot(region, graph, order, state)
               for state in snapshots]) for region in regions]
    region_moves = []
    for region in regions:
        C, inner, outer = set(region['cycle']), set(region['inner']), set(region['outer'])
        region_moves.append(dict(region_id=region['region_id'],
            moves=[dict(move_id=move['move_id'],
                component_in_Q=sorted(set(move['component']) & set(region['Q'])),
                component_in_inner=sorted(set(move['component']) & inner),
                component_on_cycle=sorted(set(move['component']) & C),
                component_in_outer=sorted(set(move['component']) & outer),
                cycle_changed_vertices=sorted(set(move['component']) & C)) for move in moves],
            normalized_cycle_colors=[[c[order.index(x)] for x in region['cycle']]
                for c in control['normalized_iterates']],
            fixed_on_source_comparisons=[dict(**ref, fixed=True) for ref in region['source_comparison_refs']],
            same_cycle_colors_at_all_normalized_iterates=len({tuple(c[order.index(x)] for x in region['cycle'])
                for c in control['normalized_iterates']}) == 1))
    intersections = []
    for i, first in enumerate(differences):
        for j, second in enumerate(differences[i + 1:], i + 1):
            intersections.append(dict(first_comparison=i, second_comparison=j,
                D_intersection=sorted(set(first['D']) & set(second['D'])),
                D_equal=first['D'] == second['D'],
                component_intersections=[dict(first_component=a, second_component=b,
                    intersection=sorted(set(q['vertices']) & set(r['vertices'])))
                    for a, q in enumerate(first['components']) for b, r in enumerate(second['components'])],
                contract='Set intersections only. No pointwise component transport by H is assumed.'))
    words = vertex_words(control, moves, continuous)
    closed = continuous[-1] == continuous[0]
    if control['premise_flags']['least_h_period4']:
        assert len(moves) == 20 and len(events) == 4 and closed
        assert all(w['fixes_initial_color'] for w in words)
    escapes = [dict(normalized_iterate=i, **shortest_escape(control, graph, c))
        for i, c in enumerate(control['normalized_iterates'])]
    return dict(name=control['name'], source_control_index=index,
        source_ref=dict(file=str(SOURCE.relative_to(ROOT)), json_pointer=f'/controls/{index}',
            preserves=['original_edges', 'sphere_faces', 'rotation', 'exterior_vertices', 'exterior_edges',
                      'complete_ABACD_fibre', 'full_boundary_fibres', 'full_kempe_component']),
        premise_flags=control['premise_flags'], differences=differences, regions=regions,
        snapshots=snapshots, moves=moves, normalization_events=events,
        continuous_literal_colors=continuous, region_gluing=gluing,
        region_moves=region_moves, comparison_intersections=intersections,
        vertex_words=words,
        synchronous_difference_traces=synchronous_difference_traces(control, graph, snapshots, moves),
        closure=dict(completed_rounds=len(events), actual_exchange_count=len(moves),
            prescribed_singleton_exchange_count=sum(m['prescribed_singleton'] for m in moves),
            alignment_power=power(ALIGN, len(events)),
            continuous_literal_closed=closed,
            word_requirement='Each induced permutation fixes the actual initial color; its action on unused colors need not be identity.',
            all_vertex_words_fix_initial_color=all(w['fixes_initial_color'] for w in words),
            identity_permutation_vertex_count=sum(w['permutation_is_identity'] for w in words)),
        escape_routes=escapes, first_failure_escape=failure_escape(control, graph, snapshots, moves), disk_fibres=disk_fibres(control, regions, graph),
        evidence_scope='Concrete original source. All actions and same-state paths are realized. Neither source is fully blocked; Errera fails S5. No abstract necessary model is called a source.')


def produce():
    source = json.loads(SOURCE.read_text())
    separation = json.loads(SEPARATION.read_text())
    return dict(schema='c5-six-cross-round-v1',
        provenance_inputs={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                           for p in (SOURCE, SEPARATION)},
        producer_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        controls=[inspect(c, s, i) for i, (c, s) in enumerate(zip(source['controls'], separation['controls']))],
        scope='Two preserved concrete controls. The legal n17 source fails at third-round step three; Errera is actual period four but S5-negative. No legal fully blocked period-four source or general exclusion is claimed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = produce()
    output = AUDIT / 'cross-round-certificate.json'
    encoded = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + '\n'
    if args.check:
        assert output.read_text() == encoded
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded)
    print(json.dumps(dict(status='OK', controls=[dict(name=c['name'],
        regions=len(c['regions']), snapshots=len(c['snapshots']), moves=len(c['moves']),
        gluing_pair_records=sum(len(s['pairs']) for r in c['region_gluing'] for s in r['snapshots']),
        shortest_escape_lengths=[r['length'] for r in c['escape_routes']],
        closure=c['closure']) for c in result['controls']]), sort_keys=True))


if __name__ == '__main__':
    main()
