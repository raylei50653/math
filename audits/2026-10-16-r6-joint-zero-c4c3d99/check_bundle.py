#!/usr/bin/env python3
"""Read-only custody, new-source syntax, and local-link audit."""
import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preseal', action='store_true')
    args = parser.parse_args()
    base = json.loads((HERE / 'BASE.json').read_text())
    routing = json.loads((HERE / 'ROUTING_BASE.json').read_text())
    permitted = {row['path'] for row in routing['permitted_routing_updates']}
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    assert head == base['base'] == routing['base'], 'HEAD drift'
    changed = set(subprocess.check_output(
        ['git', 'diff', '--name-only', base['base']], cwd=REPO, text=True).splitlines())
    assert changed <= permitted, ('unauthorized tracked drift', changed - permitted)
    authority_count = 0
    for row in base['inputs']:
        assert sha(HERE / 'frozen' / row['path']) == row['sha256'], row['path']
        if row['path'] not in permitted:
            assert sha(REPO / row['path']) == row['sha256'], row['path']
            authority_count += 1
    for row in routing['permitted_routing_updates']:
        assert sha(HERE / 'routing-before' / row['path']) == row['sha256'], row['path']
    new = [p for p in HERE.rglob('*') if p.is_file()
           and not {'frozen', 'routing-before'}.intersection(p.relative_to(HERE).parts)]
    scripts = [p for p in new if p.suffix == '.py']
    for p in scripts:
        ast.parse(p.read_text(), filename=str(p))
    link_count = 0
    for p in new:
        if p.suffix != '.md':
            continue
        for dest in re.findall(r'\]\(([^)\s]+)\)', p.read_text()):
            if '://' in dest or dest.startswith('#'):
                continue
            path = unquote(dest.split('#', 1)[0])
            target = p.parent / path
            pending = {HERE / 'MANIFEST.json', HERE / 'bundle-check.json'}
            assert target.exists() or (args.preseal and target in pending), (p, dest)
            link_count += 1
    manifest = HERE / 'MANIFEST.json'
    if manifest.exists():
        seal = json.loads(manifest.read_text())
        actual = {str(p.relative_to(HERE)): sha(p) for p in HERE.rglob('*')
                  if p.is_file() and p != manifest}
        assert actual == seal['audit_files'], 'audit member or byte drift'
        for name, digest in seal['routing_files'].items():
            assert sha(REPO / name) == digest, name
    print(json.dumps({'result': 'PASS', 'base': head,
                      'frozen_inputs': len(base['inputs']),
                      'live_authority_unchanged': authority_count,
                      'routing_changed': sorted(changed),
                      'new_python_scripts': len(scripts),
                      'new_source_links': link_count,
                      'final_manifest_checked': manifest.exists()}, sort_keys=True))


if __name__ == '__main__':
    main()
