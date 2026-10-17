#!/usr/bin/env python3
"""Replay frozen custody and small parity controls, not source realizability."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
BASE = "3d325d7197aa05815c71bedc52c1b253d736c7bb"
INPUT_SHA = "a559536abe8c7ec256198d9030e1ee2e275193481c7f37e6c2d4c59956944a62"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(u, v):
    return tuple(sorted((u, v)))


def circuit(vertices):
    return {edge(u, v) for u, v in zip(vertices, vertices[1:] + vertices[:1])}


def components(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    unseen = set(range(n))
    result = []
    while unseen:
        todo = [min(unseen)]
        seen = set(todo)
        while todo:
            for v in sorted(adj[todo.pop()] - seen):
                seen.add(v)
                todo.append(v)
        unseen -= seen
        result.append(sorted(seen))
    return result


def perfect_matchings(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    def visit(unmatched, chosen):
        if not unmatched:
            yield set(chosen)
            return
        u = min(unmatched)
        for v in sorted(adj[u] & unmatched):
            yield from visit(unmatched - {u, v}, chosen + [edge(u, v)])

    return list(visit(set(range(n)), []))


def graph_control(name, cycles, matching):
    n = sum(map(len, cycles))
    m = {edge(*e) for e in matching}
    f = set().union(*(circuit(c) for c in cycles))
    d = f | m
    require(not f & m and len(m) * 2 == n, "bad control matching")
    require(sorted(v for e in m for v in e) == list(range(n)), "incomplete matching")
    require(all(sum(v in e for e in d) == 3 for v in range(n)), "not cubic")
    require(len(components(n, d)) == 1, "disconnected control")
    odd = [set(c) for c in cycles if len(c) % 2]
    rows = []
    for r in perfect_matchings(n, d):
        complement = components(n, d - r)
        even = all(len(c) % 2 == 0 for c in complement)
        regions = components(n, d - (m & r))
        odd_counts = [sum(c <= set(w) for c in odd) for w in regions]
        require(sum(odd_counts) == len(odd), "incomplete F region")
        if even:
            require(all(len(w) % 2 == 0 for w in regions), "odd order region")
            require(all(k % 2 == 0 for k in odd_counts), "odd F count in region")
        rows.append({"R": sorted(r), "complement": complement,
                     "even_complement": even, "regions": regions,
                     "odd_F_per_region": odd_counts})
    even_rows = [row for row in rows if row["even_complement"]]
    require(even_rows, "even reference control not triggered")
    if len(cycles) == 2:
        require(all(len(row["regions"]) == 1 for row in even_rows),
                "two total odd circles failed connectedness")
    else:
        require(any(len(row["regions"]) > 1 for row in even_rows),
                "extra even circle boundary not triggered")
    bad_reference = next(row for row in rows if {tuple(e) for e in row["R"]} == m)
    require(not bad_reference["even_complement"] and
            bad_reference["odd_F_per_region"].count(1) == 2,
            "necessity of even reference not triggered")
    return {"name": name, "vertices": n, "D": sorted(d), "M": sorted(m),
            "F_cycles": cycles, "all_references": rows,
            "even_references": len(even_rows),
            "disconnected_even_regions": sum(len(row["regions"]) > 1 for row in even_rows)}


def reconstruct():
    return {"schema": "two-cycle-parity-controls-v1", "base": BASE,
            "scope": "fixed cubic graphs only; not the named minimal source",
            "source_realizability": "not triggered",
            "controls": [
                graph_control("seven-prism", [list(range(7)), list(range(7, 14))],
                              [(i, i + 7) for i in range(7)]),
                graph_control("two-odd-plus-even", [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]],
                              [(0, 3), (1, 4), (2, 6), (5, 8), (7, 9)])]}


def custody(path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == INPUT_SHA, "input manifest changed")
    manifest = json.loads(raw)
    require(manifest["base"] == BASE, "wrong BASE")
    entries = manifest["inputs"]
    require(len(entries) == len({e["path"] for e in entries}) == 13, "incomplete inputs")
    for item in entries:
        p = item["path"]
        frozen = (HERE / "frozen" / p).read_bytes()
        require(len(frozen) == item["bytes"] and
                hashlib.sha256(frozen).hexdigest() == item["sha256"], "frozen drift: " + p)
        require(frozen == subprocess.check_output(["git", "show", BASE + ":" + p], cwd=REPO),
                "wrong BASE bytes: " + p)
        if not item["routing"]:
            require((REPO / p).read_bytes() == frozen, "live authority drift: " + p)
    previous = manifest["previous_audit_inventory"]
    require(len(previous) == len({e["path"] for e in previous}) == 77,
            "incomplete previous audit inventory")
    old_dir = REPO / "audits/2026-10-17-r6-active-f-seven-ffea555"
    require({str(p.relative_to(REPO)) for p in old_dir.rglob("*") if p.is_file()} ==
            {e["path"] for e in previous}, "previous audit membership changed")
    for item in previous:
        raw = (REPO / item["path"]).read_bytes()
        require(len(raw) == item["bytes"] and hashlib.sha256(raw).hexdigest() == item["sha256"],
                "previous audit changed: " + item["path"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=HERE / "INPUTS.json")
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()
    try:
        custody(args.inputs)
        expected = reconstruct()
        if args.write_certificate:
            with args.certificate.open("x") as stream:
                json.dump(expected, stream, indent=2, sort_keys=True)
                stream.write("\n")
        else:
            require(json.loads(args.certificate.read_text()) == json.loads(json.dumps(expected)),
                    "certificate differs from complete reconstruction")
        print(json.dumps({"base": BASE, "frozen_inputs": 13, "previous_audit_files": 77,
                          "drift": [], "source_realizability": "not triggered",
                          "controls": [{k: c[k] for k in ["name", "even_references", "disconnected_even_regions"]}
                                       for c in expected["controls"]]}, sort_keys=True))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
