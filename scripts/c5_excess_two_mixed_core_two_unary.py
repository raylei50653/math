#!/usr/bin/env python3
"""Retained mixed core: omit one original single-contact unary at each root.

Keep the full joint core relation, both nonempty original endpoint relations,
and both fixed actual supports in one literal color frame. S4 constraints and
explicit two-star disk minors exclude the inherited necessary domain. Paper
supplies arbitrary-size coverage; this is not a graph census or Lean theorem.
Run: uv run --with networkx==3.5 python scripts/<this file> [--check]
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import networkx as nx

from c5_independent_support_capacity import B, FRAME, ROWS, U
from c5_941_two_spoke import Q4, relabel_mask, search
from c5_excess_two_mixed_core_spokes import (
    encoded, load_forms, original_regions, validate_witness, witnesses,
)
from c5_excess_two_mixed_core_spoke_unary import (
    grown_form, support_domain, verify_subdivision,
)
from c5_odd_join_cores import kuratowski_certificate

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_two_unary/observations.json'
BRANCHES = ROOT / 'artifacts/c5_triangle_branches/observations.json'
PATHS = ROOT / 'artifacts/c5_triangle_path_reduction/observations.json'
DOUBLE = ROOT / 'artifacts/c5_two_triangle_blocks/observations.json'


def choice_constraints(allowed_rows, du, dv):
    """Binary constraints between the two SAME support/local-shape functions."""
    sizes = [len(s['choices']) for d in (du, dv) for s in d['local_shapes']]
    offset, tables, origins = len(du['local_shapes']), {}, {}
    for ri, (allowed, tu, tv) in enumerate(zip(
            allowed_rows, du['row_transports'], dv['row_transports'], strict=True)):
        edge = (tu['local_shape'], offset+tv['local_shape'])
        table = {(i, j) for i, a in enumerate(tu['literal_forbidden_choices'])
                       for j, b in enumerate(tv['literal_forbidden_choices'])
                 if (a, b) in allowed}
        if edge in tables:
            tables[edge] &= table
        else:
            tables[edge] = table
            origins[edge] = []
        origins[edge].append(ri)
    return sizes, [(a, b, tuple(sorted(t))) for (a, b), t in sorted(tables.items())], origins


def filtered_masks(da, db, table):
    na, nb = 0, 0
    for i, j in table:
        if da >> i & 1 and db >> j & 1:
            na |= 1 << i
            nb |= 1 << j
    return na, nb


def solve_choices(sizes, tables):
    """Return an assignment or a complete finite unsatisfiability proof tree.

    A proof node is [propagation_steps, end]. A step [constraint, new_a, new_b]
    removes precisely unsupported values. End is ['empty', constraint] or
    ['branch', variable, [[choice, child_proof], ...]], covering every value.
    """
    def go(domains):
        steps, changed = [], True
        while changed:
            changed = False
            for ci, (a, b, table) in enumerate(tables):
                na, nb = filtered_masks(domains[a], domains[b], table)
                if not na or not nb:
                    return None, [steps, ['empty', ci]]
                if (na, nb) != (domains[a], domains[b]):
                    domains[a], domains[b] = na, nb
                    steps.append([ci, na, nb])
                    changed = True
        assignment = [(d & -d).bit_length()-1 for d in domains]
        if all((assignment[a], assignment[b]) in table for a, b, table in tables):
            return assignment, None
        candidates = [v for v, d in enumerate(domains) if d.bit_count() > 1
                      and any(v in (a, b) for a, b, _ in tables)]
        v = min(candidates, key=lambda v: (domains[v].bit_count(), v))
        children = []
        for c in range(sizes[v]):
            if not domains[v] >> c & 1:
                continue
            child = domains.copy()
            child[v] = 1 << c
            answer, proof = go(child)
            if answer is not None:
                return answer, None
            children.append([c, proof])
        return None, [steps, ['branch', v, children]]
    return go([(1 << s)-1 for s in sizes])


def verify_unsat(sizes, tables, proof):
    """Independent proof traversal; does not call the search solver."""
    nodes = 0

    def visit(domains, node):
        nonlocal nodes
        nodes += 1
        steps, end = node
        for ci, na, nb in steps:
            a, b, table = tables[ci]
            # Recompute support directly from all allowed pairs.
            possible = [(i, j) for i, j in table
                        if domains[a] >> i & 1 and domains[b] >> j & 1]
            expected_a = sum(1 << i for i in {i for i, _ in possible})
            expected_b = sum(1 << j for j in {j for _, j in possible})
            assert (na, nb) == (expected_a, expected_b) and na and nb
            assert (na, nb) != (domains[a], domains[b])
            domains[a], domains[b] = na, nb
        if end[0] == 'empty':
            a, b, table = tables[end[1]]
            assert not any(domains[a] >> i & 1 and domains[b] >> j & 1
                           for i, j in table)
        else:
            assert end[0] == 'branch'
            _, v, children = end
            choices = [c for c in range(sizes[v]) if domains[v] >> c & 1]
            assert len(choices) > 1 and [c for c, _ in children] == choices
            for c, child_proof in children:
                child = domains.copy()
                child[v] = 1 << c
                visit(child, child_proof)
    visit([(1 << s)-1 for s in sizes], proof)
    return nodes


def support_query(relations, target, supports):
    allowed = [set((a, b) for a, b in product(range(-1, 4), repeat=2)
                   if any(x != a and y != b for x, y in k) == bool(target >> ri & 1))
               for ri, k in enumerate(relations)]
    assert all(allowed)
    tests, compatible, counts = [], [], Counter()
    for du in supports:
        for dv in supports:
            sizes, tables, _ = choice_constraints(allowed, du, dv)
            assignment, proof = solve_choices(sizes, tables)
            if assignment is None:
                counts['unsat_proof_nodes'] += verify_unsat(sizes, tables, proof)
                tests.append([0, proof])
                counts['incompatible'] += 1
            else:
                offset = len(du['local_shapes'])
                schedule = [(tu['literal_forbidden_choices'][assignment[tu['local_shape']]],
                             tv['literal_forbidden_choices'][assignment[offset+tv['local_shape']]])
                            for tu, tv in zip(du['row_transports'], dv['row_transports'], strict=True)]
                # Validate against complete pairs, independently of constraint tables.
                assert sum(1 << ri for ri, (k, (a, b)) in enumerate(zip(relations, schedule, strict=True))
                           if any(x != a and y != b for x, y in k)) == target
                assert all((assignment[a], assignment[b]) in t for a, b, t in tables)
                tests.append([1, assignment])
                compatible.append((du['id'], dv['id']))
                counts['compatible'] += 1
    assert len(tests) == 1024
    return dict(root_pair_relations=relations, target_mask=target,
                row_allowed_literal_forbidden_pairs=list(map(sorted, allowed)),
                support_pair_test_order='index=32*support_U_mask+support_V_mask; [0, unsat proof] or [1, local-choice assignment]',
                tests=tests, compatible_support_pairs=compatible,
                counts=dict(sorted(counts.items())))


def two_star_obstruction(fi, form, edges, pair, supports):
    a, b, h = range(form['vertices'], form['vertices']+3)
    su, sv = supports
    star = {(pair[0], a), (pair[1], b)}
    star |= {(v, a) for v in B if su >> v & 1}
    star |= {(v, b) for v in B if sv >> v & 1}
    augmented = edges | star | {(v, h) for v in B}
    g = nx.Graph()
    g.add_nodes_from(range(h+1))
    g.add_edges_from(sorted(augmented))
    certificate = kuratowski_certificate(g)
    verify_subdivision(augmented, certificate)
    return dict(form_id=fi, original_root_order=pair,
                original_unary_identities=['U_at_'+str(pair[0]), 'V_at_'+str(pair[1])],
                retained_support_masks=[su, sv],
                retained_boundary_supports=[[v for v in sorted(B) if mask >> v & 1] for mask in supports],
                contracted_original_unary_vertices=[a, b], boundary_apex=h,
                minor_edges=sorted(augmented), obstruction=certificate)


def actual_double_unary_controls(forms):
    templates = [dict(kind='singleton', inner=[], supports=[[0, 2, 4]]),
        dict(kind='edge', inner=[(0, 1)], supports=[[0, 2], [1, 3, 4]]),
        dict(kind='path', inner=[(0, 1), (1, 2)], supports=[[0, 2], [0, 2], [1, 3, 4]]),
        dict(kind='triangle', inner=[(0, 1), (0, 2), (1, 2)], supports=[[0], [1, 3], [2, 4]])]
    saved, checks = [], 0
    for fi in (0, 26, 62, 125):
        form = forms[fi]
        edges = set(map(tuple, form['edges']))
        triangles = [t for t in combinations(form['interior_order'], 3)
                     if all(e in edges for e in combinations(t, 2))]
        pair = triangles[0][:2]
        regions = original_regions(form['interior_order'], edges, pair)
        ports = list(pair)+sorted(set().union(*(set(r['contact_order']) for r in regions)))
        core = [witnesses(form['interior_order'], edges, row, ports) for row in ROWS]
        for tids in product(range(4), repeat=2):
            unaries, added, next_vertex = [], set(), form['vertices']
            for side, ti in enumerate(tids):
                template = templates[ti]
                vs = list(range(next_vertex, next_vertex+len(template['supports'])))
                next_vertex += len(vs)
                ve = {tuple(sorted((vs[x], vs[y]))) for x, y in template['inner']}
                ve |= {(b, v) for v, support in zip(vs, template['supports'], strict=True) for b in support}
                added |= ve | {(pair[side], vs[0])}
                unaries.append(dict(identity='UV'[side], owner=pair[side], vertices=vs,
                    endpoint=vs[0], template_kind=template['kind'], edges=sorted(ve),
                    coloring_order=sorted(B | set(vs))))
            full_edges = edges | added
            interior = list(range(5, next_vertex))
            full_ports = ports+[u['endpoint'] for u in unaries]
            assert all(sum(v in e for e in full_edges) == 4 for u in unaries for v in u['vertices'])
            assert [sum(r in e for e in full_edges) for r in pair] == [5, 5]
            rows = []
            for ri, row in enumerate(ROWS):
                uw, vw = [witnesses(u['vertices'], set(map(tuple, u['edges'])), row, [u['endpoint']])
                          for u in unaries]
                assert uw and vw
                joined = {t+(a[0], b[0]) for t in core[ri] for a in uw for b in vw
                          if t[0] != a[0] and t[1] != b[0]}
                actual = witnesses(interior, full_edges, row, full_ports)
                assert set(actual) == joined
                for t, coloring in actual.items():
                    validate_witness(coloring, list(range(next_vertex)), full_edges, row, full_ports, t)
                rows.append(dict(row_index=ri,
                    original_endpoint_relations=[sorted(uw), sorted(vw)],
                    original_unary_complete_witnesses=[[ws[t] for t in sorted(ws)] for ws in (uw, vw)],
                    full_joint_tuples=sorted(actual), complete_coloring_witnesses=[actual[t] for t in sorted(actual)]))
                checks += 1
            saved.append(dict(form_id=fi, original_root_order=pair, template_ids=tids,
                original_unaries=unaries, full_edges=sorted(full_edges),
                full_coloring_order=list(range(next_vertex)), complete_port_order=full_ports,
                original_components=original_regions(interior, full_edges, pair), rows=rows,
                disk_or_minimality_claimed=False))
    assert len(saved) == 64 and checks == 640
    return dict(graphs=saved, whole_original_graph_row_checks=checks)


def build():
    forms = load_forms()
    supports = [support_domain(m) for m in range(32)]
    orbits = {str(m): sorted({relabel_mask(m, [(s*j+t) % 5 for j in range(5)])
                            for s in (-1, 1) for t in range(5)}) for m in (933, 941)}
    queries, cache, saved, topology, counts = [], {}, [], [], Counter()
    operator_digest, negative = sha256(), None
    for fi, form in enumerate(forms):
        edges = set(map(tuple, form['edges']))
        interior, order = form['interior_order'], list(range(form['vertices']))
        assert all(sum(v in e for e in edges) == 4 for v in interior)
        assert [[b for b in sorted(B) if (b, v) in edges] for v in interior] == [sorted(s) for s in form['neighborhoods']]
        triangles = [t for t in combinations(interior, 3) if all(e in edges for e in combinations(t, 2))]
        pairs = sorted({e for t in triangles for e in combinations(t, 2)})
        critical = []
        for edge in sorted(edges-FRAME):
            coloring = next(search(interior, edges-{edge}, dict(enumerate(Q4))), None)
            assert coloring is not None
            critical.append(dict(edge=edge, coloring=[coloring[v] for v in order]))
        long = grown_form(form) if form['family'].startswith('single_triangle') else None
        marked, long_marks = [], []
        for pair in pairs:
            regions = original_regions(interior, edges, pair)
            ports = list(pair)+sorted(set().union(*(set(r['contact_order']) for r in regions)))
            core = [witnesses(interior, edges, row, ports) for row in ROWS]
            relations = tuple(tuple(sorted({t[:2] for t in ws})) for ws in core)
            assert sum(1 << i for i, ws in enumerate(core) if ws) == 1022
            rows = []
            for ri, (row, ws) in enumerate(zip(ROWS, core, strict=True)):
                tuples = sorted(ws)
                for t, coloring in ws.items():
                    validate_witness(coloring, order, edges, row, ports, t)
                kernel = sorted(t+(a, b) for t in tuples for a, b in product(sorted(U), repeat=2)
                                if t[0] != a and t[1] != b)
                a, b = form['vertices'], form['vertices']+1
                operator = witnesses(interior+[a, b], edges | {(pair[0], a), (pair[1], b)}, row, ports+[a, b])
                assert set(operator) == set(kernel)
                lookup = {t: j for j, t in enumerate(tuples)}
                indices = [lookup[t[:-2]] for t in kernel]
                by_endpoints = [[j for j, t in enumerate(kernel) if t[-2:] == (a, b)]
                                for a, b in product(range(4), repeat=2)]
                bitsets = [sum(1 << j for j in js) for js in by_endpoints]
                for um, vm in product(range(1, 16), repeat=2):
                    selected = 0
                    for a, b in product(range(4), repeat=2):
                        if um >> a & 1 and vm >> b & 1:
                            selected |= bitsets[4*a+b]
                    expected = {t+(a, b) for t in tuples for a, b in product(range(4), repeat=2)
                                if um >> a & 1 and vm >> b & 1 and t[0] != a and t[1] != b}
                    assert {t for j, t in enumerate(kernel) if selected >> j & 1} == expected
                    fu = (um & -um).bit_length()-1 if um.bit_count() == 1 else -1
                    fv = (vm & -vm).bit_length()-1 if vm.bit_count() == 1 else -1
                    assert bool(selected) == any(x != fu and y != fv for x, y in relations[ri])
                    counts['nonempty_double_endpoint_operator_checks'] += 1
                operator_digest.update(json.dumps(kernel, separators=(',', ':')).encode())
                rows.append(dict(row_index=ri, complete_joint_tuples=tuples,
                    complete_coloring_witnesses=[ws[t] for t in tuples],
                    exact_double_gluing_operator=kernel, operator_core_witness_indices=indices,
                    operator_indices_by_literal_endpoint_pair=by_endpoints))
                counts['core_and_free_operator_row_checks'] += 1
            if long:
                lg, branch_sets, mapping = long
                le = set(map(tuple, lg['edges']))
                assert all(branch_sets[r-5] == [r] for r in pair)
                for vs in branch_sets:
                    g = nx.Graph()
                    g.add_nodes_from(vs)
                    g.add_edges_from(e for e in le if set(e) <= set(vs))
                    assert nx.is_connected(g)
                lregions = original_regions(lg['interior_order'], le, pair)
                lports = list(pair)+sorted(set().union(*(set(r['contact_order']) for r in lregions)))
                lrows = [witnesses(lg['interior_order'], le, row, lports) for row in ROWS]
                for short, full in zip(core, lrows, strict=True):
                    assert {t[:2] for t in short} == {t[:2] for t in full}
                    counts['long_root_pair_row_checks'] += 1
                long_marks.append(dict(original_root_order=pair, original_components=lregions,
                    complete_port_order=lports, rows=[dict(row_index=ri, joint_tuples=sorted(ws),
                        complete_coloring_witnesses=[ws[t] for t in sorted(ws)]) for ri, ws in enumerate(lrows)]))
            exclusions, compatible_union = [], set()
            for candidate, targets in orbits.items():
                for target in targets:
                    counts[candidate+'_comparisons'] += 1
                    empty = next((i for i, k in enumerate(relations) if target >> i & 1 and not k), None)
                    robust = next((i for i, k in enumerate(relations) if not target >> i & 1
                                   and all(any(x != a and y != b for x, y in k)
                                           for a, b in product(range(-1, 4), repeat=2))), None)
                    if empty is not None:
                        result = dict(reason='target_accepted_row_already_empty', row_index=empty)
                        counts[candidate+'_empty_row_exclusions'] += 1
                    elif robust is not None:
                        result = dict(reason='survives_every_two_nonempty_original_unaries', row_index=robust)
                        counts[candidate+'_robust_pair_exclusions'] += 1
                    else:
                        counts[candidate+'_support_stage_cases'] += 1
                        key = (relations, target)
                        if key not in cache:
                            cache[key] = len(queries)
                            queries.append(support_query(relations, target, supports))
                        query = queries[cache[key]]
                        compatible_union.update(query['compatible_support_pairs'])
                        result = dict(reason='fixed_two_support_functions_or_same_source_two_star_minor',
                                      shared_support_query_id=cache[key])
                        counts['fixed_support_pair_tests'] += 1024
                        counts['S4_incompatible_support_pair_tests'] += query['counts']['incompatible']
                        counts['S4_compatible_support_pair_tests'] += query['counts']['compatible']
                        if negative is None:
                            schedule = [next((a, b) for a, b in product(range(-1, 4), repeat=2)
                                             if any(x != a and y != b for x, y in k) == bool(target >> ri & 1))
                                        for ri, k in enumerate(relations)]
                            negative = dict(form_id=fi, original_root_order=pair, target_mask=target,
                                independent_row_forbidden_pairs=schedule,
                                complete_root_pair_relations=relations,
                                semantics='An operator-only rowwise schedule, not a same-source disk realization')
                    exclusions.append(dict(candidate=int(candidate), target_mask=target, **result))
            minima, obstruction_ids = [], []
            for s in sorted(compatible_union, key=lambda s: (sum(x.bit_count() for x in s), s)):
                if not any(t[0] & s[0] == t[0] and t[1] & s[1] == t[1] for t in minima):
                    minima.append(s)
                    obstruction_ids.append(len(topology))
                    topology.append(two_star_obstruction(fi, form, edges, pair, s))
            coverage = []
            for s in sorted(compatible_union):
                j = next(j for j, t in enumerate(minima) if t[0] & s[0] == t[0] and t[1] & s[1] == t[1])
                coverage.append(dict(actual_support_masks=s, obstruction_id=obstruction_ids[j]))
            counts['unique_per_core_compatible_support_pairs'] += len(compatible_union)
            marked.append(dict(original_root_order=pair, original_components=regions,
                original_omitted_unary_identities=['U_at_'+str(pair[0]), 'V_at_'+str(pair[1])],
                original_unary_owners=pair, complete_core_port_order=ports,
                free_operator_port_order=ports+[form['vertices'], form['vertices']+1],
                core_rows=rows, target_exclusions=exclusions,
                same_source_actual_support_minor_coverage=coverage))
        long_control = None
        if long:
            lg, branch_sets, mapping = long
            long_control = dict(original_graph=lg, original_interior_branch_sets=branch_sets,
                                quotient_to_form=mapping, marked_roots=long_marks)
            counts['fixed_original_long_graphs'] += 1
        saved.append(dict(form_id=fi, family=form['family'], input_index=form['input_index'],
            original_edges=sorted(edges), original_neighborhoods=form['neighborhoods'],
            original_coloring_order=order, q4_critical_witnesses=critical,
            marked_cores=marked, original_long_control=long_control))
    assert counts['fixed_support_pair_tests'] == 2184192
    assert counts['S4_compatible_support_pair_tests'] == 100859
    assert len(topology) == 3180 and len(queries) == 377 and negative is not None
    actual = actual_double_unary_controls(forms)
    dependencies = [Path(__file__).resolve(), BRANCHES, PATHS, DOUBLE]+[ROOT/'scripts'/name for name in (
        'c5_excess_two_mixed_core_spoke_unary.py', 'c5_excess_two_mixed_core_spokes.py',
        'c5_excess_two_triangle_edge.py', 'c5_941_three_spoke.py', 'c5_941_two_spoke.py',
        'c5_independent_support_capacity.py', 'c5_odd_join_cores.py')]
    return dict(schema=1,
        scope='Fixed complete-Sigma 933/941 epsilon-two disk sources with adjacent degree-five roots and exactly one original mixed component: omitting one original single-contact unary at each root accepts all ten rows. Arbitrary-size coverage is paper.',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        pattern_order=ROWS, normalized_core_rejection=Q4, target_D5_orbits=orbits,
        operator_semantics='Both free endpoint coordinates must be restricted to the complete nonempty relations of the SAME original U and V. Core witnesses only certify the core, not invented unary interiors.',
        support_semantics='Two fixed named actual supports; local-shape variables belong to their original unary. All row transports use the one literal boundary/color frame.',
        proof_semantics='Each support query includes all 1024 support pairs, verified UNSAT proof trees or SAT assignments. SAT is a necessary relaxation, not realizability.',
        minor_semantics='Contract the SAME two disjoint original unary components only for topology; delete listed excess support edges to the smaller support pair certificate. This does not preserve their coloring relations or Sigma.',
        fixed_support_domains=supports, shared_support_queries=queries,
        necessary_forms=saved, same_source_two_star_subdivisions=topology,
        independent_row_choice_negative_control=negative, actual_original_double_unary_controls=actual,
        summary=dict(**dict(sorted(counts.items())), necessary_forms=len(forms),
            marked_original_root_edges=sum(len(f['marked_cores']) for f in saved), target_comparisons=5700,
            unique_support_queries=len(queries), unique_support_pair_solver_checks=1024*len(queries),
            unique_unsat_proof_nodes=sum(q['counts'].get('unsat_proof_nodes', 0) for q in queries),
            unique_two_star_subdivisions=len(topology),
            subdivision_models=dict(sorted(Counter(t['obstruction']['model'] for t in topology).items())),
            original_double_unary_control_graphs=len(actual['graphs']),
            original_double_unary_graph_row_checks=actual['whole_original_graph_row_checks'],
            full_double_operator_sha256=operator_digest.hexdigest(), remaining=0,
            graph_census=False, disk_realizability_claimed=False, new_lean_theorem=False))


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
