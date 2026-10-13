#!/usr/bin/env python3
"""Complete fixed original fibres, joints, collision certificates and K3,3 control."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = list(itertools.product(range(4), repeat=2))
TARGET = {0: [0, 1, 2, 1, 2], 1: [0, 1, 2, 0, 2], 3: [0, 1, 0, 2, 1]}
B = list(range(5))
ROOTS = [5, 6]
P = list(range(7, 11))
Q = list(range(11, 15))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def connected(vertices, edges):
    vertices = set(vertices)
    seen = {min(vertices)}
    while True:
        more = seen | {b if a in seen else a for a, b in edges
                       if a in vertices and b in vertices and (a in seen or b in seen)}
        if more == seen:
            return seen == vertices
        seen = more


def neighbors(vertices, edges):
    return {v: {b if a == v else a for a, b in edges if v in (a, b)} for v in vertices}


def lifts(vertices, edges, colors):
    """Lexicographic DFS on all original coordinates."""
    nbr = neighbors(vertices, edges)
    colors = dict(colors)
    answer = []
    def visit(j):
        if j == len(vertices):
            answer.append([colors[v] for v in vertices])
            return
        v = vertices[j]
        forbidden = {colors[w] for w in nbr[v] if w in colors}
        for color in range(4):
            if color not in forbidden:
                colors[v] = color
                visit(j + 1)
                del colors[v]
    visit(0)
    return answer


def brute_piece(vertices, edges, colors):
    """Independent Cartesian enumeration, no recursive DFS or list pruning."""
    answer = []
    for values in itertools.product(range(4), repeat=len(vertices)):
        c = dict(colors)
        c.update(zip(vertices, values))
        if all(c[a] != c[b] for a, b in edges if a in vertices or b in vertices):
            answer.append(list(values))
    return answer


def graph():
    edges = [(b, (b + 1) % 5) for b in B] + [(5, 0), (6, 4)]
    for vs, arc in [(P, [0, 1, 2]), (Q, [2, 3, 4])]:
        a, b, c = arc
        edges += list(zip(vs, vs[1:])) + list(zip(vs, [5, 5, 6, 6]))
        edges += [(vs[0], a), (vs[0], b), (vs[1], a),
                  (vs[2], c), (vs[3], b), (vs[3], c)]
    return sorted({tuple(sorted(e)) for e in edges})


def minor(edges, attachment):
    # All vertices and witness edges belong to the one explicit graph.
    sides = ([[[2, 3], [5, 7, 8, 1], [6]], [[9], [10], Q]] if attachment == 3 else
             [[[0, 4], [6, 10, 9, 1], [5]], [[8], [7], Q]])
    bags = [sorted(b) for side in sides for b in side]
    assert sum(map(len, bags)) == len(set().union(*map(set, bags)))
    assert all(connected(bag, edges) for bag in bags)
    witnesses = []
    for i in range(3):
        for j in range(3, 6):
            links = [list(e) for e in edges
                     if (e[0] in bags[i] and e[1] in bags[j])
                     or (e[1] in bags[i] and e[0] in bags[j])]
            assert links
            witnesses.append({'bag_pair': [i, j], 'original_edge': links[0]})
    return {'actual_Q_attachment': attachment, 'branch_sides': [bags[:3], bags[3:]], 'nine_original_adjacencies': witnesses,
            'conclusion': 'nonplanar; no disk rotation exists', 'status': 'triggered and holds'}


def generate():
    base = json.loads((HERE / 'BASE.json').read_bytes())
    for item in base['inputs']:
        data = (HERE / 'frozen' / item['path']).read_bytes()
        assert len(data) == item['bytes'] and sha(data) == item['sha256'], item['path']
    old_path = 'audits/2026-10-11-n2-long-mask-sync/high-contact/observations.json'
    old = json.loads((HERE / 'frozen' / old_path).read_bytes())
    original = old['named_full_fibre_controls'][0]
    table = [row['beta'] for row in original['rows']]
    assert len(table) == 10 and all(q in table for q in TARGET.values())
    edges = graph()
    nbr = neighbors(range(15), edges)
    assert [len(nbr[v]) for v in ROOTS] == [5, 5]
    assert all(len(nbr[v]) == 4 for v in P + Q)
    H = ROOTS + P + Q
    assert all(connected([w for w in H if w != v], edges) for v in H)
    assert set().union(*(nbr[v] & set(B) for v in H)) == set(B)
    records = []
    local_cell_count = local_empty = local_tuple_count = global_tuple_count = 0
    collision_trigger_count = one_sided_joint_count = cross_joint_count = 0
    local_masks = []
    for vs in [P, Q]:
        contacts = [[v for v in vs if root in nbr[v]] for root in ROOTS]
        attachments = {str(v): sorted(nbr[v] & set(B)) for v in vs}
        W = [sorted(set().union(*(nbr[v] & set(B) for v in cs))) for cs in contacts]
        rows = []
        for beta in table:
            cells = []
            collision_flags = []
            for pin in PINS:
                fixed = dict(enumerate(beta)); fixed.update(zip(ROOTS, pin))
                cell = lifts(vs, edges, fixed)
                assert cell == brute_piece(vs, edges, fixed)
                # Exact rectangle law for the retained four-contact path.
                reject_rectangle = pin[0] not in {beta[b] for b in W[0]} and pin[1] not in {beta[b] for b in W[1]}
                assert bool(cell) == (not reject_rectangle)
                collision = not reject_rectangle
                collision_flags.append(collision)
                if collision:
                    assert cell
                    collision_trigger_count += 1
                cells.append(cell)
                local_empty += not bool(cell)
                local_tuple_count += len(cell)
                local_cell_count += 1
            rows.append({'beta': beta, 'full_lifts_by_ordered_pins': cells,
                         'external_collision_filter': collision_flags})
        mask = [i for i, beta in TARGET.items()
                if not next(row for row in rows if row['beta'] == beta)['full_lifts_by_ordered_pins'][15]]
        assert mask == [0, 1, 3]
        local_masks.append(mask)
        records.append({'name': 'P' if vs == P else 'Q', 'original_vertices': vs,
                        'ordered_roots': ROOTS, 'ordered_original_contacts': contacts,
                        'actual_attachments': attachments, 'actual_support': sorted(set().union(*map(set, attachments.values()))),
                        'contact_boundary_sets_W_by_root': W, 'literal_shared_contacts': [],
                        'root_incidence_by_ordered_root': list(map(len, contacts)),
                        'diagonal_rejection_mask': mask, 'rows': rows})
    # Recover the old original path tuple coordinates and pins exactly (only labels renamed).
    assert records[0]['rows'] == [dict(row, external_collision_filter=[bool(c) for c in row['full_lifts_by_ordered_pins']]) for row in original['rows']]
    joint_rows = []
    for row_index, beta in enumerate(table):
        E = [sorted(set(range(4)) - {beta[b] for b in nbr[root] & set(B)}) for root in ROOTS]
        assert list(map(len, E)) == [3, 3]
        cells = []
        global_row = []
        for pin in PINS:
            external = all(pin[j] in E[j] for j in range(2))
            pc = records[0]['rows'][row_index]['full_lifts_by_ordered_pins'][4 * pin[0] + pin[1]]
            qc = records[1]['rows'][row_index]['full_lifts_by_ordered_pins'][4 * pin[0] + pin[1]]
            joined = [list(pin) + a + b for a in pc for b in qc] if external else []
            fixed = dict(enumerate(beta)); fixed.update(zip(ROOTS, pin))
            direct = [list(pin) + row for row in lifts(P + Q, edges, fixed)] if external else []
            assert joined == direct
            for lift in joined:
                full = dict(enumerate(beta)); full.update(zip(ROOTS + P + Q, lift))
                assert all(full[a] != full[b] for a, b in edges)
            global_row += joined
            cells.append({'external_factor': external, 'full_original_lifts': joined})
        # Direct full-graph DFS independently chooses both roots and all piece vertices.
        assert global_row == lifts(ROOTS + P + Q, edges, dict(enumerate(beta)))
        global_tuple_count += len(global_row)
        assert global_row
        assert not cells[15]['full_original_lifts']
        accepted_pins = [list(pin) for pin, cell in zip(PINS, cells) if cell['full_original_lifts']]
        forbidden_bounds = []
        for piece_index, rec in enumerate(records):
            for fixed_root in range(2):
                free_root = 1 - fixed_root
                for fixed_color in range(4):
                    forbidden = []
                    for free_color in range(4):
                        pin = [0, 0];pin[fixed_root] = fixed_color;pin[free_root] = free_color
                        if not rec['rows'][row_index]['full_lifts_by_ordered_pins'][4 * pin[0] + pin[1]]:
                            forbidden.append(free_color)
                    assert len(forbidden) <= rec['root_incidence_by_ordered_root'][free_root]
                    forbidden_bounds.append({'piece': rec['name'], 'fixed_root': ROOTS[fixed_root],
                                             'fixed_color': fixed_color, 'free_root': ROOTS[free_root],
                                             'forbidden': forbidden, 'bound': rec['root_incidence_by_ordered_root'][free_root]})
        X = [[sorted(set(E[j]) & {beta[b] for b in rec['contact_boundary_sets_W_by_root'][j]}) for j in range(2)] for rec in records]
        one_sided = []
        for ci, rec in enumerate(records):
            for fixed_root in range(2):
                free_root = 1 - fixed_root
                for fixed_color in X[ci][fixed_root]:
                    assert rec['root_incidence_by_ordered_root'][free_root] >= 2
                    other = records[1 - ci]
                    assert other['root_incidence_by_ordered_root'][free_root] < len(E[free_root])
                    witness_pins = [p for p in accepted_pins if p[fixed_root] == fixed_color]
                    assert witness_pins
                    pin = witness_pins[0]
                    lift = cells[4 * pin[0] + pin[1]]['full_original_lifts'][0]
                    one_sided.append({'piece': rec['name'], 'fixed_root': ROOTS[fixed_root], 'collision_color': fixed_color,
                                      'ordered_pins': pin, 'complete_original_lift': lift})
                    one_sided_joint_count += 1
        cross = []
        for ci in range(2):
            for x in X[ci][0]:
                for y in X[1 - ci][1]:
                    assert cells[4 * x + y]['full_original_lifts']
                    cross.append({'r_collision_piece': records[ci]['name'], 's_collision_piece': records[1-ci]['name'],
                                  'ordered_pins': [x, y], 'complete_original_lift': cells[4*x+y]['full_original_lifts'][0]})
                    cross_joint_count += 1
        joint_rows.append({'beta': beta, 'root_external_available_colors': E,
                           'complete_accepting_ordered_pins': accepted_pins,
                           'full_lifts_by_ordered_pins': cells, 'complete_global_relation_accepts': True,
                           'forbidden_column_capacity_checks': forbidden_bounds,
                           'collision_sets_by_piece_then_root': X,
                           'one_sided_collision_capacity_joints': one_sided,
                           'cross_collision_joints': cross})
    return {'scope': 'one original explicitly declared double-long gluing; calibration only, no source enumeration',
            'frozen_head': base['head'], 'input_hashes_verified': len(base['inputs']),
            'original_boundary': B, 'ordered_original_roots': ROOTS, 'original_vertices': list(range(15)),
            'original_edges': edges, 'original_H_vertex_order': ROOTS + P + Q,
            'literal_frame_rows': table, 'target_row_labels': TARGET, 'ordered_pin_order': PINS,
            'external_root_spokes': [[5, 0], [6, 4]], 'original_nonadjacent_roots': True,
            'original_full_degrees': {str(v): len(nbr[v]) for v in range(15)},
            'H_biconnected': True, 'full_B_touch': True, 'unary_count': 0,
            'same_original_piece_records': records, 'same_original_joint_rows': joint_rows,
            'diagonal_union_mask': [0, 1, 3], 'diagonal_only_claim_status': 'counterexample',
            'joint_lemma_calibration_status': 'triggered and holds',
            'K33_minors': [minor(edges, h) for h in [3, 4]], 'disk_rotation_status': 'impossible by checked original K3,3 minor',
            'full_target_source_status': 'not triggered',
            'missing_target_hypotheses': ['planar disk embedding impossible', 'all ten rows accepted; required rejected rows absent', 'full Sigma933/941 criticality absent'],
            'counts': {'fixed_original_gluings': 1, 'local_pieces': 2, 'local_ambient_cells': local_cell_count,
                       'local_empty_cells': local_empty, 'local_full_tuples': local_tuple_count,
                       'joint_ambient_cells': len(table) * 16, 'complete_global_full_lifts': global_tuple_count,
                       'local_collision_triggered_cells': collision_trigger_count,
                       'one_sided_collision_capacity_joints': one_sided_joint_count,
                       'cross_collision_joints': cross_joint_count, 'complete_target_sources': 0}}


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--write', action='store_true')
    modes.add_argument('--check', action='store_true')
    parser.add_argument('--artifact', type=Path, default=HERE / 'observations.json')
    args = parser.parse_args()
    result = generate()
    data = (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()
    if args.write:
        with args.artifact.open('xb') as out:
            out.write(data)
    else:
        assert args.artifact.read_bytes() == data, 'artifact mismatch'
    print(json.dumps({'mode': 'write' if args.write else 'check', 'bytes': len(data),
                      'sha256': sha(data), 'counts': result['counts']}, sort_keys=True))


if __name__ == '__main__':
    main()
