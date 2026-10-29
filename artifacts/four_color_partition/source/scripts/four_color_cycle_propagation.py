"""Bounded discovery of original cycles for optional redundant propagation.

The finder reads only actual vertices, edges, and the supplied current domains.
It does not read graph-family metadata or assume a geometric embedding.  Every
returned cycle is simple and every consecutive pair, including its closing
edge, is checked against the original graph.

Discovery is deliberately incomplete: each selected induced subgraph contributes
fundamental cycles of a deterministic spanning forest, rather than every simple
cycle.  Domain-pair subgraphs run first so that a long two-colour rim is not
hidden by many short cycles through unrestricted or fixed-colour hubs.  A cap
only omits optional propagators; original edge constraints must remain active.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations


def find_original_cycles(graph, domain_masks, *, max_cycles=128,
                         max_scan_steps=200000, charge=None):
    """Return canonical original cycles found within a bounded forest scan.

    ``domain_masks`` is aligned with the supplied vertex order and contains
    exact integers from 0 through 15.  For each two-colour palette, then each
    three-colour palette, scan the subgraph induced by vertices with a nonempty
    domain contained in that palette.  Finally scan the full original graph.
    Identical induced vertex sets need only one forest scan.  Call again after
    domains change if newly useful domain-induced cycles are wanted.

    Each cycle starts at its earliest input vertex and uses the lexicographically
    smaller orientation in input-position order.  Returned cycles are sorted in
    that order; vertex identities themselves need not be numerically ordered.

    A scan step is charged *before* an eligibility/root/dequeue/edge candidate,
    a tree-path position, or a canonicalization/verification position.  Graph
    validation and adjacency preparation are outside the discovery budget.
    Optional ``charge()`` is called before every such step; its exceptions
    propagate unchanged, without mutating the graph or supplied domains.

    ``complete`` means the prescribed contexts were fully scanned, never that
    all cycles were found.  ``all_cycles_complete`` is always false.  Either
    zero cap, reaching the cycle cap, or needing another step beyond the scan
    budget conservatively sets ``truncated=True``.
    """
    from four_color_lab import normalize_graph

    g = normalize_graph(graph)
    if any(type(value) is not int or value < 0
           for value in (max_cycles, max_scan_steps)):
        raise ValueError("cycle and scan limits must be nonnegative integers")
    if (not isinstance(domain_masks, (list, tuple))
            or len(domain_masks) != len(g["vertices"])
            or any(type(mask) is not int or not 0 <= mask <= 15
                   for mask in domain_masks)):
        raise ValueError("domain masks must be integers 0..15 aligned with vertices")
    if charge is not None and not callable(charge):
        raise ValueError("charge must be callable or None")

    vertices = g["vertices"]
    masks = tuple(domain_masks)
    palettes = [sum(1 << colour for colour in colours)
                for size in (2, 3)
                for colours in combinations(range(4), size)]
    contexts_total = len(palettes) + 1
    steps = 0
    found = set()
    contexts = []
    contexts_completed = 0
    unique_subgraphs_scanned = 0

    def result(complete):
        return dict(
            cycles=[tuple(vertices[position] for position in cycle)
                    for cycle in sorted(found)],
            scan_steps=steps, steps=steps, complete=complete,
            truncated=not complete, all_cycles_complete=False,
            max_cycles=max_cycles, max_scan_steps=max_scan_steps,
            coverage=("bounded fundamental cycles of original graph and "
                      "domain-induced subgraphs; not all cycles"),
            algorithm="domain-induced-bfs-fundamental-cycles-v1",
            step_unit=("one eligibility/root/dequeue/edge candidate, tree-path "
                       "position, or canonicalization/verification position; "
                       "graph preparation uncharged"),
            contexts_total=contexts_total,
            contexts_completed=contexts_completed,
            unique_subgraphs_scanned=unique_subgraphs_scanned,
            contexts=contexts,
        )

    if max_cycles == 0 or max_scan_steps == 0:
        return result(False)

    index = {vertex: position for position, vertex in enumerate(vertices)}
    adjacency_sets = [set() for _ in vertices]
    for a, b in g["edges"]:
        a, b = index[a], index[b]
        adjacency_sets[a].add(b)
        adjacency_sets[b].add(a)
    adjacency = [tuple(sorted(neighbours)) for neighbours in adjacency_sets]

    class ScanLimit(Exception):
        pass

    def tick():
        nonlocal steps
        if steps >= max_scan_steps:
            raise ScanLimit
        if charge is not None:
            charge()
        steps += 1

    def canonical_cycle(path):
        """Verify original edges, then orient by original vertex positions."""
        if len(path) < 3 or len(set(path)) != len(path):
            raise AssertionError("forest produced a non-simple cycle")
        minimum_position = 0
        for position, vertex in enumerate(path):
            tick()
            if path[(position + 1) % len(path)] not in adjacency_sets[vertex]:
                raise AssertionError("forest produced a non-original cycle edge")
            if vertex < path[minimum_position]:
                minimum_position = position
        forward, backward = [], []
        for offset in range(len(path)):
            tick()
            forward.append(path[(minimum_position + offset) % len(path)])
            backward.append(path[(minimum_position - offset) % len(path)])
        return min(tuple(forward), tuple(backward))

    def fundamental_cycle(a, b, parent, depth):
        """The unique tree path from a to b, closed by the non-tree edge."""
        left, right = [], []
        while depth[a] > depth[b]:
            tick()
            left.append(a)
            a = parent[a]
        while depth[b] > depth[a]:
            tick()
            right.append(b)
            b = parent[b]
        while a != b:
            tick()
            left.append(a)
            a = parent[a]
            tick()
            right.append(b)
            b = parent[b]
        tick()
        left.append(a)
        return canonical_cycle(left + list(reversed(right)))

    seen_subgraphs = {}
    try:
        for palette in [*palettes, None]:
            selected = []
            for vertex, mask in enumerate(masks):
                tick()
                if palette is None or (mask and mask & ~palette == 0):
                    selected.append(vertex)
            selected = tuple(selected)
            context = dict(palette_mask=palette, vertex_count=len(selected),
                           complete=False, new_cycles=0)
            contexts.append(context)
            if selected in seen_subgraphs:
                context["duplicate_of"] = seen_subgraphs[selected]
                context["complete"] = True
                contexts_completed += 1
                continue
            seen_subgraphs[selected] = len(contexts) - 1
            unique_subgraphs_scanned += 1
            allowed = set(selected)
            parent = [-1] * len(vertices)
            depth = [0] * len(vertices)
            for root in selected:
                tick()
                if parent[root] != -1:
                    continue
                parent[root] = root
                queue = deque([root])
                while queue:
                    tick()
                    vertex = queue.popleft()
                    for neighbour in adjacency[vertex]:
                        tick()
                        if neighbour not in allowed:
                            continue
                        if parent[neighbour] == -1:
                            parent[neighbour] = vertex
                            depth[neighbour] = depth[vertex] + 1
                            queue.append(neighbour)
                        elif (vertex < neighbour
                              and parent[vertex] != neighbour
                              and parent[neighbour] != vertex):
                            cycle = fundamental_cycle(vertex, neighbour, parent, depth)
                            if cycle not in found:
                                found.add(cycle)
                                context["new_cycles"] += 1
                                if len(found) >= max_cycles:
                                    raise ScanLimit
            context["complete"] = True
            contexts_completed += 1
    except ScanLimit:
        return result(False)
    return result(True)
