#!/usr/bin/env python3
"""Independent C6 necessary Kempe rules and actual disk controls.

No imports from the reconstruction producer. Boundary vertex order is 0,...,5;
colour orbits identify palette permutations only, never boundary permutations.
The rules use all set partitions represented as restricted-growth words and
the alternating-four-indices criterion for noncrossing.
"""

import hashlib
import itertools
import json


def canonical(word):
    labels = {}
    return tuple(labels.setdefault(value, len(labels)) for value in word)


rows = tuple(sorted({
    canonical(word)
    for word in itertools.product(range(4), repeat=6)
    if all(word[i] != word[(i + 1) % 6] for i in range(6))
}))
assert len(rows) == 31
ROW_INDEX = {row: i for i, row in enumerate(rows)}
SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
UNIVERSE = (1 << len(rows)) - 1


def _partition_words(prefix=(0,)):
    if len(prefix) == 6:
        yield prefix
        return
    for value in range(max(prefix) + 2):
        yield from _partition_words(prefix + (value,))


def _noncrossing(word):
    return not any(
        word[a] == word[c] and word[b] == word[d] and word[a] != word[b]
        for a, b, c, d in itertools.combinations(range(6), 4)
    )


PARTITIONS = tuple(word for word in _partition_words() if _noncrossing(word))
assert len(PARTITIONS) == 132


def _rules_for(row, split):
    group = {colour: i for i, pair in enumerate(split) for colour in pair}
    swap = {pair[i]: pair[1 - i] for pair in split for i in (0, 1)}
    result = set()
    for partition in PARTITIONS:
        if any(
            partition[i] == partition[j] and group[row[i]] != group[row[j]]
            for i, j in itertools.combinations(range(6), 2)
        ):
            continue
        if any(
            group[row[i]] == group[row[(i + 1) % 6]]
            and partition[i] != partition[(i + 1) % 6]
            for i in range(6)
        ):
            continue
        orbit_mask = 0
        for selected in range(1 << (max(partition) + 1)):
            switched = tuple(
                swap[colour] if selected & (1 << partition[i]) else colour
                for i, colour in enumerate(row)
            )
            orbit_mask |= 1 << ROW_INDEX[canonical(switched)]
        result.add(orbit_mask)
    assert result
    assert all(mask & (1 << ROW_INDEX[row]) for mask in result)
    return tuple(sorted(result))


rules = tuple(tuple(_rules_for(row, split) for split in SPLITS) for row in rows)


def kappa(support):
    """Simultaneous deletion to the greatest fixed point contained in support."""
    if not isinstance(support, int) or support < 0 or support & ~UNIVERSE:
        raise ValueError("support must be a nonnegative 31-bit integer")
    while True:
        next_support = support
        for i, split_rules in enumerate(rules):
            if support & (1 << i) and any(
                not any(orbit & support == orbit for orbit in alternatives)
                for alternatives in split_rules
            ):
                next_support &= ~(1 << i)
        if next_support == support:
            return support
        support = next_support


def _edges(*groups):
    return tuple(sorted({tuple(sorted(edge)) for group in groups for edge in group}))


RIM = tuple((i, (i + 1) % 6) for i in range(6))
FAN = ((0, 2), (0, 3), (0, 4))
CONTROLS = (
    ("cycle", 6, _edges(RIM), "Six-cycle bounds an empty disk."),
    ("wheel", 7, _edges(RIM, ((6, i) for i in range(6))),
     "One interior point joined to the entire rim."),
    ("fan_triangulation", 6, _edges(RIM, FAN),
     "Three polygon diagonals from boundary vertex 0."),
    ("zigzag_triangulation", 6, _edges(RIM, ((0, 2), (2, 5), (3, 5))),
     "Noncrossing diagonals 02,25,35 triangulate the hexagon."),
    ("short_chord", 6, _edges(RIM, ((0, 2),)),
     "One polygon diagonal 02."),
    ("opposite_chord", 6, _edges(RIM, ((0, 3),)),
     "One polygon diagonal 03."),
    ("stacked_fan", 7, _edges(RIM, FAN, ((6, 0), (6, 1), (6, 2))),
     "Insert vertex 6 into face 012 of the fan and join its three corners."),
)


def actual_support(vertex_count, edges):
    """Exhaust all literal colourings with boundary vertex 0 fixed to colour 0."""
    adjacent = [set() for _ in range(vertex_count)]
    for u, v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    order = (0,) + tuple(sorted(range(1, vertex_count), key=lambda v: (-len(adjacent[v]), v)))
    colours = [-1] * vertex_count
    colours[0] = 0
    result = 0
    count = 0

    def visit(position):
        nonlocal result, count
        if position == vertex_count:
            result |= 1 << ROW_INDEX[canonical(colours[:6])]
            count += 1
            return
        vertex = order[position]
        forbidden = {colours[w] for w in adjacent[vertex]}
        for colour in range(4):
            if colour not in forbidden:
                colours[vertex] = colour
                visit(position + 1)
        colours[vertex] = -1

    visit(1)
    return result, count * 4


def control_report():
    cases = []
    for name, vertex_count, edges, embedding in CONTROLS:
        support, literal_count = actual_support(vertex_count, edges)
        pruned = kappa(support)
        cases.append({
            "name": name,
            "vertex_count": vertex_count,
            "edges": edges,
            "disk_construction": embedding,
            "literal_colouring_count": literal_count,
            "support_mask": support,
            "support_size": support.bit_count(),
            "kappa_mask": pruned,
            "pass": support == pruned,
        })
    rule_bytes = json.dumps(rules, separators=(",", ":")).encode("ascii")
    return {
        "status": "PASS" if all(case["pass"] for case in cases) else "FAIL",
        "scope": "Independent necessary-rule reconstruction and seven actual disk controls only",
        "row_count": len(rows),
        "rows": rows,
        "split_order": SPLITS,
        "noncrossing_partition_count": len(PARTITIONS),
        "rules_sha256": hashlib.sha256(rule_bytes).hexdigest(),
        "empty_support_fixed": kappa(0) == 0,
        "universe_fixed": kappa(UNIVERSE) == UNIVERSE,
        "cases": cases,
    }


if __name__ == "__main__":
    report = control_report()
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(0 if report["status"] == "PASS" else 1)
