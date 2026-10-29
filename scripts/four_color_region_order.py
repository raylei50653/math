"""Bounded, deterministic region orders for exact tree-separator queries.

The only output consumed by a solver is a permutation of original vertices.
Fill edges below describe dependencies during planning, never additional
colouring constraints.  Geometric cuts are graph separators, not a claim that
every region has a simple polygon boundary.  Coordinates need not be planar.
"""

from collections import deque
from collections.abc import Mapping
from itertools import combinations
from math import isfinite

from four_color_lab import normalize_graph


STRATEGIES = ("min_degree", "geometric_sweep", "geometric_nested",
              "bfs_nested", "bfs_sweep")


class _PlanningLimit(Exception):
    pass


def build_region_order(graph, strategy, positions=None, max_checks=1_000_000,
                       leaf_size=8):
    """Return a complete elimination order, or ``limit`` with ``order=None``.

    ``positions`` is a mapping of original IDs to finite (x, y) pairs, or a
    sequence aligned with graph vertices.  Geometry strategies also accept an
    explicit graph['positions']; a generated display layout is never used.
    Nongeometry strategies ignore positions.  Nested strategies process graph
    interiors before their separators, then use local min-fill in unsplit
    leaves.  Their separator score includes the current inherited filled
    boundary, rather than only counting the newly selected cut vertices.

    ``stats.checks`` charges graph scans, ordering candidates, separator
    evaluation, and fill work.  Validation, allocation, sorting, and Python
    container bookkeeping are not CPU-instruction counted.  Both planning
    time and these checks should be included in end-to-end comparisons.
    Colours and fixed assignments never influence the planned order.
    """
    if type(strategy) is not str or strategy not in STRATEGIES:
        raise ValueError("unknown region strategy")
    if type(max_checks) is not int or max_checks < 0:
        raise ValueError("max_checks must be a nonnegative integer")
    if type(leaf_size) is not int or leaf_size < 1:
        raise ValueError("leaf_size must be a positive integer")
    g = normalize_graph(graph)
    vertices = g["vertices"]
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    coordinates = None
    if strategy.startswith("geometric_"):
        supplied = positions if positions is not None else graph.get("positions")
        if supplied is None:
            raise ValueError("geometric strategies require explicit positions")
        if isinstance(supplied, Mapping):
            if (any(type(v) is not int for v in supplied)
                    or set(supplied) != set(vertices)):
                raise ValueError("positions must cover exactly the original vertices")
            supplied = [supplied[v] for v in vertices]
        if (not isinstance(supplied, (list, tuple)) or len(supplied) != n
                or any(not isinstance(p, (list, tuple)) or len(p) != 2
                       or any(type(x) not in (int, float) or not isfinite(x)
                              for x in p) for p in supplied)):
            raise ValueError("positions must be finite coordinate pairs")
        coordinates = [tuple(p) for p in supplied]

    stats = dict(checks=0, check_kinds={}, vertices_planned=0,
                 peak_filled_boundary=0, filled_boundary_sum=0, fill_edges=0,
                 separator_candidates=0, split_count=0, max_depth=0)
    splits, order = [], []
    sweep_choice = None

    def charge(kind, count=1):
        if count > max_checks - stats["checks"]:
            remaining = max_checks - stats["checks"]
            stats["checks"] += remaining
            stats["check_kinds"][kind] = stats["check_kinds"].get(kind, 0) + remaining
            raise _PlanningLimit()
        stats["checks"] += count
        stats["check_kinds"][kind] = stats["check_kinds"].get(kind, 0) + count

    def result(status):
        return dict(status=status, strategy=strategy,
                    order=[vertices[v] for v in order] if status == "planned" else None,
                    stats=stats, splits=splits, sweep_choice=sweep_choice,
                    leaf_size=leaf_size,
                    limit_reason="max_checks" if status == "limit" else None,
                    contract="original vertex order only; fill edges are planning dependencies")

    try:
        charge("input_vertex", n)
        original = [set() for _ in vertices]
        for u, v in g["edges"]:
            charge("input_edge")
            a, b = index[u], index[v]
            original[a].add(b)
            original[b].add(a)
        filled = [set(ns) for ns in original]
        active = set(range(n))

        def boundary(nodes):
            outside = set()
            for v in nodes:
                charge("boundary_scan", len(filled[v]) + 1)
                outside.update(filled[v] - nodes)
            return outside

        def eliminate(v):
            neighbours = sorted(filled[v])
            charge("eliminate_vertex")
            stats["peak_filled_boundary"] = max(stats["peak_filled_boundary"], len(neighbours))
            stats["filled_boundary_sum"] += len(neighbours)
            for u, w in combinations(neighbours, 2):
                charge("fill_pair")
                if w not in filled[u]:
                    filled[u].add(w)
                    filled[w].add(u)
                    stats["fill_edges"] += 1
            for u in neighbours:
                charge("retire_edge")
                filled[u].remove(v)
            filled[v].clear()
            active.remove(v)
            order.append(v)
            stats["vertices_planned"] += 1

        def leaf(nodes, degree_only=False):
            nodes = set(nodes)
            while nodes:
                best = None
                for v in sorted(nodes):
                    charge("order_candidate")
                    missing = 0
                    if not degree_only:
                        for u, w in combinations(sorted(filled[v]), 2):
                            charge("minfill_pair")
                            missing += w not in filled[u]
                    score = ((len(filled[v]), v) if degree_only else
                             (missing, len(filled[v]), v))
                    if best is None or score < best[0]:
                        best = score, v
                v = best[1]
                eliminate(v)
                nodes.remove(v)

        def components(nodes):
            unseen, parts = set(nodes), []
            for root in sorted(nodes):
                charge("component_root")
                if root not in unseen:
                    continue
                unseen.remove(root)
                todo, part = [root], {root}
                while todo:
                    v = todo.pop()
                    charge("component_scan", len(filled[v]) + 1)
                    following = filled[v] & unseen
                    unseen.difference_update(following)
                    part.update(following)
                    todo.extend(sorted(following))
                parts.append(part)
            return parts

        def bfs(nodes, root, adjacency):
            distance, todo = {root: 0}, deque([root])
            while todo:
                v = todo.popleft()
                charge("bfs_scan", len(adjacency[v]) + 1)
                for w in sorted(adjacency[v] & nodes):
                    if w not in distance:
                        distance[w] = distance[v] + 1
                        todo.append(w)
            return distance

        def frontier_score(candidate):
            # Original-graph vertex separation is a structural order heuristic,
            # not a count of lazy queries or a guaranteed solver cost.
            unseen, frontier = set(range(n)), set()
            peak = total = 0
            for v in candidate:
                charge("sweep_frontier", len(original[v]) + 1)
                unseen.remove(v)
                frontier.discard(v)
                frontier.update(original[v] & unseen)
                peak = max(peak, len(frontier))
                total += len(frontier)
            return peak, total

        if strategy == "min_degree":
            leaf(active, degree_only=True)
        elif strategy.endswith("sweep"):
            candidates = []
            if strategy == "geometric_sweep":
                for axis in range(2):
                    for direction in (1, -1):
                        charge("coordinate_order", n)
                        candidate = sorted(range(n), key=lambda v: (
                            direction * coordinates[v][axis], coordinates[v][1 - axis], v))
                        candidates.append((dict(axis=axis, direction=direction), candidate))
            else:
                # Each connected component has two BFS roots; combine the
                # corresponding contour orders across components.
                parts = components(active)
                variants = [[] for _ in range(4)]
                for part in parts:
                    root = min(part)
                    first = bfs(part, root, original)
                    farthest = min(part, key=lambda v: (-first[v], v))
                    for root_index, distance in enumerate((first, bfs(part, farthest, original))):
                        for direction_index, direction in enumerate((1, -1)):
                            charge("bfs_order", len(part))
                            variants[2 * root_index + direction_index].extend(
                                sorted(part, key=lambda v: (direction * distance[v], v)))
                candidates = [(dict(root_variant=i // 2, direction=(1, -1)[i % 2]), candidate)
                              for i, candidate in enumerate(variants)]
            scored = [(frontier_score(candidate), i, metadata, candidate)
                      for i, (metadata, candidate) in enumerate(candidates)]
            score, _, metadata, candidate = min(scored, key=lambda item: item[:2])
            sweep_choice = dict(metadata, original_frontier_peak=score[0],
                                original_frontier_sum=score[1])
            for v in candidate:
                eliminate(v)
        else:
            def choose_separator(nodes):
                best = None
                seen = set()

                def consider(cut, metadata):
                    nonlocal best
                    frozen = frozenset(cut)
                    if not cut or frozen in seen:
                        return
                    seen.add(frozen)
                    charge("separator_candidate")
                    stats["separator_candidates"] += 1
                    parts = components(nodes - cut)
                    largest = max(map(len, parts), default=0)
                    if len(parts) < 2 or 3 * largest > 2 * len(nodes):
                        return
                    interfaces = [boundary(part) for part in parts]
                    maximum = max(map(len, interfaces), default=0)
                    score = (maximum, sum(map(len, interfaces)), len(cut), largest,
                             tuple(sorted(cut)))
                    if best is None or score < best[0]:
                        best = score, set(cut), parts, metadata, interfaces

                if strategy == "geometric_nested":
                    for axis in range(2):
                        charge("coordinate_levels", len(nodes))
                        levels = sorted({coordinates[v][axis] for v in nodes})
                        gaps = list(range(1, len(levels)))
                        # At most nine deterministic threshold candidates per
                        # axis; this is bounded discovery, not an optimum cut.
                        if len(gaps) > 9:
                            gaps = sorted({1 + (len(gaps) - 1) * i // 8 for i in range(9)})
                        for gap in gaps:
                            threshold = levels[gap]
                            charge("coordinate_partition", len(nodes))
                            low = {v for v in nodes if coordinates[v][axis] < threshold}
                            high = nodes - low
                            low_cut, high_cut = set(), set()
                            for v in low:
                                charge("crossing_edge_scan", len(filled[v]) + 1)
                                crossing = filled[v] & high
                                if crossing:
                                    low_cut.add(v)
                                    high_cut.update(crossing)
                            for side, cut in (("lower", low_cut), ("upper", high_cut)):
                                consider(cut, dict(kind="axis_crossing_endpoints", axis=axis,
                                                   threshold=threshold, side=side))
                else:
                    root = min(nodes)
                    first = bfs(nodes, root, filled)
                    farthest = min(nodes, key=lambda v: (-first[v], v))
                    for source, distance in ((root, first), (farthest, bfs(nodes, farthest, filled))):
                        for level in range(1, max(distance.values(), default=0)):
                            charge("bfs_layer", len(nodes))
                            cut = {v for v in nodes if distance[v] == level}
                            consider(cut, dict(kind="bfs_layer", root=vertices[source], level=level))
                return best

            pending = [(set(active), 0, False, None)] if active else []
            while pending:
                nodes, depth, terminal, parent_split = pending.pop()
                charge("region_visit", len(nodes) + 1)
                stats["max_depth"] = max(stats["max_depth"], depth)
                if terminal or len(nodes) <= leaf_size:
                    leaf(nodes)
                    continue
                parts = components(nodes)
                inherited = boundary(nodes)
                selected = None if len(parts) > 1 else choose_separator(nodes)
                if len(parts) == 1 and selected is None:
                    leaf(nodes)
                    continue
                if selected is None:
                    cut, metadata = set(), dict(kind="components")
                    interfaces = [boundary(part) for part in parts]
                else:
                    _, cut, parts, metadata, interfaces = selected
                split_id = len(splits)
                splits.append(dict(id=split_id, parent=parent_split, depth=depth,
                                   region=[vertices[v] for v in sorted(nodes)],
                                   separator=[vertices[v] for v in sorted(cut)],
                                   interiors=[[vertices[v] for v in sorted(part)] for part in parts],
                                   external_boundary=[vertices[v] for v in sorted(inherited)],
                                   estimated_child_interfaces=[len(interface) for interface in interfaces],
                                   method=metadata))
                stats["split_count"] += 1
                if cut:
                    pending.append((cut, depth, True, split_id))
                # Process small complete interfaces first.  Every subsequent
                # child is planned against the updated filled dependency graph.
                children = sorted(zip(parts, interfaces),
                                  key=lambda item: (len(item[1]), len(item[0]), min(item[0])))
                pending.extend((part, depth + 1, False, split_id)
                               for part, _ in reversed(children))
        if len(order) != n or set(order) != set(range(n)):
            raise AssertionError("planner did not produce a vertex permutation")
        return result("planned")
    except _PlanningLimit:
        return result("limit")
