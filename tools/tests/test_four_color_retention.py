"""Boundary support and internal witness retention have different contracts."""

from copy import deepcopy
from itertools import combinations
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from four_color_constraints import solve_constraints
from four_color_retention_audit import (
    KINDS, audit_result, decode, encode_records, negative_controls,
    original_solutions, reconstruct, valid_coloring,
)


class RetentionTests(unittest.TestCase):
    def solve(self, graph, **options):
        return solve_constraints(graph, use_substructures=False, use_conflicts=False, **options)

    def test_nonempty_masks_preserve_every_subset_of_the_four_literal_colors(self):
        for size in range(1, 5):
            for choices in combinations(range(4), size):
                result = dict(status="colored", record_relations=True, elimination_records=[dict(
                    vertex=40, scope=[], complete=True, relation_rows=1,
                    rows=[dict(boundary=[], colors=list(choices))])])
                encoded = encode_records(result, "mask")
                mask = encoded[0][2][()]
                self.assertEqual(decode(mask, "mask"), choices)
                self.assertGreater(mask, 0)
                self.assertLess(mask, 16)

    def test_all_retention_modes_reconstruct_literal_fixed_and_disconnected_graphs(self):
        for graph in (dict(vertices=[], edges=[], fixed=[]),
                      dict(vertices=[40, -3, 900, 17, 0],
                           edges=[[40, -3], [-3, 900], [900, 40]], fixed=[[900, 3]])):
            result = self.solve(graph)
            before = deepcopy(result)
            metrics = audit_result(result, solutions=list(original_solutions(graph)))
            self.assertEqual(metrics["writebacks_checked"], 7)
            self.assertEqual(result, before)

    def test_one_witness_intentionally_loses_solutions_while_masks_keep_them(self):
        graph = dict(vertices=[17], edges=[], fixed=[])
        result = self.solve(graph)
        full = encode_records(result, "full")[0][2][()]
        mask = encode_records(result, "mask")[0][2][()]
        one = encode_records(result, "one_min")[0][2][()]
        self.assertEqual(full, (0, 1, 2, 3))
        self.assertEqual(decode(mask, "mask"), full)
        self.assertEqual(decode(one, "one_min"), (0,))
        self.assertEqual(len(list(original_solutions(graph))), 4)

    def test_unsat_and_limits_cannot_be_written_back(self):
        graph = dict(vertices=list(range(5)), edges=list(map(list, combinations(range(5), 2))))
        result = self.solve(graph)
        self.assertEqual(result["status"], "unsatisfiable")
        audit_result(result, solutions=[])
        for kind in KINDS:
            with self.assertRaises(ValueError):
                reconstruct(result, encode_records(result, kind), kind)
            with self.assertRaises(ValueError):
                encode_records(self.solve(graph, max_checks=0), kind)
            with self.assertRaises(ValueError):
                encode_records(self.solve(graph, record_relations=False), kind)

    def test_missing_boundary_or_elimination_cannot_be_silently_accepted(self):
        result = self.solve(dict(vertices=[42, -9], edges=[[42, -9]], fixed=[]))
        encoded = encode_records(result, "one_min")
        with self.assertRaises(ValueError):
            reconstruct(result, encoded[:-1], "one_min")
        encoded[-1][2].clear()
        with self.assertRaises(KeyError):
            reconstruct(result, encoded, "one_min")

    def test_even_one_deleted_star_boundary_has_a_valid_rejected_context(self):
        controls = negative_controls()
        self.assertEqual(len(controls), 8)
        self.assertEqual(controls[-1]["kept_boundary_rows"], 231)
        self.assertEqual(controls[-1]["full_boundary_rows"], 232)
        for control in controls:
            self.assertTrue(valid_coloring(control["graph"], control["original_witness"]))
            self.assertEqual(self.solve(control["graph"])["status"], "colored")
            self.assertEqual(control["truncated_interface_status"], "empty")


if __name__ == "__main__":
    unittest.main()
