#!/usr/bin/env python3
"""t=2, original (4): common-D active forest and fixed pendant bags.

Reuses the t=1 four-contact argument in the same original graph. Checks all
named spoke/sector/target cases, exact five-port joins, and two-spoke K5
skeletons. No graph catalog, source realizability, or new Lean theorem.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U
from c5_excess_two_three_unary import orbit
from c5_excess_two_four_one import bag_evidence, triangle_minor
from c5_single_spoke_two_two_minor import verify_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_two_spoke_four/observations.json'
TARGETS = tuple(sorted(set(orbit(933) + orbit(941))))


def sectors(s, t):
    """Two actual closed sectors; preserve linear order from each spoke."""
    assert 0 <= s < t < 5
    result = []
    for start, end in ((s, t), (t, s)):
        arc = [start]
        while arc[-1] != end:
            arc.append((arc[-1] + 1) % 5)
        assert len(set(arc)) == len(arc)
        result.append(tuple(arc))
    assert sum(len(arc) - 1 for arc in result) == 5
    return result


def source_queries():
    records = []
    for s, t in combinations(range(5), 2):
        for sector_index, envelope in enumerate(sectors(s, t)):
            for target in TARGETS:
                rejected = tuple(i for i in range(10) if not target >> i & 1)
                assert rejected and all(len(set(ROWS[i])) == 3 for i in rejected)
                equal_rows = [i for i in rejected if ROWS[i][s] == ROWS[i][t]]
                record = dict(original_spokes=[s, t], actual_sector=sector_index,
                    fixed_sector_order=envelope, target=target,
                    original_component='C_four_contact', rejected_rows=rejected,
                    same_spoke_color_rejections=equal_rows)
                if equal_rows:
                    witness = equal_rows[0]
                    forbidden = sorted(U - {ROWS[witness][s]})
                    assert len(forbidden) == 3
                    records.append(dict(record, reason='four_contact_three_ban_K5',
                        three_ban_witness=dict(row=witness, required_forbidden=forbidden),
                        remaining=0))
                    continue
                queries = tuple((i, tuple(sorted(U - {ROWS[i][s], ROWS[i][t]})))
                                for i in rejected)
                assert all(len(f) == 2 and 3 in f for _, f in queries)
                evidence = bag_evidence(envelope, queries)
                assert evidence['applicable'] and evidence['eliminated']
                # A nonempty family and the full original sector are positive
                # controls. Exclusion concerns two simultaneous original bags.
                assert evidence['final_supports']
                assert tuple(sorted(envelope)) in evidence['final_supports']
                records.append(dict(record, reason='fixed_pendant_bag_sector_order',
                    rejected_row_pairs=queries, bag_certificate=evidence, remaining=0))
    assert len(records) == 200 and all(r['remaining'] == 0 for r in records)
    counts = Counter(r['reason'] for r in records)
    assert counts == {'four_contact_three_ban_K5': 100,
                      'fixed_pendant_bag_sector_order': 100}
    # This is checked rather than assumed: all nonadjacent pairs have a
    # same-colour rejection; all adjacent pairs use the simultaneous-bag proof.
    for record in records:
        s, t = record['original_spokes']
        adjacent = (t - s) in (1, 4)
        assert adjacent == (record['reason'] == 'fixed_pendant_bag_sector_order')
    return records


def gluing_controls():
    """All singleton/two-tuple relations, retaining ordered four contacts."""
    ports = tuple(product(range(4), repeat=4))
    checked, digest = 0, sha256()

    def check(relation):
        nonlocal checked
        forbidden = set.intersection(*(set(p) for p in relation))
        unrestricted = tuple((a, *p) for a in range(4) for p in relation if a not in p)
        assert {t[0] for t in unrestricted} == U - forbidden
        for e, f in product(range(4), repeat=2):
            joined = tuple(t for t in unrestricted if t[0] != e and t[0] != f)
            direct = tuple((a, *p) for a in range(4) for p in relation
                           if all(a != c for c in (*p, e, f)))
            assert joined == direct
            assert {t[0] for t in joined} == U - forbidden - {e, f}
            digest.update(json.dumps([relation, [e, f], joined],
                                     separators=(',', ':')).encode())
            checked += 1

    for p in ports:
        check((p,))
    for relation in combinations(ports, 2):
        check(relation)
    assert checked == 526336
    # Coordinate marginals falsely produce lifts for an empty full join.
    relation = ((0, 1, 2, 3), (1, 2, 3, 0))
    marginal_product = tuple(product(*(sorted({p[j] for p in relation}) for j in range(4))))
    exact = [(a, *p) for a in range(4) for p in relation
             if a not in (*p, 0, 1)]
    fake = [(a, *p) for a in range(4) for p in marginal_product
            if a not in (*p, 0, 1)]
    assert exact == [] and {t[0] for t in fake} == {2, 3}
    return dict(complete_five_port_checks=checked,
        singleton_relations=len(ports), two_tuple_relations=32640,
        spoke_colour_pairs=list(product(range(4), repeat=2)),
        all_complete_joins_sha256=digest.hexdigest(),
        marginal_negative_control=dict(ordered_relation=relation, spoke_colours=[0, 1],
            exact_join=exact, false_marginal_join=fake))


def two_spoke_minor(s, t, selected, connector, arms, subdivide, shared):
    record = triangle_minor(selected, connector, arms, subdivide, shared)
    es = set(map(tuple, record['edges']))
    es.add(tuple(sorted(('r', f'b{s}'))))
    es.add(tuple(sorted(('r', f'b{t}'))))
    bags = list(map(set, record['branch_sets']))
    contacts = set(record['ordered_original_contacts'])
    neighbours = {v if u == 'r' else u for u, v in es if 'r' in (u, v)}
    assert neighbours == contacts | {f'b{s}', f'b{t}'} and len(neighbours) == 6
    return dict(record, original_spokes=[s, t], selected_hub_spoke=selected,
                edges=sorted(es), adjacencies=verify_minor(es, bags))


def minor_controls():
    digest, count, examples = sha256(), 0, []
    for s, t in combinations(range(5), 2):
        for selected, connector, arms, subdivide, shared in product(
                (s, t), range(4), product((0, 1), repeat=4), (False, True), (False, True)):
            record = two_spoke_minor(s, t, selected, connector, arms, subdivide, shared)
            count += 1
            digest.update(json.dumps(record, sort_keys=True).encode())
            if selected == s and connector in (0, 1) and arms == (0, 0, 0, 0):
                examples.append(record)
    assert count == 5120 and len(examples) == 80
    base = two_spoke_minor(0, 1, 0, 0, (0, 0, 0, 0), False, True)
    es, bags = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    # Either one of the original spokes is enough for the same minor.
    for omitted in (0, 1):
        verify_minor(es - {tuple(sorted(('r', f'b{omitted}')))}, bags)
    failures = []
    for name, bad_edges, bad_bags in (
            ('both_original_spokes_missing', es - {('b0', 'r'), ('b1', 'r')}, bags),
            ('shared_case_X_Z_adjacency_missing',
             {e for e in es if not ((e[0] in bags[2] and e[1] in bags[3])
                                   or (e[1] in bags[2] and e[0] in bags[3]))}, bags),
            ('overlapping_original_branch_sets', es, [bags[0] | {'x'}] + bags[1:])):
        try:
            verify_minor(bad_edges, bad_bags)
        except AssertionError:
            failures.append(name)
        else:
            raise AssertionError(name)
    return dict(controls=count,
        ordered_parameter_names=['s', 't', 'selected_hub_spoke', 'connector_length',
                                 'four_original_arm_lengths', 'subdivided_tethers',
                                 'shared_boundary_landing'],
        parameter_domain=dict(original_spoke_pairs=list(combinations(range(5), 2)),
            selected_hub_spoke='one of the same original pair, in increasing order',
            connector_lengths=list(range(4)),
            four_original_arm_lengths=list(product((0, 1), repeat=4)),
            subdivided_tethers=[False, True], shared_boundary_landing=[False, True]),
        original_edge_examples=examples,
        all_controls_sha256=digest.hexdigest(), negative_controls=failures,
        either_original_spoke_positive_control=True)


def build():
    queries = source_queries()
    minors, gluing = minor_controls(), gluing_controls()
    guard = bag_evidence((0, 1, 2), ((0, (0, 1)),))
    positive = bag_evidence((0, 1, 2, 3), ((0, (2, 3)),))
    assert not guard['applicable'] and not guard['eliminated']
    assert positive['applicable'] and not positive['eliminated']
    assert positive['compatible_ordered_pairs']
    paths = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
        ROOT / 'scripts/c5_excess_two_three_unary.py',
        ROOT / 'scripts/c5_excess_two_four_one.py',
        ROOT / 'scripts/c5_excess_two_binary_three_unary.py',
        ROOT / 'scripts/c5_single_spoke_frame_arc.py',
        ROOT / 'scripts/c5_single_spoke_cross_row.py',
        ROOT / 'scripts/c5_single_spoke_two_two_minor.py']
    return dict(schema=1, scope='t=2 original (4) whole-source exclusion for 933/941',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        pattern_order=ROWS, original_ports=['r', 'C_x0', 'C_x1', 'C_x2', 'C_x3'],
        original_component_order=['C_four_contact'],
        target_orbits={str(m): orbit(m) for m in (933, 941)}, source_queries=queries,
        connected_active_tree_minors=minors, full_gluing_controls=gluing,
        non_D_pair_guard=guard, compatible_pendant_bags_positive_control=positive,
        paper_dependencies=['connected exterior K4 and four-contact three-ban K5',
            'same original incidence matrix and common D-membership coefficient',
            'four-leaf active forest: connected two triangles or two bridge paths',
            'original tethers and connected-case K5, including shared triangle cut',
            'two fixed single-contact pendant bags and exact rooted residual pairs',
            'same original two-spoke sector and disjoint open support hulls'],
        summary=dict(original_spoke_pairs=10, original_spoke_sector_target_queries=200,
            same_spoke_colour_three_ban_exclusions=100,
            simultaneous_fixed_pendant_bag_exclusions=100,
            nonempty_pendant_bag_support_families=100,
            original_two_spoke_minor_controls=minors['controls'],
            complete_five_port_checks=gluing['complete_five_port_checks'], remaining=0,
            graph_enumeration=False, disk_realizability_claimed=False, new_lean_theorem=False))


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
