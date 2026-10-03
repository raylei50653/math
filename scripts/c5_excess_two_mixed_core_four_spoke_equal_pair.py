#!/usr/bin/env python3
"""Four-spoke (2,2): eliminate common original spoke pairs at mixed-(1,1).

Keep the original C/U/V and six-role joint. A same-pair spoke diamond seals
C in one original triangle. The existing arbitrary-size three-hub theorem
extends every proper triangle coloring; original G-C accepts all ten rows.
The paper exclusion is narrow: unequal spoke pairs remain unresolved.
"""
import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_short_support_singleton import three_hub_controls, k5_witness
from c5_excess_two_four_spoke_equal_pair_joint_controls import edge, fixed_graph_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_equal_pair/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
SHORT = ROOT / 'artifacts/c5_short_support_singleton/observations.json'


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


def diamond_rotations():
    records, checks = [], 0
    for pair, swapped in product(combinations(sorted(B), 2), (False, True)):
        h, k = pair
        a, b = (6, 5) if swapped else (5, 6)
        es = {edge(a, b)} | {edge(r, v) for r in (a, b) for v in pair}
        vertices = sorted({z for e in es for z in e})
        options = []
        for z in vertices:
            ns = sorted(w if v == z else v for v, w in es if z in (v, w))
            options.append([(ns[0], *p) for p in permutations(ns[1:])])
        valid = []
        for rings in product(*options):
            checks += 1
            rotation = dict(zip(vertices, rings, strict=True))
            faces = rotation_faces(rotation)
            if len(vertices) - len(es) + len(faces) != 2:
                continue
            shared_faces = [f for f in faces if {a, b} <= set(f)]
            triangles = [f for f in shared_faces if len(f) == 3]
            assert {frozenset(f) for f in triangles} == {
                frozenset((a, b, h)), frozenset((a, b, k))}
            assert sorted(map(len, faces)) == [3, 3, 4]
            valid.append(dict(rotation=[dict(vertex=z, ring=rotation[z]) for z in vertices],
                faces=faces, shared_root_triangle_faces=triangles,
                boundary_arcs_must_use_quadrilateral_face=True))
        assert len(valid) == 2
        records.append(dict(original_spoke_pair=pair, a=a, b=b, edges=sorted(es),
            all_spherical_diamond_rotations=valid,
            scope='Exhaustive diamond rotations; original disk placement is a paper Jordan argument'))
    assert checks == 80 and sum(len(r['all_spherical_diamond_rotations']) for r in records) == 40
    return dict(rotation_assignments_checked=checks, records=records)


def inherited_three_hub_audit():
    old = json.loads(SHORT.read_text())
    payload = three_hub_controls()
    assert json.loads(json.dumps(payload)) == old['three_hub_controls']
    lifted = []
    for ri, item in enumerate(payload['rejected_cases']):
        for h, swapped in product((0, 1), (False, True)):
            a, b = (6, 5) if swapped else (5, 6)
            mapping = dict(zip(item['hub_order'], (a, b, h), strict=True))
            mapping.update({z: 7 + i for i, z in enumerate(item['component_vertices'])})
            es = {edge(mapping[z], mapping[w]) for z, w in item['edges']}
            es |= FRAME | {edge(r, k) for r in (a, b) for k in (0, 1)}
            cv = [mapping[z] for z in item['component_vertices']]
            assert all(sum(z in e for e in es) == 4 for z in cv)
            groups = [[mapping[z] for z in bag] for bag in item['branch_sets']]
            witness = k5_witness(es, groups)
            lifted.append(dict(inherited_rejected_case_index=ri, original_a=a, original_b=b,
                sealing_boundary_vertex=h, original_C_vertices=cv, edges=sorted(es),
                original_C_root_incidence_counts=[sum(edge(r, z) in es for z in cv) for r in (a, b)],
                inherited_list_rejection_reason=item['reason'], **witness,
                scope='General three-hub rejection skeleton; not an incidence-(1,1) degree-5 source'))
    assert len(lifted) == 112
    return dict(original_artifact_sha256=sha256(SHORT.read_bytes()).hexdigest(),
        original_three_hub_payload_recomputed_equal=True,
        attachment_cases=sum(r['attachment_cases'] for r in payload['template_summary']),
        rejected_cases=len(payload['rejected_cases']), lifted_original_K5_skeletons=lifted)


def named_frames(inherited):
    targets, d5_checks, root_checks = [], 0, 0
    for target in inherited['targets']:
        all_frames, excluded, remaining = [], [], []
        for index, item in enumerate(target['named_spoke_skeletons']['records']):
            supports = item['original_spoke_supports']
            if item['status'] != 'necessary_skeleton_only' or list(map(len, supports)) != [2, 2]:
                continue
            frame = dict(inherited_named_skeleton_index=index,
                original_root_order=item['root_order'], original_spoke_supports=supports,
                original_root_and_boundary_edges=item['retained_source_edges'],
                inherited_skeleton_apex_rotation=item['apex_rotation'])
            all_frames.append(frame)
            if supports[0] != supports[1]:
                frame['status'] = 'unequal_original_pairs_unresolved'
                remaining.append(frame)
                continue
            a, b = item['root_order']
            faces = rotation_faces(dict(enumerate(item['apex_rotation'])))
            common_faces = [f for f in faces if {a, b} <= set(f)]
            assert {frozenset(f) for f in common_faces} == {
                frozenset((a, b, h)) for h in supports[0]}
            assert all(len(f) == 3 for f in common_faces)
            es = set(map(tuple, item['retained_source_edges']))
            swapped_edges = {edge(b if z == a else a if z == b else z,
                                  b if w == a else a if w == b else w) for z, w in es}
            assert swapped_edges == es
            frame.update(status='excluded_by_sealed_original_triangle_extension',
                original_possible_sealing_triangles=[[a, b, h] for h in supports[0]],
                inherited_augmented_skeleton_shared_root_faces=common_faces,
                exact_original_C_support_envelope='One selected sealing boundary vertex, not the union of both',
                arbitrary_original_C_size=True, shared_x_and_distinct_x_y_both_covered=True,
                original_G_minus_C_sigma=1023,
                extension_paper_dependency='docs/c5_short_support_singleton.md section 4')
            excluded.append(frame)
            for sign, shift, row in product((-1, 1), range(5), ROWS):
                move = [(sign*i + shift) % 5 for i in range(5)]
                tr = transport(row, move)
                pair = [move[h] for h in supports[0]]
                moved_edges = {edge(move[z] if z in B else z, move[w] if w in B else w)
                               for z, w in item['retained_source_edges']}
                assert all(edge(r, h) in moved_edges for r in (a, b) for h in pair)
                assert edge(a, b) in moved_edges
                assert all(tr['transported_row'][move[h]] == tr['color_permutation'][row[h]] for h in B)
                d5_checks += 1
            root_checks += 1
        sigma = target['source_sigma']
        assert (len(all_frames), len(excluded), len(remaining)) == (
            (47, 7, 40) if sigma == 933 else (75, 9, 66))
        targets.append(dict(source_sigma=sigma, necessary_named_22_frames=len(all_frames),
            excluded_common_pair_frames=excluded, remaining_unequal_pair_frames=remaining))
    return targets, d5_checks, root_checks


def build():
    inherited = json.loads(SOURCE.read_text())
    targets, d5, root = named_frames(inherited)
    rotations, hubs = diamond_rotations(), inherited_three_hub_audit()
    controls = fixed_graph_controls()
    drift = [dict(path=p, recorded_sha256=digest,
                  current_sha256=sha256((ROOT / p).read_bytes()).hexdigest())
             for p, digest in sorted(inherited['input_sha256'].items())
             if sha256((ROOT / p).read_bytes()).hexdigest() != digest]
    assert all(d['path'].startswith('docs/') for d in drift)
    paths = [Path(__file__), SOURCE, SHORT,
        ROOT / 'scripts/c5_excess_two_four_spoke_equal_pair_joint_controls.py']
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        original_single_spoke_provenance=dict(document_provenance_drift=drift,
            old_artifact_rewritten=False, historical_byte_check_rerun=False),
        original_joint_contract=dict(component_order=['C', 'U-at-a', 'V-at-b'],
            ordered_port_roles=['a', 'b', 'x', 'y', 'u', 'v'],
            original_C_tuple_required=['x', 'y'], shared_contact_is_one_vertex=True,
            root_guards=['a!=b', 'a!=x', 'b!=y', 'a!=u', 'b!=v'],
            pinned_fiber='Every literal (a,b) retains all (x,y,u,v) tuples, including empty fibers'),
        targets=targets, exhaustive_diamond_rotation_controls=rotations,
        inherited_three_hub_audit=hubs, fixed_complete_degree_graph_controls=controls,
        summary=dict(source_sigmas=[933, 941], necessary_named_22_frames=[47, 75],
            excluded_common_spoke_pair_frames=[7, 9], remaining_unequal_pair_frames=[40, 66],
            selected_01_01_frames_excluded=2, root_swap_frame_checks=root,
            simultaneous_D5_row_checks=d5, exhaustive_diamond_rotation_assignments=80,
            spherical_diamond_rotations=40, inherited_three_hub_attachment_cases=1201,
            inherited_three_hub_rejected_cases=28, lifted_original_K5_skeletons=112,
            fixed_complete_degree_graphs=len(controls['records']),
            independent_whole_graph_joins=controls['independent_whole_graph_joins'],
            independent_pinned_a_b_fibers=controls['independent_pinned_a_b_fibers'],
            exact_original_edge_restorations=controls['exact_original_edge_restorations'],
            complete_graph_root_swap_variant_checks=controls['complete_graph_root_swap_variant_checks'],
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
