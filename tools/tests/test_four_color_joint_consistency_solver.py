"""End-to-end correctness and budget boundaries of joint consistency."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_color_constraints import solve_constraints
from four_color_joint_consistency import joint_supports
from test_four_color_joint_consistency import initial_factors, original_solutions


class JointConsistencySolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = json.loads((ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f/"
                                 "propagation/inputs.json").read_text())

    def check_witness(self, graph, colors):
        self.assertEqual(len(colors), len(graph["vertices"]))
        self.assertTrue(all(type(c) is int and c in range(4) for c in colors))
        assignment = dict(zip(graph["vertices"], colors))
        self.assertTrue(all(assignment[u] != assignment[v] for u, v in graph["edges"]))
        self.assertTrue(all(assignment[v] == c for v, c in graph.get("fixed", [])))

    def test_fixed_gap_is_rejected_by_initial_propagation_before_any_bucket(self):
        graph = self.inputs["graph"]
        options = dict(self.inputs["options"], use_joint_consistency=True)
        initial = initial_factors(graph, options)
        self.assertFalse(initial["consistent"])
        self.assertEqual(initial["stats"]["candidate_checks"], 0)
        result = solve_constraints(graph, **options)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(result["elimination_records"], [])
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertEqual(result["stats"]["writebacks"], 0)
        self.assertEqual(result["stats"]["candidate_checks"], 0)
        self.assertGreater(result["stats"]["joint_consistency_checks"], 0)
        self.assertEqual(result["stats"]["joint_consistency_queries"], 0)
        self.assertGreater(result["stats"]["triangle_equality_checks"], 0)
        conflicts = [event for event in result["events"] if event["kind"] == "conflict"]
        self.assertEqual(conflicts[0]["propagation_kind"], "triangle_equalities")
        self.assertTrue(conflicts[0]["structural_proof"])
        original_edges = {frozenset(edge) for edge in graph["edges"]}
        self.assertTrue(all(frozenset(edge) in original_edges
                            for edge in conflicts[0]["causal_edges"]))
        fixed = dict(graph["fixed"])
        self.assertEqual(result["colors"], [fixed.get(v, -1) for v in graph["vertices"]])

    def test_bare_graph_preserves_every_solution_and_learns_the_pair_relation(self):
        graph = dict(self.inputs["graph"], fixed=[])
        solutions = list(original_solutions(graph))
        self.assertEqual(len(solutions), 624)
        options = dict(self.inputs["options"], use_joint_consistency=True)
        initial = initial_factors(graph, options)
        self.assertTrue(initial["consistent"])
        expected_pair = {(a, b) for a in range(4) for b in range(4) if a != b}
        pair_relations = [{(row[scope.index(9)], row[scope.index(11)]) for row in rows}
                          for scope, rows in initial["factors"] if 9 in scope and 11 in scope]
        self.assertIn(expected_pair, pair_relations)
        result = solve_constraints(graph, **options)
        self.assertEqual(result["status"], "colored")
        self.check_witness(graph, result["colors"])
        self.assertLessEqual(result["stats"]["joint_consistency_checks"], 200000)
        self.assertGreater(result["stats"]["joint_consistency_row_prunes"], 0)
        self.assertGreater(result["stats"]["joint_consistency_incomplete"], 0)
        for event in result["events"]:
            if event["phase"] != "reduce":
                continue
            self.assertEqual(event["colors"], [-1] * len(graph["vertices"]))
            for coloring in solutions:
                self.assertTrue(all(coloring[v] in values for v, values
                                    in zip(graph["vertices"], event["domains"])))
        original_edges = {frozenset(edge) for edge in graph["edges"]}
        for record in result["elimination_records"]:
            fibers = {tuple(row["boundary"]): set(row["colors"]) for row in record["rows"]}
            source_domains = {row["vertex"]: row["colors"] for row in record["source_domains"]}
            relations = [(relation["scope"], set(map(tuple, relation["rows"])))
                         for relation in record["input_relations"]]
            self.assertTrue(all(frozenset(edge) in original_edges for edge in record["source_edges"]))
            for coloring in solutions:
                self.assertTrue(all(coloring[v] in domain for v, domain in source_domains.items()))
                self.assertIn(coloring[record["vertex"]],
                              fibers[tuple(coloring[v] for v in record["scope"])])
                self.assertTrue(all(tuple(coloring[v] for v in columns) in rows
                                    for columns, rows in relations))

    def test_zero_optional_budget_skips_join_without_changing_exact_result(self):
        graph = self.inputs["graph"]
        options = self.inputs["options"]
        old = solve_constraints(graph, **options)
        result = solve_constraints(graph, **dict(options, use_joint_consistency=True,
                                                 joint_consistency_max_checks=0))
        self.assertEqual(result["status"], old["status"])
        self.assertEqual(result["colors"], old["colors"])
        self.assertEqual(result["elimination_records"], old["elimination_records"])
        self.assertEqual(result["stats"]["checks"], old["stats"]["checks"])
        self.assertEqual(result["stats"]["joint_consistency_checks"], 0)
        self.assertGreater(result["stats"]["candidate_checks"], 0)

    def test_total_optional_budget_is_bounded_and_partial_query_is_discarded(self):
        graph = self.inputs["graph"]
        old = solve_constraints(graph, **self.inputs["options"])
        result = solve_constraints(graph, **dict(self.inputs["options"],
                                                 use_joint_consistency=True,
                                                 joint_consistency_max_checks=20))
        self.assertEqual(result["status"], old["status"])
        self.assertEqual(result["elimination_records"], old["elimination_records"])
        self.assertEqual(result["stats"]["joint_consistency_checks"], 20)
        self.assertEqual(result["stats"]["joint_consistency_incomplete"], 1)
        self.assertEqual(result["stats"]["joint_consistency_row_prunes"], 0)
        self.assertFalse(any(event["kind"] == "joint_consistency" for event in result["events"]))

    def test_global_budget_interrupts_query_atomically_without_rewrite(self):
        # The fixed graph now ends in the earlier triangle proof. The bare graph
        # still reaches the full joint query after an n-check full-palette guard.
        graph = dict(self.inputs["graph"], fixed=[])
        baseline = initial_factors(graph, self.inputs["options"])
        guard_checks = len(graph["vertices"])
        entered = []

        def wrapped(factors, domains, **options):
            before = deepcopy((factors, domains))
            entered.append(True)
            try:
                return joint_supports(factors, domains, **options)
            finally:
                self.assertEqual((factors, domains), before)

        with patch("four_color_joint_consistency.joint_supports", side_effect=wrapped):
            result = solve_constraints(graph, **dict(self.inputs["options"],
                                                     use_joint_consistency=True,
                                                     max_checks=baseline["stats"]["checks"] + guard_checks + 5))
        self.assertEqual(entered, [True])
        self.assertEqual(result["status"], "limit")
        self.assertEqual(result["stats"]["joint_consistency_checks"], guard_checks + 5)
        self.assertEqual(result["stats"]["triangle_equality_checks"], guard_checks)
        self.assertEqual(result["stats"]["joint_support_checks"], 5)
        self.assertEqual(result["stats"]["joint_consistency_row_prunes"], 0)
        self.assertEqual(result["elimination_records"], [])
        self.assertEqual(result["stats"]["writebacks"], 0)
        self.assertEqual(result["domains"], [sorted(values) for values in baseline["domains"]])

    def test_relabeling_and_vertex_order_do_not_install_a_special_case(self):
        graph = self.inputs["graph"]
        mapping = {v: 900 - v * 17 for v in graph["vertices"]}
        relabeled = dict(vertices=[mapping[v] for v in reversed(graph["vertices"])],
                         edges=[[mapping[u], mapping[v]] for u, v in reversed(graph["edges"])],
                         fixed=[[mapping[v], c] for v, c in graph["fixed"]])
        result = solve_constraints(relabeled, **dict(self.inputs["options"],
                                                     use_joint_consistency=True))
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(result["stats"]["candidate_checks"], 0)
        self.assertEqual(result["elimination_records"], [])

    def test_small_graph_oracle_and_all_solution_preservation(self):
        rng = random.Random(20261027)
        for index in range(40):
            vertices = rng.sample(range(-20, 40), rng.randrange(1, 8))
            graph = dict(vertices=vertices,
                         edges=[list(edge) for edge in combinations(vertices, 2) if rng.random() < .5],
                         fixed=[[v, rng.randrange(4)] for v in vertices if rng.random() < .2])
            solutions = list(original_solutions(graph))
            result = solve_constraints(graph, use_joint_consistency=True,
                                       joint_consistency_max_checks=5000,
                                       use_substructures=index % 2 == 0,
                                       use_conflicts=False, use_intersections=index % 3 == 0,
                                       use_interface_cache=index % 3 == 0,
                                       interface_cache_max_rows=24,
                                       bucket_method="prefix" if index % 2 else "anchor")
            with self.subTest(index=index):
                self.assertEqual(result["status"], "colored" if solutions else "unsatisfiable")
                self.assertLessEqual(result["stats"]["joint_consistency_checks"], 5000)
                self.assertEqual(result["stats"]["checks"], result["stats"]["candidate_checks"]
                                 + result["stats"]["relation_checks"])
                if solutions:
                    self.check_witness(graph, result["colors"])
                for record in result["elimination_records"]:
                    fibers = {tuple(row["boundary"]): row["colors"] for row in record["rows"]}
                    for coloring in solutions:
                        self.assertIn(coloring[record["vertex"]],
                                      fibers[tuple(coloring[v] for v in record["scope"])])

    def test_invalid_flags_and_cli_forwarding(self):
        graph = dict(vertices=[0, 1, 2], edges=[[0, 1], [1, 2]])
        for options in [dict(use_joint_consistency=1), dict(joint_consistency_max_checks=-1),
                        dict(joint_consistency_max_checks=True)]:
            with self.assertRaises(ValueError):
                solve_constraints(graph, **options)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "graph.json"
            output = Path(directory) / "result.json"
            source.write_text(json.dumps(graph))
            command = [sys.executable, str(ROOT / "scripts/four_color_lab.py"), "solve", str(source),
                       "--joint-consistency", "--joint-consistency-max-checks", "37"]
            done = subprocess.run(command + ["--engine", "constraints", "--json", str(output)],
                                  cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stderr)
            result = json.loads(output.read_text())
            self.assertTrue(result["use_joint_consistency"])
            self.assertEqual(result["joint_consistency_max_checks"], 37)
            self.assertLessEqual(result["stats"]["joint_consistency_checks"], 37)
            bad = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("require --engine constraints", bad.stderr)


if __name__ == "__main__":
    unittest.main()
