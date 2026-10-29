#!/usr/bin/env python3
"""Audit how much reconstruction information an exact four-colour solver needs.

This is a representation/reconstruction experiment, not a new solver mode.
All ordered boundary tuples remain present. Masks retain every colour; one
chosen colour per tuple retains a witness, but no longer all original solutions.
The production solver and its complete records are never modified by this audit.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import random
import sys

from four_color_constraints import solve_constraints


ROOT = Path(__file__).resolve().parents[1]
KINDS = ("full", "mask", "one_min", "one_max", "one_seed17")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def original_solutions(graph):
    """Independent literal Cartesian oracle: only original edges/fixed colours."""
    fixed = dict(graph.get("fixed", []))
    domains = [(fixed[v],) if v in fixed else range(4) for v in graph["vertices"]]
    for row in product(*domains):
        assignment = dict(zip(graph["vertices"], row))
        if all(assignment[u] != assignment[v] for u, v in graph["edges"]):
            yield list(row)


def valid_coloring(graph, colors):
    if len(colors) != len(graph["vertices"]) or any(type(c) is not int or c not in range(4)
                                                  for c in colors):
        return False
    assignment = dict(zip(graph["vertices"], colors))
    return (all(assignment[u] != assignment[v] for u, v in graph["edges"])
            and all(assignment[v] == c for v, c in graph.get("fixed", [])))


def encode_records(result, kind):
    """Compile separate maps; never label a one-witness map a complete fibre."""
    if kind not in KINDS:
        raise ValueError("unknown retention kind")
    if result["status"] not in ("colored", "unsatisfiable"):
        raise ValueError("a limited/stuck run cannot supply a complete result")
    if not result["record_relations"]:
        raise ValueError("complete source records are required")
    rng = random.Random(17)
    encoded = []
    for record in result["elimination_records"]:
        if not record["complete"]:
            raise ValueError("partial elimination record")
        table = {}
        for row in record["rows"]:
            boundary, choices = tuple(row["boundary"]), tuple(row["colors"])
            if (not choices or choices != tuple(sorted(set(choices)))
                    or any(type(c) is not int or c not in range(4) for c in choices)):
                raise ValueError("invalid nonempty fibre")
            if boundary in table or len(boundary) != len(record["scope"]):
                raise ValueError("invalid ordered boundary")
            if kind == "full":
                value = choices
            elif kind == "mask":
                value = sum(1 << c for c in choices)
            else:
                value = (min(choices) if kind == "one_min" else max(choices)
                         if kind == "one_max" else rng.choice(choices))
            table[boundary] = value
        if len(table) != record["relation_rows"]:
            raise ValueError("boundary rows were omitted")
        encoded.append((record["vertex"], tuple(record["scope"]), table))
    return encoded


def decode(value, kind):
    if kind == "full":
        return value
    if kind == "mask":
        return tuple(c for c in range(4) if value & (1 << c))
    return (value,)


def reconstruct(result, encoded, kind, *, largest=False):
    """Choose a common boundary before looking up its internal witness."""
    if result["status"] != "colored":
        raise ValueError("only complete successful elimination permits writeback")
    graph = result["graph"]
    eliminated = [v for v, _, _ in encoded]
    if len(eliminated) != len(set(eliminated)) or set(eliminated) != set(graph["vertices"]):
        raise ValueError("missing or duplicate elimination")
    assignment = dict(graph.get("fixed", []))
    for vertex, scope, table in reversed(encoded):
        boundary = tuple(assignment[v] for v in scope)
        choices = decode(table[boundary], kind)
        if vertex in assignment:
            if assignment[vertex] not in choices:
                raise AssertionError("fixed colour lost")
        else:
            assignment[vertex] = max(choices) if largest else min(choices)
    colors = [assignment[v] for v in graph["vertices"]]
    if not valid_coloring(graph, colors):
        raise AssertionError("invalid original-edge/fixed-colour witness")
    return colors


def object_bytes(value):
    """Deep Python object size of these maps only, with shared objects counted once.

    This excludes records, input factors, graph, indexes, interpreter and RSS.
    It measures reconstructed experimental objects, not production allocations.
    """
    seen = set()

    def visit(item):
        if id(item) in seen:
            return 0
        seen.add(id(item))
        size = sys.getsizeof(item)
        if isinstance(item, dict):
            return size + sum(visit(k) + visit(v) for k, v in item.items())
        if isinstance(item, (tuple, list)):
            return size + sum(map(visit, item))
        return size

    return visit(value)


def check_complete_joins(result):
    """Small inputs only: verify every present AND absent fibre by Cartesian join."""
    for record in result["elimination_records"]:
        vertices = [record["vertex"], *record["scope"]]
        domains = {item["vertex"]: item["colors"] for item in record["source_domains"]}
        inputs = [(r["scope"], set(map(tuple, r["rows"]))) for r in record["input_relations"]]
        expected = {}
        for row in product(*(domains[v] for v in vertices)):
            assignment = dict(zip(vertices, row))
            if all(tuple(assignment[v] for v in scope) in rows for scope, rows in inputs):
                expected.setdefault(row[1:], []).append(row[0])
        actual = {tuple(r["boundary"]): r["colors"] for r in record["rows"]}
        if actual != expected:
            raise AssertionError("saved fibres differ from the complete Cartesian join")


def audit_result(result, *, solutions=None):
    if solutions is not None:
        if result["status"] != ("colored" if solutions else "unsatisfiable"):
            raise AssertionError("solver disagrees with independent original-edge oracle")
        check_complete_joins(result)
    before = digest(result)
    full = encode_records(result, "full")
    histogram = Counter(len(choices) for _, _, table in full for choices in table.values())
    metrics = dict(status=result["status"], boundary_rows=sum(histogram.values()),
                   full_color_choices=sum(k * n for k, n in histogram.items()),
                   fibre_size_histogram=dict(sorted(histogram.items())),
                   map_object_bytes={}, writebacks_checked=0)
    if solutions is not None:
        for solution in solutions:
            assignment = dict(zip(result["graph"]["vertices"], solution))
            for vertex, scope, table in full:
                if assignment[vertex] not in table[tuple(assignment[v] for v in scope)]:
                    raise AssertionError("an original solution lost a full fibre")
    for kind in KINDS:
        encoded = full if kind == "full" else encode_records(result, kind)
        for (_, _, original), (_, _, compact) in zip(full, encoded, strict=True):
            if original.keys() != compact.keys():
                raise AssertionError("a boundary possibility was dropped")
            for boundary, choices in original.items():
                retained = decode(compact[boundary], kind)
                if (kind in ("full", "mask") and retained != choices
                        or kind.startswith("one_") and (len(retained) != 1 or retained[0] not in choices)):
                    raise AssertionError("representation violated its stated contract")
        metrics["map_object_bytes"][kind] = object_bytes(encoded)
        if result["status"] == "colored":
            for largest in ((False, True) if kind in ("full", "mask") else (False,)):
                colors = reconstruct(result, encoded, kind, largest=largest)
                if solutions is not None and colors not in solutions:
                    raise AssertionError("reconstruction missing from independent complete solutions")
                if kind in ("full", "mask", "one_min") and not largest and colors != result["colors"]:
                    raise AssertionError("minimum-choice reconstruction changed")
                metrics["writebacks_checked"] += 1
    if digest(result) != before:
        raise AssertionError("audit mutated the full source evidence")
    return metrics


def small_cases():
    # All 1,100 labelled simple graphs on 0..5 vertices, no planarity assumption.
    for n in range(6):
        pairs = list(combinations(range(n), 2))
        for bits in range(1 << len(pairs)):
            graph = dict(vertices=list(range(n)), edges=[list(e) for i, e in enumerate(pairs)
                                                         if bits & (1 << i)], fixed=[])
            yield "all_graphs_n0_to_n5", graph
            # All additional nonempty partial fixed assignments on 0..3 vertices.
            if n <= 3:
                for fixed in product(range(-1, 4), repeat=n):
                    if any(c >= 0 for c in fixed):
                        yield "all_nonempty_partial_fixed_n1_to_n3", dict(
                            graph, fixed=[[v, c] for v, c in enumerate(fixed) if c >= 0])
    rng = random.Random(20261026)
    for i in range(96):
        vertices = [40, -3, 900, 17, 0, 81]
        rng.shuffle(vertices)
        yield "seeded_n6_literal_frames", dict(
            vertices=vertices,
            edges=[list(e) for e in combinations(vertices, 2) if rng.random() < (i % 5 + 1) / 6],
            fixed=[[v, rng.randrange(4)] for v in vertices[:i % 5]])


def negative_controls():
    """Even retaining 231/232 star boundaries loses a possible exterior."""
    graph = dict(vertices=list(range(5)), edges=[[0, v] for v in range(1, 5)], fixed=[])
    relation = {}
    for colors in original_solutions(graph):
        relation.setdefault(tuple(colors[1:]), []).append(colors[0])
    rows = sorted(relation)
    controls = []
    for cap in (1, 2, 4, 8, 16, 64, 128, len(rows) - 1):
        target = rows[cap]
        context = dict(graph, fixed=[[v, c] for v, c in zip(range(1, 5), target)])
        solutions = list(original_solutions(context))
        if not solutions or target in rows[:cap]:
            raise AssertionError("negative control is not a false rejection")
        controls.append(dict(kept_boundary_rows=cap, full_boundary_rows=len(rows),
                             deleted_boundary=list(target), graph=context,
                             original_witness=solutions[0], original_status="colored",
                             truncated_interface_status="empty"))
    return controls


def summarize(rows):
    return dict(cases=len(rows), status_counts=dict(Counter(r["status"] for r in rows)),
                boundary_rows=sum(r["boundary_rows"] for r in rows),
                full_color_choices=sum(r["full_color_choices"] for r in rows),
                writebacks_checked=sum(r["writebacks_checked"] for r in rows),
                map_object_bytes_sum={k: sum(r["map_object_bytes"][k] for r in rows) for k in KINDS})


def run_audit(frozen_run=None):
    source_paths = sorted((ROOT / "scripts").glob("four_color*.py"))
    sources = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    grouped, case_digests = {}, []
    for group, graph in small_cases():
        result = solve_constraints(graph, use_substructures=False, use_conflicts=False,
                                   max_checks=1_000_000, max_table_rows=1_000_000,
                                   trace_limit=0, bucket_method="prefix")
        metrics = audit_result(result, solutions=list(original_solutions(graph)))
        grouped.setdefault(group, []).append(metrics)
        case_digests.append(digest(dict(graph=graph, status=result["status"], records=result["elimination_records"])))
    report = dict(schema="four-color-retention-audit-v1", python=sys.version.split()[0],
                  sources_sha256=sources, small_cases={k: summarize(v) for k, v in grouped.items()},
                  small_case_results_sha256=digest(case_digests), negative_controls=negative_controls(),
                  contracts=dict(full="all boundary rows and all fibre colours",
                                 mask="lossless four-bit fibre colours; all boundary rows",
                                 one="all boundary rows; one witness per row, NOT all solutions"),
                  scope="Post-elimination representation and reconstruction audit. No production "
                        "memory or speed claim. Object sizes cover experimental maps only, not "
                        "complete records or RSS. Small inputs use an independent exhaustive oracle; "
                        "larger inputs retain their existing per-case validation coverage.")
    if frozen_run is not None:
        raw_report = (frozen_run / "report.json").read_bytes()
        frozen = json.loads(raw_report)
        checked = []
        for case in frozen["cases"]:
            row = case["results"]["combined-contexts"]
            raw = (frozen_run / row["full_record"]).read_bytes()
            if hashlib.sha256(raw).hexdigest() != row["compressed_record_sha256"]:
                raise AssertionError("frozen full record changed")
            result = json.loads(gzip.decompress(raw))
            if result["graph_sha256"] != case["graph_sha256"] or result["status"] != case["reference_status"]:
                raise AssertionError("full record does not match its reference")
            checked.append(dict(name=case["name"], graph_sha256=case["graph_sha256"],
                                source_record_sha256=row["compressed_record_sha256"],
                                reference_coverage=case["reference_coverage"], **audit_result(result)))
        report["frozen_cases"] = checked
        report["frozen_totals"] = summarize(checked)
        report["frozen_report_sha256"] = hashlib.sha256(raw_report).hexdigest()
        report["frozen_sources"] = frozen["sources"]
        report["frozen_inputs_sha256"] = frozen["inputs_sha256"]
    if sources != {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}:
        raise AssertionError("audit sources changed during execution")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--frozen-run", type=Path,
                        help="completed four_color_flow_experiment output directory")
    args = parser.parse_args()
    if args.out.exists():
        parser.error("use a new output file to preserve previous evidence")
    report = run_audit(args.frozen_run)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(dict(small_cases=report["small_cases"],
                          frozen_totals=report.get("frozen_totals"),
                          negative_controls=len(report["negative_controls"])), indent=2))


if __name__ == "__main__":
    main()
