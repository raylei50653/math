#!/usr/bin/env python3
"""Shared-endpoint mixed K2, t_w=0 and (2,1): source K5 and targets.

Arbitrary-size support, annulus and bridge coverage is supplied by the report.
The records and minor skeletons do not certify disk realizability or Lean proofs.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_mixed_edge_shared import allowed, forbidden, schemas_for
from c5_adjacent_degree5_mixed_edge_shared_t1_pair import DIAMOND, stable, stable_schema_ids
from c5_adjacent_degree5_singleton_long_arc import component_options
from c5_single_spoke_cores import Q, U, PERMS, PI, RHO, TARGETS
from c5_single_spoke_two_two_minor import residual_audit, support_audit, verify_minor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared_t0_pair_single/observations.json"
TABLE = OUT.with_name("support_table.md")
NAMES = ("Cz", "Cwp", "Cws", "u", "v")
ARITIES = (2, 2, 1)


def cardinality(name, support):
    return (len(support) >= 2 if name.startswith("C") else
            len(support) == 2 if name == "v" else len(support) == 1)


def geometries():
    """Ordered actual support lifts; allow gaps and shared boundary endpoints."""
    choices = {k: tuple(s for n in range(1, 6) for s in combinations(range(6), n)
                        if cardinality(k, s) and max(s) - min(s) < 5) for k in NAMES}
    result = {}
    for w_order in permutations(("Cwp", "Cws")):
        forward = ("Cz",) + w_order + ("u", "v")
        for reverse in (False, True):
            order = ("Cz",) + tuple(reversed(forward[1:])) if reverse else forward

            def visit(j, end, assigned):
                if j == len(NAMES):
                    for anchor in range(5):
                        supports = tuple(tuple(sorted((anchor + i) % 5 for i in assigned[k]))
                                         for k in NAMES)
                        placement = dict(order=order, anchor=anchor,
                                         lifts={k: tuple(anchor + i for i in assigned[k]) for k in NAMES})
                        result.setdefault(supports, []).append(placement)
                    return
                name = order[j]
                for support in choices[name]:
                    if min(support) >= end and (j or min(support) == 0):
                        visit(j + 1, max(support), assigned | {name: support})
            visit(0, 0, {})
    return result


def independent_geometries():
    """Disjoint cyclic hull edge masks, then the combined w interval."""
    def hulls(name):
        for n in range(1, 6):
            for support in combinations(range(5), n):
                if not cardinality(name, support):
                    continue
                for start in support:
                    span = max((i - start) % 5 for i in support)
                    mask = sum(1 << ((start + j) % 5) for j in range(span))
                    yield support, start, span, mask

    found = set()
    cs, vs = tuple(hulls("Cz")), tuple(hulls("v"))
    for z in cs:
        for p in cs:
            if z[3] & p[3]:
                continue
            for s in cs:
                used = z[3] | p[3]
                if used & s[3]:
                    continue
                for v in vs:
                    if (used | s[3]) & v[3]:
                        continue
                    a, b, d = ((c[1] - z[1]) % 5 for c in (p, s, v))
                    ae, be, de = a + p[2], b + s[2], d + v[2]
                    if max(ae, be, de) > 5:
                        continue
                    lo, hi = min(a, b), max(ae, be)
                    for u in range(6):
                        if (z[2] <= lo <= hi <= u <= d <= de <= 5 or
                                z[2] <= d <= de <= u <= lo <= hi <= 5):
                            found.add((z[0], p[0], s[0], ((u + z[1]) % 5,), v[0]))
    return found


def source_key(r):
    return tuple(r[k] for k in ("h", "e", "d")) + (
        tuple(r["z"]["forbidden"][0]), tuple(r["w"]["forbidden"][0]),
        r["w"]["forbidden"][1][0])


def bind_sources(inherited):
    records = [r for r in inherited["abstract_relations"]
               if r["w"]["ports"] == [2, 1] and not r["w"]["spokes_colors"]]
    reconstructed = set()
    for h, e, d in permutations(range(3)):
        for fz, c in product(((h,), tuple(sorted((h, d))), tuple(sorted((h, 3)))), sorted(U - {e})):
            reconstructed.add((h, e, d, fz, tuple(sorted(U - {e, c})), c))
    assert len(records) == len(reconstructed) == 54
    assert {source_key(r) for r in records} == reconstructed
    for r in records:
        assert r["planar_necessary_retained"] and r["z"]["ports"] == [2]
        assert not r["z"]["spokes_colors"] and r["w"]["residual"] == [r["e"]]
        pair, single = r["w"]["forbidden"]
        assert r["w_contact_relations"] == [[list(p) for p in permutations(pair)], [single]]
        assert len(schemas_for(set(r["z"]["forbidden"][0]))) == r["z_schema_count"]
    return records


def compatible(r, supports):
    cz, cp, cs, u, v = supports
    return (Q[u[0]] == r["h"] and {Q[i] for i in v} == {r["h"], r["e"]}
            and all(len({Q[i] for i in t}) >= 2 for t in (cz, cp, cs))
            and all(stable(t, tuple(f)) for t, f in
                    zip((cz, cp, cs), r["z"]["forbidden"] + r["w"]["forbidden"])))


@lru_cache(None)
def local_colorings(supports, row):
    """One z,w,u,v coloring, retaining zw, wu, uv, vz and chord zu."""
    _, _, _, bu, bv = supports
    result = {}
    for a, b, s, t in product(range(4), repeat=4):
        if (a != b and s not in {a, b, t, row[bu[0]]}
                and t not in {a, row[bv[0]], row[bv[1]]}):
            result.setdefault((a, b), (a, b, s, t))
    return result


def row_evidence(r, supports, row):
    components = tuple(component_options(arity, support, tuple(f), row)
                       for arity, support, f in zip(ARITIES, supports[:3],
                                                   r["z"]["forbidden"] + r["w"]["forbidden"]))
    _, _, _, bu, bv = supports
    x, y = U - {row[bu[0]]}, U - {row[i] for i in bv}
    banned, direct = forbidden(x, y), local_colorings(supports, row)
    joins, common = [], set(direct)
    for fz, fp, fs in product(*(c["options"] for c in components)):
        ez, ew = U - set(fz), U - set(fp) - set(fs)
        assert len(ez) >= 2 and ew
        pairs = allowed(ez, ew, banned)
        assert {p for p in direct if p[0] not in fz and p[1] not in fp and p[1] not in fs} == pairs
        assert (not pairs) == (bool(banned) and ew == x - y and ez <= x)
        common &= pairs
        joins.append(dict(forbidden_sets=(fz, fp, fs), residuals=(sorted(ez), sorted(ew)),
                          local_witness_zwuv=direct[min(pairs)] if pairs else None))
    outcomes = {j["local_witness_zwuv"] is not None for j in joins}
    return dict(row=row, components=components, mixed_lists=(sorted(x), sorted(y)),
                mixed_forbidden=sorted(banned), joins=joins,
                uniform_local_witness_zwuv=direct[min(common)] if common else None,
                status="accept" if outcomes == {True} else
                "reject" if outcomes == {False} else "unresolved")


def diamond_edges(supports):
    _, _, _, u, v = supports
    edges = list(DIAMOND) + [("u", f"b{u[0]}")] + [("v", f"b{i}") for i in v]
    return {tuple(sorted(e)) for e in edges}


def external_routes(supports, root, pair):
    """Only original diamond and u/v attachments; neither root has a spoke."""
    edges, result = diamond_edges(supports), []

    def visit(path):
        v = path[-1]
        if v.startswith("b"):
            if int(v[1:]) not in pair:
                result.append(tuple(path))
            return
        neighbors = {b if a == v else a for a, b in edges if v in (a, b)}
        for w in sorted(neighbors - set(path)):
            visit(path + [w])
    visit([root])
    return sorted(result, key=lambda p: (len(p), p))


def source_exclusions(r, supports):
    result = []
    for k, root in enumerate(("z", "w")):
        f = set(r[root]["forbidden"][0])
        if len(f) != 2:
            continue
        required = U - f if 3 in f else f
        suppliers = [[i for i in supports[k] if Q[i] == c] for c in sorted(required)]
        if not all(len(s) == 1 for s in suppliers):
            continue
        pair = tuple(sorted(s[0] for s in suppliers))
        if (pair[0] - pair[1]) % 5 not in (1, 4):
            continue
        routes = external_routes(supports, root, pair)
        if routes:
            result.append(dict(component=NAMES[k], root=root, forbidden=sorted(f),
                               required_colors=sorted(required), forced_pair=pair,
                               complement_arc=sorted(set(range(5)) - set(pair)),
                               original_external_routes=routes, chosen_route=routes[0]))
    return result


def contact_words(placement):
    result = []
    for flips in product((False, True), repeat=2):
        expansion = dict(Cz=("zx0", "zx1"), Cwp=("wy0", "wy1"), Cws=("wt",),
                         u=("u_boundary",), v=("v_boundary_first", "v_boundary_last"))
        for name, flip in zip(NAMES[:2], flips):
            if flip:
                expansion[name] = tuple(reversed(expansion[name]))
        result.append(tuple(edge for unit in placement["order"] for edge in expansion[unit]))
    return result


def minor_control(supports, witness, length=1, index=0, shared=False):
    """Retain all three named unary units; skeleton only, no degree/list claim."""
    assert length % 2 == 1 and 0 <= index < length
    root, pair, route = witness["root"], witness["forced_pair"], witness["chosen_route"]
    subject = NAMES.index(witness["component"])
    edges = diamond_edges(supports)

    def edge(a, b):
        edges.add(tuple(sorted((a, b))))

    for i in range(5):
        edge(f"b{i}", f"b{(i+1) % 5}")
    path = [f"x{i}" for i in range(length + 1)]
    for a, b in zip([root] + path, path + [root]):
        edge(a, b)
    for k, (name, arity) in enumerate(zip(NAMES, ARITIES)):
        if k == subject:
            continue
        r = "z" if k == 0 else "w"
        nodes = [f"{name}{j}" for j in range(arity)]
        for node in nodes:
            edge(r, node)
        if arity == 2:
            edge(*nodes)
        for b in supports[k]:
            edge(nodes[0], f"b{b}")
    bags, tethers = [], []
    for x in path:
        bag = {x}
        tether = x + "_t" if shared else x
        if shared:
            edge(x, tether)
            bag.add(tether)
        for b in pair:
            edge(tether, f"b{b}")
        if x in path[index:index+2]:
            bags.append(bag)
            tethers.append([(tether, f"b{b}") for b in pair])
    for b in supports[subject]:
        edge("x0_t" if shared else "x0", f"b{b}")
    outside = (set(path) - set(path[index:index+2])) | set(route)
    outside |= {f"b{i}" for i in witness["complement_arc"]}
    bags += [outside, {f"b{pair[0]}"}, {f"b{pair[1]}"}]
    assert all(tuple(sorted(e)) in diamond_edges(supports) for e in zip(route, route[1:]))
    assert not any(a.startswith("b") and b in ("z", "w") for a, b in edges)
    return dict(length=length, index=index, shared_tether=shared, original_external_route=route,
                edges=sorted(edges), branch_sets=[sorted(b) for b in bags], tethers=tethers,
                adjacencies=verify_minor(edges, bags), scope="topology skeleton; not a degree-list source")


def reflection_control(records, abstract):
    lookup = {(r["source_id"], r["supports"]): r for r in records}
    sources = {source_key(r): r for r in abstract}
    for r in records:
        h, e, d, fz, fp, c = source_key(r["source_record"])
        src = sources[(PI[h], PI[e], PI[d], tuple(sorted(PI[a] for a in fz)),
                       tuple(sorted(PI[a] for a in fp)), PI[c])]
        supports = tuple(tuple(sorted(RHO[i] for i in s)) for s in r["supports"])
        other = lookup[src["id"], supports]
        r["reflected_id"] = other["id"]
        assert bool(r["source_K5"]) == bool(other["source_K5"])
        for w in r["source_K5"]:
            moved = next(a for a in other["source_K5"] if a["component"] == w["component"])
            assert moved["forced_pair"] == tuple(sorted(RHO[i] for i in w["forced_pair"]))
            assert set(moved["original_external_routes"]) == {
                tuple(f"b{RHO[int(v[1:])]}" if v.startswith("b") else v for v in p)
                for p in w["original_external_routes"]}
        r["reflected_targets"] = []
        for before in r["targets"]:
            row = tuple(PI[before["row"][RHO[i]]] for i in range(5))
            after = row_evidence(src, supports, row)
            assert after["status"] == before["status"]
            for old, new in zip(before["components"], after["components"]):
                assert sorted(tuple(sorted(PI[c] for c in f)) for f in old["options"]) == sorted(new["options"])
            r["reflected_targets"].append(dict(raw_row=row, status=after["status"]))
    assert all(records[r["reflected_id"]]["reflected_id"] == r["id"] for r in records)


def frame_control(records):
    checks = Counter()
    for r in records:
        for ev in r["targets"]:
            for join in ev["joins"]:
                if join["local_witness_zwuv"] is None:
                    continue
                for sigma in PERMS:
                    row = tuple(sigma[c] for c in ev["row"])
                    a, b, s, t = (sigma[c] for c in join["local_witness_zwuv"])
                    fz, fp, fs = ({sigma[c] for c in f} for f in join["forbidden_sets"])
                    _, _, _, bu, bv = r["supports"]
                    assert a not in fz and b not in fp and b not in fs and a != b
                    assert s not in {a, b, t, row[bu[0]]}
                    assert t not in {a, row[bv[0]], row[bv[1]]}
                    checks["all"] += 1
                    if not r["source_K5"]:
                        checks["retained"] += 1
    return checks


def negative_controls(base, witness):
    edges, bags = set(map(tuple, base["edges"])), list(map(set, base["branch_sets"]))
    pair = witness["forced_pair"]
    broken_outside = {e for e in edges if not (e[0].startswith("b") and e[1] in ("u", "v")
                                              and int(e[0][1:]) in witness["complement_arc"])}
    rejected = []
    for name, es, bs in (
        ("missing_tether", edges - {tuple(sorted((f"b{pair[0]}", "x1")))}, bags),
        ("missing_original_bridge", edges - {("x0", "x1")}, bags),
        ("missing_frame_pair_edge", edges - {(f"b{pair[0]}", f"b{pair[1]}")}, bags),
        ("overlapping_branch_sets", edges, [bags[0] | {witness["root"]}] + bags[1:]),
        ("missing_diamond_to_complement_connection", broken_outside, bags),
    ):
        try:
            verify_minor(es, bs)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    # A repeated supplier cannot be replaced by a selected named frame vertex.
    synthetic = dict(z=dict(forbidden=[[0]]), w=dict(forbidden=[[2, 3], [0]]))
    assert source_exclusions(synthetic, ((0, 1), (0, 2, 3, 4), (0, 1), (2,), (2, 3))) == []
    rejected.append("nonunique_supplier_is_not_a_forced_pair")
    return rejected


def build():
    inherited = json.loads(SOURCE.read_text())
    assert sha256((ROOT / "scripts/c5_adjacent_degree5_mixed_edge_shared.py").read_bytes()).hexdigest() == inherited["source_sha256"]
    for path, expected in inherited["inputs_sha256"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    abstract, geometry = bind_sources(inherited), geometries()
    assert set(geometry) == independent_geometries()
    assert len(geometry) == sum(map(len, geometry.values())) == 240
    positive = ((0, 1), (1, 2), (2, 3), (3,), (3, 4))
    interleaved = ((0, 1), (1, 2, 3), (2, 4), (4,), (0, 4))
    assert positive in geometry and interleaved not in geometry
    assert any(len(s) < max(p["lifts"][k]) - min(p["lifts"][k]) + 1
               for ss, ps in geometry.items() for p in ps for k, s in zip(NAMES, ss))
    local_ids = {(tuple(r["support_u"]), tuple(r["support_v"])): r
                 for r in inherited["actual_K2_supports"]}
    records, geometry_records = [], []
    for supports, placements in sorted(geometry.items()):
        gid = len(geometry_records)
        geometry_records.append(dict(id=gid, supports=supports, placements=placements))
        for src in abstract:
            if not compatible(src, supports):
                continue
            local = local_ids[supports[3:]]
            assert all(local[k] == src[k] for k in ("h", "e", "d"))
            fz = src["z"]["forbidden"][0]
            kind, key = ("singleton", str(fz[0])) if len(fz) == 1 else ("pair", str(tuple(fz)))
            ids = stable_schema_ids(inherited["two_contact_schemas"][kind][key], supports[0])
            assert ids
            for support, rel in zip(supports[1:3], src["w_contact_relations"]):
                assert stable_schema_ids([rel], support) == [0]
            q = row_evidence(src, supports, Q)
            assert q["status"] == "reject"
            excluded = source_exclusions(src, supports)
            targets = [row_evidence(src, supports, p) for p in TARGETS]
            # Separation already holds before the independent source K5 filter.
            assert all(t["status"] == "accept" for t in targets)
            if not excluded:
                assert all(t["status"] == "accept" and t["uniform_local_witness_zwuv"] for t in targets)
                assert all(c["exact"] for t in targets for c in t["components"])
            records.append(dict(id=len(records), source_id=src["id"], source_record=src,
                                geometry_id=gid, local_K2_support_id=local["id"], supports=supports,
                                placements=placements, ordered_contact_words=[contact_words(p) for p in placements],
                                z_schema_key=(kind, key), z_stable_schema_ids=ids, q=q, targets=targets,
                                source_K5=excluded, status="source_excluded" if excluded else "retained"))
    retained, excluded = ([r for r in records if bool(r["source_K5"]) == flag] for flag in (False, True))
    assert (len(records), len(excluded), len(retained)) == (102, 94, 8)
    reflection_control(records, abstract)
    frame_checks = frame_control(records)
    fibers = [dict(source_id=src["id"], source_record=src,
                   support_record_ids=[r["id"] for r in records if r["source_id"] == src["id"]],
                   retained_record_ids=[r["id"] for r in retained if r["source_id"] == src["id"]])
              for src in abstract]
    assert sum(not f["support_record_ids"] for f in fibers) == 42
    assert {r["source_id"] for r in retained} == {54, 156}
    for r in excluded:
        r["minor_skeleton"] = minor_control(r["supports"], r["source_K5"][0])
    examples = [next((r, w) for r in excluded for w in r["source_K5"] if w["component"] == name)
                for name in NAMES[:2]]
    controls = [minor_control(r["supports"], w, length, i, shared)
                for r, w in examples for length in (1, 3, 5) for i in range(length) for shared in (False, True)]
    negatives = negative_controls(controls[0], examples[0][1])
    formula_checks = sum(len(ev["joins"]) for r in records for ev in (r["q"], *r["targets"]))
    joins = sum(len(t["joins"]) for r in retained for t in r["targets"])
    all_joins = sum(len(t["joins"]) for r in records for t in r["targets"])
    assert (formula_checks, joins, frame_checks["retained"], frame_checks["all"]) == (450, 16, 384, 8352)
    assert all_joins == 348
    paths = [SOURCE, Path(__file__)] + [ROOT / "scripts" / f"{name}.py" for name in (
        "c5_adjacent_degree5_mixed_edge_shared", "c5_adjacent_degree5_mixed_edge_shared_t1_pair",
        "c5_adjacent_degree5_singleton_long_arc", "c5_single_spoke_cores", "c5_single_spoke_two_two_minor")]
    paths += [ROOT / "docs" / f"{name}.md" for name in (
        "c5_adjacent_degree5_mixed_edge_shared_t0_pair_single", "c5_adjacent_degree5_mixed_edge_shared",
        "c5_adjacent_degree5_mixed_edge_shared_t1_pair", "c5_single_spoke_two_two_external")]
    return dict(schema=1, scope="necessary same-source supports, paper source K5 and complete forbidden-set bounds; no disk realization or Lean theorem",
                original_source_ids_bound=True,
                inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
                inherited_inputs_sha256=inherited["inputs_sha256"],
                summary=dict(inherited_abstract_records=54, support_geometries=240, placement_witnesses=240,
                             necessary_support_records=102, source_excluded=94, source_retained=8,
                             empty_abstract_fibers=42, retained_abstract_records=2,
                             accepted_all_target_queries=204, unresolved_all_target_queries=0,
                             all_target_forbidden_set_joins=all_joins,
                             accepted_retained_target_queries=16, unresolved_retained_target_queries=0,
                             retained_target_forbidden_set_joins=joins, formula_direct_comparisons=formula_checks,
                             reflected_target_queries=2 * len(records), common_frame_witness_checks=frame_checks["retained"],
                             all_candidate_common_frame_witness_checks=frame_checks["all"],
                             source_exclusion_roles=dict(Counter("+".join(w["component"] for w in r["source_K5"]) for r in excluded)),
                             minor_skeletons=len(excluded) + len(controls), named_pair_contact_orders=4,
                             T4_used=False, root_spokes_used=False, routes_through_other_unary_used=False,
                             pair_source_K5_needed_for_target_separation=False),
                abstract_fibers=fibers, inherited_two_contact_schemas=inherited["two_contact_schemas"],
                geometries=geometry_records, records=records, minor_controls=controls,
                residual_controls=residual_audit(), support_controls=support_audit(), negative_controls=negatives,
                geometry_controls=dict(shared_endpoints_positive=positive, interleaved_supports_negative=interleaved))


def table(data):
    lines = ["# 共鄰端點 mixed K2：t_w=0、(2,1) 的來源排除與雙列", "",
             "必要支援資料，不是來源圖數。原 54 筆 ID 與完整關係由 JSON 綁定。", "",
             "全部 102 筆的 204 查詢已接受；另有 94 筆由原 diamond／u、v 附件給 K5。",
             "保留 8 筆的 16 查詢均為精確搬運；雙列分離不需這份 pair K5 排除。", "",
             "| ID | 原 ID | Cz | Cwp | Cws | u | v | Fz(q) | Fwp/Fws(q) | 結果 | 反射 ID |",
             "| ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: |"]
    for r in data["records"]:
        ss = " | ".join("".join(map(str, s)) for s in r["supports"])
        src = r["source_record"]
        outcome = "K5:" + ",".join(w["component"] for w in r["source_K5"]) if r["source_K5"] else "A/A"
        lines.append(f"| {r['id']} | {r['source_id']} | {ss} | {src['z']['forbidden'][0]} | "
                     f"{src['w']['forbidden']} | {outcome} | {r['reflected_id']} |")
    lines += ["", "## 保留資料的共同局部見證", "", "各見證對該 target 的全部禁色候選通用。", "",
              "| ID | p1 的 (z,w,u,v) | p2 的 (z,w,u,v) |", "| ---: | --- | --- |"]
    for r in data["records"]:
        if not r["source_K5"]:
            ws = " | ".join(str(t["uniform_local_witness_zwuv"]) for t in r["targets"])
            lines.append(f"| {r['id']} | {ws} |")
    lines += ["", "## 原 54 筆的完整纖維", "", "空纖維或全排除無此型 disk 來源；保留不宣稱實現。", "",
              "| 原 ID | h/e/d | Fz | Fwp/Fws | 必要資料數 | 保留 IDs |", "| ---: | --- | --- | --- | ---: | --- |"]
    for f in data["abstract_fibers"]:
        r = f["source_record"]
        ids = ", ".join(map(str, f["retained_record_ids"])) or "空"
        lines.append(f"| {r['id']} | {r['h']}/{r['e']}/{r['d']} | {r['z']['forbidden'][0]} | "
                     f"{r['w']['forbidden']} | {len(f['support_record_ids'])} | {ids} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    for path, payload in ((OUT, json.dumps(result, indent=2, sort_keys=True) + "\n"), (TABLE, table(result))):
        if args.check:
            assert path.read_bytes() == payload.encode(), f"certificate differs: {path}"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
