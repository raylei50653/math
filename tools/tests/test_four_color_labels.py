"""Arbitrary integer identities must survive solving, hashing and export."""
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_constraints import solve_constraints
from four_color_lab import graph_fingerprint, normalize_graph, solve, verify_coloring, write_html
from four_color_serialization import browser_payload, int_text, json_dumps, json_loads


class IntegerLabelTests(unittest.TestCase):
    BIG = 10 ** 4300

    def test_normal_json_and_fingerprint_remain_byte_identical(self):
        graph = dict(vertices=[71, -9, 3], edges=[[71, 3], [-9, 3]], fixed=[[71, 2]])
        data = dict(graph=graph, text="原圖 < >", float=0.125, bool=True, none=None)
        for options in ({}, dict(ensure_ascii=False, indent=2),
                        dict(sort_keys=True, separators=(",", ":"))):
            self.assertEqual(json_dumps(data, **options), json.dumps(data, **options))
        clean = normalize_graph(graph)
        source = {key: clean[key] for key in ("vertices", "edges", "fixed")}
        expected = hashlib.sha256(json.dumps(source, separators=(",", ":")).encode()).hexdigest()
        self.assertEqual(graph_fingerprint(graph), expected)

    def test_exact_decimal_json_roundtrip_does_not_change_interpreter_setting(self):
        limit = sys.get_int_max_str_digits()
        self.assertEqual(int_text(self.BIG), "1" + "0" * 4300)
        self.assertEqual(int_text(-self.BIG), "-1" + "0" * 4300)
        value = dict(vertices=[self.BIG, self.BIG + 1, -self.BIG], metadata={self.BIG: "原點"})
        for options in ({}, dict(ensure_ascii=False, indent=2), dict(indent="\t", sort_keys=True)):
            encoded = json_dumps(value, **options)
            decoded = json_loads(encoded)
            self.assertEqual(decoded["vertices"], value["vertices"])
            self.assertEqual(decoded["metadata"], {int_text(self.BIG): "原點"})
            self.assertTrue(all(type(v) is int for v in decoded["vertices"]))
        self.assertEqual(sys.get_int_max_str_digits(), limit)

    def test_safe_fallback_retains_noninteger_json_errors(self):
        with self.assertRaises(ValueError):
            json_dumps([self.BIG, float("nan")], allow_nan=False)
        cyclic = [self.BIG]
        cyclic.append(cyclic)
        with self.assertRaisesRegex(ValueError, "Circular reference"):
            json_dumps(cyclic)
        with self.assertRaises(json.JSONDecodeError):
            json_loads('{"vertices": [01]}')

    def test_both_engines_preserve_large_ids_with_and_without_trace(self):
        big = self.BIG
        graphs = [dict(vertices=[big], edges=[]),
                  dict(vertices=[big, big + 1, -big], edges=[[big, big + 1]], fixed=[[-big, 3]]),
                  dict(vertices=[big, big + 1], edges=[[big, big + 1]], fixed=[[big, 1], [big + 1, 1]]),
                  dict(vertices=[big + v for v in range(5)],
                       edges=[[big + u, big + v] for u, v in combinations(range(5), 2)])]
        limit = sys.get_int_max_str_digits()
        for graph, expected in zip(graphs, ("colored", "colored", "unsatisfiable", "unsatisfiable")):
            for engine in (solve, solve_constraints):
                for trace_limit in (0, 1000):
                    with self.subTest(engine=engine.__name__, n=len(graph["vertices"]), trace=trace_limit):
                        result = engine(graph, trace_limit=trace_limit)
                        self.assertEqual(result["status"], expected)
                        self.assertEqual(result["graph"]["vertices"], graph["vertices"])
                        if expected == "colored":
                            self.assertTrue(verify_coloring(graph, result["colors"]))
                        self.assertEqual(json_loads(json_dumps(result))["graph"]["vertices"], graph["vertices"])
        self.assertEqual(sys.get_int_max_str_digits(), limit)

    def test_large_ids_in_optional_cycle_and_context_inference(self):
        big = self.BIG
        graph = dict(vertices=[big + i for i in range(6)],
                     edges=[[big + i, big + (i + 1) % 5] for i in range(5)]
                           + [[big + 5, big + i] for i in range(5)])
        result = solve_constraints(graph, use_c5=True, c5_method="structure",
                                   use_intersections=True, use_cycles=True,
                                   use_cycle_contexts=True, cycle_context_search="partial",
                                   use_joint_consistency=True)
        self.assertEqual(result["status"], "colored")
        self.assertTrue(verify_coloring(graph, result["colors"]))
        self.assertGreater(result["stats"]["joint_consistency_queries"], 0)

    def test_viewer_uses_distinct_exact_strings_above_js_safe_integer_range(self):
        labels = [(1 << 53), (1 << 53) + 1, self.BIG, self.BIG + 1, -self.BIG]
        graph = dict(vertices=labels, edges=[[labels[0], labels[1]], [labels[2], labels[3]]])
        result = solve(graph)
        payload = browser_payload(dict(runs=[result]))
        converted = payload["runs"][0]
        expected = list(map(int_text, labels))
        self.assertEqual(converted["graph"]["vertices"], expected)
        self.assertEqual(len(set(expected)), len(labels))
        self.assertTrue(all(event["vertex"] is None or event["vertex"] in expected
                            for event in converted["events"]))
        self.assertEqual(result["graph"]["vertices"], labels)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "viewer.html"
            write_html(path, dict(runs=[result]))
            text = path.read_text()
            match = re.search(r'<script[^>]*id="four-color-data"[^>]*>(.*?)</script>', text, re.S)
            self.assertIsNotNone(match)
            self.assertEqual(json.loads(match.group(1))["runs"][0]["graph"]["vertices"], expected)

    def test_cli_reads_and_writes_large_integer_json_for_both_engines(self):
        graph = dict(vertices=[self.BIG, self.BIG + 1], edges=[[self.BIG, self.BIG + 1]])
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.json"
            source.write_text(json_dumps(graph))
            for engine in ("search", "constraints"):
                out = Path(directory) / (engine + ".json")
                html = out.with_suffix(".html")
                run = subprocess.run([sys.executable, str(ROOT / "scripts/four_color_lab.py"),
                                      "solve", str(source), "--engine", engine,
                                      "--json", str(out), "--html", str(html)],
                                     cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                result = json_loads(out.read_text())
                self.assertEqual(result["status"], "colored")
                self.assertEqual(result["graph"]["vertices"], graph["vertices"])
                self.assertTrue(verify_coloring(graph, result["colors"]))
                self.assertTrue(html.is_file())


if __name__ == "__main__":
    unittest.main()
