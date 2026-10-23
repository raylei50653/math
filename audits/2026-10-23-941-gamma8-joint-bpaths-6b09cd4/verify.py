#!/usr/bin/env python3
"""Retain exclusive normal/seed17/negative replay receipts."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent


def main():
    runs=[]
    for name,flags,seed in [('normal',[],None),('seed17',['-O'],17),('negative',[],None)]:
        cmd=[sys.executable,'-B',*flags,str(HERE/'check.py')]
        if seed:cmd+=['--seed',str(seed)]
        if name=='negative':cmd+=['--negative']
        env=dict(os.environ)
        if seed:env['PYTHONHASHSEED']=str(seed)
        proc=subprocess.run(cmd,text=True,capture_output=True,env=env)
        receipt=dict(command=cmd,returncode=proc.returncode,stdout=proc.stdout,stderr=proc.stderr)
        with (HERE/'runs'/f'{name}.json').open('x') as f:json.dump(receipt,f,sort_keys=True,indent=2);f.write('\n')
        if proc.returncode:raise RuntimeError(name+' failed')
        runs.append(json.loads(proc.stdout))
    if runs[0]!=runs[1]:raise RuntimeError('seed replay mismatch')
    broken=json.loads((HERE/'certificate.json').read_text())
    broken['face_tables'][0]['admissible_third_points'].append('W')
    path=HERE/'runs'/'corrupted-certificate.json'
    with path.open('x') as f:json.dump(broken,f,sort_keys=True,indent=2);f.write('\n')
    cmd=[sys.executable,'-B',str(HERE/'check.py'),'--certificate',str(path)]
    proc=subprocess.run(cmd,text=True,capture_output=True)
    if not proc.returncode:raise RuntimeError('external corrupt certificate accepted')
    with (HERE/'runs'/'external-negative.json').open('x') as f:
        json.dump(dict(command=cmd,returncode=proc.returncode,stdout=proc.stdout,stderr=proc.stderr),f,sort_keys=True,indent=2);f.write('\n')
    data=dict(schema='941-gamma8-joint-bpaths-verification-v1',normal_seed17_identical=True,
        finite_result=runs[0],semantic_negative_controls=runs[2]['negative'],external_negative_rejected=True,
        source_realizability='not triggered',
        script_sha256={name:sha256((HERE/name).read_bytes()).hexdigest() for name in ['produce.py','check.py','explore_caps.py']})
    with (HERE/'VERIFICATION.json').open('x') as f:json.dump(data,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps(data,sort_keys=True))


if __name__=='__main__':main()
