#!/usr/bin/env python3
"""Independent bounded BR-SD-1a list/edge calibration; no repository solver imports."""
import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

COLORS = ['A', 'B', 'C', 'D']
D = 3
SCHEMA = 'BR-SD-1a-controls-v1'


def edge(a, b):
    return tuple(sorted((a, b)))


def adjacent(vertices, edges):
    out = {v: set() for v in vertices}
    for a, b in edges:
        assert a != b and a in out and b in out
        out[a].add(b)
        out[b].add(a)
    return out


def components(vertices, edges):
    adj = adjacent(vertices, edges)
    unseen = set(vertices)
    result = []
    while unseen:
        root = min(unseen)
        todo = [root]
        unseen.remove(root)
        found = []
        while todo:
            v = todo.pop()
            found.append(v)
            for w in sorted(adj[v]):
                if w in unseen:
                    unseen.remove(w)
                    todo.append(w)
        result.append(sorted(found))
    return sorted(result)


def actual_blocks(vertices, edges):
    """Tarjan edge blocks derived only from the declared original C edges."""
    adj = adjacent(vertices, edges)
    stamp = {}
    low = {}
    stack = []
    blocks = []
    def visit(v, parent):
        stamp[v] = low[v] = len(stamp)
        for w in sorted(adj[v]):
            if w == parent:
                continue
            if w not in stamp:
                stack.append(edge(v, w))
                visit(w, v)
                low[v] = min(low[v], low[w])
                if low[w] >= stamp[v]:
                    found = []
                    while True:
                        item = stack.pop()
                        found.append(item)
                        if item == edge(v, w):
                            break
                    blocks.append(sorted(found))
            elif stamp[w] < stamp[v]:
                stack.append(edge(v, w))
                low[v] = min(low[v], stamp[w])
    for v in vertices:
        if v not in stamp:
            visit(v, None)
    assert not stack
    return sorted(blocks)


def make_graph(name, lengths, arms, mode, sample_size=None):
    l1, l2, l3 = lengths
    assert min(lengths) >= 3 and all(n % 2 for n in lengths)
    cycles = {
        'J1': ['r'] + ['a' + str(i) for i in range(1, l1)],
        'J2': ['r', 'u'] + ['b' + str(i) for i in range(1, l2 - 1)],
        'J3': ['v'] + ['c' + str(i) for i in range(1, l3)],
    }
    block_edges = {}
    for block, cycle in cycles.items():
        block_edges[block] = sorted(edge(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle)))
    block_edges['uv'] = [edge('u', 'v')]
    arm_paths = {}
    contacts = []
    for prefix, anchor, length in [('p', 'a1', arms[0]), ('q', 'c1', arms[1])]:
        path = [anchor] + [prefix + str(i) for i in range(1, length + 1)]
        arm_paths[prefix] = path
        contacts.append(path[-1])
        for i in range(length):
            block_edges[prefix + '-bridge-' + str(i + 1)] = [edge(path[i], path[i + 1])]
    edges = sorted({e for es in block_edges.values() for e in es})
    vertices = sorted({v for e in edges for v in e})
    adj = adjacent(vertices, edges)
    assert len(components(vertices, edges)) == 1
    cutpoints = []
    cut_witness = {}
    for v in vertices:
        remaining = [w for w in vertices if w != v]
        comps = components(remaining, [e for e in edges if v not in e])
        if len(comps) > 1:
            cutpoints.append(v)
        cut_witness[v] = comps
    assert actual_blocks(vertices, edges) == sorted(block_edges.values())
    selected = {}
    for block in ['J1', 'J2']:
        candidates = [v for v in cycles[block] if v not in cutpoints and v not in contacts]
        assert candidates
        selected[block] = candidates[0]
        assert len(adj[candidates[0]]) == 2
    options = []
    for v in vertices:
        degree = len(adj[v])
        masks = [m for m in range(1, 16) if m.bit_count() == degree]
        if v in selected.values():
            masks = [m for m in masks if m & (1 << D)]
        assert masks
        options.append(masks)
    total = math.prod(len(x) for x in options)
    if mode == 'exhaustive':
        ranks = list(range(total))
    else:
        assert sample_size and total >= sample_size > 1
        ranks = [i * (total - 1) // (sample_size - 1) for i in range(sample_size)]
        assert len(set(ranks)) == sample_size
    data = {
        'name': name,
        'scope': 'abstract list graph; no actual target disk or beta-refusing source is supplied',
        'target_source_status': 'not triggered',
        'list_control_status': 'triggered and holds',
        'cycle_lengths': list(lengths), 'arm_lengths': list(arms),
        'vertex_order': vertices, 'original_C_edges': edges,
        'named_cycles': cycles, 'original_block_edges': block_edges,
        'original_arm_paths': arm_paths, 's_contacts_from_original_edges': contacts,
        'articulation_vertices_from_original_edges': cutpoints,
        'all_vertex_deletion_components': cut_witness,
        'all_original_C_neighbors': {v: sorted(adj[v]) for v in vertices},
        'degree_C': {v: len(adj[v]) for v in vertices},
        'selected_w': selected,
        'selection_checks': {block: {
            'vertex': w, 'cycle': block, 'is_C_articulation': False,
            'is_s_contact': False, 'degree_C': 2,
            'actual_C_neighbors': sorted(adj[w]),
            'original_s_edges_checked': [edge('s', p) for p in contacts],
        } for block, w in selected.items()},
        'mask_semantics': 'bit i denotes COLORS[i]; a row stores every list mask and every assigned color in vertex_order',
        'assignment_scope': {
            'list_sizes': 'exactly degree_C at every original vertex',
            'D_presence_required_at': [selected['J1'], selected['J2']],
            'contact_lists': 'unrestricted tight degree lists in this abstract enumeration',
            'all_vertex_options': {v: opts for v, opts in zip(vertices, options)},
            'total_domain_size': total, 'mode': mode,
            'enumerated_ranks': ranks if mode != 'exhaustive' else {'start': 0, 'stop_exclusive': total, 'step': 1},
            'enumerated_count': len(ranks),
        },
    }
    return data, options, ranks


def masks_at_rank(options, rank):
    result = [0] * len(options)
    for i in range(len(options) - 1, -1, -1):
        rank, j = divmod(rank, len(options[i]))
        result[i] = options[i][j]
    assert rank == 0
    return result


def solve(vertices, edges, masks, all_solutions=False):
    """Independent direct vertex backtracking over literal original edges."""
    adj = adjacent(vertices, edges)
    ix = {v: i for i, v in enumerate(vertices)}
    neighbors = [[ix[w] for w in sorted(adj[v])] for v in vertices]
    values = [[c for c in range(4) if mask & (1 << c)] for mask in masks]
    assigned = [-1] * len(vertices)
    solutions = []
    nodes = 0
    def visit():
        nonlocal nodes
        nodes += 1
        remaining = [i for i, c in enumerate(assigned) if c < 0]
        if not remaining:
            solutions.append(assigned.copy())
            return not all_solutions
        choices = []
        for i in remaining:
            banned = {assigned[j] for j in neighbors[i] if assigned[j] >= 0}
            available = [c for c in values[i] if c not in banned]
            if not available:
                return False
            choices.append((len(available), -len(neighbors[i]), i, available))
        _, _, i, available = min(choices)
        for c in available:
            assigned[i] = c
            stop = visit()
            assigned[i] = -1
            if stop:
                return True
        return False
    visit()
    solutions.sort()
    return solutions, nodes


def validate_full_tuple(vertices, edges, masks, colors):
    assert len(colors) == len(vertices) == len(masks)
    asg = dict(zip(vertices, colors))
    assert all(0 <= c < 4 and m & (1 << c) for c, m in zip(colors, masks))
    assert all(asg[a] != asg[b] for a, b in edges)


def list_records(graph, options, ranks):
    vertices = graph['vertex_order']
    edges = graph['original_C_edges']
    w1 = vertices.index(graph['selected_w']['J1'])
    w2 = vertices.index(graph['selected_w']['J2'])
    records = []
    node_total = 0
    for rank in ranks:
        masks = masks_at_rank(options, rank)
        assert all(m.bit_count() == graph['degree_C'][v] for v, m in zip(vertices, masks))
        assert masks[w1] & 8 and masks[w2] & 8
        # If an uncolorable blockwise-uniform assignment existed, private
        # w1/w2 force these two palettes, whose intersection contains D.
        assert masks[w1] & masks[w2] & 8
        found, nodes = solve(vertices, edges, masks)
        assert found, ('unexpected list counterexample', graph['name'], rank, masks)
        validate_full_tuple(vertices, edges, masks, found[0])
        records.append([masks, found[0]])
        node_total += nodes
    return {
        'row_format': ['all_list_masks_in_vertex_order', 'full_coloring_tuple_in_vertex_order'],
        'records': records,
        'summary': {
            'enumerated_assignments': len(records), 'colorable': len(records),
            'uncolorable': 0, 'forced_J1_J2_palette_D_overlap': len(records),
            'direct_backtracking_nodes': node_total,
        },
    }


def removed_D_negative(graph):
    palettes = {'J1': 3, 'J2': 12, 'uv': 1, 'J3': 6}
    vertices = graph['vertex_order']
    masks = []
    at_vertex = {}
    for v in vertices:
        blocks = [b for b, es in graph['original_block_edges'].items() if any(v in e for e in es)]
        assert all((palettes[a] & palettes[b]) == 0 for a, b in itertools.combinations(blocks, 2))
        union = 0
        for b in blocks:
            union |= palettes[b]
        assert union.bit_count() == graph['degree_C'][v]
        masks.append(union)
        at_vertex[v] = {
            'actual_original_neighbors': graph['all_original_C_neighbors'][v],
            'blocks': blocks, 'incident_palettes': {b: palettes[b] for b in blocks},
            'list_mask': union, 'list_colors': [COLORS[c] for c in range(4) if union & (1 << c)],
            'degree_C': graph['degree_C'][v],
            'is_s_contact': v in graph['s_contacts_from_original_edges'],
            'D_present': bool(union & 8),
        }
    for b, es in graph['original_block_edges'].items():
        expected_size = 2 if b in graph['named_cycles'] else 1
        assert palettes[b].bit_count() == expected_size
    assert palettes['J1'] | palettes['J2'] == 15
    assert palettes['J1'] & palettes['J2'] == 0
    tuples, nodes = solve(vertices, graph['original_C_edges'], masks, all_solutions=True)
    assert not tuples
    w1 = graph['selected_w']['J1']
    w2 = graph['selected_w']['J2']
    assert not at_vertex[w1]['D_present'] and at_vertex[w2]['D_present']
    return {
        'name': 'removed-D-at-w1-blockwise-uniform',
        'status': 'triggered and holds (negative control after removing selected-w1 D presence)',
        'scope': 'same abstract named C edges; no beta-derived target disk source',
        'graph_name': graph['name'], 'vertex_order': vertices,
        'original_C_edges': graph['original_C_edges'], 'all_list_masks': masks,
        'block_palette_masks': palettes, 'all_original_vertex_data': at_vertex,
        'shared_r': {'incident_cycle_palettes': [palettes['J1'], palettes['J2']], 'disjoint': True, 'union': 15},
        'failed_target_premise': {'vertex': w1, 'is_noncut_noncontact': True, 'D_present': False,
                                  'reason': 'D unused on beta and no original s edge would force D present; that premise is deliberately removed here'},
        'complete_coloring_fibre': tuples, 'direct_backtracking_nodes': nodes,
        'uncolorable': True,
    }


def reconstructed_M(graph):
    """Literal edge calibration of unused-D/list semantics, never a disk source."""
    C = graph['vertex_order']
    ce = [tuple(e) for e in graph['original_C_edges']]
    contacts = graph['s_contacts_from_original_edges']
    B = ['B' + str(i) for i in range(5)]
    beta = dict(zip(B, [0, 1, 0, 1, 2]))
    frame = [edge(B[i], B[(i + 1) % 5]) for i in range(5)]
    attachments = {}
    for v in C:
        slots = 4 - graph['degree_C'][v] - int(v in contacts)
        assert 0 <= slots <= 2
        attachments[v] = ['B0', 'B1'][:slots]
    sb = ['B0', 'B1', 'B4']
    medges = sorted(set(ce + frame + [edge(v, b) for v in C for b in attachments[v]] + [edge('s', p) for p in contacts] + [edge('s', b) for b in sb]))
    vertices = sorted(C + B + ['s'])
    madj = adjacent(vertices, medges)
    assert len(madj['r']) == 4 and len(madj['s']) == 5
    assert all(len(madj[v]) == 4 for v in C if v != 'r')
    assert all(beta[a] != beta[b] for a, b in frame)
    queries = []
    for sc in range(4):
        masks = []
        for v in C:
            banned = {beta[b] for b in madj[v] if b in beta}
            if 's' in madj[v]:
                banned.add(sc)
            masks.append(sum(1 << c for c in range(4) if c not in banned))
        tuples, nodes = solve(C, ce, masks, all_solutions=True)
        for tup in tuples:
            validate_full_tuple(C, ce, masks, tup)
        queries.append({'s_color': sc, 'all_derived_list_masks': masks,
                        'complete_C_coloring_fibre': tuples,
                        'fibre_count': len(tuples), 'backtracking_nodes': nodes,
                        's_to_B_spokes_imposed': False})
    dquery = queries[D]
    assert all(m.bit_count() >= graph['degree_C'][v] for v, m in zip(C, dquery['all_derived_list_masks']))
    assert all(dquery['all_derived_list_masks'][C.index(w)] & 8 for w in graph['selected_w'].values())
    full_tuples = []
    for sc in range(4):
        if any(sc == beta[b] for b in sb):
            continue
        for tup in queries[sc]['complete_C_coloring_fibre']:
            coloring = dict(zip(C, tup)) | beta | {'s': sc}
            full = [coloring[v] for v in vertices]
            validate_full_tuple(vertices, medges, [1 << coloring[v] for v in vertices], full)
            full_tuples.append(full)
    full_tuples.sort()
    assert full_tuples
    witness = dict(zip(vertices, full_tuples[0]))
    per_point = {}
    for v in C:
        mask = dquery['all_derived_list_masks'][C.index(v)]
        per_point[v] = {
            'all_original_M_neighbors': sorted(madj[v]),
            'actual_boundary_neighbors': attachments[v],
            'actual_boundary_neighbor_colors': [beta[b] for b in attachments[v]],
            'original_s_edge_present': 's' in madj[v],
            'degree_M': len(madj[v]), 'degree_C': graph['degree_C'][v],
            'derived_L_D_mask': mask, 'derived_L_D_size': mask.bit_count(),
            'D_present': bool(mask & 8),
        }
    return {
        'name': graph['name'] + '-synthetic-M-original-edge-calibration',
        'status': 'triggered and holds (original-edge/list/reconstructed-full-lift calibration)',
        'target_source_status': 'not triggered',
        'scope': {
            'finite_simple_graph': True, 'induced_ordered_C5_frame': True,
            'degree_M_r_4_s_5_other_C_4': True,
            's_two_C_contacts_three_original_boundary_spokes': True,
            'specified_C_block_shape': True, 'proper_three_color_beta': True,
            'D_unused_by_beta': True, 'beta_refusal_on_M': False,
            'beta_minimal_core': False, 'disk_embedding': 'not supplied or asserted',
            'Sigma_criticality_ownership_rotation_target_identity': 'not supplied or asserted',
        },
        'C_graph_name': graph['name'], 'M_vertex_order': vertices,
        'all_original_M_edges': medges, 'ordered_frame': B,
        'proper_beta': beta, 'D': D,
        'removed_original_G_spoke_for_X_M_calibration': edge('r', 'B2'),
        'original_G_edges': sorted(medges + [edge('r', 'B2')]),
        'actual_boundary_attachments': attachments, 's_original_B_neighbors': sb,
        's_original_C_neighbors': contacts, 'all_original_M_degrees': {v: len(madj[v]) for v in vertices},
        'all_original_C_vertex_list_derivations_for_s_D': per_point,
        'query_semantics': 'fixed beta on C-B and chosen s color on s-C; do not impose s-B in the four C queries',
        'four_s_queries': queries,
        'complete_full_M_beta_lift_fibre': full_tuples,
        'full_M_beta_lift_count': len(full_tuples),
        'reconstructed_full_M_edge_witness': {
            'full_assignment_in_M_vertex_order': full_tuples[0],
            'all_original_edge_color_pairs': [[a, b, witness[a], witness[b]] for a, b in medges],
        },
    }


def build_certificate():
    specs = [
        ('C-333-arms-00', (3, 3, 3), (0, 0), 'exhaustive', None),
        ('C-533-arms-00', (5, 3, 3), (0, 0), 'sampled', 96),
        ('C-333-arms-11', (3, 3, 3), (1, 1), 'sampled', 96),
    ]
    fixtures = []
    for spec in specs:
        graph, options, ranks = make_graph(*spec)
        graph['list_assignments_with_complete_witnesses'] = list_records(graph, options, ranks)
        graph['same_original_M_edge_calibration'] = reconstructed_M(graph)
        fixtures.append(graph)
    total = sum(g['list_assignments_with_complete_witnesses']['summary']['enumerated_assignments'] for g in fixtures)
    return {
        'schema': SCHEMA, 'colors_in_literal_order': COLORS, 'D_color_index': D,
        'independence': 'stdlib only, no old repository solver imports, direct original-edge backtracking',
        'claim_boundary': 'finite list/edge calibration only; arbitrary-size paper proof and actual target source are outside this checker',
        'actual_BR_SD_1a_target_source_status': 'not triggered',
        'fixtures': fixtures, 'removed_D_negative_control': removed_D_negative(fixtures[0]),
        'summary': {'listed_fixture_count': len(fixtures), 'checked_list_assignments': total,
                    'all_enumerated_assignments_colored': True, 'list_assignment_counterexamples': 0,
                    'actual_target_sources': 0},
    }


def serialize(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def inspect_records(data):
    assert data['schema'] == SCHEMA
    for graph in data['fixtures']:
        vertices = graph['vertex_order']
        edges = graph['original_C_edges']
        options = [graph['assignment_scope']['all_vertex_options'][v] for v in vertices]
        spec = graph['assignment_scope']['enumerated_ranks']
        ranks = list(range(spec['start'], spec['stop_exclusive'], spec['step'])) if isinstance(spec, dict) else spec
        records = graph['list_assignments_with_complete_witnesses']['records']
        assert len(ranks) == len(records)
        for rank, row in zip(ranks, records):
            masks, colors = row
            assert masks == masks_at_rank(options, rank), (graph['name'], rank, 'lists')
            validate_full_tuple(vertices, edges, masks, colors)
            for w in graph['selected_w'].values():
                assert masks[vertices.index(w)] & 8


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--certificate', type=Path, required=True)
    args = parser.parse_args()
    if args.check:
        raw = args.certificate.read_bytes()
        existing = json.loads(raw)
        inspect_records(existing)
    expected = build_certificate()
    raw_expected = serialize(expected)
    if args.write:
        with args.certificate.open('xb') as file:
            file.write(raw_expected)
        raw = raw_expected
    else:
        assert raw == raw_expected, 'certificate differs from complete deterministic recomputation'
    digest = hashlib.sha256(raw).hexdigest()
    print(json.dumps({'mode': 'write' if args.write else 'check', 'certificate': str(args.certificate),
                      'sha256': digest, 'bytes': len(raw), **expected['summary']}, sort_keys=True))
    for graph in expected['fixtures']:
        print(json.dumps({'fixture': graph['name'], **graph['list_assignments_with_complete_witnesses']['summary'],
                          'D_full_M_beta_lifts': graph['same_original_M_edge_calibration']['full_M_beta_lift_count'],
                          'four_s_query_fibre_counts': [q['fibre_count'] for q in graph['same_original_M_edge_calibration']['four_s_queries']]}, sort_keys=True))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (AssertionError, ValueError, KeyError, TypeError, IndexError) as error:
        print('FAIL: ' + repr(error), file=sys.stderr)
        raise SystemExit(1)
