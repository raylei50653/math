#!/usr/bin/env python3
"""Audit automatic nine-point joint factors on thirty original-edge contexts.

Compare historical shared-interface/cycle/context propagation with the same
solver plus automatic named-pattern matching.  Every original solution is
independently enumerated and retained, including all twenty-one edge-deletion
controls.  This is a finite preservation and early-detection receipt, not a
claim that arbitrary joint restrictions are discovered.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

from four_color_conflict_priority import (
    original_solutions,
    pre_elimination_metrics,
    verify_preservation,
)
from four_color_constraints import solve_constraints
from four_color_joint_constraint_audit import (
    DEFAULT_ROLE_MAPPING,
    FACTOR_ID,
    FIXED_GRAPH_SHA256,
    FROZEN_INPUT,
    FROZEN_INPUT_SHA256,
    UNFIXED_GRAPH_SHA256,
    instantiate_nine_point_constraint,
)
from four_color_lab import graph_fingerprint, normalize_graph, verify_coloring


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "artifacts/four_color_joint_propagation"
MAX_CHECKS = 5_000_000
MODES = {
    "historical": {"use_joint_constraints": False},
    "joint": {"use_joint_constraints": True},
}
SOURCE_PATHS = (
    "scripts/four_color_joint_propagation_experiment.py",
    "scripts/four_color_joint_patterns.py",
    "scripts/four_color_joint_constraint_audit.py",
    "scripts/four_color_constraints.py",
    "scripts/four_color_lab.py",
    "scripts/four_color_serialization.py",
    "scripts/four_color_joint_consistency.py",
    "scripts/four_color_triangle_equalities.py",
    "scripts/four_color_partition.py",
    "scripts/four_color_intersections.py",
    "scripts/four_color_conflict_priority.py",
    "scripts/four_color_intersection_experiment.py",
    "scripts/four_color_examples.py",
    "scripts/four_color_c5.py",
    "scripts/four_color_conflicts.py",
    "scripts/four_color_cycle_structure.py",
    "scripts/four_color_cycle_propagation.py",
    "scripts/four_color_cycle_contexts.py",
    "scripts/four_color_local_information.py",
    "tools/four_color_lab_viewer.html",
    "tools/tests/test_four_color_constraints.py",
    "tools/tests/test_four_color_joint_constraints.py",
    "tools/tests/test_four_color_joint_propagation.py",
)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)
            + "\n").encode()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def source_hashes():
    """Bind the executable helpers, manual premise checker and three tests."""
    return {name: sha256((ROOT / name).read_bytes())
            for name in sorted(SOURCE_PATHS)}


def build_cases():
    """Derive thirty named cases from unchanged frozen source bytes only."""
    raw = (ROOT / FROZEN_INPUT).read_bytes()
    if sha256(raw) != FROZEN_INPUT_SHA256:
        raise AssertionError("the original frozen gap input bytes changed")
    matches = [case for case in json.loads(raw)
               if case.get("role") == "secondary-gap"]
    if len(matches) != 1:
        raise AssertionError("expected one frozen secondary-gap original graph")
    fixed = normalize_graph(matches[0]["graph"])
    graph = normalize_graph(dict(fixed, fixed=[]))
    if (graph_fingerprint(fixed) != FIXED_GRAPH_SHA256
            or graph_fingerprint(graph) != UNFIXED_GRAPH_SHA256):
        raise AssertionError("frozen literal source graph identity changed")
    manual = instantiate_nine_point_constraint(graph, DEFAULT_ROLE_MAPPING)
    if manual is None or len(graph["edges"]) != 21:
        raise AssertionError("frozen source is not the registered 21-edge pattern")

    def case(name, original, *, group, count=None, **metadata):
        original = normalize_graph(dict(original, name=name))
        return dict(name=name, case_group=group, graph=original,
                    graph_sha256=graph_fingerprint(original),
                    source_graph_sha256=graph_fingerprint(dict(original, fixed=[])),
                    expected_solution_count=count, **metadata)

    cases = [
        case("nine-point-unfixed", graph, group="source", count=48),
        case("nine-point-incompatible-pins", fixed, group="incompatible", count=0),
    ]
    for colour in range(4):
        cases.append(case(
            f"nine-point-compatible-pin-{colour}", dict(graph, fixed=[[0, colour]]),
            group="compatible-pin", count=12, common_colour=colour))

    leaf = max(graph["vertices"]) + 1
    leaf_graph = {key: value for key, value in graph.items() if key != "positions"}
    leaf_graph.update(vertices=graph["vertices"] + [leaf],
                      edges=graph["edges"] + [[9, leaf]])
    cases.append(case("nine-point-exterior-leaf", leaf_graph,
                      group="extension", count=144, leaf_vertex=leaf))

    relabeling = {vertex: 103 - 17 * offset
                  for offset, vertex in enumerate(graph["vertices"])}
    relabeled = dict(
        vertices=[relabeling[vertex] for vertex in reversed(graph["vertices"])],
        edges=[[relabeling[a], relabeling[b]] for a, b in graph["edges"]], fixed=[])
    cases.append(case(
        "nine-point-relabel-reversed", relabeled, group="relabel", count=48,
        relabeling=[[vertex, relabeling[vertex]] for vertex in graph["vertices"]]))
    cases.append(case(
        "nine-point-extra-original-edge", dict(graph, edges=graph["edges"] + [[0, 6]]),
        group="extra-edge", count=0, added_original_edge=[0, 6]))

    for offset, edge in enumerate(graph["edges"]):
        cases.append(case(
            f"nine-point-remove-edge-{offset:02d}",
            dict(graph, edges=[other for other in graph["edges"] if other != edge]),
            group="missing-edge", removed_original_edge=edge))
    if len(cases) != 30 or len({case["name"] for case in cases}) != 30:
        raise AssertionError("expected exactly thirty distinct original contexts")
    return cases, raw


def independent_reference(case):
    """Exhaust literal 4^n assignments against original edges, then pins.

    The imported independent helper receives no pins so its free-variable
    enumeration is literally 4^n.  Filtering its complete original-edge
    solutions by the original pins does not consult any pattern or relation.
    """
    graph = case["graph"]
    positions = {vertex: index for index, vertex in enumerate(graph["vertices"])}
    solutions = [colours for colours in original_solutions(dict(graph, fixed=[]))
                 if all(colours[positions[vertex]] == colour
                        for vertex, colour in graph["fixed"])]
    if (case["expected_solution_count"] is not None
            and len(solutions) != case["expected_solution_count"]):
        raise AssertionError("independent original-edge solution count changed")
    if any(not verify_coloring(graph, colours) for colours in solutions):
        raise AssertionError("independent original-edge enumerator returned an invalid witness")
    reference = dict(
        name=case["name"], graph_sha256=case["graph_sha256"],
        source_graph_sha256=case["source_graph_sha256"],
        vertex_order=graph["vertices"],
        method="exhaust literal 4^n assignments using only original edges and pins",
        assignments_checked=4 ** len(graph["vertices"]),
        solution_count=len(solutions), original_solutions=solutions,
    )
    if case["case_group"] == "missing-edge":
        witness = next((colours for colours in solutions
                        if colours[positions[0]] != colours[positions[6]]), None)
        if witness is None:
            raise AssertionError("missing-edge control lacks an independently valid unequal witness")
        reference["unequal_uv_witness"] = witness
    return reference


def verify_learned_membership(graph, solutions, result):
    """Check raw learned factors/events against every complete source solution."""
    positions = {vertex: index for index, vertex in enumerate(graph["vertices"])}
    learned = [record for record in result["self_constraints"]
               if record["id"] == FACTOR_ID]
    events = [event for event in result["events"]
              if event["kind"] == "structural_constraint"
              and event.get("relation_kind") == "joint_constraint"]
    checks = 0
    for record in learned:
        manual = instantiate_nine_point_constraint(graph, record["role_mapping"])
        if (manual is None or manual["source_edges"] != record["source_edges"]
                or manual["source_vertices"] != record["source_vertices"]
                or len(record["source_edges"]) != 21
                or len(set(record["source_vertices"])) != 9):
            raise AssertionError("learned relation lacks its complete original-subgraph witness")
        rows = {tuple(row) for row in record["rows"]}
        for colours in solutions:
            if tuple(colours[positions[vertex]] for vertex in record["frontier"]) not in rows:
                raise AssertionError("learned relation removed an original complete solution")
            checks += 1
    for event in events:
        rows = {tuple(row["boundary"]) for row in event["relation_preview"]}
        for colours in solutions:
            if tuple(colours[positions[vertex]] for vertex in event["frontier"]) not in rows:
                raise AssertionError("recorded learned rows removed an original complete solution")
            checks += 1
    return dict(learned_factors=len(learned), recorded_joint_events=len(events),
                complete_solution_memberships=checks,
                all_learned_rows_preserve_all_solutions=True), events


def verify_case_obligations(case, result, metrics, events):
    """Check the requested before-elimination conclusions in their literal frame."""
    if not result["use_joint_constraints"]:
        if events or result["stats"]["joint_factors"]:
            raise AssertionError("historical mode unexpectedly installed a joint factor")
        return {}
    if not result["joint_scan"]["complete"]:
        raise AssertionError("finite named-pattern scan unexpectedly incomplete")
    if case["case_group"] == "missing-edge":
        if result["stats"]["joint_matches"] != 0 or events:
            raise AssertionError("missing required edge was accepted by automatic matching")
        return dict(missing_edge_guard_verified=True)
    if not events:
        raise AssertionError("a complete original pattern was not automatically found")
    if case["name"] == "nine-point-unfixed":
        first_elimination = next(index for index, event in enumerate(result["events"])
                                 if event["kind"] == "eliminate")
        matches = [(index, event) for index, event in enumerate(result["events"])
                   if event in events and event["frontier"] == [0, 6, 9]]
        if len(matches) != 1:
            raise AssertionError("unfixed source did not learn its canonical common triple")
        index, event = matches[0]
        expected = [[colour, colour, colour] for colour in range(4)]
        if (index >= first_elimination or event["depth"] != 0
                or event["stats"]["eliminations"] != 0
                or event["relation_rows"] != 4 or event["rows"] != expected
                or [row["boundary"] for row in event["relation_preview"]] != expected):
            raise AssertionError("the full unfixed equality relation was not learned before elimination")
        return dict(common_triple=[0, 6, 9], full_literal_equality_rows=expected,
                    structural_event_index=index, first_elimination_index=first_elimination,
                    learned_at_depth_zero=True, learned_before_first_elimination=True)
    if case["case_group"] == "incompatible":
        if (result["status"] != "unsatisfiable" or result["stats"]["eliminations"] != 0
                or result["stats"]["writebacks"] != 0 or result["elimination_records"]):
            raise AssertionError("incompatible pins were not rejected before elimination")
        return dict(incompatible_pins_rejected_before_elimination=True)
    if case["case_group"] == "compatible-pin":
        domains = {row["vertex"]: row["colors"]
                   for row in metrics["domain_candidates_before_first_elimination"]}
        colour = case["common_colour"]
        if any(domains[vertex] != [colour] for vertex in (0, 6, 9)):
            raise AssertionError("the compatible pin did not propagate to both other common vertices")
        return dict(common_colour=colour,
                    common_vertex_domains_before_first_elimination={
                        str(vertex): domains[vertex] for vertex in (0, 6, 9)},
                    no_early_writeback_verified=True)
    return dict(automatic_pattern_found=True)


def _write_frozen(path, data):
    if path.exists() and path.read_bytes() != data:
        raise AssertionError(f"refusing to replace different frozen bytes: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def experiment(out_dir=DEFAULT_OUT, *, max_checks=MAX_CHECKS):
    """Produce deterministic, complete-run finite evidence in a new directory."""
    if type(max_checks) is not int or max_checks < 0:
        raise ValueError("max_checks must be a nonnegative integer")
    out_dir = Path(out_dir)
    cases, frozen_raw = build_cases()
    source_bytes = {name: (ROOT / name).read_bytes() for name in sorted(SOURCE_PATHS)}
    sources = {name: sha256(data) for name, data in source_bytes.items()}
    options = dict(
        max_checks=max_checks, trace_limit=10000, record_relations=True,
        use_substructures=True, use_intersections=True, use_cycles=True,
        use_cycle_contexts=True, use_conflicts=False, use_c5=False,
        cycle_context_search="neighbours", cycle_max_cycles=128,
        cycle_max_scan_steps=200_000, cycle_context_max_contexts=128,
        cycle_context_max_scan_steps=200_000,
        joint_max_matches=128, joint_max_scan_steps=200_000,
    )
    references = [independent_reference(case) for case in cases]
    input_bytes, reference_bytes = encoded(cases), encoded(references)
    out_dir.mkdir(parents=True, exist_ok=True)
    _write_frozen(out_dir / "inputs.json", input_bytes)
    _write_frozen(out_dir / "references.json", reference_bytes)
    _write_frozen(out_dir / "frozen-gap-inputs.json", frozen_raw)
    for name, data in source_bytes.items():
        _write_frozen(out_dir / "baseline-source" / name, data)
    (out_dir / "runs").mkdir(exist_ok=True)

    records = []
    for offset, (case, reference) in enumerate(zip(cases, references)):
        graph, solutions = case["graph"], reference["original_solutions"]
        expected = "colored" if solutions else "unsatisfiable"
        results = {}
        for mode, mode_options in MODES.items():
            before = encoded(graph)
            result = solve_constraints(graph, **options, **mode_options)
            if before != encoded(graph) or result["graph_sha256"] != case["graph_sha256"]:
                raise AssertionError("main propagation changed the original input graph")
            if result["status"] != expected:
                raise AssertionError("finite solver run is incomplete or disagrees with the exhaustive reference")
            preservation = verify_preservation(graph, solutions, result)
            preservation.update(
                coverage="all_original_solutions_in_every_saved_domain_relation_and_fibre",
                exact_global_solution_count=len(solutions),
                unsat_preservation_vacuous=not solutions, complete_solver_run=True,
                trace_complete=True)
            learned, events = verify_learned_membership(graph, solutions, result)
            preservation["learned_relations"] = learned
            metrics = pre_elimination_metrics(result)
            obligations = verify_case_obligations(case, result, metrics, events)
            relative = f"runs/{case['name']}-{mode}.json.gz"
            full_bytes = encoded(result)
            compressed = gzip.compress(full_bytes, mtime=0)
            (out_dir / relative).write_bytes(compressed)
            results[mode] = dict(
                status=result["status"], colors=result["colors"], stats=result["stats"],
                metrics=metrics, preservation=preservation, obligations=obligations,
                joint_scan=result["joint_scan"],
                structural_joint_events=events,
                trace_truncated=result["trace_truncated"], event_count=result["event_count"],
                full_record=relative, full_record_sha256=sha256(full_bytes),
                compressed_record_sha256=sha256(compressed),
            )
        records.append(dict(
            name=case["name"], case_group=case["case_group"],
            graph_sha256=case["graph_sha256"],
            source_graph_sha256=case["source_graph_sha256"],
            vertices=len(graph["vertices"]), edges=len(graph["edges"]),
            reference_status=expected, exact_solution_count=len(solutions),
            independent_reference=dict(file="references.json", index=offset,
                                       assignments_checked=reference["assignments_checked"]),
            results=results,
            comparison=dict(
                statuses_agree=results["historical"]["status"] == results["joint"]["status"],
                eliminations_before_conflict_historical=results["historical"]["metrics"][
                    "eliminations_before_first_conflict"],
                eliminations_before_conflict_joint=results["joint"]["metrics"][
                    "eliminations_before_first_conflict"],
            ),
        ))
        print(f"{offset + 1}/30 {case['name']}: " + ", ".join(
            f"{mode}={row['status']},eliminations={row['stats']['eliminations']}"
            for mode, row in results.items()), flush=True)

    if source_hashes() != sources:
        raise AssertionError("experiment sources changed during the run; replay after edits finish")
    totals = {}
    for mode in MODES:
        rows = [record["results"][mode] for record in records]
        totals[mode] = dict(
            cases=len(rows), status_counts=dict(Counter(row["status"] for row in rows)),
            early_conflicts=sum(row["metrics"]["early_conflict"] for row in rows),
            all_solutions_preserved=all(row["preservation"]["all_solutions_preserved"]
                                        for row in rows),
            no_early_writeback_verified=all(
                row["preservation"]["no_early_writeback_verified"] for row in rows),
            complete_runs=sum(row["preservation"]["complete_solver_run"] for row in rows),
            joint_factors=sum(row["stats"]["joint_factors"] for row in rows),
            joint_scan_steps=sum(row["stats"]["joint_scan_steps"] for row in rows),
            source_solution_occurrences=sum(record["exact_solution_count"] for record in records),
            recorded_memberships={key: sum(row["preservation"]["checks"][key] for row in rows)
                                  for key in rows[0]["preservation"]["checks"]},
            learned_relation_memberships=sum(
                row["preservation"]["learned_relations"]["complete_solution_memberships"]
                for row in rows),
        )
    report = dict(
        schema="four-color-joint-propagation-v1", cases=records, case_count=len(records),
        options=options, modes=MODES, totals=totals,
        input_file="inputs.json", inputs_sha256=sha256(input_bytes),
        references_file="references.json", references_sha256=sha256(reference_bytes),
        frozen_source_input=dict(source=FROZEN_INPUT, copy="frozen-gap-inputs.json",
                                 sha256=FROZEN_INPUT_SHA256,
                                 fixed_graph_sha256=FIXED_GRAPH_SHA256,
                                 unfixed_graph_sha256=UNFIXED_GRAPH_SHA256),
        sources=sources, source_snapshots="baseline-source", python=sys.version.split()[0],
        interpretation=(
            "Thirty finite original-edge contexts, with all literal original solutions "
            "retained in references.json. Both modes use historical neighbour-only "
            "cycle contexts, complete shared-interface intersections and original-cycle "
            "closure. Only automatic named nine-point factors differ. Complete "
            "original-edge/pin solutions are checked against every recorded reduction "
            "domain, elimination source domain, full input relation, saved reconstruction "
            "fibre and learned factor/event row. Unsatisfiable preservation is vacuous; "
            "their complete independent enumeration and decision agree. The initial "
            "structural equality rows retain all four literal colours; no case colour "
            "is written before full elimination. Matching covers this named 21-edge "
            "non-induced pattern only, never arbitrary joint restrictions or all graphs."
        ),
    )
    (out_dir / "report.json").write_bytes(encoded(report))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--max-checks", type=int, default=MAX_CHECKS)
    args = parser.parse_args(argv)
    report = experiment(args.out_dir, max_checks=args.max_checks)
    print(json.dumps(report["totals"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
