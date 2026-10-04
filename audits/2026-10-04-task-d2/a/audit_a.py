#!/usr/bin/env python3
"""Independent mixed12 identity, serialized graph/relation and witness audit.

Only Python stdlib; imports no production enumerator, join or validator.
Reads a frozen repository snapshot and writes only beside this audit script.
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
                rejected = [(i, q) for i, q in enumerate(rows) if not sigma >> i & 1]
                for sign, shift in product((-1, 1), range(5)):
                    move = [(sign*i+shift) % 5 for i in range(5)]
                    transported_sigma = moved_mask(sigma, move, rows)
                    COUNTS[f'D5_source_mask_{sigma}_to_{transported_sigma}'] += 1
                    screen = schedules(transported_sigma, tuple(sorted(move[i] for i in sa)), tuple(sorted(move[i] for i in p['actual_original_U_support'])), rows)
                    expected = set()
                    for sched in p['complete_singleton_unary_relation_schedules']:
                        by_row = {}
                        for (_, q), color in zip(rejected, sched['singleton_colors'], strict=True):
                            moved_row, colors = transported(q, move)
                            assert color in colors or color == 3
                            by_row[moved_row] = colors.get(color, 3)
                        expected.add(tuple(by_row[q] for i, q in enumerate(rows) if not transported_sigma >> i & 1))
                    assert expected == {v for v, (aok, bok) in screen[3].items() if aok and bok}
                    # Relabel the saved rotation itself; no separately selected canonical rotation is compared.
                    for ri in p['supporting_original_rotation_indices']:
                        rot = {((move[x['vertex']]) if x['vertex'] in BOUNDARY else x['vertex']): tuple(move[w] if w in BOUNDARY else w for w in x['ring']) for x in serialized[ri]['rotation']}
                        fs2 = faces(rot)
                        assert 7-len(expected_edges)+len(fs2) == 2
                        assert any(len(x) == 5 and set(x) == BOUNDARY for x in fs2)
                        COUNTS['D5_original_rotations_transported'] += 1
                    COUNTS['D5_complete_residual_schedule_checks'] += 1
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


def audit_graphs(data, rows):
    controls = data['fixed_full_degree_same_graph_controls']
    records = controls['records']
    unique([r['control_index'] for r in records], 'control indices')
    assert [r['control_index'] for r in records] == list(range(len(records)))
    image_counts = Counter()
    for rec in records:
        a, b = rec['original_a'], rec['original_b']
        C, U = rec['C'], rec['unary_U']
        cv, uv = set(C['vertices']), set(U['vertices'])
        x, y0, y1 = C['ordered_contacts']
        u, = U['ordered_contacts']
        ports = [a, b, x, y0, y1, u]
        assert C['owners'] == [a, b, b] and U['owner'] == a
        assert rec['complete_port_order'] == ports and y0 != y1
        assert C['x_y_alias'] == ('y0' if x == y0 else 'y1' if x == y1 else None)
        COUNTS['contact_identity_' + str(C['x_y_alias']) + '_graphs'] += 1
        assert not cv & uv and not (cv | uv) & (BOUNDARY | {a, b})
        original = es(rec['original_edges'])
        parts = {}
        for name, part in (('C', C), ('U', U)):
            vertices = set(part['vertices'])
            internal = es(part['original_internal_edges'])
            assert all(set(e) <= vertices for e in internal) and connected(vertices, internal)
            attach = {edge(int(v), h) for v, hs in part['actual_attachments'].items() for h in hs}
            assert set(map(int, part['actual_attachments'])) == vertices
            assert {h for v, hs in part['actual_attachments'].items() for h in hs} == set(part['actual_support'])
            assert all(h in BOUNDARY for hs in part['actual_attachments'].values() for h in hs)
            parts[name] = internal | attach
            for p in part['original_owner_to_attachment_paths']:
                path = p['original_path']
                assert path[0] == p['owner'] and path[-1] == p['boundary_endpoint']
                assert len(path) == len(set(path)) and set(path[1:-1]) <= vertices
                assert all(edge(v, w) in original for v, w in zip(path, path[1:]))
                assert p['owner'] in ([a, b] if name == 'C' else [a])
                COUNTS['actual_attachment_path_witnesses'] += 1
        crosscut = U['original_0_to_3_crosscut']
        assert crosscut[0] == 0 and crosscut[-1] == 3 and set(crosscut[1:-1]) <= uv
        assert len(crosscut) == len(set(crosscut))
        assert all(edge(v, w) in parts['U'] for v, w in zip(crosscut, crosscut[1:]))
        rebuilt = FRAME | parts['C'] | parts['U'] | {edge(a, b), edge(a, x), edge(a, u), edge(b, y0), edge(b, y1)}
        rebuilt |= {edge(a, h) for h in rec['original_root_spokes']['a']} | {edge(b, h) for h in rec['original_root_spokes']['b']}
        assert original == rebuilt
        order = sorted(BOUNDARY | {a, b} | cv | uv)
        assert order == rec['vertex_order']
        assert all(sum(z in e for e in original) == (5 if z in (a, b) else 4) for z in {a, b} | cv | uv)
        assert len(rec['rows']) == len(rows)
        variant_images = Counter()
        for row_index, row in enumerate(rec['rows']):
            assert row['row_index'] == row_index and tuple(row['literal_boundary']) == rows[row_index]
            beta = rows[row_index]
            cr = relation(C['vertex_order'], FRAME | parts['C'], beta, [x, y0, y1], row['C_complete_tuples'], 'C_complete_ternary')
            ur = relation(U['vertex_order'], FRAME | parts['U'], beta, [u], row['U_complete_tuples'], 'U_complete_unary')
            unique([v['id'] for v in row['variants']], 'variants')
            assert {v['id'] for v in row['variants']} == {'original', 'a_spoke_0', 'a_spoke_1', 'b_spoke_2', 'b_spoke_3', 'a_x', 'a_u'}
            joints = {}
            for var in row['variants']:
                omitted = var['omitted_original_edge']
                expected = original - ({edge(*omitted)} if omitted is not None else set())
                edges = es(var['actual_edges'])
                assert edges == expected
                assert var['full_a_b_degrees'] == [sum(r in e for e in edges) for r in (a, b)]
                joint = relation(order, edges, beta, ports, var['complete_joint_tuples'], 'full_six_role_joint')
                joints[var['id']] = joint
                variant_images[var['id']] += (1 << row_index) if joint else 0
                fibres(var['pinned_a_b_fibers'], joint, 'complete_x_y0_y1_u_fiber')
                # Separate fresh join from independent literal graph enumeration.
                joined = {(ac, bc, xc, c0, c1, uc) for xc, c0, c1 in cr for uc, in ur for ac, bc in product(COLORS, repeat=2)
                          if ac != bc and all(ac != beta[h] for h in range(5) if edge(a, h) in edges)
                          and all(bc != beta[h] for h in range(5) if edge(b, h) in edges)
                          and (edge(a, x) not in edges or ac != xc) and (edge(a, u) not in edges or ac != uc)
                          and bc != c0 and bc != c1}
                assert joined == joint
                COUNTS['independent_same_graph_join_crosschecks'] += 1
                if 'original_K' in var or 'original_L' in var:
                    key = 'original_K' if 'original_K' in var else 'original_L'
                    part = var[key]
                    p_edges = es(part['actual_edges']) | FRAME
                    expected_vs = {a} | cv | uv if key == 'original_K' else {b} | cv
                    expected_edges = {e for e in edges if b not in e} if key == 'original_K' else FRAME | parts['C'] | {edge(b, y0), edge(b, y1)} | {edge(b, h) for h in var['retained_b_spokes']}
                    assert p_edges == expected_edges and set(part['vertices']) == expected_vs
                    assert connected(expected_vs, p_edges)
                    field = 'complete_ternary_relation' if key == 'original_K' else 'complete_binary_relation'
                    expected_ports = [a, y0, y1] if key == 'original_K' else [x, b]
                    assert part['ordered_contacts'] == expected_ports
                    relation(part['vertex_order'], p_edges, beta, expected_ports, part[field], 'K_after_a_spoke' if key == 'original_K' else 'L_after_b_spoke')
                    if key == 'original_K':
                        assert part['marked_a_degree_in_K'] == 2 and set(part['marked_a_actual_neighbors']) == {x, u}
                if 'exact_reattachment' in var and 'removed_joint_tuples' in var['exact_reattachment']:
                    info = var['exact_reattachment']
                    position, endpoint = info['root_tuple_position'], info['boundary_endpoint']
                    removed = tuples(info['removed_joint_tuples'], 'removed_joint_tuples')
                    assert removed == {t for t in joint if t[position] == beta[endpoint]}
                    for w in info['removed_joint_tuples']:
                        validate(order, w['coloring'], edges, beta, ports, w['tuple'])
                        COUNTS['reattachment_removed_tuple_witnesses'] += 1
            restored = joints['original']
            for name, joint in joints.items():
                if name == 'original':
                    continue
                var, = [v for v in row['variants'] if v['id'] == name]
                omitted = var['omitted_original_edge']
                guard = set()
                for t in joint:
                    f = dict(enumerate(beta)) | dict(zip(ports, t, strict=True))
                    if f[omitted[0]] != f[omitted[1]]:
                        guard.add(t)
                assert guard == restored
                COUNTS['exact_original_edge_reattachment_checks'] += 1
            n = row['original_unary_omission']
            nedges = {e for e in original if not set(e) & uv}
            norder = sorted(set(order)-uv)
            assert es(n['actual_edges']) == nedges and n['vertex_order'] == norder
            assert n['removed_original_vertices'] == sorted(uv) and n['complete_port_order'] == ports[:5]
            nj = relation(norder, nedges, beta, ports[:5], n['complete_five_role_joint'], 'N_five_role_joint')
            variant_images[n['id']] += (1 << row_index) if nj else 0
            fibres(n['pinned_a_b_fibers'], nj, 'complete_x_y0_y1_fiber')
            assert joints['a_u'] == {(*t, uc) for t in nj for uc, in ur}
            assert {t[:5] for t in joints['a_u']} == nj
            assert n['all_literal_a_colors'] == sorted({t[0] for t in nj})
            assert n['original_U_contact_colors'] == sorted(t[0] for t in ur)
            COUNTS['literal_U_omission_product_checks'] += 1
            k = n['original_K_after_b_deletion']
            kedges = {e for e in nedges if b not in e}
            assert es(k['actual_edges']) == kedges and set(k['vertices']) == ({a} | cv)
            assert k['marked_a_degree_in_K'] == 1 and k['marked_a_actual_neighbors'] == [x]
            relation(k['vertex_order'], kedges, beta, [a, y0, y1], k['complete_ternary_relation'], 'K_after_whole_U_omission')
            if C['actual_support'] == [3]:
                projection = lambda j: {(t[0], t[1], t[5]) for t in j}
                assert projection(restored) == projection(joints['a_x'])
                exterior = {(ac, bc, uc) for uc, in ur for ac, bc in product(COLORS, repeat=2)
                            if ac != bc and ac not in {beta[0], beta[1], uc} and bc not in {beta[2], beta[3]}}
                assert projection(restored) == exterior
                COUNTS['sealed_C_projection_checks'] += 1
        for image in rec['independently_computed_control_boundary_images']:
            assert image['full_boundary_image'] == variant_images[image['variant_id']]
            COUNTS['independent_control_Sigma_masks'] += 1
        image_counts[variant_images['original']] += 1
        COUNTS['fixed_graphs'] += 1
    for pair in controls['root_swap_controls']:
        left, right = (records[pair[k]] for k in ('original_control_index', 'exchanged_control_index'))
        move = lambda z: 11-z if z in (5, 6) else z
        assert {edge(move(v), move(w)) for v, w in left['original_edges']} == es(right['original_edges'])
        for name in ('C', 'unary_U'):
            p, q = left[name], right[name]
            for field in ('vertices', 'ordered_contacts', 'actual_attachments', 'actual_support', 'original_internal_edges'):
                assert p[field] == q[field]
            if name == 'C':
                assert [move(z) for z in p['owners']] == q['owners']
            else:
                assert move(p['owner']) == q['owner']
        for lr, rr in zip(left['rows'], right['rows'], strict=True):
            for lv, rv in zip(lr['variants'], rr['variants'], strict=True):
                assert lv['pinned_a_b_fibers'] == rv['pinned_a_b_fibers']
                assert {edge(move(v), move(w)) for v, w in lv['actual_edges']} == es(rv['actual_edges'])
                assert [w['tuple'] for w in lv['complete_joint_tuples']] == [w['tuple'] for w in rv['complete_joint_tuples']]
                for lw, rw in zip(lv['complete_joint_tuples'], rv['complete_joint_tuples'], strict=True):
                    f = dict(zip(left['vertex_order'], lw['coloring'], strict=True))
                    assert [f[move(z)] for z in right['vertex_order']] == rw['coloring']
                    COUNTS['root_swap_literal_full_witness_checks'] += 1
                COUNTS['root_swap_literal_joint_checks'] += 1
            ln, rn = lr['original_unary_omission'], rr['original_unary_omission']
            assert ln['pinned_a_b_fibers'] == rn['pinned_a_b_fibers']
            for lw, rw in zip(ln['complete_five_role_joint'], rn['complete_five_role_joint'], strict=True):
                assert lw['tuple'] == rw['tuple']
                f = dict(zip(ln['vertex_order'], lw['coloring'], strict=True))
                assert [f[move(z)] for z in rn['vertex_order']] == rw['coloring']
                COUNTS['root_swap_literal_N_witness_checks'] += 1
        COUNTS['root_swap_graph_pairs'] += 1
    for name in ('complete_nonempty_singleton_join_controls',):
        for g in data[name]:
            ad, ud = g['nonempty_original_N_a_domain'], g['nonempty_complete_original_U_relation']
            expected = {(a, u) for a in ad for u in ud if a != u}
            assert set(map(tuple, g['all_guarded_a_u_pairs'])) == expected
            assert g['source_rejects'] == (not expected) == (len(ad) == len(ud) == 1 and ad == ud)
            COUNTS['independent_nonempty_domain_guard_checks'] += 1
    helper_guards = controls['complete_domain_singleton_guard_controls']
    unique([(tuple(g['complete_a_domain']), tuple(g['complete_R_U'])) for g in helper_guards], 'helper complete nonempty domain pairs')
    domains = {p for n in range(1, 5) for p in combinations(COLORS, n)}
    assert {(tuple(g['complete_a_domain']), tuple(g['complete_R_U'])) for g in helper_guards} == set(product(domains, repeat=2))
    for g in helper_guards:
        ad, ud = g['complete_a_domain'], g['complete_R_U']
        expected = {(a, u) for a in ad for u in ud if a != u}
        assert set(map(tuple, g['complete_guarded_pair_relation'])) == expected
        assert (not expected) == (len(ad) == len(ud) == 1 and ad == ud)
        COUNTS['independent_helper_nonempty_domain_guard_checks'] += 1
    special = {}
    for name in ('ternary_marginal_collision', 'nonempty_omission_empty_original_joint', 'six_role_joint_inequivalence'):
        item = controls[name]
        rec = records[item['control_index']]
        row = rec['rows'][item['row_index']]
        beta = rows[item['row_index']]
        original, = [v for v in row['variants'] if v['id'] == 'original']
        if name == 'ternary_marginal_collision':
            C = rec['C']
            relation(C['vertex_order'], FRAME | es(C['original_internal_edges']) | {edge(int(v), h) for v, hs in C['actual_attachments'].items() for h in hs}, beta, C['ordered_contacts'], item['complete_C_tuples'], 'negative_control_C')
            cr = {tuple(w['tuple']) for w in row['C_complete_tuples']}
            ac, bc = item['literal_a_b_colors']
            guarded = {t for t in cr if t[0] != ac and t[1] != bc and t[2] != bc}
            assert set(map(tuple, item['complete_guarded_ternary_fiber'])) == guarded == set()
            marginals = [{t[i] for t in cr} for i in range(3)]
            marginal_join = {t for t in product(*marginals) if t[0] != ac and t[1] != bc and t[2] != bc}
            assert marginal_join
            special[name] = dict(control_index=item['control_index'], row_index=item['row_index'], fake_marginal_tuples=[list(t) for t in sorted(marginal_join)], exact_fibre=[])
        elif name == 'nonempty_omission_empty_original_joint':
            omitted, = [v for v in row['variants'] if v['omitted_original_edge'] == item['omitted_original_edge']]
            assert item['nonempty_omission_joint'] == omitted['complete_joint_tuples']
            assert not original['complete_joint_tuples'] and item['empty_original_joint'] == []
            relation(rec['vertex_order'], es(omitted['actual_edges']), beta, rec['complete_port_order'], item['nonempty_omission_joint'], 'negative_control_omission_joint')
            special[name] = dict(control_index=item['control_index'], row_index=item['row_index'], omitted_original_edge=item['omitted_original_edge'])
        else:
            omitted, = [v for v in row['variants'] if v['id'] == 'a_x']
            assert item['complete_original_joint'] == original['complete_joint_tuples']
            assert item['complete_a_x_omission_joint'] == omitted['complete_joint_tuples']
            j = relation(rec['vertex_order'], es(original['actual_edges']), beta, rec['complete_port_order'], item['complete_original_joint'], 'negative_control_original_joint')
            k = relation(rec['vertex_order'], es(omitted['actual_edges']), beta, rec['complete_port_order'], item['complete_a_x_omission_joint'], 'negative_control_ax_omission_joint')
            t = tuple(item['omitted_only_tuple'])
            assert t in k-j
            validate(rec['vertex_order'], item['omitted_only_full_coloring'], es(omitted['actual_edges']), beta, rec['complete_port_order'], t)
            assert {(t[0],t[1],t[5]) for t in j} == {(t[0],t[1],t[5]) for t in k} == set(map(tuple,item['equal_a_b_u_projection']))
            special[name] = dict(control_index=item['control_index'], row_index=item['row_index'], omitted_only_tuple=list(t), original_tuple_count=len(j), omission_tuple_count=len(k), equal_a_b_u_projection=item['equal_a_b_u_projection'])
        special[name]['literal_boundary'] = list(beta)
        special[name]['original_edges'] = rec['original_edges']
        special[name]['vertex_order'] = rec['vertex_order']
        special[name]['complete_port_order'] = rec['complete_port_order']
        special[name]['stored_counterexample_and_full_witnesses'] = item
    return dict(original_control_Sigma_counts=dict(image_counts), counterexamples=special)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', '--root', dest='root', type=Path, default=Path('/tmp/math-task-d2-snapshot'))
    args = parser.parse_args()
    out = Path(__file__).resolve().parent
    started = time.monotonic()
    paths = [args.root/'artifacts/c5_excess_two_mixed_core_four_spoke_mixed12/observations.json', args.root/'artifacts/c5_excess_two_mixed_core_single_spoke/observations.json']
    hashes = {str(p.relative_to(args.root)): sha256(p.read_bytes()).hexdigest() for p in paths}
    data, source = [json.loads(p.read_text()) for p in paths]
    # Independent C5 restricted-growth pattern domain.
    rows = tuple(sorted({normalized(q)[0] for q in product(COLORS, repeat=5) if all(q[a] != q[b] for a,b in FRAME)}))
    assert tuple(map(tuple, data['pattern_order'])) == rows == tuple(map(tuple, source['pattern_order']))
    identity = audit_identity(data, source, rows)
    print(json.dumps(dict(identity=identity, elapsed_seconds=round(time.monotonic()-started,3))), flush=True)
    graphs = audit_graphs(data, rows)
    def count_serialized_colorings(value):
        if isinstance(value, list):
            return sum(map(count_serialized_colorings, value))
        if isinstance(value, dict):
            return sum(int(k in ('coloring', 'omitted_only_full_coloring')) + count_serialized_colorings(v)
                       for k, v in value.items())
        return 0
    stored_coloring_fields = count_serialized_colorings(data)
    assert stored_coloring_fields == COUNTS['stored_colorings_validated']
    COUNTS['all_serialized_coloring_fields_accounted_for'] = stored_coloring_fields
    after = {str(p.relative_to(args.root)): sha256(p.read_bytes()).hexdigest() for p in paths}
    assert hashes == after
    result = dict(status='PASS', all_checks_passed=True, summary=dict(COUNTS), frozen_input_root=str(args.root), input_sha256=hashes, source_artifact_bytes_preserved=True,
                  independent_method='stdlib-only MRV literal-color backtracking plus independent source-filtered identity/rotation/support/schedule enumeration; no production enumerator, join or validator imports',
                  identity=identity, graphs=graphs, counts=dict(COUNTS), elapsed_seconds=round(time.monotonic()-started,3),
                  limits=['Fixed serialized graph controls only; no disk, criticality or Sigma933/941 source realization proved.',
                          'Short-support, minimal-core saturation, two-spoke ternary K5, Gallai palette and unused-color conservation are paper dependencies; schedule screen audits their finite necessary algebra only.',
                          'Mixed12 subtype remains open at 22/26 necessary frames; epsilon>=3, general exits, topology formalization and K-infinity=K-at-most5 are not proved.'])
    (out/'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+'\n')
    (out/'counterexamples.json').write_text(json.dumps(graphs['counterexamples'], ensure_ascii=False, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'], counts=result['counts'], elapsed_seconds=result['elapsed_seconds']), sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
