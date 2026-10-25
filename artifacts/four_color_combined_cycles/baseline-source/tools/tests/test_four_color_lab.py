"""Independent coloring oracle and original-edge checks for the coloring lab."""
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import four_color_lab as lab


def complete(n):
    return {"vertices": list(range(n)),
            "edges": [list(edge) for edge in combinations(range(n), 2)]}


def brute_force_coloring(graph):
    """Enumerate literal assignments, without solver ordering or propagation."""
    vertices = graph["vertices"]
    positions = {vertex: i for i, vertex in enumerate(vertices)}
    fixed = dict(graph.get("fixed", []))
    choices = [(fixed[v],) if v in fixed else range(4) for v in vertices]
    for colors in product(*choices):
        if all(colors[positions[u]] != colors[positions[v]]
               for u, v in graph["edges"]):
            return colors
    return None


class FourColorLabTests(unittest.TestCase):
    def assert_coloring(self, graph, colors):
        self.assertEqual(len(colors), len(graph["vertices"]))
        assignment = dict(zip(graph["vertices"], colors))
        self.assertTrue(all(type(color) is int and 0 <= color < 4
                            for color in colors))
        for u, v in graph["edges"]:
            self.assertNotEqual(assignment[u], assignment[v], (u, v))
        for vertex, color in graph.get("fixed", []):
            self.assertEqual(assignment[vertex], color)

    def assert_oracle_agreement(self, graph, **options):
        answer = brute_force_coloring(graph)
        result = lab.solve(graph, **options)
        self.assertEqual(result["status"],
                         "colored" if answer is not None else "unsatisfiable")
        if answer is not None:
            self.assert_coloring(graph, result["colors"])
        return result

    def test_all_1024_labeled_five_vertex_graphs_against_exhaustive_oracle(self):
        possible_edges = list(combinations(range(5), 2))
        for mask in range(1 << len(possible_edges)):
            graph = {"vertices": list(range(5)),
                     "edges": [list(edge) for bit, edge in enumerate(possible_edges)
                               if mask & (1 << bit)]}
            for strategy, propagation in product(("natural", "dsatur"), (False, True)):
                with self.subTest(mask=mask, strategy=strategy, propagation=propagation):
                    self.assert_oracle_agreement(graph, strategy=strategy,
                                                 propagation=propagation, trace_limit=0)

    def test_fixed_assignments_against_exhaustive_oracle(self):
        graphs = [complete(4), complete(5),
                  {"vertices": [8, -3, 40, 12, 0],
                   "edges": [[8, -3], [-3, 40], [40, 12], [12, 0], [0, 8]]},
                  {"vertices": list(range(5)),
                   "edges": [[0, leaf] for leaf in range(1, 5)]}]
        for graph in graphs:
            first, second = graph["vertices"][:2]
            for colors in product(range(4), repeat=2):
                fixed_graph = deepcopy(graph)
                fixed_graph["fixed"] = list(map(list, zip((first, second), colors)))
                with self.subTest(graph=graph, fixed=fixed_graph["fixed"]):
                    self.assert_oracle_agreement(fixed_graph)

    def test_nonclique_obstruction_against_exhaustive_oracle(self):
        # Four originals, four independent twins, and an apex on the twins.
        # No five-vertex clique can account for this graph's obstruction.
        graph = {"vertices": list(range(9)),
                 "edges": [list(edge) for edge in combinations(range(4), 2)]
                          + [[u + 4, v] for u in range(4) for v in range(4)
                             if u != v]
                          + [[8, v] for v in range(4, 8)]}
        result = self.assert_oracle_agreement(graph)
        self.assertEqual(result["status"], "unsatisfiable")
        for vertex in graph["vertices"]:
            smaller = {"vertices": [v for v in graph["vertices"] if v != vertex],
                       "edges": [edge for edge in graph["edges"] if vertex not in edge]}
            with self.subTest(deleted_vertex=vertex):
                self.assert_oracle_agreement(smaller)

    def test_seeded_seven_vertex_graphs_with_fixed_colors(self):
        rng = random.Random(20261025)
        possible_edges = list(combinations(range(7), 2))
        for case in range(32):
            graph = {"vertices": list(range(7)),
                     "edges": [list(edge) for edge in possible_edges
                               if rng.random() < 0.7],
                     "fixed": [[0, rng.randrange(4)], [6, rng.randrange(4)]]}
            with self.subTest(case=case):
                self.assert_oracle_agreement(graph)

    def test_propagation_is_optional_and_preserves_exact_answers(self):
        for graph in (complete(4), complete(5),
                      {"vertices": list(range(5)),
                       "edges": [[0, leaf] for leaf in range(1, 5)],
                       "fixed": [[1, 0], [2, 1], [3, 2], [4, 3]]}):
            with self.subTest(graph=graph):
                self.assert_oracle_agreement(graph, propagation=False)

    def test_empty_disconnected_and_nonconsecutive_vertex_labels(self):
        self.assert_oracle_agreement({"vertices": [], "edges": []})
        self.assert_oracle_agreement({"vertices": [99, -20, 4, 0, 7],
                                      "edges": [[99, -20], [4, 7]],
                                      "fixed": [[99, 3], [0, 1]]})

    def test_input_is_not_mutated_and_trace_is_deterministic(self):
        graph = complete(5)
        before = deepcopy(graph)
        first = lab.solve(graph)
        second = lab.solve(graph)
        self.assertEqual(first, second)
        self.assertEqual(graph, before)

    def test_search_limit_and_disabled_backtracking_are_not_unsat_proofs(self):
        graph = complete(5)
        self.assertEqual(lab.solve(graph, max_steps=1)["status"], "limit")
        self.assertEqual(lab.solve(graph, backtracking=False)["status"], "stuck")
        self.assertEqual(lab.solve(graph)["status"], "unsatisfiable")

    def test_bad_greedy_history_on_a_tree_is_repaired_by_backtracking(self):
        vertices, edges = [], []

        def grow(level):
            children = [grow(k) for k in range(1, level)]
            root = len(vertices)
            vertices.append(root)
            edges.extend([[root, child] for child in children])
            return root

        grow(5)
        graph = {"vertices": vertices, "edges": edges}
        greedy = lab.solve(graph, strategy="natural", propagation=False,
                           backtracking=False)
        self.assertEqual(greedy["status"], "stuck")
        repaired = lab.solve(graph, strategy="natural", propagation=False)
        self.assertEqual(repaired["status"], "colored")
        self.assertGreater(repaired["stats"]["backtracks"], 0)
        self.assert_coloring(graph, repaired["colors"])
        propagated = lab.solve(graph, strategy="natural", propagation=True,
                               backtracking=False)
        self.assertEqual(propagated["status"], "colored")
        self.assert_coloring(graph, propagated["colors"])

    def test_trace_limit_does_not_limit_search(self):
        graph = complete(5)
        full = lab.solve(graph)
        short = lab.solve(graph, trace_limit=2)
        self.assertEqual(short["status"], full["status"])
        self.assertEqual(short["stats"], full["stats"])
        self.assertLessEqual(len(short["events"]), 2)
        self.assertTrue(short["trace_truncated"])

    def test_four_blocker_star_is_an_original_edge_conflict(self):
        graph = {"vertices": [11, 21, 31, 41, 51],
                 "edges": [[11, leaf] for leaf in (21, 31, 41, 51)],
                 "fixed": [[21, 0], [31, 1], [41, 2], [51, 3]]}
        result = self.assert_oracle_agreement(graph)
        conflicts = [event for event in result["events"]
                     if event["kind"] == "conflict"]
        self.assertTrue(conflicts)
        conflict = conflicts[0]
        self.assertEqual(conflict["vertex"], 11)
        self.assertEqual({blocker["color"] for blocker in conflict["blockers"]},
                         set(range(4)))
        self.assertEqual({blocker["vertex"] for blocker in conflict["blockers"]},
                         {21, 31, 41, 51})
        self.assertEqual({frozenset(edge) for edge in conflict["conflict_edges"]},
                         {frozenset(edge) for edge in graph["edges"]})
        # The same planar star is easily colorable when the boundary is free.
        free_graph = {key: value for key, value in graph.items() if key != "fixed"}
        self.assert_oracle_agreement(free_graph)

    def test_trace_assignments_and_highlighted_edges_stay_on_original_graph(self):
        graph = complete(5)
        result = lab.solve(graph)
        vertices = graph["vertices"]
        edges = {frozenset(edge) for edge in graph["edges"]}
        self.assertGreater(result["stats"]["conflicts"], 0)
        self.assertGreater(result["stats"]["backtracks"], 0)
        for event in result["events"]:
            assignment = dict(zip(vertices, event["colors"]))
            self.assertEqual(len(event["colors"]), len(vertices))
            self.assertEqual(len(event["domains"]), len(vertices))
            for vertex, domain in zip(vertices, event["domains"]):
                forbidden = {assignment[next(iter(edge - {vertex}))]
                             for edge in edges if vertex in edge}
                expected = ([assignment[vertex]] if assignment[vertex] >= 0 else
                            [color for color in range(4) if color not in forbidden])
                self.assertEqual(domain, expected)
            for u, v in graph["edges"]:
                if assignment[u] != -1 and assignment[v] != -1:
                    self.assertNotEqual(assignment[u], assignment[v], event)
            for key in ("causal_edges", "conflict_edges"):
                self.assertTrue(all(frozenset(edge) in edges for edge in event[key]),
                                (key, event))
            self.assertTrue(set(event["causal_vertices"]) <= set(vertices))
            for blocker in event["blockers"]:
                self.assertEqual(assignment[blocker["vertex"]], blocker["color"])
                self.assertIn(frozenset((event["vertex"], blocker["vertex"])), edges)

    def test_malformed_graphs_and_fixed_colors_are_rejected(self):
        invalid = [
            {"vertices": [0, 0], "edges": []},
            {"vertices": [True], "edges": []},
            {"vertices": [0.0], "edges": []},
            {"vertices": [0], "edges": [[0, 0]]},
            {"vertices": [0], "edges": [[0, 1]]},
            {"vertices": [0, 1], "edges": [[0]]},
            {"vertices": [0, 1], "edges": [[0, 1], [1, 0]]},
            {"vertices": [0], "edges": [], "fixed": [[0, 4]]},
            {"vertices": [0], "edges": [], "fixed": [[0, -1]]},
            {"vertices": [0], "edges": [], "fixed": [[0, True]]},
            {"vertices": [0], "edges": [], "fixed": [[1, 0]]},
            {"vertices": [0], "edges": [], "fixed": [[0, 0], [0, 1]]},
        ]
        for graph in invalid:
            with self.subTest(graph=graph), self.assertRaises(ValueError):
                lab.solve(graph)


if __name__ == "__main__":
    unittest.main()
