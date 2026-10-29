"""A partial history remains exact only with its residual and recovery rules."""

from copy import deepcopy
from itertools import combinations, product
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from four_color_partial_history import (
    build_representation, compile_representation, fibre_choices, reconstruct_one,
)


def original_accepts(graph, colors):
    """Independent oracle uses only the supplied original edges and fixed colors."""
    assignment = dict(zip(graph["vertices"], colors))
    return (all(assignment[u] != assignment[v] for u, v in graph["edges"])
            and all(assignment[v] == c for v, c in graph.get("fixed", [])))


class PartialHistoryTests(unittest.TestCase):
    def assert_exact(self, graph, representation):
        accepts = compile_representation(representation)
        expected_count = 0
        for colors in product(range(4), repeat=len(graph["vertices"])):
            expected = original_accepts(graph, colors)
            self.assertEqual(accepts(list(colors)), expected,
                             (graph, representation["history"], colors))
            expected_count += expected
        witness = reconstruct_one(representation)
        if expected_count:
            self.assertIsNotNone(witness)
            self.assertEqual(len(witness), len(graph["vertices"]))
            self.assertTrue(original_accepts(graph, witness))
            self.assertTrue(accepts(witness))
        else:
            self.assertIsNone(witness)
        return expected_count

    def test_every_cut_and_storage_mode_matches_original_edges_and_fixed_colors(self):
        graphs = [
            dict(vertices=[], edges=[]),
            dict(vertices=[17], edges=[]),
            dict(vertices=[17], edges=[], fixed=[[17, 3]]),
            dict(vertices=[40, -3, 900], edges=[[40, -3], [-3, 900]]),
            dict(vertices=[40, -3, 900, 17],
                 edges=[[40, -3], [-3, 900], [900, 40]], fixed=[[900, 2]]),
            dict(vertices=[0, 1], edges=[[0, 1]], fixed=[[0, 0], [1, 0]]),
            dict(vertices=list(range(5)),
                 edges=[list(e) for e in combinations(range(5), 2)]),
            dict(vertices=list(range(5)), edges=[[0, v] for v in range(1, 5)]),
        ]
        for graph in graphs:
            for mode in ("table", "recipe", "mixed"):
                for cut in range(len(graph["vertices"]) + 1):
                    with self.subTest(graph=graph, mode=mode, cut=cut):
                        representation = build_representation(
                            graph, stop_after=cut, history_mode=mode)
                        self.assertEqual(len(representation["history"]), cut)
                        self.assert_exact(graph, representation)

    def test_zero_history_and_zero_budget_still_define_all_original_solutions(self):
        graph = dict(vertices=[8, -5, 30], edges=[[8, -5]], fixed=[[30, 2]])
        original = deepcopy(graph)
        representation = build_representation(graph, stop_after=0, max_checks=0)
        self.assertEqual(representation["history"], [])
        self.assertEqual(representation["active_vertices"], graph["vertices"])
        self.assertEqual(representation["metrics"]["candidate_checks"], 0)
        self.assertEqual(representation["stop_reason"], "requested_prefix")
        self.assertEqual(representation["decision"], "undetermined")
        self.assertEqual(self.assert_exact(graph, representation), 12)
        self.assertEqual(graph, original)

    def test_recipe_recomputes_all_ordered_star_fibres_without_stored_fibre_rows(self):
        graph = dict(vertices=[80, -2, 4, 30, 9],
                     edges=[[80, v] for v in [-2, 4, 30, 9]])
        representation = build_representation(graph, stop_after=1,
                                              history_mode="recipe")
        history = representation["history"][0]
        self.assertEqual(history["kind"], "recipe")
        self.assertNotIn("rows", history)
        self.assertEqual(set(history["scope"]), {-2, 4, 30, 9})
        self.assertEqual(representation["metrics"]["stored_fibre_rows"], 0)
        for boundary in product(range(4), repeat=4):
            self.assertEqual(fibre_choices(representation, 0, list(boundary)),
                             tuple(c for c in range(4) if c not in boundary))
        self.assertEqual(fibre_choices(representation, 0, [0, 1, 2, 3]), ())
        self.assertEqual(fibre_choices(representation, 0, [3, 3, 3, 3]), (0, 1, 2))

    def test_recipe_preserves_fixed_domains_and_prior_projected_relations(self):
        graph = dict(vertices=[50, 30, -1, 90],
                     edges=[[50, 30], [30, -1], [-1, 90], [90, 50]],
                     fixed=[[50, 2]])
        representation = build_representation(graph, stop_after=3,
                                              history_mode="recipe")
        before = deepcopy(representation)
        self.assert_exact(graph, representation)
        for row in product(range(4), repeat=len(representation["history"][0]["scope"])):
            self.assertTrue(set(fibre_choices(representation, 0, list(row))) <= {2})
        self.assertEqual(representation, before)

    def test_work_limit_never_commits_an_incomplete_projection_or_history(self):
        graph = dict(vertices=[4, -2, 90], edges=[[4, -2], [-2, 90]])
        for mode in ("table", "recipe", "mixed"):
            complete = build_representation(graph, history_mode=mode)
            first = build_representation(graph, stop_after=1, history_mode=mode)
            cost = first["metrics"]["candidate_checks"]
            for budget, completed in ((0, 0), (1, 0), (cost - 1, 0),
                                      (cost, 1), (cost + 1, 1)):
                with self.subTest(mode=mode, budget=budget):
                    limited = build_representation(graph, history_mode=mode,
                                                   max_checks=budget)
                    committed = build_representation(graph, history_mode=mode,
                                                     stop_after=completed)
                    self.assertEqual(limited["stop_reason"], "work_limit")
                    self.assertEqual(limited["metrics"]["candidate_checks"], budget)
                    for field in ("history", "active_vertices", "active_factor_ids", "factors"):
                        self.assertEqual(limited[field], committed[field], field)
                    self.assert_exact(graph, limited)
            at_full_budget = build_representation(
                graph, history_mode=mode,
                max_checks=complete["metrics"]["candidate_checks"])
            self.assertEqual(at_full_budget, complete)

    def test_empty_interface_false_is_preserved_and_not_confused_with_empty_graph(self):
        graph = dict(vertices=[0, 1], edges=[[0, 1]], fixed=[[0, 0], [1, 0]])
        for mode in ("table", "recipe", "mixed"):
            representation = build_representation(graph, history_mode=mode)
            self.assertEqual(representation["active_vertices"], [])
            self.assertEqual(representation["decision"], "unsatisfiable")
            active = [representation["factors"][key]
                      for key in representation["active_factor_ids"]]
            self.assertTrue(any(f["kind"] == "table" and f["scope"] == []
                                and f["rows"] == [] for f in active))
            self.assertEqual(self.assert_exact(graph, representation), 0)
        empty = build_representation(dict(vertices=[], edges=[]))
        self.assertEqual(empty["decision"], "satisfiable")
        self.assertEqual(reconstruct_one(empty), [])
        self.assertTrue(compile_representation(empty)([]))

    def test_json_roundtrip_is_self_contained_and_literal_vertex_order_is_preserved(self):
        graph = dict(vertices=[1000, -30, 7, 0],
                     edges=[[1000, -30], [-30, 7]], fixed=[[0, 3]])
        for mode in ("table", "recipe", "mixed"):
            representation = build_representation(
                graph, stop_after=2, history_mode=mode, order=[7, -30, 0, 1000])
            self.assertEqual(representation["vertices"], graph["vertices"])
            self.assertEqual([h["vertex"] for h in representation["history"]], [7, -30])
            restored = json.loads(json.dumps(representation))
            before = deepcopy(restored)
            self.assert_exact(graph, restored)
            self.assertEqual(restored, before)

    def test_decision_metadata_does_not_replace_the_actual_constraints(self):
        graph = dict(vertices=[0, 1], edges=[[0, 1]])
        representation = build_representation(graph, stop_after=1,
                                              history_mode="recipe")
        representation["decision"] = "unsatisfiable"
        self.assertTrue(compile_representation(representation)([0, 1]))
        self.assertFalse(compile_representation(representation)([0, 0]))
        self.assertTrue(original_accepts(graph, reconstruct_one(representation)))

    def test_dropping_a_residual_edge_accepts_false_solutions(self):
        graph = dict(vertices=[0, 1, 2], edges=[[0, 1], [1, 2]])
        representation = build_representation(graph, stop_after=1, history_mode="table")
        self.assertFalse(compile_representation(representation)([1, 0, 0]))
        altered = deepcopy(representation)
        altered["active_factor_ids"] = [
            key for key in altered["active_factor_ids"]
            if altered["factors"][key]["kind"] != "neq"]
        self.assertTrue(compile_representation(altered)([1, 0, 0]))
        self.assertFalse(original_accepts(graph, [1, 0, 0]))

    def test_dropping_a_fibre_choice_loses_an_original_solution(self):
        graph = dict(vertices=[0, 1], edges=[[0, 1]])
        representation = build_representation(graph, stop_after=1, history_mode="table")
        self.assertTrue(compile_representation(representation)([3, 0]))
        altered = deepcopy(representation)
        row = next(row for row in altered["history"][0]["rows"]
                   if row["boundary"] == [0])
        row["colors"].remove(3)
        self.assertFalse(compile_representation(altered)([3, 0]))
        self.assertTrue(original_accepts(graph, [3, 0]))

    def test_invalid_options_or_missing_history_do_not_silently_change_semantics(self):
        graph = dict(vertices=[0, 1], edges=[[0, 1]])
        for options in (dict(stop_after=-1), dict(stop_after=3), dict(stop_after=True),
                        dict(history_mode="one_witness"), dict(max_checks=-1),
                        dict(max_checks=True), dict(order=[0]), dict(order=[0, 0]),
                        dict(order=[0, 2])):
            with self.subTest(options=options), self.assertRaises(ValueError):
                build_representation(graph, **options)
        representation = build_representation(graph, stop_after=1)
        representation["history"].clear()
        with self.assertRaises(ValueError):
            compile_representation(representation)


if __name__ == "__main__":
    unittest.main()
