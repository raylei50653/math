#!/usr/bin/env python3
"""Reproducible, nonuniform C5-disk sampling with exact ten-row SAT queries.

The supplied oriented triangulation is the source, not a catalogue stand-in.
python-sat is an isolated external dependency; no production modules imported.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations
import json
import math
from pathlib import Path
import random
import sys
import time

HERE = Path(__file__).resolve().parent
PATTERNS = ("01012", "01021", "01023", "01201", "01202", "01203",
            "01212", "01213", "01231", "01232")
PROFILES = ("free", "chordless", "degree-biased")
RIM = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def load_catalogue():
    data = json.loads((HERE / "frozen/artifacts/c5_cells/cells.json").read_text())
    assert ["".join(map(str, p)) for p in data["pattern_order"]] == list(PATTERNS)
    assert len(data["cells"]) == data["distinct_sigma"] == 132
    return data


class Disk:
    def __init__(self):
        self.n = 6
        self.faces = {}
        self.incident = {}
        self.edge_list = []
        self.edge_index = {}
        self.degree = [0] * 6
        self.next_face = 0
        for i in range(5):
            self.add_face((i, (i + 1) % 5, 5))

    def add_face(self, face):
        fid = self.next_face
        self.next_face += 1
        self.faces[fid] = tuple(face)
        for u, v in zip(face, (*face[1:], face[0])):
            e = tuple(sorted((u, v)))
            if e not in self.incident:
                self.incident[e] = set()
                self.edge_index[e] = len(self.edge_list)
                self.edge_list.append(e)
                self.degree[u] += 1
                self.degree[v] += 1
            self.incident[e].add(fid)
        return fid

    def remove_face(self, fid):
        face = self.faces.pop(fid)
        for u, v in zip(face, (*face[1:], face[0])):
            e = tuple(sorted((u, v)))
            self.incident[e].remove(fid)
            if not self.incident[e]:
                del self.incident[e]
                index = self.edge_index.pop(e)
                last = self.edge_list.pop()
                if index < len(self.edge_list):
                    self.edge_list[index] = last
                    self.edge_index[last] = index
                self.degree[u] -= 1
                self.degree[v] -= 1

    def insert(self, rng):
        fid = rng.choice(sorted(self.faces))
        a, b, c = self.faces[fid]
        self.remove_face(fid)
        v = self.n
        self.n += 1
        self.degree.append(0)
        for f in ((a, b, v), (b, c, v), (c, a, v)):
            self.add_face(f)

    @staticmethod
    def deficit(v, degree):
        return max(0, (4 if v < 5 else 5) - degree)

    def flip(self, rng, profile):
        u, v = rng.choice(self.edge_list)
        old = (u, v)
        if old in RIM:
            return False
        f1, f2 = sorted(self.incident[old])
        face = self.faces[f1]
        # Choose the direction of this edge in the first oriented triangle.
        if not any(face[i] == u and face[(i + 1) % 3] == v for i in range(3)):
            u, v = v, u
        a = next(w for w in face if w not in old)
        b = next(w for w in self.faces[f2] if w not in old)
        new = tuple(sorted((a, b)))
        if len({u, v, a, b}) != 4 or new in self.incident:
            return False
        if profile != "free" and a < 5 and b < 5:
            return False
        if profile == "degree-biased":
            delta = sum(self.deficit(w, self.degree[w] + change)
                        - self.deficit(w, self.degree[w])
                        for w, change in ((u, -1), (v, -1), (a, 1), (b, 1)))
            if delta > 0 and rng.random() >= math.exp(-1.5 * delta):
                return False
        self.remove_face(f1)
        self.remove_face(f2)
        self.add_face((a, u, b))
        self.add_face((a, b, v))
        return True

    def graph(self):
        faces = []
        for f in self.faces.values():
            j = f.index(min(f))
            faces.append(f[j:] + f[:j])
        return dict(n=self.n, k=self.n - 5, boundary=list(range(5)),
                    edges=[list(e) for e in sorted(self.incident)],
                    faces=[list(f) for f in sorted(faces)])


def structure(graph):
    n = graph["n"]
    adj = [set() for _ in range(n)]
    for u, v in graph["edges"]:
        adj[u].add(v)
        adj[v].add(u)
    degree = list(map(len, adj))
    remaining = set(range(n))
    reduced_degree = degree[:]
    queue = deque(v for v in range(5, n) if degree[v] <= 3)
    while queue:
        v = queue.popleft()
        if v not in remaining:
            continue
        remaining.remove(v)
        for w in adj[v] & remaining:
            reduced_degree[w] -= 1
            if w >= 5 and reduced_degree[w] <= 3:
                queue.append(w)
    triangles = {tuple(sorted((u, v, w)))
                 for u in range(n) for v in adj[u] if v > u
                 for w in adj[u] & adj[v] if w > v}
    separating = triangles - {tuple(sorted(f)) for f in graph["faces"]}
    crosscuts = sum(tuple(sorted((a, b))) not in RIM
                    for v in range(5, n)
                    for a, b in combinations(sorted(adj[v] & set(range(5))), 2))
    chords = [e for e in graph["edges"] if e[1] < 5 and tuple(e) not in RIM]
    energy = sum(Disk.deficit(v, degree[v]) for v in range(n))
    all_interior_neighbors = sum(degree[v] == 5 and all(w >= 5 for w in adj[v])
                                 for v in range(5, n))
    return dict(boundary_degrees=degree[:5], minimum_interior_degree=min(degree[5:]),
                interior_degree_histogram=dict(sorted(Counter(degree[5:]).items())),
                n5=sum(d == 5 for d in degree[5:]),
                interior_degree5_centers_without_boundary_neighbors=all_interior_neighbors,
                r1_core_k=len(remaining) - 5,
                nonfacial_triangles=len(separating), two_edge_crosscuts=crosscuts,
                boundary_chords=len(chords), degree_deficit=energy,
                minimum_source_geometry=(not chords and energy == 0
                                         and not separating and crosscuts == 0))


def exact_sigma(n, edges):
    from pysat.solvers import Solver

    clauses = []
    for v in range(n):
        clauses.append([4 * v + c + 1 for c in range(4)])
        for c, d in combinations(range(4), 2):
            clauses.append([-(4 * v + c + 1), -(4 * v + d + 1)])
    for u, v in edges:
        clauses.extend([[-(4 * u + c + 1), -(4 * v + c + 1)] for c in range(4)])
    witnesses = []
    with Solver(name="g4", bootstrap_with=clauses) as solver:
        for word in PATTERNS:
            assumptions = [4 * v + int(c) + 1 for v, c in enumerate(word)]
            answer = solver.solve(assumptions=assumptions)
            if answer is not True and answer is not False:
                raise RuntimeError("UNRESOLVED SAT decision")
            if answer:
                positive = set(x for x in solver.get_model() if x > 0)
                colors = [next(c for c in range(4) if 4 * v + c + 1 in positive)
                          for v in range(n)]
                assert colors[:5] == list(map(int, word))
                assert all(colors[u] != colors[v] for u, v in edges)
                witnesses.append(colors)
            else:
                witnesses.append(None)
    sigma = sum(1 << j for j, w in enumerate(witnesses) if w is not None)
    return sigma, witnesses


def derive_seed(master, profile, k, index):
    return int.from_bytes(sha256(f"{master}/{profile}/{k}/{index}".encode()).digest()[:8], "big")


def make_sample(master, profile, k, index, steps):
    seed = derive_seed(master, profile, k, index)
    rng = random.Random(seed)
    disk = Disk()
    for _ in range(k - 1):
        disk.insert(rng)
    accepted = sum(disk.flip(rng, profile) for _ in range(steps * disk.n))
    graph = disk.graph()
    sigma, witnesses = exact_sigma(graph["n"], graph["edges"])
    graph_hash = sha256(canonical_bytes({s: graph[s] for s in ("n", "boundary", "edges")})).hexdigest()
    return dict(id=f"{profile}/k{k}/{index}", profile=profile, seed=seed,
                sample_index=index, master_seed=master, attempted_flips=steps * disk.n,
                accepted_flips=accepted, graph_sha256=graph_hash, **graph,
                rows=list(PATTERNS), sigma=sigma, witnesses=witnesses,
                structure=structure(graph))


def calibrate():
    catalogue = load_catalogue()
    checked = []
    for key, cell in sorted(catalogue["cells"].items(), key=lambda pair: int(pair[0])):
        n = 5 + cell["k_eff"]
        edges = sorted({tuple(sorted(e)) for e in cell["edges"]} | RIM)
        sigma, _ = exact_sigma(n, edges)
        if sigma != int(key):
            raise ValueError(f"catalogue calibration mismatch {key} -> {sigma}")
        checked.append(sigma)
    # An intentionally nonplanar graph tests that the evaluator does not force
    # its output into K132, or apply an unproved planar necessary screen.
    nonplanar = sorted(RIM | set(combinations(range(5, 10), 2)))
    sigma, _ = exact_sigma(10, nonplanar)
    assert sigma == 0 and "0" not in catalogue["cells"]
    return dict(catalogue_representatives=len(checked), mismatches=0,
                nonplanar_K5_control_sigma=sigma, nonplanar_control_outside_K132=True)


def summarize(samples):
    known = {int(s) for s in load_catalogue()["cells"]}
    groups = {}
    total = Counter()
    hashes = set()
    for row in samples:
        key = f"{row['profile']}/k{row['k']}"
        group = groups.setdefault(key, dict(samples=0, sigma_histogram=Counter(),
            r1_core_histogram=Counter(), interior_min_degree_histogram=Counter(),
            degree_deficit_histogram=Counter(), nonfacial_triangle_histogram=Counter(),
            minimum_source_geometry=0, accepted_flips=0, attempted_flips=0,
            boundary_chord_histogram=Counter(), two_edge_crosscut_histogram=Counter(),
            n5_histogram=Counter()))
        group["samples"] += 1
        group["sigma_histogram"][row["sigma"]] += 1
        for name, field in (("r1_core_histogram", "r1_core_k"),
                ("interior_min_degree_histogram", "minimum_interior_degree"),
                ("degree_deficit_histogram", "degree_deficit"),
                ("nonfacial_triangle_histogram", "nonfacial_triangles"),
                ("boundary_chord_histogram", "boundary_chords"),
                ("two_edge_crosscut_histogram", "two_edge_crosscuts"),
                ("n5_histogram", "n5")):
            group[name][row["structure"][field]] += 1
        group["minimum_source_geometry"] += row["structure"]["minimum_source_geometry"]
        for field in ("accepted_flips", "attempted_flips"):
            group[field] += row[field]
        total["samples"] += 1
        total["outside_K132"] += row["sigma"] not in known
        total["minimum_source_geometry"] += row["structure"]["minimum_source_geometry"]
        hashes.add(row["graph_sha256"])
    return dict(total=dict(total), distinct_labelled_graphs=len(hashes),
                sigma_histogram=dict(sorted(Counter(r["sigma"] for r in samples).items())),
                groups=groups, inference="Nonuniform seeded finite experiment; general coverage OPEN")


def write_json(path, value):
    with Path(path).open("x") as f:
        json.dump(value, f, sort_keys=True, indent=2)
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sat-path", type=Path, default=Path("/tmp/c5-large-k-sat-78375cc"))
    sub = parser.add_subparsers(dest="command", required=True)
    cal = sub.add_parser("calibrate")
    cal.add_argument("--output", type=Path, required=True)
    run = sub.add_parser("sample")
    run.add_argument("--output", type=Path, required=True)
    run.add_argument("--summary", type=Path, required=True)
    run.add_argument("--per-stratum", type=int, default=100)
    run.add_argument("--k-min", type=int, default=25)
    run.add_argument("--k-max", type=int, default=60)
    run.add_argument("--master-seed", type=int, default=20261023)
    run.add_argument("--steps-per-vertex", type=int, default=40)
    replay = sub.add_parser("replay")
    replay.add_argument("samples", type=Path)
    replay.add_argument("--output", type=Path, required=True)
    replay.add_argument("--stride", type=int, default=1)
    replay.add_argument("--limit", type=int)
    args = parser.parse_args()
    sys.path.insert(0, str(args.sat_path))
    start = time.monotonic()
    if args.command == "calibrate":
        result = calibrate()
    elif args.command == "sample":
        known = {int(s) for s in load_catalogue()["cells"]}
        samples = []
        with args.output.open("x") as out:
            for profile in PROFILES:
                for k in range(args.k_min, args.k_max + 1):
                    for index in range(args.per_stratum):
                        row = make_sample(args.master_seed, profile, k, index, args.steps_per_vertex)
                        out.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
                        samples.append(row)
                        if row["sigma"] not in known:
                            out.flush()
                            result = summarize(samples)
                            result["new_key_candidate"] = row["id"]
                            result["elapsed_seconds"] = time.monotonic() - start
                            write_json(args.summary, result)
                            print(json.dumps({"STOP_NEW_KEY": row["id"], "sigma": row["sigma"]}), flush=True)
                            return
                    out.flush()
                    print(json.dumps(dict(profile=profile, k=k, completed=len(samples),
                                          seconds=round(time.monotonic() - start, 2))), flush=True)
        result = summarize(samples)
        result["elapsed_seconds"] = time.monotonic() - start
        write_json(args.summary, result)
        print(json.dumps(result["total"]), flush=True)
        return
    else:
        count = 0
        with args.samples.open() as f:
            for index, line in enumerate(f):
                if index % args.stride:
                    continue
                row = json.loads(line)
                regenerated = make_sample(row["master_seed"], row["profile"], row["k"],
                    row["sample_index"], row["attempted_flips"] // row["n"])
                # JSON stringifies integer histogram keys; compare its actual
                # persisted representation, including all null rows/witnesses.
                if json.loads(json.dumps(regenerated)) != row:
                    raise ValueError(f"replay mismatch {row['id']}")
                count += 1
                if args.limit and count >= args.limit:
                    break
        result = dict(replayed=count, deterministic_bytes_match=True)
    result["elapsed_seconds"] = time.monotonic() - start
    write_json(args.output, result)
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
