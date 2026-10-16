#!/usr/bin/env python3
"""Independent 4^5 row screen; geometric soundness is proved in PROOF.md."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
FROZEN = AUDIT / "frozen"
CATALOGUE = "artifacts/c5_cells/cells.json"
TRANSFER = "audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/transfer.json"
COUNTS = "audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/counts.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normalise(values):
    names = {}
    return tuple(names.setdefault(value, len(names)) for value in values)


def word(values):
    return "".join(chr(65 + value) for value in values)


def make_certificate():
    seal = json.loads((AUDIT / "INPUTS.json").read_text())
    require(seal["base"] == "676b1024715f24a0d969fba90baab21b756406e2", "wrong BASE")
    for entry in seal["inputs"]:
        require(sha(FROZEN / entry["path"]) == entry["sha256"],
                "frozen input digest mismatch: " + entry["path"])
    cells = json.loads((FROZEN / CATALOGUE).read_text())
    transfer = json.loads((FROZEN / TRANSFER).read_text())
    counts = json.loads((FROZEN / COUNTS).read_text())

    # Rebuild all rows from all labelled assignments; no production imports.
    assignments = list(itertools.product(range(4), repeat=5))
    proper = [row for row in assignments
              if all(row[i] != row[(i + 1) % 5] for i in range(5))]
    patterns = sorted({normalise(row) for row in proper})
    # Independent canonicalisation by the whole S4 orbit, checked on every row.
    permutations = list(itertools.permutations(range(4)))
    for row in proper:
        orbit_minimum = min(tuple(p[colour] for colour in row) for p in permutations)
        require(normalise(row) == orbit_minimum, "canonicalisation disagreement")
    require(len(assignments) == 1024 and len(proper) == 240, "wrong labelled domain")
    require(len(patterns) == 10, "wrong canonical row domain")
    require([list(p) for p in patterns] == cells["pattern_order"], "catalogue row order mismatch")
    require([list(p) for p in patterns] == counts["pattern_order"], "old count row order mismatch")
    names = [word(p) for p in patterns]
    require(names == [row["boundary"] for row in transfer["table"]], "transfer row order mismatch")
    require([row["index"] for row in transfer["table"]] == list(range(10)), "transfer bit order mismatch")

    upper = sum(1 << i for i, row in enumerate(transfer["table"]) if row["ordered_pq"])
    require(upper == transfer["allowed_outer_mask"] == 319, "frozen all-lift support mismatch")
    catalogue_masks = sorted(int(mask) for mask in cells["cells"])
    require(len(catalogue_masks) == cells["distinct_sigma"] == 132, "wrong catalogue size")
    require(0 not in catalogue_masks, "empty catalogue relation present")
    candidates = [mask for mask in catalogue_masks if mask & upper == mask]
    require(candidates == transfer["catalogue_candidates"] == counts["masks"] == [271, 314, 319],
            "wrong old candidate set")

    equality_screens = []
    for label, left, right in [("s=w", 1, 3), ("v=t", 2, 4)]:
        indices = [i for i, row in enumerate(patterns) if row[left] == row[right]]
        equal_mask = sum(1 << i for i in indices)
        # Check the equality support directly before S4 quotient as well.
        labelled_equal = [row for row in proper if row[left] == row[right]]
        require({normalise(row) for row in labelled_equal} == {patterns[i] for i in indices},
                "labelled equality support disagreement")
        live_indices = [i for i in indices if upper & (1 << i)]
        require(len(live_indices) == 1, "equality did not force exactly one live row")
        equality_screens.append({
            "equality": label,
            "positions": [left, right],
            "labelled_proper_assignments": len(labelled_equal),
            "all_rows": [names[i] for i in indices],
            "equality_mask": equal_mask,
            "rows_inside_upper": [names[i] for i in live_indices],
            "forced_nonempty_row_bit": 1 << live_indices[0],
            "excluded_old_masks": [mask for mask in candidates if mask & equal_mask == 0],
        })
    required = sum(screen["forced_nonempty_row_bit"] for screen in equality_screens)
    surviving = [mask for mask in candidates if mask & required == required]
    require(required == 17 and surviving == [319], "wrong strengthened frontier")
    # Check whether both equality requirements could use the same colouring.
    joint = [row for row in proper if row[1] == row[3] and row[2] == row[4]]
    # There actually is the proper row ABCBC with both equalities; it lies
    # outside 319. Check that fact explicitly rather than conflating witnesses.
    require({word(normalise(row)) for row in joint} == {"ABCBC"}, "joint equality row mismatch")
    require(not any((upper & (1 << i)) and row[1] == row[3] and row[2] == row[4]
                    for i, row in enumerate(patterns)), "unexpected same-colouring witness")

    return {
        "status": "PASS: finite row screen for the paper source-quotient theorem",
        "base": seal["base"],
        "script_sha256": sha(Path(__file__).resolve()),
        "input_manifest_sha256": sha(AUDIT / "INPUTS.json"),
        "frozen_inputs_verified": len(seal["inputs"]),
        "input_sha256": {name: sha(FROZEN / name) for name in [CATALOGUE, TRANSFER, COUNTS]},
        "pins": ["z", "s", "v", "w", "t"],
        "labelled_assignments_checked": len(assignments),
        "proper_labelled_assignments": len(proper),
        "canonical_rows": names,
        "row_orbit_sizes": [sum(normalise(row) == p for row in proper) for p in patterns],
        "catalogue_size": len(catalogue_masks),
        "catalogue_has_empty_relation": False,
        "all_lift_upper_mask": upper,
        "old_candidates": candidates,
        "equality_screens": equality_screens,
        "required_row_bits": required,
        "surviving_candidates": surviving,
        "joint_equality_rows": sorted({word(normalise(row)) for row in joint}),
        "joint_equality_rows_inside_upper": [],
        "cap_budget": {
            "U_total": "k", "quotient_total": "k-1", "added_vertices": 3,
            "outer_boundary_vertices": 5, "cap_total": "k+2", "cap_interiors": "k-3",
            "strictly_below_source_k": True,
        },
        "geometry_authority": "PROOF.md; the checker does not certify an arbitrary embedding",
        "counts_authority": "old certificates retained; their weaker necessary model remains feasible",
        "source_realizations_constructed": 0,
        "new_Lean_theorems": 0,
        "general_bound": "unchanged: k>=23 and K<=22=K<=5=K132",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "r6-final.json")
    args = parser.parse_args()
    certificate = make_certificate()
    if args.write:
        with args.certificate.open("x") as stream:
            stream.write(json.dumps(certificate, indent=2, ensure_ascii=False) + "\n")
        print("WROTE " + str(args.certificate))
    else:
        actual = json.loads(args.certificate.read_text())
        require(actual == certificate, "certificate differs from independent recomputation")
        print("PASS: 1024 assignments; 240 proper; ten rows; 132 frozen masks; 271/314 excluded; 319 survives")
        print("NOTE: geometric cap proof is in PROOF.md; two separate full-colouring witnesses; no new 4CT/Lean/source claim")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
