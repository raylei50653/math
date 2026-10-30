#!/usr/bin/env python3
"""Independent raw-edge review of the complete nine-side certificate.

No imports from the classification, family, join, or reduction implementations.
The paper coverage proof remains separate from these finite equality checks.
"""
import argparse
import ast
from collections import Counter, defaultdict
import gzip
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parents[1]
ROWS = list(itertools.product(range(4), repeat=6))
X_EDGES = ([(i, (i+1) % 6) for i in range(6)]
           + [(6+i, (2*i+j) % 6) for i in range(3) for j in range(3)]
           + [(6, 7), (7, 8), (6, 8)])


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def enumerate_edges(vertices, edges):
    """Original-edge backtracking; no boundary decomposition or colour quotient."""
    vertices = sorted(vertices)
    neighbours = {v: set() for v in vertices}
    for u, v in edges:
        neighbours[u].add(v)
        neighbours[v].add(u)
    order = sorted(vertices, key=lambda v: (-len(neighbours[v]), v))
    assigned, result = {}, []

    def visit(depth):
        if depth == len(order):
            result.append(tuple(assigned[v] for v in vertices))
            return
        vertex = order[depth]
        for colour in range(4):
            if all(assigned[w] != colour for w in neighbours[vertex] if w in assigned):
                assigned[vertex] = colour
                visit(depth+1)
                del assigned[vertex]

    visit(0)
    return sorted(result)


def attachments(profile):
    """Reconstruct the ordered strip by its successive X/Y face moves."""
    y, result = 0, []
    for x, degree in enumerate(profile):
        for _ in range(degree-1):
            result.append((x, y % 6))
            y += 1
        result.append((x, y % 6))
    assert y == 6 and len(set(result)) == len(result) == 12
    return result


def cycle_side_check(vertices, edges):
    """Recompute a spherical embedding, all short cycles, and their exact sides."""
    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    graph.add_edges_from(edges)
    assert min(dict(graph.degree()).values()) >= 5
    planar, rotation = nx.check_planarity(graph)
    assert planar and len(edges) == 3*len(vertices)-6
    used, faces = set(), []
    for u in vertices:
        for v in rotation.neighbors_cw_order(u):
            if (u, v) not in used:
                face = rotation.traverse_face(u, v, used)
                assert len(face) == 3
                faces.append(face)
    incidence = defaultdict(list)
    for j, face in enumerate(faces):
        for u, v in zip(face, face[1:]+face[:1]):
            incidence[tuple(sorted((u, v)))].append(j)
    assert all(len(fs) == 2 for fs in incidence.values())
    cycles = []
    for root in vertices:
        def extend(path):
            if len(path) >= 3 and graph.has_edge(path[-1], root) and path[1] < path[-1]:
                cycles.append(tuple(path))
            if len(path) < 5:
                for w in sorted(graph[path[-1]]):
                    if w > root and w not in path:
                        extend(path+[w])
        extend([root])
    checks = {}
    for cycle in cycles:
        blocked = {tuple(sorted((u, v))) for u, v in zip(cycle, cycle[1:]+cycle[:1])}
        dual = [set() for _ in faces]
        for edge, (a, b) in incidence.items():
            if edge not in blocked:
                dual[a].add(b)
                dual[b].add(a)
        unseen, components = set(range(len(faces))), []
        while unseen:
            found, todo = set(), [min(unseen)]
            while todo:
                j = todo.pop()
                if j not in found:
                    found.add(j)
                    todo.extend(dual[j]-found)
            unseen -= found
            components.append(found)
        assert len(components) == 2
        sides = sorted(sorted(set().union(*(set(faces[j]) for j in cc))-set(cycle))
                       for cc in components)
        assert min(map(len, sides)) <= (0 if len(cycle) < 5 else 1)
        checks[tuple(sorted(blocked))] = sides
    return checks


def review(report):
    assert report['complete_literal_boundary_rows'] == [list(b) for b in ROWS]
    # This deliberately visits every literal nine-point assignment once.
    xrows = [row for row in itertools.product(range(4), repeat=9)
             if all(row[u] != row[v] for u, v in X_EDGES)]
    assert len(xrows) == 432
    xf = [[] for _ in ROWS]
    row_index = {b: j for j, b in enumerate(ROWS)}
    for row in xrows:
        xf[row_index[row[:6]]].append(row[6:])
    assert xf == [[tuple(p) for p in f] for f in
                  report['complete_original_X_family']['complete_fibres']]
    proper = [(j, b) for j, b in enumerate(ROWS)
              if all(b[i] != b[(i+1) % 6] for i in range(6))]
    assert len(proper) == 732
    expected_profiles = [d for d in itertools.product((1, 2, 3), repeat=6)
                         if sum(d) == 12 and all(d[i] >= (1, 2, 1, 2, 1, 2)[i]
                                               for i in range(6))]
    local = report['all_degree_necessary_profiles']
    assert [tuple(r['X_cross_degrees']) for r in local] == expected_profiles
    fibres, local_reviews = {}, []
    for record in local:
        d = tuple(record['X_cross_degrees'])
        pairs = attachments(d)
        assert record['ordered_original_cross_edges'] == [[x, 9+y] for x, y in pairs]
        expected_edges = sorted(set(tuple(sorted(e)) for e in
                                    X_EDGES + [(9+i, 9+(i+1) % 6) for i in range(6)]
                                    + [(x, 9+y) for x, y in pairs]))
        assert record['original_local_edges'] == [list(e) for e in expected_edges]
        complete = [[] for _ in ROWS]
        for j, beta in proper:
            complete[j] = [a for a in xrows if all(a[x] != beta[y] for x, y in pairs)]
        saved = record['complete_nine_point_lifts_R_d_over_Y']['complete_fibres']
        assert complete == [[tuple(a) for a in f] for f in saved]
        fibres[d] = complete
        local_reviews.append(dict(profile=d, all_4096_complete_fibres_equal=True,
                                  complete_fibres_sha256=digest(complete),
                                  nonempty_rows=sum(bool(f) for f in complete),
                                  complete_lifts=sum(map(len, complete))))
    # Read only the two literal data constants, never execute the reduction code.
    syntax = ast.parse((ROOT/'scripts/four_color_twelve_cut_nine_side_reduction.py').read_text())
    literals = {node.targets[0].id: ast.literal_eval(node.value)
                for node in syntax.body if isinstance(node, ast.Assign)
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in {'SPECS', 'TABLES'}}
    tables, specs = literals['TABLES'], literals['SPECS']
    assert set(tables) == set(specs) | {'222222'}
    for key, table in tables.items():
        chords, triangle = ([], (0, 1, 2)) if key == '222222' else specs[key]
        expected_keys = {''.join(map(str, b)) for _, b in proper
                         if tuple(b[j] for j in triangle) == (0, 1, 2)
                         and (key != '222222' or b[0] == b[3])
                         and all(b[a] != b[c] for a, c in chords)}
        assert set(table) == expected_keys
        assert len(table) == (6 if key == '222222' else 8)
        for beta, lift in table.items():
            assert tuple(map(int, lift)) in fibres[tuple(map(int, key))][row_index[tuple(map(int, beta))]]
    source_reviews = []
    assert len(report['realizations']) == 26
    assert {tuple(s['X_cross_degrees']) for s in report['realizations']} == {
        tuple(r['X_cross_degrees']) for r in local if r['status'] == 'realizable_with_full_source'}
    for source in report['realizations']:
        d = tuple(source['X_cross_degrees'])
        vertices = source['original_vertices']
        edges = [tuple(e) for e in source['original_edges']]
        checks = cycle_side_check(vertices, edges)
        saved_checks = {}
        for check in source['original_short_cycles_with_complete_side_vertices']:
            c = check['cycle']
            key = tuple(sorted(tuple(sorted((u, v))) for u, v in zip(c, c[1:]+c[:1])))
            saved_checks[key] = check['side_vertices']
        assert checks == saved_checks
        direct = enumerate_edges(vertices, edges)
        assert direct == [tuple(a) for a in source['complete_direct_original_colourings']]
        yvertices = source['original_Y_vertices']
        yedges = [(u, v) for u, v in edges if u in yvertices and v in yvertices]
        yrows = enumerate_edges(yvertices, yedges)
        complete_join = sorted(a + y for y in yrows
                               for a in fibres[d][row_index[y[:6]]])
        assert complete_join == direct
        reduction = source['C_reduction']
        reduced_edges = [tuple(e) for e in reduction['reduced_edges']]
        reduced_vertices = reduction['reduced_vertices']
        pullback = {int(v): image for v, image in reduction['original_Y_to_reduced_vertex'].items()}
        assert set(pullback) == set(yvertices)
        reduced_graph = nx.Graph()
        reduced_graph.add_nodes_from(reduced_vertices)
        reduced_graph.add_edges_from(reduced_edges)
        assert nx.check_planarity(reduced_graph)[0] and not nx.number_of_selfloops(reduced_graph)
        reduced = enumerate_edges(reduced_vertices, reduced_edges)
        witnesses = reduction['complete_reduced_colourings_and_unchanged_witness_lifts']
        assert reduced == [tuple(w['reduced_colouring']) for w in witnesses]
        assert len(vertices)-len(reduced_vertices) == reduction['vertex_drop']
        assert reduction['vertex_drop'] in (9, 10)
        spec = reduction['specification']
        if spec['kind'] == 'identify_opposite':
            i, j = spec['identified_Y_indices']
            assert i != j and (i-j) % 6 not in (1, 5)
            assert all(pullback[v] == (9+i if v == 9+j else v) for v in yvertices)
            expected_reduced = {tuple(sorted((pullback[u], pullback[v]))) for u, v in yedges}
            assert all(u != v for u, v in expected_reduced)
            admissible = [(index, b) for index, b in proper if b[i] == b[j]]
        else:
            chords = [tuple(sorted(e)) for e in spec['added_Y_index_pairs']]
            assert len(chords) == len(set(chords)) == 3
            assert all((b-a) % 6 not in (0, 1, 5) for a, b in chords)
            for (a, b), (c, e) in itertools.combinations(chords, 2):
                assert len({a, b, c, e}) < 4 or ((a<c<b) == (a<e<b))
            assert all(pullback[v] == v for v in yvertices)
            expected_reduced = {tuple(sorted(e)) for e in yedges} | {(9+a, 9+b) for a, b in chords}
            admissible = [(index, b) for index, b in proper
                          if all(b[a] != b[c] for a, c in chords)]
        assert set(reduced_edges) == expected_reduced
        assert len(admissible) == (144 if spec['kind'] == 'identify_opposite' else 192)
        assert all(fibres[d][index] for index, b in admissible)
        literal_table_lifts = {}
        for index, beta in admissible:
            uniform = spec['kind'] == 'identify_opposite'
            xmap = list(range(9)) if uniform else spec['representative_to_original_X']
            ymap = list(range(6)) if uniform else spec['representative_to_original_Y']
            assert sorted(xmap) == list(range(9)) and sorted(ymap) == list(range(6))
            transformed = tuple(beta[j] for j in ymap)
            names = [transformed[j] for j in spec['normalizing_triangle']]
            assert len(set(names)) == 3
            names += sorted(set(range(4))-set(names))
            normalized = ''.join(str(names.index(c)) for c in transformed)
            encoded = tables[spec['representative']][normalized]
            lifted = [None]*9
            for j, original in enumerate(xmap):
                lifted[original] = names[int(encoded[j])]
            assert tuple(lifted) in fibres[d][index]
            literal_table_lifts[index] = tuple(lifted)
        direct_set = set(direct)
        for w in witnesses:
            assigned = dict(zip(reduced_vertices, w['reduced_colouring']))
            y = tuple(assigned[pullback[v]] for v in yvertices)
            restored = tuple(w['restored_original_colouring'])
            assert restored[9:] == y == tuple(w['unchanged_original_Y_colouring'])
            assert restored in direct_set
            assert restored[:9] in fibres[d][row_index[y[:6]]]
            assert restored[:9] == literal_table_lifts[row_index[y[:6]]]
            assert y[6:] == tuple(w['unchanged_opposite_complete_internal_witness'])
        source_reviews.append(dict(profile=d, original_vertices=len(vertices),
                                   short_cycle_side_sets_equal=True,
                                   short_cycle_counts=dict(Counter(map(len, (c['cycle'] for c in source['original_short_cycles_with_complete_side_vertices'])))),
                                   complete_original_colourings=len(direct),
                                   complete_raw_edge_set_equals_R_d_join=True,
                                   all_reduction_boundary_rows_have_full_R_d_witness=True,
                                   admitted_reduction_boundary_rows=len(admissible),
                                   complete_reduced_colourings=len(reduced),
                                   every_reduced_colouring_preserves_same_Y=True))
    for path, sha in report['sources_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == sha
    return dict(schema='four-color-twelve-cut-nine-side-independent-review-v1',
                sources_sha256=report['sources_sha256'],
                reviewer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                original_X_literal_assignments_examined=4**9,
                original_X_complete_colourings=len(xrows),
                complete_boundary_rows_reviewed=len(local)*len(ROWS),
                all_35_profiles_full_fibres_equal=True, local_fibre_reviews=local_reviews,
                all_54_normalized_paper_table_branches_verified=True,
                source_reviews=source_reviews,
                complete_original_colourings=sum(s['complete_original_colourings'] for s in source_reviews),
                complete_reduced_colourings=sum(s['complete_reduced_colourings'] for s in source_reviews),
                all_26_same_Y_reductions_pass=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    opener = gzip.open if args.input.suffix == '.gz' else open
    with opener(args.input, 'rt') as handle:
        report = json.load(handle)
    result = review(report)
    result['input_sha256'] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in
                      {'local_fibre_reviews', 'source_reviews', 'sources_sha256'}}, sort_keys=True))


if __name__ == '__main__':
    main()
