#!/usr/bin/env python3
"""Independent r6 review by literal cap edges, including empty r fibres."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
D4 = HERE.parent / "degree4"
C = set(range(4))


def canonical(row):
    seen = []
    result = []
    for colour in row:
        if colour not in seen:
            seen.append(colour)
        result.append(seen.index(colour))
    return tuple(result)


def proper_boundary(row):
    return all(row[i] != row[(i + 1) % 5] for i in range(5))


def cap_ok(z, s, r, t, p, q):
    # Check all 16 actual original x,y lifts directly, without the old table.
    for x, y in itertools.product(range(4), repeat=2):
        if x not in (z, s, r) and y not in (z, r, t) and x != y:
            if {x, y} != {p, q}:
                return False
    # The extra actual-source Kempe theorem for cap-empty ABCB fibres.
    if s == t and z != r and not ({p, q} & (C - {z, s, r, t})):
        return False
    return True


def once(row):
    z, s, v, w, t, p, q = row
    if not proper_boundary(row[:5]) or z in (p, q) or p == q:
        return False
    return all(cap_ok(z, s, r, t, p, q) for r in C - {s, v, w, t})


def twice_internal(row):
    z, s, v, w, h, p, q = row
    if not proper_boundary(row[:5]) or z in (p, q) or p == q:
        return False
    return all(cap_ok(z, s, r, t, p, q)
               for t in C - {z, w, h}
               for r in C - {s, v, w, t})


def twice_promoted(row):
    z, s, v, w, p, q = row
    if not proper_boundary(row[:5]) or z in (p, q) or p == q:
        return False
    return all(cap_ok(z, s, r, t, p, q)
               for t in C - {z, w, p}
               for r in C - {s, v, w, t})


def make_result():
    blob = (D4 / "cells.json").read_bytes()
    digest = hashlib.sha256(blob).hexdigest()
    assert digest == "04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8"
    catalogue = json.loads(blob)
    patterns = [tuple(row) for row in catalogue["pattern_order"]]
    masks = sorted(map(int, catalogue["cells"]))
    assert len(masks) == 132
    results = {}
    for label, predicate, count in (
        ("delete_r", once, 7),
        ("delete_r_t_keep_pq_internal", twice_internal, 7),
        ("delete_r_t_promote_p", twice_promoted, 6),
    ):
        accepted = [row for row in itertools.product(range(4), repeat=count) if predicate(row)]
        rows = []
        upper = 0
        for index, boundary in enumerate(patterns):
            tail = [list(tail) for tail in itertools.product(range(4), repeat=count - 5)
                    if predicate(boundary + tail)]
            if tail:
                upper |= 1 << index
            rows.append({"boundary": list(boundary), "tails": tail})
        results[label] = {
            "all_labelled_assignments_tested": 4 ** count,
            "accepted_labelled_assignments": len(accepted),
            "canonical_rows": rows,
            "upper_outer_mask": upper,
            "catalogue_submasks": [mask for mask in masks if not mask & ~upper],
        }
        if label == "delete_r":
            transfer = json.loads((D4 / "transfer.json").read_text())
            assert upper == transfer["allowed_outer_mask"] == 319
            assert len(accepted) == transfer["labelled_rows"] == 624
            names = {"".join("ABCD"[x] for x in canonical(row)) for row in accepted}
            assert names == set(transfer["orbits"])
            results[label]["agrees_with_transfer_certificate"] = True
            zero = [row for row in accepted if not C - set(row[1:5])]
            assert len(zero) == 288
            results[label]["accepted_zero_r_lift_assignments"] = len(zero)
    assert results["delete_r"]["catalogue_submasks"] == [271, 314, 319]
    general = results["delete_r_t_keep_pq_internal"]
    assert general["upper_outer_mask"] == 575
    assert general["catalogue_submasks"] == [564, 567, 572, 575]
    special = results["delete_r_t_promote_p"]
    assert special["upper_outer_mask"] == 542 and special["catalogue_submasks"] == []

    # The paper Kempe argument removes boundary bit 9 from the general case.
    after = general["upper_outer_mask"] & ~(1 << 9)
    assert after == 63
    assert not any(not mask & ~after for mask in masks)
    return {
        "status": "PASS",
        "method": "literal cap x,y edges plus frozen ABCB missing-colour theorem; all r,t lifts",
        "empty_r_fibres_are_kept": True,
        "catalogue_sha256": digest,
        "results": results,
        "paper_removes_ABCDC": {"outer_upper_mask_after_removal": after, "catalogue_submasks": []},
        "actual_source_graphs_enumerated": 0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = make_result()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    path = HERE / "r6-certificate.json"
    if args.check:
        assert path.read_text() == text
    else:
        with path.open("x") as stream:
            stream.write(text)
    print("PASS: independent literal-cap screens 319/575/542, 288 retained zero-r-lift rows, final 63 has no catalogue submask")


if __name__ == "__main__":
    main()
