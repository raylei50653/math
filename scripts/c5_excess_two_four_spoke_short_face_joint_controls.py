#!/usr/bin/env python3
"""Literal original C/U/V joins for spokes a:{0,1}, b:{0,2}.

These degree-correct fixed graphs check relation algebra and edge restoration.
They are not disk realizations, complete-Sigma candidates, or critical graphs.
The short-support triangle deliberately violates planarity; its K5 minor
shows why the companion paper's short-face exclusion needs disk topology.
"""
from itertools import product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import search
from c5_excess_two_four_spoke_equal_pair_joint_controls import component, edge, unary
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses
from c5_short_support_singleton import k5_witness


def short_triangle(start, owner):
    """Degree-four U whose one contact is forced to boundary vertex 1's color."""
    vertices = list(range(start, start + 3))
    internal = {edge(v, w) for v, w in ((start, start + 1),
                (start, start + 2), (start + 1, start + 2))}
    attachments = {start: [0], start + 1: [0, 1], start + 2: [0, 1]}
    return component(vertices, internal, attachments, [start], [owner])


def fixed_graph_controls():
    shapes = [
        ('shared_singleton', [7], set(), {7: [2, 3]}, 7, 7),
        ('distinct_edge', [7, 8], {(7, 8)}, {7: [0, 2], 8: [1, 4]}, 7, 8),
        ('distinct_triangle', [7, 8, 9], {(7, 8), (7, 9), (8, 9)},
         {7: [2], 8: [4], 9: [0, 3]}, 7, 8),
    ]
    kind_pairs = [('singleton', 'singleton'), ('edge', 'singleton'),
                  ('singleton', 'triangle'), ('triangle_short01', 'singleton')]
    records, joins, fibers_checked, restorations = [], 0, 0, 0
    projection_checks, replacement_witnesses, singleton_failures = 0, 0, 0
    marginal_collision, blocked_unary, blocked_spoke = None, None, None
    singleton_projection_counterexample = None
    short_counterexample = None
    for shape, kinds, swapped in product(shapes, kind_pairs, (False, True)):
        name, cv, ce, ca, x, y = shape
        a, b = (6, 5) if swapped else (5, 6)
        c = component(cv, ce, ca, [x, y], [a, b])
        u = (short_triangle(max(cv) + 1, a) if kinds[0] == 'triangle_short01'
             else unary(kinds[0], max(cv) + 1, a, 'U'))
        v = unary(kinds[1], max(u['vertices']) + 1, b, 'V')
        if kinds == ('singleton', 'singleton'):
            # This degree-correct choice includes a nonempty G-au row for
            # which every lifted tuple identifies a with its unary contact.
            u = component(u['vertices'], set(), {u['vertices'][0]: [0, 1, 4]},
                          u['ordered_contacts'], [a])
            v = component(v['vertices'], set(), {v['vertices'][0]: [0, 1, 4]},
                          v['ordered_contacts'], [b])
        uc, vc = u['ordered_contacts'][0], v['ordered_contacts'][0]
        parts = [c, u, v]
        for p in parts:
            p['actual_support'] = sorted({h for hs in p['actual_attachments'].values()
                                          for h in hs})
            p['original_root_contact_edges'] = [edge(r, q) for r, q in
                zip(p['owners'], p['ordered_contacts'], strict=True)]
        # Each factor sees this literal boundary frame; no factor gets its own
        # color normalization. Repeated x=y remains two named roles.
        part_edges = [FRAME | set(map(tuple, p['edges'])) for p in parts]
        interior = [a, b, *cv, *u['vertices'], *v['vertices']]
        order = sorted(B | set(interior))
        original = set.union(*part_edges)
        original |= {edge(a, b), edge(a, x), edge(b, y), edge(a, uc), edge(b, vc)}
        spokes = {a: [0, 1], b: [0, 2]}
        original |= {edge(r, h) for r in (a, b) for h in spokes[r]}
        degrees = {z: sum(z in e for e in original) for z in order}
        assert all(degrees[z] == (5 if z in (a, b) else 4) for z in interior)
        rows = []
        short_rows = []
        for ri, row in enumerate(ROWS):
            relations = [witnesses(p['vertices'], es, row, p['ordered_contacts'])
                         for p, es in zip(parts, part_edges, strict=True)]
            assert all(relations)
            for p, es, relation in zip(parts, part_edges, relations, strict=True):
                for t, f in relation.items():
                    validate_witness(f, sorted(B | set(p['vertices'])), es, row,
                                     p['ordered_contacts'], t)
            if kinds[0] == 'triangle_short01':
                assert set(relations[1]) == {(row[1],)}
                short_rows.append(dict(row_index=ri, literal_boundary=row,
                    singleton_forbidden_a_color=row[1],
                    complete_U_tuples=[dict(tuple=t, coloring=f)
                                       for t, f in sorted(relations[1].items())]))
            specs = [('G', None, False), ('G-au', edge(a, uc), False),
                     ('G-bv', edge(b, vc), False), ('G-ab', edge(a, b), False)]
            specs += [(f'G-{role}{h}', edge(r, h), False)
                      for role, r in (('a', a), ('b', b)) for h in spokes[r]]
            specs += [('G-C', None, True)]
            variants = []
            for label, omitted, omit_c in specs:
                actual = original - ({omitted} if omitted is not None else set())
                active = set(interior)
                ports, roles = [a, b, x, y, uc, vc], ['a', 'b', 'x', 'y', 'u', 'v']
                if omit_c:
                    actual = {e for e in actual if not set(e) & set(cv)}
                    active -= set(cv)
                    ports, roles = [a, b, uc, vc], ['a', 'b', 'u', 'v']
                actual_order = sorted(B | active)
                allowed = [U - {row[h] for h in spokes[r] if edge(r, h) != omitted}
                           for r in (a, b)]
                joined = {}
                citems = [((), [])] if omit_c else sorted(relations[0].items())
                for ((ct, cf), ((ut,), uf), ((vt,), vf)) in product(
                        citems, sorted(relations[1].items()), sorted(relations[2].items())):
                    for ac, bc in product(*map(sorted, allowed)):
                        if ((ac == ut and omitted != edge(a, uc))
                                or (bc == vt and omitted != edge(b, vc))
                                or (ac == bc and omitted != edge(a, b))):
                            continue
                        if not omit_c and (ac == ct[0] or bc == ct[1]):
                            continue
                        f = dict(enumerate(row)) | {a: ac, b: bc}
                        for p, coloring in ((u, uf), (v, vf)):
                            f.update(zip(sorted(B | set(p['vertices'])), coloring, strict=True))
                        if not omit_c:
                            f.update(zip(sorted(B | set(cv)), cf, strict=True))
                        t = tuple(f[z] for z in ports)
                        assert x != y or omit_c or t[2] == t[3]
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
                    named_role_order=roles, port_order=ports, actual_edges=sorted(actual),
                    complete_joint=[dict(tuple=t, coloring=f) for t, f in sorted(joined.items())],
                    pinned_a_b_fibers=fibers))
            original_joint = {tuple(t['tuple']) for t in variants[0]['complete_joint']}
            # Forget only U's contact color. Keep both roots, both original
            # C roles (including repeated x=y), and the original V contact.
            # This is conditional algebra, independent of short-face topology.
            keep = [0, 1, 2, 3, 5]
            projection = lambda t: tuple(t[i] for i in keep)
            omitted_u_joint = {tuple(t['tuple']) for t in variants[1]['complete_joint']}
            original_projection = sorted({projection(t) for t in original_joint})
            omitted_projection = sorted({projection(t) for t in omitted_u_joint})
            replacement_records = []
            if len(relations[1]) >= 2:
                assert original_projection == omitted_projection
                projection_checks += 1
                outside_u = set(order) - set(u['vertices'])
                u_order = sorted(B | set(u['vertices']))
                for lifted in variants[1]['complete_joint']:
                    old_tuple = tuple(lifted['tuple'])
                    old_coloring = dict(zip(order, lifted['coloring'], strict=True))
                    replacement_tuple, replacement = next((t, f) for t, f in
                        sorted(relations[1].items()) if t[0] != old_tuple[0])
                    new_coloring = dict(old_coloring)
                    new_coloring.update(zip(u_order, replacement, strict=True))
                    assert all(new_coloring[z] == old_coloring[z] for z in outside_u)
                    assert new_coloring[uc] != new_coloring[a]
                    new_tuple = tuple(new_coloring[z] for z in variants[0]['port_order'])
                    assert new_tuple in original_joint
                    assert projection(new_tuple) == projection(old_tuple)
                    new_witness = [new_coloring[z] for z in order]
                    validate_witness(new_witness, order, original, row,
                                     variants[0]['port_order'], new_tuple)
                    replacement_witnesses += 1
                    replacement_records.append(dict(
                        G_au_tuple=old_tuple, G_au_coloring=lifted['coloring'],
                        changed_original_U_vertices=sorted(z for z in u['vertices']
                            if new_coloring[z] != old_coloring[z]),
                        replacement_original_U_tuple=replacement_tuple,
                        replacement_original_U_vertex_order=u_order,
                        replacement_original_U_coloring=replacement,
                        extended_original_G_tuple=new_tuple,
                        extended_original_G_coloring=new_witness))
            elif original_projection != omitted_projection:
                singleton_failures += 1
                if singleton_projection_counterexample is None:
                    singleton_projection_counterexample = dict(control_index=len(records),
                        row_index=ri, literal_boundary=row,
                        original_U_complete_tuples=sorted(relations[1]),
                        retained_role_order=['a', 'b', 'x', 'y', 'v'],
                        original_G_projection=original_projection,
                        G_au_projection=omitted_projection,
                        missing_original_G_projected_tuples=sorted(
                            set(omitted_projection) - set(original_projection)),
                        scope='Failure without the at-least-two-U-colors hypothesis')
            projection_audit = dict(retained_tuple_positions=keep,
                retained_role_order=['a', 'b', 'x', 'y', 'v'],
                original_U_contact_relation_size=len(relations[1]),
                at_least_two_original_U_contact_colors=len(relations[1]) >= 2,
                original_G_projection=original_projection,
                G_au_projection=omitted_projection,
                projections_equal=original_projection == omitted_projection,
                original_U_replacement_witnesses=replacement_records,
                scope='Fixed-graph conditional U replacement; no short-face or disk conclusion')
            for variant in variants[1:-1]:
                z, w = variant['omitted_original_edge']
                pi = {p: i for i, p in enumerate(variant['port_order'])}
                lifted = {tuple(t['tuple']) for t in variant['complete_joint']}
                restored = {t for t in lifted if
                            (t[pi[z]] if z in pi else row[z]) !=
                            (t[pi[w]] if w in pi else row[w])}
                assert restored == original_joint
                restorations += 1
                if lifted and not original_joint:
                    obstruction = dict(control_index=len(records), row_index=ri,
                        variant=variant['name'], omitted_original_edge=[z, w],
                        nonempty_omission_joint=sorted(lifted), restored_original_joint=[],
                        one_omission_coloring=variant['complete_joint'][0]['coloring'],
                        vertex_order=variant['vertex_order'],
                        scope='Restoration obstruction at this fixed row; no criticality claim')
                    if variant['name'] == 'G-au' and blocked_unary is None:
                        assert all(t[0] == t[4] for t in lifted)
                        assert len(relations[1]) == 1
                        obstruction.update(original_U_complete_tuples=sorted(relations[1]),
                            retained_tuple_positions=keep,
                            original_G_projection=original_projection,
                            G_au_projection=omitted_projection)
                        blocked_unary = obstruction
                    if z in B and blocked_spoke is None:
                        blocked_spoke = obstruction
            cr = relations[0]
            if marginal_collision is None:
                marginals = [{t[i] for t in cr} for i in (0, 1)]
                for ac, bc in product(sorted(U), repeat=2):
                    if (marginals[0] - {ac} and marginals[1] - {bc}
                            and not any(ct[0] != ac and ct[1] != bc for ct in cr)):
                        marginal_collision = dict(control_index=len(records), row_index=ri,
                            original_contact_vertices=[x, y], C_complete_tuples=sorted(cr),
                            literal_a_b_colors=[ac, bc], guarded_C_fiber=[],
                            scope='Complete C guard before spoke and unary eligibility')
                        break
            rows.append(dict(row_index=ri, literal_boundary=row,
                original_relations=[dict(component=name,
                    vertex_order=sorted(B | set(p['vertices'])), actual_edges=sorted(es),
                    ordered_contacts=p['ordered_contacts'],
                    complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(r.items())])
                    for name, p, es, r in zip(('C', 'U', 'V'), parts, part_edges,
                                            relations, strict=True)], variants=variants,
                conditional_U_projection_extension_audit=projection_audit))
        if kinds[0] == 'triangle_short01' and short_counterexample is None:
            short_counterexample = dict(control_index=len(records),
                original_root=a, original_contact=uc, actual_support=[0, 1],
                original_spokes=spokes[a], original_U=u,
                original_edges=sorted(original), rows=short_rows,
                **k5_witness(original, [[0], [1, a], *[[z] for z in u['vertices']]]),
                scope='Nonplanar fixed graph with short support and forbidden singleton; '
                      'short-support exclusion requires the disk hypothesis')
        records.append(dict(control_index=len(records), C_kind=name, unary_kinds=kinds,
            root_swapped=swapped, a=a, b=b, boundary_cyclic_order=list(range(5)),
            literal_frame_edges=sorted(FRAME),
            original_root_spoke_supports=[spokes[a], spokes[b]],
            original_edges=sorted(original), vertex_order=order, original_degrees=degrees,
            original_components=dict(C=c, U=u, V=v),
            shared_original_contact=x == y, rows=rows,
            scope='Complete degree graph; no disk, candidate Sigma or criticality claim'))
    assert len(records) == 24 and joins == 2160 and fibers_checked == 34560
    assert restorations == 1680 and marginal_collision is not None
    assert blocked_unary is not None and blocked_spoke is not None
    assert short_counterexample is not None
    assert projection_checks == 108 and replacement_witnesses == 3736
    assert singleton_failures == 58 and singleton_projection_counterexample is not None
    swap_checks = 0
    for original, swapped in zip(records[::2], records[1::2], strict=True):
        def swap_vertex(z):
            return 11 - z if z in (5, 6) else z

        assert {edge(swap_vertex(z), swap_vertex(w))
                for z, w in original['original_edges']} == set(swapped['original_edges'])
        for row, partner in zip(original['rows'], swapped['rows'], strict=True):
            audit = row['conditional_U_projection_extension_audit']
            other_audit = partner['conditional_U_projection_extension_audit']
            for key in ('original_U_contact_relation_size', 'original_G_projection',
                        'G_au_projection', 'projections_equal'):
                assert audit[key] == other_audit[key]
            for variant, other in zip(row['variants'], partner['variants'], strict=True):
                assert {edge(swap_vertex(z), swap_vertex(w))
                        for z, w in variant['actual_edges']} == set(other['actual_edges'])
                assert {tuple(t['tuple']) for t in variant['complete_joint']} == {
                    tuple(t['tuple']) for t in other['complete_joint']}
                assert variant['pinned_a_b_fibers'] == other['pinned_a_b_fibers']
                swap_checks += 1
    assert swap_checks == 1080
    summary = dict(complete_original_degree_graphs=len(records),
        literal_boundary_rows_per_graph=len(ROWS),
        independent_whole_graph_joins=joins,
        independent_pinned_a_b_fibers=fibers_checked,
        exact_original_edge_restorations=restorations,
        complete_graph_root_swap_variant_checks=swap_checks,
        conditional_U_projection_row_checks=projection_checks,
        original_U_replacement_witnesses=replacement_witnesses,
        singleton_U_projection_failure_rows=singleton_failures)
    return dict(records=records, summary=summary,
        independent_whole_graph_joins=joins,
        independent_pinned_a_b_fibers=fibers_checked,
        exact_original_edge_restorations=restorations,
        complete_graph_root_swap_variant_checks=swap_checks,
        conditional_U_projection_row_checks=projection_checks,
        original_U_replacement_witnesses=replacement_witnesses,
        marginal_collision=marginal_collision,
        blocked_au_restoration=blocked_unary, blocked_spoke_restoration=blocked_spoke,
        singleton_U_projection_counterexample=singleton_projection_counterexample,
        short_support_without_topology_counterexample=short_counterexample)
