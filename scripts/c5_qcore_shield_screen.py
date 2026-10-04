#!/usr/bin/env python3
"""Replay Task W's fixed-ledger shield certificate, without graph enumeration.

The arbitrary-size exclusion is a paper proof. Python checks the literal
source identities and the 2-per-piece lower-bound arithmetic, not the unknown
unary graphs/relations or the topological/Gallai lemmas. All predecessor files
are read-only. --write creates only a previously absent verdict artifact.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LEDGER = "artifacts/c5_open_leaf_ledger/ledger.json"
CELLS = "artifacts/c5_cells/cells.json"
OUT = ROOT / "artifacts/c5_qcore_shield_budget/verdicts.json"
# Paper dependencies are bound at a fixed commit, so later wording edits to these
# reports do not break the byte replay; the commit holds the bytes recorded in the
# revised verdict (the D6-audited v1 bound the pre-correction shield report).
DOCS_COMMIT = "e95912512f07cc3533ad4578076e4af65f82c277"
DOCS = (
    "docs/c5_unattached_boundary.md",
    "docs/c5_independent_support_capacity.md",
    "docs/c5_unary_shield_budget.md",
    "docs/c5_short_support_singleton.md",
    "docs/c5_excess_two_no_spoke_complete.md",
    "docs/c5_mixed_p3_common_endpoint.md",
    "docs/c5_open_leaf_ledger.md",
)
T4_INDICES = (2, 5, 7, 8, 9)
FRAME_EDGES = tuple((i, (i + 1) % 5) for i in range(5))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":")) + "\n").encode()


def digest(raw):
    return sha256(raw).hexdigest()


def pointer(value, path):
    for token in path.removeprefix("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def canonical(row):
    """One common color permutation, with the ordered boundary fixed."""
    names = {}
    return tuple(names.setdefault(color, len(names)) for color in row)


def recolor_controls(cells):
    patterns = cells["pattern_order"]
    require(len(patterns) == 10, "boundary pattern order drift")
    require([i for i, q in enumerate(patterns) if len(set(q)) == 4]
            == list(T4_INDICES), "T4 indices drift")
    witnesses = []
    for row in product(range(4), repeat=5):
        if len(set(row)) != 3 or any(row[a] == row[b] for a, b in FRAME_EDGES):
            continue
        counts = Counter(row)
        singleton = next(i for i, color in enumerate(row) if counts[color] == 1)
        index = patterns.index(list(canonical(row)))
        require(cells["singleton_of_three_colour"][str(index)] == singleton,
                "named singleton mapping drift")
        unused = next(color for color in range(4) if color not in counts)
        for vertex in range(5):
            if vertex == singleton:
                continue
            changed = list(row)
            changed[vertex] = unused
            new_index = patterns.index(list(canonical(changed)))
            require(new_index in T4_INDICES, "non-singleton recoloring is not T4")
            witnesses.append({"row": list(row), "singleton": singleton,
                              "vertex": vertex, "changed_row": changed,
                              "changed_pattern_index": new_index})
    require(len(witnesses) == 480, "recolor control count drift")
    # Recoloring the singleton stays three-colored: it cannot justify that case.
    singleton_changes = []
    for index, singleton in sorted(cells["singleton_of_three_colour"].items()):
        changed = list(patterns[int(index)])
        changed[singleton] = next(c for c in range(4) if c not in changed)
        require(len(set(changed)) == 3, "singleton negative control drift")
        singleton_changes.append({"pattern_index": int(index),
                                  "singleton": singleton, "changed_row": changed,
                                  "is_T4": False})
    return {"proper_labeled_three_color_rows": 120,
            "non_singleton_recolorings": witnesses,
            "singleton_negative_controls": singleton_changes}


def connected(vertices, edges):
    if not vertices:
        return False
    seen = {min(vertices)}
    while True:
        grown = seen | {b for a, b in edges if a in seen and b in vertices}
        grown |= {a for a, b in edges if b in seen and a in vertices}
        if grown == seen:
            return seen == vertices
        seen = grown


def piece_certificate(row):
    """Check recorded source premises, without inventing unary own supports."""
    q = row["common_color_frame"]
    require(q == [0, 1, 0, 1, 2], "shared literal frame drift")
    require(row["original_components"] == {
        "P3": "x0-x1-x2", "ordered_vertices": ["x0", "x1", "x2"],
        "root_masks": [0, 0, 3]}, "original mixed component identity drift")
    supports = row["original_P3_actual_supports"]
    require(list(map(len, supports)) == [3, 2, 1], "original attachments drift")
    require(all(len(set(s)) == len(s) and set(s) <= set(range(5)) for s in supports),
            "invalid original support")
    require({q[b] for b in supports[0]} == {0, 1, 2}, "x0 three-color support drift")
    mixed_support = sorted(set().union(*map(set, supports)))
    require(len(mixed_support) >= 3, "mixed piece lacks long-shield premise")

    lists = [sorted(set(range(4)) - {q[b] for b in s}) for s in supports]
    tuples = [list(t) for t in product(*lists) if t[0] != t[1] and t[1] != t[2]]
    require(tuples == row["original_P3_complete_tuples"], "complete P3 tuples drift")
    pairs = [list(pair) for pair in product(range(4), repeat=2)
             if not any(t[2] not in pair for t in tuples)]
    require(pairs == row["original_P3_forbidden_pairs"], "ordered forbidden pairs drift")
    for pair, fibre in zip(product(range(4), repeat=2),
                           row["complete_P3_root_fibres"], strict=True):
        expected = [t for t in tuples if t[2] not in pair]
        require(fibre["root_pair"] == list(pair)
                and fibre["complete_original_P3_tuples"] == expected
                and fibre["full_P3_lifts"] == [dict(zip(("x0", "x1", "x2"), t))
                                               for t in expected], "full root fibre drift")

    unary = row["original_unary_components"]
    vertices = {"z", "w", "C*"} | {d["component"] for d in unary}
    edges = [("z", "w"), ("z", "C*"), ("w", "C*")]
    require(len(vertices) == 3 + len(unary), "duplicate component identity")
    for root, role_key in (("z", "z_role"), ("w", "w_role")):
        role = row[role_key]
        pieces = [d for d in unary if d["root"] == root]
        require(len(pieces) == len(role["unary_contacts"]) >= 1,
                "retained key lacks a unary on each root")
        require(len(role["spoke_colors"]) + sum(role["unary_contacts"]) + 2 == 5,
                "original root degree budget drift")
        for d, contacts, forbidden in zip(pieces, role["unary_contacts"],
                                          role["unary_forbidden"], strict=True):
            require(len(d["ordered_original_contacts"]) == contacts,
                    "ordered original contact count drift")
            require(d["forbidden_colors"] == forbidden and 0 < len(forbidden) <= contacts,
                    "private forbidden-color premise drift")
            edges.append((root, d["component"]))
    require(all(d["root"] in ("z", "w") for d in unary), "foreign unary owner")
    require(connected(vertices, edges), "component incidence graph disconnected")
    removed_pieces = ["C*"] + [d["component"] for d in unary]
    require(all(connected(vertices - {piece}, edges) for piece in removed_pieces),
            "one-sided premise failed")

    # If any unary were supported in this frame edge, this SAME original path
    # gives the external hub required by the short-support paper lemma.
    external_paths = []
    for a, b in FRAME_EDGES:
        h = min(set(supports[0]) - {a, b})
        external_paths.append({"hypothetical_short_support_edge": [a, b],
                               "h": h, "path": ["r", "x2", "x1", "x0", f"b{h}"]})
    costs = {"C*": 2, **{d["component"]: 2 for d in unary}}
    total = sum(costs.values())
    require(total > 5, "shield budget does not exclude this key")
    return {"original_mixed_support": mixed_support,
            "piece_owners": [[d["component"], d["root"]] for d in unary],
            "one_sided_incidence_edges": [list(e) for e in edges],
            "external_path_template_r_is_each_unary_owner": external_paths,
            "shield_lower_bounds": costs, "required_frame_edges": total,
            "available_frame_edges": 5,
            "basis": ["topology_1b", "short_support_external_path",
                      "topology_1d", "fixed_C_original_premises"]}


def build():
    sources = {}

    def read(path):
        raw = (ROOT / path).read_bytes()
        sources[path] = {"sha256": digest(raw), "bytes": len(raw)}
        return json.loads(raw)

    ledger, cells = read(LEDGER), read(CELLS)
    payloads = {}
    for path, recorded in sorted(ledger["sources"].items()):
        payloads[path] = read(path)
        require(sources[path] == recorded, f"ledger input hash drift: {path}")
    for path in DOCS:
        raw = subprocess.check_output(["git", "show", f"{DOCS_COMMIT}:{path}"], cwd=ROOT)
        sources[path] = {"sha256": digest(raw), "bytes": len(raw)}
    scope, common = payloads[ledger["scope_source"]], payloads[ledger["common_source"]]
    require(len(ledger["leaves"]) == len(scope["ledger"]) == 3500, "domain size drift")
    all_keys = [leaf["key"] for leaf in ledger["leaves"]]
    require(len(set(map(tuple, all_keys))) == 3500, "duplicate literal key")
    require(digest(encode(sorted(all_keys))) == ledger["domain_sha256"], "domain hash drift")
    require(set(map(tuple, all_keys)) == {tuple(r["key"]) for r in scope["ledger"]},
            "scope coverage drift")
    certificates, verdicts, skipped = {}, [], []
    unary_counts, own_unknown = Counter(), 0
    boundary_coverage = Counter()
    for li, leaf in enumerate(ledger["leaves"]):
        row = pointer(scope, leaf["scope_pointer"])
        require(row["key"] == leaf["key"], "literal key/pointer mismatch")
        case = pointer(common, leaf["common_case_pointer"])
        geometry = pointer(common, leaf["common_geometry_pointer"])
        require(row["case"] == case and row["geometry"] == geometry,
                "common named source payload drift")
        require(leaf["id"] == f'C/{leaf["key"][0]}/g{leaf["key"][1]}/j{leaf["key"][2]}',
                "stable leaf ID drift")
        config = next(c for c in common["local"]["configurations"]
                      if c["id"] == case["local_id"])
        side_ids = common["local"]["joins_by_a"][str(config["a"])][leaf["key"][2]]
        require(row["side_ids"] == side_ids, "shared side join identity drift")
        require(row["z_role"] == common["local"]["side_roles"][side_ids[0]]
                and row["w_role"] == common["local"]["side_roles"][side_ids[1]],
                "original owner roles drift")
        if leaf["status"] != "open_unreviewed":
            require(leaf["status"] == "closed_source_excluded"
                    and row["closed_by"] == [leaf["closed_by"]], "inherited closure drift")
            skipped.append({"id": leaf["id"], "key": leaf["key"],
                            "closed_by": leaf["closed_by"]})
            continue
        require(not row["closed_by"] and leaf["closed_by"] is None, "open/closed mismatch")
        certificate = piece_certificate(row)
        certificate_id = digest(encode(certificate))
        certificates[certificate_id] = certificate
        verdicts.append({"id": leaf["id"], "key": leaf["key"],
                         "ledger_pointer": f"/leaves/{li}",
                         "scope_pointer": leaf["scope_pointer"],
                         "complete_scope_row_sha256": digest(encode(row)),
                         "certificate": certificate_id,
                         "verdict": "source_excluded_by_paper_shield_budget"})
        unary_counts[len(row["original_unary_components"])] += 1
        own_unknown += sum(d["actual_own_support"] is None
                           for d in row["original_unary_components"])
        # This is a whole-source coverage AUDIT, never a unary own-support.
        covered = set().union(*map(set, row["original_P3_actual_supports"]),
                              *map(set, geometry["actual_side_supports"]))
        boundary_coverage[",".join(map(str, sorted(covered)))] += 1
    require(len(verdicts) == 3497 and len(skipped) == 3, "open-key census drift")
    require(dict(unary_counts) == {2: 1258, 3: 1679, 4: 560}, "unary census drift")
    # Necessary-budget controls: two long shields fit; three do not. Missing
    # T4 does not imply compulsory non-singleton coverage in this broader C.
    controls = {"two_long_pieces_lower_bound": 4, "two_long_pieces_excluded": 4 > 5,
                "three_long_pieces_lower_bound": 6, "three_long_pieces_excluded": 6 > 5,
                "unknown_unary_own_supports_kept_unknown": own_unknown,
                "broader_C_T4_assumed": False,
                "non_singleton_coverage_not_recorded_for_keys": 1197}
    require(own_unknown == 8398, "unknown own-support count drift")
    require(dict(boundary_coverage) == {"0,1,2,3,4": 2300, "0,1,2,4": 597,
                                       "1,2,3,4": 600}, "coverage audit drift")
    return {"schema": 1, "task": "W/q-core shield budget and fixed C ledger screen",
            "baseline_commit": "ca3870f9b79684c2100480d0dc04523899666928",
            "sources": sources, "ledger_source": LEDGER,
            "scope_source": ledger["scope_source"],
            "common_source": ledger["common_source"],
            "domain_sha256": ledger["domain_sha256"],
            "evidence": {"paper": "docs/c5_qcore_shield_budget.md §§2-5",
                         "external": "degree-list/Gallai; inherited short-support hub proof",
                         "python": "480 boundary recolorings and literal finite ledger certificate replay",
                         "lean": "none",
                         "limit": "No unary graph/relation realization, full Sigma, target extension, or general exit check"},
            "recolor_controls": recolor_controls(cells),
            "negative_controls": controls, "whole_source_support_census": dict(boundary_coverage),
            "certificates": certificates, "verdicts": verdicts,
            "inherited_closed_keys_not_counted_as_new": skipped,
            "summary": {"catalogue_keys": 3500, "input_open_keys": 3497,
                        "screened_keys": 3497, "newly_source_excluded_keys": 3497,
                        "remaining_open_keys_under_fixed_C_premises": 0,
                        "unary_count_distribution": dict(sorted(unary_counts.items())),
                        "ledger_writes": 0, "producer_runs": 0,
                        "graph_enumerations": 0, "target_queries": 0}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="read-only exact byte replay")
    mode.add_argument("--write", action="store_true", help="create a new verdict file; never overwrite")
    args = parser.parse_args()
    result = build()
    raw = encode(result)
    if args.check:
        require(OUT.read_bytes() == raw, "verdict artifact differs from replay")
    elif args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with OUT.open("xb") as stream:
            stream.write(raw)
    print("OK:", json.dumps(result["summary"], sort_keys=True),
          f"artifact_bytes={len(raw)} sha256={digest(raw)}")


if __name__ == "__main__":
    main()
