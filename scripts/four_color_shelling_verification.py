#!/usr/bin/env python3
"""Independently check canonical-shelling geometry, not four-colourability.

NetworkX supplies a candidate ordering. Checks use the original embedding,
induced original edges, and face traversals; no colouring oracle is used.
"""

import argparse
import hashlib
import json
from pathlib import Path

import networkx as nx
from networkx.algorithms.planar_drawing import get_canonical_ordering


def faces(embedding):
    seen, result = set(), []
    for u in embedding:
        for v in embedding.neighbors_cw_order(u):
            if (u, v) not in seen:
                result.append(embedding.traverse_face(u, v, seen))
    return result


def induced_embedding(original, active):
    rotation = {
        u: [v for v in original.neighbors_cw_order(u) if v in active]
        for u in sorted(active)
    }
    result = nx.PlanarEmbedding()
    result.set_data(rotation)
    result.check_structure()
    return result


def verify(name, graph, outer=None):
    planar, embedding = nx.check_planarity(graph)
    assert planar
    assert all(len(f) == 3 for f in faces(embedding))
    if outer is None:
        outer = faces(embedding)[0]
    else:
        # Preserve the orientation of this face in the supplied embedding.
        outer = next(f for f in faces(embedding) if set(f) == set(outer))
        # Both directions of the base are valid. The third point stays last.
        outer = next(outer[j:] + outer[:j] for j in range(3)
                     if set((outer[j], outer[(j + 1) % 3])) == {0, 1})
    order = [v for v, _ in get_canonical_ordering(embedding, outer)]
    assert len(set(order)) == len(graph)
    u, v = order[:2]
    boundaries, steps = {}, []
    for k in range(3, len(order) + 1):
        active = set(order[:k])
        prefix = graph.subgraph(active)
        induced = induced_embedding(embedding, active)
        boundary = induced.traverse_face(u, v)
        assert len(boundary) == len(set(boundary))
        assert nx.is_biconnected(prefix)
        all_faces = faces(induced)
        directed_boundary = set(zip(boundary, boundary[1:] + boundary[:1]))
        outer_faces = 0
        for face in all_faces:
            if set(zip(face, face[1:] + face[:1])) == directed_boundary:
                outer_faces += 1
            else:
                assert len(face) == 3
        assert outer_faces == 1
        # Original remaining endpoints of every processed edge lie on this ring.
        removed = set(graph) - active
        frontier = {b for a in removed for b in graph[a] if b in active}
        assert frontier <= set(boundary)
        if removed:
            assert nx.is_connected(graph.subgraph(removed))
        boundaries[k] = boundary
        if k == 3:
            assert set(boundary) == active
            continue
        x = order[k - 1]
        previous = boundaries[k - 1]
        neighbours = set(graph[x]) & set(order[:k - 1])
        # All lower neighbours form one interval in the outer path avoiding uv.
        path = [previous[0]] + list(reversed(previous[1:]))
        indices = [i for i, w in enumerate(path) if w in neighbours]
        assert len(indices) >= 2
        assert indices == list(range(min(indices), max(indices) + 1))
        assert set(boundary) == (set(previous) - set(path[min(indices) + 1:max(indices)])) | {x}
        assert x in boundary
        # Reversing insertion replaces x by the intervening original path.
        steps.append({"removed": x, "lower_neighbours": path[min(indices):max(indices) + 1],
                      "boundary_before": len(boundary), "boundary_after": len(previous)})
    return {"name": name, "vertices": len(graph), "edges": graph.number_of_edges(),
            "canonical_order": order, "outer_face": outer,
            "peak_boundary": max(map(len, boundaries.values())),
            "prefixes_checked": len(boundaries), "reverse_steps": list(reversed(steps))}


def bipyramid(r):
    graph = nx.cycle_graph(r)
    graph.add_edges_from((hub, v) for hub in (r, r + 1) for v in range(r))
    return graph


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    cases = []
    for index, graph in enumerate(nx.graph_atlas_g()):
        n = len(graph)
        if n >= 4 and graph.number_of_edges() == 3 * n - 6 and nx.check_planarity(graph)[0]:
            cases.append(verify(f"atlas-{index}", graph))
    cases.append(verify("icosahedron", nx.icosahedral_graph()))
    for r in (4, 5, 8, 16, 32):
        case = verify(f"bipyramid-{r}", bipyramid(r), outer=[0, 1, r])
        assert case["reverse_steps"][0]["removed"] == r
        assert case["reverse_steps"][0]["boundary_after"] == r
        cases.append(case)
    report = {
        "schema": "four-color-shelling-verification-v1",
        "networkx_version": nx.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "finite embedding/order checks; no Lean proof or 4CT existence inference",
        "cases": cases,
        "total_cases": len(cases),
        "total_prefixes": sum(c["prefixes_checked"] for c in cases),
        "total_reverse_steps": sum(len(c["reverse_steps"]) for c in cases),
    }
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
