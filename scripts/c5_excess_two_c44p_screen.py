#!/usr/bin/env python3
"""Recompute and screen all saved C44 two-root (4,4) occurrences.

No C44 colouring, core-search, or group-action implementation is imported.
An accepted row has a complete colouring; a rejected row has a complete
four-way decision tree with one conflicting edge for every pruned branch.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "artifacts/c5_excess_two_c44/orbits"
OUTPUT = ROOT / "artifacts/c5_excess_two_c44p"
FRAME = {(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)}


def normalize(row):
    colours = {}
    return tuple(colours.setdefault(c, len(colours)) for c in row)


REPS = tuple(sorted({normalize(row) for row in product(range(4), repeat=5)
                     if all(row[i] != row[(i + 1) % 5] for i in range(5))}))
assert len(REPS) == 10


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def literal_graph(edges):
    result = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    assert len(set(result)) == len(result)
    assert FRAME <= set(result)
    assert {edge for edge in result if edge[1] < 5} == FRAME
    return result


def full_decision(edges, row):
    """Exact DFS, fixed literal boundary colours, complete rejection tree.

    At a node choose the uncoloured vertex with the fewest available colours.
    For each of all four colours, either record a conflict with an already
    coloured neighbour or recursively visit that branch. Thus rejection is
    covered exhaustively, including initially impossible boundary lists.
    """
    vertices = sorted({v for edge in edges for v in edge})
    adjacency = {v: [] for v in vertices}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    for neighbours in adjacency.values():
        neighbours.sort()
    assignment = {v: row[v] for v in range(5)}
    states = 0

    def available(v):
        used = {assignment[w] for w in adjacency[v] if w in assignment}
        return [c for c in range(4) if c not in used]

    def visit():
        nonlocal states
        states += 1
        remaining = [v for v in vertices if v not in assignment]
        if not remaining:
            return {str(v): assignment[v] for v in vertices}, None
        v = min(remaining, key=lambda w: (len(available(w)), w))
        branches = []
        for colour in range(4):
            blockers = [w for w in adjacency[v]
                        if assignment.get(w, -1) == colour]
            if blockers:
                branches.append({"colour": colour, "conflict_edge": sorted([v, blockers[0]])})
                continue
            assignment[v] = colour
            witness, subtree = visit()
            del assignment[v]
            if witness is not None:
                return witness, None
            branches.append({"colour": colour, "child": subtree})
        return None, {"vertex": v, "branches": branches}

    witness, rejection = visit()
    result = {"accepted": witness is not None, "states": states}
    if witness is not None:
        assert all(witness[str(u)] != witness[str(v)] for u, v in edges)
        assert tuple(witness[str(v)] for v in range(5)) == row
        result["colouring"] = witness
    else:
        assert verify_rejection_tree(edges, row, rejection)
        result["rejection_tree"] = rejection
    return result


def verify_rejection_tree(edges, row, tree):
    """Check a tree's coverage and each literal conflict, without DFS search."""
    adjacency = defaultdict(set)
    vertices = {v for edge in edges for v in edge}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colours = {v: row[v] for v in range(5)}

    def verify(node):
        v = node["vertex"]
        assert v in vertices and v not in colours
        branches = node["branches"]
        assert [b["colour"] for b in branches] == list(range(4))
        for branch in branches:
            colour = branch["colour"]
            if "conflict_edge" in branch:
                u, w = branch["conflict_edge"]
                assert v in (u, w)
                neighbour = w if u == v else u
                assert neighbour in adjacency[v] and colours[neighbour] == colour
            else:
                assert all(colours.get(w, -1) != colour for w in adjacency[v])
                colours[v] = colour
                verify(branch["child"])
                del colours[v]

    verify(tree)
    return True


def target_images():
    result = []
    for target in (933, 941):
        for s in (1, -1):
            for r in range(5):
                mapping = [(s * i + r) % 5 for i in range(5)]
                permutation = []
                for row in REPS:
                    moved = [None] * 5
                    for i in range(5):
                        moved[mapping[i]] = row[i]
                    permutation.append(REPS.index(normalize(moved)))
                rows = sorted(permutation[i] for i in range(10) if target & (1 << i))
                result.append({"image_id": f"{target}:s{s}:r{r}",
                               "target_sigma_mask": target,
                               "image_sigma_mask": sum(1 << i for i in rows),
                               "accepted_rows": rows, "s": s, "r": r,
                               "vertex_map": mapping, "row_permutation": permutation})
    return result


def mixed_components(edges):
    private = {v for edge in edges for v in edge if v >= 5} - {5, 6}
    adjacency = defaultdict(set)
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    result = []
    while private:
        start = min(private)
        component, todo = set(), [start]
        while todo:
            v = todo.pop()
            if v in component:
                continue
            component.add(v)
            todo.extend(sorted((adjacency[v] & private) - component, reverse=True))
        private -= component
        owners = [root for root in (5, 6)
                  if any(root in adjacency[v] for v in component)]
        if owners == [5, 6]:
            result.append({"vertices": sorted(component), "owners": owners})
    return result


def faces_from_rotation(rotation):
    rotation = {int(v): list(ws) for v, ws in rotation.items()}
    unvisited = {(v, w) for v, ws in rotation.items() for w in ws}
    faces = []
    while unvisited:
        start = min(unvisited)
        dart, face = start, []
        while True:
            assert dart in unvisited
            unvisited.remove(dart)
            u, v = dart
            face.append(u)
            neighbours = rotation[v]
            dart = (v, neighbours[(neighbours.index(u) - 1) % len(neighbours)])
            if dart == start:
                break
        faces.append(face)
    return faces


def inherited_embedding(edges, occurrence, source_cache):
    source_path = occurrence["source_metadata"]["source_file"]
    if source_path not in source_cache:
        source_bytes = (ROOT / source_path).read_bytes()
        data = json.loads(source_bytes)
        source_cache[source_path] = {
            "sha256": sha256(source_bytes).hexdigest(),
            "records": {record["code"]: (i, record)
                        for i, record in enumerate(data["q_orbits"])}}
    actual_source_sha256 = source_cache[source_path]["sha256"]
    assert actual_source_sha256 == occurrence["source_metadata"]["source_sha256"]
    index, source = source_cache[source_path]["records"][occurrence["source_metadata"]["code"]]
    source_edges = literal_graph(source["canonical_edges"])
    assert set(edges) <= set(source_edges)
    vertices = sorted({v for edge in edges for v in edge})
    apex = 5 + occurrence["source_metadata"]["k"]
    augmented_edges = set(edges) | {tuple(sorted((i, apex))) for i in range(5)}
    rotation = {}
    for v in sorted(vertices + [apex]):
        rotation[str(v)] = [w for w in source["augmented_rotation"][str(v)]
                            if tuple(sorted((v, w))) in augmented_edges]
    assert {(min(int(v), w), max(int(v), w)) for v, ws in rotation.items() for w in ws} == augmented_edges
    for v, ws in rotation.items():
        for w in ws:
            assert int(v) in rotation[str(w)]
    faces = faces_from_rotation(rotation)
    euler = len(rotation) - len(augmented_edges) + len(faces)
    assert euler == 2
    disk_rotation = {v: [w for w in ws if w != apex]
                     for v, ws in rotation.items() if int(v) != apex}
    disk_faces = faces_from_rotation(disk_rotation)
    boundary_faces = [i for i, face in enumerate(disk_faces)
                      if len(face) == 5 and set(face) == set(range(5))
                      and all(tuple(sorted((face[j], face[(j + 1) % 5]))) in FRAME
                              for j in range(5))]
    assert len(boundary_faces) == 1
    return {"source_file": source_path, "source_pointer": f"/q_orbits/{index}",
            "source_sha256": actual_source_sha256,
            "saved_source_sha256_matches": True,
            "method": "Delete omitted vertices and edges in the saved source rotation; retain the original apex.",
            "apex": apex, "augmented_rotation": rotation, "augmented_faces": faces,
            "augmented_euler_characteristic": euler,
            "disk_rotation": disk_rotation, "disk_faces": disk_faces,
            "boundary_face_index": boundary_faces[0]}


def compute_outputs():
    input_manifest, occurrences, graph_occurrences = [], [], defaultdict(list)
    saved_metadata_mismatches = []
    for path in sorted(INPUT.glob("chunk_*.json")):
        input_manifest.append({"path": str(path.relative_to(ROOT)),
                               "sha256": sha256(path.read_bytes()).hexdigest()})
        data = json.loads(path.read_text())
        for oi, orbit in enumerate(data["orbits"]):
            if orbit["type"] not in ("AD", "NA"):
                continue
            for ri, row in enumerate(orbit["rows"]):
                assert tuple(row["literal_row"]) == REPS[row["row_index"]]
                for ci, core in enumerate(row["cores"]):
                    edges = literal_graph(core["edges"])
                    vertices = sorted({v for edge in edges for v in edge})
                    degrees = [sum(root in edge for edge in edges) if root in vertices else None
                               for root in (5, 6)]
                    if degrees != [4, 4]:
                        continue
                    mixed = mixed_components(edges)
                    metadata = {"root_degrees": degrees, "vertices": vertices,
                                "private_size": len(vertices) - 5, "total_size": len(vertices),
                                "mixed_components": mixed,
                                "contains_mixed_component": bool(mixed)}
                    differences = {key: {"saved": core[key], "computed": value}
                                   for key, value in metadata.items() if core[key] != value}
                    pointer = f"/orbits/{oi}/rows/{ri}/cores/{ci}"
                    if differences:
                        saved_metadata_mismatches.append({"input_chunk": str(path.relative_to(ROOT)),
                                                          "input_pointer": pointer, "differences": differences})
                    record = {"input_chunk": str(path.relative_to(ROOT)), "input_pointer": pointer,
                              "row_index": row["row_index"], "literal_row": list(REPS[row["row_index"]]),
                              "saved_sigma_mask": core["sigma_mask"],
                              "source_metadata": {"type": orbit["type"], "critical": orbit["critical"],
                                                  "k": orbit["k"], "code": orbit["code"],
                                                  "sigma_mask": orbit["sigma_mask"], "roots": orbit["roots"],
                                                  "orbit_size": orbit["orbit_size"],
                                                  "stabilizer_size": orbit["stabilizer_size"],
                                                  "source_file": orbit["source"],
                                                  "source_sha256": orbit["source_sha256"]}, **metadata}
                    occurrences.append(record)
                    graph_occurrences[edges].append(record)
    assert len(input_manifest) == 19
    assert Counter(o["source_metadata"]["type"] for o in occurrences) == {"AD": 2360, "NA": 56}
    assert not saved_metadata_mismatches
    images = target_images()
    source_cache, catalog, sigma_mismatches = {}, [], []
    for number, edges in enumerate(sorted(graph_occurrences), start=1):
        graph_records = graph_occurrences[edges]
        name = f"C44P-S{number:04d}"
        decisions = [dict(row_index=i, literal_row=list(row), **full_decision(edges, row))
                     for i, row in enumerate(REPS)]
        sigma = sum(1 << i for i, decision in enumerate(decisions) if decision["accepted"])
        accepted = [i for i in range(10) if sigma & (1 << i)]
        rejected = [i for i in range(10) if not sigma & (1 << i)]
        matches, failures = [], []
        for image in images:
            absent = sorted(set(image["accepted_rows"]) - set(accepted))
            if not absent:
                matches.append({key: image[key] for key in ("image_id", "target_sigma_mask",
                                                            "image_sigma_mask", "s", "r", "vertex_map")})
            else:
                i = absent[0]
                failures.append({"image_id": image["image_id"], "missing_row_index": i,
                                 "missing_literal_row": list(REPS[i]),
                                 "rejection_tree_reference": f"/row_decisions/{i}/rejection_tree"})
        minimality = []
        for i in rejected:
            for edge in edges:
                if edge in FRAME:
                    continue
                result = full_decision(tuple(e for e in edges if e != edge), REPS[i])
                assert result["accepted"]
                minimality.append({"row_index": i, "deleted_edge": list(edge),
                                   "colouring": result["colouring"]})
        embedding = inherited_embedding(edges, graph_records[0], source_cache)
        graph = {"name": name, "vertices": graph_records[0]["vertices"],
                 "edges": [list(edge) for edge in edges], "roots": [5, 6],
                 "root_degrees": [4, 4], "private_size": graph_records[0]["private_size"],
                 "total_size": graph_records[0]["total_size"],
                 "mixed_components": graph_records[0]["mixed_components"],
                 "contains_mixed_component": graph_records[0]["contains_mixed_component"],
                 "sigma_mask": sigma, "accepted_rows": accepted, "rejected_rows": rejected,
                 "row_decisions": decisions, "minimality_witnesses": minimality,
                 "compatible": bool(matches), "matches": matches,
                 "image_failures": failures, "embedding": embedding,
                 "occurrence_count": len(graph_records),
                 "occurrences_by_source_type": dict(sorted(Counter(o["source_metadata"]["type"]
                                                                    for o in graph_records).items())),
                 "occurrences_by_criticality": dict(sorted(Counter("critical" if o["source_metadata"]["critical"]
                                                                    else "noncritical" for o in graph_records).items()))}
        catalog.append(graph)
        for occurrence in graph_records:
            occurrence.update({"core_name": name, "recomputed_sigma_mask": sigma,
                               "saved_sigma_matches": occurrence["saved_sigma_mask"] == sigma,
                               "compatible": bool(matches), "matches": matches,
                               "image_failures": failures})
            assert occurrence["row_index"] in rejected
            if not occurrence["saved_sigma_matches"]:
                sigma_mismatches.append({key: occurrence[key] for key in
                                         ("input_chunk", "input_pointer", "core_name",
                                          "saved_sigma_mask", "recomputed_sigma_mask")})
    joint = defaultdict(lambda: {"occurrences": 0, "compatible": 0, "incompatible": 0,
                                 "weighted_occurrences": 0, "literal_core_names": set()})
    for occurrence in occurrences:
        source = occurrence["source_metadata"]
        key = (source["type"], "critical" if source["critical"] else "noncritical",
               occurrence["private_size"], occurrence["contains_mixed_component"])
        group = joint[key]
        group["occurrences"] += 1
        group["compatible" if occurrence["compatible"] else "incompatible"] += 1
        group["weighted_occurrences"] += source["orbit_size"]
        group["literal_core_names"].add(occurrence["core_name"])
    tables = []
    for (source_type, population, size, mixed), counts in sorted(joint.items()):
        names = sorted(counts.pop("literal_core_names"))
        tables.append({"source_type": source_type, "population": population, "private_size": size,
                       "total_size": size + 5, "mixed": mixed, **counts,
                       "distinct_literal_cores_in_group": len(names), "core_names": names})
    outputs = {}
    output_manifest = []
    for kind, records, chunk_size in (("catalog", catalog, 10), ("occurrences", occurrences, 100)):
        for start in range(0, len(records), chunk_size):
            relative = f"saved_screen/{kind}/chunk_{1 + start // chunk_size:04d}.json"
            payload = encoded({kind: records[start:start + chunk_size]})
            outputs[relative] = payload
            output_manifest.append({"path": relative, "sha256": sha256(payload).hexdigest(),
                                    "count": len(records[start:start + chunk_size]), "bytes": len(payload)})
            assert len(payload) < 1_000_000
    mixed_core = min((core for core in catalog if core["contains_mixed_component"]),
                     key=lambda core: (core["private_size"], core["name"]))
    named_mixed = {"alias": "C44P-MIXED3-001", "catalog_core_name": mixed_core["name"],
                   "graph": mixed_core,
                   "first_occurrence": next(o for o in occurrences if o["core_name"] == mixed_core["name"])}
    outputs["saved_screen/named_C44P-MIXED3-001.json"] = encoded(named_mixed)
    definitions = {
        "boundary": [0, 1, 2, 3, 4], "frame_edges": [list(edge) for edge in sorted(FRAME)],
        "REPS": [list(row) for row in REPS],
        "Sigma": "Literal row indices admitting an extension to one shared four-colour frame; S4 quotient by first-appearance normalization.",
        "D5_action": "Forward vertex map g(i)=(s*i+r)%5; transported colours placed at g(i), then one shared S4 normalization.",
        "selection": "AD or NA, original roots 5 and 6 present, recomputed retained degrees exactly [4,4]; both critical and noncritical.",
        "duplicate_equivalence": "Identical sorted literal full edge sets, including boundary labels and private labels; no isomorphism quotient.",
        "compatibility": "At least one of all 20 (base 933/941, D5 element) image row sets is a subset of the recomputed Sigma(M).",
        "mixed": "Component of effective private vertices after removing named original roots 5,6 with retained contacts to both roots.",
        "rejection_tree": "At each node all four colours are covered once. A branch either identifies an edge to an already coloured equal-colour neighbour, or recurses after assigning the node vertex. The root starts with the literal boundary row.",
        "sources": ["docs/c5_excess_two_finite_search.md#1", "artifacts/c5_excess_two_c44/REPORT.md#1",
                    "artifacts/c5_excess_two_c44/PROOF_NOTES.md#1", "docs/c5_kempe_guide.md#3"]}
    embedding_input_manifest = [{"path": path, "sha256": source_cache[path]["sha256"]}
                                for path in sorted(source_cache)]
    summary = {"definitions": definitions, "input_manifest": input_manifest,
               "embedding_input_manifest": embedding_input_manifest, "output_manifest": output_manifest,
               "target_images": images, "occurrences": len(occurrences), "distinct_literal_cores": len(catalog),
               "compatible_occurrences": sum(o["compatible"] for o in occurrences),
               "incompatible_occurrences": sum(not o["compatible"] for o in occurrences),
               "compatible_literal_cores": sum(core["compatible"] for core in catalog),
               "incompatible_literal_cores": sum(not core["compatible"] for core in catalog),
               "sigma_mismatches": sigma_mismatches, "metadata_mismatches": saved_metadata_mismatches,
               "saved_sigma_mask_occurrences": dict(sorted(Counter(str(o["saved_sigma_mask"])
                                                                   for o in occurrences).items())),
               "recomputed_sigma_mask_occurrences": dict(sorted(Counter(str(o["recomputed_sigma_mask"])
                                                                         for o in occurrences).items())),
               "joint_statistics": tables,
               "named_mixed_certificate": {"alias": named_mixed["alias"], "catalog_core_name": mixed_core["name"],
                                           "path": "saved_screen/named_C44P-MIXED3-001.json"},
               "computational_scope": "Ten independent literal-row searches per distinct literal graph, memoized only across exactly equal input edge sets; all 2416 occurrence comparisons retained.",
               "embedding_scope": "Each catalog graph has a directly inherited saved ER source rotation; retained dart coverage, symmetry, Euler2 and the C5 boundary face are checked.",
               "branch": "At least one compatible core; stop generalizing. Compatibility is necessary only, and does not exhibit any source with full Sigma933/941."}
    outputs["saved_screen_summary.json"] = encoded(summary)
    return outputs, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Recompute all outputs and compare exact bytes without writes.")
    args = parser.parse_args()
    outputs, summary = compute_outputs()
    mismatches = []
    for relative, payload in sorted(outputs.items()):
        path = OUTPUT / relative
        if args.check:
            if not path.is_file() or path.read_bytes() != payload:
                mismatches.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "output_files": len(outputs),
                      "occurrences": summary["occurrences"], "distinct_literal_cores": summary["distinct_literal_cores"],
                      "compatible_occurrences": summary["compatible_occurrences"],
                      "incompatible_occurrences": summary["incompatible_occurrences"],
                      "saved_sigma_mismatches": len(summary["sigma_mismatches"]),
                      "byte_mismatches": mismatches}, sort_keys=True))
    return int(bool(mismatches or summary["sigma_mismatches"]))


if __name__ == "__main__":
    raise SystemExit(main())
