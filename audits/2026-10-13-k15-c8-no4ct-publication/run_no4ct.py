#!/usr/bin/env python3
"""Record read-only publication replays; original audit bytes are preserved."""
import json,os,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
NX='/home/ray/.cache/uv/archive-v0/HGS6nMcAklcC0r9f'
COL='audits/2026-10-13-c5-no4ct-collar-6cafdfb/'
commands=[
 ('dependency',['python3','-B','audits/2026-10-13-c5-no4ct-dependency-6cafdfb/check.py','--check']),
 ('relative-c4',['python3','-B','audits/2026-10-13-c5-no4ct-degrees-6cafdfb/check_c4.py','--check']),
 ('collar-frozen-c4',['python3','-B',COL+'frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/check_c4.py','--check']),
 ('crosscut',['python3','-B',COL+'frozen/audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/checker.py','--check']),
 ('three-target-collar',['python3','-B',COL+'collar/check.py','--check']),
 ('collar-independent',['python3','-B',COL+'review/independent_review.py']),
 ('c7-independent-count',['python3','-B',COL+'frozen/audits/2026-10-13-c7-joint-kempe-19209f4c/topology/count_review.py']),
 ('c8-no4ct',['python3','-B','audits/2026-10-13-c5-no4ct-c8-6cafdfb/verify.py','--check','--negative']),
 ('c8-no4ct-seed17',['python3','-B','audits/2026-10-13-c5-no4ct-c8-6cafdfb/verify.py','--check','--negative']),
]
results=[]
for name,cmd in commands:
 env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONPATH']=NX
 if name.endswith('seed17'): env['PYTHONHASHSEED']='17'
 t=time.monotonic(); proc=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
 log=HERE/'validation'/('no4ct-'+name+'.log'); log.write_text(proc.stdout+proc.stderr)
 results.append({'name':name,'command':cmd,'environment':{'PYTHONPATH':NX,**({'PYTHONHASHSEED':'17'} if name.endswith('seed17') else {})},'exit_code':proc.returncode,'log':str(log.relative_to(HERE)),'elapsed_seconds':round(time.monotonic()-t,3)})
 (HERE/'validation/no4ct-results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,proc.returncode,flush=True)
 if proc.returncode: sys.exit(proc.returncode)
