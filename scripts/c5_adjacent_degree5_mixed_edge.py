#!/usr/bin/env python3
"""Sole mixed original K2, one distinct contact at each adjacent root.

Arbitrary-size proofs are in the report. Abstract unary data, actual K2
attachments, full-graph controls and minor skeletons have separate scopes.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

import c5_adjacent_degree5_interfaces as base
import c5_adjacent_degree5_shared_singleton as unary
from c5_single_spoke_three_one import edge, validate_minor


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge/observations.json"
TABLE = OUT.with_name("necessary_table.md")
U = frozenset(base.U)
SUPPORTS = tuple(combinations(range(5), 2))


def forbidden(x, y):
    """Exact K2 rejection, with the original uv inequality still present."""
    if len(x) != 2 or len(y) != 2:
        return frozenset()
    return frozenset((next(iter(x - {c})), next(iter(y - {c}))) for c in x & y)


def region_for(su, sv):
    return base.make_region("mixed_uv", [(7, 8)],
                            {7: (base.Z,) + su, 8: (base.W,) + sv})


def local_audit():
    records, counts = [], Counter()
    for su, sv in product(SUPPORTS, repeat=2):
        region = region_for(su, sv)
        transcript, canonical = [], []
        for row in base.ROWS:
            x, y = U - {row[i] for i in su}, U - {row[i] for i in sv}
            relation, ports, witnesses = base.joint_interface(region, row)
            assert ports == (7, 8)
            expected = base.PAIRS - forbidden(x, y)
            assert relation == expected
            transcript.append([row, base.mask(relation)])
            counts["actual_attachment_row_checks"] += 1
            if row not in base.CANONICAL:
                continue
            canonical.append(dict(row=row, lists=[sorted(x), sorted(y)],
                                  tuples=sorted(witnesses), forbidden=sorted(forbidden(x, y))))
            for a, b in sorted(base.PAIRS):
                fixed = dict(enumerate(row)) | {base.Z: a, base.W: b}
                coloring = base.first_coloring(tuple(range(9)), region["edges"], fixed)
                assert (coloring is not None) == ((a, b) in expected)
                counts["independent_pinned_queries"] += 1
                for e in sorted(region["edges"]):
                    coloring = base.first_coloring(tuple(range(9)), region["edges"] - {e}, fixed)
                    assert coloring is not None
                    if (a, b) not in expected:
                        assert coloring[e[0]] == coloring[e[1]]
                        counts["deleted_endpoint_forcing_checks"] += 1
                    counts["independent_deletion_queries"] += 1
            for sigma in permutations(base.U):
                moved = tuple(sigma[c] for c in row)
                actual = base.joint_interface(region, moved)[0]
                assert actual == frozenset((sigma[a], sigma[b]) for a, b in relation)
                counts["common_frame_checks"] += 1
        records.append(dict(support_u=su, support_v=sv, edges=sorted(region["edges"]),
                            canonical_rows=canonical,
                            all_rows_sha256=sha256(json.dumps(transcript).encode()).hexdigest()))
    # Full endpoint marginals introduce the forbidden same-color uv tuple.
    x, y = frozenset({0, 3}), frozenset({1, 3})
    tuples = set(product(x, y)) - base.DELTA
    marginal_product = set(product({a for a, _ in tuples}, {b for _, b in tuples}))
    assert (3, 3) not in tuples and (3, 3) in marginal_product
    assert (0, 1) in forbidden(x, y)
    assert any(a != 0 and b != 1 for a, b in marginal_product)
    assert not any(a != 0 and b != 1 for a, b in tuples)
    negative = dict(lists=[sorted(x), sorted(y)], tuples=sorted(tuples),
                    marginal_product=sorted(marginal_product), falsely_accepted_root_pair=[0, 1],
                    equal_lists_forbid_diagonals=sorted(forbidden(x, x)))
    return records, dict(counts), negative


def allowed(left, right, banned, root_edge=True, mixed=True):
    pairs = set(product(left, right))
    return pairs - (base.DELTA if root_edge else set()) - (banned if mixed else set())


def direct_minimality(left, right, banned):
    ez, ew = unary.residual(left), unary.residual(right)
    if allowed(ez, ew, banned) or not allowed(ez, ew, banned, root_edge=False):
        return False
    if not allowed(ez, ew, banned, mixed=False):
        return False
    for i in range(len(left[2])):
        if not allowed(unary.residual(left, i), ew, banned):
            return False
    for i in range(len(right[2])):
        if not allowed(ez, unary.residual(right, i), banned):
            return False
    for c in U - left[0]:
        if not allowed({c} - unary.union(left[2]), ew, banned):
            return False
    for c in U - right[0]:
        if not allowed(ez, {c} - unary.union(right[2]), banned):
            return False
    return True


def side_condition(side):
    available, _, bans = side
    return (all(f <= available for f in bans)
            and all(f - unary.union([g for j, g in enumerate(bans) if i != j])
                    for i, f in enumerate(bans)))


def normal_form(left, right, d, e):
    if d == e:
        return False
    ez, ew = unary.residual(left), unary.residual(right)
    return (((ez == {d} and ew == {d, e}) or (ez == {d, e} and ew == {e}))
            and side_condition(left) and side_condition(right))


def abstract_audit():
    options = unary.sides()
    records, counts, shapes = [], Counter(), Counter()
    for d, e in product(range(3), repeat=2):
        banned = forbidden(frozenset({d, 3}), frozenset({e, 3}))
        for left, right in product(options, repeat=2):
            direct = direct_minimality(left, right, banned)
            assert direct == normal_form(left, right, d, e), (left, right, d, e)
            counts["minimality_comparisons"] += 1
            if not direct:
                continue
            small_root = "z" if len(unary.residual(left)) == 1 else "w"
            small, large = (left, right) if small_root == "z" else (right, left)
            assert sum(map(len, small[2])) == sum(small[1])
            assert len(unary.union(small[2])) == sum(small[1])
            assert sum(large[1]) - len(unary.union(large[2])) == 1
            planar = all(side[1] != (3,) for side in (left, right))
            if planar:
                assert small[1] in ((1,), (2,), (1, 1), (2, 1), (1, 1, 1))
                assert large[1] in ((2,), (2, 1))
                assert all(len(f) == 1 for f in large[2])
                key = str((len(U - small[0]), small[1], len(U - large[0]), large[1]))
                shapes[key] += 1
            records.append(dict(id=len(records), missing_u=d, missing_v=e, small_root=small_root,
                                z=unary.encode_side(left), w=unary.encode_side(right),
                                planar_necessary_retained=planar))
    counts.update(side_candidates=len(options), abstract_records=len(records),
                  planar_necessary_records=sum(r["planar_necessary_retained"] for r in records))
    assert len(records) == 816 and counts["planar_necessary_records"] == 576
    return records, dict(counts), dict(sorted(shapes.items()))


def alternating(su, sv):
    return (len(set(su + sv)) == 4
            and ((su[0] < sv[0] < su[1]) != (su[0] < sv[1] < su[1])))


def attachment_audit():
    records = []
    for su, sv in product(SUPPORTS, repeat=2):
        x, y = U - {base.Q[i] for i in su}, U - {base.Q[i] for i in sv}
        if len(x) != 2 or len(y) != 2 or x == y:
            continue
        d, e = next(iter(x - {3})), next(iter(y - {3}))
        assert forbidden(x, y) == {(d, e)}
        crossed = alternating(su, sv)
        # Independent circular-word test of the two disjoint crosscuts.
        word = [0 if i in su else 1 for i in sorted(set(su + sv))]
        assert crossed == (len(set(su + sv)) == 4 and word in ([0, 1, 0, 1], [1, 0, 1, 0]))
        row = dict(id=len(records), support_u=su, support_v=sv, missing_u=d, missing_v=e,
                   crossing_excluded=crossed,
                   original_crosscuts=[[su[0], "u", su[1]], [sv[0], "v", sv[1]]])
        records.append(row)
    rho = lambda i: (3 - i) % 5
    pi = (1, 0, 2, 3)
    keys = {(tuple(r["support_u"]), tuple(r["support_v"])): r for r in records}
    for r in records:
        key = (tuple(sorted(rho(i) for i in r["support_u"])),
               tuple(sorted(rho(i) for i in r["support_v"])))
        reflected = keys[key]
        assert reflected["missing_u"] == pi[r["missing_u"]]
        assert reflected["missing_v"] == pi[r["missing_v"]]
        assert reflected["crossing_excluded"] == r["crossing_excluded"]
        r["reflected_id"] = reflected["id"]
    assert len(records) == 40 and sum(r["crossing_excluded"] for r in records) == 4
    return records


def cross_row_audit():
    """Any lists arising from two boundary attachments, with nonempty residuals."""
    lists = [x for x in unary.subsets(U) if len(x) in (2, 3)]
    residuals = [x for x in unary.subsets(U) if x]
    count = 0
    for x, y in product(lists, repeat=2):
        f = forbidden(x, y)
        off = f - base.DELTA
        for ez, ew in product(residuals, repeat=2):
            reject = not allowed(ez, ew, f)
            predicted = ez == ew and len(ez) == 1
            if off:
                assert len(off) == 1
                a, b = next(iter(off))
                predicted |= (ez == {a} and ew <= {a, b}) or (ew == {b} and ez <= {a, b})
            assert reject == predicted
            count += 1
    return dict(cases=count,
                scope="row-specific original lists and unary residuals; q normal forms are not transferred")


def fixed_graph_audit():
    """A true minimal q-core; no disk or T4 claim."""
    regions = [region_for((1, 4), (0, 4)),
               base.make_region("z_single", [], {9: (base.Z, 0, 1, 4)}),
               base.make_region("w_triangle", [(10, 11), (10, 12), (11, 12)],
                                {10: (0, 4), 11: (base.W, 0), 12: (base.W, 0)}),
               base.make_region("w_single", [], {13: (base.W, 0, 1, 4)})]
    edges = (base.CYCLE | {base.edge(base.Z, base.W), base.edge(base.Z, 1), base.edge(base.Z, 4)}
             | unary.union([r["edges"] for r in regions]))
    vertices = tuple(range(14))
    assert [sum(v in e for e in edges) for v in vertices[5:]] == [5, 5] + [4] * 7
    assert not base.whole_pairs(vertices, edges, base.Q)
    witnesses = []
    for e in sorted(edges - base.CYCLE):
        f = base.first_coloring(vertices, edges - {e}, dict(enumerate(base.Q)))
        assert f is not None and f[e[0]] == f[e[1]]
        witnesses.append(dict(edge=e, coloring=[f[v] for v in vertices]))
    transcript, canonical = [], []
    for row in base.ROWS:
        local = [base.joint_interface(r, row) for r in regions]
        direct = base.whole_pairs(vertices, edges, row)
        assert direct == base.glued_pairs(regions, [r[0] for r in local], edges, row, frozenset())
        transcript.append([row, base.mask(direct)])
        if row in base.CANONICAL:
            canonical.append(dict(row=row, root_pairs=sorted(direct),
                                  local_tuples=[dict(name=r["name"], ports=t[1], tuples=sorted(t[2]))
                                                for r, t in zip(regions, local)]))
    return dict(scope="actual degree (5,5,4,...) minimal q-core; disk/T4 not certified",
                vertices=vertices, edges=sorted(edges), q_deletion_witnesses=witnesses,
                canonical_rows=canonical,
                all_rows_sha256=sha256(json.dumps(transcript).encode()).hexdigest())


def minor_audit(attachments):
    """Original r-u-B or r-v-B replaces the shared-singleton external path."""
    records = []
    for a in attachments:
        for root, port, support in (("z", "u", a["support_u"]), ("w", "v", a["support_v"])):
            for landing in support:
                for lengths in ((0, 0, 0), (1, 3, 1), (2, 2, 2)):
                    es = {edge(f"b{i}", f"b{(i+1)%5}") for i in range(5)}
                    es.update({edge("z", "u"), edge("u", "v"), edge("v", "w"), edge("w", "z")})
                    for name, supp in (("u", a["support_u"]), ("v", a["support_v"])):
                        es.update(edge(name, f"b{i}") for i in supp)
                    arms, groups = [], [{root}]
                    outside = {f"b{i}" for i in range(5)} | {port}
                    for k, length in enumerate(lengths):
                        arm = [f"a{k}_{j}" for j in range(length + 1)]
                        es.update(edge(x, y) for x, y in zip(arm, arm[1:]))
                        es.add(edge(root, arm[-1]))
                        # Both direct and subdivided actual boundary tethers.
                        tether = [arm[0], f"t{k}", f"b{(landing+k)%5}"] if length else [arm[0], f"b{(landing+k)%5}"]
                        es.update(edge(x, y) for x, y in zip(tether, tether[1:]))
                        outside.update(tether[1:])
                        arms.append(arm)
                        groups.append(set(arm))
                    es.update(edge(arms[i][0], arms[j][0]) for i, j in combinations(range(3), 2))
                    groups.append(outside)
                    r = dict(attachment_id=a["id"], root=root, arm_lengths=lengths,
                             external_path=[root, port, f"b{landing}"], edges=sorted(es),
                             branch_sets=[sorted(g) for g in groups])
                    assert validate_minor(r)
                    assert not validate_minor(dict(r, edges=sorted(es - {edge(root, port)})))
                    r["adjacency"] = [dict(pair=[i, j], edge=next(
                        edge(x, y) for x in sorted(groups[i]) for y in sorted(groups[j]) if edge(x, y) in es))
                        for i, j in combinations(range(5), 2)]
                    records.append(r)
    return records


def build():
    abstract, summary, shapes = abstract_audit()
    attachments = attachment_audit()
    local, local_counts, negative = local_audit()
    fixed = fixed_graph_audit()
    minors = minor_audit(attachments)
    cross_rows = cross_row_audit()
    summary.update(local_counts)
    summary.update(actual_K2_support_pairs=len(attachments),
                   alternating_support_exclusions=sum(r["crossing_excluded"] for r in attachments),
                   K5_skeletons=len(minors), cross_row_cases=cross_rows["cases"],
                   full_graph_rows=len(base.ROWS), full_graph_deletions=len(fixed["q_deletion_witnesses"]))
    inputs = ["scripts/c5_adjacent_degree5_interfaces.py", "scripts/c5_adjacent_degree5_shared_singleton.py",
              "scripts/c5_single_spoke_three_one.py", "docs/c5_adjacent_degree5_shared_singleton.md",
              "docs/c5_single_spoke_three_one.md"]
    return dict(schema=1, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                scope="necessary sole-mixed-K2 reduction; unary actual supports and global cyclic order remain open",
                summary=summary, planar_shape_counts=shapes, abstract_relations=abstract,
                actual_K2_supports=attachments, local_controls=local, marginal_negative_control=negative,
                cross_row_conditions=cross_rows, fixed_graph=fixed, minor_skeletons=minors)


def table(result):
    lines = ["# Sole mixed K2: necessary data", "",
             "These are necessary relations and local attachments, not disk realizations.", "",
             "## Unary shapes after the original-path K5 exclusion", "",
             "Counts include ordered missing colors, the small root, and named unary components.", "",
             "| (small t, ports, large t, ports) | Records |", "| --- | ---: |"]
    lines += [f"| `{shape}` | {count} |" for shape, count in result["planar_shape_counts"].items()]
    lines += ["", "## Actual ordered K2 boundary supports", "",
              "Only the two original boundary pairs are classified here; all unary supports remain to be joined.", "",
              "| ID | u support | v support | Missing colors (u,v) | Disk crosscuts | Reflection |",
              "| ---: | --- | --- | --- | --- | ---: |"]
    for r in result["actual_K2_supports"]:
        su, sv = ("".join(map(str, r[k])) for k in ("support_u", "support_v"))
        status = "excluded: alternating" if r["crossing_excluded"] else "necessary candidate"
        lines.append(f"| {r['id']} | {su} | {sv} | {r['missing_u']},{r['missing_v']} | {status} | {r['reflected_id']} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    rendered = table(result)
    if args.check:
        assert OUT.read_bytes() == payload.encode(), "certificate differs"
        assert TABLE.read_bytes() == rendered.encode(), "table differs"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(payload)
        TABLE.write_text(rendered)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
