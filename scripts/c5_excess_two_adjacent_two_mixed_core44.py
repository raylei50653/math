#!/usr/bin/env python3
"""U2: omit an original mixed11 at adjacent roots with two mixed pieces.

Rebuild the inherited triangle-marker domain from three small saved inputs.
Replay uses only the standard library: full graph colorings, fixed-support
S4 transport, and explicit subdivisions. NetworkX 3.5 is used only when
generating a new subdivision. Paper supplies arbitrary-size coverage.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_adjacent_two_mixed_core44/observations.json'
INPUTS = [ROOT / 'artifacts/c5_triangle_branches/observations.json',
          ROOT / 'artifacts/c5_triangle_path_reduction/observations.json',
          ROOT / 'artifacts/c5_two_triangle_blocks/observations.json']
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


def normal_forms():
    branches, switches, double = [json.loads(p.read_text()) for p in INPUTS]
    forms = []

    def add(edges, family, origin, rotation=None):
        es = {tuple(sorted(e)) for e in edges}
        order = sorted(set().union(*map(set, es)))
        assert order == list(range(len(order)))
        if rotation is not None:
            rotation_check(es, rotation)
        forms.append(dict(edges=sorted(es), family=family, input_origin=origin,
                          coloring_vertex_order=order))

    for i, old in enumerate(branches['disk_templates']):
        add(old['edges'], 'single_triangle', [0, i], old['apex_rotation'])
    for i, old in sorted(enumerate(switches['normal_forms']), key=lambda t: t[1]['base']):
        add(old['edges'], 'single_triangle_two_runs', [1, i],
            old['topology']['apex_rotation'])
    bare_count = 0
    for missing in combinations(range(3), 2):
        supports = [tuple(sorted((a, b))) for a in sorted(B) for b in sorted(B)
                    if Q[a] == missing[0] and Q[b] == missing[1]]
        for ns in product(supports, repeat=3):
            es = FRAME | {(5, 6), (5, 7), (6, 7)}
            es |= {(b, 5+i) for i, support in enumerate(ns) for b in support}
            sigma = sum(1 << ri for ri, row in enumerate(ROWS)
                        if colorings(es, row, (), first_only=True))
            if sigma & T4 == T4:
                assert sigma == 1022
                add(es, 'bare_triangle', ['bare', bare_count])
            bare_count += 1
    assert bare_count == 80
    for i, old in enumerate(double['disk_templates']):
        es = set(map(tuple, old['edges']))
        sigma = sum(1 << ri for ri, row in enumerate(ROWS)
                    if colorings(es, row, (), first_only=True))
        assert sigma == old['sigma']
        if sigma == 1022:
            add(es, 'double_triangle', [2, i], old['apex_rotation'])
    assert Counter(f['family'] for f in forms) == dict(
        single_triangle=18, single_triangle_two_runs=8, bare_triangle=36, double_triangle=64)
    return forms


def forbidden_sets():
    fs = [()] + [(p,) for p in PAIRS]
    fs += [p for p in combinations(PAIRS, 2)
           if len({a for a, _ in p}) == len({b for _, b in p}) == 2]
    assert len(fs) == 89
    return fs


def support_domain(mask, fs):
    support = [b for b in sorted(B) if mask >> b & 1]
    shapes, transports = [], []
    for ri, row in enumerate(ROWS):
        values = tuple(row[b] for b in support)
        shape = normalize(values)
        sid = next((i for i, s in enumerate(shapes) if s['shape'] == shape), None)
        if sid is None:
            stabilizers = [p for p in PERMS if all(p[c] == c for c in values)]
            choices = [f for f in fs if all(
                tuple(sorted((p[a], p[b]) for a, b in f)) == f for p in stabilizers)]
            sid = len(shapes)
            shapes.append(dict(shape=shape, representative_row=ri, values=values,
                               stabilizers=stabilizers, choices=choices))
        rep = shapes[sid]
        maps = [p for p in PERMS if tuple(p[c] for c in rep['values']) == values]
        choices = []
        for f in rep['choices']:
            images = {tuple(sorted((p[a], p[b]) for a, b in f)) for p in maps}
            assert len(images) == 1
            choices.append(images.pop())
        transports.append(dict(shape=sid, permutation=maps[0], forbidden_choices=choices))
    return dict(support_mask=mask, actual_support=support, shapes=shapes, rows=transports)


def support_test(ks, target, domain):
    allowed = [set(range(len(s['choices']))) for s in domain['shapes']]
    row_constraints = []
    for ri, (k, t) in enumerate(zip(ks, domain['rows'], strict=True)):
        choices = {i for i, f in enumerate(t['forbidden_choices'])
                   if bool(set(k)-set(f)) == bool(target >> ri & 1)}
        allowed[t['shape']] &= choices
        row_constraints.append(sorted(choices))
    empty = next((i for i, a in enumerate(allowed) if not a), None)
    if empty is not None:
        conflicts = [dict(row_index=ri, allowed_choice_indices=row_constraints[ri])
                     for ri, t in enumerate(domain['rows']) if t['shape'] == empty]
        assert not set.intersection(*(set(c['allowed_choice_indices']) for c in conflicts))
        return dict(support_mask=domain['support_mask'], empty_shape=empty,
                    conflicting_row_constraints=conflicts)
    assignment = [min(a) for a in allowed]
    schedule = [t['forbidden_choices'][assignment[t['shape']]] for t in domain['rows']]
    assert sum(1 << i for i, (k, f) in enumerate(zip(ks, schedule, strict=True))
               if set(k)-set(f)) == target
    return dict(support_mask=domain['support_mask'], shape_assignment=assignment,
                possible_choice_indices=list(map(sorted, allowed)), forbidden_schedule=schedule)


def verify_subdivision(edges, cert):
    branch = set(cert['branch_vertices'])
    paths = cert['paths']
    interiors, links = [], set()
    for path in paths:
        assert len(path) >= 2 and len(path) == len(set(path))
        assert path[0] in branch and path[-1] in branch
        assert not branch.intersection(path[1:-1])
        assert all(tuple(sorted(e)) in edges for e in zip(path, path[1:]))
        interiors.extend(path[1:-1])
        links.add(tuple(sorted((path[0], path[-1]))))
    assert len(interiors) == len(set(interiors)) and len(links) == len(paths)
    if cert['model'] == 'K5':
        assert len(branch) == 5 and links == set(combinations(sorted(branch), 2))
    else:
        assert cert['model'] == 'K3,3' and len(branch) == 6
        assert any(links == {tuple(sorted((a, b))) for a in side for b in branch-set(side)}
                   for side in combinations(sorted(branch), 3))


def topology(form_id, form, roots, support, saved):
    d = len(form['coloring_vertex_order'])
    apex = d+1
    edges = set(map(tuple, form['edges'])) | {(r, d) for r in roots}
    edges |= {(b, d) for b in support} | {(b, apex) for b in B}
    if saved is None:
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
                path, previous = [u, v], u
                used.add(tuple(sorted((u, v))))
                while v not in branch:
                    following, = set(witness[v])-{previous}
                    used.add(tuple(sorted((v, following))))
                    path.append(following)
                    previous, v = v, following
                paths.append(path)
        assert len(used) == witness.number_of_edges()
        cert = dict(model='K5' if len(branch) == 5 else 'K3,3',
                    branch_vertices=branch, paths=paths)
    else:
        assert set(map(tuple, saved['minor_edges'])) == edges
        cert = saved['obstruction']
    verify_subdivision(edges, cert)
    return dict(form_id=form_id, original_root_order=roots, actual_support=support,
                contracted_original_D_vertex=d, exterior_boundary_apex=apex,
                minor_edges=sorted(edges), obstruction=cert,
                semantics='contract all original D only for topology; no coloring replacement')


def gluing_controls(forms, fs):
    """Whole original D witnesses, including shared and distinct contacts."""
    templates = [
        dict(kind='shared_singleton', inner=[], supports=[[0, 2]], contacts=[0, 0]),
        dict(kind='shared_edge', inner=[(0, 1)], supports=[[0], [1, 3, 4]], contacts=[0, 0]),
        dict(kind='distinct_edge', inner=[(0, 1)], supports=[[0, 2], [1, 3]], contacts=[0, 1]),
        dict(kind='distinct_path', inner=[(0, 1), (1, 2)],
             supports=[[0, 2], [0, 2], [1, 3]], contacts=[0, 2]),
        dict(kind='distinct_triangle', inner=[(0, 1), (0, 2), (1, 2)],
             supports=[[0], [1], [2, 4]], contacts=[0, 1])]
    records, joins, transports = [], 0, 0
    for fi in (0, 18, 26, 125):
        form = forms[fi]
        edges = set(map(tuple, form['edges']))
        mark = form['marked_cores'][0]
        roots, ports = mark['original_root_order'], mark['port_order']
        for template in templates:
            vs = list(range(len(form['coloring_vertex_order']),
                            len(form['coloring_vertex_order'])+len(template['supports'])))
            de = {tuple(sorted((vs[a], vs[b]))) for a, b in template['inner']}
            de |= {(b, v) for v, support in zip(vs, template['supports'], strict=True) for b in support}
            contacts = [vs[i] for i in template['contacts']]
            dp = sorted(set(contacts))
            attached = edges | de | {(r, c) for r, c in zip(roots, contacts, strict=True)}
            assert all(sum(v in e for e in attached) == 4 for v in vs)
            assert all(sum(r in e for e in attached) == 5 for r in roots)
            support = sorted(set().union(*map(set, template['supports'])))
            rows, role_relations = [], []
            for ri, row in enumerate(ROWS):
                dw = colorings(de, row, dp)
                assert dw
                role_relation = {tuple(t[dp.index(c)] for c in contacts) for t in dw}
                role_relations.append(role_relation)
                forbidden = tuple(p for p in PAIRS if not any(
                    p[0] != c and p[1] != d for c, d in role_relation))
                assert forbidden in fs
                core = mark['rows'][ri]['joint_port_tuples']
                joined = {tuple(t)+u for t in core for u in dw
                          if t[0] != u[dp.index(contacts[0])]
                          and t[1] != u[dp.index(contacts[1])]}
                actual = colorings(attached, row, ports+dp)
                assert set(actual) == joined
                assert bool(actual) == bool(set(map(tuple, mark['rows'][ri]['root_pairs']))-set(forbidden))
                rows.append(dict(D_contact_tuples=sorted(dw),
                    D_complete_coloring_order=sorted(B | set(vs)),
                    D_complete_witnesses=[dw[t] for t in sorted(dw)],
                    ordered_D_endpoint_roles=sorted(role_relation), forbidden_pairs=forbidden,
                    full_joint_tuples=sorted(actual),
                    original_G_complete_witnesses=[actual[t] for t in sorted(actual)]))
                joins += 1
            for i, r in enumerate(ROWS):
                for j, s in enumerate(ROWS):
                    for p in PERMS:
                        if all(p[r[b]] == s[b] for b in support):
                            assert {(p[a], p[b]) for a, b in role_relations[i]} == role_relations[j]
                            transports += 1
            records.append(dict(form_id=fi, original_root_order=roots,
                D_identity=template['kind'], D_vertices=vs, ordered_D_contacts=contacts,
                unique_D_contact_order=dp, D_edges=sorted(de),
                D_actual_support=support, D_boundary_attachments=template['supports'],
                full_original_G_edges=sorted(attached),
                full_original_G_coloring_order=list(range(vs[-1]+1)),
                full_port_order=ports+dp, rows=rows,
                disk_or_Sigma_criticality_claimed=False))
    assert len(records) == 20 and joins == 200
    collision = [((0, 0), (1, 1)), ((0, 1), (1, 0))]
    joins_by_relation = [[(c, d) for c, d in rel if c != 0 and d != 1] for rel in collision]
    assert joins_by_relation == [[], [(1, 0)]]
    return dict(graphs=records, complete_original_G_row_joins=joins,
        whole_D_S4_transport_checks=transports,
        abstract_marginal_collision=dict(root_pair=[0, 1], endpoint_relations=collision,
            endpoint_marginals=[[0, 1], [0, 1]], surviving_endpoint_tuples=joins_by_relation,
            source_realization_claimed=False))


def long_controls(forms):
    """Grow actual uniform runs by two; keep all triangle markers singleton."""
    records, checks = [], 0
    for fi, form in enumerate(forms):
        if not form['family'].startswith('single_triangle'):
            continue
        edges = set(map(tuple, form['edges']))
        tri = {5, 6, 7}
        grow = set()
        for vs in components(set(form['coloring_vertex_order'])-B-tri, edges):
            path, previous = [], None
            start, = [v for v in vs if any(tuple(sorted((v, t))) in edges for t in tri)]
            current = start
            while True:
                path.append(current)
                following = [v for v in vs if v != previous and tuple(sorted((v, current))) in edges]
                if not following:
                    break
                following_vertex, = following
                previous, current = current, following_vertex
            assert set(path) == set(vs)
            # In the two-run domain X must remain one point. Grow only Y.
            grow.add(path[-2])
        branch_sets, next_vertex = {b: [b] for b in B}, 5
        for v in form['coloring_vertex_order'][5:]:
            size = 3 if v in grow else 1
            branch_sets[v] = list(range(next_vertex, next_vertex+size))
            next_vertex += size
        grown = set(FRAME)
        for v, group in branch_sets.items():
            if v in B:
                continue
            grown |= set(zip(group, group[1:]))
            grown |= {(b, w) for b in B if (b, v) in edges for w in group}
        for a, b in edges:
            if a not in B:
                grown.add((branch_sets[a][-1], branch_sets[b][0]))
        inverse = {w: v for v, group in branch_sets.items() for w in group}
        quotient = {tuple(sorted((inverse[a], inverse[b]))) for a, b in grown
                    if inverse[a] != inverse[b]}
        assert quotient == edges
        assert all(branch_sets[v] == [v] for v in tri)
        assert all(sum(v in e for e in grown) == 4 for v in range(5, next_vertex))
        rows = []
        for row in ROWS:
            short = colorings(edges, row, sorted(tri))
            long = colorings(grown, row, sorted(tri))
            assert set(short) == set(long)
            rows.append(dict(triangle_joint_tuples=sorted(long),
                             actual_long_coloring_witnesses=[long[t] for t in sorted(long)]))
            checks += 1
        records.append(dict(form_id=fi, actual_long_edges=sorted(grown),
            long_coloring_vertex_order=list(range(next_vertex)),
            boundary_fixed_minor_branch_sets=[branch_sets[v] for v in range(len(branch_sets))],
            singleton_triangle_order=sorted(tri), rows=rows))
    assert len(records) == 26 and checks == 260
    return dict(actual_long_graphs=records, complete_triangle_joint_comparisons=checks)


def build(saved=None):
    forms, fs = normal_forms(), forbidden_sets()
    domains = [support_domain(m, fs) for m in range(32)]
    row_index = {r: i for i, r in enumerate(ROWS)}
    orbits = {str(mask): sorted({sum(1 << row_index[normalize(
        [row[(s*j+t) % 5] for j in range(5)])]
        for ri, row in enumerate(ROWS) if mask >> ri & 1)
        for s in (-1, 1) for t in range(5)}) for mask in (933, 941)}
    counts, minors, minor_indices = Counter(), [], {}
    for fi, form in enumerate(forms):
        edges, order = set(map(tuple, form['edges'])), form['coloring_vertex_order']
        interior = set(order)-B
        assert all(sum(v in e for e in edges) == 4 for v in interior)
        assert components(interior, edges) == [sorted(interior)]
        triangles = [t for t in combinations(sorted(interior), 3)
                     if all(e in edges for e in combinations(t, 2))]
        pairs = sorted({e for t in triangles for e in combinations(t, 2)})
        critical = []
        for edge in sorted(edges-FRAME):
            witnesses = colorings(edges-{edge}, Q, (), first_only=True)
            assert witnesses
            critical.append(dict(edge=edge, coloring=next(iter(witnesses.values()))))
        form['q_critical_witnesses'] = critical
        marked = []
        for roots in pairs:
            counts['marked_cores'] += 1
            regions = []
            for vs in components(interior-set(roots), edges):
                contacts = [[v for v in vs if tuple(sorted((r, v))) in edges] for r in roots]
                attachments = [[b for b in sorted(B) if (b, v) in edges] for v in vs]
                regions.append(dict(vertices=vs, root_contacts=contacts,
                    owners=[r for r, cs in zip(roots, contacts, strict=True) if cs],
                    contact_order=sorted(set().union(*map(set, contacts))),
                    boundary_attachments=attachments,
                    actual_support=sorted(set().union(*map(set, attachments))),
                    incident_edges=sorted(e for e in edges if set(e).intersection(vs))))
            mixed, = [r for r in regions if len(r['owners']) == 2]
            assert mixed['root_contacts'][0] == mixed['root_contacts'][1]
            assert len(mixed['root_contacts'][0]) == 1
            ports = list(roots)+sorted({v for r in regions for v in r['contact_order']})
            rows, ks = [], []
            for row in ROWS:
                joint = colorings(edges, row, ports)
                root_pairs = sorted({t[:2] for t in joint})
                assert root_pairs == sorted(colorings(edges, row, roots))
                rows.append(dict(joint_port_tuples=sorted(joint), root_pairs=root_pairs,
                                 full_coloring_witnesses=[joint[t] for t in sorted(joint)]))
                ks.append(root_pairs)
                counts['full_joint_row_checks'] += 1
            assert sum(1 << ri for ri, k in enumerate(ks) if k) == 1022
            tests = []
            for target in sorted(set().union(*map(set, orbits.values()))):
                counts['target_comparisons'] += 1
                empty = [i for i, k in enumerate(ks) if target >> i & 1 and not k]
                capacity = [i for i, k in enumerate(ks) if not (target >> i & 1) and k
                            and tuple(map(tuple, k)) not in fs]
                test = dict(target_mask=target)
                if empty:
                    counts['accepted_empty_exclusions'] += 1
                    test.update(exclusion='target_accepts_empty_core_row', row_index=empty[0])
                elif capacity:
                    counts['capacity_exclusions'] += 1
                    test.update(exclusion='mixed11_forbidden_capacity', row_index=capacity[0])
                else:
                    counts['fixed_support_comparisons'] += 1
                    checks = []
                    for domain in domains:
                        counts['support_queries'] += 1
                        check = support_test(ks, target, domain)
                        if 'empty_shape' in check:
                            counts['incompatible_supports'] += 1
                        else:
                            counts['compatible_nondisk_supports'] += 1
                            key = (fi, roots, domain['support_mask'])
                            if key not in minor_indices:
                                idx = len(minors)
                                previous = None if saved is None else saved['subdivisions'][idx]
                                minors.append(topology(fi, form, roots, domain['actual_support'], previous))
                                minor_indices[key] = idx
                            check['subdivision_index'] = minor_indices[key]
                        checks.append(check)
                    test.update(exclusion='fixed_support_transport_or_nondisk', support_tests=checks)
                tests.append(test)
            marked.append(dict(original_root_order=roots, retained_original_pieces=regions,
                               port_order=ports, rows=rows, target_comparisons=tests))
        form['marked_cores'] = marked
    counts.update(normal_forms=len(forms), explicit_subdivisions=len(minors), residuals=0,
                  subdivision_paths=sum(len(m['obstruction']['paths']) for m in minors))
    assert dict(counts) == dict(normal_forms=126, marked_cores=570, full_joint_row_checks=5700,
        target_comparisons=5700, accepted_empty_exclusions=1710, capacity_exclusions=3927,
        fixed_support_comparisons=63, support_queries=2016, incompatible_supports=1917,
        compatible_nondisk_supports=99, explicit_subdivisions=27, subdivision_paths=246, residuals=0), dict(counts)
    counts.update({f'subdivision_{k}': v for k, v in Counter(
        m['obstruction']['model'] for m in minors).items()})
    if saved is not None:
        assert len(saved['subdivisions']) == len(minors)
    return dict(schema=1,
        scope='U2 core44 only, complete Sigma933/941 D5 images; paper covers arbitrary size',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                       for p in INPUTS+[Path(__file__).resolve()]},
        pattern_order=ROWS, normalized_rejected_row=Q, target_D5_orbits=orbits,
        forbidden_pair_domain=fs, fixed_actual_support_domains=domains,
        forms=forms, subdivisions=minors, actual_mixed_gluing_controls=gluing_controls(forms, fs),
        actual_long_triangle_controls=long_controls(forms), summary=dict(sorted(counts.items())),
        trust_boundary='inherited all-degree-four classification and triangle run coverage; no new Lean theorem or source realization')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    saved = json.loads(OUT.read_text()) if args.check else None
    data = build(saved)
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':'))+'\n'
    if args.check:
        assert OUT.read_text() == encoded, 'certificate differs; preserve historical inputs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(encoded)
    print(json.dumps(dict(status='checked' if args.check else 'written', **data['summary']), sort_keys=True))


if __name__ == '__main__':
    main()
