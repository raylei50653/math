#!/usr/bin/env python3
"""Read-only round-three scope, frozen-input, syntax and link checks."""
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


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    base = json.loads((HERE / 'BASE.json').read_text())
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == base['base']
    assert not subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'], cwd=ROOT, text=True).strip(), 'tracked edits'
    for name, expected in base['prior_file_hashes'].items():
        assert digest(ROOT / name) == expected, name
    actual_prior = {
        str(path.relative_to(ROOT))
        for name in base['prior_audits']
        for path in (ROOT / name).rglob('*')
        if path.is_file() and '__pycache__' not in path.parts
    }
    assert actual_prior == set(base['prior_file_hashes']), 'prior file membership changed'
    for name, expected in base['authority_hashes'].items():
        assert digest(ROOT / name) == expected, name
        assert digest(HERE / 'frozen' / name) == expected, 'frozen ' + name
    seal = HERE / 'MANIFEST.json'
    if seal.exists():
        sealed = json.loads(seal.read_text())
        for name, expected in sealed['file_hashes'].items():
            assert digest(ROOT / name) == expected, name
        new_files = {
            str(path.relative_to(ROOT))
            for name in base['write_scope']
            for path in (ROOT / name).rglob('*')
            if path.is_file() and '__pycache__' not in path.parts
        }
        assert new_files - set(sealed['excluded_outputs']) == set(sealed['file_hashes']), 'new file membership changed'
    spec = importlib.util.spec_from_file_location('navigation', ROOT / 'scripts/check_docs.py')
    navigation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(navigation)
    counts = {'markdown': 0, 'python': 0, 'local_links': 0}
    for name in base['write_scope']:
        directory = ROOT / name
        assert (directory / 'REPORT.md').is_file(), 'missing REPORT: ' + name
        for path in sorted(directory.rglob('*')):
            if not path.is_file() or any(p in ('frozen', '__pycache__') for p in path.relative_to(directory).parts):
                continue
            if path.suffix not in ('.md', '.py'):
                continue
            content = path.read_text()
            assert all(line == line.rstrip() for line in content.splitlines()), 'trailing whitespace: ' + str(path)
            if path.suffix == '.py':
                ast.parse(content, filename=str(path))
                counts['python'] += 1
                continue
            counts['markdown'] += 1
            for line, destination in navigation.links(content):
                url = urlsplit(destination)
                if url.scheme or url.netloc:
                    continue
                counts['local_links'] += 1
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                # These two outputs are created only after the preliminary pass.
                pending = {HERE / 'bundle-check.json', HERE / 'MANIFEST.json'}
                assert target.exists() or target in pending, (str(path), line, destination)
                if url.fragment and target.suffix == '.md':
                    assert unquote(url.fragment) in navigation.anchors(target.read_text()), (str(path), line, destination)
    untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
    allowed = tuple(name + '/' for name in base['prior_audits'] + base['write_scope'])
    assert all(path.startswith(allowed) for path in untracked), 'unrelated untracked file'
    return {'status': 'PASS', 'base': base['base'], 'prior_files': len(actual_prior),
            'prior_drift': 0, 'authority_drift': 0, 'tracked_changes': 0,
            'new_audits': base['write_scope'], 'checks': counts,
            'scope': 'Round-three files and immutable inputs; not a mathematical source-exclusion checker.'}


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
