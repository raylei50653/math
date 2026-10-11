#!/usr/bin/env python3
"""Independent fixed-source DFS and attachment arithmetic; no graph search.

Reads only BASE-frozen snapshots. Does not import or execute the old checker.
Generation exclusively creates a new artifact; --check reads and compares it.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
BASE = AUDIT / "BASE.json"
SOURCE = "artifacts/c5_excess_two_arc_component_slack/observations.json"
OLD = "audits/2026-10-11-n2-unary-three-row-escape/observations.json"
LEAF = "artifacts/c5_excess_two_arc_leaf_blocks/observations.json"
PINS = tuple(product(range(4), repeat=2))
QS = ((0, (0, 1, 2, 1, 2)), (1, (0, 1, 2, 0, 2)), (3, (0, 1, 0, 2, 1)))
BEDGES = tuple(sorted(tuple(sorted((i, (i + 1) % 5))) for i in range(5)))
ROWS = tuple(sorted(beta for beta in product(range(4), repeat=5)
                    if beta[0] == 0 and all(beta[i] != beta[(i + 1) % 5] for i in range(5))
                    and all(beta[i] <= 1 + max(beta[:i], default=-1) for i in range(5))))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def clean(edges):
    result = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    require(len(set(result)) == len(result) and all(a != b for a, b in result), "non-simple edges")
    return result


def adjacencies(vertices, edges):
    answer = {v: set() for v in vertices}
    for a, b in edges:
        require(a in answer and b in answer, "edge outside named vertices")
        answer[a].add(b)
        answer[b].add(a)
    return answer


def components(vertices, edges):
    vertices = set(vertices)
    adj = adjacencies(vertices, [e for e in edges if set(e) <= vertices])
    unseen, answer = set(vertices), []
    while unseen:
        reached, pending = set(), [min(unseen)]
        while pending:
            v = pending.pop()
            if v in reached:
                continue
            reached.add(v)
            pending.extend(adj[v] - reached)
        unseen -= reached
        answer.append(tuple(sorted(reached)))
    return tuple(sorted(answer))


def blocks(vertices, edges):
    """Split on literal articulation vertices, independent of Tarjan low-link."""
    vertices = tuple(sorted(vertices))
    require(len(components(vertices, edges)) == 1, "disconnected local component")
    if len(vertices) == 1:
        return ()
    for cut in vertices:
        pieces = components(set(vertices) - {cut}, edges)
        if len(pieces) > 1:
            answer = []
            for piece in pieces:
                part = set(piece) | {cut}
                answer.extend(blocks(part, [e for e in edges if set(e) <= part]))
            return tuple(sorted(answer))
    return (vertices,)


def full_lifts(vertices, edges, fixed):
    """Dynamic smallest-domain DFS; store complete ordered vertex tuples."""
    vertices = tuple(vertices)
    adj = adjacencies(set(vertices) | set(fixed), edges)
    if any(a in fixed and b in fixed and fixed[a] == fixed[b] for a, b in edges):
        return []
    colors, lifts = dict(fixed), []

    def visit(remaining):
        if not remaining:
            lifts.append(tuple(colors[v] for v in vertices))
            return
        options = []
        for v in remaining:
            forbidden = {colors[w] for w in adj[v] if w in colors}
            allowed = tuple(c for c in range(4) if c not in forbidden)
            if not allowed:
                return
            options.append((len(allowed), -len(adj[v]), v, allowed))
        _, _, v, allowed = min(options)
        for color in allowed:
            colors[v] = color
            visit(remaining - {v})
        del colors[v]

    visit(set(vertices))
    require(len(set(lifts)) == len(lifts), "duplicate full lift")
    return [list(lift) for lift in sorted(lifts)]


def fibres(vertices, edges, roots, beta):
    return [full_lifts(vertices, edges, dict(enumerate(beta)) | dict(zip(roots, pin))) for pin in PINS]


def prerequisites(vertices, region, roots):
    verts = set(vertices)
    adj = adjacencies(verts | set(roots) | set(range(5)), region)
    internal = [e for e in region if set(e) <= verts]
    bs = blocks(vertices, internal)
    memberships = Counter(v for b in bs for v in b)
    contacts = {v for v in vertices if adj[v] & set(roots)}
    incidence = [sum(root in adj[v] for v in vertices) for root in roots]
    owners = [i for i, count in enumerate(incidence) if count]
    attachment = {v: sorted(adj[v] & set(range(5))) for v in vertices}
    h2 = [v for v in vertices if len(adj[v] & (verts | set(roots))) == 2]
    cactus, ordinary_cap, private_leaf = True, True, True
    for b in bs:
        badj = adjacencies(b, [e for e in internal if set(e) <= set(b)])
        odd_cycle = len(b) >= 3 and len(b) % 2 == 1 and all(len(badj[v]) == 2 for v in b)
        cactus &= len(b) == 2 or odd_cycle
        if odd_cycle:
            ordinary_cap &= sum(memberships[v] == 1 and v not in contacts for v in b) <= 1
        if len(bs) > 1 and sum(memberships[v] > 1 for v in b) == 1:
            private_leaf &= any(v in contacts and memberships[v] == 1 for v in b)
    conditions = {
        "unary_two_or_three_contacts": len(owners) == 1 and incidence[owners[0]] in (2, 3),
        "complete_degree_four": all(len(adj[v]) == 4 for v in vertices),
        "boundary_at_most_adjacent_two": all(len(a) <= 2 and (len(a) < 2 or tuple(a) in BEDGES)
                                                for a in attachment.values()),
        "support_at_least_three": len(set().union(*(set(a) for a in attachment.values()))) >= 3,
        "odd_cactus": cactus,
        "ordinary_private_cycle_cap_one": ordinary_cap,
        "private_contact_in_each_leaf_block": private_leaf,
        "H_degree_two_attachment_injective": len({tuple(attachment[v]) for v in h2}) == len(h2),
    }
    return {"conditions": conditions, "triggered": all(conditions.values()), "blocks": [list(b) for b in bs],
            "root_incidence": incidence, "ordered_root_contacts": [v for v in vertices if v in contacts],
            "boundary_attachments": [[v, attachment[v]] for v in vertices], "H_degree_two_vertices": h2,
            "owner_coordinate_index": owners[0] if len(owners) == 1 else None}


def boundary_arithmetic():
    """Solve simultaneously for actual frame attachments, without signature lookup."""
    betas = [beta for _, beta in QS]
    points = [tuple(beta[v] for beta in betas) for v in range(5)]
    third = [tuple(next(c for c in range(3) if c not in (beta[a], beta[b])) for beta in betas)
             for a, b in BEDGES]
    pairs = []
    for i, j in product(range(5), repeat=2):
        different = all(third[i][row] != third[j][row] for row in range(3))
        actual = [v for v in range(5) if all(len({third[i][row], third[j][row], betas[row][v]}) == 3
                                           for row in range(3))]
        require(not actual, "two-edge simultaneous actual point found")
        pairs.append({"edges": [BEDGES[i], BEDGES[j]], "rowwise_distinct": different,
                      "simultaneous_actual_point_solutions": actual})
    triples = []
    for ids in combinations(range(5), 3):
        palette_candidates = [colors for colors in product(range(3), repeat=3)
                              if all(colors[row] != third[j][row] for j in ids for row in range(3))]
        feasible = []
        for colors in palette_candidates:
            actual = [[v for v in range(5) if all(len({third[j][row], colors[row], betas[row][v]}) == 3
                                                  for row in range(3))] for j in ids]
            feasible.append({"cycle_colors_by_q": colors, "actual_point_choices_by_edge": actual,
                             "full_attachment_tuples": list(product(*actual))})
        require(not any(row["full_attachment_tuples"] for row in feasible), "central triangle actual attachment found")
        triples.append({"edges": [BEDGES[j] for j in ids], "candidates": feasible})
    return {"boundary_points": points, "edge_T_signatures": [{"edge": e, "signature": t} for e, t in zip(BEDGES, third)],
            "ordered_pairs": pairs, "unordered_distinct_triples": triples,
            "ordered_pairs_rowwise_distinct": sum(x["rowwise_distinct"] for x in pairs),
            "triples_with_abstract_cycle_palette": sum(bool(x["candidates"]) for x in triples),
            "triples_with_complete_actual_attachments": 0}


def normalized_row(beta):
    mapping = {}
    return tuple(mapping.setdefault(c, len(mapping)) for c in beta)


def d5_masks(mask):
    return sorted({sum(1 << ROWS.index(normalized_row([ROWS[j][(shift + direction * i) % 5] for i in range(5)]))
                       for j in range(10) if mask & (1 << j))
                   for shift in range(5) for direction in (-1, 1)})


def named_controls(old):
    specs = [{"name": s["name"], "vertices": s["vertices"], "roots": s["roots"], "region": s["region"]}
             for s in old["named_controls"]]
    specs.extend([
        {"name": "same_literal_P3_split_root_contacts", "vertices": [7, 8, 9], "roots": [5, 6],
         "region": [[7, 8], [8, 9], [5, 7], [6, 8], [5, 9], [0, 7], [1, 7], [3, 8], [2, 9], [3, 9]]},
        {"name": "one_literal_shared_contact_DD_slack", "vertices": [7], "roots": [5, 6],
         "region": [[5, 7], [6, 7], [0, 7], [1, 7]]},
    ])
    for index, spec in enumerate(specs):
        edges = clean(spec["region"])
        spec["region"] = [list(e) for e in edges]
        spec["prerequisites"] = prerequisites(spec["vertices"], edges, spec["roots"])
        spec["rows"] = [{"beta": list(beta), "full_local_fibres_by_pins": fibres(spec["vertices"], edges, spec["roots"], beta)}
                        for beta in ROWS]
        spec["DD_escape_rows"] = [q for q, beta in QS if spec["rows"][ROWS.index(beta)]["full_local_fibres_by_pins"][15]]
        spec["graph_scope"] = "fixed literal local control; disk, Sigma-criticality and N2 target source not claimed"
        if index < 3:
            require(spec["prerequisites"] == old["named_controls"][index]["prerequisites"], "named control prerequisites differ")
            require(spec["rows"] == old["named_controls"][index]["rows"], "named control complete fibres differ")
    require(specs[0]["DD_escape_rows"] == [] and not specs[0]["prerequisites"]["conditions"]["H_degree_two_attachment_injective"],
            "injectivity negative control did not refute weakened claim")
    require(specs[1]["DD_escape_rows"] == [3] and specs[1]["prerequisites"]["triggered"], "k3 positive control failed")
    require(specs[2]["DD_escape_rows"] == [] and not specs[2]["prerequisites"]["conditions"]["support_at_least_three"],
            "span negative control did not refute weakened claim")
    require(specs[3]["DD_escape_rows"] == [3], "split-root DD transfer control failed")
    require(specs[4]["DD_escape_rows"] == [0, 1, 3], "shared-contact DD slack control failed")
    return specs


def produce():
    base_raw = BASE.read_bytes()
    base = json.loads(base_raw)
    index = {record["path"]: record for record in base["inputs"]}
    inputs, loaded = [], {}
    for path in (SOURCE, OLD, LEAF):
        entry = index[path]
        raw = (ROOT / entry["snapshot"]).read_bytes()
        require(len(raw) == entry["bytes"] and sha256(raw).hexdigest() == entry["sha256"], "frozen input checksum differs")
        loaded[path] = json.loads(raw)
        inputs.append(entry)
    source, old, leaf = loaded[SOURCE], loaded[OLD], loaded[LEAF]
    require(len(ROWS) == 10 and len(source["records"]) == len(leaf["records"]) == 63, "unexpected fixed input dimensions")
    old_unary = {record["original_component_pointer"]: record for record in old["fixed_original_unary_records"]}
    counts, graph_checks, unaries = Counter(), [], []
    target_masks = set(d5_masks(933) + d5_masks(941))
    for gi, graph in enumerate(source["records"]):
        edges, roots, interior = clean(graph["edges"]), tuple(graph["roots"]), tuple(graph["interior_coordinates"])
        adj = adjacencies(set(range(5)) | set(interior), edges)
        graph_vertices = tuple(v for v in interior if v not in roots)
        pieces = components(graph_vertices, edges)
        require(pieces == tuple(tuple(c["vertices"]) for c in graph["components"]), "source component split differs")
        component_edges = [tuple(e for e in edges if set(e) & set(c["vertices"])) for c in graph["components"]]
        require(all(list(map(list, e)) == c["edges"] for e, c in zip(component_edges, graph["components"])), "original incident region differs")
        component_rows = [[fibres(c["vertices"], region, roots, beta) for beta in ROWS]
                          for c, region in zip(graph["components"], component_edges)]
        sigma, full_rows = 0, []
        for ri, beta in enumerate(ROWS):
            direct = fibres(graph_vertices, edges, roots, beta)
            joined = []
            for pi, pin in enumerate(PINS):
                fixed = dict(enumerate(beta)) | dict(zip(roots, pin))
                all_fixed_proper = all(fixed[a] != fixed[b] for a, b in edges if a in fixed and b in fixed)
                join = []
                if all_fixed_proper:
                    for parts in product(*(rows[ri][pi] for rows in component_rows)):
                        assigned = {v: color for piece, colors in zip(pieces, parts) for v, color in zip(piece, colors)}
                        join.append([assigned[v] for v in graph_vertices])
                joined.append(sorted(join))
            require(direct == joined, "complete whole graph tuple join differs from independent DFS")
            sigma |= (1 << ri) if any(direct) else 0
            counts["whole_graph_full_fibre_rows"] += 1
            counts["whole_graph_ambient_pin_cells"] += 16
            full_rows.append({"beta": beta, "full_graph_fibres_by_pins": direct})
        require(sigma == graph["sigma_mask"], "complete source Sigma differs")
        candidate_target = sigma in target_masks
        target_prerequisites = {"complete_Sigma933_941_or_D5_image": candidate_target,
                                "two_original_degree5_roots": all(len(adj[r]) == 5 for r in roots),
                                "nonadjacent_roots": roots[1] not in adj[roots[0]],
                                "other_original_interior_degree4": all(len(adj[v]) == 4 for v in graph_vertices)}
        require(not candidate_target, "unexpected full target Sigma source requires a larger prerequisite audit")
        graph_checks.append({"original_graph_pointer": f"/records/{gi}", "original_graph_edges": [list(e) for e in edges],
                             "roots": roots, "ordered_nonroot_interior": graph_vertices, "complete_sigma": sigma,
                             "target_prerequisites_checked": target_prerequisites, "target_source_status": "not triggered",
                             "rows": full_rows})
        for ci, (c, region, rows) in enumerate(zip(graph["components"], component_edges, component_rows)):
            incidence = [sum(r in adj[v] for v in c["vertices"]) for r in roots]
            require(incidence == c["root_incidence"], "original contact incidence differs")
            if sum(n > 0 for n in incidence) != 1:
                continue
            pointer = f"/records/{gi}/components/{ci}"
            prior = old_unary[pointer]
            pre = prerequisites(c["vertices"], region, roots)
            require(pre == prior["prerequisites"], "independent prerequisite/block reconstruction differs")
            owner = next(i for i, count in enumerate(incidence) if count)
            failed, escaped, saved_rows = [], [], []
            for ri, beta in enumerate(ROWS):
                require(list(beta) == c["rows"][ri]["beta"], "literal row frame differs")
                require(rows[ri] == c["rows"][ri]["local_full_fibres_by_pins"], "source complete local tuple differs")
                require(rows[ri] == prior["rows"][ri]["full_local_fibres_by_pins"], "old unary complete local tuple differs")
                counts["full_fibre_rows"] += 1
                counts["ambient_pin_cells"] += 16
                counts["empty_cells"] += sum(not cell for cell in rows[ri])
                saved_rows.append({"beta": beta, "full_local_fibres_by_pins": rows[ri]})
                for q, target_beta in QS:
                    if beta == target_beta:
                        forbidden = not any(cell for pin, cell in zip(PINS, rows[ri]) if pin[owner] == 3)
                        (failed if forbidden else escaped).append(q)
            failed.sort()
            escaped.sort()
            require(failed == prior["D_forbidden_rows"] and escaped == prior["D_escape_rows"], "whole owner-pin quantifier differs")
            if pre["triggered"]:
                require(bool(escaped), "fixed local three-row escape counterexample")
                counts["local_lemma_triggered_and_holds"] += 1
                counts[f"triggered_k{incidence[owner]}"] += 1
            else:
                counts["local_lemma_not_triggered"] += 1
            unaries.append({"original_component_pointer": pointer, "original_graph_edges": graph["edges"],
                            "roots": roots, "vertices": c["vertices"], "region_edges": [list(e) for e in region],
                            "prerequisites": pre, "D_forbidden_rows": failed, "D_escape_rows": escaped,
                            "rows": saved_rows, "target_source_status": "not triggered"})
    require(len(unaries) == len(old_unary), "frozen unary domain lost records")
    controls = named_controls(old)
    arithmetic = boundary_arithmetic()
    counts.update({"fixed_original_unaries": len(unaries), "source_graphs": len(graph_checks),
                   "named_local_controls": len(controls), "named_local_ambient_pin_cells": len(controls) * 160,
                   "target_source_triggered": 0, "target_source_not_triggered": len(graph_checks)})
    return {"base_head": base["head"], "base_sha256": sha256(base_raw).hexdigest(), "frozen_inputs": inputs,
            "scope": "fixed original graph controls; independent MRV DFS and complete whole-graph joins; no source search",
            "pin_order": PINS, "literal_q_rows": dict(QS), "complete_canonical_rows": ROWS, "counts": dict(counts),
            "palette_arithmetic": arithmetic, "full_original_graph_checks": graph_checks,
            "fixed_original_unary_records": unaries, "named_controls": controls,
            "Sigma933_D5_masks": d5_masks(933), "Sigma941_D5_masks": d5_masks(941),
            "target_source_status": "not triggered",
            "evidence_limit": "Full tuples and joins are checked only on these fixed inputs. Disk/rotation, Sigma-criticality, arbitrary-size case-split completeness, source existence and Lean are not verified here."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=HERE / "observations.json")
    args = parser.parse_args()
    data = produce()
    raw = encode(data)
    if args.check:
        require(args.output.read_bytes() == raw, "artifact mismatch")
    else:
        with args.output.open("xb") as handle:
            handle.write(raw)
    print(json.dumps({"check": args.check, "bytes": len(raw), "sha256": sha256(raw).hexdigest(), **data["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
