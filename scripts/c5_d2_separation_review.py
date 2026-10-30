#!/usr/bin/env python3
"""Independent stdlib checks for full-source D2 separation controls.

No imports from the control or boundary producers. Surface links, short-cycle
sides, every ABACD fibre, all actual Kempe actions, and complete colourings are
reconstructed from the original edges and faces.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'audits/2026-10-30-c5-d2-separation'
PAIRS = ((0, 3), (1, 3), (1, 2), (0, 2), (0, 3))
POSITIONS = (2, 4, 1, 3, 0)
ALIGN = (2, 3, 1, 0)
FRAME = (0, 1, 0, 2, 3)


def components(graph, vertices):
    remaining, answer = set(vertices), []
    while remaining:
        reached, stack = {min(remaining)}, [min(remaining)]
        remaining -= reached
        while stack:
            x = stack.pop()
            new = graph[x] & remaining
            remaining -= new
            reached |= new
            stack.extend(new)
        answer.append(tuple(sorted(reached)))
    return sorted(answer)


def norm(colors):
    table, out = {}, []
    for color in colors:
        if color not in table:
            table[color] = len(table)
        out.append(table[color])
    return tuple(out)


def cyclic(row):
    row = tuple(row)
    return min(row[j:] + row[:j] for j in range(len(row)))


def unoriented(row):
    return min(cyclic(row), cyclic(tuple(reversed(row))))


def geometry(control):
    n, faces = control['n'], control['sphere_faces']
    graph = {x: set() for x in range(n)}
    edges = [tuple(sorted(e)) for e in control['original_edges']]
    assert len(set(edges)) == len(edges) == 3 * n - 6
    for x, y in edges:
        assert 0 <= x < y < n
        graph[x].add(y)
        graph[y].add(x)
    assert len(components(graph, graph)) == 1
    assert len(faces) == 2 * n - 4
    assert len({tuple(sorted(f)) for f in faces}) == len(faces)
    owners, darts, links = defaultdict(list), {}, defaultdict(dict)
    for j, face in enumerate(faces):
        assert len(set(face)) == len(face) == 3
        for k in range(3):
            a, b, c = face[k:] + face[:k]
            assert b in graph[a]
            assert (a, b) not in darts
            darts[a, b] = j
            owners[tuple(sorted((a, b)))].append(j)
            assert c not in links[a]
            links[a][c] = b
    assert len(darts) == 2 * len(edges)
    assert all((b, a) in darts for a, b in darts)
    assert set(owners) == set(edges)
    assert all(len(js) == 2 for js in owners.values())
    rotation = []
    for x in range(n):
        assert set(links[x]) == set(links[x].values()) == graph[x]
        first = min(graph[x])
        row, y = [], first
        while y not in row:
            row.append(y)
            y = links[x][y]
        assert y == first and set(row) == graph[x]
        rotation.append(row)
    supplied = control.get('rotation')
    if supplied is not None:
        supplied = [supplied[str(x)] for x in range(n)] if isinstance(supplied, dict) else supplied
        assert (all(cyclic(supplied[x]) == cyclic(rotation[x]) for x in range(n)) or
                all(cyclic(supplied[x]) == cyclic(rotation[x][::-1]) for x in range(n)))
    v, boundary = control['center'], control['boundary']
    assert len(boundary) == len(set(boundary)) == 5
    assert set(boundary) == graph[v]
    assert unoriented(boundary) == unoriented(rotation[v])
    assert all(boundary[(i + 1) % 5] in graph[boundary[i]] for i in range(5))
    third = []
    for i in range(5):
        a, b = boundary[i], boundary[(i + 1) % 5]
        others = [next(x for x in faces[j] if x not in (a, b)) for j in owners[tuple(sorted((a, b)))]]
        assert v in others
        third.append(next(x for x in others if x != v))
    # Independently enumerate all short cycles and cut the original dual.
    short = []
    dual = {j: set() for j in range(len(faces))}
    for a, b in owners.values():
        dual[a].add(b)
        dual[b].add(a)
    for start in range(n):
        stack = [(start,)]
        while stack:
            path = stack.pop()
            if len(path) >= 3 and start in graph[path[-1]] and path[1] < path[-1]:
                blocked = {tuple(sorted((path[k], path[(k + 1) % len(path)]))) for k in range(len(path))}
                cutdual = {j: set(js) for j, js in dual.items()}
                for e in blocked:
                    a, b = owners[e]
                    cutdual[a].remove(b)
                    cutdual[b].remove(a)
                regions = components(cutdual, cutdual)
                assert len(regions) == 2
                sides = [sorted({x for j in part for x in faces[j]} - set(path)) for part in regions]
                assert set(sides[0]).isdisjoint(sides[1])
                assert set(sides[0]) | set(sides[1]) == set(graph) - set(path)
                sides.sort(key=lambda side: (len(side), side))
                short.append(dict(cycle=list(path), sides=sides))
            if len(path) < 5:
                stack.extend(path + (x,) for x in graph[path[-1]] if x > start and x not in path)
    s34 = all(not item['sides'][0] for item in short if len(item['cycle']) < 5)
    s5 = all(len(item['sides'][0]) <= 1 for item in short if len(item['cycle']) == 5)
    return graph, faces, rotation, owners, third, short, s34, s5


def enumerate_fibre(exterior, graph, boundary):
    """Fixed original-vertex order, no dependency on producer search ordering."""
    colors = dict(zip(boundary, FRAME))
    free = [v for v in exterior if v not in colors]
    answer = []
    def visit(j):
        if j == len(free):
            answer.append(tuple(colors[v] for v in exterior))
            return
        x = free[j]
        forbidden = {colors[y] for y in graph[x] if y in colors}
        for value in range(4):
            if value not in forbidden:
                colors[x] = value
                visit(j + 1)
        colors.pop(x, None)
    assert all(colors[a] != colors[b] for a in colors for b in graph[a] if b in colors)
    visit(0)
    return sorted(answer)



def all_boundary_fibres_check(control, graph, exterior, position):
    """Enumerate every full-O coloring directly, then check every literal fibre.

    The producer's complete S4-lift references are decoded only after the
    independent original-edge enumeration has completed.
    """
    colors, all_colorings = {}, []
    order = sorted(exterior, key=lambda x: (-len(graph[x]), x))
    def visit(j):
        if j == len(order):
            all_colorings.append(tuple(colors[x] for x in exterior))
            return
        x = order[j]
        forbidden = {colors[y] for y in graph[x] if y in colors}
        for value in range(4):
            if value not in forbidden:
                colors[x] = value
                visit(j + 1)
        colors.pop(x, None)
    visit(0)
    assert len(all_colorings) == len(set(all_colorings))
    all_colorings = set(all_colorings)
    boundary = control['boundary']
    words = list(product(range(4), repeat=5))
    proper_words = {word for word in words if all(word[i] != word[(i + 1) % 5] for i in range(5))}
    assert len(proper_words) == 240
    direct = {word: set() for word in proper_words}
    for c in all_colorings:
        word = tuple(c[position[x]] for x in boundary)
        assert word in direct
        direct[word].add(c)
    # All other literal boundary words have an original monochromatic B edge.
    assert all(any(word[i] == word[(i + 1) % 5] for i in range(5))
               for word in set(words) - proper_words)
    stored = control['full_boundary_fibres']
    assert stored['proper_boundary_words'] == len(proper_words)
    assert stored['full_original_edge_enumeration_count'] == len(all_colorings)
    rows = stored['rows']
    assert len(rows) == len(proper_words)
    assert {tuple(row['boundary_word']) for row in rows} == proper_words
    states = control['full_kempe_component']['normalized_states']
    seen_lifts, decoded_colorings = set(), set()
    for row in rows:
        decoded = set()
        for lift in row['complete_lifts']:
            state_id = lift['normalized_state']
            perm = tuple(lift['global_permutation'])
            assert 0 <= state_id < len(states) and set(perm) == set(range(4)) and len(perm) == 4
            assert (state_id, perm) not in seen_lifts
            seen_lifts.add((state_id, perm))
            c = tuple(perm[value] for value in states[state_id])
            assert c not in decoded_colorings
            decoded_colorings.add(c)
            decoded.add(c)
        assert decoded == direct[tuple(row['boundary_word'])]
    assert decoded_colorings == all_colorings
    assert seen_lifts == set(product(range(len(states)), permutations(range(4))))
    assert stored['all_proper_colorings_in_single_kempe_component']
    digest = sha256(json.dumps(sorted(all_colorings), separators=(',', ':')).encode()).hexdigest()
    assert stored['full_original_edge_enumeration_sha256'] == digest == stored['class_lifts_sha256']
    assert stored['original_edge_enumeration_equals_class_lifts']
    assert stored['empty_proper_boundary_fibres'] == sum(not direct[word] for word in proper_words)
    assert stored['nonproper_boundary_words'] == 784
    assert stored['nonproper_boundary_fibres_empty_by_original_B_edges']
    return dict(literal_boundary_words=1024, proper_boundary_words=240,
                improper_empty_fibres=1024 - 240,
                proper_empty_fibres=sum(not direct[word] for word in proper_words),
                complete_original_edge_colorings=len(all_colorings),
                all_S4_lift_references_verified=True)


def class_check(control, graph, exterior, position):
    stored = control['full_kempe_component']
    states = [tuple(c) for c in stored['normalized_states']]
    assert states and len(states) == len(set(states))
    assert all(norm(c) == c for c in states)
    table = {c: i for i, c in enumerate(states)}
    assert norm(control['normalized_iterates'][0]) in table
    computed_actions, extending = [], []
    bpos = [position[v] for v in control['boundary']]
    for source, c in enumerate(states):
        assert all(c[position[x]] != c[position[y]] for x in exterior for y in graph[x])
        if len({c[p] for p in bpos}) == 3:
            extending.append(source)
        expected = set()
        for a, b in combinations(range(4), 2):
            active = {x for x in exterior if c[position[x]] in (a, b)}
            for part in components(graph, active):
                changed = norm(tuple(a + b - color if x in part else color for x, color in zip(exterior, c)))
                assert changed in table, 'Kempe class omitted a reachable complete coloring'
                expected.add(((a, b), part, table[changed]))
        supplied = stored['all_actual_component_actions'][source]
        actual = {(tuple(a['pair']), tuple(a['component']), a['target']) for a in supplied}
        assert actual == expected and len(actual) == len(supplied)
        computed_actions.append(expected)
    start = table[norm(control['normalized_iterates'][0])]
    reached, stack = {start}, [start]
    while stack:
        for _, _, target in computed_actions[stack.pop()]:
            if target not in reached:
                reached.add(target)
                stack.append(target)
    assert len(reached) == len(states)
    assert stored['normalized_size'] == len(states)
    assert stored['literal_size'] == 24 * len(states)
    assert stored['extending_state_ids'] == extending
    assert stored['blocked'] == (not extending)
    return len(states), len(extending)


def collar_cycles(q, graph, faces):
    """Cycles of mixed-face arcs on Q/outside edge midpoints, then projection.

    This derives the boundary through a degree-two graph rather than following
    the producer's rotation successor. Stationary projections in two-Q faces
    are kept until the final consecutive-repeat compression.
    """
    arcs, incidence = [], defaultdict(list)
    for j, face in enumerate(faces):
        crossing = [tuple(sorted((face[k], face[(k + 1) % 3]))) for k in range(3)
                    if (face[k] in q) != (face[(k + 1) % 3] in q)]
        if crossing:
            assert len(crossing) == 2
            arcs.append((j, *crossing))
            incidence[crossing[0]].append(len(arcs) - 1)
            incidence[crossing[1]].append(len(arcs) - 1)
    assert all(len(ids) == 2 for ids in incidence.values())
    unused, result = set(range(len(arcs))), []
    while unused:
        chosen = min(unused)
        first = arcs[chosen][1]
        node, arc = first, chosen
        walk, boundary_faces, crossed_edges = [], [], []
        while True:
            assert arc in unused
            unused.remove(arc)
            face_id, a, b = arcs[arc]
            boundary_faces.append(face_id)
            crossed_edges.append(node)
            walk.append(next(x for x in node if x not in q))
            node = b if node == a else a
            candidates = [i for i in incidence[node] if i != arc]
            assert len(candidates) == 1
            arc = candidates[0]
            if node == first:
                assert arc == chosen
                break
        compressed = [x for i, x in enumerate(walk) if x != walk[i - 1]] or walk[:1]
        assert compressed
        if len(compressed) == 1:
            assert all(x == compressed[0] for x in walk)
        else:
            assert all(compressed[(i + 1) % len(compressed)] in graph[x]
                       for i, x in enumerate(compressed))
        result.append(dict(projected_walk=list(unoriented(compressed)),
                           mixed_face_ids=sorted(boundary_faces),
                           crossing_edges=sorted(map(list, crossed_edges)),
                           simple=len(compressed) >= 3 and len(compressed) == len(set(compressed))))
    return sorted(result, key=lambda row: (row['projected_walk'], row['mixed_face_ids']))


def inspect(control):
    graph, faces, rotation, owners, third, short, s34, s5 = geometry(control)
    exterior = control['exterior_vertices']
    assert len(set(exterior)) == len(exterior) == control['n'] - 1
    assert set(exterior) == set(graph) - {control['center']}
    position = {v: i for i, v in enumerate(exterior)}
    ograph = {x: graph[x] & set(exterior) for x in exterior}
    assert {tuple(sorted((x, y))) for x in exterior for y in ograph[x]} == {tuple(sorted(e)) for e in control['exterior_edges']}
    fibre = enumerate_fibre(exterior, ograph, control['boundary'])
    supplied_fibre = [tuple(c) for c in control['complete_ABACD_fibre']]
    assert sorted(supplied_fibre) == fibre and len(supplied_fibre) == len(set(supplied_fibre))
    iterates = [tuple(c) for c in control['normalized_iterates']]
    assert all(c in set(fibre) for c in iterates)
    snapshots = []
    for r, stored in enumerate(control['rounds']):
        c = tuple(stored['source_colors'])
        assert c == iterates[r]
        snapshots.append(c)
        assert len(stored['moves']) == 5
        for pair, root_position, move in zip(PAIRS, POSITIONS, stored['moves']):
            root = control['boundary'][root_position]
            assert tuple(move['pair']) == pair and move['root'] == root
            assert c[position[root]] in pair
            active = {x for x in exterior if c[position[x]] in pair}
            comp = next(part for part in components(ograph, active) if root in part)
            assert set(comp) & set(control['boundary']) == {root}
            assert list(comp) == sorted(move['component'])
            if 'boundary_intersection' in move:
                assert move['boundary_intersection'] == [root]
            c = tuple(sum(pair) - color if x in comp else color for x, color in zip(exterior, c))
            assert c == tuple(move['colors'])
            assert all(c[position[x]] != c[position[y]] for x in exterior for y in ograph[x])
            snapshots.append(c)
        target = tuple(ALIGN[x] for x in c)
        assert target == tuple(stored['normalized_colors'])
        assert target == iterates[(r + 1) % len(iterates)]
    failed = control.get('failed_next_round')
    if failed is not None:
        assert not failed['defined']
        c = tuple(failed['source_colors'])
        assert c == iterates[-1]
        first_bad = None
        for j, (pair, root_position, move) in enumerate(zip(PAIRS, POSITIONS, failed['moves'])):
            root = control['boundary'][root_position]
            assert tuple(move['pair']) == pair and move['root'] == root
            active = {x for x in exterior if c[position[x]] in pair}
            comp = next(part for part in components(ograph, active) if root in part)
            assert list(comp) == sorted(move['component'])
            hit = sorted(set(comp) & set(control['boundary']))
            assert move['boundary_intersection'] == hit
            c = tuple(sum(pair) - color if x in comp else color for x, color in zip(exterior, c))
            assert c == tuple(move['colors'])
            if hit != [root]:
                first_bad = j
                break
        assert first_bad == len(failed['moves']) - 1
    class_size, extending = class_check(control, ograph, exterior, position)
    full_fibres = all_boundary_fibres_check(control, ograph, exterior, position)
    flags = control['premise_flags']
    assert flags['S34'] == s34 and flags['S5'] == s5
    assert flags['minimum_degree5'] == (min(map(len, graph.values())) >= 5)
    assert flags['fully_blocked'] == (not extending)
    if flags['least_h_period4']:
        assert len(iterates) == len(set(iterates)) == len(control['rounds']) == 4
    comparisons = []
    for compare in control['comparisons']:
        c, d = tuple(compare['c']), tuple(compare['d'])
        assert c == iterates[compare['source_iterate']]
        assert d == iterates[compare['target_iterate']]
        difference = {x for x in exterior if c[position[x]] != d[position[x]]}
        assert difference
        assert not difference & (set(control['boundary']) | set(third))
        rows = []
        for part in components(ograph, difference):
            q = set(part)
            attachments = set().union(*(graph[x] for x in q)) - q
            assert control['center'] not in attachments
            assert all(c[position[x]] == d[position[x]] for x in attachments)
            rows.append(dict(vertices=list(part), attachments=sorted(attachments),
                             collar_boundaries=collar_cycles(q, graph, faces)))
            if s34 and s5:
                assert len(attachments) >= 6
        fixed_five = []
        for item in short:
            cycle = item['cycle']
            if len(cycle) != 5 or control['center'] in cycle or difference & set(cycle):
                continue
            center_side = next(side for side in item['sides'] if control['center'] in side)
            remote = next(side for side in item['sides'] if control['center'] not in side)
            hit = sorted(difference & set(remote))
            fixed_five.append(dict(cycle=cycle, center_side=center_side, other_side=remote,
                                   differences_in_other_side=hit,
                                   rigidity_applicable=len(center_side) >= 2))
            if s5 and len(center_side) >= 2:
                assert not hit
        comparisons.append(dict(source_iterate=compare['source_iterate'], target_iterate=compare['target_iterate'],
                                difference=sorted(difference), components=rows,
                                all_fixed_original_five_cycles=fixed_five))
    return dict(name=control['name'], S34=s34, S5=s5, complete_fibre_size=len(fibre),
                full_literal_boundary_fibres=full_fibres,
                kempe_quotient_size=class_size, extending_quotient_states=extending,
                actual_exchange_count=5 * len(control['rounds']), comparisons=comparisons)



def simple_cycles(graph, allowed):
    allowed, answer = set(allowed), []
    for start in sorted(allowed):
        stack = [(start,)]
        while stack:
            path = stack.pop()
            if len(path) >= 3 and start in graph[path[-1]] and path[1] < path[-1]:
                answer.append(path)
            stack.extend(path + (x,) for x in graph[path[-1]] & allowed
                         if x > start and x not in path)
    return answer


def cycle_sides(cycle, faces, owners):
    blocked = {tuple(sorted((cycle[i], cycle[(i + 1) % len(cycle)]))) for i in range(len(cycle))}
    dual = {j: set() for j in range(len(faces))}
    for edge, (a, b) in owners.items():
        if edge not in blocked:
            dual[a].add(b)
            dual[b].add(a)
    regions = components(dual, dual)
    assert len(regions) == 2
    sides = [sorted({x for j in part for x in faces[j]} - set(cycle)) for part in regions]
    return sorted(sides, key=lambda side: (len(side), side))


def open_walk(walk):
    walk = list(walk)
    if len(walk) > 1 and walk[0] == walk[-1]:
        walk.pop()
    return walk



def check_gluing(raw, records, graph):
    exterior = set(raw['exterior_vertices'])
    position = {x: j for j, x in enumerate(raw['exterior_vertices'])}
    graph = {x: graph[x] & exterior for x in exterior}
    snapshots = [(r, t, colors) for r, row in enumerate(raw['rounds'])
                 for t, colors in enumerate([row['source_colors']] + [move['colors'] for move in row['moves']])]
    pair_count = 0
    for record in records:
        kept, remote = set(record['kept_vertices']), set(record['remote_vertices'])
        assert not kept & remote and kept | remote == exterior
        assert record['interface'] == sorted(x for x in kept if graph[x] & remote)
        assert len(record['snapshots']) == len(snapshots)
        for supplied, (r, t, colors) in zip(record['snapshots'], snapshots):
            assert supplied['round'] == r and supplied['time'] == t and supplied['colors'] == colors
            assert len(supplied['all_six_pairs']) == 6
            for pair, row in zip(combinations(range(4), 2), supplied['all_six_pairs']):
                assert row['pair'] == list(pair)
                active = {x for x in exterior if colors[position[x]] in pair}
                full = components(graph, active)
                local = components(graph, active & kept)
                far = components(graph, active & remote)
                assert row['full_components'] == list(map(list, full))
                assert row['local_components'] == list(map(list, local))
                expected_stars = [dict(component=list(part), attachments=sorted(set().union(*(graph[x] for x in part)) & kept & active)) for part in far]
                assert row['remote_stars'] == expected_stars
                # Union local component IDs through every remote attachment set.
                # This does not use the producer's auxiliary-star graph traversal.
                owner = {x: j for j, part in enumerate(local) for x in part}
                parent = list(range(len(local)))
                def find(a):
                    while parent[a] != a:
                        parent[a] = parent[parent[a]]
                        a = parent[a]
                    return a
                for star in expected_stars:
                    ids = [owner[x] for x in star['attachments']]
                    for target in ids[1:]:
                        parent[find(target)] = find(ids[0])
                groups = defaultdict(set)
                for j, part in enumerate(local):
                    groups[find(j)].update(part)
                recomposed = sorted(sorted(part) for part in groups.values())
                projection = sorted(sorted(set(part) & kept) for part in full if set(part) & kept)
                assert recomposed == projection == row['full_projection'] == row['recomposed_projection']
                pair_count += 1
    return pair_count


def review_separation(source, certificate, independently_checked):
    assert len(certificate['controls']) == len(source['controls'])
    reviewed, contour_count, pair_count = [], 0, 0
    for raw, produced, checked in zip(source['controls'], certificate['controls'], independently_checked):
        assert raw['name'] == produced['name'] == checked['name']
        graph, faces, rotation, owners, third, short, s34, s5 = geometry(raw)
        assert produced['collar']['third_vertices'] == third
        collar = produced['collar']
        assert len(collar['fans']) == 5
        reconstructed_walk = []
        for i, fan in enumerate(collar['fans']):
            x = raw['boundary'][i]
            assert fan['boundary_vertex'] == x
            link = {y: set() for y in graph[x] - set(raw['boundary']) - {raw['center']}}
            for f in faces:
                if x in f:
                    a, b = [y for y in f if y != x]
                    if a in link and b in link:
                        link[a].add(b)
                        link[b].add(a)
            path = [third[(i - 1) % 5]]
            while path[-1] != third[i]:
                next_vertices = link[path[-1]] - set(path)
                assert len(next_vertices) == 1
                path.append(next(iter(next_vertices)))
            assert set(path) == set(link)
            assert fan['vertices'] == path
            assert fan['internal_vertices'] == path[1:-1]
            assert fan['degree'] == len(graph[x])
            assert fan['gap'] == (path[-1] not in graph[path[0]])
            reconstructed_walk.extend(path[:-1])
        assert collar['walk'] == reconstructed_walk
        assert collar['is_original_simple_cycle'] == (len(reconstructed_walk) >= 3 and len(reconstructed_walk) == len(set(reconstructed_walk)))
        pair_count += check_gluing(raw, produced['full_O_gluing_records'], graph)
        assert len(produced['comparisons']) == len(checked['comparisons'])
        total_cycles, total_fixed = 0, 0
        for expected, result in zip(checked['comparisons'], produced['comparisons']):
            assert result['source_iterate'] == expected['source_iterate']
            assert result['target_iterate'] == expected['target_iterate']
            assert result['difference_vertices'] == expected['difference']
            assert len(result['components']) == len(expected['components'])
            for eq, pq in zip(expected['components'], result['components']):
                q, attachments = set(eq['vertices']), set(eq['attachments'])
                assert pq['vertices'] == eq['vertices']
                assert pq['attachments'] == eq['attachments']
                assert pq['attachment_count'] == len(attachments)
                assert len(pq['original_neighbor_rows']) == len(q)
                for vertex, row in zip(sorted(q), pq['original_neighbor_rows']):
                    assert row['vertex'] == vertex and row['neighbors'] == sorted(graph[vertex])
                    assert row['rotation'] == raw['rotation'][vertex]
                keep = q | attachments
                gluing = produced['full_O_gluing_records'][pq['gluing_record_id']]
                assert gluing['kept_vertices'] == sorted(keep)
                assert pq['incident_original_face_ids'] == [j for j, f in enumerate(faces) if q & set(f)]
                v_boundary = pq['v_facing_boundary']
                rcomp = next(set(part) for part in components(graph, set(graph) - q) if raw['center'] in part)
                assert v_boundary['v_component_after_deleting_Q'] == sorted(rcomp)
                restricted = [dict(vertex=x, rotation=[y for y in raw['rotation'][x] if y in rcomp]) for x in sorted(rcomp)]
                assert v_boundary['induced_rotation_rows'] == restricted
                restrict_rotation = {row['vertex']: row['rotation'] for row in restricted}
                wanted_walk = v_boundary['Q_facing_face_boundary_closed_walk']
                # Enumerate every face of the restricted rotation directly.
                darts = {(x, y) for x in rcomp for y in graph[x] & rcomp}
                face_walks = []
                while darts:
                    start = min(darts)
                    current, walk = start, []
                    while current in darts:
                        darts.remove(current)
                        a, b = current
                        walk.append(a)
                        row = restrict_rotation[b]
                        current = (b, row[(row.index(a) - 1) % len(row)])
                    assert current == start
                    face_walks.append(walk)
                assert unoriented(wanted_walk) in {unoriented(walk) for walk in face_walks}
                assert set(wanted_walk) <= attachments
                original_third = {}
                for face in faces:
                    for i in range(3):
                        original_third[face[i], face[(i + 1) % 3]] = face[(i + 2) % 3]
                thirds = [original_third[wanted_walk[i], wanted_walk[(i + 1) % len(wanted_walk)]] for i in range(len(wanted_walk))]
                assert v_boundary['Q_facing_original_third_vertices'] == thirds
                assert set(thirds) <= q
                b_edges = {tuple(sorted((raw['boundary'][i], raw['boundary'][(i + 1) % 5]))) for i in range(5)}
                walk_edges = {tuple(sorted((wanted_walk[i], wanted_walk[(i + 1) % len(wanted_walk)]))) for i in range(len(wanted_walk))}
                assert not walk_edges & b_edges
                separator = v_boundary['selected_original_separator']
                selected = separator['cycle']
                assert len(selected) == len(set(selected)) >= 3
                assert {tuple(sorted((selected[i], selected[(i + 1) % len(selected)]))) for i in range(len(selected))} <= walk_edges
                selected_sides = cycle_sides(selected, faces, owners)
                assert separator['sides'] == selected_sides
                center_side = next(side for side in selected_sides if raw['center'] in side)
                opposite_side = next(side for side in selected_sides if raw['center'] not in side)
                assert len(center_side) >= 2 and q <= set(opposite_side)
                assert separator['center_side'] == center_side and separator['opposite_side'] == opposite_side
                assert separator['fixed'] and separator['contains_difference_opposite']
                assert separator['rigidity_trigger'] == (len(selected) == 5)
                if s34 and s5:
                    assert len(selected) >= 6
                collars = eq['collar_boundaries']
                contours = pq['contours']
                assert len(contours) == len(collars)
                actual_signatures = []
                all_crossed = []
                for contour in contours:
                    darts = contour['crossing_darts']
                    assert all(a in q and b in attachments for a, b in darts)
                    crossed = sorted(tuple(sorted((a, b))) for a, b in darts)
                    all_crossed.extend(crossed)
                    assert len(darts) == len(contour['face_ids']) == len(contour['external_trace'])
                    for i, (a, b) in enumerate(darts):
                        next_dart = darts[(i + 1) % len(darts)]
                        face = faces[contour['face_ids'][i]]
                        assert set((a, b)) | set(next_dart) == set(face)
                        assert contour['external_trace'][i] == b
                    raw_trace = contour['external_trace']
                    compressed = [x for i, x in enumerate(raw_trace) if x != raw_trace[i - 1]] or raw_trace[:1]
                    projected = open_walk(contour['compressed_closed_walk'])
                    assert unoriented(compressed) == unoriented(projected)
                    assert contour['is_original_simple_cycle'] == (len(projected) >= 3 and len(projected) == len(set(projected)))
                    actual_signatures.append((unoriented(projected), tuple(sorted(contour['face_ids'])), tuple(crossed)))
                    if contour['is_original_simple_cycle']:
                        assert contour['sides'] == cycle_sides(projected, faces, owners)
                expected_signatures = [(tuple(row['projected_walk']), tuple(row['mixed_face_ids']),
                                        tuple(map(tuple, row['crossing_edges']))) for row in collars]
                assert sorted(actual_signatures) == sorted(expected_signatures)
                assert sorted(all_crossed) == sorted(tuple(sorted((x, y))) for x in q for y in graph[x] - q)
                contour_count += len(contours)
                cycles = simple_cycles(graph, attachments)
                supplied_cycles = pq['all_attachment_simple_cycles']
                assert {unoriented(row['cycle']) for row in supplied_cycles} == {unoriented(c) for c in cycles}
                assert len(supplied_cycles) == len(cycles)
                for row in supplied_cycles:
                    expected_sides = cycle_sides(row['cycle'], faces, owners)
                    assert row['sides'] == expected_sides
                    center_side = next(side for side in expected_sides if raw['center'] in side)
                    opposite_side = next(side for side in expected_sides if raw['center'] not in side)
                    assert row['center_side'] == center_side and row['opposite_side'] == opposite_side
                    assert row['fixed']
                    assert row['contains_difference_opposite'] == bool(set(expected['difference']) & set(opposite_side))
                    assert row['rigidity_trigger'] == (len(row['cycle']) == 5 and len(center_side) >= 2)
                total_cycles += len(cycles)
            fixed = expected['all_fixed_original_five_cycles']
            actual = result['fixed_five_cycles']
            assert {unoriented(row['cycle']) for row in actual} == {unoriented(row['cycle']) for row in fixed}
            assert len(actual) == len(fixed)
            fixed_table = {unoriented(row['cycle']): row for row in fixed}
            for row in actual:
                match = fixed_table[unoriented(row['cycle'])]
                assert row['center_side'] == match['center_side']
                assert row['opposite_side'] == match['other_side']
                assert row['sides'] == cycle_sides(row['cycle'], faces, owners)
                assert row['fixed']
                assert row['contains_difference_opposite'] == bool(match['differences_in_other_side'])
                assert row['rigidity_trigger'] == match['rigidity_applicable']
            expected_violations = [row for row in actual if row['rigidity_trigger'] and row['contains_difference_opposite']]
            assert result['rigidity_violations'] == expected_violations
            assert result['collar_fixed'] == (not (set(collar['walk']) & set(expected['difference'])))
            total_fixed += len(fixed)
        reviewed.append(dict(name=raw['name'], attachment_cycles=total_cycles, fixed_five_cycles=total_fixed))
    return dict(boundary_projection='mixed-face midpoint degree-two graph',
                controls=reviewed, complete_contours=contour_count,
                v_facing_faces_and_original_separators_verified=True,
                complete_attachment_cycles_verified=True, complete_fixed_five_cycles_verified=True,
                complete_full_O_pair_gluing_records=pair_count)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=AUDIT / 'controls.json')
    parser.add_argument('--output', type=Path, default=AUDIT / 'review-certificate.json')
    parser.add_argument('--separation', type=Path, default=AUDIT / 'separation-certificate.json')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    source = json.loads(args.input.read_text())
    for relative, expected in source['provenance_inputs'].items():
        assert sha256((ROOT / relative).read_bytes()).hexdigest() == expected
    result = dict(schema='independent-d2-separation-review-v1',
                  imports_producers=False,
                  input_sha256=sha256(args.input.read_bytes()).hexdigest(),
                  checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  controls=[inspect(c) for c in source['controls']])
    assert args.separation.exists(), 'Produce the separation certificate before independent review'
    result['separation_sha256'] = sha256(args.separation.read_bytes()).hexdigest()
    separation = json.loads(args.separation.read_text())
    assert separation['source_sha256'] == result['input_sha256']
    assert separation['producer_sha256'] == sha256((ROOT / 'scripts/c5_d2_separation.py').read_bytes()).hexdigest()
    result['separation_review'] = review_separation(source, separation, result['controls'])
    encoded = json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        assert args.output.read_text() == encoded, 'Independent replay differs'
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(json.dumps(dict(status='INDEPENDENT D2 CHECK OK', controls=[
        dict(name=row['name'], S5=row['S5'], fibre=row['complete_fibre_size'],
             actual_exchanges=row['actual_exchange_count'],
             attachment_sizes=[[len(q['attachments']) for q in c['components']] for c in row['comparisons']])
        for row in result['controls']]), sort_keys=True))


if __name__ == '__main__':
    main()
