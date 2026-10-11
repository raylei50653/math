#!/usr/bin/env python3
"""Read-only independent S4, forbidden-column, and coverage metadata check.

No delivered checker is imported. No graph, source assignment, or old control
is constructed. All mathematical source premises remain paper dependencies.
"""
from copy import deepcopy
from itertools import combinations, permutations, product
import json
from pathlib import Path


TARGET = Path(__file__).resolve().parent.parent / "2026-10-11-n45-s-long-s-t2-q0-restore"
COLOURS = frozenset(range(4))
BETA = (0, 1, 2, 1, 2)
Q1 = (0, 1, 2, 0, 2)
Q2 = (0, 1, 2, 0, 1)
Q_ROWS = (BETA, Q1, Q2, (0, 1, 0, 2, 1), (0, 1, 0, 1, 2))
EXPECTED_SCHEDULES = {(933, (0, 2, 3, 4)), (941, (0, 2, 3)), (941, (0, 2, 4))}
ALL_PINS = set(product(range(4), repeat=2))


def read(relative):
    return json.loads((TARGET / relative).read_text())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def differences(first, second, path=""):
    """Record scalar differences; treat a changed list length as one difference."""
    if isinstance(first, dict) and isinstance(second, dict):
        out = []
        for key in sorted(first.keys() | second.keys()):
            if key not in first or key not in second:
                out.append({"path": path + "/" + key, "missing_key": True})
            else:
                out.extend(differences(first[key], second[key], path + "/" + key))
        return out
    if isinstance(first, list) and isinstance(second, list):
        if len(first) != len(second):
            return [{"path": path, "length_before": len(first), "length_after": len(second)}]
        out = []
        for index, (left, right) in enumerate(zip(first, second)):
            out.extend(differences(left, right, path + "/" + str(index)))
        return out
    return [] if first == second else [{"path": path, "before": first, "after": second}]


def main():
    certificate = read("proof-calibration.json")
    coverage = read("coverage.json")
    transports = []
    require(len(certificate["support_transports"]) == 2, "transport count")
    for name, support, target_literal in (("L", (2, 3, 4), Q1), ("S", (4, 0), Q2)):
        # Exhaust all of S4; the fixed s=3 condition leaves exactly one map.
        candidates = [
            perm for perm in permutations(range(4))
            if perm[3] == 3 and all(perm[BETA[i]] == target_literal[i] for i in support)
        ]
        require(len(candidates) == 1, "unique S4 support transport: " + name)
        perm = candidates[0]
        matches = [tr for tr in certificate["support_transports"] if tr["piece"] == name]
        require(len(matches) == 1, "transport record uniqueness: " + name)
        recorded = matches[0]
        maps = [
            {"beta_pin": [a, b], "target_pin": [perm[a], perm[b]]}
            for a, b in product(range(4), repeat=2)
        ]
        require({tuple(item["target_pin"]) for item in maps} == ALL_PINS, "pin bijection")
        require(recorded["all_16_ordered_pin_maps"] == maps, "complete recorded pin maps")
        require(recorded["whole_piece_colour_permutation"] == list(perm), "recorded S4 map")
        require(recorded["ordered_actual_support"] == list(support), "ordered actual support")
        require(recorded["beta_values"] == [BETA[i] for i in support], "beta support values")
        require(recorded["target_values"] == [target_literal[i] for i in support], "target support values")
        require(recorded["mapped_beta_values"] == [perm[BETA[i]] for i in support], "mapped support values")
        require(recorded["target_literal"] == "".join(map(str, target_literal)), "transport literal")
        transports.append({
            "piece": name, "ordered_support": list(support),
            "unique_s3_fixing_colour_permutation": list(perm),
            "S4_permutations_checked": 24, "pin_bijections": len(maps),
            "s3_column_pins": sum(item["beta_pin"][1] == 3 for item in maps),
        })

    p_l = transports[0]["unique_s3_fixing_colour_permutation"]
    p_s = transports[1]["unique_s3_fixing_colour_permutation"]
    cases = []
    # Paper premises: each column has size 2, disjoint union is all four colours,
    # and the short diagonal theorem excludes colour 3 from beta D_S.
    for pair in combinations(range(3), 2):
        d_s = frozenset(pair)
        d_l = COLOURS - d_s
        q1_d_l = frozenset(p_l[colour] for colour in d_l)
        q1_allowed = COLOURS - (d_s | q1_d_l)
        q2_d_s = frozenset(p_s[colour] for colour in d_s)
        cases.append({
            "beta_D_S": sorted(d_s), "beta_D_L": sorted(d_l),
            "q1_D_L": sorted(q1_d_l), "q1_allowed_r": sorted(q1_allowed),
            "excluded_by_original_q1_acceptance": not q1_allowed,
            "q2_D_S": sorted(q2_d_s),
            "q2_r1_fibre_empty_in_surviving_case": (1 in q2_d_s) if q1_allowed else None,
        })
    require(cases == certificate["cases"], "independent forbidden-column cases")
    surviving = [case for case in cases if not case["excluded_by_original_q1_acceptance"]]
    require(len(surviving) == 2, "surviving columns")
    require(all(2 in case["beta_D_S"] and 1 in case["q2_D_S"] for case in surviving), "q2 r1 blocker")

    schedules = coverage["schedules"]
    require(len(schedules) == 3, "schedule count")
    require({(s["SigmaG_orbit"], tuple(s["QG"])) for s in schedules} == EXPECTED_SCHEDULES,
            "exact assigned schedules")
    # Independently enumerate normalized proper literal boundary rows only.
    literals = sorted(
        "".join(map(str, row)) for row in product(range(4), repeat=5)
        if row[0] == 0
        and all(row[i] != row[(i + 1) % 5] for i in range(5))
        and all(row[j] <= max(row[:j]) + 1 for j in range(1, 5))
    )
    require(len(literals) == 10, "ten normalized proper boundary rows")
    total_pins = diagonals = q2_empty = restoration_pool = 0
    total_rows = 0
    for schedule in schedules:
        require(schedule["original_s_spoke_variants"] == [[0, 2]], "original spokes")
        require(schedule["beta_q"] == 0 and schedule["beta_literal"] == "01212", "original beta")
        require(1 not in schedule["QG"] and 2 in schedule["QG"], "accepted q1 and rejected q2")
        expected_delta = [
            {"q": q, "literal": "".join(map(str, Q_ROWS[q])),
             "original_rejection_requires_all_X_lifts_r": Q_ROWS[q][4]}
            for q in schedule["QG"] if q != 0
        ]
        require(schedule["Delta"] == expected_delta, "literal original-edge Delta")
        rows = schedule["all_ten_literal_obligations"]
        require(["".join(map(str, row["literal"])) for row in rows] == literals, "literal row completeness")
        total_rows += len(rows)
        for row in rows:
            literal_tuple = tuple(row["literal"])
            literal = "".join(map(str, literal_tuple))
            pins = row["pins"]
            require(len(pins) == 16 and {(pin["r"], pin["s"]) for pin in pins} == ALL_PINS,
                    "all ordered pin positions")
            require(row["gamma_b4"] == literal_tuple[4], "original b4 colour")
            analysis = row["current_paper_analysis"]
            q = Q_ROWS.index(literal_tuple) if literal_tuple in Q_ROWS else None
            expected_empty_r = [a for a in range(4) if a != literal_tuple[4]] if q in schedule["QG"] else []
            require(analysis["literal_b4_colour"] == literal_tuple[4], "analysis b4 colour")
            require(analysis["restoration_condition"] == "a != literal(b4)", "restoration condition")
            require(analysis["G_rejection_necessary_empty_r_values"] == expected_empty_r, "rejection fibre coordinate")
            require(analysis["concrete_relations_and_preimages_supplied"] is False, "metadata assignment scope")
            total_pins += len(pins)
            diagonals += sum(pin["r"] == pin["s"] for pin in pins)
            for pin in pins:
                a, b = pin["r"], pin["s"]
                reasons = []
                if literal_tuple == BETA:
                    reasons.append("accepted original beta rejection: all X pins empty")
                if b in {literal_tuple[0], literal_tuple[2]}:
                    reasons.append("retained original s-spoke constraint")
                if literal_tuple in (BETA, Q1, Q2) and b == 1:
                    reasons.append("actual U012 F_U={1}")
                if literal_tuple == Q2 and a == 1 and b == 3:
                    reasons.append("T2Q0-Q2-EMPTY1 via complete S pi12 bijection")
                require(pin["new_paper_necessary_empty_reasons"] == reasons, "pin emptiness metadata")
                pool = literal_tuple == Q2 and b == 3 and a != 1
                require(pin["new_q2_restoration_pool_member"] == pool, "restoration pool metadata")
                require(pin["concrete_fibre_values_supplied"] is False, "no invented fibre values")
                if literal_tuple == Q2:
                    necessarily_empty = b != 3 or a == 1
                    require(bool(reasons) == necessarily_empty, "q2 thirteen empty positions")
                    q2_empty += necessarily_empty
                    restoration_pool += pool
    require((total_rows, total_pins, diagonals, q2_empty, restoration_pool) == (30, 480, 120, 39, 9),
            "coverage counts")

    bad_column = read("negative-controls/bad-q2-column.json")
    column_differences = differences(certificate, bad_column)
    require(column_differences == [{"path": "/cases/1/q2_D_S/1", "before": 1, "after": 2}],
            "exact q2 negative-control difference")
    bad_coverage = read("negative-controls/missing-diagonal.json")
    coverage_differences = differences(coverage, bad_coverage)
    require(coverage_differences == [{
        "path": "/schedules/0/all_ten_literal_obligations/0/pins", "length_before": 16, "length_after": 15,
    }], "single shortened pin list")
    expected_bad_coverage = deepcopy(coverage)
    expected_pins = expected_bad_coverage["schedules"][0]["all_ten_literal_obligations"][0]["pins"]
    expected_pins[:] = [pin for pin in expected_pins if (pin["r"], pin["s"]) != (3, 3)]
    require(bad_coverage == expected_bad_coverage, "exact diagonal removal with no other mutation")
    require(schedules[0]["id"] == "B-933-0234" and literals[0] == "01012", "negative-control location")

    print(json.dumps({
        "status": "independent arithmetic passes",
        "scope": "bounded abstract columns, colour transports and assignment metadata only",
        "cases": cases, "transports": transports,
        "counts": {
            "S4_permutations_checked_per_transport": 24, "column_cases": 3, "survivors": 2,
            "support_transports": 2, "pin_maps": 32, "coverage_schedules": 3,
            "coverage_rows": total_rows, "coverage_pins": total_pins, "diagonal_positions": diagonals,
            "q2_necessarily_empty_positions": q2_empty,
            "q2_collectively_nonempty_pool_positions": restoration_pool,
        },
        "negative_q2_diff": column_differences,
        "negative_diagonal_removed": {"schedule": "B-933-0234", "literal": "01012", "pin": [3, 3]},
        "checker_imported": False, "source_controls_reexecuted": False, "source_graphs_enumerated": 0,
        "actual_assignment_values_supplied": False,
        "individual_restoration_pool_fibre_nonempty_claimed": False,
        "target_source": {"executed": False, "trigger_count": None, "status": "not triggered"},
    }, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
