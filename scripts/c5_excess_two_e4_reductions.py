#!/usr/bin/env python3
"""E4 fixed local controls and provenance-preserving residual interfaces.

The theta/Gallai source exclusions are paper proofs in REPORT.md.  This checker
checks explicit finite rotations, literal contact tuples, palette arithmetic,
and the recorded symbolic interfaces; it does not enumerate source graphs,
decide arbitrary disk realizability, or use a Four Color Theorem oracle.
Generation uses exclusive create; --check is read only and byte exact.
"""
from __future__ import annotations
import argparse
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'artifacts/c5_excess_two_e4/reductions.json'
U = frozenset(range(4))
B = frozenset(range(5))
FRAME = frozenset(tuple(sorted((i, (i+1) % 5))) for i in range(5))
SOURCES = (
    'artifacts/c5_cells/cells.json',
    'artifacts/c5_excess_two_e3/REPORT.md',
    'artifacts/c5_excess_two_e3/nonadjacent_notes.md',
    'artifacts/c5_excess_two_e3/nonadjacent.json',
    'artifacts/c5_excess_one_e2/REPORT.md',
    'docs/c5_unary_shield_budget.md',
    'docs/c5_qcore_shield_budget.md',
    'scripts/c5_excess_two_e4_reductions.py',
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def connected_components(vertices, edges):
    remaining = set(vertices)
    out = []
    while remaining:
        todo = [min(remaining)]
        got = set()
        while todo:
            v = todo.pop()
            if v in got:
                continue
            got.add(v)
            todo.extend(sorted({b if a == v else a for a, b in edges
                                if v in (a, b)} & remaining - got, reverse=True))
        remaining -= got
        out.append(sorted(got))
    return out


def orientation(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def theta_controls():
    """Two explicit straight-line disks; no universal topology inference."""
    positions = {0:(0,-20), 1:(20,-7), 2:(13,16), 3:(-13,16),
                 4:(-20,-7), 5:(-6,0), 6:(6,0), 7:(0,-6),
                 8:(0,6), 9:(0,0)}
    records = []
    for m in (2, 3):
        vertices = set(range(9 + (m == 3)))
        branches = [7, 8] + ([9] if m == 3 else [])
        edges = set(FRAME) | {(0,7),(2,8),(4,5),(1,6)}
        edges |= {tuple(sorted((r,x))) for r in (5,6) for x in branches}
        # No pair of disjoint fixed line segments crosses or meets.
        for e, f in combinations(sorted(edges), 2):
            if set(e) & set(f):
                continue
            a,b = (positions[v] for v in e)
            c,d = (positions[v] for v in f)
            o = [orientation(a,b,c), orientation(a,b,d),
                 orientation(c,d,a), orientation(c,d,b)]
            assert not (o[0]*o[1] < 0 and o[2]*o[3] < 0), (e,f)
            for x,y,z,value in ((a,b,c,o[0]),(a,b,d,o[1]),(c,d,a,o[2]),(c,d,b,o[3])):
                on_segment = (min(x[0],y[0]) <= z[0] <= max(x[0],y[0]) and
                              min(x[1],y[1]) <= z[1] <= max(x[1],y[1]))
                assert not (value == 0 and on_segment), (e,f,'disjoint segments meet')
        rotation = {}
        for v in sorted(vertices):
            ns = {b if a == v else a for a,b in edges if v in (a,b)}
            rotation[v] = sorted(ns, key=lambda w: math.atan2(
                positions[w][1]-positions[v][1], positions[w][0]-positions[v][0]))
        todo = {(a,b) for a,b in edges} | {(b,a) for a,b in edges}
        faces = []
        while todo:
            start = min(todo)
            edge = start
            walk = []
            while True:
                assert edge in todo
                todo.remove(edge)
                a,b = edge
                walk.append(a)
                ns = rotation[b]
                edge = (b, ns[(ns.index(a)+1) % len(ns)])
                if edge == start:
                    break
            faces.append(walk)
        assert len(vertices)-len(edges)+len(faces) == 2
        assert any(len(f) == 5 and set(f) == B for f in faces)
        original_pieces = connected_components(vertices-B-{5,6}, edges)
        assert original_pieces == [[x] for x in branches]
        supports = {str(x): sorted({b if a == x else a for a,b in edges
                                    if x in (a,b)} & B) for x in branches}
        if m == 3:
            assert supports['9'] == []
            # The enclosing original Jordan cycle uses the two outer pieces.
            jordan = [5,7,6,8]
            assert all(tuple(sorted(e)) in edges for e in zip(jordan,jordan[1:]+jordan[:1]))
            assert all(orientation(positions[a],positions[b],positions[9]) > 0
                       for a,b in zip(jordan,jordan[1:]+jordan[:1]))
        else:
            jordan = None
            assert all(supports[str(x)] for x in branches)
        records.append(dict(mixed_count=m, vertices=sorted(vertices),
            full_edges=[list(e) for e in sorted(edges)],
            positions={str(v):list(positions[v]) for v in sorted(vertices)},
            rotations={str(v):rotation[v] for v in sorted(vertices)},
            faces=faces, roots=[5,6], original_pieces=original_pieces,
            actual_supports=supports, enclosing_original_cycle=jordan,
            hidden_piece=[9] if m == 3 else [],
            scope='Fixed topology control only; not degree-four or Sigma-critical positive control.'))
    return records


def local_short_shared_contact(rows):
    """All complete relations of one literal shared singleton contact."""
    records = []
    for i, beta in enumerate(rows):
        tuples = [[c] for c in sorted(U-set(beta[:2]))]
        fibres = []
        for a,b in product(range(4), repeat=2):
            exact = [t for t in tuples if t[0] != a and t[0] != b]
            # Shared contact is a single vertex/coordinate, never two marginals.
            direct = [[c] for c in range(4)
                      if c not in {beta[0],beta[1],a,b}]
            assert exact == direct
            if a == b:
                assert exact
            if not exact:
                assert len({beta[0],beta[1],a,b}) == 4
            fibres.append(dict(root_tuple=[a,b], complete_contact_tuples=exact,
                local_witnesses=[{'7':t[0]} for t in exact]))
        records.append(dict(row_index=i, literal_row=beta, contact_order=[7],
            root_contact_ports={'5':[7], '6':[7]},
            actual_attachments={'7':[0,1]}, complete_relation=tuples,
            full_root_fibres=fibres))
    return dict(vertices=[7], roots=[5,6], original_edges=[[0,7],[1,7],[5,7],[6,7]],
        degree_of_piece_vertex=4, rows=records,
        scope='Fixed local short-mixed relation control, not a full Sigma-critical disk source.')


def palette_arithmetic():
    # The capacity bound is a necessary query bound, not a replacement relation.
    checks = []
    for k in range(1,6):
        checked = 0
        for color_set_size in range(1,min(k,4)+1):
            for colors in combinations(range(4), color_set_size):
                # One complete k-tuple realizes each possible color-set size.
                t = tuple(colors) + (colors[0],)*(k-color_set_size)
                forbidden = set(t)
                assert len(forbidden) <= k
                assert len(U-forbidden) >= max(0,4-k)
                checked += 1
        checks.append(dict(contact_capacity=k, complete_tuple_color_sets_checked=checked))
    budgets = []
    for u in range(3):
        for long in range(3):
            short = 2-long
            for pair in range(short+1):
                lower = 2*u+2*long+pair
                if lower <= 5:
                    budgets.append(dict(unary_count=u, long_mixed_count=long,
                        short_mixed_count=short, short_pair_count=pair,
                        minimum_total_shield_edges=lower,
                        zero_unary_all_short_excluded=bool(u == 0 and long == 0)))
    # A correlated relation cannot be independently projected at its two ports.
    relation = [[0,1],[1,0]]
    allowed_pin = [0,0]
    exact = [t for t in relation if t[0] != allowed_pin[0] and t[1] != allowed_pin[1]]
    fake_product_witness = [1,1]
    assert exact == [] and fake_product_witness not in relation
    return dict(capacity_checks=checks, N2_necessary_shield_budgets=budgets,
        projection_guard=dict(full_ordered_relation=relation,
            root_pin=allowed_pin, exact_fibre=exact,
            false_witness_from_independent_marginals=fake_product_witness),
        scope='Finite tuple/palette and integer arithmetic only; no source graph keys.')


def residual_interfaces():
    # Every variable denotes the original graph; no catalogued relation is guessed.
    original = dict(
        frame='B=(b0,b1,b2,b3,b4) in this fixed cyclic order',
        roots=['z','w'], root_edge_present=False,
        factor_metadata=['original vertices', 'all original internal edges',
            'actual boundary attachments', 'owner roots', 'ordered distinct contacts',
            'literal shared contact identities', 'original rotation and face'],
        full_relation='R_P(beta)={(f(x))_(x in X_P): f colors every original vertex of P and all original P-B edges against the same literal beta}',
        witness_lifts='For every tuple retain f on every vertex of P; shared contacts occur once.',
        exact_mixed_query='A_P(beta)={(a,b): exists t in R_P(beta), all original z-contact coordinates avoid a and all original w-contact coordinates avoid b}',
        exact_side_query='E_r(beta)=colors avoiding all original r-spokes and, for every original unary U at r, admitting one complete tuple t in R_U(beta) avoiding that color at all contacts}',
        complete_original_join='J_G(beta)={(a,b): a in E_z(beta), b in E_w(beta), (a,b) in every original A_Cj(beta)}',
        extension_iff='J_G(beta) nonempty, with one whole tuple and its same-graph lift chosen per original factor',
        selected_rows={'q0':[0,1,2,1,2], 'q1':[0,1,2,0,2], 'q3':[0,1,0,2,1]},
        selected_join_condition='J_G(q0)=J_G(q1)=J_G(q3)=empty',
        T4_join_condition='J_G(beta) nonempty for indices 2,5,7,8,9',
        triple_criticality='For every original nonframe edge e, save a full same-graph coloring of G-e for one index in {1,4,6}; only the original factor or original port inequality incident to e changes.',
        unrestricted_row_indices=[0,3])
    return dict(original_complete_relation_interface=original,
        N1=dict(status='open with reductions', mixed_count=1,
            mixed_relation='R_C(beta) and all of its 16 original root fibres for all ten literal rows remain unclassified',
            excluded_subfamily='original mixed incidences (2,2) with any (4,4) core: exact path4 connector, adjacent terminal frame pairs and the two named side shields require 3+3>5',
            requirements=['separating C with nonempty actual support', 'at most two original unaries',
                'at most one root-deletion exception across all rejected rows'],
            core_types=[dict(degrees=[4,4], omission='one original unit side factor at z and one at w; original C retained'),
                dict(degrees=[4,5], omission='one original z-spoke or capacity-one unary at z; original C retained'),
                dict(degrees=[5,4], omission='one original w-spoke or capacity-one unary at w; original C retained'),
                dict(degrees=[5,5], omission='none: the complete original G is the q-core'),
                dict(degrees='one degree-four root', omission='original unary side S_r only; at most one rejected row')],
            excluded_core_incidence='(4,4) retains C: mixed root contacts each at most two; original (2,2) incidence is excluded, leaving (1,1),(1,2),(2,1)',
            stop='Other core types, including (2,2) sources with no (4,4) core, need original mixed joint classification; no per-key enumeration begun.'),
        N2=dict(status='partly excluded; exact relation families remain', mixed_count=2,
            mixed_relation='R_C0(beta), R_C1(beta), their original root fibres and same-graph lifts; J uses A_C0 intersection A_C1',
            requirements=['both original mixed supports nonempty', 'all original pieces one-sided',
                'unary_count + long_mixed_count <= 2',
                'every short mixed admits every diagonal root pin under the local-list hub proof'],
            excluded_subfamily='both mixed short and no unary: every three-color row extends using both roots in its unused color',
            residual_families=[{'long_mixed_count':2,'unary_count':0},
                {'long_mixed_count':1,'unary_count':[0,1]},
                {'long_mixed_count':0,'unary_count':[1,2]}],
            core_types=[dict(degrees=[4,4], omission='one original (1,1) mixed; the other original mixed retained and no side omission'),
                dict(degrees=[4,5], omission='one original z-side unit; both original mixed retained'),
                dict(degrees=[5,4], omission='one original w-side unit; both original mixed retained'),
                dict(degrees=[5,5], omission='none: complete original G')],
            short_family_condition='E_z(beta) intersection E_w(beta) empty on each rejected row; this is necessary, not sufficient',
            stop='No exhaustive mixed-joint classification or exact q2/q4 acceptance was assumed.'),
        N3=dict(status='excluded by arbitrary-size N-theta plus inherited N-empty',
            mixed_count='at least 3', core_types_excluded=['(4,5)','(5,4)','original (5,5)'],
            proof_dependency='three original disjoint mixed paths enclose an entire original empty-support mixed piece; all pieces one-sided; N-empty contradicts criticality',
            residual=[]),
        exact_optional_row_branches=[
            {'mask':941,'q2':'accept','q4':'accept'},
            {'mask':933,'q2':'reject','q4':'accept'},
            {'mask':940,'q2':'accept','q4':'reject'},
            {'mask':932,'q2':'reject','q4':'reject'}],
        row_dependency_note='No E4 reduction depends on choosing one of the four masks. If a later exact-role proof is required, stop at these four branches.')


def three_row_terminal_pairs(rows):
    selected = [(6,'q0'),(4,'q1'),(1,'q3')]
    certificates = []
    for pair in combinations(range(5),2):
        repeats = [name for i,name in selected if rows[i][pair[0]] == rows[i][pair[1]]]
        adjacent = tuple(pair) in FRAME
        assert bool(repeats) != adjacent
        certificates.append(dict(actual_attachment_pair=list(pair), is_frame_edge=adjacent,
            selected_rows_with_repeated_color=repeats))
    return dict(all_actual_pairs=certificates,
        paper_use='A repeated terminal pair makes the same connected original degree-four C list-slack; N1 mixed22 with a (4,4) core must have frame-edge terminal pairs.',
        scope='Ten named frame pairs only, not per-key mixed relation enumeration.')


def build():
    cells = json.loads((ROOT / SOURCES[0]).read_bytes())
    rows = cells['pattern_order']
    assert len(rows) == 10
    assert rows[6] == [0,1,2,1,2] and rows[4] == [0,1,2,0,2] and rows[1] == [0,1,0,2,1]
    return dict(schema_version=1, task='E4 nonadjacent roots, N1-N3',
        baseline_commit='2ac279b6144cdfcf4ececd7b72f5d287a6f4b4ac',
        sources={p:{'sha256':digest((ROOT/p).read_bytes()), 'bytes':(ROOT/p).stat().st_size}
                 for p in SOURCES},
        pattern_order=rows, selected_rejection_indices=[1,4,6], T4_indices=[2,5,7,8,9],
        topology_controls=theta_controls(),
        full_shared_contact_local_control=local_short_shared_contact(rows),
        palette_and_budget_checks=palette_arithmetic(),
        N1_terminal_pair_controls=three_row_terminal_pairs(rows),
        residual_interfaces=residual_interfaces(),
        evidence_boundary='The report supplies arbitrary-size paper proofs. Fixed controls, rotations, and arithmetic do not prove them or show that an abstract residual is realizable.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path, default=DEFAULT)
    args = parser.parse_args()
    result = build()
    raw = (json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n').encode()
    if args.check:
        assert args.output.read_bytes() == raw, 'Exact E4 artifact replay failed.'
        print('CHECK OK: E4 fixed theta rotations, full shared-contact fibres, palette budgets, residual interfaces')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('xb') as f:
            f.write(raw)
        print(f'GENERATED {args.output}: bytes={len(raw)} sha256={digest(raw)}')
    print('PAPER STATUS: N1 partly excluded; N2 partly excluded; N3 excluded by N-theta/N-empty')


if __name__ == '__main__':
    main()
