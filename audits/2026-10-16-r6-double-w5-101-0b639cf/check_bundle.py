#!/usr/bin/env python3
"""Read-only audit custody, syntax, links and seal checks; not a proof verifier."""
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


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preseal', action='store_true')
    args = parser.parse_args()
    base = json.loads((HERE / 'BASE.json').read_text())
    require(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO,
                                    text=True).strip() == base['base'], 'HEAD drift')
    expected_old = {row['path'] for row in base['prior_audits']}
    old_roots = {str(Path(name).parents[len(Path(name).parts)-3]) for name in expected_old}
    actual_old = {str(p.relative_to(REPO)) for root in old_roots
                  for p in (REPO / root).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    require(actual_old == expected_old, 'prior-audit file membership drift')
    for row in base['prior_audits']:
        require(digest(REPO / row['path']) == row['sha256'], 'prior byte drift: ' + row['path'])
    allowed = {'docs/STATUS.md', 'docs/c5_kempe_guide.md',
               'docs/c5_c4_triangle_core.md', 'docs/c5_state_guide.md'}
    for row in base['frozen_inputs']:
        require(digest(HERE / row['frozen_path']) == row['sha256'], row['frozen_path'])
        if row['path'] not in allowed:
            require(digest(REPO / row['path']) == row['sha256'], row['path'])
    changed = set(subprocess.check_output(['git', 'diff', '--name-only', base['base']],
                                          cwd=REPO, text=True).splitlines())
    require(changed <= allowed, 'unrelated tracked edits: ' + repr(changed-allowed))
    new = [p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts
           and 'frozen' not in p.relative_to(HERE).parts]
    for p in new:
        if p.suffix == '.py':
            ast.parse(p.read_text(), filename=str(p))
    links = 0
    for p in new:
        if p.suffix != '.md':
            continue
        for raw in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if raw.startswith(('http:', 'https:', '#', 'mailto:')):
                continue
            target = (p.parent / unquote(raw.split('#', 1)[0])).resolve()
            if args.preseal and target == HERE / 'MANIFEST.json':
                continue
            require(target.exists(), 'missing local link: ' + str(p) + ': ' + raw)
            links += 1
    sealed = 0
    if not args.preseal:
        manifest = json.loads((HERE / 'MANIFEST.json').read_text())
        actual = {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.name != 'MANIFEST.json'}
        require(actual == {row['path'] for row in manifest['files']}, 'seal membership drift')
        for row in manifest['files']:
            require(digest(HERE / row['path']) == row['sha256'], 'seal byte drift: ' + row['path'])
        sealed = len(actual)
    print(json.dumps({'status': 'PASS', 'prior_files_unchanged': len(expected_old),
                      'frozen_authorities': len(base['frozen_inputs']), 'local_links': links,
                      'sealed_files': sealed, 'mathematical_proof_verified': False}, sort_keys=True))


if __name__ == '__main__':
    main()
