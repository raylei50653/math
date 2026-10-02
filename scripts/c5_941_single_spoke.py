#!/usr/bin/env python3
"""Fixed 941 t=1 exclusion controls; arbitrary-size coverage is a paper proof.

Preserve named binary contacts and actual attachments over all ten rows.
No source graph census, planarity oracle, or independent contact projections.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import B, FRAME, ROWS, U, colorings
from c5_single_spoke_cores import placements

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_941_single_spoke/observations.json'
D = 3
Q = {next(i for i in range(5) if b.count(b[i]) == 1): b
     for b in ROWS if len(set(b)) == 3}


def forbidden(relation):
    assert relation
    return set.intersection(*(set(t) for t in relation))


def edge_relation(left, right):
    return sorted((a, b) for a in left for b in right if a != b)


def local_relations():
    lists = [set(c) | {D} for k in range(1, 4)
             for c in combinations(range(3), k)]
    result = []
    for left, right in product(lists, repeat=2):
        relation = edge_relation(left, right)
        f = forbidden(relation)
        expected = left if left == right and len(left) == 2 else set()
        assert f == expected and f != {D}
        result.append(dict(lists=[sorted(left), sorted(right)],
                           ordered_relation=relation, forbidden=sorted(f)))
    return result


def support_controls():
    # Every larger support contains a three-point subset. The unbounded
    # embedding-to-common-lifts implication is proved in the report.
    supports = list(combinations(range(5), 3))
    digest, counts = sha256(), Counter()
    for s in range(5):
        for named in product(supports, repeat=3):
            actual = placements(s, named)
            assert not actual
            counts[str(s)] += 1
            digest.update((json.dumps([s, named, actual]) + '\n').encode())
    positive = ((0, 1), (1, 2, 3), (0, 3, 4))
    witnesses = placements(0, positive)
    assert witnesses
    return dict(component_order=['C_2', 'U_0', 'U_1'],
                triple_support_subsets=supports, checked_by_spoke=dict(counts),
                compatible_three_leaf_cases=0, enumeration_sha256=digest.hexdigest(),
                positive_233_control=dict(spoke=0, supports=positive,
                                          placements=witnesses,
                                          scope='support control, not a graph realization'))


def minimal_covers():
    result = []
    options = [set()] + [{a} for a in range(3)]
    binary = [{D}] + [{D, a} for a in range(3)]
    for s, f, f0, f1 in product(range(5), binary, options, options):
        factors = [{Q[3][s]}, f, f0, f1]
        if set.union(*factors) != U:
            continue
        omitted = [i for i in range(4)
                   if set.union(*(g for j, g in enumerate(factors) if j != i)) == U]
        if not omitted:
            assert f == {D}
            assert len(set.union(factors[0], f0, f1)) == 3
            result.append(dict(spoke=s, row=Q[3],
                               factor_order=['spoke', 'C_2', 'U_0', 'U_1'],
                               forbidden_sets=[sorted(g) for g in factors],
                               omitted=[]))
    assert len(result) == 10
    return result


def edge_attachments():
    result, histogram = [], Counter()
    for nx, ny in product(combinations(range(5), 2), repeat=2):
        # r=5 is uncolored for R_C; x=6 and y=7 remain ordered contacts.
        edges = FRAME | {(5, 6), (5, 7), (6, 7)}
        edges |= {(b, 6) for b in nx} | {(b, 7) for b in ny}
        rows = []
        for b in ROWS:
            choices = colorings([6, 7], edges, dict(enumerate(b)))
            relation = sorted({(c[6], c[7]) for c in choices})
            lists = [U - {b[v] for v in ns} for ns in (nx, ny)]
            assert relation == edge_relation(*lists)
            f = forbidden(relation)
            expected = lists[0] if lists[0] == lists[1] and len(lists[0]) == 2 else set()
            assert f == expected
            root_rows = []
            for a in range(4):
                pinned = colorings([6, 7], edges, dict(enumerate(b)) | {5: a})
                assert bool(pinned) == (a not in f)
                root_rows.append(dict(root_color=a, accepts=bool(pinned),
                                      coloring=([pinned[0][v] for v in range(8)]
                                                if pinned else None)))
            if len(set(b)) == 3:
                assert f != {D}
            rows.append(dict(row=b, lists=[sorted(ls) for ls in lists],
                             ordered_relation=relation, forbidden=sorted(f),
                             tuple_witnesses=[dict(tuple=t, coloring=list(b) + list(t),
                                                   vertex_order=[0, 1, 2, 3, 4, 6, 7])
                                              for t in relation],
                             root_queries=root_rows))
            histogram[len(f)] += 1
        by_row = {tuple(r['row']): r for r in rows}
        saturated = all(D in by_row[Q[i]]['forbidden'] and
                        len(by_row[Q[i]]['forbidden']) == 2 for i in (0, 1))
        result.append(dict(contacts=[6, 7], attachments={'6': nx, '7': ny},
                           support=sorted(set(nx) | set(ny)), edges=sorted(edges),
                           full_ten_rows=rows, both_omission_rows_saturated=saturated,
                           q3_singleton_D=by_row[Q[3]]['forbidden'] == [D]))
    assert len(result) == 100
    return result, dict(sorted(histogram.items()))


def build():
    local = local_relations()
    support = support_controls()
    covers = minimal_covers()
    edges, histogram = edge_attachments()
    deps = ['scripts/c5_941_single_spoke.py',
            'scripts/c5_independent_support_capacity.py', 'scripts/c5_single_spoke_cores.py']
    return dict(schema=1,
                scope='finite algebra/support controls; arbitrary-size exclusion uses documented structure',
                source_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in deps},
                pattern_order=ROWS, singleton_rows=Q,
                normal_form_contract=dict(root='r', binary='C_2', ordered_contacts=['x', 'y'],
                    unary_components=['U_0', 'U_1'], spoke='r-b_s',
                    omission_witnesses=[dict(row=Q[0], omitted='U_0',
                        retained=['spoke', 'C_2', 'U_1']),
                        dict(row=Q[1], omitted='U_1', retained=['spoke', 'C_2', 'U_0'])],
                    witness_scope='hypotheses of the impossible source; not constructed colorings'),
                local_relations=local, common_support_controls=support,
                minimal_q3_covers=covers, binary_edge_attachment_models=edges,
                summary=dict(local_relation_pairs=len(local),
                    named_three_leaf_support_checks=sum(support['checked_by_spoke'].values()),
                    compatible_three_leaf_cases=0, minimal_q3_covers=len(covers),
                    binary_attachment_models=len(edges), binary_ten_row_checks=len(edges) * len(ROWS),
                    pinned_root_checks=len(edges) * len(ROWS) * 4,
                    forbidden_size_histogram=histogram,
                    both_saturated_attachment_models=sum(r['both_omission_rows_saturated'] for r in edges),
                    singleton_D_attachment_models=0, t1_disk_sources=0,
                    remaining_941_excess_one_spokes=[2, 3],
                    new_source_graph_enumeration=False, new_lean_theorem=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
