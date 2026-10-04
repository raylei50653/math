#!/usr/bin/env python3
"""A4 fixed same-graph mixed-(1,2)+a-unary controls: original spokes 04/04.

These 24 explicit graphs retain degree-five roots, degree-four remaining
interior vertices, complete ordered C ternaries, U relations and six-role joins.
The original rejected row 01202 is audited at BOTH singleton colors 1 and 3:
triangle support124 gives 1, singleton support123 gives 3. The former misses
required source endpoint3; neither family is a 933/941 critical disk source.
Complete exterior projections are compared with ax omitted, and whole-C
replacement witnesses retain all literal exterior colors. Four skeleton disk
rotations, exact lists and connected exterior paths are checked separately;
this finite certificate does not prove disk realization or the arbitrary-size
paper extension. No D5 source exclusion or mask transport is used.
"""
import argparse
from itertools import product
import json

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import search
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses
from c5_excess_two_mixed_core_four_spoke_mixed12 import cycle_key, disk_rotations
from c5_excess_two_four_spoke_mixed12_joint_controls import (
    _c_shapes, _connected, _path, _tuples, edge,
)


DESIGNATED_ROW = (0, 1, 2, 0, 2)


def c_shapes():
    """Translate only six sealed-support controls, preserving original aliases."""
    shapes = [s for s in _c_shapes() if s[0].startswith('sealed_3_')]
    assert len(shapes) == 3
    for h, shape in product((0, 4), shapes):
        label, vertices, internal, attachments, x, y0, y1 = shape
        assert {i for vs in attachments.values() for i in vs} == {3}
        translated = {v: [h for _ in vs] for v, vs in attachments.items()}
        yield (label.replace('sealed_3_', f'sealed_{h}_'), vertices,
               internal, translated, x, y0, y1)


def u_shape(kind, u):
    """Two explicit original U controls for the literal rejected row01202."""
    if kind == 'singleton_support_123':
        return [u], set(), {u: [1, 2, 3]}
    assert kind == 'triangle_support_124'
    vertices = [u, u + 1, u + 2]
    internal = {edge(u, u + 1), edge(u, u + 2), edge(u + 1, u + 2)}
    # A narrow construction translated at graph-edge level from the old
    # triangle support023. Complete source Sigma is not transported or used.
    attachments = {u: [4], u + 1: [1, 4], u + 2: [1, 2]}
    return vertices, internal, attachments


def skeleton_audits(a, b, h, actual_u_support):
    """Keep four original rotations; audit possible same-rotation placements."""
    skeleton = FRAME | {edge(a, b)} | {
        edge(r, i) for r in (a, b) for i in (0, 4)}
    controls = disk_rotations(skeleton)
    assert controls['rotation_assignments_checked'] == 144
    rotations = controls['all_disk_rotations']
    assert len(rotations) == 4
    cface = list(cycle_key([a, b, h]))
    common = sorted([list(cycle_key([a, b, v])) for v in (0, 4)])
    placements = []
    for ri, rotation in enumerate(rotations):
        assert sorted(f for f in rotation['original_disk_faces']
                      if a in f and b in f) == common
        assert cface in rotation['original_disk_faces']
        uf = [f for f in rotation['original_disk_faces'] if a in f
              and set(actual_u_support) <= set(f) & B]
        placements.append(dict(original_rotation_index=ri,
            complete_original_rotation=rotation,
            actual_C_support=[h], original_C_face=cface,
            possible_same_rotation_original_U_faces=uf))
    assert sum(bool(r['possible_same_rotation_original_U_faces'])
               for r in placements) == 2
    return dict(original_root_spokes=dict(a=[0, 4], b=[0, 4]),
        original_skeleton_edges=sorted(skeleton),
        rotation_assignments_checked=144, all_four_rotations=placements,
        full_control_graph_disk_embedding_claimed=False)


def _full_map(order, relation_coloring):
    return dict(zip(order, relation_coloring, strict=True))


def _rotation_signature(record, move=lambda v: v):
    rings = []
    for r in record['rotation']:
        ring = [move(v) for v in r['ring']]
        k = ring.index(min(ring))
        rings.append((move(r['vertex']), tuple(ring[k:] + ring[:k])))
    return tuple(sorted(rings))


def build():
    records, swap_index = [], {}
    counts = dict(independent_whole_graph_joins=0,
                  independent_pinned_a_b_fibers=0,
                  empty_pinned_fibers=0,
                  complete_joint_tuple_witnesses=0,
                  complete_five_role_tuple_witnesses=0,
                  exact_spoke_reattachments=0,
                  exact_ax_reattachments=0,
                  exact_ax_exterior_projection_equalities=0,
                  ax_projection_witness_replacements=0,
                  complete_C_legal_root_pair_extensions=0,
                  exact_au_products_and_reattachments=0,
                  nonempty_domain_singleton_identity_checks=0,
                  designated_row_complete_unary_singletons=0,
                  designated_row_fixed_exterior_C_extensions=0,
                  original_exact_C_degree_list_checks=0,
                  literal_distinct_hub_checks=0,
                  connected_original_exterior_checks=0,
                  original_four_rotation_graph_controls=0)
    marginal_collision, six_role_inequivalence = None, None
    designated_records = []
    ukinds = ('triangle_support_124', 'singleton_support_123')
    shapes = list(c_shapes())
    for shape, ukind, swapped in product(shapes, ukinds, (False, True)):
        ckind, cv, ce, ca, x, y0, y1 = shape
        a, b = (6, 5) if swapped else (5, 6)
        u = max(cv) + 1
        uv, ue, ua = u_shape(ukind, u)
        c_edges = ce | {edge(v, i) for v in cv for i in ca[v]}
        u_edges = ue | {edge(v, i) for v in uv for i in ua[v]}
        a_spokes, b_spokes = {0, 4}, {0, 4}
        original = (FRAME | c_edges | u_edges
                    | {edge(a, b), edge(a, x), edge(a, u),
                       edge(b, y0), edge(b, y1)}
                    | {edge(a, i) for i in a_spokes}
                    | {edge(b, i) for i in b_spokes})
        interior, ports = [a, b, *cv, *uv], [a, b, x, y0, y1, u]
        order, corder, uorder = (sorted(B | set(vs)) for vs in (interior, cv, uv))
        assert y0 != y1 and set(cv).isdisjoint(uv)
        assert _connected(cv, ce) and _connected(uv, ue)
        assert all(sum(v in e for e in original) == (5 if v in (a, b) else 4)
                   for v in interior)
        assert {(r, v) for r in (a, b) for v in cv if edge(r, v) in original} == {
            (a, x), (b, y0), (b, y1)}
        c_support = sorted({i for vs in ca.values() for i in vs})
        u_support = sorted({i for vs in ua.values() for i in vs})
        assert len(c_support) == 1 and c_support[0] in (0, 4)
        h, = c_support
        hubs = [a, b, h]
        hub_edges = {edge(v, w) for v, w in ((a, b), (a, h), (b, h))}
        assert hub_edges <= original
        exterior_vertices = sorted(B | {a, b} | set(uv))
        exterior_edges = {e for e in original if not set(e) & set(cv)}
        assert _connected(exterior_vertices, exterior_edges)
        counts['connected_original_exterior_checks'] += 1
        exterior_paths = [dict(start=v, end=w,
            original_path=_path(v, w, set(exterior_vertices)-{v, w}, exterior_edges))
            for v, w in ((a, b), (a, h), (b, h))]
        rotations = skeleton_audits(a, b, h, u_support)
        counts['original_four_rotation_graph_controls'] += 1
        degree_lists = [dict(vertex=v,
            original_full_neighbors=sorted(w if z == v else z
                for z, w in original if v in (z, w)),
            original_full_degree=sum(v in e for e in original),
            original_component=('root' if v in (a, b) else 'C' if v in cv else 'U'))
            for v in interior]
        rows = []
        for ri, row in enumerate(ROWS):
            cr = witnesses(cv, c_edges, row, [x, y0, y1])
            ur = witnesses(uv, u_edges, row, [u])
            for relation, vorder, es, contacts in (
                    (cr, corder, c_edges, [x, y0, y1]),
                    (ur, uorder, u_edges, [u])):
                for t, f in sorted(relation.items()):
                    validate_witness(f, vorder, es, row, contacts, t)
            variants, joint_maps = [], {}
            omissions = [('original', None), ('a_x', edge(a, x)),
                         ('a_u', edge(a, u))]
            omissions += [(f'a_spoke_{i}', edge(a, i)) for i in sorted(a_spokes)]
            omissions += [(f'b_spoke_{i}', edge(b, i)) for i in sorted(b_spokes)]
            for variant_id, omitted in omissions:
                actual = original if omitted is None else original - {omitted}
                kept_a = sorted(i for i in a_spokes if edge(a, i) in actual)
                kept_b = sorted(i for i in b_spokes if edge(b, i) in actual)
                joined = {}
                for (xc, c0, c1), cf in sorted(cr.items()):
                    for (uc,), uf in sorted(ur.items()):
                        forbidden_a = {row[i] for i in kept_a}
                        if edge(a, x) in actual:
                            forbidden_a.add(xc)
                        if edge(a, u) in actual:
                            forbidden_a.add(uc)
                        for ac in sorted(U - forbidden_a):
                            for bc in sorted(U - {row[i] for i in kept_b} - {ac, c0, c1}):
                                full = (_full_map(corder, cf) | _full_map(uorder, uf)
                                        | {a: ac, b: bc})
                                joined.setdefault((ac, bc, xc, c0, c1, uc),
                                                  [full[v] for v in order])
                direct = search(set(interior), actual, dict(enumerate(row)))
                assert set(joined) == {tuple(f[v] for v in ports) for f in direct}
                counts['independent_whole_graph_joins'] += 1
                for t, f in sorted(joined.items()):
                    validate_witness(f, order, actual, row, ports, t)
                counts['complete_joint_tuple_witnesses'] += len(joined)
                fibers = []
                for ac, bc in product(sorted(U), repeat=2):
                    fixed = dict(enumerate(row)) | {a: ac, b: bc}
                    found = [f for f in search(set(interior) - {a, b}, actual, fixed)
                             if all(f[v] != f[w] for v, w in actual)]
                    fiber = sorted({(f[x], f[y0], f[y1], f[u]) for f in found})
                    assert fiber == sorted(t[2:] for t in joined if t[:2] == (ac, bc))
                    counts['independent_pinned_a_b_fibers'] += 1
                    counts['empty_pinned_fibers'] += not fiber
                    fibers.append(dict(a_color=ac, b_color=bc,
                                       complete_x_y0_y1_u_fiber=fiber))
                variants.append(dict(id=variant_id, omitted_original_edge=omitted,
                    actual_edges=sorted(actual), vertex_order=order,
                    complete_port_order=ports, retained_a_spokes=kept_a,
                    retained_b_spokes=kept_b, complete_joint_tuples=_tuples(joined),
                    pinned_a_b_fibers=fibers))
                joint_maps[variant_id] = joined
            restored = set(joint_maps['original'])
            for variant in variants[3:7]:
                endpoint, owner = variant['omitted_original_edge']
                position = 0 if owner == a else 1
                joint = joint_maps[variant['id']]
                assert {t for t in joint if t[position] != row[endpoint]} == restored
                variant['exact_reattachment'] = dict(root_tuple_position=position,
                    boundary_endpoint=endpoint, literal_forbidden_color=row[endpoint],
                    restored_joint_equals_guarded_omission_joint=True,
                    removed_joint_tuples=_tuples({t: f for t, f in joint.items()
                                                 if t[position] == row[endpoint]}))
                counts['exact_spoke_reattachments'] += 1
            ax = joint_maps['a_x']
            assert {t for t in ax if t[0] != t[2]} == restored
            positions = (0, 1, 5)
            original_projection = {tuple(t[i] for i in positions) for t in restored}
            omitted_projection = {tuple(t[i] for i in positions) for t in ax}
            assert original_projection == omitted_projection
            counts['exact_ax_exterior_projection_equalities'] += 1
            replacements = []
            for t, f in sorted(ax.items()):
                exterior = tuple(t[i] for i in positions)
                rt = min(t0 for t0 in restored
                         if tuple(t0[i] for i in positions) == exterior)
                rf = joint_maps['original'][rt]
                original_map = _full_map(order, rf)
                omitted_map = _full_map(order, f)
                # Literally preserve the omitted graph's whole U witness,
                # boundary and roots, replacing only the original C coloring.
                replacement_map = omitted_map | {v: original_map[v] for v in cv}
                replacement = [replacement_map[v] for v in order]
                validate_witness(replacement, order, original, row, ports, rt)
                assert all(replacement_map[v] == omitted_map[v]
                           for v in order if v not in cv)
                replacements.append(dict(omitted_six_role_tuple=t,
                    omitted_full_coloring=f, restored_six_role_tuple=rt,
                    restored_full_coloring=replacement,
                    original_C_vertices_only_recolored=cv))
                counts['ax_projection_witness_replacements'] += 1
            allowed_roots = sorted(U - {row[0], row[4]})
            complete_C_extensions = []
            for ac, bc in product(allowed_roots, repeat=2):
                if ac == bc:
                    continue
                fiber = {t: f for t, f in cr.items()
                         if t[0] != ac and bc not in t[1:]}
                assert fiber
                assert len({ac, bc, row[c_support[0]]}) == 3
                counts['literal_distinct_hub_checks'] += 1
                fixed_hub_colors = {a: ac, b: bc, h: row[h]}
                local_lists = []
                for v in cv:
                    internal_neighbors = sorted(w if z == v else z
                        for z, w in ce if v in (z, w))
                    external_neighbors = sorted(w if z == v else z
                        for z, w in original if v in (z, w)
                        and (w if z == v else z) not in cv)
                    assert set(external_neighbors) <= set(hubs)
                    assert len(internal_neighbors)+len(external_neighbors) == 4
                    forbidden = sorted({fixed_hub_colors[w]
                        for w in external_neighbors})
                    allowed = sorted(U-set(forbidden))
                    assert len(forbidden) == len(external_neighbors)
                    assert len(allowed) == len(internal_neighbors)
                    local_lists.append(dict(original_vertex=v,
                        original_internal_C_neighbors=internal_neighbors,
                        original_external_neighbors=external_neighbors,
                        literal_forbidden_colors=forbidden,
                        exact_C_list=allowed,
                        internal_C_degree=len(internal_neighbors),
                        exact_list_is_degree_assignment=True))
                    counts['original_exact_C_degree_list_checks'] += 1
                complete_C_extensions.append(dict(a_color=ac, b_color=bc,
                    complete_C_fixed_root_fiber=_tuples(fiber),
                    three_distinct_original_hub_colors=[ac, bc, row[c_support[0]]],
                    complete_original_C_exact_degree_lists=local_lists))
                counts['complete_C_legal_root_pair_extensions'] += 1
            variants[1]['exact_reattachment'] = dict(root_and_contact_tuple_positions=[0, 2],
                restored_joint_equals_guarded_omission_joint=True,
                complete_a_b_u_projection_equal=True,
                complete_original_a_b_u_projection=sorted(original_projection),
                complete_ax_omitted_a_b_u_projection=sorted(omitted_projection),
                whole_C_witness_replacements_preserving_exterior=replacements,
                complete_C_legal_root_pair_extensions=complete_C_extensions,
                complete_six_role_equality_claimed=False)
            counts['exact_ax_reattachments'] += 1
            if six_role_inequivalence is None and set(ax) - restored:
                t = min(set(ax) - restored)
                replacement, = [r for r in replacements
                                if r['omitted_six_role_tuple'] == t]
                six_role_inequivalence = dict(control_index=len(records), row_index=ri,
                    literal_boundary=row,
                    original_complete_joint=_tuples(joint_maps['original']),
                    ax_omitted_complete_joint=_tuples(ax),
                    omission_only_tuple=t, omission_only_full_coloring=ax[t],
                    same_literal_exterior_projection=list(t[i] for i in positions),
                    whole_C_replacement_preserving_original_exterior=replacement,
                    exterior_projection_equality_holds=True,
                    complete_joint_equality_claimed=False)
            # Whole-U omission is a separate five-role graph. All remaining
            # original C tuples are kept before taking its a-color projection.
            nv, nports = [a, b, *cv], [a, b, x, y0, y1]
            ne = {e for e in original if not set(e) & set(uv)}
            norder = sorted(B | set(nv))
            nj = {}
            for (xc, c0, c1), cf in sorted(cr.items()):
                for ac in sorted(U - {row[i] for i in a_spokes} - {xc}):
                    for bc in sorted(U - {row[i] for i in b_spokes} - {ac, c0, c1}):
                        full = _full_map(corder, cf) | {a: ac, b: bc}
                        nj.setdefault((ac, bc, xc, c0, c1), [full[v] for v in norder])
            assert set(nj) == {tuple(f[v] for v in nports)
                              for f in search(set(nv), ne, dict(enumerate(row)))}
            counts['independent_whole_graph_joins'] += 1
            counts['complete_five_role_tuple_witnesses'] += len(nj)
            nfibers = []
            for ac, bc in product(sorted(U), repeat=2):
                fixed = dict(enumerate(row)) | {a: ac, b: bc}
                found = [f for f in search(set(cv), ne, fixed)
                         if all(f[v] != f[w] for v, w in ne)]
                fiber = sorted({(f[x], f[y0], f[y1]) for f in found})
                assert fiber == sorted(t[2:] for t in nj if t[:2] == (ac, bc))
                counts['independent_pinned_a_b_fibers'] += 1
                counts['empty_pinned_fibers'] += not fiber
                nfibers.append(dict(a_color=ac, b_color=bc, complete_x_y0_y1_fiber=fiber))
            for t, f in sorted(nj.items()):
                validate_witness(f, norder, ne, row, nports, t)
            adomain, udomain = {t[0] for t in nj}, {t[0] for t in ur}
            assert set(joint_maps['a_u']) == {(*t, uc) for t in nj for (uc,) in ur}
            assert {t for t in joint_maps['a_u'] if t[0] != t[5]} == restored
            variants[2]['exact_reattachment'] = dict(root_and_contact_tuple_positions=[0, 5],
                exact_complete_joint_product_with_G_minus_U=True,
                restored_joint_equals_guarded_omission_joint=True,
                marked_u_full_degree_after_edge_omission=3,
                edge_omission_is_not_asserted_to_be_a_minimal_core=True)
            counts['exact_au_products_and_reattachments'] += 1
            if adomain and udomain:
                assert (not restored) == (adomain == udomain and len(adomain) == 1)
                counts['nonempty_domain_singleton_identity_checks'] += 1
            variants.append(dict(id='whole_U', removed_original_vertices=uv,
                actual_edges=sorted(ne), vertex_order=norder, complete_port_order=nports,
                complete_five_role_joint=_tuples(nj), pinned_a_b_fibers=nfibers,
                all_literal_a_colors_after_complete_join=sorted(adomain),
                complete_original_U_contact_colors=sorted(udomain),
                exact_a_u_omission_joint_is_product=True))
            if marginal_collision is None and cr:
                marginals = [{t[j] for t in cr} for j in range(3)]
                for ac, bc in product(sorted(U), repeat=2):
                    if (marginals[0] - {ac} and marginals[1] - {bc}
                            and marginals[2] - {bc}
                            and not any(t[0] != ac and bc not in t[1:] for t in cr)):
                        marginal_collision = dict(control_index=len(records), row_index=ri,
                            ordered_original_contacts=[x, y0, y1],
                            complete_C_tuples=_tuples(cr), literal_a_b_colors=[ac, bc],
                            independently_nonempty_contact_marginals=True,
                            complete_guarded_ternary_fiber=[],
                            root_spoke_eligibility_is_separate=True)
                        break
            designated = None
            if row == DESIGNATED_ROW:
                singleton_color = 1 if ukind == 'triangle_support_124' else 3
                assert udomain == {singleton_color}
                counts['designated_row_complete_unary_singletons'] += 1
                exterior = (4-singleton_color, singleton_color, singleton_color)
                assert exterior[0] not in {row[i] for i in a_spokes}
                assert exterior[1] not in {row[i] for i in b_spokes}
                assert exterior[0] != exterior[1] and exterior[0] != exterior[2]
                assert len({exterior[0], exterior[1], row[h]}) == 3
                c_tuples = {t: f for t, f in cr.items()
                            if t[0] != exterior[0] and exterior[1] not in t[1:]}
                joined_at_exterior = {t: f for t, f in joint_maps['original'].items()
                                      if (t[0], t[1], t[5]) == exterior}
                assert bool(c_tuples) == bool(joined_at_exterior)
                designated = dict(row_index=ri, literal_boundary=row,
                    fixed_original_exterior=dict(a=exterior[0], b=exterior[1], u=exterior[2]),
                    complete_original_R_U=_tuples(ur),
                    complete_original_C_fixed_root_fiber=_tuples(c_tuples),
                    complete_original_joint_at_fixed_exterior=_tuples(joined_at_exterior),
                    has_complete_C_extension=bool(c_tuples),
                    fixed_C_boundary_hub=c_support[0],
                    three_distinct_auxiliary_hub_colors=[exterior[0], exterior[1], row[c_support[0]]],
                    required_original_source_U_support=[1, 2, 3],
                    actual_U_source_support_compatible={1, 2, 3} <= set(u_support),
                    missing_required_original_U_support=sorted({1, 2, 3}-set(u_support)),
                    scope='Fixed graph computation; topology is a separate paper argument')
                if c_tuples:
                    counts['designated_row_fixed_exterior_C_extensions'] += 1
                else:
                    designated['refused_exact_list_context'] = [dict(vertex=v,
                        original_C_neighbors=sorted(w if z == v else z for z, w in ce if v in (z, w)),
                        literal_allowed_colors=sorted(U - {row[i] for i in ca[v]}
                            - ({exterior[0]} if v == x else set())
                            - ({exterior[1]} if v in (y0, y1) else set()))) for v in cv]
                designated_records.append(dict(control_index=len(records), **designated))
            rows.append(dict(row_index=ri, literal_boundary=row,
                C_complete_tuples=_tuples(cr), U_complete_tuples=_tuples(ur),
                variants=variants, designated_rejected_row_audit=designated))
        c_paths = []
        for owner, contacts in ((a, [x]), (b, [y0, y1])):
            actual = c_edges | {edge(owner, v) for v in contacts}
            c_paths.extend(dict(owner=owner, boundary_endpoint=i,
                original_path=_path(owner, i, cv, actual)) for i in c_support)
        u_paths = [dict(owner=a, boundary_endpoint=i,
            original_path=_path(a, i, uv, u_edges | {edge(a, u)})) for i in u_support]
        masks = [dict(variant_id=v['id'], full_boundary_image=sum(1 << r['row_index']
                    for r in rows if r['variants'][vi].get('complete_joint_tuples',
                        r['variants'][vi].get('complete_five_role_joint'))))
                 for vi, v in enumerate(rows[0]['variants'])]
        record = dict(control_index=len(records), C_kind=ckind, U_kind=ukind,
            root_swapped=swapped, original_a=a, original_b=b,
            vertex_order=order, complete_port_order=ports, original_edges=sorted(original),
            original_root_spokes=dict(a=[0, 4], b=[0, 4]),
            complete_original_interior_degree_list=degree_lists,
            original_skeleton_rotation_controls=rotations,
            original_three_hub_exterior=dict(hubs=hubs,
                original_hub_edges=sorted(hub_edges),
                original_exterior_vertices=exterior_vertices,
                original_exterior_edges=sorted(exterior_edges),
                complete_original_exterior_is_connected=True,
                hub_paths_avoid_original_C=exterior_paths,
                scope='Literal original exterior premise; no minor or disk theorem inferred'),
            C=dict(vertices=cv, vertex_order=corder, original_internal_edges=sorted(ce),
                actual_attachments=ca, actual_support=c_support, ordered_contacts=[x, y0, y1],
                owners=[a, b, b], incidence=[1, 2], y0_y1_distinct=True,
                x_y_alias='y0' if x == y0 else 'y1' if x == y1 else None,
                original_owner_to_attachment_paths=c_paths),
            unary_U=dict(vertices=uv, vertex_order=uorder,
                original_internal_edges=sorted(ue), actual_attachments=ua,
                actual_support=u_support, ordered_contacts=[u], owner=a,
                original_owner_to_attachment_paths=u_paths,
                original_a_to_2_crosscut=_path(a, 2, uv, u_edges | {edge(a, u)}),
                original_a_to_3_crosscut=(None if 3 not in u_support else
                    _path(a, 3, uv, u_edges | {edge(a, u)})),
                required_original_source_support=[1, 2, 3],
                actual_U_source_support_compatible={1, 2, 3} <= set(u_support)),
            rows=rows, independently_computed_control_boundary_images=masks,
            scope='Fixed full-degree relation control; disk, source Sigma and criticality not asserted')
        records.append(record)
        swap_index[(ckind, ukind, swapped)] = record
    swaps = []
    for ckind, ukind in product([s[0] for s in shapes], ukinds):
        left, right = (swap_index[(ckind, ukind, s)] for s in (False, True))
        move = lambda v: 11 - v if v in (5, 6) else v
        assert sorted(edge(move(v), move(w)) for v, w in left['original_edges']) == right['original_edges']
        assert move(left['original_a']) == right['original_a']
        assert move(left['original_b']) == right['original_b']
        assert move(left['unary_U']['owner']) == right['unary_U']['owner']
        assert [move(v) for v in left['C']['owners']] == right['C']['owners']
        assert left['C']['actual_attachments'] == right['C']['actual_attachments']
        assert left['unary_U']['actual_attachments'] == right['unary_U']['actual_attachments']
        lrots = left['original_skeleton_rotation_controls']['all_four_rotations']
        rrots = right['original_skeleton_rotation_controls']['all_four_rotations']
        ri_by_signature = {_rotation_signature(r['complete_original_rotation']): i
                           for i, r in enumerate(rrots)}
        rotation_mapping = [ri_by_signature[_rotation_signature(
            r['complete_original_rotation'], move)] for r in lrots]
        assert sorted(rotation_mapping) == list(range(4))
        for li, lr in enumerate(lrots):
            rr = rrots[rotation_mapping[li]]
            moved_C_face = list(cycle_key([move(v) for v in lr['original_C_face']]))
            moved_U_faces = sorted([list(cycle_key([move(v) for v in face]))
                                   for face in lr['possible_same_rotation_original_U_faces']])
            assert moved_C_face == rr['original_C_face']
            assert moved_U_faces == rr['possible_same_rotation_original_U_faces']
            moved_disk_faces = sorted([list(cycle_key([move(v) for v in face]))
                for face in lr['complete_original_rotation']['original_disk_faces']])
            assert moved_disk_faces == rr['complete_original_rotation']['original_disk_faces']
        for lr, rr in zip(left['rows'], right['rows'], strict=True):
            assert lr['C_complete_tuples'] == rr['C_complete_tuples']
            assert lr['U_complete_tuples'] == rr['U_complete_tuples']
            for lv, rv in zip(lr['variants'], rr['variants'], strict=True):
                assert lv['pinned_a_b_fibers'] == rv['pinned_a_b_fibers']
                key = 'complete_five_role_joint' if lv['id'] == 'whole_U' else 'complete_joint_tuples'
                assert [t['tuple'] for t in lv[key]] == [t['tuple'] for t in rv[key]]
                for lt, rt in zip(lv[key], rv[key], strict=True):
                    lf = _full_map(lv['vertex_order'], lt['coloring'])
                    assert [lf[move(v)] for v in rv['vertex_order']] == rt['coloring']
        swaps.append(dict(original_control_index=left['control_index'],
            exchanged_control_index=right['control_index'], vertex_permutation={5: 6, 6: 5},
            original_to_root_swapped_skeleton_rotation_indices=rotation_mapping,
            original_C_U_attachments_supports_and_roles_preserved=True,
            possible_same_rotation_C_U_placements_preserved=True,
            literal_boundary_and_color_frame_fixed=True,
            complete_relations_joint_fibers_and_witnesses_equal=True))
    assert len(records) == 24 and len(swaps) == 12
    assert counts['independent_whole_graph_joins'] == 1920
    assert counts['independent_pinned_a_b_fibers'] == 30720
    assert counts['exact_ax_exterior_projection_equalities'] == 240
    assert counts['complete_C_legal_root_pair_extensions'] == 480
    assert counts['designated_row_complete_unary_singletons'] == 24
    assert counts['designated_row_fixed_exterior_C_extensions'] == 24
    assert all(sum(r['fixed_original_exterior']['u'] == d
                   for r in designated_records) == 12 for d in (1, 3))
    assert sum(r['actual_U_source_support_compatible']
               for r in designated_records) == 12
    assert counts['connected_original_exterior_checks'] == 24
    assert counts['literal_distinct_hub_checks'] == 480
    assert counts['original_four_rotation_graph_controls'] == 24
    assert marginal_collision is not None and six_role_inequivalence is not None
    masks = [r['independently_computed_control_boundary_images'][0]['full_boundary_image']
             for r in records]
    assert all(sigma not in (933, 941) for sigma in masks)
    assert set(masks) == {1023}
    return dict(schema=1, scope=__doc__, pattern_order=ROWS, records=records,
        designated_row_fixed_exterior_audits=designated_records,
        designated_original_rejected_row=DESIGNATED_ROW,
        original_source_Sigma_claimed=False, D5_source_result_transport_used=False,
        root_swap_controls=swaps, ternary_marginal_collision=marginal_collision,
        six_role_joint_inequivalence=six_role_inequivalence,
        summary=dict(fixed_full_degree_graphs=len(records), root_swap_graph_checks=len(swaps),
            distinct_x_y0_y1_graphs=sum(r['C']['x_y_alias'] is None for r in records),
            x_equals_y0_graphs=sum(r['C']['x_y_alias'] == 'y0' for r in records),
            x_equals_y1_graphs=sum(r['C']['x_y_alias'] == 'y1' for r in records),
            **counts,
            designated_row_literal_U_singleton_color_counts=[dict(color=d,
                graphs=sum(r['fixed_original_exterior']['u'] == d
                           for r in designated_records)) for d in (1, 3)],
            designated_row_full_source_U_support_compatible_graphs=sum(
                r['actual_U_source_support_compatible'] for r in designated_records),
            ternary_marginal_false_join_negative_control=marginal_collision is not None,
            six_role_joint_inequality_negative_control=six_role_inequivalence is not None,
            original_control_boundary_image_counts=[dict(full_boundary_image=s,
                graphs=masks.count(s)) for s in sorted(set(masks))],
            disk_or_source_Sigma_realizations_claimed=False,
            source_graphs_enumerated=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--payload', action='store_true', help='Print full deterministic payload')
    parser.add_argument('--check', action='store_true', help='Recompute all controls without writing files')
    args = parser.parse_args()
    result = build()
    print(json.dumps(result if args.payload else result['summary'], ensure_ascii=False,
                     sort_keys=True, indent=1))


if __name__ == '__main__':
    main()
