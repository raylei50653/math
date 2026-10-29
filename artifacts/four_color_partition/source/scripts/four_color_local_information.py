"""Bounded audit of exact local interfaces and structural cycle propagation.

Only Python's standard library is used.  The cycle algorithm does not build or
query a colouring table: it preserves the anchor colour while processing the
path, then checks the original closing edge.  The finite audit has an independent
literal-assignment oracle and does not establish a general graph-colouring
theorem or a source-realisation claim.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random


PALETTE = tuple(range(4))


def _masks(domain_masks, minimum):
    try:
        masks = list(domain_masks)
    except TypeError as exc:
        raise ValueError("domain_masks must be an iterable of masks") from exc
    if len(masks) < minimum or any(type(mask) is not int or not 0 <= mask <= 15
                                   for mask in masks):
        raise ValueError(f"requires at least {minimum} masks, each an integer in 0..15")
    return masks


def _colours(mask):
    return [colour for colour in PALETTE if mask & (1 << colour)]


def path_endpoint_relation(domain_masks):
    """Return the complete literal first/last relation of a nonempty path.

    Counts include every path colouring.  One complete internal lift is kept
    for each nonempty endpoint fibre; these examples do not enumerate all lifts.
    At most sixteen endpoint pairs are live, independent of path length.
    """
    masks = _masks(domain_masks, 1)
    counts = [[0] * 4 for _ in PALETTE]
    witnesses = {}
    for anchor in _colours(masks[0]):
        current_counts = [int(colour == anchor) for colour in PALETTE]
        predecessors = []
        for mask in masks[1:]:
            next_counts = [0] * 4
            previous_by_colour = [None] * 4
            for colour in _colours(mask):
                next_counts[colour] = sum(current_counts[previous]
                                          for previous in PALETTE if previous != colour)
                previous = next((previous for previous in PALETTE
                                 if previous != colour and current_counts[previous]), None)
                previous_by_colour[colour] = previous
            predecessors.append(previous_by_colour)
            current_counts = next_counts
        counts[anchor] = current_counts
        for last in PALETTE:
            if current_counts[last]:
                path = [last]
                for previous_by_colour in reversed(predecessors):
                    path.append(previous_by_colour[path[-1]])
                witnesses[(anchor, last)] = list(reversed(path))
    rows = [[first, last] for first in PALETTE for last in PALETTE
            if counts[first][last]]
    return {"rows": rows, "counts": counts, "state_count": len(rows),
            "state_capacity": 16, "domain_masks": masks,
            "witness_by_endpoints": [
                {"boundary": row, "colors": witnesses[tuple(row)]} for row in rows],
            "relation_contract": "exact endpoint relation of this path under these literal domains; witnesses are one lift per nonempty fibre"}


def derive_cycle(domain_masks, *, charge=None):
    """Compute exact unary supports and row count on any cycle of length >=3.

    Forward and backward support sets are joined only at the same position and
    the same anchor.  A charged callback runs before every counted DP stage;
    exceptions propagate without mutating the supplied domain sequence.
    ``witness`` is one full cycle assignment, or None for an empty relation.
    """
    masks = _masks(domain_masks, 3)
    if charge is not None and not callable(charge):
        raise ValueError("charge must be callable")
    size = len(masks)
    supports = [0] * size
    row_count = 0
    anchor_cases = []
    witness = None
    op_count = 0

    def step():
        nonlocal op_count
        if charge is not None:
            charge()
        op_count += 1

    for anchor in _colours(masks[0]):
        step()
        anchor_bit = 1 << anchor
        counts = [int(colour == anchor) for colour in PALETTE]
        forward = [anchor_bit] + [0] * (size - 1)
        for position in range(1, size):
            step()
            total = sum(counts)
            counts = [total - counts[colour] if masks[position] & (1 << colour)
                      else 0 for colour in PALETTE]
            forward[position] = sum(1 << colour for colour in PALETTE if counts[colour])
        step()
        case_count = sum(counts[colour] for colour in PALETTE if colour != anchor)
        backward = [0] * size
        backward[-1] = masks[-1] & (15 ^ anchor_bit)
        for position in range(size - 2, -1, -1):
            step()
            following = backward[position + 1]
            compatible = (15 if following.bit_count() >= 2 else
                          15 ^ following if following else 0)
            backward[position] = (anchor_bit if position == 0 else masks[position]) & compatible
        for position in range(size):
            step()
            supports[position] |= forward[position] & backward[position]
        row_count += case_count
        anchor_cases.append({"anchor": anchor, "row_count": case_count,
                             "forward_masks": forward, "backward_masks": backward})
        if case_count and witness is None:
            path = [anchor]
            for position in range(1, size):
                step()
                allowed = backward[position] & (15 ^ (1 << path[-1]))
                path.append(_colours(allowed)[0])
            witness = path
    return {"supports": supports, "row_count": row_count, "witness": witness,
            "anchor_cases": anchor_cases, "op_count": op_count,
            "method": "anchored-forward-backward-cycle", "state_capacity": 16,
            "domain_masks": masks,
            "relation_contract": "exact supports and count for these cyclic inequalities and literal domains; unary supports are not their joint relation"}


def _graph_data(graph):
    if not isinstance(graph, dict):
        raise ValueError("graph must contain vertices and edges")
    try:
        vertices = list(graph["vertices"])
        edges = [list(edge) for edge in graph["edges"]]
    except (KeyError, TypeError) as exc:
        raise ValueError("graph must contain vertices and edge pairs") from exc
    if (any(type(vertex) is not int for vertex in vertices)
            or len(vertices) != len(set(vertices))):
        raise ValueError("vertices must be unique integer ids")
    vertex_set = set(vertices)
    for edge in edges:
        if (len(edge) != 2 or any(type(vertex) is not int or vertex not in vertex_set
                                for vertex in edge) or edge[0] == edge[1]):
            raise ValueError("edges must join two distinct original vertex ids")
    if len({frozenset(edge) for edge in edges}) != len(edges):
        raise ValueError("duplicate original edges are not allowed")
    return vertices, edges


def validate_separator(graph, interior, boundary):
    """Check that every attachment from the eliminated interior is retained.

    An edge from ``interior`` to a vertex outside ``interior | boundary`` is an
    escaping original edge.  Invalid id sets raise ValueError; a well-formed but
    incomplete separator returns valid=False and the original escaping edges.
    """
    vertices, edges = _graph_data(graph)
    try:
        interior, boundary = list(interior), list(boundary)
    except TypeError as exc:
        raise ValueError("interior and boundary must be iterables of vertex ids") from exc
    for scope in (interior, boundary):
        if (any(type(vertex) is not int or vertex not in vertices for vertex in scope)
                or len(scope) != len(set(scope))):
            raise ValueError("interior and boundary must contain unique original vertex ids")
    private, interface = set(interior), set(boundary)
    if private & interface:
        raise ValueError("interior and boundary must be disjoint")
    retained = private | interface
    escaping = [edge for edge in edges
                if (edge[0] in private and edge[1] not in retained)
                or (edge[1] in private and edge[0] not in retained)]
    return {"valid": not escaping, "escaping_edges": escaping,
            "interior": interior, "boundary": boundary,
            "source_vertices": vertices, "source_edges": edges}


def _original_rows(graph, domain_masks=None):
    """Independent audit oracle: enumerate assignments and check original edges."""
    vertices, edges = _graph_data(graph)
    masks = [15] * len(vertices) if domain_masks is None else _masks(domain_masks, 0)
    if len(masks) != len(vertices):
        raise ValueError("one domain mask is required per original vertex")
    positions = {vertex: index for index, vertex in enumerate(vertices)}
    edge_positions = [(positions[first], positions[second]) for first, second in edges]
    return [row for row in product(*(_colours(mask) for mask in masks))
            if all(row[first] != row[second] for first, second in edge_positions)]


def _source_record(graph, domain_masks=None):
    vertices, edges = _graph_data(graph)
    masks = [15] * len(vertices) if domain_masks is None else list(domain_masks)
    source = {"vertices": vertices, "edges": edges,
              "domain_scope": vertices[:], "domain_masks": masks,
              "palette": list(PALETTE)}
    source["sha256"] = sha256(json.dumps(source, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return source


def _interface(graph, boundary, all_rows=None):
    vertices, _ = _graph_data(graph)
    boundary = list(boundary)
    interior = [vertex for vertex in vertices if vertex not in boundary]
    index = {vertex: position for position, vertex in enumerate(vertices)}
    rows = _original_rows(graph) if all_rows is None else all_rows
    fibres = {row: [] for row in product(PALETTE, repeat=len(boundary))}
    for row in rows:
        key = tuple(row[index[vertex]] for vertex in boundary)
        fibres[key].append([row[index[vertex]] for vertex in interior])
    return {"source": _source_record(graph), "boundary": boundary, "interior": interior,
            "rows": [list(row) for row, lifts in fibres.items() if lifts],
            "row_count": sum(bool(lifts) for lifts in fibres.values()),
            "original_coloring_count": len(rows),
            "fibres": [{"boundary": list(row), "lifts": lifts}
                       for row, lifts in fibres.items()],
            "relation_contract": "complete boundary relation and all interior lifts, including empty fibres, from this one original graph and literal frame"}


def _projection_closures(rows, arity):
    relation = {tuple(row) for row in rows}
    size = len(next(iter(relation))) if relation else arity
    scopes = [scope for width in range(1, arity + 1)
              for scope in combinations(range(size), width)]
    projections = {scope: {tuple(row[index] for index in scope) for row in relation}
                   for scope in scopes}
    closure = {row for row in product(PALETTE, repeat=size)
               if all(tuple(row[index] for index in scope) in values
                      for scope, values in projections.items())}
    return {"maximum_projection_arity": arity,
            "projection_scopes": [list(scope) for scope in scopes],
            "projections": [{"scope": list(scope), "rows": [list(row) for row in sorted(values)]}
                            for scope, values in projections.items()],
            "closure_row_count": len(closure),
            "false_row_count": len(closure - relation),
            "false_rows": [list(row) for row in sorted(closure - relation)]}


def _cycle_audit():
    rng = random.Random(20261025)
    cases = []
    for size in range(3, 11):
        contexts = [("full_four", [15] * size), ("full_three", [7] * size),
                    ("common_two", [3] * size),
                    ("unique_escape", [7] + [3] * (size - 1)),
                    ("adjacent_same_fixed", [1, 1] + [15] * (size - 2)),
                    ("empty_domain", [0] + [15] * (size - 1))]
        contexts += [(f"seeded_{index:02d}", [rng.randrange(16) for _ in range(size)])
                     for index in range(12)]
        graph = {"vertices": list(range(size)),
                 "edges": [[index, (index + 1) % size] for index in range(size)]}
        for name, masks in contexts:
            result = derive_cycle(masks)
            rows = _original_rows(graph, masks)
            oracle_supports = [0] * size
            for row in rows:
                for index, colour in enumerate(row):
                    oracle_supports[index] |= 1 << colour
            witness = result["witness"]
            witness_valid = (witness is None if not rows else
                             witness is not None and tuple(witness) in set(rows))
            matched = (result["supports"] == oracle_supports
                       and result["row_count"] == len(rows) and witness_valid)
            if not matched:
                raise AssertionError((size, name, masks, result, oracle_supports, len(rows)))
            if name in ("full_four", "full_three", "common_two"):
                colour_count = {"full_four": 4, "full_three": 3, "common_two": 2}[name]
                formula = (colour_count - 1) ** size + (colour_count - 1) * (-1) ** size
                if len(rows) != formula:
                    raise AssertionError("cycle counting control failed")
            cases.append({"name": name, "length": size,
                          "source": _source_record(graph, masks),
                          "supports": result["supports"], "row_count": result["row_count"],
                          "witness": witness, "anchor_cases": result["anchor_cases"],
                          "op_count": result["op_count"],
                          "independent_oracle_row_count": len(rows),
                          "independent_oracle_supports": oracle_supports,
                          "witness_valid": witness_valid, "matched": matched})
    seven = {"vertices": list(range(7)),
             "edges": [[index, (index + 1) % 7] for index in range(7)]}
    domains = [set((0, 1)) for _ in range(7)]
    changed = True
    while changed:
        changed = False
        for first, second in seven["edges"]:
            for vertex, neighbour in ((first, second), (second, first)):
                kept = {colour for colour in domains[vertex]
                        if any(colour != other for other in domains[neighbour])}
                changed |= kept != domains[vertex]
                domains[vertex] = kept
    six = {"vertices": list(range(6)),
           "edges": [[index, (index + 1) % 6] for index in range(6)]}
    chorded_six = {"vertices": six["vertices"], "edges": six["edges"] + [[0, 2]]}
    bare_six_rows = _original_rows(six, [3] * 6)
    chorded_six_rows = _original_rows(chorded_six, [3] * 6)
    if len(bare_six_rows) != 2 or chorded_six_rows:
        raise AssertionError("original chord control failed")
    return {"lengths": list(range(3, 11)), "seed": 20261025,
            "case_count": len(cases), "mismatches": 0, "cases": cases,
            "scope": "finite selected-domain correctness controls; not exhaustive over all cycle lengths or domains",
            "unary_propagation_negative_control": {
                "source": _source_record(seven, [3] * 7),
                "edge_arc_consistent_domains": [sorted(domain) for domain in domains],
                "anchored_cycle_rows": derive_cycle([3] * 7)["row_count"],
                "claim": "edge arc consistency retains both colours at every vertex while the original two-colour odd cycle has no colouring"},
            "original_chord_negative_control": {
                "bare_cycle_source": _source_record(six, [3] * 6),
                "chorded_original_source": _source_record(chorded_six, [3] * 6),
                "bare_cycle_rows": [list(row) for row in bare_six_rows],
                "bare_cycle_supports": derive_cycle([3] * 6)["supports"],
                "chorded_original_rows": [], "extra_original_edge": [0, 2],
                "claim": "the two bare-cycle witnesses violate the original chord; exact cycle support is only a necessary consequence when the source has additional edges"}}


def build_report():
    """Produce deterministic finite evidence with full named source contexts."""
    star = {"vertices": list(range(5)), "edges": [[0, leaf] for leaf in range(1, 5)]}
    star_relation = _interface(star, [1, 2, 3, 4])
    star_relation["projection_audits"] = [
        _projection_closures(star_relation["rows"], arity) for arity in range(1, 4)]
    if star_relation["row_count"] != 232 or any(
            item["closure_row_count"] != 256 or item["false_row_count"] != 24
            for item in star_relation["projection_audits"]):
        raise AssertionError("four-leaf star control failed")

    wheel = {"vertices": list(range(6)),
             "edges": [[index, (index + 1) % 5] for index in range(5)]
                      + [[5, index] for index in range(5)]}
    wheel_relation = _interface(wheel, list(range(5)))
    wheel_relation["projection_audits"] = [
        _projection_closures(wheel_relation["rows"], arity) for arity in range(1, 4)]
    triple = wheel_relation["projection_audits"][-1]
    if (wheel_relation["row_count"] != 120 or triple["closure_row_count"] != 240
            or triple["false_row_count"] != 120):
        raise AssertionError("five-wheel triple-projection control failed")

    boundary = [0, 1, 2, 3]
    host = {"vertices": list(range(6)),
            "edges": [[center, leaf] for center in (4, 5) for leaf in boundary]}
    left = {"vertices": boundary + [4], "edges": host["edges"][:4]}
    right = {"vertices": boundary + [5], "edges": host["edges"][4:]}
    left_relation, right_relation = _interface(left, boundary), _interface(right, boundary)
    left_fibres = {tuple(item["boundary"]): item["lifts"] for item in left_relation["fibres"]}
    right_fibres = {tuple(item["boundary"]): item["lifts"] for item in right_relation["fibres"]}
    joined = {assignment + tuple(first) + tuple(second)
              for assignment in product(PALETTE, repeat=4)
              for first in left_fibres[assignment] for second in right_fibres[assignment]}
    original = set(_original_rows(host))
    if joined != original or len(original) != 516:
        raise AssertionError("same-source interface join failed")
    actual_interface = _interface(host, boundary, sorted(original))
    shared_rows = (set(map(tuple, left_relation["rows"]))
                   & set(map(tuple, right_relation["rows"])))
    if shared_rows != set(map(tuple, actual_interface["rows"])) or len(shared_rows) != 232:
        raise AssertionError("same-source boundary intersection failed")

    escaped = {"vertices": host["vertices"], "edges": host["edges"] + [[4, 5]]}
    invalid = validate_separator(escaped, [4], boundary)
    repaired = validate_separator(escaped, [4], boundary + [5])
    escaped_original = set(_original_rows(escaped))
    if (invalid["valid"] or invalid["escaping_edges"] != [[4, 5]]
            or not repaired["valid"] or len(escaped_original) != 192):
        raise AssertionError("escaping-original-edge control failed")
    join = {"source": _source_record(host), "boundary": boundary,
            "regions": [left_relation, right_relation],
            "separator_checks": [validate_separator(host, [4], boundary),
                                 validate_separator(host, [5], boundary)],
            "exact_global_interface": actual_interface,
            "joined_original_assignments": [list(row) for row in sorted(joined)],
            "full_original_assignment_count": len(original),
            "joined_assignment_count": len(joined), "matched": joined == original,
            "boundary_intersection_count": len(shared_rows),
            "negative_cross_private_edge": {
                "source": _source_record(escaped), "invalid_separator": invalid,
                "enlarged_separator": repaired, "join_permitted": invalid["valid"],
                "actual_original_assignment_count": len(escaped_original),
                "incorrect_join_if_edge_were_ignored_count": len(joined),
                "false_assignments_if_edge_were_ignored": [list(row) for row in sorted(joined - escaped_original)],
                "claim": "the original center-center edge escapes the four-leaf interface; include the other center in the interface before eliminating this center"}}
    return {"version": "four-colour-local-information-v1", "palette": list(PALETTE),
            "script_source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "source_file": "scripts/four_color_local_information.py",
            "named_bounded_claims": [
                "One four-leaf star loses 24 forbidden interface rows after retaining every projection of arity at most three.",
                "One planar five-wheel has 120 exact boundary rows; joining every projection of arity at most three admits 240 rows.",
                "Anchored structural cycle propagation matches independent original-edge enumeration on the recorded lengths and domain contexts.",
                "For the recorded two-colour six-cycle, the original chord [0,2] rejects both bare-cycle witnesses.",
                "For the recorded two-star host, full common-interface relations and Cartesian interior fibres recover exactly the original assignments.",
                "An original edge between private centers invalidates the four-leaf separator; enlarging the interface retains that attachment."],
            "not_claimed": ["bounded arity is insufficient for every possible structural encoding",
                            "a fixed separator bound for arbitrary planar graphs",
                            "new source realisation, source coverage, or general graph exclusion"],
            "four_leaf_star": star_relation, "five_wheel": wheel_relation,
            "cycle_controls": _cycle_audit(), "same_source_join": join}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path,
                        default=Path("artifacts/four_color_local_information/report.json"))
    args = parser.parse_args(argv)
    report = build_report()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({"out": str(args.out),
                      "star_rows": report["four_leaf_star"]["row_count"],
                      "wheel_rows": report["five_wheel"]["row_count"],
                      "cycle_cases": report["cycle_controls"]["case_count"],
                      "cycle_mismatches": report["cycle_controls"]["mismatches"],
                      "same_source_join_rows": report["same_source_join"]["joined_assignment_count"],
                      "script_source_sha256": report["script_source_sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
