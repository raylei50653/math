#!/usr/bin/env python3
"""Read-only independent original-edge DFS and complete D interface validation."""

from collections import defaultdict
import hashlib
from itertools import product
import json
from pathlib import Path
import stat


REPO = Path(__file__).resolve().parents[2]
TARGET = REPO / "audits/2026-10-11-n45-s-long-s-block-transfer"
LITERALS = ["01012", "01021", "01023", "01201", "01202", "01203", "01212", "01213", "01231", "01232"]
Q = {0: "01212", 1: "01202", 2: "01201", 3: "01021", 4: "01012"}
CASE_IDS = ["TT5", "T5_7", "BRIDGE_BAD6", "BRIDGE_FIX6", "NONROOT_CYCLE7"]
SPOKES = [["b0"], ["b2"], ["b0", "b2"]]
BASE = "f2692089ad4259808e27d9b7e882ac09505b180a"
DELIVERY_SHA = "ee7bd0093a4e244ee0d8c1af65f0ddedd95125861b5816c8dcbb7975aa43e0ed"


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def load(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    result = {}
    for path in TARGET.rglob("*"):
        mode = path.lstat().st_mode
        rel = path.relative_to(TARGET).as_posix()
        if stat.S_ISREG(mode):
            result[rel] = {"type": "regular", "bytes": path.stat().st_size, "sha256": sha(path)}
        elif stat.S_ISDIR(mode):
            result[rel] = {"type": "directory"}
        else:
            raise AssertionError("special or symlink target entry: " + rel)
    return result


def structure(case):
    vertices = case["vertices"]
    names = set(vertices)
    need(len(vertices) == len(names) and "r" in names, "invalid original vertex order")
    neighbours = {v: set() for v in vertices}
    edges = set()
    for edge in case["original_edges"]:
        need(len(edge) == 2 and len(set(edge)) == 2 and set(edge) <= names, "invalid original edge")
        key = frozenset(edge)
        need(key not in edges, "duplicate original edge")
        edges.add(key)
        u, v = edge
        neighbours[u].add(v)
        neighbours[v].add(u)
    need(set(case["boundary_attachments"]) == names, "attachment domains mismatch")
    contacts = case["s_contacts"]
    need(len(contacts) == len(set(contacts)) == 2 and set(contacts) <= names and "r" not in contacts,
         "ordered original s contacts mismatch")
    need(case["original_e"] == ["r", "b4"] and case["retained_r_spokes"] == []
         and case["t_r"] == 1 and case["boundary_attachments"]["r"] == [], "original r/e identity mismatch")
    need(len(neighbours["r"]) == 4 and case["s_spoke_variants"] == SPOKES, "root degree/spoke declaration mismatch")
    need(case["actual_U_supplied"] is False and case["actual_G_supplied"] is False
         and case["K11_witnesses"] is None and case["K12_witnesses"] is None
         and case["disk_topology_verified"] is False, "microcase falsely upgraded to source")
    L, S = set(case["pieces"]["L"]), set(case["pieces"]["S"])
    need(not (L & S) and L | S == names - {"r"}, "actual L/S partition mismatch")
    for i, (label, piece, supports) in enumerate((("L", L, {"b2", "b3", "b4"}), ("S", S, {"b4", "b0"}))):
        need(contacts[i] in piece, "ordered contact ownership mismatch")
        expected_r = [v for v in case["pieces"][label] if v in neighbours["r"]]
        need(case["r_contacts"][label] == expected_r and len(expected_r) == 2, "ordered r contact mismatch")
        need({b for v in piece for b in case["boundary_attachments"][v]} == supports
             and set(case["support_order"][label]) == supports, "actual support mismatch")
        reached = {next(iter(piece))}
        pending = list(reached)
        while pending:
            v = pending.pop()
            for w in neighbours[v] & piece - reached:
                reached.add(w)
                pending.append(w)
        need(reached == piece, "C-r piece not connected")
        need(all(neighbours[v] <= piece | {"r"} for v in piece), "cross-piece original edge")
    # An exact edge partition into these bridges/cycles with a tree incidence
    # proves they are the actual blocks, independently of the worker's Tarjan code.
    incidence = {("v", v): [] for v in vertices}
    partition = []
    root_blocks = []
    for j, block in enumerate(case["blocks"]):
        bv = block["vertices"]
        need(len(bv) == len(set(bv)) and set(bv) <= names, "invalid block vertices")
        if block["type"] == "bridge":
            need(len(bv) == 2, "invalid bridge")
            be = [frozenset(bv)]
        else:
            need(block["type"] == "odd_cycle" and len(bv) >= 3 and len(bv) % 2 == 1, "invalid odd cycle")
            be = [frozenset((bv[k], bv[(k + 1) % len(bv)])) for k in range(len(bv))]
        partition.extend(be)
        node = ("b", j)
        incidence[node] = [("v", v) for v in bv]
        for v in bv:
            incidence[("v", v)].append(node)
        if "r" in bv:
            root_blocks.append(block)
    need(len(partition) == len(edges) and len(set(partition)) == len(partition)
         and set(partition) == edges, "original edge block partition mismatch")
    need(len(root_blocks) == 2 and all(b["type"] == "odd_cycle" for b in root_blocks), "original root blocks mismatch")
    seen = {("v", "r")}
    pending = [(('v', 'r'), None)]
    while pending:
        node, parent = pending.pop()
        for child in incidence[node]:
            if child == parent:
                continue
            need(child not in seen, "incidence not a tree")
            seen.add(child)
            pending.append((child, node))
    need(seen == set(incidence), "incidence disconnected")
    degree_rows, findings = [], []
    for v in vertices:
        attachments = case["boundary_attachments"][v]
        need(len(attachments) == len(set(attachments)) and set(attachments) <= {f"b{i}" for i in range(5)},
             "invalid boundary attachment")
        role = "root" if v == "r" else "L" if v in L else "S"
        need(case["ownership"][v] == role, "duplicate or changed ownership")
        original_neighbours = list(neighbours[v]) + attachments + (["s"] if v in contacts else []) + (["b4"] if v == "r" else [])
        need(sorted(case["rotation"][v]) == sorted(original_neighbours), "rotation loses original neighbour")
        full_degree = len(neighbours[v]) + len(attachments) + int(v in contacts)
        degree_rows.append({"vertex": v, "deg_C": len(neighbours[v]), "N_B": attachments,
                            "s_contact": v in contacts, "full_degree": full_degree})
        if full_degree != 4:
            findings.append({"vertex": v, "deg_C": len(neighbours[v]),
                             "boundary_attachment_count": len(attachments), "s_contact_incidence": int(v in contacts),
                             "full_degree": full_degree, "expected": 4})
    need(case["expected_valid"] is (not bool(findings)), "declared degree validity mismatch")
    return neighbours, findings, degree_rows


def edge_dfs(case, literal, neighbours):
    """Dynamic most-constrained original-vertex DFS; no block use or imports."""
    vertices = case["vertices"]
    masks = {}
    for v in vertices:
        forbidden = {int(literal[int(b[1:])]) for b in case["boundary_attachments"][v]}
        masks[v] = sum(1 << colour for colour in range(4) if colour not in forbidden)
    assignment = {}
    vectors = []

    def visit():
        if len(assignment) == len(vertices):
            vectors.append([assignment[v] for v in vertices])
            return
        candidates = []
        for i, v in enumerate(vertices):
            if v in assignment:
                continue
            mask = masks[v]
            for w in neighbours[v]:
                if w in assignment:
                    mask &= ~(1 << assignment[w])
            if not mask:
                return
            candidates.append((mask.bit_count(), -len(neighbours[v]), -i, v, mask))
        _, _, _, v, mask = min(candidates)
        for colour in range(3, -1, -1):
            if mask & (1 << colour):
                assignment[v] = colour
                visit()
                del assignment[v]

    visit()
    vectors.sort()
    need(len({tuple(v) for v in vectors}) == len(vectors), "DFS duplicated original assignment")
    return vectors


def interface(case, literal, neighbours):
    vectors = edge_dfs(case, literal, neighbours)
    index = {v: i for i, v in enumerate(case["vertices"])}
    ri = index["r"]
    ci = [index[v] for v in case["s_contacts"]]
    cells = defaultdict(list)
    pinned = defaultdict(list)
    for vector in vectors:
        tau = tuple(vector[i] for i in ci)
        cells[(*tau, vector[ri])].append(vector)
        for b in range(4):
            if b not in tau:
                pinned[(vector[ri], b)].append(vector)
    ambient = [{"tuple": [t0, t1], "r": a, "preimages": cells[(t0, t1, a)]}
               for t0, t1, a in product(range(4), repeat=3)]

    def pins(spokes):
        out = []
        blocked_s = {int(literal[int(b[1:])]) for b in spokes}
        for a, b in product(range(4), repeat=2):
            preimages = [] if b in blocked_s else pinned[(a, b)]
            out.append({"r": a, "s": b, "preimages": preimages,
                        "restored_preimages": preimages if a != int(literal[4]) else []})
        return out

    return {"literal": literal, "assignments": vectors, "ambient_fibres": ambient,
            "pins": pins([]), "spoke_variants": [{"s_spokes": variant, "pins": pins(variant)} for variant in SPOKES]}


def check_coverage():
    coverage = load(TARGET / "coverage.json")
    ledger = load(TARGET / "authority/sealed/audits/2026-10-11-n45-s-long-s-review/remaining-schedules.json")
    need(coverage["inherited_schedule_counts"] == ledger["counts"] == {"raw": 28, "remaining": 24, "restoration_excluded": 4},
         "inherited ledger counts changed")
    schedules = coverage["assigned_schedules"]
    need(len(schedules) == coverage["assigned_schedule_count"] == 24, "schedule count changed")
    consumed = set()
    variants = obligations = 0
    for schedule in schedules:
        key = (schedule["t_s"], schedule["SigmaG_orbit"], tuple(schedule["QG"]), schedule["beta_q"])
        need(key not in consumed, "duplicate inherited schedule")
        consumed.add(key)
        matching = [entry for entry in ledger["remaining_schedules"]
                    if (entry["t_s"], entry["SigmaG_orbit"], tuple(entry["QG"]), entry["beta_q"]) == key]
        need(len(matching) == 1, "unrecognized inherited schedule")
        need(all(schedule[name] == value for name, value in matching[0].items()), "inherited schedule data changed")
        need(schedule["concrete_source_relations"] is None and schedule["concrete_source_preimage_counts"] is None
             and schedule["new_proved_restoration_rows"] == [] and schedule["new_source_minors"] == [], "D claims new source data")
        expected_spokes = [[0], [2]] if schedule["t_s"] == 1 else [[0, 2]]
        need([v["original_s_spokes"] for v in schedule["variants"]] == expected_spokes, "s-spoke variant domain changed")
        for variant in schedule["variants"]:
            variants += 1
            rows = variant["ten_rows"]
            need([r["literal"] for r in rows] == LITERALS, "symbolic literal domain changed")
            for row in rows:
                literal = row["literal"]
                q = next((i for i, value in Q.items() if value == literal), None)
                need(row["q"] == q and row["gamma_b4"] == int(literal[4])
                     and row["is_Delta"] == (q in schedule["Delta"])
                     and row["is_beta"] == (q == schedule["beta_q"]), "symbolic literal/r identity changed")
                pins = row["pins"]
                need([(p["r"], p["s"]) for p in pins] == list(product(range(4), repeat=2)), "symbolic pin inventory changed")
                for pin in pins:
                    factor = all(pin["s"] != int(literal[i]) for i in variant["original_s_spokes"])
                    need(pin["s_spoke_factor"] == factor and pin["rb4_restorable"] == (pin["r"] != int(literal[4]))
                         and pin["concrete_full_X_preimages"] is None, "symbolic pin factor or source data changed")
                    obligations += 1
                opened = row["OPEN_fibres"]
                if q in schedule["Delta"]:
                    need(opened["r_colours"] == [a for a in range(4) if a != int(literal[4])]
                         and opened["actual_values_supplied"] is False, "OPEN fibre domain changed")
                else:
                    need(opened is None, "non-Delta row presented as OPEN restoration")
    need(variants == coverage["assigned_schedule_spoke_variants"] == 38 and obligations == 6080,
         "symbolic variant/obligation total changed")
    excluded = coverage["inherited_restoration_excluded_schedules"]
    need(len(excluded) == 4, "historical exclusions count changed")
    for record, inherited in zip(excluded, ledger["excluded_schedules"], strict=True):
        need(all(record[name] == value for name, value in inherited.items()), "historical exclusions modified")
        need(record["authority"] == "sealed adopted review, not this task", "historical exclusion promoted to new D proof")
    need(coverage["minimal_named_residual"] == "same-source-Delta-restorable-r-fibre-nonemptiness",
         "D changed open lemma")
    return {"necessary_schedules": 24, "spoke_variants": 38, "symbolic_pin_obligations": 6080,
            "new_source_exclusions": 0, "residual": coverage["minimal_named_residual"]}


def main():
    before = snapshot()
    need(sha(TARGET / "delivery.json") == DELIVERY_SHA, "bound D delivery changed")
    raw = (TARGET / "cases.json").read_bytes()
    plan = json.loads(raw)
    need(plan["literals"] == LITERALS and [c["id"] for c in plan["cases"]] == CASE_IDS, "fixed finite plan changed")
    need(plan["declared_case_count"] == 5 and plan["declared_largest_C"] == 7
         and plan["maximum_named_cases"] == 8 and plan["maximum_C_vertices_per_case"] == 11,
         "named finite bounds changed")
    records, failures, degree_records, counts = [], [], [], {}
    for case in plan["cases"]:
        neighbours, findings, degrees = structure(case)
        degree_records.append({"case_id": case["id"], "expected_valid": case["expected_valid"],
                               "vertices": degrees, "findings": findings, "disk_topology_verified": False})
        if findings:
            failures.append({"case_id": case["id"], "findings": findings})
            continue
        rows = [interface(case, literal, neighbours) for literal in LITERALS]
        counts[case["id"]] = [len(row["assignments"]) for row in rows]
        records.append({"case_id": case["id"], "vertices": case["vertices"], "rows": rows})
    expected = {"schema": 1, "cases_sha256": hashlib.sha256(raw).hexdigest(), "cases": records,
                "failed_cases": failures, "target_source": {"executed": False, "trigger_count": None, "status": "not triggered"}}
    require_failure = [{"case_id": "BRIDGE_BAD6", "findings": [{"vertex": "l0", "deg_C": 3,
                        "boundary_attachment_count": 2, "s_contact_incidence": 0, "full_degree": 5, "expected": 4}]}]
    need(failures == require_failure, "failed declared case not precisely retained")
    need(load(TARGET / "degree-audit.json") == {"status": "待獨立驗收", "cases": degree_records}, "degree audit disagrees")
    certificate = load(TARGET / "certificate.json")
    need(certificate == expected, "all original-edge assignments/interfaces do not match certificate")
    canonical = (json.dumps(expected, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    need((TARGET / "certificate.json").read_bytes() == canonical, "certificate canonical byte mismatch")
    # JSON clone deliberately removes any Python aliasing of full vectors.
    negative_r = json.loads(json.dumps(expected))
    cell = next(c for c in negative_r["cases"][0]["rows"][0]["ambient_fibres"]
                if c["tuple"] == [0, 1] and c["r"] == 2)
    need(cell["preimages"] and cell["preimages"][0][0] == 2, "negative r cell not triggered")
    cell["preimages"][0][0] = 3
    need(load(TARGET / "negative-r-colour.json") == negative_r and negative_r != expected, "r negative not exact")
    negative_empty = json.loads(json.dumps(expected))
    cells = negative_empty["cases"][0]["rows"][0]["ambient_fibres"]
    cell = next(c for c in cells if c["tuple"] == [0, 0] and c["r"] == 0)
    need(cell["preimages"] == [], "negative empty cell was not empty")
    cells.remove(cell)
    need(load(TARGET / "negative-empty-cell.json") == negative_empty and negative_empty != expected, "empty negative not exact")
    negative_branch = json.loads(json.dumps(expected))
    record = next(c for c in negative_branch["cases"] if c["case_id"] == "BRIDGE_FIX6")
    coordinate = record["vertices"].index("l2")
    record["vertices"].pop(coordinate)
    for row in record["rows"]:
        lists = [row["assignments"]] + [c["preimages"] for c in row["ambient_fibres"]]
        all_pins = row["pins"] + [p for variant in row["spoke_variants"] for p in variant["pins"]]
        lists += [p[name] for p in all_pins for name in ("preimages", "restored_preimages")]
        for vectors in lists:
            for vector in vectors:
                vector.pop(coordinate)
    need(load(TARGET / "negative-missing-branch.json") == negative_branch and negative_branch != expected,
         "branch negative not exact")
    coverage = check_coverage()
    all_rows = [row for case in records for row in case["rows"]]
    totals = {"valid_cases": len(records), "rows": len(all_rows),
              "assignments": sum(len(row["assignments"]) for row in all_rows),
              "ambient_cells": sum(len(row["ambient_fibres"]) for row in all_rows),
              "empty_ambient_cells": sum(not cell["preimages"] for row in all_rows for cell in row["ambient_fibres"]),
              "ordered_pins": sum(len(row["pins"]) for row in all_rows),
              "spoke_filtered_pin_cells": sum(len(v["pins"]) for row in all_rows for v in row["spoke_variants"])}
    need(totals == {"valid_cases": 4, "rows": 40, "assignments": 1344, "ambient_cells": 2560,
                    "empty_ambient_cells": 1966, "ordered_pins": 640, "spoke_filtered_pin_cells": 1920}, "finite summary changed")
    need(snapshot() == before, "target changed during independent read-only review")
    print(json.dumps({"status": "independent D original-edge/interface check passed", "base": BASE,
                      "target_delivery_sha256": DELIVERY_SHA, "certificate_sha256": sha(TARGET / "certificate.json"),
                      "algorithm": "dynamic minimum-remaining-colour DFS on original edges; no worker imports or block recurrence use",
                      "totals": totals, "per_case_literal_assignment_counts": counts, "failed_cases": failures,
                      "negative_controls": [{"file": "negative-r-colour.json", "status": "exact corruption confirmed; differs from independent reconstruction"},
                                            {"file": "negative-empty-cell.json", "status": "exact missing empty ambient cell confirmed"},
                                            {"file": "negative-missing-branch.json", "status": "exact omitted original l2 coordinate confirmed"}],
                      "coverage": coverage, "target_source": expected["target_source"],
                      "whole_X_G_or_nonempty_isolated_factor_executed": False,
                      "new_Lean_or_general_closure_claimed": False, "writes": []}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
