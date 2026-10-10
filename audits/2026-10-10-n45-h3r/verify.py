#!/usr/bin/env python3
"""Read-only H3R custody and small abstract/toy controls; no source search."""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
COL = tuple(range(4))
METADATA = {"manifest.json", "delivery.json", "receipts.json"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def custody(check_manifest=True):
    index = json.loads((OUT / "input-index.json").read_text())
    assert len(index["inputs"]) == 14
    for row in index["inputs"]:
        frozen = OUT / row["frozen_path"]
        live = (subprocess.check_output(
            ["git", "show", index["BASE"] + ":" + row["source_path"]], cwd=ROOT)
            if row["layer"] == "base" else (ROOT / row["source_path"]).read_bytes())
        manager = ROOT / "audits/2026-10-10-n45-progress-management/frozen" / row["layer"] / row["source_path"]
        assert sha(live) == sha(frozen.read_bytes()) == sha(manager.read_bytes()) == row["sha256"], row["source_path"]
    if check_manifest:
        manifest = json.loads((OUT / "manifest.json").read_text())
        found = {str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file()
                 and str(p.relative_to(OUT)) not in METADATA}
        assert found == set(manifest["payload"]), (found ^ set(manifest["payload"]))
        for name, expected in manifest["payload"].items():
            assert sha((OUT / name).read_bytes()) == expected, name
        assert manifest["exact_top_level_metadata_exclusions"] == sorted(METADATA)
        digest = sha((OUT / "manifest.json").read_bytes())
        for name in ("delivery.json", "receipts.json"):
            p = OUT / name
            if not p.exists():
                continue
            metadata = json.loads(p.read_text())
            assert metadata["manifest_sha256"] == digest, name
            assert metadata["input_index_sha256"] == sha((OUT / "input-index.json").read_bytes()), name
            assert metadata["certificate_sha256"] == sha((OUT / "abstract-toy-certificate.json").read_bytes()), name
            if name == "receipts.json":
                for receipt in metadata["executions"]:
                    assert sha(receipt["stdout"].encode()) == receipt["stdout_sha256"]
                    assert sha(receipt["stderr"].encode()) == receipt["stderr_sha256"]
                assert metadata["normal_seed17_same_bytes"] is True
    return index


def assignments(names, inner, attachments, gamma):
    """Direct complete assignments; fixed vertex coordinates, no quotients."""
    earlier = {v: [] for v in names}
    for u, v in inner:
        earlier[names[max(names.index(u), names.index(v))]].append(
            names[min(names.index(u), names.index(v))])
    lists = {v: [c for c in COL if c not in {gamma[i] for i in attachments.get(v, [])}]
             for v in names}
    result = []

    def visit(k, f):
        if k == len(names):
            result.append(tuple(f[v] for v in names))
            return
        v = names[k]
        for c in lists[v]:
            if all(f[u] != c for u in earlier[v]):
                f[v] = c
                visit(k + 1, f)
        f.pop(v, None)

    visit(0, {})
    return result


def controls():
    subsets = [set(c for c in COL if mask & (1 << c)) for mask in range(16)]
    covers = sorted((tuple(sorted(c)), tuple(sorted(u))) for c in subsets for u in subsets
                    if len(c) <= 2 and len(u) <= 3 and c | u == set(COL)
                    and c - u and u - c)
    assert len(covers) == 22
    assert all(len(u) >= 2 for c, u in covers)
    assert sorted(set((len(c), len(u)) for c, u in covers)) == [(1, 3), (2, 2), (2, 3)]
    # A joint relation can block colors that independent endpoint marginals miss.
    relation = [(0, 1), (1, 0)]
    true_forbidden = sorted(set.intersection(*(set(t) for t in relation)))
    marginal_product = list(itertools.product(*[sorted({t[i] for t in relation}) for i in range(2)]))
    false_forbidden = sorted(set.intersection(*(set(t) for t in marginal_product)))
    assert true_forbidden == [0, 1] and false_forbidden == []
    triple = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    assert len(set.intersection(*(set(t) for t in triple))) == 3

    # This one fixed graph is an algebra toy, with shared r/s contact p and q0.
    # It is not certified disk, Sigma 933/941, critical, or beta-minimal.
    c_names = ("r", "p", "q0", "q1")
    u_names = ("x0", "x1", "x2")
    names = ("r", "s", "p", "q0", "q1", "x0", "x1", "x2", "w")
    c_edges = [("r", "p"), ("r", "q0"), ("r", "q1"), ("q0", "q1")]
    u_edges = [("x0", "x1"), ("x1", "x2"), ("x2", "x0")]
    contacts = [("s", v) for v in ("p", "q0", "x0", "x1", "x2")]
    attach = {"r": [4], "p": [0, 1], "q0": [2], "q1": [2, 3],
              "x0": [0], "x1": [1], "x2": [4]}
    g_attach = copy.deepcopy(attach)
    g_attach["r"] = [0, 4]
    rows = [g for g in itertools.product(COL, repeat=5)
            if all(g[i] != g[(i + 1) % 5] for i in range(5))]
    assert len(rows) == 240
    totals = {"X_full_lifts": 0, "G_full_lifts": 0, "restore_removed_lifts": 0,
              "ambient_full_fibres": 0, "empty_full_fibres": 0,
              "C_empty_r_tuple_fibres": 0, "U_empty_tuple_fibres": 0}
    row_hashes = []
    for gamma in rows:
        cf = {(a, t): [] for a in COL for t in itertools.product(COL, repeat=2)}
        uf = {t: [] for t in itertools.product(COL, repeat=3)}
        for f in assignments(c_names, c_edges, attach, gamma):
            cf[(f[0], (f[1], f[2]))].append(f)
        for f in assignments(u_names, u_edges, attach, gamma):
            uf[f].append(f)
        joined = {}
        for (a, t), fs in cf.items():
            for v, us in uf.items():
                for d in COL:
                    if d in t or d in v:
                        continue
                    for fc in fs:
                        for fu in us:
                            for z in COL:
                                key = (a, d, *t, *v, z)
                                joined.setdefault(key, set()).add((a, d, *fc[1:], *fu, z))
        direct = {}
        x_lifts = assignments(names, c_edges + u_edges + contacts, attach, gamma)
        for f in x_lifts:
            key = (f[0], f[1], f[2], f[3], f[5], f[6], f[7], f[8])
            direct.setdefault(key, set()).add(f)
        assert joined == direct, gamma
        # All ambient slots, including impossible r pins and empty tuples, exist.
        for key in itertools.product(COL, repeat=8):
            assert joined.get(key, set()) == direct.get(key, set()), (gamma, key)
        g_lifts = set(assignments(names, c_edges + u_edges + contacts, g_attach, gamma))
        restored = {f for f in x_lifts if f[0] != gamma[0]}
        assert g_lifts == restored
        totals["X_full_lifts"] += len(x_lifts)
        totals["G_full_lifts"] += len(g_lifts)
        totals["restore_removed_lifts"] += len(x_lifts) - len(g_lifts)
        totals["ambient_full_fibres"] += 4 ** 8
        totals["empty_full_fibres"] += 4 ** 8 - len(joined)
        totals["C_empty_r_tuple_fibres"] += sum(not fs for fs in cf.values())
        totals["U_empty_tuple_fibres"] += sum(not fs for fs in uf.values())
        row_hashes.append(sha(json.dumps([gamma, sorted(x_lifts), sorted(g_lifts)], separators=(",", ":")).encode()))
    assert totals["restore_removed_lifts"] > 0
    q = (0, 1, 0, 1, 2)
    three = [g for g in rows if len(set(g)) == 3]
    perms = list(itertools.permutations(COL))
    for g in three:
        assert any(tuple(pi[g[(i + shift) % 5]] for i in range(5)) == q
                   for shift in range(5) for pi in perms), g
    t4 = [2, 5, 7, 8, 9]
    rejects = {str(mask): [i for i in range(10) if not mask & (1 << i)] for mask in (933, 941)}
    assert all(mask & (1 << i) for mask in (933, 941) for i in t4)
    return {
        "abstract_irredundant_2_3_cover_count": len(covers),
        "abstract_cover_profiles": [[1, 3], [2, 2], [2, 3]],
        "all_abstract_covers_have_U_at_least_two": True,
        "no_single_contact_capacity_assumed": True,
        "marginal_negative": {"true_F": true_forbidden, "marginal_F": false_forbidden},
        "toy_relation_status": "triggered and holds",
        "toy_is_H3_source": False,
        "toy_proper_literal_rows": len(rows),
        "toy_shared_contact_coordinates": ["p", "q0"],
        "toy_isolated_free_factor_vertex": "w",
        "toy_totals": totals,
        "toy_full_lifts_digest": sha("".join(row_hashes).encode()),
        "three_color_literal_transport_count": len(three),
        "mask_rejected_cells": rejects,
        "finite_H3_source": {"established": False, "executed": False,
                             "status": "not triggered", "trigger_count": None},
        "arbitrary_size_paper_proved_by_python": False,
        "new_Lean": False,
    }


def document_checks():
    # Check authored audit Markdown only; inherited historical links are preserved.
    report = OUT / "REPORT.md"
    body = report.read_text()
    for line in body.splitlines():
        assert line == line.rstrip(), "trailing whitespace"
    for target in re.findall(r"\]\(([^)]+)\)", body):
        if target.startswith("https://") or target.startswith("#"):
            continue
        assert (report.parent / target.split("#", 1)[0]).exists(), target
    judgment = json.loads((OUT / "independent-judgment.json").read_text())
    classifications = json.loads((OUT / "controls.json").read_text())
    assert classifications["certificate_sha256"] == sha((OUT / "abstract-toy-certificate.json").read_bytes())
    for control in classifications["controls"]:
        assert control["status"] in {"triggered and holds", "not triggered", "counterexample"}
    required = {"HIGH3-CORE", "HIGH3-COMPONENT", "HIGH3-JOIN", "HIGH3-RESTORE", "HIGH3-F", "HIGH3-MAP", "HIGH3-SCOPED-CONCLUSION"}
    assert required == {c["id"] for c in judgment["claims"]}
    for claim in judgment["claims"]:
        assert claim["verdict"] == "holds under stated hypotheses"
        assert claim["quantifier"] and claim["K1_K13_used"] and claim["BASE_exact_sections"]
        assert claim["new_sufficient_premises"] == [] and claim["exact_residual"]
    assert judgment["adopted"] is False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preflight", action="store_true")
    ap.add_argument("--negative", action="store_true")
    args = ap.parse_args()
    try:
        index = custody(not args.preflight)
        got = controls()
        if args.preflight:
            print(json.dumps(got, indent=2, sort_keys=True))
            return 0
        expected = json.loads((OUT / "abstract-toy-certificate.json").read_text())
        if args.negative:
            expected["all_abstract_covers_have_U_at_least_two"] = False
        assert got == expected, "abstract/toy certificate mismatch"
        document_checks()
        print(json.dumps({"task": "N45-H3R", "status": "triggered and holds",
                          "scope": "custody, abstract arithmetic and one algebra toy only",
                          "authority_inputs": len(index["inputs"]),
                          "certificate_sha256": sha((OUT / "abstract-toy-certificate.json").read_bytes()),
                          "finite_H3_source_status": "not triggered",
                          "arbitrary_size_paper_proved_by_python": False}, sort_keys=True))
        return 0
    except (AssertionError, OSError, ValueError, subprocess.CalledProcessError) as e:
        print("FAIL: " + str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
