"""Early complete-factor rejection preserves exact fibres and explanations."""

from copy import deepcopy
from itertools import combinations
import gzip
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import test_four_color_bucket_flow as bucket_tests


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_constraints import solve_constraints
from four_color_logic_experiment import compare, semantic_record


class PrefixBucketTests(bucket_tests.BucketFlowTests):
    # Reuse independent Cartesian-join, empty-fibre, original-solution and
    # every-work-interruption tests against the new mode, including empty buckets.
    def solve(self, graph, **options):
        return super().solve(graph, bucket_method="prefix", **options)

    def test_complete_outputs_match_anchor_on_new_fixed_graphs_and_color_frames(self):
        rng = random.Random(20261026)
        labels = [40, -3, 900, 17, 0, 81]
        for case in range(20):
            graph = dict(vertices=labels, edges=[list(edge) for edge in combinations(labels, 2)
                         if rng.random() < 0.55], fixed=[[labels[0], rng.randrange(4)]])
            if case % 2:
                graph = dict(vertices=list(reversed(labels)),
                             edges=[list(reversed(edge)) for edge in reversed(graph["edges"])],
                             fixed=[[labels[0], 3 - graph["fixed"][0][1]]])
            before = deepcopy(graph)
            for contexts in (False, True):
                settings = dict(use_substructures=False, use_conflicts=False,
                                use_intersections=contexts, use_cycles=contexts,
                                use_cycle_contexts=contexts, max_checks=1_000_000,
                                trace_limit=10000, max_table_rows=100000,
                                cycle_context_search="partial" if contexts else "neighbours")
                with self.subTest(case=case, contexts=contexts):
                    anchor = solve_constraints(graph, bucket_method="anchor", **settings)
                    prefix = solve_constraints(graph, bucket_method="prefix", **settings)
                    self.assertNotEqual(prefix["status"], "limit")
                    self.assertEqual(semantic_record(anchor), semantic_record(prefix))
                    self.assert_complete_join_fibres(prefix)
                    self.assertEqual(graph, before)

    def test_prefix_rejects_k5_with_complete_empty_joint_fibre(self):
        graph = dict(vertices=list(range(5)), edges=list(map(list, combinations(range(5), 2))))
        options = dict(use_substructures=False, use_conflicts=False, use_intersections=False)
        anchor = solve_constraints(graph, **options)
        prefix = solve_constraints(graph, bucket_method="prefix", **options)
        self.assertEqual(prefix["status"], "unsatisfiable")
        self.assertLess(prefix["stats"]["checks"], anchor["stats"]["checks"])
        self.assertEqual(semantic_record(anchor), semantic_record(prefix))

    def test_storage_interruptions_never_publish_partial_fibres(self):
        graph = dict(vertices=[9, -2, 40, 17], edges=[[9, -2], [-2, 40], [40, 17], [17, 9]],
                     fixed=[[9, 0]])
        complete = self.solve(graph, max_table_rows=100000)
        needed = max(complete["stats"]["table_rows"], complete["stats"]["certificate_rows"])
        for cap in range(needed + 1):
            with self.subTest(cap=cap):
                result = self.solve(graph, max_table_rows=cap)
                self.assert_complete_join_fibres(result)
                records = result["elimination_records"]
                self.assertEqual(records, complete["elimination_records"][:len(records)])
                if result["status"] == "limit":
                    self.assertEqual(result["colors"], [0, -1, -1, -1])
                    self.assertEqual(result["stats"]["writebacks"], 0)
                else:
                    self.assertEqual(result["status"], "colored")

    def test_method_api_and_cli(self):
        graph = dict(vertices=[0, 1], edges=[[0, 1]])
        self.assertEqual(solve_constraints(graph)["bucket_method"], "anchor")
        for value in (None, True, 0, [], {}, "join", "PREFIX"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                solve_constraints(graph, bucket_method=value)
        with TemporaryDirectory() as directory:
            source = Path(directory) / "graph.json"
            output = Path(directory) / "result.json"
            source.write_text(json.dumps(graph))
            command = [sys.executable, str(ROOT / "scripts/four_color_lab.py"),
                       "solve", str(source), "--bucket-method", "prefix"]
            process = subprocess.run(command + ["--engine", "constraints", "--json", str(output)],
                                     capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads(output.read_text())["bucket_method"], "prefix")
            process = subprocess.run(command + ["--engine", "search"], capture_output=True, text=True)
            self.assertNotEqual(process.returncode, 0)
            self.assertIn("require --engine constraints", process.stderr)

    def test_comparison_rejects_wrong_mode_and_changed_explanations(self):
        graph = dict(vertices=[0, 1], edges=[[0, 1]])
        for corruption in (None, "reported_mode", "executed_mode", "explanation"):
            with self.subTest(corruption=corruption), TemporaryDirectory() as directory:
                root = Path(directory)
                for mode in ("anchor", "prefix"):
                    folder = root / mode
                    folder.mkdir()
                    result = solve_constraints(graph, bucket_method=mode)
                    if mode == "prefix" and corruption == "executed_mode":
                        result["bucket_method"] = "anchor"
                    if mode == "prefix" and corruption == "explanation":
                        result["events"][0]["detail"] = "changed explanation"
                    raw = gzip.compress(json.dumps(result).encode(), mtime=0)
                    (folder / "record.json.gz").write_bytes(raw)
                    row = dict(stats=result["stats"], full_record="record.json.gz",
                               compressed_record_sha256=hashlib.sha256(raw).hexdigest())
                    report = dict(inputs_sha256="fixture", sources={}, driver_sha256="fixture",
                                  selected_cases=["fixture"], oracle_max_rows=100000,
                                  python="fixture", networkx=None, totals={"all": {}},
                                  options={"bucket_method": "anchor" if mode == "prefix"
                                           and corruption == "reported_mode" else mode},
                                  cases=[dict(name="fixture", case_group="gap",
                                              results={"combined-contexts": row})])
                    (folder / "report.json").write_text(json.dumps(report))
                if corruption is None:
                    self.assertEqual(compare(root)["case_groups"], {"gap": 1})
                else:
                    with self.assertRaises(AssertionError):
                        compare(root)


if __name__ == "__main__":
    unittest.main()
