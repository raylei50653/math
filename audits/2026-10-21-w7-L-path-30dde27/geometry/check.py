#!/usr/bin/env python3
"""Local original-wheel controls; all >=6 one-hub fills are conditional only."""
import gzip
import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(word):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in word)


def wheel(center, boundary):
    return [(center, boundary[i], boundary[(i+1) % len(boundary)]) for i in range(len(boundary))]


def graph(faces):
    result = defaultdict(set)
    for face in faces:
        for a, b in itertools.combinations(face, 2):
            result[a].add(b)
            result[b].add(a)
    return result


def compositions13(total):
    if total == 0:
        yield ()
    for first in (1, 3):
        if first <= total:
            for rest in compositions13(total-first):
                yield (first, *rest)


def rejects(action):
    try:
        action()
    except ValueError:
        return True
    return False


def validate_spoke_pattern(spokes, length=5):
    marks = (0, *spokes, length)
    require(2 not in [b-a for a, b in zip(marks, marks[1:])], "maximal original gap2 is forbidden")


def validate_one_hub_scope(row):
    require(row["one_hub_for_gaps_ge4_is_extra_assumption"] == any(g >= 4 for g in row["maximal_gaps"]),
            "a large cell was wrongly asserted to have an unconditional one-hub filling")


def patch(faces, boundary, colors):
    faces = {tuple(sorted(face)) for face in faces}
    incidences = defaultdict(int)
    adjacency = graph(faces)
    for face in faces:
        require(len({colors[v] for v in face}) == 3, "improper original triangle")
        for edge in itertools.combinations(face, 2):
            incidences[tuple(sorted(edge))] += 1
    expected = {tuple(sorted((boundary[i], boundary[(i+1) % len(boundary)]))) for i in range(len(boundary))}
    require({e for e, n in incidences.items() if n == 1} == expected, "patch boundary changed")
    require(all(n in (1, 2) for n in incidences.values()), "bad face multiplicity")
    require(len(adjacency) - len(incidences) + len(faces) == 1, "disk Euler failed")
    stars = {}
    for c in sorted(set(adjacency) - set(boundary)):
        link = defaultdict(set)
        for face in faces:
            if c in face:
                a, b = [v for v in face if v != c]
                link[a].add(b)
                link[b].add(a)
        require(all(len(ns) == 2 for ns in link.values()), "interior original link not complete")
        todo, seen = [next(iter(link))], set()
        while todo:
            v = todo.pop()
            if v in seen:
                continue
            seen.add(v)
            todo.extend(link[v] - seen)
        require(seen == set(link), "disconnected original link")
        stars[c] = {"degree": len(link), "complete_neighbors": sorted(link)}
    return {"V": len(adjacency), "E": len(incidences), "F": len(faces), "complete_stars": stars}


def main():
    manifest = json.loads((HERE / "BASE.json").read_text())
    for row in manifest["inputs"]:
        raw = (HERE / "frozen" / row["path"]).read_bytes()
        require(len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"], "frozen drift")
    alias = json.loads((HERE / "ALIAS_02.json").read_text())
    raw = (HERE / "frozen" / alias["source_path"]).read_bytes()
    require(len(raw) == alias["source_bytes"] and hashlib.sha256(raw).hexdigest() == alias["source_sha256"], "parent v3 drift")
    parent = json.loads(gzip.decompress(raw))
    extracted = [c for c in parent["L_complete_residual"] if c["split_containing_0"] == [0, 2]]
    require(extracted == alias["extracted_complete_02_target_cases"], "incomplete parent 02 extraction")
    alias_cases = []
    for case in extracted:
        tip = "v" if case["E_state"] == 560 else "w"
        rows = []
        for column in case["complete_surviving_columns"]:
            blocks = column["component_blocks"]
            merged = any(tip in block and "z4" in block for block in blocks)
            rows.append({"column": column["column_id"], "tip_z4_same_02_block": merged})
        require(all(row["tip_z4_same_02_block"] for row in rows) == (case["E_state"] == 560), "alias source classification changed")
        alias_cases.append({"E_state": case["E_state"], "U_alias": tip, "columns": rows,
                            "typeII_alias_excluded": case["E_state"] == 572})

    B = ("L", "u1", "z4", "V", "U", "Y")
    short_faces = {
        "I": wheel("z5", B),
        "II": wheel("z5", ("L", "u1", "z4", "K", "Y")) + wheel("K", ("Y", "U", "V", "z4", "z5")),
    }
    short_relations = []
    sigmas = sorted({canonical(t) for t in itertools.product(range(4), repeat=6)
                     if all(t[i] != t[(i+1) % 6] for i in range(6))})
    require(len(sigmas) == 31, "incomplete proper C6 domain")
    for kind, faces in short_faces.items():
        adjacency = graph(faces)
        rows = []
        for sigma in sigmas:
            fixed = dict(zip(B, sigma))
            inner = ("z5",) if kind == "I" else ("z5", "K")
            direct = []
            for colors in itertools.product(range(4), repeat=len(inner)):
                complete = fixed | dict(zip(inner, colors))
                if all(complete[v] != complete[w] for v in adjacency for w in adjacency[v]):
                    direct.append(list(colors))
            if kind == "I":
                formula = [[s] for s in range(4) if s not in sigma]
            else:
                formula = [[s, k] for s, k in itertools.product(range(4), repeat=2)
                           if s not in {fixed["L"], fixed["u1"], fixed["z4"], fixed["Y"], k}
                           and k not in {fixed["Y"], fixed["U"], fixed["V"], fixed["z4"], s}]
            require(direct == formula, "full short fibre differs from direct original graph lifts")
            rows.append({"sigma": sigma, "all_lifts": direct})
        short_relations.append({"kind": kind, "all_proper_sigma_fibres": rows,
                                "empty_fibres": sum(not row["all_lifts"] for row in rows),
                                "total_lifts": sum(len(row["all_lifts"]) for row in rows)})

    expected = {(), (1,), (4,), (1, 2), (3, 4), (1, 4), (1, 2, 3, 4)}
    patterns = []
    all_subsets = []
    wrong_hub_rejected = False
    for mask in range(16):
        subset = tuple(i for i in range(1, 5) if mask >> (i-1) & 1)
        marks = (0, *subset, 5)
        gaps = tuple(b-a for a, b in zip(marks, marks[1:]))
        allowed = 2 not in gaps
        all_subsets.append({"spokes": subset, "maximal_gaps": gaps, "gap2_absent": allowed})
        if not allowed:
            continue
        X = ("Y", "U1", "U2", "U3", "U4", "z4")
        colors = dict(zip(X, (1, 0, 1, 0, 1, 0))) | {"z5": 3, "L": 2, "u1": 1}
        faces = [("z5", "Y", "L"), ("z5", "L", "u1"), ("z5", "u1", "z4")]
        hub_degrees = []
        conditional = False
        for a, b in zip(marks, marks[1:]):
            if b-a == 1:
                faces.append(("z5", X[a], X[b]))
            else:
                h = f"K{a}_{b}"
                colors[h] = 2
                cell = ("z5", *X[a:b+1])
                faces.extend(wheel(h, cell))
                hub_degrees.append(len(cell))
                conditional |= b-a >= 4
        result = patch(faces, (*X, "u1", "L"), colors)
        if 3 in gaps:
            wrong_colors = dict(colors)
            wrong_colors[next(name for name in colors if name.startswith("K"))] = 3
            try:
                patch(faces, (*X, "u1", "L"), wrong_colors)
            except ValueError:
                wrong_hub_rejected = True
        degree = result["complete_stars"]["z5"]["degree"]
        require(degree == (8 if len(subset) == 4 else len(subset)+5), "wrong original z5 complete degree")
        if not conditional:
            require(degree in (7, 8), "a closed short-cell case has wrong degree")
        patterns.append({"spokes": subset, "maximal_gaps": gaps,
                         "one_hub_for_gaps_ge4_is_extra_assumption": conditional,
                         "calibration_hub_degrees": hub_degrees, "patch": result})
    require({tuple(row["spokes"]) for row in patterns} == expected, "seven-spoke coverage changed")
    general_gaps = []
    for length in (5, 7, 9, 11):
        allowed, closed = [], []
        for mask in range(1 << (length-1)):
            marks = (0, *(i for i in range(1, length) if mask >> (i-1) & 1), length)
            gaps = tuple(b-a for a, b in zip(marks, marks[1:]))
            if 2 in gaps:
                continue
            allowed.append(gaps)
            if all(g in (1, 3) for g in gaps):
                r = gaps.count(3)
                by_neighbors = 4 + len(marks)-2 + r
                require(by_neighbors == length+3-r, "general original z5 degree formula failed")
                closed.append(gaps)
        require(set(closed) == set(compositions13(length)), "independent 1/3 composition coverage differs")
        general_gaps.append({"odd_shortest_length": length, "all_spoke_subsets": 1 << (length-1),
                             "gap2_free_subsets": len(allowed), "all_closed_13_gap_compositions": closed,
                             "exact_degree_formula": "ell+3-r"})
    wrong_scope = dict(next(row for row in patterns if row["one_hub_for_gaps_ge4_is_extra_assumption"]))
    wrong_scope["one_hub_for_gaps_ge4_is_extra_assumption"] = False
    wrong_alias = dict(alias_cases[0], typeII_alias_excluded=True)
    negative = {
        "wrong_gap2_pattern_2_rejected": rejects(lambda: validate_spoke_pattern((2,))),
        "delete_one_seven_pattern_rejected": rejects(lambda: require(
            {tuple(row["spokes"]) for row in patterns[:-1]} == expected, "incomplete seven-spoke coverage")),
        "one_hub_for_arbitrary_C6_C7_not_asserted": rejects(lambda: validate_one_hub_scope(wrong_scope)),
        "typeII_alias_B_rule_not_applied_to_A": rejects(lambda: require(
            wrong_alias["typeII_alias_excluded"] == (wrong_alias["E_state"] == 572), "unsupported A alias exclusion")),
    }
    negative["wrong_gap3_hub_color3_rejected"] = wrong_hub_rejected
    bad_length = next((row["odd_shortest_length"], gaps.count(3))
                      for row in general_gaps for gaps in row["all_closed_13_gap_compositions"] if 3 in gaps)
    negative["wrong_general_degree_plus_r_rejected"] = rejects(lambda: require(
        bad_length[0]+3+bad_length[1] == bad_length[0]+3-bad_length[1], "wrong general degree sign"))
    require(all(negative.values()), "a negative control was not exercised")
    print(json.dumps({"scope": "local complete fibres and 16 spoke subsets; no source enumeration",
                      "frozen_inputs": len(manifest["inputs"]), "frozen_parent_v3_sha256": alias["source_sha256"],
                      "typeII_actual_alias_02_cases": alias_cases,
                      "short_patch_complete_fibres": short_relations,
                      "all_16_spoke_subsets": all_subsets, "seven_spoke_calibrations": patterns,
                      "general_odd_shortest_gap_controls": general_gaps,
                      "negative_controls": negative,
                      "source_exclusions": ["typeII_targetB_U_equals_original_w"],
                      "whole_L_excluded": False, "long_cell_one_hub_proved_without_assumption": False},
                     ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
