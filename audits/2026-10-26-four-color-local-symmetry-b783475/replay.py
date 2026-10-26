#!/usr/bin/env python3
"""Compare literal and domain-preserving colour-orbit separator caches.

Small cases independently materialize full separator relations and check every
literal yes/no reply. Three wider cases use original-edge DSATUR for the final
decision only; their individual replies are NOT full-table verified. Timing is
written separately and is excluded from the deterministic evidence report.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import importlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
BASE = "b783475a1cc24ff126c09ad276816a3b7eb4e8d8"
SOURCE_NAMES = ("four_color_local_messages.py", "four_color_lab.py", "four_color_serialization.py")
REFERENCE = ROOT / "audits/2026-10-26-four-color-local-messages-f30cd6f/replay.py"
CAPS = dict(max_checks=10_000_000, max_messages=1_000_000,
            max_cache_entries=1_000_000, transcript_limit=1_000_000,
            audit_metadata=True)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def file_digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load_reference():
    spec = importlib.util.spec_from_file_location("independent_eager_reference", REFERENCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ensure_baseline():
    destination = AUDIT / "baseline-source"
    destination.mkdir(exist_ok=True)
    for name in SOURCE_NAMES:
        data = subprocess.run(["git", "show", f"{BASE}:scripts/{name}"], cwd=ROOT,
                              check=True, stdout=subprocess.PIPE).stdout
        path = destination / name
        if path.exists():
            assert path.read_bytes() == data, f"frozen baseline differs: {path}"
        else:
            path.write_bytes(data)
    return destination


def load_solver(source):
    # Each module's globals keep its matching dependencies after removal from
    # sys.modules; no baseline call can accidentally use the current lab copy.
    for name in ("four_color_local_messages", "four_color_lab", "four_color_serialization"):
        sys.modules.pop(name, None)
    sys.path.insert(0, str(source.resolve()))
    try:
        module = importlib.import_module("four_color_local_messages")
        return module.solve_local_messages
    finally:
        sys.path.pop(0)


def grid(rows, columns, *, triangular=False, flip=False):
    edges = []
    for i in range(rows):
        for j in range(columns):
            x = i * columns + j
            if j + 1 < columns:
                edges.append([x, x + 1])
            if i + 1 < rows:
                edges.append([x, x + columns])
            if triangular and i + 1 < rows and j + 1 < columns:
                edges.append([x, x + columns + 1])
    if flip:
        assert triangular
        x = (rows // 2 - 1) * columns + (columns // 2 - 1)
        edges.remove([x, x + columns + 1])
        edges.append([x + 1, x + columns])
    return dict(vertices=list(range(rows * columns)), edges=edges, fixed=[])


def mycielski(graph):
    n = len(graph["vertices"])
    assert graph["vertices"] == list(range(n))
    edges = [list(edge) for edge in graph["edges"]]
    for u, v in graph["edges"]:
        edges.extend([[u, n + v], [v, n + u]])
    edges.extend([[n + i, 2 * n] for i in range(n)])
    return dict(vertices=list(range(2 * n + 1)), edges=edges, fixed=[])


def make_cases(reference):
    cases = [dict(name=name, graph=graph, domains=domains, expected=expected,
                  reply_reference="complete same-decomposition eager tables")
             for name, graph, domains, expected in reference.make_cases()]
    k4 = dict(vertices=list(range(4)), edges=[list(e) for e in combinations(range(4), 2)], fixed=[])
    c5 = dict(vertices=list(range(5)), edges=[[i, (i + 1) % 5] for i in range(5)], fixed=[])
    extra = [
        ("three_point_positive_symmetry_hit",
         dict(vertices=[0, 1, 2], edges=[[0, 2], [1, 2]], fixed=[[1, 0]]), None, True, True),
        ("Mycielski_K4", mycielski(k4), None, False, True),
        ("triangular_grid_4x5_three_colours", grid(4, 5, triangular=True), None, True, True),
        ("flipped_triangular_grid_4x5_three_colours", grid(4, 5, triangular=True, flip=True), None, False, True),
        ("triangular_grid_6x7_fixed_corners_three_colours", grid(6, 7, triangular=True), None, False, True),
        ("flipped_triangular_grid_8x9_three_colours", grid(8, 9, triangular=True, flip=True), None, False, False),
        ("grid_9x10", grid(9, 10), None, True, False),
        ("Mycielski_twice_C5", mycielski(mycielski(c5)), None, False, False),
    ]
    for name, graph, domains, expected, full in extra:
        if "three_colours" in name:
            domains = {v: [0, 1, 2] for v in graph["vertices"]}
        if "fixed_corners" in name:
            graph["fixed"] = [[0, 0], [len(graph["vertices"]) - 1, 0]]
        cases.append(dict(name=name, graph=graph, domains=domains, expected=expected,
                          reply_reference=("complete same-decomposition eager tables" if full
                                           else "protocol checks only; individual reply semantics not full-table verified")))
    assert len(cases) == 17
    return cases


def original_edge_dsatur(graph, domains):
    """Independent exhaustive DFS; no bags, colour symmetry or planar theorem.

    Select a vertex by saturation/degree/input position, and try all permitted
    literal colours. It stops at one full witness or exhausts all branches.
    """
    vertices = graph["vertices"]
    positions = {v: i for i, v in enumerate(vertices)}
    allowed = {v: set((domains or {}).get(v, range(4))) for v in vertices}
    for v, colour in graph.get("fixed", []):
        allowed[v] &= {colour}
    allowed = {v: tuple(sorted(values)) for v, values in allowed.items()}
    adjacent = {v: set() for v in vertices}
    for u, v in graph["edges"]:
        adjacent[u].add(v)
        adjacent[v].add(u)
    assignment = {}
    counts = dict(search_nodes=0, colour_trials=0)

    def visit():
        counts["search_nodes"] += 1
        if len(assignment) == len(vertices):
            return True
        vertex = max((v for v in vertices if v not in assignment),
                     key=lambda v: (len({assignment[u] for u in adjacent[v] if u in assignment}),
                                    len(adjacent[v]), -positions[v]))
        forbidden = {assignment[u] for u in adjacent[vertex] if u in assignment}
        for colour in allowed[vertex]:
            counts["colour_trials"] += 1
            if colour in forbidden:
                continue
            assignment[vertex] = colour
            if visit():
                return True
        assignment.pop(vertex, None)
        return False

    possible = visit()
    return dict(possible=possible, counts=counts,
                colors=[assignment[v] for v in vertices] if possible else None,
                algorithm="original-edge literal-colour exhaustive DSATUR DFS")


def validate_witness(graph, domains, colors):
    assert colors is not None and len(colors) == len(graph["vertices"])
    assignment = dict(zip(graph["vertices"], colors))
    assert all(type(c) is int and 0 <= c < 4 for c in colors)
    assert all(assignment[u] != assignment[v] for u, v in graph["edges"])
    assert all(assignment[v] == c for v, c in graph.get("fixed", []))
    assert all(assignment[v] in values for v, values in (domains or {}).items())


def validate_decomposition(graph, decomposition):
    bags = decomposition["bags"]
    assert decomposition["validated"] and len(bags) == len(graph["vertices"])
    assert set(decomposition["order"]) == set(graph["vertices"])
    assert len(set(decomposition["order"])) == len(graph["vertices"])
    assert decomposition["roots"] == [b["id"] for b in bags if b["parent"] is None]
    allocated = []
    for b, bag in enumerate(bags):
        assert b == bag["id"]
        assert set(bag["vertices"]) == {bag["vertex"], *bag["separator"]}
        parent = bag["parent"]
        if parent is not None:
            assert parent > b and b in bags[parent]["children"]
            assert set(bag["separator"]) == set(bag["vertices"]) & set(bags[parent]["vertices"])
        else:
            assert not bag["separator"]
        assert bag["children"] == [i for i, child in enumerate(bags) if child["parent"] == b]
        for edge in bag["local_edges"]:
            assert set(edge) <= set(bag["vertices"])
            allocated.append(frozenset(edge))
    assert sorted(map(sorted, allocated)) == sorted(map(sorted, map(frozenset, graph["edges"])))
    for vertex in graph["vertices"]:
        scope = {b for b, bag in enumerate(bags) if vertex in bag["vertices"]}
        assert scope
        seen = set()
        pending = [min(scope)]
        while pending:
            b = pending.pop()
            if b in seen:
                continue
            seen.add(b)
            pending.extend(i for i in [*bags[b]["children"], bags[b]["parent"]]
                           if i in scope and i not in seen)
        assert seen == scope


def validate_messages(result, relations=None):
    assert not result["transcript_truncated"]
    bags = result["decomposition"]["bags"]
    queries = {}
    replied = set()
    distinct_nonroot = set()
    colour_values = 0
    positive_hits = 0
    for event in result["transcript"]:
        common = {"kind", "query_id", "bag", "sender", "receiver", "separator", "colors"}
        is_query = event["kind"] == "query"
        assert set(event) == (common if is_query else common | {"possible", "cached"})
        bag = bags[event["bag"]]
        assert event["separator"] == bag["separator"]
        assert len(event["colors"]) == len(bag["separator"])
        assert all(type(c) is int and 0 <= c < 4 for c in event["colors"])
        assert event["bag"] == (event["receiver"] if is_query else event["sender"])
        assert bag["parent"] == (event["sender"] if is_query else event["receiver"])
        colour_values += len(event["colors"])
        query_id = event["query_id"]
        if is_query:
            assert query_id not in queries
            queries[query_id] = event
            if bag["parent"] is not None:
                distinct_nonroot.add((event["bag"], tuple(event["colors"])))
        else:
            assert query_id in queries and query_id not in replied
            replied.add(query_id)
            query = queries[query_id]
            assert all(event[field] == query[field] for field in ("bag", "separator", "colors"))
            assert type(event["possible"]) is bool and type(event["cached"]) is bool
            positive_hits += event["possible"] and event["cached"]
            if relations is not None:
                assert event["possible"] == (tuple(event["colors"]) in relations[event["bag"]])
    assert set(queries) == replied
    assert len(queries) == result["stats"]["queries"] == result["stats"]["replies"]
    assert len(result["transcript"]) == result["stats"]["messages"]
    return dict(distinct_nonroot_literal_tuples=len(distinct_nonroot),
                colour_values_sent_both_directions=colour_values,
                positive_cached_replies=positive_hits,
                protocol_and_pairing_checked=True,
                all_reply_semantics_full_table_checked=relations is not None)


def summarize(result, message_checks):
    return dict(status=result["status"], colors=result["colors"], stats=result["stats"],
                limit_reason=result["limit_reason"],
                eager_tables_built=result["eager_tables_built"],
                cache_declared_complete=result["cache_declared_complete"],
                transcript_sha256=digest(result["transcript"]),
                decomposition_sha256=digest(result["decomposition"]),
                transcript_events=len(result["transcript"]), message_checks=message_checks)


def assert_literal_unchanged(baseline, current):
    reduced = deepcopy(current)
    reduced.pop("color_symmetry")
    assert reduced["stats"].pop("symmetry_bags") == 0
    assert reduced["stats"].pop("symmetry_cache_hits") == 0
    assert reduced == baseline, "default literal solver differs from frozen baseline"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "scripts")
    parser.add_argument("--out", type=Path, default=AUDIT / "report.json")
    parser.add_argument("--timing-out", type=Path, default=AUDIT / "timing.json")
    args = parser.parse_args()
    reference = load_reference()
    baseline_source = ensure_baseline()
    baseline_solve = load_solver(baseline_source)
    current_solve = load_solver(args.source)
    records = []
    timings = []
    for case in make_cases(reference):
        name, graph, domains = case["name"], case["graph"], case["domains"]
        case_times = dict(name=name, seconds={})
        started = time.perf_counter()
        oracle = original_edge_dsatur(graph, domains)
        case_times["seconds"]["original_edge_oracle"] = time.perf_counter() - started
        assert oracle["possible"] == case["expected"], name
        if oracle["possible"]:
            validate_witness(graph, domains, oracle["colors"])
        raw_modes = {}
        for mode in ("baseline", "literal", "symmetry"):
            started = time.perf_counter()
            if mode == "baseline":
                result = baseline_solve(graph, domains=domains, **CAPS)
            else:
                result = current_solve(graph, domains=domains, color_symmetry=mode == "symmetry", **CAPS)
            case_times["seconds"][mode] = time.perf_counter() - started
            assert result["status"] == ("colored" if oracle["possible"] else "unsatisfiable"), (name, mode)
            if oracle["possible"]:
                validate_witness(graph, domains, result["colors"])
            else:
                assert result["colors"] is None and result["stats"]["writeback_vertices"] == 0
            assert not result["eager_tables_built"] and not result["cache_declared_complete"]
            validate_decomposition(graph, result["decomposition"])
            raw_modes[mode] = result
        assert_literal_unchanged(raw_modes["baseline"], raw_modes["literal"])
        assert raw_modes["literal"]["decomposition"] == raw_modes["symmetry"]["decomposition"]
        relations = None
        eager = None
        if case["reply_reference"] == "complete same-decomposition eager tables":
            started = time.perf_counter()
            possible, relations, eager_stats = reference.eager_reference(graph, domains, raw_modes["literal"]["decomposition"])
            case_times["seconds"]["eager_reference"] = time.perf_counter() - started
            assert possible == oracle["possible"]
            eager = dict(stats=eager_stats,
                         full_relation_sha256=digest({b: sorted(rows) for b, rows in relations.items()}))
        modes = {mode: summarize(result, validate_messages(result, relations))
                 for mode, result in raw_modes.items()}
        if name == "three_point_positive_symmetry_hit":
            assert modes["symmetry"]["stats"]["symmetry_cache_hits"] > 0
            assert modes["symmetry"]["message_checks"]["positive_cached_replies"] > 0
        record = dict(name=name, graph=graph,
                      domains=None if domains is None else [[v, values] for v, values in sorted(domains.items())],
                      input_sha256=digest(dict(graph=graph, domains=None if domains is None else [[v, values] for v, values in sorted(domains.items())])),
                      expected=case["expected"], oracle=oracle,
                      reply_reference=case["reply_reference"], eager=eager, modes=modes,
                      baseline_literal_exact_match=True)
        records.append(record)
        timings.append(case_times)
        print(json.dumps(dict(name=name, status=modes["literal"]["status"],
                              width=modes["literal"]["stats"]["max_separator_size"],
                              literal_checks=modes["literal"]["stats"]["checks"],
                              symmetry_checks=modes["symmetry"]["stats"]["checks"],
                              literal_cache=modes["literal"]["stats"]["cache_entries"],
                              symmetry_cache=modes["symmetry"]["stats"]["cache_entries"],
                              symmetry_hits=modes["symmetry"]["stats"]["symmetry_cache_hits"])), flush=True)
    # A separate control uses the actual API defaults for all three work and
    # storage caps. Transcript suppression changes logging only. Unlike the
    # seventeen main cases, these two runs have no per-message validation.
    default_case = next(c for c in records if c["name"] == "Mycielski_twice_C5")
    default_graph = default_case["graph"]
    started = time.perf_counter()
    default_oracle = original_edge_dsatur(default_graph, None)
    default_times = dict(original_edge_oracle=time.perf_counter() - started)
    assert default_oracle == default_case["oracle"]
    assert default_oracle["possible"] is False
    default_modes = {}
    for mode in ("literal", "symmetry"):
        started = time.perf_counter()
        result = current_solve(default_graph, domains=None,
                               color_symmetry=mode == "symmetry", transcript_limit=0)
        default_times[mode] = time.perf_counter() - started
        assert result["colors"] is None
        assert result["stats"]["writeback_vertices"] == 0
        assert not result["transcript"] and result["transcript_truncated"]
        if mode == "literal":
            assert result["status"] == "limit" and result["limit_reason"] == "max_messages"
            assert result["stats"]["messages"] == 100_000
            assert result["stats"]["checks"] <= 1_000_000
        else:
            assert result["status"] == "unsatisfiable" and result["limit_reason"] is None
            assert result["stats"]["checks"] <= 1_000_000
        assert result["stats"]["messages"] <= 100_000
        assert result["stats"]["cache_entries"] <= 100_000
        default_modes[mode] = summarize(result, dict(
            protocol_and_pairing_checked=False,
            all_reply_semantics_full_table_checked=False,
            reason="transcript_limit=0; no per-reply validation in this default-budget control"))
        default_modes[mode]["transcript_truncated"] = result["transcript_truncated"]
    default_control = dict(name="Mycielski_twice_C5_default_budget",
                           graph_case="Mycielski_twice_C5",
                           input_sha256=default_case["input_sha256"],
                           resource_caps=dict(max_checks=1_000_000, max_messages=100_000,
                                              max_cache_entries=100_000, transcript_limit=0,
                                              audit_metadata=False),
                           work_and_storage_caps_passed_explicitly=False,
                           oracle=default_oracle, modes=default_modes,
                           assertions=dict(literal_limit_is_inconclusive=True,
                                           literal_limit_reason_is_max_messages=True,
                                           symmetry_exact_unsatisfiable_matches_original_edge_DFS=True,
                                           neither_mode_returns_partial_coloring=True,
                                           no_per_reply_validation_claim=True))
    print(json.dumps(dict(name=default_control["name"],
                          literal_status=default_modes["literal"]["status"],
                          literal_checks=default_modes["literal"]["stats"]["checks"],
                          symmetry_status=default_modes["symmetry"]["status"],
                          symmetry_checks=default_modes["symmetry"]["stats"]["checks"])), flush=True)
    report = dict(baseline_commit=BASE, resource_caps=CAPS,
                  sources={name: file_digest(args.source / name) for name in SOURCE_NAMES},
                  baseline_sources={name: file_digest(baseline_source / name) for name in SOURCE_NAMES},
                  driver_sha256=file_digest(Path(__file__)),
                  eager_reference=dict(path=str(REFERENCE.relative_to(ROOT)), sha256=file_digest(REFERENCE)),
                  cases=records, default_budget_control=default_control,
                  assertions=dict(cases=17, modes_per_case=3,
                                  all_decisions_match_independent_original_edge_DFS=True,
                                  all_colored_witnesses_checked_on_original_edges_domains_fixed=True,
                                  all_decompositions_independently_validated=True,
                                  all_literal_results_identical_to_frozen_baseline_except_new_zero_stats_and_flag=True,
                                  full_reply_semantic_checks_cases=sum(c["eager"] is not None for c in records),
                                  large_cases_without_full_reply_semantic_checks=[c["name"] for c in records if c["eager"] is None],
                                  complete_untruncated_protocol_transcripts_checked_all_cases=True,
                                  no_eager_tables_or_complete_cache_claims=True),
                  scope="Seventeen named finite conditions. Full-table reply semantics checked only on fourteen explicitly marked cases; three wider cases have an independent final decision oracle and message protocol checks. A separate default-budget Mycielski-twice-C5 control compares literal limit with exact symmetry unsatisfiability; it suppresses transcripts and has no per-reply validation claim. Timing is separate. No universal speedup, fixed-width, complete-fibre enumeration, privacy or planar four-colour theorem claim.")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    args.timing_out.parent.mkdir(parents=True, exist_ok=True)
    args.timing_out.write_text(json.dumps(dict(cases=timings, default_budget_control_seconds=default_times,
                                             source_report_sha256=file_digest(args.out),
                                             metric="One sequential wall-clock run; not a general performance guarantee."),
                                        sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
