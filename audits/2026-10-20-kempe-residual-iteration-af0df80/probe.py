#!/usr/bin/env python3
"""Active distinguishing probes followed by inverse restoration, fixed cell95."""
import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "frozen/audits/2026-10-20-multi-kempe-machines-af0df80/experiment/certificate.json"


def generate():
    raw = SOURCE.read_bytes()
    d = json.loads(raw)
    colors, actions, trans = d["all_colorings"], d["actions"], d["transitions"]
    obs = [tuple(j) for j in d["joint_monitor_rows"]]
    fibres = defaultdict(list)
    for i, j in enumerate(obs):
        fibres[j].append(i)

    def shortest(left, right):
        pending = deque([(left, right, ())])
        seen = {(left, right)}
        while pending:
            l, r, path = pending.popleft()
            assert obs[l] == obs[r]
            for a in range(len(actions)):
                ll, rr = trans[l][a], trans[r][a]
                assert (ll < 0) == (rr < 0)
                if ll < 0:
                    continue
                if obs[ll] != obs[rr]:
                    return path + (a,)
                if (ll, rr) not in seen:
                    seen.add((ll, rr))
                    pending.append((ll, rr, path + (a,)))
        raise AssertionError("An inseparable doubleton was encountered")

    records = []
    histogram = Counter()
    for joint, ids in sorted(fibres.items()):
        if len(ids) == 1:
            continue
        assert len(ids) == 2
        word = shortest(*ids)
        histogram[len(word)] += 1
        schedule = word + word[::-1]
        runs = []
        for initial in ids:
            current = initial
            residual = set(ids)
            trace = []
            for a in schedule:
                current = trans[current][a]
                assert current >= 0
                residual = {trans[c][a] for c in residual
                            if trans[c][a] >= 0 and obs[trans[c][a]] == obs[current]}
                assert current in residual
                trace.append({"action": actions[a], "actual": colors[current],
                              "joint_observation": obs[current],
                              "residual_lifts": [colors[c] for c in sorted(residual)]})
            assert current == initial and residual == {initial}
            assert len(trace[len(word) - 1]["residual_lifts"]) == 1
            runs.append({"initial_actual": colors[initial], "trace": trace,
                         "restored_actual": colors[current],
                         "final_residual": [colors[c] for c in sorted(residual)]})
        records.append({"initial_joint": joint,
                        "initial_lifts": [colors[i] for i in ids],
                        "shortest_probe_actions": [actions[a] for a in word],
                        "probe_length": len(word), "round_trip_length": len(schedule),
                        "actual_branches": runs})
    assert len(records) == 72 and sum(histogram.values()) == 72
    return {
        "scope": "All72 doubleton J-fibres of fixed cell95; original roots; literal colors.",
        "source_sha256": sha256(raw).hexdigest(),
        "initial_singletons_need_no_probe": sum(len(ids) == 1 for ids in fibres.values()),
        "doubleton_fibres": len(records),
        "shortest_probe_length_histogram": dict(sorted(histogram.items())),
        "complete_actual_branches": sum(len(r["actual_branches"]) for r in records),
        "maximum_scheme_round_trip_length": max(r["round_trip_length"] for r in records),
        "round_trip_optimality_claimed": False,
        "probe_restore_records": records,
        "j1_source_status": "not triggered",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument("--generate", action="store_true")
    modes.add_argument("--check", action="store_true")
    p.add_argument("--certificate", type=Path, default=HERE / "probe.json")
    args = p.parse_args()
    result = generate()
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    if args.generate:
        with args.certificate.open("xb") as f:
            f.write(raw)
    elif args.certificate.read_bytes() != raw:
        raise SystemExit("FAIL: probe certificate differs from reconstruction")
    print(json.dumps({k: v for k, v in result.items() if k != "probe_restore_records"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
