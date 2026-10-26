"""Bounded original-subgraph discovery of the named nine-point relation.

This scan recognizes only the archived ``nine_point_joint_equality_v1``
template.  Each returned factor is independently checked by its manual
instantiator against all 21 original edges.  The scan neither reads domains nor
uses fixed colours, and does not claim to find arbitrary joint restrictions.
"""

from __future__ import annotations

from four_color_joint_constraint_audit import (
    FACTOR_ID,
    REQUIRED_ROLE_EDGES,
    ROLE_ORDER,
    instantiate_nine_point_constraint,
)
from four_color_lab import normalize_graph


def find_joint_constraints(graph, *, max_matches=128, max_scan_steps=200000,
                           charge=None):
    """Find distinct necessary equal triples within a bounded structural scan.

    Search is an injective, non-induced match of the nine named roles: extra
    original edges and outside attachments are permitted.  Candidate vertices
    are filtered by original degree and intersected with the neighbours of all
    already assigned adjacent roles.  The next role uses minimum remaining
    candidates, breaking ties by ``ROLE_ORDER``; candidate iteration uses the
    original input vertex order.  Vertex IDs, pins, and domains never choose a
    special case.

    Factors are deduplicated and sorted by the three frontier vertices in
    original input-position order.  The all-equal rows are symmetric, so their
    frontier can be reordered without changing the relation.  One exact role
    mapping, all nine source vertices, and all 21 mapped original edges are
    retained for each factor.

    A scan step precedes each degree-eligibility candidate, backtracking entry,
    MRV role/intersection stage, candidate assignment, or complete-map
    validation.  ``charge()`` is called before committing each counted step;
    its exceptions propagate unchanged.  Input validation and adjacency
    preparation are outside this budget.  Either zero cap, reaching the
    distinct-factor cap, or requiring work beyond the scan budget returns
    ``truncated=True``.  Any factors already returned remain valid.  A complete
    scan exhausts embeddings of this named template only, never all possible
    joint restrictions of the target.
    """
    g = normalize_graph(graph)
    if any(type(value) is not int or value < 0
           for value in (max_matches, max_scan_steps)):
        raise ValueError("match and scan limits must be nonnegative integers")
    if charge is not None and not callable(charge):
        raise ValueError("charge must be callable or None")

    vertices = g["vertices"]
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    adjacency = [set() for _ in vertices]
    for first, second in g["edges"]:
        first, second = positions[first], positions[second]
        adjacency[first].add(second)
        adjacency[second].add(first)
    role_positions = {role: index for index, role in enumerate(ROLE_ORDER)}
    role_adjacency = [set() for _ in ROLE_ORDER]
    for first, second in REQUIRED_ROLE_EDGES:
        first, second = role_positions[first], role_positions[second]
        role_adjacency[first].add(second)
        role_adjacency[second].add(first)

    steps = 0
    embeddings = 0
    duplicate_embeddings = 0
    found = {}

    def result(complete):
        return dict(
            constraints=[found[key] for key in sorted(found)],
            scan_steps=steps, steps=steps, complete=complete,
            truncated=not complete,
            pattern_id=FACTOR_ID,
            discoveries=len(found), embeddings=embeddings,
            duplicate_embeddings=duplicate_embeddings,
            max_matches=max_matches, max_scan_steps=max_scan_steps,
            coverage=("injective non-induced embeddings of the named nine-point "
                      "21-original-edge pattern only; not arbitrary joint restrictions"),
            all_named_pattern_embeddings_complete=complete,
            all_joint_constraints_complete=False,
            algorithm="nine-point-original-subgraph-mrv-v1",
            step_unit=("one degree-eligibility candidate, backtracking entry, "
                       "MRV role/intersection stage, candidate assignment, or "
                       "complete-map validation; adjacency preparation uncharged"),
            conditions_used="original vertices and original edges only",
            fixed_and_domain_conditions_applied=False,
        )

    if max_matches == 0 or max_scan_steps == 0:
        return result(False)

    class ScanLimit(Exception):
        pass

    class MatchLimit(Exception):
        pass

    def tick():
        nonlocal steps
        if steps >= max_scan_steps:
            raise ScanLimit
        if charge is not None:
            charge()
        steps += 1

    eligible = []
    mapping = {}
    used = set()

    def search():
        nonlocal embeddings, duplicate_embeddings
        tick()
        if len(mapping) == len(ROLE_ORDER):
            tick()
            exact_mapping = {role: vertices[mapping[index]]
                             for index, role in enumerate(ROLE_ORDER)}
            factor = instantiate_nine_point_constraint(g, exact_mapping)
            if factor is None:
                raise AssertionError("structural matcher omitted a required original edge")
            embeddings += 1
            key = tuple(sorted(positions[vertex] for vertex in factor["frontier"]))
            if key in found:
                duplicate_embeddings += 1
            else:
                factor["frontier"] = [vertices[position] for position in key]
                found[key] = factor
                if len(found) >= max_matches:
                    raise MatchLimit
            return

        next_role = None
        next_candidates = None
        for role in range(len(ROLE_ORDER)):
            if role in mapping:
                continue
            tick()
            candidates = eligible[role] - used
            for neighbour in sorted(role_adjacency[role]):
                if neighbour in mapping:
                    tick()
                    candidates &= adjacency[mapping[neighbour]]
            if not candidates:
                return
            if next_candidates is None or len(candidates) < len(next_candidates):
                next_role, next_candidates = role, candidates
        for candidate in sorted(next_candidates):
            tick()
            mapping[next_role] = candidate
            used.add(candidate)
            try:
                search()
            finally:
                used.remove(candidate)
                del mapping[next_role]

    try:
        for neighbours in role_adjacency:
            candidates = set()
            for position, original_neighbours in enumerate(adjacency):
                tick()
                if len(original_neighbours) >= len(neighbours):
                    candidates.add(position)
            eligible.append(candidates)
        search()
    except (ScanLimit, MatchLimit):
        return result(False)
    return result(True)
