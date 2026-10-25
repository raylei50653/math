"""Exact semijoin on a shared, ordered interface in one literal colour frame.

Rows keep their private coordinates.  Projection is used only to find common
support, never to reconstruct a full row by mixing independent coordinates.
The optional callback charges each projected row and membership test before
performing it.  No input is mutated, including when the callback interrupts.
"""

from __future__ import annotations

from itertools import combinations


class SharedInterfaceIndex:
    """Live factor pairs with at least two shared variables and revision stamps.

    Factor objects expose ``scope`` and ``revision``.  Stable serial numbers
    distinguish new objects even when a retired object's list position or
    Python identity is reused.  Strong references are retained only for live
    factors.  Synchronization is staged: a charging exception leaves the last
    complete index and its revision stamps unchanged.
    """

    def __init__(self):
        self._factors = {}
        self._identities = {}
        self._scopes = {}
        self._incidence = {}
        self._pair_keys = set()
        self._seen = {}
        self._order = ()
        self._next_serial = 0

    def sync(self, factors, charge=None):
        """Register live factors, charging once per newly discovered pair.

        Two-variable incidence excludes pairs that share only one variable.
        A pair sharing three or more variables is discovered once and retains
        its entire shared interface when queried; this index never replaces a
        shared triple by independent pairs.  The optional callback runs before
        a newly discovered factor pair is registered.
        """
        if charge is not None and not callable(charge):
            raise ValueError("charge must be callable or None")
        live = tuple(factors)
        identities, factor_map, scopes, order = {}, {}, {}, []
        next_serial = self._next_serial
        new_serials = []
        for factor in live:
            identity = id(factor)
            if identity in identities:
                raise ValueError("live factors must contain distinct objects")
            scope = tuple(factor.scope)
            serial = self._identities.get(identity)
            if (serial is None or self._factors[serial] is not factor
                    or self._scopes[serial] != scope):
                serial = next_serial
                next_serial += 1
                new_serials.append(serial)
            identities[identity] = serial
            factor_map[serial] = factor
            scopes[serial] = scope
            order.append(serial)

        retained = set(factor_map) & set(self._factors)
        incidence = {key: members & retained
                     for key, members in self._incidence.items()
                     if members & retained}
        pair_keys = {pair for pair in self._pair_keys
                     if pair[0] in retained and pair[1] in retained}
        for serial in new_serials:
            keys = {frozenset(pair) for pair in combinations(scopes[serial], 2)}
            candidates = set()
            for key in keys:
                candidates.update(incidence.get(key, ()))
            for other in sorted(candidates):
                if charge is not None:
                    charge()
                pair_keys.add((min(serial, other), max(serial, other)))
            for key in keys:
                incidence.setdefault(key, set()).add(serial)

        # Commit only after every discovery charge has completed.  In
        # particular, interrupted new factors cannot inherit any old stamp.
        self._factors = factor_map
        self._identities = identities
        self._scopes = scopes
        self._incidence = incidence
        self._pair_keys = pair_keys
        self._seen = {pair: signature for pair, signature in self._seen.items()
                      if pair in pair_keys}
        self._order = tuple(order)
        self._next_serial = next_serial

    def pairs(self):
        """Yield factor pairs in the current live list's lexicographic order."""
        positions = {serial: position for position, serial in enumerate(self._order)}
        ordered = [tuple(sorted(pair, key=positions.__getitem__))
                   for pair in self._pair_keys]
        for left, right in sorted(ordered,
                                  key=lambda pair: (positions[pair[0]], positions[pair[1]])):
            yield self._factors[left], self._factors[right]

    def _key(self, left, right):
        left_serial = self._identities.get(id(left))
        right_serial = self._identities.get(id(right))
        if (left_serial is None or right_serial is None
                or self._factors[left_serial] is not left
                or self._factors[right_serial] is not right):
            return None
        key = (min(left_serial, right_serial), max(left_serial, right_serial))
        return key if key in self._pair_keys else None

    def _signature(self, key):
        return tuple(self._factors[serial].revision for serial in key)

    def seen(self, left, right):
        """Whether this live pair was completed at its current revisions."""
        key = self._key(left, right)
        return key is not None and self._seen.get(key) == self._signature(key)

    def mark_seen(self, left, right):
        """Record current revisions after a complete pair query and commit."""
        key = self._key(left, right)
        if key is None:
            raise ValueError("pair must be registered with a shared interface")
        self._seen[key] = self._signature(key)


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

    def keep(rows, offsets, projection):
        if len(common) == len(projection):
            # Every original row has shared support.  Reuse an immutable
            # relation instead of repeating its row-membership tests.  Common
            # is already a subset, so cardinalities suffice without another
            # uncharged relation traversal.
            return rows if isinstance(rows, frozenset) else frozenset(rows)
        kept = set()
        for row in sorted(rows):
            tick()
            if tuple(row[offset] for offset in offsets) in common:
                kept.add(row)
        return frozenset(kept)

    return dict(scope=shared, common_rows=frozenset(common),
                left_rows=keep(left_rows, left_offsets, left_projection),
                right_rows=keep(right_rows, right_positions, right_projection))
