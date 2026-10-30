#!/usr/bin/env python3
"""Exact Ck component-partition consistency and greatest obstruction sets.

This generalizes only the noncrossing component-partition condition in
``c5_kempe_screen.py``. It does not use that module's exterior screen, a graph
catalogue, or the Four Color Theorem. Calling it the classical D criterion
requires a separate comparison of definitions.

All boundary positions keep their cyclic order. Each state is one complete
S4 orbit of proper boundary colorings. A witness is one joint partition for
both complementary color pairs; independent single-vertex supports are never
substituted. Abstract witness partitions are not claimed to be realizable.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


PAIRS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def normalize(values):
    labels = {}
    return tuple(labels.setdefault(value, len(labels)) for value in values)


@lru_cache(maxsize=None)
def patterns(k):
    """Proper ordered Ck states, normalized only by a single common S4 action."""
    if type(k) is not int or k < 3:
        raise ValueError("ring length must be an integer at least three")

    def visit(prefix, maximum):
        if len(prefix) == k:
            if prefix[-1] != prefix[0]:
                yield tuple(prefix)
            return
        for color in range(min(3, maximum + 1) + 1):
            if prefix and prefix[-1] == color:
                continue
            yield from visit(prefix + [color], max(maximum, color))

    return tuple(visit([], -1))


def partitions(values):
    """Every set partition exactly once; block order is not significant."""
    if not values:
        yield ()
        return
    first, *rest = values
    for partition in partitions(rest):
        yield ((first,),) + partition
        for j, block in enumerate(partition):
            yield partition[:j] + ((first,) + block,) + partition[j + 1:]


def noncrossing(blocks):
    """Joint noncrossing test on the original cyclic boundary positions."""
    owner = {v: j for j, block in enumerate(blocks) for v in block}
    return not any(owner[a] == owner[c] and owner[b] == owner[d]
                   and owner[a] != owner[b]
                   for a, b, c, d in combinations(sorted(owner), 4))


def _forced_atoms(pattern, pairs):
    """Contract only same-pair *boundary edges* before partition enumeration.

    The output atoms are forced subsets of a single Kempe component. Merging
    arbitrary atoms later still visits every admissible component partition.
    This avoids enumerating Bell(k) partitions and rejecting forced links.
    """
    size = len(pattern)
    parent = list(range(size))
    side = [int(color in pairs[1]) for color in pattern]

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for v in range(size):
        w = (v + 1) % size
        if side[v] == side[w]:
            parent[root(w)] = root(v)
    grouped = {}
    for v in range(size):
        grouped.setdefault(root(v), []).append(v)
    atoms = tuple(sorted(tuple(points) for points in grouped.values()))
    return tuple(tuple(atom for atom in atoms if side[atom[0]] == s) for s in (0, 1))


def _expanded_partitions(atoms):
    for partition in partitions(tuple(range(len(atoms)))):
        yield tuple(tuple(sorted(v for j in block for v in atoms[j])) for block in partition)


@lru_cache(maxsize=None)
def partition_options(k, pattern_index, split, planar=True):
    """All ``(orbit_mask, joint_partition)`` options for this state and split.

    Unlike ``obligations``, this retains distinct partitions having the same
    swap orbit. A proposed connectivity/locking rule must filter this complete
    family, not one arbitrarily selected representative per orbit.
    """
    states = patterns(k)
    if not 0 <= pattern_index < len(states) or not 0 <= split < len(PAIRS):
        raise ValueError("pattern index or complementary split out of range")
    index = {pattern: j for j, pattern in enumerate(states)}
    pattern = states[pattern_index]
    pairs = PAIRS[split]
    left_atoms, right_atoms = _forced_atoms(pattern, pairs)
    mate = {a: b for pair in pairs for a, b in (pair, pair[::-1])}
    options = []
    for left in _expanded_partitions(left_atoms):
        for right in _expanded_partitions(right_atoms):
            blocks = tuple(sorted(left + right))
            if planar and not noncrossing(blocks):
                continue
            orbit = 0
            for selected in range(1 << len(blocks)):
                changed = list(pattern)
                for j, block in enumerate(blocks):
                    if selected >> j & 1:
                        for v in block:
                            changed[v] = mate[pattern[v]]
                assert all(changed[v] != changed[(v + 1) % k] for v in range(k))
                orbit |= 1 << index[normalize(changed)]
            options.append((orbit, blocks))
    assert options
    return tuple(sorted(options))


@lru_cache(maxsize=None)
def _obligation_data(k, planar=True):
    states = patterns(k)
    table = []
    for pattern_index in range(len(states)):
        row = []
        for split in range(len(PAIRS)):
            witnesses = {}
            for orbit, blocks in partition_options(k, pattern_index, split, planar):
                if orbit not in witnesses or blocks < witnesses[orbit]:
                    witnesses[orbit] = blocks
            assert witnesses
            row.append(tuple(sorted(witnesses.items())))
        table.append(tuple(row))
    return tuple(table)


def obligations(k, planar=True):
    """Return ``[state][split]`` tuples of complete block-swap orbit masks.

    Each alternative is existential: one such whole orbit must be contained
    in a consistent set. All three splits must have a passing alternative.
    The underlying chosen joint partition is retained for certificates.
    """
    return tuple(tuple(tuple(mask for mask, _ in choices) for choices in row)
                 for row in _obligation_data(k, planar))


def _indices(mask):
    result = []
    while mask:
        bit = mask & -mask
        result.append(bit.bit_length() - 1)
        mask ^= bit
    return result


def failure(mask, table):
    """First failed obligation, or None if this complete set is consistent."""
    for j in _indices(mask):
        for split, choices in enumerate(table[j]):
            if not any(mask & orbit == orbit for orbit in choices):
                return dict(pattern=j, split=split, required_alternatives=list(choices))
    return None


def obstruction(k, accepted_mask, planar=True):
    """Greatest consistent subset disjoint from a complete accepted relation.

    Peeling is synchronous. Every consistent subset of the current set remains
    after each round; the final fixed point is therefore greatest, not merely
    one locally stable candidate. Empty residual means only that no abstract
    obstruction passes this specified partition screen.
    """
    states = patterns(k)
    full = (1 << len(states)) - 1
    if type(accepted_mask) is not int or accepted_mask < 0 or accepted_mask & ~full:
        raise ValueError("accepted_mask must be a nonnegative mask on this ring's states")
    data = _obligation_data(k, planar)
    current = full ^ accepted_mask
    initial = current
    rounds = []
    while True:
        removed = []
        remove_mask = 0
        for j in _indices(current):
            for split, choices in enumerate(data[j]):
                if not any(current & orbit == orbit for orbit, _ in choices):
                    removed.append(dict(
                        pattern_index=j, pattern=list(states[j]), split=split,
                        required_alternatives=[dict(
                            orbit_mask=orbit,
                            missing_pattern_indices=_indices(orbit & ~current),
                            joint_partition=[list(block) for block in blocks])
                            for orbit, blocks in choices]))
                    remove_mask |= 1 << j
                    break
        if not remove_mask:
            break
        after = current & ~remove_mask
        rounds.append(dict(round=len(rounds) + 1, before_mask=current,
                           removed_mask=remove_mask, after_mask=after,
                           removals=removed))
        current = after
    survivors = []
    for j in _indices(current):
        witnesses = []
        for split, choices in enumerate(data[j]):
            orbit, blocks = next((orbit, blocks) for orbit, blocks in choices
                                 if current & orbit == orbit)
            witnesses.append(dict(split=split, orbit_mask=orbit,
                                  joint_partition=[list(block) for block in blocks]))
        survivors.append(dict(pattern_index=j, pattern=list(states[j]), witnesses=witnesses))
    return dict(
        ring_length=k, pattern_order=[list(pattern) for pattern in states],
        complementary_splits=[[list(pair) for pair in pairs] for pairs in PAIRS],
        topology="joint noncrossing partitions" if planar else "unrestricted partitions",
        accepted_mask=accepted_mask, accepted_count=accepted_mask.bit_count(),
        initial_obstruction_mask=initial, initial_obstruction_count=initial.bit_count(),
        residual_mask=current, residual_count=current.bit_count(),
        rounds=rounds, survivors=survivors,
        criterion="repo component-partition consistency; classical-D comparison is separate",
        scope="No graph realizability, actual exterior, Four Color Theorem, or efficiency claim.")


def controls():
    """Narrow controls against the existing C5 definition and literal colors."""
    import c5_kempe_screen as old

    assert patterns(5) == old.REPS
    table = obligations(5)
    assert [[list(choices) for choices in row] for row in table] == old.obligations()
    accepted = [mask for mask in range(1, 1 << len(patterns(5)))
                if failure(mask, table) is None]
    assert len(accepted) == 153
    # Independent finite maximality check: list every stable C5 set first,
    # then take their union under each possible acceptance restriction.
    stable = [0] + accepted
    for acceptance in range(1024):
        greatest = 0
        for candidate in stable:
            if not candidate & acceptance:
                greatest |= candidate
        assert obstruction(5, acceptance)["residual_mask"] == greatest
    unrestricted = obligations(5, planar=False)
    assert all(failure(mask, unrestricted) is None for mask in range(1, 1024))
    assert not noncrossing(((0, 2), (1, 3), (4,)))
    assert noncrossing(((0, 3), (1, 2), (4,)))
    for k in (5, 6, 7, 8):
        literal = {normalize(row) for row in product(range(4), repeat=k)
                   if all(row[v] != row[(v + 1) % k] for v in range(k))}
        assert patterns(k) == tuple(sorted(literal))
        # Without topology, merging each whole color-pair side gives a
        # singleton normalized orbit. Hence *every* subset is stable, even
        # though enumerating all subsets for k=8 would be inappropriate.
        assert all(1 << j in choices for j, row in enumerate(obligations(k, planar=False))
                   for choices in row)
    return dict(c5_pattern_order_matches=True, c5_obligations_match=True,
                c5_consistent_nonempty_masks=len(accepted),
                c5_unrestricted_nonempty_masks=1023,
                c5_greatest_fixed_point_checked_for_all_1024_accepted_masks=True,
                literal_pattern_orbits_checked_through_ring_length=8,
                unrestricted_singleton_orbit_controls_through_ring_length=8,
                crossing_negative_control=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path,
                        help="Explicit new output path; no historical artifact is overwritten implicitly.")
    args = parser.parse_args()
    checked = controls()
    wheels = []
    for k in (5, 6, 7, 8):
        accepted = sum(1 << j for j, pattern in enumerate(patterns(k)) if max(pattern) < 3)
        wheels.append(obstruction(k, accepted))
    report = dict(
        script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        controls=checked, wheel_controls=wheels,
        trust="Component-partition screen only; no exterior gluing or 4CT oracle.")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps([dict(k=row["ring_length"], patterns=len(row["pattern_order"]),
                           accepted=row["accepted_count"], residual=row["residual_count"],
                           rounds=len(row["rounds"])) for row in wheels], sort_keys=True))


if __name__ == "__main__":
    main()
