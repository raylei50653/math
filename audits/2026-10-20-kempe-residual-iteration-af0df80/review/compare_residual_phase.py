#!/usr/bin/env python3
"""Cross-review residual observer and complementary-channel phase certificates."""
import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
CHANNELS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = {
        "independent": HERE / "independent_residual_certificate.json",
        "main": AUDIT / "experiment/certificate.json",
        "phase": AUDIT / "phase.json",
    }
    raw = {name: path.read_bytes() for name, path in files.items()}
    review = json.loads(raw["independent"])
    colors = review["colors"]
    trans = review["concrete_transitions"]
    obs = review["observation_ids_by_coloring"]
    actions = review["actions"]
    fibres = [tuple(r) for r in review["initial_fibres"]]
    residuals = [tuple(r) for r in review["residuals"]]
    edges = {(residuals[r], a, o): residuals[t]
             for r, a, o, t in review["nonempty_edges"]}

    def update(residual, action, observed):
        return tuple(sorted({trans[i][action] for i in residual
                             if trans[i][action] >= 0 and
                             obs[trans[i][action]] == observed}))

    # Independent whole-graph transitions, now compute phase counts before
    # inspecting the phase certificate results.
    per_channel = []
    allowed = []
    for channel in CHANNELS:
        acts = [a for a, (x, y, _) in enumerate(actions) if (x, y) in channel]
        allowed.append(acts)
        count = 0
        for i, row in enumerate(trans):
            for a in acts:
                if row[a] < 0:
                    continue
                for b in acts:
                    j = trans[row[a]][b]
                    if j < 0:
                        continue
                    assert row[b] >= 0
                    assert trans[row[b]][a] == j
                    count += 1
        per_channel.append(count)
    phase_paths = {
        (obs[i], a, obs[j], b, obs[k])
        for acts in allowed
        for i, row in enumerate(trans)
        for a in acts if (j := row[a]) >= 0
        for b in acts if (k := trans[j][b]) >= 0
    }
    informative_identity = 0
    for q0, a, q1, b, q2 in phase_paths:
        if a != b:
            continue
        assert q0 == q2
        after = update(update(fibres[q0], a, q1), b, q2)
        assert set(after) <= set(fibres[q0])
        informative_identity += bool(after) and set(after) != set(fibres[q0])
    wave = set(fibres)
    waves = [len(wave)]
    while True:
        new = wave | {t for (r, _, _), t in edges.items() if r in wave}
        if new == wave:
            break
        wave = new
        waves.append(len(wave))
    assert wave == set(residuals)

    main_cert = json.loads(raw["main"])
    phase = json.loads(raw["phase"])
    assert main_cert["original_colorings"] == colors
    assert main_cert["actions"] == actions
    obs_map = {}
    for old, current in zip(main_cert["original_observations"], obs):
        assert obs_map.setdefault(old, current) == current
    assert len(obs_map) == len(set(obs_map.values())) == 192
    external_residuals = [tuple(r) for r in main_cert["residuals"]]
    assert set(external_residuals) == {()} | set(residuals)
    checked = 0
    for r, rows in zip(external_residuals, main_cert["transitions"]):
        assert len(rows) == 30
        for a, row in enumerate(rows):
            status = ("reject" if not r else "legal" if trans[r[0]][a] >= 0 else "illegal")
            assert row["action_status"] == status
            if r:
                assert all((trans[i][a] >= 0) == (status == "legal") for i in r)
            for old_o in range(192):
                expected = update(r, a, obs_map[old_o])
                external_target = external_residuals[row["output_successors"].get(str(old_o), 0)]
                assert external_target == expected
                checked += 1
    for old_o, rid in enumerate(main_cert["initial_state_for_observation"]):
        assert external_residuals[rid] == fibres[obs_map[old_o]]
    assert main_cert["metrics"]["closure_nonempty_counts"] == waves
    assert main_cert["metrics"]["all_action_output_labels_checked"] == checked

    quotient_edges = {(obs[i], a, obs[t])
                      for i, row in enumerate(trans) for a, t in enumerate(row) if t >= 0}
    outgoing = defaultdict(set)
    for q, a, t in quotient_edges:
        outgoing[q].add((a, t))
    abstract = {(q, a, mid, b, last)
                for q, a, mid in quotient_edges for b, last in outgoing[mid]}
    rejected = set()
    anchored_checked = 0
    for q0, a, q1, b, q2 in abstract:
        middle = update(fibres[q0], a, q1)
        final = update(middle, b, q2)
        # Original witnesses are meaningful only together with their transport.
        original_survivors = [
            i for i in fibres[q0] if trans[i][a] >= 0 and obs[trans[i][a]] == q1 and
            trans[trans[i][a]][b] >= 0 and obs[trans[trans[i][a]][b]] == q2
        ]
        transported_originals = tuple(sorted(trans[trans[i][a]][b] for i in original_survivors))
        assert transported_originals == final
        anchored_checked += 1
        if not final:
            rejected.add((q0, a, q1, b, q2))
    supplied_rejects = {
        (obs_map[q0], a, obs_map[q1], b, obs_map[q2])
        for q0, a, q1, b, q2 in main_cert["two_step_validation"]["rejected_paths"]
    }
    assert rejected == supplied_rejects and len(rejected) == 384
    assert len(abstract) - len(rejected) == 45888

    assert phase["per_channel_checks"] == per_channel
    assert phase["same_channel_ordered_two_action_checks"] == sum(per_channel)
    assert phase["observed_two_step_phase_branches"] == len(phase_paths)
    assert phase["informative_identity_phases"] == informative_identity
    witness = phase["transport_only_cancellation_negative"]
    start = tuple(colors.index(c) for c in witness["source_lifts"])
    assert start in fibres
    a = actions.index(witness["action"])
    observed_ids = [
        obs_map[main_cert["joint_observation_values"].index(value)]
        for value in witness["observations"]
    ]
    current = start
    for step, observed in zip(("first", "second", "third"), observed_ids):
        current = update(current, a, observed)
        assert [colors[i] for i in current] == witness[f"after_{step}"]
    assert current == ()
    assert all(trans[trans[i][a]][a] == i for i in start)
    endpoint_only = update(start, a, observed_ids[-1])
    assert [colors[i] for i in endpoint_only] == witness["endpoint_only_false_after_third"]
    assert endpoint_only
    assert set(update(update(start, a, observed_ids[0]), a, observed_ids[1])) < set(start)

    result = {
        "status": "PASS",
        "input_sha256": {name: sha256(value).hexdigest() for name, value in raw.items()},
        "closure_waves": waves,
        "all_state_action_observation_results_checked": checked,
        "anchored_original_witness_transport_checks": anchored_checked,
        "old_false_two_step_paths_rejected_exactly": len(rejected),
        "old_concrete_two_step_paths_accepted": len(abstract) - len(rejected),
        "same_channel_ordered_two_action_checks": sum(per_channel),
        "per_channel_checks": per_channel,
        "observed_two_step_phase_branches": len(phase_paths),
        "informative_identity_phases": informative_identity,
        "saved_three_step_counterexample_verified": True,
        "phase_endpoint_parity_does_not_replace_intermediate_filters": True,
    }
    encoded = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    target = HERE / "cross_review.json"
    if args.check:
        assert target.read_bytes() == encoded
    else:
        with target.open("xb") as stream:
            stream.write(encoded)
    print(encoded.decode(), end="")


if __name__ == "__main__":
    main()
