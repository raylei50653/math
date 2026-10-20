#!/usr/bin/env python3
"""Cross-review saved results only after independent reconstruction."""
from hashlib import sha256
from collections import deque
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sources = {
        "independent": HERE / "independent_certificate.json",
        "experiment": AUDIT / "experiment/certificate.json",
        "coupling": AUDIT / "coupling-v2.json",
    }
    files = {name: path.read_bytes() for name, path in sources.items()}
    review, main, coupling = (
        json.loads(files[name]) for name in ("independent", "experiment", "coupling")
    )
    assert review["source_sha256"] == main["source_sha256"]
    assert review["colorings"] == main["all_colorings"]
    assert review["edges"] == main["edges"]
    assert review["action_order"] == main["actions"]
    assert review["transitions"] == main["transitions"]
    for subset, external in zip(review["subsets"].values(), main["subset_results"]):
        full = external["full_alphabet"]
        assert subset["full_alphabet_refinement_counts"] == full["refinement_counts"]
        assert subset["full_alphabet_conflicts"]["conflicting_state_action_pairs"] == (
            full["layers"][0]["ambiguous_class_action_pairs"])
    for local, external in zip(review["local_channels"], main["local_alphabet_results"]):
        assert local["local_refinement_counts"] == external["refinement_counts"]
        assert local["local_conflicts"]["conflicting_state_action_pairs"] == 0
    for a, b in zip(review["cross_channel_effects"], coupling["cross_channel_effects"]):
        assert a["pair"] == b["pair"] and a["enabled"] == b["enabled"]
        assert a["changed_partition_channel_counts"] == b["changed_partition_channel_counts"]
        assert a["persistent_contact_connectivity_change_counts"] == (
            b["persistent_contact_connectivity_changed"])
    assert review["commutators"] == coupling["commutators"]
    for key in ("successor_marginal_product", "two_step_quotient_paths"):
        assert all(coupling[key][k] == value for k, value in review[key].items())

    colors = review["colorings"]
    observations = review["joint_monitor_observations"]
    trans = review["transitions"]
    actions = review["action_order"]
    witness = coupling["two_step_quotient_paths"]["first_witness"]
    ids = [colors.index(c) for c in witness["source_lifts"]]
    initial = observations[ids[0]]
    assert ids == [i for i, obs in enumerate(observations) if obs == initial]
    first = actions.index(witness["first_action"])
    second = actions.index(witness["second_action"])
    supplier = colors.index(witness["incompatible_middle_lift"])
    middle = observations[supplier]
    reached = [trans[i][first] for i in ids if trans[i][first] >= 0 and
               observations[trans[i][first]] == middle]
    assert [colors[i] for i in reached] == witness["actual_lifts_after_first"]
    assert supplier not in reached
    false = trans[supplier][second]
    assert false >= 0
    assert colors[false] == witness["false_target_lift"]
    final = [trans[i][second] for i in reached if trans[i][second] >= 0]
    assert [colors[i] for i in final] == witness["actual_final_lifts"]
    assert all(observations[false] != observations[i] for i in final)
    assert first == second
    assert all(trans[trans[i][first]][first] == i for i in ids)

    # Check the saved indefinite uninformative cycle using independently
    # reconstructed transitions; it does not imply a universal online depth.
    cycle = coupling["uninformative_online_cycle"]
    cycle_ids = [colors.index(c) for c in cycle["source_lifts"]]
    action = actions.index(cycle["action"])
    one = [trans[i][action] for i in cycle_ids]
    two = [trans[i][action] for i in one]
    assert [colors[i] for i in one] == cycle["after_one"]
    assert [colors[i] for i in two] == cycle["after_two"] == cycle["source_lifts"]
    assert all(observations[i] == observations[one[0]] for i in one)
    assert len(cycle_ids) == cycle["belief_size"] > 1

    # Reconstruct every saved monitor value from the main per-coloring row.
    for i, row in enumerate(main["joint_monitor_rows"]):
        for m, state_id in enumerate(row):
            frame, pair_partitions = main["monitor_values"][m][state_id]
            assert observations[i][m] == [frame, *pair_partitions]

    def trace_observation(i, channels):
        if channels is None:
            return colors[i][:5]
        return [[observations[i][m][0], observations[i][m][1:]] for m in channels]

    def shortest_depth(left, right, channels):
        pending = deque([(left, right, 0)])
        visited = {(left, right)}
        while pending:
            l, r, depth = pending.popleft()
            if trace_observation(l, channels) != trace_observation(r, channels):
                return depth
            for a in range(30):
                nl, nr = trans[l][a], trans[r][a]
                if (nl < 0) != (nr < 0):
                    return depth + 1
                if nl >= 0 and (nl, nr) not in visited:
                    pending.append((nl, nr, depth + 1))
                    visited.add((nl, nr))
        return None

    trace_items = [(None, main["boundary_only"])]
    trace_items.extend(([m - 1 for m in row["monitors"]], row["full_alphabet"])
                       for row in main["subset_results"])
    for channels, details in trace_items:
        witness = details["deepest_shortest_trace"]
        trace_actions = [actions.index(a) for a in witness["actions"]]
        initial_pair = [colors.index(path["full_colorings"][0])
                        for path in witness["paths"]]
        assert shortest_depth(*initial_pair, channels) == witness["shortest_distinguishing_length"]
        for path in witness["paths"]:
            current = colors.index(path["full_colorings"][0])
            assert trace_observation(current, channels) == path["observations"][0]
            for step, action in enumerate(trace_actions, 1):
                current = trans[current][action]
                assert current >= 0
                assert colors[current] == path["full_colorings"][step]
                assert trace_observation(current, channels) == path["observations"][step]
        if "first_collision" in details:
            collision = details["first_collision"]
            left, right = (colors.index(collision[k]) for k in ("source1", "source2"))
            assert trace_observation(left, channels) == trace_observation(right, channels)
            action = actions.index(collision["action"])
            left, right = trans[left][action], trans[right][action]
            assert colors[left] == collision["target1"] and colors[right] == collision["target2"]
            assert trace_observation(left, channels) != trace_observation(right, channels)

    result = {
        "status": "PASS",
        "input_sha256": {name: sha256(raw).hexdigest() for name, raw in files.items()},
        "verified": [
            "Every literal proper coloring and all 30 partial transitions",
            "Every per-coloring monitor row and all refinement count sequences",
            "Own-channel deterministic updates and mixed-channel conflicts",
            "Commutators and persistent-contact connectivity changes",
            "Two-step abstract/concrete path totals and same-involution false witness",
            "Uninformative online cycle with two complete possible colorings",
            "Saved deepest shortest distinguishing traces and first collisions",
        ],
        "temporal_negative_control": {
            "abstract_edges_exist": True,
            "common_whole_source_path_exists": False,
            "same_action_twice": coupling["two_step_quotient_paths"]["first_witness"]["first_action"],
            "incompatible_middle_lift_rejected": coupling["two_step_quotient_paths"]["first_witness"]["incompatible_middle_lift"],
        },
    }
    encoded = (json.dumps(result, indent=2) + "\n").encode()
    destination = HERE / "cross_review.json"
    if args.check:
        assert destination.read_bytes() == encoded
    else:
        with destination.open("xb") as stream:
            stream.write(encoded)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
