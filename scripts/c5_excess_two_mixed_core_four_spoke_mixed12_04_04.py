#!/usr/bin/env python3
"""A4: original mixed-(1,2)+a-unary, shared spokes 04/04, root swaps.

Read the A3 ledger verbatim. All four disk rotations of each named skeleton
are retained. The paper proof extends the complete original C at any legal
exterior coloring using its three literal hubs, making original ax noncritical.
Finite full-degree joints and witness replacements audit semantics only.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, ROWS, U, normalize
from c5_excess_two_mixed_core_four_spoke_mixed12 import named_frame, subsets, cycle_key
from c5_excess_two_four_spoke_mixed12_unary_controls import singleton_schedules
from c5_excess_two_four_spoke_mixed12_04_04_joint_controls import build as joint_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_01_01/observations.json'
GENERIC = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
Q = (0, 1, 2, 0, 2)


def edge(v, w):
    return tuple(sorted((v, w)))


def hub_instance(frame, h):
    a, b = frame['original_a'], frame['original_b']
    edges = set(map(tuple, frame['original_root_and_boundary_edges']))
    adjacency = [dict(hub_pair=[v, w], original_edge=edge(v, w))
                 for v, w in combinations((a, b, h), 2)]
    assert all(tuple(r['original_edge']) in edges for r in adjacency)
    colors = []
    for ri, row in enumerate(ROWS):
        allowed = sorted(U - {row[0], row[4]})
        assert len(allowed) == 2
        for ac, bc in product(allowed, repeat=2):
            if ac == bc:
                continue
            hc = row[h]
            assert len({ac, bc, hc}) == 3
            local = []
            for ns in subsets([0, 1, 2]):
                available = sorted(U - {[ac, bc, hc][i] for i in ns})
                assert len(available) == 4 - len(ns)
                local.append(dict(actual_external_neighbor_indices=ns,
                    internal_C_degree=4-len(ns), exact_C_list=available,
                    exact_list_size_equals_internal_degree=True,
                    degree_preserved_by_literal_distinct_hubs=True))
            colors.append(dict(row_index=ri, literal_boundary=row,
                original_a_b_colors=[ac, bc], boundary_hub_color=hc,
                all_local_C_external_neighbor_subsets=local))
    assert len(colors) == 20
    return dict(original_C_face=list(cycle_key([a, b, h])),
        actual_C_support_subsets=[[], [h]],
        empty_actual_support_excluded_by_degree_handshake=True,
        boundary_attachment_edge_count_is_odd='4|C|=2|E(C)|+3+|E(C,B)|',
        possible_actual_C_supports=[[h]], literal_hub_bags=[[a], [b], [h]],
        all_original_hub_adjacencies=adjacency,
        connected_original_exterior_branch_set=[a, b, h],
        extra_original_exterior_path_assumed=False,
        all_legal_root_pair_exact_list_instances=colors,
        paper_conclusion='Complete original C witness exists for each legal exterior coloring',
        trust='Paper degree-list, connected-exterior K4 and three-hub Gallai proof; not a finite general theorem')


def geometry(frame):
    a, b = frame['original_a'], frame['original_b']
    rotations = frame['exhaustive_original_skeleton_rotations']['all_disk_rotations']
    assert len(rotations) == 4
    common = sorted([list(cycle_key([a, b, h])) for h in (0, 4)])
    records = []
    for i, r in enumerate(rotations):
        cf = sorted(f for f in r['original_disk_faces'] if a in f and b in f)
        assert cf == common
        uf = [f for f in r['original_disk_faces'] if a in f]
        placements = []
        for f in uf:
            envelope = sorted(set(f) & B)
            placements.append(dict(original_U_face=f, exact_boundary_envelope=envelope,
                can_have_actual_support_123={1, 2, 3} <= set(envelope),
                compatible_original_C_common_faces=cf))
        records.append(dict(original_rotation_index=i, complete_original_rotation=r,
            original_C_common_faces=cf, all_original_a_incident_U_faces=placements))
    return dict(all_four_original_rotations=records,
        original_C_hub_instances=[hub_instance(frame, h) for h in (0, 4)],
        full_source_touch_all_B_requires_actual_U_support_contains=[1, 2, 3],
        reason='Roots touch only 04; C touches one of 0,4, so original U must touch 1,2,3')


def short_U_external_path_audits(frame):
    """Check inherited short-U path premises without using them to extend C."""
    a, b = frame['original_a'], frame['original_b']
    es = set(map(tuple, frame['original_root_and_boundary_edges']))
    records = []
    for placement in frame['all_original_U_face_support_placements']:
        for support in placement['all_actual_original_U_support_subsets']:
            if support['status'] != 'excluded_original_au_noncritical_short_support':
                continue
            instance = support['original_external_path_lemma_instance']
            pair = set(instance['enclosing_original_boundary_edge'])
            if 'original_external_path' in instance:
                path = instance['original_external_path']
                assert path[0] == a and path[-1] in B-pair
                assert set(path[1:-1]) <= {b}
                assert all(edge(v, w) in es for v, w in zip(path, path[1:]))
                status = 'literal_skeleton_path_verified_avoids_original_C_and_U'
            else:
                assert pair == {0, 4}
                # The original support lemma forces a C attachment outside 04
                # if U is short inside 04, but our fresh C geometry forbids it.
                # This conditional path is not silently replaced by an edge.
                assert instance['original_path_avoids_U']
                assert not instance['skeleton_only_original_path_claimed']
                status = 'full_source_touch_all_B_and_this_short_U_impossible_with_C_geometry'
            records.append(dict(original_U_face=placement['original_U_face'],
                actual_U_support=support['actual_original_U_support'],
                complete_inherited_original_path_instance=instance,
                audited_status=status, used_for_C_extension=False))
    assert records
    return records


def D5_shortcut_diagnostics():
    """Move complete masks/rows/colors; no source exclusion is transported."""
    records = []
    for direction, offset in product((1, -1), range(5)):
        move = [(direction*i+offset) % 5 for i in range(5)]
        if {move[0], move[1]} != {0, 4}:
            continue
        rows = []
        for ri, row in enumerate(ROWS):
            moved = [None]*5
            for v in range(5):
                moved[move[v]] = row[v]
            target = normalize(moved)
            colors = dict(zip(moved, target))
            colors.update(zip(sorted(U-set(colors)), sorted(U-set(colors.values()))))
            perm = [colors[c] for c in sorted(U)]
            assert sorted(perm) == sorted(U)
            assert tuple(perm[c] for c in moved) == target
            rows.append(dict(source_row_index=ri, source_literal_boundary=row,
                moved_literal_boundary_before_shared_color_normalization=moved,
                target_row_index=ROWS.index(target), target_literal_boundary=target,
                single_color_permutation_for_boundary_C_U_and_all_six_roles=perm))
        images = []
        for sigma in (933, 941):
            target = sum(1 << r['target_row_index'] for r in rows
                         if sigma >> r['source_row_index'] & 1)
            assert target not in (933, 941)
            images.append(dict(source_sigma=sigma, target_complete_sigma=target,
                complete_rejected_row_transport=[r for r in rows
                    if not sigma >> r['source_row_index'] & 1]))
        records.append(dict(direction='01_to_04', boundary_vertex_permutation=move,
            full_row_and_common_color_frame_transport=rows, full_sigma_images=images,
            physical_root_roles_fixed=[5, 6], U_owner_role_fixed='a',
            tuple_role_order=['a', 'b', 'x', 'y0', 'y1', 'u'],
            original_relations_or_source_exclusions_transported=False,
            diagnostic='Both candidate masks change; no fixed-mask shortcut used'))
    assert len(records) == 2
    return records


def rotation_signature(record, move=lambda v: v):
    rings = []
    for r in record['rotation']:
        ring = [move(v) for v in r['ring']]
        k = ring.index(min(ring))
        rings.append((move(r['vertex']), tuple(ring[k:] + ring[:k])))
    return tuple(sorted(rings))


def swap_check(left, right):
    move = lambda v: 11-v if v in (5, 6) else v
    assert sorted(edge(move(v), move(w)) for v, w in left['original_root_and_boundary_edges']) == sorted(map(tuple, right['original_root_and_boundary_edges']))
    lr = left['exhaustive_original_skeleton_rotations']['all_disk_rotations']
    rr = right['exhaustive_original_skeleton_rotations']['all_disk_rotations']
    indices = {rotation_signature(r): i for i, r in enumerate(rr)}
    mapping = [indices[rotation_signature(r, move)] for r in lr]
    assert sorted(mapping) == list(range(4))
    for i, r in enumerate(lr):
        moved_faces = sorted([list(cycle_key([move(v) for v in f]))
                              for f in r['original_disk_faces']])
        assert moved_faces == rr[mapping[i]]['original_disk_faces']
        assert cycle_key([move(v) for v in r['original_outer_face']]) == cycle_key(rr[mapping[i]]['original_outer_face'])
    pairs = []
    for p in left['remaining_named_original_U_placements']:
        face = list(cycle_key([move(v) for v in p['original_U_face']]))
        match, = [q for q in right['remaining_named_original_U_placements']
                  if q['original_U_face'] == face and
                  q['actual_original_U_support'] == p['actual_original_U_support']]
        assert match['complete_singleton_unary_relation_schedules'] == p['complete_singleton_unary_relation_schedules']
        assert sorted(mapping[i] for i in p['supporting_original_rotation_indices']) == match['supporting_original_rotation_indices']
        moved_C_faces = sorted([dict(face=list(cycle_key([move(v) for v in q['face']])),
            supporting_rotation_indices=sorted(mapping[i] for i in q['supporting_rotation_indices']))
            for q in p['compatible_original_C_common_faces']], key=lambda q: q['face'])
        assert moved_C_faces == match['compatible_original_C_common_faces']
        pairs.append(dict(original_U_face=p['original_U_face'], swapped_U_face=face,
            actual_U_support=p['actual_original_U_support'],
            complete_literal_singleton_schedules_preserved=True,
            same_rotation_C_face_compatibility_preserved=True))
    return dict(original_frame_id=left['named_frame_id'], swapped_frame_id=right['named_frame_id'],
        vertex_permutation={5: 6, 6: 5}, original_to_swapped_rotation_indices=mapping,
        complete_original_U_placement_bijection=pairs,
        boundary_and_color_frame_fixed=True, original_component_ownership_transported=True)


def build():
    inherited = json.loads(SOURCE.read_text())
    generic = json.loads(GENERIC.read_text())
    selected, targets, swaps = [], [], []
    for target in inherited['targets']:
        sigma = target['source_sigma']
        original = target['complete_remaining_named_original_frames']
        chosen = [f for f in original if f['original_a_spokes'] == f['original_b_spokes'] == [0, 4]]
        assert len(chosen) == 2
        assert sum(len(f['remaining_named_original_U_placements']) for f in chosen) == (4 if sigma == 933 else 12)
        assert sum(len(p['complete_singleton_unary_relation_schedules']) for f in chosen
                   for p in f['remaining_named_original_U_placements']) == (6 if sigma == 933 else 18)
        gt, = [t for t in generic['targets'] if t['source_sigma'] == sigma]
        for f in chosen:
            gi = f['generic_single_spoke_source_index']
            rebuilt = named_frame(sigma, f['original_a'], f['original_b'], [0, 4], [0, 4],
                                  gi, gt['named_spoke_skeletons']['records'][gi])
            assert json.loads(json.dumps(rebuilt)) == f
            ge = geometry(f)
            audits = []
            for p in f['remaining_named_original_U_placements']:
                screen = singleton_schedules(sigma, [0, 4], p['actual_original_U_support'])
                schedules = p['complete_singleton_unary_relation_schedules']
                assert json.loads(json.dumps(screen['surviving_schedules'])) == schedules
                q_audits = []
                for si, s in enumerate(schedules):
                    qr, = [r for r in s['complete_singleton_unary_relations'] if r['literal_boundary'] == list(Q)]
                    d, = qr['complete_R_U'][0]
                    assert qr['complete_R_U'] == [[d]] and d in (1, 3)
                    ac, bc, uc = 4-d, d, d
                    assert ac != bc and ac != uc and {ac, bc} == U-{Q[0], Q[4]}
                    q_audits.append(dict(inherited_schedule_index=si, complete_R_U=[[d]],
                        designated_row_index=ROWS.index(Q), literal_boundary=Q,
                        original_a_b_u_colors=[ac, bc, uc],
                        full_joint_claim=[ac, bc, 'X', 'Y0', 'Y1', uc],
                        C_witness_guards=['X != a', 'Y0 != b', 'Y1 != b'],
                        trust='Paper C extension gives a complete tuple, not free marginal choices'))
                audits.append(dict(inherited_complete_original_U_placement=p,
                    full_source_support_compatible={1, 2, 3} <= set(p['actual_original_U_support']),
                    missing_actual_full_source_boundary_endpoints=sorted({1, 2, 3}-set(p['actual_original_U_support'])),
                    designated_row_complete_joint_paper_instances=q_audits))
            compatible = [r for r in audits if r['full_source_support_compatible']]
            assert len(compatible) == (2 if sigma == 933 else 3)
            assert sum(len(r['designated_row_complete_joint_paper_instances']) for r in compatible) == (3 if sigma == 933 else 5)
            assert not sigma >> ROWS.index(Q) & 1
            selected.append(dict(named_frame_id=f['named_frame_id'], inherited_complete_named_frame=f,
                same_embedding_C_U_geometry=ge, complete_actual_U_support_schedule_audits=audits,
                inherited_short_U_original_path_premise_audits=short_U_external_path_audits(f),
                fixed_original_ax_noncritical_paper_conclusion=True,
                exact_projection='pi_(a,b,u) J_G(beta) = pi_(a,b,u) J_(G-ax)(beta)',
                whole_C_witness_replacement_preserves_all_exterior_vertices=True,
                universal_six_role_joint_equality_claimed=False,
                status='selected_original_source_excluded'))
        swaps.append(swap_check(chosen[0], chosen[1]))
        remaining = [f for f in original if f not in chosen]
        counts = dict(remaining_named_frames=len(remaining),
            remaining_actual_U_support_records=sum(len(f['remaining_named_original_U_placements']) for f in remaining),
            remaining_complete_singleton_schedules=sum(len(p['complete_singleton_unary_relation_schedules'])
                for f in remaining for p in f['remaining_named_original_U_placements']))
        assert list(counts.values()) == ([16, 40, 50] if sigma == 933 else [20, 58, 84])
        targets.append(dict(source_sigma=sigma,
            inherited_named_frame_ids=[f['named_frame_id'] for f in original],
            newly_excluded_named_frame_ids=[f['named_frame_id'] for f in chosen],
            complete_remaining_named_original_frames=remaining, summary=counts))
    controls = joint_controls()
    inputs = [Path(__file__), SOURCE, GENERIC, *[ROOT/'scripts'/s for s in (
        'c5_excess_two_four_spoke_mixed12_04_04_joint_controls.py',
        'c5_excess_two_four_spoke_mixed12_01_01_joint_controls.py',
        'c5_excess_two_four_spoke_mixed12_01_12_joint_controls.py',
        'c5_excess_two_mixed_core_four_spoke_mixed12.py',
        'c5_excess_two_four_spoke_mixed12_unary_controls.py',
        'c5_excess_two_four_spoke_mixed12_joint_controls.py',
        'c5_excess_two_mixed_core_four_spoke_short_face.py',
        'c5_excess_two_mixed_core_spokes.py', 'c5_941_two_spoke.py',
        'c5_independent_support_capacity.py')]]
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        selected_complete_original_frames=selected, root_swap_checks=swaps, targets=targets,
        D5_no_fixed_mask_shortcut_diagnostics=D5_shortcut_diagnostics(),
        fixed_full_degree_same_graph_controls=controls,
        trust_boundary=dict(source_graphs_enumerated=False, old_A_A2_A3_artifacts_rewritten=False,
            D5_source_exclusion_transport_used=False,
            mixed11_sealed_triangle_conclusion_used=False,
            arbitrary_size_proof='Literal three hubs, degree lists, expanded connected-exterior K4 exclusion',
            source_realization_claimed=False, entire_mixed_12_subtype_excluded=False,
            epsilon_three_proved=False, new_lean_theorem=False),
        summary=dict(selected_04_04_frames_excluded_with_root_swap=len(selected),
            original_disk_rotations_retained_per_frame=4,
            inherited_selected_actual_U_support_records=[4, 12],
            inherited_selected_singleton_schedules=[6, 18],
            full_source_compatible_U_support_records_before_C_extension=[4, 6],
            full_source_compatible_U_singleton_schedules_before_C_extension=[6, 10],
            selected_source_residuals=[0, 0], fixed_original_noncritical_edge='a-x',
            designated_rejected_row=list(Q), both_singleton_colors_1_3_covered=True,
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
