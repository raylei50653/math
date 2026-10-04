#!/usr/bin/env python3
"""Independent D3 C2 graph audit: no imports from production checkers."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIVE = HERE.parents[2]
Q, U = (0, 1, 0, 1, 2), set(range(4))
CONTACTS, P3 = (10, 11, 12), (7, 8, 9)
SUPPORTS = ((0, 1, 4), (1, 4), (4,))
C2 = "artifacts/c5_mixed_p3_one_color_ternary_unary/observations.json"
C = "artifacts/c5_mixed_p3_common_endpoint/observations.json"
ALIASES = {**{i: f"b{i}" for i in range(5)}, 5: "z", 6: "w",
           **{v: f"x{i}" for i, v in enumerate(P3)},
           **{v: f"u{i}" for i, v in enumerate(CONTACTS)}}


def edge(a, b):
    return (min(a, b), max(a, b))


FRAME = {edge(i, (i + 1) % 5) for i in range(5)}
P3_INTERNAL = {(7, 8), (8, 9)}
P3_ATTACHMENTS = {edge(v, b) for v, bs in zip(P3, SUPPORTS) for b in bs}
ROOT_ORIGINAL = {(5, 6), (5, 9), (6, 9)}
CONTEXT = FRAME | P3_INTERNAL | P3_ATTACHMENTS | ROOT_ORIGINAL
TRIANGLE_INTERNAL = {edge(a, b) for a, b in combinations(CONTACTS, 2)}
TRIANGLE_ATTACHMENTS = {edge(v, a) for v in CONTACTS for a in (1, 5)}
TRIANGLE = TRIANGLE_INTERNAL | TRIANGLE_ATTACHMENTS
PROJECTION = CONTEXT | TRIANGLE


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def col_dict(raw):
    return None if raw is None else {int(v): c for v, c in raw.items()}


def enumerate_colorings(free, edges, pins):
    out = []
    for cs in product(range(4), repeat=len(free)):
        col = pins | dict(zip(free, cs))
        if all(col[a] != col[b] for a, b in edges):
            out.append(col)
    return out


def connected(group, edges):
    if not group:
        return False
    reached = {next(iter(group))}
    while True:
        grown = reached | {b for a, b in edges if a in reached and b in group}
        grown |= {a for a, b in edges if b in reached and a in group}
        if grown == reached:
            return reached == group
        reached = grown


class Audit:
    def __init__(self):
        self.checks, self.failures = 0, []

    def ck(self, name, passed, detail=None):
        self.checks += 1
        if not passed:
            self.failures.append({"check": name, "detail": detail})

    def edges(self, raw, label, expected):
        result = {tuple(e) for e in raw}
        self.ck(label + "/unique", len(result) == len(raw))
        self.ck(label + "/canonical_simple", all(a < b for a, b in result))
        self.ck(label + "/exact_original_set", result == expected,
                {"missing": sorted(expected - result), "extra": sorted(result - expected)})
        return result

    def coloring(self, raw, vertices, edges, pins, label):
        col = col_dict(raw)
        self.ck(label + "/present", col is not None)
        if col is None:
            return None
        self.ck(label + "/exact_vertex_domain", set(col) == set(vertices))
        self.ck(label + "/colors_in_U", all(c in U for c in col.values()))
        self.ck(label + "/shared_frame_and_pins", all(col.get(v) == c for v, c in pins.items()))
        self.ck(label + "/proper_every_retained_edge", all(col.get(a) != col.get(b) for a, b in edges))
        return col

    def minor(self, edges, raw_groups, witnesses, label):
        groups = [set(g) for g in raw_groups]
        self.ck(label + "/five_nonempty_sets", len(groups) == 5 and all(groups))
        self.ck(label + "/sets_disjoint", sum(map(len, groups)) == len(set().union(*groups)))
        for i, g in enumerate(groups):
            self.ck(f"{label}/connected_set_{i}", connected(g, edges))
        self.ck(label + "/ten_distinct_pairs", len(witnesses) == 10 and
                {tuple(w["pair"]) for w in witnesses} == set(combinations(range(5), 2)))
        for n, w in enumerate(witnesses):
            a, b = w["actual_edge"]
            i, j = w["pair"]
            self.ck(f"{label}/witness_{n}_original_edge", edge(a, b) in edges)
            self.ck(f"{label}/witness_{n}_named_sets",
                    (a in groups[i] and b in groups[j]) or (b in groups[i] and a in groups[j]))

    def subdivision(self, record, edges, label):
        branches = tuple(record["branch_vertices"])
        self.ck(label + "/named_branches", branches == (1, 5, 10, 11, 12))
        pairs = [tuple(r["branch_pair"]) for r in record["routes"]]
        self.ck(label + "/ten_distinct_branch_pairs", len(pairs) == 10 and
                set(pairs) == set(combinations(branches, 2)))
        interior_sets, edge_sets, paths = [], [], []
        for n, route in enumerate(record["routes"]):
            a, b = route["branch_pair"]
            path = tuple(route["original_path"])
            self.ck(f"{label}/path_{n}_endpoints", path[0] == a and path[-1] == b)
            self.ck(f"{label}/path_{n}_simple", len(path) == len(set(path)))
            inner = set(path[1:-1])
            self.ck(f"{label}/path_{n}_no_internal_branch", not inner & set(branches))
            used = {edge(x, y) for x, y in zip(path, path[1:])}
            self.ck(f"{label}/path_{n}_every_original_edge", used <= edges,
                    {"extra": sorted(used - edges)})
            interior_sets.append(inner)
            edge_sets.append(used)
            paths.append(path)
        for i, j in combinations(range(len(paths)), 2):
            self.ck(f"{label}/paths_{i}_{j}_internal_disjoint", not interior_sets[i] & interior_sets[j])
            self.ck(f"{label}/paths_{i}_{j}_edge_disjoint", not edge_sets[i] & edge_sets[j])
            self.ck(f"{label}/paths_{i}_{j}_only_shared_endpoints",
                    set(paths[i]) & set(paths[j]) == set(pairs[i]) & set(pairs[j]))
        union = set().union(*edge_sets)
        self.edges(record["subdivision_edges"], label + "/edge_union", union)
        vertices = set(branches) | set().union(*interior_sets)
        degrees = {v: sum(v in e for e in union) for v in vertices}
        self.ck(label + "/branch_and_internal_degrees",
                all(degrees[v] == (4 if v in branches else 2) for v in vertices))
        outside = tuple(record["external_path"])
        self.ck(label + "/named_external_original_path",
                outside in ((5, 9, 4, 3, 2, 1), (5, 9, 4, 0, 1)))
        expected_groups = [{10}, {11}, {12}, {5, *outside[1:-1]}, {1}]
        self.ck(label + "/exact_minor_sets", [set(g) for g in record["branch_sets"]] == expected_groups)
        self.minor(edges, record["branch_sets"], record["minor_adjacency"], label + "/minor")
        return {"external_path": list(outside),
                "external_path_names": [ALIASES[v] for v in outside],
                "path_count": len(paths), "subdivision_edges": len(union),
                "vertices": len(vertices), "internal_vertices": sorted(vertices - set(branches)),
                "edge_pair_disjointness_checks": len(edge_sets) * (len(edge_sets) - 1) // 2,
                "all_edges_with_original_provenance": sorted(union)}


def run(source):
    a = Audit()
    data = json.loads((source / C2).read_bytes())
    parent = json.loads((source / C).read_bytes())
    baseline = json.loads((LIVE / "audits/2026-10-04-task-d2/successor_baseline_final.json").read_bytes())
    hashes = {}
    for name in (C2, "scripts/c5_mixed_p3_one_color_ternary_unary.py",
                 "docs/c5_mixed_p3_one_color_ternary_unary.md"):
        actual, live, expected = digest(source / name), digest(LIVE / name), baseline["new_files"][name]["sha256"]
        a.ck("D2_baseline/" + name, actual == expected)
        hashes[name] = {"D2_sha256": expected, "audited_sha256": actual,
                        "live_sha256_at_audit": live, "live_matches_D2": live == expected}
    for name, expected in data["inputs_sha256"].items():
        a.ck("recorded_input_hash/" + name, digest(source / name) == expected)
    hashes[C] = {"sha256": digest(source / C), "C2_recorded_sha256": data["inputs_sha256"][C]}
    identity, tri = data["identity"], data["forced_triangle"]
    a.ck("identity/predecessor_exact_entry", identity["parent_entry"] == parent["next_entry"])
    entry = identity["parent_entry"]
    a.ck("identity/target", (entry["case_name"], entry["geometry_id"], entry["side_join_id"]) == ("CPP-134-1", 30, 20))
    a.ck("identity/aliases", {int(k): v for k, v in identity["aliases"].items()} == ALIASES)
    a.ck("identity/literal_P3_supports", identity["local"]["actual_supports"] == [list(s) for s in SUPPORTS])
    a.ck("identity/actual_side_supports", identity["geometry"]["actual_side_supports"] == [[1], [2, 4]])
    a.ck("identity/no_original_spokes", all(not entry[side]["spoke_colors"] for side in ("z_role", "w_role")))
    a.ck("identity/side_ids", entry["side_ids"] == [8, 1])
    a.edges(identity["original_context_edges"], "context", CONTEXT)
    a.edges(tri["edges"], "forced_original_unary", TRIANGLE)
    a.edges(tri["original_source_projection_edges"], "source_projection", PROJECTION)
    a.ck("unary/original_contacts", tuple(tri["ordered_contacts"]) == CONTACTS)
    a.ck("unary/original_attachments", tri["actual_attachments"] == {str(v): [1, 5] for v in CONTACTS})
    degrees = {v: sum(v in e for e in PROJECTION) for v in (5, 6, *P3, *CONTACTS)}
    a.ck("projection/degrees", all(degrees[v] == (5 if v == 5 else 4) for v in (5, *P3, *CONTACTS)))
    a.ck("projection/w_symbolic_three_contacts", degrees[6] == 2 and identity["preserved_w_component"]["root_incidence_count"] == 3)
    pins = dict(enumerate(Q))
    p3_tuples = sorted(tuple(c[v] for v in P3) for c in enumerate_colorings(P3, P3_INTERNAL | P3_ATTACHMENTS, pins))
    a.ck("P3/full_triples", p3_tuples == [(3, 0, 1), (3, 0, 3)] == [tuple(t) for t in identity["local"]["complete_triples"]])
    p3_fibres = {f"{z},{w}": [list(t) for t in p3_tuples if t[2] not in (z, w)] for z, w in product(range(4), repeat=2)}
    p3_empty = [tuple(map(int, p.split(","))) for p, f in p3_fibres.items() if not f]
    a.ck("P3/all_empty_fibres", p3_empty == [(1, 3), (3, 1)] == [tuple(p) for p in identity["original_P3_forbidden"]])
    joint = {(z, w) for z, w in product((1,), (1, 3)) if p3_fibres[f"{z},{w}"]}
    a.ck("side_join/without_zw", joint == {(1, 1)} == {tuple(p) for p in identity["original_root_join_without_zw"]})
    a.ck("side_join/with_original_zw", {p for p in joint if p[0] != p[1]} == set() == {tuple(p) for p in identity["original_root_join_with_zw"]})
    unary_tuples = sorted(tuple(c[v] for v in CONTACTS) for c in enumerate_colorings(CONTACTS, TRIANGLE_INTERNAL | {edge(1, v) for v in CONTACTS}, pins))
    a.ck("unary/all_six_ordered_triples", unary_tuples == [tuple(t) for t in tri["complete_contact_tuples"]] and len(unary_tuples) == 6)
    forbidden = set.intersection(*(set(t) for t in unary_tuples))
    a.ck("unary/complete_forbidden", forbidden == {0, 2, 3} == set(tri["forbidden"]))
    unary_fibres = {f"{z},{w}": [list(t) for t in unary_tuples if z not in t] for z, w in product(range(4), repeat=2)}
    a.ck("unary/root_pair_relation", {tuple(map(int, p.split(","))) for p, f in unary_fibres.items() if f} == {tuple(p) for p in tri["root_pair_relation"]})
    intact_counts = {}
    a.ck("unary/four_intact_pins", len(tri["intact_pins"]) == 4 and {r["z"] for r in tri["intact_pins"]} == U)
    for row in tri["intact_pins"]:
        h = row["z"]
        fixed = pins | {5: h, 6: 1}
        cols = enumerate_colorings(CONTACTS, TRIANGLE, fixed)
        intact_counts[str(h)] = len(cols)
        a.ck(f"unary/intact_z_{h}_empty", (row["coloring"] is None) == (len(cols) == 0))
        if row["coloring"] is not None:
            a.coloring(row["coloring"], (*range(7), *CONTACTS), TRIANGLE, fixed, f"unary/intact_z_{h}")
    a.ck("unary/intact_counts", intact_counts == {"0": 0, "1": 6, "2": 0, "3": 0})
    a.ck("unary/rejection_palettes", tri["rejection_block_palettes"] == [{"z": h, "palette": sorted(U - {1, h})} for h in (0, 2, 3)])
    rows = data["local_degree_lists"]
    a.ck("degree_lists/four_original_types", len(rows) == 4 and {(r["original_z_contact"], r["original_b1_attachment"]) for r in rows} == set(product((False, True), repeat=2)))
    for n, row in enumerate(rows):
        p, s = int(row["original_z_contact"]), int(row["original_b1_attachment"])
        degree = 4 - p - s
        a.ck(f"degree_lists/type_{n}_degree", row["degree_in_D"] == degree)
        a.ck(f"degree_lists/type_{n}_four_pins", len(row["pinned_lists"]) == 4 and {r["z"] for r in row["pinned_lists"]} == U)
        for pin in row["pinned_lists"]:
            h = pin["z"]
            colors = ([h] if p else []) + ([1] if s else [])
            allowed = U - set(colors)
            a.ck(f"degree_lists/type_{n}_pin_{h}", pin["external_colors"] == colors and pin["list"] == sorted(allowed) and pin["slack"] == len(allowed) - degree == int(h == 1 and p == s == 1))
    deletions = tri["deletions"]
    a.ck("deletions/exact_nine_original_edges", len(deletions) == 9 and {tuple(r["deleted_edge"]) for r in deletions} == TRIANGLE)
    delete_counts, local_count, critical_count, partial_count = [], 0, 0, 0
    for row in deletions:
        deleted = tuple(row["deleted_edge"])
        label = "delete_" + "_".join(map(str, deleted))
        local_after, projection_after = TRIANGLE - {deleted}, PROJECTION - {deleted}
        a.ck(label + "/four_local_pins", len(row["local_witnesses"]) == 4 and {r["z"] for r in row["local_witnesses"]} == U)
        pin_counts = {}
        for witness in row["local_witnesses"]:
            h = witness["z"]
            fixed = pins | {5: h, 6: 1}
            cols = enumerate_colorings(CONTACTS, local_after, fixed)
            pin_counts[str(h)] = len(cols)
            a.ck(f"{label}/enumerated_z_{h}_nonempty", bool(cols))
            col = a.coloring(witness["coloring"], (*range(7), *CONTACTS), local_after, fixed, f"{label}/stored_local_z_{h}")
            local_count += 1
            if h in forbidden and col:
                a.ck(f"{label}/equal_deleted_ends_z_{h}", col[deleted[0]] == col[deleted[1]])
                critical_count += 1
        root_counts = {f"{z},{w}": len(enumerate_colorings(CONTACTS, local_after, pins | {5: z, 6: w})) for z, w in product(range(4), repeat=2)}
        a.ck(label + "/all_sixteen_root_fibres_nonempty", all(root_counts.values()))
        fixed = pins | {5: 0, 6: 1}
        partial_cols = enumerate_colorings((*P3, *CONTACTS), projection_after, fixed)
        a.ck(label + "/partial_enumeration_nonempty", bool(partial_cols))
        col = a.coloring(row["original_context_witness"], range(13), projection_after, fixed, label + "/stored_partial")
        if col:
            a.ck(label + "/partial_equal_deleted_ends", col[deleted[0]] == col[deleted[1]])
            a.ck(label + "/partial_literal_P3_triple", tuple(col[v] for v in P3) == (3, 0, 3))
        a.ck(label + "/unknown_w_completion_scope", "not enumerated" in row["missing_w_completion"])
        partial_count += 1
        delete_counts.append({"deleted_edge": list(deleted), "all_colorings_by_z": pin_counts, "all_root_pair_coloring_counts": root_counts, "partial_projection_coloring_count": len(partial_cols)})
    a.ck("scope/no_invented_Dw_tuples", identity["preserved_w_component"]["relation"] == "R_Dw(q) subset U^3, full same-source relation unknown")
    a.ck("scope/one_named_branch_only", data["summary"]["named_source_branches_closed"] == 1 and data["summary"]["predecessor_deletions"] == 0)
    a.ck("scope/no_target_queries", data["summary"]["target_queries"] == 0)
    subs = [a.subdivision(r, PROJECTION, f"K5_{i}") for i, r in enumerate(data["k5_subdivisions"])]
    a.ck("K5/two_distinct_original_outer_paths", len(subs) == 2 and {tuple(r["external_path"]) for r in subs} == {(5, 9, 4, 3, 2, 1), (5, 9, 4, 0, 1)})
    records = data["k4_tether_controls"]["records"]
    a.ck("K4/exact_control_count", len(records) == 32)
    control_ids = []
    for n, record in enumerate(records):
        label, paths = f"K4_control_{n}", record["tethers"]
        a.ck(label + "/four_tethers", len(paths) == 4)
        clique = {edge(x, y) for x, y in combinations((20, 21, 22, 23), 2)}
        tail_edges = set()
        for i, path in enumerate(paths):
            a.ck(f"{label}/tether_{i}_endpoints", path[0] == 20 + i and path[-1] in (1, 5))
            a.ck(f"{label}/tether_{i}_simple", len(path) == len(set(path)))
            a.ck(f"{label}/tether_{i}_control_interior", path[1:-1] in ([], [40 + i]))
            tail_edges |= {edge(x, y) for x, y in zip(path, path[1:])}
        for i, j in combinations(range(4), 2):
            a.ck(f"{label}/tethers_{i}_{j}_disjoint_before_hub", not set(paths[i][:-1]) & set(paths[j][:-1]))
        shape = tuple(len(p) for p in paths)
        a.ck(label + "/uniform_control_subdivision", shape in ((2,) * 4, (3,) * 4))
        edges = a.edges(record["edges"], label + "/edges", CONTEXT | clique | tail_edges)
        hub = {0, 1, 2, 3, 4, 5, 9} | set().union(*(set(p[1:-1]) for p in paths))
        a.ck(label + "/exact_branch_sets", [set(g) for g in record["branch_sets"]] == [{20}, {21}, {22}, {23}, hub])
        a.minor(edges, record["branch_sets"], record["adjacency"], label + "/minor")
        control_ids.append((tuple(p[-1] for p in paths), shape))
    expected_controls = {(ends, shape) for ends in product((1, 5), repeat=4) for shape in ((2,) * 4, (3,) * 4)}
    a.ck("K4/all_distinct_endpoint_shape_controls", len(set(control_ids)) == 32 and set(control_ids) == expected_controls)
    a.ck("K4/no_source_realization_claim", "not degree/minimality realizations" in data["k4_tether_controls"]["scope"])
    negative = []
    mutations = (
        ("wrong_branch_path_endpoint", lambda r: r["routes"][0]["original_path"].__setitem__(0, 0)),
        ("branch_vertex_as_path_interior", lambda r: r["routes"][0]["original_path"].__setitem__(1, 10)),
        ("repeated_route_pair", lambda r: r["routes"][1].__setitem__("branch_pair", r["routes"][0]["branch_pair"])),
        ("missing_original_edge", lambda r: r["routes"][0]["original_path"].__setitem__(1, 8)),
    )
    for name, mutate in mutations:
        mutant = deepcopy(data["k5_subdivisions"][0])
        mutate(mutant)
        check = Audit()
        check.subdivision(mutant, PROJECTION, "negative_" + name)
        negative.append({"mutation": name, "caught": bool(check.failures), "failures": check.failures})
        a.ck("negative_control/" + name, bool(check.failures))
    summary = {"checks": a.checks, "failures": len(a.failures), "context_edges": len(CONTEXT),
               "forced_original_unary_edges": len(TRIANGLE), "original_projection_edges": len(PROJECTION),
               "full_P3_triples": len(p3_tuples), "empty_P3_root_pair_fibres": len(p3_empty),
               "full_unary_triples": len(unary_tuples), "empty_intact_unary_root_pair_fibres": sum(not f for f in unary_fibres.values()),
               "pinned_list_checks": 16, "deleted_unary_edges": len(deletions),
               "stored_local_deletion_witnesses": local_count, "critical_equal_deleted_ends": critical_count,
               "stored_partial_projection_witnesses": partial_count, "K5_subdivisions": len(subs),
               "K5_ten_pair_paths": 20, "K5_path_pair_edge_disjointness_checks": 90,
               "K5_minor_adjacency_witnesses": 20, "K4_tether_controls": len(records),
               "K4_minor_adjacency_witnesses": 10 * len(records), "negative_controls_caught": sum(n["caught"] for n in negative)}
    return {"schema": 1, "timestamp_utc": datetime.now(timezone.utc).isoformat(), "audited_source_root": str(source),
            "method": "No production imports; literal original edge reconstruction and exhaustive finite color assignments",
            "summary": summary, "failures": a.failures, "input_hashes": hashes,
            "original_edge_provenance": {"induced_C5_frame": sorted(FRAME), "P3_internal": sorted(P3_INTERNAL),
                "literal_P3_attachments": sorted(P3_ATTACHMENTS), "original_root_edges": sorted(ROOT_ORIGINAL),
                "paper_forced_original_unary_internal": sorted(TRIANGLE_INTERNAL), "paper_forced_original_unary_attachments": sorted(TRIANGLE_ATTACHMENTS)},
            "original_projection_degrees": degrees, "P3_triples": p3_tuples,
            "P3_complete_same_frame_root_fibres": p3_fibres, "unary_triples": unary_tuples,
            "unary_complete_same_frame_root_fibres": unary_fibres, "intact_coloring_counts_by_z": intact_counts,
            "deletion_full_enumeration_counts": delete_counts, "K5_subdivisions": subs, "negative_controls": negative,
            "evidence_boundaries": ["The nine original unary edges follow from the paper unary-to-triangle argument. Arbitrary unary size is not enumerated.",
                "The 36 local witnesses use B,z,w,D_z and local unary edges only. They are not whole source colorings.",
                "The nine partial witnesses color the entire 13-vertex original projection except the deleted unary edge. D_w is symbolic.",
                "If original R_Dw exists with f_Dw={0,2}, it contains a tuple avoiding w=1. Its tuples are not invented or enumerated.",
                "The 32 K4 tether controls are route controls, not full source or degree/minimality realizations.",
                "The two K5 subdivisions use every stated edge from the reconstructed original projection; all path interiors and edges are disjoint.",
                "Only CPP-134-1 / geometry 30 / side_join_id 20 is a named C2 exclusion. No target, Lean, full Sigma or general exit is claimed."]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=HERE.parent / "snapshot")
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    args = parser.parse_args()
    result = run(args.source_root)
    args.output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result["summary"], sort_keys=True, indent=2))
    raise SystemExit(bool(result["failures"]))


if __name__ == "__main__":
    main()
