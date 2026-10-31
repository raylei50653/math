"""Embed frozen records in both fragments without network requests.

Standalone preview exports are separate snapshots; re-export after changing a
fragment. The browser checks exercise the checked-in standalone snapshots.
"""
import json
from pathlib import Path
import re

directory = Path(__file__).resolve().parent
for fragment_name, records in [
    ("triangle-crystals.html", [("tc-catalog", "crystals.json")]),
    ("color-periodicity.html", [("cp-geometry", "crystals.json"), ("cp-colorings", "colorings.json")]),
]:
    fragment = directory / fragment_name
    source = fragment.read_text()
    for script_id, filename in records:
        data = json.loads((directory / filename).read_text())
        encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        pattern = rf'(<script id="{script_id}" type="application/json">).*?(</script>)'
        source, count = re.subn(pattern, lambda m: m[1] + encoded + m[2], source, flags=re.S)
        assert count == 1
    fragment.write_text(source)
    print(f"Embedded frozen records: {fragment.name} ({fragment.stat().st_size} bytes)")
