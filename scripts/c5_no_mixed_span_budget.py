#!/usr/bin/env python3
"""Audit the no-mixed bundle and the source side-span necessary inequality.

Reads existing certificates without regenerating them. The arbitrary-size
topology and palette lemmas remain paper arguments, not Python conclusions.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

from c5_adjacent_degree5_no_mixed_t2_t1_bridge import frame_evidence, minor_control
from c5_single_spoke_frame_arc import admissible_supports

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "artifacts/c5_adjacent_degree5_no_mixed"
OUT = ROOT / "artifacts/c5_no_mixed_span_budget"
Q = (0, 1, 0, 1, 2)
WEIGHTS = dict(A=2, B=2, C=3, D=4, E=3)
FAMILIES = {
    "AA": "t2_path_palettes", "AB": "t2_t1_endpoints",
    "AC": "t2_t0_pairs", "AD": "t2_t0_overlap", "AE": "t2_t0_singles",
    "BB": "bb", "BC": "bc", "BD": "bd", "BE": "be",
    "CC": "cc", "CD": "cd", "CE": "ce", "DD": "dd", "DE": "de", "EE": "ee",
}


def kind(side):
    shape = (len(side["root_boundary"]), tuple(side["ports"]))
    if shape == (2, (2,)):
        return "A"
    if shape == (1, (2, 1)):
        return "B"
    if shape == (0, (2, 2)):
        return "C" if side["overlap_excess"] == 0 else "D"
    assert shape == (0, (2, 1, 1)), shape
    return "E"


def original_record(record):
    while "original_record" in record or "inherited_record" in record:
        record = record.get("original_record", record.get("inherited_record"))
    return record


def context(record, source):
    supports = record["supports"]
    components, offset = [], 0
    for root in ("z", "w"):
        side = source[root]
        for i, (ports, banned) in enumerate(zip(side["ports"], side["forbidden"], strict=True)):
            name = "CDE"[i] + root
            components.append(dict(name=name, root=root, support=supports[offset],
                                   source_forbidden=banned,
                                   contacts=[f"{name}_{j}" for j in range(ports)]))
            offset += 1
        spokes = supports[offset:offset + len(side["root_boundary"])]
        assert all(len(s) == 1 for s in spokes)
        assert sorted(s[0] for s in spokes) == side["root_boundary"]
        offset += len(spokes)
    assert offset == len(supports)
    return dict(record_id=record["id"], components=components,
                root_boundary={r: source[r]["root_boundary"] for r in ("z", "w")})


def side_arcs(ctx, root):
    """Independent circular interval masks; no old geometry generator imported."""
    comps = [c for c in ctx["components"] if c["root"] == root]
    spokes = ctx["root_boundary"][root]
    arcs = set()
    for anchor in range(5):
        intervals = [sorted((h-anchor) % 5 for h in c["support"]) for c in comps]
        points = [(h-anchor) % 5 for h in spokes]
        if any(not (a[-1] <= b[0] or b[-1] <= a[0])
               for a, b in combinations(intervals, 2)):
            continue
        if any(a[0] < h < a[-1] for a in intervals for h in points):
            continue
        ends = [v for a in intervals for v in a] + points
        lo, hi = min(ends), max(ends)
        mask = sum(1 << ((anchor+h) % 5) for h in range(lo, hi))
        saturated_ok = all(a[-1]-a[0] >= 2 for a, c in zip(intervals, comps, strict=True)
                           if len(c["source_forbidden"]) == 2)
        arcs.add((mask, hi-lo, saturated_ok))
    return sorted(arcs)


def elementary_controls():
    # A singleton invariant under the pointwise stabilizer of two observed
    # colors is one of those colors; no invariant singleton avoids both.
    singleton_cases = 0
    pair_cases = 0
    for a, b in permutations(range(4), 2):
        stabilizer = [p for p in permutations(range(4)) if p[a] == a and p[b] == b]
        fixed = [d for d in range(4) if all(p[d] == d for p in stabilizer)]
        assert set(fixed) == {a, b}
        singleton_cases += 1
    for a in range(4):
        stabilizer = [p for p in permutations(range(4)) if p[a] == a]
        for pair in combinations(range(4), 2):
            assert not all({p[d] for d in pair} == set(pair) for p in stabilizer)
            pair_cases += 1
    # The extra A-side unit is necessary: m+s alone misses A-D.
    assert 1 + (2+2) == 5 and WEIGHTS["A"] + WEIGHTS["D"] > 5
    return dict(two_observed_color_singleton_cases=singleton_cases,
                one_observed_color_pair_cases=pair_cases,
                uncorrected_component_budget_misses="AD")


def build():
    hashes = {}

    def read(path):
        raw = (ROOT/path).read_bytes()
        hashes[path] = sha256(raw).hexdigest()
        return json.loads(raw)

    data = read(PREFIX + "/observations.json")
    pairs = data["abstract_conditions"]["retained"]
    lookup = {tuple(pair): i for i, pair in enumerate(pairs)}
    assert len(lookup) == len(pairs) == 3548
    sides = data["side_normal_forms"]
    covered, tables, all_audits, minor_count = set(), [], {}, 0
    for cell, suffix in FAMILIES.items():
        path = f"{PREFIX}_{suffix}/observations.json"
        bundle = read(path)
        sources = bundle.get("original_records", bundle.get("original_frontier"))
        for source in sources:
            assert [source[r] for r in ("z", "w")] == [sides[i] for i in source["side_ids"]]
        forward = {lookup[tuple(s["side_ids"])] for s in sources}
        assert all((kind(s["z"]), kind(s["w"])) == tuple(cell) for s in sources)
        ids = forward | {lookup[tuple(pairs[i][::-1])] for i in forward}
        expected = {i for i, pair in enumerate(pairs)
                    if "".join(sorted(kind(sides[j]) for j in pair)) == cell}
        assert ids == expected and not covered & ids
        covered |= ids
        over_budget = sum(WEIGHTS[c] for c in cell) > 5
        fibers = Counter()
        excluded = accepts = edge_records = 0
        audits = []
        for final in bundle.get("records", []):
            rec = original_record(final)
            source = sources[rec["source_id"]]
            jid = lookup[tuple(source["side_ids"])]
            fibers[rec["source_id"]] += 1
            ctx = context(rec, source)
            arcs = [side_arcs(ctx, root) for root in ("z", "w")]
            placements = [(a, b) for a, b in product(*arcs) if not a[0] & b[0]]
            assert placements, (cell, rec["id"], "missing circular placement")
            for a, b in placements:
                assert a[1] + b[1] <= 5
                for arc, side in zip((a, b), cell, strict=True):
                    if side == "A":
                        assert arc[1] >= 2, (cell, rec["id"], "A-side span")
                    if arc[2]:
                        assert arc[1] >= WEIGHTS[side]
            planar_spans = sorted({(a[1], b[1]) for a, b in placements if a[2] and b[2]})
            if over_budget:
                assert not planar_spans
            edge_witnesses = []
            for i, comp in enumerate(ctx["components"]):
                support = comp["support"]
                if len(comp["source_forbidden"]) != 2 or len(support) != 2:
                    continue
                x, y = support
                if (x-y) % 5 not in (1, 4):
                    continue
                family = admissible_supports(Q, tuple(support), tuple(comp["source_forbidden"]))
                assert list(map(sorted, family)) == [support]
                ev = frame_evidence(ctx, i, family)
                witness = next(w for w in ev["witnesses"]
                               if list(map(list, w["frame_arcs"])) == [[x], [y], sorted(set(range(5))-set(support))])
                edge_witnesses.append(dict(component=i, name=comp["name"], witness=witness))
            if over_budget:
                assert edge_witnesses, (cell, rec["id"], "no edge-saturated component")
            is_excluded = rec.get("status") in ("excluded", "source_excluded")
            assert is_excluded == rec.get("source_evidence", {}).get("eliminated", False)
            excluded += is_excluded
            if edge_witnesses:
                edge_records += 1
                assert is_excluded, (cell, rec["id"], "new exclusion requires separate review")
                ev = edge_witnesses[0]
                controls = [minor_control(ctx, ev["component"], ev["witness"], length=n) for n in (1, 3, 5)]
                minor_count += len(controls)
                ev["minor_controls_sha256"] = sha256(json.dumps(controls, sort_keys=True).encode()).hexdigest()
            targets = final.get("final_targets", final.get("targets", []))
            assert len(targets) == (0 if is_excluded else 2), (cell, rec["id"], is_excluded, type(targets), len(targets))
            if targets:
                assert [t["row"] for t in targets] == [[0, 1, 0, 2, 1], [0, 1, 2, 1, 2]]
            assert all(t["status"] == "accept" for t in targets)
            accepts += len(targets)
            audits.append(dict(record_id=rec["id"], retained_join_id=jid,
                               side_span_pairs=sorted({(a[1], b[1]) for a, b in placements}),
                               span_pairs_without_short_saturated_component=planar_spans,
                               edge_saturated_components=[e["name"] for e in edge_witnesses],
                               first_edge_witness=edge_witnesses[0] if edge_witnesses else None,
                               inherited_source_excluded=is_excluded, inherited_target_accepts=len(targets)))
        nrecords = len(audits)
        empty = len(sources)-len(fibers)
        assert nrecords == bundle["summary"].get("necessary_support_records", nrecords)
        assert accepts == bundle["summary"]["target_queries"]
        if over_budget:
            assert excluded == nrecords and accepts == 0
        else:
            assert accepts == 2*(nrecords-excluded) and accepts > 0
        tables.append(dict(cell=cell, side_weights=[WEIGHTS[c] for c in cell],
                           original_forward_joins=len(sources), original_ordered_joins=len(ids),
                           original_join_ids=sorted(ids), empty_forward_fibers=empty,
                           necessary_supports=nrecords, inherited_source_exclusions=excluded,
                           edge_saturated_supports=edge_records, retained_supports=nrecords-excluded,
                           inherited_target_accepts=accepts,
                           conclusion="source_excluded" if over_budget else "two_target_separation",
                           source_artifact=path))
        all_audits[cell] = audits
    assert covered == set(range(3548))
    total = {key: sum(t[key] for t in tables) for key in (
        "original_ordered_joins", "necessary_supports", "inherited_source_exclusions",
        "edge_saturated_supports", "retained_supports", "inherited_target_accepts")}
    # Retained necessary supports must not be mistaken for realizable sources.
    total.update(source_excluded_cells=sum(t["conclusion"] == "source_excluded" for t in tables),
                 separated_cells=sum(t["conclusion"] == "two_target_separation" for t in tables),
                 over_budget_original_joins=sum(t["original_ordered_joins"] for t in tables
                                                if t["conclusion"] == "source_excluded"),
                 minor_controls=minor_count, new_source_exclusions=0, new_target_accepts=0)
    for path in ("scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py",
                 "scripts/c5_single_spoke_frame_arc.py", "scripts/c5_single_spoke_two_two_minor.py",
                 "scripts/c5_single_spoke_two_two_external.py", "scripts/c5_single_spoke_cores.py"):
        hashes[path] = sha256((ROOT/path).read_bytes()).hexdigest()
    return dict(schema=1, scope="paper source-span compression plus finite certificate audit; no realizability or Lean theorem",
                source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(), inputs_sha256=hashes,
                side_weights=WEIGHTS, summary=total, elementary_controls=elementary_controls(),
                cells=tables, record_audits=all_audits)


def render(data):
    lines = ["# No-mixed 十五類總表", "", "由 `scripts/c5_no_mixed_span_budget.py` 生成。",
             "原接合含 root 交換方向；支援與查詢只計各報告保存的正向表。",
             "支援／來源排除／target 接受為不同計數單位；必要支援不是來源圖。", "",
             "| 類型 | 側跨度下界和 | 原接合 | 空正向纖維 | 必要支援 | 原 source 排除 | 保留支援 | 原 target 接受 |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for t in data["cells"]:
        lines.append("| " + " | ".join(map(str, ["–".join(t["cell"]), sum(t["side_weights"]),
                     t["original_ordered_joins"], t["empty_forward_fibers"], t["necessary_supports"],
                     t["inherited_source_exclusions"], t["retained_supports"], t["inherited_target_accepts"]])) + " |")
    lines += ["", "總計：`" + json.dumps(data["summary"], ensure_ascii=False, sort_keys=True) + "`", "",
              "新推導為紙面必要不等式；本表不新增來源排除或 target 接受。", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    outputs = {"observations.json": json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)+"\n",
               "summary_table.md": render(data)}
    for name, content in outputs.items():
        path = OUT/name
        if args.check:
            assert path.read_text() == content, f"stale artifact: {path}"
        else:
            OUT.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print(json.dumps(data["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
