#!/usr/bin/env python3
"""Finite simultaneous Kempe monitors on one frozen cell95 graph.

Independent DFS implementation; no imports from the prior audit's checker.
All coordinates and transition witnesses originate in the same full coloring.
"""
import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random
import tempfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SOURCE = AUDIT / "frozen/audits/2026-10-20-joint-kempe-state-1148ce0/frozen/artifacts/c5_cells/cells.json"
SOURCE_SHA = "04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8"
BASE = "af0df8081e79b51f8b24e17e01b2bd5572e46a0a"
B = tuple(range(5))
PAIRS = tuple(combinations(range(4), 2))
CHANNELS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
ACTIONS = tuple((a, b, r) for a, b in PAIRS for r in B)


def encoded(x):
    return (json.dumps(x, indent=2, sort_keys=True) + "\n").encode()


def classes(keys):
    lookup = {key: i for i, key in enumerate(sorted(set(keys)))}
    return tuple(lookup[key] for key in keys)


def components(c, adjacency, pair):
    unseen = {v for v, color in enumerate(c) if color in pair}
    blocks = []
    while unseen:
        todo = [min(unseen)]
        unseen.remove(todo[0])
        block = []
        while todo:
            v = todo.pop()
            block.append(v)
            for w in adjacency[v]:
                if w in unseen:
                    unseen.remove(w)
                    todo.append(w)
        blocks.append(tuple(sorted(block)))
    return tuple(sorted(blocks))


def collision_stats(ids, transitions, alphabet):
    successor_sets = defaultdict(set)
    for i, row in enumerate(transitions):
        for a in alphabet:
            successor_sets[ids[i], a].add(-1 if row[a] < 0 else ids[row[a]])
    ambiguous = sorted(key for key, values in successor_sets.items() if len(values) > 1)
    sizes = Counter(Counter(ids).values())
    return {
        "classes": len(set(ids)),
        "class_size_histogram": dict(sorted(sizes.items())),
        "ambiguous_classes": len({key[0] for key in ambiguous}),
        "ambiguous_class_action_pairs": len(ambiguous),
        "stable": not ambiguous,
    }


def refine(ids, transitions, alphabet):
    layers = [ids]
    stats = [collision_stats(ids, transitions, alphabet)]
    while not stats[-1]["stable"]:
        ids = classes([
            (ids[i], tuple(-1 if row[a] < 0 else ids[row[a]] for a in alphabet))
            for i, row in enumerate(transitions)
        ])
        layers.append(ids)
        stats.append(collision_stats(ids, transitions, alphabet))
    return layers, stats


def shortest_trace(i, j, ids, transitions, alphabet):
    queue = deque([(i, j, ())])
    seen = {(i, j)}
    while queue:
        x, y, trace = queue.popleft()
        if x < 0 or y < 0:
            if x != y:
                return trace
            continue
        if ids[x] != ids[y]:
            return trace
        for a in alphabet:
            pair = transitions[x][a], transitions[y][a]
            if pair not in seen:
                seen.add(pair)
                queue.append((*pair, trace + (a,)))
    return None


def trace_witness(layers, keys, colors, transitions, alphabet):
    """Choose a same-observation pair split at the deepest refinement round."""
    depth = len(layers) - 1
    if not depth:
        return None
    pair = next(
        (i, j) for i, j in combinations(range(len(colors)), 2)
        if layers[-2][i] == layers[-2][j] and layers[-1][i] != layers[-1][j]
    )
    trace = shortest_trace(*pair, layers[0], transitions, alphabet)
    assert trace is not None and len(trace) == depth
    paths = []
    for start in pair:
        states = [start]
        for a in trace:
            states.append(-1 if states[-1] < 0 else transitions[states[-1]][a])
        paths.append({
            "full_colorings": [None if s < 0 else colors[s] for s in states],
            "observations": [None if s < 0 else keys[s] for s in states],
        })
    return {
        "shortest_distinguishing_length": len(trace),
        "actions": [ACTIONS[a] for a in trace],
        "paths": paths,
    }


def first_collision(ids, keys, colors, transitions, alphabet):
    first = {}
    for i, row in enumerate(transitions):
        for a in alphabet:
            target = row[a]
            label = -1 if target < 0 else ids[target]
            key = ids[i], a
            if key in first and first[key][0] != label:
                _, j, old_target = first[key]
                return {
                    "source1": colors[j], "source2": colors[i],
                    "common_observation": keys[i], "action": ACTIONS[a],
                    "target1": None if old_target < 0 else colors[old_target],
                    "target2": None if target < 0 else colors[target],
                    "target_observation1": None if old_target < 0 else keys[old_target],
                    "target_observation2": None if target < 0 else keys[target],
                }
            first.setdefault(key, (label, i, target))
    return None


def join_rows(rows):
    domains = [sorted({row[k] for row in rows}) for k in range(3)]
    cartesian = set(product(*domains))
    projections = [{(row[a], row[b]) for row in rows} for a, b in combinations(range(3), 2)]
    joined = {
        row for row in cartesian
        if all((row[a], row[b]) in projection
               for (a, b), projection in zip(combinations(range(3), 2), projections))
    }
    return domains, cartesian, joined


def reconstruct(seed=None):
    assert sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA, "frozen source digest mismatch"
    catalog = json.loads(SOURCE.read_text())
    cell = catalog["cells"]["95"]
    n = 5 + cell["k_eff"]
    assert n == 8
    edges = tuple(sorted({tuple(sorted(e)) for e in cell["edges"]} |
                         {tuple(sorted((v, (v + 1) % 5))) for v in B}))
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    candidates = list(product(range(4), repeat=n))
    if seed is not None:
        random.Random(seed).shuffle(candidates)
    colors = tuple(sorted(c for c in candidates if all(c[u] != c[v] for u, v in edges)))
    index = {c: i for i, c in enumerate(colors)}
    blocks = [
        {pair: components(c, adjacency, pair) for pair in PAIRS}
        for c in colors
    ]
    monitors = []
    for channel in CHANNELS:
        monitors.append([
            (c[:5], tuple(tuple(sorted(
                tuple(v for v in block if v in B)
                for block in bs[pair] if any(v in B for v in block)
            )) for pair in channel))
            for c, bs in zip(colors, blocks)
        ])
    monitor_ids = [classes(keys) for keys in monitors]
    monitor_values = [
        tuple(sorted(set(keys))) for keys in monitors
    ]
    transitions = []
    for c, bs in zip(colors, blocks):
        row = []
        for a, b, root in ACTIONS:
            if c[root] not in (a, b):
                row.append(-1)
                continue
            component = next(block for block in bs[(a, b)] if root in block)
            target = tuple(a + b - color if v in component else color for v, color in enumerate(c))
            assert target in index
            row.append(index[target])
        transitions.append(tuple(row))
    transitions = tuple(transitions)
    for i, row in enumerate(transitions):
        assert sum(t >= 0 for t in row) == 15
        for a, target in enumerate(row):
            assert target < 0 or transitions[target][a] == i

    all_actions = tuple(range(len(ACTIONS)))
    subset_results = []
    for size in range(1, 4):
        for subset in combinations(range(3), size):
            keys = [tuple(monitors[k][i] for k in subset) for i in range(len(colors))]
            ids = classes(keys)
            layers, stats = refine(ids, transitions, all_actions)
            subset_results.append({
                "monitors": tuple(k + 1 for k in subset),
                "full_alphabet": {
                    "alphabet_size": 30, "refinement_counts": [s["classes"] for s in stats],
                    "layers": stats,
                    "first_collision": first_collision(ids, keys, colors, transitions, all_actions),
                    "deepest_shortest_trace": trace_witness(layers, keys, colors, transitions, all_actions),
                },
            })
    boundary_keys = [c[:5] for c in colors]
    boundary_ids = classes(boundary_keys)
    boundary_layers, boundary_stats = refine(boundary_ids, transitions, all_actions)
    local_results = []
    for k, channel in enumerate(CHANNELS):
        alphabet = tuple(a for a, action in enumerate(ACTIONS) if action[:2] in channel)
        layers, stats = refine(monitor_ids[k], transitions, alphabet)
        local_results.append({
            "monitor": k + 1, "alphabet": [ACTIONS[a] for a in alphabet],
            "refinement_counts": [s["classes"] for s in stats], "layers": stats,
            "first_collision": first_collision(monitor_ids[k], monitors[k], colors, transitions, alphabet),
        })

    joint_rows = [tuple(ids[i] for ids in monitor_ids) for i in range(len(colors))]
    boundary_groups = defaultdict(list)
    for i, c in enumerate(colors):
        boundary_groups[c[:5]].append(i)
    relation_rows = []
    for beta, indices in sorted(boundary_groups.items()):
        rows = {joint_rows[i] for i in indices}
        domains, cartesian, pair_join = join_rows(rows)
        spurious = sorted(cartesian - rows)
        pair_spurious = sorted(pair_join - rows)
        witness = None
        if spurious:
            fake = spurious[0]
            witness = {
                "triple": fake,
                "observations": [monitor_values[k][fake[k]] for k in range(3)],
                "separate_full_lift_witnesses": [
                    colors[next(i for i in indices if joint_rows[i][k] == fake[k])]
                    for k in range(3)
                ],
                "common_full_lifts": [],
            }
        relation_rows.append({
            "boundary": beta, "full_lifts": [colors[i] for i in indices],
            "marginal_sizes": [len(domain) for domain in domains],
            "genuine_joint_triples": sorted(rows),
            "cartesian_count": len(cartesian), "genuine_count": len(rows),
            "cartesian_spurious_count": len(spurious),
            "pairwise_join_count": len(pair_join),
            "pairwise_join_spurious_count": len(pair_spurious),
            "first_cartesian_spurious": witness,
            "first_pairwise_join_spurious": pair_spurious[0] if pair_spurious else None,
        })

    # Hold the whole observed source triple and literal action fixed; test whether
    # coordinatewise possible successors may be combined independently.
    joint_source_groups = defaultdict(list)
    for i, row in enumerate(joint_rows):
        joint_source_groups[row].append(i)
    dynamics = []
    for source_row, indices in sorted(joint_source_groups.items()):
        for a in all_actions:
            targets = {transitions[i][a] for i in indices}
            if targets == {-1}:
                continue
            assert -1 not in targets
            by_beta = defaultdict(set)
            for target in targets:
                by_beta[colors[target][:5]].add(joint_rows[target])
            for beta, rows in sorted(by_beta.items()):
                domains, cartesian, pair_join = join_rows(rows)
                spurious = sorted(cartesian - rows)
                if spurious:
                    fake = spurious[0]
                    witness = {
                        "source_triple": source_row,
                        "source_full_lifts": [colors[i] for i in indices],
                        "action": ACTIONS[a], "target_boundary": beta,
                        "spurious_target_triple": fake,
                        "genuine_target_triples": sorted(rows),
                        "coordinate_transition_witnesses": [],
                    }
                    for k in range(3):
                        i = next(i for i in indices if transitions[i][a] >= 0 and
                                 joint_rows[transitions[i][a]][k] == fake[k] and
                                 colors[transitions[i][a]][:5] == beta)
                        witness["coordinate_transition_witnesses"].append({
                            "source": colors[i], "target": colors[transitions[i][a]],
                        })
                    dynamics.append({
                        "genuine_count": len(rows), "cartesian_count": len(cartesian),
                        "spurious_count": len(spurious), "pairwise_join_count": len(pair_join),
                        "pairwise_join_spurious_count": len(pair_join - rows),
                        "witness": witness,
                    })

    canonical = []
    by_boundary = {tuple(row["boundary"]): row for row in relation_rows}
    for beta_list in catalog["pattern_order"]:
        beta = tuple(beta_list)
        record = by_boundary.get(beta)
        canonical.append({
            "boundary": beta, "full_lifts": [] if record is None else record["full_lifts"],
            "count": 0 if record is None else len(record["full_lifts"]),
            "marginal_sizes": [0, 0, 0] if record is None else record["marginal_sizes"],
            "genuine_joint_count": 0 if record is None else record["genuine_count"],
            "cartesian_count": 0 if record is None else record["cartesian_count"],
            "cartesian_spurious_count": 0 if record is None else record["cartesian_spurious_count"],
            "pairwise_join_count": 0 if record is None else record["pairwise_join_count"],
            "pairwise_join_spurious_count": 0 if record is None else record["pairwise_join_spurious_count"],
        })
    mask = sum(1 << i for i, row in enumerate(canonical) if row["count"])
    assert mask == 95 and len(colors) == 264 and len(boundary_groups) == 144
    assert sum(row["count"] for row in canonical) * 24 == len(colors)
    relation_totals = {
        "realized_literal_boundaries": len(relation_rows),
        "cartesian_count": sum(row["cartesian_count"] for row in relation_rows),
        "genuine_count": sum(row["genuine_count"] for row in relation_rows),
        "cartesian_spurious_count": sum(row["cartesian_spurious_count"] for row in relation_rows),
        "boundaries_with_cartesian_spurious": sum(row["cartesian_spurious_count"] > 0 for row in relation_rows),
        "pairwise_join_count": sum(row["pairwise_join_count"] for row in relation_rows),
        "pairwise_join_spurious_count": sum(row["pairwise_join_spurious_count"] for row in relation_rows),
    }
    return {
        "claim": "Finite cell95 information audit; not a J1 realization, general closure, or retained-pin theorem.",
        "base": BASE, "source_path": str(SOURCE.relative_to(AUDIT)), "source_sha256": SOURCE_SHA,
        "implementation": "Independent literal product enumeration and DFS maximal components.",
        "n": n, "edges": edges, "boundary": B, "channels": CHANNELS, "actions": ACTIONS,
        "illegal_action_target": -1, "literal_colorings": len(colors),
        "enabled_actions": sum(t >= 0 for row in transitions for t in row),
        "all_colorings": colors, "transitions": transitions,
        "monitor_values": monitor_values, "joint_monitor_rows": joint_rows,
        "complete_canonical_fibres": canonical, "mask": mask,
        "boundary_only": {
            "refinement_counts": [s["classes"] for s in boundary_stats], "layers": boundary_stats,
            "deepest_shortest_trace": trace_witness(boundary_layers, boundary_keys, colors, transitions, all_actions),
        },
        "subset_results": subset_results, "local_alphabet_results": local_results,
        "conditional_relation_totals": relation_totals,
        "conditional_relations": relation_rows,
        "conditional_transition_product": {
            "source_class_action_target_boundary_groups_with_spurious": len(dynamics),
            "spurious_total": sum(row["spurious_count"] for row in dynamics),
            "pairwise_join_spurious_total": sum(row["pairwise_join_spurious_count"] for row in dynamics),
            "first_witness": dynamics[0] if dynamics else None,
        },
        "j1_source_status": "not triggered", "general_multi_monitor_closure": "OPEN",
    }


def verify(certificate, result):
    if certificate.read_bytes() != encoded(result):
        raise ValueError("certificate differs from complete reconstruction")


def negatives(certificate, result):
    """Write deliberately wrong independent copies; preserve the certificate."""
    original_sha = sha256(certificate.read_bytes()).hexdigest()
    cases = []
    for name in ("wrong_count", "drop_empty_fibre", "splice_marginals", "illegal_as_self_loop"):
        bad = json.loads(encoded(result))
        if name == "wrong_count":
            bad["literal_colorings"] += 1
        elif name == "drop_empty_fibre":
            bad["complete_canonical_fibres"] = [x for x in bad["complete_canonical_fibres"] if x["count"]]
        elif name == "splice_marginals":
            # Each coordinate is a real marginal value, but their literal
            # boundary colors differ: this is deliberately not a common frame.
            bad["joint_monitor_rows"][0] = [
                0, len(bad["monitor_values"][1]) - 1, 0,
            ]
        else:
            row = next(i for i, ts in enumerate(bad["transitions"]) if -1 in ts)
            a = bad["transitions"][row].index(-1)
            bad["transitions"][row][a] = row
        with tempfile.TemporaryDirectory(prefix="multi-kempe-negative-") as directory:
            path = Path(directory) / "bad.json"
            path.write_bytes(encoded(bad))
            try:
                verify(path, result)
            except ValueError:
                cases.append({"case": name, "rejected": True})
            else:
                raise AssertionError(f"negative accepted: {name}")
    assert sha256(certificate.read_bytes()).hexdigest() == original_sha
    return {"cases": cases, "saved_certificate_sha256_unchanged": original_sha}


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
    summary = {
        "literal_colorings": result["literal_colorings"], "enabled_actions": result["enabled_actions"],
        "subsets": [
            {"monitors": row["monitors"], "counts": row["full_alphabet"]["refinement_counts"],
             "initial_ambiguity": row["full_alphabet"]["layers"][0]}
            for row in result["subset_results"]
        ],
        "local_alphabet_counts": [row["refinement_counts"] for row in result["local_alphabet_results"]],
        "relation_totals": result["conditional_relation_totals"],
        "transition_products": result["conditional_transition_product"],
        "certificate_sha256": sha256(args.certificate.read_bytes()).hexdigest(),
        "seed": args.seed,
    }
    if args.negative_controls:
        summary["negative_controls"] = negatives(args.certificate, result)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
