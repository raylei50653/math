#!/usr/bin/env python3
"""Independent sequential coloring and edge-closure cross-review; stdlib only."""
import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SOURCE = AUDIT / "frozen/artifacts/c5_cells/cells.json"
PAIRS = tuple(itertools.combinations(range(4), 2))
ACTIONS = tuple((a, b, root) for a, b in PAIRS for root in range(5))
OUT = HERE / "cross_certificate.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def key(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def edges_of(cell):
    return tuple(sorted({tuple(sorted(edge)) for edge in cell["edges"]}
                        | {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}))


def enumerate_colors(n, edges, fixed=()):
    colors = list(fixed)
    if any(colors[u] == colors[v] for u, v in edges if u < len(colors) and v < len(colors)):
        return
    previous = [{u for u, w in edges if w == v} for v in range(n)]

    def visit():
        v = len(colors)
        if v == n:
            yield tuple(colors)
            return
        blocked = {colors[u] for u in previous[v]}
        for color in range(4):
            if color not in blocked:
                colors.append(color)
                yield from visit()
                colors.pop()

    yield from visit()


def blocks(coloring, edges, pair):
    remaining = {v for v, c in enumerate(coloring) if c in pair}
    answer = []
    while remaining:
        reached = {min(remaining)}
        while True:
            grown = reached | {v for e in edges if reached.intersection(e)
                               for v in e if coloring[v] in pair}
            if grown == reached:
                break
            reached = grown
        remaining -= reached
        answer.append(tuple(sorted(reached)))
    return tuple(answer)


def summary(coloring, systems, ports):
    keep = set(ports)
    return (tuple(coloring[v] for v in ports),
            tuple(tuple(sorted(tuple(v for v in block if v in keep)
                               for block in family if keep.intersection(block)))
                  for family in systems))


def action(coloring, systems, label):
    a, b, root = label
    if coloring[root] not in {a, b}:
        return None
    selected = next(block for block in systems[PAIRS.index((a, b))] if root in block)
    return tuple(a + b - c if v in selected else c for v, c in enumerate(coloring))


def class_ids(signatures):
    numbered = {}
    return tuple(numbered.setdefault(s, len(numbered)) for s in signatures)


def conflicts(ids, transitions):
    values = defaultdict(set)
    for source, row in enumerate(transitions):
        for label, target in enumerate(row):
            values[ids[source], label].add(None if target is None else ids[target])
    return sum(len(observed) > 1 for observed in values.values())


def refinement(ids, transitions):
    counts = [len(set(ids))]
    while True:
        refined = class_ids([
            (ids[source], tuple(None if target is None else ids[target] for target in row))
            for source, row in enumerate(transitions)
        ])
        if len(set(refined)) == counts[-1]:
            require(conflicts(refined, transitions) == 0, "refinement failed")
            return counts
        ids = refined
        counts.append(len(set(ids)))


def fixed_graph_review(catalogue):
    edges = edges_of(catalogue["cells"]["95"])
    colors = tuple(enumerate_colors(8, edges))
    index = {coloring: i for i, coloring in enumerate(colors)}
    systems = [tuple(blocks(coloring, edges, pair) for pair in PAIRS) for coloring in colors]
    transitions = []
    for coloring, components in zip(colors, systems):
        row = []
        for label in ACTIONS:
            target = action(coloring, components, label)
            require(target is None or target in index, "target absent")
            row.append(None if target is None else index[target])
        transitions.append(row)
    pin_results = []
    for size in range(4):
        for pins in itertools.combinations(range(5, 8), size):
            ports = tuple(range(5)) + pins
            ids = class_ids([summary(c, cs, ports) for c, cs in zip(colors, systems)])
            pin_results.append({"pins": list(pins), "classes": len(set(ids)),
                                "conflicting_class_action_pairs": conflicts(ids, transitions)})
    joint_ids = class_ids([summary(c, cs, range(5)) for c, cs in zip(colors, systems)])
    boundary_ids = class_ids([c[:5] for c in colors])
    one_step = class_ids([
        (c[:5], tuple(None if target is None else colors[target][:5] for target in row))
        for c, row in zip(colors, transitions)
    ])
    require(joint_ids == one_step,
            "joint and depth-one observations differ")
    word = [(1, 2, 1), (0, 1, 0)]
    traces = []
    for source in [(0, 1, 0, 1, 2, 1, 3, 2), (0, 1, 0, 1, 2, 2, 3, 3)]:
        trace = [source]
        current = index[source]
        for label in word:
            current = transitions[current][ACTIONS.index(label)]
            require(current is not None, "word disabled")
            trace.append(colors[current])
        traces.append(trace)
    require(traces[0][1][:5] == traces[1][1][:5], "first boundaries differ")
    require(traces[0][2][:5] != traces[1][2][:5], "second boundaries equal")
    return {
        "literal_colorings": len(colors),
        "enabled_actions": sum(target is not None for row in transitions for target in row),
        "pin_results": pin_results,
        "joint_signature_refinement_counts": refinement(joint_ids, transitions),
        "boundary_observation_refinement_counts": refinement(boundary_ids, transitions),
        "boundary_depth_one_and_joint_partition_equal": True,
        "distinguishing_word": word, "distinguishing_traces": traces,
    }


def catalogue_review(catalogue):
    totals = Counter(graphs=len(catalogue["cells"]), fibres=10 * len(catalogue["cells"]))
    rows = []
    for name, cell in sorted(catalogue["cells"].items(), key=lambda item: int(item[0])):
        n, edges = 5 + cell["k_eff"], edges_of(cell)
        state_counts = Counter()
        targets = defaultdict(set)
        fibres, fibre_states = [], []
        for boundary in catalogue["pattern_order"]:
            lifts = tuple(enumerate_colors(n, edges, boundary))
            fibres.append(["".join(map(str, coloring)) for coloring in lifts])
            local_states = set()
            for coloring in lifts:
                systems = tuple(blocks(coloring, edges, pair) for pair in PAIRS)
                observed = summary(coloring, systems, range(5))
                local_states.add(observed)
                state_counts[observed] += 1
                for label in ACTIONS:
                    target = action(coloring, systems, label)
                    if target is not None:
                        require(all(target[u] != target[v] for u, v in edges), "improper target")
                        target_blocks = tuple(blocks(target, edges, pair) for pair in PAIRS)
                        targets[observed, label].add(summary(target, target_blocks, range(5)))
            fibre_states.append(len(local_states))
        counts = [len(f) for f in fibres]
        require(sum(1 << i for i, f in enumerate(fibres) if f) == int(name), "support mask")
        ambiguous = {state_action for state_action, result in targets.items() if len(result) > 1}
        row = {"mask": int(name), "fibres": fibres, "fibre_counts": counts,
               "joint_states_by_fibre": fibre_states, "joint_states": len(state_counts),
               "states_merging_full_lifts": sum(count > 1 for count in state_counts.values()),
               "enabled_rooted_actions": 15 * sum(counts), "state_action_pairs": len(targets),
               "ambiguous_state_action_pairs": len(ambiguous),
               "ambiguous_joint_states": len({state for state, label in ambiguous}),
               "max_target_states": max(map(len, targets.values()), default=0)}
        rows.append(row)
        totals.update({
            "empty_fibres": counts.count(0), "full_lifts": sum(counts),
            "joint_states": len(state_counts),
            "boundary_fibres_split_by_joint_state": sum(count > 1 for count in fibre_states),
            "graphs_with_boundary_fibre_split": int(any(count > 1 for count in fibre_states)),
            "enabled_rooted_actions": row["enabled_rooted_actions"],
            "state_action_pairs": len(targets),
            "ambiguous_state_action_pairs": len(ambiguous),
            "ambiguous_joint_states": row["ambiguous_joint_states"],
            "graphs_with_collision": int(bool(ambiguous)),
        })
    return {"totals": dict(totals), "cells": rows}


def generate():
    raw = SOURCE.read_bytes()
    catalogue = json.loads(raw)
    fixed = fixed_graph_review(catalogue)
    full = catalogue_review(catalogue)
    root = json.loads((AUDIT / "refinement.json").read_bytes())
    experiment = json.loads((AUDIT / "experiment/certificate.json").read_bytes())
    require(root["edges"] == [list(e) for e in edges_of(catalogue["cells"]["95"])],
            "root graph mismatch")
    require(root["boundary"] == list(range(5))
            and root["actions"] == [list(a) for a in ACTIONS], "root action grammar")
    for field in ["literal_colorings", "enabled_actions", "joint_signature_refinement_counts",
                  "boundary_observation_refinement_counts"]:
        require(fixed[field] == root[field], "root mismatch: " + field)
    require(len(fixed["pin_results"]) == len(root["pin_results"]), "pin row count")
    for expected, actual in zip(fixed["pin_results"], root["pin_results"]):
        require(all(expected[field] == actual[field] for field in expected), "pin mismatch")
    require(full["totals"] == experiment["totals"], "catalogue total mismatch")
    require(len(full["cells"]) == len(experiment["cells"]), "catalogue row count")
    for expected, actual in zip(full["cells"], experiment["cells"]):
        require(all(expected[field] == actual[field] for field in expected), "catalogue row mismatch")
        frozen_cell = catalogue["cells"][str(expected["mask"])]
        require(actual["n"] == 5 + frozen_cell["k_eff"]
                and actual["edges"] == [list(e) for e in edges_of(frozen_cell)],
                "catalogue graph mismatch")
    return {
        "schema": "independent-joint-kempe-cross-review-v1",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "fixed_graph": fixed, "catalogue_totals": full["totals"],
        "catalogue_rows_sha256": hashlib.sha256(key(full["cells"]).encode()).hexdigest(),
        "scope": "Exact frozen 132 catalogue rows; fixed cell95 complete literal action graph; no imports from experiment or root refinement; J1/r6 not triggered",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["build", "check"])
    args = parser.parse_args()
    result = generate()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.mode == "build":
        with OUT.open("x", encoding="utf-8") as stream:
            stream.write(encoded)
    require(OUT.read_text() == encoded, "saved independent cross certificate mismatch")
    print(json.dumps({"status": "PASS", "mode": args.mode,
                      "certificate_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
                      "fixed_graph": result["fixed_graph"],
                      "catalogue_totals": result["catalogue_totals"]}, indent=2))


if __name__ == "__main__":
    main()
