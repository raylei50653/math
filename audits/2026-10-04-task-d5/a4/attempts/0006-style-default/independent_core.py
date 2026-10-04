#!/usr/bin/env python3
"""Independent mixed12 identity, serialized graph/relation and witness audit.

Only Python stdlib; imports no production enumerator, join or validator.
D5 provenance: copied D4 a3 independent_core.py; only independent utilities
and the A1 identity rebuild remain. D5 diagnostic transport loop removed.
No production code is imported. Retain ordinary graph and literal color frame.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time

COLORS = tuple(range(4))
BOUNDARY = set(range(5))
FRAME = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
PERMS = tuple(permutations(COLORS))
COUNTS = Counter()


def edge(a, b):
    return tuple(sorted((a, b)))


def es(values):
    result = {edge(*e) for e in values}
    assert len(result) == len(values), ('duplicate edges', values)
    assert all(a != b for a, b in result)
    return result


def unique(values, name):
    assert len(values) == len(set(values)), ('duplicate array identity', name)
    COUNTS['raw_arrays_checked_for_duplicates'] += 1


def tuples(values, name):
    result = [tuple(w['tuple']) for w in values]
    unique(result, name)
    return set(result)


def validate(order, values, edges, beta, ports=(), t=()):
    assert len(order) == len(values) and len(set(order)) == len(order)
    f = dict(zip(order, values, strict=True))
    assert all(c in COLORS for c in values)
    assert all(f[i] == c for i, c in enumerate(beta))
    assert all(a in f and b in f and f[a] != f[b] for a, b in edges)
    assert tuple(f[z] for z in ports) == tuple(t)
    COUNTS['stored_colorings_validated'] += 1
    return f


@lru_cache(maxsize=15000)
def enumerate_relation(order, edges, beta, ports):
    """New literal-color MRV backtracking; do not quotient colorings."""
    order, edges, beta, ports = tuple(order), tuple(edges), tuple(beta), tuple(ports)
    adj = {z: set() for z in order}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    f = dict(enumerate(beta))
    if any(f[a] == f[b] for a, b in edges if a in f and b in f):
        return frozenset()
    remaining = set(order) - set(f)
    result = set()

    def visit():
        if not remaining:
            result.add(tuple(f[z] for z in ports))
            return
        domains = {z: set(COLORS) - {f[w] for w in adj[z] if w in f}
                   for z in remaining}
        z = min(remaining, key=lambda z: (len(domains[z]), -len(adj[z]), z))
        if not domains[z]:
            return
        remaining.remove(z)
        for c in sorted(domains[z]):
            f[z] = c
            visit()
        f.pop(z, None)
        remaining.add(z)

    visit()
    return frozenset(result)


def relation(order, edges, beta, ports, stored, category):
    actual = tuples(stored, category)
    direct = enumerate_relation(tuple(order), tuple(sorted(edges)), tuple(beta), tuple(ports))
    assert actual == direct, ('incomplete relation', category, actual ^ direct)
    COUNTS[category + '_relations'] += 1
    for w in stored:
        validate(order, w['coloring'], edges, beta, ports, w['tuple'])
        COUNTS[category + '_witnesses'] += 1
    return actual


def fibres(stored, joint, tail_key):
    keys = [(f['a_color'], f['b_color']) for f in stored]
    unique(keys, 'literal pinned fibre keys')
    assert set(keys) == set(product(COLORS, repeat=2))
    for f in stored:
        key = (f['a_color'], f['b_color'])
        values = [tuple(t) for t in f[tail_key]]
        unique(values, tail_key)
        expected = {t[2:] for t in joint if t[:2] == key}
        assert set(values) == expected
        COUNTS['literal_pinned_fibres'] += 1
        COUNTS['empty_literal_pinned_fibres'] += not expected


def connected(vs, edges):
    reached = {min(vs)}
    while True:
        extended = reached | {w for a, b in edges for z, w in ((a, b), (b, a))
                              if z in reached and w in vs}
        if extended == reached:
            return reached == set(vs)
        reached = extended


def cycle(face):
    face = list(face)
    return min(tuple(f[i:] + f[:i]) for f in (face, face[::-1]) for i in range(len(f)))


def faces(rotation):
    darts = {(v, w) for v, ring in rotation.items() for w in ring}
    result = []
    while darts:
        start = min(darts)
        d = start
        found = []
        while True:
            assert d in darts
            darts.remove(d)
            v, w = d
            found.append(v)
            ring = rotation[w]
            d = (w, ring[(ring.index(v) + 1) % len(ring)])
            if d == start:
                break
        result.append(found)
    return result


def disk_rotations(edges):
    vertices = sorted(set().union(*(set(e) for e in edges)))
    choices = []
    for v in vertices:
        adjacent = sorted(w for e in edges for z, w in (e, e[::-1]) if z == v)
        choices.append([(adjacent[0],) + p for p in permutations(adjacent[1:])])
    result = {}
    assignments = 0
    for rings in product(*choices):
        assignments += 1
        rot = dict(zip(vertices, rings, strict=True))
        fs = faces(rot)
        outer = [f for f in fs if len(f) == 5 and set(f) == BOUNDARY]
        if len(vertices) - len(edges) + len(fs) == 2 and len(outer) == 1:
            result[tuple((v, rot[v]) for v in vertices)] = frozenset(cycle(f) for f in fs if f != outer[0])
    return assignments, result


def normalized(row):
    names = {}
    for c in row:
        names.setdefault(c, len(names))
    return tuple(names[c] for c in row), names


def transported(row, move):
    result = [None] * 5
    for i, c in enumerate(row):
        result[move[i]] = c
    return normalized(result)


def moved_mask(sigma, move, rows):
    return sum(1 << rows.index(transported(row, move)[0]) for i, row in enumerate(rows)
               if sigma >> i & 1)


@lru_cache(maxsize=2000)
def schedules(sigma, spokes, support, rows):
    rs = tuple((i, q) for i, q in enumerate(rows) if not sigma >> i & 1)
    domains = [tuple(c for c in COLORS if c not in {q[h] for h in spokes}) for i, q in rs]
    constraints = [(i, j, p) for i, (_, q) in enumerate(rs) for j, (_, r) in enumerate(rs)
                   for p in PERMS if all(p[q[h]] == r[h] for h in support)]
    result = {}
    for values in product(*domains):
        covariant = all(p[values[i]] == values[j] for i, j, p in constraints)
        conserved = not (3 in values and any(c != 3 for c in values))
        result[values] = (covariant, conserved)
    return rs, domains, constraints, result


def audit_schedule(screen, sigma, spokes, support, rows):
    assert screen['source_sigma'] == sigma
    assert tuple(screen['original_a_spokes']) == tuple(sorted(spokes))
    assert tuple(screen['actual_original_U_support']) == tuple(sorted(support))
    rs, domains, constraints, expected = schedules(sigma, tuple(sorted(spokes)), tuple(sorted(support)), rows)
    assert screen['candidate_singleton_domains'] == [list(x) for x in domains]
    assert screen['literal_rejected_rows'] == [dict(row_index=i, literal_boundary=list(q)) for i, q in rs]
    assert screen['support_matching_S4_constraints'] == len(constraints)
    assert screen['same_row_stabilizer_constraints'] == sum(i == j for i, j, p in constraints)
    candidates = screen['all_candidate_schedules']
    unique([tuple(s['singleton_colors']) for s in candidates], 'candidate singleton schedules')
    assert {tuple(s['singleton_colors']) for s in candidates} == set(expected)
    for s in candidates:
        values = tuple(s['singleton_colors'])
        equivariant, conserved = expected[values]
        assert (s['support_S4_equivariant'], s['fixed_unused_3_conserved']) == (equivariant, conserved)
        assert s['survives_both_necessary_controls'] == (equivariant and conserved)
        for item, (i, q), c in zip(s['complete_singleton_unary_relations'], rs, values, strict=True):
            assert item == dict(row_index=i, literal_boundary=list(q), contact_order=['u'], complete_R_U=[[c]])
            COUNTS['complete_singleton_schedule_rows'] += 1
        conflict = s['first_S4_conflict']
        if conflict:
            i, j = conflict['source_row_index'], conflict['target_row_index']
            p = conflict['literal_color_permutation']
            assert sorted(p) == list(COLORS)
            assert all(p[rows[i][h]] == rows[j][h] for h in support)
            ri = [i for i, q in rs].index(i)
            rj = [i for i, q in rs].index(j)
            assert p[values[ri]] != values[rj]
            COUNTS['independently_validated_S4_conflict_witnesses'] += 1
        conservation = s['fixed_unused_3_conflict']
        if conservation:
            assert conservation['fixed_unused_color'] == 3
            p = conservation['row_forbidding_fixed_color']
            q = conservation['row_forbidding_other_color']
            assert p['complete_R_U'] == [[3]] and q['complete_R_U'] != [[3]]
            assert 3 not in rows[p['row_index']] and 3 not in rows[q['row_index']]
            COUNTS['unused_color_conservation_premise_witnesses'] += 1
    survivors = screen['surviving_schedules']
    unique([tuple(s['singleton_colors']) for s in survivors], 'surviving singleton schedules')
    assert {tuple(s['singleton_colors']) for s in survivors} == {v for v, (a, b) in expected.items() if a and b}
    for s in survivors:
        assert s in candidates
    COUNTS['independent_actual_support_schedule_screens'] += 1


def audit_omissions(f):
    ids = [(x['original_omission'], x['omitted_original_spoke_point']) for x in f['original_omission_identities']]
    unique(ids, 'omission identities')
    assert set(ids) == {('a_spoke', i) for i in f['original_a_spokes']} | {('b_spoke', i) for i in f['original_b_spokes']} | {('whole_U', None)}
    for item in f['original_omission_identities']:
        kind, point = item['original_omission'], item['omitted_original_spoke_point']
        factors = [(f'a:spoke:{i}', (1, 0)) for i in f['original_a_spokes'] if kind != 'a_spoke' or i != point]
        factors += [(f'b:spoke:{i}', (0, 1)) for i in f['original_b_spokes'] if kind != 'b_spoke' or i != point]
        factors += [('original:C', (1, 2))]
        if kind != 'whole_U':
            factors += [('original:U', (1, 0))]
        assert item['retained_original_factors'] == [dict(id=k, incidence=list(v)) for k, v in factors]
        degrees = (5, 4) if kind == 'b_spoke' else (4, 5)
        expected = {}
        for n in range(len(factors) + 1):
            for indices in combinations(range(len(factors)), n):
                ds = tuple(degrees[j] - sum(factors[i][1][j] for i in indices) for j in (0, 1))
                if min(ds) >= 4:
                    expected[tuple(factors[i][0] for i in indices)] = ds
        actual = item['all_degree_admissible_further_omissions']
        unique([tuple(x['omitted_original_factors']) for x in actual], 'degree admissible omissions')
        assert {tuple(x['omitted_original_factors']): tuple(x['resulting_a_b_degrees']) for x in actual} == expected
        COUNTS['independent_factor_omission_identities'] += 1


def audit_identity(data, source, rows):
    results = []
    swap_ids = [tuple(p) for p in data['root_swap_frames']]
    unique(swap_ids, 'raw root-swap frame array')
    expected_swap_ids = set()
    unique([t['source_sigma'] for t in data['targets']], 'target masks')
    for target in data['targets']:
        sigma = target['source_sigma']
        generic, = [t for t in source['targets'] if t['source_sigma'] == sigma]
        rs = [r for i, r in enumerate(rows) if not sigma >> i & 1]
        a_pairs = [p for p in combinations(range(5), 2) if all(r[p[0]] != r[p[1]] for r in rs)]
        b_pairs = []
        for p in combinations(range(5), 2):
            forced = {next(i for i in range(5) if r.count(r[i]) == 1) for r in rs if r[p[0]] == r[p[1]]}
            if not any(set(e) <= forced for e in FRAME):
                b_pairs.append(p)
            stored, = [r for r in target['original_b_pair_necessary_constraints'] if tuple(r['original_b_spoke_pair']) == p]
            adjacent = [list(e) for e in sorted(FRAME) if set(e) <= forced]
            assert stored['same_color_forced_rejected_positions'] == sorted(forced)
            assert stored['violating_adjacent_rejected_positions'] == adjacent
            assert stored['admissible_generic_single_spoke_position_constraint'] == (not adjacent)
            COUNTS['independent_b_pair_source_filter_records'] += 1
        unique([tuple(r['original_b_spoke_pair']) for r in target['original_b_pair_necessary_constraints']], 'b-pair constraint array')
        assert len(target['original_b_pair_necessary_constraints']) == 10
        exclusions = target['original_a_pair_exclusions']
        unique([tuple(r['original_pair']) for r in exclusions], 'a-pair exclusion array')
        assert {tuple(r['original_pair']) for r in exclusions} == set(combinations(range(5), 2)) - set(a_pairs)
        for r in exclusions:
            p = r['original_pair']
            assert r['same_color_rejected_rows'] == [list(q) for q in rs if q[p[0]] == q[p[1]]]
        assert set(a_pairs) == FRAME
        domain = {(sigma, a, b, sa, sb) for a, b in ((5, 6), (6, 5)) for sa, sb in product(a_pairs, b_pairs)}
        frames = target['fresh_original_incidence_named_frames']
        keys = [(f['source_sigma'], f['original_a'], f['original_b'], tuple(f['original_a_spokes']), tuple(f['original_b_spokes'])) for f in frames]
        unique(keys, 'source-filtered fresh frames')
        unique([f['named_frame_id'] for f in frames], 'fresh named frame ids')
        assert set(keys) == domain
        excluded = target['excluded_named_frame_ids']
        remaining = target['remaining_named_original_frames']
        unique(excluded, 'excluded raw ids')
        unique([f['named_frame_id'] for f in remaining], 'remaining raw frame ids')
        assert set(excluded) | {f['named_frame_id'] for f in remaining} == {f['named_frame_id'] for f in frames}
        assert not set(excluded) & {f['named_frame_id'] for f in remaining}
        assignments, disk_count, residual_records, residual_schedules = 0, 0, 0, 0
        for f in frames:
            assert f['source_sigma'] == sigma
            a, b = f['original_a'], f['original_b']
            sa, sb = tuple(f['original_a_spokes']), tuple(f['original_b_spokes'])
            expected_edges = FRAME | {edge(a, b)} | {edge(a, h) for h in sa} | {edge(b, h) for h in sb}
            assert es(f['original_root_and_boundary_edges']) == expected_edges
            supports = [list(sa), list(sb)] if a == 5 else [list(sb), list(sa)]
            matches = [(i, r) for i, r in enumerate(generic['named_spoke_skeletons']['records']) if r['original_spoke_supports'] == supports]
            assert len(matches) == 1
            i, src = matches[0]
            assert f['generic_single_spoke_source_index'] == i and src['status'] == 'necessary_skeleton_only'
            assert es(src['retained_source_edges']) == expected_edges
            contract = f['original_incidence_contract']
            assert contract['C_incidence'] == [1, 2] and contract['C_owners'] == [a, b, b] and contract['U_owner'] == a
            audit_omissions(f)
            n, computed = disk_rotations(expected_edges)
            rot_info = f['exhaustive_original_skeleton_rotations']
            assert rot_info['rotation_assignments_checked'] == n
            serialized = rot_info['all_disk_rotations']
            actual = {tuple((p['vertex'], tuple(p['ring'])) for p in r['rotation']): frozenset(tuple(x) for x in r['original_disk_faces']) for r in serialized}
            assert len(actual) == len(serialized) and actual == computed
            assignments += n
            disk_count += len(computed)
            COUNTS['independent_exhaustive_rotation_frames'] += 1
            fs = set().union(*computed.values())
            placements = f['all_original_U_face_support_placements']
            unique([tuple(p['original_U_face']) for p in placements], 'U face placements')
            assert {tuple(p['original_U_face']) for p in placements} == {face for face in fs if a in face}
            expected_residual = []
            for placement in placements:
                face = tuple(placement['original_U_face'])
                envelope = set(face) & BOUNDARY
                assert placement['exact_face_boundary_envelope'] == sorted(envelope)
                indices = [i for i, r in enumerate(serialized) if list(face) in r['original_disk_faces']]
                assert placement['supporting_original_rotation_indices'] == indices
                cfaces = set().union(*(set(tuple(x) for x in serialized[i]['original_disk_faces']) for i in indices))
                cfaces = {x for x in cfaces if a in x and b in x}
                assert {tuple(c['face']) for c in placement['compatible_original_C_common_faces']} == cfaces
                for c in placement['compatible_original_C_common_faces']:
                    assert c['supporting_rotation_indices'] == [i for i in indices if c['face'] in serialized[i]['original_disk_faces']]
                supports = placement['all_actual_original_U_support_subsets']
                unique([tuple(s['actual_original_U_support']) for s in supports], 'actual support subsets')
                assert {tuple(s['actual_original_U_support']) for s in supports} == {p for n in range(len(envelope)+1) for p in combinations(sorted(envelope), n)}
                for s in supports:
                    support = tuple(s['actual_original_U_support'])
                    short = len(support) <= 1 or any(set(support) <= set(e) for e in FRAME)
                    if short:
                        assert s['status'] == 'excluded_original_au_noncritical_short_support'
                        lemma = s['original_external_path_lemma_instance']
                        assert lemma['actual_support'] == list(support) and lemma['original_unary_owner'] == a
                        assert set(support) <= set(lemma['enclosing_original_boundary_edge'])
                        if 'original_external_path' in lemma:
                            path = lemma['original_external_path']
                            assert path[0] == a and path[-1] in BOUNDARY-set(lemma['enclosing_original_boundary_edge'])
                            assert len(path) == len(set(path)) and all(edge(v,w) in expected_edges for v,w in zip(path,path[1:]))
                            COUNTS['independent_short_support_skeleton_path_witnesses'] += 1
                        else:
                            assert lemma['skeleton_only_original_path_claimed'] is False
                            assert lemma['original_external_path_roles'][0] == a
                            COUNTS['short_support_paper_path_existence_records'] += 1
                    else:
                        screen = s['complete_singleton_unary_relation_screen']
                        audit_schedule(screen, sigma, sa, support, rows)
                        survives = bool(screen['surviving_schedules'])
                        assert s['status'] == ('necessary_original_U_relation_only' if survives else 'excluded_by_same_original_U_relation')
                        if survives:
                            expected_residual.append((face, support))
            residual = f['remaining_named_original_U_placements']
            unique([(tuple(p['original_U_face']), tuple(p['actual_original_U_support'])) for p in residual], 'residual raw placement identities')
            assert set(expected_residual) == {(tuple(p['original_U_face']), tuple(p['actual_original_U_support'])) for p in residual}
            assert f['status'] == ('necessary_named_source_residual' if residual else 'named_original_source_excluded')
            assert (f['named_frame_id'] in excluded) == (not residual)
            assert (f in remaining) == bool(residual)
            for p in residual:
                original_p, = [z for z in placements if z['original_U_face'] == p['original_U_face']]
                original_s, = [s for s in original_p['all_actual_original_U_support_subsets'] if s['actual_original_U_support'] == p['actual_original_U_support']]
                assert p['complete_singleton_unary_relation_schedules'] == original_s['complete_singleton_unary_relation_screen']['surviving_schedules']
                assert p['supporting_original_rotation_indices'] == original_p['supporting_original_rotation_indices']
                assert p['compatible_original_C_common_faces'] == original_p['compatible_original_C_common_faces']
                residual_records += 1
                residual_schedules += len(p['complete_singleton_unary_relation_schedules'])
            partner, = [q for q in frames if q['original_a'] == b and tuple(q['original_a_spokes']) == sa and tuple(q['original_b_spokes']) == sb]
            expected_swap_ids.add((f['named_frame_id'], partner['named_frame_id']))
            move_root = lambda v: 11-v if v in (5, 6) else v
            assert {edge(move_root(v), move_root(w)) for v, w in expected_edges} == es(partner['original_root_and_boundary_edges'])
            expected_partner = {(cycle([move_root(v) for v in p['original_U_face']]), tuple(p['actual_original_U_support']), tuple(tuple(x['singleton_colors']) for x in p['complete_singleton_unary_relation_schedules'])) for p in residual}
            actual_partner = {(tuple(p['original_U_face']), tuple(p['actual_original_U_support']), tuple(tuple(x['singleton_colors']) for x in p['complete_singleton_unary_relation_schedules'])) for p in partner['remaining_named_original_U_placements']}
            assert expected_partner == actual_partner
            for placement in placements:
                partner_placement, = [p for p in partner['all_original_U_face_support_placements'] if tuple(p['original_U_face']) == cycle([move_root(v) for v in placement['original_U_face']])]
                left_supports = placement['all_actual_original_U_support_subsets']
                right_supports = partner_placement['all_actual_original_U_support_subsets']
                assert len(left_supports) == len(right_supports)
                for left_support, right_support in zip(left_supports, right_supports, strict=True):
                    moved_support = json.loads(json.dumps(left_support))
                    lemma = moved_support.get('original_external_path_lemma_instance')
                    if lemma:
                        lemma['original_unary_owner'] = move_root(lemma['original_unary_owner'])
                        for field in ('original_external_path', 'original_external_path_roles'):
                            if field in lemma:
                                lemma[field] = [move_root(v) if isinstance(v,int) else v for v in lemma[field]]
                    assert moved_support == right_support
                expected_cfaces = {cycle([move_root(v) for v in c['face']]) for c in placement['compatible_original_C_common_faces']}
                assert expected_cfaces == {tuple(c['face']) for c in partner_placement['compatible_original_C_common_faces']}
                COUNTS['named_root_swap_all_face_support_checks'] += 1
            for rot in serialized:
                exchanged = {move_root(p['vertex']): tuple(move_root(v) for v in p['ring']) for p in rot['rotation']}
                exchanged_faces = {cycle(x) for x in faces(exchanged)}
                assert any(len(x) == 5 and set(x) == BOUNDARY for x in exchanged_faces)
                assert {cycle([move_root(v) for v in x]) for x in rot['original_disk_faces']} <= exchanged_faces
                COUNTS['root_swap_saved_rotation_legality_checks'] += 1
            COUNTS['named_root_swap_frame_checks'] += 1
        result = dict(source_sigma=sigma, source_filtered_named_frames=len(domain), excluded=len(excluded), residual=len(remaining), residual_actual_face_support_records=residual_records, residual_complete_schedules=residual_schedules, rotation_assignments=assignments, disk_rotations=disk_count)
        assert result['source_filtered_named_frames'] == target['summary']['necessary_named_frames']
        assert residual_records == target['summary']['remaining_actual_U_face_support_records'] and residual_schedules == target['summary']['remaining_complete_singleton_relation_schedules']
        results.append(result)
    assert expected_swap_ids == set(swap_ids)
    return results
