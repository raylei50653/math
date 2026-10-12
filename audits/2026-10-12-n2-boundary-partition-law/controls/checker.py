#!/usr/bin/env python3
"""Fixed saved-piece boundary-partition fibre controls; no source enumeration.

Cell maps reference complete frozen tuples rather than copying them.  Each
representative-to-cell map is one permutation of all four colours, checked on
the entire ordered tuple relation, including empty relations.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
CONTROLS = "audits/2026-10-11-n2-long-mask-sync/controls/observations.json"
SLACK = "artifacts/c5_excess_two_arc_component_slack/observations.json"
HIGH = "audits/2026-10-11-n2-long-mask-sync/high-contact/observations.json"
PINS = list(product(range(4), repeat=2))
PERMS = list(permutations(range(4)))
BEDGES = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
QS = {0: [0, 1, 2, 1, 2], 1: [0, 1, 2, 0, 2], 3: [0, 1, 0, 2, 1]}


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def digest(value):
    return sha256(encoded(value)).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def partition(colors):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in colors)


def edgeset(edges):
    answer = {tuple(sorted(e)) for e in edges}
    require(all(a != b for a, b in answer), "loop in original edges")
    require(len(answer) == len(edges), "duplicate original edge")
    return answer


def assignments(vertices, edges, fixed):
    """Independent exhaustive DFS of one saved original graph or piece."""
    vertices = list(vertices)
    require(len(vertices) == len(set(vertices)), "duplicate tuple vertex")
    require(not set(vertices) & set(fixed), "fixed and tuple vertices overlap")
    adjacency = {v: set() for v in set(vertices) | set(fixed)}
    for a, b in edges:
        require(a in adjacency and b in adjacency, "unknown edge endpoint")
        adjacency[a].add(b)
        adjacency[b].add(a)
    if any(a in fixed and b in fixed and fixed[a] == fixed[b] for a, b in edges):
        return []
    colors = dict(fixed)
    answer = []

    def visit(index):
        if index == len(vertices):
            answer.append([colors[v] for v in vertices])
            return
        vertex = vertices[index]
        forbidden = {colors[v] for v in adjacency[vertex] if v in colors}
        for color in range(4):
            if color not in forbidden:
                colors[vertex] = color
                visit(index + 1)
        colors.pop(vertex, None)

    visit(0)
    return answer


def frozen_inputs():
    base_bytes = (AUDIT / "BASE.json").read_bytes()
    base = json.loads(base_bytes)
    verified = []
    datasets = {}
    for entry in base["inputs"]:
        snapshot = AUDIT / "frozen" / (entry["path"] + ".snapshot")
        raw = snapshot.read_bytes()
        require(len(raw) == entry["bytes"], "BASE input byte size mismatch: " + entry["path"])
        require(sha256(raw).hexdigest() == entry["sha256"], "BASE input hash mismatch: " + entry["path"])
        verified.append({**entry, "snapshot": str(snapshot.relative_to(AUDIT))})
        if entry["path"] in {CONTROLS, SLACK, HIGH}:
            datasets[entry["path"]] = json.loads(raw)
    require(len(verified) == 12, "unexpected frozen BASE input coverage")
    return base, sha256(base_bytes).hexdigest(), verified, datasets


def adapt_piece(raw, source, pointer):
    high = source == HIGH
    roots = raw["ordered_roots"]
    vertices = raw["original_vertices"]
    all_edges = edgeset(raw["original_edges"] if high else raw["original_region_edges"])
    # The high-contact snapshot supplies the original complete graph including
    # boundary edges.  The local fibre owns precisely edges incident with C.
    region = {e for e in all_edges if set(e) & set(vertices)}
    support = sorted({b for a, b in region if b in range(5)} |
                     {a for a, b in region if a in range(5)})
    contacts = [[v for v in vertices if tuple(sorted((r, v))) in region] for r in roots]
    attachments = [[v, [b for b in range(5) if tuple(sorted((b, v))) in region]] for v in vertices]
    require(support == raw["actual_support"], "actual support drift")
    require(contacts == raw["ordered_original_contacts" if high else "ordered_root_contacts"], "contact ownership drift")
    supplied = ([[int(v), raw["actual_attachments"][v]] for v in sorted(raw["actual_attachments"], key=int)]
                if high else raw["actual_boundary_attachments"])
    require(attachments == supplied, "actual attachment drift")
    rows = []
    for row_index, row in enumerate(raw["rows"]):
        rows.append({"beta": row["beta" if high else "literal_beta"],
                     "fibres": row["full_lifts_by_ordered_pins" if high else "full_local_fibres_by_ordered_pins"]})
        require(len(rows[-1]["fibres"]) == 16, "incomplete ordered pin cells")
        if not high:
            require(row["row_index"] == row_index, "row index drift")
    require(len(rows) == 10, "incomplete boundary row table")
    return {"reference": raw.get("reference", raw.get("name")), "source": source,
            "pointer": pointer, "vertices": vertices, "roots": roots,
            "edges": sorted(map(list, region)), "support": support,
            "contacts": contacts, "attachments": attachments, "rows": rows,
            "supplied_mask": raw["diagonal_rejection_mask"]}


def saved_pieces(datasets):
    source = datasets[CONTROLS]
    require(source["ordered_pin_order"] == list(map(list, PINS)), "pin order drift")
    pieces = []
    for key in ["frozen_piece_records", "bounded_motif_full_fibre_exemplars"]:
        for i, raw in enumerate(source[key]):
            pieces.append(adapt_piece(raw, CONTROLS, f"/{key}/{i}"))
    for i, raw in enumerate(source["named_joint_and_K5_controls"]["pieces"]):
        pieces.append(adapt_piece(raw, CONTROLS, f"/named_joint_and_K5_controls/pieces/{i}"))
    for i, raw in enumerate(datasets[HIGH]["named_full_fibre_controls"]):
        pieces.append(adapt_piece(raw, HIGH, f"/named_full_fibre_controls/{i}"))
    require(len(pieces) == 228, "saved-piece coverage drift")
    return pieces


def cell(piece, index):
    row, pin = divmod(index, 16)
    return piece["rows"][row]["fibres"][pin]


def interface(piece, index):
    row, pin = divmod(index, 16)
    beta = piece["rows"][row]["beta"]
    return [beta[b] for b in piece["support"]] + list(PINS[pin])


def image_fibre(fibre, permutation):
    return sorted([[permutation[c] for c in lift] for lift in fibre])


def verify_fibre_image(source, target, permutation, message):
    transported = image_fibre(source, permutation)
    require(transported == target, message)
    return transported


def piece_observation(piece, counts):
    edges = edgeset(piece["edges"])
    complete_degree_four = all(sum(v in e for e in edges) == 4 for v in piece["vertices"])
    internal_adjacency = {v: set() for v in piece["vertices"]}
    for a, b in edges:
        if a in internal_adjacency and b in internal_adjacency:
            internal_adjacency[a].add(b)
            internal_adjacency[b].add(a)
    reached = {piece["vertices"][0]}
    todo = list(reached)
    while todo:
        for vertex in internal_adjacency[todo.pop()] - reached:
            reached.add(vertex)
            todo.append(vertex)
    require(reached == set(piece["vertices"]), "saved local piece is disconnected")
    representatives = {}
    classes = []
    cell_maps = []
    collision_cells = []
    for index in range(160):
        row_index, pin_index = divmod(index, 16)
        row = piece["rows"][row_index]
        fibre = cell(piece, index)
        fixed = {**dict(enumerate(row["beta"])), **dict(zip(piece["roots"], PINS[pin_index]))}
        require(assignments(piece["vertices"], edges, fixed) == fibre,
                f"independent full local DFS mismatch: {piece['reference']} cell {index}")
        counts["independent_local_dfs_cells"] += 1
        counts["complete_local_tuples_checked"] += len(fibre)
        counts["empty_local_cells"] += not fibre
        collision = None
        for vertex in piece["vertices"]:
            external = sorted(w for e in edges if vertex in e for w in e
                              if w != vertex and w in fixed)
            for i, first in enumerate(external):
                for second in external[i + 1:]:
                    if fixed[first] == fixed[second]:
                        collision = [index, vertex, first, second, fixed[first]]
                        break
                if collision:
                    break
            if collision:
                break
        if complete_degree_four:
            if collision:
                require(bool(fibre), "complete degree-four external colour collision has empty fibre")
                counts["external_colour_collision_triggered_and_holds"] += 1
                collision_cells.append(collision)
            else:
                counts["external_colour_collision_not_triggered"] += 1
                counts["external_colour_collision_not_triggered_empty"] += not fibre
        else:
            counts["external_colour_collision_degree_hypothesis_not_applicable"] += 1
        key = partition(interface(piece, index))
        if key not in representatives:
            representatives[key] = index
            classes.append({"partition": list(key), "representative_cell": index, "members": []})
        representative = representatives[key]
        next(c for c in classes if c["representative_cell"] == representative)["members"].append(index)
        left, right = interface(piece, representative), interface(piece, index)
        permutation_index = next(i for i, perm in enumerate(PERMS) if [perm[c] for c in left] == right)
        transported = verify_fibre_image(cell(piece, representative), fibre, PERMS[permutation_index],
                                         f"complete tuple bijection mismatch: {piece['reference']} cell {index}")
        counts["complete_tuple_bijections"] += 1
        counts["nonidentity_permutation_maps"] += permutation_index != 0
        # Map columns: target cell, representative cell, permutation index,
        # complete relation size, SHA256 of complete transported relation.
        cell_maps.append([index, representative, permutation_index, len(fibre), digest(transported)])
    by_beta = {tuple(row["beta"]): row for row in piece["rows"]}
    mask = [q for q, beta in QS.items() if not by_beta[tuple(beta)]["fibres"][15]]
    require(mask == piece["supplied_mask"], "frozen diagonal mask drift")
    arcs = []
    for start in range(5):
        points = [(start + j) % 5 for j in range(3)]
        if set(piece["support"]) <= set(points):
            eq = [q for q, beta in QS.items() if beta[points[0]] == beta[points[2]]]
            diff = [q for q in QS if q not in eq]
            possibilities = {(): "empty", tuple(eq): "Eq", tuple(diff): "Diff", tuple(QS): "I"}
            require(tuple(mask) in possibilities, "three-arc orbit law failed")
            full_arc_groups = {}
            collision_indices = {c[0] for c in collision_cells}
            for index in range(160):
                row_index, pin_index = divmod(index, 16)
                beta = piece["rows"][row_index]["beta"]
                key = partition([beta[v] for v in points] + list(PINS[pin_index]))
                full_arc_groups.setdefault(key, set()).add(index in collision_indices)
            require(len(full_arc_groups) == 26 and all(len(v) == 1 for v in full_arc_groups.values()),
                    "full-arc collision filter fails to preserve interface partitions")
            filtered = [list(k) for k, v in sorted(full_arc_groups.items()) if next(iter(v))]
            residual = [list(k) for k, v in sorted(full_arc_groups.items()) if not next(iter(v))]
            counts["three_arc_full_partition_classes"] += 26
            counts["collision_filtered_three_arc_interface_classes"] += len(filtered)
            counts["residual_three_arc_interface_classes"] += len(residual)
            arcs.append({"ordered_arc": points, "Eq": eq, "Diff": diff, "mask_type": possibilities[tuple(mask)],
                         "full_arc_pin_cells": 160, "full_arc_interface_partition_count": 26,
                         "collision_filtered_partitions": filtered, "residual_interface_partitions": residual})
            counts["three_arc_mask_checks"] += 1
    counts["interface_partition_classes"] += len(classes)
    collision_index_set = {c[0] for c in collision_cells}
    for group in classes:
        statuses = {i in collision_index_set for i in group["members"]}
        require(len(statuses) == 1, "collision status is not an interface partition invariant")
        group["external_colour_collision"] = bool(next(iter(statuses)))
    counts["collision_interface_partition_classes"] += sum(c["external_colour_collision"] for c in classes)
    return {"reference": piece["reference"], "source": piece["source"], "source_pointer": piece["pointer"],
            "ordered_original_vertices": piece["vertices"], "ordered_roots": piece["roots"],
            "original_region_edges": piece["edges"], "actual_support": piece["support"],
            "interface_order": piece["support"] + piece["roots"],
            "actual_boundary_attachments": piece["attachments"], "ordered_root_contacts": piece["contacts"],
            "partition_classes": classes, "cell_maps": cell_maps,
            "complete_degree_four": complete_degree_four,
            "external_colour_collision_columns": ["cell_index", "original_C_vertex", "first_actual_external_neighbour", "second_actual_external_neighbour", "common_fixed_colour"],
            "external_colour_collision_cells": collision_cells,
            "external_colour_collision_status": "triggered and holds" if collision_cells else "not triggered",
            "diagonal_rejection_mask": mask, "three_arc_incidences": arcs}


def graph_observations(datasets, pieces, counts):
    source = datasets[CONTROLS]
    by_ref = {p["reference"]: p for p in pieces if p["source"] == CONTROLS}
    graphs = [(g, f"/frozen_same_graph_records/{i}") for i, g in enumerate(source["frozen_same_graph_records"])]
    graphs += [(g, f"/named_joint_and_K5_controls/graphs/{i}") for i, g in enumerate(source["named_joint_and_K5_controls"]["graphs"])]
    observations = []
    for graph, pointer in graphs:
        edges = edgeset(graph["original_edges"])
        vertices = graph["nonroot_tuple_order"]
        roots = graph["ordered_roots"]
        owned = [by_ref[r] for r in graph["piece_references"]]
        require(sum(len(p["vertices"]) for p in owned) == len(vertices), "piece overlap or missing graph vertices")
        require(set(vertices) == {v for p in owned for v in p["vertices"]}, "tuple ownership drift")
        region_union = set().union(*(edgeset(p["edges"]) for p in owned))
        external = {e for e in edges if not set(e) & set(vertices)}
        require(edges == region_union | external, "cross-piece original edge is missing")
        row_checks = []
        for row_index, row in enumerate(graph["rows"]):
            beta = row["literal_beta"]
            joined_cells = []
            for pin_index, pin in enumerate(PINS):
                fixed = {**dict(enumerate(beta)), **dict(zip(roots, pin))}
                local_cells = []
                for p in owned:
                    require(p["rows"][row_index]["beta"] == beta, "independent normalized component row attempted")
                    require(p["roots"] == roots, "ordered root mismatch")
                    local_cells.append(cell(p, row_index * 16 + pin_index))
                joined = []
                if not any(fixed[a] == fixed[b] for a, b in external):
                    for lifts in product(*local_cells):
                        colors = {}
                        for p, lift in zip(owned, lifts):
                            colors.update(zip(p["vertices"], lift))
                        joined.append([colors[v] for v in vertices])
                joined.sort()
                require(joined == row["full_same_pin_join_fibres"][pin_index], "saved same-row same-pin full join mismatch")
                require(joined == assignments(vertices, edges, fixed), "independent full graph DFS mismatch")
                joined_cells.append(joined)
                counts["same_row_same_pin_full_join_cells"] += 1
                counts["empty_full_join_cells"] += not joined
            global_order = graph["original_interior_coordinates"]
            direct = assignments(global_order, edges, dict(enumerate(beta)))
            reconstructed = []
            for pin, lifts in zip(PINS, joined_cells):
                for lift in lifts:
                    colors = {**dict(zip(roots, pin)), **dict(zip(vertices, lift))}
                    reconstructed.append([colors[v] for v in global_order])
            reconstructed.sort()
            require(reconstructed == direct == row["full_global_lifts"], "complete global lift reconstruction mismatch")
            counts["complete_global_rows"] += 1
            row_checks.append({"row_index": row_index, "literal_beta": beta,
                               "full_join_cell_sha256": [digest(c) for c in joined_cells],
                               "full_global_lifts_count": len(direct), "full_global_lifts_sha256": digest(direct)})
        observations.append({"reference": graph["reference"], "source": CONTROLS, "source_pointer": pointer,
                             "piece_references": graph["piece_references"], "ordered_roots": roots,
                             "nonroot_tuple_order": vertices, "original_interior_coordinates": graph["original_interior_coordinates"],
                             "original_edges": graph["original_edges"], "rows": row_checks,
                             "full_graph_diagonal_rejection_mask": graph["full_graph_diagonal_rejection_mask"],
                             "union_of_piece_diagonal_masks": graph["union_of_piece_diagonal_masks"]})
    return observations


def source_custody(datasets, pieces, counts):
    originals = [p for p in pieces if p["pointer"].startswith("/frozen_piece_records/")]
    require(len(originals) == 179, "original piece coverage drift")
    controls = datasets[CONTROLS]
    for piece in originals:
        indices = [int(t) for t in piece["reference"].split("/") if t.isdigit()]
        record = datasets[SLACK]["records"][indices[0]]
        component = record["components"][indices[1]]
        require(piece["vertices"] == component["vertices"], "original component vertex drift")
        require(piece["edges"] == sorted(map(list, edgeset(component["edges"]))), "original component edge drift")
        require(piece["roots"] == record["roots"], "original root ownership drift")
        graph = controls["frozen_same_graph_records"][indices[0]]
        require(graph["original_edges"] == record["edges"], "original graph edge drift")
        require(graph["original_interior_coordinates"] == record["interior_coordinates"], "original graph coordinate drift")
        for row_index, row in enumerate(component["rows"]):
            require(piece["rows"][row_index]["beta"] == row["beta"], "source row identity drift")
            require(piece["rows"][row_index]["fibres"] == row["local_full_fibres_by_pins"], "original source full fibre mismatch")
            source_raw = (json.dumps(graph["rows"][row_index]["full_global_lifts"], sort_keys=True,
                                     separators=(",", ":")) + "\n").encode()
            require(sha256(source_raw).hexdigest() == row["global_full_lifts_sha256"], "original source global full lift hash mismatch")
            counts["original_source_piece_rows_checked"] += 1


def boundary_geometry(table):
    partition_controls = []
    for start in range(5):
        arc = [(start + j) % 5 for j in range(3)]
        classes = {}
        for row_index, beta in enumerate(table):
            for pin_index, pin in enumerate(PINS):
                key = partition([beta[b] for b in arc] + list(pin))
                classes.setdefault(key, []).append([row_index, pin_index])
        require(len(classes) == 26, "ordered five-point interface partition count drift")
        eq_count = sum(key[0] == key[2] for key in classes)
        require(eq_count == 10, "equal-endpoint partition count drift")
        partition_controls.append({"ordered_arc": arc, "ordered_interface_roles": ["a", "b", "c", "r", "s"],
                                   "ambient_cells": 160, "classes": [{"partition": list(k), "members": v} for k, v in sorted(classes.items())],
                                   "equality_classes": 10, "distinct_endpoint_classes": 16})
    proper4 = [list(b) for b in product(range(4), repeat=5) if all(b[a] != b[c] for a, c in BEDGES)]
    proper3 = [b for b in proper4 if set(b) <= {0, 1, 2}]
    require(len(proper4) == 240 and len(proper3) == 30, "proper boundary table count drift")
    geometries = []
    for start in range(5):
        a, b, h, c, d = [(start + j) % 5 for j in range(5)]
        first, second = [a, b, h], [h, c, d]
        require(all(not (beta[a] == beta[h] and beta[h] == beta[d]) for beta in proper4), "Eq/Eq impossible geometry failed")
        eq_first = [q for q, beta in QS.items() if beta[a] == beta[h]]
        eq_second = [q for q, beta in QS.items() if beta[h] == beta[d]]
        require(not set(eq_first) & set(eq_second), "same-row Eq/Eq intersection is nonempty")
        require(eq_first and eq_second, "target rows lack mixed escape")
        diff_first = [q for q in QS if q not in eq_first]
        diff_second = [q for q in QS if q not in eq_second]
        require(set(diff_first) | set(diff_second) == set(QS), "Diff/Diff target diagonal obstruction failed")
        require(all(beta[a] != beta[h] or beta[h] != beta[d] for beta in proper3), "Diff/Diff all proper three-colour obstruction failed")
        geometries.append({"ordered_cycle": [a, b, h, c, d], "A": first, "B": second,
                           "remaining_original_edge": sorted([d, a]), "all_proper_four_colour_rows_checked": 240,
                           "all_proper_three_colour_rows_checked": 30, "EqA": eq_first, "EqB": eq_second,
                           "EqA_intersection_EqB": [], "DiffA": diff_first, "DiffB": diff_second,
                           "EqA_DiffB_escape_rows": eq_second, "DiffA_EqB_escape_rows": eq_first,
                           "DiffA_DiffB_rejects_all_target_rows": True,
                           "DiffA_DiffB_rejects_all_proper_three_colour_rows_with_spare_D": True})
    return {"ordered_three_arc_interface_classes": partition_controls,
            "proper_four_colour_boundary_rows": proper4, "proper_three_colour_boundary_rows": proper3,
            "edge_disjoint_two_arc_geometries": geometries}


def validate_map_artifact(artifact, pieces):
    records = artifact.get("pieces", [])
    require(len(records) == len(pieces), "artifact saved-piece coverage mismatch")
    for observed, piece in zip(records, pieces):
        require(observed["source_pointer"] == piece["pointer"], "artifact source pointer drift")
        maps = observed["cell_maps"]
        require(len(maps) == 160, "artifact must contain all 160 cells including empties")
        for expected_index, mapping in enumerate(maps):
            require(len(mapping) == 5, "artifact cell map schema mismatch")
            index, representative, permutation_index, relation_size, relation_hash = mapping
            require(index == expected_index and 0 <= representative < 160, "artifact cell coverage or representative mismatch")
            require(0 <= permutation_index < 24, "artifact permutation is invalid")
            left, right = interface(piece, representative), interface(piece, index)
            require(partition(left) == partition(right), "artifact representative partition mismatch")
            perm = PERMS[permutation_index]
            require([perm[c] for c in left] == right, "artifact interface permutation mismatch")
            transported = verify_fibre_image(cell(piece, representative), cell(piece, index), perm,
                                             "artifact complete full tuple bijection mismatch")
            require(relation_size == len(transported), "artifact full relation size mismatch")
            require(relation_hash == digest(transported), "artifact complete transported relation hash mismatch")


def negative_controls(observation, pieces):
    results = []
    # Corrupt a stored nonempty relation digest.  Tuple counts stay unchanged.
    corrupted = deepcopy(observation)
    pi, ci = next((pi, ci) for pi, p in enumerate(corrupted["pieces"]) for ci, m in enumerate(p["cell_maps"]) if m[3])
    old = corrupted["pieces"][pi]["cell_maps"][ci][4]
    corrupted["pieces"][pi]["cell_maps"][ci][4] = ("0" if old[0] != "0" else "1") + old[1:]
    cases = [("corrupted_complete_fibre_digest_preserving_tuple_count", corrupted, pi, ci)]
    # Dropping an empty cell may silently alter rejection if omitted cells are
    # interpreted as unobserved, so complete coverage is an explicit gate.
    corrupted = deepcopy(observation)
    pi, ci = next((pi, ci) for pi, p in enumerate(corrupted["pieces"]) for ci, m in enumerate(p["cell_maps"]) if not m[3])
    del corrupted["pieces"][pi]["cell_maps"][ci]
    cases.append(("dropped_empty_cell", corrupted, pi, ci))
    corrupted = deepcopy(observation)
    pi, ci = next((pi, ci) for pi, p in enumerate(corrupted["pieces"]) for ci, m in enumerate(p["cell_maps"]) if m[2] != 0)
    corrupted["pieces"][pi]["cell_maps"][ci][2] = 0
    cases.append(("wrong_single_colour_permutation", corrupted, pi, ci))
    for name, corrupted, piece_index, cell_index in cases:
        try:
            validate_map_artifact(corrupted, pieces)
        except ValueError as error:
            results.append({"name": name, "piece_index": piece_index, "cell_index": cell_index,
                            "control_status": "counterexample", "corruption_rejected": True, "reason": str(error)})
        else:
            raise ValueError("negative control was accepted: " + name)
    # Independently mutate one complete tuple while preserving relation size,
    # demonstrating that actual tuple equality, rather than counts, is checked.
    pi, ci = next((pi, ci) for pi, p in enumerate(pieces) for ci in range(160) if cell(p, ci))
    original = cell(pieces[pi], ci)
    corrupted_fibre = deepcopy(original)
    corrupted_fibre[0][0] = (corrupted_fibre[0][0] + 1) % 4
    require(len(corrupted_fibre) == len(original) and corrupted_fibre != original, "negative tuple mutation failed")
    try:
        verify_fibre_image(original, sorted(corrupted_fibre), PERMS[0], "corrupted complete tuple relation mismatch")
    except ValueError as error:
        results.append({"name": "one_tuple_colour_changed_same_relation_size", "piece_index": pi, "cell_index": ci,
                        "control_status": "counterexample", "tuple_count_unchanged": True,
                        "corruption_rejected": True, "reason": str(error)})
    else:
        raise ValueError("same-size tuple corruption was accepted")
    return results


def build():
    base, base_hash, verified, datasets = frozen_inputs()
    pieces = saved_pieces(datasets)
    counts = Counter()
    source_custody(datasets, pieces, counts)
    observed_pieces = [piece_observation(p, counts) for p in pieces]
    observed_graphs = graph_observations(datasets, pieces, counts)
    geometry = boundary_geometry(datasets[CONTROLS]["literal_boundary_table"])
    counts.update({"saved_local_pieces": 228, "original_source_pieces": 179,
                   "saved_bounded_motif_exemplars": 45, "saved_named_joint_pieces": 2,
                   "saved_high_contact_pieces": 2, "same_original_graphs": 63,
                   "saved_named_joint_graphs": 2, "all_saved_graphs": 65,
                   "baseline_inputs_verified": len(verified), "proper_four_colour_boundary_rows": 240,
                   "proper_three_colour_boundary_rows": 30, "edge_disjoint_two_arc_geometries": 5,
                   "complete_target_sources": 0})
    counts["residual_interface_partition_classes"] = counts["interface_partition_classes"] - counts["collision_interface_partition_classes"]
    counts["external_colour_collision_degree_hypothesis_not_applicable"] += 0
    counts["saved_connected_complete_degree_four_pieces"] = sum(p["complete_degree_four"] for p in observed_pieces)
    residual_histogram = Counter(len(a["residual_interface_partitions"]) for p in observed_pieces for a in p["three_arc_incidences"])
    high_i = next(p for p in observed_pieces if p["reference"] == "four_contact_long_path")
    require(high_i["diagonal_rejection_mask"] == list(QS), "saved high-contact I witness missing")
    named_joint = next(g for g in observed_graphs if g["reference"] == "negative_separate_path_escapes")
    require(named_joint["full_graph_diagonal_rejection_mask"] == list(QS), "same-row synchrony negative control missing")
    observed = {"schema": "boundary-partition-full-fibre-v1", "frozen_head": base["head"],
                "BASE_sha256": base_hash, "verified_frozen_inputs": verified,
                "scope": "Only saved original pieces and full fibres; no new source graph or motif enumeration.",
                "target_source_status": "not triggered", "E_ARC2": "OPEN", "N2_55": "OPEN",
                "ordered_pin_order": list(map(list, PINS)), "colour_permutation_order": list(map(list, PERMS)),
                "cell_map_columns": ["target_cell_index", "representative_cell_index", "colour_permutation_index",
                                     "complete_tuple_relation_size", "complete_transported_tuple_relation_sha256"],
                "cell_index_formula": "16 * original_row_index + ordered_pin_index",
                "full_fibre_reference_rule": "source file SHA256 + source_pointer + original row and ordered pin; full ordered tuples retained in frozen snapshot",
                "counts": dict(sorted(counts.items())), "pieces": observed_pieces, "same_graph_full_joins": observed_graphs,
                "boundary_geometry": geometry,
                "three_arc_residual_partition_class_histogram": [{"residual_classes_after_collision_filter": k, "piece_arc_incidences": v}
                                                               for k, v in sorted(residual_histogram.items())],
                "high_contact_I_control": {"reference": high_i["reference"], "source_pointer": high_i["source_pointer"],
                                           "diagonal_rejection_mask": high_i["diagonal_rejection_mask"],
                                           "four_contact_mask_excluding_I": "counterexample"},
                "same_row_requirement_control": {"reference": named_joint["reference"], "source_pointer": named_joint["source_pointer"],
                                                 "full_graph_diagonal_rejection_mask": named_joint["full_graph_diagonal_rejection_mask"],
                                                 "independent_local_escape_implies_joint_escape": "counterexample"}}
    validate_map_artifact(observed, pieces)
    observed["negative_controls"] = negative_controls(observed, pieces)
    return observed, pieces


def verification_record(observed):
    return {"status": "PASS", "frozen_head": observed["frozen_head"],
            "BASE_sha256": observed["BASE_sha256"], "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "observations_sha256": digest(observed), "counts": observed["counts"],
            "negative_controls": observed["negative_controls"], "scope": observed["scope"],
            "target_source_status": "not triggered", "E_ARC2": "OPEN", "N2_55": "OPEN"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recalculate and verify saved deterministic observations")
    parser.add_argument("--artifact", type=Path, help="verify another observation artifact, including deliberate corruption")
    args = parser.parse_args()
    observed, pieces = build()
    if args.check or args.artifact:
        path = args.artifact or HERE / "observations.json"
        supplied = json.loads(path.read_bytes())
        validate_map_artifact(supplied, pieces)
        require(supplied == observed, "artifact differs from deterministic complete recalculation")
        if args.check and not args.artifact:
            require(json.loads((HERE / "verification.json").read_bytes()) == verification_record(observed),
                    "verification receipt differs from deterministic complete recalculation")
        print(json.dumps({"status": "PASS", "artifact": str(path), "counts": observed["counts"]}, sort_keys=True))
    else:
        (HERE / "observations.json").write_bytes(encoded(observed))
        verification = verification_record(observed)
        (HERE / "verification.json").write_bytes(encoded(verification))
        print(json.dumps(verification, sort_keys=True))


if __name__ == "__main__":
    main()
