#!/usr/bin/env python3
"""Compare exact local-message decompositions, including all planning work.

The input suite includes geometric strips, triangular meshes and independently
seeded diagonals. Every original graph is checked by an independent literal
DSATUR oracle; smaller decompositions also have every reply checked against
complete eager subtree relations. Full transcripts are retained compressed.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import gzip
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from math import prod
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "audits/2026-10-26-four-color-local-messages-f30cd6f/replay.py"
STRATEGIES = ("min_fill", "min_degree", "geometric_sweep", "geometric_nested",
              "bfs_sweep", "bfs_nested")
SOURCE_NAMES = ("four_color_local_messages.py", "four_color_region_order.py",
                "four_color_lab.py", "four_color_serialization.py",
                "four_color_region_experiment.py")


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return sha256(encoded(value)).hexdigest()


def mesh(rows, columns, diagonals="none", seed=0):
    rng = random.Random(seed)
    edges = []
    for y in range(rows):
        for x in range(columns):
            v = y * columns + x
            if x + 1 < columns:
                edges.append([v, v + 1])
            if y + 1 < rows:
                edges.append([v, v + columns])
            if x + 1 < columns and y + 1 < rows and diagonals != "none":
                reverse = diagonals == "random" and rng.randrange(2)
                if diagonals == "flipped":
                    reverse = (y, x) == (rows // 2 - 1, columns // 2 - 1)
                edges.append([v + 1, v + columns] if reverse else [v, v + columns + 1])
    return dict(vertices=list(range(rows * columns)), edges=edges, fixed=[],
                positions=[[x, y] for y in range(rows) for x in range(columns)])


def make_cases():
    cases = []

    def add(name, graph, domains=None, cohort="development"):
        cases.append(dict(name=name, graph=graph, domains=domains, cohort=cohort))

    for rows, cols in ((4, 30), (6, 7), (9, 10), (12, 16)):
        add(f"grid_{rows}x{cols}", mesh(rows, cols))
    for rows, cols in ((6, 7), (8, 9)):
        graph = mesh(rows, cols, "triangular")
        add(f"triangular_{rows}x{cols}_four", graph)
        domains = {v: [0, 1, 2] for v in graph["vertices"]}
        add(f"triangular_{rows}x{cols}_three", graph, domains)
        fixed = deepcopy(graph)
        fixed["fixed"] = [[0, 0], [rows * cols - 1, 0]]
        add(f"triangular_{rows}x{cols}_three_fixed", fixed, domains)
        add(f"flipped_{rows}x{cols}_three", mesh(rows, cols, "flipped"), domains)
    for cohort, rows, cols, seeds in (("development", 6, 8, (17, 29)),
                                     ("confirmation", 7, 9, (101, 211))):
        for seed in seeds:
            graph = mesh(rows, cols, "random", seed)
            add(f"random_diagonals_{rows}x{cols}_s{seed}_four", graph, cohort=cohort)
            fixed = deepcopy(graph)
            rng = random.Random(seed + 1000)
            chosen = sorted(rng.sample(graph["vertices"], max(2, len(graph["vertices"]) // 8)))
            fixed["fixed"] = [[v, (v % cols) % 2 + 2 * ((v // cols) % 2)] for v in chosen]
            add(f"random_diagonals_{rows}x{cols}_s{seed}_fixed", fixed, cohort=cohort)
            add(f"random_diagonals_{rows}x{cols}_s{seed}_three", graph,
                {v: [0, 1, 2] for v in graph["vertices"]}, cohort)
    for rows, cols in ((5, 17), (10, 11)):
        add(f"confirmation_triangular_{rows}x{cols}_three", mesh(rows, cols, "triangular"),
            {v: [0, 1, 2] for v in range(rows * cols)}, "confirmation")
    # These two illustrations were identified in a separate exploratory probe;
    # keep them separate from the preselected development/confirmation cohort.
    add("probe_triangular_12x16_four", mesh(12, 16, "triangular"), cohort="probe_demonstration")
    for rows, cols, seed, cohort in ((8, 9, 4627, "probe_demonstration"),
                                     (7, 11, 919, "confirmation"),
                                     (10, 13, 2027, "confirmation")):
        graph = mesh(rows, cols, "triangular")
        rng = random.Random(seed)
        graph["fixed"] = [[v, ((v // cols) + (v % cols)) % 3]
                          for v in graph["vertices"] if rng.random() < .25]
        add(f"{cohort}_triangular_{rows}x{cols}_four_fixed_s{seed}", graph, cohort=cohort)
    for n in (5, 6):
        graph = dict(vertices=list(range(n)), edges=[[v, (v + 1) % n] for v in range(n)], fixed=[])
        add(f"two_colour_C{n}", graph, {v: [0, 1] for v in range(n)}, "control")
    add("K5", dict(vertices=list(range(5)), edges=[list(e) for e in combinations(range(5), 2)], fixed=[]),
        cohort="control")
    return cases


def original_oracle(graph, domains, max_trials=5_000_000):
    """Independent original-edge DFS; no decomposition or solver helpers."""
    vertices = graph["vertices"]
    rank = {v: i for i, v in enumerate(vertices)}
    allowed = {v: set((domains or {}).get(v, range(4))) for v in vertices}
    for v, colour in graph.get("fixed", []):
        allowed[v] &= {colour}
    adjacent = {v: set() for v in vertices}
    for u, v in graph["edges"]:
        adjacent[u].add(v)
        adjacent[v].add(u)
    assignment = {}
    trials = 0

    def visit():
        nonlocal trials
        if len(assignment) == len(vertices):
            return True
        v = min((v for v in vertices if v not in assignment),
                key=lambda v: (len(allowed[v] - {assignment[w] for w in adjacent[v] if w in assignment}),
                               -len(adjacent[v]), rank[v]))
        forbidden = {assignment[w] for w in adjacent[v] if w in assignment}
        for colour in sorted(allowed[v] - forbidden):
            trials += 1
            if trials > max_trials:
                raise RuntimeError("independent oracle budget exhausted")
            assignment[v] = colour
            if visit():
                return True
        assignment.pop(v, None)
        return False

    possible = visit()
    return dict(status="colored" if possible else "unsatisfiable", trials=trials,
                colors=[assignment[v] for v in vertices] if possible else None,
                method="independent original-edge literal MRV DFS")


def validate_witness(graph, domains, result):
    if result["status"] != "colored":
        assert result["colors"] is None
        assert result["stats"]["writeback_vertices"] == 0
        return
    colors = dict(zip(graph["vertices"], result["colors"]))
    assert len(colors) == len(graph["vertices"])
    assert all(type(c) is int and c in range(4) for c in colors.values())
    assert all(colors[u] != colors[v] for u, v in graph["edges"])
    assert all(colors[v] == c for v, c in graph.get("fixed", []))
    assert all(colors[v] in values for v, values in (domains or {}).items())


def message_counts(result):
    decomposition = result["decomposition"]
    if decomposition is None:
        return dict(nonroot_queries=0, nonroot_events=0, tuple_color_values=0,
                    logical_payload_bits=0, nonroot_unique_queries=0)
    bags = decomposition["bags"]
    events = [e for e in result["transcript"] if bags[e["bag"]]["parent"] is not None]
    queries = [e for e in events if e["kind"] == "query"]
    values = sum(len(e["colors"]) for e in events)
    return dict(nonroot_queries=len(queries), nonroot_events=len(events), tuple_color_values=values,
                logical_payload_bits=2 * values + sum(e["kind"] == "reply" for e in events),
                nonroot_unique_queries=len({(e["bag"], tuple(e["colors"])) for e in queries}))


def run(out, max_checks, only=None, strategies=STRATEGIES, full_table_cap=500_000):
    from four_color_local_messages import solve_local_messages
    from four_color_region_order import build_region_order
    spec = importlib.util.spec_from_file_location("region_eager_reference", REFERENCE)
    reference = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reference)
    out.mkdir(parents=True, exist_ok=False)
    (out / "runs").mkdir()
    (out / "source").mkdir()
    for name in SOURCE_NAMES:
        (out / "source" / name).write_bytes((Path(__file__).parent / name).read_bytes())
    (out / "source" / "independent_eager_reference.py").write_bytes(REFERENCE.read_bytes())
    records, timings, inputs = [], [], []
    for case in make_cases():
        if only and not any(token in case["name"] for token in only):
            continue
        graph, domains = case["graph"], case["domains"]
        oracle = original_oracle(graph, domains)
        inputs.append(dict(case, oracle=oracle))
        for strategy in strategies:
            if strategy.startswith("geometric") and "positions" not in graph:
                continue
            start = time.perf_counter()
            plan = None
            if strategy != "min_fill":
                plan = build_region_order(graph, strategy, max_checks=max_checks)
                planning_checks = plan["stats"]["checks"]
            else:
                planning_checks = 0
            planned_at = time.perf_counter()
            if plan is not None and plan["status"] == "limit":
                result = dict(status="limit", colors=None, decomposition=None, transcript=[],
                              stats=dict(checks=0, writeback_vertices=0), limit_reason="planning")
            else:
                result = solve_local_messages(graph, domains=domains,
                    elimination_order=None if plan is None else plan["order"],
                    max_checks=max_checks - planning_checks, max_messages=1_000_000,
                    max_cache_entries=1_000_000, transcript_limit=1_000_000,
                    audit_metadata=True, color_symmetry=False)
                assert not result["transcript_truncated"]
            solved_at = time.perf_counter()
            validate_witness(graph, domains, result)
            assert result["status"] == "limit" or result["status"] == oracle["status"], (case["name"], strategy)
            audit = dict(kind="original-edge final decision and witness; replies not exhaustively verified")
            if result["decomposition"] is not None:
                allowed = reference.effective_domains(graph, domains)
                candidate_rows = sum(prod(len(allowed[v]) for v in bag["vertices"])
                                     for bag in result["decomposition"]["bags"])
                if candidate_rows <= full_table_cap:
                    possible, relations, eager_stats = reference.eager_reference(graph, domains, result["decomposition"])
                    assert possible == (oracle["status"] == "colored")
                    for event in result["transcript"]:
                        if event["kind"] == "reply":
                            assert event["possible"] == (tuple(event["colors"]) in relations[event["bag"]])
                    audit = dict(kind="all replies verified against complete same-decomposition relations",
                                 eager_stats=eager_stats,
                                 relation_sha256=digest({b: sorted(rows) for b, rows in relations.items()}))
                else:
                    audit["eager_candidate_rows"] = candidate_rows
            full = dict(case=case["name"], strategy=strategy, graph_sha256=digest(graph),
                        domains_sha256=digest(domains), plan=plan, result=result, audit=audit)
            data = encoded(full)
            filename = f"{case['name']}--{strategy}.json.gz"
            (out / "runs" / filename).write_bytes(gzip.compress(data, mtime=0))
            record = dict(name=case["name"], cohort=case["cohort"], strategy=strategy,
                          vertices=len(graph["vertices"]), edges=len(graph["edges"]),
                          status=result["status"], limit_reason=result.get("limit_reason"),
                          max_separator=result["stats"].get("max_separator_size"),
                          potential_separator_rows=result["stats"].get("potential_separator_rows"),
                          planning_checks=planning_checks, solver_checks=result["stats"]["checks"],
                          total_checks=planning_checks + result["stats"]["checks"],
                          audit=audit, evidence=f"runs/{filename}", evidence_sha256=sha256(data).hexdigest(),
                          **message_counts(result))
            records.append(record)
            timings.append(dict(name=case["name"], strategy=strategy,
                                planning_seconds=planned_at-start, solving_seconds=solved_at-planned_at,
                                total_seconds=solved_at-start))
            print(json.dumps({k: record[k] for k in ("name", "strategy", "status", "max_separator",
                                                    "tuple_color_values", "total_checks")}), flush=True)
            # Durable partial progress if an external interrupt ends the experiment.
            (out / "progress.json").write_bytes(encoded(records))
    report = dict(max_checks=max_checks, color_symmetry=False, full_table_cap=full_table_cap,
                  payload_definition="sum of full separator color tuple lengths for all nonroot query and reply events; IDs and transport framing excluded",
                  logical_bits_definition="two bits per tuple color plus one bit per boolean reply; not serialized bytes",
                  cases=inputs, records=records,
                  sources={name: sha256((out / "source" / name).read_bytes()).hexdigest()
                           for name in (*SOURCE_NAMES, "independent_eager_reference.py")})
    (out / "report.json").write_bytes(encoded(report))
    (out / "timings.json").write_bytes(encoded(timings))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-checks", type=int, default=2_000_000)
    parser.add_argument("--only", nargs="+")
    parser.add_argument("--strategies", nargs="+", choices=STRATEGIES, default=STRATEGIES)
    parser.add_argument("--full-table-cap", type=int, default=500_000)
    args = parser.parse_args()
    run(args.out, args.max_checks, args.only, args.strategies, args.full_table_cap)


if __name__ == "__main__":
    main()
