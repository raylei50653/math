"""Check named C5 edge exchanges against independent complete colourings."""
from copy import deepcopy
from itertools import product
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import c5_cell_transform as transform  # noqa: E402


PATTERNS = (
    '01012', '01021', '01023', '01201', '01202',
    '01203', '01212', '01213', '01231', '01232',
)
CYCLE = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]
ORIGINAL = {
    'vertices': list(range(10)),
    'boundary': list(range(5)),
    'edges': CYCLE + [
        (2, 6), (3, 6), (4, 6), (0, 7), (1, 7), (4, 7),
        (4, 8), (1, 9), (2, 9), (5, 6), (5, 7), (5, 8),
        (5, 9), (6, 8), (6, 9), (7, 8), (7, 9),
    ],
}
ADD = (3, 8)
REMOVE = (4, 6)


def edge_set(graph):
    return {tuple(sorted(edge)) for edge in graph['edges']}


def brute_rows(graph):
    """Enumerate all four-colour assignments without using production helpers."""
    vertices = sorted(graph['vertices'])
    boundary = graph['boundary']
    inner = [vertex for vertex in vertices if vertex not in boundary]
    result = {}
    for pattern in PATTERNS:
        accepted = set()
        fixed = dict(zip(boundary, map(int, pattern)))
        for assignment in product(range(4), repeat=len(inner)):
            coloring = dict(fixed)
            coloring.update(zip(inner, assignment))
            if all(coloring[u] != coloring[v] for u, v in graph['edges']):
                accepted.add(tuple(coloring[v] for v in vertices))
        result[pattern] = accepted
    return result


def report_rows(state):
    return {row['pattern']: {tuple(lift) for lift in row['lifts']}
            for row in state['rows']}


class CellTransformTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = transform.analyze(deepcopy(ORIGINAL))
        cls.added = transform.analyze(deepcopy(ORIGINAL), add=ADD)
        cls.deleted = transform.analyze(deepcopy(ORIGINAL), remove=REMOVE)
        cls.flipped = transform.analyze(
            deepcopy(ORIGINAL), add=ADD, remove=REMOVE, require_flip=True)

    def assert_complete_state(self, state, expected_sigma):
        expected = brute_rows(state['graph'])
        self.assertEqual([row['pattern'] for row in state['rows']], list(PATTERNS))
        self.assertEqual(report_rows(state), expected)
        for row in state['rows']:
            self.assertEqual(row['count'], len(expected[row['pattern']]))
            self.assertEqual(len(row['lifts']), len(expected[row['pattern']]))
        independent_sigma = sum(1 << index for index, pattern in enumerate(PATTERNS)
                                if expected[pattern])
        self.assertEqual(state['sigma'], independent_sigma)
        self.assertEqual(state['sigma'], expected_sigma)

    def test_four_stages_retain_every_row_and_full_lift(self):
        for name, report, mask in (
            ('original', self.original, 891),
            ('add_only', self.added, 603),
            ('delete_only', self.deleted, 1019),
            ('flip', self.flipped, 987),
        ):
            with self.subTest(stage=name):
                self.assert_complete_state(report['source'], 891)
                self.assert_complete_state(report['result'], mask)

    def test_disk_and_planarity_distinguish_intermediate_from_flip(self):
        for report in (self.original, self.deleted, self.flipped):
            self.assertTrue(report['result']['topology']['planar'])
            self.assertTrue(report['result']['topology']['disk'])
        self.assertFalse(self.added['result']['topology']['planar'])
        self.assertFalse(self.added['result']['topology']['disk'])
        self.assertTrue(self.flipped['flip']['valid'])

    def test_added_edge_removes_two_patterns(self):
        self.assertEqual(self.added['lost_patterns'], ['01203', '01231'])
        self.assertEqual(self.added['gained_patterns'], [])
        self.assertFalse(self.added['sigma_preserved'])
        before = {row['pattern']: row['count'] for row in self.added['source']['rows']}
        after = {row['pattern']: row['count'] for row in self.added['result']['rows']}
        for pattern in ('01203', '01231'):
            self.assertEqual(before[pattern], 1)
            self.assertEqual(after[pattern], 0)

    def test_flip_changes_relation_and_reverse_restores_exact_graph(self):
        self.assertEqual(self.flipped['lost_patterns'], ['01203'])
        self.assertEqual(self.flipped['gained_patterns'], ['01213'])
        self.assertFalse(self.flipped['sigma_preserved'])
        final_graph = self.flipped['result_graph']
        self.assertEqual(edge_set(final_graph), (edge_set(ORIGINAL) - {REMOVE}) | {ADD})
        reverse = transform.analyze(final_graph, add=REMOVE, remove=ADD, require_flip=True)
        self.assertTrue(reverse['flip']['valid'])
        self.assertEqual(edge_set(reverse['result_graph']), edge_set(ORIGINAL))
        self.assert_complete_state(reverse['result'], 891)

    def test_joint_fibres_use_the_same_full_coloring(self):
        common_graph = deepcopy(ORIGINAL)
        common_graph['edges'] = sorted(edge_set(ORIGINAL) - {REMOVE})
        expected_rows = brute_rows(common_graph)
        source_rows = report_rows(self.flipped['source'])
        final_rows = report_rows(self.flipped['result'])
        intersection_rows = report_rows(self.added['result'])
        rows = self.flipped['joint_rows']
        self.assertEqual([row['pattern'] for row in rows], list(PATTERNS))
        for row in rows:
            pattern = row['pattern']
            expected = {key: set() for key in ('00', '01', '10', '11')}
            for lift in expected_rows[pattern]:
                removed_neq = int(lift[REMOVE[0]] != lift[REMOVE[1]])
                added_neq = int(lift[ADD[0]] != lift[ADD[1]])
                expected[f'{removed_neq}{added_neq}'].add(lift)
            actual = {key: {tuple(lift) for lift in fibre['lifts']}
                      for key, fibre in row['fibres'].items()}
            self.assertEqual(actual, expected)
            for key, fibre in row['fibres'].items():
                self.assertEqual(fibre['count'], len(expected[key]))
                self.assertEqual(len(fibre['lifts']), len(expected[key]))
            self.assertEqual(actual['10'] | actual['11'], source_rows[pattern])
            self.assertEqual(actual['01'] | actual['11'], final_rows[pattern])
            self.assertEqual(actual['11'], intersection_rows[pattern])

    def test_one_inner_star_has_equal_relation_but_different_counts(self):
        star = {
            'vertices': list(range(6)),
            'boundary': list(range(5)),
            'edges': CYCLE + [(1, 5), (2, 5), (3, 5), (4, 5)],
        }
        report = transform.analyze(star)
        self.assert_complete_state(report['result'], 987)
        counts = [row['count'] for row in report['result']['rows']]
        flip_counts = [row['count'] for row in self.flipped['result']['rows']]
        self.assertNotEqual(counts, flip_counts)

    def test_catalogue_loads_named_891_fixture(self):
        loaded = transform.load_cell(891)
        self.assertEqual(loaded['vertices'], ORIGINAL['vertices'])
        self.assertEqual(loaded['boundary'], ORIGINAL['boundary'])
        self.assertEqual(edge_set(loaded), edge_set(ORIGINAL))

    def test_analysis_does_not_mutate_the_source(self):
        graph = deepcopy(ORIGINAL)
        original = deepcopy(graph)
        transform.analyze(graph, add=ADD, remove=REMOVE)
        self.assertEqual(graph, original)

    def test_named_vertices_and_ordered_boundary_survive_relabeling(self):
        names = dict(zip(range(10), [30, -4, 91, 8, 19, -21, 6, 100, -8, 52]))
        graph = {
            'vertices': [names[v] for v in reversed(ORIGINAL['vertices'])],
            'boundary': [names[v] for v in ORIGINAL['boundary']],
            'edges': [(names[u], names[v]) for u, v in ORIGINAL['edges']],
        }
        report = transform.analyze(
            graph, add=tuple(names[v] for v in ADD),
            remove=tuple(names[v] for v in REMOVE), require_flip=True)
        self.assertEqual(report['result_graph']['boundary'], graph['boundary'])
        self.assertEqual(report['result_graph']['vertices'], sorted(names.values()))
        self.assert_complete_state(report['source'], 891)
        self.assert_complete_state(report['result'], 987)
        canonical_ids = report['result_graph']['vertices']
        positions = {v: canonical_ids.index(names[v]) for v in ORIGINAL['vertices']}
        for renamed_row, original_row in zip(report['joint_rows'], self.flipped['joint_rows']):
            for key, fibre in renamed_row['fibres'].items():
                original_order_lifts = {
                    tuple(lift[positions[v]] for v in ORIGINAL['vertices'])
                    for lift in fibre['lifts']
                }
                self.assertEqual(original_order_lifts,
                                 {tuple(lift) for lift in original_row['fibres'][key]['lifts']})
        self.assertEqual(transform.parse_vertex('b3', report['result_graph']), names[3])
        self.assertEqual(transform.parse_vertex('v-8', report['result_graph']), -8)

    def test_disconnected_interiors_keep_all_full_lifts(self):
        for name, inner, extra_edges, count in (
            ('isolated_vertex', [5], [], 4),
            ('detached_triangle', [5, 6, 7], [(5, 6), (6, 7), (5, 7)], 24),
        ):
            with self.subTest(component=name):
                graph = {'vertices': list(range(5)) + inner,
                         'boundary': list(range(5)), 'edges': CYCLE + extra_edges}
                report = transform.analyze(graph)
                self.assert_complete_state(report['result'], 1023)
                self.assertTrue(report['result']['topology']['disk'])
                self.assertTrue(report['result']['topology']['planar'])
                self.assertEqual([row['count'] for row in report['result']['rows']], [count] * 10)
                self.assertEqual({item['vertex'] for item in report['result']['topology']['rotation']},
                                 set(graph['vertices']))

    def test_planarity_alone_does_not_make_a_c5_disk(self):
        graph = {'vertices': list(range(5)), 'boundary': list(range(5)),
                 'edges': CYCLE + [(0, 2), (1, 3)]}
        report = transform.analyze(graph)
        self.assert_complete_state(report['result'], 824)
        self.assertTrue(report['result']['topology']['planar'])
        self.assertFalse(report['result']['topology']['disk'])
        self.assertEqual(transform.flip_candidates(report['result_graph']), [])

    def test_strict_flip_rejects_disconnected_component_placement(self):
        graph = deepcopy(ORIGINAL)
        graph['vertices'].append(10)
        with self.assertRaises(ValueError):
            transform.analyze(graph, add=ADD, remove=REMOVE, require_flip=True)

    def test_full_lift_limit_rejects_instead_of_truncating(self):
        for limit in (4, -1, 1.5, True):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                transform.analyze(deepcopy(ORIGINAL), max_inner=limit)
        bounded = transform.analyze(deepcopy(ORIGINAL), max_inner=5)
        self.assert_complete_state(bounded['result'], 891)

    def test_invalid_graphs_are_rejected(self):
        duplicate = deepcopy(ORIGINAL)
        duplicate['edges'].append((1, 0))
        absent_boundary_edge = deepcopy(ORIGINAL)
        absent_boundary_edge['edges'].remove((0, 1))
        repeated_boundary = deepcopy(ORIGINAL)
        repeated_boundary['boundary'] = [0, 1, 2, 3, 3]
        absent_vertex = deepcopy(ORIGINAL)
        absent_vertex['vertices'].remove(8)
        self_loop = deepcopy(ORIGINAL)
        self_loop['edges'].append((5, 5))
        pinned = {**deepcopy(ORIGINAL), 'pins': {5: 0}}
        supplied_rotation = {**deepcopy(ORIGINAL), 'rotation': []}
        for name, graph in (
            ('duplicate_edge', duplicate), ('boundary_edge', absent_boundary_edge),
            ('boundary_order', repeated_boundary), ('absent_vertex', absent_vertex),
            ('self_loop', self_loop), ('unsupported_pins', pinned),
            ('unsupported_rotation', supplied_rotation),
        ):
            with self.subTest(case=name), self.assertRaises(ValueError):
                transform.analyze(graph)

    def test_invalid_edits_are_rejected(self):
        for name, kwargs in (
            ('same_edge_flip', {'add': REMOVE, 'remove': REMOVE}),
            ('boundary_removal', {'remove': (0, 1)}),
            ('missing_vertex_add', {'add': (3, 99)}),
            ('missing_vertex_remove', {'remove': (4, 99)}),
            ('absent_edge_remove', {'remove': ADD}),
            ('existing_edge_add', {'add': REMOVE}),
            ('nonlocal_flip', {'add': (0, 8), 'remove': REMOVE, 'require_flip': True}),
            ('missing_flip_operation', {'add': ADD, 'require_flip': True}),
        ):
            with self.subTest(case=name), self.assertRaises(ValueError):
                transform.analyze(deepcopy(ORIGINAL), **kwargs)


if __name__ == '__main__':
    unittest.main()
