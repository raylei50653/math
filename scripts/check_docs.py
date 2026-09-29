#!/usr/bin/env python3
"""Check local Markdown navigation and the research entry-point contract.

Standard library only. Deliberately not a full CommonMark/HTML parser; see
 docs/DOCUMENTATION.md for scope. Run from any directory, no files are written.
"""
from __future__ import annotations

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


def check(root: Path) -> tuple[list[str], int, int]:
    files = [root / "README.md"]
    for directory in ("docs", "paper", "artifacts"):
        files.extend(sorted((root / directory).rglob("*.md")))
    errors = []
    cache = {}
    count = 0
    indexed = set()
    for source in files:
        for number, destination in links(source.read_text()):
            url = urlsplit(destination)
            if url.scheme or url.netloc:
                continue
            count += 1
            target = (source.parent / unquote(url.path)).resolve() if url.path else source
            label = f"{source.relative_to(root)}:{number}: {destination}"
            if not target.exists():
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
    return errors, len(files), count


def main() -> int:
    errors, files, count = check(ROOT)
    if errors:
        print("\n".join(errors))
        print(f"FAIL: {len(errors)} errors ({files} Markdown files, {count} local links)")
        return 1
    print(f"OK: {files} Markdown files, {count} local links; anchors, index, handoff checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
