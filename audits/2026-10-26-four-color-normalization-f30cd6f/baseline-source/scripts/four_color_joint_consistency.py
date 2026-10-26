"""Exact joint supports of existing factors without eliminating a variable.

This is an optional, bounded query on a supplied group of complete factors.
It enumerates their common assignments in one literal colour frame and projects
support back to the original rows and domains.  Its scope can be the whole graph;
it is not a fixed-width or universally sufficient local inference rule.
"""
from __future__ import annotations

from math import prod


def joint_supports(factors, domains, *, max_checks=200000,
                   max_support_rows=100000, charge=None):
    """Return exact joint row/domain supports, or an entirely uncommitted skip.

    ``factors`` is a sequence of ``(ordered_scope, complete_rows)`` pairs and
    ``domains[v]`` is the current colour set of vertex ``v``. Only scoped domains
    are consulted. No argument is mutated. ``rows`` in a complete answer is a
    list of frozensets aligned with the supplied factor order; ``domains`` is a
    mapping from vertices to frozensets. An incomplete answer exposes neither.

    A check is an anchor row, attempted prefix colour, complete factor test,
    or accepted-assignment support projection. ``charge()`` runs before each
    counted check and its exceptions propagate unchanged. The local check/row
    caps return ``complete=False`` and discard partial supports. They must not
    be interpreted as an empty relation. Input validation is outside the budget.

    Full enumeration is unnecessary once every input row and scoped domain value
    has a joint witness. In that case the supports are already exact; the result
    records ``enumeration_complete=False`` and ``all_supports_saturated=True``.
    ``assignments`` counts visited witnesses, not a general solution count.
    """
    if any(type(x) is not int or x < 0 for x in (max_checks, max_support_rows)):
        raise ValueError("joint query caps must be nonnegative integers")
    if charge is not None and not callable(charge):
        raise ValueError("charge must be callable or None")
    prepared = []
    for scope, rows in factors:
        scope = tuple(scope)
        if any(type(v) is not int for v in scope) or len(set(scope)) != len(scope):
            raise ValueError("factor scopes need distinct integer vertices")
        rows = frozenset(tuple(row) for row in rows)
        if any(len(row) != len(scope) or any(type(c) is not int or c not in range(4)
                                            for c in row) for row in rows):
            raise ValueError("factor rows need aligned literal colours 0..3")
        prepared.append((scope, rows))
    scope = tuple(sorted({v for columns, _ in prepared for v in columns}))
    values = {v: tuple(sorted(domains[v])) for v in scope}
    if any(type(c) is not int or c not in range(4) for row in values.values() for c in row):
        raise ValueError("domains need literal colours 0..3")
    checks = assignments = support_rows = 0
    supports = [set() for _ in prepared]
    domain_supports = {v: set() for v in scope}
    saturation_target = sum(len(rows) for _, rows in prepared) + sum(map(len, values.values()))
    supported_values = 0

    class QueryLimit(Exception):
        pass

    class Saturated(Exception):
        pass

    def tick():
        nonlocal checks
        if checks >= max_checks:
            raise QueryLimit("checks")
        if charge is not None:
            charge()
        checks += 1

    def result(complete, *, reason=None, saturated=False):
        return dict(complete=complete, truncated=not complete,
                    consistent=bool(assignments) if complete else None,
                    scope=scope,
                    rows=[frozenset(rows) for rows in supports] if complete else None,
                    domains={v: frozenset(rows) for v, rows in domain_supports.items()}
                    if complete else None,
                    checks=checks, assignments=assignments, support_rows=support_rows,
                    enumeration_complete=complete and not saturated,
                    all_supports_saturated=saturated, limit_reason=reason)

    def save(assignment):
        nonlocal assignments, support_rows, supported_values
        # A partially projected witness is private until this query completes.
        for i, (columns, _) in enumerate(prepared):
            tick()
            row = tuple(assignment[v] for v in columns)
            if row not in supports[i]:
                if support_rows >= max_support_rows:
                    raise QueryLimit("support_rows")
                supports[i].add(row)
                support_rows += 1
        for v in scope:
            tick()
            color = assignment[v]
            if color not in domain_supports[v]:
                domain_supports[v].add(color)
                supported_values += 1
        assignments += 1
        if support_rows + supported_values == saturation_target:
            raise Saturated

    try:
        tick()
        if any(not rows for _, rows in prepared) or any(not row for row in values.values()):
            return result(True)
        if not prepared:
            save({})
            return result(True)
        anchor_index = min(range(len(prepared)), key=lambda i: len(prepared[i][1]) * prod(
            len(values[v]) for v in scope if v not in prepared[i][0]))
        anchor_scope, anchor_rows = prepared[anchor_index]
        remaining = set(scope) - set(anchor_scope)
        free = []
        incidence = {v: [] for v in scope}
        missing = []
        completions = dict.fromkeys(scope, 0)
        for i, (columns, _) in enumerate(prepared):
            absent = set(columns) & remaining
            missing.append(absent)
            if len(absent) == 1:
                completions[next(iter(absent))] += 1
            for v in columns:
                incidence[v].append(i)
        while remaining:
            v = min(remaining, key=lambda v: (
                len(values[v]), -completions[v], -len(incidence[v]), v))
            free.append(v)
            remaining.remove(v)
            for i in incidence[v]:
                absent = missing[i]
                absent.discard(v)
                if len(absent) == 1:
                    completions[next(iter(absent))] += 1
        depths = {v: depth + 1 for depth, v in enumerate(free)}
        ready = [[] for _ in range(len(free) + 1)]
        for i, (columns, rows) in enumerate(prepared):
            if i != anchor_index:
                ready[max((depths.get(v, 0) for v in columns), default=0)].append((columns, rows))

        def accepted(depth, assignment):
            for columns, rows in ready[depth]:
                tick()
                if tuple(assignment[v] for v in columns) not in rows:
                    return False
            return True

        for row in sorted(anchor_rows):
            tick()
            if any(c not in values[v] for v, c in zip(anchor_scope, row)):
                continue
            assignment = dict(zip(anchor_scope, row))
            if not accepted(0, assignment):
                continue
            if not free:
                save(assignment)
                continue
            choices = [0] * len(free)
            depth = 0
            while depth >= 0:
                v = free[depth]
                if choices[depth] == len(values[v]):
                    choices[depth] = 0
                    assignment.pop(v, None)
                    depth -= 1
                    continue
                color = values[v][choices[depth]]
                choices[depth] += 1
                tick()
                assignment[v] = color
                if not accepted(depth + 1, assignment):
                    continue
                if depth + 1 == len(free):
                    save(assignment)
                else:
                    depth += 1
    except QueryLimit as error:
        return result(False, reason=str(error))
    except Saturated:
        return result(True, saturated=True)
    return result(True)
