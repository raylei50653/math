#!/usr/bin/env python3
"""Check local Markdown navigation and the research entry-point contract.

Standard library only. Deliberately not a full CommonMark/HTML parser; see
 docs/DOCUMENTATION.md for scope. Run from any directory, no files are written.
"""
from __future__ import annotations

import json
import re
import sys
import string
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def prose(text: str) -> str:
    """Remove fenced code while retaining source line numbers."""
    fence = None
    lines = []
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
                fence = None
            lines.append("")
        elif match:
            fence = match[1]
            lines.append("")
        else:
            lines.append(line)
    return "\n".join(lines)


def slug(title: str) -> str:
    title = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", title)
    title = re.sub(r"<[^>]*>", "", title)
    title = title.replace("`", "").replace("*", "")
    return "".join(
        c for c in title.lower()
        if (c in "-_ " or unicodedata.category(c)[0] in "LMNS")
        and (c not in string.punctuation or c in "-_")
    ).replace(" ", "-")


def anchors(text: str) -> set[str]:
    text = prose(text)
    found = set(re.findall(r'<[^>]+\b(?:id|name)=[\'\"]([^\'\"]+)', text))
    headings = set()
    for line in text.splitlines():
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            base = slug(match[1])
            key = base
            n = 0
            while key in headings:
                n += 1
                key = f"{base}-{n}"
            headings.add(key)
    return found | headings


def links(text: str):
    """Yield (line number, destination), including reference definitions."""
    for number, line in enumerate(prose(text).splitlines(), 1):
        # Ignore inline code; link labels are irrelevant to target validation.
        line = re.sub(r"(`+).*?\1", "", line)
        for match in re.finditer(r"\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)", line):
            yield number, match[1].strip("<>")
        match = re.match(r"^ {0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", line)
        if match:
            yield number, match[1].strip("<>")


def check_handoff(text: str) -> list[str]:
    """Check the thin guide list; ordinary link checking validates its targets."""
    errors = []
    guides = 0
    if len(text.splitlines()) > 30:
        errors.append("HANDOFF exceeds 30 lines; move details to research guides")
    for number, line in enumerate(prose(text).splitlines(), 1):
        # Inline code is allowed to explain the tag without activating a line.
        visible = re.sub(r"(`+).*?\1", "", line)
        destinations = [destination for _, destination in links(line)]
        if not (line.startswith("- ") or "#進行中" in visible
                or any(urlsplit(dst).path.endswith("_guide.md") for dst in destinations)):
            continue
        match = re.fullmatch(r"- \[[^\]]+\]\(([^\s)]+)\)(?: #進行中)?", line)
        if not match:
            errors.append(f"HANDOFF:{number}: expected guide list item with optional trailing #進行中")
            continue
        url = urlsplit(match[1])
        if (not url.scheme and not url.netloc and not url.fragment and not url.query
                and url.path in ("STATUS.md", "DOCUMENTATION.md")
                and not line.endswith(" #進行中")):
            continue
        if (url.scheme or url.netloc or url.fragment or url.query
                or Path(unquote(url.path)).is_absolute()
                or not unquote(url.path).endswith("_guide.md")):
            errors.append(f"HANDOFF:{number}: research entry must point to a local *_guide.md file")
            continue
        guides += 1
    if not guides:
        errors.append("HANDOFF must list at least one research guide")
    return errors


def check_guide_progress(text: str, label: str) -> list[str]:
    """Check the small handoff summary, without interpreting research claims."""
    visible = prose(text)
    heading = re.search(r"^## 最新進度\s*$", visible, re.MULTILINE)
    if not heading:
        return [f"{label}: missing 最新進度 handoff summary"]
    errors = []
    if len(re.findall(r"^## 最新進度\s*$", visible, re.MULTILINE)) != 1:
        errors.append(f"{label}: 最新進度 must occur exactly once")
    if len(visible[:heading.start()].splitlines()) >= 12:
        errors.append(f"{label}: 最新進度 must start within the first 12 lines")
    rest = visible[heading.end():]
    end = re.search(r"^## ", rest, re.MULTILINE)
    section = rest[:end.start()] if end else rest
    if len(section.strip().splitlines()) + 1 > 40:
        errors.append(f"{label}: 最新進度 exceeds 40 lines; link to detailed sections")
    milestone = re.search(r"^### 近期里程碑\s*$", section, re.MULTILINE)
    summary = section[:milestone.start()] if milestone else section
    for field in ("階段／生命週期", "最近研究更新", "上次完成", "目前停止點", "下一步", "接手入口"):
        cells = re.findall(rf"^\|\s*{re.escape(field)}\s*\|\s*(.*?)\s*\|\s*$", summary, re.MULTILINE)
        if len(cells) != 1 or not cells[0].strip():
            errors.append(f"{label}: expected one nonempty 最新進度 field: {field}")
    if not milestone:
        errors.append(f"{label}: missing 近期里程碑")
    else:
        rows = []
        for line in section[milestone.end():].splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if not line.startswith("|") or not cells[0] or cells[0] == "日期／階段":
                continue
            if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                continue
            rows.append(line)
        if not 3 <= len(rows) <= 5:
            errors.append(f"{label}: 近期里程碑 must contain 3–5 entries")
        if any(not list(links(row)) for row in rows):
            errors.append(f"{label}: each 近期里程碑 entry must link to its source")
    return errors


def check(root: Path) -> tuple[list[str], int, int]:
    files = [root / "README.md"]
    for directory in ("docs", "paper", "artifacts"):
        files.extend(sorted((root / directory).rglob("*.md")))
    errors = []
    cache = {}
    count = 0
    indexed = set()
    manifest = root / "artifacts/MANIFEST.json"
    # large JSON kept out of git and rebuilt by tools/artifacts.py count as present
    reproducible = {(root / path).resolve() for path in json.loads(manifest.read_text())["files"]} \
        if manifest.exists() else set()
    for source in files:
        for number, destination in links(source.read_text()):
            url = urlsplit(destination)
            if url.scheme or url.netloc:
                continue
            count += 1
            target = (source.parent / unquote(url.path)).resolve() if url.path else source
            label = f"{source.relative_to(root)}:{number}: {destination}"
            if not target.exists() and target not in reproducible:
                errors.append(f"missing path: {label}")
                continue
            if source == root / "docs/STATUS.md":
                indexed.add(target)
            if url.fragment and target.suffix == ".md":
                if target not in cache:
                    cache[target] = anchors(target.read_text())
                if unquote(url.fragment) not in cache[target]:
                    errors.append(f"missing anchor: {label}")
    for target in (root / "docs").rglob("*.md"):
        if target.name == "STATUS.md":
            continue
        if target.resolve() not in indexed:
            errors.append(f"not directly indexed by STATUS: {target.relative_to(root)}")
    handoff = (root / "docs/HANDOFF.md").read_text()
    errors.extend(check_handoff(handoff))
    for _, destination in links(handoff):
        url = urlsplit(destination)
        if (not url.scheme and not url.netloc and not url.fragment and not url.query
                and not Path(unquote(url.path)).is_absolute()
                and unquote(url.path).endswith("_guide.md")):
            target = root / "docs" / unquote(url.path)
            if target.exists():
                errors.extend(check_guide_progress(target.read_text(), str(target.relative_to(root))))
    return errors, len(files), count


def main() -> int:
    errors, files, count = check(ROOT)
    if errors:
        print("\n".join(errors))
        print(f"FAIL: {len(errors)} errors ({files} Markdown files, {count} local links)")
        return 1
    print(f"OK: {files} Markdown files, {count} local links; anchors, index, handoff, guide progress checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
