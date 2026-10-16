#!/usr/bin/env python3
"""Read-only custody and delivery check; not a proof verifier."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preseal', action='store_true')
    args = parser.parse_args()
    base = json.loads((HERE / 'BASE.json').read_text())
    require(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO,
                                    text=True).strip() == base['git_head'], 'HEAD drift')
    for row in base['prior_audit_inputs']:
        require(digest(REPO / row['path']) == row['sha256'], row['path'])
    for row in base['frozen_inputs']:
        require(digest(HERE / row['snapshot']) == row['sha256'], row['snapshot'])
        if not row['routing']:
            require(digest(REPO / row['path']) == row['sha256'], row['path'])
    allowed = {'docs/STATUS.md', 'docs/c5_kempe_guide.md',
               'docs/c5_c4_triangle_core.md', 'docs/c5_state_guide.md'}
    changed = set(subprocess.check_output(['git', 'diff', '--name-only'], cwd=REPO,
                                          text=True).splitlines())
    require(changed <= allowed, 'Unexpected tracked changes: ' + str(changed - allowed))
    for row in base['frozen_inputs']:
        if row['routing'] and row['path'] not in allowed:
            require(digest(REPO / row['path']) == row['sha256'], row['path'])
    new = [p for p in HERE.rglob('*') if p.is_file()
           and 'frozen' not in p.relative_to(HERE).parts
           and '__pycache__' not in p.parts]
    scripts = [p for p in new if p.suffix == '.py']
    for p in scripts:
        ast.parse(p.read_text(), filename=str(p))
    links = 0
    for p in new:
        if p.suffix != '.md':
            continue
        for raw in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if raw.startswith(('http:', 'https:', '#', 'mailto:')):
                continue
            target = unquote(raw.split('#', 1)[0])
            if args.preseal and (p.parent / target).resolve() == HERE / 'MANIFEST.json':
                continue
            require((p.parent / target).exists(), f'Missing link: {p}: {target}')
            links += 1
    manifest_rows = 0
    if not args.preseal:
        manifest = json.loads((HERE / 'MANIFEST.json').read_text())
        actual = {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file()
                  and p != HERE / 'MANIFEST.json' and '__pycache__' not in p.parts}
        expected = {row['path'] for row in manifest['files']}
        require(actual == expected, 'Manifest membership drift')
        for row in manifest['files']:
            require(digest(HERE / row['path']) == row['sha256'], row['path'])
        manifest_rows = len(expected)
    print(json.dumps({'status': 'PASS', 'mathematical_proof_verified': False,
                      'prior_audit_files_unchanged': len(base['prior_audit_inputs']),
                      'frozen_inputs': len(base['frozen_inputs']),
                      'new_python_syntax_checked': len(scripts), 'local_links': links,
                      'sealed_files_checked': manifest_rows}, indent=2))


if __name__ == '__main__':
    main()
