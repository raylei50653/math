#!/usr/bin/env python3
"""Deliberate corruptions and the Boolean-support versus count-vector control."""
from copy import deepcopy
from fractions import Fraction as Q
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from checker import algebra, check_identity, verify

HERE = Path(__file__).resolve().parent


def rejected(action):
    try:
        action()
    except AssertionError as error:
        return str(error)
    raise AssertionError('negative control unexpectedly accepted')


def main():
    interface = json.loads((HERE.parent/'interface.json').read_text())
    certificate = json.loads((HERE/'certificate.v2.json').read_text())
    words, nc, active, rows = algebra()
    source = next(q for q in certificate['queries'] if q['status'] == 'excluded_count')
    bad_identity = deepcopy(source['identity'])
    bad_identity['lhs'][0]['coefficient'] += 1
    coefficient = rejected(lambda: check_identity(bad_identity, words, nc))
    bad_labels = deepcopy(source['identity'])
    term = bad_labels['lhs'][0]
    term['word'] = list(words[(term['index']+1) % 274])
    label = rejected(lambda: check_identity(bad_labels, words, nc))
    bad_preimage = deepcopy(certificate)
    q = next(q for q in bad_preimage['queries'] if q['status'] == 'excluded_count')
    q['accepted_preimages'][str(q['forced_outer_index'])].pop()
    preimage = rejected(lambda: verify(bad_preimage, interface))
    bad_coefficient_certificate = deepcopy(certificate)
    q = next(q for q in bad_coefficient_certificate['queries'] if q['status'] == 'excluded_count')
    q['identity'] = bad_identity
    cli_rejections = {}
    with tempfile.TemporaryDirectory(prefix='c8-count-negative-') as temporary:
        for name, bad in [('coefficient', bad_coefficient_certificate), ('preimage', bad_preimage)]:
            path = Path(temporary)/(name+'.json')
            path.write_text(json.dumps(bad))
            run = subprocess.run([sys.executable, str(HERE/'checker.py'), '--check',
                                  '--certificate', str(path)], text=True, capture_output=True)
            assert run.returncode != 0 and 'AssertionError' in run.stderr
            cli_rejections[name] = {'exit_code': run.returncode,
                                    'last_stderr_line': run.stderr.strip().splitlines()[-1]}
    bad_closure = deepcopy(certificate)
    q = next(q for q in bad_closure['queries'] if q['status'] == 'necessary_condition_residual')
    del q['residual_support_mask']
    closure = rejected(lambda: verify(bad_closure, interface))
    upper = source['upper_mask']
    boolean_residual = sum(Q(t['coefficient'])*int(upper >> t['index'] & 1)
                           for t in source['identity']['lhs']) - \
                       sum(Q(t['coefficient'])*int(upper >> t['index'] & 1)
                           for t in source['identity']['rhs'])
    assert boolean_residual != 0
    result = {'status': 'PASS', 'coefficient_corruption': coefficient,
              'mixed_named_pattern': label, 'missing_preimage': preimage,
              'missing_joint_support_verification': closure,
              'actual_checker_cli_rejections': cli_rejections,
              'boolean_upper_count_countercontrol': {'case_id': source['case_id'],
                  'target': source['target'], 'identity_residual': str(boolean_residual),
                  'result': 'Boolean necessary upper is not an actual count vector'}}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
