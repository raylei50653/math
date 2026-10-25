"""Incremental interfaces preserve literal relations and complete fibres."""

from copy import deepcopy
from dataclasses import dataclass, field
import gc
from itertools import combinations, product
from pathlib import Path
import sys
import unittest
import weakref


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_conflict_priority import original_solutions, verify_preservation
from four_color_constraints import solve_constraints
from four_color_intersections import SharedInterfaceIndex, intersect_on_shared


@dataclass(eq=False)
class Factor:
    scope: tuple
    rows: frozenset = field(default_factory=frozenset)
    revision: int = 0


class SharedInterfaceIndexTests(unittest.TestCase):
    def test_new_same_revision_factors_do_not_inherit_shifted_list_stamps(self):
        first, middle, last = Factor((0, 1)), Factor((0, 1, 2)), Factor((1, 2))
        index = SharedInterfaceIndex()
        charges = []
        index.sync([first, middle, last], charge=lambda: charges.append(None))
        initial_pairs = list(index.pairs())
        self.assertEqual(initial_pairs, [(first, middle), (middle, last)])
        self.assertEqual(len(charges), len(initial_pairs))
        for pair in initial_pairs:
            index.mark_seen(*pair)
        index.sync([first, middle, last], charge=lambda: self.fail("unchanged pair rediscovered"))

        replacement = Factor(first.scope)
        index.sync([middle, last, replacement])
        self.assertEqual(list(index.pairs()), [(middle, last), (middle, replacement)])
        self.assertTrue(index.seen(middle, last))
        self.assertFalse(index.seen(middle, replacement))
        self.assertFalse(index.seen(first, middle))
        index.mark_seen(middle, replacement)
        index.sync([replacement, last, middle])
        self.assertEqual(list(index.pairs()), [(replacement, middle), (last, middle)])
        self.assertTrue(index.seen(replacement, middle))
        self.assertTrue(index.seen(last, middle))

    def test_retired_factors_and_their_cached_references_are_released(self):
        first, second = Factor((0, 1)), Factor((0, 1, 2))
        reference = weakref.ref(first)
        index = SharedInterfaceIndex()
        index.sync([first, second])
        index.mark_seen(first, second)
        index.sync([second])
        del first
        gc.collect()
        self.assertIsNone(reference())
        replacement = Factor((0, 1))
        index.sync([second, replacement])
        self.assertFalse(index.seen(second, replacement))

    def test_later_pair_pruning_reawakens_an_earlier_pair(self):
        first = Factor((0, 1), frozenset({(0, 0), (1, 1)}))
        middle = Factor((0, 1, 2), frozenset({(0, 0, 0), (1, 1, 1)}))
        last = Factor((1, 2), frozenset({(1, 1)}))
        index = SharedInterfaceIndex()
        index.sync([first, middle, last])

        def query(left, right):
            answer = intersect_on_shared(left.scope, left.rows, right.scope, right.rows)
            for factor, key in ((left, "left_rows"), (right, "right_rows")):
                if answer[key] != factor.rows:
                    factor.rows = answer[key]
                    factor.revision += 1
            index.mark_seen(left, right)

        query(first, middle)
        self.assertTrue(index.seen(first, middle))
        query(middle, last)
        self.assertFalse(index.seen(first, middle))
        self.assertTrue(index.seen(middle, last))
        query(first, middle)
        self.assertEqual(first.rows, frozenset({(1, 1)}))
        self.assertTrue(index.seen(first, middle))
        self.assertTrue(index.seen(middle, last))

    def test_single_shared_variable_is_excluded_and_triple_is_kept_whole(self):
        even = frozenset((*row, 0) for row in product(range(2), repeat=3)
                         if sum(row) % 2 == 0)
        odd_reversed = frozenset((row[2], row[1], row[0], 1)
                                 for row in product(range(2), repeat=3)
                                 if sum(row) % 2 == 1)
        left, right = Factor((0, 1, 2, 3), even), Factor((2, 1, 0, 4), odd_reversed)
        single = Factor((0, 5))
        index, charges = SharedInterfaceIndex(), []
        index.sync([left, single, right], charge=lambda: charges.append(None))
        self.assertEqual(list(index.pairs()), [(left, right)])
        self.assertEqual(len(charges), len(list(index.pairs())))
        result = intersect_on_shared(left.scope, left.rows, right.scope, right.rows)
        self.assertEqual(result["scope"], (0, 1, 2))
        self.assertFalse(result["common_rows"])
        self.assertFalse(result["left_rows"])
        self.assertFalse(result["right_rows"])

    def test_interrupted_discovery_keeps_old_index_and_resumes_without_false_hits(self):
        first, middle = Factor((0, 1)), Factor((0, 1, 2))
        later, final = Factor((1, 2, 3)), Factor((1, 2))
        replacement = [middle, later, final]
        reference, charges = SharedInterfaceIndex(), []
        reference.sync([first, middle])
        reference.sync(replacement, charge=lambda: charges.append(None))

        class Interrupted(Exception):
            pass

        for stop_at in range(len(charges)):
            index = SharedInterfaceIndex()
            index.sync([first, middle])
            index.mark_seen(first, middle)
            visited = 0

            def charge():
                nonlocal visited
                if visited == stop_at:
                    raise Interrupted
                visited += 1

            with self.subTest(stop_at=stop_at):
                with self.assertRaises(Interrupted):
                    index.sync(replacement, charge=charge)
                self.assertEqual(list(index.pairs()), [(first, middle)])
                self.assertTrue(index.seen(first, middle))
                index.sync(replacement)
                self.assertEqual(list(index.pairs()), list(reference.pairs()))
                self.assertTrue(all(not index.seen(*pair) for pair in index.pairs()))

    def test_unpruned_semijoin_reuses_immutable_complete_relations(self):
        left = frozenset({(0, 1, 2), (1, 0, 2)})
        right = frozenset({(1, 3, 0), (0, 3, 1)})
        answer = intersect_on_shared((10, 20, 30), left, (20, 40, 10), right)
        self.assertIs(answer["left_rows"], left)
        self.assertIs(answer["right_rows"], right)
        self.assertEqual(answer["common_rows"], frozenset({(0, 1), (1, 0)}))


class FlowSolutionPreservationTests(unittest.TestCase):
    def assert_complete_fibres(self, result):
        """Enumerate each recorded bucket directly, including absent fibres."""
        for record in result["elimination_records"]:
            scope = [record["vertex"], *record["scope"]]
            domains = {item["vertex"]: item["colors"] for item in record["source_domains"]}
            inputs = [(item["scope"], {tuple(row) for row in item["rows"]})
                      for item in record["input_relations"]]
            expected = {}
            for colors in product(*(domains[vertex] for vertex in scope)):
                assignment = dict(zip(scope, colors))
                if all(tuple(assignment[vertex] for vertex in columns) in rows
                       for columns, rows in inputs):
                    boundary = tuple(assignment[vertex] for vertex in record["scope"])
                    expected.setdefault(boundary, set()).add(assignment[record["vertex"]])
            actual = {tuple(row["boundary"]): set(row["colors"]) for row in record["rows"]}
            self.assertEqual(len(actual), len(record["rows"]))
            self.assertEqual(actual, expected)

    def test_partial_context_flow_preserves_every_original_solution_and_bucket_fibre(self):
        # The two hubs share an original triangle.  Their differently restricted
        # domains become equal through full-interface feedback, then narrow the
        # triangle and free leaf.  Source-only enumeration knows none of this.
        edges = [list(pair) for pair in combinations(range(3), 2)]
        edges += [[vertex, hub] for vertex in range(3) for hub in (3, 4)]
        edges += [[3, 5], [3, 6], [4, 7], [4, 8]]
        graph = dict(vertices=list(range(9)), edges=edges,
                     fixed=[[5, 2], [6, 3], [7, 0]])
        labels = dict(zip(graph["vertices"], [101, -4, 23, 800, -9, 54, 2, 70, -300]))
        renamed = dict(vertices=[labels[vertex] for vertex in reversed(graph["vertices"])],
                       edges=[[labels[a], labels[b]] for a, b in reversed(edges)],
                       fixed=[[labels[vertex], color] for vertex, color in graph["fixed"]])
        for case in (graph, renamed):
            before = deepcopy(case)
            solutions = list(original_solutions(case))
            self.assertGreater(len(solutions), 1)
            with self.subTest(vertices=case["vertices"]):
                result = solve_constraints(
                    case, use_conflicts=False, use_intersections=True,
                    use_cycles=True, use_cycle_contexts=True,
                    cycle_context_search="partial", max_checks=1_000_000,
                    trace_limit=10000, record_relations=True)
                self.assertEqual(result["status"], "colored")
                self.assertFalse(result["trace_truncated"])
                self.assertTrue(verify_preservation(case, solutions, result)["all_solutions_preserved"])
                self.assertGreater(result["stats"]["intersection_prunes"], 0)
                self.assert_complete_fibres(result)
                self.assertEqual(case, before)


if __name__ == "__main__":
    unittest.main()
