#!/usr/bin/env python3
"""Census the fixed common-endpoint P3 catalogue; never infer source existence.

The 140 x 25 expansion follows D3 audit_scope.py. Complete same-graph payloads
stay in the sealed D5 ledger and are referenced by SHA256 and JSON pointer.
No producer is executed and no predecessor artifact is rewritten.

Two versions are produced (D6 merge plan).  The C4 ledger at OUT stays byte
for byte the predecessor that the W verdict hashed; the cw-v1 ledger applies
W's batch verdict on top of it.  --dry-run builds both and writes nothing.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_open_leaf_ledger"
COMMON = "artifacts/c5_mixed_p3_common_endpoint/observations.json"
SCOPE = "audits/2026-10-04-task-d5/c4/scope_ledger.json"
CW_OUT = OUT / "cw-v1"
PUBLICATION = "83ca6180d7724ba357f971fddd1b5e00867daaa1"
# Named stage specs.  "single" stages close one literal key via /identity;
# the "batch" stage closes a whole key set via /verdicts (built in build_cw).
STAGES = (
    {"stage": "C2", "kind": "single", "producer": "c5_mixed_p3_one_color_ternary_unary",
     "target": ("CPP-134-1", 30, 20)},
    {"stage": "C3", "kind": "single", "producer": "c5_mixed_p3_two_frame_ternary_unary",
     "target": ("CPP-134-1", 34, 20)},
    {"stage": "C4", "kind": "single", "producer": "c5_mixed_p3_two_frame_two_unary",
     "target": ("CPP-134-1", 34, 60)},
)
W_STAGE = {"stage": "W", "kind": "batch",
           "source": "artifacts/c5_qcore_shield_budget/verdicts.json",
           "verdict": "source_excluded_by_paper_shield_budget",
           "published_commit": "e95912512f07cc3533ad4578076e4af65f82c277",
           "audit": "audits/2026-10-04-task-d6/REPORT.md"}
PREDECESSOR = "artifacts/c5_open_leaf_ledger/ledger.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def leaf_id(key):
    return f"C/{key[0]}/g{key[1]}/j{key[2]}"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def reconcile(universe, before, after, declared_closed):
    """A new key or an overbroad deletion cannot masquerade as progress."""
    require(before <= universe and after <= universe, "foreign leaf key")
    require(after <= before, "unexpected reopening in closure event")
    require(before - after == declared_closed, "closure exceeds the exact named scope")


def build():
    sources = {}

    def read(path):
        raw = (ROOT / path).read_bytes()
        sources[path] = {"sha256": digest(raw), "bytes": len(raw)}
        return json.loads(raw)

    common, scope = read(COMMON), read(SCOPE)
    cases = {c["id"]: (i, c) for i, c in enumerate(common["local"]["cases"])}
    local = {c["id"]: c for c in common["local"]["configurations"]}
    geometries = common["geometry"]["retained_geometries"]
    require(len(cases) == len(common["local"]["cases"]), "duplicate source case")
    retained_cases = {g["case_id"] for g in geometries}
    require(len(retained_cases) == common["geometry"]["retained_cases"] == 36,
            "retained case identity drift")
    require(len({g["id"] for g in geometries}) == len(geometries) == 140, "geometry identity drift")
    require(common["geometry"]["retained_side_role_joins"] == 900, "join catalogue drift")
    indexed = {tuple(r["key"]): (i, r) for i, r in enumerate(scope["ledger"])}
    require(len(indexed) == len(scope["ledger"]) == 3500, "duplicate or missing D5 key")
    leaves, parents = [], []
    for case_id in sorted(retained_cases):
        _, case = cases[case_id]
        parents.append({"id": f'C/{case["name"]}', "parent": "C", "level": "case"})
    for gi, geometry in enumerate(geometries):
        ci, case = cases[geometry["case_id"]]
        config = local[case["local_id"]]
        parent = f'C/{case["name"]}/g{geometry["id"]}'
        parents.append({"id": parent, "parent": f'C/{case["name"]}', "level": "geometry"})
        joins = case["side_join_ids"]
        require(len(joins) == len(set(joins)) == 25, "case-side join identity drift")
        for join in joins:
            key = (case["name"], geometry["id"], join)
            require(key in indexed, f"missing sealed scope: {key}")
            si, sealed = indexed[key]
            side_ids = common["local"]["joins_by_a"][str(config["a"])][join]
            require(sealed["case"] == case and sealed["geometry"] == geometry,
                    f"case or geometry payload changed: {key}")
            require(sealed["side_ids"] == side_ids, f"ownership changed: {key}")
            require(sealed["original_P3_complete_tuples"] == config["complete_triples"],
                    f"ordered P3 relation changed: {key}")
            for owner, side in zip(("z_role", "w_role"), side_ids, strict=True):
                require(sealed[owner] == common["local"]["side_roles"][side],
                        f"original side role changed: {key}")
            leaves.append({"id": leaf_id(key), "parent": parent, "key": list(key),
                           "scope_pointer": f"/ledger/{si}",
                           "common_geometry_pointer": f"/geometry/retained_geometries/{gi}",
                           "common_case_pointer": f"/local/cases/{ci}",
                           "status": "open_unreviewed", "closed_by": None})
    universe = {tuple(r["key"]) for r in leaves}
    require(universe == set(indexed), "catalogue coverage is not exact")
    leaves.sort(key=lambda r: r["id"])
    require(len({r["id"] for r in leaves}) == 3500, "duplicate stable leaf ID")
    parents.sort(key=lambda r: r["id"])
    open_keys = set(universe)
    events, trend = [], []

    def census(stage, new_closed):
        return {"stage": stage, "open_leaves": len(open_keys),
                "closed_leaves": len(universe - open_keys), "new_closed": new_closed,
                "new_leaves": 0, "split_events": 0, "split_net": 0, "reopened": 0,
                "open_cases": len({k[0] for k in open_keys}),
                "open_case_geometries": len({k[:2] for k in open_keys})}

    trend.append(census("C0_reconstructed_baseline", 0))
    for spec in STAGES:
        require(spec["kind"] == "single", f"C4 prefix holds single stages only: {spec['stage']}")
        stage, producer, target = spec["stage"], spec["producer"], spec["target"]
        path = f"artifacts/{producer}/observations.json"
        result = read(path)
        identity = result["identity"]
        entry = identity.get("parent_entry")
        actual = ((entry["case_name"], entry["geometry_id"], entry["side_join_id"])
                  if entry else (identity["case"]["name"], identity["geometry"]["id"], identity["side_join_id"]))
        require(actual == target, f"producer scope changed: {stage}")
        require(result["summary"]["named_source_branches_closed"] == 1,
                f"producer does not close exactly one named branch: {stage}")
        require(result["summary"]["predecessor_deletions"] == result["summary"]["target_queries"] == 0,
                f"predecessor or target scope drift: {stage}")
        require(target in open_keys, f"duplicate closure: {target}")
        after = open_keys - {target}
        reconcile(universe, open_keys, after, {target})
        events.append({"event_id": stage, "sequence": len(events) + 1, "type": "close",
                       "leaf_id": leaf_id(target), "key": list(target),
                       "report_date": "2026-10-04", "research_completed_at": None,
                       "published_commit": PUBLICATION, "evidence": path,
                       "evidence_pointer": "/identity", "scope_delta": -1,
                       "evidence_layer": "reported arbitrary-size paper + finite Python; inherited independent audit; no Lean"})
        open_keys = after
        trend.append(census(stage, 1))
    closure_by_key = {tuple(e["key"]): e["event_id"] for e in events}
    require(set(closure_by_key) == {tuple(k) for k in scope["closed_named_keys"]},
            "registered closures differ from sealed D5 verdicts")
    for row in leaves:
        key = tuple(row["key"])
        sealed = indexed[key][1]
        require(set(sealed["closed_by"]) == ({closure_by_key[key]} if key in closure_by_key else set()),
                f"sealed leaf verdict mismatch: {key}")
        if key in closure_by_key:
            row.update(status="closed_source_excluded", closed_by=closure_by_key[key])
    require(sum(r["status"] == "open_unreviewed" for r in leaves) == 3497, "leaf census mismatch")
    require(scope["not_audited_named_keys"] == 3497, "sealed open count mismatch")
    require(("CPP-134-1", 35, 20) in open_keys, "next named entry prematurely closed")

    # Meaningful scope controls: all three historical overbroad predicates fail.
    controls = []
    target = STAGES[0]["target"]
    for name, wrong in (
        ("whole_case", {k for k in universe if k[0] == target[0]}),
        ("whole_geometry", {k for k in universe if k[:2] == target[:2]}),
        ("join_across_case_geometries", {k for k in universe if k[0] == target[0] and k[2] == target[2]}),
    ):
        try:
            reconcile(universe, universe, universe - wrong, {target})
        except ValueError:
            controls.append({"name": name, "rejected": True, "extra_closed": len(wrong - {target})})
        else:
            raise ValueError(f"overbroad closure accepted: {name}")
    require([c["extra_closed"] for c in controls] == [149, 24, 5], "scope negative controls drift")
    domain_hash = digest(encode(sorted(universe)).encode())
    return {"schema": 1, "cohort": "weak-deletion/common-endpoint-P3/C",
            "unit": "one literal (case, geometry, side_join) necessary index key",
            "domain_sha256": domain_hash, "sources": sources,
            "scope_source": SCOPE, "common_source": COMMON,
            "parents": parents, "leaves": leaves, "events": events, "trend": trend,
            "negative_controls": controls,
            "coverage": {"cases": 36, "case_geometries": 140, "case_side_joins": 900,
                         "catalogue_leaves": 3500, "global_weak_deletion_leaf_count": None,
                         "unindexed_gaps": ["larger or multiple mixed components", "more incidences",
                                             "nonadjacent roots or more roots", "higher degrees outside this catalogue",
                                             "per-coloring repair", "general single-sided and common exits", "K∞=K≤5"]},
            "time": {"stage_order_is_dependency_order": True,
                     "baseline_is_reconstructed_not_historical_observation": True,
                     "publication_commit": PUBLICATION,
                     "publication_at": git("show", "-s", "--format=%aI", PUBLICATION),
                     "daily_samples": [{"date": "2026-10-03", "open_leaves": None,
                                        "reason": "no same-cohort dated census"},
                                       {"date": "2026-10-04", "open_leaves": 3497,
                                        "basis": "published C4 catalogue verdicts"}],
                     "leaves_per_day": None}}


def pointer(document, path):
    value = document
    for token in path.removeprefix("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def extract_batch(result, predecessor, scope, open_keys, inherited):
    """Exact batch closure: the verdict key set must equal the open set."""
    universe = {tuple(r["key"]) for r in predecessor["leaves"]}
    require(result["domain_sha256"] == predecessor["domain_sha256"], "batch domain drift")
    require((result["common_source"], result["scope_source"], result["ledger_source"])
            == (COMMON, SCOPE, PREDECESSOR), "batch source paths drift")
    require(result["sources"][PREDECESSOR]["sha256"] == digest(encode(predecessor).encode()),
            "batch was not computed on this predecessor ledger")
    seen, closed = set(), []
    for i, verdict in enumerate(result["verdicts"]):
        key = tuple(verdict["key"])
        require(key in universe, f"foreign batch key: {key}")
        require(key not in inherited, f"inherited closure counted as new: {key}")
        require(key not in seen, f"duplicate batch key: {key}")
        seen.add(key)
        require(verdict["id"] == leaf_id(key), f"batch leaf ID mismatch: {key}")
        require(verdict["verdict"] == W_STAGE["verdict"], f"batch verdict string: {key}")
        row = pointer(scope, verdict["scope_pointer"])
        require(tuple(row["key"]) == key, f"scope pointer mismatch: {key}")
        require(digest(encode(row).encode()) == verdict["complete_scope_row_sha256"],
                f"complete scope row changed: {key}")
        leaf = pointer(predecessor, verdict["ledger_pointer"])
        require(tuple(leaf["key"]) == key and leaf["status"] == "open_unreviewed",
                f"predecessor leaf pointer mismatch: {key}")
        certificate = result["certificates"][verdict["certificate"]]
        require(digest(encode(certificate).encode()) == verdict["certificate"],
                f"certificate hash mismatch: {key}")
        closed.append((i, key, verdict["certificate"]))
    require(seen == open_keys, "batch must close exactly the open key set")
    require(result["summary"]["newly_source_excluded_keys"] == len(seen)
            and result["summary"]["target_queries"] == 0, "batch summary drift")
    return closed


def build_cw(predecessor):
    sources = {}

    def read(path):
        raw = (ROOT / path).read_bytes()
        sources[path] = {"sha256": digest(raw), "bytes": len(raw)}
        return json.loads(raw)

    scope, result = read(SCOPE), read(W_STAGE["source"])
    ledger = copy.deepcopy(predecessor)
    universe = {tuple(r["key"]) for r in ledger["leaves"]}
    open_keys = {tuple(r["key"]) for r in ledger["leaves"] if r["status"] == "open_unreviewed"}
    inherited = {tuple(e["key"]): e["event_id"] for e in ledger["events"]}
    require(len(open_keys) == 3497 and len(inherited) == 3, "predecessor census drift")
    require(("CPP-134-1", 35, 20) in open_keys, "historical next entry was not open in the predecessor")
    closed = extract_batch(result, predecessor, scope, open_keys, set(inherited))

    controls = []
    mutations = {
        "missing_key": lambda r: r["verdicts"].pop(),
        "duplicate_key": lambda r: r["verdicts"].append(copy.deepcopy(r["verdicts"][0])),
        "foreign_key": lambda r: r["verdicts"][0].update(key=["CPP-000-0", 0, 0]),
        "inherited_counted_as_new": lambda r: r["verdicts"][0].update(
            key=list(next(iter(inherited))), id=leaf_id(next(iter(inherited)))),
    }
    for name, mutate in mutations.items():
        broken = copy.deepcopy(result)
        mutate(broken)
        try:
            extract_batch(broken, predecessor, scope, open_keys, set(inherited))
        except (ValueError, KeyError):
            controls.append({"name": name, "rejected": True})
        else:
            raise ValueError(f"malformed batch accepted: {name}")

    by_id = {r["id"]: r for r in ledger["leaves"]}
    for i, key, certificate in closed:
        event_id = f"W/{leaf_id(key)}"
        ledger["events"].append({
            "event_id": event_id, "sequence": len(ledger["events"]) + 1, "type": "close",
            "leaf_id": leaf_id(key), "key": list(key), "report_date": "2026-10-04",
            "research_completed_at": None, "published_commit": W_STAGE["published_commit"],
            "evidence": W_STAGE["source"], "evidence_pointer": f"/verdicts/{i}",
            "certificate_pointer": f"/certificates/{certificate}", "scope_delta": -1,
            "audit": W_STAGE["audit"],
            "evidence_layer": "arbitrary-size paper (theorem C-W) + external Gallai + finite Python; "
                              "independent audit D6; no Lean"})
        by_id[leaf_id(key)].update(status="closed_source_excluded", closed_by=event_id)
    after = open_keys - {k for _, k, _ in closed}
    reconcile(universe, open_keys, after, {k for _, k, _ in closed})
    census = dict(ledger["trend"][-1])
    census.update(stage="W", open_leaves=len(after), closed_leaves=len(universe - after),
                  new_closed=len(closed), open_cases=len({k[0] for k in after}),
                  open_case_geometries=len({k[:2] for k in after}))
    ledger["trend"].append(census)
    require([r["open_leaves"] for r in ledger["trend"]] == [3500, 3499, 3498, 3497, 0], "trend drift")
    require([r["new_closed"] for r in ledger["trend"]] == [0, 1, 1, 1, 3497], "closure trend drift")
    for row in ledger["leaves"]:
        key = tuple(row["key"])
        if key in inherited:
            require(row["closed_by"] == inherited[key], f"inherited closure changed: {key}")
    require(all(r["status"] == "closed_source_excluded" for r in ledger["leaves"]), "open leaf remains")
    ledger.update(version="cw-v1",
                  predecessor={"path": PREDECESSOR, "sha256": digest(encode(predecessor).encode()),
                               "version": "c4"},
                  batch_negative_controls=controls)
    ledger["sources"] = {**ledger["sources"], **sources}
    ledger["coverage"]["branch_status"] = ("C section-1 common-endpoint P3 source branch closed: "
                                           "catalogue empty after W, zero-unary sides excluded by D6")
    ledger["time"]["w_publication_commit"] = W_STAGE["published_commit"]
    ledger["time"]["w_publication_at"] = git("show", "-s", "--format=%aI", W_STAGE["published_commit"])
    return ledger


def outputs(ledger):
    csv_text = io.StringIO()
    writer = csv.writer(csv_text, lineterminator="\n")
    writer.writerow(["stage", "open_leaves", "closed_leaves", "new_closed", "new_leaves",
                     "split_events", "split_net", "reopened", "open_cases", "open_case_geometries"])
    for row in ledger["trend"]:
        writer.writerow(row.values())
    return {"ledger.json": encode(ledger), "trend.csv": csv_text.getvalue()}


def snapshot(ledger):
    return {"schema": 1, "cohort": ledger["cohort"], "unit": ledger["unit"],
            "domain_sha256": ledger["domain_sha256"],
            "observed_at": datetime.now().astimezone().isoformat(), "head": git("rev-parse", "HEAD"),
            "sources": ledger["sources"], "catalogue_leaves": ledger["coverage"]["catalogue_leaves"],
            "ledger_version": ledger.get("version", "c4"),
            "open_leaf_ids": sorted(r["id"] for r in ledger["leaves"] if r["status"] == "open_unreviewed"),
            "leaf_ids": sorted(r["id"] for r in ledger["leaves"]),
            "evidence_limit": "dated ledger census of inherited verdicts; proofs not rerun"}


def compare(before, after):
    for field in ("schema", "cohort", "unit", "domain_sha256", "catalogue_leaves", "leaf_ids"):
        require(before[field] == after[field], f"comparison domain drift: {field}")
    universe = set(before["leaf_ids"])
    require(len(universe) == len(before["leaf_ids"]) == before["catalogue_leaves"], "invalid snapshot universe")
    for sample in (before, after):
        ids = sample["open_leaf_ids"]
        require(len(set(ids)) == len(ids) and set(ids) <= universe, "invalid snapshot open leaves")
    elapsed = (datetime.fromisoformat(after["observed_at"]) - datetime.fromisoformat(before["observed_at"])).total_seconds()
    require(elapsed > 0, "snapshots must have increasing observation times")
    old, new = set(before["open_leaf_ids"]), set(after["open_leaf_ids"])
    closed, reopened = sorted(old - new), sorted(new - old)
    delta = len(new) - len(old)
    require(delta == len(reopened) - len(closed), "snapshot conservation failed")
    return {"before": len(old), "after": len(new), "delta": delta, "closed_ids": closed,
            "reopened_ids": reopened, "elapsed_days": elapsed / 86400,
            "leaves_per_day": delta / (elapsed / 86400),
            "rate_basis": "observation interval, not proof completion times",
            "split_events": 0, "new_leaves": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dry-run", action="store_true", help="build both versions; write nothing")
    mode.add_argument("--snapshot", type=Path, help="fresh path; never overwrite a dated sample")
    mode.add_argument("--compare", nargs=2, type=Path, metavar=("BEFORE", "AFTER"))
    args = parser.parse_args()
    if args.compare:
        print(json.dumps(compare(*(json.loads(p.read_text()) for p in args.compare)), ensure_ascii=False, indent=2))
        return
    predecessor = build()
    ledger = build_cw(predecessor)
    targets = {OUT: outputs(predecessor), CW_OUT: outputs(ledger)}
    if args.check:
        for folder, payloads in targets.items():
            for name, content in payloads.items():
                require((folder / name).read_bytes() == content.encode(), f"ledger differs: {folder / name}")
    elif args.write:
        for name, content in targets[OUT].items():
            require((OUT / name).read_bytes() == content.encode(),
                    f"predecessor ledger would change; refusing: {name}")
        CW_OUT.mkdir(parents=True, exist_ok=True)
        for name, content in targets[CW_OUT].items():
            path = CW_OUT / name
            require(not path.exists() or path.read_bytes() == content.encode(),
                    f"refusing to overwrite a different {path}")
            path.write_text(content)
    elif args.snapshot:
        args.snapshot.parent.mkdir(parents=True, exist_ok=True)
        with args.snapshot.open("x") as destination:
            destination.write(encode(snapshot(ledger)))
    leaves = ledger["leaves"]
    print(json.dumps({"catalogue": len(leaves), "version": ledger["version"],
                      "open": sum(r["status"] == "open_unreviewed" for r in leaves),
                      "closed": sum(r["status"] != "open_unreviewed" for r in leaves),
                      "stage_trend": [r["open_leaves"] for r in ledger["trend"]],
                      "candidate_sha256": {str(f.relative_to(ROOT) / n): digest(c.encode())
                                           for f, p in targets.items() for n, c in p.items()},
                      "global_count": None, "historical_daily_rate": None,
                      "scope_negative_controls": ledger["negative_controls"],
                      "batch_negative_controls": ledger["batch_negative_controls"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
