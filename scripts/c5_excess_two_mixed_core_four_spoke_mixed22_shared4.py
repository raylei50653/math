#!/usr/bin/env python3
"""B4: W933-129, original 04/12 long face, shared attachment {4}.

The designated shared contact is a genuine C-leaf, with tight singleton lists
on all rejected-row root pairs.  Original cut parity forces a further actual
boundary attachment of C minus that leaf.  Five original connected bags give
K5, closing only this conditional attachment branch, not the entire frame.
"""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS
from c5_excess_two_mixed_core_four_spoke_mixed22 import (
    attachment_constraints, contact_identities, root_pairs, rotation_faces,
)
from c5_excess_two_four_spoke_mixed22_shared4_controls import controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_shared4/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json'
LONG = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face/observations.json'
U = set(range(4))
SA, SB = (0, 4), (1, 2)


def canonical_cycle(vertices):
    vertices = tuple(vertices)
    return min(vertices[i:] + vertices[:i] for i in range(len(vertices)))


def augmented_rotations(frame):
    """Insert the actual av,bv,4v star, preserving each original rotation."""
    result, checked = [], 0
    v = 7
    skeleton = set(map(tuple, frame['original_root_and_boundary_edges']))
    actual = skeleton | {(4, v), (5, v), (6, v)}
    for saved in frame['fixed_original_skeleton_rotation_audit']['disk_rotations']:
        inherited = {r['vertex']: r['ring'] for r in saved['rotation']}
        found = []
        for insertions, v_ring in product(product(range(3), repeat=3), ((4, 5, 6), (4, 6, 5))):
            rotation = {w: list(ns) for w, ns in inherited.items()}
            for w, after in zip((4, 5, 6), insertions, strict=True):
                rotation[w].insert(after + 1, v)
            rotation[v] = list(v_ring)
            checked += 1
            faces = rotation_faces(rotation)
            if len(rotation) - len(actual) + len(faces) != 2:
                continue
            outer = canonical_cycle(saved['original_outer_boundary'])
            if not any(canonical_cycle(f) == outer for f in faces):
                continue
            inner = [f for f in faces if canonical_cycle(f) != outer]
            if not any(set(f) == {2, 3, 4, 6, v} for f in inner):
                continue  # v must lie in the selected original long face.
            assert any(set(f) == {5, 6, v} for f in inner)
            assert any(set(f) == {4, 5, v} for f in inner)
            common = [f for f in inner if {5, 6, v} <= set(f)]
            assert len(common) == 1 and set(common[0]) == {5, 6, v}
            found.append(dict(rotation=[dict(vertex=w, ring=ns) for w, ns in sorted(rotation.items())],
                all_original_augmented_faces=faces,
                sole_face_incident_to_a_b_and_designated_shared_leaf=common[0],
                original_outer_boundary=saved['original_outer_boundary']))
        assert len(found) == 1
        result.append(dict(inherited_original_rotation=saved, original_augmented_edges=sorted(actual),
            designated_shared_leaf=v, selected_long_face_extensions=found))
    assert len(result) == 2 and checked == 108
    return dict(rotation_insertions_checked=checked, original_long_face_extensions=result,
        geometry_crosscheck='C-v is connected, meets a,b,v, and must be sealed in original abv triangle',
        boundary_attachment_count_forced_by_geometry=0,
        geometry_is_not_needed_for_original_K5_parity_proof=True)


def exact_lists(face):
    leaf_rows, neighbor_cases = [], []
    rows = face['rejected_rows_with_complete_original_root_pairs']
    for row in rows:
        q, ri = row['row'], row['row_index']
        entries = []
        for pair in root_pairs(q, SA, SB):
            c, = U - {q[4], *pair}
            entries.append(dict(original_root_pair=pair, actual_leaf_external_colors=[*pair, q[4]],
                exact_leaf_list=[c], original_C_degree=1, original_complete_degree=4,
                exact_degree_slack=0))
        leaf_rows.append(dict(row_index=ri, literal_boundary=q, all_legal_root_pairs=entries))
    counts = dict(candidates=0, pair_checks=0, excluded=0, retained=0)
    for table in face['per_original_vertex_attachment_necessities']:
        owners = table['fixed_root_owners']
        for hs in table['permissible_actual_boundary_attachment_subsets']:
            counts['candidates'] += 1
            records = []
            degree = 4 - len(owners) - len(hs)
            for row in rows:
                q, ri = row['row'], row['row_index']
                for pair in root_pairs(q, SA, SB):
                    c, = U - {q[4], *pair}
                    ls = U - {q[h] for h in hs} - {pair[j] for j in owners}
                    assert len(ls) == degree
                    after = ls - {c}
                    slack = len(after) - (degree - 1)
                    assert slack in (0, 1)
                    counts['pair_checks'] += 1
                    records.append(dict(row_index=ri, literal_boundary=q,
                        original_root_pair=pair, designated_leaf_forced_color=c,
                        original_neighbor_exact_list=sorted(ls),
                        C_minus_leaf_neighbor_degree=degree-1,
                        exact_neighbor_list_after_fixing_original_leaf=sorted(after),
                        connected_remainder_slack=slack))
            failure = next((r for r in records if r['connected_remainder_slack']), None)
            if failure:
                counts['excluded'] += 1
            else:
                counts['retained'] += 1
            neighbor_cases.append(dict(original_neighbor_owner=table['original_vertex_role'],
                actual_neighbor_boundary_attachments=hs, original_neighbor_C_degree=degree,
                all_rejected_row_pair_exact_lists=records,
                actual_cross_row_slack_witness=failure,
                survives_leaf_deletion_slack_necessity=failure is None,
                retained_candidate_is_not_a_source_realization=True))
    assert sum(len(r['all_legal_root_pairs']) for r in leaf_rows) == 11
    assert counts == dict(candidates=13, pair_checks=143, excluded=5, retained=8)
    return dict(designated_leaf_actual_attachments=[4],
        designated_leaf_original_C_edge_is_bridge=True,
        all_original_rejected_rows_and_literal_pairs=leaf_rows,
        original_leaf_is_tight_on_every_pair=True,
        B3_shared_leaf_slack_exclusion_does_not_apply=True,
        all_possible_actual_bridge_neighbor_candidates=neighbor_cases,
        summary=counts,
        retained_slack_candidates_closed_by_separate_original_cut_parity_K5_lemma=True)


def build():
    source, long = json.loads(SOURCE.read_text()), json.loads(LONG.read_text())
    target = next(t for t in source['targets'] if t['source_sigma'] == 933)
    frame = next(f for f in target['original_named_frames']
                 if f['original_spoke_supports'] == [list(SA), list(SB)])
    assert frame['inherited_named_skeleton_index'] == 129
    face = next(f for f in frame['retained_original_C_face_necessities']
                if f['exact_actual_support_envelope'] == [2, 3, 4])
    assert face['original_face'] == [2, 6, 5, 4, 3]
    assert json.loads(json.dumps(attachment_constraints(933, SA, SB, face['original_face']))) == face
    assert [r['row_index'] for r in face['rejected_rows_with_complete_original_root_pairs']] == [1, 3, 4, 6]
    identities = []
    for ident in contact_identities():
        p = ident['original_vertex_partition']
        designated = [dict(original_vertex_class=k,
            roles=[ident['original_ordered_roles'][i] for i, value in enumerate(p) if value == k])
            for k in sorted(set(p)) if any(p[i] == k for i in (0, 1)) and any(p[i] == k for i in (2, 3))]
        identities.append(dict(inherited_original_identity=ident,
            possible_designated_shared_vertices=designated,
            designated_shared_attachment4_status='excluded_by_original_cut_parity_K5' if designated else
                'not_applicable_no_shared_contact',
            other_actual_attachment_branches='retained_without_new_claim'))
    assert sum(len(r['possible_designated_shared_vertices']) for r in identities) == 8
    fixed = controls()
    files = [Path(__file__), ROOT / 'scripts/c5_excess_two_four_spoke_mixed22_shared4_controls.py',
             ROOT / 'scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py',
             ROOT / 'scripts/c5_excess_two_four_spoke_mixed22_joint_controls.py', SOURCE, LONG]
    return dict(schema=1, scope=__doc__, input_sha256={str(p.relative_to(ROOT)):
        sha256(p.read_bytes()).hexdigest() for p in files}, pattern_order=ROWS,
        named_original_frame='W933-129', inherited_original_named_frame=frame,
        selected_original_long_face=face, source_omission_and_q_core_conclusions=source['original_omission_q_core_identity'],
        original_relation_contract=source['original_relation_contract'],
        inherited_B3_scope=long['summary'],
        all_seven_original_identities_and_designated_shared_branches=identities,
        original_leaf_and_bridge_cross_row_lists=exact_lists(face),
        actual_star_rotation_and_face_crosscheck=augmented_rotations(frame),
        arbitrary_size_original_cut_parity_lemma=dict(
            original_remainder='K = complete original C minus the designated shared leaf v',
            original_remainder_is_nonempty_and_connected=True,
            three_fixed_original_cut_edges=['a-x_other', 'b-y_other', 'v-t'],
            literal_degree_identity='4*|K| = 2*|E(K)| + 3 + |E(K,B)|',
            actual_K_to_boundary_edge_count_is_odd_and_positive=True,
            shared_remaining_contact_still_gives_two_distinct_root_edges=True,
            five_original_connected_bags=['{a}', '{b}', '{v}', 'original B', 'complete original K'],
            all_ten_original_adjacencies=['ab', 'av', 'bv', 'a original spoke', 'b original spoke', 'v4',
                'a-x_other', 'b-y_other', 'v-t', 'one actual K-to-B attachment forced by parity'],
            no_Gallai_terminal_block_classification_required=True,
            no_minor_preservation_of_relation_fibres_or_Sigma_claimed=True),
        fixed_complete_degree_relations_and_original_K5_controls=fixed,
        summary=dict(selected_original_frames=1, named_original_frame='W933-129', source_sigma=933,
            original_spoke_supports=[list(SA), list(SB)], selected_original_face_envelope=[2,3,4],
            labelled_shared_contact_identities=6, designated_original_shared_choices=8,
            original_leaf_rejected_row_pair_tightness_checks=11,
            bridge_neighbor_actual_attachment_candidates=13, bridge_neighbor_row_pair_checks=143,
            bridge_neighbor_slack_exclusions=5, bridge_neighbor_slack_survivors=8,
            arbitrary_size_designated_shared_attachment4_source_exclusion=True,
            designated_shared_attachment4_residuals=0,
            entire_W933_129_frame_excluded=False, other_identities_attachments_and_frames_retained=True,
            original_B_and_B3_artifacts_rewritten=False, full_mixed22_branch_excluded=False,
            epsilon_three_proved=False, source_graph_catalogue_enumerated=False,
            source_realizability_claimed=False, new_lean_theorem=False,
            fixed_control_summary=fixed['summary']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, sort_keys=True, indent=1)+'\n').encode()
    if args.check:
        assert OUT.read_bytes() == payload, f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
