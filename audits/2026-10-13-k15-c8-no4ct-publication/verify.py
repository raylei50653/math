#!/usr/bin/env python3
"""Check original delivery bytes and additive archive preservation, read-only.

This replaces no original mathematical replay or isolation-state gate. Archived
files can be verified before restore; the original checkers require restore.
"""

import gzip
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical_digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def check():
    imported = json.loads((HERE / "IMPORTED.json").read_text())
    subprocess.run(["git", "merge-base", "--is-ancestor", imported["base"], "HEAD"],
                   cwd=REPO, check=True)
    archive = json.loads((REPO / "audits/ARCHIVE.json").read_text())
    addition = json.loads((HERE / "ARCHIVE_APPEND.json").read_text())
    baseline = json.loads(subprocess.check_output(
        ["git", "show", imported["base"] + ":audits/ARCHIVE.json"], cwd=REPO))
    for group in ("files", "blobs"):
        added = addition["added"][group]
        assert all(archive[group].get(key) == record for key, record in added.items()), group
        previous = baseline[group]
        expected = addition["previous"][group]
        assert len(previous) == expected["count"], group
        assert canonical_digest(previous) == expected["sha256"], group
        assert all(archive[group].get(key) == record for key, record in previous.items()), group
    for record in addition["added"]["blobs"].values():
        raw = (REPO / record["path"]).read_bytes()
        assert len(raw) == record["bytes"] and sha(raw) == record["sha256"], record["path"]
    for name, record in imported["files"].items():
        path = REPO / name
        if path.is_file():
            raw = path.read_bytes()
            assert path.stat().st_mode & 0o777 == record["mode"], name
        else:
            archived = archive["files"][name]
            assert all(archived[key] == record[key] for key in ("bytes", "sha256", "mode")), name
            blob = archive["blobs"][archived["sha256"]]
            raw = gzip.decompress((REPO / blob["path"]).read_bytes())
        assert len(raw) == record["bytes"] and sha(raw) == record["sha256"], name
    expected_paths = set(imported["files"])
    for prefix in imported["sources"]:
        actual = {str(path.relative_to(REPO)) for path in (REPO / prefix).rglob("*")
                  if path.is_file() and "__pycache__" not in path.parts
                  and path.suffix != ".pyc" and path.name not in {"plantri", "plantri_min4_filter"}}
        actual.update(name for name in archive["files"] if name.startswith(prefix + "/"))
        assert actual == {name for name in expected_paths if name.startswith(prefix + "/")}, prefix
    print(json.dumps({"status": "PASS", "original_files": len(expected_paths),
                      "original_bytes_unchanged": True, "old_archive_records_unchanged": True,
                      "archived_paths_added": len(addition["added"]["files"]),
                      "new_Lean_theorem": False}, sort_keys=True))


if __name__ == "__main__":
    check()
