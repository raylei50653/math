#!/usr/bin/env python3
"""Exact degree-six n expansion, retaining every original private vertex."""
from pathlib import Path
from itertools import product
import argparse
import gzip
import hashlib
import importlib.util
import json

D = Path(__file__).resolve().parent
SOURCE = D.parent / "frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c"
spec = importlib.util.spec_from_file_location("frozen_w5_interface", SOURCE / "interface/check.py")
up = importlib.util.module_from_spec(spec)
spec.loader.exec_module(up)
m = up.m
RIM = ("a", "z", "u2", "u1", "L", "q", "c", "s", "v", "w", "t")


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def compute():
    path = SOURCE / "interface/certificate-v4.json.gz"
    parent = json.load(gzip.open(path, "rt"))
    parent_live = set(parent["live"])
    states = [t for t in m.growth(11, four=True) if m.proper(t)]
    index = {t: i for i, t in enumerate(states)}
    assert [tuple(c["core"]) for c in parent["caps"]] == states
    caps = []
    zero = set()
    matrices = {name: [[0] * len(states) for _ in m.ROWS]
                for name in ("G", "Q1", "J1", "C0", "C1")}
    for i, state in enumerate(states):
        a, z, u2, u1, L, q, c, s, v, w, t = state
        right = [tuple(x) for x in parent["caps"][i]["right_xyr"]]
        nlifts = [(n, index[m.canonical((a, n, u2, u1, L, q, c, s, v, w, t))])
                  for n in range(4) if n not in (a, z, u2)]
        assert nlifts
        bad_lifts = [(n, j) for n, j in nlifts if j not in parent_live]
        if bad_lifts:
            zero.add(i)
        lifts = {name: [] for name in matrices}
        for n, _ in nlifts:
            for b, p, h, R in product(range(4), repeat=4):
                if (b not in (a, c, q, p) and p not in (a, q, n, h)
                        and h not in (q, L, R, n) and R not in (n, u2, u1, L)):
                    lifts["G"].append((b, p, h, R, n))
            for b, R in product(range(4), repeat=2):
                if b not in (a, c, q) and R not in (n, u2, u1, L):
                    if b == n and R == q:
                        lifts["Q1"].append((b, R, n))
                    if b == L and a != R:
                        lifts["J1"].append((b, R, n))
        if L not in (a, c, q):
            if u1 == a:
                lifts["C0"].append((L,))
            if u2 == a:
                lifts["C1"].append((L,))
        for name, values in lifts.items():
            for lift in values:
                b = lift[0]
                for x, y, r in right:
                    row = m.ROWS.index("".join(map(str, m.canonical((x, y, a, b, c)))))
                    matrices[name][row][i] += 1
        caps.append({
            "core": state, "n_lifts": nlifts, "zero_n_lifts": bad_lifts,
            "right_xyr": right, "left": lifts,
        })
    K = up.old.kempe(11, states)
    live, rounds = m.close(K, set(range(len(states))) - zero)
    # The possible extra original z contacts are tested conditionally.
    # They are NOT assumed present and no surviving case is called realized.
    chord_profiles = []
    for target in RIM[3:]:
        j = RIM.index(target)
        restricted = {i for i in live if states[i][1] != states[i][j]}
        clive, crounds = m.close(K, restricted)
        chord_profiles.append({
            "present_chord": ["z", target], "live_ids": clive,
            "deletion_rounds": crounds,
            "source_positive_rows_survive": [
                any(matrices["G"][j][i] for i in clive) for j in (0, 2, 3, 5, 7, 8, 9)
            ],
        })
    candidates = []
    for name in ("C0", "C1"):
        candidates.append({
            "name": name, "completed_k_delta": -6,
            "negative_live_ids": {
                m.ROWS[j]: [i for i in live if matrices[name][j][i]]
                for j in (1, 4, 6)
            },
        })
    return {
        "status": "conditional n-degree-six necessary interface",
        "source_interface_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "rim": RIM, "states": len(states), "caps": caps,
        "initial_zero": sorted(zero), "live": live, "deletion_rounds": rounds,
        "kempe_columns_sha256": hashlib.sha256(packed(K["columns"])).hexdigest(),
        "matrices_sha256": hashlib.sha256(packed(matrices)).hexdigest(),
        "candidates": candidates, "conditional_chords": chord_profiles,
        "source_positive_rows_survive": [
            any(matrices["G"][j][i] for i in live) for j in (0, 2, 3, 5, 7, 8, 9)
        ],
        "source_excluded": False, "all_n_ge_6_closed": False,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--certificate", type=Path, default=D / "n6-certificate.json.gz")
    args = ap.parse_args()
    data = json.loads(packed(compute()))
    if args.build:
        with args.certificate.open("xb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as out:
                out.write(packed(data) + b"\n")
    else:
        assert data == json.load(gzip.open(args.certificate, "rt"))
    print(json.dumps({
        "status": data["status"],
        "initial_zero": len(data["initial_zero"]), "live": len(data["live"]),
        "source_positive_rows_survive": data["source_positive_rows_survive"],
        "candidates": [{k: ({z: len(v) for z, v in value.items()}
                            if k == "negative_live_ids" else value)
                        for k, value in candidate.items()}
                       for candidate in data["candidates"]],
        "conditional_chords": [
            {"chord": p["present_chord"], "live": len(p["live_ids"]),
             "source_positive_rows_survive": p["source_positive_rows_survive"]}
            for p in data["conditional_chords"]
        ],
        "source_excluded": False, "all_n_ge_6_closed": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
