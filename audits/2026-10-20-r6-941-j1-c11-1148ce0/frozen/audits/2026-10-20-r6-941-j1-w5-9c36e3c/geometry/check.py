#!/usr/bin/env python3
"""Replay the original W5 seven-rim chord and contact certificates (stdlib)."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FROZEN = HERE.parent / "frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c"
CHAINS = FROZEN / "frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/frozen/audits/2026-10-19-r6-941-existence-f13eb4d/frozen/audits/2026-10-19-r6-941-chains-13dc5ff"
ACCEPTANCE = CHAINS.parent / "2026-10-19-r6-941-acceptance-13dc5ff"


def edge(x, y):
    return tuple(sorted((x, y)))


def inputs():
    return {
        str(p.relative_to(HERE.parent)): sha256(p.read_bytes()).hexdigest()
        for p in (
            FROZEN / "SOURCE_CONTRACT.md",
            FROZEN / "geometry/PROOF.md",
            FROZEN / "geometry/certificate.json",
            CHAINS / "B/PROOF.md",
            CHAINS / "B/certificate.json",
            ACCEPTANCE / "PROOF.md",
        )
    }


def separated_faces(faces, path):
    """Part of the original patch separated from the original outer edge ab."""
    cut = {edge(x, y) for x, y in zip(path, path[1:])}
    dual = {i: set() for i in range(len(faces))}
    for i, j in combinations(range(len(faces)), 2):
        common = set(faces[i]) & set(faces[j])
        if len(common) == 2 and tuple(sorted(common)) not in cut:
            dual[i].add(j)
            dual[j].add(i)
    anchor = [i for i, f in enumerate(faces) if {"a", "b"} <= set(f)]
    assert len(anchor) == 1
    seen = set(anchor)
    todo = list(anchor)
    while todo:
        for j in dual[todo.pop()] - seen:
            seen.add(j)
            todo.append(j)
    other = sorted(set(dual) - seen)
    assert other
    return other


def crosses(chord1, chord2, rim):
    if set(chord1) & set(chord2):
        return False
    i, j = sorted(rim.index(v) for v in chord1)
    k, l = sorted(rim.index(v) for v in chord2)
    return (i < k < j < l) or (k < i < l < j)


def build():
    upstream = json.loads((FROZEN / "geometry/certificate.json").read_text())
    patch = upstream["exceptional_patch"]
    faces = patch["faces"]
    rim = patch["rim"]
    assert rim == ["a", "b", "q", "L", "u1", "u2", "n"]
    counts = Counter(edge(f[i], f[(i + 1) % 3]) for f in faces for i in range(3))
    assert {e for e, n in counts.items() if n == 1} == {
        edge(rim[i], rim[(i + 1) % 7]) for i in range(7)
    }
    assert all(n in (1, 2) for n in counts.values())
    paths = [
        ["a", "p", "q"],
        ["a", "p", "h", "L"],
        ["a", "p", "h", "R", "u1"],
        ["a", "p", "h", "R", "u2"],
        ["b", "p", "h", "L"],
        ["b", "p", "h", "R", "u1"],
        ["b", "p", "h", "R", "u2"],
        ["b", "p", "n"],
        ["q", "h", "R", "u1"],
        ["q", "h", "R", "u2"],
        ["q", "p", "n"],
        ["L", "R", "u2"],
        ["L", "h", "n"],
        ["u1", "R", "n"],
    ]
    rows = []
    for path in paths:
        assert len(set(path)) == len(path)
        assert all(edge(x, y) in counts for x, y in zip(path, path[1:]))
        other = separated_faces(faces, path)
        enclosed = sorted(set().union(*(set(faces[i]) for i in other)) - set(path))
        length = len(path)  # path edges + one hypothetical exterior chord
        excluded = (length in (3, 4) and bool(enclosed)) or (
            length == 5 and len(enclosed) >= 2
        )
        rows.append({
            "chord": [path[0], path[-1]],
            "original_path": path,
            "cycle_length_if_chord_exists": length,
            "enclosed_original_vertices_at_least": enclosed,
            "original_patch_faces_separated_from_ab": other,
            "excluded_by_pocket_theorem": excluded,
        })
    diagonals = {
        edge(rim[i], rim[j])
        for i, j in combinations(range(7), 2)
        if (j - i) not in (1, 6)
    }
    assert {edge(*r["chord"]) for r in rows} == diagonals
    assert [r["chord"] for r in rows if not r["excluded_by_pocket_theorem"]] == [["a", "u2"]]

    old = json.loads((CHAINS / "B/certificate.json").read_text())
    allowed = [set(r["contacts"]) for r in old["complete_contact_subsets"] if r["necessary_allowed"]]
    # Full-star seven-rim exclusions plus inherited original-graph distance bounds.
    requirements = {"u1": {"R", "L"}, "u2": {"n", "R"}}
    bans = {"u1": {"a", "n", "q", "s", "t"}, "u2": {"q", "L", "t"}}
    profiles = {
        u: [sorted(S) for S in allowed if requirements[u] <= S and not (S & bans[u])]
        for u in requirements
    }
    c11 = ["a", "n", "u2", "u1", "L", "q", "c", "s", "v", "w", "t"]
    extras = {
        u: set().union(*(set(S) for S in profiles[u])) - requirements[u]
        for u in profiles
    }
    chords = sorted(edge(u, v) for u, values in extras.items() for v in values)
    joint = []
    rejected = []
    for S1 in profiles["u1"]:
        for S2 in profiles["u2"]:
            actual = sorted(edge("u1", v) for v in set(S1) - requirements["u1"])
            actual += sorted(edge("u2", v) for v in set(S2) - requirements["u2"])
            crossing = [[list(x), list(y)] for x, y in combinations(actual, 2) if crosses(x, y, c11)]
            target = rejected if crossing else joint
            target.append({"u1_old_rim_contacts": S1, "u2_old_rim_contacts": S2, "crossings": crossing})
    # anR is the only allowed profile containing a; no global realization is asserted.
    assert [S for S in profiles["u2"] if "a" in S] == [["R", "a", "n"]]
    return {
        "input_sha256": inputs(),
        "original_rim": rim,
        "pocket_chord_records": rows,
        "possible_original_seven_rim_chords": [["a", "u2"]],
        "degree_split": {
            "a_u2_present": {"n_degree": 5, "n_star": ["a", "p", "h", "R", "u2"], "outer_six": rim[:-1], "interior": ["p", "h", "R", "n"]},
            "a_u2_absent": {"n_degree_lower_bound": 6, "seven_rim_induced": True},
        },
        "necessary_complete_old_rim_contact_profiles": profiles,
        "expanded_c11_rim": c11,
        "possible_original_expanded_rim_chords": [list(e) for e in chords],
        "noncrossing_joint_profiles": joint,
        "crossing_joint_profiles_rejected": rejected,
        "scope": {
            "same_original_graph": True,
            "private_vertices_retained": True,
            "all_remaining_profiles_source_realized": False,
            "source_excluded": False,
            "strictly_smaller_bad_constructed": False,
            "J1_J2_closed": False,
            "paper_pocket_jordan_arguments_mechanized": False,
        },
        "status": "structural dichotomy only; OPEN",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    actual = build()
    if args.write:
        with args.certificate.open("x") as output:
            output.write(json.dumps(actual, indent=2, sort_keys=True) + "\n")
    assert json.loads(args.certificate.read_text()) == actual, "certificate mismatch"
    print(json.dumps({
        "pass": True,
        "original_chords_checked": len(actual["pocket_chord_records"]),
        "original_chords_excluded": 13,
        "remaining_original_chord": "a-u2 iff n=5",
        "u1_contact_profiles": len(actual["necessary_complete_old_rim_contact_profiles"]["u1"]),
        "u2_contact_profiles": len(actual["necessary_complete_old_rim_contact_profiles"]["u2"]),
        "noncrossing_joint_profiles": len(actual["noncrossing_joint_profiles"]),
        "crossing_joint_profiles_rejected": len(actual["crossing_joint_profiles_rejected"]),
        "source_excluded": False,
        "smaller_bad_constructed": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
