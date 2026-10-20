#!/usr/bin/env python3
"""Verify transport plus observation filtering and safe same-channel batching."""
import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "frozen/audits/2026-10-20-multi-kempe-machines-af0df80/experiment/certificate.json"
CHANNELS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def component(c, pair, root, edges):
    reached = {root}
    while True:
        grown = reached | {v for u, v in edges if u in reached and c[v] in pair}
        grown |= {u for u, v in edges if v in reached and c[u] in pair}
        if grown == reached:
            return frozenset(reached)
        reached = grown


def generate():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    colors = tuple(tuple(c) for c in data["all_colorings"])
    actions = tuple(tuple(a) for a in data["actions"])
    trans = data["transitions"]
    obs = tuple(tuple(j) for j in data["joint_monitor_rows"])
    buckets = defaultdict(list)
    for i, j in enumerate(obs):
        buckets[j].append(i)

    # Within a fixed complementary-pair phase, every full component is fixed.
    # Compute both switches from original components, then use parity to cancel.
    phase_checks = 0
    phase_counts = []
    for channel in CHANNELS:
        count = 0
        labels = [a for a, (x, y, _) in enumerate(actions) if (x, y) in channel]
        for i, c in enumerate(colors):
            legal = [a for a in labels if trans[i][a] >= 0]
            for a in legal:
                for b in legal:
                    parity = set()
                    for k in (a, b):
                        x, y, root = actions[k]
                        key = ((x, y), component(c, (x, y), root, data["edges"]))
                        if key in parity:
                            parity.remove(key)
                        else:
                            parity.add(key)
                    out = list(c)
                    for (x, y), block in sorted(parity, key=lambda t: (t[0], sorted(t[1]))):
                        for v in block:
                            out[v] = x + y - out[v]
                    target = trans[trans[i][a]][b]
                    assert target >= 0 and tuple(out) == colors[target]
                    assert trans[trans[i][b]][a] == target
                    count += 1
        phase_counts.append(count)
        phase_checks += count

    # A transport followed by observation is a partial bijection restricted to
    # surviving initial indices. Test that endpoint parity plus survivor mask
    # agrees with every actual same-channel two-step observed trajectory.
    observed_cases = 0
    informative_identity_phases = 0
    first = None
    for joint, source in sorted(buckets.items()):
        for channel in CHANNELS:
            labels = [a for a, (x, y, _) in enumerate(actions) if (x, y) in channel]
            for a in labels:
                if trans[source[0]][a] < 0:
                    continue
                for b in labels:
                    if trans[source[0]][b] < 0:
                        continue
                    branches = defaultdict(list)
                    for i in source:
                        middle = trans[i][a]
                        target = trans[middle][b]
                        assert target >= 0
                        branches[obs[middle], obs[target]].append(i)
                    for (middle_obs, final_obs), initial_survivors in sorted(branches.items()):
                        r1 = {trans[i][a] for i in source if obs[trans[i][a]] == middle_obs}
                        r2 = {trans[i][b] for i in r1 if obs[trans[i][b]] == final_obs}
                        anchored = {trans[trans[i][a]][b] for i in initial_survivors}
                        assert r2 == anchored
                        assert len(initial_survivors) == len(r2) <= len(source)
                        observed_cases += 1
                        if a == b and len(initial_survivors) < len(source):
                            informative_identity_phases += 1
                            assert r2 == set(initial_survivors)
                            assert final_obs == joint
                            # Endpoint-only identity incorrectly reintroduces
                            # discarded lifts; select an impossible next output.
                            bad_obs = next(
                                obs[trans[i][a]] for i in source
                                if i not in initial_survivors
                            )
                            third = {trans[i][a] for i in r2
                                     if obs[trans[i][a]] == bad_obs}
                            endpoint_only = {trans[i][a] for i in source
                                             if obs[trans[i][a]] == bad_obs}
                            assert not third and endpoint_only
                            if first is None:
                                first = {
                                    "source_lifts": [colors[i] for i in source],
                                    "action": actions[a],
                                    "observations": [middle_obs, final_obs, bad_obs],
                                    "after_first": [colors[i] for i in sorted(r1)],
                                    "after_second": [colors[i] for i in sorted(r2)],
                                    "after_third": [],
                                    "endpoint_only_false_after_third": [
                                        colors[i] for i in sorted(endpoint_only)],
                                    "phase_endpoint_transport_is_identity": True,
                                    "phase_filter_is_identity": False,
                                }
    assert first is not None
    return {
        "scope": "Fixed cell95; all literal colorings; original five action roots.",
        "source_sha256": sha256(raw).hexdigest(),
        "phase_channels": CHANNELS,
        "same_channel_ordered_two_action_checks": phase_checks,
        "per_channel_checks": phase_counts,
        "observed_two_step_phase_branches": observed_cases,
        "informative_identity_phases": informative_identity_phases,
        "transport_only_cancellation_negative": first,
        "safe_batch_rule": "Keep original survivor indices plus per-component parity; never drop intermediate observation filters.",
        "j1_source_status": "not triggered",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument("--generate", action="store_true")
    modes.add_argument("--check", action="store_true")
    p.add_argument("--certificate", type=Path, default=HERE / "phase.json")
    args = p.parse_args()
    result = generate()
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    if args.generate:
        with args.certificate.open("xb") as f:
            f.write(raw)
    elif args.certificate.read_bytes() != raw:
        raise SystemExit("FAIL: phase certificate differs from reconstruction")
    print(json.dumps({k: v for k, v in result.items()
                      if k != "transport_only_cancellation_negative"}, sort_keys=True))


if __name__ == "__main__":
    main()
