#!/usr/bin/env python3
"""E4 core, spoke, and parallel-path finite checks.

The report supplies the arbitrary-size arguments.  This script checks only
literal boundary rows, fixed root-path hub partitions, quotient embeddings,
and symbolic complete-relation interfaces.  It performs no source-graph
search, per-key mixed-relation classification, or Four Color Theorem query.
All generated files use exclusive create; --check reads without writes.
"""
from __future__ import annotations
import argparse
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_e4/core_constraints.json'
B = frozenset(range(5))
U = frozenset(range(4))
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
SELECTED = ((6, 'q0'), (4, 'q1'), (1, 'q3'))
SINGLETON = {0: 4, 1: 3, 3: 2, 4: 1, 6: 0}
SOURCES = ('artifacts/c5_cells/cells.json',
    'artifacts/c5_excess_two_e3/REPORT.md',
    'artifacts/c5_excess_two_e3/nonadjacent_notes.md',
    'artifacts/c5_excess_two_e3/nonadjacent.json',
    'artifacts/c5_excess_one_e2/REPORT.md',
    'docs/c5_unary_shield_budget.md', 'docs/c5_qcore_shield_budget.md',
    'scripts/c5_excess_two_e4_core_constraints.py')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def face_walks(rotation):
    unseen = {(v, w) for v, ns in rotation.items() for w in ns}
    result = []
    while unseen:
        initial = min(unseen)
        dart = initial
        face = []
        while True:
            assert dart in unseen
            unseen.remove(dart)
            a, b = dart
            face.append(a)
            ns = rotation[b]
            dart = (b, ns[(ns.index(a) + 1) % len(ns)])
            if dart == initial:
                break
        result.append(face)
    return result


def quotient_face_controls():
    records = []
    for m in range(2, 6):
        centers = tuple(range(2, m + 2))
        for tail in permutations(centers[1:]):
            order = (centers[0],) + tail
            rotation = {0: list(order), 1: list(reversed(order))}
            rotation.update({v: [0, 1] for v in centers})
            faces = face_walks(rotation)
            assert len(rotation) - 2 * m + len(faces) == 2
            assert len(faces) == m
            assert all(len(f) == 4 and len(set(f)) == 4 for f in faces)
            assert all(len(set(f) & set(centers)) == 2 for f in faces)
            records.append(dict(m=m, roots=[0, 1], mixed_bags=list(centers),
                rotation={str(v): rotation[v] for v in sorted(rotation)},
                faces=faces,
                mixed_nodes_on_each_face=[sorted(set(f) & set(centers)) for f in faces]))
    assert len(records) == 1 + 2 + 6 + 24
    return dict(count=len(records), records=records,
        paper_claim='For every plane K(2,m), m>=2: V=m+2,E=2m,F=m; all faces have length4 and exactly two mixed vertices. A connected disjoint B occupies one face.',
        scope='Fixed quotient rotation controls; full original pieces are never replaced in coloring relations.')


def spoke_controls(rows):
    records = []
    forbidden = []
    for size in range(4):
        for support in combinations(range(5), size):
            identities = []
            for index, name in SELECTED:
                beta = rows[index]
                duplicates = [list(pair) for pair in combinations(support, 2)
                              if beta[pair[0]] == beta[pair[1]]]
                private = [v for v in support
                           if sum(beta[w] == beta[v] for w in support) == 1]
                identities.append(dict(row_index=index, row_name=name,
                    duplicate_pairs=duplicates, private_spoke_positions=private))
            never_private = [v for v in support if not any(
                v in rec['private_spoke_positions'] for rec in identities)]
            rec = dict(actual_spoke_set=list(support), rows=identities,
                never_private_spoke_positions=never_private)
            records.append(rec)
            if never_private:
                forbidden.append(rec)
    assert [(r['actual_spoke_set'], r['never_private_spoke_positions']) for r in forbidden] == [([0, 2, 4], [2]), ([1, 2, 4], [4])]
    pairs = []
    for pair in combinations(range(5), 2):
        repeated = [name for index, name in SELECTED
                    if rows[index][pair[0]] == rows[index][pair[1]]]
        assert bool(repeated) == (pair not in FRAME)
        pairs.append(dict(actual_pair=list(pair), selected_duplicate_rows=repeated))
    return dict(all_26_spoke_sets=records,
        excluded_three_spoke_sets=forbidden, all_10_frame_pairs=pairs,
        evidence='Literal row arithmetic. Triple-criticality supplies the no-never-private paper implication.')


def derivative_masks():
    def allowed(eps):
        result = []
        for mask in range(1024):
            if mask & 932 != 932:
                continue
            missing = sorted(SINGLETON[i] for i in SINGLETON if not mask >> i & 1)
            if len(missing) > eps + 1:
                continue
            if eps == 1 and len(missing) == 2 and tuple(missing) not in FRAME:
                continue
            rejected = [name for index, name in SELECTED if not mask >> index & 1]
            assert not ('q3' in rejected and any(q in rejected for q in ('q0', 'q1')))
            result.append(dict(complete_sigma=mask, Q=missing,
                selected_rejected_rows=rejected))
        return result
    zero, one = allowed(0), allowed(1)
    assert len(zero) == 6 and len(one) == 11
    return dict(epsilon_zero_masks=zero, epsilon_at_most_one_masks=one,
        hypotheses='X is a disk subgraph retaining B, accepts all T4, every effective private degree>=4, epsilon(X)<=1. X need not itself be Sigma-critical.',
        proof_dependency='Select a Sigma-preserving minimal Y. Its degree floor gives epsilon(Y)<=epsilon(X); use E2 on Y. This is a paper argument, not established by mask enumeration.',
        original_unit_side_deletion='X=G-f has epsilon1 for an original root-spoke or capacity-one unary factor.',
        double_unit_side_or_unit_mixed_deletion='When both roots lose one incidence, X has epsilon0; omitted complete degree-four pieces contribute zero.')


def boundary_path_hubs(rows):
    path = [5, 0, 1, 2, 6]
    path_edges = {tuple(sorted(e)) for e in zip(path, path[1:])}
    edges = set(FRAME) | path_edges
    records = []
    for index, beta in enumerate(rows):
        for a, b in product(range(4), repeat=2):
            coloring = dict(enumerate(beta)) | {5: a, 6: b}
            if not all(coloring[x] != coloring[y] for x, y in edges):
                continue
            if a == b:
                bags = [path]
                hub_colors = [a]
            else:
                bags = [path[:2], path[2:]]
                hub_colors = [a, b]
                assert tuple(sorted((path[1], path[2]))) in path_edges
            assert set(bags[0]).isdisjoint(bags[1]) if len(bags) == 2 else True
            contacts = {5, 6}
            assert contacts <= set().union(*(set(bag) for bag in bags))
            for bag, c in zip(bags, hub_colors):
                assert {coloring[v] for v in set(bag) & contacts} == {c}
                assert all(tuple(sorted(e)) in path_edges for e in zip(bag, bag[1:]))
            records.append(dict(row_index=index, literal_row=beta,
                root_tuple=[a, b], original_external_path=path,
                hub_bags=bags, hub_contact_colors=hub_colors,
                external_coloring_order=list(range(7)),
                external_coloring=[coloring[v] for v in range(7)]))
    assert len(records) == 90
    return dict(count=len(records), original_external_edges=[list(e) for e in sorted(edges)],
        contact_vertices=[5, 6], mixed_boundary_support=[], records=records,
        strengthened_hypothesis='An external z-w path in G-P suffices for N-empty when N_B(P)=empty; the path may pass through B. H-P connected is sufficient, not necessary.',
        N1_applicability='Sole mixed C with incidences a,b<=4: each root has an original side factor, and each unary has actual boundary support. G-C joins both sides through B.',
        N1_unproved_empty_support_cases='One incidence equals5: that root has no external side factor. This strengthening gives no outside z-w path.',
        scope='Fixed legal outside colorings and bags, not a realizable Sigma-edge-minimal degree5 positive control.')


def exact_residuals(rows):
    common = dict(frame_order=['b0', 'b1', 'b2', 'b3', 'b4'], roots=['z', 'w'],
        actual_root_edge=None,
        original_piece_data=['original vertices', 'original internal edges',
            'actual boundary attachments', 'root ownership',
            'ordered distinct contact vertices', 'original rotation and faces'],
        complete_relation='R_P(beta)={(f(x)) for x in ordered distinct original contacts: f colors every vertex of original P and every actual P-B edge against the literal beta}',
        full_same_graph_lift='Each tuple carries its whole original-P coloring; a shared contact occurs once.',
        root_fibre='R_P(beta;a,b) is the subset of complete tuples avoiding a at all original z-contacts and b at all original w-contacts; absent values are UNKNOWN, never empty by default.',
        exact_root_pair_query='J_P(beta)={(a,b): R_P(beta;a,b) nonempty}',
        side_available_colors='A_r(beta)={a: all actual root-spokes avoid a and every original unary factor has a whole original tuple avoiding a at all its r-contacts}',
        exact_complete_join='J_G(beta)=(A_z(beta) x A_w(beta)) intersection every J_Cj(beta)',
        selected_rows=[dict(index=i, name=name, literal_row=rows[i], required_complete_join='empty') for i, name in SELECTED],
        T4_rows=[dict(index=i, literal_row=rows[i], required_complete_join='nonempty') for i in (2, 5, 7, 8, 9)],
        all_16_fibres_per_row=[dict(root_tuple=[a, b], value='UNKNOWN original fibre; retain whole tuples and witnesses') for a, b in product(range(4), repeat=2)],
        complete_row_count=10,
        triple_criticality='For each original nonframe edge e retain a full coloring of G-e extending a row in indices1/4/6, including all original attachments and one literal shared color frame.')
    core_types = [dict(root_degrees=[4, 5], omitted='one original z-side unit factor', retained='all original mixed'),
        dict(root_degrees=[5, 4], omitted='one original w-side unit factor', retained='all original mixed'),
        dict(root_degrees=[5, 5], omitted='none', retained='G itself')]
    return dict(complete_same_graph_relation_schema=common,
        N1=dict(status='partly reduced, separating mixed relation remains open', mixed_count=1,
            root_omission='At most one rejected row, original unary side S_z or S_w; possible only with mixed incidence1 on that side.',
            core_44=dict(omitted='one original unit side factor at each root', retained='sole original mixed C',
                retained_mixed_incidence_pairs=[[1, 1], [1, 2], [2, 1], [2, 2]]),
            other_core_types=core_types,
            empty_support_reduction='Excluded when both mixed incidences<=4; cases with incidence5 remain unexcluded by this argument.',
            unit_side_derivative_constraint='G-f cannot reject q3 and either q0 or q1, even if G-f was not initially known Sigma-critical.',
            stop='Classifying actual arbitrary-size mixed R_C over all literal support/attachment identities would require a new uniform theorem or per-key work. No such enumeration started.'),
        N2=dict(status='partly reduced, two complete mixed relations remain open', mixed_count=2,
            core_44=dict(omitted='one original (1,1) mixed', retained='the other original mixed only; no side factor omission'),
            other_core_types=core_types,
            duplicate_spoke_constraint='For each selected row at most one root has equal-colored actual spokes.',
            single_duplicate_core_identity='If only z has a duplicate pair, every minimal core of that row is G minus one of those two original z-spokes and has root degrees(4,5); swap roots for w.',
            support_constraints='Each mixed has nonempty actual support; all pieces are one-sided; each unary costs>=2 shield edges, each mixed with support not inside a frame-edge pair costs>=2, with total<=5.',
            unit_side_derivative_constraint='G-f cannot reject q3 together with q0 or q1.',
            stop='The remaining original unit-mixed reconnection, unit-side cross-row palettes, and full(5,5) joint have not been classified.'),
        N3=dict(status='EXCLUDED', mixed_count='at least3',
            reason='Every mixed has nonempty boundary support by inherited N-empty; contracted K(2,m) has one outer face containing B and only two mixed vertices on that face.',
            residual=[]),
        exact_optional_row_branches=[dict(mask=941, q2='accept', q4='accept'),
            dict(mask=933, q2='reject', q4='accept'), dict(mask=940, q2='accept', q4='reject'),
            dict(mask=932, q2='reject', q4='reject')],
        realizability='None of these symbolic unknown relations is claimed to be realizable or a counterexample.')


def build():
    rows = json.loads((ROOT / SOURCES[0]).read_bytes())['pattern_order']
    assert rows[6] == [0, 1, 2, 1, 2]
    assert rows[4] == [0, 1, 2, 0, 2]
    assert rows[1] == [0, 1, 0, 2, 1]
    return dict(schema_version=1, task='E4 independent core constraints', baseline_commit='2ac279b',
        sources={name: dict(sha256=sha((ROOT / name).read_bytes()), bytes=(ROOT / name).stat().st_size) for name in SOURCES},
        quotient_face_controls=quotient_face_controls(),
        boundary_spoke_controls=spoke_controls(rows),
        noncritical_derivative_E2_interface=derivative_masks(),
        boundary_path_Nempty_controls=boundary_path_hubs(rows),
        exact_residuals=exact_residuals(rows),
        requested_nonadjacent_positive_control='Not found; see control_probe/REPORT.md. The fixed controls here do not meet the requested positive-control premises.',
        evidence_boundary='Finite literal arithmetic and fixed graph interfaces. Arbitrary-size source exclusions are the paper proofs in REPORT.md, not a source search or Lean theorem.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path, default=OUT)
    args = parser.parse_args()
    raw = (json.dumps(build(), ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    if args.check:
        assert args.output.read_bytes() == raw, 'Exact core-constraints replay failed.'
        print('CHECK OK: 33 quotient rotations; 26 spoke sets; epsilon0/1 mask interfaces; 90 legal boundary-path hubs; complete residual schemas')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as stream:
            stream.write(raw)
        print(f'GENERATED {args.output}: bytes={len(raw)} sha256={sha(raw)}')
    print('PAPER STATUS: N1 and N2 retain precise original relations; N3 excluded by planar K(2,m) faces and N-empty')


if __name__ == '__main__':
    main()
