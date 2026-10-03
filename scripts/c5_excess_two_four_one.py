#!/usr/bin/env python3
"""t=1, original (4,1): common active forest and two fixed pendant bags.

Checks an over-approximate support/profile domain, complete six-port algebra,
and original-edge K5 controls. No source graph enumeration or realizability.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_independent_support_capacity import ROWS, U, normalize
from c5_excess_two_three_unary import orbit
from c5_excess_two_binary_three_unary import invariant_sets, transport
from c5_single_spoke_frame_arc import admissible_supports
from c5_single_spoke_cross_row import joint_supports
from c5_single_spoke_two_two_minor import verify_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_four_one/observations.json'
TARGETS = tuple(sorted(set(orbit(933) + orbit(941))))
SINGLETONS = tuple(i for i, row in enumerate(ROWS) if len(set(row)) == 3)


@lru_cache(None)
def moved(base, values, forbidden):
    return transport(base, values, forbidden)


@lru_cache(None)
def bag_evidence(envelope, queries):
    """Same two original bags, in this fixed spoke-slit envelope only."""
    assert queries and all(len(f) == 2 for _, f in queries)
    if any(3 not in forbidden for _, forbidden in queries):
        return dict(applicable=False, reason='a_rejected_pair_does_not_contain_D',
                    eliminated=False)
    family = {frozenset(t) for n in range(len(envelope) + 1)
              for t in combinations(sorted(envelope), n)}
    stages = []
    for i, forbidden in queries:
        family &= set(admissible_supports(ROWS[i], envelope, forbidden))
        stages.append(dict(row=i, forbidden=forbidden,
                           remaining_supports=sorted(tuple(sorted(t)) for t in family)))
    for (i, forbidden), (j, other) in combinations(queries, 2):
        family &= set(joint_supports(ROWS[i], ROWS[j], envelope, forbidden, other))
        stages.append(dict(rows=[i, j], forbidden=[forbidden, other],
                           remaining_supports=sorted(tuple(sorted(t)) for t in family)))
    # Independent 24-permutation definition, with one representation throughout.
    brute = set()
    for n in range(len(envelope) + 1):
        for raw in combinations(sorted(envelope), n):
            support = frozenset(raw)
            local_ok = all({p[c] for c in forbidden} == set(forbidden)
                           for i, forbidden in queries for p in permutations(range(4))
                           if all(p[ROWS[i][v]] == ROWS[i][v] for v in support))
            cross_ok = all({p[c] for c in forbidden} == set(other)
                           for (i, forbidden), (j, other) in combinations(queries, 2)
                           for p in permutations(range(4))
                           if all(p[ROWS[i][v]] == ROWS[j][v] for v in support))
            if local_ok and cross_ok:
                brute.add(support)
    assert family == brute
    # Each envelope has length at most three, so no repeated boundary vertex.
    # These positions never use the complementary arc across the original spoke.
    intervals = [dict(support=sorted(t), interval=[min(envelope.index(v) for v in t),
                                          max(envelope.index(v) for v in t)])
                 for t in sorted(tuple(sorted(t)) for t in family) if t]
    compatible = [[i, j] for i, left in enumerate(intervals)
                  for j, right in enumerate(intervals)
                  if left['interval'][1] <= right['interval'][0]
                  or right['interval'][1] <= left['interval'][0]]
    return dict(applicable=True, stages=stages,
                final_supports=sorted(tuple(sorted(t)) for t in family),
                fixed_envelope=envelope, pendant_bag_intervals=intervals,
                compatible_ordered_pairs=compatible, independent_permutation_check=True,
                eliminated=not compatible)


def solve(envelopes, target):
    maps, options = {}, {}
    for component, (support, capacity) in enumerate(zip(envelopes, (2, 1))):
        representatives = {}
        for i, row in enumerate(ROWS):
            values = tuple(row[j] for j in support)
            shape = normalize(values)
            key = component, shape
            if shape not in representatives:
                representatives[shape] = values
                options[key] = invariant_sets(set(values), capacity)
            maps[component, i] = key, representatives[shape], values
    row_options = []
    for i, row in enumerate(ROWS):
        data = [maps[c, i] for c in range(2)]
        choices = []
        for indexes in product(*(range(len(options[d[0]])) for d in data)):
            forbidden = tuple(moved(d[1], d[2], options[d[0]][j])
                              for d, j in zip(data, indexes))
            accepted = bool(U - {row[0]} - set().union(*map(set, forbidden)))
            if accepted != bool(target >> i & 1):
                continue
            assignment = dict((d[0], j) for d, j in zip(data, indexes))
            choices.append((assignment, forbidden))
        row_options.append(choices)
    result = dict(original_spoke=0, component_envelopes=envelopes, target=target,
                  row_option_counts=list(map(len, row_options)),
                  local_profile_domains=[dict(component=c, local_pattern=pattern,
                                               forbidden_options=fs)
                                         for (c, pattern), fs in sorted(options.items())])
    if any(not opts for opts in row_options):
        return dict(result, reason='empty_row_domain', empty_rows=[i for i, opts in
                    enumerate(row_options) if not opts], search_nodes=0,
                    complete_profiles=0, bag_certificates=[], remaining=0)
    order = sorted(range(10), key=lambda i: len(row_options[i]))
    chosen, counters, certificates = {}, Counter(), {}
    digest = sha256()

    def dfs(position, assignment, unary_D_role=None):
        counters['search_nodes'] += 1
        if position == 10:
            counters['complete_profiles'] += 1
            queries = tuple((i, chosen[i][0]) for i in range(10) if not target >> i & 1)
            assert all(len(f) == 2 for _, f in queries)
            evidence = bag_evidence(envelopes[0], queries)
            # Keep the D guard explicit: a non-D pair is never silently sent
            # through the shared-D active-forest argument.
            assert evidence['applicable'], (envelopes, target, queries)
            # The original whole-component profile already obeys the same
            # equivariance. Its full envelope must survive every bag screen.
            assert tuple(sorted(envelopes[0])) in evidence['final_supports']
            assert evidence['eliminated'], (envelopes, target, queries, evidence)
            certificates[queries] = evidence
            digest.update(json.dumps([chosen[i] for i in range(10)], separators=(',', ':')).encode())
            return
        i = order[position]
        for extension, forbidden in row_options[i]:
            if any(key in assignment and assignment[key] != value
                   for key, value in extension.items()):
                counters['inconsistent_shared_profile'] += 1
                continue
            new_role = unary_D_role
            if i in SINGLETONS and forbidden[1]:
                role = 3 in forbidden[1]
                if unary_D_role is not None and unary_D_role != role:
                    counters['inconsistent_original_unary_D_role'] += 1
                    continue
                new_role = role
            chosen[i] = forbidden
            dfs(position + 1, assignment | extension, new_role)
            del chosen[i]

    dfs(0, {})
    return dict(result, reason='shared_profiles_and_fixed_pendant_bags', row_search_order=order,
                search_counts=dict(counters), search_nodes=counters['search_nodes'],
                complete_profiles=counters['complete_profiles'],
                complete_profiles_sha256=digest.hexdigest(), remaining=0,
                bag_certificates=[dict(rejected_row_pairs=q, evidence=e)
                                  for q, e in sorted(certificates.items())])


def triangle_minor(spoke, connector_length, arm_lengths, subdivide, shared_landing):
    edges = {tuple(sorted((f'b{i}', f'b{(i+1)%5}'))) for i in range(5)}

    def edge(a, b):
        edges.add(tuple(sorted((a, b))))

    edge('r', f'b{spoke}')
    y = 'x' if connector_length == 0 else 'y'
    for triangle in (['a', 'b', 'x'], ['c', 'd', y]):
        for a, b in zip(triangle, triangle[1:] + triangle[:1]):
            edge(a, b)
    connector = ['x'] if connector_length == 0 else (
        ['x'] + [f'j{i}' for i in range(connector_length - 1)] + ['y'])
    for a, b in zip(connector, connector[1:]):
        edge(a, b)
    arms = []
    for label, length in zip('abcd', arm_lengths):
        arm = [label] + [f'{label}p{i}' for i in range(length)]
        for a, b in zip(arm, arm[1:]):
            edge(a, b)
        edge(arm[-1], 'r')
        arms.append(arm)
    selected = ['a', 'b', 'c'] if connector_length == 0 else ['a', 'b', 'x']
    outside = {f'b{i}' for i in range(5)}
    tethers = []
    for j, vertex in enumerate(selected):
        landing = spoke if shared_landing else (spoke + j + 1) % 5
        tether = [vertex, f'{vertex}t', f'b{landing}'] if subdivide else [vertex, f'b{landing}']
        for a, b in zip(tether, tether[1:]):
            edge(a, b)
        outside.update(tether[1:])
        tethers.append(tether)
        assert sum(vertex in e for e in edges) == 4
    if connector_length == 0:
        bags = [set(arms[0]), set(arms[1]), {'x', 'c'}, {'r'} | set(arms[3]), outside]
    else:
        rest = set(connector[1:]) | set(arms[2]) | set(arms[3]) | {'r'}
        bags = [set(arms[0]), set(arms[1]), {'x'}, rest, outside]
    return dict(spoke=spoke, connector_length=connector_length, arm_lengths=arm_lengths,
                ordered_original_contacts=[arm[-1] for arm in arms],
                original_arms=arms, original_connector=connector, original_tethers=tethers,
                edges=sorted(edges), branch_sets=[sorted(b) for b in bags],
                adjacencies=verify_minor(edges, bags))


def minor_controls():
    digest, parameters, examples = sha256(), [], []
    for spoke, connector, arms, subdivide, shared in product(
            range(5), range(4), product((0, 1), repeat=4), (False, True), (False, True)):
        record = triangle_minor(spoke, connector, arms, subdivide, shared)
        parameters.append([spoke, connector, list(arms), subdivide, shared])
        digest.update(json.dumps(record, sort_keys=True).encode())
        if arms == (0, 0, 0, 0):
            examples.append(record)
    base = triangle_minor(0, 0, (0, 0, 0, 0), False, False)
    edges, bags = set(map(tuple, base['edges'])), list(map(set, base['branch_sets']))
    negative = []
    for name, bad_edges, bad_bags in (
            ('missing_original_spoke', edges - {('b0', 'r')}, bags),
            ('missing_shared_case_X_Z_adjacency',
             {e for e in edges if not ((e[0] in bags[2] and e[1] in bags[3])
                                      or (e[1] in bags[2] and e[0] in bags[3]))}, bags),
            ('overlapping_shared_cut_branch_sets', edges, [bags[0] | {'x'}] + bags[1:])):
        try:
            verify_minor(bad_edges, bad_bags)
        except AssertionError:
            negative.append(name)
        else:
            raise AssertionError(name)
    return dict(parameters=parameters, original_edge_examples=examples,
                all_controls_sha256=digest.hexdigest(), negative_controls=negative)


def gluing_controls():
    ports = tuple(product(range(4), repeat=4))
    domains = [tuple(c for c in range(4) if bits >> c & 1) for bits in range(1, 16)]
    checked, digest = 0, sha256()

    def check(relation, domain):
        nonlocal checked
        tuples = tuple((r, *p, u) for r in range(4) for p in relation for u in domain
                       if r not in (*p, u))
        direct = tuple(sorted({(r, *p, u) for p in relation for u in domain
                               for r in U - set(p) - {u}}))
        assert tuples == direct
        forbidden = set.intersection(*(set(p) for p in relation))
        if len(domain) == 1:
            forbidden |= set(domain)
        assert {t[0] for t in tuples} == U - forbidden
        for spoke_color in range(4):
            assert {t[0] for t in tuples if t[0] != spoke_color} == U - forbidden - {spoke_color}
        digest.update(json.dumps([relation, domain, tuples], separators=(',', ':')).encode())
        checked += 1

    for p, domain in product(ports, domains):
        check((p,), domain)
    for relation in combinations(ports, 2):
        for color in range(4):
            check(relation, (color,))
    return dict(complete_six_port_checks=checked, spoke_restrictions=checked * 4,
                tuples_sha256=digest.hexdigest())


def build():
    arcs = [(a, b) for a in range(6) for b in range(a + 2, 6)]
    ordered = [(a, b) for a, b in product(arcs, repeat=2) if a[1] <= b[0]]
    assert len(ordered) == 5
    records = []
    for shape in ordered:
        for ownership in permutations(range(2)):
            envelopes = tuple(tuple(i % 5 for i in range(shape[j][0], shape[j][1] + 1))
                              for j in ownership)
            for target in TARGETS:
                result = solve(envelopes, target)
                records.append(dict(original_slit_intervals=shape, component_ownership=ownership,
                                    **result))
    assert len(records) == 100 and all(r['remaining'] == 0 for r in records)
    # Guard controls: a pair lacking the one common unused colour is outside
    # the pendant-bag theorem, even when a generic set screen could reject it.
    guard = bag_evidence((0, 1, 2), ((0, (0, 1)),))
    assert not guard['applicable'] and not guard['eliminated']
    positive = bag_evidence((0, 1, 2, 3), ((0, (2, 3)),))
    assert positive['applicable'] and not positive['eliminated']
    assert positive['final_supports'] and positive['compatible_ordered_pairs']
    minors, gluing = minor_controls(), gluing_controls()
    paths = [Path(__file__).resolve(), ROOT / 'scripts/c5_independent_support_capacity.py',
             ROOT / 'scripts/c5_excess_two_three_unary.py',
             ROOT / 'scripts/c5_excess_two_binary_three_unary.py',
             ROOT / 'scripts/c5_single_spoke_frame_arc.py',
             ROOT / 'scripts/c5_single_spoke_cross_row.py',
             ROOT / 'scripts/c5_single_spoke_two_two_minor.py']
    return dict(schema=1, scope='t=1 original (4,1) complete-source exclusion',
                source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                               for p in paths}, pattern_order=ROWS,
                original_ports=['r', 'C_x0', 'C_x1', 'C_x2', 'C_x3', 'W_w'],
                original_component_order=['C_four_contact', 'W_unary'],
                target_orbits={str(m): orbit(m) for m in (933, 941)},
                spoke_slit_order=[0, 1, 2, 3, 4, 0], ordered_positive_span_intervals=ordered,
                source_exclusions=records, connected_active_tree_minors=minors,
                full_gluing_controls=gluing, non_D_pair_guard=guard,
                compatible_pendant_bags_positive_control=positive,
                paper_dependencies=['tight Gallai palettes and four-contact three-ban K5',
                    'short-support exclusion and same-spoke ordered original support envelopes',
                    'original unary unused-colour conservation',
                    'incidence-column independence and the one common D-membership coefficient',
                    'two active triangles original tethers and K5',
                    'two fixed contact pendant bags and complete rooted residual transport'],
                summary=dict(ordered_slit_interval_pairs=len(ordered), source_queries=len(records),
                    queries_reaching_complete_profiles=sum(bool(r['complete_profiles']) for r in records),
                    complete_profiles=sum(r['complete_profiles'] for r in records),
                    shared_pendant_bag_certificates=sum(len(r['bag_certificates']) for r in records),
                    original_two_triangle_minor_controls=len(minors['parameters']),
                    complete_six_port_checks=gluing['complete_six_port_checks'], remaining=0,
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
