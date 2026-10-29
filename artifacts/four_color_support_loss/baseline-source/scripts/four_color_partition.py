"""Static partitions and current-factor work regions for exact elimination.

Only scheduling changes. Every live factor (including cross-block inferred
factors) still participates in its bucket, in the original literal colour frame.
Scheduling work is outside the solver's relation-check budget; timings include it.
"""

from collections import deque
from math import prod


STATIC_STRATEGIES = ("none", "components", "articulation", "bfs")
DYNAMIC_STRATEGIES = ("adaptive", "information", "message")
STRATEGIES = STATIC_STRATEGIES + DYNAMIC_STRATEGIES


def partition_plan(graph, strategy="none", block_size=12):
    from four_color_lab import normalize_graph

    if type(strategy) is not str or strategy not in STRATEGIES:
        raise ValueError("partition_strategy must be one of " + ", ".join(STRATEGIES))
    if type(block_size) is not int or block_size < 1:
        raise ValueError("partition_block_size must be a positive integer")
    graph = normalize_graph(graph)
    if strategy in DYNAMIC_STRATEGIES:
        return dict(strategy=strategy, block_size=block_size, groups=[], splits=[],
                    decisions=[], regions=[], candidate_evaluations=0,
                    contract="dynamic overlapping work regions from current factors; adaptive/information use a global min-fill/width guard; message uses estimated join work; all factors retained")
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


class InformationScheduler:
    """Rebuild work regions when no globally eligible vertex remains inside.

    Domain products and anchor row counts are scheduling estimates only: they
    never stand in for complete relations and never prune a row or a colour.
    Planning scans factor metadata, not relation rows, and is outside checks.
    """

    def __init__(self, plan, vertices):
        self.plan, self.vertices = plan, vertices
        self.region = set()

    def select(self, primal, priorities, factors, domains):
        active = set(primal)
        best = min(value[:2] for value in priorities.values())
        eligible = {v for v in active if priorities[v][:2] == best}
        incident = {v: [] for v in active}
        for factor in factors:
            for v in factor.scope:
                incident[v].append(factor)
        volumes = {v: prod(len(domains[w]) for w in primal[v] | {v}) for v in active}
        factor_volumes = {id(f): prod(len(domains[w]) for w in f.scope) for f in factors}
        estimates = {v: min((len(f.rows) * (volumes[v] // factor_volumes[id(f)])
                            for f in incident[v]), default=len(domains[v])) for v in active}
        work = {v: estimates[v] * (1 + len(incident[v])) + sum(len(f.rows) for f in incident[v])
                for v in active}
        self.plan["candidate_evaluations"] += len(active)
        # Adaptive/information require the best global (fill, width) tier.
        # Information mode additionally requires the smallest current anchor
        # enumeration bound in that tier, before preferring a region member.
        if self.plan["strategy"] == "information":
            cheapest = min(estimates[v] for v in eligible)
            eligible = {v for v in eligible if estimates[v] == cheapest}
        elif self.plan["strategy"] == "message":
            cheapest = min((work[v], priorities[v][:2]) for v in active)
            eligible = {v for v in active if (work[v], priorities[v][:2]) == cheapest}
        self.region.intersection_update(active)
        replanned = not (self.region & eligible)
        if replanned:
            seed = min(eligible, key=lambda v: (estimates[v], v))
            region = {seed}
            boundary = primal[seed] - region
            while boundary and len(region) < self.plan["block_size"]:
                def growth_key(v):
                    outside = (boundary | primal[v]) - region - {v}
                    return (prod(len(domains[w]) for w in outside), len(outside),
                            -len(primal[v] & region), estimates[v], v)
                added = min(boundary, key=growth_key)
                region.add(added)
                boundary = (boundary | primal[added]) - region
            self.region = region
            self.plan["regions"].append(dict(
                members=[self.vertices[v] for v in sorted(region)],
                boundary=[self.vertices[v] for v in sorted(boundary)],
                boundary_domain_product=prod(len(domains[v]) for v in boundary)))
            # groups records the actual selected work, not an a priori cover.
            self.plan["groups"].append([])
        chosen = min(eligible & self.region, key=lambda v: (estimates[v], v))
        self.plan["groups"][-1].append(self.vertices[chosen])
        self.plan["decisions"].append(dict(
            vertex=self.vertices[chosen], min_fill=priorities[chosen][0],
            frontier_size=priorities[chosen][1],
            global_min_fill=best[0], global_min_frontier=best[1], work_estimate=work[chosen],
            anchor_bound=estimates[chosen], replanned=replanned,
            baseline_vertex=self.vertices[min(active, key=priorities.__getitem__)]))
        return chosen
