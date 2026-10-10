#!/usr/bin/env python3
"""N45-PC fixed-domain certificate replay and read-only proposal CLI.

--generate exclusive-creates certificate.json before computing. --check never
writes. --source only reads input files and prints JSON; exit 2 means the full
LP source contract does not hold (including missing scope premises).
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys

import validator as v

HOME = Path(__file__).resolve().parent
ROOT = HOME.parent.parent
BASE = "dc8e9aa7d6fccb51f63d30aa3f9c132296d44744"
N2_IDS = ["NA7-0002", "NA8-0014", "NA8-0015", "NA8-0016", "NA8-0017", "NA8-0018",
          "NA8-0020", "NA8-0021", "NA8-0022", "NA9-0010", "NA9-0011", "NA9-0020",
          "NA9-0021", "NA9-0022", "NA9-0023", "NA9-0024", "NA9-0025", "NA9-0026", "NA9-0027"]
N1_IDS = ["NA8-0003", "NA8-0007", "NA8-0009", "NA8-0010"]


def read(path):
    return json.loads(Path(path).read_text())


def verify_inputs():
    m = read(HOME / "inputs.json")
    actual = subprocess.check_output(["git", "-C", str(HOME / "source"), "rev-parse", "HEAD"], text=True).strip()
    v.need(actual == BASE, "independent source checkout HEAD drift")
    v.need(subprocess.check_output(["git", "-C", str(HOME / "source"), "status", "--porcelain"], text=True) == "", "independent BASE checkout is dirty")
    for item in m["authority_files"]:
        blob = subprocess.check_output(["git", "-C", str(ROOT), "show", BASE + ":" + item["path"]])
        p = HOME / "source" / item["path"]
        v.need(p.read_bytes() == blob and v.digest(p) == item["sha256"], "BASE input drift: " + item["path"])
    for item in m["frozen_deliveries"]:
        v.need(v.digest(HOME / "frozen" / item["path"]) == item["sha256"], "frozen delivery input drift: " + item["path"])
    return m


def compare_saved(g, raw, suj):
    old = next(x for x in suj["graphs"] if x["id"] == g["id"])
    v.need(g["sigma"] == old["sigma"] and g["vertices"] == old["vertices"] and g["edges"] == old["edges"], "SU-J original source graph mismatch")
    v.need(g["rotation"] == old["rotation"] and g["H_bridges"] == old["H_bridges"], "SU-J original topology mismatch")
    for p in g["pieces"]:
        sp = next(x for x in old["pieces"] if x["id"] == p["id"])
        for key in ("vertices", "contacts", "owners", "contact_order", "shared_contacts", "support", "attachments", "internal_edges", "incidences", "kind", "one_sided", "original_internal_bridges"):
            v.need(p[key] == sp[key], "SU-J complete original interface drift: " + key)
        if "shield" in p:
            v.need(p["shield"] == sp["shield"], "SU-J original shield drift")
        for row, sr in zip(p["rows"], sp["rows"]):
            expected = [{"tuple": t["tuple"], "lifts": t["full_piece_lifts"]} for t in sr["tuples"]]
            v.need(row["tuples"] == expected and row["fibres"] == sr["fibres"] and row["F"] == sr["F"], "SU-J complete tuples/lifts/fibres drift")
    for row, saved in zip(g["rows"], old["joins"]):
        v.need(row["root_pairs"] == saved["root_pairs"], "SU-J complete original root pairs drift")
        for cell, sc in zip(row["all_16_fibres"], saved["all_16_fibres"]):
            v.need(cell["pins"] == sc["pins"] and cell["tuple_indices"] == sc["tuple_indices"], "SU-J complete selected fibres drift")
            v.need(len(cell["full_lifts"]) == sc["full_lift_count"], "SU-J full-lift count drift")
            if sc["full_graph_lift"] is not None:
                v.need(sc["full_graph_lift"] in cell["full_lifts"], "SU-J saved full lift not in original-edge oracle")
    # Original certificate witnesses are checked against actual edges, not chosen-solution equality.
    for deletion in raw["deletions"]:
        e = tuple(deletion["edge"])
        es = [tuple(f) for f in g["edges"] if tuple(f) != e]
        v.need(e in list(map(tuple, g["edges"])) and e not in v.frame_edges(g["frame"]), "saved criticality deletion is not an original nonframe edge")
        gained = next(w for w in g["critical_witnesses"] if w["edge"] == list(e))["gained_rows"]
        v.need([w["index"] for w in gained] == deletion["gained"] and gained, "saved gained-row criticality inventory drift")
        for i in deletion["gained"]:
            v.legal(g["vertices"], es, dict(zip(g["frame"], v.PATTERNS[i])), deletion["witnesses"][str(i)])


def check_negative(item):
    qpath = HOME / item["proposal"]
    q = read(qpath)
    raw = read(qpath.parent / q["graph_file"])
    # Independent evidence retained before the deliberate mutation.
    oracle = item["oracle"]
    frame = q.get("frame", list(range(5)))
    pins = dict(zip(frame, oracle["literal_beta"]))
    if "piece" in oracle:
        original = next(p for p in raw["pieces"] if p["id"] == oracle["piece"])
        pv = original["vertices"]
        local_vs = v.sv(set(frame) | set(pv))
        local_es = [tuple(e) for e in raw["edges"] if set(e) <= set(local_vs)]
        f = pins | dict(zip(pv, oracle["original_legal_piece_lift"]))
        # Verify the retained oracle on original edges directly, before reading the changed tuples.
        v.need(all(f[u] != f[w] for u, w in local_es), "negative oracle is not an original legal piece lift")
        v.need([f[x] for x in original["contact_order"]] == oracle["original_contact_tuple"], "negative tuple oracle has wrong named coordinates")
        v.need(any(t["tuple"] == oracle["original_contact_tuple"] and oracle["original_legal_piece_lift"] in t["lifts"]
                   for t in original["rows"][oracle["index"]]["tuples"]), "negative oracle lacks original saved-lift provenance")
        for contact in oracle.get("original_root_contact_edges", []):
            v.need(contact in raw["edges"], "negative shared-contact oracle is not an original edge")
        if "shared_original_vertex" in oracle:
            x = oracle["shared_original_vertex"]
            v.need(all(x in original["contacts"][str(r)] for r in q["roots"]), "negative oracle shared vertex is not owned by both original roots")
    if "original_edge" in oracle:
        v.need(oracle["original_edge"] in raw["edges"], "negative original-edge oracle is not an actual source edge")
    if "legal_whole_lift" in oracle:
        v.legal(v.sv(raw["vertices"]), list(map(tuple, raw["edges"])), pins, oracle["legal_whole_lift"])
    try:
        v.validate_proposal(qpath)
    except (v.DataError, KeyError, TypeError, ValueError) as exc:
        v.need(item["expected_error"] in str(exc), "negative rejected for an unrelated reason: " + str(exc))
        return {"id": item["id"], "proposal_sha256": v.digest(qpath), "status": "triggered and holds",
                "rejection": str(exc), "oracle": oracle,
                "scope": "Malformed declaration rejection; never a mathematical source counterexample."}
    raise v.DataError("negative input was not rejected: " + item["id"])


def audit():
    manifest = verify_inputs()
    suj = read(HOME / "frozen/audits/2026-10-09-n45-su-j/certificate.json")
    J = read(HOME / "frozen/audits/2026-10-09-n45-j/results/inventory.json")
    v.need(N2_IDS == J["N2_selected"], "fixed N2 domain differs from frozen J")
    proposal_index = read(HOME / "controls-v2/index.json")
    v.need(len(proposal_index) == 11 and len({x["proposal"] for x in proposal_index}) == 11, "fixed control proposal index incomplete/duplicated")
    results, counts, profiles = [], Counter(), []
    for family, ids in (("N2", N2_IDS), ("N1 calibration only", N1_IDS)):
        for name in ids:
            path = HOME / "source/artifacts/c5_excess_two_e4c/controls" / (name + ".json")
            raw = read(path)
            seed = HOME / "source" / raw["source"]
            v.need(v.digest(seed) == raw["source_sha256"], "raw fixed-control source hash drift")
            original = read(seed)
            v.need(original["canonical_edges"] == raw["edges"], "fixed graph original source edges differ")
            g = v.compute_graph(raw)
            compare_saved(g, raw, suj)
            geometry = v.lp_geometry(g)
            if family == "N2":
                v.need(sum(p["kind"] == "mixed" for p in g["pieces"]) == 2, "N2 membership from original components drift")
                counts["N2_graphs"] += 1
                counts["N2_LP_geometry_triggered"] += geometry["status"] == "triggered and holds"
                counts["N2_target_sigma_triggered"] += any(t["sigma"] == g["sigma"] for t in v.d5_targets())
                profiles.append({"id": name, "sigma": g["sigma"], "full_B_touch": g["layers"]["full_B_touch_H_connected"]["status"],
                                 "geometry": geometry, "pieces": [{k: p[k] for k in ("id", "kind", "incidences", "support", "shield")} for p in g["pieces"]]})
            else:
                v.need(sum(p["kind"] == "mixed" for p in g["pieces"]) == 1, "N1 calibration accidentally entered N2")
                counts["N1_calibration_graphs"] += 1
            omissions = []
            for p in g["pieces"]:
                counts["piece_rows"] += 10
                counts["piece_full_lifts"] += sum(len(t["lifts"]) for row in p["rows"] for t in row["tuples"])
                if p["kind"] != "unary" or sum(p["incidences"]) != 1:
                    continue
                proposal = HOME / "controls-v2" / (name + "-" + p["id"] + ".json")
                validated = v.validate_proposal(proposal)
                v.need(validated["source_contract"]["status"] == "not triggered", "fixed control was silently promoted to a complete LP source")
                old_g = next(x for x in suj["graphs"] if x["id"] == name)
                old_u = next(x for x in old_g["unit_derivatives"] if x["piece"] == p["id"])
                # Check every original literal row, even when the selected beta is outside the core domain.
                us = []
                for i, beta in enumerate(v.PATTERNS):
                    u = v.omit_unit(g, p["id"], beta)
                    if i == 0:
                        v.need(u["vertices_X"] == old_u["vertices_X"] and u["edges_X"] == old_u["edges_X"] and u["sigma_X"] == old_u["sigma_X"], "SU-J exact whole U/X identity drift")
                        for row, saved in zip(u["rows_X"], old_u["joins_X"]):
                            v.need(row["root_pairs"] == saved["root_pairs"], "SU-J X complete root pairs differ")
                            for cell, sc in zip(row["all_16_fibres"], saved["all_16_fibres"]):
                                v.need(cell["tuple_indices"] == sc["tuple_indices"] and len(cell["full_lifts"]) == sc["full_lift_count"], "SU-J X full fibre drift")
                        counts["N2_whole_U_omissions" if family == "N2" else "N1_whole_U_calibrations"] += 1
                        counts["N2_Delta_gamma_instances" if family == "N2" else "N1_Delta_gamma_instances"] += len(u["new_gamma_singleton_forcing"])
                        counts["N2_X_16pin_fibres" if family == "N2" else "N1_X_16pin_fibres"] += 160
                    core = u["layers"]["rejecting_beta_minimal_45_54_core"]["status"]
                    counts["N2_rejecting_beta_minimal_occurrences" if family == "N2" else "N1_rejecting_beta_minimal_calibrations"] += core == "triggered and holds"
                    if family == "N1 calibration only" and core == "triggered and holds":
                        v.need(u["layers"]["core_zero_slack_full_partition"]["status"] == "triggered and holds", "N1 zero-slack interface calibration fails")
                    us.append({"index": i, "literal_beta": beta, "layers": u["layers"],
                               "retained_edge_beta_witnesses": u["retained_edge_beta_witnesses"], "zero_slack_columns": u["zero_slack_columns"]})
                first = v.omit_unit(g, p["id"], v.PATTERNS[0])
                first["all_ten_literal_beta_core_checks"] = us
                first["proposal_contract"] = {"proposal_sha256": validated["proposal_sha256"], "layers": validated["layers"], "source_contract": validated["source_contract"]}
                omissions.append(first)
            counts["N2_original_16pin_fibres" if family == "N2" else "N1_original_16pin_fibres"] += 160
            counts["nonframe_critical_edges"] += len(g["critical_witnesses"])
            results.append({"family": family, "source_sha256": v.digest(path), "graph": g, "LP_geometry": geometry, "whole_U_omissions": omissions})
    v.need(counts["N2_graphs"] == 19 and counts["N2_whole_U_omissions"] == 7 and counts["N1_whole_U_calibrations"] == 4, "19 N2 / 7 N2 U / 4 N1 U domain drift")
    v.need(counts["N2_LP_geometry_triggered"] == counts["N2_target_sigma_triggered"] == counts["N2_rejecting_beta_minimal_occurrences"] == 0, "supervisor zero-trigger claim contradicted by independent source reconstruction")
    negatives = [check_negative(item) for item in read(HOME / "negative-inputs-v2/index.json")]
    counts["negative_inputs_rejected"] = len(negatives)
    return {"task": "N45-PC", "BASE": BASE, "inputs_sha256": v.digest(HOME / "inputs.json"),
            "checker_sha256": v.digest(Path(__file__)), "validator_sha256": v.digest(HOME / "validator.py"),
            "controls_index_sha256": v.digest(HOME / "controls-v2/index.json"),
            "negative_index_sha256": v.digest(HOME / "negative-inputs-v2/index.json"),
            "counts": dict(sorted(counts.items())), "whole_D5_target_transports": v.d5_targets(),
            "N2_original_geometry_profiles": profiles, "fixed_sources": results, "negative_inputs": negatives,
            "coverage": {"N2_LP_source_contract": v.layer(missing=["unique unit U + long + short edge-pair geometry positive control", "Sigma 933/941 complete target positive control", "N2 rejecting beta-minimal 45/54 X positive control"]),
                         "N1": "Interface calibration only; excluded from N2/LP coverage", "paper": "not audited", "Lean": "no new theorem", "source_exclusion": "not established"},
            "no_source_exclusion_aggregate": True}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--generate", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--source", type=Path)
    args = ap.parse_args()
    if args.source:
        try:
            result = v.validate_proposal(args.source)
        except (v.DataError, KeyError, TypeError, ValueError, OSError) as exc:
            print(v.enc({"source_contract": {"status": "counterexample", "finding": str(exc),
                          "meaning": "Input declaration error, not a mathematical source counterexample."}}).decode(), end="")
            return 2
        print(v.enc(result).decode(), end="")
        return 0 if result["source_contract"]["status"] == "triggered and holds" else 2
    path = HOME / "certificate-final-v2.json"
    if args.generate:
        # Reserve before calculation. Existing or interrupted outputs are never overwritten.
        with path.open("xb") as stream:
            result = audit()
            stream.write(v.enc(result))
        print(json.dumps({"generated": str(path), "counts": result["counts"]}, ensure_ascii=False, sort_keys=True))
    else:
        result = audit()
        v.need(path.read_bytes() == v.enc(result), "certificate byte replay mismatch")
        print(json.dumps({"replay": "holds", "certificate_sha256": v.digest(path), "counts": result["counts"],
                          "LP_source_status": "not triggered", "source_exclusion": "not established"}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
