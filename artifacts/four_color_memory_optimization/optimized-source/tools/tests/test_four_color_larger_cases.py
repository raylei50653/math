"""Structured large-case oracles checked independently on original edges."""

from copy import deepcopy
from itertools import combinations
from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from four_color_larger_cases import (
    ProjectionLimit,
    create_oracle,
    double_wheel_case,
    equality_tree_case,
    generate_cases,
)
from four_color_constraints import solve_constraints
from four_color_lab import graph_fingerprint
from four_color_larger_experiment import (
    validate_random_binding,
    verify_projections,
    verify_reference_witness,
)


def original_edge_solutions(graph):
    """Exhaust original literal assignments, pruning only original edges.

    The enumeration knows nothing about gadgets, hub equalities, tree messages,
    cycle parity, or the supplied oracle descriptor.
    """
    adjacency = {vertex: set() for vertex in graph["vertices"]}
    for left, right in graph["edges"]:
        adjacency[left].add(right)
        adjacency[right].add(left)
    fixed = dict(graph.get("fixed", []))
    order = sorted(graph["vertices"],
                   key=lambda vertex: (vertex not in fixed,
                                       -len(adjacency[vertex]), vertex))
    assignment = {}
    solutions = []

    def visit(offset):
        if offset == len(order):
            solutions.append(dict(assignment))
            return
        vertex = order[offset]
        choices = (fixed[vertex],) if vertex in fixed else range(4)
        for colour in choices:
            if any(assignment.get(neighbor) == colour
                   for neighbor in adjacency[vertex]):
                continue
            assignment[vertex] = colour
            visit(offset + 1)
            del assignment[vertex]

    visit(0)
    return solutions


def direct_witness_valid(graph, colours):
    if (len(colours) != len(graph["vertices"])
            or any(type(colour) is not int or colour not in range(4)
                   for colour in colours)):
        return False
    assignment = dict(zip(graph["vertices"], colours))
    return (all(assignment[left] != assignment[right]
                for left, right in graph["edges"])
            and all(assignment[vertex] == colour
                    for vertex, colour in graph.get("fixed", [])))


class StructuredOracleTests(unittest.TestCase):
    def assert_original_edge_agreement(self, case):
        graph = case["graph"]
        solutions = original_edge_solutions(graph)
        oracle = create_oracle(case)
        self.assertEqual(oracle.solution_count, len(solutions))

        # Include the empty scope: {()} means at least one global extension,
        # while an empty set means none.  Reverse every nontrivial scope so
        # tuple columns cannot accidentally be interpreted in sorted order.
        for width in range(4):
            for scope in combinations(graph["vertices"], width):
                expected = frozenset(tuple(row[vertex] for vertex in scope)
                                     for row in solutions)
                with self.subTest(case=case["name"], scope=scope):
                    self.assertEqual(oracle.projection_count(scope), len(expected))
                    self.assertEqual(oracle.project(scope), expected)
                    if width > 1:
                        self.assertEqual(
                            oracle.project(tuple(reversed(scope))),
                            frozenset(tuple(reversed(row)) for row in expected))

        witnesses = oracle.witnesses(limit=4)
        self.assertEqual(len(witnesses), min(4, len(solutions)))
        self.assertEqual(len({tuple(row) for row in witnesses}), len(witnesses))
        complete = {tuple(row[vertex] for vertex in graph["vertices"])
                    for row in solutions}
        for witness in witnesses:
            self.assertIn(tuple(witness), complete)
            self.assertTrue(direct_witness_valid(graph, witness))
            self.assertTrue(oracle.validate_witness(witness))
        self.assertEqual(oracle.witnesses(limit=0), [])
        return oracle, solutions

    def test_small_chains_match_all_original_solutions_and_width_three_projections(self):
        for edge_count in (1, 2):
            for endpoint in ("compatible", "overlap", "incompatible"):
                case = equality_tree_case("chain", edge_count, endpoint)
                with self.subTest(edge_count=edge_count, endpoint=endpoint):
                    self.assert_original_edge_agreement(case)

    def test_branching_tree_matches_original_edges_in_each_fixed_context(self):
        for endpoint in ("compatible", "overlap", "incompatible"):
            case = equality_tree_case("binary", 2, endpoint)
            with self.subTest(endpoint=endpoint):
                self.assert_original_edge_agreement(case)

    def test_double_wheel_even_and_odd_match_direct_original_edge_enumeration(self):
        for rim_size in (4, 5):
            case = double_wheel_case(rim_size)
            with self.subTest(rim_size=rim_size):
                self.assert_original_edge_agreement(case)

    def test_unsatisfiable_fixed_context_never_produces_projected_rows(self):
        cases = [equality_tree_case("chain", 2, "incompatible"),
                 equality_tree_case("binary", 2, "incompatible"),
                 double_wheel_case(5)]
        for case in cases:
            with self.subTest(case=case["name"]):
                self.assertEqual(original_edge_solutions(case["graph"]), [])
                oracle = create_oracle(case)
                self.assertEqual(oracle.solution_count, 0)
                self.assertEqual(oracle.project(()), frozenset())
                self.assertEqual(oracle.project(case["graph"]["vertices"]),
                                 frozenset())
                self.assertEqual(oracle.witnesses(), [])

    def test_projection_budget_is_explicit_and_does_not_change_exact_oracle(self):
        case = equality_tree_case("chain", 2, "compatible")
        oracle = create_oracle(case)
        scope = tuple(case["graph"]["vertices"])
        complete = oracle.project(scope)
        self.assertGreater(len(complete), 1)
        for cap in (0, 1, len(complete) - 1):
            with self.subTest(max_rows=cap):
                with self.assertRaises(ProjectionLimit):
                    oracle.project(scope, max_rows=cap)
                self.assertEqual(oracle.project(scope), complete)
                self.assertEqual(oracle.solution_count, len(complete))
        self.assertEqual(oracle.project(scope, max_rows=len(complete)), complete)

    def test_original_vertex_order_controls_complete_witness_columns(self):
        case = deepcopy(equality_tree_case("chain", 2, "overlap"))
        case["graph"]["vertices"].reverse()
        self.assert_original_edge_agreement(case)

    def test_repeated_original_ids_retain_repeated_literal_projection_columns(self):
        case = equality_tree_case("binary", 2, "compatible")
        solutions = original_edge_solutions(case["graph"])
        oracle = create_oracle(case)
        vertices = case["graph"]["vertices"]
        scope = (vertices[4], vertices[0], vertices[4], vertices[-1])
        expected = frozenset(tuple(row[vertex] for vertex in scope)
                             for row in solutions)
        self.assertEqual(oracle.project(scope), expected)
        self.assertEqual(oracle.projection_count(scope), len(expected))

    def test_changed_actual_source_or_descriptor_rejects_structural_oracle_claim(self):
        original = equality_tree_case("chain", 2, "compatible")
        variants = {}
        removed = deepcopy(original)
        removed["graph"]["edges"].pop()
        variants["removed-original-edge"] = removed
        added = deepcopy(original)
        added["graph"]["edges"].append([0, 2])
        variants["added-original-hub-edge"] = added
        fixed = deepcopy(original)
        fixed["graph"]["fixed"][0][1] = (fixed["graph"]["fixed"][0][1] + 1) % 4
        variants["changed-original-fixed-color"] = fixed
        tree = deepcopy(original)
        tree["graph"]["source_metadata"]["hub_tree_edges"][0] = [0, 2]
        variants["invalid-metadata-hub-tree"] = tree
        descriptor = deepcopy(original)
        descriptor["oracle"]["common_hub_colours"] = [0, 1, 2]
        variants["fabricated-oracle-descriptor"] = descriptor
        for name, case in variants.items():
            with self.subTest(change=name):
                with self.assertRaises(ValueError):
                    create_oracle(case)


class GeneratedLargeCaseTests(unittest.TestCase):
    def test_all_larger_cases_are_connected_simple_original_graphs_with_exact_witnesses(self):
        cases = generate_cases()
        self.assertEqual(len(cases), 24)
        self.assertEqual(len({case["name"] for case in cases}), len(cases))
        self.assertGreaterEqual(max(len(case["graph"]["vertices"])
                                    for case in cases), 125)
        for case in cases:
            graph = case["graph"]
            vertices = graph["vertices"]
            with self.subTest(case=case["name"]):
                self.assertEqual(len(vertices), len(set(vertices)))
                edges = {frozenset(edge) for edge in graph["edges"]}
                self.assertEqual(len(edges), len(graph["edges"]))
                self.assertTrue(all(len(edge) == 2 and edge <= set(vertices)
                                    for edge in edges))
                adjacency = {vertex: set() for vertex in vertices}
                for left, right in graph["edges"]:
                    adjacency[left].add(right)
                    adjacency[right].add(left)
                reached, pending = set(), [vertices[0]]
                while pending:
                    vertex = pending.pop()
                    if vertex not in reached:
                        reached.add(vertex)
                        pending.extend(adjacency[vertex] - reached)
                self.assertEqual(reached, set(vertices))

                oracle = create_oracle(case)
                witnesses = oracle.witnesses(limit=4)
                self.assertEqual(len(witnesses), min(4, oracle.solution_count))
                self.assertEqual(len({tuple(row) for row in witnesses}), len(witnesses))
                self.assertEqual(oracle.project(()),
                                 frozenset({()}) if oracle.solution_count else frozenset())
                for witness in witnesses:
                    self.assertTrue(direct_witness_valid(graph, witness))
                    self.assertTrue(oracle.validate_witness(witness))
                if witnesses:
                    broken = witnesses[0][:]
                    left, right = graph["edges"][0]
                    left_column, right_column = vertices.index(left), vertices.index(right)
                    broken[right_column] = broken[left_column]
                    self.assertFalse(direct_witness_valid(graph, broken))
                    self.assertFalse(oracle.validate_witness(broken))


class SavedRecordPreservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = equality_tree_case("chain", 2, "overlap")
        cls.graph = cls.case["graph"]
        cls.oracle = create_oracle(cls.case)
        cls.reference = cls.oracle.witnesses(limit=1)[0]
        cls.results = {
            mode: solve_constraints(cls.graph, use_intersections=mode,
                                    use_conflicts=False, use_c5=False,
                                    record_relations=True, trace_limit=5000)
            for mode in (False, True)
        }

    def test_actual_solver_records_preserve_every_global_projection_and_reference(self):
        original = original_edge_solutions(self.graph)
        self.assertGreater(len(original), 1)
        for mode, result in self.results.items():
            with self.subTest(intersections=mode):
                self.assertEqual(result["status"], "colored")
                self.assertFalse(result["trace_truncated"])
                summary = verify_projections(self.oracle, result, 100000)
                self.assertEqual(summary["coverage"], "all_global_solutions_in_saved_records")
                self.assertTrue(summary["complete_projections_checked"])
                self.assertTrue(summary["complete_solver_run"])
                self.assertTrue(summary["trace_complete"])
                self.assertFalse(summary["unsat_preservation_vacuous"])
                self.assertEqual(summary["exact_global_solution_count"], len(original))
                self.assertEqual(summary["projection_limits"], [])
                for kind in ("reduction_domains", "source_domains", "input_relations", "saved_choices"):
                    self.assertGreater(summary["checks"][kind], 0)
                reference = verify_reference_witness(self.graph, result, self.reference)
                self.assertTrue(reference["witness_preserved"])
                self.assertEqual(reference["coverage"], "one_reference_witness_in_saved_records")
                self.assertIsNone(reference["all_solutions_preserved"])

    def test_deleting_a_globally_supported_input_row_or_saved_choice_is_detected(self):
        result = self.results[True]
        # Select witnesses directly from independent original-edge enumeration,
        # rather than relying on the audit helper's choice of projected rows.
        assignment = original_edge_solutions(self.graph)[0]
        missing_input = deepcopy(result)
        relation = next(relation
                        for record in missing_input["elimination_records"]
                        for relation in record["input_relations"])
        row = tuple(assignment[vertex] for vertex in relation["scope"])
        self.assertIn(row, map(tuple, relation["rows"]))
        relation["rows"] = [candidate for candidate in relation["rows"]
                            if tuple(candidate) != row]
        with self.assertRaisesRegex(AssertionError, "input row"):
            verify_projections(self.oracle, missing_input, 100000)

        missing_choice = deepcopy(result)
        record = missing_choice["elimination_records"][0]
        boundary = tuple(assignment[vertex] for vertex in record["scope"])
        saved = next(row for row in record["rows"] if tuple(row["boundary"]) == boundary)
        saved["colors"].remove(assignment[record["vertex"]])
        with self.assertRaisesRegex(AssertionError, "reconstruction choice"):
            verify_projections(self.oracle, missing_choice, 100000)

    def test_zero_projection_budget_reports_partial_coverage_for_a_satisfiable_source(self):
        result = self.results[True]
        summary = verify_projections(self.oracle, result, 0)
        self.assertEqual(result["status"], "colored")
        self.assertEqual(summary["coverage"], "projection_limit_partial")
        self.assertFalse(summary["complete_projections_checked"])
        self.assertTrue(summary["complete_solver_run"])
        self.assertFalse(summary["unsat_preservation_vacuous"])
        self.assertGreater(summary["exact_global_solution_count"], 0)
        self.assertGreater(len(summary["projection_limits"]), 0)
        self.assertTrue(all(entry["rows"] > 0 and entry["limit"] == 0
                            for entry in summary["projection_limits"]))
        self.assertEqual(summary["projection_rows"], 0)
        self.assertTrue(verify_projections(self.oracle, result, 100000)
                        ["complete_projections_checked"])

    def test_independent_reference_witness_detects_domain_row_and_choice_losses(self):
        result = self.results[False]
        self.assertTrue(direct_witness_valid(self.graph, self.reference))
        assignment = dict(zip(self.graph["vertices"], self.reference))
        variants = {}

        reduced = deepcopy(result)
        event = next(event for event in reduced["events"] if event["phase"] == "reduce")
        event["domains"][0].remove(self.reference[0])
        variants["reduction-domain"] = reduced

        source = deepcopy(result)
        entry = source["elimination_records"][0]["source_domains"][0]
        entry["colors"].remove(assignment[entry["vertex"]])
        variants["saved-source-domain"] = source

        missing_input = deepcopy(result)
        relation = missing_input["elimination_records"][0]["input_relations"][0]
        witness_row = tuple(assignment[v] for v in relation["scope"])
        relation["rows"] = [row for row in relation["rows"] if tuple(row) != witness_row]
        variants["input-row"] = missing_input

        missing_choice = deepcopy(result)
        record = missing_choice["elimination_records"][0]
        boundary = tuple(assignment[v] for v in record["scope"])
        saved = next(row for row in record["rows"] if tuple(row["boundary"]) == boundary)
        saved["colors"].remove(assignment[record["vertex"]])
        variants["saved-choice"] = missing_choice

        for kind, damaged in variants.items():
            with self.subTest(loss=kind):
                with self.assertRaises(AssertionError):
                    verify_reference_witness(self.graph, damaged, self.reference)

    def test_frozen_random_reference_rejects_changed_original_edges_and_fixed_frame(self):
        graph = {"vertices": [17, -4, 90], "edges": [[17, -4], [-4, 90]],
                 "fixed": [[17, 0], [-4, 0]]}
        self.assertEqual(original_edge_solutions(graph), [])
        case = {
            "graph": graph,
            "graph_sha256": graph_fingerprint(graph),
            "source_graph_sha256": graph_fingerprint(dict(graph, fixed=[])),
            "reference": {"status": "unsatisfiable", "coverage": "exhaustive_search"},
        }
        self.assertIsNone(validate_random_binding(case))

        missing_edge = deepcopy(case)
        missing_edge["graph"]["edges"].remove([17, -4])
        self.assertGreater(len(original_edge_solutions(missing_edge["graph"])), 0)
        changed_fixed = deepcopy(case)
        changed_fixed["graph"]["fixed"][1][1] = 1
        self.assertGreater(len(original_edge_solutions(changed_fixed["graph"])), 0)
        changed_source_hash = deepcopy(case)
        changed_source_hash["source_graph_sha256"] = "0" * 64
        rehashed_context = deepcopy(missing_edge)
        rehashed_context["graph_sha256"] = graph_fingerprint(rehashed_context["graph"])
        # Rehashing the edited fixed context alone must not hide a stale
        # unfixed-source binding or carry its old UNSAT reference forward.
        for name, damaged in (("original-edge", missing_edge),
                              ("literal-fixed-color", changed_fixed),
                              ("unfixed-source-hash", changed_source_hash),
                              ("context-rehashed-but-source-stale", rehashed_context)):
            with self.subTest(drift=name):
                with self.assertRaises(ValueError):
                    validate_random_binding(damaged)


if __name__ == "__main__":
    unittest.main()
