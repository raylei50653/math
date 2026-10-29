"""Exact q-way projection must preserve residuals and complete history fibres."""

from copy import deepcopy
from itertools import combinations, product
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from four_color_bounded_projection import (
    build_representation, compile_representation, fibre_choices, reconstruct_one,
)


def original_accepts(graph, colors):
    assignment = dict(zip(graph["vertices"], colors))
    return (all(assignment[u] != assignment[v] for u, v in graph["edges"])
            and all(assignment[v] == c for v, c in graph.get("fixed", [])))


class BoundedProjectionTests(unittest.TestCase):
    def assert_exact(self, graph, rep):
        rep = json.loads(json.dumps(rep))
        accepts = compile_representation(rep)
        expected_count = 0
        projected = set()
        active = rep["active_vertices"]
        indices = [graph["vertices"].index(v) for v in active]
        for colors in product(range(4), repeat=len(graph["vertices"])):
            expected = original_accepts(graph, colors)
            self.assertEqual(accepts(colors), expected, (graph, rep["history"], colors))
            expected_count += expected
            if expected:
                projected.add(tuple(colors[i] for i in indices))

        # Complete-history membership alone can hide an overly weak residual:
        # the original bucket recipes would still reject false originals.
        # Independently verify the residual is exactly the existential image.
        def residual_accepts(row):
            assignment = dict(zip(active, row))
            for key in rep["active_factor_ids"]:
                factor = rep["factors"][key]
                values = [assignment[v] for v in factor["scope"]]
                if factor["kind"] == "domain":
                    valid = values[0] in factor["colors"]
                elif factor["kind"] == "neq":
                    valid = values[0] != values[1]
                else:
                    valid = values in factor["rows"]
                if not valid:
                    return False
            return True

        for row in product(range(4), repeat=len(active)):
            self.assertEqual(residual_accepts(row), row in projected,
                             ("residual_projection", graph, rep["history"], row))
        witness = reconstruct_one(rep)
        if expected_count:
            self.assertIsNotNone(witness)
            self.assertTrue(original_accepts(graph, witness))
            self.assertTrue(accepts(witness))
        else:
            self.assertIsNone(witness)
        return expected_count

    def test_every_small_graph_every_prefix_and_both_methods(self):
        for n in range(4):
            pairs = list(combinations(range(n), 2))
            for bits in range(1 << len(pairs)):
                graph = dict(vertices=list(range(n)), edges=[list(e) for i, e in enumerate(pairs)
                                                            if bits & (1 << i)])
                for method in ("bounded", "full", "anchored"):
                    for cut in range(n + 1):
                        rep = build_representation(graph, stop_after=cut, method=method)
                        self.assertEqual(len(rep["history"]), cut)
                        self.assert_exact(graph, rep)

    def test_four_rainbow_neighbors_need_four_factors_and_keep_all_fibres(self):
        graph = dict(vertices=[80, -2, 4, 30, 9],
                     edges=[[80, v] for v in [-2, 4, 30, 9]])
        rep = build_representation(graph, stop_after=1)
        for boundary in product(range(4), repeat=4):
            self.assertEqual(fibre_choices(rep, 0, boundary),
                             tuple(c for c in range(4) if c not in boundary))
        self.assertEqual(fibre_choices(rep, 0, [0, 1, 2, 3]), ())
        self.assert_exact(graph, rep)
        # Every three of these original edge factors has an x witness.
        rainbow = {-2: 0, 4: 1, 30: 2, 9: 3}
        for triple in combinations(rainbow, 3):
            self.assertTrue(any(all(c != rainbow[v] for v in triple) for c in range(4)))

    def test_high_degree_center_splits_into_exact_four_neighbor_tables(self):
        graph = dict(vertices=list(range(7)), edges=[[0, v] for v in range(1, 7)])
        bounded = build_representation(graph, stop_after=1)
        full = build_representation(graph, stop_after=1, method="full")
        bstep, fstep = bounded["metrics"]["steps"][0], full["metrics"]["steps"][0]
        self.assertEqual(bstep["projected_factors"], 15)
        self.assertEqual(bstep["max_projected_scope"], 4)
        self.assertEqual(fstep["max_projected_scope"], 6)
        self.assertEqual(self.assert_exact(graph, bounded), self.assert_exact(graph, full))

    def test_fixed_eliminand_uses_single_factor_projections(self):
        graph = dict(vertices=[0, 1, 2, 3, 4], edges=[[0, v] for v in range(1, 5)],
                     fixed=[[0, 2]])
        rep = build_representation(graph, stop_after=1)
        step = rep["metrics"]["steps"][0]
        self.assertEqual(step["effective_domain_size"], 1)
        self.assertEqual(step["max_projected_scope"], 1)
        self.assertEqual(step["projected_factors"], 4)
        for boundary in product(range(4), repeat=4):
            self.assertEqual(fibre_choices(rep, 0, boundary), () if 2 in boundary else (2,))
        self.assertEqual(self.assert_exact(graph, rep), 81)

    def test_anchored_star_uses_one_anchor_and_three_other_factors(self):
        graph = dict(vertices=list(range(9)), edges=[[0, v] for v in range(1, 9)])
        rep = build_representation(graph, stop_after=1, method="anchored")
        step = rep["metrics"]["steps"][0]
        self.assertEqual(step["anchor_support_cap"], 3)
        self.assertEqual(step["projected_factors"], 35)
        self.assertEqual(step["projected_rows"], 35 * 232)
        self.assertEqual(step["max_projected_scope"], 4)
        # Exhaust every residual boundary tuple, including rainbow failures.
        factors = [rep["factors"][key] for key in rep["active_factor_ids"]
                   if rep["factors"][key]["kind"] == "table"]
        relations = [set(map(tuple, f["rows"])) for f in factors]
        for boundary in product(range(4), repeat=8):
            assignment = dict(zip(range(1, 9), boundary))
            actual = all(tuple(assignment[v] for v in factor["scope"]) in rows
                         for factor, rows in zip(factors, relations))
            self.assertEqual(actual, len(set(boundary)) < 4)

    def test_literal_ids_fixed_colors_and_both_orders(self):
        graphs = [
            dict(vertices=[1000, -30, 7, 0], edges=[[1000, -30], [-30, 7]], fixed=[[0, 3]]),
            dict(vertices=[30, -7, 800], edges=[[30, -7]], fixed=[[30, 2], [-7, 2]]),
            dict(vertices=list(range(5)), edges=[list(e) for e in combinations(range(5), 2)]),
            dict(vertices=list(range(6)), edges=[[i, (i + 1) % 5] for i in range(5)]
                 + [[5, i] for i in range(5)]),
        ]
        for graph in graphs:
            for order in (graph["vertices"], list(reversed(graph["vertices"]))):
                for method in ("bounded", "full", "anchored"):
                    for cut in range(len(order) + 1):
                        with self.subTest(graph=graph, order=order, method=method, cut=cut):
                            self.assert_exact(graph, build_representation(
                                graph, stop_after=cut, order=order, method=method))

    def test_every_work_budget_retains_last_complete_prefix_atomically(self):
        graph = dict(vertices=[4, -2, 90, 17],
                     edges=[[4, -2], [-2, 90], [90, 17], [17, 4]], fixed=[[90, 1]])
        for method in ("bounded", "full", "anchored"):
            complete = build_representation(graph, method=method)
            prefixes = [build_representation(graph, method=method, stop_after=cut)
                        for cut in range(len(graph["vertices"]) + 1)]
            for budget in range(complete["metrics"]["candidate_checks"] + 1):
                limited = build_representation(graph, method=method, max_checks=budget)
                expected = prefixes[len(limited["history"])]
                for field in ("history", "factors", "active_vertices", "active_factor_ids"):
                    self.assertEqual(limited[field], expected[field], (method, budget, field))
                self.assertLessEqual(limited["metrics"]["candidate_checks"], budget)
                self.assertEqual(limited["metrics"]["candidate_checks"],
                                 limited["metrics"]["color_trials"] + limited["metrics"]["cap_scan_rows"])
                self.assert_exact(graph, limited)
            self.assertEqual(build_representation(graph, method=method,
                             max_checks=complete["metrics"]["candidate_checks"]), complete)
            if method == "anchored":
                self.assertGreater(complete["metrics"]["cap_scan_rows"], 0)

    def test_zeroary_false_empty_graph_and_unary_domain_exhaustion(self):
        empty = build_representation(dict(vertices=[], edges=[]))
        self.assertEqual(empty["decision"], "satisfiable")
        self.assertEqual(reconstruct_one(empty), [])
        graph = dict(vertices=[0, 1], edges=[[0, 1]], fixed=[[0, 0], [1, 0]])
        rep = build_representation(graph)
        self.assertEqual(rep["decision"], "unsatisfiable")
        self.assertEqual(rep["history"][-1]["effective_domain"], [])
        self.assertTrue(any(f["kind"] == "table" and f["scope"] == [] and f["rows"] == []
                            for key in rep["active_factor_ids"] for f in [rep["factors"][key]]))
        self.assert_exact(graph, rep)

    def test_metadata_never_replaces_constraints_and_input_unchanged(self):
        graph = dict(vertices=[0, 1], edges=[[0, 1]])
        old = deepcopy(graph)
        rep = build_representation(graph, stop_after=1)
        rep["decision"] = "unsatisfiable"
        self.assertTrue(compile_representation(rep)([0, 1]))
        self.assertFalse(compile_representation(rep)([0, 0]))
        self.assertEqual(graph, old)

    def test_invalid_options_or_corrupt_history_raise(self):
        graph = dict(vertices=[0, 1], edges=[[0, 1]])
        for options in (dict(method="approx"), dict(stop_after=True), dict(stop_after=3),
                        dict(max_checks=-1), dict(max_checks=True), dict(order=[0, 0])):
            with self.subTest(options=options), self.assertRaises(ValueError):
                build_representation(graph, **options)
        rep = build_representation(graph, stop_after=1)
        rep["history"].clear()
        with self.assertRaises(ValueError):
            compile_representation(rep)
