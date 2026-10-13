#!/usr/bin/env python3
"""Independent original-edge fibre/join and original-minor controls.

Frozen observations supply expected data, never executable enumeration code.
Local cells use Cartesian enumeration; the complete original graph uses DFS.
--check is read-only.  --write creates a new artifact exclusively.
"""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
BASE = '3097ef5be241b7777451a5ef8a663f3987d6b866'
UPSTREAM = 'audits/2026-10-13-n2-double-long-joint/controls/observations.json'
B, ROOTS = list(range(5)), [5, 6]
PIECES = [list(range(7, 11)), list(range(11, 15))]
H = ROOTS + PIECES[0] + PIECES[1]
PINS = list(itertools.product(range(4), repeat=2))
TARGET = {'0': [0, 1, 2, 1, 2], '1': [0, 1, 2, 0, 2], '3': [0, 1, 0, 2, 1]}
FRAME = 'literal colors 0,1,2,3; D=3; ordered B=(0,1,2,3,4)'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def declared_edges():
    # Original edges of the fixed retained control, independently declared.
    edges = [(j, (j + 1) % 5) for j in B] + [(5, 0), (6, 4)]
    for vs, (a, b, c) in zip(PIECES, [(0, 1, 2), (2, 3, 4)]):
        edges += list(zip(vs, vs[1:]))
        edges += list(zip(vs, [5, 5, 6, 6]))
        edges += [(vs[0], a), (vs[0], b), (vs[1], a),
                  (vs[2], c), (vs[3], b), (vs[3], c)]
    return sorted([min(a, b), max(a, b)] for a, b in edges)


EDGES = declared_edges()
SOURCE_ID = digest(encode({'B': B, 'roots': ROOTS, 'pieces': PIECES, 'edges': EDGES}))


def frozen_authority():
    base = json.loads((AUDIT / 'BASE.json').read_bytes())
    require(base['base'] == BASE, 'wrong frozen BASE')
    item = next(x for x in base['files'] if x['path'] == UPSTREAM)
    data = (AUDIT / 'frozen' / UPSTREAM).read_bytes()
    require(digest(data) == item['sha256'], 'frozen authority hash mismatch')
    authority = json.loads(data)
    require(authority['original_edges'] == EDGES, 'authority original edge mismatch')
    return authority, item['sha256']


def neighbors(edges):
    ans = {v: set() for v in B + H}
    for a, b in edges:
        ans[a].add(b)
        ans[b].add(a)
    return ans


def spanning_tree(vertices, edges):
    allowed = set(vertices)
    reached = {min(vertices)}
    tree = []
    while reached != allowed:
        candidates = [[a, b] for a, b in edges if a in allowed and b in allowed
                      and ((a in reached) != (b in reached))]
        require(bool(candidates), 'original bag disconnected')
        edge = candidates[0]
        tree.append(edge)
        reached.update(edge)
    return tree


def verify_original_source(source):
    require(source['ordered_boundary'] == B, 'ordered original boundary mismatch')
    require(source['ordered_roots'] == ROOTS, 'ordered original roots mismatch')
    require(source['pieces'] == PIECES, 'original piece vertices mismatch')
    require(source['original_edges'] == EDGES, 'missing or changed original edge')
    require(source['source_id'] == SOURCE_ID, 'source identity mismatch')


def local_fibre(vertices, beta, pin, edges=EDGES):
    fixed = dict(enumerate(beta))
    fixed.update(zip(ROOTS, pin))
    incident = [[a, b] for a, b in edges if a in vertices or b in vertices]
    result = []
    for values in itertools.product(range(4), repeat=len(vertices)):
        coloring = dict(fixed)
        coloring.update(zip(vertices, values))
        if all(coloring[a] != coloring[b] for a, b in incident):
            result.append(list(values))
    return result


def whole_graph_fibre(beta):
    """Direct lexicographic DFS, independent of the product-of-local-fibres."""
    adjacent = neighbors(EDGES)
    coloring = dict(enumerate(beta))
    require(all(coloring[a] != coloring[b] for a, b in EDGES if a in B and b in B),
            'improper original boundary')
    result = []

    def visit(j):
        if j == len(H):
            result.append([coloring[v] for v in H])
            return
        v = H[j]
        forbidden = {coloring[w] for w in adjacent[v] if w in coloring}
        for c in range(4):
            if c not in forbidden:
                coloring[v] = c
                visit(j + 1)
                del coloring[v]

    visit(0)
    return result


def bad_edges(beta, lift):
    require(len(lift) == len(H), 'incomplete original lift')
    coloring = dict(enumerate(beta))
    coloring.update(zip(H, lift))
    return [[a, b] for a, b in EDGES if coloring[a] == coloring[b]]


def verify_original_lift(beta, lift):
    require(all(c in range(4) for c in beta + lift), 'invalid color')
    require(not bad_edges(beta, lift), 'complete lift violates original edge')


def package(piece, row_index, beta, pin, fibre):
    return {'source_id': SOURCE_ID, 'frame': FRAME, 'piece': piece,
            'row_index': row_index, 'beta': beta, 'ordered_pins': list(pin),
            'full_lifts': fibre}


def join_packages(p, q):
    require(p['source_id'] == q['source_id'] == SOURCE_ID, 'mixed original source')
    require(p['frame'] == q['frame'] == FRAME, 'mixed literal color frame')
    require(p['row_index'] == q['row_index'] and p['beta'] == q['beta'], 'cross-row join')
    require(p['ordered_pins'] == q['ordered_pins'], 'mismatched root pins')
    require([p['piece'], q['piece']] == [0, 1], 'wrong piece ownership')
    beta, pin = p['beta'], p['ordered_pins']
    for part in [p, q]:
        require(part['full_lifts'] == local_fibre(PIECES[part['piece']], beta, pin),
                'incomplete or foreign original fibre')
    adjacent = neighbors(EDGES)
    if any(pin[j] == beta[b] for j, r in enumerate(ROOTS) for b in adjacent[r] & set(B)):
        return []
    joined = [pin + a + b for a in p['full_lifts'] for b in q['full_lifts']]
    for lift in joined:
        verify_original_lift(beta, lift)
    return joined


def minor_certificate(attachment):
    bags = ([[2, 3], [1, 5, 7, 8], [6], [9], [10], PIECES[1]] if attachment == 3
            else [[0, 4], [1, 6, 9, 10], [5], [8], [7], PIECES[1]])
    trees = [spanning_tree(bag, EDGES) for bag in bags]
    crosses = []
    for a in range(3):
        for b in range(3, 6):
            edge = next(e for e in EDGES if (e[0] in bags[a] and e[1] in bags[b])
                        or (e[1] in bags[a] and e[0] in bags[b]))
            if a == 0 and b == 5:
                edge = [3, 11] if attachment == 3 else [4, 13]
            crosses.append({'bag_pair': [a, b], 'original_edge': edge})
    return {'Q_actual_attachment': attachment, 'original_bags': bags,
            'original_bag_spanning_trees': trees, 'nine_original_cross_edges': crosses,
            'status': 'triggered and holds'}


def verify_minor(certificate):
    bags = certificate['original_bags']
    require(len(bags) == 6 and all(bags), 'wrong minor bags')
    flat = [v for bag in bags for v in bag]
    require(len(flat) == len(set(flat)), 'minor bags overlap')
    require(set(flat) <= set(B + H), 'non-original minor vertex')
    require(len(certificate['original_bag_spanning_trees']) == 6, 'missing bag tree')
    for bag, tree in zip(bags, certificate['original_bag_spanning_trees']):
        require(all(e in EDGES and set(e) <= set(bag) for e in tree), 'non-original bag edge')
        spanning_tree(bag, tree)
    crosses = certificate['nine_original_cross_edges']
    require([e['bag_pair'] for e in crosses] == [[a, b] for a in range(3) for b in range(3, 6)],
            'missing K3,3 adjacency')
    for record in crosses:
        a, b = record['bag_pair']
        u, v = record['original_edge']
        require([u, v] in EDGES, 'non-original minor cross edge')
        require((u in bags[a] and v in bags[b]) or (v in bags[a] and u in bags[b]),
                'minor cross edge has wrong endpoints')


def expect_rejection(name, reason, operation, evidence=None):
    try:
        operation()
    except ValueError as error:
        require(str(error) == reason, 'wrong rejection reason: ' + str(error))
        return {'name': name, 'status': 'rejected', 'reason': reason, 'evidence': evidence}
    raise ValueError('negative control incorrectly accepted: ' + name)


def verify_qualification(claim, certificates):
    for certificate in certificates:
        verify_minor(certificate)
    require(claim != 'qualified complete source', 'nonplanar graph cannot qualify')


def generate():
    authority, authority_sha = frozen_authority()
    rows = authority['literal_frame_rows']
    require(all(beta in rows for beta in TARGET.values()), 'missing target frame row')
    source = {'ordered_boundary': B, 'ordered_roots': ROOTS, 'pieces': PIECES,
              'original_edges': EDGES, 'source_id': SOURCE_ID}
    verify_original_source(source)
    adjacent = neighbors(EDGES)
    degrees = {str(v): len(adjacent[v]) for v in B + H}
    require([degrees[str(v)] for v in ROOTS] == [5, 5], 'root degree')
    require(all(degrees[str(v)] == 4 for v in PIECES[0] + PIECES[1]), 'ordinary degree')
    require(6 not in adjacent[5], 'roots adjacent')
    require(set().union(*(adjacent[v] & set(B) for v in H)) == set(B), 'not full B touch')
    spanning_tree(H, EDGES)
    for deleted in H:
        spanning_tree([v for v in H if v != deleted], EDGES)
    require(not any(a in PIECES[0] and b in PIECES[1] for a, b in EDGES), 'cross-piece edge')
    require(not any(v in PIECES[1] and w in PIECES[0] for v, w in EDGES), 'cross-piece edge')
    local = []
    packages = {}
    for c, vertices in enumerate(PIECES):
        contacts = [sorted(adjacent[root] & set(vertices)) for root in ROOTS]
        attachments = {str(v): sorted(adjacent[v] & set(B)) for v in vertices}
        w = [sorted(set().union(*(adjacent[v] & set(B) for v in contact))) for contact in contacts]
        per_row = []
        for row_index, beta in enumerate(rows):
            fibres = []
            for pin in PINS:
                fibre = local_fibre(vertices, beta, pin)
                index = 4 * pin[0] + pin[1]
                expected = authority['same_original_piece_records'][c]['rows'][row_index]['full_lifts_by_ordered_pins'][index]
                require(fibre == expected, 'independent local fibre differs from frozen authority')
                fibres.append(fibre)
                packages[c, row_index, pin] = package(c, row_index, beta, pin, fibre)
            per_row.append({'row_index': row_index, 'beta': beta, 'full_lifts_by_ordered_pins': fibres})
        local.append({'original_vertices': vertices, 'ordered_contacts': contacts,
                      'ownership_by_original_vertex': {str(v): sorted(adjacent[v] & set(ROOTS)) for v in vertices},
                      'actual_attachments': attachments, 'actual_support': sorted(set().union(*map(set, attachments.values()))),
                      'W_by_ordered_root': w, 'shared_contacts': sorted(set(contacts[0]) & set(contacts[1])),
                      'root_incidences': list(map(len, contacts)), 'rows': per_row})
    joints = []
    cuts = []
    for row_index, beta in enumerate(rows):
        joined_cells = []
        for pin in PINS:
            joined = join_packages(packages[0, row_index, pin], packages[1, row_index, pin])
            expected = authority['same_original_joint_rows'][row_index]['full_lifts_by_ordered_pins'][4 * pin[0] + pin[1]]['full_original_lifts']
            require(joined == expected, 'independent joint differs from frozen authority')
            joined_cells.append(joined)
        all_joined = [lift for cell in joined_cells for lift in cell]
        require(all_joined == whole_graph_fibre(beta), 'same-row product differs from direct original graph DFS')
        joints.append({'row_index': row_index, 'beta': beta, 'full_original_lifts_by_ordered_pins': joined_cells})
        if beta in TARGET.values():
            e = [sorted(set(range(4)) - {beta[b] for b in adjacent[root] & set(B)}) for root in ROOTS]
            s = []
            for c in range(2):
                x = [{beta[b] for b in local[c]['W_by_ordered_root'][j]} & set(e[j]) for j in range(2)]
                accepted = [list(pin) for pin in itertools.product(*e) if pin[0] in x[0] or pin[1] in x[1]
                            or (pin[0] == pin[1] and local[c]['shared_contacts'])]
                require(all(local[c]['rows'][row_index]['full_lifts_by_ordered_pins'][4 * a + b] for a, b in accepted),
                        'basic S cell has empty full fibre')
                s.append(accepted)
            overlap = [pin for pin in s[0] if pin in s[1]]
            require(bool(overlap), 'expected basic S-overlap control')
            require(all(not local[c]['rows'][row_index]['full_lifts_by_ordered_pins'][15] for c in range(2)),
                    'diagonal rejection control lost')
            pin = overlap[0]
            cuts.append({'target_row_label': next(k for k, q in TARGET.items() if q == beta),
                         'beta': beta, 'E_by_ordered_root': e, 'basic_S_by_piece': s, 'overlap': overlap,
                         'overlap_original_full_lift': joined_cells[4 * pin[0] + pin[1]][0],
                         'both_D_diagonal_fibres_empty': True,
                         'all_complete_joint_pins': [list(pin) for pin, cell in zip(PINS, joined_cells) if cell],
                         'status': 'triggered and holds'})
    certificates = [minor_certificate(a) for a in [3, 4]]
    for certificate in certificates:
        verify_minor(certificate)
    negative = []
    changed = copy.deepcopy(source)
    changed['original_edges'].remove([8, 9])
    negative.append(expect_rejection('omitted original edge in source', 'missing or changed original edge',
                                     lambda: verify_original_source(changed), {'deleted_original_edge': [8, 9]}))
    # A semantic witness newly admitted by forgetting one edge; original lift verification rejects it.
    deletion_witness = None
    for row_index, beta in enumerate(rows):
        for pin in PINS:
            q = packages[1, row_index, pin]
            if not q['full_lifts'] or not joints[row_index]['full_original_lifts_by_ordered_pins'][4 * pin[0] + pin[1]]:
                continue
            enlarged = local_fibre(PIECES[0], beta, pin, changed['original_edges'])
            original = packages[0, row_index, pin]['full_lifts']
            for p in enlarged:
                if p not in original:
                    lift = list(pin) + p + q['full_lifts'][0]
                    deletion_witness = {'beta': beta, 'ordered_pins': list(pin), 'foreign_lift': lift,
                                        'violated_original_edges': bad_edges(beta, lift)}
                    break
            if deletion_witness:
                break
        if deletion_witness:
            break
    require(deletion_witness is not None, 'no semantic deleted-edge witness')
    negative.append(expect_rejection('deleted-edge lift restoration', 'complete lift violates original edge',
                                     lambda: verify_original_lift(deletion_witness['beta'], deletion_witness['foreign_lift']), deletion_witness))
    first = next((row_index, pin) for row_index in range(len(rows)) for pin in PINS
                 if joints[row_index]['full_original_lifts_by_ordered_pins'][4 * pin[0] + pin[1]])
    row_index, pin = first
    p, q = packages[0, row_index, pin], packages[1, row_index, pin]
    foreign_frame = copy.deepcopy(q)
    # This permutation fixes both root pins but independently changes Q's frame.
    permutation = [0, 1, 3, 2]
    require(all(permutation[c] == c for c in pin), 'frame-control pins must be fixed')
    foreign_frame['frame'] = 'piecewise color permutation (2 3), forbidden independent frame'
    foreign_frame['beta'] = [permutation[c] for c in q['beta']]
    foreign_frame['full_lifts'] = sorted([[permutation[c] for c in lift] for lift in q['full_lifts']])
    require(foreign_frame['full_lifts'] == local_fibre(PIECES[1], foreign_frame['beta'], pin),
            'foreign-frame control must be complete in its own frame')
    mixed_lift = list(pin) + p['full_lifts'][0] + foreign_frame['full_lifts'][0]
    mixed_evidence = {'original_beta': p['beta'], 'foreign_beta': foreign_frame['beta'],
                      'permutation': permutation, 'ordered_pins': list(pin),
                      'mixed_frame_lift': mixed_lift, 'violated_original_edges': bad_edges(p['beta'], mixed_lift)}
    negative.append(expect_rejection('mixed color frames', 'mixed literal color frame',
                                     lambda: join_packages(p, foreign_frame), mixed_evidence))
    negative.append(expect_rejection('mixed-frame original-edge restoration', 'complete lift violates original edge',
                                     lambda: verify_original_lift(p['beta'], mixed_lift), mixed_evidence))
    cross = None
    for a, b in itertools.permutations(range(len(rows)), 2):
        for pins in PINS:
            pa, qb = packages[0, a, pins], packages[1, b, pins]
            for plift in pa['full_lifts']:
                for qlift in qb['full_lifts']:
                    lift = list(pins) + plift + qlift
                    violations = bad_edges(rows[a], lift)
                    if violations and all(pins[j] != rows[a][h] for j, root in enumerate(ROOTS) for h in adjacent[root] & set(B)):
                        cross = (pa, qb, {'P_beta': rows[a], 'Q_beta': rows[b], 'ordered_pins': list(pins),
                                         'cross_row_lift': lift, 'violated_original_edges_under_P_row': violations})
                        break
                if cross:
                    break
            if cross:
                break
        if cross:
            break
    require(cross is not None, 'no cross-row semantic witness')
    pa, qb, evidence = cross
    negative.append(expect_rejection('cross-row product', 'cross-row join', lambda: join_packages(pa, qb), evidence))
    negative.append(expect_rejection('cross-row original-edge restoration', 'complete lift violates original edge',
                                     lambda: verify_original_lift(evidence['P_beta'], evidence['cross_row_lift']), evidence))
    wrong_pins = copy.deepcopy(q)
    wrong_pins['ordered_pins'] = [(pin[0] + 1) % 4, pin[1]]
    negative.append(expect_rejection('different root pins', 'mismatched root pins', lambda: join_packages(p, wrong_pins)))
    foreign_fibre = copy.deepcopy(q)
    foreign_fibre['full_lifts'] = []
    negative.append(expect_rejection('erased accepted fibre', 'incomplete or foreign original fibre', lambda: join_packages(p, foreign_fibre)))
    minor_missing_edge = copy.deepcopy(certificates[0])
    minor_missing_edge['nine_original_cross_edges'][0]['original_edge'] = [2, 14]
    negative.append(expect_rejection('invented minor edge', 'non-original minor cross edge', lambda: verify_minor(minor_missing_edge)))
    negative.append(expect_rejection('nonplanar graph promoted to complete source', 'nonplanar graph cannot qualify',
                                     lambda: verify_qualification('qualified complete source', certificates)))
    local_cells = [cell for record in local for row in record['rows'] for cell in row['full_lifts_by_ordered_pins']]
    joint_cells = [cell for row in joints for cell in row['full_original_lifts_by_ordered_pins']]
    return {'base': BASE, 'authority_sha256': authority_sha,
            'scope': 'one fixed original graph; finite calibration only; no enumeration of qualified sources',
            'source': source, 'literal_frame': FRAME, 'literal_frame_rows': rows, 'target_rows': TARGET,
            'ordered_pin_order': PINS, 'original_H_tuple_order': H,
            'complete_original_degrees': degrees, 'epsilon': sum(degrees[str(v)] - 4 for v in H),
            'H_connected': True, 'H_biconnected': True, 'full_B_touch': True,
            'free_isolated_original_coordinates': [], 'free_coordinate_product_factor': 1,
            'local_complete_fibres': local, 'same_row_same_pin_complete_joints': joints,
            'basic_S_overlap_controls': cuts, 'original_K33_certificates': certificates,
            'negative_controls': negative, 'full_target_source_status': 'not triggered',
            'missing_full_target_hypotheses': ['planar disk impossible by original K3,3 minor',
                                               'all ten frame rows accepted; complete Sigma is 1023, neither 933 nor 941',
                                               'required three rejected rows absent; Sigma-criticality not certified'],
            'diagonal_only_weakened_claim_status': 'counterexample',
            'basic_LL_CUT_on_qualified_source_status': 'not triggered',
            'counts': {'fixed_original_graphs': 1, 'local_cells': len(local_cells),
                       'local_empty_cells': sum(not cell for cell in local_cells),
                       'local_complete_tuples': sum(map(len, local_cells)),
                       'joint_cells': len(joint_cells), 'joint_empty_cells': sum(not cell for cell in joint_cells),
                       'complete_original_lifts': sum(map(len, joint_cells)),
                       'target_rows_with_basic_S_overlap': len(cuts), 'checked_original_K33_minors': len(certificates),
                       'negative_controls_rejected': len(negative), 'qualified_full_target_sources': 0}}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--artifact', type=Path, default=HERE / 'observations.json')
    args = parser.parse_args()
    result = generate()
    data = encode(result)
    if args.write:
        with args.artifact.open('xb') as stream:
            stream.write(data)
    else:
        require(args.artifact.read_bytes() == data, 'artifact mismatch')
    print(json.dumps({'mode': 'write' if args.write else 'check', 'bytes': len(data),
                      'sha256': digest(data), 'counts': result['counts']}, sort_keys=True))


if __name__ == '__main__':
    main()
