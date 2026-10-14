#!/usr/bin/env python3
"""Read-only check of the actual Lean graft edges against the named sources.

Lean proves the colouring semantics. This check evaluates its concrete edge
lists and matches both orientations and all four first-layer modes to the
original Python construction, preserving literal vertex names. No enumeration
of colourings, topology claim, or artifact rewrite is performed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import tempfile

from c5_two_vertex_repair_caps import EDGES
from c5_two_vertex_repair_sources import core_edges

ROOT = Path(__file__).resolve().parents[1]
EXTERIOR = [*range(8), 9, 10, 11, 12, 14]
RIMS = ((10, 2, 12, 0), (7, 6, 14, 5))
CENTRES = (8, 13)
PREFIX = "named-replacement:"


def expected_graph(orientation: str, cap_a: bool, cap_b: bool):
    edges = set(core_edges(orientation))
    vertices = list(EXTERIOR)
    next_vertex = 15
    for enabled, centre, rim in zip((cap_a, cap_b), CENTRES, RIMS):
        neighbours = {v if u == centre else u for u, v in edges if centre in (u, v)}
        assert neighbours == set(rim), (orientation, centre, "unsealed centre")
        vertices.append(centre)
        if enabled:
            new_vertices = list(range(next_vertex, next_vertex + 8))
            vertices.extend(new_vertices)
            mapping = [*rim, centre, *new_vertices]
            edges = {e for e in edges if centre not in e}
            edges.update(tuple(sorted((mapping[u], mapping[v]))) for u, v in EDGES)
            next_vertex += 8
    return vertices, edges


def lean_edges():
    commands = ["import Math.NamedRepairReplacement", "open FiveBoundary.NamedRepairReplacement"]
    for rev in (False, True):
        for cap_a in (False, True):
            for cap_b in (False, True):
                tag = f"{int(rev)}{int(cap_a)}{int(cap_b)}"
                flags = [str(v).lower() for v in (rev, cap_a, cap_b)]
                edges = f"graftEdges {flags[0]} (patchEdges {flags[1]}) (patchEdges {flags[2]})"
                count = f"13 + (tailSize {flags[1]} + tailSize {flags[2]})"
                commands.append(
                    f'#eval IO.println ("{PREFIX}{tag}:" ++ '
                    f'(Lean.Json.arr #[Lean.toJson ({count}), '
                    f'Lean.Json.arr (({edges}).map (fun e => '
                    "Lean.Json.arr #[Lean.toJson e.1.val, Lean.toJson e.2.val])).toArray]).compress)"
                )
    with tempfile.TemporaryDirectory(prefix="math-named-replacement-") as temporary:
        probe = Path(temporary) / "Edges.lean"
        probe.write_text("\n".join(commands) + "\n")
        result = subprocess.run(
            ["lake", "env", "lean", "-j", "1", str(probe)], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
    if result.returncode:
        raise RuntimeError(
            "Lean edge evaluation failed; build Math.NamedRepairReplacement first.\n"
            + result.stdout + result.stderr
        )
    records = {}
    for line in result.stdout.splitlines():
        if line.startswith(PREFIX):
            tag, data = line[len(PREFIX):].split(":", 1)
            assert tag not in records, (tag, "duplicate Lean output")
            records[tag] = json.loads(data)
    assert len(records) == 8, ("missing Lean graph outputs", records.keys())
    return records


def check():
    records = lean_edges()
    for rev in (False, True):
        orientation = "reverse" if rev else "forward"
        for cap_a in (False, True):
            for cap_b in (False, True):
                tag = f"{int(rev)}{int(cap_a)}{int(cap_b)}"
                vertices, expected = expected_graph(orientation, cap_a, cap_b)
                count, raw = records[tag]
                assert count == len(vertices), (tag, "vertex count mismatch", count)
                assert all(0 <= u < len(vertices) and 0 <= v < len(vertices) and u != v
                           for u, v in raw), (tag, "invalid endpoint")
                actual = {tuple(sorted((vertices[u], vertices[v]))) for u, v in raw}
                assert actual == expected, (tag, "edge mismatch", actual ^ expected)
                caps = int(cap_a) + int(cap_b)
                assert len(vertices) == 15 + 8 * caps
                assert len(actual) == 35 + 24 * caps
                assert len(raw) == len(actual) + 8, (tag, "unexpected rim duplication")
                # In particular the first eight vertices remain the original U.
                assert vertices[:8] == list(range(8)) and len(set(vertices)) == len(vertices)
    print("Lean replacement provenance OK: 8 actual graphs, both orientations; "
          "15/35, 23/59, 31/83 vertices/edges; literal U, ordered ports and sealed centres.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    check()
