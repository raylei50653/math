#!/usr/bin/env python3
"""Independent named-C5 coloring by explicit frontier transfer.

The frame is vertices 0,...,4. Its representative colors come only from
c5_kempe_screen.REPS; all other vertices use the same four named colors.
No planarity assumption, Four Color Theorem, graph catalogue, finite-search
implementation, or stored ES result is used here.

The primary algorithm processes interior vertices in the fixed numeric order
5,...,n-1. A state is a tuple of colors on processed vertices with an edge to
the unprocessed suffix. Transitions check all newly closed edges and project
to the next frontier. This is exact variable elimination, without coloring
bitsets or degree-dependent variable ordering.

A separate numeric-order DFS provides coloring witnesses. A third method
iterates the complete Cartesian product of interior colors for small graphs.
Neither alternative uses the frontier transitions.

python scripts/c5_excess_two_independent_coloring.py --self-test
python scripts/c5_excess_two_independent_coloring.py --check
python scripts/c5_excess_two_independent_coloring.py --edges-json GRAPH.json
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations, product
import json
from pathlib import Path
import random
import subprocess
import sys
from time import perf_counter
from typing import Iterable, Sequence

from c5_kempe_screen import REPS

ROOT = Path(__file__).resolve().parents[1]
Edge = tuple[int, int]
Coloring = tuple[int, ...]
FRAME_EDGES = tuple(sorted((min(i, (i + 1) % 5), max(i, (i + 1) % 5))
                           for i in range(5)))
FRAME_EDGE_SET = frozenset(FRAME_EDGES)
T4_MASK = 932
T4_INDICES = tuple(i for i in range(len(REPS)) if T4_MASK & (1 << i))
SINGLETON_INDICES = (6, 4, 3, 1, 0)
ALL_ROWS_MASK = (1 << len(REPS)) - 1


@dataclass(frozen=True)
class FrontierStep:
    vertex: int
    boundary_neighbors: tuple[int, ...]
    previous_positions: tuple[int, ...]
    retained_positions: tuple[int, ...]
    retain_vertex: bool
    frontier_before: tuple[int, ...]
    frontier_after: tuple[int, ...]


@dataclass(frozen=True)
class CompiledGraph:
    """Graph data and a degree-independent fixed-order transfer schedule."""

    edges: tuple[Edge, ...]
    n_vertices: int
    adjacency: tuple[tuple[int, ...], ...]
    boundary_edges: tuple[Edge, ...]
    steps: tuple[FrontierStep, ...]
    max_frontier: int


def _edge_tuple(edges: Iterable[Sequence[int]]) -> tuple[Edge, ...]:
    result = set()
    for edge in edges:
        if len(edge) != 2:
            raise ValueError("Every edge must have two endpoints")
        u, v = edge
        if (not isinstance(u, int) or isinstance(u, bool)
                or not isinstance(v, int) or isinstance(v, bool)):
            raise ValueError("Vertex labels must be integers")
        if min(u, v) < 0 or u == v:
            raise ValueError("Edges must have distinct nonnegative endpoints")
        result.add((min(u, v), max(u, v)))
    return tuple(sorted(result))


def compile_graph(edges: Iterable[Sequence[int]] | CompiledGraph,
                  n_vertices: int | None = None) -> CompiledGraph:
    """Compile the numeric-order schedule; retain explicitly named vertices.

    The coloring routines also accept graphs with missing frame edges or
    extra frame chords. Checking the induced-C5 input domain belongs to the
    caller; those graphs are useful as negative controls.
    """
    if isinstance(edges, CompiledGraph):
        if n_vertices is not None and n_vertices != edges.n_vertices:
            raise ValueError("n_vertices differs from the compiled graph")
        return edges
    clean = _edge_tuple(edges)
    inferred = max(5, 1 + max((v for edge in clean for v in edge), default=-1))
    if n_vertices is None:
        n_vertices = inferred
    if (not isinstance(n_vertices, int) or isinstance(n_vertices, bool)
            or n_vertices < inferred):
        raise ValueError("n_vertices must include every endpoint and the frame")
    adjacency_sets = [set() for _ in range(n_vertices)]
    for u, v in clean:
        adjacency_sets[u].add(v)
        adjacency_sets[v].add(u)
    adjacency = tuple(tuple(sorted(row)) for row in adjacency_sets)
    # Future edges to the frame are impossible: its colors are already pinned.
    last_inner_neighbor = tuple(max((u for u in row if u >= 5), default=-1)
                                for row in adjacency)
    frontier: tuple[int, ...] = ()
    steps = []
    max_frontier = 0
    for vertex in range(5, n_vertices):
        positions = {u: i for i, u in enumerate(frontier)}
        previous = tuple(positions[u] for u in adjacency[vertex]
                         if 5 <= u < vertex)
        retained = tuple(i for i, u in enumerate(frontier)
                         if last_inner_neighbor[u] > vertex)
        retain_vertex = last_inner_neighbor[vertex] > vertex
        after = tuple(frontier[i] for i in retained)
        if retain_vertex:
            after += (vertex,)
        steps.append(FrontierStep(
            vertex, tuple(u for u in adjacency[vertex] if u < 5),
            previous, retained, retain_vertex, frontier, after))
        max_frontier = max(max_frontier, len(frontier), len(after))
        frontier = after
    assert not frontier
    return CompiledGraph(clean, n_vertices, adjacency,
                         tuple(edge for edge in clean if edge[1] < 5),
                         tuple(steps), max_frontier)


def _row_indices(rep_indices: Iterable[int] | None) -> tuple[int, ...]:
    indices = tuple(range(len(REPS))) if rep_indices is None else tuple(rep_indices)
    if any(not isinstance(i, int) or not 0 <= i < len(REPS) for i in indices):
        raise ValueError("Representative index is outside the ten-row frame")
    return tuple(dict.fromkeys(indices))


def _transfer_accepts(graph: CompiledGraph, boundary: tuple[int, ...],
                      state_counts: list[int] | None = None) -> bool:
    if any(boundary[u] == boundary[v] for u, v in graph.boundary_edges):
        return False
    states = {()}
    if state_counts is not None:
        state_counts.append(1)
    for step in graph.steps:
        blocked = {boundary[u] for u in step.boundary_neighbors}
        allowed = tuple(c for c in range(4) if c not in blocked)
        if not allowed:
            if state_counts is not None:
                state_counts.append(0)
            return False
        following = set()
        for state in states:
            old_colors = tuple(state[i] for i in step.previous_positions)
            prefix = tuple(state[i] for i in step.retained_positions)
            for color in allowed:
                if color not in old_colors:
                    following.add(prefix + (color,) if step.retain_vertex else prefix)
        states = following
        if state_counts is not None:
            state_counts.append(len(states))
        if not states:
            return False
    return bool(states)


def sigma_mask(edges: Iterable[Sequence[int]] | CompiledGraph,
               n_vertices: int | None = None, *,
               rep_indices: Iterable[int] | None = None) -> int:
    """Exact Sigma mask, or a selected-row mask in the original bit positions."""
    graph = compile_graph(edges, n_vertices)
    mask = 0
    for index in _row_indices(rep_indices):
        if _transfer_accepts(graph, REPS[index]):
            mask |= 1 << index
    return mask


def transfer_details(edges: Iterable[Sequence[int]] | CompiledGraph,
                     n_vertices: int | None = None) -> dict:
    """Exact mask plus frontier widths and reached-state counts, for auditing."""
    graph = compile_graph(edges, n_vertices)
    rows = {}
    mask = 0
    for index, boundary in enumerate(REPS):
        counts: list[int] = []
        accepted = _transfer_accepts(graph, boundary, counts)
        rows[str(index)] = {"accepted": accepted, "state_counts": counts}
        if accepted:
            mask |= 1 << index
    return {
        "mask": mask, "vertex_order": list(range(5, graph.n_vertices)),
        "max_frontier": graph.max_frontier,
        "frontiers": [list(step.frontier_after) for step in graph.steps],
        "rows": rows,
    }


def find_extension(edges: Iterable[Sequence[int]] | CompiledGraph,
                   rep_index: int, n_vertices: int | None = None) -> Coloring | None:
    """Find the first numeric-order, lexicographic coloring; independent DFS."""
    graph = compile_graph(edges, n_vertices)
    _row_indices((rep_index,))
    colors = list(REPS[rep_index]) + [-1] * (graph.n_vertices - 5)
    if any(colors[u] == colors[v] for u, v in graph.boundary_edges):
        return None
    previous_neighbors = tuple(
        tuple(u for u in graph.adjacency[v] if u < v)
        for v in range(graph.n_vertices))

    def visit(vertex: int) -> bool:
        if vertex == graph.n_vertices:
            return True
        for color in range(4):
            if all(colors[u] != color for u in previous_neighbors[vertex]):
                colors[vertex] = color
                if visit(vertex + 1):
                    return True
        colors[vertex] = -1
        return False

    return tuple(colors) if visit(5) else None


def t4_screen(edges: Iterable[Sequence[int]] | CompiledGraph,
              n_vertices: int | None = None, *, method: str = "dp") -> bool:
    """Require all five named T4 rows, rejecting immediately at the first gap."""
    graph = compile_graph(edges, n_vertices)
    if method not in ("dp", "dfs"):
        raise ValueError("method must be 'dp' or 'dfs'")
    for index in T4_INDICES:
        if method == "dp":
            accepted = _transfer_accepts(graph, REPS[index])
        else:
            accepted = find_extension(graph, index) is not None
        if not accepted:
            return False
    return True


def witness_is_valid(edges: Iterable[Sequence[int]] | CompiledGraph,
                     rep_index: int, colors: Sequence[int],
                     n_vertices: int | None = None) -> bool:
    graph = compile_graph(edges, n_vertices)
    return (0 <= rep_index < len(REPS)
            and len(colors) == graph.n_vertices
            and tuple(colors[:5]) == REPS[rep_index]
            and all(isinstance(c, int) and 0 <= c < 4 for c in colors)
            and all(colors[u] != colors[v] for u, v in graph.edges))


def sigma_mask_with_witnesses(
        edges: Iterable[Sequence[int]] | CompiledGraph,
        n_vertices: int | None = None) -> tuple[int, dict[int, Coloring]]:
    """Compute Sigma by transfer and attach independently found DFS witnesses."""
    graph = compile_graph(edges, n_vertices)
    mask = sigma_mask(graph)
    witnesses = {}
    for index in range(len(REPS)):
        if mask & (1 << index):
            witness = find_extension(graph, index)
            if witness is None or not witness_is_valid(graph, index, witness):
                raise AssertionError("Frontier/DFS disagreement")
            witnesses[index] = witness
    return mask, witnesses


def deletion_profile(
        edges: Iterable[Sequence[int]] | CompiledGraph,
        n_vertices: int | None = None, *, with_witnesses: bool = True,
        include_frame_edges: bool = False,
        edges_to_delete: Iterable[Sequence[int]] | None = None
) -> dict[Edge, tuple[int, dict[int, Coloring]]]:
    """Compute every selected edge deletion on the original named vertex set.

    By default only non-frame edges are deleted. No isolated vertex is dropped,
    and every witness remains in the original vertex/color frame.
    """
    graph = compile_graph(edges, n_vertices)
    if edges_to_delete is None:
        selected = tuple(edge for edge in graph.edges
                         if include_frame_edges or edge not in FRAME_EDGE_SET)
    else:
        selected = _edge_tuple(edges_to_delete)
        if any(edge not in graph.edges for edge in selected):
            raise ValueError("Deletion requested for an absent edge")
    result = {}
    for edge in selected:
        deleted = compile_graph((other for other in graph.edges if other != edge),
                                graph.n_vertices)
        if with_witnesses:
            result[edge] = sigma_mask_with_witnesses(deleted)
        else:
            result[edge] = (sigma_mask(deleted), {})
    return result


def direct_product_sigma(
        edges: Iterable[Sequence[int]] | CompiledGraph,
        n_vertices: int | None = None, *, max_inner: int | None = 8
) -> tuple[int, dict[int, Coloring]]:
    """Third method: test every interior color product, including after success.

    The implementation directly checks full colorings against the edge list.
    It does not use frontier layouts, DFS decisions, or stored coloring results.
    max_inner guards accidental large products; None disables that guard.
    """
    if isinstance(edges, CompiledGraph):
        if n_vertices is not None and n_vertices != edges.n_vertices:
            raise ValueError("n_vertices differs from the compiled graph")
        clean, n_vertices = edges.edges, edges.n_vertices
    else:
        clean = _edge_tuple(edges)
        inferred = max(5, 1 + max((v for edge in clean for v in edge), default=-1))
        if n_vertices is None:
            n_vertices = inferred
        if not isinstance(n_vertices, int) or n_vertices < inferred:
            raise ValueError("n_vertices must include every endpoint and the frame")
    inner_count = n_vertices - 5
    if max_inner is not None and inner_count > max_inner:
        raise ValueError("Direct product exceeds max_inner")
    witnesses: dict[int, Coloring] = {}
    mask = 0
    for index, boundary in enumerate(REPS):
        for interior in product(range(4), repeat=inner_count):
            colors = boundary + interior
            if all(colors[u] != colors[v] for u, v in clean):
                mask |= 1 << index
                if index not in witnesses:
                    witnesses[index] = colors
    return mask, witnesses


def _check_three_methods(edges: Iterable[Sequence[int]], n_vertices: int) -> int:
    graph = compile_graph(edges, n_vertices)
    transfer, witnesses = sigma_mask_with_witnesses(graph)
    direct, direct_witnesses = direct_product_sigma(graph)
    assert transfer == direct, (graph.edges, transfer, direct)
    for index in range(len(REPS)):
        witness = find_extension(graph, index)
        assert bool(transfer & (1 << index)) == (witness is not None)
        if witness is not None:
            assert witness_is_valid(graph, index, witness)
            # Both independent witnesses are the first numeric-order coloring.
            assert witness == direct_witnesses[index] == witnesses[index]
    assert t4_screen(graph) == ((transfer & T4_MASK) == T4_MASK)
    assert t4_screen(graph, method="dfs") == t4_screen(graph)
    assert sigma_mask(graph, rep_indices=SINGLETON_INDICES) == (transfer & ~T4_MASK)
    return transfer


def self_test() -> dict:
    """Exhaust small graph families and exercise deletion/forgetting controls."""
    start = perf_counter()
    assert len(REPS) == 10
    assert set(T4_INDICES).isdisjoint(SINGLETON_INDICES)
    assert set(T4_INDICES) | set(SINGLETON_INDICES) == set(range(10))
    graphs_checked = 0
    deletions_checked = 0
    bare_mask = _check_three_methods(FRAME_EDGES, 5)
    assert bare_mask == ALL_ROWS_MASK
    graphs_checked += 1
    # Every boundary attachment set for one interior vertex.
    for bits in range(32):
        edges = FRAME_EDGES + tuple((u, 5) for u in range(5) if bits & (1 << u))
        _check_three_methods(edges, 6)
        graphs_checked += 1
    # Every two-vertex attachment set, with and without the original inner edge.
    for bits in range(1024):
        attachments = tuple((u, 5 + j) for j in range(2) for u in range(5)
                            if bits & (1 << (5 * j + u)))
        for adjacent in (False, True):
            edges = FRAME_EDGES + attachments + (((5, 6),) if adjacent else ())
            _check_three_methods(edges, 7)
            graphs_checked += 1
    # Wheel control, computed from the actual number of boundary colors.
    wheel = FRAME_EDGES + tuple((u, 5) for u in range(5))
    wheel_mask = sigma_mask(wheel, 6)
    assert wheel_mask == sum(1 << i for i, rep in enumerate(REPS)
                             if len(set(rep)) == 3)
    # A K5 interior has no four-coloring; no planar theorem is consulted.
    inner_k5 = FRAME_EDGES + tuple(combinations(range(5, 10), 2))
    assert sigma_mask(inner_k5, 10) == 0
    assert direct_product_sigma(inner_k5, 10)[0] == 0
    graphs_checked += 2
    # Fixed random controls reach wider/nonmonotone frontiers and isolated nodes.
    rng = random.Random(0xC5E2)
    for n_vertices in range(8, 12):
        optional = [(u, v) for u, v in combinations(range(n_vertices), 2)
                    if v >= 5]
        for sample in range(12):
            edges = FRAME_EDGES + tuple(edge for edge in optional
                                       if rng.random() < (0.18 + 0.045 * sample))
            mask = _check_three_methods(edges, n_vertices)
            graphs_checked += 1
            if sample < 3:
                profile = deletion_profile(edges, n_vertices,
                                           include_frame_edges=True)
                for edge, (deleted_mask, witnesses) in profile.items():
                    deleted_edges = tuple(e for e in edges if e != edge)
                    direct_mask, _ = direct_product_sigma(deleted_edges, n_vertices)
                    assert deleted_mask == direct_mask
                    assert (deleted_mask & mask) == mask
                    for index, witness in witnesses.items():
                        assert witness_is_valid(deleted_edges, index, witness,
                                                n_vertices)
                    deletions_checked += 1
    return {
        "status": "passed", "graphs_checked": graphs_checked,
        "edge_deletions_checked": deletions_checked,
        "methods": ["explicit_frontier_transfer", "fixed_order_dfs",
                    "full_interior_cartesian_product"],
        "vertex_order": "numeric labels; no degree sorting",
        "seconds": round(perf_counter() - start, 6),
    }


def benchmark() -> list[dict]:
    """Small synthetic timing data, without any source catalogue."""
    records = []
    for inner_count in (4, 7, 9):
        vertices = tuple(range(5, 5 + inner_count))
        path_edges = tuple(zip(vertices, vertices[1:]))
        families = {
            "path": FRAME_EDGES + path_edges
                    + tuple((i % 5, vertex) for i, vertex in enumerate(vertices)),
            "ladder": FRAME_EDGES + path_edges
                    + tuple((vertices[i], vertices[i + 2])
                            for i in range(inner_count - 2))
                    + tuple((i % 5, vertex) for i, vertex in enumerate(vertices)),
            "star": FRAME_EDGES
                    + tuple((vertices[0], vertex) for vertex in vertices[1:])
                    + tuple((i % 5, vertex) for i, vertex in enumerate(vertices)),
        }
        for name, edges in families.items():
            graph = compile_graph(edges, 5 + inner_count)
            repetitions = 150
            start = perf_counter()
            for _ in range(repetitions):
                mask = sigma_mask(graph)
            elapsed = perf_counter() - start
            start = perf_counter()
            for _ in range(repetitions):
                accepted_t4 = t4_screen(graph)
            screen_elapsed = perf_counter() - start
            records.append({
                "family": name, "inner_vertices": inner_count,
                "edges": len(graph.edges), "max_frontier": graph.max_frontier,
                "mask": mask, "t4": accepted_t4,
                "sigma_microseconds": round(elapsed * 1e6 / repetitions, 3),
                "t4_microseconds": round(screen_elapsed * 1e6 / repetitions, 3),
            })
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--check", action="store_true",
                        help="Replay saved ER controls and source fingerprints byte for byte")
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--edges-json", type=Path)
    parser.add_argument("--n-vertices", type=int)
    parser.add_argument("--delete-edges", action="store_true")
    parser.add_argument("--direct-product", action="store_true")
    args = parser.parse_args()
    if args.check:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/c5_excess_two_independent_search.py"),
             "--controls-only", "--check"],
            check=False,
        ).returncode
    result = {}
    if args.self_test or not (args.edges_json or args.benchmark):
        result["self_test"] = self_test()
    if args.benchmark:
        result["benchmark"] = benchmark()
    if args.edges_json:
        payload = json.loads(args.edges_json.read_text())
        edges = payload["edges"] if isinstance(payload, dict) else payload
        n_vertices = args.n_vertices
        if n_vertices is None and isinstance(payload, dict):
            n_vertices = payload.get("n_vertices")
        graph = compile_graph(edges, n_vertices)
        mask, witnesses = sigma_mask_with_witnesses(graph)
        result["graph"] = {
            "n_vertices": graph.n_vertices, "edges": graph.edges,
            "mask": mask, "witnesses": witnesses,
            "transfer": transfer_details(graph),
        }
        if args.delete_edges:
            result["deletions"] = [
                {"edge": edge, "mask": deleted_mask, "witnesses": deleted_witnesses}
                for edge, (deleted_mask, deleted_witnesses) in
                deletion_profile(graph).items()
            ]
        if args.direct_product:
            direct_mask, direct_witnesses = direct_product_sigma(graph)
            result["direct_product"] = {
                "mask": direct_mask, "witnesses": direct_witnesses,
                "agrees_with_transfer": direct_mask == mask,
            }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
