"""Read the `docgraph:` block from Markdown front matter.

Only that block is parsed, with a small YAML subset (nested scalars, block
lists and flow lists), so other front-matter keys never affect DocGraph and
no third-party YAML library is needed. Files are only read, never written.
"""
from __future__ import annotations

import re
from pathlib import Path

from .model import FIELDS, NAME, Diagnostic, Node

SKIP_DIRS = {".git", ".lake", ".docgraph", "node_modules", "__pycache__", ".venv"}


class ParseError(ValueError):
    pass


def markdown_files(root: Path, include: list[str] | None = None) -> list[Path]:
    if include:
        found = {p for pattern in include for p in root.glob(pattern) if p.is_file()}
    else:
        found = {
            p for p in root.rglob("*.md")
            if not any(part in SKIP_DIRS or part.startswith(".")
                       for part in p.relative_to(root).parts[:-1])
        }
    return sorted(found)


def front_matter(text: str) -> list[str] | None:
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].rstrip() != "---":
        return None
    for end in range(1, len(lines)):
        if lines[end].rstrip() in ("---", "..."):
            return lines[1:end]
    # A leading thematic break is not front matter unless it claims to be ours.
    if any(l.startswith("docgraph:") for l in lines):
        raise ParseError("front matter is not closed by '---'")
    return None


def _strip_comment(line: str) -> str:
    quote = None
    for i, c in enumerate(line):
        if quote:
            if c == quote:
                quote = None
        elif c in "'\"":
            quote = c
        elif c == "#" and (i == 0 or line[i - 1].isspace()):
            return line[:i].rstrip()
    return line.rstrip()


def _scalar(value: str):
    value = value.strip()
    if value.startswith("[") :
        if not value.endswith("]"):
            raise ParseError(f"unterminated flow list: {value}")
        inner = value[1:-1].strip()
        return [_scalar(v) for v in inner.split(",")] if inner else []
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    if value[:1] in "{&*!|>":
        raise ParseError(f"unsupported YAML value: {value}")
    return value


def docgraph_block(lines: list[str]) -> dict | None:
    """Return the parsed `docgraph:` mapping, or None if the key is absent."""
    if sum(1 for l in lines if re.match(r"^docgraph:", l)) > 1:
        raise ParseError("front matter declares 'docgraph:' more than once")
    start = next((i for i, l in enumerate(lines) if re.match(r"^docgraph:\s*(#.*)?$", l)), None)
    if start is None:
        if any(re.match(r"^docgraph:", l) for l in lines):
            raise ParseError("'docgraph:' must be followed by an indented mapping")
        return None
    body = []
    for line in lines[start + 1:]:
        stripped = _strip_comment(line)
        if not stripped.strip():
            continue
        if not line[:1].isspace():
            break
        body.append(stripped)
    if not body:
        return {}
    indent = len(body[0]) - len(body[0].lstrip())
    data: dict = {}
    key = None
    for line in body:
        depth = len(line) - len(line.lstrip())
        text = line.strip()
        if depth == indent:
            match = re.match(r"^([A-Za-z_][\w-]*):(?:\s+(.*))?$", text)
            if not match:
                raise ParseError(f"expected 'key: value': {text}")
            key = match[1]
            if key in data:
                raise ParseError(f"duplicate key: {key}")
            data[key] = _scalar(match[2]) if match[2] else None
        elif depth > indent and text.startswith("- ") and key is not None:
            if data[key] is None:
                data[key] = []
            if not isinstance(data[key], list):
                raise ParseError(f"'{key}' mixes a value and list items")
            data[key].append(_scalar(text[2:]))
        else:
            raise ParseError(f"unexpected indentation: {text}")
    return data


def _names(value, key: str) -> tuple[str, ...]:
    if value is None:
        return ()
    items = value if isinstance(value, list) else [value]
    for item in items:
        if not isinstance(item, str) or not NAME.match(item):
            raise ParseError(f"'{key}' entries must be plain names, got {item!r}")
    if len(set(items)) != len(items):
        raise ParseError(f"'{key}' lists a name twice")
    return tuple(items)


def title_of(text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
        if match:
            return match[1]
    return ""


def parse_file(path: Path, root: Path) -> tuple[Node | None, list[Diagnostic]]:
    rel = path.relative_to(root).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
        lines = front_matter(text)
        block = docgraph_block(lines) if lines is not None else None
        if block is None:
            return None, []
        if not isinstance(block.get("id"), str) or not NAME.match(block["id"]):
            raise ParseError("'docgraph.id' is required and must be a plain name")
        relations = {
            k: _names(v, k) for k, v in block.items() if k not in FIELDS
        }
        node = Node(
            id=block["id"],
            path=rel,
            title=title_of(text),
            families=_names(block.get("family"), "family"),
            relations={k: v for k, v in relations.items() if v},
        )
        return node, []
    except (ParseError, UnicodeDecodeError) as exc:
        return None, [Diagnostic("error", "parse", str(exc), rel)]


def parse_repo(root: Path, include: list[str] | None = None):
    nodes, diagnostics = [], []
    for path in markdown_files(root, include):
        node, diags = parse_file(path, root)
        diagnostics.extend(diags)
        if node:
            nodes.append(node)
    return nodes, diagnostics
