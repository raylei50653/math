#!/usr/bin/env python3
"""Finite publication custody check; reads saved evidence without solving graphs.

Run from any directory with --out pointing to a fresh JSON path. Historical
sources are checked against their saved snapshots, not silently relabelled as
the current implementation. This is a publication receipt, not a new CI gate.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = [
    "artifacts/four_color_information_partition",
    "artifacts/four_color_information_partition_final",
    "artifacts/four_color_partial_history",
    "artifacts/four_color_partition",
    "artifacts/four_color_propagation",
    "artifacts/four_color_support_loss",
]
AUDITS = [
    "audits/2026-10-27-four-color-math-analysis-aec8920",
    "audits/2026-10-27-four-color-method-comparison-aec8920",
    "audits/2026-10-27-four-color-region-messages-aec8920",
    "audits/2026-10-29-four-color-bounded-projection-aec8920",
    "audits/2026-10-29-four-color-six-cut-exclusion-aec8920",
]
METHOD = ROOT / AUDITS[1]
CACHE = {}


def label(path):
    return str(path.relative_to(ROOT))


def digest(path):
    if path not in CACHE:
        CACHE[path] = hashlib.sha256(path.read_bytes()).hexdigest()
    return CACHE[path]


def read(path):
    return json.loads(path.read_text())


def checked(path, expected):
    assert path.is_file(), f"missing file: {path}"
    assert digest(path) == expected, f"hash mismatch: {path}"


def graph_digest(graph):
    normalized = dict(vertices=list(graph["vertices"]),
                      edges=[list(edge) for edge in sorted(
                          {tuple(sorted(edge)) for edge in graph["edges"]})],
                      fixed=[list(pair) for pair in graph.get("fixed", [])])
    return hashlib.sha256(json.dumps(normalized, separators=(",", ":")).encode()).hexdigest()


def source_map(report, mapping):
    bindings = {}
    historical = []
    for name, expected in mapping.items():
        candidates = []
        for ancestor in (report.parent, *report.parents):
            if ancestor == ROOT.parent:
                break
            candidates.extend((ancestor / "source" / name,
                               ancestor / "source" / Path(name).name))
        candidates.append(ROOT / name)
        if name == "scripts/four_color_lab.py":
            candidates.append(ROOT / "audits/2026-10-26-four-color-local-messages-f30cd6f/source/four_color_lab.py")
        matches = [path for path in candidates
                   if path.is_file() and digest(path) == expected]
        assert matches, f"no saved source matches {report}: {name}"
        bindings[name] = label(matches[0])
        if (ROOT / name).is_file() and digest(ROOT / name) != expected:
            historical.append(name)
    return dict(entries=len(mapping), bindings=bindings,
                differs_from_current=historical)


def flow_report(path):
    report = read(path)
    checked(path.parent / report["input_file"], report["inputs_sha256"])
    checked(path.parent / report["baseline_manifest_file"],
            report["baseline_manifest_sha256"])
    checked(ROOT / report["frozen_source_input"], report["inputs_sha256"])
    inputs = read(path.parent / report["input_file"])
    assert len(inputs) == len(report["cases"]) == report["case_count"]
    input_by_name = {case["name"]: case for case in inputs}
    assert list(input_by_name) == report["selected_cases"]
    records = {}
    for case in report["cases"]:
        original = input_by_name[case["name"]]
        expected_graph = graph_digest(original["graph"])
        assert case["graph_sha256"] == expected_graph
        if "graph_sha256" in original:
            assert original["graph_sha256"] == expected_graph
        for row in case["results"].values():
            record = path.parent / row["full_record"]
            checked(record, row["compressed_record_sha256"])
            data = json.loads(gzip.decompress(record.read_bytes()))
            assert data["graph_sha256"] == case["graph_sha256"]
            assert data["status"] == row["status"]
            assert data["colors"] == row["colors"]
            records[case["name"]] = row["compressed_record_sha256"]
    sources = source_map(path, report["sources"])
    assert report["driver_sha256"] == report["sources"]["scripts/four_color_flow_experiment.py"]
    return dict(sha256=digest(path), inputs_sha256=report["inputs_sha256"],
                cases=len(report["cases"]), records=records, sources=sources)


def comparison(path, reports):
    data = read(path)
    bindings = 0
    for name, case in data["cases"].items():
        modes = case.get("modes", case)
        for mode, row in modes.items():
            if not isinstance(row, dict) or "record_sha256" not in row:
                continue
            report_name = label(path.parent / mode / "report.json")
            assert row["record_sha256"] == reports[report_name]["records"][name]
            bindings += 1
    result = dict(sha256=digest(path), record_bindings=bindings)
    if "sources" in data:
        result["sources"] = source_map(path, data["sources"])
    return result


def audit():
    flow = {}
    comparisons = {}
    for root in [*ARTIFACTS, AUDITS[1]]:
        for path in sorted((ROOT / root).rglob("report.json")):
            flow[label(path)] = flow_report(path)
        for path in sorted((ROOT / root).rglob("comparison.json")):
            comparisons[label(path)] = comparison(path, flow)
    partial_path = ROOT / ARTIFACTS[2] / "summary.json"
    partial = source_map(partial_path, read(partial_path)["sources_sha256"])
    partial["summary_sha256"] = digest(partial_path)
    checked(partial_path, read(partial_path.parent / "verification.json")["summary_sha256"])
    math_root = ROOT / AUDITS[0]
    math_files = read(math_root / "verification.json")["files"]
    for name, expected in math_files.items():
        checked(math_root / name, expected)
    latest = ROOT / AUDITS[1] / "replay/comparison.json"
    latest_sources = read(latest)["sources"]
    for name, expected in latest_sources.items():
        checked(ROOT / name, expected)
    checked(METHOD / "replay/comparison_driver.py", read(latest)["comparison_driver_sha256"])
    checked(METHOD / "compare.py", read(latest)["comparison_driver_sha256"])
    large = []
    for root in [*ARTIFACTS, *AUDITS]:
        for path in sorted((ROOT / root).rglob("*.json")):
            if path.stat().st_size >= 1_000_000:
                large.append(dict(path=label(path), bytes=path.stat().st_size,
                                  sha256=digest(path)))
    return dict(
        schema="four-color-progress-publication-custody-v1", state="passed",
        scope="Saved input/source/run custody only; no experiment reruns or mathematical proof validation.",
        flow_reports=flow, comparisons=comparisons,
        flow_report_count=len(flow),
        compressed_run_hash_checks=sum(len(r["records"]) for r in flow.values()),
        comparison_record_bindings=sum(r["record_bindings"] for r in comparisons.values()),
        partial_history=partial,
        mathematical_analysis=dict(entries=len(math_files), all_saved_hashes_equal=True),
        current_method_comparison=dict(source_entries=len(latest_sources),
                                       all_sources_equal_current=True,
                                       comparator_and_snapshot_equal=True),
        large_json_threshold_bytes=1_000_000, large_json_count=len(large),
        large_json_total_bytes=sum(row["bytes"] for row in large), large_json=large,
        note="Earlier document hashes and prior check failures remain historical; source differences use saved snapshots.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    with args.out.open("x") as output:
        output.write(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in
                      ("state", "flow_report_count", "compressed_run_hash_checks",
                       "comparison_record_bindings", "large_json_count")}, sort_keys=True))
