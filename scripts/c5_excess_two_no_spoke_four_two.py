#!/usr/bin/env python3
"""t=0, original (4,2): fixed cyclic supports and original binary path bags.

Exhausts a finite necessary profile domain, not source graphs. The arbitrary
size structural and disk arguments belong to the accompanying paper report.
Every relation uses four named C contacts and two named A contacts in one frame.
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
from c5_excess_two_ternary_binary import path_evidence

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/c5_excess_two_no_spoke_four_two/observations.json'
COLORS = tuple(range(4))
PERMS = tuple(permutations(COLORS))
TARGETS = tuple(sorted(set(orbit(933) + orbit(941))))
FRAME = frozenset(range(5))
FRAME_EDGES = frozenset(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
CANONICAL = (((0, 1, 2), (2, 3, 4)),
             ((0, 1, 2), (3, 4, 0)),
             ((0, 1, 2), (2, 3, 4, 0)),
             ((0, 1, 2, 3), (3, 4, 0)))


def packed(value):
    return json.dumps(value, separators=(',', ':'), sort_keys=True).encode()


def update_digest(digest, value):
    digest.update(packed(value) + b'\n')


def connected(vertices, edges):
    if not vertices:
        return False
    reached = {min(vertices)}
    while True:
        more = reached | {a for a, b in edges if b in reached and a in vertices} | {
            b for a, b in edges if a in reached and b in vertices}
        if more == reached:
            return reached == set(vertices)
        reached = more


def partition_controls():
    """Two independent constructions of all ten connected frame bipartitions."""
    by_vertices = set()
    for size in range(1, 5):
        for raw in combinations(range(5), size):
            left = frozenset(raw)
            if 0 in left and connected(left, FRAME_EDGES) and connected(FRAME - left, FRAME_EDGES):
                by_vertices.add(left)
    by_cuts = set()
    for deleted in combinations(sorted(FRAME_EDGES), 2):
        edges = FRAME_EDGES - set(deleted)
        left = {0}
        while True:
            more = left | {a for a, b in edges if b in left} | {b for a, b in edges if a in left}
            if more == left:
                break
            left = more
        by_cuts.add(frozenset(left))
    assert by_vertices == by_cuts and len(by_vertices) == 10
    return [[sorted(left), sorted(FRAME - left)] for left in
            sorted(by_vertices, key=lambda t: tuple(sorted(t)))]


@lru_cache(None)
def verified_path_evidence(envelope, external, queries):
    """Independently inspect every subset and all 24 color permutations."""
    assert queries and all(len(f) == 2 for _, f in queries)
    evidence = path_evidence(envelope, external, queries)
    family = []
    examined = 0
    for size in range(len(envelope) + 1):
        for raw in combinations(sorted(envelope), size):
            examined += 1
            local = all({p[c] for c in f} == set(f)
                        for i, f in queries for p in PERMS
                        if all(p[ROWS[i][v]] == ROWS[i][v] for v in raw))
            cross = all({p[c] for c in f} == set(g)
                        for (i, f), (j, g) in combinations(queries, 2) for p in PERMS
                        if all(p[ROWS[i][v]] == ROWS[j][v] for v in raw))
            if local and cross:
                family.append(raw)
    family.sort()
    assert family == evidence['admissible_actual_bag_supports']
    assert family and evidence['exclusion'] == 'common_two_frame_arcs_K5'
    arcs = evidence['frame_partition']
    left, right = map(set, arcs)
    assert left | right == FRAME and not left & right
    assert connected(left, FRAME_EDGES) and connected(right, FRAME_EDGES)
    assert any((a in left) != (b in left) for a, b in FRAME_EDGES)
    assert set(external) & left and set(external) & right
    assert all(set(t) & left and set(t) & right for t in family)
    # Every external anchor is an actual endpoint of the four-contact support;
    # no root-boundary spoke or envelope-interior attachment is introduced.
    return dict(evidence, independent_subset_checks=examined,
                independent_color_permutations=24,
                external_attachment_mode='other_original_four_contact_component',
                external_landings=[min(set(external) & arc) for arc in (left, right)],
                branch_set_recipe=dict(
                    A='one complete original binary path bag and intermediate path',
                    A_prime='a second complete original binary path bag',
                    Z='r, remaining binary path ends, and entire original C4',
                    X=arcs[0], Y=arcs[1]))


def profile_domain(envelopes):
    maps, options = {}, {}
    for component, envelope in enumerate(envelopes):
        representatives = {}
        for i, row in enumerate(ROWS):
            values = tuple(row[v] for v in envelope)
            key = component, normalize(values)
            if key not in representatives:
                representatives[key] = values
                choices = invariant_sets(set(values), 2)
                # Direct stabilizer definition, independent of invariant_sets.
                direct = [f for size in range(3) for f in combinations(COLORS, size)
                          if all({p[c] for c in f} == set(f) for p in PERMS
                                 if all(p[c] == c for c in set(values)))]
                assert choices == direct
                options[key] = choices
            base = representatives[key]
            for forbidden in options[key]:
                moved = transport(base, values, forbidden)
                direct = {tuple(sorted(p[c] for c in forbidden)) for p in PERMS
                          if all(p[a] == b for a, b in zip(base, values))}
                assert direct == {moved}
            maps[component, i] = key, base, values
    records = [dict(component=key[0], equality_pattern=key[1],
                    forbidden_options=options[key]) for key in sorted(options)]
    return maps, options, records


def solve(envelopes, target, maps, options):
    row_choices = []
    for i in range(10):
        data = [maps[c, i] for c in range(2)]
        choices = []
        for indexes in product(*(range(len(options[d[0]])) for d in data)):
            forbidden = tuple(transport(d[1], d[2], options[d[0]][j])
                              for d, j in zip(data, indexes, strict=True))
            if bool(U - set().union(*map(set, forbidden))) != bool(target >> i & 1):
                continue
            assignment = dict((d[0], j) for d, j in zip(data, indexes, strict=True))
            choices.append((assignment, forbidden))
        row_choices.append(choices)
    order = sorted(range(10), key=lambda i: len(row_choices[i]))
    rejected = tuple(i for i in range(10) if not target >> i & 1)
    assert len(rejected) in (3, 4)
    external = tuple(sorted({envelopes[0][0], envelopes[0][-1]}))
    chosen, counts, certificates, d_patterns = {}, Counter(), {}, Counter()
    profile_digest, choice_digest = sha256(), sha256()
    for row in row_choices:
        for assignment, forbidden in row:
            update_digest(choice_digest, [sorted(assignment.items()), forbidden])

    def dfs(position, assignment):
        counts['search_nodes'] += 1
        if position == 10:
            profile = tuple(chosen[i] for i in range(10))
            counts['complete_weak_profiles'] += 1
            update_digest(profile_digest, profile)
            assert all(len(profile[i][0]) == len(profile[i][1]) == 2 and
                       set(profile[i][0]).isdisjoint(profile[i][1]) for i in rejected)
            queries = tuple((i, profile[i][1]) for i in rejected)
            evidence = verified_path_evidence(envelopes[1], external, queries)
            counts[evidence['exclusion']] += 1
            d_patterns[tuple(3 in profile[i][0] for i in rejected)] += 1
            if queries not in certificates:
                certificates[queries] = dict(evidence=evidence, multiplicity=0,
                    representative_complete_ten_row_forbidden=profile, digest=sha256())
            certificate = certificates[queries]
            certificate['multiplicity'] += 1
            update_digest(certificate['digest'], profile)
            return
        i = order[position]
        for extension, forbidden in row_choices[i]:
            if any(k in assignment and assignment[k] != v for k, v in extension.items()):
                counts['same_original_local_profile_conflicts'] += 1
                continue
            chosen[i] = forbidden
            dfs(position + 1, assignment | extension)
            del chosen[i]

    dfs(0, {})
    records = []
    for queries, certificate in sorted(certificates.items()):
        records.append(dict(rejected_row_binary_pairs=queries,
            path_bag_evidence=certificate['evidence'],
            weak_profile_multiplicity=certificate['multiplicity'],
            complete_weak_profiles_sha256=certificate['digest'].hexdigest()))
    assert sum(c['weak_profile_multiplicity'] for c in records) == counts['complete_weak_profiles']
    if records:
        assert len(records) == 8 and all(c['weak_profile_multiplicity'] == 45 for c in records)
    return dict(target=target, rejected_rows=rejected,
        row_candidate_counts=list(map(len, row_choices)), row_search_order=order,
        exact_literal_row_choices_sha256=choice_digest.hexdigest(),
        complete_weak_profiles_sha256=profile_digest.hexdigest(),
        representative_complete_ten_row_forbidden=(certificates[min(certificates)][
            'representative_complete_ten_row_forbidden'] if certificates else None),
        search_counts=dict(sorted(counts.items())), path_certificates=records,
        four_contact_D_membership_controls=[dict(rejected_row_membership=pattern, count=count)
            for pattern, count in sorted(d_patterns.items())],
        remaining_profiles=0)


def source_controls():
    geometry, queries = [], []
    for shape, canonical in enumerate(CANONICAL):
        for rotation in range(5):
            envelopes = tuple(tuple((v + rotation) % 5 for v in envelope)
                              for envelope in canonical)
            maps, options, domains = profile_domain(envelopes)
            gid = len(geometry)
            geometry.append(dict(id=gid, canonical_shape=shape, rotation=rotation,
                original_component_order=['original_C4', 'original_A2'],
                cyclic_envelopes=envelopes, support_spans=[len(e) - 1 for e in envelopes],
                actual_external_anchors=sorted({envelopes[0][0], envelopes[0][-1]}),
                local_profile_domains=domains))
            for target in TARGETS:
                queries.append(dict(geometry_id=gid, **solve(envelopes, target, maps, options)))
    assert len(geometry) == 20 and len(queries) == 200
    # Independent geometric definition: all directed cyclic arcs, then retain
    # exactly the pairs whose open original frame-edge sets are disjoint.
    arcs = [tuple((start + j) % 5 for j in range(span + 1))
            for start in range(5) for span in (2, 3)]
    arc_edges = lambda arc: {tuple(sorted(e)) for e in zip(arc, arc[1:])}
    independent = {(c, a) for c, a in product(arcs, repeat=2)
                   if not arc_edges(c) & arc_edges(a)}
    assert independent == {tuple(record['cyclic_envelopes']) for record in geometry}
    assert len(independent) == 20
    weaker = [q for q in queries if q['search_counts'].get('complete_weak_profiles')]
    assert len(weaker) == 20
    assert all(q['search_counts']['complete_weak_profiles'] == 360 for q in weaker)
    return dict(original_component_order=['original_C4', 'original_A2'],
        original_contact_order=['C_x0', 'C_x1', 'C_x2', 'C_x3', 'A_u', 'A_v'],
        canonical_geometry=CANONICAL,
        geometry_completeness='Rotate the first actual C4 envelope endpoint to b0. '
            'Both spans are at least two and total at most five; the residual '
            'cyclic gap is zero or one, giving these four named canonical shapes.',
        envelope_endpoint_rule='Endpoints are actual same-source attachments; '
            'envelope interiors only permit attachment positions.',
        root_boundary_spokes=[], target_orbits={str(m): orbit(m) for m in (933, 941)},
        independent_edge_disjoint_geometry_count=len(independent),
        geometry=geometry, queries=queries,
        scope='Over-approximate same-source necessary profiles; representatives '
            'are negative controls, not graph or disk realizations.')


def forbidden(relation):
    assert relation
    return set.intersection(*(set(t) for t in relation))


def relation_controls():
    quads = tuple(product(COLORS, repeat=4))
    pairs = tuple(product(COLORS, repeat=2))
    operator = tuple(t for t in product(COLORS, repeat=7) if t[0] not in t[1:])
    fibers = {(p, q): [] for p, q in product(quads, pairs)}
    for t in operator:
        fibers[t[1:5], t[5:]].append(t)
    singleton_digest, singleton_count, occupied = sha256(), 0, 0
    for p, q in product(quads, pairs):
        direct = tuple((a,) + p + q for a in COLORS if a not in p + q)
        assert tuple(fibers[p, q]) == direct
        update_digest(singleton_digest, [p, q, direct])
        singleton_count += 1
        occupied += bool(direct)
    assert singleton_count == 256 * 16

    quad_relations = set()
    for size in range(5):
        for colors in combinations(COLORS, size):
            if colors:
                quad_relations.add((colors + (colors[-1],) * (4 - size),))
            else:
                quad_relations.add(((0, 0, 0, 0), (1, 1, 1, 1)))
    for a, b in combinations(COLORS, 2):
        quad_relations.add(((a, b, a, b), (b, a, b, a)))
        quad_relations.add(((a, a, a, a), (b, b, b, b)))
    for a, b in permutations(COLORS, 2):
        quad_relations.add(tuple(sorted(((a, a, a, a), (a, b, b, b)))))
    quad_relations.add(quads)
    quad_relations = tuple(sorted(quad_relations))
    pair_relations = tuple(sorted(set((p,) for p in pairs) |
                                 set(combinations(pairs, 2)) | {pairs}))
    assert {tuple(sorted(forbidden(r))) for r in quad_relations} == {
        f for size in range(5) for f in combinations(COLORS, size)}
    digest, checked = sha256(), 0
    for rc, ra in product(quad_relations, pair_relations):
        joined = tuple(sorted(t for p, q in product(rc, ra) for t in fibers[p, q]))
        direct = tuple(sorted((a,) + p + q for a, p, q in product(COLORS, rc, ra)
                              if a not in p + q))
        assert joined == direct
        assert {t[0] for t in joined} == U - forbidden(rc) - forbidden(ra)
        update_digest(digest, [rc, ra, joined])
        checked += 1

    r1 = ((0, 1, 0, 1), (1, 0, 1, 0))
    r2 = ((0, 0, 0, 0), (1, 1, 1, 1))
    binary = ((2, 2), (3, 3))
    margins = lambda relation: [sorted({t[i] for t in relation}) for i in range(4)]
    assert margins(r1) == margins(r2)
    j1 = tuple(sorted(t for p, q in product(r1, binary) for t in fibers[p, q]))
    j2 = tuple(sorted(t for p, q in product(r2, binary) for t in fibers[p, q]))
    assert {t[0] for t in j1} == {2, 3}
    assert {t[0] for t in j2} == U
    return dict(port_order=['r', 'C_x0', 'C_x1', 'C_x2', 'C_x3', 'A_u', 'A_v'],
        ordered_quadruple_count=256, ordered_pair_count=16,
        full_seven_port_operator_size=len(operator), singleton_fiber_checks=singleton_count,
        occupied_singleton_fibers=occupied,
        complete_singleton_fibers_sha256=singleton_digest.hexdigest(),
        chosen_complete_quad_relations=quad_relations,
        chosen_complete_binary_relations=pair_relations,
        chosen_full_relation_pair_checks=checked, complete_join_sha256=digest.hexdigest(),
        marginal_collision=dict(C_relation_1=r1, C_relation_2=r2,
            common_C_contact_marginals=margins(r1), same_A_relation=binary,
            C_forbidden_1=sorted(forbidden(r1)), C_forbidden_2=sorted(forbidden(r2)),
            complete_join_1=j1, complete_join_2=j2,
            root_projection_1=[2, 3], root_projection_2=sorted(U)),
        arbitrary_relation_coverage='Any nonempty ordered C4/A2 relations join '
            'as the union of their singleton fibers in this one literal frame.',
        scope='Abstract complete relations, not source realizations.')


def build():
    partitions = partition_controls()
    source, relations = source_controls(), relation_controls()
    counts = Counter()
    for query in source['queries']:
        counts.update(query['search_counts'])
    assert counts['complete_weak_profiles'] == counts['common_two_frame_arcs_K5'] == 7200
    names = ('c5_independent_support_capacity', 'c5_excess_two_three_unary',
             'c5_excess_two_binary_three_unary', 'c5_excess_two_ternary_binary',
             'c5_single_spoke_frame_arc', 'c5_single_spoke_cross_row',
             'c5_single_spoke_two_arc', 'c5_single_spoke_two_two_minor')
    paths = [Path(__file__).resolve()] + [ROOT / 'scripts' / (name + '.py') for name in names]
    return dict(schema=1, scope='t=0 original (4,2) whole-source exclusion, '
        'conditional on the paper structural and same-embedding support lemmas',
        source_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
        pattern_order=ROWS, source_controls=source, independent_frame_partitions=partitions,
        complete_relation_controls=relations,
        paper_dependencies=['original component slack and complete ordered six-contact gluing',
            'fixed-Sigma edge-minimal private-factor witnesses and short-support lemma',
            'same-source circular support envelopes with spans at least two and sum at most five',
            'original external root-to-boundary paths through the other component',
            'four-contact capacity at most two and original binary pair path-bag identity',
            'same original binary path bags and common two-frame-arc K5'],
        summary=dict(named_cyclic_placements=20, target_queries=200,
            queries_without_weak_profiles=180, queries_with_weak_profiles=20,
            complete_weak_profiles=7200, exact_rejected_pair_schemas=160,
            path_bag_excluded_profiles=7200, remaining_profiles=0,
            singleton_seven_port_fibers=relations['singleton_fiber_checks'],
            full_relation_pair_checks=relations['chosen_full_relation_pair_checks'],
            independent_frame_partitions=len(partitions), graph_enumeration=False,
            disk_realizability_claimed=False, new_lean_theorem=False))


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
