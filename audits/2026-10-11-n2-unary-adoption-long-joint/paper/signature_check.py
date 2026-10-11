#!/usr/bin/env python3
"""Independent literal-C5 arithmetic and exact frozen-input verification.

No author checker imports, source enumeration, normalization, or graph edits.
The finite arithmetic does not verify the arbitrary-size block-tree proof.
"""
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = AUDIT.parent.parent
ROWS = ((0, 1, 2, 1, 2), (0, 1, 2, 0, 2), (0, 1, 0, 2, 1))
EDGES = ((0, 1), (1, 2), (2, 3), (3, 4), (4, 0))
NAMES = ("01", "12", "23", "34", "40")
USED = frozenset((0, 1, 2))


def only(values):
    assert len(values) == 1
    return next(iter(values))


def build():
    point_signatures = tuple(tuple(row[v] for row in ROWS) for v in range(5))
    edge_signatures = tuple(
        tuple(only(USED - {row[a], row[b]}) for row in ROWS)
        for a, b in EDGES
    )
    assert len(set(point_signatures)) == 5
    assert len(set(edge_signatures)) == 5
    pairs = []
    for e, f in itertools.product(range(5), repeat=2):
        if all(edge_signatures[e][i] != edge_signatures[f][i] for i in range(3)):
            third = tuple(
                only(USED - {edge_signatures[e][i], edge_signatures[f][i]})
                for i in range(3)
            )
            assert third not in point_signatures
            pairs.append({"edges": [NAMES[e], NAMES[f]], "third": third})
    assert len(pairs) == 4
    triples = []
    for triple in itertools.combinations(range(5), 3):
        choices = [
            sorted(USED - {edge_signatures[e][i] for e in triple})
            for i in range(3)
        ]
        palettes = []
        for c in itertools.product(*choices):
            required = {
                NAMES[e]: tuple(
                    only(USED - {c[i], edge_signatures[e][i]})
                    for i in range(3)
                )
                for e in triple
            }
            missing = [name for name, sig in required.items() if sig not in point_signatures]
            assert missing
            palettes.append({"c": c, "required": required, "missing": missing})
        triples.append({"edges": [NAMES[e] for e in triple], "palettes": palettes})
    assert len(triples) == 10
    assert sum(not item["palettes"] for item in triples) == 8
    assert sum(len(item["palettes"]) for item in triples) == 2
    base = json.loads((AUDIT / "BASE.json").read_text())
    inputs = []
    for entry in base["inputs"]:
        frozen = REPO / entry["snapshot"]
        data = frozen.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == entry["sha256"]
        assert len(data) == entry["bytes"]
        inputs.append({
            "path": entry["path"], "frozen_sha256": digest,
            "frozen_bytes": len(data), "frozen_matches_BASE": True,
        })
    return {
        "scope": "Literal ordered q0,q1,q3 signatures and exact frozen inputs only",
        "head": base["head"],
        "rows": ROWS,
        "points": {str(v): point_signatures[v] for v in range(5)},
        "edges": dict(zip(NAMES, edge_signatures)),
        "ordered_different_pairs": pairs,
        "unordered_triples": triples,
        "inputs": inputs,
        "external_pdf_sha256": hashlib.sha256((HERE / "gallai.pdf").read_bytes()).hexdigest(),
        "target_source_status": "not triggered; no new target realization or source enumeration",
        "arbitrary_size_proof": "See independent_review.md; not checked by this script",
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    path = HERE / "signature_check_final.json"
    if args.check:
        assert json.loads(path.read_text()) == json.loads(json.dumps(result))
    else:
        with path.open("x") as out:
            json.dump(result, out, indent=2, sort_keys=True)
            out.write("\n")
    print("PASS: 25 ordered pairs, 4 differing; 10 distinct triples, 0 feasible; 11 frozen inputs match BASE")
