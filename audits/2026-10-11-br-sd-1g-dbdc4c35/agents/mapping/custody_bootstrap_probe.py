#!/usr/bin/env python3
"""Read-only actual pre-seal prerequisites and narrow link exception."""
import hashlib
import json
from pathlib import Path
import runpy


def main():
    audit = Path(__file__).resolve().parents[2]
    ns = runpy.run_path(str(audit / "verify.py"), run_name="bootstrap_custody_review")
    pending = not (audit / "SEAL.json").exists()
    counts = ns["prerequisites"](allow_pending_seal=True)
    strict_rejected = None
    if pending:
        try:
            ns["prerequisites"]()
        except ValueError as error:
            if "missing local link" not in str(error) or "SEAL.json" not in str(error):
                raise
            strict_rejected = str(error)
        else:
            raise AssertionError("missing planned seal was accepted in strict check mode")
    print(json.dumps({"scope": "actual read-only prerequisites, no seal creation and no mathematical verification", "verify_sha256": hashlib.sha256((audit / "verify.py").read_bytes()).hexdigest(), "seal_missing_at_probe": pending, "preseal_prerequisites_passed": True, "counts": {"authority_inputs": counts[0], "old_custody_files": counts[1], "recorded_checks": counts[2], "existing_local_links": counts[3]}, "strict_missing_seal_rejection": strict_rejected, "postseal_replay": "when SEAL exists, strict prerequisites should pass and missing-target control is not triggered"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
