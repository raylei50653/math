#!/usr/bin/env python3
"""Read-only publication custody replay; does not verify the paper theorem."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ROUTING_EDITS = {
    'docs/STATUS.md', 'docs/c5_kempe_guide.md',
    'docs/c5_c4_triangle_core.md', 'docs/c5_state_guide.md',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def files(directory):
    return {str(p.relative_to(directory)): p for p in directory.rglob('*')
            if p.is_file() and '__pycache__' not in p.parts}


def main():
    initial = json.loads((HERE / 'initial-state.json').read_text())
    results = []
    for snapshot in initial['audits']:
        audit = ROOT / snapshot['directory']
        current = files(audit)
        expected = {r['path']: r for r in snapshot['files']}
        require(current.keys() == expected.keys(), 'audit membership drift')
        for rel, path in current.items():
            require(not path.is_symlink(), 'unexpected audit symlink: ' + rel)
            require(digest(path.read_bytes()) == expected[rel]['sha256'], rel)
        manifest = json.loads((audit / 'MANIFEST.json').read_text())
        require(set(current) == {r['path'] for r in manifest['files']} | {'MANIFEST.json'},
                'manifest membership drift')
        for row in manifest['files']:
            path = audit / row['path']
            require(digest(path.read_bytes()) == row['sha256'], str(path))
            require(path.stat().st_size == row['bytes'], str(path))
        base = json.loads((audit / 'BASE.json').read_text())
        subprocess.run(['git', 'merge-base', '--is-ancestor', base['base'], 'HEAD'],
                       cwd=ROOT, check=True)
        inputs = {r['path']: r['sha256'] for r in base['inputs']}
        historical_routing = []
        for rel, expected_sha in inputs.items():
            if rel in ROUTING_EDITS:
                data = subprocess.check_output(['git', 'show', base['base'] + ':' + rel],
                                               cwd=ROOT)
                historical_routing.append(rel)
            else:
                data = (ROOT / rel).read_bytes()
            require(digest(data) == expected_sha, 'authority drift: ' + rel)
        for directory in base['prior_directories']:
            actual = {directory + '/' + rel for rel in files(ROOT / directory)}
            require(actual == {rel for rel in inputs if rel.startswith(directory + '/')},
                    'prior audit membership drift: ' + directory)
        for rel, path in files(audit / 'frozen').items():
            require(rel in inputs and digest(path.read_bytes()) == inputs[rel],
                    'frozen authority drift: ' + rel)
        results.append({'directory': snapshot['directory'], 'base': base['base'],
                        'sealed_files_including_manifest': len(current),
                        'authority_inputs': len(inputs),
                        'routing_checked_at_research_base': sorted(historical_routing)})
    print(json.dumps({'status': 'PASS', 'audits': results,
                      'original_audit_bytes_unchanged': True,
                      'mathematical_proof_verifier': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
