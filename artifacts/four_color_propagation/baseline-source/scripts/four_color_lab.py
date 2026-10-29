#!/usr/bin/env python3
"""Four operational rules, exact search, and replayable conflict explanations.

The solver uses only the standard library. It accepts any finite simple graph;
it neither assumes nor proves the four-color theorem. Search may be exponential.
"""
from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path
import sys

from four_color_serialization import browser_payload, int_text, json_dumps, json_loads


RULES = [
    {"id": "R1", "name": "刪除鄰色", "description": "未染點的候選色，排除所有已染鄰點的顏色。"},
    {"id": "R2", "name": "唯一色強迫", "description": "只剩一種候選色時，直接填入；可關閉作對照。"},
    {"id": "R3", "name": "選點試色", "description": "依指定次序選點，依序嘗試候選色；這一步是猜測。"},
    {"id": "R4", "name": "衝突回退", "description": "候選色為空就退回最近的未試完選擇，完整還原再試。"},
]


def normalize_graph(graph):
    """Validate integer identities and preserve supplied vertex order."""
    if not isinstance(graph, dict):
        raise ValueError("graph must be an object")
    vertices, edges = graph.get("vertices"), graph.get("edges")
    if not isinstance(vertices, list) or any(type(v) is not int for v in vertices):
        raise ValueError("vertices must be a list of exact integers")
    if len(set(vertices)) != len(vertices):
        raise ValueError("duplicate vertex")
    if not isinstance(edges, list):
        raise ValueError("edges must be a list")
    ids = set(vertices)
    clean_edges = set()
    for edge in edges:
        if (not isinstance(edge, (list, tuple)) or len(edge) != 2
                or any(type(v) is not int or v not in ids for v in edge)):
            raise ValueError("each edge needs two declared integer vertices")
        u, v = edge
        if u == v:
            raise ValueError("self-loops are not simple graph edges")
        key = tuple(sorted((u, v)))
        if key in clean_edges:
            raise ValueError("duplicate undirected edge")
        clean_edges.add(key)
    fixed = graph.get("fixed", [])
    if not isinstance(fixed, list):
        raise ValueError("fixed must be a list of [vertex, color] pairs")
    seen = set()
    for pair in fixed:
        if (not isinstance(pair, (list, tuple)) or len(pair) != 2
                or type(pair[0]) is not int or pair[0] not in ids
                or type(pair[1]) is not int or pair[1] not in range(4)):
            raise ValueError("fixed colors need declared integer vertices and colors 0..3")
        if pair[0] in seen:
            raise ValueError("duplicate fixed vertex")
        seen.add(pair[0])
    result = dict(graph, vertices=list(vertices), edges=[list(e) for e in sorted(clean_edges)],
                  fixed=[list(p) for p in fixed])
    positions = result.get("positions")
    if positions is None:
        n = len(vertices)
        positions = [[.5 + .43 * math.cos(2 * math.pi * i / n),
                      .5 + .43 * math.sin(2 * math.pi * i / n)] for i in range(n)]
    if (not isinstance(positions, list) or len(positions) != len(vertices)
            or any(not isinstance(p, (list, tuple)) or len(p) != 2
                   or any(type(x) not in (int, float) or not math.isfinite(x) for x in p)
                   for p in positions)):
        raise ValueError("positions must be finite [x,y] pairs aligned with vertices")
    result["positions"] = positions
    return result


def verify_coloring(graph, colors):
    """Check a full witness directly against original edges and fixed colors."""
    g = normalize_graph(graph)
    if (not isinstance(colors, list) or len(colors) != len(g["vertices"])
            or any(type(c) is not int or c not in range(4) for c in colors)):
        return False
    assignment = dict(zip(g["vertices"], colors))
    return (all(assignment[u] != assignment[v] for u, v in g["edges"])
            and all(assignment[v] == c for v, c in g["fixed"]))


def graph_fingerprint(graph):
    """Hash ordered vertices, original edges, and literal fixed colors."""
    g = normalize_graph(graph)
    source = {k: g[k] for k in ("vertices", "edges", "fixed")}
    return hashlib.sha256(json_dumps(source, separators=(",", ":")).encode()).hexdigest()


def solve(graph, strategy="dsatur", propagation=True, backtracking=True,
          max_steps=100000, trace_limit=5000):
    """Iterative depth-first search; max_steps caps assignments, not trace length.

    `unsatisfiable` means exhaustive under the supplied fixed colors. `stuck`
    means a branch failed with backtracking disabled; `limit` is inconclusive.
    Each stored event contains a full state. R1 counts removed candidates,
    R2/R3 count assignments, R4 counts failed alternatives undone.
    """
    g = normalize_graph(graph)
    if strategy not in ("natural", "dsatur"):
        raise ValueError("strategy must be natural or dsatur")
    if type(propagation) is not bool or type(backtracking) is not bool:
        raise ValueError("propagation and backtracking must be booleans")
    if any(type(x) is not int or x < 0 for x in (max_steps, trace_limit)):
        raise ValueError("limits must be nonnegative integers")
    vertices = g["vertices"]
    index = {v: i for i, v in enumerate(vertices)}
    neighbors = [[] for _ in vertices]
    for u, v in g["edges"]:
        neighbors[index[u]].append(index[v])
        neighbors[index[v]].append(index[u])
    for ns in neighbors:
        ns.sort()
    colors = [-1] * len(vertices)
    reasons = [[] for _ in vertices]
    for v, c in g["fixed"]:
        colors[index[v]] = c
    stats = dict(assignments=0, decisions=0, forced=0, prunes=0, conflicts=0,
                 backtracks=0, max_depth=0, steps=0)
    counts = dict.fromkeys((r["id"] for r in RULES), 0)
    events = []
    conflict_subgraphs = []
    emitted = 0
    stack = []

    def domains():
        return [[c] if c >= 0 else [a for a in range(4)
                if all(colors[j] != a for j in neighbors[i])]
                for i, c in enumerate(colors)]

    def emit(kind, rule=None, vertex=None, color=None, detail="", **extra):
        nonlocal emitted
        emitted += 1
        if len(events) < trace_limit:
            events.append(dict(kind=kind, rule=rule, colors=colors[:], domains=domains(),
                               depth=len(stack), vertex=vertex, color=color, detail=detail,
                               blockers=[], causal_vertices=[], causal_edges=[],
                               conflict_edges=[], stats=stats.copy(), rule_counts=counts.copy(),
                               **extra))

    # Extra conflict fields replace the empty defaults after emission.
    def conflict(i):
        stats["conflicts"] += 1
        by_color = {}
        for j in neighbors[i]:
            if colors[j] >= 0:
                by_color.setdefault(colors[j], j)
        blockers = [dict(vertex=vertices[by_color[c]], color=c) for c in sorted(by_color)]
        causal_edges = set()
        visited = {i}
        pending = [i]
        local_reasons = {i: list(by_color.values())}
        while pending:
            child = pending.pop()
            for parent in local_reasons.get(child, reasons[child]):
                causal_edges.add(tuple(sorted((vertices[child], vertices[parent]))))
                if parent not in visited:
                    visited.add(parent)
                    pending.append(parent)
        emit("conflict", vertex=vertices[i],
             detail=f"點 {int_text(vertices[i])} 沒有候選色：鄰點已分別佔用色 1、2、3、4。這是目前分支的死路。")
        if events and len(events) == emitted:
            from four_color_conflicts import find_known_conflict
            witness = find_known_conflict(
                [vertices[i], *[b["vertex"] for b in blockers]],
                [[vertices[i], b["vertex"]] for b in blockers],
                [domains()[i], *[[b["color"]] for b in blockers]],
                fixed=g["fixed"], scope="current-branch")
            if witness is not None:
                witness.update(causal_vertices=[vertices[j] for j in sorted(visited)],
                               causal_edges=[list(e) for e in sorted(causal_edges)])
                conflict_subgraphs.append(witness)
            events[-1].update(blockers=blockers, conflict_shape="four_color_star",
                              conflict_subgraph=witness, conflict_template_id="four_color_star",
                              conflict_edges=[[vertices[i], b["vertex"]] for b in blockers],
                              causal_vertices=[vertices[j] for j in sorted(visited)],
                              causal_edges=[list(e) for e in sorted(causal_edges)])

    def assign(i, c, forced=False):
        before = domains()
        parents = {}
        # Record the reason for excluded colors even at a guessed assignment.
        # These edges explain its domain, not why that guess had to be chosen.
        for j in neighbors[i]:
            if colors[j] >= 0:
                parents.setdefault(colors[j], j)
        colors[i] = c
        reasons[i] = list(parents.values())
        stats["assignments"] += 1
        stats["steps"] += 1
        field, rule, kind = ("forced", "R2", "forced") if forced else ("decisions", "R3", "choose")
        stats[field] += 1
        counts[rule] += 1
        stats["max_depth"] = max(stats["max_depth"], len(stack))
        emit(kind, rule, vertices[i], c,
             f"點 {int_text(vertices[i])} {'只剩唯一色，填入' if forced else '試用'}色 {c + 1}。")
        after = domains()
        removed = sum(len(before[j]) - len(after[j]) for j in range(len(vertices)) if colors[j] < 0)
        if removed:
            stats["prunes"] += removed
            counts["R1"] += removed
            emit("prune", "R1", vertices[i], c,
                 f"點 {int_text(vertices[i])} 的色 {c + 1}，合計刪去未染鄰點的 {removed} 個候選色。")

    emit("start", detail="從指定固定色開始。顏色數字為 1–4；未染點顯示候選色。")
    initial_removed = sum(4 - len(d) for i, d in enumerate(domains()) if colors[i] < 0)
    if initial_removed:
        stats["prunes"] += initial_removed
        counts["R1"] += initial_removed
        emit("prune", "R1", detail=f"固定色合計刪去 {initial_removed} 個候選色。")
    bad_edge = next(((u, v) for u, v in g["edges"]
                     if colors[index[u]] >= 0 and colors[index[u]] == colors[index[v]]), None)
    if bad_edge:
        stats["conflicts"] += 1
        emit("conflict", detail=f"固定色在原邊 {int_text(bad_edge[0])}–{int_text(bad_edge[1])} 兩端相同，不能延伸。")
        if events and len(events) == emitted:
            from four_color_conflicts import find_known_conflict
            witness = find_known_conflict(list(bad_edge), [list(bad_edge)],
                [[colors[index[v]]] for v in bad_edge], fixed=g["fixed"], scope="current-branch")
            conflict_subgraphs.append(witness)
            events[-1].update(conflict_shape="fixed_edge", conflict_edges=[list(bad_edge)],
                              conflict_subgraph=witness, conflict_template_id="fixed_edge",
                              causal_vertices=list(bad_edge), causal_edges=[list(bad_edge)])
        status = "unsatisfiable"
    else:
        status = None
    while status is None:
        available = domains()
        empty = next((i for i, c in enumerate(colors) if c < 0 and not available[i]), None)
        if empty is not None:
            conflict(empty)
            if not backtracking:
                status = "stuck"
                break
            # A frame owns the complete state before its trial, including all
            # forced consequences. Restoring it never carries over old reasons.
            while stack:
                frame = stack[-1]
                colors = frame["colors"][:]
                reasons = [p[:] for p in frame["reasons"]]
                stats["backtracks"] += 1
                counts["R4"] += 1
                emit("backtrack", "R4", vertices[frame["vertex"]],
                     detail=f"還原到點 {int_text(vertices[frame['vertex']])} 試色前，撤銷該次試色與全部後果。")
                if frame["remaining"]:
                    if stats["steps"] >= max_steps:
                        status = "limit"
                        break
                    assign(frame["vertex"], frame["remaining"].pop(0))
                    break
                stack.pop()
            else:
                status = "unsatisfiable"
            continue
        if all(c >= 0 for c in colors):
            status = "colored"
            if not verify_coloring(g, colors):
                raise AssertionError("invalid solver witness")
            emit("solution", detail="全部原邊兩端異色，且符合全部固定色；已直接核對。")
            break
        if stats["steps"] >= max_steps:
            status = "limit"
            break
        forced = next((i for i, c in enumerate(colors) if c < 0 and len(available[i]) == 1), None)
        if propagation and forced is not None:
            assign(forced, available[forced][0], forced=True)
            continue
        uncolored = [i for i, c in enumerate(colors) if c < 0]
        i = (uncolored[0] if strategy == "natural" else max(uncolored, key=lambda j:
             (len({colors[k] for k in neighbors[j] if colors[k] >= 0}), len(neighbors[j]), -j)))
        choices = available[i]
        stack.append(dict(vertex=i, remaining=choices[1:], colors=colors[:],
                          reasons=[p[:] for p in reasons]))
        assign(i, choices[0])
    if status == "limit":
        emit("limit", detail=f"達到 {max_steps} 次填色上限；是否存在延伸尚未判定。")
    elif status != "colored":
        emit("end", detail=("所有允許的分支皆已窮盡；這份固定色條件無法延伸。" if g["fixed"] else
                            "所有分支皆已窮盡；此圖無四色染色。") if status == "unsatisfiable" else
             "目前分支卡住；回退已關閉，尚未判定其他分支。")
    from four_color_conflicts import conflict_catalogue
    return dict(name=g.get("name", "自訂圖"), description=g.get("description", ""), graph=g,
                strategy=strategy, propagation=propagation, backtracking=backtracking,
                status=status, colors=colors, events=events, stats=stats,
                rule_counts=counts, trace_truncated=emitted > len(events),
                event_count=emitted, max_steps=max_steps, graph_sha256=graph_fingerprint(g),
                conflict_catalogue=conflict_catalogue(include_rows=False),
                conflict_subgraphs=conflict_subgraphs)


def write_html(path, payload):
    template = Path(__file__).resolve().parents[1] / "tools/four_color_lab_viewer.html"
    encoded = json_dumps(browser_payload(payload), ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(template.read_text().replace("__FOUR_COLOR_DATA__", encoded), encoding="utf-8")


def viewer_run(result):
    """Keep complete relation certificates in JSON, previews in the player."""
    return {k: v for k, v in result.items() if k != "elimination_records"}


def experiment(count, size, seed, max_steps):
    from four_color_examples import random_triangulation
    # This independent library check is for the sampled input class only.
    import networkx as nx
    totals = {}
    for strategy in ("natural", "dsatur"):
        for propagation in (False, True):
            totals[f"{strategy}/{'force' if propagation else 'no-force'}"] = dict(
                graphs=0, colored=0, limit=0, graphs_with_conflicts=0,
                conflicts=0, backtracks=0, assignments=0, max_backtracks=0)
    graph_records = []
    for offset in range(count):
        g = random_triangulation(size, seed + offset)
        graph = nx.Graph()
        graph.add_nodes_from(g["vertices"])
        graph.add_edges_from(g["edges"])
        if not nx.check_planarity(graph)[0]:
            raise AssertionError("sample is not planar")
        row = dict(seed=seed + offset, graph_sha256=graph_fingerprint(g),
                   edges=len(g["edges"]), generator=g["generator"], results={})
        for strategy in ("natural", "dsatur"):
            for propagation in (False, True):
                key = f"{strategy}/{'force' if propagation else 'no-force'}"
                r = solve(g, strategy, propagation, max_steps=max_steps, trace_limit=0)
                if r["status"] not in ("colored", "limit"):
                    raise AssertionError("unexpected result on a generated planar graph")
                t = totals[key]
                t["graphs"] += 1
                t[r["status"]] += 1
                t["graphs_with_conflicts"] += bool(r["stats"]["conflicts"])
                for name in ("conflicts", "backtracks", "assignments"):
                    t[name] += r["stats"][name]
                t["max_backtracks"] = max(t["max_backtracks"], r["stats"]["backtracks"])
                row["results"][key] = dict(status=r["status"], **r["stats"])
        graph_records.append(row)
    return dict(count=count, vertices=size, seed=seed, max_steps=max_steps,
                sampling="face insertion and geometric legal flips; nonuniform",
                networkx=nx.__version__, python=sys.version.split()[0], totals=totals, records=graph_records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="write offline replay viewer with built-in examples")
    demo.add_argument("--out", type=Path, default=Path("artifacts/four_color_lab"))
    run = sub.add_parser("solve", help="solve a JSON graph and optionally render its trace")
    run.add_argument("input", type=Path)
    run.add_argument("--engine", choices=("search", "constraints"), default="search")
    run.add_argument("--edges-only", action="store_true", help="constraints engine: disable triangle/K4 templates")
    run.add_argument("--no-conflicts", action="store_true", help="constraints engine: disable known structural conflict guards")
    run.add_argument("--intersections", action="store_true",
                     help="constraints engine: propagate whole shared tuples between relation tables")
    run.add_argument("--cycles", action="store_true",
                     help="constraints engine: close bounded original cycles and feed supports back into propagation")
    run.add_argument("--cycle-max-cycles", type=int, default=128)
    run.add_argument("--cycle-max-scan-steps", type=int, default=200000)
    run.add_argument("--cycle-contexts", action="store_true",
                     help="constraints engine: preserve a common cycle context and export pair relations; requires --intersections --cycles")
    run.add_argument("--cycle-context-max-contexts", type=int, default=128)
    run.add_argument("--cycle-context-max-scan-steps", type=int, default=200000)
    run.add_argument("--cycle-context-search", choices=("neighbours", "partial"),
                     default="neighbours",
                     help="constraints engine: search neighbour cycles (default) or allow partial actual spokes; requires --cycle-contexts")
    run.add_argument("--joint-constraints", action="store_true",
                     help="constraints engine: automatically match registered original-edge patterns and propagate their joint relations")
    run.add_argument("--joint-consistency", action="store_true",
                     help="constraints engine: filter each variable's incident factors by their complete joint support before elimination")
    run.add_argument("--joint-consistency-max-checks", type=int, default=200000,
                     help="optional joint-support work budget for the whole solve; unfinished queries add no restrictions")
    run.add_argument("--joint-max-matches", type=int, default=128)
    run.add_argument("--joint-max-scan-steps", type=int, default=200000)
    run.add_argument("--c5-method", choices=("structure", "table"), default="structure",
                     help="C5 inference: derive from cycle structure (default), or query the audit table")
    c5_mode = run.add_mutually_exclusive_group()
    c5_mode.add_argument("--c5", action="store_true", help="constraints engine: derive constraints from induced C5s")
    c5_mode.add_argument("--c5-local", action="store_true", help="constraints engine: scan each center once for degree-five neighbor rings")
    run.add_argument("--c5-max-cycles", type=int, default=128)
    run.add_argument("--c5-max-scan-steps", type=int, default=200000)
    run.add_argument("--max-checks", type=int, default=1000000, help="constraints engine work budget")
    run.add_argument("--bucket-method", choices=("anchor", "prefix"), default="anchor",
                     help="constraints engine: enumerate complete anchor extensions (default), or prune prefixes when a complete input factor fails")
    run.add_argument("--partition", choices=("none", "components", "articulation", "bfs", "adaptive", "information", "message"), default="none",
                     help="constraints engine: static separator blocks or dynamic regions guided by current factor information")
    run.add_argument("--partition-block-size", type=int, default=12,
                     help="static splitting threshold, or dynamic work-region size; not a bound on complete interfaces")
    run.add_argument("--max-table-rows", type=int,
                     help="constraints engine generated-table and complete-record row budget; default min(max-checks, 1000000)")
    run.add_argument("--interface-cache", action="store_true",
                     help="constraints engine: retain complete shared-interface indexes in RAM; requires --intersections")
    run.add_argument("--interface-cache-max-rows", type=int, default=1000000,
                     help="maximum retained complete-row references in optional interface indexes")
    run.add_argument("--strategy", choices=("natural", "dsatur"), default="dsatur")
    run.add_argument("--no-propagation", action="store_true")
    run.add_argument("--no-backtracking", action="store_true")
    run.add_argument("--max-steps", type=int, default=100000)
    run.add_argument("--trace-limit", type=int, default=5000)
    run.add_argument("--json", type=Path)
    run.add_argument("--html", type=Path)
    batch = sub.add_parser("experiment", help="compare orders and propagation on the same planar samples")
    batch.add_argument("--count", type=int, default=100)
    batch.add_argument("--vertices", type=int, default=30)
    batch.add_argument("--seed", type=int, default=0)
    batch.add_argument("--max-steps", type=int, default=100000)
    batch.add_argument("--out", type=Path, default=Path("artifacts/four_color_lab/experiment.json"))
    c_demo = sub.add_parser("constraint-demo", help="record possibilities, eliminate, then write back")
    c_demo.add_argument("--out", type=Path, default=Path("artifacts/four_color_constraints"))
    conflict_demo = sub.add_parser("conflict-demo", help="record known conflict subgraphs and structural C5 deductions")
    conflict_demo.add_argument("--out", type=Path, default=Path("artifacts/four_color_conflicts"))
    c_batch = sub.add_parser("constraint-experiment", help="compare edge relations and recorded substructures")
    c_batch.add_argument("--count", type=int, default=100)
    c_batch.add_argument("--vertices", type=int, default=30)
    c_batch.add_argument("--seed", type=int, default=0)
    c_batch.add_argument("--max-checks", type=int, default=1000000)
    c_batch.add_argument("--out", type=Path, default=Path("artifacts/four_color_constraints/experiment.json"))
    c5_demo = sub.add_parser("c5-demo", help="compare indexed C5 propagation and replay its joint relations")
    c5_demo.add_argument("--out", type=Path, default=Path("artifacts/four_color_c5"))
    c5_scan = sub.add_parser("c5-scan", help="find a bounded subset of induced five-cycles in cyclic order")
    c5_scan.add_argument("input", type=Path)
    c5_scan.add_argument("--local", action="store_true", help="only inspect degree-five neighbor rings; does not claim all cycles")
    c5_scan.add_argument("--max-cycles", type=int, default=128)
    c5_scan.add_argument("--max-scan-steps", type=int, default=200000)
    c5_scan.add_argument("--out", type=Path)
    c5_batch = sub.add_parser("c5-experiment", help="measure lookup speed and matched solver runs with/without C5")
    c5_batch.add_argument("--count", type=int, default=100)
    c5_batch.add_argument("--vertices", type=int, default=30)
    c5_batch.add_argument("--seed", type=int, default=0)
    c5_batch.add_argument("--max-checks", type=int, default=1000000)
    c5_batch.add_argument("--out", type=Path, default=Path("artifacts/four_color_c5/experiment.json"))
    args = parser.parse_args()
    try:
        if args.command == "solve":
            if args.engine == "constraints":
                if args.no_propagation or args.no_backtracking or args.strategy != "dsatur":
                    raise ValueError("constraints mode uses relation propagation and min-fill elimination; search flags do not apply")
                from four_color_constraints import solve_constraints
                r = solve_constraints(json_loads(args.input.read_text()), not args.edges_only,
                                      args.max_checks, args.trace_limit, use_c5=args.c5 or args.c5_local,
                                      bucket_method=args.bucket_method,
                                      partition_strategy=args.partition,
                                      partition_block_size=args.partition_block_size,
                                      max_table_rows=args.max_table_rows,
                                      use_interface_cache=args.interface_cache,
                                      interface_cache_max_rows=args.interface_cache_max_rows,
                                      c5_max_cycles=args.c5_max_cycles, c5_max_scan_steps=args.c5_max_scan_steps,
                                      c5_scan_method="local" if args.c5_local else "complete",
                                      use_conflicts=not args.no_conflicts, c5_method=args.c5_method,
                                      use_intersections=args.intersections, use_cycles=args.cycles,
                                      cycle_max_cycles=args.cycle_max_cycles,
                                      cycle_max_scan_steps=args.cycle_max_scan_steps,
                                      use_cycle_contexts=args.cycle_contexts,
                                      cycle_context_max_contexts=args.cycle_context_max_contexts,
                                      cycle_context_max_scan_steps=args.cycle_context_max_scan_steps,
                                      cycle_context_search=args.cycle_context_search,
                                      use_joint_constraints=args.joint_constraints,
                                      use_joint_consistency=args.joint_consistency,
                                      joint_consistency_max_checks=args.joint_consistency_max_checks,
                                      joint_max_matches=args.joint_max_matches,
                                      joint_max_scan_steps=args.joint_max_scan_steps)
            else:
                if args.edges_only or args.c5 or args.c5_local or args.no_conflicts or args.intersections or args.cycles or args.cycle_contexts or args.cycle_context_search != "neighbours" or args.joint_constraints or args.joint_consistency or args.joint_consistency_max_checks != 200000 or args.max_table_rows is not None or args.interface_cache or args.interface_cache_max_rows != 1000000 or args.bucket_method != "anchor" or args.partition != "none" or args.partition_block_size != 12:
                    raise ValueError("constraint feature flags require --engine constraints")
                r = solve(json_loads(args.input.read_text()), args.strategy, not args.no_propagation,
                          not args.no_backtracking, args.max_steps, args.trace_limit)
            if args.json:
                args.json.parent.mkdir(parents=True, exist_ok=True)
                args.json.write_text(json_dumps(r, ensure_ascii=False, indent=2) + "\n")
            if args.html:
                write_html(args.html, dict(rules=r.get("rules", RULES), runs=[viewer_run(r)]))
            print(json_dumps({k: r[k] for k in ("status", "colors", "stats", "rule_counts", "trace_truncated")},
                             ensure_ascii=False, indent=2))
        elif args.command == "demo":
            from four_color_examples import examples
            graphs = examples()
            runs = []
            for g in graphs:
                for strategy, force, backtrack in (("natural", False, False), ("natural", False, True),
                                                   ("natural", True, True), ("dsatur", True, True)):
                    r = solve(g, strategy, force, backtrack)
                    runs.append(r)
            args.out.mkdir(parents=True, exist_ok=True)
            for i, g in enumerate(graphs):
                (args.out / f"example-{i}.json").write_text(json_dumps(g, ensure_ascii=False, indent=2) + "\n")
            write_html(args.out / "index.html", dict(rules=RULES, runs=runs))
            summary = [{k: r[k] for k in ("name", "strategy", "propagation", "backtracking", "status", "stats", "rule_counts")}
                       for r in runs]
            (args.out / "summary.json").write_text(json_dumps(summary, ensure_ascii=False, indent=2) + "\n")
            print(f"{len(graphs)} graphs / {len(runs)} runs: {args.out / 'index.html'}")
        elif args.command == "constraint-demo":
            from four_color_constraints import CONSTRAINT_RULES, solve_constraints, substructure_catalogue
            from four_color_examples import constraint_examples
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / "library.json").write_text(json_dumps(substructure_catalogue(), ensure_ascii=False, indent=2) + "\n")
            runs, summary = [], []
            for i, g in enumerate(constraint_examples()):
                (args.out / f"example-{i}.json").write_text(json_dumps(g, ensure_ascii=False, indent=2) + "\n")
                for motifs in (False, True):
                    r = solve_constraints(g, use_substructures=motifs, use_conflicts=False)
                    tag = f"run-{i}-{'substructures' if motifs else 'edges'}"
                    (args.out / f"{tag}.json").write_text(json_dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
                    runs.append(viewer_run(r))
                    summary.append({k: r[k] for k in ("name", "engine", "use_substructures", "status",
                                                        "stats", "substructures", "graph_sha256")})
            write_html(args.out / "index.html", dict(rules=CONSTRAINT_RULES, runs=runs))
            (args.out / "summary.json").write_text(json_dumps(summary, ensure_ascii=False, indent=2) + "\n")
            print(f"{len(runs)} constraint runs: {args.out / 'index.html'}")
        elif args.command == "conflict-demo":
            from four_color_conflicts import conflict_catalogue
            from four_color_constraints import CONSTRAINT_RULES, solve_constraints
            from four_color_examples import examples, constraint_examples, c5_examples
            selected = {g["name"]: g for g in examples() + constraint_examples() + c5_examples()}
            names = ("star_free", "star_fixed_four_colours", "triangle_joint_free",
                     "triangle_joint_conflict", "c5_bipyramid_free", "c5_two_color_conflict",
                     "c5_forced_exit", "k5_nonplanar_control")
            fixed_edge = dict(name="fixed_edge_conflict", vertices=[30, -7], edges=[[30, -7]],
                              fixed=[[30, 2], [-7, 2]])
            graphs = [fixed_edge] + [selected[name] for name in names]
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / "library.json").write_text(json_dumps(conflict_catalogue(), ensure_ascii=False, indent=2) + "\n")
            runs, summary = [], []
            for i, graph in enumerate(graphs):
                (args.out / f"example-{i}.json").write_text(json_dumps(graph, ensure_ascii=False, indent=2) + "\n")
                modes = [("guards", dict(use_conflicts=True)),
                         ("baseline", dict(use_conflicts=False))]
                if graph["name"].startswith("c5_"):
                    modes += [(method, dict(use_conflicts=False, use_c5=True, c5_method=method))
                              for method in ("structure", "table")]
                statuses = set()
                for mode, options in modes:
                    result = solve_constraints(graph, **options)
                    statuses.add(result["status"])
                    if result["status"] == "colored" and not verify_coloring(graph, result["colors"]):
                        raise AssertionError("conflict demo lost original-edge witness")
                    result["comparison_mode"] = mode
                    (args.out / f"run-{i}-{mode}.json").write_text(
                        json_dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n")
                    runs.append(viewer_run(result))
                    summary.append({key: result[key] for key in (
                        "name", "status", "comparison_mode", "stats", "graph_sha256",
                        "use_conflicts", "use_c5", "c5_method", "conflict_subgraphs")})
                if len(statuses) != 1 or "limit" in statuses:
                    raise AssertionError("conflict demo modes disagree or exceeded budget")
            branch = solve(selected["binomial_tree_t5"], strategy="natural",
                           propagation=False, backtracking=True)
            branch["comparison_mode"] = "branch"
            runs.append(branch)
            (args.out / "run-branch.json").write_text(json_dumps(branch, ensure_ascii=False, separators=(",", ":")) + "\n")
            write_html(args.out / "index.html", dict(rules=CONSTRAINT_RULES, runs=runs))
            (args.out / "summary.json").write_text(json_dumps(summary, ensure_ascii=False, indent=2) + "\n")
            print(f"{len(graphs)} graphs / {len(runs)} runs: {args.out / 'index.html'}")
        elif args.command == "c5-scan":
            from four_color_c5 import find_induced_c5, find_local_c5
            g = normalize_graph(json_loads(args.input.read_text()))
            finder = find_local_c5 if args.local else find_induced_c5
            result = finder(g, args.max_cycles, args.max_scan_steps)
            result.update(graph_sha256=graph_fingerprint(g), count=len(result["cycles"]),
                          ordering="cyclic order; first vertex and orientation canonical by input vertex order")
            encoded = json_dumps(result, ensure_ascii=False, indent=2) + "\n"
            if args.out:
                args.out.parent.mkdir(parents=True, exist_ok=True)
                args.out.write_text(encoded)
            print(encoded, end="")
        elif args.command == "c5-demo":
            from four_color_c5 import c5_catalogue
            from four_color_constraints import CONSTRAINT_RULES, solve_constraints
            from four_color_examples import c5_examples
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / "library.json").write_text(json_dumps(c5_catalogue(), ensure_ascii=False, indent=2) + "\n")
            runs, summary = [], []
            for i, g in enumerate(c5_examples()):
                (args.out / f"example-{i}.json").write_text(json_dumps(g, ensure_ascii=False, indent=2) + "\n")
                for mode in ("base", "c5", "local"):
                    r = solve_constraints(g, use_c5=mode != "base",
                                          c5_scan_method="local" if mode == "local" else "complete",
                                          use_conflicts=False, c5_method="table")
                    tag = f"run-{i}-{mode}"
                    (args.out / f"{tag}.json").write_text(json_dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
                    runs.append(viewer_run(r))
                    summary.append({k: r[k] for k in ("name", "engine", "use_substructures", "use_c5", "c5_scan_method", "status",
                                                       "stats", "substructures", "graph_sha256")})
            write_html(args.out / "index.html", dict(rules=CONSTRAINT_RULES, runs=runs))
            (args.out / "summary.json").write_text(json_dumps(summary, ensure_ascii=False, indent=2) + "\n")
            print(f"{len(runs)} C5 comparison runs: {args.out / 'index.html'}")
        elif args.command in ("constraint-experiment", "c5-experiment"):
            if args.count < 1 or args.vertices < 4 or args.max_checks < 0:
                raise ValueError("count >= 1, vertices >= 4, max-checks >= 0 required")
            if args.command == "c5-experiment":
                from four_color_c5_experiment import experiment as compare_constraints
            else:
                from four_color_constraint_experiment import experiment as compare_constraints
            result = compare_constraints(args.count, args.vertices, args.seed, args.max_checks)
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json_dumps(result, ensure_ascii=False, indent=2) + "\n")
            print(json_dumps(result["totals"], ensure_ascii=False, indent=2))
            if "lookup" in result:
                print(json_dumps(result["lookup"], ensure_ascii=False, indent=2))
        else:
            if args.count < 1 or args.vertices < 4 or args.max_steps < 0:
                raise ValueError("count >= 1, vertices >= 4, max-steps >= 0 required")
            result = experiment(args.count, args.vertices, args.seed, args.max_steps)
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json_dumps(result, ensure_ascii=False, indent=2) + "\n")
            print(json_dumps(result["totals"], ensure_ascii=False, indent=2))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
