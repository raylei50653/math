#!/usr/bin/env python3
"""Literal six-role controls for the original 01/03 unary-crosscut argument.

Hand-built complete-degree graphs audit full C/U/V relations and whole-C
witness replacement, including a shared original contact. They are not disk
realizations or critical sources. The path contraction belongs to topology;
its internal U colors are never identified in these coloring joins.
"""
from itertools import combinations, product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import search
from c5_excess_two_four_spoke_equal_pair_joint_controls import component, edge
from c5_excess_two_four_spoke_long_face_joint_controls import anchored_support_path
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses


def crosscut_unary(kind, start, owner, side):
    arc = [1, 2, 3] if side == 'U' else [3, 4, 0]
    if kind == 'singleton':
        vertices, internal = [start], set()
        attachments = {start: arc}
    elif kind == 'edge':
        vertices, internal = [start, start + 1], {edge(start, start + 1)}
        attachments = {start: [arc[0], arc[2]], start + 1: arc}
    else:
        assert kind == 'triangle'
        vertices = [start, start + 1, start + 2]
        internal = {edge(z, w) for z, w in combinations(vertices, 2)}
        attachments = {start: [arc[2]], start + 1: arc[:2], start + 2: arc[1:]}
    return component(vertices, internal, attachments, [start], [owner])


def variant_joint(parts, relations, roots, spokes, interior, original, row,
                  omitted, omit_c):
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
    factors = [[((), [])] if omit_c else sorted(relations[0].items()),
               sorted(relations[1].items()), sorted(relations[2].items())]
    joined = {}
    for ((ct, cf), ((ut,), uf), ((vt,), vf)), (ac, bc) in product(
            product(*factors), product(*map(sorted, allowed))):
        if ((ac == ut and omitted != edge(a, uc)) or
                (bc == vt and omitted != edge(b, vc)) or
                (ac == bc and omitted != edge(a, b)) or
                (not omit_c and ((ac == ct[0] and omitted != edge(a, x)) or
                                 (bc == ct[1] and omitted != edge(b, y))))):
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


def replacement_audit(parts, relation, original_variant, variant, row):
    c, u, v = parts
    a, b = c['owners']
    x, y = c['ordered_contacts']
    order = original_variant['vertex_order']
    ports = original_variant['port_order']
    actual = set(map(tuple, original_variant['actual_edges']))
    project = lambda t: (t[0], t[1], t[4], t[5])
    original_projection = sorted({project(t['tuple'])
                                  for t in original_variant['complete_joint']})
    other_projection = sorted({tuple(t['tuple']) if variant['original_C_omitted']
                              else project(t['tuple']) for t in variant['complete_joint']})
    assert original_projection == other_projection
    replacements = []
    part_order = sorted(B | set(c['vertices']))
    for witness in variant['complete_joint']:
        before = dict(zip(variant['vertex_order'], witness['coloring'], strict=True))
        ct, cf = min((ct, cf) for ct, cf in relation.items()
                     if ct[0] != before[a] and ct[1] != before[b])
        after = dict(before)
        local = dict(zip(part_order, cf, strict=True))
        after.update({z: local[z] for z in c['vertices']})
        outside = set(order) - set(c['vertices'])
        assert all(after[z] == before[z] for z in outside)
        t, coloring = tuple(after[z] for z in ports), [after[z] for z in order]
        validate_witness(coloring, order, actual, row, ports, t)
        if x == y:
            assert t[2] == t[3]
        old_projection = tuple(witness['tuple']) if variant['original_C_omitted'] \
            else project(witness['tuple'])
        assert project(t) == old_projection
        replacements.append(dict(original_variant_tuple=witness['tuple'],
            original_variant_vertex_order=variant['vertex_order'],
            original_variant_coloring=witness['coloring'],
            replacement_original_C_tuple=ct, replacement_original_C_vertex_order=part_order,
            replacement_original_C_coloring=cf, extended_original_G_tuple=t,
            extended_original_G_coloring=coloring, all_original_outside_vertices_fixed=True))
    return dict(variant_original_edge=variant['omitted_original_edge'],
        retained_role_order=['a', 'b', 'u', 'v'], original_G_projection=original_projection,
        variant_projection=other_projection, projections_equal=True,
        original_C_replacement_witnesses=replacements)


def fixed_graph_controls():
    rim, center = [7, 8, 9, 10], 11
    wheel = {edge(rim[i], rim[(i + 1) % 4]) for i in range(4)}
    wheel |= {edge(center, z) for z in rim}
    subdivided = {edge(z, w) for z, w in combinations((8, 9, 10, 11), 2)} - {(8, 9)}
    subdivided |= {(7, 8), (7, 9)}
    shapes = [
        ('wheel_adjacent_contacts', [7, 8, 9, 10, 11], wheel,
         {7: [], 8: [], 9: [3], 10: [3], 11: []}, 7, 8),
        ('wheel_opposite_contacts', [7, 8, 9, 10, 11], wheel,
         {7: [], 8: [3], 9: [], 10: [3], 11: []}, 7, 9),
        ('shared_subdivided_K4_contact', [7, 8, 9, 10, 11], subdivided,
         {7: [], 8: [3], 9: [3], 10: [3], 11: [3]}, 7, 7),
    ]
    records, joins, fibers, restorations, swaps, replacements = [], 0, 0, 0, 0, 0
    hub_branches, full_joint_difference = [0, 0], None
    for shape, kinds, swapped in product(shapes,
            (('singleton', 'singleton'), ('edge', 'singleton'), ('singleton', 'triangle')),
            (False, True)):
        name, cv, ce, ca, x, y = shape
        a, b = (6, 5) if swapped else (5, 6)
        parts = [component(cv, ce, ca, [x, y], [a, b])]
        parts.append(crosscut_unary(kinds[0], 12, a, 'U'))
        parts.append(crosscut_unary(kinds[1], max(parts[1]['vertices']) + 1, b, 'V'))
        for p in parts:
            p['actual_support'] = sorted({h for hs in p['actual_attachments'].values() for h in hs})
            p['original_root_contact_edges'] = [edge(r, z) for r, z in
                zip(p['owners'], p['ordered_contacts'], strict=True)]
        uc, vc = [p['ordered_contacts'][0] for p in parts[1:]]
        roots, spokes = (a, b), {a: [0, 1], b: [0, 3]}
        interior = {a, b} | set().union(*(set(p['vertices']) for p in parts))
        factor_edges = [FRAME | set(map(tuple, p['edges'])) for p in parts]
        original = set.union(*factor_edges) | {edge(a, b)}
        original |= {e for p in parts for e in p['original_root_contact_edges']}
        original |= {edge(r, h) for r in roots for h in spokes[r]}
        degrees = {z: sum(z in e for e in original) for z in sorted(B | interior)}
        assert all(degrees[z] == (5 if z in roots else 4) for z in interior)
        path = anchored_support_path(parts[1], 3)
        assert set(path[1:-1]) <= set(parts[1]['vertices'])
        assert not set(path) & set(parts[0]['vertices'])
        rows = []
        for ri, row in enumerate(ROWS):
            relations = [witnesses(p['vertices'], es, row, p['ordered_contacts'])
                         for p, es in zip(parts, factor_edges, strict=True)]
            assert all(relations)
            guarded = []
            for ac, bc in product(sorted(U), repeat=2):
                choices = [(ct, cf) for ct, cf in sorted(relations[0].items())
                           if ct[0] != ac and ct[1] != bc]
                eligible = ac != bc and bc != row[3]
                if eligible:
                    assert choices
                    hub_branches[ac != row[3]] += 1
                guarded.append(dict(a_color=ac, b_color=bc,
                    original_ab_and_b3_guards=eligible,
                    auxiliary_hub_branch=('three_distinct_hubs' if ac != row[3]
                                          else 'two_same_color_merged_hubs'),
                    complete_guarded_original_C_fiber=[dict(tuple=ct, coloring=cf)
                                                      for ct, cf in choices]))
            specs = [('G', None, False), ('G-ax', edge(a, x), False),
                     ('G-by', edge(b, y), False), ('G-C', None, True)]
            variants = [dict(name=label, **variant_joint(parts, relations, roots,
                spokes, interior, original, row, omitted, omit_c))
                for label, omitted, omit_c in specs]
            audits = [replacement_audit(parts, relations[0], variants[0], variant, row)
                      for variant in variants[1:]]
            replacements += sum(len(audit['original_C_replacement_witnesses']) for audit in audits)
            joined = {tuple(t['tuple']) for t in variants[0]['complete_joint']}
            for side, variant in enumerate(variants[1:3]):
                lifted = {tuple(t['tuple']) for t in variant['complete_joint']}
                assert {t for t in lifted if t[side] != t[2 + side]} == joined
                restorations += 1
                if lifted != joined and full_joint_difference is None:
                    full_joint_difference = dict(control_index=len(records), row_index=ri,
                        omitted_original_edge=variant['omitted_original_edge'],
                        original_six_role_joint=sorted(joined), omission_six_role_joint=sorted(lifted),
                        four_role_projections_equal=True)
            joins += len(variants)
            fibers += sum(len(v['pinned_a_b_fibers']) for v in variants)
            rows.append(dict(row_index=ri, literal_boundary=row,
                original_relations=[dict(component=role, vertex_order=sorted(B | set(p['vertices'])),
                    complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(r.items())])
                    for role, p, r in zip(('C', 'U', 'V'), parts, relations, strict=True)],
                complete_guarded_C_fibers=guarded, variants=variants,
                whole_original_C_replacement_audits=audits))
        records.append(dict(control_index=len(records), C_kind=name, unary_kinds=kinds,
            root_swapped=swapped, original_root_order=list(roots),
            original_spoke_supports=[[0, 1], [0, 3]], original_edges=sorted(original),
            original_vertex_degrees=degrees, original_components=dict(zip(('C', 'U', 'V'), parts)),
            shared_original_contact=x == y, original_U_owner_to_actual_b3_path=path,
            original_C_actual_support=[3], rows=rows,
            scope='Complete degree graph and literal relations; no disk/Sigma/criticality assertion'))
    for original, swapped in zip(records[::2], records[1::2], strict=True):
        for row, partner in zip(original['rows'], swapped['rows'], strict=True):
            for variant, other in zip(row['variants'], partner['variants'], strict=True):
                assert {tuple(t['tuple']) for t in variant['complete_joint']} == {
                    tuple(t['tuple']) for t in other['complete_joint']}
                assert variant['pinned_a_b_fibers'] == other['pinned_a_b_fibers']
                swaps += 1
    assert len(records) == 18 and joins == 720 and fibers == 11520
    assert restorations == 360 and swaps == 360 and full_joint_difference is not None
    return dict(records=records, full_six_role_joint_difference_control=full_joint_difference,
        summary=dict(complete_degree_graphs=len(records), independent_whole_graph_joins=joins,
            independent_pinned_a_b_fibers=fibers, exact_mixed_edge_restorations=restorations,
            root_swap_variant_checks=swaps, whole_C_projection_checks=540,
            whole_original_C_replacement_witnesses=replacements,
            eligible_same_color_two_hub_C_fibers=hub_branches[0],
            eligible_distinct_color_three_hub_C_fibers=hub_branches[1],
            full_six_role_joint_equality_claimed=False))
