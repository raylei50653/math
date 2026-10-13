#!/usr/bin/env python3
"""Read-only integration replay for this exclusive no4ct prerequisite audit."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def inputs():
    data = json.loads((HERE / 'INPUTS.json').read_text())
    drift = []
    for entry in data['inputs']:
        payload = (HERE / 'frozen' / entry['path']).read_bytes()
        assert len(payload) == entry['bytes'], entry['path']
        assert hashlib.sha256(payload).hexdigest() == entry['sha256'], entry['path']
        if hashlib.sha256((REPO / entry['path']).read_bytes()).hexdigest() != entry['sha256']:
            drift.append(entry['path'])
    assert not drift, f'live authority-input drift: {drift}'
    return {'base':data['base'], 'frozen_files':len(data['inputs']), 'live_input_drift':drift}


def seal():
    data = json.loads((HERE / 'MANIFEST.json').read_text())
    for entry in data['outputs']:
        payload = (HERE / entry['path']).read_bytes()
        assert len(payload) == entry['bytes'], entry['path']
        assert hashlib.sha256(payload).hexdigest() == entry['sha256'], entry['path']
    return len(data['outputs'])


def ledger():
    with gzip.open(HERE/'c9/finite/certificate.v2.json.gz','rt') as stream:
        cert=json.load(stream)
    result=json.loads((HERE/'c9/RESULTS.json').read_text())
    assert result['base']==cert['base']
    assert result['summary']==cert['summary']
    keys=('query_id','case_id','geometry_id','target','extras','status',
          'necessary_support_size','fixed_point','possible_outer_union','missing_quotient_indices')
    assert result['queries']==[{k:q[k] for k in keys} for q in cert['queries']]
    assert result['source_status'].startswith('not triggered')
    assert result['general_main_proposition']=='OPEN'
    ears=[q for q in cert['queries'] if q['geometry_id']!='induced']
    assert len(ears)==225
    assert all(q['status']=='excluded_transfer_kempe' and q['possible_outer_union']==0 for q in ears)
    residuals=[q for q in cert['queries'] if q['status']=='necessary_condition_residual']
    assert len(residuals)==84 and all(q['geometry_id']=='induced' for q in residuals)
    assert all(max(q['extras'])<=3 for q in residuals)
    r932=[q for q in residuals if q['target']==932]
    assert len(r932)==20 and all(max(q['extras'])==2 for q in r932)
    return cert['summary']


def replay(path, negative, check_flag=True):
    command=[sys.executable,'-B',str(HERE/path)]
    if check_flag:command.append('--check')
    if negative:command.append('--negative')
    process=subprocess.run(command,capture_output=True,text=True)
    if process.returncode:
        sys.stderr.write(process.stdout)
        sys.stderr.write(process.stderr)
        raise SystemExit(process.returncode)
    lines=[line for line in process.stdout.splitlines() if line.strip()]
    assert lines, path
    summary=json.loads(lines[-1])
    assert summary['status']=='PASS', path
    return summary


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true',required=True)
    parser.add_argument('--negative',action='store_true')
    args=parser.parse_args()
    custody=inputs()
    sealed=seal()
    counts=ledger()
    primary=replay('c9/finite/check.py',args.negative)
    independent=replay('c9/review/check.py',args.negative,check_flag=False)
    terminals=replay('terminals/check.py',args.negative)
    assert primary['by_target']==counts['by_target']
    print(json.dumps({'status':'PASS','custody':custody,'sealed_outputs':sealed,
                      'c9_primary':primary,'c9_independent':independent,
                      'terminal_full_lifts':terminals,
                      'evidence':'conditional paper structure plus exhaustive named interface/full-fibre verification',
                      'actual_target_source':'not triggered',
                      'source_realizability':'OPEN for all necessary residuals',
                      'unbounded_three_branches':'OPEN','main_proposition':'OPEN',
                      'lean':'not formalized'},sort_keys=True))


if __name__=='__main__':main()
