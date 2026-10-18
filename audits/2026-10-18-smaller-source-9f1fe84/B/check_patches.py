#!/usr/bin/env python3
"""Exact fixed-rim 0/1-inner replacement families; no source search."""
import argparse
import hashlib
import itertools as it
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "9f1fe84f73aabfa87a33d28754633bae6bf0b707"


def edge(a, b):
    return tuple(sorted((a, b)))


def rim(n):
    return {edge(i, (i + 1) % n) for i in range(n)}


def edges_of(faces):
    return {edge(a, b) for f in faces for a, b in zip(f, f[1:] + f[:1])}


@lru_cache(None)
def polygon_faces(p):
    if len(p) < 3:
        return ((),)
    return tuple(sorted({tuple(sorted(l + r + ((p[0], p[i], p[-1]),)))
                         for i in range(1, len(p) - 1)
                         for l in polygon_faces(p[:i + 1])
                         for r in polygon_faces(p[i:])}))


def one_inner_faces(n):
    out = set()
    for degree in range(3, n + 1):
        for neighbours in it.combinations(range(n), degree):
            core, sectors = [], []
            for a, b in zip(neighbours, neighbours[1:] + neighbours[:1]):
                arc, t = [a], a
                while t != b:
                    t = (t + 1) % n
                    arc.append(t)
                core.append((a, b, n))
                sectors.append(polygon_faces(tuple(arc)))
            for choices in it.product(*sectors):
                out.add(tuple(sorted(tuple(core) + sum(choices, ()))))
    return tuple(sorted(out))


def rotation(faces, n, vertices):
    # The reversed outer face makes a sphere rotation, with every dart once.
    all_faces = list(faces) + [tuple(reversed(range(n)))]
    successor = {v: {} for v in range(vertices)}
    darts = set()
    for f in all_faces:
        for j, v in enumerate(f):
            a, b = f[j - 1], f[(j + 1) % len(f)]
            assert a not in successor[v]
            successor[v][a] = b
            assert (v, b) not in darts
            darts.add((v, b))
    result = []
    for v in range(vertices):
        todo = successor[v]
        assert todo
        first, order = min(todo), []
        t = first
        while not order or t != first:
            assert t not in order
            order.append(t)
            t = todo[t]
        assert set(order) == set(todo)
        result.append(order)
    assert all((b, a) in darts for a, b in darts)
    assert vertices - len(darts) // 2 + len(all_faces) == 2
    return result


def normal(t):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in t)


def rows(n):
    return sorted({normal(t) for t in it.product(range(4), repeat=n)
                   if all(t[a] != t[b] for a, b in rim(n))})


def fibres(es, rs, inner):
    return [[list(q) for q in it.product(range(4), repeat=inner)
             if all((t + q)[a] != (t + q)[b] for a, b in es)] for t in rs]


def support(fs):
    return {i for i, fibre in enumerate(fs) if fibre}


def cap(n):
    # n=5 has centre degrees 4,5; n=6 has centre degrees 5,5.
    split = n - 3
    u, h = n, n + 1
    faces = [(u, i, i + 1) for i in range(split)]
    faces += [(u, split, h), (u, h, 0)]
    faces += [(h, i, (i + 1) % n) for i in range(split, n)]
    faces = tuple(sorted(faces))
    return {"vertices": list(range(n + 2)), "rim": list(range(n)),
            "faces": faces, "edges": sorted(edges_of(faces)),
            "rotation": rotation(faces, n, n + 2)}


def family(n, inner, rs, target):
    triangulations = polygon_faces(tuple(range(n))) if inner == 0 else one_inner_faces(n)
    maxima, candidates = [], {}
    for index, fs in enumerate(triangulations):
        es = edges_of(fs)
        maxima.append({"faces": fs, "rotation": rotation(fs, n, n + inner)})
        optional = sorted(es - rim(n))
        for bits in it.product((0, 1), repeat=len(optional)):
            sub = tuple(sorted(rim(n) | {e for e, b in zip(optional, bits) if b}))
            candidates.setdefault(sub, index)
    output, accepted, covered = [], 0, set()
    for es, completion in sorted(candidates.items()):
        ff = fibres(es, rs, inner)
        ss = support(ff)
        sound = ss <= target
        leaks = sorted(ss - target)
        if sound:
            accepted += 1
            covered |= ss
        output.append({"edges": es, "completion": completion, "fibres": ff,
                       "sound": sound, "first_leak": leaks[0] if leaks else None})
    return {"inner_vertices": inner, "maximal_patches": maxima, "patches": output,
            "summary": {"maximal_count": len(maxima), "count": len(output),
                        "sound_count": accepted, "covered_rows": sorted(covered)}}


def build():
    result = {"base": BASE,
              "domain": "simple plane patches with fixed labelled cycle rim and at most one inner vertex",
              "encoding": "All proper canonical boundary rows and complete private fibres. Improper rim tuples have empty fibre. Expand each row and its whole lift by the same S4 permutation; duplicate expanded lifts are sets.",
              "source_realization": "not triggered", "disks": {}}
    for n in (5, 6):
        rs, original = rows(n), cap(n)
        ff = fibres(original["edges"], rs, 2)
        original["fibres"] = ff
        target = support(ff)
        fs = [family(n, k, rs, target) for k in (0, 1)]
        result["disks"][str(n)] = {"rows": rs, "cap": original, "families": fs}
    five = result["disks"]["5"]
    assert sum(1 << i for i in support(five["cap"]["fibres"])) == 567
    assert [(x["summary"]["count"], x["summary"]["sound_count"])
            for x in five["families"]] == [(11, 1), (212, 16)]
    assert all(x["summary"]["covered_rows"] == [2, 4, 5, 9] for x in five["families"])
    for fam in five["families"]:
        for p in fam["patches"]:
            assert p["sound"] == ({(1, 3), (1, 4)} <= set(p["edges"]))
    six = result["disks"]["6"]
    assert [(x["summary"]["count"], x["summary"]["sound_count"])
            for x in six["families"]] == [(45, 0), (1148, 0)]
    # Explicit smaller cap and total same-rim lift function.
    fan = rim(5) | {(1, 3), (1, 4)}
    maps = []
    for beta in it.product(range(4), repeat=5):
        if not all(beta[a] != beta[b] for a, b in fan):
            continue
        h = beta[1]
        u = min(set(range(4)) - set(beta[:3]))
        lifted = beta + (u, h)
        assert all(lifted[a] != lifted[b] for a, b in five["cap"]["edges"])
        maps.append({"rim": beta, "centres": (u, h)})
    result["fan_lift_all_literal_rows"] = maps
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    if bool(args.write) == bool(args.check):
        parser.error("exactly one of --write / --check required")
    expected = json.loads(json.dumps(build()))
    if args.write:
        with args.write.open("x") as f:
            json.dump(expected, f, separators=(",", ":"), sort_keys=True)
            f.write("\n")
    else:
        actual = json.loads(args.check.read_text())
        if actual != expected:
            raise SystemExit("REJECT: incomplete or incorrect patch certificate")
    print(json.dumps({"status": "PASS", "source_realization": "not triggered",
                      "families": {n: [x["summary"] for x in d["families"]]
                                   for n, d in expected["disks"].items()},
                      "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                     sort_keys=True))


if __name__ == "__main__":
    main()
