#!/usr/bin/env python3
"""Regenerate W5 three-colour-support controls, including every empty fibre.

Stdlib only. --write creates exclusive local outputs; --check regenerates all
fields. --seed changes DFS traversal, not the canonical result. The frozen
predecessor supplies the declared 34 graph constructors, planar-map checks,
graph DFS and quotient controls. A separate reviewer imports none of this code.
"""
import argparse
import gzip
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FROZEN_REL = "frozen/audits/2026-10-12-w5-marked-relation-e299ae98/controls/check_w5.py"
FROZEN = ROOT / FROZEN_REL
spec = importlib.util.spec_from_file_location("frozen_w5_controls", FROZEN)
old = importlib.util.module_from_spec(spec)
previous_bytecode_setting = sys.dont_write_bytecode
sys.dont_write_bytecode = True
spec.loader.exec_module(old)
sys.dont_write_bytecode = previous_bytecode_setting


def checked(test, message):
    if not test:
        raise ValueError(message)


def tau_index(tau):
    return sum(c * 4 ** (4 - i) for i, c in enumerate(tau))


def g_from_h(graph, lift, center):
    colors = dict(zip(graph["h_vertices"], lift))
    colors[old.V] = center
    return tuple(colors[x] for x in graph["g_vertices"])


def g_tau(graph, lift):
    colors = dict(zip(graph["g_vertices"], lift))
    return tuple(colors[x] for x in old.U)


def valid_lift(graph, kind, lift):
    vertices, edges = graph[f"{kind}_vertices"], graph[f"{kind}_edges"]
    colors = dict(zip(vertices, lift))
    return (len(lift) == len(vertices) and set(lift) <= set(old.C)
            and all(colors[a] != colors[b] for a, b in edges))


def add_support(graph):
    hv, he = set(graph["h_vertices"]), set(map(tuple, graph["h_edges"]))
    checked(set(old.B + old.U) <= hv and old.V not in hv, "missing named boundary or deleted center")
    rim = {old.edge(old.U[i], old.U[(i + 1) % 5]) for i in old.B}
    checked({e for e in he if set(e) <= set(old.U)} == rim, "U is not the induced C5")
    checked(set(graph["g_vertices"]) == hv | {old.V}, "G has incorrect vertex restoration")
    checked(set(map(tuple, graph["g_edges"])) == he | {old.edge(old.V, u) for u in old.U},
            "G is not exactly H capped at the named U")
    r3, support = [], []
    for bi, row in enumerate(graph["rows"]):
        indices = []
        for ti, cell in enumerate(row["cells"]):
            if cell:
                support.append([bi, ti])
                if len(set(old.TAUS[ti])) == 3:
                    r3.append([bi, ti])
                    indices.append(ti)
        row["r3_tau_indices"] = indices
        checked(bool(indices) == bool(row["g_lifts"]), "R3 projection differs from direct G DFS")
    graph["r3_support"] = r3
    graph["full_support"] = support


def color_transports(graphs):
    """Every proper literal beta has a unique S4 transporter of its RGS row."""
    records = []
    for literal in old.TAUS:
        if not old.cycle_proper(literal):
            continue
        beta = old.normalized(literal)
        bi = old.BETAS.index(beta)
        matches = [p for p in itertools.permutations(old.C)
                   if tuple(p[c] for c in beta) == literal]
        checked(len(matches) == 1, "outer beta transporter is not unique")
        records.append({"literal_beta": literal, "beta_index": bi,
                        "canonical_to_literal": matches[0]})
    checked(len(records) == 240, "wrong literal outer row domain")
    h_instances = g_instances = 0
    for graph in graphs:
        for transport in records:
            bi, perm = transport["beta_index"], transport["canonical_to_literal"]
            row = graph["rows"][bi]
            for cell in row["cells"]:
                for lift in cell:
                    mapped = tuple(perm[c] for c in lift)
                    checked(valid_lift(graph, "h", mapped), "global transport breaks H")
                    checked(tuple(dict(zip(graph["h_vertices"], mapped))[b] for b in old.B)
                            == transport["literal_beta"], "wrong transported B")
                    h_instances += 1
            for lift in row["g_lifts"]:
                mapped = tuple(perm[c] for c in lift)
                checked(valid_lift(graph, "g", mapped), "global transport breaks G")
                checked(set(g_tau(graph, mapped)) == set(old.C) - {
                    dict(zip(graph["g_vertices"], mapped))[old.V]}, "transport breaks missing colour")
                g_instances += 1
    return {"literal_beta_count": 240, "canonical_beta_count": 10,
            "records": records, "global_h_lift_instances": h_instances,
            "global_g_lift_instances": g_instances, "score": "triggered and holds",
            "rule": "Apply the unique common S4 permutation to B, U, center and every private vertex; never normalize U independently."}


def selector(source, target):
    rows = []
    count = 0
    for bi, row in enumerate(source["rows"]):
        transfers = []
        for source_g in row["g_lifts"]:
            source_map = dict(zip(source["g_vertices"], source_g))
            tau = tuple(source_map[x] for x in old.U)
            ti = tau_index(tau)
            cell = target["rows"][bi]["cells"][ti]
            checked(cell and len(set(tau)) == 3, "selector has no three-colour target fibre")
            target_h = min(cell)
            target_g = g_from_h(target, target_h, source_map[old.V])
            target_map = dict(zip(target["g_vertices"], target_g))
            checked(target_g in target["rows"][bi]["g_lifts"], "selector target not in direct G enumeration")
            checked(all(source_map[x] == target_map[x] for x in old.B + old.U + (old.V,)),
                    "selector changed a named boundary or center colour")
            checked(valid_lift(target, "g", target_g), "selector violates target graph edge")
            transfers.append({"source_g_lift": source_g, "tau_index": ti,
                              "target_h_lift": target_h, "target_g_lift": target_g})
            count += 1
        rows.append({"beta_index": bi, "transfers": transfers})
    return {"source_graph": source["id"], "target_graph": target["id"],
            "rows": rows, "score": "triggered and holds"}, count


def pair_controls(graphs):
    pairs, selectors = [], []
    equal_count = transfer_count = 0
    for a, b in itertools.combinations(graphs, 2):
        same_r3 = a["r3_support"] == b["r3_support"]
        same_sigma = a["sigma_g"] == b["sigma_g"]
        checked(not same_r3 or same_sigma, "equal R3 but unequal capped Sigma")
        pairs.append({"graphs": [a["id"], b["id"]], "equal_r3": same_r3,
                      "equal_sigma_g": same_sigma,
                      "implication_score": "triggered and holds" if same_r3 else "not triggered"})
        if same_r3:
            equal_count += 1
            for source, target in ((a, b), (b, a)):
                record, count = selector(source, target)
                selectors.append(record)
                transfer_count += count
    return {"unordered_distinct_pair_count": len(pairs), "pairs": pairs,
            "equal_r3_pair_count": equal_count, "directional_selectors": selectors,
            "selector_lift_instances": transfer_count}


def new_witnesses(graphs):
    by_id = {g["id"]: g for g in graphs}
    prism, tri, decorated = (by_id[k] for k in ("prism", "triangulated_00", "prism_decorated"))
    checked(prism["sigma_g"] == tri["sigma_g"], "strictness pair Sigma differs")
    different = sorted(set(map(tuple, prism["r3_support"])) ^ set(map(tuple, tri["r3_support"])))
    checked(different, "strictness pair has equal R3")
    bi, ti = different[0]
    present, absent = (prism, tri) if prism["rows"][bi]["cells"][ti] else (tri, prism)
    ph = present["rows"][bi]["cells"][ti][0]
    missing = next(iter(set(old.C) - set(old.TAUS[ti])))
    sigma_not_r3 = {
        "graphs": [prism["id"], tri["id"]], "sigma_g": prism["sigma_g"],
        "r3_support_sizes": [len(prism["r3_support"]), len(tri["r3_support"])],
        "distinguishing": {"beta_index": bi, "tau_index": ti,
                           "beta": old.BETAS[bi], "tau": old.TAUS[ti],
                           "present_graph": present["id"], "present_h_lift": ph,
                           "present_g_lift": g_from_h(present, ph, missing),
                           "absent_graph": absent["id"], "absent_full_cell": []},
        "candidate": "Equal capped outer Sigma implies equal named three-colour support",
        "score": "counterexample"}
    r3 = set(map(tuple, prism["r3_support"]))
    beta_projection, tau_projection = sorted({b for b, t in r3}), sorted({t for b, t in r3})
    bi, ti = next((b, t) for b in beta_projection for t in tau_projection if (b, t) not in r3)
    other_ti = min(t for b, t in r3 if b == bi)
    other_bi = min(b for b, t in r3 if t == ti)
    def actual_cell(b, t):
        lift = prism["rows"][b]["cells"][t][0]
        missing = next(iter(set(old.C) - set(old.TAUS[t])))
        return {"beta_index": b, "tau_index": t, "h_lift": lift,
                "g_lift": g_from_h(prism, lift, missing)}
    marginal = {"graph": prism["id"], "fake_beta_index": bi, "fake_tau_index": ti,
                "fake_beta": old.BETAS[bi], "fake_tau": old.TAUS[ti],
                "actual_beta_witness": actual_cell(bi, other_ti),
                "actual_tau_witness": actual_cell(other_bi, ti), "fake_full_cell": [],
                "candidate": "Independent B and U projections reconstruct the joint three-colour support",
                "score": "counterexample"}
    checked(not prism["rows"][bi]["cells"][ti], "marginal false cell is nonempty")
    checked(prism["r3_support"] == decorated["r3_support"], "decoration changed R3")
    checked(prism["full_support"] == decorated["full_support"], "decoration changed full support")
    for arow, brow in zip(prism["rows"], decorated["rows"]):
        for acell, bcell in zip(arow["cells"], brow["cells"]):
            checked(len(bcell) == 2 * len(acell), "decoration fibre multiplicity is not two")
            checked(sorted(tuple(dict(zip(decorated["h_vertices"], e))[x]
                                 for x in prism["h_vertices"]) for e in bcell)
                    == sorted(e for e in acell for _ in range(2)), "decoration lift forgetting fails")
    bi, ti = prism["r3_support"][0]
    def cell_g(graph):
        return [e for e in graph["rows"][bi]["g_lifts"] if tau_index(g_tau(graph, e)) == ti]
    support_not_lifts = {
        "graphs": [prism["id"], decorated["id"]], "r3_equal": True,
        "full_support_equal": True, "all_nonempty_cell_multiplicity_ratio": 2,
        "witness": {"beta_index": bi, "tau_index": ti, "beta": old.BETAS[bi], "tau": old.TAUS[ti],
                    "base_h_lifts": prism["rows"][bi]["cells"][ti],
                    "decorated_h_lifts": decorated["rows"][bi]["cells"][ti],
                    "base_g_lifts_at_cell": cell_g(prism),
                    "decorated_g_lifts_at_cell": cell_g(decorated)},
        "candidate": "Equal three-colour support preserves complete lift fibres or their multiplicities",
        "score": "counterexample"}
    equal_pairs = [(a, b) for a, b in itertools.combinations(graphs, 2)
                   if a["r3_support"] == b["r3_support"]]
    unequal_full = [(a["id"], b["id"]) for a, b in equal_pairs if a["full_support"] != b["full_support"]]
    return {"sigma_not_r3": sigma_not_r3, "beta_tau_marginal_mix": marginal,
            "support_not_full_lifts": support_not_lifts,
            "r3_vs_full_support": {
                "score": "triggered and holds" if unequal_full else "not triggered",
                "equal_r3_pair_count": len(equal_pairs),
                "unequal_full_support_pairs": unequal_full,
                "candidate": "Existence in the original 34 controls of equal R3 but unequal all-colour support",
                "scope": "Absence of this witness in these 34 controls is not an equivalence claim."}}


def build(seed):
    old.DFS_SEED = seed
    certificate, inherited_summary = old.build()
    certificate["schema"] = "w5-three-color-support-v1"
    certificate["provenance"] = "Exactly the frozen predecessor's 34 literal disk controls, regenerated by graph DFS; no source-minimality claim."
    certificate["source_reuse"] = {
        "frozen_checker": FROZEN_REL,
        "frozen_checker_sha256": hashlib.sha256(FROZEN.read_bytes()).hexdigest(),
        "reused": ["34 graph constructors", "directed-face geometry validation", "full H/G and quotient DFS", "old signed/chord/negative controls"]}
    certificate["common_slot"] = {
        "B": old.B, "U": old.U, "center": old.V,
        "outer_boundary_face": tuple(reversed(old.B)), "inner_boundary_face": old.U,
        "rule": "Delete the distinguished B and U face interiors from H to obtain the common ordered annulus slot; cap U with the five named center triangles."}
    for graph in certificate["graphs"]:
        add_support(graph)
    certificate["support_semantics"] = "r3_support lists exactly [beta_index,tau_index] with nonempty complete H fibre and exactly three literal U colours; indices refer to the global domains. full_support omits only the three-colour predicate."
    certificate["color_frame_transports"] = color_transports(certificate["graphs"])
    certificate["pair_controls"] = pair_controls(certificate["graphs"])
    certificate["witnesses"].update(new_witnesses(certificate["graphs"]))
    for key, witness in certificate["witnesses"].items():
        if key == "nontrivial_full_fibre":
            witness["score"] = "triggered and holds"
        witness["graph_record_reference"] = "All named graph edges, faces, rotations and vertex-vector orders are in graphs[] matched by id."
    r3_cells = sum(len(g["r3_support"]) for g in certificate["graphs"])
    pair = certificate["pair_controls"]
    summary = {key: inherited_summary[key] for key in (
        "graph_count", "beta_count", "tau_count", "explicit_cell_count", "empty_cell_count",
        "nonempty_cell_count", "complete_h_lift_count", "complete_g_lift_count",
        "literal_quotient_count", "complete_quotient_lift_count", "center_reconstruction",
        "pointwise_signed_identity", "direct_quotient_pullback", "source_minimality")}
    summary.update({
        "schema": certificate["schema"], "r3_nonempty_cell_count": r3_cells,
        "geometry_checked_graph_maps": len(certificate["graphs"]) * 2,
        "projection_formula": {"score": "triggered and holds", "row_instances": 340},
        "unordered_distinct_pair_count": pair["unordered_distinct_pair_count"],
        "equal_r3_pair_count": pair["equal_r3_pair_count"],
        "nontriggered_pair_count": pair["unordered_distinct_pair_count"] - pair["equal_r3_pair_count"],
        "equal_r3_pair_ids": [p["graphs"] for p in pair["pairs"] if p["equal_r3"]],
        "directional_selector_count": len(pair["directional_selectors"]),
        "selector_lift_instances": pair["selector_lift_instances"],
        "global_h_lift_transport_instances": certificate["color_frame_transports"]["global_h_lift_instances"],
        "global_g_lift_transport_instances": certificate["color_frame_transports"]["global_g_lift_instances"],
        "witnesses": certificate["witnesses"],
        "limits": ["Finite calibration on the fixed original 34 controls only", "No general annulus small representative constructed", "No main proposition closure or source-minimality conclusion", "No Lean verification", "Bidirectional selectors need not be inverses and do not preserve full lift multiplicities", "Separate single-pair quotient embeddings do not authorize a simultaneous quotient"]})
    return certificate, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    certificate_path = args.certificate or HERE / "certificate.json.gz"
    summary_path = HERE / "summary.json"
    checked(not args.write or args.certificate is None, "--write uses exclusive local output paths only")
    if args.write:
        checked(not certificate_path.exists() and not summary_path.exists(), "refusing to overwrite existing certificate or summary")
    certificate, summary = build(args.seed)
    payload = old.canonical_bytes(certificate)
    summary["canonical_certificate_sha256"] = hashlib.sha256(payload).hexdigest()
    if args.write:
        with certificate_path.open("xb") as stream:
            stream.write(gzip.compress(payload, compresslevel=9, mtime=0))
        with summary_path.open("x") as stream:
            json.dump(summary, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
    else:
        with gzip.open(certificate_path, "rb") as stream:
            actual = json.load(stream)
        difference = old.first_difference(json.loads(payload), actual)
        checked(difference is None, f"certificate mismatch: {difference}")
        if args.certificate is None:
            with summary_path.open() as stream:
                actual_summary = json.load(stream)
            checked(json.loads(old.canonical_bytes(summary)) == actual_summary, "summary differs from regenerated result")
    print(json.dumps({"result": "PASS", "mode": "write" if args.write else "check", "dfs_seed": args.seed,
                      **{key: summary[key] for key in (
                          "graph_count", "explicit_cell_count", "empty_cell_count", "complete_h_lift_count",
                          "complete_g_lift_count", "r3_nonempty_cell_count", "unordered_distinct_pair_count",
                          "equal_r3_pair_count", "selector_lift_instances", "canonical_certificate_sha256")}}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"FAIL: {error}")
