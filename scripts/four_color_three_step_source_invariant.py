#!/usr/bin/env python3
"""Exact three-step fibres and immutable marked-source nonalternation controls.

The alternating source certificate is rejected, not its color relation.  The
positive source and both historical nine-vertex controls retain empty fibres.
No 4CT oracle, production elimination engine, or bounded search is used.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess

import networkx as nx

import four_color_eight_cut_three_step_verification as historical

ROOT = Path(__file__).resolve().parents[1]
COLORS = tuple(range(4))
LABELS = ['x1', 'x2', 'z', 'a', 'b', 'c', 'd', 'w', 'e']


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def canonical_edges(edges):
    return sorted({tuple(sorted(edge)) for edge in edges})


def alternating_quadruples(cycle, left, right):
    """Actual cyclic port order, never a color-based or scope-sorted order."""
    left, right = set(left), set(right)
    answer = []
    for indexes in combinations(range(len(cycle)), 4):
        ports = tuple(cycle[i] for i in indexes)
        owners = tuple(0 if p in left else 1 if p in right else None for p in ports)
        if owners in ((0, 1, 0, 1), (1, 0, 1, 0)):
            answer.append(ports)
    return answer


def source_certificate(name, edges, cycle=None):
    certificate = dict(
        certificate_id=name, vertex_order=list(range(9)), original_edges=edges,
        marked_original_cycle=cycle, private_paths=[[3, 0, 4], [5, 1, 6]] if cycle else [],
        port_orders=[[3, 4], [5, 6]] if cycle else [],
        source_semantics='Original vertices, edges and cycle survive as provenance after quantification.',
    )
    if cycle:
        edge_set = set(edges)
        assert all(tuple(sorted((u, v))) in edge_set
                   for u, v in zip(cycle, cycle[1:] + cycle[:1]))
        for path in certificate['private_paths']:
            assert all(tuple(sorted(edge)) in edge_set for edge in zip(path, path[1:]))
        assert not set(certificate['private_paths'][0]) & set(certificate['private_paths'][1])
        assert all(not set(path[1:-1]) & set(cycle) for path in certificate['private_paths'])
        certificate['alternating_port_quadruples'] = alternating_quadruples(cycle, [3, 4], [5, 6])
        certificate['P_nonalternating'] = not certificate['alternating_port_quadruples']
        certificate['P_hypothesis'] = (
            'Both private paths lie in the same closed disk bounded by the marked C, '
            'and their interiors avoid C. The planar positive embedding certifies '
            'this placement; the alternating candidate cannot have it.')
    return certificate


def original_factor(edge, i):
    return dict(id=f'edge:{i}', scope=tuple(edge),
                rows={row for row in product(COLORS, repeat=2) if row[0] != row[1]},
                source_ids={f'edge:{i}'})


def exact_elimination(edges, certificate):
    """Full literal tables with empty history fibres and coherent reverse lifts."""
    certificate_digest = digest(certificate)
    factors = [original_factor(edge, i) for i, edge in enumerate(edges)]
    initial = [dict(id=f['id'], ordered_scope=f['scope'], original_edge=edges[i],
                    complete_rows=sorted(f['rows'])) for i, f in enumerate(factors)]
    histories, lookup = [], []
    for step, vertex in enumerate((0, 1, 2)):
        bucket = [f for f in factors if vertex in f['scope']]
        factors = [f for f in factors if vertex not in f['scope']]
        scope = tuple(sorted(set().union(*(set(f['scope']) for f in bucket)) - {vertex}))
        fibres, table = {}, set()
        indexes = [tuple((None if v == vertex else scope.index(v)) for v in f['scope'])
                   for f in bucket]
        for row in product(COLORS, repeat=len(scope)):
            allowed = tuple(color for color in COLORS if all(
                tuple(color if pos is None else row[pos] for pos in positions) in factor['rows']
                for factor, positions in zip(bucket, indexes)))
            fibres[row] = allowed
            if allowed:
                table.add(row)
        factor_id = f'projection:{step}:{vertex}'
        sources = set().union(*(f['source_ids'] for f in bucket))
        factors.append(dict(id=factor_id, scope=scope, rows=table, source_ids=sources))
        histories.append(dict(
            step=step, eliminated_vertex=vertex, operation='natural_join_then_exists',
            input_factor_ids=[f['id'] for f in bucket], output_factor_id=factor_id,
            ordered_scope=scope, original_source_ids=sorted(sources),
            source_certificate_digest=certificate_digest,
            full_fibres=[dict(row=row, eliminated_colors=fibres[row]) for row in sorted(fibres)],
            nonempty_rows=len(table), empty_rows=len(fibres) - len(table),
        ))
        lookup.append((vertex, scope, fibres))
        # Detect accidental provenance mutations at each step, including after z.
        assert digest(certificate) == certificate_digest
    boundary = tuple(range(3, 9))
    direct = {row: [] for row in product(COLORS, repeat=6)}
    for coloring in product(COLORS, repeat=9):
        if all(coloring[u] != coloring[v] for u, v in edges):
            direct[coloring[3:]].append(coloring[:3])
    output = []
    for row in product(COLORS, repeat=6):
        assignment = dict(zip(boundary, row))
        satisfies = all(tuple(assignment[v] for v in f['scope']) in f['rows'] for f in factors)
        lifts = [assignment] if satisfies else []
        for vertex, scope, fibres in reversed(lookup):
            lifts = [assignment | {vertex: color}
                     for assignment in lifts
                     for color in fibres[tuple(assignment[v] for v in scope)]]
        reconstructed = sorted(tuple(assignment[v] for v in (0, 1, 2)) for assignment in lifts)
        assert reconstructed == direct[row], (row, reconstructed, direct[row])
        output.append(dict(row=row, full_internal_lifts=reconstructed))
    return dict(
        elimination_order=[0, 1, 2], boundary_order=boundary,
        original_edge_factors=initial, history=histories,
        remaining_factors=[dict(id=f['id'], ordered_scope=f['scope'], complete_rows=sorted(f['rows']),
                                original_source_ids=sorted(f['source_ids'])) for f in factors],
        source_certificate_digest=certificate_digest,
        original_assignments_checked=4**9, complete_boundary_rows=4**6,
        full_solution_count=sum(len(v) for v in direct.values()),
        nonempty_fibres=sum(bool(v) for v in direct.values()),
        empty_fibres=sum(not v for v in direct.values()),
        complete_fibres=output,
    )


def rotation_from_faces(faces, graph):
    """Construct a full spherical rotation, including the external ze bridge."""
    successor = {vertex: {} for vertex in graph}
    for face in faces:
        for i, vertex in enumerate(face):
            previous, following = face[i - 1], face[(i + 1) % len(face)]
            assert previous not in successor[vertex]
            successor[vertex][previous] = following
    rotations = {}
    for vertex, neighbors in successor.items():
        first = min(neighbors)
        order = [first]
        while neighbors[order[-1]] != first:
            order.append(neighbors[order[-1]])
            assert len(order) <= len(neighbors)
        assert set(order) == set(graph[vertex])
        rotations[vertex] = order
    embedding = nx.PlanarEmbedding()
    embedding.set_data(rotations)
    embedding.check_structure()
    assert set(embedding.edges()) == {(u, v) for u, v in graph.edges()} | {(v, u) for u, v in graph.edges()}
    visited, obtained = set(), []
    for u in embedding:
        for v in embedding[u]:
            if (u, v) not in visited:
                obtained.append(embedding.traverse_face(u, v, visited))
    assert len(graph) - graph.number_of_edges() + len(obtained) == 2
    return dict(rotation_system=rotations, oriented_face_walks=obtained,
                prescribed_bounded_face_walks=faces[:-1], prescribed_exterior_walk=faces[-1])


def k33_certificate(edges):
    left, right = [3, 4, 1], [5, 6, 0]
    paths = [[3, 5], [3, 2, 6], [3, 0], [4, 7, 5], [4, 6], [4, 0],
             [1, 5], [1, 6], [1, 0]]
    edge_set = set(edges)
    assert {(p[0], p[-1]) for p in paths} == set(product(left, right))
    interior = [v for path in paths for v in path[1:-1]]
    assert len(interior) == len(set(interior))
    assert not set(interior) & set(left + right)
    assert all(tuple(sorted(edge)) in edge_set for path in paths for edge in zip(path, path[1:]))
    return dict(branch_sets=[left, right], nine_original_paths=paths,
                interpretation='A literal K3,3 subdivision, independently checkable from original edges.')


def baseline_checks(edges):
    graph = nx.Graph(edges)
    edge_set = set(edges)
    # Complete local wheels are present as subgraphs; the crossed candidate has
    # two additional original edges between their private boundary vertices.
    wheel_rims = [[1, 2, 3, 4, 7], [0, 2, 6, 5, 7]]
    assert all(tuple(sorted(edge)) in edge_set for rim in wheel_rims
               for edge in zip(rim, rim[1:] + rim[:1]))
    common = sorted(set(graph[0]) & set(graph[1]))
    assert common == [2, 7]
    codegrees = [[u, v, len(set(graph[u]) & set(graph[v]))] for u, v in edges]
    assert max(row[2] for row in codegrees) <= 2
    boundary = (0, 1, 1, 0, 0, 1)  # a,b,c,d,w,e
    fixed = dict(zip(range(3, 9), boundary))
    A = set(COLORS) - {fixed[v] for v in (3, 4, 7)}
    B = set(COLORS) - {fixed[v] for v in (5, 6, 7)}
    assert A == B == {2, 3}
    support = [z for z in COLORS if any(x1 != x2 and x1 != z and x2 != z
                                       for x1 in A for x2 in B)]
    assert support == [0, 1]
    assert all(fixed[u] != fixed[v] for u, v in edges if u >= 3 and v >= 3)
    support_after_original_z_edges = [z for z in support
                                     if all(z != fixed[v] for v in graph[2] if v >= 3)]
    assert not support_after_original_z_edges
    return dict(
        witness_boundary_order=list(range(3, 9)), witness_boundary=boundary,
        Group_A_nonempty_before_z_edges=[sorted(A), sorted(B)],
        triangle_anchor_edges=[[0, 1], [0, 2], [1, 2]], triangle_anchor_t=2,
        complete_local_wheel_rims=wheel_rims, common_center_neighbors=common,
        original_edge_codegrees=codegrees, minimum_cross_step_scope=6 - len(common),
        joint_z_support_before_original_z_edges=support,
        original_z_attachment_vertices=sorted(v for v in graph[2] if v >= 3),
        joint_z_support_after_original_z_edges=support_after_original_z_edges,
        scope_note='These necessary local checks do not assert that the marked global placement is planar.',
    )


def conditional_elimination(edges, certificate, fixed):
    """Complete 64-assignment check at one named 14-coordinate interface.

    This is deliberately not a claim about all 4**14 interfaces. Original
    factor scopes and all substituted coordinates stay in the derivation.
    """
    certificate_digest = digest(certificate)
    factors, initial = [], []
    for i, edge in enumerate(edges):
        scope = tuple(vertex for vertex in edge if vertex not in fixed)
        rows = set()
        for row in product(COLORS, repeat=len(scope)):
            values = fixed | dict(zip(scope, row))
            if values[edge[0]] != values[edge[1]]:
                rows.add(row)
        factor = dict(id=f'edge:{i}', scope=scope, rows=rows, source_ids={f'edge:{i}'})
        factors.append(factor)
        initial.append(dict(id=factor['id'], original_ordered_scope=edge,
                            substituted_coordinates=[[v, fixed[v]] for v in edge if v in fixed],
                            conditional_ordered_scope=scope, complete_conditional_rows=sorted(rows)))
    histories, lookup = [], []
    for step, vertex in enumerate((0, 1, 2)):
        bucket = [f for f in factors if vertex in f['scope']]
        factors = [f for f in factors if vertex not in f['scope']]
        scope = tuple(sorted(set().union(*(set(f['scope']) for f in bucket)) - {vertex}))
        fibres = {}
        for row in product(COLORS, repeat=len(scope)):
            assignment = dict(zip(scope, row))
            fibres[row] = tuple(color for color in COLORS if all(
                tuple(color if v == vertex else assignment[v] for v in factor['scope']) in factor['rows']
                for factor in bucket))
        table = {row for row, colors in fibres.items() if colors}
        factor_id = f'projection:{step}:{vertex}'
        sources = set().union(*(f['source_ids'] for f in bucket))
        factors.append(dict(id=factor_id, scope=scope, rows=table, source_ids=sources))
        histories.append(dict(step=step, eliminated_vertex=vertex,
                              input_factor_ids=[f['id'] for f in bucket], output_factor_id=factor_id,
                              ordered_scope=scope, original_source_ids=sorted(sources),
                              source_certificate_digest=certificate_digest,
                              full_fibres=[dict(row=row, eliminated_colors=colors)
                                           for row, colors in sorted(fibres.items())]))
        lookup.append((vertex, scope, fibres))
        assert digest(certificate) == certificate_digest
    assert all(not factor['scope'] for factor in factors)
    assignments = [{}] if all(() in factor['rows'] for factor in factors) else []
    for vertex, scope, fibres in reversed(lookup):
        assignments = [assignment | {vertex: color} for assignment in assignments
                       for color in fibres[tuple(assignment[v] for v in scope)]]
    reconstructed = sorted(tuple(assignment[v] for v in (0, 1, 2)) for assignment in assignments)
    raw, direct = [], []
    for inner in product(COLORS, repeat=3):
        coloring = fixed | dict(zip((0, 1, 2), inner))
        valid = all(coloring[u] != coloring[v] for u, v in edges)
        raw.append(dict(internal_colors=inner, satisfies_original_edges=valid))
        if valid:
            direct.append(inner)
    assert reconstructed == direct
    return dict(elimination_order=[0, 1, 2], boundary_order=sorted(fixed),
                named_boundary_row=[fixed[v] for v in sorted(fixed)],
                full_internal_fibre=direct, raw_64_internal_assignments=raw,
                original_edge_factors=initial, history=histories,
                source_certificate_digest=certificate_digest,
                scope='Complete fibre at this one named row only; not all 4**14 interface rows.')


def noncrossing_blocks(cycle, blocks):
    owner = {v: i for i, block in enumerate(blocks) for v in block}
    for indexes in combinations(range(len(cycle)), 4):
        ids = tuple(owner.get(cycle[i]) for i in indexes)
        if None not in ids and ids[0] == ids[2] and ids[1] == ids[3] and ids[0] != ids[1]:
            return False
    return True


def actual_bichromatic_partitions(edges, cycle, coloring):
    graph = nx.Graph()
    graph.add_nodes_from(coloring)
    graph.add_edges_from(edges)
    pair_blocks, records = {}, []
    for pair in combinations(COLORS, 2):
        vertices = [v for v, color in coloring.items() if color in pair]
        components = sorted(sorted(c) for c in nx.connected_components(graph.subgraph(vertices)))
        blocks = [sorted(set(component) & set(cycle)) for component in components
                  if set(component) & set(cycle)]
        assert noncrossing_blocks(cycle, blocks)
        pair_blocks[pair] = blocks
        records.append(dict(color_pair=pair, complete_original_components=components,
                            boundary_blocks=blocks, noncrossing=True))
    splits = []
    for left, right in [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]:
        blocks = pair_blocks[left] + pair_blocks[right]
        assert noncrossing_blocks(cycle, blocks)
        splits.append(dict(color_pairs=[left, right], boundary_blocks=blocks, noncrossing=True))
    return dict(six_actual_pair_partitions=records, three_actual_split_partitions=splits)


def outer_attachment_controls():
    """A named source obstruction surviving every actual splitwise NC test."""
    spokes = [(0, 1), (0, 2), (0, 7), (0, 3), (0, 4),
              (1, 2), (1, 7), (1, 5), (1, 6), (2, 8)]
    inner_cycle = [2, 3, 4, 7, 5, 6]
    core = spokes + list(zip(inner_cycle, inner_cycle[1:] + inner_cycle[:1]))
    attachments = [(3, 9), (4, 13), (5, 11), (6, 15)]
    fixed = dict(zip(range(3, 9), (0, 1, 1, 0, 0, 1)))
    fixed.update({9: 2, 10: 3, 11: 2, 12: 3, 13: 2, 14: 3, 15: 2, 16: 3})
    results = {}
    for name, cycle in [('alternating_outer_attachment_blocker', [9, 10, 11, 12, 13, 14, 15, 16]),
                        ('planar_outer_attachment_control', [9, 10, 13, 12, 11, 14, 15, 16])]:
        edges = canonical_edges(core + attachments + list(zip(cycle, cycle[1:] + cycle[:1])))
        paths = [[9, 3, 0, 4, 13], [11, 5, 1, 6, 15]]
        assert not set(paths[0]) & set(paths[1])
        edge_set = set(edges)
        assert all(tuple(sorted(edge)) in edge_set for path in paths for edge in zip(path, path[1:]))
        assert all(not set(path[1:-1]) & set(cycle) for path in paths)
        alternations = alternating_quadruples(cycle, [9, 13], [11, 15])
        certificate = dict(certificate_id=name, vertex_order=list(range(17)), original_edges=edges,
                           marked_original_cycle=cycle, private_paths=paths,
                           alternating_port_quadruples=alternations, P_nonalternating=not alternations,
                           placement_hypothesis='Both marked paths lie in the same disk bounded by C; '
                           'their interiors avoid C. This is impossible in the alternating case.')
        conditional = conditional_elimination(edges, certificate, fixed)
        assert conditional['full_internal_fibre'] == []
        pre_edges = [edge for edge in edges if edge != (2, 8)]
        pre_lifts = []
        for inner in product(COLORS, repeat=3):
            coloring = fixed | dict(zip((0, 1, 2), inner))
            if all(coloring[u] != coloring[v] for u, v in pre_edges):
                pre_lifts.append(dict(internal_colors=inner,
                                      actual_partitions=actual_bichromatic_partitions(pre_edges, cycle, coloring)))
        assert [lift['internal_colors'] for lift in pre_lifts] == [(2, 3, 1), (3, 2, 1)]
        graph = nx.Graph(edges)
        planar, embedding = nx.check_planarity(graph)
        assert planar == ('control' in name)
        codegrees = [[u, v, len(set(graph[u]) & set(graph[v]))] for u, v in edges]
        assert max(row[2] for row in codegrees) == 2
        result = dict(labels=LABELS + ['A', 's', 'F', 't', 'B', 'u', 'D', 'v'],
                      certificate=certificate, networkx_planar=planar,
                      original_core_cycle=inner_cycle, attachment_edges=attachments,
                      original_edge_codegrees=codegrees,
                      center_common_neighbors=sorted(set(graph[0]) & set(graph[1])),
                      Group_A_sets_before_z_edges=[[2, 3], [2, 3]],
                      triangle_anchor_t=2, minimum_cross_step_scope=4,
                      joint_z_support_before_original_z_edges=[0, 1],
                      all_six_actual_pair_and_three_split_partitions_noncrossing=True,
                      exact_named_row=conditional, before_ze_complete_fibre=pre_lifts,
                      scope='Conditional 17-vertex original-edge control. It does not enumerate '
                            'all interfaces or assert a genuine disk placement for the alternating source.')
        if planar:
            embedding.check_structure()
            faces = [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 7], [0, 7, 1],
                     [1, 7, 5], [1, 5, 6], [1, 6, 2],
                     [4, 3, 9, 10, 13], [5, 7, 4, 13, 12, 11],
                     [6, 5, 11, 14, 15], [3, 2, 8, 2, 6, 15, 16, 9],
                     [9, 16, 15, 14, 11, 12, 13, 10]]
            result['embedding'] = rotation_from_faces(faces, graph)
            result['embedding']['placement'] = 'Marked outer C is the exterior face; all core vertices and both paths lie inside.'
        results[name] = result
    return results


def cases_audit():
    spokes = [(0, 1), (0, 2), (0, 7), (0, 3), (0, 4),
              (1, 2), (1, 7), (1, 5), (1, 6), (2, 8)]
    cases = {}
    for name, cycle in [('alternating_blocker', [2, 3, 5, 7, 4, 6]),
                        ('planar_doublefan_control', [2, 3, 4, 7, 5, 6])]:
        edges = canonical_edges(spokes + [(3, 4), (5, 6)]
                                + list(zip(cycle, cycle[1:] + cycle[:1])))
        certificate = source_certificate(name, edges, cycle)
        graph = nx.Graph(edges)
        planar, _ = nx.check_planarity(graph)
        case = dict(labels=LABELS, certificate=certificate, baseline_checks=baseline_checks(edges),
                    networkx_planar=planar, exact=exact_elimination(edges, certificate))
        witness = next(f for f in case['exact']['complete_fibres']
                       if f['row'] == (0, 1, 1, 0, 0, 1))
        assert witness['full_internal_lifts'] == []
        if name == 'alternating_blocker':
            assert not planar and not certificate['P_nonalternating']
            case['nonplanarity_certificate'] = k33_certificate(edges)
        else:
            assert planar and certificate['P_nonalternating']
            faces = [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 7], [0, 7, 1],
                     [1, 7, 5], [1, 5, 6], [1, 6, 2], [2, 8, 2, 6, 5, 7, 4, 3]]
            case['embedding'] = rotation_from_faces(faces, graph)
            case['embedding']['placement'] = 'Both centers inside marked C; leaf e lies outside C at z.'
        cases[name] = case
    old_cases = [('historical_adjacent_nine_point', historical.three_step_audit()),
                 ('historical_independent_nine_point', historical.independent_centers_audit())]
    for name, old in old_cases:
        edges = canonical_edges(old['original_edges'])
        certificate = source_certificate(name, edges)
        exact = exact_elimination(edges, certificate)
        assert exact['full_solution_count'] == old['full_solution_count']
        assert exact['complete_fibres'] == old['complete_fibres']
        assert nx.check_planarity(nx.Graph(edges))[0]
        cases[name] = dict(certificate=certificate, networkx_planar=True, exact=exact,
                           independently_recomputed_historical_control=old)
    assert cases['historical_adjacent_nine_point']['exact']['full_solution_count'] == 7776
    assert cases['historical_adjacent_nine_point']['exact']['nonempty_fibres'] == 2256
    assert cases['historical_independent_nine_point']['exact']['full_solution_count'] == 26244
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', required=True, type=Path)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=False)
    cases = cases_audit()
    result = dict(networkx_version=nx.__version__, cases=cases,
                  conditional_outer_attachment_cases=outer_attachment_controls(),
                  scope='Finite original-edge verification of a marked-source invariant; '
                        'not an arbitrary planar-source existence theorem, a row-pruning rule, or 4CT.')
    output = args.out_dir / 'results.json'
    output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    sources = ['scripts/four_color_three_step_source_invariant.py',
               'scripts/four_color_eight_cut_three_step_verification.py',
               'scripts/four_color_seven_cut_verification.py']
    baseline = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    receipt = dict(baseline=baseline,
                   sources={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in sources},
                   outputs={'results.json': sha256(output.read_bytes()).hexdigest()})
    (args.out_dir / 'verification.json').write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print(json.dumps({name: {key: case['exact'][key] for key in
                            ('full_solution_count', 'nonempty_fibres', 'empty_fibres')}
                      | {'networkx_planar': case['networkx_planar']}
                      for name, case in cases.items()}, sort_keys=True))


if __name__ == '__main__':
    main()
