#!/usr/bin/env python3
"""Experimental exact solution representation using an unfinished history.

A completed elimination prefix and its residual factors define every original
solution. A history entry may store its complete fibre table or an exact recipe
over the old bucket factors. Recipes omit tables, not constraints. This module
does not change the production solver, assign live colours, or promise speedups.
"""

from __future__ import annotations

from itertools import product

from four_color_lab import normalize_graph


SCHEMA = "four-color-partial-history-v1"
HISTORY_MODES = ("table", "recipe", "mixed")
COLORS = range(4)


def _colors(values):
    return (isinstance(values, (list, tuple))
            and all(type(c) is int and c in COLORS for c in values))


def _scope(scope, allowed):
    if (not isinstance(scope, list) or any(type(v) is not int or v not in allowed for v in scope)
            or len(set(scope)) != len(scope)):
        raise ValueError("invalid factor or history scope")
    return tuple(scope)


def _factor_predicate(factor, allowed):
    scope = _scope(factor["scope"], allowed)
    kind = factor["kind"]
    if kind == "domain":
        colors = factor["colors"]
        if len(scope) != 1 or not _colors(colors) or len(set(colors)) != len(colors):
            raise ValueError("invalid domain factor")
        choices = frozenset(colors)
        return lambda assignment: assignment[scope[0]] in choices
    if kind == "neq":
        if len(scope) != 2:
            raise ValueError("invalid edge factor")
        return lambda assignment: assignment[scope[0]] != assignment[scope[1]]
    if kind == "table":
        rows = factor["rows"]
        if (not isinstance(rows, list)
                or any(not _colors(row) or len(row) != len(scope) for row in rows)):
            raise ValueError("invalid factor rows")
        relation = frozenset(tuple(row) for row in rows)
        if len(relation) != len(rows):
            raise ValueError("duplicate factor row")
        return lambda assignment: tuple(assignment[v] for v in scope) in relation
    raise ValueError("unknown factor kind")


def build_representation(graph, *, stop_after=None, history_mode="table", order=None,
                         max_checks=None):
    """Eliminate at most the requested prefix; interrupted steps never commit.

    Work counts full bucket assignments checked, not interpreter operations.
    Projected relations are still explicit tables in every mode. Recipe mode
    omits history fibre rows and retains the exact factors needed to recompute
    them; it does not claim a smaller representation for every input.
    """
    graph = normalize_graph(graph)
    vertices = graph["vertices"]
    n = len(vertices)
    if stop_after is None:
        stop_after = n
    if type(stop_after) is not int or not 0 <= stop_after <= n:
        raise ValueError("stop_after must be an integer from zero to the vertex count")
    if history_mode not in HISTORY_MODES:
        raise ValueError("unknown history_mode")
    if max_checks is not None and (type(max_checks) is not int or max_checks < 0):
        raise ValueError("max_checks must be a nonnegative integer or None")
    if order is None:
        order = vertices
    if (not isinstance(order, (list, tuple)) or any(type(v) is not int for v in order)
            or len(order) != n or set(order) != set(vertices)):
        raise ValueError("order must be a permutation of the original vertices")

    factors, predicates, active_ids, history = {}, {}, [], []
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

    checks = 0
    stop_reason = "requested_prefix"
    for step, vertex in enumerate(order[:stop_after]):
        bucket = [key for key in active_ids if vertex in factors[key]["scope"]]
        union = {v for key in bucket for v in factors[key]["scope"]}
        frontier = [v for v in vertices if v in union and v != vertex]
        table = {}
        interrupted = False
        for boundary in product(COLORS, repeat=len(frontier)):
            assignment = dict(zip(frontier, boundary))
            choices = []
            for color in COLORS:
                if max_checks is not None and checks >= max_checks:
                    interrupted = True
                    break
                checks += 1
                assignment[vertex] = color
                if all(predicates[key](assignment) for key in bucket):
                    choices.append(color)
            if interrupted:
                break
            if choices:
                table[boundary] = choices
        if interrupted:
            stop_reason = "work_limit"
            break

        # Only now is the exact projection complete. Everything above was local
        # work; a limit cannot publish an incomplete table as an empty fibre.
        kind = "recipe" if history_mode == "recipe" or (history_mode == "mixed" and step % 2) else "table"
        record = dict(vertex=vertex, scope=frontier, kind=kind)
        if kind == "table":
            record["rows"] = [dict(boundary=list(boundary), colors=choices)
                              for boundary, choices in table.items()]
        else:
            record["input_factor_ids"] = bucket
        projected = add_factor(dict(kind="table", scope=frontier,
                                    rows=[list(boundary) for boundary in table]))
        bucket_ids = set(bucket)
        active_ids = [key for key in active_ids if key not in bucket_ids] + [projected]
        active.remove(vertex)
        history.append(record)
    else:
        if not active:
            stop_reason = "all_eliminated"

    # Factors contain no nested references. Retain precisely the active factors
    # and direct historical recipe dependencies, including domain restrictions.
    needed = set(active_ids)
    for record in history:
        needed.update(record.get("input_factor_ids", []))
    factors = {key: factor for key, factor in factors.items() if key in needed}
    empty = any(factors[key]["kind"] == "table" and not factors[key]["rows"] for key in active_ids)
    decision = "unsatisfiable" if empty else "satisfiable" if not active else "undetermined"
    return dict(schema=SCHEMA, vertices=list(vertices),
                active_vertices=[v for v in vertices if v in active],
                factors=factors, active_factor_ids=active_ids, history=history,
                stop_reason=stop_reason, decision=decision,
                metrics=dict(candidate_checks=checks, eliminations=len(history),
                             stored_fibre_rows=sum(len(h.get("rows", [])) for h in history),
                             recipe_steps=sum(h["kind"] == "recipe" for h in history),
                             retained_table_rows=sum(len(f.get("rows", [])) for f in factors.values())))


def _compile(rep):
    """Compile the self-contained constraints, independently of decision labels."""
    if rep.get("schema") != SCHEMA:
        raise ValueError("unknown representation schema")
    vertices = rep["vertices"]
    if (not isinstance(vertices, list) or any(type(v) is not int for v in vertices)
            or len(set(vertices)) != len(vertices)):
        raise ValueError("invalid original vertex identities")
    allowed = set(vertices)
    active = _scope(rep["active_vertices"], allowed)
    history = rep["history"]
    eliminated = [h["vertex"] for h in history]
    if (any(type(v) is not int for v in eliminated) or len(set(eliminated)) != len(eliminated)
            or set(eliminated) & set(active) or set(eliminated) | set(active) != allowed):
        raise ValueError("history and active vertices must partition the original vertices")
    factors = rep["factors"]
    predicates = {key: _factor_predicate(factor, allowed) for key, factor in factors.items()}

    def references(keys, scope):
        if not isinstance(keys, list) or len(set(keys)) != len(keys):
            raise ValueError("invalid factor references")
        if any(key not in factors or not set(factors[key]["scope"]) <= scope for key in keys):
            raise ValueError("missing factor or factor outside the permitted scope")
        return tuple(predicates[key] for key in keys)

    residual = references(rep["active_factor_ids"], set(active))
    compiled_history = []
    remaining = set(vertices)
    for record in history:
        vertex = record["vertex"]
        remaining.remove(vertex)
        scope = _scope(record["scope"], remaining)
        if record["kind"] == "table":
            table = {}
            for row in record["rows"]:
                boundary, choices = row["boundary"], row["colors"]
                if (not _colors(boundary) or len(boundary) != len(scope)
                        or not _colors(choices) or not choices
                        or len(set(choices)) != len(choices) or tuple(boundary) in table):
                    raise ValueError("invalid complete fibre table")
                table[tuple(boundary)] = tuple(sorted(choices))

            def choices_for(boundary, table=table):
                return table.get(boundary, ())
        elif record["kind"] == "recipe":
            inputs = references(record["input_factor_ids"], set(scope) | {vertex})

            def choices_for(boundary, inputs=inputs, scope=scope, vertex=vertex):
                assignment = dict(zip(scope, boundary))
                choices = []
                for color in COLORS:
                    assignment[vertex] = color
                    if all(predicate(assignment) for predicate in inputs):
                        choices.append(color)
                return tuple(choices)
        else:
            raise ValueError("unknown history representation")
        compiled_history.append((vertex, scope, choices_for))
    return tuple(vertices), active, residual, compiled_history


def compile_representation(rep):
    """Return membership in all original solutions, without accessing a graph."""
    vertices, _, residual, history = _compile(rep)

    def accepts(colors):
        if not _colors(colors) or len(colors) != len(vertices):
            return False
        assignment = dict(zip(vertices, colors))
        return (all(predicate(assignment) for predicate in residual)
                and all(assignment[v] in choices(tuple(assignment[w] for w in scope))
                        for v, scope, choices in history))
    return accepts


def fibre_choices(rep, history_index, boundary):
    """Return all historical bucket supports, not global extendibility.

    The full representation also enforces residual factors, including any
    frontier domains that were outside this historical bucket.
    """
    _, _, _, history = _compile(rep)
    if type(history_index) is not int or not 0 <= history_index < len(history):
        raise ValueError("history_index is outside the recorded prefix")
    _, scope, choices = history[history_index]
    if not _colors(boundary) or len(boundary) != len(scope):
        raise ValueError("boundary must be a complete ordered tuple of literal colors")
    return choices(tuple(boundary))


def reconstruct_one(rep):
    """Solve the residual problem, then reverse the prefix for one common witness.

    The prototype enumerates residual assignments until the first solution, so
    stopping elimination earlier need not make finding a witness faster.
    """
    vertices, active, residual, history = _compile(rep)
    for row in product(COLORS, repeat=len(active)):
        assignment = dict(zip(active, row))
        if not all(predicate(assignment) for predicate in residual):
            continue
        for vertex, scope, choices in reversed(history):
            support = choices(tuple(assignment[w] for w in scope))
            if not support:
                raise ValueError("residual solution has no historical extension")
            assignment[vertex] = support[0]
        return [assignment[v] for v in vertices]
    return None
