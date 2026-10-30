#!/usr/bin/env python3
"""Independently replay three-step relation controls from original edges.

This verifier uses only the standard library and the supplied literal graph
data.  It imports neither the generator nor the earlier elimination scripts.
Bucket histories are checked by enumeration of their accumulated original
edges; final fibres are checked by enumeration of all original assignments.
"""
from __future__ import annotations

import argparse
from itertools import combinations, product
import json
from pathlib import Path


COLORS = tuple(range(4))
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def edge_set(edges):
    result = {tuple(sorted(edge)) for edge in edges}
    assert all(len(edge) == 2 and edge[0] != edge[1] for edge in result)
    assert len(result) == len(edges), 'Duplicate original edge'
    return result


def brute_fibres(vertices, edges, boundary, eliminated):
    """Enumerate full original assignments, with every empty row retained."""
    vertices, boundary, eliminated = tuple(vertices), tuple(boundary), tuple(eliminated)
    assert set(vertices) == set(boundary) | set(eliminated)
    assert not set(boundary) & set(eliminated)
    fibres = {row: [] for row in product(COLORS, repeat=len(boundary))}
    original_solutions = []
    for colors in product(COLORS, repeat=len(vertices)):
        assignment = dict(zip(vertices, colors))
        if all(assignment[u] != assignment[v] for u, v in edges):
            row = tuple(assignment[v] for v in boundary)
            fibres[row].append(tuple(assignment[v] for v in eliminated))
            original_solutions.append(colors)
    return [sorted(lifts) for lifts in fibres.values()], original_solutions


def causal_stages(edges, order):
    """Only track which original edges belong to a bucket, never evaluate joins."""
    factors = [(set(edge), {edge}) for edge in edges]
    stages = []
    for vertex in order:
        selected = [(scope, cause) for scope, cause in factors if vertex in scope]
        assert selected
        factors = [(scope, cause) for scope, cause in factors if vertex not in scope]
        scope = set().union(*(scope for scope, _ in selected)) - {vertex}
        causes = set().union(*(cause for _, cause in selected))
        stages.append((vertex, tuple(sorted(scope)), causes))
        factors.append((scope, causes))
    return stages, factors


def replay_history(edges, order, records):
    stages, _ = causal_stages(edges, order)
    assert len(records) == len(order)
    sizes = []
    for (vertex, scope, causes), record in zip(stages, records):
        assert record['eliminated_vertex'] == vertex
        assert tuple(record['ordered_scope']) == scope
        assert edge_set(record['causal_original_edges']) == causes
        allowed = {row: set() for row in product(COLORS, repeat=len(scope))}
        causal_vertices = tuple(sorted(set().union(*(set(edge) for edge in causes))))
        for colors in product(COLORS, repeat=len(causal_vertices)):
            assignment = dict(zip(causal_vertices, colors))
            if all(assignment[u] != assignment[v] for u, v in causes):
                row = tuple(assignment[v] for v in scope)
                allowed[row].add(assignment[vertex])
        expected = [sorted(colors) for colors in allowed.values()]
        assert record['full_fibres'] == expected, ('history', vertex)
        nonempty = sum(bool(colors) for colors in expected)
        assert record['nonempty_rows'] == nonempty
        assert record['empty_rows'] == len(expected) - nonempty
        sizes.append(dict(vertex=vertex, rows=len(expected), nonempty=nonempty))
    return sizes


def verify_projection_closure(boundary, fibres, records):
    support = [row for row, lifts in zip(product(COLORS, repeat=len(boundary)), fibres)
               if lifts]
    supplied = {tuple(record['ordered_scope']): record['rows'] for record in records}
    assert len(records) == len(supplied) == 2 ** len(boundary)
    total = 0
    for size in range(len(boundary) + 1):
        for scope in combinations(boundary, size):
            indexes = [boundary.index(vertex) for vertex in scope]
            expected = sorted({tuple(row[i] for i in indexes) for row in support})
            assert supplied[scope] == [list(row) for row in expected], ('projection', scope)
            total += len(expected)
    return total


def verify_sources(result, core_edges, stages):
    sources = result['outer_sources']
    assert {source['name'] for source in sources} == {'ALT-OUTER-17', 'PLANAR-TWIN-17'}
    source_edges = {}
    for source in sources:
        assert source['vertex_order'] == list(range(17))
        edges = edge_set(source['original_edges'])
        source_edges[source['name']] = edges
        obtained, _ = causal_stages(edges, result['elimination_order'])
        assert obtained == stages, ('bucket causal identity', source['name'])
        assert {edge for edge in edges if max(edge) < 9} == core_edges
        cycle = source['C_order']
        assert len(cycle) == len(set(cycle)) == 8
        cycle_edges = {tuple(sorted(edge))
                       for edge in zip(cycle, cycle[1:] + cycle[:1])}
        attachments = {(3, 9), (4, 13), (5, 11), (6, 15)}
        assert edges == core_edges | cycle_edges | attachments
    assert source_edges['ALT-OUTER-17'] != source_edges['PLANAR-TWIN-17']
    witnesses = result['global_difference_witnesses']
    assert {witness['source'] for witness in witnesses} == set(source_edges)
    for witness in witnesses:
        colors = witness['full_coloring']
        assert len(colors) == 17 and set(colors) <= set(COLORS)
        for name, edges in source_edges.items():
            proper = all(colors[u] != colors[v] for u, v in edges)
            assert proper == (name == witness['source']), ('global difference', name)


def verify_outer_tensor(result, original_solutions):
    tensor = result['outer_tensor']
    assert tensor['port_order'] == [9, 13, 11, 15]
    core_colorings = sorted(original_solutions)
    assert tensor['core_colorings'] == [list(colors) for colors in core_colorings]
    expected, counts = [], []
    for ports in product(COLORS, repeat=4):
        indices = [i for i, colors in enumerate(core_colorings)
                   if all(colors[v] != p for v, p in zip((3, 4, 5, 6), ports))]
        expected.append(indices)
        counts.append(len(indices))
    assert tensor['full_fibre_indices'] == expected
    assert tensor['counts'] == counts
    assert min(counts) > 0
    # The exact outer Boolean relation is all proper C8 words for both orders;
    # complete fibres nevertheless distinguish the marked count control.
    count_lookup = dict(zip(product(COLORS, repeat=4), counts))
    boundary_support = [row for row, lifts in zip(product(COLORS, repeat=6),
                                                result['kernel']['full_fibres']) if lifts]
    boundary_counts = {
        ports: sum(all(row[i] != color for i, color in enumerate(ports))
                   for row in boundary_support)
        for ports in product(COLORS, repeat=4)}
    count_word = (0, 1, 0, 1, 2, 0, 1, 2)
    named_counts, global_counts = {}, {}
    for source in result['outer_sources']:
        cycle = source['C_order']
        proper_rows = 0
        normalized_rows = set()
        full_solution_count = nonempty_fibres = 0
        for word in product(COLORS, repeat=8):
            if all(word[i] != word[(i + 1) % 8] for i in range(8)):
                assignment = dict(zip(cycle, word))
                ports = tuple(assignment[v] for v in tensor['port_order'])
                assert count_lookup[ports] > 0
                full_solution_count += count_lookup[ports]
                nonempty_fibres += boundary_counts[ports]
                proper_rows += 1
                names = {}
                normalized_rows.add(tuple(names.setdefault(c, len(names)) for c in word))
        assert proper_rows == 6564
        assert len(normalized_rows) == 274
        assignment = dict(zip(cycle, count_word))
        ports = tuple(assignment[v] for v in tensor['port_order'])
        named_counts[source['name']] = count_lookup[ports]
        global_counts[source['name']] = dict(
            full_solution_count=full_solution_count, nonempty_fibres=nonempty_fibres,
            complete_interface_rows=4**14, empty_fibres=4**14-nonempty_fibres)
    assert named_counts == {'ALT-OUTER-17': 291, 'PLANAR-TWIN-17': 276}
    boolean_control = result['outer_boolean_control']
    assert boolean_control == dict(
        proper_outer_words_per_source=6564, s4_patterns=274,
        accepts_all_proper_words=True, comparison_word=list(count_word),
        comparison_counts=named_counts, global_counts=global_counts)
    assert [(global_counts[name]['full_solution_count'], global_counts[name]['nonempty_fibres'])
            for name in ('ALT-OUTER-17', 'PLANAR-TWIN-17')] == [
                (1924992, 1499520), (1913472, 1488000)]
    return dict(port_rows=256, min_lifts=min(counts), max_lifts=max(counts),
                proper_C8_rows_per_source=6564, named_full_fibre_counts=named_counts)


def normalize(word):
    seen = {}
    return tuple(seen.setdefault(color, len(seen)) for color in word)


def set_partitions(points):
    """Generate via restricted-growth labels, independently of the D tool."""
    points = tuple(points)
    def extend(labels):
        if len(labels) == len(points):
            blocks = [[] for _ in range(max(labels, default=-1) + 1)]
            for point, label in zip(points, labels):
                blocks[label].append(point)
            yield tuple(tuple(block) for block in blocks)
            return
        for label in range(max(labels, default=-1) + 2):
            yield from extend(labels + [label])
    yield from extend([])


def independent_D_options(patterns):
    """All joint NC partitions, forced original boundary edges, whole orbits."""
    index = {row: i for i, row in enumerate(patterns)}
    table = []
    for row in patterns:
        splits = []
        for pairs in SPLITS:
            groups = [tuple(i for i, color in enumerate(row) if color in pair)
                      for pair in pairs]
            mate = {color: pair[1-j] for pair in pairs for j, color in enumerate(pair)}
            options = {}
            for first in set_partitions(groups[0]):
                for second in set_partitions(groups[1]):
                    blocks = tuple(sorted(first + second))
                    owner = {v: j for j, block in enumerate(blocks) for v in block}
                    if any(any(row[i] in pair and row[(i+1) % len(row)] in pair
                               for pair in pairs) and owner[i] != owner[(i+1) % len(row)]
                           for i in range(len(row))):
                        continue
                    if any(owner[a] == owner[c] and owner[b] == owner[d]
                           and owner[a] != owner[b]
                           for a, b, c, d in combinations(range(len(row)), 4)):
                        continue
                    orbit = 0
                    for selected in product((False, True), repeat=len(blocks)):
                        changed = list(row)
                        for swap, block in zip(selected, blocks):
                            if swap:
                                for v in block:
                                    changed[v] = mate[row[v]]
                        assert all(changed[i] != changed[(i+1) % len(row)]
                                   for i in range(len(row)))
                        orbit |= 1 << index[normalize(changed)]
                    options[blocks] = orbit
            assert options
            splits.append(options)
        table.append(splits)
    return table


def verify_D_control(result):
    control = result['d_control']
    assert control['name'] == 'PAIR-C0-D16'
    cycle = control['original_cycle']
    assert cycle == [2, 3, 4, 7, 5, 6]
    edges = edge_set(control['original_edges'])
    assert edges == {tuple(edge) for edge in result['core_edges'] if 8 not in edge}
    patterns = sorted({normalize(word) for word in product(COLORS, repeat=6)
                       if all(word[i] != word[(i+1) % 6] for i in range(6))})
    accepted = 0
    for i, row in enumerate(patterns):
        assignment = dict(zip(cycle, row))
        if any(all((assignment | {0: x1, 1: x2})[u] !=
                   (assignment | {0: x1, 1: x2})[v] for u, v in edges)
               for x1, x2 in product(COLORS, repeat=2)):
            accepted |= 1 << i
    fixed = control['fixed_point']
    assert fixed['ring_length'] == 6
    assert fixed['pattern_order'] == [list(row) for row in patterns]
    assert fixed['complementary_splits'] == [[list(pair) for pair in pairs] for pairs in SPLITS]
    assert fixed['accepted_mask'] == accepted == 4969575
    assert fixed['accepted_count'] == accepted.bit_count() == 13
    options = independent_D_options(patterns)
    current = ((1 << len(patterns)) - 1) ^ accepted
    assert fixed['initial_obstruction_mask'] == current
    assert fixed['initial_obstruction_count'] == current.bit_count() == 18
    round_index = 0
    while True:
        removed = {}
        for j, splits in enumerate(options):
            if not (current >> j & 1):
                continue
            for split, alternatives in enumerate(splits):
                if not any(orbit & current == orbit for orbit in alternatives.values()):
                    removed[j] = split
                    break
        if not removed:
            break
        record = fixed['rounds'][round_index]
        remove_mask = sum(1 << j for j in removed)
        assert record['round'] == round_index + 1
        assert record['before_mask'] == current
        assert record['removed_mask'] == remove_mask
        assert record['after_mask'] == current & ~remove_mask
        supplied = {item['pattern_index']: item for item in record['removals']}
        assert set(supplied) == set(removed)
        for j, split in removed.items():
            item = supplied[j]
            assert item['pattern'] == list(patterns[j]) and item['split'] == split
            assert {alternative['orbit_mask'] for alternative in item['required_alternatives']} == set(options[j][split].values())
            for alternative in item['required_alternatives']:
                partition = tuple(sorted(tuple(block) for block in alternative['joint_partition']))
                orbit = options[j][split][partition]
                assert alternative['orbit_mask'] == orbit
                missing = [k for k in range(len(patterns)) if orbit >> k & 1 and not current >> k & 1]
                assert alternative['missing_pattern_indices'] == missing
        current &= ~remove_mask
        round_index += 1
    assert len(fixed['rounds']) == round_index == 1
    assert fixed['residual_mask'] == current == 2075405200
    assert fixed['residual_count'] == current.bit_count() == 16
    survivors = {item['pattern_index']: item for item in fixed['survivors']}
    assert set(survivors) == {j for j in range(len(patterns)) if current >> j & 1}
    for j, item in survivors.items():
        assert item['pattern'] == list(patterns[j])
        assert {witness['split'] for witness in item['witnesses']} == {0, 1, 2}
        for witness in item['witnesses']:
            partition = tuple(sorted(tuple(block) for block in witness['joint_partition']))
            orbit = options[j][witness['split']][partition]
            assert orbit == witness['orbit_mask'] and orbit & current == orbit
    return dict(states=len(patterns), accepted=13, initial_obstructions=18,
                residual=16, rounds=round_index)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', required=True, type=Path)
    args = parser.parse_args()
    result = json.loads(args.results.read_text())
    assert result['colors'] == list(COLORS)
    assert result['elimination_order'] == [0, 1, 2]
    assert result['core_vertices'] == list(range(9))
    core_edges = edge_set(result['core_edges'])
    kernel = result['kernel']
    boundary = kernel['boundary_order']
    assert boundary == list(range(3, 9))
    fibres, solutions = brute_fibres(result['core_vertices'], core_edges, boundary,
                                    result['elimination_order'])
    assert kernel['full_fibres'] == [[list(lift) for lift in lifts] for lifts in fibres]
    assert len(solutions) == 936
    assert sum(bool(lifts) for lifts in fibres) == 732
    assert fibres[list(product(COLORS, repeat=6)).index((0, 1, 1, 0, 0, 1))] == []
    history = result.get('history', kernel.get('history'))
    projection_closure = result.get('projection_closure', kernel.get('projection_closure'))
    history_summary = replay_history(core_edges, result['elimination_order'], history)
    projection_rows = verify_projection_closure(boundary, fibres, projection_closure)
    stages, _ = causal_stages(core_edges, result['elimination_order'])
    verify_sources(result, core_edges, stages)
    controls = {}
    expected_counts = {'historical_adjacent9': (7776, 2256),
                       'historical_tree9': (26244, 4096),
                       'planar_core9': (936, 732)}
    for control in result['controls']:
        observed, original = brute_fibres(control['vertices'], edge_set(control['original_edges']),
                                         control['boundary_order'], result['elimination_order'])
        assert control['full_fibres'] == [[list(lift) for lift in lifts] for lifts in observed]
        counts = (len(original), sum(bool(lifts) for lifts in observed))
        assert counts == expected_counts[control['name']]
        assert control['solution_count'] == counts[0]
        assert control['nonempty_fibres'] == counts[1]
        controls[control['name']] = counts
    assert {'historical_adjacent9', 'historical_tree9'} <= set(controls)
    outer_summary = verify_outer_tensor(result, solutions)
    d_summary = verify_D_control(result)
    print(json.dumps(dict(status='PASS', method='independent original-edge enumeration',
                          core_solution_count=len(solutions), core_nonempty_fibres=732,
                          core_empty_fibres=4096 - 732, history=history_summary,
                          projection_scopes=64, projection_rows=projection_rows,
                          controls=controls, outer_tensor=outer_summary,
                          original_C0_D=d_summary), sort_keys=True))


if __name__ == '__main__':
    main()
