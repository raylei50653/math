"""Original-edge discovery must add a safe joint factor before elimination.

Reference assignments come only from the frozen original edges and pins.  In
particular, membership in the learned equality is checked against every full
legal assignment, never against a solver-selected witness alone.
"""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_conflict_priority import original_solutions, verify_preservation
import four_color_constraints as constraints
from four_color_joint_constraint_audit import (
    FACTOR_ID, instantiate_nine_point_constraint,
)
from four_color_joint_patterns import find_joint_constraints


def nine_point_graph():
    cases = json.loads((ROOT / "artifacts/four_color_guarantee_gap/inputs.json").read_text())
    return deepcopy(next(case["graph"] for case in cases if case["role"] == "secondary-gap"))


class JointConstraintPropagationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = nine_point_graph()
        cls.graph["fixed"] = []
        cls.solutions = list(original_solutions(cls.graph))
        if len(cls.solutions) != 48:
            raise AssertionError("the frozen unfixed source must have 48 literal solutions")

    def solve(self, graph, **options):
        settings = dict(use_joint_constraints=True, use_substructures=False,
                        use_conflicts=False, use_c5=False, use_cycles=False,
                        use_cycle_contexts=False, use_intersections=False,
                        record_relations=True, trace_limit=10000,
                        max_checks=1_000_000)
        settings.update(options)
        return constraints.solve_constraints(graph, **settings)

    def learned(self, result):
        return [record for record in result["self_constraints"] if record["id"] == FACTOR_ID]

    def joint_events(self, result):
        return [event for event in result["events"]
                if event["kind"] == "structural_constraint"
                and event.get("relation_kind") == "joint_constraint"]

    def assert_no_early_colours(self, graph, result):
        fixed = dict(graph["fixed"])
        expected = [fixed.get(vertex, -1) for vertex in graph["vertices"]]
        for event in result["events"]:
            if event["phase"] == "reduce":
                self.assertEqual(event["colors"], expected)
        self.assertEqual(result["stats"]["decisions"], 0)
        self.assertEqual(result["stats"]["backtracks"], 0)

    def assert_preserved(self, graph, solutions, result):
        audit = verify_preservation(graph, solutions, result)
        self.assertTrue(audit["all_solutions_preserved"])
        self.assertTrue(audit["witness_verified"])
        positions = {vertex: index for index, vertex in enumerate(graph["vertices"])}
        for record in self.learned(result):
            allowed = {tuple(row) for row in record["rows"]}
            for solution in solutions:
                self.assertIn(tuple(solution[positions[vertex]] for vertex in record["frontier"]),
                              allowed)
        for event in self.joint_events(result):
            allowed = {tuple(row["boundary"]) for row in event["relation_preview"]}
            for solution in solutions:
                self.assertIn(tuple(solution[positions[vertex]] for vertex in event["frontier"]),
                              allowed)
        self.assert_no_early_colours(graph, result)

    def test_unequal_frozen_pins_conflict_before_any_elimination(self):
        graph = nine_point_graph()
        before = deepcopy(graph)
        self.assertEqual(list(original_solutions(graph)), [])
        result = self.solve(graph)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertEqual(result["stats"]["writebacks"], 0)
        self.assertEqual(result["elimination_records"], [])
        self.assertEqual(result["stats"]["joint_factors"], 1)
        self.assertEqual(result["stats"]["joint_rows"], 4)
        self.assertTrue(result["joint_scan"]["complete"])
        self.assertEqual(len(self.learned(result)), 1)
        self.assertTrue(any(event["kind"] == "conflict" for event in result["events"]))
        self.assert_no_early_colours(graph, result)
        self.assertEqual(graph, before)

    def test_all_48_solutions_survive_every_domain_input_and_saved_fibre(self):
        graph = deepcopy(self.graph)
        before = deepcopy(graph)
        result = self.solve(graph)
        self.assertEqual(result["status"], "colored")
        self.assert_preserved(graph, self.solutions, result)
        record, = self.learned(result)
        self.assertEqual(record["frontier"], [0, 6, 9])
        self.assertEqual(record["rows"], [[colour] * 3 for colour in range(4)])
        # Every embedding is rechecked through the independently callable
        # original-edge instantiator before it is permitted into propagation.
        instantiated = instantiate_nine_point_constraint(graph, record["role_mapping"])
        self.assertIsNotNone(instantiated)
        self.assertEqual(set(record["source_vertices"]), set(graph["vertices"]))
        self.assertEqual(len(record["source_edges"]), 21)
        self.assertEqual({frozenset(edge) for edge in record["source_edges"]},
                         {frozenset(edge) for edge in graph["edges"]})
        self.assertEqual(record["contract"]["kind"], "NECESSARY_ORIGINAL_SUBGRAPH_RELATION")
        event, = self.joint_events(result)
        self.assertEqual(event["rule"], "C1")
        self.assertEqual(event["depth"], 0)
        self.assertEqual(event["stats"]["eliminations"], 0)
        self.assertEqual(event["frontier"], [0, 6, 9])
        self.assertEqual(event["relation_rows"], 4)
        self.assertEqual({frozenset(edge) for edge in event["causal_edges"]},
                         {frozenset(edge) for edge in graph["edges"]})
        self.assertTrue(any(set(relation["scope"]) == {0, 6, 9}
                            and relation["rows"] == record["rows"]
                            for elimination in result["elimination_records"]
                            for relation in elimination["input_relations"]))
        self.assertEqual(graph, before)

    def test_each_compatible_pin_propagates_all_three_domains_without_writing(self):
        for colour in range(4):
            graph = dict(deepcopy(self.graph), fixed=[[0, colour]])
            solutions = list(original_solutions(graph))
            with self.subTest(colour=colour):
                self.assertEqual(len(solutions), 12)
                result = self.solve(graph)
                self.assert_preserved(graph, solutions, result)
                pre = []
                for event in result["events"]:
                    if event["kind"] == "eliminate":
                        break
                    if event["phase"] == "reduce":
                        pre.append(event)
                self.assertTrue(pre)
                for vertex in (0, 6, 9):
                    self.assertEqual(pre[-1]["domains"][graph["vertices"].index(vertex)], [colour])
                # The unconditional source relation keeps its complete four
                # literal rows even when current domains select only one.
                self.assertEqual(self.learned(result)[0]["rows"],
                                 [[value] * 3 for value in range(4)])

    def test_relabelled_and_shuffled_vertices_still_supply_a_source_witness(self):
        labels = dict(zip(self.graph["vertices"], [501, -21, 14, 770, 88, -402, 39, 7, 2200]))
        graph = dict(vertices=list(reversed([labels[vertex] for vertex in self.graph["vertices"]])),
                     edges=[[labels[right], labels[left]]
                            for left, right in reversed(self.graph["edges"])], fixed=[])
        result = self.solve(graph)
        solutions = list(original_solutions(graph))
        self.assertEqual(len(solutions), 48)
        self.assert_preserved(graph, solutions, result)
        record, = self.learned(result)
        expected = [vertex for vertex in graph["vertices"]
                    if vertex in {labels[0], labels[6], labels[9]}]
        self.assertEqual(record["frontier"], expected)
        self.assertIsNotNone(instantiate_nine_point_constraint(graph, record["role_mapping"]))
        self.assertEqual(self.joint_events(result)[0]["depth"], 0)

    def test_every_missing_original_edge_blocks_the_pattern_and_keeps_a_violating_lift(self):
        positions = {vertex: index for index, vertex in enumerate(self.graph["vertices"])}
        for missing in self.graph["edges"]:
            graph = dict(deepcopy(self.graph),
                         edges=[edge for edge in self.graph["edges"] if edge != missing],
                         fixed=[[0, 0]])
            with self.subTest(missing=missing):
                # Fixing one colour only removes global colour-name symmetry.
                witness = next((row for row in original_solutions(graph)
                                if len({row[positions[vertex]] for vertex in (0, 6, 9)}) > 1), None)
                self.assertIsNotNone(witness)
                scan = find_joint_constraints(graph)
                self.assertEqual(scan["constraints"], [])
                self.assertTrue(scan["complete"])
                pinned = dict(graph, fixed=[list(pair) for pair in zip(graph["vertices"], witness)])
                result = self.solve(pinned)
                self.assertEqual(result["status"], "colored")
                self.assertEqual(result["colors"], witness)
                self.assertEqual(self.learned(result), [])

    def test_zero_discovery_caps_and_disabled_feature_keep_exact_fallback(self):
        graph = nine_point_graph()
        for options in (dict(joint_max_matches=0), dict(joint_max_scan_steps=0),
                        dict(use_joint_constraints=False)):
            with self.subTest(options=options):
                result = self.solve(graph, **options)
                self.assertEqual(result["status"], "unsatisfiable")
                self.assertGreater(result["stats"]["eliminations"], 0)
                self.assertEqual(result["stats"]["joint_factors"], 0)
                self.assertEqual(self.learned(result), [])
                self.assert_no_early_colours(graph, result)
                if options.get("use_joint_constraints", True):
                    self.assertTrue(result["joint_scan"]["truncated"])

    def test_main_work_and_storage_limits_cannot_commit_partial_factors(self):
        graph = deepcopy(self.graph)
        scan_steps = find_joint_constraints(graph)["scan_steps"]
        # Interrupt both discovery and the staging of a factor after two of
        # its four rows; no proper subset may become a learned restriction.
        for maximum in (0, 1, scan_steps, scan_steps + 2):
            with self.subTest(max_checks=maximum):
                result = self.solve(graph, max_checks=maximum)
                self.assertEqual(result["status"], "limit")
                self.assertLessEqual(result["stats"]["checks"], maximum)
                self.assertEqual(result["stats"]["joint_factors"], 0)
                self.assertEqual(self.learned(result), [])
                self.assertEqual(result["colors"], [-1] * 9)
                if maximum < scan_steps:
                    self.assertTrue(result["joint_scan"]["truncated"])
                else:
                    self.assertTrue(result["joint_scan"]["complete"])
                self.assert_no_early_colours(graph, result)
        with patch.object(constraints, "TABLE_ROW_CEILING", 3):
            result = self.solve(graph)
        self.assertEqual(result["status"], "limit")
        self.assertEqual(result["stats"]["joint_factors"], 0)
        self.assertEqual(result["stats"]["joint_rows"], 0)
        self.assertEqual(self.learned(result), [])
        self.assertEqual(self.joint_events(result), [])
        self.assertEqual(result["colors"], [-1] * 9)

    def test_extra_edge_contradicts_the_necessary_relation_before_elimination(self):
        graph = dict(deepcopy(self.graph), edges=self.graph["edges"] + [[0, 6]])
        self.assertEqual(list(original_solutions(graph)), [])
        # Unary GAC alone cannot compare these two unpinned relations.  The
        # existing complete shared-interface mode joins the equality's pair
        # projection with this additional original disequality edge.
        result = self.solve(graph, use_intersections=True)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertTrue(self.learned(result))
        self.assert_no_early_colours(graph, result)

    def test_outside_leaf_keeps_all_144_full_original_solutions(self):
        graph = dict(deepcopy(self.graph), vertices=self.graph["vertices"] + [100],
                     edges=self.graph["edges"] + [[9, 100]])
        graph.pop("positions", None)
        solutions = list(original_solutions(graph))
        self.assertEqual(len(solutions), 144)
        result = self.solve(graph)
        self.assert_preserved(graph, solutions, result)
        record, = self.learned(result)
        self.assertEqual(set(record["source_vertices"]), set(self.graph["vertices"]))
        self.assertEqual(len(record["source_edges"]), 21)
        self.assertFalse(record["contract"]["exact_projection_of_full_target"])

    def test_embeddings_are_deduplicated_and_disjoint_occurrences_are_found(self):
        scan = find_joint_constraints(self.graph)
        self.assertEqual(len(scan["constraints"]), 1)
        self.assertGreater(scan["embeddings"], 1)
        self.assertGreater(scan["duplicate_embeddings"], 0)
        labels = {vertex: vertex + 100 for vertex in self.graph["vertices"]}
        graph = dict(vertices=self.graph["vertices"] + list(labels.values()),
                     edges=self.graph["edges"]
                     + [[labels[left], labels[right]] for left, right in self.graph["edges"]], fixed=[])
        scan = find_joint_constraints(graph)
        self.assertTrue(scan["complete"])
        self.assertEqual({frozenset(record["frontier"]) for record in scan["constraints"]},
                         {frozenset((0, 6, 9)), frozenset((100, 106, 109))})
        capped = find_joint_constraints(graph, max_matches=1)
        self.assertEqual(len(capped["constraints"]), 1)
        self.assertTrue(capped["truncated"])
        factor, = capped["constraints"]
        self.assertIsNotNone(instantiate_nine_point_constraint(graph, factor["role_mapping"]))

    def test_cli_and_invalid_option_validation(self):
        for options in (dict(use_joint_constraints=1), dict(joint_max_matches=-1),
                        dict(joint_max_matches=True), dict(joint_max_scan_steps=-1),
                        dict(joint_max_scan_steps=0.5)):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.solve(self.graph, **options)
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "graph.json", Path(directory) / "result.json"
            source.write_text(json.dumps(nine_point_graph()))
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts/four_color_lab.py"), "solve", str(source),
                 "--engine", "constraints", "--edges-only", "--no-conflicts",
                 "--joint-constraints", "--joint-max-matches", "128",
                 "--joint-max-scan-steps", "200000", "--json", str(output)],
                capture_output=True, text=True, timeout=30)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(output.read_text())
            self.assertEqual(result["status"], "unsatisfiable")
            self.assertEqual(result["stats"]["eliminations"], 0)
            self.assertTrue(result["use_joint_constraints"])
            self.assertEqual(json.loads(completed.stdout)["status"], result["status"])


if __name__ == "__main__":
    unittest.main()
