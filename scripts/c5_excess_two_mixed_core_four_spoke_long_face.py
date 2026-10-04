#!/usr/bin/env python3
"""Four-spoke (2,2): two original unary supports cannot share a three-edge arc.

Read the inherited named frames without changing their certificates. All
disk rotations, actual support subsets, literal frame transport and explicit
apex K3,3 subdivisions are fixed controls. The unbounded source exclusion
is the paper crosscut plus short-support argument, not graph enumeration.
"""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, span
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_excess_two_mixed_core_four_spoke_short_face import disk_rotations, short_face
from c5_excess_two_four_spoke_binary_star import subdivision, verify_subdivision
from c5_short_support_singleton import local_controls, three_hub_controls
from c5_excess_two_four_spoke_long_face_joint_controls import fixed_graph_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_long_face/observations.json'
PREVIOUS = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_short_face/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
SHORT = ROOT / 'artifacts/c5_short_support_singleton/observations.json'


def edge(z, w):
    return tuple(sorted((z, w)))


def short_support_instance(support, owner, roots, edges):
    pair = min(e for e in FRAME if set(support) <= set(e))
    other, = set(roots) - {owner}
    paths = [[owner, h] for h in sorted(B - set(pair)) if edge(owner, h) in edges]
    paths += [[owner, other, h] for h in sorted(B - set(pair))
              if edge(owner, other) in edges and edge(other, h) in edges]
    path = min(paths, key=lambda p: (len(p), p))
    assert set(path[1:-1]) <= set(roots) - {owner}
    assert path[-1] not in pair and all(edge(z, w) in edges
                                      for z, w in zip(path, path[1:]))
    return dict(actual_support=sorted(support), original_unary_owner=owner,
        enclosing_original_boundary_edge=pair, original_external_path=path,
        path_avoids_original_C_U_V=True)


def oriented_arc(face, roots):
    a, b = roots
    i = face.index(a)
    path = face[i:] + face[:i]
    if path[1] == b:
        path = [a, *path[:0:-1]]
    assert path[-1] == b and set(path[1:-1]) <= B
    assert all(edge(z, w) in FRAME for z, w in zip(path[1:-2], path[2:-1]))
    return path[1:-1]


def support_controls(arc, roots, edges):
    assert len(arc) == 4
    a, b = roots
    supports = [tuple(h for i, h in enumerate(arc) if bits >> i & 1)
                for bits in range(16)]
    position = {h: i for i, h in enumerate(arc)}
    crossings = []
    for j in range(1, 4):
        for k in range(j):
            # Contract only paths internal to the two original components.
            # The apex is placed outside the original C5 disk; it is not a
            # source vertex and never appears in any coloring relation.
            es = edges | {edge(a, 7), edge(7, arc[j]), edge(b, 8), edge(8, arc[k])}
            es |= {edge(9, h) for h in B}
            cert = subdivision(tuple(sorted(es)))
            assert cert is not None
            verify_subdivision(es, cert)
            crossings.append(dict(a_support_endpoint=arc[j], b_support_endpoint=arc[k],
                ordered_boundary_endpoints=[a, arc[k], arc[j], b],
                original_a_U_path_roles=[a, 'internal_path_in_original_U', arc[j]],
                original_b_V_path_roles=[b, 'internal_path_in_original_V', arc[k]],
                contracted_path_vertices=dict(original_U=7, original_V=8),
                outside_boundary_apex=9, contracted_original_skeleton_edges=sorted(es),
                explicit_apex_K33_subdivision=cert,
                scope='Topology control after original disjoint-path contractions; '
                      'no degree or source-realization assertion'))
    records, ordered, both_long = [], 0, 0
    for su, sv in product(supports, repeat=2):
        pu, pv = [position[h] for h in su], [position[h] for h in sv]
        diameters = [max(p) - min(p) if p else 0 for p in (pu, pv)]
        compatible = not su or not sv or max(pu) <= min(pv)
        both = span(set(su)) >= 2 and span(set(sv)) >= 2
        crossing = None
        if not compatible:
            crossing, = [i for i, c in enumerate(crossings)
                if c['a_support_endpoint'] == arc[max(pu)]
                and c['b_support_endpoint'] == arc[min(pv)]]
        short = []
        if compatible:
            ordered += 1
            assert sum(diameters) <= 3
            for support, owner, diameter in zip((su, sv), roots, diameters, strict=True):
                if diameter <= 1:
                    short.append(short_support_instance(support, owner, roots, edges))
            assert short
        if both:
            both_long += 1
            assert not compatible and crossing is not None
        records.append(dict(actual_original_U_support=su, actual_original_V_support=sv,
            common_face_arc_positions=[pu, pv], interval_diameters=diameters,
            minimal_cyclic_support_spans=[span(set(su)), span(set(sv))],
            original_disjoint_path_order_compatible=compatible,
            alternating_path_control_index=crossing,
            both_supports_nonshort=both, certified_short_original_unaries=short))
    assert ordered == 80 and both_long == 64
    return dict(common_original_face_boundary_arc=arc, actual_support_pairs=records,
        alternating_original_path_controls=crossings,
        total_support_pairs=256, order_compatible_pairs_including_empty=ordered,
        order_compatible_nonempty_pairs=49, both_nonshort_pairs=both_long,
        order_compatible_both_nonshort_pairs=0,
        shared_support_endpoint_allowed=True,
        scope='All actual support subsets within this single fixed original face envelope')


def frame_analysis(frame, original):
    assert frame['original_root_order'] == original['root_order']
    assert frame['original_spoke_supports'] == original['original_spoke_supports']
    assert frame['original_root_and_boundary_edges'] == original['retained_source_edges']
    assert frame['inherited_skeleton_apex_rotation'] == original['apex_rotation']
    roots = frame['original_root_order']
    edges = set(map(tuple, frame['original_root_and_boundary_edges']))
    rotations = disk_rotations(edges)
    faces = rotations['all_original_C5_outer_face_rotations'][0]['original_disk_faces']
    owners = []
    for r in roots:
        incident = [f for f in faces if r in f]
        long = [f for f in incident if span(set(f) & B) >= 2]
        owners.append(dict(original_owner=r,
            all_incident_faces=incident, long_incident_faces=long,
            short_incident_face_lemma_instances=[short_face(f, r, roots, edges)
                for f in incident if span(set(f) & B) <= 1]))
    qualified = (all(len(o['long_incident_faces']) == 1 for o in owners)
        and set(owners[0]['long_incident_faces'][0]) ==
            set(owners[1]['long_incident_faces'][0]))
    result = {k: v for k, v in frame.items() if k != 'status'}
    result.update(inherited_status=frame['status'],
        status='excluded_by_common_long_face_unary_order' if qualified
            else 'unequal_original_pairs_unresolved',
        exhaustive_fixed_skeleton_rotations=rotations,
        original_unary_incident_face_analysis=owners,
        excluded_by_common_long_face_unary_order=qualified)
    if qualified:
        face = owners[0]['long_incident_faces'][0]
        arc = oriented_arc(face, roots)
        assert len(arc) == 4
        result.update(common_original_long_face=face,
            common_long_face_support_controls=support_controls(arc, roots, edges))
    return result


def transport_checks(record):
    roots = record['original_root_order']
    es = set(map(tuple, record['original_root_and_boundary_edges']))
    controls = record['common_long_face_support_controls']
    support_checks, row_checks, subdivision_checks = 0, 0, 0
    for sign, shift in product((-1, 1), range(5)):
        move = [(sign*i + shift) % 5 for i in range(5)]
        rename = lambda z: move[z] if z in B else z
        edges = {edge(rename(z), rename(w)) for z, w in es}
        moved_arc = list(map(rename, controls['common_original_face_boundary_arc']))
        assert all(edge(z, w) in FRAME for z, w in zip(moved_arc, moved_arc[1:]))
        for pair in controls['actual_support_pairs']:
            su, sv = [list(map(rename, pair[k])) for k in
                      ('actual_original_U_support', 'actual_original_V_support')]
            assert [span(set(s)) for s in (su, sv)] == pair['minimal_cyclic_support_spans']
            pos = [[moved_arc.index(h) for h in s] for s in (su, sv)]
            assert (not su or not sv or max(pos[0]) <= min(pos[1])) == \
                pair['original_disjoint_path_order_compatible']
            for instance in pair['certified_short_original_unaries']:
                path = list(map(rename, instance['original_external_path']))
                enclosing = {rename(h) for h in instance['enclosing_original_boundary_edge']}
                assert set(map(rename, instance['actual_support'])) <= enclosing
                assert path[-1] not in enclosing
                assert all(edge(z, w) in edges for z, w in zip(path, path[1:]))
            support_checks += 1
        for control in controls['alternating_original_path_controls']:
            graph = {edge(rename(z), rename(w)) for z, w in control['contracted_original_skeleton_edges']}
            cert = control['explicit_apex_K33_subdivision']
            moved = dict(left=list(map(rename, cert['left'])), right=list(map(rename, cert['right'])),
                paths=[list(map(rename, path)) for path in cert['paths']])
            verify_subdivision(graph, moved)
            subdivision_checks += 1
        for row in ROWS:
            tr = transport(row, move)
            assert all(tr['transported_row'][move[h]] ==
                       tr['color_permutation'][row[h]] for h in B)
            row_checks += 1
    return support_checks, row_checks, subdivision_checks


def build():
    previous, source, short = (json.loads(p.read_text()) for p in (PREVIOUS, SOURCE, SHORT))
    assert json.loads(json.dumps(local_controls())) == short['local_controls']
    assert json.loads(json.dumps(three_hub_controls())) == short['three_hub_controls']
    targets, counts, root_swaps = [], [0, 0, 0], 0
    for target in previous['targets']:
        sigma = target['source_sigma']
        original = next(t for t in source['targets'] if t['source_sigma'] == sigma)
        records = original['named_spoke_skeletons']['records']
        excluded, remaining, analyses = [], [], []
        for frame in target['remaining_unequal_pair_frames']:
            if len(set(frame['original_spoke_supports'][0]) &
                   set(frame['original_spoke_supports'][1])) != 1:
                remaining.append(frame)
                continue
            record = frame_analysis(frame, records[frame['inherited_named_skeleton_index']])
            analyses.append(record)
            if record['excluded_by_common_long_face_unary_order']:
                excluded.append(record)
                counts = [a+b for a, b in zip(counts, transport_checks(record), strict=True)]
            else:
                remaining.append(frame)
        assert (len(analyses), len(excluded), len(remaining)) == (
            (18, 10, 22) if sigma == 933 else (32, 10, 40))
        selected = {98, 126} if sigma == 933 else {135, 195}
        assert selected <= {r['inherited_named_skeleton_index'] for r in excluded}
        for record in excluded:
            a, b = record['original_root_order']
            swap = lambda z: b if z == a else a if z == b else z
            es = {edge(swap(z), swap(w)) for z, w in record['original_root_and_boundary_edges']}
            partner, = [r for r in excluded if set(map(tuple, r['original_root_and_boundary_edges'])) == es]
            assert partner['original_spoke_supports'] == record['original_spoke_supports'][::-1]
            assert partner['common_long_face_support_controls']['common_original_face_boundary_arc'] == \
                record['common_long_face_support_controls']['common_original_face_boundary_arc'][::-1]
            root_swaps += 1
        targets.append(dict(source_sigma=sigma,
            inherited_remaining_unequal_pair_frames=len(target['remaining_unequal_pair_frames']),
            one_common_boundary_vertex_analysis=analyses,
            newly_excluded_named_frame_indices=[r['inherited_named_skeleton_index'] for r in excluded],
            remaining_unequal_pair_frames=remaining,
            remaining_one_common_vertex_frames=len(analyses)-len(excluded),
            remaining_disjoint_pair_frames=sum(not(set(f['original_spoke_supports'][0]) &
                set(f['original_spoke_supports'][1])) for f in remaining)))
    controls = fixed_graph_controls()
    inputs = [Path(__file__), PREVIOUS, SOURCE, SHORT,
        ROOT / 'scripts/c5_excess_two_four_spoke_long_face_joint_controls.py']
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        original_joint_contract=dict(component_order=['C', 'U-at-a', 'V-at-b'],
            port_order=['a', 'b', 'x', 'y', 'u', 'v'],
            shared_contact_is_one_original_vertex=True,
            guards=['a!=b', 'a!=x', 'b!=y', 'a!=u', 'b!=v'],
            noncritical_edge_chosen_from_fixed_original_supports=True,
            projection_equality_preserves_original_C_and_other_unary=True,
            full_six_role_joint_equality_claimed=False),
        inherited_short_support_mathematical_payload_audit=dict(
            local_controls_equal=True, three_hub_controls_equal=True,
            old_artifacts_rewritten=False), targets=targets,
        fixed_complete_degree_graph_controls=controls,
        summary=dict(source_sigmas=[933, 941], inherited_unequal_pair_frames=[32, 50],
            newly_excluded_common_long_face_frames=[10, 10], remaining_unequal_pair_frames=[22, 40],
            remaining_one_common_vertex_frames=[8, 22], remaining_disjoint_pair_frames=[14, 18],
            selected_original_indices=[[98, 126], [135, 195]],
            selected_01_04_and_root_swap_excluded=True,
            fixed_skeleton_rotation_assignments=96*50, valid_disk_skeleton_rotations=2*50,
            actual_support_pair_checks=256*20, both_nonshort_support_pairs=64*20,
            compatible_both_nonshort_support_pairs=0, explicit_apex_K33_subdivisions=6*20,
            root_swap_frame_checks=root_swaps, simultaneous_D5_support_pair_checks=counts[0],
            simultaneous_D5_row_checks=counts[1], D5_subdivision_path_checks=counts[2],
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
