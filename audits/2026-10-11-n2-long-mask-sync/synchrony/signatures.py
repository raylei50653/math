#!/usr/bin/env python3
"""Five literal two-edge shield arcs; no graph or source enumeration."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ROWS = {0: [0, 1, 2, 1, 2], 1: [0, 1, 2, 0, 2], 3: [0, 1, 0, 2, 1]}
I = {0, 1, 3}


def payload():
    base = json.loads((ROOT / "BASE.json").read_text())
    receipts = []
    for item in base["inputs"]:
        snapshot = ROOT / "frozen" / (item["path"] + ".snapshot")
        raw = snapshot.read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        assert actual == item["sha256"], item["path"]
        assert len(raw) == item["bytes"], item["path"]
        receipts.append({"path": item["path"], "bytes": len(raw), "sha256": actual})
    arcs = []
    for start in range(5):
        vertices = [start, (start + 1) % 5, (start + 2) % 5]
        equal = sorted(i for i in I if ROWS[i][vertices[0]] == ROWS[i][vertices[2]])
        arcs.append({"start": start, "vertices": vertices, "edges": [start, (start + 1) % 5],
                     "Eq": equal, "Diff": sorted(I - set(equal))})
    pairs = []
    for first in range(5):
        for second in range(first + 1, 5):
            a, b = arcs[first], arcs[second]
            if set(a["edges"]) & set(b["edges"]):
                continue
            unions = []
            for am in ["Eq", "Diff"]:
                for bm in ["Eq", "Diff"]:
                    union = set(a[am]) | set(b[bm])
                    unions.append({"first_mask": am, "second_mask": bm,
                                   "union": sorted(union), "common_escape": sorted(I - union),
                                   "covers_I": union == I})
                    if am != bm:
                        assert union != I
            pairs.append({"first": first, "second": second, "mask_unions": unions})
    assert len(pairs) == 5
    assert sum(u["covers_I"] for p in pairs for u in p["mask_unions"]) == 7
    return {"scope": "literal shield-arc signatures only; no local fibres or source realizability",
            "base_head": base["head"], "input_receipts": receipts, "rows": ROWS,
            "arcs": arcs, "edge_disjoint_arc_pairs": pairs,
            "counts": {"arcs": 5, "edge_disjoint_arc_pairs": 5, "mask_unions": 20,
                       "mixed_type_common_escapes": 10, "Eq_Eq_covers": 2, "Diff_Diff_covers": 5}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--artifact", type=Path, default=HERE / "observations.json")
    args = parser.parse_args()
    artifact = args.artifact
    raw = (json.dumps(payload(), ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    if args.check:
        assert artifact.read_bytes() == raw, "artifact mismatch"
    else:
        with artifact.open("xb") as stream:
            stream.write(raw)
    print(json.dumps({"check": args.check, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}))


if __name__ == "__main__":
    main()
