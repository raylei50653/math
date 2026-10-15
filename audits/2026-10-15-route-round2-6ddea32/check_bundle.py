#!/usr/bin/env python3
"""Read-only boundary, immutable-input, syntax, and link audit for round two."""
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


def check():
    manifest = json.loads((HERE/'BASE.json').read_text())
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == manifest['base']
    assert not subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=ROOT, text=True).strip()
    for entry in manifest['authority']:
        for path in (ROOT/entry['path'], HERE/'frozen'/entry['path']):
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], str(path)
    for entry in manifest['prior_round_files']:
        path = ROOT/entry['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], str(path)
    final_manifest = HERE/'MANIFEST.json'
    if final_manifest.exists():
        for entry in json.loads(final_manifest.read_text())['files']:
            path = ROOT/entry['path']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], str(path)
    spec = importlib.util.spec_from_file_location('navigation', ROOT/'scripts/check_docs.py')
    navigation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(navigation)
    markdown = python = local_links = 0
    for name in manifest['new_directories']:
        directory = ROOT/'audits'/name
        assert (directory/'REPORT.md').is_file(), str(directory)
        for path in sorted(directory.rglob('*')):
            if not path.is_file() or any(p in ('frozen', '__pycache__') for p in path.relative_to(directory).parts):
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
            for line, destination in navigation.links(content):
                url = urlsplit(destination)
                if url.scheme or url.netloc:
                    continue
                local_links += 1
                target = (path.parent/unquote(url.path)).resolve() if url.path else path
                assert target.exists() or target == HERE/'bundle-check.json', (str(path), line, destination)
                if url.fragment and target.suffix == '.md':
                    assert unquote(url.fragment) in navigation.anchors(target.read_text()), (str(path), line, destination)
    untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
    prefixes = tuple('audits/'+name+'/' for name in manifest['prior_round_directories']+manifest['new_directories'])
    assert all(path.startswith(prefixes) for path in untracked), 'unrelated untracked file in shared workspace'
    return {'status': 'PASS', 'base': manifest['base'], 'tracked_changes': 0,
            'authority_drift': 0, 'prior_round_drift': 0,
            'sealed_prior_files': len(manifest['prior_round_files']),
            'new_audit_directories': manifest['new_directories'],
            'markdown_files_checked': markdown, 'python_files_parsed': python,
            'local_links_checked': local_links,
            'scope': 'Round-two research text, syntax, links, and immutability; frozen links retain historical context.'}


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
