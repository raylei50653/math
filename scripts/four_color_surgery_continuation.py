#!/usr/bin/env python3
"""Exact same-disk counterexample to iterating full component partitions.

Uses three existing survivor coloring tables, not a new graph search.  Standard
library only.  The selected T4 witnesses have the same three partitions of ALL
named dual vertices, and the first swap uses the very same named edge path.
The full partitions then diverge; a second common rooted rule separates even
the boundary.  No exclusion of support 932 or planar-source theorem is claimed.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
import json
from pathlib import Path

import c5_dual_path_surgery as surgery

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_cells/edge_states.json"
DEFAULT_OUT = ROOT / "audits/2026-10-29-counts-surgery-continuation/surgery-partitions.json"


def components(vertices, edges):
    """Independent adjacency traversal, including retained isolated vertices."""
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    unseen, answer = set(adj), []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue = [root]
        for u in queue:
            for v in sorted(adj[u] & unseen):
                unseen.remove(v)
                queue.append(v)
        answer.append(tuple(sorted(queue)))
    return tuple(sorted(answer))


def full_partitions(de, labels, f):
    answer = []
    for pair in surgery.PAIRS:
        edges = [ends for ends, label in zip(de, labels) if label in pair]
        vertices = set(range(f + 5))
        actual = components(vertices, edges)
        active = {v for ends in edges for v in ends}
        traced = tuple(sorted([tuple(sorted(set(s["vertices"])))
                               for s in surgery.pair_strands(de, labels, pair)]
                              + [(v,) for v in sorted(vertices - active)]))
        assert actual == traced
        answer.append(actual)
    return tuple(answer)


def boundary(de, labels, f):
    return tuple(surgery.matching(de, labels, pair, f) for pair in surgery.PAIRS)


def apply(de, labels, pair, strand):
    """Check a whole actual component, then swap precisely its named edges."""
    assert strand in surgery.pair_strands(de, labels, pair)
    selected = set(strand["edges"])
    target = tuple(sum(pair) - label if e in selected else label
                   for e, label in enumerate(labels))
    assert all((target[e] in pair) == (labels[e] in pair) for e in range(len(labels)))
    return target


def retained_partitions(de, labels, f, removed):
    # Vertices are retained even when all their incident selected edges vanish.
    return tuple(components(set(range(f + 5)),
                            [ends for e, ends in enumerate(de)
                             if labels[e] in pair and e not in removed])
                 for pair in surgery.PAIRS)


def coarse_cut_counts(de, labels, f, removed):
    """Counts indexed by the complete old named component vertex sets."""
    return tuple(tuple((part, sum(e in removed and labels[e] in pair
                                 and de[e][0] in part for e in range(len(de))))
                       for part in parts)
                 for pair, parts in zip(surgery.PAIRS, full_partitions(de, labels, f)))


def port_summary(cut):
    """The existing sufficient one-step input, omitting witness edge traces."""
    return dict(ordered_vertices=cut["ordered_vertices"],
                ordered_path_edges=cut["ordered_path_edges"],
                port_vertices=cut["port_vertices"], local_links=cut["local_links"],
                cuts=[dict(pair=part["pair"],
                           exterior_pairs=sorted(tuple(sorted(s["ends"]))
                                                 for s in part["exterior_segments"]),
                           untouched_cycle_count=len(part["untouched_cycles"]),
                           old_local_links=part["old_local_links"],
                           new_local_links=part["new_local_links"])
                      for part in cut["cuts"]])


def replay(graph, coloring, first_ends=(2, 3), second_root=10):
    edges = list(map(tuple, graph["edges"]))
    de, f = surgery.dual(edges, graph["faces"]), len(graph["faces"])
    labels = tuple(coloring[u] ^ coloring[v] for u, v in edges)
    assert all(label in (1, 2, 3) for label in labels)
    for v in range(f):
        assert {label for ends, label in zip(de, labels) if v in ends} == {1, 2, 3}
    first = next(s for s in surgery.pair_strands(de, labels, (1, 2))
                 if s["ends"] == [f + e for e in first_ends])
    predicted, cut = surgery.ordered_surgery(de, labels, f, (1, 2), first)
    surgery.check_cut_sides(edges, graph["faces"], first, cut)
    after = apply(de, labels, (1, 2), first)
    for pair, wanted in predicted.items():
        assert surgery.matching(de, after, pair, f) == wanted
    second = next(s for s in surgery.pair_strands(de, after, (1, 3))
                  if second_root in s["vertices"])
    final = apply(de, after, (1, 3), second)
    # Integrability and properness on the original graph are independently
    # checked after each step, with primal vertex 0 fixed to color 0.
    after_coloring = surgery.integrate(graph["n"], edges, after)
    final_coloring = surgery.integrate(graph["n"], edges, final)
    removed = set(first["edges"])
    return dict(source_coloring=coloring, source_edge_labels=labels,
                source_boundary=boundary(de, labels, f),
                source_full_partitions=full_partitions(de, labels, f),
                first_action=dict(pair=(1, 2), strand=first,
                                  selected_edge_labels=[labels[e] for e in first["edges"]]),
                old_component_cut_counts=coarse_cut_counts(de, labels, f, removed),
                retained_full_partitions=retained_partitions(de, labels, f, removed),
                first_port_summary=port_summary(cut), first_cut_edge_traces=cut,
                after_first=dict(coloring=after_coloring, edge_labels=after,
                                 boundary=boundary(de, after, f),
                                 full_partitions=full_partitions(de, after, f)),
                second_action=dict(pair=(1, 3), root=second_root, strand=second),
                after_second=dict(coloring=final_coloring, edge_labels=final,
                                  boundary=boundary(de, final, f),
                                  full_partitions=full_partitions(de, final, f)))


def boundary_rooted_bfs(graph, coloring_ids=(4, 5), max_depth=6):
    """Shortest separating pairing word on ONE fixed source pair, depth <=6.

    A selector is a color pair and a named boundary terminal.  Both actual
    components are recomputed, and the selector must be legal on both sides.
    We stop at the first unequal boundary pairing (ignoring cycle counts).
    """
    edges = list(map(tuple, graph["edges"]))
    de, f = surgery.dual(edges, graph["faces"]), len(graph["faces"])
    start = tuple(tuple(graph["coloring_table"][i][u] ^ graph["coloring_table"][i][v]
                        for u, v in edges) for i in coloring_ids)

    def pairing_state(labels):
        return tuple(surgery.matching(de, labels, pair, f)[0] for pair in surgery.PAIRS)

    def selected(labels, pair, terminal):
        return next((strand for strand in surgery.pair_strands(de, labels, pair)
                     if f + terminal in strand["ends"]), None)

    pending = deque([(start, ())])
    seen = {start}
    expanded = Counter()
    found = None
    while pending:
        current, word = pending.popleft()
        expanded[len(word)] += 1
        if pairing_state(current[0]) != pairing_state(current[1]):
            found = word
            break
        if len(word) == max_depth:
            continue
        for pair in surgery.PAIRS:
            for terminal in range(5):
                strands = [selected(labels, pair, terminal) for labels in current]
                if any(strand is None for strand in strands):
                    continue
                target = tuple(apply(de, labels, pair, strand)
                               for labels, strand in zip(current, strands))
                if target not in seen:
                    seen.add(target)
                    pending.append((target, word + ((pair, terminal),)))
    assert found == (((1, 3), 0), ((2, 3), 0), ((1, 2), 0))
    assert sum(expanded.values()) == 53 and len(seen) == 156
    # Replay the shortest word, then append one common boundary-rooted action
    # that turns the pairing difference into different literal boundary words.
    current = start
    steps = []
    for pair, terminal in found + (((1, 3), 0),):
        strands = [selected(labels, pair, terminal) for labels in current]
        assert all(strand is not None for strand in strands)
        target = tuple(apply(de, labels, pair, strand)
                       for labels, strand in zip(current, strands))
        cuts = []
        for labels, strand, after in zip(current, strands, target):
            predicted, cut = surgery.ordered_surgery(de, labels, f, pair, strand)
            surgery.check_cut_sides(edges, graph["faces"], strand, cut)
            assert surgery.matching(de, after, pair, f) == surgery.matching(de, labels, pair, f)
            for mixed_pair, wanted in predicted.items():
                assert surgery.matching(de, after, mixed_pair, f) == wanted
            cuts.append(cut)
        colorings = [surgery.integrate(graph["n"], edges, labels) for labels in target]
        steps.append(dict(pair=pair, boundary_terminal=terminal,
                          source_boundary=[boundary(de, labels, f) for labels in current],
                          source_boundary_pairings=[pairing_state(labels) for labels in current],
                          actual_strands=strands,
                          exact_surgery_cut_data=cuts,
                          target_edge_labels=target, target_colorings=colorings,
                          target_boundary=[boundary(de, labels, f) for labels in target],
                          target_full_partitions=[full_partitions(de, labels, f)
                                                  for labels in target]))
        current = target
    assert all(steps[i]["actual_strands"][0]["ends"] ==
               steps[i]["actual_strands"][1]["ends"] for i in range(3))
    assert all(steps[i]["target_colorings"][0][:5] ==
               steps[i]["target_colorings"][1][:5] for i in range(3))
    assert all(tuple(p[0] for p in steps[i]["target_boundary"][0]) ==
               tuple(p[0] for p in steps[i]["target_boundary"][1]) for i in range(2))
    assert tuple(p[0] for p in steps[2]["target_boundary"][0]) != \
        tuple(p[0] for p in steps[2]["target_boundary"][1])
    assert steps[2]["target_colorings"][0][:5] == [0, 1, 2, 3, 2]
    assert steps[3]["target_colorings"][0][:5] != steps[3]["target_colorings"][1][:5]
    return dict(scope="Only survivor-891, source coloring table IDs 4 and 5; common legal boundary-rooted selectors.",
                requested_depth_bound=max_depth, expanded_pairs=sum(expanded.values()),
                discovered_pairs=len(seen), expanded_by_depth=dict(sorted(expanded.items())),
                shortest_pairing_separation_depth=len(found),
                literal_boundary_separation_depth=len(steps),
                common_cut_side_checks=2 * len(steps), steps=steps)


def report():
    source = json.loads(SOURCE.read_text())
    tables, totals = [], defaultdict(int)
    for graph in source["graphs"]:
        if "coloring_table" not in graph:
            continue
        edges = list(map(tuple, graph["edges"]))
        faces = list(map(tuple, graph["faces"]))
        surgery.check_faces(graph["n"], edges, faces)
        de, f = surgery.dual(edges, faces), len(faces)
        groups = defaultdict(list)
        for i, coloring in enumerate(graph["coloring_table"]):
            labels = tuple(coloring[u] ^ coloring[v] for u, v in edges)
            assert all(label in (1, 2, 3) for label in labels)
            for v in range(f):
                assert {labels[e] for e, ends in enumerate(de) if v in ends} == {1, 2, 3}
            key = tuple(coloring[:5]), full_partitions(de, labels, f)
            groups[key].append(i)
        duplicates = [ids for ids in groups.values() if len(ids) > 1]
        tables.append(dict(name=graph["name"], vertices=graph["n"],
                           coloring_count=len(graph["coloring_table"]),
                           full_partition_states=len(groups), collision_buckets=duplicates))
        totals["colorings"] += len(graph["coloring_table"])
        totals["full_partition_states"] += len(groups)
        totals["collision_buckets"] += len(duplicates)
    assert len(tables) == 3 and dict(totals) == dict(colorings=491,
                                                        full_partition_states=465,
                                                        collision_buckets=26)
    graph = next(g for g in source["graphs"] if g["name"] == "survivor-891")
    a, b = [replay(graph, graph["coloring_table"][i]) for i in (4, 5)]
    assert a["source_coloring"][:5] == b["source_coloring"][:5] == [0, 1, 0, 2, 3]
    for field in ("source_boundary", "source_full_partitions", "first_action",
                  "old_component_cut_counts", "first_port_summary"):
        assert a[field] == b[field], field
    assert len(a["first_action"]["strand"]["edges"]) == 22
    assert a["retained_full_partitions"] != b["retained_full_partitions"]
    assert a["after_first"]["boundary"] == b["after_first"]["boundary"]
    assert a["after_first"]["full_partitions"] != b["after_first"]["full_partitions"]
    assert a["second_action"]["root"] == b["second_action"]["root"] == 10
    assert a["second_action"]["strand"]["ends"] != b["second_action"]["strand"]["ends"]
    assert a["after_second"]["boundary"] != b["after_second"]["boundary"]
    assert a["after_second"]["coloring"][:5] != b["after_second"]["coloring"][:5]
    boundary_word = boundary_rooted_bfs(graph)
    # The identical retained-port summary correctly predicts the identical
    # first boundary; it has lost where named INTERNAL vertices lie along
    # those strands, which is needed to apply the next common rooted rule.
    files = [Path(__file__), SOURCE, ROOT / "scripts/c5_dual_path_surgery.py",
             ROOT / "scripts/c5_kempe_connectivity.py",
             ROOT / "scripts/c5_adjacent_singleton_counts.py",
             ROOT / "scripts/c5_kempe_screen.py"]
    return dict(scope="Same embedded original disk, literal color frame, all named dual vertices; no 932 exclusion.",
                evidence="Exact Python replay, using existing coloring tables; no new Lean theorem or catalogue search.",
                summary=dict(totals, first_path_edges=22, witnesses=2,
                             first_boundary_equal=True, first_full_partitions_equal=False,
                             second_boundary_equal=False,
                             shortest_boundary_rooted_pairing_word=3,
                             boundary_rooted_literal_separation_word=4),
                corpus_audit=tables,
                graph={k: graph[k] for k in ("name", "n", "edges", "faces")},
                source_coloring_table_ids=[4, 5], witnesses=[a, b],
                boundary_rooted_word=boundary_word,
                conclusion="Three full named-vertex component partitions do not determine their own successor, even with the identical named first edge path and identical one-step port interfaces.",
                sources={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                         for p in files})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = report()
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.check:
        assert args.out.read_text() == payload, "Certificate mismatch; inspect before replacing."
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
