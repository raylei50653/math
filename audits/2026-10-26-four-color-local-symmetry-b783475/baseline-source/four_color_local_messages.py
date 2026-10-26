"""Exact lazy separator queries, with local witnesses kept until writeback.

This experimental solver builds a tree decomposition and asks one complete
separator tuple at a time.  A reply says only whether that tuple has a local
extension.  It does not export a full separator table or a private bag row.
The original constraints remain the exact implicit relation; the explored
cache is not declared a complete relation or a list of all colouring fibres.

There is no cryptographic privacy claim: one process receives the whole graph,
the decomposition is public, and the final requested colouring is returned.
The message protocol reduces disclosure/work on some inputs, but may inspect
every separator tuple.  Fill edges describe bags, never extra colouring edges.
"""

from __future__ import annotations

from collections.abc import Mapping
from itertools import combinations

from four_color_lab import normalize_graph


class _Limit(Exception):
    pass


def solve_local_messages(graph, *, domains=None, max_checks=1000000,
                         max_messages=100000, max_cache_entries=100000,
                         transcript_limit=100000, audit_metadata=False):
    """Decide finite graph colouring by lazy, exact tree-separator queries.

    ``graph`` uses the laboratory's vertices/edges/fixed dictionary format.
    Optional ``domains`` maps original vertex IDs to iterables of literal
    colours; omitted vertices allow all four, and fixed colours intersect them.
    The input is never mutated.  Completed replies are exact existential
    decisions for the queried subtree's allocated edges and vertex domains.

    A successful query privately remembers one owner colour, not all fibres.
    Only after every root succeeds does writeback select one compatible global
    witness, independently checked against all original edges and domains.
    Internal candidate rows are feasibility probes, not committed colours.

    All three resource caps fail with ``status='limit'`` and ``colors=None``;
    no unfinished query returns a negative reply.  Work checks include min-fill
    candidates/pairs, decomposition validation, local queries, and writeback.
    Input validation, object allocation, sorting and dictionary operations are
    outside this logical-work count; it is not a CPU instruction counter.
    The transcript storage cap only truncates logging, never computation.
    All traversals are iterative, including deep disconnected forests.
    ``audit_metadata=True`` additionally exports private bags and allocated
    original edges for independent replay.  Default metadata only describes
    bag identifiers, interface vertices, tree links, and bag sizes.
    """
    for value in (max_checks, max_messages, max_cache_entries, transcript_limit):
        if type(value) is not int or value < 0:
            raise ValueError("limits must be nonnegative integers")
    if type(audit_metadata) is not bool:
        raise ValueError("audit_metadata must be a boolean")
    g = normalize_graph(graph)
    vertices = g["vertices"]
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    allowed = [set(range(4)) for _ in vertices]
    if domains is not None:
        if not isinstance(domains, Mapping):
            raise ValueError("domains must map declared vertices to colour iterables")
        for vertex, values in domains.items():
            if type(vertex) is not int or vertex not in index:
                raise ValueError("domains contain an undeclared integer vertex")
            try:
                values = list(values)
            except TypeError as exc:
                raise ValueError("each domain must be an iterable of colours") from exc
            if any(type(c) is not int or c not in range(4) for c in values):
                raise ValueError("domain colours must be exact integers in 0..3")
            allowed[index[vertex]] = set(values)
    for vertex, colour in g["fixed"]:
        allowed[index[vertex]].intersection_update((colour,))
    allowed = [tuple(sorted(values)) for values in allowed]
    edges = [tuple(sorted((index[u], index[v]))) for u, v in g["edges"]]
    original = [set() for _ in vertices]
    for u, v in edges:
        original[u].add(v)
        original[v].add(u)

    stats = dict(checks=0, check_kinds={}, preprocessing_checks=0, query_checks=0,
                 writeback_checks=0, messages=0, queries=0, replies=0,
                 positive_replies=0, negative_replies=0, cache_hits=0,
                 cache_entries=0, unique_queries=0, max_bag_size=0,
                 max_separator_size=0, potential_separator_rows=0,
                 table_rows_exported=0, writeback_vertices=0,
                 candidate_rows=0, max_stack_depth=0)
    transcript = []
    decomposition = None
    private_cache = {}
    requested = set()
    phase = "preprocessing_checks"

    def charge(kind):
        if stats["checks"] >= max_checks:
            raise _Limit("max_checks")
        stats["checks"] += 1
        stats[phase] += 1
        stats["check_kinds"][kind] = stats["check_kinds"].get(kind, 0) + 1

    def emit(event):
        if stats["messages"] >= max_messages:
            raise _Limit("max_messages")
        stats["messages"] += 1
        if len(transcript) < transcript_limit:
            transcript.append(event)

    def result(status, colours=None, reason=None):
        return dict(status=status, colors=colours, limit_reason=reason,
                    stats=stats, decomposition=decomposition,
                    transcript=transcript,
                    transcript_truncated=len(transcript) < stats["messages"],
                    eager_tables_built=False,
                    cache_declared_complete=False,
                    relation_representation="original constraints plus exact lazy query procedure")

    try:
        # The order depends only on graph structure, not colours or responses.
        remaining = set(range(n))
        filled = [set(neighbours) for neighbours in original]
        order = []
        separators = []
        while remaining:
            best = None
            selected = None
            selected_neighbours = None
            for v in sorted(remaining):
                charge("minfill_candidate")
                ns = sorted(filled[v] & remaining)
                missing = 0
                for u, w in combinations(ns, 2):
                    charge("minfill_pair")
                    missing += w not in filled[u]
                score = (missing, len(ns), v)
                if best is None or score < best:
                    best, selected, selected_neighbours = score, v, ns
            order.append(selected)
            separators.append(tuple(selected_neighbours))
            for u, w in combinations(selected_neighbours, 2):
                charge("fill_pair")
                filled[u].add(w)
                filled[w].add(u)
            remaining.remove(selected)
        rank = {v: b for b, v in enumerate(order)}
        parent = [min((rank[v] for v in sep), default=None) for sep in separators]
        children = [[] for _ in vertices]
        roots = []
        bags = []
        local_edges = [[] for _ in vertices]
        for u, v in edges:
            charge("edge_allocation")
            local_edges[min(rank[u], rank[v])].append((u, v))
        for b, v in enumerate(order):
            charge("bag_validation")
            bag = tuple(sorted((v, *separators[b])))
            bags.append(bag)
            if parent[b] is None:
                roots.append(b)
            else:
                if parent[b] <= b:
                    raise AssertionError("decomposition parent is not later")
                children[parent[b]].append(b)

        # Explicitly verify coverage and running intersection.  The parent
        # forest is acyclic; a connected occurrence set has size-1 tree edges.
        occurrences = [0] * n
        shared_links = [0] * n
        for b, bag in enumerate(bags):
            bag_set = set(bag)
            for v in bag:
                charge("vertex_occurrence")
                occurrences[v] += 1
            if parent[b] is not None:
                parent_set = set(bags[parent[b]])
                if not set(separators[b]) <= parent_set:
                    raise AssertionError("separator is not inside its parent bag")
                for v in bag_set & parent_set:
                    charge("running_intersection")
                    shared_links[v] += 1
            elif separators[b]:
                raise AssertionError("root has a nonempty separator")
            for u, v in local_edges[b]:
                charge("edge_coverage")
                if u not in bag_set or v not in bag_set:
                    raise AssertionError("an original edge is not covered")
        for v in range(n):
            charge("running_intersection_vertex")
            if occurrences[v] == 0 or shared_links[v] != occurrences[v] - 1:
                raise AssertionError("vertex bags violate running intersection")
        decomposition = dict(
            roots=roots, validated=True, audit_metadata=audit_metadata,
            bags=[dict(id=b, bag_size=len(bags[b]),
                       separator=[vertices[v] for v in separators[b]],
                       parent=parent[b], children=children[b]) for b in range(n)])
        if audit_metadata:
            decomposition["order"] = [vertices[v] for v in order]
            for b, metadata in enumerate(decomposition["bags"]):
                metadata.update(vertex=vertices[order[b]],
                                vertices=[vertices[v] for v in bags[b]],
                                local_edges=[[vertices[u], vertices[v]]
                                             for u, v in local_edges[b]])
        stats["max_bag_size"] = max(map(len, bags), default=0)
        stats["max_separator_size"] = max(map(len, separators), default=0)
        stats["potential_separator_rows"] = sum(4 ** len(sep) for sep in separators)
        phase = "query_checks"
        stack = []

        def ask(bag, row):
            query_id = stats["queries"]
            event = dict(kind="query", query_id=query_id, bag=bag, sender=parent[bag],
                         receiver=bag, separator=[vertices[v] for v in separators[bag]],
                         colors=list(row))
            emit(event)
            stats["queries"] += 1
            requested.add((bag, row))
            stats["unique_queries"] = len(requested)
            stack.append(dict(bag=bag, boundary=row, query_id=query_id,
                              stage="start", next_colour=0))
            stats["max_stack_depth"] = max(stats["max_stack_depth"], len(stack))

        def finish(possible, owner_colour=None, cached=False):
            frame = stack[-1]
            bag, row = frame["bag"], frame["boundary"]
            key = (bag, row)
            if not cached and len(private_cache) >= max_cache_entries:
                raise _Limit("max_cache_entries")
            charge("completed_reply")
            event = dict(kind="reply", query_id=frame["query_id"], bag=bag,
                         sender=bag, receiver=parent[bag],
                         separator=[vertices[v] for v in separators[bag]],
                         colors=list(row), possible=possible, cached=cached)
            emit(event)
            if not cached:
                private_cache[key] = (possible, owner_colour)
                stats["cache_entries"] = len(private_cache)
            stats["replies"] += 1
            stats["positive_replies" if possible else "negative_replies"] += 1
            stack.pop()
            if stack:
                stack[-1]["child_result"] = possible
            return possible

        for root in roots:
            ask(root, ())
            root_result = None
            while stack:
                frame = stack[-1]
                b, boundary = frame["bag"], frame["boundary"]
                owner = order[b]
                if frame["stage"] == "start":
                    charge("cache_lookup")
                    cached = private_cache.get((b, boundary))
                    if cached is not None:
                        stats["cache_hits"] += 1
                        root_result = finish(cached[0], cached=True)
                        continue
                    boundary_ok = True
                    for v, colour in zip(separators[b], boundary):
                        charge("boundary_domain")
                        if colour not in allowed[v]:
                            boundary_ok = False
                            break
                    if not boundary_ok:
                        root_result = finish(False)
                        continue
                    frame["stage"] = "candidate"
                elif frame["stage"] == "candidate":
                    if frame["next_colour"] >= len(allowed[owner]):
                        root_result = finish(False)
                        continue
                    colour = allowed[owner][frame["next_colour"]]
                    frame["next_colour"] += 1
                    charge("candidate_row")
                    stats["candidate_rows"] += 1
                    row = dict(zip(separators[b], boundary))
                    row[owner] = colour
                    legal = True
                    for u, v in local_edges[b]:
                        charge("local_edge")
                        if row[u] == row[v]:
                            legal = False
                            break
                    if legal:
                        frame.update(stage="children", row=row, owner_colour=colour,
                                     next_child=0)
                elif frame["stage"] == "children":
                    if frame["next_child"] == len(children[b]):
                        root_result = finish(True, frame["owner_colour"])
                        continue
                    child = children[b][frame["next_child"]]
                    frame["next_child"] += 1
                    child_row = []
                    for v in separators[child]:
                        charge("child_projection")
                        child_row.append(frame["row"][v])
                    frame["stage"] = "await_child"
                    ask(child, tuple(child_row))
                else:
                    frame["stage"] = ("children" if frame.pop("child_result")
                                      else "candidate")
            if root_result is not True:
                return result("unsatisfiable")

        # One compatible global assignment is first committed here.  Every
        # remembered child query was answered under this exact parent tuple.
        phase = "writeback_checks"
        colours = [None] * n
        pending = [(root, ()) for root in reversed(roots)]
        while pending:
            b, boundary = pending.pop()
            charge("writeback_owner")
            possible, colour = private_cache[(b, boundary)]
            if not possible:
                raise AssertionError("writeback reached a negative query")
            row = dict(zip(separators[b], boundary))
            row[order[b]] = colour
            colours[order[b]] = colour
            stats["writeback_vertices"] += 1
            for child in reversed(children[b]):
                child_row = []
                for v in separators[child]:
                    charge("writeback_projection")
                    child_row.append(row[v])
                pending.append((child, tuple(child_row)))
        for v, colour in enumerate(colours):
            charge("verify_domain")
            if colour not in allowed[v]:
                raise AssertionError("writeback violates an original domain")
        for u, v in edges:
            charge("verify_edge")
            if colours[u] == colours[v]:
                raise AssertionError("writeback violates an original edge")
        return result("colored", colours)
    except _Limit as exc:
        return result("limit", reason=str(exc))
