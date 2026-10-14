#!/usr/bin/env python3
"""Exact local p/q deletions and complete-fibre controls; no graph search."""
import argparse
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = "ABCD"
WORDS = ("ABAB", "ABAC", "ABCB", "ABCD")


def triangle_palettes(z):
    return tuple(itertools.permutations([c for c in COLORS if c != z], 2))


def original_joint_accept(outer, ordered):
    z, s, r, t = outer
    palette = set(ordered)
    if z == r and s == t:
        return palette == set(COLORS) - {z, s}
    if z == r:
        return False
    if s == t:
        missing = (set(COLORS) - set(outer)).pop()
        return missing in palette
    return palette == {s, t}


def local_tables():
    single, double, shared = {}, {}, {}
    for word in WORDS:
        z, q, ell, m = word
        lifts = [c for c in COLORS if c not in word]
        good = ["".join(xy) for xy in triangle_palettes(z)
                if all(set(xy) == {q, p} for p in lifts)]
        single[word] = {"all_p_lifts": lifts, "universally_admissible_xy": good}

        z, m, ell, n = word
        pairs = [(p, q) for p in COLORS for q in COLORS
                 if p not in {z, m, ell} and q not in {z, ell, n, p}]
        good = ["".join(xy) for xy in triangle_palettes(z)
                if all(set(xy) == set(pq) for pq in pairs)]
        double[word] = {"all_pq_lifts": ["".join(pq) for pq in pairs],
                        "universally_admissible_xy": good}

        z, m, w, n = word
        ell_colors = [c for c in COLORS if c not in {m, w, n}]
        good = ["".join(xy) for xy in triangle_palettes(z)
                if all(original_joint_accept((z, m, ell, n), xy)
                       for ell in ell_colors)]
        shared[word] = {"all_ell_lifts": ell_colors,
                        "universally_admissible_xy": good}
    assert [single[w]["universally_admissible_xy"] for w in WORDS] == [
        [], ["BD", "DB"], ["BD", "DB"], ["BC", "BD", "CB", "CD", "DB", "DC"]]
    assert [double[w]["universally_admissible_xy"] for w in WORDS] == [
        ["CD", "DC"], [], ["BC", "BD", "CB", "CD", "DB", "DC"], ["BD", "DB"]]
    assert [shared[w]["universally_admissible_xy"] for w in WORDS] == [
        ["CD", "DC"], ["BC", "CB"], ["CD", "DC"], []]
    return {"single_p_deletion": single, "double_pq_deletion": double,
            "shared_ell_deletion": shared}


def actual_mask14_control():
    # A single explicitly named triangulated C4 disk, with no separating-source claim.
    vertices = ("z", "q", "ell", "m", "X", "Y", "W")
    edges = [("z", "q"), ("q", "ell"), ("ell", "m"), ("m", "z"),
             ("X", "Y"), ("Y", "W"), ("W", "X"),
             ("z", "X"), ("q", "X"), ("q", "Y"), ("ell", "Y"),
             ("ell", "W"), ("m", "W"), ("z", "W")]
    faces = [("z", "q", "X"), ("q", "Y", "X"), ("q", "ell", "Y"),
             ("ell", "W", "Y"), ("ell", "m", "W"), ("m", "z", "W"),
             ("z", "X", "W"), ("X", "Y", "W")]
    incidences = {tuple(sorted(e)): 0 for e in edges}
    for a, b, c in faces:
        for e in ((a, b), (b, c), (c, a)):
            incidences[tuple(sorted(e))] += 1
    boundary = {tuple(sorted(e)) for e in edges[:4]}
    assert all(n == (1 if e in boundary else 2) for e, n in incidences.items())
    outer_face = ("z", "m", "ell", "q")
    all_faces = faces + [outer_face]
    assert len(vertices) - len(edges) + len(all_faces) == 2
    darts = []
    links = {v: {} for v in vertices}
    for face in all_faces:
        for i, v in enumerate(face):
            previous, following = face[i - 1], face[(i + 1) % len(face)]
            darts.append((v, following))
            assert previous not in links[v]
            links[v][previous] = following
    assert len(darts) == len(set(darts)) == 2 * len(edges)
    assert all((b, a) in darts for a, b in darts)
    rotations = {}
    for v in vertices:
        neighbors = {b if a == v else a for a, b in edges if v in (a, b)}
        assert set(links[v]) == set(links[v].values()) == neighbors
        start = min(neighbors)
        cycle, current = [], start
        while current not in cycle:
            cycle.append(current)
            current = links[v][current]
        assert current == start and set(cycle) == neighbors
        rotations[v] = cycle
    fibres = {}
    for word in WORDS:
        rows = []
        for rest in itertools.product(COLORS, repeat=3):
            f = dict(zip(vertices, tuple(word) + rest))
            if all(f[a] != f[b] for a, b in edges):
                rows.append("".join(f[v] for v in vertices))
        fibres[word] = rows
    mask = sum(1 << i for i, w in enumerate(WORDS) if fibres[w])
    assert mask == 14
    # Distinguished facial triangle is z-X-W. The full bad-palette contract fails.
    witness = next(row for row in fibres["ABAC"] if {row[4], row[6]} != {"B", "D"})
    return {"vertices": vertices, "edges": edges, "triangular_faces": faces,
            "outer_face": outer_face, "vertex_rotations": rotations,
            "embedding_validation": "Euler=2; all directed darts exactly once; one cyclic link per vertex",
            "full_fixed_frame_fibres": fibres, "mask": mask,
            "ABAC_bad_palette_failure_witness": witness,
            "source_controls": 0}


def abstract_residual_control():
    # A complete S4-closed abstract six-pin relation, not a graph colouring relation.
    selected = ["ABACBD", "ABC BBD".replace(" ", ""), "ABCDBC", "ABCDBD"]
    relation = set()
    for row in selected:
        for perm in itertools.permutations(COLORS):
            rename = dict(zip(COLORS, perm))
            relation.add("".join(rename[c] for c in row))
    fibres = {w: sorted(row for row in relation if row[:4] == w) for w in WORDS}
    assert not fibres["ABAB"]
    assert all(set(row[4:]) == {"B", "D"} for w in ("ABAC", "ABCB") for row in fibres[w])
    assert all(set(row[4:]) in ({"B", "C"}, {"B", "D"}) for row in fibres["ABCD"])
    assert len(fibres["ABCD"]) == len(fibres["ABAC"]) + len(fibres["ABCB"])
    return {"vertices": ("z", "q", "ell", "m", "x", "y"),
            "full_fixed_frame_abstract_fibres": fibres,
            "S4_closed_relation_size": len(relation),
            "mask": 14, "no_rainbow_hypothesis": False,
            "graph_realizability_asserted": False}


def build():
    return {"status": "PASS", "scope": "local exhaustive assignment controls, not source enumeration",
            "tables": local_tables(), "actual_mask14_control": actual_mask14_control(),
            "abstract_residual_control": abstract_residual_control()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate-final.json")
    args = parser.parse_args()
    result = build()
    artifact = args.certificate
    if args.check:
        assert json.loads(artifact.read_text()) == json.loads(json.dumps(result))
    else:
        with artifact.open("x") as out:
            json.dump(result, out, indent=2, sort_keys=True)
            out.write("\n")
    print("PASS: exact local tables, literal full-fibre mask14 disk, and abstract residual control; source controls=0")


if __name__ == "__main__":
    main()
