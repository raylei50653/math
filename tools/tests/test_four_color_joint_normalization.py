"""Common colour orbits preserve complete literal supports and budget semantics."""
from copy import deepcopy
from itertools import permutations, product
import json
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_color_joint_consistency import joint_supports
from test_four_color_joint_consistency import enumerate_supports, initial_factors


class JointNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        inputs = json.loads((ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f/"
                             "propagation/inputs.json").read_text())
        cls.fixed = initial_factors(inputs["graph"], inputs["options"])
        cls.bare = initial_factors(dict(inputs["graph"], fixed=[]), inputs["options"])

    def bucket(self, state):
        return [factor for factor in state["factors"] if 0 in factor[0]]

    def assert_same_support(self, literal, adaptive):
        self.assertTrue(literal["complete"])
        self.assertTrue(adaptive["complete"])
        self.assertEqual(literal["consistent"], adaptive["consistent"])
        self.assertEqual(literal["rows"], adaptive["rows"])
        self.assertEqual(literal["domains"], adaptive["domains"])

    def test_easy_fixed_query_has_no_recognition_or_restart_overhead(self):
        bucket = self.bucket(self.fixed)
        literal = joint_supports(bucket, self.fixed["domains"], normalization=False)
        adaptive = joint_supports(bucket, self.fixed["domains"])
        self.assert_same_support(literal, adaptive)
        self.assertEqual(adaptive["checks"], literal["checks"])
        self.assertEqual(adaptive["method"], "literal")
        self.assertEqual(adaptive["symmetry_checks"], 0)
        self.assertEqual(adaptive["restarted_checks"], 0)

    def test_bare_common_s4_orbits_restore_all_literal_rows_at_lower_total_cost(self):
        bucket = self.bucket(self.bare)
        before = deepcopy((bucket, self.bare["domains"]))
        literal = joint_supports(bucket, self.bare["domains"], normalization=False)
        adaptive = joint_supports(bucket, self.bare["domains"])
        self.assert_same_support(literal, adaptive)
        self.assertEqual(adaptive["method"], "common_color_orbits")
        self.assertEqual(adaptive["symmetry_group_size"], 24)
        self.assertEqual(adaptive["restarted_checks"], 1024)
        self.assertEqual(adaptive["assignments"], 26)
        self.assertEqual(adaptive["anchor_orbits"], 1)
        self.assertEqual(adaptive["representative_assignments"], 26)
        self.assertEqual(adaptive["support_rows"], 2632)
        self.assertGreater(adaptive["symmetry_checks"], 0)
        self.assertLess(adaptive["checks"], literal["checks"])
        self.assertEqual((bucket, self.bare["domains"]), before)

    def test_fixed_literal_colour_allows_only_common_stabilizing_group(self):
        edges = [((0, v), frozenset((a, b) for a in range(4) for b in range(4) if a != b))
                 for v in range(1, 7)]
        factors = [((0,), frozenset({(1,)})), *edges]
        domains = {0: {1}, **{v: set(range(4)) for v in range(1, 7)}}
        literal = joint_supports(factors, domains, normalization=False)
        adaptive = joint_supports(factors, domains)
        self.assert_same_support(literal, adaptive)
        self.assertEqual(adaptive["symmetry_group_size"], 6)
        self.assertEqual(adaptive["domains"][0], {1})
        self.assertTrue(all(adaptive["domains"][v] == {0, 2, 3} for v in range(1, 7)))

    def test_noninvariant_factor_rejects_domain_suggested_symmetry(self):
        factors = [((0,), {(1,)})] + [
            ((0, v), frozenset((a, b) for a in range(4) for b in range(4) if a != b))
            for v in range(1, 7)]
        domains = {v: set(range(4)) for v in range(7)}
        literal = joint_supports(factors, domains, normalization=False)
        adaptive = joint_supports(factors, domains)
        self.assert_same_support(literal, adaptive)
        self.assertEqual(adaptive["method"], "literal_fallback")
        self.assertEqual(adaptive["symmetry_group_size"], 1)
        self.assertEqual(adaptive["domains"][0], {1})

    def test_independent_table_palette_changes_cannot_splice_a_false_witness(self):
        scope = tuple(range(6))
        # Each relation separately can be recoloured into the other. Their
        # literal shared variable requires both 0 and 1, so their join is empty.
        factors = [(scope, frozenset((fixed, *tail) for tail in product(range(4), repeat=5)))
                   for fixed in (0, 1)]
        domains = {v: set(range(4)) for v in scope}
        literal = joint_supports(factors, domains, normalization=False)
        adaptive = joint_supports(factors, domains)
        self.assert_same_support(literal, adaptive)
        self.assertFalse(adaptive["consistent"])
        self.assertEqual(adaptive["symmetry_group_size"], 1)

    def test_budget_cuts_across_warmup_certification_and_final_lift_are_atomic(self):
        bucket = self.bucket(self.bare)
        domains = self.bare["domains"]
        complete = joint_supports(bucket, domains)
        before = deepcopy((bucket, domains))
        for cap in (0, 10, 1024, 1025, 1200, 10000, complete["checks"] - 1):
            ticks = []
            answer = joint_supports(bucket, domains, max_checks=cap,
                                    charge=lambda: ticks.append(1))
            self.assertFalse(answer["complete"], cap)
            self.assertEqual(answer["checks"], cap)
            self.assertEqual(len(ticks), cap)
            self.assertIsNone(answer["rows"])
            self.assertIsNone(answer["domains"])
            self.assertIsNone(answer["consistent"])
            self.assertEqual((bucket, domains), before)
        limited_rows = joint_supports(bucket, domains, max_support_rows=1000)
        self.assertFalse(limited_rows["complete"])
        self.assertEqual(limited_rows["limit_reason"], "support_rows")
        self.assertIsNone(limited_rows["rows"])
        self.assertIsNone(limited_rows["domains"])

        class MainLimit(Exception):
            pass

        ticks = 0

        def charge():
            nonlocal ticks
            ticks += 1
            if ticks == complete["checks"] - 1:
                raise MainLimit

        with self.assertRaises(MainLimit):
            joint_supports(bucket, domains, charge=charge)
        self.assertEqual((bucket, domains), before)

    def test_symmetric_and_asymmetric_networks_match_independent_full_oracle(self):
        rng = random.Random(171717)
        group = list(permutations(range(4)))
        for case in range(120):
            vertices = rng.sample(range(-10, 20), rng.randrange(1, 6))
            domains = {v: {c for c in range(4) if rng.random() < .8} for v in vertices}
            factors = []
            for _ in range(rng.randrange(1, 7)):
                scope = tuple(rng.sample(vertices, rng.randrange(min(len(vertices), 3) + 1)))
                rows = {row for row in product(range(4), repeat=len(scope)) if rng.random() < .1}
                if case % 2 == 0:
                    rows = {tuple(permutation[c] for c in row) for row in rows for permutation in group}
                factors.append((scope, rows))
            count, rows, values = enumerate_supports(factors, domains)
            answer = joint_supports(factors, domains)
            with self.subTest(case=case):
                self.assertTrue(answer["complete"])
                self.assertEqual(answer["consistent"], bool(count))
                self.assertEqual(answer["rows"], rows)
                self.assertEqual(answer["domains"], values)

    def test_factor_generator_survives_restart_and_normalization_flag_is_strict(self):
        bucket = self.bucket(self.bare)
        answer = joint_supports((factor for factor in bucket), self.bare["domains"])
        expected = joint_supports(bucket, self.bare["domains"])
        self.assert_same_support(answer, expected)
        with self.assertRaises(ValueError):
            joint_supports([], {}, normalization=1)

    def test_random_nonempty_networks_exercise_certified_and_rejected_groups(self):
        rng = random.Random(171718)
        observed = set()
        for case in range(18):
            vertices = rng.sample(range(-30, 40), 8)
            center, *leaves = vertices
            pin = rng.randrange(4)
            free = set(range(4)) - {pin}
            domains = {center: {pin}, **{v: set(free) for v in leaves}}
            factors = [((center, v), {(pin, c) for c in free}) for v in leaves]
            for i in range(len(leaves) - 1):
                if rng.random() < .25:
                    factors.append(((leaves[i], leaves[i + 1]),
                                    {(a, b) for a in free for b in free if a != b}))
            if case % 3 == 0:
                # Domains suggest S3, but this complete literal factor breaks it.
                factors.append(((leaves[-1],), {(min(free),)}))
            count, rows, values = enumerate_supports(factors, domains)
            literal = joint_supports(factors, domains, normalization=False)
            adaptive = joint_supports(factors, domains)
            observed.add(adaptive["method"])
            with self.subTest(case=case):
                self.assert_same_support(literal, adaptive)
                self.assertEqual(adaptive["consistent"], bool(count))
                self.assertEqual(adaptive["rows"], rows)
                self.assertEqual(adaptive["domains"], values)
        self.assertIn("common_color_orbits", observed)
        self.assertIn("literal_fallback", observed)


if __name__ == "__main__":
    unittest.main()
