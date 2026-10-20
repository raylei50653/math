#!/usr/bin/env python3
"""Independent direct-state closure; no H-row or frozen model imports."""
import argparse
import hashlib
import json
from collections import defaultdict
from itertools import product
from pathlib import Path

from check import D, OLD, PAIRS, canon, noncrossing, partitions, proper


def build_family():
    states = [u for u in partitions(10, 4) if proper(u)]
    index = {u: i for i, u in enumerate(states)}
    by_sides = defaultdict(list)
    for p in partitions(10):
        if not noncrossing(p):
            continue
        blocks = max(p) + 1
        if sum(p[i] != p[(i + 1) % 10] for i in range(10)) != 2 * (blocks - 1):
            continue
        # Different components encountered across a boundary edge must be
        # opposite complementary sides. Solve those equations independently.
        neighbours = [set() for _ in range(blocks)]
        for i in range(10):
            x, y = p[i], p[(i + 1) % 10]
            if x != y:
                neighbours[x].add(y)
                neighbours[y].add(x)
        labels = {0: 0}
        pending = [0]
        possible = True
        while pending:
            x = pending.pop()
            for y in neighbours[x]:
                if y in labels:
                    if labels[y] == labels[x]:
                        possible = False
                else:
                    labels[y] = 1 - labels[x]
                    pending.append(y)
        assert len(labels) == blocks
        if possible:
            side = tuple(labels[x] for x in p)
            by_sides[side].append(p)
            by_sides[tuple(1 - x for x in side)].append(p)
    rows = []
    for i, u in enumerate(states):
        for pair in PAIRS:
            complement = tuple(c for c in range(4) if c not in pair)
            reverse = {pair[0]: pair[1], pair[1]: pair[0],
                       complement[0]: complement[1], complement[1]: complement[0]}
            side = tuple(int(value in pair) for value in u)
            supports = set()
            for p in by_sides[side]:
                support = frozenset(index[canon(
                    reverse[value] if mask & (1 << p[j]) else value
                    for j, value in enumerate(u))]
                    for mask in range(1 << (max(p) + 1)))
                supports.add(support)
            assert supports and all(i in support for support in supports)
            rows.append((i, pair, tuple(sorted(supports, key=lambda s: tuple(sorted(s))))))
    return states, index, rows


def close(rows, initial):
    live = set(initial)
    rounds = []
    while True:
        remove = {}
        for index, pair, supports in rows:
            if index in live and not any(support <= live for support in supports):
                remove.setdefault(index, pair)
        if not remove:
            return live, rounds
        rounds.append([{"core_index": i, "pair": list(remove[i])} for i in sorted(remove)])
        live.difference_update(remove)


def calculate():
    frozen = json.loads((OLD / "J2/certificate.json").read_text())
    states, index, rows = build_family()
    initial = set(frozen["live"])
    stable, rounds = close(rows, initial)
    assert stable == initial and rounds == []
    targets = set(row["core_index"] for row in frozen["forms"])
    seeds = [row for row in frozen["forms"] if row["literal_core"][6] == 2]
    seed_indices = {row["core_index"] for row in seeds}
    assert len(seeds) == len(seed_indices) == 6
    live, rounds = close(rows, initial - seed_indices)
    assert not live & targets
    # The necessary support family does not force any zero without assumptions.
    assert targets <= initial
    family_bytes = json.dumps([
        [i, list(pair), [sorted(support) for support in supports]]
        for i, pair, supports in rows], separators=(",", ":")).encode()
    return {"status": "PASS", "source_realized": False, "last_rejection": "OPEN",
            "family_rows": len(rows), "family_sha256": hashlib.sha256(family_bytes).hexdigest(),
            "method": "three complementary-pair obligations for each literal canonical state",
            "initial_live": len(initial), "seed_indices": sorted(seed_indices),
            "seed_literal_fibres": [row["literal_core"] for row in seeds],
            "target_indices": sorted(targets), "deletion_rounds": rounds,
            "final_live": sorted(live),
            "conclusion": "simultaneous six d=2 zeros imply all twelve J2 target zeros"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--certificate", type=Path, default=D / "closure-certificate.json")
    args = parser.parse_args()
    result = calculate()
    if args.build:
        with args.certificate.open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    else:
        assert json.loads(args.certificate.read_text()) == result
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("final_live", "deletion_rounds", "seed_literal_fibres")},
                     sort_keys=True))


if __name__ == "__main__":
    main()
