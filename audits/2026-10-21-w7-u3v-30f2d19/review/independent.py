#!/usr/bin/env python3
"""Independent synchronous zero-closure for the one actual edge u3-v.

No import from closure/check.py, no queue, no degree-decrement algorithm,
no LP. Every round rebuilds support from the complete pinned column family.
The root residual is compared only after the independent fixed point exists.
"""
from collections import defaultdict
import argparse
import gzip
from hashlib import sha256
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = HERE.parents[2]
SOURCE = "audits/2026-10-20-r6-941-j1-five-edge-417732f"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_pinned(name, manifest, digests):
    path = ROOT / name
    data = path.read_bytes()
    frozen = next(item for item in manifest["inputs"] if item["path"] == name)
    digest = sha256(data).hexdigest()
    require(len(data) == frozen["bytes"] and digest == frozen["sha256"],
            "frozen input drift: " + name)
    digests[name] = digest
    return json.loads(gzip.decompress(data))


def validate_chord_zero(state, caps):
    require(caps["states"][state][3] == caps["states"][state][10],
            "u3-v does not force this complete fibre to vanish")


def compare_residual(record, states, columns):
    require(record["live_state_ids"] == sorted(states),
            "root residual has the wrong live-state set")
    require(record["live_column_ids"] == sorted(columns),
            "root residual has the wrong live-column set")


def derive(seed):
    manifest = json.loads((AUDIT / "BASE.json").read_text())
    digests = {}
    caps = load_pinned(SOURCE + "/counting/caps.json.gz", manifest, digests)
    orbit = load_pinned(SOURCE + "/counting/orbits.json.gz", manifest, digests)
    require(caps["ordered_rim"] == ["a", "n", "u4", "u3", "u2", "u1", "L", "q", "c", "s", "v", "w", "t"],
            "the fixed original rim changed")
    row_state = dict(orbit["rowids"])
    state_rows = defaultdict(list)
    for row, state in orbit["rowids"]:
        state_rows[state].append(row)
    original_states = set(orbit["live"])
    columns = orbit["columns"]
    order = list(range(len(columns)))
    random.Random(seed).shuffle(order)
    # This independent representation retains full rows, but drops duplicate
    # state occurrences only for the all-live test; no incidence is dropped
    # from the supported-half-row union.
    column_states = [frozenset(row_state[row] for row in col) for col in columns]
    all_rows = {row for col in columns for row in col}
    require(all(len(state_rows[s]) == 3 and set(state_rows[s]) <= all_rows
                for s in original_states), "the original frozen closure has an empty row")
    require(all(states <= original_states for states in column_states),
            "frozen surviving column meets an old zero fibre")

    initial_zeros = {s for s in original_states
                     if caps["states"][s][3] == caps["states"][s][10]}
    for s in initial_zeros:
        validate_chord_zero(s, caps)
    live_states = original_states - initial_zeros
    live_columns = set(range(len(columns)))
    rounds = []
    while True:
        # Rebuild both sets synchronously from scratch. This is deliberately
        # distinct from the root's asynchronous queue and adjacency counters.
        next_columns = {j for j in order if column_states[j] <= live_states}
        supported_rows = {row for j in next_columns for row in columns[j]}
        next_states = {s for s in live_states
                       if all(row in supported_rows for row in state_rows[s])}
        require(next_states <= live_states and next_columns <= live_columns,
                "zero propagation ceased to be monotone")
        rounds.append(dict(round=len(rounds) + 1, live_states=len(next_states),
                           live_columns=len(next_columns),
                           newly_zero_states=len(live_states - next_states),
                           newly_zero_columns=len(live_columns - next_columns),
                           target_A_live=44459 in next_states,
                           target_B_live=44466 in next_states,
                           two_columns_live=[j in next_columns for j in (66582, 67755)]))
        stable = next_states == live_states and next_columns == live_columns
        live_states, live_columns = next_states, next_columns
        if stable:
            break
    require(len(original_states) == 61308 and len(columns) == 307197,
            "the complete frozen family size changed")
    require(len(initial_zeros) == 15382, "single-edge initial zeros differ")
    require(len(live_states) == 35132 and len(live_columns) == 70343,
            "the independently derived fixed point changed")
    require(not ({44459, 44466} & live_states), "a required witness target survived")
    require(not ({66582, 67755} & live_columns), "a requested orbit column survived")

    # Compare after derivation, not as an input to zero propagation.
    root_path = AUDIT / "closure/result.json.gz"
    root_bytes = root_path.read_bytes()
    root = json.loads(gzip.decompress(root_bytes))
    profile10 = next(row for row in root["profiles"] if row["original_profile_id"] == 10)
    require(profile10["all_original_chords"] == [["u3", "v"]],
            "root minimal profile has extra original edges")
    compare_residual(profile10, live_states, live_columns)

    # Controls check real proof gates, not just self-comparison of a JSON blob.
    # Without an added edge, the old full family is already a fixed point.
    require(all(states <= original_states for states in column_states) and
            all(set(state_rows[s]) <= all_rows for s in original_states),
            "edge-free frozen family is not a fixed point")
    rejected = False
    try:
        validate_chord_zero(44459, caps)
    except ValueError:
        rejected = True
    require(rejected, "a target proper on u3-v was accepted as a chord-zero leaf")
    # The two columns are proper in every row on the actual chord and survive
    # the first complete-column filter: a witness-only or one-split test is
    # insufficient for this exclusion.
    require(all(column_states[j].isdisjoint(initial_zeros) for j in (66582, 67755)),
            "requested columns unexpectedly die directly on the original edge")
    require(rounds[0]["two_columns_live"] == [True, True],
            "the cross-split propagation control failed")
    corrupted = dict(profile10)
    corrupted["live_state_ids"] = sorted(live_states | {44459})
    rejected_corruption = False
    try:
        compare_residual(corrupted, live_states, live_columns)
    except ValueError:
        rejected_corruption = True
    require(rejected_corruption, "reintroducing the target escaped residual comparison")

    return dict(
        status="PASS; independent synchronous single-edge source zero closure",
        mathematical_base=manifest["mathematical_base"],
        audit_base=manifest["base"],
        input_sha256=digests,
        root_residual_sha256=sha256(root_bytes).hexdigest(),
        algorithm="synchronous full-family set recomputation; no root checker imported",
        original_edge=["u3", "v"], initial_new_zero_states=len(initial_zeros),
        original_live_states=len(original_states), original_columns=len(columns),
        rounds=rounds, final_live_states=len(live_states), final_live_columns=len(live_columns),
        newly_propagated_state_zeros=len(original_states)-len(initial_zeros)-len(live_states),
        root_profile10_residual_exact_match=True,
        target_A_zero=True, target_B_zero=True,
        requested_columns_zero=[66582, 67755],
        source_exclusion="strict W7 contract plus original u3-v; actual target sum must be positive",
        controls=dict(edge_free_frozen_family_fixed_point=True,
                      target_A_cannot_be_a_direct_chord_zero_leaf=True,
                      both_columns_survive_initial_chord_filter=True,
                      target_reintroduction_rejected=True),
        no_LP=True, no_new_original_graph_enumeration=True,
        limitations=["Uses frozen complete orbit-coverage and previous zero-fibre authority",
                     "Does not identify a smaller bad source or perform corridor contraction",
                     "No conclusion for other W7 profiles, general C7, J1/J2, or Lean"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    result = derive(args.seed)
    path = HERE / "independent.json"
    if args.build:
        with path.open("x") as output:
            json.dump(result, output, indent=2, sort_keys=True)
            output.write("\n")
    else:
        require(json.loads(path.read_text()) == result, "independent review certificate differs")
    print(json.dumps(dict(status=result["status"], seed=args.seed,
                          rounds=len(result["rounds"]),
                          final_live_states=result["final_live_states"],
                          final_live_columns=result["final_live_columns"],
                          requested_columns_zero=result["requested_columns_zero"],
                          source_excluded=True, controls="4 passed"), indent=2))


if __name__ == "__main__":
    main()
