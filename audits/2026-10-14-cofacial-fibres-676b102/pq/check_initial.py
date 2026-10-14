#!/usr/bin/env python3
"""Exact local full lifts on the two actual C4 faces of T0-{x,y,p}."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random

PINS = ("z", "s", "r", "t", "q", "ell", "m")
FACE_EDGES = (("z", "s"), ("s", "r"), ("r", "t"), ("t", "z"),
              ("z", "q"), ("q", "ell"), ("ell", "m"), ("m", "z"))
CAP_EDGES = (("z", "x"), ("s", "x"), ("r", "x"), ("x", "y"),
             ("z", "y"), ("r", "y"), ("t", "y"), ("p", "z"),
             ("p", "q"), ("p", "ell"), ("p", "m"))
COLORS = range(4)
HERE = Path(__file__).resolve().parent


def word(row):
    return "".join("ABCD"[c] for c in row)


def canonical(row):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in row)


def proper(f, edges):
    return all(f[a] != f[b] for a, b in edges)


def direct_lifts(f):
    lifts = []
    for x, y, p in itertools.product(COLORS, repeat=3):
        g = dict(f, x=x, y=y, p=p)
        if proper(g, CAP_EDGES):
            lifts.append((x, y, p))
    return lifts


def product_lifts(f):
    xy = [(x, y) for x in COLORS for y in COLORS
          if x not in {f["z"], f["s"], f["r"]}
          and y not in {f["z"], f["r"], f["t"]} and x != y]
    ps = [p for p in COLORS
          if p not in {f["z"], f["q"], f["ell"], f["m"]}]
    return [(x, y, p) for x, y in xy for p in ps]


def changing(f, lift):
    x, y, p = lift
    return {x, y} != {p, f["q"]}


def build(seed):
    rows = list(itertools.product(COLORS, repeat=len(PINS)))
    random.Random(seed).shuffle(rows)
    cells = {}
    proper_count = quotient_count = quotient_lifts = 0
    quotient_survivors = []
    alias_count = alias_lifts = alias_changing = 0
    alias_survivors = []
    for row in rows:
        f = dict(zip(PINS, row))
        if not proper(f, FACE_EDGES):
            continue
        proper_count += 1
        lifts = direct_lifts(f)
        assert lifts == product_lifts(f), (row, "cap product mismatch")
        bad = [lift for lift in lifts if changing(f, lift)]
        if row == canonical(row):
            cells[word(row)] = {
                "all_cap_lifts_x_y_p": [word(lift) for lift in lifts],
                "palette_changing_lifts_x_y_p": [word(lift) for lift in bad],
                "universal_target_failure_allowed": not bad,
            }
        if f["z"] != f["r"] or f["q"] != f["m"]:
            continue
        quotient_count += 1
        quotient_lifts += len(lifts)
        assert lifts, (row, "quotient slice must have a full cap lift")
        expected_survival = (
            f["s"] == f["t"] == f["ell"]
            and len({f["z"], f["s"], f["q"]}) == 3
        )
        assert (not bad) == expected_survival, (row, lifts, bad)
        if not bad:
            quotient_survivors.append(row)
        if f["m"] == f["t"]:
            alias_count += 1
            alias_lifts += len(lifts)
            alias_changing += len(bad)
            if not bad:
                alias_survivors.append(row)
    orbit = sorted({word(canonical(row)) for row in quotient_survivors})
    assert proper_count == 1764
    assert len(cells) == 74
    assert quotient_count == 324
    assert len(quotient_survivors) == 24
    assert orbit == ["ABABCBC"]
    assert alias_count == 108
    assert alias_lifts == 384
    assert alias_changing == 288
    assert not alias_survivors
    assert cells["ABABCBC"]["all_cap_lifts_x_y_p"] == ["CDD", "DCD"]
    return {
        "schema": "same-T0-two-C4-local-full-lifts-v1",
        "frozen_base": "676b1024715f24a0d969fba90baab21b756406e2",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "pins": PINS,
        "actual_C4_faces": (("z", "s", "r", "t"), ("z", "q", "ell", "m")),
        "retained_required_edges": FACE_EDGES,
        "all_restoration_edges": CAP_EDGES,
        "labelled_assignments_examined": 4 ** len(PINS),
        "proper_labelled_face_rows": proper_count,
        "all_canonical_proper_face_rows": dict(sorted(cells.items())),
        "simultaneous_identification_slice": {
            "classes": (("z", "r"), ("q", "m")),
            "proper_labelled_rows": quotient_count,
            "complete_cap_lifts": quotient_lifts,
            "universal_failure_labelled_rows": len(quotient_survivors),
            "universal_failure_canonical_rows": orbit,
            "all_universal_failure_labelled_rows": sorted(map(word, quotient_survivors)),
        },
        "literal_alias_m_equals_t": {
            "proper_labelled_rows": alias_count,
            "complete_cap_lifts": alias_lifts,
            "palette_changing_complete_lifts": alias_changing,
            "rows_without_any_palette_changing_lift": len(alias_survivors),
        },
        "scope": "Local edge arithmetic only; source planarity and minimality are paper obligations.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    args = parser.parse_args()
    result = json.loads(json.dumps(build(args.seed)))
    if args.check:
        saved = json.loads(args.certificate.read_text())
        if saved != result:
            raise SystemExit("FAIL: certificate differs from independent complete local replay")
    else:
        args.certificate.write_text(json.dumps(result, indent=2) + "\n")
    summary = {key: result[key] for key in (
        "proper_labelled_face_rows", "simultaneous_identification_slice",
        "literal_alias_m_equals_t")}
    summary["simultaneous_identification_slice"].pop("all_universal_failure_labelled_rows")
    print(json.dumps({"status": "PASS", "seed": args.seed, **summary}, indent=2))


if __name__ == "__main__":
    main()
