"""A known two-colourable grid completes with the revised default capacity."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from four_color_constraints import solve_constraints


def rectangular_grid(height=6, width=7):
    edges = []
    for row in range(height):
        for column in range(width):
            vertex = row * width + column
            if column + 1 < width:
                edges.append([vertex, vertex + 1])
            if row + 1 < height:
                edges.append([vertex, vertex + width])
    return dict(vertices=list(range(height * width)), edges=edges)


class DefaultCapacityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = rectangular_grid()
        cls.default = solve_constraints(cls.graph)

    def test_default_grid_completes_and_keeps_complete_certificates(self):
        result = self.default
        known = [(v // 7 + v % 7) % 2 for v in self.graph["vertices"]]
        self.assertTrue(all(known[u] != known[v] for u, v in self.graph["edges"]))
        self.assertEqual(result["status"], "colored")
        self.assertEqual(result["max_checks"], 1_000_000)
        self.assertEqual(result["max_table_rows"], 1_000_000)
        self.assertLessEqual(result["stats"]["checks"], result["max_checks"])
        self.assertGreater(result["stats"]["certificate_rows"], 100_000)
        self.assertTrue(all(type(c) is int and 0 <= c < 4 for c in result["colors"]))
        self.assertTrue(all(result["colors"][u] != result["colors"][v]
                            for u, v in self.graph["edges"]))
        self.assertEqual(len(result["elimination_records"]), len(self.graph["vertices"]))
        for record in result["elimination_records"]:
            self.assertTrue(record["complete"])
            self.assertEqual(len(record["rows"]), record["relation_rows"])
            self.assertIn("source_domains", record)
            self.assertIn("input_relations", record)
        explicit = solve_constraints(self.graph, max_table_rows=1_000_000)
        self.assertEqual(explicit, result)

    def test_explicit_old_capacity_still_limits_without_false_verdict_or_partial_record(self):
        limited = solve_constraints(self.graph, max_table_rows=100_000)
        self.assertEqual(limited["status"], "limit")
        self.assertEqual(limited["max_checks"], self.default["max_checks"])
        self.assertEqual(limited["max_table_rows"], 100_000)
        self.assertEqual(limited["colors"], [-1] * len(self.graph["vertices"]))
        self.assertEqual(limited["stats"]["writebacks"], 0)
        self.assertLessEqual(limited["stats"]["certificate_rows"], 100_000)
        records = limited["elimination_records"]
        self.assertEqual(records, self.default["elimination_records"][:len(records)])
        self.assertIn("記錄", limited["events"][-1]["detail"])

    def test_public_snapshot_rows_remain_independent_mutable_lists(self):
        records = deepcopy(self.default["elimination_records"])
        seen = {}
        for record in records:
            for relation in record["input_relations"]:
                for row in relation["rows"]:
                    self.assertIs(type(row), list)
                    key = tuple(row)
                    if key and key in seen:
                        other = seen[key]
                        self.assertIsNot(row, other)
                        previous = list(other)
                        row[0] = (row[0] + 1) % 4
                        self.assertEqual(other, previous)
                        return
                    seen[key] = row
        self.fail("grid fixture did not exercise duplicate literal input rows")


if __name__ == "__main__":
    unittest.main()
