"""Demand masks with separate known/allowed bits, independent of main solver.

Only the anchor rows are scanned. Other full relations remain available as
membership oracles. A missing support-cache bit is UNKNOWN, never false.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
from hashlib import sha256
import json
from math import prod
from pathlib import Path

from audit import (ROOT, Factor, cartesian_oracle, controls, projected_prefix,
                   random_cases, source_buckets, validate)


def demand_prefix(owner, boundary, domains, factors, anchor_index):
    stats = Counter()
    result = {}
    attempted, survived = {}, {}
    if not factors:
        bits = sum(1 << c for c in domains[owner])
        if bits:
            result[()] = bits
        return result, stats, attempted, survived
    anchor = factors[anchor_index]
    ab_scope = tuple(v for v in anchor.scope if v != owner)
    free = tuple(v for v in boundary if v not in anchor.scope)
    positions = {v: depth + 1 for depth, v in enumerate(free)}
    ready = [[] for _ in range(len(free) + 1)]
    for i, factor in enumerate(factors):
        if i != anchor_index:
            ready[max((positions.get(v, 0) for v in factor.scope), default=0)].append(i)
    grouped = {}
    for row in sorted(anchor.rows):
        stats["anchor_rows_scanned"] += 1
        okay = True
        for v, c in zip(anchor.scope, row):
            stats["anchor_domain_tests"] += 1
            if c not in domains[v]:
                okay = False
                break
        if okay:
            a = dict(zip(anchor.scope, row))
            key = tuple(a[v] for v in ab_scope)
            grouped[key] = grouped.get(key, 0) | (1 << a[owner])
            stats["anchor_mask_merges"] += 1
    stats["anchor_index_entries"] = len(grouped)
    cache = [{} for _ in factors]

    def put(trace, depth, key, bits):
        nodes = trace.setdefault(depth, {})
        nodes[key] = nodes.get(key, 0) | bits

    def query(index, assignment, live):
        factor = factors[index]
        key = tuple(assignment[v] for v in factor.scope if v != owner)
        stats["support_cache_lookups"] += 1
        known, allowed = cache[index].get(key, (0, 0))
        unknown = live & ~known
        stats["cached_colour_hits"] += (live & known).bit_count()
        if key not in cache[index]:
            stats["cache_entries_created"] += 1
        # Probe only untested colours that are still feasible at THIS prefix.
        while unknown:
            bit = unknown & -unknown
            color = bit.bit_length() - 1
            row = tuple(color if v == owner else assignment[v] for v in factor.scope)
            stats["raw_relation_membership_tests"] += 1
            if row in factor.rows:
                allowed |= bit
            known |= bit
            unknown ^= bit
        cache[index][key] = (known, allowed)
        stats["support_cache_stores"] += 1
        stats["live_mask_intersections"] += 1
        return live & allowed

    def visit(depth, assignment, live, ab, prefix):
        key = (ab, prefix)
        put(attempted, depth, key, live)
        stats["attempted_prefix_visits"] += 1
        for index in ready[depth]:
            live = query(index, assignment, live)
            if not live:
                return
        put(survived, depth, key, live)
        stats["surviving_prefix_visits"] += 1
        if depth == len(free):
            if not free:
                stats["candidate_attempts"] += 1
            b = tuple(assignment[v] for v in boundary)
            result[b] = result.get(b, 0) | live
            stats["output_updates"] += 1
            return
        vertex = free[depth]
        for color in domains[vertex]:
            stats["candidate_attempts"] += 1
            assignment[vertex] = color
            visit(depth+1, assignment, live, ab, (*prefix, color))
        assignment.pop(vertex, None)

    for ab, live in sorted(grouped.items()):
        stats["anchor_starts"] += 1
        visit(0, dict(zip(ab_scope, ab)), live, ab, ())
    stats["cached_known_bits"] = sum(known.bit_count() for entries in cache
                                    for known, _ in entries.values())
    stats["cached_allowed_bits"] = sum(allowed.bit_count() for entries in cache
                                      for _, allowed in entries.values())
    return dict(sorted(result.items())), stats, attempted, survived


def pick_anchor(boundary, domains, factors):
    return min(range(len(factors)), key=lambda i: len(factors[i].rows) * prod(
        len(domains[v]) for v in boundary if v not in factors[i].scope)) if factors else None


def dominance(literal_stats, demand_stats):
    assert demand_stats["anchor_rows_scanned"] == literal_stats["literal_anchor_rows_scanned"]
    assert demand_stats["raw_relation_membership_tests"] <= literal_stats["ready_factor_lookups"]
    assert demand_stats["support_cache_lookups"] <= literal_stats["ready_factor_lookups"]
    for key in ("candidate_attempts", "attempted_prefix_visits", "surviving_prefix_visits", "output_updates"):
        assert demand_stats[key] <= literal_stats[key]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-replay", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    small = []
    for item in [*controls(), *random_cases(), *source_buckets()]:
        owner, boundary, domains, factors = (item[k] for k in ("owner", "boundary", "domains", "factors"))
        validate(owner, boundary, domains, factors)
        anchor = pick_anchor(boundary, domains, factors)
        literal = projected_prefix(owner, boundary, domains, factors, anchor, masks=False)
        demand = demand_prefix(owner, boundary, domains, factors, anchor)
        expected = {b: sum(1 << c for c in choices) for b, choices in
                    cartesian_oracle(owner, boundary, domains, factors).items() if choices}
        assert literal[0] == demand[0] == expected
        assert literal[2] == demand[2] and literal[3] == demand[3]
        dominance(literal[1], demand[1])
        small.append(dict(name=item["name"], literal_stats=dict(literal[1]), demand_stats=dict(demand[1]),
                          exact_cartesian_fibres_including_empty_equal=True,
                          every_depth_projection_equal=True))
    frozen = json.loads(args.frozen_replay.read_text())
    groups = []
    totals = Counter()
    aggregate = Counter()
    for group in frozen["groups"]:
        path = ROOT / group["full_record"]
        data = path.read_bytes()
        assert sha256(data).hexdigest() == group["compressed_record_sha256"]
        record = json.loads(gzip.decompress(data))
        buckets = []
        for old, bucket in zip(group["buckets"], record["elimination_records"], strict=True):
            owner, boundary = bucket["vertex"], tuple(bucket["scope"])
            domains = {d["vertex"]: tuple(d["colors"]) for d in bucket["source_domains"]}
            factors = [Factor(tuple(f["scope"]), frozenset(map(tuple, f["rows"])))
                       for f in bucket["input_relations"]]
            anchor = pick_anchor(boundary, domains, factors)
            assert anchor == old["anchor_index"]
            demand = demand_prefix(owner, boundary, domains, factors, anchor)
            expected = {tuple(r["boundary"]): sum(1 << c for c in r["colors"]) for r in bucket["rows"]}
            assert demand[0] == expected
            previous = Counter(old["literal_stats"])
            dominance(previous, demand[1])
            old_charge = previous["literal_anchor_rows_scanned"] + previous["candidate_attempts"] + previous["ready_factor_lookups"]
            new_charge = demand[1]["anchor_rows_scanned"] + demand[1]["candidate_attempts"] + demand[1]["raw_relation_membership_tests"]
            assert new_charge <= old_charge
            buckets.append(dict(index=old["index"], demand_stats=dict(demand[1]),
                                original_membership_extension_row_visit_charge=dict(literal=old_charge, demand=new_charge),
                                exact_complete_saved_fibre_map_equal=True))
            totals.update(buckets=1, literal_charge=old_charge, demand_charge=new_charge,
                          nonempty_fibres=len(expected), empty_fibres=old["empty_fibres"])
            totals["original_operation_charge_improved" if new_charge < old_charge else
                   "original_operation_charge_tied"] += 1
            aggregate.update(demand[1])
        groups.append(dict(name=group["name"], buckets=buckets))
    result = dict(schema="demand-known-allowed-mask-audit-v1", small_cases=small,
                  source_frozen_replay=str(args.frozen_replay),
                  source_frozen_replay_sha256=sha256(args.frozen_replay.read_bytes()).hexdigest(),
                  sources={p.name: sha256(p.read_bytes()).hexdigest()
                           for p in (Path(__file__), Path(__file__).with_name("audit.py"))},
                  groups=groups, totals=dict(totals), demand_totals=dict(aggregate),
                  interpretation="Original row-membership tests and extension attempts are dominated at fixed anchor/order. "
                                 "Extra grouping, cache lookup/store, bit scans/intersections, tuple and allocation work is listed separately. "
                                 "The charge excludes that extra work and is NOT a total-work, main checks or speed claim. "
                                 "Small inputs checked independently Cartesian and by depthwise trace; frozen large buckets checked against exact complete saved fibre maps. "
                                 "Unknown cache bits never mean false. No main-engine change, changed schedule or whole-solver timing.")
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result["totals"], sort_keys=True))
    print("PASS demand masks: small Cartesian/depthwise checks and all frozen buckets")


if __name__ == "__main__":
    main()
