#!/usr/bin/env python3
"""No-spoke six-contact paper reduction: palettes, full relations and minors.

The arbitrary-size source reductions are proved in the companion report.
These fixed controls are not source graphs or realizability certificates.
"""
import argparse
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_no_spoke_exterior import four_palettes
from c5_short_support_singleton import original_lift_controls
from c5_excess_two_five_contact import minor
from c5_single_spoke_three_one import edge, validate_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_no_spoke_reduction/observations.json'
U = frozenset(range(4))


def partitions(n, upper=None):
    if n == 0:
        yield ()
        return
    for k in range(min(n, upper or n), 0, -1):
        for rest in partitions(n - k, k):
            yield (k,) + rest


def reduction_controls():
    records = []
    for p in partitions(6):
        if len(p) >= 3:
            reason = 'same_embedding_support_span_at_least_2_per_component'
        elif p == (6,):
            reason = 'four_palettes_saturate_two_K4_original_bridge_K5'
        elif p == (5, 1):
            reason = 'exterior_path_five_contact_capacity_2_plus_unary_1'
        elif p == (3, 3):
            reason = 'exterior_path_ternary_capacity_1_plus_1'
        else:
            assert p == (4, 2)
            reason = 'requires_original_binary_path_certificate'
        records.append(dict(original_contact_partition=p, reason=reason,
                            minimum_total_span=2 * len(p) if len(p) > 1 else None))
    assert len(records) == 11
    assert sum(len(r['original_contact_partition']) >= 3 for r in records) == 7
    covers, checks = [], 0
    for p, bounds in (((5, 1), (2, 1)), ((3, 3), (1, 1)), ((4, 2), (2, 2))):
        pools = [[frozenset(c) for n in range(bound + 1)
                  for c in combinations(range(4), n)] for bound in bounds]
        for fs in product(*pools):
            checks += 1
            if fs[0] | fs[1] != U:
                continue
            assert p == (4, 2) and len(fs[0]) == len(fs[1]) == 2 and not fs[0] & fs[1]
            covers.append(dict(original_contact_partition=p,
                               literal_forbidden_sets=[sorted(f) for f in fs]))
    assert checks == 201 and len(covers) == 6
    invariant = [list(c) for n in range(5) for c in combinations(range(4), n)
                 if all({p[v] for v in c} == set(c) for p in permutations(range(4)))]
    assert invariant == [[], [0, 1, 2, 3]]
    return dict(partitions=records, capacity_checks=checks,
                remaining_literal_pair_covers=covers,
                empty_support_S4_invariant_forbidden_sets=invariant)


def finish(record):
    assert validate_minor(record)
    es = set(map(tuple, record['edges']))
    groups = record['branch_sets']
    record['all_ten_adjacencies'] = [dict(branch_pair=[i, j], original_edge=next(
        edge(v, w) for v in sorted(groups[i]) for w in sorted(groups[j])
        if edge(v, w) in es)) for i, j in combinations(range(5), 2)]
    return record


def single_component_controls():
    left, right = ['x', 'a0', 'a1', 'a2'], ['y', 'b0', 'b1', 'b2']
    ports = left[1:] + right[1:]
    internal = {edge(v, w) for block in (left, right) for v, w in combinations(block, 2)}
    internal.add(edge('x', 'y'))
    es = internal | {edge('r', p) for p in ports}
    witness = finish(dict(original_root='r', original_contact_order=ports,
        original_contact_partition=[6], original_spokes=[],
        original_K4_blocks=[left, right], original_negative_bridge=['x', 'y'],
        edges=sorted(es), branch_sets=[[v] for v in left] + [['r'] + right]))
    assert sum('r' in e for e in es) == 6
    assert all(sum(v in e for e in es) == 4 for v in left + right)
    vertices, colorings = sorted(left + right), {}
    for colors in product(range(4), repeat=8):
        f = dict(zip(vertices, colors, strict=True))
        if all(f[v] != f[w] for v, w in internal):
            t = tuple(f[p] for p in ports)
            colorings.setdefault(t, colors)
    relation = sorted(colorings)
    assert len(relation) == 432 and all(set(t) == U for t in relation)
    analytic = [a + b for a, b in product(permutations(range(4), 3), repeat=2)
                if U - set(a) != U - set(b)]
    assert sorted(analytic) == relation
    assert all({t[j] for t in relation} == U for j in range(6))
    joined = [(a,) + t for t, a in product(relation, range(4)) if a not in t]
    assert joined == []
    marginal_root = {a for a in range(4) for t in product(range(4), repeat=6) if a not in t}
    assert marginal_root == U
    releases = []
    for j in range(6):
        lifts = [(a,) + t for t, a in product(relation, range(4))
                 if all(c != a for k, c in enumerate(t) if k != j)]
        assert len(lifts) == 144
        for a in range(4):
            fiber = [t for t in lifts if t[0] == a]
            assert len(fiber) == 36
            t = fiber[0]
            releases.append(dict(deleted_original_contact=ports[j], root_color=a,
                original_contact_tuple=t[1:], full_coloring_witness=colorings[t[1:]],
                complete_lift_count=len(fiber)))
    negatives = []
    for name, removed in (('missing_original_bridge', {edge('x', 'y')}),
                          ('missing_named_root_contact', {edge('r', 'a0')}),
                          ('disconnected_other_K4_hub', {edge('r', p) for p in right[1:]})):
        damaged = dict(witness, edges=sorted(es - removed))
        assert not validate_minor(damaged)
        negatives.append(dict(failure=name, removed_original_edges=sorted(removed)))
    return dict(original_minor=witness, vertex_order=vertices,
        complete_ordered_six_contact_relation=relation,
        complete_coloring_witnesses=[colorings[t] for t in relation],
        exact_full_seven_port_join=joined, endpoint_marginals=[sorted(U)] * 6,
        incorrect_marginal_product_root_projection=sorted(marginal_root),
        named_contact_deletion_lifts=releases, negative_controls=negatives,
        scope='Nonplanar abstract control; the unbounded palette saturation is a paper proof.')


def no_spoke_short_support_controls():
    records, seen, digest, count = [], set(), sha256(), 0
    for base in original_lift_controls():
        r, b = base['original_spoke']
        edges = [tuple(e) for e in base['edges'] if tuple(e) != edge(r, b)]
        signature = (tuple(edges), tuple(base['external_path']),
                     tuple(base['support_envelope']))
        if signature in seen:
            continue
        seen.add(signature)
        assert not any(r in e and any(v < 5 for v in e if v != r) for e in edges)
        record = {k: v for k, v in base.items() if k != 'original_spoke'}
        record.update(edges=edges, original_spokes=[],
            external_path_ownership='a different original component, not a new spoke')
        record = finish(record)
        digest.update(json.dumps(record, sort_keys=True).encode())
        count += 1
        if len(records) < 12:
            records.append(record)
    assert count == 480
    return dict(no_spoke_K5_controls=count, representative_records=records,
        all_records_sha256=digest.hexdigest(),
        scope='Seen-color two-hub lifts only; unseen-color three-hub proof is reused on paper.')


def five_contact_exterior_controls():
    records = []
    for kind, landing, length, shared in product(
            ('positive_C5', 'three_positive_triangles'), range(5), (1, 3), (False, True)):
        base = minor(kind, 0, tuple(range(5)), 1, shared)
        es = set(map(tuple, base['edges'])) - {edge('r', 'b0')}
        path = ['r', 'original_V_contact'] + [f'original_V_path_{j}' for j in range(length - 1)]
        path.append(f'b{landing}')
        es.update(edge(v, w) for v, w in zip(path, path[1:]))
        groups = [g[:] for g in base['branch_sets']]
        groups[4].extend(path[1:-1])
        record = {k: v for k, v in base.items() if k not in ('spoke', 'adjacency')}
        record.update(edges=sorted(es), branch_sets=groups, original_spokes=[],
            exterior_original_unary_path=path,
            original_contact_partition=[5, 1],
            original_component_contact_order=[base['contact_order'], ['original_V_contact']])
        assert {v if u == 'r' else u for u, v in es if 'r' in (u, v)} == set(
            base['contact_order'] + ['original_V_contact'])
        records.append(finish(record))
    assert len(records) == 40
    damaged = dict(records[0], edges=[e for e in records[0]['edges']
                    if e != edge('r', 'original_V_contact')])
    assert not validate_minor(damaged)
    return dict(records=records, missing_exterior_contact_negative=True,
        scope='Minor skeletons preserve six contacts and ownership; not full degree-list sources.')


def build():
    palettes, incidence = four_palettes()
    reduction = reduction_controls()
    single = single_component_controls()
    short = no_spoke_short_support_controls()
    five = five_contact_exterior_controls()
    paths = [Path(__file__).resolve()] + [ROOT / 'scripts' / (n + '.py') for n in (
        'c5_no_spoke_exterior', 'c5_short_support_singleton',
        'c5_excess_two_five_contact', 'c5_single_spoke_four', 'c5_single_spoke_three_one')]
    return dict(schema=1, scope='t=0 six original contacts: reduce eleven partitions to (4,2)',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        partition_reduction=reduction, four_palette_types=palettes,
        four_palette_incidence_controls=incidence, original_single_component=single,
        no_spoke_short_support=short, five_contact_external_hub=five,
        summary=dict(partitions=11, excluded_before_binary_path=10, remaining_partition=[4, 2],
            capacity_comparisons=reduction['capacity_checks'], four_palette_types=len(palettes),
            local_incidence_controls=len(incidence), single_component_relation_tuples=432,
            named_contact_deletion_lifts=864, no_spoke_short_support_K5_controls=480,
            five_contact_exterior_K5_controls=40, graph_enumeration=False,
            disk_realizability_claim=False, new_Lean_theorem=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == payload, 'certificate differs'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
