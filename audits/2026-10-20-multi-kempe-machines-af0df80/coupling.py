#!/usr/bin/env python3
"""Fixed cell95 cross-channel effects and loss of common successor witnesses."""
import argparse
from collections import defaultdict
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE / "frozen/audits/2026-10-20-joint-kempe-state-1148ce0"
CHANNELS = ((0, 5), (1, 4), (2, 3))
NAMES = ("01|23", "02|13", "03|12")


def model():
    # Reuse the frozen, previously independently checked union-find component
    # routine. Current experiment/ and review/ reconstruct independently.
    spec = importlib.util.spec_from_file_location("frozen_refine", OLD / "refine.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = json.loads((OLD / "refinement.json").read_text())
    edges = data["edges"]
    colors = tuple(c for c in product(range(4), repeat=8)
                   if all(c[u] != c[v] for u, v in edges))
    lookup = {c: i for i, c in enumerate(colors)}
    blocks = [tuple(module.pair_blocks(c, edges, p) for p in module.PAIRS)
              for c in colors]
    parts = [module.signature(c, bs, module.B)[1]
             for c, bs in zip(colors, blocks)]
    sigs = [(c[:5], p) for c, p in zip(colors, parts)]
    channels = [tuple((c[:5], tuple(p[k] for k in ch)) for ch in CHANNELS)
                for c, p in zip(colors, parts)]
    transitions = []
    for c, bs in zip(colors, blocks):
        row = []
        for a, b, root in module.ACTIONS:
            if c[root] not in (a, b):
                row.append(-1)
                continue
            block = next(t for t in bs[module.PAIRS.index((a, b))] if root in t)
            target = tuple(a + b - x if v in block else x for v, x in enumerate(c))
            row.append(lookup[target])
        transitions.append(tuple(row))
    assert len(colors) == 264
    assert sum(t >= 0 for row in transitions for t in row) == 3960
    return module, colors, blocks, parts, sigs, channels, transitions


def generate():
    m, colors, blocks, parts, sigs, channels, trans = model()
    effects = []
    for pair in m.PAIRS:
        acts = [j for j, a in enumerate(m.ACTIONS) if a[:2] == pair]
        counts = [0, 0, 0]
        persistent = [0, 0, 0]
        enabled = 0
        for i, row in enumerate(trans):
            for j in acts:
                target = row[j]
                if target < 0:
                    continue
                enabled += 1
                for k, ch in enumerate(CHANNELS):
                    counts[k] += any(parts[i][p] != parts[target][p] for p in ch)
                    changes = []
                    for p in ch:
                        before = {v: block for block in parts[i][p] for v in block}
                        after = {v: block for block in parts[target][p] for v in block}
                        changes.extend(
                            (before[u] == before[v]) != (after[u] == after[v])
                            for u, v in combinations(sorted(before.keys() & after.keys()), 2)
                        )
                    persistent[k] += any(changes)
        effects.append({"pair": pair, "enabled": enabled,
                        "changed_partition_channel_counts": counts,
                        "persistent_contact_connectivity_changed": persistent})

    buckets = defaultdict(list)
    for i, s in enumerate(sigs):
        buckets[s].append(i)
    joined_cases = false_total = 0
    max_extra = 0
    first_false = None
    for sig, ids in sorted(buckets.items()):
        for j, action in enumerate(m.ACTIONS):
            if trans[ids[0]][j] < 0:
                assert all(trans[i][j] < 0 for i in ids)
                continue
            targets = [trans[i][j] for i in ids]
            actual = {channels[t] for t in targets}
            assert len({colors[t][:5] for t in targets}) == 1
            marginal = [sorted({x[k] for x in actual}) for k in range(3)]
            naive = set(product(*marginal))
            extra = sorted(naive - actual)
            if extra:
                joined_cases += 1
                false_total += len(extra)
                max_extra = max(max_extra, len(extra))
                if first_false is None:
                    first_false = {
                        "source_lifts": [colors[i] for i in ids],
                        "source_signature": sig, "action": action,
                        "actual_target_lifts": [colors[t] for t in targets],
                        "actual_channel_tuples": sorted(actual),
                        "false_channel_tuple": extra[0],
                        "false_tuple_globally_realized": extra[0] in channels,
                    }

    # A quotient path may use one full lift for its first edge and another
    # incompatible lift for its second. Check full intermediate observations.
    key_ids = {sig: i for i, sig in enumerate(sorted(buckets))}
    ids_by_key = [buckets[sig] for sig in sorted(buckets)]
    joint_ids = [key_ids[sig] for sig in sigs]
    quotient = {}
    for q, ids in enumerate(ids_by_key):
        for j in range(len(m.ACTIONS)):
            quotient[q, j] = sorted({joint_ids[trans[i][j]]
                                     for i in ids if trans[i][j] >= 0})
    abstract_paths = concrete_paths = false_paths = 0
    false_trace = None
    for q, ids in enumerate(ids_by_key):
        for j in range(len(m.ACTIONS)):
            for q1 in quotient[q, j]:
                first_lifts = [trans[i][j] for i in ids
                               if trans[i][j] >= 0 and joint_ids[trans[i][j]] == q1]
                for k in range(len(m.ACTIONS)):
                    concrete = {joint_ids[trans[i][k]] for i in first_lifts
                                if trans[i][k] >= 0}
                    possible = set(quotient[q1, k])
                    assert concrete <= possible
                    abstract_paths += len(possible)
                    concrete_paths += len(concrete)
                    extra = sorted(possible - concrete)
                    false_paths += len(extra)
                    if extra and false_trace is None:
                        q2 = extra[0]
                        supplying = next(i for i in ids_by_key[q1]
                                         if trans[i][k] >= 0 and joint_ids[trans[i][k]] == q2)
                        false_trace = {
                            "source_lifts": [colors[i] for i in ids],
                            "first_action": m.ACTIONS[j], "second_action": m.ACTIONS[k],
                            "actual_lifts_after_first": [colors[i] for i in first_lifts],
                            "incompatible_middle_lift": colors[supplying],
                            "false_target_lift": colors[trans[supplying][k]],
                            "actual_final_lifts": [colors[trans[i][k]] for i in first_lifts
                                                   if trans[i][k] >= 0],
                            "middle_signature": sigs[supplying],
                            "false_final_signature": sigs[trans[supplying][k]],
                        }

    commute = {}
    for kind in ("same_pair", "disjoint_pairs", "overlap_one_color"):
        commute[kind] = {"both_orders_legal": 0, "different_full_target": 0,
                         "different_joint_target": 0, "different_boundary": 0}
    mixed_witness = None
    # Unordered pairs of distinct action labels; both evaluation orders tested.
    for i in range(len(colors)):
        for j, k in combinations(range(len(m.ACTIONS)), 2):
            ij, ik = trans[i][j], trans[i][k]
            if min(ij, ik) < 0:
                continue
            ijk, ikj = trans[ij][k], trans[ik][j]
            if min(ijk, ikj) < 0:
                continue
            p, q = set(m.ACTIONS[j][:2]), set(m.ACTIONS[k][:2])
            kind = ("same_pair" if p == q else
                    "disjoint_pairs" if p.isdisjoint(q) else "overlap_one_color")
            row = commute[kind]
            row["both_orders_legal"] += 1
            row["different_full_target"] += ijk != ikj
            row["different_joint_target"] += sigs[ijk] != sigs[ikj]
            row["different_boundary"] += colors[ijk][:5] != colors[ikj][:5]
            if ijk != ikj and mixed_witness is None:
                mixed_witness = {
                    "source": colors[i], "action_a": m.ACTIONS[j],
                    "action_b": m.ACTIONS[k],
                    "a_then_b": colors[ijk], "b_then_a": colors[ikj],
                }

    # Online belief states retain possible complete current colorings.
    # Find an involution that leaves a nonsingleton belief unresolved forever:
    # its observation is uniform after one step, and repeating returns exactly.
    stutter = None
    for sig, ids in sorted(buckets.items()):
        if len(ids) <= 1:
            continue
        for j, action in enumerate(m.ACTIONS):
            targets = [trans[i][j] for i in ids]
            if min(targets) < 0 or len({sigs[t] for t in targets}) != 1:
                continue
            assert all(trans[t][j] == i for i, t in zip(ids, targets))
            stutter = {"source_lifts": [colors[i] for i in ids],
                       "action": action, "after_one": [colors[t] for t in targets],
                       "after_two": [colors[trans[t][j]] for t in targets],
                       "belief_size": len(ids),
                       "one_step_shared_signature": sigs[targets[0]]}
            break
        if stutter:
            break

    return {
        "scope": "Fixed cell95, all 264 literal colorings; B-rooted actions only.",
        "reused_frozen_component_code_sha256": sha256((OLD / "refine.py").read_bytes()).hexdigest(),
        "channel_order": NAMES,
        "cross_channel_effects": effects,
        "successor_marginal_product": {
            "inflated_source_joint_action_cases": joined_cases,
            "total_false_successor_tuples_with_multiplicity": false_total,
            "maximum_extra_in_one_case": max_extra,
            "first_witness": first_false,
        },
        "two_step_quotient_paths": {
            "abstract_observed_paths": abstract_paths,
            "concrete_observed_paths": concrete_paths,
            "spurious_observed_paths": false_paths,
            "first_witness": false_trace,
        },
        "commutators": commute,
        "first_noncommuting_witness": mixed_witness,
        "uninformative_online_cycle": stutter,
        "j1_source_status": "not triggered",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--generate", action="store_true")
    group.add_argument("--check", action="store_true")
    p.add_argument("--certificate", type=Path, default=HERE / "coupling-v2.json")
    args = p.parse_args()
    result = generate()
    raw = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    if args.generate:
        with args.certificate.open("xb") as f:
            f.write(raw)
    elif args.certificate.read_bytes() != raw:
        raise SystemExit("FAIL: coupling certificate differs from reconstruction")
    brief = {k: v for k, v in result.items() if k not in
             ("uninformative_online_cycle", "first_noncommuting_witness")}
    brief["successor_marginal_product"] = {
        k: v for k, v in result["successor_marginal_product"].items()
        if k != "first_witness"}
    brief["two_step_quotient_paths"] = {
        k: v for k, v in result["two_step_quotient_paths"].items()
        if k != "first_witness"}
    print(json.dumps(brief, sort_keys=True))


if __name__ == "__main__":
    main()
