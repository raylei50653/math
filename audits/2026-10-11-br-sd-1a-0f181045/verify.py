#!/usr/bin/env python3
"""Read-only byte custody and optional live boundary check for BR-SD-1a.
This verifies archive integrity, not the unbounded mathematical theorem.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def frozen_checks():
    authority = json.loads((HERE / 'authority-v2.json').read_text())
    require(authority['schema'] == 'BR-SD-1a-authority-v2', 'authority schema')
    inputs = authority['inputs']
    require(len(inputs) == 14 and len({x['path'] for x in inputs}) == 14, '14 unique authority inputs')
    for item in inputs:
        rel = item['path']
        data = (HERE / 'authority/current' / rel).read_bytes()
        require(len(data) == item['current_size'], f'current input size: {rel}')
        require(digest(data) == item['current_sha256'], f'current input hash: {rel}')
        head = subprocess.check_output(['git', 'show', f"{authority['actual_head']}:{rel}"], cwd=ROOT)
        require(digest(head) == item['head_git_sha256'] == item['current_sha256'], f'execution-head input: {rel}')
        base = subprocess.run(['git', 'show', f"{authority['source_base']}:{rel}"], cwd=ROOT, capture_output=True)
        require((base.returncode == 0) == item['base_present'], f'BASE presence: {rel}')
        if item['base_present']:
            saved = (HERE / 'authority/base' / rel).read_bytes()
            require(saved == base.stdout, f'BASE frozen bytes: {rel}')
            require(digest(saved) == item['base_sha256'], f'BASE hash: {rel}')
            require(len(saved) == item['base_size'], f'BASE size: {rel}')
        else:
            require(not (HERE / 'authority/base' / rel).exists(), f'false BASE reconstruction: {rel}')
    external = json.loads((HERE / 'external/download.json').read_text())
    data = (HERE / 'external/gallai.pdf').read_bytes()
    require(digest(data) == external['sha256'] == '50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea', 'external PDF hash')
    require(len(data) == external['size'] == 164927, 'external PDF size')
    return authority


def seal_checks(manifest_path):
    manifest = json.loads(manifest_path.read_text())
    require(manifest['schema'] == 'BR-SD-1a-seal-v1', 'seal schema')
    require(manifest['task'] == 'BR-SD-1a', 'seal task')
    names = [x['path'] for x in manifest['payloads']]
    require(names and len(names) == len(set(names)), 'unique nonempty payloads')
    for item in manifest['payloads']:
        rel = Path(item['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'relative payload path')
        file = HERE / rel
        require(file.is_file() and not file.is_symlink(), f'regular payload: {rel}')
        data = file.read_bytes()
        require(len(data) == item['size'] and digest(data) == item['sha256'], f'seal mismatch: {rel}')
    mandatory = {'REPORT.md', 'PROOF.md', 'authority-v2.json', 'prior-custody.json', 'verify.py',
                 'external/SOURCE.md', 'external/gallai.pdf', 'agents/paper/REVIEW.md',
                 'agents/mapping/MAPPING.md', 'agents/mapping/mapping.json', 'agents/controls/checker.py',
                 'agents/controls/REPORT.v2.md', 'agents/controls/certificate.normal.json',
                 'independent_fibres.py', 'checks-root-v1.json'}
    require(mandatory.issubset(names), 'missing mandatory payloads')
    return len(names)


def live_checks(authority):
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    require(head == authority['actual_head'], 'live HEAD changed')
    for item in authority['inputs']:
        require(digest((ROOT / item['path']).read_bytes()) == item['current_sha256'], f"live authority drift: {item['path']}")
    custody = json.loads((HERE / 'prior-custody.json').read_text())
    expected = {x['path']: x for x in custody['files']}
    actual = set()
    for directory in custody['root_directories']:
        for file in (ROOT / directory).rglob('*'):
            if file.is_file() and not file.is_symlink():
                actual.add(file.relative_to(ROOT).as_posix())
    require(actual == set(expected), 'prior audit file membership changed')
    for rel, item in expected.items():
        data = (ROOT / rel).read_bytes()
        require(len(data) == item['size'] and digest(data) == item['sha256'], f'prior audit drift: {rel}')
    tracked = subprocess.run(['git', 'diff', '--exit-code', 'HEAD', '--'], cwd=ROOT, capture_output=True)
    require(tracked.returncode == 0, 'tracked worktree or index changed')
    untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z'], cwd=ROOT)
    prefix = HERE.relative_to(ROOT).as_posix() + '/'
    outside = [x.decode() for x in untracked.split(bytes([0])) if x and not x.decode().startswith(prefix)]
    require(not outside, f'untracked files outside exclusive directory: {outside}')
    return len(expected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--manifest', type=Path, default=HERE / 'seal-v1.json')
    args = parser.parse_args()
    authority = frozen_checks()
    count = seal_checks(args.manifest.resolve())
    result = {'task': 'BR-SD-1a', 'payloads_verified': count, 'authority_inputs_verified': 14,
              'source_base': authority['source_base'], 'actual_head': authority['actual_head'],
              'target_source_status': 'not triggered', 'scope': 'byte custody only; paper theorem is separately reviewed'}
    if args.live:
        result['prior_files_verified_unchanged'] = live_checks(authority)
        result['exclusive_write_boundary'] = 'holds'
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
