#!/usr/bin/env python3
"""Exact catalogue implications and NONREALIZED named-relation controls.

No graph search is performed. The catalogue's realizability/completeness bounds
are upstream inputs. --write uses exclusive creation; --check is read-only.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TAUS = list(itertools.product(range(4), repeat=5))


def canonical(t):
    names = {}
    return tuple(names.setdefault(c, len(names)) for c in t)


def proper(t):
    return all(t[j] != t[(j + 1) % 5] for j in range(5))


PATS = sorted({canonical(t) for t in TAUS if proper(t)})


def rotate(t, amount):
    return tuple(t[(j - amount) % 5] for j in range(5))


def bitmask(indices):
    return sum(1 << i for i in indices)


def minimal(masks):
    return [m for m in masks if not any(n != m and n & m == n for n in masks)]


def abstract_control(target, base, catalogue):
    # One named support on B/U only. This is NOT a graph and does not claim
    # planar realizability, attachments, rotation, private vertices or full lifts.
    support = []
    for row in range(10):
        ts = []
        if base >> row & 1:
            ts = [rotate((0, 1, 2, 1, 2), i) for i in range(5)]
        elif target >> row & 1:
            ts = [rotate((0, 1, 2, 1, 2), 4)]
        elif row == 1:
            ts = [rotate((0, 1, 0, 2, 3), i) for i in (0, 1)]
        assert all(proper(t) for t in ts)
        support.append(sorted(set(ts)))

    h = bitmask(i for i, ts in enumerate(support) if ts)
    g = bitmask(i for i, ts in enumerate(support) if any(len(set(t)) == 3 for t in ts))
    qs = [bitmask(i for i, ts in enumerate(support)
                  if any(t[j] == t[(j + 2) % 5] for t in ts)) for j in range(5)]
    fs = [bitmask(i for i, ts in enumerate(support)
                  if any(t[j] != t[(j + 2) % 5] and t[j] != t[(j + 3) % 5]
                         for t in ts)) for j in range(5)]
    assert g == target and h == target | 2
    assert qs == [target | 2, target | 2, base, base, base]
    assert fs == [base | 2] * 4 + [target | 2]
    assert all(m in catalogue for m in [h] + qs + fs)
    for ts in support:
        for t in ts:
            multiplicity = sum(t[j] == t[(j + 2) % 5] for j in range(5))
            assert multiplicity == (2 if len(set(t)) == 3 else 1)
    leak_assignments = sum(len(ts) for i, ts in enumerate(support) if not target >> i & 1)
    assert leak_assignments == 2
    return {
        "status": "triggered and holds: abstract relation arithmetic only",
        "graph_realizability": "not triggered; no realizing graph asserted",
        "target": target,
        "base": base,
        "H_projection": h,
        "Q_projections": qs,
        "fan_projections": fs,
        "wheel_projection": g,
        "forbidden_named_assignments": leak_assignments,
        "support_rows": [{"beta": list(PATS[i]),
                          "nonempty_tau_indices": [TAUS.index(t) for t in ts],
                          "empty_tau_indices": [j for j, t in enumerate(TAUS) if t not in ts]}
                         for i, ts in enumerate(support)],
    }


def certificate():
    raw = (ROOT / "frozen/cells.json").read_bytes()
    manifest = json.loads((ROOT / "INPUTS.json").read_text())
    assert manifest["base"] == "19209f4cf68261fdce5e84a7804cfe04ae0957bf"
    assert manifest["source_path"] == "artifacts/c5_cells/cells.json"
    assert manifest["source_sha256"] == manifest["frozen_sha256"] == hashlib.sha256(raw).hexdigest()
    assert manifest["bytes"] == len(raw) and manifest["source_matches_base_blob"] is True
    data = json.loads(raw)
    assert data["pattern_order"] == [list(p) for p in PATS]
    masks = sorted(map(int, data["cells"]))
    assert len(masks) == 132
    rows = []
    for target, expected_subs, expected_supers in (
        (933, [165], [935,943,951,957,959,997,999,1005,1007,1013,1015,1021,1023]),
        (941, [165,424,429], [943,957,959,1005,1007,1021,1023]),
    ):
        subs = [m for m in masks if m & target == m]
        supers = [m for m in masks if m & target == target]
        assert subs == expected_subs and supers == expected_supers
        trigger_rows = []
        for trigger in (512, 256, 768):
            selected = [m for m in masks if m & trigger == trigger]
            leakage = sorted({m & ~target for m in selected})
            trigger_rows.append({"trigger": trigger, "catalogue_mask_count": len(selected),
                                 "leakage_masks": leakage,
                                 "minimal_leakage_masks": minimal(leakage)})
        assert trigger_rows[0]["minimal_leakage_masks"] == [2,16,64]
        if target == 933:
            assert trigger_rows[1]["minimal_leakage_masks"] == [2,8,64]
            assert trigger_rows[2]["minimal_leakage_masks"] == [2,24,64]
        else:
            assert trigger_rows[1]["minimal_leakage_masks"] == [0]
            assert trigger_rows[2]["minimal_leakage_masks"] == [2,16,64]
        rows.append({"target": target,
                     "source_realizability": "not triggered",
                     "subrelations": subs,
                     "superrelations": supers,
                     "superrelation_leaks": [m & ~target for m in supers],
                     "minimal_superrelation_leaks": minimal(sorted({m & ~target for m in supers})),
                     "triggers": trigger_rows})

    # Every one of the 240 proper rim assignments is checked, independently of
    # the named abstract supports. A three-colour type belongs to adjacent Qs.
    proper_taus = [t for t in TAUS if proper(t)]
    assert len(proper_taus) == 240
    for t in proper_taus:
        equalities = [j for j in range(5) if t[j] == t[(j + 2) % 5]]
        fans = [i for i in range(5)
                if t[i] != t[(i + 2) % 5] and t[i] != t[(i + 3) % 5]]
        if len(set(t)) == 3:
            singleton = next(i for i in range(5) if t.count(t[i]) == 1)
            assert set(equalities) == {(singleton + 1) % 5, (singleton + 2) % 5}
            assert fans == [singleton]
        else:
            assert len(equalities) == 1 and len(fans) == 3
    return {"scope": "finite catalogue arithmetic plus abstract controls; no source graph search",
            "catalogue_source": "artifacts/c5_cells/cells.json",
            "catalogue_sha256": hashlib.sha256(raw).hexdigest(),
            "pattern_order": [list(p) for p in PATS],
            "tau_domain": [list(t) for t in TAUS],
            "catalogue_masks": masks,
            "proper_rim_assignments_checked": len(proper_taus),
            "conditional_catalogue_constraints": rows,
            "abstract_controls": [abstract_control(933, 165, masks),
                                  abstract_control(941, 429, masks)]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    value = certificate()
    path = ROOT / "certificate.json"
    if args.write:
        with path.open("x") as f:
            json.dump(value, f, indent=2)
            f.write("\n")
    else:
        assert json.loads(path.read_text()) == value, "certificate mismatch"
    print("PASS: 132 catalogue masks; 240 proper rim tuples; two exact abstract controls")
    print("933/941 minimum source: not triggered; abstract controls: no graph realization asserted")


if __name__ == "__main__":
    main()
