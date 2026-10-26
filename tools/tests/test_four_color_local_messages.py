"""Independent correctness and disclosure checks for lazy separator messages."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_local_messages import solve_local_messages as _solve_local_messages


def solve_local_messages(*args, **kwargs):
    """Tests opt into private audit metadata to check every local obligation."""
    kwargs.setdefault("audit_metadata", True)
    return _solve_local_messages(*args, **kwargs)


def original_solutions(graph, domains=None, *, first_only=False):
    """Original-edge DFS oracle, independent of bags, fill edges and messages."""
    domains = {} if domains is None else domains
    vertices = list(graph["vertices"])
    allowed = {v: set(domains.get(v, range(4))) for v in vertices}
    for vertex, colour in graph.get("fixed", []):
        allowed[vertex].intersection_update({colour})
    neighbors = {v: set() for v in vertices}
    for left, right in graph["edges"]:
        neighbors[left].add(right)
        neighbors[right].add(left)
    positions = {v: index for index, v in enumerate(vertices)}
    order = sorted(vertices, key=lambda v: (len(allowed[v]), -len(neighbors[v]), positions[v]))
    assignment = {}
    answers = []

    def visit(index):
        if index == len(order):
            answers.append(dict(assignment))
            return first_only
        vertex = order[index]
        for colour in sorted(allowed[vertex]):
            if any(assignment.get(other) == colour for other in neighbors[vertex]):
                continue
            assignment[vertex] = colour
            if visit(index + 1):
                return True
        assignment.pop(vertex, None)
        return False

    visit(0)
    return answers


def cycle(n):
    return {"vertices": list(range(n)),
            "edges": [[i, (i + 1) % n] for i in range(n)], "fixed": []}


class LocalMessageTests(unittest.TestCase):
    def check_coloring(self, graph, result, domains=None):
        self.assertEqual(result["status"], "colored")
        colors = result["colors"]
        self.assertEqual(len(colors), len(graph["vertices"]))
        self.assertTrue(all(type(c) is int and 0 <= c < 4 for c in colors))
        assignment = dict(zip(graph["vertices"], colors))
        self.assertTrue(all(assignment[u] != assignment[v] for u, v in graph["edges"]))
        self.assertTrue(all(assignment[v] == c for v, c in graph.get("fixed", [])))
        if domains is not None:
            self.assertTrue(all(assignment[v] in colors for v, colors in domains.items()))

    def check_decomposition(self, graph, result):
        decomposition = result["decomposition"]
        self.assertTrue(decomposition["validated"])
        bags = {bag["id"]: bag for bag in decomposition["bags"]}
        self.assertEqual(set(decomposition["order"]), set(graph["vertices"]))
        self.assertEqual(len(bags), len(graph["vertices"]))
        self.assertEqual(set(decomposition["roots"]),
                         {index for index, bag in bags.items() if bag["parent"] is None})
        owned = []
        for index, bag in bags.items():
            self.assertEqual(set(bag["vertices"]), {bag["vertex"], *bag["separator"]})
            self.assertNotIn(bag["vertex"], bag["separator"])
            parent = bag["parent"]
            if parent is not None:
                self.assertIn(index, bags[parent]["children"])
                self.assertEqual(set(bag["separator"]),
                                 set(bag["vertices"]) & set(bags[parent]["vertices"]))
            else:
                self.assertEqual(bag["separator"], [])
            for u, v in bag["local_edges"]:
                self.assertIn(u, bag["vertices"])
                self.assertIn(v, bag["vertices"])
                owned.append(frozenset((u, v)))
        self.assertCountEqual(owned, [frozenset(edge) for edge in graph["edges"]])
        for vertex in graph["vertices"]:
            containing = {index for index, bag in bags.items() if vertex in bag["vertices"]}
            reached = set()
            pending = [next(iter(containing))]
            while pending:
                current = pending.pop()
                if current in reached:
                    continue
                reached.add(current)
                adjacent = [*bags[current]["children"], bags[current]["parent"]]
                pending.extend(i for i in adjacent if i in containing and i not in reached)
            self.assertEqual(reached, containing)

    def check_messages(self, graph, result, domains=None, *, semantic=True):
        """Every response has an independent subtree existential interpretation."""
        bags = {bag["id"]: bag for bag in result["decomposition"]["bags"]}
        queries = {}
        allowed_fields = {"kind", "query_id", "bag", "sender", "receiver", "separator", "colors"}
        base_domains = {v: set((domains or {}).get(v, range(4))) for v in graph["vertices"]}
        for vertex, colour in graph.get("fixed", []):
            base_domains[vertex].intersection_update({colour})
        for event in result["transcript"]:
            self.assertIn(event["kind"], ("query", "reply"))
            expected = allowed_fields | ({"possible", "cached"} if event["kind"] == "reply" else set())
            self.assertEqual(set(event), expected)
            bag = bags[event["bag"]]
            if event["kind"] == "query":
                self.assertEqual(event["sender"], bag["parent"])
                self.assertEqual(event["receiver"], bag["id"])
            else:
                self.assertEqual(event["sender"], bag["id"])
                self.assertEqual(event["receiver"], bag["parent"])
            self.assertEqual(event["separator"], bag["separator"])
            self.assertEqual(len(event["colors"]), len(bag["separator"]))
            self.assertNotIn(bag["vertex"], event["separator"])
            if event["kind"] == "query":
                self.assertNotIn(event["query_id"], queries)
                queries[event["query_id"]] = event
                continue
            query = queries[event["query_id"]]
            for field in ("bag", "separator", "colors"):
                self.assertEqual(event[field], query[field])
            self.assertIs(type(event["possible"]), bool)
            if not semantic:
                continue
            descendants = set()
            pending = [bag["id"]]
            while pending:
                current = pending.pop()
                descendants.add(current)
                pending.extend(bags[current]["children"])
            scope = set().union(*(set(bags[i]["vertices"]) for i in descendants))
            local_graph = {"vertices": [v for v in graph["vertices"] if v in scope],
                           "edges": [edge for i in descendants for edge in bags[i]["local_edges"]],
                           "fixed": list(zip(event["separator"], event["colors"]))}
            local_domains = {v: base_domains[v] for v in local_graph["vertices"]}
            possible = bool(original_solutions(local_graph, local_domains, first_only=True))
            self.assertEqual(event["possible"], possible)

    def test_two_hundred_small_graphs_against_original_edge_oracle(self):
        rng = random.Random(923761)
        for index in range(200):
            n = rng.randrange(8)
            vertices = list(range(n))
            rng.shuffle(vertices)
            graph = {"vertices": vertices,
                     "edges": [list(edge) for edge in combinations(vertices, 2)
                               if rng.random() < .39],
                     "fixed": [[v, rng.randrange(4)] for v in vertices if rng.random() < .19]}
            domains = {v: [c for c in range(4) if rng.random() < .73] for v in vertices}
            expected = bool(original_solutions(graph, domains, first_only=True))
            result = solve_local_messages(graph, domains=domains)
            with self.subTest(case=index):
                self.assertEqual(result["status"], "colored" if expected else "unsatisfiable")
                self.check_decomposition(graph, result)
                self.check_messages(graph, result, domains)
                if expected:
                    self.check_coloring(graph, result, domains)
                else:
                    self.assertIsNone(result["colors"])

    def test_fill_edges_are_not_added_as_colour_constraints(self):
        graph = cycle(4)
        domains = {v: [0, 1] for v in graph["vertices"]}
        result = solve_local_messages(graph, domains=domains)
        self.check_coloring(graph, result, domains)
        self.check_decomposition(graph, result)
        self.check_messages(graph, result, domains)
        self.assertEqual(len(original_solutions(graph, domains)), 2)

    def test_odd_cycle_local_supports_do_not_imply_global_solution(self):
        graph = cycle(5)
        domains = {v: [0, 1] for v in graph["vertices"]}
        result = solve_local_messages(graph, domains=domains)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertIsNone(result["colors"])
        self.check_messages(graph, result, domains)

    def test_k5_is_rejected_without_planarity_assumption(self):
        graph = {"vertices": list(range(5)), "edges": [list(e) for e in combinations(range(5), 2)]}
        result = solve_local_messages(graph)
        self.assertEqual(result["status"], "unsatisfiable")
        self.check_decomposition(graph, result)
        self.check_messages(graph, result)

    def test_fourteen_point_conditions_match_independent_counts(self):
        inputs = json.loads((ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f/"
                             "propagation/inputs.json").read_text())
        fixed = inputs["graph"]
        bare = dict(fixed, fixed=[])
        repaired = dict(fixed, edges=[edge for edge in fixed["edges"] if set(edge) != {7, 13}])
        for name, graph, count in (("fixed", fixed, 0), ("bare", bare, 624),
                                   ("edge_removed", repaired, 6)):
            with self.subTest(condition=name):
                answers = original_solutions(graph)
                self.assertEqual(len(answers), count)
                result = solve_local_messages(graph)
                self.assertEqual(result["status"], "colored" if count else "unsatisfiable")
                self.check_decomposition(graph, result)
                self.check_messages(graph, result, semantic=False)
                if count:
                    self.check_coloring(graph, result)
                    self.assertIn(dict(zip(graph["vertices"], result["colors"])), answers)

    def test_budgets_never_turn_incomplete_queries_into_negative_answers(self):
        graph = cycle(5)
        full = solve_local_messages(graph)
        self.check_coloring(graph, full)
        for name in ("max_checks", "max_messages", "max_cache_entries"):
            for cap in (0, 1, 2):
                with self.subTest(budget=name, cap=cap):
                    result = solve_local_messages(graph, **{name: cap})
                    self.assertEqual(result["status"], "limit")
                    self.assertIsNone(result["colors"])
                    if result["decomposition"] is not None and result["decomposition"]["validated"]:
                        self.check_messages(graph, result)

    def test_transcript_truncation_does_not_change_answer(self):
        graph = cycle(6)
        full = solve_local_messages(graph)
        for cap in (0, 1, 3):
            result = solve_local_messages(graph, transcript_limit=cap)
            self.assertEqual(result["status"], full["status"])
            self.assertEqual(result["colors"], full["colors"])
            self.assertLessEqual(len(result["transcript"]), cap)

    def test_default_output_omits_private_audit_fields(self):
        graph = cycle(6)
        normal = _solve_local_messages(graph)
        audit = solve_local_messages(graph)
        self.assertEqual(normal["status"], audit["status"])
        self.assertEqual(normal["colors"], audit["colors"])
        self.assertEqual(normal["transcript"], audit["transcript"])
        self.assertFalse(normal["eager_tables_built"])
        self.assertFalse(normal["cache_declared_complete"])
        self.assertNotIn("order", normal["decomposition"])
        for bag in normal["decomposition"]["bags"]:
            self.assertEqual(set(bag), {"id", "separator", "parent", "children", "bag_size"})

    def test_late_budget_exhaustion_does_not_publish_partial_writeback(self):
        graph = cycle(6)
        full = solve_local_messages(graph)
        for budget, count in (("max_checks", full["stats"]["checks"]),
                              ("max_messages", full["stats"]["messages"])):
            result = solve_local_messages(graph, **{budget: count - 1})
            self.assertEqual(result["status"], "limit")
            self.assertIsNone(result["colors"])
            self.check_messages(graph, result)

    def test_deep_tree_queries_and_writeback_do_not_use_python_recursion(self):
        n = 1050
        graph = {"vertices": list(range(n)), "edges": [[i, i + 1] for i in range(n - 1)]}
        result = solve_local_messages(graph, max_checks=3000000, transcript_limit=0)
        self.check_coloring(graph, result)
        self.assertGreater(result["stats"]["max_stack_depth"], 1000)
        self.assertEqual(result["stats"]["max_separator_size"], 1)

    def test_signed_huge_labels_permutation_and_no_input_mutation(self):
        graph = cycle(4)
        graph["fixed"] = [[0, 2]]
        labels = {0: 10 ** 4300, 1: -10 ** 4301, 2: -7, 3: 43}
        renamed = {"vertices": [labels[v] for v in (2, 0, 3, 1)],
                   "edges": [[labels[u], labels[v]] for u, v in graph["edges"]],
                   "fixed": [[labels[v], c] for v, c in graph["fixed"]]}
        domains = {labels[v]: {1, 2} for v in graph["vertices"]}
        frozen = deepcopy((renamed, domains))
        result = solve_local_messages(renamed, domains=domains)
        self.check_coloring(renamed, result, domains)
        self.check_decomposition(renamed, result)
        self.check_messages(renamed, result, domains)
        self.assertEqual((renamed, domains), frozen)
        self.assertEqual(result, solve_local_messages(renamed, domains=domains))

    def test_disconnected_and_empty_graphs(self):
        for graph in ({"vertices": [], "edges": []},
                      {"vertices": [0, 1, 2, 3, 4], "edges": [[0, 1], [2, 3]], "fixed": [[4, 3]]}):
            result = solve_local_messages(graph)
            self.check_coloring(graph, result)
            self.check_decomposition(graph, result)
            self.check_messages(graph, result)

    def test_invalid_limits_domains_and_graphs_are_rejected(self):
        graph = cycle(3)
        for argument in ("max_checks", "max_messages", "max_cache_entries", "transcript_limit"):
            for value in (-1, True, 2.5):
                with self.subTest(argument=argument, value=value):
                    with self.assertRaises(ValueError):
                        solve_local_messages(graph, **{argument: value})
        for domains in ({9: [0]}, {0: [4]}, {0: [True]}, {0: None}):
            with self.assertRaises(ValueError):
                solve_local_messages(graph, domains=domains)
        with self.assertRaises(ValueError):
            solve_local_messages(graph, audit_metadata=1)
        with self.assertRaises(ValueError):
            solve_local_messages({"vertices": [0], "edges": [[0, 0]]})


if __name__ == "__main__":
    unittest.main()
