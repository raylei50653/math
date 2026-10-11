#!/usr/bin/env python3
"""Read-only, independent N45-S-LONG-S-FIBRE necessary-domain audit.

Enumerates D5/S4 normalizers and rejection-set orbits from frozen BASE data.
Does not import the delivery checker and does not validate a target source.
"""

import hashlib
import itertools
import json
from pathlib import Path
import re


BASE = "f2692089ad4259808e27d9b7e882ac09505b180a"
WORKER = Path(__file__).resolve().parents[1] / "2026-10-11-n45-s-long-s-fibre"
COLORS = tuple(range(4))
QROWS = tuple(tuple(map(int, row)) for row in (
    "01212", "01202", "01201", "01021", "01012"
))
CANONICAL = QROWS[4]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalizers(row, original_spoke):
    """Find whole-frame D5/S4 maps to q4 and BASE spoke representatives.

    The selected normalizer prefers an orientation-preserving map when the
    spoke already lies in the BASE representative set {0,1,4}. Otherwise it
    uses the orientation-reversing map. Complete C/U identities are retained.
    """
    candidates = []
    for orientation in (1, -1):
        for shift in range(5):
            boundary = tuple((orientation * i + shift) % 5 for i in range(5))
            if boundary[original_spoke] not in (0, 1, 4):
                continue
            for colors in itertools.permutations(COLORS):
                moved = [None] * 5
                for old in range(5):
                    moved[boundary[old]] = colors[row[old]]
                if tuple(moved) == CANONICAL:
                    candidates.append((orientation, shift, boundary, colors))
    require(bool(candidates), "No complete D5/S4 normalizer")
    return min(candidates, key=lambda item: (item[0] != 1, item[1], item[3]))


def query_domain(observations, final_ids, delivered):
    queries = []
    for beta, row in enumerate(QROWS):
        for spoke in (0, 2):
            orientation, shift, boundary, colors = normalizers(row, spoke)
            actual_supports = ((0, 2, 3, 4), (0, 1, 2))
            moved_supports = [sorted(boundary[i] for i in support)
                              for support in actual_supports]
            available = set(COLORS) - {row[spoke]}
            for c_forbidden in sorted(available):
                u_forbidden = available - {c_forbidden}
                moved_bans = [[colors[c_forbidden]],
                              sorted(colors[color] for color in u_forbidden)]
                matches = [record for record in observations["records"]
                           if record["spoke"] == boundary[spoke]
                           and record["supports"] == moved_supports
                           and record["bans"] == moved_bans]
                initial = sorted(record["id"] for record in matches)
                t4 = sorted(record["id"] for record in matches
                            if record["T4_status"] == "retained")
                final = sorted(set(initial) & final_ids)
                if not initial:
                    classification = "no initial necessary-table match"
                elif not t4:
                    classification = "T4 excluded"
                elif not final:
                    classification = "subsequent source excluded"
                else:
                    classification = "final retained necessary query"
                key = (beta, spoke, c_forbidden)
                require(key in delivered, "Delivery omitted an ambient query")
                saved = delivered[key]
                require(initial == saved["BASE_record_ids"], "Initial IDs differ")
                require(t4 == saved["T4_retained"], "T4 IDs differ")
                require(final == saved["final_retained"], "Final IDs differ")
                queries.append({
                    "beta_q": beta, "beta_literal": "".join(map(str, row)),
                    "original_s_spoke": spoke,
                    "F_C_beta": [c_forbidden], "F_U_beta": sorted(u_forbidden),
                    "whole_boundary_map": boundary, "whole_color_map": colors,
                    "orientation": orientation, "shift": shift,
                    "ordered_actual_supports_after_transport": moved_supports,
                    "BASE_record_ids": initial, "T4_retained": t4,
                    "final_retained": final, "classification": classification,
                })
    require(len(queries) == 30 and len(delivered) == 30, "Query count differs")
    counts = {name: sum(q["classification"] == name for q in queries) for name in (
        "no initial necessary-table match", "T4 excluded",
        "subsequent source excluded", "final retained necessary query"
    )}
    require(list(counts.values()) == [12, 4, 10, 4], "Unexpected query partition")
    return queries, counts


def set_orbit(rejected):
    return sorted({tuple(sorted((orientation * i + shift) % 5 for i in rejected))
                   for orientation in (1, -1) for shift in range(5)})


def schedule_domain(certificate):
    orbits = {941: set_orbit((0, 1, 3)), 933: set_orbit((0, 1, 2, 3))}
    schedules = []
    for spokes, betas in ((1, (3, 4)), (2, (0, 2))):
        for mask, rejection_sets in orbits.items():
            for rejected in rejection_sets:
                for beta in betas:
                    if beta not in rejected:
                        continue
                    delta = sorted(set(rejected) - {beta})
                    excluded = spokes == 2 and beta == 0 and 1 in rejected
                    schedules.append({
                        "t_s": spokes, "SigmaG_orbit": mask,
                        "QG": list(rejected), "beta_q": beta,
                        "beta_literal": "".join(map(str, QROWS[beta])),
                        "QX": [beta], "Delta": delta,
                        "original_e": "rb4", "original_r_split": [2, 2],
                        "s_spoke_domain": [[0], [2]] if spokes == 1 else [[0, 2]],
                        "F_C_beta": [1] if spokes == 1 else [3],
                        "F_U_beta": [2, 3] if spokes == 1 else [1],
                        "all_Delta_X_lifts_required_r": {
                            str(index): QROWS[index][4] for index in delta
                        },
                        "restoration_excluded": excluded,
                        "reason": "q0->q1 restores rb4 and q1 is originally rejected"
                                  if excluded else "same-source r-fibre obligation remains",
                    })
    key = lambda item: (item["t_s"], item["SigmaG_orbit"],
                        tuple(item["QG"]), item["beta_q"])
    require(sorted(map(key, schedules)) == sorted(map(key, certificate["schedules"])),
            "Delivered full-Q schedule domain differs")
    require(len({key(item) for item in schedules}) == len(schedules), "Duplicate schedule")
    counts = {"raw": len(schedules),
              "restoration_excluded": sum(item["restoration_excluded"] for item in schedules),
              "remaining": sum(not item["restoration_excluded"] for item in schedules)}
    require(counts == {"raw": 28, "restoration_excluded": 4, "remaining": 24},
            "Unexpected full-Q schedule partition")
    return orbits, schedules, counts


def main():
    inputs = json.loads((WORKER / "inputs.json").read_text())
    require(inputs["base"] == BASE, "Wrong BASE")
    for entry in inputs["entries"]:
        require(entry["base"] == BASE, "Entry BASE differs")
        require(digest(WORKER / entry["frozen_path"]) == entry["sha256"],
                "Frozen input drift: " + entry["path"])
    obs_path = WORKER / "frozen/artifacts/c5_single_spoke_two_two/observations.json"
    table_path = WORKER / "frozen/artifacts/c5_single_spoke_residual_locality/support_table.md"
    observations = json.loads(obs_path.read_text())
    final_ids = {int(match.group(1)) for match in
                 re.finditer(r"^\| (\d+) \|", table_path.read_text(), re.MULTILINE)}
    require(len(final_ids) == 102, "Unexpected frozen final-table coverage")
    certificate_path = WORKER / "certificate.json"
    certificate = json.loads(certificate_path.read_text())
    delivered = {(item["beta_q"], item["original_s_spoke"], item["FC_beta"][0]): item
                 for item in certificate["pair_t1_BASE_mapping"]}
    queries, query_counts = query_domain(observations, final_ids, delivered)
    orbits, schedules, schedule_counts = schedule_domain(certificate)
    print(json.dumps({
        "status": "triggered and holds", "scope": "necessary-domain arithmetic only",
        "finite_source_status": "not triggered", "finite_source_validator_executed": False,
        "BASE": BASE, "frozen_input_count": len(inputs["entries"]),
        "frozen_input_drift": 0,
        "compared_files_sha256": {str(path.relative_to(WORKER)): digest(path)
                                  for path in (obs_path, table_path, certificate_path)},
        "query_counts": query_counts, "queries": queries,
        "QG_orbits": orbits, "schedule_counts": schedule_counts,
        "schedules": schedules,
    }, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
