#!/usr/bin/env python3
"""Run bounded read-only replay and retain exact receipts in this audit only."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent


def main():
    runs=[]
    for name,args,seed in [('normal',[],None),('seed17',['-O'],17),('negative',[],None)]:
        cmd=[sys.executable,'-B',*args,str(HERE/'check.py')]
        if seed:cmd+=['--seed',str(seed)]
        if name=='negative':cmd+=['--negative']
        env=dict(os.environ)
        if seed:env['PYTHONHASHSEED']=str(seed)
        proc=subprocess.run(cmd,env=env,text=True,capture_output=True)
        result=dict(command=cmd,returncode=proc.returncode,stdout=proc.stdout,stderr=proc.stderr)
        with (HERE/'runs'/f'{name}.json').open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
        if proc.returncode:raise RuntimeError(name+' failed')
        runs.append(dict(name=name,result=json.loads(proc.stdout)))
    if runs[0]['result']!=runs[1]['result']:raise RuntimeError('seed replay mismatch')
    bad=json.loads((HERE/'certificate.json').read_text())
    bad['star_restrictions'][0]['full_links']['v'].append('x')
    path=HERE/'runs'/'corrupted-certificate.json'
    with path.open('x') as f:json.dump(bad,f,sort_keys=True,indent=2);f.write('\n')
    cmd=[sys.executable,'-B',str(HERE/'check.py'),'--certificate',str(path)]
    proc=subprocess.run(cmd,text=True,capture_output=True)
    if not proc.returncode:raise RuntimeError('external negative accepted')
    with (HERE/'runs'/'external-negative.json').open('x') as f:
        json.dump(dict(command=cmd,returncode=proc.returncode,stdout=proc.stdout,stderr=proc.stderr),f,sort_keys=True,indent=2);f.write('\n')
    result=dict(schema='941-gamma8-u-link-verification-v1',normal_seed17_identical=True,
        finite_results=runs[0]['result'],semantic_negative_count=runs[2]['result']['negative']['count'],
        external_corrupted_certificate_rejected=True,
        producer_checker_sha256={name:sha256((HERE/name).read_bytes()).hexdigest() for name in ['produce.py','check.py']},
        source_realizability='not triggered',new_Lean=False,new_LP=False,smaller_bad=False)
    with (HERE/'VERIFICATION.json').open('x') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
