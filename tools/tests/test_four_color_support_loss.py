"""Only a complete interface's last lost support can invalidate neighbour rows."""

from dataclasses import dataclass
from itertools import product, combinations
from pathlib import Path
import json
import random
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import test_four_color_bucket_flow as bucket_tests

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_intersections import SharedInterfaceIndex, intersect_on_shared
from four_color_constraints import solve_constraints
from four_color_propagation_experiment import semantic_record


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
    index.mark_seen(left, right, support_count=len(answer["common_rows"]),
                    common_rows=answer["common_rows"], common_scope=answer["scope"])


def shrink(factor, kept):
    factor.rows = frozenset(kept)
    factor.revision += 1


class SupportLossIndexTests(unittest.TestCase):
    def setup_pair(self, capacity=1000):
        left = Factor((0, 1, 2), frozenset(product(range(2), repeat=3)))
        right = Factor((1, 0, 3), frozenset(product(range(2), repeat=3)))
        index = SharedInterfaceIndex(cache_max_rows=capacity, monotone_updates=True, support_loss=True)
        index.sync([left, right])
        commit(index, left, right, index.intersect(left, right))
        return index, left, right

    def oracle(self, left, right):
        return intersect_on_shared(left.scope, left.rows, right.scope, right.rows)

    def assert_capacity(self, index, cap):
        retained = sum(entry[2] for entry in index._group_cache.values())
        retained += sum(len(entry[1]) for entry in index._messages.values())
        self.assertEqual(index.cache_stats["rows"], retained)
        self.assertLessEqual(retained, cap)
        self.assertLessEqual(index.cache_stats["peak_rows"], cap)

    def test_removed_row_projection_is_not_a_lost_support(self):
        index, left, right = self.setup_pair()
        before = right.rows
        shrink(left, left.rows - {(0, 1, 0)})
        answer = index.intersect(left, right)
        self.assertEqual(answer, self.oracle(left, right))
        self.assertIs(answer["right_rows"], before)
        self.assertEqual(index.delta_stats["loss_tuples"], 0)
        self.assertEqual(index.delta_stats["loss_empty"], 1)
        commit(index, left, right, answer)
        # Removing the OTHER row loses the last support for this ordered pair.
        shrink(left, left.rows - {(0, 1, 1)})
        answer = index.intersect(left, right)
        self.assertEqual(answer, self.oracle(left, right))
        self.assertEqual(before - answer["right_rows"], frozenset({(1, 0, 0), (1, 0, 1)}))
        self.assertEqual(index.delta_stats["loss_tuples"], 1)

    def test_both_sides_lose_different_whole_supports(self):
        index, left, right = self.setup_pair()
        shrink(left, (r for r in left.rows if r[:2] != (0, 1)))
        shrink(right, (r for r in right.rows if r[:2] != (0, 1)))
        answer = index.intersect(left, right)
        self.assertEqual(answer, self.oracle(left, right))
        self.assertEqual(answer["common_rows"], frozenset({(0, 0), (1, 1)}))
        self.assertEqual(index.delta_stats["loss_tuples"], 2)

    def test_both_private_changes_with_equal_projections_emit_no_loss(self):
        index, left, right = self.setup_pair()
        shrink(left, (r for r in left.rows if r[2] == 0))
        shrink(right, (r for r in right.rows if r[2] == 1))
        answer = index.intersect(left, right)
        self.assertEqual(answer, self.oracle(left, right))
        self.assertEqual(index.delta_stats["loss_empty"], 1)
        self.assertEqual(index.delta_stats["loss_rows_removed"], 0)

    def test_joint_parity_rejection_cannot_be_replaced_by_marginals(self):
        all_rows = frozenset(product(range(2), repeat=3))
        left, right = Factor((0, 1, 2), all_rows), Factor((0, 1, 2), all_rows)
        index = SharedInterfaceIndex(cache_max_rows=100, monotone_updates=True, support_loss=True)
        index.sync([left, right])
        commit(index, left, right, index.intersect(left, right))
        shrink(left, (r for r in left.rows if sum(r) % 2 == 0))
        shrink(right, (r for r in right.rows if sum(r) % 2 == 1))
        self.assertFalse(index.intersect(left, right)["common_rows"])
        self.assertEqual(index.delta_stats["loss_tuples"], 8)

    def test_reordering_replacement_and_retirement_invalidate_checkpoints(self):
        index, left, right = self.setup_pair()
        shrink(left, (r for r in left.rows if r[0] == r[1]))
        index.sync([right, left])
        # Shared order changed: use a complete fallback, then save that frame.
        answer = index.intersect(right, left)
        self.assertEqual(answer, self.oracle(right, left))
        commit(index, right, left, answer)
        replacement = Factor(left.scope, frozenset({(0, 1, 0)}))
        index.sync([right, replacement])
        self.assertFalse(index.intersect(right, replacement)["common_rows"])
        index.sync([])
        self.assertEqual(index._messages, {})
        self.assertEqual(index.cache_stats["rows"], 0)

    def test_random_shrinks_and_small_capacities_match_full_semijoin(self):
        rng = random.Random(20261028)
        for cap in (0, 1, 4, 10, 1000):
            for _ in range(15):
                index, left, right = self.setup_pair(cap)
                for step in range(8):
                    for factor in (left, right):
                        if rng.random() < .7:
                            shrink(factor, (r for r in sorted(factor.rows) if rng.random() < .85))
                    index.sync([left, right] if step % 2 else [right, left])
                    answer = index.intersect(left, right)
                    self.assertEqual(answer, self.oracle(left, right))
                    commit(index, left, right, answer)
                    self.assert_capacity(index, cap)

    def test_every_loss_query_interruption_is_atomic_and_retryable(self):
        class Interrupted(Exception):
            pass
        def setup():
            index, left, right = self.setup_pair()
            shrink(left, (r for r in left.rows if r[0] == r[1]))
            shrink(right, (r for r in right.rows if r[:2] != (1, 1)))
            index.sync([left, right])
            return index, left, right
        index, left, right = setup()
        charges = []
        expected = index.intersect(left, right, charge=lambda: charges.append(1))
        for stop in range(len(charges)):
            index, left, right = setup()
            original = left.rows, left.revision, right.rows, right.revision
            count = 0
            def charge():
                nonlocal count
                if count == stop:
                    raise Interrupted
                count += 1
            with self.assertRaises(Interrupted):
                index.intersect(left, right, charge=charge)
            self.assertEqual(original, (left.rows, left.revision, right.rows, right.revision))
            self.assertEqual(list(index.pending_pairs()), [(left, right)])
            self.assertEqual(index.intersect(left, right), expected)
            self.assert_capacity(index, 1000)


class SupportLossSolverTests(bucket_tests.BucketFlowTests):
    def solve(self, graph, **options):
        if options.get("use_intersections", True):
            options.update(propagation_method="support", use_interface_cache=True)
        return super().solve(graph, **options)

    def test_complete_records_match_delta_with_cache_and_partition_variants(self):
        rng = random.Random(1027)
        for _ in range(12):
            graph = dict(vertices=list(range(6)), edges=[list(e) for e in combinations(range(6), 2)
                         if rng.random() < .5], fixed=[[0, rng.randrange(4)]])
            for partition in ("none", "information"):
                for cap in (0, 10, 10000):
                    options = dict(use_intersections=True, use_interface_cache=True,
                                   interface_cache_max_rows=cap, use_cycles=True, use_cycle_contexts=True,
                                   partition_strategy=partition, partition_block_size=2,
                                   bucket_method="prefix", max_checks=1_000_000)
                    old = solve_constraints(graph, propagation_method="delta", **options)
                    new = solve_constraints(graph, propagation_method="support", **options)
                    self.assertNotEqual(new["status"], "limit")
                    self.assertEqual(semantic_record(old), semantic_record(new))
                    self.assert_complete_join_fibres(new)

    def test_storage_limits_and_cli(self):
        graph = dict(vertices=list(range(5)), edges=[[i, (i+1) % 5] for i in range(5)])
        for method in ("anchor", "prefix"):
            complete = self.solve(graph, bucket_method=method)
            for cap in (0, 1, 12, 40, 100):
                result = self.solve(graph, bucket_method=method, max_table_rows=cap)
                records = result["elimination_records"]
                self.assertEqual(records, complete["elimination_records"][:len(records)])
                self.assert_complete_join_fibres(result)
                if result["status"] == "limit":
                    self.assertEqual(result["colors"], [-1] * 5)
        with TemporaryDirectory() as directory:
            source, output = Path(directory)/"g.json", Path(directory)/"r.json"
            source.write_text(json.dumps(graph))
            command = [sys.executable, str(ROOT/"scripts/four_color_lab.py"), "solve", str(source),
                       "--engine", "constraints", "--intersections", "--interface-cache",
                       "--propagation-method", "support", "--json", str(output)]
            run = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(output.read_text())["propagation_method"], "support")


if __name__ == "__main__":
    unittest.main()
