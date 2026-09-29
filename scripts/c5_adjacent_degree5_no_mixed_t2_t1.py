#!/usr/bin/env python3
"""No-mixed t_z=2,(2), t_w=1,(2,1): budgets, supports and rejection causes.

Necessary same-source data only. Cross-component upper-bound choices are not
asserted realizable. Arbitrary-size support coverage is proved in the report.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2 import schema_audit, stable_schema_ids
from c5_adjacent_degree5_singleton_long_arc import component_options, valid_q_support
from c5_root_degree_excess import budget
from c5_single_spoke_cores import Q, U, PI, RHO, TARGETS

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_no_mixed/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_no_mixed_t2_t1/observations.json"
TABLE = OUT.with_name("support_table.md")
NAMES = ("Cz", "z0", "z1", "Cw", "Dw", "w0")
COMPONENTS = (("Cz", "z", 0, 0, 2), ("Cw", "w", 0, 3, 2), ("Dw", "w", 1, 4, 1))


def cardinalities(name):
    return range(2, 6) if name in ("Cz", "Cw", "Dw") else (1,)


def geometries():
    choices = {name: [s for k in cardinalities(name) for s in combinations(range(6), k)
                      if max(s) - min(s) < 5] for name in NAMES}
    orders = set()
    for z, w in product(permutations(NAMES[:3]), permutations(NAMES[3:])):
        order = z + w
        i = order.index("Cz")
        orders.add(order[i:] + order[:i])
    result = {}
    for order in sorted(orders):
        def visit(j, end, assigned):
            if j == 6:
                for anchor in range(5):
                    supports = tuple(tuple(sorted((anchor + i) % 5 for i in assigned[n]))
                                     for n in NAMES)
                    if supports[1] >= supports[2]:
                        continue
                    result.setdefault(supports, []).append(dict(
                        order=order, anchor=anchor, lifts=tuple(assigned[n] for n in NAMES)))
                return
            for support in choices[order[j]]:
                if min(support) >= end and (j or min(support) == 0):
                    visit(j + 1, max(support), assigned | {order[j]: support})
        visit(0, 0, {})
    return result


def independent_geometries():
    """Actual support hulls on each whole side, with disjoint frame-edge masks."""
    sides = []
    for names in (NAMES[:3], NAMES[3:]):
        found = set()
        choices = [[s for k in cardinalities(n) for s in combinations(range(5), k)] for n in names]
        for supports in product(*choices):
            if names[0] == "Cz" and supports[1] >= supports[2]:
                continue
            for anchor in set().union(*map(set, supports)):
                lifts = [sorted((i - anchor) % 5 for i in s) for s in supports]
                if any(not (a[-1] <= b[0] or b[-1] <= a[0])
                       for a, b in combinations(lifts, 2)):
                    continue
                span = max(s[-1] for s in lifts)
                mask = sum(1 << ((anchor + j) % 5) for j in range(span))
                found.add((supports, mask))
        sides.append(found)
    # Group by masks to avoid an unnecessarily large all-pairs product.
    groups = []
    for side in sides:
        by_mask = {}
        for supports, mask in side:
            by_mask.setdefault(mask, set()).add(supports)
        groups.append(by_mask)
    return {a + b for ma, aa in groups[0].items() for mb, bb in groups[1].items()
            if not ma & mb for a, b in product(aa, bb)}


def rotations(order):
    result = []
    for flips in product((False, True), repeat=2):
        expansion = {n: (n,) for n in NAMES}
        for name, flip in zip(("Cz", "Cw"), flips):
            ports = (name + "_0", name + "_1")
            expansion[name] = ports[::-1] if flip else ports
        expansion["Dw"] = ("Dw_0",)
        roots = {}
        for root, own, other in (("z", NAMES[:3], "w"), ("w", NAMES[3:], "z")):
            start = next(i for i, n in enumerate(order) if n in own and order[i - 1] not in own)
            units = tuple(order[(start + j) % 6] for j in range(3))
            assert set(units) == set(own)
            roots[root] = (other,) + tuple(p for n in units for p in expansion[n])
            assert len(roots[root]) == len(set(roots[root])) == 5
        result.append(dict(contact_flips=flips, root_rotations=roots,
                           neighborhood_word=tuple(p for n in order for p in expansion[n])))
    return result


def bind_sources(data):
    sides = data["side_normal_forms"]
    records = []
    for join_id, (i, j) in enumerate(data["abstract_conditions"]["retained"]):
        z, w = sides[i], sides[j]
        if (len(z["root_boundary"]), z["ports"], len(w["root_boundary"]), w["ports"]) != (2, [2], 1, [2, 1]):
            continue
        budgets = {r: budget(s) for r, s in (("z", z), ("w", w))}
        assert budgets["z"]["component_deficits"] == [1]
        assert budgets["w"]["component_deficits"] == [1, 0]
        records.append(dict(id=len(records), retained_join_id=join_id, side_ids=(i, j),
                            common=z["common"], z=z, w=w, source_budgets=budgets))
    def key(s):
        return (tuple(s["z"]["root_boundary"]), tuple(s["w"]["root_boundary"]), s["common"],
                tuple(s["z"]["forbidden"][0]), tuple(map(tuple, s["w"]["forbidden"])))
    rebuilt = set()
    for sz, sw in product(combinations(range(5), 2), combinations(range(5), 1)):
        if len({Q[i] for i in sz}) != 2:
            continue
        for c in U - {Q[i] for i in sz + sw}:
            fz = tuple(sorted(U - {Q[i] for i in sz} - {c}))
            for a, b in permutations(U - {Q[sw[0]], c}):
                rebuilt.add((sz, sw, c, fz, ((a,), (b,))))
    assert {key(s) for s in records} == rebuilt and len(records) == 136
    assert records[0]["side_ids"] == (133, 91)
    return records


def row_evidence(source, supports, row):
    components = [dict(name=name, **component_options(k, supports[pos], tuple(source[root]["forbidden"][col]), row))
                  for name, root, col, pos, k in COMPONENTS]
    joins = []
    for fz, fw, fd in product(*(c["options"] for c in components)):
        ez = U - {row[i] for i in source["z"]["root_boundary"]} - set(fz)
        ew = U - {row[i] for i in source["w"]["root_boundary"]} - set(fw) - set(fd)
        pairs = sorted((a, b) for a, b in product(ez, ew) if a != b)
        direct = [(a, b) for a, b in product(range(4), repeat=2)
                  if a != b and a not in fz and b not in fw and b not in fd
                  and all(a != row[i] for i in source["z"]["root_boundary"])
                  and all(b != row[i] for i in source["w"]["root_boundary"])]
        assert pairs == direct
        reasons = (["empty_z"] if not ez else []) + (["empty_w"] if not ew else [])
        if len(ez) == 1 and ez == ew:
            reasons.append("same_singleton")
        assert bool(reasons) == (not pairs)
        joins.append(dict(forbidden_sets=(fz, fw, fd), residuals=(sorted(ez), sorted(ew)),
                          root_pairs=pairs, witness=pairs[0] if pairs else None,
                          obstruction_reasons=reasons))
    accepted = all(j["root_pairs"] for j in joins)
    mechanism = ("complete_relation_transport" if all(c["exact"] for c in components)
                 else "transport_and_capacity_bound") if accepted else None
    return dict(row=row, components=components, joins=joins,
                status="accept" if accepted else "unresolved", closure_reason=mechanism)


def symmetry_audit(records, sources):
    def key(src):
        return tuple((tuple(src[r]["root_boundary"]), tuple(map(tuple, src[r]["forbidden"]))) for r in ("z", "w"))
    source_lookup = {key(s): s["id"] for s in sources}
    lookup = {(r["source_id"], r["supports"]): r for r in records}
    def moved_join(j):
        return (tuple(tuple(sorted(PI[c] for c in f)) for f in j["forbidden_sets"]),
                tuple(tuple(sorted(PI[c] for c in e)) for e in j["residuals"]),
                tuple(j["obstruction_reasons"]))
    count = 0
    for record in records:
        src = sources[record["source_id"]]
        moved_key = tuple((tuple(sorted(RHO[i] for i in src[r]["root_boundary"])),
                           tuple(tuple(sorted(PI[c] for c in f)) for f in src[r]["forbidden"])) for r in ("z", "w"))
        sid = source_lookup[moved_key]
        supports = tuple(tuple(sorted(RHO[i] for i in s)) for s in record["supports"])
        supports = (supports[0], *sorted(supports[1:3]), *supports[3:])
        record["reflected_id"] = lookup[sid, supports]["id"]
        record["reflected_raw_targets"] = []
        for before in record["targets"]:
            row = tuple(PI[before["row"][RHO[i]]] for i in range(5))
            after = row_evidence(sources[sid], supports, row)
            assert before["status"] == after["status"]
            assert {moved_join(j) for j in before["joins"]} == {
                (tuple(map(tuple, j["forbidden_sets"])), tuple(map(tuple, j["residuals"])),
                 tuple(j["obstruction_reasons"])) for j in after["joins"]}
            record["reflected_raw_targets"].append(row)
            count += 1
    return count


def build():
    original = json.loads(SOURCE.read_text())
    sources = bind_sources(original)
    geometry = geometries()
    assert set(geometry) == independent_geometries()
    schemas = schema_audit()
    source_lookup = {}
    for src in sources:
        key = tuple(src["z"]["root_boundary"]), tuple(src["w"]["root_boundary"])
        source_lookup.setdefault(key, []).append(src)
    records, geometry_records, templates = [], [], []
    template_ids = {}
    for supports, placements in sorted(geometry.items()):
        gid = len(geometry_records)
        for placement in placements:
            order = placement["order"]
            if order not in template_ids:
                template_ids[order] = len(templates)
                templates.append(dict(id=len(templates), order=order, contact_rotations=rotations(order)))
            placement["rotation_template_id"] = template_ids[order]
        geometry_records.append(dict(id=gid, supports=supports, placements=placements))
        key = tuple(s[0] for s in supports[1:3]), supports[5]
        for src in source_lookup.get(key, []):
            if not all(len({Q[i] for i in supports[pos]}) >= 2
                       and valid_q_support(supports[pos], tuple(src[root]["forbidden"][col]))
                       for _, root, col, pos, _ in COMPONENTS):
                continue
            ids = {name: stable_schema_ids(src[root]["forbidden"][col][0], supports[pos])
                   for name, root, col, pos, k in COMPONENTS if k == 2}
            assert all(ids.values())
            q = row_evidence(src, supports, Q)
            assert len(q["joins"]) == 1 and q["joins"][0]["residuals"] == ([src["common"]],) * 2
            records.append(dict(id=len(records), source_id=src["id"], source_side_ids=src["side_ids"],
                                geometry_id=gid, supports=supports, common=src["common"],
                                q_schema_ids=ids, q_single_contact_relation=((src["w"]["forbidden"][1][0],),),
                                q=q, targets=[row_evidence(src, supports, row) for row in TARGETS]))
    reflected = symmetry_audit(records, sources)
    fibers = [dict(source_id=s["id"], side_ids=s["side_ids"],
                   support_record_ids=[r["id"] for r in records if r["source_id"] == s["id"]]) for s in sources]
    queries = [dict(record_id=r["id"], source_id=r["source_id"], target_index=i, row=t["row"],
                    failing_joins=[j for j in t["joins"] if not j["root_pairs"]])
               for r in records for i, t in enumerate(r["targets"]) if t["status"] == "unresolved"]
    reasons = Counter(reason for q in queries for j in q["failing_joins"] for reason in j["obstruction_reasons"])
    closures = Counter(t["closure_reason"] for r in records for t in r["targets"] if t["closure_reason"])
    outcomes = Counter(tuple(t["status"] for t in r["targets"]) for r in records)
    assert len(geometry) == sum(map(len, geometry.values())) == 3150
    assert len(records) == 560 and len(queries) == 118
    assert outcomes == {("accept", "accept"): 442, ("accept", "unresolved"): 59,
                        ("unresolved", "accept"): 59}
    assert reasons == {"empty_z": 60, "empty_w": 68, "same_singleton": 18}
    assert closures == {"complete_relation_transport": 724, "transport_and_capacity_bound": 278}
    assert sum(not f["support_record_ids"] for f in fibers) == 70
    assert (queries[0]["record_id"], queries[0]["target_index"]) == (14, 0)
    summary = dict(original_frontier=len(sources), geometric_supports=len(geometry),
                   placements=sum(map(len, geometry.values())), necessary_support_records=len(records),
                   source_records_with_support=sum(bool(f["support_record_ids"]) for f in fibers),
                   empty_source_fibers=sum(not f["support_record_ids"] for f in fibers),
                   target_queries=2 * len(records), target_accepts=2 * len(records) - len(queries),
                   unresolved_target_queries=len(queries), closure_reasons=dict(sorted(closures.items())),
                   failing_candidate_causes=dict(sorted(reasons.items())),
                   target_candidate_joins=sum(len(t["joins"]) for r in records for t in r["targets"]),
                   literal_target_reflections=reflected, support_records_excluded=0)
    inputs = [str(SOURCE.relative_to(ROOT))] + ["scripts/" + name + ".py" for name in (
        "c5_adjacent_degree5_no_mixed_t2", "c5_adjacent_degree5_mixed_edge_shared",
        "c5_adjacent_degree5_singleton_long_arc", "c5_root_degree_excess", "c5_single_spoke_cores")]
    return dict(schema=1, scope="necessary same-source supports and complete relation bounds; no disk realization or Lean theorem",
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                summary=summary, original_records=sources, source_fibers=fibers,
                geometries=geometry_records, rotation_templates=templates,
                q_complete_binary_schemas=schemas, records=records, open_queries=queries)


def render(data):
    lines = ["# 無 mixed：t_z=2,(2)，t_w=1,(2,1) 的必要支援", "",
             "支援順序 Cz / z0 / z1 / Cw / Dw / w0；Dw 是原單接點分量，不是 root-spoke。",
             "所有原 source 兩側 (D,O,kappa)=(1,0,0)，w 的分量缺額為 (1,0)。",
             "A 表示所有完整禁色上界接合皆接受；? 是未決，均未證來源可實現性。", "",
             "| ID | 原子表 ID | 原側 IDs | 實際支援 | p₁ 關閉原因 | p₂ 關閉原因 |",
             "| ---: | ---: | --- | --- | --- | --- |"]
    for r in data["records"]:
        supports = " / ".join("".join(map(str, s)) for s in r["supports"])
        statuses = [t["closure_reason"] or "?" for t in r["targets"]]
        lines.append(f'| {r["id"]} | {r["source_id"]} | {r["source_side_ids"]} | {supports} | {statuses[0]} | {statuses[1]} |')
    lines += ["", "## 原 136 份資料的完整纖維", "",
              "| 原子表 ID | 原側 IDs | 支援筆數 |", "| ---: | --- | ---: |"]
    for f in data["source_fibers"]:
        lines.append(f'| {f["source_id"]} | {f["side_ids"]} | {len(f["support_record_ids"])} |')
    lines += ["", "逐候選拒絕原因、完整 schemas、五接點 rotations 與原 ID／SHA 見 [JSON](observations.json)。",
              "任意大小覆蓋及界線見 [研究報告](../../docs/c5_adjacent_degree5_no_mixed_t2_t1.md)。", ""]
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
