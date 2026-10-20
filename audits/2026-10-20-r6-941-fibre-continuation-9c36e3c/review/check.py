#!/usr/bin/env python3
"""Independent partition enumeration and complete-fibre transport audit.

This imports no sibling or frozen checker implementation. Frozen live sets
are theorem inputs, not independently re-proved here.
"""
import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

D = Path(__file__).resolve().parent
BASE = D.parent
OLD = BASE / "frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d"
PAIRS = ((0, 1), (0, 2), (0, 3))


def canon(values):
    seen = {}
    return tuple(seen.setdefault(v, len(seen)) for v in values)


def partitions(n, cap=None, prefix=(0,)):
    if len(prefix) == n:
        yield prefix
        return
    largest = max(prefix) + 1
    if cap is not None:
        largest = min(largest, cap - 1)
    for value in range(largest + 1):
        yield from partitions(n, cap, prefix + (value,))


def proper(u):
    return all(u[i] != u[(i + 1) % len(u)] for i in range(len(u)))


def noncrossing(p):
    return not any(p[a] == p[c] and p[b] == p[d] and p[a] != p[b]
                   for a, b, c, d in combinations(range(len(p)), 4))


def swap(u, p, root, pair):
    x, y = pair
    return tuple(y if value == x and p[i] == p[root]
                 else x if value == y and p[i] == p[root]
                 else value for i, value in enumerate(u))


def global23(u):
    return tuple(5 - value if value in (2, 3) else value for value in u)


def allowed(u, pair, all_parts, state_index, live):
    complement = tuple(c for c in range(4) if c not in pair)
    opposite = {pair[0]: pair[1], pair[1]: pair[0],
                complement[0]: complement[1], complement[1]: complement[0]}
    side = tuple(value in pair for value in u)
    changes = sum(side[i] != side[(i + 1) % 10] for i in range(10))
    answer = []
    for p in all_parts:
        blocks = max(p) + 1
        if blocks != changes // 2 + 1:
            continue
        if any(side[i] != side[j] for i in range(10)
               for j in range(i) if p[i] == p[j]):
            continue
        if any(side[i] == side[(i + 1) % 10] and p[i] != p[(i + 1) % 10]
               for i in range(10)):
            continue
        orbit = [state_index[canon(
            opposite[value] if mask & (1 << p[i]) else value
            for i, value in enumerate(u))]
            for mask in range(1 << blocks)]
        if all(index in live for index in orbit):
            answer.append(p)
    return answer


def calculate():
    manifest = json.loads((BASE / "INPUTS.json").read_text())
    for entry in manifest:
        path = BASE / "frozen" / entry["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
    c1 = json.loads((OLD / "J1/certificate.json").read_text())
    c2 = json.loads((OLD / "J2/certificate.json").read_text())
    states = [u for u in partitions(10, 4) if proper(u)]
    assert len(states) == 2461
    index = {u: i for i, u in enumerate(states)}
    all_parts = [p for p in partitions(10) if noncrossing(p)]
    assert len(all_parts) == 16796
    records = []
    j1_parts = {}
    total_j1 = total_j2 = 0
    for rec in c1["component_records"]:
        u = tuple(rec["core"])
        for pair, frozen in zip(PAIRS, rec["splits"]):
            rebuilt = allowed(u, pair, all_parts, index, set(c1["final_live"]))
            assert set(rebuilt) == set(map(tuple, frozen["partitions"]))
            j1_parts[u, pair] = rebuilt
            total_j1 += len(rebuilt)
    for rec in c2["forms"]:
        u = tuple(rec["literal_core"])
        for pair, frozen in zip(PAIRS, rec["pair_records"]):
            rebuilt = allowed(u, pair, all_parts, index, set(c2["live"]))
            assert set(rebuilt) == {
                tuple(row["partition"]) for row in frozen["partitions"]}
            total_j2 += len(rebuilt)
    for rec in c1["component_records"]:
        u = tuple(rec["core"])
        d_target = u[:6] + (5 - u[6],) + u[7:9] + (5 - u[9],)
        for p in j1_parts[u, (0, 1)]:
            assert global23(swap(u, p, 2, (2, 3))) == d_target
            assert global23(swap(d_target, p, 2, (2, 3))) == u
        if u[4] == 0:
            q_target = u[:4] + (3,) + u[5:]
            for p in j1_parts[u, (0, 3)]:
                assert [i for i in range(10) if p[i] == p[4]] == [4]
                assert swap(u, p, 4, (0, 3)) == q_target
            target_blocks = [[i for i in range(10) if p[i] == p[4]]
                             for p in j1_parts[q_target, (0, 3)]]
            assert target_blocks.count([4]) == 1
            assert len(target_blocks) == 3
            if u[6] == 2:
                zero = 7 if u[7] == 0 else 8
                assert {tuple(b) for b in target_blocks} == {
                    (4,), tuple(sorted((4, zero))), tuple(sorted((2, 4, zero)))}
        # Prospective stratum lemma: component-disjoint v,w swap iff s~t.
        separate, joined = [], []
        e_target = u[:7] + (u[8], u[7]) + u[9:]
        for p in j1_parts[u, (0, 1)]:
            assert p[7] == p[8] and p[0] == p[1] == p[5]
            is_separate = p[7] != p[0]
            assert is_separate == (p[6] == p[9])
            result = swap(u, p, 7, (0, 1))
            if is_separate:
                assert result == e_target
                assert swap(result, p, 7, (0, 1)) == u
                separate.append(list(p))
            else:
                assert result != e_target
                joined.append(list(p))
        assert len(separate) == len(joined) == 1
        records.append({"core": list(u), "separate_partition": separate[0],
                        "joined_partition": joined[0]})
    for rec in c2["forms"]:
        if rec["family"] != 3:
            continue
        u = tuple(rec["literal_core"])
        target = u[:6] + (5 - u[6],) + u[7:9] + (5 - u[9],)
        for p in allowed(u, (0, 1), all_parts, index, set(c2["live"])):
            assert global23(swap(u, p, 2, (2, 3))) == target
            assert global23(swap(target, p, 2, (2, 3))) == u
    assert total_j1 == 56
    assert total_j2 == 112
    return {"status": "PASS", "input_files": len(manifest),
            "j1_partition_records": 24, "j1_partitions": total_j1,
            "j2_partition_records": 36, "j2_partitions": total_j2,
            "j1_strata": records,
            "scope": "independent partition reconstruction and transport formulas",
            "upstream_zero_closure": "frozen theorem input",
            "source_realized": False, "last_rejection": "OPEN"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--certificate", type=Path, default=D / "certificate.json")
    args = parser.parse_args()
    out = calculate()
    if args.build:
        with args.certificate.open("x") as stream:
            json.dump(out, stream, indent=2)
            stream.write("\n")
    else:
        assert json.loads(args.certificate.read_text()) == out
    print(json.dumps({key: value for key, value in out.items() if key != "j1_strata"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
