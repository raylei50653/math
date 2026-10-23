#!/usr/bin/env python3
"""Independently recompute graph metadata and reconcile summary histograms."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


PROFILES = ("free", "chordless", "degree-biased")


def recompute(sample):
    n = sample["n"]
    boundary = sample["boundary"]
    assert boundary == list(range(5))
    rim = {frozenset((boundary[i], boundary[(i + 1) % 5])) for i in range(5)}
    edges = {frozenset(pair) for pair in sample["edges"]}
    adj = [{w for w in range(n) if w != v and frozenset((v, w)) in edges}
           for v in range(n)]
    degree = list(map(len, adj))
    remaining = set(range(n))
    while True:
        removable = {v for v in remaining - set(boundary)
                     if len(adj[v] & remaining) <= 3}
        if not removable:
            break
        remaining -= removable
    faces = {frozenset(face) for face in sample["faces"]}
    nonfacial = sum(frozenset((u, v, w)) not in faces
                   for u, v, w in combinations(range(n), 3)
                   if v in adj[u] and w in adj[u] and w in adj[v])
    chord_count = sum(pair <= set(boundary) and pair not in rim for pair in edges)
    crosscuts = sum(v in adj[a] and v in adj[b]
                    for a, b in combinations(boundary, 2) if frozenset((a, b)) not in rim
                    for v in range(5, n))
    deficit = sum(max(0, (4 if v in boundary else 5) - degree[v]) for v in range(n))
    return dict(boundary_degrees=degree[:5], minimum_interior_degree=min(degree[5:]),
                interior_degree_histogram={str(d): c for d, c in sorted(Counter(degree[5:]).items())},
                n5=degree[5:].count(5),
                interior_degree5_centers_without_boundary_neighbors=sum(
                    degree[v] == 5 and adj[v].isdisjoint(boundary) for v in range(5, n)),
                r1_core_k=len(remaining) - 5, nonfacial_triangles=nonfacial,
                two_edge_crosscuts=crosscuts, boundary_chords=chord_count,
                degree_deficit=deficit,
                minimum_source_geometry=(chord_count == 0 and deficit == 0
                                         and nonfacial == 0 and crosscuts == 0))


def main():
    sample_path, summary_path, output_path = map(Path, sys.argv[1:])
    sample_bytes = sample_path.read_bytes()
    samples = [json.loads(line) for line in sample_bytes.splitlines() if line]
    summary = json.loads(summary_path.read_bytes())
    sigma_hist = Counter()
    graph_hashes = set()
    strata = defaultdict(list)
    seen_ids = set()
    for s in samples:
        assert s["profile"] in PROFILES
        assert s["id"] == f"{s['profile']}/k{s['k']}/{s['sample_index']}"
        assert s["id"] not in seen_ids
        seen_ids.add(s["id"])
        seed = int.from_bytes(sha256(f"{s['master_seed']}/{s['profile']}/{s['k']}/{s['sample_index']}".encode()).digest()[:8], "big")
        assert s["seed"] == seed
        assert s["attempted_flips"] == 40 * s["n"]
        assert type(s["accepted_flips"]) is int and 0 <= s["accepted_flips"] <= s["attempted_flips"]
        graph = {key: s[key] for key in ("n", "boundary", "edges")}
        digest = sha256(json.dumps(graph, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        assert s["graph_sha256"] == digest
        graph_hashes.add(digest)
        structure = recompute(s)
        assert structure == s["structure"], (s["id"], structure, s["structure"])
        if s["profile"] != "free":
            assert structure["boundary_chords"] == 0
        sigma_hist[str(s["sigma"])] += 1
        strata[f"{s['profile']}/k{s['k']}"].append(s)
    assert summary["sigma_histogram"] == dict(sigma_hist)
    assert summary["distinct_labelled_graphs"] == len(graph_hashes)
    assert summary["total"]["samples"] == len(samples)
    assert summary["total"]["minimum_source_geometry"] == sum(s["structure"]["minimum_source_geometry"] for s in samples)
    for stratum, group in strata.items():
        actual = summary["groups"][stratum]
        assert actual["samples"] == len(group)
        assert actual["sigma_histogram"] == dict(Counter(str(s["sigma"]) for s in group))
        for field in ("accepted_flips", "attempted_flips"):
            assert actual[field] == sum(s[field] for s in group)
        assert actual["minimum_source_geometry"] == sum(s["structure"]["minimum_source_geometry"] for s in group)
        for histogram, field in (("r1_core_histogram", "r1_core_k"),
                ("interior_min_degree_histogram", "minimum_interior_degree"),
                ("degree_deficit_histogram", "degree_deficit"),
                ("nonfacial_triangle_histogram", "nonfacial_triangles"),
                ("boundary_chord_histogram", "boundary_chords"),
                ("two_edge_crosscut_histogram", "two_edge_crosscuts"),
                ("n5_histogram", "n5")):
            assert actual[histogram] == dict(Counter(str(s["structure"][field]) for s in group))
    assert set(summary["groups"]) == set(strata)
    result = dict(schema="c5-independent-metadata-review-v1", sample_count=len(samples),
                  strata=len(strata), metadata_and_histograms_verified=True,
                  samples_sha256=sha256(sample_bytes).hexdigest(),
                  summary_sha256=sha256(summary_path.read_bytes()).hexdigest(),
                  checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    with output_path.open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
