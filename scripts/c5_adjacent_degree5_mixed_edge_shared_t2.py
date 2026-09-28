#!/usr/bin/env python3
"""Shared-endpoint mixed K2, w with two spokes: actual supports and both targets.

The report proves the arbitrary-size disk-to-annulus reduction. This finite
certificate covers necessary supports and whole forbidden sets, not sources.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_mixed_edge_shared import allowed, forbidden
from c5_adjacent_degree5_singleton_long_arc import component_options
from c5_single_spoke_cores import Q, U, PERMS, PI, RHO, TARGETS

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared_t2/observations.json"
TABLE = OUT.with_name("support_table.md")
NAMES = ("Cz", "Cw", "sh", "sd", "u", "v")
SUBSETS = tuple(s for n in range(1, 6) for s in combinations(range(5), n))


def cardinality(name, support):
    return (len(support) >= 2 if name == "Cz" else
            len(support) >= 3 if name == "Cw" else
            len(support) == 2 if name == "v" else len(support) == 1)


def geometries():
    """Pack original root blocks, allowing gaps and shared boundary endpoints."""
    choices = {k: tuple(s for n in range(1, 6)
                        for s in combinations(range(6), n)
                        if cardinality(k, s) and max(s) - min(s) < 5)
               for k in NAMES}
    result = {}
    for w_order in permutations(("Cw", "sh", "sd")):
        forward = ("Cz",) + w_order + ("u", "v")
        for reverse in (False, True):
            order = ("Cz",) + tuple(reversed(forward[1:])) if reverse else forward

            def visit(j, end, assigned):
                if j == len(NAMES):
                    if assigned["sh"][0] % 5 == assigned["sd"][0] % 5:
                        return  # A simple graph has two distinct w-spoke ends.
                    for anchor in range(5):
                        supports = tuple(tuple(sorted((anchor + i) % 5
                                                      for i in assigned[k])) for k in NAMES)
                        assert supports not in result
                        result[supports] = dict(order=order, anchor=anchor,
                                               lifts={k: tuple(anchor + i for i in assigned[k])
                                                      for k in NAMES})
                    return
                name = order[j]
                for support in choices[name]:
                    if min(support) >= end and (j or min(support) == 0):
                        visit(j + 1, max(support), assigned | {name: support})
            visit(0, 0, {})
    assert len(result) == 280
    return result


def independent_geometries():
    """Independent cyclic hull masks; test the w-block as one interval.

    No ordered recursion or perimeter cut-off is used here. All proper hulls
    of Cz, Cw and v are tested; singleton ends may occupy either cut copy.
    """
    def hulls(name):
        for support in SUBSETS:
            if not cardinality(name, support):
                continue
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
        for sh, sd, u in product(range(6), repeat=3):
            if sh % 5 == sd % 5 or wz < sh < we or wz < sd < we:
                continue
            lo, hi = min(wz, sh, sd), max(we, sh, sd)
            if not (z[2] <= lo <= hi <= u <= vz <= ve <= 5 or
                    z[2] <= vz <= ve <= u <= lo <= hi <= 5):
                continue
            found.add((z[0], w[0], ((sh + z[1]) % 5,), ((sd + z[1]) % 5,),
                       ((u + z[1]) % 5,), v[0]))
    return found


@lru_cache(None)
def stable(support, ban):
    return all({p[c] for c in ban} == set(ban) for p in PERMS
               if all(p[Q[i]] == Q[i] for i in support))


def compatible(record, supports):
    cz, cw, sh, sd, u, v = supports
    h, e, d = (record[k] for k in ("h", "e", "d"))
    return (Q[u[0]] == h and {Q[i] for i in v} == {h, e}
            and Q[sh[0]] == h and Q[sd[0]] == d
            and len({Q[i] for i in cz}) >= 2
            and stable(cz, tuple(record["z"]["forbidden"][0]))
            and stable(cw, (3,)))


@lru_cache(None)
def local_colorings(supports, row):
    """Direct assignments to the original z,w,u,v, including the chord zu."""
    _, _, sh, sd, su, sv = supports
    result = {}
    for a, b, s, t in product(range(4), repeat=4):
        if (a != b and b not in {row[sh[0]], row[sd[0]]}
                and s not in {a, b, t, row[su[0]]}
                and t not in {a, row[sv[0]], row[sv[1]]}):
            result.setdefault((a, b), (a, b, s, t))
    return result


def row_evidence(record, supports, row):
    cz, cw, sh, sd, su, sv = supports
    components = (component_options(2, cz, tuple(record["z"]["forbidden"][0]), row),
                  component_options(1, cw, (3,), row))
    x, y = U - {row[su[0]]}, U - {row[i] for i in sv}
    banned = forbidden(x, y)
    direct = local_colorings(supports, row)
    joins = []
    for fz, fw in product(*(c["options"] for c in components)):
        ez, ew = U - set(fz), U - {row[sh[0]], row[sd[0]]} - set(fw)
        assert len(ez) >= 2 and ew
        pairs = allowed(ez, ew, banned)
        actual = {pair for pair in direct if pair[0] not in fz and pair[1] not in fw}
        assert actual == pairs
        if banned:
            e = next(iter(x - y))
            assert (not pairs) == (ew == {e} and ez <= x)
        else:
            assert pairs
        witness = direct[min(pairs)] if pairs else None
        joins.append(dict(forbidden_sets=(fz, fw), residuals=(sorted(ez), sorted(ew)),
                          local_witness_zwuv=witness))
    outcomes = {j["local_witness_zwuv"] is not None for j in joins}
    return dict(row=row, components=components, mixed_lists=(sorted(x), sorted(y)),
                mixed_forbidden=sorted(banned), joins=joins,
                status="accept" if outcomes == {True} else
                "reject" if outcomes == {False} else "unresolved")


def contact_words(geometry):
    """Both named Cz port orders, keeping every original w and mixed edge."""
    result = []
    for ports in (("zx0", "zx1"), ("zx1", "zx0")):
        expansion = {"Cz": ports, "Cw": ("wy",), "sh": ("w_sh",),
                     "sd": ("w_sd",), "u": ("u_boundary",),
                     "v": ("v_boundary_first", "v_boundary_last")}
        result.append(tuple(edge for unit in geometry["order"] for edge in expansion[unit]))
    return result


def reflection_control(records):
    lookup = {(r["source_id"], r["supports"]): r for r in records}
    source_lookup = {(r["h"], r["e"], r["d"], tuple(r["z"]["forbidden"][0])): r
                     for r in (item["source_record"] for item in records)}
    checks = 0
    for r in records:
        src = r["source_record"]
        moved_source = source_lookup[tuple(PI[src[k]] for k in ("h", "e", "d")) +
                                     (tuple(sorted(PI[c] for c in src["z"]["forbidden"][0])),)]
        supports = tuple(tuple(sorted(RHO[i] for i in s)) for s in r["supports"])
        other = lookup[moved_source["id"], supports]
        r["reflected_id"] = other["id"]
        for before in r["targets"]:
            moved_row = tuple(PI[before["row"][RHO[i]]] for i in range(5))
            after = row_evidence(moved_source, supports, moved_row)
            assert after["status"] == "accept"
            for old, new in zip(before["components"], after["components"]):
                assert sorted(tuple(sorted(PI[c] for c in f)) for f in old["options"]) == sorted(new["options"])
            checks += 1
    assert all(records[r["reflected_id"]]["reflected_id"] == r["id"] for r in records)
    return checks


def build():
    inherited = json.loads(SOURCE.read_text())
    abstract = [r for r in inherited["abstract_relations"] if len(r["w"]["spokes_colors"]) == 2]
    assert len(abstract) == 18
    assert all(r["w"]["ports"] == [1] and r["w"]["forbidden"] == [[3]]
               and r["planar_necessary_retained"] for r in abstract)
    local_ids = {(tuple(r["support_u"]), tuple(r["support_v"])): r
                 for r in inherited["actual_K2_supports"]}
    geometry = geometries()
    assert set(geometry) == independent_geometries()
    # The fixed forbidden set {3} requires all three actual q colors.
    assert all(stable(s, (3,)) == (len({Q[i] for i in s}) == 3) for s in SUBSETS)
    records, geometry_records = [], []
    for supports, placement in sorted(geometry.items()):
        gid = len(geometry_records)
        geometry_records.append(dict(id=gid, supports=supports, **placement))
        for src in abstract:
            if not compatible(src, supports):
                continue
            local = local_ids[supports[4:]]
            assert all(local[k] == src[k] for k in ("h", "e", "d"))
            q_evidence = row_evidence(src, supports, Q)
            assert q_evidence["status"] == "reject"
            targets = [row_evidence(src, supports, p) for p in TARGETS]
            assert all(t["status"] == "accept" for t in targets)
            records.append(dict(id=len(records), source_id=src["id"], source_record=src,
                                geometry_id=gid, local_K2_support_id=local["id"],
                                supports=supports, placement=placement,
                                ordered_contact_words=contact_words(placement),
                                q=q_evidence, targets=targets))
    assert len(records) == 38
    reflection_checks = reflection_control(records)
    by_source = [dict(source_id=src["id"], h=src["h"], e=src["e"], d=src["d"],
                      forbidden_z=src["z"]["forbidden"][0],
                      support_record_ids=[r["id"] for r in records if r["source_id"] == src["id"]])
                 for src in abstract]
    assert sum(not r["support_record_ids"] for r in by_source) == 10
    # Verify common-frame transport of each saved local witness; the component
    # options come from whole same-source forbidden sets, not port marginals.
    frame_checks = 0
    for r in records:
        for ev in r["targets"]:
            for sigma in PERMS:
                moved_row = tuple(sigma[c] for c in ev["row"])
                direct = local_colorings(r["supports"], moved_row)
                for join in ev["joins"]:
                    moved = tuple(sigma[c] for c in join["local_witness_zwuv"])
                    fz, fw = ({sigma[c] for c in f} for f in join["forbidden_sets"])
                    assert moved[:2] in direct and moved[0] not in fz and moved[1] not in fw
                    # Check the actual moved tuple too, rather than just its roots.
                    cz, cw, sh, sd, su, sv = r["supports"]
                    a, b, s, t = moved
                    assert a != b and b not in {moved_row[sh[0]], moved_row[sd[0]]}
                    assert s not in {a, b, t, moved_row[su[0]]}
                    assert t not in {a, moved_row[sv[0]], moved_row[sv[1]]}
                    frame_checks += 1
    # Shared endpoints and genuine gaps survive; a w spoke inside the open Cz
    # hull cannot be packed. These guard against changing the support semantics.
    positive = ((0, 1), (2, 3, 4), (0,), (4,), (2,), (1, 2))
    assert positive in geometry
    interior_spoke = ((0, 1, 2), (2, 3, 4), (1,), (4,), (4,), (0, 4))
    assert interior_spoke not in geometry
    assert any(len(r["supports"][1]) < max(r["placement"]["lifts"]["Cw"]) -
               min(r["placement"]["lifts"]["Cw"]) + 1 for r in records)
    inputs = [SOURCE, ROOT / "scripts/c5_adjacent_degree5_mixed_edge_shared.py",
              ROOT / "scripts/c5_adjacent_degree5_singleton_long_arc.py",
              ROOT / "scripts/c5_single_spoke_cores.py",
              ROOT / "docs/c5_adjacent_degree5_mixed_edge_shared.md",
              ROOT / "docs/c5_adjacent_degree5_mixed_edge_shared_t2.md"]
    return dict(schema=1, scope="necessary actual supports; both targets without T4; no disk realization or Lean theorem",
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
                summary=dict(inherited_abstract_records=18, distinct_spoke_geometries=len(geometry),
                             geometry_compatible_abstract_records=8, empty_abstract_fibers=10,
                             q_support_records=len(records), q_support_geometries=len({r["supports"] for r in records}),
                             used_local_K2_supports=len({r["local_K2_support_id"] for r in records}),
                             accepted_target_queries=76, unresolved_target_queries=0,
                             target_forbidden_set_joins=sum(len(t["joins"]) for r in records for t in r["targets"]),
                             reflected_support_records=38, reflected_target_queries=reflection_checks,
                             common_frame_witness_checks=frame_checks,
                             named_Cz_port_orders=2, T4_used=False),
                span_profiles=dict(Counter(str(tuple(max(r["placement"]["lifts"][k]) -
                                                      min(r["placement"]["lifts"][k])
                                                      for k in ("Cz", "Cw", "v"))) for r in records)),
                controls=dict(shared_endpoint_positive=positive, interior_spoke_negative=interior_spoke),
                abstract_fibers=by_source, geometries=geometry_records, records=records)


def table(data):
    lines = ["# 共鄰端點 mixed K2：w 側 t=2 的實際支援與雙列", "",
             "必要支援表，不是來源實現。Cz 保留兩個有序接點，Cw 保留原單接點。", "",
             "全部 38 筆的 p1=01021、p2=01212 均接受，不需 T4。", "",
             "| ID | 原關係 ID | K2 支援 ID | Cz | Cw | sh | sd | u | v | Fz(q) | p1/p2 | 反射 ID |",
             "| ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: |"]
    for r in data["records"]:
        supports = " | ".join("".join(map(str, s)) for s in r["supports"])
        fz = "".join(map(str, r["source_record"]["z"]["forbidden"][0]))
        lines.append(f"| {r['id']} | {r['source_id']} | {r['local_K2_support_id']} | {supports} | {fz} | A/A | {r['reflected_id']} |")
    lines += ["", "## 18 筆原關係的完整支援纖維", "",
              "空纖維表示此 t=2 disk 型不可能；非空不宣稱可實現。", "",
              "| 原 ID | h/e/d | Fz(q) | 支援資料 IDs |", "| ---: | --- | --- | --- |"]
    for r in data["abstract_fibers"]:
        ids = ", ".join(map(str, r["support_record_ids"])) or "空"
        lines.append(f"| {r['source_id']} | {r['h']}/{r['e']}/{r['d']} | {r['forbidden_z']} | {ids} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    for path, payload in ((OUT, json.dumps(result, indent=2, sort_keys=True) + "\n"),
                          (TABLE, table(result))):
        if args.check:
            assert path.read_bytes() == payload.encode(), f"certificate differs: {path}"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
