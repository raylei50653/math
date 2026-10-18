#!/usr/bin/env python3
"""Exhaust the named zero/one-centre noncrossing hexagon operation family.

This is an independent finite patch calculation, not enumeration of sources.
No graph library and no unbounded-source existence hypothesis is used here.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERT = HERE / "hexagon_obstruction.json"
COLORS = range(4)
RIM = tuple((i, (i + 1) % 6) for i in range(6))
DIAGS = tuple((i, j) for i in range(6) for j in range(i + 1, 6)
              if j - i not in (1, 5))
ROWS = ("01232", "01021", "01202", "01212")


def crosses(a, b):
    i, j = a
    k, ell = b
    return i < k < j < ell or k < i < ell < j


def encode(t):
    return sum(c * 4 ** i for i, c in enumerate(t))


def old_fibre(t):
    """Actual rim (a,b,q,u1,u2,n); centres (p,h)."""
    a, b, q, u1, u2, n = t
    return tuple((p, h) for p, h in itertools.product(COLORS, repeat=2)
                 if p != h and p not in (a, b, q, n)
                 and h not in (q, u1, u2, n))


def shapes():
    for ds in itertools.combinations(DIAGS, 3):
        if not any(crosses(x, y) for x, y in itertools.combinations(ds, 2)):
            yield (), ds
    for ns in range(3, 7):
        for spokes in itertools.combinations(range(6), ns):
            for ds in itertools.combinations(DIAGS, 6 - ns):
                if any(crosses(x, y) for x, y in itertools.combinations(ds, 2)):
                    continue
                # A chord cannot separate two neighbours of the centre.
                if any(any(a < x < b for x in spokes)
                       and any(x < a or x > b for x in spokes)
                       for a, b in ds):
                    continue
                yield spokes, ds


def compute():
    tuples = tuple(t for t in itertools.product(COLORS, repeat=6)
                   if all(t[i] != t[j] for i, j in RIM))
    fibres = {t: old_fibre(t) for t in tuples}
    old = {t for t in tuples if fibres[t]}
    candidates = []
    shape_counts = {"0": 0, "1": 0}
    family_counts = {"0": 0, "1": 0}
    nonempty = {"0": 0, "1": 0}
    for spokes, ds in shapes():
        typ = str(bool(spokes) * 1)
        shape_counts[typ] += 1
        for equals in itertools.product((False, True), repeat=len(ds)):
            family_counts[typ] += 1
            support = tuple(t for t in tuples
                            if all((t[a] == t[b]) == eq
                                   for (a, b), eq in zip(ds, equals))
                            and (not spokes or len({t[i] for i in spokes}) <= 3))
            leak = next((t for t in support if t not in old), None)
            if support:
                nonempty[typ] += 1
                assert leak is not None
            candidates.append({"private_vertices": int(typ), "spokes": spokes,
                               "diagonals": ds, "equality_flags": equals,
                               "support": [encode(t) for t in support],
                               "leak": leak})
    # The two pinned rejected contexts cover every S4 orbit of rim tuples.
    orbit_cover = []
    for t in tuples:
        a, b, q, *_ = t
        if q == a:
            mapping = {a: 0, b: 2}
            other = sorted(set(COLORS) - {a, b})
            mapping.update(zip(other, (1, 3)))
            row = "01021"
        else:
            mapping = {a: 2, b: 0, q: 1}
            mapping[next(iter(set(COLORS) - {a, b, q}))] = 3
            row = "01202"
        renamed = tuple(mapping[x] for x in t)
        ra, rb, rc = map(int, row[2:])
        assert renamed[0] == ra and renamed[1] == rb and renamed[2] != rc
        assert bool(old_fibre(renamed)) == bool(old_fibre(t))
        orbit_cover.append([encode(t), row, encode(renamed),
                            [mapping[c] for c in COLORS]])
    fan = {t for t in tuples if all(t[0] != t[j] for j in (2, 3, 4))}
    contexts = {}
    for row in ROWS:
        a, b, c = map(int, row[2:])
        ambient = {t for t in tuples if t[0] == a and t[1] == b and t[2] != c}
        good = ambient & old
        new = ambient & fan
        contexts[row] = {"old_count": len(good), "new_count": len(new),
                         "retained_count": len(good & new),
                         "leaks": sorted(new - good), "lost": sorted(good - new)}
    return {"schema": 1, "boundary": ["a", "b", "q", "u1", "u2", "n"],
            "patch_centres": ["p", "h"], "shape_counts": shape_counts,
            "candidate_counts": family_counts, "nonempty_counts": nonempty,
            "proper_rim_count": len(tuples), "old_support_count": len(old),
            "old_fibres": [[encode(t), fibres[t]] for t in tuples],
            "candidates": candidates, "two_rejection_orbit_cover": orbit_cover,
            "fan_contexts": contexts,
            "larger_named_patches": larger_named_patches(tuples, candidates)}


def larger_named_patches(tuples, small_candidates):
    patches = {
        "triangle_three_centres": {
            "edges": ((0, 1), (1, 2), (0, 2)),
            "neighbours": ((0, 1, 2), (2, 3, 4), (4, 5, 0))},
        "diamond_four_centres": {
            "edges": ((0, 1), (1, 2), (2, 3), (3, 0), (0, 2)),
            "neighbours": ((0, 1), (1, 2, 3), (3, 4), (4, 5, 0))}}
    two_centres = []
    for spokes, ds in shapes():
        if not spokes:
            continue
        for i, j in itertools.combinations(range(len(spokes)), 2):
            xs, ys = spokes[i:j + 1], spokes[j:] + spokes[:i + 1]
            for equals in itertools.product((False, True), repeat=len(ds)):
                support = []
                for t in tuples:
                    if not all((t[a] == t[b]) == e for (a, b), e in zip(ds, equals)):
                        continue
                    lx = set(COLORS) - {t[a] for a in xs}
                    ly = set(COLORS) - {t[a] for a in ys}
                    if any(x != y for x in lx for y in ly):
                        support.append(encode(t))
                two_centres.append({"x_neighbours": xs, "y_neighbours": ys,
                                    "diagonals": ds, "equality_flags": equals,
                                    "support": support})
    for name, data in patches.items():
        n = len(data["neighbours"])
        cs = tuple(c for c in itertools.product(COLORS, repeat=n)
                   if all(c[i] != c[j] for i, j in data["edges"]))
        fibres = {encode(t): tuple(c for c in cs
                                  if all(c[i] not in {t[j] for j in neighbours}
                                         for i, neighbours in enumerate(data["neighbours"])))
                  for t in tuples}
        good = {key for key, value in fibres.items() if value}
        leaks = []
        for family in (small_candidates, two_centres):
            witnesses = []
            for candidate in family:
                leak = next((key for key in candidate["support"] if key not in good), None)
                assert not candidate["support"] or leak is not None, name
                witnesses.append(leak)
            leaks.append(witnesses)
        data["full_fibres"] = sorted(fibres.items())
        data["support_count"] = len(good)
        data["leak_witnesses_by_family"] = leaks
    return {"two_centre_candidates": two_centres, "patches": patches}


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    result = compute()
    data = encoded(result)
    if args.write:
        with CERT.open("xb") as output:
            output.write(data)
    else:
        assert CERT.read_bytes() == data, "finite patch certificate mismatch"
    if args.negative_control:
        # A tempting smaller fan has genuine local leaks: the checker must
        # reject the claim that every retained tuple extends to p,h.
        a_fan = next(c for c in result["candidates"]
                     if c["private_vertices"] == 0
                     and c["diagonals"] == ((0, 2), (0, 3), (0, 4))
                     and not any(c["equality_flags"]))
        assert a_fan["leak"] is not None
        assert not old_fibre(tuple(a_fan["leak"]))
        changed = json.loads(data)
        changed["fan_contexts"]["01202"]["leaks"] = []
        assert encoded(changed) != data
        print("PASS: fan soundness claim and erased rejection leaks are rejected")
    print(json.dumps({key: result[key] for key in
                      ("shape_counts", "candidate_counts", "nonempty_counts",
                       "proper_rim_count", "old_support_count")}, sort_keys=True))
    print("sha256=" + hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
