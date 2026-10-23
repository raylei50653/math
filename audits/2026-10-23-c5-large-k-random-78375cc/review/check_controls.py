#!/usr/bin/env python3
"""Replay independently checked positive and deliberately invalid controls."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import independent_check as checker


HERE = Path(__file__).resolve().parent
CATALOGUE = HERE.parent / "frozen/artifacts/c5_cells/cells.json"


def controls():
    data = json.loads(CATALOGUE.read_bytes())
    keys = {int(key) for key in data["cells"]}
    checked_catalogue_rows = 0
    for key, cell in data["cells"].items():
        n = 5 + cell["k_eff"]
        edges = {checker.edge(*pair) for pair in cell["edges"]}
        edges.update(checker.edge(i, (i + 1) % 5) for i in range(5))
        adjacent = [set() for _ in range(n)]
        for u, v in edges:
            adjacent[u].add(v)
            adjacent[v].add(u)
        mask = 0
        for i, word in enumerate(checker.PATTERNS):
            result, _ = checker.solve_row(adjacent, list(range(5)), word)
            if result is not None:
                checker.check_witness(result, n, list(range(5)), word, edges)
                mask |= 1 << i
            checked_catalogue_rows += 1
        assert mask == int(key), (mask, key)

    # Exhaustive lifts on every graph obtained by adding any subset of the
    # five spokes to C5: includes disconnected inner vertex and inconsistent
    # color constraints.  This comparison does not import an existing solver.
    brute_rows = 0
    for spoke_bits in range(32):
        edges = [(i, (i + 1) % 5) for i in range(5)]
        edges.extend((i, 5) for i in range(5) if spoke_bits & (1 << i))
        adjacent = [set() for _ in range(6)]
        for u, v in edges:
            adjacent[u].add(v)
            adjacent[v].add(u)
        for word in checker.PATTERNS:
            brute = [list(map(int, word)) + [c] for c in range(4)
                     if all((list(map(int, word)) + [c])[u]
                            != (list(map(int, word)) + [c])[v] for u, v in edges)]
            exact, _ = checker.solve_row(adjacent, list(range(5)), word)
            assert bool(brute) == (exact is not None), (spoke_bits, word)
            brute_rows += 1

    # Build a real k=25 disk by deterministic face subdivision.  This is only
    # a fixed solver/topology control; it is not part of the random hunt.
    faces = [[i, (i + 1) % 5, 5] for i in range(5)]
    for v in range(6, 30):
        a, b, c = faces.pop(0)
        faces.extend([[a, b, v], [b, c, v], [c, a, v]])
    edges = sorted({checker.edge(face[i], face[(i + 1) % 3])
                    for face in faces for i in range(3)})
    sample = {"k": 25, "n": 30, "boundary": list(range(5)),
              "edges": [list(e) for e in edges], "faces": faces,
              "rows": list(checker.PATTERNS), "sigma": 91, "witnesses": []}
    adjacency = checker.check_disk(sample)
    for word in checker.PATTERNS:
        colors, _ = checker.solve_row(adjacency, sample["boundary"], word)
        sample["witnesses"].append(colors)
    assert checker.check_sample(sample, keys)["status"] == "VERIFIED"
    reversed_sample = deepcopy(sample)
    reversed_sample["faces"] = [list(reversed(f)) for f in sample["faces"]]
    assert checker.check_sample(reversed_sample, keys)["status"] == "VERIFIED"

    rejected_controls = []
    def reject(name, alter):
        bad = deepcopy(sample)
        alter(bad)
        try:
            checker.check_sample(bad, keys)
        except ValueError as exc:
            rejected_controls.append({"name": name, "rejection": str(exc)})
        else:
            raise AssertionError(f"negative control accepted: {name}")

    reject("edge missing", lambda s: s["edges"].pop())
    reject("edge duplicated", lambda s: s["edges"].append(s["edges"][0]))
    reject("face reversed locally", lambda s: s["faces"].__setitem__(0, list(reversed(s["faces"][0]))))
    reject("face duplicated", lambda s: s["faces"].__setitem__(0, s["faces"][1]))
    reject("wrong k", lambda s: s.__setitem__("k", 26))
    reject("boundary order changed", lambda s: s.__setitem__("boundary", [0, 2, 1, 3, 4]))
    reject("rows omitted empty", lambda s: s.__setitem__("rows", [w for i, w in enumerate(checker.PATTERNS) if 91 & (1 << i)]))
    reject("bad full witness", lambda s: s["witnesses"][0].__setitem__(5, s["witnesses"][0][0]))
    reject("missing accepted witness", lambda s: s["witnesses"].__setitem__(0, None))
    reject("false UNSAT", lambda s: (s.__setitem__("sigma", 90), s["witnesses"].__setitem__(0, None)))
    reject("partial witness", lambda s: s["witnesses"][0].pop())

    # A boundary-free nonplanar K5 CSP is unsatisfiable; a tiny search budget
    # must remain unresolved, while the unlimited solver proves UNSAT.
    k5 = [set(range(5)) - {v} for v in range(5)]
    capped, _ = checker.solve_row(k5, [], "", max_nodes=1)
    assert capped == "UNRESOLVED"
    exact, _ = checker.solve_row(k5, [], "")
    assert exact is None
    return {"schema": "c5-independent-checker-controls-v1",
            "catalogue_sha256": sha256(CATALOGUE.read_bytes()).hexdigest(),
            "checked_catalogue_rows": checked_catalogue_rows,
            "brute_force_comparison_rows": brute_rows,
            "positive_topology_controls": 2,
            "negative_controls": rejected_controls,
            "node_limit_distinguishes_unresolved": True,
            "all_passed": True}


if __name__ == "__main__":
    result = controls()
    output = HERE / "controls.json"
    with output.open("x") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result, sort_keys=True))
