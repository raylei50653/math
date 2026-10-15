#!/usr/bin/env python3
"""Run read-only normal/seed17 checks and retained negative controls."""
import copy,hashlib,json,os,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
cert=HERE/'certificate.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
logs=HERE/'logs';logs.mkdir(exist_ok=True)
before=sha(cert);data=json.loads(cert.read_text());records=[]
for name,mutation in [('wrong-target',lambda d:d['states'][0]['pairings'][0]['cube_targets_by_bitmask'].__setitem__(1,0)),('missing-state',lambda d:d['states'].pop())]:
 bad=copy.deepcopy(data);mutation(bad);path=logs/(name+'.json')
 with path.open('x') as f:json.dump(bad,f,ensure_ascii=False,indent=2);f.write('\n')
commands=[('normal',['--check'],0,{}),('seed17',['--check'],0,{'PYTHONHASHSEED':'17'}),('wrong-target',['--check','--certificate',str(logs/'wrong-target.json')],1,{}),('missing-state',['--check','--certificate',str(logs/'missing-state.json')],1,{}),('exclusive-create',['--write'],1,{})]
for name,args,expect,extra in commands:
 cmd=[sys.executable,'-B',str(HERE/'check.py')]+args
 start=time.monotonic();r=subprocess.run(cmd,cwd=HERE.parents[1],env={**os.environ,**extra},text=True,capture_output=True)
 assert (r.returncode==0)==(expect==0),(name,r.stdout,r.stderr)
 (logs/(name+'.stdout')).write_text(r.stdout);(logs/(name+'.stderr')).write_text(r.stderr)
 records.append({'name':name,'command':cmd,'extra_environment':extra,'returncode':r.returncode,'expected_success':expect==0,'seconds':round(time.monotonic()-start,3)})
assert sha(cert)==before
with (logs/'receipts.json').open('x') as f:json.dump({'certificate_sha256_before':before,'certificate_sha256_after':sha(cert),'runs':records},f,indent=2);f.write('\n')
print(json.dumps({'normal_and_seed17':'PASS','corrupted_certificates_rejected':2,'exclusive_create_rejected':True,'certificate_unchanged':True}))
