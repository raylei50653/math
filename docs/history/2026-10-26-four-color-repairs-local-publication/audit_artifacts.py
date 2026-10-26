#!/usr/bin/env python3
"""Audit saved colouring evidence without rerunning solvers or benchmarks.

Only --out is written. Historical source hashes bind to the recorded Git base
or the preserved pre-normalization snapshot, not automatically to current code.
Prior test, timing and seed-17 receipts remain historical execution evidence.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys


def digest(raw):
    return sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    prefix = root / "audits"
    dirs = {name: prefix / ("2026-10-26-four-color-" + name + "-f30cd6f")
            for name in ("counterexamples", "repairs", "normalization", "local-messages")}
    counts, errors = Counter(), []
    current_sources, snapshots, checked_files = set(), set(), set()
    historical_routing_docs = []
    historical_source_gaps = []

    def require(condition, label, detail=""):
        counts[label] += 1
        if not condition:
            errors.append(dict(kind=label, detail=str(detail)))

    def load(path):
        return json.loads(path.read_bytes())

    def file_hash(path, expected, label):
        require(path.is_file() and digest(path.read_bytes()) == expected,
                label, path.relative_to(root))
        checked_files.add(path)

    def hashes(directory, values, label):
        for name, expected in values.items():
            file_hash(directory / name, expected, label)

    def git_hash(commit, relative, expected):
        require(bool(re.fullmatch(r"[0-9a-f]{40}", commit)), "base_sha_shape", commit)
        result = subprocess.run(["git", "-C", str(root), "show", commit + ":" + relative],
                                capture_output=True, check=False)
        require(result.returncode == 0 and digest(result.stdout) == expected,
                "original_git_source_bindings", relative)

    def current_hashes(values):
        for relative, expected in values.items():
            file_hash(root / relative, expected, "current_source_bindings")
            current_sources.add(relative)

    def snapshot_hashes(values):
        for relative, expected in values.items():
            path = dirs["normalization"] / "baseline-source" / relative
            file_hash(path, expected, "repair_snapshot_bindings")
            snapshots.add(path)

    def witness(graph, colors, domains=None):
        if (not isinstance(colors, list) or len(colors) != len(graph["vertices"])
                or any(type(c) is not int or c not in range(4) for c in colors)):
            return False
        assignment = dict(zip(graph["vertices"], colors))
        return (all(assignment[u] != assignment[v] for u, v in graph["edges"])
                and all(assignment[v] == c for v, c in graph.get("fixed", []))
                and all(assignment[v] in values for v, values in (domains or [])))

    # Original findings use the immutable parent commit, before any repair.
    original = load(dirs["counterexamples"] / "findings.json")
    base = original["base_commit"]
    hashes(dirs["counterexamples"], original["evidence_sha256"], "original_evidence_bindings")
    for relative, expected in original["source_sha256"].items():
        git_hash(base, relative, expected)
    require(original["validation"]["ordinary_label_wrong_verdicts_found"] == 0,
            "original_finite_verdict_summary")
    require(original["verification"]["seed17_report_sha256"] ==
            original["evidence_sha256"]["propagation/report.json"],
            "historical_original_seed17_receipt_binding")

    # The exact repair-era sources survive as the next experiment's baseline.
    repair = load(dirs["repairs"] / "report.json")
    repair_receipt = load(dirs["repairs"] / "verification.json")
    hashes(dirs["repairs"], repair_receipt["evidence_sha256"], "repair_evidence_bindings")
    file_hash(dirs["repairs"] / "report.json", repair_receipt["report_sha256"],
              "repair_report_binding")
    file_hash(dirs["repairs"] / "replay.py", repair["driver_sha256"], "repair_driver_binding")
    hashes(root, repair["baseline_files_sha256"], "repair_original_evidence_custody")
    snapshot_hashes(repair["source_sha256"])
    for name, directory, source_mode in (("original", dirs["counterexamples"], "git"),
                                          ("repaired", dirs["repairs"], "snapshot")):
        atlas = load(directory / "atlas_results.json")
        file_hash(dirs["counterexamples"] / "atlas_audit.py", atlas["driver_sha256"],
                  "atlas_driver_bindings")
        require(not atlas["failures"], "saved_atlas_no_failures", name)
        if source_mode == "git":
            for relative, expected in atlas["sources"].items():
                git_hash(base, relative, expected)
        else:
            for relative, expected in atlas["sources"].items():
                path = dirs["normalization"] / "baseline-source" / relative
                if path.is_file() and digest(path.read_bytes()) == expected:
                    snapshot_hashes({relative: expected})
                else:
                    historical_source_gaps.append(dict(
                        report=str((directory / "atlas_results.json").relative_to(root)),
                        source=relative, expected_sha256=expected,
                        status="Exact intermediate historical source not preserved in the bound snapshots; saved atlas result is archival only. Primary repair report sources are fully bound separately."))
    grid = load(dirs["counterexamples"] / "grid_6x7.json")
    capacity = load(dirs["repairs"] / "capacity_comparison.json")["records"]
    require([case["status"] for case in capacity] == ["limit", "colored", "colored"],
            "saved_capacity_statuses")
    for case in capacity:
        if case["status"] == "colored":
            require(witness(grid, case["colors"]), "saved_capacity_original_witness")

    # Primary same-input normalization results and source custody.
    normalized = dirs["normalization"]
    normal_receipt = load(normalized / "verification.json")
    hashes(normalized, normal_receipt["files_sha256"], "normalization_evidence_bindings")
    manifest = load(normalized / "baseline_manifest.json")
    snapshot_hashes(manifest)
    before, after = load(normalized / "baseline.json"), load(normalized / "optimized.json")
    for report, mode in ((before, "baseline"), (after, "optimized")):
        file_hash(normalized / "compare.py", report["driver_sha256"], "comparison_driver_binding")
        sources = {"scripts/" + name: expected for name, expected in report["sources"].items()}
        snapshot_hashes(sources) if mode == "baseline" else current_hashes(sources)
    require(len(before["cases"]) == len(after["cases"]) == 2, "comparison_case_count")
    for left, right in zip(before["cases"], after["cases"]):
        require(left["graph"] == right["graph"] and left["fixed"] == right["fixed"],
                "comparison_same_original_input")
        require(left["kernel"]["input_sha256"] == right["kernel"]["input_sha256"],
                "comparison_same_joint_query")
        require(left["kernel"]["literal_support_sha256"] == right["kernel"]["literal_support_sha256"],
                "comparison_same_complete_literal_support")
        require(left["full"]["status"] == right["full"]["status"], "comparison_same_verdict")
        for record in (left, right):
            if record["full"]["status"] == "colored":
                require(witness(record["graph"], record["full"]["colors"]),
                        "comparison_original_graph_witness")
    verified = load(normalized / "verification_result.json")
    file_hash(normalized / "verify.py", verified["driver_sha256"], "normalization_driver_binding")
    hashes(root, verified["baseline_files_sha256"], "normalization_original_evidence_custody")
    current_hashes(verified["source_sha256"])
    require(verified["bare_solution_count"] == repair["bare_solution_count"] == 624,
            "saved_original_bare_solution_count")
    for label, report in (("repaired", repair), ("normalized", verified)):
        require([report[k]["status"] for k in ("fixed", "bare", "grid_default", "grid_explicit_old_capacity")]
                == ["unsatisfiable", "colored", "colored", "limit"],
                "saved_repair_and_normalized_statuses", label)

    # Lazy-message snapshots, recorded protocol consistency and original edges.
    lazy = dirs["local-messages"]
    local_receipt = load(lazy / "verification.json")
    for relative, expected in local_receipt["files_sha256"].items():
        if relative.startswith("docs/"):
            path = root / relative
            archive = (Path(__file__).resolve().parent / "pre-publication-docs" /
                       (Path(relative).name + ".txt"))
            preserved = archive.is_file() and digest(archive.read_bytes()) == expected
            if preserved:
                file_hash(archive, expected, "pre_publication_document_snapshot")
            historical_routing_docs.append(dict(path=relative, historical_sha256=expected,
                                                current_sha256=digest(path.read_bytes()),
                                                current_matches=path.is_file() and digest(path.read_bytes()) == expected,
                                                preserved_snapshot=str(archive.relative_to(root)) if preserved else None))
        else:
            file_hash(root / relative, expected, "local_evidence_bindings")
    local = load(lazy / "report.json")
    file_hash(lazy / "replay.py", local["driver_sha256"], "local_driver_binding")
    for name, expected in local["sources"].items():
        file_hash(lazy / "source" / name, expected, "local_snapshot_bindings")
        file_hash(root / "scripts" / name, expected, "local_current_source_bindings")
        snapshots.add(lazy / "source" / name)
    require(len(local["cases"]) == 9, "local_case_count")
    for case in local["cases"]:
        queries, replied, unique_nonroot = {}, set(), set()
        for event in case["transcript"]:
            qid = event["query_id"]
            if event["kind"] == "query":
                require(qid not in queries, "local_query_id_unique", case["name"])
                queries[qid] = event
                if event["sender"] is not None:
                    unique_nonroot.add((event["receiver"], tuple(event["colors"])))
            else:
                require(qid in queries and qid not in replied, "local_reply_id_pairing", case["name"])
                replied.add(qid)
                query = queries[qid]
                require(event["sender"] == query["receiver"] and event["receiver"] == query["sender"]
                        and event["separator"] == query["separator"] and event["colors"] == query["colors"],
                        "local_reply_interface_and_direction", case["name"])
        require(set(queries) == replied, "local_queries_all_answered", case["name"])
        require(len(unique_nonroot) == case["queried_nonroot_distinct_tuples"],
                "local_distinct_query_count", case["name"])
        if case["status"] == "colored":
            require(witness(case["graph"], case["colors"], case["domains"]),
                    "local_original_graph_witness", case["name"])
        else:
            require(case["colors"] is None and case["stats"]["writeback_vertices"] == 0,
                    "local_no_unsat_writeback", case["name"])

    # A publication-time rerun can validate current verdicts while preserving
    # the explicitly unresolved intermediate historical atlas-source binding.
    atlas_current_path = Path(__file__).resolve().with_name("atlas-current.json")
    publication_atlas = dict(present=atlas_current_path.is_file())
    if atlas_current_path.is_file():
        atlas_current = load(atlas_current_path)
        file_hash(dirs["counterexamples"] / "atlas_audit.py", atlas_current["driver_sha256"],
                  "publication_atlas_driver_binding")
        current_hashes(atlas_current["sources"])
        require(not atlas_current["failures"] and atlas_current["statuses"].get("limit", 0) == 0,
                "publication_atlas_no_failure_or_limit")
        require([atlas_current["totals"][k] for k in ("graphs", "conditions", "solver_calls")]
                == [1253, 3755, 7510], "publication_atlas_coverage")
        for previous_dir in (dirs["counterexamples"], dirs["repairs"]):
            previous_atlas = load(previous_dir / "atlas_results.json")
            require(atlas_current["result_sha256"] == previous_atlas["result_sha256"],
                    "publication_atlas_same_verdict_and_witness_digest", previous_dir.name)
        publication_atlas.update(path=str(atlas_current_path.relative_to(root)),
                                 sha256=digest(atlas_current_path.read_bytes()),
                                 totals=atlas_current["totals"], statuses=atlas_current["statuses"],
                                 result_sha256=atlas_current["result_sha256"])
        checked_files.add(atlas_current_path)

    inventory = []
    for name, directory in dirs.items():
        files = [p for p in directory.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
        large = [str(p.relative_to(root)) for p in files if p.stat().st_size > 1_000_000
                 and p.suffix in {".json", ".jsonl", ".ndjson", ".json5", ".bin"}]
        require(not large, "no_new_large_generated_exception_required", name)
        inventory.append(dict(name=name, files=len(files), bytes=sum(p.stat().st_size for p in files),
                              largest_bytes=max((p.stat().st_size for p in files), default=0)))
    output = dict(passed=not errors, checks=dict(counts), errors=errors, inventory=inventory,
                  verified_file_hash_paths=len(checked_files), preserved_snapshot_paths=len(snapshots),
                  current_source_paths=len(current_sources), original_base_commit=base,
                  historical_routing_docs=historical_routing_docs,
                  historical_source_gaps=historical_source_gaps,
                  publication_atlas=publication_atlas,
                  archive_only_not_reexecuted=["kernel_benchmark.json timing/random receipts",
                                               "rejected_absorption.json", "rejected_prefix_index.json",
                                               "rejected_bitset.json", "browser.json"],
                  scope="Saved evidence integrity, exact historical/current source bindings, protocol consistency and final original-graph witnesses. No solver, benchmark, random search, complete fibre reconstruction, or seed-17 replay executed by this checker. Routing document changes are explicit historical deltas.",
                  auditor_sha256=digest(Path(__file__).read_bytes()))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print(json.dumps(dict(passed=not errors, checks=sum(counts.values()), errors=errors,
                         inventory=inventory), ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
