#!/usr/bin/env python3
"""B3: original long face {0,4,3} of W933-101 / W941-139.

Five original leaf types give conditional K5 extraction controls.  The
arbitrary-size source exclusion is proved in the companion report.  These
literal relation controls are not source realizations or a source catalogue.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS
from c5_excess_two_mixed_core_four_spoke_mixed22 import (
    attachment_constraints, contact_identities, root_pairs,
)
from c5_excess_two_mixed_core_four_spoke_mixed22_short_face import original_K4_tethers
from c5_excess_two_four_spoke_mixed22_long_face_controls import controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json'
SHORT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face/observations.json'


def leaf_ledger():
    skeleton = FRAME | {(5, 6), (0, 5), (1, 5), (2, 6), (3, 6)}
    cases = [
        ('none_04', (), [0, 4], [5, 1, 2, 6, 3], 'all original root contacts remain'),
        ('none_34', (), [3, 4], [6, 2, 1, 5, 0], 'all original root contacts remain'),
        ('a_only_0', (0,), [5, 0], [1, 2, 6, 3, 4], 'both original b contacts remain'),
        ('b_only_3', (1,), [6, 3], [2, 1, 5, 0, 4], 'both original a contacts remain'),
        ('shared_a_b', (0, 1), [5, 6], [0, 1, 2, 3, 4],
         'another terminal nonowner odd cycle has actual attachments 04 or 34'),
    ]
    records = []
    for name, owners, hubs, path, reason in cases:
        assert tuple(sorted(hubs)) in skeleton
        assert set(path) == (B | {5, 6}) - set(hubs)
        assert all(tuple(sorted(e)) in skeleton for e in zip(path, path[1:]))
        neighbors = [next(tuple(sorted((h, v))) for v in path
                          if tuple(sorted((h, v))) in skeleton) for h in hubs]
        eligible = []
        for ident in contact_identities():
            p = ident['original_vertex_partition']
            count = sum(tuple(j for j in (0, 1) if any(p[i] == v for i in (2*j, 2*j+1)))
                        == owners for v in sorted(set(p)))
            if not owners or count >= 2:
                eligible.append(ident['identity'])
        records.append(dict(original_leaf_type=name, original_root_owners=list(owners),
            actual_private_external_neighbors=hubs,
            actual_adjacent_hub_edge=sorted(hubs),
            actual_complementary_exterior_path=path,
            actual_hub_to_exterior_edge_witnesses=neighbors,
            possible_labelled_contact_identities=eligible,
            contact_leaf_is_triangle=bool(owners),
            original_C_remainder_to_exterior_reason=reason,
            five_original_branch_sets=['{h}', '{k}', '{u}', '{w}',
                'original C minus adjacent private u,w, union original X minus h,k'],
            arbitrary_size_extraction_proved_in_report=True))
    assert [r['possible_labelled_contact_identities'] for r in records] == [
        [r['identity'] for r in contact_identities()],
        [r['identity'] for r in contact_identities()],
        ['D4'], ['D4'], ['Pstraight', 'Pcross']]
    return records


def shared_bridge_obstructions():
    records = []
    for h in (0, 3, 4):
        for ri, q in enumerate(ROWS):
            if any(sigma >> ri & 1 for sigma in (933, 941)):
                continue
            pair = next((p for p in root_pairs(q, (0, 1), (2, 3))
                         if q[h] in p), None)
            if pair is None:
                continue
            forbidden = [*pair, q[h]]
            palette = sorted(set(range(4)) - set(forbidden))
            assert len(palette) > 1
            records.append(dict(hypothetical_original_shared_contact_boundary_attachment=h,
                hypothetical_original_C_degree=1, original_complete_degree=4,
                common_rejected_row_index=ri, literal_boundary=q,
                legal_original_G_minus_C_root_pair=pair,
                actual_external_neighbor_colors=forbidden,
                exact_list=palette, connected_slack=len(palette)-1,
                consequence='connected C is list-colorable; contradicts original rejected row'))
            break
    assert len(records) == 3
    return dict(shared_contact_leaf_bridge_is_possible=False,
        degree_two_shared_contacts_on_internal_bridge_chains_retained=True,
        all_possible_long_face_boundary_neighbors=[0, 3, 4],
        exact_same_frame_slack_witnesses=records,
        original_shared_contact_actual_attachments=[], original_shared_contact_C_degree=2,
        different_original_04_12_frame_not_identified=True)


def build():
    source, short = json.loads(SOURCE.read_text()), json.loads(SHORT.read_text())
    frames = []
    for sigma, index in ((933, 101), (941, 139)):
        target = next(t for t in source['targets'] if t['source_sigma'] == sigma)
        frame = next(f for f in target['original_named_frames']
                     if f['inherited_named_skeleton_index'] == index)
        assert frame['original_spoke_supports'] == [[0, 1], [2, 3]]
        face = next(f for f in frame['retained_original_C_face_necessities']
                    if f['exact_actual_support_envelope'] == [0, 3, 4])
        expected = attachment_constraints(sigma, (0, 1), (2, 3), face['original_face'])
        assert json.loads(json.dumps(expected)) == face
        assert face['necessary_minimum_C_degree_by_original_role'] == {
            'none': 2, 'a_only': 2, 'b_only': 2, 'shared_a_b': 2}
        tables = {t['original_vertex_role']: t for t in face['per_original_vertex_attachment_necessities']}
        assert {k: v['permissible_actual_boundary_attachment_subsets'] for k, v in tables.items()} == {
            'none': [[], [0], [3], [4], [0, 4], [3, 4]],
            'a_only': [[], [0]], 'b_only': [[], [3]], 'shared_a_b': [[]]}
        previous = next(f for f in short['selected_original_frames'] if f['source_sigma'] == sigma)
        assert previous['inherited_original_named_frame'] == frame
        assert previous['named_short_face_residuals'] == []
        assert {tuple(f['exact_actual_support_envelope']) for f in
                frame['retained_original_C_face_necessities']} == {(1, 2), (0, 3, 4)}
        identities = [dict(identity=r['identity'],
            long_face_status='excluded_by_B3_arbitrary_size_original_K5_lemma')
            for r in contact_identities()]
        frames.append(dict(named_source=f'W{sigma}-{index}', source_sigma=sigma,
            inherited_original_named_frame=frame, selected_original_long_face=face,
            all_seven_original_contact_identity_results=identities,
            named_long_face_residuals=[],
            both_original_C_faces_excluded_by_separate_lemmas=dict(
                short_face='B2: envelope 1,2', long_face='B3: envelope 0,4,3'),
            original_B_frame_not_rewritten=True, other_original_named_frames_status='retained_without_new_claim'))
    fixed = controls()
    files = [Path(__file__),
        ROOT / 'scripts/c5_excess_two_four_spoke_mixed22_long_face_controls.py',
        ROOT / 'scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py',
        ROOT / 'scripts/c5_excess_two_four_spoke_mixed22_joint_controls.py',
        ROOT / 'scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py',
        SOURCE, SHORT]
    return dict(schema=1, scope=__doc__, input_sha256={str(p.relative_to(ROOT)):
        sha256(p.read_bytes()).hexdigest() for p in files}, pattern_order=ROWS,
        source_omission_and_q_core_conclusions=source['original_omission_q_core_identity'],
        original_relation_contract=source['original_relation_contract'],
        contact_identity_table=contact_identities(), selected_original_frames=frames,
        shared_contact_original_leaf_bridge_audit=shared_bridge_obstructions(),
        complete_leaf_type_and_original_exterior_path_ledger=leaf_ledger(),
        conditional_K4_actual_tether_controls=original_K4_tethers(),
        fixed_complete_degree_and_original_K5_controls=fixed,
        external_theorem=dict(author='Zdenek Dvorak', title='List coloring and Gallai trees',
            url='https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf',
            dependencies=['Lemma 7', 'Corollary 8', 'Theorem 10'],
            fixed_pinned_root_pair_edge_minimality_required=False),
        summary=dict(named_source_long_faces=2, labelled_contact_identities=7,
            arbitrary_size_long_face_source_exclusion=True, original_leaf_types=5,
            shared_contact_leaf_bridge_excluded=True, shared_bridge_slack_witnesses=3,
            named_long_face_residuals=0,
            selected_two_frames_both_faces_excluded_by_distinct_lemmas=True,
            other_original_frames_retained=True, original_B_and_B2_artifacts_rewritten=False,
            conditional_K4_tether_certificates=2, full_mixed22_branch_excluded=False,
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
