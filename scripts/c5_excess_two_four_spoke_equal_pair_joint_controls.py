#!/usr/bin/env python3
"""Complete original (2,2), mixed-(1,1), U-at-a/V-at-b relation controls.

Hand-built degree-correct graphs audit literal joins and empty fibers. They
are not disk realizations or candidates. The sealed-triangle exclusion is
an arbitrary-size paper argument in the companion report.
"""
from itertools import product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import search
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses


def edge(a, b):
    return tuple(sorted((a, b)))


def component(vertices, internal, attachments, contacts, owners):
    edges = set(internal) | {edge(v, h) for v in vertices for h in attachments[v]}
    return dict(vertices=vertices, internal_edges=sorted(internal),
                actual_attachments=attachments, ordered_contacts=contacts,
                owners=owners, edges=sorted(edges))


def unary(kind, start, owner, side):
    if kind == 'singleton':
        vertices, internal = [start], set()
        attachments = {start: [0, 2, 3] if side == 'U' else [1, 3, 4]}
    elif kind == 'edge':
        vertices, internal = [start, start + 1], {edge(start, start + 1)}
        attachments = {start: [0, 3], start + 1: [1, 2, 4]}
    else:
        assert kind == 'triangle'
        vertices = [start, start + 1, start + 2]
        internal = {edge(a, b) for a, b in ((start, start + 1),
                    (start, start + 2), (start + 1, start + 2))}
        attachments = {start: [3], start + 1: [0, 2], start + 2: [1, 4]}
    return component(vertices, internal, attachments, [start], [owner])


def fixed_graph_controls():
    shapes = [
        ('shared_singleton', [7], set(), {7: [2, 3]}, 7, 7),
        ('distinct_edge', [7, 8], {(7, 8)}, {7: [0, 2], 8: [1, 4]}, 7, 8),
        ('distinct_triangle', [7, 8, 9], {(7, 8), (7, 9), (8, 9)},
         {7: [2], 8: [4], 9: [0, 3]}, 7, 8),
        ('shared_triangle', [7, 8, 9], {(7, 8), (7, 9), (8, 9)},
         {7: [], 8: [1, 2], 9: [3, 4]}, 7, 7),
        ('distinct_square', [7, 8, 9, 10], {(7, 8), (8, 9), (9, 10), (7, 10)},
         {7: [0], 8: [1, 4], 9: [3], 10: [2, 4]}, 7, 9),
        ('path_middle_contact', [7, 8, 9], {(7, 8), (8, 9)},
         {7: [0, 2], 8: [4], 9: [1, 2, 3]}, 7, 8),
    ]
    records, joins, fibers_checked, restorations = [], 0, 0, 0
    marginal_collision, blocked_spoke = None, None
    for shape, kinds, swapped in product(shapes,
            (('singleton', 'singleton'), ('edge', 'singleton'), ('singleton', 'triangle')),
            (False, True)):
        name, cv, ce, ca, x, y = shape
        a, b = (6, 5) if swapped else (5, 6)
        c = component(cv, ce, ca, [x, y], [a, b])
        u = unary(kinds[0], max(cv) + 1, a, 'U')
        v = unary(kinds[1], max(u['vertices']) + 1, b, 'V')
        uc, vc = u['ordered_contacts'][0], v['ordered_contacts'][0]
        parts = [c, u, v]
        part_edges = [set(map(tuple, p['edges'])) for p in parts]
        interior = [a, b, *cv, *u['vertices'], *v['vertices']]
        order = sorted(B | set(interior))
        original = FRAME | set.union(*part_edges)
        original |= {edge(a, b), edge(a, x), edge(b, y), edge(a, uc), edge(b, vc)}
        original |= {edge(r, h) for r in (a, b) for h in (0, 1)}
        assert all(sum(z in e for e in original) == (5 if z in (a, b) else 4)
                   for z in interior)
        rows = []
        for ri, row in enumerate(ROWS):
            relations = [witnesses(p['vertices'], es, row, p['ordered_contacts'])
                         for p, es in zip(parts, part_edges, strict=True)]
            assert all(relations)
            for p, es, relation in zip(parts, part_edges, relations, strict=True):
                for t, f in relation.items():
                    validate_witness(f, sorted(B | set(p['vertices'])), es, row,
                                     p['ordered_contacts'], t)
            variants = []
            specs = [('G', None, False), ('G-ab', edge(a, b), False)]
            specs += [(f'G-{role}{h}', edge(r, h), False)
                      for role, r in (('a', a), ('b', b)) for h in (0, 1)]
            specs += [('G-C', None, True)]
            for label, omitted, omit_c in specs:
                actual = original - ({omitted} if omitted is not None else set())
                active = set(interior)
                ports = [a, b, x, y, uc, vc]
                if omit_c:
                    actual = {e for e in actual if not set(e) & set(cv)}
                    active -= set(cv)
                    ports = [a, b, uc, vc]
                actual_order = sorted(B | active)
                allowed = [U - {row[h] for h in (0, 1) if edge(r, h) != omitted}
                           for r in (a, b)]
                joined = {}
                citems = [((), [])] if omit_c else sorted(relations[0].items())
                for ((ct, cf), ((ut,), uf), ((vt,), vf)) in product(
                        citems, sorted(relations[1].items()), sorted(relations[2].items())):
                    for ac, bc in product(*map(sorted, allowed)):
                        if ac == ut or bc == vt or (ac == bc and omitted != edge(a, b)):
                            continue
                        if not omit_c and (ac == ct[0] or bc == ct[1]):
                            continue
                        f = dict(enumerate(row)) | {a: ac, b: bc}
                        for p, coloring in ((u, uf), (v, vf)):
                            f.update(zip(sorted(B | set(p['vertices'])), coloring, strict=True))
                        if not omit_c:
                            f.update(zip(sorted(B | set(cv)), cf, strict=True))
                        t = tuple(f[z] for z in ports)
                        joined.setdefault(t, [f[z] for z in actual_order])
                direct = list(search(active, actual, dict(enumerate(row))))
                assert set(joined) == {tuple(f[z] for z in ports) for f in direct}
                joins += 1
                for t, f in joined.items():
                    validate_witness(f, actual_order, actual, row, ports, t)
                fibers = []
                for ac, bc in product(sorted(U), repeat=2):
                    fixed = dict(enumerate(row)) | {a: ac, b: bc}
                    found = [f for f in search(active - {a, b}, actual, fixed)
                             if all(f[z] != f[w] for z, w in actual)]
                    fiber = sorted({tuple(f[z] for z in ports[2:]) for f in found})
                    assert fiber == sorted({t[2:] for t in joined if t[:2] == (ac, bc)})
                    fibers_checked += 1
                    fibers.append(dict(a_color=ac, b_color=bc,
                                       full_remaining_port_fiber=fiber))
                variants.append(dict(name=label, omitted_original_edge=omitted,
                    original_C_omitted=omit_c, vertex_order=actual_order,
                    port_order=ports, actual_edges=sorted(actual),
                    complete_joint=[dict(tuple=t, coloring=f) for t, f in sorted(joined.items())],
                    pinned_a_b_fibers=fibers))
            original_joint = {tuple(t['tuple']) for t in variants[0]['complete_joint']}
            for variant in variants[1:-1]:
                z, w = variant['omitted_original_edge']
                pi = {p: i for i, p in enumerate(variant['port_order'])}
                lifted = {tuple(t['tuple']) for t in variant['complete_joint']}
                restored = {t for t in lifted if
                            (t[pi[z]] if z in pi else row[z]) !=
                            (t[pi[w]] if w in pi else row[w])}
                assert restored == original_joint
                restorations += 1
                if lifted and not original_joint and z in B and blocked_spoke is None:
                    blocked_spoke = dict(control_index=len(records), row_index=ri,
                        omitted_original_edge=[z, w], nonempty_omission_joint=sorted(lifted),
                        restored_original_joint=[])
            cr = relations[0]
            if marginal_collision is None:
                marginals = [{t[i] for t in cr} for i in (0, 1)]
                for ac, bc in product(sorted(U), repeat=2):
                    if (marginals[0] - {ac} and marginals[1] - {bc}
                            and not any(ct[0] != ac and ct[1] != bc for ct in cr)):
                        marginal_collision = dict(control_index=len(records), row_index=ri,
                            original_contact_vertices=[x, y], C_complete_tuples=sorted(cr),
                            literal_a_b_colors=[ac, bc], guarded_C_fiber=[],
                            scope='Original complete C guard, before spoke/unary eligibility')
                        break
            rows.append(dict(row_index=ri, literal_boundary=row,
                original_relations=[dict(component=name,
                    vertex_order=sorted(B | set(p['vertices'])),
                    complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(r.items())])
                    for name, p, r in zip(('C', 'U', 'V'), parts, relations, strict=True)],
                variants=variants))
        records.append(dict(control_index=len(records), C_kind=name, unary_kinds=kinds,
            root_swapped=swapped, a=a, b=b, original_root_spoke_supports=[[0, 1], [0, 1]],
            original_edges=sorted(original), vertex_order=order,
            original_components=dict(C=c, U=u, V=v),
            shared_original_contact=x == y, rows=rows,
            scope='Complete degree graph; no disk, candidate Sigma or criticality claim'))
    assert len(records) == 36 and joins == 2520 and fibers_checked == 40320
    assert restorations == 1800 and marginal_collision is not None and blocked_spoke is not None
    swap_checks = 0
    for original, swapped in zip(records[::2], records[1::2], strict=True):
        for row, partner in zip(original['rows'], swapped['rows'], strict=True):
            for variant, other in zip(row['variants'], partner['variants'], strict=True):
                assert {tuple(t['tuple']) for t in variant['complete_joint']} == {
                    tuple(t['tuple']) for t in other['complete_joint']}
                assert variant['pinned_a_b_fibers'] == other['pinned_a_b_fibers']
                swap_checks += 1
    assert swap_checks == 1260
    return dict(records=records, independent_whole_graph_joins=joins,
        independent_pinned_a_b_fibers=fibers_checked,
        exact_original_edge_restorations=restorations,
        complete_graph_root_swap_variant_checks=swap_checks,
        marginal_collision=marginal_collision, blocked_spoke_restoration=blocked_spoke)
