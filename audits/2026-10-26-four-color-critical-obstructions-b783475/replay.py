#!/usr/bin/env python3
"""Finite original-edge checks for critical-core colouring obstructions.

This audit is self-contained and never imports a production solver. Exhaustive
literal-colour DFS decides each named graph and each vertex/edge deletion.
Saved SAT assignments and Kempe paths are separately checked on original edges.
One deletion witness is not an UNSAT certificate; final UNSAT decisions come
from independent exhaustive original-edge DFS. No planar 4CT claim is made.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time


AUDIT = Path(__file__).resolve().parent
BASE = "b783475a1cc24ff126c09ad276816a3b7eb4e8d8"
PALETTE = tuple(range(4))


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def canonical_cycle(vertices):
    row = tuple(vertices)
    return min(oriented[i:] + oriented[:i]
               for oriented in (row, row[::-1]) for i in range(len(row)))


def complete_graph(n):
    return dict(vertices=list(range(n)), edges=[list(e) for e in combinations(range(n), 2)], fixed=[])


def mycielski(graph):
    n = len(graph["vertices"])
    assert graph["vertices"] == list(range(n))
    edges = [list(e) for e in graph["edges"]]
    for u, v in graph["edges"]:
        edges.extend([[u, n + v], [v, n + u]])
    edges.extend([[n + v, 2 * n] for v in range(n)])
    return dict(vertices=list(range(2 * n + 1)), edges=edges, fixed=[])


def make_cases():
    c5 = dict(vertices=list(range(5)), edges=[[v, (v + 1) % 5] for v in range(5)], fixed=[])
    myc_k4 = mycielski(complete_graph(4))
    redundant = dict(myc_k4, edges=myc_k4["edges"] + [[4, 5]])
    return [
        ("K5", complete_graph(5), "bare vertex-and-edge critical control"),
        ("Mycielski_twice_C5", mycielski(mycielski(c5)), "triangle-free bare vertex-and-edge critical control"),
        ("Mycielski_K4_plus_clone_edge", redundant, "vertex-minimal does not imply edge-minimal"),
        ("two_fixed_equal_endpoints", dict(vertices=[0, 1], edges=[[0, 1]], fixed=[[0, 0], [1, 0]]),
         "fixed domains forbid arbitrary Kempe swaps"),
    ]


def effective_domains(graph):
    allowed = {v: set(PALETTE) for v in graph["vertices"]}
    for vertex, colour in graph.get("fixed", []):
        allowed[vertex].intersection_update((colour,))
    return {v: tuple(sorted(values)) for v, values in allowed.items()}


def adjacency(graph):
    result = {v: set() for v in graph["vertices"]}
    for u, v in graph["edges"]:
        assert u in result and v in result and u != v
        result[u].add(v)
        result[v].add(u)
    assert len({frozenset(e) for e in graph["edges"]}) == len(graph["edges"])
    return result


def oracle(graph):
    """Exhaust literal-colour assignments; use only original edges and fixes."""
    vertices = graph["vertices"]
    positions = {v: i for i, v in enumerate(vertices)}
    allowed = effective_domains(graph)
    adjacent = adjacency(graph)
    assignment = {}
    counts = dict(search_nodes=0, colour_trials=0)

    def visit():
        counts["search_nodes"] += 1
        if len(assignment) == len(vertices):
            return True
        vertex = max((v for v in vertices if v not in assignment),
                     key=lambda v: (len({assignment[w] for w in adjacent[v] if w in assignment}),
                                    len(adjacent[v]), -positions[v]))
        forbidden = {assignment[w] for w in adjacent[vertex] if w in assignment}
        for colour in allowed[vertex]:
            counts["colour_trials"] += 1
            if colour in forbidden:
                continue
            assignment[vertex] = colour
            if visit():
                return True
        assignment.pop(vertex, None)
        return False

    possible = visit()
    colours = [assignment[v] for v in vertices] if possible else None
    if possible:
        check_colouring(graph, colours)
    return dict(possible=possible, colors=colours, counts=counts,
                algorithm="exhaustive original-edge literal-colour DSATUR DFS; no symmetry pruning")


def check_colouring(graph, colours):
    assert colours is not None and len(colours) == len(graph["vertices"])
    assert all(type(c) is int and c in PALETTE for c in colours)
    assignment = dict(zip(graph["vertices"], colours))
    allowed = effective_domains(graph)
    assert all(assignment[v] in allowed[v] for v in graph["vertices"])
    assert all(assignment[u] != assignment[v] for u, v in graph["edges"])
    return assignment


def delete_vertex(graph, vertex):
    return dict(vertices=[v for v in graph["vertices"] if v != vertex],
                edges=[e for e in graph["edges"] if vertex not in e],
                fixed=[p for p in graph.get("fixed", []) if p[0] != vertex])


def delete_edge(graph, index):
    return dict(graph, edges=graph["edges"][:index] + graph["edges"][index + 1:])


def bichromatic_path(graph, colours, source, target, pair):
    """Deterministic shortest path in one actual two-colour subgraph."""
    assignment = dict(zip(graph["vertices"], colours))
    adjacent = adjacency(graph)
    assert assignment[source] in pair and assignment[target] in pair
    parent = {source: None}
    pending = deque([source])
    while pending and target not in parent:
        v = pending.popleft()
        for w in sorted(adjacent[v]):
            if assignment[w] in pair and w not in parent:
                parent[w] = v
                pending.append(w)
    if target not in parent:
        return None
    path = []
    v = target
    while v is not None:
        path.append(v)
        v = parent[v]
    path.reverse()
    assert len(set(path)) == len(path)
    assert all(v in adjacent[u] for u, v in zip(path, path[1:]))
    assert all(assignment[v] in pair for v in path)
    assert all(assignment[u] != assignment[v] for u, v in zip(path, path[1:]))
    return path


def graph_stats(graph):
    adjacent = adjacency(graph)
    triangles = sum(1 for u in adjacent for v in adjacent[u] if u < v
                    for w in adjacent[u] & adjacent[v] if v < w)
    return dict(vertices=len(graph["vertices"]), edges=len(graph["edges"]),
                minimum_degree=min(map(len, adjacent.values()), default=0), triangles=triangles)


def audit_case(name, graph, role):
    whole = oracle(graph)
    assert not whole["possible"], name
    adjacent = adjacency(graph)
    allowed = effective_domains(graph)
    bare = all(values == PALETTE for values in allowed.values())
    vertex_records = []
    for v in graph["vertices"]:
        reduced = delete_vertex(graph, v)
        result = oracle(reduced)
        record = dict(vertex=v, oracle=result)
        if result["possible"]:
            assignment = check_colouring(reduced, result["colors"])
            neighbour_colours = {assignment[w] for w in adjacent[v]}
            assert set(allowed[v]) <= neighbour_colours
            record["neighbour_colours"] = sorted(neighbour_colours)
            record["all_owner_domain_colours_blocked"] = True
        vertex_records.append(record)

    edge_records = []
    path_histogram = Counter()
    unique_saved_cycles = set()
    for index, (x, y) in enumerate(graph["edges"]):
        reduced = delete_edge(graph, index)
        result = oracle(reduced)
        record = dict(edge=[x, y], edge_critical=result["possible"], oracle=result)
        if result["possible"]:
            assignment = check_colouring(reduced, result["colors"])
            violations = [e for e in graph["edges"] if assignment[e[0]] == assignment[e[1]]]
            assert violations == [[x, y]]
            colour = assignment[x]
            assert assignment[y] == colour
            remaining_x = set(allowed[x]) - {assignment[w] for w in adjacent[x] - {y}}
            remaining_y = set(allowed[y]) - {assignment[w] for w in adjacent[y] - {x}}
            assert remaining_x == remaining_y == {colour}
            record.update(endpoint_colour=colour,
                          remaining_domains=[sorted(remaining_x), sorted(remaining_y)],
                          witness_violates_exactly_deleted_original_edge=True,
                          same_coloring_paths=[])
            for other in PALETTE:
                if other == colour:
                    continue
                path = bichromatic_path(reduced, result["colors"], x, y, (colour, other))
                if bare:
                    assert path is not None, (name, record["edge"], colour, other)
                    assert (len(path) - 1) % 2 == 0 and len(path) >= 3
                    # The deleted edge closes this simple even path to an odd cycle.
                    assert frozenset((path[-1], path[0])) == frozenset((x, y))
                    cycle = path[:]
                    assert len(cycle) % 2 == 1
                    unique_saved_cycles.add(canonical_cycle(cycle))
                    path_histogram[len(path) - 1] += 1
                else:
                    cycle = None
                record["same_coloring_paths"].append(dict(colours=[colour, other], path=path,
                                                           odd_cycle=cycle))
            record["bare_kempe_necessity_applied"] = bare
            if bare:
                assert len({canonical_cycle(p["odd_cycle"]) for p in record["same_coloring_paths"]}) == 3
        edge_records.append(record)

    all_vertices_critical = all(r["oracle"]["possible"] for r in vertex_records)
    all_edges_critical = all(r["edge_critical"] for r in edge_records)
    if name in ("K5", "Mycielski_twice_C5"):
        assert bare and all_vertices_critical and all_edges_critical
    if name == "Mycielski_twice_C5":
        assert graph_stats(graph)["triangles"] == 0
        assert len(edge_records) == 71 and len(vertex_records) == 23
        assert path_histogram == Counter({4: 213})
    if name == "Mycielski_K4_plus_clone_edge":
        assert all_vertices_critical and not all_edges_critical
        clone_edge = next(r for r in edge_records if r["edge"] == [4, 5])
        assert not clone_edge["edge_critical"]
    if name == "two_fixed_equal_endpoints":
        assert all_vertices_critical and all_edges_critical and not bare
        assert all(r["path"] is None for r in edge_records[0]["same_coloring_paths"])
    return dict(name=name, role=role, graph=graph, graph_sha256=digest(graph),
                graph_stats=graph_stats(graph), effective_domains=[[v, list(allowed[v])] for v in graph["vertices"]],
                whole_graph_oracle=whole, vertex_deletions=vertex_records, edge_deletions=edge_records,
                summary=dict(vertex_minimal=all_vertices_critical, edge_minimal=all_edges_critical,
                             edge_critical_count=sum(r["edge_critical"] for r in edge_records),
                             redundant_edge_count=sum(not r["edge_critical"] for r in edge_records),
                             redundant_edges=[r["edge"] for r in edge_records if not r["edge_critical"]],
                             bare_four_colour_domains=bare,
                             same_coloring_path_length_histogram=dict(sorted(path_histogram.items())),
                             total_saved_necessary_paths=sum(path_histogram.values()),
                             saved_odd_cycle_occurrences=sum(path_histogram.values()),
                             unique_saved_odd_cycles=len(unique_saved_cycles),
                             canonical_unique_saved_odd_cycles=[list(c) for c in sorted(unique_saved_cycles)],
                             edge_deletion_oracle_trials=sum(r["oracle"]["counts"]["colour_trials"] for r in edge_records)))


def theta_control():
    """An actual planar triangle-free graph with one blocked exterior row only."""
    # Layout: x=(0,0), y=(4,0); three arcs via y=1,2,3 can be nested without
    # crossing. Three length-four x-y paths and the direct x-y edge form a
    # planar subdivision of parallel edges. Only the stated graph is used.
    graph = dict(vertices=list(range(11)), edges=[[0, 1]], fixed=[])
    blocked = {0: 0, 1: 0}
    positive = {0: 0, 1: 1}
    paths = []
    for other in (1, 2, 3):
        a, b, c = 2 + 3 * (other - 1), 3 + 3 * (other - 1), 4 + 3 * (other - 1)
        path = [0, a, b, c, 1]
        graph["edges"].extend([[u, v] for u, v in zip(path, path[1:])])
        blocked.update({a: other, b: 0, c: other})
        positive.update({a: 1, b: 0, c: 2})
        paths.append(dict(colours=[0, other], path=path, odd_cycle=path))
    deleted = delete_edge(graph, 0)
    blocked_colours = [blocked[v] for v in graph["vertices"]]
    positive_colours = [positive[v] for v in graph["vertices"]]
    check_colouring(deleted, blocked_colours)
    check_colouring(graph, positive_colours)
    adjacent = adjacency(graph)
    remaining = [sorted(set(PALETTE) - {blocked[w] for w in adjacent[v] - {1 - v}}) for v in (0, 1)]
    assert remaining == [[0], [0]]
    for record in paths:
        path = bichromatic_path(deleted, blocked_colours, 0, 1, record["colours"])
        assert path == record["path"]
    result = oracle(graph)
    assert result["possible"] and graph_stats(graph)["triangles"] == 0
    assert graph_stats(graph)["vertices"] == 11 and graph_stats(graph)["edges"] == 13
    return dict(name="three_length_four_paths_plus_edge", graph=graph, graph_sha256=digest(graph),
                graph_stats=graph_stats(graph), whole_graph_oracle=result,
                deleted_edge=[0, 1], blocked_deleted_edge_colors=blocked_colours,
                blocked_remaining_domains=remaining, three_same_coloring_paths=paths,
                explicit_original_graph_three_colour_witness=positive_colours,
                assertions=dict(planar_by_parallel_path_subdivision_construction=True,
                                triangle_free_checked=True, blocked_row_and_three_kempe_paths_exist=True,
                                original_graph_three_colour_witness_checked=True,
                                existential_blocked_row_is_not_unsatisfiability=True))


def multipartite_control():
    """Every edge has four odd cycles, but the graph is explicitly 4-colourable."""
    parts = [[2 * part, 2 * part + 1] for part in range(4)]
    owner = {v: part for part, vertices in enumerate(parts) for v in vertices}
    graph = dict(vertices=list(range(8)),
                 edges=[[u, v] for u, v in combinations(range(8), 2) if owner[u] != owner[v]], fixed=[])
    colours = [owner[v] for v in graph["vertices"]]
    check_colouring(graph, colours)
    adjacent = adjacency(graph)
    records = []
    triangles = set()
    for x, y in graph["edges"]:
        common = sorted(adjacent[x] & adjacent[y])
        assert len(common) == 4
        cycles = [[x, z, y] for z in common]
        assert all(y in adjacent[z] and z in adjacent[x] for z in common)
        triangles.update(canonical_cycle(c) for c in cycles)
        records.append(dict(edge=[x, y], four_triangles=cycles))
    assert len(graph["edges"]) == 24 and len(triangles) == 32
    return dict(name="K_2_2_2_2", graph=graph, graph_sha256=digest(graph), parts=parts,
                explicit_original_graph_four_colour_witness=colours,
                graph_stats=graph_stats(graph), edge_triangle_witnesses=records,
                unique_triangles=[list(c) for c in sorted(triangles)],
                assertions=dict(every_edge_on_four_distinct_triangles=True,
                                original_graph_four_colour_witness_checked=True,
                                three_odd_cycles_per_edge_do_not_imply_unsat=True,
                                exhaustive_edge_deletion_oracles_run=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=AUDIT / "report.json")
    parser.add_argument("--timing-out", type=Path,
                        help="Optional timing output; omitted means no timing file is written.")
    args = parser.parse_args()
    cases = []
    timings = []
    for name, graph, role in make_cases():
        started = time.perf_counter()
        record = audit_case(name, graph, role)
        timings.append(dict(name=name, seconds=time.perf_counter() - started))
        cases.append(record)
        print(json.dumps(dict(name=name, **{key: value for key, value in record["summary"].items()
                                           if key != "canonical_unique_saved_odd_cycles"}),
                         sort_keys=True), flush=True)
    started = time.perf_counter()
    negative = theta_control()
    timings.append(dict(name=negative["name"], seconds=time.perf_counter() - started))
    started = time.perf_counter()
    structural_negative = multipartite_control()
    timings.append(dict(name=structural_negative["name"], seconds=time.perf_counter() - started))
    report = dict(baseline_commit_for_workspace_provenance=BASE,
                  driver_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  production_solver_imports=False, cases=cases, existential_negative_control=negative,
                  structural_negative_control=structural_negative,
                  assertions=dict(all_named_unsat_cases_decided_by_exhaustive_original_edge_DFS=True,
                                  all_saved_sat_witnesses_independently_checked_on_original_edges=True,
                                  all_successful_edge_deletions_violate_exactly_one_original_edge=True,
                                  same_remaining_singleton_checked_for_every_successful_edge_deletion=True,
                                  every_saved_necessary_kempe_path_uses_the_same_deleted_edge_coloring=True,
                                  vertex_minimal_does_not_imply_edge_minimal_control_passed=True,
                                  fixed_domain_kempe_swap_counterexample_passed=True,
                                  one_blocked_exterior_row_does_not_imply_unsat_control_passed=True,
                                  three_odd_cycles_per_edge_not_sufficient_control_passed=True),
                  scope="Six named finite graphs. Critical deletion witnesses establish minimality only together with the separate whole-graph UNSAT oracle. Three-path necessity applies to bare four-colour domains and every deleted-edge coloring; saved witnesses demonstrate it for one coloring per critical edge. Paths and odd-cycle occurrences are counted separately from distinct cycles: different edge witnesses can reuse one cycle and different deleted edges may use different colorings. No exhaustive solution/fibre listing, general reducibility, planar 4CT, or new 932 exclusion claim.")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(report, sort_keys=True, indent=2) + "\n"
    args.out.write_text(encoded)
    if args.timing_out is not None:
        args.timing_out.parent.mkdir(parents=True, exist_ok=True)
        args.timing_out.write_text(json.dumps(dict(report_sha256=sha256(encoded.encode()).hexdigest(),
                                                  cases=timings, metric="One sequential wall-clock run."),
                                             sort_keys=True, indent=2) + "\n")
    print(json.dumps(dict(report_sha256=sha256(encoded.encode()).hexdigest(), cases=len(cases) + 2,
                          output=str(args.out)), sort_keys=True))


if __name__ == "__main__":
    main()
