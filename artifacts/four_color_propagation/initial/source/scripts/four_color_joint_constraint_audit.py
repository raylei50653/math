#!/usr/bin/env python3
"""Record and independently audit one named nine-point common constraint.

The runtime helper requires an explicit role mapping.  It does not scan a graph,
modify domains, commit colors, or integrate with the main solver.  Its factor is
necessary for any target containing the 21 original edges, including targets
with additional edges, vertices, pins, or domains.  It need not be the exact
projection of such a larger or more constrained target.
"""

from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path

from four_color_lab import graph_fingerprint, normalize_graph


ROOT = Path(__file__).resolve().parents[1]
ROLE_ORDER = ("u", "v", "a", "b", "r0", "r1", "r2", "r3", "h")
DEFAULT_ROLE_MAPPING = dict(zip(ROLE_ORDER, (0, 6, 1, 5, 2, 4, 7, 8, 9)))
FRONTIER_ROLES = ("u", "v", "h")
INTERNAL_ROLES = ("a", "b", "r0", "r1", "r2", "r3")
EDGE_GROUPS = {
    "shared_adjacent_pair": (("u", "a"), ("u", "b"), ("v", "a"),
                             ("v", "b"), ("a", "b")),
    "rim_attachments": (("u", "r0"), ("a", "r0"), ("v", "r1"),
                        ("a", "r1"), ("v", "r2"), ("b", "r2"),
                        ("u", "r3"), ("b", "r3")),
    "original_rim": (("r0", "r1"), ("r1", "r2"), ("r2", "r3"),
                     ("r3", "r0")),
    "common_neighbor": (("h", "r0"), ("h", "r1"), ("h", "r2"),
                        ("h", "r3")),
}
REQUIRED_ROLE_EDGES = tuple(edge for group in EDGE_GROUPS.values() for edge in group)
FACTOR_ID = "nine_point_joint_equality_v1"
FROZEN_INPUT = "artifacts/four_color_guarantee_gap/inputs.json"
FROZEN_INPUT_SHA256 = "624fa536d4d2fe060cb024252cfae18c66f928ac2931d8a301b12ccc0104e090"
FIXED_GRAPH_SHA256 = "10eb7febb228531089f53d33ab7a9351c4acbdcb17ea502f5271804b178b5cd7"
UNFIXED_GRAPH_SHA256 = "b2fcb9682b4ccf5be9c106dc3106baaad30d673a5f1a5edc4f2e9541387fd85e"
SOURCE_PATHS = ("scripts/four_color_joint_constraint_audit.py", "scripts/four_color_lab.py",
                "scripts/four_color_serialization.py",
                "tools/tests/test_four_color_joint_constraints.py")


def instantiate_nine_point_constraint(graph, role_mapping):
    """Return the structural necessary relation, or None for a missing edge.

    Mapping keys must be exactly ROLE_ORDER, values must be distinct declared
    integer vertex IDs.  Invalid graphs or mappings raise ValueError.  Extra
    original edges and outside vertices are allowed: this is a non-induced
    subgraph test.  Pins and domains are separate conditions and never remove
    structural rows here; in particular contradictory pins still return all
    four rows.  Neither input object is changed.
    """
    graph = normalize_graph(graph)
    if not isinstance(role_mapping, dict) or set(role_mapping) != set(ROLE_ORDER):
        raise ValueError("role_mapping must contain exactly the nine named roles")
    mapping = {role: role_mapping[role] for role in ROLE_ORDER}
    if any(type(vertex) is not int for vertex in mapping.values()):
        raise ValueError("role IDs must be exact integers")
    if len(set(mapping.values())) != len(ROLE_ORDER):
        raise ValueError("role IDs must be injective")
    if not set(mapping.values()).issubset(graph["vertices"]):
        raise ValueError("every role ID must be an original declared vertex")
    required = sorted(tuple(sorted((mapping[a], mapping[b])))
                      for a, b in REQUIRED_ROLE_EDGES)
    original = {tuple(edge) for edge in graph["edges"]}
    if not set(required).issubset(original):
        return None
    return {
        "id": FACTOR_ID,
        "frontier": [mapping[role] for role in FRONTIER_ROLES],
        "rows": [[color, color, color] for color in range(4)],
        "source_vertices": [mapping[role] for role in ROLE_ORDER],
        "source_edges": [list(edge) for edge in required],
        "role_mapping": mapping,
        "contract": {
            "kind": "NECESSARY_ORIGINAL_SUBGRAPH_RELATION",
            "meaning": "every proper four-coloring of the target restricts to an allowed row",
            "exact_projection_of_template": True,
            "exact_projection_of_full_target": False,
            "induced_subgraph_required": False,
            "fixed_and_domain_conditions_applied": False,
            "literal_color_frame": [0, 1, 2, 3],
            "limitation": "additional target constraints may remove rows or all full extensions",
        },
    }


def original_solutions(graph):
    """Enumerate every literal 4^n tuple; check original edges and pins only.

    This checker does not consult the template, equality formula, or runtime
    factor.  Lists are in the supplied original vertex order.  Fixed colors do
    not reduce its enumeration space, so the reported trial count is literal.
    """
    graph = normalize_graph(graph)
    positions = {vertex: index for index, vertex in enumerate(graph["vertices"])}
    edges = [(positions[a], positions[b]) for a, b in graph["edges"]]
    pins = [(positions[vertex], color) for vertex, color in graph["fixed"]]
    solutions = []
    for colors in product(range(4), repeat=len(positions)):
        if (all(colors[a] != colors[b] for a, b in edges)
                and all(colors[index] == color for index, color in pins)):
            solutions.append(list(colors))
    return solutions, 4 ** len(positions)


def _template_graph(mapping=DEFAULT_ROLE_MAPPING):
    return normalize_graph({
        "vertices": [mapping[role] for role in ROLE_ORDER],
        "edges": [[mapping[a], mapping[b]] for a, b in REQUIRED_ROLE_EDGES],
        "fixed": [],
    })


def _constructed_solutions(vertices, mapping):
    """Construct the 48 template lifts; the literal checker verifies equality."""
    solutions = []
    for common in range(4):
        for a in range(4):
            for b in range(4):
                if len({common, a, b}) != 3:
                    continue
                fourth = next(color for color in range(4) if color not in {common, a, b})
                for rim in ((b, fourth, a, fourth), (fourth, b, fourth, a)):
                    colors = dict(zip(ROLE_ORDER, (common, common, a, b, *rim, common)))
                    assignment = {mapping[role]: colors[role] for role in ROLE_ORDER}
                    solutions.append([assignment[vertex] for vertex in vertices])
    return sorted(solutions)


def _complete_fibres(graph, solutions, frontier, internal):
    positions = {vertex: index for index, vertex in enumerate(graph["vertices"])}
    buckets = {row: [] for row in product(range(4), repeat=len(frontier))}
    for full in solutions:
        row = tuple(full[positions[vertex]] for vertex in frontier)
        buckets[row].append(full)
    return [
        {"row": list(row), "count": len(full_lifts),
         "internal_lifts": [[full[positions[vertex]] for vertex in internal]
                            for full in full_lifts],
         "full_lifts": full_lifts}
        for row, full_lifts in buckets.items()
    ]


def _projection(graph, solutions, frontier):
    positions = {vertex: index for index, vertex in enumerate(graph["vertices"])}
    return sorted({tuple(full[positions[vertex]] for vertex in frontier) for full in solutions})


def _preserved(graph, solutions, factor):
    allowed = {tuple(row) for row in factor["rows"]}
    return sum(row in allowed for row in
               (tuple(full[graph["vertices"].index(vertex)] for vertex in factor["frontier"])
                for full in solutions))


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def _load_frozen_input():
    payload = (ROOT / FROZEN_INPUT).read_bytes()
    if _sha256(payload) != FROZEN_INPUT_SHA256:
        raise AssertionError("frozen input bytes drifted")
    matches = [case for case in json.loads(payload) if case.get("role") == "secondary-gap"]
    if len(matches) != 1:
        raise AssertionError("expected exactly one frozen secondary-gap source")
    case = matches[0]
    fixed = normalize_graph(case["graph"])
    unfixed = normalize_graph(dict(fixed, fixed=[]))
    if (graph_fingerprint(fixed) != FIXED_GRAPH_SHA256
            or case["graph_sha256"] != FIXED_GRAPH_SHA256
            or graph_fingerprint(unfixed) != UNFIXED_GRAPH_SHA256
            or case["source_graph_sha256"] != UNFIXED_GRAPH_SHA256):
        raise AssertionError("frozen literal graph identity drifted")
    template = _template_graph()
    if (set(unfixed["vertices"]) != set(template["vertices"])
            or unfixed["edges"] != template["edges"]
            or len(unfixed["edges"]) != 21):
        raise AssertionError("21-edge template differs from the frozen original graph")
    return case, fixed, unfixed


def audit(out_dir):
    """Write a deterministic finite receipt for this explicitly named pattern."""
    source_bytes = {path: (ROOT / path).read_bytes() for path in SOURCE_PATHS}
    sources = {path: _sha256(data) for path, data in source_bytes.items()}
    frozen_case, fixed, graph = _load_frozen_input()
    factor = instantiate_nine_point_constraint(graph, DEFAULT_ROLE_MAPPING)
    if factor is None:
        raise AssertionError("frozen source did not instantiate the named factor")
    solutions, checked = original_solutions(graph)
    constructed = _constructed_solutions(graph["vertices"], DEFAULT_ROLE_MAPPING)
    if len(solutions) != 48 or sorted(solutions) != constructed:
        raise AssertionError("constructive lifts differ from independent literal enumeration")
    frontier = factor["frontier"]
    internal = [DEFAULT_ROLE_MAPPING[role] for role in INTERNAL_ROLES]
    fibres = _complete_fibres(graph, solutions, frontier, internal)
    expected_rows = [[color, color, color] for color in range(4)]
    if ([row["row"] for row in fibres if row["count"]] != expected_rows
            or [row["count"] for row in fibres if row["count"]] != [12] * 4
            or len(fibres) != 64):
        raise AssertionError("triple frontier must have four nonempty and sixty empty fibres")
    pair_frontier = [DEFAULT_ROLE_MAPPING[role] for role in ("u", "v")]
    pair_internal = [DEFAULT_ROLE_MAPPING[role] for role in (*INTERNAL_ROLES, "h")]
    pair_fibres = _complete_fibres(graph, solutions, pair_frontier, pair_internal)
    if ([row["row"] for row in pair_fibres if row["count"]]
            != [[color, color] for color in range(4)]
            or [row["count"] for row in pair_fibres if row["count"]] != [12] * 4):
        raise AssertionError("pair projection differs from the four equality rows")
    preserved = _preserved(graph, solutions, factor)
    if preserved != len(solutions):
        raise AssertionError("a legal original solution was removed by the factor")
    fixed_solutions, fixed_checked = original_solutions(fixed)
    fixed_factor = instantiate_nine_point_constraint(fixed, DEFAULT_ROLE_MAPPING)
    pins = dict(fixed["fixed"])
    pin_compatible = [row for row in factor["rows"]
                      if all(vertex not in pins or pins[vertex] == color
                             for vertex, color in zip(frontier, row))]
    if fixed_solutions or pin_compatible or fixed_factor != factor:
        raise AssertionError("pins must separately contradict the unchanged structural factor")

    negative_controls = []
    for edge in graph["edges"]:
        weakened = normalize_graph(dict(graph, edges=[e for e in graph["edges"] if e != edge]))
        if instantiate_nine_point_constraint(weakened, DEFAULT_ROLE_MAPPING) is not None:
            raise AssertionError("the 21-edge guard accepted a missing required edge")
        weakened_solutions, trials = original_solutions(weakened)
        u_index, v_index = (graph["vertices"].index(DEFAULT_ROLE_MAPPING[role])
                            for role in ("u", "v"))
        witness = next((full for full in weakened_solutions if full[u_index] != full[v_index]), None)
        if witness is None:
            raise AssertionError("edge deletion did not admit the required unequal witness")
        negative_controls.append({
            "removed_edge": edge, "candidate_rows_checked": trials,
            "solution_count": len(weakened_solutions), "runtime_factor": None,
            "unequal_uv_witness": witness,
            "witness_vertex_order": graph["vertices"],
        })

    relabeling = {vertex: 100 - 3 * index for index, vertex in enumerate(graph["vertices"])}
    relabeled = normalize_graph({
        "vertices": [relabeling[vertex] for vertex in reversed(graph["vertices"])],
        "edges": [[relabeling[a], relabeling[b]] for a, b in graph["edges"]], "fixed": [],
    })
    mapped_roles = {role: relabeling[vertex] for role, vertex in DEFAULT_ROLE_MAPPING.items()}
    relabeled_factor = instantiate_nine_point_constraint(relabeled, mapped_roles)
    relabeled_solutions, relabeled_checked = original_solutions(relabeled)
    if (relabeled_factor is None or len(relabeled_solutions) != 48
            or _preserved(relabeled, relabeled_solutions, relabeled_factor) != 48):
        raise AssertionError("the factor did not survive original-ID and vertex-order changes")

    outside_vertex = max(graph["vertices"]) + 1
    outside = normalize_graph({
        "vertices": [*graph["vertices"], outside_vertex],
        "edges": [*graph["edges"], [DEFAULT_ROLE_MAPPING["u"], outside_vertex]], "fixed": [],
    })
    outside_factor = instantiate_nine_point_constraint(outside, DEFAULT_ROLE_MAPPING)
    outside_solutions, outside_checked = original_solutions(outside)
    if (outside_factor != factor or len(outside_solutions) != 144
            or _preserved(outside, outside_solutions, factor) != 144):
        raise AssertionError("outside-vertex control lost valid extensions")

    extra = normalize_graph(dict(graph, edges=[*graph["edges"], pair_frontier]))
    extra_factor = instantiate_nine_point_constraint(extra, DEFAULT_ROLE_MAPPING)
    extra_solutions, extra_checked = original_solutions(extra)
    if extra_factor != factor or extra_solutions:
        raise AssertionError("extra u-v edge must make the target empty, leaving the necessary factor")

    inputs = {
        "frozen_input": {"path": FROZEN_INPUT, "sha256": FROZEN_INPUT_SHA256},
        "frozen_case": frozen_case,
        "unfixed_original_graph": graph,
        "unfixed_original_graph_sha256": UNFIXED_GRAPH_SHA256,
        "pattern": {"id": FACTOR_ID, "role_order": ROLE_ORDER,
                    "role_mapping": DEFAULT_ROLE_MAPPING, "edge_groups": EDGE_GROUPS,
                    "required_role_edges": REQUIRED_ROLE_EDGES,
                    "required_vertex_count": 9, "required_edge_count": 21},
        "conditions": {"structural_factor": {"fixed": [], "domains": []},
                       "frozen_literal_test": {"fixed": fixed["fixed"]}},
    }
    relation = {
        "factor": factor, "source_vertex_order": graph["vertices"],
        "frontier_role_order": FRONTIER_ROLES,
        "internal_role_order": INTERNAL_ROLES, "internal_vertex_order": internal,
        "fibres": fibres, "all_full_lifts": solutions,
        "pair_uv_projection": {"frontier": pair_frontier,
                               "internal_role_order": (*INTERNAL_ROLES, "h"),
                               "internal_vertex_order": pair_internal, "fibres": pair_fibres},
        "constructive_description": {
            "u_v_h": "one common color t",
            "a_b": "ordered distinct colors different from t; d is the fourth color",
            "rim_orders_r0_r1_r2_r3": [["b", "d", "a", "d"], ["d", "b", "d", "a"]],
            "all_full_lifts": constructed,
        },
    }
    report = {
        "status": "FINITE_NAMED_PATTERN_AUDIT",
        "method": "independent itertools.product(range(4), repeat=n); original edges and literal pins only",
        "no_main_solver_integration": True, "no_automatic_pattern_scan": True,
        "source_hashes": sources,
        "input_hashes": {FROZEN_INPUT: FROZEN_INPUT_SHA256},
        "fixed_graph_sha256": FIXED_GRAPH_SHA256,
        "unfixed_graph_sha256": UNFIXED_GRAPH_SHA256,
        "template_exactly_matches_frozen_original_edges": True,
        "unfixed": {"candidate_rows_checked": checked, "solution_count": len(solutions),
                    "frontier": frontier, "relation_rows": expected_rows,
                    "complete_fibres": 64, "nonempty_fibres": 4, "empty_fibres": 60,
                    "lifts_per_nonempty_fibre": 12, "all_original_solutions_preserved": preserved,
                    "constructive_and_independent_full_lifts_match": True},
        "fixed_literal_test": {"fixed": fixed["fixed"], "candidate_rows_checked": fixed_checked,
                               "solution_count": len(fixed_solutions),
                               "structural_rows_unchanged": True,
                               "pin_compatible_rows": pin_compatible},
        "single_edge_deletion_controls": negative_controls,
        "relabel_control": {"vertex_relabeling": [[v, relabeling[v]] for v in graph["vertices"]],
                            "graph": relabeled, "factor": relabeled_factor,
                            "candidate_rows_checked": relabeled_checked,
                            "solution_count": 48, "all_solutions_preserved": True},
        "outside_leaf_control": {"graph": outside, "factor": outside_factor,
                                 "candidate_rows_checked": outside_checked,
                                 "solution_count": 144, "all_solutions_preserved": True},
        "extra_edge_control": {"added_edge": pair_frontier, "graph": extra,
                               "factor": extra_factor, "candidate_rows_checked": extra_checked,
                               "solution_count": 0,
                               "full_target_projection": _projection(extra, extra_solutions, frontier),
                               "structural_factor_rows_unchanged": True},
        "boundary": "necessary relation for this named original-edge pattern only; no general propagation or graph-coloring completeness claim",
    }
    outputs = {"inputs.json": inputs, "relation.json": relation, "report.json": report}
    encoded = {name: _encoded(value) for name, value in outputs.items()}
    if any((ROOT / path).read_bytes() != data for path, data in source_bytes.items()):
        raise AssertionError("producer or direct dependency changed during audit")
    verification = {
        "status": "PASS", "source_hashes": sources,
        "output_hashes": {name: _sha256(data) for name, data in sorted(encoded.items())},
        "frozen_input_sha256": FROZEN_INPUT_SHA256,
        "literal_template_trials": checked,
        "negative_controls": len(negative_controls),
        "all_21_single_edge_deletions_admit_unequal_uv": True,
        "complete_triple_fibres_including_empty": 64,
        "complete_pair_fibres_including_empty": 16,
        "runtime_factor_separate_from_literal_conditions": True,
        "source_snapshot": "baseline-source/",
    }
    encoded["verification.json"] = _encoded(verification)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, data in encoded.items():
        (out_dir / name).write_bytes(data)
    for path, data in source_bytes.items():
        destination = out_dir / "baseline-source" / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "artifacts/four_color_joint_constraints")
    args = parser.parse_args()
    report = audit(args.out_dir)
    print(json.dumps({"status": report["status"], "out_dir": str(args.out_dir),
                      "relation_rows": report["unfixed"]["relation_rows"],
                      "solution_count": report["unfixed"]["solution_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
