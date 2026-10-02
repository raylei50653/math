#!/usr/bin/env python3
"""Check explicit common-repair hypotheses on the six existing named joins.

The general equivalence is a paper proof. This certificate checks full literal
relations, exact witness rejectors and both cover laws, independently of the
saved minimal-repair answer. No new graph search or Lean claim.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from c5_two_vertex_join import CASES
from c5_two_vertex_repair_transport import (
    DOMAIN, FRAMES, SOURCE, check_hashes, minimal_covers, project, reconstruct,
    relation, verify_frame_proofs, word,
)

ROOT = Path(__file__).resolve().parents[1]
AUDIT = "artifacts/c5_two_vertex_overlap/repair_transport.json"
OUT = ROOT / "artifacts/c5_two_vertex_overlap/common_repair.json"


def union(parts):
    return set().union(*parts)


def signatures(a, b, t, es):
    return ({a}, {b, t}, {b} | set(es))


def rejectors(row, cuts):
    return {i for i, cut in enumerate(cuts) if row in cut}


def verify_hypotheses(delta, cuts, a, b, t, es, witnesses):
    """Accept explicit witnesses, never a claimed minimal-cover classification."""
    indices = set(range(len(cuts)))
    assert len({a, b, t}) == 3 and {a, b, t} <= indices
    assert es and len(es) == len(set(es)) and set(es) <= indices - {a, b, t}
    assert all(cut <= delta for cut in cuts)
    assert len(witnesses) == 3
    for row, expected in zip(witnesses, signatures(a, b, t, es)):
        assert row in delta and rejectors(row, cuts) == expected, "witness signature"
    assert cuts[a] | cuts[b] == delta, "AB coverage"
    assert all(cuts[a] | cuts[t] | cuts[e] == delta for e in es), "ATE coverage"
    return sorted([tuple(sorted((a, b)))] + [tuple(sorted((a, t, e))) for e in es],
                  key=lambda ids: (len(ids), ids))


def verify_lift(encoded, row, scope, graph, joint):
    full = tuple(map(int, encoded))
    assert len(full) == len(graph["vertices"]) and set(full) <= set(range(4))
    assert all(full[u] != full[v] for u, v in graph["edges"])
    assert full[:8] in joint and project(full, scope) == project(row, scope)


def audit_case(source, saved, frames, catalogue, order):
    joint, _, _ = reconstruct(source, catalogue, order)
    verify_frame_proofs(frames, source["graph"])
    frame_scopes = [tuple(f["cycle"]) for f in frames if f["available"]]
    frame_relations = [{project(q, s) for q in joint} for s in frame_scopes]
    pullback = {q for q in DOMAIN if all(project(q, s) in local
                for s, local in zip(frame_scopes, frame_relations))}
    assert joint <= pullback
    delta = pullback - joint
    assert saved["J"] == relation(joint) and saved["P"] == relation(pullback)
    assert saved["difference"] == relation(delta)
    ports = source["joint"]["ports"]
    result = {"name": source["name"], "ports": ports,
              "J": relation(joint), "P": relation(pullback), "difference": relation(delta)}
    if not delta:
        assert joint == pullback and saved["minimum_sufficient_arity"] == 0
        assert [r["scope_ids"] for r in saved["all_inclusion_minimal_repairs"]] == [[]]
        result.update(branch="P_equals_J", all_inclusion_minimal_repairs=[[]],
                      forced_scope_ids=[], r_star=0)
        return result

    # Fix named roles before inspecting the old answer or detected structure.
    assert source["name"] in ("private_interiors", "private_interiors_reverse")
    scopes = list(combinations(range(8), 4))

    def scope_id(names):
        return scopes.index(tuple(sorted(ports.index(v) for v in names)))

    a = scope_id(("a0", "a1", "a2", "a3"))
    t = scope_id(("a0", "a2", "b0", "b2"))
    b = scope_id(("a0" if source["name"] == "private_interiors" else "a2",
                  "b0", "b2", "b4"))
    missing_edge = {ports.index("b2"), ports.index("b4")}
    es = [i for i, s in enumerate(scopes) if missing_edge <= set(s) and i != b]
    local = [{project(q, s) for q in joint} for s in scopes]
    cuts = [{q for q in delta if project(q, s) not in r} for s, r in zip(scopes, local)]
    assert [r["relation"] for r in saved["scope_catalog"]] == [relation(r) for r in local]
    words = (("01232113", "01201130", "01012122") if source["name"] == "private_interiors"
             else ("01232112", "01212132", "01012122"))
    witnesses = [tuple(map(int, w)) for w in words]
    templates = verify_hypotheses(delta, cuts, a, b, t, es, witnesses)
    witness_pool = {r["pattern"]: r for r in saved["witness_pool"]}
    records = []
    for label, row, rejected in zip(("A", "BT", "BE"), witnesses, signatures(a, b, t, es)):
        data = witness_pool[word(row)]
        assert data["rejected_scope_ids"] == sorted(rejected)
        assert data["original_graph_extension_exists"] is False and row not in joint
        accepted = sorted(set(range(len(scopes))) - rejected)
        assert [r["scope_id"] for r in data["accepted_scope_lifts"]] == accepted
        for r in data["accepted_scope_lifts"]:
            verify_lift(r["full_colouring"], row, scopes[r["scope_id"]], source["graph"], joint)
        assert len(data["separate_frame_lifts"]) == len(frame_scopes)
        for encoded, s in zip(data["separate_frame_lifts"], frame_scopes):
            verify_lift(encoded, row, s, source["graph"], joint)
        # The three maximal failed families are complements of exact signatures.
        residual = delta - union(cuts[i] for i in accepted)
        assert row in residual and all(rejectors(q, cuts) == rejected for q in residual)
        assert all(union(cuts[j] for j in accepted + [i]) == delta for i in rejected)
        records.append({"role": label, "witness": data,
                        "maximal_failed_scope_ids": accepted,
                        "complete_residual": relation(residual)})

    # Compare predictions only after every hypothesis has been checked.
    assert [list(ids) for ids in templates] == [r["scope_ids"] for r in saved["all_inclusion_minimal_repairs"]]
    template_records = []
    for ids in templates:
        repaired = {q for q in pullback if all(project(q, scopes[i]) in local[i] for i in ids)}
        assert repaired == joint
        deletion = []
        for omitted in ids:
            row = witnesses[0 if omitted == a else 1 if omitted in (b, t) else 2]
            assert row in cuts[omitted] and all(row not in cuts[i] for i in ids if i != omitted)
            deletion.append({"omitted_scope_id": omitted, "witness_pattern": word(row)})
        template_records.append({"scope_ids": ids, "uncovered_difference": relation(delta - union(cuts[i] for i in ids)),
                                 "repaired_relation_equals_J": True, "uniform_deletion_witnesses": deletion})
    result.update(branch="common_repair", roles={"A": a, "B": b, "T": t, "E": es},
                  scope_catalog=[{"scope_id": i, "ports": [ports[v] for v in s]} for i, s in enumerate(scopes)],
                  hypothesis_witnesses=records, cover_laws=template_records,
                  all_inclusion_minimal_repairs=templates, forced_scope_ids=[a],
                  minimum_projection_count=2,
                  accepted_scope_lifts_checked=sum(len(r["witness"]["accepted_scope_lifts"]) for r in records))
    return result


def premise_controls():
    """Small countermodels: every one of the five laws is independently needed."""
    a, b, t, es = 0, 1, 2, (3, 4)
    base = [{a}, {b, t}, {b, *es}]
    specs = [
        ("without_W_A", base[1:], 0),
        ("without_W_BT", base[:1] + base[2:], 1),
        ("without_W_BE", base[:2], 2),
        ("without_C_AB", base + [{t, *es}], 3),
        ("without_C_ATE_for_E2", base + [{b, es[0]}], 4),
    ]
    records = []
    for name, incidence, omitted in specs:
        delta = set(range(len(incidence)))
        cuts = [{q for q in delta if i in incidence[q]} for i in range(5)]
        flags = [any(rejectors(q, cuts) == expected for q in delta)
                 for expected in signatures(a, b, t, es)]
        flags += [cuts[a] | cuts[b] == delta,
                  all(cuts[a] | cuts[t] | cuts[e] == delta for e in es)]
        assert flags == [i != omitted for i in range(5)]
        predicted = [(a, b), (a, t, es[0]), (a, t, es[1])]
        actual = minimal_covers(cuts, delta)
        assert actual != predicted
        # The real premise verifier must reject every malformed input too.
        witnesses = [next((q for q in delta if rejectors(q, cuts) == expected), -1)
                     for expected in signatures(a, b, t, es)]
        try:
            verify_hypotheses(delta, cuts, a, b, t, es, witnesses)
        except AssertionError:
            pass
        else:
            raise AssertionError(name)
        records.append({"name": name, "row_rejectors": [sorted(s) for s in incidence],
                        "hypotheses_WA_WBT_WBE_CAB_CATE": flags,
                        "actual_minimal_repairs": actual, "premise_verifier_rejected": True})
    return records


def build():
    audit = json.loads((ROOT / AUDIT).read_text())
    source = json.loads((ROOT / SOURCE).read_text())
    frames = json.loads((ROOT / FRAMES).read_text())
    for saved in (audit, source, frames):
        check_hashes(saved)
    catalogue_path = "artifacts/c5_cells/cells.json"
    catalogue = json.loads((ROOT / catalogue_path).read_text())
    assert [c["name"] for c in source["cases"]] == [spec[0] for spec in CASES]
    assert [c["name"] for c in audit["cases"]] == [c["name"] for c in source["cases"]]
    cases = [audit_case(c, saved, frames["cases"][c["name"]], catalogue,
                        tuple(map(tuple, source["pattern_order"])))
             for c, saved in zip(source["cases"], audit["cases"])]
    controls = premise_controls()
    paths = [AUDIT, SOURCE, FRAMES, catalogue_path, "scripts/c5_two_vertex_common_repair.py",
             "scripts/c5_two_vertex_repair_transport.py", "scripts/c5_two_vertex_join.py",
             "scripts/c5_two_vertex_join_topology.py", "scripts/boundary_relations.py"]
    return {"schema": "c5-common-repair-hypotheses-v1",
            "scope": "Paper iff lemma for sound conditions; fixed six-graph premise checks. P alone, original named U, one colour frame, no new class pairs or Lean theorem.",
            "source_sha256": {p: sha256((ROOT / p).read_bytes()).hexdigest() for p in paths},
            "relation_encoding": audit["relation_encoding"], "hash_encoding": audit["hash_encoding"],
            "cases": cases, "premise_independence_controls": controls,
            "summary": {"cases": len(cases), "degenerate_cases": sum(c["branch"] == "P_equals_J" for c in cases),
                        "nondegenerate_cases": sum(c["branch"] == "common_repair" for c in cases),
                        "explicit_witnesses": sum(len(c.get("hypothesis_witnesses", [])) for c in cases),
                        "cover_equalities": sum(len(c.get("cover_laws", [])) for c in cases),
                        "uniform_deletion_checks": sum(len(r["uniform_deletion_witnesses"]) for c in cases for r in c.get("cover_laws", [])),
                        "accepted_scope_lifts": sum(c.get("accepted_scope_lifts_checked", 0) for c in cases),
                        "independence_controls": len(controls), "new_lean_theorem": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="recompute and compare without writing")
    args = parser.parse_args()
    result = build()
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != payload:
            raise SystemExit(f"FAIL: common-repair certificate differs or is missing: {OUT}")
    else:
        OUT.write_bytes(payload)
    print(json.dumps({"mode": "check" if args.check else "write", "status": "pass",
                      "bytes": len(payload), **result["summary"]}))


if __name__ == "__main__":
    main()
