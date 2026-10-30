#!/usr/bin/env python3
"""Original-source double-C6 audit and W6-side C-reduction checks.

The arbitrary-source topology and reduction are paper lemmas. This script checks
the 32 cuts in the preceding fixed-embedding certificate, preserving all literal
fibres (including empty rows), and independently enumerates original edges.
No Four Colour Theorem oracle or production colouring solver is used.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx

from four_color_bond_perimeter_small_cuts import original_faces


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / 'audits/2026-10-29-bond-perimeter-small-cuts-e1a90fe/small-cuts.json'
ROWS = list(itertools.product(range(4), repeat=6))
ROW_INDEX = {row: i for i, row in enumerate(ROWS)}


def colourings(graph, vertices=None):
    """Enumerate by original edges, without boundary projection or symmetry."""
    vertices = sorted(graph if vertices is None else vertices)
    induced = graph.subgraph(vertices)
    order = sorted(vertices, key=lambda v: (-induced.degree(v), v))
    assigned, result = {}, []

    def visit(i):
        if i == len(order):
            result.append(tuple(assigned[v] for v in vertices))
            return
        vertex = order[i]
        forbidden = {assigned[w] for w in induced[vertex] if w in assigned}
        for colour in range(4):
            if colour not in forbidden:
                assigned[vertex] = colour
                visit(i + 1)
                del assigned[vertex]

    visit(0)
    return sorted(result)


def valid(graph, assigned):
    return set(assigned) == set(graph) and all(assigned[u] != assigned[v] for u, v in graph.edges())


def digest_rows(rows):
    return hashlib.sha256(json.dumps(sorted(rows), separators=(',', ':')).encode()).hexdigest()


def ordered_strip(graph, faces, X, Y):
    crossing = sorted((u, v) for u in X for v in graph[u] if v in Y)
    assert len(crossing) == 12
    transitions, adjacency = {}, defaultdict(list)
    mixed = []
    for face in faces:
        xs, ys = set(face) & X, set(face) & Y
        if not xs or not ys:
            continue
        edges = sorted((u, v) for u in xs for v in ys if graph.has_edge(u, v))
        assert len(edges) == 2
        a, b = edges
        key = frozenset((a, b))
        assert key not in transitions
        transitions[key] = list(face)
        adjacency[a].append(b)
        adjacency[b].append(a)
        mixed.append(list(face))
    assert len(mixed) == 12 and set(adjacency) == set(crossing)
    assert all(len(v) == 2 for v in adjacency.values())
    start, previous = crossing[0], None
    current, sequence = start, []
    while not sequence or current != start:
        assert current not in sequence
        sequence.append(current)
        options = sorted(v for v in adjacency[current] if v != previous)
        previous, current = current, options[0]
    assert len(sequence) == 12 and set(sequence) == set(crossing)
    x_order = list(dict.fromkeys(x for x, _ in sequence))
    y_order = list(dict.fromkeys(y for _, y in sequence))
    assert len(x_order) == len(y_order) == 6
    xi, yi = {v: i for i, v in enumerate(x_order)}, {v: i for i, v in enumerate(y_order)}
    steps, original_steps = [], []
    for a, b in zip(sequence, sequence[1:] + sequence[:1]):
        if a[0] != b[0]:
            assert a[1] == b[1] and xi[b[0]] == (xi[a[0]] + 1) % 6
            assert graph.has_edge(a[0], b[0])
            steps.append('X')
        else:
            assert a[1] != b[1] and yi[b[1]] == (yi[a[1]] + 1) % 6
            assert graph.has_edge(a[1], b[1])
            steps.append('Y')
        original_steps.append(transitions[frozenset((a, b))])
    assert Counter(steps) == {'X': 6, 'Y': 6}
    multiplicities = [[sum(x == v for x, _ in sequence) for v in x_order],
                      [sum(y == v for _, y in sequence) for v in y_order]]
    assert all(1 <= degree <= 3 for counts in multiplicities for degree in counts)
    assert all(counts.count(1) == counts.count(3) for counts in multiplicities)
    return dict(X_boundary=x_order, Y_boundary=y_order,
                ordered_original_cross_edges=sequence,
                ordered_index_pairs=[(xi[x], yi[y]) for x, y in sequence],
                cyclic_step_word=''.join(steps),
                original_face_between_successive_cross_edges=original_steps,
                incidence_multiplicities=multiplicities)


def side_family(graph, vertices, boundary):
    vertices, boundary = sorted(vertices), list(boundary)
    internal = sorted(set(vertices) - set(boundary))
    rows = colourings(graph, vertices)
    fibres = [[] for _ in ROWS]
    for row in rows:
        assigned = dict(zip(vertices, row))
        beta = tuple(assigned[v] for v in boundary)
        fibres[ROW_INDEX[beta]].append(tuple(assigned[v] for v in internal))
    for fibre in fibres:
        fibre.sort()
    assert sum(map(len, fibres)) == len(rows)
    return dict(vertices=vertices, ordered_boundary=boundary, internal_vertices=internal,
                literal_boundary_encoding='lexicographic product(range(4), repeat=6); index=sum(beta[i]*4**(5-i))',
                complete_fibres=fibres, full_colouring_count=len(rows),
                nonempty_boundary_rows=sum(bool(f) for f in fibres),
                empty_boundary_rows=sum(not f for f in fibres),
                full_colouring_sha256=digest_rows(rows))


def classify_c6_source(graph, side, boundary, family):
    """Check the paper C6-CHORD classification on this original induced disk."""
    side, boundary = set(side), list(boundary)
    ring = {frozenset((boundary[i], boundary[(i + 1) % 6])) for i in range(6)}
    boundary_set = set(boundary)
    chords = sorted(tuple(sorted((u, v))) for u, v in graph.subgraph(boundary).edges()
                    if frozenset((u, v)) not in ring)
    interior = sorted(side - boundary_set)
    assert interior
    if chords:
        assert len(side) == 7 and len(interior) == 1 and len(chords) == 1
        hub, = interior
        u, v = chords[0]
        distance = (boundary.index(u) - boundary.index(v)) % 6
        assert distance in (2, 4), 'C6-CHORD excludes an opposite-vertex chord'
        ear_candidates = [w for w in boundary
                          if {boundary[(boundary.index(w) - 1) % 6],
                              boundary[(boundary.index(w) + 1) % 6]} == {u, v}]
        ear, = ear_candidates
        neighbours = boundary_set - {ear}
        expected = ring | {frozenset((u, v))} | {frozenset((hub, w)) for w in neighbours}
        assert {frozenset(e) for e in graph.subgraph(side).edges()} == expected
        # Check the whole literal family, not merely its positive support.
        for i, beta in enumerate(ROWS):
            assigned = dict(zip(boundary, beta))
            proper = all(assigned[a] != assigned[b] for a, b in
                         graph.subgraph(boundary).edges())
            expected_fibre = [(c,) for c in range(4)
                              if proper and c not in {assigned[w] for w in neighbours}]
            assert family['complete_fibres'][i] == expected_fibre
        return dict(type='W5_plus_triangular_ear', boundary_chords=chords,
                    original_hub=hub, original_ear=ear,
                    original_hub_neighbours=sorted(neighbours),
                    complete_hub_fibres_equal_absent_neighbour_colours=True)
    if len(side) == 7:
        hub = wheel_hub(graph, side, boundary)
        assert hub is not None
        return dict(type='W6', boundary_chords=[], original_hub=hub)
    assert len(side) >= 8
    return dict(type='large_chordless', boundary_chords=[])


def joined_colourings(graph, Xfamily, Yfamily, sequence):
    xb, yb = Xfamily['ordered_boundary'], Yfamily['ordered_boundary']
    xi, yi = {v: i for i, v in enumerate(xb)}, {v: i for i, v in enumerate(yb)}
    pairs = [(xi[x], yi[y]) for x, y in sequence]
    joined = set()
    accepted_pairs = []
    vertices = sorted(graph)
    for i, xf in enumerate(Xfamily['complete_fibres']):
        if not xf:
            continue
        alpha = ROWS[i]
        for j, yf in enumerate(Yfamily['complete_fibres']):
            if not yf:
                continue
            beta = ROWS[j]
            if any(alpha[p] == beta[q] for p, q in pairs):
                continue
            accepted_pairs.append((i, j))
            boundary = dict(zip(xb, alpha)) | dict(zip(yb, beta))
            for xcol in xf:
                for ycol in yf:
                    assigned = boundary | dict(zip(Xfamily['internal_vertices'], xcol)) | dict(zip(Yfamily['internal_vertices'], ycol))
                    assert valid(graph, assigned)
                    joined.add(tuple(assigned[v] for v in vertices))
    return joined, accepted_pairs


def wheel_hub(graph, side, boundary):
    internal = set(side) - set(boundary)
    if len(internal) != 1:
        return None
    hub, = internal
    expected = {tuple(sorted((boundary[i], boundary[(i + 1) % 6]))) for i in range(6)}
    expected |= {tuple(sorted((hub, v))) for v in boundary}
    actual = {tuple(sorted(e)) for e in graph.subgraph(side).edges()}
    return hub if actual == expected else None


def aligned_opposite(graph, xb, opposite):
    choices = []
    for raw in (opposite, list(reversed(opposite))):
        for offset in range(6):
            yb = raw[offset:] + raw[:offset]
            if all(set(graph[xb[i]]) & set(opposite) == {yb[i], yb[(i - 1) % 6]} for i in range(6)):
                choices.append(yb)
    assert choices
    return min(choices)


def lift_wheel(colours, xb, yb, hub):
    a, b, c = [colours[yb[i]] for i in (0, 2, 4)]
    assert len({a, b, c}) == 3
    missing, = set(range(4)) - {a, b, c}
    return colours | dict(zip(xb, (c, b, a, c, b, a))) | {hub: missing}


def reduction_check(graph, side, xb, opposite, hub):
    assert all(len(set(graph[x]) - set(side)) == 2 for x in xb)
    yb = aligned_opposite(graph, xb, opposite)
    reduced = graph.subgraph(set(graph) - set(side)).copy()
    triangle = [(yb[0], yb[2]), (yb[2], yb[4]), (yb[4], yb[0])]
    existing = [e for e in triangle if reduced.has_edge(*e)]
    reduced.add_edges_from(triangle)
    assert len(reduced) == len(graph) - 7 and nx.check_planarity(reduced)[0]
    rows = colourings(reduced)
    lifted = []
    for row in rows:
        assigned = dict(zip(sorted(reduced), row))
        restored = lift_wheel(assigned, xb, yb, hub)
        assert valid(graph, restored)
        assert all(restored[v] == assigned[v] for v in reduced)
        lifted.append(tuple(restored[v] for v in sorted(graph)))
    return dict(X_boundary=xb, aligned_Y_boundary=yb, original_hub=hub,
                deleted_original_vertices=sorted(side), added_triangle_edges=triangle,
                triangle_edges_already_in_original=existing,
                reduced_vertices=sorted(reduced), reduced_edges=sorted(tuple(sorted(e)) for e in reduced.edges()),
                all_reduced_colourings=rows, reduced_colouring_count=len(rows),
                every_reduced_colouring_lifted=True, lifted_original_colourings=lifted)


def local_check():
    # Local original patch: X rim0..5, hub6, opposite Y rim7..12.
    graph = nx.Graph()
    xb, yb, hub = list(range(6)), list(range(7, 13)), 6
    for i in range(6):
        graph.add_edges_from([(xb[i], xb[(i + 1) % 6]), (hub, xb[i]),
                              (yb[i], yb[(i + 1) % 6]),
                              (xb[i], yb[i]), (xb[i], yb[(i - 1) % 6])])
    assert nx.check_planarity(graph)[0]
    full = side_family(graph, sorted(graph), yb)
    proper, accepted, rejected = [], [], []
    for i, beta in enumerate(ROWS):
        if not all(beta[j] != beta[(j + 1) % 6] for j in range(6)):
            assert not full['complete_fibres'][i]
            continue
        proper.append(i)
        if len({beta[0], beta[2], beta[4]}) == 3:
            accepted.append(i)
            assigned = lift_wheel(dict(zip(yb, beta)), xb, yb, hub)
            assert valid(graph, assigned)
            assert tuple(assigned[v] for v in full['internal_vertices']) in full['complete_fibres'][i]
        if not full['complete_fibres'][i]:
            rejected.append(i)
    assert len(proper) == 732 and len(accepted) == 192
    assert full['nonempty_boundary_rows'] == 444 and len(rejected) == 288
    three_colour_control = (0, 1, 0, 2, 1, 2)
    assert ROW_INDEX[three_colour_control] in rejected
    assert not full['complete_fibres'][ROW_INDEX[three_colour_control]]
    return dict(original_vertices=sorted(graph), original_edges=sorted(tuple(sorted(e)) for e in graph.edges()),
                complete_local_extension_family=full,
                proper_C6_boundary_count=len(proper), triangle_boundary_count=len(accepted),
                complete_triangle_boundary_indices=accepted,
                all_triangle_boundaries_lifted=True,
                rejected_proper_C6_boundary_indices=rejected,
                rejected_without_triangle_control=list(ROWS[rejected[0]]),
                rejected_three_colour_C6_control=three_colour_control)


def audit_case(case):
    graph = nx.Graph()
    graph.add_nodes_from(case['vertices'])
    graph.add_edges_from(case['original_edges'])
    embedding = nx.PlanarEmbedding()
    embedding.set_data({int(v): neighbors for v, neighbors in case['original_rotation_cw'].items()})
    embedding.check_structure()
    assert set(map(frozenset, embedding.edges())) == set(map(frozenset, graph.edges()))
    assert original_faces(embedding) == case['original_oriented_faces']
    assert graph.number_of_edges() == 3 * len(graph) - 6
    assert min(dict(graph.degree()).values()) >= 5
    direct = set(colourings(graph))
    families, family_ids, cuts = [], {}, []
    reductions, words, degrees = [], Counter(), Counter()
    for cut in case['complete_unordered_cuts_at_most_12_sides_ge_3']:
        if cut['cut_size'] != 12 or min(cut['side_sizes']) < 7:
            continue
        X, Y = set(cut['X']), set(graph) - set(cut['X'])
        strip = ordered_strip(graph, case['original_oriented_faces'], X, Y)
        ids = []
        for side, boundary in ((X, strip['X_boundary']), (Y, strip['Y_boundary'])):
            key = (tuple(sorted(side)), tuple(boundary))
            if key not in family_ids:
                family_ids[key] = len(families)
                family = side_family(graph, side, boundary)
                family['C6_CHORD_source_classification'] = classify_c6_source(graph, side, boundary, family)
                families.append(family)
            ids.append(family_ids[key])
        joined, accepted_pairs = joined_colourings(graph, families[ids[0]], families[ids[1]], strip['ordered_original_cross_edges'])
        assert joined == direct
        cut_record = dict(X=sorted(X), Y=sorted(Y), **strip,
                          X_complete_family_id=ids[0], Y_complete_family_id=ids[1],
                          complete_compatible_boundary_index_pairs=accepted_pairs,
                          joined_original_colouring_count=len(joined),
                          joined_original_colouring_sha256=digest_rows(joined),
                          joined_set_equals_direct_original_edge_set=True,
                          W6_reduction_ids=[])
        for side, xb, opposite in ((X, strip['X_boundary'], strip['Y_boundary']),
                                   (Y, strip['Y_boundary'], strip['X_boundary'])):
            hub = wheel_hub(graph, side, xb)
            if hub is not None:
                cut_record['W6_reduction_ids'].append(len(reductions))
                reductions.append(reduction_check(graph, side, xb, opposite, hub))
        cuts.append(cut_record)
        words[strip['cyclic_step_word']] += 1
        for counts in strip['incidence_multiplicities']:
            degrees[tuple(counts)] += 1
    return dict(name=case['name'], original_vertices=case['vertices'], original_edges=case['original_edges'],
                original_rotation_cw=case['original_rotation_cw'], original_oriented_faces=case['original_oriented_faces'],
                direct_original_colourings=sorted(direct), direct_original_colouring_count=len(direct),
                direct_original_colouring_sha256=digest_rows(direct),
                complete_side_families=families, complete_twelve_cuts=cuts,
                W6_reductions=reductions,
                summary=dict(cuts=len(cuts), ordered_side_families=len(families),
                             W6_side_reductions=len(reductions),
                             C6_CHORD_classification_counts=dict(sorted(Counter(
                                 family['C6_CHORD_source_classification']['type'] for family in families).items())),
                             cyclic_step_word_counts=dict(sorted(words.items())),
                             incidence_multiplicity_counts=[dict(multiplicities=k, count=v) for k, v in sorted(degrees.items())]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=DEFAULT_INPUT)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    previous = json.loads(args.input.read_text())
    cases = [audit_case(case) for case in previous['cases'] if case['name'].startswith('capped-antiprism-')]
    assert [case['summary']['cuts'] for case in cases] == [25, 7]
    all_classes = Counter(family['C6_CHORD_source_classification']['type']
                          for case in cases for family in case['complete_side_families'])
    assert all_classes == {'W5_plus_triangular_ear': 48, 'W6': 2, 'large_chordless': 14}
    paths = [Path(__file__).resolve(), args.input.resolve(), ROOT / 'scripts/four_color_bond_perimeter_small_cuts.py']
    sources = {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    report = dict(schema='four-color-twelve-cut-c6-v1',
                  baseline='e1a90fea41702d7c98747716a5960198aecbecb3',
                  scope='Two fixed source triangulations and their complete 32 twelve-cuts; arbitrary-source reduction is a paper proof.',
                  sources_sha256=sources, networkx_version=nx.__version__,
                  colour_frame=[0, 1, 2, 3], complete_literal_boundary_rows=ROWS,
                  local_W6_reduction=local_check(), cases=cases)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(cases=[dict(name=c['name'], **c['summary']) for c in cases],
                          local_proper_C6=report['local_W6_reduction']['proper_C6_boundary_count'],
                          local_triangle_boundaries=report['local_W6_reduction']['triangle_boundary_count']), sort_keys=True))


if __name__ == '__main__':
    main()
