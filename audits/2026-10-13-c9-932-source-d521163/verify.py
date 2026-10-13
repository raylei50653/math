#!/usr/bin/env python3
"""Read-only exact replay of the isolated C9/932 h=4 source audit."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def custody():
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    drift = []
    for item in manifest['inputs']:
        frozen = (HERE / 'frozen' / item['path']).read_bytes()
        assert len(frozen) == item['bytes'], item['path']
        assert hashlib.sha256(frozen).hexdigest() == item['sha256'], item['path']
        live = REPO / item['path']
        if not live.is_file() or hashlib.sha256(live.read_bytes()).hexdigest() != item['sha256']:
            drift.append(item['path'])
    assert not drift, ('live prerequisite drift', drift)
    return {'base': manifest['base'], 'frozen_files': len(manifest['inputs']),
            'live_prerequisite_drift': drift}


def seal():
    manifest = json.loads((HERE / 'MANIFEST.json').read_text())
    for item in manifest['outputs']:
        raw = (HERE / item['path']).read_bytes()
        assert len(raw) == item['bytes'], item['path']
        assert hashlib.sha256(raw).hexdigest() == item['sha256'], item['path']
    return len(manifest['outputs'])


def run(relative, negative):
    command = [sys.executable, '-B', str(HERE / relative), '--check']
    if negative:
        command.append('--negative')
    process = subprocess.run(command, text=True, capture_output=True)
    if process.returncode:
        sys.stderr.write(process.stdout + process.stderr)
        raise SystemExit(process.returncode)
    result = json.loads(process.stdout.splitlines()[-1])
    assert result['status'] == 'PASS', relative
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', required=True, action='store_true')
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    inputs = custody()
    sealed = seal()
    primary = run('counts/check.py', args.negative)
    independent = run('review/check.py', args.negative)
    geometry = run('geometry/check.py', args.negative)
    assert primary['excluded_hypotheses'] == independent['hypotheses_excluded'] == 100
    print(json.dumps({'status': 'PASS', 'custody': inputs, 'sealed_files': sealed,
                      'primary': primary, 'independent': independent, 'geometry': geometry,
                      'claim_domain': 'globally minimal no4ct source, complete 932, h=4',
                      'apex_H_degree_at_least': 4, 'apex_G_degree_at_least': 6,
                      'original_inner_vertices_at_least': 18,
                      'whole_h4_932_sources_excluded': 0,
                      'general_932': 'OPEN', 'h_ge_5': 'OPEN',
                      'source_realizability': 'OPEN', 'lean': 'not formalized'}, sort_keys=True))


if __name__ == '__main__':
    main()
