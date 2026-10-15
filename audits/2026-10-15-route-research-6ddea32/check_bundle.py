#!/usr/bin/env python3
"""Read-only checks for the four isolated research directories."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
NAMES = ('2026-10-15-route-research-6ddea32', '2026-10-15-tait-separation-6ddea32',
         '2026-10-15-f4-relation-6ddea32', '2026-10-15-r6-seven-pin-6ddea32')


def check():
    manifest = json.loads((HERE/'BASE.json').read_text())
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == manifest['base']
    assert not subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=ROOT, text=True).strip()
    for item in manifest['files']:
        for path in (ROOT/item['path'], HERE/'frozen'/item['path']):
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], str(path)
    spec = importlib.util.spec_from_file_location('navigation', ROOT/'scripts/check_docs.py')
    nav = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nav)
    markdown = python = local_links = 0
    for name in NAMES:
        for path in sorted((ROOT/'audits'/name).rglob('*')):
            if not path.is_file() or any(p in ('frozen', 'inputs') for p in path.relative_to(ROOT/'audits'/name).parts):
                continue
            if path.suffix not in ('.md', '.py'):
                continue
            content = path.read_text()
            assert all(line == line.rstrip() for line in content.splitlines()), 'trailing whitespace: '+str(path)
            if path.suffix == '.py':
                ast.parse(content, filename=str(path))
                python += 1
                continue
            markdown += 1
            for line, destination in nav.links(content):
                url = urlsplit(destination)
                if url.scheme or url.netloc:
                    continue
                local_links += 1
                target = (path.parent/unquote(url.path)).resolve() if url.path else path
                # This receipt is created only after this very first check succeeds.
                assert target.exists() or target == HERE/'bundle-check.json', (path, line, destination)
                if url.fragment and target.suffix == '.md':
                    assert unquote(url.fragment) in nav.anchors(target.read_text()), (path, line, destination)
    untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
    prefixes = tuple('audits/'+name+'/' for name in NAMES)
    assert all(path.startswith(prefixes) for path in untracked), 'unrelated untracked file in shared workspace'
    return {'status': 'PASS', 'base': manifest['base'], 'frozen_input_drift': 0,
            'tracked_changes': 0, 'exclusive_audit_directories': list(NAMES),
            'markdown_files_checked': markdown, 'python_files_parsed': python,
            'local_links_checked': local_links, 'untracked_files_in_scope': len(untracked),
            'scope': 'Research text and source checks; frozen snapshots retain original relative references.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    result = check()
    if args.write:
        with args.write.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
