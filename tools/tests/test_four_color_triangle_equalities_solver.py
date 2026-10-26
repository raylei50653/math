"""Early structural proofs, unchanged original solutions, and atomic budgets."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import random
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_color_constraints import solve_constraints
from four_color_triangle_equalities import derive_triangle_equalities
from test_four_color_joint_consistency import original_solutions
import test_four_color_triangle_equalities as helper_tests


class TriangleEqualitySolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = json.loads((ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f/"
                                 "propagation/inputs.json").read_text())

    def test_both_simple_and_strong_modes_reject_before_cycles_or_joint_enumeration(self):
        graph = self.inputs["graph"]
        for extra in ({}, self.inputs["options"]):
            with self.subTest(strong=bool(extra)):
                result = solve_constraints(graph, **dict(extra, use_joint_consistency=True))
                self.assertEqual(result["status"], "unsatisfiable")
                for stat in ("candidate_checks", "eliminations", "writebacks",
                             "cycle_queries", "cycle_context_queries", "joint_consistency_queries"):
                    self.assertEqual(result["stats"][stat], 0)
                self.assertEqual(result["elimination_records"], [])
                self.assertGreater(result["stats"]["triangle_equality_merges"], 0)
                self.assertLess(result["stats"]["checks"], 10000)
                self.assertEqual(result["stats"]["joint_consistency_checks"],
                                 result["stats"]["triangle_equality_checks"])
                event = next(event for event in result["events"] if event["kind"] == "conflict")
                self.assertEqual(event["propagation_kind"], "triangle_equalities")
                self.assertEqual(event["structural_conflict"]["kind"], "same_singleton_edge")
                original = {frozenset(edge) for edge in graph["edges"]}
                self.assertTrue(all(frozenset(edge) in original for edge in event["causal_edges"]))
                for pin, _ in graph["fixed"]:
                    self.assertTrue(any(pin in edge for edge in event["causal_edges"]))

    def test_satisfiable_edge_deletion_replays_proofs_and_preserves_every_original_solution(self):
        graph = dict(self.inputs["graph"], edges=[edge for edge in self.inputs["graph"]["edges"]
                                                 if edge != [7, 13]])
        before = deepcopy(graph)
        solutions = list(original_solutions(graph))
        self.assertEqual(len(solutions), 6)
        captured = []

        def wrapped(vertices, edges, domains, **options):
            inputs = deepcopy((vertices, edges, domains))
            answer = derive_triangle_equalities(vertices, edges, domains, **options)
            self.assertEqual((vertices, edges, domains), inputs)
            if answer["complete"]:
                helper_tests.TriangleEqualityTests().check_proof(*inputs, answer)
            captured.append((inputs, answer))
            return answer

        with patch("four_color_triangle_equalities.derive_triangle_equalities", side_effect=wrapped):
            result = solve_constraints(graph, use_joint_consistency=True, trace_limit=20000)
        self.assertEqual(result["status"], "colored")
        self.assertEqual(graph, before)
        self.assertGreater(result["stats"]["triangle_equality_prunes"], 0)
        self.assertTrue(captured)
        fixed = dict(graph["fixed"])
        original = {frozenset(edge) for edge in graph["edges"]}
        for event in result["events"]:
            if event["phase"] != "reduce":
                continue
            self.assertEqual(event["colors"], [fixed.get(v, -1) for v in graph["vertices"]])
            for solution in solutions:
                self.assertTrue(all(solution[v] in domain for v, domain
                                    in zip(graph["vertices"], event["domains"])))
            if event["kind"] == "triangle_equalities":
                self.assertTrue(all(frozenset(edge) in original for edge in event["causal_edges"]))
                self.assertTrue(any(answer["proof_steps"] == event["structural_proof"]
                                    for _, answer in captured if answer["complete"]))
        assignment = dict(zip(graph["vertices"], result["colors"]))
        self.assertTrue(all(assignment[u] != assignment[v] for u, v in graph["edges"]))

    def test_bare_graph_keeps_all_624_solutions_and_uses_full_palette_fastpath(self):
        graph = dict(self.inputs["graph"], fixed=[])
        solutions = list(original_solutions(graph))
        self.assertEqual(len(solutions), 624)
        result = solve_constraints(graph, use_joint_consistency=True, trace_limit=20000)
        self.assertEqual(result["status"], "colored")
        self.assertEqual(result["stats"]["triangle_equality_merges"], 0)
        self.assertEqual(result["stats"]["triangle_equality_prunes"], 0)
        for event in result["events"]:
            if event["phase"] == "reduce":
                for solution in solutions:
                    self.assertTrue(all(solution[v] in domain for v, domain
                                        in zip(graph["vertices"], event["domains"])))

    def test_relabel_and_reorder_preserve_structural_refutation(self):
        graph = self.inputs["graph"]
        rename = {v: -100 + 31 * v for v in graph["vertices"]}
        renamed = dict(vertices=[rename[v] for v in reversed(graph["vertices"])],
                       edges=[[rename[v], rename[u]] for u, v in reversed(graph["edges"])],
                       fixed=[[rename[v], c] for v, c in graph["fixed"]])
        result = solve_constraints(renamed, use_joint_consistency=True)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(result["stats"]["candidate_checks"], 0)
        event = next(event for event in result["events"] if event["kind"] == "conflict")
        self.assertEqual(event["propagation_kind"], "triangle_equalities")

    def test_local_cap_discards_partial_proof_and_preserves_exact_fallback(self):
        graph = self.inputs["graph"]
        options = self.inputs["options"]
        baseline = solve_constraints(graph, **options)
        result = solve_constraints(graph, **dict(options, use_joint_consistency=True,
                                                 joint_consistency_max_checks=100))
        self.assertEqual(result["status"], baseline["status"])
        self.assertEqual(result["elimination_records"], baseline["elimination_records"])
        self.assertEqual(result["stats"]["joint_consistency_checks"], 100)
        self.assertEqual(result["stats"]["triangle_equality_checks"], 100)
        self.assertEqual(result["stats"]["triangle_equality_merges"], 0)
        self.assertEqual(result["stats"]["triangle_equality_prunes"], 0)
        self.assertEqual(result["stats"]["triangle_equality_incomplete"], 1)
        self.assertFalse(any("structural_proof" in event for event in result["events"]))

    def test_global_cap_interrupts_private_closure_before_any_live_domain_commit(self):
        graph = self.inputs["graph"]
        options = self.inputs["options"]
        starts = []

        def observe(vertices, edges, domains, **settings):
            starts.append(deepcopy(domains))
            return derive_triangle_equalities(vertices, edges, domains, **settings)

        completed = solve_constraints(graph, **dict(options, use_joint_consistency=True))
        before_checks = (completed["stats"]["checks"]
                         - completed["stats"]["triangle_equality_checks"])
        with patch("four_color_triangle_equalities.derive_triangle_equalities", side_effect=observe):
            result = solve_constraints(graph, **dict(options, use_joint_consistency=True,
                                                     max_checks=before_checks + 100))
        self.assertEqual(result["status"], "limit")
        self.assertEqual(len(starts), 1)
        self.assertEqual(result["domains"], [sorted(starts[0][v]) for v in graph["vertices"]])
        self.assertEqual(result["stats"]["triangle_equality_checks"], 100)
        self.assertEqual(result["stats"]["triangle_equality_merges"], 0)
        self.assertEqual(result["stats"]["triangle_equality_prunes"], 0)
        self.assertEqual(result["elimination_records"], [])
        self.assertEqual(result["stats"]["writebacks"], 0)
        self.assertFalse(any("structural_proof" in event for event in result["events"]))

    def test_small_graph_domain_feedback_preserves_every_literal_solution(self):
        rng = random.Random(26031)
        for case in range(80):
            vertices = rng.sample(range(-10, 25), rng.randrange(1, 8))
            graph = dict(vertices=vertices,
                         edges=[list(edge) for edge in combinations(vertices, 2) if rng.random() < .6],
                         fixed=[[v, rng.randrange(4)] for v in vertices if rng.random() < .3])
            solutions = list(original_solutions(graph))
            result = solve_constraints(graph, use_joint_consistency=True, use_conflicts=False,
                                       use_substructures=case % 2 == 0,
                                       joint_consistency_max_checks=20000, trace_limit=20000)
            self.assertEqual(result["status"], "colored" if solutions else "unsatisfiable")
            self.assertLessEqual(result["stats"]["joint_consistency_checks"], 20000)
            self.assertEqual(result["stats"]["joint_consistency_checks"],
                             result["stats"]["triangle_equality_checks"]
                             + result["stats"]["joint_support_checks"])
            for event in result["events"]:
                if event["phase"] == "reduce":
                    for solution in solutions:
                        self.assertTrue(all(solution[v] in domain for v, domain
                                            in zip(vertices, event["domains"])))


if __name__ == "__main__":
    unittest.main()
