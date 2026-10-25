"""Independent checks for whole-interface filtering and delayed reconstruction."""

from copy import deepcopy
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import four_color_constraints as constraints
from four_color_intersections import intersect_on_shared


def original_colorings(graph):
    """Enumerate only the original edges and literal fixed colors."""
    vertices = graph["vertices"]
    fixed = dict(graph.get("fixed", []))
    choices = [(fixed[v],) if v in fixed else range(4) for v in vertices]
    for colors in product(*choices):
        coloring = dict(zip(vertices, colors))
        if all(coloring[a] != coloring[b] for a, b in graph["edges"]):
            yield coloring


def two_tetrahedra():
    vertices = [90, -5, 17, 33, 0]
    cliques = [vertices[:4], [*vertices[:3], vertices[4]]]
    edges = {tuple(sorted(edge)) for clique in cliques
             for edge in combinations(clique, 2)}
    return {"vertices": vertices, "edges": [list(edge) for edge in sorted(edges)]}


def restricted_bipyramid(incompatible=False):
    # The hubs 3 and 4 see the same original triangle and hence must agree.
    # Original fixed leaves make the first hub's domain {0,1}.
    edges = [list(edge) for edge in combinations(range(3), 2)]
    edges += [[v, hub] for v in range(3) for hub in (3, 4)]
    edges += [[3, 5], [3, 6]]
    fixed = [[5, 2], [6, 3]]
    if incompatible:
        # The second hub's domain {2,3} is individually feasible, but cannot
        # share a complete triangle coloring with the first hub's domain.
        edges += [[4, 7], [4, 8]]
        fixed += [[7, 0], [8, 1]]
    return {"vertices": list(range(9 if incompatible else 7)),
            "edges": edges, "fixed": fixed}


class SharedInterfaceTests(unittest.TestCase):
    def test_common_vertices_keep_left_order_and_literal_column_identity(self):
        # Both private coordinates and the opposite interface column order
        # matter; intersecting raw tuples or sorting the shared scope is wrong.
        left = {(3, 0, 1), (2, 1, 0), (3, 2, 0), (0, 1, 3)}
        right = {(1, 2, 0), (0, 3, 1), (0, 2, 3)}
        answer = intersect_on_shared((90, -5, 17), left,
                                     (17, 44, -5), right)
        self.assertEqual(answer["scope"], (-5, 17))
        self.assertEqual(answer["common_rows"], frozenset({(0, 1), (1, 0)}))
        self.assertEqual(answer["left_rows"], frozenset({(3, 0, 1), (2, 1, 0)}))
        self.assertEqual(answer["right_rows"], frozenset({(1, 2, 0), (0, 3, 1)}))

    def test_pair_conflict_is_invisible_to_all_unary_supports(self):
        left = {(0, 1), (1, 0)}
        right = {(0, 0), (1, 1)}
        for column in range(2):
            self.assertEqual({row[column] for row in left}, {0, 1})
            self.assertEqual({row[column] for row in right}, {0, 1})
        answer = intersect_on_shared((8, 3), left, (8, 3), right)
        self.assertEqual(answer["common_rows"], frozenset())
        self.assertEqual(answer["left_rows"], frozenset())
        self.assertEqual(answer["right_rows"], frozenset())

    def test_multiple_surviving_interface_rows_do_not_require_uniqueness(self):
        left = {(0, 1), (0, 2), (1, 2)}
        right = {(0, 2), (1, 2), (3, 0)}
        answer = intersect_on_shared((4, 9), left, (4, 9), right)
        surviving = frozenset({(0, 2), (1, 2)})
        self.assertEqual(answer["common_rows"], surviving)
        self.assertEqual(answer["left_rows"], surviving)
        self.assertEqual(answer["right_rows"], surviving)

    def test_three_point_intersection_keeps_correlations_beyond_all_pairs(self):
        left = {row for row in product(range(2), repeat=3) if sum(row) % 2 == 0}
        right = {row for row in product(range(2), repeat=3) if sum(row) % 2 == 1}
        for columns in combinations(range(3), 2):
            self.assertEqual({tuple(row[i] for i in columns) for row in left},
                             {tuple(row[i] for i in columns) for row in right})
        answer = intersect_on_shared((9, -2, 40), left, (9, -2, 40), right)
        self.assertEqual(answer["scope"], (9, -2, 40))
        self.assertFalse(answer["common_rows"])
        self.assertFalse(answer["left_rows"])
        self.assertFalse(answer["right_rows"])

    def test_disjoint_scopes_and_empty_relation_have_existential_semantics(self):
        answer = intersect_on_shared((7,), {(0,), (1,)}, (-4,), {(2,)})
        self.assertEqual(answer["scope"], ())
        self.assertEqual(answer["common_rows"], frozenset({()}))
        self.assertEqual(answer["left_rows"], frozenset({(0,), (1,)}))
        self.assertEqual(answer["right_rows"], frozenset({(2,)}))
        for left, right in ((set(), {(2,)}), ({(0,)}, set()), (set(), set())):
            with self.subTest(left=left, right=right):
                answer = intersect_on_shared((7,), left, (-4,), right)
                self.assertEqual(answer["common_rows"], frozenset())
                self.assertEqual(answer["left_rows"], frozenset())
                self.assertEqual(answer["right_rows"], frozenset())
        answer = intersect_on_shared((), {()}, (7,), {(3,)})
        self.assertEqual(answer["common_rows"], frozenset({()}))
        self.assertEqual(answer["right_rows"], frozenset({(3,)}))

    def test_budget_callback_interrupts_without_mutating_either_input(self):
        left = {(0, 1, 2), (0, 2, 1), (1, 2, 3)}
        right = {(2, 1, 3), (1, 2, 0), (0, 3, 1)}
        before = deepcopy((left, right))
        charges = []
        expected = intersect_on_shared((1, 2, 3), left, (3, 2, 4), right,
                                       charge=lambda: charges.append(None))
        self.assertGreater(len(charges), 0)

        class Interrupted(Exception):
            pass

        # Interrupt before every operation in turn, including the last one.
        for stop_at in range(len(charges)):
            visited = 0

            def charge():
                nonlocal visited
                if visited == stop_at:
                    raise Interrupted
                visited += 1

            with self.subTest(stop_at=stop_at):
                with self.assertRaises(Interrupted):
                    intersect_on_shared((1, 2, 3), left, (3, 2, 4), right,
                                        charge=charge)
                self.assertEqual((left, right), before)
        self.assertEqual(intersect_on_shared((1, 2, 3), left, (3, 2, 4), right),
                         expected)

    def test_cyclic_local_support_is_not_a_global_satisfiability_verdict(self):
        # Every edge of a two-color triangle supports both endpoint colors.
        # All neighboring full-interface intersections are nonempty and stable,
        # but no common coloring of the three original vertices exists.
        scopes = [(0, 1), (1, 2), (2, 0)]
        edge_rows = frozenset({(0, 1), (1, 0)})
        for i, j in combinations(range(3), 2):
            answer = intersect_on_shared(scopes[i], edge_rows, scopes[j], edge_rows)
            self.assertTrue(answer["common_rows"])
            self.assertEqual(answer["left_rows"], edge_rows)
            self.assertEqual(answer["right_rows"], edge_rows)
        self.assertFalse(any(all(colors[a] != colors[b] for a, b in scopes)
                             for colors in product(range(2), repeat=3)))


class IntersectionSolverTests(unittest.TestCase):
    def assert_valid_witness(self, graph, colors):
        self.assertEqual(len(colors), len(graph["vertices"]))
        self.assertTrue(all(type(color) is int and 0 <= color < 4 for color in colors))
        coloring = dict(zip(graph["vertices"], colors))
        self.assertTrue(all(coloring[a] != coloring[b] for a, b in graph["edges"]))
        self.assertTrue(all(coloring[v] == color for v, color in graph.get("fixed", [])))

    def assert_oracle_agreement(self, graph, **options):
        exists = next(original_colorings(graph), None) is not None
        result = constraints.solve_constraints(graph, use_intersections=True, **options)
        self.assertTrue(result["use_intersections"])
        self.assertEqual(result["status"], "colored" if exists else "unsatisfiable")
        if exists:
            self.assert_valid_witness(graph, result["colors"])
        return result

    def test_all_1024_five_vertex_graphs_against_direct_original_edges(self):
        possible = list(combinations(range(5), 2))
        for mask in range(1 << len(possible)):
            graph = {"vertices": list(range(5)),
                     "edges": [list(edge) for i, edge in enumerate(possible)
                               if mask & (1 << i)]}
            with self.subTest(mask=mask):
                self.assert_oracle_agreement(graph, use_conflicts=False,
                                             record_relations=False, trace_limit=0)

    def test_partial_fixed_contexts_in_both_template_modes(self):
        graph = two_tetrahedra()
        for a, b in product(range(4), repeat=2):
            for templates in (False, True):
                case = deepcopy(graph)
                case["fixed"] = [[90, a], [-5, b]]
                with self.subTest(fixed=case["fixed"], templates=templates):
                    self.assert_oracle_agreement(case, use_substructures=templates,
                                                 use_conflicts=False)

    def test_every_complete_original_coloring_survives_saved_records(self):
        cycle = {"vertices": [7, 11, 2, 40, -3],
                 "edges": [[7, 11], [11, 2], [2, 40], [40, -3], [-3, 7]],
                 "fixed": [[7, 3]]}
        for graph in (two_tetrahedra(), cycle, restricted_bipyramid()):
            colorings = list(original_colorings(graph))
            self.assertGreater(len(colorings), 1)
            for templates in (False, True):
                result = self.assert_oracle_agreement(graph, use_substructures=templates,
                                                     use_conflicts=False)
                for record in result["elimination_records"]:
                    with self.subTest(graph=graph, templates=templates,
                                      vertex=record["vertex"]):
                        rows = {tuple(row["boundary"]): set(row["colors"])
                                for row in record["rows"]}
                        self.assertEqual(len(rows), len(record["rows"]))
                        domains = {entry["vertex"]: set(entry["colors"])
                                   for entry in record["source_domains"]}
                        inputs = [(relation["scope"], {tuple(row) for row in relation["rows"]})
                                  for relation in record["input_relations"]]
                        for coloring in colorings:
                            self.assertTrue(all(coloring[v] in allowed
                                                for v, allowed in domains.items()))
                            for scope, allowed in inputs:
                                self.assertIn(tuple(coloring[v] for v in scope), allowed)
                            boundary = tuple(coloring[v] for v in record["scope"])
                            self.assertIn(boundary, rows)
                            self.assertIn(coloring[record["vertex"]], rows[boundary])

    def test_real_interface_pruning_propagates_hub_domain_before_elimination(self):
        graph = restricted_bipyramid()
        result = self.assert_oracle_agreement(graph, use_conflicts=False)
        self.assertGreater(result["stats"]["intersection_prunes"], 0)
        first_elimination = next(event for event in result["events"]
                                 if event["kind"] == "eliminate")
        self.assertEqual(first_elimination["domains"][3], [0, 1])
        self.assertEqual(first_elimination["domains"][4], [0, 1])
        self.assertEqual(first_elimination["colors"], [-1] * 5 + [2, 3])

    def test_incompatible_hub_domains_are_rejected_before_any_elimination(self):
        graph = restricted_bipyramid(incompatible=True)
        self.assertIsNone(next(original_colorings(graph), None))
        baseline = constraints.solve_constraints(graph, use_conflicts=False)
        result = self.assert_oracle_agreement(graph, use_conflicts=False)
        self.assertEqual(baseline["status"], "unsatisfiable")
        self.assertGreater(baseline["stats"]["eliminations"], 0)
        self.assertEqual(result["stats"]["eliminations"], 0)
        self.assertGreater(result["stats"]["intersection_prunes"], 0)
        self.assertEqual(result["colors"], [-1] * 5 + [2, 3, 0, 1])
        self.assertFalse(any(event["phase"] == "writeback" for event in result["events"]))

    def test_multiple_solutions_reconstruct_one_after_all_eliminations(self):
        graph = two_tetrahedra()
        graph["fixed"] = [[90, 2]]
        self.assertGreater(len(list(original_colorings(graph))), 1)
        result = self.assert_oracle_agreement(graph, use_conflicts=False)
        fixed_colors = [dict(graph["fixed"]).get(v, -1) for v in graph["vertices"]]
        wrote = False
        for event in result["events"]:
            if event["phase"] == "reduce":
                self.assertEqual(event["colors"], fixed_colors)
            if event["phase"] == "writeback":
                wrote = True
                self.assertEqual(set(event["eliminated_vertices"]), set(graph["vertices"]))
        self.assertTrue(wrote)
        self.assertEqual(result["stats"]["decisions"], 0)
        self.assertEqual(result["stats"]["backtracks"], 0)

    def test_additional_intersection_work_obeys_limit_without_early_coloring(self):
        graph = two_tetrahedra()
        options = dict(use_conflicts=False, record_relations=False)
        plain = constraints.solve_constraints(graph, **options)
        full = constraints.solve_constraints(graph, use_intersections=True, **options)
        self.assertEqual(plain["status"], "colored")
        self.assertEqual(full["status"], "colored")
        self.assertGreater(full["stats"]["intersection_checks"], 0)
        self.assertGreater(full["stats"]["intersection_pairs"], 0)
        # Here both initial K4 tables project to the same triangle table, so
        # filtering saves no work and its own operations add measurable cost.
        self.assertGreater(full["stats"]["checks"], plain["stats"]["checks"])
        limit = plain["stats"]["checks"]
        limited = constraints.solve_constraints(graph, use_intersections=True,
                                                max_checks=limit, **options)
        self.assertEqual(limited["status"], "limit")
        self.assertEqual(limited["colors"], [-1] * len(graph["vertices"]))
        self.assertLessEqual(limited["stats"]["checks"], limit)
        self.assertFalse(any(event["phase"] == "writeback" for event in limited["events"]))
        zero = constraints.solve_constraints(graph, use_intersections=True,
                                             max_checks=0, **options)
        self.assertEqual(zero["status"], "limit")
        self.assertEqual(zero["colors"], [-1] * len(graph["vertices"]))

    def test_trace_limits_preserve_work_records_and_deterministic_witness(self):
        graph = two_tetrahedra()
        graph["fixed"] = [[90, 2]]
        before = deepcopy(graph)
        full = self.assert_oracle_agreement(graph, use_conflicts=False)
        for trace_limit in (0, 1, 3):
            with self.subTest(trace_limit=trace_limit):
                short = constraints.solve_constraints(graph, use_intersections=True,
                                                      use_conflicts=False,
                                                      trace_limit=trace_limit)
                for field in ("status", "colors", "stats", "elimination_records", "event_count"):
                    self.assertEqual(short[field], full[field])
                self.assertLessEqual(len(short["events"]), trace_limit)
                self.assertTrue(short["trace_truncated"])
        self.assertEqual(graph, before)

    def test_cli_intersections_flag_runs_enabled_constraint_engine(self):
        graph = two_tetrahedra()
        script = Path(__file__).resolve().parents[2] / "scripts" / "four_color_lab.py"
        with TemporaryDirectory() as directory:
            source = Path(directory) / "graph.json"
            output = Path(directory) / "result.json"
            source.write_text(json.dumps(graph))
            completed = subprocess.run(
                [sys.executable, str(script), "solve", str(source),
                 "--engine", "constraints", "--intersections", "--trace-limit", "0",
                 "--json", str(output)],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(output.read_text())
            self.assertTrue(result["use_intersections"])
            self.assertEqual(result["status"], "colored")
            self.assert_valid_witness(graph, result["colors"])
            self.assertEqual(json.loads(completed.stdout)["colors"], result["colors"])


if __name__ == "__main__":
    unittest.main()
