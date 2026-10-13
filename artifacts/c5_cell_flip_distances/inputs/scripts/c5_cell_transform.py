#!/usr/bin/env python3
"""Exact edits and facial diagonal flips on an explicitly named C5 graph.

Keep the actual result graph for further edits. A catalogue match is only a
boundary-extension equivalence; it never replaces the graph automatically.
Requires networkx==3.5. See docs/c5_cell_flip.md for the paper contract.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import networkx as nx

from boundary_relations import normalize

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "artifacts/c5_cells/cells.json"
PATTERNS = tuple(sorted({normalize(p) for p in product(range(4), repeat=5)
                         if all(p[i] != p[(i + 1) % 5] for i in range(5))}))


def edge(pair):
    if len(pair) != 2 or any(type(v) is not int for v in pair) or pair[0] == pair[1]:
        raise ValueError("Edges must join two different integer vertex IDs")
    return tuple(sorted(pair))


def canonical_graph(graph):
    unexpected = set(graph) - {"vertices", "boundary", "edges"}
    if unexpected:
        raise ValueError(f"Unsupported graph fields (extra colour pins/rotations are not consumed): {sorted(unexpected)}")
    vertices, boundary = list(graph["vertices"]), list(graph["boundary"])
    if any(type(v) is not int for v in vertices) or len(set(vertices)) != len(vertices):
        raise ValueError("Vertices must be distinct integer IDs")
    if (len(boundary) != 5 or any(type(v) is not int for v in boundary)
            or len(set(boundary)) != 5 or not set(boundary) <= set(vertices)):
        raise ValueError("Boundary must name five distinct vertices in cyclic order")
    edges = [edge(e) for e in graph["edges"]]
    if len(set(edges)) != len(edges):
        raise ValueError("Duplicate edges are not allowed")
    if any(not set(e) <= set(vertices) for e in edges):
        raise ValueError("An edge names an absent vertex")
    cycle = {edge((boundary[i], boundary[(i + 1) % 5])) for i in range(5)}
    if not cycle <= set(edges):
        raise ValueError("The five boundary edges must be present")
    return {"vertices": sorted(vertices), "boundary": boundary,
            "edges": [list(e) for e in sorted(edges)]}


def read_catalogue(path=CATALOGUE):
    data = json.loads(Path(path).read_text())
    if data["pattern_order"] != [list(p) for p in PATTERNS]:
        raise ValueError("Catalogue pattern order does not match the fixed C5 frame")
    return data


def load_cell(mask, catalogue_path=CATALOGUE):
    data = read_catalogue(catalogue_path)
    if str(mask) not in data["cells"]:
        raise ValueError(f"No saved representative for class {mask}")
    saved = data["cells"][str(mask)]
    edges = {edge(e) for e in saved["edges"]}
    edges.update(edge((i, (i + 1) % 5)) for i in range(5))
    return canonical_graph({"vertices": list(range(5 + saved["k_eff"])),
                            "boundary": list(range(5)), "edges": list(edges)})


def with_edges(graph, edges):
    return canonical_graph({**graph, "edges": [list(e) for e in sorted(edges)]})


def topology(graph):
    """Return a checked disk rotation, or an explicit nonplanarity obstruction."""
    g = nx.Graph()
    g.add_nodes_from(graph["vertices"])
    g.add_edges_from(graph["edges"])
    planar, embedding = nx.check_planarity(g, counterexample=True)
    result = {"planar": planar, "disk": False, "connected": nx.is_connected(g)}
    if not planar:
        result["kuratowski_edges"] = [list(e) for e in sorted(edge(e) for e in embedding.edges())]
        return result
    apex = max(graph["vertices"]) + 1
    augmented = g.copy()
    augmented.add_edges_from((apex, b) for b in graph["boundary"])
    disk, embedding = nx.check_planarity(augmented, counterexample=True)
    result["disk"] = disk
    if not disk:
        result["apex"] = apex
        result["apex_kuratowski_edges"] = [list(e) for e in sorted(edge(e) for e in embedding.edges())]
        return result
    rotation = {v: [w for w in embedding.neighbors_cw_order(v) if w != apex]
                for v in graph["vertices"]}
    disk_embedding = nx.PlanarEmbedding()
    disk_embedding.set_data(rotation)
    disk_embedding.check_structure()
    visited, faces = set(), []
    for u, v in disk_embedding.edges():
        if (u, v) not in visited:
            face = disk_embedding.traverse_face(u, v, visited)
            start = face.index(min(face))
            faces.append(face[start:] + face[:start])
    result["rotation"] = [{"vertex": v, "clockwise": rotation[v]}
                          for v in graph["vertices"]]
    result["faces"] = sorted(faces)
    result["face_scope"] = "face boundary walks in each connected component"
    return result


def flip_candidates(graph, topo=None):
    """Facial flips in this computed disk embedding, not all embeddings."""
    topo = topology(graph) if topo is None else topo
    if not topo["disk"] or not topo["connected"]:
        return []
    edges = {edge(e) for e in graph["edges"]}
    boundary = graph["boundary"]
    cycle = {edge((boundary[i], boundary[(i + 1) % 5])) for i in range(5)}
    candidates = []
    for old in sorted(edges - cycle):
        incident = [f for f in topo["faces"]
                    if any(edge((f[i], f[(i + 1) % len(f)])) == old for i in range(len(f)))]
        if len(incident) != 2 or any(len(f) != 3 for f in incident):
            continue
        opposite = [next(v for v in f if v not in old) for f in incident]
        if len(set(old + tuple(opposite))) != 4:
            continue
        new = edge(opposite)
        if new in edges:
            continue
        candidates.append({"remove": list(old), "add": list(new),
                           "faces": incident,
                           "quadrilateral": [opposite[0], old[0], opposite[1], old[1]]})
    return candidates


def enumerate_rows(graph):
    """All lifts in one literal colour frame; vertex order is graph.vertices."""
    vertices, boundary = graph["vertices"], graph["boundary"]
    adjacent = {v: set() for v in vertices}
    for u, v in graph["edges"]:
        adjacent[u].add(v)
        adjacent[v].add(u)
    inner = set(vertices) - set(boundary)
    rows = []
    for pattern in PATTERNS:
        colors = dict(zip(boundary, pattern))
        lifts = []

        def visit(remaining):
            if not remaining:
                lifts.append([colors[v] for v in vertices])
                return
            options = {v: sorted(set(range(4)) - {colors[w] for w in adjacent[v] if w in colors})
                       for v in remaining}
            v = min(remaining, key=lambda w: (len(options[w]), w))
            for color in options[v]:
                colors[v] = color
                visit(remaining - {v})
                del colors[v]

        if all(colors[u] != colors[v] for u, v in graph["edges"] if u in colors and v in colors):
            visit(inner)
        lifts.sort()
        rows.append({"pattern": "".join(map(str, pattern)), "count": len(lifts), "lifts": lifts})
    return rows


def filter_rows(rows, graph, required):
    indices = {v: i for i, v in enumerate(graph["vertices"])}
    result = []
    for row in rows:
        lifts = [c for c in row["lifts"]
                 if all(c[indices[u]] != c[indices[v]] for u, v in required)]
        result.append({"pattern": row["pattern"], "count": len(lifts), "lifts": lifts})
    return result


def state(graph, rows):
    return {"graph": graph, "sigma": sum(1 << i for i, row in enumerate(rows) if row["count"]),
            "rows": rows, "topology": topology(graph)}


def analyze(graph, add=None, remove=None, require_flip=False, max_inner=8):
    graph = canonical_graph(graph)
    if type(max_inner) is not int or max_inner < 0:
        raise ValueError("max_inner must be a nonnegative integer")
    if len(graph["vertices"]) - 5 > max_inner:
        raise ValueError(f"Exact full-lift enumeration exceeds --max-inner {max_inner}")
    add = edge(add) if add is not None else None
    remove = edge(remove) if remove is not None else None
    edges = {edge(e) for e in graph["edges"]}
    boundary = graph["boundary"]
    cycle = {edge((boundary[i], boundary[(i + 1) % 5])) for i in range(5)}
    for operation in (add, remove):
        if operation is not None and not set(operation) <= set(graph["vertices"]):
            raise ValueError("An edit names an absent vertex")
    if remove is not None and remove not in edges:
        raise ValueError("The edge to remove is absent")
    if remove in cycle:
        raise ValueError("Removing a boundary edge would change the fixed C5")
    if add in edges:
        raise ValueError("The edge to add already exists")
    if require_flip and (add is None or remove is None):
        raise ValueError("A flip requires both the old and new diagonal")
    topo = topology(graph)
    candidate = next((c for c in flip_candidates(graph, topo)
                      if c["remove"] == list(remove or ()) and c["add"] == list(add or ())), None)
    if require_flip and candidate is None:
        raise ValueError("Not a facial diagonal flip of a connected graph in the saved disk embedding")
    common_edges = edges - ({remove} if remove else set())
    result_edges = common_edges | ({add} if add else set())
    common_graph = with_edges(graph, common_edges)
    common_rows = enumerate_rows(common_graph)
    source_rows = filter_rows(common_rows, graph, [remove] if remove else [])
    result_rows = filter_rows(common_rows, graph, [add] if add else [])
    source, result = state(graph, source_rows), state(with_edges(graph, result_edges), result_rows)
    report = {"schema": "c5-cell-transform-v1", "vertex_order": graph["vertices"],
              "pattern_order": ["".join(map(str, p)) for p in PATTERNS],
              "operations": {"remove": list(remove) if remove else None,
                             "add": list(add) if add else None,
                             "require_flip": require_flip},
              "max_inner": max_inner, "source": source, "result": result,
              "result_graph": result["graph"],
              "sigma_preserved": source["sigma"] == result["sigma"],
              "gained_patterns": [p["pattern"] for p, q in zip(result_rows, source_rows)
                                  if p["count"] and not q["count"]],
              "lost_patterns": [p["pattern"] for p, q in zip(source_rows, result_rows)
                                if p["count"] and not q["count"]]}
    if add and remove:
        report["flip"] = {"valid": candidate is not None and result["topology"]["disk"],
                          "embedding_scope": "the saved source disk rotation", "local": candidate}
        report["deleted"] = state(common_graph, common_rows)
        both_graph = with_edges(graph, edges | {add})
        report["both_edges"] = state(both_graph, filter_rows(common_rows, graph, [remove, add]))
        indices = {v: i for i, v in enumerate(graph["vertices"])}
        joint = []
        for row in common_rows:
            fibres = {key: {"count": 0, "lifts": []} for key in ("00", "01", "10", "11")}
            for c in row["lifts"]:
                key = "".join(str(int(c[indices[u]] != c[indices[v]])) for u, v in (remove, add))
                fibres[key]["lifts"].append(c)
                fibres[key]["count"] += 1
            joint.append({"pattern": row["pattern"], "fibres": fibres})
        report["joint_rows"] = joint
    return report


def catalogue_match(report, catalogue_path):
    """Recheck a saved same-frame representative without replacing the result."""
    data = read_catalogue(catalogue_path)
    mask = report["result"]["sigma"]
    resolved = Path(catalogue_path).resolve()
    path_reference = str(resolved.relative_to(ROOT)) if resolved.is_relative_to(ROOT) else str(resolved)
    result = {"path": path_reference,
              "sha256": sha256(Path(catalogue_path).read_bytes()).hexdigest(), "match": None}
    if str(mask) not in data["cells"]:
        return result
    # Catalogue boundary IDs 0..4 must follow this graph's literal boundary order.
    representative = load_cell(mask, catalogue_path)
    boundary = report["result_graph"]["boundary"]
    renaming = dict(zip(range(5), boundary))
    next_id = max(report["result_graph"]["vertices"]) + 1
    for offset, v in enumerate(representative["vertices"][5:]):
        renaming[v] = next_id + offset
    representative = canonical_graph({
        "vertices": [renaming[v] for v in representative["vertices"]], "boundary": boundary,
        "edges": [[renaming[u], renaming[v]] for u, v in representative["edges"]]})
    checked = state(representative, enumerate_rows(representative))
    if checked["sigma"] != mask or not checked["topology"]["disk"]:
        raise ValueError("Catalogue representative failed the independent graph replay")
    result["match"] = {"sigma": mask, "interior_count": len(representative["vertices"]) - 5,
                       "boundary_feasibility_equivalent": True,
                       "preserves_interior_identity_or_lift_counts": False,
                       "automatically_applied": False, "representative": checked}
    return result


def parse_vertex(token, graph):
    if token.startswith("b"):
        index = int(token[1:])
        if not 0 <= index < 5:
            raise ValueError("Boundary names are b0 through b4")
        return graph["boundary"][index]
    return int(token[1:] if token.startswith("v") else token)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sources = parser.add_mutually_exclusive_group(required=True)
    sources.add_argument("--cell", type=int, help="load this catalogue representative")
    sources.add_argument("--graph", type=Path, help="explicit graph JSON or a previous report")
    sources.add_argument("--check", type=Path, help="recompute and compare a saved complete report")
    parser.add_argument("--catalogue", type=Path, default=CATALOGUE)
    parser.add_argument("--add", nargs=2, metavar=("U", "V"))
    parser.add_argument("--remove", nargs=2, metavar=("U", "V"))
    parser.add_argument("--flip", nargs=4, metavar=("OLD_U", "OLD_V", "NEW_U", "NEW_V"))
    parser.add_argument("--list-flips", action="store_true")
    parser.add_argument("--max-inner", type=int, default=8)
    parser.add_argument("--output", type=Path, help="create a new report; never overwrite")
    parser.add_argument("--json", action="store_true", help="print the full report instead of the summary")
    args = parser.parse_args()
    try:
        if args.check:
            if args.add or args.remove or args.flip or args.list_flips or args.output:
                raise ValueError("--check does not accept edit or output options")
            saved = json.loads(args.check.read_text())
            report = analyze(saved["source"]["graph"], **saved["operations"], max_inner=saved["max_inner"])
            catalogue_path = Path(saved["catalogue"]["path"])
            if not catalogue_path.is_absolute():
                catalogue_path = ROOT / catalogue_path
            report["catalogue"] = catalogue_match(report, catalogue_path)
            if report != saved:
                raise ValueError("Saved report differs from the complete recomputation")
            print("PASS: graph, disk tests, ten full fibres, operations and catalogue match replayed")
            return
        if args.flip and (args.add or args.remove):
            raise ValueError("Use --flip or --add/--remove, not both")
        if args.list_flips and (args.add or args.remove or args.flip or args.output):
            raise ValueError("--list-flips only inspects the current graph")
        if args.cell is not None:
            graph = load_cell(args.cell, args.catalogue)
        else:
            loaded = json.loads(args.graph.read_text())
            graph = canonical_graph(loaded.get("result_graph", loaded))
        if args.list_flips:
            topo = topology(graph)
            if not topo["disk"] or not topo["connected"]:
                raise ValueError("Listing facial flips requires a connected C5 disk graph")
            print(json.dumps({"graph": graph, "topology": topo,
                              "scope": "candidates in this computed disk embedding only",
                              "flips": flip_candidates(graph, topo)}, indent=2))
            return
        removed = args.flip[:2] if args.flip else args.remove
        added = args.flip[2:] if args.flip else args.add
        report = analyze(graph,
                         add=tuple(parse_vertex(v, graph) for v in added) if added else None,
                         remove=tuple(parse_vertex(v, graph) for v in removed) if removed else None,
                         require_flip=bool(args.flip), max_inner=args.max_inner)
        if args.cell is not None and report["source"]["sigma"] != args.cell:
            raise ValueError("Source catalogue key does not match its actual graph")
        report["catalogue"] = catalogue_match(report, args.catalogue)
        if args.output:
            with args.output.open("x") as stream:
                json.dump(report, stream, indent=2)
                stream.write("\n")
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"Sigma: {report['source']['sigma']} -> {report['result']['sigma']}")
            print(f"Result planar={report['result']['topology']['planar']} disk={report['result']['topology']['disk']}")
            print(f"Sigma preserved: {report['sigma_preserved']}")
            print(f"Gained: {report['gained_patterns']}; lost: {report['lost_patterns']}")
            if "flip" in report:
                print(f"Facial flip: {report['flip']['valid']}")
                print(f"Delete-first: {report['source']['sigma']} -> {report['deleted']['sigma']} -> {report['result']['sigma']}")
                print(f"Both-edge intermediate: {report['both_edges']['sigma']} (disk={report['both_edges']['topology']['disk']})")
            match = report["catalogue"]["match"]
            if match:
                print(f"Verified catalogue representative: {match['interior_count']} interior vertices; graph not replaced")
            if args.output:
                print(f"Saved full report: {args.output}")
    except (ValueError, KeyError, TypeError, OSError, nx.NetworkXException) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
