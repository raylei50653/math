"""Independent original-edge checks for compact local colouring information."""

from itertools import combinations, product
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from four_color_local_information import (
    derive_cycle, path_endpoint_relation, validate_separator,
)


def literal_rows(masks, *, close_cycle=False):
    """Oracle uses original edges and domains, without a transfer recurrence."""
    domains = [[colour for colour in range(4) if mask & (1 << colour)]
               for mask in masks]
    for row in product(*domains):
        if any(row[i] == row[i + 1] for i in range(len(row) - 1)):
            continue
        if close_cycle and row[-1] == row[0]:
            continue
        yield row


def literal_graph_rows(vertex_count, edges):
    for row in product(range(4), repeat=vertex_count):
        if all(row[u] != row[v] for u, v in edges):
            yield row


class ArbitraryCycleTests(unittest.TestCase):
    def assert_witness(self, witness, masks, *, close_cycle=False):
        self.assertEqual(len(witness), len(masks))
        self.assertTrue(all(type(colour) is int and 0 <= colour < 4
                            and masks[i] & (1 << colour)
                            for i, colour in enumerate(witness)))
        self.assertTrue(all(witness[i] != witness[i + 1]
                            for i in range(len(witness) - 1)))
        if close_cycle:
            self.assertNotEqual(witness[-1], witness[0])

    def assert_cycle_oracle(self, masks):
        expected_supports = [0] * len(masks)
        expected_count = 0
        for row in literal_rows(masks, close_cycle=True):
            expected_count += 1
            for i, colour in enumerate(row):
                expected_supports[i] |= 1 << colour
        before = list(masks)
        result = derive_cycle(masks)
        self.assertEqual(masks, before)
        self.assertEqual(result["supports"], expected_supports)
        self.assertEqual(result["row_count"], expected_count)
        if expected_count:
            self.assert_witness(result["witness"], masks, close_cycle=True)
        else:
            self.assertIsNone(result["witness"])
        return result

    def test_32_selected_domains_on_original_cycles_c3_through_c10(self):
        rng = random.Random(20261025)
        for size in range(3, 11):
            # Long cases have small literal domains; this is a finite oracle,
            # not an exhaustive search over all possible input domain masks.
            cases = [
                [15] * size if size <= 7
                else [3, 6, 12, 9] * (size // 4) + [3] * (size % 4),
                [rng.choice((3, 5, 6, 7, 9, 10, 12, 13, 14))
                 for _ in range(size)],
                [15 if i == size // 2 else (3, 5, 9)[i % 3]
                 for i in range(size)],
                [0 if i == size // 2 else 15 for i in range(size)],
            ]
            for masks in cases:
                with self.subTest(size=size, masks=masks):
                    self.assert_cycle_oracle(masks)

    def test_full_palette_counts_match_cycle_chromatic_polynomial(self):
        for size in range(3, 41):
            with self.subTest(size=size):
                result = derive_cycle([15] * size)
                self.assertEqual(result["row_count"], 3 ** size + (-1) ** size * 3)
                self.assertEqual(result["supports"], [15] * size)
                self.assert_witness(result["witness"], [15] * size,
                                    close_cycle=True)

    def test_two_colour_odd_obstruction_and_even_alternation(self):
        for size in range(3, 11):
            with self.subTest(size=size):
                result = self.assert_cycle_oracle([5] * size)
                self.assertEqual(result["row_count"], 0 if size % 2 else 2)
                self.assertEqual(result["supports"], [0 if size % 2 else 5] * size)

    def test_unique_escape_on_c7_and_even_cycle_negative_control(self):
        odd = self.assert_cycle_oracle([15] + [3] * 6)
        self.assertEqual(odd["supports"], [12] + [3] * 6)
        self.assertEqual(odd["row_count"], 4)
        even = self.assert_cycle_oracle([15] + [3] * 5)
        self.assertEqual(even["supports"], [15] + [3] * 5)
        self.assertEqual(even["row_count"], 6)

    def test_rotation_and_colour_permutation_preserve_supports(self):
        masks = [11, 6, 13, 7, 14, 3, 5]
        original = self.assert_cycle_oracle(masks)
        for shift in range(len(masks)):
            result = self.assert_cycle_oracle(masks[shift:] + masks[:shift])
            self.assertEqual(result["row_count"], original["row_count"])
            self.assertEqual(result["supports"],
                             original["supports"][shift:] + original["supports"][:shift])
        permutation = [3, 0, 2, 1]

        def relabel(mask):
            return sum(1 << permutation[colour] for colour in range(4)
                       if mask & (1 << colour))

        result = self.assert_cycle_oracle([relabel(mask) for mask in masks])
        self.assertEqual(result["row_count"], original["row_count"])
        self.assertEqual(result["supports"], [relabel(mask) for mask in original["supports"]])

    def test_callback_is_charged_and_interruptions_preserve_input(self):
        masks = [15, 3, 3, 3, 3, 3, 3]
        before = masks[:]
        calls = []
        expected = derive_cycle(masks, charge=lambda: calls.append(True))
        self.assertGreater(len(calls), 0)
        self.assertEqual(len(calls), expected["op_count"])
        self.assertEqual(masks, before)

        class BudgetExpired(Exception):
            pass

        def exhausted():
            raise BudgetExpired

        with self.assertRaises(BudgetExpired):
            derive_cycle(masks, charge=exhausted)
        self.assertEqual(masks, before)
        self.assertEqual(derive_cycle(masks), expected)

    def test_invalid_cycle_inputs_are_rejected(self):
        invalid = ([], [15], [15, 15], [15, -1, 15], [15, 16, 15],
                   [15, True, 15], [15, 1.0, 15])
        for masks in invalid:
            with self.subTest(masks=masks), self.assertRaises(ValueError):
                derive_cycle(masks)
        with self.assertRaises(ValueError):
            derive_cycle([15] * 3, charge=3)


class PathInterfaceTests(unittest.TestCase):
    assert_witness = ArbitraryCycleTests.assert_witness

    def assert_endpoint_oracle(self, masks):
        counts = [[0] * 4 for _ in range(4)]
        for row in literal_rows(masks):
            counts[row[0]][row[-1]] += 1
        expected_rows = [[a, b] for a in range(4) for b in range(4) if counts[a][b]]
        before = masks[:]
        result = path_endpoint_relation(masks)
        self.assertEqual(masks, before)
        self.assertEqual(result["counts"], counts)
        self.assertEqual(result["rows"], expected_rows)
        self.assertEqual(result["state_count"], len(expected_rows))
        self.assertLessEqual(result["state_count"], 16)
        witnesses = result["witness_by_endpoints"]
        self.assertEqual(len(witnesses), len(expected_rows))
        self.assertEqual({tuple(item["boundary"]) for item in witnesses},
                         set(map(tuple, expected_rows)))
        for item in witnesses:
            self.assert_witness(item["colors"], masks)
            self.assertEqual(item["boundary"], [item["colors"][0], item["colors"][-1]])
        return result

    def test_path_endpoints_counts_and_full_witnesses_against_original_edges(self):
        for size in range(1, 11):
            cases = [[15] * size if size <= 7 else [3] * size,
                     [(3, 5, 7, 9)[i % 4] for i in range(size)],
                     [0 if i == size // 2 else 15 for i in range(size)]]
            for masks in cases:
                with self.subTest(size=size, masks=masks):
                    self.assert_endpoint_oracle(masks)

    def test_single_vertex_boundary_is_diagonal_and_cannot_split_its_two_roles(self):
        result = self.assert_endpoint_oracle([10])
        self.assertEqual(result["rows"], [[1, 1], [3, 3]])
        self.assertEqual(sum(map(sum, result["counts"])), 2)

    def test_endpoint_marginals_cannot_replace_the_joint_relation(self):
        result = self.assert_endpoint_oracle([3, 3])
        self.assertEqual(result["rows"], [[0, 1], [1, 0]])
        self.assertEqual({row[0] for row in result["rows"]}, {0, 1})
        self.assertEqual({row[1] for row in result["rows"]}, {0, 1})
        self.assertNotIn([0, 0], result["rows"])

    def test_two_paths_compose_exactly_at_their_shared_original_vertex(self):
        masks = [15, 3, 14, 5, 11, 9, 6]
        split = 3
        left = self.assert_endpoint_oracle(masks[:split + 1])
        right = self.assert_endpoint_oracle(masks[split:])
        whole = self.assert_endpoint_oracle(masks)
        composed = [[sum(left["counts"][a][middle] * right["counts"][middle][b]
                         for middle in range(4))
                     for b in range(4)] for a in range(4)]
        self.assertEqual(composed, whole["counts"])
        left_lifts = {tuple(item["boundary"]): item["colors"]
                      for item in left["witness_by_endpoints"]}
        right_lifts = {tuple(item["boundary"]): item["colors"]
                       for item in right["witness_by_endpoints"]}
        for a, b in whole["rows"]:
            middle = next(c for c in range(4)
                          if (a, c) in left_lifts and (c, b) in right_lifts)
            lift = left_lifts[a, middle] + right_lifts[middle, b][1:]
            self.assert_witness(lift, masks)

    def test_closing_endpoint_edge_recovers_exact_cycle_count(self):
        for masks in ([15] * 5, [3] * 7, [3] * 8,
                      [15, 3, 3, 3, 3, 3, 3], [11, 6, 13, 7, 14, 3]):
            with self.subTest(masks=masks):
                path = self.assert_endpoint_oracle(masks)
                cycle = derive_cycle(masks)
                self.assertEqual(cycle["row_count"],
                                 sum(path["counts"][a][b] for a in range(4)
                                     for b in range(4) if a != b))

    def test_invalid_path_inputs_are_rejected(self):
        for masks in ([], [-1], [16], [True], [1.0]):
            with self.subTest(masks=masks), self.assertRaises(ValueError):
                path_endpoint_relation(masks)


class ProjectionLossTests(unittest.TestCase):
    def test_star_has_232_rows_but_even_all_triple_projections_miss_24_conflicts(self):
        edges = [[0, leaf] for leaf in range(1, 5)]
        fibres = {}
        for row in literal_graph_rows(5, edges):
            fibres.setdefault(row[1:], set()).add(row[0])
        self.assertEqual(len(fibres), 232)
        for boundary, colours in fibres.items():
            self.assertEqual(colours, set(range(4)) - set(boundary))
        triples = list(combinations(range(4), 3))
        projections = {indices: {tuple(row[i] for i in indices) for row in fibres}
                       for indices in triples}
        self.assertTrue(all(len(rows) == 4 ** 3 for rows in projections.values()))
        joined = {row for row in product(range(4), repeat=4)
                  if all(tuple(row[i] for i in indices) in projections[indices]
                         for indices in triples)}
        self.assertEqual(len(joined), 256)
        self.assertEqual(len(joined - set(fibres)), 24)
        self.assertIn((0, 1, 2, 3), joined)
        self.assertNotIn((0, 1, 2, 3), fibres)

    def test_c5_wheel_has_120_joint_rows_but_triple_join_accepts_240(self):
        rim_edges = [[i, (i + 1) % 5] for i in range(5)]
        edges = rim_edges + [[5, i] for i in range(5)]
        fibres = {}
        for row in literal_graph_rows(6, edges):
            fibres.setdefault(row[:5], set()).add(row[5])
        self.assertEqual(len(fibres), 120)
        for boundary, colours in fibres.items():
            self.assertEqual(len(set(boundary)), 3)
            self.assertEqual(colours, set(range(4)) - set(boundary))
        triples = list(combinations(range(5), 3))
        projections = {indices: {tuple(row[i] for i in indices) for row in fibres}
                       for indices in triples}
        joined = {row for row in product(range(4), repeat=5)
                  if all(tuple(row[i] for i in indices) in projections[indices]
                         for indices in triples)}
        proper_rim = set(literal_rows([15] * 5, close_cycle=True))
        self.assertEqual(joined, proper_rim)
        self.assertEqual(len(joined), 240)
        self.assertIn((0, 1, 2, 3, 1), joined)
        self.assertNotIn((0, 1, 2, 3, 1), fibres)


class SeparatorSafetyTests(unittest.TestCase):
    def test_hidden_edge_between_two_interiors_requires_an_enlarged_interface(self):
        graph = {"vertices": list(range(6)),
                 "edges": [[center, leaf] for center in (0, 1)
                           for leaf in range(2, 6)] + [[0, 1]]}
        before = {"vertices": graph["vertices"][:],
                  "edges": [edge[:] for edge in graph["edges"]]}
        unsafe = validate_separator(graph, [0], [2, 3, 4, 5])
        self.assertFalse(unsafe["valid"])
        self.assertEqual({frozenset(edge) for edge in unsafe["escaping_edges"]},
                         {frozenset((0, 1))})
        safe = validate_separator(graph, [0], [1, 2, 3, 4, 5])
        self.assertTrue(safe["valid"])
        self.assertEqual(safe["escaping_edges"], [])
        self.assertEqual(graph, before)

    def test_attachment_to_a_forgotten_path_interior_is_not_an_endpoint_attachment(self):
        graph = {"vertices": [10, 20, 30, 40],
                 "edges": [[10, 20], [20, 30], [20, 40]]}
        result = validate_separator(graph, [20], [10, 30])
        self.assertFalse(result["valid"])
        self.assertEqual({frozenset(edge) for edge in result["escaping_edges"]},
                         {frozenset((20, 40))})
        self.assertTrue(validate_separator(graph, [20], [10, 30, 40])["valid"])

    def test_unknown_vertices_and_overlapping_interface_are_rejected(self):
        graph = {"vertices": [10, 20], "edges": [[10, 20]]}
        for interior, boundary in (([99], [20]), ([10], [99]), ([10], [10, 20])):
            with self.subTest(interior=interior, boundary=boundary):
                with self.assertRaises(ValueError):
                    validate_separator(graph, interior, boundary)


if __name__ == "__main__":
    unittest.main()
