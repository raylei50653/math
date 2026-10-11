#!/usr/bin/env python3
"""Same-frame unary controls and three-row palette arithmetic; no source search."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = "5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc"
SOURCE = "artifacts/c5_excess_two_arc_component_slack/observations.json"
LEAF = "artifacts/c5_excess_two_arc_leaf_blocks/observations.json"
QS = {0: (0, 1, 2, 1, 2), 1: (0, 1, 2, 0, 2), 3: (0, 1, 0, 2, 1)}
BEDGES = tuple(tuple(sorted((i, (i + 1) % 5))) for i in range(5))
PINS = tuple(product(range(4), repeat=2))


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def adjacency(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        assert a != b and a in adj and b in adj
        adj[a].add(b)
        adj[b].add(a)
    return adj


def blocks(vertices, edges):
    """Independent Tarjan traversal; bridges remain literal K2 blocks."""
    adj = adjacency(vertices, edges)
    order, low, stack, out = {}, {}, [], []

    def visit(v, parent=None):
        order[v] = low[v] = len(order)
        for w in sorted(adj[v]):
            if w == parent:
                continue
            if w not in order:
                stack.append((v, w))
                visit(w, v)
                low[v] = min(low[v], low[w])
                if low[w] >= order[v]:
                    block = set()
                    while True:
                        edge = stack.pop()
                        block.update(edge)
                        if edge == (v, w):
                            break
                    out.append(sorted(block))
            elif order[w] < order[v]:
                stack.append((v, w))
                low[v] = min(low[v], order[w])

    visit(min(vertices))
    assert set(order) == set(vertices) and not stack
    return sorted(out)


def full_fibres(vertices, edges, roots, beta):
    """Exhaustive numeric-order DFS, retaining every ambient root-pin cell."""
    adj = adjacency(set(vertices) | set(roots) | set(range(5)), edges)
    answer = []
    for pin in PINS:
        colors = {**dict(enumerate(beta)), **dict(zip(roots, pin))}
        if any(a in colors and b in colors and colors[a] == colors[b] for a, b in edges):
            answer.append([])
            continue
        lifts = []

        def visit(position):
            if position == len(vertices):
                lifts.append([colors[v] for v in vertices])
                return
            v = vertices[position]
            forbidden = {colors[w] for w in adj[v] if w in colors}
            for color in range(4):
                if color not in forbidden:
                    colors[v] = color
                    visit(position + 1)
            colors.pop(v, None)

        visit(0)
        answer.append(lifts)
    return answer


def prerequisites(vertices, region, roots):
    """Local hypotheses of REPORT section 2, reconstructed from original edges."""
    verts = set(vertices)
    adj = adjacency(verts | set(roots) | set(range(5)), region)
    internal = [e for e in region if set(e) <= verts]
    bs = blocks(vertices, internal)
    counts = Counter(v for block in bs for v in block)
    contacts = {v for v in vertices if adj[v] & set(roots)}
    root_incidence = [sum(r in adj[v] for v in vertices) for r in roots]
    owners = [i for i, k in enumerate(root_incidence) if k]
    boundary = {v: sorted(adj[v] & set(range(5))) for v in vertices}
    d2 = [v for v in vertices if len(adj[v] & (verts | set(roots))) == 2]
    d2_pairs = [tuple(boundary[v]) for v in d2]
    odd_cactus = True
    normal_private_cap = True
    leaf_contacts = True
    for block in bs:
        be = [e for e in internal if set(e) <= set(block)]
        badj = adjacency(block, be)
        cycle = len(block) >= 3 and len(block) % 2 == 1 and all(len(badj[v]) == 2 for v in block)
        odd_cactus &= len(block) == 2 or cycle
        ordinary = [v for v in block if counts[v] == 1 and v not in contacts]
        if cycle:
            normal_private_cap &= len(ordinary) <= 1
        if len(bs) > 1 and sum(counts[v] > 1 for v in block) == 1:
            leaf_contacts &= any(v in contacts and counts[v] == 1 for v in block)
    conditions = {
        "unary_two_or_three_contacts": len(owners) == 1 and root_incidence[owners[0]] in (2, 3),
        "complete_degree_four": all(len(adj[v]) == 4 for v in vertices),
        "boundary_at_most_adjacent_two": all(len(p) <= 2 and (len(p) < 2 or tuple(p) in BEDGES)
                                             for p in boundary.values()),
        "support_at_least_three": len(set().union(*(set(p) for p in boundary.values()))) >= 3,
        "odd_cactus": odd_cactus,
        "ordinary_private_cycle_cap_one": normal_private_cap,
        "private_contact_in_each_leaf_block": leaf_contacts,
        "H_degree_two_attachment_injective": len(set(d2_pairs)) == len(d2_pairs),
    }
    return {"conditions": conditions, "triggered": all(conditions.values()), "blocks": bs,
            "root_incidence": root_incidence, "ordered_root_contacts": [v for v in vertices if v in contacts],
            "boundary_attachments": [[v, boundary[v]] for v in vertices], "H_degree_two_vertices": d2,
            "owner_coordinate_index": owners[0] if len(owners) == 1 else None}


def palette_arithmetic():
    qlist = list(QS.values())
    point_sigs = [tuple(q[v] for q in qlist) for v in range(5)]
    third = [tuple(next(iter({0, 1, 2} - {q[a], q[b]})) for q in qlist) for a, b in BEDGES]
    assert len(set(point_sigs)) == len(set(third)) == 5
    pairs = []
    for a, b in product(range(5), repeat=2):
        distinct = all(x != y for x, y in zip(third[a], third[b]))
        record = {"edges": [BEDGES[a], BEDGES[b]], "T_signatures": [third[a], third[b]],
                  "rowwise_distinct": distinct}
        if distinct:
            rest = tuple(next(iter({0, 1, 2} - {x, y})) for x, y in zip(third[a], third[b]))
            record.update({"remaining_used_color_signature": rest,
                           "matching_boundary_points": [i for i, s in enumerate(point_sigs) if s == rest],
                           "matching_boundary_edges_T": [BEDGES[i] for i, s in enumerate(third) if s == rest]})
            assert rest not in point_sigs and rest not in third
        pairs.append(record)
    assert sum(r["rowwise_distinct"] for r in pairs) == 4
    triples = []
    for ids in combinations(range(5), 3):
        seen = [set(third[j][qi] for j in ids) for qi in range(3)]
        possible = list(product(*(sorted({0, 1, 2} - s) for s in seen)))
        candidates = []
        for cycle_color in possible:
            needed = [tuple(next(iter({0, 1, 2} - {third[j][qi], cycle_color[qi]}))
                            for qi in range(3)) for j in ids]
            missing = [i for i, s in enumerate(needed) if s not in point_sigs]
            assert missing, "central triangle palette unexpectedly has all actual attachments"
            candidates.append({"cycle_other_color_signature": cycle_color,
                               "required_cutpoint_boundary_signatures": needed,
                               "missing_boundary_signature_positions": missing})
        triples.append({"leaf_edges": [BEDGES[i] for i in ids], "row_T_color_sets": [sorted(s) for s in seen],
                        "candidate_cycle_palettes_with_D": candidates, "all_three_rows_feasible": False})
    assert sum(bool(r["candidate_cycle_palettes_with_D"]) for r in triples) == 2
    return {"q_order": list(QS), "boundary_point_signatures": point_sigs,
            "T_edge_signatures": [{"edge": e, "signature": t} for e, t in zip(BEDGES, third)],
            "ordered_edge_pairs": pairs, "distinct_edge_triples": triples}


def named_controls():
    specs = [
        {"name": "repeat_D_edge_without_injectivity", "vertices": [7, 8], "roots": [5, 6],
         "region": [[7, 8], [5, 7], [5, 8], [0, 7], [1, 7], [0, 8], [1, 8]],
         "meaning": "counterexample to deleting the H-degree-two attachment injectivity hypothesis"},
        {"name": "same_U_two_rows_do_not_suffice", "vertices": [7, 8, 9], "roots": [5, 6],
         "region": [[7, 8], [8, 9], [5, 7], [5, 8], [5, 9], [0, 7], [1, 7], [3, 8], [2, 9], [3, 9]],
         "meaning": "q0 and q1 forbid D, q3 admits D on this one literal unary"},
        {"name": "single_triangle_support_one_without_span", "vertices": [7, 8, 9], "roots": [5, 6],
         "region": [[7, 8], [8, 9], [7, 9], [5, 7], [5, 8], [5, 9], [0, 7], [0, 8], [0, 9]],
         "meaning": "counterexample to deleting the unary support-size hypothesis"},
    ]
    ten_rows = sorted({tuple([0, 1, *tail]) for tail in product(range(4), repeat=3)
                       if all([0, 1, *tail][i] != [0, 1, *tail][(i + 1) % 5] for i in range(5))
                       and max([0, 1, *tail]) <= 3
                       and all(c <= 1 + max([0, 1, *tail][:i]) for i, c in enumerate(tail, 2))})
    assert len(ten_rows) == 10
    for spec in specs:
        spec["region"] = sorted([sorted(e) for e in spec["region"]])
        pre = prerequisites(spec["vertices"], spec["region"], spec["roots"])
        rows, failed = [], []
        for beta in ten_rows:
            fibres = full_fibres(spec["vertices"], spec["region"], spec["roots"], beta)
            rows.append({"beta": beta, "full_local_fibres_by_pins": fibres})
            if beta in QS.values() and all(not fibre for pin, fibre in zip(PINS, fibres) if pin[0] == 3):
                failed.append(next(i for i, q in QS.items() if q == beta))
        spec.update({"prerequisites": pre, "rows": rows, "D_forbidden_rows": sorted(failed),
                     "graph_scope": "fixed local degree-four control only; no target-source or disk claim"})
    assert specs[0]["D_forbidden_rows"] == [0, 1, 3]
    assert not specs[0]["prerequisites"]["conditions"]["H_degree_two_attachment_injective"]
    assert specs[1]["D_forbidden_rows"] == [0, 1]
    assert specs[1]["prerequisites"]["triggered"]
    assert specs[2]["D_forbidden_rows"] == [0, 1, 3]
    assert not specs[2]["prerequisites"]["conditions"]["support_at_least_three"]
    return specs


def produce():
    inputs, loaded = [], []
    for path in (SOURCE, LEAF):
        raw = (ROOT / path).read_bytes()
        inputs.append({"path": path, "sha256": sha256(raw).hexdigest(), "bytes": len(raw)})
        loaded.append(json.loads(raw))
    source, leaf = loaded
    assert len(source["records"]) == len(leaf["records"]) == 63
    assert leaf["literal_q_rows"] == {str(q): list(beta) for q, beta in QS.items()}
    assert leaf["pin_order"] == [list(pin) for pin in PINS]
    records, counts = [], Counter()
    for gi, (g, lg) in enumerate(zip(source["records"], leaf["records"])):
        assert g["edges"] == lg["edges"] and g["roots"] == lg["roots"]
        assert len(g["components"]) == len(lg["components"])
        for ci, (c, lc) in enumerate(zip(g["components"], lg["components"])):
            owners = [i for i, k in enumerate(c["root_incidence"]) if k]
            if len(owners) != 1:
                continue
            assert c["vertices"] == lc["vertices"] and c["edges"] == lc["edges"]
            pre = prerequisites(c["vertices"], c["edges"], g["roots"])
            assert pre["blocks"] == sorted(b["vertices"] for b in lc["blocks"])
            assert pre["root_incidence"] == c["root_incidence"]
            owner = owners[0]
            rows, failed, escaped = [], [], []
            for ri, row in enumerate(c["rows"]):
                beta = tuple(row["beta"])
                fibres = full_fibres(c["vertices"], c["edges"], g["roots"], beta)
                assert fibres == row["local_full_fibres_by_pins"], "complete original local fibres differ"
                counts["full_fibre_rows"] += 1
                counts["ambient_pin_cells"] += len(fibres)
                counts["empty_cells"] += sum(not f for f in fibres)
                item = {"source_pointer": f"/records/{gi}/components/{ci}/rows/{ri}/local_full_fibres_by_pins",
                        "beta": beta, "full_local_fibres_by_pins": fibres}
                if beta in QS.values():
                    q = next(q for q, val in QS.items() if val == beta)
                    candidates = [(pin, f) for pin, f in zip(PINS, fibres) if pin[owner] == 3]
                    d_forbidden = not any(f for _, f in candidates)
                    item.update({"named_q": q, "D_forbidden": d_forbidden})
                    if d_forbidden:
                        failed.append(q)
                    else:
                        escaped.append(q)
                        pin, f = next((pin, f) for pin, f in candidates if f)
                        item["D_escape_full_lift"] = {"ordered_root_pin": pin, "complete_component_colors": f[0]}
                rows.append(item)
            assert len(rows) == 10 and len(failed) + len(escaped) == 3
            if pre["triggered"]:
                assert escaped, "local unary three-row escape counterexample"
                counts["local_lemma_triggered_and_holds"] += 1
            else:
                counts["local_lemma_not_triggered"] += 1
            assert not lg["target_source_triggered"]
            records.append({"original_graph_pointer": f"/records/{gi}", "original_component_pointer": f"/records/{gi}/components/{ci}",
                            "original_graph_edges": g["edges"], "original_sigma": g["sigma_mask"],
                            "roots": g["roots"], "vertices": c["vertices"], "region_edges": c["edges"],
                            "prerequisites": pre, "D_forbidden_rows": sorted(failed), "D_escape_rows": sorted(escaped),
                            "rows": rows, "target_source_status": "not triggered"})
    counts["fixed_original_unaries"] = len(records)
    assert len(records) == 97 and counts["ambient_pin_cells"] == 15520
    arithmetic = palette_arithmetic()
    controls = named_controls()
    counts.update({"ordered_edge_pairs": 25, "rowwise_distinct_edge_pairs": 4,
                   "distinct_edge_triples": 10, "central_triangle_feasible_triples": 0,
                   "named_local_controls": len(controls), "target_source_triggered": 0})
    return {"base_head": BASE, "scope": "same-frame frozen unary fibres and small palette tables; no source graph search",
            "inputs": inputs, "pin_order": PINS, "literal_q_rows": QS, "palette_arithmetic": arithmetic,
            "fixed_original_unary_records": records, "named_controls": controls, "counts": dict(counts),
            "paper_result": "N2-55-U-THREE-ROW-ESCAPE and (ell,u)=(0,1) paper exclusion",
            "independent_paper_adoption": "not performed in this run", "original_55": "OPEN", "N2": "OPEN", "E_ARC2": "OPEN",
            "evidence_limit": "Finite controls do not prove the arbitrary-size block-tree case split, source existence, or a Lean theorem."}


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
        with args.output.open("xb") as f:
            f.write(raw)
    print(json.dumps({"check": args.check, "bytes": len(raw), "sha256": sha256(raw).hexdigest(),
                      **data["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
