#!/usr/bin/env python3
"""Fixed original-vertex controls; no source search, planarity or criticality oracle.

The local enumerator uses an exhaustive Cartesian product.  A separate MRV DFS
computes whole-graph fibres, with original roots either pinned or unpinned.
--check only reads.  --write refuses to replace any existing artifact.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = tuple(range(4))
B = tuple(range(5))
ROOTS = (9, 10)
PINS = tuple(itertools.product(COLORS, repeat=2))
TARGET = {0: (0, 1, 2, 1, 2), 1: (0, 1, 2, 0, 2),
          3: (0, 1, 0, 2, 1)}
BOUNDARY = tuple(sorted({tuple(sorted((b, (b + 1) % 5))) for b in B}))
SP0 = 'audits/2026-10-11-n2-long-mask-sync/high-contact/observations.json'


def require(value, message):
    if not value:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inputs():
    base = json.loads((HERE / 'BASE.json').read_bytes())
    for item in base['inputs']:
        data = (HERE / 'frozen' / item['path']).read_bytes()
        require(len(data) == item['bytes'] and sha(data) == item['sha256'],
                'frozen input drift: ' + item['path'])
    old = json.loads((HERE / 'frozen' / SP0).read_bytes())
    original = old['named_full_fibre_controls'][0]
    require(original['name'] == 'four_contact_long_path', 'old control identity')
    table = [tuple(row['beta']) for row in original['rows']]
    # Independently recover all ten proper C5 color partitions with <= 4 colors.
    canonical = []
    for q in itertools.product(COLORS, repeat=5):
        if all(q[a] != q[b] for a, b in BOUNDARY) and partition(q) == q:
            canonical.append(q)
    require(table == canonical and len(table) == 10, 'boundary table incomplete')
    return base, original, table


def partition(values):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in values)


def named_blocks(names, values):
    key = partition(values)
    return [[name for name, block in zip(names, key) if block == k]
            for k in range(max(key) + 1)]


def permutation(source, target):
    require(partition(source) == partition(target), 'different named partitions')
    mapping = dict(zip(source, target))
    require(len(set(mapping.values())) == len(mapping), 'non-bijective transport')
    for a, b in zip(sorted(set(COLORS) - mapping.keys()),
                    sorted(set(COLORS) - set(mapping.values()))):
        mapping[a] = b
    result = tuple(mapping[x] for x in COLORS)
    require(sorted(result) == list(COLORS), 'incomplete color permutation')
    return result


def product_fibres(order, edges, fixed):
    """Local Cartesian product, independent of global graph DFS."""
    out = []
    for values in itertools.product(COLORS, repeat=len(order)):
        assignment = {**fixed, **dict(zip(order, values))}
        if all(assignment[a] != assignment[b] for a, b in edges):
            out.append(list(values))
    return out


def dfs_fibres(order, edges, fixed):
    """MRV whole-graph DFS, checking every original edge including fixed edges."""
    adjacency = {v: set() for v in set(order) | set(fixed)}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    if any(a in fixed and b in fixed and fixed[a] == fixed[b] for a, b in edges):
        return []
    colors = dict(fixed)
    out = []

    def visit(remaining):
        if not remaining:
            out.append([colors[v] for v in order])
            return
        choices = []
        for v in remaining:
            available = tuple(c for c in COLORS
                              if all(colors.get(w) != c for w in adjacency[v]))
            choices.append((len(available), v, available))
        _, vertex, available = min(choices)
        for color in available:
            colors[vertex] = color
            visit(remaining - {vertex})
            del colors[vertex]

    visit(set(order))
    return sorted(out)


def make_piece(name, vertices, internal, attachments, contacts):
    edges = set(tuple(sorted(e)) for e in internal)
    for v, neighbors in attachments.items():
        edges.update(tuple(sorted((v, b))) for b in neighbors)
    for root, group in zip(ROOTS, contacts):
        edges.update(tuple(sorted((root, v))) for v in group)
    support = sorted(set().union(*map(set, attachments.values())))
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)}
                 for v in vertices}
    require(all(len(neighbors[v]) == 4 for v in vertices), name + ': degree four')
    require(all(tuple(sorted((a, b))) in BOUNDARY
                for att in attachments.values() for a, b in itertools.combinations(att, 2)),
            name + ': nonconsecutive attachment pair')
    common = sorted(set(contacts[0]) & set(contacts[1]))
    collision = {}
    for v in vertices:
        external = sorted(neighbors[v] - set(vertices))
        for a, b in itertools.combinations(external, 2):
            collision.setdefault((a, b), []).append(v)
    return {'name': name, 'original_vertices': list(vertices),
            'original_constraint_edges': [list(e) for e in sorted(edges)],
            'ordered_roots': list(ROOTS), 'ordered_original_contacts': contacts,
            'actual_attachments': {str(v): attachments[v] for v in vertices},
            'actual_support': support, 'literal_shared_contacts': common,
            'root_incidence_total': sum(map(len, contacts)),
            'complete_original_degree_four': True,
            'interface_order': support + list(ROOTS),
            'collision_edges_with_original_vertex_witnesses':
                [{'interface_pair': list(e), 'original_vertices': collision[e]}
                 for e in sorted(collision)]}


def local_table(piece, table):
    rows = []
    vertices = piece['original_vertices']
    edges = piece['original_constraint_edges']
    interface = piece['interface_order']
    representatives = {}
    classes = []
    for row_index, beta in enumerate(table):
        cells = []
        for pin_index, pin in enumerate(PINS):
            fixed = {**dict(enumerate(beta)), **dict(zip(ROOTS, pin))}
            eta = [fixed[v] for v in interface]
            key = partition(eta)
            lifts = product_fibres(vertices, edges, fixed)
            collided = [item['interface_pair']
                        for item in piece['collision_edges_with_original_vertex_witnesses']
                        if fixed[item['interface_pair'][0]] == fixed[item['interface_pair'][1]]]
            require(not collided or lifts, piece['name'] + ': collision slack violation')
            if key not in representatives:
                representatives[key] = (len(classes), eta, lifts)
                classes.append({'partition_id': len(classes),
                                'named_blocks': named_blocks(interface, eta),
                                'representative_row_index': row_index,
                                'representative_ordered_pins': list(pin),
                                'full_representative_fibre': lifts})
            class_id, ref_eta, ref_lifts = representatives[key]
            pi = permutation(ref_eta, eta)
            transported = sorted([[pi[x] for x in lift] for lift in ref_lifts])
            require(transported == lifts, piece['name'] + ': full fibre transport mismatch')
            cells.append({'ordered_pins': list(pin), 'partition_id': class_id,
                          'literal_interface_colors': eta,
                          'representative_to_literal_color_permutation': list(pi),
                          'same_color_collision_pairs': collided,
                          'full_fibre': lifts})
        rows.append({'row_index': row_index, 'literal_beta': list(beta), 'cells': cells})
    by_beta = {tuple(row['literal_beta']): row for row in rows}
    mask = [i for i, beta in TARGET.items() if not by_beta[beta]['cells'][15]['full_fibre']]
    return {**piece, 'full_named_partition_representatives': classes,
            'diagonal_rejection_mask': mask, 'rows': rows,
            'partition_transport_status': 'triggered and holds',
            'collision_necessary_condition_status': 'triggered and holds',
            'target_source_status': 'not triggered'}


def partition_catalogue(table):
    """Every named support of size 3,4,5; never collapse four/five to Eq/Diff."""
    catalogue = []
    for size in (3, 4, 5):
        for support in itertools.combinations(B, size):
            interface = support + ROOTS
            groups = {}
            for row, beta in enumerate(table):
                for pins in PINS:
                    eta = tuple(beta[b] for b in support) + pins
                    key = partition(eta)
                    groups.setdefault(key, []).append((row, pins, eta))
            entries = []
            for key, members in sorted(groups.items()):
                representative = members[0]
                entries.append({'named_blocks': named_blocks(interface, representative[2]),
                                'representative_row_index': representative[0],
                                'representative_ordered_pins': list(representative[1]),
                                'all_ambient_cells':
                                    [{'row_index': row, 'ordered_pins': list(pins),
                                      'representative_to_literal_color_permutation':
                                          list(permutation(representative[2], eta))}
                                     for row, pins, eta in members]})
            require(sum(len(e['all_ambient_cells']) for e in entries) == 160,
                    'incomplete interface catalogue')
            catalogue.append({'actual_support': list(support), 'interface_order': list(interface),
                              'named_partition_count': len(entries), 'partitions': entries})
    return catalogue


def joined_control(long_piece, short_piece, table, spoke_name, spokes):
    # Fixed literal graphs. Only the four-spoke controls have degree-five roots.
    external = sorted(set(BOUNDARY) | {tuple(sorted(e)) for e in spokes})
    edges = sorted(set(external) |
                   {tuple(e) for p in (long_piece, short_piece)
                    for e in p['original_constraint_edges']})
    piece_order = long_piece['original_vertices'] + short_piece['original_vertices']
    order = list(ROOTS) + piece_order
    rows = []
    contact_set = set().union(*map(set, long_piece['ordered_original_contacts']))
    W = sorted(set().union(*(set(long_piece['actual_attachments'][str(v)])
                           for v in contact_set)))
    T = sorted({b for root, b in spokes})
    escape_witnesses = []
    for row_index, beta in enumerate(table):
        cells = []
        reconstructed_global = []
        for pin_index, pins in enumerate(PINS):
            fixed = {**dict(enumerate(beta)), **dict(zip(ROOTS, pins))}
            external_ok = all(fixed[a] != fixed[b] for a, b in external)
            left = long_piece['rows'][row_index]['cells'][pin_index]['full_fibre']
            right = short_piece['rows'][row_index]['cells'][pin_index]['full_fibre']
            joined = sorted([a + b for a, b in itertools.product(left, right)]) if external_ok else []
            direct = dfs_fibres(piece_order, edges, fixed)
            require(joined == direct, 'same-row same-pin whole-graph mismatch')
            reconstructed_global.extend([list(pins) + lift for lift in joined])
            cells.append({'ordered_pins': list(pins), 'external_factor': external_ok,
                          'full_same_row_join': joined})
        reconstructed_global.sort()
        direct_global = dfs_fibres(order, edges, dict(enumerate(beta)))
        require(reconstructed_global == direct_global, 'unpinned global DFS mismatch')
        for color in sorted({beta[b] for b in W} - {beta[b] for b in T}):
            pin_index = PINS.index((color, color))
            fibre = cells[pin_index]['full_same_row_join']
            require(fibre, 'common-color collision escape failed')
            witness = list(beta) + [color, color] + fibre[0]
            witness_order = list(B) + list(ROOTS) + piece_order
            assignment = dict(zip(witness_order, witness))
            require(all(assignment[a] != assignment[b] for a, b in edges),
                    'common-color full witness missed original edge')
            collision_contacts = [v for v in sorted(contact_set)
                                  if color in {beta[b] for b in long_piece['actual_attachments'][str(v)]}]
            require(collision_contacts, 'missing original root-boundary collision')
            escape_witnesses.append({'row_index': row_index, 'literal_beta': list(beta),
                                     'ordered_pins': [color, color],
                                     'original_long_collision_contacts': collision_contacts,
                                     'full_original_vertex_order': witness_order,
                                     'full_original_coloring': witness,
                                     'complete_same_pin_fibre_size': len(fibre)})
        rows.append({'row_index': row_index, 'literal_beta': list(beta),
                     'cells': cells, 'full_global_lifts': direct_global})
    accepted = [row['literal_beta'] for row in rows if row['full_global_lifts']]
    return {'name': long_piece['name'] + '_with_fixed_short_' + spoke_name,
            'original_edges': [list(e) for e in edges], 'original_root_spokes': spokes,
            'ordered_roots': list(ROOTS), 'full_original_interior_order': order,
            'pinned_original_piece_order': piece_order, 'literal_short_piece': short_piece['name'],
            'literal_long_piece': long_piece['name'], 'complete_degree_five_roots':
                all(sum(root in e for e in edges) == 5 for root in ROOTS),
            'rows': rows, 'complete_accepted_boundary_rows': accepted,
            'same_row_common_color_escape': {'T_original_spoke_support': T,
                                             'W_original_contact_boundary_neighbors': W,
                                             'status': 'triggered and holds' if escape_witnesses else 'not triggered',
                                             'all_available_color_full_witnesses': escape_witnesses},
            'same_row_join_status': 'triggered and holds',
            'source_qualification': {'target_status': 'not triggered',
                                     'disk_rotation': 'not supplied or checked',
                                     'Sigma_criticality': 'not checked',
                                     'complete_source_contract': 'not asserted'},
            'scope': 'fixed full-graph join calibration, not an N2 source witness'}


def signature_closure_table(table):
    entries = []
    for mask in range(32):
        T = [b for b in B if mask & (1 << b)]
        target_sets = {str(i): [b for b in B if beta[b] in {beta[t] for t in T}]
                       for i, beta in TARGET.items()}
        closure = [b for b in B if all(b in allowed for allowed in target_sets.values())]
        all_rows = [b for b in B if all(beta[b] in {beta[t] for t in T} for beta in table)]
        # Every possible named W is checked, not just singleton membership.
        for wmask in range(32):
            W = [b for b in B if wmask & (1 << b)]
            condition = all({beta[b] for b in W} <= {beta[t] for t in T}
                            for beta in TARGET.values())
            require(condition == (set(W) <= set(closure)), 'closure set equivalence')
        entries.append({'T_mask_in_boundary_order': mask, 'T_named_vertices': T,
                        'target_rows_available_point_sets': target_sets,
                        'three_row_signature_closure': closure,
                        'all_ten_row_signature_closure': all_rows,
                        'all_32_named_W_equivalences_checked': True})
    require(entries[0]['three_row_signature_closure'] == [], 'empty T closure')
    return {'status': 'triggered and holds',
            'meaning': 'q_i(W) subset q_i(T) for every target row iff W subset listed closure',
            'target_source_status': 'not triggered', 'all_32_T_subsets': entries}


def path_palette_witness(piece):
    """Literal bridge palettes certify all three empty diagonal path fibres."""
    vertices = piece['original_vertices']
    edges = piece['original_constraint_edges']
    result = []
    for row_label, beta in TARGET.items():
        fixed = {**dict(enumerate(beta)), **dict(zip(ROOTS, (3, 3)))}
        lists = []
        for v in vertices:
            forbidden = {fixed[b if a == v else a] for a, b in edges
                         if v in (a, b) and (b if a == v else a) in fixed}
            lists.append(sorted(set(COLORS) - forbidden))
        palettes = [lists[0]]
        require(len(palettes[0]) == 1, 'first bridge palette')
        for allowed in lists[1:-1]:
            require(set(palettes[-1]) <= set(allowed), 'bridge palette recurrence')
            palettes.append(sorted(set(allowed) - set(palettes[-1])))
            require(len(palettes[-1]) == 1, 'bridge singleton palette')
        require(palettes[-1] == lists[-1], 'last bridge palette')
        for j, allowed in enumerate(lists):
            incident = palettes[max(0, j - 1):min(j + 1, len(palettes))]
            require(set(allowed) == set().union(*map(set, incident)), 'list-palette union')
            require(sum(map(len, incident)) == len(set(allowed)), 'palette disjointness')
        result.append({'row_label': row_label, 'literal_beta': list(beta),
                       'ordered_pins': [3, 3], 'lists_in_original_vertex_order': lists,
                       'original_path_edges': [[a, b] for a, b in zip(vertices, vertices[1:])],
                       'disjoint_incident_bridge_palettes': palettes,
                       'empty_full_fibre': []})
    return result


def generate():
    base, old, table = inputs()
    path = [(5, 6), (6, 7), (7, 8)]
    contacts = [[5, 6], [7, 8]]
    specs = [('three_support_original_four_contact_path', {5: [0, 1], 6: [0], 7: [2], 8: [1, 2]}),
             ('four_support_four_contact_path', {5: [0, 1], 6: [0], 7: [3], 8: [2, 3]}),
             ('five_support_four_contact_path', {5: [0, 1], 6: [2], 7: [3], 8: [3, 4]})]
    longs = [local_table(make_piece(name, [5, 6, 7, 8], path, att, contacts), table)
             for name, att in specs]
    for new_row, old_row in zip(longs[0]['rows'], old['rows']):
        require(new_row['literal_beta'] == old_row['beta'], 'original row transport')
        require([c['full_fibre'] for c in new_row['cells']] == old_row['full_lifts_by_ordered_pins'],
                'original path full fibre drift')
    require(longs[0]['diagonal_rejection_mask'] == [0, 1, 3], 'original mask drift')
    short = local_table(make_piece('fixed_shared_contact_short', [11], [],
                                   {11: [3, 4]}, [[11], [11]]), table)
    require(short['diagonal_rejection_mask'] == [], 'short diagonal should accept')
    schedules = [('four_spokes', [(9, 0), (9, 4), (10, 1), (10, 2)]),
                 ('zero_spokes', []), ('one_spoke', [(9, 0)]),
                 ('two_spokes', [(9, 0), (10, 1)])]
    joins = [joined_control(piece, short, table, name, spokes)
             for piece in longs for name, spokes in schedules]
    catalogue = partition_catalogue(table)
    all_pieces = longs + [short]
    return {'schema': 'n2-one-long-complete-controls-v1', 'frozen_head': base['head'],
            'scope': 'fixed local fibres, complete named interface partitions, and direct same-row joins',
            'source_search_performed': False, 'source_exclusion_claimed': False,
            'target_source_status': 'not triggered', 'target_sources': 0,
            'literal_boundary_order': list(B), 'ordered_root_names': {'9': 'r', '10': 's'},
            'all_ten_boundary_rows': [list(q) for q in table],
            'ordered_pin_order': [list(p) for p in PINS],
            'target_literal_rows': {str(i): list(q) for i, q in TARGET.items()},
            'full_named_interface_catalogue': catalogue, 'complete_local_pieces': all_pieces,
            'literal_spoke_contact_signature_closure': signature_closure_table(table),
            'complete_same_row_graph_controls': joins,
            'permanent_diagonal_path_control': {
                'status': 'counterexample',
                'refuted_local_claim': 'degree four, distinct root contacts, and injective leaf attachments force a diagonal escape',
                'not_a_counterexample_to': 'complete N2 source exclusion or E-ARC2',
                'original_piece': longs[0]['name'],
                'three_named_empty_fibre_palette_witnesses': path_palette_witness(longs[0])},
            'counts': {'local_pieces': len(all_pieces), 'full_local_cells': len(all_pieces) * 160,
                       'empty_local_cells': sum(not c['full_fibre'] for p in all_pieces
                                                for r in p['rows'] for c in r['cells']),
                       'saved_local_lifts': sum(len(c['full_fibre']) for p in all_pieces
                                                for r in p['rows'] for c in r['cells']),
                       'full_same_row_join_cells': len(joins) * 160,
                       'empty_join_cells': sum(not c['full_same_row_join'] for g in joins
                                               for r in g['rows'] for c in r['cells']),
                       'global_unpinned_DFS_comparisons': len(joins) * 10,
                       'same_row_common_color_full_witnesses':
                           sum(len(g['same_row_common_color_escape']['all_available_color_full_witnesses'])
                               for g in joins),
                       'signature_T_subsets': 32, 'signature_T_W_equivalences': 1024,
                       'named_support_catalogues': len(catalogue),
                       'catalogued_ambient_cells': len(catalogue) * 160,
                       'target_sources': 0}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
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
    print(json.dumps({'mode': 'write' if args.write else 'check', 'sha256': sha(data),
                      'bytes': len(data), 'counts': result['counts']}, sort_keys=True))


if __name__ == '__main__':
    main()
