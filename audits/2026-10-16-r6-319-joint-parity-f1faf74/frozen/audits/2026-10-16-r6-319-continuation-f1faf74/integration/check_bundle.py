#!/usr/bin/env python3
"""Read-only custody replay for this isolated research increment."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
ROUTING = ('docs/STATUS.md', 'docs/c5_kempe_guide.md',
           'docs/c5_c4_triangle_core.md')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authority():
    base = json.loads((ROOT / 'BASE.json').read_text())
    extra = json.loads((ROOT / 'ADDITIONAL_INPUTS.json').read_text())
    assert extra['base'] == base['base']
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO,
                                   text=True).strip() == base['base']
    records = base['authority_inputs'] + extra['authority_inputs']
    for record in records:
        path = record['path']
        assert sha(ROOT / 'frozen' / path) == record['sha256'], path
        original = subprocess.check_output(
            ['git', 'show', base['base'] + ':' + path], cwd=REPO)
        assert hashlib.sha256(original).hexdigest() == record['sha256'], path
        if path not in ROUTING:
            assert sha(REPO / path) == record['sha256'], path
    return base['base'], len(records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seal', action='store_true')
    parser.add_argument('--manifest', type=Path, default=ROOT / 'MANIFEST.json')
    args = parser.parse_args()
    base, inputs = authority()
    if args.seal:
        files = sorted(p for p in ROOT.rglob('*') if p.is_file()
                       and p != ROOT / 'MANIFEST.json')
        result = {'base': base, 'frozen_authorities': inputs,
                  'files': {str(p.relative_to(ROOT)): sha(p) for p in files},
                  'routing': {p: sha(REPO / p) for p in ROUTING},
                  'source_exclusion': 'OPEN', 'commit_or_push': False}
        with args.manifest.open('x') as out:
            json.dump(result, out, indent=2, sort_keys=True)
            out.write('\n')
    else:
        result = json.loads(args.manifest.read_text())
        assert result['base'] == base and result['frozen_authorities'] == inputs
        assert result['source_exclusion'] == 'OPEN'
        assert result['commit_or_push'] is False
        for name, digest in result['files'].items():
            path = (ROOT / name).resolve()
            assert path.is_relative_to(ROOT), name
            assert sha(path) == digest, name
        assert {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
                and p != ROOT / 'MANIFEST.json'} == set(result['files'])
        for name, digest in result['routing'].items():
            assert name in ROUTING and sha(REPO / name) == digest, name
    print(json.dumps({'ok': True, 'frozen_authorities': inputs,
                      'sealed_files': len(result['files']),
                      'source_exclusion': 'OPEN'}, sort_keys=True))


if __name__ == '__main__':
    main()
