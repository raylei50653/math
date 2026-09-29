#!/usr/bin/env python3
"""No-mixed root residuals, unary capacity, and original exterior paths.

Finite relation controls support the paper reduction. Necessary records and
selected minor subgraphs are not planar/disk source realizations.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

import c5_adjacent_degree5_interfaces as base
from c5_single_spoke_three_one import edge, validate_minor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_adjacent_degree5_no_mixed/observations.json"
TABLE = OUT.with_name("normal_forms.md")
U = frozenset(base.U)
PARTITIONS = {
    0: ((),), 1: ((1,),), 2: ((2,), (1, 1)),
    3: ((3,), (2, 1), (1, 1, 1)),
    4: ((4,), (3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1)),
}


def subsets(xs):
    return [frozenset(c) for k in range(len(xs) + 1)
            for c in combinations(sorted(xs), k)]


def union(sets):
    return frozenset().union(*sets)


def available(spokes, row=base.Q):
    return U - {row[i] for i in spokes}


def residual(side, omitted=None, cut_spoke=None):
    spokes, _, forbidden = side
    return available(tuple(i for i in spokes if i != cut_spoke)) - union(
        f for j, f in enumerate(forbidden) if j != omitted)


def private_colors(forbidden, i):
    return forbidden[i] - union(f for j, f in enumerate(forbidden) if j != i)


def direct_side_minimality(side, common):
    """Actual spoke removals and whole-original-component erasures, other root=c."""
    e = residual(side)
    if set(product(e, {common})) - base.DELTA or common not in e:
        return False
    if any(not (residual(side, omitted=i) - {common}) for i in range(len(side[2]))):
        return False
    return all(residual(side, cut_spoke=i) - {common} for i in side[0])


def side_criterion(side, common):
    spokes, _, forbidden = side
    a = available(spokes)
    return (len({base.Q[i] for i in spokes}) == len(spokes)
            and common in a and union(forbidden) == a - {common}
            and all(private_colors(forbidden, i) for i in range(len(forbidden))))


def normal_form(side, common):
    spokes, ports, forbidden = side
    a = available(spokes)
    assert len(spokes) <= 2 and all(forbidden)
    assert all(f <= a - {common} and len(f) <= k for f, k in zip(forbidden, ports))
    deficiency = sum(k - len(f) for k, f in zip(ports, forbidden))
    overlap = sum(map(len, forbidden)) - len(union(forbidden))
    assert deficiency + overlap == 1
    if overlap:
        assert ports == (2, 2) and all(len(f) == 2 for f in forbidden)
        assert len(forbidden[0] & forbidden[1]) == 1
        kind = "one_overlap"
    else:
        assert deficiency == 1
        assert sum(len(f) < k for f, k in zip(forbidden, ports)) == 1
        kind = "one_capacity_deficit"
    expected = {
        (2, (2,)): (1,), (1, (3,)): (2,), (1, (2, 1)): (1, 1),
        (0, (4,)): (3,), (0, (3, 1)): (2, 1), (0, (2, 1, 1)): (1, 1, 1),
    }
    if ports != (2, 2):
        assert tuple(map(len, forbidden)) == expected[len(spokes), ports]
    elif not overlap:
        assert sorted(map(len, forbidden)) == [1, 2]
    return kind, deficiency, overlap


def encode_side(side, common):
    spokes, ports, forbidden = side
    kind, deficiency, overlap = normal_form(side, common)
    excluded = "three_contacts_two_bans" if 3 in ports else (
        "four_contacts_three_bans" if 4 in ports else None)
    return dict(common=common, root_boundary=spokes, available=sorted(available(spokes)),
                ports=ports, forbidden=[sorted(f) for f in forbidden],
                private=[sorted(private_colors(forbidden, i)) for i in range(len(forbidden))],
                kind=kind, capacity_deficit=deficiency, overlap_excess=overlap,
                planar_exclusion=excluded)


def abstract_audit():
    all_sets = subsets(U)
    rectangle_cases = 0
    for left, right in product(all_sets, repeat=2):
        k = set(product(left, right))
        assert (bool(k) and k <= base.DELTA) == (len(left) == 1 and left == right)
        rejected = not (k - base.DELTA)
        assert rejected == (not left or not right or (len(left) == 1 and left == right))
        rectangle_cases += 1
    records, candidates, checks = [], 0, 0
    for t in range(5):
        for spokes in combinations(range(5), t):
            for ports in PARTITIONS[4 - t]:
                for forbidden in product(*[[f for f in all_sets if len(f) <= k] for k in ports]):
                    side = (spokes, ports, forbidden)
                    candidates += 1
                    for common in U:
                        direct = direct_side_minimality(side, common)
                        assert direct == side_criterion(side, common), (side, common)
                        checks += 1
                        if direct:
                            records.append(dict(id=len(records), **encode_side(side, common)))
    assert candidates == 2502 and len(records) == 149
    joins = [(a["id"], b["id"]) for a, b in product(records, repeat=2) if a["common"] == b["common"]]
    retained = [(i, j) for i, j in joins if not records[i]["planar_exclusion"]
                and not records[j]["planar_exclusion"]]
    two_spoke_frontier = [(i, j) for i, j in retained
                          if len(records[i]["root_boundary"]) == len(records[j]["root_boundary"]) == 2]
    assert len(two_spoke_frontier) == 88
    by_shape = Counter(str((len(r["root_boundary"]), r["ports"], r["kind"])) for r in records)
    # Full source reflection: rho(i)=3-i, with the SAME color permutation on both sides.
    lookup = {(tuple(r["root_boundary"]), r["ports"], tuple(tuple(f) for f in r["forbidden"]), r["common"])
              for r in records}
    pi = (1, 0, 2, 3)
    for r in records:
        reflected = (tuple(sorted((3 - i) % 5 for i in r["root_boundary"])), r["ports"],
                     tuple(tuple(sorted(pi[c] for c in f)) for f in r["forbidden"]), pi[r["common"]])
        assert reflected in lookup
    # Empty F, hidden spoke colors, duplicate coverage, and repeated spoke colors
    # are admitted to the input domain and rejected by the independent deletion test.
    negatives = [
        ("redundant_component", ((), (2, 1, 1), (frozenset({0, 1}), frozenset({2}), frozenset())), 3),
        ("spoke_color_also_banned", ((0,), (3,), (frozenset({0, 1, 2}),)), 3),
        ("component_without_private_color", ((), (2, 1, 1),
                                            (frozenset({0, 1}), frozenset({0}), frozenset({2}))), 3),
        ("repeated_spoke_color", ((0, 2), (2,), (frozenset({1, 2}),)), 3),
    ]
    negative_records = []
    for name, side, common in negatives:
        assert residual(side) == {common} and not direct_side_minimality(side, common)
        negative_records.append(dict(name=name, spokes=side[0], ports=side[1],
                                     forbidden=[sorted(f) for f in side[2]], common=common))
    return records, dict(rectangle_cases=rectangle_cases, side_candidates=candidates,
                         pinned_side_deletion_checks=checks, side_normal_forms=len(records),
                         planar_necessary_sides=sum(not r["planar_exclusion"] for r in records),
                         common_color_joins=len(joins), planar_necessary_joins=len(retained),
                         two_spoke_frontier=len(two_spoke_frontier),
                         side_shapes=dict(sorted(by_shape.items())),
                         reflection_checks=len(records)), dict(
                             joins=joins, retained=retained, two_spoke_frontier=two_spoke_frontier,
                             negative_controls=negative_records)


def fixed_sources():
    triangle_regions = []
    for root, vertices in ((base.Z, (7, 8, 9)), (base.W, (10, 11, 12))):
        a, x, y = vertices
        triangle_regions.append(base.make_region("triangle_" + str(root), list(combinations(vertices, 2)),
                                                {a: (0, 1), x: (root, 0), y: (root, 0)}))
    pair_regions = []
    for root, start in ((base.Z, 7), (base.W, 11)):
        for offset, support in ((0, (1, 4)), (2, (0, 4))):
            u, v = start + offset, start + offset + 1
            pair_regions.append(base.make_region("pair_" + str(u), [(u, v)],
                                                 {u: (root, *support), v: (root, *support)}))
    return [
        ("one_capacity_deficit", tuple(range(13)), triangle_regions,
         {base.edge(r, i) for r in (base.Z, base.W) for i in (0, 4)},
         [[7], [8], [9], [0], [1, 2, 3, 4, 5]]),
        ("one_overlap", tuple(range(15)), pair_regions, set(),
         [[5, 9], [7], [8], [4], [0, 1, 2, 3, 6, 11]]),
    ]


def fixed_audit():
    records, counts = [], Counter()
    for name, vertices, regions, spokes, groups in fixed_sources():
        edges = set(base.CYCLE) | {base.edge(base.Z, base.W)} | spokes | union(r["edges"] for r in regions)
        assert [sum(v in e for e in edges) for v in vertices[5:]] == [5, 5] + [4] * (len(vertices) - 7)
        assert all(bool(r["ports_z"]) != bool(r["ports_w"]) for r in regions)
        assert not base.whole_pairs(vertices, edges, base.Q)
        minor = dict(edges=sorted(edges), branch_sets=groups)
        assert validate_minor(minor)
        deletion_witnesses, q_tuples, canonical, transcript = [], [], [], []
        for row in base.ROWS:
            bans, residuals = {}, {}
            for r in regions:
                relation, ports, tuples = base.joint_interface(r, row)
                root = base.Z if r["ports_z"] else base.W
                allowed_colors = {pair[0 if root == base.Z else 1] for pair in relation}
                f = U - allowed_colors
                assert tuples and f == frozenset.intersection(*(frozenset(t) for t in tuples))
                assert len(f) <= len(ports)
                bans[r["name"]] = f
                if row == base.Q:
                    q_tuples.append(dict(name=r["name"], root=root, vertices=r["vertices"],
                                         edges=sorted(r["edges"]), ports=ports, forbidden=sorted(f),
                                         tuples=[dict(contact=t, coloring=c) for t, c in sorted(tuples.items())]))
                    marginals = [set(t[i] for t in tuples) for i in range(len(ports))]
                    marginal_bans = frozenset.intersection(*(frozenset(t) for t in product(*marginals)))
                    assert marginal_bans != f
                    counts["marginal_product_failures"] += 1
            for root in (base.Z, base.W):
                root_spokes = [i for i in range(5) if base.edge(root, i) in edges]
                port_key = "ports_z" if root == base.Z else "ports_w"
                fs = [bans[r["name"]] for r in regions if r[port_key]]
                residuals[root] = available(root_spokes, row) - union(fs)
            prediction = set(product(residuals[base.Z], residuals[base.W])) - base.DELTA
            direct = base.whole_pairs(vertices, edges, row)
            assert prediction == direct
            transcript.append([row, sorted(residuals[base.Z]), sorted(residuals[base.W]), base.mask(direct)])
            counts["fixed_graph_rows"] += 1
            if row in base.CANONICAL:
                canonical.append(dict(row=row, z_residual=sorted(residuals[base.Z]),
                                      w_residual=sorted(residuals[base.W]), root_pairs=sorted(direct)))
            if row == base.Q:
                assert residuals[base.Z] == residuals[base.W] and len(residuals[base.Z]) == 1
                common = next(iter(residuals[base.Z]))
                for cut in sorted(edges - base.CYCLE):
                    actual = base.whole_pairs(vertices, edges - {cut}, row)
                    if cut == base.edge(base.Z, base.W):
                        expected = {(common, common)}
                    elif cut in spokes:
                        root = base.Z if base.Z in cut else base.W
                        color = row[min(cut)]
                        expected = {(color, common)} if root == base.Z else {(common, color)}
                    else:
                        r = next(r for r in regions if cut in r["edges"])
                        root = base.Z if r["ports_z"] else base.W
                        others = [bans[s["name"]] for s in regions if s != r and bool(s["ports_z"]) == bool(r["ports_z"])]
                        private = bans[r["name"]] - union(others)
                        expected = set(product(private, {common})) if root == base.Z else set(product({common}, private))
                        erased = base.joint_interface(r, row, frozenset({cut}))[0]
                        assert erased == base.PAIRS
                    assert actual == expected and actual
                    witnesses = []
                    for a, b in sorted(actual):
                        coloring = base.first_coloring(vertices, edges - {cut},
                                                      dict(enumerate(row)) | {base.Z: a, base.W: b})
                        assert coloring and coloring[cut[0]] == coloring[cut[1]]
                        assert all(coloring[u] != coloring[v] for u, v in edges - {cut})
                        witnesses.append(dict(pair=(a, b), coloring=[coloring[v] for v in vertices]))
                        counts["fixed_deletion_pair_witnesses"] += 1
                    deletion_witnesses.append(dict(edge=cut, pairs=sorted(actual), witnesses=witnesses))
                    counts["fixed_edge_deletions"] += 1
        records.append(dict(name=name, vertices=vertices, edges=sorted(edges), common=common,
                            q_full_contact_relations=q_tuples, canonical_rows=canonical,
                            all_rows_sha256=sha256(json.dumps(transcript).encode()).hexdigest(),
                            q_deletions=deletion_witnesses, K5_minor=minor,
                            scope="genuine nonplanar minimal q-core; not a disk or T4 control"))
    assert {r["common"] for r in records} == {2, 3}
    return records, dict(counts)


def minor_audit():
    records = []
    for target, length, long_tether in product(range(5), (1, 3), (False, True)):
        qpath = ["z", "w"] + [f"outside_{i}" for i in range(length - 1)] + [f"b{target}"]
        for kind in ("k4", "three_contacts", "four_contacts"):
            cases = range(16) if kind == "k4" else range(3) if kind == "three_contacts" else range(1)
            for case in cases:
                es = {edge(f"b{i}", f"b{(i + 1) % 5}") for i in range(5)}
                es.update(edge(a, b) for a, b in zip(qpath, qpath[1:]))
                hub = {f"b{i}" for i in range(5)} | set(qpath[1:])
                arms, tethers = [], []
                if kind == "k4":
                    core = [f"v{i}" for i in range(4)]
                    es.update(edge(a, b) for a, b in combinations(core, 2))
                    hub.add("z")
                    groups = [{v} for v in core] + [hub]
                else:
                    core = ["a", "b", "x"]
                    es.update(edge(a, b) for a, b in combinations(core, 2))
                    groups = [{"z"}] + [{v} for v in core] + [hub]
                    if kind == "three_contacts":
                        lengths = ((0, 0, 0), (2, 0, 2), (1, 3, 1))[case]
                        for i, (v, n) in enumerate(zip(core, lengths)):
                            arm = [v] + [f"arm{i}_{j}" for j in range(n)]
                            es.update(edge(a, b) for a, b in zip(arm, arm[1:]))
                            es.add(edge("z", arm[-1]))
                            groups[i + 1].update(arm)
                            arms.append(arm)
                    else:
                        es.update(edge(a, b) for a, b in combinations(("c", "d", "y"), 2))
                        es.add(edge("x", "y"))
                        es.update(edge("z", v) for v in ("a", "b", "c", "d"))
                        groups[0].update(("c", "d", "y"))
                for i, v in enumerate(core):
                    endpoint = "z" if kind == "k4" and case & (1 << i) else f"b{(target + i) % 5}"
                    path = [v] + ([f"tether{i}_0", f"tether{i}_1"] if long_tether else []) + [endpoint]
                    es.update(edge(a, b) for a, b in zip(path, path[1:]))
                    hub.update(path[1:])
                    tethers.append(path)
                witness = dict(edges=sorted(es), branch_sets=[sorted(g) for g in groups])
                assert validate_minor(witness)
                assert not validate_minor(dict(witness, edges=sorted(es - {edge("z", "w")})))
                adjacency = [dict(pair=[i, j], original_edge=next(edge(a, b) for a in sorted(groups[i])
                             for b in sorted(groups[j]) if edge(a, b) in es)) for i, j in combinations(range(5), 2)]
                records.append(dict(id=len(records), kind=kind, outside_path=qpath,
                                    arms=arms, tethers=tethers, **witness, ten_adjacencies=adjacency))
    assert len(records) == 400
    return records


def build():
    sides, summary, abstract = abstract_audit()
    fixed, counts = fixed_audit()
    minors = minor_audit()
    summary.update(counts)
    summary.update(K5_selected_subgraphs=len(minors), deleted_zw_witness_failures=len(minors),
                   target_separation_queries=0)
    inputs = ["scripts/c5_adjacent_degree5_interfaces.py", "scripts/c5_single_spoke_three_one.py",
              "docs/c5_no_spoke_exterior.md", "docs/c5_single_spoke_three_one.md",
              "docs/c5_single_spoke_four.md"]
    return dict(schema=1, source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                scope="exact same-source reduction; necessary forms and selected minors are not disk realizations",
                summary=summary, side_normal_forms=sides, abstract_conditions=abstract,
                fixed_sources=fixed, original_path_minors=minors)


def render(result):
    lines = ["# 無 mixed 型：具名 root-spoke 與 unary 禁色正常形", "",
             "這是 q 必要資料，沒有指定 unary 的實際支援／環序，也不是來源圖實現。",
             "z、w 必使用同一個 c；同接點數的各欄仍是不同具名原分量。", "",
             "| ID | c | root 的 boundary 鄰點 | 接點分拆 | 各原分量 F | 私有色 | 平面必要篩選 |",
             "| ---: | ---: | --- | --- | --- | --- | --- |"]
    for r in result["side_normal_forms"]:
        lines.append(f'| {r["id"]} | {r["common"]} | {list(r["root_boundary"])} | {list(r["ports"])} | '
                     f'{r["forbidden"]} | {r["private"]} | {r["planar_exclusion"] or "保留，未證實現"} |')
    lines += ["", "完整接合數及證書見 [JSON](observations.json)；一般證明與界線見",
              "[研究報告](../../docs/c5_adjacent_degree5_no_mixed.md)。", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    for path, payload in ((OUT, json.dumps(result, sort_keys=True, indent=2) + "\n"), (TABLE, render(result))):
        if args.check:
            assert path.read_bytes() == payload.encode(), f"certificate differs: {path}"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
