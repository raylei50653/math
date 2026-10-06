#!/usr/bin/env python3
"""Independent exhaustive reference for C44 minimal rejected-row cores.

Definitions are taken from docs/c5_independent_support_capacity.md section 1
and docs/c5_qcore_shield_budget.md section 1: retain the ordered frame
B=(0,1,2,3,4), all five frame edges, and the literal boundary row
c5_kempe_screen.REPS[row_index].  A q-core is any subgraph rejecting that row;
an inclusion-minimal q-core has no proper rejecting edge subgraph.  Isolated
private vertices do not distinguish cores.  Original private labels, including
the original roots, are never changed.  This reference computes edge sets; it
does not infer the roots or their degrees.

For m nonframe edges, visit each of the 2**m edge subsets exactly once, in
binary-reflected Gray order.  The optional degree filter discards a subset
having a private vertex of degree 1, 2, or 3.  This filter cannot discard a
minimal rejection: if M-v had a q-colouring, one of four colours could be
assigned to such a vertex v, contradicting rejection.  Thus M-v still rejects
and M was not minimal.  Degree zero is permitted and ignored.  This is the
elementary recolouring proof of W1 in c5_qcore_shield_budget.md section 2.2;
no planarity, T4, Sigma-criticality, or four-colour theorem is needed.

Every degree-valid subset is tested, separately for each requested row, by
ordinary fixed-numeric-order four-colour DFS.  No rejection monotonicity is
used to skip subsets or colouring decisions.  After all subsets have been
tested, exact containment checks select the minimal rejecting edge sets.
This is sufficient even with the degree filter: every rejecting proper
subgraph contains an inclusion-minimal rejection, which passes that filter.
The ``degree_filter=False`` option tests all subsets without that lemma.

Independence boundary: this module imports only REPS, not the ES/E4c core
algorithms or C44 optimized recursion.  During document reading the author
also saw ES section 2 (including its general colouring and criticality
explanation), beyond the requested ES section 1.  No ES implementation was
read or imported.  The colouring decisions here are ordinary DFS, and no
one-pass deletion/criticality calculation is shared with the optimized code.
"""

from __future__ import annotations

from collections.abc import Iterable, MutableMapping
from typing import TypeAlias

from c5_kempe_screen import REPS


Edge: TypeAlias = tuple[int, int]
Core: TypeAlias = tuple[Edge, ...]
FRAME: Core = ((0, 1), (0, 4), (1, 2), (2, 3), (3, 4))


def _prepare(k: int, edges: Iterable[Iterable[int]]) -> tuple[Core, Core]:
    if not isinstance(k, int) or isinstance(k, bool) or k < 0:
        raise ValueError("k must be a nonnegative integer")
    normalized: list[Edge] = []
    for edge in edges:
        endpoints = tuple(edge)
        if len(endpoints) != 2:
            raise ValueError("an edge must have exactly two endpoints")
        u, v = endpoints
        if any(not isinstance(x, int) or isinstance(x, bool) for x in (u, v)):
            raise ValueError("endpoints must be integers")
        if u == v or min(u, v) < 0 or max(u, v) >= 5 + k:
            raise ValueError("graph must be simple with vertices 0 through 4+k")
        normalized.append((min(u, v), max(u, v)))
    if len(set(normalized)) != len(normalized):
        raise ValueError("duplicate edge")
    full = tuple(sorted(normalized))
    frame = tuple(edge for edge in full if edge[1] < 5)
    if frame != FRAME:
        raise ValueError("graph must retain exactly the five induced-C5 frame edges")
    return full, tuple(edge for edge in full if edge[1] >= 5)


def _candidate_masks(k: int, nonframe: Core, degree_filter: bool):
    """Yield all masks, or the degree-valid ones; always visit every subset."""
    m = len(nonframe)
    if not degree_filter:
        yield from range(1 << m)
        return
    private_endpoints = tuple(
        tuple(v - 5 for v in edge if v >= 5) for edge in nonframe
    )
    degrees = [0] * k
    mask = 0
    bad = 0
    yield mask
    for ordinal in range(1, 1 << m):
        bit = ordinal & -ordinal
        index = bit.bit_length() - 1
        mask ^= bit
        delta = 1 if mask & bit else -1
        for vertex in private_endpoints[index]:
            old = degrees[vertex]
            new = old + delta
            bad += (1 <= new <= 3) - (1 <= old <= 3)
            degrees[vertex] = new
        if bad == 0:
            yield mask


def _accepts(k: int, earlier: tuple[tuple[int, ...], ...], row_index: int) -> bool:
    """Direct DFS on private vertices 5,6,... with four literal colours."""
    colours = list(REPS[row_index]) + [-1] * k

    def visit(index: int) -> bool:
        if index == k:
            return True
        vertex = 5 + index
        forbidden = {colours[u] for u in earlier[index]}
        for colour in range(4):
            if colour not in forbidden:
                colours[vertex] = colour
                if visit(index + 1):
                    return True
        colours[vertex] = -1
        return False

    return visit(0)


def brute_all_rows(
    k: int,
    edges: Iterable[Iterable[int]],
    row_indices: Iterable[int],
    *,
    degree_filter: bool = True,
    stats: MutableMapping[str, int] | None = None,
) -> dict[int, list[Core]]:
    """Return every minimal core, with frame edges and original vertex labels.

    Row keys and core edge tuples are sorted.  The optional ``stats`` mapping
    receives deterministic counts for this graph call.  It is cleared first.
    This routine is practical for the C44 k<=6 reference, not a large-k search.
    """
    _, nonframe = _prepare(k, edges)
    rows = tuple(sorted(set(row_indices)))
    if any(not isinstance(row, int) or isinstance(row, bool)
           or not 0 <= row < len(REPS) for row in rows):
        raise ValueError("row index must refer to the fixed REPS order")
    rejected: dict[int, list[int]] = {row: [] for row in rows}
    candidates = 0
    for mask in _candidate_masks(k, nonframe, degree_filter):
        candidates += 1
        backward: list[list[int]] = [[] for _ in range(k)]
        bits = mask
        while bits:
            bit = bits & -bits
            u, v = nonframe[bit.bit_length() - 1]
            backward[v - 5].append(u)
            bits ^= bit
        earlier = tuple(tuple(neighbours) for neighbours in backward)
        for row in rows:
            if not _accepts(k, earlier, row):
                rejected[row].append(mask)

    result: dict[int, list[Core]] = {}
    for row in rows:
        minimal: list[int] = []
        for mask in sorted(rejected[row], key=lambda value: (value.bit_count(), value)):
            if not any(core & mask == core for core in minimal):
                minimal.append(mask)
        result[row] = sorted(
            tuple(sorted(FRAME + tuple(edge for i, edge in enumerate(nonframe)
                                      if mask & (1 << i))))
            for mask in minimal
        )
    if stats is not None:
        stats.clear()
        stats.update(
            nonframe_edges=len(nonframe),
            subsets_visited=1 << len(nonframe),
            degree_valid_subsets=candidates,
            dfs_calls=candidates * len(rows),
            rejecting_degree_valid_subsets=sum(map(len, rejected.values())),
            minimal_cores=sum(map(len, result.values())),
        )
    return result


def brute_cores(
    k: int,
    edges: Iterable[Iterable[int]],
    row_index: int,
    *,
    degree_filter: bool = True,
    stats: MutableMapping[str, int] | None = None,
) -> list[Core]:
    """Convenience wrapper for one literal rejection row."""
    return brute_all_rows(k, edges, (row_index,), degree_filter=degree_filter,
                          stats=stats)[row_index]
