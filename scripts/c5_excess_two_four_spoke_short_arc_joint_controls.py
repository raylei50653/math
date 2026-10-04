#!/usr/bin/env python3
"""Literal degree-correct C/U/V controls for original spokes 02/03.

These twelve hand-built graphs verify full six-role relations and constructive
acceptance of 01021. They are not disk realizations or edge-minimal sources.
Mixed C may reject other root pairs; both such obstructions are retained.
"""
from itertools import combinations, product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_excess_two_four_spoke_equal_pair_joint_controls import component, edge
from c5_excess_two_four_spoke_crosscut_joint_controls import crosscut_unary, variant_joint
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses


def short_arc_unary(kind, start, owner, side):
    original = crosscut_unary(kind, start, owner, side)
    # Construct the hand-built component in this one literal original frame.
    # These template maps never normalize a component coloring relation.
    move = [4, 0, 1, 2, 3] if side == 'U' else [3, 2, 1, 0, 4]
    attachments = {z: [move[h] for h in hs]
                   for z, hs in original['actual_attachments'].items()}
    result = component(original['vertices'], set(map(tuple, original['internal_edges'])),
                       attachments, original['ordered_contacts'], [owner])
    result['construction_template_boundary_permutation'] = move
    return result


def target_witness(parts, relations, variants, row):
    c, u, v = parts
    a, b = c['owners']
    ut, uf = min((t, f) for t, f in relations[1].items() if t[0] != 2)
    vt, vf = min(relations[2].items())
    bc = min({1, 3} - {vt[0]})
    ct, cf = min((t, f) for t, f in relations[0].items() if t[0] != 2 and t[1] != bc)
    original = variants[0]
    f = dict(enumerate(row)) | {a: 2, b: bc}
    for part, local in zip(parts, (cf, uf, vf), strict=True):
        f.update(zip(sorted(B | set(part['vertices'])), local, strict=True))
    ports, order = original['port_order'], original['vertex_order']
    t, coloring = tuple(f[z] for z in ports), [f[z] for z in order]
    validate_witness(coloring, order, set(map(tuple, original['actual_edges'])), row, ports, t)
    assert t in {tuple(w['tuple']) for w in original['complete_joint']}
    return dict(literal_boundary=row, original_a_color=2, original_b_color=bc,
        original_C_tuple=ct, original_U_tuple=ut, original_V_tuple=vt,
        original_six_role_tuple=t, original_vertex_order=order,
        complete_original_G_coloring=coloring)


def fixed_graph_controls():
    shapes = [
        ('shared_singleton', [7], set(), {7: [2, 3]}, 7, 7),
        ('distinct_triangle', [7, 8, 9], {edge(z, w) for z, w in combinations((7, 8, 9), 2)},
         {7: [2], 8: [3], 9: [2, 3]}, 7, 8),
    ]
    records, joins, fibers, restorations, swaps, constructed = [], 0, 0, 0, 0, 0
    negative_shared, negative_triangle = None, None
    for shape, kinds, swapped in product(shapes,
            (('singleton', 'singleton'), ('edge', 'singleton'), ('singleton', 'triangle')),
            (False, True)):
        name, cv, ce, ca, x, y = shape
        a, b = (6, 5) if swapped else (5, 6)
        parts = [component(cv, ce, ca, [x, y], [a, b])]
        parts.append(short_arc_unary(kinds[0], max(cv) + 1, a, 'U'))
        parts.append(short_arc_unary(kinds[1], max(parts[1]['vertices']) + 1, b, 'V'))
        for part in parts:
            part['actual_support'] = sorted({h for hs in part['actual_attachments'].values() for h in hs})
            part['original_root_contact_edges'] = [edge(r, z) for r, z in
                zip(part['owners'], part['ordered_contacts'], strict=True)]
        assert [p['actual_support'] for p in parts] == [[2, 3], [0, 1, 2], [0, 3, 4]]
        uc, vc = [p['ordered_contacts'][0] for p in parts[1:]]
        roots, spokes = (a, b), {a: [0, 2], b: [0, 3]}
        interior = {a, b} | set().union(*(set(p['vertices']) for p in parts))
        factor_edges = [FRAME | set(map(tuple, p['edges'])) for p in parts]
        original = set.union(*factor_edges) | {edge(a, b)}
        original |= {e for p in parts for e in p['original_root_contact_edges']}
        original |= {edge(r, h) for r in roots for h in spokes[r]}
        degrees = {z: sum(z in e for e in original) for z in sorted(B | interior)}
        assert all(degrees[z] == (5 if z in roots else 4) for z in interior)
        rows = []
        for ri, row in enumerate(ROWS):
            relations = [witnesses(p['vertices'], es, row, p['ordered_contacts'])
                         for p, es in zip(parts, factor_edges, strict=True)]
            assert all(relations)
            for part, es, relation in zip(parts, factor_edges, relations, strict=True):
                for t, f in relation.items():
                    validate_witness(f, sorted(B | set(part['vertices'])), es,
                                     row, part['ordered_contacts'], t)
            cr = relations[0]
            common_avoidances = []
            for color in sorted(U):
                choices = [(t, f) for t, f in sorted(cr.items()) if color not in t]
                assert choices
                t, f = choices[0]
                common_avoidances.append(dict(common_root_color=color,
                    original_C_tuple=t, complete_original_C_coloring=f))
            guarded = []
            for ac, bc in product(sorted(U), repeat=2):
                choices = [(ct, cf) for ct, cf in sorted(cr.items()) if ct[0] != ac and ct[1] != bc]
                guarded.append(dict(a_color=ac, b_color=bc,
                    original_spoke_and_ab_guards=ac != bc and all(
                        color != row[h] for r, color in ((a, ac), (b, bc)) for h in spokes[r]),
                    complete_guarded_original_C_fiber=[dict(tuple=ct, coloring=cf) for ct, cf in choices]))
            specs = [('G', None, False), ('G-au', edge(a, uc), False),
                     ('G-bv', edge(b, vc), False), ('G-ax', edge(a, x), False),
                     ('G-by', edge(b, y), False), ('G-ab', edge(a, b), False)]
            specs += [(f'G-{role}{h}', edge(r, h), False)
                      for role, r in (('a', a), ('b', b)) for h in spokes[r]]
            specs += [('G-C', None, True)]
            variants = [dict(name=label, **variant_joint(parts, relations, roots, spokes,
                interior, original, row, omitted, omit_c)) for label, omitted, omit_c in specs]
            joined = {tuple(t['tuple']) for t in variants[0]['complete_joint']}
            for variant in variants[1:-1]:
                z, w = variant['omitted_original_edge']
                positions = {p: i for i, p in enumerate(variant['port_order'])}
                lifted = {tuple(t['tuple']) for t in variant['complete_joint']}
                restored = {t for t in lifted if
                    (t[positions[z]] if z in positions else row[z]) !=
                    (t[positions[w]] if w in positions else row[w])}
                assert restored == joined
                restorations += 1
            witness = None
            if ri == 1:
                assert row == (0, 1, 0, 2, 1)
                cp, up = [0, 3, 2, 1], [0, 1, 3, 2]
                assert {tuple(cp[c] for c in t) for t in cr} == set(cr)
                assert {tuple(up[c] for c in t) for t in relations[1]} == set(relations[1])
                witness = target_witness(parts, relations, variants, row)
                constructed += 1
                if name == 'shared_singleton' and negative_shared is None:
                    assert not any(t[0] != 1 and t[1] != 3 for t in cr)
                    negative_shared = dict(control_index=len(records), row_index=ri,
                        literal_boundary=row, original_a_b_colors=[1, 3],
                        ordered_quad_external_colors=[1, 3, row[2], row[3]],
                        complete_original_C_tuples=sorted(cr), guarded_original_C_fiber=[],
                        original_spoke_and_ab_guards_hold=True,
                        scope='Local four-distinct-color C obstruction; no U/V or source claim')
                if name == 'distinct_triangle' and negative_triangle is None:
                    assert not any(t[0] != 2 and t[1] != 0 for t in cr)
                    local_lists = {z: sorted(U - {row[h] for h in parts[0]['actual_attachments'][z]} -
                        ({2} if z == x else set()) - ({0} if z == y else set())) for z in cv}
                    assert all(colors == [1, 3] for colors in local_lists.values())
                    negative_triangle = dict(control_index=len(records), row_index=ri,
                        literal_boundary=row, original_a_b_colors=[2, 0],
                        ordered_quad_external_colors=[2, 0, row[2], row[3]],
                        complete_original_C_tuples=sorted(cr), exact_original_C_lists=local_lists,
                        guarded_original_C_fiber=[], original_quad_guards_hold=True,
                        original_b0_spoke_guard_holds=False,
                        scope='Local swapped-seen-color C obstruction; the original b0 guard excludes this root pair')
            joins += len(variants)
            fibers += sum(len(v['pinned_a_b_fibers']) for v in variants)
            rows.append(dict(row_index=ri, literal_boundary=row,
                original_relations=[dict(component=role,
                    original_vertex_order=sorted(B | set(part['vertices'])),
                    ordered_contacts=part['ordered_contacts'],
                    complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(relation.items())])
                    for role, part, relation in zip(('C', 'U', 'V'), parts, relations, strict=True)],
                original_C_all_common_root_color_avoidances=common_avoidances,
                complete_guarded_C_fibers=guarded, variants=variants,
                constructed_original_01021_witness=witness))
        records.append(dict(control_index=len(records), C_kind=name, unary_kinds=kinds,
            root_swapped=swapped, a=a, b=b, original_root_order=[5, 6],
            original_spoke_supports=[spokes[5], spokes[6]],
            original_edges=sorted(original), original_vertex_order=sorted(B | interior),
            original_complete_degrees=degrees, original_components=dict(zip(('C', 'U', 'V'), parts)),
            shared_original_contact=x == y, named_role_order=['a', 'b', 'x', 'y', 'u', 'v'],
            boundary_cyclic_order=list(range(5)), literal_frame_edges=sorted(FRAME), rows=rows,
            scope='Hand-built complete degree graph; no disk, target Sigma, criticality or realizability claim'))
    for original, partner in zip(records[::2], records[1::2], strict=True):
        for row, swapped_row in zip(original['rows'], partner['rows'], strict=True):
            for variant, swapped_variant in zip(row['variants'], swapped_row['variants'], strict=True):
                assert {tuple(t['tuple']) for t in variant['complete_joint']} == {
                    tuple(t['tuple']) for t in swapped_variant['complete_joint']}
                assert variant['pinned_a_b_fibers'] == swapped_variant['pinned_a_b_fibers']
                swaps += 1
    assert len(records) == 12 and joins == 1320 and fibers == 21120 and restorations == 1080
    assert constructed == 12 and swaps == 660 and negative_shared is not None and negative_triangle is not None
    return dict(records=records, negative_four_distinct_color_C_control=negative_shared,
        negative_swapped_seen_color_C_control=negative_triangle,
        summary=dict(complete_degree_graphs=len(records), independent_whole_graph_joins=joins,
            independent_pinned_a_b_fibers=fibers, exact_original_edge_restorations=restorations,
            root_swap_variant_checks=swaps, complete_original_01021_witnesses=constructed,
            C_all_legal_root_pairs_extension_claimed=False, full_six_role_joint_equality_claimed=False))
