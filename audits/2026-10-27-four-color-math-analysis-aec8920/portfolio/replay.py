#!/usr/bin/env python3
"""Exact relation-query toy model for persistent lazy/eager work interleaving.

One logical step either examines one complete original row in the lazy plan,
or projects and indexes one complete original row in the eager plan. These
are model units, not CPU instructions or the production solver's checks.
"""

import argparse
from collections import defaultdict
import hashlib
from itertools import product
import json
from pathlib import Path
import random


class Portfolio:
    def __init__(self, rows, width):
        self.rows = tuple(sorted(set(rows)))
        self.width = width
        self.groups = defaultdict(list)
        self.eager_position = 0
        self.eager_complete = not self.rows
        self.cache = {}
        self.turn = "lazy"
        self.lazy_work = 0
        self.eager_work = 0
        self.lookups = 0

    def query(self, key):
        self.lookups += 1
        if self.eager_complete:
            rows = self.groups.get(key, ())
            return rows[0] if rows else None
        if key in self.cache:
            return self.cache[key]
        position = 0
        while True:
            if self.turn == "eager":
                row = self.rows[self.eager_position]
                self.groups[row[:self.width]].append(row)
                self.eager_position += 1
                self.eager_work += 1
                self.turn = "lazy"
                if self.eager_position == len(self.rows):
                    self.eager_complete = True
                    rows = self.groups.get(key, ())
                    return rows[0] if rows else None
            else:
                row = self.rows[position]
                position += 1
                self.lazy_work += 1
                self.turn = "eager"
                if row[:self.width] == key:
                    self.cache[key] = row
                    return row
                if position == len(self.rows):
                    self.cache[key] = None
                    return None


def verify_case(name, rows, width, requests):
    rows = tuple(sorted(set(rows)))
    eager = defaultdict(list)
    for row in rows:
        eager[row[:width]].append(row)
    plan = Portfolio(rows, width)
    pure_lazy_cache = {}
    pure_lazy_work = 0
    prefixes = []
    for q, key in enumerate(requests, 1):
        expected = eager.get(key, ())
        expected = expected[0] if expected else None
        if key not in pure_lazy_cache:
            answer = None
            for row in rows:
                pure_lazy_work += 1
                if row[:width] == key:
                    answer = row
                    break
            pure_lazy_cache[key] = answer
        assert pure_lazy_cache[key] == expected
        answer = plan.query(key)
        assert answer == expected
        total = plan.lazy_work + plan.eager_work
        bound = 2 * min(pure_lazy_work, len(rows))
        assert total <= bound, (name, q, total, bound)
        assert abs(plan.lazy_work - plan.eager_work) <= 1
        if plan.eager_complete:
            assert dict(plan.groups) == dict(eager)
        else:
            # Incomplete indexing is never treated as a negative answer.
            assert plan.eager_position < len(rows)
        prefixes.append(dict(requests=q, pure_lazy_work=pure_lazy_work,
                             eager_work_to_complete=len(rows), portfolio_work=total,
                             twice_best_plan=bound))
    return dict(name=name, complete_input_rows=len(rows), interface_width=width,
                requests=len(requests), all_answers_equal=True,
                all_prefix_bounds_passed=True, lazy_work=plan.lazy_work,
                eager_work=plan.eager_work, total_work=plan.lazy_work+plan.eager_work,
                pure_lazy_work=pure_lazy_work, eager_complete=plan.eager_complete,
                prefixes=prefixes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rng = random.Random(20261027)
    results = []
    # These are full proper colourings of the original four-leaf star.
    star = [(a, b, c, d, x) for a, b, c, d, x in product(range(4), repeat=5)
            if x not in (a, b, c, d)]
    keys4 = list(product(range(4), repeat=4))
    results.append(verify_case("original_star_all_boundaries", star, 4, keys4))
    results.append(verify_case("original_star_one_easy_positive", star, 4, [star[0][:4]]))
    results.append(verify_case("original_star_repeated_positive", star, 4, [star[0][:4]]*300))
    results.append(verify_case("original_star_early_empty_fibre", star, 4, [(0, 1, 2, 3)]))
    results.append(verify_case("empty_relation", (), 2, [(0, 0), (1, 2)]))
    results.append(verify_case("empty_interface_true", [(0,), (1,)], 0, [(), ()]))
    results.append(verify_case("empty_interface_false", (), 0, [(), ()]))
    keys2 = list(product(range(4), repeat=2))
    universe = list(product(range(4), repeat=3))
    for index in range(160):
        probability = (index % 9) / 8
        rows = [row for row in universe if rng.random() < probability]
        requests = rng.choices(keys2, k=48)
        results.append(verify_case(f"seeded_relation_{index}", rows, 2, requests))
    report = dict(schema="four-color-lazy-eager-portfolio-model-v1", cases=len(results),
                  query_prefixes_checked=sum(r["requests"] for r in results),
                  all_answers_equal=True, all_prefix_bounds_passed=True,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  cost_model="Each row comparison or row projection/index insertion is one equal-cost logical step. Common preparation, tuple widths, result lookups, immutable snapshots, scheduling and memory are separate. This does not measure CPU time or production checks.",
                  theorem_scope="One fixed complete relation, one fixed interface, and one fixed request sequence with completed-query caching. The alternating turn persists across requests. Before any revision or change to interface or factors, both plans must be invalidated. No claim for arbitrary CPU costs or adaptive query-order comparisons.",
                  results=results)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x") as stream:
        json.dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({key: report[key] for key in ("cases", "query_prefixes_checked", "all_answers_equal", "all_prefix_bounds_passed")}))


if __name__ == "__main__":
    main()
