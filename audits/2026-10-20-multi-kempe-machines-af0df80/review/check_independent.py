#!/usr/bin/env python3
"""Independent fixed-cell95 review: exhaustive tuples and adjacency BFS.

This file does not import the experiment, its outputs, or prior checkers.
All monitors in a row are obtained from one literal proper coloring.
"""
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations, product
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
CATALOGUE = AUDIT / (
    "frozen/audits/2026-10-20-joint-kempe-state-1148ce0/"
    "frozen/artifacts/c5_cells/cells.json"
)
PAIRS = tuple(combinations(range(4), 2))
CHANNELS = ((0, 5), (1, 4), (2, 3))
CHANNEL_NAMES = ("01|23", "02|13", "03|12")


def partition_ids(values):
    keys = sorted(set(values))
    lookup = {key: idx for idx, key in enumerate(keys)}
    return tuple(lookup[value] for value in values)


def refine(observations, transitions, allowed):
    colors = partition_ids(observations)
    counts = [len(set(colors))]
    while True:
        keys = [
            (colors[i], tuple(-1 if row[a] < 0 else colors[row[a]] for a in allowed))
            for i, row in enumerate(transitions)
        ]
        updated = partition_ids(keys)
        count = len(set(updated))
        if count == counts[-1]:
            return counts, colors
        counts.append(count)
        colors = updated


def transition_conflicts(observations, transitions, allowed):
    rows = defaultdict(dict)
    for source, obs in enumerate(observations):
        for action in allowed:
            target = transitions[source][action]
            out = None if target < 0 else observations[target]
            rows[(obs, action)].setdefault(out, source)
    bad = [(key, choices) for key, choices in rows.items() if len(choices) > 1]
    if not bad:
        return {"conflicting_state_action_pairs": 0}
    (obs, action), choices = bad[0]
    source_ids = list(choices.values())[:2]
    return {
        "conflicting_state_action_pairs": len(bad),
        "witness_source_ids": source_ids,
        "action_id": action,
        "observation": obs,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Reconstruct and byte-check the saved certificate.")
    args = parser.parse_args()
    raw = CATALOGUE.read_bytes()
    cell = json.loads(raw)["cells"]["95"]
    n = 5 + cell["k_eff"]
    assert n == 8
    edges = sorted({tuple(sorted(edge)) for edge in cell["edges"]} |
                   {tuple(sorted((i, (i + 1) % 5))) for i in range(5)})
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colorings = [
        c for c in product(range(4), repeat=n)
        if all(c[u] != c[v] for u, v in edges)
    ]
    index = {c: i for i, c in enumerate(colorings)}
    components = []
    partitions = []
    for c in colorings:
        c_components, c_partitions = [], []
        for a, b in PAIRS:
            remaining = {v for v in range(n) if c[v] in (a, b)}
            blocks = []
            while remaining:
                start = min(remaining)
                remaining.remove(start)
                queue, seen = deque([start]), {start}
                while queue:
                    u = queue.popleft()
                    for v in adjacency[u] & remaining:
                        remaining.remove(v)
                        seen.add(v)
                        queue.append(v)
                blocks.append(tuple(sorted(seen)))
            c_components.append(tuple(blocks))
            c_partitions.append(tuple(sorted(tuple(v for v in block if v < 5)
                                            for block in blocks if any(v < 5 for v in block))))
        components.append(c_components)
        partitions.append(c_partitions)
    actions = [(pair_idx, root) for pair_idx in range(6) for root in range(5)]
    transitions = []
    for ci, c in enumerate(colorings):
        row = []
        for pair_idx, root in actions:
            pair = PAIRS[pair_idx]
            if c[root] not in pair:
                row.append(-1)
                continue
            block = next(block for block in components[ci][pair_idx] if root in block)
            d = list(c)
            for v in block:
                d[v] = pair[1] if c[v] == pair[0] else pair[0]
            assert tuple(d) in index
            row.append(index[tuple(d)])
        transitions.append(row)
    monitors = [
        [(c[:5], partitions[i][pairs[0]], partitions[i][pairs[1]])
         for i, c in enumerate(colorings)]
        for pairs in CHANNELS
    ]
    joint = [tuple(monitors[m][i] for m in range(3)) for i in range(len(colorings))]
    effects = []
    for pair_idx, pair in enumerate(PAIRS):
        enabled = 0
        changed = [0, 0, 0]
        persistent_changed = [0, 0, 0]
        for i, row in enumerate(transitions):
            for action, (p, root) in enumerate(actions):
                if p != pair_idx or row[action] < 0:
                    continue
                target = row[action]
                enabled += 1
                for ch, pair_indexes in enumerate(CHANNELS):
                    changed[ch] += any(partitions[i][q] != partitions[target][q]
                                       for q in pair_indexes)
                    # Compare connectivity only between contacts belonging to
                    # the pair before and after; color-domain moves are excluded.
                    any_change = False
                    for q in pair_indexes:
                        persistent = [v for v in range(5)
                                      if colorings[i][v] in PAIRS[q] and
                                      colorings[target][v] in PAIRS[q]]
                        for v, w in combinations(persistent, 2):
                            before = any(v in block and w in block
                                         for block in partitions[i][q])
                            after = any(v in block and w in block
                                        for block in partitions[target][q])
                            any_change |= before != after
                    persistent_changed[ch] += any_change
        effects.append({
            "pair": pair, "enabled": enabled,
            "changed_partition_channel_counts": changed,
            "persistent_contact_connectivity_change_counts": persistent_changed,
        })
    commutators = {
        kind: {"both_orders_legal": 0, "different_full_target": 0,
               "different_joint_target": 0, "different_boundary": 0}
        for kind in ("same_pair", "disjoint_pairs", "overlap_one_color")
    }
    for i, row in enumerate(transitions):
        for a, b in combinations(range(30), 2):
            a1, b1 = row[a], row[b]
            if a1 < 0 or b1 < 0:
                continue
            a2, b2 = transitions[a1][b], transitions[b1][a]
            if a2 < 0 or b2 < 0:
                continue
            p, q = PAIRS[actions[a][0]], PAIRS[actions[b][0]]
            kind = ("same_pair" if p == q else "disjoint_pairs"
                    if not set(p) & set(q) else "overlap_one_color")
            entry = commutators[kind]
            entry["both_orders_legal"] += 1
            entry["different_full_target"] += a2 != b2
            entry["different_joint_target"] += joint[a2] != joint[b2]
            entry["different_boundary"] += colorings[a2][:5] != colorings[b2][:5]
    joint_fibres = defaultdict(list)
    for i, obs in enumerate(joint):
        joint_fibres[obs].append(i)
    inflated_cases = inflated_tuples = 0
    for ids in joint_fibres.values():
        for a in range(30):
            targets = [transitions[i][a] for i in ids]
            if targets[0] < 0:
                assert all(t < 0 for t in targets)
                continue
            assert all(t >= 0 for t in targets)
            actual = {joint[t] for t in targets}
            assert len({colorings[t][:5] for t in targets}) == 1
            marginals = [{row[m] for row in actual} for m in range(3)]
            false = set(product(*marginals)) - actual
            inflated_cases += bool(false)
            inflated_tuples += len(false)
    # Form actual trace sets by traversing concrete colorings. Separately
    # compose the existential quotient edges; compare the complete trace sets.
    joint_ids = partition_ids(joint)
    quotient_edges = {
        (joint_ids[i], a, joint_ids[t])
        for i, row in enumerate(transitions)
        for a, t in enumerate(row) if t >= 0
    }
    outgoing = defaultdict(set)
    for source, action, target in quotient_edges:
        outgoing[source].add((action, target))
    abstract_paths = {
        (source, a, middle, b, target)
        for source, a, middle in quotient_edges
        for b, target in outgoing[middle]
    }
    concrete_paths = {
        (joint_ids[i], a, joint_ids[middle], b, joint_ids[target])
        for i, row in enumerate(transitions)
        for a, middle in enumerate(row) if middle >= 0
        for b, target in enumerate(transitions[middle]) if target >= 0
    }
    assert concrete_paths <= abstract_paths
    false_paths = abstract_paths - concrete_paths
    subsets = [s for size in range(1, 4) for s in combinations(range(3), size)]
    subset_results = {}
    for subset in subsets:
        obs = [tuple(monitors[m][i] for m in subset) for i in range(len(colorings))]
        counts, _ = refine(obs, transitions, range(30))
        subset_results[",".join(CHANNEL_NAMES[m] for m in subset)] = {
            "observed_states": len(set(obs)),
            "fibre_size_histogram": dict(sorted(Counter(Counter(obs).values()).items())),
            "full_alphabet_refinement_counts": counts,
            "full_alphabet_conflicts": transition_conflicts(obs, transitions, range(30)),
        }
    local_results = []
    for m, pairs in enumerate(CHANNELS):
        allowed = [a for a, (p, _) in enumerate(actions) if p in pairs]
        counts, _ = refine(monitors[m], transitions, allowed)
        local_results.append({
            "channel": CHANNEL_NAMES[m],
            "local_actions": [(*PAIRS[p], r) for p, r in (actions[a] for a in allowed)],
            "local_refinement_counts": counts,
            "local_conflicts": transition_conflicts(monitors[m], transitions, allowed),
        })

    frames = defaultdict(list)
    for i, c in enumerate(colorings):
        frames[c[:5]].append(i)
    compatibility = []
    false_product_witness = None
    false_pair_join_witness = None
    for frame, ids in sorted(frames.items()):
        relation = {tuple(monitors[m][i] for m in range(3)) for i in ids}
        marginals = [sorted({monitors[m][i] for i in ids}) for m in range(3)]
        pairs = {(a, b): {(r[a], r[b]) for r in relation}
                 for a, b in combinations(range(3), 2)}
        cartesian = set(product(*marginals))
        pair_join = {r for r in cartesian
                     if all((r[a], r[b]) in proj for (a, b), proj in pairs.items())}
        compatibility.append({
            "frame": frame,
            "proper_colorings": len(ids),
            "marginal_sizes": list(map(len, marginals)),
            "joint_size": len(relation),
            "conditional_product_size": len(cartesian),
            "pairwise_join_size": len(pair_join),
        })
        if false_product_witness is None and cartesian - relation:
            witness = min(cartesian - relation)
            false_product_witness = {
                "frame": frame, "tuple": witness,
                "individual_witnesses": [
                    colorings[next(i for i in ids if monitors[m][i] == witness[m])]
                    for m in range(3)
                ],
                "whole_tuple_has_witness": False,
            }
        if false_pair_join_witness is None and pair_join - relation:
            witness = min(pair_join - relation)
            false_pair_join_witness = {
                "frame": frame, "tuple": witness,
                "pair_witnesses": [
                    {"channels": (a, b), "coloring": colorings[
                        next(i for i in ids if monitors[a][i] == witness[a] and
                             monitors[b][i] == witness[b])]}
                    for a, b in combinations(range(3), 2)
                ],
                "whole_tuple_has_witness": False,
            }
    # The source is complete in each literal boundary fibre, including empties.
    proper_frames = [c for c in product(range(4), repeat=5)
                     if all(c[i] != c[(i+1) % 5] for i in range(5))]
    full_fibres = [
        {"frame": f, "colorings": [colorings[i] for i in frames.get(f, [])]}
        for f in proper_frames
    ]
    # Controls intentionally break one source edge or substitute independent witnesses.
    missing_edge = (5, 6)
    relaxed = [c for c in product(range(4), repeat=n)
               if all(c[u] != c[v] for u, v in edges if (u, v) != missing_edge)]
    invalid = [c for c in relaxed if c[5] == c[6]]
    assert invalid and all(c not in index for c in invalid)
    cross_frame = (monitors[0][0], monitors[1][-1], monitors[2][0])
    assert len({entry[0] for entry in cross_frame}) > 1
    assert all(cross_frame != tuple(monitors[m][i] for m in range(3))
               for i in range(len(colorings)))
    negative_controls = {
        "drop_source_edge": {
            "removed_edge": missing_edge,
            "relaxed_proper_count": len(relaxed),
            "rejected_extra_count": len(invalid),
            "rejected_example": invalid[0],
        },
        "independent_marginals": false_product_witness,
        "pairwise_join": false_pair_join_witness,
        "forget_shared_boundary_frame": {
            "tuple": cross_frame,
            "individual_witnesses": [colorings[0], colorings[-1], colorings[0]],
            "whole_tuple_has_witness": False,
        },
    }
    result = {
        "source_sha256": sha256(raw).hexdigest(),
        "algorithm": "All 4^8 tuples; edge filter; adjacency BFS; direct successor lookup.",
        "cell": "95", "n": n, "boundary": list(range(5)), "edges": edges,
        "proper_coloring_count": len(colorings),
        "all_proper_boundary_frame_count": len(proper_frames),
        "nonempty_boundary_frame_count": len(frames),
        "empty_boundary_frame_count": len(proper_frames) - len(frames),
        "action_order": [(*PAIRS[p], r) for p, r in actions],
        "subsets": subset_results,
        "cross_channel_effects": effects,
        "commutators": commutators,
        "successor_marginal_product": {
            "inflated_source_joint_action_cases": inflated_cases,
            "total_false_successor_tuples_with_multiplicity": inflated_tuples,
        },
        "two_step_quotient_paths": {
            "abstract_observed_paths": len(abstract_paths),
            "concrete_observed_paths": len(concrete_paths),
            "spurious_observed_paths": len(false_paths),
        },
        "local_channels": local_results,
        "compatibility_totals": {
            k: sum(row[k] for row in compatibility)
            for k in ("joint_size", "conditional_product_size", "pairwise_join_size")
        },
        "compatibility_by_frame": compatibility,
        "negative_controls": negative_controls,
        "colorings": colorings,
        "transitions": transitions,
        "joint_monitor_observations": joint,
        "full_fibres": full_fibres,
    }
    certificate = HERE / "independent_certificate.json"
    encoded = (json.dumps(result, indent=2) + "\n").encode()
    if args.check:
        assert certificate.read_bytes() == encoded, "Saved certificate differs."
    else:
        with certificate.open("xb") as stream:
            stream.write(encoded)
    print(json.dumps({k: result[k] for k in (
        "proper_coloring_count", "all_proper_boundary_frame_count",
        "nonempty_boundary_frame_count", "empty_boundary_frame_count",
        "subsets", "local_channels", "compatibility_totals", "negative_controls",
        "cross_channel_effects", "commutators", "successor_marginal_product",
        "two_step_quotient_paths"
    )}, indent=2))


if __name__ == "__main__":
    main()
