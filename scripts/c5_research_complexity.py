#!/usr/bin/env python3
"""Measure a curated C5 claim inventory, separately from docs and Lean imports.

Standard library only. Default generation writes the pilot's JSON/CSV/HTML;
--check is read-only and compares deterministic outputs. This validates the
inventory and its source anchors, not the mathematics or Lean elaboration.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from collections import Counter
from functools import lru_cache
from itertools import combinations_with_replacement
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "artifacts/c5_research_complexity"
sys.path.insert(0, str(ROOT))
from tools.docgraph.parser import parse_repo
from tools.docgraph.validate import validate


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_text(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def source_baseline() -> str:
    config = json.loads((BASE / "baseline.json").read_text())
    baseline = config["source_baseline_head"]
    if config.get("schema_version") != 1 or not re.fullmatch(r"[0-9a-f]{40}", baseline):
        raise ValueError("invalid source baseline configuration")
    if git("rev-parse", f"{baseline}^{{commit}}") != baseline:
        raise ValueError("source baseline does not identify the recorded commit")
    return baseline


def graph_metrics(deps: dict[str, list[str]]) -> dict:
    """A -> prerequisite; rank is zero for leaves in this selected graph."""
    if any(p not in deps for ps in deps.values() for p in ps):
        raise ValueError("dependency refers to a missing node")
    incoming = {n: [] for n in deps}
    for n, ps in deps.items():
        if len(ps) != len(set(ps)):
            raise ValueError(f"duplicate dependency: {n}")
        for p in ps:
            incoming[p].append(n)
    visiting = set()

    @lru_cache(None)
    def rank(n):
        if n in visiting:
            raise ValueError(f"dependency cycle at {n}")
        visiting.add(n)
        result = 1 + max((rank(p) for p in deps[n]), default=-1)
        visiting.remove(n)
        return result

    def closure(n, adjacency):
        seen, pending = set(), list(adjacency[n])
        while pending:
            p = pending.pop()
            if p not in seen:
                seen.add(p)
                pending.extend(adjacency[p])
        return sorted(seen)

    ranks = {n: rank(n) for n in sorted(deps)}
    per_node = {
        n: {"rank": ranks[n], "prerequisites": sorted(deps[n]),
            "consumers": sorted(incoming[n]),
            "ancestor_ids": closure(n, deps),
            "descendant_ids": closure(n, incoming)}
        for n in sorted(deps)
    }
    return {"nodes": len(deps), "edges": sum(map(len, deps.values())),
            "max_rank": max(ranks.values(), default=0),
            "rank_width": dict(sorted(Counter(ranks.values()).items())),
            "per_node": per_node}


def source_refs(value):
    if isinstance(value, dict):
        for k, v in value.items():
            if k == "source_refs":
                yield from v
            else:
                yield from source_refs(v)
    elif isinstance(value, list):
        for item in value:
            yield from source_refs(item)


def validate_sources(inventories: list[dict]) -> list[dict]:
    sources = {}
    for ref in source_refs(inventories):
        path = (ROOT / ref["path"]).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError(f"invalid source path: {ref['path']}")
        lines = path.read_text().splitlines()
        lo, hi = ref["line"], ref.get("end_line", ref["line"])
        if not isinstance(lo, int) or not isinstance(hi, int) or not 1 <= lo <= hi <= len(lines):
            raise ValueError(f"invalid source lines: {ref}")
        quote = ref.get("quote", "")
        if not quote.strip():
            raise ValueError(f"empty source quote: {ref}")
        if " ".join(quote.split()) not in " ".join("\n".join(lines[lo - 1:hi]).split()):
            raise ValueError(f"source quote mismatch: {ref['path']}:{lo}-{hi}: {quote}")
        sources[ref["path"]] = {"path": ref["path"], "sha256": digest(path)}
    return [sources[p] for p in sorted(sources)]


def validate_inventory(inventories: list[dict]) -> tuple[dict, dict]:
    claims, contracts, groups_seen = {}, {}, set()
    for inventory in inventories:
        if inventory.get("schema_version") != 1:
            raise ValueError("unsupported input schema")
        family = inventory["family"]
        for contract in inventory["contracts"]:
            cid = contract["id"]
            if cid in contracts or not contract.get("source_refs"):
                raise ValueError(f"duplicate or unanchored contract: {cid}")
            if not all(contract.get("scope", {}).get(k) for k in
                       ("source_generality", "observation", "behavior")):
                raise ValueError(f"missing abstraction scope: {cid}")
            contracts[cid] = {**contract, "family": family}
        for claim in inventory["claims"]:
            cid = claim["id"]
            if cid in claims or not claim.get("source_refs"):
                raise ValueError(f"duplicate or unanchored claim: {cid}")
            if claim["status"] not in {"established", "open", "counterexample"}:
                raise ValueError(f"invalid claim status: {cid}")
            if claim["role"] not in {"shared_lemma", "branch_result", "aggregate_result", "instance_result"}:
                raise ValueError(f"invalid claim role: {cid}")
            claims[cid] = {**claim, "family": family}
        for group in inventory.get("branch_groups", []):
            if group["id"] in groups_seen:
                raise ValueError(f"duplicate group ID: {group['id']}")
            groups_seen.add(group["id"])
            if group.get("group_kind") not in {"inventory_bucket", "branch_partition", "peer_comparison"}:
                raise ValueError(f"missing comparison kind: {group['id']}")
            ids = group["members"]
            if not ids or len(ids) != len(set(ids)):
                raise ValueError(f"empty or duplicated peer group: {group['id']}")
            local_ids = {c["id"] for c in inventory["claims"]}
            if any(cid not in local_ids for cid in ids):
                raise ValueError(f"peer group contains nonlocal claim: {group['id']}")
        for comparison in inventory.get("comparisons", []):
            if any(cid not in {c["id"] for c in inventory["claims"]} for cid in comparison["members"]):
                raise ValueError(f"comparison contains nonlocal claim: {comparison['id']}")
    for claim in claims.values():
        if claim["contract_id"] not in contracts:
            raise ValueError(f"missing contract for {claim['id']}")
        if claims[claim["id"]]["family"] != contracts[claim["contract_id"]]["family"]:
            raise ValueError(f"cross-family contract for {claim['id']}")
        pg = claim.get("peer_group")
        if pg:
            matching = [g for inv in inventories for g in inv.get("branch_groups", []) if g["id"] == pg]
            if len(matching) != 1 or claim["id"] not in matching[0]["members"]:
                raise ValueError(f"invalid peer group membership for {claim['id']}: {pg}")
    for inventory in inventories:
        local_ids = {c["id"] for c in inventory["claims"]}
        for candidate in inventory.get("abstraction_candidates", []):
            if not candidate.get("claim_ids") or any(cid not in local_ids for cid in candidate["claim_ids"]):
                raise ValueError(f"candidate contains missing/nonlocal claim: {candidate['id']}")
            if candidate["kind"] not in {"existing_interface_adoption", "new_theorem_required"}:
                raise ValueError(f"invalid candidate kind: {candidate['id']}")
            for obligation in candidate.get("adapter_obligations", []):
                if obligation["status"] not in {"established", "open", "contract_specific"}:
                    raise ValueError(f"invalid adapter obligation status: {candidate['id']}")
    graph_metrics({cid: c["dependencies"] for cid, c in claims.items()})
    return claims, contracts


def lean_code(text: str) -> str:
    """Remove nested comments and string contents, preserving source positions."""
    out, i, level, string = [], 0, 0, False
    while i < len(text):
        if level:
            if text.startswith("/-", i):
                level += 1
                out.extend("  ")
                i += 2
            elif text.startswith("-/", i):
                level -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif string:
            if text[i] == "\\" and i + 1 < len(text):
                out.extend("\n" if x == "\n" else " " for x in text[i:i + 2])
                i += 2
            else:
                if text[i] == '"':
                    string = False
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif text.startswith("/-", i):
            level = 1
            out.extend("  ")
            i += 2
        elif text.startswith("--", i):
            end = text.find("\n", i)
            if end < 0:
                end = len(text)
            out.extend(" " * (end - i))
            i = end
        elif text[i] == '"':
            string = True
            out.append(" ")
            i += 1
        else:
            out.append(text[i])
            i += 1
    if level or string:
        raise ValueError("unclosed Lean comment/string in inventory scan")
    return "".join(out)


DECL = re.compile(r"^(?:\s*@\[[^\n]*?\]\s*)*(?:\s*(?:private|protected|noncomputable|partial|unsafe)\s+)*"
                  r"\s*(theorem|lemma|def|abbrev|structure|inductive|instance)\b", re.M)


def repository_metrics(baseline_head: str) -> dict:
    nodes, diagnostics = parse_repo(ROOT, ["docs/**/*.md"])
    graph, diagnostics = validate(nodes, diagnostics)
    errors = [str(d) for d in diagnostics if d.level == "error"]
    if errors:
        raise ValueError("formal-docs DocGraph invalid: " + "; ".join(errors))
    dg = graph_metrics({cid: graph.prerequisites(cid) for cid in graph.nodes})
    for cid, row in dg["per_node"].items():
        row["path"] = graph.nodes[cid].path
    doc_paths = git("ls-tree", "-r", "--name-only", baseline_head, "--", "docs").splitlines()
    top_md = [p for p in doc_paths if p.endswith(".md") and p.count("/") == 1]
    dg.update(unit="document", coverage_denominator="top-level docs Markdown tracked at source baseline",
              tracked_top_level_docs=len(top_md),
              metadata_top_level_docs=sum(n.path in top_md for n in nodes),
              relation_counts=dict(sorted(Counter(e.type for e in graph.edges).items())),
              limitations=["Only declared metadata; no inference from Markdown links.",
                           "Document dependencies are not a theorem proof DAG."])
    buckets = {k: {"modules": 0, "declarations": Counter()} for k in
               ("ordinary_source", "generated", "audit")}
    modules = {}
    for path in sorted((ROOT / "Math").glob("*.lean")):
        name = path.stem
        bucket = "audit" if name.endswith("Audit") else "generated" if "Generated" in name else "ordinary_source"
        code = lean_code(path.read_text())
        counts = Counter(m[1] for m in DECL.finditer(code))
        buckets[bucket]["modules"] += 1
        buckets[bucket]["declarations"].update(counts)
        if bucket == "ordinary_source":
            modules[name] = {"path": str(path.relative_to(ROOT)), "declarations": dict(sorted(counts.items())),
                             "imports": re.findall(r"^\s*import\s+Math\.([\w]+)\b", code, re.M)}
    imports = {n: sorted(set(p for p in m["imports"] if p in modules)) for n, m in modules.items()}
    lg = graph_metrics(imports)
    for n, m in modules.items():
        lg["per_node"][n].update(m)
    lg.update(unit="module", buckets={k: {"modules": v["modules"],
                                          "declarations": dict(sorted(v["declarations"].items()))}
                                      for k, v in buckets.items()},
              limitations=["Source declaration scan, not an elaborated Lean environment.",
                           "Audit/Generated consumers and Math.lean are outside this import graph.",
                           "Module rank is not abstraction level or theorem proof depth.",
                           "Ordinary-source bucket may contain finite proofs and helpers; no axiom audit was run."])
    # Hash the exact source boundary of the two automatically scanned inventories.
    automatic_sources = {str(p.relative_to(ROOT)): digest(p) for p in
                         sorted((ROOT / "Math").glob("*.lean"))}
    automatic_sources.update({n.path: digest(ROOT / n.path) for n in nodes})
    return {"document_graph": dg, "lean_import_graph": lg,
            "automatic_source_sha256": dict(sorted(automatic_sources.items()))}


def calibrations(inventories: list[dict]) -> dict:
    nm = next(i for i in inventories if i["family"] == "no_mixed")
    # This checks the stated comparison unit, not source realizability.
    branches = [c for c in nm["claims"] if c["role"] == "branch_result"]
    if len(branches) != 15:
        raise ValueError("No-mixed calibration must contain 15 branch identities")
    pairs = [tuple(c["branch"]["sides"]) for c in branches]
    if set(pairs) != set(combinations_with_replacement("ABCDE", 2)) or len(set(pairs)) != 15:
        raise ValueError("No-mixed branch identity partition is incomplete or duplicated")
    lower_bounds = dict(zip("ABCDE", (2, 2, 3, 4, 3)))
    classification = Counter()
    for claim in branches:
        b = claim["branch"]
        lower = [lower_bounds[s] for s in b["sides"]]
        if b["side_lower_bounds"] != lower or b["lower_bound_sum"] != sum(lower) or b["total_budget"] != 5:
            raise ValueError(f"No-mixed side arithmetic mismatch: {claim['id']}")
        expected = "source_excluded" if sum(lower) > 5 else "specified_two_row_separation"
        if b["classification"] != expected:
            raise ValueError(f"No-mixed branch classification mismatch: {claim['id']}")
        classification[expected] += 1
    result = {"no_mixed_branch_identities": len(branches),
              "no_mixed_outcome_counts": dict(sorted(classification.items()))}
    cr = next(i for i in inventories if i["family"] == "common_repair")
    public_group = next(g for g in cr["branch_groups"] if g["id"] == "CR.GROUP.abstract_public_declarations")
    code = lean_code((ROOT / "Math/CommonRepair.lean").read_text())
    declarations = {}
    for match in DECL.finditer(code):
        if match[1] in {"theorem", "lemma"}:
            name = re.match(r"\s+([^\s(:]+)", code[match.end():])[1]
            declarations[name] = code.count("\n", 0, match.end()) + 1
    if {cid.rsplit(".", 1)[-1] for cid in public_group["members"]} != set(declarations):
        raise ValueError("CommonRepair public-declaration inventory is incomplete or inconsistent")
    cr_claims = {c["id"]: c for c in cr["claims"]}
    for cid in public_group["members"]:
        line = declarations[cid.rsplit(".", 1)[-1]]
        if not any(r["path"] == "Math/CommonRepair.lean" and r["line"] <= line <= r.get("end_line", r["line"])
                   for r in cr_claims[cid]["source_refs"]):
            raise ValueError(f"CommonRepair declaration anchor does not cover signature: {cid}")
    result["common_repair_public_declarations"] = len(declarations)
    if "obligation_summary" in cr:
        s = cr["obligation_summary"]
        a, b = s["exact_witness_instances_per_core"], s["cover_instances_per_core"]
        if a + b != s["concrete_wc_obligations_per_core"]:
            raise ValueError("W/C concrete obligation arithmetic does not reconcile")
        if (a + b) * s["named_core_instances"] != s["concrete_wc_obligations_total"]:
            raise ValueError("W/C total obligation arithmetic does not reconcile")
        result["common_repair_obligations"] = s
    return result


def collect(input_dir: Path) -> dict:
    baseline_head = source_baseline()
    files = sorted(input_dir.glob("*.json"))
    inventories = [json.loads(p.read_text()) for p in files]
    if {i["family"] for i in inventories} != {"no_mixed", "common_repair", "n45"} or len(files) != 3:
        raise ValueError("expected exactly no_mixed/common_repair/n45 inputs")
    claims, contracts = validate_inventory(inventories)
    sources = validate_sources(inventories)
    metric = graph_metrics({cid: c["dependencies"] for cid, c in claims.items()})
    families = []
    groups = []
    comparisons = []
    candidates = []
    for inventory in inventories:
        family = inventory["family"]
        local = {c["id"]: c["dependencies"] for c in inventory["claims"]}
        fm = graph_metrics(local)
        families.append({"family": family, "claims": fm["nodes"], "dependency_edges": fm["edges"],
                         "max_selected_rank": fm["max_rank"], "rank_width": fm["rank_width"],
                         "roles": dict(sorted(Counter(c["role"] for c in inventory["claims"]).items())),
                         "statuses": dict(sorted(Counter(c["status"] for c in inventory["claims"]).items()))})
        for group in inventory.get("branch_groups", []):
            group = {**group, "family": family, "width": len(group["members"])}
            group["rank_width"] = dict(sorted(Counter(metric["per_node"][cid]["rank"] for cid in group["members"]).items()))
            group["status_width"] = dict(sorted(Counter(claims[cid]["status"] for cid in group["members"]).items()))
            groups.append(group)
        comparisons.extend({**c, "family": family} for c in inventory.get("comparisons", []))
        candidates.extend({**c, "family": family} for c in inventory.get("abstraction_candidates", []))
    skeletons = {}
    for cid, claim in claims.items():
        if claim.get("proof_skeleton"):
            skeletons.setdefault((claim["family"], claim["proof_skeleton"]), []).append(cid)
    repeats = [{"family": f, "skeleton": s, "claim_ids": sorted(ids), "claims": len(ids),
                "roles": dict(sorted(Counter(claims[cid]["role"] for cid in ids).items())),
                "independent_proof_repetition": "not_measured"}
               for (f, s), ids in sorted(skeletons.items()) if len(ids) > 1]
    for cid, claim in claims.items():
        gm = metric["per_node"][cid]
        claim["metrics"] = {"selected_rank": gm["rank"], "direct_prerequisites": len(gm["prerequisites"]),
                            "transitive_prerequisites": len(gm["ancestor_ids"]),
                            "direct_consumers": len(gm["consumers"]),
                            "transitive_consumers": len(gm["descendant_ids"])}
    return {"schema_version": 1, "baseline_head": baseline_head,
            "baseline_sha256": digest(BASE / "baseline.json"),
            "collector_sha256": digest(Path(__file__)),
            "input_sha256": {p.name: digest(p) for p in files},
            "source_files": sources, "contracts": [contracts[c] for c in sorted(contracts)],
            "claims": [claims[c] for c in sorted(claims)], "families": families,
            "peer_groups": groups, "comparisons": comparisons, "abstraction_candidates": candidates,
            "repeated_skeleton_groups": repeats, "calibrations": calibrations(inventories),
            "selected_claim_graph": metric, "repository": repository_metrics(baseline_head),
            "limitations": [
                "Selected claim DAG is curated and incomplete; rank and reuse are local to this inventory.",
                "Branches, hypotheses, minimal repairs, declarations, documents, and modules use different counting units.",
                "No total complexity score or numerical abstraction level is assigned.",
                "Source anchors and arithmetic are checked; mathematical proofs and axiom audits are inherited.",
                "Proof-skeleton labels identify analytic similarity, not logical equivalence.",
                "Same original graph, named/ordered contacts, actual attachments and one shared color frame are retained.",
                "Boundary dependencies remain explicit; zero local consumers does not prove no research consumers.",
            ]}


def claim_csv(snapshot: dict) -> str:
    out = io.StringIO(newline="")
    fields = ["id", "family", "label", "role", "status", "contract_id", "peer_group",
              "proof_skeleton", "selected_rank", "direct_prerequisites", "transitive_prerequisites",
              "direct_consumers", "transitive_consumers", "source_generality", "observation", "behavior",
              "boundary_dependencies", "source_refs"]
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    contracts = {c["id"]: c for c in snapshot["contracts"]}
    for claim in snapshot["claims"]:
        row = {k: claim.get(k, "") for k in fields[:8]}
        row.update(claim["metrics"])
        row.update(contracts[claim["contract_id"]]["scope"])
        row["boundary_dependencies"] = json.dumps(claim.get("boundary_dependencies", []), ensure_ascii=False)
        row["source_refs"] = "; ".join(f"{r['path']}:{r['line']}" for r in claim["source_refs"])
        writer.writerow(row)
    return out.getvalue()


def peer_csv(snapshot: dict) -> str:
    out = io.StringIO(newline="")
    fields = ["id", "family", "label", "group_kind", "unit", "width", "normalization", "members"]
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for group in snapshot["peer_groups"]:
        row = {k: group[k] for k in fields[:-1]}
        row["members"] = ";".join(group["members"])
        writer.writerow(row)
    return out.getvalue()


def outputs(snapshot: dict) -> dict[str, str]:
    template = (BASE / "dashboard.template.html").read_text()
    # Embedded payload works when opened as a local file; no network or fetch.
    payload = json.dumps(snapshot, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    payload = payload.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    if template.count("__PAYLOAD__") != 1:
        raise ValueError("dashboard template must have exactly one payload placeholder")
    return {"metrics.json": json_text(snapshot), "claims.csv": claim_csv(snapshot),
            "peer_groups.csv": peer_csv(snapshot), "dashboard.html": template.replace("__PAYLOAD__", payload)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="read-only deterministic comparison")
    parser.add_argument("--input-dir", type=Path, default=BASE / "inputs")
    parser.add_argument("--output-dir", type=Path, default=BASE)
    args = parser.parse_args()
    try:
        snapshot = collect(args.input_dir)
        generated = outputs(snapshot)
        if args.check:
            for name, content in generated.items():
                path = args.output_dir / name
                if not path.exists() or path.read_bytes() != content.encode("utf-8"):
                    raise ValueError(f"output missing or stale: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
        else:
            args.output_dir.mkdir(parents=True, exist_ok=True)
            for name, content in generated.items():
                (args.output_dir / name).write_text(content)
        print(f"{'CHECK' if args.check else 'GENERATED'}: {len(snapshot['claims'])} selected claim records; "
              f"{len(snapshot['peer_groups'])} comparison/inventory groups; source anchors and selected DAG valid")
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
