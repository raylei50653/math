#!/usr/bin/env python3
"""Replay canonical fan budgets, degree-four forward repair, and exact fibres.

This is finite original-edge evidence. The general budget and Kempe arguments
are paper lemmas; this checker neither proves 4CT nor repairs fans of size >=5.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx
from networkx.algorithms.planar_drawing import get_canonical_ordering

from four_color_shelling_verification import bipyramid, faces, induced_embedding


COLORS = tuple(range(4))


def proper(edges, coloring):
    return all(coloring[u] != coloring[v] for u, v in edges)


def geometry(graph, outer=None, order=None):
    planar, embedding = nx.check_planarity(graph)
    assert planar
    assert all(len(face) == 3 for face in faces(embedding))
    if outer is None:
        outer = faces(embedding)[0]
    else:
        assert any(outer == face[j:] + face[:j]
                   for face in faces(embedding) for j in range(len(face)))
    if order is None:
        candidate = get_canonical_ordering(embedding, outer)
        order = [vertex for vertex, _ in candidate]
    assert len(order) == len(graph) and set(order) == set(graph)
    assert order[:2] == outer[:2] and order[-1] == outer[-1]
    roots = order[:2]
    boundaries = {}
    steps = []
    parent_edges = []
    for k in range(3, len(order) + 1):
        active = set(order[:k])
        induced = induced_embedding(embedding, active)
        boundary = induced.traverse_face(*roots)
        assert len(boundary) == len(set(boundary))
        assert nx.is_biconnected(graph.subgraph(active))
        for face in faces(induced):
            if face != boundary:
                # Face traversal can start at another vertex.
                face_edges = set(zip(face, face[1:] + face[:1]))
                outer_edges = set(zip(boundary, boundary[1:] + boundary[:1]))
                assert face_edges == outer_edges or len(face) == 3
        boundaries[k] = boundary
        removed = set(graph) - active
        assert {v for u in removed for v in graph[u] if v in active} <= set(boundary)
        if k == 3:
            continue
        x = order[k - 1]
        previous = boundaries[k - 1]
        path = [previous[0]] + list(reversed(previous[1:]))
        neighbors = set(graph[x]) & set(order[:k - 1])
        indices = [j for j, vertex in enumerate(path) if vertex in neighbors]
        assert len(indices) >= 2
        assert indices == list(range(min(indices), max(indices) + 1))
        interval = path[min(indices):max(indices) + 1]
        swallowed = interval[1:-1]
        assert set(boundary) == (set(previous) - set(swallowed)) | {x}
        assert len(boundary) == len(previous) + 3 - len(interval)
        parent_edges.extend((child, x) for child in swallowed)
        steps.append({"vertex": x, "lower_neighbors": interval,
                      "m": len(interval), "swallowed": swallowed,
                      "boundary_before": previous, "boundary_after": boundary})
    tree = nx.DiGraph()
    tree.add_nodes_from(order[2:])
    tree.add_edges_from(parent_edges)
    assert nx.is_tree(tree.to_undirected())
    assert all(tree.out_degree(v) == (0 if v == order[-1] else 1) for v in tree)
    positions = {v: j for j, v in enumerate(order)}
    assert all(positions[child] < positions[parent] and graph.has_edge(child, parent)
               for child, parent in parent_edges)
    budget = sum(step["m"] - 2 for step in steps)
    hard_count = sum(step["m"] >= 5 for step in steps)
    assert budget == len(graph) - 3
    assert hard_count <= (len(graph) - 3) // 3
    return {"order": order, "outer_face": outer,
            "rotation_cw": {v: list(embedding.neighbors_cw_order(v)) for v in graph},
            "boundaries": boundaries,
            "steps": steps, "middle_parent_edges": parent_edges,
            "swallowed_budget": budget, "hard_fans": hard_count,
            "hard_fan_bound": (len(graph) - 3) // 3}


def fixed_triangle_colorings(graph, order):
    """All proper colors with the first triangle fixed to 0,1,2."""
    coloring = dict(zip(order[:3], range(3)))
    assert proper(graph.subgraph(order[:3]).edges(), coloring)

    def visit(j):
        if j == len(order):
            yield dict(coloring)
            return
        vertex = order[j]
        forbidden = {coloring[u] for u in graph[vertex] if u in coloring}
        for color in COLORS:
            if color not in forbidden:
                coloring[vertex] = color
                yield from visit(j + 1)
        coloring.pop(vertex, None)

    yield from visit(3)


def bicolor_component(graph, coloring, source, pair):
    active = [v for v in graph if coloring[v] in pair]
    return nx.node_connected_component(graph.subgraph(active), source)


def repair_small_fan(graph, coloring, interval):
    used = {coloring[v] for v in interval}
    if len(used) <= 3:
        return dict(coloring), min(set(COLORS) - used), "already_three"
    assert len(interval) == 4
    p, q, r, s = interval
    a, b, c, d = (coloring[v] for v in interval)
    component = bicolor_component(graph, coloring, p, {a, c})
    pair = {a, c}
    missing = a
    branch = "first_opposite_pair"
    if r in component:
        component = bicolor_component(graph, coloring, q, {b, d})
        assert s not in component
        pair = {b, d}
        missing = b
        branch = "second_opposite_pair"
    replacement = {color: next(iter(pair - {color})) for color in pair}
    recolored = {v: replacement[color] if v in component else color
                 for v, color in coloring.items()}
    assert proper(graph.edges(), recolored)
    assert missing not in {recolored[v] for v in interval}
    return recolored, missing, branch


def forward_replay(graph, geom):
    result = []
    order = geom["order"]
    for k, step in enumerate(geom["steps"], 4):
        prefix = graph.subgraph(order[:k - 1])
        counts = {"already_three": 0, "first_opposite_pair": 0,
                  "second_opposite_pair": 0, "rainbow_hard_fan": 0}
        tested = 0
        for coloring in fixed_triangle_colorings(graph, order[:k - 1]):
            tested += 1
            if step["m"] >= 5:
                counts["rainbow_hard_fan"] += len({coloring[v] for v in step["lower_neighbors"]}) == 4
                continue
            recolored, color, branch = repair_small_fan(prefix, coloring, step["lower_neighbors"])
            counts[branch] += 1
            recolored[step["vertex"]] = color
            assert proper(graph.subgraph(order[:k]).edges(), recolored)
        assert step["m"] >= 5 or tested == sum(counts.values())
        result.append({"vertex": step["vertex"], "m": step["m"],
                       "fixed_triangle_prefix_colorings": tested, **counts})
    return result


def assignments(vertices):
    for values in itertools.product(COLORS, repeat=len(vertices)):
        yield values, dict(zip(vertices, values))


def direct_relation(graph, active, boundary):
    """Independent existential enumeration using only original processed edges."""
    removed = sorted(set(graph) - set(active))
    outside_edges = [(u, v) for u, v in graph.edges() if u in removed or v in removed]
    relation = set()
    for _, coloring in assignments(removed + boundary):
        if proper(outside_edges, coloring):
            relation.add(tuple(coloring[v] for v in boundary))
    return relation


def exact_replay(graph, geom):
    order = geom["order"]
    full_colorings = [coloring for _, coloring in assignments(order)
                      if proper(graph.edges(), coloring)]
    stages = []
    previous_relation = None
    previous_boundary = None
    for k in range(len(order), 2, -1):
        active = order[:k]
        boundary = geom["boundaries"][k]
        relation = direct_relation(graph, active, boundary)
        projected = {tuple(coloring[v] for v in active) for coloring in full_colorings}
        joined = {values for values, coloring in assignments(active)
                  if proper(graph.subgraph(active).edges(), coloring)
                  and tuple(coloring[v] for v in boundary) in relation}
        assert joined == projected
        stage = {"active": active, "boundary": boundary,
                 "complete_relation_rows": sorted(relation),
                 "all_boundary_assignments": 4 ** len(boundary),
                 "joined_original_edge_solutions": len(joined)}
        if previous_relation is not None:
            x = order[k]
            old_remaining = set(previous_boundary) - {x}
            assert old_remaining <= set(boundary)
            neighbors = [u for u in graph[x] if u in active]
            fibres = []
            derived = set()
            for values, coloring in assignments(boundary):
                colors = []
                for color in COLORS:
                    lifted = dict(coloring)
                    lifted[x] = color
                    old_row = tuple(lifted[v] for v in previous_boundary)
                    if old_row in previous_relation and all(color != coloring[u] for u in neighbors):
                        colors.append(color)
                fibres.append({"assignment": values, "colors": colors})
                if colors:
                    derived.add(values)
            assert derived == relation
            stage["eliminated"] = x
            stage["complete_fibres_including_empty"] = fibres
        stages.append(stage)
        previous_relation, previous_boundary = relation, boundary
    return {"original_full_colorings": len(full_colorings), "stages": stages}


def unions_of_components(components):
    for bits in itertools.product((False, True), repeat=len(components)):
        yield set().union(*(component for bit, component in zip(bits, components) if bit))


def same_witness_lift_replay(graph, geom):
    """Compare exterior boundary blocks with brute force at one fixed witness.

    The first triangle is fixed to 0,1,2. Every full colouring has such a global
    colour permutation; checking all six pairs covers the omitted permutations.
    This is a lift criterion for this witness, not membership in R for a new
    boundary assignment with a potentially different exterior witness.
    """
    order = geom["order"]
    totals = {"fixed_triangle_full_colorings": 0, "splits": 0,
              "selected_active_component_unions": 0,
              "lift_exists": 0, "lift_obstructed": 0}
    for coloring in fixed_triangle_colorings(graph, order):
        totals["fixed_triangle_full_colorings"] += 1
        for k in range(3, len(order)):
            totals["splits"] += 1
            active = set(order[:k])
            removed = set(graph) - active
            boundary = set(geom["boundaries"][k])
            inside = graph.subgraph(active)
            outside = nx.Graph()
            outside.add_nodes_from(removed | boundary)
            outside.add_edges_from((u, v) for u, v in graph.edges()
                                   if u in removed or v in removed)
            for pair in itertools.combinations(COLORS, 2):
                in_pair = inside.subgraph(v for v in inside if coloring[v] in pair)
                out_pair = outside.subgraph(v for v in outside if coloring[v] in pair)
                inside_components = list(nx.connected_components(in_pair))
                outside_components = list(nx.connected_components(out_pair))
                blocks = [component & boundary for component in outside_components
                          if component & boundary]
                outside_signatures = {frozenset(selected & boundary)
                                      for selected in unions_of_components(outside_components)}
                eligible_removed = sorted(v for v in removed if coloring[v] in pair)
                for selected in unions_of_components(inside_components):
                    totals["selected_active_component_unions"] += 1
                    signature = selected & boundary
                    criterion = all(not (block & signature) or block <= signature for block in blocks)
                    brute_components = frozenset(signature) in outside_signatures
                    assert criterion == brute_components
                    brute_vertex_switch = False
                    for bits in itertools.product((False, True), repeat=len(eligible_removed)):
                        switched = selected | {v for bit, v in zip(bits, eligible_removed) if bit}
                        recolored = {v: sum(pair) - color if v in switched else color
                                     for v, color in coloring.items()}
                        if proper(graph.edges(), recolored):
                            brute_vertex_switch = True
                            break
                    assert criterion == brute_vertex_switch
                    totals["lift_exists" if criterion else "lift_obstructed"] += 1
    return totals


def family_geometry(kind, parameter):
    graph = nx.complete_graph(3)
    a, b = 0, 1
    path = [a, 2, b]
    order = [a, b, 2]
    pattern = []

    def insert(interval):
        nonlocal path
        x = len(graph)
        start = path.index(interval[0])
        assert path[start:start + len(interval)] == interval
        graph.add_edges_from((x, vertex) for vertex in interval)
        path = path[:start + 1] + [x] + path[start + len(interval) - 1:]
        order.append(x)
        pattern.append(len(interval))

    if kind == "sharp":
        for _ in range(parameter):
            insert(path[:2])
            insert(path[:2])
            assert len(path) == 5
            insert(path[:])
        assert pattern == [2, 2, 5] * parameter
    else:
        assert kind == "easy_large_boundary"
        for _ in range(parameter):
            insert(path[:2])
        assert len(path) == parameter + 3
        for _ in range(parameter):
            insert(path[:4])
        assert pattern == [2] * parameter + [4] * parameter
    assert len(path) == 3
    planar, embedding = nx.check_planarity(graph)
    assert planar
    outer = next(face for face in faces(embedding) if set(face) == set(path))
    outer = next(outer[j:] + outer[:j] for j in range(3)
                 if set((outer[j], outer[(j + 1) % 3])) == {a, b})
    order[:2] = outer[:2]
    geom = geometry(graph, outer, order)
    assert [step["m"] for step in geom["steps"]] == pattern
    if kind == "sharp":
        assert geom["hard_fans"] == geom["hard_fan_bound"] == parameter
    else:
        assert geom["hard_fans"] == 0
        assert max(map(len, geom["boundaries"].values())) == parameter + 3
    return {"kind": kind, "parameter": parameter, "vertices": len(graph),
            "graph_edges": sorted(tuple(sorted(edge)) for edge in graph.edges()),
            "geometry": geom}


def t5_control():
    graph = bipyramid(3)
    planar, embedding = nx.check_planarity(graph)
    assert planar
    outer = embedding.traverse_face(1, 4)
    assert set(outer) == {0, 1, 4}
    geom = geometry(graph, outer)
    assert geom["order"] == [1, 4, 2, 3, 0]
    boundary = geom["boundaries"][4]
    assert boundary == [1, 4, 2, 3]
    relation = direct_relation(graph, geom["order"][:4], boundary)
    expected = {values for values, _ in assignments(boundary) if len(set(values)) <= 3}
    assert relation == expected and len(relation) == 232
    prefix = graph.subgraph(geom["order"][:4])
    before = {1: 0, 2: 1, 3: 2, 4: 2}
    after = dict(before)
    after[3] = 3
    assert proper(prefix.edges(), before) and proper(prefix.edges(), after)
    assert tuple(before[v] for v in boundary) in relation
    assert tuple(after[v] for v in boundary) not in relation
    active_component = bicolor_component(prefix, before, 3, {2, 3})
    assert active_component == {3}
    full_witness = dict(before)
    full_witness[0] = 3
    assert proper(graph.edges(), full_witness)
    full_component = bicolor_component(graph, full_witness, 3, {2, 3})
    assert full_component == {0, 3, 4}
    raw_colors = [color for color in COLORS if color not in {before[1], before[2]}]
    exact_colors = []
    for color in raw_colors:
        lifted = dict(before)
        lifted[3] = color
        if tuple(lifted[v] for v in boundary) in relation:
            exact_colors.append(color)
    assert raw_colors == [2, 3] and exact_colors == [2]
    replay = exact_replay(graph, geom)
    assert replay["original_full_colorings"] == 24
    proper_prefix = [coloring for _, coloring in assignments(geom["order"][:4])
                     if proper(prefix.edges(), coloring)]
    assert len(proper_prefix) == 48
    return {"graph_edges": sorted(tuple(sorted(edge)) for edge in graph.edges()),
            "geometry": geom, "exact_replay": replay,
            "R1_rows": len(relation), "proper_diamond_colorings": 48,
            "proper_diamond_colorings_rejected_by_R1": 24,
            "active_coloring_before": before, "active_coloring_after": after,
            "active_swap_component": sorted(active_component),
            "full_witness": full_witness, "full_swap_component": sorted(full_component),
            "next_two_neighbor_raw_fibre": raw_colors,
            "next_two_neighbor_exact_fibre": exact_colors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    cases = []
    for index, graph in enumerate(nx.graph_atlas_g()):
        n = len(graph)
        if n >= 4 and graph.number_of_edges() == 3 * n - 6 and nx.check_planarity(graph)[0]:
            geom = geometry(graph)
            cases.append({"name": f"atlas-{index}", "vertices": n,
                          "graph_edges": sorted(tuple(sorted(edge)) for edge in graph.edges()),
                          "geometry": geom, "forward_replay": forward_replay(graph, geom),
                          "exact_replay": exact_replay(graph, geom),
                          "same_witness_lift_replay": same_witness_lift_replay(graph, geom)})
    graph = nx.icosahedral_graph()
    geom = geometry(graph)
    cases.append({"name": "icosahedron", "vertices": len(graph),
                  "graph_edges": sorted(tuple(sorted(edge)) for edge in graph.edges()),
                  "geometry": geom, "forward_replay": forward_replay(graph, geom)})
    for r in (4, 5, 8, 16, 32):
        graph = bipyramid(r)
        planar, embedding = nx.check_planarity(graph)
        assert planar
        outer = next(face for face in faces(embedding) if set(face) == {0, 1, r})
        outer = next(outer[j:] + outer[:j] for j in range(3)
                     if set((outer[j], outer[(j + 1) % 3])) == {0, 1})
        geom = geometry(graph, outer)
        assert geom["steps"][-1]["vertex"] == r and geom["steps"][-1]["m"] == r
        cases.append({"name": f"bipyramid-{r}", "vertices": len(graph),
                      "graph_edges": sorted(tuple(sorted(edge)) for edge in graph.edges()),
                      "geometry": geom})
    assert len(cases) == 15
    t5 = t5_control()
    families = [family_geometry(kind, parameter)
                for kind in ("sharp", "easy_large_boundary")
                for parameter in (1, 2, 4, 8, 16, 32)]
    replay_steps = [step for case in cases for step in case.get("forward_replay", [])]
    report = {"schema": "four-color-shelling-fan-verification-v1",
              "scope": "finite replay; no general fan>=5 repair, 4CT proof, or new Lean theorem",
              "networkx_version": nx.__version__,
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "geometry_dependency_sha256": hashlib.sha256(Path(__file__).with_name(
                  "four_color_shelling_verification.py").read_bytes()).hexdigest(),
              "cases": cases, "T5_control": t5, "families": families,
              "totals": {"geometry_cases": len(cases),
                         "exact_relation_cases": sum("exact_replay" in case for case in cases),
                         "exact_relation_stages": sum(len(case["exact_replay"]["stages"])
                                                      for case in cases if "exact_replay" in case),
                         "forward_replay_cases": sum("forward_replay" in case for case in cases),
                         "small_fan_prefix_colorings": sum(step["fixed_triangle_prefix_colorings"]
                                                           for step in replay_steps if step["m"] <= 4),
                         "first_opposite_pair_repairs": sum(step["first_opposite_pair"] for step in replay_steps),
                         "second_opposite_pair_repairs": sum(step["second_opposite_pair"] for step in replay_steps),
                         "same_witness_lift_requests": sum(case["same_witness_lift_replay"][
                             "selected_active_component_unions"] for case in cases if "same_witness_lift_replay" in case),
                         "same_witness_lift_obstructions": sum(case["same_witness_lift_replay"][
                             "lift_obstructed"] for case in cases if "same_witness_lift_replay" in case),
                         "explicit_family_cases": len(families)}}
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded)
        print(json.dumps(report["totals"], sort_keys=True))
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
