#!/usr/bin/env python3
"""Recount saved messages and verify frozen/default compatibility."""
import argparse
import gzip
from hashlib import sha256
import importlib
import json
from pathlib import Path
import sys

AUDIT = Path(__file__).resolve().parent


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_solver(source):
    for name in ("four_color_local_messages", "four_color_lab", "four_color_serialization"):
        sys.modules.pop(name, None)
    sys.path.insert(0, str(source))
    try:
        return importlib.import_module("four_color_local_messages").solve_local_messages
    finally:
        sys.path.pop(0)


def verify(directory):
    report = json.loads((directory / "report.json").read_text())
    for name, expected in report["sources"].items():
        assert sha256((directory / "source" / name).read_bytes()).hexdigest() == expected
    cases = {case["name"]: case for case in report["cases"]}
    counts = dict(runs=0, complete=0, limits=0, positive_witnesses=0,
                  full_reply_reference_runs=0, recounted_events=0)
    for record in report["records"]:
        data = gzip.decompress((directory / record["evidence"]).read_bytes())
        assert sha256(data).hexdigest() == record["evidence_sha256"]
        full = json.loads(data)
        case = cases[record["name"]]
        graph = case["graph"]
        domains = {int(v): cs for v, cs in (case["domains"] or {}).items()}
        result = full["result"]
        assert full["graph_sha256"] == digest(graph)
        assert full["domains_sha256"] == digest(None if case["domains"] is None else domains)
        assert result["status"] == record["status"]
        assert record["total_checks"] == record["planning_checks"] + result["stats"]["checks"]
        assert record["total_checks"] <= report["max_checks"]
        if result["status"] == "limit":
            counts["limits"] += 1
            assert result["colors"] is None
        else:
            counts["complete"] += 1
            assert result["status"] == case["oracle"]["status"]
        if result["status"] == "colored":
            colors = dict(zip(graph["vertices"], result["colors"]))
            assert len(colors) == len(graph["vertices"])
            assert all(type(c) is int and c in range(4) for c in colors.values())
            assert all(colors[u] != colors[v] for u, v in graph["edges"])
            assert all(colors[v] == c for v, c in graph.get("fixed", []))
            assert all(colors[v] in values for v, values in domains.items())
            counts["positive_witnesses"] += 1
        assert not result.get("transcript_truncated", False)
        bags = (result.get("decomposition") or {}).get("bags", [])
        values = events = queries = replies = 0
        distinct = set()
        for event in result["transcript"]:
            if bags[event["bag"]]["parent"] is None:
                continue
            values += len(event["colors"])
            events += 1
            if event["kind"] == "query":
                queries += 1
                distinct.add((event["bag"], tuple(event["colors"])))
            else:
                replies += 1
        assert record["tuple_color_values"] == values
        assert record["logical_payload_bits"] == 2 * values + replies
        assert record["nonroot_queries"] == queries
        assert record["nonroot_unique_queries"] == len(distinct)
        assert record["nonroot_events"] == events
        counts["recounted_events"] += events
        counts["runs"] += 1
        counts["full_reply_reference_runs"] += full["audit"]["kind"].startswith("all replies verified")
    baseline = load_solver(AUDIT / "baseline-source")
    current = load_solver(directory / "source")
    comparisons = []
    for case in cases.values():
        domains = (None if case["domains"] is None else
                   {int(v): cs for v, cs in case["domains"].items()})
        options = dict(domains=domains, max_checks=report["max_checks"], max_messages=1_000_000,
                       max_cache_entries=1_000_000, transcript_limit=1_000_000, audit_metadata=True)
        before = baseline(case["graph"], **options)
        after = current(case["graph"], **options)
        assert before == after, case["name"]
        comparisons.append(dict(name=case["name"], status=after["status"], sha256=digest(after)))
    return dict(counts=counts, baseline_default_exact_equal=comparisons,
                source_hashes_verified=True, evidence_hashes_verified=True,
                all_messages_recounted=True, all_returned_witnesses_original_edges_checked=True,
                scope="recount and final witnesses; complete-reply reference results are from experiment, not repeated here")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=AUDIT / "verified")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    receipt = verify(args.directory)
    args.out.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print(json.dumps(receipt["counts"], sort_keys=True))
