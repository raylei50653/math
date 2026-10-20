#!/usr/bin/env python3
"""Exact residual observer for the frozen, literal cell95 transition table.

Explicit reuse: graph-coloring and maximal-component enumeration belong to the
prior frozen certificate; this checker reconstructs the observer and all checks.
"""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import random
import tempfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SOURCE = AUDIT / "frozen/audits/2026-10-20-multi-kempe-machines-af0df80/experiment/certificate.json"
SOURCE_SHA = "feed98beeb5f83e29bf9c690283aff5d768d4f1e8ba0504f0422560fddeea6dc"
COUPLING = AUDIT / "frozen/audits/2026-10-20-multi-kempe-machines-af0df80/coupling-v2.json"
COUPLING_SHA = "98b5586e7ae1c7170ac0462e3c50c7a8614d45c7876cbe64f1077f54058ae1a6"
BASE = "af0df8081e79b51f8b24e17e01b2bd5572e46a0a"


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def digest(value):
    return sha256(encoded(value)).hexdigest()


def load_inputs():
    assert sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
    assert sha256(COUPLING.read_bytes()).hexdigest() == COUPLING_SHA
    source = json.loads(SOURCE.read_text())
    coupling = json.loads(COUPLING.read_text())
    colors = tuple(tuple(c) for c in source["all_colorings"])
    transitions = tuple(tuple(row) for row in source["transitions"])
    actions = tuple(tuple(a) for a in source["actions"])
    triples = tuple(tuple(row) for row in source["joint_monitor_rows"])
    values = tuple(sorted(set(triples)))
    observation_index = {value: i for i, value in enumerate(values)}
    observations = tuple(observation_index[row] for row in triples)
    fibres = tuple(
        tuple(i for i, observation in enumerate(observations) if observation == j)
        for j in range(len(values))
    )
    assert len(colors) == 264 and len(values) == 192 and len(actions) == 30
    assert Counter(map(len, fibres)) == {1: 120, 2: 72}
    for i, row in enumerate(transitions):
        assert len(row) == 30
        for a, target in enumerate(row):
            assert target < 0 or transitions[target][a] == i
    return source, coupling, colors, transitions, actions, values, observations, fibres


def grouped_successors(residual, action, transitions, observations):
    """All feasible J outputs, with exact current full-coloring residuals."""
    if not residual:
        return "reject", {}
    targets = [transitions[c][action] for c in residual]
    if all(target < 0 for target in targets):
        return "illegal", {}
    assert all(target >= 0 for target in targets), "same J frame must determine legality"
    assert len(set(targets)) == len(residual), "actual Kempe action must be injective"
    groups = defaultdict(list)
    for target in targets:
        groups[observations[target]].append(target)
    return "legal", {j: tuple(sorted(group)) for j, group in sorted(groups.items())}


def anchored_update(anchors, action, observation, transitions, observations):
    """Original-lift IDs never change; current candidates move and get filtered."""
    result = {
        origin: transitions[current][action]
        for origin, current in anchors.items()
        if transitions[current][action] >= 0 and
        observations[transitions[current][action]] == observation
    }
    assert set(result) <= set(anchors)
    assert len(set(result.values())) == len(result)
    return result


def reconstruct(seed=None):
    source, coupling, colors, transitions, actions, values, observations, fibres = load_inputs()
    rng = random.Random(seed)
    discovered = set(fibres)
    frontier = set(fibres)
    closure_layers = [len(discovered)]
    while frontier:
        added = set()
        order = sorted(frontier)
        action_order = list(range(len(actions)))
        if seed is not None:
            rng.shuffle(order)
            rng.shuffle(action_order)
        for residual in order:
            for action in action_order:
                _, groups = grouped_successors(residual, action, transitions, observations)
                added.update(groups.values())
        added -= discovered
        if not added:
            break
        discovered.update(added)
        closure_layers.append(len(discovered))
        frontier = added

    residuals = ((),) + tuple(sorted(discovered))
    residual_index = {residual: i for i, residual in enumerate(residuals)}
    assert len(residuals) == len(residual_index)
    initial = tuple(residual_index[fibre] for fibre in fibres)
    rows = []
    statuses = Counter()
    feasible_labels = 0
    for residual in residuals:
        row = []
        for action in range(len(actions)):
            status, groups = grouped_successors(residual, action, transitions, observations)
            successors = {str(j): residual_index[group] for j, group in groups.items()}
            statuses[status] += 1
            feasible_labels += len(successors)
            # Empty reject is a defined sink for every valid (action,J) label.
            row.append({"action_status": status, "output_successors": successors})
        rows.append(row)

    def step(state, action, output):
        return rows[state][action]["output_successors"].get(str(output), 0)

    # Independently enumerate the coarse existential quotient relation.
    quotient = []
    for fibre in fibres:
        row = []
        for action in range(len(actions)):
            successors = {
                observations[transitions[c][action]]
                for c in fibre if transitions[c][action] >= 0
            }
            row.append(tuple(sorted(successors)))
        quotient.append(tuple(row))

    accepted = []
    rejected = []
    first_witness = None
    anchor_checks = 0
    for j0, fibre in enumerate(fibres):
        anchors0 = {c: c for c in fibre}
        for a in range(len(actions)):
            for j1 in quotient[j0][a]:
                r1 = step(initial[j0], a, j1)
                anchors1 = anchored_update(anchors0, a, j1, transitions, observations)
                assert r1 != 0 and tuple(sorted(anchors1.values())) == residuals[r1]
                for b in range(len(actions)):
                    for j2 in quotient[j1][b]:
                        path = (j0, a, j1, b, j2)
                        r2 = step(r1, b, j2)
                        anchors2 = anchored_update(anchors1, b, j2, transitions, observations)
                        # Ground truth: same original coloring executes both actions.
                        concrete = tuple(sorted(
                            transitions[transitions[c][a]][b]
                            for c in fibre
                            if transitions[c][a] >= 0 and
                            observations[transitions[c][a]] == j1 and
                            transitions[transitions[c][a]][b] >= 0 and
                            observations[transitions[transitions[c][a]][b]] == j2
                        ))
                        assert residuals[r2] == concrete == tuple(sorted(anchors2.values()))
                        assert set(anchors2) <= set(anchors1) <= set(anchors0)
                        assert len(anchors2) <= len(anchors1) <= len(anchors0) <= 2
                        anchor_checks += 1
                        (accepted if concrete else rejected).append(path)
                        if not concrete and first_witness is None:
                            intermediate = fibre
                            first_witness = {
                                "path": path,
                                "actions": [actions[a], actions[b]],
                                "initial_full_lifts": [colors[c] for c in fibre],
                                "residual_after_first": [colors[c] for c in residuals[r1]],
                                "residual_after_second": [],
                                "intermediate_coarse_fibre": [colors[c] for c in fibres[j1]],
                                "false_target_coarse_fibre": [colors[c] for c in fibres[j2]],
                                "incompatible_intermediate_lifts": [
                                    colors[c] for c in fibres[j1]
                                    if c not in residuals[r1] and transitions[c][b] >= 0 and
                                    observations[transitions[c][b]] == j2
                                ],
                            }
    accepted.sort()
    rejected.sort()
    old_counts = coupling["two_step_quotient_paths"]
    assert len(accepted) == old_counts["concrete_observed_paths"] == 45888
    assert len(rejected) == old_counts["spurious_observed_paths"] == 384
    assert len(accepted) + len(rejected) == old_counts["abstract_observed_paths"] == 46272

    # Reconstruct and reject the literal witness saved by the previous audit.
    old = old_counts["first_witness"]
    color_index = {c: i for i, c in enumerate(colors)}
    a = actions.index(tuple(old["first_action"]))
    b = actions.index(tuple(old["second_action"]))
    j0 = observations[color_index[tuple(old["source_lifts"][0])]]
    j1 = observations[color_index[tuple(old["actual_lifts_after_first"][0])]]
    j2 = observations[color_index[tuple(old["false_target_lift"])]]
    saved_path = (j0, a, j1, b, j2)
    assert saved_path in rejected
    saved_r1 = step(initial[j0], a, j1)
    assert step(saved_r1, b, j2) == 0

    # Check every explicitly encoded finite-domain transition, including default
    # rejections for unlisted observation labels.
    label_checks = 0
    for state, residual in enumerate(residuals):
        for action in range(len(actions)):
            for output in range(len(values)):
                expected = tuple(sorted(
                    transitions[c][action] for c in residual
                    if transitions[c][action] >= 0 and
                    observations[transitions[c][action]] == output
                ))
                assert residuals[step(state, action, output)] == expected
                label_checks += 1

    histogram = Counter(map(len, residuals))
    return {
        "scope": "Fixed cell95 exact residual observer; not a general compressed closed-state theorem.",
        "git_base": BASE,
        "source_authority": "Frozen worktree bytes; previous certificate was not present at Git BASE.",
        "reused_source": str(SOURCE.relative_to(AUDIT)), "reused_source_sha256": SOURCE_SHA,
        "comparison_source": str(COUPLING.relative_to(AUDIT)), "comparison_source_sha256": COUPLING_SHA,
        "implementation": "Reuses frozen full colorings/actions/transitions; independently reconstructs residual observer closure.",
        "update": "R_next = {T_a(c): c in R, T_a(c) defined, J(T_a(c))=observed_J}",
        "empty_reject_state": 0,
        "illegal_action_semantics": "Separate tagged terminal outcome, no graph successor and no self-loop; all claimed valid J outputs reject.",
        "transition_encoding": "For each state/action, all 192 J outputs are defined: listed output_successors target nonempty states; every unlisted output targets empty reject 0.",
        "actions": actions, "joint_observation_values": values,
        "original_colorings": colors, "original_observations": observations,
        "initial_state_for_observation": initial,
        "residuals": residuals, "transitions": rows,
        "metrics": {
            "full_colorings": len(colors), "coarse_joint_states": len(fibres),
            "initial_size_histogram": dict(sorted(Counter(map(len, fibres)).items())),
            "closure_nonempty_counts": closure_layers,
            "reachable_nonempty_residuals": len(residuals) - 1,
            "states_including_empty_reject": len(residuals),
            "residual_size_histogram": dict(sorted(histogram.items())),
            "maximum_nonempty_residual_size": max(map(len, residuals)),
            "action_row_status_counts": dict(sorted(statuses.items())),
            "feasible_action_output_transitions": feasible_labels,
            "all_action_output_labels_checked": label_checks,
            "all_nonempty_states_have_one_current_J": all(
                len({observations[c] for c in residual}) == 1 for residual in residuals[1:]
            ),
            "all_local_updates_injective_on_candidates": True,
        },
        "two_step_validation": {
            "abstract_paths": len(accepted) + len(rejected),
            "actual_paths_all_accepted": len(accepted),
            "spurious_paths_all_rejected": len(rejected),
            "accepted_paths_sha256": digest(accepted),
            "rejected_paths_sha256": digest(rejected),
            "rejected_paths": rejected,
            "anchored_updates_checked": anchor_checks,
            "saved_old_witness_path": saved_path,
            "saved_old_witness_rejected": True,
            "first_rejected_witness": first_witness,
        },
        "storage_interpretation": {
            "online_current_candidates_maximum": 2,
            "original_anchor_candidates_maximum": 2,
            "anchor_ids_only_removed": True,
            "offline_residual_automaton_is_larger_than_full_coloring_automaton": True,
            "arbitrary_online_history_need_not_identify_single_actual_coloring": True,
        },
        "complete_canonical_fibres": source["complete_canonical_fibres"],
        "j1_source_status": "not triggered", "general_small_summary_closure": "OPEN",
    }


def verify(path, result):
    if path.read_bytes() != encoded(result):
        raise ValueError("residual certificate differs from complete reconstruction")


def negative_controls(certificate, result):
    before = sha256(certificate.read_bytes()).hexdigest()
    cases = []
    for name in ("reset_to_coarse_fibre", "empty_becomes_accepting", "illegal_as_self_loop", "wrong_residual_count", "omit_empty_fibre"):
        bad = json.loads(encoded(result))
        if name == "reset_to_coarse_fibre":
            witness = bad["two_step_validation"]["first_rejected_witness"]
            j0, a, j1, _, _ = witness["path"]
            initial = bad["initial_state_for_observation"][j0]
            old_target = bad["transitions"][initial][a]["output_successors"][str(j1)]
            bad_target = bad["initial_state_for_observation"][j1]
            assert old_target != bad_target
            bad["transitions"][initial][a]["output_successors"][str(j1)] = bad_target
        elif name == "empty_becomes_accepting":
            bad["transitions"][0][0]["output_successors"]["0"] = bad["initial_state_for_observation"][0]
        elif name == "illegal_as_self_loop":
            state, action = next(
                (s, a) for s, row in enumerate(bad["transitions"])
                for a, entry in enumerate(row) if entry["action_status"] == "illegal"
            )
            observation = bad["original_observations"][bad["residuals"][state][0]]
            bad["transitions"][state][action]["action_status"] = "legal"
            bad["transitions"][state][action]["output_successors"][str(observation)] = state
        elif name == "wrong_residual_count":
            bad["metrics"]["reachable_nonempty_residuals"] -= 1
        else:
            bad["complete_canonical_fibres"] = [row for row in bad["complete_canonical_fibres"] if row["count"]]
        with tempfile.TemporaryDirectory(prefix="kempe-residual-negative-") as directory:
            path = Path(directory) / "contaminated.json"
            path.write_bytes(encoded(bad))
            try:
                verify(path, result)
            except ValueError:
                cases.append({"case": name, "rejected": True})
            else:
                raise AssertionError(f"negative accepted: {name}")
    after = sha256(certificate.read_bytes()).hexdigest()
    assert before == after
    return {"cases": cases, "saved_certificate_sha256_unchanged": after}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--generate", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--negative-controls", action="store_true")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    args = parser.parse_args()
    result = reconstruct(args.seed)
    if args.generate:
        with args.certificate.open("xb") as stream:
            stream.write(encoded(result))
    else:
        verify(args.certificate, result)
    validation = result["two_step_validation"]
    summary = {
        "metrics": result["metrics"],
        "two_step": {key: validation[key] for key in (
            "abstract_paths", "actual_paths_all_accepted", "spurious_paths_all_rejected",
            "anchored_updates_checked", "saved_old_witness_rejected",
        )},
        "seed": args.seed,
        "certificate_sha256": sha256(args.certificate.read_bytes()).hexdigest(),
    }
    if args.negative_controls:
        summary["negative_controls"] = negative_controls(args.certificate, result)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
