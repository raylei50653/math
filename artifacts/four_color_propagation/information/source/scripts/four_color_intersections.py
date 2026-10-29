"""Exact semijoin on a shared, ordered interface in one literal colour frame.

Rows keep their private coordinates.  Projection is used only to find common
support, never to reconstruct a full row by mixing independent coordinates.
The optional callback charges each projected row and membership test before
performing it.  No input is mutated, including when the callback interrupts.
"""

from __future__ import annotations

from collections import OrderedDict
from itertools import combinations
from heapq import heappop, heappush


class SharedInterfaceIndex:
    """Live factor pairs with at least two shared variables and revision stamps.

    Factor objects expose ``scope`` and ``revision``.  Stable serial numbers
    distinguish new objects even when a retired object's list position or
    Python identity is reused.  Strong references are retained only for live
    factors.  Synchronization is staged: a charging exception leaves the last
    complete index and its revision stamps unchanged.
    """

    def __init__(self, cache_max_rows=0, *, monotone_updates=False):
        if type(cache_max_rows) is not int or cache_max_rows < 0:
            raise ValueError("cache_max_rows must be a nonnegative integer")
        if type(monotone_updates) is not bool:
            raise ValueError("monotone_updates must be boolean")
        # Opt-in contract: an existing factor may only lose rows. Growth or a
        # scope change requires a new factor identity. The solver obeys this.
        self._monotone_updates = monotone_updates
        self._support_counts = {}
        self._pending = set()
        self._incident_pairs = {}
        self._known_revisions = {}
        self._pair_rank = {}
        self._heap = None
        self._queued = set()
        self._cursor = -1
        self.delta_stats = dict(pair_visits=0, queue_pushes=0, support_reuses=0, full_scope_views=0)
        self._factors = {}
        self._identities = {}
        self._scopes = {}
        self._incidence = {}
        self._pair_keys = set()
        self._seen = {}
        self._order = ()
        self._ordered_pairs = ()
        self._next_serial = 0
        self.skipped_pair_queries = 0
        self._cache_max_rows = cache_max_rows
        self._group_cache = OrderedDict()
        self._factor_cache_keys = {}
        self.cache_stats = dict(hits=0, builds=0, rows=0, peak_rows=0,
                                entries=0, evictions=0)

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
        if len(live) == len(self._order) and all(
                self._factors[serial] is factor and self._scopes[serial] == tuple(factor.scope)
                for serial, factor in zip(self._order, live)):
            for serial in tuple(self._factor_cache_keys):
                self._discard_stale_indexes(serial)
            if self._monotone_updates:
                self._notice_revisions()
            return
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
        positions = {serial: position for position, serial in enumerate(self._order)}
        ordered = []
        for key in pair_keys:
            left, right = sorted(key, key=positions.__getitem__)
            ordered.append((key, left, right))
        ordered.sort(key=lambda item: (positions[item[1]], positions[item[2]]))
        self._ordered_pairs = tuple(
            (key, factor_map[left], factor_map[right], left == key[0])
            for key, left, right in ordered)
        if self._monotone_updates:
            self._support_counts = {key: count for key, count in self._support_counts.items()
                                    if key in pair_keys}
            self._pending.intersection_update(pair_keys)
            self._pending.update(pair_keys - self._seen.keys())
            self._incident_pairs = {serial: set() for serial in order}
            self._pair_rank = {}
            for rank, (key, _, _, _) in enumerate(self._ordered_pairs):
                self._pair_rank[key] = rank
                for serial in key:
                    self._incident_pairs[serial].add(key)
            self._known_revisions = {serial: rev for serial, rev in self._known_revisions.items()
                                     if serial in factor_map}
            self._notice_revisions()
        for serial in tuple(self._factor_cache_keys):
            self._discard_stale_indexes(serial)

    def _notice_revisions(self, serials=None):
        for serial in self._order if serials is None else serials:
            revision = self._factors[serial].revision
            if self._known_revisions.get(serial) == revision:
                continue
            self._known_revisions[serial] = revision
            for key in self._incident_pairs[serial]:
                self._pending.add(key)
                rank = self._pair_rank[key]
                if self._heap is not None and rank > self._cursor and key not in self._queued:
                    heappush(self._heap, (rank, key))
                    self._queued.add(key)
                    self.delta_stats["queue_pushes"] += 1

    def pairs(self):
        """Yield factor pairs in the current live list's lexicographic order."""
        for _, left, right, _ in self._ordered_pairs:
            yield left, right

    def pending_pairs(self):
        """Yield only unfinished pairs, checking revisions at iteration time.

        The retained array follows current live-list order and holds strong
        factor references.  Revision changes after one yield are observed by
        subsequent entries, so pruning can awaken a later pair in this pass.
        Topology synchronization must happen between complete pair passes.
        """
        if self._monotone_updates:
            yield from self._pending_delta_pairs()
            return
        for key, left, right, forward in self._ordered_pairs:
            signature = self._seen.get(key)
            if signature is not None:
                first, second = (left, right) if forward else (right, left)
                if signature[0] == first.revision and signature[1] == second.revision:
                    self.skipped_pair_queries += 1
                    continue
            yield left, right

    def _pending_delta_pairs(self):
        """Preserve pass order: changes behind the cursor wait until next pass.

        Call mark_seen after committing each yielded pair. Other row changes
        are discovered by sync between passes. Unfinished queries stay pending.
        """
        self._notice_revisions()
        self._heap, self._queued, self._cursor = [], set(), -1
        yielded = 0
        for key in self._pending:
            heappush(self._heap, (self._pair_rank[key], key))
            self._queued.add(key)
            self.delta_stats["queue_pushes"] += 1
        try:
            while self._heap:
                rank, key = heappop(self._heap)
                self._queued.remove(key)
                self._cursor = rank
                if key not in self._pending:
                    continue
                if self._seen.get(key) == self._signature(key):
                    self._pending.discard(key)
                    continue
                _, left, right, _ = self._ordered_pairs[rank]
                self.delta_stats["pair_visits"] += 1
                yielded += 1
                yield left, right
            self.skipped_pair_queries += len(self._ordered_pairs) - yielded
        finally:
            self._heap, self._queued, self._cursor = None, set(), -1

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

    def mark_seen(self, left, right, support_count=None):
        """Record revisions after a complete pair query and commit.

        With monotone_updates, support_count must be the cardinality of the
        completed common projection, after BOTH filtered relations commit.
        Omit it to disable the support shortcut for this pair.
        """
        key = self._key(left, right)
        if key is None:
            raise ValueError("pair must be registered with a shared interface")
        self._seen[key] = self._signature(key)
        if self._monotone_updates:
            if support_count is None:
                self._support_counts.pop(key, None)
            else:
                self._support_counts[key] = support_count
            self._notice_revisions(key)
            self._pending.discard(key)
        for serial in key:
            self._discard_stale_indexes(serial)

    def _remove_group_index(self, key, *, eviction=False):
        entry = self._group_cache.pop(key)
        self.cache_stats["rows"] -= entry[2]
        self.cache_stats["entries"] -= 1
        keys = self._factor_cache_keys[key[0]]
        keys.remove(key)
        if not keys:
            del self._factor_cache_keys[key[0]]
        if eviction:
            self.cache_stats["evictions"] += 1

    def _discard_stale_indexes(self, serial):
        keys = self._factor_cache_keys.get(serial)
        if not keys:
            return
        revision = self._factors[serial].revision if serial in self._factors else None
        for key in tuple(keys):
            if serial not in self._factors or key[1] != revision:
                self._remove_group_index(key)

    def _group_index(self, factor, serial, shared, offsets, tick):
        """Return complete support keys and optional full-row groups.

        A cache row is one retained reference to an original complete row on
        one ordered interface.  Oversized entries use a temporary projection
        and ordinary row filtering, so capacity exhaustion omits no support.
        """
        self._discard_stale_indexes(serial)
        key = (serial, factor.revision, shared)
        tick()
        if (self._monotone_updates and isinstance(factor.rows, frozenset)
                and offsets == tuple(range(len(factor.scope)))):
            # The ordered interface IS this whole relation: projection is
            # the identity. Reuse it rather than build a second row index.
            self.delta_stats["full_scope_views"] += 1
            return factor.rows, None
        entry = self._group_cache.get(key)
        if entry is not None:
            self.cache_stats["hits"] += 1
            self._group_cache.move_to_end(key)
            return entry[0], entry[1]

        if not factor.rows or len(factor.rows) > self._cache_max_rows:
            projection = set()
            for row in sorted(factor.rows):
                tick()
                projection.add(tuple(row[offset] for offset in offsets))
            return frozenset(projection), None

        groups = {}
        for row in sorted(factor.rows):
            tick()
            projected = tuple(row[offset] for offset in offsets)
            groups.setdefault(projected, []).append(row)
        # Freeze already constructed groups.  This changes storage only;
        # all relation projections and group insertions above were charged.
        immutable_groups = {projected: tuple(rows) for projected, rows in groups.items()}
        projection = frozenset(immutable_groups)
        entry = (projection, immutable_groups, len(factor.rows))
        # No incomplete entry or speculative eviction is published if any
        # charge interrupts the build.  Capacity counts retained references;
        # the current query may also hold completed temporary entry objects.
        while self.cache_stats["rows"] + entry[2] > self._cache_max_rows:
            self._remove_group_index(next(iter(self._group_cache)), eviction=True)
        self._group_cache[key] = entry
        self._factor_cache_keys.setdefault(serial, set()).add(key)
        self.cache_stats["builds"] += 1
        self.cache_stats["rows"] += entry[2]
        self.cache_stats["entries"] += 1
        self.cache_stats["peak_rows"] = max(self.cache_stats["peak_rows"],
                                             self.cache_stats["rows"])
        return projection, immutable_groups

    def intersect(self, left, right, charge=None):
        """Exact semijoin, optionally reusing retained full-interface groups.

        Every cached group contains complete original rows, including private
        coordinates.  Shared tuples always follow the left scope's full order.
        Charge before each cache lookup, projected input row/group construction,
        common-support membership, retained group lookup, and collected full
        row.  Exceptions never modify either factor or publish partial groups.
        The default zero capacity delegates to the uncached pure function.
        """
        if charge is not None and not callable(charge):
            raise ValueError("charge must be callable or None")
        if not self._cache_max_rows and not self._monotone_updates:
            return intersect_on_shared(left.scope, left.rows, right.scope, right.rows,
                                       charge=charge)
        left_serial = self._identities.get(id(left))
        right_serial = self._identities.get(id(right))
        if (left_serial is None or right_serial is None
                or self._factors[left_serial] is not left
                or self._factors[right_serial] is not right):
            # Only registered strong-reference identities may own cache entries.
            return intersect_on_shared(left.scope, left.rows, right.scope, right.rows,
                                       charge=charge)
        right_offsets = {vertex: offset for offset, vertex in enumerate(right.scope)}
        shared = tuple(vertex for vertex in left.scope if vertex in right_offsets)
        left_offsets = tuple(offset for offset, vertex in enumerate(left.scope)
                             if vertex in right_offsets)
        right_positions = tuple(right_offsets[vertex] for vertex in shared)

        def tick():
            if charge is not None:
                charge()

        key = self._key(left, right)
        seen = self._seen.get(key)
        old_count = self._support_counts.get(key)
        unchanged = {}
        if self._monotone_updates and seen is not None and old_count is not None:
            unchanged = {serial: self._factors[serial].revision == revision
                         for serial, revision in zip(key, seen)}
        if unchanged.get(left_serial) or unchanged.get(right_serial):
            # Previously both projections equalled S. With row deletion only,
            # if one side is unchanged, the other's projection T is a subset
            # of S. Hence common = T, with no second intersection needed.
            changed_left = unchanged.get(right_serial, False)
            factor = left if changed_left else right
            serial = left_serial if changed_left else right_serial
            offsets = left_offsets if changed_left else right_positions
            common, groups = self._group_index(factor, serial, shared, offsets, tick)
            tick()
            self.delta_stats["support_reuses"] += 1
            if len(common) == old_count:
                return dict(scope=shared, common_rows=common,
                            left_rows=left.rows if isinstance(left.rows, frozenset) else frozenset(left.rows),
                            right_rows=right.rows if isinstance(right.rows, frozenset) else frozenset(right.rows))
            if changed_left:
                left_projection, left_groups = common, groups
                right_projection, right_groups = self._group_index(
                    right, right_serial, shared, right_positions, tick)
            else:
                right_projection, right_groups = common, groups
                left_projection, left_groups = self._group_index(
                    left, left_serial, shared, left_offsets, tick)
        else:
            left_projection, left_groups = self._group_index(
                left, left_serial, shared, left_offsets, tick)
            right_projection, right_groups = self._group_index(
                right, right_serial, shared, right_positions, tick)
            smaller, larger = sorted((left_projection, right_projection), key=len)
            common = set()
            for row in sorted(smaller):
                tick()
                if row in larger:
                    common.add(row)

        def keep(factor, offsets, projection, groups):
            if len(common) == len(projection):
                return factor.rows if isinstance(factor.rows, frozenset) else frozenset(factor.rows)
            if self._monotone_updates and offsets == tuple(range(len(factor.scope))):
                tick()
                return frozenset(common)
            kept = set()
            if groups is None:
                for row in sorted(factor.rows):
                    tick()
                    if tuple(row[offset] for offset in offsets) in common:
                        kept.add(row)
            else:
                for projected in sorted(common):
                    tick()
                    for row in groups[projected]:
                        tick()
                        kept.add(row)
            return frozenset(kept)

        return dict(scope=shared, common_rows=frozenset(common),
                    left_rows=keep(left, left_offsets, left_projection, left_groups),
                    right_rows=keep(right, right_positions, right_projection, right_groups))


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
