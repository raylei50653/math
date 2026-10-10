#!/usr/bin/env python3
"""Exclusive audit logs; no worker or shared-file writes."""
import datetime,json,os,subprocess,sys
from pathlib import Path
D=Path(__file__).resolve().parent
name=sys.argv[1]; command=sys.argv[2:]
for suffix in ['command.json','stdout.log','stderr.log']:
    if (D/'logs'/f'{name}.{suffix}').exists():
        raise FileExistsError(name)
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run(command,cwd=D,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
meta={'name':name,'argv':command,'cwd':str(D),'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'PYTHONHASHSEED':os.environ.get('PYTHONHASHSEED')}
for suffix,data in [('command.json',(json.dumps(meta,indent=2)+'\n').encode()),('stdout.log',p.stdout),('stderr.log',p.stderr)]:
    with (D/'logs'/f'{name}.{suffix}').open('xb') as f:f.write(data)
print(json.dumps(meta))
if p.stdout: print(p.stdout.decode(),end='')
if p.stderr: print(p.stderr.decode(),end='',file=sys.stderr)
sys.exit(p.returncode)
