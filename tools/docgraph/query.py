"""Human-readable queries over the graph."""
from __future__ import annotations

import re
from pathlib import Path

from .graph import Graph
from .model import CORE_RELATIONS

PEERS = 10  # family peers listed per family in `show`


def _section(title: str, items) -> str:
    items = list(items)
    return "\n".join([f"{title}:", *[f"  {i}" for i in items]]) if items else ""


def show(graph: Graph, node_id: str) -> str:
    node = graph.nodes[node_id]
    head = [node_id] + ([f"  {node.title}"] if node.title else []) + [f"  {node.path}"]
    blocks = ["\n".join(head), _section("Families", node.families)]
    for rel in ("requires", "derives_from"):
        blocks.append(_section(rel.replace("_", " ").capitalize(), node.relations.get(rel, ())))
    blocks.append(_section("Related", graph.related(node_id)))
    for rel, targets in sorted(node.relations.items()):
        if rel not in CORE_RELATIONS:
            blocks.append(_section(rel, targets))
    reverse = graph.reverse(node_id)
    reverse.pop("related_from", None)  # already merged into Related
    for label, sources in reverse.items():
        blocks.append(_section(label.replace("_", " ").capitalize(), sources))
    ancestors, descendants = graph.ancestors(node_id), graph.descendants(node_id)
    if ancestors or descendants:
        blocks.append(f"Dependency closure: {len(ancestors)} ancestors, "
                      f"{len(descendants)} descendants")
    # Narrowest family first: it is usually the most informative grouping.
    for name in sorted(node.families, key=lambda f: len(graph.families[f])):
        peers = [m for m in graph.families[name] if m != node_id]
        shown = peers[:PEERS] + ([f"... {len(peers) - PEERS} more: docgraph family {name}"]
                                 if len(peers) > PEERS else [])
        blocks.append(_section(f"Family {name}", shown))
    return "\n\n".join(b for b in blocks if b)


def family(graph: Graph, name: str, recursive: bool = False) -> str:
    members = graph.family_members(name, recursive)
    lines = [f"Family: {name}" + (" (with sub-families)" if recursive else ""), ""]
    width = max((len(m) for m in members), default=0)
    lines += [f"  {m:<{width}}  {graph.nodes[m].title}" for m in members]
    return "\n".join(lines)


def families(graph: Graph) -> str:
    width = max((len(f) for f in graph.families), default=0)
    return "\n".join(f"{f:<{width}}  {len(m)}" for f, m in graph.families.items())


LINK = re.compile(r"\]\(\s*<?([^\s)>#]+\.md)(?:#[^\s)>]*)?>?(?:\s+[^)]*)?\)")


def suggest(graph: Graph, root: Path) -> list[tuple[str, str, int]]:
    """Candidate relations only: Markdown links between nodes with no declared
    relation in either direction. Never written anywhere."""
    by_path = {(root / n.path).resolve(): n.id for n in graph.nodes.values()}
    declared = {frozenset((e.source, e.target)) for e in graph.edges}
    counts: dict[tuple[str, str], int] = {}
    for node in graph.nodes.values():
        source = root / node.path
        for target in LINK.findall(source.read_text(encoding="utf-8")):
            other = by_path.get((source.parent / target).resolve())
            if other and other != node.id and frozenset((node.id, other)) not in declared:
                counts[(node.id, other)] = counts.get((node.id, other), 0) + 1
    return sorted((a, b, n) for (a, b), n in counts.items())
