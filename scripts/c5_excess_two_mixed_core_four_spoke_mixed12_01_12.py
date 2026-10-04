#!/usr/bin/env python3
"""A2: original mixed-(1,2)+a-unary, spokes 01/12 and root swaps.

Read the A ledger without changing its domain. The arbitrary-size exclusion is
the paper actual-U crosscut and three-hub Gallai argument at row 01202. Fixed
rotations, literal singleton relations, minors and complete same-graph joints
are controls, not a source-graph enumeration or disk-realizability certificate.
"""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_independent_support_capacity import B, ROWS, U
from c5_excess_two_mixed_core_four_spoke_mixed12 import named_frame, subsets
from c5_excess_two_four_spoke_mixed12_unary_controls import singleton_schedules
from c5_excess_two_mixed_core_four_spoke_crosscut import hub_bags
from c5_excess_two_four_spoke_binary_star import subdivision, verify_subdivision
from c5_excess_two_four_spoke_mixed12_01_12_joint_controls import build as joint_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed12/observations.json'
GENERIC = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
Q = (0, 1, 2, 0, 2)


def edge(v, w):
    return tuple(sorted((v, w)))


def crosscut(frame):
    a, b = frame['original_a'], frame['original_b']
    edges = set(map(tuple, frame['original_root_and_boundary_edges']))
    records = []
    for endpoint in (0, 4, 3):
        # These two vertices stand for disjoint original paths in U and C;
        # the apex is outside the disk. This is a topology-only control.
        graph = edges | {edge(a, 7), edge(7, 2), edge(b, 8),
                         edge(a, 8), edge(8, endpoint)}
        graph |= {edge(9, h) for h in B}
        cert = subdivision(tuple(sorted(graph)))
        assert cert is not None
        verify_subdivision(graph, cert)
        records.append(dict(forbidden_actual_C_boundary_endpoint=endpoint,
            alternating_original_face_endpoint_order=[a, endpoint, 2, b],
            original_U_path_roles=[a, 'u', 'path_in_original_U', 2],
            original_C_path_roles=[b, 'yj', 'path_in_original_C', endpoint],
            original_other_C_contact_at_a_preserved=True,
            contracted_path_vertices=dict(original_U=7, original_C=8),
            outside_disk_apex=9, contracted_edges=sorted(graph),
            explicit_apex_subdivision=cert))
    supports = [dict(actual_C_support=s,
        compatible_with_same_original_U_crosscut=set(s) <= {2},
        forbidden_actual_endpoints=sorted(set(s)-{2})) for s in subsets([0, 2, 3, 4])]
    assert len(supports) == 16 and sum(s['compatible_with_same_original_U_crosscut'] for s in supports) == 2
    return dict(original_long_face=[a, 0, 4, 3, 2, b], actual_U_endpoint=2,
        all_actual_C_support_subsets=supports, crossing_path_controls=records,
        surviving_actual_C_supports=[[], [2]],
        scope='Fixed disjoint original path controls; arbitrary-size crosscut is a paper argument')


def hub_instance(frame, h):
    a, b = frame['original_a'], frame['original_b']
    edges = set(map(tuple, frame['original_root_and_boundary_edges']))
    if h == 2:
        hubs = hub_bags(edges, a, b, 2, False)
    else:
        assert h == 1
        bags = [[a], [b], [h]]
        adjacency = []
        for i, j in combinations(range(3), 2):
            e = edge(bags[i][0], bags[j][0])
            assert e in edges
            adjacency.append(dict(hub_pair=[i, j], original_edge=e))
        hubs = dict(connected_hub_bags=bags, all_hub_adjacencies=adjacency,
            C_external_neighbor_order=[a, b, h], external_neighbor_to_hub=[0, 1, 2],
            original_edges=sorted(edges), paper_lemma='three_hub_Gallai_K5')
    colors = [3, 0, Q[h]]
    assert len(set(colors)) == 3
    local = []
    for ns in subsets([0, 1, 2]):
        available = sorted(U-{colors[i] for i in ns})
        assert len(available) == 4-len(ns)
        local.append(dict(actual_external_neighbor_indices=ns,
            actual_external_neighbors=[[a, b, h][i] for i in ns],
            internal_C_degree=4-len(ns), exact_C_list=available,
            degree_preserved_by_distinct_hub_mapping=True))
    return dict(original_C_face_kind='short' if h == 1 else 'long',
        actual_C_support_subsets=[[], [h]], original_boundary_hub=h,
        designated_row_index=ROWS.index(Q), literal_boundary=Q,
        original_a_b_u_colors=[3, 0, 2], auxiliary_C_hub_colors=colors,
        original_exterior_hub_instance=hubs,
        all_local_C_external_neighbor_subsets=local,
        x_aliases_keep_both_distinct_root_guards=True,
        conclusion='Original C has a complete extension witness at the fixed exterior colors',
        trust='Paper three-hub lemma, connected-exterior K4 exclusion; not established by these local controls')


def build():
    inherited = json.loads(SOURCE.read_text())
    generic = json.loads(GENERIC.read_text())
    selected, targets, swap_checks = [], [], []
    for target in inherited['targets']:
        sigma = target['source_sigma']
        original = target['remaining_named_original_frames']
        chosen = [f for f in original if f['original_a_spokes'] == [0, 1]
                  and f['original_b_spokes'] == [1, 2]]
        assert len(chosen) == 2
        gt, = [t for t in generic['targets'] if t['source_sigma'] == sigma]
        for f in chosen:
            gi = f['generic_single_spoke_source_index']
            rebuilt = named_frame(sigma, f['original_a'], f['original_b'], [0, 1], [1, 2],
                                  gi, gt['named_spoke_skeletons']['records'][gi])
            assert json.loads(json.dumps(rebuilt)) == f
            expected = [[0, 2, 3], [0, 2, 3, 4]] if sigma == 933 else [
                [0, 2, 3], [2, 3, 4], [0, 2, 3, 4]]
            placements = f['remaining_named_original_U_placements']
            assert {tuple(p['actual_original_U_support']) for p in placements} == set(map(tuple, expected))
            for p in placements:
                screen = singleton_schedules(sigma, [0, 1], p['actual_original_U_support'])
                assert json.loads(json.dumps(screen['surviving_schedules'])) == p['complete_singleton_unary_relation_schedules']
                assert len(screen['surviving_schedules']) == 1
                assert set(screen['surviving_schedules'][0]['singleton_colors']) == {2}
                assert 2 in p['actual_original_U_support']
            assert not sigma >> ROWS.index(Q) & 1
            # The entire long-face envelope is fixed by this SAME literal map.
            stabilizer = (0, 3, 2, 1)
            assert all(stabilizer[Q[h]] == Q[h] for h in (0, 2, 3, 4))
            assert U-{Q[0], Q[1]} == {2, 3}
            assert stabilizer[2] == 2 and stabilizer[3] != 3
            assert 3 not in {Q[0], Q[1]} and 0 not in {Q[1], Q[2]}
            selected.append(dict(named_frame_id=f['named_frame_id'], inherited_complete_named_frame=f,
                inherited_actual_U_face_support_count=len(placements),
                original_U_has_actual_2_attachment=True,
                designated_original_rejected_row=dict(row_index=ROWS.index(Q), literal_boundary=Q,
                    actual_attachment_stabilizer=stabilizer, complete_R_U=[[2]],
                    chosen_original_a_b_u_colors=[3, 0, 2], all_exterior_guards_legal=True),
                long_face_original_crosscut=crosscut(f),
                complete_C_extension_paper_instances=[hub_instance(f, h) for h in (1, 2)],
                status='selected_original_source_excluded_by_designated_row_full_joint',
                claim='A complete (3,0,X,Y0,Y1,2) tuple exists in original J_G(01202)',
                universal_six_role_joint_equality_claimed=False))
        remaining = [f for f in original if f not in chosen]
        counts = dict(remaining_named_frames=len(remaining),
            remaining_actual_U_support_records=sum(len(f['remaining_named_original_U_placements']) for f in remaining),
            remaining_complete_singleton_schedules=sum(len(p['complete_singleton_unary_relation_schedules'])
                for f in remaining for p in f['remaining_named_original_U_placements']))
        assert list(counts.values()) == ([20, 52, 68] if sigma == 933 else [24, 86, 124])
        targets.append(dict(source_sigma=sigma,
            inherited_named_frame_ids=[f['named_frame_id'] for f in original],
            newly_excluded_named_frame_ids=[f['named_frame_id'] for f in chosen],
            complete_remaining_named_original_frames=remaining, summary=counts))
        swap_checks.append(dict(source_sigma=sigma, original_and_swapped_ids=[f['named_frame_id'] for f in chosen],
            whole_frame_root_swap_only=True,
            same_actual_supports_and_literal_singleton_relations=True))
    # Preserve explicit necessary contradictions for EVERY actual support
    # missing 2; do not use an envelope as though it were an actual support.
    missing_2 = []
    for sigma in (933, 941):
        for support in subsets([0, 3, 4]):
            screen = singleton_schedules(sigma, [0, 1], support)
            assert not screen['surviving_schedules']
            missing_2.append(screen)
    controls = joint_controls()
    inputs = [Path(__file__), SOURCE, GENERIC, *[ROOT / 'scripts' / s for s in (
        'c5_excess_two_four_spoke_mixed12_01_12_joint_controls.py',
        'c5_excess_two_mixed_core_four_spoke_mixed12.py',
        'c5_excess_two_four_spoke_mixed12_unary_controls.py',
        'c5_excess_two_mixed_core_four_spoke_crosscut.py',
        'c5_excess_two_four_spoke_binary_star.py',
        'c5_excess_two_four_spoke_mixed12_joint_controls.py',
        'c5_excess_two_mixed_core_spokes.py',
        'c5_941_two_spoke.py', 'c5_independent_support_capacity.py')]]
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        selected_complete_original_frames=selected,
        actual_U_supports_without_2_complete_relation_conflicts=missing_2,
        root_swap_checks=swap_checks, targets=targets,
        fixed_full_degree_same_graph_controls=controls,
        trust_boundary=dict(source_graphs_enumerated=False, old_A_artifact_rewritten=False,
            arbitrary_size_proof='Fixed actual U crosscut, degree lists, connected-exterior K4 and three-hub Gallai',
            finite_control='Four named inherited skeletons, actual supports, minors and full same-graph relations',
            source_realization_claimed=False, entire_mixed_12_subtype_excluded=False,
            epsilon_three_proved=False, new_lean_theorem=False),
        summary=dict(selected_01_12_frames_excluded_with_root_swap=len(selected),
            inherited_selected_actual_U_support_records=[4, 6],
            inherited_selected_singleton_schedules=[4, 6],
            selected_source_residuals=[0, 0], original_apex_crosscut_subdivisions=12,
            paper_designated_row_index=ROWS.index(Q), paper_root_pair=[3, 0], paper_U_color=2,
            remaining_named_frames=[t['summary']['remaining_named_frames'] for t in targets],
            remaining_actual_U_support_records=[t['summary']['remaining_actual_U_support_records'] for t in targets],
            remaining_complete_singleton_schedules=[t['summary']['remaining_complete_singleton_schedules'] for t in targets],
            fixed_full_degree_graph_controls=controls['summary'],
            source_graphs_enumerated=False, epsilon_three_proved=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=1)+'\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
