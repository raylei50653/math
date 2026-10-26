"""Independent literal witnesses for reusable four-colour conflict motifs."""

from copy import deepcopy
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import four_color_conflicts as conflicts
import four_color_constraints as constraints


def literal_rows(vertices, edges, domains):
    """Use only original edge inequalities, independent of motif lookup code."""
    for row in product(*(domains[v] for v in vertices)):
        assignment = dict(zip(vertices, row))
        if all(assignment[u] != assignment[v] for u, v in edges):
            yield row


def cycle(labels):
    return [[labels[i], labels[(i + 1) % len(labels)]]
            for i in range(len(labels))]


class KnownConflictTests(unittest.TestCase):
    def assert_certificate(self, certificate, vertices, edges, domains,
                           expected_id=None, scope="current-domains"):
        self.assertIsNotNone(certificate)
        if expected_id is not None:
            self.assertEqual(certificate["id"], expected_id)
        self.assertEqual(certificate["scope"], scope)
        self.assertIs(certificate["empty_relation"], True)
        self.assertTrue(certificate["name"])
        self.assertTrue(certificate["condition"])
        selected = certificate["vertices"]
        self.assertEqual(len(selected), len(set(selected)))
        self.assertTrue(set(selected) <= set(vertices))
        original_edges = {frozenset(edge) for edge in edges}
        self.assertTrue(all(frozenset(edge) in original_edges
                            for edge in certificate["edges"]))
        self.assertTrue(all(set(edge) <= set(selected)
                            for edge in certificate["edges"]))
        selected_domains = {entry["vertex"]: entry["colors"]
                            for entry in certificate["domains"]}
        self.assertEqual(set(selected_domains), set(selected))
        original_domains = dict(zip(vertices, domains))
        self.assertEqual(selected_domains,
                         {v: sorted(original_domains[v]) for v in selected})
        self.assertIsNone(next(literal_rows(selected, certificate["edges"],
                                            selected_domains), None))
        # The public report must remain transportable to the JSON viewer.
        json.loads(json.dumps(certificate))

    def test_catalogue_literal_relations_and_exact_projected_star_extensions(self):
        catalogue = conflicts.conflict_catalogue()
        self.assertEqual(catalogue["version"], "literal-four-colour-conflicts-v1")
        self.assertEqual(catalogue["palette"], list(range(4)))
        templates = {item["id"]: item for item in catalogue["templates"]}
        self.assertEqual(set(templates), {"fixed_edge", "four_color_star",
                                          "triangle_two_colors", "c5_two_colors", "k5"})
        for identifier in ("fixed_edge", "triangle_two_colors", "c5_two_colors", "k5"):
            template = templates[identifier]
            vertices = template["scope"]
            domains = {vertex: range(4) for vertex in vertices}
            expected = set(literal_rows(vertices, template["edges"], domains))
            actual = {tuple(row) for row in template["rows"]}
            self.assertEqual(actual, expected, identifier)
            self.assertEqual(len(actual), len(template["rows"]))
        self.assertEqual(len(templates["fixed_edge"]["rows"]), 12)
        self.assertEqual(len(templates["triangle_two_colors"]["rows"]), 24)
        self.assertEqual(len(templates["c5_two_colors"]["rows"]), 240)
        self.assertEqual(templates["k5"]["rows"], [])

        star = templates["four_color_star"]
        self.assertEqual(star["center"], 0)
        self.assertEqual(star["boundary"], [1, 2, 3, 4])
        expected = {}
        for row in literal_rows(star["scope"], star["edges"],
                                {v: range(4) for v in star["scope"]}):
            assignment = dict(zip(star["scope"], row))
            boundary = tuple(assignment[v] for v in star["boundary"])
            expected.setdefault(boundary, set()).add(assignment[star["center"]])
        actual = {tuple(row["boundary"]): set(row["colors"])
                  for row in star["rows"]}
        self.assertEqual(actual, expected)
        self.assertEqual(len(star["rows"]), 232)
        forbidden = {tuple(row) for row in star["forbidden_rows"]}
        self.assertEqual(forbidden, set(permutations(range(4))))
        self.assertEqual(len(star["forbidden_rows"]), 24)
        self.assertEqual(set(expected) | forbidden, set(product(range(4), repeat=4)))
        self.assertFalse(set(expected) & forbidden)

    def test_each_known_motif_has_a_literal_empty_original_edge_relation(self):
        labels = [90, -7, 31, 2, 65]
        cases = [
            ("fixed_edge", labels[:2], [[90, -7]], [{2}, {2}]),
            ("four_color_star", labels, [[90, v] for v in labels[1:]],
             [set(range(4)), {0}, {1}, {2}, {3}]),
            ("triangle_two_colors", labels[:3],
             [list(edge) for edge in combinations(labels[:3], 2)], [{0, 3}] * 3),
            ("c5_two_colors", labels, cycle(labels), [{1, 2}] * 5),
            ("k5", labels, [list(edge) for edge in combinations(labels, 2)],
             [set(range(4)) for _ in labels]),
        ]
        for identifier, vertices, edges, domains in cases:
            with self.subTest(identifier=identifier):
                before = deepcopy((vertices, edges, domains))
                certificate = conflicts.find_known_conflict(vertices, edges, domains)
                self.assert_certificate(certificate, vertices, edges, domains, identifier)
                self.assertEqual((vertices, edges, domains), before)

    def test_relabelled_ordered_vertices_and_reversed_edges_preserve_detection(self):
        labels = [-11, 42, 0, 71, 8]
        edges = cycle(labels)
        for order in (labels, list(reversed(labels)), [0, 8, 42, -11, 71]):
            domains = [{0, 2} for _ in order]
            certificate = conflicts.find_known_conflict(order,
                [list(reversed(edge)) for edge in reversed(edges)], domains)
            self.assert_certificate(certificate, order, edges, domains, "c5_two_colors")

    def test_certificate_omits_unrelated_disconnected_components(self):
        vertices = [80, 4, 27, -20, 99]
        edges = [[80, 4], [4, 27], [27, 80], [-20, 99]]
        domains = [{1, 3}, {1, 3}, {1, 3}, {0}, {2, 3}]
        certificate = conflicts.find_known_conflict(vertices, edges, domains)
        self.assert_certificate(certificate, vertices, edges, domains, "triangle_two_colors")
        self.assertEqual(set(certificate["vertices"]), {80, 4, 27})

    def test_star_certificate_is_a_scoped_obstruction_to_extension(self):
        vertices = [50, 7, 19, -4, 88]
        edges = [[50, leaf] for leaf in vertices[1:]]
        domains = [set(range(4)), {0}, {1}, {2}, {3}]
        fixed = [[leaf, color] for leaf, color in zip(vertices[1:], range(4))]
        certificate = conflicts.find_known_conflict(vertices, edges, domains,
                                                   fixed=fixed, scope="fixed-context")
        self.assert_certificate(certificate, vertices, edges, domains,
                                "four_color_star", scope="fixed-context")
        self.assertEqual({tuple(pair) for pair in certificate["fixed"]},
                         {tuple(pair) for pair in fixed})
        # The same original star is colourable when this boundary is released.
        self.assertIsNotNone(next(literal_rows(vertices, edges,
                                                {v: range(4) for v in vertices}), None))
        self.assertIsNone(conflicts.find_known_conflict(vertices, edges,
                           [set(range(4)) for _ in vertices]))

    def test_possible_four_colours_do_not_block_a_star(self):
        vertices = list(range(5))
        edges = [[0, leaf] for leaf in vertices[1:]]
        cases = [[{0, 1, 2, 3}, {0, 1}, {1, 2}, {2, 3}, {0, 3}],
                 [{0}, {0, 1}, {1}, {2}, {3}],
                 [set(range(4)), {0}, {1}, {2}, {2}]]
        for domains in cases:
            with self.subTest(domains=domains):
                self.assertIsNotNone(next(literal_rows(vertices, edges,
                                           dict(zip(vertices, domains))), None))
                self.assertIsNone(conflicts.find_known_conflict(vertices, edges, domains))

    def test_triangle_and_five_cycle_escape_third_colour_is_not_a_conflict(self):
        for size in (3, 5):
            vertices = list(range(size))
            edges = cycle(vertices)
            domains = [{0, 1} for _ in vertices]
            domains[-1] = {0, 1, 3}
            self.assertIsNotNone(next(literal_rows(vertices, edges,
                                       dict(zip(vertices, domains))), None))
            self.assertIsNone(conflicts.find_known_conflict(vertices, edges, domains))

    def test_domain_free_odd_cycle_is_not_a_graph_obstruction(self):
        vertices = list(range(5))
        self.assertIsNone(conflicts.find_known_conflict(vertices, cycle(vertices),
                                                       [range(4)] * 5))

    def test_bounded_cycle_scan_omits_an_uncompleted_motif(self):
        vertices = [14, 9, 40, -2, 33]
        self.assertIsNone(conflicts.find_known_conflict(vertices, cycle(vertices),
                           [{0, 1}] * 5, max_scan_steps=0))
        self.assert_certificate(conflicts.find_known_conflict(vertices, cycle(vertices),
                                [{0, 1}] * 5), vertices, cycle(vertices),
                                [{0, 1}] * 5, "c5_two_colors")

    def test_detector_does_not_swallow_work_budget_interruption(self):
        class BudgetExpired(Exception):
            pass

        def charge():
            raise BudgetExpired

        with self.assertRaises(BudgetExpired):
            conflicts.find_known_conflict([1, 7], [[1, 7]], [{2}, {2}], charge=charge)

    def test_solver_records_original_motifs_before_any_elimination(self):
        triangle = {"vertices": list(range(5)),
                    "edges": [[0, 1], [1, 2], [2, 0]]
                             + [[u, v] for u in range(3) for v in (3, 4)],
                    "fixed": [[3, 2], [4, 3]]}
        ring = {"vertices": list(range(7)), "edges": cycle(list(range(5)))
                + [[u, v] for u in range(5) for v in (5, 6)],
                "fixed": [[5, 2], [6, 3]]}
        star = {"vertices": list(range(5)), "edges": [[0, v] for v in range(1, 5)],
                "fixed": [[v, v - 1] for v in range(1, 5)]}
        for graph, identifier in ((star, "four_color_star"),
                                  (triangle, "triangle_two_colors"),
                                  (ring, "c5_two_colors")):
            with self.subTest(identifier=identifier):
                result = constraints.solve_constraints(graph, use_substructures=False,
                             use_c5=False, use_conflicts=True)
                control = constraints.solve_constraints(graph, use_substructures=False,
                              use_c5=False, use_conflicts=False)
                self.assertEqual(result["status"], "unsatisfiable")
                self.assertEqual(result["status"], control["status"])
                self.assertEqual(result["stats"]["eliminations"], 0)
                self.assertEqual(result["stats"]["writebacks"], 0)
                certificates = result["conflict_subgraphs"]
                self.assertTrue(certificates)
                self.assertIn(identifier, [item["id"] for item in certificates])
                events = [event for event in result["events"]
                          if event.get("conflict_subgraph")]
                self.assertTrue(events)
                self.assertTrue(all(event["kind"] == "conflict" for event in events))
                self.assertTrue(all(event["conflict_subgraph"] in certificates for event in events))
                original = {frozenset(edge) for edge in graph["edges"]}
                for certificate in certificates:
                    self.assertTrue(all(frozenset(edge) in original
                                        for edge in certificate["edges"]))
                    domain_map = {item["vertex"]: item["colors"]
                                  for item in certificate["domains"]}
                    self.assertIsNone(next(literal_rows(certificate["vertices"],
                        certificate["edges"], domain_map), None))

    def test_catalogue_export_mutation_cannot_corrupt_later_queries(self):
        before = conflicts.conflict_catalogue()
        mutated = conflicts.conflict_catalogue()
        mutated["palette"].clear()
        for template in mutated["templates"]:
            template["edges"].clear()
            template["rows"].clear()
        self.assertEqual(conflicts.conflict_catalogue(), before)
        self.assertIsNotNone(conflicts.find_known_conflict([0, 1], [[0, 1]], [{1}, {1}]))


if __name__ == "__main__":
    unittest.main()
