#!/usr/bin/env python3
"""Four-spoke (2,2), original mixed-(1,2) plus one unary at a.

Fresh named incidence identities and fixed actual-support singleton relations,
not the completed mixed-(1,1) table. Arbitrary-size source exclusions use the
paper minimal-core/ternary argument, disk crosscuts and unary fixed-color
conservation. Full C ternary tuples and same-graph six-role witnesses are kept.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, U, span
from c5_excess_one_subcovers import singleton
from c5_941_two_spoke import relabel_mask
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_excess_two_mixed_core_four_spoke_short_face import rotation_faces, short_face
from c5_excess_two_mixed_core_four_spoke_long_face import short_support_instance
from c5_excess_two_mixed_core_four_spoke_crosscut import crosscut_controls, tightness_rows
from c5_two_spoke_three_contacts import run as ternary_replay
from c5_single_spoke_root_conservation import local_audit
from c5_excess_two_four_spoke_mixed12_unary_controls import singleton_schedules, canonical_conflicts
from c5_excess_two_four_spoke_mixed12_joint_controls import build as joint_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed12/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
TERNARY = ROOT / 'artifacts/c5_two_spoke_three_contacts/observations.json'
CONSERVATION = ROOT / 'artifacts/c5_single_spoke_root_conservation/observations.json'


def edge(v, w):
    return tuple(sorted((v, w)))


def subsets(values):
    return [list(s) for n in range(len(values)+1) for s in combinations(sorted(values), n)]


def cycle_key(face):
    return min(tuple(f[i:]+f[:i]) for f in (face, face[::-1]) for i in range(len(f)))


def disk_rotations(edges):
    vertices = sorted({v for e in edges for v in e})
    options = []
    for v in vertices:
        ns = sorted(w if z == v else z for z, w in edges if v in (z, w))
        options.append([(ns[0], *p) for p in permutations(ns[1:])])
    checked, records = 0, []
    for rings in product(*options):
        checked += 1
        rotation = dict(zip(vertices, rings, strict=True))
        faces = rotation_faces(rotation)
        outer = [f for f in faces if len(f) == 5 and set(f) == B]
        if len(vertices)-len(edges)+len(faces) != 2 or len(outer) != 1:
            continue
        records.append(dict(rotation=[dict(vertex=v, ring=rotation[v]) for v in vertices],
            original_outer_face=outer[0], original_disk_faces=sorted(
                [list(cycle_key(f)) for f in faces if f != outer[0]])))
    assert records
    return dict(rotation_assignments_checked=checked, all_disk_rotations=records,
        scope='All rotations of the fixed original seven-vertex spoke skeleton only')


def omission_identity(sa, sb, omitted_kind, omitted_point=None):
    factors = [dict(id=f'a:spoke:{i}', incidence=[1, 0]) for i in sa
               if omitted_kind != 'a_spoke' or i != omitted_point]
    factors += [dict(id=f'b:spoke:{i}', incidence=[0, 1]) for i in sb
                if omitted_kind != 'b_spoke' or i != omitted_point]
    factors += [dict(id='original:C', incidence=[1, 2])]
    if omitted_kind != 'whole_U':
        factors += [dict(id='original:U', incidence=[1, 0])]
    degrees = [4, 5] if omitted_kind != 'b_spoke' else [5, 4]
    identities = []
    for omitted in subsets(list(range(len(factors)))):
        ds = [degrees[j]-sum(factors[i]['incidence'][j] for i in omitted) for j in (0, 1)]
        if min(ds) >= 4:
            identities.append(dict(omitted_original_factors=[factors[i]['id'] for i in omitted],
                resulting_a_b_degrees=ds,
                status='original_omission_graph_itself' if not omitted else 'excluded_original_4_4_q_core'))
    assert len(identities) == (4 if omitted_kind == 'b_spoke' else 3)
    return dict(original_omission=omitted_kind, omitted_original_spoke_point=omitted_point,
        original_a_b_degrees=degrees, retained_original_factors=factors,
        all_degree_admissible_further_omissions=identities,
        original_C_cannot_be_omitted=True,
        minimal_if_it_rejects=True,
        core_after_unique_root_deletion=(
            dict(component='original C + original a + original U', contacts=['a', 'y0', 'y1'],
                 contact_partition=[3], degree_of_a_inside_component=2)
            if omitted_kind == 'a_spoke' else
            dict(component='original C + original a', contacts=['a', 'y0', 'y1'],
                 contact_partition=[3], degree_of_a_inside_component=1)
            if omitted_kind == 'whole_U' else
            dict(components=['original C + original b', 'original U'],
                 contacts=[['x', 'b'], ['u']], contact_partition=[2, 1],
                 degree_of_b_inside_binary_component=2)),
        conclusion='all_rows_accepted_by_original_two_spoke_ternary_theorem'
            if omitted_kind != 'b_spoke' else 'only_necessary_minimal_two_spoke_2_1_identity')


def singleton_join_controls():
    """Nonempty FULL witness domains; projection is taken after the exact join."""
    records = []
    for na, ru in product(subsets(range(4))[1:], repeat=2):
        joined = [(a, u) for a, u in product(na, ru) if a != u]
        empty = not joined
        assert empty == (len(na) == len(ru) == 1 and na == ru)
        records.append(dict(nonempty_original_N_a_domain=na,
            nonempty_complete_original_U_relation=ru,
            all_guarded_a_u_pairs=joined, source_rejects=empty,
            both_domains_same_singleton=empty))
    assert len(records) == 225
    return records


def short_unary_instance(support, a, b, edges):
    pair = min(e for e in FRAME if set(support) <= set(e))
    outside_spokes = [v for v in sorted(B-set(pair)) if edge(a, v) in edges or edge(b, v) in edges]
    if outside_spokes:
        return short_support_instance(support, a, [a, b], edges)
    # Equal original spoke pairs have no skeleton-only outside path. The
    # full-source support lemma supplies an actual C attachment instead;
    # record its existence rather than inventing a skeleton edge.
    assert all(v in pair for v in B if edge(a, v) in edges or edge(b, v) in edges)
    h = min(B-set(pair))
    return dict(actual_support=support, original_unary_owner=a, enclosing_original_boundary_edge=pair,
        original_external_path_roles=[a, 'original_C_x', 'path_inside_original_C', f'actual_C_attachment_at_{h}', h],
        original_path_existence='Full effective interior touches all five boundary vertices; roots and short U do not touch h, so original C does',
        original_path_avoids_U=True, skeleton_only_original_path_claimed=False)


def named_frame(sigma, a, b, sa, sb, source_index, source):
    edges = FRAME | {edge(a, b)} | {edge(a, i) for i in sa} | {edge(b, i) for i in sb}
    assert sorted(map(tuple, source['retained_source_edges'])) == sorted(edges)
    rotations = disk_rotations(edges)
    faces = sorted({tuple(f) for r in rotations['all_disk_rotations'] for f in r['original_disk_faces']})
    placements = []
    for face in faces:
        if a not in face:
            continue
        envelope = sorted(set(face) & B)
        supports = []
        for support in subsets(envelope):
            short = span(set(support)) <= 1
            item = dict(actual_original_U_support=support, minimal_cyclic_span=span(set(support)))
            if short:
                item.update(status='excluded_original_au_noncritical_short_support',
                    original_external_path_lemma_instance=short_unary_instance(support, a, b, edges))
            else:
                schedules = singleton_schedules(sigma, sa, support)
                item.update(complete_singleton_unary_relation_screen=schedules,
                    status='necessary_original_U_relation_only' if schedules['surviving_schedules']
                        else 'excluded_by_same_original_U_relation')
            supports.append(item)
        rotation_indices = [i for i, r in enumerate(rotations['all_disk_rotations']) if list(face) in r['original_disk_faces']]
        assert rotation_indices
        compatible_C_faces = sorted({tuple(f) for i in rotation_indices
            for f in rotations['all_disk_rotations'][i]['original_disk_faces'] if a in f and b in f})
        placements.append(dict(original_U_face=list(face), exact_face_boundary_envelope=envelope,
            supporting_original_rotation_indices=rotation_indices,
            compatible_original_C_common_faces=[dict(face=list(f), supporting_rotation_indices=[i for i in rotation_indices
                if list(f) in rotations['all_disk_rotations'][i]['original_disk_faces']]) for f in compatible_C_faces],
            all_actual_original_U_support_subsets=supports))
    residual = [dict(original_U_face=p['original_U_face'], actual_original_U_support=s['actual_original_U_support'],
        complete_singleton_unary_relation_schedules=s['complete_singleton_unary_relation_screen']['surviving_schedules'],
        supporting_original_rotation_indices=p['supporting_original_rotation_indices'],
        compatible_original_C_common_faces=p['compatible_original_C_common_faces'])
        for p in placements for s in p['all_actual_original_U_support_subsets']
        if s['status'] == 'necessary_original_U_relation_only']
    return dict(named_frame_id=f'{sigma}:a{a}:b{b}:Sa{"".join(map(str,sa))}:Sb{"".join(map(str,sb))}',
        source_sigma=sigma, original_a=a, original_b=b, original_a_spokes=sa, original_b_spokes=sb,
        original_root_and_boundary_edges=sorted(edges), generic_single_spoke_source_index=source_index,
        original_incidence_contract=dict(C_incidence=[1, 2], C_contacts=['x', 'y0', 'y1'],
            C_owners=[a, b, b], U_owner=a, U_contact='u', y0_y1_distinct=True,
            allowed_original_contact_identities=['x_distinct_from_y0_y1', 'x_is_y0', 'x_is_y1'],
            preserve_all_original_attachments_bridges_and_rotation=True),
        exhaustive_original_skeleton_rotations=rotations,
        all_original_U_face_support_placements=placements,
        original_omission_identities=[omission_identity(sa, sb, 'a_spoke', i) for i in sa]
            + [omission_identity(sa, sb, 'b_spoke', i) for i in sb]
            + [omission_identity(sa, sb, 'whole_U')],
        remaining_named_original_U_placements=residual,
        remaining_original_C_common_faces=[list(f) for f in faces if a in f and b in f],
        residual_C_relation='Complete original R_C(x,y0,y1), not independent contact marginals',
        residual_joint_order=['a', 'b', 'x', 'y0', 'y1', 'u'],
        status='necessary_named_source_residual' if residual else 'named_original_source_excluded')


def build():
    source = json.loads(SOURCE.read_text())
    three = ternary_replay()
    assert json.loads(json.dumps(three)) == json.loads(TERNARY.read_text())
    conservation = local_audit()
    assert json.loads(json.dumps(conservation)) == json.loads(CONSERVATION.read_text())['local']
    targets, frame_swaps, transport_count = [], [], 0
    for target in source['targets']:
        sigma = target['source_sigma']
        rejected = [r for i, r in enumerate(ROWS) if not sigma >> i & 1]
        apairs = [p for p in combinations(range(5), 2) if all(r[p[0]] != r[p[1]] for r in rejected)]
        assert set(apairs) == FRAME
        bpair_records = []
        for p in combinations(range(5), 2):
            forced = {singleton(r) for r in rejected if r[p[0]] == r[p[1]]}
            adjacent = [list(e) for e in sorted(FRAME) if set(e) <= forced]
            bpair_records.append(dict(original_b_spoke_pair=p, same_color_forced_rejected_positions=sorted(forced),
                violating_adjacent_rejected_positions=adjacent,
                admissible_generic_single_spoke_position_constraint=not adjacent))
        bpairs = [r['original_b_spoke_pair'] for r in bpair_records
                  if r['admissible_generic_single_spoke_position_constraint']]
        assert len(bpairs) == (7 if sigma == 933 else 9)
        records = target['named_spoke_skeletons']['records']
        frames = []
        for a, b in ((5, 6), (6, 5)):
            for sa, sb in product(apairs, bpairs):
                supports = [list(sa), list(sb)] if a == 5 else [list(sb), list(sa)]
                matches = [(i, r) for i, r in enumerate(records) if r['original_spoke_supports'] == supports]
                assert len(matches) == 1 and matches[0][1]['status'] == 'necessary_skeleton_only'
                frames.append(named_frame(sigma, a, b, list(sa), list(sb), *matches[0]))
        remaining = [f for f in frames if f['status'] == 'necessary_named_source_residual']
        assert len(frames) == (70 if sigma == 933 else 90)
        assert len(remaining) == (22 if sigma == 933 else 26)
        counts = Counter(s['status'] for f in frames for p in f['all_original_U_face_support_placements']
                         for s in p['all_actual_original_U_support_subsets'])
        surviving_supports = sum(len(f['remaining_named_original_U_placements']) for f in remaining)
        surviving_schedules = sum(len(p['complete_singleton_unary_relation_schedules']) for f in remaining
                                  for p in f['remaining_named_original_U_placements'])
        assert surviving_supports == (56 if sigma == 933 else 92)
        assert surviving_schedules == (72 if sigma == 933 else 130)
        for frame in frames:
            partner, = [f for f in frames if f['original_a'] == frame['original_b']
                and f['original_a_spokes'] == frame['original_a_spokes']
                and f['original_b_spokes'] == frame['original_b_spokes']]
            swap = lambda v: 11-v if v in (5, 6) else v
            assert {edge(swap(v), swap(w)) for v, w in frame['original_root_and_boundary_edges']} == set(
                map(tuple, partner['original_root_and_boundary_edges']))
            assert partner['status'] == frame['status']
            left = {(cycle_key([swap(v) for v in p['original_U_face']]), tuple(p['actual_original_U_support']),
                     json.dumps(p['complete_singleton_unary_relation_schedules'], sort_keys=True),
                     tuple(sorted(cycle_key([swap(v) for v in c['face']]) for c in p['compatible_original_C_common_faces'])))
                    for p in frame['remaining_named_original_U_placements']}
            right = {(tuple(p['original_U_face']), tuple(p['actual_original_U_support']),
                      json.dumps(p['complete_singleton_unary_relation_schedules'], sort_keys=True),
                      tuple(sorted(tuple(c['face']) for c in p['compatible_original_C_common_faces'])))
                     for p in partner['remaining_named_original_U_placements']}
            assert left == right
            frame_swaps.append([frame['named_frame_id'], partner['named_frame_id']])
            for sign, shift in product((-1, 1), range(5)):
                move = [(sign*i+shift) % 5 for i in range(5)]
                moved_sigma = relabel_mask(sigma, move)
                for p in frame['remaining_named_original_U_placements']:
                    moved = singleton_schedules(moved_sigma, [move[i] for i in frame['original_a_spokes']],
                        [move[i] for i in p['actual_original_U_support']])
                    # Each whole-frame color map depends on the row. Transport
                    # full unary singleton relations before comparing schedules.
                    expected = []
                    for sched in p['complete_singleton_unary_relation_schedules']:
                        by_row = {}
                        for row, color in zip(rejected, sched['singleton_colors'], strict=True):
                            tr = transport(row, move)
                            by_row[tuple(tr['transported_row'])] = tr['color_permutation'][color]
                        expected.append([by_row[r] for i, r in enumerate(ROWS) if not moved_sigma >> i & 1])
                    assert sorted(list(s['singleton_colors']) for s in moved['surviving_schedules']) == sorted(expected)
                    transport_count += 1
        targets.append(dict(source_sigma=sigma, fresh_original_incidence_named_frames=frames,
            original_a_pair_necessary_constraint='Boundary edge; both a-spoke omissions accept all rows',
            original_a_pair_exclusions=[dict(original_pair=p, same_color_rejected_rows=[r for r in rejected if r[p[0]] == r[p[1]]])
                for p in combinations(range(5), 2) if p not in apairs],
            original_b_pair_necessary_constraints=bpair_records,
            excluded_named_frame_ids=[f['named_frame_id'] for f in frames if f not in remaining],
            remaining_named_original_frames=remaining,
            summary=dict(necessary_named_frames=len(frames), excluded_named_frames=len(frames)-len(remaining),
                remaining_named_frames=len(remaining), remaining_actual_U_face_support_records=surviving_supports,
                remaining_complete_singleton_relation_schedules=surviving_schedules, support_status_counts=dict(counts),
                rotation_assignments=sum(f['exhaustive_original_skeleton_rotations']['rotation_assignments_checked'] for f in frames),
                disk_rotations=sum(len(f['exhaustive_original_skeleton_rotations']['all_disk_rotations']) for f in frames))))
    selected = [f for t in targets for f in t['fresh_original_incidence_named_frames']
                if f['original_a_spokes'] == [0, 1] and f['original_b_spokes'] == [2, 3]]
    assert len(selected) == 4 and all(f['status'] == 'named_original_source_excluded' for f in selected)
    selected_geometry = []
    for f in selected:
        a, b = f['original_a'], f['original_b']
        es = set(map(tuple, f['original_root_and_boundary_edges']))
        selected_geometry.append(dict(named_frame_id=f['named_frame_id'],
            original_U_long_face=[a, 0, 4, 3, b], required_actual_U_support_endpoints=[0, 3],
            allowed_actual_U_supports=[[0, 3], [0, 3, 4]],
            original_U_crosscut_roles=[a, 'u', 'original_U_path_to_actual_attachment_at_3', 3],
            original_C_other_common_face=[a, 1, 2, b], short_face_actual_C_support_envelope=[1, 2],
            long_face_C_crosscut_controls=crosscut_controls([0, 4, 3], a, b, es),
            sealed_C_exact_list_hub_controls=tightness_rows(dict(original_root_order=[a, b],
                original_spoke_supports=[[0, 1], [2, 3]]), a, b, 3, es),
            long_face_C_conclusion='pi_(a,b,u) joint equality under original ax omission; full six-role equality not claimed',
            canonical_same_U_three_row_contradiction=dict(canonical_conflicts(), original_a=a, original_b=b)))
    controls = joint_controls()
    inputs = [Path(__file__), SOURCE, TERNARY, CONSERVATION,
        *[ROOT / 'scripts' / name for name in (
            'c5_excess_two_four_spoke_mixed12_unary_controls.py',
            'c5_excess_two_four_spoke_mixed12_joint_controls.py',
            'c5_excess_two_mixed_core_four_spoke_crosscut.py',
            'c5_excess_two_mixed_core_four_spoke_short_face.py',
            'c5_excess_two_mixed_core_four_spoke_long_face.py',
            'c5_two_spoke_three_contacts.py', 'c5_single_spoke_root_conservation.py')]]
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        trust_boundary=dict(arbitrary_size_proof='Original minimal-core identities, ternary K5 and unary block-palette induction',
            finite_domain='Named skeletons, actual support subsets, complete unary singleton relations and fixed full graph joins',
            old_mixed_11_classification_used=False, source_graphs_enumerated=False,
            source_realization_claimed=False, epsilon_three_proved=False, new_lean_theorem=False),
        inherited_mathematical_payload_audits=dict(complete_two_spoke_ternary_payload_equal=True,
            unary_fixed_color_local_payload_equal=True, old_artifacts_rewritten=False),
        complete_joint_contract=dict(port_order=['a', 'b', 'x', 'y0', 'y1', 'u'],
            C_relation='R_C(x,y0,y1)', U_relation='R_U(u)', guards=['a!=b,x,u', 'b!=y0,y1'],
            x_may_equal_y0_or_y1=True, y0_y1_distinct=True, shared_color_frame=True,
            whole_U_omission_graph_is_minimal_if_rejecting=True,
            only_au_edge_omission_graph_is_not_claimed_minimal=True),
        complete_nonempty_singleton_join_controls=singleton_join_controls(), targets=targets,
        selected_01_23_original_geometry=selected_geometry, root_swap_frames=frame_swaps,
        fixed_full_degree_same_graph_controls=controls,
        summary=dict(source_sigmas=[933, 941], selected_01_23_sources_excluded_with_root_swap=True,
            fresh_incidence_named_frames=[t['summary']['necessary_named_frames'] for t in targets],
            excluded_named_frames=[t['summary']['excluded_named_frames'] for t in targets],
            remaining_named_frames=[t['summary']['remaining_named_frames'] for t in targets],
            remaining_actual_U_support_records=[t['summary']['remaining_actual_U_face_support_records'] for t in targets],
            remaining_unary_relation_schedules=[t['summary']['remaining_complete_singleton_relation_schedules'] for t in targets],
            root_swap_checks=len(frame_swaps), simultaneous_D5_residual_schedule_checks=transport_count,
            fixed_full_degree_graph_controls=controls['summary'], source_graphs_enumerated=False,
            entire_mixed_12_subtype_excluded=False, epsilon_three_proved=False, new_lean_theorem=False))


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
