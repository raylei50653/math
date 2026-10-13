#!/usr/bin/env python3
"""Independent reader: imports neither producer nor previous audit code."""
import argparse
import collections
import copy
import gzip
import hashlib
import itertools
import json
import pathlib
import random

HERE = pathlib.Path(__file__).resolve().parent


def normalize(row):
    colors = list(dict.fromkeys(row))
    return [colors.index(x) for x in row], colors


def cyclic_signature(row):
    return min(tuple(row[i:] + row[:i]) for i in range(len(row)))


def direct_tuples(edges, boundary, private, row):
    colors = dict(zip(boundary, row))
    boundary_edges, variable_edges = [], []
    for a, b in edges:
        (boundary_edges if a in colors and b in colors else variable_edges).append((a, b))
    if any(colors[a] == colors[b] for a, b in boundary_edges):
        return []
    tuples = []
    for assignment in itertools.product(range(4), repeat=len(private)):
        colors.update(zip(private, assignment))
        if all(colors[a] != colors[b] for a, b in variable_edges):
            tuples.append(list(assignment))
    return tuples


def partitions_by_assignments():
    # Independent Bell partition construction by merging each next vertex into
    # existing set blocks, and crossing checks against every pair of block chords.
    output = []
    def recurse(v, blocks):
        if v == 8:
            labels = [None] * 8
            chords = []
            for k, block in enumerate(blocks):
                for vertex in block:
                    labels[vertex] = k
                chords.extend((a, b, k) for a, b in itertools.combinations(block, 2))
            if any(labels[i] == labels[(i + 1) % 8] for i in range(8)):
                return
            for (a, c, ka), (b, d, kb) in itertools.combinations(chords, 2):
                if ka != kb and len({a, b, c, d}) == 4 and (a < b < c < d or b < a < d < c):
                    return
            output.append(labels)
            return
        for k in range(len(blocks)):
            next_blocks = [list(b) for b in blocks]
            next_blocks[k].append(v)
            recurse(v + 1, next_blocks)
        recurse(v + 1, blocks + [[v]])
    recurse(0, [])
    return sorted(output)


def embedded_faces(partition, chords):
    edges = {tuple(sorted((i, (i + 1) % 8))) for i in range(8)} | {tuple(e) for e in chords}
    neighbors = {v: sorted([b if a == v else a for a, b in edges if v in (a, b)],
                           key=lambda w: (w - v) % 8) for v in range(8)}
    used = set()
    faces = []
    for first in [(a, b) for edge in sorted(edges) for a, b in (edge, edge[::-1])]:
        if first in used:
            continue
        a, b = first
        face = []
        while (a, b) not in used:
            used.add((a, b))
            face.append(a)
            c = neighbors[b][(neighbors[b].index(a) - 1) % len(neighbors[b])]
            a, b = b, c
        assert (a, b) == first
        faces.append(face)
    assert len(used) == len(edges) * 2
    exterior = cyclic_signature(list(range(7, -1, -1)))
    interiors = [f for f in faces if cyclic_signature(f) != exterior]
    assert len(interiors) == len(faces) - 1
    cycles = []
    for face in interiors:
        labels = [partition[v] for v in face]
        cycle = [labels[j] for j in range(len(labels)) if labels[j] != labels[j - 1]]
        assert len(cycle) >= 2 and len(set(cycle)) == len(cycle)
        cycles.append(cycle)
    return interiors, cycles


def check(value, source, interface, queries):
    results = collections.Counter()
    part = value["partition_control"]
    assert sorted(row["partition"] for row in part["rows"]) == partitions_by_assignments()
    for row in part["rows"]:
        p = row["partition"]
        _, cycles = embedded_faces(p, row["fan_forest"])
        assert sorted(cyclic_signature(c) for c in cycles) == sorted(cyclic_signature(c) for c in row["pocket_cycles"])
        assert sorted(map(len, cycles)) == row["length_profile"]
        assert len(cycles) == row["saving_d"] + 1 and sum(map(len, cycles)) == 8
        results["partition_rotation_face_walks"] += 1
    witnesses = {w["c4_mask"]: w["C4"] for w in source["witnesses"]}
    expected_masks = [7, 10, 11, 12, 13, 14, 15]
    expected_c4_literals = [list(row) for row in itertools.product(range(4), repeat=4)
                            if all(row[j] != row[(j + 1) % 4] for j in range(4))]
    assert sorted(w["mask"] for w in value["C4_contained_relations"]["witnesses"]) == expected_masks
    assert value["C4_contained_relations"]["literal_order"] == expected_c4_literals
    c4_rows = {w["mask"]: w for w in value["C4_contained_relations"]["witnesses"]}
    for mask, saved in c4_rows.items():
        graph = witnesses[mask]
        assert saved["edges"] == graph["edges"]
        assert saved["named_boundary"] == graph["named_boundary"]
        assert saved["private_order"] == graph["interior_order"]
        assert [r["boundary_colors"] for r in saved["all_84_fibres"]] == expected_c4_literals
        for row in saved["all_84_fibres"]:
            assert direct_tuples(graph["edges"], graph["named_boundary"], graph["interior_order"], row["boundary_colors"]) == row["lifts"]
            results["C4_literal_fibres"] += 1
    reductions = value["C4_contained_relations"]["cheap_contained_relations"]
    assert sorted(r["original_mask"] for r in reductions) == expected_masks
    for reduction in reductions:
        allowed = [m for m in [7, 10, 12] if m & reduction["original_mask"] == m]
        assert reduction["all_contained_cheap_masks"] == allowed
        assert reduction["selected_mask"] in allowed
        assert reduction["selected_private_count"] == len(witnesses[reduction["selected_mask"]]["interior_order"])
        old = c4_rows[reduction["original_mask"]]["all_84_fibres"]
        cheap = c4_rows[reduction["selected_mask"]]["all_84_fibres"]
        assert all(not r["lifts"] or old[i]["lifts"] for i, r in enumerate(cheap))
        results["C4_cheap_literal_relation_inclusions"] += 84
    assert value["original_C8_pattern_order"] == interface["pattern_order"]
    assert value["original_U_queries"] == queries
    rng = random.Random(17)
    combos = list(value["opposite_pair_C4_joint_fibres"]["combinations"])
    expected_combo_keys = {(i, i + 4, m1, m2) for i in range(4)
                           for m1, m2 in itertools.product(expected_masks, repeat=2)}
    actual_combo_keys = [tuple(c["identified_original_pair"] + c["ordered_masks"]) for c in combos]
    assert len(actual_combo_keys) == len(expected_combo_keys) == 196
    assert set(actual_combo_keys) == expected_combo_keys
    rng.shuffle(combos)
    for combo in combos:
        pair = combo["identified_original_pair"]
        i = pair[0]
        orders = [[(i + j) % 8 for j in range(4)], [i] + [(i + j) % 8 for j in range(5, 8)]]
        assert orders == combo["pocket_boundary_orders"]
        reconstructed = set()
        private = []
        next_private = 8
        for mask, boundary in zip(combo["ordered_masks"], orders):
            graph = witnesses[mask]
            mapping = dict(zip(graph["named_boundary"], boundary))
            for v in graph["interior_order"]:
                mapping[v] = next_private
                private.append(next_private)
                next_private += 1
            reconstructed.update(tuple(sorted((mapping[a], mapping[b]))) for a, b in graph["edges"])
        assert combo["edges"] == [list(e) for e in sorted(reconstructed)]
        assert combo["private_order"] == private
        assert len(combo["all_274_fibres"]) == 274
        indices = list(range(274))
        rng.shuffle(indices)
        edges = list(combo["edges"])
        rng.shuffle(edges)
        for p in indices:
            row = interface["pattern_order"][p]
            full = [] if row[pair[0]] != row[pair[1]] else direct_tuples(edges, list(range(8)), private, row)
            assert full == combo["all_274_fibres"][p]
            results["whole_graph_seed17_product_fibres"] += 1
        support = [p for p, f in enumerate(combo["all_274_fibres"]) if f]
        assert support == combo["support_original_indices"]
        assert len(combo["U_intersections"]) == len(queries) == 8
        for saved, q in zip(combo["U_intersections"], queries):
            assert saved["query_id"] == q["query_id"]
            intersection = [p for p in support if q["support"] & (1 << p)]
            assert saved["original_C8_row_indices"] == intersection and intersection
            assert saved["first_complete_lift"] == combo["all_274_fibres"][intersection[0]][0]
            results["original_U_joint_intersections"] += 1
    projection = value["C6_short_chord_projections"]
    c6_patterns = projection["C6_pattern_order"]
    expected_c6 = sorted({tuple(normalize(row)[0]) for row in itertools.product(range(4), repeat=6)
                          if all(row[j] != row[(j + 1) % 6] for j in range(6))})
    assert c6_patterns == [list(row) for row in expected_c6]
    assert len(c6_patterns) == 31
    assert projection["query_order"] == [q["query_id"] for q in queries]
    chords = projection["all_eight_short_chords"]
    assert sorted(c["identified_original_pair"] for c in chords) == [[i, (i + 2) % 8] for i in range(8)]
    for chord in chords:
        a, b = chord["identified_original_pair"]
        order = [a] + [(a + j) % 8 for j in range(3, 8)]
        assert order == chord["long_pocket_original_order"]
        direct_literal_map = []
        canonical_map = {}
        for index, literal in enumerate(interface["literal_assignments"]):
            if literal[a] != literal[b]:
                continue
            projected = [literal[j] for j in order]
            normalized, colors = normalize(projected)
            projected_index = c6_patterns.index(normalized)
            original_index = interface["literal_to_pattern"][index]
            direct_literal_map.append([index, original_index, projected, projected_index, colors, literal[(a + 1) % 8]])
            canonical = interface["pattern_order"][original_index]
            canonical_projected = [canonical[j] for j in order]
            n, frame = normalize(canonical_projected)
            canonical_map[original_index] = (canonical_projected, c6_patterns.index(n), frame)
        assert direct_literal_map == chord["all_2196_literal_Eq_mappings"]
        results["C6_complete_literal_preimage_mappings"] += len(direct_literal_map)
        assert sorted(canonical_map) == [m["original_C8_index"] for m in chord["original_C8_mappings"]]
        for saved in chord["original_C8_mappings"]:
            p = saved["original_C8_index"]
            projected, index, frame = canonical_map[p]
            assert saved["projected_literal_C6_row"] == projected
            assert saved["normalized_C6_index"] == index
            assert saved["C6_normalized_color_to_original_color"] == frame
            assert saved["in_original_U"] == [bool(q["support"] & (1 << p)) for q in queries]
        fibres = chord["all_31_C6_preimage_fibres_including_empty_U_fibres"]
        assert sorted(f["C6_index"] for f in fibres) == list(range(31))
        for fibre in fibres:
            assert fibre["C6_row"] == c6_patterns[fibre["C6_index"]]
            preimages = [p for p in sorted(canonical_map) if canonical_map[p][1] == fibre["C6_index"]]
            assert preimages == fibre["all_original_Eq_preimages"]
            assert fibre["original_U_preimages"] == [[p for p in preimages if q["support"] & (1 << p)] for q in queries]
            results["C6_all_31_complete_preimage_fibres"] += 1
        assert len(chord["projected_U_bounds"]) == len(queries) == 8
        for saved, q in zip(chord["projected_U_bounds"], queries):
            assert saved["query_id"] == q["query_id"]
            original = [p for p in sorted(canonical_map) if q["support"] & (1 << p)]
            normalized = sorted({canonical_map[p][1] for p in original})
            assert original == saved["original_Eq_U_indices"]
            assert normalized == saved["projected_C6_indices"]
            assert sum(1 << p for p in normalized) == saved["projected_C6_mask"]
    return dict(results)


def negative_checks(value, source, interface, queries):
    """Send real corrupted certificates through the same fail-closed reader."""
    cases = {}
    bad = copy.deepcopy(value)
    bad["partition_control"]["rows"].pop()
    cases["dropped_partition"] = bad
    bad = copy.deepcopy(value)
    bad["opposite_pair_C4_joint_fibres"]["combinations"].pop()
    cases["dropped_joint_combination"] = bad
    bad = copy.deepcopy(value)
    combo = bad["opposite_pair_C4_joint_fibres"]["combinations"][0]
    index = next(p for p, f in enumerate(combo["all_274_fibres"]) if not f)
    combo["all_274_fibres"][index] = [[0] * len(combo["private_order"])]
    cases["fabricated_empty_fibre"] = bad
    bad = copy.deepcopy(value)
    reduction = next(r for r in bad["C4_contained_relations"]["cheap_contained_relations"] if r["original_mask"] == 14)
    reduction["selected_mask"] = 7
    reduction["selected_private_count"] = 1
    cases["false_C4_selected7_subset14"] = bad
    bad = copy.deepcopy(value)
    fibre = bad["C6_short_chord_projections"]["all_eight_short_chords"][0]["all_31_C6_preimage_fibres_including_empty_U_fibres"][0]
    fibre["all_original_Eq_preimages"].pop()
    cases["dropped_C6_preimage"] = bad
    outcomes = {}
    for name, corrupted in cases.items():
        try:
            check(corrupted, source, interface, queries)
        except (AssertionError, ValueError) as error:
            outcomes[name] = {"rejected": True, "exception": type(error).__name__}
        else:
            raise AssertionError("Independent validator accepted negative control: " + name)
    return outcomes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="exclusively save independent check report")
    parser.add_argument("--write-v2", action="store_true", help="exclusively save new independent check report, preserving v1")
    parser.add_argument("--negative", action="store_true", help="validate five actual corrupted certificate copies")
    args = parser.parse_args()
    assert not (args.write and args.write_v2)
    manifest = json.loads((HERE.parent / "INPUTS.json").read_text())
    for record in manifest["files"]:
        data = (HERE.parent / "frozen" / record["path"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == record["sha256"]
    frozen = HERE.parent / "frozen"
    source = json.loads(gzip.decompress(next(frozen.rglob("C4_CERTIFICATE.json.gz")).read_bytes()))
    interface = json.loads(next(frozen.rglob("interface.json")).read_text())
    integrated = json.loads(next(frozen.rglob("RESULTS.json")).read_text())
    queries = [q for q in integrated["queries"] if q["status"] == "necessary_condition_residual"]
    packed = (HERE / "CERTIFICATE.json.gz").read_bytes()
    value = json.loads(gzip.decompress(packed))
    result = {"independent_check": "PASS", "producer_imported": False,
              "certificate_sha256": hashlib.sha256(packed).hexdigest(),
              "routes": {"partitions": "set-block assignments and all-block-chord crossings",
                         "pockets": "directed-edge face walks of convex polygon rotation system",
                         "full_fibres": "seed17 direct whole-graph4^a products",
                         "C6_projection": "literal6564-row projection then canonical-row reconstruction"},
              "checks": check(value, source, interface, queries)}
    result["exact_coverage"] = {"C4_masks": 7, "literal_rows_per_C4": 84,
                                "opposite_identification_ordered_mask_keys": 196,
                                "original_rows_per_joint_graph": 274,
                                "short_chords": 8, "proper_C6_rows": 31,
                                "original_queries": 8}
    if args.negative:
        result["actual_mutated_certificate_rejections"] = negative_checks(value, source, interface, queries)
    if args.write or args.write_v2:
        target = "INDEPENDENT_CHECK.v2.json" if args.write_v2 else "INDEPENDENT_CHECK.json"
        with (HERE / target).open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
