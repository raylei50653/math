#!/usr/bin/env python3
"""Fixed same-graph mixed-(1,2)+a-unary controls for spokes 01/23.

Every graph has adjacent full degree-five roots and full degree-four remaining
interior vertices. These are complete relation and omission controls, not disk,
edge-critical, or complete-Sigma 933/941 realizations. Original ternary contacts
remain ordered even when x is the same original vertex as y0 or y1.
"""
import argparse
from itertools import combinations, product
import json

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import search
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses


def edge(a, b):
    return tuple(sorted((a, b)))


def _connected(vertices, edges):
    reached = {min(vertices)}
    while True:
        extended = reached | {w for e in edges for v, w in (e, e[::-1])
                              if v in reached and w in vertices}
        if extended == reached:
            return reached == set(vertices)
        reached = extended


def _path(start, end, interior, edges):
    """A literal original-edge path with every interior vertex in the component."""
    allowed = set(interior) | {start, end}
    queue = [[start]]
    reached = {start}
    for path in queue:
        if path[-1] == end:
            assert len(path) == len(set(path))
            assert all(edge(v, w) in edges for v, w in zip(path, path[1:]))
            assert set(path[1:-1]) <= set(interior)
            return path
        adjacent = sorted({w for e in edges for v, w in (e, e[::-1])
                           if v == path[-1] and w in allowed and w not in reached})
        for w in adjacent:
            reached.add(w)
            queue.append(path + [w])
    raise AssertionError(('missing original attachment path', start, end))


def _c_shapes():
    shapes = [
        ('edge_shared_y0', [7, 8], {(7, 8)}, {7: [1], 8: [2, 3]}, 7, 7, 8),
        ('edge_shared_y1', [7, 8], {(7, 8)}, {7: [1], 8: [2, 3]}, 7, 8, 7),
        ('path_middle', [7, 8, 9], {(7, 8), (8, 9)},
         {7: [0, 1], 8: [4], 9: [2, 3]}, 8, 7, 9),
        ('triangle_distinct', [7, 8, 9], {(7, 8), (7, 9), (8, 9)},
         {7: [1], 8: [4], 9: [2]}, 7, 8, 9),
        ('triangle_shared_y0', [7, 8, 9], {(7, 8), (7, 9), (8, 9)},
         {7: [], 8: [3], 9: [0, 1]}, 7, 7, 8),
        ('triangle_tail', [7, 8, 9, 10], {(7, 8), (7, 9), (8, 9), (7, 10)},
         {7: [4], 8: [1], 9: [3], 10: [0, 2]}, 10, 8, 9),
    ]
    # The dense alias has full degree four using only a singleton boundary
    # support: the shared contact has two literal root edges and no attachment.
    dense_vertices = [7, 8, 9, 10, 11]
    dense = {edge(v, w) for v, w in combinations(dense_vertices, 2)} - {
        (7, 9), (7, 10), (8, 11)}
    for label, attachments in (
            ('sealed_3', {7: [3], 8: [3], 9: [3]}),
            ('short_12', {7: [1], 8: [2], 9: [1]})):
        shapes.append((f'{label}_triangle_distinct', [7, 8, 9],
                       {(7, 8), (7, 9), (8, 9)}, attachments, 7, 8, 9))
        dense_attachments = ({7: [], 8: [], 9: [3], 10: [3], 11: [3]}
                             if label == 'sealed_3' else
                             {7: [], 8: [], 9: [1], 10: [2], 11: [1]})
        for y0, y1, alias in ((7, 8, 'y0'), (8, 7, 'y1')):
            shapes.append((f'{label}_dense_shared_{alias}', dense_vertices,
                           dense, dense_attachments, 7, y0, y1))
    return shapes


def _u_shape(kind, u):
    if kind == 'singleton':
        return [u], set(), {u: [0, 3, 4]}
    if kind == 'edge':
        return [u, u+1], {edge(u, u+1)}, {u: [0, 4], u+1: [0, 3, 4]}
    assert kind == 'triangle_branch'
    return [u, u+1, u+2, u+3], {
        edge(u, u+1), edge(u+1, u+2), edge(u+1, u+3), edge(u+2, u+3)}, {
        u: [0, 4], u+1: [4], u+2: [0, 3], u+3: [3, 4]}


def _tuples(relation):
    return [dict(tuple=t, coloring=f) for t, f in sorted(relation.items())]


def _projection(joint, positions):
    return {tuple(t[i] for i in positions) for t in joint}


def build():
    """Return deterministic complete fixed-graph payload; perform every check."""
    records = []
    counts = dict(independent_whole_graph_joins=0,
                  independent_complete_K_ternary_relations=0,
                  independent_complete_L_binary_relations=0,
                  independent_complete_K_after_U_omission_relations=0,
                  independent_pinned_a_b_fibers=0,
                  independent_unary_omission_five_role_joints=0,
                  independent_unary_edge_omission_products=0,
                  unary_edge_omission_projection_checks=0,
                  original_spoke_reattachment_checks=0,
                  same_color_spoke_equalities=0,
                  sealed_C_projected_replacement_checks=0,
                  complete_joint_tuple_witnesses=0,
                  complete_five_role_tuple_witnesses=0,
                  empty_pinned_fibers=0)
    marginal_collision = None
    blocked_reattachment = None
    six_role_inequivalence = None
    swap_records = {}
    for shape, ukind, swapped in product(
            _c_shapes(), ('singleton', 'edge', 'triangle_branch'), (False, True)):
        ckind, cv, ce, ca, x, y0, y1 = shape
        a, b = (6, 5) if swapped else (5, 6)
        u = max(cv) + 1
        uv, ue, ua = _u_shape(ukind, u)
        c_edges = ce | {edge(v, i) for v in cv for i in ca[v]}
        u_edges = ue | {edge(v, i) for v in uv for i in ua[v]}
        a_spokes, b_spokes = {0, 1}, {2, 3}
        original = (FRAME | c_edges | u_edges
                    | {edge(a, b), edge(a, x), edge(a, u),
                       edge(b, y0), edge(b, y1)}
                    | {edge(a, i) for i in a_spokes}
                    | {edge(b, i) for i in b_spokes})
        interior = [a, b, *cv, *uv]
        order = sorted(B | set(interior))
        ports = [a, b, x, y0, y1, u]
        assert y0 != y1 and set(cv).isdisjoint(uv)
        assert _connected(cv, ce) and _connected(uv, ue)
        assert all(sum(v in e for e in original) == (5 if v in (a, b) else 4)
                   for v in interior)
        assert {(r, v) for r in (a, b) for v in cv if edge(r, v) in original} == {
            (a, x), (b, y0), (b, y1)}
        c_support = sorted({i for v in cv for i in ca[v]})
        u_support = sorted({i for v in uv for i in ua[v]})
        assert u_support == [0, 3, 4]
        rows = []
        for ri, row in enumerate(ROWS):
            cr = witnesses(cv, c_edges, row, [x, y0, y1])
            ur = witnesses(uv, u_edges, row, [u])
            for vs, es, contacts, relation in (
                    (cv, c_edges, [x, y0, y1], cr), (uv, u_edges, [u], ur)):
                for t, f in sorted(relation.items()):
                    validate_witness(f, sorted(B | set(vs)), es, row, contacts, t)
            variants, joint_maps = [], []
            for variant_id, omitted in (
                    ('original', None), ('a_spoke_0', edge(a, 0)),
                    ('a_spoke_1', edge(a, 1)), ('b_spoke_2', edge(b, 2)),
                    ('b_spoke_3', edge(b, 3)), ('a_x', edge(a, x)),
                    ('a_u', edge(a, u))):
                actual = original if omitted is None else original - {omitted}
                kept_a = sorted(i for i in a_spokes if edge(a, i) in actual)
                kept_b = sorted(i for i in b_spokes if edge(b, i) in actual)
                joined = {}
                for (xc, c0, c1), cf in sorted(cr.items()):
                    for (uc,), uf in sorted(ur.items()):
                        aforbidden = {row[i] for i in kept_a}
                        if edge(a, u) in actual:
                            aforbidden.add(uc)
                        if edge(a, x) in actual:
                            aforbidden.add(xc)
                        for ac in sorted(U - aforbidden):
                            for bc in sorted(U - {row[i] for i in kept_b} - {ac, c0, c1}):
                                full = (dict(zip(sorted(B | set(cv)), cf, strict=True))
                                        | dict(zip(sorted(B | set(uv)), uf, strict=True))
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
                    assert fiber == sorted({t[2:] for t in joined if t[:2] == (ac, bc)})
                    counts['independent_pinned_a_b_fibers'] += 1
                    counts['empty_pinned_fibers'] += not fiber
                    fibers.append(dict(a_color=ac, b_color=bc,
                                       complete_x_y0_y1_u_fiber=fiber))
                variant = dict(id=variant_id, omitted_original_edge=omitted,
                    actual_edges=sorted(actual), retained_a_spokes=kept_a,
                    retained_b_spokes=kept_b,
                    full_a_b_degrees=[sum(a in e for e in actual),
                                      sum(b in e for e in actual)],
                    complete_joint_tuples=_tuples(joined), pinned_a_b_fibers=fibers)
                if variant_id == 'a_u':
                    assert sum(u in e for e in actual) == 3
                if variant_id.startswith('a_spoke_'):
                    # M-b has one connected original ternary component. The
                    # marked a has TWO internal neighbors, x and u.
                    kv = [a, *cv, *uv]
                    ke = {e for e in actual if b not in e}
                    kr = {}
                    for (xc, c0, c1), cf in sorted(cr.items()):
                        for (uc,), uf in sorted(ur.items()):
                            for ac in sorted(U - {row[i] for i in kept_a} - {xc, uc}):
                                full = (dict(zip(sorted(B | set(cv)), cf, strict=True))
                                        | dict(zip(sorted(B | set(uv)), uf, strict=True))
                                        | {a: ac})
                                kr.setdefault((ac, c0, c1),
                                              [full[v] for v in sorted(B | set(kv))])
                    assert set(kr) == set(witnesses(kv, ke, row, [a, y0, y1]))
                    assert _connected(kv, ke)
                    assert sum(a in e and set(e) <= set(kv) for e in ke) == 2
                    counts['independent_complete_K_ternary_relations'] += 1
                    for t, f in sorted(kr.items()):
                        validate_witness(f, sorted(B | set(kv)), ke, row, [a, y0, y1], t)
                    variant['original_K'] = dict(name='original C+a+U',
                        vertices=kv, vertex_order=sorted(B | set(kv)),
                        actual_edges=sorted(ke), ordered_contacts=[a, y0, y1],
                        marked_a_degree_in_K=2, marked_a_actual_neighbors=[x, u],
                        complete_ternary_relation=_tuples(kr))
                elif variant_id.startswith('b_spoke_'):
                    # M-a has original C+b as a binary component and U as a
                    # separate singleton-contact unary. L is not a ternary.
                    lv = [b, *cv]
                    le = c_edges | {edge(b, y0), edge(b, y1)} | {
                        edge(b, i) for i in kept_b}
                    lr = {}
                    for (xc, c0, c1), cf in sorted(cr.items()):
                        for bc in sorted(U - {row[i] for i in kept_b} - {c0, c1}):
                            full = dict(zip(sorted(B | set(cv)), cf, strict=True)) | {b: bc}
                            lr.setdefault((xc, bc), [full[v] for v in sorted(B | set(lv))])
                    assert set(lr) == set(witnesses(lv, le, row, [x, b]))
                    assert _connected(lv, le)
                    counts['independent_complete_L_binary_relations'] += 1
                    for t, f in sorted(lr.items()):
                        validate_witness(f, sorted(B | set(lv)), le, row, [x, b], t)
                    variant['original_L'] = dict(name='original C+b',
                        vertices=lv, vertex_order=sorted(B | set(lv)),
                        actual_edges=sorted(le), ordered_contacts=[x, b],
                        complete_binary_relation=_tuples(lr),
                        other_original_component='original U')
                variants.append(variant)
                joint_maps.append(joined)
            restored = set(joint_maps[0])
            for variant, joint in zip(variants[1:5], joint_maps[1:5], strict=True):
                # Boundary IDs precede root IDs in normalized undirected edges.
                endpoint, owner = variant['omitted_original_edge']
                assert endpoint in B and owner in (a, b)
                position = 0 if owner == a else 1
                assert {t for t in joint if t[position] != row[endpoint]} == restored
                counts['original_spoke_reattachment_checks'] += 1
                kept = variant['retained_a_spokes'] if owner == a else variant['retained_b_spokes']
                if any(row[endpoint] == row[i] for i in kept):
                    assert set(joint) == restored
                    counts['same_color_spoke_equalities'] += 1
                variant['exact_reattachment'] = dict(root_tuple_position=position,
                    boundary_endpoint=endpoint, literal_forbidden_color=row[endpoint],
                    restored_joint_equals_guarded_omission_joint=True,
                    removed_joint_tuples=_tuples({t: f for t, f in joint.items()
                                                 if t[position] == row[endpoint]}))
                if joint and not restored and blocked_reattachment is None:
                    blocked_reattachment = dict(control_index=len(records), row_index=ri,
                        omitted_original_edge=variant['omitted_original_edge'],
                        nonempty_omission_joint=_tuples(joint), empty_original_joint=[])
            ax_omitted = joint_maps[5]
            assert {t for t in ax_omitted if t[0] != t[2]} == restored
            variants[5]['exact_reattachment'] = dict(root_and_contact_tuple_positions=[0, 2],
                restored_joint_equals_guarded_omission_joint=True)
            if c_support == [3]:
                assert _projection(joint_maps[0], [0, 1, 5]) == _projection(ax_omitted, [0, 1, 5])
                # Check extension for EVERY legal exterior coloring, including
                # fibres absent from the original full joint before joining C.
                external = {(ac, bc, uc) for (uc,) in ur
                    for ac in U - {row[0], row[1], uc}
                    for bc in U - {row[2], row[3], ac}}
                assert _projection(joint_maps[0], [0, 1, 5]) == external
                counts['sealed_C_projected_replacement_checks'] += 1
                variants[5]['projected_C_replacement'] = dict(
                    retained_tuple_positions=[0, 1, 5],
                    complete_a_b_u_projection=sorted(external),
                    exact_projection_equality=True, full_six_role_equality_claimed=False)
                extra = sorted(set(ax_omitted) - restored)
                if extra and six_role_inequivalence is None:
                    t = extra[0]
                    six_role_inequivalence = dict(control_index=len(records), row_index=ri,
                        complete_original_joint=_tuples(joint_maps[0]),
                        complete_a_x_omission_joint=_tuples(ax_omitted),
                        omitted_only_tuple=t, omitted_only_full_coloring=ax_omitted[t],
                        equal_a_b_u_projection=sorted(external),
                        scope='Projection is equal while literal six-role joints differ')
            # G-U deletes the entire named original unary. G-au retains all
            # its vertices and internal edges, including the degree-three u.
            nv = [a, b, *cv]
            ne = {e for e in original if not set(e) & set(uv)}
            norder, nports = sorted(B | set(nv)), [a, b, x, y0, y1]
            nj = {}
            for (xc, c0, c1), cf in sorted(cr.items()):
                for ac in sorted(U - {row[0], row[1], xc}):
                    for bc in sorted(U - {row[2], row[3], ac, c0, c1}):
                        full = dict(zip(sorted(B | set(cv)), cf, strict=True)) | {a: ac, b: bc}
                        nj.setdefault((ac, bc, xc, c0, c1), [full[v] for v in norder])
            assert set(nj) == {tuple(f[v] for v in nports) for f in
                              search(set(nv), ne, dict(enumerate(row)))}
            counts['independent_whole_graph_joins'] += 1
            counts['independent_unary_omission_five_role_joints'] += 1
            counts['complete_five_role_tuple_witnesses'] += len(nj)
            for t, f in sorted(nj.items()):
                validate_witness(f, norder, ne, row, nports, t)
            assert set(joint_maps[6]) == {(*t, uc) for t in nj for (uc,) in ur}
            assert {t for t in joint_maps[6] if t[0] != t[5]} == restored
            counts['independent_unary_edge_omission_products'] += 1
            if ur:
                assert _projection(joint_maps[6], range(5)) == set(nj)
                counts['unary_edge_omission_projection_checks'] += 1
            nfibers = []
            for ac, bc in product(sorted(U), repeat=2):
                fixed = dict(enumerate(row)) | {a: ac, b: bc}
                found = [f for f in search(set(cv), ne, fixed)
                         if all(f[v] != f[w] for v, w in ne)]
                fiber = sorted({(f[x], f[y0], f[y1]) for f in found})
                assert fiber == sorted({t[2:] for t in nj if t[:2] == (ac, bc)})
                counts['independent_pinned_a_b_fibers'] += 1
                counts['empty_pinned_fibers'] += not fiber
                nfibers.append(dict(a_color=ac, b_color=bc, complete_x_y0_y1_fiber=fiber))
            variants[6]['exact_reattachment'] = dict(root_and_contact_tuple_positions=[0, 5],
                restored_joint_equals_guarded_omission_joint=True,
                exact_complete_joint_product_with_G_minus_U=True,
                projected_five_role_joint_equals_G_minus_U_if_R_U_nonempty=True,
                marked_u_full_degree_after_edge_omission=3,
                unary_edge_omission_is_not_asserted_to_be_a_minimal_core=True)
            unary_omission = dict(id='G_minus_original_U', removed_original_vertices=uv,
                actual_edges=sorted(ne), vertices=nv, vertex_order=norder, complete_port_order=nports,
                full_a_b_degrees=[4, 5], complete_five_role_joint=_tuples(nj),
                pinned_a_b_fibers=nfibers,
                R_U_nonempty=bool(ur), all_literal_a_colors=sorted({t[0] for t in nj}),
                original_U_contact_colors=sorted(t[0] for t in ur),
                exact_a_u_omission_joint_is_product=True)
            k0v = [a, *cv]
            k0e = c_edges | FRAME | {edge(a, x), edge(a, 0), edge(a, 1)}
            k0order = sorted(B | set(k0v))
            k0r = {}
            for (xc, c0, c1), cf in sorted(cr.items()):
                for ac in sorted(U - {row[0], row[1], xc}):
                    full = dict(zip(sorted(B | set(cv)), cf, strict=True)) | {a: ac}
                    k0r.setdefault((ac, c0, c1), [full[v] for v in k0order])
            assert set(k0r) == set(witnesses(k0v, k0e, row, [a, y0, y1]))
            assert _connected(k0v, k0e)
            assert sum(a in e and set(e) <= set(k0v) for e in k0e) == 1
            for t, f in sorted(k0r.items()):
                validate_witness(f, k0order, k0e, row, [a, y0, y1], t)
            counts['independent_complete_K_after_U_omission_relations'] += 1
            unary_omission['original_K_after_b_deletion'] = dict(
                name='original C+a', vertices=k0v, vertex_order=k0order,
                actual_edges=sorted(k0e), ordered_contacts=[a, y0, y1],
                marked_a_degree_in_K=1, marked_a_actual_neighbors=[x],
                retained_a_spokes=[0, 1], complete_ternary_relation=_tuples(k0r))
            adomain = {t[0] for t in nj}
            udomain = {t[0] for t in ur}
            if adomain and udomain and not restored:
                assert adomain == udomain and len(adomain) == 1
                unary_omission['empty_original_join_singleton_identity'] = dict(
                    complete_G_minus_U_a_domain=sorted(adomain),
                    complete_original_R_U=sorted(udomain),
                    forced_literal_singleton=next(iter(adomain)))
            if marginal_collision is None and cr:
                marginals = [{t[j] for t in cr} for j in range(3)]
                for ac, bc in product(sorted(U), repeat=2):
                    if (marginals[0] - {ac} and marginals[1] - {bc}
                            and marginals[2] - {bc}
                            and not any(t[0] != ac and bc not in t[1:] for t in cr)):
                        marginal_collision = dict(control_index=len(records), row_index=ri,
                            original_ordered_contacts=[x, y0, y1],
                            complete_C_tuples=_tuples(cr), literal_a_b_colors=[ac, bc],
                            complete_guarded_ternary_fiber=[],
                            scope='Original C relation; root-spoke eligibility is separate')
                        break
            rows.append(dict(row_index=ri, literal_boundary=row,
                C_complete_tuples=_tuples(cr), U_complete_tuples=_tuples(ur), variants=variants,
                original_unary_omission=unary_omission))
        c_attachment_paths = []
        for owner, contacts in ((a, [x]), (b, [y0, y1])):
            actual = c_edges | {edge(owner, v) for v in contacts}
            c_attachment_paths.extend(dict(owner=owner, boundary_endpoint=i,
                original_path=_path(owner, i, cv, actual)) for i in c_support)
        u_attachment_paths = [dict(owner=a, boundary_endpoint=i,
            original_path=_path(a, i, uv, u_edges | {edge(a, u)})) for i in u_support]
        control_masks = [dict(variant_id=variant_id,
            full_boundary_image=sum(1 << row['row_index'] for row in rows
                                    if row['variants'][vi]['complete_joint_tuples']))
            for vi, variant_id in enumerate(v['id'] for v in rows[0]['variants'])]
        record = dict(control_index=len(records), C_kind=ckind, U_kind=ukind,
            root_swapped=swapped, original_a=a, original_b=b, vertex_order=order,
            complete_port_order=ports, original_edges=sorted(original),
            original_root_spokes=dict(a=[0, 1], b=[2, 3]),
            C=dict(vertices=cv, vertex_order=sorted(B | set(cv)),
                original_internal_edges=sorted(ce), actual_attachments=ca,
                actual_support=c_support, ordered_contacts=[x, y0, y1],
                original_owner_to_attachment_paths=c_attachment_paths,
                owners=[a, b, b], incidence=[1, 2], y0_y1_distinct=True,
                x_y_alias='y0' if x == y0 else 'y1' if x == y1 else None),
            unary_U=dict(vertices=uv, vertex_order=sorted(B | set(uv)),
                original_internal_edges=sorted(ue), actual_attachments=ua,
                actual_support=u_support, ordered_contacts=[u], owner=a,
                original_owner_to_attachment_paths=u_attachment_paths,
                original_0_to_3_crosscut=_path(0, 3, uv, u_edges)), rows=rows,
            independently_computed_control_boundary_images=control_masks,
            scope='Fixed full-degree relation control; disk/Sigma/criticality not asserted')
        records.append(record)
        swap_records[(ckind, ukind, swapped)] = record
    root_swaps = []
    for ckind, ukind in product([shape[0] for shape in _c_shapes()],
                               ('singleton', 'edge', 'triangle_branch')):
        left, right = (swap_records[(ckind, ukind, s)] for s in (False, True))
        move = lambda v: 11-v if v in (5, 6) else v
        assert sorted(edge(move(v), move(w)) for v, w in left['original_edges']) == right['original_edges']
        for lrow, rrow in zip(left['rows'], right['rows'], strict=True):
            assert lrow['C_complete_tuples'] == rrow['C_complete_tuples']
            assert lrow['U_complete_tuples'] == rrow['U_complete_tuples']
            for lv, rv in zip(lrow['variants'], rrow['variants'], strict=True):
                assert lv['pinned_a_b_fibers'] == rv['pinned_a_b_fibers']
                assert [t['tuple'] for t in lv['complete_joint_tuples']] == [
                    t['tuple'] for t in rv['complete_joint_tuples']]
                for lt, rt in zip(lv['complete_joint_tuples'], rv['complete_joint_tuples'], strict=True):
                    lf = dict(zip(left['vertex_order'], lt['coloring'], strict=True))
                    assert [lf[move(v)] for v in right['vertex_order']] == rt['coloring']
            ln, rn = lrow['original_unary_omission'], rrow['original_unary_omission']
            assert ln['pinned_a_b_fibers'] == rn['pinned_a_b_fibers']
            for lt, rt in zip(ln['complete_five_role_joint'], rn['complete_five_role_joint'], strict=True):
                assert lt['tuple'] == rt['tuple']
                lf = dict(zip(ln['vertex_order'], lt['coloring'], strict=True))
                assert [lf[move(v)] for v in rn['vertex_order']] == rt['coloring']
        root_swaps.append(dict(original_control_index=left['control_index'],
                              exchanged_control_index=right['control_index'],
                              vertex_permutation={5: 6, 6: 5}, complete_joint_and_witnesses_equal=True))
    assert len(records) == 72 and len(root_swaps) == 36
    assert counts['independent_whole_graph_joins'] == 5760
    assert counts['independent_pinned_a_b_fibers'] == 92160
    assert counts['independent_complete_K_ternary_relations'] == 1440
    assert counts['independent_complete_L_binary_relations'] == 1440
    assert counts['independent_complete_K_after_U_omission_relations'] == 720
    assert counts['same_color_spoke_equalities'] == 0  # 01 and 23 are original C5 edges.
    assert marginal_collision is not None and six_role_inequivalence is not None
    masks = [r['independently_computed_control_boundary_images'][0]['full_boundary_image']
             for r in records]
    assert all(sigma not in (933, 941) for sigma in masks)
    domains = [set(c) for size in range(1, 5) for c in combinations(sorted(U), size)]
    singleton_guards = []
    for adomain, udomain in product(domains, repeat=2):
        guarded = sorted((ac, uc) for ac in adomain for uc in udomain if ac != uc)
        assert (not guarded) == (adomain == udomain and len(adomain) == 1)
        singleton_guards.append(dict(complete_a_domain=sorted(adomain),
            complete_R_U=sorted(udomain), complete_guarded_pair_relation=guarded,
            empty_iff_equal_singletons=True))
    return dict(schema=1, scope=__doc__, pattern_order=ROWS, records=records,
        root_swap_controls=root_swaps, ternary_marginal_collision=marginal_collision,
        nonempty_omission_empty_original_joint=blocked_reattachment,
        six_role_joint_inequivalence=six_role_inequivalence,
        complete_domain_singleton_guard_controls=singleton_guards,
        summary=dict(fixed_full_degree_graphs=len(records), root_swap_graph_checks=len(root_swaps),
            full_nonempty_domain_singleton_guard_checks=len(singleton_guards),
            distinct_x_y0_y1_graphs=sum(r['C']['x_y_alias'] is None for r in records),
            x_equals_y0_graphs=sum(r['C']['x_y_alias'] == 'y0' for r in records),
            x_equals_y1_graphs=sum(r['C']['x_y_alias'] == 'y1' for r in records), **counts,
            original_control_boundary_image_counts=[dict(full_boundary_image=sigma,
                graphs=masks.count(sigma)) for sigma in sorted(set(masks))],
            disk_or_source_Sigma_realizations_claimed=False))


def fixed_graph_controls():
    """Compatibility entry point for the enclosing named-source checker."""
    return build()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--payload', action='store_true', help='Print the complete deterministic payload')
    parser.add_argument('--check', action='store_true', help='Replay all internal mathematical checks')
    args = parser.parse_args()
    result = build()
    print(json.dumps(result if args.payload else result['summary'],
                     ensure_ascii=False, sort_keys=True, indent=1))


if __name__ == '__main__':
    main()
