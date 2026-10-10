#!/usr/bin/env python3
"""Exclusive command records and combined stdout/stderr logs."""
import argparse,json,os,subprocess,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--cwd',type=Path,default=Path.cwd());p.add_argument('--seed');p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
cmd=a.command[1:] if a.command and a.command[0]=='--' else a.command
home=Path(__file__).resolve().parent
log=home/'logs'/f'{a.id}.log';record=home/'logs'/f'{a.id}.json'
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
if a.seed is not None:env['PYTHONHASHSEED']=a.seed
start=time.time()
with log.open('xb') as f:r=subprocess.run(cmd,cwd=a.cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
value={'id':a.id,'command':cmd,'cwd':str(a.cwd.resolve()),'environment':{'PYTHONDONTWRITEBYTECODE':'1',**({'PYTHONHASHSEED':a.seed} if a.seed is not None else {})},'exit':r.returncode,'seconds':round(time.time()-start,6),'log':str(log.relative_to(home))}
with record.open('x') as f:json.dump(value,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
print(json.dumps(value,sort_keys=True));print(log.read_text()[-3500:])
