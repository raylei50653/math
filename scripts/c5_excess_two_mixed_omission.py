#!/usr/bin/env python3
"""Omitting the unique original (1,1)-mixed component accepts every row.

Inherited degree-four cores retain both ends of the original bridge zw.
The original mixed relation is binary, in one literal frame. Its capacity,
one fixed support's S4 transport, and explicit contraction-star subdivisions
exclude the necessary domain. Arbitrary-size coverage is a paper argument.
Run under: uv run --with networkx==3.5 python scripts/<this file> [--check]
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import networkx as nx

from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, components
from c5_941_two_spoke import Q4, relabel_mask, search
from c5_excess_two_triangle_edge import graph, inherited_bases as triangle_bases
from c5_excess_two_path_edge import inherited_bases as path_bases, path_edges
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses
from c5_excess_two_mixed_core_spoke_unary import verify_subdivision
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_omission/observations.json'
BRANCHES = ROOT / 'artifacts/c5_triangle_branches/observations.json'
SWITCHES = ROOT / 'artifacts/c5_triangle_path_reduction/observations.json'
DOUBLE = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'
ODD = ROOT / 'artifacts/c5_odd_join_cores/observations.json'
TREE = ROOT / 'artifacts/c5_tree_cores/observations.json'
PERMUTATIONS = tuple(permutations(range(4)))
PAIRS = tuple(product(range(4), repeat=2))


def encoded(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + '\n'


def forbidden_domain():
    fs = [()] + [(t,) for t in PAIRS]
    fs += [t for t in combinations(PAIRS, 2)
           if len({a for a, _ in t}) == len({b for _, b in t}) == 2]
    assert len(fs) == 89 and len(set(fs)) == 89
    assert {tuple(sorted((b, a) for a, b in f)) for f in fs} == set(fs)
    return fs


def local_shape(values):
    labels = {}
    return tuple(labels.setdefault(c, len(labels)) for c in values)


def support_domain(mask, fs):
    support = [b for b in sorted(B) if mask >> b & 1]
    shapes, representatives, transports = {}, [], []
    for ri, row in enumerate(ROWS):
        values = tuple(row[b] for b in support)
        shape = local_shape(values)
        if shape not in shapes:
            shapes[shape] = len(representatives)
            stabilizers = [p for p in PERMUTATIONS if all(p[c] == c for c in values)]
            choices = [f for f in fs if all(
                tuple(sorted((p[a], p[b]) for a, b in f)) == f for p in stabilizers)]
            representatives.append(dict(shape=shape, representative_row=ri,
                literal_support_colors=values, stabilizers=stabilizers, choices=choices))
        sid = shapes[shape]
        rep = representatives[sid]
        maps = [p for p in PERMUTATIONS
                if tuple(p[c] for c in rep['literal_support_colors']) == values]
        outputs = []
        for f in rep['choices']:
            images = {tuple(sorted((p[a], p[b]) for a, b in f)) for p in maps}
            assert len(images) == 1
            outputs.append(images.pop())
        transports.append(dict(local_shape=sid, color_permutation=maps[0],
            all_color_maps=len(maps), literal_forbidden_choices=outputs))
    return dict(id=mask, actual_boundary_support=support,
                local_shapes=representatives, row_transports=transports)


def support_test(ks, target, domain):
    allowed = [set(range(len(s['choices']))) for s in domain['local_shapes']]
    row_choices = []
    for ri, (k, t) in enumerate(zip(ks, domain['row_transports'], strict=True)):
        choices = {j for j, f in enumerate(t['literal_forbidden_choices'])
                   if bool(set(k)-set(f)) == bool(target >> ri & 1)}
        allowed[t['local_shape']] &= choices
        row_choices.append(sorted(choices))
    empty = [s for s, a in enumerate(allowed) if not a]
    if empty:
        sid = empty[0]
        conflicts = [dict(row_index=ri, allowed_choice_indices=row_choices[ri])
                     for ri, t in enumerate(domain['row_transports'])
                     if t['local_shape'] == sid]
        assert not set.intersection(*(set(c['allowed_choice_indices']) for c in conflicts))
        return dict(support_id=domain['id'], empty_local_shape=sid,
                    conflicting_row_constraints=conflicts)
    assignment = [min(a) for a in allowed]
    schedule = [t['literal_forbidden_choices'][assignment[t['local_shape']]]
                for t in domain['row_transports']]
    assert sum(1 << ri for ri, (k, f) in enumerate(zip(ks, schedule, strict=True))
               if set(k)-set(f)) == target
    return dict(support_id=domain['id'], shape_assignment=assignment,
                possible_local_choice_indices=list(map(sorted, allowed)),
                literal_forbidden_schedule=schedule)


def necessary_forms():
    forms = {}

    def add(data, pair, runs, origin):
        # Positive unmarked gaps use one or two points; zero stays zero.
        for run in runs:
            gap = 0
            for v in run:
                if v in pair:
                    if gap > 2:
                        return
                    gap = 0
                else:
                    gap += 1
            if gap > 2 or (not set(run) & set(pair) and len(run) > 2):
                return
        key = (tuple(map(tuple, data['edges'])), pair)
        if key not in forms:
            forms[key] = dict(data, original_root_order=pair,
                              uniform_runs=runs, inherited_origin=origin)

    bases, switches = triangle_bases()
    for bi, base in enumerate(bases):
        for lengths in product((1, 3, 5), repeat=len(base['branch_paths'])):
            tails = [[base['neighborhoods'][3+2*s]]*length
                     + [base['neighborhoods'][4+2*s]]
                     for s, length in enumerate(lengths)]
            data = dict(graph(base, tails), family='triangle_single_run')
            inner = set(data['interior_order'])
            for pair in sorted(e for e in map(tuple, data['edges'])
                               if set(e) <= inner and not set(e) <= {5, 6, 7}):
                add(data, pair, [p[:-1] for p in data['branch_paths']],
                    dict(input=str(BRANCHES.relative_to(ROOT)), base_index=bi))
    for bi, other in sorted(switches.items()):
        base = bases[bi]
        for length in (2, 4, 6):
            data = dict(graph(base, [[base['neighborhoods'][3]]+[other]*length
                                    + [base['neighborhoods'][4]]]),
                        family='triangle_two_runs')
            path = data['branch_paths'][0]
            for pair in [(5, path[0])] + list(zip(path, path[1:])):
                add(data, pair, [path[:1], path[1:-1]],
                    dict(input=str(SWITCHES.relative_to(ROOT)), base_index=bi))
    for bi, base in enumerate(path_bases()[0]):
        ns, supports = base['neighborhoods'], []
        for support in ns[1:-1]:
            if not supports or support != supports[-1]:
                supports.append(support)
        for lengths in product((2, 4, 6), repeat=len(supports)):
            ns2 = [ns[0]] + [s for s, length in zip(supports, lengths, strict=True)
                            for _ in range(length)] + [ns[-1]]
            interior = list(range(5, 5+len(ns2)))
            data = dict(vertices=5+len(ns2), interior_order=interior,
                neighborhoods=ns2, edges=sorted(path_edges(ns2)), family='path')
            runs, start = [], 6
            for length in lengths:
                runs.append(list(range(start, start+length)))
                start += length
            for pair in zip(interior, interior[1:]):
                add(data, pair, runs, dict(input=base['input_path'], base_index=bi))
    old = json.loads(DOUBLE.read_text())['disk_templates']
    assert len(old) == 128
    for bi, base in enumerate(old):
        es = set(map(tuple, base['edges']))
        interior = list(range(5, 5+len(base['neighborhoods'])))
        sigma = sum(1 << ri for ri, row in enumerate(ROWS)
                    if next(search(interior, es, dict(enumerate(row))), None))
        assert sigma == base['sigma']
        if sigma != 1022:
            continue
        triangles = [t for t in combinations(interior, 3)
                     if all(e in es for e in combinations(t, 2))]
        bridge, = [e for e in es if set(e) <= set(interior)
                   and not any(set(e) <= set(t) for t in triangles)]
        add(dict(vertices=5+len(interior), interior_order=interior,
                 neighborhoods=base['neighborhoods'], edges=sorted(es),
                 family='double_triangle'), bridge, [],
            dict(input=str(DOUBLE.relative_to(ROOT)), base_index=bi))
    result = list(forms.values())
    assert Counter(f['family'] for f in result) == {
        'triangle_single_run': 160, 'triangle_two_runs': 64, 'path': 56,
        'double_triangle': 64}
    return result


def dynamic_pairs(form, row, cut, port_order=None):
    """Complete joint port DP, with each output's whole-core witness."""
    pair, ns = form['original_root_order'], form['neighborhoods']
    ports = list(pair) if port_order is None else port_order
    positions = {v: i for i, v in enumerate(ports)}
    avail = {v: U-{row[b] for b in ns[v-5]} for v in form['interior_order']}
    if form['family'] == 'double_triangle':
        es = set(map(tuple, form['edges'])) - ({tuple(pair)} if cut else set())
        return {t: tuple(f[5:]) for t, f in witnesses(
            form['interior_order'], es, row, ports).items()}
    if form['family'] == 'path':
        states = {((), None, (None,)*len(ports)): ()}
        paths = [form['interior_order']]
    else:
        states = {}
        for colors in product(*(sorted(avail[v]) for v in (5, 6, 7))):
            if len(set(colors)) == 3:
                values = tuple(colors[v-5] if v < 8 else None for v in ports)
                states[(colors, None, values)] = colors
        paths = form['branch_paths']
    for slot, path in enumerate(paths):
        if form['family'] != 'path':
            states = {(tri, tri[slot], values): full
                      for (tri, _, values), full in states.items()}
        previous = None if form['family'] == 'path' else 5+slot
        for v in path:
            following = {}
            removed = cut and previous is not None and tuple(sorted((previous, v))) == tuple(pair)
            for (tri, last, values), full in sorted(states.items(), key=lambda x: repr(x[0])):
                for c in sorted(avail[v]):
                    if c == last and not removed:
                        continue
                    updated = list(values)
                    if v in positions:
                        updated[positions[v]] = c
                    key = (tri, c, tuple(updated))
                    following.setdefault(key, full+(c,))
            states, previous = following, v
    result = {}
    for (_, _, values), full in sorted(states.items(), key=lambda x: repr(x[0])):
        assert all(c is not None for c in values)
        result.setdefault(values, full)
    return result


def core_context(form):
    es, pair = set(map(tuple, form['edges'])), tuple(form['original_root_order'])
    interior, cut = set(form['interior_order']), es-{pair}
    sides = components(interior, cut)
    assert len(sides) == 2
    sides.sort(key=lambda vs: pair[0] not in vs)
    assert all(pair[i] in sides[i] and pair[1-i] not in sides[i] for i in (0, 1))
    regions = []
    for ri, vs in enumerate(components(interior-set(pair), es)):
        contacts = [[v for v in vs if tuple(sorted((r, v))) in es] for r in pair]
        owners = [r for r, cs in zip(pair, contacts, strict=True) if cs]
        assert len(owners) == 1
        attachments = [dict(vertex=v, neighbors=sorted(b for b in B if (b, v) in es))
                       for v in vs]
        regions.append(dict(id=ri, vertices=vs, ownership=owners, kind='unary',
            root_contacts=contacts, contact_order=sorted(set().union(*map(set, contacts))),
            boundary_attachments=attachments,
            actual_support=sorted({b for a in attachments for b in a['neighbors']}),
            incident_edges=sorted(e for e in es if set(e) & set(vs))))
    ports = list(pair) + sorted({v for r in regions for v in r['contact_order']})
    side_context = [dict(root=pair[i], vertices=vs,
        port_order=[v for v in ports if v in vs],
        edges=sorted(e for e in cut if set(e) <= (B | set(vs))),
        boundary_attachments=[dict(vertex=v, neighbors=sorted(b for b in B if (b, v) in es))
                              for v in vs]) for i, vs in enumerate(sides)]
    rows = []
    for row in ROWS:
        joint = witnesses(interior, cut, row, ports)
        pairs = {t[:2] for t in joint}
        assert set(joint) == set(dynamic_pairs(form, row, True, ports))
        assert pairs == set(dynamic_pairs(form, row, True))
        assert {t for t in pairs if t[0] != t[1]} == set(dynamic_pairs(form, row, False))
        side_rows, composed = [], set()
        side_relations = []
        for side in side_context:
            sw = witnesses(side['vertices'], set(map(tuple, side['edges'])), row, side['port_order'])
            assert sw
            side_relations.append(sw)
            side_rows.append(dict(port_tuples=sorted(sw),
                witness_vertex_order=sorted(B | set(side['vertices'])),
                coloring_witnesses=[sw[t] for t in sorted(sw)]))
        for a, b in product(*side_relations):
            f = dict(zip(side_context[0]['port_order'], a, strict=True))
            f.update(zip(side_context[1]['port_order'], b, strict=True))
            composed.add(tuple(f[v] for v in ports))
        assert composed == set(joint)
        order = sorted(B | interior)
        for t, f in joint.items():
            validate_witness(f, order, cut, row, ports, t)
        rows.append(dict(joint_port_tuples=sorted(joint),
            coloring_witnesses=[joint[t] for t in sorted(joint)],
            complete_root_pairs=sorted(pairs),
            original_bridge_retained_pairs=sorted(t for t in pairs if t[0] != t[1]),
            side_relations=side_rows))
    assert sum(1 << ri for ri, r in enumerate(rows) if r['original_bridge_retained_pairs']) == 1022
    assert all(sum(v in e for e in es) == 4 for v in interior)
    critical = []
    for edge in sorted(es-FRAME):
        f = next(search(interior, es-{edge}, dict(enumerate(Q4))), None)
        assert f is not None
        critical.append(dict(edge=edge, coloring=[f[v] for v in sorted(B | interior)]))
    return dict(form, port_order=ports, witness_vertex_order=sorted(B | interior),
                original_retained_unaries=regions, original_cut_root_sides=side_context,
                q4_critical_witnesses=critical, sigma=1022, rows=rows)


def grown_control(form):
    """Grow each positive unmarked gap by two, retaining singleton roots."""
    pair, grow = tuple(form['original_root_order']), set()
    for run in form['uniform_runs']:
        last_marked = True
        for v in run:
            if v in pair:
                last_marked = True
            else:
                if last_marked:
                    grow.add(v)
                last_marked = False
    branch_sets, next_vertex, ns = {b: [b] for b in sorted(B)}, 5, []
    for v in form['interior_order']:
        size = 3 if v in grow else 1
        branch_sets[v] = list(range(next_vertex, next_vertex+size))
        ns.extend([form['neighborhoods'][v-5]]*size)
        next_vertex += size
    edges = set(FRAME)
    for v in form['interior_order']:
        group = branch_sets[v]
        edges |= set(zip(group, group[1:]))
        edges |= {(b, w) for w in group for b in form['neighborhoods'][v-5]}
    for a, b in map(tuple, form['edges']):
        if a not in B:
            edges.add((branch_sets[a][-1], branch_sets[b][0]))
    inverse = {v: old for old, group in branch_sets.items() for v in group}
    quotient = {tuple(sorted((inverse[a], inverse[b]))) for a, b in edges if inverse[a] != inverse[b]}
    assert quotient == set(map(tuple, form['edges']))
    roots = tuple(branch_sets[v][0] for v in pair)
    assert all(len(branch_sets[v]) == 1 for v in pair)
    data = dict(vertices=next_vertex, interior_order=list(range(5, next_vertex)),
        neighborhoods=ns, edges=sorted(edges), family=form['family'],
        original_root_order=roots, quotient_branch_sets=branch_sets)
    if form['family'] != 'path' and form['family'] != 'double_triangle':
        data.update(triangle=[5, 6, 7], branch_paths=[
            [w for v in path for w in branch_sets[v]] for path in form['branch_paths']])
    context = core_context_light(data)
    ports = list(roots) + sorted({v for region in context['retained_unaries']
                                 for cs in region['root_contacts'] for v in cs})
    data['port_order'] = ports
    relations = []
    for ri, row in enumerate(ROWS):
        ws = dynamic_pairs(data, row, True)
        assert set(ws) == set(map(tuple, form['rows'][ri]['complete_root_pairs']))
        retained = {t for t in ws if t[0] != t[1]}
        assert retained == set(dynamic_pairs(data, row, False))
        assert retained == set(map(tuple, form['rows'][ri]['original_bridge_retained_pairs']))
        for t, f in ws.items():
            validate_witness(list(row)+list(f), list(range(next_vertex)),
                             edges-{roots}, row, roots, t)
        joint = dynamic_pairs(data, row, True, ports)
        assert {t[:2] for t in joint} == set(ws)
        for t, f in joint.items():
            validate_witness(list(row)+list(f), list(range(next_vertex)),
                             edges-{roots}, row, ports, t)
        relations.append(dict(complete_root_pairs=sorted(ws),
            coloring_witnesses=[list(row)+list(ws[t]) for t in sorted(ws)],
            complete_joint_port_tuples=sorted(joint),
            joint_coloring_witnesses=[list(row)+list(joint[t]) for t in sorted(joint)],
            bridge_retained_joint_tuple_indices=[i for i, t in enumerate(sorted(joint))
                                                 if t[0] != t[1]]))
    data['rows'] = relations
    data['original_context'] = context
    return data


def core_context_light(data):
    """Original components, actual attachments and contacts of a grown core."""
    es, roots = set(map(tuple, data['edges'])), data['original_root_order']
    regions = []
    for vs in components(set(data['interior_order'])-set(roots), es):
        contacts = [[v for v in vs if tuple(sorted((r, v))) in es] for r in roots]
        regions.append(dict(vertices=vs, root_contacts=contacts,
            ownership=[r for r, cs in zip(roots, contacts, strict=True) if cs],
            boundary_attachments=[dict(vertex=v, neighbors=data['neighborhoods'][v-5]) for v in vs],
            actual_support=sorted({b for v in vs for b in data['neighborhoods'][v-5]})))
    return dict(retained_unaries=regions, cut_root_sides=components(
        set(data['interior_order']), es-{tuple(roots)}))


def star_obstruction(fi, form, support):
    c, apex = form['vertices'], form['vertices']+1
    pair, es = tuple(form['original_root_order']), set(map(tuple, form['edges']))
    augmented = es | {(r, c) for r in pair} | {(b, c) for b in support} | {(b, apex) for b in B}
    g = nx.Graph()
    g.add_nodes_from(range(apex+1))
    g.add_edges_from(sorted(augmented))
    certificate = kuratowski_certificate(g)
    verify_subdivision(augmented, certificate)
    return dict(form_id=fi, original_root_order=pair, actual_boundary_support=support,
        contracted_original_mixed_vertex=c, boundary_apex=apex,
        minor_edges=sorted(augmented), obstruction=certificate,
        contraction_semantics='the entire original connected C is one branch set; this is only a topology minor, not a color-relation replacement')


def algebra_controls(fs):
    permitted = []
    for a, b in PAIRS:
        permitted.append(sum(1 << i for i, (x, y) in enumerate(PAIRS) if x != a and y != b))
    counts, images, digest = Counter(), set(), sha256()
    for mask in range(65536):
        f = tuple(t for t, allow in zip(PAIRS, permitted, strict=True) if not mask & allow)
        counts['complete_binary_relations'] += 1
        if all(sum(x == a for x, _ in f) <= 1 for a in U) and all(
                sum(y == b for _, y in f) <= 1 for b in U):
            assert f in fs
            images.add(f)
            counts['relations_satisfying_root_slack_capacity'] += 1
        digest.update(f'{mask}:{f}\n'.encode())
    assert images == set(fs)
    assert counts['relations_satisfying_root_slack_capacity'] == 65431
    diagonal, off_diagonal = {(0, 0), (1, 1)}, {(0, 1), (1, 0)}
    def join(t):
        return [(a, b, x, y) for a, b in ((0, 1),) for x, y in sorted(t)
                if a != x and b != y]
    assert not join(diagonal) and join(off_diagonal)
    return dict(**counts, distinct_forbidden_relations=len(images),
        enumeration_sha256=digest.hexdigest(),
        marginal_collision=dict(scope='abstract relation control, not a source realization',
            core_root_pair=[0, 1], complete_C_relations=[sorted(diagonal), sorted(off_diagonal)],
            equal_endpoint_marginals=[[0, 1], [0, 1]],
            joined_tuples=[join(diagonal), join(off_diagonal)]))


def actual_mixed_controls(forms):
    templates = [dict(kind='shared_singleton', inner=[], supports=[[0, 2]], contacts=[0, 0]),
        dict(kind='shared_edge', inner=[(0, 1)], supports=[[0], [1, 3, 4]], contacts=[0, 0]),
        dict(kind='distinct_edge', inner=[(0, 1)], supports=[[0, 2], [1, 3]], contacts=[0, 1]),
        dict(kind='distinct_path', inner=[(0, 1), (1, 2)], supports=[[0, 2], [0, 2], [1, 3]], contacts=[0, 2]),
        dict(kind='distinct_triangle', inner=[(0, 1), (0, 2), (1, 2)], supports=[[0], [1], [2, 4]], contacts=[0, 1])]
    selected = [next(i for i, f in enumerate(forms) if f['family'] == family)
                for family in ('triangle_single_run', 'triangle_two_runs', 'path', 'double_triangle')]
    records, collision, checks, transport_checks = [], None, 0, 0
    for fi in selected:
        form, es = forms[fi], set(map(tuple, forms[fi]['edges']))
        z, w = form['original_root_order']
        for template in templates:
            vs = list(range(form['vertices'], form['vertices']+len(template['supports'])))
            ce = {tuple(sorted((vs[a], vs[b]))) for a, b in template['inner']}
            ce |= {(b, v) for v, support in zip(vs, template['supports'], strict=True) for b in support}
            x, y = [vs[i] for i in template['contacts']]
            attached = {(z, x), (w, y)}
            edges, interior = es | ce | attached, form['interior_order']+vs
            assert all(sum(v in e for e in edges) == (5 if v in (z, w) else 4) for v in interior)
            port_order = form['port_order'] + sorted(set((x, y)))
            rows = []
            for ri, row in enumerate(ROWS):
                contact_order = sorted(set((x, y)))
                cw = witnesses(vs, FRAME | ce, row, contact_order)
                t = {(a[contact_order.index(x)], a[contact_order.index(y)]): f for a, f in cw.items()}
                assert t
                forbidden = {p for p in PAIRS if not any(p[0] != a and p[1] != b for a, b in t)}
                assert tuple(sorted(forbidden)) in forbidden_domain()
                core_row = form['rows'][ri]
                joined, cut_joined = {}, {}
                for a, f in zip(core_row['joint_port_tuples'], core_row['coloring_witnesses'], strict=True):
                    for c, g in cw.items():
                        if a[0] == c[contact_order.index(x)] or a[1] == c[contact_order.index(y)]:
                            continue
                        witness = f + g[5:]
                        cut_joined.setdefault(tuple(a)+c, witness)
                        if a[0] != a[1]:
                            joined.setdefault(tuple(a)+c, witness)
                direct = witnesses(interior, edges, row, port_order)
                direct_cut = witnesses(interior, edges-{(z, w)}, row, port_order)
                assert set(joined) == set(direct) and set(cut_joined) == set(direct_cut)
                assert bool(joined) == bool(set(map(tuple, core_row['original_bridge_retained_pairs']))-forbidden)
                for value, witness in joined.items():
                    validate_witness(witness, list(range(max(interior)+1)), edges, row, port_order, value)
                if collision is None:
                    k = core_row['original_bridge_retained_pairs']
                    marginal_join = [(a, b) for a, b in k if any(x1 != a for x1, _ in t)
                                     and any(y1 != b for _, y1 in t)]
                    if marginal_join and not joined:
                        collision = dict(form_id=fi, template_kind=template['kind'], row_index=ri,
                            actual_C_relation=sorted(t), complete_core_root_pairs=k,
                            spurious_marginal_pairs=marginal_join,
                            full_graph_joined_tuples=[], core_coloring_witnesses=core_row['coloring_witnesses'],
                            C_coloring_witnesses=[t[a] for a in sorted(t)])
                rows.append(dict(original_C_contact_order=contact_order,
                    original_C_complete_tuples=sorted(cw), C_coloring_witnesses=[cw[a] for a in sorted(cw)],
                    original_C_role_relation=sorted(t), forbidden_root_pairs=sorted(forbidden),
                    complete_G_tuples=sorted(joined), G_coloring_witnesses=[joined[a] for a in sorted(joined)],
                    complete_N_tuples=sorted(cut_joined), N_coloring_witnesses=[cut_joined[a] for a in sorted(cut_joined)]))
                checks += 1
            support = sorted({b for s in template['supports'] for b in s})
            for i, j in product(range(10), repeat=2):
                for permutation in PERMUTATIONS:
                    if all(permutation[ROWS[i][b]] == ROWS[j][b] for b in support):
                        assert {tuple(permutation[c] for c in t) for t in rows[i]['original_C_role_relation']} == set(rows[j]['original_C_role_relation'])
                        assert {tuple(permutation[c] for c in t) for t in rows[i]['forbidden_root_pairs']} == set(rows[j]['forbidden_root_pairs'])
                        transport_checks += 1
            records.append(dict(form_id=fi, template_kind=template['kind'], original_root_order=[z, w],
                original_mixed_vertices=vs, original_contacts=[[x], [y]],
                original_C_edges=sorted(ce), original_root_contact_edges=sorted(attached),
                actual_C_attachments=[dict(vertex=v, neighbors=s) for v, s in zip(vs, template['supports'], strict=True)],
                actual_C_support=sorted({b for s in template['supports'] for b in s}),
                full_G_edges=sorted(edges), full_G_port_order=port_order,
                witness_vertex_order=list(range(max(interior)+1)),
                C_witness_vertex_order=sorted(B | set(vs)), rows=rows,
                scope='actual same-graph coloring controls; no disk or target realization assertion'))
    assert collision is not None
    return dict(original_graphs=records, full_row_join_checks=checks,
                original_C_full_relation_transport_checks=transport_checks,
                actual_marginal_collision=collision)


def build():
    fs = forbidden_domain()
    supports = [support_domain(mask, fs) for mask in range(32)]
    forms = [core_context(f) for f in necessary_forms()]
    orbits = {str(mask): sorted({relabel_mask(mask, [(s*j+t) % 5 for j in range(5)])
                for s in (-1, 1) for t in range(5)}) for mask in (933, 941)}
    summary, minor_index, minors = Counter(), {}, []
    for fi, form in enumerate(forms):
        ks = [r['original_bridge_retained_pairs'] for r in form['rows']]
        comparisons = []
        for label, targets in orbits.items():
            for target in targets:
                summary['target_comparisons'] += 1
                empty = [ri for ri, k in enumerate(ks) if target >> ri & 1 and not k]
                capacity = [ri for ri, k in enumerate(ks) if not target >> ri & 1 and k
                    and (len(k) > 2 or len({a for a, _ in k}) != len(k)
                         or len({b for _, b in k}) != len(k))]
                record = dict(target_family=int(label), target_mask=target)
                if empty:
                    record.update(exclusion='target_accepts_empty_core_row', row_index=empty[0])
                    summary['empty_accepted_core_row'] += 1
                elif capacity:
                    record.update(exclusion='mixed_capacity', row_index=capacity[0])
                    summary['capacity_exclusions'] += 1
                else:
                    summary['fixed_support_comparisons'] += 1
                    tests = []
                    for domain in supports:
                        test = support_test(ks, target, domain)
                        if 'empty_local_shape' in test:
                            summary['incompatible_supports'] += 1
                        else:
                            summary['compatible_nondisk_supports'] += 1
                            key = (fi, domain['id'])
                            if key not in minor_index:
                                minor_index[key] = len(minors)
                                minors.append(star_obstruction(fi, form, domain['actual_boundary_support']))
                            test['contraction_star_subdivision_index'] = minor_index[key]
                        tests.append(test)
                    record.update(exclusion='fixed_support_transport_or_nondisk_star', support_tests=tests)
                comparisons.append(record)
        form['target_comparisons'] = comparisons
    long_controls = [grown_control(f) for f in forms]
    pinned, pinned_forms = 0, []
    for family in ('triangle_single_run', 'triangle_two_runs', 'path', 'double_triangle'):
        chosen = sorted((i for i, f in enumerate(forms) if f['family'] == family),
                        key=lambda i: (-long_controls[i]['vertices'], i))[:3]
        pinned_forms.extend(chosen)
        for fi in chosen:
            data = long_controls[fi]
            pair, edges = data['original_root_order'], set(map(tuple, data['edges']))
            for ri, row in enumerate(ROWS):
                actual = set(map(tuple, data['rows'][ri]['complete_root_pairs']))
                for value in PAIRS:
                    fixed = dict(enumerate(row)) | dict(zip(pair, value, strict=True))
                    cut_edges = edges-{tuple(pair)}
                    fixed_conflict = any(fixed[a] == fixed[b] for a, b in cut_edges
                                         if a in fixed and b in fixed)
                    f = None if fixed_conflict else next(search(
                        set(data['interior_order'])-set(pair), cut_edges, fixed), None)
                    assert (f is not None) == (value in actual)
                    pinned += 1
    controls = actual_mixed_controls(forms)
    summary.update(normal_forms=len(forms), full_core_row_queries=10*len(forms),
        original_cut_side_row_queries=20*len(forms), original_long_graphs=len(long_controls),
        long_relation_comparisons=20*len(forms), independent_pinned_long_queries=pinned,
        actual_mixed_control_graphs=len(controls['original_graphs']),
        actual_mixed_control_row_joins=controls['full_row_join_checks'],
        actual_C_relation_transports=controls['original_C_full_relation_transport_checks'],
        explicit_contraction_star_subdivisions=len(minors), residuals=0)
    summary.update({'subdivision_'+kind: count for kind, count in Counter(
        m['obstruction']['model'] for m in minors).items()})
    assert summary['fixed_support_comparisons'] == 286
    assert summary['incompatible_supports'] == 8508
    assert summary['compatible_nondisk_supports'] == 644
    dependencies = [Path(__file__).resolve(), ROOT/'scripts/c5_independent_support_capacity.py',
        ROOT/'scripts/c5_941_two_spoke.py', ROOT/'scripts/c5_excess_two_triangle_edge.py',
        ROOT/'scripts/c5_excess_two_path_edge.py', ROOT/'scripts/c5_excess_two_mixed_core_spokes.py',
        ROOT/'scripts/c5_excess_two_mixed_core_spoke_unary.py', ROOT/'scripts/c5_odd_join_cores.py',
        BRANCHES, SWITCHES, DOUBLE, ODD, TREE]
    return dict(schema=1,
        scope='inherited necessary all-degree-four cores with the original bridge roots retained; arbitrary original (1,1)-mixed C is constrained by exact binary joining, capacity and one fixed actual support; paper supplies arbitrary-size coverage',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        pattern_order=ROWS, normalized_omitted_row=Q4, target_D5_orbits=orbits,
        forbidden_pair_relations=fs, fixed_support_domains=supports,
        relation_controls=algebra_controls(fs), original_marked_cores=forms,
        contraction_star_subdivisions=minors, original_long_graph_controls=long_controls,
        independent_pinned_long_form_ids=pinned_forms,
        actual_mixed_controls=controls, summary=dict(sorted(summary.items())))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = build()
    result = encoded(data)
    if args.check:
        assert OUT.read_text() == result, 'certificate differs; regenerate intentionally'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(result)
    print(json.dumps(dict(status='checked' if args.check else 'written', **data['summary']), sort_keys=True))


if __name__ == '__main__':
    main()
