#!/usr/bin/env python3
"""Replay v2 and exercise the CLI with reconstructible corruptions.

Negative files are temporary local copies; recipes and byte digests are retained
in VALIDATION.json. Logs/output are exclusively created. No shared file writes.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CERT = HERE / 'certificate.v2.json'
TAG = ''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    protected = [p for p in ROOT.rglob('*') if p.is_file() and
                 ('frozen' in p.relative_to(ROOT).parts or p.suffix == '.py' or
                  p.name in ('INPUTS.json', 'DESIGN.json', 'domain.json', 'CONTRACT.md',
                             'certificate.json', 'certificate.v2.json'))]
    return {str(p.relative_to(ROOT)): sha(p) for p in protected}


def run(name, command, expected_code=0, env=None, cwd=None):
    result = subprocess.run(command, capture_output=True, text=True, env=env, cwd=cwd)
    log = ROOT / 'logs' / ((TAG + '-' if TAG else '') + name + '.log')
    with log.open('x') as f:
        f.write(result.stdout + result.stderr)
    if result.returncode != expected_code:
        raise ValueError(f'{name}: exit {result.returncode}, expected {expected_code}; see {log}')
    print(name, 'PASS', flush=True)
    return {'name': name, 'exit_code': result.returncode,
            'expected_exit_code': expected_code, 'log': str(log.relative_to(ROOT))}


def main():
    global TAG
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag', default='', help='new output tag; existing logs/results are never overwritten')
    args = parser.parse_args()
    if not re.fullmatch('[a-z0-9_-]*', args.tag):
        raise ValueError('tag must contain only lowercase letters, digits, underscore or hyphen')
    TAG = args.tag
    before = snapshot()
    python = [sys.executable, '-B']
    command = python + [str(HERE / 'check.py'), '--check', str(CERT)]
    records = [run('replay-normal', command)]
    records.append(run('replay-seed17-other-cwd', command + ['--seed', '17'],
                       env=os.environ | {'PYTHONHASHSEED': '17'}, cwd='/tmp'))
    upstream = ROOT / 'frozen/audits/2026-10-12-cofacial-uniform-separation-eb6b2303'
    records.append(run('inherited-cofacial-v2', python + [str(upstream / 'controls/checker.py'),
                       '--check', str(upstream / 'controls/certificate.v2.json')]))
    records.append(run('negative-exclusive-write', python + [str(HERE / 'check.py'),
                       '--write', str(CERT)], expected_code=1))
    original = json.loads(CERT.read_text())
    mutations = [
        ('missing-row', 'remove last row from graphs.W5.rows'),
        ('wrong-label', 'replace W5 boundary label b4 by b0 in embedded domain'),
        ('wrong-lift', 'set W5 row0 first lift color at b0 equal to b1'),
        ('illegal-quotient', 'replace first admitted quotient partition by a block merging b0 and b1'),
        ('missing-empty-fibre', 'remove empty truth-value fibre 00 from first operation row'),
    ]
    negatives = []
    for name, recipe in mutations:
        bad = copy.deepcopy(original)
        if name == 'missing-row':
            bad['graphs']['W5']['rows'].pop()
        elif name == 'wrong-label':
            next(s for s in bad['domain']['sources'] if s['id'] == 'W5')['graph']['boundary'][4] = 0
        elif name == 'wrong-lift':
            c = bad['graphs']['W5']['rows'][0]['full_lifts'][0]
            c[0] = c[1]
        elif name == 'illegal-quotient':
            op = next(op for m in bad['domain']['marks'] for op in m['operations'] if op['kind'] == 'quotient')
            op['partition'] = [[0, 1], [2], [3], [4]]
        elif name == 'missing-empty-fibre':
            row = bad['marks'][0]['operations'][0]['rows'][0]
            assert row['joint_condition_fibres']['00'] == []
            del row['joint_condition_fibres']['00']
        with tempfile.TemporaryDirectory(prefix='negative-', dir=HERE) as directory:
            path = Path(directory) / 'malformed.json'
            with path.open('x') as f:
                json.dump(bad, f, sort_keys=True, separators=(',', ':'))
                f.write('\n')
            record = run('negative-' + name, python + [str(HERE / 'check.py'), '--check', str(path)], 1)
            record.update({'recipe': recipe, 'malformed_sha256': sha(path)})
            negatives.append(record)
    after = snapshot()
    if before != after:
        raise ValueError('protected inputs/certificates/scripts changed during read-only checks')
    result = {'schema': 'degree5-star-B-validation-v1', 'certificate': str(CERT.relative_to(ROOT)),
              'certificate_sha256': sha(CERT), 'normal_and_seed17_match_same_complete_certificate': True,
              'protected_file_drift': [], 'protected_file_hashes': before,
              'replays': records, 'negative_controls': negatives,
              'Lean': 'not run; this task has no new Lean theorem',
              'outside_933_941_source': 'not triggered'}
    with (ROOT / ('VALIDATION' + ('.' + TAG if TAG else '') + '.json')).open('x') as f:
        json.dump(result, f, sort_keys=True, indent=2)
        f.write('\n')
    print('PASS protected drift zero; all malformed certificates rejected', flush=True)


if __name__ == '__main__':
    main()
