"""Exact semijoin on a shared, ordered interface in one literal colour frame.

Rows keep their private coordinates.  Projection is used only to find common
support, never to reconstruct a full row by mixing independent coordinates.
The optional callback charges each projected row and membership test before
performing it.  No input is mutated, including when the callback interrupts.
"""

from __future__ import annotations


def intersect_on_shared(left_scope, left_rows, right_scope, right_rows, *, charge=None):
    """Filter two valid finite relations by their complete shared tuple.

Scopes contain distinct variable identities and rows align with those scopes.
The shared scope follows the left scope's order, even when the right scope
lists the same variables differently.  Empty relations remain contradictions;
two nonempty disjoint relations share the single empty tuple.
"""
    right_offsets = {vertex: offset for offset, vertex in enumerate(right_scope)}
    shared = tuple(vertex for vertex in left_scope if vertex in right_offsets)
    left_offsets = tuple(offset for offset, vertex in enumerate(left_scope)
                         if vertex in right_offsets)
    right_positions = tuple(right_offsets[vertex] for vertex in shared)

    def tick():
        if charge is not None:
            charge()

    def project(rows, offsets):
        projections = set()
        for row in sorted(rows):
            tick()
            projections.add(tuple(row[offset] for offset in offsets))
        return projections

    left_projection = project(left_rows, left_offsets)
    right_projection = project(right_rows, right_positions)
    smaller, larger = sorted((left_projection, right_projection), key=len)
    common = set()
    for row in sorted(smaller):
        tick()
        if row in larger:
            common.add(row)

    def keep(rows, offsets):
        kept = set()
        for row in sorted(rows):
            tick()
            if tuple(row[offset] for offset in offsets) in common:
                kept.add(row)
        return frozenset(kept)

    return dict(scope=shared, common_rows=frozenset(common),
                left_rows=keep(left_rows, left_offsets),
                right_rows=keep(right_rows, right_positions))
