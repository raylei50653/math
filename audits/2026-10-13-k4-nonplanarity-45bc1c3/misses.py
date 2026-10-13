#!/usr/bin/env python3
"""Exactly classify K5 minors on the 76 missed Atlas graphs (at most 7 nodes).

This finite diagnostic recursively tries every edge contraction and vertex
deletion. It is not the production detector or an arbitrary-size performance
claim. Edge deletion is unnecessary: extra edges never invalidate a minor.
"""
import argparse
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent


@lru_cache(maxsize=None)
def model(n, edges):
    if n < 5 or len(edges) < 10:
        return None
    edge_set = set(edges)
    for clique in combinations(range(n), 5):
        if all(e in edge_set for e in combinations(clique, 2)):
            return tuple((v,) for v in clique)
    if n == 5:
        return None
    maps = []
    for removed in range(n):
        maps.append(tuple((v,) for v in range(n) if v != removed))
    for a, b in edges:
        maps.append(tuple((a, b) if v == a else (v,)
                          for v in range(n) if v != b))
    for groups in maps:
        owner = {v: i for i, group in enumerate(groups) for v in group}
        quotient = tuple(sorted({tuple(sorted((owner[a], owner[b])))
                                 for a, b in edges if a in owner and b in owner and owner[a] != owner[b]}))
        found = model(n - 1, quotient)
        if found is not None:
            return tuple(tuple(sorted(v for i in branch for v in groups[i])) for branch in found)
    return None


def validate(raw, branches):
    g = nx.Graph()
    g.add_nodes_from(raw["vertices"])
    g.add_edges_from(raw["edges"])
    assert len(branches) == 5
    used = set()
    for branch in branches:
        assert branch and not (set(branch) & used)
        assert nx.is_connected(g.subgraph(branch))
        used.update(branch)
    for left, right in combinations(branches, 2):
        assert any(g.has_edge(a, b) for a in left for b in right)


def evaluate():
    rows = json.loads((HERE / "results.json").read_text())["records"]
    missed = [row for row in rows if row["dataset"] == "atlas_n_le_7" and
              not row["reference_planar"] and not row["detected"]]
    records = []
    for row in missed:
        raw = row["graph"]
        vertices = raw["vertices"]
        assert len(vertices) <= 7
        order = {v: i for i, v in enumerate(vertices)}
        edges = tuple(sorted(tuple(sorted((order[a], order[b]))) for a, b in raw["edges"]))
        found = model(len(vertices), edges)
        lifted = [[vertices[v] for v in branch] for branch in found] if found is not None else None
        if lifted is not None:
            validate(raw, lifted)
        records.append({"name": row["name"], "graph_sha256": row["sha256"],
                        "literal_k4_count": row["literal_k4_count"],
                        "has_k5_minor": found is not None, "branch_sets": lifted})
    summary = {"misses": len(records),
               "with_k5_minor": sum(row["has_k5_minor"] for row in records),
               "without_k5_minor": sum(not row["has_k5_minor"] for row in records),
               "with_k4_without_k5_minor": sum(row["literal_k4_count"] > 0 and not row["has_k5_minor"] for row in records)}
    return {"schema": 1, "scope": "Exact contraction/deletion search on missed Atlas graphs only, n<=7", "summary": summary, "records": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = evaluate()
    target = HERE / "misses.json"
    if args.check:
        assert result == json.loads(target.read_text())
        print("PASS:", result["summary"])
    else:
        with target.open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
        print(result["summary"])


if __name__ == "__main__":
    main()
