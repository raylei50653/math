#!/usr/bin/env python3
"""Two literal small-disk controls; no graph enumeration or catalogue mutation."""
import argparse
import itertools
import json
from pathlib import Path

PATTERNS = [
    (0, 1, 0, 1, 2), (0, 1, 0, 2, 1), (0, 1, 0, 2, 3),
    (0, 1, 2, 0, 1), (0, 1, 2, 0, 2), (0, 1, 2, 0, 3),
    (0, 1, 2, 1, 2), (0, 1, 2, 1, 3), (0, 1, 2, 3, 1),
    (0, 1, 2, 3, 2),
]
BOUNDARY = (0, 1, 2, 3, 4)
SOURCE_FACES = [
    (0, 1, 5), (1, 2, 5), (2, 6, 5), (2, 3, 6),
    (3, 4, 6), (4, 0, 6), (0, 5, 6),
]
GRAPHS = {
    "G": SOURCE_FACES,
    "D_flip": SOURCE_FACES[:5] + [(4, 0, 5, 6)],
    "F": SOURCE_FACES[:5] + [(4, 0, 5), (4, 5, 6)],
    "D_identify": [SOURCE_FACES[i] for i in (0, 1, 4, 5, 6)]
                  + [(2, 3, 6, 5)],
    "Q": [(0, 1, 3), (1, 2, 3), (0, 3, 6), (3, 4, 6), (4, 0, 6)],
}


def cycle_edges(face):
    return list(zip(face, face[1:] + face[:1]))


def disk_record(faces):
    """A rotation system plus Euler=2 certifies this explicit sphere embedding."""
    all_faces = faces + [tuple(reversed(BOUNDARY))]
    darts = [edge for face in all_faces for edge in cycle_edges(face)]
    assert len(darts) == len(set(darts))
    assert all((b, a) in darts for a, b in darts)
    edges = sorted({tuple(sorted(e)) for e in darts})
    vertices = sorted({v for edge in edges for v in edge})
    assert len(vertices) - len(edges) + len(all_faces) == 2
    assert all(len(face) == len(set(face)) for face in all_faces)
    rotation = {}
    for v in vertices:
        successor = {}
        for face in all_faces:
            if v in face:
                i = face.index(v)
                successor[face[i - 1]] = face[(i + 1) % len(face)]
        start = min(successor)
        seen = [start]
        while successor[seen[-1]] != start:
            assert successor[seen[-1]] not in seen
            seen.append(successor[seen[-1]])
        assert set(seen) == set(successor)
        rotation[v] = seen
    reached = {0}
    while True:
        new = reached | {b for a, b in darts if a in reached}
        if new == reached:
            break
        reached = new
    assert reached == set(vertices)
    interiors = sorted(set(vertices) - set(BOUNDARY))
    fibres = []
    for p in PATTERNS:
        full_lifts = []
        for values in itertools.product(range(4), repeat=len(interiors)):
            c = dict(zip(BOUNDARY, p)) | dict(zip(interiors, values))
            if all(c[a] != c[b] for a, b in edges):
                full_lifts.append([c[v] for v in vertices])
        fibres.append({"pattern": list(p), "full_lifts": full_lifts})
    mask = sum(1 << i for i, row in enumerate(fibres) if row["full_lifts"])
    return {
        "boundary": list(BOUNDARY), "vertices": vertices,
        "interiors": interiors, "edges": edges,
        "oriented_bounded_faces": [list(f) for f in faces],
        "rotation": rotation, "sigma_mask": mask,
        "fibres": fibres,
    }


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Read-only check (default)")
    mode.add_argument("--write", action="store_true", help="Exclusively create a new certificate")
    parser.add_argument("--certificate", type=Path,
                        default=Path(__file__).with_name("rewire_controls.json"))
    args = parser.parse_args()
    result = {name: disk_record(faces) for name, faces in GRAPHS.items()}
    assert [result[n]["sigma_mask"] for n in GRAPHS] == [567, 1015, 854, 959, 774]
    edge_sets = {
        name: {tuple(e) for e in graph["edges"]} for name, graph in result.items()
    }
    assert edge_sets["D_flip"] == edge_sets["G"] - {(0, 6)}
    assert edge_sets["F"] == edge_sets["D_flip"] | {(4, 5)}
    assert edge_sets["D_identify"] == edge_sets["G"] - {(2, 6)}
    expected_q = {
        tuple(sorted((3 if a == 5 else a, 3 if b == 5 else b)))
        for a, b in edge_sets["D_identify"]
    }
    assert edge_sets["Q"] == expected_q
    # Every original p* lift survives both operations. This is deliberately
    # weaker than preserving every row, which the recorded masks disprove.
    for full_lift in result["G"]["fibres"][9]["full_lifts"]:
        assert full_lift in result["F"]["fibres"][9]["full_lifts"]
        assert full_lift[5] == full_lift[3]
        assert [full_lift[v] for v in result["Q"]["vertices"]] in (
            result["Q"]["fibres"][9]["full_lifts"]
        )
    payload = {
        "status": "counterexample to a single-witness rewire criterion",
        "not_claimed": "No graph here has Sigma 933 or 941; no fixed-target exclusion.",
        "pattern_order": [list(p) for p in PATTERNS],
        "operations": {
            "flip": "G - {0,6} + {4,5}",
            "identify": "(G - {2,6}) / (5=3), then simplify parallel edges",
        },
        "graphs": result,
    }
    target = args.certificate
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        with target.open("x") as output:
            output.write(serialized)
    else:
        assert target.read_text() == serialized, "saved evidence differs"
    print(json.dumps({n: r["sigma_mask"] for n, r in result.items()}, sort_keys=True))


if __name__ == "__main__":
    main()
