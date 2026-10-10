#!/usr/bin/env python3
"""A/U delivery and finite cross-review. No delivered checker is imported."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"
A, U, J = [ROOT / ("audits/2026-10-09-n45-" + t) for t in ["a", "u", "j"]]
spec = importlib.util.spec_from_file_location("supervisor_full_edge_enumerator",
    ROOT / "audits/2026-10-09-n45-s-supervision/review.py")
own = importlib.util.module_from_spec(spec)
spec.loader.exec_module(own)


def load(p):
    return json.loads(p.read_text())


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fingerprint(p, exclude_source=False):
    return {str(x.relative_to(p)): {"sha256": digest(x), "bytes": x.stat().st_size,
            "mtime_ns": x.stat().st_mtime_ns} for x in sorted(p.rglob("*"))
            if x.is_file() and not (exclude_source and x.relative_to(p).parts[0] == "source")}


def run(output):
    before_a, before_u = fingerprint(A), fingerprint(U, True)
    ai, ui = load(A / "inputs.json"), load(U / "inputs.json")
    afiles = {x["path"]: x for x in ai["BASE_inputs"] + load(A / "validation-inputs.json")["files"]}
    assert len(afiles) == 720
    ufiles = {x["path"]: x for x in ui["base_inputs"]}
    assert len(ufiles) == 70
    paths = sorted(set(afiles) | set(ufiles))
    batch = subprocess.check_output(["git", "cat-file", "--batch"], cwd=ROOT,
                input="".join(BASE + ":" + p + "\n" for p in paths).encode())
    offset, git_hashes = 0, {}
    for path in paths:
        end = batch.index(b"\n", offset)
        header = batch[offset:end].split()
        assert header[1] == b"blob"
        size = int(header[2]); raw = batch[end + 1:end + 1 + size]
        git_hashes[path] = hashlib.sha256(raw).hexdigest()
        offset = end + 2 + size
    assert offset == len(batch)
    for records, source in [(afiles, Path(ai["source_worktree"])), (ufiles, U / "source")]:
        assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source).decode().strip() == BASE
        assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=source)
        for path, item in records.items():
            assert git_hashes[path] == item["sha256"] == digest(source / path)
    amanifest = load(A / "MANIFEST.json")["files"]
    assert set(amanifest) == set(before_a) - {"MANIFEST.json"}
    for path, item in amanifest.items():
        assert all(before_a[path][k] == item[k] for k in ["sha256", "bytes"])
    for item in load(U / "checks.json")["payload_hashes"]:
        assert all(before_u[item["path"]][k] == item[k] for k in ["sha256", "bytes"])
    for record in load(U / "checks.json")["commands_and_logs"]:
        if record.get("log_sha256"):
            assert digest(U / record["log"]) == record["log_sha256"]
    for item in load(A / "provenance-comparison.json"):
        old, new = load(Path(item["historical_path"])), load(Path(item["fresh_path"]))
        assert {k: v for k, v in old.items() if k != "sources"} == {k: v for k, v in new.items() if k != "sources"}
        assert set(old["sources"]) == set(new["sources"])
        changed = [k for k in old["sources"] if old["sources"][k] != new["sources"][k]]
        assert changed == ["artifacts/c5_excess_two_e3/REPORT.md"]
        assert old["sources"][changed[0]]["sha256"] == "6d385639c565e2dd08eb61d7835f5fbfec29cd7c467ce8e5abba1dfc2e39e659"
        assert new["sources"][changed[0]]["sha256"] == git_hashes[changed[0]]

    a, u, j = [load(p) for p in [A / "certificate.json", U / "certificate-final.json", J / "results/certificate.json"]]
    jgraphs = {g["id"]: g for g in j["N2"] + j["N1_separate"]}
    counts = {"A_graphs": 54, "A_full_sigma_rows": 0, "A_unit_derivative_rows": 0,
              "A_critical_edge_witnesses": 0, "A_BC2_columns_vs_J": 0,
              "U_graphs": 23, "U_original_pair_cells": 0, "U_derivative_pair_cells": 0,
              "U_contact_deleted_pair_cells": 0, "U_local_relation_rows_vs_J": 0,
              "U_full_piece_lifts_vs_J": 0, "U_BC2_columns_vs_J": 0}
    for g in a["graphs"]:
        for index, beta in enumerate(j["canonical_patterns"]):
            pairs = own.full_root_pairs(g["vertices"], g["edges"], beta, g["roots"])
            assert bool(pairs) == bool(g["sigma"] & (1 << index))
            counts["A_full_sigma_rows"] += 1
        for cut in g["critical_edge_deletions"]:
            edges = [e for e in g["edges"] if e != cut["edge"]]
            for index in cut["gained"]:
                assert not g["sigma"] & (1 << index)
                own.witness(g["vertices"], edges, j["canonical_patterns"][index], cut["full_lifts"][str(index)])
            counts["A_critical_edge_witnesses"] += 1
        for d in g["unit_derivatives"]:
            for index, beta in enumerate(j["canonical_patterns"]):
                pairs = own.full_root_pairs(d["vertices"], d["edges"], beta, g["roots"])
                assert bool(pairs) == bool(d["sigma"] & (1 << index))
                counts["A_unit_derivative_rows"] += 1
        if g["m"] == 2:
            jg = jgraphs[g["id"]]
            assert g["sigma"] == jg["original"]["sigma"]
            for row in g["BC2_rejected_rows"]:
                jc = jg["original"]["rows"][row["row_index"]]["capacity"]
                for col in row["capacity_columns"]:
                    if col["status"] != "triggered and holds": continue
                    match = next(c for c in jc if c.get("r") == col["r"] and c.get("b") == col["b"])
                    assert col["terms_Du_Ou_delta_o_lambda"] == [match[k] for k in ["D_u", "O_u", "delta", "o", "lambda"]]
                    counts["A_BC2_columns_vs_J"] += 1
    for g in u["graphs"]:
        jg, roots = jgraphs[g["id"]], g["root_order"]
        assert g["vertices"] == jg["graph"]["vertices"] and g["edges"] == jg["graph"]["edges"]
        assert g["rotation"] == jg["graph"]["rotation"] and roots == jg["graph"]["roots"]
        for p in g["pieces"]:
            jp = next(x for x in jg["pieces"] if x["id"] == p["id"])
            assert all(p[k] == jp[k] for k in ["vertices", "contact_order", "contacts", "owners", "support", "attachments", "internal_edges"])
            for row in p["rows"]:
                jr = jg["relations"][row["index"]][p["id"]]
                converted = [{"tuple": t["tuple"], "lifts": t["full_piece_lifts"]} for t in row["tuples"]]
                assert converted == jr["tuples"] and row["fibres"] == jr["fibres"]
                counts["U_local_relation_rows_vs_J"] += 1
                counts["U_full_piece_lifts_vs_J"] += sum(len(t["lifts"]) for t in converted)
        for derivative, vertices, edges, rows in [(None, g["vertices"], g["edges"], g["joins"])] + [
            (d, d["vertices_X"], d["edges_X"], d["joins_X"]) for d in g["unit_derivatives"]]:
            jo = jg["original"] if derivative is None else next(x for x in jg["unit_derivatives"] if x["vertices"] == vertices and x["edges"] == edges)
            for row in rows:
                index, beta = row["index"], j["canonical_patterns"][row["index"]]
                pairs = own.full_root_pairs(vertices, edges, beta, roots)
                assert pairs == set(map(tuple, row["root_pairs"])) == set(map(tuple, jo["rows"][index]["root_pairs"]))
                counts["U_original_pair_cells" if derivative is None else "U_derivative_pair_cells"] += 16
                if derivative is not None:
                    contact = sorted(derivative["contact"])
                    cut = [e for e in g["edges"] if e != contact]
                    assert pairs == own.full_root_pairs(g["vertices"], cut, beta, roots)
                    counts["U_contact_deleted_pair_cells"] += 16
                for fibre in row["all_16_fibres"]:
                    lift = fibre["full_graph_lift"]
                    assert (lift is not None) == (tuple(fibre["pins"]) in pairs)
                    if lift is not None: own.witness(vertices, edges, beta, lift)
                    if derivative is not None and fibre["contact_edge_deleted_full_lift"] is not None:
                        own.witness(g["vertices"], cut, beta, fibre["contact_edge_deleted_full_lift"])
                for col in row["capacity"]:
                    if col["status"] != "triggered and holds":continue
                    match = next(c for c in jo["rows"][index]["capacity"] if c.get("r") == col["r"] and c.get("b") == col["b"])
                    assert col["D_O_delta_o_lambda"] == [match[k] for k in ["D_u", "O_u", "delta", "o", "lambda"]]
                    counts["U_BC2_columns_vs_J"] += 1
    assert counts["A_BC2_columns_vs_J"] == 74 and counts["A_critical_edge_witnesses"] == 1289
    assert counts["U_BC2_columns_vs_J"] == 102 and counts["U_local_relation_rows_vs_J"] == 690
    assert counts["U_full_piece_lifts_vs_J"] == 2986
    assert counts["U_original_pair_cells"] == 3680 and counts["U_derivative_pair_cells"] == counts["U_contact_deleted_pair_cells"] == 1760
    assert before_a == fingerprint(A) and before_u == fingerprint(U, True)
    result = {"BASE": BASE, "A_BASE_files_verified": 720, "U_BASE_files_verified": 70,
              "A_manifest_entries": len(amanifest), "U_authored_files_frozen": len(before_u),
              "A_fingerprint": before_a, "U_fingerprint": before_u, "original_delivery_drift": [],
              "counts": counts, "precise_target_sources_triggered": 0,
              "paper_proved_by_program": False,
              "enumerator": "supervisor fixed-order full-edge enumeration; no worker-checker imports",
              "provenance_payload_equal_except_sources": True}
    with output.open("x") as f:
        json.dump(result, f, ensure_ascii=False, sort_keys=True, indent=2);f.write("\n")
    print(json.dumps({k: v for k, v in result.items() if not k.endswith("fingerprint")}, ensure_ascii=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--output", type=Path, required=True)
    run(p.parse_args().output)
