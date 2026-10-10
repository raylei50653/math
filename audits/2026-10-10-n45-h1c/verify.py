#!/usr/bin/env python3
"""Read-only H1C exact seal gate and independent frozen worker replay."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SEAL_FILES = ['seal-checks/' + name + '.' + suffix
              for name in ('normal', 'seed17', 'bad-digest')
              for suffix in ('stdout.txt', 'stderr.txt', 'json')] + ['seal-checks/receipt.json']
EXCLUDED = set(['MANIFEST.sha256', 'delivery.json'] + SEAL_FILES)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def safe(name):
    p = PurePosixPath(name)
    need(name and '\\' not in name and not p.is_absolute() and all(x not in ('.', '..') for x in p.parts) and p.as_posix() == name, 'unsafe seal path')
    return name


def payload_gate(data):
    saved = {}
    for line in data.decode().splitlines():
        h, name = line.split('  ', 1)
        need(len(h) == 64 and all(c in '0123456789abcdef' for c in h), 'invalid seal digest')
        safe(name)
        need(name not in saved, 'duplicate seal path')
        saved[name] = h
    current = {}
    for p in sorted(HERE.rglob('*')):
        need(not p.is_symlink(), 'symlink in audit seal')
        if p.is_file():
            name = p.relative_to(HERE).as_posix()
            if name not in EXCLUDED:
                current[name] = sha(p)
    need(list(saved) == sorted(saved), 'seal order')
    need(set(saved) == set(current), 'audit payload inventory')
    for name in saved:
        need(saved[name] == current[name], 'audit payload digest differs: ' + name)
    return len(saved)


def receipt_gate(count):
    d = json.loads((HERE / 'delivery.json').read_bytes())
    need(d['task'] == 'N45-H1C' and d['decision'] == 'accepted_artifact_integrity_only', 'audit delivery identity/scope')
    need(d['manifest_file'] == 'MANIFEST.sha256' and d['manifest_sha256'] == sha(HERE / 'MANIFEST.sha256'), 'audit manifest binding')
    need(d['payload_files'] == count and set(d['seal_files']) == set(SEAL_FILES), 'audit exact receipt exclusions')
    for name, h in d['seal_files'].items():
        need(sha(HERE / safe(name)) == h, 'audit receipt-bound metadata: ' + name)
    r = json.loads((HERE / 'seal-checks/receipt.json').read_bytes())
    need(r['manifest_sha256'] == d['manifest_sha256'] and r['payload_files'] == count and r['payload_before_after_identical'], 'audit receipt payload custody')
    runs = r['runs']
    need(len(runs) == 3 and {x['id'] for x in runs} == {'normal', 'seed17', 'bad-digest'}, 'audit receipt actual run coverage')
    by_id = {x['id']: x for x in runs}
    for name, expected, env in [('normal', 0, {}), ('seed17', 0, {'PYTHONHASHSEED': '17'}), ('bad-digest', 2, {})]:
        q = by_id[name]
        need(q['actual_exit'] == q['expected_exit'] == expected and q['environment'] == env and q['cwd'] == str(ROOT), 'audit actual replay identity')
        need(json.loads((HERE / ('seal-checks/' + name + '.json')).read_bytes()) == q, 'audit nested run receipt')
        for stream in ('stdout', 'stderr'):
            need(q[stream + '_file'] == 'seal-checks/' + name + '.' + stream + '.txt'
                 and sha(HERE / q[stream + '_file']) == q[stream + '_sha256'], 'audit actual stream binding')
    for name in ('normal', 'seed17'):
        need(by_id[name]['command'] == ['python3','-B','audits/2026-10-10-n45-h1c/verify.py','--payload-only'], 'audit replay command')
    for stream in ('stdout', 'stderr'):
        need((HERE / by_id['normal'][stream + '_file']).read_bytes() == (HERE / by_id['seed17'][stream + '_file']).read_bytes(), 'audit normal/seed17 bytes')
    bad = by_id['bad-digest']
    need(bad['command'] == ['python3','-B','audits/2026-10-10-n45-h1c/verify.py','--payload-only','--manifest-stdin'], 'audit negative command')
    reject = json.loads((HERE / bad['stderr_file']).read_bytes())
    need(reject['stage'] == 'audit payload inventory' and 'digest differs' in reject['reason'], 'audit negative digest stage')
    judgment = json.loads((HERE / 'independent-judgment.json').read_bytes())
    need(judgment['decision'] == 'accepted_artifact_integrity_only' and judgment['paper_mathematics'] == 'not adjudicated'
         and judgment['finite_HIGH1_source'] == 'not established / not executed / no trigger count', 'audit evidence boundary')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--payload-only', action='store_true')
    p.add_argument('--manifest-stdin', action='store_true')
    a = p.parse_args()
    stage = 'audit payload inventory'
    try:
        data = sys.stdin.buffer.read() if a.manifest_stdin else (HERE / 'MANIFEST.sha256').read_bytes()
        count = payload_gate(data)
        if not a.payload_only:
            stage = 'audit delivery/receipt exact binding'
            receipt_gate(count)
        stage = 'frozen worker replay'
        r = subprocess.run(['python3','-B',str(HERE / 'checker.py')], cwd=ROOT, capture_output=True)
        sys.stdout.buffer.write(r.stdout)
        sys.stderr.buffer.write(r.stderr)
        return r.returncode
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(json.dumps(dict(status='REJECT', stage=stage, reason=str(e)), sort_keys=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
