#!/usr/bin/env python3
"""Final isolated custody controls; prerequisites deliberately mocked."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile


def main():
    directory = Path(__file__).resolve().parent
    audit = directory.parents[1]
    baseline = runpy.run_path(str(directory / "custody_probe.py"), run_name="baseline_probe")
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        baseline["main"]()
    results = json.loads(output.getvalue())["results"]
    ns = runpy.run_path(str(audit / "verify.py"), run_name="claim_probe")
    scope = ns["main"].__globals__
    original_argv = sys.argv[:]
    with tempfile.TemporaryDirectory(prefix="br-sd-1g-final-custody-") as name:
        isolated = Path(name)
        scope["AUDIT"] = isolated
        scope["prerequisites"] = lambda: (31, 313, 1, 1)
        (isolated / "payload.txt").write_bytes(b"final review payload\n")
        sys.argv = ["verify.py", "--seal"]
        with contextlib.redirect_stdout(io.StringIO()):
            ns["main"]()
        seal = isolated / "SEAL.json"
        original = seal.read_text()
        for label, mutation in [
            ("claim drift rejected", lambda value: value.update(claim="unscoped closure")),
            ("extra seal metadata rejected", lambda value: value.update(unreviewed_metadata=True)),
        ]:
            value = json.loads(original)
            mutation(value)
            seal.write_text(json.dumps(value))
            sys.argv = ["verify.py", "--check"]
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    ns["main"]()
            except ValueError as error:
                results.append({"control": label, "caught": "ValueError", "message": str(error)})
            else:
                raise AssertionError(label)
        seal.write_text(original)
        with contextlib.redirect_stdout(io.StringIO()):
            ns["main"]()
        results.append({"control": "restored fixed claim and exact keys", "passed": True})
    sys.argv = original_argv
    print(json.dumps({"scope": "isolated custody I/O only; prerequisites mocked; no actual audit seal verification", "verify_sha256": hashlib.sha256((audit / "verify.py").read_bytes()).hexdigest(), "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
