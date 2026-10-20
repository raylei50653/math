#!/usr/bin/env python3
"""Independent small contract controls; no graph catalogue search.

--write exclusively creates contract_controls.json. --check is read-only.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FROZEN = HERE.parent / "frozen"
SOURCE = FROZEN / "docs/sources/2026-10-19-c5-grammar-v02/certificate_v02.json"


def require(value, message):
    if not value:
        raise ValueError(message)


def normalize(values):
    names = {}
    return "".join(str(names.setdefault(value, len(names))) for value in values)


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def reconstruct():
    for record in json.loads((HERE / "additional-inputs.json").read_text()):
        raw = (HERE / "frozen" / record["source"]).read_bytes()
        require(sha256(raw).hexdigest() == record["sha256"], "additional input drift")
    model = json.loads(SOURCE.read_bytes())["model"]
    rows = ["".join(map(str, row)) if not isinstance(row, str) else row for row in model["rows"]]
    cycles = [(i, (i + 1) % 5) for i in range(5)]
    proper = [
        values
        for values in product(range(4), repeat=5)
        if all(values[u] != values[v] for u, v in cycles)
    ]
    require(len(proper) == 240, "proper boundary census")
    require(sorted({normalize(values) for values in proper}) == rows, "row order")

    # Compile the two operators from actual boundary colours and new P edges.
    operators = {}
    for letter in ("P", "R"):
        matrix = []
        for word in rows:
            beta = tuple(map(int, word))
            old_rows = (
                [(t,) + beta[1:] for t in range(4) if t not in {beta[0], beta[1], beta[4]}]
                if letter == "P"
                else [beta[1:] + beta[:1]]
            )
            coeff = [0] * 10
            for old in old_rows:
                require(all(old[u] != old[v] for u, v in cycles), "improper source row")
                coeff[rows.index(normalize(old))] += 1
            matrix.append(coeff)
        require(matrix == model["operators"][letter], "literal operator mismatch")
        operators[letter] = matrix

    # Complete literal fibres of C5 plus one internal leaf x adjacent to b0.
    graph_edges = cycles + [(0, 5)]
    fibres = {}
    for values in proper:
        lifts = [
            list(values + (t,))
            for t in range(4)
            if all((values + (t,))[u] != (values + (t,))[v] for u, v in graph_edges)
        ]
        require(len(lifts) == 3, "leaf source does not have exactly three lifts")
        if "".join(map(str, values)) in rows:
            fibres["".join(map(str, values))] = lifts
    leaf_counts = [len(fibres[row]) for row in rows]
    require(leaf_counts == [3] * 10, "leaf canonical count vector")

    # Every P output has an even sum on rows 1, 3, 8, for all integer inputs.
    parity_coeff = [sum(operators["P"][i][j] for i in (1, 3, 8)) for j in range(10)]
    require(parity_coeff == [0, 2, 0, 2, 0, 0, 0, 0, 2, 0], "P parity identity")
    require(sum(leaf_counts[i] for i in (1, 3, 8)) % 2 == 1, "leaf failed parity obstruction")
    require(
        [sum(a * b for a, b in zip(row, leaf_counts)) for row in operators["R"]] == leaf_counts,
        "constant target is not rotation invariant",
    )
    for seed in model["seeds"].values():
        counts = seed["counts"]
        for _ in range(5):
            require(counts != leaf_counts, "zero-P grammar word equals leaf counts")
            counts = [sum(a * b for a, b in zip(row, counts)) for row in operators["R"]]

    catalogue = json.loads((HERE / "frozen/artifacts/c5_cells/cells.json").read_bytes())
    keys = sorted(map(int, catalogue["cells"]))
    require(keys == model["states"], "grammar states do not equal saved catalogue keys")
    require(len(keys) == 132 and 0 not in keys and 932 not in keys, "known catalogue contract")
    require(["".join(map(str, row)) for row in catalogue["pattern_order"]] == rows, "catalogue row order")

    return {
        "scope": "finite literal leaf fibres, integer parity obstruction, and saved set identity; no catalogue completeness proof",
        "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "rows": rows,
        "proper_literal_boundary_count": len(proper),
        "leaf_graph": {"vertices": 6, "boundary": list(range(5)), "edges": graph_edges},
        "leaf_canonical_fibres": fibres,
        "leaf_canonical_counts": leaf_counts,
        "leaf_support": 1023,
        "P_rows_1_3_8_sum_coefficients": parity_coeff,
        "leaf_rows_1_3_8_sum": 9,
        "all_zero_P_seed_rotations_excluded": True,
        "no_FC_PR_count_representative": True,
        "saved_catalogue_equals_grammar_states": True,
        "saved_catalogue_key_count": len(keys),
        "catalogue_completeness_reproved": False,
    }


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=HERE / "contract_controls.json")
    args = parser.parse_args()
    raw = encode(reconstruct())
    target = args.certificate
    if args.write:
        with target.open("xb") as output:
            output.write(raw)
    else:
        require(target.read_bytes() == raw, "contract control bytes differ")
    print("PASS: complete leaf fibres, last-P parity obstruction, saved catalogue identity")


if __name__ == "__main__":
    main()
