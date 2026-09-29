#!/usr/bin/env python3
"""No mixed, two spokes on both roots: actual-support order and target bounds.

The arbitrary-size disk reduction is a paper proof. These are necessary data,
not source realizations; an unresolved upper-bound join is not a counterexample.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_mixed_edge_shared import schemas_for
from c5_adjacent_degree5_singleton_long_arc import component_options, valid_q_support
from c5_single_spoke_cores import Q, U, TARGETS, PERMS, PI, RHO

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_no_mixed/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_no_mixed_t2/observations.json"
TABLE = OUT.with_name("support_table.md")
NAMES = ("Cz", "z0", "z1", "Cw", "w0", "w1")


def geometries():
    """Six units on the boundary of a neighborhood of the ORIGINAL edge zw."""
    choices = {n: [s for k in (range(2, 6) if n.startswith("C") else (1,))
                   for s in combinations(range(6), k) if max(s) - min(s) < 5]
               for n in NAMES}
    orders = set()
    for z, w in product(permutations(NAMES[:3]), permutations(NAMES[3:])):
        order = z + w
        i = order.index("Cz")
        orders.add(order[i:] + order[:i])
    result = {}
    for order in sorted(orders):
        def visit(j, end, assigned):
            if j == len(NAMES):
                for anchor in range(5):
                    supports = tuple(tuple(sorted((anchor + i) % 5 for i in assigned[n]))
                                     for n in NAMES)
                    # The two original spokes at each root are named by boundary index.
                    if supports[1] >= supports[2] or supports[4] >= supports[5]:
                        continue
                    placement = dict(order=order, anchor=anchor,
                                     lifts=tuple(assigned[n] for n in NAMES))
                    result.setdefault(supports, []).append(placement)
                return
            for support in choices[order[j]]:
                if min(support) >= end and (j or min(support) == 0):
                    visit(j + 1, max(support), assigned | {order[j]: support})
        visit(0, 0, {})
    assert len(result) == 2550 and sum(map(len, result.values())) == 2560
    return result


def independent_geometries():
    """Whole-side cyclic hull edge masks; no permutation/ordered-lift recursion."""
    sides = []
    for k in range(2, 6):
        for component in combinations(range(5), k):
            for spokes in combinations(range(5), 2):
                for anchor in sorted(set(component + spokes)):
                    cs = sorted((i - anchor) % 5 for i in component)
                    ss = sorted((i - anchor) % 5 for i in spokes)
                    if any(cs[0] < i < cs[-1] for i in ss):
                        continue
                    span = max(cs + ss)
                    mask = sum(1 << ((anchor + j) % 5) for j in range(span))
                    sides.append((component, tuple((i,) for i in spokes), mask))
    assert len(sides) == 370
    return {(a[0], *a[1], b[0], *b[1]) for a, b in product(sides, repeat=2)
            if not a[2] & b[2]}


def contact_rotations(placement):
    order = placement["order"]
    result = []
    for flips in product((False, True), repeat=2):
        expanded = {n: (n,) for n in NAMES}
        for j, name in enumerate(("Cz", "Cw")):
            ports = (name + "_0", name + "_1")
            expanded[name] = ports[::-1] if flips[j] else ports
        rotations = {}
        for root, own, other in (("z", NAMES[:3], "w"), ("w", NAMES[3:], "z")):
            start = next(i for i, n in enumerate(order) if n in own and order[i - 1] not in own)
            units = tuple(order[(start + j) % 6] for j in range(3))
            assert set(units) == set(own)
            rotations[root] = (other,) + tuple(p for n in units for p in expanded[n])
            assert len(rotations[root]) == len(set(rotations[root])) == 5
        result.append(dict(contact_flips=flips, root_rotations=rotations,
                           neighborhood_word=tuple(p for n in order for p in expanded[n])))
    return result


def bind_sources(data):
    sides = data["side_normal_forms"]
    selected = [r for r in sides if len(r["root_boundary"]) == 2 and r["ports"] == [2]]
    rebuilt = set()
    for sz, sw in product(combinations(range(5), 2), repeat=2):
        if len({Q[i] for i in sz}) != 2 or len({Q[i] for i in sw}) != 2:
            continue
        for common in U - {Q[i] for i in sz + sw}:
            rebuilt.add((sz, sw, common))
    records = []
    for source_id, (i, j) in enumerate(data["abstract_conditions"]["two_spoke_frontier"]):
        z, w = sides[i], sides[j]
        assert z in selected and w in selected and z["common"] == w["common"]
        for side in (z, w):
            assert set(side["forbidden"][0]) == U - {Q[k] for k in side["root_boundary"]} - {side["common"]}
        records.append(dict(id=source_id, side_ids=(i, j), common=z["common"], z=z, w=w))
    keys = {(tuple(r["z"]["root_boundary"]), tuple(r["w"]["root_boundary"]), r["common"])
            for r in records}
    assert keys == rebuilt and len(records) == len(rebuilt) == 88
    return records


def schema_audit():
    """Independently scan ALL nonempty binary relations, including diagonal tuples."""
    pairs = tuple(product(range(4), repeat=2))
    found = {h: [] for h in range(4)}
    for mask in range(1, 1 << 16):
        relation = tuple(p for i, p in enumerate(pairs) if mask >> i & 1)
        ban = set.intersection(*(set(p) for p in relation))
        if len(ban) != 1:
            continue
        h = next(iter(ban))
        if all(any(t[j] == h and t[1 - j] != h for t in relation) for j in range(2)):
            found[h].append(relation)
    schemas = {h: schemas_for({h}) for h in range(4)}
    for h in range(4):
        assert len(schemas[h]) == 95
        assert set(found[h]) == {tuple(s) for s in schemas[h]}
    return schemas


@lru_cache(None)
def stable_schema_ids(h, support):
    stabilizer = [p for p in PERMS if all(p[Q[i]] == Q[i] for i in support)]
    return [i for i, rel in enumerate(schemas_for({h})) if all(
        {tuple(p[c] for c in t) for t in rel} == set(rel) for p in stabilizer)]


def row_evidence(source, supports, row):
    components = [component_options(2, supports[j], tuple(source[root]["forbidden"][0]), row)
                  for root, j in (("z", 0), ("w", 3))]
    joins = []
    for fz, fw in product(*(c["options"] for c in components)):
        ez = U - {row[i] for i in source["z"]["root_boundary"]} - set(fz)
        ew = U - {row[i] for i in source["w"]["root_boundary"]} - set(fw)
        pairs = sorted((a, b) for a, b in product(ez, ew) if a != b)
        # Direct same-root-pair check keeps zw and ALL FOUR actual spokes.
        direct = [(a, b) for a, b in product(range(4), repeat=2)
                  if a != b and a not in fz and b not in fw
                  and all(a != row[i] for i in source["z"]["root_boundary"])
                  and all(b != row[i] for i in source["w"]["root_boundary"])]
        assert pairs == direct
        reason = None if pairs else ("empty_z" if not ez else "empty_w" if not ew else "same_singleton")
        assert bool(pairs) == bool(ez and ew and not (len(ez) == 1 and ez == ew))
        joins.append(dict(forbidden_sets=(fz, fw), residuals=(sorted(ez), sorted(ew)),
                          root_pairs=pairs, witness=pairs[0] if pairs else None,
                          obstruction=reason))
    return dict(row=row, components=components, joins=joins,
                status="accept" if all(j["root_pairs"] for j in joins) else "unresolved")


def symmetry_audit(records, sources):
    lookup = {(r["source_id"], r["supports"]): r for r in records}
    source_keys = {(tuple(s["z"]["root_boundary"]), tuple(s["w"]["root_boundary"]), s["common"]): s
                   for s in sources}
    reflection_count = 0
    for r in records:
        src = sources[r["source_id"]]
        sz, sw = (tuple(src[root]["root_boundary"]) for root in ("z", "w"))
        swapped_src = source_keys[sw, sz, src["common"]]
        swapped = lookup[swapped_src["id"], r["supports"][3:] + r["supports"][:3]]
        r["root_swapped_id"] = swapped["id"]
        for before, after in zip(r["targets"], swapped["targets"]):
            assert before["status"] == after["status"]
            old = {(tuple(j["forbidden_sets"][::-1]), tuple(map(tuple, j["residuals"][::-1])))
                   for j in before["joins"]}
            new = {(tuple(j["forbidden_sets"]), tuple(map(tuple, j["residuals"]))) for j in after["joins"]}
            assert old == new
        moved_spokes = tuple(tuple(sorted(RHO[i] for i in s)) for s in (sz, sw))
        reflected_src = source_keys[*moved_spokes, PI[src["common"]]]
        moved_supports = []
        for offset in (0, 3):
            moved_supports.append(tuple(sorted(RHO[i] for i in r["supports"][offset])))
            moved_supports.extend(sorted((RHO[r["supports"][offset + j][0]],) for j in (1, 2)))
        reflected = lookup[reflected_src["id"], tuple(moved_supports)]
        r["reflected_id"] = reflected["id"]
        r["reflected_raw_targets"] = []
        for before in r["targets"]:
            moved_row = tuple(PI[before["row"][RHO[i]]] for i in range(5))
            after = row_evidence(reflected_src, tuple(moved_supports), moved_row)
            assert before["status"] == after["status"]
            old = {(tuple(tuple(sorted(PI[c] for c in f)) for f in j["forbidden_sets"]),
                    tuple(tuple(sorted(PI[c] for c in e)) for e in j["residuals"])) for j in before["joins"]}
            new = {(tuple(j["forbidden_sets"]), tuple(map(tuple, j["residuals"]))) for j in after["joins"]}
            assert old == new
            r["reflected_raw_targets"].append(moved_row)
            reflection_count += 1
    return dict(root_swaps=len(records), literal_target_reflections=reflection_count)


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
    records, geometry_records, rotation_templates = [], [], []
    rotation_ids = {}
    for supports, placements in sorted(geometry.items()):
        gid = len(geometry_records)
        for placement in placements:
            order = placement["order"]
            if order not in rotation_ids:
                rotation_ids[order] = len(rotation_templates)
                rotation_templates.append(dict(id=len(rotation_templates), order=order,
                                               contact_rotations=contact_rotations(placement)))
            placement["rotation_template_id"] = rotation_ids[order]
            assert contact_rotations(placement) == rotation_templates[rotation_ids[order]]["contact_rotations"]
        geometry_records.append(dict(id=gid, supports=supports, placements=placements))
        key = tuple(s[0] for s in supports[1:3]), tuple(s[0] for s in supports[4:6])
        for src in source_lookup.get(key, []):
            if not all(valid_q_support(supports[j], tuple(src[root]["forbidden"][0]))
                       for root, j in (("z", 0), ("w", 3))):
                continue
            schema_ids = [stable_schema_ids(src[root]["forbidden"][0][0], supports[j])
                          for root, j in (("z", 0), ("w", 3))]
            assert all(schema_ids)
            q = row_evidence(src, supports, Q)
            assert len(q["joins"]) == 1 and q["joins"][0]["residuals"] == ([src["common"]],) * 2
            targets = [row_evidence(src, supports, row) for row in TARGETS]
            records.append(dict(id=len(records), source_id=src["id"], source_side_ids=src["side_ids"],
                                geometry_id=gid, supports=supports, common=src["common"],
                                q_schema_ids=schema_ids, q=q, targets=targets))
    assert len(records) == 322
    fibers = [dict(source_id=src["id"], side_ids=src["side_ids"],
                   support_record_ids=[r["id"] for r in records if r["source_id"] == src["id"]])
              for src in sources]
    symmetries = symmetry_audit(records, sources)
    queries = [dict(record_id=r["id"], source_id=r["source_id"], target_index=i, row=t["row"],
                    failing_joins=[j for j in t["joins"] if not j["root_pairs"]])
               for r in records for i, t in enumerate(r["targets"]) if t["status"] == "unresolved"]
    counts = Counter(tuple(t["status"] for t in r["targets"]) for r in records)
    assert counts == {("accept", "accept"): 206, ("accept", "unresolved"): 50,
                      ("unresolved", "accept"): 50, ("unresolved", "unresolved"): 16}
    assert len(queries) == 132 and sum(not f["support_record_ids"] for f in fibers) == 46
    # These allow component intervals separately, but violate the same-source root grouping.
    nongrouped = ((0, 1), (2,), (4,), (2, 3), (0,), (4,))
    assert nongrouped not in geometry
    # Multiplying marginals destroys the exact singleton ban.
    relation = ((1, 0), (2, 1))
    marginal_product = set(product({t[0] for t in relation}, {t[1] for t in relation}))
    assert set.intersection(*(set(t) for t in relation)) == {1}
    assert not set.intersection(*(set(t) for t in marginal_product))
    negatives = dict(root_grouping_violation=nongrouped,
                     relation=relation, wrong_marginal_product=sorted(marginal_product),
                     empty_residual_query=queries[0])
    inputs = ["scripts/c5_adjacent_degree5_mixed_edge_shared.py",
              "scripts/c5_adjacent_degree5_singleton_long_arc.py", "scripts/c5_single_spoke_cores.py"]
    summary = dict(original_frontier=88, source_records_with_support=42, empty_source_fibers=46,
                   geometric_supports=len(geometry), placements=sum(map(len, geometry.values())),
                   contact_rotation_controls=4 * sum(map(len, geometry.values())),
                   necessary_support_records=322, both_targets_proved=206,
                   target_queries=644, target_accepts=512, unresolved_target_queries=len(queries),
                   target_candidate_joins=sum(len(t["joins"]) for r in records for t in r["targets"]),
                   binary_relations_checked=65535, schemas_per_singleton=95,
                   common_colors=dict(sorted(Counter(r["common"] for r in records).items())),
                   **symmetries)
    return dict(schema=1, scope="necessary actual supports and rotations; partial target bounds; no disk realizations or Lean theorem",
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                original_source_path=str(SOURCE.relative_to(ROOT)),
                original_source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
                original_source_ids_bound=True,
                inputs_sha256={p: sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs},
                summary=summary, original_records=sources, source_fibers=fibers,
                geometries=geometry_records, rotation_templates=rotation_templates,
                q_complete_schemas=schemas, records=records,
                open_queries=queries, negative_controls=negatives)


def render(data):
    lines = ["# 無 mixed、兩側 t=2,(2)：同源必要支援與指定查詢", "",
             "這些是必要資料，並非來源圖或 disk 實現。支援順序為 Cz / z0 / z1 / Cw / w0 / w1。",
             "原分量、兩個接點次序、四條 spokes 與原 zw 皆保留；A 為全部候選皆接受，? 為上界未決。", "",
             "| ID | 原 frontier ID | 原側 IDs | actual supports | c | p₁ | p₂ | 反射 ID |",
             "| ---: | ---: | --- | --- | ---: | --- | --- | ---: |"]
    for r in data["records"]:
        supports = " / ".join("".join(map(str, s)) for s in r["supports"])
        outcomes = ["A" if t["status"] == "accept" else "?" for t in r["targets"]]
        lines.append(f'| {r["id"]} | {r["source_id"]} | {r["source_side_ids"]} | {supports} | '
                     f'{r["common"]} | {outcomes[0]} | {outcomes[1]} | {r["reflected_id"]} |')
    lines += ["", "## 原 88 份資料的完整纖維", "",
              "| 原 frontier ID | 原側 IDs | 支援筆數 |", "| ---: | --- | ---: |"]
    for f in data["source_fibers"]:
        lines.append(f'| {f["source_id"]} | {f["side_ids"]} | {len(f["support_record_ids"])} |')
    lines += ["", "全部 placements、具名 root rotations、完整 q schemas、逐候選 joins 及未決見證見",
              "[JSON](observations.json)；任意大小覆蓋與界線見",
              "[研究報告](../../docs/c5_adjacent_degree5_no_mixed_t2.md)。", ""]
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
