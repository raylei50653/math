#!/usr/bin/env python3
"""Named full-fibre/signature/minor controls; no source search or planarity oracle."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
TARGET = {0: [0, 1, 2, 1, 2], 1: [0, 1, 2, 0, 2],
          3: [0, 1, 0, 2, 1]}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_frozen():
    base = json.loads((AUDIT / 'BASE.json').read_bytes())
    for item in base['inputs']:
        data = (AUDIT / 'frozen' / (item['path'] + '.snapshot')).read_bytes()
        assert len(data) == item['bytes'] and sha(data) == item['sha256'], item['path']
    path = 'artifacts/c5_excess_two_arc_component_slack/observations.json'
    original = json.loads((AUDIT / 'frozen' / (path + '.snapshot')).read_bytes())
    table = [r['beta'] for r in original['records'][0]['components'][0]['rows']]
    assert len(table) == 10 and all(q in table for q in TARGET.values())
    return table, base['head'], len(base['inputs'])


def signatures():
    rows = [TARGET[i] for i in (0, 1, 3)]
    vertices = [tuple(row[b] for row in rows) for b in range(5)]
    edges = [tuple(3-row[e]-row[(e+1) % 5] for row in rows) for e in range(5)]
    assert len(set(edges)) == 5
    pairs = []
    for e, f in itertools.product(range(5), repeat=2):
        if all(edges[e][i] != edges[f][i] for i in range(3)):
            third = tuple(3-edges[e][i]-edges[f][i] for i in range(3))
            assert third not in vertices
            pairs.append({'edges': [e, f], 'third_signature': third})
    assert {(p['edges'][0], p['edges'][1]) for p in pairs} == {
        (0, 2), (2, 0), (0, 3), (3, 0)}
    triples = []
    for triple in itertools.combinations(range(5), 3):
        rainbow = [len({edges[e][i] for e in triple}) == 3 for i in range(3)]
        assert not all(rainbow)
        triples.append({'edges': triple, 'row_rainbow': rainbow})
    return {'boundary_vertex_signatures': vertices,
            'boundary_edge_T_signatures': edges,
            'all_row_distinct_ordered_pairs': pairs,
            'all_ten_distinct_edge_triples': triples}


def fibre_record(name, vertices, roots, region_edges, expected, table):
    boundary = [(i, (i+1) % 5) for i in range(5)]
    edges = {tuple(sorted(e)) for e in boundary + region_edges}
    neighbors = {v: {b if a == v else a for a, b in edges if v in (a, b)}
                 for v in vertices}
    assert all(len(neighbors[v]) == 4 for v in vertices)
    contacts = [[v for v in vertices if root in neighbors[v]] for root in roots]
    assert not set(contacts[0]) & set(contacts[1])
    attachments = {v: sorted(neighbors[v] & set(range(5))) for v in vertices}
    tree_edges = [[a, b] for a, b in sorted(edges) if a in vertices and b in vertices]
    degree_c = {v: sum(v in e for e in tree_edges) for v in vertices}
    degree_h_two = [v for v in vertices
                    if degree_c[v] + sum(v in x for x in contacts) == 2]
    injective = len({tuple(attachments[v]) for v in degree_h_two}) == len(degree_h_two)
    assert injective
    rows = []
    for beta in table:
        cells = []
        for pins in itertools.product(range(4), repeat=2):
            colors = dict(enumerate(beta))
            colors.update(zip(roots, pins))
            lifts = []

            def visit(j):
                if j == len(vertices):
                    lifts.append([colors[v] for v in vertices])
                    return
                v = vertices[j]
                forbidden = {colors[w] for w in neighbors[v] if w in colors}
                for color in range(4):
                    if color not in forbidden:
                        colors[v] = color
                        visit(j+1)
                        del colors[v]

            visit(0)
            cells.append(lifts)
        rows.append({'beta': beta, 'full_lifts_by_ordered_pins': cells})
    by_beta = {tuple(row['beta']): row for row in rows}
    mask = [i for i in (0, 1, 3)
            if not by_beta[tuple(TARGET[i])]['full_lifts_by_ordered_pins'][15]]
    assert mask == expected
    return {'name': name, 'original_vertices': vertices, 'ordered_roots': roots,
            'original_edges': sorted(edges), 'ordered_original_contacts': contacts,
            'actual_attachments': attachments,
            'actual_support': sorted(set().union(*map(set, attachments.values()))),
            'root_incidence_total': sum(map(len, contacts)),
            'literal_shared_contacts': [], 'complete_degree_four': True,
            'C_internal_edges': tree_edges, 'C_degrees': degree_c,
            'all_contacts_C_leaves': all(degree_c[v] == 1
                                        for x in contacts for v in x),
            'H_degree_two_attachment_injection': injective,
            'diagonal_rejection_mask': mask,
            'status': 'counterexample' if expected else 'triggered and holds',
            'target_source_status': 'not triggered', 'rows': rows}


def minor_control():
    edges = {tuple(sorted(e)) for e in [(i, (i+1) % 5) for i in range(5)] +
             [(5, 0), (5, 1), (6, 0), (6, 1),
              (5, 7), (7, 6), (7, 2), (5, 8), (8, 6)]}
    bags = [[5, 8], [6], [0], [1], [7, 2, 3, 4]]
    assert len(set().union(*map(set, bags))) == sum(map(len, bags))
    for bag in bags:
        seen = {bag[0]}
        while True:
            expanded = seen | {w for v in seen for w in bag
                               if tuple(sorted((v, w))) in edges}
            if expanded == seen:
                break
            seen = expanded
        assert seen == set(bag)
    witnesses = []
    for a, b in itertools.combinations(range(5), 2):
        links = [e for e in sorted(edges)
                 if (e[0] in bags[a] and e[1] in bags[b]) or
                    (e[1] in bags[a] and e[0] in bags[b])]
        assert links
        witnesses.append({'bag_pair': [a, b], 'original_edge': links[0]})
    return {'name': 'common_two_spoke_edge_K5', 'original_edges': sorted(edges),
            'ordered_roots': [5, 6], 'mixed_C_path': [5, 7, 6],
            'mixed_Q_path': [5, 8, 6], 'outside_actual_attachment': [7, 2],
            'K5_branch_sets': bags, 'all_ten_original_adjacencies': witnesses,
            'status': 'triggered and holds', 'target_source_status': 'not triggered'}


def generate():
    table, head, frozen_count = verify_frozen()
    controls = [
        fibre_record('four_contact_long_path', [5, 6, 7, 8], [9, 10],
                     [(5, 6), (6, 7), (7, 8), (9, 5), (9, 6),
                      (10, 7), (10, 8), (5, 0), (5, 1), (6, 0),
                      (7, 2), (8, 1), (8, 2)], [0, 1, 3], table),
        fibre_record('four_leaf_contact_tree', [5, 6, 7, 8, 9], [10, 11],
                     [(5, 6), (5, 7), (5, 8), (5, 9), (10, 6), (10, 7),
                      (11, 8), (11, 9), (6, 0), (6, 1), (7, 1), (7, 2),
                      (8, 2), (8, 3), (9, 3), (9, 4)], [], table),
    ]
    return {'scope': 'named local full-fibre controls and literal signatures; no source search',
            'frozen_head': head, 'frozen_input_hashes_verified': frozen_count,
            'target_row_labels_and_literal_beta': TARGET,
            'ordered_pin_order': list(itertools.product(range(4), repeat=2)),
            'signature_controls': signatures(), 'named_full_fibre_controls': controls,
            'named_minor_control': minor_control(),
            'counts': {'local_controls': 2, 'rows': 20, 'ambient_cells': 320,
                       'empty_cells': sum(not cell for item in controls
                                          for row in item['rows']
                                          for cell in row['full_lifts_by_ordered_pins']),
                       'target_sources': 0}, 'target_source_status': 'not triggered'}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--artifact', type=Path, default=HERE / 'observations.json')
    args = parser.parse_args()
    result = generate()
    data = (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()
    if args.write:
        with args.artifact.open('xb') as handle:
            handle.write(data)
    else:
        assert args.artifact.read_bytes() == data, 'artifact mismatch'
    print(json.dumps({'mode': 'write' if args.write else 'check',
                      'bytes': len(data), 'sha256': sha(data),
                      'counts': result['counts']}, sort_keys=True))


if __name__ == '__main__':
    main()
