#!/usr/bin/env python3
"""No-mixed t_z=2,(2), t_w=0,(2,1,1): budgets, supports and rejection causes.

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
HANDOFF = ROOT / "artifacts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_no_mixed_t2_t0_singles/observations.json"
TABLE = OUT.with_name("support_table.md")
NAMES = ("Cz", "z0", "z1", "Cw", "Dw", "Ew")
COMPONENTS = (("Cz", "z", 0, 0, 2), ("Cw", "w", 0, 3, 2), ("Dw", "w", 1, 4, 1), ("Ew", "w", 2, 5, 1))


def cardinalities(name):
    return range(2, 6) if name in ("Cz", "Cw", "Dw", "Ew") else (1,)


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
        expansion["Ew"] = ("Ew_0",)
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


def verify_placement(supports, placement, contact_rotations):
    """Check named incidences and lifts independently of their generators."""
    order = placement["order"]
    assert len(order) == len(NAMES) and set(order) == set(NAMES) and order[0] == "Cz"
    side = [n in NAMES[:3] for n in order]
    assert sum(side[i] != side[i - 1] for i in range(6)) == 2
    lifts = dict(zip(NAMES, placement["lifts"], strict=True))
    assert len(supports) == 6 and 0 <= placement["anchor"] < 5
    assert min(lifts["Cz"]) == 0 and max(lifts[order[-1]]) <= 5
    for i, (name, support) in enumerate(zip(NAMES, supports, strict=True)):
        values = lifts[name]
        assert tuple(sorted(set(values))) == tuple(values)
        assert len(values) in cardinalities(name) and max(values) - min(values) < 5
        assert tuple(sorted((placement["anchor"] + j) % 5 for j in values)) == tuple(support)
    assert supports[1] < supports[2]
    assert all(max(lifts[a]) <= min(lifts[b]) for a, b in zip(order, order[1:]))
    assert sum(max(lifts[n]) - min(lifts[n]) for n, _, _, _, _ in COMPONENTS) >= 4
    expected = {"z": {"w", "Cz_0", "Cz_1", "z0", "z1"},
                "w": {"z", "Cw_0", "Cw_1", "Dw_0", "Ew_0"}}
    assert len(contact_rotations) == 4
    assert {tuple(r["contact_flips"]) for r in contact_rotations} == set(product((False, True), repeat=2))
    for record in contact_rotations:
        word = record["neighborhood_word"]
        assert len(word) == len(set(word)) == 8
        assert set(word) == (expected["z"] | expected["w"]) - {"z", "w"}
        compressed = []
        for port in word:
            unit = port.split("_")[0]
            if not compressed or compressed[-1] != unit:
                compressed.append(unit)
        assert tuple(compressed) == tuple(order)
        for name, flip in zip(("Cz", "Cw"), record["contact_flips"], strict=True):
            ports = [name + "_0", name + "_1"]
            assert [p for p in word if p.startswith(name + "_")] == (ports[::-1] if flip else ports)
        for root, other, units in (("z", "w", NAMES[:3]), ("w", "z", NAMES[3:])):
            rotation = record["root_rotations"][root]
            assert len(rotation) == 5 and set(rotation) == expected[root] and rotation[0] == other
            start = next(i for i, p in enumerate(word)
                         if p.split("_")[0] in units and word[i - 1].split("_")[0] not in units)
            assert tuple(rotation[1:]) == tuple(word[(start + j) % 8] for j in range(4))


def bind_sources(data):
    sides = data["side_normal_forms"]
    records = []
    for join_id, (i, j) in enumerate(data["abstract_conditions"]["retained"]):
        z, w = sides[i], sides[j]
        if (len(z["root_boundary"]), z["ports"], len(w["root_boundary"]), w["ports"]) != (2, [2], 0, [2, 1, 1]):
            continue
        budgets = {r: budget(s) for r, s in (("z", z), ("w", w))}
        assert budgets["z"]["component_deficits"] == [1]
        assert budgets["w"]["component_deficits"] == [1, 0, 0]
        records.append(dict(id=len(records), retained_join_id=join_id, side_ids=(i, j),
                            common=z["common"], z=z, w=w, source_budgets=budgets))
    def key(s):
        return (tuple(s["z"]["root_boundary"]), tuple(s["w"]["root_boundary"]), s["common"],
                tuple(s["z"]["forbidden"][0]), tuple(map(tuple, s["w"]["forbidden"])))
    rebuilt = set()
    for sz in combinations(range(5), 2):
        if len({Q[i] for i in sz}) != 2:
            continue
        for c in sorted(U - {Q[i] for i in sz}):
            fz = tuple(sorted(U - {Q[i] for i in sz} - {c}))
            for a, b, e in permutations(sorted(U - {c})):
                rebuilt.add((sz, (), c, fz, ((a,), (b,), (e,))))
    assert {key(s) for s in records} == rebuilt and len(records) == 96
    assert (records[0]["retained_join_id"], records[0]["side_ids"]) == (3048, (133, 64))
    frontier = json.loads(HANDOFF.read_text())["next_frontier"]
    assert frontier["source_sha256"] == sha256(SOURCE.read_bytes()).hexdigest()
    assert frontier["records"] == [dict(retained_join_id=s["retained_join_id"], side_ids=list(s["side_ids"]))
                                   for s in records]
    assert frontier["first_sides"] == [records[0][r] for r in ("z", "w")]
    return records


def row_evidence(source, supports, row):
    components = [dict(name=name, **component_options(k, supports[pos], tuple(source[root]["forbidden"][col]), row))
                  for name, root, col, pos, k in COMPONENTS]
    joins = []
    for fz, fw, fd, fe in product(*(c["options"] for c in components)):
        ez = U - {row[i] for i in source["z"]["root_boundary"]} - set(fz)
        ew = U - {row[i] for i in source["w"]["root_boundary"]} - set(fw) - set(fd) - set(fe)
        pairs = sorted((a, b) for a, b in product(ez, ew) if a != b)
        direct = [(a, b) for a, b in product(range(4), repeat=2)
                  if a != b and a not in fz and b not in fw and b not in fd and b not in fe
                  and all(a != row[i] for i in source["z"]["root_boundary"])
                  and all(b != row[i] for i in source["w"]["root_boundary"])]
        assert pairs == direct
        # Exchange the entire root assignment, retaining the four components
        # on their renamed root and all original boundary incidences.
        swapped = [(a, b) for a, b in product(range(4), repeat=2)
                   if a != b and b not in fz and a not in fw and a not in fd and a not in fe
                   and all(b != row[i] for i in source["z"]["root_boundary"])
                   and all(a != row[i] for i in source["w"]["root_boundary"])]
        assert set(swapped) == {(b, a) for a, b in pairs}
        reasons = (["empty_z"] if not ez else []) + (["empty_w"] if not ew else [])
        if len(ez) == 1 and ez == ew:
            reasons.append("same_singleton")
        assert bool(reasons) == (not pairs)
        joins.append(dict(forbidden_sets=(fz, fw, fd, fe), residuals=(sorted(ez), sorted(ew)),
                          root_pairs=pairs, witness=pairs[0] if pairs else None,
                          obstruction_reasons=reasons))
    accepted = all(j["root_pairs"] for j in joins)
    mechanism = ("complete_relation_transport" if all(c["exact"] for c in components)
                 else "transport_and_capacity_bound") if accepted else None
    status = "accept" if accepted else "reject" if all(c["exact"] for c in components) else "unresolved"
    return dict(row=row, components=components, joins=joins, status=status, closure_reason=mechanism)


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


def singleton_swap_audit(records, sources, schemas):
    """Swap Dw and Ew as WHOLE components; never identify or merge them."""
    lookup = {(tuple(s["z"]["root_boundary"]), s["common"], tuple(map(tuple, s["w"]["forbidden"]))): s["id"]
              for s in sources}
    by_record = {(r["source_id"], r["supports"]): r for r in records}
    for record in records:
        src = sources[record["source_id"]]
        fs = src["w"]["forbidden"]
        sid = lookup[tuple(src["z"]["root_boundary"]), src["common"], (tuple(fs[0]), tuple(fs[2]), tuple(fs[1]))]
        supports = (*record["supports"][:4], record["supports"][5], record["supports"][4])
        twin = by_record[sid, supports]
        record["singleton_swapped_id"] = twin["id"]
        for t, u in zip(record["targets"], twin["targets"], strict=True):
            assert t["status"] == u["status"]
            def key(j, swap=False):
                f = j["forbidden_sets"]
                return (tuple(map(tuple, (f[0], f[1], f[3], f[2]) if swap else f)),
                        tuple(j["root_pairs"]))
            assert {key(j, True) for j in t["joins"]} == {key(j) for j in u["joins"]}
        # Literal reflection acts on the COMPLETE source relations as well.
        reflected = records[record["reflected_id"]]
        for name, root, col, _, arity in COMPONENTS:
            h = src[root]["forbidden"][col][0]
            if arity == 2:
                moved = {tuple(sorted(tuple(PI[c] for c in t) for t in schemas[h][i]))
                         for i in record["q_schema_ids"][name]}
                expected = {tuple(sorted(schemas[PI[h]][i])) for i in reflected["q_schema_ids"][name]}
                assert moved == expected
            else:
                assert reflected["q_single_contact_relations"][name] == ((PI[h],),)
    return len(records)


def negative_controls(geometry):
    """Guard the same-source distinctions used by this particular cover."""
    supports = ((0, 1), (0,), (4,), (1, 2), (2, 3), (3, 4))
    placement = geometry[supports][0]
    templates = rotations(placement["order"])
    broken = []
    changed = json.loads(json.dumps(placement))
    changed["order"] = ["Cz", "Cw", "z0", "Dw", "z1", "Ew"]
    broken.append(("interleaved_root_units", supports, changed, templates))
    changed = json.loads(json.dumps(placement))
    changed["lifts"][4] = [changed["lifts"][4][0]]
    bad_supports = (*supports[:4], (supports[4][0],), supports[5])
    broken.append(("single_contact_component_is_not_a_spoke", bad_supports, changed, templates))
    changed = json.loads(json.dumps(templates))
    changed[0]["root_rotations"]["w"][-1] = "Dw_0"
    broken.append(("merging_Dw_Ew_contacts", supports, placement, changed))
    changed = json.loads(json.dumps(templates))
    changed[0]["root_rotations"]["z"].remove("w")
    broken.append(("missing_original_zw", supports, placement, changed))
    for name, ss, p, ts in broken:
        try:
            verify_placement(ss, p, ts)
        except AssertionError:
            pass
        else:
            raise AssertionError(name)
    relation = ((0, 1), (2, 0))
    marginals = tuple(product({t[0] for t in relation}, {t[1] for t in relation}))
    assert set.intersection(*map(set, relation)) == {0}
    assert set.intersection(*map(set, marginals)) == set()
    assert not valid_q_support((), (0,)) and not valid_q_support((0, 2), (0,))
    assert not valid_q_support((0, 1), (3,))
    nonexact = component_options(2, (0, 1, 4), (0,), TARGETS[0])
    assert not nonexact["exact"] and (2, 3) in nonexact["options"]
    return [b[0] for b in broken] + ["binary_marginals_lose_the_complete_ban",
        "empty_or_monochromatic_source_support", "unseen_source_color_requires_three_seen_colors",
        "source_budget_is_not_a_target_singleton_bound"]


def next_frontier(data):
    """Read the next deficit subtable, without starting its support enumeration."""
    sides = data["side_normal_forms"]
    rows = []
    for i, pair in enumerate(data["abstract_conditions"]["retained"]):
        z, w = (sides[j] for j in pair)
        if (len(z["root_boundary"]), z["ports"], len(w["root_boundary"]), w["ports"],
            w["capacity_deficit"], w["overlap_excess"]) == (2, [2], 0, [2, 2], 1, 0):
            rows.append(dict(retained_join_id=i, side_ids=pair))
    assert len(rows) == 96 and rows[0] == dict(retained_join_id=3036, side_ids=[133, 16])
    return dict(scope="t_z=2,(2), t_w=0,(2,2), D_w=1,O_w=0; no support coverage yet",
                source_path=str(SOURCE.relative_to(ROOT)), source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
                records=rows, first_sides=[sides[i] for i in rows[0]["side_ids"]])


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
            verify_placement(supports, placement, templates[template_ids[order]]["contact_rotations"])
        geometry_records.append(dict(id=gid, supports=supports, placements=placements))
        key = tuple(s[0] for s in supports[1:3]), ()
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
                                q_schema_ids=ids, q_single_contact_relations={name: ((src[root]["forbidden"][col][0],),)
                                                           for name, root, col, _, k in COMPONENTS if k == 1},
                                q=q, targets=[row_evidence(src, supports, row) for row in TARGETS]))
    reflected = symmetry_audit(records, sources)
    singleton_swaps = singleton_swap_audit(records, sources, schemas)
    fibers = [dict(source_id=s["id"], side_ids=s["side_ids"],
                   support_record_ids=[r["id"] for r in records if r["source_id"] == s["id"]]) for s in sources]
    queries = [dict(record_id=r["id"], source_id=r["source_id"], target_index=i, row=t["row"],
                    failing_joins=[j for j in t["joins"] if not j["root_pairs"]])
               for r in records for i, t in enumerate(r["targets"]) if t["status"] != "accept"]
    reasons = Counter(reason for q in queries for j in q["failing_joins"] for reason in j["obstruction_reasons"])
    closures = Counter(t["closure_reason"] for r in records for t in r["targets"] if t["closure_reason"])
    outcomes = Counter(tuple(t["status"] for t in r["targets"]) for r in records)
    assert len(geometry) == sum(map(len, geometry.values())) == 480
    assert len(records) == 120 and not queries and not reasons
    assert outcomes == {("accept", "accept"): 120}
    assert closures == {"complete_relation_transport": 216, "transport_and_capacity_bound": 24}
    assert sum(not f["support_record_ids"] for f in fibers) == 60
    assert {r["common"] for r in records} == {3}
    for r in records:
        for t in r["targets"]:
            assert all(c["exact"] for c in t["components"][1:])
            if not t["components"][0]["exact"]:
                assert len(t["joins"]) == 5
                assert all(any(a != 3 and b == 3 for a, b in j["root_pairs"]) for j in t["joins"])
    summary = dict(original_frontier=len(sources), geometric_supports=len(geometry),
                   placements=sum(map(len, geometry.values())), necessary_support_records=len(records),
                   source_records_with_support=sum(bool(f["support_record_ids"]) for f in fibers),
                   empty_source_fibers=sum(not f["support_record_ids"] for f in fibers),
                   target_queries=2 * len(records), target_accepts=2 * len(records) - len(queries),
                   unresolved_target_queries=len(queries), closure_reasons=dict(sorted(closures.items())),
                   failing_candidate_causes=dict(sorted(reasons.items())),
                   target_candidate_joins=sum(len(t["joins"]) for r in records for t in r["targets"]),
                   literal_target_reflections=reflected, whole_singleton_swaps=singleton_swaps,
                   whole_root_swap_joins=sum(len(t["joins"]) for r in records for t in [r["q"], *r["targets"]]),
                   contact_rotation_checks=4 * sum(map(len, geometry.values())),
                   support_records_excluded=0)
    assert summary["target_candidate_joins"] == 336 and summary["whole_root_swap_joins"] == 456
    inputs = [str(p.relative_to(ROOT)) for p in (SOURCE, HANDOFF)] + ["scripts/" + name + ".py" for name in (
        "c5_adjacent_degree5_no_mixed_t2", "c5_adjacent_degree5_mixed_edge_shared",
        "c5_adjacent_degree5_singleton_long_arc", "c5_root_degree_excess", "c5_single_spoke_cores")]
    return dict(schema=1, scope="necessary same-source supports and complete relation bounds; no disk realization or Lean theorem",
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                summary=summary, original_records=sources, source_fibers=fibers,
                geometries=geometry_records, rotation_templates=templates,
                q_complete_binary_schemas=schemas, records=records, open_queries=queries,
                negative_controls=negative_controls(geometry), next_frontier=next_frontier(original))


def render(data):
    lines = ["# 無 mixed：t_z=2,(2)，t_w=0,(2,1,1) 的必要支援", "",
             "支援順序 Cz / z0 / z1 / Cw / Dw / Ew；Dw、Ew 是兩個原單接點分量，均不是 root-spoke。",
             "所有原 source 兩側 (D,O,kappa)=(1,0,0)，w 的分量缺額為 (1,0,0)。",
             "A 表示所有完整禁色上界接合皆接受；? 是未決，均未證來源可實現性。", "",
             "| ID | 原子表 ID | 原側 IDs | 實際支援 | p₁ 關閉原因 | p₂ 關閉原因 |",
             "| ---: | ---: | --- | --- | --- | --- |"]
    for r in data["records"]:
        supports = " / ".join("".join(map(str, s)) for s in r["supports"])
        statuses = [t["closure_reason"] or "?" for t in r["targets"]]
        lines.append(f'| {r["id"]} | {r["source_id"]} | {r["source_side_ids"]} | {supports} | {statuses[0]} | {statuses[1]} |')
    lines += ["", "## 原 96 份資料的完整纖維", "",
              "| 原子表 ID | 原側 IDs | 支援筆數 |", "| ---: | --- | ---: |"]
    for f in data["source_fibers"]:
        lines.append(f'| {f["source_id"]} | {f["side_ids"]} | {len(f["support_record_ids"])} |')
    lines += ["", "逐候選拒絕原因、完整 schemas、六接點 rotations 與原 ID／SHA 見 [JSON](observations.json)。",
              "任意大小覆蓋及界線見 [研究報告](../../docs/c5_adjacent_degree5_no_mixed_t2_t0_singles.md)。", ""]
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
