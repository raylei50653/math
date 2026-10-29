"""Original-edge and subtree-oracle checks for regional message orders."""

from copy import deepcopy
from itertools import combinations
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import test_four_color_local_messages as reference
from four_color_local_messages import solve_local_messages


def solve(graph, **kwargs):
    kwargs.setdefault("audit_metadata", True)
    return solve_local_messages(graph, **kwargs)


class RegionMessageTests(unittest.TestCase):
    def setUp(self):
        # Only assertion/oracle helpers are reused; the historical test cases
        # are not inherited and run a second time under unittest discovery.
        self.reference = reference.LocalMessageTests()

    def check_result(self, graph, result, domains=None):
        expected = bool(reference.original_solutions(graph, domains, first_only=True))
        self.assertEqual(result["status"], "colored" if expected else "unsatisfiable")
        self.reference.check_decomposition(graph, result)
        self.reference.check_messages(graph, result, domains)
        if expected:
            self.reference.check_coloring(graph, result, domains)
        else:
            self.assertIsNone(result["colors"])

    def test_all_four_point_graphs_and_two_palettes_across_three_orders(self):
        vertices = [40, -11, 10000, 7]
        pairs = list(combinations(vertices, 2))
        orders = [vertices, [7, -11, 40, 10000], [10000, 40, 7, -11]]
        for mask in range(1 << len(pairs)):
            graph = {"vertices": vertices,
                     "edges": [list(edge) for bit, edge in enumerate(pairs)
                               if mask & (1 << bit)]}
            for palette in ((0, 1), (0, 1, 2, 3)):
                domains = {v: palette for v in vertices}
                for order in orders:
                    with self.subTest(mask=mask, palette=palette, order=order):
                        result = solve(graph, domains=domains, elimination_order=order)
                        self.assertEqual(result["decomposition"]["order"], order)
                        self.check_result(graph, result, domains)

    def test_asymmetric_domains_and_fixed_colors_across_orders_and_symmetry(self):
        rng = random.Random(472951)
        for case in range(40):
            vertices = [-19, 42, 2003, -8, 71, 993][:rng.randrange(2, 7)]
            rng.shuffle(vertices)
            graph = {"vertices": vertices,
                     "edges": [list(edge) for edge in combinations(vertices, 2)
                               if rng.random() < .43],
                     "fixed": [[v, rng.randrange(4)] for v in vertices
                               if rng.random() < .22]}
            domains = {v: [c for c in range(4) if rng.random() < .8]
                       for v in vertices}
            order = rng.sample(vertices, len(vertices))
            frozen = deepcopy((graph, domains, order))
            for ordered in (order, list(reversed(order))):
                for symmetry in (False, True):
                    with self.subTest(case=case, symmetry=symmetry, order=ordered):
                        result = solve(graph, domains=domains, elimination_order=ordered,
                                       color_symmetry=symmetry)
                        self.check_result(graph, result, domains)
            self.assertEqual((graph, domains, order), frozen)

    def test_explicit_default_order_preserves_messages_and_witness(self):
        graph = reference.cycle(7)
        graph["fixed"] = [[2, 3]]
        for symmetry in (False, True):
            default = solve(graph, color_symmetry=symmetry)
            order = default["decomposition"]["order"]
            explicit = solve(graph, color_symmetry=symmetry, elimination_order=iter(order))
            self.assertEqual(default["status"], explicit["status"])
            self.assertEqual(default["colors"], explicit["colors"])
            self.assertEqual(default["transcript"], explicit["transcript"])
            self.assertEqual(default["decomposition"], explicit["decomposition"])
            self.assertEqual(default["stats"]["query_checks"],
                             explicit["stats"]["query_checks"])
            self.assertEqual(default["stats"]["writeback_checks"],
                             explicit["stats"]["writeback_checks"])
            self.assertEqual(default, solve(graph, color_symmetry=symmetry,
                                           elimination_order=None))

    def test_fill_edges_never_become_coloring_edges(self):
        graph = reference.cycle(6)
        domains = {v: [0, 1] for v in graph["vertices"]}
        # Removing alternate vertices first creates a filled triangle on the
        # remaining vertices, which would falsely reject a two-color C6 if
        # those bookkeeping edges were interpreted as original constraints.
        order = [0, 2, 4, 1, 3, 5]
        result = solve(graph, domains=domains, elimination_order=order)
        self.check_result(graph, result, domains)
        self.assertEqual(result["status"], "colored")
        self.assertEqual(len(reference.original_solutions(graph, domains)), 2)
        self.assertGreaterEqual(result["stats"]["max_separator_size"], 2)

    def test_local_supports_do_not_accept_two_color_odd_cycle_or_k5(self):
        cases = [(reference.cycle(5), {v: [0, 1] for v in range(5)}, [0, 2, 4, 1, 3]),
                 ({"vertices": list(range(5)),
                   "edges": [list(edge) for edge in combinations(range(5), 2)]},
                  None, [3, 1, 4, 0, 2])]
        for graph, domains, order in cases:
            result = solve(graph, domains=domains, elimination_order=order)
            self.check_result(graph, result, domains)
            self.assertEqual(result["status"], "unsatisfiable")
            self.assertEqual(result["stats"]["writeback_vertices"], 0)

    def test_every_small_budget_cutoff_keeps_replies_exact_and_colors_unpublished(self):
        graph = reference.cycle(4)
        order = [0, 2, 1, 3]
        full = solve(graph, elimination_order=order)
        for argument, stat in (("max_checks", "checks"), ("max_messages", "messages"),
                               ("max_cache_entries", "cache_entries")):
            for cap in range(full["stats"][stat] + 1):
                with self.subTest(argument=argument, cap=cap):
                    result = solve(graph, elimination_order=order, **{argument: cap})
                    if cap == full["stats"][stat]:
                        self.check_result(graph, result)
                    else:
                        self.assertEqual(result["status"], "limit")
                        self.assertIsNone(result["colors"])
                        if result["decomposition"] is not None:
                            self.reference.check_messages(graph, result)

    def test_experiment_accepts_a_late_limit_without_published_colors(self):
        from four_color_region_experiment import validate_witness
        graph = reference.cycle(4)
        order = [0, 2, 1, 3]
        full = solve(graph, elimination_order=order)
        limited = solve(graph, elimination_order=order,
                        max_checks=full["stats"]["checks"] - 1)
        self.assertEqual(limited["status"], "limit")
        self.assertIsNone(limited["colors"])
        # Work may have advanced into private reconstruction before the cap;
        # the public result must still be an inconclusive, uncolored result.
        self.assertGreater(limited["stats"]["writeback_vertices"], 0)
        validate_witness(graph, None, limited)

    def test_empty_disconnected_and_signed_huge_labels(self):
        graphs = [{"vertices": [], "edges": []},
                  {"vertices": [-10**200, 7, 10**180, 9, 42],
                   "edges": [[-10**200, 7], [10**180, 9]], "fixed": [[42, 3]]}]
        for graph in graphs:
            order = list(reversed(graph["vertices"]))
            frozen = deepcopy((graph, order))
            result = solve(graph, elimination_order=order)
            self.check_result(graph, result)
            self.assertEqual((graph, order), frozen)
            self.assertEqual(result, solve(graph, elimination_order=order))

    def test_bad_orders_are_rejected_before_any_search(self):
        graph = reference.cycle(3)
        for order in ([0, 1], [0, 1, 1], [0, 1, 9], [0, 1, 2, 3],
                      [False, 1, 2], [0.0, 1, 2], "012", 2):
            with self.subTest(order=order):
                with self.assertRaises(ValueError):
                    solve(graph, elimination_order=order, max_checks=0)


class RegionPlannerTests(unittest.TestCase):
    strategies = ("min_degree", "geometric_sweep", "geometric_nested",
                  "bfs_nested", "bfs_sweep")

    def setUp(self):
        from four_color_region_order import build_region_order
        self.plan = build_region_order
        self.reference = reference.LocalMessageTests()

    @staticmethod
    def grid(rows, columns):
        vertices = [101 + 7 * i for i in range(rows * columns)]
        positions = {vertices[y * columns + x]: (x, y)
                     for y in range(rows) for x in range(columns)}
        edges = []
        for y in range(rows):
            for x in range(columns):
                v = vertices[y * columns + x]
                if x + 1 < columns:
                    edges.append([v, vertices[y * columns + x + 1]])
                if y + 1 < rows:
                    edges.append([v, vertices[(y + 1) * columns + x]])
        return {"vertices": vertices, "edges": edges}, positions

    def check_split_edges(self, graph, plan):
        for split in plan["splits"]:
            region = set(split["region"])
            separator = set(split["separator"])
            interiors = list(map(set, split["interiors"]))
            self.assertTrue(separator <= region)
            self.assertGreaterEqual(len(interiors), 2)
            self.assertEqual(separator | set().union(*interiors), region)
            self.assertEqual(sum(map(len, interiors)) + len(separator), len(region))
            for interior in interiors:
                self.assertFalse(interior & separator)
            membership = {v: i for i, interior in enumerate(interiors) for v in interior}
            # No candidate geometry may hide an actual edge connecting the
            # private interiors on opposite sides of a separator.
            for u, v in graph["edges"]:
                if u in membership and v in membership:
                    self.assertEqual(membership[u], membership[v])
            self.assertFalse(region & set(split["external_boundary"]))

    def test_each_planner_retains_exact_original_graph_semantics(self):
        rng = random.Random(826103)
        for case in range(12):
            vertices = [53, -17, 9001, 0, 72, -44]
            rng.shuffle(vertices)
            positions = {v: (i % 3, i // 3) for i, v in enumerate(vertices)}
            graph = {"vertices": vertices,
                     "edges": [list(edge) for edge in combinations(vertices, 2)
                               if rng.random() < .37],
                     "fixed": [[vertices[0], case % 4]]}
            domains = {v: [c for c in range(4) if rng.random() < .8] for v in vertices}
            expected = bool(reference.original_solutions(graph, domains, first_only=True))
            frozen = deepcopy((graph, positions, domains))
            for strategy in self.strategies:
                with self.subTest(case=case, strategy=strategy):
                    plan = self.plan(graph, strategy, positions=positions, leaf_size=2)
                    self.assertEqual(plan["status"], "planned")
                    self.assertCountEqual(plan["order"], vertices)
                    self.check_split_edges(graph, plan)
                    result = solve(graph, domains=domains, elimination_order=plan["order"])
                    self.assertEqual(result["status"], "colored" if expected else "unsatisfiable")
                    self.reference.check_decomposition(graph, result)
                    self.reference.check_messages(graph, result, domains)
                    if expected:
                        self.reference.check_coloring(graph, result, domains)
                    else:
                        self.assertIsNone(result["colors"])
                    self.assertEqual(plan["stats"]["peak_filled_boundary"],
                                     result["stats"]["max_separator_size"])
            self.assertEqual((graph, positions, domains), frozen)

    def test_recursive_splits_include_real_edges_and_are_deterministic(self):
        graph, positions = self.grid(4, 5)
        # Deliberately bypass a coordinate line. Geometry alone must never
        # make this edge disappear from the decomposition or split check.
        graph["edges"].append([graph["vertices"][0], graph["vertices"][-1]])
        frozen = deepcopy((graph, positions))
        for strategy in self.strategies:
            with self.subTest(strategy=strategy):
                plan = self.plan(graph, strategy, positions=positions, leaf_size=2)
                self.assertEqual(plan["status"], "planned")
                self.assertCountEqual(plan["order"], graph["vertices"])
                self.check_split_edges(graph, plan)
                self.assertEqual(plan, self.plan(graph, strategy, positions=positions, leaf_size=2))
                result = solve(graph, elimination_order=plan["order"])
                self.reference.check_decomposition(graph, result)
                self.reference.check_coloring(graph, result)
                self.assertEqual(plan["stats"]["peak_filled_boundary"],
                                 result["stats"]["max_separator_size"])
        self.assertEqual((graph, positions), frozen)

    def test_planner_limits_never_publish_partial_order(self):
        graph, positions = self.grid(3, 4)
        for strategy in self.strategies:
            full = self.plan(graph, strategy, positions=positions, leaf_size=2)
            self.assertEqual(full["status"], "planned")
            count = full["stats"]["checks"]
            for budget in (0, 1, count - 1, count):
                with self.subTest(strategy=strategy, budget=budget):
                    plan = self.plan(graph, strategy, positions=positions,
                                     leaf_size=2, max_checks=budget)
                    self.assertLessEqual(plan["stats"]["checks"], budget)
                    if budget < count:
                        self.assertEqual(plan["status"], "limit")
                        self.assertIsNone(plan["order"])
                    else:
                        self.assertEqual(plan, full)

    def test_geometry_is_optional_only_for_graph_based_planners(self):
        graph, positions = self.grid(2, 3)
        for strategy in ("min_degree", "bfs_nested", "bfs_sweep"):
            self.assertEqual(self.plan(graph, strategy)["status"], "planned")
        for strategy in ("geometric_sweep", "geometric_nested"):
            for invalid in (None, {}, {**positions, graph["vertices"][0]: (float("nan"), 0)},
                            {**positions, graph["vertices"][0]: (float("inf"), 0)}):
                with self.subTest(strategy=strategy, positions=invalid):
                    with self.assertRaises(ValueError):
                        self.plan(graph, strategy, positions=invalid)


if __name__ == "__main__":
    unittest.main()
