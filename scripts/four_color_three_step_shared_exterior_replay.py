#!/usr/bin/env python3
"""Replay the shared-exterior certificate using only literal original edges.

No generator, production solver, networkx, or earlier audit module is imported.
The full finite coloring family is re-enumerated; empty fibres are checked too.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

COLORS = tuple(range(4))
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def edges_checked(values):
    answer = {tuple(sorted(edge)) for edge in values}
    assert len(answer) == len(values)
    assert all(len(edge) == 2 and edge[0] < edge[1] for edge in answer)
    return answer


def canonical_colors(word):
    names = {}
    return tuple(names.setdefault(color, len(names)) for color in word)


def proper(word, edges):
    return all(word[u] != word[v] for u, v in edges)


def base_colorings(edges):
    return [word for word in product(COLORS, repeat=9) if proper(word, edges)]


def validate_contract(contract):
    assert contract['vertices'] == list(range(17))
    assert contract['elimination_order'] == [0, 1, 2]
    assert contract['shared_interface'] == [3, 4, 5, 6, 7, 8, 16]
    assert contract['new_edges'] == [[2, 16]]
    cycle = contract['C_order']
    assert cycle == [9, 10, 13, 12, 11, 14, 15, 16]
    core = edges_checked(contract['base_core_edges'])
    edges = edges_checked(contract['original_edges'])
    cycle_edges = {tuple(sorted(edge)) for edge in zip(cycle, cycle[1:] + cycle[:1])}
    assert edges == core | cycle_edges | {(2, 16), (3, 9), (4, 13), (5, 11), (6, 15)}
    assert {v if u == 0 else u for u, v in edges if 0 in (u, v)} == {1, 2, 3, 4, 7}
    assert {v if u == 1 else u for u, v in edges if 1 in (u, v)} == {0, 2, 5, 6, 7}
    exterior = {edge for edge in edges if not set(edge) & {0, 1, 2}}
    assert edges_checked(contract['exterior_edges']) == exterior
    faces = contract['oriented_faces']
    darts = Counter(edge for face in faces for edge in zip(face, face[1:] + face[:1]))
    expected = {(u, v) for u, v in edges} | {(v, u) for u, v in edges}
    assert set(darts) == expected and set(darts.values()) == {1}
    assert 17 - len(edges) + len(faces) == 2
    # Each local rotation obtained from facial successors must be one cycle.
    for vertex in range(17):
        following = {}
        for face in faces:
            for i, point in enumerate(face):
                if point == vertex:
                    a, b = face[i - 1], face[(i + 1) % len(face)]
                    assert a not in following
                    following[a] = b
        start = next(iter(following))
        visited, current = set(), start
        while current not in visited:
            visited.add(current)
            current = following[current]
        assert current == start and visited == set(following)
    def same_cycle(face):
        if len(face) != len(cycle) or set(face) != set(cycle):
            return False
        start = face.index(cycle[0])
        aligned = face[start:] + face[:start]
        reversed_cycle = [cycle[0]] + list(reversed(cycle[1:]))
        return aligned == cycle or aligned == reversed_cycle
    assert any(same_cycle(face) for face in faces)
    return core, edges, exterior


def verify_histories(edges, order, records):
    factors = [(set(edge), {edge}) for edge in edges]
    summary = []
    for vertex, record in zip(order, records):
        bucket = [(scope, causes) for scope, causes in factors if vertex in scope]
        factors = [(scope, causes) for scope, causes in factors if vertex not in scope]
        scope = tuple(sorted(set().union(*(scope for scope, _ in bucket)) - {vertex}))
        causes = set().union(*(causes for _, causes in bucket))
        assert record['eliminated_vertex'] == vertex
        assert record['ordered_scope'] == list(scope)
        assert edges_checked(record['causal_original_edges']) == causes
        assert ((2, 16) in causes) == (vertex == 2)
        vertices = tuple(sorted({point for edge in causes for point in edge}))
        index = {point: i for i, point in enumerate(vertices)}
        checked_edges = [(index[u], index[v]) for u, v in causes]
        allowed = [set() for _ in product(COLORS, repeat=len(scope))]
        for colors in product(COLORS, repeat=len(vertices)):
            if proper(colors, checked_edges):
                pos = 0
                for point in scope:
                    pos = 4 * pos + colors[index[point]]
                allowed[pos].add(colors[index[vertex]])
        expected = [sorted(values) for values in allowed]
        assert record['full_fibres'] == expected
        count = sum(map(bool, expected))
        assert record['nonempty_rows'] == count
        assert record['empty_rows'] == len(expected) - count
        summary.append([count, len(expected) - count])
        factors.append((set(scope), causes))
    assert len(records) == len(order)
    return summary, factors


def verify_kernel(data, core, final_factors):
    boundary = data['contract']['shared_interface']
    edges = core | {(2, 16)}
    vertices = list(range(9)) + [16]
    indexes = {point: i for i, point in enumerate(vertices)}
    indexed_edges = [(indexes[u], indexes[v]) for u, v in edges]
    fibres = [[] for _ in product(COLORS, repeat=7)]
    for colors in product(COLORS, repeat=10):
        if proper(colors, indexed_edges):
            pos = 0
            for point in boundary:
                pos = 4 * pos + colors[indexes[point]]
            fibres[pos].append(list(colors[:3]))
    kernel = data['kernel']
    assert kernel['full_fibres'] == fibres
    assert sum(map(len, fibres)) == 2808
    assert sum(map(bool, fibres)) == 2340
    expected_remaining = {(tuple(sorted(scope)), tuple(sorted(causes))) for scope, causes in final_factors}
    supplied_remaining = {(tuple(f['ordered_scope']), tuple(sorted(edges_checked(f['causal_original_edges']))))
                          for f in kernel['remaining_factors']}
    # The full source retains outer factors; a core-only remaining list is
    # also permitted when explicitly marked in the kernel artifact.
    core_remaining = {(scope, causes) for scope, causes in expected_remaining
                      if all(set(edge) <= set(vertices) for edge in causes)}
    assert supplied_remaining in (expected_remaining, core_remaining)
    factor_lookups = []
    for factor in kernel['remaining_factors']:
        scope = factor['ordered_scope']
        causes = edges_checked(factor['causal_original_edges'])
        if len(causes) == 1:
            expected_rows = [list(row) for row in product(COLORS, repeat=2) if row[0] != row[1]]
            assert set(scope) == set(next(iter(causes)))
        else:
            final = data['history'][-1]
            assert scope == final['ordered_scope']
            assert causes == edges_checked(final['causal_original_edges'])
            expected_rows = [list(row) for row, allowed in
                             zip(product(COLORS, repeat=len(scope)), final['full_fibres']) if allowed]
        assert factor['rows'] == expected_rows
        if all(set(edge) <= set(vertices) for edge in causes):
            factor_lookups.append((scope, set(map(tuple, expected_rows))))
    # Reconstruct only after a whole boundary row satisfies every residual
    # core factor, then use that same assignment throughout the reverse chain.
    for row, direct in zip(product(COLORS, repeat=7), fibres):
        assignment = dict(zip(boundary, row))
        lifts = [assignment] if all(tuple(assignment[v] for v in scope) in rows
                                    for scope, rows in factor_lookups) else []
        for record in reversed(data['history']):
            extended = []
            for partial in lifts:
                pos = 0
                for v in record['ordered_scope']:
                    pos = 4 * pos + partial[v]
                extended.extend(partial | {record['eliminated_vertex']: color}
                                for color in record['full_fibres'][pos])
            lifts = extended
        reconstructed = sorted([assignment[v] for v in (0, 1, 2)] for assignment in lifts)
        assert reconstructed == direct
    rows = list(product(COLORS, repeat=7))
    alive = [row for row, lifts in zip(rows, fibres) if lifts]
    projections = kernel['projection_closure']
    supplied = {tuple(p['ordered_scope']): p['rows'] for p in projections}
    assert len(supplied) == len(projections) == 128
    projection_rows = 0
    for size in range(8):
        for scope in combinations(boundary, size):
            positions = [boundary.index(v) for v in scope]
            expected = sorted({tuple(row[pos] for pos in positions) for row in alive})
            assert supplied[scope] == [list(row) for row in expected]
            projection_rows += len(expected)
    return dict(lifts=2808, nonempty=2340, empty=len(fibres)-2340,
                projection_tables=128, projection_rows=projection_rows)


def enumerate_full_graph(edges):
    neighbors = {v: set() for v in range(17)}
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    colors = [-1] * 17
    colors[:3] = [0, 1, 2]
    remaining = set(range(3, 17))
    answers = []

    def visit():
        if not remaining:
            answers.append(tuple(colors))
            return
        candidates = [(len({colors[n] for n in neighbors[v] if colors[n] >= 0}), len(neighbors[v]), v)
                      for v in remaining]
        vertex = max(candidates)[2]
        forbidden = {colors[n] for n in neighbors[vertex]}
        remaining.remove(vertex)
        for color in COLORS:
            if color not in forbidden:
                colors[vertex] = color
                visit()
        colors[vertex] = -1
        remaining.add(vertex)

    visit()
    return sorted(answers)


def verify_outer(data, core_colorings):
    cycle = data['contract']['C_order']
    ports = [9, 13, 11, 15, 16]
    inner = [3, 4, 5, 6, 2]
    counts = {}
    old_counts = {}
    for colors in product(COLORS, repeat=5):
        counts[colors] = sum(all(word[v] != color for v, color in zip(inner, colors))
                             for word in core_colorings)
        old_counts[colors[:4]] = sum(all(word[v] != color for v, color in zip(inner[:4], colors[:4]))
                                    for word in core_colorings)
    expected = []
    accepted_patterns = set()
    for word in product(COLORS, repeat=8):
        if not all(word[i] != word[(i + 1) % 8] for i in range(8)):
            expected.append(0)
            continue
        fixed = dict(zip(cycle, word))
        port_colors = tuple(fixed[v] for v in ports)
        assert old_counts[port_colors[:4]] > 0
        expected.append(counts[port_colors])
        if counts[port_colors]:
            accepted_patterns.add(canonical_colors(word))
    outer = data['outer']
    assert outer['full_counts'] == expected
    positive = [count for count in expected if count]
    assert outer['literal_proper_count'] == outer['accepted_count'] == len(positive) == 6564
    assert outer['s4_pattern_count'] == len(accepted_patterns) == 274
    assert outer['min_lifts'] == min(positive) == 174
    assert outer['max_lifts'] == max(positive) == 324
    assert outer['total_lifts'] == sum(expected) == 1529784
    return dict(proper=6564, accepted=6564, patterns=274,
                min_lifts=min(positive), max_lifts=max(positive), total_lifts=sum(expected))


def all_partitions(points):
    if not points:
        yield ()
        return
    point, *rest = points
    for partition in all_partitions(rest):
        yield ((point,),) + partition
        for i, block in enumerate(partition):
            yield partition[:i] + ((point,) + block,) + partition[i+1:]


def verify_old_control(data, core, solutions):
    control = data['old_control']
    assert control['kernel_lifts'] == len(solutions) == 936
    assert control['kernel_nonempty'] == len({word[3:] for word in solutions}) == 732
    assert control['outer_all_accept'] is True
    d_control = control['d_control']
    assert d_control['name'] == 'PAIR-C0-D16'
    cycle = d_control['original_cycle']
    assert cycle == [2, 3, 4, 7, 5, 6]
    edges = edges_checked(d_control['original_edges'])
    assert edges == {edge for edge in core if 8 not in edge}
    patterns = sorted({canonical_colors(word) for word in product(COLORS, repeat=6)
                       if all(word[i] != word[(i+1) % 6] for i in range(6))})
    lookup = {word: i for i, word in enumerate(patterns)}
    accepted = 0
    for i, pattern in enumerate(patterns):
        fixed = dict(zip(cycle, pattern))
        if any(proper(fixed | {0: a, 1: b}, edges) for a, b in product(COLORS, repeat=2)):
            accepted |= 1 << i
    assert accepted == 4969575
    options = []
    for word in patterns:
        split_options = []
        for first, second in SPLITS:
            alternatives = set()
            mate = {a: b for pair in (first, second) for a, b in (pair, pair[::-1])}
            left = [i for i, color in enumerate(word) if color in first]
            right = [i for i, color in enumerate(word) if color in second]
            for lp in all_partitions(left):
                for rp in all_partitions(right):
                    partition = lp + rp
                    owner = {v: i for i, block in enumerate(partition) for v in block}
                    if any((word[i] in first) == (word[(i+1) % 6] in first)
                           and owner[i] != owner[(i+1) % 6] for i in range(6)):
                        continue
                    if any(owner[a] == owner[c] and owner[b] == owner[d] and owner[a] != owner[b]
                           for a, b, c, d in combinations(range(6), 4)):
                        continue
                    orbit = 0
                    for selected in product((False, True), repeat=len(partition)):
                        changed = list(word)
                        for swap, block in zip(selected, partition):
                            if swap:
                                for pos in block:
                                    changed[pos] = mate[word[pos]]
                        orbit |= 1 << lookup[canonical_colors(changed)]
                    alternatives.add(orbit)
            assert alternatives
            split_options.append(alternatives)
        options.append(split_options)
    current = ((1 << len(patterns)) - 1) ^ accepted
    rounds = []
    while True:
        remove = sum(1 << i for i, choices in enumerate(options)
                     if current >> i & 1 and any(not any(orbit & current == orbit for orbit in alternatives)
                                               for alternatives in choices))
        if not remove:
            break
        rounds.append(remove)
        current &= ~remove
    fixed = d_control['fixed_point']
    assert fixed['accepted_mask'] == accepted
    assert fixed['residual_mask'] == current == 2075405200
    assert fixed['residual_count'] == 16 and current.bit_count() == 16
    assert rounds == [67108872]
    assert fixed['pattern_order'] == [list(word) for word in patterns]
    assert len(fixed['rounds']) == 1 and fixed['rounds'][0]['removed_mask'] == rounds[0]
    return dict(inner_accepted=13, inner_blocked_fixed_point=16, deletion_rounds=1)


def adjacency(vertices, edges):
    graph = {vertex: set() for vertex in vertices}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph


def components_bfs(graph, colors, pair):
    """Traverse the actual induced graph, retaining every isolated vertex."""
    unseen = {vertex for vertex in graph if colors[vertex] in pair}
    answer = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        reached, pending = {start}, [start]
        while pending:
            vertex = pending.pop()
            following = graph[vertex] & unseen
            unseen.difference_update(following)
            reached.update(following)
            pending.extend(following)
        answer.append(tuple(sorted(reached)))
    return tuple(sorted(answer))


def triangle_canonical(colors):
    names = {colors[i]: i for i in range(3)}
    assert len(names) == 3
    unused = set(COLORS) - set(names)
    names[next(iter(unused))] = 3
    return tuple(names[color] for color in colors)


def digest_record(digest, record):
    digest.update(json.dumps(record, separators=(',', ':')).encode() + b'\n')


def verify_cross_rows(data, edges, exterior, representatives):
    cycle = data['contract']['C_order']
    interface = data['contract']['shared_interface']
    remaining = list(range(3, 17))
    whole_graph = adjacency(range(17), edges)
    outside_graph = adjacency(remaining, exterior)
    inside_graph = adjacency([0, 1, 2] + interface, edges - exterior)
    core_graph = adjacency(range(9), {edge for edge in edges if max(edge) < 9})
    ring_graph = adjacency(cycle, {edge for edge in edges if min(edge) >= 9})
    cut_edges = {edge for edge in edges if min(edge) < 9 <= max(edge)}
    assert cut_edges == {(2, 16), (3, 9), (4, 13), (5, 11), (6, 15)}
    pairs = list(combinations(COLORS, 2))
    index = {colors: i for i, colors in enumerate(representatives)}
    part_digest, swap_digest = sha256(), sha256()
    counts = dict(states=len(representatives), pair_partitions=0, joint_noncrossing_splits=0,
                  component_swaps=0, swaps_changing_outer_row=0,
                  swaps_preserving_outer_row=0, gluing_checks=0, core_outer_gluing_checks=0)
    outside_cache, ring_cache = {}, {}
    for i, colors in enumerate(representatives):
        row = tuple(colors[v] for v in remaining)
        if row not in outside_cache:
            outside_cache[row] = {pair: components_bfs(outside_graph, colors, pair) for pair in pairs}
        ring_row = tuple(colors[v] for v in cycle)
        if ring_row not in ring_cache:
            ring_cache[ring_row] = {pair: components_bfs(ring_graph, colors, pair) for pair in pairs}
        actual = {pair: components_bfs(whole_graph, colors, pair) for pair in pairs}
        for pair in pairs:
            outside_components = outside_cache[row][pair]
            inside_components = components_bfs(inside_graph, colors, pair)
            # Treat each piece's actual component as a connected star, then
            # traverse their union on the identical original vertex set.
            component_links = {(block[0], v) for block in outside_components + inside_components
                               for v in block[1:]}
            glued_graph = adjacency(range(17), component_links)
            assert components_bfs(glued_graph, colors, pair) == actual[pair]
            counts['gluing_checks'] += 1
            core_blocks = components_bfs(core_graph, colors, pair)
            ring_blocks = ring_cache[ring_row][pair]
            core_ring_links = {(block[0], v) for block in core_blocks + ring_blocks for v in block[1:]}
            core_ring_graph = adjacency(range(17), core_ring_links | cut_edges)
            assert components_bfs(core_ring_graph, colors, pair) == actual[pair]
            counts['core_outer_gluing_checks'] += 1
            counts['pair_partitions'] += 1
            digest_record(part_digest, [i, pair, actual[pair], outside_components])
            complementary = tuple(color for color in COLORS if color not in pair)
            for block in actual[pair]:
                changed = list(colors)
                for vertex in block:
                    changed[vertex] = pair[1] if colors[vertex] == pair[0] else pair[0]
                assert proper(changed, edges)
                assert components_bfs(whole_graph, changed, pair) == actual[pair]
                assert components_bfs(whole_graph, changed, complementary) == actual[complementary]
                target_id = index[triangle_canonical(changed)]
                digest_record(swap_digest, [i, pair, block, target_id, changed[:3]])
                counts['component_swaps'] += 1
                key = ('swaps_changing_outer_row' if any(changed[v] != colors[v] for v in cycle)
                       else 'swaps_preserving_outer_row')
                counts[key] += 1
        for first, second in SPLITS:
            boundary_blocks = [tuple(cycle.index(v) for v in block if v in cycle)
                               for block in actual[first] + actual[second]]
            owner = {vertex: j for j, block in enumerate(boundary_blocks) for vertex in block}
            assert not any(owner[a] == owner[c] and owner[b] == owner[d] and owner[a] != owner[b]
                           for a, b, c, d in combinations(range(8), 4))
            counts['joint_noncrossing_splits'] += 1
    counts.update(partition_sha256=part_digest.hexdigest(), transition_sha256=swap_digest.hexdigest(),
                  distinct_anchored_remaining_rows=len(outside_cache),
                  distinct_anchored_outer_rows=len(ring_cache))
    assert data['cross_row'] == counts
    control = data['splice_control']
    assert control['name'] == 'SWAP-TARGET-SPLICE-ZV'
    source = tuple(control['source_coloring'])
    target = tuple(control['true_target'])
    forged = tuple(control['forged_target'])
    pair, block = tuple(control['color_pair']), tuple(control['actual_component'])
    assert pair == (0, 1) and block == (8,)
    assert block in components_bfs(whole_graph, source, pair)
    expected = list(source)
    for vertex in block:
        expected[vertex] = pair[1] if source[vertex] == pair[0] else pair[0]
    assert target == tuple(expected) and forged != target
    assert [v for v in range(17) if forged[v] != target[v]] == control['illegal_changes'] == [3, 4]
    assert tuple(source[v] for v in cycle) == tuple(forged[v] for v in cycle)
    assert control['all_three_colorings_proper'] is True
    for word in (source, target, forged):
        assert proper(word, edges) and triangle_canonical(word) in index
    assert control['new_solution_rows_deleted'] == 0
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', required=True, type=Path)
    args = parser.parse_args()
    data = json.loads(args.results.read_text())
    core, edges, exterior = validate_contract(data['contract'])
    history, factors = verify_histories(edges, [0, 1, 2], data['history'])
    kernel = verify_kernel(data, core, factors)
    solutions = base_colorings(core)
    outer = verify_outer(data, solutions)
    old = verify_old_control(data, core, solutions)
    representatives = enumerate_full_graph(edges)
    supplied = data['full_colorings']
    assert supplied['triangle_anchor'] == [0, 1, 2]
    assert supplied['representatives'] == [list(word) for word in representatives]
    assert len(representatives) == 63741
    assert supplied['literal_count'] == 24 * len(representatives) == outer['total_lifts']
    cross_rows = verify_cross_rows(data, edges, exterior, representatives)
    receipt = dict(status='PASS', verifier='standard-library independent original-edge replay',
                   results_sha256=sha256(args.results.read_bytes()).hexdigest(),
                   history=history, kernel=kernel, outer=outer, old_control=old,
                   full_S4_representatives=len(representatives), cross_row=cross_rows,
                   forged_transition_rejected=True)
    target = args.results.parent / 'replay.json'
    target.write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    main()
