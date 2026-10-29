#!/usr/bin/env python3
"""Small exact controls for literal continuation signatures and transport.

This is an independent relation prototype, not a production solver option.
Every boundary tuple is explicitly enumerated; no speed claim is made.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

COLORS = tuple(range(4))


@dataclass(frozen=True)
class Factor:
    scope: tuple[str, ...]
    rows: frozenset[tuple[int, ...]]

    def accepts(self, assignment):
        return tuple(assignment[v] for v in self.scope) in self.rows


def edge(a, b):
    return Factor((a, b), frozenset((x, y) for x in COLORS for y in COLORS if x != y))


def assignments(vertices, domains):
    for row in product(*(domains[v] for v in vertices)):
        yield dict(zip(vertices, row))


def extensions(boundary, future, domains, factors):
    return frozenset(tuple(a[v] for v in future)
                     for a in assignments(future, domains)
                     if all(f.accepts(boundary | a) for f in factors))


def signature(boundary, domains, factors, local_possible=True):
    """Complete factor restrictions, normalized by known future domains.

    Factor identity/order is fixed within this context. Production use would
    also need every factor identity, revision, scope and domain revision.
    """
    if not local_possible:
        return (False,)
    result = []
    for factor in factors:
        residual_scope = tuple(v for v in factor.scope if v not in boundary)
        residual_rows = frozenset(
            tuple(row[i] for i, v in enumerate(factor.scope) if v not in boundary)
            for row in factor.rows
            if all(row[i] == boundary[v] if v in boundary else row[i] in domains[v]
                   for i, v in enumerate(factor.scope))
        )
        result.append((residual_scope, tuple(sorted(residual_rows))))
    return (True, tuple(result))


def groups(values, key):
    classes = {}
    for value in values:
        classes.setdefault(key(value), []).append(value)
    return list(classes.values())


def edge_context_signature(boundary, future, domains, edges):
    """Exact exterior domain restriction signature for original-edge CSPs.

    The future graph and literal coordinate order are fixed. Interface values
    are retained separately; this signature only memoizes exterior problems.
    """
    blocked = {v: set() for v in future}
    for a, b in edges:
        if a in boundary and b in boundary:
            if boundary[a] == boundary[b]:
                return (False,)
        elif a in boundary and b in blocked:
            blocked[b].add(boundary[a])
        elif b in boundary and a in blocked:
            blocked[a].add(boundary[b])
    return (True, tuple((v, tuple(c for c in domains[v] if c not in blocked[v]))
                        for v in future))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('output must be new')

    # A local s-x edge permits every s. Its local S4 symmetry says nothing
    # about the literal outer continuation s-t with t fixed to zero.
    fixed_domains = {'s': COLORS, 't': (0,)}
    outer = (edge('s', 't'),)
    e_fixed = {s: extensions({'s': s}, ('t',), fixed_domains, outer) for s in COLORS}
    keys = {s: signature({'s': s}, fixed_domains, outer) for s in COLORS}
    assert e_fixed[0] == frozenset() and all(e_fixed[s] == {(0,)} for s in (1, 2, 3))
    assert groups(list(COLORS), lambda s: keys[s]) == [[0], [1, 2, 3]]
    for s, t in product(COLORS, repeat=2):
        if keys[s] == keys[t]:
            assert e_fixed[s] == e_fixed[t]

    # Equal future relations do not imply equal private fibres.
    fibre1 = frozenset(x for x in COLORS if x != 1)
    fibre2 = frozenset(x for x in COLORS if x != 2)
    assert fibre1 != fibre2 and 2 in fibre1 and 2 not in fibre2
    swap12 = (0, 2, 1, 3)
    assert frozenset(swap12[x] for x in fibre1) == fibre2
    assert swap12[0] == 0  # The fixed outer colour is preserved.

    # Even a common valid global permutation gives covariance, rather than
    # equality of literal continuation relations on future vertices.
    free_domains = {'s': COLORS, 't': COLORS}
    e_free = {s: extensions({'s': s}, ('t',), free_domains, outer) for s in COLORS}
    swap01 = (1, 0, 2, 3)
    transported = frozenset(tuple(swap01[c] for c in row) for row in e_free[0])
    assert transported == e_free[1] and e_free[0] != e_free[1]

    # No nontrivial equivalence survives every possible future fixed-colour
    # edge context: t fixed to s distinguishes every pair s != t.
    distinguished = []
    for first, second in combinations(COLORS, 2):
        domain = {'s': COLORS, 't': (first,)}
        left = extensions({'s': first}, ('t',), domain, outer)
        right = extensions({'s': second}, ('t',), domain, outer)
        assert not left and right
        distinguished.append([first, second])

    # Four ordered interface coordinates all meet one exterior vertex. The
    # exterior sees their used-colour set, not the ordered tuple. Keep every
    # original tuple as a separate lift label while memoizing its exterior.
    boundary_vertices = ('s0', 's1', 's2', 's3')
    future = ('u',)
    crossing = tuple((s, 'u') for s in boundary_vertices)
    star_outer = tuple(edge(s, 'u') for s in boundary_vertices)
    star_domains = {v: COLORS for v in (*boundary_vertices, *future)}
    sigma_rows = list(product(COLORS, repeat=len(boundary_vertices)))
    exterior_cache = {}
    lifted_rows = set()
    direct_rows = set()
    members = {}
    for row in sigma_rows:
        sigma = dict(zip(boundary_vertices, row))
        key = edge_context_signature(sigma, future, star_domains, crossing)
        exact = extensions(sigma, future, star_domains, star_outer)
        if key in exterior_cache:
            assert exterior_cache[key] == exact
        else:
            exterior_cache[key] = exact
        members.setdefault(key, []).append(row)
        direct_rows.update(row + tail for tail in exact)
    for key, labels in members.items():
        lifted_rows.update(row + tail for row in labels for tail in exterior_cache[key])
    assert len(exterior_cache) == 15  # All nonempty used-colour subsets.
    assert lifted_rows == direct_rows and len(direct_rows) == 324
    two_rows = ((0, 0, 1, 1), (0, 1, 0, 1))
    two_sigma = [dict(zip(boundary_vertices, row)) for row in two_rows]
    assert edge_context_signature(two_sigma[0], future, star_domains, crossing) == \
        edge_context_signature(two_sigma[1], future, star_domains, crossing)
    assert not any(tuple(perm[c] for c in two_rows[0]) == two_rows[1]
                   for perm in permutations(COLORS))

    # Truly separated active factor components factorize their full relation.
    domains = {'a': COLORS, 'b': COLORS, 'x': (0,), 'y': (1,)}
    separated = (edge('a', 'x'), edge('b', 'y'))
    relation = frozenset((a, b) for a, b in product(COLORS, repeat=2)
                         if extensions({'a': a, 'b': b}, ('x', 'y'), domains, separated))
    product_relation = frozenset(product((1, 2, 3), (0, 2, 3)))
    assert relation == product_relation
    # A live cross-scope relation invalidates the product, regardless of an
    # older partition plan. This equality can arise by eliminating the centre
    # of a two-colour a-z-b path, with all three domains {2,3}.
    equality = Factor(('a', 'b'), frozenset({(2, 2), (3, 3)}))
    coupled = frozenset(row for row in relation if row in equality.rows)
    pa = {row[0] for row in coupled}
    pb = {row[1] for row in coupled}
    assert len(coupled) == 2 and len(frozenset(product(pa, pb))) == 4

    # Width and support mass do not determine first-success query work.
    # The two singleton supports are realized by one boundary s adjacent to
    # three fixed-colour internal neighbours, in the same original star.
    def star_support(blocked):
        return frozenset(c for c in COLORS if c not in blocked)

    def first_success(support, width):
        ordered = list(product(COLORS, repeat=width))
        asked = ordered[:next(i + 1 for i, row in enumerate(ordered) if row in support)]
        return {'width': width, 'support_rows': len(support), 'queries': len(asked),
                'colour_payload_query_plus_reply': 2 * width * len(asked)}

    assert star_support((0, 1, 2)) == {3} and star_support((1, 2, 3)) == {0}
    last_singleton = first_success({(3,)}, 1)
    first_singleton = first_success({(0,)}, 1)
    wide_easy = first_success(set(product(COLORS, repeat=2)), 2)
    assert last_singleton['queries'] == 4 and first_singleton['queries'] == 1
    assert last_singleton['colour_payload_query_plus_reply'] > wide_easy['colour_payload_query_plus_reply']

    report = {
        'scope': 'independent exact finite controls; not a production solver or speed benchmark',
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'context_signature': {
            'literal_future_extensions': {str(s): sorted(e_fixed[s]) for s in COLORS},
            'signature_classes': groups(list(COLORS), lambda s: keys[s]),
            'all_equal_signature_pairs_have_equal_complete_future_relation': True,
            'signature_uses_known_domains': True,
            'private_fibres_still_differ': [sorted(fibre1), sorted(fibre2)],
            'blind_private_witness_reuse_fails': {'source_boundary': 1, 'target_boundary': 2,
                                                 'cached_x': 2, 'transported_x': swap12[2]},
        },
        'global_symmetry': {'literal_future_relations_equal': False,
                            'full_future_transport_is_exact': True,
                            'local_symmetry_alone_may_break_outer_fixed_colour': True},
        'all_possible_contexts': {'pairwise_distinguishing_edge_contexts': distinguished,
                                  'nontrivial_universal_literal_quotient': False},
        'original_edge_exterior_signature': {
            'ordered_interface_tuples': len(sigma_rows),
            'different_complete_exterior_subproblems': len(exterior_cache),
            'lifted_original_colourings': len(lifted_rows),
            'direct_original_colourings': len(direct_rows),
            'all_exterior_relations_equal_within_each_signature': True,
            'every_original_ordered_interface_label_preserved': True,
            'same_signature_example': [list(sigma.values()) for sigma in two_sigma],
            'same_signature_example_not_in_one_common_colour_permutation_orbit': True,
            'not_valid_as_a_key_for_the_interior_relation': True,
        },
        'active_factor_separation': {'separated_relation_rows': len(relation),
                                     'complete_cartesian_factorization_verified': True,
                                     'after_cross_factor_complete_rows': len(coupled),
                                     'unary_marginal_product_rows': len(pa) * len(pb)},
        'query_cost_controls': {'narrow_singleton_last': last_singleton,
                                'narrow_singleton_first': first_singleton,
                                'wider_full_first': wide_easy,
                                'same_query_repeated_100_times': {
                                    'width': 1, 'unique_queries': 1, 'queries': 100,
                                    'colour_payload_query_plus_reply': 200}},
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x') as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
        stream.write('\n')
    print(json.dumps({'written': str(args.out), 'all_assertions_passed': True}, sort_keys=True))


if __name__ == '__main__':
    main()
