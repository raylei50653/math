#!/usr/bin/env python3
"""Finite pocket controls. Stdlib only; --write refuses existing outputs."""
from __future__ import annotations

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
AUDIT = HERE.parent
MASKS = (7, 10, 11, 12, 13, 14, 15)


def canon(row):
    frame = []
    out = []
    for color in row:
        if color not in frame:
            frame.append(color)
        out.append(frame.index(color))
    return tuple(out), tuple(frame)


def proper(row):
    return all(row[i] != row[(i + 1) % len(row)] for i in range(len(row)))


def load_inputs():
    manifest = json.loads((AUDIT / "INPUTS.json").read_text())
    for record in manifest["files"]:
        data = (AUDIT / "frozen" / record["path"]).read_bytes()
        assert len(data) == record["bytes"]
        assert hashlib.sha256(data).hexdigest() == record["sha256"]
    frozen = AUDIT / "frozen"
    c4 = json.loads(gzip.decompress(next(frozen.rglob("C4_CERTIFICATE.json.gz")).read_bytes()))
    interface = json.loads(next(frozen.rglob("interface.json")).read_text())
    integrated = json.loads(next(frozen.rglob("RESULTS.json")).read_text())
    queries = [q for q in integrated["queries"] if q["status"] == "necessary_condition_residual"]
    assert len(queries) == 8
    assert len(interface["pattern_order"]) == 274
    assert len(interface["literal_assignments"]) == 6564
    return manifest, c4, interface, queries


def restricted_growth(n):
    """All Bell(n) restricted growth strings, without planarity pruning."""
    def rec(prefix, maximum):
        if len(prefix) == n:
            yield tuple(prefix)
        else:
            for x in range(maximum + 2):
                yield from rec(prefix + [x], max(maximum, x))
    yield from rec([0], 0)


def legal_partition(p):
    if any(p[i] == p[(i + 1) % len(p)] for i in range(len(p))):
        return False
    for a, b, c, d in itertools.combinations(range(len(p)), 4):
        if p[a] == p[c] and p[b] == p[d] and p[a] != p[b]:
            return False
    return True


def independent_partitions(n):
    """Set-block recursion, with an independent chord-crossing criterion."""
    def rec(remaining, blocks):
        if not remaining:
            labels = [None] * n
            for k, block in enumerate(blocks):
                for v in block:
                    labels[v] = k
            edges = []
            for block in blocks:
                # All polygon sides of each block, rather than the fan scaffold.
                if len(block) > 1:
                    edges.extend(tuple(sorted((block[j], block[(j + 1) % len(block)])))
                                 for j in range(len(block)))
            if any(labels[i] == labels[(i + 1) % n] for i in range(n)):
                return
            for (a, c), (b, d) in itertools.combinations(edges, 2):
                if len({a, b, c, d}) == 4 and (a < b < c < d or b < a < d < c):
                    return
            yield tuple(labels)
            return
        root, *rest = remaining
        for size in range(len(rest) + 1):
            for tail in itertools.combinations(rest, size):
                block = (root,) + tail
                yield from rec(tuple(x for x in rest if x not in tail), blocks + [block])
    yield from rec(tuple(range(n)), [])


def pockets(p):
    blocks = [[i for i, label in enumerate(p) if label == k] for k in range(max(p) + 1)]
    forest = [(block[0], v) for block in blocks for v in block[1:]]
    faces = [list(range(len(p)))]
    for a, b in forest:
        containing = [(i, face) for i, face in enumerate(faces) if a in face and b in face]
        assert len(containing) == 1
        index, face = containing[0]
        ia, ib = face.index(a), face.index(b)
        if ia > ib:
            ia, ib = ib, ia
        assert ib - ia > 1 and not (ia == 0 and ib == len(face) - 1)
        faces[index:index + 1] = [face[ia:ib + 1], face[ib:] + face[:ia + 1]]
    cycles = []
    for face in faces:
        contracted = []
        for v in face:
            if not contracted or p[v] != contracted[-1]:
                contracted.append(p[v])
        if len(contracted) > 1 and contracted[0] == contracted[-1]:
            contracted.pop()
        assert len(contracted) >= 2  # Parallel-edge digons are retained.
        assert len(set(contracted)) == len(contracted)
        cycles.append(contracted)
    d = len(p) - len(blocks)
    assert len(faces) == d + 1
    assert sum(map(len, cycles)) == len(p)
    return {"partition": p, "blocks": blocks, "saving_d": d, "fan_forest": forest,
            "uncontracted_faces": faces, "pocket_cycles": cycles,
            "length_profile": sorted(map(len, cycles))}


def partition_control():
    all_rgs = list(restricted_growth(8))
    assert len(all_rgs) == 4140
    accepted = [p for p in all_rgs if legal_partition(p)]
    independent = sorted(independent_partitions(8))
    assert sorted(accepted) == independent
    rows = [pockets(p) for p in accepted]
    histogram = collections.Counter((r["saving_d"], tuple(r["length_profile"])) for r in rows)
    assert set(histogram) == {(0, (8,)), (1, (2, 6)), (1, (3, 5)), (1, (4, 4)),
                              (2, (2, 2, 4)), (2, (2, 3, 3)), (3, (2, 2, 2, 2))}
    return {"all_Bell8_restricted_growth_strings": len(all_rgs),
            "accepted": len(rows), "independent_set_block_enumerator_agrees": True,
            "maximum_saving": max(r["saving_d"] for r in rows),
            "profile_counts": [{"d": d, "lengths": lengths, "count": count}
                               for (d, lengths), count in sorted(histogram.items())],
            "rows": rows}


def dfs_fibre(edges, boundary, private, literal):
    """Whole-graph DFS with dynamic degree ordering, returns ordered full tuples."""
    colors = dict(zip(boundary, literal))
    neighbors = collections.defaultdict(set)
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
        if a == b or (a in colors and b in colors and colors[a] == colors[b]):
            return []
    result = []
    def rec(remaining):
        if not remaining:
            result.append(tuple(colors[v] for v in private))
            return
        v = max(remaining, key=lambda x: (len(neighbors[x] & colors.keys()), len(neighbors[x]), -x))
        forbidden = {colors[u] for u in neighbors[v] if u in colors}
        for color in range(4):
            if color not in forbidden:
                colors[v] = color
                rec(remaining - {v})
                del colors[v]
    rec(set(private))
    return sorted(result)


def product_fibre(edges, boundary, private, literal):
    """Independent direct product constraint evaluation."""
    fixed = dict(zip(boundary, literal))
    result = []
    for assignment in itertools.product(range(4), repeat=len(private)):
        colors = fixed | dict(zip(private, assignment))
        if all(colors[a] != colors[b] for a, b in edges):
            result.append(assignment)
    return result


def c4_control(source):
    witnesses = {w["c4_mask"]: w["C4"] for w in source["witnesses"]}
    literals = [row for row in itertools.product(range(4), repeat=4) if proper(row)]
    assert len(literals) == 84
    full = {}
    for mask in MASKS:
        graph = witnesses[mask]
        rows = []
        for literal in literals:
            direct = product_fibre(graph["edges"], graph["named_boundary"], graph["interior_order"], literal)
            whole = dfs_fibre(graph["edges"], graph["named_boundary"], graph["interior_order"], literal)
            assert whole == direct
            rows.append({"boundary_colors": literal, "lifts": direct})
        assert rows == [{"boundary_colors": tuple(r["boundary_colors"]),
                         "lifts": [tuple(x) for x in r["lifts"]]}
                        for r in graph["all_boundary_rows"]]
        full[mask] = rows
    reductions = []
    for mask in MASKS:
        options = [cheap for cheap in (7, 10, 12) if cheap & mask == cheap]
        assert options
        selected = min(options, key=lambda m: (len(witnesses[m]["interior_order"]), m))
        for cheap in options:
            assert all(not row["lifts"] or full[mask][i]["lifts"] for i, row in enumerate(full[cheap]))
        reductions.append({"original_mask": mask, "all_contained_cheap_masks": options,
                           "selected_mask": selected,
                           "selected_private_count": len(witnesses[selected]["interior_order"]),
                           "relation_inclusion_on_all_84_literal_rows": True})
    return {"pattern_order": source["C4_pattern_order"], "literal_order": literals,
            "witnesses": [{"mask": mask, "edges": witnesses[mask]["edges"],
                           "named_boundary": witnesses[mask]["named_boundary"],
                           "private_order": witnesses[mask]["interior_order"],
                           "all_84_fibres": full[mask]} for mask in MASKS],
            "cheap_contained_relations": reductions}, witnesses


def map_graph(graph, boundary, next_private):
    mapping = dict(zip(graph["named_boundary"], boundary))
    private = list(range(next_private, next_private + len(graph["interior_order"])))
    mapping.update(zip(graph["interior_order"], private))
    edges = sorted({tuple(sorted((mapping[a], mapping[b]))) for a, b in graph["edges"]})
    return edges, private


def opposite_control(witnesses, patterns, queries):
    combinations = []
    totals = collections.Counter()
    min_query_intersection = {q["query_id"]: 274 for q in queries}
    for i in range(4):
        pocket_orders = [[(i + j) % 8 for j in range(4)],
                         [i] + [(i + j) % 8 for j in range(5, 8)]]
        for m1, m2 in itertools.product(MASKS, repeat=2):
            e1, v1 = map_graph(witnesses[m1], pocket_orders[0], 8)
            e2, v2 = map_graph(witnesses[m2], pocket_orders[1], 8 + len(v1))
            private = v1 + v2
            edges = sorted(set(e1 + e2))
            rows = []
            support = []
            for p, literal in enumerate(patterns):
                if literal[i] != literal[i + 4]:
                    whole, joined = [], []
                else:
                    whole = dfs_fibre(edges, list(range(8)), private, literal)
                    local1 = product_fibre(e1, pocket_orders[0], v1, [literal[j] for j in pocket_orders[0]])
                    local2 = product_fibre(e2, pocket_orders[1], v2, [literal[j] for j in pocket_orders[1]])
                    joined = sorted(a + b for a, b in itertools.product(local1, local2))
                    assert whole == joined
                totals["rows"] += 1
                totals["full_lifts"] += len(whole)
                totals["empty_fibres"] += not whole
                if whole:
                    support.append(p)
                rows.append(whole)
            intersections = []
            for q in queries:
                common = [p for p in support if q["support"] >> p & 1]
                assert common
                min_query_intersection[q["query_id"]] = min(min_query_intersection[q["query_id"]], len(common))
                intersections.append({"query_id": q["query_id"], "original_C8_row_indices": common,
                                      "first_complete_lift": rows[common[0]][0]})
            combinations.append({"identified_original_pair": [i, i + 4], "ordered_masks": [m1, m2],
                                 "pocket_boundary_orders": pocket_orders, "private_order": private,
                                 "edges": edges, "all_274_fibres": rows,
                                 "support_original_indices": support, "U_intersections": intersections,
                                 "whole_DFS_equals_same_literal_pocket_join": True,
                                 "six_private_exception": m1 == 14 and m2 == 14})
    assert len(combinations) == 196
    assert totals["rows"] == 196 * 274
    return {"combinations": combinations, "summary": dict(totals),
            "all_1568_combination_query_intersections_nonempty": True,
            "minimum_U_intersection_by_query": min_query_intersection,
            "max_private_count": max(len(c["private_order"]) for c in combinations),
            "six_private_14_14_combinations": 4,
            "scope": "Exact canonical ordered frozen representatives; no arbitrary-gadget theorem."}


def c6_projection(patterns, literals, literal_to_pattern, queries):
    c6_patterns = sorted({canon(row)[0] for row in itertools.product(range(4), repeat=6) if proper(row)})
    assert len(c6_patterns) == 31
    c6_index = {row: i for i, row in enumerate(c6_patterns)}
    chords = []
    for i in range(8):
        identified = [i, (i + 2) % 8]
        long_order = [i] + [(i + j) % 8 for j in range(3, 8)]
        mappings = []
        for p, original in enumerate(patterns):
            if original[identified[0]] == original[identified[1]]:
                projected = tuple(original[j] for j in long_order)
                normalized, frame = canon(projected)
                mappings.append({"original_C8_index": p, "original_C8_row": original,
                                 "projected_literal_C6_row": projected,
                                 "normalized_C6_index": c6_index[normalized],
                                 "C6_normalized_color_to_original_color": frame,
                                 "omitted_original_vertex": (i + 1) % 8,
                                 "omitted_original_color": original[(i + 1) % 8],
                                 "in_original_U": [bool(q["support"] >> p & 1) for q in queries]})
        fibres = []
        for index, row in enumerate(c6_patterns):
            preimages = [m["original_C8_index"] for m in mappings if m["normalized_C6_index"] == index]
            fibres.append({"C6_index": index, "C6_row": row, "all_original_Eq_preimages": preimages,
                           "original_U_preimages": [[p for p in preimages if q["support"] >> p & 1]
                                                    for q in queries]})
        literal_mappings = []
        for index, original in enumerate(literals):
            if original[identified[0]] == original[identified[1]]:
                projected = tuple(original[j] for j in long_order)
                normalized, frame = canon(projected)
                literal_mappings.append([index, literal_to_pattern[index], list(projected),
                                         c6_index[normalized], list(frame), original[(i + 1) % 8]])
        assert len(mappings) == 92
        assert len(literal_mappings) == 2196
        assert all(f["all_original_Eq_preimages"] for f in fibres)
        supports = []
        for qn, q in enumerate(queries):
            rows = [f["C6_index"] for f in fibres if f["original_U_preimages"][qn]]
            supports.append({"query_id": q["query_id"], "projected_C6_indices": rows,
                             "projected_C6_mask": sum(1 << r for r in rows),
                             "projected_support_size": len(rows),
                             "original_Eq_U_indices": [m["original_C8_index"] for m in mappings if m["in_original_U"][qn]]})
        chords.append({"identified_original_pair": identified, "long_pocket_original_order": long_order,
                       "digon_original_vertex": (i + 1) % 8, "original_C8_mappings": mappings,
                       "all_31_C6_preimage_fibres_including_empty_U_fibres": fibres,
                       "literal_mapping_columns": ["original_6564_literal_index", "original_274_pattern_index",
                                                   "projected_literal_C6", "normalized_C6_index",
                                                   "normalized_C6_color_to_original_color", "omitted_original_color"],
                       "all_2196_literal_Eq_mappings": literal_mappings,
                       "projected_U_bounds": supports})
    return {"C6_pattern_order": c6_patterns, "query_order": [q["query_id"] for q in queries],
            "all_eight_short_chords": chords,
            "scope": "Exact image of original U intersect Eq. Necessary bounds only; no actual H relation asserted.",
            "source_realizability": "OPEN", "uncovered_cap_private_vertices": 6}


def produce():
    manifest, c4, interface, queries = load_inputs()
    c4_result, witnesses = c4_control(c4)
    return {"schema": "c8-pocket-finite-controls-v1", "base": manifest["base"],
            "frozen_input_sha256": {r["path"]: r["sha256"] for r in manifest["files"]},
            "colour_frame": [0, 1, 2, 3], "original_C8_pattern_order": interface["pattern_order"],
            "original_U_queries": queries, "partition_control": partition_control(),
            "C4_contained_relations": c4_result,
            "opposite_pair_C4_joint_fibres": opposite_control(witnesses, interface["pattern_order"], queries),
            "C6_short_chord_projections": c6_projection(interface["pattern_order"], interface["literal_assignments"],
                                                      interface["literal_to_pattern"], queries),
            "four_colour_theorem_assumed": False, "new_Lean_theorem": False,
            "general_theorem": "OPEN"}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def negative_controls(value):
    results = {}
    # Removing a legal partition must fail the independently enumerated exact set.
    mutated = copy.deepcopy(value["partition_control"]["rows"])
    mutated.pop()
    results["dropped_partition_detected"] = {tuple(x["partition"]) for x in mutated} != set(independent_partitions(8))
    # Turning an empty full fibre into a tuple breaks direct exact-fibre replay.
    combo = value["opposite_pair_C4_joint_fibres"]["combinations"][0]
    empty_index = next(i for i, row in enumerate(combo["all_274_fibres"]) if not row)
    mutated_fibre = [[0] * len(combo["private_order"])]
    original = value["original_C8_pattern_order"][empty_index]
    pair = combo["identified_original_pair"]
    expected = [] if original[pair[0]] != original[pair[1]] else dfs_fibre(
        combo["edges"], list(range(8)), combo["private_order"], original)
    results["fabricated_empty_fibre_detected"] = mutated_fibre != expected
    # Mask 14 does not contain relation 7: the alternating row is explicit countercontrol.
    source = {r["mask"]: r for r in value["C4_contained_relations"]["witnesses"]}
    i = value["C4_contained_relations"]["literal_order"].index([0, 1, 0, 1])
    results["false_C4_7_subset_14_detected"] = bool(source[7]["all_84_fibres"][i]["lifts"]) and not source[14]["all_84_fibres"][i]["lifts"]
    # Dropping an original projection preimage changes the complete preimage fibre.
    chord = value["C6_short_chord_projections"]["all_eight_short_chords"][0]
    fibre = next(x for x in chord["all_31_C6_preimage_fibres_including_empty_U_fibres"] if len(x["all_original_Eq_preimages"]) > 1)
    expected = [m["original_C8_index"] for m in chord["original_C8_mappings"] if m["normalized_C6_index"] == fibre["C6_index"]]
    results["dropped_projection_preimage_detected"] = fibre["all_original_Eq_preimages"][1:] != expected
    assert all(results.values())
    return results


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    certificate = HERE / "CERTIFICATE.json.gz"
    summary_path = HERE / "RESULTS.json"
    if args.write:
        assert not certificate.exists() and not summary_path.exists(), "exclusive create required"
        value = produce()
        data = encoded(value)
        packed = gzip.compress(data, mtime=0)
        with certificate.open("xb") as stream:
            stream.write(packed)
        part = value["partition_control"]
        opposite = value["opposite_pair_C4_joint_fibres"]
        summary = {"schema": value["schema"], "certificate_sha256": hashlib.sha256(packed).hexdigest(),
                   "certificate_bytes": len(packed), "uncompressed_bytes": len(data),
                   "partition_control": {k: v for k, v in part.items() if k != "rows"},
                   "C4_cheap_contained_relations": value["C4_contained_relations"]["cheap_contained_relations"],
                   "opposite_pair_joint_control": {k: v for k, v in opposite.items() if k != "combinations"},
                   "C6_projection_sizes_by_short_chord": [[u["projected_support_size"] for u in c["projected_U_bounds"]]
                                                         for c in value["C6_short_chord_projections"]["all_eight_short_chords"]],
                   "original_eight_residuals_retained": True, "general_theorem": "OPEN",
                   "four_colour_theorem_assumed": False, "new_Lean_theorem": False}
        with summary_path.open("x") as stream:
            json.dump(summary, stream, indent=2)
            stream.write("\n")
        print(json.dumps(summary, sort_keys=True))
    else:
        packed = certificate.read_bytes()
        summary = json.loads(summary_path.read_text())
        assert hashlib.sha256(packed).hexdigest() == summary["certificate_sha256"]
        saved = json.loads(gzip.decompress(packed))
        replay = json.loads(encoded(produce()))
        assert saved == replay
        negatives = negative_controls(saved)
        # Seed17 shuffles row/edge order independently of the producer enumeration.
        rng = random.Random(17)
        combos = list(saved["opposite_pair_C4_joint_fibres"]["combinations"])
        rng.shuffle(combos)
        checked = 0
        for combo in combos:
            indices = list(range(274))
            rng.shuffle(indices)
            edges = list(combo["edges"])
            rng.shuffle(edges)
            for p in indices:
                row = saved["original_C8_pattern_order"][p]
                a, b = combo["identified_original_pair"]
                expected = [] if row[a] != row[b] else dfs_fibre(edges, list(range(8)), combo["private_order"], row)
                assert [list(t) for t in expected] == combo["all_274_fibres"][p]
                checked += 1
        print(json.dumps({"replay_exact": True, "negative_controls": negatives,
                          "seed17_full_rows_checked": checked, "frozen_inputs_verified": True}, sort_keys=True))


if __name__ == "__main__":
    main()
