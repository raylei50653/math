"""Exact original-edge checks for intersections combined with cycle support.

These tests deliberately allow multiple solutions.  A cycle is only an extra
propagator: its chords, attachments, and every original edge remain constraints.
"""

from copy import deepcopy
from itertools import combinations
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
from four_color_cycle_propagation import find_original_cycles
from four_color_larger_cases import create_oracle, double_wheel_case, equality_tree_case
from four_color_larger_experiment import verify_projections


def original_edge_solutions(graph):
    """Enumerate assignments using only literal fixed colours and original edges."""
    adjacency = {vertex: set() for vertex in graph["vertices"]}
    for left, right in graph["edges"]:
        adjacency[left].add(right)
        adjacency[right].add(left)
    fixed = dict(graph.get("fixed", []))
    order = sorted(graph["vertices"],
                   key=lambda vertex: (vertex not in fixed, -len(adjacency[vertex]), vertex))
    assignment, solutions = {}, []

    def visit(offset):
        if offset == len(order):
            solutions.append(dict(assignment))
            return
        vertex = order[offset]
        for colour in ((fixed[vertex],) if vertex in fixed else range(4)):
            if any(assignment.get(neighbor) == colour for neighbor in adjacency[vertex]):
                continue
            assignment[vertex] = colour
            visit(offset + 1)
            del assignment[vertex]

    visit(0)
    return solutions


def escape_ring():
    """An odd ring whose four restricted vertices force its escape to {2,3}."""
    return {"vertices": list(range(7)),
            "edges": [[i, (i + 1) % 5] for i in range(5)]
                     + [[vertex, fixed] for vertex in range(1, 5) for fixed in (5, 6)],
            "fixed": [[5, 2], [6, 3]]}


def alternating_propagators():
    """Two original odd rings linked through complete shared-triangle factors.

    The first equality gadget restricts ring vertex 1 to {0,1}.  The first ring
    then forces vertex 0 to {2,3}; a second equality gadget transmits this to
    vertex 13, whose second ring needs it outside {2,3}.  No colour is guessed.
    """
    edges = [[i, (i + 1) % 5] for i in range(5)]
    # The fixed leaves 18,19 impose {0,1}; 16,17 impose {2,3}.
    edges += [[vertex, leaf] for vertex in (2, 3, 4, 8) for leaf in (18, 19)]
    for triangle, hubs in (((5, 6, 7), (1, 8)), ((9, 10, 11), (0, 13))):
        edges += [list(edge) for edge in combinations(triangle, 2)]
        edges += [[hub, vertex] for hub in hubs for vertex in triangle]
    second_ring = (13, 12, 14, 15, 20)
    edges += [[second_ring[i], second_ring[(i + 1) % 5]] for i in range(5)]
    edges += [[vertex, leaf] for vertex in second_ring[1:] for leaf in (16, 17)]
    return {"vertices": list(range(21)), "edges": edges,
            "fixed": [[16, 0], [17, 1], [18, 2], [19, 3]]}


class CombinedCycleTests(unittest.TestCase):
    def solve(self, graph, **options):
        defaults = dict(use_intersections=True, use_cycles=True,
                        use_conflicts=False, use_c5=False,
                        record_relations=True, trace_limit=10000,
                        max_checks=5_000_000)
        defaults.update(options)
        return solve_constraints(graph, **defaults)

    def assert_witness(self, graph, result):
        self.assertEqual(result["status"], "colored")
        self.assertEqual(len(result["colors"]), len(graph["vertices"]))
        self.assertTrue(all(type(colour) is int and colour in range(4)
                            for colour in result["colors"]))
        assignment = dict(zip(graph["vertices"], result["colors"]))
        self.assertTrue(all(assignment[left] != assignment[right]
                            for left, right in graph["edges"]))
        self.assertTrue(all(assignment[vertex] == colour
                            for vertex, colour in graph.get("fixed", [])))

    def assert_delayed_writeback(self, graph, result):
        fixed = dict(graph.get("fixed", []))
        expected = [fixed.get(vertex, -1) for vertex in graph["vertices"]]
        for event in result["events"]:
            if event["phase"] == "reduce":
                self.assertEqual(event["colors"], expected)
            elif event["kind"] == "writeback":
                self.assertEqual(set(event["eliminated_vertices"]), set(graph["vertices"]))
        self.assertEqual(result["stats"]["decisions"], 0)
        self.assertEqual(result["stats"]["backtracks"], 0)

    def assert_preserved(self, graph, solutions, result):
        """Every full original solution must survive all trace and saved rows."""
        self.assertFalse(result["trace_truncated"])
        for event in result["events"]:
            if event["phase"] == "reduce":
                for solution in solutions:
                    self.assertTrue(all(solution[vertex] in domain
                                        for vertex, domain in zip(graph["vertices"], event["domains"])))
        for record in result["elimination_records"]:
            saved = {tuple(row["boundary"]): set(row["colors"]) for row in record["rows"]}
            inputs = [(relation["scope"], {tuple(row) for row in relation["rows"]})
                      for relation in record["input_relations"]]
            for solution in solutions:
                self.assertTrue(all(solution[entry["vertex"]] in entry["colors"]
                                    for entry in record["source_domains"]))
                for scope, rows in inputs:
                    self.assertIn(tuple(solution[vertex] for vertex in scope), rows)
                boundary = tuple(solution[vertex] for vertex in record["scope"])
                self.assertIn(solution[record["vertex"]], saved.get(boundary, set()))

    def test_97_rim_conflict_is_found_before_elimination_and_writeback(self):
        graph = double_wheel_case(97)["graph"]
        baseline = self.solve(graph, use_cycles=False)
        combined = self.solve(graph)
        self.assertEqual(baseline["status"], "unsatisfiable")
        self.assertEqual(baseline["stats"]["eliminations"], 95)
        self.assertEqual(combined["status"], "unsatisfiable")
        self.assertEqual(combined["stats"]["eliminations"], 0)
        self.assertGreater(combined["stats"]["cycle_conflicts"], 0)
        self.assertFalse(any(event["phase"] == "writeback" for event in combined["events"]))
        self.assert_delayed_writeback(graph, combined)

    def test_even_98_rim_preserves_both_complete_solutions_and_reconstructs_one(self):
        case = double_wheel_case(98)
        graph, oracle = case["graph"], create_oracle(case)
        self.assertEqual(oracle.solution_count, 2)
        result = self.solve(graph)
        self.assert_witness(graph, result)
        self.assertIn(result["colors"], oracle.witnesses(limit=2))
        self.assertGreater(result["stats"]["cycle_queries"], 0)
        checked = verify_projections(oracle, result, 100000)
        self.assertTrue(checked["complete_projections_checked"])
        self.assertEqual(checked["exact_global_solution_count"], 2)
        self.assertEqual(checked["projection_limits"], [])
        self.assert_delayed_writeback(graph, result)

    def test_long_unrestricted_cycle_preserves_exact_count_above_javascript_integer_limit(self):
        graph = {"vertices": list(range(40)),
                 "edges": [[vertex, (vertex + 1) % 40] for vertex in range(40)]}
        result = self.solve(graph, max_checks=1_000_000)
        event = next(event for event in result["events"]
                     if event["kind"] == "cycle_query" and event["cycle_length"] == 40)
        # Closing a literal four-colour even cycle gives 3**n + 3 rows.
        expected = 3 ** 40 + 3
        self.assertGreater(expected, 2 ** 53)
        self.assertEqual(event["relation_rows"], expected)
        self.assertEqual(event["relation_rows_decimal"], str(expected))
        self.assert_witness(graph, result)
        self.assert_delayed_writeback(graph, result)

    def test_representative_structured_families_keep_every_global_projection(self):
        cases = [equality_tree_case(shape, size, endpoint)
                 for shape, size in (("chain", 2), ("binary", 6))
                 for endpoint in ("compatible", "overlap", "incompatible")]
        cases += [double_wheel_case(size) for size in (4, 5)]
        for case in cases:
            with self.subTest(case=case["name"]):
                oracle = create_oracle(case)
                result = self.solve(case["graph"])
                self.assertEqual(result["status"], "colored" if oracle.solution_count else "unsatisfiable")
                checked = verify_projections(oracle, result, 100000)
                self.assertTrue(checked["complete_projections_checked"])
                self.assertTrue(checked["trace_complete"])
                self.assertEqual(checked["projection_limits"], [])
                if oracle.solution_count:
                    self.assert_witness(case["graph"], result)
                self.assert_delayed_writeback(case["graph"], result)

    def test_all_1024_five_vertex_graphs_match_independent_original_edge_search(self):
        possible_edges = list(combinations(range(5), 2))
        unsatisfiable = 0
        for bits in range(1 << len(possible_edges)):
            graph = {"vertices": list(range(5)),
                     "edges": [list(edge) for index, edge in enumerate(possible_edges)
                               if bits & (1 << index)]}
            expected = original_edge_solutions(graph)
            result = self.solve(graph, record_relations=False, trace_limit=0)
            with self.subTest(edge_mask=bits):
                self.assertEqual(result["status"], "colored" if expected else "unsatisfiable")
                if expected:
                    self.assert_witness(graph, result)
                else:
                    unsatisfiable += 1
        # This suite includes the actual non-four-colourable K5; no planarity
        # theorem or "all generated graphs should be colourable" assumption.
        self.assertEqual(unsatisfiable, 1)

    def test_fixed_random_seven_vertex_contexts_preserve_all_original_solutions(self):
        rng = random.Random(20261025)
        pruned = 0
        graphs = [escape_ring()]
        for _ in range(24):
            graph = {"vertices": list(range(7)),
                     "edges": [list(edge) for edge in combinations(range(7), 2)
                               if rng.random() < 0.4],
                     "fixed": [[vertex, rng.randrange(4)]
                               for vertex in rng.sample(range(7), rng.randrange(3))]}
            graphs.append(graph)
        for index, graph in enumerate(graphs):
            with self.subTest(case=index):
                solutions = original_edge_solutions(graph)
                result = self.solve(graph)
                self.assertEqual(result["status"], "colored" if solutions else "unsatisfiable")
                self.assert_preserved(graph, solutions, result)
                self.assert_delayed_writeback(graph, result)
                if solutions:
                    self.assert_witness(graph, result)
                    pruned += bool(result["stats"]["cycle_prunes"])
        self.assertGreater(pruned, 0, "preservation must include an actual cycle-domain deletion")

    def test_intersections_and_cycles_reach_a_common_fixed_point(self):
        graph = alternating_propagators()
        self.assertEqual(original_edge_solutions(graph), [])
        result = self.solve(graph)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertGreater(result["stats"]["intersection_prunes"], 0)
        self.assertGreater(result["stats"]["cycle_prunes"], 0)
        self.assertGreater(result["stats"]["conflicts"], 0)
        changing_cycles = [offset for offset, event in enumerate(result["events"])
                           if event["kind"] == "cycle_query"
                           and event["domain_masks"] != event["supported_domain_masks"]]
        intersections = [offset for offset, event in enumerate(result["events"])
                         if event["kind"] == "intersection"]
        self.assertTrue(changing_cycles)
        self.assertTrue(any(offset < changing_cycles[0] for offset in intersections))
        self.assertTrue(any(offset > changing_cycles[-1] for offset in intersections),
                        "cycle consequences must feed back into shared-factor filtering")
        self.assert_delayed_writeback(graph, result)

    def test_zero_cycle_discovery_caps_only_omit_optional_propagators(self):
        for case in (double_wheel_case(9), double_wheel_case(10)):
            for caps in (dict(cycle_max_cycles=0), dict(cycle_max_scan_steps=0)):
                with self.subTest(case=case["name"], caps=caps):
                    result = self.solve(case["graph"], **caps)
                    oracle = create_oracle(case)
                    self.assertEqual(result["status"], "colored" if oracle.solution_count else "unsatisfiable")
                    self.assertEqual(result["stats"]["cycle_queries"], 0)
                    self.assertTrue(result["cycle_scan"]["truncated"])
                    self.assertFalse(result["cycle_scan"]["all_cycles_complete"])
                    if oracle.solution_count:
                        self.assert_witness(case["graph"], result)

    def test_query_budget_interrupts_before_any_partial_domain_commit(self):
        graph = escape_ring()
        full = self.solve(graph, use_substructures=False)
        query = next(event for event in full["events"]
                     if event["kind"] == "cycle_query"
                     and event["domain_masks"] != event["supported_domain_masks"])
        # Stop one charged operation before this successful pure query returns.
        cap = query["stats"]["checks"] - 1
        limited = self.solve(graph, use_substructures=False, max_checks=cap)
        self.assertEqual(limited["status"], "limit")
        self.assertEqual(limited["stats"]["checks"], cap)
        last = limited["events"][-1]
        by_vertex = dict(zip(graph["vertices"], last["domains"]))
        actual = [sum(1 << colour for colour in by_vertex[vertex]) for vertex in query["frontier"]]
        self.assertEqual(actual, query["domain_masks"])
        self.assertFalse(any(event["phase"] == "writeback" for event in limited["events"]))
        self.assert_delayed_writeback(graph, limited)
        zero = self.solve(graph, max_checks=0)
        self.assertEqual(zero["status"], "limit")
        self.assertEqual(zero["stats"]["checks"], 0)
        self.assert_delayed_writeback(graph, zero)

    def test_interrupted_discovery_reports_incomplete_metadata_and_charged_steps(self):
        graph = {"vertices": list(range(5)),
                 "edges": [[vertex, (vertex + 1) % 5] for vertex in range(5)]}
        full = self.solve(graph)
        first_query = next(event for event in full["events"] if event["kind"] == "cycle_query")
        # Before the first query, cycle checks consist only of discovery and
        # pure DP work.  Allow exactly one discovery step after ordinary GAC.
        before_discovery = first_query["stats"]["checks"] - first_query["stats"]["cycle_checks"]
        limited = self.solve(graph, max_checks=before_discovery + 1)
        self.assertEqual(limited["status"], "limit")
        self.assertEqual(limited["stats"]["cycle_queries"], 0)
        self.assertEqual(limited["stats"]["cycle_scan_steps"], 1)
        self.assertEqual(limited["cycle_scan"]["scan_steps"], 1)
        self.assertTrue(limited["cycle_scan"]["truncated"])
        self.assertFalse(limited["cycle_scan"]["last_discovery_complete"])
        self.assertTrue(limited["cycle_scan"]["last_discovery_interrupted"])
        self.assertFalse(full["cycle_scan"]["last_discovery_interrupted"])
        self.assertEqual(limited["stats"]["eliminations"], 0)
        self.assertFalse(any(event["phase"] == "writeback" for event in limited["events"]))
        self.assert_delayed_writeback(graph, limited)

    def test_real_python_decimal_digit_limit_returns_an_inconclusive_result(self):
        graph = {"vertices": list(range(1400)),
                 "edges": [[vertex, (vertex + 1) % 1400] for vertex in range(1400)]}
        previous_limit = sys.get_int_max_str_digits()
        try:
            sys.set_int_max_str_digits(640)
            # The actual exact count 3**1400 + 3 has 668 decimal digits.
            # No fabricated count or patched arithmetic exercises this path.
            result = self.solve(graph, max_checks=1_000_000)
        finally:
            sys.set_int_max_str_digits(previous_limit)
        self.assertEqual(sys.get_int_max_str_digits(), previous_limit)
        self.assertEqual(result["status"], "limit")
        self.assertEqual(result["stats"]["cycle_queries"], 1)
        self.assertEqual(result["stats"]["cycle_prunes"], 0)
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertEqual(result["events"][-1]["domains"], [[0, 1, 2, 3]] * 1400)
        self.assertIn("十進位", result["events"][-1]["detail"])
        self.assertFalse(any(event["phase"] == "writeback" for event in result["events"]))
        self.assert_delayed_writeback(graph, result)

    def test_decimal_conversion_failure_cannot_commit_a_real_cycle_prune(self):
        import four_color_local_information

        graph = escape_ring()
        original_derive = four_color_local_information.derive_cycle
        attempted = []

        class DecimalConversionLimit(int):
            def __str__(self):
                raise ValueError("injected Python decimal conversion limit")

        def derive_with_conversion_limit(masks, *, charge=None):
            answer = original_derive(masks, charge=charge)
            if tuple(answer["supports"]) != tuple(masks):
                attempted.append((tuple(masks), tuple(answer["supports"])))
                # Keep the correct numeric count and all actual DP supports;
                # inject only the serialization failure at the commit boundary.
                answer["row_count"] = DecimalConversionLimit(answer["row_count"])
            return answer

        with patch.object(four_color_local_information, "derive_cycle",
                          side_effect=derive_with_conversion_limit):
            result = self.solve(graph, use_substructures=False)
        self.assertEqual(result["status"], "limit")
        self.assertEqual(len(attempted), 1)
        input_masks, supported_masks = attempted[0]
        self.assertNotEqual(input_masks, supported_masks)
        self.assertEqual(result["stats"]["cycle_prunes"], 0)
        self.assertEqual(result["stats"]["eliminations"], 0)
        # The actual cycle is recorded before its query begins.  Its candidate
        # domains must still equal the pre-query masks after conversion fails.
        ring = next(cycle for cycle in result["cycle_scan"]["cycles"]
                    if set(cycle) == set(range(5)))
        last_domains = dict(zip(graph["vertices"], result["events"][-1]["domains"]))
        retained_masks = tuple(sum(1 << colour for colour in last_domains[vertex]) for vertex in ring)
        self.assertEqual(retained_masks, input_masks)
        self.assertFalse(any(event["phase"] == "writeback" for event in result["events"]))
        self.assert_delayed_writeback(graph, result)

    def test_reordered_nonconsecutive_labels_keep_literal_columns_and_source_edges(self):
        graph = escape_ring()
        mapping = {0: 90, 1: -7, 2: 41, 3: 0, 4: 5, 5: -33, 6: 18}
        graph = {"vertices": [mapping[v] for v in (3, 6, 0, 2, 5, 4, 1)],
                 "edges": [[mapping[a], mapping[b]] for a, b in graph["edges"]],
                 "fixed": [[mapping[v], colour] for v, colour in graph["fixed"]]}
        before = deepcopy(graph)
        solutions = original_edge_solutions(graph)
        result = self.solve(graph)
        self.assert_witness(graph, result)
        self.assert_preserved(graph, solutions, result)
        original_edges = {frozenset(edge) for edge in graph["edges"]}
        for event in result["events"]:
            if event.get("relation_kind") == "cycle":
                ring = event["frontier"]
                self.assertEqual(len(ring), len(set(ring)))
                self.assertTrue(all(frozenset((ring[i], ring[(i + 1) % len(ring)])) in original_edges
                                    for i in range(len(ring))))
                self.assertTrue(all(frozenset(edge) in original_edges
                                    for edge in event["causal_edges"]))
        self.assertEqual(graph, before)

    def test_chords_and_escaping_attachments_remain_in_the_full_problem(self):
        # Bare-cycle support is nonempty in all these graphs.  The added chord
        # and fixed attachment can still remove extensions or make them empty.
        ring = {"vertices": list(range(6)),
                "edges": [[i, (i + 1) % 5] for i in range(5)] + [[0, 2], [0, 5]]}
        for fixed in ([], [[5, 3]], [[0, 0], [2, 0]], [[0, 1], [5, 1]]):
            graph = dict(ring, fixed=fixed)
            with self.subTest(fixed=fixed):
                solutions = original_edge_solutions(graph)
                result = self.solve(graph)
                self.assertEqual(result["status"], "colored" if solutions else "unsatisfiable")
                self.assert_preserved(graph, solutions, result)
                if solutions:
                    self.assert_witness(graph, result)

    def test_cli_enables_both_optional_propagators_and_round_trips_json(self):
        graph = escape_ring()
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "graph.json", Path(directory) / "result.json"
            source.write_text(json.dumps(graph))
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "four_color_lab.py"),
                 "solve", str(source), "--engine", "constraints",
                 "--cycles", "--intersections", "--no-conflicts", "--json", str(output)],
                capture_output=True, text=True, timeout=30)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(output.read_text())
            self.assertTrue(result["use_cycles"])
            self.assertTrue(result["use_intersections"])
            self.assertGreater(result["stats"]["cycle_prunes"], 0)
            self.assert_witness(graph, result)
            self.assertEqual(json.loads(completed.stdout)["colors"], result["colors"])


class OriginalCycleDiscoveryTests(unittest.TestCase):
    def test_callbacks_are_charged_before_work_and_never_mutate_source_inputs(self):
        graph = double_wheel_case(7)["graph"]
        masks = [3] * 7 + [4, 8]
        before = deepcopy((graph, masks))
        charges = []
        expected = find_original_cycles(graph, masks, charge=lambda: charges.append(None))
        self.assertTrue(expected["cycles"])
        self.assertEqual(len(charges), expected["scan_steps"])

        class Interrupted(Exception):
            pass

        for stop_at in (0, 1, len(charges) // 2, len(charges) - 1):
            used = 0

            def charge():
                nonlocal used
                if used == stop_at:
                    raise Interrupted
                used += 1

            with self.subTest(stop_at=stop_at):
                with self.assertRaises(Interrupted):
                    find_original_cycles(graph, masks, charge=charge)
                self.assertEqual((graph, masks), before)
        self.assertEqual(find_original_cycles(graph, masks), expected)

    def test_discovery_caps_preserve_actual_cycles_without_claiming_complete_enumeration(self):
        graph = double_wheel_case(7)["graph"]
        masks = [3] * 7 + [4, 8]
        original_edges = {frozenset(edge) for edge in graph["edges"]}
        for cycle_cap, step_cap in ((0, 200000), (128, 0), (1, 200000), (128, 7), (128, 200000)):
            with self.subTest(cycle_cap=cycle_cap, step_cap=step_cap):
                result = find_original_cycles(graph, masks, max_cycles=cycle_cap,
                                              max_scan_steps=step_cap)
                self.assertLessEqual(len(result["cycles"]), cycle_cap)
                self.assertLessEqual(result["scan_steps"], step_cap)
                self.assertFalse(result["all_cycles_complete"])
                self.assertEqual(len(result["cycles"]), len(set(result["cycles"])))
                for cycle in result["cycles"]:
                    self.assertGreaterEqual(len(cycle), 3)
                    self.assertEqual(len(cycle), len(set(cycle)))
                    self.assertTrue(all(frozenset((cycle[i], cycle[(i + 1) % len(cycle)])) in original_edges
                                        for i in range(len(cycle))))
                if cycle_cap == 0 or step_cap == 0:
                    self.assertEqual(result["cycles"], [])
                    self.assertEqual(result["scan_steps"], 0)
                    self.assertTrue(result["truncated"])


if __name__ == "__main__":
    unittest.main()
