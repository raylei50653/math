"""Exact local cycle supports with one common original context vertex.

Each candidate colour of the context vertex is kept fixed while the entire
original cycle is closed.  The candidates are then united, rather than chosen.
This preserves a shared condition that independent unary cycle supports lose.
Only actual cycle edges and actual edges from the context vertex to that cycle
participate.  Original chords and other attachments remain the responsibility
of their original factors; this local query is not a global SAT certificate.
"""

from __future__ import annotations

from four_color_local_information import derive_cycle


def derive_cycle_context(graph, cycle, context_vertex, domain_masks, *, charge=None):
    """Return exact supports and hub/rim pair projections of a local relation.

    ``domain_masks`` has one exact integer in 0..15 per original vertex, in
    ``graph['vertices']`` order.  ``cycle`` is an ordered simple original cycle
    of at least three vertices.  The original ``context_vertex`` is outside it.
    Its colour is excluded only at its actual neighbours on the cycle; partial
    spokes are allowed.  Supplied masks carry all current unary restrictions.

    For every context candidate, an anchored forward/backward cycle query is
    completed before its supports contribute to the result.  ``pair_relations``
    gives the complete binary projection on ``[context_vertex, rim_vertex]``
    for *every* rim vertex, including non-neighbours.  ``cycle_edge_relations``
    similarly projects onto every consecutive rim edge, including the closing
    edge in its supplied orientation.  ``context_edge_relations`` preserves
    the shared context colour in the complete ternary projection on each
    ``[context_vertex, rim_vertex, next_rim_vertex]`` scope.  At most sixteen
    rows are exported per pair and sixty-four per triple; no full cycle-
    colouring table is enumerated.  These projections do not, by themselves,
    recover the complete local relation.

    ``charge()`` is called before every counted validation, conditioning,
    support/export stage, and every stage of the underlying cycle DP.  Its
    exceptions propagate unchanged.  No supplied object is mutated, including
    if validation or a query is interrupted.  Empty domains return an empty
    local relation; malformed inputs raise ValueError.  Other original edges,
    fixed-colour metadata, and domains outside the cycle/context are not extra
    constraints of this local query.
    """
    if charge is not None and not callable(charge):
        raise ValueError("charge must be callable or None")
    operations = 0
    dp_operations = 0

    def step():
        nonlocal operations
        if charge is not None:
            charge()
        operations += 1

    def dp_step():
        nonlocal dp_operations
        step()
        dp_operations += 1

    if not isinstance(graph, dict):
        raise ValueError("graph must contain original vertices and edges")
    supplied_vertices, supplied_edges = graph.get("vertices"), graph.get("edges")
    if not isinstance(supplied_vertices, list):
        raise ValueError("vertices must be a list of unique exact integer ids")
    vertices = list(supplied_vertices)
    positions = {}
    for position, vertex in enumerate(vertices):
        step()
        if type(vertex) is not int or vertex in positions:
            raise ValueError("vertices must be a list of unique exact integer ids")
        positions[vertex] = position
    if not isinstance(supplied_edges, list):
        raise ValueError("edges must be a list of original edge pairs")
    original_edges = set()
    for edge in supplied_edges:
        step()
        if (not isinstance(edge, (list, tuple)) or len(edge) != 2
                or any(type(vertex) is not int or vertex not in positions
                       for vertex in edge) or edge[0] == edge[1]):
            raise ValueError("edges must join two distinct original vertex ids")
        key = frozenset(edge)
        if key in original_edges:
            raise ValueError("duplicate original edge")
        original_edges.add(key)

    try:
        masks = list(domain_masks)
    except TypeError as error:
        raise ValueError("domain masks must be aligned with original vertices") from error
    if len(masks) != len(vertices):
        raise ValueError("one domain mask is required per original vertex")
    for mask in masks:
        step()
        if type(mask) is not int or not 0 <= mask <= 15:
            raise ValueError("domain masks must be exact integers in 0..15")
    try:
        rim = list(cycle)
    except TypeError as error:
        raise ValueError("cycle must contain at least three distinct original ids") from error
    if len(rim) < 3:
        raise ValueError("cycle must contain at least three distinct original ids")
    seen = set()
    for vertex in rim:
        step()
        if type(vertex) is not int or vertex not in positions or vertex in seen:
            raise ValueError("cycle must contain distinct original vertex ids")
        seen.add(vertex)
    if (type(context_vertex) is not int or context_vertex not in positions
            or context_vertex in seen):
        raise ValueError("context vertex must be an original id outside the cycle")

    cycle_edges, context_edges, spoke_positions = [], [], set()
    for position, vertex in enumerate(rim):
        step()
        following = rim[(position + 1) % len(rim)]
        if frozenset((vertex, following)) not in original_edges:
            raise ValueError("every consecutive and closing cycle edge must be original")
        cycle_edges.append([vertex, following])
        step()
        if frozenset((context_vertex, vertex)) in original_edges:
            context_edges.append([context_vertex, vertex])
            spoke_positions.add(position)

    rim_masks = [masks[positions[vertex]] for vertex in rim]
    context_mask = masks[positions[context_vertex]]
    supports = [0] * len(rim)
    pair_rows = [[] for _ in rim]
    edge_rows = [set() for _ in rim]
    context_edge_rows = [set() for _ in rim]
    context_support = 0
    row_count = 0
    cases = []
    witness = None
    for colour in range(4):
        step()
        bit = 1 << colour
        if not context_mask & bit:
            continue
        conditioned = []
        for position, mask in enumerate(rim_masks):
            step()
            conditioned.append(mask & (15 ^ bit) if position in spoke_positions else mask)
        answer = derive_cycle(conditioned, charge=dp_step)
        cases.append({"context_color": colour,
                      "conditioned_domain_masks": conditioned,
                      "cycle_supports": list(answer["supports"]),
                      "row_count": answer["row_count"]})
        if not answer["row_count"]:
            continue
        context_support |= bit
        row_count += answer["row_count"]
        for position, supported in enumerate(answer["supports"]):
            step()
            supports[position] |= supported
            for rim_colour in range(4):
                step()
                if supported & (1 << rim_colour):
                    pair_rows[position].append([colour, rim_colour])
        # A prefix and suffix can be joined across one rim edge only when
        # they keep the *same* cycle anchor.  Combining anchors here would
        # incorrectly admit incompatible pieces of different local rows.
        for anchor_case in answer["anchor_cases"]:
            step()
            if not anchor_case["row_count"]:
                continue
            anchor = anchor_case["anchor"]
            forward = anchor_case["forward_masks"]
            backward = anchor_case["backward_masks"]
            for position in range(len(rim)):
                step()
                if position == len(rim) - 1:
                    for first in range(4):
                        step()
                        if forward[position] & (1 << first) and first != anchor:
                            edge_rows[position].add((first, anchor))
                            triple = (colour, first, anchor)
                            if triple not in context_edge_rows[position]:
                                step()
                                context_edge_rows[position].add(triple)
                else:
                    for first in range(4):
                        for second in range(4):
                            step()
                            if (forward[position] & (1 << first)
                                    and backward[position + 1] & (1 << second)
                                    and first != second):
                                edge_rows[position].add((first, second))
                                triple = (colour, first, second)
                                if triple not in context_edge_rows[position]:
                                    step()
                                    context_edge_rows[position].add(triple)
        if witness is None:
            witness = {"scope": [context_vertex, *rim],
                       "colors": [colour, *answer["witness"]]}

    return {
        "context_vertex": context_vertex,
        "cycle": rim,
        "domain_scope": [context_vertex, *rim],
        "domain_masks": [context_mask, *rim_masks],
        "context_support_mask": context_support,
        "cycle_supports": supports,
        "row_count": row_count,
        "pair_relations": [{"scope": [context_vertex, vertex], "rows": rows}
                           for vertex, rows in zip(rim, pair_rows)],
        "cycle_edge_relations": [
            {"scope": edge, "rows": [list(row) for row in sorted(rows)]}
            for edge, rows in zip(cycle_edges, edge_rows)],
        "context_edge_relations": [
            {"scope": [context_vertex, *edge],
             "rows": [list(row) for row in sorted(rows)]}
            for edge, rows in zip(cycle_edges, context_edge_rows)],
        "cases": cases,
        "cycle_edges": cycle_edges,
        "context_edges": context_edges,
        "witness": witness,
        "op_count": operations,
        "dp_op_count": dp_operations,
        "state_capacity": 16,
        "context_case_capacity": 4,
        "pair_relation_row_capacity": 16,
        "context_edge_relation_row_capacity": 64,
        "method": "context-conditioned-anchored-forward-backward-cycle",
        "relation_contract": (
            "exact supports, count, complete context/rim binary projections, "
            "complete consecutive rim-edge binary projections, and complete "
            "context/rim-edge ternary projections "
            "for this one original cycle, its actual context spokes, and these "
            "literal domains; the cases are united without choosing a colour; "
            "these projections are not the complete joint relation and local "
            "nonemptiness does not imply global satisfiability"
        ),
    }
