#!/usr/bin/env python3
"""Independent replay of the frozen six-attachment cross-round controls.

The only project import is the earlier independent D2 reviewer. No producer is
imported. That reviewer reconstructs the original sphere, complete fibres and
all actual Kempe actions; the checks below additionally reconstruct the new
cross-round data directly from full colour vectors and original edges/faces.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_d2_separation_review as upstream

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'audits/2026-10-30-c5-six-cross-round'
SOURCE = ROOT / 'audits/2026-10-30-c5-d2-separation/controls.json'
SEPARATION = SOURCE.with_name('separation-certificate.json')
PAIRS = ((0, 3), (1, 3), (1, 2), (0, 2), (0, 3))
POSITIONS = (2, 4, 1, 3, 0)
ALIGN = (2, 3, 1, 0)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def parts(graph, vertices):
    """Sorted components by union-find, independently of producer traversals."""
    vertices = set(vertices)
    parent = {x: x for x in vertices}

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for x in vertices:
        for y in graph[x] & vertices:
            parent[root(x)] = root(y)
    blocks = defaultdict(list)
    for x in sorted(vertices):
        blocks[root(x)].append(x)
    return sorted(blocks.values())


def swap(graph, order, colors, pair, component):
    c = dict(zip(order, colors))
    active = {x for x in order if c[x] in pair}
    component = sorted(component)
    assert component in parts(graph, active), 'A saved exchange is not one actual full-O component'
    after = tuple(sum(pair) - c[x] if x in component else c[x] for x in order)
    assert all(after[order.index(x)] != after[order.index(y)] for x in order for y in graph[x])
    return after


def replay_source(raw):
    graph, faces, rotation, owners, third, short, s34, s5 = upstream.geometry(raw)
    order = raw['exterior_vertices']
    ograph = {x: graph[x] & set(order) for x in order}
    boundary = raw['boundary']
    position = {x: j for j, x in enumerate(order)}
    snapshots, moves, word = [], [], {x: [] for x in order}
    permutation = {x: tuple(range(4)) for x in order}
    for r, row in enumerate(raw['rounds']):
        c = tuple(row['source_colors'])
        assert c == tuple(raw['normalized_iterates'][r])
        snapshots.append(dict(round=r, time=0, colors=list(c), failed=False))
        for t, (pair, bp, saved) in enumerate(zip(PAIRS, POSITIONS, row['moves']), 1):
            active = {x for x in order if c[position[x]] in pair}
            component = next(p for p in parts(ograph, active) if boundary[bp] in p)
            hit = sorted(set(component) & set(boundary))
            assert hit == [boundary[bp]]
            assert list(saved['component']) == component
            after = swap(ograph, order, c, pair, component)
            assert after == tuple(saved['colors'])
            for x in order:
                bit = int(x in component)
                word[x].append(bit)
                if bit:
                    permutation[x] = tuple(sum(pair) - k if k in pair else k for k in permutation[x])
            moves.append(dict(round=r, step=t, pair=list(pair), root=boundary[bp],
                              component=component, boundary_intersection=hit,
                              before=list(c), after=list(after), failed=False))
            c = after
            snapshots.append(dict(round=r, time=t, colors=list(c), failed=False))
        normalized = tuple(ALIGN[k] for k in c)
        assert normalized == tuple(row['normalized_colors'])
        for x in order:
            permutation[x] = tuple(ALIGN[k] for k in permutation[x])
        assert normalized == tuple(raw['normalized_iterates'][(r + 1) % len(raw['normalized_iterates'])])
    failed = raw.get('failed_next_round')
    failure = None
    if failed:
        r, c = len(raw['rounds']), tuple(failed['source_colors'])
        snapshots.append(dict(round=r, time=0, colors=list(c), failed=True))
        for t, (pair, bp, saved) in enumerate(zip(PAIRS, POSITIONS, failed['moves']), 1):
            active = {x for x in order if c[position[x]] in pair}
            component = next(p for p in parts(ograph, active) if boundary[bp] in p)
            hit = sorted(set(component) & set(boundary))
            assert component == saved['component']
            assert hit == saved['boundary_intersection']
            after = swap(ograph, order, c, pair, component)
            assert after == tuple(saved['colors'])
            moves.append(dict(round=r, step=t, pair=list(pair), root=boundary[bp],
                              component=component, boundary_intersection=hit,
                              before=list(c), after=list(after), failed=True))
            c = after
            snapshots.append(dict(round=r, time=t, colors=list(c), failed=True))
            if hit != [boundary[bp]]:
                assert t == len(failed['moves'])
                failure = dict(round=r, step=t, pair=list(pair), root=boundary[bp],
                               component=component, boundary_intersection=hit)
                break
            assert t < len(failed['moves'])
        assert failure is not None
    closed = len(raw['rounds']) == 4 and raw['rounds'][-1]['normalized_colors'] == raw['normalized_iterates'][0]
    initial = dict(zip(order, raw['normalized_iterates'][0]))
    final = dict(zip(order, raw['rounds'][-1]['normalized_colors']))
    for x in order:
        assert permutation[x][initial[x]] == final[x]
        if closed:
            assert permutation[x][initial[x]] == initial[x]
    return dict(graph=graph, faces=faces, owners=owners, order=order, ograph=ograph,
                snapshots=snapshots, moves=moves, words=word, permutations=permutation,
                closed=closed, failure=failure)


def reconstruct_differences(raw, data):
    order, graph, faces, owners = data['order'], data['graph'], data['faces'], data['owners']
    rows = []
    for comparison in raw['comparisons']:
        c, d = comparison['c'], comparison['d']
        difference = {x for x, a, b in zip(order, c, d) if a != b}
        comps = []
        for q in parts(data['ograph'], difference):
            attachments = sorted(set().union(*(graph[x] for x in q)) - set(q))
            assert not set(attachments) & difference
            cycles = upstream.simple_cycles(graph, attachments)
            separating = []
            for cycle in cycles:
                sides = upstream.cycle_sides(cycle, faces, owners)
                inner = next(side for side in sides if raw['center'] not in side)
                if set(q) <= set(inner):
                    separating.append(cycle)
            assert separating
            if len(attachments) == 6:
                # For these concrete sources the complete induced graph is a
                # single chordless six-cycle. This finite fact is not the paper proof.
                assert all(len(graph[x] & set(attachments)) == 2 for x in attachments)
                assert len(parts(graph, attachments)) == 1
                assert len(cycles) == 1 and len(cycles[0]) == 6
            comps.append(dict(Q=q, A=attachments, cycles=cycles))
        rows.append(dict(source=comparison['source_iterate'], target=comparison['target_iterate'],
                         D=sorted(difference), components=comps))
    return rows


def interface_partition(raw, data, cycle, colors):
    """Rebuild both side stars, including stars with empty interface contact."""
    graph, faces, owners = data['graph'], data['faces'], data['owners']
    cycle = set(cycle)
    sides = upstream.cycle_sides(sorted_cycle(cycle, graph), faces, owners)
    inner = set(next(side for side in sides if raw['center'] not in side))
    outer = set(next(side for side in sides if raw['center'] in side)) - {raw['center']}
    assert inner | outer | cycle == set(data['order'])
    c = dict(zip(data['order'], colors))
    answer = []
    for pair in combinations(range(4), 2):
        active = {x for x in data['order'] if c[x] in pair}
        full = parts(data['ograph'], active)
        local = parts(data['ograph'], active & cycle)
        stars = []
        for side_name, vertices in [('inner', inner), ('outer', outer)]:
            for component in parts(data['ograph'], active & vertices):
                edges = sorted([x, y] for x in component for y in graph[x] & cycle & active)
                stars.append(dict(side=side_name, component=component,
                                  attachments=sorted({y for _, y in edges}), cross_edges=edges))
        # Recompute full partitions using only disjoint side components and
        # interface edges, represented as a union-find over original vertices.
        aux = {x: set() for x in active}
        for component in local:
            for x in component[1:]:
                aux[x].add(component[0]); aux[component[0]].add(x)
        for star in stars:
            vertices = star['component'] + star['attachments']
            for x in vertices[1:]:
                aux[x].add(vertices[0]); aux[vertices[0]].add(x)
        recomposed = parts(aux, active)
        assert recomposed == full
        answer.append(dict(pair=list(pair), full_components=full,
                           interface_components=local,
                           inner_components=[s['component'] for s in stars if s['side'] == 'inner'],
                           outer_components=[s['component'] for s in stars if s['side'] == 'outer'],
                           stars=stars, recomposed_components=recomposed))
    return answer


def sorted_cycle(vertices, graph):
    """Unique orientation chosen independently by walking the induced cycle."""
    start = min(vertices)
    row = [start, min(graph[start] & vertices)]
    while len(row) < len(vertices):
        options = (graph[row[-1]] & vertices) - set(row)
        assert len(options) == 1
        row.append(next(iter(options)))
    assert start in graph[row[-1]]
    return row


def path_check(data, colors, pair, path):
    c = dict(zip(data['order'], colors))
    assert len(path) == len(set(path))
    assert all(c[x] in pair for x in path)
    assert all(y in data['ograph'][x] for x, y in zip(path, path[1:]))


def minimum_escape_length(raw, data, start):
    """Literal BFS, with neither S4 quotient nor inserted frame changes."""
    order, graph = data['order'], data['ograph']
    ix = {x: j for j, x in enumerate(order)}
    initial = tuple(start)
    queue, seen = deque([(initial, 0)]), {initial}
    while queue:
        c, distance = queue.popleft()
        if len({c[ix[x]] for x in raw['boundary']}) == 3:
            return distance
        for pair in combinations(range(4), 2):
            active = {x for x in order if c[ix[x]] in pair}
            for component in parts(graph, active):
                after = tuple(sum(pair) - k if x in component else k for x, k in zip(order, c))
                if after not in seen:
                    seen.add(after)
                    queue.append((after, distance + 1))
    return None


def palette_power(exponent):
    values = list(range(4))
    for _ in range(exponent % 4):
        values = [ALIGN[x] for x in values]
    return values


def check_timeline(raw, new, data):
    order, graph = data['order'], data['ograph']
    assert len(new['snapshots']) == len(data['snapshots'])
    assert len(new['moves']) == len(data['moves'])
    continuous = [list(raw['normalized_iterates'][0])]
    for i, (wanted, given) in enumerate(zip(data['moves'], new['moves'])):
        for key in ('round', 'step', 'pair', 'root', 'component', 'boundary_intersection'):
            assert given[key] == wanted[key], (i, key)
        assert given['move_id'] == i
        assert given['continuous_time'] == i
        back = palette_power(-wanted['round'])
        lifted_pair = sorted(back[x] for x in wanted['pair'])
        assert given['continuous_pair'] == lifted_pair
        assert [back[x] for x in wanted['before']] == continuous[-1]
        after = swap(graph, order, continuous[-1], lifted_pair, wanted['component'])
        assert list(after) == [back[x] for x in wanted['after']]
        continuous.append(list(after))
        assert given['prescribed_singleton'] == (wanted['boundary_intersection'] == [wanted['root']])
        before = new['snapshots'][given['source_snapshot_id']]
        after_state = new['snapshots'][given['target_snapshot_id']]
        assert before['colors'] == wanted['before'] and after_state['colors'] == wanted['after']
        paths = given['same_state_paths_to_boundary']
        assert [p['target'] for p in paths] == wanted['boundary_intersection']
        for row in paths:
            assert row['path'][0] == wanted['root'] and row['path'][-1] == row['target']
            path_check(data, wanted['before'], wanted['pair'], row['path'])
    assert new['continuous_literal_colors'] == continuous
    for i, (wanted, given) in enumerate(zip(data['snapshots'], new['snapshots'])):
        assert given['snapshot_id'] == i
        for key in ('round', 'time', 'colors'):
            assert given[key] == wanted[key]
        assert given['round_defined'] == (not wanted['failed'])
        tick = 5 * wanted['round'] + wanted['time']
        assert given['continuous_time'] == tick
        assert given['continuous_colors'] == continuous[tick]
    events = new['normalization_events']
    assert len(events) == len(raw['rounds'])
    for i, (given, old) in enumerate(zip(events, raw['rounds'])):
        assert given == dict(round=i, permutation=list(ALIGN),
                             raw_colors=old['moves'][-1]['colors'],
                             normalized_colors=old['normalized_colors'], continuous_time=5*(i+1))
    assert len(new['vertex_words']) == len(order)
    identity = 0
    for x, given in zip(order, new['vertex_words']):
        j, perm, prefixes = order.index(x), list(range(4)), []
        bits = []
        for k, move in enumerate(new['moves']):
            bit = int(x in move['component']); bits.append(str(bit))
            if bit:
                a, b = move['continuous_pair']
                perm = [a+b-z if z in (a, b) else z for z in perm]
            assert perm[continuous[0][j]] == continuous[k+1][j]
            if (k+1) % 5 == 0:
                prefixes.append(perm[:])
        assert given['vertex'] == x
        assert given['membership_word'] == ''.join(bits)
        assert given['continuous_colors'] == [c[j] for c in continuous]
        assert given['induced_permutation'] == perm
        assert given['prefix_permutations_after_each_complete_round'] == prefixes
        fixes = perm[continuous[0][j]] == continuous[0][j]
        is_identity = perm == list(range(4))
        assert given['fixes_initial_color'] == fixes
        assert given['permutation_is_identity'] == is_identity
        identity += int(is_identity)
    closure = new['closure']
    assert closure['completed_rounds'] == len(events)
    assert closure['actual_exchange_count'] == len(new['moves'])
    assert closure['prescribed_singleton_exchange_count'] == sum(m['prescribed_singleton'] for m in new['moves'])
    assert closure['alignment_power'] == palette_power(len(events))
    assert closure['continuous_literal_closed'] == (continuous[0] == continuous[-1])
    assert closure['all_vertex_words_fix_initial_color'] == all(w['fixes_initial_color'] for w in new['vertex_words'])
    assert closure['identity_permutation_vertex_count'] == identity
    return dict(successful_prescribed_exchanges=sum(
                    m['boundary_intersection'] == [m['root']] for m in data['moves']),
                completed_round_exchange_count=5*len(raw['rounds']),
                recorded_actual_exchanges=len(new['moves']), snapshots=len(new['snapshots']),
                continuous_literal_closed=closure['continuous_literal_closed'],
                identity_permutation_vertices=identity,
                closure_requires_only_initial_color_stabilization=True,
                failed_next_round=data['failure'])


def check_geometry(raw, old_separation, new, data):
    independent = reconstruct_differences(raw, data)
    assert len(independent) == len(new['differences'])
    for i, (expected, given, frozen) in enumerate(zip(independent, new['differences'], old_separation['comparisons'])):
        assert given['comparison_index'] == i
        assert given['source_iterate'] == expected['source']
        assert given['target_iterate'] == expected['target']
        assert given['D'] == expected['D']
        assert given['fixed_five_cycles'] == frozen['fixed_five_cycles']
        assert given['rigidity_violations'] == frozen['rigidity_violations']
        assert len(given['components']) == len(expected['components'])
        for j, (q, row, original) in enumerate(zip(expected['components'], given['components'], frozen['components'])):
            # Every inherited original neighbour, rotation, face, contour,
            # separator and both sides was independently checked upstream.
            for key, value in original.items():
                assert row[key] == value
            assert row['vertices'] == q['Q'] and row['attachments'] == q['A']
            region = new['regions'][row['region_id']]
            assert region['Q'] == q['Q'] and region['attachments'] == q['A']
            assert row['inner_vertices_not_in_Q'] == sorted(set(region['inner']) - set(q['Q']))
            sides = []
            for item in region['full_open_side_components']:
                vertices = set(item['vertices'])
                sides.append(dict(**item, changed_vertices=sorted(vertices & set(expected['D'])),
                                  fixed_vertices=sorted(vertices - set(expected['D'])),
                                  other_difference_components=[qq['Q'] for qq in expected['components']
                                      if qq['Q'] != q['Q'] and set(qq['Q']) & vertices]))
            assert row['side_components_at_this_comparison'] == sides
    for i, region in enumerate(new['regions']):
        assert region['region_id'] == i
        cycle = region['cycle']
        graph, faces = data['graph'], data['faces']
        sides = upstream.cycle_sides(cycle, faces, data['owners'])
        inner = next(side for side in sides if raw['center'] not in side)
        center_side = next(side for side in sides if raw['center'] in side)
        assert region['inner'] == inner and region['center_side'] == center_side
        assert region['outer'] == sorted(set(center_side) - {raw['center']})
        assert set(region['Q']) <= set(inner)
        assert region['Q_equals_entire_inner_open_side'] == (set(region['Q']) == set(inner))
        assert region['inner_open_side_connected'] == (len(parts(graph, inner)) == 1)
        assert region['Q_equals_entire_inner_open_side'] and region['inner_open_side_connected']
        edges = sorted([x, y] for x in cycle for y in graph[x] & set(cycle) if x < y)
        assert region['cycle_induced_edges'] == edges
        assert region['cycle_is_chordless'] == (len(edges) == len(cycle))
        assert region['cycle_is_chordless'] and len(cycle) == 6
        components = parts(graph, set(graph) - set(cycle))
        assert region['full_open_side_components'] == [dict(vertices=p,
            side='center' if set(p) <= set(center_side) else 'opposite') for p in components]
        assert region['original_face_ids_meeting_Q'] == [j for j, f in enumerate(faces) if set(f) & set(region['Q'])]
        assert region['original_face_ids_on_inner_side'] == [j for j, f in enumerate(faces) if set(f) <= set(cycle) | set(inner)]
        refs = [dict(comparison_index=ci, component_index=qi)
                for ci, comp in enumerate(new['differences']) for qi, q in enumerate(comp['components'])
                if q['region_id'] == i]
        assert region['source_comparison_refs'] == refs
    expected_intersections = []
    for i, first in enumerate(new['differences']):
        for j in range(i+1, len(new['differences'])):
            second = new['differences'][j]
            expected_intersections.append(dict(first_comparison=i, second_comparison=j,
                D_intersection=sorted(set(first['D']) & set(second['D'])), D_equal=first['D'] == second['D'],
                component_intersections=[dict(first_component=a, second_component=b,
                    intersection=sorted(set(q['vertices']) & set(r['vertices'])))
                    for a,q in enumerate(first['components']) for b,r in enumerate(second['components'])]))
    assert len(expected_intersections) == len(new['comparison_intersections'])
    for given, expected in zip(new['comparison_intersections'], expected_intersections):
        for key, value in expected.items():
            assert given[key] == value
    return independent


def check_gluing(raw, new, data):
    count, empty_contacts = 0, 0
    assert len(new['region_gluing']) == len(new['regions'])
    for region, gluing in zip(new['regions'], new['region_gluing']):
        assert gluing['region_id'] == region['region_id']
        assert len(gluing['snapshots']) == len(new['snapshots'])
        for snapshot, given in zip(new['snapshots'], gluing['snapshots']):
            assert given['snapshot_id'] == snapshot['snapshot_id']
            expected = interface_partition(raw, data, region['cycle'], snapshot['colors'])
            assert len(given['pairs']) == 6
            for row, computed in zip(given['pairs'], expected):
                for key in ('pair', 'full_components', 'interface_components', 'recomposed_components'):
                    assert row[key] == computed[key]
                c = dict(zip(data['order'], snapshot['colors']))
                active = {x for x in data['order'] if c[x] in row['pair']}
                for key, side in [('inner_components', 'inner'), ('outer_components', 'outer')]:
                    expected_components = computed[key]
                    assert len(row[key]) == len(expected_components)
                    for star, component in zip(row[key], expected_components):
                        assert star['component'] == component
                        original = sorted(set().union(*(data['ograph'][x] for x in component)) - set(component))
                        cross = sorted([x,y] for x in component for y in data['ograph'][x] & set(region['cycle']))
                        active_cross = [xy for xy in cross if xy[1] in active]
                        assert star['all_original_attachments'] == original
                        assert star['all_interface_cross_edges'] == cross
                        assert star['active_interface_cross_edges'] == active_cross
                        assert star['active_interface_attachments'] == sorted({y for _,y in active_cross})
                        empty_contacts += not star['active_interface_attachments']
                assert row['full_three_way_intersections'] == [dict(component=p,
                    inner=sorted(set(p) & set(region['inner'])),
                    interface=sorted(set(p) & set(region['cycle'])),
                    outer=sorted(set(p) & set(region['outer']))) for p in computed['full_components']]
                count += 1
    assert len(new['region_moves']) == len(new['regions'])
    for region, row in zip(new['regions'], new['region_moves']):
        assert row['region_id'] == region['region_id']
        expected = []
        for move in new['moves']:
            component = set(move['component'])
            expected.append(dict(move_id=move['move_id'], component_in_Q=sorted(component & set(region['Q'])),
                component_in_inner=sorted(component & set(region['inner'])),
                component_on_cycle=sorted(component & set(region['cycle'])),
                component_in_outer=sorted(component & set(region['outer'])),
                cycle_changed_vertices=sorted(component & set(region['cycle']))))
        assert row['moves'] == expected
        ix = {x:j for j,x in enumerate(data['order'])}
        cycle_colors = [[c[ix[x]] for x in region['cycle']] for c in raw['normalized_iterates']]
        assert row['normalized_cycle_colors'] == cycle_colors
        assert row['same_cycle_colors_at_all_normalized_iterates'] == (len(set(map(tuple, cycle_colors))) == 1)
        assert row['fixed_on_source_comparisons'] == [dict(**ref, fixed=True) for ref in region['source_comparison_refs']]
        for ref in region['source_comparison_refs']:
            comp = raw['comparisons'][ref['comparison_index']]
            assert all(comp['c'][ix[x]] == comp['d'][ix[x]] for x in region['cycle'])
    return dict(complete_six_pair_gluing_records=count, zero_contact_side_components_retained=empty_contacts)


def check_escapes(raw, new, data):
    assert len(new['escape_routes']) == len(raw['normalized_iterates'])
    lengths = []
    ix = {x:j for j,x in enumerate(data['order'])}
    for i, given in enumerate(new['escape_routes']):
        assert given['normalized_iterate'] == i
        c = tuple(raw['normalized_iterates'][i])
        assert given['source_colors'] == list(c)
        for move in given['literal_moves']:
            assert move['source_colors'] == list(c)
            assert move['boundary_intersection'] == sorted(set(move['component']) & set(raw['boundary']))
            c = swap(data['ograph'], data['order'], c, move['pair'], move['component'])
            assert move['target_colors'] == list(c)
        assert given['target_colors'] == list(c)
        word = [c[ix[x]] for x in raw['boundary']]
        assert given['target_boundary_word'] == word and len(set(word)) == 3
        assert given['length'] == len(given['literal_moves'])
        minimum = minimum_escape_length(raw, data, given['source_colors'])
        assert minimum == given['length']
        assert given['search_complete_through_shorter_distances']
        lengths.append(minimum)
    return lengths


def check_disk_fibres(raw, new, data):
    # References are decoded from the already independently validated whole-O
    # fibre table, rather than reconstructing the producer's quotient loop.
    states = raw['full_kempe_component']['normalized_states']
    full = []
    for fibre in raw['full_boundary_fibres']['rows']:
        for lift in fibre['complete_lifts']:
            perm = lift['global_permutation']
            c = tuple(perm[x] for x in states[lift['normalized_state']])
            full.append((lift, dict(zip(data['order'], c))))
    assert len(new['disk_fibres']) == len(new['regions'])
    fibre_count, row_count, empty_count, action_count = 0, 0, 0, 0
    for region, given in zip(new['regions'], new['disk_fibres']):
        assert given['region_id'] == region['region_id']
        order = region['cycle'] + sorted(region['inner'])
        assert given['disk_vertex_order'] == order
        edges = sorted([x,y] for x in order for y in data['ograph'][x] & set(order) if x < y)
        assert given['disk_original_edges'] == edges
        words = defaultdict(list)
        pos = {x:j for j,x in enumerate(data['order'])}
        for i,c in enumerate(raw['normalized_iterates']):
            words[tuple(c[pos[x]] for x in region['cycle'])].append(i)
        assert len(given['fibres']) == len(words)
        for (word, endpoints), saved in zip(sorted(words.items()), given['fibres']):
            assert saved['cycle_word'] == list(word)
            assert saved['normalized_iterate_refs'] == endpoints
            rows = []
            for values in product(range(4), repeat=len(region['inner'])):
                c = dict(zip(region['cycle'], word))
                c.update(zip(sorted(region['inner']), values))
                if all(c[x] != c[y] for x,y in edges):
                    rows.append(tuple(c[x] for x in order))
            rows.sort()
            assert saved['complete_disk_fibre_size'] == len(rows) == len(saved['complete_disk_rows'])
            extendible = 0
            local_graph = {i:set() for i in range(len(rows))}
            disk_graph = {x:data['ograph'][x] & set(order) for x in order}
            for row_id, (row, record) in enumerate(zip(rows, saved['complete_disk_rows'])):
                assert record['disk_row_id'] == row_id
                assert record['disk_colors'] == list(row)
                expected_refs = [ref for ref,c in full if tuple(c[x] for x in order) == row]
                norm_ref = lambda ref: (ref['normalized_state'], tuple(ref['global_permutation']))
                assert sorted(map(norm_ref, record['full_source_lifts_refs'])) == sorted(map(norm_ref, expected_refs))
                assert len(record['full_source_lifts_refs']) == len(expected_refs)
                extendible += bool(expected_refs)
                empty_count += not expected_refs
                colors = dict(zip(order, row))
                pair_rows, actions = [], []
                for pair in combinations(range(4), 2):
                    components = parts(disk_graph, {x for x in order if colors[x] in pair})
                    pair_rows.append(dict(pair=list(pair), components=components))
                    for component in components:
                        if set(component).isdisjoint(region['cycle']):
                            target = tuple(sum(pair)-k if x in component else k for x,k in zip(order,row))
                            target_id = rows.index(target)
                            actions.append(dict(pair=list(pair), component=component,
                                target_disk_row=target_id,
                                is_actual_full_O_component_by_interface_separation=True))
                            local_graph[row_id].add(target_id)
                            # A local action avoiding C must remain one full-O
                            # component in every complete lift of this disk row.
                            for _, full_colors in full:
                                if tuple(full_colors[x] for x in order) == row:
                                    complete_components = parts(data['ograph'], {
                                        x for x in data['order'] if full_colors[x] in pair})
                                    assert component in complete_components
                assert record['all_six_pairs_disk_components'] == pair_rows
                assert record['boundary_fixed_interior_Kempe_actions'] == actions
                action_count += len(actions)
            classes = parts(local_graph, local_graph)
            assert saved['boundary_fixed_interior_Kempe_classes'] == classes
            endpoint_rows = []
            for endpoint in endpoints:
                full_colors = dict(zip(data['order'], raw['normalized_iterates'][endpoint]))
                projected = tuple(full_colors[x] for x in order)
                row_id = rows.index(projected)
                class_id = next(j for j,part in enumerate(classes) if row_id in part)
                endpoint_rows.append(dict(normalized_iterate=endpoint,
                    disk_row_id=row_id, interior_Kempe_class_id=class_id))
            assert saved['normalized_endpoint_disk_rows'] == endpoint_rows
            assert saved['globally_extendible_disk_row_count'] == extendible
            fibre_count += 1; row_count += len(rows)
    return dict(endpoint_cycle_word_fibres=fibre_count, complete_disk_rows=row_count,
                rows_with_empty_full_source_fibre=empty_count,
                boundary_fixed_interior_Kempe_actions=action_count,
                disk_enumeration_precedes_global_extendibility=True)


def check_first_failure_escape(raw, new, data):
    given = new['first_failure_escape']
    failures = [m for m in new['moves'] if not m['prescribed_singleton']]
    if not failures:
        assert given is None
        return None
    assert len(failures) == 1 and given is not None
    failed = failures[0]
    assert given['failed_move_id'] == failed['move_id']
    assert given['source_snapshot_id'] == failed['source_snapshot_id']
    current = new['snapshots'][given['source_snapshot_id']]['colors']
    pair = sorted(set(range(4)) - set(failed['pair']))
    assert given['alternate_pair'] == pair
    color = dict(zip(data['order'], current))
    components = parts(data['ograph'], {x for x in data['order'] if color[x] in pair})
    assert given['all_actual_complementary_components'] == components
    root, other = given['alternate_root'], given['other_complementary_boundary_root']
    assert root in raw['boundary'] and other in raw['boundary'] and root != other
    assert given['alternate_component'] == next(part for part in components if root in part)
    assert given['other_complementary_component'] == next(part for part in components if other in part)
    assert given['alternate_component'] != given['other_complementary_component']
    assert given['two_complementary_roots_disconnected_in_this_full_coloring']
    assert given['source_normalized_iterate'] == failed['round']
    c = tuple(raw['normalized_iterates'][failed['round']])
    assert given['source_colors'] == list(c)
    prefix = [m for m in new['moves'] if m['round'] == failed['round'] and m['step'] < failed['step']]
    assert len(given['literal_moves']) == len(prefix) + 1
    for i, move in enumerate(given['literal_moves']):
        assert move['source_colors'] == list(c)
        if i < len(prefix):
            assert move['pair'] == prefix[i]['pair'] and move['component'] == prefix[i]['component']
        else:
            assert list(c) == current
            assert move['pair'] == pair and move['component'] == given['alternate_component']
        c = swap(data['ograph'], data['order'], c, move['pair'], move['component'])
        assert move['target_colors'] == list(c)
    assert given['target_colors'] == list(c)
    ix = {x:j for j,x in enumerate(data['order'])}
    word = [c[ix[x]] for x in raw['boundary']]
    assert given['target_boundary_word'] == word and len(set(word)) == 3
    return dict(first_failure_step=failed['step'], alternate_pair=pair,
                source_roots=[root, other], disjoint_current_components=components,
                literal_escape_length=len(given['literal_moves']), target_boundary_word=word)


def check_synchronous_differences(raw, new, data):
    # Exhaustive scalar identity verification is algebra only. These 216
    # allowed local assignments are not asserted to be planar realizations.
    scalar_cases = 0
    for pair in combinations(range(4), 2):
        for a, b, k, ell in product(range(4), range(4), range(2), range(2)):
            if (k and a not in pair) or (ell and b not in pair):
                continue
            aa = sum(pair)-a if k else a
            bb = sum(pair)-b if ell else b
            toggled = bool((k != ell) and a in pair and b in pair)
            assert (aa != bb) == ((a != b) ^ toggled)
            scalar_cases += 1
    moves = {(m['round'],m['step']):m for m in data['moves']}
    snapshots = {(s['round'],s['time']):s for s in data['snapshots']}
    ids = {(s['round'],s['time']):s['snapshot_id'] for s in new['snapshots']}
    move_ids = {(m['round'],m['step']):m['move_id'] for m in new['moves']}
    starts = list(range(4)) if raw['premise_flags']['least_h_period4'] else [0]
    assert len(new['synchronous_difference_traces']) == len(starts)
    summaries, count = [], 0
    order = data['order']
    for r, trace in zip(starts, new['synchronous_difference_traces']):
        s = (r+2)%4 if raw['premise_flags']['least_h_period4'] else r+2
        assert trace['first_round'] == r and trace['second_round'] == s
        possible_steps = [t for t in range(1,6) if (r,t) in moves and (s,t) in moves]
        assert [row['step'] for row in trace['steps']] == possible_steps
        legal = True
        for t, row in zip(possible_steps, trace['steps']):
            first, second = moves[r,t], moves[s,t]
            assert first['pair'] == second['pair'] == row['pair']
            pair = row['pair']
            a = dict(zip(order, snapshots[r,t-1]['colors']))
            b = dict(zip(order, snapshots[s,t-1]['colors']))
            aa = dict(zip(order, snapshots[r,t]['colors']))
            bb = dict(zip(order, snapshots[s,t]['colors']))
            K, L = set(first['component']), set(second['component'])
            J = {x for x in order if a[x] in pair and b[x] in pair}
            toggle = (K ^ L) & J
            before, after = {x for x in order if a[x] != b[x]}, {x for x in order if aa[x] != bb[x]}
            assert after == before ^ toggle
            assert row['K'] == sorted(K) and row['L'] == sorted(L)
            assert row['both_colors_in_pair_J'] == sorted(J)
            assert row['K_symmetric_difference_L'] == sorted(K ^ L)
            assert row['equality_toggle_vertices'] == sorted(toggle)
            assert row['D_before'] == sorted(before) and row['D_after'] == sorted(after)
            assert row['born'] == sorted(after-before) and row['died'] == sorted(before-after)
            assert row['difference_components_before'] == parts(data['ograph'],before)
            assert row['difference_components_after'] == parts(data['ograph'],after)
            assert row['first_source_snapshot_id'] == ids[r,t-1]
            assert row['second_source_snapshot_id'] == ids[s,t-1]
            assert row['first_target_snapshot_id'] == ids[r,t]
            assert row['second_target_snapshot_id'] == ids[s,t]
            assert row['first_move_id'] == move_ids[r,t] and row['second_move_id'] == move_ids[s,t]
            singleton = first['boundary_intersection'] == [first['root']] and second['boundary_intersection'] == [second['root']]
            assert row['both_exchanges_prescribed_singleton'] == singleton
            legal &= singleton
            count += 1
        complete = len(possible_steps) == 5
        assert trace['compared_steps'] == len(possible_steps)
        assert trace['initial_difference'] == trace['steps'][0]['D_before']
        assert trace['terminal_difference'] == trace['steps'][-1]['D_after']
        assert trace['complete_five_step_pair'] == complete
        assert trace['prescribed_continuation_legal'] == legal
        assert trace['common_alignment_applied'] == complete
        assert trace['produces_next_parity_difference'] == complete
        if complete:
            target_pair = [(r+1)%4,(s+1)%4]
            assert trace['target_normalized_iterate_pair'] == target_pair
            first_colors = [ALIGN[x] for x in snapshots[r,5]['colors']]
            second_colors = [ALIGN[x] for x in snapshots[s,5]['colors']]
            assert first_colors == raw['normalized_iterates'][target_pair[0]]
            assert second_colors == raw['normalized_iterates'][target_pair[1]]
            difference = sorted(x for x,a,b in zip(order,first_colors,second_colors) if a != b)
            assert trace['normalized_terminal_difference'] == trace['terminal_difference'] == difference
        else:
            assert trace['normalized_terminal_difference'] is None
            assert trace['target_normalized_iterate_pair'] is None
            assert not legal  # n17 only, never a next normalized parity difference.
        summaries.append(dict(first_round=r, second_round=s,
            compared_steps=len(possible_steps), initial=trace['initial_difference'],
            terminal=trace['terminal_difference'], produces_next_parity_difference=complete,
            prescribed_continuation_legal=legal))
    return dict(scalar_algebra_assignments_checked=scalar_cases,
                full_source_synchronous_update_rows=count, traces=summaries,
                identity='D_after = D_before symmetric_difference ((K symmetric_difference L) intersection J)')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=AUDIT / 'cross-round-certificate.json')
    parser.add_argument('--output', type=Path, default=AUDIT / 'review-certificate.json')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    source = json.loads(SOURCE.read_text())
    separation = json.loads(SEPARATION.read_text())
    certificate = json.loads(args.input.read_text())
    assert certificate['schema'] == 'c5-six-cross-round-v1'
    for relative, expected in source['provenance_inputs'].items():
        assert digest(ROOT / relative) == expected
    for relative, expected in certificate['provenance_inputs'].items():
        assert digest(ROOT / relative) == expected
    assert certificate['producer_sha256'] == digest(ROOT / 'scripts/c5_six_cross_round.py')
    upstream_controls = [upstream.inspect(c) for c in source['controls']]
    upstream_result = upstream.review_separation(source, separation, upstream_controls)
    reviewed = []
    assert len(certificate['controls']) == len(source['controls'])
    for i, (raw, old, new) in enumerate(zip(source['controls'], separation['controls'], certificate['controls'])):
        assert raw['name'] == new['name']
        assert new['source_control_index'] == i
        assert new['source_ref']['file'] == str(SOURCE.relative_to(ROOT))
        assert new['source_ref']['json_pointer'] == f'/controls/{i}'
        assert set(new['source_ref']['preserves']) == {
            'original_edges', 'sphere_faces', 'rotation', 'exterior_vertices', 'exterior_edges',
            'complete_ABACD_fibre', 'full_boundary_fibres', 'full_kempe_component'}
        assert new['premise_flags'] == raw['premise_flags']
        data = replay_source(raw)
        timeline = check_timeline(raw, new, data)
        differences = check_geometry(raw, old, new, data)
        gluing = check_gluing(raw, new, data)
        escapes = check_escapes(raw, new, data)
        disk = check_disk_fibres(raw, new, data)
        failure_escape = check_first_failure_escape(raw, new, data)
        synchronous = check_synchronous_differences(raw, new, data)
        reviewed.append(dict(name=raw['name'], timeline=timeline,
            differences=[dict(source=d['source'], target=d['target'], D=d['D'],
                all_components=[dict(Q=q['Q'], A=q['A']) for q in d['components']]) for d in differences],
            chordless_six_cycle_regions=len(new['regions']), gluing=gluing,
            shortest_literal_escape_lengths=escapes, disk_fibres=disk,
            first_failure_escape=failure_escape, synchronous_differences=synchronous))
    result = dict(schema='independent-six-cross-round-review-v1',
        imports_producers=False,
        upstream_independent_reviewer='scripts/c5_d2_separation_review.py',
        upstream_trust_boundary='The earlier independent reviewer is rerun for original geometry, complete fibres/actions, contours and full original cycle sides. No producer is imported.',
        checked_inputs_sha256={str(p.relative_to(ROOT)): digest(p) for p in (
            SOURCE, SEPARATION, args.input, ROOT / 'scripts/c5_d2_separation_review.py',
            ROOT / 'scripts/c5_six_cross_round.py')},
        checker_sha256=digest(Path(__file__)),
        upstream_review=upstream_result, controls=reviewed,
        scope='Exact finite concrete-source replay only. Neither control is fully blocked; Errera fails S5. No general six-attachment exclusion or escape theorem is established.')
    encoded = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert args.output.read_text() == encoded, 'Independent replay differs'
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(json.dumps(dict(status='INDEPENDENT SIX CROSS ROUND CHECK OK', controls=reviewed), sort_keys=True))


if __name__ == '__main__':
    main()

