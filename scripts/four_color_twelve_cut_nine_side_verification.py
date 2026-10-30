#!/usr/bin/env python3
"""Nine-point double-C6 source classification with complete literal R_d fibres.

The coverage argument is a paper proof in the companion document.  The opposite
proxy hub below is only a topological placeholder, never an original source or
colouring witness. No four-colour theorem oracle is used.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx

from four_color_bond_perimeter_small_cuts import original_faces, short_cycles
from four_color_twelve_cut_c6_verification import (
    ROWS, ROW_INDEX, colourings, digest_rows, joined_colourings, side_family, valid,
)
from four_color_twelve_cut_eight_side_verification import (
    arithmetic_short_cycle_certificate, check_source, edge_list, pairs,
)

ROOT = Path(__file__).resolve().parents[1]
BASE = (1, 2, 1, 2, 1, 2)
PROFILES = [d for d in itertools.product(range(1, 4), repeat=6)
            if sum(d) == 12 and all(a >= b for a, b in zip(d, BASE))]
EXCLUDED = {(1, 2, 1, 2, 3, 3), (1, 2, 1, 3, 2, 3), (1, 2, 1, 3, 3, 2),
            (1, 2, 3, 3, 1, 2), (1, 3, 2, 3, 1, 2), (1, 3, 3, 2, 1, 2),
            (2, 3, 1, 2, 1, 3), (3, 2, 1, 2, 1, 3), (3, 3, 1, 2, 1, 2)}


def disk_faces(offset=0, shift=0):
    rim = lambda j: offset + (j + shift) % 6
    hub = lambda j: offset + 6 + j % 3
    return ([(hub(i), rim(2*i+j), rim(2*i+j+1)) for i in range(3) for j in range(2)]
            + [(hub(i), hub(i+1), rim(2*i+2)) for i in range(3)]
            + [(hub(0), hub(1), hub(2))])


def ten_disk_faces(offset=9, shift=0):
    """Four interior points on a 1,2,1,2 boundary fan cycle, diagonal r0r2."""
    rim = lambda j: offset + (j + shift) % 6
    hub = lambda j: offset + 6 + j % 4
    starts, faces = (0, 1, 3, 4, 6), []
    for i in range(4):
        faces.extend((hub(i), rim(j), rim(j+1)) for j in range(starts[i], starts[i+1]))
        faces.append((hub(i), hub(i+1), rim(starts[i+1])))
    return faces + [(hub(0), hub(1), hub(2)), (hub(0), hub(2), hub(3))]


def graph_from_faces(faces):
    graph = nx.Graph()
    for f in faces:
        graph.add_edges_from(zip(f, f[1:] + f[:1]))
    return graph


def cross_edges(profile):
    return [(x, 9+y) for x, y in pairs(profile)]


def mixed_faces(profile):
    cross = cross_edges(profile)
    return [tuple(sorted(set(a+b))) for a, b in zip(cross, cross[1:] + cross[:1])]


def local_graph(profile):
    graph = graph_from_faces(disk_faces() + mixed_faces(profile))
    graph.add_edges_from((9+i, 9+(i+1) % 6) for i in range(6))
    return graph


def orbit(profile):
    return sorted({tuple(profile[(a + sign*i) % 6] for i in range(6))
                   for a in (0, 2, 4) for sign in (1, -1)})


def induced_exhaustion():
    """Independent enumeration after the Euler/degree argument forces K3+9 spokes."""
    choices = list(itertools.combinations(range(6), 3))
    rim = [(i, (i+1) % 6) for i in range(6)]
    accepted, checked = [], 0
    for n0, n1, n2 in itertools.product(choices, repeat=3):
        checked += 1
        graph = nx.Graph(rim + [(6, 7), (7, 8), (8, 6)]
                         + [(6+i, j) for i, ns in enumerate((n0, n1, n2)) for j in ns])
        # The extra vertex is strictly outside the designated C6 disk.
        graph.add_edges_from((9, j) for j in range(6))
        if nx.check_planarity(graph)[0]:
            accepted.append(edge_list(graph.subgraph(range(9))))
    expected = []
    for shift in (0, 1):
        graph = graph_from_faces(disk_faces(shift=shift))
        for perm in itertools.permutations(range(6, 9)):
            expected.append(edge_list(nx.relabel_nodes(graph, dict(zip(range(6, 9), perm)))))
    assert checked == 8000 and len(accepted) == 12 and sorted(accepted) == sorted(expected)
    return dict(ordered_three_neighbourhood_choices_checked=checked,
                boundary_facial_planar_original_edge_lists=sorted(accepted),
                unique_type_up_to_dihedral_rim_and_internal_permutation=True)


def disk_family():
    graph = graph_from_faces(disk_faces())
    family = side_family(graph, range(9), range(6))
    for index, alpha in enumerate(ROWS):
        expected = [p for p in itertools.product(range(4), repeat=3)
                    if all(alpha[i] != alpha[(i+1) % 6] for i in range(6))
                    and len(set(p)) == 3
                    and all(p[i] not in {alpha[(2*i+j) % 6] for j in range(3)} for i in range(3))]
        assert expected == family['complete_fibres'][index]
    assert family['full_colouring_count'] == 432 and family['nonempty_boundary_rows'] == 336
    return family


def forced_short_cycle_audit(profile):
    """All original-only cycles of length<=5, with exact side sets in a proxy cap.

    The proxy hub stands for ALL unknown opposite interior vertices, at least
    three. Its six incident triangles replace only the opposite open disk.
    Every inspected cycle avoids it, so the same original sides remain valid
    for every opposite completion.
    """
    proxy = 15
    faces = (disk_faces() + mixed_faces(profile)
             + [(proxy, 9+i, 9+(i+1) % 6) for i in range(6)])
    graph = graph_from_faces(faces)
    planar, embedding = nx.check_planarity(graph)
    assert planar
    assert {frozenset(f) for f in original_faces(embedding)} == {frozenset(f) for f in faces}
    dual, edge_faces = nx.Graph(), defaultdict(list)
    dual.add_nodes_from(range(len(faces)))
    for j, face in enumerate(faces):
        for u, v in zip(face, face[1:] + face[:1]):
            edge_faces[tuple(sorted((u, v)))].append(j)
    for ff in edge_faces.values():
        assert len(ff) == 2
        dual.add_edge(*ff)
    records = []
    for cycle in short_cycles(graph):
        if proxy in cycle:
            continue
        cut = dual.copy()
        for u, v in zip(cycle, cycle[1:] + cycle[:1]):
            cut.remove_edge(*edge_faces[tuple(sorted((u, v)))])
        components = sorted(map(sorted, nx.connected_components(cut)))
        assert len(components) == 2
        sides = []
        for cc in components:
            vertices = set().union(*(set(faces[j]) for j in cc)) - set(cycle)
            has_unknown = proxy in vertices
            fixed = sorted(vertices - {proxy})
            sides.append(dict(original_local_vertices=fixed,
                              includes_all_opposite_interior_vertices=has_unknown,
                              minimum_opposite_interior_count=3 if has_unknown else 0,
                              original_vertex_count_lower_bound=len(fixed) + (3 if has_unknown else 0)))
        sides.sort(key=lambda s: s['original_local_vertices'])
        lower = [s['original_vertex_count_lower_bound'] for s in sides]
        violates = min(lower) > (0 if len(cycle) <= 4 else 1)
        records.append(dict(original_cycle=cycle,
                            is_mixed=any(v < 9 for v in cycle) and any(v >= 9 for v in cycle),
                            original_sides=sides, violates_S34_or_S5=violates))
    bad = [r for r in records if r['violates_S34_or_S5']]
    assert bool(bad) == (profile in EXCLUDED)
    assert all(len(r['original_cycle']) == 5 and r['is_mixed'] for r in bad)
    return dict(proxy_vertex=proxy, proxy_is_not_original=True,
                proxy_oriented_faces=faces,
                all_original_only_short_cycles=records,
                exhaustive_original_mixed_short_cycle_counts=dict(Counter(len(r['original_cycle']) for r in records if r['is_mixed'])),
                forced_obstructions=bad,
                unknown_opposite_edges_and_cycles_not_screened=True)


def local_record(profile, xfamily):
    graph = local_graph(profile)
    family = side_family(graph, range(15), range(9, 15))
    assert family['internal_vertices'] == list(range(9))
    # An independent constructive join: enumerate all complete original X
    # colourings, then all Y tuples from the twelve simultaneous inequalities.
    expected = [[] for _ in ROWS]
    xrows = colourings(graph.subgraph(range(9)))
    for xrow in xrows:
        allowed = [tuple(c for c in range(4)
                         if all(c != xrow[x] for x, y in pairs(profile) if y == j)) for j in range(6)]
        for beta in itertools.product(*allowed):
            if all(beta[i] != beta[(i+1) % 6] for i in range(6)):
                expected[ROW_INDEX[beta]].append(xrow)
    assert [sorted(f) for f in expected] == family['complete_fibres']
    audit = forced_short_cycle_audit(profile)
    reduction = None
    if profile not in EXCLUDED:
        from four_color_twelve_cut_nine_side_reduction import (
            paper_lift, reduced_boundary_accepts, reduction_spec,
        )
        accepted = []
        for index, beta in enumerate(ROWS):
            if reduced_boundary_accepts(profile, beta):
                lifted = paper_lift(profile, beta)
                assert lifted in family['complete_fibres'][index]
                assert valid(graph, dict(zip(range(9, 15), beta)) | dict(enumerate(lifted)))
                accepted.append(index)
        assert len(accepted) == (144 if profile == (2,)*6 else 192)
        reduction = dict(**reduction_spec(profile), complete_accepted_boundary_indices=accepted,
                         all_accepted_rows_lift_by_paper_table=True)
    return dict(X_cross_degrees=profile,
                Y_cross_degrees=[sum(y == j for _, y in pairs(profile)) for j in range(6)],
                increments=[a-b for a, b in zip(profile, BASE)],
                degree_orbit_representative=min(orbit(profile)),
                status='excluded_by_forced_original_mixed_S5' if profile in EXCLUDED else 'locally_admissible',
                original_X_vertices=list(range(9)), original_Y_boundary=list(range(9, 15)),
                ordered_original_cross_edges=cross_edges(profile), ordered_index_pairs=pairs(profile),
                original_mixed_faces_between_successive_cross_edges=mixed_faces(profile),
                original_local_edges=edge_list(graph),
                complete_nine_point_lifts_R_d_over_Y=family,
                independent_original_edge_DFS_equals_constructive_complete_join=True,
                original_short_cycle_audit=audit, C_reduction=reduction)


def source(profile, shift, kind='three_internal_triangle'):
    cap = disk_faces(offset=9, shift=shift) if kind == 'three_internal_triangle' else ten_disk_faces(shift=shift)
    faces = disk_faces() + mixed_faces(profile) + cap
    return graph_from_faces(faces), faces


def reduction_replay(graph, profile, direct, xfamily, yfamily):
    from four_color_twelve_cut_nine_side_reduction import (
        paper_lift, reduced_boundary_accepts, reduction_spec,
    )
    spec = reduction_spec(profile)
    yvertices = sorted(set(graph) - set(range(9)))
    reduced = graph.subgraph(yvertices).copy()
    pullback = {v: v for v in yvertices}
    if spec['kind'] == 'identify_opposite':
        i, j = spec['identified_Y_indices']
        assert not graph.has_edge(9+i, 9+j)
        reduced = nx.contracted_nodes(reduced, 9+i, 9+j, self_loops=False)
        pullback[9+j] = 9+i
        expected_drop = 10
    else:
        chords = spec['added_Y_index_pairs']
        for (a, b), (c, d) in itertools.combinations(chords, 2):
            a, b = sorted((a, b))
            if len({a, b, c, d}) == 4:
                assert ((a < c < b) == (a < d < b))
        reduced.add_edges_from((9+a, 9+b) for a, b in chords)
        expected_drop = 9
    assert len(reduced) == len(graph) - expected_drop
    assert not nx.number_of_selfloops(reduced) and nx.check_planarity(reduced)[0]
    direct_set, witnesses = set(direct), []
    for row in colourings(reduced):
        assigned = dict(zip(sorted(reduced), row))
        original_y = {v: assigned[pullback[v]] for v in yvertices}
        beta = tuple(original_y[v] for v in range(9, 15))
        assert reduced_boundary_accepts(profile, beta)
        lifted = paper_lift(profile, beta)
        restored = original_y | dict(enumerate(lifted))
        assert valid(graph, restored)
        assert tuple(restored[v] for v in sorted(graph)) in direct_set
        alpha = tuple(restored[v] for v in range(6))
        xinternal = tuple(restored[v] for v in (6, 7, 8))
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


def replay_source(profile, shift, kind, graph, checked, xfamily):
    embedding, faces, cycles = checked
    yvertices = sorted(set(graph) - set(range(9)))
    yfamily = side_family(graph, yvertices, range(9, 15))
    joined, accepted = joined_colourings(graph, xfamily, yfamily, cross_edges(profile))
    direct = colourings(graph)
    assert joined == set(direct)
    by_face = {frozenset(f): j for j, f in enumerate(faces)}
    mixed_ids = [by_face[frozenset(f)] for f in mixed_faces(profile)]
    assert len(set(mixed_ids)) == 12
    return dict(X_cross_degrees=profile, Y_cap_shift=shift, Y_cap_kind=kind,
                original_vertices=sorted(graph), original_edges=edge_list(graph),
                original_rotation_cw={v: list(embedding.neighbors_cw_order(v)) for v in sorted(graph)},
                original_oriented_faces=faces,
                original_short_cycles_with_complete_side_vertices=cycles,
                arithmetic_short_cycle_certificate=arithmetic_short_cycle_certificate(graph, cycles),
                original_X_vertices=list(range(9)), original_Y_vertices=yvertices,
                ordered_X_boundary=list(range(6)), ordered_Y_boundary=list(range(9, 15)),
                ordered_original_cross_edges=cross_edges(profile),
                original_mixed_face_ids_between_successive_cross_edges=mixed_ids,
                complete_X_family=xfamily, complete_Y_family=yfamily,
                complete_compatible_boundary_index_pairs=accepted,
                complete_direct_original_colourings=direct,
                direct_original_colouring_count=len(direct),
                direct_original_colouring_sha256=digest_rows(direct),
                complete_join_equals_direct_original_edges=True,
                C_reduction=reduction_replay(graph, profile, direct, xfamily, yfamily))


def main():
    from four_color_twelve_cut_nine_side_reduction import TABLES, SPECS, validate_paper_tables
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert len(PROFILES) == 35
    xfamily = disk_family()
    local = [local_record(d, xfamily) for d in PROFILES]
    sources, attempts = [], []
    for profile in PROFILES:
        choices = []
        for shift in (0, 1):
            graph, expected = source(profile, shift)
            checked = check_source(graph, expected)
            attempts.append(dict(profile=profile, Y_internal_count=3, shift=shift,
                                 satisfies_all_hypotheses=checked is not None))
            if checked is not None:
                choices.append((shift, 'three_internal_triangle', graph, checked))
        if not choices and profile not in EXCLUDED:
            for shift in range(6):
                graph, expected = source(profile, shift, kind='four_internal_diagonal_cycle')
                checked = check_source(graph, expected)
                attempts.append(dict(profile=profile, Y_internal_count=4, shift=shift,
                                     satisfies_all_hypotheses=checked is not None))
                if checked is not None:
                    choices.append((shift, 'four_internal_diagonal_cycle', graph, checked))
        if choices:
            shift, kind, graph, checked = choices[0]
            sources.append(replay_source(profile, shift, kind, graph, checked, xfamily))
            local[PROFILES.index(profile)]['status'] = 'realizable_with_full_source'
    assert len(sources) == 26
    paths = [Path(__file__).resolve(), ROOT / 'scripts/four_color_twelve_cut_c6_verification.py',
             ROOT / 'scripts/four_color_twelve_cut_eight_side_verification.py',
             ROOT / 'scripts/four_color_bond_perimeter_small_cuts.py',
             ROOT / 'scripts/four_color_twelve_cut_nine_side_reduction.py']
    report = dict(schema='four-color-twelve-cut-nine-side-v1',
                  baseline='e1a90fea41702d7c98747716a5960198aecbecb3',
                  scope='Unique nine-point disk; 35 degree candidates, 9 forced mixed-S5 exclusions, 26 realizable types with complete ordered-attachment R_d fibres and same-opposite-witness C reductions. General nine-cuts and general twelve-cuts remain OPEN.',
                  colour_frame=[0, 1, 2, 3], complete_literal_boundary_rows=ROWS,
                  original_X_oriented_faces=disk_faces(), complete_original_X_family=xfamily,
                  sources_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                  networkx_version=nx.__version__, induced_exhaustion=induced_exhaustion(),
                  all_degree_necessary_profiles=local, nine_point_Y_cap_attempts=attempts,
                  paper_reduction_tables=TABLES, paper_reduction_specs=SPECS,
                  paper_table_validation=validate_paper_tables(),
                  realizations=sources)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(degree_profiles=len(local), excluded=len(EXCLUDED),
                         locally_admissible=len(PROFILES)-len(EXCLUDED),
                         source_Y_sizes=Counter(len(s['original_Y_vertices']) for s in sources),
                         unresolved_larger_Y_source_profiles=[r['X_cross_degrees'] for r in local
                           if r['status']=='locally_admissible' and r['X_cross_degrees'] not in
                             [s['X_cross_degrees'] for s in sources]],
                         original_X_colourings=xfamily['full_colouring_count'],
                         complete_R_d_rows=len(local)*len(ROWS),
                         nonempty_R_d_rows=sum(r['complete_nine_point_lifts_R_d_over_Y']['nonempty_boundary_rows'] for r in local),
                         total_complete_R_d_lifts=sum(r['complete_nine_point_lifts_R_d_over_Y']['full_colouring_count'] for r in local),
                         joined_original_colourings=sum(r['direct_original_colouring_count'] for r in sources),
                         complete_reduced_colourings=sum(r['C_reduction']['complete_reduced_colouring_count'] for r in sources)), sort_keys=True))


if __name__ == '__main__':
    main()
