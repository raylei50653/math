#!/usr/bin/env python3
"""Small independent labelled edge-subset reference for the excess-two layers.

The outer cycle is 0,1,2,3,4 and the inner labels are 5,...,4+k.
Every inner-edge subset and every degree-prescribed spoke tuple is visited.
No embedded-map generator, source search, or prior finite-search module is used.

An outcome cache identifies only uniform relabellings: D5 on the boundary,
the interchange of the two degree-five roots, and permutations of ordinary
inner vertices.  In particular, each original labelled tuple contributes one
to its counts, even when its disk/coloring outcome is retrieved from the cache.
The cache does not discard Q values or impose a support-size bound.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path
from typing import Callable, Iterable

import networkx as nx


FRAME = tuple((i, (i + 1) % 5) for i in range(5))
FRAME_SET = frozenset(tuple(sorted(e)) for e in FRAME)
T4_MASK = 932
SINGLETON_ROWS = (6, 4, 3, 1, 0)
KINDS = ("NA", "AD", "D6")


def _edges(pairs: tuple[tuple[int, int], ...], mask: int) -> tuple[tuple[int, int], ...]:
    return tuple(e for bit, e in enumerate(pairs) if mask & (1 << bit))


def _connected(k: int, edges: Iterable[tuple[int, int]]) -> bool:
    adj = [[] for _ in range(k)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    reached = {0}
    pending = [0]
    while pending:
        for v in adj[pending.pop()]:
            if v not in reached:
                reached.add(v)
                pending.append(v)
    return len(reached) == k


def _inner_permutations(kind: str, k: int) -> tuple[tuple[int, ...], ...]:
    if kind == "D6":
        return tuple((0,) + tail for tail in permutations(range(1, k)))
    return tuple(roots + tail for roots in ((0, 1), (1, 0))
                 for tail in permutations(range(2, k)))


def _permuted_h_mask(edges: Iterable[tuple[int, int]], p: tuple[int, ...],
                     edge_bits: dict[tuple[int, int], int]) -> int:
    out = 0
    for u, v in edges:
        out |= 1 << edge_bits[tuple(sorted((p[u], p[v])))]
    return out


def _boundary_maps() -> tuple[tuple[int, ...], ...]:
    # Each table acts on the 32 possible subsets of named boundary contacts.
    return tuple(tuple(sum(1 << ((shift + direction * v) % 5)
                           for v in range(5) if mask & (1 << v))
                       for mask in range(32))
                 for direction in (1, -1) for shift in range(5))


BOUNDARY_MAPS = _boundary_maps()
SPOKE_CHOICES = tuple(tuple(sum(1 << v for v in vs)
                           for vs in combinations(range(5), size))
                     for size in range(4))


def _q(mask: int) -> tuple[int, ...]:
    return tuple(pos for pos, row in enumerate(SINGLETON_ROWS)
                 if not mask & (1 << row))


def _q_shape(q: tuple[int, ...]) -> tuple[int, int, int]:
    mask = sum(1 << v for v in q)
    components = (1 if len(q) == 5 else
                  sum(v in q and (v - 1) % 5 not in q for v in range(5)))
    return len(q), components, min(mapping[mask] for mapping in BOUNDARY_MAPS)


def _graph_edges(k: int, h_edges: tuple[tuple[int, int], ...],
                 spokes: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    edges = list(FRAME_SET)
    edges.extend((u + 5, v + 5) for u, v in h_edges)
    edges.extend((v, u + 5) for u, mask in enumerate(spokes)
                 for v in range(5) if mask & (1 << v))
    return tuple(sorted(edges))


def _is_disk(k: int, edges: tuple[tuple[int, int], ...]) -> bool:
    # The augmented graph has 6+k vertices and five extra apex edges.
    if len(edges) + 5 > 3 * (6 + k) - 6:
        return False
    augmented = nx.Graph()
    augmented.add_nodes_from(range(6 + k))
    augmented.add_edges_from(edges)
    augmented.add_edges_from((v, 5 + k) for v in range(5))
    return nx.check_planarity(augmented, counterexample=False)[0]


def _empty(kind: str, k: int) -> dict:
    return {
        "kind": kind,
        "k": k,
        "counts": {"degree_candidates": 0, "disk": 0, "t4": 0,
                   "q": 0, "crit": 0},
        "Q_shape_distribution": [],
        "q_orbits": [],
        "crit_codes": [],
    }


def brute_layer(kind: str, k: int, *,
                progress: Callable[[dict], None] | None = None) -> dict:
    """Return deterministic labelled counts and canonical Q/critical sets.

    The reference domain is k <= 5.  Counts ``q`` and ``crit`` are cumulative
    after the disk and T4 screens.  Q_shape_distribution counts labelled
    graphs in the q layer, grouped by Q_size, induced cyclic component count
    c_Q, and the least dihedral five-bit Q mask.
    """
    if kind not in KINDS:
        raise ValueError(f"unknown layer {kind!r}; expected one of {KINDS}")
    if not isinstance(k, int) or not 0 <= k <= 5:
        raise ValueError("independent brute reference requires 0 <= k <= 5")
    result = _empty(kind, k)
    if k < (3 if kind == "AD" else 4):
        return result

    # The shared helpers are new ER implementations.  Lazy imports also make
    # the genuinely empty layers runnable before those helpers are installed.
    from c5_excess_two_independent_coloring import sigma_mask
    from c5_excess_two_independent_canonical import canonical

    pairs = tuple(combinations(range(k), 2))
    edge_bits = {edge: bit for bit, edge in enumerate(pairs)}
    inner_perms = _inner_permutations(kind, k)
    desired = tuple(6 if kind == "D6" and u == 0 else
                    5 if kind != "D6" and u < 2 else 4 for u in range(k))
    # Each canonical H has its own exact support-tuple cache and automorphisms.
    h_data: dict[int, tuple[tuple[tuple[int, int], ...],
                            tuple[tuple[int, ...], ...], dict]] = {}
    q_orbits: dict[str, dict] = {}
    shapes: Counter[tuple[int, int, int]] = Counter()
    counts = result["counts"]
    outcome_calls = 0

    for h_mask in range(1 << len(pairs)):
        h_edges = _edges(pairs, h_mask)
        if kind != "D6" and (((0, 1) in h_edges) != (kind == "AD")):
            continue
        degrees = [0] * k
        for u, v in h_edges:
            degrees[u] += 1
            degrees[v] += 1
        spoke_degrees = tuple(desired[u] - degrees[u] for u in range(k))
        if any(s < 0 or s > 3 for s in spoke_degrees):
            continue
        if not _connected(k, h_edges):
            continue

        h_code, to_canonical_h = min(
            (_permuted_h_mask(h_edges, p, edge_bits), p) for p in inner_perms)
        if h_code not in h_data:
            canonical_h_edges = _edges(pairs, h_code)
            automorphisms = tuple(p for p in inner_perms
                                  if _permuted_h_mask(canonical_h_edges, p, edge_bits)
                                  == h_code)
            h_data[h_code] = (canonical_h_edges, automorphisms, {})
        canonical_h_edges, automorphisms, cache = h_data[h_code]

        for labelled_spokes in product(*(SPOKE_CHOICES[s] for s in spoke_degrees)):
            counts["degree_candidates"] += 1
            spokes_list = [0] * k
            for u, mask in enumerate(labelled_spokes):
                spokes_list[to_canonical_h[u]] = mask
            spokes = tuple(spokes_list)
            outcome = cache.get(spokes)
            if outcome is None:
                outcome_calls += 1
                graph_edges = _graph_edges(k, canonical_h_edges, spokes)
                disk = _is_disk(k, graph_edges)
                t4 = q_present = critical = False
                shape = None
                if disk:
                    mask = sigma_mask(graph_edges, 5 + k)
                    t4 = (mask & T4_MASK) == T4_MASK
                    q = _q(mask)
                    q_present = t4 and bool(q)
                    if q_present:
                        shape = _q_shape(q)
                        critical = all(
                            sigma_mask(graph_edges[:i] + graph_edges[i + 1:], 5 + k)
                            != mask
                            for i, edge in enumerate(graph_edges)
                            if edge not in FRAME_SET)
                        representative = canonical(kind, k, graph_edges)
                        code = representative.code
                        canonical_edges = tuple(tuple(e) for e in representative.edges)
                        canonical_mask = sigma_mask(canonical_edges, 5 + k)
                        row = {
                            "code": code,
                            "canonical_edges": [list(e) for e in canonical_edges],
                            "orbit_size": representative.orbit_size,
                            "stabilizer_size": representative.stabilizer_size,
                            "sigma_mask": canonical_mask,
                            "Q": list(_q(canonical_mask)),
                            "crit": critical,
                        }
                        if code in q_orbits and q_orbits[code] != row:
                            raise AssertionError("uniform relabelling changed an orbit outcome")
                        q_orbits[code] = row
                outcome = (disk, t4, q_present, critical, shape)
                # Mark every exact relabelling in this canonical H.  The target
                # T4 rows, nonempty Q, Q shape, and Sigma-criticality are all
                # invariant under the same boundary/inner permutation action.
                for p in automorphisms:
                    permuted = [0] * k
                    for u, value in enumerate(spokes):
                        permuted[p[u]] = value
                    for boundary_map in BOUNDARY_MAPS:
                        key = tuple(boundary_map[value] for value in permuted)
                        prior = cache.setdefault(key, outcome)
                        if prior != outcome:
                            raise AssertionError("inconsistent relabelling cache")

            disk, t4, q_present, critical, shape = outcome
            counts["disk"] += int(disk)
            counts["t4"] += int(t4)
            counts["q"] += int(q_present)
            counts["crit"] += int(critical)
            if q_present:
                shapes[shape] += 1
        if progress is not None:
            progress({"kind": kind, "k": k, "H_mask": h_mask,
                      "counts": dict(counts), "outcome_calls": outcome_calls})

    result["Q_shape_distribution"] = [
        {"Q_size": size, "c_Q": components, "canonical_mask": mask, "count": count}
        for (size, components, mask), count in sorted(shapes.items())]
    result["q_orbits"] = [q_orbits[code] for code in sorted(q_orbits)]
    result["crit_codes"] = sorted(code for code, row in q_orbits.items() if row["crit"])
    if sum(row["orbit_size"] for row in result["q_orbits"]) != counts["q"]:
        raise AssertionError("canonical orbit sizes do not reproduce labelled Q count")
    if sum(row["orbit_size"] for row in result["q_orbits"] if row["crit"]) != counts["crit"]:
        raise AssertionError("canonical orbit sizes do not reproduce labelled critical count")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=KINDS, required=True)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check and args.output is None:
        parser.error("--check requires --output")
    payload = (json.dumps(brute_layer(args.kind, args.k), indent=2, sort_keys=True)
               + "\n").encode()
    if args.output is None:
        print(payload.decode(), end="")
    elif args.check:
        if args.output.read_bytes() != payload:
            raise RuntimeError(f"byte mismatch: {args.output}")
    else:
        with args.output.open("xb") as output:
            output.write(payload)


if __name__ == "__main__":
    main()
