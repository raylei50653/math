#!/usr/bin/env python3
"""Exact eight-point C6 source classification and identity-preserving replay.

The arbitrary-source coverage/exclusions are paper proofs in the companion doc.
This enumerates all literal fibres and finite, explicitly embedded realizations;
no Four Colour Theorem or production solver is used.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx

from four_color_bond_perimeter_small_cuts import original_faces, short_cycle_sides
from four_color_twelve_cut_c6_verification import (
    ROWS, ROW_INDEX, colourings, digest_rows, joined_colourings, side_family, valid,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = (1, 2, 2, 1, 2, 2)
EXCLUDED = {(1, 2, 2, 1, 3, 3), (1, 3, 3, 1, 2, 2)}
UNIFORM = (2,) * 6
REPRESENTATIVES = [(1, 2, 2, 2, 2, 3), (1, 2, 2, 2, 3, 2),
                   (1, 2, 2, 3, 2, 2), (1, 2, 3, 1, 2, 3), (1, 2, 3, 1, 3, 2)]
CHORDS_A = [(0, 2), (2, 5), (3, 5)]
CHORDS_B = [(0, 3), (0, 4), (1, 3)]
TABLE_A = {
    '021012': ['13032320', '21023130', '21020331'],
    '021032': ['23032110', '13031320', '21020331'],
    '021302': ['21021330', '21021330', '21021330'],
    '021312': ['21020331', '21020331', '21020331'],
    '031012': ['21232301', '21023130', '21020331'],
    '031032': ['31032120', '12021330', '12021330'],
    '031302': ['12021330', '12021330', '12021330'],
    '031312': ['21020331', '21020331', '21020331'],
}
TABLE_B = {
    '020121': ['21320301', '21320301'],
    '020123': ['21320103', '21320103'],
    '023121': ['21020331', '21020331'],
    '023123': ['21023130', '23020113'],
    '030121': ['21230301', '21230301'],
    '030123': ['31230102', '31230102'],
    '032121': ['21020331', '12023230'],
    '032123': ['21023130', '31030221'],
}
TABLE_U = dict(zip(['012012', '012013', '012021', '012023', '012031', '012032'],
                   ['20120331', '20320113', '23130301', '30130221', '20120331', '20120331']))


def reduction_spec(profile):
    if profile == UNIFORM:
        return dict(kind='identify_opposite', identified_Y_indices=[0, 3])
    options = []
    for a in (0, 3):
        for sign in (1, -1):
            transformed = tuple(profile[(a + sign * i) % 6] for i in range(6))
            if transformed not in REPRESENTATIVES:
                continue
            for b in range(6):
                if {((a + sign * x) % 6, (b + sign * y) % 6)
                    for x, y in pairs(transformed)} == set(pairs(profile)):
                    options.append((transformed, a, sign, b))
    representative, a, sign, b = min(options)
    column = REPRESENTATIVES.index(representative)
    xmap = [(a + sign * i) % 6 for i in range(6)]
    ymap = [(b + sign * i) % 6 for i in range(6)]
    hubs = [6, 7] if set(xmap[:4]) == {0, 1, 2, 3} else [7, 6]
    canonical = CHORDS_A if column < 3 else CHORDS_B
    return dict(kind='add_noncrossing_chords', representative=representative,
                representative_column=column, a=a, sign=sign, b=b,
                representative_to_original_X=xmap + hubs,
                representative_to_original_Y=ymap,
                added_Y_index_pairs=[(ymap[i], ymap[j]) for i, j in canonical])


def paper_lift(profile, beta):
    spec = reduction_spec(profile)
    if profile == UNIFORM:
        assert beta[0] == beta[3]
        transformed, triangle, table, column = beta, (0, 1, 2), TABLE_U, None
    else:
        column = spec['representative_column']
        transformed = tuple(beta[j] for j in spec['representative_to_original_Y'])
        triangle = (0, 2, 5) if column < 3 else (0, 3, 4)
        table = TABLE_A if column < 3 else TABLE_B
    names = [transformed[j] for j in triangle]
    assert len(set(names)) == 3
    names += sorted(set(range(4)) - set(names))
    inverse = {c: i for i, c in enumerate(names)}
    key = ''.join(str(inverse[c]) for c in transformed)
    encoded = table[key] if column is None else table[key][column if column < 3 else column - 3]
    new_lift = [names[int(c)] for c in encoded]
    if profile == UNIFORM:
        return tuple(new_lift)
    result = [None] * 8
    for i, original in enumerate(spec['representative_to_original_X']):
        result[original] = new_lift[i]
    return tuple(result)


def reduced_boundary_accepts(profile, beta):
    if not all(beta[i] != beta[(i + 1) % 6] for i in range(6)):
        return False
    spec = reduction_spec(profile)
    if profile == UNIFORM:
        return beta[0] == beta[3]
    return all(beta[i] != beta[j] for i, j in spec['added_Y_index_pairs'])


def disk_edges(shift=0, offset=0):
    rim = lambda i: offset + (i + shift) % 6
    return ([(rim(i), rim(i + 1)) for i in range(6)]
            + [(offset + 6, rim(i)) for i in range(4)]
            + [(offset + 7, rim(i)) for i in (0, 3, 4, 5)]
            + [(offset + 6, offset + 7)])


def disk_faces(shift=0, offset=0):
    rim = lambda i: offset + (i + shift) % 6
    h, k = offset + 6, offset + 7
    return ([(h, rim(i), rim(i + 1)) for i in range(3)]
            + [(k, rim(i), rim(i + 1)) for i in range(3, 6)]
            + [(h, k, rim(0)), (k, h, rim(3))])


def pairs(profile):
    result, start = [], 0
    for x, degree in enumerate(profile):
        result.extend((x, (start + j) % 6) for j in range(degree))
        start += degree - 1
    assert start == 6 and len(result) == len(set(result)) == 12
    return result


def local_patch(profile):
    graph = nx.Graph()
    graph.add_edges_from(disk_edges())
    graph.add_edges_from((8 + i, 8 + (i + 1) % 6) for i in range(6))
    graph.add_edges_from((x, 8 + y) for x, y in pairs(profile))
    return graph


def mixed_faces(profile):
    cross = [(x, 8 + y) for x, y in pairs(profile)]
    return [tuple(sorted(set(a + b))) for a, b in zip(cross, cross[1:] + cross[:1])]


def triangular_cap(shift):
    rim = lambda j: 8 + (shift + j) % 6
    return ([(14 + i, rim(2 * i + j), rim(2 * i + j + 1))
             for i in range(3) for j in range(2)]
            + [(14 + i, 14 + (i + 1) % 3, rim(2 * i + 2)) for i in range(3)]
            + [(14, 15, 16)])


def edge_list(graph):
    return sorted(tuple(sorted(e)) for e in graph.edges())


def source(profile, cap_kind, shift):
    expected = disk_faces() + mixed_faces(profile)
    expected += disk_faces(shift, 8) if cap_kind == 'two_internal' else triangular_cap(shift)
    graph = nx.Graph()
    for face in expected:
        graph.add_edges_from(zip(face, face[1:] + face[:1]))
    assert edge_list(graph.subgraph(range(14))) == edge_list(local_patch(profile))
    return graph, expected


def check_source(graph, expected):
    if min(dict(graph.degree()).values()) < 5:
        return None
    planar, embedding = nx.check_planarity(graph)
    assert planar
    faces = original_faces(embedding)
    assert {frozenset(f) for f in faces} == {frozenset(f) for f in expected}
    assert len(faces) == len(expected) == 2 * len(graph) - 4
    try:
        cycles = short_cycle_sides(graph, faces)
    except AssertionError:
        return None
    return embedding, faces, cycles


def arithmetic_short_cycle_certificate(graph, cycles):
    """Exact integer trace identities independently check the paper source table."""
    vertices = sorted(graph)
    adjacency = [[int(graph.has_edge(a, b)) for b in vertices] for a in vertices]
    power = adjacency
    traces = {}
    for exponent in range(2, 6):
        power = [[sum(power[i][k] * adjacency[k][j] for k in range(len(vertices)))
                  for j in range(len(vertices))] for i in range(len(vertices))]
        if exponent >= 3:
            traces[exponent] = sum(power[i][i] for i in range(len(vertices)))
    degrees = [graph.degree(v) for v in vertices]
    wedges = sum(d * (d - 1) // 2 for d in degrees)
    m, f, n5 = graph.number_of_edges(), 2 * len(graph) - 4, degrees.count(5)
    assert traces[3] == 6 * f
    assert traces[4] == 8 * m + 2 * m + 4 * wedges
    assert traces[5] == 10 * (3 * f + n5) + 20 * wedges
    assert Counter(len(c['cycle']) for c in cycles) == {3: f, 4: m, 5: 3 * f + n5}
    return dict(n=len(graph), m=m, f=f, n5=n5, sum_choose_degree_2=wedges,
                adjacency_power_traces=traces, C3=f, C4=m, C5=3 * f + n5,
                all_counts_equal_facial_or_at_most_one_interior_cycles=True)


def induced_exhaustion():
    ring = [(i, (i + 1) % 6) for i in range(6)]
    checked, accepted = 0, []
    for a in itertools.combinations(range(6), 4):
        for b in itertools.combinations(range(6), 4):
            checked += 1
            g = nx.Graph(ring + [(6, 7)] + [(6, i) for i in a] + [(7, i) for i in b])
            # A new vertex on the OTHER side forces the nominated C6 to be facial.
            augmented = g.copy()
            augmented.add_edges_from((8, i) for i in range(6))
            if nx.check_planarity(augmented)[0]:
                accepted.append(edge_list(g))
    expected = []
    for shift in range(3):
        g = nx.Graph(disk_edges(shift))
        expected.append(edge_list(g))
        expected.append(edge_list(nx.relabel_nodes(g, {6: 7, 7: 6})))
    assert checked == 225 and sorted(accepted) == sorted(expected) and len(accepted) == 6
    return dict(spoke_pairs_checked=checked, boundary_facial_planar_cases=accepted,
                unique_type_up_to_rim_dihedral_and_internal_swap=True)


def local_record(profile):
    graph = local_patch(profile)
    family = side_family(graph, sorted(graph), range(8, 14))
    assert family['internal_vertices'] == list(range(8))
    # Independent literal 4096 x16 enumeration for the original eight-point disk.
    xgraph = graph.subgraph(range(8)).copy()
    xf = side_family(xgraph, range(8), range(6))
    for i, alpha in enumerate(ROWS):
        brute = []
        for internal in itertools.product(range(4), repeat=2):
            if valid(xgraph, dict(enumerate(alpha + internal))):
                brute.append(internal)
        assert brute == xf['complete_fibres'][i]
    excluded = profile in EXCLUDED
    obstruction = None
    if excluded:
        cycle = ([4, 5, 8, 9, 10] if profile == (1, 2, 2, 1, 3, 3)
                 else [1, 2, 12, 13, 8])
        assert all(graph.has_edge(a, b) for a, b in zip(cycle, cycle[1:] + cycle[:1]))
        obstruction = dict(original_cycle=cycle,
                           one_side_contains_original_vertices=sorted(set(range(8)) - set(cycle)),
                           other_side_contains_all_opposite_internal_vertices=True,
                           side_size_lower_bounds=[6, 2], excluded_by='S5')
    reduction = None
    if not excluded:
        accepted = []
        for index, beta in enumerate(ROWS):
            if reduced_boundary_accepts(profile, beta):
                lifted = paper_lift(profile, beta)
                assert lifted in family['complete_fibres'][index]
                assert valid(graph, dict(zip(range(8, 14), beta)) | dict(enumerate(lifted)))
                accepted.append(index)
        assert len(accepted) == (144 if profile == UNIFORM else 192)
        reduction = dict(**reduction_spec(profile), complete_accepted_boundary_indices=accepted,
                         all_accepted_rows_lift_by_paper_table=True)
    return dict(X_cross_degrees=profile,
                increments=tuple(a - b for a, b in zip(profile, BASE)),
                Y_cross_degrees=[sum(y == j for _, y in pairs(profile)) for j in range(6)],
                status='excluded_by_mixed_S5' if excluded else 'realizable',
                original_X_vertices=list(range(8)), original_Y_boundary=list(range(8, 14)),
                original_local_edges=edge_list(graph),
                ordered_original_cross_edges=[(x, 8 + y) for x, y in pairs(profile)],
                ordered_index_pairs=pairs(profile),
                original_mixed_faces_between_successive_cross_edges=mixed_faces(profile),
                complete_original_X_family=xf,
                complete_eight_point_lifts_over_Y=family, C_reduction=reduction,
                mixed_S5_obstruction=obstruction)


def reduction_replay(graph, profile, direct, xfamily, yfamily):
    spec = reduction_spec(profile)
    yvertices = sorted(set(graph) - set(range(8)))
    reduced = graph.subgraph(yvertices).copy()
    pullback = {v: v for v in yvertices}
    if profile == UNIFORM:
        assert not graph.has_edge(8, 11)
        reduced = nx.contracted_nodes(reduced, 8, 11, self_loops=False)
        pullback[11] = 8
        expected_drop = 9
    else:
        added = [(8 + a, 8 + b) for a, b in spec['added_Y_index_pairs']]
        # Endpoints lie on a convex six-gon; check all chord pairs directly.
        for (a, b), (c, d) in itertools.combinations(spec['added_Y_index_pairs'], 2):
            a, b = sorted((a, b))
            if len({a, b, c, d}) == 4:
                assert ((a < c < b) == (a < d < b))
        reduced.add_edges_from(added)
        expected_drop = 8
    assert len(reduced) == len(graph) - expected_drop
    assert not nx.number_of_selfloops(reduced) and nx.check_planarity(reduced)[0]
    direct_set = set(direct)
    witnesses = []
    for row in colourings(reduced):
        assigned = dict(zip(sorted(reduced), row))
        original_y = {v: assigned[pullback[v]] for v in yvertices}
        beta = tuple(original_y[v] for v in range(8, 14))
        assert reduced_boundary_accepts(profile, beta)
        lifted = paper_lift(profile, beta)
        restored = original_y | dict(enumerate(lifted))
        assert valid(graph, restored)
        assert tuple(restored[v] for v in sorted(graph)) in direct_set
        alpha = tuple(restored[v] for v in range(6))
        xinternal = tuple(restored[v] for v in (6, 7))
        yinternal = tuple(original_y[v] for v in yfamily['internal_vertices'])
        assert xinternal in xfamily['complete_fibres'][ROW_INDEX[alpha]]
        assert yinternal in yfamily['complete_fibres'][ROW_INDEX[beta]]
        assert all(restored[v] == original_y[v] for v in yvertices)
        witnesses.append(dict(reduced_colouring=row,
                              unchanged_original_Y_colouring=[original_y[v] for v in yvertices],
                              unchanged_opposite_boundary_index=ROW_INDEX[beta],
                              unchanged_opposite_complete_internal_witness=yinternal,
                              restored_original_colouring=[restored[v] for v in sorted(graph)]))
    assert witnesses
    return dict(specification=spec, reduced_vertices=sorted(reduced),
                reduced_edges=edge_list(reduced), original_Y_to_reduced_vertex=pullback,
                vertex_drop=expected_drop, simple_planar_strictly_smaller=True,
                complete_reduced_colouring_count=len(witnesses),
                complete_reduced_colourings_and_unchanged_witness_lifts=witnesses)


def replay_source(profile, cap_kind, shift, checked):
    graph, expected = source(profile, cap_kind, shift)
    embedding, faces, cycles = checked
    cross = [(x, 8 + y) for x, y in pairs(profile)]
    by_face = {frozenset(f): i for i, f in enumerate(faces)}
    mix_ids = [by_face[frozenset(f)] for f in mixed_faces(profile)]
    assert len(set(mix_ids)) == 12
    xfamily = side_family(graph, range(8), range(6))
    yfamily = side_family(graph, range(8, len(graph)), range(8, 14))
    joined, accepted = joined_colourings(graph, xfamily, yfamily, cross)
    direct = colourings(graph)
    assert joined == set(direct)
    cycle_counts = Counter((len(c['cycle']), min(map(len, c['side_vertices']))) for c in cycles)
    reduction = reduction_replay(graph, profile, direct, xfamily, yfamily)
    arithmetic = arithmetic_short_cycle_certificate(graph, cycles)
    return dict(X_cross_degrees=profile, Y_cap_kind=cap_kind, Y_cap_shift=shift,
                original_vertices=sorted(graph), original_edges=edge_list(graph),
                original_rotation_cw={v: list(embedding.neighbors_cw_order(v)) for v in sorted(graph)},
                original_oriented_faces=faces, original_short_cycles_with_complete_side_vertices=cycles,
                arithmetic_short_cycle_certificate=arithmetic,
                cycle_counts=[dict(length=k[0], smaller_side_size=k[1], count=v)
                              for k, v in sorted(cycle_counts.items())],
                original_X_vertices=list(range(8)), original_Y_vertices=list(range(8, len(graph))),
                ordered_X_boundary=list(range(6)), ordered_Y_boundary=list(range(8, 14)),
                ordered_original_cross_edges=cross,
                cyclic_step_word=''.join('X' if a[0] != b[0] else 'Y'
                                        for a, b in zip(cross, cross[1:] + cross[:1])),
                original_mixed_face_ids_between_successive_cross_edges=mix_ids,
                original_mixed_faces_between_successive_cross_edges=[faces[i] for i in mix_ids],
                complete_X_family=xfamily, complete_Y_family=yfamily,
                complete_compatible_boundary_index_pairs=accepted,
                complete_direct_original_colourings=direct,
                direct_original_colouring_count=len(direct),
                direct_original_colouring_sha256=digest_rows(direct),
                complete_join_equals_direct_original_edges=True, C_reduction=reduction)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    profiles = [d for d in itertools.product(range(1, 4), repeat=6)
                if sum(d) == 12 and all(a >= b for a, b in zip(d, BASE))]
    assert len(profiles) == 17
    local = [local_record(d) for d in profiles]
    realizations, cap_attempts = [], []
    for d in profiles:
        choices = []
        for shift in range(3):
            graph, faces = source(d, 'two_internal', shift)
            checked = check_source(graph, faces)
            cap_attempts.append(dict(profile=d, Y_internal_count=2, shift=shift,
                                     satisfies_all_hypotheses=checked is not None))
            if checked is not None:
                choices.append(('two_internal', shift, checked))
        if not choices and d not in EXCLUDED:
            for shift in range(2):
                graph, faces = source(d, 'three_internal_triangle', shift)
                checked = check_source(graph, faces)
                cap_attempts.append(dict(profile=d, Y_internal_count=3, shift=shift,
                                         satisfies_all_hypotheses=checked is not None))
                if checked is not None:
                    choices.append(('three_internal_triangle', shift, checked))
        assert bool(choices) == (d not in EXCLUDED)
        if choices:
            kind, shift, checked = choices[0]
            realizations.append(replay_source(d, kind, shift, checked))
    assert Counter(len(r['original_Y_vertices']) for r in realizations) == {8: 13, 9: 2}
    paths = [Path(__file__).resolve(), ROOT / 'scripts/four_color_twelve_cut_c6_verification.py',
             ROOT / 'scripts/four_color_bond_perimeter_small_cuts.py']
    report = dict(schema='four-color-twelve-cut-eight-side-v1',
                  baseline='e1a90fea41702d7c98747716a5960198aecbecb3',
                  scope='Unique eight-point original disk; 17 degree candidates, 2 paper exclusions, 15 actual sources and C reductions. General cuts and both sides >=9 remain OPEN.',
                  colour_frame=[0, 1, 2, 3], complete_literal_boundary_rows=ROWS,
                  sources_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                  networkx_version=nx.__version__, induced_exhaustion=induced_exhaustion(),
                  all_degree_necessary_profiles=local, cap_attempts=cap_attempts,
                  paper_tables=dict(A=TABLE_A, B=TABLE_B, uniform=TABLE_U),
                  realizations=realizations)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(degree_profiles=len(local), excluded=2, realizable=len(realizations),
                         source_sizes=Counter(len(r['original_vertices']) for r in realizations),
                         original_X_colourings=local[0]['complete_original_X_family']['full_colouring_count'],
                         joined_original_colourings=sum(r['direct_original_colouring_count'] for r in realizations),
                         complete_reduced_colourings=sum(r['C_reduction']['complete_reduced_colouring_count'] for r in realizations)), sort_keys=True))


if __name__ == '__main__':
    main()
