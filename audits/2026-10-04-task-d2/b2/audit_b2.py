#!/usr/bin/env python3
"""Independent successor B2 serialized identity/relation/witness/minor audit.

Only standard library and the new audit-local independent_core are used.
No math producer enumerators, join helpers or validators are imported.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys
import time
sys.dont_write_bytecode = True
from independent_core import (B, U, FRAME, COUNTS, edge, edges, unique,
    normalize, powerset, connected, solve, witness, stored_relation,
    rotation_faces, renamed_rotation, transport, walk)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=Path('/tmp/math-task-d2-successor-v2'))
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent)
args = parser.parse_args()
BASE, OUT = args.repo.resolve(), args.output.resolve()
started = time.monotonic()
REL = 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face/observations.json'
PREV = 'artifacts/c5_excess_two_mixed_core_four_spoke_mixed22/observations.json'
DATA = json.loads((BASE / REL).read_text())
SOURCE = json.loads((BASE / PREV).read_text())
ROWS = [tuple(q) for q in DATA['pattern_order']]
assert ROWS == [tuple(q) for q in SOURCE['pattern_order']]
assert ROWS == sorted({normalize(q) for q in product(range(4), repeat=5)
    if all(q[h] != q[(h + 1) % 5] for h in B)})
RESULT = {'schema': 1, 'scope': __doc__, 'read_only_snapshot': str(BASE),
    'input_sha256': {rel: sha256((BASE / rel).read_bytes()).hexdigest()
                    for rel in [REL, PREV, *DATA['input_sha256']]},
    'selected_frames': [], 'examples': {},
    'claims_not_proved_by_this_audit': [
        'Arbitrary-size short-face K5 theorem, Gallai uniform lists, general leaf existence',
        'B spoke-omission Omega and q-core theorem or any new Lean theorem',
        'Disk, target Sigma, Sigma-criticality, or source realizability of controls',
        'Other original faces, all mixed22, epsilon>=3, general exits or K_infinity=K_at_most_5']}
for rel, digest in DATA['input_sha256'].items():
    assert sha256((BASE / rel).read_bytes()).hexdigest() == digest
    COUNTS['declared_input_hashes_checked'] += 1
assert DATA['original_relation_contract'] == SOURCE['original_relation_contract']
assert DATA['source_omission_and_q_core_conclusions'] == SOURCE['original_omission_q_core_identity']

parts = {normalize(t) for t in product(range(4), repeat=4) if t[0] != t[1] and t[2] != t[3]}
named_parts = {}
for p in parts:
    shared = [(i, j - 2) for i in range(2) for j in range(2, 4) if p[i] == p[j]]
    name = ('D4' if not shared else f'S{shared[0][0]}{shared[0][1]}' if len(shared) == 1 else
            'Pstraight' if shared == [(0, 0), (1, 1)] else 'Pcross')
    named_parts[name] = p
assert unique([x['identity'] for x in DATA['contact_identity_table']]) == set(named_parts)
for x in DATA['contact_identity_table']:
    p = named_parts[x['identity']]
    assert tuple(x['original_vertex_partition']) == p
    assert x['original_vertex_classes'] == [[['x0', 'x1', 'y0', 'y1'][i]
        for i, c in enumerate(p) if c == k] for k in sorted(set(p))]
    COUNTS['independently_generated_contact_identities'] += 1
assert DATA['contact_identity_table'] == SOURCE['contact_identity_table']

EXPECTED_ROLES = {'none': (), 'a_only': (0,), 'b_only': (1,), 'shared_a_b': (0, 1)}
FORCED = {'none': [1, 2], 'a_only': [1], 'b_only': [2], 'shared_a_b': []}
SKELETON = FRAME | {edge(5, 6)} | {edge(5, h) for h in (0, 1)} | {edge(6, h) for h in (2, 3)}
sf = DATA['selected_original_frames']
assert unique([(x['source_sigma'], x['named_source']) for x in sf]) == {(933, 'W933-101'), (941, 'W941-139')}
for x in sf:
    sigma = x['source_sigma']
    index = 101 if sigma == 933 else 139
    target = next(t for t in SOURCE['targets'] if t['source_sigma'] == sigma)
    source_frame = next(f for f in target['original_named_frames'] if f['inherited_named_skeleton_index'] == index)
    f = x['inherited_original_named_frame']
    assert f == source_frame
    assert f['source_sigma'] == sigma and f['original_spoke_supports'] == [[0, 1], [2, 3]]
    assert edges(f['original_root_and_boundary_edges']) == SKELETON
    face = x['selected_original_short_face']
    assert face in f['retained_original_C_face_necessities']
    assert face['exact_actual_support_envelope'] == [1, 2]
    assert set(face['original_face']) == {5, 1, 2, 6}
    assert all(edge(v, w) in SKELETON for v, w in zip(face['original_face'], face['original_face'][1:] + face['original_face'][:1]))
    assert unique(x['all_seven_original_contact_identities']) == set(named_parts)
    assert x['named_short_face_residuals'] == []
    assert x['short_face_status'] == 'excluded_by_arbitrary_size_original_K5_lemma'
    assert x['other_original_faces_status'] == 'retained_without_new_claim'
    roots = face['rejected_rows_with_complete_original_root_pairs']
    rejected = {ri for ri in range(10) if not (sigma >> ri & 1)}
    assert unique([r['row_index'] for r in roots]) == rejected
    rp = {}
    for r in roots:
        ri, beta = r['row_index'], tuple(r['row'])
        assert beta == ROWS[ri]
        pairs = solve(B | {5, 6}, SKELETON, beta, [5, 6])
        assert unique([tuple(p) for p in r['original_G_minus_C_root_pairs']]) == pairs
        rp[ri] = pairs
        COUNTS['selected_face_complete_rejected_root_relations'] += 1
    tables = face['per_original_vertex_attachment_necessities']
    assert unique([t['original_vertex_role'] for t in tables]) == set(EXPECTED_ROLES)
    for t in tables:
        role, owners = t['original_vertex_role'], EXPECTED_ROLES[t['original_vertex_role']]
        permitted = []
        for attachments in powerset([1, 2]):
            if 4 - len(attachments) - len(owners) < 1:
                continue
            if all(len(set([ROWS[ri][h] for h in attachments] + [p[j] for j in owners])) == len(attachments) + len(owners)
                   for ri in rejected for p in rp[ri]):
                permitted.append(attachments)
        assert unique([tuple(t) for t in t['permissible_actual_boundary_attachment_subsets']]) == set(permitted)
        assert max(map(len, permitted)) == 2 - len(owners)
        assert tuple(FORCED[role]) in permitted
        for item in t['internal_degree_for_subset']:
            assert item['required_original_C_degree'] == 4 - len(item['actual_attachments']) - len(owners)
        COUNTS['all_rejected_row_actual_attachment_owner_intersections'] += 1
    for rr in f['fixed_original_skeleton_rotation_audit']['disk_rotations']:
        rot = {r['vertex']: r['ring'] for r in rr['rotation']}
        fs = rotation_faces(rot, SKELETON)
        assert {frozenset(g) for g in rr['mixed_capable_original_faces']} == {frozenset(g) for g in fs if {5, 6} <= set(g)}
        assert any(set(g) == {5, 1, 2, 6} for g in fs)
        assert any(set(g) == {5, 0, 4, 3, 6} for g in fs)
        COUNTS['inherited_fixed_disk_rotations_checked'] += 1
        for sign, shift in product((-1, 1), range(5)):
            move = [(sign*h + shift) % 5 for h in B]
            rename = lambda v: move[v] if v in B else v
            ms = {edge(rename(v), rename(w)) for v, w in SKELETON}
            mf = rotation_faces(renamed_rotation(rot, rename), ms)
            assert {frozenset(map(rename, g)) for g in fs} == {frozenset(g) for g in mf}
            row_map = []
            for ri, row in enumerate(ROWS):
                moved, cp = transport(row, move)
                row_map.append(ROWS.index(moved))
                assert solve(B | {5, 6}, ms, moved, [5, 6]) == {(cp[A], cp[D]) for A, D in solve(B | {5, 6}, SKELETON, row, [5, 6])}
                COUNTS['D5_selected_frame_complete_root_relations_checked'] += 1
            assert len(unique(row_map)) == 10
            moved_sigma = sum(1 << ti for ri, ti in enumerate(row_map) if sigma >> ri & 1)
            assert all(bool(moved_sigma >> ti & 1) == bool(sigma >> ri & 1) for ri, ti in enumerate(row_map))
            COUNTS['D5_selected_frame_masks_and_rotations_checked'] += 1
    RESULT['selected_frames'].append({'named_source': x['named_source'], 'source_sigma': sigma,
        'inherited_named_skeleton_index': index, 'short_envelope': [1, 2],
        'long_envelope_retained': [0, 3, 4], 'serialized_short_face_residuals': 0,
        'full_original_frame_and_selected_face_equal_B_source': True})
    COUNTS['selected_original_frame_identities_checked'] += 1

# All four owner ledgers retain actual adjacent hubs and actual complementary
# exterior paths of the same skeleton. Eligible identities derive from aliases.
ledger = DATA['complete_leaf_owner_and_original_path_ledger']
assert unique([x['original_leaf_owner'] for x in ledger]) == set(EXPECTED_ROLES)
for x in ledger:
    role, owners = x['original_leaf_owner'], EXPECTED_ROLES[x['original_leaf_owner']]
    assert x['original_root_owners'] == list(owners)
    hubs = ([1, 2] if role == 'none' else [5, 1] if role == 'a_only' else [6, 2] if role == 'b_only' else [5, 6])
    assert x['actual_private_external_neighbors'] == hubs
    assert edge(*hubs) == tuple(x['actual_adjacent_hub_edge']) and edge(*hubs) in SKELETON
    path = x['actual_complementary_exterior_path']
    assert len(unique(path)) == len(path)
    assert set(path) == (B | {5, 6}) - set(hubs)
    assert all(edge(v, w) in SKELETON for v, w in zip(path, path[1:]))
    assert all(any(edge(h, v) in SKELETON for v in path) for h in hubs)
    eligible = set()
    for name, p in named_parts.items():
        counts = Counter(tuple(j for j in (0, 1) if any(p[i] == v for i in (2*j, 2*j+1))) for v in set(p))
        if not owners or counts[owners] >= 2:
            eligible.add(name)
    assert unique(x['possible_labelled_contact_identities']) == eligible
    assert x['missing_color_membership_signature'] == [int(0 not in owners), int(1 not in owners)]
    assert x['contact_leaf_is_triangle'] == bool(owners)
    COUNTS['complete_owner_hub_path_identity_ledgers_checked'] += 1

def reconstruct(rec, identity_key=None):
    a, b = rec['original_root_order']
    contacts = rec['ordered_original_contacts']
    if identity_key:
        assert normalize(contacts) == named_parts[rec[identity_key]]
    c = rec['original_components']['C']
    cv = unique(c['vertices'])
    assert cv.isdisjoint(B | {a, b}) and set(contacts) <= cv
    original = edges(rec['original_edges'])
    vertices = {v for e in original for v in e}
    assert vertices == B | {a, b} | cv
    assert rec['original_vertex_order'] == sorted(vertices)
    assert edges(rec['literal_frame_edges']) == FRAME
    assert {e for e in original if set(e) <= B} == FRAME
    ce = {e for e in original if set(e) & cv and not set(e) & {a, b}}
    internal = {e for e in ce if set(e) <= cv}
    assert edges(c['edges']) == ce and edges(c['internal_edges']) == internal
    assert connected(cv, internal) and c['ordered_contacts'] == contacts
    attachments = {v: sorted(w if z == v else z for z, w in original if v in (z, w) and set((z, w)) & B) for v in cv}
    assert {int(v): hs for v, hs in c['actual_attachments'].items()} == attachments
    assert c['actual_support'] == sorted({h for hs in attachments.values() for h in hs})
    assert set(c['actual_support']) <= {1, 2}
    owners = {v: sorted(r for r in (a, b) if edge(r, v) in original) for v in cv}
    assert {int(v): sorted(rs) for v, rs in c['actual_original_owners'].items()} == owners
    assert owners == {v: sorted(set(([a] if v in contacts[:2] else []) + ([b] if v in contacts[2:] else []))) for v in cv}
    owner_edges = {edge(r, v) for v, rs in owners.items() for r in rs}
    assert edges(c['original_root_contact_edges']) == owner_edges
    assert c['owners_by_ordered_role'] == [a, a, b, b]
    assert rec['original_spoke_supports'] == [[0, 1], [2, 3]]
    spokes = {edge(a, h) for h in (0, 1)} | {edge(b, h) for h in (2, 3)}
    assert original == FRAME | ce | owner_edges | spokes | {edge(a, b)}
    degrees = {v: sum(v in e for e in original) for v in vertices}
    assert degrees == {int(v): n for v, n in rec['original_complete_degrees'].items()}
    assert all(degrees[v] == (5 if v in (a, b) else 4) for v in vertices - B)
    COUNTS['complete_degree_graph_structures_reconstructed'] += 1
    return a, b, contacts, c, cv, ce, internal, original, vertices, spokes

FIXED = DATA['fixed_complete_degree_and_original_K5_controls']
records = FIXED['complete_degree_relation_controls']
assert unique([r['control_index'] for r in records]) == set(range(14))
assert unique([(r['identity'], r['root_swapped']) for r in records]) == set(product(named_parts, (False, True)))
direct_cache = {}
for rec in records:
    a, b, contacts, c, cv, ce, internal, original, vertices, spokes = reconstruct(rec, 'identity')
    assert [a, b] == ([6, 5] if rec['root_swapped'] else [5, 6])
    assert rec['boundary_cyclic_order'] == sorted(B) and rec['exact_actual_support_envelope'] == [1, 2]
    COUNTS['fixed_complete_degree_relation_graphs_checked'] += 1
    rows = rec['rows']
    assert unique([r['row_index'] for r in rows]) == set(range(10))
    for row in rows:
        ri, beta = row['row_index'], tuple(row['literal_boundary'])
        assert beta == ROWS[ri]
        corder = row['original_C_vertex_order']
        assert corder == sorted(B | cv)
        rc = stored_relation(row['complete_original_R_C'], corder, FRAME | ce, beta, contacts, 'original_R_C_witnesses_checked')
        assert rc == solve(B | cv, FRAME | ce, beta, contacts)
        COUNTS['independent_complete_four_contact_relations'] += 1
        variants = row['variants']
        assert unique([v['name'] for v in variants]) == {'G', 'G-C', 'G-a0', 'G-a1', 'G-b2', 'G-b3'}
        byname = {v['name']: v for v in variants}
        for v in variants:
            omitted = v['omitted_original_edge']
            oe = None if omitted is None else edge(*omitted)
            omit_c = v['original_C_omitted']
            assert (v['name'] == 'G-C') == omit_c
            if omitted is None:
                assert v['name'] in ('G', 'G-C')
            else:
                assert oe in spokes
            actual = original - ({oe} if oe else set())
            if omit_c:
                actual = {e for e in actual if not set(e) & cv}
            active = B | {a, b} | (set() if omit_c else cv)
            ports = [a, b] + ([] if omit_c else contacts)
            assert edges(v['actual_edges']) == actual
            assert v['original_vertex_order'] == sorted(active) and v['original_port_order'] == ports
            assert v['named_role_order'] == ['a', 'b'] + ([] if omit_c else ['x0', 'x1', 'y0', 'y1'])
            stored = stored_relation(v['complete_joint'], sorted(active), actual, beta, ports, 'complete_joint_witnesses_checked')
            direct = solve(active, actual, beta, ports)
            assert direct == stored
            direct_cache[(rec['control_index'], ri, v['name'])] = direct
            joined = set()
            for A, D in product(range(4), repeat=2):
                if A == D or any(A == beta[h] for h in (0, 1) if edge(a, h) != oe) or any(D == beta[h] for h in (2, 3) if edge(b, h) != oe):
                    continue
                for t in ([()] if omit_c else rc):
                    if omit_c or (A not in t[:2] and D not in t[2:]):
                        joined.add((A, D, *t))
            assert joined == direct
            COUNTS['independent_complete_whole_graph_joints'] += 1
            if omit_c:
                assert direct
                COUNTS['fixed_G_minus_C_Omega_rows_checked'] += 1
            else:
                assert all(t[2+i] == t[2+j] for t in direct for i, j in combinations(range(4), 2) if contacts[i] == contacts[j])
                if len(set(contacts)) < 4:
                    COUNTS['shared_contact_complete_joint_tuples_checked'] += len(direct)
            fibres = v['pinned_a_b_fibres']
            assert unique([(f['a_color'], f['b_color']) for f in fibres]) == set(product(range(4), repeat=2))
            for f in fibres:
                A, D = f['a_color'], f['b_color']
                pinned = solve(active, actual, beta, ports, {a: A, b: D})
                pf = {t[2:] for t in pinned}
                assert unique([tuple(t) for t in f['complete_C_role_fibre']]) == pf
                assert pf == {t[2:] for t in direct if t[:2] == (A, D)}
                COUNTS['independent_pinned_root_pair_fibres'] += 1
                COUNTS['independent_empty_pinned_root_pair_fibres'] += not pf
            if omitted is not None:
                r = next(z for z in omitted if z in (a, b))
                h = next(z for z in omitted if z in B)
                position = (a, b).index(r)
                assert {t for t in direct if t[position] != beta[h]} == {tuple(t['tuple']) for t in byname['G']['complete_joint']}
                COUNTS['exact_original_spoke_restorations_checked'] += 1
                COUNTS['fixed_spoke_omission_empty_rows_without_source_hypotheses'] += not direct
        s4 = row['global_S4_controls']
        assert unique([tuple(x['global_color_permutation']) for x in s4]) == set(permutations(range(4)))
        for x in s4:
            cp = x['global_color_permutation']
            moved = tuple(cp[c] for c in beta)
            assert tuple(x['transported_literal_boundary']) == moved
            mrc = solve(B | cv, FRAME | ce, moved, contacts)
            assert mrc == {tuple(cp[c] for c in t) for t in rc}
            assert x['independently_recomputed_complete_C_relation_size'] == len(mrc)
            COUNTS['independently_recomputed_global_S4_C_relations'] += 1
            for v in variants:
                for item in v['complete_joint']:
                    witness(v['original_vertex_order'], [cp[c] for c in item['coloring']], edges(v['actual_edges']), moved, v['original_port_order'], [cp[c] for c in item['tuple']])
                    COUNTS['global_S4_individual_joint_witnesses_checked'] += 1
                COUNTS['global_S4_variant_controls_checked'] += 1
        COUNTS['literal_rows_checked'] += 1
for rec, partner in zip(records[::2], records[1::2], strict=True):
    rename = lambda z: 11-z if z in (5, 6) else z
    assert {edge(rename(v), rename(w)) for v, w in edges(rec['original_edges'])} == edges(partner['original_edges'])
    assert rec['original_components']['C']['actual_attachments'] == partner['original_components']['C']['actual_attachments']
    for left, right in zip(rec['rows'], partner['rows'], strict=True):
        assert left['literal_boundary'] == right['literal_boundary']
        for lv, rv in zip(left['variants'], right['variants'], strict=True):
            assert {edge(rename(v), rename(w)) for v, w in edges(lv['actual_edges'])} == edges(rv['actual_edges'])
            assert [rename(z) for z in lv['original_port_order']] == rv['original_port_order']
            assert direct_cache[(rec['control_index'], left['row_index'], lv['name'])] == direct_cache[(partner['control_index'], right['row_index'], rv['name'])]
            assert lv['pinned_a_b_fibres'] == rv['pinned_a_b_fibres']
            COUNTS['literal_root_swap_relations_and_fibres_checked'] += 1

# Exact private palettes at every stored rejected row and every literal pair.
palettes = FIXED['exact_private_leaf_owner_palette_controls']
pr = palettes['literal_rejected_row_controls']
assert unique([x['row_index'] for x in pr]) == {1, 3, 4, 6}
for x in pr:
    ri, row = x['row_index'], tuple(x['literal_boundary'])
    assert row == ROWS[ri]
    pairs = solve(B | {5, 6}, SKELETON, row, [5, 6])
    assert unique([tuple(p) for p in x['complete_legal_root_pairs']]) == pairs
    assert unique([t['original_owner_role'] for t in x['private_owner_tables']]) == set(EXPECTED_ROLES)
    for t in x['private_owner_tables']:
        role, owners = t['original_owner_role'], EXPECTED_ROLES[t['original_owner_role']]
        hs = FORCED[role]
        assert t['original_root_owner_positions'] == list(owners) and t['forced_actual_boundary_attachments'] == hs
        entries = t['exact_private_lists']
        assert unique([tuple(e['original_root_colors']) for e in entries]) == pairs
        for e in entries:
            p = e['original_root_colors']
            forbidden = [row[h] for h in hs] + [p[j] for j in owners]
            assert e['actual_external_neighbor_colors'] == forbidden
            assert len(unique(forbidden)) == 2
            assert e['exact_private_list'] == sorted(U - set(forbidden))
            COUNTS['exact_private_leaf_owner_palettes_checked'] += 1
q = ROWS[palettes['owner_separating_row_index']]
assert tuple(palettes['owner_separating_literal_row']) == q
missing = next(iter(U - set(q)))
assert palettes['original_missing_color'] == missing == 3
pairs = [tuple(p) for p in palettes['exact_root_pair_order']]
assert pairs == [(3, 1), (2, 3)]
signatures = palettes['four_owner_signatures']
assert unique([x['original_owner_role'] for x in signatures]) == set(EXPECTED_ROLES)
for x in signatures:
    owners, hs = EXPECTED_ROLES[x['original_owner_role']], FORCED[x['original_owner_role']]
    exact = [sorted(U - ({q[h] for h in hs} | {p[j] for j in owners})) for p in pairs]
    assert x['exact_private_lists'] == exact and x['missing_color_membership'] == [int(missing in t) for t in exact]
    COUNTS['missing_color_exact_list_signatures_checked'] += 1
RESULT['examples']['q_only_is_insufficient'] = {
    'q': list(ROWS[1]), 'role': 'a_only', 'attachment_to_2_injective_for_q_only':
        all(ROWS[1][2] != A for A, D in solve(B | {5, 6}, SKELETON, ROWS[1], [5, 6])),
    'row_6_excludes_same_attachment': any(ROWS[6][2] == A for A, D in solve(B | {5, 6}, SKELETON, ROWS[6], [5, 6]))}
assert all(RESULT['examples']['q_only_is_insufficient'][k] for k in ('attachment_to_2_injective_for_q_only', 'row_6_excludes_same_attachment'))

def biconnected_blocks(vs, es):
    """New Tarjan edge-stack decomposition of actual internal edges."""
    adj = {v: [] for v in vs}
    for v, w in es:
        adj[v].append(w)
        adj[w].append(v)
    disc, low, stack, blocks = {}, {}, [], []
    def visit(v, parent=None):
        disc[v] = low[v] = len(disc)
        for w in sorted(adj[v]):
            if w == parent:
                continue
            if w not in disc:
                stack.append(edge(v, w))
                visit(w, v)
                low[v] = min(low[v], low[w])
                if low[w] >= disc[v]:
                    block = set()
                    while True:
                        e = stack.pop()
                        block.update(e)
                        if e == edge(v, w):
                            break
                    blocks.append(frozenset(block))
            elif disc[w] < disc[v]:
                stack.append(edge(v, w))
                low[v] = min(low[v], disc[w])
    visit(min(vs))
    assert set(disc) == set(vs) and not stack
    return blocks

def validate_bags(x, original, bags_key):
    bags = x[bags_key]
    assert len(bags) == 5 and all(len(unique(g)) == len(g) and connected(g, original) for g in bags)
    flat = [v for g in bags for v in g]
    assert len(unique(flat)) == len(flat)
    ws = x['ten_original_edge_witnesses']
    assert unique([tuple(w['branch_set_pair']) for w in ws]) == set(combinations(range(5), 2))
    for w in ws:
        i, j = w['branch_set_pair']
        v, z = w['original_edge']
        assert edge(v, z) in original and ((v in bags[i] and z in bags[j]) or (z in bags[i] and v in bags[j]))
        COUNTS['original_K5_interbag_edge_witnesses_checked'] += 1
    return bags

minors = FIXED['conditional_original_leaf_K5_minor_controls']
assert len(unique([x['name'] for x in minors])) == 7
leaf_lengths = []
for x in minors:
    a, b, contacts, c, cv, ce, internal, original, vertices, spokes = reconstruct(x, 'original_contact_identity')
    role = x['private_leaf_original_owner']
    leaf = x['original_leaf_odd_cycle']
    assert len(leaf) >= 3 and len(leaf) % 2 == 1 and len(unique(leaf)) == len(leaf)
    assert all(edge(v, w) in internal for v, w in zip(leaf, leaf[1:] + leaf[:1]))
    cut = x['original_leaf_cutvertex']
    private = x['original_leaf_private_vertices']
    assert cut == leaf[0] and private == leaf[1:]
    remainder = cv - set(private)
    assert unique(x['original_C_minus_private_vertices']) == remainder and connected(remainder, internal)
    assert x['original_C_minus_private_connected'] is True
    blocks = biconnected_blocks(cv, internal)
    stored_blocks = [frozenset(g) for g in c['original_block_vertex_sets']]
    assert unique(stored_blocks) == set(blocks)
    assert frozenset(leaf) in blocks and all(set(leaf) & set(g) <= {cut} for g in blocks if g != frozenset(leaf))
    for v in private:
        assert sum(v in e for e in internal) == 2
        expected_owners = [r for j, r in enumerate((a, b)) if j in EXPECTED_ROLES[role]]
        assert sorted(c['actual_original_owners'][str(v)]) == sorted(expected_owners)
        assert c['actual_attachments'][str(v)] == FORCED[role]
    hubs = x['original_adjacent_hub_pair']
    assert edge(*hubs) in original
    for v in private:
        assert {w if z == v else z for z, w in original if v in (z, w) and (w if z == v else z) not in cv} == set(hubs)
    bags = validate_bags(x, original, 'five_original_connected_branch_sets')
    assert set(bags[0]) | set(bags[1]) == set(private)
    assert bags[3:] == [[hubs[0]], [hubs[1]]]
    for p in x['actual_original_paths']:
        path = p['original_vertex_path']
        assert len(unique(path)) == len(path) and path[0] == cut and not set(path) & set(private)
        path_edges = [edge(v, w) for v, w in zip(path, path[1:])]
        assert all(e in original for e in path_edges)
        assert [tuple(e) for e in p['original_edge_path']] == path_edges
        COUNTS['conditional_leaf_actual_original_paths_checked'] += 1
    COUNTS['conditional_leaf_K5_controls_checked'] += 1
    COUNTS['independent_block_cut_decompositions_checked'] += 1
    if role == 'none':
        leaf_lengths.append(len(leaf))
assert sorted(leaf_lengths) == [3, 5, 7]

k4s = DATA['conditional_K4_actual_tether_controls']
assert len(k4s) == 2
for x in k4s:
    original = edges(x['original_edges'])
    clique = unique(x['original_K4'])
    assert len(clique) == 4 and all(edge(v, w) in original for v, w in combinations(clique, 2))
    assert all(sum(v in e for e in original) == 4 for v in clique)
    paths = x['actual_four_tether_paths']
    assert unique([p[0] for p in paths]) == clique
    all_interiors = []
    for p in paths:
        assert len(unique(p)) == len(p) and p[-1] in B | {5, 6}
        assert all(edge(v, w) in original for v, w in zip(p, p[1:]))
        all_interiors.extend(p[1:-1])
        COUNTS['conditional_K4_actual_tether_paths_checked'] += 1
    assert len(unique(all_interiors)) == len(all_interiors)
    assert not set(all_interiors) & (B | {5, 6} | clique)
    bags = validate_bags(x, original, 'five_original_branch_sets')
    assert set(bags[4]) == B | {5, 6} | set(all_interiors)
    assert x['unused_degree_edges_not_completed'] is True and x['fixed_pinned_root_pair_edge_minimality_used'] is False
    COUNTS['conditional_K4_tether_K5_controls_checked'] += 1

stored_witnesses = sum('tuple' in x and 'coloring' in x for x in walk(DATA))
assert stored_witnesses == COUNTS['original_R_C_witnesses_checked'] + COUNTS['complete_joint_witnesses_checked'] == 9598
COUNTS['all_serialized_tuple_coloring_witness_occurrences_checked'] = stored_witnesses
assert COUNTS['independent_complete_whole_graph_joints'] == 840
assert COUNTS['independent_pinned_root_pair_fibres'] == 13440
assert COUNTS['independent_empty_pinned_root_pair_fibres'] == 10372
assert COUNTS['exact_original_spoke_restorations_checked'] == 560
assert COUNTS['literal_root_swap_relations_and_fibres_checked'] == 420
assert COUNTS['independently_recomputed_global_S4_C_relations'] == 3360
assert COUNTS['global_S4_individual_joint_witnesses_checked'] == 183312
assert COUNTS['conditional_leaf_actual_original_paths_checked'] == 10
assert COUNTS['original_K5_interbag_edge_witnesses_checked'] == 90
assert DATA['summary']['fixed_control_summary'] == FIXED['summary']
assert FIXED['summary'] == {
    'complete_degree_original_graphs': 14, 'complete_relation_control_support': [1, 2],
    'conditional_original_leaf_K5_minors': 7, 'contact_identities': 7,
    'exact_original_spoke_restorations': 560,
    'fixed_controls_are_disk_source_realizations': False,
    'global_S4_complete_joint_witness_checks': 183312,
    'independently_checked_actual_external_paths': 10,
    'independently_checked_original_minor_adjacencies': 70,
    'independently_recomputed_global_S4_C_relations': 3360,
    'independently_recomputed_original_graph_joins': 840,
    'independently_recomputed_pinned_a_b_fibres': 13440,
    'none_owner_leaf_lengths': [3, 5, 7], 'private_owner_types': 4,
    'root_swap_variant_checks': 420, 'target_Sigma_or_criticality_claimed': False,
}
assert DATA['external_theorem']['fixed_pinned_root_pair_edge_minimality_required'] is False
for key in ('full_mixed22_branch_excluded', 'epsilon_three_proved', 'source_graph_catalogue_enumerated', 'source_realizability_claimed', 'new_lean_theorem'):
    assert DATA['summary'][key] is False
RESULT['summary'] = {'new_scope': 'B2 two named short faces and finite original controls',
    'selected_original_short_faces': 2, 'serialized_named_short_face_residuals': 0,
    'other_original_faces_retained': True, 'contact_identities': 7,
    'fixed_complete_degree_relation_graphs': 14, 'independent_complete_four_contact_relations': 140,
    'independent_complete_whole_graph_joints': 840, 'independent_pinned_root_pair_fibres': 13440,
    'independent_empty_pinned_root_pair_fibres': 10372,
    'all_serialized_tuple_coloring_witness_occurrences_checked': 9598,
    'conditional_leaf_K5_controls': 7, 'conditional_K4_tether_K5_controls': 2,
    'arbitrary_size_source_exclusion_independently_proved_by_finite_controls': False}
RESULT['counts'] = dict(sorted(COUNTS.items()))
RESULT['elapsed_seconds'] = round(time.monotonic() - started, 3)
RESULT['all_checks_passed'] = True
RESULT['producer_modules_imported'] = False
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'results.json').write_text(json.dumps(RESULT, ensure_ascii=False, sort_keys=True, indent=2) + '\n')
print(json.dumps({'all_checks_passed': True, 'elapsed_seconds': RESULT['elapsed_seconds'], 'counts': RESULT['counts']}, sort_keys=True), flush=True)
