"""CLI integration tests for the generated-artifact Git-index policy.

Run with ``python -m unittest discover -s tools/tests -v``.
Each test uses a fresh repository so real index entries, modes, and ignore rules
exercise the same boundary as CI without depending on this repository's data.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / "check_generated_artifacts.py"
THRESHOLD = 1_000_000
CONFIG = "tools/generated_artifact_exceptions.json"


class GeneratedArtifactPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        self.git("init", "--quiet")
        self.config({})

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )

    def write(self, path, content, *, stage=True):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content.encode() if isinstance(content, str) else content)
        if stage:
            self.git("add", "--", path)
        return target

    def config(self, files):
        self.write(CONFIG, json.dumps({"version": 1, "files": files}))

    def check(self, *, succeeds):
        result = subprocess.run(
            [sys.executable, str(CHECKER), "--repo", str(self.repo)],
            capture_output=True,
            text=True,
        )
        output = result.stdout + result.stderr
        if succeeds:
            self.assertEqual(result.returncode, 0, output)
        else:
            self.assertNotEqual(result.returncode, 0, output)
        return output

    def frozen_entry(self, content, *, reason="Historical certificate cannot be reproduced."):
        return {
            "kind": "frozen",
            "reason": reason,
            "sha256": hashlib.sha256(content).hexdigest(),
            "bytes": len(content),
        }

    def manifest(self, *, output="artifacts/generated.json", script="generate.py"):
        content = b"x" * THRESHOLD
        self.write(
            "artifacts/MANIFEST.json",
            json.dumps(
                {
                    "files": {
                        output: {
                            "bytes": len(content),
                            "sha256": hashlib.sha256(content).hexdigest(),
                            "script": script,
                        }
                    },
                    "producers": {},
                }
            ),
        )

    def test_small_tracked_json_passes_without_manifest(self):
        self.write("observations.json", b"x" * (THRESHOLD - 1))
        self.check(succeeds=True)

    def test_threshold_is_inclusive(self):
        self.write("observations.json", b"x" * THRESHOLD)
        self.check(succeeds=False)

    def test_all_generated_artifact_extensions_are_guarded(self):
        for extension in (".json", ".jsonl", ".ndjson", ".json5", ".bin"):
            with self.subTest(extension=extension):
                path = "observations" + extension
                self.write(path, b"x" * THRESHOLD)
                output = self.check(succeeds=False)
                self.assertIn(path, output)
                self.git("rm", "--force", "--", path)

    def test_adding_ignore_rule_does_not_excuse_already_tracked_output(self):
        self.write("observations.json", b"x" * THRESHOLD)
        self.write(".gitignore", "/observations.json\n")
        self.check(succeeds=False)

    @unittest.skipUnless(hasattr(os, "symlink"), "requires symlinks")
    def test_symlink_to_large_json_is_not_counted_as_large_content(self):
        self.write("large-target.json", b"x" * THRESHOLD, stage=False)
        os.symlink("large-target.json", self.repo / "reference.json")
        self.git("add", "--", "reference.json")
        self.assertTrue(self.git("ls-files", "--stage", "reference.json").stdout.startswith("120000"))
        self.check(succeeds=True)

    def test_unstaged_growth_does_not_change_small_index_blob(self):
        self.write("observations.json", b"small")
        self.write("observations.json", b"x" * THRESHOLD, stage=False)
        self.check(succeeds=True)

    def test_unstaged_shrink_does_not_hide_large_index_blob(self):
        self.write("observations.json", b"x" * THRESHOLD)
        self.write("observations.json", b"small", stage=False)
        self.check(succeeds=False)

    def test_exact_frozen_exception_passes_but_staged_mutation_fails(self):
        content = b"x" * THRESHOLD
        self.write("certificate.json", content)
        self.config({"certificate.json": self.frozen_entry(content)})
        self.check(succeeds=True)
        self.write("certificate.json", b"y" * THRESHOLD)
        self.check(succeeds=False)

    def test_unstaged_exception_cannot_excuse_large_index_blob(self):
        content = b"x" * THRESHOLD
        self.write("certificate.json", content)
        self.write(
            CONFIG,
            json.dumps({"version": 1, "files": {"certificate.json": self.frozen_entry(content)}}),
            stage=False,
        )
        self.check(succeeds=False)

    def test_frozen_exception_uses_index_hash_despite_unstaged_mutation(self):
        content = b"x" * THRESHOLD
        self.write("certificate.json", content)
        self.config({"certificate.json": self.frozen_entry(content)})
        self.write("certificate.json", b"y" * THRESHOLD, stage=False)
        self.check(succeeds=True)

    def test_frozen_exception_rejects_wrong_recorded_size(self):
        content = b"x" * THRESHOLD
        self.write("certificate.json", content)
        entry = self.frozen_entry(content)
        entry["bytes"] += 1
        self.config({"certificate.json": entry})
        self.check(succeeds=False)

    def test_missing_or_blank_exception_reason_fails(self):
        content = b"x" * THRESHOLD
        self.write("certificate.json", content)
        for reason in (None, "", "   "):
            with self.subTest(reason=reason):
                entry = self.frozen_entry(content)
                if reason is None:
                    del entry["reason"]
                else:
                    entry["reason"] = reason
                self.config({"certificate.json": entry})
                self.check(succeeds=False)

    def test_exception_config_cannot_be_removed_to_disable_guard(self):
        self.git("rm", "--force", "--", CONFIG)
        self.check(succeeds=False)

    def test_policy_top_level_list_is_rejected_without_traceback(self):
        self.write(CONFIG, "[]")
        output = self.check(succeeds=False)
        self.assertNotIn("Traceback", output)

    def test_policy_non_object_exception_is_rejected_without_traceback(self):
        self.write("certificate.json", b"x" * THRESHOLD)
        self.config({"certificate.json": []})
        output = self.check(succeeds=False)
        self.assertNotIn("Traceback", output)

    def test_exception_for_nonexistent_file_is_rejected(self):
        self.config({"missing.json": self.frozen_entry(b"x" * THRESHOLD)})
        self.check(succeeds=False)

    def test_exception_for_file_that_is_no_longer_large_is_rejected(self):
        content = b"small"
        self.write("certificate.json", content)
        self.config({"certificate.json": self.frozen_entry(content)})
        self.check(succeeds=False)

    def test_metadata_exception_requires_tracked_generator(self):
        self.write("catalog.json", b"x" * THRESHOLD)
        self.write("scripts/catalog.py", "# Generates the tracked catalog.\n")
        self.config(
            {
                "catalog.json": {
                    "kind": "metadata",
                    "reason": "Catalog is the compact rebuild index.",
                    "generator": "scripts/catalog.py",
                }
            }
        )
        self.check(succeeds=True)
        self.git("rm", "--cached", "--", "scripts/catalog.py")
        self.check(succeeds=False)

    def test_manifest_rejects_missing_producer(self):
        self.manifest()
        self.write(".gitignore", "/artifacts/generated.json\n")
        self.check(succeeds=False)

    def test_manifest_accepts_repository_relative_adjacent_producer(self):
        self.write("artifacts/probe/generate.py", "# Adjacent standalone producer.\n")
        self.write(".gitignore", "/artifacts/probe/observations.json\n")
        self.manifest(output="artifacts/probe/observations.json", script="artifacts/probe/generate.py")
        self.check(succeeds=True)

    def test_repository_relative_manifest_producer_must_be_tracked(self):
        self.write("artifacts/probe/generate.py", "# Local-only producer.\n", stage=False)
        self.write(".gitignore", "/artifacts/probe/observations.json\n")
        self.manifest(output="artifacts/probe/observations.json", script="artifacts/probe/generate.py")
        self.check(succeeds=False)

    def test_manifest_rejects_noncanonical_and_escaping_producer_paths(self):
        self.write("scripts/generate.py", "# Producer.\n")
        self.write(".gitignore", "/artifacts/generated.json\n")
        for script in (
            "../generate.py",
            "/scripts/generate.py",
            "scripts\\generate.py",
            "scripts/../generate.py",
            "./scripts/generate.py",
        ):
            with self.subTest(script=script):
                self.manifest(script=script)
                self.check(succeeds=False)

    @unittest.skipUnless(hasattr(os, "symlink"), "requires symlinks")
    def test_manifest_rejects_tracked_producer_symlink_to_outside_repository(self):
        with tempfile.TemporaryDirectory() as external:
            external_producer = Path(external) / "generate.py"
            external_producer.write_text("# Producer outside the repository.\n")
            (self.repo / "artifacts/probe").mkdir(parents=True)
            os.symlink(external_producer, self.repo / "artifacts/probe/generate.py")
            self.git("add", "--", "artifacts/probe/generate.py")
            self.write(".gitignore", "/artifacts/probe/observations.json\n")
            self.manifest(output="artifacts/probe/observations.json", script="artifacts/probe/generate.py")
            self.check(succeeds=False)

    def test_unstaged_manifest_deletion_cannot_hide_missing_producer(self):
        self.manifest()
        self.write(".gitignore", "/artifacts/generated.json\n")
        (self.repo / "artifacts/MANIFEST.json").unlink()
        self.check(succeeds=False)

    def test_manifest_top_level_list_is_rejected_without_traceback(self):
        self.write("artifacts/MANIFEST.json", "[]")
        output = self.check(succeeds=False)
        self.assertNotIn("Traceback", output)

    def test_manifest_non_object_entry_is_rejected_without_traceback(self):
        self.write("scripts/generate.py", "# Producer.\n")
        self.write(".gitignore", "/artifacts/generated.json\n")
        self.write("artifacts/MANIFEST.json", json.dumps({"files": {"artifacts/generated.json": []}}))
        output = self.check(succeeds=False)
        self.assertNotIn("Traceback", output)

    def test_manifest_rejects_tracked_output_even_if_current_blob_is_small(self):
        self.write("scripts/generate.py", "# Producer.\n")
        self.write("artifacts/generated.json", b"small")
        self.write(".gitignore", "/artifacts/generated.json\n")
        self.manifest()
        self.check(succeeds=False)

    def test_manifest_rejects_output_without_ignore_rule(self):
        self.write("scripts/generate.py", "# Producer.\n")
        self.manifest()
        self.check(succeeds=False)

    def test_untracked_ignore_rule_cannot_certify_indexed_manifest(self):
        self.write("scripts/generate.py", "# Producer.\n")
        self.manifest()
        self.write(".gitignore", "/artifacts/generated.json\n", stage=False)
        self.check(succeeds=False)

    def test_unstaged_ignore_rule_cannot_certify_indexed_manifest(self):
        self.write("scripts/generate.py", "# Producer.\n")
        self.manifest()
        self.write(".gitignore", "")
        self.write(".gitignore", "/artifacts/generated.json\n", stage=False)
        self.check(succeeds=False)

    def test_indexed_ignore_rule_survives_unstaged_change_and_deletion(self):
        self.write("scripts/generate.py", "# Producer.\n")
        self.manifest()
        self.write(".gitignore", "/artifacts/generated.json\n")
        self.write(".gitignore", "", stage=False)
        self.check(succeeds=True)
        (self.repo / ".gitignore").unlink()
        self.check(succeeds=True)

    def test_manifest_rejects_ignore_rule_only_in_local_git_exclude(self):
        self.write("scripts/generate.py", "# Producer.\n")
        self.write(".git/info/exclude", "/artifacts/generated.json\n", stage=False)
        self.manifest()
        self.check(succeeds=False)

    def test_valid_manifest_allows_ignored_untracked_generated_output(self):
        self.write("scripts/generate.py", "# Producer.\n")
        self.write(".gitignore", "/artifacts/generated.json\n")
        self.manifest()
        self.write("artifacts/generated.json", b"x" * THRESHOLD, stage=False)
        self.check(succeeds=True)

    def test_valid_manifest_allows_output_absent_from_fresh_checkout(self):
        self.write("scripts/generate.py", "# Producer.\n")
        self.write(".gitignore", "/artifacts/generated.json\n")
        self.manifest()
        self.check(succeeds=True)


if __name__ == "__main__":
    unittest.main()
