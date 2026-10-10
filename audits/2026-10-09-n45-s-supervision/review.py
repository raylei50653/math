#!/usr/bin/env python3
"""Independent N45-S bounded review; never imports either delivered checker.

Reads S/J evidence and BASE Git objects. Does not prove the paper topology.
Writes only the explicitly requested fresh review output, with exclusive create.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
S = ROOT / "audits/2026-10-09-n45-s"
J = ROOT / "audits/2026-10-09-n45-j"
BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"
COL = set(range(4))
PAIRS = set(itertools.product(range(4), repeat=2))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(directory):
    return {str(p.relative_to(directory)): {"sha256": sha(p.read_bytes()),
            "bytes": p.stat().st_size, "mtime_ns": p.stat().st_mtime_ns}
            for p in sorted(directory.rglob("*")) if p.is_file()}


def load(path):
    return json.loads(path.read_text())


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def full_root_pairs(vertices, edges, beta, roots):
    """Fixed vertex order, forward checking; exhausts all complete colourings."""
    position = {v: i for i, v in enumerate(vertices)}
    neighbours = [set() for _ in vertices]
    for u, v in edges:
        neighbours[position[u]].add(position[v])
        neighbours[position[v]].add(position[u])
    colours = [-1] * len(vertices)
    for v, c in enumerate(beta):
        colours[position[v]] = c
    assert all(colours[position[u]] != colours[position[v]]
               for u, v in edges if u < 5 and v < 5)
    order = [position[v] for v in vertices if v >= 5]
    answers = set()

    def visit(depth):
        if depth == len(order):
            answers.add(tuple(colours[position[r]] for r in roots))
            return
        v = order[depth]
        for c in range(4):
            if any(colours[w] == c for w in neighbours[v]):
                continue
            colours[v] = c
            viable = all(any(all(colours[w] != d for w in neighbours[z])
                             for d in range(4)) for z in order[depth + 1:])
            if viable:
                visit(depth + 1)
            colours[v] = -1

    visit(0)
    return answers


def witness(vertices, edges, beta, lift):
    assert lift is not None and len(vertices) == len(lift)
    f = dict(zip(vertices, lift))
    assert all(f[i] == beta[i] for i in range(5))
    assert all(f[u] != f[v] for u, v in edges)
    return f


def review():
    before_s, before_j = snapshot(S), snapshot(J)
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    inputs, delivery, cert = [load(S / p) for p in
                              ["inputs.json", "delivery.json", "certificate.json"]]
    source = Path(inputs["source_checkout"])
    assert git("-C", str(source), "rev-parse", "HEAD").decode().strip() == BASE
    assert not git("-C", str(source), "status", "--porcelain")
    for item in inputs["base_files"]:
        data = git("show", BASE + ":" + item["path"])
        assert sha(data) == item["sha256"]
        assert data == (source / item["path"]).read_bytes()
    manifest = {i["path"]: i for i in delivery["files"]}
    assert set(manifest) == set(before_s) - {"delivery.json"}
    for name, entry in manifest.items():
        assert before_s[name]["sha256"] == entry["sha256"]
        assert before_s[name]["bytes"] == entry["bytes"]
    assert sha((S / "task.md").read_bytes()) == inputs["task_instruction"]["sha256"]
    assert sha((S / "gallai.pdf").read_bytes()) == inputs["external_source"]["sha256"]
    for line in (J / "MANIFEST.sha256").read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        assert sha((J / name.strip()).read_bytes()) == digest

    # Reconstruct the stabilizer orbits by applying actual permutations.
    valid, low = 0, 0
    for row in cert["singleton_orbit_table"]:
        c = row["c"]
        representatives = [(c, next(x for x in COL if x != c)),
                           (next(x for x in COL if x != c), c),
                           tuple(sorted(COL - {c})[:2])]
        orbits = [set() for _ in representatives]
        other = sorted(COL - {c})
        for perm in itertools.permutations(other):
            mapping = {c: c, **dict(zip(other, perm))}
            for orbit, (a, b) in zip(orbits, representatives):
                orbit.add((mapping[a], mapping[b]))
        forbidden = set().union(*(orbits[i] for i in range(3)
                                  if row["orbit_mask"] & (1 << i)))
        assert forbidden == set(map(tuple, row["forbidden_pairs"]))
        columns = [sum(b == x for a, b in forbidden) for x in range(4)]
        rows = [sum(a == x for a, b in forbidden) for x in range(4)]
        assert columns == row["column_sizes"] and rows == row["row_sizes"]
        holds = max(columns) <= row["k_r"] and max(rows) <= row["k_s"]
        assert holds == (row["status"] == "triggered and holds")
        valid += holds
        if holds and row["k_r"] + row["k_s"] <= 3:
            assert not forbidden
            low += 1
    assert len(cert["singleton_orbit_table"]) == 288 and valid == 92

    abstract_columns = 0
    for model in cert["abstract_capacity_controls"]:
        assert model["source_graph"] is None and model["full_lifts"] is None
        er, es = set(model["E_r_X"]), set(model["E_s"])
        factors = list(map(set, model["side_factors_X"]))
        side_s = list(map(set, model["side_factors_s"]))
        assert er == COL - set().union(*factors)
        assert es == COL - set().union(*side_s)
        assert sum(map(len, factors)) == len(COL - er)
        assert sum(model["k_r"]) + sum(map(len, factors)) == 4
        assert sum(model["k_s"]) + sum(map(len, side_s)) == 5
        relations = [set(map(tuple, model[k])) for k in ["A_P", "A_Q"]]
        banned = [PAIRS - relation for relation in relations]
        for relation, kr, ks in zip(banned, model["k_r"], model["k_s"]):
            assert all(sum(y == b for a, y in relation) <= kr for b in COL)
            assert all(sum(x == a for x, b in relation) <= ks for a in COL)
        assert not any((a, b) in relations[0] & relations[1] for a in er for b in es)
        assert len(model["columns"]) == len(es)
        for column in model["columns"]:
            b = column["b"]
            gp, gq = [{a for a in COL if (a, b) in f} for f in banned]
            assert [len(gp), len(gq)] == model["k_r"]
            assert not gp & gq and gp | gq == er
            assert sorted(gp) == column["G_P"] and sorted(gq) == column["G_Q"]
            c = model["spoke_colour"]
            original_factors = factors + [{c}]
            overlap = sum(map(len, original_factors)) - len(set().union(*original_factors))
            waste = len((gp | gq) - (er - {c}))
            assert overlap == column["original_O"] and waste == column["original_lambda"]
            assert overlap + waste == 1 and column["derivative_slacks"] == [0] * 5
            abstract_columns += 1
    assert len(cert["both_short_incidence_counts"]) == 12
    for row in cert["both_short_incidence_counts"]:
        assert row["E_r_X_size"] == row["m_r"]
        assert row["E_s_size_lower_bound"] == row["m_s"] - 1
        assert row["both_short_necessary_count_pass"] == (row["m_r"] + row["m_s"] <= 5)
    singleton_indices = {0: 6, 1: 4, 2: 3, 3: 1, 4: 0}
    for row in cert["cross_row_masks"]:
        qg = {p for p, i in singleton_indices.items() if not row["sigma_G"] & (1 << i)}
        allowed = {frozenset(), *(frozenset({p}) for p in qg),
                   *(frozenset({p, (p + 1) % 5}) for p in qg if (p + 1) % 5 in qg)}
        assert allowed == set(map(frozenset, row["E2_permitted_Q_X"]))

    # Independent full-edge enumeration and cross-check with already accepted J.
    jcert = load(J / "results/certificate.json")
    jgraphs = {g["id"]: g for g in jcert["N2"]}
    original_queries, deletion_queries, pin_cells, lifts = 0, 0, 0, 0
    for graph in cert["fixed_graph_inventory"]:
        saved = load(source / graph["path"])
        j = jgraphs[graph["id"]]
        assert graph["edges"] == j["graph"]["edges"]
        assert graph["vertices"] == j["graph"]["vertices"]
        assert graph["roots"] == j["graph"]["roots"]
        assert graph["rotation"] == j["graph"]["rotation"] == saved["rotation"]
        assert sha(git("show", BASE + ":" + graph["path"])) == graph["input_sha256"]
        for piece in graph["original_pieces"]:
            jp = next(p for p in j["pieces"] if p["vertices"] == piece["vertices"])
            assert all(piece[k] == jp[k] for k in ["contacts", "owners", "support"])
        assert graph["sigma"] == j["original"]["sigma"] and graph["sigma"] not in [933, 941]
        for index, beta in enumerate(jcert["canonical_patterns"]):
            pairs = full_root_pairs(graph["vertices"], graph["edges"], beta, graph["roots"])
            assert pairs == set(map(tuple, j["original"]["rows"][index]["root_pairs"]))
            lift = graph["row_full_lifts"][index]
            assert bool(pairs) == (lift is not None) == bool(graph["sigma"] & (1 << index))
            if lift is not None:
                f = witness(graph["vertices"], graph["edges"], beta, lift)
                assert tuple(f[r] for r in graph["roots"]) in pairs
                lifts += 1
            original_queries += 1
            pin_cells += 16
        for query in graph["spoke_queries"]:
            derivative = next(d for d in j["unit_derivatives"] if
                              d["derivative"] == {"kind": "spoke", "edge": query["edge"], "root": query["root"]})
            reduced = [e for e in graph["edges"] if e != query["edge"]]
            assert reduced == derivative["edges"]
            assert not graph["sigma"] & (1 << query["index"])
            pairs = full_root_pairs(graph["vertices"], reduced, query["beta"], graph["roots"])
            assert pairs == set(map(tuple, derivative["rows"][query["index"]]["root_pairs"]))
            f = witness(graph["vertices"], reduced, query["beta"], query["full_lift"])
            assert tuple(f[r] for r in graph["roots"]) in pairs
            boundary = next(v for v in query["edge"] if v < 5)
            assert f[query["root"]] == query["beta"][boundary]
            assert pairs and query["status"] == "not triggered"
            assert derivative["sigma"] == 1023
            deletion_queries += 1
            pin_cells += 16
            lifts += 1
    assert (original_queries, deletion_queries, pin_cells, lifts) == (190, 47, 3792, 218)
    assert before_s == snapshot(S) and before_j == snapshot(J)
    return {"base": BASE, "S_delivery_files_including_manifest": len(before_s),
            "S_hashed_manifest_entries": len(manifest), "BASE_inputs": len(inputs["base_files"]),
            "S_fingerprint": before_s, "S_byte_or_mtime_drift": [], "J_byte_or_mtime_drift": [],
            "singleton_rows": 288, "singleton_contact_bound_triggered": valid,
            "singleton_low_incidence_valid": low, "abstract_capacity_columns": abstract_columns,
            "scalar_incidence_rows": 12, "cross_row_mask_cases": 2,
            "full_graph_rows": original_queries, "spoke_rejected_row_queries": deletion_queries,
            "complete_root_pair_cells": pin_cells, "validated_S_full_lifts": lifts,
            "S_source_triggered": 0, "paper_proof_checked_by_program": False,
            "S_report_sha256": sha((S / "REPORT.md").read_bytes()),
            "S_certificate_sha256": sha((S / "certificate.json").read_bytes()),
            "J_certificate_sha256": sha((J / "results/certificate.json").read_bytes())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = review()
    with args.output.open("x") as out:
        json.dump(result, out, ensure_ascii=False, sort_keys=True, indent=2)
        out.write("\n")
    print(json.dumps({k: v for k, v in result.items() if k != "S_fingerprint"}, ensure_ascii=False))
