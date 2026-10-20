#!/usr/bin/env python3
"""Read-only connected replay of the frozen 941 acceptance audit."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='13dc5ff163045c85b5c82dde438eb5f275dab999'

def verify_inputs(manifest):
    assert manifest['base']==BASE
    assert manifest['exclusive_audit']==HERE.relative_to(ROOT).as_posix()
    assert len(manifest['files'])==406
    assert len({r['path'] for r in manifest['files']})==406
    assert manifest['start_status'].strip(),'the inherited worktree was not clean'
    assert manifest['routing_drift_allowed']==['docs/STATUS.md','docs/c5_kempe_guide.md']
    for rec in manifest['files']:
        path=rec['path']
        actual=(HERE/'routing-start'/(Path(path).name+'.txt') if path in manifest['routing_drift_allowed'] else ROOT/path)
        raw=actual.read_bytes()
        assert len(raw)==rec['bytes'] and hashlib.sha256(raw).hexdigest()==rec['sha256'],('frozen input drift',path)

def verify_seal(seal):
    assert seal['base']==BASE and seal['main_target']=='OPEN'
    assert seal['source_realized'] is False and seal['smaller_bad_constructed'] is False
    assert seal['new_Lean_theorem'] is False
    for path,digest in seal['files'].items():
        assert hashlib.sha256((HERE/path).read_bytes()).hexdigest()==digest,('sealed audit drift',path)

def main():
    manifest=json.loads((HERE/'INPUTS.json').read_text());verify_inputs(manifest)
    seal=json.loads((HERE/'OUTPUTS.json').read_text());verify_seal(seal)
    b=json.loads((HERE/'B/certificate.json').read_text())
    d=json.loads((HERE/'D/certificate.json').read_text())
    assert b['n5_a6_exclusion']['source_alpha_zero'] is True
    assert b['n5_a6_exclusion']['source_projection_upper_mask']==429
    assert d['q6_c5_exclusion']['original_support_upper']==429
    assert d['q6_c5_exclusion']['original_alpha_cells']==[]
    # The second actual short pocket is the identical complete C5 list with
    # every boundary name transported by this one mapping, including W5.
    rename={'t':'L','a':'q','n':'c','R':'s','z':'z'}
    assert [rename[v] for v in b['short_pocket']['cycle']]==['L','q','c','s','z']
    assert b['short_pocket']['W5_boundary_degrees']==[3]*5
    assert d['changed_operation']['completed_inner_delta']==-1
    commands=[('A/check.py',['--negative-controls']),('B/check.py',[]),('C/check.py',[]),('D/check.py',[]),('B/check_contacts.py',[])]
    results=[]
    for path,args in commands:
        run=subprocess.run([sys.executable,'-B',str(HERE/path),*args],cwd=ROOT,capture_output=True,text=True)
        if run.returncode:
            sys.stderr.write(run.stdout+run.stderr);raise SystemExit(run.returncode)
        result=json.loads(run.stdout)
        assert result.get('pass',result.get('ok')) is True
        results.append({'checker':path,'exit_code':0,'result':result})
    wrong=copy.deepcopy(manifest);wrong['files'][0]['sha256']='0'*64
    try:verify_inputs(wrong)
    except AssertionError:pass
    else:raise AssertionError('corrupted frozen input hash accepted')
    wrong=copy.deepcopy(seal);wrong['smaller_bad_constructed']=True
    try:verify_seal(wrong)
    except AssertionError:pass
    else:raise AssertionError('source/model authority escalation accepted')
    verify_inputs(manifest);verify_seal(seal)
    print(json.dumps({'pass':True,'base':BASE,'frozen_inputs':406,'frozen_drift':0,'sealed_drift':0,
                      'original_source_theorems':['n=5 => a>=7','c=5 => q>=7','dist_G(t,R)>=3','dist_G(L,s)>=3'],
                      'main_target':'OPEN','source_realized':False,'smaller_bad_constructed':False,
                      'new_Lean_theorem':False,'frozen_hash_corruption_rejected':True,
                      'source_authority_escalation_rejected':True,'checks':results},sort_keys=True,ensure_ascii=False))

if __name__=='__main__':main()
