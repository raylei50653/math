"""Independent original-edge checks for optional subtree colour symmetries."""

from copy import deepcopy
from itertools import combinations, permutations
import json
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import test_four_color_local_messages as reference
from four_color_local_messages import solve_local_messages


def solve(graph, **kwargs):
    kwargs.setdefault("audit_metadata", True)
    kwargs.setdefault("color_symmetry", True)
    return solve_local_messages(graph, **kwargs)


def clique(n):
    return {"vertices": list(range(n)),
            "edges": [list(edge) for edge in combinations(range(n), 2)]}


class LocalMessageSymmetryTests(unittest.TestCase):
    def setUp(self):
        # Reuse only independent oracle/assertion helpers.  Inheriting its test
        # class would run the pre-existing suite a second time under discovery.
        self.reference = reference.LocalMessageTests()

    def check_result(self, graph, result, domains=None, *, semantic=True):
        self.assertTrue(result["color_symmetry"])
        self.reference.check_decomposition(graph, result)
        self.reference.check_messages(graph, result, domains, semantic=semantic)
        if result["status"] == "colored":
            self.reference.check_coloring(graph, result, domains)
        else:
            self.assertIsNone(result["colors"])

    def test_two_hundred_conditions_match_original_edges_and_literal_mode(self):
        rng = random.Random(470219)
        for case in range(200):
            n = rng.randrange(8)
            vertices = list(range(n))
            rng.shuffle(vertices)
            graph = {"vertices": vertices,
                     "edges": [list(edge) for edge in combinations(vertices, 2)
                               if rng.random() < .43],
                     "fixed": [[v, rng.randrange(4)] for v in vertices
                               if rng.random() < .17]}
            # Mix fully symmetric domains with several asymmetric signatures;
            # an always-asymmetric generator would rarely exercise quotienting.
            palette = rng.sample(range(4), rng.randrange(1, 5))
            domains = ({v: palette for v in vertices} if case % 3 == 0 else
                       {v: [c for c in range(4) if rng.random() < .75]
                        for v in vertices})
            frozen = deepcopy((graph, domains))
            expected = bool(reference.original_solutions(graph, domains, first_only=True))
            result = solve(graph, domains=domains)
            literal = solve(graph, domains=domains, color_symmetry=False)
            with self.subTest(case=case):
                self.assertEqual(result["status"], "colored" if expected else "unsatisfiable")
                self.assertEqual(result["status"], literal["status"])
                self.check_result(graph, result, domains)
                self.assertEqual((graph, domains), frozen)

    def test_colour_renamings_preserve_literal_domain_and_fixed_constraints(self):
        graph = reference.cycle(6)
        graph["fixed"] = [[0, 2], [3, 1]]
        domains = {0: [0, 2], 1: [0, 1, 3], 2: [0, 1, 3],
                   3: [1, 2], 4: [0, 2, 3], 5: [0, 1, 3]}
        for permutation in permutations(range(4)):
            renamed_graph = dict(graph, fixed=[[v, permutation[c]] for v, c in graph["fixed"]])
            renamed_domains = {v: [permutation[c] for c in colors]
                               for v, colors in domains.items()}
            result = solve(renamed_graph, domains=renamed_domains)
            with self.subTest(permutation=permutation):
                self.assertEqual(result["status"], "colored")
                self.check_result(renamed_graph, result, renamed_domains)

    def test_negative_cache_orbits_keep_every_reply_in_the_queried_frame(self):
        graph = clique(5)
        literal = solve(graph, color_symmetry=False)
        result = solve(graph)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertGreater(result["stats"]["symmetry_cache_hits"], 0)
        self.assertLess(result["stats"]["cache_entries"], literal["stats"]["cache_entries"])
        self.assertLess(result["stats"]["candidate_rows"], literal["stats"]["candidate_rows"])
        self.assertEqual(result["stats"]["writeback_vertices"], 0)
        self.check_result(graph, result)

    def test_positive_orbit_hit_inverts_private_owner_before_writeback(self):
        # The free leaf first answers centre=0 using private colour 1.  The
        # fixed leaf rejects that centre, so the parent asks centre=1 next.
        # The free leaf reuses its positive orbit answer, and its remembered
        # colour must be inverted back to 0 before the final assignment.
        graph = {"vertices": [0, 1, 2], "edges": [[0, 2], [1, 2]],
                 "fixed": [[1, 0]]}
        result = solve(graph)
        self.assertGreater(result["stats"]["symmetry_cache_hits"], 0)
        replies = [event for event in result["transcript"] if event["kind"] == "reply"]
        self.assertTrue(any(event["cached"] and event["possible"]
                            and event["separator"] == [2] and event["colors"] == [1]
                            for event in replies))
        self.assertEqual(result["colors"], [0, 0, 1])
        self.check_result(graph, result)

    def test_two_colour_even_cycle_keeps_fill_edges_and_inverse_frames_separate(self):
        graph = reference.cycle(4)
        domains = {v: [0, 1] for v in graph["vertices"]}
        result = solve(graph, domains=domains)
        self.assertEqual(result["status"], "colored")
        self.check_result(graph, result, domains)
        self.assertIn(dict(zip(graph["vertices"], result["colors"])),
                      reference.original_solutions(graph, domains))

    def test_same_equality_pattern_does_not_override_literal_domain_signatures(self):
        graph = clique(3)
        domains = {0: [0, 1]}
        result = solve(graph, domains=domains)
        self.check_result(graph, result, domains)
        replies = {tuple(event["colors"]): event["possible"]
                   for event in result["transcript"]
                   if event["kind"] == "reply" and event["separator"] == [1, 2]}
        # Both boundary rows have two distinct colours, but only the second
        # leaves an owner colour in {0,1}.  Arbitrary colour-name erasure would
        # incorrectly collapse these two exact query answers.
        self.assertIs(replies[(1, 0)], False)
        self.assertIs(replies[(2, 0)], True)

    def test_private_subtree_domains_prevent_unsound_boundary_only_renaming(self):
        # Each leaf alone permits three centre colours, but their complete
        # joint requirement has no extension.  Its private singleton must
        # constrain every orbit used to answer that leaf's boundary query.
        graph = {"vertices": list(range(5)),
                 "edges": [[0, v] for v in range(1, 5)],
                 "fixed": [[v + 1, v] for v in range(4)]}
        result = solve(graph)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(reference.original_solutions(graph), [])
        self.check_result(graph, result)

    def test_subtree_symmetry_survives_fixed_colours_elsewhere(self):
        # The four isolated anchors force the whole-graph colour stabilizer to
        # identity.  They do not restrict the separate K5 subtree's full S4.
        graph = clique(5)
        graph["vertices"] += [10, 11, 12, 13]
        graph["fixed"] = [[10 + c, c] for c in range(4)]
        literal = solve(graph, color_symmetry=False)
        result = solve(graph)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertGreater(result["stats"]["symmetry_cache_hits"], 0)
        self.assertLess(result["stats"]["cache_entries"], literal["stats"]["cache_entries"])
        self.check_result(graph, result)

    def test_fourteen_point_writeback_and_negative_control(self):
        graph = json.loads((ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f/"
                            "propagation/inputs.json").read_text())["graph"]
        for condition, expected in ((graph, False), (dict(graph, fixed=[]), True),
                                    (dict(graph, edges=[e for e in graph["edges"]
                                                       if set(e) != {7, 13}]), True)):
            result = solve(condition)
            with self.subTest(fixed=condition.get("fixed"), edges=len(condition["edges"])):
                self.assertEqual(result["status"], "colored" if expected else "unsatisfiable")
                self.check_result(condition, result, semantic=False)
                if expected:
                    self.assertGreater(result["stats"]["symmetry_cache_hits"], 0)
                    answers = reference.original_solutions(condition)
                    self.assertIn(dict(zip(condition["vertices"], result["colors"])), answers)

    def test_limits_and_truncated_transcripts_never_publish_partial_colours(self):
        for graph in (clique(5), reference.cycle(6)):
            full = solve(graph)
            for budget, statistic in (("max_checks", "checks"),
                                      ("max_messages", "messages"),
                                      ("max_cache_entries", "cache_entries")):
                for cap in (0, 1, full["stats"][statistic] - 1):
                    result = solve(graph, **{budget: cap})
                    with self.subTest(n=len(graph["vertices"]), budget=budget, cap=cap):
                        self.assertEqual(result["status"], "limit")
                        self.assertIsNone(result["colors"])
                        self.assertEqual(result["limit_reason"], budget)
                        if result["decomposition"] is not None:
                            self.reference.check_messages(graph, result)
            for cap in (0, 1, 3):
                result = solve(graph, transcript_limit=cap)
                self.assertEqual(result["status"], full["status"])
                self.assertEqual(result["colors"], full["colors"])
                self.assertEqual(result["stats"], full["stats"])
                self.assertLessEqual(len(result["transcript"]), cap)

    def test_switch_requires_exact_boolean_and_defaults_to_literal_mode(self):
        graph = reference.cycle(4)
        for value in (0, 1, None, "yes", []):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    solve(graph, color_symmetry=value)
        default = solve_local_messages(graph)
        explicit = solve_local_messages(graph, color_symmetry=False)
        self.assertEqual(default, explicit)
        self.assertFalse(default["color_symmetry"])


if __name__ == "__main__":
    unittest.main()
