#!/usr/bin/env python3
"""Complete-component fibre strata and a conditional six-zero J2 theorem.

Default replay is read-only. --build exclusively creates a certificate.
No abstract surviving support is asserted to be an actual graph source.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parent
FROZEN = ROOT / "frozen"
J = "audits/2026-10-20-r6-941-last-rejection-f13eb4d/"
MODEL = J + "frozen/audits/2026-10-19-r6-941-quotients-13dc5ff/A/model.py"


def calculate():
    manifest = {r["path"]: r["sha256"] for r in json.loads((ROOT / "INPUTS.json").read_text())}
    names = [MODEL, J + "J1/certificate.json", J + "J2/certificate.json", J + "SOURCE_CONTRACT.md"]
    digests = {}
    for name in names:
        digest = hashlib.sha256((FROZEN / name).read_bytes()).hexdigest()
        assert digest == manifest[name]
        digests[name] = digest
    spec = importlib.util.spec_from_file_location("frozen_model", FROZEN / MODEL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    j1 = json.loads((FROZEN / (J + "J1/certificate.json")).read_text())
    j2 = json.loads((FROZEN / (J + "J2/certificate.json")).read_text())
    states = [t for t in m.growth(10, four=True) if m.proper(t)]
    K = m.kempe(10, states)
    hindex = {t: i for i, t in enumerate(K["hrows"])}
    live1 = set(j1["final_live"])
    live2 = set(j2["live"])
    assert m.close(K, j1["initial_live"]) == (j1["final_live"], j1["deletion_rounds"])
    assert m.close(K, live2) == (sorted(live2), [])

    def partitions(u, live):
        row = hindex[m.hc(tuple(u))]
        good = [i for i, col in enumerate(K["columns"])
                if all(K["rowids"][r] in live for r, _ in col)]
        return [list(K["descriptions"][i][1]) for i in good
                if any(r == row for r, _ in K["columns"][i])]

    def swap01(u, p):
        return [1 - x if x in (0, 1) and p[i] == p[7] else x for i, x in enumerate(u)]

    strata = []
    for f in j1["component_records"]:
        u = f["core"]
        ps = partitions(u, live1)
        assert sorted(ps) == sorted(f["splits"][0]["partitions"])
        assert len(ps) == 2
        separated, joined = [], []
        target = list(u)
        target[7:9] = reversed(target[7:9])
        for p in ps:
            assert p[0] == p[1] == p[5]
            assert p[7] == p[8]
            split = p[0] != p[7]
            assert split == (p[6] == p[9])
            if split:
                assert [i for i in range(10) if p[i] == p[7]] == [7, 8]
                out = swap01(u, p)
                assert out == target
                assert swap01(out, p) == u
                separated.append(p)
            else:
                assert swap01(u, p) != target
                joined.append(p)
        assert len(separated) == len(joined) == 1
        strata.append({"source": u, "target": target, "separated_partition": separated[0],
                       "joined_partition": joined[0], "map": "entire actual K01(v)"})

    one_sided = []
    forms1 = j1["component_records"]
    for f in forms1:
        if f["core"][4] != 3 or f["core"][6] != 2:
            continue
        closed, rounds = m.close(K, live1 - {f["core_id"]})
        assert len(closed) == 1969
        survivors = [z for z in forms1 if z["core_id"] in closed]
        assert len(survivors) == 4
        assert all(z["core"][7:9] != f["core"][7:9] for z in survivors)
        locking = []
        for z in survivors:
            ps = partitions(z["core"], set(closed))
            assert len(ps) == 1
            assert all(p[0] == p[7] == p[8] and p[6] != p[9] for p in ps)
            locking.append({"core": z["core"], "01_23_partition": ps[0]})
        one_sided.append({"zero_seed": f["core"], "zero_seed_id": f["core_id"],
                          "final_live": closed, "deletion_rounds": rounds,
                          "surviving_locked_fibres": locking})

    forms2 = j2["forms"]
    # Toggle each distinct actual 23 component containing s or t exactly once.
    # The 23 induced graph and both root components are unchanged, so this
    # operation is an involution on complete colourings, not only boundary data.
    def swap23_st(u, p):
        roots = {p[6], p[9]}
        return [5 - x if x in (2, 3) and p[i] in roots else x for i, x in enumerate(u)]

    forms_by_literal = {tuple(f["literal_core"]): f for f in forms2}
    union_bijections = []
    for f in forms2:
        u = f["literal_core"]
        ps = partitions(u, live2)
        assert sorted(ps) == sorted(r["partition"] for r in f["pair_records"][0]["partitions"])
        outputs = []
        for p in ps:
            out = swap23_st(u, p)
            target = forms_by_literal[tuple(out)]
            assert out[6] == out[9] == 5 - u[6]
            assert out[7:9] == u[7:9]
            if f["family"] in (1, 2):
                assert p[4] not in (p[6], p[9])
                assert target["family"] in (1, 2)
                assert out[4] == 3
            else:
                assert p[2] not in (p[6], p[9]) and p[3] not in (p[6], p[9])
                assert target["family"] == 3
            assert swap23_st(out, p) == u
            outputs.append({"partition": p, "target": out, "target_family": target["family"]})
        union_bijections.append({"source": u, "source_family": f["family"], "all_outputs": outputs})
    assert sum(len(r["all_outputs"]) for r in union_bijections) == 64

    # Independent full zero-closure cross-check of the same six-zero implication.
    seed = [f for f in forms2 if f["literal_core"][6] == 2]
    assert len(seed) == 6 and sorted(f["family"] for f in seed) == [1, 1, 2, 2, 3, 3]
    seed_ids = {f["core_index"] for f in seed}
    closed2, rounds2 = m.close(K, live2 - seed_ids)
    assert all(f["core_index"] not in closed2 for f in forms2)
    # Record all covering orbits, each intersecting an already-proved zero,
    # for every deletion witness. This retains the universal quantifier.
    current = live2 - seed_ids
    witnesses2 = []
    for round_index, deletion_round in enumerate(rounds2):
        for core_id, row in deletion_round:
            orbit_witnesses = []
            for i, col in enumerate(K["columns"]):
                if not any(r == row for r, _ in col):
                    continue
                zeros = sorted({K["rowids"][r] for r, _ in col} - current)
                assert zeros
                orbit_witnesses.append({"column": i, "zero_core_ids": zeros})
            assert orbit_witnesses
            witnesses2.append({"round": round_index, "core_id": core_id, "H_row": row,
                               "H_literal": K["hrows"][row], "all_orbits": orbit_witnesses})
        current -= {i for i, _ in deletion_round}
    assert sorted(current) == closed2

    # Keeping either III e-pair alone gives a closed abstract support.
    # This rejects a claimed zero theorem; it is not a source construction.
    controls2 = []
    all_targets2 = {f["core_index"] for f in forms2}
    for e in ((0, 1), (1, 0)):
        keep = {f["core_index"] for f in forms2 if f["family"] == 3
                and tuple(f["literal_core"][7:9]) == e}
        controlled, control_rounds = m.close(K, live2 - (all_targets2 - keep))
        assert len(keep) == 2 and keep <= set(controlled)
        assert not control_rounds
        controls2.append({"only_T_e": e, "only_T_family": 3, "surviving_T_ids": sorted(keep),
                          "final_live": controlled})

    return {"status": "conditional full-source transports and six-zero equivalence; OPEN",
            "source_realized": False, "input_sha256": digests,
            "family_sha256": hashlib.sha256(json.dumps(K["columns"], separators=(",", ":")).encode()).hexdigest(),
            "J1_partial_e_bijections": strata,
            "J1_one_sided_zero_controls": one_sided,
            "J2_d_union_bijections": union_bijections,
            "J2_exact_identity": "N01021(J2)=2*sum_e(I_(2,e)+II_(2,e)+III_(2,e))",
            "J2_six_zero_seeds": [{"core": f["literal_core"], "core_id": f["core_index"],
                                  "family": f["family"]} for f in seed],
            "J2_six_zero_final_live": closed2, "J2_six_zero_rounds": rounds2,
            "J2_all_partition_zero_witnesses": witnesses2,
            "J2_surviving_abstract_controls": controls2,
            "negative_controls": {"universal_e_swap_rejected": True,
                                  "J1_B_zero_equivalence_not_inferred": True,
                                  "J2_actual_zero_not_established": True}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--certificate", type=Path, default=D / "certificate.json")
    args = parser.parse_args()
    out = json.loads(json.dumps(calculate()))
    if args.build:
        with args.certificate.open("x") as f:
            json.dump(out, f, indent=2)
            f.write("\n")
    else:
        assert json.loads(args.certificate.read_text()) == out
    print(json.dumps({"status": "PASS", "J1_partial_bijections": len(out["J1_partial_e_bijections"]),
                      "J2_zero_targets": len(out["J2_six_zero_seeds"]),
                      "J2_rounds": len(out["J2_six_zero_rounds"]),
                      "last_rejection": "OPEN", "source_realized": False}))


if __name__ == "__main__":
    main()
