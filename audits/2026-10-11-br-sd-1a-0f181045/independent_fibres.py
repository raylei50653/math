#!/usr/bin/env python3
"""Independently enumerate pinned assignments on full declared M edges.
No imports from the list solver; no list or palette reconstruction is used.
"""
from pathlib import Path
import argparse
import json
import sys


def all_graph_colorings(vertices, edges, pins):
    neighbors = {v: set() for v in vertices}
    for a, b in edges:
        if a == b or a not in neighbors or b not in neighbors:
            raise ValueError('invalid edge')
        neighbors[a].add(b)
        neighbors[b].add(a)
    assignment = dict(pins)
    if any(assignment[a] == assignment[b] for a, b in edges if a in assignment and b in assignment):
        return []
    order = sorted((v for v in vertices if v not in assignment), key=lambda v: (-len(neighbors[v]), v))
    answers = []
    def search(position):
        if position == len(order):
            answers.append([assignment[v] for v in vertices])
            return
        v = order[position]
        forbidden = {assignment[u] for u in neighbors[v] if u in assignment}
        for color in range(4):
            if color not in forbidden:
                assignment[v] = color
                search(position + 1)
        assignment.pop(v, None)
    search(0)
    return sorted(answers)


def require_same(observed, expected, label):
    if observed != expected:
        raise ValueError(f'{label}: complete fibre mismatch, observed={len(observed)}, expected={len(expected)}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--certificate', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text())
    checks = []
    for fixture in data['fixtures']:
        calibration = fixture['same_original_M_edge_calibration']
        vertices = calibration['M_vertex_order']
        edges = calibration['all_original_M_edges']
        beta = calibration['proper_beta']
        full = all_graph_colorings(vertices, edges, beta)
        require_same(full, calibration['complete_full_M_beta_lift_fibre'], fixture['name'] + '/full-M')
        sB = set(calibration['s_original_B_neighbors'])
        query_edges = [e for e in edges if not ('s' in e and any(v in sB for v in e))]
        queries = calibration['four_s_queries']
        if [q['s_color'] for q in queries] != [0, 1, 2, 3]:
            raise ValueError('four ordered query scopes missing')
        counts = []
        ix = [vertices.index(v) for v in fixture['vertex_order']]
        for query in queries:
            assignments = all_graph_colorings(vertices, query_edges, beta | {'s': query['s_color']})
            projected = sorted([[t[i] for i in ix] for t in assignments])
            require_same(projected, query['complete_C_coloring_fibre'], fixture['name'] + f"/s={query['s_color']}")
            counts.append(len(projected))
        checks.append({'fixture': fixture['name'], 'full_M_fibre_count': len(full), 'four_C_query_counts': counts,
                       'complete_fibres_match_direct_full_graph_enumeration': True})
    print(json.dumps({'scope': 'finite synthetic edge controls only', 'target_source_status': 'not triggered',
                      'checks': checks}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, IndexError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
