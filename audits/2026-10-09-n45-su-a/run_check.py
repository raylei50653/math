#!/usr/bin/env python3
"""Run an explicitly named read-only check and preserve exact argv, exit and logs."""
import argparse,datetime,json,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--cwd',default='.');p.add_argument('--seed17',action='store_true');p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
out=Path(__file__).resolve().parent/'logs'
cmd=a.command[1:] if a.command and a.command[0]=='--' else a.command
paths={k:out/(a.name+'.'+k) for k in ('stdout.log','stderr.log','command.json')}
# Reserve all output paths before starting; reject a repeated invocation without executing it.
handles={k:path.open('x') for k,path in paths.items()}
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
if a.seed17:env['PYTHONHASHSEED']='17'
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(cmd,cwd=a.cwd,env=env,stdout=handles['stdout.log'],stderr=handles['stderr.log'])
rec={'argv':cmd,'cwd':str(Path(a.cwd).resolve()),'env_overrides':{'PYTHONDONTWRITEBYTECODE':'1',**({'PYTHONHASHSEED':'17'} if a.seed17 else {})},'exit_code':r.returncode,'started_UTC':start,'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':str(paths['stdout.log'].relative_to(out.parent)),'stderr':str(paths['stderr.log'].relative_to(out.parent))}
json.dump(rec,handles['command.json'],ensure_ascii=False,indent=2);handles['command.json'].write('\n')
for h in handles.values():h.close()
print(json.dumps(rec,ensure_ascii=False));raise SystemExit(r.returncode)
