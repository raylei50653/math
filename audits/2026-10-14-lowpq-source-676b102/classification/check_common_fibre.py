#!/usr/bin/env python3
"""Independent labelled original-edge replay; no imports from other checkers."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT = HERE / "review-certificate.json"
NAMES = ("z", "s", "r", "t", "q", "ell", "m", "x", "y", "p")
FACE_EDGES = ((0, 1), (1, 2), (2, 3), (3, 0),
              (0, 4), (4, 5), (5, 6), (6, 0))
CAP_EDGES = ((7, 0), (7, 1), (7, 2), (7, 8), (8, 0), (8, 2),
             (8, 3), (9, 0), (9, 4), (9, 5), (9, 6))
SOURCES = (
    "audits/2026-10-14-cofacial-fibres-676b102/pq/PROOF.md",
    "audits/2026-10-14-c4-mask13-joint6-fdd3e22/SOURCE_GEOMETRY.md",
    "audits/2026-10-14-c4-return-branches-a11d4bb/r_high/PROOF.md",
    "audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compute():
    rows = []
    survivors = []
    expected = sorted({tuple(perm[i] for i in (0, 1, 0, 1, 2, 0, 1))
                       for perm in itertools.permutations(range(4))})
    for f in itertools.product(range(4), repeat=7):
        if not f[0] == f[2] == f[5]:
            continue
        if any(f[a] == f[b] for a, b in FACE_EDGES):
            continue
        lifts = []
        for xyp in itertools.product(range(4), repeat=3):
            whole = f + xyp
            if all(whole[a] != whole[b] for a, b in CAP_EDGES):
                lifts.append(xyp)
        assert lifts, "The quotient guard must admit a local full cap lift"
        failed_target = all(set(xyp[:2]) == {f[4], xyp[2]} for xyp in lifts)
        p_lifts = [p for p in range(4) if p not in {f[0], f[4], f[5], f[6]}]
        relation_condition = bool(p_lifts) and f[1] == f[3] and all(
            {f[4], p} == set(range(4)) - {f[0], f[1]} for p in p_lifts)
        assert failed_target == relation_condition
        if failed_target:
            survivors.append(f)
            assert len(lifts) == 2
            assert len(p_lifts) == 1
            assert f[3] == f[6] and f[1] == f[6]
        rows.append({"colours": list(f), "full_lifts_xyp": [list(x) for x in lifts],
                     "p_lifts": p_lifts, "all_target_palettes_equal": failed_target})
    assert survivors == expected
    assert not [f for f in survivors if f[3] != f[6]], "tm edge subbranch survives"
    assert not [f for f in survivors if f[1] != f[6]], "sm edge subbranch survives"
    return {
        "schema": "independent-common-fibre-v1",
        "base": "676b1024715f24a0d969fba90baab21b756406e2",
        "checker_sha256": digest(Path(__file__).resolve()),
        "authority_sha256": {s: digest(ROOT / s) for s in SOURCES},
        "names": list(NAMES),
        "face_edges": [list(e) for e in FACE_EDGES],
        "cap_edges": [list(e) for e in CAP_EDGES],
        "guard": "z=r=ell",
        "summary": {"labelled_assignments": 4**7,
                    "proper_quotient_slice_rows": len(rows),
                    "complete_cap_lifts": sum(len(row["full_lifts_xyp"]) for row in rows),
                    "survivor_labelled_rows": len(survivors),
                    "survivor_complete_cap_lifts": 2 * len(survivors),
                    "survivor_word": "ABABCAB",
                    "tm_edge_survivors": 0, "sm_edge_survivors": 0,
                    "source_realizations_checked": 0},
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=DEFAULT)
    args = parser.parse_args()
    result = compute()
    if args.write:
        with args.certificate.open("x") as stream:
            json.dump(result, stream, indent=2, sort_keys=True)
            stream.write("\n")
    else:
        saved = json.loads(args.certificate.read_text())
        if saved != result:
            raise SystemExit("FAIL: certificate does not match independent original-edge replay")
    print(json.dumps({"status": "PASS", **result["summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
