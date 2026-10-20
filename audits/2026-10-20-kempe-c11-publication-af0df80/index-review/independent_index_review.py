#!/usr/bin/env python3
"""Independent index custody and final routing checks; no Git mutation."""
from collections import Counter
from hashlib import sha256
import gzip
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
PUBLICATION = HERE.parent
ROOT = PUBLICATION.parents[1]
BASE = "af0df8081e79b51f8b24e17e01b2bd5572e46a0a"


def digest(data):
    return sha256(data).hexdigest()


def git(*args, input=None):
    return subprocess.check_output(["git", *args], cwd=ROOT, input=input)


def main():
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    source = json.loads((PUBLICATION / "SOURCE_FILES.json").read_text())["files"]
    required = json.loads((PUBLICATION / "required-ignored-inputs.json").read_text())["files"]
    exceptions = json.loads((PUBLICATION / "artifact-exceptions-added.json").read_text())
    whitespace = json.loads((PUBLICATION / "whitespace-preserved.json").read_text())
    assert len(source) == 1509
    assert len(required) == len(set(required)) == 39
    assert len(exceptions) == 7
    assert whitespace["path_count"] == len(whitespace["preserved_paths"]) == 8
    assert whitespace["warning_count"] == len(whitespace["warnings"]) == 29
    indexed = set(git("ls-files", "-z").decode().split("\0")) - {""}
    staged = set(git("diff", "--cached", "--name-only", "-z").decode().split("\0")) - {""}
    index_at_start = git("ls-files", "--stage", "-z")
    unmerged = git("ls-files", "--unmerged", "-z")
    assert not unmerged, "unmerged index entries"
    blob_process = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    )

    def blob(path):
        assert path in indexed, ("missing index dependency", path)
        blob_process.stdin.write((":" + path + "\n").encode())
        blob_process.stdin.flush()
        header = blob_process.stdout.readline().decode().split()
        assert len(header) == 3 and header[1] == "blob", (path, header)
        data = blob_process.stdout.read(int(header[2]))
        assert blob_process.stdout.read(1) == b"\n"
        return data

    dependency_rows = []
    try:
        for path, expected in source.items():
            data = (ROOT / path).read_bytes()
            assert len(data) == expected["bytes"], ("source worktree bytes", path)
            assert digest(data) == expected["sha256"], ("source worktree SHA", path)
            assert blob(path) == data, ("source index bytes", path)
        ignored_result = subprocess.run(
            ["git", "check-ignore", "--no-index", "-z", "--stdin"],
            cwd=ROOT, input=("\0".join(source) + "\0").encode(), capture_output=True,
        )
        assert ignored_result.returncode == 0, ignored_result.stderr.decode()
        ignored = set(ignored_result.stdout.decode().split("\0")) - {""}
        assert ignored == set(required), ("ignored-source whitelist", sorted(ignored ^ set(required)))
        assert set(required) <= set(source) <= indexed

        source_audits = json.loads((PUBLICATION / "BASE.json").read_text())["source_audits"]
        for audit in source_audits:
            inputs_path = audit + "/INPUTS.json"
            inputs_bytes = (ROOT / inputs_path).read_bytes()
            assert blob(inputs_path) == inputs_bytes
            rows = json.loads(inputs_bytes)
            empty = 0
            for row in rows:
                frozen = audit + "/" + row.get("frozen", "frozen/" + row["path"])
                assert frozen in source, ("dependency absent from source seal", frozen)
                data = blob(frozen)
                assert digest(data) == row["sha256"], ("dependency index SHA", frozen)
                assert data == (ROOT / frozen).read_bytes(), ("dependency worktree/index", frozen)
                if "bytes" in row:
                    assert len(data) == row["bytes"], ("dependency index bytes", frozen)
                empty += not data
            dependency_rows.append({"audit": audit, "inputs": len(rows), "empty_inputs": empty,
                                    "index_and_worktree_hashes_match": True})

        policy_path = "tools/generated_artifact_exceptions.json"
        old_policy = json.loads(git("show", BASE + ":" + policy_path))
        new_policy_bytes = blob(policy_path)
        new_policy = json.loads(new_policy_bytes)
        assert new_policy_bytes == (ROOT / policy_path).read_bytes()
        assert {k: v for k, v in old_policy.items() if k != "files"} == {
            k: v for k, v in new_policy.items() if k != "files"}
        old_files, new_files = old_policy["files"], new_policy["files"]
        assert set(old_files) <= set(new_files)
        assert all(new_files[k] == v for k, v in old_files.items()), "existing policy mutated"
        actual_additions = {k: v for k, v in new_files.items() if k not in old_files}
        assert actual_additions == exceptions, "policy additions are not exactly seven sealed entries"
        for path, row in exceptions.items():
            assert source[path]["bytes"] == row["bytes"]
            assert source[path]["sha256"] == row["sha256"]

        integration = {
            "docs/STATUS.md", "docs/c5_kempe_guide.md", "docs/c5_state_guide.md",
            "docs/history/2026-10-20-kempe-c11-progress-publish.md", policy_path,
        }
        publication_prefix = str(PUBLICATION.relative_to(ROOT)) + "/"
        unexpected = staged - set(source) - integration
        assert all(p.startswith(publication_prefix) for p in unexpected), sorted(unexpected)
        assert set(source) <= staged
        assert integration <= staged
        assert not git("diff", "--name-only", "--", *sorted(integration)).strip(), "unstaged integration drift"
        for path in integration:
            assert blob(path) == (ROOT / path).read_bytes(), ("integration differs from index", path)
        for row in whitespace["warnings"]:
            data = blob(row["path"])
            assert len(data) == row["bytes"] and digest(data) == row["sha256"]
    finally:
        blob_process.stdin.close()
        assert blob_process.wait() == 0

    unresolved = []
    for path in PUBLICATION.rglob("*.json"):
        if path == HERE / "summary.json":
            continue
        payload = json.loads(path.read_text())
        if re.search(r"pending|placeholder|\bTODO\b", json.dumps(payload), re.I):
            unresolved.append(str(path.relative_to(PUBLICATION)))
    assert not unresolved, ("unfinished publication metadata", unresolved)

    custody = {
        "status": "PASS", "source_files": len(source),
        "source_bytes": sum(row["bytes"] for row in source.values()),
        "source_empty_files": sum(row["bytes"] == 0 for row in source.values()),
        "worktree_and_index_match_source_sha256": True,
        "required_ignored_inputs": len(required), "exact_ignore_whitelist": True,
        "input_dependencies": dependency_rows, "policy_additions": len(actual_additions),
        "old_policy_entries_unchanged": True, "staged_paths_before_review": len(staged),
        "integration_paths": sorted(integration), "unexpected_staged_paths": [],
        "unresolved_publication_metadata": unresolved,
        "preserved_whitespace_paths": whitespace["preserved_paths"],
        "index_manifest_sha256_before_review": digest(index_at_start),
        "git_read_argv_templates": [
            ["git", "rev-parse", "HEAD"], ["git", "ls-files", "-z"],
            ["git", "diff", "--cached", "--name-only", "-z"],
            ["git", "ls-files", "--stage", "-z"], ["git", "ls-files", "--unmerged", "-z"],
            ["git", "cat-file", "--batch"],
            ["git", "check-ignore", "--no-index", "-z", "--stdin"],
            ["git", "show", BASE + ":" + policy_path],
            ["git", "diff", "--name-only", "--", *sorted(integration)],
        ],
    }
    (HERE / "custody.json").write_text(json.dumps(custody, indent=2, ensure_ascii=False) + "\n")

    command_rows = []
    commands = [
        ("docs", ["python3", "-B", "scripts/check_docs.py"], 0),
        ("docgraph-docs", ["python3", "-B", "tools/docgraph", "--include", "docs/**/*.md", "check"], 0),
        ("docgraph-all", ["python3", "-B", "tools/docgraph", "check"], 1),
        ("artifact-policy", ["python3", "-B", "tools/check_generated_artifacts.py"], 0),
        ("scoped-whitespace", ["git", "diff", "--cached", "--check", "--", ".",
             *(":(exclude)" + path for path in whitespace["preserved_paths"])], 0),
        ("preserved-whitespace", ["git", "diff", "--cached", "--check"], 2),
    ]
    command_failures = []
    for name, argv, expected in commands:
        result = subprocess.run(argv, cwd=ROOT, capture_output=True)
        stdout_name = name + (".stdout.gz" if name == "preserved-whitespace" else ".stdout")
        stored_stdout = gzip.compress(result.stdout, mtime=0) if name == "preserved-whitespace" else result.stdout
        (HERE / stdout_name).write_bytes(stored_stdout)
        (HERE / (name + ".stderr")).write_bytes(result.stderr)
        command_rows.append({
            "name": name, "argv": argv, "cwd": str(ROOT),
            "exit_code": result.returncode, "expected_exit_code": expected,
            "stdout": stdout_name, "stdout_bytes": len(result.stdout),
            "stdout_sha256": digest(result.stdout),
            "stdout_encoding": "gzip" if name == "preserved-whitespace" else "raw",
            "stored_stdout_bytes": len(stored_stdout), "stored_stdout_sha256": digest(stored_stdout),
            "stderr": name + ".stderr", "stderr_bytes": len(result.stderr),
            "stderr_sha256": digest(result.stderr),
        })
        if result.returncode != expected:
            command_failures.append(name)
        if name == "docgraph-all":
            combined = result.stdout.decode() + result.stderr.decode()
            errors = Counter(re.findall(r"^ERROR \[([^\]]+)\]", combined, re.M))
            assert errors == {"duplicate-id": 72}, ("whole-tree diagnostics changed", errors)
            command_rows[-1]["error_kinds"] = dict(errors)
            command_rows[-1]["interpretation"] = "Known archival duplicate IDs retained; formal docs pass reported separately."
        if name == "preserved-whitespace":
            actual = Counter(re.findall(r"^(.*):(\d+): (trailing whitespace\.|new blank line at EOF\.|space before tab in indent\.)$", result.stdout.decode(), re.M))
            expected_warnings = Counter((r["path"], str(r["line"]), r["warning"]) for r in whitespace["warnings"])
            assert actual == expected_warnings, ("whitespace warnings changed", actual - expected_warnings, expected_warnings - actual)
            command_rows[-1]["warning_count"] = sum(actual.values())
            command_rows[-1]["path_count"] = len({row[0] for row in actual})
            command_rows[-1]["interpretation"] = "Exactly the 29 declared warnings in eight sealed evidence/review stdout paths; scoped check is clean."

    assert not command_failures, command_failures
    assert git("ls-files", "--stage", "-z") == index_at_start, "index changed during independent review"
    summary = {
        "schema": "math-publication-independent-index-review-v1",
        "status": "PASS_WITH_DOCUMENTED_SCOPE_LIMITATIONS",
        "baseline_head": BASE,
        "invocation_argv": ["python3", "-B", str(Path(__file__).relative_to(ROOT))],
        "invocation_exit_code": 0,
        "custody": "custody.json", "custody_sha256": digest((HERE / "custody.json").read_bytes()),
        "checks": command_rows, "index_changed_during_review": False,
        "source_evidence_drift": False, "mathematical_closure_claim": False,
        "interpretation": "Independent Git blob review confirms original sealed source, full indexed frozen dependencies including empty files, exact seven policy additions and connected staging scope. Whole-tree archival duplicate IDs and declared original evidence whitespace remain explicitly reported.",
    }
    (HERE / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"status": summary["status"], "source_files": len(source),
                      "source_bytes": custody["source_bytes"], "source_drift": False,
                      "required_ignored_inputs": len(required), "policy_additions": len(exceptions),
                      "input_dependencies": dependency_rows, "checks": len(command_rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
