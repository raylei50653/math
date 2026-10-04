#!/usr/bin/env python3
"""Narrow literal graph controls for the mixed-(2,2) short face {1,2}.

All seven original contact identities keep one four-role colour frame.  The
complete-degree relation controls and the conditional original-edge K5 minor
controls are hand-built graphs, not disk or target-Sigma source realizations.
Long paths are checked as actual paths of those original graphs; no synthetic
apex or contraction is inserted into a relation calculation.
"""
from itertools import combinations, permutations, product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_excess_two_four_spoke_mixed22_joint_controls import PARTITIONS, joint, solve
from c5_excess_two_mixed_core_spokes import validate_witness


def edge(v, w):
    return tuple(sorted((v, w)))


def cycle_edges(vertices):
    assert len(vertices) >= 3 and len(set(vertices)) == len(vertices)
    return {edge(v, vertices[(i + 1) % len(vertices)])
            for i, v in enumerate(vertices)}


def connected(vertices, edges):
    vertices = set(vertices)
    assert vertices
    reached = {min(vertices)}
    while True:
        grown = reached | {w for v in reached for w in vertices if edge(v, w) in edges}
        if grown == reached:
            return reached == vertices
        reached = grown


def component_data(vertices, contacts, internal, attachments, roots):
    a, b = roots
    vertices = sorted(vertices)
    contacts = list(contacts)
    owners = {v: [r for r, owned in ((a, contacts[:2]), (b, contacts[2:]))
                  if v in owned] for v in vertices}
    es = internal | {edge(v, h) for v, hs in attachments.items() for h in hs}
    return dict(vertices=vertices, ordered_contacts=contacts,
        internal_edges=sorted(internal), actual_attachments=attachments,
        actual_support=sorted({h for hs in attachments.values() for h in hs}),
        actual_original_owners=owners, edges=sorted(es),
        owners_by_ordered_role=[a, a, b, b],
        original_root_contact_edges=sorted({edge(r, v) for v, rs in owners.items() for r in rs}))


def original_graph(component, roots):
    a, b = roots
    spokes = {a: [0, 1], b: [2, 3]}
    es = FRAME | set(map(tuple, component['edges'])) | {edge(a, b)}
    es |= set(map(tuple, component['original_root_contact_edges']))
    es |= {edge(r, h) for r, hs in spokes.items() for h in hs}
    order = sorted(B | set(component['vertices']) | set(roots))
    degrees = {v: sum(v in e for e in es) for v in order}
    assert all(degrees[v] == (5 if v in roots else 4)
               for v in set(component['vertices']) | set(roots))
    return spokes, es, order, degrees


def cycle_component(contacts, roots):
    distinct = sorted(set(contacts))
    vertices = distinct if len(distinct) >= 3 else distinct + [11]
    internal = cycle_edges(vertices)
    a, b = roots
    attachments = {}
    for v in vertices:
        owns_a, owns_b = v in contacts[:2], v in contacts[2:]
        attachments[v] = ([] if owns_a and owns_b else [1] if owns_a else
                          [2] if owns_b else [1, 2])
    return component_data(vertices, contacts, internal, attachments, roots)


def relation_controls():
    records = []
    joins = fibres = restorations = s4_relations = s4_witnesses = 0
    for (name, contacts), swapped in product(PARTITIONS, (False, True)):
        roots = (6, 5) if swapped else (5, 6)
        a, b = roots
        component = cycle_component(contacts, roots)
        spokes, original, order, degrees = original_graph(component, roots)
        cv, ce = component['vertices'], set(map(tuple, component['edges']))
        rows = []
        for ri, row in enumerate(ROWS):
            rc = solve(cv, FRAME | ce, row, contacts)
            specs = [('G', None, False)]
            specs += [(f'G-{role}{h}', edge(r, h), False)
                      for role, r in (('a', a), ('b', b)) for h in spokes[r]]
            specs += [('G-C', None, True)]
            variants = []
            for label, omitted, omit_c in specs:
                item = joint(component, rc, roots, spokes, original, row, omitted, omit_c)
                item['name'] = label
                variants.append(item)
                joins += 1
                fibres += 16
            gt = {tuple(t['tuple']) for t in variants[0]['complete_joint']}
            for variant in variants[1:-1]:
                omitted = variant['omitted_original_edge']
                r = next(v for v in omitted if v in roots)
                h = next(v for v in omitted if v in B)
                pos = roots.index(r)
                restored = {tuple(t['tuple']) for t in variant['complete_joint']
                            if t['tuple'][pos] != row[h]}
                assert restored == gt
                restorations += 1
            transports = []
            for perm in permutations(range(4)):
                moved_row = tuple(perm[c] for c in row)
                moved_rc = solve(cv, FRAME | ce, moved_row, contacts)
                assert set(moved_rc) == {tuple(perm[c] for c in t) for t in rc}
                s4_relations += 1
                for variant in variants:
                    actual = set(map(tuple, variant['actual_edges']))
                    for item in variant['complete_joint']:
                        validate_witness([perm[c] for c in item['coloring']],
                            variant['original_vertex_order'], actual, moved_row,
                            variant['original_port_order'], tuple(perm[c] for c in item['tuple']))
                        s4_witnesses += 1
                transports.append(dict(global_color_permutation=perm,
                    transported_literal_boundary=moved_row,
                    independently_recomputed_complete_C_relation_size=len(moved_rc)))
            rows.append(dict(row_index=ri, literal_boundary=row,
                original_C_vertex_order=sorted(B | set(cv)),
                complete_original_R_C=[dict(tuple=t, coloring=f) for t, f in sorted(rc.items())],
                variants=variants, global_S4_controls=transports))
        records.append(dict(control_index=len(records), identity=name, root_swapped=swapped,
            original_root_order=list(roots), original_spoke_supports=[spokes[a], spokes[b]],
            ordered_original_contacts=list(contacts), original_components=dict(C=component),
            original_edges=sorted(original), original_vertex_order=order,
            original_complete_degrees=degrees, boundary_cyclic_order=sorted(B),
            literal_frame_edges=sorted(FRAME), exact_actual_support_envelope=[1, 2],
            rows=rows,
            scope='Hand-built complete-degree original graph; not disk, critical, target Sigma, or source realization'))
    swaps = 0
    for original, partner in zip(records[::2], records[1::2], strict=True):
        assert original['identity'] == partner['identity']
        for row, other in zip(original['rows'], partner['rows'], strict=True):
            assert [item['tuple'] for item in row['complete_original_R_C']] == [
                item['tuple'] for item in other['complete_original_R_C']]
            for variant, swapped in zip(row['variants'], other['variants'], strict=True):
                assert [item['tuple'] for item in variant['complete_joint']] == [
                    item['tuple'] for item in swapped['complete_joint']]
                assert variant['pinned_a_b_fibres'] == swapped['pinned_a_b_fibres']
                swaps += 1
    assert len(records) == 14 and joins == 840 and fibres == 13440
    assert restorations == 560 and swaps == 420 and s4_relations == 3360
    return records, dict(complete_degree_original_graphs=len(records), contact_identities=7,
        independently_recomputed_original_graph_joins=joins,
        independently_recomputed_pinned_a_b_fibres=fibres,
        exact_original_spoke_restorations=restorations, root_swap_variant_checks=swaps,
        independently_recomputed_global_S4_C_relations=s4_relations,
        global_S4_complete_joint_witness_checks=s4_witnesses)


def owner_palette_controls():
    """Exact lists at private degree-two vertices, using every literal pair."""
    roles = (('none', ()), ('a_only', (0,)), ('b_only', (1,)), ('shared_a_b', (0, 1)))
    records = []
    for ri in (1, 3, 4, 6):
        row = ROWS[ri]
        pairs = [(a, b) for a, b in product(range(4), repeat=2)
                 if a != b and a not in {row[0], row[1]} and b not in {row[2], row[3]}]
        tables = []
        for name, owners in roles:
            hs = [] if len(owners) == 2 else [1] if owners == (0,) else [2] if owners == (1,) else [1, 2]
            exact = []
            for pair in pairs:
                forbidden = [row[h] for h in hs] + [pair[i] for i in owners]
                assert len(forbidden) == len(set(forbidden)) == 2
                palette = sorted(U - set(forbidden))
                assert len(palette) == 2
                exact.append(dict(original_root_colors=pair,
                    actual_external_neighbor_colors=forbidden, exact_private_list=palette))
            tables.append(dict(original_owner_role=name, original_root_owner_positions=owners,
                forced_actual_boundary_attachments=hs, exact_private_lists=exact))
        assert len({tuple(tuple(item['exact_private_list']) for item in table['exact_private_lists'])
                    for table in tables}) == 4
        records.append(dict(row_index=ri, literal_boundary=row, complete_legal_root_pairs=pairs,
            private_owner_tables=tables))
    row = ROWS[1]
    missing = next(c for c in U if c not in row)
    special = ((missing, 1), (2, missing))
    signatures = []
    for name, owners in roles:
        hs = [] if len(owners) == 2 else [1] if owners == (0,) else [2] if owners == (1,) else [1, 2]
        lists = [sorted(U - ({row[h] for h in hs} | {pair[i] for i in owners})) for pair in special]
        signature = [int(missing in palette) for palette in lists]
        signatures.append(dict(original_owner_role=name, exact_private_lists=lists,
            missing_color_membership=signature))
    assert [r['missing_color_membership'] for r in signatures] == [[1, 1], [0, 1], [1, 0], [0, 0]]
    return dict(literal_rejected_row_controls=records,
        owner_separating_row_index=1, owner_separating_literal_row=row,
        original_missing_color=missing, exact_root_pair_order=special,
        four_owner_signatures=signatures)


def two_leaf_component(shared=False):
    roots = (5, 6)
    contacts = (7, 8, 7, 8) if shared else (7, 8, 9, 10)
    internal = cycle_edges([11, 7, 8]) | cycle_edges([12, 9, 10])
    internal |= {edge(v, w) for v, w in zip([11, 13, 14, 12], [13, 14, 12])}
    attachments = {7: [] if shared else [1], 8: [] if shared else [1],
                   9: [1, 2] if shared else [2], 10: [1, 2] if shared else [2],
                   11: [1], 12: [2], 13: [1, 2], 14: [1, 2]}
    component = component_data(range(7, 15), contacts, internal, attachments, roots)
    component['original_block_vertex_sets'] = [[11, 7, 8], [12, 9, 10],
                                             [11, 13], [13, 14], [14, 12]]
    return component


def minor_record(name, owner, component, cycle, bags, hub_pair, paths):
    roots = (5, 6)
    spokes, original, order, degrees = original_graph(component, roots)
    cv = set(component['vertices'])
    assert connected(cv, original)
    assert set(cycle) <= cv and cycle_edges(cycle) <= original and len(cycle) % 2 == 1
    cut, private = cycle[0], cycle[1:]
    remainder = sorted(cv - set(private))
    internal = set(map(tuple, component['internal_edges']))
    assert connected(remainder, internal)
    block_edges = set()
    for block in component['original_block_vertex_sets']:
        assert len(block) == 2 or len(block) % 2 == 1
        block_edges |= {edge(*block)} if len(block) == 2 else cycle_edges(block)
    assert block_edges == internal
    assert all(sum(v in e for e in component['internal_edges']) == 2 for v in private)
    for v in private:
        expected = [] if owner == 'none' else [5] if owner == 'a_only' else [6] if owner == 'b_only' else [5, 6]
        assert component['actual_original_owners'][v] == expected
    flat = [v for bag in bags for v in bag]
    assert len(bags) == 5 and len(flat) == len(set(flat))
    assert set(flat) <= set(order)
    assert set(bags[0]) | set(bags[1]) == set(private)
    assert bags[3:] == [[hub_pair[0]], [hub_pair[1]]] and edge(*hub_pair) in original
    assert all(connected(bag, original) for bag in bags)
    witnesses = []
    for i, j in combinations(range(5), 2):
        actual = next((edge(v, w) for v in sorted(bags[i]) for w in sorted(bags[j])
                       if edge(v, w) in original), None)
        assert actual is not None
        witnesses.append(dict(branch_set_pair=[i, j], original_edge=actual))
    checked_paths = []
    for label, path in paths:
        assert path[0] == cut and not set(path) & set(private)
        assert len(path) == len(set(path)) and len(path) >= 3
        assert all(edge(v, w) in original for v, w in zip(path, path[1:]))
        checked_paths.append(dict(name=label, original_vertex_path=path,
            original_edge_path=[edge(v, w) for v, w in zip(path, path[1:])]))
    identity = next(identity for identity, contacts in PARTITIONS
                    if tuple(component['ordered_contacts']) == contacts)
    return dict(name=name, private_leaf_original_owner=owner,
        original_contact_identity=identity,
        original_root_order=list(roots), original_spoke_supports=[spokes[r] for r in roots],
        ordered_original_contacts=component['ordered_contacts'], original_components=dict(C=component),
        original_edges=sorted(original), original_vertex_order=order,
        original_complete_degrees=degrees, literal_frame_edges=sorted(FRAME),
        original_leaf_odd_cycle=cycle, original_leaf_cutvertex=cut,
        original_leaf_private_vertices=private, original_C_minus_private_vertices=remainder,
        original_C_minus_private_connected=True, original_adjacent_hub_pair=hub_pair,
        actual_original_paths=checked_paths, five_original_connected_branch_sets=bags,
        ten_original_edge_witnesses=witnesses,
        scope='Conditional original marked K5 minor in a hand-built complete-degree graph; no disk, criticality, target Sigma, or source-realizability claim')


def conditional_leaf_minors():
    records = []
    for length in (3, 5, 7):
        component = two_leaf_component()
        private = list(range(20, 20 + length - 1))
        leaf = [13, *private]
        internal = set(map(tuple, component['internal_edges'])) | cycle_edges(leaf)
        attachments = {int(v): list(hs) for v, hs in component['actual_attachments'].items()}
        attachments[13] = []
        attachments.update({v: [1, 2] for v in private})
        blocks = component['original_block_vertex_sets'] + [leaf]
        component = component_data(component['vertices'] + private, component['ordered_contacts'],
                                   internal, attachments, (5, 6))
        component['original_block_vertex_sets'] = blocks
        remainder = sorted(set(component['vertices']) - set(private))
        bags = [[private[0]], private[1:], remainder + [5, 6], [1], [2]]
        records.append(minor_record(f'none-owner-leaf-{length}', 'none', component, leaf, bags,
            [1, 2], [('cut-to-a-and-boundary-1', [13, 11, 7, 5, 1]),
                     ('cut-to-b-and-boundary-2', [13, 14, 12, 9, 6, 2])]))
    component = two_leaf_component()
    for owner, leaf, hub_pair, added, path in (
        ('a_only', [11, 7, 8], [5, 1], [6, 2], [11, 13, 14, 12, 9, 6, 2]),
        ('b_only', [12, 9, 10], [6, 2], [5, 1], [12, 14, 13, 11, 7, 5, 1])):
        private = leaf[1:]
        remainder = sorted(set(component['vertices']) - set(private))
        bags = [[private[0]], [private[1]], remainder + added, [hub_pair[0]], [hub_pair[1]]]
        records.append(minor_record(f'{owner}-triangle-with-original-leaf-chain', owner,
            component, leaf, bags, hub_pair, [('cut-through-C-to-other-root-and-boundary', path)]))
    for identity, contacts in (('Pstraight', (7, 8, 7, 8)), ('Pcross', (7, 8, 8, 7))):
        component = two_leaf_component(shared=True)
        blocks = component['original_block_vertex_sets']
        component = component_data(component['vertices'], contacts,
            set(map(tuple, component['internal_edges'])), component['actual_attachments'], (5, 6))
        component['original_block_vertex_sets'] = blocks
        remainder = sorted(set(component['vertices']) - {7, 8})
        bags = [[7], [8], remainder + sorted(B), [5], [6]]
        records.append(minor_record(f'shared-triangle-{identity}-with-other-none-leaf',
            'shared_a_b', component, [11, 7, 8], bags, [5, 6],
            [('cut-through-C-and-other-leaf-to-boundary', [11, 13, 14, 12, 9, 1])]))
    assert len(records) == 7
    return records


def controls():
    records, summary = relation_controls()
    minors = conditional_leaf_minors()
    summary |= dict(conditional_original_leaf_K5_minors=len(minors),
        independently_checked_original_minor_adjacencies=10 * len(minors),
        independently_checked_actual_external_paths=sum(len(r['actual_original_paths']) for r in minors),
        private_owner_types=4, none_owner_leaf_lengths=[3, 5, 7],
        complete_relation_control_support=[1, 2],
        fixed_controls_are_disk_source_realizations=False,
        target_Sigma_or_criticality_claimed=False)
    return dict(complete_degree_relation_controls=records,
        exact_private_leaf_owner_palette_controls=owner_palette_controls(),
        conditional_original_leaf_K5_minor_controls=minors, summary=summary)


if __name__ == '__main__':
    import json
    print(json.dumps(controls()['summary'], sort_keys=True))
