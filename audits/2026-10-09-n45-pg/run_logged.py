#!/usr/bin/env python3
"""Exclusive-create command recorder; forwards each command's actual exit."""
import argparse,json,subprocess,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--label',required=True);p.add_argument('--cwd',required=True);p.add_argument('argv',nargs=argparse.REMAINDER);a=p.parse_args()
argv=a.argv[1:] if a.argv[:1]==['--'] else a.argv
out=Path(__file__).resolve().parent/'logs'
paths=[out/(a.label+'.command.json'),out/(a.label+'.stdout.log'),out/(a.label+'.stderr.log')]
if any(x.exists() for x in paths):raise SystemExit('Refusing to replace existing command evidence')
t0=time.time();r=subprocess.run(argv,cwd=a.cwd,capture_output=True)
for f,b in [(paths[1],r.stdout),(paths[2],r.stderr),(paths[0],(json.dumps({'argv':argv,'cwd':a.cwd,'exit_code':r.returncode,'elapsed_seconds':round(time.time()-t0,3)},indent=2)+'\n').encode())]:
 with f.open('xb') as h:h.write(b)
print(json.dumps({'label':a.label,'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr)}));sys.exit(r.returncode)
