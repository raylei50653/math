#!/usr/bin/env python3
"""Same-source bridge, separator and full-link replay for eight u3v profiles."""

from __future__ import annotations

import argparse
from copy import deepcopy
import gzip
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AUDIT = HERE.parent
OLD = "audits/2026-10-21-w7-structural-30f2d19"
COUNT = "audits/2026-10-20-r6-941-j1-five-edge-417732f/counting"
EXPECTED = [10, 11, 12, 13, 14, 15, 43, 44]
C13 = ("a", "n", "u4", "u3", "u2", "u1", "L", "q", "c", "s", "v", "w", "t")
C8 = ("u3", "u2", "u1", "L", "q", "c", "s", "v")
C7 = ("v", "w", "t", "a", "n", "u4", "u3")
LEFT = tuple(C13.index(x) for x in C8)
RIGHT = tuple(C13.index(x) for x in C7)
CUT = (C13.index("u3"), C13.index("v"))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(relative, manifest, hashes):
    raw = (ROOT / relative).read_bytes()
    entry = manifest[relative]
    require(len(raw) == entry["bytes"] and sha256(raw).hexdigest() == entry["sha256"],
            "frozen input drift: " + relative)
    hashes[relative] = {"bytes": len(raw), "sha256": entry["sha256"]}
    return json.loads(gzip.decompress(raw) if relative.endswith(".gz") else raw)


def decode(code):
    return tuple((code >> (2 * (12 - i))) & 3 for i in range(13))


def splice(left, right):
    require(all(left[i] == right[i] for i in CUT), "literal separator colours differ")
    return tuple(left[i] if i in LEFT else right[i] for i in range(13))


def same_cut_rows(column):
    rows = set()
    for encoded in column:
        original = decode(encoded)
        for perm in permutations(range(4)):
            row = tuple(perm[x] for x in original)
            if tuple(row[i] for i in CUT) == (1, 0):
                rows.add(row)
    return sorted(rows)


def rectangle_record(rows):
    left = {tuple(row[i] for i in LEFT) for row in rows}
    right = {tuple(row[i] for i in RIGHT) for row in rows}
    actual = set(rows)
    require(len(rows) == len(left) * len(right), "same-cut support is not a rectangle")
    require(all(splice(a, b) in actual for a in rows for b in rows), "same-source splice escapes support")
    return {"literal_cut_colours": [1, 0], "C8_projections": len(left),
            "C7_projections": len(right), "full_literal_rims": len(rows),
            "rows": [list(row) for row in rows], "all_splices_already_present": True}


def compute():
    manifest = {r["path"]: r for r in json.loads((AUDIT / "BASE.json").read_text())["inputs"]}
    hashes = {}
    geometry = read(OLD + "/geometry/certificate.json", manifest, hashes)
    caps = read(COUNT + "/caps.json.gz", manifest, hashes)
    orbits = read(COUNT + "/orbits.json.gz", manifest, hashes)
    require(tuple(caps["ordered_rim"]) == C13, "original ordered C13 changed")
    union = set(geometry["target_union_surviving_original_profile_ids"])
    profiles = [r for r in geometry["profiles"] if r["original_profile_id"] in union
                and "v" in r["profile"]["u3"]]
    require([r["original_profile_id"] for r in profiles] == EXPECTED, "the eight full profiles changed")
    records = []
    for r in profiles:
        p = r["profile"]
        # The exterior part of the original full u3 link is u2,[s],v,u4.
        outside = ["u2"] + (["s"] if "s" in p["u3"] else []) + ["v", "u4"]
        gap_pairs = []
        for a, b in zip(outside, outside[1:]):
            present = b in p[a] if a.startswith("u") else a in p[b] if b.startswith("u") else {a, b} == {"s", "v"}
            if not present:
                gap_pairs.append([a, b])
        known = ["R"] + outside
        ears = []
        if "a" in p["u4"]:
            ears.append({"side": "C7", "original_triangle_face": ["a", "n", "u4"]})
        if "v" in p["u4"]:
            ears.append({"side": "C7", "original_triangle_face": ["u3", "u4", "v"]})
        if "s" in p["u3"]:
            ears.append({"side": "C8", "original_triangle_face": ["u3", "s", "v"]})
        if "v" in p["u2"]:
            ears.append({"side": "C8", "original_triangle_face": ["u3", "u2", "v"]})
        records.append({"original_profile_id": r["original_profile_id"], "complete_profile": p,
            "all_original_chords": r["chords"], "known_original_u3_link_cycle": known,
            "nonedge_gaps_requiring_distinct_private_neighbors": gap_pairs,
            "u3_degree_lower_bound": len(known) + len(gap_pairs), "original_triangle_ears": ears})
    require([r["u3_degree_lower_bound"] for r in records] == [6, 6, 5, 7, 7, 6, 5, 5],
            "full-link private-neighbor degree bounds changed")
    equal = [s for s, rim in enumerate(caps["states"]) if rim[CUT[0]] == rim[CUT[1]]]
    original_live = set(orbits["live"])
    initial = [s for s in equal if s in original_live]
    require(44466 in initial and 44459 not in equal, "literal source target distinction changed")
    columns = {j: same_cut_rows(orbits["columns"][j]) for j in (66582, 67755)}
    rectangles = {str(j): rectangle_record(rows) for j, rows in columns.items()}
    rectangles["union"] = rectangle_record(sorted(set().union(*(set(rows) for rows in columns.values()))))
    wrong = tuple((1 - x) if x in (0, 1) else x for x in columns[66582][0])
    try:
        splice(columns[66582][0], wrong)
    except ValueError:
        pass
    else:
        raise ValueError("splicing mismatched literal separator colours was accepted")
    require([r["full_literal_rims"] for r in rectangles.values()] == [32, 32, 48],
            "two-column fixed-cut rectangle control changed")
    return {"scope": "same-original source bridge; no geometric source exclusion claimed alone",
        "inputs": hashes, "fixed_profile_ids": EXPECTED, "profiles": records,
        "original_ordered_C13": list(C13), "C8_original_rim": list(C8), "C7_original_rim": list(C7),
        "shared_original_edge": ["u3", "v"],
        "initial_same_colour_zero_state_ids": initial,
        "same_colour_zero_all_C13_states": len(equal), "same_colour_zero_original_live_states": len(initial),
        "literal_targets": {"44459": {"u3": 1, "v": 0, "edge_proper": True},
                            "44466": {"u3": 1, "v": 1, "full_fibre_zero": True}},
        "same_cut_rectangles": rectangles,
        "no_go_control": "two target columns and their union already rectangle-closed; no exclusion from these splices",
        "mismatched_literal_cut_rejected": True,
        "source_excluded_by_geometry_alone": False, "new_graph_enumeration": False,
        "LP_run": False, "smaller_bad": False, "new_Lean": False}


def verify(candidate, expected):
    require(json.dumps(candidate, sort_keys=True, separators=(",", ":")) ==
            json.dumps(expected, sort_keys=True, separators=(",", ":")), "source bridge certificate differs")


def controls(result):
    for kind in ("omit_literal_zero", "omit_private_gap", "promote_geometry_to_exclusion"):
        bad = deepcopy(result)
        if kind == "omit_literal_zero":
            bad["initial_same_colour_zero_state_ids"].remove(44466)
        elif kind == "omit_private_gap":
            bad["profiles"][3]["u3_degree_lower_bound"] = 5
        else:
            bad["source_excluded_by_geometry_alone"] = True
        try:
            verify(bad, result)
        except ValueError:
            pass
        else:
            raise ValueError("malformed source bridge certificate accepted: " + kind)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    result = compute()
    path = HERE / "certificate.json"
    if args.build:
        with path.open("x") as f:
            json.dump(result, f, indent=2, sort_keys=True)
            f.write("\n")
    else:
        verify(json.loads(path.read_text()), result)
    controls(result)
    print(json.dumps({"profile_ids": EXPECTED,
        "u3_degree_lower_bounds": [r["u3_degree_lower_bound"] for r in result["profiles"]],
        "same_colour_zero_original_live_states": result["same_colour_zero_original_live_states"],
        "fixed_cut_rectangle_sizes": [r["full_literal_rims"] for r in result["same_cut_rectangles"].values()]}, sort_keys=True))


if __name__ == "__main__":
    main()
