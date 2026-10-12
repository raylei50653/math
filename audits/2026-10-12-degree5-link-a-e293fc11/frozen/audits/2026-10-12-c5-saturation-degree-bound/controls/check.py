#!/usr/bin/env python3
"""Replay the finite controls from a frozen catalogue; no research closure claim.

Python 3.11+ and NetworkX 3.5 or 3.6.x are required.  Run from any directory:
  python controls/check.py --write controls/certificate.json
  python controls/check.py --check controls/certificate.json [--seed 17]

--write creates a new file exclusively. --check is read-only and compares every
field and lift, including empty fibres. Seed changes only the independent search
route, so every successful replay has identical certificate bytes.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys

import networkx as nx

HERE = Path(__file__).resolve().parent
CATALOGUE = HERE.parent / "frozen" / "cells.json"
CATALOGUE_SHA256 = "04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8"
COLORS = tuple(range(4))
B5 = tuple(range(5))
B4 = (0, 2, 3, 4)
C5_EDGES = {tuple(sorted((i, (i + 1) % 5))) for i in B5}
C4_EDGES = {tuple(sorted((B4[i], B4[(i + 1) % 4]))) for i in range(4)}

# Literal disk embeddings, independent of a library's embedding choice.
C4_FACES = {
    7: [(0, 4, 5), (0, 5, 2), (2, 5, 3), (3, 5, 4)],
    10: [(0, 2, 4), (2, 3, 4)],
    11: [(0, 4, 5), (0, 5, 6), (0, 6, 2), (2, 6, 3), (3, 5, 4), (3, 6, 5)],
    12: [(0, 3, 2), (0, 4, 3)],
    13: [(0, 4, 6), (0, 6, 2), (2, 5, 3), (2, 6, 5), (3, 5, 4), (4, 5, 6)],
    14: [(0, 4, 5), (0, 5, 7), (0, 7, 2), (2, 6, 3), (2, 7, 6), (3, 6, 5, 4), (5, 6, 7)],
    15: [(0, 4, 3, 2)],
}
DEGREE4_EXTRA = {(2, 4), (0, 5), (0, 7), (1, 6), (1, 7), (2, 5), (2, 6), (4, 5), (5, 6), (5, 7), (6, 7)}
DEGREE4_FACES = [(0, 1, 7), (0, 7, 5), (1, 6, 7), (1, 2, 6), (2, 5, 4), (2, 6, 5), (5, 7, 6), (0, 5, 4), (2, 4, 3)]
QUOTIENT_FACES = {
    "H_06": [(0, 2, 1), (0, 4, 5), (0, 5, 2), (2, 4, 3), (2, 5, 4)],
    "H_15": [(0, 1, 4), (1, 2, 6), (1, 6, 2, 4), (2, 3, 4)],
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(data):
    return json.loads(data, object_pairs_hook=no_duplicate_keys)


def normalize(colors):
    names = {}
    return tuple(names.setdefault(color, len(names)) for color in colors)


def boundaries(length):
    return [b for b in itertools.product(COLORS, repeat=length)
            if all(b[i] != b[(i + 1) % length] for i in range(length))]


ALL4, ALL5 = boundaries(4), boundaries(5)
REPS4, REPS5 = sorted({normalize(b) for b in ALL4}), sorted({normalize(b) for b in ALL5})


def brute(vertices, edges, boundary_vertices, boundary_colors):
    inner = sorted(set(vertices) - set(boundary_vertices))
    result = []
    for values in itertools.product(COLORS, repeat=len(inner)):
        coloring = dict(zip(boundary_vertices, boundary_colors))
        coloring.update(zip(inner, values))
        if all(coloring[u] != coloring[v] for u, v in edges):
            result.append(values)
    return result


def backtrack(vertices, edges, boundary_vertices, boundary_colors, seed):
    """Independent constraint route, with seed-dependent ties and color order."""
    inner = sorted(set(vertices) - set(boundary_vertices))
    adjacent = {v: set() for v in vertices}
    for u, v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    coloring = dict(zip(boundary_vertices, boundary_colors))
    if any(u in coloring and v in coloring and coloring[u] == coloring[v] for u, v in edges):
        return []
    rng = random.Random(seed)
    result = []

    def visit():
        remaining = [v for v in inner if v not in coloring]
        if not remaining:
            result.append(tuple(coloring[v] for v in inner))
            return
        palettes = {v: [c for c in COLORS if all(coloring.get(w) != c for w in adjacent[v])]
                    for v in remaining}
        rng.shuffle(remaining)
        v = min(remaining, key=lambda w: (len(palettes[w]), -len(adjacent[w])))
        rng.shuffle(palettes[v])
        for color in palettes[v]:
            coloring[v] = color
            visit()
            del coloring[v]

    visit()
    return sorted(result)


def sigma(fibres):
    return sum(1 << i for i, fibre in enumerate(fibres) if fibre)


def row_record(patterns, fibres):
    return [{"index": i, "boundary_colors": b, "count": len(f), "lifts": f}
            for i, (b, f) in enumerate(zip(patterns, fibres))]


def rotate_face(face):
    return min(tuple(face[i:] + face[:i]) for i in range(len(face)))


def oriented_disk_faces(vertices, edges, boundary, faces):
    """Check a literal orientable sphere embedding with the named exterior face.

    Besides edge incidences and Euler, check the rotation at each vertex is one
    cycle. This rules out a list of facial walks glued with a pinched vertex.
    """
    remaining = sorted(tuple(f) for f in faces)
    oriented = [tuple(boundary)]
    while remaining:
        used = {(u, v) for f in oriented for u, v in zip(f, f[1:] + f[:1])}
        for i, face in enumerate(remaining):
            arcs = list(zip(face, face[1:] + face[:1]))
            shared = [(u, v) for u, v in arcs if (u, v) in used or (v, u) in used]
            if not shared:
                continue
            same = any((u, v) in used for u, v in shared)
            reverse = any((v, u) in used for u, v in shared)
            require(not (same and reverse), "incoherent face orientations")
            oriented.append(tuple(reversed(face)) if same else face)
            remaining.pop(i)
            break
        else:
            raise ValueError("face adjacency is disconnected")
    interior = sorted(rotate_face(f) for f in oriented[1:])
    oriented = [tuple(boundary)] + interior
    arcs = [(u, v) for f in oriented for u, v in zip(f, f[1:] + f[:1])]
    require(len(arcs) == 2 * len(edges) and len(set(arcs)) == len(arcs), "face darts are incomplete or duplicated")
    require(set(arcs) == {(u, v) for a, b in edges for u, v in ((a, b), (b, a))}, "face edges differ from graph")
    require(len(vertices) - len(edges) + len(oriented) == 2, "embedding Euler characteristic is not two")
    for face in oriented:
        require(len(face) >= 3 and len(set(face)) == len(face), "face is not a simple cycle")
    rotations = {}
    for v in sorted(vertices):
        following = {}
        for face in oriented:
            if v in face:
                i = face.index(v)
                previous, successor = face[i - 1], face[(i + 1) % len(face)]
                require(previous not in following, "vertex rotation repeats a predecessor")
                following[previous] = successor
        neighbors = {w for e in edges if v in e for w in e if w != v}
        require(set(following) == neighbors and set(following.values()) == neighbors, "vertex rotation omits a neighbor")
        require(bool(neighbors), "isolated vertex in disk")
        first = min(neighbors)
        cycle, current = [], first
        while current not in cycle:
            cycle.append(current)
            current = following[current]
        require(current == first and set(cycle) == neighbors, "pinched vertex rotation")
        rotations[str(v)] = cycle
    return {"oriented_faces_outer_first": oriented, "vertex_rotations": rotations,
            "simple_faces": True, "all_directed_edges_once": True, "Euler_characteristic": 2}


def apex_planar(vertices, edges, boundary):
    graph = nx.Graph()
    graph.add_nodes_from(sorted(vertices))
    graph.add_edges_from(sorted(edges))
    apex = max(vertices) + 1
    graph.add_edges_from((apex, v) for v in boundary)
    return nx.check_planarity(graph)[0]


def disk_record(vertices, edges, boundary, faces):
    require(set(boundary) <= set(vertices), "missing named boundary vertex")
    boundary_edges = {tuple(sorted((boundary[i], boundary[(i + 1) % len(boundary)])))
                      for i in range(len(boundary))}
    require(boundary_edges <= edges, "missing boundary cycle edge")
    require(all(u < v and u in vertices and v in vertices for u, v in edges), "invalid simple graph edge")
    embedding = oriented_disk_faces(vertices, edges, boundary, faces)
    require(apex_planar(vertices, edges, boundary), "apex graph is nonplanar")
    apex = max(vertices) + 1
    apex_faces = embedding["oriented_faces_outer_first"][1:] + [
        (boundary[i], boundary[(i + 1) % len(boundary)], apex) for i in range(len(boundary))]
    apex_edges = edges | {tuple(sorted((apex, v))) for v in boundary}
    # Independently validate the explicitly filled apex sphere. Any face can be
    # treated as its exterior for this combinatorial embedding check.
    apex_embedding = oriented_disk_faces(set(vertices) | {apex}, apex_edges, apex_faces[0], apex_faces[1:])
    return {"vertices": sorted(vertices), "edges": sorted(edges), "named_boundary": boundary,
            "interior_order": sorted(set(vertices) - set(boundary)), "disk_embedding": embedding,
            "apex": {"label": apex, "edges": sorted(apex_edges), "planar": True,
                     "explicit_sphere_embedding": apex_embedding}}


def verify_fibres(vertices, edges, boundary, all_assignments, patterns, seed):
    representative_fibres = [brute(vertices, edges, boundary, b) for b in patterns]
    bits = sigma(representative_fibres)
    assigned_fibres = []
    for b in all_assignments:
        direct = brute(vertices, edges, boundary, b)
        independent = backtrack(vertices, edges, boundary, b, seed)
        require(direct == independent, "full direct/backtracking fibres differ")
        require(bool(direct) == bool(bits >> patterns.index(normalize(b)) & 1), "global S4 orbit test failed")
        assigned_fibres.append(direct)
    return {"sigma_bits": bits, "representative_rows": row_record(patterns, representative_fibres),
            "all_boundary_rows": row_record(all_assignments, assigned_fibres),
            "independent_routes": {"direct_product": True, "constraint_backtracking": True,
                                   "compared_complete_lifts_including_empty_fibres": True,
                                   "boundary_assignments_checked": len(all_assignments), "global_S4_orbits_checked": True}}


def c4_control(catalogue, seed):
    pattern_map = []
    for i, b in enumerate(REPS5):
        allowed = b[0] != b[2]
        smaller = normalize(tuple(b[v] for v in B4)) if allowed else None
        pattern_map.append({"c5_index": i, "c5_pattern": b, "chord_02_permits": allowed,
                            "c4_pattern": smaller, "c4_index": REPS4.index(smaller) if allowed else None})
    mask_map, witnesses = [], []
    for mask in range(16):
        lifted = sum(1 << r["c5_index"] for r in pattern_map
                     if r["chord_02_permits"] and mask >> r["c4_index"] & 1)
        entry = catalogue["cells"].get(str(lifted))
        mask_map.append({"c4_mask": mask, "lifted_c5_mask": lifted, "in_catalogue": entry is not None,
                         "catalogue_k_eff": entry["k_eff"] if entry else None})
        if entry is None:
            continue
        edges5 = C5_EDGES | {tuple(sorted(e)) for e in entry["edges"]}
        vertices5 = {v for edge in edges5 for v in edge}
        require({v for e in edges5 if 1 in e for v in e if v != 1} == {0, 2}, "dummy has extra attachment")
        require((0, 2) in edges5, "original C4 edge was lost")
        vertices4, edges4 = vertices5 - {1}, {e for e in edges5 if 1 not in e}
        require(C4_EDGES <= edges4, "C4 boundary missing")
        require(len(vertices4 - set(B4)) == entry["k_eff"] <= 3, "C4 interior bound failed")
        graph4 = disk_record(vertices4, edges4, B4, C4_FACES[mask])
        graph5 = disk_record(vertices5, edges5, B5, C4_FACES[mask] + [(0, 1, 2)])
        graph4.update(verify_fibres(vertices4, edges4, B4, ALL4, REPS4, seed))
        graph5.update(verify_fibres(vertices5, edges5, B5, ALL5, REPS5, seed))
        require(graph4["sigma_bits"] == mask and graph5["sigma_bits"] == lifted, "C4/C5 mask mismatch")
        # Dummy is a named boundary vertex in C5; all remaining lift labels and
        # coordinates are identical. Check literal equality for all 240 rows.
        for row in graph5["all_boundary_rows"]:
            b = row["boundary_colors"]
            smaller = tuple(b[v] for v in B4)
            expected = brute(vertices4, edges4, B4, smaller) if b[0] != b[2] else []
            require(row["lifts"] == expected, "deleting the dummy changed a full fibre")
        witnesses.append({"c4_mask": mask, "c5_mask": lifted, "dummy_label": 1, "dummy_neighbors": [0, 2],
                          "interior_count": entry["k_eff"], "C4": graph4, "augmented_C5": graph5,
                          "literal_full_fibre_dummy_deletion_checked_on_all_240_rows": True})
    require([w["c4_mask"] for w in witnesses] == [7, 10, 11, 12, 13, 14, 15], "C4 mask set changed")
    return {"class": "named C4 disk, augmented C5=(0,1,2,3,4), C4=(0,2,3,4), chord02 retained",
            "universal_premise": "The external published C5 necessary screen puts realizable chorded-C5 relations in the catalogue; these finite controls do not prove it.",
            "C4_pattern_order": REPS4, "C5_pattern_order": REPS5, "full_pattern_map": pattern_map,
            "all_16_mask_map": mask_map, "witnesses": witnesses,
            "summary": {"possible_C4_masks_under_external_premise": [7, 10, 11, 12, 13, 14, 15],
                        "maximum_witness_interiors": max(w["interior_count"] for w in witnesses),
                        "C4_assignments_per_witness": 84, "C5_assignments_per_witness": 240}}


def degree4_control(catalogue, seed):
    edges = C5_EDGES | DEGREE4_EXTRA
    vertices = set(range(8))
    graphs = {"G": disk_record(vertices, edges, B5, DEGREE4_FACES)}
    graphs["G"].update(verify_fibres(vertices, edges, B5, ALL5, REPS5, seed))
    branches, lifts = {}, {}
    for name, gone, keep in [("H_06", 6, 0), ("H_15", 5, 1)]:
        vs = vertices - {7, gone}
        es = set()
        for u, v in edges:
            if 7 in (u, v):
                continue
            u, v = (keep if u == gone else u), (keep if v == gone else v)
            require(u != v, "quotient produces a loop")
            es.add(tuple(sorted((u, v))))
        require(C5_EDGES <= es, "quotient changes boundary cycle")
        graph = disk_record(vs, es, B5, QUOTIENT_FACES[name])
        graph.update(verify_fibres(vs, es, B5, ALL5, REPS5, seed))
        graph["quotient"] = {"delete_center": 7, "identify": [gone, keep], "retain_label": keep}
        graphs[name] = graph
        original_branches, branch_lifts = [], []
        for row, qrow in zip(graphs["G"]["all_boundary_rows"], graph["all_boundary_rows"]):
            boundary = row["boundary_colors"]
            original_branch = [f for f in row["lifts"] if f[gone - 5] == boundary[keep]]
            records = []
            for qf in qrow["lifts"]:
                coloring = dict(zip(B5, boundary))
                coloring.update(zip(graph["interior_order"], qf))
                coloring[gone] = coloring[keep]
                for color in COLORS:
                    coloring[7] = color
                    if all(coloring[u] != coloring[v] for u, v in edges):
                        records.append({"quotient_lift": qf, "original_lift": tuple(coloring[v] for v in range(5, 8))})
            restored = sorted(r["original_lift"] for r in records)
            require(restored == original_branch, "full quotient lift failed")
            original_branches.append(original_branch)
            branch_lifts.append({"boundary_colors": boundary, "lifts": records})
        branches[name] = original_branches
        lifts[name] = branch_lifts
    for i, row in enumerate(graphs["G"]["all_boundary_rows"]):
        require(set(branches["H_06"][i]) | set(branches["H_15"][i]) == set(row["lifts"]), "degree4 same-row union failed")
    require([graphs[n]["sigma_bits"] for n in ("G", "H_06", "H_15")] == [429, 424, 165], "degree4 masks changed")
    require(424 | 165 == 429 and 424 != 429 and 165 != 429, "degree4 strict branch union failed")
    require(catalogue["cells"]["429"]["k_eff"] == 3, "catalogue k_eff(429) changed")
    require(len(edges) == 3 * 3 + 7 and len(DEGREE4_FACES) == 2 * 3 + 3, "degree4 triangulation count failed")
    face_counts = Counter(tuple(sorted(e)) for f in DEGREE4_FACES for e in zip(f, f[1:] + f[:1]))
    require(all(face_counts[e] == (1 if e in C5_EDGES else 2) for e in edges), "degree4 face counts failed")
    return {"class": "simple plane disk with named C5; boundary chords allowed",
            "graphs": graphs, "degree4_center": 7, "cyclic_link": [0, 1, 6, 5],
            "all_240_original_branch_fibres": {name: row_record(ALL5, fs) for name, fs in branches.items()},
            "all_240_explicit_quotient_lifts": lifts,
            "same_original_row_full_union_checked_including_empties": True,
            "exclusive_rows": {"only_H_06": [i for i in range(10) if (424 & ~165) >> i & 1],
                               "only_H_15": [i for i in range(10) if (165 & ~424) >> i & 1]},
            "catalogue_key429_minimum_k_eff_observed": 3,
            "saturation_reason": "All nine internal faces are triangular, so no simple edge can be added within the fixed disk.",
            "scope": "This finite example refutes retaining one quotient branch; it does not refute union-based reduction or prove the universal degree bound."}


def octahedral_control(seed):
    vertices = set(range(11))
    edges = C5_EDGES | {(0, 2)}
    faces = [(0, 1, 2), (0, 2, 3, 4)]
    patches, old = [], 2
    for i in range(2):
        a, b, c = 5 + 3 * i, 6 + 3 * i, 7 + 3 * i
        patch_vertices = (0, 1, old, a, b, c)
        opposite = {tuple(sorted(e)) for e in [(0, a), (1, b), (old, c)]}
        edges.update(tuple(sorted(e)) for e in itertools.combinations(patch_vertices, 2)
                     if tuple(sorted(e)) not in opposite)
        faces.remove((0, 1, old))
        added_faces = [(0, 1, c), (0, old, b), (1, old, a), (0, b, c), (1, a, c), (old, a, b), (a, b, c)]
        faces.extend(added_faces)
        patches.append({"outer": [0, 1, old], "inner": [a, b, c], "opposite_pairs": sorted(opposite), "faces": added_faces})
        old = c
    graph = disk_record(vertices, edges, B5, faces)
    # Ten representatives suffice here; all complete six-coordinate fibres are
    # independently enumerated. The C4/degree4 controls separately check every
    # labelled boundary assignment, as recorded in their certificates.
    graph.update(verify_fibres(vertices, edges, B5, REPS5, REPS5, seed))
    require(graph["sigma_bits"] == 1016, "octahedral base mask changed")
    require([r["count"] for r in graph["representative_rows"]] == [0, 0, 0, 16, 16, 16, 16, 16, 16, 16], "octahedral fibres changed")
    cofacial = sorted({tuple(sorted((u, v))) for f in faces for u, v in itertools.combinations(f, 2)
                      if tuple(sorted((u, v))) not in edges})
    require(cofacial == [(0, 3), (2, 4)], "fixed embedding admissible edges changed")
    candidates, additions = [], []
    for edge in itertools.combinations(sorted(vertices), 2):
        if edge in edges:
            continue
        planar = apex_planar(vertices, edges | {edge}, B5)
        candidates.append({"edge": edge, "apex_planar": planar, "fixed_embedding_cofacial": edge in cofacial})
        if not planar:
            continue
        result = verify_fibres(vertices, edges | {edge}, B5, REPS5, REPS5, seed)
        result.update({"edge": edge, "removed_bits": 1016 & ~result["sigma_bits"]})
        # Explicit disk embedding after splitting the only quadrilateral.
        require(edge in cofacial, "re-embedding admits an unexpected edge")
        split = [(0, 2, 3), (0, 3, 4)] if edge == (0, 3) else [(0, 2, 4), (2, 3, 4)]
        result["disk"] = disk_record(vertices, edges | {edge}, B5, [f for f in faces if len(f) == 3] + split)
        additions.append(result)
    require(len(candidates) == 31, "not every octahedral nonedge was checked")
    require([c["edge"] for c in candidates if c["apex_planar"]] == cofacial, "abstract disk additions differ from embedding additions")
    require([a["sigma_bits"] for a in additions] == [960, 424], "octahedral addition masks changed")
    require(all(a["removed_bits"] for a in additions), "octahedral saturation failed")
    interior_edges = {e for e in edges if e[0] >= 5}
    cycles = []
    for cycle in itertools.permutations(range(5, 11), 5):
        if cycle[0] != min(cycle) or cycle[1] > cycle[-1]:
            continue
        if all(tuple(sorted(e)) in interior_edges for e in zip(cycle, cycle[1:] + cycle[:1])):
            cycles.append(cycle)
    require(not cycles, "octahedral interior C5 countercontrol failed")
    degrees = {str(v): sum(v in e for e in edges) for v in range(5, 11)}
    require(min(degrees.values()) >= 4 and len(edges) == 24 and len(faces) == 14, "octahedral geometry changed")
    return {"graph": graph, "octahedron_patches": patches, "k": 6, "E": len(edges),
            "internal_face_count": len(faces), "triangle_count": 13, "quadrilateral_count": 1,
            "interior_degree": degrees, "interior_induced_edges": sorted(interior_edges),
            "all_interior_C5": cycles, "all_31_nonedge_candidates": candidates,
            "admissible_fixed_embedding_nonedges": cofacial, "admissible_abstract_disk_nonedges": cofacial,
            "additions": additions, "sigma_saturated": True,
            "scope": "Finite k=6 saturation countercontrol has no wholly interior C5. An arbitrary-size family requires the separate paper argument."}


def replay(seed):
    version = tuple(int(part) for part in nx.__version__.split(".")[:2])
    require(version in {(3, 5), (3, 6)}, "NetworkX 3.5 or 3.6.x is required")
    require(len(ALL4) == 84 and len(ALL5) == 240 and len(REPS4) == 4 and len(REPS5) == 10, "boundary enumeration changed")
    data = CATALOGUE.read_bytes()  # Missing frozen input fails before any output.
    require(hashlib.sha256(data).hexdigest() == CATALOGUE_SHA256, "frozen catalogue SHA256 differs")
    catalogue = read_json(data)
    require(catalogue["pattern_order"] == [list(b) for b in REPS5], "catalogue named pattern order differs")
    require(len(catalogue["cells"]) == 132, "catalogue is incomplete")
    return {"schema": "c5-saturation-degree-controls-v1",
            "source": {"catalogue_relative_to_audit": "frozen/cells.json", "catalogue_sha256": CATALOGUE_SHA256,
                       "catalogue_bytes": len(data), "catalogue_masks": 132},
            "replay_contract": {"colors": COLORS, "C5_pattern_order": REPS5, "C4_pattern_order": REPS4,
                                "complete_lifts_including_empties": True, "certificate_is_seed_invariant": True,
                                "planarity_algorithm_requirement": "NetworkX 3.5 or 3.6.x; only invariant truth values are recorded",
                                "scope": "Finite controls only; external screen, universal normal-form proof, and Lean are separate."},
            "C4_bound3": c4_control(catalogue, seed),
            "degree4_two_branch_union": degree4_control(catalogue, seed),
            "octahedral_saturation": octahedral_control(seed)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path, help="exclusively create the canonical certificate")
    mode.add_argument("--check", type=Path, help="read-only complete certificate comparison")
    parser.add_argument("--seed", type=int, default=0, help="independent search ordering; no effect on certificate")
    args = parser.parse_args()
    try:
        expected = canonical_bytes(replay(args.seed))
        path = args.write or args.check
        if args.write:
            with path.open("xb") as output:
                output.write(expected)
            action = "wrote"
        else:
            actual = path.read_bytes()
            # Parse first to reject duplicate keys, then require the entire
            # canonical payload. A lost/modified empty fibre cannot pass.
            require(read_json(actual) == read_json(expected), "certificate payload differs from complete replay")
            require(actual == expected, "certificate is not the canonical deterministic byte encoding")
            action = "checked"
        print(f"PASS: {action} {path}; SHA256={hashlib.sha256(expected).hexdigest()}; complete fibres and embeddings match")
        return 0
    except (ValueError, KeyError, OSError, TypeError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
