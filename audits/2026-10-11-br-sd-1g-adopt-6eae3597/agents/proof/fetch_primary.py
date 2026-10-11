#!/usr/bin/env python3
"""Read-only fresh primary-source fetch, confined to this worker directory."""
import hashlib
import json
from pathlib import Path
import urllib.request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
URL = "https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf"
data = urllib.request.urlopen(URL, timeout=40).read()
frozen = (ROOT / "audits/2026-10-11-br-sd-1g-dbdc4c35/external/gallai.pdf").read_bytes()
(HERE / "gallai.live.pdf").write_bytes(data)
result = {
    "url": URL,
    "size": len(data),
    "sha256": hashlib.sha256(data).hexdigest(),
    "equals_original_frozen": data == frozen,
    "primary_source_version": "March 24, 2018",
    "theorem": "Theorem 10, printed p.6",
    "definition": "degree assignment, printed p.5; blockwise uniform, printed p.6",
}
(HERE / "FETCH.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
