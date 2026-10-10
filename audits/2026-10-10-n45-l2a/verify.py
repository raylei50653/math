#!/usr/bin/env python3
"""Read-only integrity verifier. Paper proofs and source existence are not checked."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'
META = {'receipt.json', 'seal/commands.json', 'seal/normal.stdout.log',
        'seal/normal.stderr.log', 'seal/seed17.stdout.log', 'seal/seed17.stderr.log'}
EXCLUDED = {'MANIFEST.sha256', 'delivery.json'} | META
IDS = ['LOW2-CORE', 'LOW2-COMP', 'LOW2-JOIN', 'LOW2-F', 'LOW2-MAP', 'LOW2-EXCLUSION']


def require(test, message):
    if not test:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(rel):
    return json.loads((HERE / rel).read_text())


def inventory():
    files, links = [], {}
    for p in HERE.rglob('*'):
        rel = p.relative_to(HERE).as_posix()
        if rel in EXCLUDED:
            continue
        if p.is_symlink():
            links[rel] = os.readlink(p)
        elif p.is_file():
            files.append(rel)
    return sorted(files), links


def verify(payload_only=False):
    files, links = inventory()
    require(not links, 'unexpected symlink')
    records = {}
    for line in (HERE / 'MANIFEST.sha256').read_text().splitlines():
        m = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(m is not None, 'manifest syntax')
        digest, rel = m.groups()
        require(not Path(rel).is_absolute() and '..' not in Path(rel).parts, 'manifest unsafe path')
        require(rel not in records, 'manifest duplicate path')
        records[rel] = digest
    require(sorted(records) == files, 'manifest exact inventory')
    for rel, digest in records.items():
        require(sha(HERE / rel) == digest, 'manifest digest differs: ' + rel)
    inputs = read('inputs.json')
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    require(head == inputs['head'] == inputs['BASE'] == BASE, 'BASE/head differs')
    for rec in inputs['inputs']:
        require(sha(HERE / rec['frozen']) == rec['sha256'], 'frozen input differs: ' + rec['source'])
        if rec['live_immutable']:
            require(sha(ROOT / rec['source']) == rec['sha256'], 'immutable old input differs: ' + rec['source'])
    for rec in inputs['base_inputs']:
        raw = subprocess.check_output(['git', 'show', BASE + ':' + rec['path']], cwd=ROOT)
        require(hashlib.sha256(raw).hexdigest() == rec['sha256'], 'BASE digest differs')
        blob = subprocess.check_output(['git', 'rev-parse', BASE + ':' + rec['path']], cwd=ROOT).decode().strip()
        require(blob == rec['git_blob'], 'BASE object differs')
        require((HERE / rec['frozen']).read_bytes() == raw, 'frozen BASE bytes differ')
    source = read('external/source.json')
    require(sha(HERE / 'external/gallai-official.pdf') == source['sha256'], 'official PDF differs')
    require(source['HTTP_status'] == 200 and source['byte_equal_BASE'], 'external intake failed')
    j, w = read('independent-judgment.json'), read('frozen/worker/claims.json')
    require([c['id'] for c in j['claims']] == IDS, 'claim inventory differs')
    for c, original in zip(j['claims'], w['claims']):
        require(c['source_contract'] == original['source_contract'] and len(c['source_contract']) == 12,
                'full source contract not retained')
        require(c['verdict'] == 'holds_under_full_LOW2_source_contract' and not c['machine_proved'],
                'evidence layer differs')
    require(j['composition']['uncovered_cases'] == [], 'composition judgment differs')
    require([(c['original_U_incidence'], c['original_r_spokes']) for c in j['composition']['case_mapping']]
            == [(1, 2), (2, 1)], 'separate coverage case mapping differs')
    require(j['source_control_evaluation'] == 'not established; not executed; no trigger count'
            and not j['new_finite_source_control'] and not j['new_Lean'] and not j['peer_judgments_read'],
            'scope/evidence boundary differs')
    text = (HERE / 'REPORT.md').read_text()
    without_code = re.sub(r'```.*?```|`[^`\n]*`', '', text, flags=re.S)
    local_links = 0
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', without_code):
        if target.startswith(('http://', 'https://', '#')):
            continue
        rel = target.split('#')[0]
        require((HERE / rel).is_file(), 'report local link missing: ' + target)
        local_links += 1
    for rel in ('REPORT.md', 'verify.py', 'seal.py', 'independent-judgment.json', 'task.json', 'inputs.json'):
        b = (HERE / rel).read_bytes()
        require(b.endswith(b'\n') and not any(x.rstrip(b' \t') != x for x in b.splitlines()),
                'authored whitespace differs: ' + rel)
    if not payload_only:
        delivery, receipt = read('delivery.json'), read('receipt.json')
        require(delivery['manifest_file'] == 'MANIFEST.sha256'
                and delivery['manifest_sha256'] == sha(HERE / 'MANIFEST.sha256'), 'delivery manifest binding differs')
        require(set(delivery['receipt_bound_metadata']) == META, 'receipt-bound metadata inventory differs')
        for rel, digest in delivery['receipt_bound_metadata'].items():
            require(sha(HERE / rel) == digest, 'receipt-bound metadata differs: ' + rel)
        commands = read('seal/commands.json')
        require(commands == receipt['commands'], 'receipt command records differ')
        require(set(commands) == {'normal', 'seed17'}, 'replay inventory differs')
        for label, rec in commands.items():
            require(rec['exit'] == 0 and rec['phase'] == 'payload_only_before_receipt', 'actual replay failed')
            require(rec['stdout_sha256'] == sha(HERE / ('seal/' + label + '.stdout.log'))
                    and rec['stderr_sha256'] == sha(HERE / ('seal/' + label + '.stderr.log')), 'logged replay differs')
        require((HERE / 'seal/normal.stdout.log').read_bytes() == (HERE / 'seal/seed17.stdout.log').read_bytes(),
                'hashseed replay output differs')
        require(receipt['payload_before'] == receipt['payload_after'] == records, 'replay payload drift')
        require(delivery['payload_files'] == len(records), 'receipt count differs')
    return {'task': 'N45-L2A', 'status': 'sealed_integrity_holds', 'payload_files': len(records),
            'frozen_inputs': len(inputs['inputs']), 'BASE_blobs': len(inputs['base_inputs']),
            'claims': len(IDS), 'composition': 'separately adjudicated, scoped LOW only',
            'report_local_links': local_links, 'paper_proved_by_tool': False,
            'new_finite_source_controls': False, 'new_Lean': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--payload-only', action='store_true')
    args = p.parse_args()
    try:
        print(json.dumps(verify(args.payload_only), sort_keys=True))
    except (OSError, ValueError, subprocess.SubprocessError, KeyError) as exc:
        print('integrity rejection: ' + str(exc), file=sys.stderr)
        raise SystemExit(2)
