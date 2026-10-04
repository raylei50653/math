#!/usr/bin/env python3
"""Fixed complete-degree controls for mixed-(2,2), with no unary.

Seven labelled contact identities remain literal throughout the joins.  These
hand-built graphs test the interfaces, not disk embedding, Sigma-criticality,
target Sigma, or source realizability.  The longer controls are separate
original graphs and are not asserted equivalent to the short graphs.
"""
from itertools import permutations, product

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import search
from c5_excess_two_mixed_core_spokes import validate_witness


PARTITIONS = (
    ('D4', (7, 8, 9, 10)),
    ('S00', (7, 8, 7, 9)),
    ('S01', (7, 8, 9, 7)),
    ('S10', (7, 8, 8, 9)),
    ('S11', (7, 8, 9, 8)),
    ('Pstraight', (7, 8, 7, 8)),
    ('Pcross', (7, 8, 8, 7)),
)


def edge(v, w):
    return tuple(sorted((v, w)))


def solve(vertices, edges, row, ports, pinned=None):
    """Direct original-edge solver, with one full witness per ordered tuple."""
    fixed = dict(enumerate(row)) | (pinned or {})
    order = sorted(B | set(vertices))
    result = {}
    for f in search(set(vertices) - set(fixed), edges, fixed):
        if not all(f[v] != f[w] for v, w in edges):
            continue
        t = tuple(f[v] for v in ports)
        result.setdefault(t, [f[v] for v in order])
    for t, witness in result.items():
        validate_witness(witness, order, edges, row, ports, t)
    return result


def make_component(contacts, longer):
    vertices = sorted(set(contacts))
    internal = ({edge(*vertices)} if len(vertices) == 2 else
                {edge(v, vertices[(i + 1) % len(vertices)])
                 for i, v in enumerate(vertices)})
    incidence = {v: int(v in contacts[:2]) + int(v in contacts[2:])
                 for v in vertices}
    # A two-contact edge, three-contact triangle, or four-contact cycle.
    # All actual attachments are chosen before any boundary row is fixed.
    attachments = {}
    for i, v in enumerate(vertices):
        deficit = 4 - sum(v in e for e in internal) - incidence[v]
        attachment_order = (0, 1) if len(vertices) == 2 else (i % 2, (i + 1) % 2)
        attachments[v] = list(attachment_order[:deficit])
        assert len(attachments[v]) == deficit
    subdivision = None
    if longer:
        v, w = min(internal)
        p, q = max(vertices) + 1, max(vertices) + 2
        internal.remove(edge(v, w))
        internal |= {edge(v, p), edge(p, q), edge(q, w)}
        vertices += [p, q]
        attachments[p] = [0, 1]
        attachments[q] = [0, 1]
        subdivision = dict(removed_template_edge=[v, w],
                           original_long_path=[v, p, q, w])
    es = internal | {edge(v, h) for v, hs in attachments.items() for h in hs}
    return dict(vertices=vertices, ordered_contacts=list(contacts),
        internal_edges=sorted(internal), actual_attachments=attachments,
        actual_support=sorted({h for hs in attachments.values() for h in hs}),
        edges=sorted(es), construction_subdivision=subdivision)


def joint(component, relation, roots, spokes, original, row, omitted=None, omit_c=False):
    a, b = roots
    cv, contacts = component['vertices'], component['ordered_contacts']
    active = {a, b} | (set() if omit_c else set(cv))
    actual = original - ({omitted} if omitted else set())
    if omit_c:
        actual = {e for e in actual if not set(e) & set(cv)}
    ports = [a, b] + ([] if omit_c else contacts)
    order, corder = sorted(B | active), sorted(B | set(cv))
    allowed = [U - {row[h] for h in spokes[r] if edge(r, h) != omitted}
               for r in roots]
    joined = {}
    items = [((), [])] if omit_c else sorted(relation.items())
    for (ct, cf), ac, bc in product(items, sorted(allowed[0]), sorted(allowed[1])):
        if ac == bc:
            continue
        if not omit_c and (ac in ct[:2] or bc in ct[2:]):
            continue
        f = dict(enumerate(row)) | {a: ac, b: bc}
        if not omit_c:
            f.update(zip(corder, cf, strict=True))
        joined.setdefault(tuple(f[v] for v in ports), [f[v] for v in order])
    direct = solve(active, actual, row, ports)
    assert set(joined) == set(direct)
    for t, coloring in joined.items():
        validate_witness(coloring, order, actual, row, ports, t)
    fibres = []
    for ac, bc in product(sorted(U), repeat=2):
        pinned = solve(active, actual, row, ports, {a: ac, b: bc})
        fibre = sorted({t[2:] for t in pinned})
        assert fibre == sorted({t[2:] for t in joined if t[:2] == (ac, bc)})
        fibres.append(dict(a_color=ac, b_color=bc, complete_C_role_fibre=fibre))
    return dict(omitted_original_edge=omitted, original_C_omitted=omit_c,
        original_vertex_order=order, original_port_order=ports,
        named_role_order=['a', 'b'] + ([] if omit_c else ['x0', 'x1', 'y0', 'y1']),
        actual_edges=sorted(actual),
        complete_joint=[dict(tuple=t, coloring=f) for t, f in sorted(joined.items())],
        pinned_a_b_fibres=fibres)


def carrier(component, relation, roots, spokes, original, row, omitted):
    """Original M minus its degree-five root: one three-contact carrier."""
    a, b = roots
    decreased = next(r for r in roots if r in omitted)
    retained = b if decreased == a else a
    own = component['ordered_contacts'][:2] if decreased == a else component['ordered_contacts'][2:]
    other = component['ordered_contacts'][2:] if decreased == a else component['ordered_contacts'][:2]
    cv = component['vertices']
    vertices = set(cv) | {decreased}
    es = {e for e in original - {omitted} if retained not in e}
    ports = [decreased, *other]
    assert len(set(ports)) == 3
    order, corder = sorted(B | vertices), sorted(B | set(cv))
    allowed = U - {row[h] for h in spokes[decreased] if edge(decreased, h) != omitted}
    joined = {}
    for (ct, cf), color in product(sorted(relation.items()), sorted(allowed)):
        own_colors = ct[:2] if decreased == a else ct[2:]
        if color in own_colors:
            continue
        f = dict(zip(corder, cf, strict=True)) | {decreased: color}
        joined.setdefault(tuple(f[v] for v in ports), [f[v] for v in order])
    direct = solve(vertices, es, row, ports)
    assert set(joined) == set(direct)
    for t, f in joined.items():
        validate_witness(f, order, es, row, ports, t)
    assert sum(decreased in e and set(e) <= vertices for e in es) == 2
    return dict(decreased_root=decreased, deleted_degree_five_root=retained,
        ordered_original_contacts=ports, marked_root_internal_degree=2,
        marked_root_is_leaf=False, original_vertex_order=order,
        original_edges=sorted(es),
        original_root_contact_edges=[edge(retained, v) for v in ports],
        complete_relation=[dict(tuple=t, coloring=f) for t, f in sorted(joined.items())],
        complete_degrees_after_original_spoke_omission={
            r: sum(r in e for e in original - {omitted}) for r in roots})


def fixed_graph_controls():
    records, joins, fibres, carriers, restorations, transports = [], 0, 0, 0, 0, 0
    marginal_failure = None
    for (name, contacts), longer, swapped in product(PARTITIONS, (False, True), (False, True)):
        a, b = (6, 5) if swapped else (5, 6)
        roots, spokes = (a, b), {a: [0, 1], b: [2, 3]}
        component = make_component(contacts, longer)
        cv, ce = component['vertices'], set(map(tuple, component['edges']))
        actual_incidence = [edge(a, v) for v in contacts[:2]] + [edge(b, v) for v in contacts[2:]]
        component['owners_by_ordered_role'] = [a, a, b, b]
        component['original_root_contact_edges'] = actual_incidence
        original = FRAME | ce | set(actual_incidence) | {edge(a, b)}
        original |= {edge(r, h) for r in roots for h in spokes[r]}
        degrees = {v: sum(v in e for e in original) for v in sorted(B | set(cv) | set(roots))}
        assert all(degrees[v] == (5 if v in roots else 4) for v in set(cv) | set(roots))
        rows = []
        for ri, row in enumerate(ROWS):
            rc = solve(cv, FRAME | ce, row, contacts)
            assert rc
            specs = [('G', None, False)]
            specs += [(f'G-{role}{h}', edge(r, h), False)
                      for role, r in (('a', a), ('b', b)) for h in spokes[r]]
            specs += [('G-C', None, True)]
            variants = []
            for label, omitted, omit_c in specs:
                item = joint(component, rc, roots, spokes, original, row, omitted, omit_c)
                item['name'] = label
                joins += 1
                fibres += 16
                if omitted:
                    item['original_three_contact_carrier'] = carrier(
                        component, rc, roots, spokes, original, row, omitted)
                    carriers += 1
                variants.append(item)
            gtuples = {tuple(t['tuple']) for t in variants[0]['complete_joint']}
            for variant in variants[1:-1]:
                r, h = (next(v for v in variant['omitted_original_edge'] if v in roots),
                        next(v for v in variant['omitted_original_edge'] if v in B))
                root_position = 0 if r == a else 1
                restored = {tuple(t['tuple']) for t in variant['complete_joint']
                            if t['tuple'][root_position] != row[h]}
                assert restored == gtuples
                restorations += 1
            # Record an actual four-role relation whose independent role
            # marginals would invent a simultaneous avoidance witness.
            if marginal_failure is None:
                marginals = [{t[i] for t in rc} for i in range(4)]
                for ac, bc in product(sorted(U), repeat=2):
                    guarded = ac != bc and all(color != row[h]
                        for r, color in ((a, ac), (b, bc)) for h in spokes[r])
                    possible = all(values - {ac if i < 2 else bc}
                                   for i, values in enumerate(marginals))
                    if guarded and possible and not any(ac not in t[:2] and bc not in t[2:] for t in rc):
                        marginal_failure = dict(control_index=len(records), identity=name,
                            row_index=ri, literal_boundary=row, original_root_colors=[ac, bc],
                            original_port_order=list(contacts),
                            complete_original_C_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(rc.items())],
                            independent_role_marginals=[sorted(s) for s in marginals],
                            guarded_original_C_fibre=[], original_spoke_and_ab_guards_hold=True,
                            scope='Actual fixed graph relation; no disk or target-source claim')
                        break
            color_controls = []
            for perm in permutations(range(4)):
                moved_row = tuple(perm[c] for c in row)
                moved_rc = solve(cv, FRAME | ce, moved_row, contacts)
                assert set(moved_rc) == {tuple(perm[c] for c in t) for t in rc}
                for variant in variants:
                    es = set(map(tuple, variant['actual_edges']))
                    for item in variant['complete_joint']:
                        moved_f = [perm[c] for c in item['coloring']]
                        moved_t = tuple(perm[c] for c in item['tuple'])
                        validate_witness(moved_f, variant['original_vertex_order'], es,
                                         moved_row, variant['original_port_order'], moved_t)
                    transports += 1
                color_controls.append(dict(global_color_permutation=perm,
                    transported_literal_boundary=moved_row,
                    independently_recomputed_complete_C_relation_size=len(moved_rc)))
            rows.append(dict(row_index=ri, literal_boundary=row,
                original_C_vertex_order=sorted(B | set(cv)),
                complete_original_R_C=[dict(tuple=t, coloring=f) for t, f in sorted(rc.items())],
                variants=variants, global_S4_color_controls=color_controls))
        records.append(dict(control_index=len(records), identity=name,
            longer_original_component=longer, root_swapped=swapped, a=a, b=b,
            original_root_order=[a, b], original_spoke_supports=[spokes[a], spokes[b]],
            ordered_original_contacts=list(contacts), original_components=dict(C=component),
            original_edges=sorted(original), original_vertex_order=sorted(B | set(cv) | set(roots)),
            original_complete_degrees=degrees, boundary_cyclic_order=sorted(B),
            literal_frame_edges=sorted(FRAME), rows=rows,
            scope='Hand-built full-degree original graph; no disk, criticality, target Sigma, or source-realizability claim'))
    swaps = 0
    for original, partner in zip(records[::2], records[1::2], strict=True):
        assert original['identity'] == partner['identity']
        for row, swapped_row in zip(original['rows'], partner['rows'], strict=True):
            for variant, swapped_variant in zip(row['variants'], swapped_row['variants'], strict=True):
                assert [item['tuple'] for item in variant['complete_joint']] == [
                    item['tuple'] for item in swapped_variant['complete_joint']]
                assert variant['pinned_a_b_fibres'] == swapped_variant['pinned_a_b_fibres']
                swaps += 1
    assert len(records) == 28 and joins == 1680 and fibres == 26880
    assert carriers == restorations == 1120 and swaps == 840 and transports == 40320
    assert marginal_failure is not None
    return dict(records=records, actual_marginal_false_positive=marginal_failure,
        summary=dict(complete_degree_original_graphs=len(records),
            contact_identity_classes=len(PARTITIONS), independent_whole_graph_joins=joins,
            independent_pinned_a_b_fibres=fibres,
            independent_original_three_contact_carrier_joins=carriers,
            exact_original_spoke_restorations=restorations,
            root_swap_variant_checks=swaps, global_S4_variant_witness_checks=transports,
            independently_recomputed_S4_C_relations=24 * 28 * len(ROWS),
            short_long_relation_equivalence_claimed=False,
            fixed_controls_are_disk_source_realizations=False))
