#!/usr/bin/env python3
"""Finite original-edge audit of the saturated common-hub closure theorem.

The proof is a paper argument. This checker uses exhaustive proper colorings
of each original exterior, independently of sector gluing and the recurrence.
Existing reverse-shelling evidence is read, never rewritten.
"""

import argparse
import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path

import networkx as nx

from four_color_shelling_fan_verification import geometry
from four_color_shelling_verification import faces


ROOT = Path(__file__).resolve().parents[1]
COLORS = tuple(range(4))
BASELINE = ROOT / "audits/2026-10-29-reverse-shelling-e1a90fe/reverse-shelling.json"


def edge_set(graph):
    return {tuple(sorted(edge)) for edge in graph.edges()}


def proper(edges, coloring):
    return all(coloring[u] != coloring[v] for u, v in edges)


def enumerate_original_edges(graph):
    """All labelled proper colorings, with no quotient or coloring oracle."""
    vertices = sorted(graph)
    visit_order = sorted(graph, key=lambda v: (-graph.degree(v), v))
    coloring = {}
    result = []

    def visit(j):
        if j == len(visit_order):
            result.append(tuple(coloring[v] for v in vertices))
            return
        vertex = visit_order[j]
        forbidden = {coloring[u] for u in graph[vertex] if u in coloring}
        for color in COLORS:
            if color not in forbidden:
                coloring[vertex] = color
                visit(j + 1)
        coloring.pop(vertex, None)

    visit(0)
    return sorted(result)


def exterior_stage(graph, geom, k):
    active = set(geom["order"][:k])
    boundary = geom["boundaries"][k]
    processed = set(graph) - active
    ring_edges = {tuple(sorted(e)) for e in
                  zip(boundary, boundary[1:] + boundary[:1])}
    edges = {e for e in edge_set(graph) if set(e) & processed} | ring_edges
    disk = nx.Graph()
    disk.add_nodes_from(sorted(processed | set(boundary)))
    disk.add_edges_from(sorted(edges))
    return {"remaining_vertices": sorted(active), "boundary_scope": boundary,
            "unprocessed_interior_vertices": sorted(active - set(boundary)),
            "exterior_vertices": sorted(disk), "exterior_edges": sorted(edges)}


def canonical_contract(graph, geom):
    """Check the saved original rotation, not a fresh embedding of the graph."""
    order = geom["order"]
    assert len(order) == len(graph) and set(order) == set(graph)
    assert order[:2] == geom["outer_face"][:2]
    assert order[-1] == geom["outer_face"][-1]
    rotation = geom["rotation_cw"]
    assert all(set(rotation[v]) == set(graph[v]) for v in graph)
    original = nx.PlanarEmbedding()
    original.set_data(rotation)
    original.check_structure()
    assert all(len(face) == 3 for face in faces(original))
    for k in range(3, len(order) + 1):
        active = set(order[:k])
        embedding = nx.PlanarEmbedding()
        embedding.set_data({v: [w for w in rotation[v] if w in active]
                            for v in sorted(active)})
        embedding.check_structure()
        boundary = embedding.traverse_face(*order[:2])
        assert boundary == geom["boundaries"][k]
        assert len(boundary) == len(set(boundary))
        assert nx.is_biconnected(graph.subgraph(active))
        outer_darts = set(zip(boundary, boundary[1:] + boundary[:1]))
        assert all(len(face) == 3 or set(zip(face, face[1:] + face[:1])) == outer_darts
                   for face in faces(embedding))
        removed = set(graph) - active
        assert {w for v in removed for w in graph[v] if w in active} <= set(boundary)
        if k > 3:
            previous = geom["boundaries"][k - 1]
            path = [previous[0]] + list(reversed(previous[1:]))
            neighbors = set(graph[order[k - 1]]) & set(order[:k - 1])
            indices = [j for j, v in enumerate(path) if v in neighbors]
            assert len(indices) >= 2
            assert indices == list(range(min(indices), max(indices) + 1))
            interval = path[min(indices):max(indices) + 1]
            assert set(boundary) == (set(previous) - set(interval[1:-1])) | {order[k - 1]}


def original_embedding_check(stage, rotation):
    graph = nx.Graph()
    graph.add_nodes_from(stage["exterior_vertices"])
    graph.add_edges_from(stage["exterior_edges"])
    boundary = stage["boundary_scope"]
    ring_edges = {tuple(sorted(e)) for e in
                  zip(boundary, boundary[1:] + boundary[:1])}
    assert {e for e in edge_set(graph) if set(e) <= set(boundary)} == ring_edges
    embedding = nx.PlanarEmbedding()
    embedding.set_data({v: [w for w in rotation[v] if graph.has_edge(v, w)]
                        for v in graph})
    embedding.check_structure()
    outer_darts = {(v, u) for u, v in
                   zip(boundary, boundary[1:] + boundary[:1])}
    fs = faces(embedding)
    matching = [f for f in fs if set(zip(f, f[1:] + f[:1])) == outer_darts]
    assert len(matching) == 1
    assert all(len(f) == 3 or f == matching[0] for f in fs)
    assert nx.is_biconnected(graph)
    return graph, embedding


def sector_audit(graph, boundary, hub, embedding, complete):
    """Derive sectors from the original embedded wheel, then enumerate each."""
    skeleton = set(boundary) | {hub}
    triangles = [(hub, u, v) for u, v in
                 zip(boundary, boundary[1:] + boundary[:1])]
    interiors = [[] for _ in triangles]
    components = sorted((sorted(c) for c in
                         nx.connected_components(graph.subgraph(set(graph) - skeleton))),
                        key=lambda c: tuple(c))
    attachments = []
    for component in components:
        attachment = {w for v in component for w in graph[v] if w in skeleton}
        matches = [j for j, triangle in enumerate(triangles)
                   if attachment == set(triangle)]
        assert len(matches) == 1
        interiors[matches[0]].extend(component)
        attachments.append({"component": component,
                            "original_skeleton_neighbors": sorted(attachment),
                            "sector_index": matches[0]})
    # Removing interior vertices from the original rotation gives exactly a wheel.
    wheel_rotation = {v: [w for w in embedding.neighbors_cw_order(v)
                          if w in skeleton] for v in skeleton}
    wheel_embedding = nx.PlanarEmbedding()
    wheel_embedding.set_data(wheel_rotation)
    wheel_embedding.check_structure()
    wheel_face_sets = [set(f) for f in faces(wheel_embedding)]
    assert all(set(t) in wheel_face_sets for t in triangles)
    assert {v for values in interiors for v in values} == set(graph) - skeleton
    sectors = []
    covered_edges = set()
    normalized_product = 1
    for j, (triangle, inside) in enumerate(zip(triangles, interiors)):
        inside = sorted(inside)
        patch = graph.subgraph(set(triangle) | set(inside)).copy()
        covered_edges |= edge_set(patch)
        patch_vertices = sorted(patch)
        anchored = defaultdict(list)
        for values in enumerate_original_edges(patch):
            c = dict(zip(patch_vertices, values))
            anchored[tuple(c[v] for v in triangle)].append(tuple(c[v] for v in inside))
        assert set(anchored) == set(itertools.permutations(COLORS, 3))
        counts = {len(values) for values in anchored.values()}
        assert len(counts) == 1
        factor = counts.pop()
        assert factor > 0
        normalized_product *= factor
        sectors.append({"index": j, "triangle_scope": triangle,
                        "interior_scope": inside,
                        "original_edges": sorted(edge_set(patch)),
                        "normalized_extension_count": factor,
                        "complete_anchored_extensions": [
                            {"triangle_colors": triple,
                             "interior_colorings": sorted(values)}
                            for triple, values in sorted(anchored.items())]})
    assert covered_edges == edge_set(graph)
    # Compare the full Cartesian gluing with independently enumerated witnesses.
    joined = set()
    for values in itertools.product(COLORS, repeat=len(boundary)):
        b = dict(zip(boundary, values))
        if not proper(list(zip(boundary, boundary[1:] + boundary[:1])), b):
            continue
        for hub_color in set(COLORS) - set(values):
            c = b | {hub: hub_color}
            choices = []
            for sector in sectors:
                triple = tuple(c[v] for v in sector["triangle_scope"])
                choices.append(next(row["interior_colorings"] for row in
                                    sector["complete_anchored_extensions"]
                                    if row["triangle_colors"] == triple))
            for assignments in itertools.product(*choices):
                whole = dict(c)
                for sector, assignment in zip(sectors, assignments):
                    whole.update(zip(sector["interior_scope"], assignment))
                joined.add(tuple(whole[v] for v in sorted(graph)))
    assert joined == set(complete)
    return sectors, normalized_product, attachments


def audit_stage(stage, rotation, preferred_hub=None):
    graph, embedding = original_embedding_check(stage, rotation)
    vertices = sorted(graph)
    boundary = stage["boundary_scope"]
    assert not stage["unprocessed_interior_vertices"]
    assert vertices == stage["exterior_vertices"]
    complete = enumerate_original_edges(graph)
    assert complete
    rows = defaultdict(list)
    for values in complete:
        c = dict(zip(vertices, values))
        rows[tuple(c[v] for v in boundary)].append(values)
    candidates = sorted(h for h in set(vertices) - set(boundary)
                        if set(boundary) <= set(graph[h]))
    if preferred_hub is not None:
        assert preferred_hub in candidates
    hub = preferred_hub if preferred_hub is not None else next(iter(candidates), None)
    output = dict(stage) | {"common_hub_candidates": candidates, "chosen_hub": hub,
                            "complete_original_edge_colorings": complete,
                            "complete_proper_boundary_rows": sorted(rows)}
    if hub is None:
        four_rows = [row for row in sorted(rows) if len(set(row)) == 4]
        output["accepted_four_color_row"] = next(iter(four_rows), None)
        if four_rows:
            output["accepted_four_color_full_witness"] = rows[four_rows[0]][0]
        ring = list(zip(boundary, boundary[1:] + boundary[:1]))
        missing_q = [values for values in itertools.product((0, 1, 2), repeat=len(boundary))
                     if proper(ring, dict(zip(boundary, values))) and values not in rows]
        output["fixed_palette_Q"] = [0, 1, 2]
        output["missing_proper_fixed_palette_row"] = next(iter(missing_q), None)
        output["missing_proper_fixed_palette_row_count"] = len(missing_q)
        return output
    sectors, k_factor, attachments = sector_audit(graph, boundary, hub, embedding, complete)
    fibre_counts = []
    ring = list(zip(boundary, boundary[1:] + boundary[:1]))
    for values in itertools.product(COLORS, repeat=len(boundary)):
        c = dict(zip(boundary, values))
        expected = ((4 - len(set(values))) * k_factor
                    if len(set(values)) <= 3 and proper(ring, c) else 0)
        assert len(rows[values]) == expected
        fibre_counts.append(expected)
    assert len(complete) == 4 * k_factor * (2 ** len(boundary) + 2 * (-1) ** len(boundary))
    output.update({"sector_component_attachments": attachments, "sectors": sectors,
                   "positive_sector_product_K": k_factor,
                   "fibre_count_order": "all base-4 boundary rows in lexicographic order; zeros included",
                   "complete_boundary_fibre_counts_including_zero": fibre_counts})
    return output


def closure_audit(old, new, x):
    old_boundary, boundary = old["boundary_scope"], new["boundary_scope"]
    assert set(boundary) == set(old_boundary) - {x}
    old_edges, new_edges = set(map(tuple, old["exterior_edges"])), set(map(tuple, new["exterior_edges"]))
    added = sorted(new_edges - old_edges)
    assert len(added) == 1 and new_edges == old_edges | set(added)
    p, q = added[0]
    assert {p, q} == {old_boundary[(old_boundary.index(x) - 1) % len(old_boundary)],
                      old_boundary[(old_boundary.index(x) + 1) % len(old_boundary)]}
    hub = old["chosen_hub"]
    assert hub == new["chosen_hub"]
    assert old["positive_sector_product_K"] == new["positive_sector_product_K"]
    left = [s for s in old["sectors"] if set(s["triangle_scope"]) == {hub, p, x}][0]
    right = [s for s in old["sectors"] if set(s["triangle_scope"]) == {hub, q, x}][0]
    merged = [s for s in new["sectors"] if set(s["triangle_scope"]) == {hub, p, q}][0]
    assert set(merged["interior_scope"]) == set(left["interior_scope"]) | set(right["interior_scope"]) | {x}
    assert merged["normalized_extension_count"] == left["normalized_extension_count"] * right["normalized_extension_count"]
    oracle = defaultdict(int)
    for values in new["complete_original_edge_colorings"]:
        c = dict(zip(new["exterior_vertices"], values))
        oracle[tuple(c[v] for v in boundary)] |= 1 << c[x]
    old_rows = set(map(tuple, old["complete_proper_boundary_rows"]))
    masks = []
    endpoint_distinct_old_rows = []
    for row in sorted(old_rows):
        c = dict(zip(old_boundary, row))
        if c[p] != c[q]:
            endpoint_distinct_old_rows.append(row)
    assert endpoint_distinct_old_rows
    for values in itertools.product(COLORS, repeat=len(boundary)):
        c = dict(zip(boundary, values))
        mask = 0
        if c[p] != c[q]:
            for t in COLORS:
                lifted = c | {x: t}
                if tuple(lifted[v] for v in old_boundary) in old_rows:
                    mask |= 1 << t
        assert mask == oracle[values]
        explicit = 0
        if proper(list(zip(boundary, boundary[1:] + boundary[:1])), c):
            for t in COLORS:
                if t not in {c[p], c[q]} and len(set(values) | {t}) <= 3:
                    explicit |= 1 << t
        assert explicit == mask
        masks.append(mask)
    survivors = [v for v in old["complete_original_edge_colorings"]
                 if dict(zip(old["exterior_vertices"], v))[p] != dict(zip(old["exterior_vertices"], v))[q]]
    assert survivors == new["complete_original_edge_colorings"]
    return {"eliminated": x, "added_original_edge": [p, q],
            "same_hub": hub, "old_K": old["positive_sector_product_K"],
            "merged_sector_factor": merged["normalized_extension_count"],
            "old_adjacent_sector_factors": [left["normalized_extension_count"], right["normalized_extension_count"]],
            "endpoint_distinct_old_rows": endpoint_distinct_old_rows,
            "fibre_scope": boundary,
            "fibre_order": "all base-4 boundary rows lexicographically; color t is bit 1<<t",
            "explicit_U3_mask_formula_checked": True,
            "complete_fibre_masks_including_zero": masks}


def case_audit(name, graph, geom, stages, baseline_case=None):
    canonical_contract(graph, geom)
    saturation = next(j for j, stage in enumerate(stages)
                      if not stage["unprocessed_interior_vertices"])
    audited = []
    preferred = None
    for stage in stages[saturation:]:
        output = audit_stage(stage, geom["rotation_cw"], preferred)
        if audited and preferred is not None:
            x = next(iter(set(audited[-1]["boundary_scope"]) - set(output["boundary_scope"])))
            output["closure_from_previous"] = closure_audit(audited[-1], output, x)
        preferred = output["chosen_hub"]
        audited.append(output)
    if baseline_case is not None:
        for old, new in zip(baseline_case["stages"][saturation:], audited):
            assert list(map(tuple, old["complete_exterior_colorings"])) == new["complete_original_edge_colorings"]
            assert list(map(tuple, old["proper_boundary_relation_rows"])) == new["complete_proper_boundary_rows"]
    return {"name": name, "original_vertices": sorted(graph),
            "original_edges": sorted(edge_set(graph)), "geometry": geom,
            "saturation_stage_index": saturation, "saturated_stages": audited}


def octahedral_patch_case():
    graph = nx.wheel_graph(5)
    graph.add_edge(1, 3)
    octahedron = nx.octahedral_graph()
    mapping = {0: 0, 1: 1, 2: 2, 3: 5, 4: 6, 5: 7}
    graph.add_edges_from((mapping[u], mapping[v]) for u, v in octahedron.edges())
    # This is an actual face and actual generated canonical ordering, not an
    # arbitrary disk relation. The embedded octahedral patch is nonstacked.
    geom = geometry(graph, outer=[2, 0, 6])
    stages = [exterior_stage(graph, geom, k) for k in range(len(graph) - 1, 2, -1)]
    result = case_audit("wheel4-with-octahedral-triangle-patch", graph, geom, stages)
    first = result["saturated_stages"][0]
    assert len(first["boundary_scope"]) == 4
    assert first["positive_sector_product_K"] == 4
    assert any(s["normalized_extension_count"] == 4 for s in first["sectors"])
    result["construction"] = {"wheel_hub": 0, "wheel_boundary": [1, 2, 3, 4],
                              "residual_original_diagonal": [1, 3],
                              "octahedral_face_identification": mapping}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    baseline = json.loads(BASELINE.read_text())
    cases = []
    for case in baseline["cases"]:
        graph = nx.Graph()
        graph.add_edges_from(case["original_edges"])
        geom = dict(case["geometry"])
        geom["boundaries"] = {int(k): v for k, v in geom["boundaries"].items()}
        geom["rotation_cw"] = {int(k): v for k, v in geom["rotation_cw"].items()}
        regenerated = [exterior_stage(graph, geom, k)
                       for k in range(len(graph) - 1, 2, -1)]
        cases.append(case_audit(case["name"], graph, geom, regenerated, case))
    cases.append(octahedral_patch_case())
    stages = [s for c in cases for s in c["saturated_stages"]]
    hub_stages = [s for s in stages if s["chosen_hub"] is not None]
    closures = [s["closure_from_previous"] for s in stages if "closure_from_previous" in s]
    excluded = [s for s in stages if s["chosen_hub"] is None]
    assert any(s.get("accepted_four_color_row") is not None for s in excluded)
    report = {"schema": "four-color-saturated-hub-verification-v1",
              "scope": "Finite common-hub canonical sources only; arbitrary sources and 4CT remain OPEN.",
              "oracle": "All labelled proper exterior colorings by raw original-edge backtracking; no symmetry quotient, sector recurrence, solver or 4CT oracle.",
              "networkx_version": nx.__version__, "cases": cases,
              "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__), BASELINE,
                                           ROOT / "scripts/four_color_shelling_fan_verification.py",
                                           ROOT / "scripts/four_color_shelling_verification.py")},
              "totals": {"original_graphs": len(cases), "atlas_original_graphs": len(cases) - 1,
                         "saturated_stages": len(stages), "common_hub_stages": len(hub_stages),
                         "source_class_excluded_stages": len(excluded),
                         "excluded_stages_with_accepted_four_color_row": sum(s.get("accepted_four_color_row") is not None for s in excluded),
                         "excluded_stages_missing_Q_support": sum(s["missing_proper_fixed_palette_row_count"] > 0 for s in excluded),
                         "common_hub_closures": len(closures),
                         "complete_original_edge_colorings": sum(len(s["complete_original_edge_colorings"]) for s in stages),
                         "complete_boundary_count_entries_including_zero": sum(len(s["complete_boundary_fibre_counts_including_zero"]) for s in hub_stages),
                         "complete_transition_masks_including_zero": sum(len(c["complete_fibre_masks_including_zero"]) for c in closures),
                         "zero_transition_masks": sum(c["complete_fibre_masks_including_zero"].count(0) for c in closures),
                         "transition_mask_bit_count_sum": sum(mask.bit_count() for c in closures for mask in c["complete_fibre_masks_including_zero"]),
                         "max_transition_mask_bit_count": max(mask.bit_count() for c in closures for mask in c["complete_fibre_masks_including_zero"]),
                         "max_transition_mask_integer": max(mask for c in closures for mask in c["complete_fibre_masks_including_zero"]),
                         "anchored_sector_triples": sum(len(t["complete_anchored_extensions"]) for s in hub_stages for t in s["sectors"]),
                         "max_original_vertices": max(len(c["original_vertices"]) for c in cases),
                         "octahedral_patch_K": 4}}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["totals"], sort_keys=True))


if __name__ == "__main__":
    main()
