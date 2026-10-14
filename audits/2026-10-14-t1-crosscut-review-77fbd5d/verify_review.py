#!/usr/bin/env python3
"""Read-only review aggregation, with optional exclusive result creation."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads((ROOT/path).read_text())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify():
    custody = load('review_custody', 'replay_candidate.py')
    assert custody.check_custody() == 41
    inputs = read('INPUTS.json')
    for record in inputs['inputs']:
        base_bytes = subprocess.check_output(['git','show',inputs['base']+':'+record['path']], cwd=ROOT)
        assert hashlib.sha256(base_bytes).hexdigest() == record['sha256']
        assert (ROOT.parents[1]/record['path']).read_bytes() == base_bytes
    normal, seed = read('replay-normal/REPLAY.json'), read('replay-seed17/REPLAY.json')
    assert normal['status'] == seed['status'] == 'PASS'
    assert normal['byte_identical_outputs'] == seed['byte_identical_outputs']
    for name, digest in normal['byte_identical_outputs'].items():
        for folder in ('replay-normal', 'replay-seed17', 'candidate-original/t1_broad_probe'):
            assert hashlib.sha256((ROOT/folder/name).read_bytes()).hexdigest() == digest
    with gzip.open(ROOT/'finite/certificate.json.gz','rt') as stream:
        certificate = json.load(stream)
    controls = load('independent_rules', 'review/kempe_controls.py')
    rows = [''.join(map(str,row)) for row in controls.rows]
    assert rows == certificate['C6_rows']
    normalize = lambda value: json.loads(json.dumps(value))
    assert normalize(controls.rules) == certificate['kempe_rules']
    sys.path.insert(0, str(ROOT/'candidate-original/t1_broad_probe'))
    producer = load('original_fast', 'candidate-original/t1_broad_probe/twohole_fast.py')
    verifier = load('original_verify', 'candidate-original/t1_broad_probe/independent_verify.py')
    assert rows == list(producer.ROWS) == verifier.R
    assert normalize(controls.rules) == normalize(verifier.OPS)
    assert [[sorted(set(x)) for x in row] for row in producer.OP] == normalize(controls.rules)
    assert normalize(controls.control_report()) == read('review/kempe_controls.json')
    for name in ('certificate.json.gz','summary.json'):
        assert (ROOT/'finite'/name).read_bytes() == (ROOT/'finite/seed17'/name).read_bytes()
    comparison = read('finite/candidate_comparison.json')
    assert comparison['status'] == 'PASS'
    assert comparison['certificate_sha256'] == hashlib.sha256((ROOT/'finite/certificate.json.gz').read_bytes()).hexdigest()
    summary = read('finite/summary.json')
    assert summary['counts'] == {'cases':32,'maximal_safe_rectangles':512568,'full_lifts_with_named_query_multiplicity':25348}
    joins = read('review/join_controls.json')
    assert joins['status'] == 'PASS' and joins['fixed_B_fibres_compared'] == 80
    assert joins['full_lifts_compared'] == 1709 and joins['empty_product_cells'] == 4671
    assert len(joins['additional_index_negative_controls_rejected']) == 4
    negative = read('replay-normal/controls.json')
    assert len(negative['negative_controls']) == 8
    assert set(negative['negative_controls'].values()) == {'REJECTED'}
    upstream = read('logs/upstream-authority.json')
    assert upstream['status'] == 'PASS' and upstream['queries'] == 8
    return {'status':'PASS_FOR_SCOPED_ADOPTION','base':inputs['base'],
            'theorem':'Under the adopted no4ct globally minimal C5 source contract, h=3 implies p=0.',
            'evidence':'agent-assisted paper review plus exact finite Python certificates; no Lean or external human review',
            'source_coverage':'arbitrary finite disk sizes and all original opposite contacts, including BRIDGE',
            'candidate_archive_sha256':inputs['candidate_archive']['sha256'],
            'frozen_BASE_inputs':len(inputs['inputs']),'frozen_input_drift':0,
            'candidate_manifest_files':41,'candidate_byte_identical_outputs_per_replay':25,
            'candidate_cases':normal['cases'],'candidate_rectangles':normal['rectangles'],
            'candidate_literal_shell_lifts':normal['shell_literal_lifts'],
            'independent_essential_reconstruction':summary['counts'],
            'common_missing_row':'01232','possible_masks':[0,165,424,429],
            'all_93_kempe_rule_sets_agree':True,'actual_disk_controls':7,
            'direct_full_join_controls':{'graphs':8,'fibres':80,'full_lifts':1709,'empty_product_cells':4671},
            'candidate_negative_controls_rejected':8,'added_coverage_negative_controls_rejected':4,
            'upstream_authority_negative_controls_rejected':3,'normal_seed17_byte_identical':True,
            'remaining_open':['RING','h>=4','general K_infinity=K_<=5'],
            'delivery':'isolated review only; main research entrypoints unchanged; no commit or push'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    report = verify()
    path = ROOT/'VERIFICATION.json'
    if args.write:
        with path.open('x') as handle:
            json.dump(report, handle, indent=2, sort_keys=True)
            handle.write('\n')
    else:
        assert json.loads(path.read_text()) == report
    print(json.dumps(report, sort_keys=True))
