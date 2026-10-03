#!/usr/bin/env python3
"""Five original spokes: marked leaf fibers and a same-unary K5 reduction.

Arbitrary-size coverage, tight block palettes and actual tether extraction
are paper arguments. Controls retain complete ordered relations and witnesses;
neither the relation algebra nor the extracted minor samples are source graphs.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, U, colorings, normalize
from c5_excess_one_subcovers import singleton
from c5_941_two_spoke import relabel_mask, search
from c5_excess_two_mixed_core_spokes import validate_witness, witnesses

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_leaf_fibers/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
Q, PA, P2 = ROWS[0], ROWS[1], ROWS[3]
SWAP = (2, 1, 0, 3)


def edge(a, b):
    return tuple(sorted((a, b)))


def transport(row, permutation):
    moved = [None] * 5
    for i in range(5):
        moved[permutation[i]] = row[i]
    target = normalize(moved)
    colors = dict(zip(moved, target))
    colors.update(zip(sorted(U - set(colors)), sorted(U - set(colors.values()))))
    assert sorted(colors.values()) == sorted(U)
    assert tuple(colors[c] for c in moved) == target
    return dict(source_row=row, transported_row=target,
                color_permutation=[colors[c] for c in sorted(U)],
                transported_row_index=ROWS.index(target))


def named_frames():
    source = json.loads(SOURCE.read_text())
    target = next(t for t in source['targets'] if t['source_sigma'] == 941)
    records = []
    for item in target['five_spoke_reductions']['records']:
        if not item['original_incidence_cases'][1]['status'].startswith('unresolved'):
            continue
        aside, bside = item['three_spoke_side'], item['two_spoke_side']
        triple, pair = (item['original_root_spoke_supports'][s] for s in (aside, bside))
        forced = item['original_incidence_cases'][1]['forced_singletons_in_high_root_spoke_support']
        qi, = forced
        choices = []
        for direction, offset in product((1, -1), range(5)):
            permutation = tuple((direction * i + offset) % 5 for i in range(5))
            if ({permutation[i] for i in triple} == {1, 2, 3}
                    and {permutation[i] for i in pair} == {1, 4}
                    and permutation[qi] == 4):
                choices.append(permutation)
        permutation, = choices
        sigma = relabel_mask(941, permutation)
        rejected = sorted(singleton(row) for i, row in enumerate(ROWS) if not sigma >> i & 1)
        assert rejected in ([1, 2, 4], [1, 3, 4])
        rows = [transport(row, permutation) for row in ROWS]
        assert len({r['transported_row_index'] for r in rows}) == 10
        records.append(dict(original_root_spoke_supports=item['original_root_spoke_supports'],
            original_a_side=aside, original_b_side=bside, original_forced_singleton=qi,
            one_global_boundary_permutation=permutation, row_transports=rows,
            canonical_spokes=dict(a=[1, 2, 3], b=[1, 4]),
            canonical_sigma=sigma, canonical_rejected_singletons=rejected,
            component_regions=dict(C=[1, 2, 3, 4], unary_U=[0, 1, 4]),
            original_omitted_spokes=[list(edge(6, i)) for i in (1, 3)],
            scope='Transport of necessary named attachments; not source realization'))
    assert len(records) == 8
    assert len({r['canonical_sigma'] for r in records}) == 2
    return records


def abstract_join(row, c_relation, u_relation):
    """Full (b,a,y,u) tuples, retaining a single whole C tuple per witness."""
    result = {}
    for (x, y), u, a, b in product(c_relation, u_relation, sorted(U), sorted(U)):
        if (a not in {row[i] for i in (1, 2, 3)} and b not in {row[i] for i in (1, 4)}
                and a != b and a != x and b != y and b != u):
            result.setdefault((b, a, y, u), (x, y))
    return result


def relation_algebra():
    assert all(PA[i] == P2[i] for i in (0, 1, 4))
    assert all(SWAP[PA[i]] == P2[i] for i in (1, 2, 3, 4))
    assert U - {PA[i] for i in (1, 2, 3)} == {3}
    assert U - {P2[i] for i in (1, 2, 3)} == {3}
    assert U - {PA[i] for i in (1, 4)} - {3} == {0, 2}
    assert U - {P2[i] for i in (1, 4)} - {3} == {0, 2}
    invariant = []
    for bits in range(1, 16):
        relation = {c for c in U if bits >> c & 1}
        if {0 if c == 0 else 1 if c == 1 else 5-c for c in relation} == relation:
            invariant.append(relation)
    assert len(invariant) == 7
    examples = [[(3, 3)], [(0, 2)], [(0, 0)], [(0, 1)]]
    records = []
    for c_relation, u_relation in product(examples, invariant):
        swapped = sorted((SWAP[x], SWAP[y]) for x, y in c_relation)
        first = abstract_join(PA, c_relation, u_relation)
        second = abstract_join(P2, swapped, u_relation)
        forbidden = sorted(u_relation) if len(u_relation) == 1 else []
        if forbidden != [0]:
            assert bool(first) == bool(second)
        if bool(first) != bool(second):
            assert forbidden == [0]
        records.append(dict(C_PA_complete_relation=c_relation,
            C_P2_complete_relation=swapped, U_same_endpoint_relation=sorted(u_relation),
            U_forbidden=forbidden,
            PA_joint_tuples=[dict(tuple=t, whole_C_tuple=x) for t, x in sorted(first.items())],
            P2_joint_tuples=[dict(tuple=t, whole_C_tuple=x) for t, x in sorted(second.items())],
            unequal_acceptance_requires_unary_singleton_zero=bool(first) != bool(second)))
    # Each complete relation is a union of individual tuples. These four
    # bit pairs exhaust its two guarded queries; no tuple marginals are used.
    singleton_bits = {(int(x != 3 and y != 0), int(x != 3 and y != 2))
                      for x, y in product(sorted(U), repeat=2)}
    assert singleton_bits == set(product((0, 1), repeat=2))
    assert len(records) == 28
    return dict(scope='Complete-relation algebra, not graph realization',
        PA=PA, P2=P2, unary_actual_support_envelope=[0, 1, 4],
        mixed_actual_support_envelope=[1, 2, 3, 4], C_color_permutation=SWAP,
        complete_C_guard_bit_pairs=sorted(singleton_bits), records=records)


def palette_algebra():
    records = []
    for kind, merged in [('odd_cycle', {2, 3}), ('bridge', {0}), ('bridge', {1})]:
        possible = []
        for old in combinations(sorted(U), len(merged)):
            if all((c in old) == (c in merged) for c in (0, 3)):
                possible.append(old)
        assert possible == ([(1, 3), (2, 3)] if kind == 'odd_cycle'
                            else [(0,)] if merged == {0} else [(1,), (2,)])
        records.append(dict(block_kind=kind, PA_palette=sorted(merged),
                            possible_Q_palettes=possible, preserved_membership=[0, 3]))
    local = []
    for nonzero, bridge_zero, bridge_nonzero in product((1, 2), (False, True), (False, True)):
        q_palette = U - {0, nonzero}
        q_bridges = ({0} if bridge_zero else set()) | ({nonzero} if bridge_nonzero else set())
        q_exterior = ({0} if not bridge_zero else set()) | ({nonzero} if not bridge_nonzero else set())
        assert U - q_exterior == q_palette | q_bridges
        pa_bridges = ({0} if bridge_zero else set()) | ({1} if bridge_nonzero else set())
        pa_exterior = ({0} if not bridge_zero else set()) | ({1} if not bridge_nonzero else set())
        assert U - pa_exterior == {2, 3} | pa_bridges
        local.append(dict(Q_cycle_palette=sorted(q_palette), PA_cycle_palette=[2, 3],
            outside_directions=[dict(Q_color=0, PA_color=0, is_bridge=bridge_zero,
                                     actual_terminal_envelope=['b', 'b0']),
                                dict(Q_color=nonzero, PA_color=1, is_bridge=bridge_nonzero,
                                     actual_terminal_envelope=[f'b{1 if nonzero == 1 else 4}'])],
            degree=4))
    return dict(block_membership_constraints=records, cycle_vertex_local_cases=local,
        scope='Local palette algebra; block incidence independence and tether existence are paper')


def connected(vertices, edges):
    seen, todo = set(), [min(vertices)]
    while todo:
        v = todo.pop()
        if v in seen:
            continue
        seen.add(v)
        todo.extend(w if v == z else z for z, w in edges
                    if v in (z, w) and {z, w} <= vertices)
    return seen == vertices


def minor_samples():
    records = []
    for length, color, depth in product((3, 5, 7, 9), (1, 2), (0, 1, 2)):
        terminal = 1 if color == 1 else 4
        other = 4 if color == 1 else 1
        cycle = list(range(6, 6 + length))
        edges = FRAME | {(1, 5), (4, 5)}
        edges |= {edge(cycle[i], cycle[(i+1) % length]) for i in range(length)}
        tethers, zero_inside, other_inside = [], set(), set()
        nxt = 6 + length
        for i, v in enumerate(cycle):
            for label, end in ((0, 5 if i == 0 else 0), (color, terminal)):
                inside = list(range(nxt, nxt + depth))
                nxt += depth
                path = [v, *inside, end]
                edges |= {edge(a, b) for a, b in zip(path, path[1:])}
                (zero_inside if label == 0 else other_inside).update(inside)
                tethers.append(dict(cycle_vertex=v, Q_label=label, path=path))
        assert all(sum(v in e for e in edges) == 4 for v in cycle)
        parts = [set(cycle[:length//3]), set(cycle[length//3:2*length//3]),
                 set(cycle[2*length//3:]), {0, 5, other} | zero_inside,
                 {terminal} | other_inside]
        assert all(parts) and all(connected(p, edges) for p in parts)
        assert all(not (a & b) for a, b in combinations(parts, 2))
        adjacency = []
        for i, j in combinations(range(5), 2):
            original = next(e for e in sorted(edges)
                            if (e[0] in parts[i] and e[1] in parts[j])
                            or (e[1] in parts[i] and e[0] in parts[j]))
            adjacency.append(dict(branch_pair=[i, j], original_edge=original))
        inner = set(range(6, nxt))
        assert connected(inner, edges)
        assert sum(5 in e and bool(set(e) & inner) for e in edges) == 1
        records.append(dict(odd_cycle_length=length, Q_nonzero_tether_color=color,
            Q_cycle_palette=sorted(U - {0, color}), subdivision_depth=depth,
            boundary_order=list(range(5)), hub=5, hub_spokes=[1, 4],
            one_original_unary_contact=tethers[0]['path'][-2],
            tethers=tethers, original_edges=sorted(edges),
            zero_hub_connecting_path=[5, other, 0],
            K5_branch_sets=[sorted(p) for p in parts], ten_original_adjacencies=adjacency,
            scope='Extracted-shape minor control; intermediate vertices need not have full degree four'))
    assert len(records) == 24
    return records


def graph_controls():
    records, negative, collision = [], None, None
    direct_checks, pinned_checks = 0, 0
    c_shapes = [('singleton', [7], set(), {7: [1, 4]}, 7, 7),
                ('edge', [7, 8], {(7, 8)}, {7: [1, 2], 8: [3, 4]}, 7, 8),
                ('triangle', [7, 8, 9], {(7, 8), (7, 9), (8, 9)},
                 {7: [1], 8: [4], 9: [2, 3]}, 7, 8)]
    for ckind, cv, ce, ca, x, y in c_shapes:
        start = max(cv) + 1
        unary_shapes = [
            ('singleton', [start], set(), {start: [0, 1, 4]}),
            ('edge', [start, start+1], {(start, start+1)},
             {start: [1, 4], start+1: [0, 1, 4]}),
            ('path', list(range(start, start+3)), {(start, start+1), (start+1, start+2)},
             {start: [1, 4], start+1: [0, 1], start+2: [0, 1, 4]}),
            ('triangle', list(range(start, start+3)),
             {(start, start+1), (start, start+2), (start+1, start+2)},
             {start: [1], start+1: [0, 1], start+2: [0, 4]}),
            ('triangle_one_terminal', list(range(start, start+3)),
             {(start, start+1), (start, start+2), (start+1, start+2)},
             {start: [1], start+1: [0, 1], start+2: [0, 1]})]
        for ukind, uv, ue, ua in unary_shapes:
            u = uv[0]
            c_edges = ce | {edge(v, i) for v in cv for i in ca[v]}
            u_edges = ue | {edge(v, i) for v in uv for i in ua[v]}
            source_edges = (FRAME | c_edges | u_edges | {(5, 6), edge(6, x), edge(5, y), edge(5, u)}
                            | {edge(6, i) for i in (1, 2, 3)} | {(1, 5), (4, 5)})
            interior, ports = [5, 6, *cv, *uv], [5, 6, y, u]
            order = sorted(B | set(interior))
            assert all(sum(v in e for e in source_edges) == (5 if v in (5, 6) else 4)
                       for v in interior)
            rows = []
            for ri, row in enumerate(ROWS):
                cr = witnesses(cv, c_edges, row, [x, y])
                ur = witnesses(uv, u_edges, row, [u])
                assert cr and ur
                for t, f in cr.items():
                    validate_witness(f, sorted(B | set(cv)), c_edges, row, [x, y], t)
                for t, f in ur.items():
                    validate_witness(f, sorted(B | set(uv)), u_edges, row, [u], t)
                variants = []
                for omitted in (None, 1, 3):
                    actual = source_edges if omitted is None else source_edges - {edge(6, omitted)}
                    support = {1, 2, 3} - ({omitted} if omitted is not None else set())
                    joined = {}
                    k_relation = {}
                    k_order = sorted(B | {6} | set(cv))
                    for (xc, yc), cf in sorted(cr.items()):
                        for ac in sorted(U - {row[i] for i in support} - {xc}):
                            k_coloring = dict(zip(sorted(B | set(cv)), cf)) | {6: ac}
                            k_relation.setdefault((ac, yc), [k_coloring[v] for v in k_order])
                            for (uc,), uf in sorted(ur.items()):
                                for bc in sorted(U - {row[i] for i in (1, 4)} - {ac, yc, uc}):
                                    coloring = dict(zip(sorted(B | set(cv)), cf))
                                    coloring.update(zip(sorted(B | set(uv)), uf))
                                    coloring.update({5: bc, 6: ac})
                                    t = (bc, ac, yc, uc)
                                    f = [coloring[v] for v in order]
                                    joined.setdefault(t, f)
                    direct = colorings(interior, actual, dict(enumerate(row)))
                    assert set(joined) == {tuple(f[v] for v in ports) for f in direct}
                    direct_checks += 1
                    for t, f in joined.items():
                        validate_witness(f, order, actual, row, ports, t)
                    k_edges = c_edges | {edge(6, x)} | {edge(6, i) for i in support}
                    for t, f in k_relation.items():
                        validate_witness(f, k_order, k_edges, row, [6, y], t)
                    fibers = []
                    for bc, ac in product(sorted(U), repeat=2):
                        fixed = dict(enumerate(row)) | {5: bc, 6: ac}
                        found = [f for f in search(set(interior) - {5, 6}, actual, fixed)
                                 if all(f[v] != f[w] for v, w in actual)]
                        fiber = sorted({(f[y], f[u]) for f in found})
                        assert fiber == sorted({t[2:] for t in joined if t[:2] == (bc, ac)})
                        pinned_checks += 1
                        fibers.append(dict(b_color=bc, a_color=ac, whole_y_u_fiber=fiber))
                    variants.append(dict(omitted_original_spoke=omitted,
                        K_ordered_ports=[6, y], K_vertex_order=k_order,
                        K_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(k_relation.items())],
                        joint_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(joined.items())],
                        pinned_b_a_fibers=fibers))
                restored = {tuple(t['tuple']) for t in variants[0]['joint_tuples']}
                for variant in variants[1:]:
                    e = variant['omitted_original_spoke']
                    tuples = {tuple(t['tuple']) for t in variant['joint_tuples']}
                    assert {t for t in tuples if t[1] != row[e]} == restored
                    if tuples and not restored and negative is None:
                        negative = dict(control_index=len(records), row_index=ri,
                            omitted_original_spoke=e, forced_leaf_color=row[e],
                            nonempty_M_joint=variant['joint_tuples'], restored_G_joint=[])
                if x == y and collision is None:
                    marginals = [{t[j] for t in cr} for j in (0, 1)]
                    for ac, bc in product(sorted(U), repeat=2):
                        if (any(s != ac for s in marginals[0]) and any(t != bc for t in marginals[1])
                                and not any(s != ac and t != bc for s, t in cr)):
                            collision = dict(control_index=len(records), row_index=ri,
                                original_contact_vertices=[x, y], complete_C_tuples=sorted(cr),
                                two_literal_root_queries=[ac, bc], complete_guarded_fiber=[],
                                scope='C query control, before root-spoke eligibility')
                rows.append(dict(row_index=ri, literal_boundary=row,
                    C_complete_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(cr.items())],
                    U_endpoint_tuples=[dict(tuple=t, coloring=f) for t, f in sorted(ur.items())],
                    variants=variants))
            unary_rows = [{t['tuple'][0] for t in r['U_endpoint_tuples']} for r in rows]
            assert {(SWAP[t['tuple'][0]], SWAP[t['tuple'][1]]) for t in rows[1]['C_complete_tuples']} == {
                tuple(t['tuple']) for t in rows[3]['C_complete_tuples']}
            assert unary_rows[1] == unary_rows[3]
            concrete_minor = None
            if unary_rows[0] == unary_rows[1] == {0}:
                assert ukind == 'triangle_one_terminal'
                parts = [{v} for v in uv] + [{0, 4, 5}, {1}]
                assert all(connected(p, source_edges) for p in parts)
                assert all(not (a & b) for a, b in combinations(parts, 2))
                adjacency = []
                for i, j in combinations(range(5), 2):
                    original = next(e for e in sorted(source_edges)
                                    if (e[0] in parts[i] and e[1] in parts[j])
                                    or (e[1] in parts[i] and e[0] in parts[j]))
                    adjacency.append(dict(branch_pair=[i, j], original_edge=original))
                concrete_minor = dict(K5_branch_sets=[sorted(p) for p in parts],
                    ten_original_adjacencies=adjacency,
                    scope='Both unary singleton queries occur in this actual nondisk graph')
            records.append(dict(C_kind=ckind, U_kind=ukind, vertex_order=order,
                root_order=[5, 6], complete_port_order=ports, original_edges=sorted(source_edges),
                C=dict(vertices=cv, internal_edges=sorted(ce), actual_attachments=ca,
                       ordered_root_contacts=[x, y], owners=[6, 5]),
                unary_U=dict(vertices=uv, internal_edges=sorted(ue), actual_attachments=ua,
                             contact=u, owner=5), rows=rows,
                simultaneous_unary_zero_queries_actual_K5=concrete_minor,
                scope='Fixed full graph relation control; no disk, minimality or candidate realization claim'))
    assert len(records) == 15 and direct_checks == 450 and pinned_checks == 7200
    assert negative is not None and collision is not None
    return dict(records=records, independent_whole_graph_checks=direct_checks,
        pinned_b_a_checks=pinned_checks, blocked_nonempty_leaf_fiber=negative,
        marginal_collision=collision)


def build():
    frames, algebra, palettes = named_frames(), relation_algebra(), palette_algebra()
    minors, controls = minor_samples(), graph_controls()
    dependencies = [Path(__file__), SOURCE]
    dependencies += [ROOT / 'scripts' / (name + '.py') for name in (
        'c5_independent_support_capacity', 'c5_excess_one_subcovers', 'c5_941_two_spoke',
        'c5_excess_two_mixed_core_spokes')]
    dependencies += [ROOT / 'docs' / (name + '.md') for name in (
        'c5_excess_two_mixed_core_single_spoke', 'c5_two_spoke_nonadjacent',
        'c5_two_spoke_adjacent_21', 'c5_degree5_tree_components')]
    return dict(schema=1, scope=__doc__, root_color_frame=sorted(U), pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in dependencies},
        named_frame_transports=frames, complete_relation_algebra=algebra,
        palette_algebra=palettes, K5_extracted_shape_certificates=minors,
        fixed_full_graph_controls=controls,
        summary=dict(named_attachment_transports=8, canonical_candidate_sigmas=sorted({r['canonical_sigma'] for r in frames}),
            full_joint_algebra_cases=28, cycle_vertex_palette_cases=8, explicit_K5_controls=24,
            fixed_full_graph_controls=15, independent_whole_graph_checks=450, pinned_b_a_fiber_checks=7200,
            candidate_original_spokes_upper_bounds=[4, 4], five_spoke_original_sources_excluded=True,
            all_original_single_spoke_omissions_excluded=False, epsilon_three_proved=False,
            new_lean_theorem=False, source_graph_enumeration=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=1) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
