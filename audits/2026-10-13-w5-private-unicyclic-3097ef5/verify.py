#!/usr/bin/env python3
"""Local verification runner; exclusive logs/results, no old-audit mutation."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--phase', choices=['math','final'], required=True)
    args = ap.parse_args()
    py = ['python3', '-B']
    rel = str(ROOT.relative_to(REPO))
    if args.phase == 'math':
        jobs = [('kernel-normal', py+[rel+'/controls/check.py','--check'], {}),
                ('kernel-seed17', py+[rel+'/controls/check.py','--check'], {'PYTHONHASHSEED':'17'}),
                ('strength-normal', py+[rel+'/controls/strength.py','--check'], {}),
                ('strength-seed17', py+[rel+'/controls/strength.py','--check'], {'PYTHONHASHSEED':'17'})]
    else:
        jobs = [('docs', ['python3','scripts/check_docs.py'], {}),
                ('docgraph-formal', ['python3','tools/docgraph','--include','docs/**/*.md','check'], {}),
                ('diff-check', ['git','diff','--check'], {}),
                ('lean-regression', ['lake','build'], {})]
    output = ROOT/(args.phase+'-verification.json')
    assert not output.exists(), 'refuse to overwrite verification result'
    records = []
    for name, cmd, extra in jobs:
        log = ROOT/'logs'/(name+'.log')
        start = time.monotonic()
        with log.open('xb') as f:
            proc = subprocess.run(cmd, cwd=REPO, env={**os.environ,**extra}, stdout=f, stderr=subprocess.STDOUT)
        rec = {'name':name,'command':cmd,'env':extra,'exit_code':proc.returncode,
               'seconds':round(time.monotonic()-start,3),'log':str(log.relative_to(ROOT)),
               'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()}
        records.append(rec)
        print(json.dumps(rec),flush=True)
    result={'phase':args.phase,'records':records}
    if args.phase == 'math':
        result['kernel_normal_seed17_output_identical']=(ROOT/'logs/kernel-normal.log').read_bytes()==(ROOT/'logs/kernel-seed17.log').read_bytes()
        result['strength_normal_seed17_output_identical']=(ROOT/'logs/strength-normal.log').read_bytes()==(ROOT/'logs/strength-seed17.log').read_bytes()
    with output.open('x') as f:
        json.dump(result,f,indent=2,sort_keys=True); f.write('\n')
    assert all(r['exit_code']==0 for r in records)
    assert all(v for k,v in result.items() if k.endswith('_identical'))


if __name__=='__main__':
    main()
