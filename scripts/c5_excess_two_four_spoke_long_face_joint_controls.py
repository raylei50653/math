#!/usr/bin/env python3
"""Literal C/U/V controls for original spokes a:{0,1}, b:{0,4}.

Degree-correct finite graphs audit complete relations, empty pinned fibers,
and conditional witness replacement. All attachments use the long envelope
{1,2,3,4}; this is not a disk realization or source-criticality assertion.
"""
from itertools import product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import search
from c5_excess_two_four_spoke_equal_pair_joint_controls import component, edge, unary
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses


def anchored_support_path(part, endpoint):
    """A shortest literal owner-to-support path through this entire component."""
    owner, = part['owners']
    edges = set(map(tuple, part['internal_edges'])) | set(part['original_root_contact_edges'])
    edges |= {edge(z, endpoint) for z in part['vertices']
              if endpoint in part['actual_attachments'][z]}
    todo, seen = [[owner]], {owner}
    while todo:
        path = todo.pop(0)
        if path[-1] == endpoint:
            assert set(path[1:-1]) <= set(part['vertices'])
            assert all(edge(z, w) in edges for z, w in zip(path, path[1:]))
            return path
        for neighbor in sorted(w if z == path[-1] else z for z, w in edges
                               if path[-1] in (z, w)):
            if neighbor not in seen:
                seen.add(neighbor)
                todo.append([*path, neighbor])
    raise AssertionError('The original connected unary does not reach its actual support')


def long_unary(kind, start, owner, side):
    original = unary(kind, start, owner, side)
    if kind == 'singleton':
        attachments = {start: [1, 2, 3] if side == 'U' else [2, 3, 4]}
    elif kind == 'edge':
        attachments = {start: [1, 2], start + 1: [2, 3, 4]}
    else:
        attachments = {start: [4], start + 1: [1, 2], start + 2: [3, 4]}
    return component(original['vertices'], set(map(tuple, original['internal_edges'])),
                     attachments, original['ordered_contacts'], [owner])


def variant_joint(parts, relations, roots, spokes, interior, original, row,
                  omitted, omit_c):
    """Join witnesses literally; independently search the same whole graph."""
    a, b = roots
    c, u, v = parts
    x, y = c['ordered_contacts']
    uc, vc = u['ordered_contacts'][0], v['ordered_contacts'][0]
    active = set(interior) - (set(c['vertices']) if omit_c else set())
    actual = {e for e in original if e != omitted and
              (not omit_c or not set(e) & set(c['vertices']))}
    ports = [a, b, uc, vc] if omit_c else [a, b, x, y, uc, vc]
    order = sorted(B | active)
    allowed = [U - {row[h] for h in spokes[r] if edge(r, h) != omitted}
               for r in roots]
    joined = {}
    factors = [[((), [])] if omit_c else sorted(relations[0].items()),
               sorted(relations[1].items()), sorted(relations[2].items())]
    for ((ct, cf), ((ut,), uf), ((vt,), vf)), (ac, bc) in product(
            product(*factors), product(*map(sorted, allowed))):
        if ((ac == ut and omitted != edge(a, uc)) or
                (bc == vt and omitted != edge(b, vc)) or
                (ac == bc and omitted != edge(a, b)) or
                (not omit_c and (ac == ct[0] or bc == ct[1]))):
            continue
        f = dict(enumerate(row)) | {a: ac, b: bc}
        for p, coloring in zip(parts, (cf, uf, vf), strict=True):
            if p is c and omit_c:
                continue
            f.update(zip(sorted(B | set(p['vertices'])), coloring, strict=True))
        joined.setdefault(tuple(f[z] for z in ports), [f[z] for z in order])
    direct = list(search(active, actual, dict(enumerate(row))))
    assert set(joined) == {tuple(f[z] for z in ports) for f in direct}
    for t, coloring in joined.items():
        validate_witness(coloring, order, actual, row, ports, t)
    fibers = []
    for ac, bc in product(sorted(U), repeat=2):
        fixed = dict(enumerate(row)) | {a: ac, b: bc}
        found = [f for f in search(active - set(roots), actual, fixed)
                 if all(f[z] != f[w] for z, w in actual)]
        fiber = sorted({tuple(f[z] for z in ports[2:]) for f in found})
        assert fiber == sorted(t[2:] for t in joined if t[:2] == (ac, bc))
        fibers.append(dict(a_color=ac, b_color=bc, full_remaining_port_fiber=fiber))
    return dict(omitted_original_edge=omitted, original_C_omitted=omit_c,
        vertex_order=order, port_order=ports, actual_edges=sorted(actual),
        complete_joint=[dict(tuple=t, coloring=f) for t, f in sorted(joined.items())],
        pinned_a_b_fibers=fibers)


def replacement_audit(part, relation, side, original_variant, omission_variant, row):
    """Forget only this contact role; preserve every other original vertex."""
    root_position, forgotten = side, 4 + side
    keep = [i for i in range(6) if i != forgotten]
    project = lambda t: tuple(t[i] for i in keep)
    original_projection = sorted({project(t['tuple'])
                                  for t in original_variant['complete_joint']})
    omission_projection = sorted({project(t['tuple'])
                                  for t in omission_variant['complete_joint']})
    replacements = []
    if len(relation) >= 2:
        assert original_projection == omission_projection
        order = original_variant['vertex_order']
        ports = original_variant['port_order']
        actual = set(map(tuple, original_variant['actual_edges']))
        part_order = sorted(B | set(part['vertices']))
        for witness in omission_variant['complete_joint']:
            t = witness['tuple']
            replacement_tuple, replacement = min(
                (ct, cf) for ct, cf in relation.items() if ct[0] != t[root_position])
            before = dict(zip(order, witness['coloring'], strict=True))
            after = dict(before)
            local = dict(zip(part_order, replacement, strict=True))
            after.update({z: local[z] for z in part['vertices']})
            assert all(after[z] == before[z] for z in set(order) - set(part['vertices']))
            new_tuple, coloring = tuple(after[z] for z in ports), [after[z] for z in order]
            validate_witness(coloring, order, actual, row, ports, new_tuple)
            assert project(new_tuple) == project(t)
            replacements.append(dict(original_omission_tuple=t,
                original_omission_coloring=witness['coloring'],
                replacement_original_unary_tuple=replacement_tuple,
                replacement_original_unary_vertex_order=part_order,
                replacement_original_unary_coloring=replacement,
                extended_original_G_tuple=new_tuple, extended_original_G_coloring=coloring))
    return dict(original_unary_component='U' if side == 0 else 'V',
        original_owner=part['owners'][0], original_contact=part['ordered_contacts'][0],
        contact_relation_size=len(relation), retained_tuple_positions=keep,
        retained_role_order=[['a', 'b', 'x', 'y', 'u', 'v'][i] for i in keep],
        at_least_two_contact_colors=len(relation) >= 2,
        original_G_projection=original_projection, omission_projection=omission_projection,
        projections_equal=original_projection == omission_projection,
        original_unary_replacement_witnesses=replacements)


def fixed_graph_controls():
    shapes = [
        ('shared_singleton', [7], set(), {7: [2, 3]}, 7, 7),
        ('distinct_edge', [7, 8], {(7, 8)}, {7: [1, 2], 8: [3, 4]}, 7, 8),
        ('distinct_triangle', [7, 8, 9], {(7, 8), (7, 9), (8, 9)},
         {7: [1], 8: [4], 9: [2, 3]}, 7, 8),
    ]
    records, joins, fibers, restorations, swap_checks = [], 0, 0, 0, 0
    projection_checks, replacements, singleton_failures = [0, 0], [0, 0], [0, 0]
    marginal_collision, blocked_restoration = None, None
    for shape, kinds, swapped in product(shapes,
            (('singleton', 'singleton'), ('edge', 'singleton'), ('singleton', 'triangle')),
            (False, True)):
        name, cv, ce, ca, x, y = shape
        a, b = (6, 5) if swapped else (5, 6)
        parts = [component(cv, ce, ca, [x, y], [a, b])]
        parts.append(long_unary(kinds[0], max(cv) + 1, a, 'U'))
        parts.append(long_unary(kinds[1], max(parts[1]['vertices']) + 1, b, 'V'))
        for p in parts:
            p['actual_support'] = sorted({h for hs in p['actual_attachments'].values() for h in hs})
            p['original_root_contact_edges'] = [edge(r, q) for r, q in
                zip(p['owners'], p['ordered_contacts'], strict=True)]
        uc, vc = [p['ordered_contacts'][0] for p in parts[1:]]
        spokes = {a: [0, 1], b: [0, 4]}
        interior = {a, b} | set().union(*(set(p['vertices']) for p in parts))
        factor_edges = [FRAME | set(map(tuple, p['edges'])) for p in parts]
        original = set.union(*factor_edges) | {edge(a, b)}
        original |= {e for p in parts for e in p['original_root_contact_edges']}
        original |= {edge(r, h) for r in (a, b) for h in spokes[r]}
        degrees = {z: sum(z in e for e in original) for z in sorted(B | interior)}
        assert all(degrees[z] == (5 if z in (a, b) else 4) for z in interior)
        up, vp = max(parts[1]['actual_support']), min(parts[2]['actual_support'])
        assert up > vp
        anchored_paths = [anchored_support_path(parts[1], up),
                          anchored_support_path(parts[2], vp)]
        assert not set(anchored_paths[0]) & set(anchored_paths[1])
        assert all(edge(z, w) in original for path in anchored_paths
                   for z, w in zip(path, path[1:]))
        long_face = [a, 1, 2, 3, 4, b]
        assert all(edge(z, w) in original for z, w in
                   zip(long_face, long_face[1:] + long_face[:1]))
        placement_control = dict(hypothetical_original_long_face_cycle=long_face,
            original_U_actual_support=parts[1]['actual_support'],
            original_V_actual_support=parts[2]['actual_support'],
            original_U_owner_to_max_support_path=anchored_paths[0],
            original_V_owner_to_min_support_path=anchored_paths[1],
            alternating_endpoint_cyclic_order=[a, vp, up, b],
            disjoint_original_component_path_interiors=True,
            all_path_edges_original=True,
            scope='Negative hypothetical same-original-long-face placement control; no disk claim')
        rows = []
        for ri, row in enumerate(ROWS):
            relations = [witnesses(p['vertices'], es, row, p['ordered_contacts'])
                         for p, es in zip(parts, factor_edges, strict=True)]
            assert all(relations)
            for p, es, relation in zip(parts, factor_edges, relations, strict=True):
                for t, coloring in relation.items():
                    validate_witness(coloring, sorted(B | set(p['vertices'])), es,
                                     row, p['ordered_contacts'], t)
            specs = [('G', None, False), ('G-au', edge(a, uc), False),
                     ('G-bv', edge(b, vc), False), ('G-ab', edge(a, b), False)]
            specs += [(f'G-{role}{h}', edge(r, h), False)
                      for role, r in (('a', a), ('b', b)) for h in spokes[r]]
            specs.append(('G-C', None, True))
            variants = [dict(name=label, **variant_joint(parts, relations, (a, b),
                spokes, interior, original, row, omitted, omit_c))
                for label, omitted, omit_c in specs]
            joins += len(variants)
            fibers += sum(len(v['pinned_a_b_fibers']) for v in variants)
            audits = [replacement_audit(parts[side + 1], relations[side + 1], side,
                      variants[0], variants[side + 1], row) for side in (0, 1)]
            for side, audit in enumerate(audits):
                projection_checks[side] += audit['at_least_two_contact_colors']
                replacements[side] += len(audit['original_unary_replacement_witnesses'])
                singleton_failures[side] += not audit['projections_equal']
            original_joint = {tuple(t['tuple']) for t in variants[0]['complete_joint']}
            for variant in variants[1:-1]:
                z, w = variant['omitted_original_edge']
                positions = {p: i for i, p in enumerate(variant['port_order'])}
                lifted = {tuple(t['tuple']) for t in variant['complete_joint']}
                restored = {t for t in lifted if
                    (t[positions[z]] if z in positions else row[z]) !=
                    (t[positions[w]] if w in positions else row[w])}
                assert restored == original_joint
                restorations += 1
                if lifted and not original_joint and blocked_restoration is None:
                    blocked_restoration = dict(control_index=len(records), row_index=ri,
                        literal_boundary=row, variant=variant['name'],
                        omitted_original_edge=[z, w], nonempty_omission_joint=sorted(lifted),
                        restored_original_joint=[], vertex_order=variant['vertex_order'],
                        one_omission_coloring=variant['complete_joint'][0]['coloring'])
            cr = relations[0]
            if marginal_collision is None:
                marginal = [{t[i] for t in cr} for i in (0, 1)]
                for ac, bc in product(sorted(U), repeat=2):
                    if (marginal[0] - {ac} and marginal[1] - {bc} and
                            not any(ct[0] != ac and ct[1] != bc for ct in cr)):
                        marginal_collision = dict(control_index=len(records), row_index=ri,
                            literal_boundary=row, original_contact_vertices=[x, y],
                            C_complete_tuples=sorted(cr), literal_a_b_colors=[ac, bc],
                            guarded_C_fiber=[])
                        break
            rows.append(dict(row_index=ri, literal_boundary=row,
                original_relations=[dict(component=label,
                    vertex_order=sorted(B | set(p['vertices'])), actual_edges=sorted(es),
                    ordered_contacts=p['ordered_contacts'],
                    complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(r.items())])
                    for label, p, es, r in zip(('C', 'U', 'V'), parts, factor_edges,
                                              relations, strict=True)],
                variants=variants, conditional_unary_projection_extension_audits=audits))
        records.append(dict(control_index=len(records), C_kind=name, unary_kinds=kinds,
            root_swapped=swapped, a=a, b=b, original_root_order=[5, 6],
            original_spoke_supports=[spokes[5], spokes[6]],
            named_role_order=['a', 'b', 'x', 'y', 'u', 'v'],
            literal_frame_edges=sorted(FRAME), boundary_cyclic_order=list(range(5)),
            original_edges=sorted(original), vertex_order=sorted(B | interior),
            original_degrees=degrees, original_components=dict(zip(('C', 'U', 'V'), parts)),
            negative_same_original_long_face_placement_control=placement_control,
            shared_original_contact=x == y, rows=rows,
            scope='Complete degree graph with long-envelope attachments; no disk, Sigma or criticality claim'))
    for original, swapped in zip(records[::2], records[1::2], strict=True):
        move = lambda z: 11 - z if z in (5, 6) else z
        assert {edge(move(z), move(w)) for z, w in original['original_edges']} == set(
            swapped['original_edges'])
        assert original['original_spoke_supports'] == swapped['original_spoke_supports'][::-1]
        for row, partner in zip(original['rows'], swapped['rows'], strict=True):
            for variant, other in zip(row['variants'], partner['variants'], strict=True):
                assert {edge(move(z), move(w)) for z, w in variant['actual_edges']} == set(
                    other['actual_edges'])
                assert variant['pinned_a_b_fibers'] == other['pinned_a_b_fibers']
                assert {tuple(t['tuple']) for t in variant['complete_joint']} == {
                    tuple(t['tuple']) for t in other['complete_joint']}
                swap_checks += 1
    assert len(records) == 18 and joins == 1620 and fibers == 25920
    assert restorations == 1260 and swap_checks == 810
    assert all(projection_checks) and all(replacements) and all(singleton_failures)
    assert marginal_collision is not None and blocked_restoration is not None
    return dict(records=records, C_marginal_collision_control=marginal_collision,
        blocked_original_edge_restoration_control=blocked_restoration,
        scope=__doc__, summary=dict(complete_original_degree_graphs=len(records),
            literal_boundary_rows_per_graph=len(ROWS), independent_whole_graph_joins=joins,
            independent_pinned_a_b_fibers=fibers, exact_original_edge_restorations=restorations,
            complete_graph_root_swap_variant_checks=swap_checks,
            explicit_anchored_component_path_negative_controls=len(records),
            conditional_unary_projection_row_checks=projection_checks,
            original_unary_replacement_witnesses=replacements,
            singleton_unary_projection_failures=singleton_failures,
            disk_realizability_claimed=False, complete_source_sigma_claimed=False,
            source_criticality_claimed=False))
