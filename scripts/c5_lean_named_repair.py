#!/usr/bin/env python3
"""Read-only provenance check for the named Lean repair instances.

Lean proves the graph semantics and classification. This check independently
matches the imported literal edges and witness/lift words to the existing source
certificate, including the original named vertex order. It does not prove topology.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path
import re

from c5_two_vertex_repair_sources import CORE_NAMES, TABLE, core_edges

ROOT = Path(__file__).resolve().parents[1]


def declaration(text, name):
    match = re.search(rf"^def {re.escape(name)}\b.*?(?=\n(?:def |instance |theorem |/--|set_option |end )|\Z)",
                      text, re.M | re.S)
    assert match, f"missing declaration {name}"
    return match[0]


def check():
    core = (ROOT / "Math/NamedRepairCore.lean").read_text()
    repair = (ROOT / "Math/NamedRepair.lean").read_text()
    source = json.loads((ROOT / "artifacts/c5_two_vertex_overlap/repair_sources.json").read_text())
    common = json.loads((ROOT / "artifacts/c5_two_vertex_overlap/common_repair.json").read_text())
    edges_text = declaration(core, "coreEdges")
    tokens = re.findall(r"\((\d+|s|t),\s*(\d+|s|t)\)", edges_text)
    assert len(tokens) == 35
    for orientation in TABLE:
        values = {"s": 0 if orientation == "forward" else 2,
                  "t": 2 if orientation == "forward" else 0}
        point = lambda x: values[x] if x in values else int(x)
        edges = {tuple(sorted((point(u), point(v)))) for u, v in tokens}
        assert edges == core_edges(orientation), (orientation, "edge mismatch")
    for name, expected in (
        ("witness", [w for side in ("reverse", "forward") for w, _ in TABLE[side]]),
        ("lifts", [w for side in ("reverse", "forward") for _, ws in TABLE[side] for w in ws]),
    ):
        words = re.findall(r"!\[([0-3](?:,\s*[0-3]){7})\]", declaration(repair, name))
        assert [re.sub(r"\D", "", word) for word in words] == expected, name
    def support(name, rev):
        block = declaration(repair, name)
        text = re.search(r"\{([^{}]+)\}", block)[1]
        named = {"source rev": 2 if rev else 0, "other rev": 0 if rev else 2}
        return tuple(sorted(named[v.strip()] if v.strip() in named else int(v.strip())
                            for v in text.split(",")))

    scopes = list(combinations(range(8), 4))
    for case in common["cases"]:
        if case["name"] not in ("private_interiors", "private_interiors_reverse"):
            continue
        rev = case["name"].endswith("reverse")
        b = scopes.index(tuple(sorted((2 if rev else 0, 5, 6, 7))))
        roles = {"A": scopes.index((0, 1, 2, 3)), "B": b,
                 "T": scopes.index((0, 2, 5, 6)),
                 "E": [i for i, s in enumerate(scopes) if 6 in s and 7 in s and i != b]}
        assert case["ports"] == CORE_NAMES[:8]
        assert case["roles"] == roles
        assert scopes.index(support("scopeA", rev)) == roles["A"]
        assert scopes.index(support("scopeB", rev)) == roles["B"]
        assert scopes.index(support("scopeT", rev)) == roles["T"]
    # The source controls preserve the actual private vertex names as well.
    records = source["cases"] if "cases" in source else source["records"]
    assert all(record["graph"]["vertices"][:15] == CORE_NAMES for record in records)
    for record in records:
        rev = record["orientation"] == "reverse"
        frames = {tuple(sorted(f["cycle"])) for f in record["frame_certificates"] if f["available"]}
        assert frames == {support("frame₁", rev), support("frame₂", rev)}
    print("Lean provenance OK: both 35-edge cores, 6 witnesses, 22 U-lifts, named ports and roles.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    check()
