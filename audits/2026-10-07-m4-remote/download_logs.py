#!/usr/bin/env python3
"""Preserve unmodified GitHub run-log ZIP bytes and checkout evidence."""
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

folder = Path(__file__).resolve().parent
run_id = sys.argv[1]
target = folder / "ci" / run_id
target.mkdir(parents=True, exist_ok=False)
argv = ["gh", "api", f"repos/raylei50653/math/actions/runs/{run_id}/logs"]
proc = subprocess.run(argv, capture_output=True)
if proc.returncode:
    (target / "download.stderr.log").write_bytes(proc.stderr)
    print(json.dumps({"argv": argv, "exit_code": proc.returncode}))
    sys.stderr.buffer.write(proc.stderr)
    sys.exit(proc.returncode)
raw = proc.stdout
(target / "original-logs.zip").write_bytes(raw)
archive = zipfile.ZipFile(io.BytesIO(raw))
checkout = []
failures = []
entries = []
for name in archive.namelist():
    if name.endswith("/"):
        continue
    data = archive.read(name)
    entries.append({"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    lines = data.decode(errors="replace").splitlines()
    for number, line in enumerate(lines):
        if "git log -1 --format=%H" in line:
            for following in range(number + 1, min(number + 5, len(lines))):
                match = re.search(r"\b([0-9a-f]{40})\s*$", lines[following])
                if match:
                    checkout.append({"path": name, "command_line": number + 1,
                                     "sha_line": following + 1, "sha": match.group(1),
                                     "command": line, "checkout_output": lines[following]})
                    break
        if any(marker in line for marker in ("missing path:", "FAIL:", "##[error]", "lake build --no-ansi", "Build completed successfully")):
            failures.append({"path": name, "line": number + 1, "text": line})
result = {"run_id": int(run_id), "argv": argv, "exit_code": 0,
          "original_zip": {"path": "original-logs.zip", "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()},
          "entries": entries, "actual_checkout_evidence": checkout,
          "checkout_shas": sorted({row["sha"] for row in checkout}),
          "build_and_failure_lines": failures}
(target / "log-evidence.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ("run_id", "original_zip", "checkout_shas", "build_and_failure_lines")}, ensure_ascii=False))
