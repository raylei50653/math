"""Deliberately restrained validation.

Errors are only real data faults: unparsable metadata, duplicate ids,
checked relations naming unknown ids, and cycles in the dependency
projection. Missing families or relations are never errors; the few
informational notes exist for discovery and do not fail by default.
"""
from __future__ import annotations

from collections import defaultdict

from .graph import Graph
from .model import Diagnostic, Node, relation_type


def validate(nodes: list[Node], parse_diagnostics: list[Diagnostic]) -> tuple[Graph, list[Diagnostic]]:
    diags = list(parse_diagnostics)

    paths = defaultdict(list)
    for node in nodes:
        paths[node.id].append(node.path)
    for node_id, where in sorted(paths.items()):
        if len(where) > 1:
            diags.append(Diagnostic("error", "duplicate-id",
                                    f"id '{node_id}' is declared by {', '.join(where)}"))

    graph = Graph(nodes)
    for edge in graph.edges:
        if relation_type(edge.type).checked and edge.target not in graph.nodes:
            diags.append(Diagnostic("error", "unknown-target",
                                    f"'{edge.source}' {edge.type} unknown id '{edge.target}'",
                                    graph.nodes[edge.source].path))
    for cycle in graph.dependency_cycles():
        diags.append(Diagnostic("error", "dependency-cycle",
                                "requires/derives_from cycle: " + " -> ".join(cycle + cycle[:1])))

    for node_id, node in sorted(graph.nodes.items()):
        if not node.families and not graph.neighbours(node_id):
            diags.append(Diagnostic("info", "unconnected",
                                    f"'{node_id}' has no family and no relations", node.path))
    for family, members in graph.families.items():
        if len(members) == 1:
            diags.append(Diagnostic("info", "single-member-family",
                                    f"family '{family}' has only '{members[0]}'"))
    superseded = {e.target: e.source for e in graph.edges if e.type == "supersedes"}
    for edge in graph.dependency_edges():
        if edge.target in superseded:
            diags.append(Diagnostic("info", "superseded-target",
                                    f"'{edge.source}' {edge.type} '{edge.target}', "
                                    f"superseded by '{superseded[edge.target]}'",
                                    graph.nodes[edge.source].path))
    return graph, diags
