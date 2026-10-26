#!/usr/bin/env python3
"""Verify the connected publication's immutable reports and source bindings.

Only explicitly named historical Markdown snapshots may replace a changed
current file. Executable-source drift fails closed. This is a custody check;
it does not establish mathematical correctness or expand the proof scope.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


PUBLICATION = Path(__file__).resolve().parent
ROOT = PUBLICATION.parents[2]
MODEL = "audits/2026-10-26-four-color-mathematical-model-8d28acc"
SIX = "audits/2026-10-26-four-color-six-edge-cuts-8d28acc"
CK = "audits/2026-10-26-ck-d-lock-comparison-8d28acc"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def audit(root):
    relative_publication = PUBLICATION.relative_to(ROOT)
    publication = root / relative_publication
    model = json.loads((root / MODEL / "verification.json").read_text())
    ck = json.loads((root / CK / "verification.json").read_text())
    snapshots = {
        (name, model["source_sha256"][name]): publication / "pre-model-docs" / (Path(name).name + ".txt")
        for name in ("docs/STATUS.md", "docs/four_color_guide.md")
    }
    snapshots[("docs/STATUS.md", ck["source_sha256"]["docs/STATUS.md"])] = (
        publication / "pre-publication-docs/STATUS.md.txt")
    records = []
    for package, filename in ((MODEL, "report.json"), (MODEL, "verification.json"),
                              (SIX, "report.json"), (CK, "report.json"), (CK, "verification.json")):
        path = root / package / filename
        payload = json.loads(path.read_text())
        sources = payload["source_sha256"]
        if isinstance(sources, str):
            sources = {package + "/replay.py": sources}
        bindings = []
        for name, expected in sources.items():
            current = root / name
            if current.is_file() and digest(current) == expected:
                bound = current
                kind = "current"
            else:
                assert name.startswith("docs/"), f"executable source drift: {name}"
                bound = snapshots[(name, expected)]
                assert digest(bound) == expected, (name, bound)
                kind = "historical-document"
            bindings.append(dict(source=name, expected_sha256=expected,
                                 binding=kind, path=str(bound.relative_to(root))))
        records.append(dict(record=str(path.relative_to(root)), record_sha256=digest(path),
                            bindings=bindings))
    return dict(records=records, checked_bindings=sum(len(r["bindings"]) for r in records),
                historical_document_bindings=sum(b["binding"] == "historical-document"
                    for r in records for b in r["bindings"]),
                all_bindings_match=True,
                script_sha256=digest(Path(__file__)),
                scope="Three original evidence packages; original receipts retained without changes.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.root.resolve())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in
          ("checked_bindings", "historical_document_bindings", "all_bindings_match")}, sort_keys=True))


if __name__ == "__main__":
    main()
