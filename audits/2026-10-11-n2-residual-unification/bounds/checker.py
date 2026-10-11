#!/usr/bin/env python3
"""Read-only arithmetic and frozen-cactus audit; no source-graph enumeration."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
UPSTREAM = "artifacts/c5_excess_two_arc_size_bound/observations.json"
BASE = "5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc"


def encoded(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def read_json(path, inputs):
    raw = (ROOT / path).read_bytes()
    inputs.append({"path": path, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})
    return json.loads(raw)


def graph_data(vertices, edges):
    vertices = set(vertices)
    adj = {v: set() for v in vertices}
    for a, b in edges:
        assert a != b and a in vertices and b in vertices
        adj[a].add(b)
        adj[b].add(a)
    seen, low, parent, stack, blocks = {}, {}, {}, [], []

    def visit(v):
        seen[v] = low[v] = len(seen)
        for w in sorted(adj[v]):
            if w not in seen:
                parent[w] = v
                stack.append((v, w))
                visit(w)
                low[v] = min(low[v], low[w])
                if low[w] >= seen[v]:
                    block = set()
                    while True:
                        edge = stack.pop()
                        block.update(edge)
                        if edge == (v, w):
                            break
                    blocks.append(sorted(block))
            elif w != parent.get(v) and seen[w] < seen[v]:
                stack.append((v, w))
                low[v] = min(low[v], seen[w])

    visit(min(vertices))
    assert set(seen) == vertices, "disconnected control"
    blocks.sort()
    cycles = []
    valid = max(map(len, adj.values())) <= 4
    for block in blocks:
        if len(block) == 2:
            continue
        cycle = len(block) % 2 == 1 and all(len(adj[v] & set(block)) == 2 for v in block)
        valid &= cycle
        if cycle:
            cycles.append(block)
    ns = Counter(map(len, adj.values()))
    return adj, blocks, cycles, ns, valid


def cactus_identity(vertices, edges):
    adj, blocks, cycles, ns, valid = graph_data(vertices, edges)
    out = {"vertices": sorted(vertices), "edges": sorted(edges), "blocks": blocks,
           "degree_counts": dict(sorted(ns.items())), "odd_cycle_blocks": cycles,
           "odd_cactus_max_degree_four": valid}
    if len(vertices) == 1:
        out["count_status"] = "not triggered: singleton handled separately"
        return out
    if not valid:
        out["count_status"] = "not triggered"
        return out
    n, n1, n4 = len(vertices), ns[1], ns[4]
    ell = ns[1] + ns[2]
    c = len(cycles)
    assert c == len(edges) - n + 1
    assert n == ell + n1 + 2 * c - 2 - n4
    b = ell - 2 - c
    assert b >= 0
    combinatorial_deficit = 2 * b + n4
    assert n == 3 * ell + n1 - 6 - combinatorial_deficit
    out.update({"count_status": "triggered and holds", "n": n, "ell": ell,
                "n1": n1, "n4": n4, "c": c, "b": b,
                "combinatorial_deficit": combinatorial_deficit})
    return out


def exact_component(vertices, edges, k, d, trigger):
    out = cactus_identity(vertices, edges)
    out.update({"root_incidences": k, "H_degree_two_count": d,
                "incidence_status": "triggered and holds" if trigger else "not triggered"})
    if not trigger:
        return out
    if len(vertices) == 1:
        assert (k, d) == (2, 1)
        delta = 2
        out["singleton_status"] = "triggered and holds"
    else:
        assert out["count_status"] == "triggered and holds"
        a = k + d - out["ell"] - out["n1"]
        assert a >= 0
        delta = 3 * a + 2 * out["n1"] + 2 * out["b"] + out["n4"]
        out["a"] = a
    assert len(vertices) == 3 * (k + d) - 6 - delta
    out.update({"exact_deficit": delta, "exact_identity_status": "triggered and holds"})
    return out


def parameter_rows():
    rows = []
    # These are necessary incidence/spoke profiles, not realizable source graphs.
    for u in range(3):
        possible = {(tr + ts, tr, ts) for tr, ts in product(range(3), repeat=2)
                    if (u == 0 or tr <= 1) and (u <= 1 or ts <= 1)}
        for t in sorted({entry[0] for entry in possible}):
            ub = 35 - 6 * u - 3 * t
            deficit_at_equality = ub - 10
            row = {"u": u, "t": t, "root_spoke_splits": sorted([tr, ts] for tt, tr, ts in possible if tt == t),
                   "lower_finite": 10, "upper_original": ub, "unexcluded_H_interval": [10, ub],
                   "deficit_equality_H10": deficit_at_equality,
                   "deficit_first_conflict_H_le9": deficit_at_equality + 1,
                   "unconditional_interval_status": "no contradiction",
                   "profile_status": "necessary incidence screen; not source realization"}
            assert ub >= 10
            # All integer deficit values up to the full base bound are checked.
            for delta in range(ub + 1):
                assert (ub - delta <= 9) == (delta >= deficit_at_equality + 1)
                assert (ub - delta == 10) == (delta == deficit_at_equality)
            rows.append(row)
    assert len(rows) == 12
    return rows


def produce():
    inputs = []
    upstream = read_json(UPSTREAM, inputs)
    cacti = []
    for i, saved in enumerate(upstream["named_cactus_controls"]):
        item = cactus_identity(saved["vertices"], saved["edges"])
        assert item["blocks"] == saved["blocks"]
        assert item["odd_cycle_blocks"] == saved["odd_cycle_blocks"]
        item.update({"name": saved["name"], "source_pointer": f"/named_cactus_controls/{i}",
                     "root_incidence_status": "not triggered: no original source attachments supplied"})
        cacti.append(item)
    assert len(cacti) == 58
    components, counts = [], Counter()
    bedges = {tuple(sorted((v, (v + 1) % 5))) for v in range(5)}
    for gi, g in enumerate(upstream["records"]):
        edges = g["edges"]
        interior, roots = set(g["interior_coordinates"]), set(g["roots"])
        all_vertices = interior | set(range(5))
        adj = {v: set() for v in all_vertices}
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
        assert all(len(adj[v]) == (5 if v in roots else 4) for v in interior)
        d2 = {v for v in interior if len(adj[v] & interior) == 2}
        boundary_ok = all(len(adj[v] & set(range(5))) <= 2 and
                          (len(adj[v] & set(range(5))) < 2 or
                           tuple(sorted(adj[v] & set(range(5)))) in bedges) for v in interior)
        for ci, c in enumerate(g["components"]):
            verts = c["vertices"]
            ce = sorted([a, b] for a, b in edges if a in verts and b in verts)
            _, _, _, _, cactus_ok = graph_data(verts, ce)
            k = sum(len(adj[v] & roots) for v in verts)
            d = len(set(verts) & d2)
            trigger = boundary_ok and cactus_ok
            item = exact_component(verts, ce, k, d, trigger)
            assert item["blocks"] == c["blocks"]
            assert item["incidence_status"] == c["size_inequality_status"]
            item.update({"source_pointer": f"/records/{gi}/components/{ci}",
                         "complete_fibres_status": "frozen upstream pointers only; not recomputed here",
                         "target_source_status": g["target_source_status"]})
            counts["fixed_components"] += 1
            counts["exact_component_identity_triggered"] += trigger
            counts["target_source_triggered"] += g["target_source_status"] != "not triggered"
            components.append(item)
    assert counts["fixed_components"] == 179
    assert counts["exact_component_identity_triggered"] == 24
    assert counts["target_source_triggered"] == 0
    finite = []
    for k in range(3, 10):
        erpath = f"artifacts/c5_excess_two_independent_search/NA_k{k}.json"
        er = read_json(erpath, inputs)
        espath = er["comparison"]["es_source"]
        es = read_json(espath, inputs)
        assert sha256((ROOT / espath).read_bytes()).hexdigest() == er["comparison"]["es_sha256"]
        assert er["comparison"]["consistent"]
        assert es["k"] == er["k"] == k and es["type"] == er["type"] == "NA"
        ercrit = [o for o in er["q_orbits"] if o["critical"]]
        assert len(ercrit) == len(es["crit_orbits"]) == er["comparison"]["er_crit_orbits"]
        assert all(o["Q_plus_cQ"] <= 4 for o in es["crit_orbits"])
        assert all(len(o["Q"]) <= 2 for o in er["q_orbits"])
        assert all(o["sigma_mask"] not in {933, 941} for o in er["q_orbits"])
        finite.append({"k": k, "q_orbits": len(er["q_orbits"]), "crit_orbits": len(ercrit),
                       "target_933_941_orbits": 0,
                       "status": "frozen ES/ER result readback holds; generation/coloring not replayed"})
    counts.update({"named_cactus_controls": 58,
                   "named_nonsingleton_count_identity_triggered": sum(c["count_status"] == "triggered and holds" for c in cacti),
                   "finite_NA_layers_read_back": len(finite), "parameter_rows": len(parameter_rows())})
    return {"base_head": BASE, "scope": "integer profiles and frozen controls only; no new source graph enumeration",
            "inputs": inputs, "parameter_rows": parameter_rows(), "named_cactus_controls": cacti,
            "fixed_component_controls": components, "finite_NA_readback": finite, "counts": dict(counts),
            "exact_slack_formula": "|H|=35-6u-3t-[3(5-|D|)+sum_C(delta_C)]",
            "delta_nonsingleton": "3a_C+2n1_C+2b_C+n4_C",
            "delta_singleton": 2, "original_55": "OPEN", "N2": "OPEN", "E_ARC2": "OPEN",
            "evidence_limit": "Arithmetic does not prove a uniform positive slack, source existence, source exclusion, or a Lean theorem."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "observations.json")
    args = parser.parse_args()
    data = produce()
    raw = encoded(data)
    if args.check:
        assert args.output.read_bytes() == raw, "artifact mismatch"
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as f:
            f.write(raw)
    print(json.dumps({"check": args.check, "sha256": sha256(raw).hexdigest(), "bytes": len(raw),
                      **data["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
