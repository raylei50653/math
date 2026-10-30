#!/usr/bin/env python3
"""Recover literal Jordan sides of a dual cycle from its frozen primal disk.

The dual cycle is supplied as an ordered ``traces`` record, with the first
vertex repeated at the end.  Original primal and dual edge IDs coincide.
Removing the primal edges crossed by a simple dual cycle leaves its two
Jordan sides.  The side containing the five primal boundary vertices is
the exterior.  This avoids a drawing, floating point geometry, or inferred
side choices made separately for different reference matchings.
"""
from __future__ import annotations

from collections import Counter


def cycle_geometry(graph, cycle, matching=None):
    """Return ordered off-cycle halfedge sides, including actual inner chords.

    ``graph`` has ``primal_vertices``, ``primal_edges``, ``oriented_faces``,
    ``network_internal_vertices`` and ``network_edges`` as in the frozen C5
    certificates.  The caller is responsible for checking that these data
    describe the specified plane disk; this function additionally checks
    the cycle, primal separation, and exact dual edge correspondence.

    Side 1 means the bounded interior.  A matching chord is recorded once
    as an edge and twice in ``off_cycle_edges``/``inside_bits``, one entry
    for each endpoint incidence, as required by the rotation parity lemma.
    If supplied, ``matching`` must contain each off-cycle edge on the cycle.
    All returned edge and vertex IDs retain their original identities.
    """
    primal_edges = graph['primal_edges']
    edges = graph['network_edges']
    faces = graph['oriented_faces']
    n = graph['network_internal_vertices']
    ordered = list(cycle['vertices'])
    cycle_edges = list(cycle['edges'])
    assert not cycle.get('ends')
    assert ordered[0] == ordered[-1]
    vertices = ordered[:-1]
    assert len(vertices) == len(set(vertices)) == len(cycle_edges)
    assert len(cycle_edges) == len(set(cycle_edges))
    assert len(vertices) >= 2 and all(v < n for v in vertices)
    assert len(edges) == len(primal_edges) and n == len(faces)
    for u, v, e in zip(ordered, ordered[1:], cycle_edges):
        assert Counter(edges[e]) == Counter((u, v))
        assert set(primal_edges[e]) <= set(faces[u]) & set(faces[v])

    cut = set(cycle_edges)
    adjacency = {v: [] for v in range(graph['primal_vertices'])}
    for e, (u, v) in enumerate(primal_edges):
        if e not in cut:
            adjacency[u].append(v)
            adjacency[v].append(u)
    unseen, sides = set(adjacency), []
    while unseen:
        reached, queue = {min(unseen)}, [min(unseen)]
        for v in queue:
            for w in adjacency[v]:
                if w not in reached:
                    reached.add(w)
                    queue.append(w)
        unseen -= reached
        sides.append(reached)
    assert len(sides) == 2
    boundary = set(range(5))
    outside = next(s for s in sides if boundary <= s)
    inside = next(s for s in sides if s is not outside)
    assert all((u in inside) != (v in inside) for e in cut
               for u, v in [primal_edges[e]])

    incident = {v: [] for v in range(n)}
    for e, ends in enumerate(edges):
        for v in ends:
            if v < n:
                incident[v].append(e)
    off_cycle, bits = [], []
    for v in vertices:
        assert len(incident[v]) == 3
        candidates = set(incident[v]) - cut
        assert len(candidates) == 1
        e = candidates.pop()
        if matching is not None:
            assert e in matching
        u, w = primal_edges[e]
        assert (u in inside) == (w in inside)
        off_cycle.append(e)
        bits.append(int(u in inside))

    cycle_vertices = set(vertices)
    inner_vertices = [v for v, face in enumerate(faces) if set(face) <= inside]
    outer_vertices = [v for v, face in enumerate(faces) if set(face) <= outside]
    assert set(inner_vertices) | set(outer_vertices) | cycle_vertices == set(range(n))
    assert not (set(inner_vertices) & set(outer_vertices))
    assert set(inner_vertices).isdisjoint(cycle_vertices)
    assert set(outer_vertices).isdisjoint(cycle_vertices)
    inner_edges = [e for e, ends in enumerate(primal_edges) if set(ends) <= inside]
    outer_edges = [e for e, ends in enumerate(primal_edges) if set(ends) <= outside]
    assert set(inner_edges) | set(outer_edges) | cut == set(range(len(edges)))
    assert all(set(edges[e]) <= set(inner_vertices) | cycle_vertices for e in inner_edges)
    assert all(set(edges[e]) <= set(outer_vertices) | cycle_vertices | set(range(n, n+5))
               for e in outer_edges)
    inner_chords = sorted({e for e in inner_edges if set(edges[e]) <= cycle_vertices})
    return dict(cycle_vertices=vertices, cycle_edges=cycle_edges,
                inside_primal_vertices=sorted(inside),
                outside_primal_vertices=sorted(outside),
                inside_network_vertices=inner_vertices,
                outside_network_vertices=outer_vertices,
                inside_network_edges=inner_edges,
                outside_network_edges=outer_edges,
                off_cycle_edges=off_cycle, inside_bits=bits,
                inside_chord_edges=inner_chords)
