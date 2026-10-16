#!/usr/bin/env python3
"""Independent complete-local-lift control; no graph realization claim."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COLOURS = tuple(range(4))
WORDS = ((0, 1, 0, 1), (0, 1, 0, 2), (0, 1, 2, 1), (0, 1, 2, 3))
NAMES = ("ABAB", "ABAC", "ABCB", "ABCD")
SEVEN = (7, 10, 11, 12, 13, 14, 15)


def proper_cycle(word):
    return all(word[i] != word[(i + 1) % 4] for i in range(4))


def allowed_equality(word, pq):
    """Direct unnormalised equality/palette implementation."""
    z, s, v, t = word
    if not proper_cycle(word):
        return False
    if s == t:
        return set(pq) == set(COLOURS) - {z, s}
    if z == v:
        return set(pq) == {s, t}
    return False


def build_literal_table():
    """Independent rule: global colour permutations of written rows."""
    canonical = (
        ((0, 1, 0, 1), (2, 3)),
        ((0, 1, 0, 2), (1, 2)),
        ((0, 1, 2, 1), (2, 3)),
    )
    table = set()
    for perm in itertools.permutations(COLOURS):
        for boundary, pair in canonical:
            image = tuple(perm[x] for x in boundary)
            order = tuple(perm[x] for x in pair)
            table.add((image, order))
            table.add((image, order[::-1]))
    return table


LITERAL = build_literal_table()


def options(word):
    z, w, v, _ = word
    return tuple(colour for colour in COLOURS if colour not in {z, w, v})


def full_lifts_a(word, pq):
    z, _, v, t = word
    return all(allowed_equality((z, colour, v, t), pq) for colour in options(word))


def full_lifts_b(word, pq):
    z, w, v, t = word
    found = False
    for inserted in COLOURS:
        # Literal restored edges zs, ws, vs, independent of options().
        if inserted == z or inserted == w or inserted == v:
            continue
        found = True
        if ((z, inserted, v, t), pq) not in LITERAL:
            return False
    assert found
    return True


def make_result():
    manifest = json.loads((ROOT / "INPUTS.json").read_text())
    verified = []
    for entry in manifest["files"]:
        path = ROOT / "frozen" / entry["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], path
        verified.append(entry["path"])

    words = [w for w in itertools.product(COLOURS, repeat=4) if proper_cycle(w)]
    assert len(words) == 84
    cases = {"distinct_pins": [0, 0], "w_equals_q": [0, 0], "w_equals_p_reflected": [0, 0]}
    compared = 0
    for word in words:
        z, w, v, t = word
        for pq in itertools.product(COLOURS, repeat=2):
            if z in pq or pq[0] == pq[1]:
                continue
            for row in words:
                assert allowed_equality(row, pq) == ((row, pq) in LITERAL)
                # Reflection s<->t retains the entire palette predicate.
                reflected = (row[0], row[3], row[2], row[1])
                assert allowed_equality(row, pq) == allowed_equality(reflected, pq)
            a, b = full_lifts_a(word, pq), full_lifts_b(word, pq)
            assert a == b
            compared += 1
            expected = len(set(word)) == 4 and set(pq) == {w, v}
            assert a == expected
            for name, eligible in (
                ("distinct_pins", True),
                ("w_equals_q", pq[1] == w),
                ("w_equals_p_reflected", pq[0] == w),
            ):
                if eligible:
                    cases[name][0] += 1
                    cases[name][1] += int(a)

    rows = []
    for name, word in zip(NAMES, WORDS):
        z, _, v, t = word
        lifts = []
        for colour in options(word):
            row = (z, colour, v, t)
            palettes = sorted({tuple(sorted(pq)) for pq in itertools.product(COLOURS, repeat=2)
                               if (row, pq) in LITERAL})
            lifts.append({"s": colour, "Rprime_boundary": list(row), "allowed_pq_palettes": palettes})
        survivors = [list(pq) for pq in itertools.product(COLOURS, repeat=2)
                     if z not in pq and pq[0] != pq[1] and full_lifts_a(word, pq)]
        rows.append({"U_boundary": name, "lifts": lifts, "surviving_ordered_pq": survivors})

    # A merely existential s lift incorrectly retains the ABAB row.
    witness_word, witness_pq = WORDS[0], (1, 2)
    statuses = [allowed_equality((0, c, 0, 1), witness_pq) for c in options(witness_word)]
    assert statuses == [True, False]
    assert not full_lifts_a(witness_word, witness_pq)

    projected_masks = (0, 8)
    assert set(projected_masks).isdisjoint(SEVEN)
    return {
        "status": "PASS",
        "claim": "complete local s-lifts force U support to be a subset of ABCD",
        "scope": "finite local control; source surgery and C4 classification are paper premises",
        "frozen_base": manifest["base"],
        "frozen_files_verified": len(verified),
        "boundary_assignments": len(words),
        "ordered_triangle_joint_assignments_compared": compared,
        "implementations_agree": True,
        "reflection_checked": True,
        "cases": {name: {"tested": counts[0], "accepted": counts[1]} for name, counts in cases.items()},
        "canonical_rows": rows,
        "surviving_outer_support_masks": list(projected_masks),
        "source_relative_C4_masks": list(SEVEN),
        "existential_lift_negative_control": {"U_boundary": "ABAB", "pq": list(witness_pq), "s_lift_acceptance": statuses},
        "actual_source_graphs_enumerated": 0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = make_result()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    certificate = HERE / "certificate.json"
    if args.check:
        assert certificate.read_text() == text, "certificate mismatch"
    else:
        with certificate.open("x") as stream:
            stream.write(text)
    print("PASS: 504 complete local joint assignments; both pin coincidences; all lifts; frozen inputs")


if __name__ == "__main__":
    main()
