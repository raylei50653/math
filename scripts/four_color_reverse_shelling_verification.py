#!/usr/bin/env python3
"""Replay proper-boundary reverse shelling from original exterior edges.

Finite evidence only. No 4CT oracle, solver call, or claim of a no-lock theorem.
All scopes are ordered and all transition fibres include their zero masks.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx

from four_color_shelling_fan_verification import geometry
from four_color_shelling_verification import faces


COLORS = tuple(range(4))
ROOT = Path(__file__).resolve().parents[1]


def proper(edges, coloring):
    return all(coloring[u] != coloring[v] for u, v in edges)


def all_colorings(vertices, edges):
    # Direct original-edge enumeration; independent of boundary recurrence.
    return [values for values in itertools.product(COLORS, repeat=len(vertices))
            if proper(edges, dict(zip(vertices, values)))]


def exterior(graph, geom, k):
    active = set(geom["order"][:k])
    removed = set(graph) - active
    boundary = geom["boundaries"][k]
    ring_edges = {tuple(sorted(edge))
                  for edge in zip(boundary, boundary[1:] + boundary[:1])}
    edges = {tuple(sorted((u, v))) for u, v in graph.edges()
             if u in removed or v in removed} | ring_edges
    vertices = sorted(removed | set(boundary))
    disk = nx.Graph()
    disk.add_nodes_from(vertices)
    disk.add_edges_from(sorted(edges))
    assert nx.is_biconnected(disk)
    assert {edge for edge in edges if set(edge) <= set(boundary)} == ring_edges
    rotation = {u: [v for v in geom["rotation_cw"][u]
                    if v in disk[u]] for u in vertices}
    embedding = nx.PlanarEmbedding()
    embedding.set_data(rotation)
    embedding.check_structure()
    outer_darts = {(v, u) for u, v in zip(boundary, boundary[1:] + boundary[:1])}
    matching = [face for face in faces(embedding)
                if set(zip(face, face[1:] + face[:1])) == outer_darts]
    assert len(matching) == 1
    assert all(len(face) == 3 or face == matching[0] for face in faces(embedding))
    full = all_colorings(vertices, sorted(edges))
    rows = sorted({tuple(dict(zip(vertices, values))[v] for v in boundary)
                   for values in full})
    return {"remaining_vertices": sorted(active), "boundary_scope": boundary,
            "exterior_vertices": vertices, "exterior_edges": sorted(edges),
            "unprocessed_interior_vertices": sorted(active - set(boundary)),
            "proper_boundary_relation_rows": rows,
            "complete_exterior_colorings": full}


def replay(name, graph):
    geom = geometry(graph)
    order = geom["order"]
    stages = [exterior(graph, geom, k) for k in range(len(order) - 1, 2, -1)]
    full_colorings = all_colorings(sorted(graph), graph.edges())
    for stage in stages:
        active = stage["remaining_vertices"]
        boundary = stage["boundary_scope"]
        rows = set(stage["proper_boundary_relation_rows"])
        projected = {tuple(dict(zip(sorted(graph), values))[v] for v in active)
                     for values in full_colorings}
        joined = {values for values in all_colorings(active, graph.subgraph(active).edges())
                  if tuple(dict(zip(active, values))[v] for v in boundary) in rows}
        assert joined == projected
        stage["joined_remaining_solution_count"] = len(joined)
    initial = stages[0]
    hub = order[-1]
    assert set(initial["exterior_vertices"]) == set(graph[hub]) | {hub}
    assert len(initial["exterior_edges"]) == 2 * len(graph[hub])
    assert initial["proper_boundary_relation_rows"]
    initial_ring = initial["boundary_scope"]
    assert set(initial["proper_boundary_relation_rows"]) == {
        values for values in itertools.product(COLORS, repeat=len(initial_ring))
        if len(set(values)) <= 3 and proper(
            list(zip(initial_ring, initial_ring[1:] + initial_ring[:1])),
            dict(zip(initial_ring, values)))}
    saturation = next(j for j, stage in enumerate(stages)
                      if not stage["unprocessed_interior_vertices"])
    for j, stage in enumerate(stages[1:], 1):
        old = stages[j - 1]
        k = len(order) - 1 - j
        x = order[k]
        path = geom["steps"][k - 3]["lower_neighbors"]
        assert geom["steps"][k - 3]["vertex"] == x
        middle = path[1:-1]
        m = len(path)
        old_scope, new_scope = old["boundary_scope"], stage["boundary_scope"]
        old_rows = set(old["proper_boundary_relation_rows"])
        assert set(path) & set(old_scope) == {path[0], path[-1]}
        assert set(new_scope) == (set(old_scope) - {x}) | set(middle)
        assert len(stage["unprocessed_interior_vertices"]) == (
            len(old["unprocessed_interior_vertices"]) - (m - 2))
        all_new_rows = list(itertools.product(COLORS, repeat=len(new_scope)))
        masks = []
        derived = set()
        ring_edges = list(zip(new_scope, new_scope[1:] + new_scope[:1]))
        for values in all_new_rows:
            coloring = dict(zip(new_scope, values))
            mask = 0
            for color in COLORS:
                lifted = coloring | {x: color}
                old_row = tuple(lifted[v] for v in old_scope)
                if (proper(ring_edges, coloring) and old_row in old_rows
                        and all(color != coloring[v] for v in path)):
                    mask |= 1 << color
            masks.append(mask)
            if mask:
                derived.add(values)
        assert derived == set(stage["proper_boundary_relation_rows"])
        transition = {"eliminated": x, "m": m, "neighbor_path": path,
                      "fibre_scope": new_scope,
                      "fibre_order": "lexicographic base-4 assignments; color t is bit 1<<t",
                      "complete_fibre_masks_including_zero": masks}
        if m >= 3:
            extensions = []
            new_edges = stage["exterior_edges"]
            for row in old["proper_boundary_relation_rows"]:
                coloring = dict(zip(old_scope, row))
                t = coloring[x]
                extension = next(values for values in itertools.product(
                    [color for color in COLORS if color != t], repeat=len(middle))
                    if proper(list(zip(path, path[1:])), coloring | dict(zip(middle, values))))
                extended = coloring | dict(zip(middle, extension))
                new_row = tuple(extended[v] for v in new_scope)
                assert new_row in derived
                # The same chosen path works for every full old fibre witness.
                for full_values in old["complete_exterior_colorings"]:
                    full = dict(zip(old["exterior_vertices"], full_values))
                    if tuple(full[v] for v in old_scope) == row:
                        full.update(dict(zip(middle, extension)))
                        assert proper(new_edges, full)
                extensions.append({"old_boundary_row": row, "new_boundary_row": new_row,
                                   "middle_colors": extension})
            transition["rowwise_same_witness_extensions"] = extensions
            assert derived
        else:
            assert set(stage["exterior_vertices"]) == set(old["exterior_vertices"])
            new_edge = tuple(sorted((path[0], path[-1])))
            assert new_edge not in set(map(tuple, old["exterior_edges"]))
            assert set(map(tuple, stage["exterior_edges"])) == (
                set(map(tuple, old["exterior_edges"])) | {new_edge})
            survivors = [values for values in old["complete_exterior_colorings"]
                         if dict(zip(old["exterior_vertices"], values))[path[0]] !=
                         dict(zip(old["exterior_vertices"], values))[path[-1]]]
            assert survivors == stage["complete_exterior_colorings"]
            equal_rows = [row for row in old["proper_boundary_relation_rows"]
                          if dict(zip(old_scope, row))[path[0]] ==
                          dict(zip(old_scope, row))[path[-1]]]
            transition.update({"added_original_edge": new_edge,
                               "old_rows_lost_by_endpoint_equality": equal_rows,
                               "old_complete_colorings_lost": len(old["complete_exterior_colorings"]) - len(survivors)})
            assert bool(derived) == (len(equal_rows) < len(old_rows))
        if j > saturation:
            assert m == 2
        stage["transition"] = transition
    _, original_embedding = nx.check_planarity(graph)
    face_triangles = {frozenset(face) for face in faces(original_embedding)}
    separating_triangles = [triangle for triangle in itertools.combinations(sorted(graph), 3)
                            if all(graph.has_edge(u, v) for u, v in itertools.combinations(triangle, 2))
                            and frozenset(triangle) not in face_triangles]
    if len(graph) > 4 and not separating_triangles:
        terminal = stages[-2]
        assert len(terminal["remaining_vertices"]) == 4
        last_step = stages[-1]["transition"]
        assert last_step["m"] == 2
        assert len(terminal["exterior_vertices"]) == len(graph)
        assert set(map(tuple, terminal["exterior_edges"])) == (
            {tuple(sorted(edge)) for edge in graph.edges()} - {tuple(last_step["added_original_edge"])})
    return {"name": name, "original_edges": sorted(tuple(sorted(edge)) for edge in graph.edges()),
            "geometry": geom, "stages": stages, "saturation_stage_index": saturation,
            "separating_triangles": separating_triangles,
            "saturation_remaining_vertices": stages[saturation]["remaining_vertices"]}


def path_replay():
    checks = []
    for m in range(2, 9):
        for t in COLORS:
            available = [c for c in COLORS if c != t]
            for a, b in itertools.product(available, repeat=2):
                count = sum(all(x != y for x, y in zip((a,) + middle, middle + (b,)))
                            for middle in itertools.product(available, repeat=m - 2))
                assert (count > 0) == (m >= 3 or a != b)
                expected = ((2 ** (m - 1) + 2 * (-1) ** (m - 1)) // 3 if a == b else
                            (2 ** (m - 1) - (-1) ** (m - 1)) // 3)
                assert count == expected
                checks.append({"m": m, "forbidden_color": t,
                               "endpoint_colors": [a, b], "middle_fillings": count})
    return checks


def wheel_negative_control():
    # A real chordless disk. One colouring has all three Kempe locks, while
    # another separates the same cofacial endpoints. Do not splice the witnesses.
    graph = nx.wheel_graph(5)
    p, x, q, y, hub = 1, 2, 3, 4, 0
    before = {p: 0, q: 0, x: 1, y: 2, hub: 3}
    after = {p: 0, q: 2, x: 1, y: 1, hub: 3}
    assert proper(graph.edges(), before) and proper(graph.edges(), after)
    paths = [[p, v, q] for v in (x, y, hub)]
    for d, path in zip((1, 2, 3), paths):
        assert [before[v] for v in path] == [0, d, 0]
        assert all(graph.has_edge(u, v) for u, v in zip(path, path[1:]))
    completed = graph.copy()
    completed.add_edge(p, q)
    assert nx.check_planarity(completed)[0] and proper(completed.edges(), after)
    return {"graph_edges": sorted(tuple(sorted(e)) for e in graph.edges()),
            "ordered_boundary": [p, x, q, y], "ear_endpoints": [p, q],
            "single_locked_witness": before, "same_witness_three_paths": paths,
            "different_witness_with_distinct_endpoints": after,
            "warning": "Three locks for one witness do not imply equality in every witness."}


def abstract_empty_control():
    scope = [0, 1, 2, 3]
    rows = [row for row in itertools.product(COLORS, repeat=4)
            if row[0] == row[2] and all(row[u] != row[v]
                for u, v in zip(scope, scope[1:] + scope[:1]))]
    assert rows and not [row for row in rows if row[0] != row[2]]
    return {"old_scope": scope, "old_proper_boundary_rows": rows,
            "close_edge": [0, 2], "new_relation_rows": [],
            "scope": "Abstract relation only; no planar disk realization is asserted."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    cases = [replay(f"atlas-{j}", graph)
             for j, graph in enumerate(nx.graph_atlas_g())
             if 4 <= len(graph) <= 7 and graph.number_of_edges() == 3 * len(graph) - 6
             and nx.check_planarity(graph)[0]]
    assert len(cases) == 9
    paths = path_replay()
    transitions = [stage["transition"] for case in cases for stage in case["stages"]
                   if "transition" in stage]
    report = {"schema": "four-color-reverse-shelling-verification-v1",
              "scope": "Finite complete exterior relations/fibres, no no-lock or 4CT theorem.",
              "networkx_version": nx.__version__, "cases": cases,
              "fixed_endpoint_three_color_path_checks": paths,
              "single_witness_negative_control": wheel_negative_control(),
              "abstract_empty_relation_control": abstract_empty_control(),
              "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                  for path in (Path(__file__), ROOT / "scripts/four_color_shelling_fan_verification.py",
                               ROOT / "scripts/four_color_shelling_verification.py")},
              "totals": {"original_graphs": len(cases),
                         "exterior_stages": sum(len(case["stages"]) for case in cases),
                         "transitions": len(transitions),
                         "m_ge_3_transitions": sum(step["m"] >= 3 for step in transitions),
                         "m_eq_2_transitions": sum(step["m"] == 2 for step in transitions),
                         "same_witness_row_extensions": sum(len(step.get("rowwise_same_witness_extensions", []))
                                                            for step in transitions),
                         "complete_fibre_masks_including_zero": sum(len(step["complete_fibre_masks_including_zero"])
                                                                    for step in transitions),
                         "zero_fibre_masks": sum(step["complete_fibre_masks_including_zero"].count(0)
                                                 for step in transitions),
                         "endpoint_path_checks": len(paths)}}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["totals"], sort_keys=True))


if __name__ == "__main__":
    main()
