#!/usr/bin/env python3
import json,os,subprocess,sys
from pathlib import Path
P=Path(__file__).resolve().parent
(P/'logs').mkdir(exist_ok=True);(P/'negative').mkdir(exist_ok=True)
fibres=json.loads((P/'full-source-local-fibres.json').read_text())
# Corrupt one nonempty complete fibre, without touching the positive certificate.
for row in fibres['fibres']:
 if row['all_lifts']:
  row['all_lifts'].pop();break
bad=P/'negative'/'missing-original-lift.json'
if not bad.exists():bad.write_text(json.dumps(fibres,indent=2)+'\n')
cases=[('normal',[sys.executable,'-B',str(P/'check.py')],{},0),('seed17',[sys.executable,'-B',str(P/'check.py')],{'PYTHONHASHSEED':'17'},0),('missing-original-lift',[sys.executable,'-B',str(P/'check.py'),'--fibres',str(bad)],{},1),('exclusive-create',[sys.executable,'-B',str(P/'explore_shared_caps.py'),'--output',str(P/'shared-caps-exploration.json')],{},1)]
result=[]
for name,cmd,patch,want in cases:
 env=dict(os.environ);env.update(patch)
 proc=subprocess.run(cmd,text=True,capture_output=True,env=env)
 (P/'logs'/f'{name}.stdout').write_text(proc.stdout);(P/'logs'/f'{name}.stderr').write_text(proc.stderr)
 if proc.returncode!=want:raise RuntimeError((name,proc.returncode,proc.stdout,proc.stderr))
 result.append({'name':name,'command':cmd,'environment_patch':patch,'exit_code':proc.returncode,'expected_exit':want,'stdout':f'logs/{name}.stdout','stderr':f'logs/{name}.stderr','pass':True})
(P/'VERIFICATION.json').write_text(json.dumps({'checks':result,'source_coverage':'not triggered','complete319':'OPEN'},indent=2)+'\n')
print(json.dumps({'checks':len(result),'status':'PASS'}))
