#!/usr/bin/env python3
"""Read-only replay of the frozen same-source geometry and cap audit."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '13dc5ff163045c85b5c82dde438eb5f275dab999'


def verify_inputs(manifest):
    assert manifest['base'] == BASE
    assert manifest['exclusive_audit'] == HERE.relative_to(ROOT).as_posix()
    assert len(manifest['files']) == 488
    assert len({r['path'] for r in manifest['files']}) == 488
    assert manifest['routing_drift_allowed'] == ['docs/STATUS.md', 'docs/c5_kempe_guide.md']
    for rec in manifest['files']:
        name = rec['path']
        actual = (HERE / 'routing-start' / (Path(name).name + '.txt')
                  if name in manifest['routing_drift_allowed'] else ROOT / name)
        raw = actual.read_bytes()
        assert len(raw) == rec['bytes'], ('frozen byte count', name)
        assert hashlib.sha256(raw).hexdigest() == rec['sha256'], ('frozen SHA drift', name)


def verify_seal(seal):
    assert seal['base'] == BASE
    assert seal['main_target'] == 'OPEN'
    for field in ('source_realized', 'smaller_bad_constructed', 'new_Lean_theorem'):
        assert seal[field] is False, ('authority escalation', field)
    for name, digest in seal['files'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, ('sealed drift', name)
    assert set(seal['routing_outputs']) == {'docs/STATUS.md', 'docs/c5_kempe_guide.md'}
    for name, digest in seal['routing_outputs'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, ('final routing drift', name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seal', type=Path, default=HERE / 'OUTPUTS.json')
    args = parser.parse_args()
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    seal = json.loads(args.seal.read_text())
    verify_inputs(manifest)
    verify_seal(seal)
    contacts = json.loads((HERE / 'B/certificate.json').read_text())
    allowed = [set(r['contacts']) for r in contacts['complete_contact_subsets']
               if r['necessary_allowed']]
    for triple in ({'q','c','s'}, {'a','n','R'}):
        assert [s for s in allowed if triple <= s] == [triple], 'complete replacement rim contacts'
    results = []
    for name in ('A/check.py', 'B/check.py', 'C/check.py', 'B/review_c.py', 'review_lifts.py'):
        extra = ['--negative-controls'] if name == 'A/check.py' else []
        run = subprocess.run([sys.executable, '-B', str(HERE / name), *extra], cwd=ROOT,
                             capture_output=True, text=True)
        if run.returncode:
            sys.stderr.write(run.stdout + run.stderr)
            raise SystemExit(run.returncode)
        result = json.loads(run.stdout)
        assert result.get('pass', result.get('ok')) is True, name
        results.append({'checker': name, 'result': result})
    negative = []
    bad = copy.deepcopy(manifest)
    bad['files'][0]['sha256'] = '0' * 64
    try:
        verify_inputs(bad)
    except AssertionError:
        negative.append('corrupted-frozen-SHA')
    else:
        raise AssertionError('corrupted frozen SHA accepted')
    bad = copy.deepcopy(seal)
    bad['smaller_bad_constructed'] = True
    try:
        verify_seal(bad)
    except AssertionError:
        negative.append('source-authority-escalation')
    else:
        raise AssertionError('model promoted to source')
    verify_inputs(manifest)
    verify_seal(seal)
    print(json.dumps({'pass': True, 'base': BASE, 'frozen_inputs': 488,
                      'frozen_drift': 0, 'sealed_drift': 0,
                      'negative_controls_rejected': negative, 'checks': results,
                      'both_low_degree_replacement_C10_induced': True,
                      'main_target': 'OPEN', 'source_realized': False,
                      'smaller_bad_constructed': False, 'new_Lean_theorem': False},
                     ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
