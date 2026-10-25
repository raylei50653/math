"""Literal-frame C5 relation and a bounded induced-cycle discovery helper.

The 240 rows retain the five ordered positions and all four literal colours.
Equality-pattern normalization is catalogue metadata only; indexed queries
never rotate a cycle or rename colours independently of the supplied frame.
"""

from __future__ import annotations

from itertools import product


C5_EDGES = ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4))
C5_ROWS = tuple(row for row in product(range(4), repeat=5)
                if all(row[a] != row[b] for a, b in C5_EDGES))
C5_ALL_ROWS = (1 << len(C5_ROWS)) - 1
C5_POSITION_COLOR_MASKS = tuple(
    tuple(sum(1 << i for i, row in enumerate(C5_ROWS) if row[position] == color)
          for color in range(4))
    for position in range(5)
)
C5_DOMAIN_MASKS = tuple(
    tuple(sum(C5_POSITION_COLOR_MASKS[position][color]
              for color in range(4) if domain & (1 << color))
          for domain in range(16))
    for position in range(5)
)


def query_c5(domain_masks, *, charge=None):
    """Return the exact compatible-row bitset and five literal support masks.

    At most 26 indexed operations are used: five domain intersections, twenty
    colour-support intersections, and one row bit count.  An optional ``charge``
    callback runs *before* each operation, allowing callers to stop safely on a
    work limit without committing partial support projections.
    """
    if (not isinstance(domain_masks, (tuple, list)) or len(domain_masks) != 5
            or any(type(mask) is not int or not 0 <= mask < 16 for mask in domain_masks)):
        raise ValueError("domain_masks must contain five integer masks in 0..15")
    operations = 0

    def tick():
        nonlocal operations
        if charge is not None:
            charge()
        operations += 1

    allowed = C5_ALL_ROWS
    for position, mask in enumerate(domain_masks):
        tick()
        allowed &= C5_DOMAIN_MASKS[position][mask]
    supports = []
    for position in range(5):
        support = 0
        for color in range(4):
            tick()
            if allowed & C5_POSITION_COLOR_MASKS[position][color]:
                support |= 1 << color
        supports.append(support)
    tick()
    row_count = allowed.bit_count()
    return dict(allowed_bits=allowed, supports=supports,
                row_count=row_count, op_count=operations)


def c5_catalogue():
    """Export full literal rows and their ten colour-equality pattern classes."""
    classes = {}
    for row_index, row in enumerate(C5_ROWS):
        labels = {}
        pattern = tuple(labels.setdefault(color, len(labels)) for color in row)
        classes.setdefault(pattern, []).append(row_index)
    return {
        "name": "c5", "version": "literal-c5-index-v1", "palette": list(range(4)),
        "scope": list(range(5)), "edges": [list(edge) for edge in C5_EDGES],
        "rows": [list(row) for row in C5_ROWS],
        "row_count": len(C5_ROWS), "index_order": "lexicographic literal colour tuples",
        "normalized_equality_patterns": [list(pattern) for pattern in sorted(classes)],
        "pattern_classes": [dict(pattern=list(pattern), row_count=len(indices), row_indices=indices)
                            for pattern, indices in sorted(classes.items())],
        "pattern_note": "Equality-pattern classes describe the full table; queries preserve the supplied ordered positions and literal colours.",
    }


def find_induced_c5(graph, max_cycles=128, max_steps=200000):
    """Find induced C5s by joining an induced path to common neighbours.

    Canonical order is relative to the input vertex list: start at its earliest
    vertex, and choose the orientation with earlier second than last vertex.
    Adjacency bitsets filter chords before extending s-a-b-c.  Its last vertex
    is in N(s) & N(c), outside N(a) | N(b), and later than a.  This preserves
    the old DFS cycle order while avoiding scans over impossible neighbours.

    A step is one selected candidate extension, including a closing vertex.
    Setup and bitset filtering are not separately charged.  Hitting either cap
    conservatively reports ``complete=False``; this is discovery truncation,
    never a conclusion about colourability.
    """
    from four_color_lab import normalize_graph

    g = normalize_graph(graph)
    if any(type(value) is not int or value < 0 for value in (max_cycles, max_steps)):
        raise ValueError("cycle and scan limits must be nonnegative integers")
    vertices = g["vertices"]
    index = {vertex: position for position, vertex in enumerate(vertices)}
    adjacency = [0 for _ in vertices]
    for a, b in g["edges"]:
        adjacency[index[a]] |= 1 << index[b]
        adjacency[index[b]] |= 1 << index[a]
    cycles = []
    steps = 0

    class Truncated(Exception):
        pass

    def tick():
        nonlocal steps
        if steps >= max_steps:
            raise Truncated
        steps += 1

    complete = True
    try:
        if len(vertices) >= 5:
            if max_cycles == 0:
                raise Truncated
            for start in range(len(vertices)):
                start_neighbors = adjacency[start]
                after_start = ~((1 << (start + 1)) - 1)
                firsts = start_neighbors & after_start
                while firsts:
                    tick()
                    bit = firsts & -firsts
                    firsts ^= bit
                    first = bit.bit_length() - 1
                    first_neighbors = adjacency[first]
                    after_first = ~((1 << (first + 1)) - 1)
                    seconds = first_neighbors & after_start & ~start_neighbors
                    while seconds:
                        tick()
                        bit = seconds & -seconds
                        seconds ^= bit
                        second = bit.bit_length() - 1
                        second_neighbors = adjacency[second]
                        thirds = second_neighbors & after_start & ~(start_neighbors | first_neighbors)
                        while thirds:
                            tick()
                            bit = thirds & -thirds
                            thirds ^= bit
                            third = bit.bit_length() - 1
                            lasts = (start_neighbors & adjacency[third] & after_first
                                     & ~(first_neighbors | second_neighbors))
                            while lasts:
                                tick()
                                bit = lasts & -lasts
                                lasts ^= bit
                                last = bit.bit_length() - 1
                                cycles.append(tuple(vertices[v] for v in (start, first, second, third, last)))
                                if len(cycles) >= max_cycles:
                                    raise Truncated
    except Truncated:
        complete = False
    return dict(cycles=cycles, steps=steps, complete=complete,
                truncated=not complete, max_cycles=max_cycles, max_steps=max_steps,
                algorithm="bitset-induced-path-join-v1",
                step_unit="selected candidate extension; setup and bitset filtering uncharged")


def find_local_c5(graph, max_cycles=128, max_steps=200000):
    """Scan each vertex once for an induced C5 on its five neighbours.

    This deliberately selects only a local subset of cycles. ``complete``
    therefore never claims global cycle coverage; ``local_scan_complete``
    reports whether every centre was inspected.  One step inspects one centre,
    including ineligible degrees.  Graph preparation is outside that budget.
    Ring traversal follows actual edges and needs no geometric embedding.
    """
    from four_color_lab import normalize_graph

    g = normalize_graph(graph)
    if any(type(value) is not int or value < 0 for value in (max_cycles, max_steps)):
        raise ValueError("cycle and scan limits must be nonnegative integers")
    vertices = g["vertices"]
    index = {vertex: position for position, vertex in enumerate(vertices)}
    adjacency = [set() for _ in vertices]
    for a, b in g["edges"]:
        adjacency[index[a]].add(index[b])
        adjacency[index[b]].add(index[a])
    cycles, centers, seen = [], [], {}
    steps, eligible = 0, 0
    truncated = False
    for center, neighbors in enumerate(adjacency):
        if steps >= max_steps or len(cycles) >= max_cycles:
            truncated = True
            break
        steps += 1
        if len(neighbors) != 5:
            continue
        eligible += 1
        ring_neighbors = {v: adjacency[v] & neighbors for v in neighbors}
        if any(len(adjacent) != 2 for adjacent in ring_neighbors.values()):
            continue
        start = min(neighbors)
        cycle = [start]
        previous, current = start, min(ring_neighbors[start])
        while current != start and len(cycle) < 5:
            cycle.append(current)
            following = next(v for v in ring_neighbors[current] if v != previous)
            previous, current = current, following
        if current != start or len(cycle) != 5 or len(set(cycle)) != 5:
            continue
        key = tuple(cycle)
        if key in seen:
            centers[seen[key]].append(vertices[center])
        else:
            seen[key] = len(cycles)
            cycles.append(tuple(vertices[v] for v in cycle))
            centers.append([vertices[center]])
        if len(cycles) >= max_cycles:
            truncated = True
            break
    return dict(cycles=cycles, centers=centers, steps=steps, eligible_centers=eligible,
                complete=False, local_scan_complete=not truncated, truncated=truncated,
                max_cycles=max_cycles, max_steps=max_steps,
                coverage="degree-five-neighbor-rings",
                algorithm="degree-five-neighbor-ring-v1",
                step_unit="one inspected center; graph preparation uncharged")
