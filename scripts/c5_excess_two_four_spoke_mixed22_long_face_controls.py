#!/usr/bin/env python3
"""Literal interface and original-path controls for mixed-(2,2) long face.

The face is a-b0-b4-b3-b-a.  All seven original contact identities retain
one four-role colour frame, actual attachments, full witnesses and empty
root-pair fibres.  These hand-built complete-degree graphs check interfaces
and conditional original K5 extraction, not disk/source realizability,
criticality, target Sigma, or equivalence after a contraction.
"""
from itertools import combinations, permutations, product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_excess_two_four_spoke_mixed22_joint_controls import PARTITIONS, joint, solve
from c5_excess_two_mixed_core_spokes import validate_witness


ENVELOPE = (0, 3, 4)
ROLES = (('none', ()), ('a_only', (0,)), ('b_only', (1,)),
         ('shared_a_b', (0, 1)))
ALLOWED = {'none': [(), (0,), (3,), (4,), (0, 4), (3, 4)],
           'a_only': [(), (0,)], 'b_only': [(), (3,)], 'shared_a_b': [()]}
LEAF_TYPES = (('none04', 'none', (), (0, 4)),
              ('none34', 'none', (), (3, 4)),
              ('a0', 'a_only', (0,), (0,)),
              ('b3', 'b_only', (1,), (3,)),
              ('sharedab', 'shared_a_b', (0, 1), ()))


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


def component_data(vertices, contacts, internal, attachments, roots=(5, 6)):
    a, b = roots
    vertices, contacts = sorted(vertices), list(contacts)
    owners = {v: [r for r, owned in ((a, contacts[:2]), (b, contacts[2:]))
                  if v in owned] for v in vertices}
    assert set(attachments) == set(vertices)
    assert all(set(hs) <= set(ENVELOPE) and len(hs) == len(set(hs))
               for hs in attachments.values())
    es = internal | {edge(v, h) for v, hs in attachments.items() for h in hs}
    return dict(vertices=vertices, ordered_contacts=contacts,
        internal_edges=sorted(internal), actual_attachments=attachments,
        actual_support=sorted({h for hs in attachments.values() for h in hs}),
        actual_original_owners=owners, edges=sorted(es),
        owners_by_ordered_role=[a, a, b, b],
        original_root_contact_edges=sorted({edge(r, v) for v, rs in owners.items() for r in rs}))


def original_graph(component, roots=(5, 6)):
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


def legal_root_pairs(row):
    return [(a, b) for a, b in product(range(4), repeat=2)
            if a != b and a not in {row[0], row[1]} and b not in {row[2], row[3]}]


def exact_list(row, pair, owners, attachments):
    neighbors = ([dict(original_neighbor=h, literal_color=row[h]) for h in attachments] +
                 [dict(original_neighbor=5 + j, literal_color=pair[j]) for j in owners])
    colors = [n['literal_color'] for n in neighbors]
    degree = 4 - len(attachments) - len(owners)
    palette = sorted(U - set(colors))
    assert degree >= 1 and len(palette) >= degree
    return dict(original_root_colors=list(pair), actual_external_neighbors=neighbors,
        exact_private_list=palette, required_original_C_degree=degree,
        exact_list_size=len(palette), exact_degree_slack=len(palette) - degree,
        all_actual_external_neighbor_colors_distinct=len(colors) == len(set(colors)))


def owner_palette_controls():
    """Exhaustive same-frame finite audit, including the shared bridge hole."""
    records, subset_checks, pair_checks = [], 0, 0
    for sigma in (933, 941):
        rows = [(i, q) for i, q in enumerate(ROWS) if not sigma >> i & 1]
        tables = []
        for role, owners in ROLES:
            candidates, permitted = [], []
            for n in range(4 - len(owners)):
                for hs in combinations(ENVELOPE, n):
                    audits = []
                    for ri, row in rows:
                        pairs = legal_root_pairs(row)
                        exact = [exact_list(row, pair, owners, hs) for pair in pairs]
                        pair_checks += len(exact)
                        audits.append(dict(row_index=ri, literal_boundary=row,
                            complete_legal_root_pairs=pairs, exact_same_frame_lists=exact))
                    allowed = all(item['exact_degree_slack'] == 0
                                  for audit in audits for item in audit['exact_same_frame_lists'])
                    subset_checks += 1
                    if allowed:
                        permitted.append(hs)
                    failure = next((dict(row_index=audit['row_index'],
                        literal_boundary=audit['literal_boundary'], exact_same_frame_list=item)
                        for audit in audits for item in audit['exact_same_frame_lists']
                        if item['exact_degree_slack']), None)
                    candidates.append(dict(actual_boundary_attachment_subset=hs,
                        permissible_across_all_rejected_rows_and_all_legal_pairs=allowed,
                        all_rejected_row_exact_lists=audits if allowed else [],
                        actual_same_frame_slack_counterexample=failure))
            assert permitted == ALLOWED[role]
            tables.append(dict(original_owner_role=role, original_root_owner_positions=owners,
                permissible_actual_boundary_attachment_subsets=permitted,
                minimum_necessary_original_C_degree=min(4-len(t)-len(owners) for t in permitted),
                all_finite_attachment_subset_audits=candidates))
        records.append(dict(source_sigma=sigma,
            all_rejected_rows=[dict(row_index=i, literal_boundary=q,
                complete_legal_root_pairs=legal_root_pairs(q)) for i, q in rows],
            original_owner_attachment_tables=tables))

    row = ROWS[1]
    assert row == (0, 1, 0, 2, 1)
    missing, = U - set(row)
    assert missing == 3
    special = ((3, 1), (2, 3))
    signatures = []
    for leaf, role, owners, hs in LEAF_TYPES:
        lists = [exact_list(row, pair, owners, hs) for pair in special]
        assert all(item['required_original_C_degree'] == item['exact_list_size'] == 2
                   for item in lists)
        signatures.append(dict(original_leaf_type=leaf, original_owner_role=role,
            original_root_owner_positions=owners, actual_boundary_attachments=hs,
            exact_root_pair_order=special, exact_same_frame_lists=lists,
            missing_color_membership=[int(missing in item['exact_private_list']) for item in lists]))
    assert [r['missing_color_membership'] for r in signatures] == [
        [1, 1], [1, 1], [0, 1], [1, 0], [0, 0]]
    assert len({tuple(tuple(i['exact_private_list']) for i in r['exact_same_frame_lists'])
                for r in signatures}) == 5

    bridge_failures = []
    for sigma, (h, ri, pair) in product((933, 941),
                                      ((0, 6, (2, 0)), (3, 1, (2, 1)), (4, 1, (2, 1)))):
        q = ROWS[ri]
        assert not sigma >> ri & 1 and pair in legal_root_pairs(q)
        item = exact_list(q, pair, (0, 1), (h,))
        assert item['required_original_C_degree'] == 1
        assert item['exact_list_size'] == 2 and item['exact_degree_slack'] == 1
        bridge_failures.append(dict(source_sigma=sigma, original_owner_role='shared_a_b',
            hypothetical_actual_boundary_attachment=[h], rejected_row_index=ri,
            literal_boundary=q, exact_same_frame_list=item,
            impossible_shared_leaf_bridge_reason='Actual degree-one private point has strict list slack'))
    return dict(per_mask_actual_attachment_subset_audits=records,
        all_finite_actual_attachment_subset_checks=subset_checks,
        all_same_frame_row_root_pair_attachment_checks=pair_checks,
        five_degree_two_leaf_palette_signatures=signatures,
        owner_separating_row_index=1, owner_separating_literal_row=row,
        original_missing_color=missing,
        shared_degree_one_actual_attachment_slack_counterexamples=bridge_failures,
        shared_permitted_actual_attachments=[], shared_minimum_necessary_C_degree=2,
        shared_leaf_bridge_possible=False,
        scope='Exact finite list arithmetic on actual attachment candidates; no source existence claim')


def cycle_component(contacts, roots):
    # These are literal interface templates.  The two extra original vertices
    # make the actual support equal to the entire long-face envelope.
    vertices = sorted(set(contacts)) + [11, 12]
    internal = cycle_edges(vertices)
    attachments = {}
    for v in vertices:
        owns_a, owns_b = v in contacts[:2], v in contacts[2:]
        attachments[v] = ([] if owns_a and owns_b else [0] if owns_a else
                          [3] if owns_b else [0, 4] if v == 11 else [3, 4])
    component = component_data(vertices, contacts, internal, attachments, roots)
    assert component['actual_support'] == list(ENVELOPE)
    return component


def add_fibre_witnesses(variant):
    for fibre in variant['pinned_a_b_fibres']:
        pair = (fibre['a_color'], fibre['b_color'])
        entries = [dict(ordered_C_role_tuple=item['tuple'][2:],
            complete_literal_join_tuple=item['tuple'],
            original_complete_coloring_witness=item['coloring'])
            for item in variant['complete_joint'] if tuple(item['tuple'][:2]) == pair]
        assert sorted(tuple(item['ordered_C_role_tuple']) for item in entries) == [
            tuple(t) for t in fibre['complete_C_role_fibre']]
        fibre['complete_C_role_fibre_with_original_witnesses'] = entries
        fibre['empty_fibre'] = not entries


def internal_shared_bridge_component(contacts, roots):
    """Positive degree-two shared bridge vertex; it is not a leaf endpoint."""
    assert contacts == (7, 8, 7, 9)
    chain = [11, 8, 7, 9, 12]
    left, right = [11, 13, 14], [12, 15, 16]
    internal = cycle_edges(left) | cycle_edges(right)
    internal |= {edge(v, w) for v, w in zip(chain, chain[1:])}
    attachments = {7: [], 8: [0], 9: [3], 11: [0], 12: [3],
                   13: [0, 4], 14: [0, 4], 15: [3, 4], 16: [3, 4]}
    component = component_data(set(chain) | set(left) | set(right), contacts,
                               internal, attachments, roots)
    shared_incident = {e for e in internal if 7 in e}
    assert shared_incident == {edge(8, 7), edge(7, 9)}
    assert all(not connected(component['vertices'], internal - {e}) for e in shared_incident)
    component['original_block_vertex_sets'] = [left, right] + [
        [v, w] for v, w in zip(chain, chain[1:])]
    component['actual_original_internal_shared_bridge_chain'] = chain
    component['original_shared_bridge_internal_vertex'] = 7
    component['original_shared_vertex_C_degree'] = 2
    component['original_shared_incident_C_edges_both_bridges'] = sorted(shared_incident)
    component['shared_vertex_is_degree_one_leaf'] = False
    original_graph(component, roots)
    return component


def relation_controls(internal_shared_bridge=False):
    records = []
    joins = fibres = restorations = s4_relations = s4_witnesses = empty_fibres = 0
    templates = (PARTITIONS[1],) if internal_shared_bridge else PARTITIONS
    for (name, contacts), swapped in product(templates, (False, True)):
        roots = (6, 5) if swapped else (5, 6)
        a, b = roots
        component = (internal_shared_bridge_component(contacts, roots) if internal_shared_bridge
                     else cycle_component(contacts, roots))
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
                add_fibre_witnesses(item)
                variants.append(item)
                joins += 1
                fibres += 16
                empty_fibres += sum(f['empty_fibre'] for f in item['pinned_a_b_fibres'])
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
            literal_frame_edges=sorted(FRAME), exact_actual_support_envelope=list(ENVELOPE),
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
                for f, sf in zip(variant['pinned_a_b_fibres'], swapped['pinned_a_b_fibres'], strict=True):
                    assert (f['a_color'], f['b_color'], f['complete_C_role_fibre'], f['empty_fibre']) == (
                        sf['a_color'], sf['b_color'], sf['complete_C_role_fibre'], sf['empty_fibre'])
                swaps += 1
    expected = 2 if internal_shared_bridge else 14
    assert len(records) == expected and joins == expected * 60 and fibres == expected * 960
    assert restorations == expected * 40 and swaps == expected * 30 and s4_relations == expected * 240
    return records, dict(complete_degree_original_graphs=len(records), contact_identities=len(templates),
        independently_recomputed_original_graph_joins=joins,
        independently_recomputed_pinned_a_b_fibres=fibres,
        explicitly_preserved_empty_pinned_a_b_fibres=empty_fibres,
        all_nonempty_fibres_have_original_complete_coloring_witnesses=True,
        exact_original_spoke_restorations=restorations, root_swap_variant_checks=swaps,
        independently_recomputed_global_S4_C_relations=s4_relations,
        global_S4_complete_joint_witness_checks=s4_witnesses)


def two_leaf_component(contacts=(7, 8, 9, 10), bridge_length=3, other_support=(0, 4)):
    shared = set(contacts[:2]) == set(contacts[2:])
    chain = [11, *range(13, 13 + bridge_length - 1), 12]
    internal = cycle_edges([11, 7, 8]) | cycle_edges([12, 9, 10])
    internal |= {edge(v, w) for v, w in zip(chain, chain[1:])}
    attachments = {7: [] if shared else [0], 8: [] if shared else [0],
                   9: list(other_support) if shared else [3],
                   10: list(other_support) if shared else [3], 11: [0], 12: [3]}
    for i, v in enumerate(chain[1:-1]):
        attachments[v] = [0, 4] if i % 2 == 0 else [3, 4]
    vertices = {7, 8, 9, 10} | set(chain)
    component = component_data(vertices, contacts, internal, attachments)
    component['original_block_vertex_sets'] = [[11, 7, 8], [12, 9, 10]] + [
        [v, w] for v, w in zip(chain, chain[1:])]
    component['actual_original_leaf_bridge_chain'] = chain
    original_graph(component)
    return component


def minor_record(name, leaf_type, component, cycle, bags, hub_pair, paths):
    owner = next(role for leaf, role, _, _ in LEAF_TYPES if leaf == leaf_type)
    spokes, original, order, degrees = original_graph(component)
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
    for v in private:
        assert sum(v in e for e in internal) == 2
        expected = [] if owner == 'none' else [5] if owner == 'a_only' else [6] if owner == 'b_only' else [5, 6]
        assert component['actual_original_owners'][v] == expected
        assert sorted(component['actual_attachments'][v] + expected) == sorted(hub_pair)
    flat = [v for bag in bags for v in bag]
    assert len(bags) == 5 and len(flat) == len(set(flat)) and set(flat) <= set(order)
    assert set(bags[0]) | set(bags[1]) == set(private)
    assert bags[3:] == [[hub_pair[0]], [hub_pair[1]]] and edge(*hub_pair) in original
    assert all(connected(bag, original) for bag in bags)
    exterior = sorted((B | {5, 6}) - set(hub_pair))
    exterior_edges = {e for e in original if set(e) <= set(exterior)}
    assert connected(exterior, exterior_edges)
    assert set(bags[2]) == set(remainder) | set(exterior)
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
        assert set(path) <= set(bags[2])
        assert all(edge(v, w) in original for v, w in zip(path, path[1:]))
        checked_paths.append(dict(name=label, original_vertex_path=path,
            original_edge_path=[edge(v, w) for v, w in zip(path, path[1:])]))
    identity = next(identity for identity, contacts in PARTITIONS
                    if tuple(component['ordered_contacts']) == contacts)
    return dict(name=name, private_leaf_type=leaf_type, private_leaf_original_owner=owner,
        original_contact_identity=identity, original_root_order=[5, 6],
        original_spoke_supports=[spokes[r] for r in (5, 6)],
        ordered_original_contacts=component['ordered_contacts'], original_components=dict(C=component),
        original_edges=sorted(original), original_vertex_order=order,
        original_complete_degrees=degrees, literal_frame_edges=sorted(FRAME),
        boundary_cyclic_order=sorted(B), exact_actual_support_envelope=list(ENVELOPE),
        original_leaf_odd_cycle=cycle, original_leaf_cutvertex=cut,
        original_leaf_private_vertices=private, original_C_minus_private_vertices=remainder,
        original_C_minus_private_connected=True, original_adjacent_hub_pair=hub_pair,
        complementary_original_exterior_vertices=exterior,
        all_complementary_original_exterior_edges=sorted(exterior_edges),
        complementary_original_exterior_connected=True,
        actual_original_paths=checked_paths, five_original_connected_branch_sets=bags,
        ten_original_edge_witnesses=witnesses,
        scope='Conditional original marked K5 minor in a hand-built complete-degree graph; no disk, criticality, target Sigma, or source-realizability claim')


def conditional_leaf_minors():
    records = []
    for length, support, bridge_length in product((3, 5, 7), ((0, 4), (3, 4)), (3, 5)):
        component = two_leaf_component(bridge_length=bridge_length)
        chain = component['actual_original_leaf_bridge_chain']
        cut = chain[1]
        private = list(range(20, 20 + length - 1))
        leaf = [cut, *private]
        internal = set(map(tuple, component['internal_edges'])) | cycle_edges(leaf)
        attachments = {int(v): list(hs) for v, hs in component['actual_attachments'].items()}
        attachments[cut] = []
        attachments.update({v: list(support) for v in private})
        blocks = component['original_block_vertex_sets'] + [leaf]
        component = component_data(component['vertices'] + private, component['ordered_contacts'], internal, attachments)
        component['original_block_vertex_sets'] = blocks
        component['actual_original_leaf_bridge_chain'] = chain
        remainder = sorted(set(component['vertices']) - set(private))
        exterior = sorted((B | {5, 6}) - set(support))
        bags = [[private[0]], private[1:], remainder + exterior, [support[0]], [support[1]]]
        a_boundary, b_boundary = (1, 3) if support == (0, 4) else (0, 2)
        leaf_type = 'none04' if support == (0, 4) else 'none34'
        records.append(minor_record(f'{leaf_type}-leaf-{length}-bridge-{bridge_length}',
            leaf_type, component, leaf, bags, list(support),
            [('cut-through-C-to-a-and-actual-boundary', [cut, 11, 7, 5, a_boundary]),
             ('cut-through-C-to-b-and-actual-boundary', [*chain[1:], 9, 6, b_boundary])]))
    for bridge_length in (1, 3, 5):
        component = two_leaf_component(bridge_length=bridge_length)
        chain = component['actual_original_leaf_bridge_chain']
        for leaf_type, leaf, hubs, path in (
            ('a0', [11, 7, 8], [5, 0], [*chain, 9, 6, 3]),
            ('b3', [12, 9, 10], [6, 3], [*reversed(chain), 7, 5, 0])):
            private = leaf[1:]
            remainder = sorted(set(component['vertices']) - set(private))
            exterior = sorted((B | {5, 6}) - set(hubs))
            bags = [[private[0]], [private[1]], remainder + exterior, [hubs[0]], [hubs[1]]]
            records.append(minor_record(f'{leaf_type}-triangle-original-bridge-{bridge_length}',
                leaf_type, component, leaf, bags, hubs,
                [('cut-through-original-bridge-to-other-root-and-boundary', path)]))
    for (identity, contacts), support, bridge_length in product(
            (('Pstraight', (7, 8, 7, 8)), ('Pcross', (7, 8, 8, 7))),
            ((0, 4), (3, 4)), (1, 3, 5)):
        component = two_leaf_component(contacts, bridge_length, support)
        chain = component['actual_original_leaf_bridge_chain']
        remainder = sorted(set(component['vertices']) - {7, 8})
        bags = [[7], [8], remainder + sorted(B), [5], [6]]
        records.append(minor_record(f'sharedab-{identity}-other-none{support[0]}4-bridge-{bridge_length}',
            'sharedab', component, [11, 7, 8], bags, [5, 6],
            [('cut-through-original-bridge-and-other-nonowner-leaf-to-boundary', [*chain, 9, 4])]))
    assert len(records) == 30
    assert {r['private_leaf_type'] for r in records} == {r[0] for r in LEAF_TYPES}
    return records


def controls():
    palettes = owner_palette_controls()
    records, summary = relation_controls()
    shared_bridge_records, shared_bridge_summary = relation_controls(internal_shared_bridge=True)
    minors = conditional_leaf_minors()
    summary |= dict(conditional_original_leaf_K5_minors=len(minors),
        independently_checked_original_minor_adjacencies=10 * len(minors),
        independently_checked_actual_external_paths=sum(len(r['actual_original_paths']) for r in minors),
        private_leaf_types=5, original_owner_types=4, none_owner_leaf_lengths=[3, 5, 7],
        actual_original_leaf_bridge_lengths=[1, 3, 5],
        finite_actual_attachment_subset_checks=palettes['all_finite_actual_attachment_subset_checks'],
        finite_same_frame_row_root_pair_attachment_checks=palettes['all_same_frame_row_root_pair_attachment_checks'],
        shared_degree_one_attachment_slack_counterexamples=len(
            palettes['shared_degree_one_actual_attachment_slack_counterexamples']),
        shared_leaf_bridge_possible=False, internal_degree_two_shared_bridge_chains_retained=True,
        positive_complete_degree_internal_shared_bridge_controls=len(shared_bridge_records),
        internal_shared_bridge_control_summary=shared_bridge_summary,
        complete_relation_control_support=list(ENVELOPE),
        fixed_controls_are_disk_source_realizations=False,
        target_Sigma_or_criticality_claimed=False)
    return dict(complete_degree_relation_controls=records,
        positive_original_internal_shared_bridge_relation_controls=shared_bridge_records,
        exact_private_leaf_owner_palette_controls=palettes,
        conditional_original_leaf_K5_minor_controls=minors, summary=summary)


if __name__ == '__main__':
    import json
    print(json.dumps(controls()['summary'], sort_keys=True))
