#!/usr/bin/env python3
"""This audit's custody checker. Does not verify the arbitrary-size theorem."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
from urllib.parse import unquote, urlsplit

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parents[1]
BASE = 'c15a635e17d4be814e19aeeeeb765f3d6024099a'
BEFORE_SHA = 'd10225c0cbbefc8ba9b7cd3ae99515d73ebf1e2bdecc8d873e40b7f7ab21ed46'
PREFIX = AUDIT.relative_to(ROOT).as_posix() + '/'
CLAIM = 'ACCEPTABLE precise scoped paper exclusion; owner adoption pending'
POST_LABELS = {'seal', 'seal-check', 'seal-hashseed17', 'seal-negative', 'boundary-readback'}
POST_NAMES = {label + suffix for label in POST_LABELS for suffix in ('.json', '.stdout.log', '.stderr.log')} | {'REVIEWER_READBACK.json'}
ENVELOPES = {'SEAL.json', 'DELIVERY.json'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def require(value, message):
    if not value:
        raise ValueError(message)

def run(argv):
    r = subprocess.run(argv, cwd=ROOT, capture_output=True, env=os.environ | {'PYTHONDONTWRITEBYTECODE': '1'})
    require(r.returncode == 0, f'command failed {argv!r}: exit={r.returncode}, stderr={r.stderr.decode()!r}')
    return r.stdout

def inventory(directory=AUDIT, excludes=()):
    out = []
    for path in sorted(directory.rglob('*')):
        require(not path.is_symlink(), f'unexpected audit symlink: {path}')
        if not path.is_file():
            continue
        name = path.relative_to(directory).as_posix()
        if name in excludes or (directory == AUDIT and name.startswith('postseal/')):
            continue
        data = path.read_bytes()
        out.append({'path': name, 'sha256': sha(data), 'size': len(data), 'mode': path.stat().st_mode & 0o777})
    return out

def workspace():
    before_bytes = (AUDIT / 'inputs/WORKSPACE_BEFORE.json').read_bytes()
    require(sha(before_bytes) == BEFORE_SHA, 'initial workspace manifest drift')
    before = json.loads(before_bytes)
    require(before['base'] == BASE and before['head'] == BASE and before['initial_status_excluding_new_audit'] == '', 'baseline identity')
    require(run(['git', 'rev-parse', 'HEAD']).decode().strip() == BASE, 'HEAD drift')
    require(run(['git', 'rev-parse', 'main']).decode().strip() == BASE, 'main drift')
    current = {}
    for item in run(['git', 'ls-files', '--stage', '-z']).decode().split('\0'):
        if not item:
            continue
        metadata, path = item.split('\t', 1)
        mode, oid, stage = metadata.split()
        require(stage == '0', 'unmerged index')
        current[path] = {'mode': mode, 'index_oid': oid}
    expected = before['tracked_files'] | before['gitlinks']
    require(current == {p: {'mode': r['mode'], 'index_oid': r['index_oid']} for p, r in expected.items()}, 'tracked/index inventory changed')
    for p, row in before['tracked_files'].items():
        path = ROOT / p
        require(path.is_symlink() == row['symlink'], f'file kind drift {p}')
        data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
        require(sha(data) == row['sha256'] and len(data) == row['size'] and path.lstat().st_mode & 0o777 == row['filesystem_mode'], f'tracked bytes/mode drift {p}')
    for item in run(['git', 'status', '--porcelain=v1', '-z', '--untracked-files=all']).split(b'\0'):
        if item:
            require(item[:2] == b'??' and item[3:].decode().startswith(PREFIX), f'outside authorized additions or staged change: {item!r}')
    require(not run(['git', 'diff', '--name-only']).strip(), 'tracked working diff')
    require(not run(['git', 'diff', '--cached', '--name-only']).strip(), 'staged diff')
    return len(before['tracked_files'])

def receipt(row):
    require(row['exit_code'] == row['expected_exit_code'], f'check expectation mismatch {row["argv"]!r}')
    require(row['cwd'] == str(ROOT), 'receipt working directory drift')
    for field in ('stdout', 'stderr'):
        path = (AUDIT / row[field + '_path']).resolve()
        require(path.is_relative_to(AUDIT), 'receipt path escapes audit')
        require(sha(path.read_bytes()) == row[field + '_sha256'], 'receipt output digest mismatch')

def local_links(precheck=False, allow_pending_seal=False, require_delivery=False):
    helper = runpy.run_path(str(ROOT / 'scripts/check_docs.py'), run_name='adopt_link_helper')
    count = 0
    pending = set()
    if precheck or allow_pending_seal:
        pending.add(AUDIT / 'SEAL.json')
    if precheck or not require_delivery:
        pending.add(AUDIT / 'DELIVERY.json')
    if precheck:
        pending.add(AUDIT / 'final_review/ACCEPTANCE.json')
    for path in sorted(AUDIT.rglob('*.md')):
        for line, destination in helper['links'](path.read_text()):
            url = urlsplit(destination)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.exists() and target in pending and not url.fragment:
                continue
            require(target.exists(), f'missing local link {path}:{line}: {destination}')
            if url.fragment and target.suffix == '.md':
                require(unquote(url.fragment) in helper['anchors'](target.read_text()), f'missing local anchor {path}:{line}')
            count += 1
    for path in AUDIT.rglob('*'):
        if path.is_file() and path.suffix in {'.md', '.py'}:
            require(all(line == line.rstrip() for line in path.read_text().splitlines()), f'trailing whitespace {path}')
    return count

def prerequisites(precheck=False, allow_pending_seal=False, require_delivery=False):
    tracked = workspace()
    historical = json.loads(run([sys.executable, '-B', str(AUDIT / 'agents/custody/independent_immutable_check.py')]))
    require(historical['original_files'] == 160 and historical['publication_files'] == 6 and historical['authority_inputs'] == 31 and historical['old_custody_files'] == 313, 'historical coverage')
    checks = json.loads((AUDIT / 'CHECKS.json').read_text())
    require(checks['base'] == BASE and checks['all_recorded_expectations_met'] is True, 'CHECKS metadata')
    require(checks['commands'], 'no command evidence')
    for row in checks['commands']:
        receipt(row)
    decision = (AUDIT / 'ADOPTION_DECISION.md').read_text()
    require('ACCEPTABLE' in decision and 'OPEN' in decision, 'decision missing exact verdict/boundary')
    count = local_links(precheck, allow_pending_seal, require_delivery)
    if not precheck:
        acceptance = json.loads((AUDIT / 'final_review/ACCEPTANCE.json').read_text())
        reviewed = inventory(excludes=ENVELOPES | {'final_review/ACCEPTANCE.json'})
        require(set(acceptance) == {'schema', 'base', 'reviewer', 'verdict', 'blocking_findings', 'decision', 'parent_status', 'new_unconditional_closures', 'accepted_payload_manifest_sha256', 'accepted_payloads'}, 'final acceptance schema')
        require(acceptance['schema'] == 'br-sd-1g-adopt-final-review-v1' and acceptance['base'] == BASE and acceptance['verdict'] == 'accepted final audit bytes' and acceptance['blocking_findings'] == 0 and acceptance['decision'] == 'ACCEPTABLE' and acceptance['parent_status'] == 'OPEN' and acceptance['new_unconditional_closures'] == 0, 'final reviewer scope')
        require(acceptance['accepted_payloads'] == reviewed and acceptance['accepted_payload_manifest_sha256'] == sha(canonical(reviewed)), 'final reviewer byte drift')
    return {'tracked_entries_unchanged': tracked, 'old_custody_files': 313, 'original_files': 160,
            'publication_files': 6, 'authority_inputs': 31, 'recorded_root_checks': len(checks['commands']), 'local_links_checked': count}

def seal_value(payloads):
    return {'schema': 'br-sd-1g-adopt-seal-v1', 'base': BASE, 'claim': CLAIM, 'decision': 'ACCEPTABLE',
            'parent_status': 'OPEN', 'new_unconditional_closures': 0, 'formal_adoption_executed': False,
            'source_status': 'not triggered', 'new_Lean_theorem': False,
            'payload_manifest_sha256': sha(canonical(payloads)), 'payloads': payloads}

def validate_seal(path):
    payloads = inventory(excludes=ENVELOPES)
    require(json.loads(path.read_text()) == seal_value(payloads), 'seal corruption or payload inventory/hash/mode drift')
    return payloads

def postseal_inventory():
    post = AUDIT / 'postseal'
    rows = inventory(post) if post.exists() else []
    require({r['path'] for r in rows} <= POST_NAMES, 'unrecognized postseal file')
    return rows

def validate_delivery(required=False):
    path = AUDIT / 'DELIVERY.json'
    rows = postseal_inventory()
    if not path.exists():
        require(not required, 'delivery seal not yet created')
        return False
    expected = delivery_value(rows)
    require(json.loads(path.read_text()) == expected, 'delivery receipt inventory/hash/mode drift')
    return True

def delivery_value(rows):
    require({r['path'] for r in rows} == POST_NAMES, 'incomplete final receipt set')
    for label in POST_LABELS:
        row = json.loads((AUDIT / 'postseal' / (label + '.json')).read_text())
        receipt(row)
        relative = AUDIT.relative_to(ROOT).as_posix()
        commands = {
            'seal': ['python3', '-B', relative + '/verify.py', '--seal'],
            'seal-check': ['python3', '-B', relative + '/verify.py', '--check'],
            'seal-hashseed17': ['python3', '-B', relative + '/verify.py', '--check'],
            'seal-negative': ['python3', '-B', relative + '/seal_negative.py'],
            'boundary-readback': ['python3', '-B', relative + '/boundary_readback.py'],
        }
        env = {'PYTHONDONTWRITEBYTECODE': '1'} | ({'PYTHONHASHSEED': '17'} if label == 'seal-hashseed17' else {})
        require(row['argv'] == commands[label] and row['env_overrides'] == env and row['exit_code'] == 0 and row['expected_exit_code'] == 0, 'final receipt command/env/status mismatch: ' + label)
        require(row['stdout_path'] == 'postseal/' + label + '.stdout.log' and row['stderr_path'] == 'postseal/' + label + '.stderr.log', 'final receipt output path mismatch: ' + label)
        require(not (AUDIT / row['stderr_path']).read_bytes(), 'unexpected final command stderr: ' + label)
        output = json.loads((AUDIT / row['stdout_path']).read_text())
        if label in {'seal', 'seal-check', 'seal-hashseed17'}:
            require(output['status'] == 'custody verified' and output['mode'] == ('seal' if label == 'seal' else 'check') and output['base'] == BASE, 'final custody output mismatch')
        elif label == 'seal-negative':
            require(output['status'] == 'triggered and holds' and output['seal_unchanged'] is True and len(output['cases']) == 7 and all(r['exit_code'] == r['expected_exit_code'] == 1 for r in output['cases']), 'seal negative output mismatch')
        else:
            require(output['base'] == output['head'] == output['main'] == BASE and output['tracked_diff'] == '' and output['staged_diff'] == '' and output['only_new_audit_untracked'] is True, 'final boundary readback output mismatch')
    reviewer = json.loads((AUDIT / 'postseal/REVIEWER_READBACK.json').read_text())
    require(reviewer['base'] == BASE and reviewer['decision'] == 'ACCEPTABLE' and reviewer['verdict'] == 'accepted sealed bytes' and reviewer['blocking_findings'] == 0 and reviewer['seal_sha256'] == sha((AUDIT / 'SEAL.json').read_bytes()) and reviewer['reviewed_final_payload_manifest_sha256'] == json.loads((AUDIT / 'SEAL.json').read_text())['payload_manifest_sha256'], 'reviewer seal readback')
    return {'schema': 'br-sd-1g-adopt-delivery-v1', 'base': BASE, 'seal_sha256': sha((AUDIT / 'SEAL.json').read_bytes()),
            'decision': 'ACCEPTABLE', 'parent_status': 'OPEN', 'new_unconditional_closures': 0,
            'postseal_manifest_sha256': sha(canonical(rows)), 'postseal_payloads': rows}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    for mode in ('precheck', 'seal', 'check', 'seal-delivery'):
        g.add_argument('--' + mode, action='store_true')
    p.add_argument('--seal-path', type=Path)
    p.add_argument('--require-delivery', action='store_true')
    a = p.parse_args()
    require(not a.seal_path or a.check, 'alternate seal only for check')
    require(not a.require_delivery or a.check, 'require-delivery only for check')
    counts = prerequisites(a.precheck, a.seal, a.require_delivery)
    if a.precheck:
        mode = 'precheck'
    elif a.seal:
        require(not (AUDIT / 'DELIVERY.json').exists(), 'delivery exists before seal')
        value = seal_value(inventory(excludes=ENVELOPES))
        with (AUDIT / 'SEAL.json').open('x') as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write('\n')
        mode = 'seal'
    else:
        validate_seal(a.seal_path or AUDIT / 'SEAL.json')
        if a.seal_delivery:
            value = delivery_value(postseal_inventory())
            with (AUDIT / 'DELIVERY.json').open('x') as stream:
                json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
                stream.write('\n')
            mode = 'seal-delivery'
        else:
            validate_delivery(a.require_delivery)
            mode = 'check'
    print(json.dumps({'status': 'custody verified', 'mode': mode, 'base': BASE, 'decision': 'ACCEPTABLE',
                      'formal_adoption_executed': False, 'parent_status': 'OPEN', 'new_unconditional_closures': 0,
                      'source_status': 'not triggered', 'new_Lean_theorem': False, **counts}, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
