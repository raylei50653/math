#!/usr/bin/env python3
"""Full-degree original mixed-(1,3) controls with complete literal relations.

Fixed graphs verify identities and constructive leaf-slack extensions. They
are not disk, criticality, or candidate-Sigma realizations. The general
spanning-tree argument is stated separately in the report.
"""
from itertools import product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import search
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses


def edge(a, b):
    return tuple(sorted((a, b)))


def greedy_original_extension(interior, edges, row, a, b, color):
    """Color the whole original K, with a as the spanning-tree root."""
    vertices = set(interior) - {b}
    fixed = dict(enumerate(row)) | {b: color}
    neighbors = {v: {w if v == z else z for z, w in edges if v in (z, w)}
                 for v in vertices}
    lists = {v: U - {fixed[w] for w in neighbors[v] if w in fixed}
             for v in vertices}
    degree = {v: len(neighbors[v] & vertices) for v in vertices}
    assert all(len(lists[v]) >= degree[v] for v in vertices)
    assert degree[a] == 1 and len(lists[a]) > degree[a]
    parent, depth, queue = {a: None}, {a: 0}, [a]
    for v in queue:
        for w in sorted(neighbors[v] & vertices):
            if w not in parent:
                parent[w], depth[w] = v, depth[v] + 1
                queue.append(w)
    assert set(parent) == vertices
    order = sorted(vertices, key=lambda v: (-depth[v], v))
    coloring = dict(fixed)
    for v in order:
        available = lists[v] - {coloring[w] for w in neighbors[v] if w in coloring}
        assert available
        coloring[v] = min(available)
    assert all(coloring[z] != coloring[w] for z, w in edges)
    full_order = sorted(B | set(interior))
    return dict(b_color=color, K_vertex_order=sorted(vertices),
        exact_lists=[dict(vertex=v, colors=sorted(lists[v]), degree_in_K=degree[v])
                     for v in sorted(vertices)],
        spanning_tree=[dict(vertex=v, parent=parent[v], depth=depth[v]) for v in sorted(vertices)],
        reverse_tree_order=order, full_vertex_order=full_order,
        whole_graph_coloring=[coloring[v] for v in full_order])


def fixed_graph_controls():
    shapes = [
        ('path_shared_y0', [7, 8, 9], {(7, 8), (8, 9)}, 7, [7, 8, 9]),
        ('path_shared_y1', [7, 8, 9], {(7, 8), (8, 9)}, 8, [7, 8, 9]),
        ('path_shared_y2', [7, 8, 9], {(7, 8), (8, 9)}, 9, [7, 8, 9]),
        ('triangle_shared', [7, 8, 9], {(7, 8), (7, 9), (8, 9)}, 7, [7, 8, 9]),
        ('star_distinct', [7, 8, 9, 10], {(7, 8), (7, 9), (7, 10)}, 7, [8, 9, 10]),
        ('cycle_distinct', [7, 8, 9, 10], {(7, 8), (8, 9), (9, 10), (7, 10)}, 7, [8, 9, 10]),
        ('triangle_tail_distinct', [7, 8, 9, 10], {(7, 8), (7, 9), (8, 9), (7, 10)}, 10, [7, 8, 9]),
        ('long_path_distinct', list(range(7, 13)), {(v, v+1) for v in range(7, 12)}, 7, [8, 10, 12]),
    ]
    records, joins, pinned, equalities, greedy_checks = [], 0, 0, 0, 0
    collision, blocked = None, None
    for shape, shift, swapped in product(shapes, range(5), (False, True)):
        kind, cv, ce, x, ys = shape
        a, b = (5, 6) if swapped else (6, 5)
        attachments = {}
        for v in cv:
            count = 4 - sum(v in e for e in ce) - int(v == x) - int(v in ys)
            assert 0 <= count <= 3
            attachments[v] = sorted((v + 2*k + shift) % 5 for k in range(count))
        c_edges = ce | {edge(v, i) for v in cv for i in attachments[v]}
        original = (FRAME | c_edges | {edge(a, b), edge(a, x), edge(b, 2)}
                    | {edge(b, y) for y in ys} | {edge(a, i) for i in (0, 1, 2)})
        interior, contacts = [a, b, *cv], [x, *ys]
        order, ports = sorted(B | set(interior)), [b, a, *contacts]
        assert len(set(ys)) == 3 and len(set([a, *ys])) == 4
        assert all(sum(v in e for e in original) == (5 if v in (a, b) else 4)
                   for v in interior)
        rows = []
        for ri, row in enumerate(ROWS):
            cr = witnesses(cv, c_edges, row, contacts)
            assert cr
            for t, f in sorted(cr.items()):
                validate_witness(f, sorted(B | set(cv)), c_edges, row, contacts, t)
            variants = []
            for omitted in (None, 0, 2):
                actual = original if omitted is None else original - {edge(a, omitted)}
                kept = {0, 1, 2} - ({omitted} if omitted is not None else set())
                k_edges = c_edges | {edge(a, x)} | {edge(a, i) for i in kept}
                korder = sorted(B | {a} | set(cv))
                kr, joined = {}, {}
                for t, cf in sorted(cr.items()):
                    xc, *yc = t
                    for ac in sorted(U - {row[i] for i in kept} - {xc}):
                        coloring = dict(zip(sorted(B | set(cv)), cf, strict=True)) | {a: ac}
                        kr.setdefault((ac, *yc), [coloring[v] for v in korder])
                        for bc in sorted(U - {row[2], ac, *yc}):
                            full = coloring | {b: bc}
                            joined.setdefault((bc, ac, *t), [full[v] for v in order])
                direct = list(search(set(interior), actual, dict(enumerate(row))))
                assert set(joined) == {tuple(f[v] for v in ports) for f in direct}
                assert set(kr) == set(witnesses([a, *cv], k_edges, row, [a, *ys]))
                joins += 1
                for t, f in sorted(joined.items()):
                    validate_witness(f, order, actual, row, ports, t)
                for t, f in sorted(kr.items()):
                    validate_witness(f, korder, k_edges, row, [a, *ys], t)
                fibers = []
                for bc, ac in product(sorted(U), repeat=2):
                    fixed = dict(enumerate(row)) | {b: bc, a: ac}
                    found = [f for f in search(set(cv), actual, fixed)
                             if all(f[v] != f[w] for v, w in actual)]
                    fiber = sorted({tuple(f[v] for v in contacts) for f in found})
                    assert fiber == sorted({t[2:] for t in joined if t[:2] == (bc, ac)})
                    pinned += 1
                    fibers.append(dict(b_color=bc, a_color=ac, complete_x_y0_y1_y2_fiber=fiber))
                forbidden = sorted(d for d in U if not any(d not in t for t in kr))
                leaf_palette = U - {row[i] for i in kept}
                if len(leaf_palette) >= 2:
                    assert set(forbidden) <= leaf_palette
                extensions = []
                for bc in sorted({row[i] for i in kept} - {row[2]}):
                    if len(leaf_palette) <= 1:
                        continue
                    cert = greedy_original_extension(interior, actual, row, a, b, bc)
                    coloring = dict(zip(cert['full_vertex_order'], cert['whole_graph_coloring'], strict=True))
                    value = tuple(coloring[v] for v in ports)
                    assert value in joined
                    validate_witness(cert['whole_graph_coloring'], order, actual, row, ports, value)
                    extensions.append(cert)
                    greedy_checks += 1
                variants.append(dict(omitted_original_spoke=omitted, actual_edges=sorted(actual),
                    K_vertex_order=korder, K_ordered_contacts=[a, *ys],
                    K_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(kr.items())],
                    K_complete_relation_forbidden_colors=forbidden,
                    marked_leaf_available_colors=sorted(leaf_palette),
                    complete_joint_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(joined.items())],
                    pinned_b_a_fibers=fibers, constructive_leaf_slack_extensions=extensions))
            restored = {tuple(t['tuple']) for t in variants[0]['complete_joint_tuples']}
            for variant in variants[1:]:
                omitted = variant['omitted_original_spoke']
                tuples = {tuple(t['tuple']) for t in variant['complete_joint_tuples']}
                assert {t for t in tuples if t[1] != row[omitted]} == restored
                if any(row[omitted] == row[i] for i in (0, 1, 2) if i != omitted):
                    assert tuples == restored and tuples
                    assert variant['constructive_leaf_slack_extensions']
                    equalities += 1
                if tuples and not restored and blocked is None:
                    blocked = dict(control_index=len(records), row_index=ri,
                        original_omitted_spoke=[a, omitted], nonempty_M_joint=variant['complete_joint_tuples'],
                        empty_restored_G_joint=[])
            if collision is None:
                marginals = [{t[j] for t in cr} for j in range(4)]
                for ac, bc in product(sorted(U), repeat=2):
                    if (marginals[0] - {ac} and all(m - {bc} for m in marginals[1:])
                            and not any(t[0] != ac and bc not in t[1:] for t in cr)):
                        collision = dict(control_index=len(records), row_index=ri,
                            original_ordered_contacts=contacts, complete_C_tuples=sorted(cr),
                            literal_a_b_colors=[ac, bc], complete_guarded_quaternary_fiber=[],
                            scope='Full original C before root-spoke eligibility; marginals falsely permit colors')
                        break
            rows.append(dict(row_index=ri, literal_boundary=row,
                C_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(cr.items())], variants=variants))
        records.append(dict(C_kind=kind, attachment_shift=shift, root_swapped=swapped,
            original_a=a, original_b=b, vertex_order=order, complete_port_order=ports,
            original_edges=sorted(original), original_root_spokes=dict(a=[0, 1, 2], b=[2]),
            C=dict(vertices=cv, original_internal_edges=sorted(ce), actual_attachments=attachments,
                ordered_contacts=contacts, owners=[a, b, b, b]), rows=rows,
            scope='Fixed full-degree graph, no disk, criticality or candidate Sigma realization claim'))
    assert len(records) == 80 and joins == 2400 and pinned == 38400
    assert collision is not None
    return dict(records=records, independent_whole_graph_joins=joins,
        independent_complete_K_relations=joins, independent_pinned_b_a_fibers=pinned,
        same_color_spoke_equalities=equalities, constructive_whole_graph_extensions=greedy_checks,
        quaternary_marginal_collision=collision, nonempty_child_empty_restored_joint=blocked)
