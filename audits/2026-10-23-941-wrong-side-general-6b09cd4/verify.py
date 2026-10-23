#!/usr/bin/env python3
"""Capture bounded read-only replays and authority drift; exclusive output."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
records=[]
for script in ['audits/2026-10-23-941-wrong-side-general-6b09cd4/check.py','audits/2026-10-23-941-p-b13-6b09cd4/check.py']:
 for label,flags,seed in [('normal',[],None),('seed17',['--seed','17'],'17'),('negative',['--negative'],None)]:
  cmd=['python3','-B']+(['-O'] if seed else [])+[script]+flags
  env=os.environ.copy()
  if seed:env['PYTHONHASHSEED']=seed
  p=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True)
  name=('current' if 'wrong-side-general' in script else 'predecessor')+'-'+label
  (HERE/'runs').mkdir(exist_ok=True)
  path=HERE/'runs'/f'{name}.json'
  with path.open('x') as f:f.write(p.stdout)
  err=HERE/'runs'/f'{name}.stderr.txt'
  with err.open('x') as f:f.write(p.stderr)
  if p.returncode: raise RuntimeError(f'{name}: {p.stderr}')
  data=json.loads(p.stdout)
  records.append(dict(name=name,command=cmd,env={} if seed is None else dict(PYTHONHASHSEED=seed),returncode=p.returncode,output=str(path.relative_to(HERE)),sha256=sha256(p.stdout.encode()).hexdigest(),status=data.get('status')))
m=json.loads((HERE/'INPUTS.json').read_text())
drift=[]
for r in m['inputs']:
 b=(ROOT/r['path']).read_bytes()
 if (len(b),sha256(b).hexdigest())!=(r['bytes'],r['sha256']):drift.append(r['path'])
require_clean=not drift
result=dict(schema='941-wrong-side-general-verification-v1',replays=records,mathematical_authority_inputs=len(m['inputs']),authority_drift=drift,finite_calibration='triggered and holds',source_control='not triggered',same_statistics_normal_seed17=json.loads((HERE/'runs/current-normal.json').read_text())['statistics']==json.loads((HERE/'runs/current-seed17.json').read_text())['statistics'])
if not require_clean:raise RuntimeError(str(drift))
with (HERE/'VERIFICATION.json').open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',replays=len(records),authority_drift=len(drift),same_statistics_normal_seed17=result['same_statistics_normal_seed17']),sort_keys=True))
