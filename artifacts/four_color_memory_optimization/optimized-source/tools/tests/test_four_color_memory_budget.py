"""Explicit storage budgets preserve complete literal-colour certificates."""

from copy import deepcopy
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import four_color_constraints as constraints
from four_color_conflict_priority import original_solutions, verify_preservation


class MemoryBudgetTests(unittest.TestCase):
    def setUp(self):
        self.graph = dict(vertices=[30, -4, 8],
                          edges=[list(pair) for pair in combinations([30, -4, 8], 2)],
                          fixed=[])

    def solve(self, **options):
        settings = dict(use_conflicts=False, record_relations=True,
                        trace_limit=10000, max_checks=1_000_000)
        settings.update(options)
        return constraints.solve_constraints(self.graph, **settings)

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
            for row in record["rows"]:
                self.assertEqual(row["colors"], sorted(set(row["colors"])))

    def assert_limited_without_early_colours(self, result):
        self.assertEqual(result["status"], "limit")
        self.assertEqual(result["colors"], [-1] * len(self.graph["vertices"]))
        self.assertEqual(result["stats"]["writebacks"], 0)
        self.assertFalse(any(event["phase"] == "writeback" for event in result["events"]))
        self.assertTrue(all(event["colors"] == result["colors"] for event in result["events"]))
        self.assert_complete_fibres(result)

    def test_explicit_budget_requires_exact_nonnegative_integer(self):
        for value in (True, False, -1, 1.0, 1.5, "100", [], {}):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "max_table_rows"):
                    self.solve(max_table_rows=value)

    def test_omitted_and_none_preserve_dynamic_historical_default(self):
        implicit = self.solve()
        explicit_none = self.solve(max_table_rows=None)
        self.assertEqual(implicit, explicit_none)
        self.assertEqual(implicit["max_table_rows"],
                         min(implicit["max_checks"], constraints.TABLE_ROW_CEILING))
        for checks in (0, 1, 12):
            with self.subTest(max_checks=checks):
                result = self.solve(max_checks=checks)
                self.assertEqual(result["max_table_rows"], min(checks, constraints.TABLE_ROW_CEILING))
        with patch.object(constraints, "TABLE_ROW_CEILING", 0):
            implicit = self.solve()
            explicit_none = self.solve(max_table_rows=None)
        self.assertEqual(implicit, explicit_none)
        self.assertEqual(implicit["max_table_rows"], 0)
        self.assert_limited_without_early_colours(implicit)
        self.assertEqual(implicit["elimination_records"], [])

    def test_explicit_capacity_exceeds_patched_default_without_changing_work_or_fibres(self):
        before = deepcopy(self.graph)
        baseline = self.solve()
        rows_needed = max(baseline["stats"]["table_rows"],
                          baseline["stats"]["certificate_rows"])
        with patch.object(constraints, "TABLE_ROW_CEILING", 0):
            implicit = self.solve()
            expanded = self.solve(max_table_rows=rows_needed)
        self.assert_limited_without_early_colours(implicit)
        self.assertEqual(expanded["status"], "colored")
        self.assertEqual(expanded["max_checks"], baseline["max_checks"])
        self.assertEqual(expanded["max_table_rows"], rows_needed)
        self.assertEqual(expanded["stats"], baseline["stats"])
        self.assertEqual(expanded["elimination_records"], baseline["elimination_records"])
        solutions = list(original_solutions(self.graph))
        self.assertGreater(len(solutions), 1)
        self.assertTrue(verify_preservation(self.graph, solutions, expanded)["all_solutions_preserved"])
        self.assert_complete_fibres(expanded)
        self.assertEqual(self.graph, before)

    def test_generated_row_budget_has_zero_and_exact_boundaries(self):
        complete = self.solve(record_relations=False)
        generated = (complete["stats"]["table_rows"]
                     + complete["stats"]["cycle_context_rows"]
                     + complete["stats"]["joint_rows"])
        self.assertGreater(generated, 0)
        exact = self.solve(record_relations=False, max_table_rows=generated)
        self.assertEqual(exact["status"], "colored")
        self.assertEqual(exact["stats"]["table_rows"], generated)
        self.assertEqual(exact["stats"]["certificate_rows"], 0)
        self.assertEqual(exact["stats"]["checks"], complete["stats"]["checks"])
        for cap in (0, generated - 1):
            with self.subTest(max_table_rows=cap):
                limited = self.solve(record_relations=False, max_table_rows=cap)
                self.assertEqual(limited["status"], "limit")
                self.assertLessEqual(limited["stats"]["table_rows"], cap)
                self.assertEqual(limited["stats"]["certificate_rows"], 0)
                self.assertEqual(limited["colors"], [-1] * len(self.graph["vertices"]))
                self.assertEqual(limited["stats"]["writebacks"], 0)

    def test_complete_certificate_budget_is_independent_and_never_truncates_a_record(self):
        complete = self.solve()
        generated = complete["stats"]["table_rows"]
        certificate = complete["stats"]["certificate_rows"]
        self.assertGreater(certificate, generated)
        exact = self.solve(max_table_rows=certificate)
        self.assertEqual(exact["status"], "colored")
        self.assertEqual(exact["stats"]["certificate_rows"], certificate)
        self.assertEqual(exact["elimination_records"], complete["elimination_records"])
        self.assert_complete_fibres(exact)
        for cap in (0, generated, certificate - 1):
            with self.subTest(max_table_rows=cap):
                limited = self.solve(max_table_rows=cap)
                self.assert_limited_without_early_colours(limited)
                self.assertLessEqual(limited["stats"]["table_rows"], cap)
                self.assertLessEqual(limited["stats"]["certificate_rows"], cap)
                records = limited["elimination_records"]
                self.assertEqual(records, complete["elimination_records"][:len(records)])
                if cap:
                    self.assertIn("記錄", limited["events"][-1]["detail"])
        compact = self.solve(record_relations=False, max_table_rows=generated)
        self.assertEqual(compact["status"], "colored")

    def test_large_explicit_capacity_does_not_increase_main_work_budget(self):
        cap = 1_000_000
        for checks in (0, 1):
            with self.subTest(max_checks=checks):
                result = self.solve(max_checks=checks, max_table_rows=cap)
                self.assert_limited_without_early_colours(result)
                self.assertEqual(result["max_checks"], checks)
                self.assertEqual(result["max_table_rows"], cap)
                self.assertLessEqual(result["stats"]["checks"], checks)
                self.assertIn("檢查", result["events"][-1]["detail"])

    def test_cli_forwards_explicit_budget_and_rejects_search_or_invalid_values(self):
        certificate = self.solve()["stats"]["certificate_rows"]
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "graph.json", Path(directory) / "result.json"
            source.write_text(json.dumps(self.graph))
            prefix = [sys.executable, str(ROOT / "scripts/four_color_lab.py"), "solve", str(source)]
            for cap, expected in ((0, "limit"), (certificate, "colored")):
                with self.subTest(cap=cap):
                    completed = subprocess.run(
                        [*prefix, "--engine", "constraints", "--no-conflicts",
                         "--max-table-rows", str(cap), "--json", str(output)],
                        capture_output=True, text=True, timeout=30)
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    result = json.loads(output.read_text())
                    self.assertEqual(result["status"], expected)
                    self.assertEqual(result["max_table_rows"], cap)
                    self.assert_complete_fibres(result)
            for arguments in (("--engine", "search", "--max-table-rows", "100"),
                              ("--engine", "constraints", "--max-table-rows", "-1")):
                with self.subTest(arguments=arguments):
                    rejected = subprocess.run([*prefix, *arguments],
                                              capture_output=True, text=True, timeout=30)
                    self.assertNotEqual(rejected.returncode, 0)
                    self.assertTrue(rejected.stderr)


if __name__ == "__main__":
    unittest.main()
