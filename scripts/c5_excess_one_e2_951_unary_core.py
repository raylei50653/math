#!/usr/bin/env python3
"""Check the fixed 252 unbranched cores in E2's unary-omission branch.

The arbitrary-size reduction is the unattached-singleton cyclic lemma in
docs/c5_two_spoke_split_support.md section 2. This checker enumerates only
its two actual interior forms with the stated original contacts, spokes,
and boundary-support restriction. No planarity or four-colour oracle.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_one_e2_951_unary_core/observations.json'
CELLS = ROOT / 'artifacts/c5_cells/cells.json'
B = set(range(5))
U = set(range(4))
FRAME = {tuple(sorted((v, (v + 1) % 5))) for v in B}
ROOT_VERTEX = 5
CONTACTS = [6, 7]
Q = [0, 1, 2, 0, 2]
P = [0, 1, 0, 1, 2]
T4 = sum(1 << i for i in (2, 5, 7, 8, 9))


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def color_relation(interior, edges, row, ports):
    """Enumerate all literal colour assignments, preserving ordered ports."""
    interior = set(interior)
    included = B | interior
    relevant = {e for e in edges if set(e) <= included}
    neighbors = {v: set() for v in included}
    for a, b in relevant:
        neighbors[a].add(b)
        neighbors[b].add(a)
    f = dict(enumerate(row))
    witnesses = {}
    full_count = 0

    def visit(left):
        nonlocal full_count
        if not left:
            full_count += 1
            t = tuple(f[v] for v in ports)
            witnesses.setdefault(t, [f[v] for v in list(range(5)) + sorted(interior)])
            return
        choices = {v: U - {f[w] for w in neighbors[v] if w in f} for v in left}
        v = min(left, key=lambda x: (len(choices[x]), x))
        for c in sorted(choices[v]):
            f[v] = c
            visit(left - {v})
            del f[v]

    visit(interior)
    tuples = sorted(witnesses)
    return tuples, [witnesses[t] for t in tuples], full_count


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    reached = {min(vertices)}
    while True:
        updated = reached | {v for u, v in edges if u in reached and v in vertices} | {
            u for u, v in edges if v in reached and u in vertices}
        if updated == reached:
            return reached == vertices
        reached = updated


def k5_private_pair(n, edges, family):
    """Certify an original K5 minor, retaining all named frame vertices."""
    x, y = (6, 7) if family == 'triangle' else (9, 10)
    sx = sorted(b for b in B if tuple(sorted((b, x))) in edges)
    sy = sorted(b for b in B if tuple(sorted((b, y))) in edges)
    assert sx == sy and len(sx) == 2 and tuple(sx) in FRAME
    a, b = sx
    sets = [[x], [y], [a], [b], sorted(set(range(n)) - {x, y, a, b})]
    assert all(connected(s, edges) for s in sets)
    assert set.union(*(set(s) for s in sets)) == set(range(n))
    assert all(set(sets[i]).isdisjoint(sets[j]) for i in range(5) for j in range(i))
    crosses = []
    for i in range(5):
        for j in range(i + 1, 5):
            candidates = sorted(e for e in edges if
                (e[0] in sets[i] and e[1] in sets[j]) or
                (e[1] in sets[i] and e[0] in sets[j]))
            assert candidates
            crosses.append(dict(branch_pair=[i, j], edge=candidates[0]))
    return dict(branch_sets=sets,
                internal_edges=[sorted(e for e in edges if set(e) <= set(s)) for s in sets],
                ten_cross_edges=crosses, private_pair=[x, y], shared_adjacent_boundary_pair=sx,
                obstruction='K5 minor in the original core; remainder is connected via an original root spoke')


def finite_forms():
    forms = [
        ('triangle', [6, 7], [(6, 7)], [2, 2]),
        ('two_triangles_direct_bridge', [6, 7, 8, 9, 10],
         [(6, 7), (6, 8), (8, 9), (8, 10), (9, 10)], [1, 2, 1, 2, 2]),
    ]
    for family, private, internal_edges, sizes in forms:
        choices = [list(combinations((2, 3, 4), size)) for size in sizes]
        for supports in product(*choices):
            edges = FRAME | {(0, 5), (4, 5), (5, 6), (5, 7)} | set(internal_edges) | {
                (b, v) for v, support in zip(private, supports) for b in support}
            yield family, private, supports, edges


def build():
    cells = json.loads(CELLS.read_text())
    rows = cells['pattern_order']
    assert Q in rows and P in rows and len(rows) == 10
    records = []
    counts = Counter()
    histograms = {family: Counter() for family in ('triangle', 'two_triangles_direct_bridge')}
    for model_id, (family, private, supports, edges) in enumerate(finite_forms()):
        interior = [5] + private
        n = max(interior) + 1
        assert FRAME <= edges
        assert connected(interior, edges)
        assert all(sum(v in e for e in edges) == 4 for v in interior)
        assert all(1 not in e for e in edges - FRAME)
        assert sorted(v for v in private if (5, v) in edges) == CONTACTS
        result_rows = []
        sigma = 0
        for i, row in enumerate(rows):
            component, component_witnesses, component_count = color_relation(private, edges, row, CONTACTS)
            assert component
            forbidden = sorted(set.intersection(*(set(t) for t in component)))
            joined = sorted((r, x, y) for r in sorted(U - {row[0], row[4]})
                            for x, y in component if r not in (x, y))
            root_relation, witnesses, full_count = color_relation(interior, edges, row, [5, 6, 7])
            assert root_relation == joined
            if root_relation:
                sigma |= 1 << i
            result_rows.append(dict(row=row, ordered_binary_contacts=CONTACTS,
                complete_ordered_binary_relation=component,
                binary_tuple_witnesses=component_witnesses,
                binary_private_order=private, binary_full_extension_count=component_count,
                binary_forbidden=forbidden, root_port_order=[5, 6, 7],
                complete_ordered_root_relation=root_relation,
                root_tuple_witnesses=witnesses, root_full_extension_count=full_count))
            counts['complete_binary_row_queries'] += 1
            counts['independent_complete_core_row_queries'] += 1
        q_data, p_data = result_rows[rows.index(Q)], result_rows[rows.index(P)]
        q_rejected = not q_data['complete_ordered_root_relation']
        accepts_t4 = sigma & T4 == T4
        relevant = q_rejected and accepts_t4
        counts[family + '_models'] += 1
        histograms[family][sigma] += 1
        record = dict(model_id=model_id, family=family, vertices=n,
            boundary_order=list(range(5)), root=5, original_spokes=[[0, 5], [4, 5]],
            binary_owner=5, binary_private_order=private, binary_contact_order=CONTACTS,
            binary_boundary_attachments=[dict(vertex=v, neighbors=s) for v, s in zip(private, supports)],
            binary_actual_support=sorted(set.union(*(set(s) for s in supports))),
            edges=sorted(edges), complete_sigma=sigma, accepts_T4=accepts_t4,
            q_rejected=q_rejected, complete_ten_row_join_sha256=digest(result_rows))
        if relevant:
            counts[family + '_q_rejected_T4_models'] += 1
            record['rows'] = result_rows
            critical = []
            for edge in sorted(edges - FRAME):
                relation, witnesses, _ = color_relation(interior, edges - {edge}, Q, [5, 6, 7])
                assert relation
                critical.append(dict(edge=edge, coloring=witnesses[0]))
                counts['q_critical_edge_witnesses'] += 1
            record['q_critical_edge_witnesses'] = critical
            choices = [(t, w) for t, w in zip(p_data['complete_ordered_root_relation'],
                                             p_data['root_tuple_witnesses']) if t[0] == 3]
            if choices:
                assert 3 not in p_data['binary_forbidden']
                record['p_root_D_extension'] = dict(ordered_ports=choices[0][0], coloring=choices[0][1])
                counts['q_T4_models_with_p_root_D_extension'] += 1
            else:
                assert 3 in p_data['binary_forbidden']
                record['original_K5_minor'] = k5_private_pair(n, edges, family)
                counts['q_T4_models_without_p_root_D_extension'] += 1
        records.append(record)
    assert len(records) == 252
    assert counts['triangle_models'] == 9
    assert counts['two_triangles_direct_bridge_models'] == 243
    assert counts['triangle_q_rejected_T4_models'] == 3
    assert counts['two_triangles_direct_bridge_q_rejected_T4_models'] == 37
    assert counts['q_T4_models_without_p_root_D_extension'] == 4
    assert counts['q_T4_models_with_p_root_D_extension'] == 36
    assert counts['complete_binary_row_queries'] == 2520
    assert counts['independent_complete_core_row_queries'] == 2520
    return dict(schema=1,
        scope='fixed S04, C-support subset234, degree-four actual unbranched cyclic cores obtained by original unary omission',
        paper_premise='unattached-singleton cyclic lemma: actual interior triangle or two disjoint triangles joined by one direct bridge; arbitrary size is reduced before enumeration',
        geometric_scope='S02 is handled by the separate spoke-omission branch; shield topology alone does not exclude it',
        source_sha256={str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest()
                       for path in (Path(__file__).resolve(), CELLS)},
        pattern_order=rows, singleton_of_three_colour=cells['singleton_of_three_colour'],
        rejected_row=Q, second_row=P, root_D=3, T4_pattern_indices=[2, 5, 7, 8, 9],
        no_planarity_oracle=True, no_four_colour_theorem_oracle=True,
        arbitrary_unary_size_enumerated=False, new_lean_theorem=False,
        models=records, family_sigma_histograms={k: dict(sorted(v.items())) for k, v in histograms.items()},
        summary=dict(**dict(sorted(counts.items())), disk_q_T4_models_without_p_root_D_extension=0,
                     original_K5_certificates=4))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        assert not OUT.exists(), f'refusing to overwrite existing certificate: {OUT}'
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
