#!/usr/bin/env python3
"""Bounded, independent original-edge differential audit; no 4CT oracle."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import networkx as nx
from four_color_constraints import solve_constraints


def witness(graph):
    """Exhaustive independent DFS: only input edges and literal fixed colors."""
    neighbors = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        neighbors[u].add(v)
        neighbors[v].add(u)
    assigned = dict(graph["fixed"])
    if any(u in assigned and v in assigned and assigned[u] == assigned[v]
           for u, v in graph["edges"]):
        return None

    def visit():
        if len(assigned) == len(neighbors):
            return [assigned[v] for v in graph["vertices"]]
        choices = {v: set(range(4)) - {assigned[w] for w in neighbors[v]
                                     if w in assigned}
                   for v in neighbors if v not in assigned}
        v = min(choices, key=lambda v: (len(choices[v]), -len(neighbors[v]), v))
        for color in sorted(choices[v]):
            assigned[v] = color
            answer = visit()
            if answer is not None:
                return answer
        assigned.pop(v, None)
        return None

    return visit()


def valid(graph, colors):
    if len(colors) != len(graph["vertices"]) or any(type(c) is not int or c not in range(4) for c in colors):
        return False
    assignment = dict(zip(graph["vertices"], colors))
    return (all(assignment[u] != assignment[v] for u, v in graph["edges"])
            and all(assignment[v] == c for v, c in graph["fixed"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    totals, statuses, modes = Counter(), Counter(), Counter()
    transcript = hashlib.sha256()
    failures = []
    configurations = {
        "default_anchor": {},
        "prefix_intersections_cache": dict(bucket_method="prefix", use_intersections=True,
                                           use_interface_cache=True, interface_cache_max_rows=37),
    }
    for atlas_id, original in enumerate(nx.graph_atlas_g()):
        planar = nx.check_planarity(original)[0]
        totals["graphs"] += 1
        totals["planar_graphs"] += planar
        # Deliberately nonconsecutive labels and reversed input order.
        labels = {v: 101 - 13 * v for v in original}
        vertices = [labels[v] for v in reversed(list(original))]
        edges = [[labels[u], labels[v]] for u, v in original.edges()]
        cases = [("free", [])]
        if len(vertices) >= 2:
            cases += [("same_fixed", [[vertices[0], 2], [vertices[-1], 2]]),
                      ("different_fixed", [[vertices[0], 3], [vertices[-1], 1]])]
        for case_name, fixed in cases:
            graph = dict(vertices=vertices, edges=edges, fixed=fixed)
            expected_witness = witness(graph)
            expected = "colored" if expected_witness is not None else "unsatisfiable"
            totals["conditions"] += 1
            totals["planar_conditions"] += planar
            totals["oracle_" + expected] += 1
            if expected_witness is not None:
                assert valid(graph, expected_witness)
            for mode, options in configurations.items():
                result = solve_constraints(graph, trace_limit=0, **options)
                totals["solver_calls"] += 1
                statuses[result["status"]] += 1
                modes[mode] += 1
                discrepancy = (result["status"] not in (expected, "limit")
                               or (result["status"] == "colored" and not valid(graph, result["colors"])))
                row = [atlas_id, case_name, mode, expected, result["status"], result["colors"]]
                transcript.update((json.dumps(row, separators=(",", ":")) + "\n").encode())
                if discrepancy:
                    failures.append(dict(atlas_id=atlas_id, mode=mode, graph=graph,
                                         oracle_witness=expected_witness, result=result))
        if atlas_id % 250 == 0:
            print(f"atlas={atlas_id} calls={totals['solver_calls']} discrepancies={len(failures)}", flush=True)
    summary = dict(
        schema="four-color-atlas-counterexample-audit-v1",
        totals=dict(totals), statuses=dict(statuses), modes=dict(modes),
        options=configurations, common_options=dict(trace_limit=0),
        result_sha256=transcript.hexdigest(), failures=failures,
        networkx=nx.__version__, python=sys.version,
        elapsed_seconds=round(time.monotonic() - started, 3),
        sources={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in sorted((ROOT / "scripts").glob("four_color*.py"))},
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        coverage="All 1253 atlas representatives of simple graphs up to seven vertices, each without fixed colors and, when possible, two selected literal two-vertex assignments. Two solver modes, complete records. Not all partial fixed assignments, vertex orders, or option combinations. Limits are inconclusive, not errors. No universal proof.")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("totals", "statuses", "modes", "elapsed_seconds")}), flush=True)
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
