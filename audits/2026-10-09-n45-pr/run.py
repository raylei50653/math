#!/usr/bin/env python3
import argparse,json,os,subprocess,time
from pathlib import Path
OUT=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('--cwd',type=Path,default=OUT);p.add_argument('--seed17',action='store_true');p.add_argument('argv',nargs=argparse.REMAINDER);a=p.parse_args();argv=a.argv[1:] if a.argv and a.argv[0]=='--' else a.argv
folder=OUT/'logs';need=folder/a.name
if any(folder.joinpath(a.name+s).exists() for s in ('.stdout.log','.stderr.log','.json')):raise SystemExit('exclusive-create refused existing command logs')
env={'PYTHONDONTWRITEBYTECODE':'1'}
if a.seed17:env['PYTHONHASHSEED']='17'
start=time.monotonic();r=subprocess.run(argv,cwd=a.cwd,capture_output=True,env={**os.environ,**env})
for suffix,b in [('.stdout.log',r.stdout),('.stderr.log',r.stderr)]:
 with (folder/(a.name+suffix)).open('xb') as f:f.write(b)
record={'argv':argv,'cwd':str(a.cwd.resolve()),'env_override':env,'exit':r.returncode,'seconds':time.monotonic()-start,'stdout':'logs/'+a.name+'.stdout.log','stderr':'logs/'+a.name+'.stderr.log'}
with (folder/(a.name+'.json')).open('x') as f:json.dump(record,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps(record));print(r.stdout.decode());print(r.stderr.decode());raise SystemExit(r.returncode)
