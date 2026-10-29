#!/usr/bin/env python3
"""Small exact controls for weighted retain/copy-delete semijoin planning.

This is an independent proposal, not a change to the main colouring solver.
The explicit model charges one metadata unit for a complete-group length query
(including its hash lookup and O(1) len). During filtering, one group lookup or
one full-row insertion/deletion/copy is one unit; final immutable-row
materialization is counted separately, one unit per output row.
Cached complete grouping, complete common support K, and the already-discovered
opposite-side last-support-loss set F are inputs. F may contain keys absent on
this side. Projection/group construction and support-loss discovery are NOT
claimed free: they precede this filter and belong to whole-query cost.
"""

import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from four_color_intersections import intersect_on_shared


class Interrupted(Exception):
    pass


class Work:
    def __init__(self, limit=None):
        self.limit = limit
        self.counts = Counter()

    def tick(self, phase):
        if self.limit is not None and sum(self.counts.values()) >= self.limit:
            raise Interrupted
        self.counts[phase] += 1


def group_rows(rows, offsets):
    groups = {}
    for row in rows:
        groups.setdefault(tuple(row[i] for i in offsets), []).append(row)
    return {key: tuple(values) for key, values in groups.items()}


def materialize(rows, work):
    for row in rows:
        work.tick("materialize")
        yield row


def adaptive_filter(rows, groups, common, forbidden, *, limit=None):
    """Return every original private row whose whole interface is in common.

    Preconditions: immutable rows; complete disjoint groups of exactly rows;
    common is the already-computed complete common support, a subset of groups;
    forbidden is the already-computed opposite-side last-support-loss set,
    with set(groups)-forbidden == common. It can contain currently absent keys.
    All intermediate mutable sets are private. An interrupt publishes nothing.
    """
    work = Work(limit)
    n, s, k, f = len(rows), len(groups), len(common), len(forbidden)
    if k == s:
        return rows, dict(plan="identity", n=n, k=k, d=0, f=f, p=n, r=0,
                          keep_cost=0, drop_cost=0, counts=dict(work.counts))
    if not k:
        return frozenset(), dict(plan="empty", n=n, k=0, d=s, f=f, p=0, r=n,
                                 keep_cost=0, drop_cost=n+f+n,
                                 counts=dict(work.counts))
    d = s-k
    if k <= f:
        # C_drop-C_keep=f+2r-k >=0, without examining group weights.
        # Use incoming complete losses; never scan all keys to discover D.
        plan = "retain"
    else:
        r = 0
        for key in forbidden:
            work.tick("estimate")
            r += len(groups.get(key, ()))
        p = n-r
        keep_cost, drop_cost = k+p, n+f+r
        plan = "retain" if keep_cost <= drop_cost else "copy-delete"
    answer = set()
    if plan == "retain":
        for key in common:
            work.tick("filter")
            for row in groups[key]:
                work.tick("filter")
                answer.add(row)
    else:
        for row in rows:
            work.tick("filter")
            answer.add(row)
        for key in forbidden:
            work.tick("filter")
            for row in groups.get(key, ()):
                work.tick("filter")
                answer.remove(row)
    p = len(answer)
    r = n-p
    keep_cost, drop_cost = k+p, n+f+r
    result = frozenset(materialize(answer, work))
    info = dict(plan=plan, n=n, k=k, d=d, f=f, p=p, r=r,
                keep_cost=keep_cost, drop_cost=drop_cost, counts=dict(work.counts))
    assert work.counts["estimate"] == (f if k > f else 0)
    assert work.counts["filter"] == min(keep_cost, drop_cost)
    # The selector's full variable work is <=C_min. Existing last-support-loss
    # discovery is an explicit prerequisite, not hidden preprocessing here.
    assert work.counts["estimate"] <= min(keep_cost, drop_cost)
    assert info["counts"]["materialize"] == p
    return result, info


def checked_filter(rows, offsets, common, forbidden=None):
    groups = group_rows(rows, offsets)
    expected = frozenset(r for r in rows if tuple(r[i] for i in offsets) in common)
    forbidden = frozenset(groups)-common if forbidden is None else forbidden
    assert frozenset(groups)-forbidden == common
    answer, info = adaptive_filter(rows, groups, common, forbidden)
    assert answer == expected
    assert set(groups) >= common
    assert sum(map(len, groups.values())) == len(rows)
    return answer, info


def exhaustive_controls():
    universe = tuple(product(range(2), repeat=3))
    interface_keys = tuple(product(range(2), repeat=2))
    count, decisions = 0, Counter()
    for row_mask in range(1 << len(universe)):
        rows = frozenset(row for i, row in enumerate(universe) if row_mask >> i & 1)
        projection = frozenset((row[1], row[0]) for row in rows)
        for key_mask in range(1 << len(interface_keys)):
            allowed = frozenset(key for i, key in enumerate(interface_keys) if key_mask >> i & 1)
            _, info = checked_filter(rows, (1, 0), allowed & projection,
                                     frozenset(interface_keys)-allowed)
            decisions[info["plan"]] += 1
            count += 1
    return dict(exact_conditions=count, decisions=dict(decisions),
                coverage="All 256 binary 3-coordinate relations x 16 interface masks; full private rows and reversed interface order.")


def weighted_control(heavy_removed):
    keys = tuple(product(range(4), repeat=2))
    private = tuple(product(range(4), repeat=4))
    rows = frozenset(key+tail for i, key in enumerate(keys)
                     for tail in (private if (i == 0) == heavy_removed else private[:1]))
    common = frozenset(keys[1:])
    _, info = checked_filter(rows, (0, 1), common, frozenset(keys[:1]))
    info["cardinality_rule_plan"] = "copy-delete" if info["d"] < info["k"] else "retain"
    return info


def pair_controls():
    rng = random.Random(17)
    left_scope, right_scope = (0, 1, 2, 3), (1, 4, 0, 5)
    left_offsets, right_offsets = (0, 1), (2, 0)
    universe = tuple(product(range(2), repeat=4))
    conditions = 0
    for _ in range(64):
        left = frozenset(r for r in universe if rng.randrange(3))
        right = frozenset(r for r in universe if rng.randrange(3))
        initial = intersect_on_shared(left_scope, left, right_scope, right)
        left, right = initial["left_rows"], initial["right_rows"]
        previous = initial["common_rows"]
        for _ in range(5):
            left_new = frozenset(r for r in left if rng.randrange(4))
            right_new = frozenset(r for r in right if rng.randrange(4))
            lp = frozenset(tuple(r[i] for i in left_offsets) for r in left_new)
            rp = frozenset(tuple(r[i] for i in right_offsets) for r in right_new)
            left_loss, right_loss = previous-lp, previous-rp
            common = previous-left_loss-right_loss
            assert common == lp & rp
            got_left, _ = checked_filter(left_new, left_offsets, common, right_loss)
            got_right, _ = checked_filter(right_new, right_offsets, common, left_loss)
            oracle = intersect_on_shared(left_scope, left_new, right_scope, right_new)
            assert got_left == oracle["left_rows"]
            assert got_right == oracle["right_rows"]
            assert common == oracle["common_rows"]
            left, right, previous = got_left, got_right, common
            conditions += 1
    return dict(monotone_pair_conditions=conditions, seed=17,
                coverage="Both sides may shrink; exact full-row results agree with the existing pure semijoin, including private coordinates and unequal scope orders.")


def last_support_control():
    left = frozenset(((0, 1, 0), (0, 1, 1)))
    new_left = frozenset(((0, 1, 1),))
    right = frozenset(((0, 1, 2), (0, 1, 3)))
    previous = frozenset((r[0], r[1]) for r in left)
    loss = previous-frozenset((r[0], r[1]) for r in new_left)
    bad_loss = frozenset((r[0], r[1]) for r in left-new_left)
    answer, info = checked_filter(right, (0, 1), previous-loss, loss)
    assert not loss and bad_loss == previous and answer == right
    return dict(correct_lost_supports=len(loss), wrongly_projected_deleted_rows=len(bad_loss),
                retained_right_rows=len(answer), plan=info["plan"])


def interruption_controls():
    cases = []
    for heavy in (False, True):
        keys = tuple(product(range(4), repeat=2))
        private = tuple(product(range(2), repeat=4))
        rows = frozenset(key+tail for i, key in enumerate(keys)
                         for tail in (private if (i == 0) == heavy else private[:1]))
        groups, common = group_rows(rows, (0, 1)), frozenset(keys[1:])
        forbidden = frozenset(keys[:1])
        answer, info = adaptive_filter(rows, groups, common, forbidden)
        full_cost = sum(info["counts"].values())
        count = 0
        frozen_groups = dict(groups)
        for budget in range(full_cost):
            try:
                adaptive_filter(rows, groups, common, forbidden, limit=budget)
            except Interrupted:
                count += 1
            else:
                raise AssertionError("partial budget unexpectedly returned output")
            assert groups == frozen_groups
        complete, _ = adaptive_filter(rows, groups, common, forbidden, limit=full_cost)
        assert complete == answer
        cases.append(dict(plan=info["plan"], interrupted_prefixes=count, full_cost=full_cost))
    return cases


def amortized_control(n=32):
    keys = tuple(product(range(4), repeat=3))[:n]
    rows = frozenset(key+(0,) for key in keys)
    totals, plans = Counter(), Counter()
    for key in keys:
        groups = group_rows(rows, (0, 1, 2))
        common = frozenset(groups)-{key}
        updated, info = adaptive_filter(rows, groups, common, frozenset((key,)))
        totals.update(info["counts"])
        plans[info["plan"]] += 1
        rows = updated
    assert not rows
    assert totals["materialize"] == n*(n-1)//2
    assert totals["estimate"] <= n
    return dict(initial_rows=n, removed_rows_over_epoch=n, final_rows=0,
                counts=dict(totals), decisions=dict(plans),
                selector_length_reads_bound=n,
                unavoidable_explicit_output_rows=n*(n-1)//2,
                interpretation="Only n row removals, yet explicit immutable outputs enumerate n(n-1)/2 retained rows. No linear whole-query amortized claim.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = dict(
        schema="weighted-full-group-filter-control-v1",
        mathematical_contract="A complete-group length query, including hash lookup and O(1) len, is one metadata unit. During filtering, one group lookup or one full-row insertion/copy/deletion is one unit. Given cached complete groups and already-discovered opposite-side support losses F, with f=|F|, k retained support keys, p retained rows / r removed rows, n=p+r: C_keep=k+p, C_drop=n+f+r. If k<=f, retain dominates without planning. Otherwise f complete-group length queries give r and p; selector plus selected filter costs <=2 min(C_keep,C_drop). F can contain currently absent keys. Projection/group construction, support-loss discovery and final immutable materialization remain separate.",
        exhaustive=exhaustive_controls(), pair_histories=pair_controls(),
        sparse_heavy_loss=weighted_control(True), sparse_light_loss=weighted_control(False),
        last_support=last_support_control(), interruptions=interruption_controls(),
        amortized=amortized_control(),
        sources={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (Path(__file__), ROOT/"scripts/four_color_intersections.py",
                           ROOT/"docs/four_color_support_loss.md")},
        scope="Independent exact relation controls. Main engine unchanged; no timing benchmark, no universal speed or academic novelty claim.",
    )
    args.out.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)+"\n")
    print(json.dumps({k: v for k, v in report.items() if k != "sources"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
