"""The internal typed graph: family grouping, relation edges, and the derived
reverse indexes and dependency closure. Everything here is computed from the
declared metadata; nothing is stored back into documents."""
from __future__ import annotations

from collections import defaultdict

from .model import Edge, Node, relation_type


class Graph:
    def __init__(self, nodes: list[Node]):
        # Duplicate ids are reported by validation; the first occurrence wins.
        self.nodes: dict[str, Node] = {}
        for node in nodes:
            self.nodes.setdefault(node.id, node)
        self.edges: list[Edge] = sorted(
            {Edge(n.id, rel, t) for n in self.nodes.values()
             for rel, targets in n.relations.items() for t in targets},
            key=lambda e: (e.source, e.type, e.target),
        )
        self.outgoing: dict[str, list[Edge]] = defaultdict(list)
        self.incoming: dict[str, list[Edge]] = defaultdict(list)
        for edge in self.edges:
            self.outgoing[edge.source].append(edge)
            self.incoming[edge.target].append(edge)
        self.families: dict[str, list[str]] = defaultdict(list)
        for node in sorted(self.nodes.values(), key=lambda n: n.id):
            for family in node.families:
                self.families[family].append(node.id)
        self.families = dict(sorted(self.families.items()))

    # -- dependency projection -------------------------------------------

    def dependency_edges(self) -> list[Edge]:
        return [e for e in self.edges
                if relation_type(e.type).dag and e.target in self.nodes]

    def prerequisites(self, node_id: str) -> list[str]:
        return sorted({e.target for e in self.outgoing.get(node_id, ())
                       if relation_type(e.type).dag and e.target in self.nodes})

    def dependents(self, node_id: str) -> list[str]:
        return sorted({e.source for e in self.incoming.get(node_id, ())
                       if relation_type(e.type).dag})

    def _closure(self, start: str, step) -> list[str]:
        seen, stack = set(), list(step(start))
        while stack:
            current = stack.pop()
            if current not in seen:
                seen.add(current)
                stack.extend(step(current))
        seen.discard(start)
        return sorted(seen)

    def ancestors(self, node_id: str) -> list[str]:
        return self._closure(node_id, self.prerequisites)

    def descendants(self, node_id: str) -> list[str]:
        return self._closure(node_id, self.dependents)

    def dependency_cycles(self) -> list[list[str]]:
        """Strongly connected components with a cycle (Tarjan, iterative)."""
        index, low, on_stack, stack, cycles = {}, {}, set(), [], []
        counter = 0
        for root in sorted(self.nodes):
            if root in index:
                continue
            work = [(root, iter(self.prerequisites(root)))]
            index[root] = low[root] = counter
            counter += 1
            stack.append(root)
            on_stack.add(root)
            while work:
                node, children = work[-1]
                child = next(children, None)
                if child is None:
                    work.pop()
                    if work:
                        parent = work[-1][0]
                        low[parent] = min(low[parent], low[node])
                    if low[node] == index[node]:
                        component = []
                        while True:
                            member = stack.pop()
                            on_stack.discard(member)
                            component.append(member)
                            if member == node:
                                break
                        if len(component) > 1 or node in self.prerequisites(node):
                            cycles.append(sorted(component))
                elif child not in index:
                    index[child] = low[child] = counter
                    counter += 1
                    stack.append(child)
                    on_stack.add(child)
                    work.append((child, iter(self.prerequisites(child))))
                elif child in on_stack:
                    low[node] = min(low[node], index[child])
        return sorted(cycles)

    # -- neighbourhood ---------------------------------------------------

    def reverse(self, node_id: str) -> dict[str, list[str]]:
        """Derived reverse relations, keyed by the inverse label."""
        result: dict[str, list[str]] = defaultdict(list)
        for edge in self.incoming.get(node_id, ()):
            result[relation_type(edge.type).inverse].append(edge.source)
        return {k: sorted(v) for k, v in sorted(result.items())}

    def related(self, node_id: str) -> list[str]:
        """Symmetric view of `related`, whichever side declared it."""
        out = {e.target for e in self.outgoing.get(node_id, ()) if e.type == "related"}
        inc = {e.source for e in self.incoming.get(node_id, ()) if e.type == "related"}
        return sorted(out | inc)

    def neighbours(self, node_id: str) -> set[str]:
        out = {e.target for e in self.outgoing.get(node_id, ()) if e.target in self.nodes}
        inc = {e.source for e in self.incoming.get(node_id, ())}
        return out | inc

    def local(self, root: str, depth: int) -> set[str]:
        seen, frontier = {root}, {root}
        for _ in range(depth):
            frontier = {n for f in frontier for n in self.neighbours(f)} - seen
            seen |= frontier
        return seen

    def family_members(self, name: str, recursive: bool = False) -> list[str]:
        if not recursive:
            return list(self.families.get(name, ()))
        return sorted({m for f, members in self.families.items()
                       if f == name or f.startswith(name + ".") for m in members})

    # -- serialisation ---------------------------------------------------

    def to_json(self) -> dict:
        return {
            "version": 1,
            "nodes": [
                {
                    "id": n.id,
                    "path": n.path,
                    "title": n.title,
                    "families": list(n.families),
                    "relations": {k: list(v) for k, v in sorted(n.relations.items())},
                    "ancestors": self.ancestors(n.id),
                    "descendants": self.descendants(n.id),
                }
                for n in sorted(self.nodes.values(), key=lambda n: n.id)
            ],
            "edges": [{"source": e.source, "type": e.type, "target": e.target}
                      for e in self.edges],
        }

    def reverse_json(self) -> dict:
        return {nid: self.reverse(nid) for nid in sorted(self.nodes) if self.reverse(nid)}
