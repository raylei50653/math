#!/usr/bin/env python3
"""Literal full-degree controls for the 933 04/12 shared-contact {4} branch.

These original graphs retain the shared contact, its actual leaf bridge,
the entire C relation and all four ordered contact roles.  They are interface
and original-minor controls, not disk realizations, Sigma-critical sources,
target-Sigma assertions, or an enumeration of arbitrary-size sources.
"""
from itertools import combinations, permutations, product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_excess_two_four_spoke_mixed22_joint_controls import (
    PARTITIONS, edge, joint, solve,
)
from c5_excess_two_mixed_core_spokes import validate_witness


TARGET_FRAME_ID = 'W933-129'
SHARED_IDENTITIES = tuple((name, contacts) for name, contacts in PARTITIONS
                          if set(contacts[:2]) & set(contacts[2:]))


def path(vertices, edges, start, finish):
    """A deterministic path of literal vertices and original edges."""
    vertices = set(vertices)
    queue, seen = [(start,)], {start}
    while queue:
        p = queue.pop(0)
        if p[-1] == finish:
            assert all(edge(v, w) in edges for v, w in zip(p, p[1:]))
            return list(p)
        for w in sorted(vertices - seen):
            if edge(p[-1], w) in edges:
                seen.add(w)
                queue.append((*p, w))
    raise AssertionError('The asserted original connected bag is disconnected')


def make_component(contacts, designated_v, shape):
    """Build actual degree-four C vertices before choosing a boundary row.

    In the two-shared-vertex positive control both vertices are leaves in C.
    Other controls put all remaining contacts in a connected cycle K.  The
    long cycle is its own original graph, with two original nonowner vertices.
    """
    contact_vertices = sorted(set(contacts))
    shared = set(contacts[:2]) & set(contacts[2:])
    assert designated_v in shared
    rest = [v for v in contact_vertices if v != designated_v]
    owners = {v: int(v in contacts[:2]) + int(v in contacts[2:])
              for v in contact_vertices}
    attachments = {designated_v: [4]}
    subdivisions = []
    if shape == 'minimal_shared_edge':
        assert len(contact_vertices) == 2 and len(shared) == 2
        t = rest[0]
        vertices = contact_vertices
        internal = {edge(designated_v, t)}
        attachments[t] = [4]
        cycle = []
    else:
        assert shape in ('short_K_cycle', 'long_K_cycle')
        t = max(contact_vertices) + 1
        cycle = [t, *rest]
        if len(cycle) == 2:
            cycle.append(t + 1)
        vertices = [designated_v, *cycle]
        internal = {edge(designated_v, t)}
        internal |= {edge(w, cycle[(i + 1) % len(cycle)])
                     for i, w in enumerate(cycle)}
        attachments[t] = [3]
        for w in cycle[1:]:
            if owners.get(w) == 2:
                attachments[w] = []
            elif w in contacts[:2]:
                attachments[w] = [4]
            elif w in contacts[2:]:
                attachments[w] = [2]
            else:
                attachments[w] = [2, 3]
        if shape == 'long_K_cycle':
            p, q = max(vertices) + 1, max(vertices) + 2
            first, second = cycle[:2]
            internal.remove(edge(first, second))
            internal |= {edge(first, p), edge(p, q), edge(q, second)}
            vertices += [p, q]
            attachments[p], attachments[q] = [2, 3], [3, 4]
            cycle = [first, p, q, *cycle[1:]]
            subdivisions.append(dict(removed_template_edge=[first, second],
                original_long_path=[first, p, q, second],
                short_long_relation_equivalence_claimed=False))
    vertices = sorted(vertices)
    internal_degrees = {w: sum(w in e for e in internal) for w in vertices}
    assert internal_degrees[designated_v] == 1
    assert all(internal_degrees[w] + owners.get(w, 0) + len(attachments[w]) == 4
               for w in vertices)
    es = internal | {edge(w, h) for w, hs in attachments.items() for h in hs}
    k = sorted(set(vertices) - {designated_v})
    internal_k = {e for e in internal if set(e) <= set(k)}
    k_paths = [path(k, internal_k, t, w) for w in k]
    assert shared <= set(contacts)
    return dict(vertices=vertices, ordered_contacts=list(contacts),
        internal_edges=sorted(internal), actual_attachments=attachments,
        actual_support=sorted({h for hs in attachments.values() for h in hs}),
        edges=sorted(es), designated_shared_contact=designated_v,
        shared_contacts=sorted(shared), shared_contact_actual_attachment=[4],
        original_shared_leaf_bridge=edge(designated_v, t),
        original_C_degrees=internal_degrees,
        K_vertices=k, original_K_cycle=cycle,
        original_K_connectivity_paths_from_bridge_neighbor=k_paths,
        construction_subdivisions=subdivisions)


def original_minor(component, roots, spokes, original):
    """Five connected original bags and all ten original inter-bag edges."""
    a, b = roots
    v = component['designated_shared_contact']
    bridge = tuple(component['original_shared_leaf_bridge'])
    t = next(w for w in bridge if w != v)
    k = set(component['K_vertices'])
    contacts = component['ordered_contacts']
    ax = next(w for w in contacts[:2] if w != v)
    by = next(w for w in contacts[2:] if w != v)
    assert ax in k and by in k
    n_b = sum(bool(set(e) & B) and bool(set(e) & k) for e in original)
    k_internal = {e for e in original if set(e) <= k}
    k_external = {e for e in original if len(set(e) & k) == 1}
    fixed_external = {edge(a, ax), edge(b, by), bridge}
    assert fixed_external <= k_external
    boundary_external = {e for e in k_external if set(e) & B}
    assert k_external == fixed_external | boundary_external
    assert n_b == len(boundary_external)
    assert 4 * len(k) == 2 * len(k_internal) + 3 + n_b
    assert n_b >= 1 and n_b % 2 == 1
    bk = min(boundary_external)
    bags = {'a': [a], 'b': [b], 'v': [v], 'B': sorted(B), 'K': sorted(k)}
    witnesses = {
        ('a', 'b'): edge(a, b), ('a', 'v'): edge(a, v),
        ('b', 'v'): edge(b, v), ('a', 'B'): edge(a, spokes[a][0]),
        ('b', 'B'): edge(b, spokes[b][0]), ('v', 'B'): edge(v, 4),
        ('v', 'K'): bridge, ('a', 'K'): edge(a, ax),
        ('b', 'K'): edge(b, by), ('B', 'K'): bk,
    }
    assert len(witnesses) == 10
    assert {frozenset(pair) for pair in witnesses} == {
        frozenset(pair) for pair in combinations(bags, 2)}
    for (left, right), e in witnesses.items():
        assert e in original
        assert (e[0] in bags[left] and e[1] in bags[right] or
                e[1] in bags[left] and e[0] in bags[right])
    assert sum(len(bag) for bag in bags.values()) == len(set().union(
        *(set(bag) for bag in bags.values())))
    connectivity = {name: [path(bag, original, min(bag), w) for w in bag]
                    for name, bag in bags.items()}
    bk_endpoint = next(w for w in bk if w in k)
    frame_path = [4, 3, 2, 1, 0]
    assert all(edge(w, z) in FRAME for w, z in zip(frame_path, frame_path[1:]))
    return dict(original_branch_sets=bags,
        original_branch_set_connectivity_paths=connectivity,
        original_B_connectivity_path=frame_path,
        actual_K_paths_from_shared_bridge_neighbor=dict(
            to_remaining_a_contact=path(k, k_internal, t, ax),
            to_remaining_b_contact=path(k, k_internal, t, by),
            to_selected_K_boundary_attachment_endpoint=path(k, k_internal, t, bk_endpoint)),
        original_K5_cross_bag_witnesses=[dict(bags=list(pair), edge=list(e))
                                        for pair, e in witnesses.items()],
        remaining_a_contact=ax, remaining_b_contact=by,
        original_shared_leaf_bridge=list(bridge), bridge_neighbor=t,
        original_K_external_edges=sorted(k_external),
        three_fixed_original_external_edges=sorted(fixed_external),
        original_K_boundary_attachment_edges=sorted(boundary_external),
        parity=dict(K_size=len(k), original_K_internal_edge_count=len(k_internal),
            complete_K_degree_sum=4 * len(k), fixed_external_edge_count=3,
            original_K_boundary_attachment_count=n_b,
            identity_holds=True, boundary_attachment_count_is_odd=True),
        scope='Original K5 minor; no disk realization or source-criticality assertion')


def with_pinned_witnesses(variant):
    """Persist witnesses for every independently checked pinned root fibre."""
    for fibre in variant['pinned_a_b_fibres']:
        ac, bc = fibre['a_color'], fibre['b_color']
        fibre['complete_full_original_pinned_joint'] = [item
            for item in variant['complete_joint'] if item['tuple'][:2] == (ac, bc)]
        assert fibre['complete_C_role_fibre'] == sorted({
            item['tuple'][2:] for item in fibre['complete_full_original_pinned_joint']})
        for item in fibre['complete_full_original_pinned_joint']:
            assert item['tuple'][:2] == (ac, bc)
    return variant


def controls():
    """Return deterministic controls; the parent checker owns artifact writes."""
    records = []
    joins = fibres = swaps = transports = restorations = 0
    relation_tuples = joint_tuples = empty_fibres = 0
    for name, contacts in SHARED_IDENTITIES:
        shared = sorted(set(contacts[:2]) & set(contacts[2:]))
        shapes = ['short_K_cycle', 'long_K_cycle']
        if len(shared) == 2:
            shapes = ['minimal_shared_edge', *shapes]
        for designated_v, shape, swapped in product(shared, shapes, (False, True)):
            roots = (6, 5) if swapped else (5, 6)
            a, b = roots
            spokes = {a: [0, 4], b: [1, 2]}
            component = make_component(contacts, designated_v, shape)
            cv, ce = component['vertices'], set(map(tuple, component['edges']))
            incidence = [edge(a, w) for w in contacts[:2]] + [
                edge(b, w) for w in contacts[2:]]
            component['owners_by_ordered_role'] = [a, a, b, b]
            component['original_root_contact_edges'] = incidence
            original = FRAME | ce | set(incidence) | {edge(a, b)}
            original |= {edge(r, h) for r in roots for h in spokes[r]}
            degrees = {w: sum(w in e for e in original)
                       for w in sorted(B | set(cv) | set(roots))}
            assert all(degrees[w] == (5 if w in roots else 4)
                       for w in set(cv) | set(roots))
            minor = original_minor(component, roots, spokes, original)
            rows = []
            for ri, row in enumerate(ROWS):
                rc = solve(cv, FRAME | ce, row, contacts)
                assert rc
                relation_tuples += len(rc)
                specs = [('G', None, False)]
                specs += [(f'G-{role}{h}', edge(r, h), False)
                    for role, r in (('a', a), ('b', b)) for h in spokes[r]]
                specs += [('G-C', None, True)]
                variants = []
                for label, omitted, omit_c in specs:
                    item = with_pinned_witnesses(joint(component, rc, roots,
                        spokes, original, row, omitted, omit_c))
                    item['name'] = label
                    joins += 1
                    fibres += 16
                    joint_tuples += len(item['complete_joint'])
                    empty_fibres += sum(not f['complete_full_original_pinned_joint']
                                        for f in item['pinned_a_b_fibres'])
                    variants.append(item)
                gtuples = {tuple(item['tuple']) for item in variants[0]['complete_joint']}
                for variant in variants[1:-1]:
                    omitted = variant['omitted_original_edge']
                    r = next(w for w in omitted if w in roots)
                    h = next(w for w in omitted if w in B)
                    position = 0 if r == a else 1
                    restored = {tuple(item['tuple']) for item in variant['complete_joint']
                                if item['tuple'][position] != row[h]}
                    assert restored == gtuples
                    restorations += 1
                color_controls = []
                for perm in permutations(range(4)):
                    moved_row = tuple(perm[c] for c in row)
                    moved_rc = solve(cv, FRAME | ce, moved_row, contacts)
                    assert set(moved_rc) == {tuple(perm[c] for c in t) for t in rc}
                    for variant in variants:
                        es = set(map(tuple, variant['actual_edges']))
                        for item in variant['complete_joint']:
                            validate_witness([perm[c] for c in item['coloring']],
                                variant['original_vertex_order'], es, moved_row,
                                variant['original_port_order'],
                                tuple(perm[c] for c in item['tuple']))
                        transports += 1
                    color_controls.append(dict(global_color_permutation=perm,
                        transported_literal_boundary=moved_row,
                        independently_recomputed_complete_C_relation_size=len(moved_rc)))
                rows.append(dict(row_index=ri, literal_boundary=row,
                    original_C_vertex_order=sorted(B | set(cv)),
                    complete_original_R_C=[dict(tuple=t, coloring=f)
                                            for t, f in sorted(rc.items())],
                    variants=variants, global_S4_color_controls=color_controls))
            records.append(dict(control_index=len(records),
                target_original_frame_id=TARGET_FRAME_ID, target_mask=933,
                identity=name, component_shape=shape,
                designated_shared_contact=designated_v, root_swapped=swapped,
                a=a, b=b, original_root_order=list(roots),
                original_spoke_supports=[spokes[a], spokes[b]],
                ordered_original_contacts=list(contacts),
                original_components=dict(C=component), original_K5_minor=minor,
                original_edges=sorted(original),
                original_vertex_order=sorted(B | set(cv) | set(roots)),
                original_complete_degrees=degrees, boundary_cyclic_order=sorted(B),
                literal_frame_edges=sorted(FRAME), target_long_face_envelope=[2, 3, 4],
                rows=rows,
                scope='Hand-built full-degree original graph; no disk, criticality, target Sigma, or source-realizability claim'))
    for original, partner in zip(records[::2], records[1::2], strict=True):
        assert original['identity'] == partner['identity']
        assert original['component_shape'] == partner['component_shape']
        assert original['designated_shared_contact'] == partner['designated_shared_contact']
        renaming = {5: 6, 6: 5}
        moved_edges = {edge(*(renaming.get(w, w) for w in e))
                       for e in original['original_edges']}
        assert moved_edges == set(map(tuple, partner['original_edges']))
        for row, swapped_row in zip(original['rows'], partner['rows'], strict=True):
            assert row['complete_original_R_C'] == swapped_row['complete_original_R_C']
            for variant, swapped_variant in zip(row['variants'], swapped_row['variants'], strict=True):
                assert [item['tuple'] for item in variant['complete_joint']] == [
                    item['tuple'] for item in swapped_variant['complete_joint']]
                assert [f['complete_C_role_fibre'] for f in variant['pinned_a_b_fibres']] == [
                    f['complete_C_role_fibre'] for f in swapped_variant['pinned_a_b_fibres']]
                swaps += 1
    assert len(records) == 40 and joins == 2400 and fibres == 38400
    assert swaps == 1200 and restorations == 1600 and transports == 57600
    return dict(records=records, summary=dict(
        complete_degree_original_graphs=len(records),
        shared_contact_identity_classes=len(SHARED_IDENTITIES),
        designated_shared_contact_cases=sum(len(set(c[:2]) & set(c[2:]))
                                            for _, c in SHARED_IDENTITIES),
        minimal_two_shared_original_edge_controls=sum(
            r['component_shape'] == 'minimal_shared_edge' for r in records),
        original_K5_minors=len(records), original_K5_cross_bag_edges=10 * len(records),
        original_shared_contact_degree_one_controls=len(records),
        independent_whole_graph_joins=joins,
        independent_pinned_a_b_fibres=fibres, saved_empty_pinned_a_b_fibres=empty_fibres,
        saved_complete_R_C_tuples=relation_tuples, saved_complete_joint_tuples=joint_tuples,
        exact_original_spoke_restorations=restorations,
        root_swap_variant_checks=swaps, global_S4_variant_witness_checks=transports,
        independently_recomputed_S4_C_relations=24 * len(records) * len(ROWS),
        short_long_relation_equivalence_claimed=False,
        fixed_controls_are_disk_source_realizations=False,
        fixed_controls_are_target_Sigma_certificates=False))
