#!/usr/bin/env python3
"""Named leaf/root boundary witnesses and complete outside-slack join controls."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import checker

HERE = Path(__file__).resolve().parent
MAIN_SHA = '516c44fc1480002c4fe358ea5ce0cc69349d55ed463427c685db42ec887ec2a7'
CHECKER_SHA = 'bfc5bd286fad1deb684b3cf25290a8481f13eb81990127ff68ae8d7f5e68432d'
ROOTS = (9, 10)
ROWS = {0: (0, 1, 2, 1, 2), 1: (0, 1, 2, 0, 2), 3: (0, 1, 0, 2, 1)}


def require(value, message):
    if not value:
        raise ValueError(message)


def boundary_witnesses():
    result = []
    for h, matching, leaves in [(2, [[0, 1], [3, 4]], [[1, 2], [2, 3]]),
                                 (4, [[0, 1], [2, 3]], [[3, 4], [4, 0]])]:
        for swap in (False, True):
            schedule = dict(zip(ROOTS, reversed(matching) if swap else matching))
            entries = []
            for vertex, leaf in zip((5, 8), leaves):
                for owner in ROOTS:
                    T = schedule[owner]
                    closure = [b for b in range(5)
                               if all(q[b] in {q[t] for t in T} for q in ROWS.values())]
                    require(closure == sorted(T), 'spoke-edge closure is not itself')
                    witnesses = []
                    for label, q in ROWS.items():
                        for a in sorted({q[b] for b in leaf} - {q[b] for b in T}):
                            witnesses.append({'row_label': label, 'literal_beta': list(q),
                                              'owner_root': owner, 'owner_color_a': a,
                                              'original_leaf_contact_vertex': vertex,
                                              'original_root_contact_edge': [owner, vertex],
                                              'original_leaf_boundary_neighbors': leaf,
                                              'same_color_boundary_vertices': [b for b in leaf if q[b] == a],
                                              'literal_original_owner_spokes': [[owner, t] for t in T]})
                    require(witnesses, 'leaf/owner has no separating target row')
                    entries.append({'original_leaf_contact_vertex': vertex,
                                    'original_leaf_attachment_edge': leaf,
                                    'owner_root': owner, 'owner_spoke_support': T,
                                    'three_row_owner_spoke_closure': closure,
                                    'all_literal_row_color_witnesses': witnesses})
            result.append({'omitted_named_vertex_h': h, 'root_ownership_swapped': swap,
                           'original_root_spoke_schedule': {str(r): schedule[r] for r in ROOTS},
                           'two_original_leaf_attachment_edges': leaves,
                           'all_leaf_owner_cases': entries,
                           'status': 'triggered and holds', 'target_source_status': 'not triggered'})
    return result


def outside_controls(main):
    pieces = {p['name']: p for p in main['complete_local_pieces']}
    out = []
    for graph in main['complete_same_row_graph_controls']:
        if not graph['complete_degree_five_roots']:
            continue
        long = pieces[graph['literal_long_piece']]
        short = pieces[graph['literal_short_piece']]
        long_vertices = set(long['original_vertices'])
        edges = graph['original_edges']
        exterior_edges = [e for e in edges if not set(e) & long_vertices]
        root_rows = []
        for row_index, row in enumerate(graph['rows']):
            beta = row['literal_beta']
            for owner in ROOTS:
                other = ROOTS[1 - ROOTS.index(owner)]
                exterior_order = [other] + short['original_vertices']
                global_order = [other] + long['original_vertices'] + short['original_vertices']
                T = sorted(b for root, b in graph['original_root_spokes'] if root == owner)
                T_other = sorted(b for root, b in graph['original_root_spokes'] if root == other)
                contacts = long['ordered_original_contacts'][ROOTS.index(owner)]
                W = sorted(set().union(*(set(long['actual_attachments'][str(v)]) for v in contacts)))
                k_other_long = len(long['ordered_original_contacts'][ROOTS.index(other)])
                k_other_short = len(short['ordered_original_contacts'][ROOTS.index(other)])
                require(k_other_long >= 2, 'outside slack needs at least two other-root long incidences')
                require(4 - len(T_other) == k_other_short + k_other_long - 1 > k_other_short,
                        'outside root degree/list slack arithmetic')
                cells = []
                for a in range(4):
                    fixed = {**dict(enumerate(beta)), owner: a}
                    exterior = checker.product_fibres(exterior_order, exterior_edges, fixed)
                    legal = a not in {beta[b] for b in T}
                    require(bool(exterior) == legal, 'legal pinned root has no full outside coloring')
                    collided = a in {beta[b] for b in W}
                    joined = []
                    for ext in exterior:
                        other_color = ext[0]
                        pins = (a, other_color) if owner == ROOTS[0] else (other_color, a)
                        pin_index = checker.PINS.index(pins)
                        local = long['rows'][row_index]['cells'][pin_index]['full_fibre']
                        if collided:
                            require(local, 'root/contact collision did not extend this complete exterior')
                        joined.extend([[other_color] + lift + ext[1:] for lift in local])
                    joined.sort()
                    direct = checker.dfs_fibres(global_order, edges, fixed)
                    require(joined == direct, 'outside complete join differs from whole-graph root-fixed DFS')
                    if legal and collided:
                        require(joined, 'sidewise used-color escape failed')
                    cells.append({'owner_root_color': a, 'owner_spokes_legal': legal,
                                  'owner_contact_boundary_collision': collided,
                                  'full_exterior_fibre': exterior,
                                  'full_same_row_global_join': joined,
                                  'sidewise_escape_status':
                                      'triggered and holds' if legal and collided else 'not triggered'})
                root_rows.append({'row_index': row_index, 'literal_beta': beta, 'owner_root': owner,
                                  'other_root': other, 'T_owner_original_spoke_support': T,
                                  'W_owner_original_long_contact_boundary_neighbors': W,
                                  'full_original_exterior_order': exterior_order,
                                  'full_original_global_order_excluding_pinned_owner': global_order,
                                  'all_four_owner_color_cells': cells})
        out.append({'original_graph_name': graph['name'], 'original_edges': edges,
                    'literal_deleted_long_vertices': long['original_vertices'],
                    'original_exterior_edges': exterior_edges,
                    'full_original_exterior_vertices': list(range(5)) + list(ROOTS) + short['original_vertices'],
                    'complete_outside_and_global_fibres': root_rows,
                    'status': 'triggered and holds', 'target_source_status': 'not triggered',
                    'scope': 'fixed whole-graph calibration of legal-owner-pin outside slack and same-pin restoration'})
    return out


def generate():
    main_bytes = (HERE / 'observations.json').read_bytes()
    require(hashlib.sha256(main_bytes).hexdigest() == MAIN_SHA, 'main observations drift')
    require(hashlib.sha256((HERE / 'checker.py').read_bytes()).hexdigest() == CHECKER_SHA, 'main checker drift')
    main = json.loads(main_bytes)
    witnesses = boundary_witnesses()
    controls = outside_controls(main)
    cells = [c for g in controls for r in g['complete_outside_and_global_fibres']
             for c in r['all_four_owner_color_cells']]
    return {'schema': 'n2-one-long-sidewise-slack-controls-v1',
            'main_observations_sha256': MAIN_SHA, 'main_checker_sha256': CHECKER_SHA,
            'scope': 'fixed named boundary cases plus complete outside/full-graph fibres; no source search',
            'boundary_leaf_owner_witnesses': witnesses,
            'complete_outside_slack_controls': controls,
            'source_exclusion_claimed_by_this_finite_artifact': False,
            'target_source_status': 'not triggered',
            'counts': {'boundary_spoke_schedules_including_root_swap': len(witnesses),
                       'named_leaf_owner_cases': sum(len(s['all_leaf_owner_cases']) for s in witnesses),
                       'literal_boundary_row_color_witnesses':
                           sum(len(c['all_literal_row_color_witnesses']) for s in witnesses
                               for c in s['all_leaf_owner_cases']),
                       'fixed_degree_five_root_graphs': len(controls),
                       'full_exterior_owner_color_cells': len(cells),
                       'empty_exterior_cells': sum(not c['full_exterior_fibre'] for c in cells),
                       'full_exterior_lifts': sum(len(c['full_exterior_fibre']) for c in cells),
                       'whole_graph_root_fixed_DFS_comparisons': len(cells),
                       'sidewise_escape_trigger_cells':
                           sum(c['sidewise_escape_status'] == 'triggered and holds' for c in cells),
                       'target_sources': 0}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--artifact', type=Path, default=HERE / 'side_observations.json')
    args = parser.parse_args()
    result = generate()
    data = (json.dumps(result, sort_keys=True, indent=2) + '\n').encode()
    if args.write:
        with args.artifact.open('xb') as stream:
            stream.write(data)
    else:
        require(args.artifact.read_bytes() == data, 'sidewise artifact mismatch')
    print(json.dumps({'mode': 'write' if args.write else 'check', 'bytes': len(data),
                      'sha256': hashlib.sha256(data).hexdigest(), 'counts': result['counts']}, sort_keys=True))


if __name__ == '__main__':
    main()
