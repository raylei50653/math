#!/usr/bin/env python3
"""Independent framed-graph canonicalization for Task ER.

Only complete graph adjacency enters the certificate: plane rotations do not.
Vertices 0..4 form the named C5; k counts inner vertices. NA/AD have the
unordered pair of roots {5,6}; D6 has root 5. The remaining inner vertices
are interchangeable. Thus the groups are D5 x S2 x S_(k-2) and
D5 x S_(k-1), respectively. Root degrees are the generator's responsibility;
this module also supports partial graphs while retaining their root roles.

This implements ordered equitable refinement with exact individualization.
The canonical adjacency string is the minimum *refinement-tree* leaf over
all ten C5 frames and all allowed root orders. It is an independent graph
certificate, not a promise of the lexicographically least adjacency string
over every permutation. Equal certificates are equivalent to membership in
the same stated group orbit.

Counting leaves attaining the canonical certificate gives the exact
stabilizer: every automorphism transports a winning refinement path to a
unique winning path, and two winning labelings differ by an automorphism.
An explicitly verified twin cell is collapsed with its factorial weight.
No external graph library or finite-search implementation is imported.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
from collections import defaultdict
from functools import lru_cache
from typing import Iterable, NamedTuple

Edge = tuple[int, int]
Partition = tuple[tuple[int, ...], ...]


class CanonicalResult(NamedTuple):
    code: str
    edges: tuple[Edge, ...]
    orbit_size: int
    stabilizer_size: int
    permutation: tuple[int, ...]  # original vertex -> canonical vertex


def _parameters(type: str, k: int) -> tuple[int, int, int]:
    if type not in ("NA", "AD", "D6"):
        raise ValueError("type must be NA, AD, or D6")
    roots = 1 if type == "D6" else 2
    if not isinstance(k, int) or k < roots:
        raise ValueError(f"{type} requires at least {roots} inner vertices")
    return 5 + k, 5 + roots, 10 * math.factorial(k - roots) * (2 if roots == 2 else 1)


def _normalize(n: int, edges: Iterable[Iterable[int]]) -> tuple[Edge, ...]:
    result = set()
    for edge in edges:
        pair = tuple(edge)
        if len(pair) != 2:
            raise ValueError("each edge must have two endpoints")
        u, v = pair
        if not isinstance(u, int) or not isinstance(v, int) or not (0 <= u < n and 0 <= v < n) or u == v:
            raise ValueError(f"invalid simple-graph edge: {pair}")
        result.add((min(u, v), max(u, v)))
    return tuple(sorted(result))


@lru_cache(maxsize=16)
def _positions(n: int) -> tuple[tuple[int, ...], ...]:
    """Bit weights for the row-major upper triangle; first pair is highest."""
    result = [[0] * n for _ in range(n)]
    shift = n * (n - 1) // 2 - 1
    for u in range(n):
        for v in range(u + 1, n):
            result[u][v] = result[v][u] = 1 << shift
            shift -= 1
    return tuple(tuple(row) for row in result)


def _integer_code(order: tuple[int, ...], edges: tuple[Edge, ...], positions: tuple[tuple[int, ...], ...]) -> int:
    mapped = [0] * len(order)
    for target, original in enumerate(order):
        mapped[original] = target
    code = 0
    for u, v in edges:
        code |= positions[mapped[u]][mapped[v]]
    return code


def _refine(partition: Partition, adjacency: tuple[int, ...]) -> Partition:
    """Refine each existing ordered cell by its ordered neighbor counts."""
    while True:
        masks = tuple(sum(1 << u for u in cell) for cell in partition)
        refined = []
        for cell in partition:
            if len(cell) == 1:
                refined.append(cell)
                continue
            buckets = defaultdict(list)
            for u in cell:
                signature = tuple((adjacency[u] & mask).bit_count() for mask in masks)
                buckets[signature].append(u)
            refined.extend(tuple(buckets[signature]) for signature in sorted(buckets))
        result = tuple(refined)
        if len(result) == len(partition):
            return result
        partition = result


def _twins(cell: tuple[int, ...], adjacency: tuple[int, ...]) -> bool:
    """Pair transpositions preserve adjacency iff vertices are true/false twins."""
    u = cell[0]
    return all(((adjacency[u] ^ adjacency[v]) & ~((1 << u) | (1 << v))) == 0 for v in cell[1:])


def _leaf_minimum(partition: Partition, adjacency: tuple[int, ...], edges: tuple[Edge, ...], positions: tuple[tuple[int, ...], ...]) -> tuple[int, int, tuple[int, ...]]:
    partition = _refine(partition, adjacency)
    weight = 1
    expanded = []
    for cell in partition:
        if len(cell) > 1 and _twins(cell, adjacency):
            weight *= math.factorial(len(cell))
            expanded.extend((u,) for u in cell)
        else:
            expanded.append(cell)
    partition = tuple(expanded)
    index = next((i for i, cell in enumerate(partition) if len(cell) > 1), None)
    if index is None:
        order = tuple(cell[0] for cell in partition)
        return _integer_code(order, edges, positions), weight, order
    cell = partition[index]
    best = None
    count = 0
    best_order = ()
    for u in cell:
        rest = tuple(v for v in cell if v != u)
        child = partition[:index] + ((u,), rest) + partition[index + 1:]
        code, multiplicity, order = _leaf_minimum(child, adjacency, edges, positions)
        if best is None or code < best:
            best, count, best_order = code, multiplicity, order
        elif code == best:
            count += multiplicity
    assert best is not None
    return best, weight * count, best_order


def canonical(type: str, k: int, edges: Iterable[Iterable[int]]) -> CanonicalResult:
    """Return an exact abstract framed-graph orbit certificate and sizes.

    `edges` must include the full graph (including all C5 edges). This function
    neither adds frame edges nor checks root degrees, criticality or planarity.
    `permutation` transports any same-graph named data into the returned frame.
    """
    n, first_free, group_size = _parameters(type, k)
    normalized = _normalize(n, edges)
    adjacency = [0] * n
    for u, v in normalized:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    adjacency = tuple(adjacency)
    free = tuple(range(first_free, n))
    free_mask = sum(1 << u for u in free)
    positions = _positions(n)
    free_bits = len(free) * (len(free) - 1) // 2

    # Initial refinement signatures already fix every anchor/free adjacency
    # bit. Reject larger anchor prefixes before doing expensive exact search.
    # Refinement only splits existing cells, so this prefix cannot change.
    best_prefix = None
    initial_partitions = []
    root_orders = ((5,),) if type == "D6" else ((5, 6), (6, 5))
    for sign in (-1, 1):
        for offset in range(5):
            frame = tuple((offset + sign * i) % 5 for i in range(5))
            for roots in root_orders:
                anchors = frame + roots
                buckets = defaultdict(list)
                for u in free:
                    signature = tuple((adjacency[u] >> v) & 1 for v in anchors) + ((adjacency[u] & free_mask).bit_count(),)
                    buckets[signature].append(u)
                cells = tuple(tuple(buckets[s]) for s in sorted(buckets))
                partition = tuple((u,) for u in anchors) + cells
                order = tuple(u for cell in partition for u in cell)
                prefix = _integer_code(order, normalized, positions) >> free_bits
                if best_prefix is None or prefix < best_prefix:
                    best_prefix = prefix
                    initial_partitions = [partition]
                elif prefix == best_prefix:
                    initial_partitions.append(partition)

    best = None
    stabilizer = 0
    best_order = ()
    for partition in initial_partitions:
        code, count, order = _leaf_minimum(partition, adjacency, normalized, positions)
        if best is None or code < best:
            best, stabilizer, best_order = code, count, order
        elif code == best:
            stabilizer += count
    assert best is not None and stabilizer > 0 and group_size % stabilizer == 0
    permutation = [0] * n
    for target, original in enumerate(best_order):
        permutation[original] = target
    mapped = tuple(sorted((min(permutation[u], permutation[v]), max(permutation[u], permutation[v])) for u, v in normalized))
    bits = format(best, f"0{n * (n - 1) // 2}b")
    return CanonicalResult(f"{type}:{k}:{bits}", mapped, group_size // stabilizer, stabilizer, tuple(permutation))


def group_permutations(type: str, k: int) -> Iterable[tuple[int, ...]]:
    """Independent exhaustive group listing, for bounded cross-checks."""
    n, first_free, _ = _parameters(type, k)
    for offset in range(5):
        for sign in (1, -1):
            boundary_images = tuple((offset + sign * u) % 5 for u in range(5))
            roots = ((5,),) if type == "D6" else ((5, 6), (6, 5))
            for root_images in roots:
                for free_images in itertools.permutations(range(first_free, n)):
                    yield boundary_images + root_images + free_images


def exhaustive_orbit(type: str, k: int, edges: Iterable[Iterable[int]]) -> set[tuple[Edge, ...]]:
    """Enumerate the literal full-edge orbit; intended for small k."""
    n, _, _ = _parameters(type, k)
    normalized = _normalize(n, edges)
    return {tuple(sorted((min(p[u], p[v]), max(p[u], p[v])) for u, v in normalized)) for p in group_permutations(type, k)}


def self_check(max_k: int = 5, samples: int = 2, seed: int = 2601004) -> dict:
    """Cross-check exact sizes and invariance over every group image.

    Includes sparse/dense symmetry controls and independent random graphs.
    The exhaustive oracle does not use equitable refinement or ES code.
    """
    if max_k > 5:
        raise ValueError("self-check exhausts every image; max_k must be <=5")
    rng = random.Random(seed)
    records = []
    certificates = {}
    images_checked = 0
    for type in ("NA", "AD", "D6"):
        for k in range(1 if type == "D6" else 2, max_k + 1):
            n = 5 + k
            frame = {(min(i, (i + 1) % 5), max(i, (i + 1) % 5)) for i in range(5)}
            if type == "AD":
                frame.add((5, 6))
            optional = [(u, v) for u in range(n) for v in range(max(5, u + 1), n) if (u, v) not in frame and not (type == "NA" and (u, v) == (5, 6))]
            examples = [frame, frame | set(optional), frame | {e for e in optional if e[0] >= 5}]
            for _ in range(samples):
                probability = rng.choice((0.2, 0.5, 0.8))
                examples.append(frame | {edge for edge in optional if rng.random() < probability})
            for edges in examples:
                result = canonical(type, k, edges)
                orbit = exhaustive_orbit(type, k, edges)
                assert result.edges in orbit
                assert result.orbit_size == len(orbit)
                group_size = _parameters(type, k)[2]
                assert result.stabilizer_size == group_size // len(orbit)
                for image in orbit:
                    equivalent = canonical(type, k, image)
                    assert equivalent.code == result.code
                    assert equivalent.edges == result.edges
                    assert equivalent.orbit_size == result.orbit_size
                    images_checked += 1
                orbit_id = (type, k, min(orbit))
                previous = certificates.setdefault(result.code, orbit_id)
                assert previous == orbit_id, "certificate collision between distinct exhaustive orbits"
                records.append({"type": type, "k": k, "edges": len(edges), "orbit_size": len(orbit), "stabilizer_size": result.stabilizer_size})
    return {"schema": "c5-er-canonical-self-check-v1", "max_k": max_k, "seed": seed, "samples": samples, "graphs_checked": len(records), "all_group_images_checked": images_checked, "passed": True, "records": records}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--check", action="store_true",
                        help="Replay stored ER controls byte-for-byte")
    parser.add_argument("--max-k", type=int, default=5)
    parser.add_argument("--samples", type=int, default=2)
    args = parser.parse_args()
    if args.check:
        from pathlib import Path
        import subprocess
        import sys
        driver = Path(__file__).with_name("c5_excess_two_independent_search.py")
        completed = subprocess.run(
            [sys.executable, str(driver), "--controls-only", "--check"],
            check=False)
        raise SystemExit(completed.returncode)
    if not args.self_check:
        parser.error("use --check, --self-check, or import canonical(type,k,edges)")
    print(json.dumps(self_check(args.max_k, args.samples), sort_keys=True))


if __name__ == "__main__":
    main()
