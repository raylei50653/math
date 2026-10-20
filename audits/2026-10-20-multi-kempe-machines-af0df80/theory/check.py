#!/usr/bin/env python3
"""Independent fixed-graph checks for the three-observer paper contract."""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / (
    "frozen/audits/2026-10-20-joint-kempe-state-1148ce0/"
    "frozen/artifacts/c5_cells/cells.json"
)
SOURCE_SHA256 = "04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8"
B = tuple(range(5))
PAIRS = tuple(combinations(range(4), 2))
CHANNELS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def components(c, pair, adjacency):
    remaining = {v for v, color in enumerate(c) if color in pair}
    result = []
    while remaining:
        root = min(remaining)
        remaining.remove(root)
        reached = {root}
        queue = [root]
        while queue:
            v = queue.pop()
            new = adjacency[v] & remaining
            remaining -= new
            reached |= new
            queue.extend(new)
        result.append(tuple(sorted(reached)))
    return tuple(sorted(result))


def boundary_partition(c, pair, adjacency):
    return tuple(sorted(
        block
        for comp in components(c, pair, adjacency)
        if (block := tuple(v for v in comp if v in B))
    ))


def observer(c, channel, adjacency):
    return c[:5], tuple(boundary_partition(c, pair, adjacency) for pair in channel)


def step(c, pair, root, adjacency):
    if c[root] not in pair:
        return None
    block = next(comp for comp in components(c, pair, adjacency) if root in comp)
    return tuple(sum(pair) - color if v in block else color
                 for v, color in enumerate(c))


def main():
    assert sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256
    cell = json.loads(SOURCE.read_text())["cells"]["95"]
    n = 5 + cell["k_eff"]
    assert n == 8
    edges = sorted({tuple(sorted(e)) for e in cell["edges"]} |
                   {tuple(sorted((v, (v + 1) % 5))) for v in B})
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colors = tuple(c for c in product(range(4), repeat=n)
                   if all(c[u] != c[v] for u, v in edges))
    assert len(colors) == 264
    checked = []
    for channel in CHANNELS:
        outputs = defaultdict(set)
        for c in colors:
            o = observer(c, channel, adjacency)
            for pair, root in product(channel, B):
                target = step(c, pair, root, adjacency)
                target_o = None if target is None else observer(target, channel, adjacency)
                outputs[o, pair, root].add(target_o)
                if target is not None:
                    assert target_o[1] == o[1]
        assert all(len(values) == 1 for values in outputs.values())
        checked.append(len(outputs))

    c = tuple(map(int, "01012132"))
    d = tuple(map(int, "01012233"))
    joint = lambda state: tuple(observer(state, channel, adjacency) for channel in CHANNELS)
    assert joint(c) == joint(d)
    cp = step(c, (1, 2), 1, adjacency)
    dp = step(d, (1, 2), 1, adjacency)
    assert cp == tuple(map(int, "02012231"))
    assert dp == tuple(map(int, "02012233"))
    assert joint(cp) != joint(dp)
    assert observer(cp, CHANNELS[2], adjacency) == observer(dp, CHANNELS[2], adjacency)
    assert observer(cp, CHANNELS[0], adjacency) != observer(dp, CHANNELS[0], adjacency)

    # The abstract middle class also contains a state unavailable after observing
    # this first move from the initial joint class. Splicing it breaks involution.
    initial_fibre = {state for state in colors if joint(state) == joint(c)}
    assert initial_fibre == {c, d}
    middle = tuple(map(int, "02012133"))
    false_target = tuple(map(int, "01012133"))
    assert joint(middle) == joint(cp)
    actual_middle = {step(state, (1, 2), 1, adjacency) for state in initial_fibre}
    filtered_middle = {state for state in actual_middle if joint(state) == joint(cp)}
    assert filtered_middle == {cp}
    assert middle not in actual_middle
    assert step(middle, (1, 2), 1, adjacency) == false_target
    assert joint(false_target) != joint(c)
    assert {step(state, (1, 2), 1, adjacency) for state in filtered_middle} == {c}
    assert all(step(step(state, (1, 2), 1, adjacency), (1, 2), 1, adjacency) == state
               for state in initial_fibre)

    # An arbitrarily long actual history need not distinguish an initial fibre.
    cycle_targets = {step(state, (0, 1), 0, adjacency) for state in initial_fibre}
    assert len(cycle_targets) == 2
    assert len({joint(state) for state in cycle_targets}) == 1
    assert {step(state, (0, 1), 0, adjacency) for state in cycle_targets} == initial_fibre

    alpha = ((0, 1), 0)
    beta = ((1, 2), 4)
    alpha_beta = step(step(c, *alpha, adjacency), *beta, adjacency)
    beta_alpha = step(step(c, *beta, adjacency), *alpha, adjacency)
    assert alpha_beta == tuple(map(int, "20201031"))
    assert beta_alpha == tuple(map(int, "10120032"))
    assert alpha_beta != beta_alpha
    print(json.dumps({
        "status": "PASS",
        "source_sha256": SOURCE_SHA256,
        "literal_colorings": len(colors),
        "own_alphabet_class_action_checks": checked,
        "own_alphabet_closure": True,
        "same_witness_product_collision_reproduced": True,
        "quotient_two_step_splice_breaks_concrete_involution": True,
        "arbitrarily_long_uninformative_online_cycle": True,
        "mixed_actions_both_orders_legal_noncommuting": True,
        "scope": "fixed cell95 only; paper own-alphabet proof is separate",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
