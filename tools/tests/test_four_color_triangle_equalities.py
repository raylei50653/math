"""Original-edge proof replay and solution preservation for equality closure."""
from copy import deepcopy
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_triangle_equalities import derive_triangle_equalities
from four_color_constraints import solve_constraints


def literal_solutions(vertices, edges, domains):
    for row in product(*(sorted(domains[v]) for v in vertices)):
        assignment = dict(zip(vertices, row))
        if all(assignment[u] != assignment[v] for u, v in edges):
            yield assignment


def ordinary_domains(graph):
    """Capture ordinary GAC before any optional cycle/context discovery."""
    state = {}

    class Captured(Exception):
        pass

    def returned(frame, event, answer):
        if event == "return":
            state.update(domains=deepcopy(frame.f_back.f_locals["domains"]), consistent=answer)
            raise Captured
        return returned

    def called(frame, event, arg):
        if event == "call" and frame.f_code.co_name == "propagate":
            return returned
        return None

    previous = sys.gettrace()
    sys.settrace(called)
    try:
        solve_constraints(graph)
    except Captured:
        pass
    finally:
        sys.settrace(previous)
    return dict(zip(graph["vertices"], state["domains"]))


def backtracking_solutions(graph):
    """Independent full original-edge enumeration for the dense fourteen-point graph."""
    adjacency = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adjacency[u].add(v)
        adjacency[v].add(u)
    assigned = {}

    def visit():
        if len(assigned) == len(adjacency):
            yield assigned.copy()
            return
        choices = {v: set(range(4)) - {assigned[w] for w in adjacency[v] if w in assigned}
                   for v in adjacency if v not in assigned}
        v = min(choices, key=lambda v: (len(choices[v]), -len(adjacency[v]), v))
        for color in sorted(choices[v]):
            assigned[v] = color
            yield from visit()
        assigned.pop(v, None)

    yield from visit()


class TriangleEqualityTests(unittest.TestCase):
    def check_proof(self, vertices, edges, initial, result):
        original = {frozenset(edge) for edge in edges}
        groups = {v: {v} for v in vertices}
        domains = {v: set(initial[v]) for v in vertices}

        def group(evidence):
            members = set(evidence["vertices"])
            self.assertTrue(members)
            self.assertEqual(groups[next(iter(members))], members)
            self.assertTrue(all(groups[v] == members for v in members))
            self.assertTrue(all(domains[v] == set(evidence["colors"]) for v in members))
            return members

        def joined(left, right, witnesses):
            return any((u in left and v in right) or (v in left and u in right)
                       for u, v in witnesses)

        for step in result["proof_steps"]:
            witnesses = step["source_edges"]
            self.assertTrue(all(frozenset(edge) in original for edge in witnesses))
            palette = set(step["palette"])
            self.assertEqual(len(palette), 3)
            if step["kind"] == "three_color_double_triangle":
                a, b = map(group, step["shared_edge_classes"])
                u, v = map(group, step["equal_classes"])
                self.assertTrue(all(domains[x] <= palette for part in (a, b, u, v) for x in part))
                self.assertTrue(all(joined(left, right, witnesses)
                                    for left, right in ((a, b), (a, u), (b, u), (a, v), (b, v))))
                merged = u | v
                shared = set.intersection(*(domains[x] for x in merged))
                self.assertEqual(shared, set(step["intersection"]))
                for x in merged:
                    groups[x], domains[x] = merged, set(shared)
            else:
                self.assertEqual(step["kind"], "three_color_triangle_exclusion")
                triangle = list(map(group, step["triangle_classes"]))
                hub = group(step["neighbor_class"])
                self.assertTrue(all(domains[x] <= palette for part in triangle for x in part))
                self.assertTrue(all(joined(left, right, witnesses)
                                    for left, right in combinations(triangle, 2)))
                self.assertTrue(all(joined(part, hub, witnesses) for part in triangle))
                narrowed = domains[next(iter(hub))] - palette
                self.assertEqual(narrowed, set(step["colors_after"]))
                for x in hub:
                    domains[x] = set(narrowed)
        self.assertEqual({frozenset(group) for group in result["classes"]},
                         {frozenset(group) for group in groups.values()})
        self.assertEqual(result["domains"], domains)
        self.assertTrue(all(frozenset(edge) in original for edge in result["source_edges"]))
        if not result["consistent"]:
            conflict = result["conflict"]
            if conflict["kind"] == "empty_class_domain":
                self.assertTrue(all(not domains[v] for v in conflict["vertices"]))
            else:
                u, v = conflict["edge"]
                self.assertIn(frozenset((u, v)), original)
                if conflict["kind"] == "equal_edge":
                    self.assertEqual(groups[u], groups[v])
                else:
                    self.assertEqual(conflict["kind"], "same_singleton_edge")
                    self.assertEqual(domains[u], domains[v])
                    self.assertEqual(len(domains[u]), 1)

    def test_double_triangle_keeps_all_six_literal_solutions(self):
        vertices = [20, -3, 7, 90]
        edges = [[20, -3], [20, 7], [-3, 7], [20, 90], [-3, 90]]
        domains = {v: {0, 1, 3} for v in vertices}
        result = derive_triangle_equalities(vertices, edges, domains)
        self.assertTrue(result["consistent"])
        self.assertIn((7, 90), result["classes"])
        self.check_proof(vertices, edges, domains, result)
        solutions = list(literal_solutions(vertices, edges, domains))
        self.assertEqual(len(solutions), 6)
        self.assertTrue(all(solution[7] == solution[90] for solution in solutions))

    def test_quotient_three_color_triangle_detects_fourteen_point_gap_before_contexts(self):
        graph = json.loads((ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f/"
                           "propagation/inputs.json").read_text())["graph"]
        domains = ordinary_domains(graph)
        self.assertEqual(domains[7], {0, 1, 2, 3})
        self.assertEqual(domains[13], {0, 1, 2, 3})
        before = deepcopy((graph, domains))
        result = derive_triangle_equalities(graph["vertices"], graph["edges"], domains)
        self.assertTrue(result["complete"])
        self.assertFalse(result["consistent"])
        self.assertLess(result["checks"], 2000)
        self.assertTrue(any(step["kind"] == "three_color_triangle_exclusion"
                            for step in result["proof_steps"]))
        self.check_proof(graph["vertices"], graph["edges"], domains, result)
        self.assertEqual((graph, domains), before)
        labels = {v: 1000 - 17 * v for v in graph["vertices"]}
        renamed = derive_triangle_equalities(
            [labels[v] for v in graph["vertices"]],
            [[labels[u], labels[v]] for u, v in graph["edges"]],
            {labels[v]: colors for v, colors in domains.items()})
        self.assertFalse(renamed["consistent"])
        self.assertEqual(renamed["checks"], result["checks"])

    def test_all_four_color_domains_exit_after_charged_domain_reads(self):
        vertices = list(range(14))
        edges = [list(edge) for edge in combinations(vertices, 2)]
        domains = {v: set(range(4)) for v in vertices}
        ticks = []
        result = derive_triangle_equalities(vertices, edges, domains, charge=lambda: ticks.append(1))
        self.assertTrue(result["complete"])
        self.assertTrue(result["consistent"])
        self.assertEqual(result["checks"], len(vertices))
        self.assertEqual(result["checks"], len(ticks))
        self.assertEqual(result["domains"], domains)
        self.assertEqual(result["proof_steps"], [])
        self.assertEqual(result["check_kinds"]["edge"], 0)
        # This means no deduction, even though this K14 is not four-colourable.

    def test_all_624_bare_graph_solutions_are_preserved(self):
        graph = json.loads((ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f/"
                           "propagation/inputs.json").read_text())["graph"]
        graph = dict(graph, fixed=[])
        result = derive_triangle_equalities(graph["vertices"], graph["edges"],
                                            {v: set(range(4)) for v in graph["vertices"]})
        count = 0
        for solution in backtracking_solutions(graph):
            count += 1
            self.assertTrue(all(solution[v] in result["domains"][v] for v in graph["vertices"]))
            self.assertTrue(all(len({solution[v] for v in group}) == 1 for group in result["classes"]))
        self.assertEqual(count, 624)

    def test_limits_and_external_interruptions_never_publish_partial_deductions(self):
        vertices = list(range(4))
        edges = [list(edge) for edge in combinations(vertices, 2)]
        domains = {v: {0, 1, 2} for v in vertices}
        before = deepcopy((vertices, edges, domains))
        full = derive_triangle_equalities(vertices, edges, domains)
        for cap in (0, 4, full["checks"] - 1):
            result = derive_triangle_equalities(vertices, edges, domains, max_checks=cap)
            self.assertFalse(result["complete"])
            self.assertIsNone(result["consistent"])
            for field in ("classes", "domains", "proof_steps", "source_edges", "conflict"):
                self.assertIsNone(result[field])
            self.assertEqual(result["checks"], cap)
        ticks = []

        def fail():
            ticks.append(1)
            if len(ticks) == 6:
                raise RuntimeError("external budget")

        with self.assertRaisesRegex(RuntimeError, "external budget"):
            derive_triangle_equalities(vertices, edges, domains, charge=fail)
        self.assertEqual((vertices, edges, domains), before)

    def test_random_small_graphs_preserve_every_original_solution_and_replay_proofs(self):
        rng = random.Random(26030)
        for index in range(200):
            vertices = rng.sample(range(-20, 30), rng.randrange(0, 7))
            edges = [list(edge) for edge in combinations(vertices, 2) if rng.random() < .55]
            domains = {v: {c for c in range(4) if rng.random() < .75} for v in vertices}
            result = derive_triangle_equalities(vertices, edges, domains)
            self.assertTrue(result["complete"])
            self.check_proof(vertices, edges, domains, result)
            for solution in literal_solutions(vertices, edges, domains):
                with self.subTest(index=index):
                    self.assertTrue(result["consistent"])
                    self.assertTrue(all(solution[v] in result["domains"][v] for v in vertices))
                    self.assertTrue(all(len({solution[v] for v in group}) == 1
                                        for group in result["classes"]))

    def test_invalid_input_and_empty_domains_precede_full_palette_fastpath(self):
        with self.assertRaises(ValueError):
            derive_triangle_equalities([1], [[1, 1]], {1: set(range(4))})
        with self.assertRaises(ValueError):
            derive_triangle_equalities([1, 2], [[1, 2], [2, 1]], {1: {0}, 2: {1}})
        with self.assertRaises(ValueError):
            derive_triangle_equalities([1], [], {1: {True}})
        with self.assertRaises(ValueError):
            derive_triangle_equalities([], [], {}, max_checks=True)
        result = derive_triangle_equalities([1, 2], [], {1: set(range(4)), 2: set()})
        self.assertFalse(result["consistent"])
        self.assertEqual(result["conflict"]["kind"], "empty_class_domain")


if __name__ == "__main__":
    unittest.main()
