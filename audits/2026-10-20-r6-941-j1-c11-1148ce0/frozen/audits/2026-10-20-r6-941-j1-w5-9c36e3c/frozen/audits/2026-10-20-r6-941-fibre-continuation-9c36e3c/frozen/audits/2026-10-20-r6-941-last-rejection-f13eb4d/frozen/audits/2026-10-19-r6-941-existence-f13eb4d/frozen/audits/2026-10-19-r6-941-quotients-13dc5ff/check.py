#!/usr/bin/env python3
"""Read-only connected replay; mathematical claims are bounded by REPORT.md."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='13dc5ff163045c85b5c82dde438eb5f275dab999'


def verify_costs(costs):
    assert costs['boundary']==['x','y','a','b','c']
    assert costs['deleted']==['p','h']
    assert costs['new_vertices']==costs['reconstruction_vertices']==0
    assert costs['changed_boundary'] is False
    classes={'Q1':[['n','b'],['R','q']],'Q2':[['n','L','b']]}
    assert set(costs['candidates'])==set(classes)
    for name,groups in classes.items():
        record=costs['candidates'][name]
        assert record['classes']==groups
        assert record['completed_inner_change']==-2-sum(len(group)-1 for group in groups), 'all completed quotient costs'


def main():
    manifest=json.loads((HERE/'INPUTS.json').read_text())
    assert manifest['base']==manifest['reference']==manifest['start_head']==BASE
    assert manifest['start_status']=='' and manifest['later_commits']==[]
    assert manifest['exclusive_audit']==HERE.relative_to(ROOT).as_posix()
    assert manifest['routing_drift_allowed']==['docs/c5_kempe_guide.md','docs/STATUS.md']
    assert len({r['path'] for r in manifest['files']})==len(manifest['files'])
    for record in manifest['files']:
        path=record['path']
        raw=(subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
             if path in manifest['routing_drift_allowed'] else (ROOT/path).read_bytes())
        assert len(raw)==record['bytes'] and hashlib.sha256(raw).hexdigest()==record['sha256'], ('frozen input drift',path)
    sealed=json.loads((HERE/'OUTPUTS.json').read_text())
    assert sealed['base']==BASE and sealed['main_target']=='OPEN' and sealed['source_realized'] is False
    def verify_seal():
        for path,digest in sealed['files'].items():
            assert hashlib.sha256((HERE/path).read_bytes()).hexdigest()==digest, ('audit evidence drift',path)
    verify_seal()
    costs=json.loads((HERE/'costs.json').read_text())
    verify_costs(costs)
    catalogue=json.loads((ROOT/'artifacts/c5_cells/cells.json').read_text())
    K=set(map(int,catalogue['cells']))
    assert len(K)==132 and 941 not in K
    assert not any(mask & (1<<9) and not mask & ((1<<1)|(1<<4)|(1<<6)) for mask in K), 'same-candidate four-row certificate outside K132'
    bad=copy.deepcopy(costs)
    bad['candidates']['Q2']['completed_inner_change']=-2
    try:
        verify_costs(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('omitted completed identification cost accepted')
    commands=[
        (ROOT/'audits/2026-10-19-r6-941-leakage-b89c591/check.py',[]),
        (HERE/'A/check.py',['--negative-controls']),
        (HERE/'B/check.py',[]),
        (HERE/'C/check.py',['--negative-control']),
        (HERE/'right_minimality.py',[]),
        (HERE/'C/review_right.py',[]),
        (HERE/'C/review_geometry.py',[]),
        (HERE/'C/review_closure.py',['--additional-chords']),
        (HERE/'C/review_counts.py',[]),
    ]
    results=[]
    for script,args in commands:
        run=subprocess.run([sys.executable,'-B',str(script),*args],cwd=ROOT,capture_output=True,text=True)
        if run.returncode:
            sys.stderr.write(run.stdout+run.stderr)
            raise SystemExit(run.returncode)
        results.append({'checker':script.relative_to(HERE).as_posix() if script.is_relative_to(HERE) else script.relative_to(ROOT).as_posix(),
                        'exit_code':run.returncode,'stdout_sha256':hashlib.sha256(run.stdout.encode()).hexdigest(),
                        'stdout':run.stdout.strip()})
    verify_seal()
    print(json.dumps({'pass':True,'base':BASE,'frozen_inputs':len(manifest['files']),
                      'frozen_drift':0,'output_drift':0,'omitted_completed_cost_rejected':True,
                      'actual_source_realized':False,'smaller_bad_constructed':False,
                      'main_target':'OPEN','checks':results},sort_keys=True))


if __name__=='__main__':
    main()
