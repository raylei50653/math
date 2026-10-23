#!/usr/bin/env python3
"""Read-only verification of the frozen five-round publication domain."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def digest(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main() -> None:
    here = Path(__file__).resolve().parent
    repo = here.parent.parent
    base = json.loads((here / "BASE.json").read_text())
    expected = {row["path"]: row for row in base["audits"]}
    actual = {
        str(path.relative_to(repo))
        for directory in base["audit_directories"]
        for path in (repo / directory).rglob("*")
        if path.is_file()
    }
    errors = []
    if actual != set(expected):
        errors.append({"missing": sorted(set(expected) - actual),
                       "extra": sorted(actual - set(expected))})
    for name, row in expected.items():
        path = repo / name
        if not path.is_file():
            continue
        if digest(path) != {key: row[key] for key in ("bytes", "sha256")}:
            errors.append({"changed": name})
    routing = []
    for row in base["routing_entry"]:
        name = row["path"]
        snapshot = here / "entry-snapshot" / name
        frozen = {key: row[key] for key in ("bytes", "sha256")}
        if digest(snapshot) != frozen:
            errors.append({"changed_entry_snapshot": name})
        changed = digest(repo / name) != frozen
        routing.append({"path": name, "changed_since_publication_entry": changed})
        if name in {"README.md", "docs/HANDOFF.md", "docs/c5_common_language.md"} and changed:
            errors.append({"unexpected_routing_change": name})
    result = {"schema": "three-mask-five-round-publication-custody-v1",
              "pass": not errors, "frozen_files": len(expected),
              "frozen_bytes": sum(row["bytes"] for row in expected.values()),
              "routing": routing, "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
