"""Matched-input comparison of exact relations with/without small substructures."""
from __future__ import annotations

import sys
import hashlib
from pathlib import Path
from time import perf_counter

from four_color_lab import graph_fingerprint, solve, verify_coloring
from four_color_examples import random_triangulation


def experiment(count=100, size=30, seed=0, max_checks=1000000):
    import networkx as nx
    from four_color_constraints import solve_constraints

    records = []
    for offset in range(count):
        g = random_triangulation(size, seed + offset)
        nx_graph = nx.Graph()
        nx_graph.add_nodes_from(g["vertices"])
        nx_graph.add_edges_from(g["edges"])
        if not nx.check_planarity(nx_graph)[0]:
            raise AssertionError("nonplanar sample")
        results = {}
        # Alternate order to avoid always giving one mode the warmed runtime.
        for motifs in ((False, True) if offset % 2 == 0 else (True, False)):
            start = perf_counter()
            r = solve_constraints(g, use_substructures=motifs, max_checks=max_checks,
                                  trace_limit=0, record_relations=False, use_conflicts=False)
            elapsed = perf_counter() - start
            if r["status"] == "colored":
                assert verify_coloring(g, r["colors"])
            elif r["status"] != "limit":
                raise AssertionError("unexpected unsat on a verified planar sample")
            results["substructures" if motifs else "edges"] = dict(
                status=r["status"], seconds=elapsed, stats=r["stats"],
                substructures={k: v for k, v in r["substructures"].items()
                               if isinstance(v, (str, int, float, bool))})
        start = perf_counter()
        r = solve(g, strategy="dsatur", propagation=True, max_steps=10000, trace_limit=0)
        elapsed = perf_counter() - start
        results["dsatur"] = dict(status=r["status"], seconds=elapsed, stats=r["stats"])
        records.append(dict(seed=seed + offset, graph_sha256=graph_fingerprint(g), results=results))
    totals = {}
    for mode in ("edges", "substructures", "dsatur"):
        rows = [r["results"][mode] for r in records]
        totals[mode] = dict(graphs=count,
                            colored=sum(r["status"] == "colored" for r in rows),
                            limit=sum(r["status"] == "limit" for r in rows),
                            seconds=sum(r["seconds"] for r in rows),
                            stats={key: (max if key.startswith(("peak_", "max_")) else sum)(
                                            r["stats"].get(key, 0) for r in rows)
                                   for key in sorted(rows[0]["stats"])})
        totals[mode]["max_peak_scope"] = max(r["stats"].get("peak_scope", 0) for r in rows)
        totals[mode]["max_peak_rows"] = max(r["stats"].get("peak_rows", 0) for r in rows)
    paired = [r for r in records if all(r["results"][mode]["status"] == "colored"
                                      for mode in ("edges", "substructures"))]
    paired_totals = {mode: dict(checks=sum(r["results"][mode]["stats"]["checks"] for r in paired),
                               seconds=sum(r["results"][mode]["seconds"] for r in paired))
                     for mode in ("edges", "substructures")}
    return dict(count=count, vertices=size, seed=seed, max_checks=max_checks,
                dsatur_max_assignments=10000, sampling="face insertion and convex flips; nonuniform",
                timing="one in-process run per mode per graph, alternating constraint mode order; not a universal speed guarantee",
                stats_aggregation="sum of work counters; maximum for peak_* and max_* fields",
                both_constraint_modes_completed=len(paired), paired_totals=paired_totals,
                sources={name: hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest()
                         for name in ("four_color_constraints.py", "four_color_examples.py",
                                      "four_color_lab.py", "four_color_constraint_experiment.py")},
                python=sys.version.split()[0], networkx=nx.__version__, totals=totals, records=records)
