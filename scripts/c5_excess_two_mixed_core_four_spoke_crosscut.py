#!/usr/bin/env python3
"""Four-spoke (2,2): an original unary crosscut seals the mixed support.

Read the remaining named frames literally. Fixed rotations, support subsets,
apex subdivisions and exterior hub bags are controls; arbitrary-size coverage
is the paper crosscut plus tight-list/Gallai argument. No source graph catalogue
or source realization is asserted, and no complete six-role equality is claimed.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, U, span
from c5_941_two_spoke import relabel_mask
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_excess_two_mixed_core_four_spoke_short_face import disk_rotations, short_face
from c5_excess_two_mixed_core_four_spoke_long_face import oriented_arc, short_support_instance
from c5_excess_two_four_spoke_binary_star import subdivision, verify_subdivision
from c5_short_support_singleton import connected, local_controls, three_hub_controls
from c5_excess_two_four_spoke_crosscut_joint_controls import fixed_graph_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_crosscut/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_long_face/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
SHORT = ROOT / 'artifacts/c5_short_support_singleton/observations.json'


def edge(a, b):
    return tuple(sorted((a, b)))


def subsets(arc):
    return [tuple(h for i, h in enumerate(arc) if bits >> i & 1)
            for bits in range(1 << len(arc))]


def hub_bags(edges, owner, other, endpoint, equal):
    """Contract an existing original U path only for the topology control."""
    path_vertex = 7
    graph = edges | {edge(owner, path_vertex), edge(path_vertex, endpoint)}
    bags = [[owner, path_vertex, endpoint], [other]] if equal else [
        [owner, path_vertex], [other], [endpoint]]
    assert all(connected(bag, graph) for bag in bags)
    assert all(not set(a) & set(b) for a, b in combinations(bags, 2))
    adjacency = []
    for i, j in combinations(range(len(bags)), 2):
        choices = sorted(e for e in graph if
            (e[0] in bags[i] and e[1] in bags[j]) or
            (e[1] in bags[i] and e[0] in bags[j]))
        assert choices
        adjacency.append(dict(hub_pair=[i, j], original_or_contracted_path_edge=choices[0]))
    neighbor_order = [owner, other, endpoint]
    mapping = [next(i for i, bag in enumerate(bags) if z in bag) for z in neighbor_order]
    assert mapping[0] == mapping[2] if equal else len(set(mapping)) == 3
    return dict(original_exterior_skeleton_edges=sorted(edges),
        original_U_path_roles=[owner, 'internal_path_in_original_U', endpoint],
        contracted_original_U_path_vertex=path_vertex,
        contracted_exterior_control_edges=sorted(graph), connected_hub_bags=bags,
        C_external_neighbor_order=neighbor_order, external_neighbor_to_hub=mapping,
        all_hub_adjacencies=adjacency,
        same_color_external_neighbor_collision=[owner, endpoint] if equal else None,
        collision_excluded_by='Same-row C tightness forbids a vertex adjacent to both equal-color external neighbors'
            if equal else None,
        paper_lemma='two_hub_Gallai_K5' if equal else 'three_hub_Gallai_K5',
        scope='Topology after contracting a path internal to the same original unary; no source-degree claim')


def tightness_rows(frame, owner, other, endpoint, edges):
    roots = frame['original_root_order']
    spokes = dict(zip(roots, frame['original_spoke_supports'], strict=True))
    rows = []
    for ri, row in enumerate(ROWS):
        cases = []
        for ac, bc in product(sorted(U), repeat=2):
            colors = dict(zip(roots, (ac, bc), strict=True))
            if ac == bc or any(colors[r] == row[h] for r in roots for h in spokes[r]):
                continue
            outside = [colors[owner], colors[other], row[endpoint]]
            assert outside[0] != outside[1] and outside[1] != outside[2]
            equal = outside[0] == outside[2]
            bags = hub_bags(edges, owner, other, endpoint, equal)
            auxiliary = [outside[0], outside[1]] if equal else outside
            assert len(set(auxiliary)) == len(auxiliary)
            local = []
            for indices in subsets(range(3)):
                degree = 4 - len(indices)
                forbidden = {outside[i] for i in indices}
                available = sorted(U - forbidden)
                slack = len(available) - degree
                collision = equal and 0 in indices and 2 in indices
                assert slack == len(indices) - len(forbidden) >= 0
                assert (slack > 0) == collision
                mapped = [bags['external_neighbor_to_hub'][i] for i in indices]
                assert (len(set(mapped)) == len(mapped)) == (slack == 0)
                local.append(dict(original_external_neighbor_indices=indices,
                    original_external_neighbors=[bags['C_external_neighbor_order'][i] for i in indices],
                    internal_C_degree=degree, original_external_colors=[outside[i] for i in indices],
                    exact_C_list=available, list_slack=slack,
                    tight=slack == 0, merged_neighbor_collision=collision,
                    C_degree_preserved_by_hub_contraction_if_tight=slack == 0))
            cases.append(dict(original_a_color=ac, original_b_color=bc,
                original_ordered_external_colors=outside,
                root_owner_color_equals_support_endpoint=equal,
                auxiliary_hub_colors=auxiliary, exterior_hub_control=bags,
                all_local_C_external_neighbor_subsets=local))
        rows.append(dict(row_index=ri, literal_boundary=row,
            all_original_spoke_and_ab_legal_root_color_cases=cases))
    return rows


def crosscut_controls(arc, owner, other, edges):
    p, middle, q = arc
    controls = []
    for forbidden_endpoint in (p, middle):
        # Original U and C are disjoint connected components. Contract only
        # paths in U and the connected C, and add an apex outside the C5 disk.
        graph = edges | {edge(owner, 7), edge(7, q), edge(other, 8),
                         edge(owner, 8), edge(8, forbidden_endpoint)}
        graph |= {edge(9, h) for h in B}
        cert = subdivision(tuple(sorted(graph)))
        assert cert is not None
        verify_subdivision(graph, cert)
        controls.append(dict(forbidden_original_C_support_endpoint=forbidden_endpoint,
            alternating_original_face_endpoint_order=[owner, forbidden_endpoint, q, other],
            original_U_crosscut_roles=[owner, 'internal_path_in_original_U', q],
            original_C_crossing_path_roles=[other, 'internal_path_in_original_C', forbidden_endpoint],
            original_C_other_root_contact_preserved=owner,
            contracted_path_vertices=dict(original_U=7, original_C=8),
            outside_boundary_apex=9, contracted_original_skeleton_edges=sorted(graph),
            explicit_apex_K33_subdivision=cert,
            scope='Fixed original disjoint-path topology control; no degree, coloring or realization claim'))
    records = []
    for support in subsets(arc):
        bad = sorted(set(support) - {q})
        records.append(dict(actual_original_C_support=support,
            compatible_with_original_U_crosscut=not bad,
            violating_actual_support_endpoints=bad,
            alternating_original_path_control_indices=[i for i, c in enumerate(controls)
                if c['forbidden_original_C_support_endpoint'] in bad]))
    assert len(records) == 8 and sum(r['compatible_with_original_U_crosscut'] for r in records) == 2
    return dict(original_face_boundary_arc=arc,
        original_U_actual_path_required_endpoint=q,
        original_C_sealed_actual_support_envelope=[q],
        all_actual_original_C_support_subsets=records,
        alternating_original_path_controls=controls,
        scope='All actual support subsets within this one fixed original common face')


def frame_analysis(frame, original):
    assert frame['original_root_order'] == original['root_order']
    assert frame['original_spoke_supports'] == original['original_spoke_supports']
    assert frame['original_root_and_boundary_edges'] == original['retained_source_edges']
    assert frame['inherited_skeleton_apex_rotation'] == original['apex_rotation']
    roots = frame['original_root_order']
    edges = set(map(tuple, frame['original_root_and_boundary_edges']))
    rotations = disk_rotations(edges)
    faces = rotations['all_original_C5_outer_face_rotations'][0]['original_disk_faces']
    common = [f for f in faces if all(r in f for r in roots)]
    assert len(common) == 2
    owners, qualified = [], []
    for r in roots:
        incident = [f for f in faces if r in f]
        long = [f for f in incident if span(set(f) & B) >= 2]
        short = [f for f in incident if span(set(f) & B) <= 1]
        eligible = len(long) == 1 and long[0] in common and len(set(long[0]) & B) == 3
        owners.append(dict(original_owner=r, all_incident_faces=incident,
            long_incident_faces=long, short_incident_face_lemma_instances=[
                short_face(f, r, roots, edges) for f in short],
            only_long_face_is_common_two_edge_boundary_arc=eligible))
        if eligible:
            qualified.append((r, long[0]))
    assert len(qualified) <= 1
    result = {k: v for k, v in frame.items() if k != 'status'}
    result.update(inherited_status=frame['status'],
        status='excluded_by_original_unary_crosscut_and_mixed_hubs' if qualified else
            'unequal_original_pairs_unresolved',
        exhaustive_fixed_skeleton_rotations=rotations,
        original_unary_incident_face_analysis=owners,
        excluded_by_original_unary_crosscut_and_mixed_hubs=bool(qualified))
    if not qualified:
        return result
    (owner, face), = qualified
    other, = set(roots) - {owner}
    arc = oriented_arc(face, [owner, other])
    assert len(arc) == 3
    p, middle, q = arc
    shared, = set(frame['original_spoke_supports'][0]) & set(frame['original_spoke_supports'][1])
    triangle, = [f for f in common if f != face]
    assert set(triangle) == {owner, other, shared}
    assert edge(other, q) in edges and edge(owner, shared) in edges
    supports = []
    for support in subsets(arc):
        nonshort = span(set(support)) >= 2
        assert nonshort == ({p, q} <= set(support))
        supports.append(dict(actual_original_forced_unary_support=support,
            minimal_cyclic_support_span=span(set(support)),
            compatible_with_original_unary_edge_criticality=nonshort,
            contains_both_fixed_arc_endpoints={p, q} <= set(support),
            short_support_lemma_instance=None if nonshort else
                short_support_instance(support, owner, roots, edges)))
    assert len(supports) == 8 and sum(s['compatible_with_original_unary_edge_criticality'] for s in supports) == 2
    result.update(original_forced_unary_owner=owner, original_other_root=other,
        original_common_boundary_vertex=shared, original_common_long_face=face,
        original_common_two_edge_boundary_arc=arc,
        original_fixed_arc_endpoints=[p, q], original_common_short_triangle_face=triangle,
        all_actual_forced_unary_support_subsets=supports,
        original_C_possible_faces=[dict(original_face=triangle,
            original_boundary_envelope=[shared], original_exterior_hubs=[owner, other, shared],
            original_exterior_hub_edges=sorted(edge(z, w) for z, w in combinations((owner, other, shared), 2))),
            dict(original_face=face, original_boundary_envelope=arc,
                crosscut_reduced_actual_support_envelope=[q])],
        original_C_support_separation_controls=crosscut_controls(arc, owner, other, edges),
        original_C_extension_tightness_rows=tightness_rows(frame, owner, other, q, edges),
        chosen_noncritical_original_mixed_contact_edge_role='a-x',
        chosen_noncritical_original_mixed_contact_owner=roots[0],
        original_relation_conclusion='pi_(a,b,u,v) J_G = J_(G-C); each original G-C coloring extends by replacing only original C',
        original_edge_conclusion='Sigma(G-ax)=Sigma(G); ax is one fixed original contact edge',
        paper_dependencies=['original disk crosscut separation', 'connected degree-list slack and Gallai characterization',
                            'connected exterior K4-block exclusion', 'two_hub_Gallai_K5', 'three_hub_Gallai_K5'])
    return result


def d5_checks(record):
    edges = set(map(tuple, record['original_root_and_boundary_edges']))
    owner, other = record['original_forced_unary_owner'], record['original_other_root']
    arc = record['original_common_two_edge_boundary_arc']
    support_checks = row_checks = subdivision_checks = 0
    for sign, shift in product((-1, 1), range(5)):
        move = [(sign * h + shift) % 5 for h in range(5)]
        rename = lambda z: move[z] if z in B else z
        moved_edges = {edge(rename(z), rename(w)) for z, w in edges}
        moved_arc = list(map(rename, arc))
        assert all(edge(z, w) in FRAME for z, w in zip(moved_arc, moved_arc[1:]))
        for support in record['all_actual_forced_unary_support_subsets']:
            actual = set(map(rename, support['actual_original_forced_unary_support']))
            assert span(actual) == support['minimal_cyclic_support_span']
            assert ({moved_arc[0], moved_arc[-1]} <= actual) == support['contains_both_fixed_arc_endpoints']
            if (instance := support['short_support_lemma_instance']) is not None:
                pair = set(map(rename, instance['enclosing_original_boundary_edge']))
                path = list(map(rename, instance['original_external_path']))
                assert actual <= pair and path[-1] not in pair
                assert all(edge(z, w) in moved_edges for z, w in zip(path, path[1:]))
            support_checks += 1
        for item in record['original_C_support_separation_controls']['all_actual_original_C_support_subsets']:
            actual = set(map(rename, item['actual_original_C_support']))
            assert (actual <= {moved_arc[-1]}) == item['compatible_with_original_U_crosscut']
            support_checks += 1
        for control in record['original_C_support_separation_controls']['alternating_original_path_controls']:
            graph = {edge(rename(z), rename(w)) for z, w in control['contracted_original_skeleton_edges']}
            cert = control['explicit_apex_K33_subdivision']
            moved = dict(left=list(map(rename, cert['left'])), right=list(map(rename, cert['right'])),
                paths=[list(map(rename, path)) for path in cert['paths']])
            verify_subdivision(graph, moved)
            subdivision_checks += 1
        for row_record in record['original_C_extension_tightness_rows']:
            row = row_record['literal_boundary']
            tr = transport(row, move)
            assert all(tr['transported_row'][move[h]] == tr['color_permutation'][row[h]] for h in B)
            for case in row_record['all_original_spoke_and_ab_legal_root_color_cases']:
                colors = dict(zip(record['original_root_order'],
                    (case['original_a_color'], case['original_b_color']), strict=True))
                cp = tr['color_permutation']
                moved_colors = [cp[colors[owner]], cp[colors[other]], tr['transported_row'][moved_arc[-1]]]
                assert moved_colors == [cp[c] for c in case['original_ordered_external_colors']]
                assert (moved_colors[0] == moved_colors[2]) == case['root_owner_color_equals_support_endpoint']
                for local in case['all_local_C_external_neighbor_subsets']:
                    available = U - {moved_colors[i] for i in local['original_external_neighbor_indices']}
                    assert available == {cp[c] for c in local['exact_C_list']}
                row_checks += 1
    return support_checks, row_checks, subdivision_checks


def selected_geometry_transport(targets):
    original = next(f for t in targets if t['source_sigma'] == 933
                    for f in t['newly_excluded_frame_analyses'] if f['inherited_named_skeleton_index'] == 100)
    destination = next(f for t in targets if t['source_sigma'] == 941
                       for f in t['newly_excluded_frame_analyses'] if f['inherited_named_skeleton_index'] == 134)
    move = [1, 0, 4, 3, 2]
    rename = lambda z: move[z] if z in B else z
    assert {edge(rename(z), rename(w)) for z, w in original['original_root_and_boundary_edges']} == \
        set(map(tuple, destination['original_root_and_boundary_edges']))
    assert [sorted(move[h] for h in s) for s in original['original_spoke_supports']] == \
        destination['original_spoke_supports']
    assert list(map(rename, original['original_common_two_edge_boundary_arc'])) == \
        destination['original_common_two_edge_boundary_arc']
    rows = [transport(row, move) for row in ROWS]
    moved_sigma = relabel_mask(933, move)
    assert moved_sigma == 940 and moved_sigma != 941
    for item in rows:
        assert all(item['transported_row'][move[h]] == item['color_permutation'][item['source_row'][h]] for h in B)
    return dict(original_source_sigma=933, original_named_skeleton_index=100,
        comparison_source_sigma=941, comparison_named_skeleton_index=134,
        original_spokes=original['original_spoke_supports'],
        transported_spokes=destination['original_spoke_supports'],
        one_global_boundary_permutation=move, original_roots_unchanged=True,
        all_ten_simultaneous_boundary_and_color_transports=rows,
        transported_original_source_sigma=moved_sigma,
        compared_source_masks_equal=False,
        scope='One whole-graph D5 geometry transport; 933 maps to Sigma 940, so it does not identify the 933 and 941 source relations')


def build():
    previous, source, short = (json.loads(p.read_text()) for p in (PREVIOUS, SOURCE, SHORT))
    assert json.loads(json.dumps(local_controls())) == short['local_controls']
    assert json.loads(json.dumps(three_hub_controls())) == short['three_hub_controls']
    targets, counts, root_swaps = [], [0, 0, 0], []
    for target in previous['targets']:
        sigma = target['source_sigma']
        original = next(t for t in source['targets'] if t['source_sigma'] == sigma)
        records = original['named_spoke_skeletons']['records']
        analyses, excluded, remaining = [], [], []
        for frame in target['remaining_unequal_pair_frames']:
            if len(set(frame['original_spoke_supports'][0]) & set(frame['original_spoke_supports'][1])) != 1:
                remaining.append(frame)
                continue
            record = frame_analysis(frame, records[frame['inherited_named_skeleton_index']])
            analyses.append(record)
            if record['excluded_by_original_unary_crosscut_and_mixed_hubs']:
                excluded.append(record)
                counts = [a + b for a, b in zip(counts, d5_checks(record), strict=True)]
            else:
                remaining.append(frame)
        expected = [100, 113, 116, 127, 156, 162, 172, 190] if sigma == 933 else [
            134, 137, 156, 160, 174, 181, 196, 222, 237, 245, 262, 266, 280, 281, 305, 306]
        assert [f['inherited_named_skeleton_index'] for f in excluded] == expected
        assert (len(analyses), len(excluded), len(remaining)) == ((8, 8, 14) if sigma == 933 else (22, 16, 24))
        for record in excluded:
            a, b = record['original_root_order']
            swap = lambda z: b if z == a else a if z == b else z
            es = {edge(swap(z), swap(w)) for z, w in record['original_root_and_boundary_edges']}
            partner, = [f for f in excluded if set(map(tuple, f['original_root_and_boundary_edges'])) == es]
            assert partner['original_spoke_supports'] == record['original_spoke_supports'][::-1]
            assert partner['original_forced_unary_owner'] == swap(record['original_forced_unary_owner'])
            assert partner['original_common_two_edge_boundary_arc'] == record['original_common_two_edge_boundary_arc']
            root_swaps.append(dict(source_sigma=sigma,
                original_named_skeleton_index=record['inherited_named_skeleton_index'],
                root_swapped_named_skeleton_index=partner['inherited_named_skeleton_index'],
                original_forced_unary_owner=record['original_forced_unary_owner'],
                root_swapped_forced_unary_owner=partner['original_forced_unary_owner']))
        targets.append(dict(source_sigma=sigma,
            inherited_remaining_unequal_pair_frames=len(target['remaining_unequal_pair_frames']),
            one_common_boundary_vertex_analysis=analyses,
            newly_excluded_named_frame_indices=expected, newly_excluded_frame_analyses=excluded,
            remaining_unequal_pair_frames=remaining,
            remaining_one_common_vertex_frames=sum(len(set(f['original_spoke_supports'][0]) &
                set(f['original_spoke_supports'][1])) == 1 for f in remaining),
            remaining_disjoint_pair_frames=sum(not(set(f['original_spoke_supports'][0]) &
                set(f['original_spoke_supports'][1])) for f in remaining)))
    controls = fixed_graph_controls()
    inputs = [Path(__file__), PREVIOUS, SOURCE, SHORT,
        ROOT / 'scripts/c5_excess_two_mixed_core_four_spoke_short_face.py',
        ROOT / 'scripts/c5_excess_two_mixed_core_four_spoke_long_face.py',
        ROOT / 'scripts/c5_excess_two_four_spoke_binary_star.py',
        ROOT / 'scripts/c5_excess_two_four_spoke_crosscut_joint_controls.py']
    legal_cases = [case for t in targets for f in t['newly_excluded_frame_analyses']
        for row in f['original_C_extension_tightness_rows']
        for case in row['all_original_spoke_and_ab_legal_root_color_cases']]
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        original_joint_contract=dict(component_order=['C', 'U-at-a', 'V-at-b'],
            port_order=['a', 'b', 'x', 'y', 'u', 'v'],
            shared_contact_is_one_original_vertex=True,
            guards=['a!=b', 'a!=x', 'b!=y', 'a!=u', 'b!=v'],
            actual_supports_and_fixed_original_face_preserved=True,
            literal_original_C_relation_retained=True,
            C_extension_equality='pi_(a,b,u,v) J_G = J_(G-C)',
            C_replacement_preserves_all_original_vertices_outside_C=True,
            chosen_noncritical_original_edge_role='a-x',
            fixed_original_face_choice_before_boundary_row=True,
            full_six_role_joint_equality_claimed=False),
        inherited_short_support_mathematical_payload_audit=dict(local_controls_equal=True,
            three_hub_controls_equal=True, old_artifacts_rewritten=False),
        targets=targets, root_swap_named_frame_controls=root_swaps,
        selected_original_933_to_941_geometry_transport=selected_geometry_transport(targets),
        fixed_complete_degree_graph_controls=controls,
        summary=dict(source_sigmas=[933, 941], inherited_unequal_pair_frames=[22, 40],
            newly_excluded_crosscut_frames=[8, 16], remaining_unequal_pair_frames=[14, 24],
            remaining_one_common_vertex_frames=[0, 6], remaining_disjoint_pair_frames=[14, 18],
            selected_original_indices=[[100, 156], [134, 174]],
            selected_01_13_and_01_03_with_root_swaps_excluded=True,
            fixed_skeleton_rotation_assignments=96 * 30, valid_disk_skeleton_rotations=2 * 30,
            actual_forced_unary_support_subsets=8 * 24,
            criticality_compatible_forced_unary_support_subsets=2 * 24,
            actual_original_C_support_subsets=8 * 24,
            crosscut_compatible_original_C_support_subsets=2 * 24,
            explicit_apex_K33_subdivisions=2 * 24,
            original_spoke_and_ab_legal_root_color_cases=len(legal_cases),
            same_color_two_hub_cases=sum(c['root_owner_color_equals_support_endpoint'] for c in legal_cases),
            distinct_color_three_hub_cases=sum(not c['root_owner_color_equals_support_endpoint'] for c in legal_cases),
            exact_local_C_tightness_cases=8 * len(legal_cases),
            root_swap_frame_checks=len(root_swaps), simultaneous_D5_support_subset_checks=counts[0],
            simultaneous_D5_row_root_color_checks=counts[1], D5_subdivision_path_checks=counts[2],
            selected_933_geometry_transport_sigma=940,
            selected_933_and_941_transported_source_masks_equal=False,
            fixed_complete_degree_graph_control_summary=controls['summary'],
            all_22_mixed_11_two_unary_sources_excluded=False,
            source_graphs_enumerated=False, epsilon_three_proved=False, new_lean_theorem=False))


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
