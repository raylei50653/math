#!/usr/bin/env python3
"""Frozen same-graph complete-fibre and bounded literal mask controls."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SOURCE = "artifacts/c5_excess_two_arc_component_slack/observations.json"
QS = {0: [0, 1, 2, 1, 2], 1: [0, 1, 2, 0, 2],
      3: [0, 1, 0, 2, 1]}
PINS = list(product(range(4), repeat=2))
BEDGES = sorted({tuple(sorted((i, (i + 1) % 5))) for i in range(5)})


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def edgeset(edges):
    result = {tuple(sorted(edge)) for edge in edges}
    assert all(a != b for a, b in result)
    return result


def assignments(vertices, edges, fixed):
    """All numeric-order full assignments; reject fixed-fixed conflicts too."""
    order = sorted(vertices)
    assert not set(order) & set(fixed)
    adj = {v: set() for v in set(order) | set(fixed)}
    for a, b in edges:
        assert a in adj and b in adj
        adj[a].add(b)
        adj[b].add(a)
    if any(a in fixed and b in fixed and fixed[a] == fixed[b]
           for a, b in edges):
        return []
    colors, result = dict(fixed), []

    def visit(index):
        if index == len(order):
            result.append([colors[v] for v in order])
            return
        v = order[index]
        forbidden = {colors[w] for w in adj[v] if w in colors}
        for color in range(4):
            if color not in forbidden:
                colors[v] = color
                visit(index + 1)
        colors.pop(v, None)

    visit(0)
    return result


def fibres(vertices, edges, roots, beta):
    return [assignments(vertices, edges,
                        {**dict(enumerate(beta)), **dict(zip(roots, pin))})
            for pin in PINS]


def geometry(vertices, edges, roots):
    vertices = sorted(vertices)
    contacts = [[v for v in vertices if tuple(sorted((r, v))) in edges]
                for r in roots]
    attachments = [[v, [b for b in range(5)
                        if tuple(sorted((v, b))) in edges]] for v in vertices]
    support = sorted({b for _, actual in attachments for b in actual})
    long = not any(set(support) <= set(edge) for edge in BEDGES)
    exact_arcs = []
    for start in range(5):
        points = [(start + j) % 5 for j in range(3)]
        if set(support) == set(points):
            exact_arcs.append({"start": start, "ordered_boundary_points": points,
                               "literal_boundary_edges": [sorted(points[:2]),
                                                          sorted(points[1:])]})
    return {"ordered_root_contacts": contacts,
            "root_incidences": list(map(len, contacts)),
            "literal_shared_contacts": sorted(set(contacts[0]) & set(contacts[1])),
            "actual_boundary_attachments": attachments,
            "actual_support": support, "long_support": long,
            "complete_degree_four": all(sum(v in edge for edge in edges) == 4
                                        for v in vertices),
            "exact_two_edge_support_arcs": exact_arcs,
            "shield_rotation_status": "not supplied by frozen calibration"}


def piece_record(vertices, edges, roots, table, reference):
    region = edgeset(edges)
    rows = [{"row_index": index, "literal_beta": beta,
             "full_local_fibres_by_ordered_pins": fibres(vertices, region, roots, beta)}
            for index, beta in enumerate(table)]
    by_beta = {tuple(row["literal_beta"]): row for row in rows}
    mask = [label for label, beta in QS.items()
            if not by_beta[tuple(beta)]["full_local_fibres_by_ordered_pins"][15]]
    result = {"reference": reference, "original_vertices": sorted(vertices),
              "original_region_edges": sorted(map(list, region)),
              "ordered_roots": roots, **geometry(vertices, region, roots),
              "diagonal_rejection_mask": mask, "rows": rows}
    if result["complete_degree_four"] and result["literal_shared_contacts"]:
        assert not mask
    return result


def graph_record(vertices, edges, roots, pieces, table, reference):
    """Join full component tuples at the same literal pins and check direct DFS."""
    edges = edgeset(edges)
    nonroots = sorted(set(vertices) - set(roots))
    assert set(nonroots) == {v for piece in pieces for v in piece["original_vertices"]}
    assert sum(len(piece["original_vertices"]) for piece in pieces) == len(nonroots)
    external = {edge for edge in edges if not set(edge) & set(nonroots)}
    rows = []
    for index, beta in enumerate(table):
        direct = fibres(nonroots, edges, roots, beta)
        joined = []
        for pin_index, pin in enumerate(PINS):
            fixed = {**dict(enumerate(beta)), **dict(zip(roots, pin))}
            cells = [piece["rows"][index]["full_local_fibres_by_ordered_pins"][pin_index]
                     for piece in pieces]
            tuples = []
            if not any(fixed[a] == fixed[b] for a, b in external):
                for local_lifts in product(*cells):
                    colors = {}
                    for piece, lift in zip(pieces, local_lifts):
                        colors.update(zip(piece["original_vertices"], lift))
                    tuples.append([colors[v] for v in nonroots])
            tuples.sort()
            assert tuples == direct[pin_index]
            joined.append(tuples)
        full = assignments(vertices, edges, dict(enumerate(beta)))
        reconstructed = []
        for pin, cell in zip(PINS, joined):
            for lift in cell:
                colors = {**dict(zip(roots, pin)), **dict(zip(nonroots, lift))}
                reconstructed.append([colors[v] for v in sorted(vertices)])
        assert sorted(reconstructed) == full
        rows.append({"row_index": index, "literal_beta": beta,
                     "full_same_pin_join_fibres": joined,
                     "full_global_lifts": full})
    by_beta = {tuple(row["literal_beta"]): row for row in rows}
    return {"reference": reference, "original_interior_coordinates": sorted(vertices),
            "nonroot_tuple_order": nonroots, "ordered_roots": roots,
            "original_edges": sorted(map(list, edges)),
            "original_root_degrees": [sum(r in edge for edge in edges) for r in roots],
            "piece_references": [piece["reference"] for piece in pieces],
            "union_of_piece_diagonal_masks": sorted({label for piece in pieces
                                                      for label in piece["diagonal_rejection_mask"]}),
            "full_graph_diagonal_rejection_mask": [label for label, beta in QS.items()
                         if not by_beta[tuple(beta)]["full_same_pin_join_fibres"][15]],
            "rows": rows}


def motif_tables(table):
    """Exhaust all literal attachments of seven named fixed block motifs."""
    specs = [
        ("bridge_two_contacts", [[7, 8]], [7, 8], [2, 2]),
        ("path_three_contacts", [[7, 8], [8, 9]], [7, 8, 9], [2, 1, 2]),
        ("triangle_three_contacts", [[7, 8], [7, 9], [8, 9]], [7, 8, 9], [1, 1, 1]),
        ("triangle_one_bridge_three_contacts",
         [[7, 8], [7, 9], [8, 9], [7, 10]], [8, 9, 10], [1, 1, 1, 2]),
        ("triangle_two_bridge_tail_three_contacts",
         [[7, 8], [7, 9], [8, 9], [7, 10], [10, 11]],
         [8, 9, 11], [1, 1, 1, 2, 2]),
        ("two_triangles_one_bridge_three_contacts",
         [[7, 8], [7, 9], [8, 9], [9, 10], [9, 11], [10, 11], [10, 12]],
         [7, 8, 12], [1, 1, 0, 1, 2, 2]),
        ("three_bridge_star_three_contacts",
         [[7, 8], [7, 9], [7, 10]], [8, 9, 10], [1, 2, 2, 2]),
    ]
    tables, exemplars = [], {}
    for name, internal, contacts, attachment_sizes in specs:
        vertices = sorted({v for edge in internal for v in edge})
        assert len(vertices) == len(attachment_sizes)
        degree_two = [v for v in vertices
                      if sum(v in edge for edge in internal) + (v in contacts) == 2]
        choices = [BEDGES if size == 2 else [(b,) for b in range(5)]
                   if size == 1 else [()] for size in attachment_sizes]
        entries = []
        for attachment in product(*choices):
            boundary = dict(zip(vertices, attachment))
            if len({tuple(sorted(boundary[v])) for v in degree_two}) != len(degree_two):
                continue
            support = {b for actual in attachment for b in actual}
            starts = [start for start in range(5)
                      if support == {(start + j) % 5 for j in range(3)}]
            if not starts:
                continue
            # Splitting owners leaves the D,D lists unchanged. Preserve one
            # literal mixed splitting, including its complete off-diagonal relation.
            region = edgeset(internal + [[5, contacts[0]]]
                             + [[6, v] for v in contacts[1:]]
                             + [[v, b] for v in vertices for b in boundary[v]])
            diagonal = {label: assignments(vertices, region,
                         {**dict(enumerate(beta)), 5: 3, 6: 3})
                        for label, beta in QS.items()}
            mask = [label for label, lifts in diagonal.items() if not lifts]
            assert mask != list(QS)
            record = {"arc_start": starts[0], "actual_boundary_attachments":
                      [[v, list(boundary[v])] for v in vertices],
                      "diagonal_rejection_mask": mask,
                      "all_complete_diagonal_lifts": diagonal}
            entries.append(record)
            key = (name, starts[0], tuple(mask))
            if key not in exemplars:
                full = piece_record(vertices, region, [5, 6], table,
                                    f"bounded_motif/{name}/arc_{starts[0]}/mask_{mask}")
                full["motif_name"] = name
                full["control_status"] = "triggered and holds"
                full["target_source_status"] = "not triggered"
                assert full["diagonal_rejection_mask"] == mask
                exemplars[key] = full
        tables.append({"name": name, "original_internal_edges": internal,
                       "ordered_vertices": vertices,
                       "contact_vertices": contacts,
                       "H_degree_two_vertices": degree_two,
                       "all_attachment_candidates": len(list(product(*choices))),
                       "retained_exact_two_edge_support_controls": len(entries),
                       "entries": entries,
                       "control_status": "triggered and holds" if entries else "not triggered",
                       "source_generation_status": "fixed named local motifs only"})
    signatures = []
    for (name, start, mask), item in sorted(exemplars.items()):
        signatures.append({"motif_name": name, "arc_start": start,
                           "literal_arc_edges": item["exact_two_edge_support_arcs"][0]["literal_boundary_edges"],
                           "mask": list(mask), "full_fibre_reference": item["reference"]})
    pair_controls = []
    for first, second in product(signatures, repeat=2):
        if set(map(tuple, first["literal_arc_edges"])) & set(map(tuple, second["literal_arc_edges"])):
            continue
        union = sorted(set(first["mask"]) | set(second["mask"]))
        pair_controls.append({"first": first, "second": second, "mask_union": union,
                              "same_row_diagonal_escape": [label for label in QS if label not in union],
                              "control_status": "triggered and holds" if union != list(QS) else "counterexample",
                              "scope": "bounded local synchrony only; no source realization"})
    return tables, list(exemplars.values()), pair_controls


def connected(bag, edges):
    seen = {min(bag)}
    while True:
        extra = {b for a, b in edges if a in seen and b in bag} | {
            a for a, b in edges if b in seen and a in bag}
        if extra <= seen:
            return seen == set(bag)
        seen |= extra


def named_joint_controls(table, exemplars):
    first = next(item for item in exemplars
                 if item["motif_name"] == "path_three_contacts"
                 and item["exact_two_edge_support_arcs"][0]["start"] == 0
                 and item["diagonal_rejection_mask"] == [0, 1])
    second_original = next(item for item in exemplars
                 if item["motif_name"] == "path_three_contacts"
                 and item["exact_two_edge_support_arcs"][0]["start"] == 2
                 and item["diagonal_rejection_mask"] == [3])
    # Change owners in the second whole local graph, without normalizing its
    # boundary frame; both original roots then have three local incidences.
    transform = {5: 6, 6: 5, 7: 11, 8: 12, 9: 13}
    second_edges = [[transform.get(a, a), transform.get(b, b)]
                    for a, b in second_original["original_region_edges"]]
    second = piece_record([11, 12, 13], second_edges, [5, 6], table,
                          "named_joint/second_path_literal_frame")
    first = piece_record(first["original_vertices"], first["original_region_edges"],
                         [5, 6], table, "named_joint/first_path_literal_frame")
    region = edgeset(first["original_region_edges"] + second["original_region_edges"])
    original_edges = region | set(BEDGES)
    negative = graph_record([5, 6, 7, 8, 9, 11, 12, 13], original_edges, [5, 6],
                            [first, second], table, "negative_separate_path_escapes")
    assert negative["union_of_piece_diagonal_masks"] == list(QS)
    negative["control_status"] = "counterexample"
    negative["meaning"] = "Two separate local three-row escapes need not share a row."
    negative["target_source_status"] = "not triggered"
    # Restore original degree-five roots by the four literal common spokes.
    # The uncontracted bags exhibit why this local synchrony obstruction is
    # incompatible with disk planarity under the additional common-spoke premise.
    k5_edges = original_edges | {(0, 5), (4, 5), (0, 6), (4, 6)}
    k5 = graph_record([5, 6, 7, 8, 9, 11, 12, 13], k5_edges, [5, 6],
                      [first, second], table, "common_complement_edge_spokes_K5")
    bags = [[5, 11, 12, 13], [6], [0], [4], [1, 2, 3, 7, 8, 9]]
    assert len({v for bag in bags for v in bag}) == sum(map(len, bags))
    assert all(connected(bag, k5_edges) for bag in bags)
    witnesses = []
    for i in range(5):
        for j in range(i + 1, 5):
            cross = sorted([list(edge) for edge in k5_edges
                            if (edge[0] in bags[i] and edge[1] in bags[j])
                            or (edge[1] in bags[i] and edge[0] in bags[j])])
            assert cross
            witnesses.append({"bag_pair": [i, j], "original_cross_edges": cross})
    assert k5["original_root_degrees"] == [5, 5]
    k5.update({"uncontracted_K5_branch_bags": bags,
               "original_bag_adjacency_witnesses": witnesses,
               "control_status": "triggered and holds",
               "target_source_status": "not triggered",
               "meaning": "Named local degree-five control with a literal K5 minor; not a disk source."})
    return {"pieces": [first, second], "graphs": [negative, k5]}


def generate():
    base = json.loads((AUDIT / "BASE.json").read_bytes())
    source = next(item for item in base["inputs"] if item["path"] == SOURCE)
    raw = (AUDIT / "frozen" / (SOURCE + ".snapshot")).read_bytes()
    assert len(raw) == source["bytes"] and sha256(raw).hexdigest() == source["sha256"]
    frozen = json.loads(raw)
    assert frozen["target_source_status"] == "not triggered"
    table = [row["beta"] for row in frozen["records"][0]["components"][0]["rows"]]
    assert len(table) == 10 and len({tuple(beta) for beta in table}) == 10
    source_row_map = {label: table.index(beta) for label, beta in QS.items()}
    records, graphs = [], []
    outside_checks = 0
    for gindex, graph in enumerate(frozen["records"]):
        pieces = []
        for cindex, original in enumerate(graph["components"]):
            item = piece_record(original["vertices"], original["edges"], graph["roots"],
                                table, f"/records/{gindex}/components/{cindex}")
            assert item["root_incidences"] == original["root_incidence"]
            for index, row in enumerate(original["rows"]):
                assert row["beta"] == table[index]
                assert item["rows"][index]["full_local_fibres_by_ordered_pins"] == row["local_full_fibres_by_pins"]
                outside_vertices = original["outside_coordinates"]
                outside_edges = {edge for edge in edgeset(graph["edges"])
                                 if not set(edge) & set(original["vertices"])}
                assert assignments(outside_vertices, outside_edges,
                                   dict(enumerate(table[index]))) == row["outside_full_lifts"]
                outside_checks += 1
            item["frozen_source_graph_reference"] = f"/records/{gindex}"
            item["frozen_source_sigma_mask"] = graph["sigma_mask"]
            pieces.append(item)
            records.append(item)
        full = graph_record(graph["interior_coordinates"], graph["edges"], graph["roots"],
                            pieces, table, f"/records/{gindex}")
        for piece in graph["components"]:
            for index, row in enumerate(piece["rows"]):
                source_encoded = (json.dumps(full["rows"][index]["full_global_lifts"],
                                   sort_keys=True, separators=(",", ":")) + "\n").encode()
                assert sha256(source_encoded).hexdigest() == row["global_full_lifts_sha256"]
        full["frozen_source_sigma_mask"] = graph["sigma_mask"]
        full["long_mixed_piece_references"] = [item["reference"] for item in pieces
                                              if item["long_support"] and all(item["root_incidences"])]
        full["target_source_status"] = "not triggered"
        graphs.append(full)
    motifs, examples, pair_controls = motif_tables(table)
    named = named_joint_controls(table, examples)
    longs = [item for item in records if item["long_support"] and all(item["root_incidences"])]
    histogram = Counter((sum(item["root_incidences"]),
                         bool(item["literal_shared_contacts"]),
                         tuple(item["diagonal_rejection_mask"])) for item in longs)
    counts = {"frozen_graphs": len(graphs), "frozen_components": len(records),
              "complete_local_rows": len(records) * 10,
              "complete_local_ordered_pin_cells": len(records) * 160,
              "empty_local_cells": sum(not cell for item in records for row in item["rows"]
                                       for cell in row["full_local_fibres_by_ordered_pins"]),
              "same_graph_join_cells": len(graphs) * 160,
              "complete_outside_checks": outside_checks,
              "long_mixed_pieces": len(longs),
              "shared_contact_long_mixed": sum(bool(item["literal_shared_contacts"]) for item in longs),
              "long_support_at_least_three_k_at_most_three": sum(
                  len(item["actual_support"]) >= 3 and sum(item["root_incidences"]) <= 3
                  for item in longs),
              "two_long_mixed_same_graph_controls": sum(len(graph["long_mixed_piece_references"]) >= 2 for graph in graphs),
              "named_fixed_motifs": len(motifs),
              "bounded_exact_arc_attachment_controls": sum(len(item["entries"]) for item in motifs),
              "all_160_cell_motif_exemplars": len(examples),
              "bounded_disjoint_arc_signature_pairs": len(pair_controls),
              "bounded_pairs_without_common_diagonal_row": sum(not pair["same_row_diagonal_escape"] for pair in pair_controls),
              "complete_target_sources": 0}
    return {"scope": "Frozen original graphs and explicitly bounded local motifs; no target source search",
            "frozen_source": source, "target_source_status": "not triggered",
            "ordered_pin_order": PINS, "literal_boundary_table": table,
            "named_target_rows": QS, "target_label_to_frozen_row_index": source_row_map,
            "counts": counts, "frozen_piece_records": records,
            "frozen_same_graph_records": graphs,
            "long_mixed_mask_histogram": [
                {"root_incidences_total": k, "has_literal_shared_contact": shared,
                 "mask": list(mask), "count": count}
                for (k, shared, mask), count in sorted(histogram.items())],
            "bounded_motif_signature_tables": motifs,
            "bounded_motif_full_fibre_exemplars": examples,
            "bounded_disjoint_arc_signature_pairs": pair_controls,
            "named_joint_and_K5_controls": named}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--artifact", type=Path, default=HERE / "observations.json")
    args = parser.parse_args()
    value = generate()
    data = encoded(value)
    if args.write:
        with args.artifact.open("xb") as handle:
            handle.write(data)
    elif args.artifact.read_bytes() != data:
        raise SystemExit("artifact mismatch")
    print(json.dumps({"mode": "write" if args.write else "check", "bytes": len(data),
                      "sha256": sha256(data).hexdigest(), "counts": value["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
