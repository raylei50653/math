#!/usr/bin/env python3
"""Four-spoke (2,2): the remaining shared-vertex frames accept a rejected row.

Original short common arc 23 plus adjacent-support C color stability forces
acceptance of 01021 after one whole-graph D5 transport. Fixed relation schemas,
rotations and complete degree graphs are controls, not a source graph catalogue.
The arbitrary-size common-color avoidance uses the existing short-support paper
theorem, with shared contacts handled by direct degree-list slack.
"""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, U, span
from c5_941_two_spoke import relabel_mask
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_excess_two_mixed_core_four_spoke_short_face import disk_rotations, short_face
from c5_short_support_singleton import local_controls, three_hub_controls
from c5_excess_two_four_spoke_short_arc_joint_controls import fixed_graph_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_short_arc/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_crosscut/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
SHORT = ROOT / 'artifacts/c5_short_support_singleton/observations.json'
Q = (0, 1, 0, 2, 1)
C_SWAP, U_SWAP = (0, 3, 2, 1), (0, 1, 3, 2)


def edge(a, b):
    return tuple(sorted((a, b)))


def forbidden(relation):
    assert relation
    return set.intersection(*(set(t) for t in relation))


def relation_controls():
    """Full ordered two-contact relations in the same literal 01021 color frame."""
    todo, orbits = set(product(sorted(U), repeat=2)), []
    while todo:
        t = min(todo)
        orbit = {t, tuple(C_SWAP[c] for c in t)}
        assert orbit <= todo
        orbits.append(sorted(orbit))
        todo -= orbit
    assert len(orbits) == 10
    unary = [tuple(c for c in sorted(U) if bits >> c & 1) for bits in range(1, 16)]
    up = [colors for colors in unary if {U_SWAP[c] for c in colors} == set(colors)]
    assert len(up) == 7 and all(set(colors) - {2} for colors in up)
    u_records = [dict(palette_index=i, complete_original_U_contact_colors=colors,
        original_U_color_selected_to_avoid_A2=min(set(colors) - {2})) for i, colors in enumerate(up)]
    v_records = [dict(palette_index=i, complete_original_V_contact_colors=colors,
        original_V_selected_contact_color=min(colors),
        original_b_color_selected_from_1_3=min({1, 3} - {min(colors)})) for i, colors in enumerate(unary)]
    joins = [dict(join_index=i, U_palette_index=ui, V_palette_index=vi,
        original_a_color=2, original_b_color=v['original_b_color_selected_from_1_3'],
        original_U_contact_color=u['original_U_color_selected_to_avoid_A2'],
        original_V_contact_color=v['original_V_selected_contact_color'])
        for i, (ui, vi) in enumerate(product(range(len(u_records)), range(len(v_records))))
        for u, v in [(u_records[ui], v_records[vi])]]
    records, diagonal_ids, constructions = [], [], 0
    for bits in range(1, 1 << len(orbits)):
        relation = sorted(t for i, orbit in enumerate(orbits) if bits >> i & 1 for t in orbit)
        bans = forbidden(relation)
        if bans:
            continue
        assert {tuple(C_SWAP[c] for c in t) for t in relation} == set(relation)
        guarded = {d: [t for t in relation if t[0] != 2 and t[1] != d] for d in (1, 3)}
        assert all(guarded.values())
        # If R were contained in row A=2 union column D=1, stability would
        # also put it in row 2 union column 3. Their intersection is row 2,
        # contradicting F_C empty. This uses the full relation, not marginals.
        choices = {d: min(guarded[d]) for d in (1, 3)}
        witnesses = []
        for join in joins:
            d, uc, vc = (join[k] for k in ('original_b_color', 'original_U_contact_color',
                                          'original_V_contact_color'))
            x, y = choices[d]
            t = (2, d, x, y, uc, vc)
            assert (x, y) in relation and uc in up[join['U_palette_index']] and \
                vc in unary[join['V_palette_index']]
            assert t[0] != t[1] and t[0] != t[2] and t[1] != t[3] and \
                t[0] != t[4] and t[1] != t[5]
            assert t[0] not in {Q[0], Q[2]} and t[1] not in {Q[0], Q[3]}
            witnesses.append(t)
            constructions += 1
        ident = len(records)
        shared = all(x == y for x, y in relation)
        if shared:
            diagonal_ids.append(ident)
            assert all(t[2] == t[3] for t in witnesses)
        records.append(dict(schema_id=ident, stable_orbit_mask=bits,
            complete_literal_ordered_C_tuples=relation, original_common_forbidden_colors=[],
            all_common_root_color_avoidance_tuples=[dict(common_root_color=c,
                original_C_tuple=min(t for t in relation if c not in t)) for c in sorted(U)],
            complete_A2_D1_guarded_C_fiber=guarded[1], complete_A2_D3_guarded_C_fiber=guarded[3],
            compatible_with_shared_original_contact=shared,
            selected_literal_six_role_joint_witnesses_in_join_index_order=witnesses))
    assert len(records) == 963 and len(diagonal_ids) == 5 and constructions == 101115
    return dict(literal_boundary=Q, named_role_order=['a', 'b', 'x', 'y', 'u', 'v'],
        original_C_alternative_actual_boundary_support_envelopes=[[0], [2, 3]],
        original_U_actual_boundary_support_envelope=[0, 1, 2],
        C_pointwise_support_color_stabilizer=C_SWAP, U_pointwise_support_color_stabilizer=U_SWAP,
        full_ordered_C_tuple_orbits=orbits, nonempty_stable_C_relations_before_F_filter=1023,
        all_complete_C_relation_schemas=records, shared_original_contact_schema_ids=diagonal_ids,
        all_nonempty_stable_original_U_palettes=u_records, all_nonempty_original_V_palettes=v_records,
        same_literal_frame_join_order=joins,
        summary=dict(ordered_C_tuple_orbits=10, nonempty_stable_C_relations=1023,
            F_empty_C_relation_schemas=963, shared_contact_F_empty_C_relation_schemas=5,
            nonempty_stable_U_palettes=7, nonempty_V_palettes=15,
            guarded_A2_D1_D3_C_fibers=2 * 963,
            exact_same_frame_six_role_joint_witnesses=constructions),
        scope='Complete fixed-domain relation algebra under the paper hypotheses; abstract schemas are not graphs or source realizations')


def frame_analysis(frame, original, sigma):
    assert frame['original_root_order'] == original['root_order']
    assert frame['original_spoke_supports'] == original['original_spoke_supports']
    assert frame['original_root_and_boundary_edges'] == original['retained_source_edges']
    assert frame['inherited_skeleton_apex_rotation'] == original['apex_rotation']
    roots = frame['original_root_order']
    edges = set(map(tuple, frame['original_root_and_boundary_edges']))
    rotations = disk_rotations(edges)
    faces = rotations['all_original_C5_outer_face_rotations'][0]['original_disk_faces']
    common = [f for f in faces if all(r in f for r in roots)]
    assert len(common) == 2 and sorted(len(set(f) & B) for f in common) == [1, 2]
    choices = []
    for sign, shift, swapped in product((-1, 1), range(5), (False, True)):
        move = [(sign * h + shift) % 5 for h in range(5)]
        spoke_supports = [sorted(move[h] for h in s) for s in frame['original_spoke_supports']]
        if swapped:
            spoke_supports.reverse()
        if spoke_supports != [[0, 2], [0, 3]]:
            continue
        rows = [transport(row, move) for row in ROWS]
        original_index, = [i for i, tr in enumerate(rows) if tr['transported_row_index'] == ROWS.index(Q)]
        moved_sigma = relabel_mask(sigma, move)
        assert bool(moved_sigma >> ROWS.index(Q) & 1) == bool(sigma >> original_index & 1)
        if sigma >> original_index & 1:
            continue
        choices.append((move, swapped, rows, original_index, moved_sigma))
    assert choices, frame['inherited_named_skeleton_index']
    move, swapped, row_transports, oi, moved_sigma = min(choices, key=lambda c: (c[1], c[0]))
    a, b = roots[::-1] if swapped else roots
    rename = lambda z: move[z] if z in B else z
    moved_edges = {edge(rename(z), rename(w)) for z, w in edges}
    canonical_edges = FRAME | {edge(a, b)} | {edge(a, h) for h in (0, 2)} | {edge(b, h) for h in (0, 3)}
    assert moved_edges == canonical_edges
    canonical_faces = [[0, 1, 2, a], [0, a, b], [0, b, 3, 4], [a, 2, 3, b]]
    assert {frozenset(map(rename, f)) for f in faces} == {frozenset(f) for f in canonical_faces}
    owner_records = []
    for r in roots:
        incident = [f for f in faces if r in f]
        long = [f for f in incident if span(set(f) & B) >= 2]
        assert len(long) == 1 and long[0] not in common
        envelope = sorted(set(long[0]) & B)
        possible_supports = [tuple(h for i, h in enumerate(envelope) if bits >> i & 1)
                             for bits in range(8)]
        owner_records.append(dict(original_owner=r, all_incident_faces=incident,
            unique_original_long_face=long[0], exact_original_long_face_boundary_envelope=envelope,
            short_incident_face_lemma_instances=[short_face(f, r, roots, edges)
                for f in incident if f != long[0]],
            all_actual_long_face_support_subsets=[dict(actual_support=s,
                minimal_cyclic_support_span=span(set(s)),
                compatible_with_original_unary_contact_criticality=span(set(s)) >= 2)
                for s in possible_supports]))
    selected_row = ROWS[oi]
    selected_transport = row_transports[oi]
    cp = selected_transport['color_permutation']
    inverse = {c: i for i, c in enumerate(cp)}
    assert tuple(selected_transport['transported_row']) == Q
    guard_controls = []
    for d in (1, 3):
        original_colors = {a: inverse[2], b: inverse[d]}
        assert original_colors[a] != original_colors[b]
        assert all(original_colors[r] != selected_row[h] for r, s in
            zip(roots, frame['original_spoke_supports'], strict=True) for h in s)
        guard_controls.append(dict(canonical_a_b_colors=[2, d],
            original_root_colors_in_original_root_order=[original_colors[r] for r in roots],
            all_original_spoke_guards_and_ab_hold=True))
    original_u_support = sorted(h for h in B if move[h] in (0, 1, 2))
    original_c_support = sorted(h for h in B if move[h] in (0, 2, 3))
    original_c_swap = [inverse[C_SWAP[cp[c]]] for c in sorted(U)]
    original_u_swap = [inverse[U_SWAP[cp[c]]] for c in sorted(U)]
    assert all(original_c_swap[selected_row[h]] == selected_row[h] for h in original_c_support)
    assert all(original_u_swap[selected_row[h]] == selected_row[h] for h in original_u_support)
    for tr, row in zip(row_transports, ROWS, strict=True):
        assert all(tr['transported_row'][move[h]] == tr['color_permutation'][row[h]] for h in B)
    result = {k: v for k, v in frame.items() if k != 'status'}
    result.update(inherited_status=frame['status'], status='excluded_by_original_short_arc_row_acceptance',
        exhaustive_fixed_skeleton_rotations=rotations, original_unary_face_analysis=owner_records,
        original_C_possible_common_faces=[dict(original_face=f,
            exact_original_boundary_support_envelope=sorted(set(f) & B),
            canonical_exact_boundary_support_envelope=sorted(move[h] for h in set(f) & B),
            canonical_enclosing_adjacent_boundary_pair=[0, 1] if len(set(f) & B) == 1 else [2, 3],
            canonical_original_external_spoke_of_merged_root=[a, 2] if len(set(f) & B) == 1 else [a, 0])
            for f in common],
        one_global_boundary_permutation=move, whole_graph_root_role_swap=swapped,
        canonical_root_roles_in_original_vertices=[a, b], canonical_spokes=[[0, 2], [0, 3]],
        canonical_role_to_original_roles=['b', 'a', 'y', 'x', 'v', 'u'] if swapped else
            ['a', 'b', 'x', 'y', 'u', 'v'],
        transported_source_sigma=moved_sigma, transported_sigma_equals_original_sigma=moved_sigma == sigma,
        all_ten_simultaneous_whole_graph_row_color_transports=row_transports,
        original_rejected_row_index=oi, original_rejected_literal_row=selected_row,
        canonical_rejected_row_index=ROWS.index(Q), canonical_rejected_literal_row=Q,
        selected_one_global_color_permutation=cp,
        original_C_support_color_stabilizer=original_c_swap,
        original_U_support_color_stabilizer=original_u_swap,
        same_frame_original_root_guard_controls=guard_controls,
        original_C_common_color_avoidance_contract=dict(
            distinct_contacts='Contract original ab; C degrees and full ordered relation remain unchanged; the merged root has an original spoke outside the adjacent C support pair',
            shared_contact='Setting both original root guards to the same color leaves at least one list slack at the shared original contact',
            common_forbidden_colors=[], relation_is_original_C_not_a_marginal=True),
        original_joint_conclusion='One original rejected boundary row has a complete original G coloring',
        original_C_all_legal_root_pairs_extension_claimed=False,
        all_22_mixed_11_two_unary_sources_excluded=False,
        original_source_excluded=True)
    return result


def build():
    previous, source, short = (json.loads(p.read_text()) for p in (PREVIOUS, SOURCE, SHORT))
    assert json.loads(json.dumps(local_controls())) == short['local_controls']
    assert json.loads(json.dumps(three_hub_controls())) == short['three_hub_controls']
    targets, swap_controls = [], []
    for target in previous['targets']:
        sigma = target['source_sigma']
        original = next(t for t in source['targets'] if t['source_sigma'] == sigma)
        records = original['named_spoke_skeletons']['records']
        excluded, remaining = [], []
        for frame in target['remaining_unequal_pair_frames']:
            if len(set(frame['original_spoke_supports'][0]) & set(frame['original_spoke_supports'][1])) != 1:
                remaining.append(frame)
                continue
            excluded.append(frame_analysis(frame, records[frame['inherited_named_skeleton_index']], sigma))
        expected = [] if sigma == 933 else [155, 175, 179, 239, 243, 263]
        assert [f['inherited_named_skeleton_index'] for f in excluded] == expected
        assert len(remaining) == (14 if sigma == 933 else 18)
        for record in excluded:
            a, b = record['original_root_order']
            swap = lambda z: b if z == a else a if z == b else z
            es = {edge(swap(z), swap(w)) for z, w in record['original_root_and_boundary_edges']}
            partner, = [f for f in excluded if set(map(tuple, f['original_root_and_boundary_edges'])) == es]
            assert partner['original_spoke_supports'] == record['original_spoke_supports'][::-1]
            swap_controls.append(dict(source_sigma=sigma,
                original_named_skeleton_index=record['inherited_named_skeleton_index'],
                root_swapped_named_skeleton_index=partner['inherited_named_skeleton_index']))
        targets.append(dict(source_sigma=sigma,
            inherited_remaining_unequal_pair_frames=len(target['remaining_unequal_pair_frames']),
            newly_excluded_named_frame_indices=expected, original_short_arc_frame_analyses=excluded,
            remaining_unequal_pair_frames=remaining, remaining_one_common_vertex_frames=0,
            remaining_disjoint_pair_frames=len(remaining)))
    relations, controls = relation_controls(), fixed_graph_controls()
    inputs = [Path(__file__), PREVIOUS, SOURCE, SHORT,
        ROOT / 'scripts/c5_excess_two_mixed_core_four_spoke_short_face.py',
        ROOT / 'scripts/c5_short_support_singleton.py',
        ROOT / 'scripts/c5_excess_two_four_spoke_crosscut_joint_controls.py',
        ROOT / 'scripts/c5_excess_two_four_spoke_short_arc_joint_controls.py']
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        original_joint_contract=dict(component_order=['C', 'U-at-a', 'V-at-b'],
            port_order=['a', 'b', 'x', 'y', 'u', 'v'], shared_contact_is_one_original_vertex=True,
            guards=['a!=b', 'a!=x', 'b!=y', 'a!=u', 'b!=v'],
            selected_canonical_row=Q, selected_a_color=2, possible_selected_b_colors=[1, 3],
            same_original_C_U_V_complete_witnesses_joined=True,
            exact_original_component_attachments_and_supports_preserved=True,
            full_six_role_joint_equality_claimed=False, all_root_pairs_C_extension_claimed=False),
        inherited_short_support_mathematical_payload_audit=dict(local_controls_equal=True,
            three_hub_controls_equal=True, old_artifacts_rewritten=False),
        targets=targets, root_swap_named_frame_controls=swap_controls,
        fixed_full_ordered_relation_controls=relations,
        fixed_complete_degree_graph_controls=controls,
        summary=dict(source_sigmas=[933, 941], inherited_unequal_pair_frames=[14, 24],
            newly_excluded_short_arc_frames=[0, 6], remaining_unequal_pair_frames=[14, 18],
            remaining_one_common_vertex_frames=[0, 0], remaining_disjoint_pair_frames=[14, 18],
            selected_original_indices=[155, 175], selected_spokes_02_03_and_root_swap_excluded=True,
            all_one_common_boundary_vertex_frames_excluded=True,
            fixed_skeleton_rotation_assignments=96 * 6, valid_disk_skeleton_rotations=2 * 6,
            whole_graph_D5_frame_transports=6, simultaneous_whole_graph_row_color_transports=10 * 6,
            original_rejected_row_acceptance_controls=6,
            original_root_guard_controls=2 * 6, root_swap_frame_checks=len(swap_controls),
            fixed_relation_control_summary=relations['summary'],
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
