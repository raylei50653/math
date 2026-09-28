#!/usr/bin/env python3
"""Sole mixed K2 with Pz=(u,v), Pw=(u), retaining the shared u.

Necessary relation data and fixed graph controls are not disk realizations.
The arbitrary-size argument, including its external theorem, is in the report.
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
OUT = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared/observations.json"
TABLE = OUT.with_name("necessary_table.md")
U = frozenset(base.U)


def forbidden(x, y):
    assert len(x) == 3 and len(y) >= 2
    if len(y) != 2 or not y < x:
        return frozenset()
    b = next(iter(x - y))
    return frozenset((a, b) for a in y)


def region_for(i, sv):
    return base.make_region("mixed_uv", [(7, 8)],
                            {7: (base.Z, base.W, i), 8: (base.Z,) + sv})


def allowed(left, right, banned, root_edge=True, mixed=True):
    return (set(product(left, right)) - (base.DELTA if root_edge else set())
            - (banned if mixed else set()))


def sides(mixed_ports):
    result = []
    for spokes in unary.subsets({0, 1, 2}):
        n = 4 - mixed_ports - len(spokes)
        if n < 0:
            continue
        for ports in unary.PARTITIONS[n]:
            choices = [[f for f in unary.subsets(U) if 0 < len(f) <= k] for k in ports]
            for bans in product(*choices):
                result.append((U - spokes, ports, bans))
    return result


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


def normal_form(left, right, h, d):
    if h == d:
        return False
    e = next(iter({0, 1, 2} - {h, d}))
    z_ok = (left[0] == U and left[1] == (2,)
            and left[2][0] in ({h}, {h, d}, {h, 3}))
    a, ports, bans = right
    w_ok = (e in a and unary.union(bans) == a - {e}
            and sum(map(len, bans)) == len(a - {e})
            and all(len(f) == k for f, k in zip(bans, ports)))
    return z_ok and w_ok


def schemas_for(ban):
    """All two-contact schemas with exact intersection and port-release witnesses."""
    candidates = [p for p in sorted(base.PAIRS) if ban <= set(p)]
    result = []
    for bits in range(1, 1 << len(candidates)):
        relation = [p for i, p in enumerate(candidates) if bits >> i & 1]
        if set.intersection(*(set(p) for p in relation)) != set(ban):
            continue
        if all(any(p[j] == c and p[1-j] != c for p in relation)
               for c in ban for j in range(2)):
            result.append(relation)
    return result


def abstract_audit():
    lefts, rights = sides(2), sides(1)
    records, shapes, count = [], Counter(), 0
    for h, d in product(range(3), repeat=2):
        banned = forbidden(U - {h}, frozenset({d, 3}))
        for left, right in product(lefts, rights):
            direct = direct_minimality(left, right, banned)
            assert direct == normal_form(left, right, h, d), (h, d, left, right)
            count += 1
            if not direct:
                continue
            e = next(iter({0, 1, 2} - {h, d}))
            retained = right[1] != (3,)
            ez = unary.residual(left)
            assert allowed(ez, {e}, banned, root_edge=False) == {(e, e)}
            assert allowed(ez, {e}, banned, mixed=False) == set(product(ez - {e}, {e}))
            assert allowed(U, {e}, banned) == {(h, e)}
            for j, f in enumerate(right[2]):
                assert allowed(ez, unary.residual(right, j), banned) == set(product(ez, f)) - base.DELTA
            for c in U - right[0]:
                assert allowed(ez, {c}, banned) == set(product(ez - {c}, {c}))
            shape = str((len(U - right[0]), right[1]))
            if retained:
                shapes[shape] += 1
            records.append(dict(id=len(records), h=h, d=d, e=e,
                                z=unary.encode_side(left), w=unary.encode_side(right),
                                planar_necessary_retained=retained,
                                w_contact_relations=([sorted(permutations(sorted(f))) for f in right[2]]
                                                     if retained else None),
                                z_schema_count=len(schemas_for(left[2][0]))))
    schemas = {str(h): schemas_for({h}) for h in range(3)}
    pair_schemas = {str(pair): schemas_for(set(pair)) for pair in combinations(base.U, 2)}
    assert all(len(s) == 95 for s in schemas.values())
    assert all(len(schemas_for({h, c})) == 1 for h in range(3) for c in U - {h})
    assert len(records) == 306
    retained = [r for r in records if r["planar_necessary_retained"]]
    assert len(retained) == 288
    return records, dict(singleton=schemas, pair=pair_schemas), dict(sorted(shapes.items())), dict(
        z_side_candidates=len(lefts), w_side_candidates=len(rights),
        minimality_comparisons=count, abstract_records=len(records),
        planar_necessary_records=len(retained),
        expanded_q_relation_schemas=sum(r["z_schema_count"] for r in retained))


def local_audit():
    records, attachments, counts = [], [], Counter()
    for i, sv in product(range(5), combinations(range(5), 2)):
        region = region_for(i, sv)
        assert region["ports_z"] == (7, 8) and region["ports_w"] == (7,)
        transcript, canonical = [], []
        for row in base.ROWS:
            x, y = U - {row[i]}, U - {row[j] for j in sv}
            actual, ports, tuples = base.joint_interface(region, row)
            assert ports == (7, 8)
            banned = forbidden(x, y)
            assert actual == base.PAIRS - banned
            assert base.DELTA <= actual
            transcript.append([row, base.mask(actual)])
            counts["actual_attachment_row_checks"] += 1
            if row not in base.CANONICAL:
                continue
            canonical.append(dict(row=row, lists=[sorted(x), sorted(y)],
                                  tuples=sorted(tuples), forbidden=sorted(banned)))
            for a, b in sorted(base.PAIRS):
                fixed = dict(enumerate(row)) | {base.Z: a, base.W: b}
                f = base.first_coloring(tuple(range(9)), region["edges"], fixed)
                assert (f is not None) == ((a, b) in actual)
                counts["independent_pinned_queries"] += 1
                for cut in sorted(region["edges"]):
                    f = base.first_coloring(tuple(range(9)), region["edges"] - {cut}, fixed)
                    assert f is not None
                    if (a, b) in banned:
                        assert f[cut[0]] == f[cut[1]]
                        counts["deleted_endpoint_forcing_checks"] += 1
                    counts["independent_deletion_queries"] += 1
            for sigma in permutations(base.U):
                moved = tuple(sigma[c] for c in row)
                assert base.joint_interface(region, moved)[0] == frozenset(
                    (sigma[a], sigma[b]) for a, b in actual)
                counts["common_frame_checks"] += 1
        records.append(dict(support_u=[i], support_v=sv, edges=sorted(region["edges"]),
                            canonical_rows=canonical,
                            all_rows_sha256=sha256(json.dumps(transcript).encode()).hexdigest()))
        f = forbidden(U - {base.Q[i]}, U - {base.Q[j] for j in sv})
        if f:
            h = base.Q[i]
            e = next(iter({base.Q[j] for j in sv} - {h}))
            d = next(iter({0, 1, 2} - {h, e}))
            attachments.append(dict(id=len(attachments), support_u=[i], support_v=sv,
                                    h=h, e=e, d=d, forbidden=sorted(f)))
    lookup = {(r["support_u"][0], tuple(r["support_v"])): r for r in attachments}
    pi = (1, 0, 2, 3)
    rho = lambda i: (3 - i) % 5
    for r in attachments:
        reflected = lookup[(rho(r["support_u"][0]), tuple(sorted(rho(j) for j in r["support_v"])))]
        assert all(reflected[k] == pi[r[k]] for k in ("h", "e", "d"))
        r["reflected_id"] = reflected["id"]
    assert len(attachments) == 28
    # A fake product of endpoint marginals introduces the unavailable tuple (3,3).
    x, y = frozenset({1, 2, 3}), frozenset({2, 3})
    tuples = sorted(set(product(x, y)) - base.DELTA)
    marginal = sorted(product({s for s, _ in tuples}, {t for _, t in tuples}))
    assert not any(s not in {2, 1} and t != 2 for s, t in tuples)
    assert any(s not in {2, 1} and t != 2 for s, t in marginal)
    # Splitting common u into independent z/w copies also wrongly accepts (2,1).
    assert any(s != 2 and t != 2 for s, t in tuples)
    assert any(s != 1 for s, _ in tuples)
    # Deleting zu must keep wu. The false witness u=w=1 violates that retained edge.
    region = region_for(0, (0, 1))
    bad = dict(enumerate(base.Q)) | {base.Z: 2, base.W: 1, 7: 1, 8: 3}
    assert all(bad[a] != bad[b] for a, b in region["edges"] - {base.edge(5, 7), base.edge(6, 7)})
    assert bad[6] == bad[7]
    negative = dict(lists=[sorted(x), sorted(y)], tuples=tuples, marginal_product=marginal,
                    falsely_accepted_root_pair=[2, 1],
                    deleting_zu_must_retain_wu=dict(coloring=[bad[v] for v in range(9)], retained_edge=[6, 7]))
    return records, attachments, dict(counts), negative


def cross_row_audit():
    residual_z = [s for s in unary.subsets(U) if len(s) >= 2]
    residual_w = [s for s in unary.subsets(U) if s]
    cases = 0
    for h in U:
        for y in [s for s in unary.subsets(U) if len(s) in (2, 3)]:
            x = U - {h}
            f = forbidden(x, y)
            for ez, ew in product(residual_z, residual_w):
                reject = not allowed(ez, ew, f)
                predicted = False
                if f:
                    e = next(iter(x - y))
                    predicted = ew == {e} and ez <= x
                assert reject == predicted
                cases += 1
    return dict(cases=cases, scope="same-source row-specific E_z has at least two colors")


def fixed_graph_audit():
    records = []
    # h=0,e=1,d=2. Three different actual z regions realize all three q ban forms.
    z_regions = [
        base.make_region("z_ban_h", [(9, 10), (9, 11), (10, 11)],
                         {9: (base.Z, 1), 10: (base.Z, 1), 11: (0, 1)}),
        base.make_region("z_ban_hd", [(9, 10), (9, 11), (10, 12)],
                         {9: (base.Z, 1), 10: (base.Z, 1), 11: (0, 1, 4), 12: (0, 1, 4)}),
        base.make_region("z_ban_h3", [(9, 10)],
                         {9: (base.Z, 1, 4), 10: (base.Z, 1, 4)}),
    ]
    for zregion, expected in zip(z_regions, ({0}, {0, 2}, {0, 3})):
        last = max(zregion["vertices"]) + 1
        regions = [region_for(0, (0, 1)), zregion,
                   base.make_region("w_single", [], {last: (base.W, 0, 1, 4)})]
        edges = (base.CYCLE | {base.edge(base.Z, base.W), base.edge(base.W, 0), base.edge(base.W, 4)}
                 | unary.union([r["edges"] for r in regions]))
        vertices = tuple(range(last + 1))
        assert [sum(v in e for e in edges) for v in vertices[5:]] == [5, 5] + [4] * (last - 6)
        ztuples = base.joint_interface(zregion, base.Q)[2]
        assert set.intersection(*(set(t) for t in ztuples)) == expected
        assert not base.whole_pairs(vertices, edges, base.Q)
        witnesses, transcript, canonical = [], [], []
        for cut in sorted(edges - base.CYCLE):
            f = base.first_coloring(vertices, edges - {cut}, dict(enumerate(base.Q)))
            assert f is not None and f[cut[0]] == f[cut[1]]
            witnesses.append(dict(edge=cut, coloring=[f[v] for v in vertices]))
        for row in base.ROWS:
            local = [base.joint_interface(r, row) for r in regions]
            actual = base.whole_pairs(vertices, edges, row)
            assert actual == base.glued_pairs(regions, [t[0] for t in local], edges, row, frozenset())
            transcript.append([row, base.mask(actual)])
            if row in base.CANONICAL:
                canonical.append(dict(row=row, root_pairs=sorted(actual),
                                      local_tuples=[dict(name=r["name"], ports=t[1], tuples=sorted(t[2]))
                                                    for r, t in zip(regions, local)]))
        records.append(dict(name=zregion["name"], z_forbidden=sorted(expected), vertices=vertices,
                            edges=sorted(edges), q_deletion_witnesses=witnesses, canonical_rows=canonical,
                            all_rows_sha256=sha256(json.dumps(transcript).encode()).hexdigest(),
                            scope="actual minimal q-core; disk and T4 not certified"))
    return records


def minor_audit(attachments):
    records = []
    for r in attachments:
        i = r["support_u"][0]
        for lengths in ((0, 0, 0), (1, 3, 1), (2, 2, 2)):
            es = {edge(f"b{k}", f"b{(k+1)%5}") for k in range(5)}
            es.update(edge(a, b) for a, b in (("z", "w"), ("z", "u"), ("z", "v"),
                                            ("w", "u"), ("u", "v"), ("u", f"b{i}")))
            es.update(edge("v", f"b{j}") for j in r["support_v"])
            groups, arms, outside = [{"w"}], [], {"u"} | {f"b{k}" for k in range(5)}
            for k, length in enumerate(lengths):
                arm = [f"a{k}_{j}" for j in range(length + 1)]
                es.update(edge(a, b) for a, b in zip(arm, arm[1:]))
                es.add(edge("w", arm[-1]))
                tether = [arm[0], f"t{k}", f"b{(i+k)%5}"] if length else [arm[0], f"b{(i+k)%5}"]
                es.update(edge(a, b) for a, b in zip(tether, tether[1:]))
                outside.update(tether[1:])
                arms.append(arm)
                groups.append(set(arm))
            es.update(edge(arms[a][0], arms[b][0]) for a, b in combinations(range(3), 2))
            groups.append(outside)
            record = dict(attachment_id=r["id"], arm_lengths=lengths, external_path=["w", "u", f"b{i}"],
                          edges=sorted(es), branch_sets=[sorted(g) for g in groups])
            assert validate_minor(record)
            assert not validate_minor(dict(record, edges=sorted(es - {edge("w", "u")})))
            record["adjacency"] = [dict(pair=[a, b], edge=next(
                edge(x, y) for x in sorted(groups[a]) for y in sorted(groups[b]) if edge(x, y) in es))
                for a, b in combinations(range(5), 2)]
            records.append(record)
    return records


def build():
    abstract, schemas, shapes, summary = abstract_audit()
    local, attachments, counts, negative = local_audit()
    fixed, cross = fixed_graph_audit(), cross_row_audit()
    minors = minor_audit(attachments)
    summary.update(counts)
    summary.update(actual_K2_supports=len(attachments), cross_row_cases=cross["cases"],
                   K5_skeletons=len(minors), full_graph_rows=len(fixed) * len(base.ROWS),
                   full_graph_deletions=sum(len(g["q_deletion_witnesses"]) for g in fixed))
    inputs = ["scripts/c5_adjacent_degree5_interfaces.py", "scripts/c5_adjacent_degree5_shared_singleton.py",
              "scripts/c5_single_spoke_three_one.py", "docs/c5_adjacent_degree5_shared_singleton.md",
              "docs/c5_single_spoke_three_one.md", "docs/c5_single_spoke_two_two.md"]
    return dict(schema=1, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                scope="necessary shared-endpoint K2 reduction; unary supports, cyclic order and separation remain open",
                summary=summary, planar_w_shape_counts=shapes, abstract_relations=abstract,
                two_contact_schemas=schemas, actual_K2_supports=attachments, local_controls=local,
                negative_controls=negative, cross_row_conditions=cross, fixed_graphs=fixed, minor_skeletons=minors)


def table(result):
    lines = ["# Shared-endpoint mixed K2: necessary relations", "",
             "Pz=(u,v), Pw=(u). These are necessary data, not disk realizations.", "",
             "z has no boundary spoke and one two-contact unary component.", "",
             "| w (spokes, unary ports) | Retained records |", "| --- | ---: |"]
    lines += [f"| `{k}` | {v} |" for k, v in result["planar_w_shape_counts"].items()]
    lines += ["", "## Actual local K2 supports", "",
              "Unary attachments and embedding orders have not been joined to these supports.", "",
              "| ID | u support | v support | (h,e,d) | Reflection |", "| ---: | --- | --- | --- | ---: |"]
    for r in result["actual_K2_supports"]:
        lines.append(f"| {r['id']} | {r['support_u'][0]} | {''.join(map(str, r['support_v']))} | "
                     f"{r['h']},{r['e']},{r['d']} | {r['reflected_id']} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    payload, rendered = json.dumps(result, sort_keys=True, indent=2) + "\n", table(result)
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
