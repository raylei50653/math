"""Independent literal-row, induced-cycle, and joint C5 propagation checks."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import four_color_c5 as c5
import four_color_constraints as constraints


def complete(n):
    return {"vertices": list(range(n)),
            "edges": [list(edge) for edge in combinations(range(n), 2)]}


def cycle_graph(labels=(0, 1, 2, 3, 4)):
    return {"vertices": list(labels),
            "edges": [[labels[i], labels[(i + 1) % 5]] for i in range(5)]}


def proper_assignments(graph):
    fixed = dict(graph.get("fixed", []))
    options = [(fixed[v],) if v in fixed else range(4) for v in graph["vertices"]]
    for row in product(*options):
        coloring = dict(zip(graph["vertices"], row))
        if all(coloring[u] != coloring[v] for u, v in graph["edges"]):
            yield coloring


def normalized_pattern(row):
    labels = {}
    return tuple(labels.setdefault(color, len(labels)) for color in row)


def brute_induced_cycles(graph):
    """Inspect five-vertex subsets and all cyclic orders, not a DFS finder."""
    edges = {frozenset(edge) for edge in graph["edges"]}
    positions = {v: i for i, v in enumerate(graph["vertices"])}
    answer = set()
    for subset in combinations(graph["vertices"], 5):
        induced = {edge for edge in edges if edge <= set(subset)}
        if len(induced) != 5:
            continue
        orders = [order for order in permutations(subset)
                  if {frozenset((order[i], order[(i + 1) % 5]))
                      for i in range(5)} == induced]
        if orders:
            answer.add(min(orders, key=lambda row: tuple(positions[v] for v in row)))
    return answer


def subset_degree_cycle_oracle(graph):
    """Independent subset oracle, using the degree-two connected criterion."""
    positions = {v: i for i, v in enumerate(graph["vertices"])}
    adjacency = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        adjacency[u].add(v)
        adjacency[v].add(u)
    cycles = []
    for subset in combinations(graph["vertices"], 5):
        selected = set(subset)
        induced = {v: adjacency[v] & selected for v in subset}
        if any(len(neighbors) != 2 for neighbors in induced.values()):
            continue
        start = subset[0]
        first = min(induced[start], key=positions.__getitem__)
        order = [start]
        previous, current = start, first
        while current not in order:
            order.append(current)
            following, = induced[current] - {previous}
            previous, current = current, following
        if len(order) == 5 and current == start:
            cycles.append(tuple(order))
    return sorted(cycles, key=lambda row: tuple(positions[v] for v in row))


class C5ConstraintTests(unittest.TestCase):
    def assert_query(self, masks):
        result = c5.query_c5(tuple(masks))
        allowed = [(i, row) for i, row in enumerate(c5.C5_ROWS)
                   if all(mask & (1 << color) for mask, color in zip(masks, row))]
        bits = sum(1 << i for i, _ in allowed)
        supports = [0] * 5
        for _, row in allowed:
            for column, color in enumerate(row):
                supports[column] |= 1 << color
        self.assertEqual(result["allowed_bits"], bits, masks)
        self.assertEqual(result["row_count"], len(allowed), masks)
        self.assertEqual(result["supports"], supports, masks)
        self.assertGreaterEqual(result["op_count"], 0)
        self.assertLessEqual(result["op_count"], 26)

    def assert_solver_agreement(self, graph, use_c5=True):
        coloring = next(proper_assignments(graph), None)
        result = constraints.solve_constraints(graph, use_c5=use_c5,
                                                record_relations=False, trace_limit=0)
        self.assertEqual(result["status"], "colored" if coloring is not None
                         else "unsatisfiable")
        if coloring is not None:
            actual = dict(zip(graph["vertices"], result["colors"]))
            self.assertTrue(all(type(color) is int and color in range(4)
                                for color in actual.values()))
            self.assertTrue(all(actual[u] != actual[v] for u, v in graph["edges"]))
            self.assertTrue(all(actual[v] == color for v, color in graph.get("fixed", [])))
        return result

    def test_240_literal_rows_and_ten_complete_equality_pattern_classes(self):
        expected = tuple(row for row in product(range(4), repeat=5)
                         if all(row[i] != row[(i + 1) % 5] for i in range(5)))
        self.assertIsInstance(c5.C5_ROWS, tuple)
        self.assertTrue(all(isinstance(row, tuple) for row in c5.C5_ROWS))
        self.assertEqual(c5.C5_ROWS, expected)
        self.assertEqual(len(expected), 240)
        patterns = Counter(normalized_pattern(row) for row in expected)
        self.assertEqual(len(patterns), 10)
        self.assertEqual(set(patterns.values()), {24})
        catalogue = c5.c5_catalogue()
        self.assertEqual(catalogue["rows"], [list(row) for row in expected])
        self.assertEqual({tuple(row) for row in catalogue["normalized_equality_patterns"]},
                         set(patterns))
        covered = []
        for group in catalogue["pattern_classes"]:
            indices = group["row_indices"]
            self.assertEqual(group["row_count"], 24)
            self.assertEqual(len(indices), 24)
            self.assertEqual({normalized_pattern(expected[index]) for index in indices},
                             {tuple(group["pattern"])})
            covered.extend(indices)
        self.assertEqual(sorted(covered), list(range(240)))

    def test_bitset_queries_match_independent_scan_for_3125_structured_domains(self):
        for masks in product((0, 1, 3, 7, 15), repeat=5):
            self.assert_query(masks)

    def test_singleton_and_seeded_irregular_domain_queries(self):
        for colors in product(range(4), repeat=5):
            self.assert_query(tuple(1 << color for color in colors))
        rng = random.Random(20261025)
        for _ in range(256):
            self.assert_query(tuple(rng.randrange(16) for _ in range(5)))

    def test_finder_and_solver_on_all_1024_five_vertex_graphs(self):
        possible = list(combinations(range(5), 2))
        for mask in range(1 << len(possible)):
            graph = {"vertices": list(range(5)),
                     "edges": [list(edge) for i, edge in enumerate(possible)
                               if mask & (1 << i)]}
            with self.subTest(mask=mask):
                result = c5.find_induced_c5(graph)
                self.assertTrue(result["complete"])
                self.assertFalse(result["truncated"])
                self.assertEqual({tuple(cycle) for cycle in result["cycles"]},
                                 brute_induced_cycles(graph))
                self.assertEqual(len(result["cycles"]), len(set(map(tuple, result["cycles"]))))
                self.assert_solver_agreement(graph)

    def test_detector_with_relabelings_chords_and_multiple_cycles(self):
        rng = random.Random(51)
        graphs = []
        for _ in range(20):
            labels = rng.sample(range(-30, 50), 7)
            graphs.append({"vertices": labels,
                           "edges": [list(edge) for edge in combinations(labels, 2)
                                     if rng.random() < 0.45]})
        graph = cycle_graph((11, -2, 90, 8, 3))
        graph["vertices"] = [90, 3, 11, 8, -2]
        graphs.append(graph)
        chorded = cycle_graph()
        chorded["edges"].append([0, 2])
        self.assertEqual(c5.find_induced_c5(chorded)["cycles"], [])
        two_cycles = {"vertices": list(range(10)),
                      "edges": cycle_graph()["edges"]
                               + cycle_graph((5, 6, 7, 8, 9))["edges"]}
        graphs.append(two_cycles)
        for graph in graphs:
            with self.subTest(graph=graph):
                result = c5.find_induced_c5(graph)
                self.assertTrue(result["complete"])
                self.assertEqual({tuple(row) for row in result["cycles"]},
                                 brute_induced_cycles(graph))
                self.assertEqual(len(result["cycles"]), len(set(map(tuple, result["cycles"]))))

    def test_detector_exhaustively_matches_all_32768_six_vertex_graphs(self):
        possible = list(combinations(range(6), 2))
        for mask in range(1 << len(possible)):
            graph = {"vertices": list(range(6)),
                     "edges": [list(edge) for i, edge in enumerate(possible)
                               if mask & (1 << i)]}
            with self.subTest(mask=mask):
                result = c5.find_induced_c5(graph)
                self.assertTrue(result["complete"])
                self.assertFalse(result["truncated"])
                self.assertEqual(list(map(tuple, result["cycles"])),
                                 subset_degree_cycle_oracle(graph))

    def test_cycle_and_step_caps_preserve_the_canonical_complete_prefix(self):
        # Independent twins replace each vertex of C5.  An induced C5 must
        # use one vertex from each part; there are exactly 3**5 such cycles.
        parts = [list(range(3 * i, 3 * i + 3)) for i in range(5)]
        graph = {"vertices": list(range(15)),
                 "edges": [[u, v] for i in range(5)
                           for u in parts[i] for v in parts[(i + 1) % 5]]}
        expected = subset_degree_cycle_oracle(graph)
        self.assertEqual(len(expected), 3 ** 5)
        full = c5.find_induced_c5(graph, max_cycles=1000, max_steps=1000000)
        self.assertTrue(full["complete"])
        self.assertEqual(list(map(tuple, full["cycles"])), expected)
        for cap in (0, 1, 2, 7, 128, len(expected), len(expected) + 1):
            with self.subTest(cycle_cap=cap):
                result = c5.find_induced_c5(graph, max_cycles=cap, max_steps=1000000)
                self.assertEqual(list(map(tuple, result["cycles"])), expected[:cap])
                self.assertEqual(result["complete"], cap > len(expected))
                self.assertEqual(result["truncated"], cap <= len(expected))
        for cap in (0, 1, 2, 3, 10, full["steps"] // 2,
                    full["steps"] - 1, full["steps"], full["steps"] + 1):
            with self.subTest(step_cap=cap):
                result = c5.find_induced_c5(graph, max_cycles=1000, max_steps=cap)
                count = len(result["cycles"])
                self.assertEqual(list(map(tuple, result["cycles"])), expected[:count])
                self.assertLessEqual(result["steps"], cap)
                self.assertEqual(result["truncated"], not result["complete"])
                if cap < full["steps"]:
                    self.assertFalse(result["complete"])
                else:
                    self.assertTrue(result["complete"])
                    self.assertEqual(count, len(expected))

    def test_sparse_bipartite_and_high_degree_graphs_have_no_induced_c5(self):
        cases = [
            {"vertices": list(range(201)), "edges": [[0, v] for v in range(1, 201)]},
            {"vertices": list(range(127)),
             "edges": [[(v - 1) // 2, v] for v in range(1, 127)]},
            {"vertices": list(range(80)),
             "edges": [[u, v] for u in range(40) for v in range(40, 80)]},
            complete(80),
        ]
        for graph in cases:
            with self.subTest(vertices=len(graph["vertices"]), edges=len(graph["edges"])):
                result = c5.find_induced_c5(graph, max_steps=1000000)
                self.assertTrue(result["complete"])
                self.assertEqual(result["cycles"], [])

    def test_detector_preserves_order_under_nonmonotone_integer_relabeling(self):
        graph = {"vertices": list(range(8)),
                 "edges": cycle_graph()["edges"]
                          + [[0, 5], [5, 6], [6, 7], [7, 1]]}
        labels = [90, -4, 17, 0, 51, -100, 8, 3]
        mapping = dict(zip(graph["vertices"], labels))
        relabeled = {"vertices": labels,
                     "edges": [[mapping[u], mapping[v]] for u, v in graph["edges"]]}
        original = c5.find_induced_c5(graph)
        renamed = c5.find_induced_c5(relabeled)
        self.assertTrue(original["complete"] and renamed["complete"])
        self.assertEqual(list(map(tuple, renamed["cycles"])),
                         [tuple(mapping[v] for v in cycle) for cycle in original["cycles"]])
        self.assertEqual(list(map(tuple, renamed["cycles"])),
                         subset_degree_cycle_oracle(relabeled))

    def test_finder_caps_are_incomplete_and_keep_only_real_cycles(self):
        graph = {"vertices": list(range(10)),
                 "edges": cycle_graph()["edges"]
                          + cycle_graph((5, 6, 7, 8, 9))["edges"]}
        all_cycles = brute_induced_cycles(graph)
        for options in ({"max_cycles": 0}, {"max_cycles": 1},
                        {"max_steps": 0}, {"max_steps": 1}):
            with self.subTest(options=options):
                result = c5.find_induced_c5(graph, **options)
                self.assertFalse(result["complete"])
                self.assertTrue(result["truncated"])
                self.assertTrue({tuple(row) for row in result["cycles"]} <= all_cycles)
                self.assertLessEqual(result["steps"], options.get("max_steps", 200000))
                self.assertLessEqual(len(result["cycles"]), options.get("max_cycles", 128))

    def test_joint_c5_detects_fixed_bipyramid_before_elimination_or_writeback(self):
        graph = {"vertices": list(range(7)),
                 "edges": cycle_graph()["edges"]
                          + [[u, hub] for u in range(5) for hub in (5, 6)],
                 "fixed": [[5, 2], [6, 3]]}
        # Isolate indexed C5 inference from the separately tested motif guards.
        result = constraints.solve_constraints(graph, use_c5=True, use_conflicts=False)
        self.assertEqual(result["status"], "unsatisfiable")
        self.assertEqual(result["colors"], [-1] * 5 + [2, 3])
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertEqual(result["stats"]["writebacks"], 0)
        self.assertGreater(result["stats"]["c5_conflicts"], 0)
        self.assert_solver_agreement(graph, use_c5=False)
        free = {key: value for key, value in graph.items() if key != "fixed"}
        self.assert_solver_agreement(free, use_c5=True)

    def test_c5_prunes_preserve_every_global_coloring_and_original_edges(self):
        # Four rim domains are {0,1}; the fifth is {0,1,2}.  Only the joint
        # cycle forces the fifth to 2 before variable elimination.
        graph = {"vertices": list(range(7)),
                 "edges": cycle_graph()["edges"]
                          + [[u, 6] for u in range(5)]
                          + [[u, 5] for u in range(4)],
                 "fixed": [[5, 2], [6, 3]]}
        result = constraints.solve_constraints(graph, use_c5=True)
        self.assertEqual(result["status"], "colored")
        self.assertGreater(result["stats"]["c5_prunes"], 0)
        self.assertGreater(result["stats"]["c5_skips"], 0)
        self.assertGreater(result["stats"]["c5_inactive_skips"], 0)
        global_colorings = list(proper_assignments(graph))
        self.assertTrue(global_colorings)
        edges = {frozenset(edge) for edge in graph["edges"]}
        lookups = [event for event in result["events"] if event["kind"] == "c5_lookup"]
        self.assertTrue(lookups)
        for event in lookups:
            self.assertEqual(event["phase"], "reduce")
            self.assertEqual(event["colors"], [-1] * 5 + [2, 3])
            self.assertEqual(event["relation_kind"], "c5")
            self.assertEqual(len(event["frontier"]), 5)
            self.assertFalse(set(event["frontier"]) & set(event["eliminated_vertices"]))
            self.assertTrue(all(frozenset(edge) in edges for edge in event["causal_edges"]))
            for coloring in global_colorings:
                self.assertTrue(all(coloring[v] in event["domains"][i]
                                    for i, v in enumerate(graph["vertices"])))
        self.assert_solver_agreement(graph, use_c5=False)

    def test_interrupted_index_query_does_not_commit_partial_domain_supports(self):
        graph = {"vertices": list(range(7)),
                 "edges": cycle_graph()["edges"]
                          + [[u, 6] for u in range(5)]
                          + [[u, 5] for u in range(4)],
                 "fixed": [[5, 2], [6, 3]]}
        full = constraints.solve_constraints(graph, use_c5=True)
        lookup = next(event for event in full["events"] if event["kind"] == "c5_lookup")
        # Interrupt immediately before the last indexed operation in the
        # first query that would otherwise remove candidate colors.
        budget = lookup["stats"]["checks"] - 1
        limited = constraints.solve_constraints(graph, use_c5=True, max_checks=budget)
        self.assertEqual(limited["status"], "limit")
        self.assertEqual(limited["stats"]["checks"], budget)
        self.assertEqual(limited["stats"]["c5_queries"], 1)
        self.assertEqual(limited["stats"]["c5_index_ops"], 25)
        self.assertEqual(limited["stats"]["c5_prunes"], 0)
        self.assertEqual(limited["stats"]["writebacks"], 0)
        self.assertEqual(limited["colors"], [-1] * 5 + [2, 3])
        last = limited["events"][-1]
        positions = {v: i for i, v in enumerate(graph["vertices"])}
        actual = [sum(1 << color for color in last["domains"][positions[v]])
                  for v in lookup["frontier"]]
        self.assertEqual(actual, lookup["domain_masks"])

    def test_truncated_cycle_discovery_still_allows_exact_base_solver(self):
        graph = cycle_graph()
        for options in ({"c5_max_cycles": 0}, {"c5_max_scan_steps": 1}):
            with self.subTest(options=options):
                result = constraints.solve_constraints(graph, use_c5=True, **options)
                self.assertEqual(result["status"], "colored")
                self.assertFalse(result["substructures"]["c5_scan_complete"])
                self.assertTrue(result["substructures"]["c5_scan_truncated"])
                self.assertEqual(result["stats"]["c5_queries"], 0)

    def test_c5_on_off_agree_on_seeded_seven_vertex_graphs(self):
        rng = random.Random(123)
        possible = list(combinations(range(7), 2))
        for case in range(20):
            graph = {"vertices": list(range(7)),
                     "edges": [list(edge) for edge in possible if rng.random() < 0.6],
                     "fixed": [[0, rng.randrange(4)], [6, rng.randrange(4)]]}
            with self.subTest(case=case):
                off = self.assert_solver_agreement(graph, use_c5=False)
                on = self.assert_solver_agreement(graph, use_c5=True)
                self.assertEqual(off["status"], on["status"])

    def test_c5_propagator_does_not_enlarge_elimination_frontiers(self):
        graph = cycle_graph((8, -4, 21, 0, 90))
        off = constraints.solve_constraints(graph, use_c5=False)
        on = constraints.solve_constraints(graph, use_c5=True)
        self.assertEqual(off["status"], "colored")
        self.assertEqual(on["status"], "colored")
        self.assertGreater(on["stats"]["c5_queries"], 0)
        self.assertEqual(off["stats"]["peak_scope"], on["stats"]["peak_scope"])
        self.assertLess(on["stats"]["peak_scope"], 5)
        self.assertEqual([(record["vertex"], record["scope"])
                          for record in off["elimination_records"]],
                         [(record["vertex"], record["scope"])
                          for record in on["elimination_records"]])

    def test_malformed_masks_and_options_are_rejected(self):
        for masks in (None, (), (15,) * 4, (15,) * 6,
                      (-1, 15, 15, 15, 15), (16, 15, 15, 15, 15),
                      (True, 15, 15, 15, 15), (1.0, 15, 15, 15, 15)):
            with self.subTest(masks=masks), self.assertRaises(ValueError):
                c5.query_c5(masks)
        for options in ({"max_cycles": -1}, {"max_steps": -1},
                        {"max_cycles": True}, {"max_steps": 1.5}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                c5.find_induced_c5(cycle_graph(), **options)
        with self.assertRaises(ValueError):
            constraints.solve_constraints(cycle_graph(), use_c5=1)


if __name__ == "__main__":
    unittest.main()
