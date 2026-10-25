"""Conflict-priority controls preserve full solutions and delayed writeback."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from four_color_conflict_priority import experiment, pre_elimination_metrics


class ConflictPriorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = experiment()
        cls.controls = {control["name"]: control for control in cls.report["controls"]}

    def test_seven_contexts_match_original_edge_enumeration(self):
        self.assertEqual(self.report["control_count"], 7)
        for control in self.controls.values():
            expected = "colored" if control["solution_count"] else "unsatisfiable"
            self.assertEqual(len(control["original_solutions"]), control["solution_count"])
            for mode, row in control["results"].items():
                with self.subTest(control=control["name"], mode=mode):
                    self.assertEqual(row["status"], expected)
                    self.assertTrue(row["all_solutions_preserved"])
                    self.assertTrue(row["no_early_writeback_verified"])
                    self.assertFalse(row["recorded_result"]["trace_truncated"])
                    self.assertEqual(row["recorded_result"]["stats"]["decisions"], 0)
                    self.assertEqual(row["recorded_result"]["stats"]["backtracks"], 0)
                    self.assertEqual(row["checks"]["original_solutions"], control["solution_count"])
                    if control["solution_count"]:
                        self.assertTrue(row["witness_verified"])
                        self.assertGreater(row["checks"]["source_domain_memberships"], 0)
                        self.assertGreater(row["checks"]["input_relation_memberships"], 0)
                        self.assertGreater(row["checks"]["saved_choice_memberships"], 0)

    def test_overlap_forces_singleton_before_elimination_with_six_solutions(self):
        control = self.controls["bipyramid_overlapping_hub_domains"]
        self.assertEqual(control["solution_count"], 6)
        rows = control["results"]
        base = rows["base"]["metrics"]
        strengthened = rows["intersections"]["metrics"]
        domains = lambda metrics: {entry["vertex"]: entry["colors"] for entry in
                                  metrics["domain_candidates_before_first_elimination"]}
        self.assertEqual(domains(base)[3], [0, 1])
        self.assertEqual(domains(base)[4], [1, 2])
        self.assertEqual(domains(strengthened)[3], [1])
        self.assertEqual(domains(strengthened)[4], [1])
        self.assertEqual(strengthened["intersection_row_prunes_before_first_elimination"], 12)
        first = next(event for event in rows["intersections"]["recorded_result"]["events"]
                     if event["kind"] == "eliminate")
        self.assertEqual(first["colors"][:5], [-1] * 5)

    def test_identical_domains_preserve_twelve_solutions_without_extra_pruning(self):
        control = self.controls["bipyramid_identical_hub_domains"]
        self.assertEqual(control["solution_count"], 12)
        base = control["results"]["base"]["metrics"]
        strengthened = control["results"]["intersections"]["metrics"]
        self.assertEqual(strengthened["intersection_row_prunes_before_first_elimination"], 0)
        self.assertEqual(base["domain_candidates_before_first_elimination"],
                         strengthened["domain_candidates_before_first_elimination"])

    def test_odd_bipyramid_requires_full_elimination_in_both_modes(self):
        control = self.controls["odd_bipyramid_distinct_fixed_hubs"]
        self.assertEqual(control["solution_count"], 0)
        for row in control["results"].values():
            self.assertEqual(row["status"], "unsatisfiable")
            self.assertEqual(row["metrics"]["eliminations_before_first_conflict"], 3)
            self.assertFalse(row["metrics"]["early_conflict"])
        self.assertEqual(control["results"]["base"]["metrics"]
                         ["domain_candidates_before_first_elimination"],
                         control["results"]["intersections"]["metrics"]
                         ["domain_candidates_before_first_elimination"])

    def test_incompatible_hubs_are_detected_before_elimination_by_intersections(self):
        control = self.controls["bipyramid_incompatible_hubs"]
        self.assertEqual(control["results"]["base"]["metrics"]
                         ["eliminations_before_first_conflict"], 5)
        self.assertEqual(control["results"]["intersections"]["metrics"]
                         ["eliminations_before_first_conflict"], 0)
        self.assertTrue(control["results"]["intersections"]["metrics"]["early_conflict"])

    def test_pre_elimination_metrics_exclude_first_elimination_and_later_events(self):
        result = deepcopy(self.controls["bipyramid_overlapping_hub_domains"]
                          ["results"]["intersections"]["recorded_result"])
        expected = pre_elimination_metrics(result)
        first = next(i for i, event in enumerate(result["events"])
                     if event["kind"] == "eliminate")
        for event in result["events"][first:]:
            event["stats"]["row_prunes"] += 100_000
            event["stats"]["prunes"] += 100_000
            event["domains"] = [[] for _ in result["graph"]["vertices"]]
        self.assertEqual(pre_elimination_metrics(result), expected)


if __name__ == "__main__":
    unittest.main()
