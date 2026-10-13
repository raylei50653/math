#!/usr/bin/env python3
"""Replay independent exact count and fixed-split cone checks."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import time
HERE=Path(__file__).resolve().parent
RUNS=[('count-normal','count_feasibility.py',False,True),('count-seed17','count_feasibility.py',True,False),
      ('cone-normal','kempe_cone_check.py',False,True),('cone-seed17','kempe_cone_check.py',True,False)]
def run(arg):
    name,script,seed,negative=arg
    cmd=['python3','-B',str(HERE/script),'--check']+(['--negative'] if negative else [])
    env=dict(os.environ)
    if seed:env['PYTHONHASHSEED']='17'
    start=time.monotonic();p=subprocess.run(cmd,text=True,capture_output=True,env=env)
    (HERE/(name+'.stdout')).write_text(p.stdout);(HERE/(name+'.stderr')).write_text(p.stderr)
    return {'name':name,'command':cmd,'PYTHONHASHSEED':env.get('PYTHONHASHSEED'),'exit_code':p.returncode,
            'elapsed_seconds':round(time.monotonic()-start,3),'stdout':p.stdout,'stderr':p.stderr}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,RUNS))
receipt={'status':'PASS' if all(r['exit_code']==0 for r in results) else 'FAIL','runs':results}
(HERE/'VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps([(r['name'],r['exit_code'],r['elapsed_seconds']) for r in results]))
assert receipt['status']=='PASS'
