#!/usr/bin/env python3
"""Read-only custody checks; --seal exclusively creates the final manifest."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO))
from scripts.check_docs import anchors, links

ROUTING = {'docs/STATUS.md', 'docs/c5_kempe_guide.md',
           'docs/c5_c4_triangle_core.md', 'docs/c5_state_guide.md'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(allow_unsealed=False):
    base = json.loads((HERE / 'BASE.json').read_text())
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    assert head == base['head'], 'HEAD changed from the frozen BASE'
    changed = set(subprocess.check_output(['git', 'diff', '--name-only', 'HEAD'],
                                         cwd=REPO, text=True).splitlines())
    assert changed <= ROUTING, ('unexpected tracked mutation', sorted(changed - ROUTING))
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'],
                                       cwd=REPO, text=True).strip(), 'unexpected staged mutation'
    for item in base['authority_files']:
        assert digest(HERE / 'frozen' / item['path']) == item['sha256'], item['path']
        if item['path'] not in ROUTING:
            assert digest(REPO / item['path']) == item['sha256'], ('live authority drift', item['path'])
    files = sorted(p for p in HERE.rglob('*') if p.is_file() and
                   '__pycache__' not in p.parts and p.name != 'MANIFEST.json')
    source_files = [p for p in files if not set(p.relative_to(HERE).parts) & {'frozen', 'routing-before'}]
    for path in source_files:
        if path.suffix == '.py':
            ast.parse(path.read_text(), filename=str(path))
        elif path.suffix == '.md':
            for line, target in links(path.read_text()):
                url = urlsplit(target)
                if url.scheme or url.netloc:
                    continue
                dest = (path.parent / unquote(url.path)).resolve() if url.path else path
                if allow_unsealed and dest == HERE / 'MANIFEST.json':
                    continue
                assert dest.exists(), (str(path.relative_to(HERE)), line, target)
                if url.fragment and dest.suffix == '.md':
                    assert unquote(url.fragment) in anchors(dest.read_text()), (str(path), line, target)
    return {'schema': 1, 'BASE': head, 'source_positivity': 'OPEN',
            'source_realizability_controls': 'not triggered',
            'frozen_authority_files': len(base['authority_files']),
            'frozen_authority_drift': [],
            'files': {str(p.relative_to(HERE)): digest(p) for p in files},
            'routing': {p: digest(REPO / p) for p in sorted(ROUTING)}}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check-inputs', action='store_true')
    mode.add_argument('--seal', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = parser.parse_args()
    actual = snapshot(allow_unsealed=args.seal or args.check_inputs)
    manifest = HERE / 'MANIFEST.json'
    if args.seal:
        with manifest.open('x') as stream:
            json.dump(actual, stream, indent=2)
            stream.write('\n')
    elif args.check:
        assert json.loads(manifest.read_text()) == actual, 'manifest membership or content drift'
    print(json.dumps({'status': 'PASS', 'audit_files': len(actual['files']),
                      'routing_files': len(actual['routing']),
                      'frozen_authority_files': actual['frozen_authority_files'],
                      'source_positivity': 'OPEN'}, sort_keys=True))


if __name__ == '__main__':
    main()
