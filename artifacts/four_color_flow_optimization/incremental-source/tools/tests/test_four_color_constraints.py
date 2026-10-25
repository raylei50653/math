"""Truth-table and witness tests for elimination-based four-color constraints."""
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import four_color_constraints as constraints
import four_color_lab as search


def complete(n):
    return {"vertices": list(range(n)),
            "edges": [list(edge) for edge in combinations(range(n), 2)]}


def literal_colorings(graph, vertices=None, edges=None):
    """Enumerate full assignments directly from edges, without constraint code."""
    vertices = graph["vertices"] if vertices is None else vertices
    edges = graph["edges"] if edges is None else edges
    fixed = dict(graph.get("fixed", []))
    domains = [(fixed[v],) if v in fixed else range(4) for v in vertices]
    for row in product(*domains):
        assignment = dict(zip(vertices, row))
        if all(assignment[u] != assignment[v] for u, v in edges):
            yield assignment


class FourColorConstraintTests(unittest.TestCase):
    def assert_valid_witness(self, graph, colors):
        self.assertEqual(len(colors), len(graph["vertices"]))
        self.assertTrue(all(type(c) is int and 0 <= c < 4 for c in colors))
        assignment = dict(zip(graph["vertices"], colors))
        self.assertTrue(all(assignment[u] != assignment[v]
                            for u, v in graph["edges"]))
        self.assertTrue(all(assignment[v] == c for v, c in graph.get("fixed", [])))

    def assert_agreement(self, graph, **options):
        exists = next(literal_colorings(graph), None) is not None
        result = constraints.solve_constraints(graph, **options)
        self.assertEqual(result["engine"], "constraints")
        self.assertEqual(result["status"], "colored" if exists else "unsatisfiable")
        if exists:
            self.assert_valid_witness(graph, result["colors"])
        return result

    def test_all_1024_five_vertex_graphs_with_and_without_substructures(self):
        possible = list(combinations(range(5), 2))
        for mask in range(1 << len(possible)):
            graph = {"vertices": list(range(5)),
                     "edges": [list(edge) for i, edge in enumerate(possible)
                               if mask & (1 << i)]}
            for use_substructures in (False, True):
                with self.subTest(mask=mask, substructures=use_substructures):
                    self.assert_agreement(graph, use_substructures=use_substructures,
                                          trace_limit=0, record_relations=False)

    def test_literal_fixed_boundaries_against_independent_oracle(self):
        graphs = [complete(4), complete(5),
                  {"vertices": [30, -4, 8, 15, 2],
                   "edges": [[30, -4], [-4, 8], [8, 15], [15, 2], [2, 30]]}]
        for graph in graphs:
            for colors in product(range(4), repeat=2):
                case = deepcopy(graph)
                case["fixed"] = [list(pair) for pair in zip(case["vertices"][:2], colors)]
                for motifs in (False, True):
                    with self.subTest(graph=graph, fixed=case["fixed"], motifs=motifs):
                        self.assert_agreement(case, use_substructures=motifs)

    def test_empty_disconnected_isolated_and_nonconsecutive_labels(self):
        for graph in ({"vertices": [], "edges": []},
                      {"vertices": [90, -5, 17], "edges": []},
                      {"vertices": [90, -5, 17, 33, 0],
                       "edges": [[90, -5], [33, 0]], "fixed": [[17, 3]]}):
            with self.subTest(graph=graph):
                self.assert_agreement(graph)

    def test_k5_is_rejected_before_any_unknown_vertex_is_colored(self):
        for motifs in (False, True):
            result = self.assert_agreement(complete(5), use_substructures=motifs)
            self.assertEqual(result["status"], "unsatisfiable")
            self.assertTrue(all(color == -1 for color in result["colors"]))
            self.assertTrue(all(color == -1 for event in result["events"]
                                for color in event["colors"]))
            self.assertFalse(any(event["phase"] == "writeback"
                                 for event in result["events"]))

    def test_nonclique_obstruction_needs_joint_relations_beyond_a_k5_check(self):
        graph = {"vertices": list(range(9)),
                 "edges": [list(edge) for edge in combinations(range(4), 2)]
                          + [[u + 4, v] for u in range(4) for v in range(4)
                             if u != v]
                          + [[8, v] for v in range(4, 8)]}
        for motifs in (False, True):
            with self.subTest(motifs=motifs):
                result = self.assert_agreement(graph, use_substructures=motifs)
                self.assertEqual(result["status"], "unsatisfiable")
                self.assertEqual(result["colors"], [-1] * 9)
                self.assertGreater(result["stats"]["eliminations"], 0)
                self.assertEqual(result["stats"]["writebacks"], 0)
        # Removing the apex leaves a compatible complete witness to rebuild.
        smaller = {"vertices": list(range(8)),
                   "edges": [edge for edge in graph["edges"] if 8 not in edge]}
        self.assert_agreement(smaller)

    def test_joint_triangle_relation_detects_more_than_unary_domains(self):
        # The three triangle vertices all have the same nonempty domain {0,1}.
        # Their joint original-edge relation is nevertheless empty.
        graph = {"vertices": [0, 1, 2, 3, 4],
                 "edges": [[0, 1], [1, 2], [0, 2]]
                          + [[u, v] for u in (0, 1, 2) for v in (3, 4)],
                 "fixed": [[3, 2], [4, 3]]}
        for motifs in (False, True):
            result = self.assert_agreement(graph, use_substructures=motifs)
            self.assertEqual(result["status"], "unsatisfiable")
            for event in result["events"]:
                self.assertEqual(event["colors"][:3], [-1, -1, -1])
                self.assertEqual(event["colors"][3:], [2, 3])

    def test_writeback_chooses_one_compatible_witness_after_full_reduction(self):
        graph = complete(4)
        graph["fixed"] = [[0, 2]]
        result = self.assert_agreement(graph)
        fixed = dict(graph["fixed"])
        records = {record["vertex"]: record for record in result["elimination_records"]}
        previous = dict(fixed)
        for event in result["events"]:
            current = dict(zip(graph["vertices"], event["colors"]))
            for vertex, color in fixed.items():
                self.assertEqual(current[vertex], color)
            if event["phase"] == "reduce":
                self.assertEqual(current, {v: fixed.get(v, -1) for v in graph["vertices"]})
            for vertex, color in current.items():
                if color < 0 or vertex in previous:
                    continue
                self.assertIn(event["phase"], ("writeback", "done"))
                self.assertEqual(set(event["eliminated_vertices"]), set(graph["vertices"]))
                record = records[vertex]
                self.assertTrue(all(current[v] >= 0 for v in record["scope"]))
                boundary = [current[v] for v in record["scope"]]
                matches = [row for row in record["rows"] if row["boundary"] == boundary]
                self.assertEqual(len(matches), 1)
                self.assertIn(color, matches[0]["colors"])
            for vertex, color in previous.items():
                self.assertEqual(current[vertex], color)
            previous = {v: c for v, c in current.items() if c >= 0}

    def test_elimination_relations_equal_joint_inputs_and_preserve_global_colorings(self):
        graphs = [complete(4),
                  {"vertices": [7, 11, 2, 40, -3],
                   "edges": [[7, 11], [11, 2], [2, 40], [40, -3], [-3, 7]],
                   "fixed": [[7, 3]]}]
        for graph, motifs in product(graphs, (False, True)):
            result = self.assert_agreement(graph, use_substructures=motifs)
            original_edges = {frozenset(edge) for edge in graph["edges"]}
            for record in result["elimination_records"]:
                with self.subTest(graph=graph, motifs=motifs, vertex=record["vertex"]):
                    scope = record["scope"]
                    self.assertNotIn(record["vertex"], scope)
                    self.assertEqual(len(scope), len(set(scope)))
                    self.assertTrue(set(scope) <= set(graph["vertices"]))
                    source = record["source_vertices"]
                    self.assertTrue(set(source) <= set(graph["vertices"]))
                    self.assertTrue({record["vertex"], *scope} <= set(source))
                    self.assertTrue(all(frozenset(edge) in original_edges
                                        for edge in record["source_edges"]))
                    # GAC domains can depend on factors outside this bucket.
                    # Verify the literal complete input relations and domains,
                    # not an unsupported isolated-subgraph interpretation.
                    domains = {entry["vertex"]: entry["colors"]
                               for entry in record["source_domains"]}
                    bucket_vertices = [record["vertex"], *scope]
                    self.assertEqual(set(domains), set(bucket_vertices))
                    inputs = []
                    for relation in record["input_relations"]:
                        self.assertTrue(set(relation["scope"]) <= set(bucket_vertices))
                        self.assertTrue(all(frozenset(edge) in original_edges
                                            for edge in relation["source_edges"]))
                        rows = {tuple(row) for row in relation["rows"]}
                        self.assertEqual(len(rows), len(relation["rows"]))
                        self.assertTrue(all(len(row) == len(relation["scope"])
                                            for row in rows))
                        inputs.append((relation["scope"], rows))
                    expected = {}
                    for colors in product(*(domains[v] for v in bucket_vertices)):
                        coloring = dict(zip(bucket_vertices, colors))
                        if all(tuple(coloring[v] for v in columns) in rows
                               for columns, rows in inputs):
                            boundary = tuple(coloring[v] for v in scope)
                            expected.setdefault(boundary, set()).add(coloring[record["vertex"]])
                    actual = {tuple(row["boundary"]): set(row["colors"])
                              for row in record["rows"]}
                    self.assertEqual(len(actual), len(record["rows"]))
                    self.assertEqual(actual, expected)
                    # A complete legal original-graph coloring must survive
                    # every domain restriction and every saved projection.
                    for coloring in literal_colorings(graph):
                        self.assertTrue(all(coloring[v] in domains[v] for v in domains))
                        self.assertIn(coloring[record["vertex"]],
                                      actual[tuple(coloring[v] for v in scope)])

    def test_limits_do_not_turn_incomplete_reduction_into_a_verdict(self):
        graph = complete(4)
        result = constraints.solve_constraints(graph, max_checks=0)
        self.assertEqual(result["status"], "limit")
        self.assertEqual(result["colors"], [-1] * 4)
        self.assertFalse(any(event["phase"] == "writeback" for event in result["events"]))

    def test_trace_truncation_does_not_change_result_or_work(self):
        graph = complete(4)
        full = constraints.solve_constraints(graph)
        short = constraints.solve_constraints(graph, trace_limit=1)
        self.assertEqual(short["status"], full["status"])
        self.assertEqual(short["colors"], full["colors"])
        self.assertEqual(short["stats"], full["stats"])
        self.assertLessEqual(len(short["events"]), 1)
        self.assertTrue(short["trace_truncated"])

    def test_templates_reuse_without_input_mutation_or_cross_run_corruption(self):
        graph = complete(4)
        before = deepcopy(graph)
        first = constraints.solve_constraints(graph)
        preserved_first = deepcopy(first)
        contradictory = complete(4)
        contradictory["fixed"] = [[0, 0], [1, 0]]
        self.assert_agreement(contradictory)
        self.assert_agreement(complete(5))
        second = constraints.solve_constraints(graph)
        self.assertEqual(first, preserved_first)
        self.assertEqual(first["status"], second["status"])
        self.assertEqual(first["colors"], second["colors"])
        self.assertEqual(first["elimination_records"], second["elimination_records"])
        self.assertEqual(graph, before)

    def test_valid_results_agree_with_search_engine_without_requiring_same_colors(self):
        for graph in (complete(4), complete(5),
                      {"vertices": [1, 20, -3, 4],
                       "edges": [[1, 20], [20, -3], [-3, 4]], "fixed": [[1, 3]]}):
            result = self.assert_agreement(graph)
            other = search.solve(graph)
            self.assertEqual(result["status"], other["status"])
            if result["status"] == "colored":
                self.assert_valid_witness(graph, other["colors"])


if __name__ == "__main__":
    unittest.main()
