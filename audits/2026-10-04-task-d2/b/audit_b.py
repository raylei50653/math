#!/usr/bin/env python3
"""Independent read-only mixed22 audit: JSON and Python standard library only.

The source and B producer/checker/helper modules are never imported. All
relations are recomputed from serialized original edges by fresh MRV search.
This checks finite payloads; arbitrary-size and topology assertions remain
paper dependencies, not conclusions of the enumeration.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time


PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument('--repo', type=Path, default=Path('/tmp/math-task-d2-snapshot'))
PARSER.add_argument('--output', type=Path, default=Path(__file__).resolve().parent)
ARGS = PARSER.parse_args()
BASE = ARGS.repo.resolve()
OUT = ARGS.output.resolve()
B = set(range(5))
U = set(range(4))
ROLES = ['x0', 'x1', 'y0', 'y1']
COUNTS = Counter()
START = time.monotonic()


def edge(v, w):
    assert v != w
    return tuple(sorted((v, w)))


FRAME = {edge(h, (h + 1) % 5) for h in B}


def edges(values):
    result = [edge(*e) for e in values]
    assert len(result) == len(set(result)), 'duplicate serialized edge'
    return set(result)


def unique(values):
    assert len(values) == len(set(values)), 'duplicate serialized array member'
    return set(values)


def normalize(values):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in values)


def powerset(values):
    vs = sorted(values)
    return [tuple(t) for n in range(len(vs) + 1) for t in combinations(vs, n)]


def connected(vs, es):
    vs = set(vs)
    if not vs:
        return False
    reached = {min(vs)}
    while True:
        more = reached | {w for v, w in es if v in reached and w in vs}
        more |= {v for v, w in es if w in reached and v in vs}
        if reached == more:
            return reached == vs
        reached = more


def solve(vs, es, beta, ports, pinned=None):
    """Fresh MRV enumeration; fixed colors stay in one literal frame."""
    vs = set(vs)
    assert B <= vs and all({v, w} <= vs for v, w in es)
    adj = {v: set() for v in vs}
    for v, w in es:
        adj[v].add(w)
        adj[w].add(v)
    f = dict(enumerate(beta))
    for v, c in (pinned or {}).items():
        if v in f and f[v] != c:
            return set()
        f[v] = c
    assert set(f) <= vs
    if any(f[v] == f[w] for v, w in es if v in f and w in f):
        return set()
    remaining = vs - set(f)
    result = set()

    def visit():
        if not remaining:
            result.add(tuple(f[v] for v in ports))
            return
        domains = {v: U - {f[w] for w in adj[v] if w in f} for v in remaining}
        v = min(remaining, key=lambda z: (len(domains[z]), -len(adj[z]), z))
        if not domains[v]:
            return
        remaining.remove(v)
        for c in sorted(domains[v]):
            f[v] = c
            visit()
        f.pop(v)
        remaining.add(v)

    visit()
    return result


def witness(order, values, es, beta, ports, t):
    assert len(order) == len(values) and len(unique(order)) == len(order)
    f = dict(zip(order, values, strict=True))
    assert all(c in U for c in f.values())
    assert all(f[h] == beta[h] for h in B)
    assert all(f[v] != f[w] for v, w in es)
    assert tuple(f[v] for v in ports) == tuple(t)
    return f


def stored_relation(items, order, es, beta, ports, count_key):
    ts = [tuple(x['tuple']) for x in items]
    unique(ts)
    for item in items:
        witness(order, item['coloring'], es, beta, ports, item['tuple'])
        COUNTS[count_key] += 1
    return set(ts)


def rotation_faces(rotation, es, require_sphere=True):
    vs = {v for e in es for v in e}
    assert set(rotation) == vs
    for v, ring in rotation.items():
        assert len(unique(ring)) == len(ring)
        assert set(ring) == {w if z == v else z for z, w in es if v in (z, w)}
    darts = {(v, w) for v, w in es} | {(w, v) for v, w in es}
    visited, result = set(), []
    for start in sorted(darts):
        if start in visited:
            continue
        dart, face = start, []
        while dart not in visited:
            visited.add(dart)
            v, w = dart
            face.append(v)
            ring = rotation[w]
            dart = (w, ring[(ring.index(v) - 1) % len(ring)])
        assert dart == start
        result.append(face)
    assert visited == darts
    if require_sphere:
        assert len(vs) - len(es) + len(result) == 2
    return result


def rotation_key(rot):
    result = []
    for v, ring in sorted(rot.items()):
        i = ring.index(min(ring))
        result.append((v, tuple(ring[i:] + ring[:i])))
    return tuple(result)


def exhaustive_disk_rotations(es):
    vs = sorted({v for e in es for v in e})
    choices = []
    for v in vs:
        ns = sorted(w if z == v else z for z, w in es if v in (z, w))
        choices.append([[ns[0], *p] for p in permutations(ns[1:])])
    all_keys, n = set(), 0
    for rings in product(*choices):
        n += 1
        rot = dict(zip(vs, rings, strict=True))
        fs = rotation_faces(rot, es, require_sphere=False)
        if len(vs) - len(es) + len(fs) != 2:
            continue
        outers = [f for f in fs if len(f) == 5 and set(f) == B]
        if len(outers) == 1:
            all_keys.add(rotation_key(rot))
    return n, all_keys


def transport(beta, move):
    moved = [None] * 5
    for h in B:
        moved[move[h]] = beta[h]
    target = normalize(moved)
    cp = dict(zip(moved, target))
    cp.update(zip(sorted(U - set(cp)), sorted(U - set(cp.values()))))
    perm = [cp[c] for c in range(4)]
    assert sorted(perm) == list(range(4))
    assert all(target[move[h]] == perm[beta[h]] for h in B)
    return target, perm


def renamed_rotation(rot, rename):
    return {rename(v): [rename(w) for w in ring] for v, ring in rot.items()}


def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk(value)


SOURCE_REL = 'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json'
B_REL = 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json'
SOURCE = json.loads((BASE / SOURCE_REL).read_text())
DATA = json.loads((BASE / B_REL).read_text())
ROWS = [tuple(q) for q in DATA['pattern_order']]
assert ROWS == [tuple(q) for q in SOURCE['pattern_order']]
canonical = sorted({normalize(q) for q in product(range(4), repeat=5)
                    if all(q[h] != q[(h + 1) % 5] for h in B)})
assert ROWS == canonical and len(unique(ROWS)) == 10
RESULT = {
    'schema': 1,
    'scope': __doc__,
    'read_only_snapshot': str(BASE),
    'input_sha256': {rel: sha256((BASE / rel).read_bytes()).hexdigest()
                     for rel in [SOURCE_REL, B_REL, *DATA['input_sha256']]},
    'claims_not_proved_by_this_audit': [
        'Arbitrary-size four-spoke-omission Omega lemma and q-core exclusions',
        'Gallai tree / uniform leaf block palette theorem or planar topology',
        'Disk, target Sigma, Sigma-criticality, or realizability of fixed controls',
        'All mixed22 sources excluded, epsilon>=3, general exits, K_infinity=K_at_most_5',
        'Any new Lean theorem or short/long original graph relation equivalence',
    ],
    'targets': [],
    'canonical_rotation_root_swap_non_covariance': [],
    'complete_source_D5_mask_images': {},
    'examples': {},
}
for rel, digest in DATA['input_sha256'].items():
    assert sha256((BASE / rel).read_bytes()).hexdigest() == digest
    COUNTS['declared_input_hashes_checked'] += 1

# Independently regenerate all seven equality patterns; names are checked from
# their cross-side equalities, rather than accepting the producer list.
parts = {normalize(t) for t in product(range(4), repeat=4)
         if t[0] != t[1] and t[2] != t[3]}
named_parts = {}
for p in parts:
    shared = [(i, j - 2) for i in range(2) for j in range(2, 4) if p[i] == p[j]]
    if not shared:
        name = 'D4'
    elif len(shared) == 1:
        name = f'S{shared[0][0]}{shared[0][1]}'
    else:
        name = 'Pstraight' if shared == [(0, 0), (1, 1)] else 'Pcross'
    named_parts[name] = p
identity_items = DATA['contact_identity_table']
assert unique([x['identity'] for x in identity_items]) == set(named_parts)
for item in identity_items:
    p = named_parts[item['identity']]
    assert tuple(item['original_vertex_partition']) == p
    assert item['original_ordered_roles'] == ROLES
    assert item['same_side_contacts_distinct'] is True
    classes = [[ROLES[i] for i, c in enumerate(p) if c == k] for k in sorted(set(p))]
    assert item['original_vertex_classes'] == classes
    assert item['distinct_original_contact_vertices'] == len(set(p))
    shared = [[ROLES[i], ROLES[j]] for i in range(2) for j in range(2, 4) if p[i] == p[j]]
    assert item['cross_shared_pairs'] == shared
    for side in ('a', 'b'):
        k = item[f'original_K_after_{side}_spoke_omission']
        assert k['all_three_contacts_distinct'] is True
        assert k[f'original_{side}_degree_in_K'] == 2
        assert k[f'original_{side}_is_leaf'] is False
    COUNTS['independently_generated_contact_identities'] += 1

# All 32 subsets of four original spokes plus whole C: degree arithmetic only.
# The exclusion statuses use the paper dependencies and are not certified as
# arbitrary-size source exclusions by this finite table check.
expected_core = {}
factors = ['a:s0', 'a:s1', 'b:s0', 'b:s1', 'original:C']
for omitted in powerset(factors):
    COUNTS['original_factor_subsets_recomputed'] += 1
    da = 5 - sum(s.startswith('a:') for s in omitted) - 2 * ('original:C' in omitted)
    db = 5 - sum(s.startswith('b:') for s in omitted) - 2 * ('original:C' in omitted)
    if min(da, db) >= 4:
        status = ('original_G_itself' if not omitted else
                  'excluded_original_single_spoke_q_core' if len(omitted) == 1 else
                  'excluded_original_double_spoke_4_4_q_core')
        expected_core[frozenset(omitted)] = ([da, db], status)
core = DATA['original_omission_q_core_identity']
stored_cores = core['all_degree_admissible_q_core_identities']
for item in stored_cores:
    unique(item['omitted_original_factors'])
keys = [frozenset(x['omitted_original_factors']) for x in stored_cores]
assert unique(keys) == set(expected_core) and len(keys) == 9
for item, key in zip(stored_cores, keys, strict=True):
    assert (item['original_root_degrees'], item['status']) == expected_core[key]
assert core['all_original_factor_subsets_checked'] == 32
assert core['original_G_minus_C_root_degrees'] == [3, 3]
COUNTS['degree_admissible_omission_identities_checked'] = len(keys)

# Original source-filtered named domains, all carried source fields, exclusions,
# residual arrays, legal transported rotations, row/root-pair and complete masks.
rotation_cache = {}
for sigma in (933, 941):
    st = next(t for t in SOURCE['targets'] if t['source_sigma'] == sigma)
    all_source = st['named_spoke_skeletons']['records']
    selected = {i: r for i, r in enumerate(all_source)
                if r['status'] == 'necessary_skeleton_only'
                and list(map(len, r['original_spoke_supports'])) == [2, 2]}
    target = next(t for t in DATA['targets'] if t['source_sigma'] == sigma)
    frames = target['original_named_frames']
    indices = [f['inherited_named_skeleton_index'] for f in frames]
    assert unique(indices) == set(selected)
    assert len(indices) == (47 if sigma == 933 else 75)
    by_pairs = {tuple(map(tuple, r['original_spoke_supports'])): i for i, r in selected.items()}
    assert len(by_pairs) == len(selected)
    partitions = Counter()
    partition_indices = {s: [] for s in ('excluded_by_original_spoke_omission_all_rows',
        'excluded_by_original_sealed_triangle_three_hubs',
        'retained_necessary_identity_not_source_realization')}
    mask_images = Counter()
    for obj in walk(target):
        if 'inherited_named_skeleton_index' not in obj:
            continue
        i = obj['inherited_named_skeleton_index']
        assert i in selected and obj['source_sigma'] == sigma
        COUNTS['stage_source_sigma_fields_checked'] += 1
        src = selected[i]
        for bkey, skey in [('original_root_order', 'root_order'),
                          ('original_spoke_supports', 'original_spoke_supports'),
                          ('original_root_and_boundary_edges', 'retained_source_edges'),
                          ('original_inherited_apex_rotation', 'apex_rotation')]:
            assert obj[bkey] == src[skey], (sigma, i, bkey)
            COUNTS['stage_source_fields_checked'] += 1
        COUNTS['all_carried_original_identity_occurrences_checked'] += 1
    for f in frames:
        i = f['inherited_named_skeleton_index']
        src = selected[i]
        a, b = src['root_order']
        sa, sb = src['original_spoke_supports']
        es = edges(src['retained_source_edges'])
        assert es == FRAME | {edge(a, b)} | {edge(a, h) for h in sa} | {edge(b, h) for h in sb}
        apex = src['boundary_apex']
        augmented = edges(src['augmented_edges'])
        assert augmented == es | {edge(apex, h) for h in B}
        rotation = dict(enumerate(src['apex_rotation']))
        source_faces = rotation_faces(rotation, augmented)
        disk_rotation = {v: [w for w in ring if w != apex] for v, ring in rotation.items() if v != apex}
        disk_faces = rotation_faces(disk_rotation, es)
        assert sum(len(g) == 5 and set(g) == B for g in disk_faces) == 1
        COUNTS['independently_filtered_source_frames'] += 1
        COUNTS['source_augmented_and_disk_rotations_checked'] += 1
        assert f['all_seven_labelled_contact_identities_retained'] is True
        roots = f['original_G_minus_C_complete_root_relations']
        assert len(roots) == 10 and unique([tuple(r['row']) for r in roots]) == set(ROWS)
        for r in roots:
            row = tuple(r['row'])
            direct = solve(B | {a, b}, es, row, [a, b])
            assert direct and unique([tuple(p) for p in r['root_pairs']]) == direct
            COUNTS['source_G_minus_C_complete_root_relations'] += 1
        redundant = []
        for side, pair in enumerate((sa, sb)):
            for ri, row in enumerate(ROWS):
                if not (sigma >> ri & 1) and row[pair[0]] == row[pair[1]]:
                    redundant.append(dict(original_root=[a, b][side],
                        omitted_original_spoke=[[a, b][side], pair[0]],
                        retained_same_color_original_spoke=[[a, b][side], pair[1]],
                        original_row_index=ri, original_literal_row=list(row)))
        assert f['redundant_original_spoke_rejected_row_witnesses'] == redundant
        COUNTS['redundant_original_spoke_row_witnesses'] += len(redundant)
        if redundant:
            expected_status = 'excluded_by_original_spoke_omission_all_rows'
            assert 'fixed_original_skeleton_rotation_audit' not in f
        else:
            assert edge(*sa) in FRAME and edge(*sb) in FRAME
            key = (tuple(sa), tuple(sb))
            if key not in rotation_cache:
                rotation_cache[key] = exhaustive_disk_rotations(es)
            assignments, direct_rotations = rotation_cache[key]
            audit = f['fixed_original_skeleton_rotation_audit']
            assert audit['rotation_assignments_checked'] == assignments
            carried = audit['disk_rotations']
            stored_keys = []
            mixed_faces = None
            for rr in carried:
                rot = {x['vertex']: x['ring'] for x in rr['rotation']}
                fs = rotation_faces(rot, es)
                outer = rr['original_outer_boundary']
                assert outer in fs and len(outer) == 5 and set(outer) == B
                inner = [g for g in fs if g != outer]
                assert sorted(inner) == rr['all_original_inner_faces']
                common = sorted(g for g in inner if {a, b} <= set(g))
                assert common == rr['mixed_capable_original_faces']
                assert len(common) == 2
                face_sets = {frozenset(g) for g in common}
                if mixed_faces is None:
                    mixed_faces = common
                else:
                    assert face_sets == {frozenset(g) for g in mixed_faces}
                stored_keys.append(rotation_key(rot))
                COUNTS['all_carried_exhaustive_disk_rotations_checked'] += 1
            assert unique(stored_keys) == direct_rotations
            triangles = [g for g in mixed_faces if len(g) == 3]
            remaining_faces = [g for g in mixed_faces if len(g) != 3]
            assert triangles == f['excluded_sealed_triangle_C_faces']
            shared = len(set(sa) & set(sb))
            expected_status = ('excluded_by_original_sealed_triangle_three_hubs' if shared == 2 else
                               'retained_necessary_identity_not_source_realization')
            if shared == 2:
                assert len(triangles) == 2 and not remaining_faces
            else:
                assert sorted(len(set(g) & B) for g in remaining_faces) == ([4] if shared else [2, 3])
            necessities = f['retained_original_C_face_necessities']
            assert unique([tuple(n['original_face']) for n in necessities]) == {tuple(g) for g in remaining_faces}
            for n in necessities:
                face = n['original_face']
                envelope = sorted(B & set(face))
                assert n['exact_actual_support_envelope'] == envelope
                rejected = [(ri, row) for ri, row in enumerate(ROWS) if not (sigma >> ri & 1)]
                rs = n['rejected_rows_with_complete_original_root_pairs']
                assert unique([r['row_index'] for r in rs]) == {ri for ri, row in rejected}
                rejected_pairs = {}
                for r in rs:
                    ri, row = r['row_index'], tuple(r['row'])
                    assert row == ROWS[ri] and not (sigma >> ri & 1)
                    direct = solve(B | {a, b}, es, row, [a, b])
                    assert unique([tuple(p) for p in r['original_G_minus_C_root_pairs']]) == direct
                    rejected_pairs[ri] = direct
                    COUNTS['face_rejected_complete_root_relations'] += 1
                owners_table = n['per_original_vertex_attachment_necessities']
                expected_roles = {'none': (), 'a_only': (0,), 'b_only': (1,), 'shared_a_b': (0, 1)}
                assert unique([x['original_vertex_role'] for x in owners_table]) == set(expected_roles)
                lower = {}
                for t in owners_table:
                    owners = expected_roles[t['original_vertex_role']]
                    assert t['fixed_root_owners'] == list(owners)
                    permitted = []
                    for attachments in powerset(envelope):
                        COUNTS['actual_attachment_candidate_subsets_checked'] += 1
                        if 4 - len(attachments) - len(owners) < 1:
                            continue
                        if all(len(set([row[h] for h in attachments] + [p[j] for j in owners]))
                               == len(attachments) + len(owners)
                               for ri, row in rejected for p in rejected_pairs[ri]):
                            permitted.append(attachments)
                    assert unique([tuple(z) for z in t['permissible_actual_boundary_attachment_subsets']]) == set(permitted)
                    entries = t['internal_degree_for_subset']
                    assert unique([tuple(x['actual_attachments']) for x in entries]) == set(permitted)
                    for x in entries:
                        assert x['required_original_C_degree'] == 4 - len(x['actual_attachments']) - len(owners)
                    lower[t['original_vertex_role']] = min(4 - len(z) - len(owners) for z in permitted)
                    COUNTS['complete_actual_attachment_owner_tables_checked'] += 1
                    COUNTS['permitted_actual_attachment_subsets_checked'] += len(permitted)
                    if sigma == 933 and sa == [0, 4] and sb == [1, 2] and owners == (0, 1) and (4,) in permitted:
                        RESULT['examples']['shared_contact_leaf_attachment'] = {
                            'source_sigma': sigma, 'inherited_named_skeleton_index': i,
                            'original_spoke_supports': [sa, sb], 'original_face': face,
                            'actual_boundary_attachment': [4], 'required_original_C_degree': 1}
                assert n['necessary_minimum_C_degree_by_original_role'] == lower
                assert n['necessary_table_is_not_source_realizability'] is True
                COUNTS['retained_original_face_necessities_checked'] += 1
        assert f['status'] == expected_status
        partitions[expected_status] += 1
        partition_indices[expected_status].append(i)
        swap = lambda v: b if v == a else a if v == b else v
        swapped_augmented = {edge(swap(v), swap(w)) for v, w in augmented}
        transported_rot = renamed_rotation(rotation, swap)
        transported_faces = rotation_faces(transported_rot, swapped_augmented)
        assert {frozenset(map(swap, g)) for g in source_faces} == {frozenset(g) for g in transported_faces}
        partner_i = by_pairs[(tuple(sb), tuple(sa))]
        partner = selected[partner_i]
        canonical_faces = rotation_faces(dict(enumerate(partner['apex_rotation'])), edges(partner['augmented_edges']))
        canonical_equal = {frozenset(g) for g in canonical_faces} == {frozenset(g) for g in transported_faces}
        if not canonical_equal:
            RESULT['canonical_rotation_root_swap_non_covariance'].append({
                'source_sigma': sigma, 'inherited_named_skeleton_index': i,
                'partner_index': partner_i, 'original_spoke_supports': [sa, sb],
                'scope': 'Transported original rotation is legal; independently chosen canonical rotation need not equal it.'})
        COUNTS['source_root_swap_transported_rotations_checked'] += 1
        for sign, shift in product((-1, 1), range(5)):
            move = [(sign * h + shift) % 5 for h in range(5)]
            rename = lambda v: move[v] if v in B else v
            mes = {edge(rename(v), rename(w)) for v, w in augmented}
            mrot = renamed_rotation(rotation, rename)
            mfaces = rotation_faces(mrot, mes)
            assert {frozenset(map(rename, g)) for g in source_faces} == {frozenset(g) for g in mfaces}
            COUNTS['D5_transported_original_rotations_checked'] += 1
            row_permutation = []
            for ri, row in enumerate(ROWS):
                moved_row, cp = transport(row, move)
                ti = ROWS.index(moved_row)
                row_permutation.append(ti)
                old_pairs = solve(B | {a, b}, es, row, [a, b])
                disk_moved_es = {edge(rename(v), rename(w)) for v, w in es}
                new_pairs = solve(B | {a, b}, disk_moved_es, moved_row, [a, b])
                assert new_pairs == {(cp[A], cp[D]) for A, D in old_pairs}
                COUNTS['D5_complete_root_pair_relations_checked'] += 1
            assert len(unique(row_permutation)) == 10
            moved_sigma = sum(1 << ti for ri, ti in enumerate(row_permutation) if sigma >> ri & 1)
            mask_images[moved_sigma] += 1
            assert all(bool(moved_sigma >> ti & 1) == bool(sigma >> ri & 1)
                       for ri, ti in enumerate(row_permutation))
            COUNTS['D5_complete_source_masks_checked'] += 1
    residual = target['retained_named_skeleton_indices']
    assert unique(residual) == set(partition_indices['retained_necessary_identity_not_source_realization'])
    assert dict(partitions) == target['counts']
    assert partitions == Counter(excluded_by_original_spoke_omission_all_rows=22 if sigma == 933 else 50,
        excluded_by_original_sealed_triangle_three_hubs=5,
        retained_necessary_identity_not_source_realization=20)
    assert all(next(x for x in frames if x['inherited_named_skeleton_index'] == by_pairs[(tuple(f['original_spoke_supports'][1]), tuple(f['original_spoke_supports'][0]))])['status'] == f['status'] for f in frames)
    RESULT['targets'].append({'source_sigma': sigma, 'source_filtered_domain_size': len(selected),
        'adjacent_pair_domain_size': 25, 'counts': dict(partitions), 'exact_stage_indices': partition_indices,
        'all_exclusion_and_residual_arrays_unique': True,
        'all_stage_source_fields_equal_source': True,
        'retained_shared_pair_indices': [f['inherited_named_skeleton_index'] for f in frames
            if f['status'].startswith('retained') and len(set(f['original_spoke_supports'][0]) & set(f['original_spoke_supports'][1])) == 1],
        'retained_disjoint_pair_indices': [f['inherited_named_skeleton_index'] for f in frames
            if f['status'].startswith('retained') and not set(f['original_spoke_supports'][0]) & set(f['original_spoke_supports'][1])]})
    RESULT['complete_source_D5_mask_images'][str(sigma)] = dict(sorted(mask_images.items()))
COUNTS['unique_adjacent_skeletons_independently_rotation_enumerated'] = len(rotation_cache)
COUNTS['unique_adjacent_rotation_assignments_independently_enumerated'] = sum(n for n, rs in rotation_cache.values())
COUNTS['unique_adjacent_disk_rotations_independently_enumerated'] = sum(len(rs) for n, rs in rotation_cache.values())
assert len(rotation_cache) == 25
assert COUNTS['unique_adjacent_rotation_assignments_independently_enumerated'] == 2320
assert COUNTS['unique_adjacent_disk_rotations_independently_enumerated'] == 60
assert len(RESULT['canonical_rotation_root_swap_non_covariance']) == 16

# The local leaf-owner table only checks a missing-color signature. The uniform
# leaf palette and triangle consequences remain paper/theorem dependencies.
signatures = DATA['private_leaf_original_owner_identity_controls']['owner_type_signatures']
assert unique([tuple(x['original_owners']) for x in signatures]) == {(), (0,), (1,), (0, 1)}
for x in signatures:
    owners = x['original_owners']
    # Fix missing=3, h_a=0, h_b=1; boundary colors exclude missing.
    code = [int(3 not in {p[j] for j in owners}) for p in ((3, 1), (0, 3))]
    assert x['missing_color_membership_in_two_exact_lists'] == code
    COUNTS['local_leaf_owner_missing_color_signatures_checked'] += 1
assert len({tuple(x['missing_color_membership_in_two_exact_lists']) for x in signatures}) == 4

# Conditional K5 extraction controls: original identities, all original edges,
# connected disjoint bags and ten literal interbag edge witnesses.
minors = DATA['conditional_marked_original_K5_minor_controls']
assert unique([(x['identity'], tuple(x['omitted_original_a_spoke'])) for x in minors]) == {
    (name, (5, h)) for name in named_parts for h in (0, 1)}
for x in minors:
    a, b = x['original_a'], x['original_b']
    contacts = x['original_ordered_C_contacts']
    assert normalize(contacts) == named_parts[x['identity']]
    gs, ms = edges(x['original_G_edges']), edges(x['original_M_edges'])
    omitted = edge(*x['omitted_original_a_spoke'])
    assert ms == gs - {omitted}
    assert all(sum(r in e for e in gs) == 5 for r in (a, b))
    cv = set(x['original_C_vertices'])
    assert cv == {v for e in gs for v in e} - B - {a, b}
    assert connected(cv, gs)
    triangle = x['actual_active_triangle']
    assert triangle == [a, *contacts[:2]]
    assert all(edge(v, w) in ms for v, w in combinations(triangle, 2))
    arms = x['actual_original_contact_arms']
    assert arms[0] == [a] and len(arms) == 3
    assert {arm[-1] for arm in arms} == {a, *contacts[2:]}
    for arm in arms:
        assert len(unique(arm)) == len(arm)
        assert (len(arm) - 1) % 2 == 0
        assert all(edge(v, w) in ms for v, w in zip(arm, arm[1:]))
        COUNTS['conditional_K5_original_arms_checked'] += 1
    for path in x['actual_boundary_tethers']:
        assert all(edge(v, w) in ms for v, w in zip(path, path[1:]))
        COUNTS['conditional_K5_actual_tethers_checked'] += 1
    bags = x['five_original_connected_branch_sets']
    assert len(bags) == 5 and all(connected(g, ms) for g in bags)
    assert sum(map(len, bags)) == len({v for g in bags for v in g})
    ws = x['ten_original_edge_witnesses']
    assert unique([tuple(w['branch_set_pair']) for w in ws]) == set(combinations(range(5), 2))
    for w in ws:
        i, j = w['branch_set_pair']
        v, z = w['original_edge']
        assert edge(v, z) in ms and ((v in bags[i] and z in bags[j]) or (z in bags[i] and v in bags[j]))
        COUNTS['conditional_K5_original_interbag_edges_checked'] += 1
    assert x['missing_unused_degree_edges_not_completed'] is True
    COUNTS['conditional_K5_controls_checked'] += 1

# Twenty-eight serialized full-degree original graphs. Rebuild components from
# graph edges and derive actual attachments/owners, then check every stored
# relation and witness against independent enumeration of those same edges.
controls = DATA['fixed_complete_degree_original_relation_controls']
records = controls['records']
assert unique([r['control_index'] for r in records]) == set(range(28))
expected_graph_keys = {(name, longer, swapped) for name in named_parts for longer, swapped in product((False, True), repeat=2)}
assert unique([(r['identity'], r['longer_original_component'], r['root_swapped']) for r in records]) == expected_graph_keys
direct_cache = {}
for rec in records:
    a, b = rec['a'], rec['b']
    assert rec['original_root_order'] == [a, b]
    assert [a, b] == ([6, 5] if rec['root_swapped'] else [5, 6])
    contacts = rec['ordered_original_contacts']
    assert normalize(contacts) == named_parts[rec['identity']]
    assert contacts[0] != contacts[1] and contacts[2] != contacts[3]
    c = rec['original_components']['C']
    cv = set(c['vertices'])
    assert cv.isdisjoint(B | {a, b})
    assert unique(c['vertices']) == cv and set(contacts) <= cv
    original = edges(rec['original_edges'])
    vertices = {v for e in original for v in e}
    assert vertices == B | {a, b} | cv
    assert rec['original_vertex_order'] == sorted(vertices)
    assert rec['boundary_cyclic_order'] == sorted(B)
    assert edges(rec['literal_frame_edges']) == FRAME
    assert {e for e in original if set(e) <= B} == FRAME
    assert c['ordered_contacts'] == contacts
    ce = {e for e in original if set(e) & cv and not set(e) & {a, b}}
    internal = {e for e in ce if set(e) <= cv}
    assert internal == edges(c['internal_edges']) and ce == edges(c['edges'])
    assert connected(cv, internal)
    actual_attachments = {v: sorted(w if z == v else z for z, w in original if v in (z, w) and set((z, w)) & B) for v in cv}
    assert {int(v): hs for v, hs in c['actual_attachments'].items()} == actual_attachments
    assert c['actual_support'] == sorted({h for hs in actual_attachments.values() for h in hs})
    owner_edges = {e for e in original if set(e) & cv and set(e) & {a, b}}
    expected_owner_edges = {edge(r, v) for r, v in zip([a, a, b, b], contacts)}
    assert owner_edges == expected_owner_edges
    assert c['owners_by_ordered_role'] == [a, a, b, b]
    assert edges(c['original_root_contact_edges']) == owner_edges
    spokes = rec['original_spoke_supports']
    expected_spokes = [[0, 1], [2, 3]]
    assert spokes == expected_spokes
    spoke_edges = {edge(r, h) for r, hs in zip((a, b), spokes) for h in hs}
    assert original == FRAME | ce | owner_edges | spoke_edges | {edge(a, b)}
    degrees = {v: sum(v in e for e in original) for v in vertices}
    assert degrees == {int(v): deg for v, deg in rec['original_complete_degrees'].items()}
    assert all(degrees[v] == (5 if v in (a, b) else 4) for v in vertices - B)
    COUNTS['fixed_complete_degree_original_graphs_checked'] += 1
    COUNTS['graphs_with_cross_side_original_contact_aliasing'] += len(set(contacts)) < 4
    rows = rec['rows']
    assert unique([r['row_index'] for r in rows]) == set(range(10))
    for row in rows:
        ri, beta = row['row_index'], tuple(row['literal_boundary'])
        assert beta == ROWS[ri]
        corder = row['original_C_vertex_order']
        assert corder == sorted(B | cv)
        rc = stored_relation(row['complete_original_R_C'], corder, FRAME | ce, beta, contacts, 'original_R_C_witnesses_checked')
        direct_rc = solve(B | cv, FRAME | ce, beta, contacts)
        assert rc == direct_rc
        COUNTS['independent_complete_four_contact_relations'] += 1
        if len(set(contacts)) < 4:
            assert all(t[i] == t[j] for t in rc for i, j in combinations(range(4), 2) if contacts[i] == contacts[j])
            COUNTS['shared_contact_component_tuples_checked'] += len(rc)
        expected_names = {'G', 'G-C'} | {f'G-{role}{h}' for role, hs in zip(('a', 'b'), spokes) for h in hs}
        variants = row['variants']
        assert unique([v['name'] for v in variants]) == expected_names
        byname = {v['name']: v for v in variants}
        for v in variants:
            omit_c = v['original_C_omitted']
            omitted = v['omitted_original_edge']
            omit_edge = None if omitted is None else edge(*omitted)
            assert (v['name'] == 'G-C') == omit_c
            expected = original - ({omit_edge} if omit_edge is not None else set())
            if omit_c:
                expected = {e for e in expected if not set(e) & cv}
            if v['name'] in ('G', 'G-C'):
                assert omit_edge is None
            else:
                assert omit_edge in spoke_edges
            assert edges(v['actual_edges']) == expected
            active = B | {a, b} | (set() if omit_c else cv)
            order = v['original_vertex_order']
            ports = [a, b] + ([] if omit_c else contacts)
            assert order == sorted(active) and v['original_port_order'] == ports
            assert v['named_role_order'] == ['a', 'b'] + ([] if omit_c else ROLES)
            stored = stored_relation(v['complete_joint'], order, expected, beta, ports, 'complete_joint_witnesses_checked')
            direct = solve(active, expected, beta, ports)
            assert direct == stored, (rec['control_index'], ri, v['name'])
            direct_cache[(rec['control_index'], ri, v['name'])] = direct
            # Assemble a second independent relation from the complete R_C and
            # original root/spoke guards, never from marginal projections.
            joined = set()
            for A, D in product(range(4), repeat=2):
                if A == D or any(A == beta[h] for h in spokes[0] if edge(a, h) != omit_edge) or any(D == beta[h] for h in spokes[1] if edge(b, h) != omit_edge):
                    continue
                for t in ([()] if omit_c else direct_rc):
                    if omit_c or (A not in t[:2] and D not in t[2:]):
                        joined.add((A, D, *t))
            assert joined == direct
            COUNTS['independent_complete_whole_graph_joints'] += 1
            COUNTS['independent_complete_relation_guard_joins'] += 1
            if omit_c:
                assert direct and all(sum(r in e for e in expected) == 3 for r in (a, b))
                COUNTS['fixed_G_minus_C_Omega_row_controls'] += 1
            elif len(set(contacts)) < 4:
                assert all(t[2 + i] == t[2 + j] for t in direct for i, j in combinations(range(4), 2) if contacts[i] == contacts[j])
                COUNTS['shared_contact_complete_joint_tuples_checked'] += len(direct)
            fs = v['pinned_a_b_fibres']
            assert unique([(f['a_color'], f['b_color']) for f in fs]) == set(product(range(4), repeat=2))
            for f in fs:
                A, D = f['a_color'], f['b_color']
                pinned_direct = solve(active, expected, beta, ports, {a: A, b: D})
                actual_fibre = {t[2:] for t in pinned_direct}
                assert unique([tuple(t) for t in f['complete_C_role_fibre']]) == actual_fibre
                assert actual_fibre == {t[2:] for t in direct if t[:2] == (A, D)}
                COUNTS['independent_pinned_root_pair_fibres'] += 1
                COUNTS['independent_empty_pinned_root_pair_fibres'] += not actual_fibre
            if omitted is not None:
                COUNTS['fixed_original_spoke_omission_row_controls'] += 1
                COUNTS['fixed_original_spoke_omission_empty_rows'] += not direct
                r = next(z for z in omitted if z in (a, b))
                h = next(z for z in omitted if z in B)
                pos = (a, b).index(r)
                restored = {t for t in direct if t[pos] != beta[h]}
                assert restored == {tuple(x['tuple']) for x in byname['G']['complete_joint']}
                COUNTS['exact_original_spoke_restorations'] += 1
                carrier = v['original_three_contact_carrier']
                retained = b if r == a else a
                other_contacts = contacts[2:] if r == a else contacts[:2]
                kports = [r, *other_contacts]
                assert len(set(kports)) == 3
                kes = {e for e in expected if retained not in e}
                kvs = B | cv | {r}
                assert edges(carrier['original_edges']) == kes
                assert carrier['ordered_original_contacts'] == kports
                assert carrier['decreased_root'] == r and carrier['deleted_degree_five_root'] == retained
                assert carrier['original_vertex_order'] == sorted(kvs)
                assert sum(r in e and set(e) <= cv | {r} for e in kes) == 2
                assert carrier['marked_root_internal_degree'] == 2 and carrier['marked_root_is_leaf'] is False
                assert edges(carrier['original_root_contact_edges']) == {edge(retained, z) for z in kports}
                assert {int(z): deg for z, deg in carrier['complete_degrees_after_original_spoke_omission'].items()} == {z: sum(z in e for e in expected) for z in (a, b)}
                stored_k = stored_relation(carrier['complete_relation'], sorted(kvs), kes, beta, kports, 'three_contact_carrier_witnesses_checked')
                direct_k = solve(kvs, kes, beta, kports)
                assert stored_k == direct_k
                COUNTS['independent_complete_three_contact_carrier_relations'] += 1
        color_controls = row['global_S4_color_controls']
        assert unique([tuple(c['global_color_permutation']) for c in color_controls]) == set(permutations(range(4)))
        for cc in color_controls:
            cp = cc['global_color_permutation']
            mbeta = tuple(cp[c] for c in beta)
            assert tuple(cc['transported_literal_boundary']) == mbeta
            moved_rc = solve(B | cv, FRAME | ce, mbeta, contacts)
            assert moved_rc == {tuple(cp[c] for c in t) for t in rc}
            assert cc['independently_recomputed_complete_C_relation_size'] == len(moved_rc)
            COUNTS['independently_recomputed_global_S4_C_relations'] += 1
            for v in variants:
                for item in v['complete_joint']:
                    witness(v['original_vertex_order'], [cp[c] for c in item['coloring']], edges(v['actual_edges']), mbeta, v['original_port_order'], [cp[c] for c in item['tuple']])
                    COUNTS['global_S4_individual_joint_witnesses_checked'] += 1
                COUNTS['global_S4_variant_controls_checked'] += 1
        COUNTS['fixed_graph_literal_rows_checked'] += 1

# Literal root-swap graph isomorphism and complete relations/fibres: transport
# physical vertices and owners simultaneously while retaining the role frame.
graph_by_key = {(r['identity'], r['longer_original_component'], r['root_swapped']): r for r in records}
for (name, longer, swapped), rec in graph_by_key.items():
    if swapped:
        continue
    partner = graph_by_key[(name, longer, True)]
    rename = lambda v: 11 - v if v in (5, 6) else v
    assert {edge(rename(v), rename(w)) for v, w in edges(rec['original_edges'])} == edges(partner['original_edges'])
    assert rec['original_components']['C']['actual_attachments'] == partner['original_components']['C']['actual_attachments']
    assert [rename(z) for z in rec['original_components']['C']['owners_by_ordered_role']] == partner['original_components']['C']['owners_by_ordered_role']
    for left, right in zip(rec['rows'], partner['rows'], strict=True):
        assert left['literal_boundary'] == right['literal_boundary']
        for lv, rv in zip(left['variants'], right['variants'], strict=True):
            assert lv['name'] == rv['name']
            assert {edge(rename(v), rename(w)) for v, w in edges(lv['actual_edges'])} == edges(rv['actual_edges'])
            assert [rename(z) for z in lv['original_port_order']] == rv['original_port_order']
            assert direct_cache[(rec['control_index'], left['row_index'], lv['name'])] == direct_cache[(partner['control_index'], right['row_index'], rv['name'])]
            assert lv['pinned_a_b_fibres'] == rv['pinned_a_b_fibres']
            COUNTS['literal_whole_graph_root_swap_relations_and_fibres_checked'] += 1

# Every witness in the explicit marginal negative control is a separate stored
# occurrence, checked again against its actual component graph and full fibre.
marginal = controls['actual_marginal_false_positive']
rec = records[marginal['control_index']]
row = rec['rows'][marginal['row_index']]
contacts = rec['ordered_original_contacts']
beta = tuple(marginal['literal_boundary'])
assert beta == tuple(row['literal_boundary'])
assert marginal['identity'] == rec['identity'] and marginal['original_port_order'] == contacts
c = rec['original_components']['C']
rc = stored_relation(marginal['complete_original_C_tuples'], row['original_C_vertex_order'], FRAME | edges(c['edges']), beta, contacts, 'marginal_negative_control_witnesses_checked')
assert rc == {tuple(t['tuple']) for t in row['complete_original_R_C']}
margs = [sorted({t[i] for t in rc}) for i in range(4)]
assert margs == marginal['independent_role_marginals']
A, D = marginal['original_root_colors']
assert A != D and all(A != beta[h] for h in rec['original_spoke_supports'][0]) and all(D != beta[h] for h in rec['original_spoke_supports'][1])
assert all(set(m) - {A if i < 2 else D} for i, m in enumerate(margs))
assert not {t for t in rc if A not in t[:2] and D not in t[2:]}
assert marginal['guarded_original_C_fibre'] == []
RESULT['examples']['marginal_false_positive'] = {
    k: marginal[k] for k in ('control_index', 'identity', 'row_index', 'literal_boundary', 'original_root_colors', 'original_port_order', 'independent_role_marginals')}

assert COUNTS['independent_complete_whole_graph_joints'] == 1680
assert COUNTS['independent_pinned_root_pair_fibres'] == 26880
assert COUNTS['independent_empty_pinned_root_pair_fibres'] == 21008
assert COUNTS['independent_complete_three_contact_carrier_relations'] == 1120
assert COUNTS['original_R_C_witnesses_checked'] == 4200
assert COUNTS['complete_joint_witnesses_checked'] == 23364
assert COUNTS['three_contact_carrier_witnesses_checked'] == 17608
assert COUNTS['global_S4_variant_controls_checked'] == 40320
assert COUNTS['independently_recomputed_global_S4_C_relations'] == 6720
assert COUNTS['literal_whole_graph_root_swap_relations_and_fibres_checked'] == 840
assert RESULT['examples']['shared_contact_leaf_attachment']['required_original_C_degree'] == 1
serialized_witnesses = sum('coloring' in obj and 'tuple' in obj for obj in walk(DATA))
checked_witnesses = sum(COUNTS[k] for k in ('original_R_C_witnesses_checked',
    'complete_joint_witnesses_checked', 'three_contact_carrier_witnesses_checked',
    'marginal_negative_control_witnesses_checked'))
assert serialized_witnesses == checked_witnesses == 45178
COUNTS['all_serialized_tuple_coloring_witness_occurrences_checked'] = checked_witnesses
assert COUNTS['fixed_original_spoke_omission_empty_rows'] == 48
control_summary = controls['summary']
expected_control_summary = {
    'complete_degree_original_graphs': 28, 'contact_identity_classes': 7,
    'independent_whole_graph_joins': 1680, 'independent_pinned_a_b_fibres': 26880,
    'independent_original_three_contact_carrier_joins': 1120,
    'exact_original_spoke_restorations': 1120, 'root_swap_variant_checks': 840,
    'global_S4_variant_witness_checks': 40320, 'independently_recomputed_S4_C_relations': 6720,
    'short_long_relation_equivalence_claimed': False,
    'fixed_controls_are_disk_source_realizations': False,
}
assert control_summary == expected_control_summary
assert DATA['summary']['complete_degree_control_summary'] == expected_control_summary
for key in ('all_mixed22_sources_excluded', 'source_realizability_claimed',
            'source_graph_catalogue_enumerated', 'unary_crosscut_used',
            'epsilon_three_proved', 'new_lean_theorem'):
    assert DATA['summary'][key] is False
RESULT['summary'] = {
    'new_scope': 'B mixed22 no-unary serialized identities/ledger and finite complete graph controls',
    'source_filtered_domains': [47, 75], 'spoke_redundancy_exclusions': [22, 50],
    'adjacent_pair_domains': [25, 25], 'sealed_equal_pair_exclusions': [5, 5],
    'retained_named_necessary_frames': [20, 20], 'retained_original_faces': 60,
    'contact_identities': 7, 'fixed_complete_degree_original_graphs': 28,
    'independent_complete_four_contact_relations': 280,
    'independent_complete_whole_graph_joints': 1680,
    'independent_pinned_root_pair_fibres': 26880,
    'independent_empty_pinned_root_pair_fibres': 21008,
    'independent_complete_three_contact_carrier_relations': 1120,
    'all_serialized_tuple_coloring_witness_occurrences_checked': 45178,
    'fixed_original_spoke_omission_empty_rows_without_source_hypotheses': 48,
    'arbitrary_size_spoke_Omega_or_q_core_theorem_independently_proved': False,
    'source_realizability_or_epsilon_three_claimed': False,
}
RESULT['counts'] = dict(sorted(COUNTS.items()))
RESULT['elapsed_seconds'] = round(time.monotonic() - START, 3)
RESULT['all_checks_passed'] = True
RESULT['producer_modules_imported'] = False
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'results.json').write_text(json.dumps(RESULT, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
print(json.dumps({'all_checks_passed': True, 'elapsed_seconds': RESULT['elapsed_seconds'],
                  'counts': RESULT['counts']}, sort_keys=True), flush=True)
