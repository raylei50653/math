#!/usr/bin/env python3
"""Original quadrilateral order excludes sole mixed K2 with one port per root.

Paper topology supplies the arbitrary-size cover. This checker audits finite
support constraints and inherited abstract IDs, not graph realizability.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_order/observations.json"
TABLE = OUT.with_name("exclusion_table.md")
Q = (0, 1, 0, 1, 2)
U = frozenset(range(4))
PERMS = tuple(permutations(range(4)))
RHO = (3, 2, 1, 0, 4)
PI = (1, 0, 2, 3)
SUPPORTS = tuple(s for n in range(1, 6) for s in combinations(range(5), n))
NAMES = ("Cs", "ps", "pl", "Cl")


@lru_cache(None)
def stable(support, forbidden):
    seen = {Q[i] for i in support}
    return all({p[c] for c in forbidden} == set(forbidden)
               for p in PERMS if all(p[c] == c for c in seen))


@lru_cache(None)
def arcs(support):
    """All positive proper cyclic hulls, including non-shortest choices."""
    result = []
    for start in support:
        length = max((i - start) % 5 for i in support)
        if length:
            result.append((start, length,
                           sum(1 << ((start + j) % 5) for j in range(length))))
    return tuple(result)


def support_catalogue():
    records = []
    for n in (1, 2):
        for forbidden in combinations(range(4), n):
            candidates = [s for s in SUPPORTS
                          if len({Q[i] for i in s}) >= 2 and stable(s, forbidden)]
            lower = min(length for s in candidates for _, length, _ in arcs(s))
            assert lower == (2 if forbidden == (3,) else 1)
            records.append(dict(forbidden=forbidden, supports=candidates, min_span=lower))
    assert [s for s in SUPPORTS if stable(s, (3,))] == [
        s for s in SUPPORTS if len({Q[i] for i in s}) == 3]
    return records


def independent_packings():
    """Exhaust all disjoint hull-edge masks, without an order or span bound."""
    choices = [(s, a) for s in SUPPORTS if len(s) >= 2 for a in arcs(s)]
    found = {}

    def visit(items, used):
        if len(items) == 4:
            supports = tuple(s for s, _ in items)
            assert supports not in found  # Four positive spans force unique hulls.
            found[supports] = tuple(a for _, a in items)
            return
        for support, arc in choices:
            if not used & arc[2]:
                visit(items + ((support, arc),), used | arc[2])
    visit((), 0)
    assert len(found) == 360
    return found


def saturated_geometries():
    """Original role order Cs,ps,pl,Cl or its reverse, with spans 1,1,1,2."""
    result = []
    for anchor in range(5):
        for forward in (True, False):
            order = ("Cl", "Cs", "ps", "pl") if forward else ("Cl", "pl", "ps", "Cs")
            lifted, cursor = {}, anchor
            for name in order:
                span = 2 if name == "Cl" else 1
                lifted[name] = tuple(range(cursor, cursor + span + 1))
                cursor += span
            supports = {k: tuple(sorted(i % 5 for i in v)) for k, v in lifted.items()}
            assert cursor == anchor + 5
            result.append(dict(id=len(result), order=order, lifts=lifted, supports=supports))
    packed = independent_packings()
    filtered = set()
    for ss, aa in packed.items():
        if tuple(a[1] for a in aa) != (1, 1, 1, 2) or len(ss[3]) != 3:
            continue
        # Recover the circular order from hull starting points, independently.
        cycle = tuple(sorted(range(4), key=lambda j: aa[j][0]))
        start = cycle.index(0)
        cycle = cycle[start:] + cycle[:start]
        if cycle in ((0, 1, 2, 3), (0, 3, 2, 1)):
            filtered.add(ss)
    assert filtered == {tuple(g["supports"][k] for k in NAMES) for g in result}
    assert len(result) == 10
    # Shared endpoints are allowed: four spans can tile all five edges.
    positive = ((0, 1), (1, 2), (2, 3), (0, 3, 4))
    assert positive in packed
    # The two {3} unary supports need >=2 edges each, plus both K2 ends >=1.
    three_color = tuple(s for s in SUPPORTS if stable(s, (3,)))
    assert len(three_color) == 9
    actual_pairs = tuple((a, b) for a, b in product(combinations(range(5), 2), repeat=2)
                         if len({Q[i] for i in a}) == len({Q[i] for i in b}) == 2
                         and {Q[i] for i in a} != {Q[i] for i in b})
    narrow = [(cs, a, b, cl) for cs, cl in product(three_color, repeat=2)
              for a, b in actual_pairs]
    assert len(actual_pairs) == 40 and len(narrow) == 3240
    assert not any(ss in packed for ss in narrow)
    return result, dict(independent_four_unit_packings=len(packed),
                        shared_endpoint_positive=positive,
                        t2_relaxed_support_quadruples=len(narrow), t2_packings=0)


def six_cases(geometries):
    cases = []
    for g in geometries:
        s = g["supports"]
        if len({Q[i] for i in s["Cl"]}) != 3:
            continue
        d = next(iter({0, 1, 2} - {Q[i] for i in s["ps"]}))
        e = next(iter({0, 1, 2} - {Q[i] for i in s["pl"]}))
        reason = "equal_missing_colors" if d == e else "small_support_misses_residual"
        assert d == e or d not in {Q[i] for i in s["Cs"]}
        if d != e:
            assert d == 2 and s["Cs"] == (1, 2)
        cases.append(dict(geometry_id=g["id"], missing_small=d, missing_large=e,
                          reason=reason))
    assert Counter(c["reason"] for c in cases) == {
        "equal_missing_colors": 4, "small_support_misses_residual": 2}
    return cases


def saturation_check(record, geometry):
    small_root = record["small_root"]
    large_root = "w" if small_root == "z" else "z"
    small, large = record[small_root], record[large_root]
    s = geometry["supports"]
    roles = {"ps": "u" if small_root == "z" else "v",
             "pl": "v" if small_root == "z" else "u"}
    failures = []
    for role in ("ps", "pl"):
        original = roles[role]
        if {Q[i] for i in s[role]} != {0, 1, 2} - {record["missing_" + original]}:
            failures.append(original + "_q_support")
    for role, side in (("Cs", small), ("Cl", large)):
        if not stable(s[role], tuple(side["forbidden"][0])):
            failures.append(role + "_forbidden_stabilizer")
    assert failures
    # Keep original spoke landing options and both orientations of each pair.
    # These restrictions are not needed for exclusion; no spoke is replaced.
    endpoints = {role: (geometry["lifts"][role][0] % 5,
                        geometry["lifts"][role][-1] % 5) for role in ("Cs", "Cl")}
    spoke_choices = [(a, b) for a, b in product(endpoints["Cs"], endpoints["Cl"])
                    if Q[a] == small["spokes_colors"][0]
                    and Q[b] == large["spokes_colors"][0]]
    return dict(geometry_id=geometry["id"], failures=failures,
                named_mixed_roles=roles, spoke_landings_small_large=spoke_choices,
                binary_port_orientations=list(product(((0, 1), (1, 0)), repeat=2)))


def build():
    inherited = json.loads(SOURCE.read_text())
    catalogue = support_catalogue()
    lower = {tuple(c["forbidden"]): c["min_span"] for c in catalogue}
    geometries, controls = saturated_geometries()
    records, shapes = [], {}
    for r in inherited["abstract_relations"]:
        if not r["planar_necessary_retained"]:
            continue
        sr = r["small_root"]
        lr = "w" if sr == "z" else "z"
        small, large = r[sr], r[lr]
        spans = {root: [lower[tuple(f)] for f in r[root]["forbidden"]]
                 for root in ("z", "w")}
        total = 2 + sum(map(sum, spans.values()))
        shape = str((len(small["spokes_colors"]), tuple(small["ports"]),
                     len(large["spokes_colors"]), tuple(large["ports"])))
        item = dict(source_id=r["id"], small_root=sr, min_unary_spans=spans,
                    min_total_span=total, source_record=r)
        if total > 5:
            item["reason"] = "perimeter_excess"
        else:
            assert total == 5 and small["ports"] == large["ports"] == [2]
            assert large["forbidden"] == [[3]]
            d = small["residual"][0]
            h = small["spokes_colors"][0]
            assert set(small["forbidden"][0]) == U - {d, h}
            assert all({d, h} <= {Q[i] for i in s}
                       for s in SUPPORTS if stable(s, tuple(small["forbidden"][0])))
            item.update(reason="saturated_order_conflict",
                        geometry_checks=[saturation_check(r, g) for g in geometries])
        entry = shapes.setdefault(shape, dict(records=0, min_total_span=total,
                                               span_counts={}, reason=item["reason"]))
        entry["min_total_span"] = min(entry["min_total_span"], total)
        entry["span_counts"][str(total)] = entry["span_counts"].get(str(total), 0) + 1
        entry["records"] += 1
        records.append(item)
    counts = Counter(r["reason"] for r in records)
    assert len(records) == 576 and counts == {
        "perimeter_excess": 552, "saturated_order_conflict": 24}
    narrow = [r for r in records if r["source_record"][r["small_root"]]["ports"] == [1]]
    assert len(narrow) == 36 and all(r["min_total_span"] >= 6 for r in narrow)
    # Reflection keeps original z,w identities and transports every color/set.
    lookup = {}
    for r in records:
        s = r["source_record"]
        key = (s["missing_u"], s["missing_v"], s["small_root"],
               tuple((tuple(s[root]["spokes_colors"]), tuple(s[root]["ports"]),
                      tuple(tuple(f) for f in s[root]["forbidden"])) for root in ("z", "w")))
        lookup[key] = r
    for key, r in lookup.items():
        d, e, sr, sides = key
        moved = (PI[d], PI[e], sr, tuple((tuple(sorted(PI[c] for c in spoke)), ports,
                                        tuple(tuple(sorted(PI[c] for c in f)) for f in fs))
                                       for spoke, ports, fs in sides))
        other = lookup[moved]
        assert (other["min_total_span"], other["reason"]) == (r["min_total_span"], r["reason"])
        r["reflected_source_id"] = other["source_id"]
    support_keys = {tuple(g["supports"][k] for k in NAMES): g for g in geometries}
    for g in geometries:
        key = tuple(tuple(sorted(RHO[i] for i in g["supports"][k])) for k in NAMES)
        g["reflected_geometry_id"] = support_keys[key]["id"]
    inputs = [SOURCE, ROOT / "scripts/c5_adjacent_degree5_mixed_edge.py"]
    return dict(schema=1,
                scope="paper arbitrary-size source exclusion; finite necessary supports, no source realization or Lean theorem",
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in inputs},
                summary=dict(planar_necessary_records=576, perimeter_exclusions=552,
                             saturated_order_exclusions=24, remaining_records=0,
                             narrow_t2_records=36, saturated_geometries=10,
                             q_compatible_large_support_geometries=6,
                             same_source_geometry_checks=240,
                             reflected_abstract_records=576, reflected_geometries=10,
                             **controls),
                shape_counts=shapes, support_catalogue=catalogue,
                saturated_geometries=geometries, six_cases=six_cases(geometries), records=records)


def table(data):
    lines = ["# 唯一 mixed K2：原四環外側次序的來源排除", "",
             "此表重播必要資料的排除；任意大小來源覆蓋見證明報告，不是來源圖枚舉。", "",
             "| (一色側 t, 分拆, 兩色側 t, 分拆) | 原資料數 | 最小總跨度 | 排除 |",
             "| --- | ---: | ---: | --- |"]
    for shape, v in sorted(data["shape_counts"].items()):
        lines.append(f"| `{shape}` | {v['records']} | {v['min_total_span']} | {v['reason']} |")
    lines += ["", "## 飽和後的六種 q 相容大側支援", "",
              "ps、pl 分別為一色側、兩色側的原 mixed 端點；原 z/w/u/v 身份見 JSON。", "",
              "| 幾何 ID | Cs | ps | pl | Cl | 缺色 d,e | 矛盾 |",
              "| ---: | --- | --- | --- | --- | --- | --- |"]
    for case in data["six_cases"]:
        g = data["saturated_geometries"][case["geometry_id"]]
        supports = ["".join(map(str, g["supports"][k])) for k in NAMES]
        lines.append(f"| {g['id']} | " + " | ".join(supports) +
                     f" | {case['missing_small']},{case['missing_large']} | {case['reason']} |")
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
