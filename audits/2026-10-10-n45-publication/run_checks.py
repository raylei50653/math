#!/usr/bin/env python3
"""Capture true execution provenance for publication checks; never overwrite logs."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


def run(name,argv,cwd=ROOT,seed=None,expected=0,stdin=None):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
    env.pop('PYTHONHASHSEED',None)
    if seed is not None:env['PYTHONHASHSEED']=str(seed)
    started=datetime.now(timezone.utc).isoformat();clock=time.monotonic()
    result=subprocess.run(argv,cwd=cwd,env=env,input=stdin,capture_output=True)
    record={'name':name,'command':argv,'cwd':str(cwd),'environment':{'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0','PYTHONHASHSEED':str(seed) if seed is not None else 'unset'},'start_UTC':started,'elapsed_seconds':round(time.monotonic()-clock,3),'exit_code':result.returncode,'expected_exit':expected}
    for channel,data in [('stdout',result.stdout),('stderr',result.stderr)]:
        path=HERE/'logs'/(name+'.'+channel+'.txt')
        with path.open('xb') as f:f.write(data)
        record[channel]=str(path.relative_to(HERE));record[channel+'_sha256']=hashlib.sha256(data).hexdigest()
    if stdin is not None:record['stdin_sha256']=hashlib.sha256(stdin).hexdigest()
    with (HERE/'logs'/(name+'.receipt.json')).open('x') as f:json.dump(record,f,ensure_ascii=False,indent=2);f.write('\n')
    return record


def main():
    jobs=[('lake-build',['lake','build'])]
    results=[run(name,argv) for name,argv in jobs]
    print(json.dumps({x['name']:x['exit_code'] for x in results},sort_keys=True))
    assert all(x['exit_code']==x['expected_exit'] for x in results)


if __name__=='__main__':main()
