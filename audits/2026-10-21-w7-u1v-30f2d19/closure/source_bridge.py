#!/usr/bin/env python3
"""Independent original-edge/profile and unaugmented-incidence bridge for u1v."""

from __future__ import annotations

import argparse
from copy import deepcopy
import gzip
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AUDIT = HERE.parent
SOURCE = "audits/2026-10-20-r6-941-j1-five-edge-417732f"
OLD = "audits/2026-10-21-w7-structural-30f2d19"
EXPECTED = [68, 69, 78, 79, 88, 89, 92, 93]
OLD_U3V = [10, 11, 12, 13, 14, 15, 43, 44]
RIM = ["a", "n", "u4", "u3", "u2", "u1", "L", "q", "c", "s", "v", "w", "t"]
STATES = {
    44459: [0, 1, 2, 1, 2, 1, 2, 3, 1, 2, 0, 1, 2],
    44111: [0, 1, 2, 1, 2, 1, 2, 0, 2, 1, 3, 1, 2],
    44127: [0, 1, 2, 1, 2, 1, 2, 0, 2, 3, 1, 3, 2],
    44466: [0, 1, 2, 1, 2, 1, 2, 3, 1, 2, 1, 0, 2],
}
INCIDENCE = {
    12302027: [306985],
    12301211: [306972, 306983, 306985, 307044, 307049],
    10064313: [147448, 147449, 167802, 226130, 231666],
    10064365: [147448, 147449, 167802, 226130, 231666],
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load():
    manifest = {r["path"]: r for r in json.loads((AUDIT / "BASE.json").read_text())["inputs"]}
    paths = [SOURCE + "/SOURCE_CONTRACT.md", SOURCE + "/counting/PROOF.md",
             SOURCE + "/counting/caps.json.gz", SOURCE + "/counting/orbits.json.gz",
             OLD + "/geometry/certificate.json", OLD + "/review/profile_orbits.json",
             "audits/2026-10-21-w7-u3v-30f2d19/REPORT.md",
             "audits/2026-10-21-w7-u3v-30f2d19/transport/PROOF.md"]
    hashes, data = {}, {}
    for name in paths:
        raw = (ROOT / name).read_bytes()
        entry = manifest[name]
        require(len(raw) == entry["bytes"] and sha256(raw).hexdigest() == entry["sha256"],
                "frozen source input drift: " + name)
        hashes[name] = {"bytes": len(raw), "sha256": entry["sha256"]}
        if name.endswith(".json.gz"):
            data[name] = json.loads(gzip.decompress(raw))
        elif name.endswith(".json"):
            data[name] = json.loads(raw)
    return hashes, data


def compute():
    hashes, data = load()
    caps = data[SOURCE + "/counting/caps.json.gz"]
    orbit = data[SOURCE + "/counting/orbits.json.gz"]
    geometry = data[OLD + "/geometry/certificate.json"]
    profile_orbits = data[OLD + "/review/profile_orbits.json"]
    require(caps["ordered_rim"] == RIM, "original literal frame changed")
    require(all(caps["states"][s] == row for s, row in STATES.items()), "named literal source states changed")
    original40 = set(geometry["target_union_surviving_original_profile_ids"])
    table = {r["original_profile_id"]: r for r in geometry["profiles"]}
    ids = sorted(i for i in original40 if "v" in table[i]["profile"]["u1"])
    require(ids == EXPECTED, "the eight complete u1v profiles changed")
    require(all(["u1", "v"] in table[i]["chords"] for i in ids), "original u1v edge was lost")
    old_ids = sorted(i for i in original40 if "v" in table[i]["profile"]["u3"])
    require(old_ids == OLD_U3V and not set(ids).intersection(old_ids), "previously closed u3v branch changed")
    remaining32 = sorted(original40 - set(old_ids))
    remaining24 = sorted(set(remaining32) - set(ids))
    require((len(remaining32), len(remaining24)) == (32, 24), "source profile coverage sizes differ")
    rows = dict(orbit["rowids"])
    require([rows[h] for h in INCIDENCE] == [44459, 44111, 44111, 44127],
            "unaugmented half-row to full-state map changed")
    actual = {h: [] for h in INCIDENCE}
    wanted = set(INCIDENCE)
    for j, column in enumerate(orbit["columns"]):
        for h in wanted.intersection(column):
            actual[h].append(j)
    require(actual == INCIDENCE, "original complete incidences differ")
    require(set(actual[12302027]) <= set(actual[12301211]), "A to M domination failed")
    require(actual[10064313] == actual[10064365], "M to F equality failed")
    require(rows[6712710] == 44459 and all(6712710 in orbit["columns"][j] for j in (48617, 67755)),
            "requested original X columns do not share the zero A half-row")
    u1, v = RIM.index("u1"), RIM.index("v")
    require(STATES[44127][u1] == STATES[44127][v] == 1, "F is not zero on actual u1v")
    require(STATES[44466][u1] == STATES[44466][v] == 1, "B is not zero on actual u1v")
    require(STATES[44459][u1] != STATES[44459][v], "A was incorrectly declared a direct edge zero")
    positives = []
    for i in ids:
        r = table[i]
        require(r["target_compatibility"]["44459"]["compatible"] and
                not r["target_compatibility"]["44466"]["compatible"], "source target orientation differs")
        positives.append({"original_profile_id": i, "complete_profile": r["profile"],
                          "all_original_chords": r["chords"]})
    orbit_table = {r["original_profile_id"]: r for r in profile_orbits["profiles"]}
    require(all(orbit_table[i]["retained_columns"]["44459_only"] == [48617, 67755] for i in ids),
            "two-column support of the fixed u1v profiles changed")
    final_classes = {"twelve_full_fifteen_column_profiles": [], "twelve_joined_two_column_profiles": []}
    for i in remaining24:
        retained = orbit_table[i]["retained_columns"]
        size = sum(len(x) for x in retained.values())
        if size == 15:
            final_classes["twelve_full_fifteen_column_profiles"].append(i)
        elif size == 2:
            final_classes["twelve_joined_two_column_profiles"].append(i)
        else:
            raise ValueError("unexpected old necessary profile support size")
    require(all(len(ids) == 12 for ids in final_classes.values()), "remaining source classes are not twelve/twelve")
    remaining_targets = {t: [i for i in remaining24 if table[i]["target_compatibility"][t]["compatible"]]
                         for t in ("44459", "44466")}
    require([len(x) for x in remaining_targets.values()] == [12, 24], "remaining literal target coverage differs")
    return {"scope": "strict original only-R/W7 source with actual original edge u1v",
        "inputs": hashes, "original_ordered_rim": RIM, "original_edge": ["u1", "v"],
        "complete_profiles": positives, "named_original_literal_states": {str(s): row for s, row in STATES.items()},
        "unaugmented_complete_incidence": {str(h): js for h, js in actual.items()},
        "unaugmented_source_law": "0<=Z44459<=Z44111=Z44127; no new edge used in this law",
        "direct_original_edge_zero_states": [44127, 44466],
        "forced_zero_original_X_columns": [48617, 67755], "their_zero_A_halfrow": 6712710,
        "source_contradiction": "original witness gives Z44459+Z44466>0; actual u1v makes both zero",
        "previously_closed_u3v_profiles": old_ids, "remaining32_before": remaining32,
        "remaining24_after": remaining24, "remaining_target_compatible_profiles": remaining_targets,
        "remaining_classes_from_old_necessary_support": final_classes,
        "source_branch_excluded": True, "general_W7_excluded": False,
        "graph_symmetry_used": False, "u3v_assumption_used_for_u1v_proof": False,
        "LP_run": False, "new_original_graph_enumeration": False, "smaller_bad": False, "new_Lean": False}


def verify(candidate, expected):
    require(json.dumps(candidate, sort_keys=True, separators=(",", ":")) ==
            json.dumps(expected, sort_keys=True, separators=(",", ":")), "source bridge certificate differs")


def controls(result):
    for kind in ("omit_incident_column", "source_scope", "wrong_original_edge"):
        bad = deepcopy(result)
        if kind == "omit_incident_column":
            bad["unaugmented_complete_incidence"]["10064313"].pop()
        elif kind == "source_scope":
            bad["general_W7_excluded"] = True
        else:
            bad["original_edge"] = ["u3", "v"]
        try:
            verify(bad, result)
        except ValueError:
            pass
        else:
            raise ValueError("invalid source bridge accepted: " + kind)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    result = compute()
    path = HERE / "source-bridge-certificate.json"
    if args.build:
        with path.open("x") as f:
            json.dump(result, f, indent=2, sort_keys=True)
            f.write("\n")
    else:
        verify(json.loads(path.read_text()), result)
    controls(result)
    print(json.dumps({"original_profiles": EXPECTED, "source_law": result["unaugmented_source_law"],
        "remaining_profiles": len(result["remaining24_after"]), "source_branch_excluded": True,
        "general_W7_excluded": False}, sort_keys=True))


if __name__ == "__main__":
    main()
