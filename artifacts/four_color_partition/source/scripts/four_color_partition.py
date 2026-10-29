"""Deterministic original-graph partitions for exact elimination scheduling.

Only scheduling changes. Every live factor (including cross-block inferred
factors) still participates in its bucket, in the original literal colour frame.
Planning is static preprocessing, outside the solver's relation-check budget.
"""

from collections import deque


STRATEGIES = ("none", "components", "articulation", "bfs")


def partition_plan(graph, strategy="none", block_size=12):
    from four_color_lab import normalize_graph

    if type(strategy) is not str or strategy not in STRATEGIES:
        raise ValueError("partition_strategy must be none, components, articulation or bfs")
    if type(block_size) is not int or block_size < 1:
        raise ValueError("partition_block_size must be a positive integer")
    graph = normalize_graph(graph)
    vertices = graph["vertices"]
    position = {v: i for i, v in enumerate(vertices)}
    adjacency = {v: set() for v in vertices}
    for a, b in graph["edges"]:
        adjacency[a].add(b)
        adjacency[b].add(a)

    def ordered(nodes):
        return sorted(nodes, key=position.__getitem__)

    def components(nodes):
        unseen, result = set(nodes), []
        for root in ordered(nodes):
            if root not in unseen:
                continue
            unseen.remove(root)
            component, stack = {root}, [root]
            while stack:
                v = stack.pop()
                following = adjacency[v] & unseen
                unseen.difference_update(following)
                component.update(following)
                stack.extend(following)
            result.append(component)
        return result

    def separator(nodes):
        candidates = []
        if strategy == "articulation":
            # Deliberately simple reference strategy; O(n(n+m)) per region.
            for v in ordered(nodes):
                parts = components(nodes - {v})
                if len(parts) > 1:
                    candidates.append((max(map(len, parts)), position[v], {v}, parts))
            if candidates:
                _, _, cut, parts = min(candidates, key=lambda item: item[:2])
                return cut, parts
        elif strategy == "bfs":
            # Two deterministic roots, all internal BFS layers. A whole layer
            # separates earlier and later layers because edges span <= 1 level.
            root = ordered(nodes)[0]
            roots = [root]
            seen_cuts = set()
            for attempt in range(2):
                distance, queue = {roots[attempt]: 0}, deque([roots[attempt]])
                while queue:
                    v = queue.popleft()
                    for w in ordered(adjacency[v] & nodes):
                        if w not in distance:
                            distance[w] = distance[v] + 1
                            queue.append(w)
                if attempt == 0:
                    roots.append(min(nodes, key=lambda v: (-distance[v], position[v])))
                for level in range(1, max(distance.values(), default=0)):
                    cut = frozenset(v for v in nodes if distance[v] == level)
                    if cut in seen_cuts:
                        continue
                    seen_cuts.add(cut)
                    parts = components(nodes - cut)
                    largest = max(map(len, parts), default=0)
                    if len(parts) > 1 and 3 * largest <= 2 * len(nodes):
                        key = (len(cut), largest, tuple(position[v] for v in ordered(cut)))
                        candidates.append((key, set(cut), parts))
            if candidates:
                _, cut, parts = min(candidates, key=lambda item: item[0])
                return cut, parts
        return set(), []

    groups, splits = [], []
    # Explicit stack avoids Python recursion limits on long graphs.
    pending = [(set(vertices), False)] if vertices else []
    while pending:
        nodes, terminal = pending.pop()
        if terminal or strategy == "none":
            groups.append(ordered(nodes))
            continue
        parts = components(nodes)
        if len(parts) > 1:
            pending.extend((part, False) for part in reversed(parts))
            continue
        cut, parts = (separator(nodes) if len(nodes) > block_size else (set(), []))
        if not cut:
            groups.append(ordered(nodes))
            continue
        splits.append(dict(region=ordered(nodes), separator=ordered(cut),
                           interiors=[ordered(part) for part in parts]))
        pending.append((cut, True))
        pending.extend((part, False) for part in reversed(parts))
    return dict(strategy=strategy, block_size=block_size, groups=groups, splits=splits,
                contract="postorder interior groups before separators; dynamic min-fill within each group; all live factors retained")
