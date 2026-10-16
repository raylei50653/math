#!/usr/bin/env python3
"""Rebuild the labelled radius-two simplicial disk and local ear controls.

This finite calibration neither realizes a minimum source nor verifies the
arbitrary-size source lemmas used by the paper proof.  No graph library is used.
"""
import argparse
from collections import defaultdict
import hashlib
from itertools import combinations
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def edge(u, v):
    require(u != v, 'loop')
    return tuple(sorted((u, v)))


def vertex(prefix, i):
    return prefix + str(i % 5)


def face_row(name, kind, vertices, bit=None):
    row = {'id': name, 'kind': kind, 'oriented_vertices': list(vertices)}
    if bit is not None:
        row['bit'] = bit
    return row


def rebuild(faces):
    """Use complete literal face lists to reconstruct every edge and link."""
    require(len({row['id'] for row in faces}) == len(faces), 'face IDs repeat')
    triangles = [tuple(sorted(row['oriented_vertices'])) for row in faces]
    require(len(set(triangles)) == len(triangles), 'triangle repeats')
    edge_faces = defaultdict(list)
    edge_directions = defaultdict(list)
    link_edges = defaultdict(set)
    neighbours = defaultdict(set)
    face_by_id = {row['id']: row for row in faces}
    for row in faces:
        vs = row['oriented_vertices']
        require(len(vs) == len(set(vs)) == 3, 'non-triangular literal face')
        for i, u in enumerate(vs):
            v, w = vs[(i + 1) % 3], vs[(i + 2) % 3]
            edge_faces[edge(u, v)].append(row['id'])
            edge_directions[edge(u, v)].append([u, v])
            link_edges[u].add(edge(v, w))
            neighbours[u].update((v, w))
    for key, incident in edge_faces.items():
        require(1 <= len(incident) <= 2, 'non-manifold edge: ' + repr(key))
        if len(incident) == 2:
            directions = edge_directions[key]
            require(directions[0] == directions[1][::-1],
                    'inconsistent face orientation: ' + repr(key))
    vertices = sorted(neighbours)
    reached = {vertices[0]}
    pending = list(reached)
    while pending:
        for v in neighbours[pending.pop()]:
            if v not in reached:
                reached.add(v)
                pending.append(v)
    require(reached == set(vertices), 'disconnected vertex graph')
    adjacency = defaultdict(set)
    for incident in edge_faces.values():
        if len(incident) == 2:
            a, b = incident
            adjacency[a].add(b)
            adjacency[b].add(a)
    seen = {faces[0]['id']}
    pending = list(seen)
    while pending:
        for other in adjacency[pending.pop()]:
            if other not in seen:
                seen.add(other)
                pending.append(other)
    require(seen == set(face_by_id), 'disconnected dual face adjacency')
    return {'vertices': vertices, 'edge_faces': edge_faces,
            'neighbours': neighbours, 'link_edges': link_edges,
            'face_by_id': face_by_id}


def verify_link(data, u, order, closed):
    require(set(order) == data['neighbours'][u] and len(order) == len(set(order)),
            'incomplete literal neighbour order: ' + u)
    pairs = list(zip(order, order[1:]))
    if closed:
        pairs.append((order[-1], order[0]))
    require({edge(a, b) for a, b in pairs} == data['link_edges'][u],
            'incomplete facial link: ' + u)
    return {'vertex': u, 'degree': len(order), 'ordered_neighbours': order,
            'closed': closed, 'literal_link_edges': [list(e) for e in sorted(data['link_edges'][u])]}


def summary(faces, data):
    boundary = sorted(e for e, incident in data['edge_faces'].items() if len(incident) == 1)
    return {'vertex_count': len(data['vertices']),
            'edge_count': len(data['edge_faces']), 'face_count': len(faces),
            'euler_characteristic': len(data['vertices']) - len(data['edge_faces']) + len(faces),
            'vertices': data['vertices'],
            'edges': [{'vertices': list(e), 'literal_incident_faces': sorted(incident)}
                      for e, incident in sorted(data['edge_faces'].items())],
            'boundary_edges': [list(e) for e in boundary],
            'degrees': {u: len(data['neighbours'][u]) for u in data['vertices']}}


def compute():
    faces = []
    for i in range(5):
        faces.append(face_row('W' + str(i), 'complete_inner_wheel',
                              ('c', vertex('u', i), vertex('u', i + 1)), 1))
        faces.append(face_row('R' + str(i), 'exterior_face_on_original_rim_edge',
                              (vertex('u', i + 1), vertex('u', i), vertex('a', i)), 0))
        faces.append(face_row('K' + str(i), 'remaining_face_at_inner_rim_vertex',
                              (vertex('u', i), vertex('a', i - 1), vertex('a', i)), 1))
    data = rebuild(faces)
    disk = summary(faces, data)
    require((disk['vertex_count'], disk['edge_count'], disk['face_count'],
             disk['euler_characteristic']) == (11, 25, 15, 1), 'radius-two disk counts')
    boundary = [vertex('a', i) for i in range(5)]
    expected_boundary = {edge(boundary[i], boundary[(i + 1) % 5]) for i in range(5)}
    require({tuple(e) for e in disk['boundary_edges']} == expected_boundary,
            'outer boundary is not the literal C5')
    inner_links = [verify_link(data, 'c', [vertex('u', i) for i in range(5)], True)]
    outer_intervals = []
    for i in range(5):
        u, a = vertex('u', i), vertex('a', i)
        inner_links.append(verify_link(data, u,
            ['c', vertex('u', i - 1), vertex('a', i - 1), a, vertex('u', i + 1)], True))
        order = [vertex('a', i - 1), u, vertex('u', i + 1), vertex('a', i + 1)]
        link = verify_link(data, a, order, False)
        ids = ['K' + str(i), 'R' + str(i), 'K' + str((i + 1) % 5)]
        require({row['id'] for row in faces if a in row['oriented_vertices']} == set(ids),
                'outer interval misses an actual face')
        bits = [data['face_by_id'][name]['bit'] for name in ids]
        require(bits == [1, 0, 1], 'wrong literal outer interval bits')
        outer_intervals.append({'vertex': a, 'ordered_literal_faces': ids,
                                'bits': bits, 'complete_disk_link': link})
    require(all(row['degree'] == 5 for row in inner_links), 'inner six degrees')
    require({bit: sum(row['bit'] == bit for row in faces) for bit in (0, 1)} == {0: 5, 1: 10},
            'complete disk face-bit counts')
    disk.update({'oriented_boundary_cycle': boundary, 'literal_faces': faces,
                 'complete_inner_links': inner_links, 'outer_three_face_intervals': outer_intervals})

    ears = []
    for i in range(5):
        # The only exterior facial ear at a_(i+1) closes its path of three
        # interior incident triangles.  The new chord is a_i a_(i+2).
        ear = face_row('EAR' + str(i), 'hypothetical_exterior_facial_ear',
                       (vertex('a', i), vertex('a', i + 2), vertex('a', i + 1)))
        ear_faces = faces + [ear]
        ear_data = rebuild(ear_faces)
        ear_vertex = vertex('a', i + 1)
        complete_link = verify_link(ear_data, ear_vertex,
            [vertex('a', i), vertex('u', i + 1), vertex('u', i + 2), vertex('a', i + 2)], True)
        require(complete_link['degree'] == 4, 'facial ear did not close degree-four star')
        expected_faces = {'K' + str((i + 1) % 5), 'R' + str((i + 1) % 5),
                          'K' + str((i + 2) % 5), ear['id']}
        actual_faces = {row['id'] for row in ear_faces if ear_vertex in row['oriented_vertices']}
        require(actual_faces == expected_faces, 'ear full star misses a literal face')
        ear_summary = summary(ear_faces, ear_data)
        require((ear_summary['vertex_count'], ear_summary['edge_count'], ear_summary['face_count'],
                 ear_summary['euler_characteristic']) == (11, 26, 16, 1), 'facial ear counts')
        require(len(ear_summary['boundary_edges']) == 4, 'ear did not leave four-cycle boundary')
        ears.append({'chord': list(edge(vertex('a', i), vertex('a', i + 2))),
                     'literal_added_face': ear, 'closed_degree_four_vertex': ear_vertex,
                     'complete_incident_face_ids': sorted(actual_faces),
                     'complete_link': complete_link, 'complex': ear_summary})

    cap_faces = [face_row('CAP' + str(i), 'opposite_complete_W5_face',
                         ('outside_c', vertex('a', i + 1), vertex('a', i))) for i in range(5)]
    sphere_faces = faces + cap_faces
    sphere_data = rebuild(sphere_faces)
    sphere = summary(sphere_faces, sphere_data)
    require((sphere['vertex_count'], sphere['edge_count'], sphere['face_count'],
             sphere['euler_characteristic']) == (12, 30, 20, 2), 'opposite-cap sphere counts')
    require(not sphere['boundary_edges'], 'opposite-cap sphere has a boundary')
    require(set(sphere['degrees'].values()) == {5}, 'opposite cap not all degree five')
    sphere_links = list(inner_links)
    for i in range(5):
        sphere_links.append(verify_link(sphere_data, vertex('a', i),
            [vertex('a', i - 1), vertex('u', i), vertex('u', i + 1),
             vertex('a', i + 1), 'outside_c'], True))
    sphere_links.append(verify_link(sphere_data, 'outside_c', boundary, True))
    graph_edges = set(sphere_data['edge_faces'])
    all_triangles = {tuple(triple) for triple in combinations(sphere_data['vertices'], 3)
                     if all(edge(u, v) in graph_edges for u, v in combinations(triple, 2))}
    require(all_triangles == {tuple(sorted(row['oriented_vertices'])) for row in sphere_faces},
            'opposite-cap sphere has a nonfacial triangle')
    sphere.update({'literal_faces': sphere_faces, 'complete_vertex_links': sphere_links,
                   'all_three_cliques_are_listed_faces': True,
                   'all_triangle_vertex_sets': [list(row) for row in sorted(all_triangles)]})
    return {'schema': 'R6-DOUBLE-W5-101-radius-two-calibration-v1',
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope': 'exact labelled simplicial disk, five local facial-ear controls, opposite W5 cap',
            'source_coverage': {'status': 'not triggered', 'genuine_sources': 0,
                                'source_realization_claim': False, 'paper_proof_verified': False},
            'authority_boundary': ['finite literal-face and local-link calibration only',
                                   'does not prove source faciality or source short-cap theorem',
                                   'does not prove a hypothetical source contains this disk',
                                   'disk labels do not identify original source pins'],
            'radius_two_disk': disk, 'five_hypothetical_facial_ears': ears,
            'opposite_complete_W5_cap_sphere': sphere}


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = compute()
    if args.write:
        with args.write.open('x') as stream:
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write('\n')
    else:
        require(json.loads(args.check.read_text()) == result, 'radius-two certificate mismatch')
    print(json.dumps({'status': 'PASS', 'disk_vertices': 11, 'disk_faces': 15,
                      'outer_facial_ear_controls': 5, 'opposite_cap_vertices': 12,
                      'opposite_cap_faces': 20, 'opposite_cap_all_degrees': 5,
                      'genuine_sources': 0, 'paper_proof_verified': False}, sort_keys=True))


if __name__ == '__main__':
    main()
