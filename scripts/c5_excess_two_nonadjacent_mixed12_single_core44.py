#!/usr/bin/env python3
"""U3 sole mixed12: marked single-triangle finite necessity controls.

Retain the ordered boundary and every original root/contact coordinate.
Marked uniform and two-run tails are compressed only by positive-run parity.
The paper supplies arbitrary-length coverage and unary-shield geometry.
Replay requires only Python's standard library; generation of subdivisions
uses NetworkX 3.5. No old primary producer is imported or rerun.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_nonadjacent_mixed12_single_core44/observations.json'
INPUTS = [ROOT / 'artifacts/c5_triangle_branches/observations.json',
          ROOT / 'artifacts/c5_triangle_path_reduction/observations.json']
B = set(range(5))
FRAME = {tuple(sorted((i, (i+1) % 5))) for i in range(5)}
PAIRS = tuple(product(range(4), repeat=2))
PERMS = tuple(permutations(range(4)))


def normalize(values):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in values)


ROWS = tuple(sorted({normalize(r) for r in product(range(4), repeat=5)
                     if all(r[a] != r[b] for a, b in FRAME)}))
Q = (0, 1, 0, 1, 2)
T4 = sum(1 << i for i, r in enumerate(ROWS) if len(set(r)) == 4)


def colorings(edges, row, ports, first_only=False):
    """MRV whole-graph backtracking, one whole coloring per complete tuple."""
    vertices = B | set().union(*map(set, edges))
    adjacent = {v: set() for v in vertices}
    for a, b in edges:
        adjacent[a].add(b)
        adjacent[b].add(a)
    fixed, result = dict(enumerate(row)), {}

    def visit():
        todo = vertices - fixed.keys()
        if not todo:
            result.setdefault(tuple(fixed[v] for v in ports),
                              tuple(fixed[v] for v in sorted(vertices)))
            return
        choices = {v: set(range(4)) - {fixed[u] for u in adjacent[v] if u in fixed}
                   for v in todo}
        v = min(todo, key=lambda x: (len(choices[x]), -len(adjacent[x]), x))
        for c in sorted(choices[v]):
            fixed[v] = c
            visit()
            if first_only and result:
                break
        fixed.pop(v, None)

    visit()
    return result


def components(vertices, edges):
    todo, result = set(vertices), []
    while todo:
        found, pending = set(), [min(todo)]
        while pending:
            v = pending.pop()
            if v in found:
                continue
            found.add(v)
            pending.extend(b if a == v else a for a, b in edges
                           if v in (a, b) and {a, b} <= todo)
        todo -= found
        result.append(sorted(found))
    return result


def rotation_check(edges, rotation):
    """Verify the saved exterior-apex combinatorial sphere embedding."""
    n = len(rotation)-1
    augmented = edges | {(b, n) for b in B}
    for v, ns in enumerate(rotation):
        assert len(ns) == len(set(ns))
        assert set(ns) == {b if a == v else a for a, b in augmented if v in (a, b)}
    todo = {(a, b) for a, b in augmented} | {(b, a) for a, b in augmented}
    faces = []
    while todo:
        start = min(todo)
        dart, face = start, []
        while True:
            assert dart in todo
            todo.remove(dart)
            a, b = dart
            face.append(a)
            ns = rotation[b]
            dart = (b, ns[(ns.index(a)-1) % len(ns)])
            if dart == start:
                break
        faces.append(face)
    assert len(rotation)-len(augmented)+len(faces) == 2
    return faces


def marked_forms():
    """Keep the marked root singleton and preserve zero/positive run parity."""
    bases = json.loads(INPUTS[0].read_text())['disk_templates']
    runs = json.loads(INPUTS[1].read_text())['normal_forms']
    forms = []
    contexts = [(0, i, b) for i, b in enumerate(bases)] + [(1, i, b) for i, b in enumerate(runs)]
    for family, bi, b in contexts:
        es = set(map(tuple, b['edges']))
        triangle = {5, 6, 7}
        rotation_check(es, b['apex_rotation'] if family == 0 else b['topology']['apex_rotation'])
        tails = []
        for vs in components(set().union(*map(set, es)) - B - triangle, es):
            path = []
            prior = None
            start, = [v for v in vs if any((tuple(sorted((v, t))) in es for t in triangle))]
            t, = [t for t in triangle if tuple(sorted((t, start))) in es]
            current = start
            while True:
                path.append(current)
                nxt = [v for v in vs if v != prior and tuple(sorted((v, current))) in es]
                if not nxt:
                    break
                prior, current = (current, nxt[0])
            assert set(path) == set(vs)
            tails.append((t, path))
        for ti, (t, path) in enumerate(tails):
            X = sorted((bd for bd in B if tuple(sorted((bd, path[0]))) in es))
            leaf = sorted((bd for bd in B if tuple(sorted((bd, path[-1]))) in es))
            specs = []
            if family == 0:
                for p, s in ((0, 0), (0, 2), (2, 0), (2, 2), (1, 1)):
                    specs.append(('uniform_nonleaf', p, s, [X] * (p + 1 + s) + [leaf], p))
                specs.append(('uniform_leaf', 0, 0, [X, leaf], 1))
            else:
                Y = sorted((bd for bd in B if tuple(sorted((bd, path[1]))) in es))
                specs.append(('two_run_X', 0, 2, [X, Y, Y, leaf], 0))
                for p, s in ((0, 1), (1, 0), (1, 2), (2, 1)):
                    specs.append(('two_run_Y', p, s, [X] + [Y] * (p + 1 + s) + [leaf], 1 + p))
                specs.append(('two_run_leaf', 0, 2, [X, Y, Y, leaf], 3))
            for w in sorted(triangle - {t}):
                for kind, p, s, ns, offset in specs:
                    vertices = set().union(*map(set, es))
                    other = sorted(vertices - B - set(path))
                    remap = {v: v for v in B}
                    remap.update({v: 5 + j for j, v in enumerate(other)})
                    nextv = 5 + len(other)
                    newpath = list(range(nextv, nextv + len(ns)))
                    edges = {tuple(sorted((remap[a], remap[c]))) for a, c in es if a not in path and c not in path}
                    edges |= {(bd, v) for v, support in zip(newpath, ns) for bd in support}
                    edges |= set(zip(newpath, newpath[1:]))
                    edges.add(tuple(sorted((remap[t], newpath[0]))))
                    roots = [newpath[offset], remap[w]]
                    assert all((sum((v in e for e in edges)) == 4 for v in range(5, nextv + len(ns))))
                    assert tuple(sorted(roots)) not in edges
                    pieces = []
                    for vs in components(set(range(5, nextv + len(ns))) - set(roots), edges):
                        contacts = [[v for v in vs if tuple(sorted((r, v))) in edges] for r in roots]
                        owners = [r for r, cs in zip(roots, contacts) if cs]
                        pieces.append(dict(vertices=vs, root_contacts=contacts, owners=owners, contact_order=sorted(set().union(*map(set, contacts))), boundary_attachments=[[bd for bd in B if (bd, v) in edges] for v in vs]))
                    mixed, = [r for r in pieces if len(r['owners']) == 2]
                    assert list(map(len, mixed['root_contacts'])) == [1, 2]
                    forms.append(dict(family=family, origin=bi, tail=ti, kind=kind, prefix=p, suffix=s, edges=sorted(edges), roots=roots, pieces=pieces, original_triangle_w=w, path=newpath, marker_offset=offset))
    assert Counter((f['family'] for f in forms)) == {0: 240, 1: 96}
    assert len(forms) == 336
    return forms

def unary_domain(mask):
    """A fixed actual support chooses one S4-invariant forbidden-color rule."""
    support = [b for b in B if mask >> b & 1]
    shapes = []
    rows = []
    for ri, row in enumerate(ROWS):
        values = tuple((row[b] for b in support))
        shape = normalize(values)
        sid = next((i for i, s in enumerate(shapes) if s['shape'] == shape), None)
        if sid is None:
            stabilizers = [p for p in PERMS if all((p[c] == c for c in values))]
            choices = [None] + [c for c in range(4) if all((p[c] == c for p in stabilizers))]
            sid = len(shapes)
            shapes.append(dict(shape=shape, representative_row=ri, values=values, stabilizers=stabilizers, choices=choices))
        maps = [p for p in PERMS if tuple((p[c] for c in shapes[sid]['values'])) == values]
        choices = [None if c is None else maps[0][c] for c in shapes[sid]['choices']]
        assert all((choices == [None if c is None else p[c] for c in shapes[sid]['choices']] for p in maps))
        rows.append(dict(shape=sid, transport_permutation=maps[0], choices=choices))
    return dict(mask=mask, support=support, shapes=shapes, rows=rows)

def unary_supports():
    """All eleven continuous subsets of the ordered C5 of size at least three."""
    return [sum((1 << (i + j) % 5 for j in range(k))) for k in (3, 4, 5) for i in (range(5) if k < 5 else (0,))]

def solve(ks, target, domains, owners):
    """Exact finite CSP for one or two fixed-support unary forbidden schedules."""
    variables = [(i, j) for i, d in enumerate(domains) for j in range(len(d['shapes']))]
    allowed = {v: set(range(len(domains[v[0]]['shapes'][v[1]]['choices']))) for v in variables}
    constraints = []
    for ri, k in enumerate(ks):
        vs = [(i, d['rows'][ri]['shape']) for i, d in enumerate(domains)]
        options = []
        for indices in product(*(range(len(d['rows'][ri]['choices'])) for d in domains)):
            colors = [d['rows'][ri]['choices'][j] for d, j in zip(domains, indices)]
            survives = any((all((c is None or pair[r] != c for r, c in zip(owners, colors))) for pair in k))
            if survives == bool(target >> ri & 1):
                options.append(indices)
        constraints.append((vs, set(options), ri))
    while True:
        changed = False
        for vs, options, ri in constraints:
            options = {cs for cs in options if all((c in allowed[v] for v, c in zip(vs, cs)))}
            if not options:
                return None
            for j, v in enumerate(vs):
                new = allowed[v] & {cs[j] for cs in options}
                if new != allowed[v]:
                    changed = True
                    allowed[v] = new
        if not changed:
            break

    def visit(assign):
        if len(assign) == len(variables):
            return assign
        v = min((v for v in variables if v not in assign), key=lambda v: len(allowed[v]))
        for c in sorted(allowed[v]):
            trial = assign | {v: c}
            if all((any((all((v not in trial or trial[v] == c for v, c in zip(vs, cs))) for cs in opts)) for vs, opts, ri in constraints)):
                result = visit(trial)
                if result is not None:
                    return result
        return None
    return visit({})


def verify_coloring(edges, row, order, witness, ports=(), values=()):
    fixed = dict(zip(order, witness, strict=True))
    assert tuple(fixed[b] for b in range(5)) == row
    assert all(c in range(4) for c in fixed.values())
    assert all(fixed[a] != fixed[b] for a, b in edges)
    assert tuple(fixed[v] for v in ports) == tuple(values)


def pinned_witness(edges, row, roots, pair):
    """Independent fixed-order search on the entire core, root colors pinned."""
    vertices = sorted(B | set().union(*map(set, edges)))
    adjacent = {v: set() for v in vertices}
    for a, b in edges:
        adjacent[a].add(b)
        adjacent[b].add(a)
    fixed = dict(enumerate(row)) | dict(zip(roots, pair, strict=True))
    if any(a in fixed and b in fixed and fixed[a] == fixed[b] for a, b in edges):
        return None
    todo = [v for v in vertices if v not in fixed]

    def extend(index):
        if index == len(todo):
            return tuple(fixed[v] for v in vertices)
        v = todo[index]
        for c in range(4):
            if any(fixed.get(u) == c for u in adjacent[v]):
                continue
            fixed[v] = c
            answer = extend(index + 1)
            if answer is not None:
                return answer
        fixed.pop(v, None)
        return None

    return extend(0)


def core_relations(form):
    edges = set(map(tuple, form['edges']))
    roots = form['roots']
    order = sorted(B | set().union(*map(set, edges)))
    ports = roots + sorted({v for p in form['pieces'] for v in p['contact_order']})
    root_spokes = [[b for b in sorted(B) if tuple(sorted((b, r))) in edges]
                   for r in roots]
    for piece in form['pieces']:
        vs = set(piece['vertices'])
        piece['piece_edges'] = sorted(e for e in edges if set(e) <= B | vs)
        piece['root_incidence_edges'] = sorted(e for e in edges
            if set(e) & vs and set(e) & set(roots))
        piece['actual_support'] = sorted(set().union(*map(set, piece['boundary_attachments'])))
        piece['ordered_owner_roles'] = [i for i, cs in enumerate(piece['root_contacts']) if cs]
    rows = []
    for row in ROWS:
        saved = []
        for piece in form['pieces']:
            es = set(map(tuple, piece['piece_edges']))
            cp = piece['contact_order']
            relation = colorings(es, row, cp)
            po = sorted(B | set(piece['vertices']))
            for values, witness in relation.items():
                verify_coloring(es, row, po, witness, cp, values)
            tuples = sorted(relation)
            saved.append(dict(contact_order=cp, tuples=tuples,
                whole_piece_coloring_order=po,
                whole_piece_witnesses=[relation[t] for t in tuples]))
        joint = colorings(edges, row, ports)
        composite = {}
        for pair in PAIRS:
            if any(pair[i] == row[b] for i, bs in enumerate(root_spokes) for b in bs):
                continue
            for indices in product(*(range(len(p['tuples'])) for p in saved)):
                fixed = dict(enumerate(row)) | dict(zip(roots, pair, strict=True))
                for piece, i in zip(saved, indices, strict=True):
                    fixed.update(zip(piece['whole_piece_coloring_order'],
                                     piece['whole_piece_witnesses'][i], strict=True))
                if any(fixed[a] == fixed[b] for p in form['pieces']
                       for a, b in p['root_incidence_edges']):
                    continue
                values = tuple(fixed[v] for v in ports)
                verify_coloring(edges, row, order, tuple(fixed[v] for v in order), ports, values)
                composite.setdefault(values, indices)
        assert set(composite) == set(joint)
        tuples = sorted(joint)
        fibres = []
        for pair in PAIRS:
            indices = [i for i, values in enumerate(tuples) if values[:2] == pair]
            witness = pinned_witness(edges, row, roots, pair)
            assert bool(indices) == (witness is not None)
            if witness is not None:
                verify_coloring(edges, row, order, witness, roots, pair)
            fibres.append(dict(root_pair=pair, joint_tuple_indices=indices,
                               independently_searched_whole_core_witness=witness))
        rows.append(dict(boundary_row=row, whole_piece_relations=saved,
            joint_port_tuples=tuples,
            joint_tuple_piece_witness_indices=[composite[t] for t in tuples],
            whole_core_witnesses=[joint[t] for t in tuples],
            all_sixteen_root_fibres=fibres,
            root_pairs=sorted({t[:2] for t in tuples})))
    critical = []
    for edge in sorted(edges - FRAME):
        witnesses = colorings(edges - {edge}, Q, (), first_only=True)
        assert witnesses
        witness = next(iter(witnesses.values()))
        verify_coloring(edges - {edge}, Q, order, witness)
        critical.append(dict(deleted_edge=edge, whole_core_coloring=witness))
    form['normalized_q_critical_witnesses'] = critical
    form.update(coloring_vertex_order=order, port_order=ports,
                original_core_root_spokes=root_spokes, rows=rows)
    assert sum(1 << i for i, row in enumerate(rows) if row['root_pairs']) == 1022
    return form


def restoration_choices(form):
    edges = set(map(tuple, form['edges']))
    interior = set(form['coloring_vertex_order']) - B
    z, w = form['roots']
    zleaf = form['marker_offset'] == len(form['path']) - 1
    wdegree = sum(tuple(sorted((w, v))) in edges for v in interior)
    zchoices = [('unit_unary', None)] if zleaf else [
        ('spoke', b) for b in sorted(B) if tuple(sorted((b, z))) not in edges]
    wchoices = [('spoke', b) for b in sorted(B) if tuple(sorted((b, w))) not in edges]
    if wdegree == 2:
        wchoices.append(('unit_unary', None))
    assert wdegree in (2, 3)
    assert len(zchoices) == (1 if zleaf else 3)
    assert len(wchoices) == 4
    return list(product(zchoices, wchoices))


def verify_subdivision(edges, cert):
    branch = set(cert['branch_vertices'])
    interiors, links = [], set()
    for path in cert['paths']:
        assert len(path) >= 2 and len(path) == len(set(path))
        assert path[0] in branch and path[-1] in branch
        assert not branch.intersection(path[1:-1])
        assert all(tuple(sorted(e)) in edges for e in zip(path, path[1:]))
        interiors.extend(path[1:-1])
        links.add(tuple(sorted((path[0], path[-1]))))
    assert len(interiors) == len(set(interiors)) and len(links) == len(cert['paths'])
    if cert['model'] == 'K5':
        assert len(branch) == 5 and links == set(combinations(sorted(branch), 2))
    else:
        assert cert['model'] == 'K3,3' and len(branch) == 6
        assert any(links == {tuple(sorted((a, b))) for a in side for b in branch - set(side)}
                   for side in combinations(sorted(branch), 3))


def topology(form_id, plan_id, form, choices, masks, domains, previous):
    edges = set(map(tuple, form['edges']))
    roots = form['roots']
    owners = [r for r, (kind, _) in enumerate(choices) if kind == 'unit_unary']
    edges |= {tuple(sorted((roots[r], b))) for r, (kind, b) in enumerate(choices)
              if kind == 'spoke'}
    nextv = len(form['coloring_vertex_order'])
    contracted = []
    for r, mask in zip(owners, masks, strict=True):
        edges.add(tuple(sorted((roots[r], nextv))))
        edges |= {(b, nextv) for b in domains[mask]['support']}
        contracted.append(dict(root_role=r, contracted_unit_unary=nextv,
            actual_support=domains[mask]['support']))
        nextv += 1
    edges |= {(b, nextv) for b in sorted(B)}
    if previous is None:
        import networkx as nx
        assert nx.__version__ == '3.5', 'generation requires NetworkX 3.5'
        graph = nx.Graph(sorted(edges))
        planar, witness = nx.check_planarity(graph, counterexample=True)
        assert not planar, 'unexcluded compatible support'
        branch = sorted(v for v, degree in witness.degree() if degree != 2)
        used, paths = set(), []
        for u in branch:
            for v in sorted(witness[u]):
                if tuple(sorted((u, v))) in used:
                    continue
                path, prior = [u, v], u
                used.add(tuple(sorted((u, v))))
                while v not in branch:
                    following, = set(witness[v]) - {prior}
                    used.add(tuple(sorted((v, following))))
                    path.append(following)
                    prior, v = v, following
                paths.append(path)
        assert len(used) == witness.number_of_edges()
        cert = dict(model='K5' if len(branch) == 5 else 'K3,3',
                    branch_vertices=branch, paths=paths)
    else:
        assert set(map(tuple, previous['minor_edges'])) == edges
        cert = previous['obstruction']
    verify_subdivision(edges, cert)
    return dict(form_id=form_id, restoration_plan_id=plan_id,
        original_root_order=roots, omitted_unary_contractions=contracted,
        exterior_boundary_apex=nextv, minor_edges=sorted(edges), obstruction=cert,
        semantics='Each omitted unary is contracted only for topology; its actual fixed support is retained. No coloring replacement is asserted.')


def arbitrary_scalar_capacity(ks, target, owners):
    """Necessary per-row test before any fixed-support transport condition."""
    for ri, pairs in enumerate(ks):
        if target >> ri & 1 or not pairs:
            continue
        if not any(not any(all(c is None or pair[r] != c
                               for r, c in zip(owners, colors, strict=True))
                           for pair in pairs)
                   for colors in product([None, 0, 1, 2, 3], repeat=len(owners))):
            return ri
    return None


def actual_unary_controls(forms):
    """Whole original unary pieces; complete tuple joins in one literal frame."""
    representatives = {}
    for fi, form in enumerate(forms):
        for pi, choices in enumerate(restoration_choices(form)):
            owners = tuple(r for r, (kind, _) in enumerate(choices) if kind == 'unit_unary')
            representatives.setdefault(owners, (fi, pi, form, choices))
    assert set(representatives) == {(), (0,), (1,), (0, 1)}
    templates = [dict(kind='singleton', supports=[[0, 1, 2]]),
                 dict(kind='two_point_path', supports=[[0, 1], [0, 1, 2]]),
                 dict(kind='three_point_path', supports=[[0, 1], [0, 1], [0, 1, 2]])]
    records, checks, transports = [], 0, 0
    for owners, (fi, pi, form, choices) in sorted(representatives.items()):
        for picks in product(range(len(templates)), repeat=len(owners)):
            edges = set(map(tuple, form['edges']))
            roots, ports = form['roots'], form['port_order']
            edges |= {tuple(sorted((roots[r], b))) for r, (kind, b) in enumerate(choices)
                      if kind == 'spoke'}
            original_core = set(edges)
            nextv = len(form['coloring_vertex_order'])
            pieces = []
            for role, pick in zip(owners, picks, strict=True):
                template = templates[pick]
                vertices = list(range(nextv, nextv + len(template['supports'])))
                nextv += len(vertices)
                es = set(FRAME) | set(zip(vertices, vertices[1:]))
                es |= {(b, v) for v, support in zip(vertices, template['supports'], strict=True)
                       for b in support}
                edges |= es | {tuple(sorted((roots[role], vertices[0])))}
                pieces.append(dict(identity=template['kind'], root_role=role,
                    vertices=vertices, ordered_distinct_contact=[vertices[0]],
                    actual_support=sorted(set().union(*map(set, template['supports']))),
                    boundary_attachments=template['supports'], piece_edges=sorted(es)))
            assert all(sum(v in e for e in edges) == (5 if v in roots else 4)
                       for v in range(5, nextv))
            contacts = [p['ordered_distinct_contact'][0] for p in pieces]
            rows, role_relations = [], [[] for _ in pieces]
            for ri, row in enumerate(ROWS):
                relations, piece_saved = [], []
                for j, piece in enumerate(pieces):
                    es = set(map(tuple, piece['piece_edges']))
                    relation = colorings(es, row, piece['ordered_distinct_contact'])
                    tuples = sorted(relation)
                    allowed = {t[0] for t in tuples}
                    forbidden = [c for c in range(4) if not any(c != a for a in allowed)]
                    assert len(forbidden) <= 1
                    role_relations[j].append(allowed)
                    piece_saved.append(dict(contact_tuples=tuples,
                        whole_piece_coloring_order=sorted(B | set(piece['vertices'])),
                        whole_piece_witnesses=[relation[t] for t in tuples],
                        forbidden_root_colors=forbidden))
                    relations.append(relation)
                core = colorings(original_core, row, ports)
                joined = {t + tuple(u[0] for u in us)
                    for t in core for us in product(*(sorted(rel) for rel in relations))
                    if all(t[p['root_role']] != u[0] for p, u in zip(pieces, us, strict=True))}
                actual = colorings(edges, row, ports + contacts)
                assert set(actual) == joined
                for values, witness in actual.items():
                    verify_coloring(edges, row, list(range(nextv)), witness, ports + contacts, values)
                tuples = sorted(actual)
                rows.append(dict(boundary_row=row, original_unit_unary_relations=piece_saved,
                    full_original_graph_joint_tuples=tuples,
                    whole_original_graph_witnesses=[actual[t] for t in tuples]))
                checks += 1
            for piece, relations in zip(pieces, role_relations, strict=True):
                for i, row in enumerate(ROWS):
                    for j, other in enumerate(ROWS):
                        for perm in PERMS:
                            if all(perm[row[b]] == other[b] for b in piece['actual_support']):
                                assert {perm[c] for c in relations[i]} == relations[j]
                                transports += 1
            records.append(dict(form_id=fi, restoration_plan_id=pi,
                original_root_order=roots, original_unit_unary_pieces=pieces,
                full_original_graph_edges=sorted(edges), full_port_order=ports + contacts,
                whole_original_graph_coloring_order=list(range(nextv)), rows=rows,
                disk_or_Sigma_criticality_claimed=False))
    assert len(records) == 16 and checks == 160
    return dict(graphs=records, whole_original_graph_row_joins=checks,
                whole_unary_S4_transport_checks=transports)


def actual_long_controls(forms):
    """Grow positive marker-side runs by two; zero segments and markers stay fixed."""
    representatives = {}
    for fi, form in enumerate(forms):
        representatives.setdefault((form['kind'], form['prefix'], form['suffix']), (fi, form))
    records, checks = [], 0
    for _, (fi, form) in sorted(representatives.items()):
        edges = set(map(tuple, form['edges']))
        path, marker = form['path'], form['marker_offset']
        if form['family'] == 0:
            segments = [path[:marker], path[marker + 1:-1]] if marker < len(path) - 1 else [path[:-1]]
        elif form['kind'] == 'two_run_X':
            segments = [path[1:-1]]
        elif form['kind'] == 'two_run_Y':
            segments = [path[1:marker], path[marker + 1:-1]]
        else:
            segments = [path[1:-1]]
        grow = {segment[0] for segment in segments if segment}
        groups, nextv = {b: [b] for b in sorted(B)}, 5
        for v in form['coloring_vertex_order'][5:]:
            groups[v] = list(range(nextv, nextv + (3 if v in grow else 1)))
            nextv += len(groups[v])
        grown = set(FRAME)
        for v, group in groups.items():
            if v in B:
                continue
            grown |= set(zip(group, group[1:]))
            grown |= {(b, u) for b in sorted(B) if (b, v) in edges for u in group}
        for a, b in edges:
            if a not in B:
                grown.add(tuple(sorted((groups[a][-1], groups[b][0]))))
        inverse = {u: v for v, group in groups.items() for u in group}
        quotient = {tuple(sorted((inverse[a], inverse[b]))) for a, b in grown
                    if inverse[a] != inverse[b]}
        assert quotient == edges
        triangle = [5, 6, 7]
        assert all(len(groups[v]) == 1 for v in triangle + form['roots'])
        assert all(sum(v in e for e in grown) == 4 for v in range(5, nextv))
        ports = triangle + [form['roots'][0]]
        longports = [groups[v][0] for v in ports]
        rows = []
        for row in ROWS:
            short = colorings(edges, row, ports)
            long = colorings(grown, row, longports)
            assert set(short) == set(long)
            tuples = sorted(long)
            for values, witness in long.items():
                verify_coloring(grown, row, list(range(nextv)), witness, longports, values)
            rows.append(dict(boundary_row=row, triangle_and_marker_joint_tuples=tuples,
                             actual_long_graph_witnesses=[long[t] for t in tuples]))
            checks += 1
        records.append(dict(form_id=fi, marker_preserved_as_singleton=groups[form['roots'][0]],
            positive_segments_grown=segments, original_triangle_and_marker_order=ports,
            long_triangle_and_marker_order=longports, actual_long_edges=sorted(grown),
            actual_long_coloring_order=list(range(nextv)),
            boundary_fixed_minor_branch_sets=[groups[v] for v in form['coloring_vertex_order']], rows=rows))
    assert len(records) == 12 and checks == 120
    return dict(graphs=records, marked_joint_transfer_row_comparisons=checks)


def build(saved=None):
    index = {r: i for i, r in enumerate(ROWS)}
    orbits = {str(mask): sorted({sum(1 << index[normalize(
        [r[(sign * j + shift) % 5] for j in range(5)])]
        for i, r in enumerate(ROWS) if mask >> i & 1)
        for sign in (-1, 1) for shift in range(5)}) for mask in (933, 941)}
    targets = sorted(set().union(*map(set, orbits.values())))
    domains = {m: unary_domain(m) for m in unary_supports()}
    forms = [core_relations(f) for f in marked_forms()]
    counts = Counter()
    subdivisions, subdivision_indices = [], {}
    for fi, form in enumerate(forms):
        roots = form['roots']
        plans = []
        for pi, choices in enumerate(restoration_choices(form)):
            counts['restoration_plans'] += 1
            owners = [r for r, (kind, _) in enumerate(choices) if kind == 'unit_unary']
            ks, rows = [], []
            for row in form['rows']:
                boundary = row['boundary_row']
                indices = [i for i, values in enumerate(row['joint_port_tuples'])
                    if all(kind != 'spoke' or values[r] != boundary[b]
                           for r, (kind, b) in enumerate(choices))]
                pairs = sorted({tuple(row['joint_port_tuples'][i][:2]) for i in indices})
                ks.append(pairs)
                rows.append(dict(surviving_core_joint_tuple_indices=indices, root_pairs=pairs))
                for i in indices:
                    witness = row['whole_core_witnesses'][i]
                    es = set(map(tuple, form['edges'])) | {
                        tuple(sorted((roots[r], b))) for r, (kind, b) in enumerate(choices) if kind == 'spoke'}
                    verify_coloring(es, boundary, form['coloring_vertex_order'], witness)
            tests = []
            for target in targets:
                counts['target_comparisons'] += 1
                test = dict(target_mask=target)
                empty = next((ri for ri, k in enumerate(ks) if target >> ri & 1 and not k), None)
                if empty is not None:
                    counts['accepted_empty_exclusions'] += 1
                    test.update(exclusion='target_accepts_empty_restored_core_row', row_index=empty)
                elif not owners:
                    sigma = sum(1 << ri for ri, k in enumerate(ks) if k)
                    assert sigma != target
                    counts['no_omitted_unary_sigma_mismatches'] += 1
                    test.update(exclusion='no_omitted_unary_exact_sigma_mismatch', exact_sigma=sigma)
                else:
                    capacity = arbitrary_scalar_capacity(ks, target, owners)
                    if capacity is not None:
                        counts['unary_capacity_exclusions'] += 1
                        test.update(exclusion='unit_unary_empty_or_singleton_capacity', row_index=capacity)
                    else:
                        counts['fixed_support_comparisons'] += 1
                        checks = []
                        for masks in product(domains, repeat=len(owners)):
                            counts['fixed_support_queries'] += 1
                            assignment = solve(ks, target, [domains[m] for m in masks], owners)
                            check = dict(ordered_actual_support_masks=masks)
                            if assignment is None:
                                counts['incompatible_supports'] += 1
                                check.update(status='fixed_support_transport_incompatible')
                            else:
                                counts['compatible_nondisk_supports'] += 1
                                key = fi, pi, masks
                                if key not in subdivision_indices:
                                    si = len(subdivisions)
                                    previous = None if saved is None else saved['subdivisions'][si]
                                    subdivisions.append(topology(fi, pi, form, choices, masks, domains, previous))
                                    subdivision_indices[key] = si
                                check.update(status='compatible_but_explicitly_nondisk',
                                    shape_choice_assignment=[dict(unit_unary_role=i, shape=j, choice=assignment[i, j])
                                                             for i, j in sorted(assignment)],
                                    subdivision_index=subdivision_indices[key])
                            checks.append(check)
                        test.update(exclusion='fixed_support_transport_or_nondisk', support_tests=checks)
                tests.append(test)
            plans.append(dict(ordered_root_restorations=[dict(root_role=r, kind=kind,
                restored_boundary_neighbor=b) for r, (kind, b) in enumerate(choices)],
                ordered_omitted_unit_unary_owner_roles=owners, rows=rows, target_comparisons=tests))
        form['restoration_plans'] = plans
    counts.update(inherited_uniform_templates=18, inherited_two_run_contexts=8,
        marked_uniform_cores=240, marked_two_run_cores=96, marked_cores=len(forms),
        whole_core_row_queries=3360, pinned_root_fibres=53760,
        whole_piece_row_relations=sum(len(f['pieces']) * 10 for f in forms),
        explicit_subdivisions=len(subdivisions),
        subdivision_paths=sum(len(s['obstruction']['paths']) for s in subdivisions), residuals=0)
    expected = dict(restoration_plans=3584, target_comparisons=35840,
        accepted_empty_exclusions=29804, no_omitted_unary_sigma_mismatches=3404,
        unary_capacity_exclusions=2480, fixed_support_comparisons=152,
        fixed_support_queries=7832, incompatible_supports=6976, compatible_nondisk_supports=856)
    assert all(counts[k] == v for k, v in expected.items()), dict(counts)
    counts.update({f'subdivision_{k}': v for k, v in Counter(s['obstruction']['model'] for s in subdivisions).items()})
    if saved is not None:
        assert len(saved['subdivisions']) == len(subdivisions)
    return dict(schema=1,
        scope='U3 sole mixed12 marked single-triangle finite necessity controls in the inherited minimal core grammar. Arbitrary-length compression and source coverage remain separate paper dependencies.',
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in INPUTS},
        source_sha256={str(Path(__file__).resolve().relative_to(ROOT)): sha256(Path(__file__).resolve().read_bytes()).hexdigest()},
        pattern_order=ROWS, normalized_rejected_row=Q, target_D5_orbits=orbits,
        fixed_actual_unit_unary_support_domains=list(domains.values()),
        family_names={0: 'inherited_uniform_single_triangle', 1: 'inherited_single_triangle_two_runs'},
        forms=forms, subdivisions=subdivisions,
        actual_unit_unary_gluing_controls=actual_unary_controls(forms),
        actual_long_marker_controls=actual_long_controls(forms), summary=dict(sorted(counts.items())),
        witness_semantics='Each original piece has its complete contact relation and a witness on the entire piece. All sixteen ordered root fibres are joined in the one literal boundary color frame and independently checked by whole-core pinned search. Every joint tuple references whole-piece witness indices. Restored spokes filter these same joint tuples; omitted unary supports remain fixed across rows and obey S4 transport. Unary contractions are used only in explicit topology minors.',
        paper_dependencies=['Inherited degree-four single-triangle grammar with nonbranching tails',
            'Marker-preserving positive-run parity compression with zero runs fixed',
            'Original nonleaf z has one unary; extra unary excluded by unary shields and w-star faces',
            'Each omitted unit unary has continuous actual support of size at least three and empty/singleton forbidden root color'],
        trust_boundary='Finite grammar audit only: no independent source census, no claim that abstract unary schedules are realizable, no new Lean theorem, no arbitrary-size theorem supplied by computation.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    saved = json.loads(OUT.read_text()) if args.check else None
    data = build(saved)
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'
    if args.check:
        assert OUT.read_text() == encoded, 'certificate differs; preserve historical inputs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print(json.dumps(dict(status='checked' if args.check else 'written', **data['summary']), sort_keys=True))


if __name__ == '__main__':
    main()
