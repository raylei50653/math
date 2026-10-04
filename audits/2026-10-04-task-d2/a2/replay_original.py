#!/usr/bin/env python3
"""Read-only two-seed replay of the original A2 checker; outputs beside script."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import time

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path('/tmp/math-task-d2-successor-v2'))
    args=parser.parse_args();out=Path(__file__).resolve().parent
    script='scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.py'
    artifact=args.repo/'artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12/observations.json'
    before=sha256(artifact.read_bytes()).hexdigest();checks=[]
    for seed in (None,'17'):
        env=os.environ.copy();env.pop('PYTHONHASHSEED',None)
        if seed is not None:env['PYTHONHASHSEED']=seed
        tag=seed or 'default';started=time.monotonic()
        p=subprocess.run(['python3',script,'--check'],cwd=args.repo,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (out/f'original.seed-{tag}.log').write_text(p.stdout)
        check=dict(seed=tag,command=f'python3 {script} --check',cwd=str(args.repo),exit_code=p.returncode,elapsed_seconds=round(time.monotonic()-started,3),log=f'original.seed-{tag}.log',status='PASS' if p.returncode==0 else 'FAIL')
        checks.append(check);print(json.dumps(check),flush=True)
    after=sha256(artifact.read_bytes()).hexdigest();assert before==after
    (out/'original_replay_results.json').write_text(json.dumps(dict(checks=checks,artifact_sha256_before=before,artifact_sha256_after=after,bytes_preserved=True),indent=2)+'\n')

if __name__=='__main__':main()
