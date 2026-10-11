#!/usr/bin/env python3
"""Read-only byte custody. Mathematical conclusions require the paper review."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', required=True)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--manifest', type=Path, default=AUDIT / 'seal-v1.json')
    args = parser.parse_args()
    seal = json.loads(args.manifest.read_text())
    authority = json.loads((AUDIT / 'authority.json').read_text())
    require(seal['base'] == authority['base'], 'base mismatch')
    require(bool(seal['payloads']), 'empty payload list')
    seen = set()
    for entry in seal['payloads']:
        path = (AUDIT / entry['path']).resolve()
        require(path.is_relative_to(AUDIT), 'payload escapes audit')
        require(entry['path'] not in seen, 'duplicate payload')
        seen.add(entry['path'])
        data = path.read_bytes()
        require(len(data) == entry['bytes'] and digest(data) == entry['sha256'], 'payload drift: ' + entry['path'])
    for entry in authority['input_files']:
        data = (AUDIT / 'authority' / entry['path']).read_bytes()
        blob = subprocess.check_output(['git', 'show', authority['base'] + ':' + entry['path']], cwd=ROOT)
        require(data == blob and digest(data) == entry['sha256'] and len(data) == entry['bytes'], 'frozen authority drift: ' + entry['path'])
    if args.live:
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        require(head == authority['base'], 'live HEAD changed')
        for entry in authority['input_files'] + authority['prior_br_sd_1a_files']:
            data = (ROOT / entry['path']).read_bytes()
            require(digest(data) == entry['sha256'] and len(data) == entry['bytes'], 'live input/custody drift: ' + entry['path'])
        require(not subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT), 'tracked working-tree diff')
        require(not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT), 'index diff')
        untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
        prefix = str(AUDIT.relative_to(ROOT)) + '/'
        require(all(p.startswith(prefix) for p in untracked), 'untracked output outside exclusive audit')
    print(json.dumps({'payloads': len(seen), 'authority_inputs': len(authority['input_files']), 'base': seal['base'], 'live': args.live, 'prior_custody_files': len(authority['prior_br_sd_1a_files']) if args.live else None}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise SystemExit('FAIL: ' + str(exc))
