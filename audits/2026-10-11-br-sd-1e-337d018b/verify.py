#!/usr/bin/env python3
"""Read-only custody, final-review bindings and local-link verification.

This verifier establishes bytes and recorded control results, not mathematics.
The arbitrary-size theorem is in PROOF.md and its independent paper review.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote

AUDIT = Path(__file__).resolve().parent
REPO = AUDIT.parent.parent
BASE = '337d018bfaddfe6b39f7cdc3f3c8ec8bc7c4075f'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(*args):
    return subprocess.check_output(args, cwd=REPO)


def old_paths():
    paths = []
    for directory in sorted((REPO / 'audits').glob('*br-sd-1[abcd]*')):
        paths.extend(p for p in sorted(directory.rglob('*')) if p.is_file())
    paths.extend(sorted((REPO / 'docs/history').glob('*br-sd-1[abcd]*')))
    return paths


def local_links():
    checked = 0
    for path in sorted(AUDIT.rglob('*.md')):
        source = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', source):
            target = target.strip().strip('<>')
            if re.match(r'^[a-z]+:', target) or target.startswith('#'):
                continue
            target = unquote(target.split('#', 1)[0])
            assert (path.parent / target).exists(), f'missing local link: {path}: {target}'
            checked += 1
        assert all(line.rstrip() == line for line in path.read_text().splitlines()), f'trailing whitespace: {path}'
    return checked


def verify(manifest_path, live):
    seal = json.loads(manifest_path.read_text())
    assert seal['task'] == 'BR-SD-1e' and seal['base'] == BASE
    paths = [record['path'] for record in seal['payloads']]
    assert len(paths) == len(set(paths)), 'duplicate seal path'
    assert paths == sorted(paths), 'noncanonical seal order'
    excluded = {'seal-v1.json', 'validation/final.json', 'validation/seal.corrupted.json'}
    assert set(seal['unsealed_postseal_outputs']) == excluded - {'seal-v1.json'}
    actual_paths = {str(p.relative_to(AUDIT)) for p in AUDIT.rglob('*') if p.is_file()}
    assert actual_paths - excluded == set(paths), 'unlisted or missing audit payload'
    for record in seal['payloads']:
        relative = Path(record['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        path = AUDIT / relative
        assert path.is_file() and not path.is_symlink(), f'absent payload: {relative}'
        assert path.stat().st_size == record['size'] and sha(path) == record['sha256'], f'payload drift: {relative}'
    authority = json.loads((AUDIT / 'authority/INPUTS.json').read_text())
    assert authority['base'] == authority['head'] == authority['origin_main'] == BASE
    assert authority['remote_main'].split()[0] == BASE
    assert authority['head_base_diff'] == ''
    for record in authority['inputs']:
        frozen = AUDIT / record['snapshot']
        assert sha(frozen) == record['sha256']
        assert command('git', 'show', BASE + ':' + record['path']) == frozen.read_bytes(), 'BASE input mismatch'
        if live:
            assert sha(REPO / record['path']) == record['sha256'], 'live authority drift'
    custody = json.loads((AUDIT / 'authority/OLD-CUSTODY.json').read_text())
    assert [str(p.relative_to(REPO)) for p in old_paths()] == [r['path'] for r in custody], 'old custody path drift'
    for record in custody:
        path = REPO / record['path']
        assert path.stat().st_size == record['size'] and sha(path) == record['sha256'], 'old archive byte drift'
        assert path.stat().st_mode & 0o777 == record['mode'], 'old archive mode drift'
    controls = AUDIT / 'agents/controls'
    assert (controls / 'certificate.v2.normal.json').read_bytes() == (controls / 'certificate.v2.seed17.json').read_bytes()
    assert sha(controls / 'certificate.v2.normal.json') == 'df640b4b5a60929ccd5d1fda4a8018876fff34ff83221d0a92ba3838e41c6705'
    receipt = json.loads((AUDIT / 'validation/root-replay.v2.json').read_text())
    assert len(receipt) == 13 and len({r['name'] for r in receipt}) == 13
    assert all(r['matched'] and r['result']['exit_code'] == r['expected'] for r in receipt)
    acceptance = json.loads((AUDIT / 'agents/paper/ACCEPTANCE.json').read_text())
    assert acceptance['verdict'] == 'accepted candidate scoped exclusion'
    assert set(acceptance['accepted_files']) == {'PROOF.md', 'REPORT.md', 'MAPPING.md'}
    for relative, digest in acceptance['accepted_files'].items():
        assert sha(AUDIT / relative) == digest, 'final paper-review binding drift'
    links = local_links()
    if live:
        assert command('git', 'rev-parse', 'HEAD').decode().strip() == BASE, 'HEAD advanced'
        assert command('git', 'rev-parse', 'refs/remotes/origin/main').decode().strip() == BASE, 'tracking main advanced'
        remote = command('git', 'ls-remote', 'origin', 'refs/heads/main').decode().strip()
        assert remote.split()[0] == BASE, 'remote main advanced'
        assert command('git', 'diff', '--name-only') == b'', 'tracked working-tree edits'
        assert command('git', 'diff', '--cached', '--name-only') == b'', 'index edits'
        allowed = str(AUDIT.relative_to(REPO)) + '/'
        status = command('git', 'status', '--porcelain=v1', '-z').decode()
        assert all(item.startswith('?? ' + allowed) for item in status.split('\0') if item), 'writes outside exclusive audit'
    return {'task': 'BR-SD-1e', 'base': BASE, 'live': live,
            'payloads_verified': len(paths), 'authority_inputs_verified': len(authority['inputs']),
            'old_custody_files_verified': len(custody), 'local_link_targets_checked': links,
            'recorded_checks_verified': len(receipt),
            'final_paper_review_bindings': 'matched', 'actual_target_source_status': 'not triggered',
            'scope': 'byte custody and recorded checks only; paper theorem separately reviewed'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--manifest', type=Path, default=AUDIT / 'seal-v1.json')
    args = parser.parse_args()
    print(json.dumps(verify(args.manifest, args.live), sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, OSError, ValueError, KeyError, TypeError, IndexError, subprocess.CalledProcessError) as error:
        raise SystemExit('FAIL: ' + str(error))
