#!/usr/bin/env python3
"""Record final read-only replay after the parent delivery metadata exists."""
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
AUDIT = ROOT/'audits/2026-10-10-n45-high23-supervision'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(seed):
    argv = ['python3','-B',str(AUDIT/'verify.py')]
    env = dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0')
    env.pop('PYTHONHASHSEED',None)
    if seed:
        env['PYTHONHASHSEED']='17'
    started=datetime.now(timezone.utc).isoformat()
    clock=time.monotonic()
    p=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True)
    return {'name':'seed17' if seed else 'normal','command':argv,'cwd':str(ROOT),
            'environment':{'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0','PYTHONHASHSEED':'17' if seed else 'unset'},
            'start_UTC':started,'elapsed_seconds':round(time.monotonic()-clock,3),
            'exit_code':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),
            'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}


def main():
    metadata={name:sha((AUDIT/name).read_bytes()) for name in ['manifest.json','delivery.json','receipt.json']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        executions=list(pool.map(run,[False,True]))
    assert metadata=={name:sha((AUDIT/name).read_bytes()) for name in metadata}
    result={'audit':'N45-HIGH23-SUPERVISION','parent_exact_metadata_sha256':metadata,
            'verifier_sha256':sha((AUDIT/'verify.py').read_bytes()),'executions':executions,
            'normal_seed17_stdout_identical':executions[0]['stdout']==executions[1]['stdout'],
            'sealed_parent_mutated':False}
    with (HERE/'high23-final-replays.json').open('x') as f:
        json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
    print(json.dumps({'exits':[x['exit_code'] for x in executions], 'stdout_identical':result['normal_seed17_stdout_identical'], 'normal_stdout':executions[0]['stdout']},sort_keys=True))
    assert all(x['exit_code']==0 for x in executions),executions
    assert result['normal_seed17_stdout_identical'] and executions[0]['stderr']==executions[1]['stderr']


if __name__ == '__main__':
    main()
