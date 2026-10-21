#!/usr/bin/env python3
"""Exact original-pocket replay on the frozen 112 W7 contact profiles.

The C13 cells are topology placeholders, not assertions that the unknown
source has no vertices there.  Only named vertices forced inside a short
cycle are used.  No source graphs or colourings are generated.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
UP = ROOT / "audits/2026-10-20-r6-941-j1-five-edge-417732f"
CAP_PROOF = UP / ("frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/"
    "frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/"
    "frozen/audits/2026-10-19-r6-941-chains-13dc5ff/B/PROOF.md")
ORIGINAL_OUTER = ("x", "y", "a", "b", "c")
OLD_RIM = ("a", "n", "R", "L", "q", "c", "s", "v", "w", "t")
C13 = ("a", "n", "u4", "u3", "u2", "u1", "L", "q", "c", "s", "v", "w", "t")
BASE_FACES = tuple(tuple(s) for s in (
    "bap", "bpq", "bqc", "pan", "pnh", "phq", "hnR", "hRL", "hLq",
    "ayt", "yrt", "yxr", "xrs", "xsc", "rtw", "rwv", "rvs",
)) + (("R", "n", "u4"), ("R", "u4", "u3"), ("R", "u3", "u2"),
      ("R", "u2", "u1"), ("R", "u1", "L"))


def require(test, message):
    if not test:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def ring_edges(rim):
    return tuple(edge(rim[i], rim[(i + 1) % len(rim)]) for i in range(len(rim)))


BASE_EDGES = {e for f in BASE_FACES for e in ring_edges(f)}


def profile_chords(profile):
    return sorted({edge(u, z) for u, contacts in profile.items() for z in contacts} - BASE_EDGES)


def topology_cells(profile):
    """Split one C13 placeholder by the given actual noncrossing chords."""
    regions = [list(C13)]
    for a, b in profile_chords(profile):
        candidates = [(i, f) for i, f in enumerate(regions) if a in f and b in f]
        require(len(candidates) == 1, "chord is not inside one unsplit C13 cell")
        cell_id, cell = candidates[0]
        i, j = sorted((cell.index(a), cell.index(b)))
        require(1 < j - i < len(cell) - 1, "attempt to split a boundary edge")
        regions.pop(cell_id)
        regions += [cell[i:j + 1], cell[j:] + cell[:i + 1]]
    cells = [list(f) for f in BASE_FACES] + regions
    incidence = defaultdict(list)
    graph = defaultdict(set)
    links = defaultdict(lambda: defaultdict(set))
    for cell_id, f in enumerate(cells):
        require(len(set(f)) == len(f) >= 3, "non-simple topology cell")
        for e in ring_edges(f):
            incidence[e].append(cell_id)
            a, b = e
            graph[a].add(b)
            graph[b].add(a)
        for i, vertex in enumerate(f):
            a, b = f[i - 1], f[(i + 1) % len(f)]
            links[vertex][a].add(b)
            links[vertex][b].add(a)
    require(set(map(len, incidence.values())) <= {1, 2}, "edge incidence is not a disk")
    require({e for e, ids in incidence.items() if len(ids) == 1} == set(ring_edges(ORIGINAL_OUTER)),
            "original ordered C5 was changed")
    require(len(graph) - len(incidence) + len(cells) == 1, "wrong disk Euler value")
    for vertex, link in links.items():
        todo = [next(iter(link))]
        seen = set(todo)
        while todo:
            for neighbor in link[todo.pop()] - seen:
                seen.add(neighbor)
                todo.append(neighbor)
        require(len(seen) == len(link), "disconnected vertex link")
        degrees = sorted(len(n) for n in link.values())
        expected = [1, 1] + [2] * (len(link) - 2) if vertex in ORIGINAL_OUTER else [2] * len(link)
        require(degrees == expected, "vertex link is not the original path/cycle")
    return cells, dict(graph), dict(incidence)


def short_cycles(graph):
    cycles = set()
    for start in sorted(graph):
        def visit(path):
            for vertex in sorted(graph[path[-1]]):
                if vertex == start and 3 <= len(path) <= 5:
                    cycles.add(min(tuple(path), (start,) + tuple(reversed(path[1:]))))
                elif vertex > start and vertex not in path and len(path) < 5:
                    visit(path + [vertex])
        visit([start])
    return sorted(cycles)


def bounded_side(cells, incidence, cycle):
    cut = set(ring_edges(cycle))
    outside = len(cells)
    dual = {i: set() for i in range(outside + 1)}
    for e, cell_ids in incidence.items():
        if e in cut:
            continue
        ids = cell_ids if len(cell_ids) == 2 else cell_ids + [outside]
        a, b = ids
        dual[a].add(b)
        dual[b].add(a)
    todo = [outside]
    reached = set(todo)
    while todo:
        for neighbor in dual[todo.pop()] - reached:
            reached.add(neighbor)
            todo.append(neighbor)
    enclosed_cells = sorted(set(range(outside)) - reached)
    require(bool(enclosed_cells), "simple cycle has no enclosed topology cell")
    forced = sorted(set().union(*(set(cells[i]) for i in enclosed_cells)) - set(cycle))
    return forced, enclosed_cells


def inspect_profile(profile):
    cells, graph, incidence = topology_cells(profile)
    contradictions, forced_centers = [], []
    for cycle in short_cycles(graph):
        if len(cycle) == 5 and set(cycle) == set(ORIGINAL_OUTER):
            continue  # Original B is expressly exempt from the pocket theorem.
        inside, cell_ids = bounded_side(cells, incidence, cycle)
        record = {"cycle": list(cycle), "forced_original_interior": inside,
                  "bounded_topology_cells": cell_ids}
        if len(cycle) <= 4 and inside:
            contradictions.append(record | {"reason": f"C{len(cycle)}_nonempty"})
        elif len(cycle) == 5 and len(inside) >= 2:
            contradictions.append(record | {"reason": "C5_at_least_two"})
        elif len(cycle) == 5 and len(inside) == 1:
            center = inside[0]
            extra = sorted(graph[center] - set(cycle))
            missing = sorted(set(cycle) - graph[center])
            absent = [z for z in missing if (center in profile and z in OLD_RIM)
                      or (z in profile and center in OLD_RIM)]
            forced_centers.append(record | {"center": center,
                "forced_complete_degree": 5, "forced_complete_neighbors": sorted(cycle),
                "missing_known_spokes": missing})
            if extra:
                contradictions.append(record | {"reason": "C5_center_extra_neighbor",
                                                "center": center, "extra_original_neighbors": extra})
            if absent:
                contradictions.append(record | {"reason": "C5_center_absent_spoke",
                                                "center": center, "absent_original_spokes": absent})
    return {"profile": profile, "chords": [list(e) for e in profile_chords(profile)],
            "topology_cells": cells, "contradictions": contradictions,
            "forced_degree5_centers": forced_centers}


def rule_records(profile):
    """Independent short list of the new paper lemmas, without dual search."""
    forbidden, forced = [], []
    for z in ("s", "v", "w"):
        contacts = [i for i in range(1, 5) if z in profile[f"u{i}"]]
        for i in contacts:
            for j in contacts:
                if j >= i + 2:
                    forbidden.append({"rule": "nonconsecutive_wheel_contacts", "external_vertex": z,
                                      "contacts": [f"u{i}", f"u{j}"]})
    for name, required_edges, center, neighbors in (
        ("left_middle_W5", (("u2", "s"), ("u4", "v")), "u3", ("R", "u2", "s", "v", "u4")),
        ("right_middle_W5", (("u1", "v"), ("u3", "w")), "u2", ("R", "u1", "v", "w", "u3")),
        ("opposite_cap_W5", (("u2", "s"), ("u3", "w")), "v", ("r", "s", "u2", "u3", "w")),
    ):
        if not all(z in profile[u] for u, z in required_edges):
            continue
        missing = [z for z in neighbors if
            (center in profile and z in OLD_RIM and z not in profile[center]) or
            (z in profile and center in OLD_RIM and center not in profile[z])]
        row = {"rule": name, "center": center, "complete_degree": 5,
               "complete_neighbors": sorted(neighbors)}
        forced.append(row)
        if missing:
            forbidden.append(row | {"missing_required_contacts": missing})
    return forbidden, forced


def target_records(profile):
    records = {}
    for target, v, w in (("44459", 0, 1), ("44466", 1, 0)):
        colours = dict(zip(C13, (0, 1, 2, 1, 2, 1, 2, 3, 1, 2, v, w, 2))) | {"R": 3}
        improper = sorted(edge(u, z) for u, contacts in profile.items() for z in contacts
                          if colours[u] == colours[z])
        records[target] = {"compatible": not improper,
                           "same_colour_original_edges": [list(e) for e in improper]}
    return records


def guard_records():
    wheel_rim = ("n", "h", "L", "u1", "u2", "u3", "u4")
    nonconsecutive = []
    for i in range(7):
        for j in range(i + 1, 7):
            if j - i in (1, 6):
                continue
            arcs = [list(wheel_rim[i + 1:j]), list(wheel_rim[j + 1:] + wheel_rim[:i])]
            require(all(arcs), "nonconsecutive wheel pair has an empty open arc")
            nonconsecutive.append({"pair": [wheel_rim[i], wheel_rim[j]], "two_open_arcs": arcs})
    chain = ("n", "u4", "u3", "u2", "u1", "L")
    distinct_guards = []
    rim_non_edges = {edge(*r["pair"]) for r in nonconsecutive}
    for i in range(5):
        for j in range(i + 1, 5):
            endpoints = sorted(set(chain[i:i + 2]) | set(chain[j:j + 2]))
            nonedge = next(edge(a, b) for a in endpoints for b in endpoints if edge(a, b) in rim_non_edges)
            distinct_guards.append({"path_edges": [list(chain[i:i + 2]), list(chain[j:j + 2])],
                                    "nonconsecutive_endpoints": list(nonedge)})
    return {"wheel_rim": list(wheel_rim), "nonconsecutive_rim_pairs": nonconsecutive,
            "five_exterior_face_centers_pairwise_distinct": distinct_guards,
            "chord_free_C13_forces_five_private_F13_vertices": True}


def build():
    original = json.loads((UP / "geometry/certificate.json").read_text())
    profiles = original["noncrossing_joint_contact_profiles"]
    results = []
    for i, profile in enumerate(profiles):
        full = inspect_profile(profile)
        simple_bad, simple_forced = rule_records(profile)
        require(bool(full["contradictions"]) == bool(simple_bad), "paper rules and complete pocket replay disagree")
        results.append(full | {"original_profile_id": i, "paper_rule_contradictions": simple_bad,
            "paper_rule_forced_centers": simple_forced, "target_compatibility": target_records(profile)})
    live = [r for r in results if not r["contradictions"]]
    target_summary = {}
    for target in ("44459", "44466"):
        before = [r for r in results if r["target_compatibility"][target]["compatible"]]
        after = [r for r in live if r["target_compatibility"][target]["compatible"]]
        target_summary[target] = {"compatible_before": len(before), "compatible_after": len(after),
            "surviving_original_profile_ids": [r["original_profile_id"] for r in after],
            "surviving_n5": sum("a" in r["profile"]["u4"] for r in after)}
    union = [r["original_profile_id"] for r in live if
             any(t["compatible"] for t in r["target_compatibility"].values())]
    paths = (UP / "SOURCE_CONTRACT.md", UP / "geometry/PROOF.md", UP / "geometry/certificate.json", CAP_PROOF)
    custody = {str(p.relative_to(ROOT)): {"bytes": p.stat().st_size,
                                         "sha256": sha256(p.read_bytes()).hexdigest()} for p in paths}
    require(custody[str(CAP_PROOF.relative_to(ROOT))]["sha256"] ==
            original["input_sha256"][str(CAP_PROOF.relative_to(UP))],
            "frozen original cap proof differs from pinned upstream geometry certificate")
    parent_base = json.loads((HERE.parent / "BASE.json").read_text())
    for item in parent_base["inputs"]:
        if item["path"] in custody:
            require(custody[item["path"]] == {"bytes": item["bytes"], "sha256": item["sha256"]},
                    "parent frozen input bytes/SHA differ")
    return {"scope": "necessary original-source geometry only; no source existence/exclusion",
        "original_outer": list(ORIGINAL_OUTER), "C13": list(C13),
        "original_known_triangle_faces": [list(f) for f in BASE_FACES],
        "profiles": results, "surviving_original_profile_ids": [r["original_profile_id"] for r in live],
        "target_compatibility": target_summary, "target_union_surviving_original_profile_ids": union,
        "guard_lemma": guard_records(),
        "counts": {"input": len(results), "excluded": len(results) - len(live),
            "surviving": len(live), "surviving_n5": sum("a" in r["profile"]["u4"] for r in live),
            "target_union_surviving": len(union),
            "reasons_by_profile": dict(sorted(Counter(reason for r in results for reason in
                {c["reason"] for c in r["contradictions"]}).items()))},
        "source_excluded": False, "source_realized": False, "smaller_bad": False,
        "inputs": custody}


def controls(result):
    rows = result["profiles"]
    require(not rows[0]["contradictions"], "chord-free necessary profile was incorrectly excluded")
    require(all(t["compatible"] for t in rows[0]["target_compatibility"].values()),
            "chord-free profile must allow either witness rim")
    for center, profile_id in (("u3", 35), ("v", 58), ("u2", 94)):
        row = rows[profile_id]
        require(not row["contradictions"], "legal W5 center alternative was incorrectly discarded")
        require(any(r["center"] == center for r in row["paper_rule_forced_centers"]),
                "W5 complete-star control is absent")
    cells, _, incidence = topology_cells(rows[0]["profile"])
    inside, _ = bounded_side(cells, incidence, ORIGINAL_OUTER)
    require(len(inside) == 15, "original B exception control changed")
    row = rows[70]
    require(any(r["cycle"] == ["R", "u1", "v", "u4"] and
                r["forced_original_interior"] == ["u2", "u3"] for r in row["contradictions"]),
            "nonempty original C4 control is absent")
    mutated = deepcopy(result)
    mutated["surviving_original_profile_ids"].append(70)
    try:
        verify_certificate(mutated, result)
    except ValueError:
        pass
    else:
        raise ValueError("reintroducing a C4-forbidden profile was accepted")
    mutated = deepcopy(result)
    mutated["profiles"][0]["target_compatibility"]["44466"]["compatible"] = False
    try:
        verify_certificate(mutated, result)
    except ValueError:
        pass
    else:
        raise ValueError("mixing the two literal witness rims was accepted")
    return {"chord_free_survives_both_witnesses": True, "original_B_exempt": True,
            "three_W5_center_alternatives_retained": True, "C4_bounded_side_checked": True,
            "reintroduced_forbidden_profile_rejected": True, "mixed_literal_rim_rejected": True}


def verify_certificate(candidate, expected):
    # JSON comparison preserves the type distinction between integers/bools.
    require(json.dumps(candidate, sort_keys=True, separators=(",", ":")) ==
            json.dumps(expected, sort_keys=True, separators=(",", ":")), "geometry certificate differs")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    result = build()
    target = HERE / "certificate.json"
    if args.build:
        with target.open("x") as out:
            json.dump(result, out, indent=2, sort_keys=True)
            out.write("\n")
    else:
        verify_certificate(json.loads(target.read_text()), result)
    if args.controls:
        controls(result)
    print(json.dumps(result["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
