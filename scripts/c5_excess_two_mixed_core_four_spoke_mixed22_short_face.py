#!/usr/bin/env python3
"""B2: fixed W933-101 / W941-139 original mixed-(2,2) short face.

Finite controls preserve seven contact identities and complete literal fibres.
The arbitrary-size original K5 extraction is proved in the companion report;
these controls are not a source catalogue, disk realizations or Lean proofs.
"""
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS
from c5_excess_two_mixed_core_four_spoke_mixed22 import (
    attachment_constraints, contact_identities, root_pairs,
)
from c5_excess_two_four_spoke_mixed22_short_face_controls import controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json'


def leaf_ledger():
    identities, records = contact_identities(), []
    types = [('none', ()), ('a_only', (0,)), ('b_only', (1,)),
             ('shared_a_b', (0, 1))]
    hubs = {'none': [1, 2], 'a_only': [5, 1],
            'b_only': [6, 2], 'shared_a_b': [5, 6]}
    exterior = {'none': [5, 0, 4, 3, 6],
                'a_only': [6, 2, 3, 4, 0],
                'b_only': [5, 1, 0, 4, 3],
                'shared_a_b': [0, 1, 2, 3, 4]}
    skeleton = FRAME | {(5, 6), (0, 5), (1, 5), (2, 6), (3, 6)}
    for typ, owners in types:
        x, y = hubs[typ]
        path = exterior[typ]
        assert tuple(sorted((x, y))) in skeleton
        assert all(tuple(sorted(e)) in skeleton for e in zip(path, path[1:]))
        assert not {x, y} & set(path)
        assert all(any(tuple(sorted((h, v))) in skeleton for v in path) for h in (x, y))
        membership = [int(0 not in owners), int(1 not in owners)]
        eligible = []
        for ident in identities:
            partition = ident['original_vertex_partition']
            owner_count = sum(tuple(j for j in (0, 1)
                                    if any(partition[i] == v for i in (2*j, 2*j+1))) == owners
                              for v in set(partition))
            if not owners or owner_count >= 2:
                eligible.append(ident['identity'])
        records.append(dict(original_leaf_owner=typ, original_root_owners=list(owners),
            missing_color_membership_signature=membership,
            actual_private_external_neighbors=hubs[typ],
            actual_adjacent_hub_edge=sorted((x, y)),
            actual_complementary_exterior_path=path,
            possible_labelled_contact_identities=eligible,
            contact_leaf_is_triangle=bool(owners),
            minimum_leaf_odd_cycle_length=3,
            fifth_branch_set='C minus adjacent private u,w, union the actual exterior path',
            actual_C_remainder_to_exterior_reason={
                'none': 'all original root contacts remain in C remainder',
                'a_only': 'both original b contacts remain in C remainder',
                'b_only': 'both original a contacts remain in C remainder',
                'shared_a_b': 'another terminal odd cycle has nonowner private vertices with actual attachments 1,2',
            }[typ],
            universal_extraction_proved_in_report=True))
    assert len({tuple(r['missing_color_membership_signature']) for r in records}) == 4
    assert [r['possible_labelled_contact_identities'] for r in records] == [
        [r['identity'] for r in identities], ['D4'], ['D4'], ['Pstraight', 'Pcross']]
    return records


def original_K4_tethers():
    """Literal long-tether certificates for the structural K4-block lemma."""
    records = []
    for lengths in ((1, 1, 1, 1), (2, 3, 4, 5)):
        clique = [7, 8, 9, 10]
        es = FRAME | {(5, 6), (0, 5), (1, 5), (2, 6), (3, 6)}
        es |= {tuple(e) for e in combinations(clique, 2)}
        paths, fresh = [], 11
        for v, h, length in zip(clique, (5, 1, 2, 6), lengths, strict=True):
            path = [v, *range(fresh, fresh+length-1), h]
            fresh += length-1
            paths.append(path)
            es |= {tuple(sorted(e)) for e in zip(path, path[1:])}
        assert all(len(p) == len(set(p)) and
                   all(tuple(sorted(e)) in es for e in zip(p, p[1:])) for p in paths)
        interiors = [v for p in paths for v in p[1:-1]]
        assert len(interiors) == len(set(interiors))
        assert not set(interiors) & (B | {5, 6} | set(clique))
        assert all(sum(v in e for e in es) == 4 for v in clique)
        hub = sorted(B | {5, 6} | {v for p in paths for v in p[1:]})
        groups = [[v] for v in clique] + [hub]
        seen = {hub[0]}
        while True:
            nxt = seen | {w for v in seen for w in hub if tuple(sorted((v, w))) in es}
            if nxt == seen:
                break
            seen = nxt
        assert seen == set(hub)
        witnesses = []
        for i, j in combinations(range(5), 2):
            witness = next(tuple(sorted((v, w))) for v, w in product(groups[i], groups[j])
                           if tuple(sorted((v, w))) in es)
            witnesses.append(dict(branch_set_pair=[i, j], original_edge=witness))
        assert sum(map(len, groups)) == len(set(v for g in groups for v in g))
        records.append(dict(original_edges=sorted(es), original_K4=clique,
            actual_four_tether_paths=paths, five_original_branch_sets=groups,
            ten_original_edge_witnesses=witnesses,
            unused_degree_edges_not_completed=True,
            fixed_pinned_root_pair_edge_minimality_used=False,
            scope='Conditional original-path certificate, not a complete-degree or source graph'))
    return records


def build():
    source = json.loads(SOURCE.read_text())
    frames = []
    for sigma, index in ((933, 101), (941, 139)):
        target = next(t for t in source['targets'] if t['source_sigma'] == sigma)
        frame = next(f for f in target['original_named_frames']
                     if f['inherited_named_skeleton_index'] == index)
        assert frame['original_spoke_supports'] == [[0, 1], [2, 3]]
        face = next(f for f in frame['retained_original_C_face_necessities']
                    if f['exact_actual_support_envelope'] == [1, 2])
        expected = attachment_constraints(sigma, (0, 1), (2, 3), face['original_face'])
        assert json.loads(json.dumps(expected)) == face
        assert face['necessary_minimum_C_degree_by_original_role'] == {
            'none': 2, 'a_only': 2, 'b_only': 2, 'shared_a_b': 2}
        tables = {t['original_vertex_role']: t for t in face['per_original_vertex_attachment_necessities']}
        assert {k: v['permissible_actual_boundary_attachment_subsets'] for k, v in tables.items()} == {
            'none': [[], [1], [2], [1, 2]], 'a_only': [[], [1]],
            'b_only': [[], [2]], 'shared_a_b': [[]]}
        q = tuple(ROWS[1])
        assert q == (0, 1, 0, 2, 1) and not sigma >> 1 & 1
        assert root_pairs(q, (0, 1), (2, 3)) == [(2, 1), (2, 3), (3, 1)]
        frames.append(dict(named_source=f'W{sigma}-{index}', source_sigma=sigma,
            inherited_original_named_frame=frame,
            selected_original_short_face=face,
            all_seven_original_contact_identities=[r['identity'] for r in contact_identities()],
            short_face_status='excluded_by_arbitrary_size_original_K5_lemma',
            other_original_faces_status='retained_without_new_claim',
            named_short_face_residuals=[]))
    fixed = controls()
    files = [Path(__file__), ROOT / 'scripts/c5_excess_two_four_spoke_mixed22_short_face_controls.py',
             ROOT / 'scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py',
             ROOT / 'scripts/c5_excess_two_four_spoke_mixed22_joint_controls.py', SOURCE]
    return dict(schema=1, scope=__doc__, input_sha256={str(p.relative_to(ROOT)):
        sha256(p.read_bytes()).hexdigest() for p in files}, pattern_order=ROWS,
        source_omission_and_q_core_conclusions=source['original_omission_q_core_identity'],
        original_relation_contract=source['original_relation_contract'],
        contact_identity_table=contact_identities(), selected_original_frames=frames,
        complete_leaf_owner_and_original_path_ledger=leaf_ledger(),
        conditional_K4_actual_tether_controls=original_K4_tethers(),
        fixed_complete_degree_and_original_K5_controls=fixed,
        external_theorem=dict(author='Zdenek Dvorak', title='List coloring and Gallai trees',
            url='https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf',
            dependencies=['Lemma 7', 'Corollary 8', 'Theorem 10'],
            fixed_pinned_root_pair_edge_minimality_required=False),
        summary=dict(named_source_short_faces=2, labelled_contact_identities=7,
            arbitrary_size_short_face_source_exclusion=True,
            leaf_owner_cases=4, conditional_K4_tether_certificates=2,
            named_short_face_residuals=0, other_original_faces_retained=True,
            full_mixed22_branch_excluded=False, epsilon_three_proved=False,
            source_graph_catalogue_enumerated=False, source_realizability_claimed=False,
            new_lean_theorem=False, fixed_control_summary=fixed['summary']))


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
