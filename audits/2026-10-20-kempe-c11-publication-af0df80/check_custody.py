#!/usr/bin/env python3
"""Check the published original source bytes in both worktree and Git index."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    files = json.loads((HERE / "SOURCE_FILES.json").read_text())["files"]
    indexed = set(subprocess.check_output(
        ["git", "-C", str(ROOT), "ls-files", "-z"]
    ).decode().split("\0"))
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    )
    try:
        for path, expected in files.items():
            assert path in indexed, ("source missing from index", path)
            current = (ROOT / path).read_bytes()
            assert len(current) == expected["bytes"], ("worktree size", path)
            assert sha256(current).hexdigest() == expected["sha256"], ("worktree SHA", path)
            process.stdin.write((":" + path + "\n").encode())
            process.stdin.flush()
            header = process.stdout.readline().decode().split()
            assert len(header) == 3 and header[1] == "blob", ("index object", path, header)
            staged = process.stdout.read(int(header[2]))
            assert process.stdout.read(1) == b"\n"
            assert staged == current, ("index differs from sealed source", path)
    finally:
        process.stdin.close()
        assert process.wait() == 0
    required = json.loads((HERE / "required-ignored-inputs.json").read_text())["files"]
    assert set(required) <= set(files)
    assert set(required) <= indexed
    additions = json.loads((HERE / "artifact-exceptions-added.json").read_text())
    policy = json.loads(subprocess.check_output(
        ["git", "-C", str(ROOT), "show", ":tools/generated_artifact_exceptions.json"]
    ))["files"]
    for path, record in additions.items():
        assert policy[path] == record, ("staged policy exception drift", path)
    print(json.dumps({
        "status": "PASS", "source_files": len(files),
        "source_bytes": sum(r["bytes"] for r in files.values()),
        "required_ignored_inputs": len(required),
        "frozen_policy_additions": len(additions),
        "worktree_and_index_match_original_source_SHA256": True,
        "mathematical_closure_claim": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
