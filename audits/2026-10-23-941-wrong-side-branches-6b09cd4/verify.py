#!/usr/bin/env python3
from hashlib import sha256
import json,os,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
records=[]
for name,script in [('current','audits/2026-10-23-941-wrong-side-branches-6b09cd4/check.py'),('predecessor','audits/2026-10-23-941-wrong-side-general-6b09cd4/check.py')]:
 for mode,flags in [('normal',[]),('seed17',['--seed','17']),('negative',['--negative'])]:
  env=os.environ.copy();cmd=['python3','-B']+(['-O'] if mode=='seed17' else [])+[script]+flags
  if mode=='seed17':env['PYTHONHASHSEED']='17'
  p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
  (HERE/'runs').mkdir(exist_ok=True)
  stem=name+'-'+mode
  with (HERE/'runs'/f'{stem}.json').open('x') as f:f.write(p.stdout)
  with (HERE/'runs'/f'{stem}.stderr.txt').open('x') as f:f.write(p.stderr)
  if p.returncode:raise RuntimeError(p.stderr)
  records.append(dict(name=stem,command=cmd,env={} if mode!='seed17' else dict(PYTHONHASHSEED='17'),returncode=p.returncode,output='runs/'+stem+'.json',sha256=sha256(p.stdout.encode()).hexdigest()))
m=json.loads((HERE/'INPUTS.json').read_text());drift=[]
for r in m['inputs']:
 b=(ROOT/r['path']).read_bytes()
 if (len(b),sha256(b).hexdigest())!=(r['bytes'],r['sha256']):drift.append(r['path'])
same=json.loads((HERE/'runs/current-normal.json').read_text())['statistics']==json.loads((HERE/'runs/current-seed17.json').read_text())['statistics']
if drift or not same:raise RuntimeError(str(drift))
with (HERE/'VERIFICATION.json').open('x') as f:json.dump(dict(status='PASS',certificate='certificate-v2.json',replays=records,authority_inputs=len(m['inputs']),authority_drift=drift,normal_seed17_statistics_equal=same,source_control='not triggered'),f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',replays=len(records),authority_drift=drift,normal_seed17_statistics_equal=same)))
