#!/usr/bin/env python3
"""Local face/matching algebra calibration; no source realization claim."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "ffea555fc2a896d8166ce198ca28ed9262912f25"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def frozen_inputs() -> list[dict]:
    manifest = json.loads((ROOT / "INPUTS.json").read_text())
    require(manifest["base"] == BASE, "wrong frozen BASE")
    seals = []
    for entry in manifest["inputs"]:
        data = (ROOT / "frozen" / entry["path"]).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        require(len(data) == entry["bytes"], f"frozen byte drift: {entry['path']}")
        require(digest == entry["sha256"], f"frozen hash drift: {entry['path']}")
        seals.append({"path": entry["path"], "sha256": digest})
    return seals


def rows(edges: list[str], vertices: list[list[str]]) -> list[dict]:
    result = []
    for bits in itertools.product((0, 1), repeat=len(edges)):
        assignment = dict(zip(edges, bits))
        result.append({
            "assignment": assignment,
            "matching_at_named_faces": all(
                sum(assignment[edge] for edge in incident) == 1
                for incident in vertices
            ),
        })
    return result


def slice_rows(all_rows: list[dict], pins: dict[str, int]) -> list[dict]:
    return [row["assignment"] for row in all_rows
            if row["matching_at_named_faces"]
            and all(row["assignment"][edge] == bit for edge, bit in pins.items())]


def forcing_case(c_side: bool) -> dict:
    # Literal two primal triangles: mzq and zpq, or mzp and zpq.
    side = "q" if c_side else "p"
    forced = "pz*" if c_side else "zq*"
    shared = "zq*" if c_side else "pz*"
    private = f"m{side}*"
    all_rows = rows(["g", private, shared, "f", forced],
                    [["g", private, shared], [shared, "f", forced]])
    target = slice_rows(all_rows, {"g": 1, "f": 0})
    without_g = slice_rows(all_rows, {"f": 0})
    without_f = slice_rows(all_rows, {"g": 1})
    require(len(target) == 1 and target[0][forced] == 1,
            "degree-four forcing failed")
    require(any(row[forced] == 0 for row in without_g),
            "removed-g negative control has no countermodel")
    require(any(row[forced] == 0 for row in without_f),
            "removed-f negative control has no countermodel")
    return {
        "side_degree_four": "c0" if c_side else "a0",
        "primal_faces": [["m", "z", side], ["z", "p", "q"]],
        "forced_dual_edge": forced,
        "all_assignments_including_nonmatchings": all_rows,
        "g_selected_f_omitted": target,
        "remove_g_premise": without_g,
        "remove_f_premise": without_f,
    }


def degree_six_faces(alpha: str, n_vertex: str) -> list[list[str]]:
    faces = [["m", "z", alpha], ["z", alpha, n_vertex]]
    require(all(len(set(face)) == 3 for face in faces),
            "degree-six faces must be genuine triangles")
    return faces


def collision_case(c_side: bool) -> dict:
    centre = "q" if c_side else "p"
    inner = "beta" if c_side else "alpha"
    near = "n_c" if c_side else "n_a"
    faces = degree_six_faces(inner, near)
    cap_centres = {centre, near}
    inside = [bool(set(face) & cap_centres) for face in faces]
    require(inside == [False, True], "wrong actual cap-face membership")
    spoke = f"z{inner}*"
    first_private = f"m{inner}*"
    last_private = [f"z{near}*", f"{inner}{near}*"]
    all_rows = rows(["g", first_private, spoke] + last_private,
                    [["g", first_private, spoke], [spoke] + last_private])
    target = slice_rows(all_rows, {"g": 1, spoke: 1})
    without_g = slice_rows(all_rows, {spoke: 1})
    without_spoke = slice_rows(all_rows, {"g": 1})
    require(target == [], "two incident selected matching edges were accepted")
    require(len(without_g) > 0 and len(without_spoke) > 0,
            "collision negative control failed to recover local matchings")
    return {
        "side_degree_six": "c0" if c_side else "a0",
        "primal_faces": faces,
        "cap_centres": sorted(cap_centres),
        "dual_vertices_in_X": inside,
        "crossing_spoke": spoke,
        "all_assignments_including_nonmatchings": all_rows,
        "g_and_spoke_selected": target,
        "remove_g_premise": without_g,
        "remove_spoke_premise": without_spoke,
    }


def reconstruct() -> dict:
    seals = frozen_inputs()
    try:
        degree_six_faces("n_a", "n_a")
    except ValueError as error:
        degenerate_control = {"status": "rejected", "reason": str(error)}
    else:
        raise ValueError("degree-five endpoint collision was silently accepted")
    return {
        "schema": "active-f-seven-A-local-matching-v1",
        "base": BASE,
        "authority": "finite local matching calibration only",
        "source_realization": "not triggered",
        "input_seals": seals,
        "degree_four_forcing": [forcing_case(False), forcing_case(True)],
        "degree_six_collision": [collision_case(False), collision_case(True)],
        "degenerate_endpoint_negative_control": degenerate_control,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write-certificate", type=Path)
    group.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    expected = reconstruct()
    if args.write_certificate:
        with args.write_certificate.open("x") as output:
            json.dump(expected, output, sort_keys=True, indent=2)
            output.write("\n")
        action = "created exclusively"
    else:
        actual = json.loads(args.certificate.read_text())
        require(actual == expected, "certificate differs from full reconstruction")
        action = "replayed read-only"
    print(json.dumps({
        "status": "PASS", "action": action,
        "frozen_inputs": len(expected["input_seals"]),
        "degree_four_cases": len(expected["degree_four_forcing"]),
        "degree_six_cases": len(expected["degree_six_collision"]),
        "all_assignments_retained": 4 * 2 ** 5,
        "source_realization": "not triggered",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
