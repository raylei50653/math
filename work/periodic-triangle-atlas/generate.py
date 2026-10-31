#!/usr/bin/env python3
"""Generate 12 numerical periodic triangle specimens; no classification claim.

Run: uv run --with scipy python work/periodic-triangle-atlas/generate.py
Dependencies are recorded in crystals.json. No project dependency is changed.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.spatial import Delaunay


OUTPUT = Path(__file__).with_name("crystals.json")


def torus_distance(a, b):
    d = np.abs(a - b)
    d = np.minimum(d, 1 - d)
    return float(np.linalg.norm(d))


def motif(kind, n, seed):
    rng = np.random.default_rng(seed)
    if kind in ("jitter", "shear"):
        side = math.isqrt(n)
        assert side * side == n
        p = np.array(
            [((i + 0.5) / side, (j + 0.5) / side)
             for i in range(side) for j in range(side)]
        )
        p = (p + rng.uniform(-0.44, 0.44, (n, 2)) / side) % 1
    else:
        p = []
        centers = rng.uniform(0, 1, (3, 2))
        min_distance = (0.31 if kind == "random" else 0.18) / math.sqrt(n)
        for _ in range(100000):
            if len(p) == n:
                break
            q = (rng.uniform(0, 1, 2) if kind == "random"
                 else (centers[len(p) % 3] + rng.normal(0, 0.12, 2)) % 1)
            if all(torus_distance(q, old) >= min_distance for old in p):
                p.append(q)
        assert len(p) == n
        p = np.asarray(p)
    # Coordinates are frozen BEFORE triangulation and serialization.
    return np.round(p, 8)


def triangulate(points, basis, halo):
    n = len(points)
    shifts = [(x, y) for x in range(-halo, halo + 1)
              for y in range(-halo, halo + 1)]
    frac = np.concatenate([points + shift for shift in shifts])
    physical = frac @ basis
    ids = [(v, sx, sy) for sx, sy in shifts for v in range(n)]
    tri = Delaunay(physical)
    result = []
    for vertices in tri.simplices:
        barycenter = frac[vertices].mean(axis=0)
        if np.all(barycenter >= 0) and np.all(barycenter < 1):
            face = [ids[int(k)] for k in vertices]
            a, b, c = physical[vertices]
            signed_twice_area = float(np.linalg.det(np.stack((b - a, c - a))))
            if signed_twice_area < 0:
                face[1], face[2] = face[2], face[1]
            start = min(range(3), key=face.__getitem__)
            result.append(tuple(face[start:] + face[:start]))
    assert len(set(result)) == len(result)
    return sorted(result)


def canonical_edge(a, b):
    forward = (a[0], b[0], b[1] - a[1], b[2] - a[2])
    reverse = (b[0], a[0], a[1] - b[1], a[2] - b[2])
    return (forward, 1) if forward < reverse else (reverse, -1)


def inspect(points, basis, faces):
    n = len(points)
    incidence = defaultdict(list)
    links = [defaultdict(list) for _ in points]
    areas, angles, lengths, clearances = [], [], [], []
    inv_basis = np.linalg.inv(basis)
    image_offsets = np.array([(x, y) for x in range(-2, 3)
                             for y in range(-2, 3)])
    used = set()
    for face_index, face in enumerate(faces):
        frac = np.array([points[v] + [dx, dy] for v, dx, dy in face])
        physical = frac @ basis
        a, b, c = physical
        area = float(np.linalg.det(np.stack((b - a, c - a)))) / 2
        assert area > 1e-12, ("degenerate face", face_index)
        areas.append(area)
        for k in range(3):
            u, v, w = face[k], face[(k + 1) % 3], face[(k + 2) % 3]
            used.add(u[0])
            key, sign = canonical_edge(u, v)
            incidence[key].append((face_index, sign))
            nv = (v[0], v[1] - u[1], v[2] - u[2])
            nw = (w[0], w[1] - u[1], w[2] - u[2])
            links[u[0]][nv].append(nw)
            links[u[0]][nw].append(nv)
            pv = physical[(k + 1) % 3] - physical[k]
            pw = physical[(k + 2) % 3] - physical[k]
            lengths.append(float(np.linalg.norm(pv)))
            cosine = np.dot(pv, pw) / (np.linalg.norm(pv) * np.linalg.norm(pw))
            angles.append(math.degrees(math.acos(float(np.clip(cosine, -1, 1)))))

        # Find the physical circumcenter of this face.
        center = np.linalg.solve(2 * np.stack((b - a, c - a)),
                                 np.array([np.dot(b, b) - np.dot(a, a),
                                           np.dot(c, c) - np.dot(a, a)]))
        radius2 = float(np.sum((center - a) ** 2))
        center_frac = center @ inv_basis
        nearest_shifts = np.rint(center_frac - points).astype(int)
        candidates_frac = points[:, None, :] + nearest_shifts[:, None, :] + image_offsets
        candidate_physical = candidates_frac @ basis
        distance2 = np.sum((candidate_physical - center) ** 2, axis=2)
        # Exclude the three face vertices; include all other periodic images.
        for vertex, dx, dy in face:
            actual_shifts = nearest_shifts[vertex] + image_offsets
            mask = np.all(actual_shifts == [dx, dy], axis=1)
            assert mask.sum() == 1
            distance2[vertex, mask] = np.inf
        clearance = float(np.min(distance2) - radius2)
        assert clearance > 1e-10, ("cocircular or interior point", face_index, clearance)
        # The finite candidate search is complete for each circle: any omitted
        # integer shift differs by at least 2.5 in one fractional coordinate;
        # sigma_min(B) bounds its Euclidean distance below.
        sigma_min = float(np.linalg.svd(basis, compute_uv=False)[-1])
        assert math.sqrt(radius2) < 2.5 * sigma_min
        clearances.append(clearance)

    edges = sorted(incidence)
    degrees = [0] * n
    for u, v, dx, dy in edges:
        assert (u, 0, 0) != (v, dx, dy)
        degrees[u] += 1
        degrees[v] += 1
    for edge, incidences in incidence.items():
        assert len(incidences) == 2, ("edge face count", edge, incidences)
        assert sum(sign for _, sign in incidences) == 0
    for root, link in enumerate(links):
        assert len(link) == degrees[root]
        assert all(len(adj) == 2 and len(set(adj)) == 2 for adj in link.values())
        start = next(iter(link))
        seen, stack = set(), [start]
        while stack:
            v = stack.pop()
            if v not in seen:
                seen.add(v)
                stack.extend(link[v])
        assert len(seen) == len(link)
    assert used == set(range(n))
    assert len(faces) == 2 * n and len(edges) == 3 * n
    assert n - len(edges) + len(faces) == 0
    assert sum(6 - degree for degree in degrees) == 0
    determinant = float(np.linalg.det(basis))
    assert math.isclose(sum(areas), determinant, rel_tol=1e-10, abs_tol=1e-10)
    return edges, degrees, {
        "vertices": n, "edges": len(edges), "faces": len(faces),
        "degree_counts": dict(sorted(Counter(degrees).items())),
        "area": round(sum(areas), 12), "mean_degree": sum(degrees) / n,
        "min_angle_degrees": round(min(angles), 6),
        "max_edge_length": round(max(lengths), 8),
        "min_nonface_circumcircle_clearance_squared": min(clearances),
    }


def main():
    specifications = [
        ("P01", "小塊錯落", "jitter", 9, 1103),
        ("P02", "中塊錯落", "jitter", 16, 1129),
        ("P03", "大塊錯落", "jitter", 25, 1151),
        ("P04", "長週期錯落", "jitter", 36, 1181),
        ("P05", "稀疏散點", "random", 8, 1201),
        ("P06", "散點小團", "random", 12, 1217),
        ("P07", "散點中團", "random", 18, 1237),
        ("P08", "散點大團", "random", 24, 1259),
        ("P09", "三簇小團", "cluster", 12, 1301),
        ("P10", "三簇中團", "cluster", 20, 1321),
        ("P11", "三簇大團", "cluster", 28, 1361),
        ("P12", "斜向重複", "shear", 16, 1409),
    ]
    examples = []
    for specimen_id, name, kind, n, seed in specifications:
        points = motif(kind, n, seed)
        basis = np.array([[1.0, 0.0], [0.32 if kind == "shear" else 0.0, 1.0]])
        faces2, faces3 = [triangulate(points, basis, halo) for halo in (2, 3)]
        assert faces2 == faces3, (specimen_id, "halo mismatch")
        edges, degrees, stats = inspect(points, basis, faces3)
        examples.append({
            "id": specimen_id, "name": name, "kind": kind, "seed": seed,
            "points": points.tolist(), "basis": basis.tolist(),
            "faces": faces3, "edges": edges, "degrees": degrees, "stats": stats,
            "checks": {key: True for key in [
                "halo2_equals_halo3", "edge_two_face_opposite",
                "vertex_links_cycles", "euler", "area", "curvature",
                "all_vertices_present", "positive_faces",
                "periodic_empty_circumcircles_numerical",
                "circumcircle_candidate_search_complete_bound",
            ]},
        })
        print(specimen_id, name, f"V/E/F={n}/{3*n}/{2*n}", stats["degree_counts"])
    payload = {
        "schema": "periodic-triangle-atlas/1",
        "method": {
            "algorithm": "SciPy Delaunay on 5x5 and 7x7 copies; central-barycenter face orbits",
            "dependencies": {"numpy": np.__version__, "scipy": scipy.__version__},
            "basis_convention": "physical = fractional[0]*basis[0] + fractional[1]*basis[1]",
            "face_vertex": "[motif_vertex_id, lattice_dx, lattice_dy]; CCW in physical plane",
            "edge": "[u,v,dx,dy] joins (u,0,0) to (v,dx,dy), undirected periodic edge orbit",
            "coordinate_precision": "8 decimal places, rounded before triangulation",
            "period_cell": "chosen repeating cell, not asserted primitive",
            "claim_scope": "12 numerical specimens, not exhaustive isomorphism classes; no coloring claims",
            "numerical_checks": "Float64, positive-area threshold 1e-12, strict empty-circle clearance >1e-10",
            "empty_circle_search": "Nearest fractional integer shift plus [-2,2]^2; omitted points bounded by 2.5*sigma_min(basis) exceeding radius",
        },
        "examples": examples,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {OUTPUT}: {len(examples)} specimens, all numerical checks passed.")


if __name__ == "__main__":
    main()
