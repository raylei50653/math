#!/usr/bin/env python3
"""Validate links and whitespace in the active standalone D4 audit package."""
import argparse
import importlib.util
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.repo.resolve()
    base = root / 'audits/2026-10-04-task-d4'
    spec = importlib.util.spec_from_file_location('navigation', root / 'scripts/check_docs.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    documents = sorted(p for p in base.rglob('*.md') if not {'snapshot', '.snapshot'} & set(p.relative_to(base).parts))
    errors, links = [], 0
    for source in documents:
        for line, destination in module.links(source.read_text()):
            url = urlsplit(destination)
            if url.scheme or url.netloc:
                continue
            links += 1
            target = (source.parent / unquote(url.path)).resolve() if url.path else source
            if not target.exists() and target != args.output.resolve():
                errors.append(dict(source=str(source.relative_to(root)), line=line,
                                   problem='missing target', destination=destination))
            elif target.exists() and url.fragment and target.suffix == '.md' and unquote(url.fragment) not in module.anchors(target.read_text()):
                errors.append(dict(source=str(source.relative_to(root)), line=line,
                                   problem='missing anchor', destination=destination))
    whitespace = []
    archived_sources = []
    for source in sorted(base.rglob('*')):
        if not source.is_file() or source.suffix not in ('.md', '.py', '.json'):
            continue
        if {'snapshot', '.snapshot'} & set(source.relative_to(base).parts):
            continue
        parts = source.relative_to(base).parts
        if source.suffix == '.py' and any(p.startswith('attempt') or 'root-replay' in p for p in parts[:-1]):
            archived_sources.append(dict(path=str(source.relative_to(root)),
                                         sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
            continue
        value = source.read_text()
        for number, line in enumerate(value.splitlines(), 1):
            if line.rstrip() != line:
                whitespace.append(dict(path=str(source.relative_to(root)), line=number))
        if value and not value.endswith('\n'):
            whitespace.append(dict(path=str(source.relative_to(root)), problem='missing final newline'))
        if value.endswith('\n\n'):
            whitespace.append(dict(path=str(source.relative_to(root)), problem='blank final line'))
    result = dict(all_checks_passed=not errors and not whitespace, markdown_files=len(documents),
                  local_links=links, link_errors=errors, whitespace_errors=whitespace,
                  archived_source_versions=archived_sources,
                  scope='Active D4 files; immutable snapshot and archived attempt source bytes retain their historical authority and are hash-recorded separately. The current result output target is created by this run.')
    assert not args.output.exists(), 'Preserve earlier validation attempts'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result, ensure_ascii=False))
    assert result['all_checks_passed']


if __name__ == '__main__':
    main()
