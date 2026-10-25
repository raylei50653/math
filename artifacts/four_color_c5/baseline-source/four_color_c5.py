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
    """Find a safe bounded subset of induced C5s using chordless path growth.

    Canonical order is relative to the input vertex list: start at its earliest
    vertex, and choose the orientation with earlier second than last vertex.
    A step is one inspected neighbour during path growth.  Hitting either cap
    conservatively reports ``complete=False``; this is discovery truncation,
    never a conclusion about colourability.
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
    neighbors = [sorted(adjacent) for adjacent in adjacency]
    cycles = []
    steps = 0

    class Truncated(Exception):
        pass

    def tick():
        nonlocal steps
        if steps >= max_steps:
            raise Truncated
        steps += 1

    def visit(path):
        start = path[0]
        for candidate in neighbors[path[-1]]:
            tick()
            if candidate <= start or candidate in path:
                continue
            if len(path) == 4:
                if candidate not in adjacency[start] or path[1] >= candidate:
                    continue
                if any(candidate in adjacency[earlier] for earlier in path[1:-1]):
                    continue
                cycles.append(tuple(vertices[v] for v in path + [candidate]))
                if len(cycles) >= max_cycles:
                    raise Truncated
            else:
                if any(candidate in adjacency[earlier] for earlier in path[:-1]):
                    continue
                visit(path + [candidate])

    complete = True
    try:
        if len(vertices) >= 5:
            if max_cycles == 0:
                raise Truncated
            for start in range(len(vertices)):
                for first in neighbors[start]:
                    tick()
                    if first > start:
                        visit([start, first])
    except Truncated:
        complete = False
    return dict(cycles=cycles, steps=steps, complete=complete,
                truncated=not complete, max_cycles=max_cycles, max_steps=max_steps)
