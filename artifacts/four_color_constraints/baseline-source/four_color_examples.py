"""Small, reproducible graph fixtures for the four-colour experiment.

Coordinates are normalized straight-line drawings, not rotation-system proofs.
The random generator preserves a plane triangulation by face insertion and
geometrically legal edge flips.  Its distribution is deliberately not claimed
to be uniform over planar graphs or triangulations.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
import math
import random


def _graph(name, description, positions, edges, *, planar=True, fixed=()):
    result = {
        "name": name,
        "description": description,
        "vertices": list(range(len(positions))),
        "edges": [list(edge) for edge in sorted({tuple(sorted(e)) for e in edges})],
        "positions": [list(point) for point in positions],
        "expected_planar": planar,
    }
    if fixed:
        result["fixed"] = [list(pair) for pair in fixed]
    return result


def _cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _binomial_tree() -> dict:
    """T_1 is a vertex; T_k joins a new root to roots of T_1,...,T_(k-1)."""
    children = []
    edges = []

    def build(order):
        roots = [build(smaller) for smaller in range(1, order)]
        root = len(children)
        children.append(roots)
        edges.extend((root, child) for child in roots)
        return root

    root = build(5)
    positions = [None] * len(children)
    next_leaf = 0

    def place(vertex, depth):
        nonlocal next_leaf
        if children[vertex]:
            child_x = [place(child, depth + 1) for child in children[vertex]]
            x = sum(child_x) / len(child_x)
        else:
            x = 0.06 + 0.88 * next_leaf / 7
            next_leaf += 1
        positions[vertex] = [x, 0.08 + 0.21 * depth]
        return x

    place(root, 0)
    return _graph(
        "binomial_tree_t5",
        "這棵 16 點的樹可二染。選自然順序並關閉強制填色時，點 0、2、6、14 依序佔用色 1、2、3、4，最後堵住點 15；回退可修復這個前綴。",
        positions,
        edges,
    )


def random_triangulation(n: int, seed: int) -> dict:
    """Return a deterministic planar triangulation with ``n >= 3`` vertices.

    Start from a triangle.  Insert each new vertex strictly inside a randomly
    selected bounded triangular face, then try ``12*n`` random edge flips.
    A flip is accepted only when its two incident faces form a strictly convex
    quadrilateral and its new diagonal is absent.  Thus the stored drawing
    remains crossing-free.  Finally randomly relabel the vertices so natural
    vertex order does not simply undo the insertion order.
    """
    if isinstance(n, bool) or not isinstance(n, int) or n < 3:
        raise ValueError("n must be an integer at least 3")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    rng = random.Random(seed)
    positions = [(0.05, 0.94), (0.50, 0.06), (0.95, 0.94)]
    faces = [(0, 1, 2)]
    for vertex in range(3, n):
        index = rng.randrange(len(faces))
        a, b, c = faces.pop(index)
        # Positive weights keep the inserted point strictly inside its face.
        weights = [rng.uniform(0.7, 1.3) for _ in range(3)]
        total = sum(weights)
        point = tuple(
            sum(weight * positions[v][axis] for weight, v in zip(weights, (a, b, c))) / total
            for axis in (0, 1)
        )
        positions.append(point)
        faces.extend((tuple(sorted((a, b, vertex))), tuple(sorted((b, c, vertex))), tuple(sorted((a, c, vertex)))))

    accepted = 0
    for _ in range(12 * n):
        edge_faces = defaultdict(list)
        for index, face in enumerate(faces):
            for edge in combinations(face, 2):
                edge_faces[tuple(sorted(edge))].append(index)
        interior = sorted(edge for edge, incident in edge_faces.items() if len(incident) == 2)
        if not interior:
            break
        a, b = rng.choice(interior)
        left, right = edge_faces[(a, b)]
        u = next(v for v in faces[left] if v not in (a, b))
        v = next(v for v in faces[right] if v not in (a, b))
        if tuple(sorted((u, v))) in edge_faces:
            continue
        # Opposite diagonals must cross strictly in their interiors.  The
        # tolerance rejects tiny near-degenerate flips conservatively.
        if _cross(positions[a], positions[b], positions[u]) * _cross(positions[a], positions[b], positions[v]) >= -1e-20:
            continue
        if _cross(positions[u], positions[v], positions[a]) * _cross(positions[u], positions[v], positions[b]) >= -1e-20:
            continue
        faces[left] = tuple(sorted((u, v, a)))
        faces[right] = tuple(sorted((u, v, b)))
        accepted += 1

    edges = {tuple(sorted(edge)) for face in faces for edge in combinations(face, 2)}
    permutation = list(range(n))
    rng.shuffle(permutation)
    relabeled_positions = [None] * n
    for old, new in enumerate(permutation):
        relabeled_positions[new] = positions[old]
    graph = _graph(
        f"triangulation_n{n}_seed{seed}",
        f"平面三角剖分：面內插點 {n - 3} 次，合法凸四邊形翻邊 {accepted} 次，seed={seed}；最後隨機重編點號。這不是均勻抽樣。",
        relabeled_positions,
        [(permutation[a], permutation[b]) for a, b in edges],
    )
    graph["generator"] = {"method": "face-insertion-convex-flips-v1", "seed": seed, "n": n, "accepted_flips": accepted}
    return graph


def examples() -> list[dict]:
    """Return independent mutable fixtures; colour indices are 0, 1, 2, 3."""
    outer = [(0.08, 0.90), (0.50, 0.08), (0.92, 0.90)]
    k4 = _graph(
        "k4",
        "平面 K4 必須用到四種顏色，可觀察前三點填色後，第四點如何被迫選色。",
        outer + [(0.50, 0.62)],
        combinations(range(4), 2),
    )
    ring = [(0.50 + 0.41 * math.cos(2 * math.pi * i / 5 - math.pi / 2), 0.50 + 0.41 * math.sin(2 * math.pi * i / 5 - math.pi / 2)) for i in range(5)]
    wheel = _graph(
        "odd_wheel",
        "五邊形外圈加上中心點：奇圈需要三色，相鄰於整個外圈的中心需要第四色。",
        ring + [(0.50, 0.50)],
        [(i, (i + 1) % 5) for i in range(5)] + [(i, 5) for i in range(5)],
    )
    star_positions = [(0.50, 0.50), (0.50, 0.08), (0.92, 0.50), (0.50, 0.92), (0.08, 0.50)]
    star_edges = [(0, leaf) for leaf in range(1, 5)]
    free_star = _graph(
        "star_free",
        "四條輻射邊的星形圖可二染。與固定四片葉子為不同顏色的案例比較，就能區分原圖可染與固定前綴可延伸。",
        star_positions,
        star_edges,
    )
    fixed_star = _graph(
        "star_fixed_four_colours",
        "固定四片葉子為四種不同顏色，中心因此無色可填。無法延伸的是這份固定前綴；原圖仍可二染。",
        star_positions,
        star_edges,
        fixed=[(1, 0), (2, 1), (3, 2), (4, 3)],
    )
    k5 = _graph(
        "k5_nonplanar_control",
        "非平面負控制：K5 無法四色染色。圖中的交叉是刻意保留的；它不屬於四色定理的平面圖範圍。",
        ring,
        combinations(range(5), 2),
        planar=False,
    )
    natural_trap = random_triangulation(12, 0)
    natural_trap["description"] = (
        "可四色染色的平面三角剖分。自然順序即使開啟強制填色，仍會遇到一次衝突；"
        "改用 DSATUR 並開啟強制填色則避開該分支。產生器 n=12、seed=0，只重畫座標。"
    )
    dsatur_trap = random_triangulation(12, 8)
    dsatur_trap["description"] = (
        "可四色染色的平面三角剖分。即使用 DSATUR 並開啟強制填色，也會遇到兩次衝突；"
        "回退後找到合法染色。產生器 n=12、seed=8，只重畫座標。"
    )
    # Saved drawings from NetworkX 3.5 planar_layout, independently rescaled
    # into [.06, .94] on each axis.  Saving the small integer-grid drawings
    # improves readability without introducing a runtime layout dependency.
    natural_trap["positions"] = [
        [0.060, 0.060], [0.940, 0.060], [0.324, 0.412], [0.588, 0.148],
        [0.456, 0.764], [0.720, 0.236], [0.764, 0.324], [0.500, 0.588],
        [0.412, 0.412], [0.192, 0.236], [0.500, 0.940], [0.368, 0.324],
    ]
    dsatur_trap["positions"] = [
        [0.060, 0.060], [0.940, 0.060], [0.456, 0.236], [0.676, 0.500],
        [0.412, 0.676], [0.852, 0.148], [0.588, 0.324], [0.456, 0.500],
        [0.412, 0.324], [0.720, 0.412], [0.500, 0.940], [0.368, 0.588],
    ]
    for graph in (natural_trap, dsatur_trap):
        graph["layout"] = "saved-networkx-3.5-planar-layout-rescaled"
    return [k4, wheel, free_star, fixed_star, _binomial_tree(), natural_trap, dsatur_trap, k5]


def constraint_examples() -> list[dict]:
    """Add a planar list obstruction whose unary domains all remain nonempty."""
    trapped = _graph(
        "triangle_joint_conflict",
        "同一平面圖的兩個非相鄰頂點固定成色 3、4，讓中間三角形每點都剩 {1,2}。"
        "各點都有候選色，但三點無法共同異色；子構造表可在回寫前發現衝突。",
        [(0.06, 0.06), (0.94, 0.06), (0.50, 0.6467),
         (0.50, 0.3533), (0.50, 0.94)],
        [(0, 1), (1, 2), (0, 2)] + [(v, h) for v in range(3) for h in (3, 4)],
        fixed=[(3, 2), (4, 3)],
    )
    free = dict(trapped, name="triangle_joint_free", fixed=[],
                description="解除固定色後，同一張五點平面圖可四色染色；比較其完整關係消元與倒序回填。")
    base = examples()
    return [free, trapped, base[4], base[5], base[6], base[7]]
