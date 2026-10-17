#!/usr/bin/env python3
"""Finite cap arithmetic and parent-input custody, not a source enumerator."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(u, v):
    return tuple(sorted((u, v)))


def crosses(e, f):
    if set(e) & set(f):
        return False
    a, b = e
    c, d = f
    return (a < c < b) != (a < d < b)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", choices=["allow-aw", "wheel-chord"])
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    manifest = json.loads((root / "INPUTS.json").read_text())
    require(manifest["base"] == "6c420f3ca77d60952ed76f93dff7449c522715ca", "wrong BASE")
    for entry in manifest["entries"]:
        raw = (root / entry["frozen_path"]).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == entry["sha256"], "frozen drift: " + entry["path"])

    # Cyclic order (a,p,h,w,t); the c computation has the identical five
    # labelled positions (c,q,h,v,s) in the same original-source argument.
    boundary = {edge(i, (i + 1) % 5) for i in range(5)}
    diagonals = sorted(set(itertools.combinations(range(5), 2)) - boundary)
    all_triangulations = []
    for chords in itertools.combinations(diagonals, 2):
        if not crosses(*chords):
            all_triangulations.append(chords)
    require(len(all_triangulations) == 5, "pentagon triangulation enumeration failed")
    forbidden = set() if args.negative == "allow-aw" else {edge(0, 3)}
    empty_rows = []
    for chords in all_triangulations:
        if forbidden.intersection(chords):
            continue
        cap_edges = boundary | set(chords)
        cap_degree = sum(0 in e for e in cap_edges)
        # The actual sector proof supplies exactly two outside neighbours
        # y,b (respectively x,b), in addition to the bounded cap link.
        full_degree = cap_degree + 2
        require(full_degree <= 5, "removing original aw/cv nonedge permits full degree " + str(full_degree))
        empty_rows.append({"chords": chords, "cap_degree": cap_degree, "full_degree": full_degree})
    require(len(empty_rows) == 3, "wrong empty-cap count")

    wheel_edges = boundary | {edge(5, i) for i in range(5)}
    if args.negative == "wheel-chord":
        wheel_edges.add(edge(0, 2))
    # Euler for a triangulated b=5 disk with s=1 gives exactly 10 edges.
    require(len(wheel_edges) == 3 * 1 + 2 * 5 - 3, "a W5 plus boundary chord violates cap Euler count")
    require(sum(0 in e for e in wheel_edges) + 2 == 5, "wrong W5 complete boundary degree")
    output = {
        "base": manifest["base"],
        "frozen_inputs_checked": len(manifest["entries"]),
        "empty_cap_triangulations": empty_rows,
        "wheel_full_degree": 5,
        "scope": "local cap arithmetic only; original sector and arbitrary-size source theorem are paper proof",
    }
    print(json.dumps(output, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
