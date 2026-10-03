#!/usr/bin/env python3
"""Fixed full-degree mixed-(1,2) graphs; literal ternary joins and witnesses.

These are relation controls, not disk, criticality or candidate realizations.
No component or contact is replaced by an independently normalized factor.
"""
from itertools import product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import search
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses


def edge(a, b):
    return tuple(sorted((a, b)))


def fixed_graph_controls():
    shapes = [
        ('edge_shared', [7, 8], {(7, 8)}, {7: [1], 8: [2, 3]}, 7, 7, 8),
        ('path_middle', [7, 8, 9], {(7, 8), (8, 9)},
         {7: [0, 1], 8: [4], 9: [2, 3]}, 8, 7, 9),
        ('triangle_distinct', [7, 8, 9], {(7, 8), (7, 9), (8, 9)},
         {7: [1], 8: [4], 9: [2]}, 7, 8, 9),
        ('triangle_shared', [7, 8, 9], {(7, 8), (7, 9), (8, 9)},
         {7: [], 8: [3], 9: [0, 1]}, 7, 7, 8),
        ('triangle_tail', [7, 8, 9, 10], {(7, 8), (7, 9), (8, 9), (7, 10)},
         {7: [4], 8: [1], 9: [3], 10: [0, 2]}, 10, 8, 9),
    ]
    records, joins, pinned, equalities = [], 0, 0, 0
    collision, blocked = None, None
    for shape, ukind, swapped in product(shapes,
            ('singleton', 'edge', 'path', 'triangle', 'triangle_branch'), (False, True)):
        ckind, cv, ce, ca, x, y0, y1 = shape
        a, b = (5, 6) if swapped else (6, 5)
        u = max(cv) + 1
        if ukind == 'singleton':
            uv, ue, ua = [u], set(), {u: [1, 3, 4]}
        elif ukind == 'edge':
            uv, ue, ua = [u, u+1], {edge(u, u+1)}, {u: [0, 1], u+1: [2, 3, 4]}
        elif ukind == 'path':
            uv, ue = [u, u+1, u+2], {edge(u, u+1), edge(u+1, u+2)}
            ua = {u: [0, 1], u+1: [2, 3], u+2: [0, 1, 4]}
        elif ukind == 'triangle':
            uv = [u, u+1, u+2]
            ue = {edge(u, u+1), edge(u, u+2), edge(u+1, u+2)}
            ua = {u: [4], u+1: [0, 1], u+2: [2, 3]}
        else:
            uv = [u, u+1, u+2, u+3]
            ue = {edge(u, u+1), edge(u+1, u+2), edge(u+1, u+3), edge(u+2, u+3)}
            ua = {u: [0, 1], u+1: [4], u+2: [0, 1], u+3: [2, 3]}
        c_edges = ce | {edge(v, i) for v in cv for i in ca[v]}
        u_edges = ue | {edge(v, i) for v in uv for i in ua[v]}
        original = (FRAME | c_edges | u_edges
            | {edge(a, b), edge(a, x), edge(b, y0), edge(b, y1), edge(b, u), edge(b, 2)}
            | {edge(a, i) for i in (0, 1, 2)})
        interior = [a, b, *cv, *uv]
        order, ports = sorted(B | set(interior)), [b, a, x, y0, y1, u]
        assert y0 != y1 and a not in cv and u not in cv
        assert all(sum(v in e for e in original) == (5 if v in (a, b) else 4)
                   for v in interior)
        rows = []
        for ri, row in enumerate(ROWS):
            cr = witnesses(cv, c_edges, row, [x, y0, y1])
            ur = witnesses(uv, u_edges, row, [u])
            for vs, es, contacts, relation in (
                    (cv, c_edges, [x, y0, y1], cr), (uv, u_edges, [u], ur)):
                for t, f in sorted(relation.items()):
                    validate_witness(f, sorted(B | set(vs)), es, row, contacts, t)
            variants = []
            for omitted in (None, 0, 2):
                actual = original if omitted is None else original - {edge(a, omitted)}
                kept = {0, 1, 2} - ({omitted} if omitted is not None else set())
                k_edges = c_edges | {edge(a, x)} | {edge(a, i) for i in kept}
                korder = sorted(B | {a} | set(cv))
                kr, joined = {}, {}
                for (xc, c0, c1), cf in sorted(cr.items()):
                    for ac in sorted(U - {row[i] for i in kept} - {xc}):
                        coloring = dict(zip(sorted(B | set(cv)), cf, strict=True)) | {a: ac}
                        kr.setdefault((ac, c0, c1), [coloring[v] for v in korder])
                        for (uc,), uf in sorted(ur.items()):
                            for bc in sorted(U - {row[2], ac, c0, c1, uc}):
                                full = coloring | dict(zip(sorted(B | set(uv)), uf, strict=True)) | {b: bc}
                                joined.setdefault((bc, ac, xc, c0, c1, uc), [full[v] for v in order])
                direct = list(search(set(interior), actual, dict(enumerate(row))))
                assert set(joined) == {tuple(f[v] for v in ports) for f in direct}
                assert set(kr) == set(witnesses([a, *cv], k_edges, row, [a, y0, y1]))
                joins += 1
                for t, f in sorted(joined.items()):
                    validate_witness(f, order, actual, row, ports, t)
                for t, f in sorted(kr.items()):
                    validate_witness(f, korder, k_edges, row, [a, y0, y1], t)
                fibers = []
                for bc, ac in product(sorted(U), repeat=2):
                    fixed = dict(enumerate(row)) | {b: bc, a: ac}
                    found = [f for f in search(set(interior) - {a, b}, actual, fixed)
                             if all(f[v] != f[w] for v, w in actual)]
                    fiber = sorted({(f[x], f[y0], f[y1], f[u]) for f in found})
                    assert fiber == sorted({t[2:] for t in joined if t[:2] == (bc, ac)})
                    pinned += 1
                    fibers.append(dict(b_color=bc, a_color=ac, complete_x_y0_y1_u_fiber=fiber))
                variants.append(dict(omitted_original_spoke=omitted, actual_edges=sorted(actual),
                    K_vertex_order=korder, K_ordered_contacts=[a, y0, y1],
                    K_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(kr.items())],
                    complete_joint_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(joined.items())],
                    pinned_b_a_fibers=fibers))
            restored = set(tuple(t['tuple']) for t in variants[0]['complete_joint_tuples'])
            for variant in variants[1:]:
                e = variant['omitted_original_spoke']
                tuples = set(tuple(t['tuple']) for t in variant['complete_joint_tuples'])
                assert {t for t in tuples if t[1] != row[e]} == restored
                if any(row[e] == row[i] for i in (0, 1, 2) if i != e):
                    assert tuples == restored
                    equalities += 1
                if tuples and not restored and blocked is None:
                    blocked = dict(control_index=len(records), row_index=ri,
                        original_omitted_spoke=[a, e], nonempty_M_joint=variant['complete_joint_tuples'],
                        empty_restored_G_joint=[])
            if collision is None and cr:
                marginals = [{t[j] for t in cr} for j in range(3)]
                for ac, bc in product(sorted(U), repeat=2):
                    if (marginals[0] - {ac} and marginals[1] - {bc} and marginals[2] - {bc}
                            and not any(t[0] != ac and bc not in t[1:] for t in cr)):
                        collision = dict(control_index=len(records), row_index=ri,
                            original_ordered_contacts=[x, y0, y1], complete_C_tuples=sorted(cr),
                            literal_a_b_colors=[ac, bc], complete_guarded_ternary_fiber=[],
                            scope='Full original C before root-spoke eligibility; marginals falsely permit colors')
                        break
            rows.append(dict(row_index=ri, literal_boundary=row,
                C_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(cr.items())],
                U_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(ur.items())], variants=variants))
        records.append(dict(C_kind=ckind, U_kind=ukind, root_swapped=swapped,
            original_a=a, original_b=b, vertex_order=order, complete_port_order=ports,
            original_edges=sorted(original), original_root_spokes=dict(a=[0, 1, 2], b=[2]),
            C=dict(vertices=cv, original_internal_edges=sorted(ce), actual_attachments=ca,
                ordered_contacts=[x, y0, y1], owners=[a, b, b]),
            unary_U=dict(vertices=uv, original_internal_edges=sorted(ue), actual_attachments=ua,
                ordered_contacts=[u], owner=b), rows=rows,
            scope='Fixed full-degree graph, no disk, criticality or candidate Sigma realization claim'))
    assert len(records) == 50 and joins == 1500 and pinned == 24000
    assert collision is not None
    return dict(records=records, independent_whole_graph_joins=joins,
        independent_complete_K_relations=joins, independent_pinned_b_a_fibers=pinned,
        same_color_spoke_equalities=equalities, ternary_marginal_collision=collision,
        nonempty_child_empty_restored_joint=blocked)
