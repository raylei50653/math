#!/usr/bin/env python3
"""E5 fixed-column, contact-cover and original-root-path arithmetic.

No source graph search, four-colour oracle, planarity oracle or historical
exact-target ledger is used. Palette sets are exact common-root avoidance
queries on complete ordered relations in the paper argument, not marginals.
Generation is exclusive-create; --check is read-only deterministic replay.
"""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_e5/local.json'
CELLS = ROOT / 'artifacts/c5_cells/cells.json'
INPUTS = ROOT / 'artifacts/c5_excess_two_e3/positive_control_inputs.json'
COLORS = frozenset(range(4))
FRAME = tuple(range(5))
CYCLE = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in FRAME)
SELECTED_Q = (0, 1, 3)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def edge(u, v):
    assert u != v
    return tuple(sorted((u, v)))


def powerset(values):
    values = tuple(sorted(values))
    return [frozenset(x) for n in range(len(values) + 1) for x in combinations(values, n)]


def row_arithmetic(rows, row_of_q):
    indices = [row_of_q[q] for q in SELECTED_Q]
    columns = [dict(boundary_vertex=i,
                    literal_selected_column=[rows[ri][i] for ri in indices]) for i in FRAME]
    assert len({tuple(item['literal_selected_column']) for item in columns}) == 5
    edge_signatures = []
    for pair in sorted(CYCLE):
        signatures = [sorted({rows[ri][v] for v in pair}) for ri in indices]
        assert all(len(colors) == 2 for colors in signatures)
        edge_signatures.append(dict(actual_ordered_boundary_edge=pair,
                                    literal_unordered_color_set_signature=signatures))
    assert len({tuple(tuple(x) for x in r['literal_unordered_color_set_signature'])
                for r in edge_signatures}) == 5
    pair_checks = []
    for pair in combinations(FRAME, 2):
        repetitions = [dict(singleton=q, row_index=row_of_q[q],
                            literal_row=rows[row_of_q[q]]) for q in SELECTED_Q
                       if rows[row_of_q[q]][pair[0]] == rows[row_of_q[q]][pair[1]]]
        assert bool(repetitions) == (edge(*pair) not in CYCLE)
        pair_checks.append(dict(ordered_boundary_pair=pair,
                                same_color_selected_rows=repetitions,
                                is_original_frame_edge=edge(*pair) in CYCLE))
    triple_checks = []
    for triple in combinations(FRAME, 3):
        witnesses = []
        for q in SELECTED_Q:
            ri, beta = row_of_q[q], rows[row_of_q[q]]
            for removed in triple:
                same = [v for v in triple if v != removed and beta[v] == beta[removed]]
                if same:
                    witnesses.append(dict(singleton=q, row_index=ri, literal_row=beta,
                        omitted_original_a_spoke_endpoint=removed,
                        original_a_spoke_support=triple,
                        retained_same_color_original_spoke_endpoints=same))
        assert witnesses
        triple_checks.append(dict(original_a_spoke_support=triple,
                                  all_literal_same_color_omission_witnesses=witnesses))
    return dict(selected_singletons=SELECTED_Q, selected_row_indices=indices,
                boundary_columns=columns, frame_edge_color_set_signatures=edge_signatures,
                all_ten_boundary_pairs=pair_checks,
                all_ten_three_spoke_sets=triple_checks,
                scope='Literal row arithmetic; no source realizability or independent color normalization')


def branch_arithmetic(rows, row_of_q):
    branches = []
    expected = {941: [[0,1,2],[0,1,4],[0,3,4],[1,2,3]],
                933: [[0,1,2],[1,2,3]], 940: [[0,1,4],[0,3,4]], 932: []}
    for mask in (941, 933, 940, 932):
        rejected = tuple(q for q in FRAME if not mask >> row_of_q[q] & 1)
        assert set(SELECTED_Q) <= set(rejected)
        assert mask & 932 == 932
        tests, allowed = [], []
        for triple in combinations(FRAME, 3):
            spokes = []
            for removed in triple:
                duplicate_singletons = [q for q in rejected
                    if any(rows[row_of_q[q]][v] == rows[row_of_q[q]][removed]
                           for v in triple if v != removed)]
                spokes.append(dict(omitted_original_a_spoke_endpoint=removed,
                    retained_original_a_spoke_endpoints=[v for v in triple if v != removed],
                    D_e_rejected_singletons=duplicate_singletons,
                    D_e_literal_rows=[dict(singleton=q, row_index=row_of_q[q],
                        literal_row=rows[row_of_q[q]]) for q in duplicate_singletons]))
            valid = all(len(item['D_e_rejected_singletons']) <= 1 for item in spokes)
            tests.append(dict(original_a_spoke_support=triple,
                              literal_spoke_columns=spokes,
                              satisfies_paper_derived_single_rejection_bound=valid))
            if valid:
                allowed.append(list(triple))
        assert allowed == expected[mask]
        branches.append(dict(canonical_branch_mask=mask, rejected_singletons=rejected,
            q2_accepted=bool(mask >> row_of_q[2] & 1),
            q4_accepted=bool(mask >> row_of_q[4] & 1),
            all_ten_three_spoke_support_tests=tests,
            necessary_three_spoke_supports=allowed,
            input_bound='Paper proof |Q(G-e)| <= 1 for the stated E5 incidence; D_e subset Q(G-e)',
            scope='Necessary literal-column constraints, not a source oracle or existence statement'))
    return branches


def ternary_palette_arithmetic(rows, row_of_q):
    queries, tested = [], 0
    for triple in combinations(FRAME, 3):
        for s in FRAME:
            for q in SELECTED_Q:
                ri, beta = row_of_q[q], rows[row_of_q[q]]
                for removed in triple:
                    kept = tuple(v for v in triple if v != removed)
                    same = [v for v in kept if beta[v] == beta[removed]]
                    if not same:
                        continue
                    leaf_colors = COLORS - {beta[v] for v in kept}
                    root_colors = COLORS - {beta[s]}
                    assert len(leaf_colors) == 2 and len(root_colors) == 3
                    solutions = []
                    for forbidden_k in powerset(leaf_colors):
                        for forbidden_u in [frozenset(), *[frozenset((c,)) for c in sorted(COLORS)]]:
                            tested += 1
                            if root_colors <= forbidden_k | forbidden_u:
                                assert forbidden_k == leaf_colors
                                assert leaf_colors <= root_colors
                                assert forbidden_u == root_colors - leaf_colors
                                solutions.append(dict(F_K=sorted(forbidden_k), F_U=sorted(forbidden_u)))
                    assert len(solutions) == int(leaf_colors <= root_colors)
                    queries.append(dict(original_a_spoke_support=triple,
                        original_b_spoke_endpoint=s, singleton=q,
                        row_index=ri, literal_row=beta,
                        omitted_original_a_spoke_endpoint=removed,
                        retained_original_a_spoke_endpoints=kept,
                        retained_same_color_original_spoke_endpoints=same,
                        literal_marked_leaf_available_colors_L=sorted(leaf_colors),
                        literal_root_available_colors_A=sorted(root_colors),
                        solutions=solutions,
                        ordered_K_contact_roles=['a','y0','y1'],
                        ordered_U_contact_roles=['u'],
                        full_joint_roles=['b','a','x','y0','y1','u'],
                        scope='F is exact common-root avoidance of the full ordered relation; never contact marginals'))
    assert len(queries) == 180 and tested == 3600
    return dict(all_literal_same_color_queries=queries, palette_candidate_checks=tested,
        query_count=len(queries), feasible_cover_count=sum(bool(q['solutions']) for q in queries),
        paper_consequence='Every surviving cover has F_K=L subset A and F_U=A minus L; the original three-contact two-ban active-triangle lemma applies')


def simple_paths(edges, start, target, forbidden):
    adjacency = {v: sorted(w for e in edges if v in e for w in e if w != v)
                 for v in {w for e in edges for w in e}}
    result = []
    def visit(path):
        if path[-1] == target:
            result.append(tuple(path))
            return
        for nxt in adjacency[path[-1]]:
            if nxt not in forbidden and nxt not in path:
                visit((*path, nxt))
    visit((start,))
    return sorted(result, key=lambda path: (len(path), path))


def original_root_path_controls(exact):
    record, = [r for r in exact['records'] if r['graph']['sigma_mask'] == 935]
    graph = record['graph']
    original_edges = frozenset(tuple(e) for e in graph['all_edges'])
    a, b = 5, 6
    a_spokes = sorted(i for i in FRAME if edge(a,i) in original_edges)
    b_spokes = sorted(i for i in FRAME if edge(b,i) in original_edges)
    assert a_spokes == [1,2,3] and b_spokes == [0,1,4]
    controls = []
    for a_pair in ((1,2),(2,3)):
        for b_pair in ((0,1),(0,4)):
            external = CYCLE | {edge(a,b)} | {edge(a,i) for i in a_pair} | {edge(b,i) for i in b_pair}
            assert external <= original_edges
            for h in FRAME:
                a_paths = simple_paths(external,a,h,{b})
                b_paths = simple_paths(external,b,h,{a})
                chosen = next(((pa,pb) for pa in a_paths for pb in b_paths
                               if set(pa) & set(pb) == {h}), None)
                assert chosen is not None
                pa,pb = chosen
                assert pa[0] == a and pb[0] == b and pa[-1] == pb[-1] == h
                assert len(set(pa)) == len(pa) and len(set(pb)) == len(pb)
                assert b not in pa and a not in pb
                path_edges = [[edge(u,v) for u,v in zip(path,path[1:])] for path in chosen]
                assert all(set(es) <= original_edges for es in path_edges)
                controls.append(dict(source_pointer=record['pointer'],
                    source_record_sha256=record['record_sha256'],
                    source_sigma_mask=935, root_roles=dict(a=a,b=b),
                    original_root_spokes=dict(a=a_spokes,b=b_spokes),
                    selected_actual_a_spoke_pair=a_pair,
                    selected_actual_b_spoke_pair=b_pair,
                    actual_common_boundary_target=h,
                    actual_root_exterior_subgraph_edges=sorted(external),
                    simple_original_a_to_h_path=pa,
                    simple_original_b_to_h_path=pb,
                    all_actual_path_edges=path_edges,
                    path_intersection=[h],
                    scope='Original E1 935 graph edge/path control; no coloring or source exclusion claim'))
    assert len(controls) == 20
    return dict(source_pointer=record['pointer'], original_graph=graph,
                actual_root_spoke_pair_path_controls=controls,
                count=len(controls))


def build():
    cell_bytes, input_bytes = CELLS.read_bytes(), INPUTS.read_bytes()
    cells, exact = json.loads(cell_bytes), json.loads(input_bytes)
    rows = tuple(tuple(beta) for beta in cells['pattern_order'])
    row_of_q = {int(q): int(ri) for ri,q in cells['singleton_of_three_colour'].items()}
    assert row_of_q == {0:6,1:4,2:3,3:1,4:0}
    for record in exact['records']:
        assert sha256(canonical(record['graph'])).hexdigest() == record['record_sha256']
    arithmetic = row_arithmetic(rows,row_of_q)
    branches = branch_arithmetic(rows,row_of_q)
    palette = ternary_palette_arithmetic(rows,row_of_q)
    paths = original_root_path_controls(exact)
    return dict(task='E5 local fixed-domain arithmetic',
        inputs=[dict(path=str(p.relative_to(ROOT)),sha256=sha256(raw).hexdigest())
                for p,raw in ((CELLS,cell_bytes),(INPUTS,input_bytes))],
        script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        exact_E1_provenance_and_input_records=exact,
        complete_literal_pattern_order=rows,
        singleton_to_row_index=row_of_q,
        local_row_arithmetic=arithmetic,
        branch_single_rejection_columns=branches,
        full_ordered_relation_ternary_palette_queries=palette,
        original_935_root_path_controls=paths,
        evidence_boundary='Fixed row/palette/path arithmetic only; unbounded source, topology and Gallai claims remain paper proofs',
        summary=dict(boundary_column_injectivity=True, frame_edge_signature_injectivity=True,
            three_spoke_sets_with_selected_same_color_witness=10,
            branch_necessary_support_counts={str(x['canonical_branch_mask']):len(x['necessary_three_spoke_supports']) for x in branches},
            ternary_literal_queries=palette['query_count'],
            ternary_palette_candidate_checks=palette['palette_candidate_checks'],
            ternary_feasible_covers=palette['feasible_cover_count'],
            actual_E1_935_root_path_controls=paths['count'],
            no_four_colour_or_planarity_oracle=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Read-only deterministic byte replay')
    args = parser.parse_args()
    result = build()
    payload = encoded(result)
    if args.check:
        assert OUT.read_bytes() == payload, 'E5 local artifact byte mismatch'
        action = 'checked'
    else:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        with OUT.open('xb') as handle:
            handle.write(payload)
        action = 'exclusive-created'
    print(json.dumps(dict(action=action,artifact=str(OUT.relative_to(ROOT)),
                         sha256=sha256(payload).hexdigest(),**result['summary']),sort_keys=True))


if __name__ == '__main__':
    main()
