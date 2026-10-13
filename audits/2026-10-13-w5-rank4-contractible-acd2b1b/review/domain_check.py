#!/usr/bin/env python3
"""Cross-check both finite domains and every literal geometry, without colours.

This review compares two separately implemented constructors. It does not prove
the source-to-template theorem; structure/ supplies that proof.
"""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def main():
    sys.path.insert(0, str(ROOT / "independent"))
    primary = module("rank4_primary_review", ROOT / "controls/check.py")
    independent = module("rank4_independent_review", ROOT / "independent/check.py")
    domains = []
    for implementation in (primary, independent):
        params = list(implementation.parameters())
        keyed = {independent.key(p): p for p in params}
        assert len(keyed) == len(params), "duplicate parameter key"
        domains.append(keyed)
    assert domains[0].keys() == domains[1].keys(), "different necessary domains"
    counts = Counter()
    families = Counter()
    degrees = Counter()
    digest = hashlib.sha256()
    for key, param in sorted(domains[0].items()):
        record = primary.make(param)
        n, edges, components = independent.graph_from_neighbours(domains[1][key])
        independent.geometry(record, param, n, edges, components)
        counts[(param["c"], param["r"])] += 1
        families[primary.family(param)] += 1
        # Degree flags are independently re-derived from literal G edges.
        dg = [sum(x in e for e in edges) + int(5 <= x < 10)
              for x in range(n)]
        flags = (min(dg[:5]) >= 4, min(dg[5:10]) >= 5)
        degrees[flags] += 1
        digest.update((key + "\n").encode())
    print(json.dumps({
        "status": "PASS domain, original edges, rotations, full degrees",
        "templates": len(domains[0]),
        "parameter_keys_sha256": digest.hexdigest(),
        "counts_c_r": {str(k): v for k, v in sorted(counts.items())},
        "families": dict(sorted(families.items())),
        "flags_B_at_least_4_U_at_least_5": {
            str(k): v for k, v in sorted(degrees.items())
        },
        "source_completeness": "paper proof; not established by this comparison",
        "colour_rows_checked": False,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
