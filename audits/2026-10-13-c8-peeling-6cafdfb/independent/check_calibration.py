#!/usr/bin/env python3
"""Replay literal primary graph data with an independent fixed-order search."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json

from check import C, T, adjacency, compare_expected, edge, embedding, expect_rejection, fixture, verify_caps

ROOT = Path(__file__).resolve().parent
INPUT = ROOT.parent / "calibration" / "certificate.json.gz"


def direct(vertices, edges, pins):
    # Choose the order once without inspecting actual color values or branches.
    adj = adjacency(vertices, edges)
    if any(pins[a] == pins[b] for a in pins for b in adj[a] & pins.keys()):
        return []
    placed = set(pins)
    remaining = set(vertices) - placed
    index = {v: i for i, v in enumerate(vertices)}
    order = []
    while remaining:
        v = min(remaining, key=lambda w: (-len(adj[w] & placed), -len(adj[w]), index[w]))
        order.append(v)
        remaining.remove(v)
        placed.add(v)
    assign = dict(pins)
    result = []
    def visit(k):
        if k == len(order):
            result.append("".join(str(assign[v]) for v in vertices))
            return
        v = order[k]
        forbidden = {assign[w] for w in adj[v] if w in assign}
        for c in range(4):
            if c not in forbidden:
                assign[v] = c
                visit(k + 1)
        assign.pop(v, None)
    visit(0)
    return sorted(result)


def known_class(edges):
    wanted = {edge(a, b) for a, b in edges}
    matches = []
    for name in ("M10-FAN3", "M10-FAN4", "M10-CHORD4"):
        _, base, _ = fixture(name)
        for offset in range(8):
            for swap in (False, True):
                mapping = {f"{letter}{i}": f"{letter}{(i + offset) % 8}"
                           for letter in ("c", "t") for i in range(8)}
                mapping.update({"r": "s" if swap else "r", "s": "r" if swap else "s"})
                candidate = {edge(mapping[a], mapping[b]) for a, b in base}
                if candidate == wanted:
                    matches.append((name, offset, swap))
    assert matches
    return matches[0][0]


def run(write=False, negative=False):
    data = json.load(gzip.open(INPUT, "rt"))
    records = []
    class_counts = Counter()
    total_h = total_g = empty_h = core_fibres = core_lifts = 0
    for case in data["H_cases"]:
        graph = case["H"]
        vertices = tuple(graph["vertices"])
        edges = graph["edges"]
        adj = adjacency(vertices, edges)
        _, oriented = embedding(vertices, edges, graph["oriented_inner_faces"])
        caps = verify_caps(vertices, adj, oriented)
        assert {k.replace("-", "_"): v for k, v in caps.items()} == case["cap_counts"]
        klass = known_class(edges)
        class_counts[klass] += 1
        assert all(len(adj[v]) >= (4 if v in C else 5) for v in vertices)
        replay = {}
        for row in case["C_normalized_row_order"]:
            lifts = direct(vertices, edges, dict(zip(C, map(int, row))))
            compare_expected(lifts, case["H_complete_fibres"][row])
            replay[row] = lifts
            total_h += len(lifts)
            empty_h += not lifts
        core = case["Q"]
        for row in case["core_literal_row_order"]:
            lifts = direct(tuple(core["vertices"]), core["edges"], dict(zip(T, map(int, row))))
            compare_expected(lifts, case["core_complete_fibres"][row])
            core_fibres += 1
            core_lifts += len(lifts)
        records.append({"id": case["id"], "class": klass,
                        "original_cap_counts": caps,
                        "complete_H_fibres_sha256": sha256(json.dumps(replay, sort_keys=True, separators=(",", ":")).encode()).hexdigest()})
    assert class_counts == {"M10-FAN3": 8, "M10-FAN4": 4, "M10-CHORD4": 4}
    g_records = []
    for control in data["B_source_controls"]:
        graph = control["graph"]
        replay = {}
        for row in control["B_row_order"]:
            pins = dict(zip(graph["vertices"][:5], map(int, row)))
            lifts = direct(tuple(graph["vertices"]), graph["edges"], pins)
            compare_expected(lifts, control["complete_fibres"][row])
            assert lifts
            replay[row] = lifts
            total_g += len(lifts)
        assert control["sigma"] == 1023
        g_records.append({"id": control["id"], "sigma": 1023,
                          "complete_G_fibres_sha256": sha256(json.dumps(replay, sort_keys=True, separators=(",", ":")).encode()).hexdigest()})
    receipt = {"input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
               "H_graphs": len(records), "H_fibres": sum(len(c["C_normalized_row_order"]) for c in data["H_cases"]),
               "H_lifts": total_h, "H_empty_fibres": empty_h,
               "core_literal_fibres": core_fibres, "core_literal_lifts": core_lifts,
               "G_graphs": len(g_records), "G_fibres": sum(len(c["B_row_order"]) for c in data["B_source_controls"]),
               "G_lifts": total_g, "all_G_sigma": 1023,
               "named_class_counts": dict(sorted(class_counts.items())),
               "method": "literal edge lists; independent fixed search order; exact sorted full-lift equality, including empty fibres; no primary generator import",
               "H_receipts": records, "G_receipts": g_records, "status": "PASS"}
    if write:
        ROOT.joinpath("calibration_replay.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    else:
        compare_expected(receipt, json.loads(ROOT.joinpath("calibration_replay.json").read_text()))
    if negative:
        control = data["B_source_controls"][0]
        row = control["B_row_order"][0]
        graph = control["graph"]
        pins = dict(zip(graph["vertices"][:5], map(int, row)))
        reproduced = direct(tuple(graph["vertices"]), graph["edges"], pins)
        damaged = list(control["complete_fibres"][row])
        damaged.pop()
        expect_rejection(damaged, reproduced)
        fan = next(case for case in data["H_cases"] if case["type"] == "EDGE-35")
        altered = [e for e in fan["H"]["edges"] if edge(*e) != edge("r", "s")]
        try:
            known_class(altered)
        except AssertionError:
            pass
        else:
            raise AssertionError("changed original center edge must be rejected")
    summary = {k: v for k, v in receipt.items() if k not in ("H_receipts", "G_receipts")}
    summary["negative_corruptions_rejected"] = 2 if negative else 0
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    run(write=args.write, negative=args.negative)
