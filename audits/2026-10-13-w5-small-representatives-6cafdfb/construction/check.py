#!/usr/bin/env python3
"""Actual face-preserving free-W5 representatives; complete literal fibres.

Replay: uv run --with networkx==3.5 python -B .../construction/check.py --check
The certificate is generated exclusively with --write; --check is read-only.
"""
import argparse
from collections import Counter
import gzip
import itertools
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT.parent / 'frozen/artifacts/c5_cells/cells.json'
B = tuple(range(5))
U = tuple(range(5, 10))
C = range(4)
TAUS = tuple(itertools.product(C, repeat=5))


def edge(a, b):
    return tuple(sorted((a, b)))


def proper(tau):
    return all(tau[i] != tau[(i + 1) % 5] for i in B)


def canonical_face(face):
    return min(face[i:] + face[:i] for i in range(len(face)))


def faces_from_rotation(rotation):
    todo = {(v, w) for v, ws in rotation.items() for w in ws}
    faces = []
    while todo:
        start = min(todo)
        dart = start
        face = []
        while True:
            assert dart in todo
            todo.remove(dart)
            v, w = dart
            face.append(v)
            neighbours = rotation[w]
            dart = (w, neighbours[(neighbours.index(v) + 1) % len(neighbours)])
            if dart == start:
                break
        faces.append(canonical_face(face))
    return sorted(faces)


def verify_map(vertices, edges, faces, inner=False):
    assert faces[0] == [0, 4, 3, 2, 1]
    if inner:
        assert faces[-1] == list(U)
    darts = Counter((f[i], f[(i + 1) % len(f)]) for f in faces for i in range(len(f)))
    assert darts == Counter(d for e in edges for d in (tuple(e), tuple(e)[::-1]))
    assert len(vertices) - len(edges) + len(faces) == 2
    rotation = {}
    for v in vertices:
        links = {}
        for f in faces:
            for i, x in enumerate(f):
                if x == v:
                    assert f[i - 1] not in links
                    links[f[i - 1]] = f[(i + 1) % len(f)]
        assert set(links) == set(links.values())
        start = min(links)
        cycle, w = [], start
        while w not in cycle:
            cycle.append(w)
            w = links[w]
        assert w == start and len(cycle) == len(links)
        rotation[str(v)] = cycle
    seen, todo = set(), [0]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(rotation[str(v)])
    assert seen == set(vertices)
    assert len(set(map(tuple, edges))) == len(edges)
    assert all(a != b for a, b in edges)
    return rotation


def disk_witness(cell):
    k = cell['k_eff']
    relabel = {i: i if i < 5 else i + 5 for i in range(5 + k)}
    vertices = [relabel[i] for i in range(5 + k)]
    edges = {edge(i, (i + 1) % 5) for i in B}
    edges |= {edge(relabel[a], relabel[b]) for a, b in cell['edges']}
    assert all(a >= 5 or b >= 5 or (a - b) % 5 in (1, 4) for a, b in edges)
    cone = nx.Graph()
    cone.add_nodes_from(vertices + [20])
    cone.add_edges_from(sorted(edges))
    cone.add_edges_from((20, b) for b in B)
    planar, embedding = nx.check_planarity(cone)
    assert planar
    rotation = {v: [w for w in embedding.neighbors_cw_order(v) if w != 20]
                for v in vertices}
    faces = faces_from_rotation(rotation)
    outer = [0, 4, 3, 2, 1]
    if outer not in faces:
        rotation = {v: list(reversed(ws)) for v, ws in rotation.items()}
        faces = faces_from_rotation(rotation)
    assert outer in faces
    faces.remove(outer)
    faces = [outer] + sorted(faces)
    return {'vertices': vertices, 'edges': sorted(edges), 'faces': faces,
            'rotation': verify_map(vertices, sorted(edges), faces),
            'private': list(range(10, 10 + k))}


def attach_ring(witness):
    k = len(witness['private'])
    vertices = list(range(10 + k))
    edges = set(map(tuple, witness['edges']))
    edges |= {edge(U[i], U[(i + 1) % 5]) for i in B}
    edges.add(edge(0, U[0]))
    faces = [f[:] for f in witness['faces']]
    chosen = next(i for i in range(1, len(faces)) if 0 in faces[i])
    old = faces[chosen]
    position = old.index(0)
    faces[chosen] = old[:position + 1] + [5, 9, 8, 7, 6, 5, 0] + old[position + 1:]
    faces.append(list(U))
    return {'vertices': vertices, 'edges': sorted(edges), 'faces': faces,
            'rotation': verify_map(vertices, sorted(edges), faces, inner=True),
            'B': list(B), 'U': list(U), 'private': witness['private'],
            'ownership': {'annulus_private': witness['private'], 'inner_open_disk': [],
                          'all_named_pins_retained': True},
            'insertion': {'bounded_witness_face_index': chosen, 'bounded_witness_face': old,
                          'attachment_dart': [0, 5], 'attachment_kind': 'bridge'}}


def cap(annulus):
    center = len(annulus['vertices'])
    vertices = annulus['vertices'] + [center]
    edges = sorted(annulus['edges'] + [edge(center, u) for u in U])
    faces = annulus['faces'][:-1] + [[center, U[i], U[(i + 1) % 5]] for i in B]
    return {'vertices': vertices, 'edges': edges, 'faces': faces,
            'rotation': verify_map(vertices, edges, faces), 'center': center,
            'B': list(B), 'U': list(U), 'private': annulus['private']}


def subdivide_bridge(annulus):
    private = len(annulus['vertices'])
    vertices = annulus['vertices'] + [private]
    edges = set(map(tuple, annulus['edges']))
    edges.remove(edge(0, 5))
    edges |= {edge(0, private), edge(private, 5)}
    faces = []
    for face in annulus['faces']:
        new_face = []
        for i, a in enumerate(face):
            b = face[(i + 1) % len(face)]
            new_face.append(a)
            if {a, b} == {0, 5}:
                new_face.append(private)
        faces.append(new_face)
    return {'vertices': vertices, 'edges': sorted(edges), 'faces': faces,
            'rotation': verify_map(vertices, sorted(edges), faces, inner=True),
            'B': list(B), 'U': list(U), 'private': annulus['private'] + [private],
            'ownership': {'annulus_private': annulus['private'] + [private],
                          'inner_open_disk': [], 'all_named_pins_retained': True},
            'subdivision_vertex': private}


def enumerate_lifts(graph, beta):
    vertices = graph['vertices']
    adjacency = {v: set() for v in vertices}
    for a, b in graph['edges']:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colors = dict(zip(B, beta))
    assert all(colors[a] != colors[b] for a, b in graph['edges'] if a in colors and b in colors)
    free = [v for v in vertices if v not in B]
    result = []

    def visit(position):
        if position == len(free):
            result.append(''.join(str(colors[v]) for v in vertices))
            return
        v = free[position]
        banned = {colors[w] for w in adjacency[v] if w in colors}
        for color in C:
            if color not in banned:
                colors[v] = color
                visit(position + 1)
        colors.pop(v, None)

    visit(0)
    return sorted(result)


def tau_index(tau):
    return sum(int(tau[j]) * 4 ** (4 - j) for j in B)


def complete_rows(graph, betas):
    rows = []
    for beta in betas:
        cells = [[] for _ in TAUS]
        for lift in enumerate_lifts(graph, beta):
            cells[tau_index(lift[5:10])].append(lift)
        rows.append({'beta': beta, 'cells': cells})
    return rows


def row_mask(rows):
    return sum(1 << i for i, row in enumerate(rows) if any(row['cells']))


def factor_check(witness, annulus, capped, betas):
    for hrow, arow, grow in zip(witness['rows'], annulus['rows'], capped['rows']):
        beta = hrow['beta']
        for tau, annulus_lifts, capped_lifts in zip(TAUS, arow['cells'], grow['cells']):
            expected = sorted(h[:5] + ''.join(map(str, tau)) + h[5:]
                              for h in hrow['lifts'] if proper(tau) and tau[0] != beta[0])
            assert annulus_lifts == expected
            expected_cap = []
            if proper(tau) and len(set(tau)) == 3:
                center_color = next(iter(set(C) - set(tau)))
                expected_cap = [lift + str(center_color) for lift in expected]
            assert capped_lifts == expected_cap


def build():
    assert nx.__version__ == '3.5'
    data = json.loads(FROZEN.read_text())
    betas = data['pattern_order']
    representatives = []
    chorded = []
    for mask, cell in sorted(data['cells'].items(), key=lambda item: int(item[0])):
        chords = [e for e in cell['edges'] if max(e) < 5]
        if chords:
            chorded.append({'mask': int(mask), 'stored_boundary_chords': chords})
            continue
        witness = disk_witness(cell)
        witness['rows'] = [{'beta': beta, 'lifts': enumerate_lifts(witness, beta)} for beta in betas]
        assert sum(1 << i for i, row in enumerate(witness['rows']) if row['lifts']) == int(mask)
        annulus = attach_ring(witness)
        annulus['rows'] = complete_rows(annulus, betas)
        capped = cap(annulus)
        capped['rows'] = complete_rows(capped, betas)
        factor_check(witness, annulus, capped, betas)
        assert row_mask(annulus['rows']) == row_mask(capped['rows']) == int(mask)
        assert len(annulus['private']) <= 5
        representatives.append({'mask': int(mask), 'private_count': len(witness['private']),
                                'witness': witness, 'annulus': annulus, 'capped': capped})
    assert len(representatives) == 102 and len(chorded) == 30
    controls = []
    for mask in (1023, 127):
        representative = next(item for item in representatives if item['mask'] == mask)
        source = subdivide_bridge(representative['annulus'])
        source['rows'] = complete_rows(source, betas)
        source_capped = cap(source)
        source_capped['rows'] = complete_rows(source_capped, betas)
        assert row_mask(source_capped['rows']) == mask
        strict_r3_cells = []
        for i, (source_row, target_row) in enumerate(zip(source['rows'], representative['annulus']['rows'])):
            for j, (tau, ss, ts) in enumerate(zip(TAUS, source_row['cells'], target_row['cells'])):
                if proper(tau) and len(set(tau)) == 3 and bool(ss) != bool(ts):
                    assert ss and not ts and tau[0] == betas[i][0]
                    strict_r3_cells.append([i, j])
        assert strict_r3_cells
        for srow, grow in zip(source['rows'], source_capped['rows']):
            for tau, ss, gs in zip(TAUS, srow['cells'], grow['cells']):
                expected = []
                if proper(tau) and len(set(tau)) == 3:
                    missing = next(iter(set(C) - set(tau)))
                    expected = [lift + str(missing) for lift in ss]
                assert gs == expected
        controls.append({'target_mask': mask, 'source_annulus': source,
                         'source_capped': source_capped,
                         'target_private_count': representative['private_count'],
                         'source_private_count': len(source['private']),
                         'strict_R3_difference_cells': strict_r3_cells,
                         'source_minimality': 'not triggered'})
    certificate = {'schema': 1, 'B': list(B), 'U': list(U), 'colors': list(C),
                   'beta_domain': betas, 'tau_domain': [list(tau) for tau in TAUS],
                   'representatives': representatives, 'stored_chorded_witnesses': chorded,
                   'strict_shrink_controls': controls,
                   'global_color_closure': 'the same permutation acts on every vertex of the complete graph',
                   'scope': 'catalogue-recognized induced-B relations and the stated bridge/path family only'}

    def total_lifts(graphs):
        return sum(len(cell) for graph in graphs for row in graph['rows'] for cell in row['cells'])

    summary = {'representatives': len(representatives), 'stored_chorded_witnesses': len(chorded),
               'private_count_distribution': dict(sorted(Counter(r['private_count'] for r in representatives).items())),
               'maximum_representative_private_count': 5,
               'maximum_capped_internal_count': 11,
               'annulus_cells': len(representatives) * len(betas) * len(TAUS),
               'witness_full_lifts': sum(len(row['lifts']) for r in representatives for row in r['witness']['rows']),
               'annulus_full_lifts': total_lifts(r['annulus'] for r in representatives),
               'capped_full_lifts': total_lifts(r['capped'] for r in representatives),
               'strict_shrink_controls': [{'mask': c['target_mask'],
                    'source_private_count': c['source_private_count'],
                    'target_private_count': c['target_private_count'],
                    'R3_difference_cells': len(c['strict_R3_difference_cells']),
                    'source_capped_full_lifts': total_lifts([c['source_capped']]),
                    'source_minimality': c['source_minimality']} for c in controls],
               'preservation': 'complete capped outer Sigma equal; R3 need not be equal',
               'arbitrary_source_representative_existence': 'OPEN',
               'minimal_catalogue_outside_source_control': 'not triggered',
               'Lean_formalization': 'not added'}
    return json.loads(json.dumps(certificate)), json.loads(json.dumps(summary))


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    args = parser.parse_args()
    certificate, summary = build()
    path = ROOT / 'certificate.json.gz'
    summary_path = ROOT / 'summary.json'
    if args.write:
        with path.open('xb') as output:
            with gzip.GzipFile(fileobj=output, mode='wb', mtime=0) as compressed:
                compressed.write(json.dumps(certificate, separators=(',', ':')).encode() + b'\n')
        with summary_path.open('x') as output:
            json.dump(summary, output, indent=2)
            output.write('\n')
    else:
        with gzip.open(path, 'rt') as stored:
            assert json.load(stored) == certificate
        assert json.loads(summary_path.read_text()) == summary
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
