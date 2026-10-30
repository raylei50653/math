#!/usr/bin/env python3
"""Finite original-source checks for the seven-vertex W5-plus-ear C-reduction.

Arbitrary-source classification, embedding and minimality are paper arguments.
This audit preserves every literal local fibre, and replays each reduced full
colouring against the original edges and both original complete side fibres.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

import networkx as nx

from four_color_twelve_cut_c6_verification import (
    ROOT, ROWS, ROW_INDEX, colourings, side_family, valid,
)

DEFAULT_INPUT = ROOT / 'audits/2026-10-29-twelve-cut-c6-e1a90fe/c6-sources.json.gz'
EXTRA_POSITIONS = (0, 2, 3, 4, 5)
# Rows of the paper table: columns give x0,...,x5,h for representatives 0,3,4.
PAPER_TABLE = {
    '101032': ('2312103', '2302103', '3203102'),
    '101202': ('2313130', '3203102', '3203102'),
    '101232': ('2310103', '0230132', '3203102'),
    '101302': ('3201302', '2302103', '0230132'),
    '301032': ('2312103', '1202103', '1203102'),
    '301202': ('1301302', '1203102', '1203102'),
    '301232': ('2310103', '1230102', '1203102'),
    '301302': ('1201302', '1202103', '1202103'),
}


def profile(extra):
    degrees = [1, 3, 1, 2, 2, 2]
    degrees[extra] += 1
    return degrees


def cross_pairs(extra):
    pairs, start = [], 0
    for x, degree in enumerate(profile(extra)):
        pairs.extend((x, (start + j) % 6) for j in range(degree))
        start += degree - 1
    assert start == 6 and len(pairs) == len(set(pairs)) == 12
    return pairs


def reflection(extra):
    # New representative labels are x'_i=x_(2-i), y'_j=y_(k-j).
    return (0, 3) if extra == 2 else (3, 2) if extra == 5 else (extra, None)


def diagonals(extra):
    _, offset = reflection(extra)
    common = [(1, 5), (2, 4), (2, 5)]
    return common if offset is None else [((offset-a) % 6, (offset-b) % 6) for a, b in common]


def table_lift(extra, beta):
    representative, offset = reflection(extra)
    transformed = beta if offset is None else tuple(beta[(offset-j) % 6] for j in range(6))
    named = [transformed[j] for j in (1, 2, 5)]
    assert len(set(named)) == 3
    named += sorted(set(range(4)) - set(named))
    inverse = {colour: i for i, colour in enumerate(named)}
    key = ''.join(str(inverse[colour]) for colour in transformed)
    encoded = PAPER_TABLE[key][(0, 3, 4).index(representative)]
    lifted = tuple(named[int(colour)] for colour in encoded)
    if offset is None:
        return lifted
    return tuple(lifted[(2-i) % 6] for i in range(6)) + (lifted[6],)


def paper_table_check():
    rows = []
    for beta_text, columns in PAPER_TABLE.items():
        beta = tuple(map(int, beta_text))
        assert [beta[j] for j in (1, 2, 5)] == [0, 1, 2]
        for representative, column in zip((0, 3, 4), columns):
            assigned = dict(zip(range(7, 13), beta)) | dict(zip(range(7), map(int, column)))
            assert valid(local_patch(representative), assigned)
            assert table_lift(representative, beta) == tuple(map(int, column))
        rows.append(dict(normalized_Y_boundary=beta,
                         representative_lifts={r: list(map(int, c)) for r, c in zip((0, 3, 4), columns)}))
    for extra in (2, 5):
        representative, offset = reflection(extra)
        reflected_cross = {((2-x) % 6, (offset-y) % 6) for x, y in cross_pairs(extra)}
        assert reflected_cross == set(cross_pairs(representative))
    return dict(normalized_rows=rows, representatives=[0, 3, 4],
                reflection_cross_edges_checked=True,
                all_24_table_cells_valid_on_original_edges=True)


def edges(graph):
    return sorted(tuple(sorted(e)) for e in graph.edges())


def local_patch(extra):
    graph = nx.Graph()
    graph.add_nodes_from(range(13))
    graph.add_edges_from((i, (i + 1) % 6) for i in range(6))
    graph.add_edge(0, 2)
    graph.add_edges_from((6, i) for i in (0, 2, 3, 4, 5))
    graph.add_edges_from((7 + i, 7 + (i + 1) % 6) for i in range(6))
    graph.add_edges_from((x, 7 + y) for x, y in cross_pairs(extra))
    assert nx.check_planarity(graph)[0]
    return graph


def noncrossing_diagonals(chords):
    for i, (a, b) in enumerate(chords):
        a, b = sorted((a, b))
        assert a != b
        for c, d in chords[i + 1:]:
            if len({a, b, c, d}) == 4:
                assert ((a < c < b) == (a < d < b))
    return True


def local_check(extra):
    graph = local_patch(extra)
    family = side_family(graph, sorted(graph), range(7, 13))
    assert family['internal_vertices'] == list(range(7))
    chords = diagonals(extra)
    noncrossing_diagonals(chords)
    reduced = graph.subgraph(range(7, 13)).copy()
    reduced.add_edges_from((7 + a, 7 + b) for a, b in chords)
    accepted = []
    for i, beta in enumerate(ROWS):
        assigned = dict(zip(range(7, 13), beta))
        if valid(reduced, assigned):
            assert family['complete_fibres'][i]
            lifted = table_lift(extra, beta)
            assert lifted in family['complete_fibres'][i]
            restored = assigned | dict(zip(range(7), lifted))
            assert valid(graph, restored)
            accepted.append(i)
    assert len(accepted) == 192
    assert len(colourings(reduced)) == 192
    return dict(extra_incidence_at_x=extra, X_cross_degrees=profile(extra),
                canonical_X_vertices=list(range(7)), canonical_Y_boundary=list(range(7, 13)),
                ordered_original_cross_edges=[(x, 7 + y) for x, y in cross_pairs(extra)],
                ordered_index_pairs=cross_pairs(extra),
                repeated_incidence_preserved=True,
                original_vertices=sorted(graph), original_edges=edges(graph),
                complete_local_extension_family=family,
                reduced_diagonal_indices=chords,
                diagonals_noncrossing=noncrossing_diagonals(chords),
                complete_reduced_boundary_indices=accepted,
                reduced_boundary_count=len(accepted),
                every_reduced_boundary_has_complete_lift=True)


def cyclic_equal(a, b):
    return len(a) == len(b) and any(a == b[i:] + b[:i] for i in range(len(b)))


def canonical_attachment(graph, side, boundary, opposite, ear):
    """Choose original IDs once; never merge equal-colour or repeated incidences."""
    candidates = []
    boundary = list(boundary)
    for direction in (1, -1):
        center = boundary.index(ear)
        xb = [boundary[(center + direction * (i - 1)) % 6] for i in range(6)]
        degrees = [len(set(graph[x]) - set(side)) for x in xb]
        extras = [r for r in EXTRA_POSITIONS if degrees == profile(r)]
        assert len(extras) == 1
        extra, = extras
        for reverse in (False, True):
            raw = list(reversed(opposite)) if reverse else list(opposite)
            for offset in range(6):
                yb = raw[offset:] + raw[:offset]
                expected = {(xb[x], yb[y]) for x, y in cross_pairs(extra)}
                actual = {(x, y) for x in side for y in graph[x] if y not in side}
                if expected == actual:
                    candidates.append((tuple(xb), tuple(yb), extra))
    assert candidates
    xb, yb, extra = min(candidates)
    return list(xb), list(yb), extra


def source_family_witness(family, assigned):
    beta = tuple(assigned[v] for v in family['ordered_boundary'])
    index = ROW_INDEX[beta]
    internal = [assigned[v] for v in family['internal_vertices']]
    assert internal in family['complete_fibres'][index]
    return dict(boundary_index=index, complete_internal_witness=internal)


def audit_case(case, local):
    graph = nx.Graph()
    graph.add_nodes_from(case['original_vertices'])
    graph.add_edges_from(case['original_edges'])
    reductions = []
    families = case['complete_side_families']
    direct = {tuple(row) for row in case['direct_original_colourings']}
    assert direct == set(colourings(graph))
    for cut_id, cut in enumerate(case['complete_twelve_cuts']):
        for side_name, opposite_name in (('X', 'Y'), ('Y', 'X')):
            family_id = cut[f'{side_name}_complete_family_id']
            opposite_id = cut[f'{opposite_name}_complete_family_id']
            family, other = families[family_id], families[opposite_id]
            classification = family['C6_CHORD_source_classification']
            if classification['type'] != 'W5_plus_triangular_ear':
                continue
            side = set(family['vertices'])
            hub = classification['original_hub']
            xb, yb, extra = canonical_attachment(
                graph, side, family['ordered_boundary'], other['ordered_boundary'],
                classification['original_ear'])
            assert set(xb) | {hub} == side and xb[1] == classification['original_ear']
            pairs = [(xb[x], yb[y]) for x, y in cross_pairs(extra)]
            original_order = [tuple(e) if side_name == 'X' else tuple(reversed(e))
                              for e in cut['ordered_original_cross_edges']]
            assert cyclic_equal(pairs, original_order) or cyclic_equal(pairs, list(reversed(original_order)))
            canonical_to_original = dict(zip(range(7), xb + [hub])) | dict(zip(range(7, 13), yb))
            local_graph = local_patch(extra)
            original_patch = graph.subgraph(side | set(yb)).copy()
            # The opposite side may itself have original chords; retain those.
            mapped_local = {frozenset((canonical_to_original[a], canonical_to_original[b]))
                            for a, b in local_graph.edges()}
            assert mapped_local <= {frozenset(e) for e in original_patch.edges()}
            assert {frozenset(e) for e in graph.subgraph(side).edges()} == {
                frozenset((canonical_to_original[a], canonical_to_original[b]))
                for a, b in local_graph.subgraph(range(7)).edges()}
            reduced = graph.subgraph(set(graph) - side).copy()
            added = [(yb[a], yb[b]) for a, b in diagonals(extra)]
            existing = [e for e in added if reduced.has_edge(*e)]
            assert all(a != b for a, b in added)
            reduced.add_edges_from(added)
            assert not nx.number_of_selfloops(reduced)
            assert len(reduced) == len(graph) - 7 and nx.check_planarity(reduced)[0]
            reduced_rows = colourings(reduced)
            assert reduced_rows
            witnesses = []
            local_fibres = local[extra]['complete_local_extension_family']['complete_fibres']
            for row in reduced_rows:
                assigned = dict(zip(sorted(reduced), row))
                beta = tuple(assigned[v] for v in yb)
                fibre = local_fibres[ROW_INDEX[beta]]
                assert fibre
                lifted = table_lift(extra, beta)
                assert lifted in fibre
                restored = assigned | dict(zip(xb + [hub], lifted))
                assert valid(graph, restored)
                assert all(restored[v] == assigned[v] for v in reduced)
                assert tuple(restored[v] for v in sorted(graph)) in direct
                x_witness = source_family_witness(family, restored)
                y_witness_before = source_family_witness(other, assigned)
                y_witness_after = source_family_witness(other, restored)
                assert y_witness_before == y_witness_after
                assert all(restored[a] != restored[b] for a, b in original_order)
                witnesses.append(dict(reduced_colouring=list(row),
                                      restored_original_colouring=[restored[v] for v in sorted(graph)],
                                      original_side_witness=x_witness,
                                      unchanged_opposite_witness=y_witness_after))
            reductions.append(dict(original_cut_id=cut_id, original_side=side_name,
                                   original_complete_side_family_id=family_id,
                                   original_opposite_complete_family_id=opposite_id,
                                   canonical_X_boundary=xb, canonical_Y_boundary=yb,
                                   original_hub=hub, original_ear=xb[1],
                                   canonical_profile_extra=extra,
                                   canonical_to_original_vertex_ids=canonical_to_original,
                                   source_ordered_original_cross_edges=original_order,
                                   canonical_ordered_original_cross_edges=pairs,
                                   original_faces_between_cross_edges=cut['original_face_between_successive_cross_edges'],
                                   original_incidence_multiplicities=cut['incidence_multiplicities'],
                                   added_chords=added, chords_already_in_original=existing,
                                   no_identifications=True, no_selfloops=True,
                                   reduced_simple_planar=True, deleted_original_vertices=sorted(side),
                                   reduced_vertices=sorted(reduced), reduced_edges=edges(reduced),
                                   reduced_colouring_count=len(reduced_rows),
                                   complete_colouring_lift_witnesses=witnesses,
                                   every_reduced_full_colouring_lifted_with_same_opposite_witness=True))
    return dict(name=case['name'], original_vertices=sorted(graph),
                reduction_count=len(reductions),
                profile_counts=dict(sorted(Counter(r['canonical_profile_extra'] for r in reductions).items())),
                reduced_colouring_count=sum(r['reduced_colouring_count'] for r in reductions),
                reductions=reductions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=DEFAULT_INPUT)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    with gzip.open(args.input, 'rt') as handle:
        previous = json.load(handle)
    local = {r: local_check(r) for r in EXTRA_POSITIONS}
    cases = [audit_case(case, local) for case in previous['cases']]
    assert sum(case['reduction_count'] for case in cases) == 48
    paths = [Path(__file__).resolve(), args.input.resolve(),
             ROOT / 'scripts/four_color_twelve_cut_c6_verification.py',
             ROOT / 'scripts/four_color_bond_perimeter_small_cuts.py']
    sources = {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):
               hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    report = dict(schema='four-color-twelve-cut-w5-ear-v1',
                  baseline='e1a90fea41702d7c98747716a5960198aecbecb3',
                  scope='All five necessary attachment profiles and 48 original sides in two fixed sources; universal topology/minimality are paper proofs.',
                  sources_sha256=sources, networkx_version=nx.__version__,
                  colour_frame=[0, 1, 2, 3], complete_literal_boundary_rows=ROWS,
                  original_complete_side_fibres='Retained unmodified in the hashed input certificate; witness references use case and family ID.',
                  paper_table=paper_table_check(),
                  local_profiles=[local[r] for r in EXTRA_POSITIONS], cases=cases)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(local_profiles=[dict(extra=r,
        nonempty_rows=local[r]['complete_local_extension_family']['nonempty_boundary_rows'],
        empty_rows=local[r]['complete_local_extension_family']['empty_boundary_rows'],
        complete_lifts=local[r]['complete_local_extension_family']['full_colouring_count'],
        reduced_boundaries=local[r]['reduced_boundary_count']) for r in EXTRA_POSITIONS],
        original_cases=[{k: c[k] for k in ('name', 'reduction_count', 'profile_counts', 'reduced_colouring_count')}
                        for c in cases]), sort_keys=True))


if __name__ == '__main__':
    main()
