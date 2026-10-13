"""Independent full-atlas checks and corruption controls for graph-state BFS."""
from copy import deepcopy
import gzip
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_c5_cell_flip_distances as audit  # noqa: E402


class CellFlipDistanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / 'artifacts/c5_cell_flip_distances/atlas.json.gz'
        with gzip.open(path, 'rt') as stream:
            cls.atlas = json.load(stream)
        cls.catalogue = json.loads(audit.CATALOGUE.read_text())
        cls.tables = {k: audit.AssignmentAudit(k) for k in range(6)}

    def test_entire_atlas_has_independent_assignment_rotation_and_bfs_audit(self):
        result = audit.validate_atlas(self.atlas)
        self.assertEqual(result['checked_sources'], 132)
        self.assertEqual(result['checked_graphs'], 20531)
        self.assertEqual(result['checked_expanded_rotations'], 5441)

    def test_small_spaces_have_known_exhaustive_distances(self):
        pentagon = self.atlas['sources']['165']
        self.assertEqual(pentagon['state_layers'], [1, 2, 2, 0])
        self.assertTrue(pentagon['exhausted'])
        self.assertEqual({m: d for m, d in pentagon['distance'].items() if d is not None},
                         {'165': 0, '424': 1, '564': 1, '774': 2, '960': 2})
        wheel = self.atlas['sources']['91']
        self.assertEqual(wheel['state_layers'], [1, 5, 15, 0])
        self.assertTrue(wheel['exhausted'])
        self.assertEqual(wheel['lower_catalogue_k_distance'], 2)

    def test_new_graph_states_continue_after_new_relation_masks_stop(self):
        source = self.atlas['sources']['987']
        self.assertEqual(source['state_layers'], [1, 2, 2, 2])
        self.assertEqual(source['relation_layers'], [1, 2, 2, 0])
        self.assertEqual({m: d for m, d in source['distance'].items() if d is not None},
                         {'987': 0, '830': 1, '431': 1, '564': 2, '165': 2})

    def test_known_flip_keeps_literal_graph_instead_of_representative(self):
        source = self.atlas['sources']['891']
        self.assertEqual(source['distance']['987'], 1)
        path = source['paths']['987']
        before_k, before_edges = audit.decode(path[0])
        after_k, after_edges = audit.decode(path[-1])
        self.assertEqual(before_k, 5)
        self.assertEqual(after_k, before_k)
        self.assertEqual(len(before_edges), len(after_edges))
        self.assertNotEqual(path[-1], self.atlas['sources']['987']['start'])
        self.assertEqual(self.atlas['sources']['987']['k'], 1)

    def test_bare_frame_is_frozen_and_nulls_are_not_zero(self):
        source = self.atlas['sources']['1023']
        self.assertEqual(source['state_layers'], [1, 0, 0, 0])
        self.assertEqual(source['distance']['1023'], 0)
        self.assertIsNone(source['distance']['91'])
        self.assertTrue(source['exhausted'])
        self.assertEqual(source['one_step_moves'], {})

    def mutable_wheel_node(self):
        key = self.atlas['sources']['91']['start']
        return key, deepcopy(self.atlas['nodes'][key])

    def test_rejects_corrupted_full_assignment_count(self):
        key, node = self.mutable_wheel_node()
        node['counts'][0] += 1
        with self.assertRaisesRegex(ValueError, 'counts differ'):
            audit.validate_node(key, node, self.tables)

    def test_rejects_corrupted_rotation(self):
        key, node = self.mutable_wheel_node()
        node['rotation'][0]['clockwise'].pop()
        with self.assertRaisesRegex(ValueError, 'incident edges'):
            audit.validate_node(key, node, self.tables)

    def test_rejects_missing_legal_flip(self):
        key, node = self.mutable_wheel_node()
        node['moves'].pop()
        with self.assertRaisesRegex(ValueError, 'move set differs'):
            audit.validate_node(key, node, self.tables)

    def changed_source(self, mask):
        # Share immutable nodes; mutation controls only alter one copied source.
        data = {**self.atlas, 'sources': dict(self.atlas['sources'])}
        data['sources'][str(mask)] = deepcopy(data['sources'][str(mask)])
        return data, data['sources'][str(mask)]

    def test_rejects_false_distance(self):
        data, source = self.changed_source(91)
        source['distance']['165'] = 1
        with self.assertRaisesRegex(ValueError, 'Distance table differs'):
            audit.validate_sources(data, self.catalogue)

    def test_rejects_mask_based_source_replacement(self):
        data, source = self.changed_source(891)
        source['start'] = next(key for key, node in self.atlas['nodes'].items()
                               if node['sigma'] == 891 and key != source['start'])
        self.assertEqual(self.atlas['nodes'][source['start']]['sigma'], 891)
        with self.assertRaisesRegex(ValueError, 'Source graph was replaced'):
            audit.validate_sources(data, self.catalogue)

    def test_rejects_path_that_restarts_from_target_representative(self):
        data, source = self.changed_source(91)
        source['paths']['165'][-1] = self.atlas['sources']['165']['start']
        with self.assertRaisesRegex(ValueError, 'witness paths differ'):
            audit.validate_sources(data, self.catalogue)

    def test_rejects_exhaustion_with_unexpanded_frontier(self):
        data, source = self.changed_source(891)
        source['exhausted'] = True
        with self.assertRaisesRegex(ValueError, 'False exhaustion claim'):
            audit.validate_sources(data, self.catalogue)

    def test_rejects_relation_only_layer_count(self):
        data, source = self.changed_source(987)
        source['state_layers'] = list(source['relation_layers'])
        with self.assertRaisesRegex(ValueError, 'Graph layers differ'):
            audit.validate_sources(data, self.catalogue)

    def test_rejects_invalid_graph_keys(self):
        for key in ('-1:0', '6:0', '1:-1', '1:32768', '01:0'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                audit.decode(key)


if __name__ == '__main__':
    unittest.main()
