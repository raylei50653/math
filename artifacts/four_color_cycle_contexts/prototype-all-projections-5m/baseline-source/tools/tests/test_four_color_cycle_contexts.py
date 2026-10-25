"""Exact conditional-cycle propagation without choosing a context colour.

Independent enumeration uses literal edges and domains only.  Multiple feasible
context colours contribute a union of pair rows; they are never intersected as
if the context had already been assigned every possible colour at once.
"""

from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import random
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_constraints import solve_constraints
from four_color_conflict_priority import original_solutions, verify_preservation
from four_color_cycle_contexts import derive_cycle_context


def conditional_cycle_oracle(graph, cycle, context, masks):
    """Project the actual cycle edges and actual context spokes by brute force.

    Chords and attachments deliberately remain outside this local query.  The
    integration tests separately require the solver to retain every such edge.
    """
    by_vertex = dict(zip(graph["vertices"], masks))
    original = {frozenset(edge) for edge in graph["edges"]}
    local_edges = [(cycle[i], cycle[(i + 1) % len(cycle)])
                   for i in range(len(cycle))]
    local_edges += [(context, vertex) for vertex in cycle
                    if frozenset((context, vertex)) in original]
    scope = [context, *cycle]
    allowed = [[colour for colour in range(4) if by_vertex[vertex] & (1 << colour)]
               for vertex in scope]
    assignments = []
    for row in product(*allowed):
        assignment = dict(zip(scope, row))
        if all(assignment[left] != assignment[right] for left, right in local_edges):
            assignments.append(assignment)
    supports = {vertex: sum(1 << colour for colour in
                            {row[vertex] for row in assignments})
                for vertex in scope}
    pairs = [{"scope": [context, vertex],
              "rows": [list(row) for row in sorted(
                  {(assignment[context], assignment[vertex])
                   for assignment in assignments})]}
             for vertex in cycle]
    edge_pairs = [{"scope": [cycle[index], cycle[(index + 1) % len(cycle)]],
                   "rows": [list(row) for row in sorted(
                       {(assignment[cycle[index]], assignment[cycle[(index + 1) % len(cycle)]])
                        for assignment in assignments})]}
                  for index in range(len(cycle))]
    conditioned_edges = [{"scope": [context, cycle[index], cycle[(index + 1) % len(cycle)]],
                          "rows": [list(row) for row in sorted(
                              {(assignment[context], assignment[cycle[index]],
                                assignment[cycle[(index + 1) % len(cycle)]])
                               for assignment in assignments})]}
                         for index in range(len(cycle))]
    cases = []
    for colour in range(4):
        if not by_vertex[context] & (1 << colour):
            continue
        selected = [row for row in assignments if row[context] == colour]
        cases.append({"context_color": colour, "row_count": len(selected),
                      "cycle_supports": [sum(1 << value for value in
                                             {row[vertex] for row in selected})
                                         for vertex in cycle]})
    return {"row_count": len(assignments),
            "context_support_mask": supports[context],
            "cycle_supports": [supports[vertex] for vertex in cycle],
            "pair_relations": pairs, "cycle_edge_relations": edge_pairs,
            "context_edge_relations": conditioned_edges, "cases": cases}


def frozen_cases():
    return json.loads((ROOT / "artifacts/four_color_guarantee_gap/inputs.json").read_text())


class ConditionalCycleHelperTests(unittest.TestCase):
    def assert_exact(self, graph, cycle, context, masks):
        before = deepcopy((graph, cycle, masks))
        expected = conditional_cycle_oracle(graph, cycle, context, masks)
        result = derive_cycle_context(graph, cycle, context, masks)
        for field in ("row_count", "context_support_mask", "cycle_supports", "pair_relations",
                      "cycle_edge_relations", "context_edge_relations"):
            self.assertEqual(result[field], expected[field], field)
        self.assertEqual(
            [{field: case[field] for field in ("context_color", "row_count", "cycle_supports")}
             for case in result["cases"]], expected["cases"])
        self.assertEqual((graph, cycle, masks), before)
        return result

    def test_every_partial_spoke_pattern_matches_literal_enumeration(self):
        rng = random.Random(20261025)
        cycle, context = [17, -4, 90, 8], 41
        vertices = [8, 41, -4, 100, 17, 90]
        edges = [[cycle[i], cycle[(i + 1) % 4]] for i in range(4)]
        # These original chord/attachment edges must not be silently treated as
        # cycle transitions or as fictitious context spokes.
        edges += [[17, 90], [41, 100], [100, 8]]
        for spoke_bits in range(16):
            graph = {"vertices": vertices,
                     "edges": edges + [[context, vertex]
                                       for index, vertex in enumerate(cycle)
                                       if spoke_bits & (1 << index)]}
            for variant in range(8):
                masks = [15] * len(vertices) if variant == 0 else [rng.randrange(16) for _ in vertices]
                with self.subTest(spoke_bits=spoke_bits, masks=masks):
                    result = self.assert_exact(graph, cycle, context, masks)
                    actual = {frozenset(edge) for edge in result["context_edges"]}
                    expected = {frozenset((context, vertex))
                                for index, vertex in enumerate(cycle)
                                if spoke_bits & (1 << index)}
                    self.assertEqual(actual, expected)

    def test_feasible_context_cases_are_unioned_without_choosing_a_colour(self):
        cycle = [0, 1, 2, 3]
        graph = {"vertices": [0, 1, 2, 3, 4],
                 "edges": [[i, (i + 1) % 4] for i in range(4)] + [[4, i] for i in cycle]}
        result = self.assert_exact(graph, cycle, 4, [7] * 5)
        self.assertEqual(result["row_count"], 6)
        self.assertEqual(result["context_support_mask"], 7)
        self.assertEqual(result["cycle_supports"], [7] * 4)
        self.assertEqual([case["row_count"] for case in result["cases"]], [2, 2, 2])
        expected_rows = [[left, right] for left in range(3) for right in range(3)
                         if left != right]
        self.assertTrue(all(relation["rows"] == expected_rows
                            for relation in result["pair_relations"]))

    def test_non_neighbor_pair_may_retain_equal_colours(self):
        graph = {"vertices": [0, 1, 2, 3, 4],
                 "edges": [[i, (i + 1) % 4] for i in range(4)] + [[4, 0], [4, 2]]}
        result = self.assert_exact(graph, [0, 1, 2, 3], 4, [15] * 5)
        by_vertex = {relation["scope"][1]: relation["rows"]
                     for relation in result["pair_relations"]}
        self.assertNotIn([0, 0], by_vertex[0])
        self.assertIn([0, 0], by_vertex[1])

    def test_pair_rows_retain_information_missing_from_unchanged_unary_supports(self):
        graph = {"vertices": list(range(5)),
                 "edges": [[i, (i + 1) % 4] for i in range(4)] + [[4, i] for i in range(4)]}
        masks = [14, 5, 11, 13, 3]
        result = self.assert_exact(graph, [0, 1, 2, 3], 4, masks)
        self.assertEqual(result["cycle_supports"], masks[:4])
        self.assertEqual(result["context_support_mask"], masks[4])
        pair = result["pair_relations"][0]
        self.assertEqual(pair["scope"], [4, 0])
        self.assertEqual(pair["rows"], [[0, 1], [0, 3], [1, 2], [1, 3]])
        # Both colours survive separately and satisfy their original edge,
        # but their joint choice cannot complete the same actual cycle.
        self.assertNotIn([0, 2], pair["rows"])

    def test_long_context_count_keeps_exact_integer_arithmetic(self):
        size = 60
        graph = {"vertices": list(range(size + 1)),
                 "edges": [[i, (i + 1) % size] for i in range(size)]
                          + [[size, i] for i in range(size)]}
        result = derive_cycle_context(graph, list(range(size)), size, [15] * (size + 1))
        # For each of four hub colours, the even rim has three available
        # colours and 2**size + 2 closed colourings.
        self.assertEqual(result["row_count"], 4 * (2 ** size + 2))
        self.assertGreater(result["row_count"], 2 ** 53)
        self.assertEqual([case["row_count"] for case in result["cases"]],
                         [2 ** size + 2] * 4)

    def test_empty_local_domain_means_no_rows_but_external_empty_domain_is_irrelevant(self):
        graph = {"vertices": [0, 1, 2, 3, 4],
                 "edges": [[0, 1], [1, 2], [2, 0], [3, 0], [3, 4]]}
        for vertex in (0, 1, 2, 3):
            masks = [15] * 5
            masks[vertex] = 0
            with self.subTest(empty_vertex=vertex):
                result = self.assert_exact(graph, [0, 1, 2], 3, masks)
                self.assertEqual(result["row_count"], 0)
                self.assertEqual(result["context_support_mask"], 0)
                self.assertEqual(result["cycle_supports"], [0] * 3)
                self.assertTrue(all(not relation["rows"] for relation in result["pair_relations"]))
        external_empty = self.assert_exact(graph, [0, 1, 2], 3, [15, 15, 15, 15, 0])
        self.assertGreater(external_empty["row_count"], 0)

    def test_interrupted_pure_query_has_no_partial_input_mutation(self):
        graph = {"vertices": list(range(8)),
                 "edges": [[i, (i + 1) % 7] for i in range(7)] + [[7, i] for i in range(7)]}
        cycle, masks = list(range(7)), [15] * 8
        before = deepcopy((graph, cycle, masks))
        charges = []
        complete = derive_cycle_context(graph, cycle, 7, masks,
                                        charge=lambda: charges.append(None))
        self.assertGreater(len(charges), 0)

        class Interrupted(Exception):
            pass

        for allowance in (0, 1, len(charges) // 2, len(charges) - 1):
            used = 0

            def charge():
                nonlocal used
                if used == allowance:
                    raise Interrupted
                used += 1

            with self.subTest(allowance=allowance):
                with self.assertRaises(Interrupted):
                    derive_cycle_context(graph, cycle, 7, masks, charge=charge)
                self.assertEqual((graph, cycle, masks), before)
        self.assertEqual(derive_cycle_context(graph, cycle, 7, masks), complete)

    def test_invalid_cycle_cannot_manufacture_original_edges(self):
        graph = {"vertices": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [3, 0]]}
        with self.assertRaises(ValueError):
            derive_cycle_context(graph, [0, 1, 2], 3, [15] * 4)
        valid = {"vertices": [0, 1, 2, 3], "edges": [[0, 1], [1, 2], [2, 0]]}
        for cycle, context, masks in (([0, 1, 1], 3, [15] * 4),
                                      ([0, 1, 2], 1, [15] * 4),
                                      ([0, 1, 2], 3, [15, 15, 15]),
                                      ([0, 1, 2], 3, [15, 15, 15, 16])):
            with self.subTest(cycle=cycle, context=context, masks=masks):
                with self.assertRaises(ValueError):
                    derive_cycle_context(valid, cycle, context, masks)


class CycleContextIntegrationTests(unittest.TestCase):
    def solve(self, graph, **options):
        defaults = dict(use_intersections=True, use_cycles=True,
                        use_cycle_contexts=True, use_conflicts=False, use_c5=False,
                        record_relations=True, trace_limit=10000,
                        max_checks=5_000_000)
        defaults.update(options)
        return solve_constraints(graph, **defaults)

    def assert_delayed_writeback(self, graph, result):
        fixed = dict(graph.get("fixed", []))
        expected = [fixed.get(vertex, -1) for vertex in graph["vertices"]]
        for event in result["events"]:
            if event["phase"] == "reduce":
                self.assertEqual(event["colors"], expected)
            if event["kind"] == "writeback":
                self.assertEqual(event["depth"], len(graph["vertices"]))
        self.assertEqual(result["stats"]["decisions"], 0)
        self.assertEqual(result["stats"]["backtracks"], 0)

    def test_primary_gap_closes_and_secondary_boundary_remains_exact(self):
        expected_baseline = {"primary-gap": 8, "secondary-gap": 4}
        expected_context = {"primary-gap": 0, "secondary-gap": 4}
        for case in frozen_cases():
            if case["role"] not in expected_baseline:
                continue
            graph = case["graph"]
            with self.subTest(case=case["name"]):
                self.assertEqual(list(original_solutions(graph)), [])
                baseline = self.solve(graph, use_cycle_contexts=False)
                self.assertEqual(baseline["status"], "unsatisfiable")
                self.assertEqual(baseline["stats"]["eliminations"], expected_baseline[case["role"]])
                result = self.solve(graph)
                self.assertEqual(result["status"], "unsatisfiable")
                self.assertEqual(result["graph_sha256"], case["graph_sha256"])
                # The 9-point context remains a recorded boundary of this
                # strengthening: propagation stability is still not SAT.
                self.assertEqual(result["stats"]["eliminations"], expected_context[case["role"]])
                self.assertGreater(result["stats"]["cycle_context_queries"], 0)
                original_edges = {frozenset(edge) for edge in graph["edges"]}
                context_events = [event for event in result["events"]
                                  if event.get("relation_kind") == "cycle_context"]
                self.assertTrue(context_events)
                for event in context_events:
                    cycle, context = event["cycle_vertices"], event["context_vertex"]
                    self.assertEqual(event["frontier"], [context, *cycle])
                    self.assertNotIn(context, cycle)
                    self.assertEqual(len(cycle), len(set(cycle)))
                    self.assertTrue(all(frozenset((cycle[i], cycle[(i + 1) % len(cycle)]))
                                        in original_edges for i in range(len(cycle))))
                    self.assertTrue(all(frozenset(edge) in original_edges
                                        for edge in event["causal_edges"]))
                self.assertFalse(any(event["phase"] == "writeback" for event in result["events"]))
                self.assert_delayed_writeback(graph, result)

    def test_even_and_relaxed_controls_preserve_every_original_solution(self):
        for case in frozen_cases():
            if case["expected_solution_count"] == 0:
                continue
            graph = case["graph"]
            solutions = list(original_solutions(graph))
            with self.subTest(case=case["name"]):
                self.assertEqual(len(solutions), case["expected_solution_count"])
                result = self.solve(graph)
                audit = verify_preservation(graph, solutions, result)
                self.assertTrue(audit["all_solutions_preserved"])
                self.assertTrue(audit["witness_verified"])
                self.assertGreater(result["stats"]["cycle_context_queries"], 0)
                self.assert_delayed_writeback(graph, result)

    def test_partial_spokes_chords_and_attachments_preserve_full_graph_solutions(self):
        edges = [[i, (i + 1) % 4] for i in range(4)] + [[4, 0], [4, 2], [0, 2], [4, 5], [1, 5]]
        for fixed in ([], [[5, 3]], [[0, 0], [2, 0]], [[4, 1], [5, 1]]):
            graph = {"vertices": list(range(6)), "edges": edges, "fixed": fixed}
            with self.subTest(fixed=fixed):
                solutions = list(original_solutions(graph))
                result = self.solve(graph)
                audit = verify_preservation(graph, solutions, result)
                self.assertTrue(audit["all_solutions_preserved"])
                self.assert_delayed_writeback(graph, result)

    def test_derived_pair_relation_feeds_intersections_when_no_unary_colour_changes(self):
        masks = [14, 5, 11, 13, 3]
        graph = {"vertices": list(range(5)), "fixed": [],
                 "edges": [[i, (i + 1) % 4] for i in range(4)] + [[4, i] for i in range(4)]}
        # Real private fixed leaves implement these domains, with no input
        # candidate metadata and no special motif recognizer involved.
        for vertex, mask in enumerate(masks):
            for colour in range(4):
                if not mask & (1 << colour):
                    leaf = len(graph["vertices"])
                    graph["vertices"].append(leaf)
                    graph["edges"].append([vertex, leaf])
                    graph["fixed"].append([leaf, colour])
        solutions = list(original_solutions(graph))
        self.assertEqual(len(solutions), 11)
        result = self.solve(graph, use_substructures=False)
        self.assertTrue(verify_preservation(graph, solutions, result)["all_solutions_preserved"])
        query_index = next(index for index, event in enumerate(result["events"])
                           if event["kind"] == "cycle_context")
        query = result["events"][query_index]
        self.assertEqual(query["domain_masks"], query["supported_domain_masks"])
        self.assertEqual(result["stats"]["cycle_context_prunes"], 0)
        self.assertGreater(query["context_rows_added"], 0)
        intersections = []
        for event in result["events"][query_index + 1:]:
            if event["kind"] == "eliminate":
                break
            if event["kind"] == "intersection":
                intersections.append(event)
        # The original edge and the new reversed-order derived pair share the
        # entire literal (0,4) interface.  Their semijoin removes a joint choice
        # even though every individual candidate colour remains possible.
        self.assertTrue(any(set(event["frontier"]) == {0, 4}
                            and event["left_scope"] == [0, 4]
                            and event["right_scope"] == [4, 0]
                            and event["left_removed"] + event["right_removed"] > 0
                            for event in intersections))
        self.assert_delayed_writeback(graph, result)

    def test_seeded_fixed_contexts_preserve_all_literal_solutions(self):
        rng = random.Random(20261026)
        vertices = list(range(7))
        possible_edges = [(left, right) for left in vertices for right in vertices if left < right]
        for index in range(20):
            graph = {"vertices": vertices,
                     "edges": [list(edge) for edge in possible_edges if rng.random() < 0.45],
                     "fixed": [[vertex, rng.randrange(4)]
                               for vertex in rng.sample(vertices, rng.randrange(3))]}
            with self.subTest(case=index):
                solutions = list(original_solutions(graph))
                result = self.solve(graph)
                self.assertTrue(verify_preservation(graph, solutions, result)["all_solutions_preserved"])
                self.assert_delayed_writeback(graph, result)

    def test_zero_work_budget_is_inconclusive_without_any_context_commit(self):
        graph = frozen_cases()[0]["graph"]
        result = self.solve(graph, max_checks=0)
        self.assertEqual(result["status"], "limit")
        self.assertEqual(result["stats"]["checks"], 0)
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertFalse(any(event.get("relation_kind") == "cycle_context"
                             for event in result["events"]))
        self.assert_delayed_writeback(graph, result)

    def test_mid_projection_staging_budget_cannot_commit_partial_domains_or_factors(self):
        graph = frozen_cases()[1]["graph"]
        complete = self.solve(graph)
        first = next(event for event in complete["events"] if event["kind"] == "cycle_context")
        self.assertGreater(first["context_rows_added"], 1)
        projections = (first["pair_relations"] + first["cycle_edge_relations"]
                       + first["context_edge_relations"])
        self.assertEqual(first["context_rows_added"], sum(len(item["rows"]) for item in projections))
        # The event is emitted only after all binary and ternary rows are staged.
        # Stop on its last charged row, after the exact pure cycle query has
        # returned but before any domain/factor update may become visible.
        limited = self.solve(graph, max_checks=first["stats"]["checks"] - 1)
        self.assertEqual(limited["status"], "limit")
        self.assertEqual(limited["stats"]["cycle_context_queries"], 1)
        self.assertEqual(limited["stats"]["cycle_context_rows"], 0)
        self.assertEqual(limited["stats"]["cycle_context_factors"], 0)
        self.assertEqual(limited["stats"]["cycle_context_prunes"], 0)
        self.assertEqual(limited["stats"]["eliminations"], 0)
        self.assertFalse(any(event.get("relation_kind") == "cycle_context"
                             for event in limited["events"]))
        retained = dict(zip(graph["vertices"], limited["events"][-1]["domains"]))
        self.assertEqual([sum(1 << colour for colour in retained[vertex])
                          for vertex in first["frontier"]], first["domain_masks"])
        self.assert_delayed_writeback(graph, limited)

    def test_context_storage_limit_cannot_commit_part_of_a_query(self):
        graph = frozen_cases()[1]["graph"]
        complete = self.solve(graph)
        first = next(event for event in complete["events"] if event["kind"] == "cycle_context")
        with patch("four_color_constraints.TABLE_ROW_CEILING", 1):
            limited = self.solve(graph)
        self.assertEqual(limited["status"], "limit")
        self.assertEqual(limited["stats"]["cycle_context_queries"], 1)
        self.assertEqual(limited["stats"]["cycle_context_rows"], 0)
        self.assertEqual(limited["stats"]["cycle_context_factors"], 0)
        self.assertEqual(limited["stats"]["cycle_context_prunes"], 0)
        self.assertEqual(limited["stats"]["eliminations"], 0)
        retained = dict(zip(graph["vertices"], limited["events"][-1]["domains"]))
        self.assertEqual([sum(1 << colour for colour in retained[vertex])
                          for vertex in first["frontier"]], first["domain_masks"])
        self.assert_delayed_writeback(graph, limited)

    def test_interrupted_context_discovery_reports_incomplete_metadata(self):
        graph = frozen_cases()[1]["graph"]
        complete = self.solve(graph)
        first = next(event for event in complete["events"] if event["kind"] == "cycle_context")
        before_contexts = first["stats"]["checks"] - first["stats"]["cycle_context_checks"]
        limited = self.solve(graph, max_checks=before_contexts + 1)
        self.assertEqual(limited["status"], "limit")
        self.assertEqual(limited["stats"]["cycle_context_queries"], 0)
        self.assertEqual(limited["stats"]["cycle_context_scan_steps"], 1)
        self.assertTrue(limited["cycle_context_scan"]["truncated"])
        self.assertFalse(limited["cycle_context_scan"]["last_discovery_complete"])
        self.assertTrue(limited["cycle_context_scan"]["last_discovery_interrupted"])
        self.assertEqual(limited["stats"]["cycle_context_rows"], 0)
        self.assert_delayed_writeback(graph, limited)

    def test_zero_context_caps_preserve_the_original_exact_fallback(self):
        for case in frozen_cases()[:2]:
            graph = case["graph"]
            solutions = list(original_solutions(graph))
            for caps in (dict(cycle_context_max_contexts=0),
                         dict(cycle_context_max_scan_steps=0)):
                with self.subTest(case=case["name"], caps=caps):
                    result = self.solve(graph, **caps)
                    self.assertEqual(result["stats"]["cycle_context_queries"], 0)
                    self.assertTrue(result["cycle_context_scan"]["truncated"])
                    self.assertTrue(verify_preservation(graph, solutions, result)["all_solutions_preserved"])
                    self.assert_delayed_writeback(graph, result)

    def test_cli_enables_contexts_with_both_required_propagators(self):
        graph = frozen_cases()[0]["graph"]
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "graph.json", Path(directory) / "result.json"
            source.write_text(json.dumps(graph))
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "four_color_lab.py"),
                 "solve", str(source), "--engine", "constraints", "--intersections",
                 "--cycles", "--cycle-contexts", "--no-conflicts", "--json", str(output)],
                capture_output=True, text=True, timeout=30)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(output.read_text())
            self.assertTrue(result["use_cycle_contexts"])
            self.assertTrue(result["use_intersections"])
            self.assertTrue(result["use_cycles"])
            self.assertEqual(result["status"], "unsatisfiable")
            self.assertEqual(result["stats"]["eliminations"], 0)
            self.assertEqual(json.loads(completed.stdout)["status"], result["status"])


if __name__ == "__main__":
    unittest.main()
