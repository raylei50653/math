#!/usr/bin/env python3
"""Check fresh publication Markdown links without reinterpreting frozen snapshots."""
import importlib.util
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
PUBLISH = HERE.parents[1]
ROOT = PUBLISH.parents[1]
spec = importlib.util.spec_from_file_location("check_docs", ROOT / "scripts/check_docs.py")
docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docs)
errors = []
files = [p for p in PUBLISH.rglob("*.md") if "entry-snapshot" not in p.relative_to(PUBLISH).parts]
count = 0
for source in files:
    for line, destination in docs.links(source.read_text()):
        url = urlsplit(destination)
        if url.scheme or url.netloc:
            continue
        count += 1
        target = (source.parent / unquote(url.path)).resolve() if url.path else source
        if not target.exists():
            errors.append({"path": str(source.relative_to(ROOT)), "line": line, "missing": destination})
        elif url.fragment and target.suffix == ".md" and unquote(url.fragment) not in docs.anchors(target.read_text()):
            errors.append({"path": str(source.relative_to(ROOT)), "line": line, "anchor": destination})
print(json.dumps({"pass": not errors, "fresh_publication_md": len(files), "links": count, "errors": errors}, indent=2))
raise SystemExit(0 if not errors else 1)
