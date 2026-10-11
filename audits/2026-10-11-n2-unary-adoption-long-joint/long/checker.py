#!/usr/bin/env python3
"""Recompute full local fibres on frozen long controls; no source search."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROWS = (0, 1, 3)
TARGET_BETAS = {0: [0, 1, 2, 1, 2], 1: [0, 1, 2, 0, 2],
                3: [0, 1, 0, 2, 1]}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def frozen(path):
    base = json.loads((AUDIT / "BASE.json").read_bytes())
    item = next(x for x in base["inputs"] if x["path"] == path)
    data = (AUDIT / "frozen" / (path + ".snapshot")).read_bytes()
    assert len(data) == item["bytes"] and digest(data) == item["sha256"]
    return json.loads(data), item


def fibres(vertices, edges, roots, beta):
    """All numeric-order assignments, with all 16 ambient ordered pin cells."""
    order = sorted(vertices)
    neighbors = {v: set() for v in order}
    for a, b in edges:
        if a in neighbors:
            neighbors[a].add(b)
        if b in neighbors:
            neighbors[b].add(a)
    answer = []
    for a in range(4):
        for b in range(4):
            colors = dict(enumerate(beta))
            colors.update(zip(roots, (a, b)))
            lifts = []

            def visit(index):
                if index == len(order):
                    lifts.append([colors[v] for v in order])
                    return
                v = order[index]
                forbidden = {colors[w] for w in neighbors[v] if w in colors}
                for color in range(4):
                    if color not in forbidden:
                        colors[v] = color
                        visit(index + 1)
                        del colors[v]

            visit(0)
            answer.append(lifts)
    return answer


def local_geometry(vertices, edges, roots):
    vertices = set(vertices)
    contacts = [[v for v in sorted(vertices) if tuple(sorted((v, r))) in edges]
                for r in roots]
    attachments = {v: sorted(w for w in range(5)
                            if tuple(sorted((v, w))) in edges)
                   for v in sorted(vertices)}
    support = sorted(set().union(*map(set, attachments.values())))
    shared = sorted(set(contacts[0]) & set(contacts[1]))
    return contacts, attachments, support, shared


def record(vertices, edges, roots, table, reference):
    edge_set = {tuple(sorted(e)) for e in edges}
    contacts, attachments, support, shared = local_geometry(
        vertices, edge_set, roots)
    rows = []
    for i, beta in enumerate(table):
        rows.append({"row_index": i, "beta": beta,
                     "full_local_fibres_by_ordered_pins":
                     fibres(vertices, edge_set, roots, beta)})
    by_beta = {tuple(row["beta"]): row for row in rows}
    missing = [i for i in ROWS if not by_beta[tuple(TARGET_BETAS[i])]
               ["full_local_fibres_by_ordered_pins"][15]]
    degree_four = all(sum(v in e for e in edge_set) == 4 for v in vertices)
    if shared and degree_four:
        assert missing == []
    return {"reference": reference, "vertices": sorted(vertices),
            "original_edges": sorted(map(list, edge_set)),
            "ordered_roots": roots, "ordered_contacts": contacts,
            "literal_shared_contacts": shared,
            "actual_attachments": attachments,
            "actual_support": support, "root_incidences": list(map(len, contacts)),
            "complete_degree_four": degree_four,
            "diagonal_rejection_mask": missing, "rows": rows}


def generate():
    original, source = frozen("artifacts/c5_excess_two_arc_component_slack/observations.json")
    table = [x["beta"] for x in original["records"][0]["components"][0]["rows"]]
    assert all(beta in table for beta in TARGET_BETAS.values())
    records = []
    for gindex, graph in enumerate(original["records"]):
        roots = graph["roots"]
        for cindex, piece in enumerate(graph["components"]):
            edges = {tuple(sorted(e)) for e in piece["edges"]}
            contacts, _, support, _ = local_geometry(piece["vertices"], edges, roots)
            long = len(support) >= 3 or (len(support) == 2
                   and (support[1] - support[0]) not in (1, 4))
            if not long or not all(contacts):
                continue
            item = record(piece["vertices"], piece["edges"], roots, table,
                          f"/records/{gindex}/components/{cindex}")
            for i, row in enumerate(piece["rows"]):
                assert item["rows"][i]["full_local_fibres_by_ordered_pins"] == \
                    row["local_full_fibres_by_pins"]
            records.append(item)

    boundary = [(i, (i + 1) % 5) for i in range(5)]
    controls = []
    specs = [
        ("mixed_three_contact_path", [7, 8, 9],
         [(7, 8), (8, 9), (5, 7), (5, 8), (6, 9),
          (0, 7), (1, 7), (3, 8), (2, 9), (3, 9)], [0, 1]),
        ("long_literal_shared_contact", [7, 8],
         [(7, 8), (5, 7), (6, 7), (5, 8), (0, 7), (1, 8), (2, 8)], []),
        ("negative_without_degree_two_attachment_injectivity", [7, 8],
         [(7, 8), (5, 7), (6, 8), (0, 7), (1, 7), (0, 8), (1, 8)], [0, 1, 3]),
        ("negative_without_long_support", [7, 8, 9],
         [(7, 8), (8, 9), (7, 9), (5, 7), (6, 8), (5, 9),
          (0, 7), (0, 8), (0, 9)], [0, 1, 3]),
    ]
    for name, vertices, edges, expected in specs:
        item = record(vertices, boundary + edges, [5, 6], table, name)
        assert item["diagonal_rejection_mask"] == expected
        item["expected_mask"] = expected
        item["source_realization_status"] = "not triggered"
        item["control_status"] = ("counterexample" if name.startswith("negative")
                                  else "triggered and holds")
        controls.append(item)

    # The equations used for the row-independent D-pattern have a unique
    # solution in any original cactus incidence tree. Check named tiny trees
    # without asserting that these abstract trees are source realizations.
    pattern_controls = []
    for name, blocks in [
        ("two_bridges", [[0, 1], [1, 2]]),
        ("bridge_triangle_bridge", [[0, 1], [1, 2, 3], [3, 4]]),
        ("two_triangles_one_shared_cut", [[0, 1, 2], [2, 3, 4]]),
        ("three_bridge_star", [[0, 1], [0, 2], [0, 3]]),
        ("triangle_three_bridges", [[0, 1, 2], [0, 3], [1, 4], [2, 5]]),
    ]:
        signatures = {}
        vertices = sorted(set().union(*map(set, blocks)))
        for bits in range(1 << len(blocks)):
            y = [(bits >> j) & 1 for j in range(len(blocks))]
            rhs = tuple(sum(y[j] for j, block in enumerate(blocks) if v in block)
                        for v in vertices)
            assert rhs not in signatures
            signatures[rhs] = y
        pattern_controls.append({"name": name, "original_blocks": blocks,
                                 "assignments": len(signatures),
                                 "status": "triggered and holds"})

    count_rows = len(records) * 10
    counts = {"frozen_long_mixed_pieces": len(records),
              "rows_recomputed": count_rows,
              "ambient_ordered_pin_cells": count_rows * 16,
              "empty_cells": sum(not cell for item in records
                                 for row in item["rows"]
                                 for cell in row["full_local_fibres_by_ordered_pins"]),
              "literal_shared_degree_four_controls": sum(
                  bool(x["literal_shared_contacts"]) and x["complete_degree_four"]
                  for x in records),
              "long_support_at_least_three_contact_three_controls": sum(
                  len(x["actual_support"]) >= 3
                  and sum(x["root_incidences"]) <= 3
                  and x["complete_degree_four"] for x in records),
              "new_named_local_controls": len(controls),
              "target_sources": 0}
    return {"scope": "frozen local full-fibre controls, no target source search",
            "source_path": source["path"], "source_sha256": source["sha256"],
            "ordered_pin_order": [[a, b] for a in range(4) for b in range(4)],
            "target_row_labels_and_literal_beta": TARGET_BETAS,
            "target_source_status": "not triggered", "counts": counts,
            "records": records, "named_controls": controls,
            "D_pattern_equation_controls": pattern_controls}


def main():
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    parser.add_argument("--artifact", type=Path, default=HERE / "observations.json")
    args = parser.parse_args()
    result = generate()
    encoded = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
    if args.write:
        with args.artifact.open("xb") as handle:
            handle.write(encoded)
    elif args.artifact.read_bytes() != encoded:
        raise SystemExit("artifact mismatch")
    print(json.dumps({"mode": "write" if args.write else "check",
                      "sha256": digest(encoded), "bytes": len(encoded),
                      "counts": result["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
