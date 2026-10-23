#!/usr/bin/env python3
"""Exclusive-create normal, seed17 and semantic/external negative receipts."""
import ast
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def write(name,value):
    p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:json.dump(value,f,indent=2,sort_keys=True);f.write('\n')

def run(name,extra=(),seed17=False):
    cmd=[sys.executable,'-B']+(['-O'] if seed17 else [])+[str(HERE/'check.py'),*extra]
    env=dict(os.environ)
    if seed17:env['PYTHONHASHSEED']='17'
    p=subprocess.run(cmd,capture_output=True,text=True,env=env)
    result=dict(command=cmd,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
    write('runs/'+name+'.json',result)
    return p,json.loads(p.stdout)

def main():
    for name in ['check.py','produce.py','verify.py']:ast.parse((HERE/name).read_text())
    normal,n=run('normal');seed,s=run('seed17',['--seed','17'],True)
    if normal.returncode or seed.returncode:raise ValueError('positive replay failed')
    if {k:v for k,v in n.items() if k!='seed'}!={k:v for k,v in s.items() if k!='seed'}:raise ValueError('seed17 differs')
    neg,ng=run('semantic-negative',['--negative'])
    if neg.returncode or len(ng['semantic_negatives'])!=10:raise ValueError('semantic negatives failed')
    c=json.loads((HERE/'certificate.json').read_text())
    bad=deepcopy(c);bad['complete_star_cases'][0]['joint_star_rows'][0]['y'].append('chi')
    write('runs/corrupted-certificate.json',bad)
    external,ex=run('external-negative',['--certificate',str(HERE/'runs/corrupted-certificate.json')])
    write('runs/malformed-certificate.json',{})
    malformed,mf=run('malformed-negative',['--certificate',str(HERE/'runs/malformed-certificate.json')])
    if external.returncode!=1 or malformed.returncode!=1:raise ValueError('external negative accepted')
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    final_hashes=[]
    for r in inputs['inputs']:
        raw=(HERE.parents[1]/r['path']).read_bytes()
        if sha256(raw).hexdigest()!=r['sha256']:raise ValueError('final live authority drift')
        final_hashes.append(dict(path=r['path'],sha256=r['sha256']))
    write('VERIFICATION.json',dict(status='PASS',normal=n,seed17=s,semantic_negative_count=10,
        external_negatives=[dict(kind='corrupt-star',status=ex['status']),dict(kind='malformed',status=mf['status'])],
        final_authority_hashes=final_hashes,immutable_drift=0,syntax_files=3,
        source_realizability='not triggered',paper_excluded_branch='empty_M2_T6_X6',
        paper_all_eleven_minimum_exterior=7,common_k_lower_bound=23))
    print(json.dumps(dict(status='PASS',normal_seed17_equal=True,semantic_negative_count=10,
        external_negative_count=2,immutable_drift=0)))

if __name__=='__main__':main()
