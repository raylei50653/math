#!/usr/bin/env python3
"""Check D9 new-text whitespace, Python syntax, and intended-path local links."""
import argparse
import ast
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    intended = args.root / 'audits/2026-10-06-task-d9'
    issues, links, checked, fragments_checked = [], [], [], 0
    for path in sorted(here.glob('*')):
        if not path.is_file() or path.suffix not in {'.py', '.md', '.json'}:
            continue
        value = path.read_text()
        checked.append(path.name)
        for lineno, line in enumerate(value.splitlines(), 1):
            if line.rstrip() != line:
                issues.append(dict(file=path.name, line=lineno, error='trailing whitespace'))
        if value and not value.endswith('\n'):
            issues.append(dict(file=path.name, error='missing final newline'))
        if value.endswith('\n\n'):
            issues.append(dict(file=path.name, error='extra final blank line'))
        if path.suffix == '.py':
            ast.parse(value, filename=path.name)
        if path.suffix == '.md':
            for match in re.finditer(r'\[[^\]]*\]\(([^\s)]+)\)', value):
                target = match.group(1).strip('<>')
                if '://' in target or target.startswith('#'):
                    continue
                target, separator, fragment = target.partition('#')
                physical = (intended / target).resolve()
                if physical.is_relative_to(intended):
                    physical = here / physical.relative_to(intended)
                exists = physical.exists()
                links.append(dict(file=path.name, target=target, exists=exists))
                if not exists:
                    issues.append(dict(file=path.name, error='missing local link', target=target))
                if exists and separator and physical.suffix == '.md':
                    headings = re.findall(r'^#{1,6}\s+(.+?)\s*#*\s*$', physical.read_text(), re.M)
                    slugs = {re.sub(r'[^\w\s-]', '', heading.lower()).replace(' ', '-')
                             for heading in headings}
                    fragments_checked += 1
                    if fragment not in slugs:
                        issues.append(dict(file=path.name, error='missing heading anchor',
                                           target=target, fragment=fragment))
    result = dict(intended_root=str(args.root), checked_files=checked,
                  local_links=links, errors=issues,
                  heading_fragments_checked=fragments_checked)
    (here / 'audit_output_checks.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(files=len(checked), links=len(links), errors=issues), ensure_ascii=False))
    raise SystemExit(bool(issues))


if __name__ == '__main__':
    main()
