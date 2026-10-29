"""Partition schedules preserve full literal fibres and original solutions."""

from copy import deepcopy
from itertools import combinations, product
import json
from pathlib import Path
import random
import subprocess
import sys
from types import SimpleNamespace
from tempfile import TemporaryDirectory
import unittest

import test_four_color_bucket_flow as bucket_tests

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_constraints import solve_constraints
from four_color_lab import normalize_graph, verify_coloring
from four_color_partition import partition_plan, STRATEGIES, STATIC_STRATEGIES, InformationScheduler


class PartitionTests(bucket_tests.BucketFlowTests):
    def solve(self, graph, **options):
        options.setdefault("partition_strategy", "bfs")
        options.setdefault("partition_block_size", 2)
        return super().solve(graph, **options)

    def test_split_contract_and_determinism(self):
        graphs = [dict(vertices=list(range(50)), edges=[[i, i + 1] for i in range(49)]),
                  dict(vertices=list(range(36)), edges=[[6*r+c, 6*s+d]
                       for r in range(6) for c in range(6)
                       for s, d in ((r+1, c), (r, c+1)) if s < 6 and d < 6])]
        for graph in graphs:
            for strategy in STATIC_STRATEGIES:
                plan = partition_plan(graph, strategy, 4)
                self.assertEqual(plan, partition_plan(graph, strategy, 4))
                flat = sum(plan["groups"], [])
                self.assertEqual(sorted(flat), graph["vertices"])
                rank = {v: i for i, group in enumerate(plan["groups"]) for v in group}
                for split in plan["splits"]:
                    cut = set(split["separator"])
                    interiors = list(map(set, split["interiors"]))
                    self.assertEqual(set(split["region"]), cut.union(*interiors))
                    self.assertEqual(sum(map(len, interiors)) + len(cut), len(split["region"]))
                    for i, inside in enumerate(interiors):
                        self.assertLess(max(rank[v] for v in inside), min(rank[v] for v in cut))
                        outside = set().union(*(interiors[:i] + interiors[i+1:]))
                        self.assertFalse(any(a in inside and b in outside or b in inside and a in outside
                                             for a, b in graph["edges"]))
                if strategy == "bfs" or strategy == "articulation" and len(flat) == 50:
                    self.assertTrue(plan["splits"])

    def test_exhaustive_small_graph_solution_sets_and_fibres(self):
        pairs = list(combinations(range(4), 2))
        graphs = [dict(vertices=list(range(4)), edges=[list(e) for i, e in enumerate(pairs)
                       if mask & (1 << i)], fixed=fixed)
                  for mask in range(64) for fixed in ([], [[0, 0], [3, 1]])]
        rng = random.Random(20261027)
        graphs += [dict(vertices=[-3, 90, 2, 71, 8, 4], edges=[list(e)
                    for e in combinations([-3, 90, 2, 71, 8, 4], 2) if rng.random() < .5],
                    fixed=[[-3, 2]]) for _ in range(10)]
        for graph in graphs:
            graph = normalize_graph(graph)
            before = deepcopy(graph)
            assignments = list(product(range(4), repeat=len(graph["vertices"])))
            expected = {row for row in assignments if verify_coloring(graph, list(row))}
            for strategy in STRATEGIES:
                result = self.solve(graph, partition_strategy=strategy)
                self.assertEqual(result["status"], "colored" if expected else "unsatisfiable")
                self.assert_complete_join_fibres(result)
                self.assert_all_source_solutions_survive(result, expected)
                if expected:
                    tables = [(r["vertex"], r["scope"],
                               {tuple(row["boundary"]): row["colors"] for row in r["rows"]})
                              for r in result["elimination_records"]]
                    represented = set()
                    for row in assignments:
                        a = dict(zip(graph["vertices"], row))
                        if all(a[v] in table.get(tuple(a[w] for w in scope), [])
                               for v, scope, table in tables):
                            represented.add(row)
                    self.assertEqual(expected, represented)
                    self.assertTrue(verify_coloring(graph, result["colors"]))
                self.assertEqual(before, graph)

    def test_shared_separator_cannot_splice_incompatible_witnesses(self):
        # Each side alone extends; the common articulation would need both
        # colour 3 and colour 0 in the same literal frame.
        graph = dict(vertices=list(range(7)), edges=[[0, v] for v in range(1, 7)],
                     fixed=[[1, 0], [2, 1], [3, 2], [4, 1], [5, 2], [6, 3]])
        for strategy in STRATEGIES:
            result = self.solve(graph, partition_strategy=strategy)
            self.assertEqual(result["status"], "unsatisfiable")
            self.assertEqual(result["stats"]["writebacks"], 0)

    def test_storage_limits_and_both_bucket_methods(self):
        graph = dict(vertices=list(range(6)), edges=[[i, (i+1) % 6] for i in range(6)])
        for strategy in STRATEGIES:
            for method in ("anchor", "prefix"):
                complete = self.solve(graph, partition_strategy=strategy, bucket_method=method)
                for cap in (0, 1, 12, 40, 100):
                    result = self.solve(graph, partition_strategy=strategy, bucket_method=method,
                                        max_table_rows=cap)
                    self.assert_complete_join_fibres(result)
                    records = result["elimination_records"]
                    self.assertEqual(records, complete["elimination_records"][:len(records)])
                    if result["status"] == "limit":
                        self.assertEqual(result["colors"], [-1] * 6)
                        self.assertEqual(result["stats"]["writebacks"], 0)

    def test_api_cli_and_validation(self):
        graph = dict(vertices=list(range(5)), edges=[[i, i+1] for i in range(4)])
        for value in (None, True, [], "BFS"):
            with self.assertRaises(ValueError):
                solve_constraints(graph, partition_strategy=value)
        for value in (None, True, 0, -1, 1.2):
            with self.assertRaises(ValueError):
                solve_constraints(graph, partition_block_size=value)
        with TemporaryDirectory() as directory:
            source, output = Path(directory)/"graph.json", Path(directory)/"result.json"
            source.write_text(json.dumps(graph))
            command = [sys.executable, str(ROOT/"scripts/four_color_lab.py"), "solve", str(source),
                       "--partition", "bfs", "--partition-block-size", "2", "--json", str(output)]
            run = subprocess.run(command + ["--engine", "constraints"], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            result = json.loads(output.read_text())
            self.assertEqual(result["partition_plan"]["strategy"], "bfs")
            self.assertTrue(result["partition_plan"]["splits"])
            run = subprocess.run(command + ["--engine", "search"], capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn("require --engine constraints", run.stderr)


class AdaptiveFibreTests(bucket_tests.BucketFlowTests):
    def solve(self, graph, **options):
        return super().solve(graph, partition_strategy="adaptive", partition_block_size=2, **options)


class InformationFibreTests(bucket_tests.BucketFlowTests):
    def solve(self, graph, **options):
        return super().solve(graph, partition_strategy="information", partition_block_size=2, **options)


class MessageFibreTests(bucket_tests.BucketFlowTests):
    def solve(self, graph, **options):
        return super().solve(graph, partition_strategy="message", partition_block_size=2, **options)


class InformationPolicyTests(unittest.TestCase):
    @staticmethod
    def state(nodes, edges, row_counts=None):
        primal = {v: set() for v in nodes}
        factors = []
        for i, (a, b) in enumerate(edges):
            primal[a].add(b)
            primal[b].add(a)
            factors.append(SimpleNamespace(scope=(a, b), rows=range(row_counts[i] if row_counts else 12)))
        priorities = {v: (sum(b not in primal[a] for a, b in combinations(sorted(neighbors), 2)),
                          len(neighbors), v) for v, neighbors in primal.items()}
        return primal, priorities, factors, [set(range(4)) for _ in range(max(nodes) + 1)]

    def test_new_cross_region_information_abandons_old_region(self):
        graph = dict(vertices=list(range(6)), edges=[[i, i+1] for i in range(5)])
        for mode in ("adaptive", "information"):
            plan = partition_plan(graph, mode, 2)
            scheduler = InformationScheduler(plan, graph["vertices"])
            self.assertEqual(scheduler.select(*self.state(range(6), graph["edges"])), 0)
            self.assertEqual(scheduler.region, {0, 1})
            # New joint messages couple the previous preferred vertex to a
            # wider interface. The remaining leaf is outside the old region.
            edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 3), (1, 4)]
            self.assertEqual(scheduler.select(*self.state(range(1, 6), edges)), 5)
            self.assertTrue(plan["decisions"][-1]["replanned"])
            self.assertEqual(plan["groups"], [[0], [5]])

    def test_actual_message_size_changes_choice_and_is_refreshed(self):
        graph = dict(vertices=list(range(4)), edges=[[0, 1], [2, 3]])
        plan = partition_plan(graph, "information", 2)
        scheduler = InformationScheduler(plan, graph["vertices"])
        state = self.state(range(4), graph["edges"], [12, 2])
        self.assertEqual(scheduler.select(*state), 2)
        self.assertEqual(plan["decisions"][-1]["anchor_bound"], 2)
        # Domain/row updates from propagation must override old block affinity.
        state[2][0].rows = range(1)
        self.assertEqual(scheduler.select(*state), 0)
        self.assertEqual(plan["decisions"][-1]["anchor_bound"], 1)
        self.assertTrue(plan["decisions"][-1]["replanned"])

    def test_dynamic_cli_trace_records_actual_selected_groups(self):
        graph = dict(vertices=list(range(6)), edges=[[i, (i+1) % 6] for i in range(6)])
        result = solve_constraints(graph, partition_strategy="information", partition_block_size=2)
        plan = result["partition_plan"]
        self.assertEqual(sum(plan["groups"], []), [r["vertex"] for r in result["elimination_records"]])
        self.assertTrue(plan["regions"])
        self.assertEqual(result["status"], "colored")
        with TemporaryDirectory() as directory:
            source, output = Path(directory)/"graph.json", Path(directory)/"result.json"
            source.write_text(json.dumps(graph))
            run = subprocess.run([sys.executable, str(ROOT/"scripts/four_color_lab.py"), "solve",
                                  str(source), "--engine", "constraints", "--partition", "information",
                                  "--partition-block-size", "2", "--json", str(output)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(output.read_text())["partition_plan"], plan)


if __name__ == "__main__":
    unittest.main()
