#!/usr/bin/env python3
"""Read-only delivery integrity; does not prove the paper or a source theorem."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
TOP_EXCLUSIONS = {'MANIFEST.final-v2.sha256', 'delivery.json'}


def sha(path):
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text())


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def inventory():
    prefix = HERE.relative_to(ROOT).as_posix() + '/'
    return sorted({p.decode() for p in git('ls-files', '--cached', '--others',
                                          '--exclude-standard', '-z').split(b'\0')
                   if p and not p.decode().startswith(prefix)})


def payload_inventory():
    regular, symlinks = [], {}
    for path in sorted(HERE.rglob('*')):
        relative = path.relative_to(HERE).as_posix()
        if relative in TOP_EXCLUSIONS or relative.startswith('seal-final-v2/'):
            continue
        if path.is_symlink():
            symlinks[relative] = os.readlink(path)
        elif path.is_file():
            regular.append(relative)
    return regular, symlinks


def verify_manifest(path):
    expected_regular, expected_links = payload_inventory()
    records = {}
    for number, line in enumerate(path.read_text().splitlines(), 1):
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, f'malformed manifest line {number}')
        digest, relative = match.groups()
        require(not Path(relative).is_absolute() and '..' not in Path(relative).parts,
                f'unsafe manifest path: {relative}')
        require(relative not in records, f'duplicate manifest path: {relative}')
        records[relative] = digest
    require(sorted(records) == sorted(expected_regular), 'manifest payload inventory differs')
    require(expected_links == read_json(HERE / 'symlinks.json'), 'payload symlink identities differ')
    for relative, expected in sorted(records.items()):
        require(sha(HERE / relative) == expected, f'manifest digest differs: {relative}')
    return len(records), len(expected_links)


def check_live():
    require(git('rev-parse', 'HEAD').decode().strip() == BASE, 'workspace HEAD differs from BASE')
    old = read_json(HERE / 'preexisting-files.json')
    require(inventory() == sorted(old), 'pre-existing workspace inventory differs')
    for relative, record in sorted(old.items()):
        path = ROOT / relative
        if record['kind'] == 'symlink':
            require(path.is_symlink() and os.readlink(path) == record['target'], f'live symlink differs: {relative}')
        elif record['kind'] == 'missing':
            require(not path.exists() and not path.is_symlink(), f'previously missing file appeared: {relative}')
        else:
            require(path.is_file() and not path.is_symlink() and sha(path) == record['sha256'],
                    f'pre-existing file differs: {relative}')
    require(git('diff', '--binary') == (HERE / 'logs/initial-tracked-diff.stdout.log').read_bytes(),
            'pre-existing tracked diff differs')
    require(git('diff', '--cached', '--binary') == (HERE / 'logs/initial-cached-diff.stdout.log').read_bytes(),
            'pre-existing staged diff differs')
    initial = read_json(HERE / 'inputs-initial.json')
    require(initial['head'] == BASE and initial['head_matches'], 'initial HEAD record differs')
    for pin in initial['pins']:
        require(pin['matches'] and pin['actual'] == pin['expected'], f'initial task pin failed: {pin["path"]}')
        require(sha(ROOT / pin['path']) == pin['expected'], f'live task pin differs: {pin["path"]}')
        require(sha(HERE / 'frozen/current' / pin['path']) == pin['expected'], f'frozen task pin differs: {pin["path"]}')
    for item in read_json(HERE / 'base-inputs.json')['inputs']:
        blob = git('show', f'{BASE}:{item["path"]}')
        require(hashlib.sha256(blob).hexdigest() == item['sha256'], f'BASE blob digest differs: {item["path"]}')
        require(git('rev-parse', f'{BASE}:{item["path"]}').decode().strip() == item['git_blob'],
                f'BASE blob object differs: {item["path"]}')
        require((HERE / 'base-source' / item['path']).read_bytes() == blob,
                f'BASE archive input differs: {item["path"]}')
    return len(old), len(initial['pins'])


def check_authored():
    claims = read_json(HERE / 'claims.json')
    ids = ['LOW1-CORE', 'LOW1-COMP', 'LOW1-JOIN', 'LOW1-F', 'LOW1-MAP', 'LOW1-EXCLUSION']
    require([c['id'] for c in claims['claims']] == ids, 'claim inventory differs')
    require(claims['delivery_status'] == 'candidate_only_not_adopted', 'candidate status differs')
    require(claims['source_controls'] == [] and claims['source_control_evaluation'].startswith('not performed'),
            'unperformed source controls misclassified')
    for claim in claims['claims']:
        require(claim['source_contract'] == claims['full_source_contract'], f'incomplete claim contract: {claim["id"]}')
        require(set(claim['dependencies']) <= set(ids), f'unknown claim dependency: {claim["id"]}')
    future = {'delivery.json', 'seal-final-v2/commands.json'}
    text = (HERE / 'REPORT.md').read_text()
    text = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)
    for destination in re.findall(r'\]\(([^\s)]+)\)', text):
        if '://' in destination:
            continue
        if destination in future and not (HERE / destination).exists():
            continue
        require((HERE / destination.split('#', 1)[0]).exists(), f'missing report link: {destination}')
    authored = ['REPORT.md', 'claims.json', 'verify.py', 'prepare.py', 'checks_runner.py', 'checks.json']
    for relative in authored:
        data = (HERE / relative).read_text()
        require(data.endswith('\n'), f'authored text lacks newline: {relative}')
        require(all(line.rstrip(' \t') == line for line in data.splitlines()), f'authored trailing whitespace: {relative}')
    external = read_json(HERE / 'external-source-check.json')
    require(external['byte_equal'] and external['base_sha256'] == external['official_sha256'],
            'official Gallai PDF does not match frozen BASE')


def check_delivery():
    delivery = read_json(HERE / 'delivery.json')
    require(delivery['manifest_sha256'] == sha(HERE / 'MANIFEST.final-v2.sha256'), 'delivery manifest binding differs')
    require(delivery['paper_status'] == 'candidate_pending_independent_adjudication', 'delivery adoption status differs')
    seal_files = sorted(p.relative_to(HERE).as_posix() for p in (HERE / 'seal-final-v2').rglob('*') if p.is_file())
    require(seal_files == sorted(delivery['seal_files']), 'unbound seal-check file or missing receipt')
    for relative, digest in sorted(delivery['seal_files'].items()):
        require(sha(HERE / relative) == digest, f'seal receipt digest differs: {relative}')
    commands = read_json(HERE / 'seal-final-v2/commands.json')
    require(all(x['exit_code'] == x['expected_exit'] for x in commands['commands']), 'seal command exit differs')
    require(commands['normal_seed17_stdout_byte_equal'], 'normal/seed17 outputs differ')
    require(commands['negative_detected_digest_mismatch'], 'negative control did not detect the corrupted digest')
    before = read_json(HERE / 'seal-final-v2/payload-before.json')
    after = read_json(HERE / 'seal-final-v2/payload-after.json')
    require(before == after, 'read-only verification or negative control changed payload')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=HERE / 'MANIFEST.final-v2.sha256')
    parser.add_argument('--payload-only', action='store_true', help='Sealing stage: verify payload, skip not-yet-created delivery receipt')
    args = parser.parse_args()
    try:
        regular, symlinks = verify_manifest(args.manifest)
        live, pins = check_live()
        check_authored()
        if not args.payload_only:
            check_delivery()
        print(json.dumps(dict(status='artifact_integrity_holds', regular_payload_files=regular,
                              payload_symlinks=symlinks, live_preexisting_files=live, task_pins=pins,
                              paper_proved_by_this_tool=False, finite_source_controls='not evaluated',
                              receipt_checked=not args.payload_only), sort_keys=True))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f'integrity rejection: {error}', file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
