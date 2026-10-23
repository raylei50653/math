#!/usr/bin/env python3
"""Independent strict-stratum metadata, seed-split, and summary checks."""
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys

from check_metadata import recompute
from independent_check import check_disk


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def face_key(face):
    pos = face.index(min(face))
    return tuple(face[pos:] + face[:pos])


def reconstruct_seed(s):
    layers = (s["k"] - 1) // 5
    faces = []
    for ring in range(layers):
        for j in range(5):
            v, w = 5 * ring + j, 5 * ring + (j + 1) % 5
            faces.extend([[v, w, v + 5], [w, w + 5, v + 5]])
    center = 5 * (layers + 1)
    faces.extend([[5 * layers + j, 5 * layers + (j + 1) % 5, center]
                  for j in range(5)])
    n = center + 1
    assert len(s["seed_vertex_splits"]) == s["k"] - (5 * layers + 1)
    for split in s["seed_vertex_splits"]:
        v, w, link, cut = (split[key] for key in ("vertex", "new_vertex", "link", "cut"))
        assert 5 <= v < n and w == n
        assert len(link) == len(set(link)) and len(link) >= 6
        assert 3 <= cut <= len(link) - 3
        previous = {face_key(f) for f in faces if v in f}
        assert previous == {face_key([v, link[i], link[(i + 1) % len(link)]])
                            for i in range(len(link))}
        faces = [f for f in faces if v not in f]
        faces.extend([[v if i < cut else w, link[i], link[(i + 1) % len(link)]]
                      for i in range(len(link))])
        faces.extend([[v, w, link[0]], [v, link[cut], w]])
        n += 1
    faces = [list(f) for f in sorted(face_key(f) for f in faces)]
    edges = sorted({tuple(sorted((f[i], f[(i + 1) % 3])))
                    for f in faces for i in range(3)})
    graph = dict(n=n, k=n - 5, boundary=list(range(5)),
                 faces=faces, edges=[list(e) for e in edges])
    assert n == s["n"]
    assert sha256(canonical(graph)).hexdigest() == s["seed_graph_sha256"]
    check_disk(graph)
    assert recompute(graph)["minimum_source_geometry"]


def main():
    samples_path, summary_path, output_path = map(Path, sys.argv[1:])
    data = samples_path.read_bytes()
    samples = [json.loads(line) for line in data.splitlines() if line]
    summary = json.loads(summary_path.read_bytes())
    strata = defaultdict(list)
    graph_hashes = set()
    for s in samples:
        assert s["profile"] == "minimum-geometry" and s["master_seed"] == 20261024
        assert s["id"] == f"minimum-geometry/k{s['k']}/{s['sample_index']}"
        expected_seed = int.from_bytes(sha256(f"20261024/minimum-geometry/{s['k']}/{s['sample_index']}".encode()).digest()[:8], "big")
        assert s["seed"] == expected_seed
        assert s["attempted_flips"] == 200 * s["n"]
        assert type(s["accepted_flips"]) is int and 0 <= s["accepted_flips"] <= s["attempted_flips"]
        digest = sha256(canonical({key: s[key] for key in ("n", "boundary", "edges")})).hexdigest()
        assert digest == s["graph_sha256"]
        graph_hashes.add(digest)
        recomputed = recompute(s)
        assert recomputed == s["structure"], s["id"]
        assert recomputed["minimum_source_geometry"], s["id"]
        reconstruct_seed(s)
        strata[f"minimum-geometry/k{s['k']}"].append(s)
    assert len({s["id"] for s in samples}) == len(samples)
    assert summary["total"]["samples"] == summary["total"]["minimum_source_geometry"] == len(samples)
    assert summary["distinct_labelled_graphs"] == len(graph_hashes)
    assert summary["sigma_histogram"] == dict(Counter(str(s["sigma"]) for s in samples))
    assert set(summary["groups"]) == set(strata)
    for key, group in strata.items():
        actual = summary["groups"][key]
        assert actual["samples"] == actual["minimum_source_geometry"] == len(group)
        assert actual["sigma_histogram"] == dict(Counter(str(s["sigma"]) for s in group))
        for field in ("accepted_flips", "attempted_flips"):
            assert actual[field] == sum(s[field] for s in group)
        for histogram, field in (("r1_core_histogram", "r1_core_k"),
                ("interior_min_degree_histogram", "minimum_interior_degree"),
                ("degree_deficit_histogram", "degree_deficit"),
                ("nonfacial_triangle_histogram", "nonfacial_triangles"),
                ("boundary_chord_histogram", "boundary_chords"),
                ("two_edge_crosscut_histogram", "two_edge_crosscuts"),
                ("n5_histogram", "n5")):
            assert actual[histogram] == dict(Counter(str(s["structure"][field]) for s in group))
    result = dict(schema="c5-independent-targeted-metadata-review-v1",
                  sample_count=len(samples), strata=len(strata),
                  metadata_and_histograms_verified=True,
                  strict_necessary_geometry_verified=len(samples),
                  ring_seeds_and_vertex_splits_independently_verified=len(samples),
                  samples_sha256=sha256(data).hexdigest(),
                  summary_sha256=sha256(summary_path.read_bytes()).hexdigest(),
                  checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  metadata_dependency_sha256=sha256(Path(__file__).with_name("check_metadata.py").read_bytes()).hexdigest(),
                  topology_dependency_sha256=sha256(Path(__file__).with_name("independent_check.py").read_bytes()).hexdigest())
    with output_path.open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
