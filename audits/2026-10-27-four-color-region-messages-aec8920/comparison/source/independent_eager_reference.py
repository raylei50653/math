#!/usr/bin/env python3
"""Independent full-table reference for the same lazy-message bag tree.

Report contains only deterministic counts; timing is deliberately separate.
The reference materializes complete relations and never calls a production
feasibility helper.  It also validates each public yes/no response.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent


def make_cases():
    frozen = ROOT / "audits/2026-10-26-four-color-counterexamples-f30cd6f"
    original = json.loads((frozen / "propagation/inputs.json").read_text())["graph"]
    bare = dict(original, fixed=[])
    positive = dict(original, edges=[e for e in original["edges"] if e != [7, 13]])
    cycle = lambda n: dict(vertices=list(range(n)),
                           edges=[[i, (i + 1) % n] for i in range(n)], fixed=[])
    star = dict(vertices=list(range(5)), edges=[[0, i] for i in range(1, 5)], fixed=[])
    k5 = dict(vertices=list(range(5)), edges=[[i, j] for i in range(5)
                                            for j in range(i + 1, 5)], fixed=[])
    return [
        ("fourteen_fixed", original, None, False),
        ("fourteen_bare", bare, None, True),
        ("fourteen_remove_7_13", positive, None, True),
        ("grid_6x7", json.loads((frozen / "grid_6x7.json").read_text()), None, True),
        ("two_colour_C5", cycle(5), {v: [0, 1] for v in range(5)}, False),
        ("two_colour_C6", cycle(6), {v: [0, 1] for v in range(6)}, True),
        ("four_leaf_star", star, None, True),
        ("four_leaf_star_blocked", dict(star, fixed=[[i + 1, i] for i in range(4)]), None, False),
        ("K5", k5, None, False),
    ]


def effective_domains(graph, domains):
    result = {v: set(range(4)) for v in graph["vertices"]}
    for v, values in (domains or {}).items():
        result[v] &= set(values)
    for v, c in graph.get("fixed", []):
        result[v] &= {c}
    return result


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# The production decomposition schema is consumed below.  Only the public bags,
# their separator order and topology are shared with the independent reference.


def eager_reference(graph, domains, decomposition):
    allowed = effective_domains(graph, domains)
    bags = decomposition["bags"]
    rank = {v: i for i, v in enumerate(decomposition["order"])}
    relations = {}
    stats = dict(candidate_rows=0, edge_checks=0, child_lookups=0,
                 full_support_rows=0, nonroot_full_support_rows=0,
                 nonroot_domain_tuple_universe=0, nonroot_full_support_color_values=0)
    allocated = {b["id"]: [] for b in bags}
    for u, v in graph["edges"]:
        allocated[min(rank[u], rank[v])].append((u, v))
    for bag in bags:
        b = bag["id"]
        assert all(child in relations for child in bag["children"])
        assert {frozenset(e) for e in allocated[b]} == {
            frozenset(e) for e in bag["local_edges"]}
        result = set()
        for values in product(*(sorted(allowed[v]) for v in bag["vertices"])):
            stats["candidate_rows"] += 1
            assignment = dict(zip(bag["vertices"], values))
            valid = True
            for u, v in allocated[b]:
                stats["edge_checks"] += 1
                if assignment[u] == assignment[v]:
                    valid = False
                    break
            if not valid:
                continue
            for child in bag["children"]:
                stats["child_lookups"] += 1
                key = tuple(assignment[v] for v in bags[child]["separator"])
                if key not in relations[child]:
                    valid = False
                    break
            if valid:
                result.add(tuple(assignment[v] for v in bag["separator"]))
        relations[b] = result
        stats["full_support_rows"] += len(result)
        if bag["parent"] is not None:
            stats["nonroot_full_support_rows"] += len(result)
            stats["nonroot_full_support_color_values"] += len(result) * len(bag["separator"])
            total = 1
            for v in bag["separator"]:
                total *= len(allowed[v])
            stats["nonroot_domain_tuple_universe"] += total
    possible = all(() in relations[root] for root in decomposition["roots"])
    return possible, relations, stats


def run_case(name, graph, domains, expected, solve, verify_coloring):
    result = solve(graph, domains=domains, max_checks=10_000_000,
                   max_messages=1_000_000, max_cache_entries=1_000_000,
                   transcript_limit=1_000_000, audit_metadata=True)
    assert not result["transcript_truncated"], name
    assert result["status"] == ("colored" if expected else "unsatisfiable"), (name, result)
    if expected:
        assert verify_coloring(graph, result["colors"]), name
        allowed = effective_domains(graph, domains)
        assert all(c in allowed[v] for v, c in zip(graph["vertices"], result["colors"]))
    else:
        assert result["colors"] is None
        assert result["stats"]["writeback_vertices"] == 0
    possible, relations, reference_stats = eager_reference(graph, domains, result["decomposition"])
    assert possible == expected, name
    queries = {}
    unique_nonroot = set()
    positive_nonroot = set()
    all_nonroot = 0
    nonroot_color_values = 0
    for event in result["transcript"]:
        if event["kind"] == "query":
            queries[event["query_id"]] = event
            if event["sender"] is not None:
                all_nonroot += 1
                unique_nonroot.add((event["receiver"], tuple(event["colors"])))
        else:
            query = queries[event["query_id"]]
            assert event["sender"] == query["receiver"]
            assert event["receiver"] == query["sender"]
            assert event["colors"] == query["colors"]
            key = tuple(event["colors"])
            assert event["possible"] == (key in relations[query["receiver"]]), (name, event)
            if event["receiver"] is not None and event["possible"]:
                positive_nonroot.add((event["sender"], key))
        if event["separator"]:
            nonroot_color_values += len(event["colors"])
    record = dict(name=name, graph=graph,
                  domains=None if domains is None else [[v, c] for v, c in sorted(domains.items())],
                  status=result["status"], colors=result["colors"], stats=result["stats"],
                  queried_nonroot_distinct_tuples=len(unique_nonroot),
                  positive_nonroot_distinct_tuples=len(positive_nonroot),
                  nonroot_queries_including_repeats=all_nonroot,
                  nonroot_color_values_sent_both_directions=nonroot_color_values,
                  eager=reference_stats, transcript_sha256=digest(result["transcript"]),
                  full_relation_sha256=digest({b: sorted(rows) for b, rows in relations.items()}),
                  decomposition=result["decomposition"], transcript=result["transcript"])
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "scripts")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.source.resolve()))
    from four_color_local_messages import solve_local_messages
    from four_color_lab import verify_coloring
    records = []
    for case in make_cases():
        record = run_case(*case, solve_local_messages, verify_coloring)
        records.append(record)
        print(json.dumps(dict(name=record["name"], status=record["status"],
                              queries=record["queried_nonroot_distinct_tuples"],
                              full_rows=record["eager"]["nonroot_full_support_rows"],
                              query_universe=record["eager"]["nonroot_domain_tuple_universe"],
                              width=record["stats"]["max_separator_size"],
                              checks=record["stats"]["checks"])), flush=True)
    source_names = ("four_color_local_messages.py", "four_color_lab.py", "four_color_serialization.py")
    report = dict(cases=records,
                  sources={name: sha256((args.source / name).read_bytes()).hexdigest()
                           for name in source_names},
                  driver_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  assertions=dict(original_graph_witnesses_checked=True,
                                  all_replies_match_independent_full_tables=True,
                                  all_case_decisions_match=True),
                  scope="Nine named conditions. Distinct queried tuples include yes and no; full support rows include only yes. They are not a common bit/CPU metric. No universal speedup, bounded-width, solution-counting, or cryptographic privacy claim.")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
