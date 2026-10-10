#!/usr/bin/env python3
"""Seal the supervision once, after scoped adoption and final checks."""
import datetime
import difflib
import importlib.util
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("supervision_review", OUT / "review.py")
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

before = json.loads((OUT / "inputs-before.json").read_text())
incoming = json.loads((OUT / "incoming-audits.json").read_text())
for name, root in r.WORKERS.items():
    assert r.inventory(name, root) == before["workers"][name], (name, "worker drift")
for name, state in incoming.items():
    assert r.inventory(name, r.ROOT / f"audits/2026-10-10-n45-{name}") == state, (name, "audit drift")
assert r.git("rev-parse", "HEAD").decode().strip() == r.BASE

prior_texts = json.loads((OUT / "shared-before.json").read_text())
current_texts = {rel: (r.ROOT / rel).read_text() for rel in prior_texts}
changed = {rel for rel in prior_texts if prior_texts[rel] != current_texts[rel]}
expected_changes = {"docs/c5_excess_two_nonadjacent_unit_core45.md", "docs/c5_kempe_guide.md", "docs/STATUS.md",
                    "docs/c5_phase_b_common_lemmas.md", "artifacts/c5_excess_two_e4/REPORT.md",
                    "docs/history/2026-10-09-n45-u-long-short-pair-tasks.md"}
assert changed == expected_changes, changed
r.put("shared-after.json", current_texts)
diff = "".join("".join(difflib.unified_diff(prior_texts[rel].splitlines(True), current_texts[rel].splitlines(True),
                                        fromfile="before/" + rel, tofile="after/" + rel)) for rel in sorted(changed))
r.put("management.diff", diff.encode())

commands = {p.name.removesuffix(".command.json"): json.loads(p.read_text()) for p in sorted((OUT / "logs").glob("*.command.json"))}
for label, record in commands.items():
    expected = 2 if label.startswith("pc-negative-") or label == "pc-valid-missing-LP" else 0
    if label in ("baseline-docs", "integration-whole-docgraph"):
        expected = 1
    assert record["actual_exit"] == expected, (label, record)
for name in ("pg", "pr", "pc"):
    assert (OUT / f"logs/{name}-normal.stdout.log").read_bytes() == (OUT / f"logs/{name}-seed17.stdout.log").read_bytes()
assert (OUT / "logs/pca-independent-normal.stdout.log").read_bytes() == (OUT / "logs/pca-independent-seed17.stdout.log").read_bytes()
for required in ("integration-formal-docs", "integration-check-docs", "integration-whole-docgraph", "integration-diff"):
    assert required in commands

authority = "docs/c5_excess_two_nonadjacent_unit_core45.md"
authority_hash = r.sha(r.ROOT / authority)
history = r.ROOT / "docs/history/2026-10-10-n45-lp-adoption.md"
assert "SHA256：" + authority_hash in history.read_text(), "next task authority hash drift"
checks = {"BASE": r.BASE, "commands": commands, "worker_payloads_and_original_input_mtimes_unchanged": True,
          "incoming_audit_payloads_and_mtimes_unchanged": True, "changed_shared_files": sorted(changed),
          "new_authority_sha256": authority_hash, "new_task_history_sha256": r.sha(history),
          "next_task": "N45-U-SS prepared; not started", "publication": "no commit/push/PR/external messages",
          "docs_status": {"current_check_docs": "PASS", "formal_docs_DocGraph": "PASS",
                          "fresh_BASE_check_docs": "FAIL: two historical missing files", "whole_worktree_DocGraph": "FAIL: 62 duplicate IDs"},
          "not_run": ["lake build/axioms: no Lean change or new formalization claim", "upstream large enumeration/classification", "U1-U4 replay", "remote CI"]}
r.put("integration-checks.json", checks)

local_links = []
for p in (OUT / "REPORT.md", history):
    text = p.read_text()
    assert text.endswith("\n") and all(line.rstrip() == line for line in text.splitlines()), p
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith(("https://", "http://")):
            continue
        path = target.split("#", 1)[0]
        if path:
            assert (p.parent / path).is_file(), (p, target)
            local_links.append({"source": str(p.relative_to(r.ROOT)), "target": target})
for p in OUT.iterdir():
    if p.is_file() and p.suffix in (".py", ".md", ".json"):
        text = p.read_text()
        assert text.endswith("\n") and all(line.rstrip() == line for line in text.splitlines()), p
        if p.suffix == ".json":
            json.loads(text)
r.put("output-validation.json", {"new_report_history_whitespace": "PASS", "own_json_parse": "PASS",
                                  "new_report_history_local_links": local_links, "next_task_authority_hash": "PASS"})
decisions = {"closure_scope": "N45-U-LP only, under all N45/PA premises and explicit BASE / external Gallai trust",
             "LP_status": "CLOSED by arbitrary-size paper; no new Lean",
             "PG": "six claims accepted with abstract-only controls / necessary profiles boundary",
             "PR_relation_lemmas": "five accepted under separate premises; ENDPOINT retains all owner-root neighbors and complete degree4",
             "PC": "scoped implementation, fixed finite delivery and observed fail-closed paths accepted",
             "PC_generic_soundness": "not established", "LP_source_control": "not triggered", "general_N2_E": "OPEN",
             "next_residual": "N45-U-SS, not started", "propagation_stop": "L2",
             "paper_audit_judgment_sha256": incoming["pa"]["files"]["independent-judgment.json"]["sha256"],
             "PG_audit_judgment_sha256": incoming["pga"]["files"]["independent-judgment.json"]["sha256"],
             "PC_audit_judgment_sha256": incoming["pca"]["files"]["independent-judgment.json"]["sha256"]}
r.put("acceptance.json", decisions)

files = sorted(p for p in OUT.rglob("*") if p.is_file() and p.name not in ("MANIFEST.sha256", "delivery.json"))
assert not any("__pycache__" in p.parts for p in files), "remove only this supervision's unsealed bytecode cache first"
manifest = "".join(r.sha(p) + "  " + p.relative_to(OUT).as_posix() + "\n" for p in files).encode()
r.put("MANIFEST.sha256", manifest)
receipt = {"task": "N45-P-supervision", "BASE": r.BASE, "sealed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "manifest_payload_count": len(files), "manifest_sha256": r.sha(OUT / "MANIFEST.sha256"),
           "manifest_exclusions": ["MANIFEST.sha256", "delivery.json"], "report_sha256": r.sha(OUT / "REPORT.md"),
           "acceptance_sha256": r.sha(OUT / "acceptance.json"), "integration_checks_sha256": r.sha(OUT / "integration-checks.json"),
           "new_authority_sha256": authority_hash, "next_task_history_sha256": r.sha(history),
           "worker_manifests": {n: q["manifest_entries"] for n, q in before["workers"].items()},
           "independent_audit_manifests": {n: q["manifest_entries"] for n, q in incoming.items()},
           "commands_logged": len(commands), "current_git_status": r.git("status", "--short").decode(),
           "new_untracked_files_written_scope": "own supervision and three independent audit directories; next-task history",
           "shared_changes": sorted(changed), "remaining_OPEN": ["N45-U-SS", "S LOW/HIGH/long", "original55/other cores", "no45/54 source", "generalN2/E", "epsilon>=3"],
           "publication": "no commit/push/PR/external message", "parent_scope": "OPEN", "propagation_stop": "L2"}
r.put("delivery.json", receipt)
state = r.inventory("supervision", OUT)
assert state["manifest_entries"] == len(files)
print(json.dumps({"sealed": True, "payload_files": len(files), "commands": len(commands), "LP_status": "CLOSED within scope",
                  "general_N2_E": "OPEN", "new_authority_sha256": authority_hash, "next_task_started": False,
                  "manifest_sha256": receipt["manifest_sha256"]}, sort_keys=True))
