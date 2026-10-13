#!/usr/bin/env python3
"""Replay a frozen, bounded K4 experiment; NetworkX is only the reference oracle."""
from __future__ import annotations

import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import platform
import statistics
import sys
import time

import networkx as nx

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import k4_nonplanarity as detector


def read(name):
    return json.loads((HERE / "frozen" / name).read_text())


def graph(vertices, edges, boundary=None):
    result = detector.normalize({"vertices": list(vertices), "edges": list(edges)})
    if boundary is not None:
        result["boundary"] = list(boundary)
    return result


def fixtures():
    cycle = [(i, (i + 1) % 5) for i in range(5)]
    cells = read("artifacts/c5_cells/cells.json")["cells"]
    for mask, cell in sorted(cells.items(), key=lambda item: int(item[0])):
        yield "c5_cells", f"cell-{mask}", graph(range(5 + cell["k_eff"]),
                                                cell["edges"] + cycle, range(5))
    saved = read("artifacts/c5_k4_blocks/observations.json")
    for family in ("normalized", "named"):
        for row in saved[family]:
            yield f"k4_{family}", row["name"], graph(row["vertices"], row["edges"], range(5))
    sector = read("artifacts/c5_sector_positive_control/observations.json")
    for row in sector["proper_hits"]:
        edges = row["sector_edges"]
        vertices = {v for e in edges for v in e}
        yield "sector_3903", f"source-{row['source_index']}", graph(vertices, edges, range(5))
    flip = read("artifacts/c5_cell_flip/891_to_987.json")
    for stage in ("source", "deleted", "both_edges", "result"):
        row = flip[stage]
        yield "cell_flip", f"{stage}-{row['sigma']}", row["graph"]
    for i, g in enumerate(nx.graph_atlas_g()):
        yield "atlas_n_le_7", f"atlas-{i}", graph(g.nodes(), g.edges())
    k4 = list(combinations(range(4), 2))
    yield "named_controls", "K4", graph(range(4), k4)
    yield "named_controls", "K5", graph(range(5), combinations(range(5), 2))
    yield "named_controls", "K33", graph(range(6), [(u, v) for u in range(3) for v in range(3, 6)])
    yield "named_controls", "K4-four-independent-leaves", graph(range(8), k4 + [(i, i + 4) for i in range(4)])
    yield "named_controls", "K4-three-common-attachments", graph(range(5), k4 + [(i, 4) for i in range(3)])
    yield "named_controls", "K4-four-path-attachments", graph(range(8), k4 + [(4, 5), (5, 6), (6, 7)] + [(i, i + 4) for i in range(4)])
    yield "named_controls", "K3-join-independent-three", graph(range(6), list(combinations(range(3), 2)) + [(u, v) for u in range(3) for v in range(3, 6)])
    edges = list(combinations(range(5), 2))
    edges.remove((0, 1))
    edges.remove((2, 3))
    yield "named_controls", "K5-two-disjoint-edges-subdivided", graph(range(7), edges + [(0, 5), (5, 1), (2, 6), (6, 3)])
    edges = []
    for v, (a, b) in enumerate(combinations(range(5), 2), 5):
        edges.extend([(a, v), (v, b)])
    yield "named_controls", "K5-every-edge-subdivided", graph(range(15), edges)
    yield "named_controls", "C5-two-alternating-chords", graph(range(5), cycle + [(0, 2), (1, 3)], range(5))
    for length in (1, 2, 4, 8, 16):
        path = [(i, i + 1) for i in range(4, 3 + length)]
        for mask in range(16):
            links = [(v, 4 + v % length) for v in range(4) if mask >> v & 1]
            yield "attachment_sweep", f"path-{length}-mask-{mask:04b}", graph(range(4 + length), k4 + path + links)


def nx_graph(raw):
    g = nx.Graph()
    g.add_nodes_from(raw["vertices"])
    g.add_edges_from(raw["edges"])
    return g


def evaluate():
    base = json.loads((HERE / "BASE.json").read_text())
    for item in base["inputs"]:
        assert hashlib.sha256((HERE / "frozen" / item["path"]).read_bytes()).hexdigest() == item["sha256"]
    rows, groups = [], {}
    for dataset, name, raw in fixtures():
        variants = [("original", raw)]
        if "boundary" in raw:
            apex = max(raw["vertices"]) + 1
            variants.append(("boundary_apex", graph(raw["vertices"] + [apex],
                                                    raw["edges"] + [[apex, b] for b in raw["boundary"]])))
        for scope, tested in variants:
            result = detector.detect(tested)
            planar, _ = nx.check_planarity(nx_graph(tested))
            if result["detected"]:
                detector.verify_certificate(tested, result["certificate"])
                assert not planar, (dataset, name, scope)
            k4_count = sum(1 for _ in detector.four_cliques(detector.adjacency(tested)))
            row = {"dataset": dataset, "name": name, "scope": scope,
                   "graph": tested, "sha256": hashlib.sha256(json.dumps(tested, sort_keys=True).encode()).hexdigest(),
                   "reference_planar": planar, "literal_k4_count": k4_count, **result}
            rows.append(row)
            key = f"{dataset}:{scope}"
            stats = groups.setdefault(key, {"graphs": 0, "planar": 0, "nonplanar": 0,
                                           "detected": 0, "false_positives": 0,
                                           "missed_with_k4": 0, "missed_without_k4": 0,
                                           "planar_with_k4": 0})
            stats["graphs"] += 1
            stats["planar" if planar else "nonplanar"] += 1
            stats["detected"] += int(result["detected"])
            stats["false_positives"] += int(result["detected"] and planar)
            stats["planar_with_k4"] += int(planar and k4_count > 0)
            if not planar and not result["detected"]:
                stats["missed_with_k4" if k4_count else "missed_without_k4"] += 1
    for stats in groups.values():
        stats["recall_on_nonplanar"] = stats["detected"] / stats["nonplanar"] if stats["nonplanar"] else None
    return {"schema": 1, "networkx": nx.__version__, "base_head": base["head"],
            "groups": groups, "records": rows}


def benchmark(rows):
    selected = [r["graph"] for r in rows if r["dataset"] == "atlas_n_le_7"]
    detectors, references, pipelines = [], [], []
    # Both timings include building their data structures from the same JSON.
    # The detector constructs and verifies positive certificates; NetworkX only
    # computes a Boolean and embedding, with counterexample=False.
    for _ in range(7):
        start = time.perf_counter()
        for raw in selected:
            detector.detect(raw)
        detectors.append(time.perf_counter() - start)
        start = time.perf_counter()
        for raw in selected:
            nx.check_planarity(nx_graph(raw), counterexample=False)
        references.append(time.perf_counter() - start)
        start = time.perf_counter()
        for raw in selected:
            if not detector.detect(raw)["detected"]:
                nx.check_planarity(nx_graph(raw), counterexample=False)
        pipelines.append(time.perf_counter() - start)
    return {"python": platform.python_version(), "platform": platform.platform(),
            "networkx": nx.__version__, "graphs": len(selected), "repetitions": 7,
            "k4_seconds": detectors, "reference_seconds": references,
            "k4_then_reference_seconds": pipelines,
            "median_k4_seconds": statistics.median(detectors),
            "median_reference_seconds": statistics.median(references),
            "median_k4_then_reference_seconds": statistics.median(pipelines),
            "scope": "Same atlas JSON inputs, data-structure construction included; detector constructs/checks K5 certificate, reference does not extract Kuratowski counterexample. Small-graph batch measurements only."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--benchmark-output", type=Path, default=HERE / "benchmark.json")
    args = parser.parse_args()
    result = evaluate()
    target = HERE / "results.json"
    if args.check:
        assert result == json.loads(target.read_text()), "frozen replay differs"
        print(f"PASS: {len(result['records'])} original/apex records, certificates and reference comparisons")
    else:
        with target.open("x") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        print(json.dumps(result["groups"], indent=2))
    if args.benchmark:
        with args.benchmark_output.open("x") as stream:
            json.dump(benchmark(result["records"]), stream, indent=2)
            stream.write("\n")


if __name__ == "__main__":
    main()
