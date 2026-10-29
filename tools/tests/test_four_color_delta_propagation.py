"""Monotone full-interface support and dirty-pair queues preserve exact joins."""

from dataclasses import dataclass
from itertools import product, combinations
from pathlib import Path
import random
import json
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import test_four_color_bucket_flow as bucket_tests

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_constraints import solve_constraints
from four_color_intersections import SharedInterfaceIndex, intersect_on_shared


@dataclass(eq=False)
class Factor:
    scope: tuple
    rows: frozenset
    revision: int = 0


def commit(index, left, right, answer):
    for factor, rows in ((left, answer["left_rows"]), (right, answer["right_rows"])):
        if factor.rows != rows:
            factor.rows = rows
            factor.revision += 1
    index.mark_seen(left, right, support_count=len(answer["common_rows"]))


class DeltaIndexTests(unittest.TestCase):
    def test_full_scope_view_keeps_literal_coordinates_without_copying(self):
        left = Factor((0, 1), frozenset({(0, 1), (1, 0), (2, 3)}))
        right = Factor((0, 1, 2), frozenset({(0, 1, 3), (1, 0, 2)}))
        index = SharedInterfaceIndex(cache_max_rows=100, monotone_updates=True)
        index.sync([left, right])
        answer = index.intersect(left, right)
        self.assertEqual(answer, intersect_on_shared(left.scope, left.rows, right.scope, right.rows))
        self.assertEqual(index.delta_stats["full_scope_views"], 1)
        self.assertEqual(index.cache_stats["rows"], len(right.rows))
        self.assertEqual(answer["left_rows"], frozenset({(0, 1), (1, 0)}))

    def test_private_row_loss_does_not_filter_unchanged_interface(self):
        left = Factor((0, 1, 2), frozenset(product(range(2), repeat=3)))
        right = Factor((1, 0, 3), frozenset(product(range(2), repeat=3)))
        index = SharedInterfaceIndex(cache_max_rows=100, monotone_updates=True)
        index.sync([left, right])
        commit(index, left, right, index.intersect(left, right))
        left.rows = frozenset(row for row in left.rows if row[2] == 0)
        left.revision += 1
        index.sync([left, right])
        answer = index.intersect(left, right)
        self.assertEqual(answer, intersect_on_shared(left.scope, left.rows, right.scope, right.rows))
        self.assertIs(answer["right_rows"], right.rows)
        self.assertEqual(index.delta_stats["support_reuses"], 1)

    def test_support_loss_propagates_whole_tuples_in_reversed_frames(self):
        left = Factor((90, -3, 7), frozenset(product(range(2), repeat=3)))
        right = Factor((7, 19, -3), frozenset(product(range(2), repeat=3)))
        index = SharedInterfaceIndex(cache_max_rows=100, monotone_updates=True)
        index.sync([left, right])
        commit(index, left, right, index.intersect(left, right))
        left.rows = frozenset(row for row in left.rows if row[1] != row[2])
        left.revision += 1
        index.sync([right, left])
        answer = index.intersect(right, left)
        self.assertEqual(answer, intersect_on_shared(right.scope, right.rows, left.scope, left.rows))
        self.assertEqual(answer["common_rows"], frozenset({(0, 1), (1, 0)}))
        self.assertTrue(all(row[0] != row[2] for row in answer["left_rows"]))

    def test_two_changed_projections_need_the_full_joint_intersection(self):
        left = Factor((0, 1, 2), frozenset(product(range(2), repeat=3)))
        right = Factor((2, 1, 0), frozenset(product(range(2), repeat=3)))
        index = SharedInterfaceIndex(cache_max_rows=100, monotone_updates=True)
        index.sync([left, right])
        commit(index, left, right, index.intersect(left, right))
        left.rows = frozenset(row for row in left.rows if sum(row) % 2 == 0)
        right.rows = frozenset(row for row in right.rows if sum(row) % 2 == 1)
        left.revision += 1
        right.revision += 1
        index.sync([left, right])
        answer = index.intersect(left, right)
        self.assertFalse(answer["common_rows"])
        self.assertEqual(index.delta_stats["support_reuses"], 0)

    def test_random_monotone_updates_match_pure_semijoin_with_evictions(self):
        rng = random.Random(20261027)
        for capacity in (0, 3, 100):
            for trial in range(12):
                left = Factor((9, -2, 7), frozenset(product(range(3), repeat=3)))
                right = Factor((7, 18, -2), frozenset(product(range(3), repeat=3)))
                index = SharedInterfaceIndex(cache_max_rows=capacity, monotone_updates=True)
                for step in range(8):
                    index.sync([left, right] if step % 2 else [right, left])
                    expected = intersect_on_shared(left.scope, left.rows, right.scope, right.rows)
                    answer = index.intersect(left, right)
                    self.assertEqual(answer, expected)
                    commit(index, left, right, answer)
                    for factor in (left, right):
                        if rng.random() < .7:
                            factor.rows = frozenset(row for row in sorted(factor.rows) if rng.random() < .8)
                            factor.revision += 1
                    self.assertLessEqual(index.cache_stats["rows"], capacity)

    def test_every_interruption_keeps_inputs_and_retry_exact(self):
        class Interrupted(Exception):
            pass

        def setup():
            left = Factor((0, 1, 2), frozenset(product(range(3), repeat=3)))
            right = Factor((1, 0, 3), frozenset(product(range(3), repeat=3)))
            index = SharedInterfaceIndex(cache_max_rows=100, monotone_updates=True)
            index.sync([left, right])
            commit(index, left, right, index.intersect(left, right))
            left.rows = frozenset(row for row in left.rows if row[0] != row[1])
            left.revision += 1
            index.sync([left, right])
            return index, left, right

        index, left, right = setup()
        charges = []
        index.intersect(left, right, charge=lambda: charges.append(1))
        for stop in range(len(charges)):
            index, left, right = setup()
            before = (left.rows, left.revision, right.rows, right.revision)
            count = 0
            def charge():
                nonlocal count
                if count == stop:
                    raise Interrupted
                count += 1
            with self.assertRaises(Interrupted):
                index.intersect(left, right, charge=charge)
            self.assertEqual(before, (left.rows, left.revision, right.rows, right.revision))
            self.assertEqual(list(index.pending_pairs()), [(left, right)])
            self.assertEqual(index.intersect(left, right),
                             intersect_on_shared(left.scope, left.rows, right.scope, right.rows))

    def test_dirty_queue_revisits_earlier_pairs_only_next_pass(self):
        first, middle, last = [Factor((0, 1, v), frozenset(product(range(2), repeat=3)))
                               for v in (2, 3, 4)]
        index = SharedInterfaceIndex(cache_max_rows=100, monotone_updates=True)
        index.sync([first, middle, last])
        for left, right in index.pending_pairs():
            commit(index, left, right, index.intersect(left, right))
        self.assertEqual(list(index.pending_pairs()), [])
        last.rows = frozenset(row for row in last.rows if row[0] == row[1])
        last.revision += 1
        index.sync([first, middle, last])
        visits = []
        for left, right in index.pending_pairs():
            visits.append((left, right))
            commit(index, left, right, index.intersect(left, right))
        self.assertEqual(visits, [(first, last), (middle, last)])
        self.assertEqual(list(index.pending_pairs()), [(first, middle)])
        commit(index, first, middle, index.intersect(first, middle))
        self.assertEqual(list(index.pending_pairs()), [])

    def test_replacement_and_retirement_cannot_inherit_seen_support(self):
        left, right = [Factor((0, 1), frozenset({(0, 0)})) for _ in range(2)]
        index = SharedInterfaceIndex(cache_max_rows=100, monotone_updates=True)
        index.sync([left, right])
        commit(index, left, right, index.intersect(left, right))
        replacement = Factor((0, 1), frozenset({(1, 1)}))
        index.sync([right, replacement])
        self.assertEqual(list(index.pending_pairs()), [(right, replacement)])
        self.assertFalse(index.intersect(right, replacement)["common_rows"])
        index.sync([])
        self.assertEqual(index._support_counts, {})
        self.assertEqual(index._pending, set())

    def test_abandoned_queue_query_is_retried(self):
        left, right = [Factor((0, 1), frozenset({(0, 0), (1, 1)})) for _ in range(2)]
        index = SharedInterfaceIndex(cache_max_rows=100, monotone_updates=True)
        index.sync([left, right])
        pending = index.pending_pairs()
        self.assertEqual(next(pending), (left, right))
        pending.close()
        self.assertEqual(list(index.pending_pairs()), [(left, right)])
        commit(index, left, right, index.intersect(left, right))
        self.assertEqual(list(index.pending_pairs()), [])

    def test_interrupted_topology_sync_does_not_publish_new_pending_pairs(self):
        left, right = [Factor((0, 1), frozenset({(0, 0)})) for _ in range(2)]
        index = SharedInterfaceIndex(cache_max_rows=100, monotone_updates=True)
        index.sync([left, right])
        commit(index, left, right, index.intersect(left, right))
        new = Factor((0, 1), frozenset({(1, 1)}))
        def interrupt():
            raise RuntimeError("interrupted")
        with self.assertRaises(RuntimeError):
            index.sync([left, right, new], charge=interrupt)
        self.assertEqual(list(index.pending_pairs()), [])
        index.sync([left, right, new])
        self.assertEqual(list(index.pending_pairs()), [(left, new), (right, new)])


class DeltaSolverTests(bucket_tests.BucketFlowTests):
    def solve(self, graph, **options):
        if options.get("use_intersections", True):
            options.update(propagation_method="delta", use_interface_cache=True)
        return super().solve(graph, **options)

    def test_fixed_graphs_preserve_exact_records_across_partitions_and_caches(self):
        rng = random.Random(41027)
        for trial in range(12):
            graph = dict(vertices=list(range(7)), edges=[list(e) for e in combinations(range(7), 2)
                         if rng.random() < .45], fixed=[[0, trial % 4]])
            for partition in ("none", "information", "message"):
                for cache in (False, True):
                    options = dict(use_intersections=True, use_interface_cache=cache,
                                   use_cycles=True, use_cycle_contexts=True,
                                   partition_strategy=partition, partition_block_size=3,
                                   bucket_method="prefix", max_checks=1_000_000)
                    scan = solve_constraints(graph, propagation_method="scan", **options)
                    delta = solve_constraints(graph, propagation_method="delta", **options)
                    self.assertEqual(scan["status"], delta["status"])
                    self.assertNotEqual(delta["status"], "limit")
                    self.assertEqual(scan["elimination_records"], delta["elimination_records"])
                    self.assertEqual(scan["colors"], delta["colors"])
                    self.assert_complete_join_fibres(delta)

    def test_storage_limits_preserve_only_complete_records(self):
        graph = dict(vertices=list(range(5)), edges=[[i, (i+1) % 5] for i in range(5)])
        for method in ("anchor", "prefix"):
            complete = self.solve(graph, bucket_method=method)
            for cap in (0, 1, 12, 24, 60, 100):
                result = self.solve(graph, max_table_rows=cap, bucket_method=method)
                self.assert_complete_join_fibres(result)
                records = result["elimination_records"]
                self.assertEqual(records, complete["elimination_records"][:len(records)])
                if result["status"] == "limit":
                    self.assertEqual(result["colors"], [-1] * 5)
                    self.assertEqual(result["stats"]["writebacks"], 0)

    def test_api_cli_flags_and_rejected_combinations(self):
        graph = dict(vertices=list(range(4)), edges=[[i, (i+1) % 4] for i in range(4)])
        for value in (None, True, [], "DELTA"):
            with self.assertRaises(ValueError):
                solve_constraints(graph, propagation_method=value)
        with self.assertRaises(ValueError):
            solve_constraints(graph, propagation_method="delta")
        with TemporaryDirectory() as directory:
            source, output = Path(directory)/"graph.json", Path(directory)/"result.json"
            source.write_text(json.dumps(graph))
            command = [sys.executable, str(ROOT/"scripts/four_color_lab.py"), "solve", str(source),
                       "--propagation-method", "delta", "--json", str(output)]
            run = subprocess.run(command + ["--engine", "constraints", "--intersections"],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(output.read_text())["propagation_method"], "delta")
            for flags in (["--engine", "search"], ["--engine", "constraints"]):
                run = subprocess.run(command + flags, capture_output=True, text=True)
                self.assertNotEqual(run.returncode, 0)


if __name__ == "__main__":
    unittest.main()
