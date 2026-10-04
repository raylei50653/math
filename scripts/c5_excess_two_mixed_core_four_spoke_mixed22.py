#!/usr/bin/env python3
"""Task B: original mixed-(2,2), four spokes and no unary.

Seven labelled contact identities, original omission/core bookkeeping, the
necessary spoke/face/tightness ledger and small complete-relation controls.
Arbitrary-size spoke-omission exclusion is a paper application of the existing
two-spoke three-contact theorem, not an inference from these finite controls.
"""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS
from c5_excess_two_mixed_core_leaf_fibers import transport
from c5_two_spoke_three_contacts import run as three_contact_payload
from c5_short_support_singleton import three_hub_controls
from c5_excess_two_four_spoke_mixed22_joint_controls import fixed_graph_controls

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json'
SOURCE = ROOT / 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
THREE = ROOT / 'artifacts/c5_two_spoke_three_contacts/observations.json'
SHORT = ROOT / 'artifacts/c5_short_support_singleton/observations.json'
U = set(range(4))
NAMES = ('x0', 'x1', 'y0', 'y1')
IDENTITIES = (
    ('D4', (0, 1, 2, 3)),
    ('S00', (0, 1, 0, 2)), ('S01', (0, 1, 2, 0)),
    ('S10', (0, 1, 1, 2)), ('S11', (0, 1, 2, 1)),
    ('Pstraight', (0, 1, 0, 1)), ('Pcross', (0, 1, 1, 0)),
)


def edge(v, w):
    return tuple(sorted((v, w)))


def normalize_partition(t):
    seen = {}
    return tuple(seen.setdefault(v, len(seen)) for v in t)


def contact_identities():
    partitions = {normalize_partition(t) for t in product(range(4), repeat=4)
                  if t[0] != t[1] and t[2] != t[3]}
    assert partitions == {p for _, p in IDENTITIES} and len(partitions) == 7
    records = []
    for name, p in IDENTITIES:
        classes = [[NAMES[i] for i, v in enumerate(p) if v == c]
                   for c in sorted(set(p))]
        records.append(dict(identity=name, original_ordered_roles=NAMES,
            original_vertex_partition=p, original_vertex_classes=classes,
            distinct_original_contact_vertices=len(classes),
            cross_shared_pairs=[[NAMES[i], NAMES[j]] for i in (0, 1) for j in (2, 3)
                                if p[i] == p[j]],
            same_side_contacts_distinct=True,
            original_K_after_a_spoke_omission=dict(vertices='original C + original a',
                b_contact_order=['a', 'y0', 'y1'], all_three_contacts_distinct=True,
                original_a_degree_in_K=2, original_a_is_leaf=False),
            original_K_after_b_spoke_omission=dict(vertices='original C + original b',
                a_contact_order=['b', 'x0', 'x1'], all_three_contacts_distinct=True,
                original_b_degree_in_K=2, original_b_is_leaf=False)))
    return records


def omission_identity():
    factors = [('a:s0', (1, 0)), ('a:s1', (1, 0)),
               ('b:s0', (0, 1)), ('b:s1', (0, 1)), ('original:C', (2, 2))]
    legal = []
    for bits in range(1 << len(factors)):
        selected = [f for i, f in enumerate(factors) if bits >> i & 1]
        lost = [sum(f[1][j] for f in selected) for j in (0, 1)]
        if max(lost) > 1:
            continue
        legal.append(dict(omitted_original_factors=[n for n, _ in selected],
            original_root_degrees=[5-v for v in lost],
            status='original_G_itself' if not selected else
                'excluded_original_single_spoke_q_core' if sum(lost) == 1 else
                'excluded_original_double_spoke_4_4_q_core'))
    assert len(legal) == 9
    assert all('original:C' not in r['omitted_original_factors'] for r in legal)
    return dict(all_original_factor_subsets_checked=32,
        all_degree_admissible_q_core_identities=legal,
        original_C_cannot_be_omitted_from_q_core=True,
        original_G_minus_C_is_a_different_graph_not_a_q_core=True,
        original_G_minus_C_root_degrees=[3, 3],
        original_G_minus_C_accepts_all_rows=True,
        original_G_is_minimal_for_every_rejected_row=True,
        arbitrary_size_dependencies=[
            'original root deletions and ab omission accept all rows',
            'saturation of original degree-four C',
            'excluded original (4,4) cores',
            'spoke omission (4,5) or (5,4) is itself minimal if rejecting',
            'original connected K has three distinct contacts and two root spokes',
            'existing arbitrary-size two-spoke three-contact exclusion'])


def root_pairs(row, sa, sb):
    return [(a, b) for a, b in product(range(4), repeat=2)
            if a != b and a not in {row[i] for i in sa}
            and b not in {row[i] for i in sb}]


def rotation_faces(rotation):
    seen, faces = set(), []
    for v, ns in sorted(rotation.items()):
        for w in ns:
            if (v, w) in seen:
                continue
            start, dart, face = (v, w), (v, w), []
            while dart not in seen:
                seen.add(dart)
                a, b = dart
                face.append(a)
                around = rotation[b]
                dart = b, around[(around.index(a)-1) % len(around)]
            assert dart == start
            faces.append(face)
    return faces


@lru_cache(None)
def disk_rotations(sa, sb):
    es = FRAME | {edge(5, 6)} | {edge(5, i) for i in sa} | {edge(6, i) for i in sb}
    vs = sorted({v for e in es for v in e})
    choices = []
    for v in vs:
        ns = sorted(w if z == v else z for z, w in es if v in (z, w))
        choices.append([(ns[0], *p) for p in permutations(ns[1:])])
    checks, rotations = 0, []
    for ns in product(*choices):
        checks += 1
        rotation = dict(zip(vs, ns, strict=True))
        faces = rotation_faces(rotation)
        outer = [f for f in faces if len(f) == 5 and set(f) == B]
        if len(vs)-len(es)+len(faces) != 2 or len(outer) != 1:
            continue
        common = sorted([f for f in faces if f != outer[0] and {5, 6} <= set(f)])
        assert len(common) == 2
        rotations.append(dict(rotation=[dict(vertex=v, ring=rotation[v]) for v in vs],
            original_outer_boundary=outer[0], all_original_inner_faces=sorted(
                f for f in faces if f != outer[0]), mixed_capable_original_faces=common))
    overlap = len(set(sa) & set(sb))
    assert checks == {0: 64, 1: 96, 2: 144}[overlap]
    # With an actual boundary edge shared by both roots the inside K4 has
    # two choices for the root on its outer triangle, and both orientations.
    assert len(rotations) == (4 if overlap == 2 else 2)
    assert {frozenset(f) for f in rotations[0]['mixed_capable_original_faces']} == {
        frozenset(f) for f in rotations[1]['mixed_capable_original_faces']}
    return dict(rotation_assignments_checked=checks, disk_rotations=rotations)


def attachment_constraints(sigma, sa, sb, face):
    envelope = sorted(set(face) & B)
    rows = [(i, q) for i, q in enumerate(ROWS) if not sigma >> i & 1]
    roles = [('none', ()), ('a_only', (0,)), ('b_only', (1,)), ('shared_a_b', (0, 1))]
    tables = []
    for name, owners in roles:
        permitted = []
        for n in range(4-len(owners)):
            for t in combinations(envelope, n):
                if all(all(len(set([q[h] for h in t] + [p[j] for j in owners]))
                               == len(t)+len(owners)
                           for p in root_pairs(q, sa, sb)) for _, q in rows):
                    permitted.append(t)
        tables.append(dict(original_vertex_role=name, fixed_root_owners=list(owners),
            permissible_actual_boundary_attachment_subsets=permitted,
            internal_degree_for_subset=[dict(actual_attachments=t,
                required_original_C_degree=4-len(t)-len(owners)) for t in permitted],
            necessity='Every actual external neighbor color is distinct for every legal same-frame root pair of every rejected row'))
    lower_degrees = {t['original_vertex_role']: min(
        r['required_original_C_degree'] for r in t['internal_degree_for_subset']) for t in tables}
    assert lower_degrees['none'] >= 2
    if len(envelope) in (2, 4):
        assert lower_degrees['shared_a_b'] == 2
        assert all(d >= 2 for d in lower_degrees.values())
    return dict(original_face=face, exact_actual_support_envelope=envelope,
        rejected_rows_with_complete_original_root_pairs=[dict(row_index=i, row=q,
            original_G_minus_C_root_pairs=root_pairs(q, sa, sb)) for i, q in rows],
        per_original_vertex_attachment_necessities=tables,
        necessary_minimum_C_degree_by_original_role=lower_degrees,
        necessary_table_is_not_source_realizability=True)


def private_leaf_owner_controls():
    """The missing-color membership signature distinguishes all owner types."""
    signatures = []
    for owners in ((), (0,), (1,), (0, 1)):
        # For pairs (missing,h_b) and (h_a,missing), boundary uses no missing.
        signature = [int(0 not in owners), int(1 not in owners)]
        signatures.append(dict(original_owners=list(owners),
            missing_color_membership_in_two_exact_lists=signature))
    assert len({tuple(s['missing_color_membership_in_two_exact_lists']) for s in signatures}) == 4
    return dict(owner_type_signatures=signatures,
        fixed_pair_order=['(missing_color,h_b)', '(h_a,missing_color)'],
        private_vertices_of_one_leaf_odd_cycle_have_one_original_owner_type=True,
        contact_bearing_leaf_odd_cycle_must_be_a_triangle=True,
        scope='Local membership control; arbitrary-size leaf palette identity is a paper consequence of Gallai lists')


def named_frame_ledger(source):
    targets, d5, swaps = [], 0, 0
    for target in source['targets']:
        sigma = target['source_sigma']
        frames = []
        for index, original in enumerate(target['named_spoke_skeletons']['records']):
            supports = original['original_spoke_supports']
            if original['status'] != 'necessary_skeleton_only' or list(map(len, supports)) != [2, 2]:
                continue
            sa, sb = map(tuple, supports)
            redundant = [dict(original_root=original['root_order'][side],
                omitted_original_spoke=[original['root_order'][side], pair[0]],
                retained_same_color_original_spoke=[original['root_order'][side], pair[1]],
                original_row_index=i, original_literal_row=q)
                for side, pair in enumerate((sa, sb)) for i, q in enumerate(ROWS)
                if not sigma >> i & 1 and q[pair[0]] == q[pair[1]]]
            frame = dict(inherited_named_skeleton_index=index, source_sigma=sigma,
                original_root_order=original['root_order'], original_spoke_supports=supports,
                original_root_and_boundary_edges=original['retained_source_edges'],
                original_inherited_apex_rotation=original['apex_rotation'],
                original_G_minus_C_complete_root_relations=[dict(row=q,
                    root_pairs=root_pairs(q, sa, sb)) for q in ROWS],
                all_seven_labelled_contact_identities_retained=True,
                redundant_original_spoke_rejected_row_witnesses=redundant)
            assert all(r['root_pairs'] for r in frame['original_G_minus_C_complete_root_relations'])
            if redundant:
                frame['status'] = 'excluded_by_original_spoke_omission_all_rows'
            else:
                assert edge(*sa) in FRAME and edge(*sb) in FRAME
                rotations = disk_rotations(sa, sb)
                faces = rotations['disk_rotations'][0]['mixed_capable_original_faces']
                frame['fixed_original_skeleton_rotation_audit'] = rotations
                shared = len(set(sa) & set(sb))
                triangle = [f for f in faces if len(f) == 3]
                frame['excluded_sealed_triangle_C_faces'] = triangle
                remaining = [f for f in faces if len(f) != 3]
                frame['retained_original_C_face_necessities'] = [
                    attachment_constraints(sigma, sa, sb, f) for f in remaining]
                if shared == 2:
                    assert len(triangle) == 2 and not remaining
                    frame['status'] = 'excluded_by_original_sealed_triangle_three_hubs'
                else:
                    assert len(remaining) == (1 if shared else 2)
                    assert sorted(len(set(f) & B) for f in remaining) == ([4] if shared else [2, 3])
                    frame['status'] = 'retained_necessary_identity_not_source_realization'
            frames.append(frame)
            for sign, shift in product((-1, 1), range(5)):
                move = [(sign*i+shift) % 5 for i in range(5)]
                for q in ROWS:
                    tr = transport(q, move)
                    moved = sorted((tr['color_permutation'][a], tr['color_permutation'][b])
                                   for a, b in root_pairs(q, sa, sb))
                    assert moved == root_pairs(tr['transported_row'],
                        [move[i] for i in sa], [move[i] for i in sb])
                    d5 += 1
        by_pairs = {tuple(map(tuple, f['original_spoke_supports'])): f for f in frames}
        for (sa, sb), f in by_pairs.items():
            assert by_pairs[(sb, sa)]['status'] == f['status']
            for r in f['original_G_minus_C_complete_root_relations']:
                assert sorted((b, a) for a, b in r['root_pairs']) == root_pairs(r['row'], sb, sa)
            swaps += 1
        counts = {s: sum(f['status'] == s for f in frames) for s in sorted({f['status'] for f in frames})}
        assert len(frames) == (47 if sigma == 933 else 75)
        assert counts['excluded_by_original_spoke_omission_all_rows'] == (22 if sigma == 933 else 50)
        assert counts['excluded_by_original_sealed_triangle_three_hubs'] == 5
        assert counts['retained_necessary_identity_not_source_realization'] == 20
        targets.append(dict(source_sigma=sigma, counts=counts, original_named_frames=frames,
            retained_named_skeleton_indices=[f['inherited_named_skeleton_index'] for f in frames
                if f['status'] == 'retained_necessary_identity_not_source_realization']))
    return targets, d5, swaps


def connected(vs, es):
    vs = set(vs)
    reached = {min(vs)}
    while True:
        new = reached | {w for v in reached for w in vs if edge(v, w) in es}
        if new == reached:
            return reached == vs
        reached = new


def marked_original_minors():
    """Conditional extraction controls, never complete degree/source models."""
    records = []
    for name, p in IDENTITIES:
        x0, x1, y0, y1 = [7+i for i in p]
        # Match every shared y to its actual x, then use the remaining arm.
        ys = [y0, y1]
        assignment = next(t for t in permutations(ys)
            if all(y not in (x0, x1) or y == x for x, y in zip((x0, x1), t)))
        es = FRAME | {edge(5, 6), edge(5, x0), edge(5, x1), edge(x0, x1)}
        es |= {edge(5, i) for i in (0, 1)} | {edge(6, i) for i in (2, 3)}
        es |= {edge(6, y0), edge(6, y1)}
        arms = [[5]]
        for i, (x, y) in enumerate(zip((x0, x1), assignment)):
            arm = [x] if x == y else [x, 20+i, y]
            es |= {edge(v, w) for v, w in zip(arm, arm[1:])}
            arms.append(arm)
        es |= {edge(x0, 0), edge(x1, 4)}
        cv = sorted({v for e in es for v in e} - B - {5, 6})
        assert connected(cv, es)
        assert sum(5 in e for e in es) == sum(6 in e for e in es) == 5
        for omitted in (0, 1):
            kept = 1-omitted
            original_m = es - {edge(5, omitted)}
            groups = [[6], *arms, sorted(B)]
            assert all(connected(g, original_m) for g in groups)
            assert sum(map(len, groups)) == len(set(v for g in groups for v in g))
            adj = []
            for i, j in combinations(range(5), 2):
                witness = next((edge(v, w) for v in sorted(groups[i]) for w in sorted(groups[j])
                                if edge(v, w) in original_m), None)
                assert witness is not None
                adj.append(dict(branch_set_pair=[i, j], original_edge=witness))
            records.append(dict(identity=name, original_a=5, original_b=6,
                original_C_vertices=cv, original_ordered_C_contacts=[x0, x1, y0, y1],
                original_G_edges=sorted(es), omitted_original_a_spoke=[5, omitted],
                original_M_edges=sorted(original_m), actual_active_triangle=[5, x0, x1],
                actual_original_contact_arms=arms,
                actual_boundary_tethers=[[5, kept], [x0, 0], [x1, 4]],
                five_original_connected_branch_sets=groups, ten_original_edge_witnesses=adj,
                missing_unused_degree_edges_not_completed=True,
                scope='Conditional original marked K5 minor; not a degree/list, disk or complete-Sigma realization'))
    assert len(records) == 14
    return records


def build():
    source = json.loads(SOURCE.read_text())
    three = three_contact_payload()
    short = three_hub_controls()
    assert json.loads(json.dumps(three)) == json.loads(THREE.read_text())
    assert json.loads(json.dumps(short)) == json.loads(SHORT.read_text())['three_hub_controls']
    targets, d5, swaps = named_frame_ledger(source)
    controls = fixed_graph_controls()
    inputs = [Path(__file__), ROOT / 'scripts/c5_excess_two_four_spoke_mixed22_joint_controls.py',
              SOURCE, THREE, SHORT, ROOT / 'scripts/c5_two_spoke_three_contacts.py',
              ROOT / 'scripts/c5_short_support_singleton.py']
    return dict(schema=1, scope=__doc__, pattern_order=ROWS,
        input_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
        contact_identity_table=contact_identities(), original_omission_q_core_identity=omission_identity(),
        original_relation_contract=dict(C_order=NAMES, joint_order=['a', 'b', *NAMES],
            one_literal_color_frame=True, shared_roles_are_one_original_vertex=True,
            all_C_internal_edges_attachments_and_bridges_retained=True,
            original_root_guards=['a!=b,x0,x1', 'b!=y0,y1', 'a avoids original a-spokes',
                                  'b avoids original b-spokes'],
            original_K_a_omission_order=['a', 'y0', 'y1'], original_K_marked_a_degree=2,
            full_relations_witnesses_and_empty_root_pair_fibers_required=True),
        inherited_three_contact_mathematical_payload_recomputed_equal=True,
        inherited_three_hub_mathematical_payload_recomputed_equal=True,
        old_artifacts_rewritten=False, targets=targets,
        conditional_marked_original_K5_minor_controls=marked_original_minors(),
        private_leaf_original_owner_identity_controls=private_leaf_owner_controls(),
        fixed_complete_degree_original_relation_controls=controls,
        summary=dict(contact_identities=7, same_side_contacts_always_distinct=True,
            all_original_spoke_omissions_accept_all_rows=True,
            all_original_rejected_q_cores_are_original_G=True,
            source_named_frames=[47, 75], redundant_spoke_excluded_frames=[22, 50],
            adjacent_pair_necessary_frames=[25, 25], equal_pair_excluded_frames=[5, 5],
            retained_necessary_named_frames=[20, 20],
            retained_unequal_pairs_sharing_a_boundary_vertex=[10, 10],
            retained_disjoint_pairs=[10, 10],
            conditional_marked_original_K5_minors=14,
            fixed_unique_adjacent_skeleton_rotation_assignments=5*144+10*96+10*64,
            fixed_unique_adjacent_disk_rotations=60,
            simultaneous_D5_root_pair_checks=d5, root_swap_frame_checks=swaps,
            complete_degree_control_summary=controls['summary'],
            all_mixed22_sources_excluded=False, source_realizability_claimed=False,
            source_graph_catalogue_enumerated=False, unary_crosscut_used=False,
            epsilon_three_proved=False, new_lean_theorem=False))


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
