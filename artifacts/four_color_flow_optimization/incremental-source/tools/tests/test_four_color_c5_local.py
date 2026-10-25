"""Sound but intentionally partial detection of degree-five neighbor rings."""
from itertools import combinations, permutations
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import four_color_c5 as c5
import four_color_constraints as constraints


def wheel(offset=0):
    return {"vertices": list(range(offset, offset + 6)),
            "edges": [[offset + i, offset + (i + 1) % 5] for i in range(5)]
                     + [[offset + i, offset + 5] for i in range(5)]}


def bipyramid(fixed=False):
    graph = wheel()
    graph["vertices"].append(6)
    graph["edges"].extend([[i, 6] for i in range(5)])
    if fixed:
        graph["fixed"] = [[5, 2], [6, 3]]
    return graph


def local_ring_oracle(graph, center_limit=None):
    """Check each center's induced neighbor graph using all five-point orders."""
    positions = {v: i for i, v in enumerate(graph["vertices"])}
    edges = {frozenset(edge) for edge in graph["edges"]}
    adjacency = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adjacency[u].add(v)
        adjacency[v].add(u)
    cycles = []
    centers = graph["vertices"] if center_limit is None else graph["vertices"][:center_limit]
    for center in centers:
        neighbors = adjacency[center]
        if len(neighbors) != 5:
            continue
        induced = {edge for edge in edges if edge <= neighbors}
        if len(induced) != 5:
            continue
        orders = [order for order in permutations(neighbors)
                  if {frozenset((order[i], order[(i + 1) % 5]))
                      for i in range(5)} == induced]
        if orders:
            canonical = min(orders, key=lambda row: tuple(positions[v] for v in row))
            if canonical not in cycles:
                cycles.append(canonical)
    return cycles


class LocalC5Tests(unittest.TestCase):
    def assert_full_local_scan(self, graph):
        result = c5.find_local_c5(graph)
        self.assertFalse(result["complete"])
        self.assertTrue(result["local_scan_complete"])
        self.assertFalse(result["truncated"])
        self.assertEqual(result["coverage"], "degree-five-neighbor-rings")
        self.assertEqual(result["steps"], len(graph["vertices"]))
        self.assertEqual(list(map(tuple, result["cycles"])), local_ring_oracle(graph))
        self.assertEqual(len(result["cycles"]), len(set(map(tuple, result["cycles"]))))
        self.assertEqual(len(result["centers"]), len(result["cycles"]))
        adjacency = {v: set() for v in graph["vertices"]}
        for u, v in graph["edges"]:
            adjacency[u].add(v)
            adjacency[v].add(u)
        self.assertEqual(result["eligible_centers"],
                         sum(len(neighbors) == 5 for neighbors in adjacency.values()))
        for cycle, centers in zip(result["cycles"], result["centers"]):
            self.assertTrue(centers)
            self.assertEqual(len(centers), len(set(centers)))
            self.assertTrue(all(adjacency[center] == set(cycle) for center in centers))
        return result

    def test_two_hubs_find_one_original_cycle(self):
        graph = bipyramid()
        result = self.assert_full_local_scan(graph)
        self.assertEqual(list(map(tuple, result["cycles"])), [(0, 1, 2, 3, 4)])
        self.assertEqual(result["centers"], [[5, 6]])

    def test_bare_cycle_and_degree_six_hub_are_intentionally_outside_coverage(self):
        bare = {"vertices": list(range(5)),
                "edges": [[i, (i + 1) % 5] for i in range(5)]}
        six_hub = wheel()
        six_hub["vertices"].append(6)
        six_hub["edges"].append([5, 6])
        for graph in (bare, six_hub):
            with self.subTest(graph=graph):
                self.assertEqual(self.assert_full_local_scan(graph)["cycles"], [])
                self.assertTrue(c5.find_induced_c5(graph)["cycles"])
                solved = constraints.solve_constraints(graph, use_c5=True,
                                                        c5_scan_method="local")
                self.assertEqual(solved["status"], "colored")
                self.assertEqual(solved["stats"]["c5_queries"], 0)
                colors = dict(zip(graph["vertices"], solved["colors"]))
                self.assertTrue(all(colors[u] != colors[v] for u, v in graph["edges"]))

    def test_chorded_neighbor_ring_is_rejected(self):
        graph = wheel()
        graph["edges"].append([0, 2])
        self.assertEqual(self.assert_full_local_scan(graph)["cycles"], [])

    def test_local_detection_is_valid_without_a_planarity_assumption(self):
        graph = wheel()
        graph["vertices"].extend(range(6, 11))
        graph["edges"].extend([list(edge) for edge in combinations(range(6, 11), 2)])
        graph["edges"].append([0, 6])
        result = self.assert_full_local_scan(graph)
        self.assertEqual(list(map(tuple, result["cycles"])), [(0, 1, 2, 3, 4)])

    def test_relabeling_and_input_order_preserve_original_cyclic_edges(self):
        graph = bipyramid()
        mapping = dict(zip(graph["vertices"], (91, -3, 7, -40, 0, 18, 200)))
        renamed = {"vertices": [mapping[v] for v in (3, 6, 1, 5, 0, 4, 2)],
                   "edges": [[mapping[u], mapping[v]] for u, v in graph["edges"]]}
        result = self.assert_full_local_scan(renamed)
        self.assertEqual(len(result["cycles"]), 1)
        self.assertEqual(result["cycles"][0][0], mapping[3])
        source_edges = {frozenset(edge) for edge in renamed["edges"]}
        cycle = result["cycles"][0]
        self.assertTrue(all(frozenset((cycle[i], cycle[(i + 1) % 5])) in source_edges
                            for i in range(5)))

    def test_local_scan_matches_independent_center_oracle_on_sampled_graphs(self):
        rng = random.Random(53)
        for case in range(80):
            labels = rng.sample(range(-60, 90), 9)
            graph = {"vertices": labels,
                     "edges": [list(edge) for edge in combinations(labels, 2)
                               if rng.random() < 0.55]}
            with self.subTest(case=case):
                self.assert_full_local_scan(graph)

    def test_center_budget_and_cycle_caps_keep_a_valid_discovery_prefix(self):
        first, second = wheel(), wheel(6)
        graph = {"vertices": first["vertices"] + second["vertices"],
                 "edges": first["edges"] + second["edges"]}
        expected = local_ring_oracle(graph)
        self.assertEqual(len(expected), 2)
        for cap in range(len(graph["vertices"]) + 2):
            with self.subTest(center_cap=cap):
                result = c5.find_local_c5(graph, max_steps=cap)
                self.assertLessEqual(result["steps"], cap)
                self.assertEqual(result["steps"], min(cap, len(graph["vertices"])))
                self.assertEqual(list(map(tuple, result["cycles"])),
                                 local_ring_oracle(graph, cap))
                self.assertFalse(result["complete"])
                self.assertEqual(result["truncated"], cap < len(graph["vertices"]))
                self.assertEqual(result["local_scan_complete"], cap >= len(graph["vertices"]))
        for cap in (0, 1, 2, 3):
            with self.subTest(cycle_cap=cap):
                result = c5.find_local_c5(graph, max_cycles=cap)
                self.assertEqual(list(map(tuple, result["cycles"])), expected[:cap])
                self.assertFalse(result["complete"])
                self.assertEqual(result["truncated"], cap <= len(expected))
                self.assertEqual(result["local_scan_complete"], cap > len(expected))

    def test_empty_graph_has_completed_local_scan_without_global_coverage_claim(self):
        result = self.assert_full_local_scan({"vertices": [], "edges": []})
        self.assertEqual(result["cycles"], [])

    def test_fixed_bipyramid_conflict_occurs_before_any_elimination_or_write(self):
        graph = bipyramid(fixed=True)
        # Exercise this finder/propagator even when the new guards can prove it earlier.
        result = constraints.solve_constraints(graph, use_c5=True, c5_scan_method="local",
                                               use_conflicts=False)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertEqual(result["stats"]["writebacks"], 0)
        self.assertEqual(result["colors"], [-1] * 5 + [2, 3])
        self.assertGreater(result["stats"]["c5_conflicts"], 0)
        self.assertEqual(result["c5_scan_method"], "local")
        self.assertEqual(result["substructures"]["c5_scan_coverage"],
                         "degree-five-neighbor-rings")
        self.assertFalse(result["substructures"]["c5_scan_complete"])
        self.assertTrue(result["substructures"]["c5_local_scan_complete"])
        self.assertEqual(result["substructures"]["c5_discovery_centers"], [[5, 6]])
        original = {frozenset(edge) for edge in graph["edges"]}
        conflicts = [event for event in result["events"]
                     if event["kind"] == "conflict" and event.get("relation_kind") == "c5"]
        self.assertTrue(conflicts)
        for event in conflicts:
            self.assertTrue(all(frozenset(edge) in original for edge in event["causal_edges"]))
            self.assertEqual(event["phase"], "reduce")

    def test_truncated_trace_does_not_change_a_local_conflict_verdict(self):
        graph = bipyramid(fixed=True)
        full = constraints.solve_constraints(graph, use_c5=True, c5_scan_method="local")
        short = constraints.solve_constraints(graph, use_c5=True,
                                              c5_scan_method="local", trace_limit=0)
        self.assertEqual(short["status"], full["status"])
        self.assertEqual(short["colors"], full["colors"])
        self.assertEqual(short["stats"], full["stats"])
        self.assertEqual(short["events"], [])
        self.assertTrue(short["trace_truncated"])

    def test_scan_truncation_falls_back_to_base_constraints_and_work_limit_is_not_unsat(self):
        graph = bipyramid(fixed=True)
        for options in ({"c5_max_cycles": 0}, {"c5_max_scan_steps": 0}):
            with self.subTest(options=options):
                result = constraints.solve_constraints(graph, use_c5=True,
                                                        c5_scan_method="local", use_conflicts=False, **options)
                self.assertEqual(result["status"], "unsatisfiable")
                self.assertEqual(result["stats"]["c5_queries"], 0)
                self.assertGreater(result["stats"]["eliminations"], 0)
        result = constraints.solve_constraints(graph, use_c5=True,
                                                c5_scan_method="local", max_checks=0)
        self.assertEqual(result["status"], "limit")
        self.assertEqual(result["colors"], [-1] * 5 + [2, 3])
        self.assertEqual(result["stats"]["writebacks"], 0)

    def test_invalid_limits_and_scan_modes_are_rejected(self):
        for options in ({"max_cycles": -1}, {"max_steps": -1},
                        {"max_cycles": True}, {"max_steps": 1.5}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                c5.find_local_c5(wheel(), **options)
        with self.assertRaises(ValueError):
            constraints.solve_constraints(wheel(), use_c5=True, c5_scan_method="unknown")
        with self.assertRaises(ValueError):
            constraints.solve_constraints(wheel(), c5_scan_method="local")


if __name__ == "__main__":
    unittest.main()
