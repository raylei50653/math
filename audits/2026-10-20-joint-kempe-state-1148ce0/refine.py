#!/usr/bin/env python3
"""Fixed cell95: literal exhaustive states, retained pins, and Moore refinement.

Independent of experiment/check.py: exhaustive 4^8 products and edge-union DSU.
No graph search, global color normalization, or general sufficiency assertion.
"""
import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "frozen/artifacts/c5_cells/cells.json"
PAIRS = tuple(combinations(range(4), 2))
B = tuple(range(5))
ACTIONS = tuple((a, b, r) for a, b in PAIRS for r in B)


def pair_blocks(c, edges, pair):
    vertices = [v for v, x in enumerate(c) if x in pair]
    parent = {v: v for v in vertices}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for u, v in edges:
        if u in parent and v in parent:
            a, b = find(u), find(v)
            parent[max(a, b)] = min(a, b)
    groups = defaultdict(list)
    for v in vertices:
        groups[find(v)].append(v)
    return tuple(sorted(tuple(x) for x in groups.values()))


def signature(c, blocks, ports):
    retained = set(ports)
    parts = tuple(
        tuple(sorted(x for block in family
                     if (x := tuple(v for v in block if v in retained))))
        for family in blocks
    )
    return tuple(c[v] for v in ports), parts


def classes(keys):
    ids = {key: i for i, key in enumerate(sorted(set(keys)))}
    return tuple(ids[key] for key in keys)


def stability(ids, transitions, colors):
    first = {}
    bad = set()
    witness = None
    for i, row in enumerate(transitions):
        for j, target in enumerate(row):
            observation = -1 if target < 0 else ids[target]
            key = ids[i], j
            if key not in first:
                first[key] = (observation, i, target)
            elif first[key][0] != observation:
                bad.add(key)
                if witness is None:
                    _, old_i, old_target = first[key]
                    witness = {
                        "source1": colors[old_i], "source2": colors[i],
                        "action": ACTIONS[j],
                        "target1": None if old_target < 0 else colors[old_target],
                        "target2": None if target < 0 else colors[target],
                    }
    return {
        "classes": len(set(ids)),
        "conflicting_class_action_pairs": len(bad),
        "stable": not bad,
        "first_collision": witness,
    }


def generate():
    catalog = json.loads(SOURCE.read_text())
    cell = catalog["cells"]["95"]
    n = 5 + cell["k_eff"]
    assert n == 8
    edges = sorted({tuple(sorted(e)) for e in cell["edges"]} |
                   {tuple(sorted((v, (v + 1) % 5))) for v in B})
    colors = tuple(c for c in product(range(4), repeat=n)
                   if all(c[u] != c[v] for u, v in edges))
    index = {c: i for i, c in enumerate(colors)}
    blocks = [tuple(pair_blocks(c, edges, pair) for pair in PAIRS) for c in colors]
    transitions = []
    for c, all_blocks in zip(colors, blocks):
        row = []
        for a, b, root in ACTIONS:
            if c[root] not in (a, b):
                row.append(-1)
                continue
            block = next(x for x in all_blocks[PAIRS.index((a, b))] if root in x)
            target = tuple(a + b - x if v in block else x for v, x in enumerate(c))
            assert all(target[u] != target[v] for u, v in edges)
            row.append(index[target])
        transitions.append(tuple(row))

    results = []
    for size in range(4):
        for pins in combinations(range(5, 8), size):
            ports = B + pins
            keys = [signature(c, bs, ports) for c, bs in zip(colors, blocks)]
            ids = classes(keys)
            result = stability(ids, transitions, colors)
            result["pins"] = pins
            result["ports"] = ports
            results.append(result)
    successful = [x["pins"] for x in results if x["stable"]]
    minimum = min(map(len, successful))

    keys = [signature(c, bs, B) for c, bs in zip(colors, blocks)]
    ids = classes(keys)
    steps = [len(set(ids))]
    while True:
        next_ids = classes([
            (ids[i], tuple(-1 if t < 0 else ids[t] for t in row))
            for i, row in enumerate(transitions)
        ])
        count = len(set(next_ids))
        if count == steps[-1]:
            assert stability(next_ids, transitions, colors)["stable"]
            break
        steps.append(count)
        ids = next_ids

    # Separate boundary-only observation refinement in the same exact action system.
    out_ids = classes([c[:5] for c in colors])
    boundary_steps = [len(set(out_ids))]
    while True:
        next_ids = classes([
            (out_ids[i], tuple(-1 if t < 0 else out_ids[t] for t in row))
            for i, row in enumerate(transitions)
        ])
        count = len(set(next_ids))
        if count == boundary_steps[-1]:
            assert stability(next_ids, transitions, colors)["stable"]
            break
        boundary_steps.append(count)
        out_ids = next_ids

    fibres = []
    for beta in catalog["pattern_order"]:
        lifts = [c for c in colors if c[:5] == tuple(beta)]
        fibres.append({"boundary": beta, "full_lifts": lifts, "count": len(lifts)})
    mask = sum(1 << i for i, f in enumerate(fibres) if f["count"])
    assert mask == 95
    assert len(colors) == 24 * sum(x["count"] for x in fibres)
    return {
        "claim": "Finite cell95 only; action roots remain original B for every pin set.",
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "n": n, "edges": edges, "boundary": B, "actions": ACTIONS,
        "literal_colorings": len(colors),
        "all_colorings_sha256": sha256(json.dumps(colors).encode()).hexdigest(),
        "enabled_actions": sum(t >= 0 for row in transitions for t in row),
        "complete_canonical_fibres": fibres,
        "pin_results": results, "minimum_added_pins": minimum,
        "minimum_sufficient_pin_sets": [p for p in successful if len(p) == minimum],
        "joint_signature_refinement_counts": steps,
        "boundary_observation_refinement_counts": boundary_steps,
        "stable_refinement_depth": len(steps) - 1,
        "j1_source_status": "not triggered",
        "general_retained_pin_bound": "OPEN",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--generate", action="store_true")
    group.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "refinement.json")
    args = parser.parse_args()
    result = generate()
    data = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    if args.generate:
        with args.certificate.open("xb") as stream:
            stream.write(data)
    else:
        if args.certificate.read_bytes() != data:
            raise SystemExit("FAIL: refinement certificate differs from complete reconstruction")
    print(json.dumps({key: result[key] for key in (
        "literal_colorings", "enabled_actions", "minimum_added_pins",
        "minimum_sufficient_pin_sets", "joint_signature_refinement_counts",
        "boundary_observation_refinement_counts",
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
