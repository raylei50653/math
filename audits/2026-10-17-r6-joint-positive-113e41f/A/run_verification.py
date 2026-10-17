#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
records=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,args,expected):
 cmd=[sys.executable,'-B',str(HERE/'check.py')]+args
 env=os.environ.copy()
 if label=='seed17':env['PYTHONHASHSEED']='17'
 p=subprocess.run(cmd,text=True,capture_output=True,env=env)
 out=HERE/(label+'.stdout');err=HERE/(label+'.stderr')
 with out.open('x') as f:f.write(p.stdout)
 with err.open('x') as f:f.write(p.stderr)
 assert p.returncode==expected,(label,p.returncode,p.stdout,p.stderr)
 records.append({'label':label,'argv':cmd,'exit_code':p.returncode,'expected_exit_code':expected,'stdout':out.name,'stderr':err.name,'stdout_sha256':digest(out),'stderr_sha256':digest(err)})
run('normal',['--create'],0)
run('seed17',['--seed','17'],0)
cert=json.loads((HERE/'certificate-v3.json').read_text())
for ctl in cert['controls']:
 for match in ctl['all_matchings']:
  for c in match['complement_cycles']:
   if c['length']==7 and not c['facial_centres']:
    c['matching_chords']=[]
    break
  else:continue
  break
 else:continue
 break
bad=HERE/'corrupt-chord.json'
with bad.open('x') as f:json.dump(cert,f,sort_keys=True,indent=2);f.write('\n')
run('corrupt-chord',['--certificate',str(bad)],1)
run('exclusive-create',['--create'],1)
report={'base':'113e41f7023aa00c8257b815ce8727035b648f26','scope':'paper arbitrary-size lemma with finite geometric calibration; no source supplied; no joint positivity proved','active_certificate':'certificate-v3.json','active_certificate_sha256':digest(HERE/'certificate-v3.json'),'proof_sha256':digest(HERE/'PROOF.md'),'checker_sha256':digest(HERE/'check.py'),'records':records}
with (HERE/'VERIFICATION.json').open('x') as f:json.dump(report,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({'ok':True,'records':len(records),'certificate_sha256':report['active_certificate_sha256']}))
