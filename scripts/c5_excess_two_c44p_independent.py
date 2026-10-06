#!/usr/bin/env python3
"""Independent C44-prime audit: frontier DP and explicit S4 quotient.

No C44-prime main implementation is imported or inspected. Definitions and
original C44 input JSON alone supply the domain. The secondary two-root test
enumerates all 240 proper literal frame words and all 16 root colour pairs.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_excess_two_c44p/independent.json"
FRAME = tuple(sorted(tuple(sorted((i, (i + 1) % 5))) for i in range(5)))
COLOUR_PERMS = tuple(permutations(range(4)))
RAW_ROWS = tuple(p for p in product(range(4), repeat=5)
                 if all(p[u] != p[v] for u, v in FRAME))
REPS = tuple(sorted({min(tuple(f[c] for c in p) for f in COLOUR_PERMS)
                     for p in RAW_ROWS}))
RAW_INDEX = {}
for i, row in enumerate(REPS):
    for f in COLOUR_PERMS:
        mapped = tuple(f[c] for c in row)
        assert mapped not in RAW_INDEX or RAW_INDEX[mapped] == i
        RAW_INDEX[mapped] = i
assert len(RAW_ROWS) == 240 and len(REPS) == 10
assert len(RAW_INDEX) == 240


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edges_of(edges):
    return tuple(sorted(tuple(sorted(e)) for e in edges))


def vertices_of(edges):
    return tuple(sorted(set(range(5)) | {v for e in edges for v in e}))


@lru_cache(maxsize=None)
def frontier_counts(edges, row):
    """Count proper extensions by numeric elimination and frontier states.

    At step v, each state records the colours of exactly those earlier
    vertices with an unvisited neighbour. Counts merge colourings sharing
    this sufficient state. No degree heuristic or recursive DFS is used.
    """
    vertices = vertices_of(edges)
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    frontier = ()
    states = {(): 1}
    profile = []
    for v in vertices:
        new_frontier = tuple(x for x in frontier + (v,)
                             if any(y > v for y in adj[x]))
        old_index = {x: i for i, x in enumerate(frontier)}
        earlier = [old_index[u] for u in sorted(adj[v]) if u < v]
        allowed = (row[v],) if v < 5 else range(4)
        nxt = defaultdict(int)
        for state, weight in states.items():
            for colour in allowed:
                if any(state[i] == colour for i in earlier):
                    continue
                expanded = state + (colour,)
                extended_index = {**old_index, v: len(frontier)}
                key = tuple(expanded[extended_index[x]] for x in new_frontier)
                nxt[key] += weight
        frontier, states = new_frontier, dict(nxt)
        profile.append({"vertex": v, "frontier": list(frontier),
                        "states": len(states), "partial_count": sum(states.values())})
    assert frontier == ()
    return states.get((), 0), tuple((r["vertex"], tuple(r["frontier"]),
                                  r["states"], r["partial_count"]) for r in profile)


def full_sigma(edges):
    counts = [frontier_counts(edges, row)[0] for row in REPS]
    return sum(1 << i for i, n in enumerate(counts) if n), counts


def images():
    result = []
    for target in (933, 941):
        for sign in (1, -1):
            for rotation in range(5):
                g = tuple((sign * i + rotation) % 5 for i in range(5))
                row_map = []
                for row in REPS:
                    moved = [None] * 5
                    for i in range(5):
                        moved[g[i]] = row[i]
                    row_map.append(RAW_INDEX[tuple(moved)])
                mask = sum(1 << row_map[i] for i in range(10) if target >> i & 1)
                result.append({"target_sigma": target, "sign": sign,
                               "rotation": rotation, "frame_map": list(g),
                               "row_map": row_map, "sigma_mask": mask})
    return result


IMAGES = images()


def compatibility(mask):
    return [x for x in IMAGES if x["sigma_mask"] & mask == x["sigma_mask"]]


def cyclic_sectors(a):
    sectors = []
    for i, first in enumerate(a):
        end = a[(i + 1) % len(a)]
        arc = [first]
        while arc[-1] != end:
            arc.append((arc[-1] + 1) % 5)
        sectors.append(arc)
    return sectors


def raw_sigma_two(edges):
    """Completely separate b check using raw frame words and root pairs."""
    accepted = set()
    counts_per_rep = defaultdict(set)
    for frame in RAW_ROWS:
        n = 0
        for private in product(range(4), repeat=2):
            colour = frame + private
            if all(colour[u] != colour[v] for u, v in edges):
                n += 1
        idx = RAW_INDEX[frame]
        counts_per_rep[idx].add(n)
        if n:
            accepted.add(idx)
    assert all(len(ns) == 1 for ns in counts_per_rep.values())
    return sum(1 << i for i in accepted), [next(iter(counts_per_rep[i]))
                                          for i in range(10)]


@lru_cache(maxsize=None)
def literal_product_mask(edges):
    """Boolean proper-extension test even when a root becomes isolated."""
    mask = 0
    for i, row in enumerate(REPS):
        for roots in product(range(4), repeat=2):
            colours = row + roots
            if all(colours[u] != colours[v] for u, v in edges):
                mask |= 1 << i
                break
    return mask


def exhaustive_minimal_sets(edges, rejected):
    movable = tuple(e for e in edges if e not in FRAME)
    subset_masks = {}
    subsets = {}
    for code in range(1 << len(movable)):
        sub = edges_of(FRAME + tuple(e for i, e in enumerate(movable) if code >> i & 1))
        subsets[code] = sub
        subset_masks[code] = literal_product_mask(sub)
    answer = []
    for row in rejected:
        minimal = []
        for code, mask in subset_masks.items():
            if mask >> row & 1:
                continue
            if all(subset_masks[code ^ (1 << i)] >> row & 1
                   for i in range(len(movable)) if code >> i & 1):
                minimal.append([list(e) for e in subsets[code]])
        answer.append({"row_index": row, "minimal_core_edge_sets": sorted(minimal)})
    return answer


def mixed(edges):
    remaining = set(vertices_of(edges)) - set(range(7))
    answer = []
    while remaining:
        first = min(remaining)
        comp, stack = {first}, [first]
        while stack:
            x = stack.pop()
            for a, b in edges:
                y = b if a == x else a if b == x else None
                if y in remaining and y not in comp:
                    comp.add(y)
                    stack.append(y)
        remaining -= comp
        owners = sorted({r for r in (5, 6)
                         if any(r in e and (e[0] in comp or e[1] in comp)
                                for e in edges)})
        if owners == [5, 6]:
            answer.append({"vertices": sorted(comp), "owners": owners})
    return answer


def saved_population():
    paths = sorted((ROOT / "artifacts/c5_excess_two_c44/orbits").glob("*.json"))
    assert len(paths) == 19
    cores = {}
    occurrences = []
    source_counts = Counter()
    for path in paths:
        data = json.loads(path.read_text())
        for oi, original in enumerate(data["orbits"]):
            if original["type"] not in ("AD", "NA"):
                continue
            for ri, row in enumerate(original["rows"]):
                assert REPS[row["row_index"]] == tuple(row["literal_row"])
                for ci, core in enumerate(row["cores"]):
                    edges = edges_of(core["edges"])
                    vertices = vertices_of(edges)
                    degree = [sum(v in e for e in edges) for v in (5, 6)]
                    if not {5, 6} <= set(vertices) or degree != [4, 4]:
                        continue
                    assert core["root_degrees"] == [4, 4]
                    assert core["private_size"] == len(vertices) - 5
                    recomputed_mixed = mixed(edges)
                    assert core["contains_mixed_component"] == bool(recomputed_mixed)
                    if edges not in cores:
                        mask, counts = full_sigma(edges)
                        match = compatibility(mask)
                        cores[edges] = {
                            "edges": [list(e) for e in edges],
                            "private_size": len(vertices) - 5,
                            "mixed_components": recomputed_mixed,
                            "sigma_mask": mask, "extension_counts": counts,
                            "compatible": bool(match), "matching_images": match,
                            "occurrence_count": 0,
                        }
                    result = cores[edges]
                    result["occurrence_count"] += 1
                    assert result["sigma_mask"] == core["sigma_mask"], (
                        str(path), oi, ri, ci, result["sigma_mask"], core["sigma_mask"])
                    assert not result["sigma_mask"] >> row["row_index"] & 1
                    pointer = f"/orbits/{oi}/rows/{ri}/cores/{ci}"
                    occurrences.append({
                        "input_chunk": str(path.relative_to(ROOT)),
                        "input_pointer": pointer,
                        "source_type": original["type"],
                        "critical": original["critical"],
                        "row_index": row["row_index"],
                        "edge_key": [list(e) for e in edges],
                        "saved_sigma_mask": core["sigma_mask"],
                        "sigma_mask": result["sigma_mask"],
                        "compatible": result["compatible"],
                    })
                    source_counts[(original["type"], original["critical"])] += 1
    assert source_counts == Counter({("AD", False): 2334, ("AD", True): 26,
                                   ("NA", False): 56})
    return {"inputs": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in paths],
            "occurrences": occurrences, "literal_cores": [cores[e] for e in sorted(cores)],
            "statistics": [{"source_type": t, "critical": c, "occurrences": n}
                           for (t, c), n in sorted(source_counts.items())]}


def two_private():
    records = []
    for adjacent in (True, False):
        count = 3 if adjacent else 4
        for a, b in product(combinations(range(5), count), repeat=2):
            edges = edges_of(FRAME + tuple((i, 5) for i in a) +
                             tuple((i, 6) for i in b) + (((5, 6),) if adjacent else ()))
            sectors = cyclic_sectors(a)
            eligible = [i for i, sector in enumerate(sectors) if set(b) <= set(sector)]
            embeddable = bool(eligible)
            augmented = nx.Graph()
            augmented.add_edges_from(edges)
            augmented.add_edges_from((i, 7) for i in range(5))
            apex_planar, _ = nx.check_planarity(augmented)
            assert embeddable == apex_planar, (adjacent, a, b, sectors)
            mask, counts = full_sigma(edges)
            raw_mask, raw_counts = raw_sigma_two(edges)
            assert (mask, counts) == (raw_mask, raw_counts)
            rejected = [i for i in range(10) if not mask >> i & 1]
            deletion_masks = []
            for edge in edges:
                if edge in FRAME:
                    continue
                deleted = tuple(e for e in edges if e != edge)
                deletion_mask, deletion_counts = raw_sigma_two(deleted)
                dp_deleted_mask, dp_deleted_counts = full_sigma(deleted)
                assert (deletion_mask, deletion_counts) == (dp_deleted_mask, dp_deleted_counts)
                deletion_masks.append({"edge": list(edge), "sigma_mask": deletion_mask})
            minimal_rows = [i for i in rejected
                            if all(d["sigma_mask"] >> i & 1 for d in deletion_masks)]
            transforms = []
            for sign in (1, -1):
                for rotation in range(5):
                    moved_a = tuple(sorted((sign * i + rotation) % 5 for i in a))
                    moved_b = tuple(sorted((sign * i + rotation) % 5 for i in b))
                    for swap in (False, True):
                        aa, bb = (moved_b, moved_a) if swap else (moved_a, moved_b)
                        transforms.append((aa, bb))
            orb = sorted(set(transforms))
            ident = ("AD" if adjacent else "NA") + "-" + "".join(map(str, a)) + "-" + "".join(map(str, b))
            match = compatibility(mask)
            records.append({
                "id": ident, "adjacent": adjacent, "spokes": {"5": list(a), "6": list(b)},
                "edges": [list(e) for e in edges],
                "disk": {"embeddable": embeddable, "sectors": sectors,
                         "eligible_sector_indices": eligible, "apex_planarity_agrees": True},
                "sigma_mask": mask, "extension_counts": counts,
                "raw_quotient_extension_counts": raw_counts,
                "rejected_rows": rejected,
                "whole_graph_minimal_rejected_rows": minimal_rows,
                "edge_deletion_masks": deletion_masks,
                "minimal_core_enumeration": exhaustive_minimal_sets(edges, rejected),
                "compatible": bool(match), "matching_images": match,
                "orbit_canonical_spokes": {"5": list(orb[0][0]), "6": list(orb[0][1])},
                "orbit_size": len(orb), "stabilizer_size": 20 // len(orb),
            })
    assert len(records) == 125
    return records


def build():
    population = saved_population()
    placements = two_private()
    return {"schema_version": 1,
            "algorithm": "numeric-order frontier DP; explicit S4 raw-word orbit lookup",
            "independence": "No C44-prime main implementation read or imported; original C44 JSON and definition docs only",
            "proper_raw_frame_words": len(RAW_ROWS), "colour_permutations": len(COLOUR_PERMS),
            "reps": [list(row) for row in REPS], "target_images": IMAGES,
            "saved_population": population, "two_private": placements,
            "summary": {"occurrences": len(population["occurrences"]),
                        "literal_cores": len(population["literal_cores"]),
                        "compatible_occurrences": sum(o["compatible"] for o in population["occurrences"]),
                        "saved_mask_differences": 0, "placements": len(placements),
                        "disk_placements": sum(p["disk"]["embeddable"] for p in placements),
                        "disk_compatible_placements": sum(p["disk"]["embeddable"] and p["compatible"] for p in placements),
                        "raw_colour_crosscheck_mismatches": 0,
                        "disk_crosscheck_mismatches": 0}}


def colouring_ok(edges, row, colours):
    if isinstance(colours, dict):
        colours = {int(v): c for v, c in colours.items()}
    else:
        colours = dict(enumerate(colours))
    assert all(v in colours and colours[v] in range(4) for v in vertices_of(edges))
    assert all(colours[v] == row[v] for v in range(5))
    assert all(colours[u] != colours[v] for u, v in edges)


def verify_rejection_tree(edges, row, tree):
    edge_set = set(edges)
    assigned = dict(enumerate(row))
    vertices = set(vertices_of(edges))
    nodes = 0

    def visit(node):
        nonlocal nodes
        nodes += 1
        vertex = node["vertex"]
        assert vertex in vertices and vertex not in assigned
        branches = node["branches"]
        assert sorted(b["colour"] for b in branches) == [0, 1, 2, 3]
        for branch in branches:
            colour = branch["colour"]
            if "conflict_edge" in branch:
                edge = tuple(sorted(branch["conflict_edge"]))
                assert edge in edge_set and vertex in edge
                other = edge[1] if edge[0] == vertex else edge[0]
                assert other in assigned and assigned[other] == colour
                assert "child" not in branch
            else:
                assert "child" in branch
                assert all(assigned.get(v) != colour for e in edges
                           if vertex in e for v in e if v != vertex and v in assigned)
                assigned[vertex] = colour
                visit(branch["child"])
                del assigned[vertex]

    visit(tree)
    return nodes


def verify_small_rejection(edges, row, witness):
    domains = {str(v): [c for c in range(4)
                        if all(c != row[u] for u, w in edges if w == v and u < 5)]
               for v in vertices_of(edges) if v >= 5}
    if witness["kind"] == "empty_root_list":
        assert witness["roots"]
        assert all(domains[str(v)] == [] for v in witness["roots"])
    elif witness["kind"] == "adjacent_equal_singleton_lists":
        edge = tuple(sorted(witness["edge"]))
        assert edge in edges
        assert domains[str(edge[0])] == domains[str(edge[1])] == [witness["forced_color"]]
    else:
        raise AssertionError(witness["kind"])
    for root, reported in witness["domains"].items():
        if root in domains:
            assert reported == domains[root]


def canonical_face(face):
    return min(tuple(face[i:] + face[:i]) for i in range(len(face)))


def verify_rotation(edges, rotation, saved_faces):
    rot = {int(v): nbrs for v, nbrs in rotation.items()}
    edge_set = set(edges)
    vertices = vertices_of(edges)
    assert set(rot) == set(vertices)
    for v in vertices:
        assert len(rot[v]) == len(set(rot[v]))
        assert set(rot[v]) == {b if a == v else a for a, b in edges if v in (a, b)}
    darts = {(a, b) for a, b in edges} | {(b, a) for a, b in edges}
    faces = []
    while darts:
        start = min(darts)
        dart = start
        face = []
        while True:
            assert dart in darts
            darts.remove(dart)
            u, v = dart
            face.append(u)
            dart = (v, rot[v][(rot[v].index(u) - 1) % len(rot[v])])
            if dart == start:
                break
        faces.append(face)
    assert len(vertices) - len(edges) + len(faces) == 2
    assert sorted(canonical_face(f) for f in faces) == sorted(canonical_face(f) for f in saved_faces)
    return faces


def check_embedding(edges, embedding):
    disk_faces = verify_rotation(edges, embedding["disk_rotation"], embedding["disk_faces"])
    assert canonical_face(list(range(5))) in [canonical_face(f) for f in disk_faces] or \
        canonical_face(list(reversed(range(5)))) in [canonical_face(f) for f in disk_faces]
    apex = embedding["apex"]
    augmented = edges_of(edges + tuple((i, apex) for i in range(5)))
    verify_rotation(augmented, embedding["augmented_rotation"], embedding["augmented_faces"])
    if "source_file" in embedding:
        assert sha(ROOT / embedding["source_file"]) == embedding["source_sha256"]
        assert embedding["saved_source_sha256_matches"]


def image_key(image):
    return (image["target_sigma"], image["sign"], image["rotation"])


def compare_main(independent):
    base = ROOT / "artifacts/c5_excess_two_c44p"
    catalog_paths = sorted((base / "saved_screen/catalog").glob("*.json"))
    occurrence_paths = sorted((base / "saved_screen/occurrences").glob("*.json"))
    main_catalog = [c for p in catalog_paths for c in json.loads(p.read_text())["catalog"]]
    main_occurrences = [c for p in occurrence_paths for c in json.loads(p.read_text())["occurrences"]]
    own = independent["saved_population"]
    own_cores = {edges_of(c["edges"]): c for c in own["literal_cores"]}
    main_cores = {edges_of(c["edges"]): c for c in main_catalog}
    assert set(own_cores) == set(main_cores) and len(main_catalog) == len(main_cores)
    image_dict = {image_key(i): i for i in IMAGES}
    image_ids = {f'{i["target_sigma"]}:s{i["sign"]}:r{i["rotation"]}': i for i in IMAGES}
    summary_path = base / "saved_screen_summary.json"
    main_summary = json.loads(summary_path.read_text())
    assert len(main_summary["target_images"]) == 20
    for image in main_summary["target_images"]:
        expected = image_dict[(image["target_sigma_mask"], image["s"], image["r"])]
        assert image["image_sigma_mask"] == expected["sigma_mask"]
        assert image["vertex_map"] == expected["frame_map"]
        assert image["row_permutation"] == expected["row_map"]
    main_names = {}
    accepted_witnesses = 0
    rejection_nodes = 0
    failures_checked = 0
    minimality_witnesses_checked = 0
    for edges, main in main_cores.items():
        own_core = own_cores[edges]
        assert main["sigma_mask"] == own_core["sigma_mask"]
        assert main["compatible"] == own_core["compatible"]
        assert main["private_size"] == own_core["private_size"]
        assert main["mixed_components"] == own_core["mixed_components"]
        assert main["occurrence_count"] == own_core["occurrence_count"]
        assert main["root_degrees"] == [4, 4]
        main_names[main["name"]] = edges
        expected_matches = {image_key(i) for i in own_core["matching_images"]}
        reported_matches = set()
        for match in main["matches"]:
            key = (match["target_sigma_mask"], match["s"], match["r"])
            assert key in expected_matches
            expected = image_dict[key]
            assert match["image_sigma_mask"] == expected["sigma_mask"]
            assert match["vertex_map"] == expected["frame_map"]
            reported_matches.add(key)
        assert reported_matches == expected_matches and len(main["matches"]) == len(expected_matches)
        assert len(main["row_decisions"]) == 10
        for idx, decision in enumerate(main["row_decisions"]):
            assert decision["row_index"] == idx and tuple(decision["literal_row"]) == REPS[idx]
            accepted = bool(own_core["sigma_mask"] >> idx & 1)
            assert decision["accepted"] == accepted
            if accepted:
                colouring_ok(edges, REPS[idx], decision["colouring"])
                accepted_witnesses += 1
            else:
                rejection_nodes += verify_rejection_tree(edges, REPS[idx], decision["rejection_tree"])
        failures = main["image_failures"]
        assert len(failures) + len(main["matches"]) == 20
        for failure in failures:
            image = image_ids[failure["image_id"]]
            idx = failure["missing_row_index"]
            assert image["sigma_mask"] >> idx & 1
            assert not own_core["sigma_mask"] >> idx & 1
            assert tuple(failure["missing_literal_row"]) == REPS[idx]
            assert failure["rejection_tree_reference"] == f"/row_decisions/{idx}/rejection_tree"
            failures_checked += 1
        expected_minimality = {(idx, edge) for idx in range(10)
                               if not own_core["sigma_mask"] >> idx & 1
                               for edge in edges if edge not in FRAME}
        actual_minimality = set()
        for witness in main["minimality_witnesses"]:
            idx = witness["row_index"]
            edge = tuple(witness["deleted_edge"])
            assert (idx, edge) in expected_minimality
            assert (idx, edge) not in actual_minimality
            actual_minimality.add((idx, edge))
            colouring_ok(tuple(e for e in edges if e != edge), REPS[idx], witness["colouring"])
            minimality_witnesses_checked += 1
        assert actual_minimality == expected_minimality
        check_embedding(edges, main["embedding"])
    own_occ = {(x["input_chunk"], x["input_pointer"]): x for x in own["occurrences"]}
    reported_occ = {(x["input_chunk"], x["input_pointer"]): x for x in main_occurrences}
    assert set(own_occ) == set(reported_occ) and len(main_occurrences) == len(reported_occ)
    for key, expected in own_occ.items():
        actual = reported_occ[key]
        assert main_names[actual["core_name"]] == edges_of(expected["edge_key"])
        assert actual["saved_sigma_mask"] == expected["saved_sigma_mask"]
        assert actual["recomputed_sigma_mask"] == expected["sigma_mask"]
        assert actual["compatible"] == expected["compatible"]
        assert actual["source_metadata"]["type"] == expected["source_type"]
        assert actual["source_metadata"]["critical"] == expected["critical"]
        core = main_cores[edges_of(expected["edge_key"])]
        assert actual["matches"] == core["matches"]
        assert actual["image_failures"] == core["image_failures"]
    two_path = base / "two_private.json"
    main_two = json.loads(two_path.read_text())
    assert main_two["target_images"] == [dict(i, accepted_rows=[r for r in range(10)
                                          if i["sigma_mask"] >> r & 1]) for i in IMAGES]
    own_placements = {p["id"]: p for p in independent["two_private"]}
    main_placements = {p["id"]: p for p in main_two["placements"]}
    assert set(own_placements) == set(main_placements) and len(main_two["placements"]) == 125
    small_witnesses = 0
    minimal_sets_checked = 0
    for ident, own_p in own_placements.items():
        main_p = main_placements[ident]
        edges = edges_of(own_p["edges"])
        assert edges == edges_of(main_p["edges"])
        assert main_p["sigma_mask"] == own_p["sigma_mask"]
        assert main_p["disk"]["embeddable"] == own_p["disk"]["embeddable"]
        if own_p["disk"]["embeddable"]:
            check_embedding(edges, main_p["disk"]["embedding"])
        assert main_p["rejected_rows"] == own_p["rejected_rows"]
        assert main_p["whole_graph_minimal_rejected_rows"] == own_p["whole_graph_minimal_rejected_rows"]
        assert main_p["compatibility"]["compatible"] == own_p["compatible"]
        assert main_p["orbit"]["size"] == own_p["orbit_size"]
        assert main_p["orbit"]["stabilizer_size"] == own_p["stabilizer_size"]
        canonical_id = main_p["orbit"]["canonical_id"]
        canonical = own_placements[canonical_id]
        assert canonical["orbit_canonical_spokes"] == own_p["orbit_canonical_spokes"]
        element = main_p["orbit"]["canonical_group_element"]
        mapped = [[(element["sign"] * i + element["rotation"]) % 5
                   for i in own_p["spokes"][root]] for root in ("5", "6")]
        mapped = [sorted(a) for a in mapped]
        if element["root_swap"]:
            mapped.reverse()
        assert mapped == [canonical["spokes"][root] for root in ("5", "6")]
        expected_images = {image_key(i) for i in own_p["matching_images"]}
        actual_images = {image_key(i) for i in main_p["compatibility"]["matching_images"]}
        assert expected_images == actual_images
        for image in main_p["compatibility"]["matching_images"]:
            expected = image_dict[image_key(image)]
            assert all(image[k] == expected[k] for k in ("sigma_mask", "frame_map", "row_map"))
        for exclusion in main_p["compatibility"]["exclusions"]:
            expected = image_dict[image_key(exclusion)]
            assert all(exclusion[k] == expected[k] for k in ("sigma_mask", "frame_map", "row_map"))
            idx = exclusion["missing_row_index"]
            assert expected["sigma_mask"] >> idx & 1
            assert not own_p["sigma_mask"] >> idx & 1
            verify_small_rejection(edges, REPS[idx], exclusion["rejection_witness"])
            small_witnesses += 1
        row_min = {x["row_index"]: x["minimal_core_edge_sets"]
                   for x in own_p["minimal_core_enumeration"]}
        deleted_masks = {tuple(x["edge"]): x["sigma_mask"] for x in own_p["edge_deletion_masks"]}
        assert len(main_p["rows"]) == 10
        assert [row["row_index"] for row in main_p["rows"]] == list(range(10))
        for row in main_p["rows"]:
            idx = row["row_index"]
            assert tuple(row["literal_row"]) == REPS[idx]
            assert row["accepted"] == bool(own_p["sigma_mask"] >> idx & 1)
            if row["accepted"]:
                expected_pairs = [list(pair) for pair in product(range(4), repeat=2)
                                  if all((REPS[idx] + pair)[u] != (REPS[idx] + pair)[v]
                                         for u, v in edges)]
                assert row["accepted_root_pairs"] == expected_pairs
                colouring_ok(edges, REPS[idx], row["accepted_witness"])
                small_witnesses += 1
                continue
            verify_small_rejection(edges, REPS[idx], row["rejection_witness"])
            small_witnesses += 1
            assert sorted(c["edges"] for c in row["minimal_cores"]) == row_min[idx]
            minimal_sets_checked += len(row_min[idx])
            for deletion in row["edge_deletion_audit"]:
                edge = tuple(deletion["edge"])
                expected_accept = bool(deleted_masks[edge] >> idx & 1)
                assert deletion["accepted"] == expected_accept
                deleted = tuple(e for e in edges if e != edge)
                if expected_accept:
                    colouring_ok(deleted, REPS[idx], deletion["accepted_witness"])
                else:
                    verify_small_rejection(deleted, REPS[idx], deletion["rejection_witness"])
                small_witnesses += 1
            for core in row["minimal_cores"]:
                core_edges = edges_of(core["edges"])
                verify_small_rejection(core_edges, REPS[idx], core["rejection_witness"])
                small_witnesses += 1
                for deletion in core["edge_deletion_witnesses"]:
                    deleted = tuple(e for e in core_edges if e != tuple(deletion["edge"]))
                    colouring_ok(deleted, REPS[idx], deletion["accepted_witness"])
                    small_witnesses += 1
    named_path = base / "named_C44P-AD2-012-034.json"
    named = json.loads(named_path.read_text())
    named_edges = edges_of(named["placement"]["edges"])
    assert named_edges == edges_of(own_placements["AD-012-034"]["edges"])
    assert named["placement"] == main_placements["AD-012-034"]
    inputs = catalog_paths + occurrence_paths + [two_path, named_path,
                                                  base / "saved_screen_summary.json"]
    return {"schema_version": 1,
            "main_inputs": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p)} for p in inputs],
            "comparison": {"occurrences": len(main_occurrences), "literal_cores": len(main_catalog),
                           "placements": len(main_placements), "mismatches": 0,
                           "mismatch_details": [],
                           "saved_screen_accepted_witnesses_checked": accepted_witnesses,
                           "saved_screen_rejection_tree_nodes_checked": rejection_nodes,
                           "saved_screen_failed_image_rows_checked": failures_checked,
                           "saved_screen_minimality_witnesses_checked": minimality_witnesses_checked,
                           "saved_screen_rotation_certificates_checked": len(main_catalog),
                           "two_private_witnesses_checked": small_witnesses,
                           "two_private_minimal_core_sets_checked": minimal_sets_checked}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare regenerated deterministic bytes")
    args = parser.parse_args()
    result = build()
    result["main_comparison"] = compare_main(result)
    encoded = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
    if args.check:
        assert OUT.read_bytes() == encoded, "independent JSON byte replay differs"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("xb") as stream:
            stream.write(encoded)
    print(json.dumps({"summary": result.get("summary", result.get("comparison")), "sha256": hashlib.sha256(encoded).hexdigest()},
                     sort_keys=True))


if __name__ == "__main__":
    main()
