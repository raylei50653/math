#!/usr/bin/env python3
"""Exact cyclic-order distances and a permissive four-star label obstruction.

Failure of permissive pseudo-tightness is a necessary excess certificate.
Success is not a drawing or a tightness certificate. Standard library only.
"""
from __future__ import annotations

import argparse
from collections import deque
from functools import lru_cache
from itertools import combinations, permutations
import json
from math import comb
from pathlib import Path


def canonical(order):
    order = tuple(order)
    i = order.index(0)
    return order[i:] + order[:i]


class CyclicOrders:
    def __init__(self, m):
        if m < 3:
            raise ValueError("m must be at least three")
        self.m = m
        self.orders = [(0,) + t for t in permutations(range(1, m))]
        self.index = {r: i for i, r in enumerate(self.orders)}
        self.labels = list(combinations(range(m), 2))
        label_index = {p: i for i, p in enumerate(self.labels)}
        self.reverse = [self.index[canonical(r[::-1])] for r in self.orders]
        self.edges = []
        for r in self.orders:
            row = []
            for j in range(m):
                k = (j + 1) % m
                s = list(r)
                s[j], s[k] = s[k], s[j]
                bit = 1 << label_index[tuple(sorted((r[j], r[k]))) ]
                row.append((self.index[canonical(s)], bit))
            self.edges.append(row)

    @lru_cache(maxsize=None)
    def distances(self, target):
        dist = [-1] * len(self.orders)
        dist[target] = 0
        queue = deque([target])
        while queue:
            v = queue.popleft()
            for w, _ in self.edges[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    queue.append(w)
        return tuple(dist)

    @lru_cache(maxsize=None)
    def shortest_summary(self, source, target):
        """Distance, labels in every / in some shortest path, without sampling."""
        dist = self.distances(target)

        @lru_cache(maxsize=None)
        def visit(v):
            if v == target:
                return 0, 0
            must = (1 << len(self.labels)) - 1
            may = 0
            for w, bit in self.edges[v]:
                if dist[w] == dist[v] - 1:
                    child_must, child_may = visit(w)
                    must &= bit | child_must
                    may |= bit | child_may
            return must, may

        must, may = visit(source)
        return dist[source], must, may

    def antipath_summary(self, r, s):
        return self.shortest_summary(self.index[canonical(r)],
                                     self.reverse[self.index[canonical(s)]])

    def decode(self, mask):
        return [list(p) for i, p in enumerate(self.labels) if mask >> i & 1]


def permissive_pair_relation(co, must, may):
    """All endpoint pairs admitting a walk with must subset support subset may.

    Walks may repeat vertices and labels. This relaxation contains every
    Woodall antipath. Within each allowed connected component a walk can visit
    every allowed edge, so its union of edge labels decides the must condition.
    """
    component = [-1] * len(co.orders)
    unions = []
    for start in range(len(co.orders)):
        if component[start] >= 0:
            continue
        ci = len(unions)
        component[start] = ci
        stack, union = [start], 0
        while stack:
            v = stack.pop()
            for w, bit in co.edges[v]:
                if bit & may:
                    union |= bit
                    if component[w] < 0:
                        component[w] = ci
                        stack.append(w)
        unions.append(union)
    return tuple(tuple(component[s] == component[co.reverse[t]]
                       and (must & ~unions[component[s]]) == 0
                       for t in range(len(co.orders)))
                 for s in range(len(co.orders)))


def four_star_obstruction(co, rotations):
    """Exact UNSAT check for a deliberately permissive pseudo-tight model."""
    if co.m % 2 == 0:
        raise ValueError("even degree does not provide integer excess units")
    if len(rotations) != 4:
        raise ValueError("exactly four labelled star rotations required")
    small = CyclicOrders(4)
    mandatory = [0] * len(co.labels)
    possible = [0] * len(co.labels)
    antisum = 0
    pair_summaries = []
    for k, (u, v) in enumerate(small.labels):
        distance, must, may = co.antipath_summary(rotations[u], rotations[v])
        antisum += distance
        pair_summaries.append({"pair": [u, v], "delta": distance,
                               "mandatory": co.decode(must),
                               "possible": co.decode(may)})
        for j in range(len(co.labels)):
            if must >> j & 1:
                mandatory[j] |= 1 << k
            if may >> j & 1:
                possible[j] |= 1 << k
    relations = {p: permissive_pair_relation(small, must, may)
                 for p, must, may in zip(co.labels, mandatory, possible)}
    assignment = [-1] * co.m
    # All opposing rotations are free; fixing one would also relabel M.
    nodes = 0

    def search():
        nonlocal nodes
        nodes += 1
        if -1 not in assignment:
            return True
        choices = []
        for v in range(co.m):
            if assignment[v] >= 0:
                continue
            domain = []
            for candidate in range(len(small.orders)):
                good = True
                for u, value in enumerate(assignment):
                    if value < 0:
                        continue
                    p = tuple(sorted((u, v)))
                    a, b = (value, candidate) if u < v else (candidate, value)
                    if not relations[p][a][b]:
                        good = False
                        break
                if good:
                    domain.append(candidate)
            if not domain:
                return False
            choices.append((len(domain), v, domain))
        _, v, domain = min(choices)
        for candidate in domain:
            assignment[v] = candidate
            if search():
                return True
        assignment[v] = -1
        return False

    compatible = search()
    return {"rotations": [list(r) for r in rotations], "antisum": antisum,
            "permissive_label_compatible": compatible,
            "proved_non_pseudo_tight": not compatible,
            "necessary_excess_units": int(not compatible),
            "csp_nodes": nodes, "pair_summaries": pair_summaries,
            "opposite_rotations_if_compatible":
                [list(small.orders[x]) for x in assignment] if compatible else None}


def hitting_number(n, obstructions, allowed_pairs=None):
    """Exact pair cover lower bound; each supplied obstruction needs e_uv>=1.

    Caller owns evidence that each subset is an obstruction. This function
    does not establish it from a supplied index list.
    """
    pairs = list(combinations(range(n), 2))
    allowed = set(pairs if allowed_pairs is None else allowed_pairs)
    choices = [tuple(p for p in combinations(sorted(s), 2) if p in allowed)
               for s in obstructions]
    if any(not row for row in choices):
        return None, []
    covers = {p: sum(1 << i for i, row in enumerate(choices) if p in row)
              for p in pairs if p in allowed}

    @lru_cache(maxsize=None)
    def solve(remaining):
        if not remaining:
            return ()
        rows = [i for i in range(len(choices)) if remaining >> i & 1]
        i = min(rows, key=lambda j: len(choices[j]))
        best = None
        for p in choices[i]:
            suffix = solve(remaining & ~covers[p])
            candidate = (p,) + suffix
            if best is None or len(candidate) < len(best):
                best = candidate
        return best

    result = solve((1 << len(choices)) - 1)
    return len(result), [list(p) for p in result]


def check():
    co5 = CyclicOrders(5)
    co7 = CyclicOrders(7)
    graph_controls = []
    for co in (co5, co7):
        expected = (co.m // 2) * ((co.m - 1) // 2)
        # Vertex transitivity and label-preserving reversal are explicit.
        dist = co.distances(0)
        assert dist[co.reverse[0]] == expected
        assert max(dist) == expected
        assert sum(d == expected for d in dist) == 1
        assert all((dist[u] - dist[v]) % 2 for u, row in enumerate(co.edges)
                   for v, _ in row)
        graph_controls.append({"m": co.m, "vertices": len(co.orders),
                               "diameter_from_identity": max(dist),
                               "unique_antipode": True, "bipartite": True})
    # Frozen explicit obstruction; discovered in deterministic exploratory
    # sampling, replayed directly with every opposite rotation free.
    rotations = [tuple(map(int, word)) for word in
                 ("0123456", "0521364", "0643215", "0612543")]
    found = four_star_obstruction(co7, rotations)
    assert found["antisum"] == 21
    assert found["proved_non_pseudo_tight"]
    assert found["csp_nodes"] == 7
    found["crossing_lower_bound"] = found["antisum"] + 2
    # Independent augmented-state reachability checks the permissive relation.
    # All opposite rotations remain free, including the first one.
    small = CyclicOrders(4)
    bounds = [[0, 0] for _ in co7.labels]
    for k, (u, v) in enumerate(small.labels):
        _, must, may = co7.antipath_summary(rotations[u], rotations[v])
        for j in range(len(co7.labels)):
            bounds[j][0] |= ((must >> j) & 1) << k
            bounds[j][1] |= ((may >> j) & 1) << k
    relation_checks = 0
    for must, may in bounds:
        relation = permissive_pair_relation(small, must, may)
        for source in range(len(small.orders)):
            seen = {(source, 0)}
            queue = deque(seen)
            while queue:
                v, used = queue.popleft()
                for w, bit in small.edges[v]:
                    if not bit & may:
                        continue
                    state = w, used | (bit & must)
                    if state not in seen:
                        seen.add(state)
                        queue.append(state)
            for target in range(len(small.orders)):
                assert relation[source][target] == ((small.reverse[target], must) in seen)
                relation_checks += 1
    positive = four_star_obstruction(co5, [co5.orders[0]] * 4)
    assert positive["permissive_label_compatible"]
    # Cover aggregation can be strictly sharper than uniform counting.
    family = [list(range(4)), list(range(4, 8))]
    tau, cover = hitting_number(8, family)
    assert tau == 2
    assert (len(family) + comb(6, 2) - 1) // comb(6, 2) == 1
    return {"scope": "exact finite label obstruction, no drawing realization",
            "graphs": graph_controls,
            "independent_augmented_state_relation_checks": relation_checks,
            "four_star_obstruction": found,
            "positive_repeated_rotation_control": positive,
            "abstract_cover_control": {"n": 8, "subsets": family,
                "woodall_uniform_count_bound": 1, "pair_cover_number": tau,
                "minimum_cover": cover,
                "scope": "abstract family only, not sourced rotation obstructions"}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check()
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    print(payload, end="")
