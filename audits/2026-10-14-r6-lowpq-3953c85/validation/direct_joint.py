#!/usr/bin/env python3
"""Independent finite arithmetic; no imports from the main local checker.

This does not decide realizability of a complete source. All assignments
to the two actual faces are kept, including empty cap-lift cells.
"""
import itertools
import json

C = range(4)
PINS = ("z", "s", "v", "w", "t", "q", "ell", "m")
EDGES = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
         (0, 5), (5, 6), (6, 7), (7, 0))


def norm(row):
    seen = {}
    return tuple(seen.setdefault(c, len(seen)) for c in row)


def word(row):
    return "".join("ABCD"[c] for c in row)


def retained_joint(z, s, r, t, p, q):
    if z == r:
        return s == t and {p, q} == set(C) - {z, s}
    if s == t:
        return bool({p, q} & (set(C) - {z, s, r}))
    return {p, q} == {s, t}


def build():
    rows = []
    labelled = 0
    for f in itertools.product(C, repeat=8):
        if any(f[i] == f[j] for i, j in EDGES):
            continue
        labelled += 1
        if f != norm(f):
            continue
        z, s, v, w, t, q, ell, m = f
        rp, rp_bad, full, target = [], [], [], []
        for r, p in itertools.product(C, repeat=2):
            if r in (s, v, w, t) or p in (z, q, ell, m):
                continue
            rp.append([r, p])
            if not retained_joint(z, s, r, t, p, q):
                rp_bad.append([r, p])
            for x, y in itertools.product(C, repeat=2):
                if x in (z, s, r) or y in (z, r, t) or x == y:
                    continue
                full.append([r, p, x, y])
                if {x, y} != {p, q}:
                    target.append([r, p, x, y])
        if not rp_bad:
            assert not target
        rows.append({"pins": word(f), "rp_lifts": rp,
                     "forbidden_joint_lifts": rp_bad,
                     "full_rpxy_lifts": full, "target_lifts": target,
                     "necessary_survivor": not rp_bad})
    survivors = [row for row in rows if row["necessary_survivor"]]
    slices = {
        "s=w,z=ell": [r["pins"] for r in survivors
                       if r["pins"][1] == r["pins"][3]
                       and r["pins"][0] == r["pins"][6]],
        "v=t,z=ell": [r["pins"] for r in survivors
                       if r["pins"][2] == r["pins"][4]
                       and r["pins"][0] == r["pins"][6]],
    }
    assert labelled == 5040 and len(rows) == 210
    assert len(survivors) == 120
    assert slices["s=w,z=ell"] == ["ABABCBAD", "ABABCCAD"]
    assert slices["v=t,z=ell"] == ["ABCACBAD", "ABCACCAD"]
    return {"scope": "fixed two-face local arithmetic, not source realization",
            "pins": PINS, "proper_labelled_rows": labelled,
            "proper_orbits": len(rows), "necessary_orbits": len(survivors),
            "slices": slices, "rows": rows}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
