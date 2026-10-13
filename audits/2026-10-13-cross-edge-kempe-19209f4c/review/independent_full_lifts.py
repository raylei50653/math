#!/usr/bin/env python3
"""Independent direct-product replay. Reads inputs; writes only stdout.

No project checker is imported. In particular, edge fibres are reconstructed
from the literal G-e edges by Cartesian products of all free vertex colours.
"""
import argparse
import copy
import gzip
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def require(value, context):
    if not value:
        raise ValueError(context)


def edge_set(edges):
    result = {tuple(sorted(edge)) for edge in edges}
    require(len(result) == len(edges), 'duplicate edge')
    require(all(a != b for a, b in result), 'loop')
    return result


def enumerate_lifts(vertices, edges, boundary, beta, colours):
    indices = {vertex: i for i, vertex in enumerate(vertices)}
    require(len(indices) == len(vertices), 'duplicate vertex')
    pinned = dict(zip(boundary, beta))
    require(len(pinned) == len(boundary) == len(beta), 'boundary size')
    free = [vertex for vertex in vertices if vertex not in pinned]
    edge_indices = [(indices[a], indices[b]) for a, b in sorted(edges)]
    result = []
    for values in product(colours, repeat=len(free)):
        assignment = pinned | dict(zip(free, values))
        lift = tuple(assignment[v] for v in vertices)
        if all(lift[a] != lift[b] for a, b in edge_indices):
            result.append(lift)
    return sorted(result)


def compare_lifts(actual, supplied, context):
    claimed = [tuple(lift) for lift in supplied]
    require(len(claimed) == len(set(claimed)), context + ': duplicate full lift')
    require(actual == sorted(claimed), context + ': full lift mismatch')


def induced_components(vertices, edges, assignment, pair):
    remaining = {v for v in vertices if assignment[v] in pair}
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    parts = []
    while remaining:
        start = min(remaining)
        remaining.remove(start)
        stack = [start]
        reached = {start}
        while stack:
            for neighbour in adjacency[stack.pop()] & remaining:
                remaining.remove(neighbour)
                reached.add(neighbour)
                stack.append(neighbour)
        parts.append(sorted(reached))
    return parts


def check_kempe(wheel, row, h_lifts, colours):
    vertices = wheel['h_vertices']
    edges = edge_set(wheel['h_edges'])
    boundary = set(wheel['B'])
    records = row['pointwise_h_records']
    compare_lifts(h_lifts, [r['h_lift'] for r in records], wheel['id'] + ': pointwise coverage')
    pair_count = 0
    move_count = 0
    for record in records:
        assignment = dict(zip(vertices, record['h_lift']))
        rim = [assignment[u] for u in wheel['U']]
        require(record['rim'] == rim, wheel['id'] + ': rim colours')
        require(record['rim_color_count'] == len(set(rim)), wheel['id'] + ': rim count')
        supplied_pairs = record['Kempe']['color_pair_records']
        require([r['colors'] for r in supplied_pairs] == [list(p) for p in combinations(colours, 2)], 'pair domain')
        all_reductions = []
        for pair_record in supplied_pairs:
            pair = pair_record['colors']
            parts = induced_components(vertices, edges, assignment, pair)
            require(parts == pair_record['components'], wheel['id'] + ': actual bichromatic components')
            expected_moves = []
            for component_index, part in enumerate(parts):
                if boundary & set(part):
                    continue
                swapped = {v: (sum(pair) - assignment[v] if v in part else assignment[v]) for v in vertices}
                lift = [swapped[v] for v in vertices]
                new_rim_count = len({swapped[u] for u in wheel['U']})
                expected_moves.append({'component_index': component_index,
                                       'new_rim_color_count': new_rim_count,
                                       'switched_H_lift': lift})
                if len(set(rim)) == 4 and new_rim_count == 3:
                    all_reductions.append({'color_pair': pair,
                                           'component_index': component_index,
                                           'switched_H_lift': lift})
            require(expected_moves == pair_record['boundary_fixed_single_component_moves'], 'single component moves')
            pair_count += 1
            move_count += len(expected_moves)
        require(all_reductions == record['Kempe']['all_rim4_to_rim3_single_moves'], 'all one-swap reductions')
    return pair_count, move_count


def check_adjacent_transport(graph, g_rows):
    vertices = graph['g_vertices']
    indices = {v: i for i, v in enumerate(vertices)}
    wheel_by_v = {w['v']: w for w in [graph] + graph['other_degree5_wheels']}
    fibre_by_edge = {tuple(f['edge']): f for f in graph['edge_fibres']}
    expected_adjacent = sorted(e for e in edge_set(graph['g_edges']) if all(v in wheel_by_v for v in e))
    require([tuple(e) for e in graph['adjacent_degree5_center_edges']] == expected_adjacent, 'adjacent degree5 edge domain')
    result = {'rejected_adjacent_edge_rows': 0, 'triggered_adjacent_edge_rows': 0,
              'transported_full_lifts': 0}

    def zero_zero(wheel, k, row_index):
        edge = tuple(sorted((wheel['v'], wheel['U'][k])))
        return [tuple(lift) for lift in fibre_by_edge[edge]['rows'][row_index]['cells'][0]]

    for v, w in expected_adjacent:
        left_wheel, right_wheel = wheel_by_v[v], wheel_by_v[w]
        i, j = left_wheel['U'].index(w), right_wheel['U'].index(v)
        for row_index, g_lifts in enumerate(g_rows):
            if g_lifts:
                continue
            result['rejected_adjacent_edge_rows'] += 1
            left = zero_zero(left_wheel, (i+2) % 5, row_index) + zero_zero(left_wheel, (i+3) % 5, row_index)
            right = zero_zero(right_wheel, (j+2) % 5, row_index) + zero_zero(right_wheel, (j+3) % 5, row_index)
            middle = fibre_by_edge[(v, w)]['rows'][row_index]['cells'][1]
            require(len(left) == len(set(left)) and len(right) == len(set(right)), 'literal union must be disjoint')
            transported_middle = []
            transported_right = []
            for source in left:
                mid = list(source)
                mid[indices[v]] = mid[indices[w]]
                transported_middle.append(tuple(mid))
                right_rim = [mid[indices[u]] for u in right_wheel['U']]
                require(len(set(right_rim)) == 4, 'rejected middle rim must use four colours')
                repeated_indices = [k for k in range(5) if right_rim[(k-1) % 5] == right_rim[(k+1) % 5]]
                require(len(repeated_indices) == 1, 'unique repeated-pair 00 spoke')
                k = repeated_indices[0]
                require(k in ((j+2) % 5, (j+3) % 5), 'right branch index')
                target = list(mid)
                target[indices[w]] = target[indices[right_wheel['U'][k]]]
                transported_right.append(tuple(target))
                require(all(source[indices[x]] == target[indices[x]] for x in vertices if x not in (v, w)), 'transport preserves all other original colours')
            compare_lifts(sorted(transported_middle), middle, graph['id'] + ': literal middle transport')
            compare_lifts(sorted(transported_right), right, graph['id'] + ': complete composed transport')
            require(len(set(transported_middle)) == len(left) and len(set(transported_right)) == len(left), 'transport injectivity')
            result['transported_full_lifts'] += len(left)
            result['triggered_adjacent_edge_rows'] += bool(left)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=Path(__file__).resolve().parents[1] / 'controls/certificate.json.gz')
    parser.add_argument('--negative-controls', action='store_true', help='Explicitly create temporary corrupted copies and check rejection; original remains read-only')
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    data = json.loads(gzip.decompress(raw))
    if args.negative_controls:
        results = []
        for name in ('drop_nonempty_J_lift', 'populate_empty_J_cell', 'drop_H_lift'):
            damaged = copy.deepcopy(data)
            first_cells = damaged['graphs'][0]['edge_fibres'][0]['rows'][0]['cells']
            if name == 'drop_nonempty_J_lift':
                first_cells[3].pop()
            elif name == 'populate_empty_J_cell':
                first_cells[0] = copy.deepcopy(first_cells[3])
            else:
                damaged['graphs'][0]['rows'][0]['h_lifts'].pop()
            with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as temporary:
                bad = Path(temporary) / 'bad.json.gz'
                bad.write_bytes(gzip.compress(json.dumps(damaged).encode(), mtime=0))
                run = subprocess.run([sys.executable, '-B', str(Path(__file__).resolve()), '--certificate', str(bad)], capture_output=True, text=True)
                require(run.returncode != 0, 'corruption was accepted: ' + name)
                results.append({'negative': name, 'returncode': run.returncode,
                                'diagnostic': run.stderr.strip().splitlines()[-1], 'status': 'triggered and holds'})
        require(args.certificate.read_bytes() == raw, 'negative controls changed original')
        print(json.dumps({'source_sha256': hashlib.sha256(raw).hexdigest(), 'negative_controls': results, 'source_unchanged': True}, sort_keys=True, indent=2))
        return
    colours = data['colors']
    betas = data['beta_domain']
    cell_domain = data['J_cell_domain']
    require(colours == [0, 1, 2, 3], 'colour domain')
    require(cell_domain == [[0, 0], [0, 1], [1, 0], [1, 1]], 'cell domain')
    require(len(betas) == 10 and len({tuple(p) for p in betas}) == 10, 'ten-row domain')
    counts = {'graphs': 0, 'G_rows': 0, 'G_lifts': 0, 'wheel_H_rows': 0,
              'wheel_H_lifts': 0, 'wheels': 0, 'edge_fibres': 0, 'J_cells': 0,
              'empty_J_cells': 0, 'J_lifts': 0, 'Kempe_component_partitions': 0,
              'Kempe_boundary_fixed_moves': 0, 'rejected_adjacent_edge_rows': 0,
              'triggered_adjacent_edge_rows': 0, 'transported_full_lifts': 0}
    per_graph = []
    for graph in data['graphs']:
        counts['graphs'] += 1
        name = graph['id']
        vertices = graph['g_vertices']
        boundary = graph['B']
        require(boundary == data['B'], name + ': B')
        edges = edge_set(graph['g_edges'])
        require([r['beta'] for r in graph['rows']] == betas, name + ': G row domain')
        g_rows = []
        for beta, row in zip(betas, graph['rows']):
            lifts = enumerate_lifts(vertices, edges, boundary, beta, colours)
            compare_lifts(lifts, row['g_lifts'], name + ': G')
            require(row['rejected_by_G'] == (not lifts), name + ': rejection flag')
            g_rows.append(lifts)
            counts['G_rows'] += 1
            counts['G_lifts'] += len(lifts)
        require([bool(x) for x in g_rows] == graph['sigma_g'], name + ': Sigma flags')
        require(sum((1 << i) for i, row in enumerate(g_rows) if row) == graph['sigma_g_integer_in_declared_beta_order'], name + ': Sigma mask')
        degree5 = sorted(v for v in vertices if v not in boundary and sum(v in e for e in edges) == 5)
        require(degree5 == graph['all_interior_degree5_centers'], name + ': degree5 domain')
        wheels = [graph] + graph['other_degree5_wheels']
        require(sorted(w['v'] for w in wheels) == degree5, name + ': complete wheel domain')
        for wheel in wheels:
            counts['wheels'] += 1
            require(wheel['g_vertices'] == vertices and edge_set(wheel['g_edges']) == edges, name + ': same literal G')
            h_vertices = [v for v in vertices if v != wheel['v']]
            h_edges = {e for e in edges if wheel['v'] not in e}
            require(h_vertices == wheel['h_vertices'] and h_edges == edge_set(wheel['h_edges']), name + ': literal centre deletion')
            require([r['beta'] for r in wheel['rows']] == betas, name + ': H row domain')
            for i, (beta, row) in enumerate(zip(betas, wheel['rows'])):
                compare_lifts(g_rows[i], row['g_lifts'], wheel['id'] + ': repeated G row')
                lifts = enumerate_lifts(h_vertices, h_edges, boundary, beta, colours)
                compare_lifts(lifts, row['h_lifts'], wheel['id'] + ': H')
                counts['wheel_H_rows'] += 1
                counts['wheel_H_lifts'] += len(lifts)
                pair_count, move_count = check_kempe(wheel, row, lifts, colours)
                counts['Kempe_component_partitions'] += pair_count
                counts['Kempe_boundary_fixed_moves'] += move_count
        edge_fibres = graph['edge_fibres']
        expected_edges = sorted(e for e in edges if any(v in degree5 for v in e))
        require([tuple(f['edge']) for f in edge_fibres] == expected_edges, name + ': complete incident-edge domain')
        graph_J_lifts = 0
        for fibre in edge_fibres:
            edge = tuple(fibre['edge'])
            opposite = fibre['opposite']
            require(len(opposite) == 2 and opposite[0] != opposite[1], 'opposite domain')
            incident_faces = [face for face in graph['g_faces'] if any(set((face[i], face[(i+1) % len(face)])) == set(edge) for i in range(len(face)))]
            require(len(incident_faces) == 2 and all(len(face) == 3 for face in incident_faces), name + ': two incident triangular faces')
            require(sorted(set(incident_faces[0]) - set(edge) | (set(incident_faces[1]) - set(edge))) == sorted(opposite), name + ': original opposite pins')
            require([r['beta'] for r in fibre['rows']] == betas, name + ': J row domain')
            counts['edge_fibres'] += 1
            indices = {v: i for i, v in enumerate(vertices)}
            for beta, row in zip(betas, fibre['rows']):
                lifts = enumerate_lifts(vertices, edges - {edge}, boundary, beta, colours)
                actual = [[] for _ in cell_domain]
                for lift in lifts:
                    a = int(lift[indices[edge[0]]] != lift[indices[edge[1]]])
                    b = int(lift[indices[opposite[0]]] != lift[indices[opposite[1]]])
                    actual[2*a+b].append(lift)
                require(len(row['cells']) == 4, 'four cells including empties')
                for i, cell in enumerate(actual):
                    compare_lifts(cell, row['cells'][i], name + ': J ' + str(edge) + '/' + str(beta) + '/' + str(cell_domain[i]))
                    counts['J_cells'] += 1
                    counts['empty_J_cells'] += not cell
                    counts['J_lifts'] += len(cell)
                    graph_J_lifts += len(cell)
        transport = check_adjacent_transport(graph, g_rows)
        for key, value in transport.items():
            counts[key] += value
        per_graph.append({'id': name, 'wheels': len(wheels), 'edge_fibres': len(edge_fibres),
                          'G_lifts': sum(map(len, g_rows)), 'J_lifts': graph_J_lifts,
                          'adjacent_transport': transport})
    require(counts['edge_fibres'] == 61 and counts['J_cells'] == 2440, 'fixed 61-edge / 2440-cell domain')
    require(args.certificate.read_bytes() == raw, 'input bytes changed during read-only check')
    print(json.dumps({'status': 'triggered and holds', 'method': 'independent direct Cartesian product of free vertex colours',
                      'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'counts': counts, 'graphs': per_graph,
                      'target_minimum_source': 'not triggered', 'writes': 'stdout only'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
