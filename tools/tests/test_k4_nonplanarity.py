"""Exercise soundness boundaries and reject damaged original-edge certificates."""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import k4_nonplanarity as detector


def complete(n):
    return {"vertices": list(range(n)), "edges": list(combinations(range(n), 2))}


class K4NonplanarityTests(unittest.TestCase):
    def test_k4_and_four_disconnected_leaves_do_not_trigger(self):
        graph = complete(4)
        self.assertFalse(detector.detect(graph)["detected"])
        graph["vertices"] += list(range(4, 8))
        graph["edges"] += [(i, i + 4) for i in range(4)]
        result = detector.detect(graph)
        self.assertEqual(result["status"], "not triggered")
        self.assertEqual(result["scan"]["max_attachment_count"], 1)

    def test_one_connected_branch_with_four_distinct_attachments(self):
        graph = complete(4)
        graph["vertices"] += list(range(4, 9))
        graph["edges"] += [(4, 5), (5, 6), (6, 7), (7, 8)]
        graph["edges"] += [(0, 4), (1, 5), (2, 7), (3, 8)]
        result = detector.detect(graph)
        self.assertTrue(result["detected"])
        self.assertTrue(detector.verify_certificate(graph, result["certificate"]))
        self.assertEqual(result["certificate"]["branch_sets"][4], list(range(4, 9)))

    def test_k33_with_extra_triangle_is_a_k4_present_miss(self):
        graph = {"vertices": list(range(6)),
                 "edges": list(combinations(range(3), 2)) +
                          [(u, v) for u in range(3) for v in range(3, 6)]}
        result = detector.detect(graph)
        self.assertFalse(result["detected"])
        self.assertEqual(result["scan"]["k4s_scanned"], 3)
        self.assertEqual(result["scan"]["max_attachment_count"], 3)

    def test_disconnected_whole_graph_can_still_have_a_valid_obstruction(self):
        graph = complete(5)
        graph["vertices"] += [8, 9]
        graph["edges"] += [(8, 9)]
        self.assertTrue(detector.detect(graph)["detected"])

    def test_missing_links_overlap_and_nonexistent_source_edges_rejected(self):
        graph = complete(5)
        good = detector.detect(graph)["certificate"]
        mutations = []
        bad = deepcopy(good)
        bad["links"].pop()
        mutations.append(bad)
        bad = deepcopy(good)
        bad["branch_sets"][4] = [0]
        mutations.append(bad)
        bad = deepcopy(good)
        bad["links"][0]["edge"] = [0, 9]
        mutations.append(bad)
        bad = deepcopy(good)
        bad["links"][1] = deepcopy(bad["links"][0])
        mutations.append(bad)
        for bad in mutations:
            with self.assertRaises(ValueError):
                detector.verify_certificate(graph, bad)

    def test_disconnected_fifth_branch_rejected_despite_four_attachments(self):
        graph = complete(4)
        graph["vertices"] += [4, 5]
        graph["edges"] += [(0, 4), (1, 4), (2, 5), (3, 5)]
        forged = {"model": "K5", "k4": list(range(4)),
                  "branch_sets": [[i] for i in range(4)] + [[4, 5]],
                  "branch_trees": [[], [], [], [], [[4, 5]]],
                  "links": [{"branches": [i, j], "edge": [i, j]}
                            for i, j in combinations(range(4), 2)] +
                           [{"branches": [i, 4], "edge": [i, 4 if i < 2 else 5]}
                            for i in range(4)]}
        self.assertFalse(detector.detect(graph)["detected"])
        with self.assertRaises(ValueError):
            detector.verify_certificate(graph, forged)

    def test_invalid_declared_vertices_and_loops_rejected(self):
        for graph in ({"vertices": [0, 0], "edges": []},
                      {"vertices": [0], "edges": [(0, 1)]},
                      {"vertices": [0], "edges": [(0, 0)]},
                      {"vertices": [True], "edges": []}):
            with self.assertRaises(ValueError):
                detector.detect(graph)

    def test_certificate_vertex_ids_are_exact_integers(self):
        graph = complete(5)
        for substitute in (False, 0.0):
            bad = deepcopy(detector.detect(graph)["certificate"])
            bad["branch_sets"][0] = [substitute]
            with self.assertRaises(ValueError):
                detector.verify_certificate(graph, bad)

    def test_duplicate_undirected_edges_normalize_to_one_edge(self):
        graph = complete(5)
        graph["edges"] += [(0, 1), (1, 0)]
        self.assertEqual(len(detector.normalize(graph)["edges"]), 10)
        self.assertTrue(detector.detect(graph)["detected"])


if __name__ == "__main__":
    unittest.main()
