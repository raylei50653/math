#!/usr/bin/env python3
"""E3 unique-degree-six: T4 plus three named singleton rejections only.

Finite necessary palette interfaces, original support envelopes and exact
positive-control relations. No source graph search, planarity oracle, 4CT
oracle, exact source Sigma mask, or omitted-component-full-acceptance screen.
Arbitrary-size conclusions require the cited paper lemmas in E3 REPORT.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_e3/degree6.json'
CONTROL = ROOT / 'artifacts/c5_excess_two_e3/positive_control_inputs.json'
COLORS = tuple(range(4))
U = frozenset(COLORS)
B = frozenset(range(5))
FRAME = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in B)
PERMS = tuple(permutations(COLORS))


def normal(values):
    names = {}
    return tuple(names.setdefault(v, len(names)) for v in values)


ROWS = tuple(sorted({normal(row) for row in product(COLORS, repeat=5)
                     if all(row[i] != row[(i + 1) % 5] for i in B)}))
ACCEPT = frozenset((2, 5, 7, 8, 9))
REJECT = frozenset((1, 4, 6))
SELECT = tuple(sorted(ACCEPT | REJECT))
SINGLETON = {i: next(v for v in B if row.count(row[v]) == 1)
             for i, row in enumerate(ROWS) if len(set(row)) == 3}
assert {SINGLETON[i] for i in REJECT} == {0, 1, 3}


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def invariant(seen, capacity):
    return [tuple(raw) for size in range(capacity + 1)
            for raw in combinations(COLORS, size)
            if all({p[c] for c in raw} == set(raw) for p in PERMS
                   if all(p[c] == c for c in seen))]


@lru_cache(None)
def moved(base, values, forbidden):
    maps = [p for p in PERMS if all(p[a] == b for a, b in zip(base, values))]
    answers = {tuple(sorted(p[c] for c in forbidden)) for p in maps}
    assert len(answers) == 1
    return answers.pop()


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    reached = {min(vertices)}
    while True:
        more = reached | {a for a, b in edges if b in reached and a in vertices} | {
            b for a, b in edges if a in reached and b in vertices}
        if more == reached:
            return reached == vertices
        reached = more


PARTITIONS = tuple((tuple(sorted(left)), tuple(sorted(B - set(left))))
                   for size in range(1, 5) for left in combinations(range(5), size)
                   if 0 in left and connected(left, FRAME) and connected(B - set(left), FRAME))
assert len(PARTITIONS) == 10


@lru_cache(None)
def support_family(envelope, queries):
    """Every subset and all 24 literal permutations; no normalized components."""
    result = []
    for size in range(len(envelope) + 1):
        for support in combinations(sorted(envelope), size):
            local = all({p[c] for c in f} == set(f)
                        for i, f in queries for p in PERMS
                        if all(p[ROWS[i][v]] == ROWS[i][v] for v in support))
            cross = all({p[c] for c in f} == set(g)
                        for (i, f), (j, g) in combinations(queries, 2) for p in PERMS
                        if all(p[ROWS[i][v]] == ROWS[j][v] for v in support))
            if local and cross:
                result.append(support)
    return tuple(result)


@lru_cache(None)
def path_evidence(envelope, external, queries):
    family = support_family(envelope, queries)
    record = dict(binary_envelope=envelope, original_external_anchors=external,
                  literal_residual_rows=queries, admissible_actual_bag_supports=family,
                  anchors_are_spokes_and_other_component_actual_envelope_endpoints=True)
    if not family:
        return dict(record, exclusion='empty_actual_bag_support_family')
    for left, right in PARTITIONS:
        if set(external) & set(left) and set(external) & set(right) and all(
                set(t) & set(left) and set(t) & set(right) for t in family):
            return dict(record, exclusion='common_two_frame_arcs_K5',
                        frame_partition=[left, right],
                        branch_set_recipe=['original W_j', 'original W_(j+1)',
                                           'r, remaining contact path, other original component',
                                           'left original frame arc', 'right original frame arc'])
    forced = set.intersection(*map(set, family))
    for pair in combinations(sorted(forced), 2):
        landing = sorted(set(external) - set(pair))
        if landing:
            return dict(record, exclusion='forced_pair_three_frame_arcs_K5',
                        forced_pair=pair, original_external_landing=landing[0])
    return dict(record, exclusion=None)


@lru_cache(None)
def first_bridge(envelope, external, queries):
    pairs = tuple((i, f) for i, f in queries if len(f) == 2)
    if not pairs:
        return None
    singles = []
    for qi, fq in queries:
        if len(fq) != 1:
            continue
        c = fq[0]
        for ri, fr in pairs:
            kept = tuple(h for h in COLORS if all(
                (ROWS[qi][v] == h) == (ROWS[ri][v] == h) for v in envelope))
            if c not in kept:
                continue
            base = dict(singleton_row=qi, singleton_forbidden=c, reference_pair_row=ri,
                        pair_forbidden=fr, conserved_envelope_membership_colors=kept)
            if c not in fr:
                return dict(base, exclusion='first_endpoint_conserved_color_contradiction')
            betas = tuple(h for h in COLORS if h != c and
                          {c, h} & set(kept) == set(fr) & set(kept))
            singles.append(dict(base, possible_original_first_bridge_beta=betas))
            break
    if not singles:
        return None
    branches = []
    for betas in product(*(r['possible_original_first_bridge_beta'] for r in singles)):
        residuals = tuple(sorted(pairs + tuple(
            (r['singleton_row'], tuple(sorted((r['singleton_forbidden'], beta))))
            for r, beta in zip(singles, betas))))
        evidence = path_evidence(envelope, external, residuals)
        if evidence['exclusion'] is None:
            return None
        branches.append(dict(independent_beta_by_row=betas, evidence=evidence))
    return dict(exclusion='all_common_first_bridge_residuals_excluded',
                singleton_local_residual_queries=singles, independent_row_beta_branches=branches,
                beta_scope='shared by two ends of the same original bridge in one row only')


@lru_cache(None)
def pendant_bags(envelope, queries):
    assert queries and all(len(f) == 2 for _, f in queries)
    if any(3 not in f for _, f in queries):
        return dict(applicable=False, eliminated=False, reason='pair_without_D')
    family = support_family(envelope, queries)
    intervals = [(min(envelope.index(v) for v in t), max(envelope.index(v) for v in t))
                 for t in family if t]
    compatible = [(i, j) for i, x in enumerate(intervals) for j, y in enumerate(intervals)
                  if x[1] <= y[0] or y[1] <= x[0]]
    return dict(applicable=True, eliminated=not compatible, literal_rejected_pair_rows=queries,
                fixed_spoke_sector_or_slit_order=envelope, actual_bag_support_family=family,
                original_bag_hull_intervals=intervals, compatible_bag_pairs=compatible,
                envelope_endpoints_are_actual_attachments=True)


def single_edge_carrier(spokes, envelopes, chosen):
    """A degree-four omitted core supplies an original one-edge contact path."""
    if len(spokes) != 2 or len(envelopes) != 2:
        return None
    for c in range(2):
        envelope = envelopes[c]
        for qi in sorted(set(chosen) & REJECT):
            if SINGLETON[qi] in set(spokes) | set(envelope):
                continue
            f = chosen[qi][c]
            if {ROWS[qi][s] for s in spokes} | set(f) != U:
                continue
            assert len(f) == 2 and 3 in f
            for pi in sorted(set(chosen) & REJECT):
                other = chosen[pi][c]
                if len(other) == 1 and 3 not in other:
                    return dict(exclusion='unattached_degree_four_core_single_original_edge_D_carrier',
                        original_binary_component=c, omitted_other_binary=1-c,
                        original_spokes=spokes, binary_envelope=envelope,
                        omitted_core_rejected_row=qi, untouched_singleton=SINGLETON[qi],
                        pair_row=qi, pair_forbidden=f, singleton_row=pi,
                        singleton_forbidden=other, common_unused_color=3,
                        actual_core_classification=['triangle', 'two_triangles_direct_bridge'],
                        actual_original_contact_path='one edge x-y',
                        original_bags='components after removing that original bridge; each contains one root contact',
                        rooted_query='E_x, E_y are exact attainable contact-color sets before root pin',
                        D_membership='off-path private points have D in both lists; rooted leaf peeling uniquely fixes palette D bits',
                        contradiction='reject c with D in both E sets => E_x minus c = E_y minus c = {D}; reject D as well',
                        residuals_need_not_equal_pair=True)
    return None


def solve(spokes, envelopes, capacities, paths=(), fourbags=None, Drole=None, carrier=False, contact_arities=None):
    maps, options = {}, {}
    for comp, (envelope, capacity) in enumerate(zip(envelopes, capacities)):
        representatives = {}
        for i in SELECT:
            values = tuple(ROWS[i][v] for v in envelope)
            key = comp, normal(values)
            if key not in representatives:
                representatives[key] = values
                options[key] = invariant(set(values), capacity)
            maps[comp, i] = key, representatives[key], values
    row_options = {}
    for i in SELECT:
        data = [maps[c, i] for c in range(len(envelopes))]
        choices = []
        for ids in product(*(range(len(options[x[0]])) for x in data)):
            fs = tuple(moved(d[1], d[2], options[d[0]][j]) for d, j in zip(data, ids))
            banned = {ROWS[i][s] for s in spokes} | set().union(*map(set, fs))
            if (banned != U) != (i in ACCEPT):
                continue
            choices.append((dict((d[0], j) for d, j in zip(data, ids)), fs))
        row_options[i] = choices
    order = sorted(SELECT, key=lambda i: len(row_options[i]))
    chosen, counts, certificates = {}, Counter(), {}
    external = [tuple(sorted(set(spokes) | {envelopes[1-c][0], envelopes[1-c][-1]}))
                if len(envelopes) == 2 else tuple(spokes) for c in range(len(envelopes))]

    def excluded(evidence):
        certificates[packed(evidence).decode()] = evidence
        counts[evidence['exclusion']] += 1

    def dfs(position, assignment, role):
        counts['search_nodes'] += 1
        if position == len(order):
            return dict(literal_named_eight_row_forbidden_profile=[[i, chosen[i]] for i in SELECT],
                        original_profile_assignments=[[str(k), v] for k, v in sorted(assignment.items())],
                        unspecified_row_indices=[0, 3], source_realizability_asserted=False)
        i = order[position]
        for extension, forbidden in row_options[i]:
            if any(k in assignment and assignment[k] != v for k, v in extension.items()):
                counts['same_original_local_profile_conflicts'] += 1
                continue
            next_role = role
            if Drole is not None and i in REJECT and forbidden[Drole]:
                new_role = 3 in forbidden[Drole]
                if role is not None and role != new_role:
                    counts['same_original_D_role_conflicts'] += 1
                    continue
                next_role = new_role
            chosen[i] = forbidden
            evidence = single_edge_carrier(spokes, envelopes, chosen) if carrier else None
            if evidence:
                excluded(evidence)
                del chosen[i]
                continue
            if fourbags is not None and REJECT <= chosen.keys():
                queries = tuple((j, chosen[j][fourbags]) for j in sorted(REJECT))
                bag = pendant_bags(envelopes[fourbags], queries)
                if bag['eliminated']:
                    excluded(dict(bag, exclusion='two_fixed_original_pendant_bags_cannot_be_ordered'))
                    del chosen[i]
                    continue
            evidence = None
            for c in paths:
                queries = tuple(sorted((j, f[c]) for j, f in chosen.items() if f[c]))
                pairs = tuple((j, f) for j, f in queries if len(f) == 2)
                if not pairs:
                    continue
                pure = path_evidence(envelopes[c], external[c], pairs)
                evidence = pure if pure['exclusion'] else first_bridge(envelopes[c], external[c], queries)
                if evidence:
                    evidence = dict(evidence, original_binary_component=c)
                    break
            if evidence:
                excluded(evidence)
                del chosen[i]
                continue
            found = dfs(position + 1, assignment | extension, next_role)
            if found is not None:
                return found
            del chosen[i]
        return None

    witness = dfs(0, {}, None)
    return dict(original_spokes=spokes, original_component_envelopes=envelopes,
                component_forbidden_capacities=capacities,
                original_contact_orders=[list(range(arity)) for arity in (contact_arities or capacities)],
                envelope_interiors_are_not_asserted_attachments=True,
                accepted_row_indices=sorted(ACCEPT), rejected_row_indices=sorted(REJECT),
                unconstrained_row_indices=[0, 3], original_omission_full_acceptance_screen=False,
                same_original_profile_domains=[dict(component=k[0], equality_pattern=k[1],
                                                      forbidden_options=options[k]) for k in sorted(options)],
                row_candidate_counts=[[i, len(row_options[i])] for i in SELECT],
                row_search_order=order, search_counts=dict(sorted(counts.items())),
                exclusion_certificates=[certificates[k] for k in sorted(certificates)],
                surviving_necessary_profile=witness)


def sectors(spokes):
    return [tuple((s + k) % 5 for k in range((spokes[(j+1) % len(spokes)] - s) % 5 + 1))
            for j, s in enumerate(spokes)]


def geometry(spokes):
    arcs = sectors(spokes)
    choices = [(sid, a, b, arc[a:b+1]) for sid, arc in enumerate(arcs)
               for a in range(len(arc)) for b in range(a+2, len(arc))]
    for p, q in product(choices, repeat=2):
        if p[0] == q[0] and not (p[2] <= q[1] or q[2] <= p[1]):
            continue
        yield p[3], q[3]


def finite_interfaces():
    slit = [(a, b) for a in range(6) for b in range(a+2, 6)]
    ordered = [(a, b) for a, b in product(slit, repeat=2) if a[1] <= b[0]]
    assert len(ordered) == 5
    one_spoke = [tuple(tuple(i % 5 for i in range(iv[j][0], iv[j][1]+1)) for j in order)
                 for iv in ordered for order in permutations(range(2))]
    canonical = (((0,1,2), (2,3,4)), ((0,1,2), (3,4,0)),
                 ((0,1,2), (2,3,4,0)), ((0,1,2,3), (3,4,0)))
    zero_spoke = [tuple(tuple((v+r) % 5 for v in envelope) for envelope in shape)
                  for r in range(5) for shape in canonical]
    groups = {
        't0_(4,2)': [solve((), s, (2,2), paths=(1,), contact_arities=(4,2)) for s in zero_spoke],
        't1_(4,1)': [solve((0,), s, (2,1), fourbags=0, Drole=1, contact_arities=(4,1)) for s in one_spoke],
        't1_(3,2)': [solve((0,), s, (2,1), paths=(0,), Drole=1, contact_arities=(2,3)) for s in one_spoke],
        't2_(4)': [solve(pair, (sector,), (2,), fourbags=0, contact_arities=(4,))
                   for pair in combinations(range(5), 2) for sector in sectors(pair)],
        't2_(3,1)': [solve(pair, s, (1,1), contact_arities=(3,1)) for pair in combinations(range(5), 2)
                     for s in geometry(pair)],
        't2_(2,2)': [solve(pair, s, (2,2), paths=(0,1), carrier=True)
                     for pair in combinations(range(5), 2) for s in geometry(pair)],
        't3_(2,1)': [solve(spokes, s, (2,1)) for spokes in combinations(range(5), 3)
                     for s in geometry(spokes)],
    }
    weak = [solve(pair, s, (2,2), paths=(0,1)) for pair in combinations(range(5), 2)
            for s in geometry(pair)]
    survivors = [r for r in weak if r['surviving_necessary_profile'] is not None]
    assert len(survivors) == 2
    assert all(r['surviving_necessary_profile'] is None for rr in groups.values() for r in rr)
    three_ternary = []
    for spokes in combinations(range(5), 3):
        failed = next(i for i in sorted(REJECT) if len({ROWS[i][s] for s in spokes}) <= 2)
        available = sorted(U - {ROWS[failed][s] for s in spokes})
        assert len(available) >= 2
        three_ternary.append(dict(original_spokes=spokes, rejected_row=failed,
                                  row=ROWS[failed], root_available=available,
                                  ternary_capacity=1, contradiction='one forbidden color cannot cover two available colors'))
    return groups, survivors, three_ternary


def carrier_edge_controls():
    checks, examples = 0, []
    domains = [set(raw) for size in range(1, 5) for raw in combinations(COLORS, size) if 3 in raw]
    for c, ex, ey in product((0,1,2), domains, domains):
        def query(root):
            return sorted((x,y) for x,y in product(sorted(ex - {root}), sorted(ey - {root})) if x != y)
        if not query(c):
            assert ex - {c} == ey - {c} == {3}
            assert not query(3)
            if len(ex) == 1 or len(ey) == 1:
                examples.append(dict(non_D_root=c, exact_E_x=sorted(ex), exact_E_y=sorted(ey),
                                     root_c_fiber=query(c), root_D_fiber=query(3)))
        checks += 1
    assert checks == 192 and examples
    return dict(complete_exact_parent_query_checks=checks,
                singleton_residual_controls=examples,
                no_false_assertion_that_both_residuals_equal_a_pair=True,
                arbitrary_off_path_D_membership_proof='Each noncontact private vertex has D in both degree lists. In the rooted block tree, peel terminal blocks away from the contact. The D-indicator palette equations at private vertices and cutpoints uniquely determine each off-path block bit; subtract child bits before solving the parent. Both rejection assignments therefore have identical off-path D bits. Rooted Gallai parent queries are exact attainable-color sets, not endpoint marginals.')


def components(vertices, edges):
    todo, result = set(vertices), []
    while todo:
        group = {min(todo)}
        while True:
            more = group | {a for a,b in edges if b in group and a in todo} | {
                b for a,b in edges if a in group and b in todo}
            if more == group:
                break
            group = more
        result.append(sorted(group)); todo -= group
    return result


def literal_colorings(private, edges, row):
    included = B | set(private)
    relevant = [e for e in edges if set(e) <= included]
    output = []
    for colors in product(COLORS, repeat=len(private)):
        f = dict(enumerate(row)); f.update(zip(private, colors))
        if all(f[a] != f[b] for a,b in relevant):
            output.append(f)
    return output


def positive_controls():
    source = json.loads(CONTROL.read_text())
    records = []
    for original in source['records']:
        graph = original['graph']; edges = set(map(tuple, graph['all_edges']))
        private = sorted(set(v for e in edges for v in e) - B)
        degrees = {v: sum(v in e for e in edges) for v in private}
        assert min(degrees.values()) >= 4 and sum(d-4 for d in degrees.values()) == 2
        assert connected(private, edges)
        assert {b for a,b in edges if a in private and b in B} | {
            a for a,b in edges if b in private and a in B} == B
        roots = sorted(v for v,d in degrees.items() if d > 4)
        all_rows = [literal_colorings(private, edges, row) for row in ROWS]
        sigma = sum(1 << i for i, fs in enumerate(all_rows) if fs)
        assert sigma == graph['sigma_mask'] and all(all_rows[i] for i in ACCEPT)
        assert not all(not all_rows[i] for i in REJECT)
        data = dict(source_pointer=original['pointer'], complete_sigma=sigma,
                    original_private_order=private, original_degrees=degrees, original_roots=roots,
                    common_degree_connected_full_B_support_spoke_bounds_passed=True,
                    triple_rejection_premise=False, unique_degree6_interface_checks=[])
        assert all(sum((v,b) in edges or (b,v) in edges for b in B) <= 3 for v in private)
        if len(roots) == 1:
            r = roots[0]; pieces = components(set(private)-{r}, edges)
            assert len(pieces) <= 2
            spokes = sorted(b for b in B if tuple(sorted((r,b))) in edges)
            assert len(spokes) <= 3
            piece_rows = []
            for piece in pieces:
                contacts = sorted(v for v in piece if tuple(sorted((r,v))) in edges)
                support = sorted(b for b in B if any(tuple(sorted((v,b))) in edges for v in piece))
                rows = []
                for i, row in enumerate(ROWS):
                    fs = literal_colorings(piece, edges, row)
                    assert fs
                    relation = sorted({tuple(f[v] for v in contacts) for f in fs})
                    forbidden = sorted(set.intersection(*(set(t) for t in relation)))
                    cap = {1:1,2:2,3:1,4:2,5:2}.get(len(contacts), len(contacts))
                    assert len(forbidden) <= cap
                    rows.append(dict(row_index=i, complete_ordered_relation=relation,
                        ordered_tuple_witnesses=[next([f[v] for v in sorted(B)+piece]
                                                     for f in fs if tuple(f[v] for v in contacts) == t)
                                                for t in relation], forbidden=forbidden))
                adjacent = len(contacts) == 2 and tuple(contacts) in edges
                pair_D = [i for i,d in enumerate(rows) if i in SINGLETON and len(d['forbidden'])==2 and 3 in d['forbidden']]
                if adjacent and pair_D:
                    assert all(not (len(rows[i]['forbidden']) == 1 and 3 not in rows[i]['forbidden']) for i in SINGLETON)
                piece_rows.append(rows)
                data['unique_degree6_interface_checks'].append(dict(
                    original_piece=piece, original_contact_order=contacts, actual_support=support,
                    actual_boundary_attachments=[[v, sorted(b for b in B if tuple(sorted((v,b))) in edges)] for v in piece],
                    forbidden_capacity=cap, nonempty_relation_and_capacity_passed=True,
                    single_original_edge_D_carrier_applicable=bool(adjacent and pair_D),
                    pair_D_reference_rows=pair_D, rows=rows))
            for i,row in enumerate(ROWS):
                exact = sorted((a,)+tuple(c for tup in tuples for c in tup)
                               for a in COLORS for tuples in product(*(d[i]['complete_ordered_relation'] for d in piece_rows))
                               if a not in {row[b] for b in spokes} | {c for tup in tuples for c in tup})
                contact_order = [r]+[v for d in data['unique_degree6_interface_checks'] for v in d['original_contact_order']]
                direct = sorted({tuple(f[v] for v in contact_order) for f in all_rows[i]})
                assert exact == direct
        records.append(data)
    assert [r['complete_sigma'] for r in records] == [951,935]
    return dict(input_sha256=sha256(CONTROL.read_bytes()).hexdigest(), records=records,
                common_lemmas_exclude_no_positive_control=True,
                full_literal_join_preserves_original_contacts=True)


def build():
    groups, weak, ternary = finite_interfaces()
    summary = {key: dict(named_geometries=len(rows), remaining=0,
                         search_nodes=sum(r['search_counts']['search_nodes'] for r in rows))
               for key, rows in groups.items()}
    summary['t2_(2,2)']['weaker_abstract_controls'] = len(weak)
    summary['t3_(3)'] = dict(named_spoke_sets=len(ternary), remaining=0)
    return dict(schema=1, scope='unique degree-six E3 under T4 plus rejected singleton positions 0,1,3',
                pattern_order=ROWS, singleton_position_by_row=SINGLETON,
                required_accepted_row_indices=sorted(ACCEPT), required_rejected_row_indices=sorted(REJECT),
                unspecified_three_color_row_indices=[0,3], no_exact_Sigma_mask=True,
                degree_partition='one degree-six root; all other effective interior vertices degree-four',
                finite_interfaces=groups, t3_ternary=ternary,
                pre_carrier_weaker_abstract_controls=weak,
                carrier_edge_controls=carrier_edge_controls(), positive_controls=positive_controls(),
                evidence_boundary='Paper Gallai, actual-degree-four core classification and same-embedding topology supply arbitrary-size coverage. Python only checks these finite necessary interfaces and controls.',
                external_theorem='Dvorak List coloring and Gallai trees Lemma 7 / Theorem 10, https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf; not a Python or Lean theorem',
                no_four_colour_oracle=True, new_Lean_theorem=False, summary=summary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = build(); payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.check:
        assert OUT.read_bytes() == payload.encode(), f'certificate differs: {OUT}'
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open('x') as stream:
            stream.write(payload)
    print(json.dumps(result['summary'], sort_keys=True))


if __name__ == '__main__':
    main()
