"""Independent bucket-mask join experiment; never patches the main solver.

All tables retain their full ordered non-owner coordinates.  Missing keys are
zero support, and all four owner colours remain in each mask.  The Cartesian
oracle does not call any implementation helper or a solver verification API.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import prod
from pathlib import Path
import random
import sys


ROOT = Path(__file__).resolve().parents[3]
PALETTE = tuple(range(4))


@dataclass(frozen=True)
class Factor:
    scope: tuple[int, ...]
    rows: frozenset[tuple[int, ...]]


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate(owner, boundary, domains, factors):
    assert owner not in boundary and len(boundary) == len(set(boundary))
    assert set(domains) == {owner, *boundary}
    assert all(set(d).issubset(PALETTE) and len(d) == len(set(d)) for d in domains.values())
    for factor in factors:
        assert owner in factor.scope and len(factor.scope) == len(set(factor.scope))
        assert set(factor.scope).issubset(domains)
        assert all(len(row) == len(factor.scope) and set(row).issubset(PALETTE)
                   for row in factor.rows)
    assert set(boundary) == {v for f in factors for v in f.scope if v != owner} or not factors


def cartesian_oracle(owner, boundary, domains, factors):
    """Direct definition: enumerate every boundary, every owner colour, all factors."""
    result = {}
    for b in product(*(domains[v] for v in boundary)):
        choices = []
        for c in domains[owner]:
            assignment = dict(zip(boundary, b))
            assignment[owner] = c
            if all(tuple(assignment[v] for v in f.scope) in f.rows for f in factors):
                choices.append(c)
        result[b] = tuple(choices)
    return result


def encode_trace(trace):
    return [{"depth": depth, "prefixes": [
        {"anchor_boundary": list(key[0]), "free_prefix": list(key[1]), "mask": mask}
        for key, mask in sorted(nodes.items())]} for depth, nodes in sorted(trace.items())]


def projected_prefix(owner, boundary, domains, factors, anchor_index, *, masks):
    """Literal prefix vs exact owner-mask prefix, fixed anchor/free/ready orders.

    The literal branch follows the main bucket's current search order, but its
    counters are independent audit counters, not the main solver's checks.
    """
    stats = Counter()
    attempted, survived = {}, {}
    result = {}
    owner_mask = sum(1 << c for c in domains[owner])

    def trace_put(trace, depth, key, bits):
        trace.setdefault(depth, {})[key] = trace.setdefault(depth, {}).get(key, 0) | bits

    if not factors:
        for b in product(*(domains[v] for v in boundary)):
            if owner_mask:
                result[b] = owner_mask
        return result, stats, attempted, survived

    anchor = factors[anchor_index]
    anchor_boundary = tuple(v for v in anchor.scope if v != owner)
    free = tuple(v for v in boundary if v not in anchor.scope)
    free_positions = {v: depth + 1 for depth, v in enumerate(free)}
    ready = [[] for _ in range(len(free) + 1)]
    for i, factor in enumerate(factors):
        if i != anchor_index:
            depth = max((free_positions.get(v, 0) for v in factor.scope), default=0)
            ready[depth].append(i)

    indices = []
    if masks:
        for factor in factors:
            xoffset = factor.scope.index(owner)
            offsets = tuple(i for i, v in enumerate(factor.scope) if v != owner)
            table = {}
            for row in sorted(factor.rows):
                stats["preprocess_input_rows"] += 1
                okay = True
                for v, c in zip(factor.scope, row):
                    stats["preprocess_domain_tests"] += 1
                    if c not in domains[v]:
                        okay = False
                        break
                if okay:
                    b = tuple(row[i] for i in offsets)
                    table[b] = table.get(b, 0) | (1 << row[xoffset])
                    stats["preprocess_mask_merges"] += 1
            indices.append(table)
        stats["index_entries"] = sum(map(len, indices))
        starts = [(b, bits & owner_mask) for b, bits in sorted(indices[anchor_index].items())]
    else:
        starts = []
        for row in sorted(anchor.rows):
            stats["literal_anchor_rows_scanned"] += 1
            okay = True
            for v, c in zip(anchor.scope, row):
                stats["literal_anchor_domain_tests"] += 1
                if c not in domains[v]:
                    okay = False
                    break
            if okay:
                a = dict(zip(anchor.scope, row))
                starts.append((tuple(a[v] for v in anchor_boundary), 1 << a[owner]))

    def accepted(depth, assignment, live):
        for index in ready[depth]:
            factor = factors[index]
            stats["ready_factor_lookups"] += 1
            if masks:
                key = tuple(assignment[v] for v in factor.scope if v != owner)
                live &= indices[index].get(key, 0)
                stats["mask_intersections"] += 1
                if not live:
                    return 0
            else:
                if tuple(assignment[v] for v in factor.scope) not in factor.rows:
                    return 0
        return live

    def visit(depth, assignment, live, ab, free_prefix):
        key = (ab, free_prefix)
        trace_put(attempted, depth, key, live)
        stats["attempted_prefix_visits"] += 1
        live = accepted(depth, assignment, live)
        if not live:
            return
        trace_put(survived, depth, key, live)
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
            visit(depth + 1, assignment, live, ab, (*free_prefix, color))
        assignment.pop(vertex, None)

    for ab, live in starts:
        stats["anchor_starts"] += 1
        assignment = dict(zip(anchor_boundary, ab))
        if not masks:
            assignment[owner] = live.bit_length() - 1
        visit(0, assignment, live, ab, ())
    return dict(sorted(result.items())), stats, attempted, survived


def factor(scope, predicate):
    return Factor(tuple(scope), frozenset(row for row in product(PALETTE, repeat=len(scope))
                                        if predicate(dict(zip(scope, row)))))


def case(name, owner, boundary, domains, factors, *, kind="synthetic_relation_control"):
    return dict(name=name, owner=owner, boundary=tuple(boundary),
                domains={v: tuple(sorted(d)) for v, d in domains.items()},
                factors=list(factors), kind=kind)


def controls():
    full = lambda vs: {v: PALETTE for v in vs}
    yield case("isolated-owner", 7, (), {7: PALETTE}, [])
    yield case("empty-owner-domain", 7, (), {7: ()}, [])
    yield case("unary-owner-fixed", -10, (), {-10: (2,)},
               [Factor((-10,), frozenset((c,) for c in PALETTE))])
    yield case("opposed-owner-supports", 9, (12, -3), full((9, 12, -3)),
               [factor((9, -3), lambda a: a[9] == 0),
                factor((12, 9), lambda a: a[9] == 1)])
    yield case("empty-factor", 0, (2, 1), full((0, 1, 2)),
               [factor((0, 1), lambda a: True), Factor((2, 0), frozenset())])
    yield case("star-four-leaves", 0, (4, 1, 3, 2), full(range(5)),
               [factor((v, 0) if v % 2 else (0, v), lambda a, v=v: a[0] != a[v])
                for v in range(1, 5)], kind="original_star_incident_edge_factors")
    yield case("dense-four-colour-support", 0, (4, 1, 3, 2), full(range(5)),
               [factor((v, 0), lambda a: True) for v in range(1, 5)])
    yield case("k4-complete-template", 2, (3, 0, 1), full(range(4)),
               [Factor((0, 2, 3, 1), frozenset(permutations(PALETTE)))],
               kind="original_k4_complete_template")
    domains = {100: (0,), **{i: PALETTE for i in range(5)}}
    yield case("preprocessing-backfire-fixed-owner", 100, (4, 3, 2, 1, 0), domains,
               [Factor((4, 100, 3, 2, 1, 0), frozenset({(0, 0, 0, 0, 0, 0)})),
                factor((100, 0, 1, 2, 3, 4), lambda a: a[100] == 0)])
    yield case("different-private-boundaries-and-orders", 80, (17, -4, 2, 9),
               {80: (0, 1, 3), 17: (1, 3), -4: (0, 2, 3), 2: (2,), 9: PALETTE},
               [factor((80, 2, -4), lambda a: a[80] != a[2] and a[80] != a[-4]),
                factor((9, -4, 80), lambda a: (a[9] + a[-4] + a[80]) % 3 != 0),
                factor((17, 80, 9), lambda a: a[80] != a[17] and a[17] != a[9])])


def random_cases():
    rng = random.Random(20261027)
    for number in range(96):
        owner = -101
        boundary = list(range(rng.randrange(1, 5)))
        rng.shuffle(boundary)
        domains = {v: tuple(c for c in PALETTE if rng.random() < .72)
                   for v in (owner, *boundary)}
        factors = []
        coverage = set()
        for i in range(rng.randrange(1, 5)):
            scope = [owner, *(v for v in boundary if rng.random() < .65)]
            rng.shuffle(scope)
            density = rng.choice((.1, .3, .6, .9, 1.))
            rows = frozenset(row for row in product(PALETTE, repeat=len(scope))
                             if rng.random() < density)
            factors.append(Factor(tuple(scope), rows))
            coverage.update(scope)
        for v in sorted(set(boundary) - coverage):
            factors.append(factor((v, owner), lambda a, v=v: a[v] != a[owner]))
        yield case(f"seeded-factor-{number:02}", owner, boundary, domains, factors,
                   kind="seeded_arbitrary_complete_factor_sample")


def source_buckets():
    """Only tiny actual solves; inspect their recorded buckets, never monkeypatch."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from four_color_constraints import solve_constraints
    graphs = [
        {"name": "star", "vertices": list(range(5)), "edges": [[0, v] for v in range(1, 5)]},
        {"name": "k4", "vertices": list(range(4)), "edges": list(combinations(range(4), 2))},
        {"name": "k5", "vertices": list(range(5)), "edges": list(combinations(range(5), 2))},
        {"name": "fixed-cycle", "vertices": [50, -7, 12, 9, 31],
         "edges": [[50, -7], [-7, 12], [12, 9], [9, 31], [31, 50]], "fixed": [[50, 2]]},
    ]
    for graph in graphs:
        for method in ("anchor", "prefix"):
            result = solve_constraints(graph, use_substructures=False, use_conflicts=False,
                                       max_checks=1000000, trace_limit=10000,
                                       record_relations=True, bucket_method=method)
            assert result["status"] != "limit"
            for i, record in enumerate(result["elimination_records"]):
                factors = [Factor(tuple(f["scope"]), frozenset(map(tuple, f["rows"])))
                           for f in record["input_relations"]]
                item = case(f"actual-{graph['name']}-{method}-bucket-{i}", record["vertex"],
                            record["scope"], {d["vertex"]: d["colors"] for d in record["source_domains"]},
                            factors, kind="current_solver_recorded_bucket")
                item["actual_record_mask_table"] = {
                    tuple(row["boundary"]): sum(1 << c for c in row["colors"])
                    for row in record["rows"]}
                yield item


def audit_case(item):
    owner, boundary, domains, factors = (item[k] for k in ("owner", "boundary", "domains", "factors"))
    validate(owner, boundary, domains, factors)
    expected = cartesian_oracle(owner, boundary, domains, factors)
    expected_masks = {b: sum(1 << c for c in choices) for b, choices in expected.items() if choices}
    if "actual_record_mask_table" in item:
        assert expected_masks == item["actual_record_mask_table"]
    anchor = min(range(len(factors)), key=lambda i: len(factors[i].rows) * prod(
        len(domains[v]) for v in boundary if v not in factors[i].scope)) if factors else None
    literal = projected_prefix(owner, boundary, domains, factors, anchor, masks=False)
    masked = projected_prefix(owner, boundary, domains, factors, anchor, masks=True)
    assert literal[0] == masked[0] == expected_masks, item["name"]
    assert literal[2] == masked[2], (item["name"], "attempted prefix colour sets")
    assert literal[3] == masked[3], (item["name"], "surviving prefix colour sets")
    for field in ("candidate_attempts", "ready_factor_lookups", "attempted_prefix_visits",
                  "surviving_prefix_visits", "output_updates"):
        assert masked[1][field] <= literal[1][field], (item["name"], field)
    complete = [{"boundary": list(b), "mask": sum(1 << c for c in choices)}
                for b, choices in expected.items()]
    return dict(name=item["name"], kind=item["kind"], owner=owner, boundary=list(boundary),
                domains=[dict(vertex=v, colors=list(domains[v])) for v in (owner, *boundary)],
                factor_scopes=[list(f.scope) for f in factors], factor_rows=[len(f.rows) for f in factors],
                anchor_index=anchor, complete_boundary_count=len(expected),
                nonempty_fibres=len(expected_masks), empty_fibres=len(expected) - len(expected_masks),
                legal_full_assignments=sum(map(len, expected.values())),
                complete_fibres_sha256=digest(complete), literal_stats=dict(literal[1]),
                mask_stats=dict(masked[1]), exact_fibres_including_absent_equal=True,
                every_depth_prefix_projection_equal=True,
                online_extension_lookup_visit_update_counts_dominated=True,
                complete_fibres=complete if item["kind"] != "seeded_arbitrary_complete_factor_sample" else None,
                mask_surviving_prefix_trace=encode_trace(masked[3])
                    if item["name"] in ("opposed-owner-supports", "different-private-boundaries-and-orders") else None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    items = [*controls(), *random_cases(), *source_buckets()]
    results = [audit_case(item) for item in items]
    opposed = next(item for item in items if item["name"] == "opposed-owner-supports")
    projected_relations = []
    for f in opposed["factors"]:
        offsets = tuple(i for i, v in enumerate(f.scope) if v != opposed["owner"])
        projected_relations.append((tuple(f.scope[i] for i in offsets),
                                    {tuple(row[i] for i in offsets) for row in f.rows}))
    naive_rows = 0
    for b in product(*(opposed["domains"][v] for v in opposed["boundary"])):
        a = dict(zip(opposed["boundary"], b))
        naive_rows += all(tuple(a[v] for v in scope) in rows for scope, rows in projected_relations)
    exact_rows = next(row["nonempty_fibres"] for row in results if row["name"] == opposed["name"])
    assert naive_rows == 16 and exact_rows == 0
    source = ROOT / "scripts/four_color_constraints.py"
    lines = source.read_text().splitlines()
    excerpt = "\n".join(f"{i+1}: {line}" for i, line in enumerate(lines) if 1383 <= i < 1486) + "\n"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    excerpt_path = args.out.with_name(args.out.stem + "-current-bucket-excerpt.txt")
    if excerpt_path.exists():
        raise FileExistsError(excerpt_path)
    excerpt_path.write_text(excerpt)
    report = dict(schema="owner-colour-mask-join-audit-v1", seed=20261027,
                  source_base_head="aec8920",
                  source_identity="current working tree including existing uncommitted changes; not pure base HEAD",
                  sources={"audit.py": sha256(Path(__file__).read_bytes()).hexdigest(),
                           str(source.relative_to(ROOT)): sha256(source.read_bytes()).hexdigest()},
                  source_excerpt=excerpt_path.name, cases=results,
                  totals=dict(cases=len(results), kinds=dict(Counter(r["kind"] for r in results)),
                              complete_fibres=sum(r["complete_boundary_count"] for r in results),
                              empty_fibres=sum(r["empty_fibres"] for r in results),
                              full_assignments=sum(r["legal_full_assignments"] for r in results)),
                  negative_control=dict(name="separate_boolean_exists_projection_is_unsound",
                                        case="opposed-owner-supports",
                                        separate_projections_accept_boundary_rows=naive_rows,
                                        exact_mask_intersection_accepts_boundary_rows=exact_rows),
                  interpretation="Independent Cartesian join verifies every fibre, including absent/empty. "
                                 "Fixed-anchor online prefix domination excludes preprocessing and does not imply total speed. "
                                 "Counters are this audit's logical operation counts, not main-solver checks or CPU time. "
                                 "Synthetic factor controls are not whole-graph solve benchmarks. No main solver modification.")
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report["totals"], sort_keys=True))
    print("PASS: all complete Cartesian fibres and depthwise prefix projections agree")


if __name__ == "__main__":
    main()
