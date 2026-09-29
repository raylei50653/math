#!/usr/bin/env python3
"""Shared-endpoint mixed K2, t_w=1 and (1,1): ordered supports and targets.

The report supplies the arbitrary-size support and annulus arguments.
These are necessary records, not realizable disk sources or Lean theorems.
"""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_mixed_edge_shared import allowed, forbidden, schemas_for
from c5_adjacent_degree5_mixed_edge_shared_t1_pair import stable, stable_schema_ids
from c5_adjacent_degree5_singleton_long_arc import component_options
from c5_single_spoke_cores import Q, U, PERMS, PI, RHO, TARGETS

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared_t1_singles/observations.json"
TABLE = OUT.with_name("support_table.md")
NAMES = ("Cz", "Cw0", "Cw1", "s", "u", "v")


def cardinality(name, support):
    return (len(support) >= 2 if name.startswith("C") else
            len(support) == 2 if name == "v" else len(support) == 1)


def geometries():
    """All ordered lifts, including gaps and shared boundary endpoints."""
    choices = {k: tuple(s for n in range(1, 6) for s in combinations(range(6), n)
                        if cardinality(k, s) and max(s) - min(s) < 5) for k in NAMES}
    result = {}
    for w_order in permutations(("Cw0", "Cw1", "s")):
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
    """Disjoint cyclic hull edge masks, with one combined w interval."""
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
        for c0 in cs:
            if z[3] & c0[3]:
                continue
            for c1 in cs:
                used = z[3] | c0[3]
                if used & c1[3]:
                    continue
                for v in vs:
                    if (used | c1[3]) & v[3]:
                        continue
                    a, b, d = ((c[1] - z[1]) % 5 for c in (c0, c1, v))
                    ae, be, de = a + c0[2], b + c1[2], d + v[2]
                    if max(ae, be, de) > 5:
                        continue
                    for s, u in product(range(6), repeat=2):
                        if a < s < ae or b < s < be:
                            continue
                        lo, hi = min(a, b, s), max(ae, be, s)
                        if (z[2] <= lo <= hi <= u <= d <= de <= 5 or
                                z[2] <= d <= de <= u <= lo <= hi <= 5):
                            found.add((z[0], c0[0], c1[0], ((s + z[1]) % 5,),
                                       ((u + z[1]) % 5,), v[0]))
    return found


def source_key(r):
    return tuple(r[k] for k in ("h", "e", "d")) + (
        tuple(r["z"]["forbidden"][0]), r["w"]["spokes_colors"][0],
        tuple(f[0] for f in r["w"]["forbidden"]))


def bind_sources(inherited):
    records = [r for r in inherited["abstract_relations"]
               if r["w"]["ports"] == [1, 1] and len(r["w"]["spokes_colors"]) == 1]
    reconstructed = set()
    for h, e, d in permutations(range(3)):
        for fz, c in product(((h,), tuple(sorted((h, d))), tuple(sorted((h, 3)))), (h, d)):
            for bans in permutations(sorted(U - {c, e})):
                reconstructed.add((h, e, d, fz, c, bans))
    assert len(records) == len(reconstructed) == 72
    assert {source_key(r) for r in records} == reconstructed
    for r in records:
        assert r["planar_necessary_retained"] and r["z"]["ports"] == [2]
        assert not r["z"]["spokes_colors"] and r["w"]["residual"] == [r["e"]]
        assert r["w_contact_relations"] == [[[f[0]]] for f in r["w"]["forbidden"]]
        assert len(schemas_for(set(r["z"]["forbidden"][0]))) == r["z_schema_count"]
    return records


def compatible(r, supports):
    cz, c0, c1, s, u, v = supports
    return (Q[u[0]] == r["h"] and {Q[i] for i in v} == {r["h"], r["e"]}
            and Q[s[0]] == r["w"]["spokes_colors"][0]
            and all(len({Q[i] for i in t}) >= 2 for t in (cz, c0, c1))
            and all(stable(t, tuple(f)) for t, f in
                    zip((cz, c0, c1), r["z"]["forbidden"] + r["w"]["forbidden"])))


@lru_cache(None)
def local_colorings(supports, row):
    """Direct same-source z,w,u,v assignments, including original chord zu."""
    _, _, _, bs, bu, bv = supports
    result = {}
    for a, b, s, t in product(range(4), repeat=4):
        if (a != b and b != row[bs[0]] and s not in {a, b, t, row[bu[0]]}
                and t not in {a, row[bv[0]], row[bv[1]]}):
            result.setdefault((a, b), (a, b, s, t))
    return result


def row_evidence(r, supports, row):
    components = tuple(component_options(arity, support, tuple(f), row)
                       for arity, support, f in zip((2, 1, 1), supports[:3],
                                                   r["z"]["forbidden"] + r["w"]["forbidden"]))
    _, _, _, bs, bu, bv = supports
    x, y = U - {row[bu[0]]}, U - {row[i] for i in bv}
    banned, direct = forbidden(x, y), local_colorings(supports, row)
    joins, common = [], set(direct)
    for fz, f0, f1 in product(*(c["options"] for c in components)):
        ez, ew = U - set(fz), U - {row[bs[0]]} - set(f0) - set(f1)
        assert len(ez) >= 2 and ew
        pairs = allowed(ez, ew, banned)
        assert {p for p in direct if p[0] not in fz and p[1] not in f0 and p[1] not in f1} == pairs
        assert (not pairs) == (bool(banned) and ew == x - y and ez <= x)
        common &= pairs
        joins.append(dict(forbidden_sets=(fz, f0, f1), residuals=(sorted(ez), sorted(ew)),
                          local_witness_zwuv=direct[min(pairs)] if pairs else None))
    outcomes = {j["local_witness_zwuv"] is not None for j in joins}
    return dict(row=row, components=components, mixed_lists=(sorted(x), sorted(y)),
                mixed_forbidden=sorted(banned), joins=joins,
                uniform_local_witness_zwuv=direct[min(common)] if common else None,
                status="accept" if outcomes == {True} else "reject" if outcomes == {False} else "unresolved")


def contact_words(placement):
    result = []
    for ports in (("zx0", "zx1"), ("zx1", "zx0")):
        expansion = dict(Cz=ports, Cw0=("wy0",), Cw1=("wy1",), s=("w_spoke",),
                         u=("u_boundary",), v=("v_boundary_first", "v_boundary_last"))
        result.append(tuple(edge for unit in placement["order"] for edge in expansion[unit]))
    return result


def symmetry_controls(records, abstract):
    lookup = {(r["source_id"], r["supports"]): r for r in records}
    sources = {source_key(r): r for r in abstract}
    for r in records:
        h, e, d, fz, c, fw = source_key(r["source_record"])
        reflected_source = sources[(PI[h], PI[e], PI[d], tuple(sorted(PI[a] for a in fz)),
                                    PI[c], tuple(PI[a] for a in fw))]
        supports = tuple(tuple(sorted(RHO[i] for i in s)) for s in r["supports"])
        r["reflected_id"] = lookup[reflected_source["id"], supports]["id"]
        swapped_source = sources[(h, e, d, fz, c, tuple(reversed(fw)))]
        ss = r["supports"]
        r["swapped_singletons_id"] = lookup[swapped_source["id"], (ss[0], ss[2], ss[1], *ss[3:])]["id"]
        swapped = records[r["swapped_singletons_id"]]
        for old, new in zip((r["q"], *r["targets"]), (swapped["q"], *swapped["targets"])):
            assert old["status"] == new["status"]
            assert old["components"] == (new["components"][0], new["components"][2], new["components"][1])
            assert old["uniform_local_witness_zwuv"] == new["uniform_local_witness_zwuv"]
        r["reflected_targets"] = []
        for before in r["targets"]:
            moved_row = tuple(PI[before["row"][RHO[i]]] for i in range(5))
            after = row_evidence(reflected_source, supports, moved_row)
            assert after["status"] == before["status"] == "accept"
            for old, new in zip(before["components"], after["components"]):
                assert sorted(tuple(sorted(PI[c] for c in f)) for f in old["options"]) == sorted(new["options"])
            r["reflected_targets"].append(dict(raw_row=moved_row, status=after["status"]))
    for key in ("reflected_id", "swapped_singletons_id"):
        assert all(records[r[key]][key] == r["id"] for r in records)
    assert all(r["swapped_singletons_id"] != r["id"] for r in records)


def frame_control(records):
    checks = 0
    for r in records:
        for ev in r["targets"]:
            for join in ev["joins"]:
                for sigma in PERMS:
                    row = tuple(sigma[c] for c in ev["row"])
                    a, b, s, t = (sigma[c] for c in join["local_witness_zwuv"])
                    fz, f0, f1 = ({sigma[c] for c in f} for f in join["forbidden_sets"])
                    _, _, _, bs, bu, bv = r["supports"]
                    assert a not in fz and b not in f0 and b not in f1
                    assert a != b and b != row[bs[0]]
                    assert s not in {a, b, t, row[bu[0]]}
                    assert t not in {a, row[bv[0]], row[bv[1]]}
                    checks += 1
    return checks


def build():
    inherited = json.loads(SOURCE.read_text())
    assert sha256((ROOT / "scripts/c5_adjacent_degree5_mixed_edge_shared.py").read_bytes()).hexdigest() == inherited["source_sha256"]
    for path, expected in inherited["inputs_sha256"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    abstract, geometry = bind_sources(inherited), geometries()
    assert set(geometry) == independent_geometries()
    assert len(geometry) == sum(map(len, geometry.values())) == 780
    positive = ((0, 1), (1, 2), (2, 3), (3,), (3,), (3, 4))
    interior_spoke = ((0, 1), (1, 2, 3), (3, 4), (2,), (4,), (0, 4))
    assert positive in geometry and interior_spoke not in geometry
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
            local = local_ids[supports[4:]]
            assert all(local[k] == src[k] for k in ("h", "e", "d"))
            fz = src["z"]["forbidden"][0]
            kind, key = ("singleton", str(fz[0])) if len(fz) == 1 else ("pair", str(tuple(fz)))
            ids = stable_schema_ids(inherited["two_contact_schemas"][kind][key], supports[0])
            assert ids
            q = row_evidence(src, supports, Q)
            assert q["status"] == "reject"
            targets = [row_evidence(src, supports, p) for p in TARGETS]
            assert all(t["status"] == "accept" and t["uniform_local_witness_zwuv"] for t in targets)
            third = 1 + src["w"]["forbidden"].index([3])
            assert len({Q[i] for i in supports[third]}) == 3
            for p in placements:
                spans = {k: max(p["lifts"][k]) - min(p["lifts"][k]) for k in NAMES}
                assert spans == (dict.fromkeys(NAMES[:3], 1) | {NAMES[third]: 2, "s": 0, "u": 0, "v": 1})
                assert all(len(supports[j]) == spans[k] + 1 for j, k in enumerate(NAMES))
            records.append(dict(id=len(records), source_id=src["id"], source_record=src,
                                geometry_id=gid, local_K2_support_id=local["id"], supports=supports,
                                placements=placements, ordered_contact_words=[contact_words(p) for p in placements],
                                z_schema_key=(kind, key), z_stable_schema_ids=ids, q=q, targets=targets))
    assert len(records) == 32
    symmetry_controls(records, abstract)
    frame_checks = frame_control(records)
    fibers = [dict(source_id=src["id"], source_record=src,
                   support_record_ids=[r["id"] for r in records if r["source_id"] == src["id"]])
              for src in abstract]
    assert sum(not f["support_record_ids"] for f in fibers) == 56
    joins = sum(len(t["joins"]) for r in records for t in r["targets"])
    assert (joins, frame_checks) == (128, 3072)
    paths = [SOURCE, Path(__file__)] + [ROOT / "scripts" / f"{name}.py" for name in (
        "c5_adjacent_degree5_mixed_edge_shared", "c5_adjacent_degree5_mixed_edge_shared_t1_pair",
        "c5_adjacent_degree5_singleton_long_arc", "c5_single_spoke_cores")]
    paths += [ROOT / "docs" / f"{name}.md" for name in (
        "c5_adjacent_degree5_mixed_edge_shared_t1_singles", "c5_adjacent_degree5_mixed_edge_shared",
        "c5_adjacent_degree5_mixed_edge_shared_t1_pair", "c5_adjacent_degree5_mixed_edge_shared_t2")]
    return dict(schema=1, scope="necessary same-source supports and complete forbidden-set bounds; no disk realization or Lean theorem",
                original_source_ids_bound=True,
                inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
                inherited_inputs_sha256=inherited["inputs_sha256"],
                summary=dict(inherited_abstract_records=72, support_geometries=780, placement_witnesses=780,
                             necessary_support_records=32, compatible_abstract_records=16, empty_abstract_fibers=56,
                             accepted_target_queries=64, unresolved_target_queries=0, target_forbidden_set_joins=joins,
                             formula_direct_comparisons=joins + len(records), reflected_target_queries=64,
                             named_singleton_swap_checks=32, common_frame_witness_checks=frame_checks,
                             named_Cz_port_orders=2, T4_used=False, new_source_minor_exclusions=0),
                abstract_fibers=fibers, inherited_two_contact_schemas=inherited["two_contact_schemas"],
                geometries=geometry_records, records=records,
                geometry_controls=dict(shared_endpoints_positive=positive, interior_spoke_negative=interior_spoke))


def table(data):
    lines = ["# 共鄰端點 mixed K2：t_w=1、(1,1) 的實際支援與雙列", "",
             "必要資料，未證 disk 可實現性。兩個具名單接點分量各有自己的完整關係。", "",
             "原 72 筆中 56 筆無相容支援；32 筆必要支援的 64 個指定查詢全接受，不需 T4。", "",
             "| ID | 原 ID | Cz | Cw0 | Cw1 | s | u | v | Fz(q) | Fw0/Fw1(q) | p1/p2 | 反射 ID | 交換 ID |",
             "| ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: |"]
    for r in data["records"]:
        ss = " | ".join("".join(map(str, s)) for s in r["supports"])
        src = r["source_record"]
        lines.append(f"| {r['id']} | {r['source_id']} | {ss} | {src['z']['forbidden'][0]} | "
                     f"{src['w']['forbidden']} | A/A | {r['reflected_id']} | {r['swapped_singletons_id']} |")
    lines += ["", "## 依禁色角色顯示的 16 列與共同局部見證", "",
              "本表只顯示 Cw1 禁 3 的一半；JSON 保留兩個具名分量的全部 32 筆。", "",
              "(z,w,u,v) 對該 target 的每一組完整禁色候選都有效。", "",
              "| ID | Cz | Cw0 | Cw1 | s | u | v | p1 的 (z,w,u,v) | p2 的 (z,w,u,v) |",
              "| ---: | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in data["records"]:
        if r["source_record"]["w"]["forbidden"][1] == [3]:
            ss = " | ".join("".join(map(str, s)) for s in r["supports"])
            ws = " | ".join(str(t["uniform_local_witness_zwuv"]) for t in r["targets"])
            lines.append(f"| {r['id']} | {ss} | {ws} |")
    lines += ["", "## 原 72 筆的完整支援纖維", "",
              "| 原 ID | h/e/d | spoke 色 | Fz | Fw0/Fw1 | 必要資料 IDs |",
              "| ---: | --- | ---: | --- | --- | --- |"]
    for f in data["abstract_fibers"]:
        r = f["source_record"]
        ids = ", ".join(map(str, f["support_record_ids"])) or "空"
        lines.append(f"| {r['id']} | {r['h']}/{r['e']}/{r['d']} | {r['w']['spokes_colors'][0]} | "
                     f"{r['z']['forbidden'][0]} | {r['w']['forbidden']} | {ids} |")
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
