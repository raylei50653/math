#!/usr/bin/env python3
"""Read-only custody and delivery checks; not an arbitrary-size proof verifier."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def members():
    return sorted(p for p in HERE.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.name != 'MANIFEST.json')


def custody():
    base = json.loads((HERE / 'BASE.json').read_text())
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    require(head == base['base'], 'research HEAD changed')
    expected = {row['path']: row['sha256'] for row in base['inputs']}
    for rel, digest in expected.items():
        require(sha(ROOT / rel) == digest, 'authority drift: ' + rel)
    for directory in base['prior_directories']:
        actual = {str(p.relative_to(ROOT)) for p in (ROOT / directory).rglob('*') if p.is_file()}
        require(actual == {p for p in expected if p.startswith(directory + '/')},
                'prior audit membership drift: ' + directory)
    for p in (HERE / 'frozen').rglob('*'):
        if p.is_file():
            rel = str(p.relative_to(HERE / 'frozen'))
            require(rel in expected and sha(p) == expected[rel], 'frozen copy drift: ' + rel)
    require(not subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT),
            'tracked worktree changes outside isolated research')
    require(not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT),
            'unexpected staged changes')
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text(), filename=str(p))
    spec = importlib.util.spec_from_file_location('audit_docs', ROOT / 'scripts/check_docs.py')
    docs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(docs)
    for p in HERE.glob('*.md'):
        for line, target in docs.links(p.read_text()):
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            dest = (p.parent / unquote(url.path)).resolve() if url.path else p
            if dest == HERE / 'MANIFEST.json' and not dest.exists():
                # The only pending target is created after all member files exist.
                continue
            require(dest.exists(), f'broken local link {p.name}:{line}: {target}')
            if url.fragment and dest.suffix == '.md':
                require(unquote(url.fragment) in docs.anchors(dest.read_text()),
                        f'broken anchor {p.name}:{line}: {target}')
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write-manifest', action='store_true')
    mode.add_argument('--check-manifest', action='store_true')
    args = parser.parse_args()
    count = custody()
    manifest = {'task': 'R6-SEVEN-DISK-RIGIDITY',
                'excludes': ['MANIFEST.json', '**/__pycache__/**'],
                'files': [{'path': str(p.relative_to(HERE)), 'sha256': sha(p),
                           'bytes': p.stat().st_size} for p in members()]}
    seal = HERE / 'MANIFEST.json'
    if args.write_manifest:
        with seal.open('x') as stream:
            json.dump(manifest, stream, indent=2, sort_keys=True)
            stream.write('\n')
    if args.check_manifest:
        require(json.loads(seal.read_text()) == manifest, 'audit seal or membership drift')
    print(json.dumps({'status': 'PASS', 'frozen_authority_files': count,
                      'sealed_members': len(manifest['files']),
                      'seal_checked': args.check_manifest,
                      'mathematical_proof_verifier': False}, sort_keys=True))


if __name__ == '__main__':
    main()
