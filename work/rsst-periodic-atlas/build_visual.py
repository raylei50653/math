#!/usr/bin/env python3
"""Embed the verified RSST periodic atlas into its inline visual source."""
from pathlib import Path
import json

DIRECTORY = Path(__file__).resolve().parent


def main():
    full = json.loads((DIRECTORY / "atlas.json").read_text())
    fields = ("id", "name", "source_index", "source_name", "ring_size",
              "source_n", "points", "basis", "edges", "degrees",
              "source_patch", "periods", "minimum_index", "preferred_period")
    data = {"examples": [{key: example[key] for key in fields}
                          for example in full["examples"]]}
    compact = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    template = (DIRECTORY / "rsst-periods-template.html").read_text()
    assert template.count("__ATLAS_JSON__") == 1
    output = template.replace("__ATLAS_JSON__", compact.replace("</", "<\\/"))
    assert len(output.encode()) < 1_000_000
    (DIRECTORY / "rsst-periods.html").write_text(output)
    print("Wrote", DIRECTORY / "rsst-periods.html", len(output.encode()), "bytes")


if __name__ == "__main__":
    main()
