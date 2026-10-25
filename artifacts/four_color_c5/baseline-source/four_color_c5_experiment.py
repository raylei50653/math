"""Matched C5 propagation experiment and independently checked lookup timing."""
from __future__ import annotations

import hashlib
from pathlib import Path
import random
import sys
from time import perf_counter


def lookup_benchmark(count=10000, seed=17):
    from four_color_c5 import C5_ROWS, query_c5
    rows = sorted(C5_ROWS)
    rng = random.Random(seed)
    keys = [tuple(rng.randrange(1, 16) for _ in range(5)) for _ in range(count)]
    start = perf_counter()
    indexed = [query_c5(key) for key in keys]
    indexed_seconds = perf_counter() - start
    start = perf_counter()
    scanned = []
    for key in keys:
        bits = 0
        supports = [0] * 5
        for i, row in enumerate(rows):
            if all(key[j] & (1 << row[j]) for j in range(5)):
                bits |= 1 << i
                for j, color in enumerate(row):
                    supports[j] |= 1 << color
        scanned.append((bits, supports))
    scan_seconds = perf_counter() - start
    assert all(result["allowed_bits"] == bits and list(result["supports"]) == supports
               and result["row_count"] == bits.bit_count()
               for result, (bits, supports) in zip(indexed, scanned))
    return dict(queries=count, seed=seed, distinct_keys=len(set(keys)),
                indexed_seconds=indexed_seconds, scan_seconds=scan_seconds,
                exact_results_equal=True, literal_rows=len(rows),
                domain_sampling="five independent uniformly sampled nonempty 4-bit masks; fixed seed")


def experiment(count=100, size=30, seed=0, max_checks=1000000):
    import networkx as nx
    from four_color_examples import random_triangulation
    from four_color_lab import graph_fingerprint, solve, verify_coloring
    from four_color_constraints import solve_constraints

    records = []
    for offset in range(count):
        g = random_triangulation(size, seed + offset)
        ng = nx.Graph()
        ng.add_nodes_from(g["vertices"])
        ng.add_edges_from(g["edges"])
        assert nx.check_planarity(ng)[0]
        witness = solve(g, max_steps=100000, trace_limit=0)
        assert witness["status"] == "colored" and verify_coloring(g, witness["colors"])
        pinned = sorted(random.Random(seed + offset + 9127).sample(g["vertices"], max(1, size // 5)))
        fixed = [[v, witness["colors"][g["vertices"].index(v)]] for v in pinned]
        record = dict(seed=seed + offset, fixed=fixed, cohorts={})
        for cohort, graph in (("free", g), ("fixed", dict(g, fixed=fixed))):
            results = {}
            for enabled in ((False, True) if offset % 2 == 0 else (True, False)):
                start = perf_counter()
                r = solve_constraints(graph, use_c5=enabled, max_checks=max_checks,
                                      trace_limit=0, record_relations=False)
                elapsed = perf_counter() - start
                assert r["status"] in ("colored", "limit")
                if r["status"] == "colored":
                    assert verify_coloring(graph, r["colors"])
                results["c5" if enabled else "base"] = dict(status=r["status"], seconds=elapsed,
                    stats=r["stats"], substructures={k: v for k, v in r["substructures"].items()
                                                    if isinstance(v, (int, float, str, bool))})
            record["cohorts"][cohort] = dict(graph_sha256=graph_fingerprint(graph), results=results)
        records.append(record)
    totals = {}
    for cohort in ("free", "fixed"):
        totals[cohort] = {}
        for mode in ("base", "c5"):
            rows = [r["cohorts"][cohort]["results"][mode] for r in records]
            totals[cohort][mode] = dict(
                colored=sum(r["status"] == "colored" for r in rows),
                limit=sum(r["status"] == "limit" for r in rows),
                seconds=sum(r["seconds"] for r in rows),
                stats={k: (max if k.startswith(("peak_", "max_")) else sum)(r["stats"].get(k, 0) for r in rows)
                       for k in sorted(rows[0]["stats"])},
                graphs_with_c5_prunes=sum(r["stats"].get("c5_prunes", 0) > 0 for r in rows))
    files = ("four_color_c5.py", "four_color_c5_experiment.py", "four_color_constraints.py",
             "four_color_examples.py", "four_color_lab.py")
    return dict(count=count, vertices=size, seed=seed, max_checks=max_checks, totals=totals, records=records,
                lookup=lookup_benchmark(), python=sys.version.split()[0], networkx=nx.__version__,
                sources={name: hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest() for name in files},
                sampling="same nonuniform triangulations as earlier experiment; fixed cohort pins one fifth of vertices to one verified witness",
                timing="one run per mode/cohort; alternate mode order; includes C5 detection and queries; not a universal performance claim",
                stats_aggregation="sum work counters; maximum peak_* and max_*; bit-index operations and row scans are distinct work units")
