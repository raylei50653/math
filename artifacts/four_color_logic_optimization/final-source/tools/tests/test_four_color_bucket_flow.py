"""Sparse bucket enumeration equals the full literal input-relation join."""

from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_conflict_priority import original_solutions, verify_preservation
from four_color_constraints import solve_constraints


class BucketFlowTests(unittest.TestCase):
    def solve(self, graph, **options):
        settings = dict(use_conflicts=False, use_substructures=False,
                        use_intersections=True, record_relations=True,
                        trace_limit=10000, max_checks=1_000_000)
        settings.update(options)
        return solve_constraints(graph, **settings)

    def assert_complete_join_fibres(self, result):
        """Use the Cartesian definition, independently of the chosen anchor."""
        for record in result["elimination_records"]:
            self.assertTrue(record["complete"])
            variables = [record["vertex"], *record["scope"]]
            domains = {item["vertex"]: item["colors"] for item in record["source_domains"]}
            self.assertEqual(set(domains), set(variables))
            inputs = [(relation["scope"], {tuple(row) for row in relation["rows"]})
                      for relation in record["input_relations"]]
            expected = {}
            for colors in product(*(domains[vertex] for vertex in variables)):
                assignment = dict(zip(variables, colors))
                if all(tuple(assignment[vertex] for vertex in columns) in rows
                       for columns, rows in inputs):
                    boundary = tuple(assignment[vertex] for vertex in record["scope"])
                    expected.setdefault(boundary, set()).add(assignment[record["vertex"]])
            actual = {tuple(row["boundary"]): set(row["colors"])
                      for row in record["rows"]}
            self.assertEqual(len(actual), len(record["rows"]))
            self.assertEqual(record["relation_rows"], len(actual))
            self.assertEqual(actual, expected)
            self.assertEqual([tuple(row["boundary"]) for row in record["rows"]], sorted(actual))
            for row in record["rows"]:
                self.assertEqual(row["colors"], sorted(set(row["colors"])))
            # Cover the ambient frontier as well as stored nonempty fibres.
            for boundary in product(*(domains[vertex] for vertex in record["scope"])):
                self.assertEqual(actual.get(boundary, set()), expected.get(boundary, set()))

    def assert_all_source_solutions_survive(self, result, solutions):
        positions = {vertex: offset for offset, vertex in enumerate(result["graph"]["vertices"])}
        for solution in solutions:
            assignment = {vertex: solution[offset] for vertex, offset in positions.items()}
            for event in result["events"]:
                if event["phase"] == "reduce":
                    self.assertTrue(all(color in domain
                                        for color, domain in zip(solution, event["domains"])))
            for record in result["elimination_records"]:
                saved = {tuple(row["boundary"]): row["colors"] for row in record["rows"]}
                boundary = tuple(assignment[vertex] for vertex in record["scope"])
                self.assertIn(assignment[record["vertex"]], saved[boundary])

    def test_empty_buckets_keep_all_free_and_fixed_colours(self):
        for graph in (dict(vertices=[], edges=[], fixed=[]),
                      dict(vertices=[42, -9, 100], edges=[], fixed=[[100, 2]])):
            with self.subTest(graph=graph):
                result = self.solve(graph)
                solutions = list(original_solutions(graph))
                self.assertEqual(result["status"], "colored")
                self.assertTrue(verify_preservation(result["graph"], solutions, result)["all_solutions_preserved"])
                self.assert_complete_join_fibres(result)
                fixed = dict(graph["fixed"])
                for record in result["elimination_records"]:
                    self.assertEqual(record["scope"], [])
                    self.assertEqual(record["input_relations"], [])
                    expected = [fixed[record["vertex"]]] if record["vertex"] in fixed else list(range(4))
                    self.assertEqual(record["rows"], [dict(boundary=[], colors=expected)])

    def test_sparse_fixed_and_reversed_literal_frames_match_full_join(self):
        graph = dict(vertices=[42, -3, 80, 5, 900, 17],
                     edges=[[42, -3], [-3, 80], [80, 5], [5, 900], [900, 42], [17, 42]],
                     fixed=[[17, 2]])
        reversed_graph = dict(vertices=list(reversed(graph["vertices"])),
                              edges=[[b, a] for a, b in reversed(graph["edges"])],
                              fixed=deepcopy(graph["fixed"]))
        for case in (graph, reversed_graph):
            solutions = list(original_solutions(case))
            self.assertGreater(len(solutions), 1)
            for templates in (False, True):
                with self.subTest(vertices=case["vertices"], templates=templates):
                    before = deepcopy(case)
                    result = self.solve(case, use_substructures=templates,
                                        use_cycles=True, use_cycle_contexts=True,
                                        cycle_context_search="partial")
                    self.assertEqual(result["status"], "colored")
                    self.assertTrue(verify_preservation(result["graph"], solutions, result)["all_solutions_preserved"])
                    self.assert_complete_join_fibres(result)
                    self.assertTrue(any(len(row["colors"]) > 1
                                        for record in result["elimination_records"]
                                        for row in record["rows"]))
                    self.assertEqual(case, before)

    def test_incompatible_full_bucket_fibres_are_not_accepted(self):
        graph = dict(vertices=list(range(5)),
                     edges=[list(pair) for pair in combinations(range(5), 2)], fixed=[])
        self.assertEqual(list(original_solutions(graph)), [])
        # Leave the contradiction to the exact bucket joins, rather than
        # allowing a redundant semijoin to discover it between eliminations.
        result = self.solve(graph, use_intersections=False)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assert_complete_join_fibres(result)
        self.assertTrue(result["elimination_records"])
        self.assertEqual(result["elimination_records"][-1]["rows"], [])
        self.assertEqual(result["stats"]["writebacks"], 0)

    def test_every_work_interruption_keeps_complete_record_prefix_and_unknown_colours(self):
        graph = dict(vertices=[9, -2, 40, 17],
                     edges=[[9, -2], [-2, 40], [40, 17], [17, 9]], fixed=[[9, 0]])
        before = deepcopy(graph)
        complete = self.solve(graph)
        self.assertEqual(complete["status"], "colored")
        solutions = list(original_solutions(graph))
        expected_colours = [dict(graph["fixed"]).get(vertex, -1) for vertex in graph["vertices"]]
        for budget in range(complete["stats"]["checks"]):
            with self.subTest(budget=budget):
                result = self.solve(graph, max_checks=budget)
                self.assertEqual(result["status"], "limit")
                self.assertEqual(result["colors"], expected_colours)
                self.assertEqual(result["stats"]["writebacks"], 0)
                self.assertFalse(any(event["phase"] == "writeback" for event in result["events"]))
                for event in result["events"]:
                    self.assertEqual(event["colors"], expected_colours)
                records = result["elimination_records"]
                self.assertEqual(records, complete["elimination_records"][:len(records)])
                self.assertEqual(len(records), result["stats"]["eliminations"])
                self.assert_complete_join_fibres(result)
                self.assert_all_source_solutions_survive(result, solutions)
                self.assertEqual(graph, before)
        at_full_budget = self.solve(graph, max_checks=complete["stats"]["checks"])
        self.assertEqual(at_full_budget["status"], "colored")
        self.assertEqual(at_full_budget["elimination_records"], complete["elimination_records"])


if __name__ == "__main__":
    unittest.main()
