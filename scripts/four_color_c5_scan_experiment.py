#!/usr/bin/env python3
"""Compare frozen DFS, indexed discovery, and local C5 rings on identical graphs.

Graph generation is outside every timed interval.  Each scanner's validation,
normalization, and adjacency construction remain inside it.  Source bytes are
captured before loading either scanner and checked again after all work.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics
import time
import types

from four_color_examples import random_triangulation
from four_color_lab import graph_fingerprint


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE = ROOT / "artifacts/four_color_c5/baseline-source/four_color_c5.py"
DEFAULT_CORPORA = ((30, 100), (100, 10), (300, 5))
METHODS = ("frozen_dfs", "current_bitset", "local_rings")
SOURCE_NAMES = {"frozen_dfs": "frozen_dfs", "current_bitset": "current_bitset",
                "local_rings": "current_bitset"}
STEP_UNITS = {
    "frozen_dfs": "inspected neighbor during chordless path growth; setup uncharged",
    "current_bitset": "selected candidate extension; setup and bitset filtering uncharged",
    "local_rings": "one inspected center; graph preparation uncharged",
}
MODES = {
    "default": {"max_cycles": 128, "max_steps": 200000},
    "full": {"max_cycles": 1000000000, "max_steps": 1000000000},
}


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _cycles_sha256(cycles):
    return _sha256(json.dumps(cycles, separators=(",", ":")).encode())


def _load_scanner(name, path, source, function="find_induced_c5"):
    # Compile the captured bytes directly: no stale bytecode cache can disagree
    # with the SHA recorded in the measurement receipt.
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(source, str(path), "exec"), module.__dict__)
    return getattr(module, function)


def _verify_cycles(graph, cycles, *, ordered=True):
    """Check ordered literal identities and all five edges/five nonedges."""
    index = {vertex: position for position, vertex in enumerate(graph["vertices"])}
    edges = {tuple(sorted(edge)) for edge in graph["edges"]}
    if len(set(cycles)) != len(cycles):
        raise AssertionError("duplicate cycle in discovery result")
    canonical_indices = []
    for cycle in cycles:
        if len(cycle) != 5 or len(set(cycle)) != 5:
            raise AssertionError("cycle is not five distinct original vertices")
        positions = tuple(index[vertex] for vertex in cycle)
        if positions[0] != min(positions) or positions[1] >= positions[-1]:
            raise AssertionError("cycle does not use canonical input-order frame")
        for i in range(5):
            for j in range(i + 1, 5):
                present = tuple(sorted((cycle[i], cycle[j]))) in edges
                required = j == i + 1 or (i == 0 and j == 4)
                if present != required:
                    raise AssertionError("reported cycle is not induced")
        canonical_indices.append(positions)
    if ordered and canonical_indices != sorted(canonical_indices):
        raise AssertionError("cycle list order is not canonical DFS order")


def _receipt(result, full_cycle_count):
    receipt = dict(cycles=len(result["cycles"]), has_cycle=bool(result["cycles"]),
                ordered_cycles_sha256=_cycles_sha256(result["cycles"]),
                complete=result["complete"], truncated=result["truncated"],
                steps=result["steps"], elapsed_ns=[],
                full_global_cycles=full_cycle_count,
                fraction_of_full_induced_cycles=(len(result["cycles"]) / full_cycle_count
                                                if full_cycle_count else None))
    if "local_scan_complete" in result:
        receipt.update(local_scan_complete=result["local_scan_complete"],
                       eligible_centers=result["eligible_centers"],
                       centers_found=sum(len(centers) for centers in result["centers"]),
                       centers_by_cycle=result["centers"])
    return receipt


def experiment(*, corpora=DEFAULT_CORPORA, repeats=5, seed=0,
               baseline_path=DEFAULT_BASELINE):
    """Return replayable receipts; default corpus is 115 seeded plane graphs."""
    if type(repeats) is not int or repeats < 1 or type(seed) is not int:
        raise ValueError("repeats must be positive and seed must be an integer")
    if any(type(n) is not int or n < 3 or type(count) is not int or count < 1
           for n, count in corpora):
        raise ValueError("each corpus needs n >= 3 and a positive graph count")
    paths = {
        "frozen_dfs": Path(baseline_path).resolve(),
        "current_bitset": ROOT / "scripts/four_color_c5.py",
        "graph_generator": ROOT / "scripts/four_color_examples.py",
        "normalizer": ROOT / "scripts/four_color_lab.py",
        "serialization": ROOT / "scripts/four_color_serialization.py",
        "benchmark": Path(__file__).resolve(),
    }
    source_bytes = {name: path.read_bytes() for name, path in paths.items()}
    scanners = {name: _load_scanner(f"_c5_scan_benchmark_{name}", paths[SOURCE_NAMES[name]],
                                   source_bytes[SOURCE_NAMES[name]],
                                   "find_local_c5" if name == "local_rings" else "find_induced_c5")
                for name in METHODS}
    started = datetime.now(timezone.utc).isoformat()
    groups = []
    for n, count in corpora:
        # Generation and graph/cycle validation are deliberately untimed.
        graphs = [random_triangulation(n, seed + offset) for offset in range(count)]
        graph_records = [dict(seed=seed + offset, vertices=n, edges=len(graph["edges"]),
                              graph_sha256=graph_fingerprint(graph), modes={})
                         for offset, graph in enumerate(graphs)]
        reference = {}
        for mode, limits in MODES.items():
            reference[mode] = {
                name: [scanner(graph, **limits) for graph in graphs]
                for name, scanner in scanners.items()
            }
        for offset, graph in enumerate(graphs):
            old_full = reference["full"]["frozen_dfs"][offset]
            new_full = reference["full"]["current_bitset"][offset]
            if not old_full["complete"] or not new_full["complete"]:
                raise AssertionError("full-scan budget was insufficient; no complete comparison is claimed")
            if old_full["cycles"] != new_full["cycles"]:
                raise AssertionError("complete scanner results differ in cycles or canonical list order")
            _verify_cycles(graph, old_full["cycles"])
            local_full = reference["full"]["local_rings"][offset]
            if local_full["complete"] or not local_full["local_scan_complete"]:
                raise AssertionError("local scan must finish its centers without claiming global completeness")
            _verify_cycles(graph, local_full["cycles"], ordered=False)
            if not set(local_full["cycles"]) <= set(old_full["cycles"]):
                raise AssertionError("local scanner returned a cycle outside the complete reference")
            neighbors = {vertex: set() for vertex in graph["vertices"]}
            for a, b in graph["edges"]:
                neighbors[a].add(b)
                neighbors[b].add(a)
            if local_full["eligible_centers"] != sum(len(adjacent) == 5 for adjacent in neighbors.values()):
                raise AssertionError("local scanner miscounted eligible degree-five centers")
            if len(local_full["centers"]) != len(local_full["cycles"]):
                raise AssertionError("local center records are not aligned with discovered cycles")
            for cycle, centers in zip(local_full["cycles"], local_full["centers"]):
                if not centers or any(neighbors[center] != set(cycle) for center in centers):
                    raise AssertionError("reported local center does not have exactly that neighbor ring")
            for mode in MODES:
                rows = {name: reference[mode][name][offset] for name in METHODS}
                for name, result in rows.items():
                    cycles = result["cycles"]
                    reference_cycles = (local_full if name == "local_rings" else old_full)["cycles"]
                    if cycles != reference_cycles[:len(cycles)]:
                        raise AssertionError("bounded scanner did not preserve the complete ordered prefix")
                    if name == "local_rings":
                        if result["complete"]:
                            raise AssertionError("local scanner incorrectly claimed global cycle completeness")
                        if result["local_scan_complete"] and cycles != local_full["cycles"]:
                            raise AssertionError("local scanner called a partial center scan complete")
                        for i, centers in enumerate(result["centers"]):
                            if centers != local_full["centers"][i][:len(centers)]:
                                raise AssertionError("bounded local centers are not an input-order prefix")
                    if result["complete"] and cycles != old_full["cycles"]:
                        raise AssertionError("scanner called a partial prefix complete")
                    if result["steps"] > MODES[mode]["max_steps"]:
                        raise AssertionError("scanner exceeded its declared scan budget")
                graph_records[offset]["modes"][mode] = {
                    name: _receipt(result, len(old_full["cycles"])) for name, result in rows.items()
                }
                graph_records[offset]["modes"][mode]["ordered_cycles_equal"] = (
                    rows["frozen_dfs"]["cycles"] == rows["current_bitset"]["cycles"])
                graph_records[offset]["modes"][mode]["local_cycles_subset_of_full"] = True

        summaries = {}
        for mode, limits in MODES.items():
            batch_times = {name: [] for name in METHODS}
            orders = []
            for repeat in range(repeats):
                offset = repeat % len(METHODS)
                order = list(METHODS[offset:] + METHODS[:offset])
                if repeat // len(METHODS) % 2:
                    order.reverse()
                orders.append(order)
                for name in order:
                    scanner = scanners[name]
                    measured_results = []
                    graph_times = []
                    begin_batch = time.perf_counter_ns()
                    for graph in graphs:
                        begin = time.perf_counter_ns()
                        result = scanner(graph, **limits)
                        graph_times.append(time.perf_counter_ns() - begin)
                        measured_results.append(result)
                    batch_times[name].append(time.perf_counter_ns() - begin_batch)
                    # Verify after timing so evidence checking cannot inflate
                    # one implementation's measured discovery work.
                    for offset, result in enumerate(measured_results):
                        expected = reference[mode][name][offset]
                        keys = ("cycles", "complete", "truncated", "steps")
                        if name == "local_rings":
                            keys += ("centers", "eligible_centers", "local_scan_complete")
                        if any(result[key] != expected[key] for key in keys):
                            raise AssertionError("scanner changed output across timing repetitions")
                        graph_records[offset]["modes"][mode][name]["elapsed_ns"].append(graph_times[offset])
            all_cycles = sum(len(result["cycles"]) for result in reference["full"]["frozen_dfs"])
            summary = dict(limits=limits, alternating_orders=orders,
                           full_global_cycles=all_cycles, methods={})
            for name in METHODS:
                rows = reference[mode][name]
                summary["methods"][name] = dict(
                    elapsed_ns=batch_times[name],
                    median_seconds=statistics.median(batch_times[name]) / 1e9,
                    complete=sum(result["complete"] for result in rows),
                    truncated=sum(result["truncated"] for result in rows),
                    cycles=sum(len(result["cycles"]) for result in rows),
                    graphs_with_cycles=sum(bool(result["cycles"]) for result in rows),
                    fraction_of_full_induced_cycles=(sum(len(result["cycles"]) for result in rows) / all_cycles
                                                    if all_cycles else None),
                    steps=sum(result["steps"] for result in rows),
                    step_unit=STEP_UNITS[name],
                )
                if name == "local_rings":
                    summary["methods"][name].update(
                        local_scan_complete=sum(result["local_scan_complete"] for result in rows),
                        eligible_centers=sum(result["eligible_centers"] for result in rows),
                        centers_found=sum(len(centers) for result in rows for centers in result["centers"]),
                    )
            summary["speedup_frozen_over_current"] = (
                summary["methods"]["frozen_dfs"]["median_seconds"] /
                summary["methods"]["current_bitset"]["median_seconds"])
            summary["speedup_current_over_local"] = (
                summary["methods"]["current_bitset"]["median_seconds"] /
                summary["methods"]["local_rings"]["median_seconds"])
            summary["speedup_frozen_over_local"] = (
                summary["methods"]["frozen_dfs"]["median_seconds"] /
                summary["methods"]["local_rings"]["median_seconds"])
            summary["local_time_over_current_time"] = (
                summary["methods"]["local_rings"]["median_seconds"] /
                summary["methods"]["current_bitset"]["median_seconds"])
            summaries[mode] = summary
        for graph_record in graph_records:
            for mode in MODES:
                for name in METHODS:
                    method_record = graph_record["modes"][mode][name]
                    method_record["median_seconds"] = statistics.median(method_record["elapsed_ns"]) / 1e9
        if any(graph_fingerprint(graph) != receipt["graph_sha256"]
               for graph, receipt in zip(graphs, graph_records)):
            raise AssertionError("a scanner mutated its shared graph input")
        groups.append(dict(vertices=n, count=count, seed=seed, summaries=summaries, records=graph_records))

    source_receipts = {}
    for name, path in paths.items():
        ending_bytes = path.read_bytes()
        if ending_bytes != source_bytes[name]:
            raise RuntimeError(f"source changed during benchmark: {path}")
        try:
            label = str(path.relative_to(ROOT))
        except ValueError:
            label = str(path)
        source_receipts[name] = dict(path=label, sha256_start=_sha256(source_bytes[name]),
                                     sha256_end=_sha256(ending_bytes), unchanged=True)
    return dict(
        schema="c5-discovery-comparison-v2", generated_at_utc=started,
        python=platform.python_version(), platform=platform.platform(),
        repeats=repeats, sources=source_receipts, method_source_names=SOURCE_NAMES,
        source_guard_passed=True,
        timing_contract="Generation and result validation excluded; per-call graph normalization and adjacency preparation included. Method order rotates and reverses across repetitions. Batch timings include shared timer/loop bookkeeping. Local selection does less work and does not promise global coverage.",
        cycle_contract="Full DFS/bitset results agree exactly in canonical cycle-list order. Local cycles are verified induced cycles and a subset of that full result; their list follows center-discovery order. Each bounded result is a prefix of its own method's full-budget list. local_scan_complete only covers center inspection; local complete is always false.",
        step_warning="DFS counts inspected neighbors; bitset counts selected extensions; local scan counts inspected centers. These counters are not comparable units; speedups use wall time only.",
        sampling_note="Seeded face insertion and legal flips are reproducible, not uniform sampling of planar graphs.",
        corpora=groups,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "artifacts/four_color_c5/scan-experiment.json")
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    result = experiment(repeats=args.repeats, seed=args.seed, baseline_path=args.baseline)
    encoded = json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n"
    if len(encoded.encode()) >= 1000000:
        raise RuntimeError("benchmark receipt unexpectedly exceeds 1 MB")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(encoded)
    for group in result["corpora"]:
        for mode, summary in group["summaries"].items():
            old = summary["methods"]["frozen_dfs"]
            new = summary["methods"]["current_bitset"]
            local = summary["methods"]["local_rings"]
            print(f"n={group['vertices']} count={group['count']} {mode}: "
                  f"{old['median_seconds']:.6f}s -> {new['median_seconds']:.6f}s "
                  f"({summary['speedup_frozen_over_current']:.2f}x), "
                  f"complete {old['complete']}/{new['complete']}; "
                  f"local {local['median_seconds']:.6f}s "
                  f"({summary['speedup_current_over_local']:.2f}x versus bitset), "
                  f"cycles {local['cycles']}/{summary['full_global_cycles']}, "
                  f"local scans complete {local['local_scan_complete']}")
    print(args.out)


if __name__ == "__main__":
    main()
