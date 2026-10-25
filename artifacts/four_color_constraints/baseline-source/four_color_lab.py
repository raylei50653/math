#!/usr/bin/env python3
"""Four operational rules, exact search, and replayable conflict explanations.

The solver uses only the standard library. It accepts any finite simple graph;
it neither assumes nor proves the four-color theorem. Search may be exponential.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys


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
    return hashlib.sha256(json.dumps(source, separators=(",", ":")).encode()).hexdigest()


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
             detail=f"點 {vertices[i]} 沒有候選色：鄰點已分別佔用色 1、2、3、4。這是目前分支的死路。")
        if events and len(events) == emitted:
            events[-1].update(blockers=blockers, conflict_shape="four_color_star",
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
             f"點 {vertices[i]} {'只剩唯一色，填入' if forced else '試用'}色 {c + 1}。")
        after = domains()
        removed = sum(len(before[j]) - len(after[j]) for j in range(len(vertices)) if colors[j] < 0)
        if removed:
            stats["prunes"] += removed
            counts["R1"] += removed
            emit("prune", "R1", vertices[i], c,
                 f"點 {vertices[i]} 的色 {c + 1}，合計刪去未染鄰點的 {removed} 個候選色。")

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
        emit("conflict", detail=f"固定色在原邊 {bad_edge[0]}–{bad_edge[1]} 兩端相同，不能延伸。")
        if events and len(events) == emitted:
            events[-1].update(conflict_shape="fixed_edge", conflict_edges=[list(bad_edge)],
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
                     detail=f"還原到點 {vertices[frame['vertex']]} 試色前，撤銷該次試色與全部後果。")
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
    return dict(name=g.get("name", "自訂圖"), description=g.get("description", ""), graph=g,
                strategy=strategy, propagation=propagation, backtracking=backtracking,
                status=status, colors=colors, events=events, stats=stats,
                rule_counts=counts, trace_truncated=emitted > len(events),
                event_count=emitted, max_steps=max_steps, graph_sha256=graph_fingerprint(g))


def write_html(path, payload):
    template = Path(__file__).resolve().parents[1] / "tools/four_color_lab_viewer.html"
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
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
    run.add_argument("--max-checks", type=int, default=1000000, help="constraints engine work budget")
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
    c_batch = sub.add_parser("constraint-experiment", help="compare edge relations and recorded substructures")
    c_batch.add_argument("--count", type=int, default=100)
    c_batch.add_argument("--vertices", type=int, default=30)
    c_batch.add_argument("--seed", type=int, default=0)
    c_batch.add_argument("--max-checks", type=int, default=1000000)
    c_batch.add_argument("--out", type=Path, default=Path("artifacts/four_color_constraints/experiment.json"))
    args = parser.parse_args()
    try:
        if args.command == "solve":
            if args.engine == "constraints":
                if args.no_propagation or args.no_backtracking or args.strategy != "dsatur":
                    raise ValueError("constraints mode uses relation propagation and min-fill elimination; search flags do not apply")
                from four_color_constraints import solve_constraints
                r = solve_constraints(json.loads(args.input.read_text()), not args.edges_only,
                                      args.max_checks, args.trace_limit)
            else:
                if args.edges_only:
                    raise ValueError("--edges-only requires --engine constraints")
                r = solve(json.loads(args.input.read_text()), args.strategy, not args.no_propagation,
                          not args.no_backtracking, args.max_steps, args.trace_limit)
            if args.json:
                args.json.parent.mkdir(parents=True, exist_ok=True)
                args.json.write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n")
            if args.html:
                write_html(args.html, dict(rules=r.get("rules", RULES), runs=[viewer_run(r)]))
            print(json.dumps({k: r[k] for k in ("status", "colors", "stats", "rule_counts", "trace_truncated")},
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
                (args.out / f"example-{i}.json").write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
            write_html(args.out / "index.html", dict(rules=RULES, runs=runs))
            summary = [{k: r[k] for k in ("name", "strategy", "propagation", "backtracking", "status", "stats", "rule_counts")}
                       for r in runs]
            (args.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
            print(f"{len(graphs)} graphs / {len(runs)} runs: {args.out / 'index.html'}")
        elif args.command == "constraint-demo":
            from four_color_constraints import CONSTRAINT_RULES, solve_constraints, substructure_catalogue
            from four_color_examples import constraint_examples
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / "library.json").write_text(json.dumps(substructure_catalogue(), ensure_ascii=False, indent=2) + "\n")
            runs, summary = [], []
            for i, g in enumerate(constraint_examples()):
                (args.out / f"example-{i}.json").write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
                for motifs in (False, True):
                    r = solve_constraints(g, use_substructures=motifs)
                    tag = f"run-{i}-{'substructures' if motifs else 'edges'}"
                    (args.out / f"{tag}.json").write_text(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")
                    runs.append(viewer_run(r))
                    summary.append({k: r[k] for k in ("name", "engine", "use_substructures", "status",
                                                        "stats", "substructures", "graph_sha256")})
            write_html(args.out / "index.html", dict(rules=CONSTRAINT_RULES, runs=runs))
            (args.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
            print(f"{len(runs)} constraint runs: {args.out / 'index.html'}")
        elif args.command == "constraint-experiment":
            if args.count < 1 or args.vertices < 4 or args.max_checks < 0:
                raise ValueError("count >= 1, vertices >= 4, max-checks >= 0 required")
            from four_color_constraint_experiment import experiment as compare_constraints
            result = compare_constraints(args.count, args.vertices, args.seed, args.max_checks)
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps(result["totals"], ensure_ascii=False, indent=2))
        else:
            if args.count < 1 or args.vertices < 4 or args.max_steps < 0:
                raise ValueError("count >= 1, vertices >= 4, max-steps >= 0 required")
            result = experiment(args.count, args.vertices, args.seed, args.max_steps)
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            print(json.dumps(result["totals"], ensure_ascii=False, indent=2))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
