#!/usr/bin/env python3
"""Four-spoke (2,2): close the remaining disjoint original spoke pairs.

Only the inherited named skeletons, their rotations and actual support subsets
are enumerated. Arbitrary-size coverage is the paper disk crosscut plus the
existing short-support theorem. Complete C/U/V relations remain literal; a fixed
original unary witness is replaced and the other original vertices are fixed.
Prior complete-degree 01/04 graph controls are audited as conditional algebra
controls, not relabeled or presented as graphs with the new disjoint spokes.
"""
import argparse
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, span
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_excess_two_mixed_core_four_spoke_short_face import rotation_faces, short_face
from c5_excess_two_mixed_core_four_spoke_long_face import oriented_arc, short_support_instance
from c5_excess_two_four_spoke_binary_star import subdivision, verify_subdivision
from c5_excess_two_four_spoke_long_face_joint_controls import fixed_graph_controls
from c5_short_support_singleton import local_controls, three_hub_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_short_arc/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
SHORT = ROOT / 'artifacts/c5_short_support_singleton/observations.json'
OLD_LONG = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_long_face/observations.json'
CHAIN_FILES = [ROOT / f'artifacts/c5_excess_two_mixed_core_four_spoke_{name}/observations.json'
               for name in ('equal_pair', 'short_face', 'long_face', 'crosscut', 'short_arc')]


def edge(z, w):
    return tuple(sorted((z, w)))


def subsets(arc):
    return [tuple(z for j, z in enumerate(arc) if bits >> j & 1)
            for bits in range(1 << len(arc))]


def disjoint_disk_rotations(edges):
    vertices = sorted({z for e in edges for z in e})
    options = []
    for z in vertices:
        ns = sorted(w if v == z else v for v, w in edges if z in (v, w))
        options.append([(ns[0], *p) for p in permutations(ns[1:])])
    checked, records = 0, []
    for rings in product(*options):
        checked += 1
        rotation = dict(zip(vertices, rings, strict=True))
        faces = rotation_faces(rotation)
        outer = [f for f in faces if len(f) == 5 and set(f) == B]
        if len(vertices) - len(edges) + len(faces) != 2 or len(outer) != 1:
            continue
        inner = [f for f in faces if f != outer[0]]
        records.append(dict(rotation=[dict(vertex=z, ring=rotation[z]) for z in vertices],
            original_outer_boundary_face=outer[0], original_disk_faces=inner))
    assert checked == 64 and len(records) == 2
    assert {frozenset(f) for f in records[0]['original_disk_faces']} == {
        frozenset(f) for f in records[1]['original_disk_faces']}
    return dict(rotation_assignments_checked=checked,
        all_original_C5_outer_face_rotations=records,
        mirror_disk_face_vertex_sets_equal=True,
        scope='All rotations of this fixed seven-vertex named skeleton; no source graph catalogue')


def support_controls(arc, roots, edges):
    assert len(arc) == 3
    a, b = roots
    position = {z: j for j, z in enumerate(arc)}
    crossings = []
    for j in range(1, 3):
        for k in range(j):
            es = edges | {edge(a, 7), edge(7, arc[j]), edge(b, 8), edge(8, arc[k])}
            es |= {edge(9, h) for h in B}
            cert = subdivision(tuple(sorted(es)))
            assert cert is not None
            verify_subdivision(es, cert)
            crossings.append(dict(a_support_endpoint=arc[j], b_support_endpoint=arc[k],
                original_alternating_face_endpoints=[a, arc[k], arc[j], b],
                original_U_path_roles=[a, 'path_internal_to_original_U', arc[j]],
                original_V_path_roles=[b, 'path_internal_to_original_V', arc[k]],
                contracted_original_path_vertices=dict(U=7, V=8), outside_boundary_apex=9,
                contracted_original_skeleton_edges=sorted(es), explicit_apex_K33_subdivision=cert,
                scope='Topology after contracting original disjoint component paths; no coloring or degree claim'))
    records, ordered, nonempty, both_long = [], 0, 0, 0
    for su, sv in product(subsets(arc), repeat=2):
        pu, pv = [position[z] for z in su], [position[z] for z in sv]
        diameters = [max(p) - min(p) if p else 0 for p in (pu, pv)]
        compatible = not su or not sv or max(pu) <= min(pv)
        both = span(set(su)) >= 2 and span(set(sv)) >= 2
        crossing, short = None, []
        if compatible:
            ordered += 1
            nonempty += bool(su and sv)
            assert sum(diameters) <= 2
            for support, owner, diameter in zip((su, sv), roots, diameters, strict=True):
                if diameter <= 1:
                    short.append(short_support_instance(support, owner, roots, edges))
            assert short
        else:
            crossing, = [i for i, c in enumerate(crossings)
                if c['a_support_endpoint'] == arc[max(pu)]
                and c['b_support_endpoint'] == arc[min(pv)]]
        if both:
            both_long += 1
            assert not compatible and crossing is not None
        records.append(dict(actual_original_U_support=su, actual_original_V_support=sv,
            fixed_original_arc_positions=[pu, pv], original_support_interval_diameters=diameters,
            minimal_cyclic_support_spans=[span(set(su)), span(set(sv))],
            original_disjoint_path_order_compatible=compatible,
            original_alternating_path_control_index=crossing,
            both_original_supports_nonshort=both,
            certified_short_original_unaries=short,
            fixed_noncritical_original_unary_owner=short[0]['original_unary_owner'] if short else None,
            edge_choice_before_boundary_row=True))
    assert len(records) == 64 and ordered == 32 and nonempty == 17 and both_long == 4
    return dict(common_original_face_boundary_arc=arc, original_boundary_arc_edge_count=2,
        all_actual_original_support_pairs=records, alternating_original_path_controls=crossings,
        total_support_pairs=64, order_compatible_pairs_including_empty=ordered,
        order_compatible_nonempty_pairs=nonempty, both_nonshort_pairs=both_long,
        order_compatible_both_nonshort_pairs=0,
        shared_boundary_endpoint_allowed=True,
        scope='All actual support subsets of this one fixed original common face')


def frame_analysis(frame, original):
    assert frame['original_root_order'] == original['root_order']
    assert frame['original_spoke_supports'] == original['original_spoke_supports']
    assert frame['original_root_and_boundary_edges'] == original['retained_source_edges']
    assert frame['inherited_skeleton_apex_rotation'] == original['apex_rotation']
    assert not set(frame['original_spoke_supports'][0]) & set(frame['original_spoke_supports'][1])
    roots = frame['original_root_order']
    edges = set(map(tuple, frame['original_root_and_boundary_edges']))
    rotations = disjoint_disk_rotations(edges)
    faces = rotations['all_original_C5_outer_face_rotations'][0]['original_disk_faces']
    apex_faces = [f for f in rotation_faces(dict(enumerate(original['apex_rotation'])))
                  if original['boundary_apex'] not in f]
    assert {frozenset(f) for f in faces} == {frozenset(f) for f in apex_faces}
    owners = []
    for r in roots:
        incident = [f for f in faces if r in f]
        assert len(incident) == 3
        long = [f for f in incident if span(set(f) & B) >= 2]
        owners.append(dict(original_owner=r, all_original_incident_faces=incident,
            long_original_incident_faces=long,
            short_original_face_lemma_instances=[short_face(f, r, roots, edges)
                for f in incident if span(set(f) & B) <= 1]))
    short_owners = [r['original_owner'] for r in owners if not r['long_original_incident_faces']]
    common_long = (all(len(r['long_original_incident_faces']) == 1 for r in owners)
        and set(owners[0]['long_original_incident_faces'][0]) ==
            set(owners[1]['long_original_incident_faces'][0]))
    assert bool(short_owners) != common_long
    result = {k: v for k, v in frame.items() if k != 'status'}
    result.update(inherited_status=frame['status'],
        status='excluded_disjoint_original_pairs', exhaustive_fixed_skeleton_rotations=rotations,
        original_unary_face_analysis=owners,
        exclusion_mechanism='all_original_owner_faces_short' if short_owners else
            'same_original_two_edge_face_unary_order',
        all_short_original_unary_owners=short_owners,
        fixed_noncritical_original_owner=short_owners[0] if short_owners else None,
        original_C_relation_and_witness_unchanged=True,
        relation_conclusion='Selected U: pi_(a,b,x,y,v) equality; selected V: pi_(a,b,x,y,u) equality',
        edge_conclusion='One fixed original au or bv has Sigma(G-e)=Sigma(G)',
        full_six_role_joint_equality_claimed=False)
    if common_long:
        face = owners[0]['long_original_incident_faces'][0]
        arc = oriented_arc(face, roots)
        assert len(arc) == 3
        result.update(common_original_long_face=face,
            common_long_original_support_controls=support_controls(arc, roots, edges),
            fixed_edge_selection_scope='Original face placement and actual supports determine the short unary before beta')
    return result


def transport_checks(record):
    roots = record['original_root_order']
    edges = set(map(tuple, record['original_root_and_boundary_edges']))
    support_checks = face_checks = row_checks = subdivisions = 0
    for sign, shift in product((-1, 1), range(5)):
        move = [(sign * h + shift) % 5 for h in range(5)]
        rename = lambda z: move[z] if z in B else z
        moved_edges = {edge(rename(z), rename(w)) for z, w in edges}
        for owner in record['original_unary_face_analysis']:
            for instance in owner['short_original_face_lemma_instances']:
                actual = set(map(rename, instance['exact_face_boundary_envelope']))
                pair = set(map(rename, instance['enclosing_original_boundary_edge']))
                path = list(map(rename, instance['original_external_path']))
                assert actual <= pair and path[-1] not in pair
                assert set(path[1:-1]) <= set(roots) - {owner['original_owner']}
                assert all(edge(z, w) in moved_edges for z, w in zip(path, path[1:]))
                face_checks += 1
        if (controls := record.get('common_long_original_support_controls')) is not None:
            arc = controls['common_original_face_boundary_arc']
            moved_position = {move[z]: j for j, z in enumerate(arc)}
            for item in controls['all_actual_original_support_pairs']:
                su, sv = [set(map(rename, item[key])) for key in
                    ('actual_original_U_support', 'actual_original_V_support')]
                assert [span(su), span(sv)] == item['minimal_cyclic_support_spans']
                assert (span(su) >= 2 and span(sv) >= 2) == item['both_original_supports_nonshort']
                pu, pv = [sorted(moved_position[z] for z in support) for support in (su, sv)]
                assert (not su or not sv or max(pu) <= min(pv)) == item['original_disjoint_path_order_compatible']
                for instance in item['certified_short_original_unaries']:
                    pair = set(map(rename, instance['enclosing_original_boundary_edge']))
                    path = list(map(rename, instance['original_external_path']))
                    actual = set(map(rename, instance['actual_support']))
                    assert actual <= pair and path[-1] not in pair
                    assert all(edge(z, w) in moved_edges for z, w in zip(path, path[1:]))
                support_checks += 1
            for control in controls['alternating_original_path_controls']:
                es = {edge(rename(z), rename(w)) for z, w in control['contracted_original_skeleton_edges']}
                cert = control['explicit_apex_K33_subdivision']
                moved = dict(left=list(map(rename, cert['left'])), right=list(map(rename, cert['right'])),
                    paths=[list(map(rename, path)) for path in cert['paths']])
                verify_subdivision(es, moved)
                subdivisions += 1
            assert all(edge(move[z], move[w]) in FRAME for z, w in zip(arc, arc[1:]))
        for row in ROWS:
            tr = transport(row, move)
            assert all(tr['transported_row'][move[h]] == tr['color_permutation'][row[h]] for h in B)
            row_checks += 1
    return support_checks, face_checks, row_checks, subdivisions


def completion_ledger(new_targets, source):
    """Audit the exact inherited named domain, not the validity of old proofs."""
    old_stages = [json.loads(path.read_text()) for path in CHAIN_FILES]
    ledger = []
    for target in new_targets:
        sigma = target['source_sigma']
        originals = next(t for t in source['targets'] if t['source_sigma'] == sigma)
        originals = originals['named_spoke_skeletons']['records']
        first = next(t for t in old_stages[0]['targets'] if t['source_sigma'] == sigma)
        domain = first['excluded_common_pair_frames'] + first['remaining_unequal_pair_frames']
        indices = {r['inherited_named_skeleton_index'] for r in domain}
        assert len(domain) == len(indices) == first['necessary_named_22_frames'] == (47 if sigma == 933 else 75)
        for frame in domain:
            original = originals[frame['inherited_named_skeleton_index']]
            assert frame['original_root_order'] == original['root_order']
            assert frame['original_spoke_supports'] == original['original_spoke_supports']
            assert frame['original_root_and_boundary_edges'] == original['retained_source_edges']
            assert frame['inherited_skeleton_apex_rotation'] == original['apex_rotation']
        remaining, steps = set(indices), []
        for stage_index, (path, data) in enumerate(zip(CHAIN_FILES, old_stages, strict=True)):
            item = next(t for t in data['targets'] if t['source_sigma'] == sigma)
            excluded = {r['inherited_named_skeleton_index'] for r in item['excluded_common_pair_frames']} \
                if stage_index == 0 else set(item['newly_excluded_named_frame_indices'])
            assert excluded <= remaining
            remaining -= excluded
            assert remaining == {r['inherited_named_skeleton_index'] for r in item['remaining_unequal_pair_frames']}
            steps.append(dict(original_exclusion_artifact=str(path.relative_to(ROOT)),
                excluded_original_named_indices=sorted(excluded), remaining_original_named_frames=len(remaining)))
        final = set(target['newly_excluded_named_frame_indices'])
        assert final == remaining
        steps.append(dict(original_exclusion_artifact=str(OUT.relative_to(ROOT)),
            excluded_original_named_indices=sorted(final), remaining_original_named_frames=0))
        ledger.append(dict(source_sigma=sigma, original_named_frame_total=len(indices),
            complete_original_named_frame_indices=sorted(indices), ordered_exclusion_stages=steps,
            original_skeleton_identity_checked_against_same_source=True,
            all_stage_exclusions_disjoint=True, final_named_domain_empty=True,
            scope='Exact named-domain bookkeeping over existing exclusion certificates; old mathematical proofs are not re-enumerated'))
    return ledger


def build():
    previous, source, short, old_long = (json.loads(p.read_text()) for p in
                                      (PREVIOUS, SOURCE, SHORT, OLD_LONG))
    assert json.loads(json.dumps(local_controls())) == short['local_controls']
    assert json.loads(json.dumps(three_hub_controls())) == short['three_hub_controls']
    prior_controls = fixed_graph_controls()
    assert json.loads(json.dumps(prior_controls)) == old_long['fixed_complete_degree_graph_controls']
    targets, counts, swaps = [], [0, 0, 0, 0], []
    expected_short = {933: [117, 130, 158, 187],
                      941: [161, 178, 200, 218, 240, 265, 285, 301]}
    expected_long = {933: [101, 102, 129, 131, 143, 147, 171, 173, 186, 189],
                     941: [139, 140, 199, 202, 219, 224, 279, 282, 300, 304]}
    for target in previous['targets']:
        sigma = target['source_sigma']
        original = next(t for t in source['targets'] if t['source_sigma'] == sigma)
        records = original['named_spoke_skeletons']['records']
        frames = target['remaining_unequal_pair_frames']
        analyses = [frame_analysis(f, records[f['inherited_named_skeleton_index']]) for f in frames]
        assert len(analyses) == (14 if sigma == 933 else 18)
        classified = [[r['inherited_named_skeleton_index'] for r in analyses
            if r['exclusion_mechanism'] == mechanism] for mechanism in
            ('all_original_owner_faces_short', 'same_original_two_edge_face_unary_order')]
        assert classified == [expected_short[sigma], expected_long[sigma]]
        for record in analyses:
            counts = [a + b for a, b in zip(counts, transport_checks(record), strict=True)]
            a, b = record['original_root_order']
            swap = lambda z: b if z == a else a if z == b else z
            swapped_edges = {edge(swap(z), swap(w)) for z, w in record['original_root_and_boundary_edges']}
            partner, = [r for r in analyses if
                set(map(tuple, r['original_root_and_boundary_edges'])) == swapped_edges]
            assert partner['original_spoke_supports'] == record['original_spoke_supports'][::-1]
            assert partner['exclusion_mechanism'] == record['exclusion_mechanism']
            assert set(partner['all_short_original_unary_owners']) == {
                swap(r) for r in record['all_short_original_unary_owners']}
            if 'common_long_original_support_controls' in record:
                assert partner['common_long_original_support_controls']['common_original_face_boundary_arc'] == \
                    record['common_long_original_support_controls']['common_original_face_boundary_arc'][::-1]
            swaps.append(dict(source_sigma=sigma,
                original_named_skeleton_index=record['inherited_named_skeleton_index'],
                root_swapped_named_skeleton_index=partner['inherited_named_skeleton_index']))
        targets.append(dict(source_sigma=sigma, inherited_remaining_unequal_pair_frames=len(frames),
            newly_excluded_named_frame_indices=[r['inherited_named_skeleton_index'] for r in analyses],
            all_short_owner_frame_indices=classified[0], same_long_face_frame_indices=classified[1],
            newly_excluded_frame_analyses=analyses, remaining_unequal_pair_frames=[],
            remaining_one_common_vertex_frames=0, remaining_disjoint_pair_frames=0))
    ledger = completion_ledger(targets, source)
    inputs = list(dict.fromkeys([Path(__file__), PREVIOUS, SOURCE, SHORT, OLD_LONG, *CHAIN_FILES,
        ROOT / 'scripts/c5_excess_two_mixed_core_four_spoke_short_face.py',
        ROOT / 'scripts/c5_excess_two_mixed_core_four_spoke_long_face.py',
        ROOT / 'scripts/c5_excess_two_four_spoke_binary_star.py',
        ROOT / 'scripts/c5_excess_two_four_spoke_long_face_joint_controls.py']))
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        original_joint_contract=dict(component_order=['C', 'U-at-a', 'V-at-b'],
            port_order=['a', 'b', 'x', 'y', 'u', 'v'], shared_contact_is_one_original_vertex=True,
            original_C_and_other_unary_witnesses_preserved=True,
            complete_original_relations_and_empty_pinned_fibers_retained=True,
            unary_edge_choice_fixed_by_original_geometry_before_boundary_row=True,
            full_six_role_joint_equality_claimed=False),
        inherited_short_support_mathematical_payload_audit=dict(local_controls_equal=True,
            three_hub_controls_equal=True, old_artifacts_rewritten=False),
        inherited_conditional_unary_witness_replacement_audit=dict(
            original_control_artifact=str(OLD_LONG.relative_to(ROOT)),
            complete_original_mathematical_payload_recomputed_equal=True,
            original_control_graph_spokes='01/04 with root exchanges',
            existing_controls_are_new_disjoint_spoke_graphs=False,
            applicability='At least two colors in the same original unary relation permit avoidance of any fixed owner color; preserve every other original vertex',
            summary=prior_controls['summary'],
            scope='Reuse only the finite conditional join/witness replacement audit; arbitrary-size disjoint source exclusion is the paper geometry and short-support theorem'),
        targets=targets, root_swap_named_frame_controls=swaps,
        complete_original_named_subtype_exclusion_ledger=ledger,
        summary=dict(source_sigmas=[933, 941], inherited_unequal_pair_frames=[14, 18],
            newly_excluded_disjoint_pair_frames=[14, 18], all_short_owner_frames=[4, 8],
            common_two_edge_long_face_frames=[10, 10], remaining_unequal_pair_frames=[0, 0],
            remaining_one_common_vertex_frames=[0, 0], remaining_disjoint_pair_frames=[0, 0],
            original_subtype_named_frame_totals=[47, 75],
            original_subtype_completion_scope='Four-spoke (2,2), unique mixed incidence (1,1), one original unary at each root',
            selected_original_indices=[[101, 129], [139, 199]],
            fixed_skeleton_rotation_assignments=64 * 32, valid_disk_skeleton_rotations=2 * 32,
            actual_same_face_support_pairs=64 * 20, both_nonshort_support_pairs=4 * 20,
            order_compatible_both_nonshort_support_pairs=0, explicit_apex_K33_subdivisions=3 * 20,
            root_swap_frame_checks=len(swaps), simultaneous_D5_support_pair_checks=counts[0],
            simultaneous_D5_short_face_path_checks=counts[1], simultaneous_D5_row_checks=counts[2],
            D5_subdivision_path_checks=counts[3],
            prior_complete_degree_graph_controls_recomputed_equal=True,
            complete_original_47_75_named_domain_ledger_checked=True,
            new_complete_degree_disjoint_spoke_graphs_generated=False,
            all_22_mixed_11_two_unary_sources_excluded=True,
            other_22_incidence_subtypes_excluded=False, source_graphs_enumerated=False,
            epsilon_three_proved=False, new_lean_theorem=False))


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
