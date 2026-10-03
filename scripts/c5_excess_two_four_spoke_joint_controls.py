#!/usr/bin/env python3
"""Fixed original four-spoke graphs: full joins and marked-leaf fibers.

These controls verify relation identities, not disk or candidate realization.
The arbitrary-size exclusion and its support lifts are paper arguments.
"""
from hashlib import sha256
from itertools import combinations, product
import json

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import search
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses


def edge(a, b):
    return tuple(sorted((a, b)))


def common_support_controls():
    """All actual supports whose minimum cyclic span is at least two."""
    from c5_independent_support_capacity import span
    from c5_single_spoke_cores import placements

    supports = [tuple(i for i in sorted(B) if bits >> i & 1)
                for bits in range(1, 32)]
    long = [s for s in supports if span(s) >= 2]
    assert len(long) == 21
    checked, digest = 0, sha256()
    for spoke, named in product(sorted(B), product(long, repeat=3)):
        assert not placements(spoke, named)
        digest.update((json.dumps([spoke, named, []]) + '\n').encode())
        checked += 1
    assert checked == 46305
    positive = ((0, 1), (1, 2, 3), (0, 3, 4))
    pos = placements(0, positive)
    assert pos and [span(s) for s in positive] == [1, 2, 2]
    exterior = []
    for triple, pair in product(combinations(sorted(B), 3), sorted(FRAME)):
        h = min(set(triple) - set(pair))
        exterior.append(dict(a_spokes=triple, adjacent_unary_support_envelope=pair,
                             outside_boundary_endpoint=h,
                             original_path_vertex_roles=['b', 'a', f'b{h}']))
    assert len(exterior) == 50
    return dict(scope='Actual support/lift controls, not graphs or an embedding theorem',
                support_span_at_least_two=long, common_lift_checks=checked,
                compatible_three_long_supports=0,
                common_lift_enumeration_sha256=digest.hexdigest(),
                positive_122=dict(spoke=0, supports=positive, placements=pos),
                all_three_spoke_external_path_choices=exterior)


def graph_controls():
    records, joins, pinned, same_color_checks = [], 0, 0, 0
    marginal_collision, blocked_leaf = None, None
    shapes = [
        ('singleton', [7], set(), {7: [1, 4]}, 7, 7),
        ('edge', [7, 8], {(7, 8)}, {7: [1, 2], 8: [3, 4]}, 7, 8),
        ('triangle', [7, 8, 9], {(7, 8), (7, 9), (8, 9)},
         {7: [1], 8: [4], 9: [2, 3]}, 7, 8),
    ]
    for shape, ukind, swapped in product(shapes, ('singleton', 'edge'), (False, True)):
        ckind, cv, ce, ca, x, y = shape
        a, b = (5, 6) if swapped else (6, 5)
        u = max(cv) + 1
        uv = [u] if ukind == 'singleton' else [u, u + 1]
        ue = set() if ukind == 'singleton' else {(u, u + 1)}
        ua = {u: [0, 1, 4]} if ukind == 'singleton' else {u: [0, 4], u + 1: [0, 1, 4]}
        v = max(uv) + 1
        vv, va = [v], {v: [0, 3, 4]}
        c_edges = ce | {edge(z, i) for z in cv for i in ca[z]}
        u_edges = ue | {edge(z, i) for z in uv for i in ua[z]}
        v_edges = {edge(v, i) for i in va[v]}
        original = (FRAME | c_edges | u_edges | v_edges
                    | {edge(a, b), edge(a, x), edge(b, y), edge(b, u), edge(b, v)}
                    | {edge(a, i) for i in (0, 1, 2)} | {edge(b, 4)})
        interior = [a, b, *cv, *uv, v]
        order, ports = sorted(B | set(interior)), [b, a, y, u, v]
        assert all(sum(z in e for e in original) == (5 if z in (a, b) else 4)
                   for z in interior)
        rows = []
        for ri, row in enumerate(ROWS):
            cr = witnesses(cv, c_edges, row, [x, y])
            ur = witnesses(uv, u_edges, row, [u])
            vr = witnesses(vv, v_edges, row, [v])
            assert cr and ur and vr
            for vertices, edges, contacts, relation in (
                    (cv, c_edges, [x, y], cr), (uv, u_edges, [u], ur),
                    (vv, v_edges, [v], vr)):
                for t, f in relation.items():
                    validate_witness(f, sorted(B | set(vertices)), edges, row, contacts, t)
            variants = []
            for omitted in (None, 0, 2):
                actual = original if omitted is None else original - {edge(a, omitted)}
                support = {0, 1, 2} - ({omitted} if omitted is not None else set())
                joined, kr = {}, {}
                korder = sorted(B | {a} | set(cv))
                for (xc, yc), cf in sorted(cr.items()):
                    for ac in sorted(U - {row[i] for i in support} - {xc}):
                        coloring = dict(zip(sorted(B | set(cv)), cf)) | {a: ac}
                        kr.setdefault((ac, yc), [coloring[z] for z in korder])
                        for ((uc,), uf), ((vc,), vf) in product(sorted(ur.items()), sorted(vr.items())):
                            for bc in sorted(U - {row[4], ac, yc, uc, vc}):
                                full = coloring | dict(zip(sorted(B | set(uv)), uf))
                                full.update(zip(sorted(B | set(vv)), vf))
                                full[b] = bc
                                joined.setdefault((bc, ac, yc, uc, vc), [full[z] for z in order])
                direct = list(search(set(interior), actual, dict(enumerate(row))))
                assert set(joined) == {tuple(f[z] for z in ports) for f in direct}
                joins += 1
                for t, f in joined.items():
                    validate_witness(f, order, actual, row, ports, t)
                k_edges = c_edges | {edge(a, x)} | {edge(a, i) for i in support}
                for t, f in kr.items():
                    validate_witness(f, korder, k_edges, row, [a, y], t)
                fibers = []
                for bc, ac in product(sorted(U), repeat=2):
                    fixed = dict(enumerate(row)) | {b: bc, a: ac}
                    found = [f for f in search(set(interior) - {a, b}, actual, fixed)
                             if all(f[z] != f[w] for z, w in actual)]
                    fiber = sorted({(f[y], f[u], f[v]) for f in found})
                    assert fiber == sorted({t[2:] for t in joined if t[:2] == (bc, ac)})
                    pinned += 1
                    fibers.append(dict(b_color=bc, a_color=ac, whole_y_u_v_fiber=fiber))
                variants.append(dict(omitted_original_spoke=omitted, actual_edges=sorted(actual),
                    K_vertex_order=korder, K_ordered_contacts=[a, y],
                    K_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(kr.items())],
                    complete_joint_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(joined.items())],
                    pinned_b_a_fibers=fibers))
            restored = {tuple(t['tuple']) for t in variants[0]['complete_joint_tuples']}
            for variant in variants[1:]:
                e = variant['omitted_original_spoke']
                tuples = {tuple(t['tuple']) for t in variant['complete_joint_tuples']}
                assert {t for t in tuples if t[1] != row[e]} == restored
                if any(row[e] == row[i] for i in (0, 1, 2) if i != e):
                    assert tuples == restored
                    same_color_checks += 1
                if tuples and not restored and blocked_leaf is None:
                    blocked_leaf = dict(control_index=len(records), row_index=ri,
                        omitted_original_spoke=[a, e], forced_a_color=row[e],
                        nonempty_M_joint=variant['complete_joint_tuples'], restored_G_joint=[])
            if x == y and marginal_collision is None:
                mx, my = ({t[j] for t in cr} for j in (0, 1))
                for ac, bc in product(sorted(U), repeat=2):
                    if (mx - {ac} and my - {bc}
                            and not any(xc != ac and yc != bc for xc, yc in cr)):
                        marginal_collision = dict(control_index=len(records), row_index=ri,
                            original_contact_vertices=[x, y], complete_C_tuples=sorted(cr),
                            literal_a_b_colors=[ac, bc], complete_guarded_fiber=[],
                            scope='Original C relation control before root-spoke eligibility')
                        break
            rows.append(dict(row_index=ri, literal_boundary=row,
                C_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(cr.items())],
                U_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(ur.items())],
                V_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(vr.items())],
                variants=variants))
        records.append(dict(C_kind=ckind, U_kind=ukind, V_kind='singleton', root_swapped=swapped,
            original_a=a, original_b=b, vertex_order=order, complete_port_order=ports,
            original_edges=sorted(original), original_root_spokes=dict(a=[0, 1, 2], b=[4]),
            C=dict(vertices=cv, original_internal_edges=sorted(ce), actual_attachments=ca,
                   ordered_contacts=[x, y], owners=[a, b]),
            unary_U=dict(vertices=uv, original_internal_edges=sorted(ue), actual_attachments=ua,
                         contact=u, owner=b),
            unary_V=dict(vertices=vv, original_internal_edges=[], actual_attachments=va,
                         contact=v, owner=b), rows=rows,
            scope='Fixed original graph, no disk, criticality or candidate realization claim'))
    assert len(records) == 12 and joins == 360 and pinned == 5760
    assert marginal_collision is not None
    return dict(records=records, independent_whole_graph_joins=joins,
                independent_pinned_b_a_fibers=pinned, same_color_spoke_equalities=same_color_checks,
                marginal_collision=marginal_collision, blocked_nonempty_leaf_fiber=blocked_leaf)
