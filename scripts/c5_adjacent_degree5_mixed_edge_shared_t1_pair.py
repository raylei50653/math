#!/usr/bin/env python3
"""Shared-endpoint mixed K2, t_w=1 and (2): source K5 and both targets.

The arbitrary-size annulus and local bridge lemmas are proved in the report.
These are necessary support records and topology controls, not disk sources.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_mixed_edge_shared import allowed, forbidden, schemas_for
from c5_adjacent_degree5_singleton_long_arc import component_options
from c5_single_spoke_cores import Q, U, PERMS, PI, RHO, TARGETS
from c5_single_spoke_two_two_minor import residual_audit, support_audit, verify_minor

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared_t1_pair/observations.json"
TABLE = OUT.with_name("support_table.md")
NAMES = ("Cz", "Cw", "s", "u", "v")
SUBSETS = tuple(s for n in range(1, 6) for s in combinations(range(5), n))
DIAMOND = (("z", "w"), ("w", "u"), ("u", "v"), ("v", "z"), ("z", "u"))


def cardinality(name, support):
    return (len(support) >= 2 if name in ("Cz", "Cw") else
            len(support) == 2 if name == "v" else len(support) == 1)


def geometries():
    """Ordered lifts of all actual supports; retain every placement witness."""
    choices = {k: tuple(s for n in range(1, 6)
                        for s in combinations(range(6), n)
                        if cardinality(k, s) and max(s) - min(s) < 5)
               for k in NAMES}
    result = {}
    for w_order in permutations(("Cw", "s")):
        forward = ("Cz",) + w_order + ("u", "v")
        for reverse in (False, True):
            order = ("Cz",) + tuple(reversed(forward[1:])) if reverse else forward

            def visit(j, end, assigned):
                if j == len(NAMES):
                    for anchor in range(5):
                        supports = tuple(tuple(sorted((anchor + i) % 5
                                                      for i in assigned[k])) for k in NAMES)
                        placement = dict(order=order, anchor=anchor,
                                         lifts={k: tuple(anchor + i for i in assigned[k])
                                                for k in NAMES})
                        result.setdefault(supports, []).append(placement)
                    return
                name = order[j]
                for support in choices[name]:
                    if min(support) >= end and (j or min(support) == 0):
                        visit(j + 1, max(support), assigned | {name: support})
            visit(0, 0, {})
    assert len(result) == 1140
    return result


def independent_geometries():
    """All proper cyclic hulls with disjoint edge masks and one w interval."""
    def hulls(name):
        for support in SUBSETS:
            if cardinality(name, support):
                for start in support:
                    span = max((i - start) % 5 for i in support)
                    mask = sum(1 << ((start + j) % 5) for j in range(span))
                    yield support, start, span, mask

    found = set()
    for z, w, v in product(hulls("Cz"), hulls("Cw"), hulls("v")):
        if z[3] & w[3] or z[3] & v[3] or w[3] & v[3]:
            continue
        wz, vz = (w[1] - z[1]) % 5, (v[1] - z[1]) % 5
        we, ve = wz + w[2], vz + v[2]
        if we > 5 or ve > 5:
            continue
        for s, u in product(range(6), repeat=2):
            if wz < s < we:
                continue
            lo, hi = min(wz, s), max(we, s)
            if (z[2] <= lo <= hi <= u <= vz <= ve <= 5 or
                    z[2] <= vz <= ve <= u <= lo <= hi <= 5):
                found.add((z[0], w[0], ((s + z[1]) % 5,),
                           ((u + z[1]) % 5,), v[0]))
    return found


@lru_cache(None)
def stable(support, ban):
    return all({p[c] for c in ban} == set(ban) for p in PERMS
               if all(p[Q[i]] == Q[i] for i in support))


def source_key(r):
    return tuple(r[k] for k in ("h", "e", "d")) + (
        tuple(r["z"]["forbidden"][0]), r["w"]["spokes_colors"][0],
        tuple(r["w"]["forbidden"][0]))


def bind_sources(inherited):
    records = [r for r in inherited["abstract_relations"]
               if r["w"]["ports"] == [2] and len(r["w"]["spokes_colors"]) == 1]
    reconstructed = set()
    for h, e, d in permutations(range(3)):
        for fz, c in product(((h,), tuple(sorted((h, d))), tuple(sorted((h, 3)))), (h, d)):
            reconstructed.add((h, e, d, fz, c, tuple(sorted(U - {c, e}))))
    assert len(records) == len(reconstructed) == 36
    assert {source_key(r) for r in records} == reconstructed
    for r in records:
        assert r["planar_necessary_retained"] and r["z"]["ports"] == [2]
        assert r["z"]["spokes_colors"] == []
        assert r["w"]["residual"] == [r["e"]]
        fw = r["w"]["forbidden"][0]
        assert r["w_contact_relations"] == [[list(p) for p in permutations(fw)]]
        assert len(schemas_for(set(r["z"]["forbidden"][0]))) == r["z_schema_count"]
    return records


def compatible(record, supports):
    cz, cw, s, u, v = supports
    return (Q[u[0]] == record["h"] and {Q[i] for i in v} == {record["h"], record["e"]}
            and Q[s[0]] == record["w"]["spokes_colors"][0]
            and len({Q[i] for i in cz}) >= 2
            and stable(cz, tuple(record["z"]["forbidden"][0]))
            and stable(cw, tuple(record["w"]["forbidden"][0])))


def stable_schema_ids(schemas, support):
    stabilizer = [p for p in PERMS if all(p[Q[i]] == Q[i] for i in support)]
    return [i for i, rel in enumerate(schemas) if all(
        {tuple(p[c] for c in t) for t in rel} == set(map(tuple, rel)) for p in stabilizer)]


@lru_cache(None)
def local_colorings(supports, row):
    """Enumerate the same z,w,u,v, explicitly retaining zu."""
    _, _, bs, bu, bv = supports
    result = {}
    for a, b, s, t in product(range(4), repeat=4):
        if (a != b and b != row[bs[0]] and s not in {a, b, t, row[bu[0]]}
                and t not in {a, row[bv[0]], row[bv[1]]}):
            result.setdefault((a, b), (a, b, s, t))
    return result


def row_evidence(record, supports, row):
    cz, cw, bs, bu, bv = supports
    components = tuple(component_options(2, support, tuple(record[k]["forbidden"][0]), row)
                       for k, support in zip(("z", "w"), (cz, cw)))
    x, y = U - {row[bu[0]]}, U - {row[i] for i in bv}
    banned = forbidden(x, y)
    direct = local_colorings(supports, row)
    joins = []
    for fz, fw in product(*(c["options"] for c in components)):
        ez, ew = U - set(fz), U - {row[bs[0]]} - set(fw)
        assert len(ez) >= 2 and ew
        pairs = allowed(ez, ew, banned)
        assert {pair for pair in direct if pair[0] not in fz and pair[1] not in fw} == pairs
        assert (not pairs) == (bool(banned) and ew == x - y and ez <= x)
        joins.append(dict(forbidden_sets=(fz, fw), residuals=(sorted(ez), sorted(ew)),
                          local_witness_zwuv=direct[min(pairs)] if pairs else None))
    outcomes = {j["local_witness_zwuv"] is not None for j in joins}
    return dict(row=row, components=components, mixed_lists=(sorted(x), sorted(y)),
                mixed_forbidden=sorted(banned), joins=joins,
                status="accept" if outcomes == {True} else
                "reject" if outcomes == {False} else "unresolved")


def diamond_edges(supports):
    _, _, s, u, v = supports
    edges = list(DIAMOND) + [("w", f"b{s[0]}"), ("u", f"b{u[0]}")]
    edges += [("v", f"b{i}") for i in v]
    return {tuple(sorted(e)) for e in edges}


def external_routes(supports, root, pair):
    edges = diamond_edges(supports)
    result = []

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


def source_exclusions(record, supports):
    result = []
    for k, root in enumerate(("z", "w")):
        f = set(record[root]["forbidden"][0])
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
        expansion = {"Cz": ("zx0", "zx1"), "Cw": ("wy0", "wy1"),
                     "s": ("w_spoke",), "u": ("u_boundary",),
                     "v": ("v_boundary_first", "v_boundary_last")}
        for name, flip in zip(NAMES[:2], flips):
            if flip:
                expansion[name] = tuple(reversed(expansion[name]))
        result.append(tuple(edge for unit in placement["order"] for edge in expansion[unit]))
    return result


def minor_control(supports, witness, length=1, index=0, shared=False):
    """Original diamond plus two unary skeletons; no degree/list claim."""
    root = witness["root"]
    other = "w" if root == "z" else "z"
    pair = witness["forced_pair"]
    route = witness["chosen_route"]
    edges = diamond_edges(supports)

    def edge(a, b):
        edges.add(tuple(sorted((a, b))))

    for i in range(5):
        edge(f"b{i}", f"b{(i+1) % 5}")
    path = [f"x{i}" for i in range(length + 1)]
    for a, b in zip([root] + path, path + [root]):
        edge(a, b)
    # Retain the other unary's two incidences, but never route through it.
    edge(other, "other0")
    edge("other0", "other1")
    edge("other1", other)
    for b in supports[1 if root == "z" else 0]:
        edge("other0", f"b{b}")
    bags = []
    tethers = []
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
    # Add all actual support vertices; these extra edges cannot harm the minor.
    for b in supports[0 if root == "z" else 1]:
        edge("x0_t" if shared else "x0", f"b{b}")
    outside = (set(path) - set(path[index:index+2])) | set(route)
    outside |= {f"b{i}" for i in witness["complement_arc"]}
    bags += [outside, {f"b{pair[0]}"}, {f"b{pair[1]}"}]
    assert all(tuple(sorted(e)) in diamond_edges(supports) for e in zip(route, route[1:]))
    return dict(length=length, index=index, shared_tether=shared, original_external_route=route,
                edges=sorted(edges), branch_sets=[sorted(b) for b in bags],
                tethers=tethers, adjacencies=verify_minor(edges, bags),
                scope="topology skeleton; not a degree-list source")


def reflection_control(records, abstract):
    lookup = {(r["source_id"], r["supports"]): r for r in records}
    sources = {source_key(r): r for r in abstract}
    checks = 0
    for r in records:
        h, e, d, fz, c, fw = source_key(r["source_record"])
        key = (PI[h], PI[e], PI[d], tuple(sorted(PI[a] for a in fz)),
               PI[c], tuple(sorted(PI[a] for a in fw)))
        src = sources[key]
        supports = tuple(tuple(sorted(RHO[i] for i in s)) for s in r["supports"])
        other = lookup[src["id"], supports]
        r["reflected_id"] = other["id"]
        assert bool(r["source_K5"]) == bool(other["source_K5"])
        for w in r["source_K5"]:
            moved_pair = tuple(sorted(RHO[i] for i in w["forced_pair"]))
            moved_routes = {tuple(f"b{RHO[int(v[1:])]}" if v.startswith("b") else v for v in p)
                            for p in w["original_external_routes"]}
            moved = next(a for a in other["source_K5"] if a["root"] == w["root"])
            assert moved["forced_pair"] == moved_pair
            assert set(moved["original_external_routes"]) == moved_routes
        r["reflected_targets"] = []
        for before in r["targets"]:
            moved_row = tuple(PI[before["row"][RHO[i]]] for i in range(5))
            after = row_evidence(src, supports, moved_row)
            assert after["status"] == before["status"]
            for old, new in zip(before["components"], after["components"]):
                assert sorted(tuple(sorted(PI[c] for c in f)) for f in old["options"]) == sorted(new["options"])
            r["reflected_targets"].append(dict(raw_row=moved_row, status=after["status"]))
            checks += 1
    assert all(records[r["reflected_id"]]["reflected_id"] == r["id"] for r in records)
    return checks


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
                    fz, fw = ({sigma[c] for c in f} for f in join["forbidden_sets"])
                    _, _, bs, bu, bv = r["supports"]
                    assert a not in fz and b not in fw
                    assert a != b and b != row[bs[0]]
                    assert s not in {a, b, t, row[bu[0]]}
                    assert t not in {a, row[bv[0]], row[bv[1]]}
                    checks["all"] += 1
                    if r["status"] == "retained":
                        checks["retained"] += 1
    return checks


def build():
    inherited = json.loads(SOURCE.read_text())
    assert sha256((ROOT / "scripts/c5_adjacent_degree5_mixed_edge_shared.py").read_bytes()).hexdigest() == inherited["source_sha256"]
    for path, expected in inherited["inputs_sha256"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    abstract = bind_sources(inherited)
    geometry = geometries()
    assert set(geometry) == independent_geometries()
    shared_endpoint = ((0, 1), (1, 2), (2,), (3,), (3, 4))
    interior_spoke = ((0, 1, 2), (2, 3), (1,), (3,), (3, 4))
    assert shared_endpoint in geometry and interior_spoke not in geometry
    assert any(len(s) < max(p["lifts"][k]) - min(p["lifts"][k]) + 1
               for ss, ps in geometry.items() for p in ps for k, s in zip(NAMES, ss))
    assert any(max(p["lifts"][k]) - min(p["lifts"][k]) >
               min(max((i - a) % 5 for i in s) for a in s)
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
            schema_ids = stable_schema_ids(inherited["two_contact_schemas"][kind][key], supports[0])
            assert schema_ids
            q = row_evidence(src, supports, Q)
            assert q["status"] == "reject"
            targets = [row_evidence(src, supports, p) for p in TARGETS]
            excluded = source_exclusions(src, supports)
            if not excluded:
                assert all(t["status"] == "accept" for t in targets)
            records.append(dict(id=len(records), source_id=src["id"], source_record=src,
                                geometry_id=gid, local_K2_support_id=local["id"], supports=supports,
                                placements=placements, ordered_contact_words=[contact_words(p) for p in placements],
                                z_schema_key=(kind, key), z_stable_schema_ids=schema_ids,
                                q=q, targets=targets, source_K5=excluded,
                                status="source_excluded" if excluded else "retained"))
    retained = [r for r in records if not r["source_K5"]]
    excluded = [r for r in records if r["source_K5"]]
    assert (len(records), len(excluded), len(retained)) == (356, 292, 64)
    reflection_checks = reflection_control(records, abstract)
    frame_checks = frame_control(records)
    fibers = [dict(source_id=src["id"], source_record=src,
                   support_record_ids=[r["id"] for r in records if r["source_id"] == src["id"]],
                   retained_record_ids=[r["id"] for r in retained if r["source_id"] == src["id"]])
              for src in abstract]
    assert sum(not f["support_record_ids"] for f in fibers) == 20
    assert sum(bool(f["retained_record_ids"]) for f in fibers) == 4
    for r in excluded:
        r["minor_skeleton"] = minor_control(r["supports"], r["source_K5"][0])
    example = next(r for r in excluded if r["supports"] == ((0, 1, 3, 4), (1, 2), (2,), (2,), (2, 3))
                   and r["source_record"]["z"]["forbidden"] == [[0, 2]])
    ew = next(w for w in example["source_K5"] if w["root"] == "w")
    assert ("w", "z", "v", "b3") in ew["original_external_routes"]
    controls = [minor_control(example["supports"], dict(ew, chosen_route=("w", "z", "v", "b3")),
                              length, i, shared)
                for length in (1, 3, 5) for i in range(length) for shared in (False, True)]
    negative = []
    base = controls[0]
    edges, bags = set(map(tuple, base["edges"])), list(map(set, base["branch_sets"]))
    for name, es, bs in (
        ("missing_path_bag_tether", edges - {("b1", "x1")}, bags),
        ("missing_original_bridge", edges - {("x0", "x1")}, bags),
        ("missing_frame_pair_edge", edges - {("b1", "b2")}, bags),
        ("overlapping_branch_sets", edges, [bags[0] | {"w"}] + bags[1:]),
    ):
        try:
            verify_minor(es, bs)
        except AssertionError:
            negative.append(name)
        else:
            raise AssertionError(name)
    # Keep all diamond edges, so remove every edge to the complementary arc.
    broken = {e for e in edges if not (e[0].startswith("b") and e[1] in ("u", "v", "w")
                                      and int(e[0][1:]) in ew["complement_arc"])}
    try:
        verify_minor(broken, bags)
    except AssertionError:
        negative.append("missing_diamond_to_complement_connection")
    else:
        raise AssertionError("external path negative control")
    formula_checks = sum(len(ev["joins"]) for r in records for ev in (r["q"], *r["targets"]))
    assert (formula_checks, reflection_checks, frame_checks["retained"]) == (2578, 712, 15312)
    assert frame_checks["all"] == 52368
    # A duplicated color supplier cannot be promoted to a named forced vertex.
    assert [i for i in (0, 2, 3, 4) if Q[i] == 0] == [0, 2]
    assert source_exclusions(dict(z=dict(forbidden=[[0]]), w=dict(forbidden=[[2, 3]])),
                             ((0, 1), (0, 2, 3, 4), (2,), (2,), (2, 3))) == []
    negative.append("nonunique_supplier_is_not_a_forced_pair")
    negative.append("spoke_inside_Cz_hull_is_not_a_geometry")
    paths = [SOURCE, Path(__file__)] + [ROOT / "scripts" / f"{name}.py" for name in (
        "c5_adjacent_degree5_mixed_edge_shared", "c5_adjacent_degree5_singleton_long_arc",
        "c5_single_spoke_cores", "c5_single_spoke_two_two_minor")]
    paths += [ROOT / "docs" / f"{name}.md" for name in (
        "c5_adjacent_degree5_mixed_edge_shared_t1_pair", "c5_adjacent_degree5_mixed_edge_shared",
        "c5_adjacent_degree5_mixed_edge_shared_t2", "c5_single_spoke_two_two_external",
        "c5_single_spoke_two_two_minor")]
    return dict(schema=1, scope="necessary supports, local paper K5, complete forbidden-set bounds; no disk realization or Lean theorem",
                original_source_ids_bound=True,
                inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
                inherited_inputs_sha256=inherited["inputs_sha256"],
                summary=dict(inherited_abstract_records=36, support_geometries=len(geometry),
                             placement_witnesses=sum(map(len, geometry.values())),
                             necessary_support_records=356, source_excluded=292, source_retained=64,
                             empty_abstract_fibers=20, retained_abstract_records=4,
                             accepted_retained_target_queries=128, unresolved_retained_target_queries=0,
                             formula_direct_comparisons=formula_checks, reflected_target_queries=reflection_checks,
                             common_frame_witness_checks=frame_checks["retained"],
                             all_candidate_common_frame_witness_checks=frame_checks["all"],
                             source_exclusion_roles=dict(Counter("+".join(w["component"] for w in r["source_K5"])
                                                                for r in excluded)),
                             retained_target_forbidden_set_joins=sum(len(t["joins"]) for r in retained for t in r["targets"]),
                             minor_skeletons=len(excluded) + len(controls), named_contact_orders=4, T4_used=False),
                example_record_id=example["id"], abstract_fibers=fibers,
                inherited_two_contact_schemas=inherited["two_contact_schemas"],
                geometries=geometry_records, records=records, minor_controls=controls,
                residual_controls=residual_audit(), support_controls=support_audit(), negative_controls=negative,
                geometry_controls=dict(shared_endpoint=shared_endpoint, interior_spoke=interior_spoke))


def table(data):
    lines = ["# 共鄰端點 mixed K2：t_w=1、(2) 的來源排除與雙列", "",
             "必要支援資料，不是來源圖數。原 36 筆 ID 與完整記錄由 JSON 綁定。", "",
             "356 筆：292 筆來源 K5 排除；64 筆保留的 128 個指定查詢全部接受。", "",
             "| ID | 原 ID | Cz | Cw | s | u | v | Fz(q) | Fw(q) | 結果 | 反射 ID |",
             "| ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: |"]
    for r in data["records"]:
        supports = " | ".join("".join(map(str, s)) for s in r["supports"])
        bans = " | ".join(str(r["source_record"][k]["forbidden"][0]) for k in ("z", "w"))
        outcome = "K5:" + ",".join(w["component"] for w in r["source_K5"]) if r["source_K5"] else "A/A"
        lines.append(f"| {r['id']} | {r['source_id']} | {supports} | {bans} | {outcome} | {r['reflected_id']} |")
    lines += ["", "## 原 36 筆的完整纖維", "", "空纖維或全排除均無此型 disk 來源；保留不宣稱實現。", "",
              "| 原 ID | h/e/d | spoke 色 | Fz | Fw | 必要資料數 | 保留 IDs |", "| ---: | --- | ---: | --- | --- | ---: | --- |"]
    for f in data["abstract_fibers"]:
        r = f["source_record"]
        ids = ", ".join(map(str, f["retained_record_ids"])) or "空"
        lines.append(f"| {r['id']} | {r['h']}/{r['e']}/{r['d']} | {r['w']['spokes_colors'][0]} | "
                     f"{r['z']['forbidden'][0]} | {r['w']['forbidden'][0]} | {len(f['support_record_ids'])} | {ids} |")
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
