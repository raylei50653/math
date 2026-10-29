#!/usr/bin/env python3
"""Exact finite-domain bucket projection with bounded factor subfamilies.

For an eliminated variable with q effective colors, a family of conditional
color sets has nonempty intersection exactly when every subfamily of size
min(q, m) does. The residual therefore may keep several smaller exact tables.
History recipes retain the entire old bucket and all historical supports.
This is an independent prototype; it does not change the production solver.
"""

from __future__ import annotations

from itertools import combinations, product
from math import comb

from four_color_lab import normalize_graph
from four_color_partial_history import (
    SCHEMA, _factor_predicate, compile_representation, fibre_choices,
    reconstruct_one,
)


COLORS = range(4)
METHODS = ("bounded", "full", "anchored")


class _WorkLimit(Exception):
    pass


def build_representation(graph, *, stop_after=None, order=None, max_checks=None,
                         method="bounded"):
    """Build an exact prefix and residual without assigning any live colors.

    ``candidate_checks`` counts construction work units: color trials (four
    trials to intersect unary bucket factors, then candidate colors considered
    for each projected row), plus complete table rows visited when measuring
    anchor caps. ``color_trials`` and ``cap_scan_rows`` report both separately.
    ``factor_lookups`` counts predicate calls (including short-circuit
    evaluation) plus table-row inspections for anchor caps. A work limit
    interrupts before the next charged trial or cap row; only a
    completely built family of projection tables is committed. Setup, Python
    operations, serialization, membership queries and final reconstruction are
    outside this construction budget.

    The serialized result uses the established partial-history recipe schema.
    Its compiler and reconstruction do not consult an original graph oracle.
    """
    graph = normalize_graph(graph)
    vertices = graph["vertices"]
    n = len(vertices)
    if stop_after is None:
        stop_after = n
    if type(stop_after) is not int or not 0 <= stop_after <= n:
        raise ValueError("stop_after must be an integer from zero to the vertex count")
    if method not in METHODS:
        raise ValueError("unknown projection method")
    if max_checks is not None and (type(max_checks) is not int or max_checks < 0):
        raise ValueError("max_checks must be a nonnegative integer or None")
    if order is None:
        order = vertices
    if (not isinstance(order, (list, tuple)) or any(type(v) is not int for v in order)
            or len(order) != n or set(order) != set(vertices)):
        raise ValueError("order must be a permutation of the original vertices")

    factors, predicates, active_ids, history, steps = {}, {}, [], [], []
    active = set(vertices)
    fixed = dict(graph["fixed"])

    def add_factor(factor):
        key = f"f{len(factors)}"
        factors[key] = factor
        predicates[key] = _factor_predicate(factor, set(vertices))
        return key

    for vertex in vertices:
        active_ids.append(add_factor(dict(kind="domain", scope=[vertex],
                                         colors=[fixed[vertex]] if vertex in fixed else list(COLORS))))
    for edge in graph["edges"]:
        active_ids.append(add_factor(dict(kind="neq", scope=edge)))

    checks = lookups = color_trials = cap_scan_rows = 0

    def charge():
        nonlocal checks
        if max_checks is not None and checks >= max_checks:
            raise _WorkLimit
        checks += 1

    def accepts(keys, assignment):
        nonlocal lookups, color_trials
        charge()
        color_trials += 1
        for key in keys:
            lookups += 1
            if not predicates[key](assignment):
                return False
        return True

    def support_cap(key, vertex, domain):
        """Uniform cap on this factor's conditional support in effective D."""
        nonlocal lookups, cap_scan_rows
        factor = factors[key]
        if factor["kind"] == "neq":
            return min(len(domain), 3)
        # Every non-unary factor produced by this prototype is neq or table.
        # Group literal complete rows; missing groups have empty support.
        index = factor["scope"].index(vertex)
        groups = {}
        for row in factor["rows"]:
            charge()
            cap_scan_rows += 1
            lookups += 1
            if row[index] in domain:
                boundary = tuple(row[:index] + row[index + 1:])
                groups.setdefault(boundary, set()).add(row[index])
        return max(map(len, groups.values()), default=0)

    stop_reason = "requested_prefix"
    for vertex in order[:stop_after]:
        bucket = [key for key in active_ids if vertex in factors[key]["scope"]]
        unary = [key for key in bucket if len(factors[key]["scope"]) == 1]
        nonunary = [key for key in bucket if len(factors[key]["scope"]) != 1]
        union = {v for key in bucket for v in factors[key]["scope"]}
        frontier = [v for v in vertices if v in union and v != vertex]
        before_checks, before_lookups = checks, lookups
        before_cap_scans, before_color_trials = cap_scan_rows, color_trials
        anchor, anchor_cap = None, None
        try:
            domain = [c for c in COLORS if accepts(unary, {vertex: c})]
            if not domain:
                groups = []
                staged = [dict(kind="table", scope=[], rows=[],
                               source_factor_ids=list(unary), eliminated_vertex=vertex)]
                raw_count, raw_rows, raw_max_scope = 1, 0, 0
            else:
                if not nonunary:
                    groups = [()]
                elif method == "full":
                    groups = [tuple(nonunary)]
                elif method == "anchored":
                    caps = {key: support_cap(key, vertex, domain) for key in nonunary}
                    anchor = min(nonunary, key=lambda key: (
                        comb(len(nonunary) - 1, min(caps[key], len(nonunary) - 1)),
                        len(factors[key]["scope"]), int(key[1:])))
                    anchor_cap = caps[anchor]
                    others = [key for key in nonunary if key != anchor]
                    groups = ((anchor,) + group for group in
                              combinations(others, min(anchor_cap, len(others))))
                else:
                    groups = combinations(nonunary, min(len(domain), len(nonunary)))
                # Equal ordered scopes have a common coordinate system. Their
                # conjunction is the exact intersection of complete row sets.
                tables = {}
                raw_count = raw_rows = raw_max_scope = 0
                for group in groups:
                    scope_set = {v for key in group for v in factors[key]["scope"]}
                    scope = tuple(v for v in vertices if v in scope_set and v != vertex)
                    rows = set()
                    for boundary in product(COLORS, repeat=len(scope)):
                        assignment = dict(zip(scope, boundary))
                        for color in domain:
                            assignment[vertex] = color
                            if accepts(group, assignment):
                                rows.add(boundary)
                                break
                    raw_count += 1
                    raw_rows += len(rows)
                    raw_max_scope = max(raw_max_scope, len(scope))
                    sources = set(unary) | set(group)
                    if scope in tables:
                        old_rows, old_sources = tables[scope]
                        old_rows.intersection_update(rows)
                        old_sources.update(sources)
                    else:
                        tables[scope] = (rows, sources)
                staged = [dict(kind="table", scope=list(scope),
                               rows=[list(row) for row in sorted(rows)],
                               source_factor_ids=sorted(sources, key=lambda key: int(key[1:])),
                               eliminated_vertex=vertex)
                          for scope, (rows, sources) in tables.items()]
        except _WorkLimit:
            stop_reason = "work_limit"
            break

        # Transaction boundary: no factor, active ID or history entry is
        # changed until every required projection has been computed in full.
        projected = [add_factor(factor) for factor in staged]
        bucket_ids = set(bucket)
        active_ids = [key for key in active_ids if key not in bucket_ids] + projected
        active.remove(vertex)
        history.append(dict(vertex=vertex, scope=frontier, kind="recipe",
                            input_factor_ids=bucket, effective_domain=domain))
        steps.append(dict(vertex=vertex, effective_domain_size=len(domain),
                          bucket_factors=len(bucket), nonunary_bucket_factors=len(nonunary),
                          complete_interface_size=len(frontier),
                          projected_factors_before_merge=raw_count,
                          projected_factors=len(staged),
                          projected_rows_before_merge=raw_rows,
                          projected_rows=sum(len(factor["rows"]) for factor in staged),
                          max_projected_scope=raw_max_scope,
                          candidate_checks=checks - before_checks,
                          factor_lookups=lookups - before_lookups,
                          color_trials=color_trials - before_color_trials,
                          cap_scan_rows=cap_scan_rows - before_cap_scans,
                          anchor_factor_id=anchor, anchor_support_cap=anchor_cap))
    else:
        if not active:
            stop_reason = "all_eliminated"

    needed = set(active_ids)
    for record in history:
        needed.update(record["input_factor_ids"])
    factors = {key: factor for key, factor in factors.items() if key in needed}
    empty = any(factors[key]["kind"] == "table" and not factors[key]["rows"]
                for key in active_ids)
    decision = "unsatisfiable" if empty else "satisfiable" if not active else "undetermined"
    return dict(schema=SCHEMA, projection_method=method, vertices=list(vertices),
                active_vertices=[v for v in vertices if v in active],
                factors=factors, active_factor_ids=active_ids, history=history,
                stop_reason=stop_reason, decision=decision,
                metrics=dict(candidate_checks=checks, factor_lookups=lookups,
                             color_trials=color_trials, cap_scan_rows=cap_scan_rows,
                             eliminations=len(history), recipe_steps=len(history),
                             stored_fibre_rows=0,
                             retained_table_rows=sum(len(f.get("rows", [])) for f in factors.values()),
                             max_projected_scope=max((s["max_projected_scope"] for s in steps), default=0),
                             steps=steps))
