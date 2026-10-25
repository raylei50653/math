"""Check structural C5 derivation against independent literal edge assignments."""

from itertools import product
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from four_color_cycle_structure import derive_c5
import four_color_constraints as constraints


# Test oracle only: generate all literal assignments from five edge inequalities.
ORACLE_ROWS = tuple(row for row in product(range(4), repeat=5)
                    if all(row[i] != row[(i + 1) % 5] for i in range(5)))
ORACLE_BITS = tuple(tuple(1 << colour for colour in row) for row in ORACLE_ROWS)


def oracle(masks):
    supports = [0] * 5
    count = 0
    for row in ORACLE_BITS:
        if (masks[0] & row[0] and masks[1] & row[1] and masks[2] & row[2]
                and masks[3] & row[3] and masks[4] & row[4]):
            count += 1
            for position in range(5):
                supports[position] |= row[position]
    return supports, count


def bipyramid():
    """An original five-ring with two independent hubs, using literal labels."""
    ring = [40, -3, 19, 72, 0]
    hubs = [8, -11]
    return {"vertices": [19, 8, 40, -11, 0, -3, 72],
            "edges": [[ring[i], ring[(i + 1) % 5]] for i in range(5)]
                     + [[hub, vertex] for hub in hubs for vertex in ring]}, ring, hubs


def original_graph_colourings(graph):
    fixed = dict(graph.get("fixed", []))
    domains = [(fixed[vertex],) if vertex in fixed else range(4)
               for vertex in graph["vertices"]]
    for row in product(*domains):
        assignment = dict(zip(graph["vertices"], row))
        if all(assignment[u] != assignment[v] for u, v in graph["edges"]):
            yield assignment


class StructuralC5Tests(unittest.TestCase):
    def assert_derivation(self, masks, preview=True):
        result = derive_c5(masks)
        expected_supports, expected_count = oracle(masks)
        self.assertEqual((result["supports"], result["row_count"]),
                         (expected_supports, expected_count), masks)
        self.assertEqual(result["method"], "cycle-path-consistency")
        self.assertGreater(result["op_count"], 0)
        self.assertTrue(any(rule["id"] == "cycle_path_consistency"
                            for rule in result["rules"]))
        if preview:
            rows = result["relation_preview"]
            self.assertLessEqual(len(rows), 6)
            self.assertEqual(len(rows), len(set(map(tuple, rows))))
            self.assertEqual(len(rows), min(6, expected_count))
            for row in rows:
                self.assertEqual(len(row), 5)
                self.assertTrue(all(masks[i] & (1 << row[i]) for i in range(5)))
                self.assertTrue(all(row[i] != row[(i + 1) % 5] for i in range(5)))
        return result

    def test_all_32768_three_colour_domain_masks_against_edge_oracle(self):
        # Includes empty domains and every subset of colours 0, 1, and 2.
        for masks in product(range(8), repeat=5):
            self.assert_derivation(masks, preview=False)

    def test_10000_seeded_four_colour_queries_against_edge_oracle(self):
        rng = random.Random(20261025)
        for _ in range(10000):
            self.assert_derivation(tuple(rng.randrange(16) for _ in range(5)))

    def test_unrestricted_ring_has_240_rows_and_full_support(self):
        result = self.assert_derivation([15] * 5)
        self.assertEqual(result["row_count"], 240)
        self.assertEqual(result["supports"], [15] * 5)
        rule = next(rule for rule in result["rules"]
                    if rule["id"] == "cycle_path_consistency")
        self.assertEqual([case["row_count"] for case in rule["anchor_cases"]], [60] * 4)

    def test_two_colour_odd_cycle_explains_its_empty_relation(self):
        result = self.assert_derivation([5] * 5)
        self.assertEqual(result["supports"], [0] * 5)
        self.assertEqual(result["row_count"], 0)
        rule = next(rule for rule in result["rules"]
                    if rule["id"] == "odd_cycle_two_colors")
        self.assertEqual(rule["pair"], [0, 2])
        self.assertTrue(rule["condition"])
        self.assertTrue(rule["conclusion"])

    def test_unique_escape_can_retain_both_colours_outside_the_pair(self):
        result = self.assert_derivation([15, 3, 3, 3, 3])
        self.assertEqual(result["row_count"], 4)
        self.assertEqual(result["supports"], [12, 3, 3, 3, 3])
        rule = next(rule for rule in result["rules"]
                    if rule["id"] == "odd_cycle_unique_escape" and rule["vertex"] == 0)
        self.assertEqual(rule["pair"], [0, 1])
        self.assertEqual(rule["removed_colors"], [0, 1])

    def test_adjacent_singleton_removes_the_colour_on_both_incident_edges(self):
        result = self.assert_derivation([2, 15, 15, 15, 15])
        self.assertEqual(result["supports"], [2, 13, 15, 15, 13])
        adjacent = [rule for rule in result["rules"] if rule["id"] == "adjacent_singleton"]
        self.assertEqual({rule["vertex"] for rule in adjacent}, {1, 4})
        self.assertTrue(all(rule["fixed_vertex"] == 0 and rule["color"] == 1
                            for rule in adjacent))

    def test_rotation_and_colour_relabeling_preserve_exact_derivation(self):
        masks = [11, 6, 13, 7, 14]
        original = self.assert_derivation(masks)
        for shift in range(5):
            rotated = masks[shift:] + masks[:shift]
            result = self.assert_derivation(rotated)
            self.assertEqual(result["row_count"], original["row_count"])
            self.assertEqual(result["supports"],
                             original["supports"][shift:] + original["supports"][:shift])
        permutation = [3, 0, 2, 1]

        def relabel(mask):
            return sum(1 << permutation[colour] for colour in range(4)
                       if mask & (1 << colour))

        result = self.assert_derivation([relabel(mask) for mask in masks])
        self.assertEqual(result["row_count"], original["row_count"])
        self.assertEqual(result["supports"], [relabel(mask) for mask in original["supports"]])

    def test_each_forward_backward_case_has_exact_conditioned_supports(self):
        masks = [15, 11, 13, 14, 7]
        result = self.assert_derivation(masks)
        generic = next(rule for rule in result["rules"]
                       if rule["id"] == "cycle_path_consistency")
        for case in generic["anchor_cases"]:
            conditioned = masks[:]
            conditioned[0] = 1 << case["anchor"]
            supports, count = oracle(conditioned)
            self.assertEqual(case["row_count"], count)
            self.assertEqual([a & b for a, b in zip(case["forward_masks"], case["backward_masks"])],
                             supports)

    def test_charging_matches_operations_and_does_not_mutate_domains(self):
        masks = [15, 3, 3, 3, 3]
        calls = []
        result = derive_c5(masks, charge=lambda: calls.append(True))
        self.assertEqual(len(calls), result["op_count"])
        self.assertEqual(masks, [15, 3, 3, 3, 3])

        class BudgetExpired(Exception):
            pass

        def exhausted():
            raise BudgetExpired

        with self.assertRaises(BudgetExpired):
            derive_c5(masks, charge=exhausted)
        self.assertEqual(masks, [15, 3, 3, 3, 3])
        self.assertEqual(derive_c5(masks), result)

    def test_invalid_masks_are_rejected(self):
        for masks in ([], [15] * 4, [15] * 6, [15, 15, -1, 15, 15],
                      [15, 16, 15, 15, 15], [True, 15, 15, 15, 15],
                      [15, 15, 1.0, 15, 15]):
            with self.subTest(masks=masks), self.assertRaises(ValueError):
                derive_c5(masks)
        with self.assertRaises(ValueError):
            derive_c5([15] * 5, charge=3)


class StructuralHubEqualityTests(unittest.TestCase):
    def solve(self, graph):
        return constraints.solve_constraints(graph, use_c5=True,
                    c5_method="structure", use_conflicts=False,
                    use_substructures=False)

    def equality(self, result):
        matches = [item for item in result["self_constraints"]
                   if item["id"] == "c5_hub_equality"]
        self.assertEqual(len(matches), 1)
        return matches[0]

    def assert_witness(self, graph, result):
        self.assertEqual(result["status"], "colored")
        assignment = dict(zip(graph["vertices"], result["colors"]))
        self.assertTrue(all(type(colour) is int and 0 <= colour < 4
                            for colour in assignment.values()))
        self.assertTrue(all(assignment[u] != assignment[v] for u, v in graph["edges"]))
        self.assertTrue(all(assignment[v] == colour for v, colour in graph.get("fixed", [])))

    def test_original_bipyramid_records_a_structural_equality_factor(self):
        graph, ring, hubs = bipyramid()
        result = self.solve(graph)
        self.assert_witness(graph, result)
        equality = self.equality(result)
        self.assertEqual(set(equality["vertices"]), set(graph["vertices"]))
        self.assertEqual(len(equality["vertices"]), 7)
        self.assertEqual(set(equality["cycle"]), set(ring))
        self.assertEqual(set(equality["boundary"]), set(hubs))
        self.assertEqual(equality["vertices"][:5], equality["cycle"])
        self.assertEqual(equality["vertices"][5:], equality["boundary"])
        self.assertEqual({frozenset(edge) for edge in equality["edges"]},
                         {frozenset(edge) for edge in graph["edges"]})
        self.assertEqual(len(equality["edges"]), 15)
        self.assertEqual(equality["rows"], [[colour, colour] for colour in range(4)])
        self.assertTrue(equality["condition"])
        self.assertTrue(equality["conclusion"])
        events = [event for event in result["events"]
                  if event["kind"] == "structural_constraint"]
        self.assertTrue(events)
        matching = [event for event in events if set(event["frontier"]) == set(hubs)]
        self.assertTrue(matching)
        self.assertTrue(matching[0]["structural_rules"])
        preview = [row["boundary"] if isinstance(row, dict) else row
                   for row in matching[0]["relation_preview"]]
        self.assertEqual(preview, equality["rows"])

    def test_every_original_global_colouring_satisfies_the_hub_equation(self):
        graph, _, hubs = bipyramid()
        rows = list(original_graph_colourings(graph))
        self.assertEqual(len(rows), 120)
        self.assertTrue(all(row[hubs[0]] == row[hubs[1]] for row in rows))
        actual_boundary = {tuple(row[v] for v in hubs) for row in rows}
        self.assertEqual(actual_boundary, {(colour, colour) for colour in range(4)})
        equality = self.equality(self.solve(graph))
        reported_boundary = {tuple(row[v] for v in equality["boundary"]) for row in rows}
        self.assertEqual({tuple(row) for row in equality["rows"]}, reported_boundary)

    def test_opposing_fixed_hubs_are_inconsistent_with_nonempty_initial_domains(self):
        graph, _, hubs = bipyramid()
        graph["fixed"] = [[hubs[0], 1], [hubs[1], 3]]
        self.assertIsNone(next(original_graph_colourings(graph), None))
        result = self.solve(graph)
        self.assertEqual(result["status"], "unsatisfiable")
        self.equality(result)
        start = next(event for event in result["events"] if event["kind"] == "start")
        self.assertTrue(all(start["domains"]))
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertEqual(result["stats"]["writebacks"], 0)

    def test_equal_fixed_hubs_and_released_boundary_remain_colourable(self):
        graph, _, hubs = bipyramid()
        for fixed in ([[[hubs[0], 2], [hubs[1], 2]], []]):
            with self.subTest(fixed=fixed):
                graph["fixed"] = fixed
                self.assertIsNotNone(next(original_graph_colourings(graph), None))
                result = self.solve(graph)
                self.assert_witness(graph, result)
                self.equality(result)


if __name__ == "__main__":
    unittest.main()
