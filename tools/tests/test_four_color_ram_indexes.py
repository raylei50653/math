"""Retained full-interface groups trade memory for repeated semijoin work."""

from copy import deepcopy
from dataclasses import dataclass
import gc
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
import weakref


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_intersections import SharedInterfaceIndex, intersect_on_shared
from four_color_constraints import solve_constraints
from four_color_conflict_priority import original_solutions, verify_preservation


@dataclass(eq=False)
class Factor:
    scope: tuple
    rows: frozenset
    revision: int = 0


def private_coordinate_pair():
    left = Factor((90, -5, 17), frozenset(product(range(4), repeat=3)))
    right = Factor((17, 44, -5),
                   frozenset((second, private, first)
                             for first, second in ((0, 1), (1, 2), (2, 3))
                             for private in (0, 3)))
    return left, right


class RamInterfaceIndexTests(unittest.TestCase):
    def oracle(self, left, right):
        return intersect_on_shared(left.scope, left.rows, right.scope, right.rows)

    def assert_budget(self, index, cap):
        self.assertLessEqual(index.cache_stats["rows"], cap)
        self.assertLessEqual(index.cache_stats["peak_rows"], cap)

    def test_default_zero_capacity_keeps_uncached_semantics_work_and_zero_stats(self):
        left, right = private_coordinate_pair()
        index = SharedInterfaceIndex()
        index.sync([left, right])
        expected_charges, actual_charges = [], []
        expected = intersect_on_shared(left.scope, left.rows, right.scope, right.rows,
                                       charge=lambda: expected_charges.append(None))
        actual = index.intersect(left, right, charge=lambda: actual_charges.append(None))
        self.assertEqual(actual, expected)
        self.assertEqual(actual_charges, expected_charges)
        self.assertTrue(all(value == 0 for value in index.cache_stats.values()))

    def test_complete_private_rows_are_retained_and_warm_queries_do_less_work(self):
        left, right = private_coordinate_pair()
        before = (left.scope, left.rows, left.revision, right.scope, right.rows, right.revision)
        index = SharedInterfaceIndex(cache_max_rows=200)
        index.sync([left, right])
        cold, warm, uncached = [], [], []
        expected = intersect_on_shared(left.scope, left.rows, right.scope, right.rows,
                                       charge=lambda: uncached.append(None))
        first = index.intersect(left, right, charge=lambda: cold.append(None))
        second = index.intersect(left, right, charge=lambda: warm.append(None))
        self.assertEqual(first, expected)
        self.assertEqual(second, expected)
        self.assertLess(len(warm), len(cold))
        self.assertLess(len(warm), len(uncached))
        self.assertEqual(index.cache_stats["rows"], len(left.rows) + len(right.rows))
        self.assertGreater(index.cache_stats["hits"], 0)
        self.assertGreater(index.cache_stats["builds"], 0)
        self.assertGreater(index.cache_stats["entries"], 0)
        self.assert_budget(index, 200)
        self.assertEqual(before, (left.scope, left.rows, left.revision,
                                  right.scope, right.rows, right.revision))
        for first_colour, second_colour in expected["common_rows"]:
            self.assertEqual({row[0] for row in second["left_rows"]
                              if row[1:] == (first_colour, second_colour)}, set(range(4)))

    def test_full_shared_triples_and_both_scope_orders_match_pure_oracle(self):
        left = Factor((0, 1, 2, 8), frozenset((*row, private)
                      for row in product(range(2), repeat=3) if sum(row) % 2 == 0
                      for private in (0, 1)))
        right = Factor((2, 1, 0, 9), frozenset((row[2], row[1], row[0], private)
                       for row in product(range(2), repeat=3) if sum(row) % 2 == 1
                       for private in (2, 3)))
        index = SharedInterfaceIndex(cache_max_rows=100)
        index.sync([left, right])
        for first, second in ((left, right), (right, left), (left, right), (right, left)):
            answer = index.intersect(first, second)
            self.assertEqual(answer, self.oracle(first, second))
            self.assertEqual(answer["scope"], tuple(vertex for vertex in first.scope
                                                   if vertex in second.scope))
            self.assertFalse(answer["common_rows"])
            self.assertFalse(answer["left_rows"])
            self.assertFalse(answer["right_rows"])
        self.assert_budget(index, 100)

    def test_empty_disjoint_single_shared_and_scalar_relations_match_oracle(self):
        cases = [
            (Factor((1,), frozenset({(0,), (1,)})), Factor((2,), frozenset({(3,)}))),
            (Factor((1, 2), frozenset({(0, 1), (1, 2)})),
             Factor((2, 3), frozenset({(1, 0)}))),
            (Factor((), frozenset({()})), Factor((1,), frozenset({(2,)}))),
            (Factor((1, 2), frozenset()), Factor((2, 1), frozenset({(1, 0)}))),
        ]
        for left, right in cases:
            with self.subTest(left=left.scope, right=right.scope):
                index = SharedInterfaceIndex(cache_max_rows=20)
                index.sync([left, right])
                self.assertEqual(index.intersect(left, right), self.oracle(left, right))
                self.assertEqual(index.intersect(right, left), self.oracle(right, left))

    def test_late_revision_and_mark_seen_release_obsolete_groups(self):
        left = Factor((0, 1), frozenset({(0, 0), (1, 1)}))
        right = Factor((1, 0, 2), frozenset({(0, 0, 3)}))
        index = SharedInterfaceIndex(cache_max_rows=20)
        index.sync([left, right])
        answer = index.intersect(left, right)
        self.assertEqual(answer, self.oracle(left, right))
        left.rows = answer["left_rows"]
        left.revision += 1
        index.mark_seen(left, right)
        self.assertEqual(index.cache_stats["rows"], len(right.rows))
        self.assertTrue(index.seen(left, right))
        self.assertEqual(index.intersect(left, right), self.oracle(left, right))
        # Lookup must also invalidate changed rows before a later sync/mark.
        right.rows = frozenset({(1, 1, 2)})
        right.revision += 1
        self.assertFalse(index.seen(left, right))
        answer = index.intersect(left, right)
        self.assertEqual(answer, self.oracle(left, right))
        self.assertFalse(answer["common_rows"])

    def test_replacement_at_same_list_position_cannot_inherit_revision_zero_groups(self):
        old = Factor((0, 1), frozenset({(0, 0)}))
        right = Factor((1, 0), frozenset({(0, 0)}))
        index = SharedInterfaceIndex(cache_max_rows=20)
        index.sync([old, right])
        self.assertEqual(index.intersect(old, right), self.oracle(old, right))
        index.mark_seen(old, right)
        replacement = Factor(old.scope, frozenset({(1, 1)}))
        index.sync([right, replacement])
        self.assertFalse(index.seen(right, replacement))
        answer = index.intersect(replacement, right)
        self.assertEqual(answer, self.oracle(replacement, right))
        self.assertFalse(answer["common_rows"])
        self.assertEqual(index.cache_stats["rows"], len(right.rows) + len(replacement.rows))

    def test_lru_eviction_and_oversized_entry_fallback_preserve_complete_rows(self):
        left = Factor((0, 1), frozenset({(0, 0), (1, 1)}))
        right = Factor((1, 0), frozenset({(0, 0), (2, 2)}))
        index = SharedInterfaceIndex(cache_max_rows=len(left.rows))
        index.sync([left, right])
        for _ in range(3):
            self.assertEqual(index.intersect(left, right), self.oracle(left, right))
            self.assert_budget(index, len(left.rows))
        self.assertGreater(index.cache_stats["evictions"], 0)
        self.assertEqual(index.cache_stats["entries"], 1)
        large, small = private_coordinate_pair()
        bounded = SharedInterfaceIndex(cache_max_rows=len(small.rows))
        bounded.sync([large, small])
        for _ in range(2):
            self.assertEqual(bounded.intersect(large, small), self.oracle(large, small))
            self.assert_budget(bounded, len(small.rows))
        self.assertEqual(bounded.cache_stats["rows"], len(small.rows))
        self.assertGreater(bounded.cache_stats["hits"], 0)

    def test_every_charged_interruption_publishes_only_complete_reusable_groups(self):
        left = Factor((0, 1, 2), frozenset({(0, 0, 3), (1, 1, 2), (2, 2, 1)}))
        right = Factor((1, 0, 4), frozenset({(0, 0, 0), (1, 1, 2)}))
        expected = self.oracle(left, right)
        reference, charges = SharedInterfaceIndex(cache_max_rows=20), []
        reference.sync([left, right])
        reference.intersect(left, right, charge=lambda: charges.append(None))
        before = (left.scope, left.rows, left.revision, right.scope, right.rows, right.revision)

        class Interrupted(Exception):
            pass

        for stop_at in range(len(charges)):
            index, visited = SharedInterfaceIndex(cache_max_rows=20), 0
            index.sync([left, right])

            def charge():
                nonlocal visited
                if visited == stop_at:
                    raise Interrupted
                visited += 1

            with self.subTest(stop_at=stop_at):
                with self.assertRaises(Interrupted):
                    index.intersect(left, right, charge=charge)
                self.assertEqual(before, (left.scope, left.rows, left.revision,
                                          right.scope, right.rows, right.revision))
                if stop_at <= len(left.rows):
                    self.assertEqual(index.cache_stats["builds"], 0)
                    self.assertEqual(index.cache_stats["rows"], 0)
                    self.assertEqual(index.cache_stats["entries"], 0)
                self.assert_budget(index, 20)
                self.assertEqual(index.intersect(left, right), expected)

    def test_interrupted_build_does_not_evict_an_existing_completed_index(self):
        left = Factor((0, 1), frozenset({(0, 0), (1, 1)}))
        right = Factor((0, 1), frozenset({(0, 0), (2, 2)}))
        new = Factor((0, 1), frozenset({(0, 0), (3, 3)}))
        capacity = len(left.rows) + len(right.rows)
        index = SharedInterfaceIndex(cache_max_rows=capacity)
        index.sync([left, right])
        index.intersect(left, right)
        index.sync([left, right, new])
        before = dict(index.cache_stats)
        visited = 0

        class Interrupted(Exception):
            pass

        def charge():
            nonlocal visited
            if visited == len(new.rows):
                raise Interrupted
            visited += 1

        with self.assertRaises(Interrupted):
            index.intersect(new, left, charge=charge)
        self.assertEqual(index.cache_stats, before)
        self.assertEqual(index.intersect(new, left), self.oracle(new, left))
        self.assert_budget(index, capacity)

    def test_retiring_cached_factor_releases_its_identity_and_all_retained_rows(self):
        left, right = private_coordinate_pair()
        reference = weakref.ref(left)
        index = SharedInterfaceIndex(cache_max_rows=200)
        index.sync([left, right])
        index.intersect(left, right)
        index.sync([right])
        del left
        gc.collect()
        self.assertIsNone(reference())
        self.assertEqual(index.cache_stats["rows"], len(right.rows))
        index.sync([])
        self.assertEqual(index.cache_stats["rows"], 0)
        self.assertEqual(index.cache_stats["entries"], 0)

    def test_capacity_validation_rejects_nonexact_integer_and_negative_values(self):
        for value in (-1, True, False, 1.0, "10", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    SharedInterfaceIndex(cache_max_rows=value)

    def test_pending_pair_order_and_skip_count_match_pairs_with_seen(self):
        factors = [Factor((0, 1, vertex), frozenset({(0, 1, 2)})) for vertex in (2, 3, 4)]
        index = SharedInterfaceIndex(cache_max_rows=20)
        index.sync(factors)
        index.mark_seen(factors[0], factors[2])
        expected = [pair for pair in index.pairs() if not index.seen(*pair)]
        skipped = sum(index.seen(*pair) for pair in index.pairs())
        self.assertEqual(list(index.pending_pairs()), expected)
        self.assertEqual(index.skipped_pair_queries, skipped)
        self.assertEqual(list(index.pending_pairs()), expected)
        self.assertEqual(index.skipped_pair_queries, 2 * skipped)
        index.sync(list(reversed(factors)))
        expected = [pair for pair in index.pairs() if not index.seen(*pair)]
        self.assertEqual(list(index.pending_pairs()), expected)

    def test_pending_generator_observes_late_revision_changes_before_each_yield(self):
        first, middle, last = [Factor((0, 1, vertex), frozenset({(0, 1, 2)}))
                               for vertex in (2, 3, 4)]
        index = SharedInterfaceIndex()
        index.sync([first, middle, last])
        index.mark_seen(first, last)
        index.mark_seen(middle, last)
        pending = index.pending_pairs()
        self.assertEqual(next(pending), (first, middle))
        last.revision += 1
        self.assertEqual(next(pending), (first, last))
        index.mark_seen(first, last)
        self.assertEqual(next(pending), (middle, last))
        with self.assertRaises(StopIteration):
            next(pending)
        self.assertEqual(index.skipped_pair_queries, 0)

    def test_ordered_pair_array_is_reused_until_topology_changes(self):
        left, right = private_coordinate_pair()
        index = SharedInterfaceIndex(cache_max_rows=200)
        index.sync([left, right])
        retained = index._ordered_pairs
        index.intersect(left, right)
        index.mark_seen(left, right)
        index.sync([left, right], charge=lambda: self.fail("unchanged pair was rediscovered"))
        self.assertIs(index._ordered_pairs, retained)
        left.revision += 1
        index.sync([left, right])
        self.assertIs(index._ordered_pairs, retained)
        self.assertEqual(index.cache_stats["rows"], len(right.rows))
        self.assertEqual(list(index.pending_pairs()), [(left, right)])
        index.sync([right, left])
        self.assertIsNot(index._ordered_pairs, retained)
        self.assertEqual(list(index.pending_pairs()), [(right, left)])

    def test_pending_array_releases_retired_factors_and_new_revision_zero_pair_is_pending(self):
        left = Factor((0, 1), frozenset({(0, 0)}))
        right = Factor((1, 0), frozenset({(0, 0)}))
        reference = weakref.ref(left)
        index = SharedInterfaceIndex()
        index.sync([left, right])
        index.mark_seen(left, right)
        self.assertEqual(list(index.pending_pairs()), [])
        index.sync([right])
        del left
        gc.collect()
        self.assertIsNone(reference())
        replacement = Factor((0, 1), frozenset({(1, 1)}))
        index.sync([right, replacement])
        self.assertEqual(list(index.pending_pairs()), [(right, replacement)])


class RamIndexCoreFlowTests(unittest.TestCase):
    def solve(self, graph, **options):
        settings = dict(use_intersections=True, use_conflicts=False,
                        use_cycles=True, use_cycle_contexts=True,
                        cycle_context_search="partial", use_interface_cache=True,
                        interface_cache_max_rows=1_000_000, max_table_rows=1_000_000,
                        max_checks=5_000_000, trace_limit=10000, record_relations=True)
        settings.update(options)
        return solve_constraints(graph, **settings)

    def assert_complete_fibres(self, result):
        for record in result["elimination_records"]:
            self.assertTrue(record["complete"])
            variables = [record["vertex"], *record["scope"]]
            domains = {item["vertex"]: item["colors"] for item in record["source_domains"]}
            inputs = [(relation["scope"], {tuple(row) for row in relation["rows"]})
                      for relation in record["input_relations"]]
            expected = {}
            for colors in product(*(domains[vertex] for vertex in variables)):
                assignment = dict(zip(variables, colors))
                if all(tuple(assignment[vertex] for vertex in scope) in rows
                       for scope, rows in inputs):
                    boundary = tuple(assignment[vertex] for vertex in record["scope"])
                    expected.setdefault(boundary, set()).add(assignment[record["vertex"]])
            actual = {tuple(row["boundary"]): set(row["colors"]) for row in record["rows"]}
            self.assertEqual(len(actual), len(record["rows"]))
            self.assertEqual(actual, expected)

    def test_cache_flag_preserves_all_nine_point_solutions_and_fixed_gap(self):
        cases = json.loads((ROOT / "artifacts/four_color_guarantee_gap/inputs.json").read_text())
        fixed = deepcopy(next(case["graph"] for case in cases if case["role"] == "secondary-gap"))
        unfixed = dict(deepcopy(fixed), fixed=[])
        for graph, count in ((unfixed, 48), (fixed, 0)):
            with self.subTest(fixed=graph["fixed"]):
                before = deepcopy(graph)
                solutions = list(original_solutions(graph))
                self.assertEqual(len(solutions), count)
                result = self.solve(graph)
                self.assertTrue(verify_preservation(graph, solutions, result)["all_solutions_preserved"])
                self.assert_complete_fibres(result)
                self.assertGreater(result["stats"]["interface_cache_builds"], 0)
                self.assertGreater(result["stats"]["interface_cache_peak_rows"], 0)
                self.assertGreater(result["stats"]["interface_cover_index_builds"], 0)
                self.assertEqual(graph, before)
                if count:
                    self.assertEqual(result["status"], "colored")
                    positions = {vertex: offset for offset, vertex in enumerate(graph["vertices"])}
                    for event in result["events"]:
                        if event.get("relation_kind") != "cycle_context":
                            continue
                        for field in ("pair_relations", "cycle_edge_relations", "context_edge_relations"):
                            for relation in event[field]:
                                rows = {tuple(row) for row in relation["rows"]}
                                offsets = [positions[vertex] for vertex in relation["scope"]]
                                for solution in solutions:
                                    self.assertIn(tuple(solution[offset] for offset in offsets), rows)
                else:
                    self.assertEqual(result["status"], "unsatisfiable")
                    self.assertEqual(result["stats"]["eliminations"], 0)
                    self.assertEqual(result["elimination_records"], [])

    def test_small_reversed_frame_and_zero_capacity_keep_every_source_solution_and_fibre(self):
        graph = dict(vertices=[42, -3, 80, 5, 900, 17],
                     edges=[[42, -3], [-3, 80], [80, 5], [5, 900], [900, 42], [17, 42]],
                     fixed=[[17, 2]])
        reverse = dict(vertices=list(reversed(graph["vertices"])),
                       edges=[[b, a] for a, b in reversed(graph["edges"])], fixed=[[17, 2]])
        for case, capacity in ((graph, 1_000_000), (reverse, 1_000_000), (reverse, 0)):
            with self.subTest(vertices=case["vertices"], capacity=capacity):
                solutions = list(original_solutions(case))
                result = self.solve(case, interface_cache_max_rows=capacity)
                self.assertEqual(result["status"], "colored")
                self.assertTrue(verify_preservation(case, solutions, result)["all_solutions_preserved"])
                self.assert_complete_fibres(result)
                self.assertGreater(result["stats"]["interface_cover_index_builds"], 0)
                if capacity == 0:
                    self.assertEqual(result["stats"]["interface_cache_peak_rows"], 0)

    def test_context_index_insertion_preflight_preserves_atomic_commit(self):
        masks = [14, 5, 11, 13, 3]
        graph = dict(vertices=list(range(5)), fixed=[],
                     edges=[[i, (i + 1) % 4] for i in range(4)] + [[4, i] for i in range(4)])
        for vertex, mask in enumerate(masks):
            for colour in range(4):
                if not mask & (1 << colour):
                    leaf = len(graph["vertices"])
                    graph["vertices"].append(leaf)
                    graph["edges"].append([vertex, leaf])
                    graph["fixed"].append([leaf, colour])
        complete = self.solve(graph, use_substructures=False)
        first = next(event for event in complete["events"] if event["kind"] == "cycle_context")
        additions, committed_at = first["context_factors_added"], first["stats"]["checks"]
        self.assertGreater(additions, 0)
        solutions = list(original_solutions(graph))
        fixed_colours = [dict(graph["fixed"]).get(vertex, -1) for vertex in graph["vertices"]]
        for budget in sorted({committed_at - 1, committed_at - additions,
                              committed_at - additions - 1}):
            with self.subTest(budget=budget):
                limited = self.solve(graph, use_substructures=False, max_checks=budget)
                self.assertEqual(limited["status"], "limit")
                self.assertEqual(limited["colors"], fixed_colours)
                self.assertEqual(limited["elimination_records"], [])
                self.assertEqual(limited["stats"]["cycle_context_factors"], 0)
                self.assertEqual(limited["stats"]["cycle_context_rows"], 0)
                self.assertEqual(limited["stats"]["cycle_context_prunes"], 0)
                self.assertFalse(any(event["kind"] == "cycle_context" for event in limited["events"]))
                final_domains = dict(zip(graph["vertices"], limited["events"][-1]["domains"]))
                self.assertEqual([sum(1 << colour for colour in final_domains[vertex])
                                  for vertex in first["frontier"]], first["domain_masks"])
                for solution in solutions:
                    self.assertTrue(all(colour in final_domains[vertex]
                                        for vertex, colour in zip(graph["vertices"], solution)))
        committed = self.solve(graph, use_substructures=False, max_checks=committed_at)
        self.assertEqual(committed["status"], "limit")
        self.assertEqual(committed["colors"], fixed_colours)
        self.assertEqual(committed["stats"]["cycle_context_factors"], additions)
        self.assertEqual(committed["stats"]["cycle_context_rows"], first["context_rows_added"])
        self.assertEqual(sum(event["kind"] == "cycle_context" for event in committed["events"]), 1)

    def test_core_cache_flags_require_intersections_and_exact_configuration_types(self):
        graph = dict(vertices=[0, 1], edges=[[0, 1]], fixed=[])
        with self.assertRaises(ValueError):
            solve_constraints(graph, use_interface_cache=True)
        for flag in (0, 1, None, "true"):
            with self.subTest(flag=flag):
                with self.assertRaises(ValueError):
                    solve_constraints(graph, use_intersections=True, use_interface_cache=flag)
        for capacity in (-1, True, False, 1.0, "128", None):
            with self.subTest(capacity=capacity):
                with self.assertRaises(ValueError):
                    solve_constraints(graph, use_intersections=True, use_interface_cache=True,
                                      interface_cache_max_rows=capacity)

    def test_cli_cache_flags_forward_capacity_and_reject_invalid_engine_combinations(self):
        graph = dict(vertices=[0, 1, 2, 3],
                     edges=[[0, 1], [1, 2], [2, 3], [3, 0]], fixed=[])
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "graph.json", Path(directory) / "result.json"
            source.write_text(json.dumps(graph))
            prefix = [sys.executable, str(ROOT / "scripts/four_color_lab.py"), "solve", str(source)]
            completed = subprocess.run(
                [*prefix, "--engine", "constraints", "--intersections", "--interface-cache",
                 "--interface-cache-max-rows", "128", "--max-table-rows", "1000000",
                 "--json", str(output)], capture_output=True, text=True, timeout=30)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(output.read_text())
            self.assertEqual(result["status"], "colored")
            self.assertTrue(result["use_interface_cache"])
            self.assertEqual(result["interface_cache_max_rows"], 128)
            solutions = list(original_solutions(graph))
            self.assertTrue(verify_preservation(graph, solutions, result)["all_solutions_preserved"])
            self.assert_complete_fibres(result)
            for flags in (("--engine", "constraints", "--interface-cache"),
                          ("--engine", "search", "--interface-cache")):
                with self.subTest(flags=flags):
                    rejected = subprocess.run([*prefix, *flags], capture_output=True,
                                              text=True, timeout=30)
                    self.assertNotEqual(rejected.returncode, 0)
                    self.assertTrue(rejected.stderr)


if __name__ == "__main__":
    unittest.main()
