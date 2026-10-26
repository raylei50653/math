#!/usr/bin/env python3
"""Replay the same two-colorable planar graph under four resource settings."""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
from four_color_constraints import solve_constraints


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    graph = json.loads((HERE / "grid_6x7.json").read_text())
    known = [(v // 7 + v % 7) % 2 for v in graph["vertices"]]
    assert all(known[u] != known[v] for u, v in graph["edges"])
    modes = dict(default={}, prefix=dict(bucket_method="prefix"),
                 more_rows=dict(max_table_rows=1_000_000),
                 prefix_more_rows=dict(bucket_method="prefix", max_table_rows=1_000_000))
    results = {}
    for name, options in modes.items():
        result = solve_constraints(graph, **options)
        actual = dict(zip(graph["vertices"], result["colors"]))
        valid = (all(type(c) is int and c in range(4) for c in result["colors"])
                 and all(actual[u] != actual[v] for u, v in graph["edges"]))
        expected = "colored" if "more_rows" in name else "limit"
        assert result["status"] == expected
        assert expected != "colored" or valid
        results[name] = dict(options=options, status=result["status"], stats=result["stats"],
                             colors=result["colors"], witness_valid=valid,
                             last_detail=result["events"][-1]["detail"])
        print(name, result["status"], result["stats"]["checks"])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(dict(graph=graph, known_witness=known, results=results),
                                   ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
