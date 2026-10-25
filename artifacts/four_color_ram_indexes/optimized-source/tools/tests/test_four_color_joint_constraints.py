"""A recorded original-subgraph relation must retain every original solution."""

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_conflict_priority import original_solutions
from four_color_joint_constraint_audit import instantiate_nine_point_constraint


MAPPING = dict(u=0, v=6, a=1, b=5, r0=2, r1=4, r2=7, r3=8, h=9)


def source_graph():
    cases = json.loads((ROOT / "artifacts/four_color_guarantee_gap/inputs.json").read_text())
    graph = deepcopy(next(case["graph"] for case in cases if case["role"] == "secondary-gap"))
    graph["fixed"] = []
    return graph


class RecordedJointConstraintTests(unittest.TestCase):
    def test_full_original_solution_projection_is_the_three_point_equality(self):
        graph = source_graph()
        before = deepcopy(graph)
        factor = instantiate_nine_point_constraint(graph, MAPPING)
        self.assertEqual(factor["frontier"], [0, 6, 9])
        positions = [graph["vertices"].index(vertex) for vertex in factor["frontier"]]
        solutions = list(original_solutions(graph))
        self.assertEqual(len(solutions), 48)
        projection = {tuple(row[index] for index in positions) for row in solutions}
        self.assertEqual({tuple(row) for row in factor["rows"]}, projection)
        self.assertEqual(projection, {(colour,) * 3 for colour in range(4)})
        for row in projection:
            self.assertEqual(sum(tuple(solution[index] for index in positions) == row
                                 for solution in solutions), 12)
        self.assertEqual({frozenset(edge) for edge in factor["source_edges"]},
                         {frozenset(edge) for edge in graph["edges"]})
        self.assertEqual(set(factor["source_vertices"]), set(graph["vertices"]))
        self.assertEqual(graph, before)

    def test_unequal_fixed_colours_filter_the_relation_without_rewriting_it(self):
        graph = source_graph()
        graph["fixed"] = [[0, 0], [6, 3]]
        before = deepcopy(graph)
        factor = instantiate_nine_point_constraint(graph, MAPPING)
        fixed = dict(graph["fixed"])
        compatible = [row for row in factor["rows"]
                      if all(vertex not in fixed or colour == fixed[vertex]
                             for vertex, colour in zip(factor["frontier"], row))]
        self.assertEqual(len(factor["rows"]), 4)
        self.assertEqual(compatible, [])
        self.assertEqual(list(original_solutions(graph)), [])
        self.assertEqual(graph, before)

    def test_every_required_edge_is_checked_before_emitting_the_relation(self):
        graph = source_graph()
        for missing in graph["edges"]:
            with self.subTest(missing=missing):
                reduced = dict(graph, edges=[edge for edge in graph["edges"] if edge != missing])
                self.assertIsNone(instantiate_nine_point_constraint(reduced, MAPPING))

    def test_role_mapping_survives_relabeling_and_vertex_order_changes(self):
        graph = source_graph()
        labels = dict(zip(graph["vertices"], [501, -21, 14, 770, 88, -402, 39, 7, 2200]))
        renamed = dict(vertices=list(reversed([labels[vertex] for vertex in graph["vertices"]])),
                       edges=[[labels[left], labels[right]] for left, right in graph["edges"]],
                       fixed=[])
        roles = {role: labels[vertex] for role, vertex in MAPPING.items()}
        factor = instantiate_nine_point_constraint(renamed, roles)
        self.assertEqual(factor["frontier"], [labels[0], labels[6], labels[9]])
        self.assertEqual(factor["rows"], [[colour] * 3 for colour in range(4)])
        self.assertEqual({frozenset(edge) for edge in factor["source_edges"]},
                         {frozenset(edge) for edge in renamed["edges"]})

    def test_extra_edges_and_attachments_preserve_only_a_necessary_relation(self):
        graph = source_graph()
        attached = dict(graph, vertices=graph["vertices"] + [100],
                        edges=graph["edges"] + [[9, 100]])
        attached.pop("positions", None)
        factor = instantiate_nine_point_constraint(attached, MAPPING)
        positions = [attached["vertices"].index(vertex) for vertex in factor["frontier"]]
        solutions = list(original_solutions(attached))
        self.assertEqual(len(solutions), 144)
        allowed = {tuple(row) for row in factor["rows"]}
        self.assertTrue(all(tuple(row[index] for index in positions) in allowed for row in solutions))

        blocked = dict(graph, edges=graph["edges"] + [[0, 6]])
        self.assertIsNotNone(instantiate_nine_point_constraint(blocked, MAPPING))
        self.assertEqual(list(original_solutions(blocked)), [])

    def test_invalid_role_maps_cannot_supply_an_original_subgraph_witness(self):
        graph = source_graph()
        invalid = [dict(MAPPING, v=MAPPING["u"]), dict(MAPPING, h=123456),
                   dict(MAPPING, u=True), {key: value for key, value in MAPPING.items() if key != "h"},
                   dict(MAPPING, outside=100)]
        for roles in invalid:
            with self.subTest(roles=roles), self.assertRaises(ValueError):
                instantiate_nine_point_constraint(graph, roles)


if __name__ == "__main__":
    unittest.main()
