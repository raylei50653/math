#!/usr/bin/env python3
"""Retain read-only normal/seed17 and fail-closed control receipts."""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def run(argv,env=None):
    result=subprocess.run(argv,cwd=ROOT,env=env,text=True,capture_output=True)
    return dict(command=argv,exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)


def main():
    normal=run([sys.executable,'-B',str(HERE/'check.py')])
    env=dict(os.environ,PYTHONHASHSEED='17')
    seed=run([sys.executable,'-B','-O',str(HERE/'check.py'),'--seed','17'],env)
    negative=run([sys.executable,'-B',str(HERE/'check.py'),'--negative'])
    if any(r['exit_code'] for r in [normal,seed,negative]):raise ValueError('replay failed')
    if json.loads(normal['stdout'])!=json.loads(seed['stdout']):raise ValueError('normal/seed mismatch')
    other=deepcopy(json.loads((HERE/'certificate.json').read_text()));other['caps'][0]['edges'].pop()
    with tempfile.TemporaryDirectory(prefix='gamma8-chi-seven-') as tmp:
        path=Path(tmp)/'corrupt.json';path.write_text(json.dumps(other))
        external=run([sys.executable,'-B',str(HERE/'check.py'),'--certificate',str(path)])
        if external['exit_code']==0:raise ValueError('external corrupt accepted')
        external['command'][-1]='<temporary-corrupt-certificate>'
    original=sha256((HERE/'certificate.json').read_bytes()).hexdigest()
    exclusive=run([sys.executable,'-B',str(HERE/'produce.py')])
    if exclusive['exit_code']==0 or sha256((HERE/'certificate.json').read_bytes()).hexdigest()!=original:raise ValueError('exclusive-create contract failed')
    report=dict(schema='941-gamma8-chi-seven-verification-v1',status='PASS',normal=normal,seed17=seed,negative=negative,
        external_corruption=external,exclusive_create_rejection=exclusive,replay_results_equal=True,source_realizability='not triggered',immutable_drift=0)
    with (HERE/'VERIFICATION.json').open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(dict(status='PASS',normal_seed_equal=True,semantic_negative_controls=9,external_negative_controls=1,exclusive_create_rejected=True)))

if __name__=='__main__':main()
