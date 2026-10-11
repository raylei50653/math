#!/usr/bin/env python3
"""Isolated custody I/O controls; no actual audit seal/prerequisite claim."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile


def main():
    audit = Path(__file__).resolve().parents[2]
    ns = runpy.run_path(str(audit / "verify.py"), run_name="custody_review_probe")
    scope = ns["main"].__globals__
    results = []
    original_argv = sys.argv[:]
    with tempfile.TemporaryDirectory(prefix="br-sd-1g-custody-review-") as directory:
        isolated = Path(directory)
        scope["AUDIT"] = isolated
        # These controls exercise manifest I/O, not real source prerequisites.
        scope["prerequisites"] = lambda: (31, 313, 1, 1)
        payload = isolated / "payload.txt"
        payload.write_bytes(b"review payload\n")
        def invoke(arguments, expected=None):
            sys.argv = ["verify.py", *arguments]
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    ns["main"]()
            except Exception as error:
                if expected is None or not isinstance(error, expected):
                    raise
                return {"caught": type(error).__name__, "message": str(error)}
            if expected is not None:
                raise AssertionError("expected rejection did not occur")
            return {"passed": True}
        results.append({"control": "exclusive first seal", **invoke(["--seal"])})
        seal_bytes = (isolated / "SEAL.json").read_bytes()
        results.append({"control": "second seal cannot overwrite", **invoke(["--seal"], FileExistsError)})
        assert (isolated / "SEAL.json").read_bytes() == seal_bytes
        results.append({"control": "unchanged exact inventory", **invoke(["--check"])})
        payload.write_bytes(b"changed bytes\n")
        results.append({"control": "payload byte change", **invoke(["--check"], ValueError)})
        payload.write_bytes(b"review payload\n")
        added = isolated / "extra.txt"
        added.write_bytes(b"extra\n")
        results.append({"control": "unlisted added payload", **invoke(["--check"], ValueError)})
        added.unlink()
        mode = payload.stat().st_mode & 0o777
        payload.chmod(mode ^ 0o100)
        results.append({"control": "payload mode change", **invoke(["--check"], ValueError)})
        payload.chmod(mode)
        symbolic = isolated / "symbolic.txt"
        symbolic.symlink_to(payload)
        results.append({"control": "symlink payload", **invoke(["--check"], ValueError)})
        symbolic.unlink()
        results.append({"control": "restored exact inventory", **invoke(["--check"])})
    sys.argv = original_argv
    original = (audit / "agents/mapping/MAPPING.review.md").read_text()
    copied = (audit / "MAPPING.md").read_text()
    start = "2026-10-11。研究基準"
    assert copied[copied.index(start):] == original[original.index(start):].replace("../../authority/", "authority/")
    results.append({"control": "mapping copy body and relative-link-only transform", "passed": True})
    print(json.dumps({"scope": "isolated custody I/O only; prerequisites mocked; no actual seal verification", "verify_sha256": hashlib.sha256((audit / "verify.py").read_bytes()).hexdigest(), "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
