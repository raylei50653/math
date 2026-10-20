#!/usr/bin/env python3
"""Finite geometry controls and complete literal fibres, with read-only replay.

The graph construction, Cartesian-product enumerator, local inverse predicates,
and insertion/deletion maps below do not consult support transition tables.
The frozen earlier checker independently validates the oriented disk cellulation
and supplies a second, pruned full-fibre enumerator.
"""

from __future__ import annotations

import argparse
import copy
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
FROZEN = AUDIT / "frozen"
OLD_REL = "audits/2026-10-19-c5-pr-disk-semantics-ed59843/C/check_full_graph.py"
SOURCE_REL = "docs/sources/2026-10-19-c5-grammar-v02/certificate_v02.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def edge(a, b):
    return tuple(sorted((a, b)))


def from_faces(n, boundary, faces):
    edges = sorted({edge(f[i], f[(i + 1) % len(f)]) for f in faces for i in range(len(f))})
    return {"vertices": n, "edges": [list(e) for e in edges], "boundary": list(boundary), "faces": copy.deepcopy(faces)}


def seed_f():
    return from_faces(5, range(5), [[0, 1, 2], [0, 2, 3], [0, 3, 4]])


def seed_c():
    return from_faces(5, range(5), [list(range(5))])


def push(g):
    h = copy.deepcopy(g)
    x = h["vertices"]
    a, b, c = h["boundary"][0], h["boundary"][1], h["boundary"][-1]
    h["vertices"] += 1
    h["edges"] = sorted(h["edges"] + [list(edge(x, v)) for v in (a, b, c)])
    h["faces"].extend([[b, a, x], [a, c, x]])
    h["boundary"][0] = x
    return h


def insert(g, face):
    h = copy.deepcopy(g)
    require(face in h["faces"] and len(face) == 3, "insertion requires the actual triangular face")
    a, b, c = face
    x = h["vertices"]
    h["vertices"] += 1
    h["edges"] = sorted(h["edges"] + [list(edge(x, v)) for v in (a, b, c)])
    h["faces"].remove(face)
    h["faces"].extend([[a, b, x], [b, c, x], [c, a, x]])
    return h


def adjacency(g):
    out = [set() for _ in range(g["vertices"])]
    for a, b in g["edges"]:
        out[a].add(b)
        out[b].add(a)
    return out


def inverse_p_sites(g):
    """Test every rotation, retaining its actual vertex and face identities."""
    adj = adjacency(g)
    sites = []
    for i, z in enumerate(g["boundary"]):
        b1 = g["boundary"][(i + 1) % 5]
        b4 = g["boundary"][(i - 1) % 5]
        extra = adj[z] - {b1, b4}
        if len(adj[z]) != 3 or len(extra) != 1:
            continue
        a = next(iter(extra))
        if a in g["boundary"]:
            continue
        incident = [f for f in g["faces"] if z in f]
        expected = {frozenset((b4, z, a)), frozenset((z, b1, a))}
        if len(incident) == 2 and {frozenset(f) for f in incident} == expected:
            sites.append({"index": i, "vertex": z, "exposed_vertex": a})
    return sites


def inverse_i_sites(g):
    adj = adjacency(g)
    out = []
    for v in range(g["vertices"]):
        if v in g["boundary"] or len(adj[v]) != 3:
            continue
        incident = [f for f in g["faces"] if v in f]
        if len(incident) != 3 or any(len(f) != 3 for f in incident):
            continue
        neighbors = sorted(adj[v])
        if all(edge(a, b) in {tuple(e) for e in g["edges"]} for a, b in zip(neighbors, neighbors[1:] + neighbors[:1])):
            out.append(v)
    return out


def compact_after_delete(g, v, boundary, faces):
    kept = [u for u in range(g["vertices"]) if u != v]
    old_to_new = {u: i for i, u in enumerate(kept)}
    h = {
        "vertices": len(kept),
        "edges": [[old_to_new[a], old_to_new[b]] for a, b in g["edges"] if v not in (a, b)],
        "boundary": [old_to_new[u] for u in boundary],
        "faces": [[old_to_new[u] for u in f] for f in faces],
    }
    return h, old_to_new


def erase_i(g, v):
    require(v in inverse_i_sites(g), "not an inverse-I site")
    incident = [f for f in g["faces"] if v in f]
    rim = [(f[i], f[(i + 1) % 3]) for f in incident for i in range(3) if v not in (f[i], f[(i + 1) % 3])]
    nxt = dict(rim)
    a = min(nxt)
    triangle = [a, nxt[a], nxt[nxt[a]]]
    require(nxt[triangle[-1]] == a and len(set(triangle)) == 3, "star rim is not a triangle")
    faces = [f for f in g["faces"] if v not in f] + [triangle]
    return compact_after_delete(g, v, g["boundary"], faces)


def erase_p_at_zero(g):
    site = next((s for s in inverse_p_sites(g) if s["index"] == 0), None)
    require(site is not None, "not an inverse-P site at index zero")
    v = site["vertex"]
    boundary = [site["exposed_vertex"]] + g["boundary"][1:]
    return compact_after_delete(g, v, boundary, [f for f in g["faces"] if v not in f])


def brute_fibres(g, rows):
    interior = sorted(set(range(g["vertices"])) - set(g["boundary"]))
    all_fibres = []
    for row in rows:
        fibre = []
        for assignment in product(range(4), repeat=len(interior)):
            colours = dict(zip(g["boundary"], map(int, row)))
            colours.update(zip(interior, assignment))
            if all(colours[a] != colours[b] for a, b in g["edges"]):
                fibre.append("".join(map(str, assignment)))
        all_fibres.append(fibre)
    return all_fibres


def record(g, rows, old):
    adj = old.validate_disk(g)
    fibres = brute_fibres(g, rows)
    require(fibres == [old.full_fibre(g, row, adj) for row in rows], "Cartesian and pruned full fibres disagree")
    counts = list(map(len, fibres))
    return {
        "graph": g,
        "interior_order": sorted(set(range(g["vertices"])) - set(g["boundary"])),
        "fibres": [{"boundary_row": row, "interior_assignments": f} for row, f in zip(rows, fibres)],
        "counts": counts,
        "mask": sum(1 << i for i, n in enumerate(counts) if n),
        "boundary_degrees": [len(adj[v]) for v in g["boundary"]],
        "interior_degrees": [len(adj[v]) for v in range(g["vertices"]) if v not in g["boundary"]],
        "inverse_P_sites": inverse_p_sites(g),
        "inverse_I_sites": inverse_i_sites(g),
    }


def restriction_fibres(g, h, mapping, rows, fibres):
    old_interior = sorted(set(range(g["vertices"])) - set(g["boundary"]))
    new_interior = sorted(set(range(h["vertices"])) - set(h["boundary"]))
    reverse = {new: old for old, new in mapping.items()}
    out = []
    for row, fibre in zip(rows, fibres):
        restricted = []
        for assignment in fibre:
            colours = dict(zip(g["boundary"], map(int, row)))
            colours.update(zip(old_interior, map(int, assignment)))
            require([colours[reverse[v]] for v in h["boundary"]] == list(map(int, row)), "literal boundary changed under I restriction")
            restricted.append("".join(str(colours[reverse[v]]) for v in new_interior))
        require(len(restricted) == len(set(restricted)), "I restriction is not injective")
        out.append(sorted(restricted))
    return out


def punctured_icosahedron():
    """Explicit oriented cap and antiprism band; no graph library or embedding oracle."""
    faces = []
    for i in range(5):
        faces.extend([[i, (i + 1) % 5, 5 + i], [i, 5 + i, 5 + (i - 1) % 5], [5 + i, 5 + (i + 1) % 5, 10]])
    return from_faces(11, range(5), faces)


def subdivide(g, a, b):
    """Subdivide a spoke, then triangulate only its far-side quadrilateral."""
    x = g["vertices"]
    faces = []
    for face in g["faces"]:
        new_face = []
        for i, v in enumerate(face):
            new_face.append(v)
            if {v, face[(i + 1) % len(face)]} == {a, b}:
                new_face.append(x)
        faces.append(new_face)
    # The cap at boundary[0] remains quadrilateral.  A diagonal on the far side
    # gives x degree three, so even the earlier validator's simple-link
    # convention (which excludes degree-two interior subdivisions) is met.
    far = next(f for f in faces if len(f) == 4 and g["boundary"][0] not in f)
    require(far[:3] == [a, x, b], "unexpected spoke orientation")
    c = far[-1]
    faces.remove(far)
    faces.extend([[a, x, c], [x, b, c]])
    return from_faces(x + 1, g["boundary"], faces)


def load_inputs():
    base = json.loads((AUDIT / "BASE.json").read_text())
    hashes = {item["path"]: item["sha256"] for item in base["inputs"]}
    for rel in (OLD_REL, SOURCE_REL):
        require(sha256((FROZEN / rel).read_bytes()).hexdigest() == hashes[rel], "frozen input SHA mismatch: " + rel)
    spec = importlib.util.spec_from_file_location("frozen_full_graph", FROZEN / OLD_REL)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    source = json.loads((FROZEN / SOURCE_REL).read_text())
    return base, source, old


def build():
    base, source, old = load_inputs()
    rows = source["model"]["rows"]
    f, c = seed_f(), seed_c()
    wheel = push(f)
    stacked = copy.deepcopy(wheel)
    for face in wheel["faces"]:
        stacked = insert(stacked, face)
    ico = punctured_icosahedron()
    subdivided = subdivide(wheel, 0, 1)
    graphs = {"F": f, "C": c, "W5_equals_FP": wheel, "W5_all_five_faces_stacked": stacked, "icosahedron_puncture": ico, "subdivided_W5_spoke": subdivided}
    cases = {name: record(g, rows, old) for name, g in graphs.items()}
    require(cases["W5_equals_FP"]["mask"] == cases["W5_all_five_faces_stacked"]["mask"] == 91, "stacked wheel support mismatch")
    require(cases["W5_all_five_faces_stacked"]["inverse_P_sites"] == [], "stacked wheel unexpectedly peelable by P")
    require(cases["icosahedron_puncture"]["counts"] == [2] * 10, "punctured icosahedron count control failed")
    require(cases["icosahedron_puncture"]["inverse_P_sites"] == cases["icosahedron_puncture"]["inverse_I_sites"] == [], "punctured icosahedron unexpectedly peelable")
    require(cases["C"]["counts"] == [1] * 10, "C control failed")
    require(cases["F"]["inverse_P_sites"] == [], "boundary third-neighbor control failed")
    require(not any(s["index"] == 0 for s in cases["subdivided_W5_spoke"]["inverse_P_sites"]), "nontriangle cap incorrectly accepted")
    require(len(adjacency(subdivided)[subdivided["boundary"][0]]) == 3, "nontriangle control lost degree three")
    require(set(inverse_i_sites(stacked)) == set(range(6, 11)), "unexpected initial inverse-I sites")

    # These actual full-graph restrictions, with all empty rows retained, are
    # machine-readable witnesses for the successful geometry reduction.
    h = stacked
    reductions = []
    for v in range(10, 5, -1):
        before = record(h, rows, old)
        smaller, mapping = erase_i(h, v)
        after = record(smaller, rows, old)
        before_fibres = [f["interior_assignments"] for f in before["fibres"]]
        after_fibres = [f["interior_assignments"] for f in after["fibres"]]
        require(restriction_fibres(h, smaller, mapping, rows, before_fibres) == after_fibres, "full-fibre I restriction is not surjective")
        reductions.append({
            "operator": "inverse_I",
            "removed_vertex": v,
            "before": before,
            "after": after,
            "old_to_new": {str(a): b for a, b in mapping.items()},
            "all_ten_literal_fibre_restrictions_bijective": True,
            "interior_count_drop": 1,
        })
        h = smaller
    require(h["edges"] == wheel["edges"] and h["boundary"] == wheel["boundary"], "I reduction did not recover W5")
    smaller, mapping = erase_p_at_zero(h)
    require(smaller["edges"] == f["edges"] and smaller["boundary"] == f["boundary"], "P reduction did not recover F")
    require(old.get_graph_counts(smaller, rows)[0] == cases["F"]["counts"], "final seed fibres mismatch")
    reductions.append({"operator": "inverse_P_at_zero", "removed_vertex": h["boundary"][0], "exposed_vertex": 0, "after": record(smaller, rows, old), "old_to_new": {str(a): b for a, b in mapping.items()}, "interior_count_drop": 1})

    # Check both the actual forward lift (unique fourth colour) and exact
    # reverse graph, rather than merely comparing support or marginal counts.
    require(cases["W5_equals_FP"]["counts"] == cases["W5_all_five_faces_stacked"]["counts"], "I changed literal counts")
    inverse_p_roundtrips = []
    for g in (f, c, ico, stacked):
        bigger = push(g)
        old.validate_disk(bigger)
        smaller, mapping = erase_p_at_zero(bigger)
        require(smaller == g, "P inverse graph roundtrip failed")
        inverse_p_roundtrips.append({"source_vertices": g["vertices"], "source_boundary": g["boundary"], "roundtrip_exact_graph": True})

    # Invalid hypotheses and corruption must fail closed.
    rotated_f = copy.deepcopy(f)
    rotated_f["boundary"] = f["boundary"][2:] + f["boundary"][:2]
    require(len(adjacency(rotated_f)[rotated_f["boundary"][0]]) == 3, "third-neighbor control lost degree three")
    rejected = []
    for name, action in [
        ("inverse_P_on_F_third_neighbor_is_boundary", lambda: erase_p_at_zero(rotated_f)),
        ("inverse_P_on_nontriangular_cap", lambda: erase_p_at_zero(subdivided)),
        ("inverse_I_on_icosahedron_degree_five", lambda: erase_i(ico, 5)),
        ("triangle_insertion_on_C_nontriangle", lambda: insert(c, c["faces"][0])),
    ]:
        try:
            action()
        except ValueError as exc:
            rejected.append({"name": name, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError("negative control accepted: " + name)

    return {
        "schema": "c5-pr-source-coverage-geometric-controls-v1",
        "base_head": base["head"],
        "input_sha256": {rel: sha256((FROZEN / rel).read_bytes()).hexdigest() for rel in (OLD_REL, SOURCE_REL)},
        "rows": rows,
        "scope": "Six explicitly embedded disks; every fixed canonical literal fibre retained including empties. No arbitrary-source coverage or 4CT.",
        "cases": cases,
        "successful_reduction": reductions,
        "inverse_P_roundtrips": inverse_p_roundtrips,
        "negative_controls": rejected,
        "summary": {
            "initial_graph_cases": len(cases),
            "initial_complete_fibres": len(cases) * 10,
            "initial_empty_fibres": sum(not f["interior_assignments"] for case in cases.values() for f in case["fibres"]),
            "initial_full_colourings": sum(sum(case["counts"]) for case in cases.values()),
            "inverse_I_full_fibre_bijections": len(reductions) - 1,
            "inverse_P_roundtrips": len(inverse_p_roundtrips),
            "rejected_invalid_operation_controls": len(rejected),
            "all_cases_cross_checked_by_cartesian_and_pruned_enumeration": True,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "geometry_certificate.json")
    args = parser.parse_args()
    result = build()
    encoded = canonical_bytes(result)
    if args.write:
        with args.certificate.open("xb") as stream:
            stream.write(encoded)
    else:
        require(args.certificate.read_bytes() == encoded, "certificate differs from independent reconstruction")
    print(json.dumps({"status": "PASS", **result["summary"]}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
