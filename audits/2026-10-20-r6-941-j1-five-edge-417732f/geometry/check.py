#!/usr/bin/env python3
"""Finite replay for the strict original C7 only-R subtype (stdlib only)."""

from __future__ import annotations

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
UP = AUDIT / "frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c"
LAST = UP / "frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d"
CHAINS = LAST / "frozen/audits/2026-10-19-r6-941-chains-13dc5ff"


def edge(x, y):
    return tuple(sorted((x, y)))


def graph(faces):
    out = {}
    for f in faces:
        for x, y in combinations(f, 2):
            out.setdefault(x, set()).add(y)
            out.setdefault(y, set()).add(x)
    return out


def boundary(faces):
    counts = Counter(edge(f[i], f[(i + 1) % 3]) for f in faces for i in range(3))
    assert set(counts.values()) <= {1, 2}
    return {e for e, n in counts.items() if n == 1}


def ring_edges(rim):
    return {edge(x, y) for x, y in zip(rim, rim[1:] + rim[:1])}


def separated_faces(faces, path):
    cut = {edge(x, y) for x, y in zip(path, path[1:])}
    dual = {i: set() for i in range(len(faces))}
    for i, j in combinations(range(len(faces)), 2):
        common = set(faces[i]) & set(faces[j])
        if len(common) == 2 and tuple(sorted(common)) not in cut:
            dual[i].add(j)
            dual[j].add(i)
    anchor = [i for i, f in enumerate(faces) if {"a", "b"} <= set(f)]
    assert len(anchor) == 1
    seen, todo = set(anchor), list(anchor)
    while todo:
        for j in dual[todo.pop()] - seen:
            seen.add(j)
            todo.append(j)
    other = sorted(set(dual) - seen)
    assert other
    return other


def crosses(e, f, rim):
    if set(e) & set(f):
        return False
    i, j = sorted(rim.index(x) for x in e)
    k, l = sorted(rim.index(x) for x in f)
    return i < k < j < l or k < i < l < j


def short_cycles(g):
    cycles = set()
    for start in sorted(g):
        def visit(path):
            for v in g[path[-1]]:
                if v == start and 3 <= len(path) <= 5:
                    rev = (start,) + tuple(reversed(path[1:]))
                    cycles.add(min(tuple(path), rev))
                elif v > start and v not in path and len(path) < 5:
                    visit(path + [v])
        visit([start])
    return sorted(cycles)


def cycle_interior(faces, cycle):
    cut = ring_edges(list(cycle))
    rim = boundary(faces)
    outside = len(faces)
    dual = {i: set() for i in range(outside + 1)}
    for i, f in enumerate(faces):
        for e in (edge(f[k], f[(k + 1) % 3]) for k in range(3)):
            if e in rim and e not in cut:
                dual[i].add(outside)
                dual[outside].add(i)
    for i, j in combinations(range(len(faces)), 2):
        common = set(faces[i]) & set(faces[j])
        if len(common) == 2 and tuple(sorted(common)) not in cut:
            dual[i].add(j)
            dual[j].add(i)
    seen, todo = {outside}, [outside]
    while todo:
        for j in dual[todo.pop()] - seen:
            seen.add(j)
            todo.append(j)
    enclosed = set().union(*(set(faces[i]) for i in range(len(faces)) if i not in seen))
    return sorted(enclosed - set(cycle))


def palette_distance(g, colours, start, finish):
    q = deque([(start, 0)])
    seen = {start}
    while q:
        v, d = q.popleft()
        if v == finish:
            return d
        for w in g[v] - seen:
            if colours[w] in {1, 2}:
                seen.add(w)
                q.append((w, d + 1))
    return None


def local_control(faces, colours):
    g = graph(faces)
    assert all(colours[x] != colours[y] for x in g for y in g[x])
    records = []
    for cycle in short_cycles(g):
        inside = cycle_interior(faces, cycle)
        assert not inside if len(cycle) <= 4 else (
            not inside or len(inside) == 1 and len(g[inside[0]]) == 5
        )
        records.append({"cycle": list(cycle), "bounded_interior": inside})
    return {
        "faces": faces,
        "boundary_edges": [list(e) for e in sorted(boundary(faces))],
        "colours": colours,
        "R_degree": len(g["R"]),
        "interior_vertices": sorted(set(g) - {"n", "h", "L", "u1", "u2", "u3", "u4"}),
        "actual_12_n_L_distance": palette_distance(g, colours, "n", "L"),
        "all_C3_C4_C5_local_pocket_checks": records,
        "full_J1_source_realized": False,
    }


def build():
    sources = [
        UP / "SOURCE_CONTRACT.md", UP / "geometry/PROOF.md",
        UP / "geometry/certificate.json", CHAINS / "B/PROOF.md",
        CHAINS / "B/certificate.json",
        AUDIT / "frozen/audits/2026-10-20-r6-941-j1-c11-1148ce0/REPORT.md",
    ]
    hashes = {str(p.relative_to(AUDIT)): sha256(p.read_bytes()).hexdigest() for p in sources}
    frozen_manifest = {"frozen/" + r["path"]: r["sha256"] for r in json.loads((AUDIT / "INPUTS.json").read_text())["inputs"]}
    assert all(frozen_manifest[p] == h for p, h in hashes.items())
    rim = ["a", "b", "q", "L", "u1", "u2", "u3", "u4", "n"]
    cap = [list(f) for f in [("a", "b", "p"), ("b", "p", "q"), ("p", "q", "h"), ("p", "h", "n"), ("p", "n", "a"), ("h", "q", "L"), ("h", "L", "R"), ("h", "R", "n")]]
    chain = ["n", "u4", "u3", "u2", "u1", "L"]
    faces = cap + [["R", x, y] for x, y in zip(chain, chain[1:])]
    assert boundary(faces) == ring_edges(rim)
    g = graph(faces)
    assert len(g["p"]) == len(g["h"]) == 5 and len(g["R"]) == 7
    assert len(faces) == 2 * 3 + len(rim) - 2 == 13

    paths = [["a", "p", "q"], ["a", "p", "h", "L"]]
    paths += [["a", "p", "h", "R", u] for u in ["u1", "u2", "u3", "u4"]]
    paths += [["b", "p", "h", "L"]]
    paths += [["b", "p", "h", "R", u] for u in ["u1", "u2", "u3", "u4"]]
    paths += [["b", "p", "n"]]
    paths += [["q", "h", "R", u] for u in ["u1", "u2", "u3", "u4"]]
    paths += [["q", "p", "n"]]
    paths += [["L", "R", u] for u in ["u2", "u3", "u4"]]
    paths += [["L", "h", "n"]]
    paths += [["u1", "R", "u3"], ["u1", "R", "u4"], ["u2", "R", "u4"]]
    paths += [[u, "R", "n"] for u in ["u1", "u2", "u3"]]
    chord_rows = []
    for path in paths:
        assert all(y in g[x] for x, y in zip(path, path[1:]))
        other = separated_faces(faces, path)
        inside = sorted(set().union(*(set(faces[i]) for i in other)) - set(path))
        length = len(path)
        excluded = (length <= 4 and bool(inside)) or (length == 5 and len(inside) >= 2)
        chord_rows.append({"chord": [path[0], path[-1]], "original_path": path, "cycle_length": length, "enclosed_original_vertices_at_least": inside, "original_patch_faces_separated_from_ab": other, "excluded_by_pocket_theorem": excluded})
    all_diagonals = {edge(rim[i], rim[j]) for i, j in combinations(range(len(rim)), 2) if j - i not in (1, len(rim) - 1)}
    assert {edge(*r["chord"]) for r in chord_rows} == all_diagonals
    assert [r["chord"] for r in chord_rows if not r["excluded_by_pocket_theorem"]] == [["a", "u4"]]

    envelope = json.loads((CHAINS / "B/certificate.json").read_text())
    allowed = [set(r["contacts"]) for r in envelope["complete_contact_subsets"] if r["necessary_allowed"]]
    req = {"u1": {"R", "L"}, "u2": {"R"}, "u3": {"R"}, "u4": {"n", "R"}}
    bans = {"u1": {"a", "n", "q", "s", "t"}, "u2": {"a", "n", "L", "q", "t"}, "u3": {"a", "n", "L", "q", "t"}, "u4": {"q", "L", "t"}}
    profiles = {u: [sorted(S) for S in allowed if req[u] <= S and not S & bans[u]] for u in req}
    c13 = ["a", "n", "u4", "u3", "u2", "u1", "L", "q", "c", "s", "v", "w", "t"]
    extras = sorted({edge(u, v) for u in req for S in profiles[u] for v in set(S) - req[u]})
    joint, rejected = [], []
    for selection in product(*(profiles[u] for u in req)):
        chosen = dict(zip(req, selection))
        chords = [edge(u, v) for u in req for v in set(chosen[u]) - req[u]]
        crossing = any(crosses(e, f, c13) for e, f in combinations(chords, 2))
        (rejected if crossing else joint).append(chosen)

    c7 = ["n", "h", "L", "u1", "u2", "u3", "u4"]
    wheel = [["R", x, y] for x, y in zip(c7, c7[1:] + c7[:1])]
    colours = {"n": 1, "h": 0, "L": 2, "u1": 1, "u2": 2, "u3": 1, "u4": 2, "R": 3}
    two = [["R", "n", "h"], ["R", "h", "L"], ["R", "L", "u1"], ["R", "u1", "Z"], ["R", "Z", "n"], ["Z", "u1", "u2"], ["Z", "u2", "u3"], ["Z", "u3", "u4"], ["Z", "u4", "n"]]
    controls = {"only_R_W7": local_control(wheel, colours), "two_interior_R5_Z6": local_control(two, colours | {"Z": 0})}
    assert all(r["actual_12_n_L_distance"] == 5 for r in controls.values())
    assert len(graph(two)["Z"]) == 6
    return {
        "base": "417732fc5ef0a012829fd6712333b1c906128d3a",
        "input_sha256": hashes,
        "strict_hypothesis": "the bounded original C7 pocket has exactly one interior vertex R",
        "original_C7_rim": c7,
        "original_patch": {"rim": rim, "interior": ["p", "h", "R"], "faces": faces, "full_R_rotation": ["n", "h", "L", "u1", "u2", "u3", "u4"], "R_degree": 7},
        "all_27_original_exterior_chord_records": chord_rows,
        "possible_original_nine_rim_chords": [["a", "u4"]],
        "degree_split": {"a_u4_present_iff_n_degree_5": True, "n_degree_5_full_star": ["a", "p", "h", "R", "u4"], "n_degree_at_least_6_implies_nine_rim_induced": True},
        "complete_old_rim_contact_profiles": profiles,
        "expanded_core": {"deleted_original_vertices": ["b", "p", "h", "R", "x", "y", "r"], "rim": c13, "potential_original_chords": [list(e) for e in extras], "induced_unconditionally": False, "all_other_original_vertices_and_edges_retained": True},
        "all_720_contact_selections": len(joint) + len(rejected),
        "noncrossing_joint_contact_profiles": joint,
        "crossing_contact_selection_count": len(rejected),
        "local_true_disk_controls": controls,
        "scope": {"general_five_edge_forces_R_degree_5": False, "general_five_edge_exhausted_by_only_R": False, "necessary_profiles_source_realized": False, "same_original_graph": True, "all_private_vertices_retained": True, "source_excluded_by_this_checker": False, "strictly_smaller_bad_constructed": False, "new_Lean_theorem": False},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    actual = build()
    if args.write:
        with args.certificate.open("x") as out:
            json.dump(actual, out, indent=2, sort_keys=True)
            out.write("\n")
    assert json.loads(args.certificate.read_text()) == actual, "certificate mismatch"
    print(json.dumps({"pass": True, "original_exterior_chords_checked": 27, "original_exterior_chords_excluded": 26, "contact_profile_counts": {u: len(v) for u, v in actual["complete_old_rim_contact_profiles"].items()}, "joint_contact_profiles": len(actual["noncrossing_joint_contact_profiles"]), "potential_C13_chords": len(actual["expanded_core"]["potential_original_chords"]), "local_true_disks_checked": 2, "source_excluded_by_geometry": False}, sort_keys=True))


if __name__ == "__main__":
    main()
