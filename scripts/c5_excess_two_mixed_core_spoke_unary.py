#!/usr/bin/env python3
"""Retained mixed core: one original spoke and one original unary omitted.

The unary stays arbitrary. Its exact gluing operator is checked first; fixed
actual support and S4 equivariance then force non-disk contracted-star minors.
This is an inherited necessary domain, not a source graph census or Lean proof.
Run with: uv run --with networkx==3.5 python scripts/<this file> [--check]
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import networkx as nx

from c5_independent_support_capacity import B, FRAME, ROWS, T4, U, normalize
from c5_941_two_spoke import Q4, relabel_mask, search
from c5_excess_two_mixed_core_spokes import (
    encoded, load_forms, original_regions,
    validate_witness, witnesses,
)
from c5_excess_two_triangle_edge import graph
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_spoke_unary/observations.json'
# Explicit inputs also give the artifact manager its producer rebuild order.
BRANCHES = ROOT / 'artifacts/c5_triangle_branches/observations.json'
PATHS = ROOT / 'artifacts/c5_triangle_path_reduction/observations.json'
DOUBLE = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'
PERMUTATIONS = tuple(permutations(range(4)))


def support_domain(mask):
    """One actual support, one local shape variable, all literal transports."""
    support = [b for b in sorted(B) if mask >> b & 1]
    local, representatives, rows = {}, [], []
    for ri, row in enumerate(ROWS):
        values = tuple(row[b] for b in support)
        shape = normalize(values)
        if shape not in local:
            local[shape] = len(representatives)
            stabilizers = [p for p in PERMUTATIONS
                           if tuple(p[c] for c in values) == values]
            choices = [-1] + [c for c in sorted(U)
                              if all(p[c] == c for p in stabilizers)]
            assert choices == [-1] + sorted(set(values) if len(set(values)) <= 2 else U)
            representatives.append(dict(shape=shape, row_index=ri,
                literal_colors=values, choices=choices))
        sid = local[shape]
        base = representatives[sid]['literal_colors']
        maps = [p for p in PERMUTATIONS if tuple(p[c] for c in base) == values]
        assert maps
        transported = []
        for c in representatives[sid]['choices']:
            outputs = {-1} if c == -1 else {p[c] for p in maps}
            assert len(outputs) == 1
            transported.append(outputs.pop())
        rows.append(dict(local_shape=sid, literal_forbidden_choices=transported,
                         color_permutation=maps[0], all_color_maps=len(maps)))
    return dict(id=mask, actual_boundary_support=support,
        local_shapes=representatives, row_transports=rows,
        choice_semantics='-1 means empty forbidden set, c means singleton {c}; nonempty endpoint relations are never asserted realizable by these choices')


def support_test(colors, target, domain):
    """Intersect row constraints on each SAME support/shape variable.

    Variables are independent in this necessary relaxation. An empty domain
    proves impossibility; a nonempty domain is never a realizability claim.
    """
    allowed = [set(range(len(s['choices']))) for s in domain['local_shapes']]
    row_choices = []
    for ri, (available, transport) in enumerate(zip(colors, domain['row_transports'], strict=True)):
        compatible = {j for j, c in enumerate(transport['literal_forbidden_choices'])
                      if bool(available - ({c} if c >= 0 else set())) == bool(target >> ri & 1)}
        sid = transport['local_shape']
        allowed[sid] &= compatible
        row_choices.append(sorted(compatible))
    empties = [sid for sid, choices in enumerate(allowed) if not choices]
    if empties:
        sid = empties[0]
        contributing = [dict(row_index=ri, allowed_choice_indices=row_choices[ri])
                        for ri, t in enumerate(domain['row_transports'])
                        if t['local_shape'] == sid]
        return dict(support_id=domain['id'], empty_local_shape=sid,
                    conflicting_row_constraints=contributing)
    return dict(support_id=domain['id'],
                possible_local_choice_indices=[sorted(s) for s in allowed])


def verify_subdivision(edges, certificate):
    """Validate explicit paths independently of the planarity boolean."""
    branches = set(certificate['branch_vertices'])
    paths = certificate['paths']
    links, used, internal = set(), set(), set()
    for path in paths:
        assert len(path) >= 2 and len(set(path)) == len(path)
        assert path[0] in branches and path[-1] in branches
        middle = set(path[1:-1])
        assert not middle & (branches | internal)
        internal |= middle
        link = tuple(sorted((path[0], path[-1])))
        assert link not in links
        links.add(link)
        for a, b in zip(path, path[1:]):
            edge = tuple(sorted((a, b)))
            assert edge in edges and edge not in used
            used.add(edge)
    if certificate['model'] == 'K5':
        assert len(branches) == 5 and links == set(combinations(sorted(branches), 2))
    else:
        assert certificate['model'] == 'K3,3' and len(branches) == 6
        sides = [side for side in combinations(sorted(branches), 3)
                 if links == {tuple(sorted((a, b))) for a in side for b in branches-set(side)}]
        assert sides


def star_obstruction(form_id, form, edges, pair, side, spoke, domain):
    z, w = pair[side], pair[1-side]
    contracted, apex = form['vertices'], form['vertices']+1
    star = {(w, contracted)} | {(b, contracted) for b in domain['actual_boundary_support']}
    augmented = edges | {spoke} | star | {(b, apex) for b in B}
    g = nx.Graph()
    g.add_nodes_from(range(apex+1))
    g.add_edges_from(sorted(augmented))
    certificate = kuratowski_certificate(g)
    verify_subdivision(augmented, certificate)
    return dict(form_id=form_id, original_root_order=pair,
        spoke_root=z, unary_root=w, original_restored_spoke=spoke,
        actual_unary_boundary_support=domain['actual_boundary_support'],
        contracted_original_unary_vertex=contracted, boundary_apex=apex,
        minor_edges=sorted(augmented), obstruction=certificate)


def grown_form(form):
    tails, branch_sets = [], [[v] for v in form['triangle']]
    next_vertex = 8
    for path in form['branch_paths']:
        tail, start = [], 0
        neighborhoods = [form['neighborhoods'][v-5] for v in path]
        while start < len(neighborhoods)-1:
            end = start+1
            while end < len(neighborhoods)-1 and neighborhoods[end] == neighborhoods[start]:
                end += 1
            run = neighborhoods[start:end]
            growth = 0 if form['family'].endswith('two_runs') and start == 0 else 2
            tail.extend(run+[run[-1]]*growth)
            for j in range(len(run)):
                size = 1+growth if j == len(run)-1 else 1
                branch_sets.append(list(range(next_vertex, next_vertex+size)))
                next_vertex += size
            start = end
        tail.append(neighborhoods[-1])
        branch_sets.append([next_vertex])
        next_vertex += 1
        tails.append(tail)
    result = graph(form, tails)
    mapping = {v: 5+j for j, vs in enumerate(branch_sets) for v in vs}
    mapping.update({b: b for b in B})
    assert set(mapping) == set(range(result['vertices']))
    quotient = {tuple(sorted((mapping[a], mapping[b]))) for a, b in result['edges']
                if mapping[a] != mapping[b]}
    assert quotient == set(map(tuple, form['edges']))
    return result, branch_sets, mapping


def actual_unary_controls(forms):
    """Small original graph controls, not coverage of arbitrary unary sources."""
    templates = [dict(kind='singleton', inner=[], supports=[[0, 2, 4]]),
        dict(kind='edge', inner=[(0, 1)], supports=[[0, 2], [1, 3, 4]]),
        dict(kind='path', inner=[(0, 1), (1, 2)],
             supports=[[0, 2], [0, 2], [1, 3, 4]]),
        dict(kind='triangle', inner=[(0, 1), (0, 2), (1, 2)],
             supports=[[0], [1, 3], [2, 4]])]
    saved, checks = [], 0
    for fi in (0, 26, 62, 125):
        form = forms[fi]
        edges = set(map(tuple, form['edges']))
        triangles = [t for t in combinations(form['interior_order'], 3)
                     if all(e in edges for e in combinations(t, 2))]
        pair = triangles[0][:2]
        regions = original_regions(form['interior_order'], edges, pair)
        ports = list(pair) + sorted(set().union(*(set(r['contact_order']) for r in regions)))
        core_rows = [witnesses(form['interior_order'], edges, row, ports) for row in ROWS]
        for side in (0, 1):
            z, w = pair[side], pair[1-side]
            b = min(b for b in B if (b, z) not in edges)
            spoke = (b, z)
            for ti, template in enumerate(templates):
                vs = list(range(form['vertices'], form['vertices']+len(template['supports'])))
                ve = {tuple(sorted((vs[a], vs[d]))) for a, d in template['inner']}
                ve |= {(b, v) for v, support in zip(vs, template['supports'], strict=True) for b in support}
                full_edges = edges | {spoke, (w, vs[0])} | ve
                assert all(sum(v in e for e in full_edges) == 4 for v in vs)
                full_interior = form['interior_order'] + vs
                full_ports = ports + [vs[0]]
                rows = []
                for ri, row in enumerate(ROWS):
                    unary = witnesses(vs, ve, row, [vs[0]])
                    assert unary
                    actual = witnesses(full_interior, full_edges, row, full_ports)
                    joined = {t+(d[0],) for t in core_rows[ri] for d in unary
                              if t[side] != row[b] and t[1-side] != d[0]}
                    assert set(actual) == joined
                    for t, f in actual.items():
                        validate_witness(f, list(range(5+len(full_interior))), full_edges, row, full_ports, t)
                    rows.append(dict(row_index=ri, unary_endpoint_relation=sorted(unary),
                        unary_complete_witnesses=[unary[t] for t in sorted(unary)],
                        original_joint_relation=sorted(actual),
                        original_complete_witnesses=[actual[t] for t in sorted(actual)]))
                    checks += 1
                saved.append(dict(form_id=fi, template_id=ti, kind=template['kind'],
                    original_root_order=pair, restored_spoke=spoke,
                    original_unary_vertices=vs, original_unary_endpoint=vs[0],
                    unary_coloring_order=sorted(B | set(vs)), unary_edges=sorted(ve),
                    full_edges=sorted(full_edges), full_coloring_order=list(range(5+len(full_interior))),
                    complete_port_order=full_ports,
                    original_components=original_regions(full_interior, full_edges, pair), rows=rows,
                    sigma=sum(1 << i for i, r in enumerate(rows) if r['original_joint_relation']),
                    disk_or_minimality_claimed=False))
    assert len(saved) == 32 and checks == 320
    return dict(graphs=saved, whole_original_graph_row_checks=checks)


def build():
    orbits = {str(m): sorted({relabel_mask(m, [(s*j+t) % 5 for j in range(5)])
        for s in (-1, 1) for t in range(5)}) for m in (933, 941)}
    forms = load_forms()
    supports = [support_domain(mask) for mask in range(32)]
    saved, topology, topo_lookup, counts = [], [], {}, Counter()
    kernel_digest, join_digest = sha256(), sha256()
    negative = None
    for fi, form in enumerate(forms):
        edges = set(map(tuple, form['edges']))
        interior, order = form['interior_order'], list(range(form['vertices']))
        assert all(sum(v in e for e in edges) == 4 for v in interior)
        assert [[b for b in sorted(B) if (b, v) in edges] for v in interior] == [
            sorted(s) for s in form['neighborhoods']]
        triangles = [t for t in combinations(interior, 3)
                     if all(e in edges for e in combinations(t, 2))]
        pairs = sorted({e for t in triangles for e in combinations(t, 2)})
        critical = []
        assert not witnesses(interior, edges, Q4, pairs[0])
        for edge in sorted(edges-FRAME):
            f = next(search(interior, edges-{edge}, dict(enumerate(Q4))), None)
            assert f is not None
            critical.append(dict(edge=edge, coloring=[f[v] for v in order]))
        long = grown_form(form) if form['family'].startswith('single_triangle') else None
        long_marks, marked = [], []
        for pair in pairs:
            regions = original_regions(interior, edges, pair)
            ports = list(pair) + sorted(set().union(*(set(r['contact_order']) for r in regions)))
            ws_rows = [witnesses(interior, edges, row, ports) for row in ROWS]
            assert sum(1 << i for i, ws in enumerate(ws_rows) if ws) == 1022
            core_rows = []
            for ri, (row, ws) in enumerate(zip(ROWS, ws_rows, strict=True)):
                for t, witness in ws.items():
                    validate_witness(witness, order, edges, row, ports, t)
                core_rows.append(dict(row_index=ri, joint_tuples=sorted(ws),
                    complete_coloring_witnesses=[ws[t] for t in sorted(ws)]))
                counts['core_joint_row_checks'] += 1
            additions = []
            long_rows = None
            if long:
                lg, branch_sets, mapping = long
                le = set(map(tuple, lg['edges']))
                assert all(branch_sets[v-5] == [v] for v in pair)
                long_regions = original_regions(lg['interior_order'], le, pair)
                long_ports = list(pair)+sorted(set().union(*(set(r['contact_order']) for r in long_regions)))
                long_rows = [witnesses(lg['interior_order'], le, row, long_ports) for row in ROWS]
                for short, full in zip(ws_rows, long_rows, strict=True):
                    assert {t[:2] for t in short} == {t[:2] for t in full}
                    counts['long_root_pair_checks'] += 1
                long_marks.append(dict(original_root_order=pair, original_components=long_regions,
                    complete_port_order=long_ports,
                    rows=[dict(row_index=ri, joint_tuples=sorted(ws),
                          complete_coloring_witnesses=[ws[t] for t in sorted(ws)])
                          for ri, ws in enumerate(long_rows)]))
            for side in (0, 1):
                z, w = pair[side], pair[1-side]
                for b in sorted(B):
                    spoke = (b, z)
                    if spoke in edges:
                        continue
                    extended = edges | {spoke}
                    assert [sum(r in e for e in extended) for r in pair] == [5 if j == side else 4 for j in (0, 1)]
                    rows, colors = [], []
                    for ri, (row, ws) in enumerate(zip(ROWS, ws_rows, strict=True)):
                        tuples = sorted(ws)
                        retained = [j for j, t in enumerate(tuples) if t[side] != row[b]]
                        exact = {tuples[j] for j in retained}
                        assert exact == set(witnesses(interior, extended, row, ports))
                        kernel = sorted(t+(d,) for t in exact for d in sorted(U) if t[1-side] != d)
                        free_endpoint = form['vertices']
                        # This free coordinate checks the operator, not an actual unary source.
                        operator = witnesses(interior+[free_endpoint], extended | {(w, free_endpoint)},
                                             row, ports+[free_endpoint])
                        assert set(operator) == set(kernel)
                        available = {t[1-side] for t in exact}
                        colors.append(available)
                        lookup = {t: j for j, t in enumerate(tuples)}
                        source_indices = [lookup[t[:-1]] for t in kernel]
                        for t, j in zip(kernel, source_indices, strict=True):
                            validate_witness(ws[tuples[j]], order, extended, row, ports, t[:-1])
                        for mask in range(1, 16):
                            endpoint = {d for d in U if mask >> d & 1}
                            joined = {t for t in kernel if t[-1] in endpoint}
                            independent = {t+(d,) for d in endpoint for t in exact if t[1-side] != d}
                            assert joined == independent
                            forbidden = endpoint if len(endpoint) == 1 else set()
                            assert bool(joined) == bool(available-forbidden)
                            join_digest.update(json.dumps([fi, pair, side, b, ri, mask, sorted(joined)], separators=(',', ':')).encode())
                            counts['nonempty_unary_operator_checks'] += 1
                        kernel_digest.update(json.dumps(kernel, separators=(',', ':')).encode())
                        rows.append(dict(row_index=ri, retained_core_tuple_indices=retained,
                            unary_root_colors=sorted(available), exact_gluing_operator=kernel,
                            operator_core_witness_indices=source_indices,
                            operator_indices_by_endpoint_color=[[j for j, t in enumerate(kernel) if t[-1] == d]
                                                               for d in range(4)]))
                        counts['spoke_joint_row_checks'] += 1
                        if long_rows is not None:
                            assert available == {t[1-side] for t in long_rows[ri] if t[side] != row[b]}
                            counts['long_spoke_row_checks'] += 1
                    upper = sum(1 << i for i, cs in enumerate(colors) if cs)
                    lower = T4 | sum(1 << i for i, cs in enumerate(colors) if len(cs) >= 2)
                    exclusions = []
                    for candidate, targets in orbits.items():
                        for target in targets:
                            counts[f'{candidate}_comparisons'] += 1
                            if target & upper != target:
                                ri = next(i for i in range(10) if target >> i & 1 and not colors[i])
                                result = dict(reason='target_accepted_row_already_empty', row_index=ri)
                                counts[f'{candidate}_empty_row_exclusions'] += 1
                            elif lower & target != lower:
                                ri = next(i for i in range(10) if not target >> i & 1 and len(colors[i]) >= 2)
                                result = dict(reason='survives_every_nonempty_original_unary', row_index=ri,
                                    operator_witness_indices_by_endpoint_color=[xs[0] for xs in rows[ri]['operator_indices_by_endpoint_color']])
                                counts[f'{candidate}_two_color_exclusions'] += 1
                            else:
                                counts[f'{candidate}_support_stage_cases'] += 1
                                tests = []
                                for domain in supports:
                                    test = support_test(colors, target, domain)
                                    counts['fixed_support_tests'] += 1
                                    if 'empty_local_shape' in test:
                                        counts['S4_incompatible_support_tests'] += 1
                                    else:
                                        counts['S4_compatible_support_tests'] += 1
                                        key = (fi, pair, side, b, domain['id'])
                                        if key not in topo_lookup:
                                            topo_lookup[key] = len(topology)
                                            topology.append(star_obstruction(fi, form, edges, pair, side, spoke, domain))
                                        test['contracted_star_obstruction_id'] = topo_lookup[key]
                                    tests.append(test)
                                result = dict(reason='fixed_support_equivariance_or_original_star_minor', support_tests=tests)
                                if negative is None:
                                    independent = [-1 if target >> i & 1 or not cs else next(iter(cs))
                                                   for i, cs in enumerate(colors)]
                                    assert all(not cs or len(cs) == 1 for i, cs in enumerate(colors) if not target >> i & 1)
                                    assert sum(1 << i for i, cs in enumerate(colors)
                                               if cs-({independent[i]} if independent[i] >= 0 else set())) == target
                                    negative = dict(form_id=fi, original_root_order=pair, spoke_root=z,
                                        unary_root=w, original_restored_spoke=spoke, target=target,
                                        independently_chosen_row_forbidden_colors=independent,
                                        unary_root_colors=list(map(sorted, colors)),
                                        semantics='Rowwise algebraic choices realize this mask in the operator, but no fixed original disk unary can supply them; not a source realization')
                            exclusions.append(dict(candidate=int(candidate), target_mask=target, **result))
                    additions.append(dict(original_spoke=spoke, omitted_unary_owner=w,
                        omitted_unary_identity='original_V_at_'+str(w),
                        intermediate_edges=sorted(extended), intermediate_sigma=upper,
                        guaranteed_acceptance_mask_if_T4=lower, rows=rows, target_exclusions=exclusions))
                    counts['spoke_unary_cases'] += 1
            marked.append(dict(original_root_order=pair, original_root_edge=pair,
                original_components=regions, complete_port_order=ports,
                original_core_rows=core_rows, original_restorations=additions))
        long_control = None
        if long:
            lg, branch_sets, mapping = long
            long_control = dict(original_graph=lg, original_coloring_order=list(range(lg['vertices'])),
                quotient_to_form=mapping, original_interior_branch_sets=branch_sets, marked_roots=long_marks)
            counts['fixed_original_long_graphs'] += 1
        saved.append(dict(form_id=fi, family=form['family'], input_index=form['input_index'],
            original_edges=sorted(edges), original_neighborhoods=form['neighborhoods'],
            original_coloring_order=order, q4_critical_witnesses=critical,
            marked_cores=marked, original_long_control=long_control))
    assert counts['spoke_unary_cases'] == 3732
    assert counts['933_support_stage_cases'] + counts['941_support_stage_cases'] == 2784
    assert counts['fixed_support_tests'] == 89088 and counts['S4_compatible_support_tests'] == 5444
    assert len(topology) == 2640 and negative is not None
    actual = actual_unary_controls(forms)
    dependencies = [Path(__file__).resolve(), BRANCHES, PATHS, DOUBLE] + [ROOT/'scripts'/name for name in (
        'c5_excess_two_mixed_core_spokes.py', 'c5_excess_two_triangle_edge.py',
        'c5_941_three_spoke.py', 'c5_941_two_spoke.py', 'c5_independent_support_capacity.py',
        'c5_odd_join_cores.py')]
    return dict(schema=1, scope='Exclude retained-mixed degree-(4,4) cores omitting one original spoke and one original unary for fixed 933/941 epsilon-two disk sources, including root swap. Arbitrary-size coverage is paper.',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        normalized_core_rejection=Q4, pattern_order=ROWS, target_D5_orbits=orbits,
        operator_semantics='The last coordinate is the endpoint of the actual omitted V; restrict it to its nonempty complete endpoint relation. Core witness indices do not invent colorings of V. All core contacts share one literal boundary/color frame.',
        contraction_semantics='Contract the SAME original connected V only for a non-disk minor; its actual support and one root edge remain. This contraction does not preserve or replace its color relation.',
        fixed_support_domains=supports, necessary_forms=saved,
        original_contracted_star_obstructions=topology, independent_row_choice_negative_control=negative,
        actual_original_unary_controls=actual,
        summary=dict(**dict(sorted(counts.items())), necessary_forms=len(forms),
            marked_original_root_edges=sum(len(f['marked_cores']) for f in saved),
            target_comparisons=37320, unique_original_star_subdivisions=len(topology),
            subdivision_models=dict(sorted(Counter(t['obstruction']['model'] for t in topology).items())),
            original_unary_control_graphs=len(actual['graphs']), original_unary_graph_row_checks=actual['whole_original_graph_row_checks'],
            full_operator_sha256=kernel_digest.hexdigest(), nonempty_join_sha256=join_digest.hexdigest(),
            remaining=0, graph_census=False, disk_realizability_claimed=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    data = encoded(result)
    if args.check:
        assert OUT.read_text() == data, 'certificate differs; regenerate intentionally'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(data)
    print(json.dumps(dict(status='checked' if args.check else 'written', **result['summary']), sort_keys=True))


if __name__ == '__main__':
    main()
