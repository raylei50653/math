#!/usr/bin/env python3
"""Sample the necessary minimum-source geometric stratum, nonuniformly.

See TARGETED_PROPOSAL.md, recorded before this second-stage experiment.
Uses the frozen first-stage evaluator but a different initial source family.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import random
import sys
import time

import sampler as base

PROFILE = "minimum-geometry"


def from_faces(n, faces):
    disk = base.Disk.__new__(base.Disk)
    disk.n = n
    disk.faces = {}
    disk.incident = {}
    disk.edge_list = []
    disk.edge_index = {}
    disk.degree = [0] * n
    disk.next_face = 0
    for face in faces:
        disk.add_face(face)
    return disk


def ring_seed(k, rng):
    layers = (k - 1) // 5
    faces = []
    for layer in range(layers):
        a, b = 5 * layer, 5 * (layer + 1)
        for i in range(5):
            j = (i + 1) % 5
            faces.extend(((a + i, a + j, b + i), (a + j, b + j, b + i)))
    center = 5 * (layers + 1)
    for i in range(5):
        faces.append((5 * layers + i, 5 * layers + (i + 1) % 5, center))
    disk = from_faces(center + 1, faces)
    split_log = []
    while disk.n < k + 5:
        choices = [v for v in range(5, disk.n) if disk.degree[v] >= 6]
        v = rng.choice(choices)
        around = {}
        old_faces = []
        for fid, f in disk.faces.items():
            if v in f:
                j = f.index(v)
                around[f[(j + 1) % 3]] = f[(j + 2) % 3]
                old_faces.append(fid)
        start = rng.choice(sorted(around))
        cycle = [start]
        while around[cycle[-1]] != start:
            cycle.append(around[cycle[-1]])
        assert len(cycle) == disk.degree[v]
        cut = rng.randrange(3, len(cycle) - 2)
        w = disk.n
        disk.n += 1
        disk.degree.append(0)
        for fid in old_faces:
            disk.remove_face(fid)
        for i in range(len(cycle)):
            owner = v if i < cut else w
            disk.add_face((owner, cycle[i], cycle[(i + 1) % len(cycle)]))
        disk.add_face((v, w, cycle[0]))
        disk.add_face((v, cycle[cut], w))
        split_log.append(dict(vertex=v, new_vertex=w, link=cycle, cut=cut))
    return disk, split_log


def constrained_flip(disk, adj, rng):
    u, v = rng.choice(disk.edge_list)
    old = (u, v)
    if old in base.RIM:
        return False
    if any(disk.degree[w] <= (4 if w < 5 else 5) for w in (u, v)):
        return False
    f1, f2 = sorted(disk.incident[old])
    face = disk.faces[f1]
    if not any(face[i] == u and face[(i + 1) % 3] == v for i in range(3)):
        u, v = v, u
    a = next(w for w in face if w not in old)
    b = next(w for w in disk.faces[f2] if w not in old)
    if a == b or b in adj[a] or (a < 5 and b < 5):
        return False
    # The only triangles created by adding ab must be its two incident faces.
    if adj[a] & adj[b] != {u, v}:
        return False
    for inside, outside in ((a, b), (b, a)):
        if inside >= 5 and outside < 5:
            if any(tuple(sorted((outside, c))) not in base.RIM
                   for c in adj[inside] if c < 5):
                return False
    disk.remove_face(f1)
    disk.remove_face(f2)
    disk.add_face((a, u, b))
    disk.add_face((a, b, v))
    adj[u].remove(v)
    adj[v].remove(u)
    adj[a].add(b)
    adj[b].add(a)
    return True


def make_sample(k, index, master_seed=20261024, steps=200):
    seed = base.derive_seed(master_seed, PROFILE, k, index)
    rng = random.Random(seed)
    disk, splits = ring_seed(k, rng)
    seed_graph = disk.graph()
    seed_structure = base.structure(seed_graph)
    assert seed_structure["minimum_source_geometry"]
    adj = [set() for _ in range(disk.n)]
    for u, v in disk.edge_list:
        adj[u].add(v)
        adj[v].add(u)
    accepted = sum(constrained_flip(disk, adj, rng) for _ in range(steps * disk.n))
    graph = disk.graph()
    structure = base.structure(graph)
    assert structure["minimum_source_geometry"]
    sigma, witnesses = base.exact_sigma(graph["n"], graph["edges"])
    graph_hash = sha256(base.canonical_bytes({s: graph[s] for s in ("n", "boundary", "edges")})).hexdigest()
    return dict(id=f"{PROFILE}/k{k}/{index}", profile=PROFILE, seed=seed,
                sample_index=index, master_seed=master_seed, attempted_flips=steps * disk.n,
                accepted_flips=accepted, graph_sha256=graph_hash, **graph,
                rows=list(base.PATTERNS), sigma=sigma, witnesses=witnesses,
                structure=structure, seed_vertex_splits=splits,
                seed_graph_sha256=sha256(base.canonical_bytes(seed_graph)).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sat-path", type=Path, default=Path("/tmp/c5-large-k-sat-78375cc"))
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("sample")
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--summary", type=Path, required=True)
    run.add_argument("--per-k", type=int, default=100)
    run.add_argument("--k-min", type=int, default=25)
    run.add_argument("--k-max", type=int, default=60)
    replay = sub.add_parser("replay")
    replay.add_argument("samples", type=Path)
    replay.add_argument("--output", type=Path, required=True)
    replay.add_argument("--stride", type=int, default=1)
    replay.add_argument("--limit", type=int)
    args = parser.parse_args()
    sys.path.insert(0, str(args.sat_path))
    start = time.monotonic()
    if args.command == "replay":
        count = 0
        for i, line in enumerate(args.samples.open()):
            if i % args.stride:
                continue
            row = json.loads(line)
            regenerated = make_sample(row["k"], row["sample_index"], row["master_seed"],
                                      row["attempted_flips"] // row["n"])
            if json.loads(json.dumps(regenerated)) != row:
                raise ValueError(f"targeted replay differs {row['id']}")
            count += 1
            if args.limit and count >= args.limit:
                break
        result = dict(replayed=count, deterministic_bytes_match=True,
                      elapsed_seconds=time.monotonic() - start)
        base.write_json(args.output, result)
        print(json.dumps(result), flush=True)
        return
    samples = []
    known = {int(key) for key in base.load_catalogue()["cells"]}
    with args.output.open("x") as out:
        for k in range(args.k_min, args.k_max + 1):
            for index in range(args.per_k):
                row = make_sample(k, index)
                samples.append(row)
                out.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
                if row["sigma"] not in known:
                    out.flush()
                    result = base.summarize(samples)
                    result["new_key_candidate"] = row["id"]
                    result["elapsed_seconds"] = time.monotonic() - start
                    base.write_json(args.summary, result)
                    print(json.dumps({"STOP_NEW_KEY": row["id"], "sigma": row["sigma"]}), flush=True)
                    return
            out.flush()
            print(json.dumps(dict(k=k, completed=len(samples),
                                  seconds=round(time.monotonic() - start, 2))), flush=True)
    result = base.summarize(samples)
    result["elapsed_seconds"] = time.monotonic() - start
    base.write_json(args.summary, result)
    print(json.dumps(result["total"]), flush=True)


if __name__ == "__main__":
    main()
