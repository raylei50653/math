#!/usr/bin/env python3
"""Task C finite cap composition, with complete fibres and literal graph replay.

Freeze DOMAIN.json before computation with --freeze-domain. --write exclusively
creates certificate.json; --check is read-only and recomputes every record.
--seed changes only computation order. All output records have canonical order.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
import sys
import time

# Read-only replay includes the frozen source-reader import.
sys.dont_write_bytecode = True

import networkx as nx

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
UPSTREAM = ROOT / 'frozen/audits/2026-10-12-cofacial-uniform-separation-eb6b2303'
NAMES = ['a', 'b', 'c', 'd', 'e', 'x', 'y', 'z', 'v']
B = [0, 1, 2, 3, 4]
L = [0, 5, 2, 6, 7]
P = [0, 1, 2, 6, 7]
Q = [0, 5, 2, 3, 4]
CYCLE = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(values):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in values)


def norm(edges):
    return sorted({tuple(sorted(e)) for e in edges})


def exclusive_json(path, data):
    with path.open('x') as stream:
        json.dump(data, stream, sort_keys=True, separators=(',', ':'))
        stream.write('\n')


def inputs():
    manifest = json.loads((ROOT / 'INPUTS.json').read_text())
    for row in manifest['files']:
        need(digest(ROOT / row['frozen']) == row['sha256'],
             'frozen input hash: ' + row['path'])
    spec = importlib.util.spec_from_file_location('frozen_cap_source',
                                                 UPSTREAM / 'controls/checker.py')
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    data = json.loads(source.SOURCE.read_text())
    upstream = json.loads((UPSTREAM / 'controls/certificate.v2.json').read_text())
    need(digest(source.SOURCE) == upstream['frozen_source']['sha256'],
         'literal source must be the v2 frozen source')
    masks = sorted(map(int, data['cells']))
    need(len(masks) == 132, '132 literal catalogue witnesses')
    pats = [list(p) for p in source.patterns()]
    need(pats == data['pattern_order'] == upstream['pattern_order'], 'ten rows')
    return manifest, source, data, upstream, masks, pats


def domain_data(manifest, masks, pats):
    return {
        'schema': 'degree5-c5-c5-domain-v1', 'base': manifest['base'],
        'source_manifest_sha256': digest(ROOT / 'INPUTS.json'),
        'boundary_order': NAMES[:5], 'link_order': [NAMES[i] for i in L],
        'P_boundary_order': [NAMES[i] for i in P],
        'Q_boundary_order': [NAMES[i] for i in Q],
        'pattern_order': pats, 'catalogue_order': masks,
        'pairs': [[a, b] for a in masks for b in masks],
        'pair_count': 132 ** 2, 'rows_per_pair': 10,
        'vertex_order': 'a,b,c,d,e,x,y,z,v,P-private ascending,Q-private ascending',
        'simple_edge_retention': 'skeleton first, then P extras, then Q extras',
        'scope': 'all ordered frozen literal cap pairs; no outside source supplied',
    }


def face_cycles(rotation, endpoints):
    """Traverse an edge-labelled orientable rotation system, also parallel edges."""
    visited = set()
    faces = []
    for v in range(len(rotation)):
        for edge in rotation[v]:
            start = (v, edge)
            if start in visited:
                continue
            dart = start
            face = []
            while dart not in visited:
                visited.add(dart)
                u, e = dart
                face.append([u, e])
                a, b = endpoints[e]
                w = b if u == a else a
                seq = rotation[w]
                dart = (w, seq[(seq.index(e) + 1) % len(seq)])
            need(dart == start, 'face permutation closes at its own dart')
            faces.append(face)
    need(len(visited) == 2 * len(endpoints), 'all darts in rotation faces')
    return faces


def cycle_equal(a, b):
    return len(a) == len(b) and any(a == b[i:] + b[:i] for i in range(len(b)))


def cap_embedding(n, edges):
    """Apex embedding places every named boundary edge on the disk perimeter."""
    graph = nx.Graph()
    graph.add_nodes_from(range(n + 1))
    graph.add_edges_from(edges)
    graph.add_edges_from((i, n) for i in range(5))
    planar, emb = nx.check_planarity(graph)
    need(planar, 'cap apex planarity')
    boundary_edges = {tuple(e) for e in CYCLE}
    ids = {e: i for i, e in enumerate(edges)}
    rotation = [[ids[tuple(sorted((v, w)))]
                 for w in emb.neighbors_cw_order(v) if w != n] for v in range(n)]
    exterior = [0, 4, 3, 2, 1]
    faces = face_cycles(rotation, edges)
    if not any(cycle_equal([d[0] for d in f], exterior) for f in faces):
        rotation = [list(reversed(seq)) for seq in rotation]
        faces = face_cycles(rotation, edges)
    outer = [f for f in faces if cycle_equal([d[0] for d in f], exterior)]
    need(len(outer) == 1, 'cap ordered C5 exterior face')
    need(n - len(edges) + len(faces) == 2, 'cap rotation sphere Euler check')
    interior = [f for f in faces if f != outer[0]]
    need(all(tuple(sorted((i, (i + 1) % 5))) in boundary_edges for i in B),
         'literal C5 boundary')
    return rotation, interior


def graph_lifts(n, edges, boundary):
    """Independent whole-graph MRV backtracking; does not consult cap fibres."""
    adjacency = [[] for _ in range(n)]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    colors = list(boundary) + [-1] * (n - 5)
    domains = [15] * n
    for a in range(5):
        for b in adjacency[a]:
            if b < 5:
                if colors[a] == colors[b]:
                    return []
            else:
                domains[b] &= ~(1 << colors[a])
    result = []

    def search(todo):
        if not todo:
            result.append(tuple(colors))
            return
        v = min(todo, key=lambda w: (domains[w].bit_count(), -len(adjacency[w]), w))
        choices = domains[v]
        if not choices:
            return
        remaining = [w for w in todo if w != v]
        while choices:
            bit = choices & -choices
            choices ^= bit
            colors[v] = bit.bit_length() - 1
            changed = []
            feasible = True
            for w in adjacency[v]:
                if colors[w] < 0 and domains[w] & bit:
                    changed.append((w, domains[w]))
                    domains[w] &= ~bit
                    if not domains[w]:
                        feasible = False
            if feasible:
                search(remaining)
            for w, old in changed:
                domains[w] = old
            colors[v] = -1

    search(list(range(5, n)))
    return sorted(result)


def make_caps(source, data, upstream, masks, pats, visits, expected):
    proper = [list(p) for p in itertools.product(range(4), repeat=5)
              if all(p[a] != p[b] for a, b in CYCLE)]
    need(len(proper) == 240, 'all actual proper C5 assignments')
    cap_map = {}
    for mask in visits:
        cell = data['cells'][str(mask)]
        n = 5 + cell['k_eff']
        edges = source.normalized(source.CYCLE + cell['edges'])
        rows = [source.lifts(n, edges, tuple(p)) for p in pats]
        need(source.relation(rows) == mask, 'upstream literal recolouring')
        need([len(r) for r in rows] == upstream['catalogue']['witness_recolouring'][str(mask)]['ten_row_lift_counts'],
             'v2 cap row counts')
        fibres = []
        for assignment in proper:
            raw = source.lifts(n, edges, tuple(assignment))
            independent = graph_lifts(n, edges, assignment)
            need(raw == [list(c) for c in independent], 'cap independent whole lifts')
            fibres.append([c[5:] for c in raw])
        rotation, faces = cap_embedding(n, edges)
        cap = {'mask': mask, 'catalogue_index': masks.index(mask),
               'k_eff': cell['k_eff'], 'edges': [list(e) for e in edges],
               'rotation_edge_ids': rotation,
               'interior_faces_vertex_edge_darts': faces,
               'actual_boundary_full_private_fibres': fibres,
               'ten_row_full_lift_counts': list(map(len, rows))}
        if expected is not None:
            need(cap == expected[masks.index(mask)], 'cap certificate differs: ' + str(mask))
        cap_map[mask] = cap
    return proper, cap_map


def fixed_skeleton():
    edges = norm(CYCLE + [(L[i], L[(i + 1) % 5]) for i in B] + [(v, 8) for v in L])
    edge_ids = {edge: i for i, edge in enumerate(edges)}
    # Both caps follow B orientation. Star triangles oppose L orientation.
    cycles = [[0, 4, 3, 2, 1]] + [[L[(i + 1) % 5], L[i], 8] for i in B]
    faces = [[[v, edge_ids[tuple(sorted((v, cycle[(i + 1) % len(cycle)])))]]
              for i, v in enumerate(cycle)] for cycle in cycles]
    return edges, faces


def literal_graph(pcap, qcap):
    kp, kq = pcap['k_eff'], qcap['k_eff']
    pmap = P + list(range(9, 9 + kp))
    qmap = Q + list(range(9 + kp, 9 + kp + kq))
    endpoints, faces = fixed_skeleton()
    owners = ['skeleton'] * len(endpoints)
    skeleton_ids = {edge: i for i, edge in enumerate(endpoints)}
    for owner, cap, mapping in [('P', pcap, pmap), ('Q', qcap, qmap)]:
        translated_ids = []
        for old_edge in cap['edges']:
            edge = tuple(sorted(mapping[v] for v in old_edge))
            if tuple(old_edge) in CYCLE:
                translated_ids.append(skeleton_ids[edge])
            else:
                translated_ids.append(len(endpoints))
                endpoints.append(edge)
                owners.append(owner)
        faces.extend([[[mapping[v], translated_ids[e]] for v, e in face]
                      for face in cap['interior_faces_vertex_edge_darts']])
    n = 9 + kp + kq
    successors = [{} for _ in range(n)]
    for face in faces:
        for i, (v, edge_out) in enumerate(face):
            edge_in = face[(i - 1) % len(face)][1]
            need(edge_in not in successors[v], 'no duplicate face corner')
            successors[v][edge_in] = edge_out
    rotation = []
    for v in range(n):
        seq = [min(successors[v])]
        while successors[v][seq[-1]] != seq[0]:
            seq.append(successors[v][seq[-1]])
            need(len(seq) <= len(successors[v]), 'rotation at vertex closes')
        need(len(seq) == len(successors[v]), 'one rotation circle per vertex')
        rotation.append(seq)
    multi_faces = face_cycles(rotation, endpoints)
    need(n - len(endpoints) + len(multi_faces) == 2, 'composed multigraph spherical rotation')
    first = {}
    duplicates = []
    for e, uv in enumerate(endpoints):
        if uv in first:
            keep = first[uv]
            duplicates.append({'endpoints': list(uv), 'kept_edge': keep,
                               'kept_owner': owners[keep], 'deleted_edge': e,
                               'deleted_owner': owners[e]})
            for v in uv:
                rotation[v].remove(e)
        else:
            first[uv] = e
    surviving = sorted(first.values())
    relabel = {old: new for new, old in enumerate(surviving)}
    edges = [endpoints[e] for e in surviving]
    rotation = [[relabel[e] for e in seq] for seq in rotation]
    simple_faces = face_cycles(rotation, edges)
    need(n - len(edges) + len(simple_faces) == 2, 'simplified rotation spherical Euler check')
    need(sum(cycle_equal([d[0] for d in f], [0, 4, 3, 2, 1]) for f in simple_faces) == 1,
         'fixed outer B face survives simplification')
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(edges)
    need(nx.is_connected(graph) and len(edges) == graph.number_of_edges(), 'connected simple graph')
    need(all(a != b for a, b in edges), 'no literal loop')
    need(nx.check_planarity(graph)[0], 'independent literal graph planarity')
    need(sorted(graph.neighbors(8)) == sorted(L), 'center literal degree-five link')
    center_neighbors = [edges[e][0] if edges[e][1] == 8 else edges[e][1]
                        for e in rotation[8]]
    need(cycle_equal(center_neighbors, L), 'actual center rotation has fixed L order')
    for i in B:
        triangle = [L[(i + 1) % 5], L[i], 8]
        need(sum(cycle_equal([d[0] for d in f], triangle) for f in simple_faces) == 1,
             'original star triangular face survives gluing')
    need(all(not (a in pmap[5:] and b in qmap[5:]) and
                 not (b in pmap[5:] and a in qmap[5:]) for a, b in edges), 'no cross-cap edge')
    return {'vertex_names': NAMES + ['P:' + str(i) for i in range(5, 5 + kp)] +
            ['Q:' + str(i) for i in range(5, 5 + kq)],
            'vertex_ownership': ['outer'] * 5 + ['link'] * 3 + ['center'] +
            ['P-private'] * kp + ['Q-private'] * kq,
            'P_local_to_global': pmap, 'Q_local_to_global': qmap,
            'edges': [list(e) for e in edges],
            'edge_owners': [owners[e] for e in surviving],
            'rotation_edge_ids': rotation,
            'faces_vertex_edge_darts': simple_faces,
            'parallel_edge_simplifications': duplicates,
            'internal_vertices': n - 5,
            'embedding_checks': 'triggered and holds'}, n, edges


def pair_record(pmask, qmask, caps, proper_index, pats, masks):
    pc, qc = caps[pmask], caps[qmask]
    graph, n, edges = literal_graph(pc, qc)
    rows = []
    for row_i, pattern in enumerate(pats):
        a, b, c, d, e = pattern
        joint = []
        expanded = []
        for x, y, z, v in itertools.product(range(4), repeat=4):
            if v in (a, x, c, y, z):
                continue
            pp, qp = (a, b, c, y, z), (a, x, c, d, e)
            if pp not in proper_index or qp not in proper_index:
                continue
            pi, qi = proper_index[pp], proper_index[qp]
            pf = pc['actual_boundary_full_private_fibres'][pi]
            qf = qc['actual_boundary_full_private_fibres'][qi]
            if not pf or not qf:
                continue
            # This block is the COMPLETE Cartesian product, not a selected lift.
            joint.append([x, y, z, v, pi, qi])
            expanded.extend(tuple(pattern + [x, y, z, v] + p + q)
                            for p in pf for q in qf)
        expanded.sort()
        direct = graph_lifts(n, edges, pattern)
        need(expanded == direct, f'independent complete literal graph lifts ({pmask},{qmask}) row {row_i}')
        need(len(expanded) == len(set(expanded)), 'full lift product encoding has no duplicates')
        rows.append({'index': row_i, 'pattern': pattern, 'joint': joint,
                     'full_lift_count': len(expanded),
                     'literal_full_witness': list(expanded[0]) if expanded else None})
    sigma = sum(1 << i for i, row in enumerate(rows) if row['joint'])
    target = caps.get(sigma)
    return {'P_mask': pmask, 'Q_mask': qmask, 'graph': graph,
            'rows': rows, 'sigma': sigma, 'in_K': target is not None,
            'representative': None if target is None else {
                'catalogue_index': masks.index(sigma), 'mask': sigma,
                'k_eff': target['k_eff'],
                'minimum_claim': 'frozen catalogue k_eff; no fresh search'},
            'joint_vs_literal_full_lifts': 'triggered and holds'}


def make_certificate(seed=None, expected=None):
    start = time.monotonic()
    manifest, source, data, upstream, masks, pats = inputs()
    domain = domain_data(manifest, masks, pats)
    need(json.loads((HERE / 'DOMAIN.json').read_text()) == domain, 'frozen domain differs')
    rng = random.Random(seed)
    visits = masks[:]
    pair_visits = domain['pairs'][:]
    if seed is not None:
        rng.shuffle(visits)
        rng.shuffle(pair_visits)
    header = {'schema': 'degree5-c5-c5-complete-lifts-v1',
              'base': manifest['base'], 'domain_sha256': digest(HERE / 'DOMAIN.json'),
              'source_manifest_sha256': digest(ROOT / 'INPUTS.json'),
              'pattern_order': pats, 'catalogue_order': masks,
              'full_lift_encoding': {
                  'cap': 'actual_boundary_order[i] concatenated with each cap fibre[i]',
                  'joint': '[X,Y,Z,V,P_assignment_index,Q_assignment_index]',
                  'whole': 'B row + [X,Y,Z,V] + every P private lift + every Q private lift',
                  'product': 'Each joint block means the entire Cartesian product of referenced fibres.',
                  'empties': 'All ten rows and all 240 cap assignments are present, including empty fibres.'}}
    if expected is not None:
        for key, value in header.items():
            need(expected.get(key) == value, 'certificate header: ' + key)
        need(len(expected.get('caps', [])) == 132, 'complete cap array')
        need(len(expected.get('pairs', [])) == 132 ** 2, 'complete pair array')
        for i, (p, q) in enumerate(domain['pairs']):
            row = expected['pairs'][i]
            need((row.get('P_mask'), row.get('Q_mask')) == (p, q), 'pair labels/order')
            need(len(row.get('rows', [])) == 10, 'complete ten joint rows')
    proper, caps = make_caps(source, data, upstream, masks, pats, visits,
                             None if expected is None else expected['caps'])
    proper_index = {tuple(p): i for i, p in enumerate(proper)}
    pair_map = {}
    if expected is not None:
        need(expected.get('actual_boundary_order') == proper, 'complete cap actual assignment order')
    for count, (p, q) in enumerate(pair_visits, 1):
        record = pair_record(p, q, caps, proper_index, pats, masks)
        if expected is not None:
            position = masks.index(p) * len(masks) + masks.index(q)
            need(record == expected['pairs'][position], 'pair certificate differs: ' + str((p, q)))
        pair_map[p, q] = record
        if count % 1000 == 0:
            print(f'checked {count}/17424 pairs; {time.monotonic()-start:.1f}s', file=sys.stderr, flush=True)
    pairs = [pair_map[p, q] for p, q in domain['pairs']]
    sigma_counts = Counter(p['sigma'] for p in pairs)
    result = header | {'actual_boundary_order': proper,
                       'caps': [caps[m] for m in masks], 'pairs': pairs,
                       'summary': {
                           'ordered_pairs': len(pairs), 'joint_rows': 10 * len(pairs),
                           'relation_counts': {str(m): sigma_counts[m] for m in sorted(sigma_counts)},
                           'all_outputs_in_K': all(p['in_K'] for p in pairs),
                           'outside_pairs': [[p['P_mask'], p['Q_mask'], p['sigma']]
                                             for p in pairs if not p['in_K']],
                           'maximum_literal_internal_vertices': max(p['graph']['internal_vertices'] for p in pairs),
                           'maximum_output_representative_k_eff': max(p['representative']['k_eff'] for p in pairs if p['in_K']),
                           'full_lifts_checked': sum(row['full_lift_count'] for p in pairs for row in p['rows']),
                           'joint_blocks': sum(len(row['joint']) for p in pairs for row in p['rows']),
                           'empty_joint_rows': sum(not row['joint'] for p in pairs for row in p['rows']),
                           'pairs_with_parallel_simplification': sum(bool(p['graph']['parallel_edge_simplifications']) for p in pairs),
                           'literal_disk_and_rotation_checks': 'triggered and holds',
                           'independent_complete_whole_graph_recolouring': 'triggered and holds',
                           'minimum_outside_source': 'not triggered',
                           '933_941_actual_source': 'not triggered',
                           'Lean': 'not triggered'}}
    if expected is not None:
        need(result == expected, 'complete certificate equality, including summary and unknown keys')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--freeze-domain', action='store_true')
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--seed', type=int)
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    args = parser.parse_args()
    if args.freeze_domain:
        manifest, _, _, _, masks, pats = inputs()
        exclusive_json(HERE / 'DOMAIN.json', domain_data(manifest, masks, pats))
        print('FROZEN: 17424 ordered cap pairs; no cap composition computed')
        return
    if args.write:
        need(not args.certificate.exists(), '--write destination already exists')
        result = make_certificate(args.seed)
        exclusive_json(args.certificate, result)
        print('WROTE ' + str(args.certificate))
    else:
        expected = json.loads(args.certificate.read_text())
        result = make_certificate(args.seed, expected)
        print('PASS: read-only complete replay; seed=' + str(args.seed))
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
