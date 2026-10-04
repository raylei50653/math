#!/usr/bin/env python3
"""Four-spoke (2,2): a unary in only short original faces is not critical.

Reuse the named unequal-pair frames. Exhaustive rotations audit the fixed
boundary skeleton, not source graphs. Arbitrary-size coverage comes from
the paper crosscut argument and the existing unary short-support theorem.
"""
import argparse
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, span
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_short_support_singleton import local_controls, three_hub_controls
from c5_excess_two_four_spoke_short_face_joint_controls import fixed_graph_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_short_face/observations.json'
PAIR = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_equal_pair/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
SHORT = ROOT / 'artifacts/c5_short_support_singleton/observations.json'


def edge(a, b):
    return tuple(sorted((a, b)))


def rotation_faces(rotation):
    seen, faces = set(), []
    for z, ring in sorted(rotation.items()):
        for w in ring:
            if (z, w) in seen:
                continue
            start, dart, face = (z, w), (z, w), []
            while dart not in seen:
                seen.add(dart)
                a, b = dart
                face.append(a)
                around = rotation[b]
                dart = b, around[(around.index(a) - 1) % len(around)]
            assert dart == start
            faces.append(face)
    return faces


def face_key(face):
    return min(tuple(face[i:] + face[:i]) for i in range(len(face)))


def disk_rotations(edges):
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
        if len(vertices) - len(edges) + len(faces) != 2:
            continue
        outer = [f for f in faces if len(f) == 5 and set(f) == B]
        if len(outer) != 1:
            continue
        inner = sorted((f for f in faces if f != outer[0]), key=face_key)
        records.append(dict(rotation=[dict(vertex=z, ring=rotation[z]) for z in vertices],
            original_outer_boundary_face=outer[0], original_disk_faces=inner))
    assert checked == 96 and len(records) == 2
    assert {frozenset(f) for f in records[0]['original_disk_faces']} == {
        frozenset(f) for f in records[1]['original_disk_faces']}
    return dict(rotation_assignments_checked=checked,
        all_original_C5_outer_face_rotations=records,
        scope='Fixed seven-vertex original skeleton rotations; no source graph enumeration')


def short_face(face, r, roots, edges):
    support = set(face) & B
    enclosing = min(e for e in FRAME if support <= set(e))
    other, = set(roots) - {r}
    paths = [[r, h] for h in sorted(B - set(enclosing)) if edge(r, h) in edges]
    paths += [[r, other, h] for h in sorted(B - set(enclosing))
              if edge(r, other) in edges and edge(other, h) in edges]
    assert paths
    path = min(paths, key=lambda p: (len(p), p))
    assert len(set(path)) == len(path) and set(path[1:-1]) <= set(roots) - {r}
    assert all(edge(z, w) in edges for z, w in zip(path, path[1:]))
    return dict(original_face_cycle=face,
        exact_face_boundary_envelope=sorted(support),
        actual_unary_support_condition='Subset of this one fixed original face envelope',
        enclosing_original_boundary_edge=enclosing,
        original_external_path=path,
        path_avoids_original_C_U_V=True,
        original_unary_owner=r, original_contact_edge_role=f'{r}-u_at_{r}')


def frame_analysis(frame, original):
    assert frame['original_root_order'] == original['root_order']
    assert frame['original_spoke_supports'] == original['original_spoke_supports']
    assert frame['original_root_and_boundary_edges'] == original['retained_source_edges']
    assert frame['inherited_skeleton_apex_rotation'] == original['apex_rotation']
    roots = frame['original_root_order']
    sa, sb = map(set, frame['original_spoke_supports'])
    assert len(sa & sb) == 1
    edges = set(map(tuple, frame['original_root_and_boundary_edges']))
    rotations = disk_rotations(edges)
    faces = rotations['all_original_C5_outer_face_rotations'][0]['original_disk_faces']
    apex_faces = [f for f in rotation_faces(dict(enumerate(original['apex_rotation'])))
                  if original['boundary_apex'] not in f]
    assert {frozenset(f) for f in faces} == {frozenset(f) for f in apex_faces}
    root_records = []
    for r in roots:
        incident = [f for f in faces if r in f]
        assert len(incident) == 3
        eligible = all(span(set(f) & B) <= 1 for f in incident)
        root_records.append(dict(original_owner=r,
            incident_face_envelopes=[dict(face=f, boundary_envelope=sorted(set(f) & B),
                                         minimal_boundary_span=span(set(f) & B)) for f in incident],
            all_faces_short=eligible,
            short_support_lemma_instances=[short_face(f, r, roots, edges) for f in incident]
                if eligible else []))
    qualified = [r['original_owner'] for r in root_records if r['all_faces_short']]
    assert len(qualified) <= 1
    identity = {k: v for k, v in frame.items() if k != 'status'}
    return dict(**identity, inherited_status=frame['status'],
        status='excluded_by_noncritical_original_unary_edge' if qualified
            else 'unequal_original_pairs_unresolved',
        exhaustive_fixed_skeleton_rotations=rotations,
        original_unary_face_analysis=root_records,
        excluded_by_noncritical_original_unary_edge=bool(qualified),
        certified_noncritical_unary_owners=qualified)


def d5_checks(record):
    roots = record['original_root_order']
    edges = set(map(tuple, record['original_root_and_boundary_edges']))
    checks = 0
    for sign, shift in product((-1, 1), range(5)):
        move = [(sign*i + shift) % 5 for i in range(5)]
        renamed = lambda z: move[z] if z in B else z
        moved_edges = {edge(renamed(z), renamed(w)) for z, w in edges}
        for rr in record['original_unary_face_analysis']:
            for item in rr['short_support_lemma_instances']:
                pair = {move[z] for z in item['enclosing_original_boundary_edge']}
                support = {move[z] for z in item['exact_face_boundary_envelope']}
                path = list(map(renamed, item['original_external_path']))
                assert tuple(sorted(pair)) in FRAME and support <= pair and path[-1] not in pair
                assert set(path[1:-1]) <= set(roots)
                assert all(edge(z, w) in moved_edges for z, w in zip(path, path[1:]))
                for row in ROWS:
                    tr = transport(row, move)
                    assert all(tr['transported_row'][move[h]] ==
                               tr['color_permutation'][row[h]] for h in B)
                    checks += 1
    return checks


def build():
    pair, source, short = (json.loads(p.read_text()) for p in (PAIR, SOURCE, SHORT))
    assert json.loads(json.dumps(local_controls())) == short['local_controls']
    assert json.loads(json.dumps(three_hub_controls())) == short['three_hub_controls']
    targets, d5, root_swaps = [], 0, 0
    for target in pair['targets']:
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
            if record['excluded_by_noncritical_original_unary_edge']:
                excluded.append(record)
                d5 += d5_checks(record)
            else:
                remaining.append(frame)
        assert (len(analyses), len(excluded), len(remaining)) == (
            (26, 8, 32) if sigma == 933 else (48, 16, 50))
        selected = {97, 111} if sigma == 933 else {133, 153}
        assert selected <= {r['inherited_named_skeleton_index'] for r in excluded}
        next_indices = {98, 126} if sigma == 933 else {135, 195}
        assert next_indices <= {r['inherited_named_skeleton_index'] for r in remaining}
        for record in excluded:
            a, b = record['original_root_order']
            swap = lambda z: b if z == a else a if z == b else z
            es = {edge(swap(z), swap(w)) for z, w in record['original_root_and_boundary_edges']}
            partner, = [r for r in excluded if set(map(tuple, r['original_root_and_boundary_edges'])) == es]
            assert partner['original_spoke_supports'] == record['original_spoke_supports'][::-1]
            assert partner['certified_noncritical_unary_owners'] == list(map(swap,
                record['certified_noncritical_unary_owners']))
            root_swaps += 1
        targets.append(dict(source_sigma=sigma,
            inherited_unequal_pair_frames=len(target['remaining_unequal_pair_frames']),
            one_common_boundary_vertex_analysis=analyses,
            newly_excluded_named_frame_indices=[r['inherited_named_skeleton_index'] for r in excluded],
            remaining_unequal_pair_frames=remaining,
            remaining_one_common_vertex_frames=sum(len(set(f['original_spoke_supports'][0]) &
                set(f['original_spoke_supports'][1])) == 1 for f in remaining),
            remaining_disjoint_pair_frames=sum(not(set(f['original_spoke_supports'][0]) &
                set(f['original_spoke_supports'][1])) for f in remaining)))
    controls = fixed_graph_controls()
    inputs = [Path(__file__), PAIR, SOURCE, SHORT,
        ROOT / 'scripts/c5_excess_two_four_spoke_short_face_joint_controls.py',
        ROOT / 'scripts/c5_short_support_singleton.py']
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        original_joint_contract=dict(component_order=['C', 'U-at-a', 'V-at-b'],
            port_order=['a', 'b', 'x', 'y', 'u', 'v'],
            shared_contact_is_one_original_vertex=True,
            guards=['a!=b', 'a!=x', 'b!=y', 'a!=u', 'b!=v'],
            short_unary_conclusion='For every boundary row, the original unary contact can avoid every root color',
            extension_equality='Projection retaining roots, both C contacts and the other unary contact',
            full_six_role_joint_equality_claimed=False),
        inherited_short_support_mathematical_payload_audit=dict(
            local_controls_equal=True, three_hub_controls_equal=True,
            old_artifacts_rewritten=False),
        targets=targets, fixed_complete_degree_graph_controls=controls,
        summary=dict(source_sigmas=[933, 941], inherited_unequal_pair_frames=[40, 66],
            newly_excluded_short_face_frames=[8, 16], remaining_unequal_pair_frames=[32, 50],
            remaining_one_common_vertex_frames=[18, 32], remaining_disjoint_pair_frames=[14, 18],
            selected_original_indices=[[97, 111], [133, 153]],
            selected_01_02_and_root_swap_excluded=True,
            fixed_skeleton_rotation_assignments=96 * 74, valid_disk_skeleton_rotations=2 * 74,
            root_swap_frame_checks=root_swaps, simultaneous_D5_row_lemma_checks=d5,
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
