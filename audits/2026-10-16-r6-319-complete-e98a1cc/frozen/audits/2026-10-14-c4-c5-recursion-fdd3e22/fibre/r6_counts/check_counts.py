#!/usr/bin/env python3
"""Necessary common labelled-row multiplicities for the degree-six r control.

--solve uses scipy only to propose a witness. --check verifies exact integer
equalities without numpy/scipy. Neither mode constructs a source graph.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
import itertools
import json
from math import gcd, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "input_transfer.py"
spec = importlib.util.spec_from_file_location("transfer", INPUT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
PATTERNS = tuple(sorted({helper.canonical(word)
                         for word in itertools.product(range(4), repeat=5)
                         if all(word[i] != word[(i + 1) % 5] for i in range(5))}))
MASKS = (271, 314, 319)


def raw_orbit(row, parts, split):
    blocks = [(block, pair) for groups, pair in zip(parts, split) for block in groups]
    rows = []
    for flags in itertools.product((False, True), repeat=len(blocks)):
        target = list(row)
        for use, (block, pair) in zip(flags, blocks):
            if use:
                a, b = pair
                for v in block:
                    target[v] = b if target[v] == a else a
        rows.append(tuple(target))
    assert len(set(rows)) == len(rows), "visible component switches must act freely"
    return tuple(sorted(rows))


def model(mask):
    rows = [row for row in itertools.product(range(4), repeat=7)
            if helper.allowed(row) and mask >> PATTERNS.index(helper.canonical(row[:5])) & 1]
    row_set = set(rows)
    canonical = sorted({helper.canonical(row) for row in rows})
    row_index = {row: i for i, row in enumerate(rows)}
    canonical_index = {row: i for i, row in enumerate(canonical)}
    blocks = []
    for split in helper.PAIRINGS:
        orbit_witnesses = {}
        for row in rows:
            for parts in itertools.product(*(helper.pair_partitions(row, pair, helper.EDGES)
                                              for pair in split)):
                if not helper.noncrossing(parts[0] + parts[1]):
                    continue
                orbit = raw_orbit(row, parts, split)
                if set(orbit) <= row_set:
                    orbit_witnesses.setdefault(orbit, parts)
        blocks.append([(orbit, orbit_witnesses[orbit]) for orbit in sorted(orbit_witnesses)])
    return {"mask": mask, "rows": rows, "canonical": canonical,
            "row_index": row_index, "canonical_index": canonical_index, "blocks": blocks}


def verify(model_data, witness):
    counts = witness["row_counts"]
    assert len(counts) == len(model_data["canonical"])
    assert all(type(x) is int and x >= 0 for x in counts)
    for i, pattern in enumerate(PATTERNS):
        if model_data["mask"] >> i & 1:
            assert sum(count for row, count in zip(model_data["canonical"], counts)
                       if helper.canonical(row[:5]) == pattern) > 0, "required fibre empty"
    assert len(witness["pairing_masses"]) == 3
    for blocks, sparse in zip(model_data["blocks"], witness["pairing_masses"]):
        actual = {row: 0 for row in model_data["rows"]}
        seen = set()
        for index, mass in sparse:
            assert type(index) is int and 0 <= index < len(blocks) and index not in seen
            seen.add(index)
            assert type(mass) is int and mass > 0
            for row in blocks[index][0]:
                actual[row] += mass
        for row, count in actual.items():
            expected = counts[model_data["canonical_index"][helper.canonical(row)]]
            assert count == expected, "pairing marginal disagrees with common full-row count"
    return True


def solve(model_data):
    import numpy as np
    from scipy.optimize import linprog
    nrows = len(model_data["rows"])
    ncanonical = len(model_data["canonical"])
    nvars = ncanonical + sum(len(blocks) for blocks in model_data["blocks"])
    equality = np.zeros((3 * nrows, nvars))
    for split_index in range(3):
        for row in model_data["rows"]:
            i = split_index * nrows + model_data["row_index"][row]
            equality[i, model_data["canonical_index"][helper.canonical(row)]] = 1
    column = ncanonical
    for split_index, blocks in enumerate(model_data["blocks"]):
        for orbit, _ in blocks:
            for row in orbit:
                equality[split_index * nrows + model_data["row_index"][row], column] = -1
            column += 1
    inequality = []
    for i, pattern in enumerate(PATTERNS):
        if model_data["mask"] >> i & 1:
            constraint = np.zeros(nvars)
            for j, row in enumerate(model_data["canonical"]):
                if helper.canonical(row[:5]) == pattern:
                    constraint[j] = -1
            inequality.append(constraint)
    objective = np.zeros(nvars)
    objective[:ncanonical] = 1
    solution = linprog(objective, A_ub=np.array(inequality), b_ub=-np.ones(len(inequality)),
                       A_eq=equality, b_eq=np.zeros(3 * nrows), bounds=(0, None), method="highs")
    assert solution.success, {"mask": model_data["mask"], "solver_status": solution.message}
    rational = [Fraction(float(value)).limit_denominator(1000000) for value in solution.x]
    multiplier = lcm(*(value.denominator for value in rational))
    integer = [int(value * multiplier) for value in rational]
    divisor = gcd(*integer)
    integer = [value // divisor for value in integer]
    row_counts = integer[:ncanonical]
    pairing_masses = []
    index = ncanonical
    for blocks in model_data["blocks"]:
        pairing_masses.append([[j, integer[index + j]] for j in range(len(blocks))
                               if integer[index + j] > 0])
        index += len(blocks)
    witness = {"row_counts": row_counts, "pairing_masses": pairing_masses}
    verify(model_data, witness)
    return witness


def describe(model_data, witness):
    records = []
    for split, blocks, sparse in zip(helper.PAIRINGS, model_data["blocks"], witness["pairing_masses"]):
        records.append({"pairing": split, "available_projected_orbits": len(blocks),
                        "positive_masses": [{"orbit_index": index, "mass": mass,
                                             "terminal_parts": blocks[index][1],
                                             "labelled_rows": [helper.name(row) for row in blocks[index][0]]}
                                            for index, mass in sparse]})
    return {"mask": model_data["mask"], "labelled_row_domain": len(model_data["rows"]),
            "canonical_rows": [helper.name(row) for row in model_data["canonical"]],
            "row_counts": witness["row_counts"], "pairing_masses": witness["pairing_masses"],
            "positive_orbit_records": records,
            "total_labelled_mass": 24 * sum(witness["row_counts"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solve", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "counts.json")
    args = parser.parse_args()
    assert args.solve != args.check, "choose --solve or --check"
    source = json.loads(args.certificate.read_text()) if args.check else None
    cases = []
    for i, mask in enumerate(MASKS):
        data = model(mask)
        witness = source["cases"][i] if source else solve(data)
        verify(data, witness)
        # Both controls must be rejected for every case.
        bad = dict(witness, row_counts=list(witness["row_counts"]))
        bad["row_counts"][0] += 1
        try:
            verify(data, bad)
        except AssertionError as error:
            assert "pairing marginal" in str(error)
        else:
            raise AssertionError("altered row count accepted")
        zero = {"row_counts": [0] * len(data["canonical"]), "pairing_masses": [[], [], []]}
        try:
            verify(data, zero)
        except AssertionError as error:
            assert "required fibre empty" in str(error)
        else:
            raise AssertionError("zero witness accepted")
        cases.append(describe(data, witness))
    result = {"status": "FEASIBLE exact integer necessary count model; no source realization",
              "masks": MASKS, "pattern_order": PATTERNS,
              "cases": cases, "actual_target_sources": 0,
              "negative_controls": {"altered_row_count_rejected": True, "all_zero_rejected": True},
              "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
              "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}
    payload = json.dumps(result, indent=2) + "\n"
    if args.check:
        assert args.certificate.read_text() == payload, "counts certificate differs"
    else:
        with args.certificate.open("x") as handle:
            handle.write(payload)
    print(json.dumps({"status": result["status"],
                      "cases": [{"mask": case["mask"], "row_counts": case["row_counts"],
                                 "total_labelled_mass": case["total_labelled_mass"]} for case in cases]}))


if __name__ == "__main__":
    main()
