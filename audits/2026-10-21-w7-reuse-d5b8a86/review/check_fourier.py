#!/usr/bin/env python3
"""Independent affine-subspace review of extracted universal template ranks.

Does not import the template or Fourier probes, and uses only stdlib.  A rank
claim is established from complete coset families in the extracted columns,
without relying on a binomial formula or on floating-point elimination.
"""
from collections import defaultdict
import argparse
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
SOURCE = ROOT / "audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/orbits.json.gz"


def read(path):
    data = path.read_bytes()
    return json.loads(gzip.decompress(data)), hashlib.sha256(data).hexdigest()


def coordinates(encoded):
    t = [0] * 13
    for i in range(12, -1, -1):
        t[i] = encoded & 3
        encoded >>= 2
    q = [x >> 1 for x in t]
    starts = [0] + [i for i in range(1, 13) if q[i] != q[i-1]]
    if q[-1] == q[0]:
        starts.pop()  # The final segment belongs to the run anchored at zero.
    assert len(starts) % 2 == 0
    assert t[starts[0]] % 2 == t[starts[1]] % 2 == 0
    phase = sum((t[i] & 1) << j for j, i in enumerate(starts[2:]))
    return sum(x << i for i, x in enumerate(q)), len(starts) // 2, phase


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true",
                        help="exclusive-create the result; default verifies saved result")
    args = parser.parse_args()
    templates, tsha = read(AUDIT / "templates/templates.json.gz")
    rows, rsha = read(AUDIT / "templates/row_map.json.gz")
    columns, csha = read(AUDIT / "templates/column_map.json.gz")
    source, ssha = read(SOURCE)
    assert ssha == "542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad"
    live = set(source["live"])
    row_source = dict(source["rowids"])
    maps = {}
    for encoded, state, q, k, phase, is_live in rows["rows"]:
        assert coordinates(encoded) == (q, k, phase)
        assert row_source[encoded] == state
        assert bool(is_live) == (state in live)
        assert encoded not in maps
        maps[encoded] = (q, k, phase)
    assert set(maps) == set(row_source)
    cmap = columns["original_column_order"]
    assert len(cmap) == len(source["columns"])
    for frozen_column, (q, k, j) in zip(source["columns"], cmap):
        coords = [maps[h] for h in frozen_column]
        assert all(a == q and b == k for a, b, _ in coords)
        assert sorted(c for _, _, c in coords) == templates[str(k)][j]

    ranks = []
    for kstr, raw_columns in templates.items():
        k = int(kstr)
        n = 1 << (2*k - 2)
        groups = defaultdict(set)
        for raw in raw_columns:
            col = tuple(raw)
            assert col == tuple(sorted(set(col)))
            assert len(col) == 1 << (k - 1)
            subgroup = tuple(sorted(x ^ col[0] for x in col))
            groups[subgroup].add(col)
        union = set()
        for subgroup, cosets in groups.items():
            subgroup_set = set(subgroup)
            assert 0 in subgroup_set
            assert all(a ^ b in subgroup_set for a in subgroup for b in subgroup)
            expected = {tuple(sorted(a ^ b for b in subgroup)) for a in range(n)}
            assert cosets == expected  # Every coset occurs, not merely some columns.
            annihilator = {a for a in range(n)
                           if all((a & b).bit_count() % 2 == 0 for b in subgroup)}
            assert len(annihilator) == n // len(subgroup)
            union.update(annihilator)
        ranks.append(dict(k=k, rows=n, columns=len(raw_columns),
                          complete_coset_families=len(groups),
                          exact_rational_rank=len(union)))
    root_ranks = json.loads((AUDIT / "fourier/ranks.json").read_text())["templates"]
    assert [(r["k"], r["exact_rational_rank"]) for r in ranks] == [
        (r["k"], r["exact_row_rank"]) for r in root_ranks]
    result = dict(status="PASS; structural/rank reconstruction only; no cone verdict",
                  independent_coordinate_checks=len(maps),
                  original_columns_exactly_reconstructed=len(cmap),
                  ranks=ranks, inputs_sha256={"templates": tsha, "rows": rsha,
                                            "columns": csha, "frozen_orbits": ssha})
    destination = HERE / "fourier-review.json"
    if args.build:
        with destination.open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    else:
        assert result == json.loads(destination.read_text()), "saved review differs"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
