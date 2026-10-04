#!/usr/bin/env python3
"""Validate links and whitespace in the active standalone D3 audit package."""
import argparse
import importlib.util
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.repo.resolve()
    base = root / 'audits/2026-10-04-task-d3'
    spec = importlib.util.spec_from_file_location('navigation', root / 'scripts/check_docs.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    documents = sorted(p for p in base.rglob('*.md') if 'snapshot' not in p.relative_to(base).parts)
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
    for source in sorted(base.rglob('*')):
        if not source.is_file() or source.suffix not in ('.md', '.py', '.json'):
            continue
        if 'snapshot' in source.relative_to(base).parts:
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
                  scope='Active D3 files; the current result output target is created by this run; immutable snapshot copies retain their original-authority relative links')
    assert not args.output.exists(), 'Preserve earlier validation attempts'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result, ensure_ascii=False))
    assert result['all_checks_passed']


if __name__ == '__main__':
    main()
