#!/usr/bin/env python3
"""Calibrate the generic used-equal-pin bound on already saved local pieces."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
spec = importlib.util.spec_from_file_location("boundary_partition_fixed_functions", HERE / "checker.py")
fixed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixed)
require = fixed.require


def block_decomposition(vertices, edges):
    """Tarjan blocks in the fixed original C; includes literal bridge blocks."""
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    number, low, stack, blocks = {}, {}, [], []

    def visit(v, parent=None):
        number[v] = low[v] = len(number)
        for w in sorted(adjacency[v]):
            if w == parent:
                continue
            if w not in number:
                stack.append(tuple(sorted((v, w))))
                visit(w, v)
                low[v] = min(low[v], low[w])
                if low[w] >= number[v]:
                    block_edges = []
                    while True:
                        edge = stack.pop()
                        block_edges.append(edge)
                        if edge == tuple(sorted((v, w))):
                            break
                    blocks.append(sorted({x for e in block_edges for x in e}))
            elif number[w] < number[v]:
                stack.append(tuple(sorted((v, w))))
                low[v] = min(low[v], number[w])

    visit(vertices[0])
    connected = len(number) == len(vertices)
    require(not stack, "unfinished original block edge stack")
    if len(vertices) == 1:
        blocks = [list(vertices)]
    return connected, sorted(blocks)


def hypotheses(piece):
    vertices = piece["vertices"]
    vertex_set = set(vertices)
    edges = fixed.edgeset(piece["edges"])
    internal = {e for e in edges if set(e) <= vertex_set}
    connected, blocks = block_decomposition(vertices, internal)
    contacts = {v for contacts in piece["contacts"] for v in contacts}
    incidence_count = sum(map(len, piece["contacts"]))
    membership_count = Counter(v for block in blocks for v in block)
    cutpoints = {v for v, count in membership_count.items() if count > 1}
    block_records = []
    for block in blocks:
        block_set = set(block)
        block_edges = [list(e) for e in sorted(internal) if set(e) <= block_set]
        degrees = Counter(v for e in block_edges for v in e)
        if len(block) == 1:
            kind = "singleton"
        elif len(block) == 2 and len(block_edges) == 1:
            kind = "bridge"
        elif len(block) % 2 == 1 and len(block_edges) == len(block) and all(degrees[v] == 2 for v in block):
            kind = "odd_cycle"
        else:
            kind = "other"
        private = sorted(block_set - cutpoints)
        private_contacts = sorted(set(private) & contacts)
        ordinary_private = sorted(set(private) - contacts)
        leaf = len(block_set & cutpoints) <= 1
        block_records.append({"original_vertices": block, "original_edges": block_edges, "type": kind,
                              "original_cutpoints": sorted(block_set & cutpoints), "private_vertices": private,
                              "private_contacts": private_contacts, "ordinary_private_vertices": ordinary_private,
                              "leaf_block": leaf})
    attachment_pairs = [actual for _, actual in piece["attachments"]]
    predicates = {
        "connected": connected,
        "original_complete_degree_four": all(sum(v in e for e in edges) == 4 for v in vertices),
        "root_incidence_count_at_most_three": incidence_count <= 3,
        "no_shared_root_contact": incidence_count == len(contacts),
        "actual_support_at_least_three": len(piece["support"]) >= 3,
        "bridge_odd_cycle_cactus": all(b["type"] != "other" for b in block_records),
        "every_leaf_block_has_private_contact": all(b["private_contacts"] for b in block_records if b["leaf_block"]),
        "every_cycle_has_at_most_one_ordinary_private_vertex": all(len(b["ordinary_private_vertices"]) <= 1
                                                                for b in block_records if b["type"] == "odd_cycle"),
        "each_actual_boundary_attachment_at_most_two_and_adjacent": all(len(a) <= 2 and
                                      (len(a) < 2 or tuple(sorted(a)) in fixed.BEDGES) for a in attachment_pairs),
    }
    return {"predicates": predicates, "local_hypotheses_triggered": all(predicates.values()),
            "root_incidence_count": incidence_count, "distinct_contact_vertices": sorted(contacts),
            "active_original_root_owners": [root for root, contacts in zip(piece["roots"], piece["contacts"]) if contacts],
            "ordered_root_contacts": piece["contacts"], "original_cutpoints": sorted(cutpoints),
            "blocks": block_records}


def equal_pin_rows(piece, shape, counts):
    rows = []
    edges = fixed.edgeset(piece["edges"])
    for row_index, row in enumerate(piece["rows"]):
        beta = row["beta"]
        colours = sorted(set(beta))
        equal_cells = [row["fibres"][5 * colour] for colour in range(4)]
        for colour, saved in enumerate(equal_cells):
            actual = fixed.assignments(piece["vertices"], edges,
                    {**dict(enumerate(beta)), **{root: colour for root in piece["roots"]}})
            require(actual == saved, "saved complete equal-pin fibre mismatch")
            counts["independent_complete_equal_pin_cells"] += 1
            counts["complete_equal_pin_tuples"] += len(actual)
        forbidden = [c for c, cell in enumerate(equal_cells) if not cell]
        used_forbidden = sorted(set(forbidden) & set(colours))
        applies = shape["local_hypotheses_triggered"] and len(colours) == 3
        if applies:
            require(len(used_forbidden) <= 1, "generic used-equal-pin bound failed")
            counts["generic_theorem_triggered_and_holds_rows"] += 1
            counts[f"triggered_used_forbidden_size_{len(used_forbidden)}"] += 1
        else:
            counts["generic_theorem_not_triggered_rows"] += 1
        counts["proper_three_colour_saved_rows" if len(colours) == 3 else "proper_four_colour_saved_rows"] += 1
        rows.append({"row_index": row_index, "literal_beta": beta, "used_global_boundary_colours": colours,
                     "forbidden_equal_pins": forbidden, "forbidden_used_colours": used_forbidden,
                     "complete_equal_pin_relation_sizes": list(map(len, equal_cells)),
                     "complete_equal_pin_relation_sha256": list(map(fixed.digest, equal_cells)),
                     "three_colour_row": len(colours) == 3,
                     "generic_theorem_status": "triggered and holds" if applies else "not triggered"})
    return rows


def rejected_stronger_claim(datasets, counts):
    probe_path = AUDIT / "review" / "equal_pin_full_probe.json"
    if not probe_path.exists():
        return {"status": "not available", "scope": "Optional already completed frozen-800 probe reference"}
    raw = probe_path.read_bytes()
    probe = json.loads(raw)
    require(len(probe["controls"]) == probe["counts"]["controls"] == 800, "fixed-800 probe coverage mismatch")
    negatives = [c for c in probe["controls"] if all(c["forbidden_equal_pins"].values())]
    require(len(negatives) == probe["counts"]["all_rows_nonempty"] == 10, "stronger-claim negative control count mismatch")
    source = datasets[fixed.CONTROLS]
    motif_by_name = {m["name"]: (i, m) for i, m in enumerate(source["bounded_motif_signature_tables"])}
    checks = []
    for negative in negatives:
        motif_index, motif = motif_by_name[negative["motif"]]
        entry_index = negative["frozen_entry_index"]
        entry = motif["entries"][entry_index]
        require(entry["actual_boundary_attachments"] == negative["actual_boundary_attachments"], "negative-control attachment identity drift")
        vertices = motif["ordered_vertices"]
        edges = fixed.edgeset(motif["original_internal_edges"])
        edges |= {tuple(sorted((5, v))) for v in motif["contact_vertices"]}
        edges |= {tuple(sorted((v, b))) for v, actual in entry["actual_boundary_attachments"] for b in actual}
        support = sorted({b for _, actual in entry["actual_boundary_attachments"] for b in actual})
        piece = {"vertices": vertices, "edges": sorted(map(list, edges)), "roots": [5],
                 "contacts": [motif["contact_vertices"]], "attachments": entry["actual_boundary_attachments"], "support": support}
        shape = hypotheses(piece)
        require(shape["local_hypotheses_triggered"], "local hypotheses missing from stronger-claim counterexample")
        rows = []
        for label, beta in fixed.QS.items():
            cells = [fixed.assignments(vertices, edges, {**dict(enumerate(beta)), 5: c}) for c in range(4)]
            require(cells == negative["complete_equal_pin_lifts"][str(label)], "stronger-claim complete tuple mismatch")
            forbidden = [c for c, cell in enumerate(cells) if not cell]
            require(forbidden == negative["forbidden_equal_pins"][str(label)] and bool(forbidden), "stronger-claim forbidden owner colour mismatch")
            used = sorted(set(forbidden) & set(beta))
            require(len(used) <= 1, "stronger-claim control also violates generic theorem")
            rows.append({"target_label": label, "literal_beta": beta, "forbidden_equal_pins": forbidden,
                         "forbidden_used_colours": used, "complete_relation_sizes": list(map(len, cells)),
                         "complete_relation_sha256": list(map(fixed.digest, cells))})
            counts["negative_control_complete_equal_pin_cells"] += 4
        checks.append({"motif": negative["motif"], "frozen_entry_index": entry_index,
                       "frozen_source_pointer": f"/bounded_motif_signature_tables/{motif_index}/entries/{entry_index}",
                       "ordered_original_vertices": vertices, "original_region_edges_with_single_owner_interpretation": piece["edges"],
                       "actual_boundary_attachments": piece["attachments"], "actual_support": support,
                       "original_motif_contact_vertices": motif["contact_vertices"],
                       "interpretation": "Equal-pin query reinterpreted as one root owner; no source realization asserted",
                       "local_hypotheses": shape, "rows": rows,
                       "stronger_F_empty_some_target_row_claim": "counterexample"})
    return {"scope": probe["scope"], "probe_path": str(probe_path.relative_to(AUDIT)), "probe_sha256": sha256(raw).hexdigest(),
            "probe_counts": probe["counts"], "negative_controls": checks,
            "generic_theorem_status": "triggered and holds", "target_source_status": "not triggered"}


def validate_artifact(observed, pieces):
    require(len(observed["pieces"]) == 228, "generic artifact local piece coverage mismatch")
    for record, piece in zip(observed["pieces"], pieces):
        require(record["source_pointer"] == piece["pointer"], "generic artifact original piece pointer mismatch")
        shape = hypotheses(piece)
        require(record["local_hypotheses"] == shape, "generic artifact hypothesis or block decomposition mismatch")
        require(len(record["rows"]) == 10, "generic artifact must retain all ten original rows")
        for row_index, row in enumerate(record["rows"]):
            original = piece["rows"][row_index]
            cells = [original["fibres"][5 * c] for c in range(4)]
            forbidden = [c for c, cell in enumerate(cells) if not cell]
            require(row["forbidden_equal_pins"] == forbidden, "generic artifact complete equal-pin forbidden relation mismatch")
            require(row["forbidden_used_colours"] == sorted(set(forbidden) & set(original["beta"])),
                    "generic artifact used-forbidden colour mismatch")
            require(row["complete_equal_pin_relation_sha256"] == list(map(fixed.digest, cells)),
                    "generic artifact complete equal-pin tuple hash mismatch")


def build():
    base, base_hash, verified, datasets = fixed.frozen_inputs()
    pieces = fixed.saved_pieces(datasets)
    counts = Counter()
    fixed.source_custody(datasets, pieces, counts)
    records = []
    failure_histogram = Counter()
    for piece in pieces:
        shape = hypotheses(piece)
        if shape["local_hypotheses_triggered"]:
            counts["generic_local_hypotheses_triggered_pieces"] += 1
            counts[f"triggered_k_{shape['root_incidence_count']}_pieces"] += 1
            counts["triggered_actual_unary_pieces" if len(shape["active_original_root_owners"]) == 1
                   else "triggered_actual_mixed_equal_pin_pieces"] += 1
        else:
            counts["generic_local_hypotheses_not_triggered_pieces"] += 1
        for predicate, holds in shape["predicates"].items():
            failure_histogram[predicate] += not holds
        rows = equal_pin_rows(piece, shape, counts)
        records.append({"reference": piece["reference"], "source": piece["source"], "source_pointer": piece["pointer"],
                        "ordered_original_vertices": piece["vertices"], "ordered_roots": piece["roots"],
                        "original_region_edges": piece["edges"], "actual_support": piece["support"],
                        "actual_boundary_attachments": piece["attachments"], "local_hypotheses": shape, "rows": rows})
    stronger_claim = rejected_stronger_claim(datasets, counts)
    counts["all_saved_local_pieces"] = len(pieces)
    counts["all_saved_boundary_rows"] = sum(len(p["rows"]) for p in pieces)
    observed = {"schema": "generic-used-equal-pin-fixed-controls-v1", "frozen_head": base["head"], "BASE_sha256": base_hash,
                "verified_frozen_inputs": verified, "scope": "Only 228 saved local pieces; generic local used-equal-pin bound, no source enumeration or source exclusion",
                "generic_theorem": "On a proper global boundary row using exactly three colours, local hypotheses imply at most one forbidden used equal-pin colour",
                "target_source_status": "not triggered", "complete_target_sources": 0, "N2_55": "OPEN", "E_ARC2": "OPEN",
                "counts": dict(sorted(counts.items())), "local_hypothesis_failure_histogram": dict(sorted(failure_histogram.items())),
                "pieces": records, "stronger_empty_row_claim_control": stronger_claim}
    validate_artifact(observed, pieces)
    corrupted = deepcopy(observed)
    record = next(r for r in corrupted["pieces"] if r["local_hypotheses"]["local_hypotheses_triggered"])
    row = next(r for r in record["rows"] if r["three_colour_row"])
    row["forbidden_used_colours"] = [c for c in row["used_global_boundary_colours"] if c not in row["forbidden_used_colours"]][:2]
    require(len(row["forbidden_used_colours"]) == 2, "generic negative mutation failed")
    try:
        validate_artifact(corrupted, pieces)
    except ValueError as error:
        observed["artifact_negative_control"] = {"control_status": "counterexample", "corruption_rejected": True,
                  "mutation": "two wrong forbidden used colours added without changing complete tuple hashes", "reason": str(error)}
    else:
        raise ValueError("generic artifact corrupted F-used was accepted")
    return observed, pieces


def receipt(observed):
    return {"status": "PASS", "frozen_head": observed["frozen_head"], "BASE_sha256": observed["BASE_sha256"],
            "paper_checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "unchanged_base_checker_sha256": sha256((HERE / "checker.py").read_bytes()).hexdigest(),
            "paper_observations_sha256": fixed.digest(observed), "counts": observed["counts"],
            "artifact_negative_control": observed["artifact_negative_control"], "target_source_status": "not triggered",
            "complete_target_sources": 0, "N2_55": "OPEN", "E_ARC2": "OPEN"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--artifact", type=Path)
    args = parser.parse_args()
    observed, pieces = build()
    if args.check or args.artifact:
        path = args.artifact or HERE / "paper_observations.json"
        supplied = json.loads(path.read_bytes())
        validate_artifact(supplied, pieces)
        require(supplied == observed, "generic artifact differs from deterministic recalculation")
        if args.check and not args.artifact:
            require(json.loads((HERE / "paper_verification.json").read_bytes()) == receipt(observed), "generic verification receipt mismatch")
        print(json.dumps({"status": "PASS", "counts": observed["counts"]}, sort_keys=True))
    else:
        (HERE / "paper_observations.json").write_bytes(fixed.encoded(observed))
        verified = receipt(observed)
        (HERE / "paper_verification.json").write_bytes(fixed.encoded(verified))
        print(json.dumps(verified, sort_keys=True))


if __name__ == "__main__":
    main()
