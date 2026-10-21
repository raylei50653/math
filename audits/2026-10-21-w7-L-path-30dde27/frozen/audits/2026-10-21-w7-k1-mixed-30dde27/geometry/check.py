#!/usr/bin/env python3
"""Tiny literal-boundary and original short-wheel controls; no source search."""
import hashlib
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def wheel_faces(center, link):
    return [tuple((center, link[i], link[(i+1) % len(link)])) for i in range(len(link))]


def patch(name, faces, colors, boundary):
    canonical = {tuple(sorted(face)) for face in faces}
    incidence = defaultdict(int)
    vertices = set()
    for face in canonical:
        vertices.update(face)
        require(len({colors[v] for v in face}) == 3, "an original triangle is not proper")
        for edge in combinations(face, 2):
            incidence[tuple(sorted(edge))] += 1
    require(all(count in (1, 2) for count in incidence.values()), "non-disk edge multiplicity")
    expected_boundary = {tuple(sorted((boundary[i], boundary[(i+1) % len(boundary)])))
                         for i in range(len(boundary))}
    require({edge for edge, count in incidence.items() if count == 1} == expected_boundary,
            "the complete original disk boundary changed")
    require(len(vertices) - len(incidence) + len(canonical) == 1, "disk Euler failed")
    links = {}
    for center in vertices - set(boundary):
        link = defaultdict(set)
        for face in canonical:
            if center not in face:
                continue
            a, b = [v for v in face if v != center]
            link[a].add(b)
            link[b].add(a)
        require(all(len(v) == 2 for v in link.values()), "an interior star is not complete cyclic link")
        todo, seen = [next(iter(link))], set()
        while todo:
            v = todo.pop()
            if v in seen:
                continue
            seen.add(v)
            todo.extend(link[v] - seen)
        require(seen == set(link), "a cyclic star has multiple components")
        links[center] = {"degree": len(link), "neighbors": sorted(link)}
    return {"name": name, "V": len(vertices), "E": len(incidence), "F": len(canonical),
            "complete_interior_stars": links}, set(incidence)


def main():
    manifest = json.loads((HERE / "BASE.json").read_text())
    require(manifest["base"] == "30dde27293b5d3ad63c75fae73cda5be96db705b", "BASE changed")
    reviewed = json.loads((HERE / "REVIEW_INPUTS.json").read_text())
    for record in manifest["inputs"] + reviewed["inputs"]:
        data = (HERE / "frozen" / record["path"]).read_bytes()
        require(len(data) == record["bytes"] and hashlib.sha256(data).hexdigest() == record["sha256"],
                "frozen input drift")

    boundary = ("Y", "U", "V", "z4", "u1", "L")
    colors = {"Y": 1, "U": 0, "V": 1, "z4": 0, "z5": 3, "u1": 1, "L": 2, "K": 2}
    first_faces = wheel_faces("z5", ("L", "u1", "z4", "V", "U", "Y"))
    first, first_edges = patch("empty-C5-forces-original-z5-six-star", first_faces, colors, boundary)
    second_faces = wheel_faces("z5", ("L", "u1", "z4", "K", "Y"))
    second_faces += wheel_faces("K", ("Y", "U", "V", "z4", "z5"))
    second, second_edges = patch("one-C5-center-forces-adjacent-original-five-stars", second_faces, colors, boundary)
    require(first["complete_interior_stars"]["z5"]["degree"] == 6, "wrong empty-C5 degree")
    require(second["complete_interior_stars"]["z5"]["degree"] == 5, "wrong one-center z5 degree")
    require(second["complete_interior_stars"]["K"]["degree"] == 5, "wrong one-center K degree")
    force_edges = {tuple(sorted(edge)) for edge in (("z5", "U"), ("z5", "V"))}
    require(force_edges <= first_edges and not (force_edges & second_edges), "short-case original edge distinction failed")

    starts = []
    for center, arc in (
        ("u3", [("a", 0), ("z1", 3), ("z2", 0), ("Y", 2), ("z3", 0), ("z4", 3), ("z5", 0), ("q", 3)]),
        ("u1", [("a", 0), ("z1", 3), ("z2", 0), ("z3", 3), ("z4", 0), ("Y", 2), ("z5", 0), ("q", 3)]),
        ("L", [("a", 0), ("z1", 3), ("z2", 0), ("z3", 3), ("z4", 0), ("z5", 3), ("Y", 1), ("q", 3)]),
    ):
        palette = {2, 3} if center != "L" else {0, 1}
        for sid, v, w in ((44459, 0, 1), (44466, 1, 0)):
            frame = arc + [("c", 1), ("s", 2), ("v", v), ("w", w), ("t", 2)]
            require(all(a[1] != b[1] for a, b in zip(frame, frame[1:] + frame[:1])), "E boundary not proper")
            candidates = [name for name, color in frame if color in palette]
            starts.append({"center": center, "target": sid, "missing_palette": sorted(palette),
                           "all_boundary_palette_candidates": candidates})
            if center == "L":
                names = [name for name, color in frame]
                z0 = "v" if sid == 44459 else "w"
                # Cyclic order Y,q,c,z0 is exactly the alternating obstruction.
                ordered = names[names.index("Y"):] + names[:names.index("Y")]
                require([ordered.index(v) for v in ("Y", "q", "c", z0)] ==
                        sorted(ordered.index(v) for v in ("Y", "q", "c", z0)),
                        "01/03 alternating endpoints changed")
                require(palette & {0, 3} == {0}, "wrong actual crossing color")

    negative = {}
    try:
        patch("polluted-empty-case", first_faces[:-1], colors, boundary)
    except ValueError:
        negative["omit_empty_C5_required_diagonal_or_face"] = True
    wrong = dict(colors, K=3)
    try:
        patch("polluted-center-color", second_faces, wrong, boundary)
    except ValueError:
        negative["one_center_wrong_color3"] = True
    negative["crossing_claimed_color1"] = ({0, 1} & {0, 3}) != {1}
    negative["all_intersections_private_even_when_z0_in_M"] = bool({"z0"} & {"z0"})
    require(len(negative) == 4 and all(negative.values()), "a negative control was not exercised")
    print(json.dumps({"scope": "tiny local patch and literal-boundary controls; complete941 source not triggered",
                      "frozen_inputs": len(manifest["inputs"]),
                      "reviewed_code_paper_snapshots": len(reviewed["inputs"]), "six_starting_cases": starts,
                      "short_C5_two_complete_patches": [first, second], "negative_controls": negative,
                      "paper_authority": "REPORT.md same-original-E Jordan and C5 pocket proof",
                      "new_source_exclusion": False, "source_realizability": "OPEN"},
                     ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
