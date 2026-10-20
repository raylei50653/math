#!/usr/bin/env python3
"""Rebuild the finite P/R support obstruction from literal local wiring.

Default generation uses exclusive creation. --check is read only. --seed only
changes internal traversal order and must not change the canonical certificate.
This does not enumerate disks or assert that a formal mask has a disk source.
"""
import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
MODEL = AUDIT / "frozen/docs/sources/2026-10-19-c5-grammar-v02/certificate_v02.json"
DEFAULT = HERE / "transition_obstruction.json"
BASE = "9c36e3c4789dfec07d60ec4e042f0bafe17451d1"


def normalize(values):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in values)


def compile_local():
    cycle = [(i, (i + 1) % 5) for i in range(5)]
    rows = sorted({normalize(b) for b in product(range(4), repeat=5)
                   if all(b[u] != b[v] for u, v in cycle)})
    index = {b: i for i, b in enumerate(rows)}
    matrices = {}
    for op, boundary, edges in (
            ("P", (5, 1, 2, 3, 4), cycle + [(5, 0), (5, 1), (5, 4)]),
            ("R", (4, 0, 1, 2, 3), cycle)):
        matrix = []
        for beta in rows:
            counts = [0] * len(rows)
            fixed = dict(zip(boundary, beta))
            missing = sorted(set(range(6 if op == "P" else 5)) - fixed.keys())
            for values in product(range(4), repeat=len(missing)):
                colors = fixed | dict(zip(missing, values))
                if all(colors[u] != colors[v] for u, v in edges):
                    old = normalize(tuple(colors[i] for i in range(5)))
                    counts[index[old]] += 1
            matrix.append(counts)
        matrices[op] = matrix
    fan = sum(1 << i for i, b in enumerate(rows)
              if b[0] != b[2] and b[0] != b[3])
    return rows, matrices, fan


def build(seed):
    rows, matrices, fan = compile_local()
    frozen_bytes = MODEL.read_bytes()
    frozen = json.loads(frozen_bytes)["model"]
    assert ["".join(map(str, r)) for r in rows] == frozen["rows"]
    assert matrices == frozen["operators"], "Local wiring differs from frozen matrices."
    assert fan == frozen["seeds"]["F"]["mask"] == 960
    assert (1 << len(rows)) - 1 == frozen["seeds"]["C"]["mask"] == 1023
    size = 1 << len(rows)
    universe = list(range(size))
    if seed is not None:
        random.Random(seed).shuffle(universe)

    def step(mask, op):
        return sum(int(any(c and mask >> j & 1 for j, c in enumerate(row))) << i
                   for i, row in enumerate(matrices[op]))

    transitions = {s: {op: step(s, op) for op in ("P", "R")} for s in universe}

    def closure(seeds):
        reached = set(seeds)
        pending = deque(sorted(reached))
        while pending:
            for target in transitions[pending.popleft()].values():
                if target not in reached:
                    reached.add(target)
                    pending.append(target)
        return reached

    known = closure([fan])
    assert known == set(frozen["states"]) and len(known) == 132
    assert closure([fan, 1023]) == known
    assert all(transitions[s] == frozen["transitions"][str(s)] for s in known)
    index = {b: i for i, b in enumerate(rows)}

    def act(mask, rotation, reflection):
        result = 0
        for j, row in enumerate(rows):
            if mask >> j & 1:
                transformed = tuple(row[(rotation + (-i if reflection else i)) % 5]
                                    for i in range(5))
                result |= 1 << index[normalize(transformed)]
        return result

    def orbit(mask):
        return sorted({act(mask, r, f) for r in range(5) for f in (False, True)})

    assert all(set(orbit(s)) <= known for s in known)
    preimages = {}
    for op in ("P", "R"):
        pre = defaultdict(list)
        for s in universe:
            pre[transitions[s][op]].append(s)
        entering = sorted(s for s in universe
                          if s not in known and transitions[s][op] in known)
        leaving = sorted(s for s in known if transitions[s][op] not in known)
        preimages[op] = {
            "image_size": len(pre),
            "nonempty_fibre_size_histogram": dict(sorted(Counter(
                map(len, pre.values())).items())),
            "preimage_K_size": len(known) - len(leaving) + len(entering),
            "outside_entering_K": entering,
            "inside_leaving_K": leaving,
            "fibres": {str(t): sorted(pre[t]) for t in sorted(pre)},
        }
    assert preimages["P"]["image_size"] == 640
    assert preimages["P"]["nonempty_fibre_size_histogram"] == {1: 512, 4: 128}
    assert preimages["P"]["preimage_K_size"] == 256
    assert len(preimages["P"]["outside_entering_K"]) == 124
    assert preimages["R"]["preimage_K_size"] == 132
    assert not preimages["P"]["inside_leaving_K"]
    assert not preimages["R"]["inside_leaving_K"]
    assert not preimages["R"]["outside_entering_K"]

    # The only Boolean information loss is on source coordinates 1, 3, 8:
    # all four assignments with at least two true coordinates share one image.
    block = (1 << 1) | (1 << 3) | (1 << 8)
    for fibre in preimages["P"]["fibres"].values():
        if len(fibre) == 4:
            assert len({s & ~block for s in fibre}) == 1
            assert {s & block for s in fibre} == {10, 258, 264, 266}
        else:
            assert len(fibre) == 1

    target_orbits = {str(s): orbit(s) for s in (932, 933, 941)}
    for key in ("933", "941"):
        members = set(target_orbits[key])
        assert not members & known
        assert all(transitions[s]["P"] in known for s in members)
        assert {transitions[s]["R"] for s in members} == members
    out932 = closure([932]) - known
    assert out932 == {932, 63, 249, 459, 599, 858}
    quotient = {str(s): {op: ("K" if t in known else t)
                        for op, t in transitions[s].items()} for s in sorted(out932)}
    assert quotient["932"] == {"P": 63, "R": 932}
    rotation63 = [63]
    for _ in range(4):
        rotation63.append(transitions[rotation63[-1]]["R"])
    assert rotation63 == [63, 459, 599, 249, 858]
    assert transitions[rotation63[-1]]["R"] == 63
    assert [i for i, s in enumerate(rotation63)
            if transitions[s]["P"] in known] == [0, 2, 3]
    assert all(transitions[rotation63[i]]["P"] == rotation63[i] for i in (1, 4))

    # Minimum number of P operations needed to enter K: reverse 0-1 BFS.
    predecessors = defaultdict(list)
    for s in sorted(transitions):
        for op, t in transitions[s].items():
            predecessors[t].append((s, op))
    distance = {s: 0 for s in known}
    pending = deque(sorted(known))
    while pending:
        t = pending.popleft()
        for s, op in predecessors[t]:
            candidate = distance[t] + (op == "P")
            if candidate < distance.get(s, 10**9):
                distance[s] = candidate
                (pending.append if op == "P" else pending.appendleft)(s)
    assert set(distance) == set(range(1, size))
    assert Counter(distance.values()) == {0: 132, 1: 355, 2: 386, 3: 135, 4: 15}
    # Along every edge, d(source) <= cost(edge) + d(target). Telescoping
    # proves a lower bound on the P cost of every path into K.
    assert all(distance[s] <= (op == "P") + distance[t]
               for s in range(1, size) for op, t in transitions[s].items())
    # A separate shortest-letter BFS supplies finite words whose push costs
    # realize the minimum above, eliminating any reliance on numeric labels alone.
    witnesses = {s: "" for s in known}
    pending = deque(sorted(known))
    while pending:
        t = pending.popleft()
        for s, op in predecessors[t]:
            if s not in witnesses and distance[s] == distance[t] + (op == "P"):
                witnesses[s] = op + witnesses[t]
                pending.append(s)
    assert set(witnesses) == set(distance)
    for s, word in witnesses.items():
        result = s
        for op in word:
            result = transitions[result][op]
        assert result in known and word.count("P") == distance[s]
    # For nonempty masks P cannot kill every row; the empty mask is absorbing.
    assert all(transitions[s]["P"] != 0 for s in range(1, size))
    assert transitions[0] == {"P": 0, "R": 0}

    # Extend the exact outside transition table to all five previously reported
    # no4ct Kempe-survivor orbits, without invoking the 4CT exterior screen.
    extra_orbits = {str(s): orbit(s) for s in (7, 63, 932, 933, 941)}
    extra = set().union(*(set(x) for x in extra_orbits.values()))
    assert len(extra) == 21 and not extra & known
    assert all(t in extra | known for s in extra for t in transitions[s].values())
    return {
        "schema": "c5-pr-source-coverage-transition-obstruction/v1",
        "base": BASE,
        "authority": "Formal 1024-mask transition calculation, not source realizability.",
        "input": {
            "path": str(MODEL.relative_to(AUDIT)),
            "sha256": sha256(frozen_bytes).hexdigest(),
        },
        "rows": ["".join(map(str, row)) for row in rows],
        "locally_compiled_matrices": matrices,
        "K132": sorted(known),
        "all_transitions": [[s, transitions[s]["P"], transitions[s]["R"]]
                            for s in sorted(transitions)],
        "preimages": preimages,
        "target_D5_orbits": target_orbits,
        "no4ct_reported_extra_D5_orbits": extra_orbits,
        "extra_transitions": [[s, transitions[s]["P"], transitions[s]["R"]]
                              for s in sorted(extra)],
        "932_outside_quotient": quotient,
        "932_rotation_cycle_after_first_P": rotation63,
        "932_enter_K_on_P_at_rotation_residues": [0, 2, 3],
        "932_stay_outside_on_P_at_rotation_residues": [1, 4],
        "nonzero_basin": {
            "size": len(distance),
            "minimum_P_histogram": dict(sorted(Counter(distance.values()).items())),
            "witnesses": {str(s): {"minimum_P": distance[s], "word": witnesses[s]}
                          for s in sorted(distance)},
        },
        "explicit_countermodels": {
            "reverse_membership": {"source_mask": 941, "P_image": 447,
                                   "same_P_image_known_masks": [935, 943]},
            "arbitrarily_many_pushes_outside": {
                "source_mask": 932, "prefix": "PR", "state": 459, "loop": "P"},
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=DEFAULT)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    result = build(args.seed)
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.check:
        # Literal canonical equality catches mutations in any retained field.
        assert args.certificate.read_text() == encoded, "Certificate mismatch."
    else:
        with args.certificate.open("x") as handle:
            handle.write(encoded)
    print(json.dumps({
        "check": args.check, "seed": args.seed, "masks": 1024, "K": 132,
        "P_image": 640, "P_preimage_K": 256, "P_outside_entering_K": 124,
        "R_preimage_K": 132, "nonzero_basin_K": 1023,
        "933_941_first_P_enters_K": True, "932_first_P_enters_K": False,
        "certificate_sha256": sha256(encoded.encode()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
