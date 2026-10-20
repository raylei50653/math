#!/usr/bin/env python3
"""Independent common-legal probe and inverse execution on graph-derived data."""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--compare-root", action="store_true")
    args = parser.parse_args()
    source_bytes = (HERE / "independent_residual_certificate.json").read_bytes()
    source = json.loads(source_bytes)
    colors = source["colors"]
    trans = source["concrete_transitions"]
    obs = source["observation_ids_by_coloring"]
    actions = source["actions"]
    doubles = [tuple(r) for r in source["initial_fibres"] if len(r) == 2]

    def shortest_common_probe(first, second):
        pending = deque([(first, second, ())])
        seen = {(first, second)}
        while pending:
            left, right, word = pending.popleft()
            if obs[left] != obs[right]:
                return word
            for action in range(30):
                a, b = trans[left][action], trans[right][action]
                if min(a, b) < 0 or (a, b) in seen:
                    continue
                pending.append((a, b, word + (action,)))
                seen.add((a, b))
        raise AssertionError("No common-legal distinguishing word")

    records = []
    for pair in doubles:
        word = shortest_common_probe(*pair)
        assert word
        traces = []
        for actual in pair:
            current = actual
            residual = set(pair)
            full_path = [current]
            residual_path = [sorted(residual)]
            all_actions = word + word[::-1]
            for action in all_actions:
                assert trans[current][action] >= 0
                current = trans[current][action]
                observed = obs[current]
                residual = {trans[i][action] for i in residual
                            if trans[i][action] >= 0 and obs[trans[i][action]] == observed}
                assert current in residual
                full_path.append(current)
                residual_path.append(sorted(residual))
            assert len(residual_path[len(word)]) == 1
            assert current == actual and residual == {actual}
            traces.append({
                "actual_start": actual,
                "action_indices": all_actions,
                "full_coloring_id_path": full_path,
                "observation_id_path": [obs[i] for i in full_path],
                "residual_id_path": residual_path,
                "final_same_as_start": True,
                "final_residual_singleton": True,
            })
        records.append({
            "initial_fibre": pair,
            "initial_lifts": [colors[i] for i in pair],
            "shortest_common_legal_probe_length": len(word),
            "probe_action_indices": word,
            "probe_actions": [actions[a] for a in word],
            "return_actions": [actions[a] for a in word[::-1]],
            "roundtrip_actions": len(word) * 2,
            "actual_cases": traces,
        })
    result = {
        "status": "PASS",
        "source_sha256": sha256(source_bytes).hexdigest(),
        "source": "independent_residual_certificate.json",
        "algorithm": "Pair-state BFS; replay each actual branch with observation filtering; reverse action word",
        "initial_double_fibres": len(doubles),
        "minimum_probe_length_histogram": dict(sorted(Counter(
            r["shortest_common_legal_probe_length"] for r in records).items())),
        "actual_cases": sum(len(r["actual_cases"]) for r in records),
        "roundtrip_move_histogram_over_actual_cases": dict(sorted(Counter(
            r["roundtrip_actions"] for r in records for _ in r["actual_cases"]).items())),
        "maximum_constructed_roundtrip_moves": max(r["roundtrip_actions"] for r in records),
        "all_final_actual_colorings_equal_start": True,
        "all_final_residuals_singleton": True,
        "claim_boundary": "Fixed cell95; initial full-J double fibres; shortest probes only, no optimal-roundtrip claim",
        "records": records,
    }
    encoded = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    destination = HERE / "probe_review.json"
    if args.check:
        assert destination.read_bytes() == encoded
    else:
        with destination.open("xb") as stream:
            stream.write(encoded)
    print(json.dumps({k: v for k, v in result.items() if k != "records"},
                     indent=2, sort_keys=True))
    if args.compare_root:
        root_raw = (HERE.parent / "probe.json").read_bytes()
        root = json.loads(root_raw)
        previous = json.loads((HERE.parent / (
            "frozen/audits/2026-10-20-multi-kempe-machines-af0df80/"
            "experiment/certificate.json")).read_bytes())
        labels = {}
        for old, current in zip(previous["joint_monitor_rows"], obs):
            assert labels.setdefault(tuple(old), current) == current
        assert len(labels) == len(set(labels.values())) == 192
        independent = {tuple(r["initial_fibre"]): r for r in records}
        assert len(root["probe_restore_records"]) == len(independent) == 72
        checked_branches = 0
        for external in root["probe_restore_records"]:
            pair = tuple(colors.index(c) for c in external["initial_lifts"])
            row = independent[pair]
            assert row["probe_actions"] == external["shortest_probe_actions"]
            assert row["shortest_common_legal_probe_length"] == external["probe_length"]
            assert row["roundtrip_actions"] == external["round_trip_length"]
            paths = {t["actual_start"]: t for t in row["actual_cases"]}
            for case in external["actual_branches"]:
                start = colors.index(case["initial_actual"])
                path = paths[start]
                assert case["restored_actual"] == colors[start]
                assert case["final_residual"] == [colors[start]]
                assert len(case["trace"]) == len(path["action_indices"])
                for step, observed_step in enumerate(case["trace"], 1):
                    assert observed_step["action"] == actions[path["action_indices"][step - 1]]
                    assert observed_step["actual"] == colors[path["full_coloring_id_path"][step]]
                    assert labels[tuple(observed_step["joint_observation"])] == path["observation_id_path"][step]
                    assert observed_step["residual_lifts"] == [
                        colors[i] for i in path["residual_id_path"][step]]
                checked_branches += 1
        assert root["round_trip_optimality_claimed"] is False
        assert root["shortest_probe_length_histogram"] == {
            str(k): v for k, v in result["minimum_probe_length_histogram"].items()}
        assert root["maximum_scheme_round_trip_length"] == 4
        print(json.dumps({
            "root_cross_review": "PASS",
            "root_probe_sha256": sha256(root_raw).hexdigest(),
            "every_full_branch_and_observation_checked": checked_branches,
        }, sort_keys=True))


if __name__ == "__main__":
    main()
