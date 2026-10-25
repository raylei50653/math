"""Partial original spokes close the frozen nine-point propagation gap.

The reference solutions come from literal original edges, independently of the
cycle queries and the solver's derived interfaces.
"""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_conflict_priority import original_solutions, verify_preservation
from four_color_constraints import solve_constraints
from four_color_cycle_contexts import derive_cycle_context


def nine_point_graph():
    cases = json.loads((ROOT / "artifacts/four_color_guarantee_gap/inputs.json").read_text())
    return deepcopy(next(case["graph"] for case in cases if case["role"] == "secondary-gap"))


class PartialSpokePropagationTests(unittest.TestCase):
    def solve(self, graph, **options):
        settings = dict(use_intersections=True, use_cycles=True,
                        use_cycle_contexts=True, cycle_context_search="partial",
                        use_conflicts=False, use_c5=False, record_relations=True,
                        trace_limit=10000, max_checks=5_000_000)
        settings.update(options)
        return solve_constraints(graph, **settings)

    def assert_no_early_colours(self, graph, result):
        fixed = dict(graph.get("fixed", []))
        expected = [fixed.get(vertex, -1) for vertex in graph["vertices"]]
        for event in result["events"]:
            if event["phase"] == "reduce":
                self.assertEqual(event["colors"], expected)
        self.assertEqual(result["stats"]["decisions"], 0)
        self.assertEqual(result["stats"]["backtracks"], 0)

    def test_frozen_nine_point_gap_closes_before_any_elimination(self):
        graph = nine_point_graph()
        before = deepcopy(graph)
        self.assertEqual(list(original_solutions(graph)), [])
        historical = self.solve(graph, cycle_context_search="neighbours")
        self.assertEqual(historical["status"], "unsatisfiable")
        self.assertEqual(historical["stats"]["eliminations"], 4)

        result = self.solve(graph)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertEqual(result["graph_sha256"], historical["graph_sha256"])
        self.assertFalse(result["trace_truncated"])
        self.assertEqual(result["elimination_records"], [])
        self.assertGreater(result["stats"]["cycle_context_factors"], 0)
        self.assertGreater(result["stats"]["intersection_prunes"], 0)
        # This is interface feedback: no individual context needs to be empty
        # and the new context queries need not remove a unary candidate.
        self.assertEqual(result["stats"]["cycle_context_conflicts"], 0)
        self.assertEqual(result["stats"]["cycle_context_prunes"], 0)
        self.assertTrue(any(event["kind"] == "conflict" for event in result["events"]))
        original = {frozenset(edge) for edge in graph["edges"]}
        partial_queries = []
        for event in result["events"]:
            if event.get("relation_kind") != "cycle_context":
                continue
            hub, cycle = event["context_vertex"], event["cycle_vertices"]
            self.assertNotIn(hub, cycle)
            self.assertEqual(len(cycle), len(set(cycle)))
            self.assertTrue(all(frozenset((cycle[index], cycle[(index + 1) % len(cycle)]))
                                in original for index in range(len(cycle))))
            self.assertTrue(all(frozenset(edge) in original for edge in event["causal_edges"]))
            if any(frozenset((hub, vertex)) not in original for vertex in cycle):
                partial_queries.append(event)
        self.assertTrue(partial_queries)
        self.assert_no_early_colours(graph, result)
        self.assertEqual(graph, before)

    def test_noncontiguous_relabeling_does_not_depend_on_named_vertex_ids(self):
        graph = nine_point_graph()
        labels = dict(zip(graph["vertices"], [41, -200, 901, 17, 302, -7, 83, 10003, -413]))
        renamed = dict(vertices=[labels[vertex] for vertex in graph["vertices"]],
                       edges=[[labels[left], labels[right]] for left, right in graph["edges"]],
                       fixed=[[labels[vertex], colour] for vertex, colour in graph["fixed"]])
        result = self.solve(renamed)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertEqual(set(result["graph"]["vertices"]), set(labels.values()))
        self.assert_no_early_colours(renamed, result)

    def test_unfixed_graph_preserves_all_48_literal_original_solutions(self):
        graph = nine_point_graph()
        graph["fixed"] = []
        solutions = list(original_solutions(graph))
        self.assertEqual(len(solutions), 48)
        positions = {vertex: index for index, vertex in enumerate(graph["vertices"])}
        self.assertTrue(all(row[positions[0]] == row[positions[6]] for row in solutions))
        result = self.solve(graph)
        self.assertEqual(result["status"], "colored")
        audit = verify_preservation(graph, solutions, result)
        self.assertTrue(audit["all_solutions_preserved"])
        self.assertTrue(audit["witness_verified"])
        # Also check every recorded exported relation directly, including ones
        # later subsumed by another complete factor.
        for event in result["events"]:
            if event.get("relation_kind") != "cycle_context":
                continue
            for field in ("pair_relations", "cycle_edge_relations", "context_edge_relations"):
                for relation in event[field]:
                    allowed = {tuple(row) for row in relation["rows"]}
                    offsets = [positions[vertex] for vertex in relation["scope"]]
                    for solution in solutions:
                        self.assertIn(tuple(solution[offset] for offset in offsets), allowed)
        self.assert_no_early_colours(graph, result)

    def test_three_partial_contexts_expose_the_missing_common_condition(self):
        graph = nine_point_graph()
        # These are the frozen pre-elimination domains, not an assignment of
        # the still-unknown colours of vertices 1 or 5.
        domains = [[0], [1, 2], [1, 2, 3], [0, 1, 2], [1, 2],
                   [3], [0, 1, 2], [1, 2, 3], [1, 2]]
        masks = [sum(1 << colour for colour in domain) for domain in domains]
        first = derive_cycle_context(graph, [0, 1, 4, 7, 5], 8, masks)
        second = derive_cycle_context(graph, [0, 1, 4, 9, 7, 5], 8, masks)
        third = derive_cycle_context(graph, [1, 5, 6], 8, masks)

        def rows(answer, field, scope):
            return {tuple(row) for relation in answer[field]
                    if relation["scope"] == scope for row in relation["rows"]}

        shared = (rows(first, "context_edge_relations", [8, 1, 4])
                  & rows(second, "context_edge_relations", [8, 1, 4]))
        pair = rows(third, "pair_relations", [8, 1])
        self.assertEqual({row for row in shared if row[0] == 1}, {(1, 2, 1)})
        self.assertEqual({row for row in shared if row[0] == 2}, {(2, 1, 2)})
        self.assertEqual({row for row in pair if row[0] in (1, 2)}, {(1, 1), (2, 2)})
        compatible = {row for row in shared if row[:2] in pair}
        self.assertEqual({row[0] for row in compatible}, {3})
        self.assertTrue(all(answer["row_count"] > 0 for answer in (first, second, third)))

    def test_zero_partial_search_caps_keep_the_exact_elimination_fallback(self):
        graph = nine_point_graph()
        for cap in (dict(cycle_context_max_contexts=0), dict(cycle_context_max_scan_steps=0)):
            with self.subTest(cap=cap):
                result = self.solve(graph, **cap)
                self.assertEqual(result["status"], "unsatisfiable")
                self.assertEqual(result["stats"]["cycle_context_queries"], 0)
                self.assertEqual(result["stats"]["eliminations"], 4)
                self.assertTrue(result["cycle_context_scan"]["truncated"])
                self.assert_no_early_colours(graph, result)

    def test_partial_search_rejects_invalid_or_inactive_options(self):
        graph = nine_point_graph()
        for option in ("unknown", None, True, 1):
            with self.subTest(option=option):
                with self.assertRaises(ValueError):
                    self.solve(graph, cycle_context_search=option)
        with self.assertRaises(ValueError):
            self.solve(graph, use_cycle_contexts=False)

    def test_cli_can_select_partial_spokes(self):
        with TemporaryDirectory() as directory:
            source, output = Path(directory) / "graph.json", Path(directory) / "result.json"
            source.write_text(json.dumps(nine_point_graph()))
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts/four_color_lab.py"), "solve", str(source),
                 "--engine", "constraints", "--intersections", "--cycles", "--cycle-contexts",
                 "--cycle-context-search", "partial", "--no-conflicts", "--json", str(output)],
                capture_output=True, text=True, timeout=30)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(output.read_text())
            self.assertEqual(result["status"], "unsatisfiable")
            self.assertEqual(result["stats"]["eliminations"], 0)
            self.assertEqual(json.loads(completed.stdout)["status"], result["status"])


if __name__ == "__main__":
    unittest.main()
